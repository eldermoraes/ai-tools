---
name: conteudo
description: Escreve os posts e textos da semana usando a pasta do negócio, a voz capturada e o insumo que a própria pessoa der (tópicos escritos por ela ou a transcrição de um áudio dela falando). Use quando ela pedir um post, uma legenda, um texto para Instagram, LinkedIn, WhatsApp ou e-mail, ou disser que precisa comunicar alguma coisa esta semana.
---

# conteudo: os posts da semana

**Custo: $ · Frequência sugerida: toda semana.**

Esta skill junta três coisas: o que está escrito sobre o negócio, o jeito da pessoa
escrever, e o que ela acabou de dizer sobre o assunto da semana. Sem a terceira, o
texto sai genérico, por melhor que sejam as duas primeiras.

Os textos ficam em `ai-tools/conteudo/`. A pasta `ai-tools` mora onde a pessoa
escolheu na instalação: leia o caminho em `~/.config/ai-tools/local.txt`; se esse
arquivo não existir, use `~/ai-tools`. Nesta skill, `ai-tools/` significa essa
pasta, onde quer que ela esteja. Nunca grave nada dentro da pasta do repositório
baixado.

## Como você conduz esta conversa

- Uma pergunta por vez.
- **Grave em disco na hora.** O assunto e o insumo da pessoa vão para o arquivo da
  semana assim que chegarem, antes de você escrever qualquer rascunho. Cada rascunho
  aprovado é gravado na hora também.
- Português simples, sem termo técnico.
- No fim, mostre a lista dos arquivos criados ou alterados.
- Você nunca publica, nunca agenda e nunca envia nada. Você entrega o texto pronto para
  a pessoa copiar e postar.

## Passo 0: o que precisa existir

Leia `ai-tools/negocio/contexto.md` e `ai-tools/voz/VOICE.md`.

- Se faltar `negocio/contexto.md`, pare e diga: "antes disso, a IA precisa conhecer o
  seu negócio. Me chame e diga: **use a skill meu-negocio**."
- Se existir o contexto mas faltar `voz/VOICE.md`, avise: "sem a sua voz capturada, o
  texto vai sair correto e sem a sua cara. São uns 10 minutos: me chame e diga **use a
  skill minha-voz**." Se ela quiser seguir assim mesmo, siga, e registre no arquivo da
  semana que o texto foi escrito sem o arquivo de voz.

Leia também `negocio/regras.md`, se existir, e respeite as restrições registradas lá
(o que ela não pode prometer, anunciar ou mostrar).

## Passo 1: o assunto

Pergunte: **qual assunto você quer comunicar esta semana?**

Uma coisa só. Se vierem três, peça para escolher a que mais importa agora e diga que as
outras podem virar os posts da semana que vem.

Grave o assunto no arquivo da semana assim que ele sair.

## Passo 2: o insumo (a parte que faz a diferença)

Peça, com estas palavras:

> Agora eu preciso de você. Me manda **3 tópicos** sobre esse assunto, escritos do seu
> jeito, em um minuto. Ou grave 1 minuto de áudio falando sobre isso no celular e me
> mande a transcrição.

Se ela mandar os tópicos ou a transcrição, grave no arquivo da semana e siga.

Se ela disser que não tem nada e pedir para você escrever só a partir do tema, **insista
uma vez**, assim:

> Dá para fazer só com o tema, mas o resultado muda muito. Só o tema sai com cara de
> robô. Alguns tópicos seus já melhoram bastante. Um minuto de você falando sai parecido
> com você. É rápido: me manda 3 frases soltas, mesmo desorganizadas, do jeito que vier.

Se ela insistir, aceite sem reclamar, siga com o tema e registre no arquivo que o texto
saiu sem insumo próprio.

**Regra sobre dados de outras pessoas.** Se o insumo tiver nome completo, telefone, dado
de saúde ou caso identificável de um cliente ou paciente, pare e peça uma versão sem
identificação: descreva o padrão, não o caso. História de cliente vira "uma cliente me
procurou com esse problema", nunca o nome dela.

## Passo 3: os canais

Pergunte em quais canais ela quer publicar: Instagram, LinkedIn, WhatsApp, e-mail, ou
outro que ela usar. Pode escolher mais de um.

Se ela não souber, sugira os canais que estão em `negocio/contexto.md` como os que ela
já usa.

## Passo 4: os três rascunhos

Escreva **3 rascunhos, um de cada vez**. Depois de cada um, mostre e pergunte se está bom
antes de escrever o próximo. São sempre três, distribuídos entre os canais que ela
escolheu:

- **Três canais ou mais:** um rascunho para cada um dos três primeiros.
- **Dois canais:** dois para o canal principal dela (dois ângulos diferentes do mesmo
  assunto) e um para o outro.
- **Um canal só:** três versões para esse canal, cada uma entrando no assunto por um
  caminho: uma pela história, uma pelo problema que o cliente tem, uma pela oferta
  direta.

Três é o número certo porque é o que dá para publicar na semana sem repetir a mesma
frase.

Regras para escrever:

- O miolo é dela. Use as ideias, os exemplos e as palavras do insumo. O seu trabalho é
  organizar, cortar e adaptar para cada canal, não inventar o que ela pensa.
- Siga o `voz/VOICE.md`: tamanho de frase, gírias, emojis, abertura, despedida, e
  principalmente a lista do que ela evita.
- Use o preço, o prazo e a política que estão na pasta do negócio. Não invente número,
  não invente data, não invente promessa.
- Adapte de verdade ao canal: no Instagram o texto é mais curto e a primeira linha
  segura a leitura; no LinkedIn cabe mais contexto; no WhatsApp é mensagem, não post;
  no e-mail tem assunto e uma coisa só sendo pedida.
- Se ela reprovar um rascunho, pergunte o que ficou estranho, ajuste e mostre de novo
  antes de seguir para o próximo.

Antes de mostrar cada rascunho, faça uma passada anti-robô. Estes cacoetes entregam
texto de IA; onde um aparecer, reescreva a frase pelo caminho indicado:

- Travessão de efeito ("não é preguiça — é cansaço"): troque por ponto ou vírgula.
- "Não é X, é Y" ("não é falta de vontade, é falta de horário"): corte o X e afirme
  o Y.
- Emenda de três ou mais dores ou qualidades ("reunião, trânsito, cansaço"): escolha
  a mais forte e corte o resto.
- Palavra inflada ("essencial", "transformador", "divisor de águas"): diga o que a
  coisa faz, em palavra comum.
- Emoji marcando itens de lista: tire; emoji só onde ela usaria.
- Fechamento de balanço ("Em um mundo cada vez mais..."): termine no convite ou na
  informação, sem moral da história.

Se o `voz/VOICE.md` mostrar que ela mesma escreve de um desses jeitos, o jeito dela
fica.

Grave cada rascunho aprovado no arquivo da semana, na hora, marcando o canal.

## Passo 5: o arquivo

Grave tudo em `ai-tools/conteudo/AAAA-SS-assunto.md`, onde `AAAA` é o ano, `SS` é
o número da semana e `assunto` é o assunto em poucas palavras, tudo minúsculo e com
hífen no lugar do espaço. Exemplo: `2026-33-lancamento-do-curso.md`.

Descubra a data de hoje pelo sistema. Se não conseguir, pergunte a data para a pessoa.
A semana no nome do arquivo é sempre a semana em que vocês escreveram. Se o conteúdo é
para uma data lá na frente (Dia das Mães, Black Friday, uma inauguração), escreva no
topo do arquivo **para quando ele é**, em uma linha: é assim que ela reencontra o texto
quando a data chegar.

O arquivo tem, nesta ordem: o assunto, o insumo que ela deu (do jeito que ela mandou),
os canais escolhidos e os três rascunhos aprovados, cada um marcado com o canal a que
se destina.

Se já existir arquivo dessa semana com o mesmo assunto, acrescente ao que está lá. Não
apague o que já foi escrito.

## Fechamento

1. Mostre o caminho do arquivo e liste o que foi gravado.
2. Feche lembrando, sem drama: dá uma lida antes de publicar. Toda IA erra, inclusive a
   melhor. O que vai para o público leva o seu nome, então a conferência é parte do
   trabalho.
3. Se o resultado tiver saído genérico e o insumo tiver sido só o tema, diga isso na
   cara e ofereça refazer com 3 tópicos dela.
