---
name: video
description: Edita o vídeo da pessoa: tira as gaguejadas, as repetições e os silêncios, gera a legenda e monta o arquivo final. Use quando ela disser que quer editar um vídeo, cortar uma gravação, tirar os erros da fala, legendar uma gravação, ou criar cortes para Reels, Shorts ou TikTok.
---

# video: a edição do seu vídeo

**Custo: $ · Frequência sugerida: por vídeo.**

Esta skill entrega o vídeo editado. Quem corta, legenda e monta o arquivo é a
skill **video-use**, uma skill de edição completa que trabalha por baixo desta.
O seu papel aqui é operar a video-use pela pessoa e traduzir cada passo para a
língua dela — alguém que provavelmente nunca abriu um editor de vídeo.

## A regra que governa esta skill

Pedido de edição de vídeo = **usar a skill video-use, agora**. Não pergunte se
pode usar, não ofereça caminho alternativo, não entregue uma lista de cortes em
texto no lugar do vídeo cortado. A pessoa pediu o vídeo editado; o resultado
desta conversa é o arquivo editado.

Só existem dois desvios, e os dois terminam voltando para a video-use:

1. **A video-use não está instalada** → conduza a instalação agora, pelo guia.
2. **Falta uma peça no meio do caminho** (ffmpeg, chave da ElevenLabs) →
   conserte com ela agora, pelo mesmo guia, e siga a edição.

## Passo 1: o vídeo

Pergunte onde está o arquivo do vídeo. É na pasta dele que a edição acontece, e
é ao lado dele que o resultado aparece.

**Dados de outras pessoas.** Antes de transcrever, avise em uma linha: o áudio
do vídeo vira texto nos servidores da ElevenLabs. Vídeo com dado sensível de
cliente ou paciente — nome, caso identificável, dado de saúde — não entra. Se
for o caso, peça outra gravação.

## Passo 2: a video-use

Invoque a skill video-use e siga o processo dela: transcrever, propor o plano
de corte, esperar o aval, executar. Enquanto ela trabalha, o seu papel é de
tradutor:

- O plano de corte que a video-use propõe, você apresenta em português simples:
  o que sai, por que sai, quanto tempo o vídeo perde. Nada de jargão de edição.
- Se a edição inclui legenda, uma escolha é dela, e você pergunta antes de
  montar o arquivo:

  > A legenda pode sair de dois jeitos: **gravada no vídeo**, sempre visível —
  > o formato de Reels, Shorts e TikTok — ou num **arquivo separado**, que você
  > envia junto no YouTube e quem assiste liga e desliga. Qual você prefere?
  > Se quiser, entrego os dois.

  Se ela não souber, sugira a gravada no vídeo, que é o formato das redes, e
  entregue o arquivo separado junto, que já sai de brinde da mesma edição.
- Nenhum corte acontece sem o "pode cortar" dela. A video-use já exige essa
  aprovação; você garante que a pergunta chegue clara.
- Uma pergunta por vez.
- O vídeo original fica intacto. O resultado sai numa pasta `edit/` ao lado do
  vídeo — mostre o caminho no fim e diga que é só abrir e assistir.

## Se a video-use não está instalada

Diga, sem drama: a skill que corta o vídeo ainda não está nesta máquina, e você
instala agora com ela — leva alguns minutos. Siga o guia
`ai-tools/_kit/avancado/video-completo.md` (a pasta `ai-tools` mora no caminho
gravado em `~/.config/ai-tools/local.txt`; se esse arquivo não existir, é
`~/ai-tools`). Você executa o que é de máquina; dela, só duas coisas: criar a
conta na ElevenLabs e escrever a chave no arquivo — **chave de acesso não se
cola no chat**: aponte o arquivo `.env` e peça para ela escrever a linha à mão.
Instalado e testado, volte ao Passo 2 e edite o vídeo desta conversa.

## Se algo quebrar no meio

ffmpeg ausente, chave da ElevenLabs faltando ou recusada, erro de instalação:
explique em uma frase o que faltou, conserte com ela pelo guia, e retome de onde
parou. Não desista para um caminho em texto; o combinado é entregar o vídeo.

## Fechamento

1. Mostre o caminho do arquivo final e diga o que fazer com ele.
2. Lembre, com naturalidade, que ela assiste ao vídeo inteiro antes de publicar:
   a máquina corta bem, mas quem conhece o público é ela. E publicar é com ela —
   você não posta nada.
