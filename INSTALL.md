# INSTALL.md

Roteiro de instalação. Quem executa este arquivo é o agente de IA, não a pessoa.
Siga os passos na ordem e vá contando em voz alta o que está fazendo, em português
simples. A pessoa do outro lado provavelmente nunca viu um terminal.

Ao final, ela precisa ter as 9 skills instaladas e a pasta `ai-tools` criada no
lugar que ela escolheu, com o caminho gravado em `~/.config/ai-tools/local.txt`.

---

## Passo 1: baixar o repositório

Baixe o repositório como arquivo compactado. **Não use `git clone`**: a máquina da
pessoa pode não ter o git instalado.

```bash
curl -L -o /tmp/ai-tools.zip https://github.com/eldermoraes/ai-tools/archive/refs/heads/main.zip
mkdir -p /tmp/ai-tools-download
unzip -o -q /tmp/ai-tools.zip -d /tmp/ai-tools-download
```

Os arquivos ficam em `/tmp/ai-tools-download/ai-tools-main/`.

Se o download falhar, mostre o erro real para a pessoa e pare. Não invente um
caminho alternativo.

## Passo 2: instalar as skills

Copie cada pasta de dentro de `skills/` para a pasta de skills do Claude Code,
criando a pasta de destino se ela não existir:

```bash
mkdir -p ~/.claude/skills
cp -R /tmp/ai-tools-download/ai-tools-main/skills/* ~/.claude/skills/
```

**Se você não é o Claude Code** (por exemplo, se você é o Codex do ChatGPT),
instale no diretório de skills equivalente da sua própria ferramenta, em vez de
`~/.claude/skills/`.

## Passo 3: perguntar onde os arquivos dela vão morar

Tudo o que a pessoa escrever sobre o negócio dela vai viver numa pasta chamada
`ai-tools`. Onde essa pasta fica é escolha dela, não sua. Pergunte, com uma
pergunta só:

> Onde você quer guardar os arquivos do seu negócio? Três opções:
>
> 1. **Na sua pasta pessoal** — o padrão. Funciona de qualquer lugar do
>    computador.
> 2. **Na pasta em que estamos agora** — bom para quem quer tudo dentro de um
>    projeto específico.
> 3. **Em outra pasta que você me indicar** — por exemplo, uma pasta que
>    sincroniza com o Google Drive, para ter cópia automática na nuvem.
>
> Se não souber, vá de 1.

Como montar o caminho final, que este roteiro chama de `PASTA` daqui em diante:

- **Opção 1:** `PASTA` é `~/ai-tools`.
- **Opção 2:** `PASTA` é a pasta atual mais `/ai-tools`. Uma trava: se a pasta
  atual for temporária (dentro de `/tmp`) ou a própria pasta baixada no Passo 1,
  explique que ali tudo se perde e volte à pergunta.
- **Opção 3:** monte o caminho junto com ela e termine com `/ai-tools`. No Mac, a
  pasta do Google Drive costuma morar em
  `~/Library/CloudStorage/GoogleDrive-<conta>/My Drive/`; no Windows, em
  `G:\Meu Drive\`. Liste o conteúdo do lugar indicado para confirmar que ele
  existe antes de seguir. E avise, em uma frase: pasta sincronizada significa que
  os arquivos do negócio sobem para a nuvem daquela conta.

Nos comandos dos próximos passos, troque `PASTA` pelo caminho completo escolhido,
escrito por extenso, sem `~`. Por exemplo: `/Users/maria/ai-tools`.

## Passo 4: criar a pasta e gravar o endereço dela

Primeiro as seis pastas:

```bash
mkdir -p PASTA/negocio PASTA/voz PASTA/marca PASTA/conselho PASTA/conteudo PASTA/radar
```

Depois o endereço, num arquivo fixo. É lendo esse arquivo que as skills descobrem
onde a pasta está, seja ela qual for:

```bash
mkdir -p ~/.config/ai-tools
echo "PASTA" > ~/.config/ai-tools/local.txt
```

As seis pastas nascem vazias. Elas se enchem conforme a pessoa usa as skills.

Tudo o que ela escrever sobre o negócio dela mora aqui, e só aqui. A pasta baixada
no Passo 1 é descartável.

## Passo 5: guardar os modelos e os guias

Copie as pastas `modelos/` e `avancado/`, mais o mapa `COMECE-AQUI.md`, para
dentro da pasta da pessoa, como material de consulta:

```bash
mkdir -p PASTA/_kit
cp -R /tmp/ai-tools-download/ai-tools-main/modelos PASTA/_kit/
cp -R /tmp/ai-tools-download/ai-tools-main/avancado PASTA/_kit/
cp /tmp/ai-tools-download/ai-tools-main/COMECE-AQUI.md PASTA/_kit/
```

## Passo 6: conferir e mostrar

Liste o que foi instalado e mostre para ela:

```bash
ls ~/.claude/skills
ls PASTA
cat ~/.config/ai-tools/local.txt
```

Confirme que as 9 skills apareceram:

`meu-negocio`, `minha-voz`, `minha-marca`, `conselho`, `conteudo`, `radar`,
`trafego`, `video`, `telegram`

Que as seis pastas mais a `_kit` apareceram dentro de `PASTA`: `negocio`, `voz`,
`marca`, `conselho`, `conteudo`, `radar`, `_kit`. E que o `local.txt` mostra
exatamente o caminho escolhido no Passo 3.

Se faltar alguma coisa, refaça o passo correspondente e confira de novo. Não siga
em frente com instalação pela metade.

## Passo 7: o aviso que não pode faltar

Diga a ela, com estas palavras:

> Feche e abra o Claude Code de novo: skill nova só carrega em conversa nova.

## Passo 8: o primeiro passo dela

Feche assim:

> Depois de reabrir, diga: **use a skill meu-negocio**.

E avise que o mapa completo do que cada skill faz está no arquivo
`COMECE-AQUI.md`, dentro da pasta `_kit`, dentro da pasta que ela escolheu.

---

## Telas que vão aparecer

Durante a instalação, o Claude Code vai parar e pedir permissão algumas vezes.
Explique isso para a pessoa antes de começar, para ela não achar que é vírus.

**"Posso rodar este comando?"**
Aparece antes de baixar o repositório e antes de criar as pastas. O comando fica
escrito na tela, inteiro. É o programa pedindo licença para mexer no computador
dela. Ela responde **sim**.

**"Posso criar esta pasta?" / "Posso escrever neste arquivo?"**
Aparece quando a instalação cria a pasta `ai-tools` e quando qualquer skill for
salvar algo depois. Ela responde **sim**. Nada é escrito fora dessas pastas.

**"Posso buscar na internet?"**
Não aparece na instalação. Aparece depois, quando ela usar a skill `radar`, que
precisa procurar notícias e preços. Ela responde **sim** quando quiser o
relatório.

**"Limite atingido" ou aviso parecido**
É a cota do plano dela, não é defeito e não quebrou nada. Basta esperar a cota
voltar e continuar de onde parou. Os arquivos já gravados continuam lá.

Três coisas que valem para todas essas telas:

- Ela pode responder **não** em qualquer uma. A instalação para e nada acontece.
- Nenhuma dessas telas pede senha, cartão ou dado bancário. Se aparecer algo assim,
  é para desconfiar.
- Tudo o que é criado fica no computador dela.
