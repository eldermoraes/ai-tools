# Cortar o vídeo na própria máquina

Isto pede um programa extra instalado, espaço em disco e paciência de verdade. Se
você só quer a lista de cortes e as legendas para aplicar no editor que já usa,
não precisa deste guia: use a skill `video` e pronto, ela roda em qualquer
computador.

**Este é o único guia do kit em que "peça ajuda ao Claude" não é sugestão, é
instrução.** Não tente seguir sozinha. Abra o Claude Code, cole este arquivo
inteiro na conversa e escreva:

> Vamos fazer isto juntos. Eu uso [macOS / Windows] e o vídeo está em [caminho].

O motivo é honesto: cada vídeo tem um formato, uma duração e uma bagunça
diferente. Os comandos mudam de caso para caso. Quem monta o comando certo para o
seu arquivo é o Claude, olhando o seu arquivo. Um guia com comando fixo daria
errado em metade dos casos.

---

## O que você precisa ter

**Espaço em disco.** Regra de bolso: deixe livre umas três vezes o tamanho do
vídeo original. Um arquivo de 2 GB pede uns 6 GB livres. O processo cria arquivos
intermediários e depois apaga; se o disco encher no meio, ele para feio.

**O ffmpeg instalado.** É o programa que corta e junta vídeo de verdade. É
gratuito, é o mesmo que roda por baixo de metade dos editores do mercado, e não
tem tela: ele obedece comandos. Para conferir se você já tem:

```bash
ffmpeg -version
```

Se responder um monte de texto com números de versão, está instalado. Se responder
"command not found" ou "não é reconhecido", peça ao Claude:

> Preciso instalar o ffmpeg aqui. Me ajuda?

No macOS ele normalmente instala pelo Homebrew; no Windows, pelo winget. Deixe
ele conduzir e não baixe de sites aleatórios: ffmpeg é popular demais e tem cópia
adulterada circulando.

**Tempo.** Cortar e gerar o vídeo final leva minutos em arquivos curtos e pode
levar horas em vídeo longo, dependendo da máquina. Enquanto roda, o computador
fica mais lento. Não comece isso quinze minutos antes de uma reunião.

**O arquivo original, numa pasta só dele.** Crie uma pasta e coloque o vídeo lá
dentro. Isso evita que os arquivos intermediários se misturem com as suas coisas.

---

## O caminho, em três etapas

### Etapa 1: a transcrição

Nada acontece sem o texto do que foi dito, com as marcações de tempo.

Se a sua máquina já tem alguma ferramenta de transcrição instalada, peça ao Claude
para conferir e usar. Se não tem, o caminho continua sendo o da skill `video`: um
aplicativo de transcrição no celular, ou subir o vídeo como não listado no YouTube
e baixar a legenda automática que ele gera. As duas rotas devolvem um arquivo de
texto, e é só disso que você precisa.

Salve o arquivo de transcrição na mesma pasta do vídeo.

### Etapa 2: a lista de cortes

Aqui entra a skill do kit. No Claude Code:

> use a skill video

Passe a transcrição. Ela devolve a lista de cortes (hesitação, repetição, trecho
regravado, silêncio) com a marcação de tempo e o motivo de cada um, mais o arquivo
de legendas limpo.

**Leia a lista inteira antes de seguir.** Este é o passo que separa um resultado
bom de duas horas perdidas: se um corte estiver errado, é agora que custa dez
segundos para tirar da lista. Depois de gerar o vídeo, custa o processo inteiro de
novo. Diga ao Claude quais cortes você quer descartar e quais quer manter.

### Etapa 3: o corte

Com a lista aprovada por você, peça:

> Agora corta o vídeo de verdade com o ffmpeg, seguindo essa lista, sem mexer no
> arquivo original.

O Claude monta os comandos, corta os pedaços que ficam e junta tudo num arquivo
novo.

Duas exigências suas, e vale insistir nelas:

1. **Comece por um teste curto.** Peça para ele processar só os primeiros 30
   segundos primeiro. Você assiste, confere que o resultado tem cara de vídeo, e
   só então libera o arquivo inteiro. Descobrir um problema em 30 segundos é
   barato; descobrir depois de uma hora de processamento, não.
2. **O original não se toca.** O resultado sai em arquivo novo, com outro nome. Se
   o Claude propuser sobrescrever o original, recuse. Se o resultado ficar ruim,
   o original é a sua rede de segurança.

---

## Legendas na tela (opcional)

Se você quiser as legendas gravadas na imagem, em vez de arquivo separado:

> Agora queima as legendas no vídeo, usando o arquivo .srt que a skill gerou.

Isso gera o vídeo de novo do zero, então some mais um tanto de tempo e de espaço
em disco à conta. Vale quando o vídeo é para uma rede que não mostra legenda
sozinha.

Repare que legenda gravada na imagem não sai mais. Se você tem dúvida sobre o
texto, confira antes: um erro de digitação vira parte do vídeo.

---

## Quando parar e voltar para o caminho leve

Sem rodeio: se você chegou na segunda hora tentando fazer isso funcionar, pare.

A skill `video` sozinha já entrega a lista de cortes e as legendas. Aplicar isso no
CapCut, no InShot ou no editor que você já domina leva quinze minutos e sai do
jeito que você quer, porque você está vendo a imagem enquanto decide. O ganho de
cortar pela máquina aparece quando você tem muitos vídeos parecidos, todo mês. Num
vídeo avulso, o caminho leve chega antes.

Isto aqui não é o degrau superior obrigatório. É outra ferramenta, boa para outro
tipo de repetição.

---

## Se travar

Cole o erro inteiro na conversa e peça: "o que isso quer dizer e o que eu faço?".
Mensagem de erro de ffmpeg é longa e assustadora, e quase sempre diz exatamente
uma de três coisas: faltou espaço, o caminho do arquivo está errado, ou o formato
do vídeo pede um ajuste no comando. As três se resolvem na mesma conversa.

Se o computador ficar lento a ponto de atrapalhar, é normal enquanto processa.
Você pode interromper com **Ctrl+C** no terminal: o arquivo original continua
intacto, e você recomeça quando quiser.
