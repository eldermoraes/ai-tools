# INSTALL.md

Roteiro de instalação. Quem executa este arquivo é o agente de IA, não a pessoa.
Siga os passos na ordem e vá contando em voz alta o que está fazendo, em português
simples. A pessoa do outro lado provavelmente nunca viu um terminal.

Ao final, ela precisa ter as 9 skills instaladas e a pasta `~/escritorio-ia/`
criada.

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

## Passo 3: guardar os modelos e os guias

Copie as pastas `modelos/` e `avancado/`, mais o mapa `COMECE-AQUI.md`, para
dentro da pasta da pessoa, como material de consulta:

```bash
mkdir -p ~/escritorio-ia/_kit
cp -R /tmp/ai-tools-download/ai-tools-main/modelos ~/escritorio-ia/_kit/
cp -R /tmp/ai-tools-download/ai-tools-main/avancado ~/escritorio-ia/_kit/
cp /tmp/ai-tools-download/ai-tools-main/COMECE-AQUI.md ~/escritorio-ia/_kit/
```

## Passo 4: criar a pasta do escritório

```bash
mkdir -p ~/escritorio-ia/negocio
mkdir -p ~/escritorio-ia/voz
mkdir -p ~/escritorio-ia/marca
mkdir -p ~/escritorio-ia/conselho
mkdir -p ~/escritorio-ia/conteudo
mkdir -p ~/escritorio-ia/radar
```

As seis pastas nascem vazias. Elas se enchem conforme a pessoa usa as skills.

Tudo o que ela escrever sobre o negócio dela mora aqui, e só aqui. A pasta baixada
no Passo 1 é descartável.

## Passo 5: conferir e mostrar

Liste o que foi instalado e mostre para ela:

```bash
ls ~/.claude/skills
ls ~/escritorio-ia
```

Confirme que as 9 skills apareceram:

`meu-negocio`, `minha-voz`, `minha-marca`, `conselho`, `conteudo`, `radar`,
`trafego`, `video`, `telegram`

E que as 6 pastas apareceram em `~/escritorio-ia/`: `negocio`, `voz`, `marca`,
`conselho`, `conteudo`, `radar`.

Se faltar alguma, refaça o passo correspondente e confira de novo. Não siga em
frente com instalação pela metade.

## Passo 6: o aviso que não pode faltar

Diga a ela, com estas palavras:

> Feche e abra o Claude Code de novo: skill nova só carrega em conversa nova.

## Passo 7: o primeiro passo dela

Feche assim:

> Depois de reabrir, diga: **use a skill meu-negocio**.

E avise que o mapa completo do que cada skill faz está no arquivo
`COMECE-AQUI.md`, dentro de `~/escritorio-ia/_kit/`.

---

## Telas que vão aparecer

Durante a instalação, o Claude Code vai parar e pedir permissão algumas vezes.
Explique isso para a pessoa antes de começar, para ela não achar que é vírus.

**"Posso rodar este comando?"**
Aparece antes de baixar o repositório e antes de criar as pastas. O comando fica
escrito na tela, inteiro. É o programa pedindo licença para mexer no computador
dela. Ela responde **sim**.

**"Posso criar esta pasta?" / "Posso escrever neste arquivo?"**
Aparece quando a instalação cria `~/escritorio-ia/` e quando qualquer skill for
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
