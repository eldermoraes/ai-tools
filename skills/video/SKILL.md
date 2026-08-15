---
name: video
description: Transforma a transcrição de um vídeo em lista de cortes com marcação de tempo, arquivo de legendas pronto para importar no editor e sugestões de clipes curtos. Use quando a pessoa disser que quer cortar um vídeo, tirar as gaguejadas e as repetições, gerar legenda, criar cortes para Reels, Shorts ou TikTok, ou pedir ajuda para editar uma gravação.
---

# video: cortes e legendas a partir da transcrição

**Custo: $ · Frequência sugerida: por vídeo.**

Esta skill trabalha em cima do texto do vídeo, e por isso roda em qualquer computador,
mesmo os mais simples. Ela não abre o arquivo do vídeo, não instala nada e não demora.

**O que ela entrega:** a lista do que cortar (com o minuto e o motivo), um arquivo de
legendas limpo, e sugestões de trechos que funcionam sozinhos como vídeo curto.

**O que ela não faz:** ela não corta e não gera o vídeo final. Ela escreve o mapa; quem
corta é você, no editor que já usa (CapCut, InShot, Premiere, o que for). O caminho em
que a própria máquina corta e monta o arquivo existe e está escrito no guia
`avancado/video-completo.md`, instalado em
`~/escritorio-ia/_kit/avancado/video-completo.md`. Ele pede programas extras e espaço em
disco.

## Como você conduz esta conversa

- Uma pergunta por vez.
- Português simples, sem termo de edição que a pessoa possa não conhecer.
- Não invente tempo, não invente frase e não invente corte. Tudo o que você marcar tem
  que estar na transcrição.
- Grave os arquivos assim que ficarem prontos, um por um, e mostre o caminho de cada um
  no fim. Nunca grave nada dentro da pasta do repositório baixado.

## Passo 1: a transcrição

Peça a transcrição do vídeo. Ela pode colar o texto na conversa ou apontar um arquivo
`.txt`, `.srt` ou `.vtt` na máquina.

**Se ela só tem o vídeo e não tem transcrição**, ofereça estes caminhos, sem prometer
fazer a transcrição por ela:

- **YouTube**: suba o vídeo como não listado, espere alguns minutos e copie a
  transcrição automática. É gratuito e sai com a marcação de tempo pronta.
- **No celular**: aplicativos de transcrição e de legenda automática geram o texto a
  partir do vídeo ou do áudio. O CapCut, por exemplo, gera legenda automática e permite
  exportar o arquivo de legendas.
- **No computador**: o editor que ela já usa provavelmente tem legenda automática. O
  arquivo exportado por ele serve aqui.

Diga com todas as letras: esta conversa não faz a transcrição do arquivo de vídeo. Ela
começa depois que o texto existe.

## Passo 2: conferir se dá para marcar o tempo

Olhe a transcrição antes de prometer qualquer coisa.

- **Tem marcação de tempo** (formato `.srt`, `.vtt`, ou texto com `00:01:23` no meio):
  ótimo, dá para fazer tudo.
- **Não tem marcação de tempo** (texto corrido): diga isso na hora. Sem tempo, você
  consegue apontar os trechos pelo que está escrito ("o pedaço que começa em *então,
  assim...*"), mas não consegue montar o arquivo de legendas nem dar o minuto do corte.
  Ofereça o caminho do YouTube do passo 1, que devolve o texto com o tempo. Se ela
  preferir seguir sem o tempo, siga assim: a lista de cortes sai com o texto de cada
  trecho no lugar do minuto, e os clipes saem com a primeira e a última frase de cada
  um, para ela achar no editor pela fala. Legenda não sai, e você diz isso de novo no
  fim, para não haver surpresa.

## Passo 3: o que ela quer (uma pergunta só)

Pergunte, de uma vez:

> O que você quer que eu prepare?
>
> 1. **Lista de cortes**: o que tirar, com o minuto e o motivo, para você aplicar no seu
>    editor.
> 2. **Legendas**: um arquivo pronto para importar, já sem os trechos cortados.
> 3. **Clipes curtos**: 2 ou 3 trechos que funcionam sozinhos como vídeo curto.
>
> Pode escolher mais de uma.

Se ela não souber, faça a 1 e a 2, que é o que serve para qualquer vídeo.

Leia `~/escritorio-ia/negocio/contexto.md`, se existir. Saber o que ela vende e para quem
muda quais trechos você sugere como clipe.

**Dados de outras pessoas.** Se a transcrição tiver nome completo, telefone, valor de
contrato, dado de saúde ou caso identificável de um cliente ou paciente, avise e sugira
cortar esse trecho ou trocar por uma versão sem identificação: descreva o padrão, não o
caso. Não repita esses dados nos arquivos que você gravar.

## Passo 4: a lista de cortes

Procure no texto, nesta ordem de prioridade:

- **Hesitações e vícios**: "éé", "ãã", "tipo assim", "né", "então" no começo de frase,
  repetidos.
- **Repetições**: a mesma ideia dita duas vezes seguidas com palavras parecidas.
- **Regravações**: quando ela erra, para e recomeça a frase. Corta a primeira, fica a
  segunda.
- **Silêncios e enrolação**: trechos longos que não avançam o assunto, do tipo "deixa eu
  ver aqui", "peraí".
- **Início e fim**: quase todo vídeo começa e termina com sobra. O primeiro corte
  costuma ser a entrada; o último, a despedida arrastada.

Entregue como tabela, uma linha por corte:

| De | Até | O que está sendo dito | Por que cortar |
|---|---|---|---|
| 00:00 | 00:07 | "deixa eu ver se está gravando..." | sobra do começo |
| dentro de 01:20 | — | "éé, tipo assim" (antes de "a drenagem") | hesitação no meio da fala |

**Você só escreve um tempo que está escrito na transcrição.** Quando o corte é um trecho
inteiro, use o tempo dele. Quando é uma gaguejada no meio de uma fala, a transcrição não
tem o segundo exato: escreva `dentro de` mais o tempo do trecho onde ela está, e cite as
palavras vizinhas para ela achar. Nunca calcule, estime ou arredonde um segundo que não
estava lá.

Duas regras:

- **Cada corte precisa ter o texto do trecho junto**, para ela conferir que é aquilo
  mesmo antes de apagar.
- **Não corte conteúdo.** Se você achar que uma parte é fraca ou longa demais, isso vai
  como sugestão separada no fim, marcada como opinião, e ela decide. Corte automático é
  só o que ninguém sente falta.

No fim da lista, diga quanto tempo o vídeo perde somando os cortes, se a transcrição
tiver marcação de tempo.

## Passo 5: o arquivo de legendas

Gere um arquivo `.srt` limpo, com os trechos cortados já fora e a numeração
recalculada do começo.

Formato, exatamente assim (número da legenda, tempo, texto, linha em branco):

```
1
00:00:07,000 --> 00:00:10,500
Bom dia! Hoje eu vou falar sobre uma coisa
que quase ninguém comenta.

2
00:00:10,600 --> 00:00:13,900
Se você já passou por isso, vai reconhecer na hora.
```

Ao escrever as legendas:

- no máximo duas linhas por legenda, e frases curtas, que é o que cabe na tela do
  celular;
- corte a legenda onde a frase respira, não no meio de uma palavra;
- arrume as hesitações e a pontuação do texto falado, sem trocar as palavras dela nem
  mudar o sentido.

**Em que tempo esse arquivo roda.** O `.srt` é feito para o vídeo **depois** dos cortes:
você tira os trechos cortados e recalcula os tempos desde o começo, sem deixar buraco. A
duração de cada fala continua sendo a real, tirada da transcrição — o que muda é só onde
ela cai na linha do tempo, porque o que veio antes encurtou.

Diga isso a ela em uma linha, junto com o arquivo: ele serve depois de aplicar a lista
de cortes inteira. Se ela aplicar só uma parte, ofereça gerar de novo com os cortes que
ela escolheu. Se ela não for cortar nada, gere sem recalcular, no tempo original.

## Passo 6: os clipes (se ela pediu)

Sugira 2 ou 3 trechos que funcionam sozinhos, cada um com:

- **início e fim**, com a marcação de tempo **do vídeo original**, o arquivo que ela tem
  na mão agora. Escreva isso com todas as letras no topo da lista de clipes: aqui os
  tempos são os do vídeo como ele está, e não os do arquivo de legendas, que roda depois
  dos cortes. São duas contagens diferentes, e ela precisa saber qual está usando para
  não procurar o trecho no minuto errado;
- **a primeira frase**, copiada da transcrição, que é o que segura a pessoa nos primeiros
  segundos;
- **por que esse trecho funciona sozinho**: ele responde uma pergunta inteira, conta uma
  história curta, ou entrega um número concreto.

Prefira trechos entre 30 e 90 segundos. Se nenhum trecho se sustentar sozinho, diga isso
com franqueza em vez de inventar três.

## Passo 7: onde gravar

- Se ela apontou um arquivo de transcrição na máquina, grave os arquivos **na mesma
  pasta** dele, com o mesmo nome e um final diferente (`-cortes.md`, `-legendas.srt`,
  `-clipes.md`). É lá que ela vai procurar na hora de editar.
- Se ela colou o texto na conversa, pergunte onde salvar e sugira a Área de Trabalho
  (`~/Desktop`): é de lá que ela vai arrastar o arquivo de legendas para dentro do
  editor. Se ela preferir outra pasta, use a que ela disser.

## Fechamento

1. Mostre o caminho de cada arquivo criado e diga o que fazer com ele: a lista de cortes
   se lê com o editor aberto do lado; o arquivo `.srt` se arrasta para dentro do projeto,
   ou se importa pelo menu de legendas do editor.
2. Lembre, sem drama, que a lista é uma leitura do texto. Você não ouviu o vídeo: pausas
   de efeito, risada e mudança de entonação não aparecem na transcrição. Ela confere antes
   de apagar qualquer coisa.
3. Se ela quiser que a própria máquina corte e monte o vídeo, aponte
   `avancado/video-completo.md` e diga o que aquilo pede: programas extras, espaço em
   disco e paciência.
