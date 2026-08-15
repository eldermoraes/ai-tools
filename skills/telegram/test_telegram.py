#!/usr/bin/env python3
"""Testes das funcoes puras do telegram. Sem rede, sem token.

Rodar: python3 skills/telegram/test_telegram.py -v
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import telegram as c  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "telegram.py"


def has_lone_surrogate(s):
    """True se a string contem metade de um par surrogate (caractere invalido)."""
    return any(0xD800 <= ord(ch) <= 0xDFFF for ch in s)


class TestUtf16(unittest.TestCase):
    def test_ascii_conta_um_por_caractere(self):
        self.assertEqual(c.utf16_len("abc"), 3)

    def test_emoji_fora_do_bmp_conta_dois(self):
        # 'a' = 1 code unit, emoji = par surrogate = 2 code units
        self.assertEqual(c.utf16_len("a\U0001F600"), 3)
        self.assertEqual(len("a\U0001F600"), 2)  # len() do Python discorda: dai o bug

    def test_truncate_nao_estoura_o_orcamento(self):
        s = "a" + "\U0001F600" * 10
        cut = c.truncate_utf16(s, 4)
        self.assertLessEqual(c.utf16_len(cut), 4)

    def test_truncate_nao_parte_par_surrogate(self):
        # orcamento 4: cabe 'a' (1) + 1 emoji (2) = 3; o proximo emoji estouraria
        cut = c.truncate_utf16("a" + "\U0001F600" * 10, 4)
        self.assertEqual(cut, "a\U0001F600")
        self.assertFalse(has_lone_surrogate(cut))

    def test_truncate_orcamento_zero_ou_negativo(self):
        self.assertEqual(c.truncate_utf16("abc", 0), "")
        self.assertEqual(c.truncate_utf16("abc", -5), "")

    def test_constantes_do_protocolo(self):
        self.assertEqual(c.CHUNK_BUDGET, 4000)
        self.assertEqual(c.CAPTION_LIMIT, 1024)
        self.assertEqual(c.MAX_FILE_BYTES, 50 * 1024 * 1024)
        self.assertEqual(c.ConfigError.code, 1)
        self.assertEqual(c.ApiError.code, 2)
        self.assertEqual(c.InputError.code, 3)


class TestSplit(unittest.TestCase):
    def test_1_texto_de_10000_chars_cabe_no_orcamento_com_prefixo(self):
        pieces = c.split_text("x" * 10000)
        self.assertGreater(len(pieces), 1)
        for p in pieces:
            self.assertLessEqual(c.utf16_len(p), c.CHUNK_BUDGET)
        self.assertTrue(pieces[0].startswith("[1/"))

    def test_2_quebra_na_fronteira_de_paragrafo(self):
        paragrafo = "palavra " * 60          # ~480 chars
        text = "\n\n".join([paragrafo] * 20)  # ~9600 chars
        pieces = c.split_text(text)
        self.assertGreater(len(pieces), 1)
        corpo = [p.split("\n", 1)[1] for p in pieces]  # tira o prefixo "[i/n]\n"
        for p in corpo[:-1]:
            self.assertTrue(p.endswith("\n\n"), f"cortou fora da fronteira: {p[-20:]!r}")

    def test_3_exatamente_4000_code_units_vira_uma_mensagem_sem_prefixo(self):
        text = "y" * 4000
        pieces = c.split_text(text)
        self.assertEqual(pieces, [text])
        self.assertNotIn("[1/1]", pieces[0])

    def test_4_emoji_fora_do_bmp_conta_dois_e_forca_a_segunda_mensagem(self):
        # 3000 codepoints, 2000 deles emoji => 1000 + 4000 = 5000 code units.
        # Com len() do Python isso "cabe" em 4000 e o Telegram devolveria 400.
        text = "a" * 1000 + "\U0001F600" * 2000
        self.assertEqual(len(text), 3000)
        self.assertEqual(c.utf16_len(text), 5000)
        pieces = c.split_text(text)
        self.assertEqual(len(pieces), 2)
        for p in pieces:
            self.assertLessEqual(c.utf16_len(p), c.CHUNK_BUDGET)

    def test_18_corte_seco_nao_parte_emoji_e_nao_perde_nada(self):
        # 'a' + emojis: o orcamento de 4000 cai em offset impar, ou seja,
        # exatamente no meio de um par surrogate se o corte fosse por code unit.
        text = "a" + "\U0001F600" * 3000
        pieces = c._split_plain(text, 4000)
        for p in pieces:
            self.assertFalse(has_lone_surrogate(p), "surrogate solto em um pedaco")
            self.assertLessEqual(c.utf16_len(p), 4000)
        self.assertEqual(c.utf16_len(pieces[0]), 3999)  # recuou 1 unit em vez de partir
        self.assertEqual("".join(pieces), text)         # nada foi descartado

    def test_join_dos_pedacos_reconstroi_o_texto(self):
        text = "linha\n\n" * 2000
        self.assertEqual("".join(c._split_plain(text, 4000)), text)

    def test_orcamento_menor_que_um_codepoint_e_rejeitado(self):
        # Com budget 1 e um emoji na frente, `truncate_utf16` devolve "" e o
        # laco de _split_plain nunca avancaria: a precondicao e o que garante
        # que ele termina, em vez de um remendo depois do fato.
        with self.assertRaises(ValueError):
            c._split_plain("\U0001F600" * 3, 1)
        self.assertEqual(len(c._split_plain("\U0001F600" * 3, 2)), 3)

    def test_prefixo_entra_no_orcamento(self):
        # com 12 pedacos o prefixo passa a ter 8 code units ("[12/12]\n" tem 8);
        # o corpo tem que encolher para compensar
        pieces = c.split_text("z" * 44000)
        for p in pieces:
            self.assertLessEqual(c.utf16_len(p), c.CHUNK_BUDGET)

    def test_prefixo_nao_come_nem_duplica_o_conteudo(self):
        # largura respeitada nao basta: se o prefixo fosse aplicado errado (comendo
        # o comeco do pedaco, por exemplo) o teste de largura acima passaria igual.
        text = "z" * 44000
        pieces = c.split_text(text)
        n = len(pieces)
        self.assertGreater(n, 1)
        corpo = []
        for i, p in enumerate(pieces, 1):
            prefixo, _, resto = p.partition("\n")
            self.assertEqual(prefixo, f"[{i}/{n}]")
            corpo.append(resto)
        self.assertEqual("".join(corpo), text)   # nada perdido, nada duplicado
        self.assertTrue(pieces[-1].startswith(f"[{n}/{n}]\n"))


FAKE_TOKEN = "123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"


class TestMascaramento(unittest.TestCase):
    def setUp(self):
        self.addCleanup(setattr, c, "_ACTIVE_TOKEN", None)
        c._ACTIVE_TOKEN = FAKE_TOKEN

    def test_5_token_conhecido_sai_filtrado(self):
        texto = f"POST https://api.telegram.org/bot{FAKE_TOKEN}/sendMessage falhou"
        saida = c.mask(texto, FAKE_TOKEN)
        self.assertNotIn(FAKE_TOKEN, saida)
        self.assertIn("<TOKEN>", saida)

    def test_5b_token_desconhecido_com_formato_de_token_tambem_sai(self):
        outro = "987654321:BBZzqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
        saida = c.mask(f"vazou {outro} aqui", token=None)
        self.assertNotIn(outro, saida)
        self.assertIn("<TOKEN>", saida)  # sem isso, um mask que devolve "" passa

    def test_5c_token_fora_do_formato_depende_do_cinto_do_token_exato(self):
        # O unico teste que isola o cinto 1: "abc:short" nao casa com
        # _TOKEN_SHAPE, entao so a substituicao do token exato pode mascarar.
        # Todos os outros testes usam token que o regex tambem pega, ou seja
        # passariam com o cinto 1 desligado.
        self.assertEqual(
            c.mask("url /botabc:short/getMe", "abc:short"), "url /bot<TOKEN>/getMe"
        )

    def test_6_excepthook_nao_vaza_token_em_traceback(self):
        buf = io.StringIO()
        try:
            raise RuntimeError(
                f"HTTP 401 em https://api.telegram.org/bot{FAKE_TOKEN}/getMe"
            )
        except RuntimeError:
            tipo, exc, tb = sys.exc_info()
            with contextlib.redirect_stderr(buf):
                c._excepthook(tipo, exc, tb)
        saida = buf.getvalue()
        self.assertNotIn(FAKE_TOKEN, saida)
        self.assertIn("<TOKEN>", saida)
        self.assertIn("RuntimeError", saida)  # o erro continua diagnosticavel

    def test_emit_mascara_usando_a_global(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            c.emit(f"ok: {FAKE_TOKEN}")
        self.assertNotIn(FAKE_TOKEN, buf.getvalue())

    def test_preview_mostra_so_o_id_do_bot_e_duas_letras(self):
        self.assertEqual(c.token_preview(FAKE_TOKEN), "123456789:AA…")

    def test_preview_recusa_token_sem_dois_pontos(self):
        # Sem os dois pontos, `partition` joga tudo em bot_id: a funcao cujo
        # unico trabalho e ser um preview seguro imprimiria o token inteiro. E o
        # regex nao cobre esse caso, porque a string nao tem formato de token.
        malformado = "AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
        saida = c.token_preview(malformado)
        self.assertNotIn(malformado, saida)
        self.assertEqual(saida, "<malformado>")
        self.assertEqual(c.token_preview("123456789:"), "<malformado>")
        self.assertEqual(c.token_preview(""), "<malformado>")


class EnvFixture(unittest.TestCase):
    """Cria um .env temporario, com modo controlado."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.env_path = self.dir / ".env"
        self.addCleanup(setattr, c, "_ACTIVE_TOKEN", None)

    def write_env(self, body, mode=0o600):
        self.env_path.write_text(body, encoding="utf-8")
        self.env_path.chmod(mode)
        return self.env_path


class TestConfig(EnvFixture):
    def test_parse_env_ignora_comentario_export_e_aspas(self):
        d = c.parse_env_file(
            '# comentario\n'
            'export TELEGRAM_BOT_TOKEN="abc:123"\n'
            "\n"
            "TELEGRAM_ALLOWED_CHATS=42\n"
            "linha sem igual\n"
        )
        self.assertEqual(d["TELEGRAM_BOT_TOKEN"], "abc:123")
        self.assertEqual(d["TELEGRAM_ALLOWED_CHATS"], "42")

    def test_11_env_com_modo_644_e_exit_1_com_instrucao_de_chmod(self):
        self.write_env(f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\n", mode=0o644)
        with self.assertRaises(c.ConfigError) as ctx:
            c.read_env(self.env_path)
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn("chmod 600", str(ctx.exception))

    def test_env_com_modo_600_passa(self):
        self.write_env("TELEGRAM_ALLOWED_CHATS=42\n", mode=0o600)
        filevars, mode = c.read_env(self.env_path)
        self.assertEqual(filevars["TELEGRAM_ALLOWED_CHATS"], "42")
        self.assertEqual(mode, 0o600)

    def test_14_token_do_ambiente_mais_allowlist_do_arquivo_funciona(self):
        self.write_env("TELEGRAM_ALLOWED_CHATS=12345678\n")
        cfg = c.load_config(
            env={"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}, env_path=self.env_path
        )
        self.assertEqual(cfg.token, FAKE_TOKEN)
        self.assertEqual(cfg.chat_id, "12345678")
        self.assertEqual(cfg.token_source, "ambiente")

    def test_14b_allowlist_no_ambiente_e_ignorada(self):
        # o conserto do furo da v3: essa variavel de ambiente nao vale nada
        self.write_env(f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\n")
        with self.assertRaises(c.ConfigError) as ctx:
            c.load_config(
                env={"TELEGRAM_ALLOWED_CHATS": "999"}, env_path=self.env_path
            )
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn("ambiente", str(ctx.exception).lower())

    def test_14c_allowlist_do_arquivo_vence_a_do_ambiente(self):
        self.write_env(
            f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\nTELEGRAM_ALLOWED_CHATS=111\n"
        )
        cfg = c.load_config(
            env={"TELEGRAM_ALLOWED_CHATS": "999"}, env_path=self.env_path
        )
        self.assertEqual(cfg.chat_id, "111")

    def test_14d_token_do_ambiente_vence_o_do_arquivo(self):
        # O outro lado da assimetria. Sem os dois tokens em disputa, nenhum teste
        # distingue "ambiente primeiro" de "arquivo primeiro": em test_14 o
        # arquivo nao tem token, entao a ordem invertida daria o mesmo resultado.
        outro = "987654321:BBZzqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
        self.write_env(f"TELEGRAM_BOT_TOKEN={outro}\nTELEGRAM_ALLOWED_CHATS=42\n")
        cfg = c.load_config(
            env={"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}, env_path=self.env_path
        )
        self.assertEqual(cfg.token, FAKE_TOKEN)
        self.assertEqual(cfg.token_source, "ambiente")

    def test_8c_allowlist_com_duas_entradas_e_exit_1(self):
        self.write_env(
            f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\nTELEGRAM_ALLOWED_CHATS=111,222\n"
        )
        with self.assertRaises(c.ConfigError) as ctx:
            c.load_config(env={}, env_path=self.env_path)
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn("111", str(ctx.exception))

    def test_grupo_com_id_negativo_e_valido(self):
        self.assertEqual(c.parse_allowlist("-1001234567890"), ["-1001234567890"])

    def test_17_allowlist_malformada_explode_ecoando_a_entrada(self):
        # ١٢٣ sao digitos arabico-indianos: `\d` do Python casa com
        # eles (e int() os converte), entao com um regex Unicode-aware essa
        # entrada passaria o portao e so morreria na API, com exit 2 e sem eco.
        arabicos = "١٢٣"
        for raw, ofensora in [
            ("111 222", "111 222"),
            ("abc", "abc"),
            ("12a", "12a"),
            (arabicos, arabicos),
        ]:
            with self.subTest(raw=raw):
                with self.assertRaises(c.ConfigError) as ctx:
                    c.parse_allowlist(raw)
                self.assertEqual(ctx.exception.code, 1)
                self.assertIn(ofensora, str(ctx.exception))

    def test_17b_allowlist_vazia_e_erro_nao_lista_vazia(self):
        with self.assertRaises(c.ConfigError):
            c.parse_allowlist("")

    def test_token_ausente_e_exit_1(self):
        self.write_env("TELEGRAM_ALLOWED_CHATS=42\n")
        with self.assertRaises(c.ConfigError) as ctx:
            c.load_config(env={}, env_path=self.env_path)
        self.assertIn("TELEGRAM_BOT_TOKEN", str(ctx.exception))

    def test_load_config_preenche_a_global_do_mascaramento(self):
        self.write_env(
            f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\nTELEGRAM_ALLOWED_CHATS=42\n"
        )
        cfg = c.load_config(env={}, env_path=self.env_path)
        self.assertEqual(c._ACTIVE_TOKEN, FAKE_TOKEN)
        # o outro rotulo de token_source: sem isso, um mutante que chamasse o
        # ramo do arquivo de "ambiente" sobreviveria (e o --doctor mostra isso)
        self.assertEqual(cfg.token_source, ".env")


class FakeResponse:
    def __init__(self, payload):
        self._body = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class RawResponse:
    """Resposta com corpo cru: bytes que nao sao JSON, ou erro na leitura.

    `FakeResponse` serializa o payload em JSON, entao nao serve para provar o que
    acontece quando o corpo *nao* e JSON. Se o corpo for uma Exception, ela sobe
    de dentro do `read()` -- que e onde o timeout de leitura acontece de verdade,
    depois de os cabecalhos ja terem chegado.
    """

    def __init__(self, body):
        self._body = body

    def read(self):
        if isinstance(self._body, Exception):
            raise self._body
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class FakeNetwork:
    """Substitui c._urlopen: registra as requisicoes e devolve payloads na ordem.

    Um payload que seja Exception e levantado em vez de devolvido; um que ja seja
    uma resposta (tem `read`) passa direto, sem virar JSON.
    """

    def __init__(self, *payloads):
        self.payloads = list(payloads) or [{"ok": True, "result": {"message_id": 1}}]
        self.requests = []

    def __call__(self, req):
        self.requests.append(req)
        idx = min(len(self.requests) - 1, len(self.payloads) - 1)
        payload = self.payloads[idx]
        if isinstance(payload, Exception):
            raise payload
        if hasattr(payload, "read"):
            return payload
        return FakeResponse(payload)


class ExplodingNetwork:
    """Qualquer chamada e falha de teste: usada para provar 'nada foi enviado'."""

    def __call__(self, req):
        raise AssertionError("chamou a rede quando nao devia")


class NetworkFixture(unittest.TestCase):
    def install(self, network):
        self.addCleanup(setattr, c, "_urlopen", c._urlopen)
        c._urlopen = network
        return network


class TestTransporte(NetworkFixture):
    def test_api_post_manda_urlencoded_para_o_metodo_certo(self):
        net = self.install(FakeNetwork({"ok": True, "result": {"message_id": 7}}))
        result = c.api_post(FAKE_TOKEN, "sendMessage", {"chat_id": "42", "text": "oi"})
        self.assertEqual(result["message_id"], 7)
        req = net.requests[0]
        self.assertEqual(req.full_url, f"{c.API_BASE}/bot{FAKE_TOKEN}/sendMessage")
        self.assertIn("chat_id=42", req.data.decode())
        self.assertEqual(
            req.headers["Content-type"], "application/x-www-form-urlencoded"
        )

    def test_api_upload_monta_multipart_com_nome_e_bytes_do_arquivo(self):
        net = self.install(FakeNetwork())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "relatorio.pdf"
            path.write_bytes(b"%PDF-1.4 conteudo")
            c.api_upload(
                FAKE_TOKEN, "sendDocument", {"chat_id": "42"}, "document", path
            )
        req = net.requests[0]
        self.assertTrue(req.headers["Content-type"].startswith("multipart/form-data; boundary="))
        body = req.data
        self.assertIn(b'filename="relatorio.pdf"', body)
        self.assertIn(b"%PDF-1.4 conteudo", body)
        self.assertIn(b'name="chat_id"', body)
        # A fronteira anunciada no cabecalho tem que ser a mesma usada no corpo, e
        # o corpo tem que fechar com "--<fronteira>--". Sem estas duas linhas, duas
        # mutacoes de um caractere sobrevivem a suite inteira e tornam *todo* upload
        # ilegivel para o Telegram -- no unico caminho que, por desenho, nao tem
        # cobertura de rede.
        b = req.headers["Content-type"].split("boundary=")[1]
        self.assertIn(f"--{b}\r\n".encode(), body)
        self.assertTrue(body.endswith(f"--{b}--\r\n".encode()))

    def test_nome_de_arquivo_com_aspas_e_quebra_nao_corrompe_o_multipart(self):
        # O nome do arquivo e entrada do usuario e vai cru para dentro de um
        # cabecalho: uma aspa fecha o parametro filename= antes da hora e uma
        # quebra de linha injeta cabecalho (ou uma fronteira falsa) no corpo.
        # Sem este teste a sanitizacao pode ser apagada e a suite passa igual.
        net = self.install(FakeNetwork())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'a"b\nc.txt'
            path.write_bytes(b"dados")
            c.api_upload(
                FAKE_TOKEN, "sendDocument", {"chat_id": "42"}, "document", path
            )
        body = net.requests[0].data
        self.assertIn(b'filename="a_b_c.txt"', body)
        self.assertNotIn(b'a"b', body)
        self.assertNotIn(b"b\nc.txt", body)

    def test_resposta_com_ok_false_e_erro_de_api(self):
        self.install(FakeNetwork({"ok": False, "description": "chat not found"}))
        with self.assertRaises(c.ApiError) as ctx:
            c.api_post(FAKE_TOKEN, "sendMessage", {"chat_id": "42", "text": "oi"})
        self.assertEqual(ctx.exception.code, 2)
        self.assertIn("chat not found", str(ctx.exception))

    def test_16_retry_after_de_429_aparece_na_mensagem(self):
        corpo = json.dumps(
            {
                "ok": False,
                "error_code": 429,
                "description": "Too Many Requests: retry later",
                "parameters": {"retry_after": 17},
            }
        ).encode("utf-8")
        erro = urllib.error.HTTPError(
            "https://api.telegram.org/botX/sendMessage",
            429,
            "Too Many Requests",
            {},
            io.BytesIO(corpo),
        )
        self.install(FakeNetwork(erro))
        with self.assertRaises(c.ApiError) as ctx:
            c.api_post(FAKE_TOKEN, "sendMessage", {"chat_id": "42", "text": "oi"})
        self.assertEqual(ctx.exception.code, 2)
        self.assertIn("17", str(ctx.exception))
        self.assertIn("retry_after", str(ctx.exception))

    def test_falha_de_rede_vira_erro_de_api_sem_traceback(self):
        self.install(FakeNetwork(urllib.error.URLError("dns morreu")))
        with self.assertRaises(c.ApiError) as ctx:
            c.api_post(FAKE_TOKEN, "getMe", {})
        self.assertIn("dns morreu", str(ctx.exception))

    def test_200_com_corpo_que_nao_e_json_vira_erro_de_api(self):
        # Captive portal ou proxy mal configurado devolve HTTP 200 com HTML: a
        # trilha de *sucesso* tambem tem json.loads, e sem guarda ela solta
        # JSONDecodeError cru -- exatamente o traceback que esta camada existe
        # para nao deixar subir. Corpo em bytes invalidos idem, por decode().
        self.install(
            FakeNetwork(
                RawResponse(b"<html>captive portal</html>"),
                RawResponse(b"\xff\xfe\x00nao-utf8"),
            )
        )
        with self.assertRaises(c.ApiError) as ctx:
            c.api_post(FAKE_TOKEN, "getMe", {})
        self.assertEqual(ctx.exception.code, 2)
        self.assertIn("captive portal", str(ctx.exception))
        with self.assertRaises(c.ApiError) as ctx:
            c.api_post(FAKE_TOKEN, "getMe", {})
        self.assertEqual(ctx.exception.code, 2)

    def test_200_com_json_que_nao_e_objeto_vira_erro_de_api(self):
        # `null`, `[1,2]` e `"texto"` sao JSON valido: passam pelo json.loads e
        # estouravam AttributeError no payload.get("ok") logo abaixo. Mesmo furo
        # do corpo nao-JSON, um degrau adiante.
        self.install(
            FakeNetwork(
                RawResponse(b"null"), RawResponse(b"[1,2]"), RawResponse(b'"texto"')
            )
        )
        for esperado in ("null", "[1,2]", '"texto"'):
            with self.subTest(corpo=esperado):
                with self.assertRaises(c.ApiError) as ctx:
                    c.api_post(FAKE_TOKEN, "getMe", {})
                self.assertEqual(ctx.exception.code, 2)
                self.assertIn(esperado, str(ctx.exception))

    def test_erro_na_leitura_do_corpo_vira_erro_de_api(self):
        # Timeout de leitura acontece depois de os cabecalhos chegarem e sobe como
        # TimeoutError puro, *sem* embrulho de URLError: escapa das duas clausulas
        # de urllib.error e so a de OSError o pega.
        self.install(FakeNetwork(RawResponse(TimeoutError("timed out"))))
        with self.assertRaises(c.ApiError) as ctx:
            c.api_post(FAKE_TOKEN, "getMe", {})
        self.assertEqual(ctx.exception.code, 2)
        self.assertIn("timed out", str(ctx.exception))

    def test_status_http_aparece_quando_o_corpo_de_erro_e_json_sem_description(self):
        # 502 de um proxy no meio do caminho, com corpo JSON que nao e do
        # Telegram: sem o status na mensagem sobraria so "resposta sem
        # description" e o 502 desapareceria.
        corpo = json.dumps({"error": "gateway"}).encode("utf-8")
        erro = urllib.error.HTTPError(
            "https://api.telegram.org/botX/sendMessage",
            502,
            "Bad Gateway",
            {},
            io.BytesIO(corpo),
        )
        self.install(FakeNetwork(erro))
        with self.assertRaises(c.ApiError) as ctx:
            c.api_post(FAKE_TOKEN, "sendMessage", {"chat_id": "1", "text": "x"})
        self.assertEqual(ctx.exception.code, 2)
        self.assertIn("502", str(ctx.exception))

    def test_erro_http_sem_json_no_corpo_nao_estoura(self):
        erro = urllib.error.HTTPError(
            "https://api.telegram.org/botX/sendMessage",
            502,
            "Bad Gateway",
            {},
            io.BytesIO(b"<html>nginx</html>"),
        )
        self.install(FakeNetwork(erro))
        with self.assertRaises(c.ApiError) as ctx:
            c.api_post(FAKE_TOKEN, "sendMessage", {"chat_id": "1", "text": "x"})
        msg = str(ctx.exception)
        self.assertIn("502", msg)
        self.assertIn("<html>nginx</html>", msg)  # quem respondeu no lugar do Telegram
        # O status entra como aposto: "resposta não é JSON (HTTP 502) em sendMessage".
        # Quem le isso esta confuso, e "em HTTP 502 em sendMessage" nao e frase.
        self.assertIn("(HTTP 502)", msg)
        self.assertNotIn("em HTTP", msg)

    def test_timeout_lendo_o_corpo_do_erro_vira_erro_de_api_e_fecha_o_socket(self):
        # err.fp e o socket vivo: ler o corpo de um erro HTTP pode dar o mesmo
        # timeout da leitura normal. Sem a guarda em volta de err.read(), o
        # TimeoutError escapa do _call cru -- e o docstring de _call afirma que
        # nenhuma excecao escapa dali. Este teste tranca a guarda e o close().
        class CorpoQueEstoura(io.BytesIO):
            def read(self, *args):
                raise TimeoutError("timed out")

        corpo = CorpoQueEstoura()
        erro = urllib.error.HTTPError(
            "https://api.telegram.org/botX/sendMessage",
            502,
            "Bad Gateway",
            {},
            corpo,
        )
        self.install(FakeNetwork(erro))
        with self.assertRaises(c.ApiError) as ctx:
            c.api_post(FAKE_TOKEN, "sendMessage", {"chat_id": "1", "text": "x"})
        msg = str(ctx.exception)
        self.assertEqual(ctx.exception.code, 2)
        self.assertIn("falha ao ler o corpo do erro (HTTP 502) em sendMessage", msg)
        self.assertIn("timed out", msg)
        # O finally tem de fechar o socket tambem no caminho de falha; sem isso o
        # 3.14 solta ResourceWarning no GC e o socket vaza.
        self.assertTrue(corpo.closed)


class TestDenylist(NetworkFixture):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.install(ExplodingNetwork())  # nada aqui pode tocar a rede

    def arquivo(self, nome, conteudo=b"x"):
        path = self.dir / nome
        path.write_bytes(conteudo)
        return path

    def test_7_chave_ssh_e_recusada_com_exit_3(self):
        with self.assertRaises(c.InputError) as ctx:
            c.validate_files(["~/.ssh/id_rsa"])
        self.assertEqual(ctx.exception.code, 3)
        self.assertIn("denylist", str(ctx.exception))

    def test_7b_denylist_nao_e_burlada_por_symlink(self):
        alvo = self.arquivo("id_rsa", b"-----BEGIN OPENSSH PRIVATE KEY-----")
        link = self.dir / "relatorio-inocente.txt"
        link.symlink_to(alvo)
        with self.assertRaises(c.InputError) as ctx:
            c.validate_files([str(link)])
        self.assertEqual(ctx.exception.code, 3)

    def test_7c_denylist_cobre_env_pem_e_credenciais(self):
        for nome in [".env", ".env.local", "chave.pem", "cofre.kdbx", "id_ed25519"]:
            with self.subTest(nome=nome):
                path = self.arquivo(nome)
                with self.assertRaises(c.InputError):
                    c.validate_files([str(path)])

    def test_7d_denylist_nao_e_burlada_por_variacao_de_caixa(self):
        # APFS e case-insensitive por padrao, mas os.path.normcase (que o
        # fnmatch.fnmatch usa) e identidade em POSIX: sem baixar a caixa dos
        # dois lados, ID_RSA alcanca o arquivo real e escapa da regra.
        self.arquivo("id_rsa", b"chave")
        for pedido in [str(self.dir / "ID_RSA"), "~/.SSH/id_rsa"]:
            with self.subTest(pedido=pedido):
                with self.assertRaises(c.InputError) as ctx:
                    c.validate_files([pedido])
                self.assertIn("denylist", str(ctx.exception))

    def test_arquivo_comum_passa_e_volta_resolvido(self):
        path = self.arquivo("resumo.md", b"# oi")
        self.assertEqual(c.validate_files([str(path)]), [path.resolve()])

    def test_9_terceiro_arquivo_inexistente_recusa_tudo_sem_rede(self):
        a = self.arquivo("a.md")
        b = self.arquivo("b.md")
        with self.assertRaises(c.InputError) as ctx:
            c.validate_files([str(a), str(b), str(self.dir / "nao-existe.md")])
        self.assertEqual(ctx.exception.code, 3)
        self.assertIn("nao-existe.md", str(ctx.exception))

    def test_12_arquivo_de_51mb_e_recusado_antes_de_qualquer_rede(self):
        grande = self.dir / "grande.bin"
        with open(grande, "wb") as fh:
            fh.truncate(51 * 1024 * 1024)  # sparse: instantaneo, nao ocupa disco
        with self.assertRaises(c.InputError) as ctx:
            c.validate_files([str(grande)])
        self.assertEqual(ctx.exception.code, 3)
        self.assertIn("50", str(ctx.exception))

    def test_diretorio_nao_e_arquivo(self):
        with self.assertRaises(c.InputError):
            c.validate_files([str(self.dir)])

    def test_human_size(self):
        self.assertEqual(c.human_size(2202010), "2.1 MB")
        self.assertEqual(c.human_size(12288), "12.0 KB")
        self.assertEqual(c.human_size(17), "17 B")


class SendFixture(EnvFixture, NetworkFixture):
    """Config valida em .env temporario + rede falsa. Destino sempre 12345678."""

    CHAT = "12345678"

    def setUp(self):
        EnvFixture.setUp(self)
        self.write_env(
            f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\nTELEGRAM_ALLOWED_CHATS={self.CHAT}\n"
        )
        self.net = self.install(FakeNetwork())

    def send(self, text=None, files=(), caption=None, env=None):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = c.cmd_send(
                text,
                list(files),
                caption,
                env={} if env is None else env,
                env_path=self.env_path,
            )
        return code, buf.getvalue().splitlines()

    def campos(self, req):
        """Devolve o corpo da requisicao como texto, urlencoded ou multipart."""
        return req.data.decode("utf-8", "replace")


class TestEnvio(SendFixture):
    def test_15_saida_de_texto_unico_bate_com_a_spec(self):
        code, linhas = self.send(text="oi")
        self.assertEqual(code, 0)
        self.assertEqual(linhas, ["ok: texto"])

    def test_15b_saida_de_texto_fatiado_bate_com_a_spec(self):
        code, linhas = self.send(text="z" * 5000)
        self.assertEqual(code, 0)
        self.assertEqual(linhas, ["ok: texto (1/2)", "ok: texto (2/2)"])
        self.assertEqual(len(self.net.requests), 2)

    def test_15c_saida_de_documento_bate_com_a_spec(self):
        path = self.dir / "relatorio.pdf"
        with open(path, "wb") as fh:
            fh.truncate(2202010)  # 2.1 MB
        code, linhas = self.send(files=[str(path)])
        self.assertEqual(code, 0)
        self.assertEqual(linhas, ["ok: documento relatorio.pdf (2.1 MB)"])

    def test_texto_vai_antes_dos_arquivos_e_na_ordem_dada(self):
        a = self.dir / "a.md"
        a.write_text("a")
        b = self.dir / "b.md"
        b.write_text("b")
        code, linhas = self.send(text="resumo", files=[str(a), str(b)])
        self.assertEqual(
            linhas,
            ["ok: texto", "ok: documento a.md (1 B)", "ok: documento b.md (1 B)"],
        )

    def test_8a_destino_e_sempre_o_da_allowlist_mesmo_com_ambiente_hostil(self):
        self.send(text="oi", env={"TELEGRAM_ALLOWED_CHATS": "999666"})
        corpo = self.campos(self.net.requests[0])
        self.assertIn(f"chat_id={self.CHAT}", corpo)
        self.assertNotIn("999666", corpo)

    def test_legenda_vai_so_no_primeiro_arquivo(self):
        a = self.dir / "a.md"
        a.write_text("a")
        b = self.dir / "b.md"
        b.write_text("b")
        self.send(files=[str(a), str(b)], caption="o primeiro")
        self.assertIn("o primeiro", self.campos(self.net.requests[0]))
        self.assertNotIn("o primeiro", self.campos(self.net.requests[1]))

    def test_10b_legenda_acima_de_1024_e_truncada_com_aviso(self):
        path = self.dir / "a.md"
        path.write_text("a")
        _, linhas = self.send(files=[str(path)], caption="c" * 2000)
        self.assertTrue(any("truncada" in l for l in linhas), linhas)
        corpo = self.campos(self.net.requests[0])
        self.assertNotIn("c" * 1025, corpo)
        self.assertIn("c" * 1024, corpo)

    def test_9_lote_com_arquivo_faltando_nao_manda_nada(self):
        a = self.dir / "a.md"
        a.write_text("a")
        b = self.dir / "b.md"
        b.write_text("b")
        with self.assertRaises(c.InputError):
            self.send(files=[str(a), str(b), str(self.dir / "sumiu.md")])
        self.assertEqual(self.net.requests, [])  # zero envios

    def test_texto_vazio_e_erro_de_entrada(self):
        with self.assertRaises(c.InputError):
            self.send(text="   ")

    def test_texto_do_stdin(self):
        self.addCleanup(setattr, sys, "stdin", sys.stdin)
        sys.stdin = io.StringIO("veio do pipe")
        _, linhas = self.send(text="-")
        self.assertEqual(linhas, ["ok: texto"])
        self.assertIn("veio+do+pipe", self.campos(self.net.requests[0]))

    def test_surrogate_solto_no_texto_e_erro_de_entrada_nao_traceback(self):
        # argv com bytes invalidos chega como surrogateescape: utf16_len
        # levantaria UnicodeEncodeError la dentro do split_text. A fronteira de
        # entrada e aqui, entao o erro certo e InputError (exit 3), nao um
        # traceback mascarado com exit 1.
        with self.assertRaises(c.InputError) as ctx:
            self.send(text="ok ate aqui \udcff")
        self.assertEqual(ctx.exception.code, 3)
        self.assertEqual(self.net.requests, [])

    def test_surrogate_solto_na_legenda_tambem_e_erro_de_entrada(self):
        path = self.dir / "a.md"
        path.write_text("a")
        with self.assertRaises(c.InputError) as ctx:
            self.send(files=[str(path)], caption="legenda \udcff")
        self.assertEqual(ctx.exception.code, 3)
        self.assertEqual(self.net.requests, [])


def update_de(chat_id, first_name="Elder", username="eldermoraes", tipo="private"):
    return {
        "update_id": 1,
        "message": {
            "message_id": 1,
            "chat": {
                "id": chat_id,
                "type": tipo,
                "first_name": first_name,
                "username": username,
            },
            "text": "oi",
        },
    }


class TestSetup(EnvFixture, NetworkFixture):
    def setUp(self):
        EnvFixture.setUp(self)
        self.write_env(f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\n")

    def rodar_setup(self, chat_id=None, updates=()):
        self.net = self.install(FakeNetwork({"ok": True, "result": list(updates)}))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = c.cmd_setup(chat_id, env={}, env_path=self.env_path)
        return code, buf.getvalue().splitlines()

    def test_sem_updates_instrui_e_cita_as_duas_causas(self):
        with self.assertRaises(c.ConfigError) as ctx:
            self.rodar_setup()
        msg = str(ctx.exception)
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn("DM", msg)
        self.assertIn("409", msg)       # webhook ativo
        self.assertIn("poller", msg)    # offset compartilhado

    def test_19_lista_candidatos_com_id_nome_e_username_e_pede_confirmacao(self):
        code, linhas = self.rodar_setup(updates=[update_de(12345678)])
        self.assertEqual(code, 1)  # nada gravado ainda
        juntas = "\n".join(linhas)
        self.assertIn("12345678", juntas)
        self.assertIn("Elder", juntas)
        self.assertIn("@eldermoraes", juntas)
        self.assertIn("--chat-id", juntas)
        self.assertNotIn("TELEGRAM_ALLOWED_CHATS", self.env_path.read_text())

    def test_chat_id_confirmado_grava_a_allowlist_e_preserva_o_token(self):
        code, linhas = self.rodar_setup(chat_id="12345678", updates=[update_de(12345678)])
        self.assertEqual(code, 0)
        corpo = self.env_path.read_text()
        self.assertIn("TELEGRAM_ALLOWED_CHATS=12345678", corpo)
        self.assertIn(f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}", corpo)
        self.assertEqual(self.env_path.stat().st_mode & 0o777, 0o600)
        self.assertNotIn(FAKE_TOKEN, "\n".join(linhas))  # so o preview mascarado
        self.assertIn("123456789:AA…", "\n".join(linhas))

    def test_18b_a_chat_id_fora_dos_candidatos_e_recusado(self):
        with self.assertRaises(c.ConfigError) as ctx:
            self.rodar_setup(chat_id="999666", updates=[update_de(12345678)])
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn("999666", str(ctx.exception))

    def test_18b_b_nao_sobrescreve_allowlist_existente_e_nem_toca_a_rede(self):
        self.write_env(
            f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\nTELEGRAM_ALLOWED_CHATS=12345678\n"
        )
        self.install(ExplodingNetwork())  # a recusa vem antes do getUpdates
        with self.assertRaises(c.ConfigError) as ctx:
            c.cmd_setup("999666", env={}, env_path=self.env_path)
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn("--doctor", str(ctx.exception))
        # o valor gravado continua intacto
        self.assertIn("TELEGRAM_ALLOWED_CHATS=12345678", self.env_path.read_text())

    def test_18b_c_recusa_vale_tambem_sem_chat_id(self):
        self.write_env(
            f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\nTELEGRAM_ALLOWED_CHATS=12345678\n"
        )
        self.install(ExplodingNetwork())
        with self.assertRaises(c.ConfigError):
            c.cmd_setup(None, env={}, env_path=self.env_path)

    def test_write_env_var_cria_diretorio_700_e_arquivo_600(self):
        novo = self.dir / "sub" / ".env"
        c.write_env_var("TELEGRAM_ALLOWED_CHATS", "42", novo)
        self.assertEqual(novo.stat().st_mode & 0o777, 0o600)
        self.assertEqual(novo.parent.stat().st_mode & 0o777, 0o700)
        self.assertFalse((novo.parent / ".env.tmp").exists())  # temporario removido

    def test_candidatos_deduplicam_o_mesmo_chat(self):
        cands = c._candidates([update_de(5), update_de(5), update_de(7)])
        self.assertEqual([x["id"] for x in cands], ["5", "7"])

    def test_candidato_de_grupo_usa_o_title(self):
        upd = {"message": {"chat": {"id": -100, "type": "group", "title": "Familia"}}}
        self.assertEqual(c._candidates([upd])[0]["name"], "Familia")


class TestDoctor(EnvFixture):
    def doctor(self, env=None):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = c.cmd_doctor(env={} if env is None else env, env_path=self.env_path)
        return code, buf.getvalue()

    def test_20_config_completa_reporta_tudo_com_token_mascarado(self):
        self.write_env(
            f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\nTELEGRAM_ALLOWED_CHATS=12345678\n"
        )
        code, saida = self.doctor()
        self.assertEqual(code, 0)
        self.assertIn("modo 600", saida)
        self.assertIn("123456789:AA…", saida)
        self.assertNotIn(FAKE_TOKEN, saida)
        self.assertIn("12345678", saida)

    def test_env_ausente_reporta_e_sai_1(self):
        code, saida = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("não existe", saida)

    def test_env_com_modo_larga_reporta_o_chmod(self):
        self.write_env(f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\n", mode=0o644)
        code, saida = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("chmod 600", saida)

    def test_allowlist_ambigua_e_reportada_como_problema(self):
        self.write_env(
            f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\nTELEGRAM_ALLOWED_CHATS=111,222\n"
        )
        code, saida = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("ambígua", saida)

    def test_allowlist_malformada_e_reportada_sem_derrubar_o_doctor(self):
        self.write_env(
            f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\nTELEGRAM_ALLOWED_CHATS=111 222\n"
        )
        code, saida = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("111 222", saida)

    def test_allowlist_no_ambiente_ganha_aviso_de_que_e_ignorada(self):
        self.write_env(
            f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\nTELEGRAM_ALLOWED_CHATS=42\n"
        )
        code, saida = self.doctor(env={"TELEGRAM_ALLOWED_CHATS": "999"})
        self.assertEqual(code, 0)
        self.assertIn("ignorada", saida)

    def test_token_so_no_ambiente_reporta_a_fonte(self):
        self.write_env("TELEGRAM_ALLOWED_CHATS=42\n")
        code, saida = self.doctor(env={"TELEGRAM_BOT_TOKEN": FAKE_TOKEN})
        self.assertEqual(code, 0)
        self.assertIn("ambiente", saida)


class TestCli(EnvFixture, NetworkFixture):
    def setUp(self):
        EnvFixture.setUp(self)
        # main() e run() nao recebem env_path: eles leem o global, que aqui aponta
        # para o .env temporario. Sem isso os testes tocariam o ~/.claude de verdade.
        self.addCleanup(setattr, c, "ENV_PATH", c.ENV_PATH)
        c.ENV_PATH = self.env_path
        # cmd_send via run() le os.environ de verdade: numa maquina com o token
        # exportado (o estado natural de quem usa a ferramenta), o teste de config
        # ausente falharia falso. Isola as duas variaveis do processo.
        for var in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_ALLOWED_CHATS"):
            valor = os.environ.pop(var, None)
            if valor is not None:
                self.addCleanup(os.environ.__setitem__, var, valor)
        self.net = self.install(FakeNetwork())

    def rodar(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = c.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_13_modos_sao_mutuamente_exclusivos(self):
        for argv in (
            ["--setup", "--text", "oi"],
            ["--doctor", "--file", "/tmp/x"],
            ["--setup", "--doctor"],
        ):
            with self.subTest(argv=argv):
                code, _, err = self.rodar(argv)
                self.assertEqual(code, 3, err)

    def test_8b_chat_id_fora_do_setup_e_recusado(self):
        code, _, err = self.rodar(["--text", "oi", "--chat-id", "999"])
        self.assertEqual(code, 3)
        self.assertIn("--setup", err)

    def test_10a_caption_sem_file_e_recusado(self):
        code, _, err = self.rodar(["--caption", "legenda"])
        self.assertEqual(code, 3)
        self.assertIn("--text", err)

    def test_sem_argumento_nenhum_e_erro_de_entrada(self):
        code, _, _ = self.rodar([])
        self.assertEqual(code, 3)

    def test_flag_desconhecida_e_exit_3_e_nao_2(self):
        # argparse sairia com 2, que neste contrato significa "erro da API"
        code, _, err = self.rodar(["--telegrama", "oi"])
        self.assertEqual(code, 3)
        self.assertIn("uso inválido", err)

    def test_envio_completo_pelo_cli_devolve_0(self):
        self.write_env(
            f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\nTELEGRAM_ALLOWED_CHATS=12345678\n"
        )
        code, out, _ = self.rodar(["--text", "oi"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "ok: texto")

    def test_erro_de_config_e_exit_1(self):
        code, _, err = self.rodar(["--text", "oi"])  # .env nem existe
        self.assertEqual(code, 1)
        self.assertIn("TELEGRAM_BOT_TOKEN", err)

    def test_erro_da_api_e_exit_2_sem_vazar_o_token(self):
        self.write_env(
            f"TELEGRAM_BOT_TOKEN={FAKE_TOKEN}\nTELEGRAM_ALLOWED_CHATS=12345678\n"
        )
        self.install(
            FakeNetwork({"ok": False, "description": f"Unauthorized: bot{FAKE_TOKEN}"})
        )
        code, _, err = self.rodar(["--text", "oi"])
        self.assertEqual(code, 2)
        self.assertNotIn(FAKE_TOKEN, err)
        self.assertIn("<TOKEN>", err)

    def test_25_script_de_verdade_em_subprocesso_respeita_os_exit_codes(self):
        """Roda o arquivo como o Claude roda: subprocesso, sem rede, HOME falso."""
        with tempfile.TemporaryDirectory() as home:
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--text", "oi"],
                capture_output=True,
                text=True,
                env={
                    "HOME": home,
                    "PATH": os.environ.get("PATH", ""),
                    "TELEGRAM_BOT_TOKEN": FAKE_TOKEN,
                },
            )
        self.assertEqual(proc.returncode, 1)  # token ok, allowlist ausente
        self.assertIn("TELEGRAM_ALLOWED_CHATS", proc.stderr)
        self.assertNotIn(FAKE_TOKEN, proc.stdout + proc.stderr)

    def test_excepthook_e_instalado_pelo_guard_main(self):
        # A promessa "traceback nunca vaza token" depende de uma linha no guard
        # __main__ que import nao executa. Aqui o script roda como script
        # (runpy, run_name __main__) e a fiacao e afirmada de verdade: sem a
        # linha, nenhum outro teste acusa.
        programa = (
            "import runpy, sys\n"
            f"caminho = {str(SCRIPT)!r}\n"
            "try:\n"
            "    runpy.run_path(caminho, run_name='__main__')\n"
            "except SystemExit:\n"
            "    pass\n"
            "assert sys.excepthook.__name__ == '_excepthook', repr(sys.excepthook)\n"
        )
        with tempfile.TemporaryDirectory() as home:
            proc = subprocess.run(
                [sys.executable, "-c", programa],
                capture_output=True,
                text=True,
                env={"HOME": home, "PATH": os.environ.get("PATH", "")},
            )
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_help_nao_e_erro(self):
        with self.assertRaises(SystemExit) as ctx:
            with contextlib.redirect_stdout(io.StringIO()):
                c.main(["--help"])
        self.assertEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
