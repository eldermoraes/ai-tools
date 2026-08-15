#!/usr/bin/env python3
"""telegram — despacha texto e arquivos para um bot do Telegram.

O braco deterministico da skill `telegram`: nao decide o que enviar, so envia.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import secrets
import sys
import traceback
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# --- protocolo (Bot API) -------------------------------------------------
API_BASE = "https://api.telegram.org"
HTTP_TIMEOUT = 60
# O limite do Telegram e 4096 code units UTF-16. Cortamos em 4000: a margem de
# 96 apaga a classe inteira de erro de borda (spec §3).
CHUNK_BUDGET = 4000
CAPTION_LIMIT = 1024
MAX_FILE_BYTES = 50 * 1024 * 1024

# --- config --------------------------------------------------------------
CONFIG_DIR = Path.home() / ".claude" / "telegram"
ENV_PATH = CONFIG_DIR / ".env"


# --- erros: cada classe carrega o exit code de §6 ------------------------
class TelegramError(Exception):
    code = 1


class ConfigError(TelegramError):
    code = 1


class ApiError(TelegramError):
    code = 2


class InputError(TelegramError):
    code = 3


# --- medicao em code units UTF-16 ---------------------------------------
def utf16_len(s: str) -> int:
    """Largura da string como o Telegram conta: code units UTF-16."""
    return len(s.encode("utf-16-le")) // 2


def _cu_width(ch: str) -> int:
    return 2 if ord(ch) > 0xFFFF else 1


def truncate_utf16(s: str, budget: int) -> str:
    """Maior prefixo de `s` que cabe em `budget` code units UTF-16.

    Percorre *codepoints* acumulando largura. E por isso que nunca *parte* um
    par surrogate: `str` do Python e sequencia de codepoints, e o emoji e um
    unico elemento. (Surrogate solto que ja venha na entrada -- via
    surrogateescape no `sys.argv`, por exemplo -- passa intacto.) A
    implementacao proibida e medir em UTF-16 e fatiar o buffer de bytes --
    `s.encode("utf-16-le")[:budget * 2]` parte o par no meio (spec §7).
    """
    if budget <= 0:
        return ""
    total = 0
    out = []
    for ch in s:
        w = _cu_width(ch)
        if total + w > budget:
            break
        total += w
        out.append(ch)
    return "".join(out)


# --- mascaramento do token em toda saida (spec §8) -----------------------
# Token de bot tem o formato <id numerico>:<35 chars>. O regex existe para pegar
# token que nao e o nosso -- o que a API as vezes ecoa de volta em erro.
_TOKEN_SHAPE = re.compile(r"\d{6,12}:[A-Za-z0-9_-]{30,}")

# Preenchida por load_token(). O filtro le daqui porque o excepthook nao recebe
# contexto nenhum -- e e justamente no traceback inesperado que o token vaza.
_ACTIVE_TOKEN: str | None = None


def mask(text: str, token: str | None = None) -> str:
    """Substitui o token (e qualquer coisa com formato de token) por <TOKEN>."""
    alvo = token if token is not None else _ACTIVE_TOKEN
    if alvo:
        text = text.replace(alvo, "<TOKEN>")
    return _TOKEN_SHAPE.sub("<TOKEN>", text)


def emit(line: str) -> None:
    print(mask(line))


def fail(line: str) -> None:
    print(mask(line), file=sys.stderr)


def token_preview(token: str) -> str:
    """Preview seguro para o --doctor: `123456:AB…` (spec §6).

    Sem os dois pontos nao existe id de bot para mostrar: `partition` jogaria o
    token inteiro em `bot_id` e o preview sairia completo -- e o regex de formato
    nao salva, porque string sem dois pontos nao tem formato de token. Entao
    recusa em vez de adivinhar onde termina a parte publica.
    """
    bot_id, sep, resto = token.partition(":")
    if not sep or not resto:
        return "<malformado>"
    return f"{bot_id}:{resto[:2]}…"


def _excepthook(exc_type, exc, tb) -> None:
    """Ultima linha de defesa: traceback inesperado tambem passa pelo filtro."""
    texto = "".join(traceback.format_exception(exc_type, exc, tb))
    sys.stderr.write(mask(texto))


# --- fatiamento ----------------------------------------------------------
# Nao aceita fronteira de separador que deixe o pedaco com menos da metade do
# orcamento: sem isso, um "\n\n" no caractere 10 de um texto de 9000 geraria um
# pedaco de 10 chars e uma mensagem a mais, sem ganho de legibilidade.
MIN_FILL_RATIO = 0.5


def _split_plain(text: str, budget: int) -> list[str]:
    """Fatia sem prefixo. Invariante: "".join(resultado) == text."""
    # 2 e a menor largura que cabe um codepoint qualquer (fora do BMP sao 2 code
    # units). Com budget >= 2, `truncate_utf16` devolve pelo menos um caractere,
    # entao `cut >= 1` e o laco abaixo sempre avanca -- e por construcao que ele
    # termina. Com budget == 1 e um emoji na frente, `head` sai vazio e o `rest`
    # nunca encolhe.
    if budget < 2:
        raise ValueError("budget precisa ser >= 2")
    pieces: list[str] = []
    rest = text
    while utf16_len(rest) > budget:
        head = truncate_utf16(rest, budget)
        cut = len(head)
        floor = int(len(head) * MIN_FILL_RATIO)
        for sep in ("\n\n", "\n"):
            idx = head.rfind(sep)
            if idx > 0 and idx >= floor:
                cut = idx + len(sep)  # o separador fica no fim do pedaco
                break
        pieces.append(rest[:cut])
        rest = rest[cut:]
    pieces.append(rest)
    return pieces


def _prefix(i: int, n: int) -> str:
    return f"[{i}/{n}]\n"


def split_text(text: str, budget: int = CHUNK_BUDGET) -> list[str]:
    """Fatia `text` em mensagens que cabem em `budget` code units UTF-16.

    O prefixo `[i/n]` entra no orcamento (§7), mas `n` so existe depois de
    fatiar -- entao isso e um ponto fixo: fatia, reserva o prefixo do `n` que
    saiu, refatia. Termina porque `n` cresce a cada volta e a reserva so muda
    quando o numero de digitos de `n` muda.
    """
    pieces = _split_plain(text, budget)
    if len(pieces) == 1:
        return pieces  # uma mensagem so: sem prefixo (§7)
    n = len(pieces)
    while True:
        reserve = utf16_len(_prefix(n, n))  # pior caso: i tem os digitos de n
        candidate = _split_plain(text, budget - reserve)
        if len(candidate) <= n:
            pieces = candidate
            break
        n = len(candidate)
    total = len(pieces)
    return [_prefix(i, total) + p for i, p in enumerate(pieces, 1)]


# --- config: .env, precedencia assimetrica e allowlist (spec §8) ---------
# [0-9] e nao \d: em `str`, o \d do Python e Unicode-aware e casa com digito
# arabico-indiano, devanagari etc. Isso derrotaria o portao -- a entrada passaria
# a validacao que existe para explodir na subida e morreria depois na API, com
# exit 2 e sem eco da entrada ofensora.
_ID_SHAPE = re.compile(r"-?[0-9]+")


@dataclass
class Config:
    token: str
    chat_id: str
    token_source: str  # "ambiente" | ".env"
    env_mode: int | None


def parse_env_file(text: str) -> dict[str, str]:
    """Parser minimo de .env: KEY=VALOR, com # de comentario e aspas opcionais."""
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        key, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out[key.strip()] = value
    return out


def check_env_mode(path: Path) -> int:
    """Recusa .env legivel por group/other. Permissao e verificada, nao assumida
    -- o caminho preferido (usuario escreve o arquivo a mao) cria com o umask do
    shell, tipicamente 644 (spec §8).
    """
    mode = path.stat().st_mode & 0o777
    if mode & 0o077:
        raise ConfigError(
            f"{path} está com modo {mode:o}: segredo legível por outros usuários. "
            f"Rode: chmod 600 {path}"
        )
    return mode


def read_env(env_path: Path | None = None) -> tuple[dict[str, str], int | None]:
    path = ENV_PATH if env_path is None else env_path
    if not path.exists():
        return {}, None
    mode = check_env_mode(path)
    return parse_env_file(path.read_text(encoding="utf-8")), mode


def parse_allowlist(raw: str) -> list[str]:
    """Valida a allowlist explodindo na subida.

    Entrada malformada nunca vira lista parcial em silencio: um id digitado
    errado manda pra um chat que nao e o usuario, e a mensagem sai antes de
    alguem perceber (spec §8, padrao herdado do irfp).
    """
    entries = [e.strip() for e in raw.split(",") if e.strip()]
    if not entries:
        raise ConfigError(
            "TELEGRAM_ALLOWED_CHATS está vazia. Rode: python3 telegram.py --setup"
        )
    for entry in entries:
        if not _ID_SHAPE.fullmatch(entry):
            raise ConfigError(
                f"entrada inválida em TELEGRAM_ALLOWED_CHATS: {entry!r}. "
                "Ids são dígitos (com '-' opcional para grupo), separados por vírgula. "
                "Nada foi enviado."
            )
    return entries


def load_token(env=None, filevars=None) -> tuple[str, str]:
    """Token: ambiente primeiro, depois .env. Preenche _ACTIVE_TOKEN."""
    global _ACTIVE_TOKEN
    env = os.environ if env is None else env
    filevars = {} if filevars is None else filevars
    token = env.get("TELEGRAM_BOT_TOKEN")
    source = "ambiente"
    if not token:
        token = filevars.get("TELEGRAM_BOT_TOKEN")
        source = ".env"
    if not token:
        raise ConfigError(
            "TELEGRAM_BOT_TOKEN não configurado. Escreva o token do @BotFather em "
            f"{ENV_PATH} (crie o diretório, depois chmod 600 no arquivo)."
        )
    _ACTIVE_TOKEN = token
    return token, source


def load_config(env=None, env_path: Path | None = None) -> Config:
    """Config completa para os modos de envio.

    Assimetria deliberada (spec §8): o token aceita ambiente; a allowlist, nao.
    Como o Claude roda comandos, dar precedencia de ambiente a allowlist seria
    dar a ele uma flag de override de destino -- exatamente o que o desenho nega.
    """
    path = ENV_PATH if env_path is None else env_path
    filevars, mode = read_env(path)
    token, source = load_token(env, filevars)
    raw = filevars.get("TELEGRAM_ALLOWED_CHATS")
    if not raw:
        raise ConfigError(
            f"TELEGRAM_ALLOWED_CHATS não está em {path}. A variável de ambiente é "
            "ignorada para o destino, por desenho. Rode: python3 telegram.py --setup"
        )
    ids = parse_allowlist(raw)
    if len(ids) > 1:
        raise ConfigError(
            f"allowlist com {len(ids)} entradas ({', '.join(ids)}): destino ambíguo. "
            f"Deixe uma entrada só em {path}."
        )
    return Config(token=token, chat_id=ids[0], token_source=source, env_mode=mode)


# --- transporte HTTP: uma unica costura de rede (spec §3) ----------------
def _urlopen(req):
    """Unico ponto de rede do script -- e a costura que os testes substituem.

    Nao chame urllib.request.urlopen em nenhum outro lugar: se chamar, existe um
    caminho de codigo que os testes automatizados nao alcancam.
    """
    return urllib.request.urlopen(req, timeout=HTTP_TIMEOUT)


def _api_error_message(method: str, payload: dict, status: int | None = None) -> str:
    desc = payload.get("description") or "resposta sem description"
    # O status entra na mensagem porque um corpo de erro que *e* JSON mas nao tem
    # `description` (proxy no meio do caminho, por exemplo) apagaria o 502 -- e
    # diagnosticabilidade e o unico trabalho desta camada.
    onde = method if status is None else f"{method} (HTTP {status})"
    msg = f"Telegram recusou {onde}: {desc}"
    retry = (payload.get("parameters") or {}).get("retry_after")
    if retry is not None:
        msg += f" (retry_after: {retry}s; o script não retenta -- decisão sua)"
    return msg


def _call(token: str, method: str, body: bytes, content_type: str) -> Any:
    """Faz a chamada e devolve o campo `result` da resposta.

    O tipo de retorno e Any de proposito: `result` vem `dict` em sendMessage,
    `list` em getUpdates, `True` em varios metodos e `None` se a resposta vier
    `ok: true` sem `result`. Anotar `dict` seria mentira para quem le.

    Nenhuma excecao de rede, de decodificacao ou de parsing escapa daqui: tudo
    vira ApiError (exit 2). E para isso que esta camada existe.
    """
    url = f"{API_BASE}/bot{token}/{method}"
    req = urllib.request.Request(url, data=body, headers={"Content-Type": content_type})
    status = None
    try:
        with _urlopen(req) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as err:  # subclasse de URLError: vem primeiro
        status = err.code
        try:
            raw = err.read()
        except OSError as erro_leitura:
            # err.fp e o socket vivo, entao ler o corpo do erro pode dar o mesmo
            # timeout que a leitura da resposta normal -- um ramo ao lado, o mesmo
            # evento fisico. Excecao levantada aqui dentro nao e pega pelas
            # clausulas irmas deste try, entao escaparia do _call. A mensagem diz
            # que a *leitura* falhou em vez de fingir que o corpo veio vazio: um
            # 502 cujo corpo nao pode ser lido e outro diagnostico.
            raise ApiError(
                f"falha ao ler o corpo do erro (HTTP {status}) em {method}: "
                f"{erro_leitura}"
            ) from None
        finally:
            # No finally para rodar nos dois caminhos: sem o close o 3.14 solta
            # ResourceWarning no GC, e no caminho de falha o socket vazaria.
            err.close()
    except urllib.error.URLError as err:
        raise ApiError(f"falha de rede em {method}: {err.reason}") from None
    except OSError as err:
        # URLError herda de OSError, entao esta clausula fica *depois* dela.
        # Existe porque timeout de leitura -- que acontece depois de os
        # cabecalhos chegarem, ja dentro do resp.read() -- sobe como TimeoutError
        # puro, sem embrulho de URLError, e escaparia das duas clausulas acima.
        raise ApiError(f"falha de rede em {method}: {err}") from None
    # "replace" e nao strict: corpo em bytes invalidos viraria UnicodeDecodeError,
    # que e justamente o traceback que esta camada existe para nao deixar subir.
    text = raw.decode("utf-8", "replace")
    # O status entra como aposto, nao como "em HTTP 502 em sendMessage": quem le
    # isso esta confuso, e a mensagem precisa ser uma frase. O trecho do corpo vai
    # junto porque e o que diz *quem* respondeu no lugar do Telegram.
    http = "" if status is None else f" (HTTP {status})"
    try:
        payload = json.loads(text)
    except ValueError:  # JSONDecodeError herda de ValueError
        raise ApiError(f"resposta não é JSON{http} em {method}: {text[:200]}") from None
    if not isinstance(payload, dict):
        # `null`, `[1,2]` e `"texto"` sao JSON *valido*: passam pelo json.loads e
        # so estouram um passo depois, com AttributeError no .get() abaixo. E o
        # mesmo furo do json.loads sem guarda, um degrau adiante.
        raise ApiError(f"resposta não é objeto JSON{http} em {method}: {text[:200]}")
    if not payload.get("ok"):
        raise ApiError(_api_error_message(method, payload, status))
    return payload.get("result")


def api_post(token: str, method: str, fields: dict) -> Any:
    body = urllib.parse.urlencode(fields).encode("utf-8")
    return _call(token, method, body, "application/x-www-form-urlencoded")


def api_upload(
    token: str, method: str, fields: dict, field_name: str, path: Path
) -> Any:
    """Multipart montado a mao: a stdlib nao monta, e a dependencia externa que
    montaria custa mais que estas 15 linhas (spec §3).
    """
    boundary = "telegram" + secrets.token_hex(16)
    # So o nome do arquivo e sanitizado, e a assimetria e proposital: as chaves de
    # `fields` sao literais do proprio codigo, e um *valor* nao consegue quebrar o
    # framing porque a fronteira carrega 128 bits de secrets.token_hex(16) -- o
    # atacante teria que adivinha-la. O nome do arquivo, nao: e entrada do usuario
    # e vai cru para dentro de um cabecalho.
    filename = path.name.replace('"', "_").replace("\r", "_").replace("\n", "_")
    out = bytearray()
    for key, value in fields.items():
        out += f"--{boundary}\r\n".encode("utf-8")
        out += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8")
        out += f"{value}\r\n".encode("utf-8")
    out += f"--{boundary}\r\n".encode("utf-8")
    out += (
        f'Content-Disposition: form-data; name="{field_name}"; '
        f'filename="{filename}"\r\n'
    ).encode("utf-8")
    out += b"Content-Type: application/octet-stream\r\n\r\n"
    out += path.read_bytes()
    out += b"\r\n"
    out += f"--{boundary}--\r\n".encode("utf-8")
    return _call(token, method, bytes(out), f"multipart/form-data; boundary={boundary}")


# --- denylist e validacao de arquivos ------------------------------------
# Piso deterministico, nao lista exaustiva (spec §8). Comparado contra o caminho
# ja resolvido (realpath), pra nao ser burlado por symlink ou "..".
# No fnmatch, `*` atravessa `/` -- entao `~/.ssh/*` cobre subdiretorio tambem.
DENY_PATTERNS = (
    "~/.claude/telegram/.env",
    "~/.ssh/*",
    "~/.aws/credentials",
    "~/.netrc",
    "*/id_rsa*",
    "*/id_ed25519*",
    "*/*.pem",
    "*/*.p12",
    "*/*.kdbx",
    "*/.env",
    "*/.env.*",
)


def denied_by(path: Path) -> str | None:
    """Padrao que casou, ou None. `path` tem que vir resolvido.

    A caixa e baixada dos dois lados antes de comparar: os.path.normcase (que o
    fnmatch.fnmatch usaria) e identidade em POSIX, inclusive Darwin, mas o APFS
    padrao e case-insensitive -- sem isso, ID_RSA alcancaria o arquivo real e
    escaparia da regra.
    """
    alvo = str(path).lower()
    for pattern in DENY_PATTERNS:
        if fnmatch.fnmatchcase(alvo, os.path.expanduser(pattern).lower()):
            return pattern
    return None


def human_size(n: int) -> str:
    if n >= 1024 * 1024:
        return f"{n / (1024 * 1024):.1f} MB"
    if n >= 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n} B"


def validate_files(raw_paths: list[str]) -> list[Path]:
    """Valida TODOS antes de qualquer envio (spec §6). Ordem de checagem:
    denylist, existencia, tamanho -- a denylist primeiro pra que uma chave que
    nao existe nesta maquina ainda receba a mensagem que ensina a regra.
    """
    resolved: list[Path] = []
    for raw in raw_paths:
        path = Path(raw).expanduser()
        try:
            path = path.resolve()
        except OSError as err:
            raise InputError(f"caminho inválido: {raw} ({err}). Nada foi enviado.") from None
        pattern = denied_by(path)
        if pattern:
            raise InputError(
                f"caminho na denylist ({pattern}): {path}. "
                "Sem override, por desenho. Nada foi enviado."
            )
        if not path.is_file():
            raise InputError(f"arquivo não encontrado: {path}. Nada foi enviado.")
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            raise InputError(
                f"arquivo de {human_size(size)} passa do limite de 50 MB do "
                f"sendDocument: {path}. Nada foi enviado."
            )
        resolved.append(path)
    return resolved


# --- envio: texto primeiro, depois arquivos na ordem (spec §6) ------------
def _check_utf16_encodable(s: str, o_que: str) -> None:
    """Fronteira de entrada: argv/stdin com bytes invalidos chega como
    surrogate solto (surrogateescape) e estouraria UnicodeEncodeError dentro de
    utf16_len -- traceback mascarado com exit 1 em vez de InputError com 3.
    """
    try:
        s.encode("utf-16-le")
    except UnicodeEncodeError:
        raise InputError(
            f"{o_que} contém bytes inválidos (surrogate solto): "
            "não dá para codificar em UTF-16. Nada foi enviado."
        ) from None


def prepare_caption(caption: str) -> str:
    """Legenda tem limite proprio de 1024 code units UTF-16 (spec §7).

    Trunca e avisa, em vez de deixar a API recusar o upload inteiro por causa da
    legenda -- o arquivo e o que importa.
    """
    largura = utf16_len(caption)
    if largura <= CAPTION_LIMIT:
        return caption
    emit(
        f"aviso: legenda truncada de {largura} para {CAPTION_LIMIT} code units UTF-16"
    )
    return truncate_utf16(caption, CAPTION_LIMIT)


def send_text(cfg: Config, text: str) -> None:
    pieces = split_text(text)
    total = len(pieces)
    for i, piece in enumerate(pieces, 1):
        api_post(cfg.token, "sendMessage", {"chat_id": cfg.chat_id, "text": piece})
        # sufixo de contagem so quando ha mais de uma mensagem (spec §6)
        emit("ok: texto" if total == 1 else f"ok: texto ({i}/{total})")


def send_file(cfg: Config, path: Path, caption: str | None = None) -> None:
    fields = {"chat_id": cfg.chat_id}
    if caption:
        fields["caption"] = caption
    api_upload(cfg.token, "sendDocument", fields, "document", path)
    emit(f"ok: documento {path.name} ({human_size(path.stat().st_size)})")


def cmd_send(
    text: str | None,
    raw_files: list[str],
    caption: str | None = None,
    env=None,
    env_path: Path | None = None,
) -> int:
    """Ordem deliberada: valida entrada, carrega config, depois envia.

    Validar antes de carregar config faz a mensagem de erro ser sobre o que o
    usuario errou (arquivo faltando) e nao sobre config -- e garante o
    tudo-ou-nada de §6, porque a validacao inteira acontece antes do 1o envio.
    A garantia acaba ai: se a API falhar no meio de um lote validado, o que ja
    saiu saiu, e a saida diz exatamente o que foi entregue.
    """
    if text == "-":
        text = sys.stdin.read()
    if text is not None and not text.strip():
        raise InputError("texto vazio: nada a enviar")
    if text is not None:
        _check_utf16_encodable(text, "texto")
    if caption is not None:
        _check_utf16_encodable(caption, "legenda")
    paths = validate_files(list(raw_files))
    cfg = load_config(env, env_path)
    if text is not None:
        send_text(cfg, text)
    legenda = prepare_caption(caption) if caption else None
    for i, path in enumerate(paths):
        send_file(cfg, path, legenda if i == 0 else None)
    return 0


# --- setup: descobrir o chat_id e gravar a allowlist (spec §6) ------------
def _candidates(updates) -> list[dict]:
    """Chats vistos no getUpdates, deduplicados, na ordem em que apareceram."""
    vistos: dict[str, dict] = {}
    for upd in updates or []:
        for key in ("message", "edited_message", "channel_post"):
            msg = upd.get(key)
            if not msg:
                continue
            chat = msg.get("chat") or {}
            if chat.get("id") is None:
                continue
            nome = chat.get("title") or " ".join(
                p for p in (chat.get("first_name"), chat.get("last_name")) if p
            )
            vistos[str(chat["id"])] = {
                "id": str(chat["id"]),
                "name": nome or "(sem nome)",
                "username": f"@{chat['username']}" if chat.get("username") else "(sem username)",
                "type": chat.get("type", "?"),
            }
    return list(vistos.values())


def write_env_var(key: str, value: str, env_path: Path | None = None) -> Path:
    """Grava uma chave no .env preservando as outras. Substitui, nao acrescenta.

    Escreve num temporario com modo 600 e troca com os.replace, pra nunca deixar
    o arquivo num estado meio-escrito nem com permissao larga por um instante.
    """
    path = ENV_PATH if env_path is None else env_path
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    existing: dict[str, str] = {}
    if path.exists():
        check_env_mode(path)
        existing = parse_env_file(path.read_text(encoding="utf-8"))
    existing[key] = value
    tmp = path.parent / (path.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write("".join(f"{k}={v}\n" for k, v in existing.items()))
    os.replace(tmp, path)
    os.chmod(path, 0o600)
    return path


def cmd_setup(
    chat_id: str | None = None, env=None, env_path: Path | None = None
) -> int:
    path = ENV_PATH if env_path is None else env_path
    filevars, _ = read_env(path)
    token, source = load_token(env, filevars)
    # Regra 5 de §6: o --setup configura allowlist que nao existe, e nao troca a que
    # existe. Sem isso, o --setup seria a rota de override de destino que a v3
    # eliminou -- dois comandos e o destino muda, sem sair da sessao (§8).
    if filevars.get("TELEGRAM_ALLOWED_CHATS"):
        raise ConfigError(
            f"a allowlist já está configurada em {path}. O --setup não troca destino: "
            "rode --doctor para ver o que está gravado e edite o arquivo à mão (ou "
            "apague a linha TELEGRAM_ALLOWED_CHATS) se quiser mudar."
        )
    updates = api_post(token, "getUpdates", {"timeout": 0})
    candidatos = _candidates(updates)
    if not candidatos:
        raise ConfigError(
            "getUpdates não devolveu nenhum chat. Manda qualquer DM pro bot e roda "
            "de novo.\n"
            "Se você já mandou, as causas são duas e diferentes (spec §12):\n"
            "  - webhook ativo: a API responde 409, porque webhook e getUpdates são "
            "mutuamente exclusivos. Remova o webhook.\n"
            "  - outro poller com o mesmo token (o plugin oficial, por exemplo): a "
            "lista vem vazia, porque o offset é estado compartilhado por token e "
            "quem confirma primeiro consome para todos. Pare o outro processo."
        )
    if chat_id is None:
        emit(
            "candidatos encontrados -- confirme QUAL é você. Um candidato único não é "
            "prova de nada: quem mandou DM pro bot antes de você aparece aqui."
        )
        for cand in candidatos:
            emit(f"  {cand['id']}  {cand['name']}  {cand['username']}  [{cand['type']}]")
        emit("")
        emit("grave a allowlist com: python3 telegram.py --setup --chat-id <ID>")
        return 1
    if chat_id not in {cand["id"] for cand in candidatos}:
        raise ConfigError(
            f"{chat_id} não está entre os candidatos do getUpdates. A allowlist só "
            "recebe um chat que mandou DM pro bot; rode --setup sem --chat-id para "
            "ver a lista."
        )
    parse_allowlist(chat_id)  # mesma validacao do caminho de leitura
    destino = write_env_var("TELEGRAM_ALLOWED_CHATS", chat_id, path)
    emit(f"allowlist gravada em {destino}: {chat_id} (substituiu o valor anterior, se havia)")
    emit(f"token: {token_preview(token)} (fonte: {source})")
    return 0


# --- doctor: diagnostico sem expor segredo (spec §6, §9) ------------------
def cmd_doctor(env=None, env_path: Path | None = None) -> int:
    """Reporta config sem expor segredo (spec §6).

    Cada problema e contado em vez de levantado: o valor do --doctor e mostrar
    tudo de uma vez, nao parar no primeiro defeito.
    """
    ambiente = os.environ if env is None else env
    path = ENV_PATH if env_path is None else env_path
    problemas = 0
    filevars: dict[str, str] = {}

    if not path.exists():
        emit(f".env: {path} não existe")
        problemas += 1
    else:
        try:
            mode = check_env_mode(path)
        except ConfigError as err:
            emit(f".env: {err}")
            return 1  # permissao larga e bloqueante: o resto nem se le
        emit(f".env: {path} (modo {mode:o})")
        filevars = parse_env_file(path.read_text(encoding="utf-8"))

    try:
        token, source = load_token(ambiente, filevars)
        emit(f"token: configurado (fonte: {source}) - {token_preview(token)}")
    except ConfigError:
        emit("token: ausente - escreva TELEGRAM_BOT_TOKEN no .env")
        problemas += 1

    raw = filevars.get("TELEGRAM_ALLOWED_CHATS")
    if not raw:
        emit(
            "allowlist: ausente no .env - rode --setup "
            "(a variável de ambiente é ignorada para o destino, por desenho)"
        )
        problemas += 1
    else:
        try:
            ids = parse_allowlist(raw)
        except ConfigError as err:
            emit(f"allowlist: {err}")
            problemas += 1
        else:
            emit(f"allowlist: {len(ids)} entrada(s) - {', '.join(ids)}")
            if len(ids) > 1:
                emit("allowlist: ambígua - o envio vai recusar. Deixe uma entrada só")
                problemas += 1

    if ambiente.get("TELEGRAM_ALLOWED_CHATS"):
        emit(
            "aviso: TELEGRAM_ALLOWED_CHATS existe no ambiente e está sendo "
            "ignorada, como manda o desenho"
        )

    emit("diagnóstico: ok" if problemas == 0 else f"diagnóstico: {problemas} problema(s)")
    return 0 if problemas == 0 else 1


# --- CLI: exclusividade de modos e exit codes (spec §6) -------------------
class _Parser(argparse.ArgumentParser):
    def error(self, message):  # noqa: A003
        # O default do argparse e sair com 2 -- que neste contrato significa
        # "erro da API do Telegram" (spec §6). Uso invalido e erro de entrada: 3.
        raise InputError(f"uso inválido: {message}")


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(
        prog="telegram.py",
        description="Despacha texto e arquivos para o seu bot do Telegram.",
        epilog=(
            "O destino vem sempre da allowlist em ~/.claude/telegram/.env. "
            "Não existe flag de destino nos modos de envio."
        ),
    )
    parser.add_argument("--text", metavar="TEXTO", help="texto a enviar; '-' lê do stdin")
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        metavar="CAMINHO",
        help="arquivo a enviar como documento (pode repetir)",
    )
    parser.add_argument("--caption", metavar="TEXTO", help="legenda do primeiro arquivo")
    parser.add_argument(
        "--setup", action="store_true", help="descobre o chat_id e grava a allowlist"
    )
    parser.add_argument(
        "--doctor", action="store_true", help="diagnóstico de config, sem expor segredo"
    )
    parser.add_argument(
        "--chat-id",
        dest="chat_id",
        metavar="ID",
        help="só dentro do --setup: qual chat entra na allowlist",
    )
    return parser


def run(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    envio = args.text is not None or bool(args.file)
    modos = [bool(args.setup), bool(args.doctor), envio]
    if sum(modos) == 0:
        raise InputError(
            "nada a fazer: use --text, --file, --setup ou --doctor (--help lista tudo)"
        )
    if sum(modos) > 1:
        raise InputError(
            "cada execução faz uma coisa só: envio (--text/--file), --setup ou --doctor"
        )
    if args.chat_id is not None and not args.setup:
        raise InputError(
            "--chat-id existe apenas dentro do --setup. O destino de envio vem da "
            "allowlist no .env, nunca de argumento"
        )
    if args.caption is not None and not args.file:
        raise InputError("--caption exige --file; para mandar texto solto use --text")
    if args.setup:
        return cmd_setup(args.chat_id)
    if args.doctor:
        return cmd_doctor()
    return cmd_send(args.text, args.file, args.caption)


def main(argv: list[str] | None = None) -> int:
    try:
        return run(sys.argv[1:] if argv is None else argv)
    except TelegramError as err:
        fail(f"erro: {err}")
        return err.code


if __name__ == "__main__":
    # O hook fica aqui, e nao dentro de main(), pra que importar o modulo (nos
    # testes) nao mexa em estado global do processo.
    sys.excepthook = _excepthook
    sys.exit(main())
