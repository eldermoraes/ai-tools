# Fazer o radar rodar sozinho de manhã

Isto pede a skill `radar` já configurada e rodando bem quando você pede à mão. Se
você nunca rodou o radar, pare e rode pelo menos uma vez antes: agendar algo que
você nunca viu funcionar é agendar um problema para as 7 da manhã.

Este guia serve para você e para o seu Claude ao mesmo tempo. Abra o Claude Code,
cole este arquivo inteiro na conversa e escreva:

> Me ajuda a seguir este guia, passo a passo. Eu uso [macOS / Windows].

---

## A parte honesta, antes de qualquer comando

**Computador desligado não roda nada.** Não existe mágica aqui: o agendador é um
programa do seu próprio computador, e programa desligado não trabalha. Se você
desliga a máquina à noite, o radar das 7h não vai acontecer.

Três variações disso, para você saber o que esperar:

- **Máquina ligada, tela apagada:** roda normal.
- **Máquina dormindo (notebook fechado):** o macOS costuma rodar assim que
  acorda, com atraso. O relatório sai, mas não na hora combinada.
- **Máquina desligada:** não roda. Quando você ligar, dependendo do sistema, ele
  pode tentar rodar o que perdeu, ou simplesmente esperar o dia seguinte.

Se a sua rotina é abrir o computador às 9h e trabalhar, agende para as 9h05 e
pronto. Melhor um horário que existe do que um horário bonito.

**Custo:** o radar busca na internet e gasta da sua cota toda vez que roda. Rodando
todo dia, é todo dia. Se você usa o Claude para outras coisas, comece de segunda a
sexta e veja como fica antes de colocar sábado e domingo.

**Ninguém confere por você.** O relatório vai sair sozinho, com IA, sem revisão.
Ele serve para você começar o dia sabendo onde olhar. Não serve para agir sem ler.

---

## Passo 1: escolher o horário e testar o comando à mão

Primeiro decida a hora. Depois, na conversa com o Claude, peça:

> Monta o comando que roda a skill radar sem ninguém na frente da tela, e testa
> aqui comigo agora.

Ele conhece as opções da própria ferramenta e monta o comando certo para a sua
versão. Este guia não tenta adivinhar isso por ele.

Rode o comando pronto **uma vez, com você olhando**. Depois confira se apareceu o
arquivo do dia:

```bash
ls ~/ai-tools/radar/
```

Esse caminho vale para quem instalou a pasta `ai-tools` na pasta pessoal, que é o
padrão. Se você escolheu outro lugar na instalação, peça ao Claude para ajustar:
o caminho de verdade está gravado em `~/.config/ai-tools/local.txt`.

Tem que existir um arquivo com a data de hoje, no formato `2026-08-15.md`. Se não
apareceu, não agende nada ainda: resolva isso primeiro, colando o erro na conversa.

Guarde o comando que funcionou. Ele é a peça central dos próximos passos.

Uma pegadinha comum: o agendador roda num ambiente mais limpo que o seu Terminal e
às vezes não acha os programas pelo nome curto. Peça ao Claude o caminho completo:

```bash
which claude
```

Use o caminho completo que ele devolver, não só a palavra `claude`.

## Passo 2 (macOS): montar o agendamento

No macOS o agendador se chama **launchd**, e a receita dele é um arquivo de texto
guardado em `~/Library/LaunchAgents/`.

Peça ao Claude:

> Cria o arquivo do launchd para rodar aquele comando todo dia às 7h, com log de
> saída, e me ensina como ligar e desligar.

O arquivo tem esta forma. Quem preenche é o Claude, com o comando que funcionou no
Passo 1:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai-tools.radar</string>
    <key>ProgramArguments</key>
    <array>
        <!-- aqui entra o comando que funcionou no Passo 1 -->
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>7</integer>
        <key>Minute</key><integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/radar.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/radar-erro.log</string>
</dict>
</plist>
```

As duas últimas linhas são o que salva a sua vida quando algo não rodar: elas
guardam o que aconteceu em `/tmp/radar.log` e `/tmp/radar-erro.log`. Sem isso, uma
falha às 7h é silêncio puro.

Com o arquivo salvo em `~/Library/LaunchAgents/ai-tools.radar.plist`, ligue:

```bash
launchctl load -w ~/Library/LaunchAgents/ai-tools.radar.plist
```

Para desligar depois, o contrário:

```bash
launchctl unload -w ~/Library/LaunchAgents/ai-tools.radar.plist
```

## Passo 2 (Windows): montar o agendamento

No Windows o programa se chama **Agendador de Tarefas** (Task Scheduler) e tem
tela, o que ajuda. Peça ao Claude:

> Me guia pelo Agendador de Tarefas do Windows para rodar aquele comando todo dia
> às 7h.

O caminho, em linhas gerais:

1. Abra o menu Iniciar e busque por "Agendador de Tarefas".
2. No lado direito, **Criar Tarefa Básica**.
3. Dê um nome: "Radar do negócio".
4. Quando começar: **Diariamente**. Escolha a hora.
5. Ação: **Iniciar um programa**. Aqui vai o comando do Passo 1, quebrado em
   programa e argumentos. Deixe o Claude dizer exatamente o que vai em cada campo.
6. Antes de concluir, marque a opção de abrir as propriedades. Lá dentro, na aba
   Condições, existe a opção de **ativar o computador para executar a tarefa**.
   Ligue se o seu computador dorme mas fica na tomada.

## Passo 3: conferir no dia seguinte

Amanhã, depois da hora marcada:

```bash
ls -la ~/ai-tools/radar/
```

(De novo: se a sua pasta `ai-tools` mora em outro lugar, o caminho certo está em
`~/.config/ai-tools/local.txt`.)

Se apareceu o arquivo com a data de hoje, funcionou. Abra e leia.

Se não apareceu, no macOS olhe o registro do que aconteceu:

```bash
cat /tmp/radar-erro.log
```

Cole o conteúdo na conversa com o Claude e peça ajuda. Nove em cada dez vezes é
caminho de programa ou permissão, e resolve em dois minutos.

## Passo 4 (opcional): receber no celular

Se você já configurou a skill `telegram` (o guia está em `_kit/avancado/telegram.md`,
dentro da sua pasta `ai-tools`), dá para o agendamento entregar o
relatório no seu celular assim que ele ficar pronto, em vez de esperar você abrir
a pasta.

Peça ao Claude:

> Depois de gerar o radar, manda o arquivo do dia pro meu Telegram, no mesmo
> agendamento.

Ele acrescenta o envio ao que já está montado. Se a skill `telegram` não estiver
configurada, este passo simplesmente não existe: pule.

---

## Como desistir

Você pode desligar o agendamento a qualquer momento sem quebrar nada. Os
relatórios que já saíram continuam na pasta, e a skill `radar` continua
funcionando quando você pedir à mão. Agendar é conveniência, não dependência.

No macOS, o `launchctl unload` do Passo 2. No Windows, botão direito na tarefa e
**Desabilitar**. Se preferir, peça ao Claude: "desliga o agendamento do radar".
