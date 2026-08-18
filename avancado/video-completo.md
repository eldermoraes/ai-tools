# O vídeo que se edita sozinho (fluxo completo)

Isto pede instalação de programas, uma conta num serviço de transcrição e
paciência na primeira vez. Normalmente você nem abre este guia por conta
própria: é a skill `video` que segue estes passos com você, na primeira vez que
você pedir um vídeo editado nesta máquina.

Ele também funciona sozinho, se você preferir instalar antes. Abra o Claude
Code, cole este arquivo inteiro na conversa e escreva:

> Me ajuda a instalar isso, passo a passo.

---

## O que você vai montar

Uma skill de edição de verdade, chamada **video-use**. Depois de instalada, o
uso é assim: você coloca os vídeos numa pasta, abre o Claude nela e diz "edita
esse vídeo: corta as gaguejadas e gera legenda". Ele transcreve, mostra o plano
de corte em português claro, espera o seu aval, e aí corta, legenda e monta o
arquivo final. Sem editor aberto, sem linha do tempo, sem menu.

É um projeto aberto e gratuito, mantido fora deste kit:
https://github.com/browser-use/video-use

## O que precisa existir (e o que custa)

1. **O ffmpeg**, o programa gratuito que corta e monta vídeo de verdade. A
   instalação dele faz parte dos passos abaixo.
2. **Uma conta na ElevenLabs**, o serviço que transcreve o vídeo palavra por
   palavra, com o tempo de cada uma (é isso que permite cortar sem errar). Tem
   faixa gratuita para começar, e o uso além dela é pago. Criar a conta e a
   chave de acesso é a única parte que é sua.
3. **Espaço em disco e paciência.** Renderizar demora minutos num vídeo curto e
   pode demorar muito num longo. Enquanto roda, o computador fica mais lento.

Uma honestidade antes de seguir: o áudio dos seus vídeos é processado nos
servidores da ElevenLabs para virar texto. Vale aqui a mesma regra de todo o
kit: vídeo com dado sensível de cliente ou paciente não entra.

## Passos

### 1. Instalar

Peça ao Claude, com estas palavras:

> Clona o repositório https://github.com/browser-use/video-use para uma pasta
> estável e segue o install.md dele.

O `install.md` do projeto foi escrito para o próprio agente executar: ele clona,
instala o ffmpeg (pedindo a sua confirmação antes), registra a skill e testa. A
única coisa que ele não consegue gerar é a chave da ElevenLabs, e essa é o
próximo passo.

### 2. A chave de acesso

Crie a conta em https://elevenlabs.io e gere uma chave de acesso (nas
configurações da conta, na parte de API Keys).

A boa prática é a mesma da skill `telegram`: **chave de acesso não se cola em
chat**. Quando o agente pedir a chave, diga "eu mesmo escrevo" e peça o caminho
do arquivo. Ele indica o arquivo `.env` na pasta do projeto; você abre num
editor de texto, escreve a linha da chave à mão, salva e avisa que está pronto.

Se você colar por engano, sem drama: gere uma chave nova no site da ElevenLabs
e apague a antiga por lá.

### 3. O teste de verdade

Coloque **um vídeo curto** (um minuto resolve) numa pasta, abra o Claude Code
nessa pasta e diga:

> Edita esse vídeo: corta os silêncios e as gaguejadas e gera legenda.

Ele transcreve, mostra o plano de corte e espera você aprovar. Só corta depois
do seu aval. No fim, o arquivo editado aparece numa pasta `edit/` ao lado do
vídeo. O original fica intacto, sempre.

Se o teste passou, está instalado. Daqui em diante é só abrir o Claude na pasta
dos vídeos e pedir.

## Quando parar

Sem rodeio: se você chegou na segunda hora tentando fazer isso funcionar, pare
e deixe para outro dia — a instalação é uma vez só, e ela não vale uma tarde.
Guarde o erro que apareceu (copie a mensagem inteira) e, na próxima conversa,
cole e pergunte o que ele quer dizer. Instalação pela metade não estraga nada:
o próximo `use a skill video` retoma de onde parou.

## Se travar

Cole o erro inteiro na conversa e peça: "o que isso quer dizer e o que eu
faço?". Instalação de programa, chave de acesso e formato de vídeo são as três
causas de quase tudo, e as três se resolvem na mesma conversa.
