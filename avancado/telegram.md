# Configurar a skill `telegram`

Isto pede o Telegram instalado no seu celular e uns dez minutos de atenção. Se
você ainda não instalou o kit, pare e faça a instalação primeiro: esta
configuração é uma etapa à parte e não roda junto com ela.

Este guia serve para você e para o seu Claude ao mesmo tempo. Abra o Claude Code,
cole este arquivo inteiro na conversa e escreva:

> Me ajuda a seguir este guia, passo a passo.

Uma coisa só é sua, e não dá para delegar: o Passo 2. Leia o aviso lá antes de
começar.

---

## O que você vai montar

Um robozinho seu dentro do Telegram (um "bot"), que só fala com você. Quando você
pedir ao Claude "me manda esse arquivo no celular", ele entrega ali. É de mão
única: a skill só envia. Ela não lê as suas mensagens do Telegram, não responde
ninguém e não entra em grupo.

---

## Passo 1: criar o bot

Isto acontece dentro do Telegram, no celular. Nenhum comando, nenhum terminal.

1. Abra o Telegram e busque por **@BotFather** (com essa grafia exata; o perfil
   tem selo azul de verificado).
2. Abra a conversa e toque em **Iniciar** (ou mande `/start`).
3. Mande a mensagem `/newbot`.
4. Ele pede um **nome**. Pode ser qualquer coisa: "Avisos da Marina".
5. Ele pede um **nome de usuário**, que precisa ser único no mundo e terminar em
   `bot`. Se der "já existe", tente outro: `avisos_marina_2026_bot`.
6. Ele responde com uma mensagem de parabéns e, no meio dela, uma linha comprida
   de letras, números e um sinal de dois pontos. **É esse o código de acesso do
   seu bot.**

Deixe essa conversa aberta. Você vai voltar nela daqui a pouco.

## Passo 2: guardar o código de acesso, à mão

**Este código não se cola em chat. Nem no do Claude.**

Com todas as letras: não cole esse código na conversa com a IA, não mande por
WhatsApp, não passe por e-mail, não coloque num documento compartilhado. Quem tem
o código controla o bot. Ele vai de um lugar só (a conversa do BotFather) para um
lugar só (um arquivo na sua máquina), e o caminho entre os dois é o seu dedo.

Se você colar por engano, não tem drama: volte no BotFather, mande `/revoke`,
escolha o bot, e ele gera um código novo. O antigo morre na hora. Faça isso sempre
que desconfiar.

**Primeiro, prepare o arquivo vazio.** Estes comandos criam a pasta e o arquivo já
protegidos. Pode pedir ao Claude para rodar, ou colar no Terminal você mesma:

```bash
mkdir -p ~/.claude/telegram
chmod 700 ~/.claude/telegram
touch ~/.claude/telegram/.env
chmod 600 ~/.claude/telegram/.env
```

**Agora abra o arquivo num editor de texto.** No macOS:

```bash
open -e ~/.claude/telegram/.env
```

Abre o TextEdit com uma folha em branco. Escreva uma linha só, assim:

```
TELEGRAM_BOT_TOKEN=
```

E depois do sinal de igual, **digite o código do bot**. Sem espaço antes, sem
espaço depois, sem aspas. A linha inteira fica parecida com isto (o código abaixo
é inventado, o seu é outro):

```
TELEGRAM_BOT_TOKEN=8123456789:AAF3xk_exemplo_inventado_nao_use_isto
```

Se preferir não digitar caractere por caractere, copie do Telegram e cole **no
editor de texto**. Copiar e colar dentro do seu computador é seguro. O que não
pode é colar na conversa com a IA.

Salve (Cmd+S) e feche a janela. Depois de salvar, rode de novo:

```bash
chmod 600 ~/.claude/telegram/.env
```

O editor às vezes afrouxa a proteção do arquivo ao salvar. Esse comando aperta de
volta. O script confere isso e recusa funcionar com o arquivo aberto demais.

**No Windows**, o caminho é o mesmo com outro editor (Bloco de Notas). Peça ao
Claude: "me ajuda a criar esse arquivo aqui no Windows". Deixe ele montar os
comandos; a digitação do código continua sendo sua.

## Passo 3: mandar um oi para o bot

Volte ao Telegram, no celular. Busque pelo nome de usuário que você criou no Passo
1 (aquele terminado em `bot`), abra a conversa, toque em **Iniciar** e mande
qualquer coisa: um "oi" resolve.

Isso não é enfeite. É assim que o bot descobre quem é você. Sem essa mensagem, o
próximo passo não tem o que encontrar.

## Passo 4: dizer para onde enviar

De volta ao computador, rode:

```bash
python3 ~/.claude/skills/telegram/telegram.py --setup
```

Ele mostra uma lista de candidatos, com um número comprido na frente de cada um, e
para. É assim mesmo: ele não escolhe por você. Ache a linha com o seu nome e copie
o número.

O aviso na tela é sério: candidato único não prova nada. Se alguém mandou mensagem
para o seu bot antes de você, essa pessoa aparece na lista também. Confira o nome
antes de copiar.

Agora grave, trocando `<NUMERO>` pelo número que você copiou:

```bash
python3 ~/.claude/skills/telegram/telegram.py --setup --chat-id <NUMERO>
```

Ele confirma que gravou. Pronto: esse é o único destino que a skill aceita, para
sempre. Não existe jeito de mandar mensagem para outra pessoa por acidente.

## Passo 5: conferir

```bash
python3 ~/.claude/skills/telegram/telegram.py --doctor
```

Ele lista o que encontrou e termina com `diagnóstico: ok`. Do código de acesso,
mostra só os dois primeiros caracteres: ele nunca imprime o código inteiro em
lugar nenhum, nem quando dá erro.

Se der `diagnóstico: 1 problema(s)` ou mais, a própria mensagem diz o que fazer.
Não decifre sozinha: cole o texto inteiro na conversa com o Claude e peça ajuda.
Pode colar essa saída à vontade, o código de acesso não aparece nela.

## Passo 6: o teste de verdade

No Claude Code, escreva:

> manda um oi pro meu celular

Se o celular vibrar, acabou. Está funcionando.

A partir de agora vale para qualquer coisa: "me manda esse PDF no celular", "me
manda esse resumo no Telegram", "manda o radar de hoje pra mim".

---

## Precisa de Python 3

O pedaço que conversa com o Telegram é um programa em Python. **No macOS já vem
instalado**, então provavelmente não há nada a fazer. Para confirmar:

```bash
python3 --version
```

Se responder um número de versão, está resolvido.

**No Windows**, o Python normalmente não vem instalado, e o comando se chama
`python` em vez de `python3`. Não saia baixando de qualquer site: peça ao Claude
na conversa:

> Preciso instalar o Python 3 aqui no Windows. Me ajuda?

Ele monta os comandos e acompanha.

## Windows: uma ressalva franca

Antes de enviar qualquer coisa, o programa confere se o arquivo com o código de
acesso está fechado para outras pessoas do computador. Essa conferência usa o jeito
do Mac e do Linux de marcar permissão de arquivo, e o Windows marca de outro jeito.
Resultado: no Windows puro, o programa costuma recusar e reclamar da permissão,
mesmo com tudo certo.

Não é defeito da sua instalação, e não adianta insistir no `chmod`. Os caminhos que
funcionam:

- **Rodar pelo WSL** (o Linux que roda dentro do Windows). Cole este parágrafo na
  conversa com o Claude e peça: "me ajuda a instalar o WSL e rodar isso lá dentro".
- **Usar esta skill num Mac ou num Linux**, se você tiver acesso a um.

O resto do kit funciona normalmente no Windows. Só esta skill tem essa trava, e ela
existe porque proteger o código de acesso vale mais do que a comodidade de rodar em
qualquer lugar.

---

## Se você quiser mudar o destino depois

Por desenho, o `--setup` configura o destino uma vez e não troca destino
configurado. Para mudar, abra `~/.claude/telegram/.env` no editor, apague a linha
que começa com `TELEGRAM_ALLOWED_CHATS`, salve, rode `chmod 600` de novo e refaça
os Passos 3 e 4.

Dá um pouco mais de trabalho de propósito: trocar o destino de uma mensagem é
exatamente o tipo de coisa que não deve acontecer sem alguém decidindo.
