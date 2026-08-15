---
name: minha-voz
description: Captura o jeito da pessoa escrever a partir de textos que ela já escreveu e grava um arquivo de voz que as outras skills usam para os textos não saírem com cara de robô. Use quando ela disser que quer a IA escrevendo no tom dela, reclamar que os textos saem com cara de IA, ou pedir para capturar, registrar ou ajustar a voz dela.
---

# minha-voz: a sua voz capturada

**Custo: $ · Frequência sugerida: uma vez.**

Pedir "escreve no meu tom" dentro de cada conversa não sustenta: no dia seguinte você
digita tudo de novo. Esta skill lê textos que a pessoa já escreveu, conversa um pouco
sobre o jeito dela falar e grava isso num arquivo. Depois disso, toda skill do kit que
escreve texto lê esse arquivo antes de começar.

O arquivo final fica em `~/escritorio-ia/voz/VOICE.md`. Nunca grave nada dentro da
pasta do repositório baixado.

## Como você conduz esta conversa

- Uma pergunta por vez.
- **Grave em disco na hora.** Cada texto colado e cada resposta da entrevista vão para
  `~/escritorio-ia/voz/anotacoes.md` assim que chegarem. O `VOICE.md` é escrito no fim,
  depois da aprovação, mas o material bruto não pode depender da conversa continuar
  aberta.
- Português simples, sem termo técnico.
- Não invente característica que você não viu nos textos. Se um traço aparece uma vez
  só, ou você confirma com a pessoa, ou deixa de fora.
- No fim, mostre a lista dos arquivos criados ou alterados.

## Antes de começar

Leia `~/escritorio-ia/negocio/contexto.md`, se existir, para saber do que a pessoa fala
no dia a dia. Se não existir, tudo bem: esta skill funciona sozinha. Só não invente o
ramo do negócio.

Se `~/escritorio-ia/voz/VOICE.md` já existir, mostre o que está escrito e pergunte se
ela quer ajustar alguma coisa ou refazer com textos novos. Trabalhe em cima do que
existe, não jogue fora.

## Regra sobre dados de outras pessoas

Os textos que ela vai colar podem ter conversa com cliente dentro. Diga, antes de pedir
os textos:

> Estamos capturando o SEU jeito de escrever, não os assuntos dos seus clientes. Se o
> texto tiver nome completo, telefone, valor de contrato, dado de saúde ou qualquer
> caso identificável de um cliente ou paciente, apague isso antes de colar. Para o que
> a gente precisa aqui, o assunto não importa: importa como você escreve.

Se algum dado desse tipo escapar para o texto colado, não grave o trecho: registre só o
padrão de escrita e avise a pessoa em uma frase.

## Passo 1: os textos

Peça de 3 a 10 textos que ela mesma escreveu. Post, e-mail, mensagem para cliente,
legenda, resposta de orçamento. Quanto mais recentes e mais parecidos com o que ela
quer escrever daqui pra frente, melhor.

Se ela disser que não tem nada à mão, use este caminho, com estas palavras:

> Não tem textos à mão? Abre o WhatsApp e copia 3 mensagens que você mandou para
> clientes esta semana. Todo mundo tem voz registrada no bolso.

Aceite os textos de uma vez ou aos poucos. A cada texto colado, grave em
`voz/anotacoes.md` e agradeça em uma linha, sem comentar o conteúdo.

Com menos de 3 textos, diga que dá para começar, mas que o arquivo vai ficar mais fraco,
e ofereça esperar mais um.

## Passo 2: a entrevista de tom

Cinco perguntas, uma de cada vez, gravando cada resposta:

1. Tem alguma coisa que você nunca diria num texto do seu negócio? (palavra, promessa,
   jeito de falar)
2. Você tem alguma gíria, expressão ou frase que repete bastante?
3. Você fala com o cliente de um jeito mais formal ou mais próximo? Chama de "você",
   "senhor", pelo nome?
4. Emoji: usa, não usa, ou usa pouco? Quais?
5. Como você costuma começar e como costuma terminar uma mensagem?

## Passo 3: o que você observou

Leia os textos com atenção e anote o que dá para ver, não o que dá para supor:

- tamanho das frases e dos parágrafos;
- palavras e expressões que se repetem;
- pontuação característica (usa reticências? exclamação? escreve tudo corrido?);
- como ela explica uma coisa difícil;
- como ela pede alguma coisa (pagamento, retorno, decisão);
- o que ela nunca faz (não usa exclamação, não usa emoji, não escreve parágrafo longo).

Cada característica precisa vir com um exemplo tirado dos textos dela. Sem exemplo, não
entra.

## Passo 4: a validação (não pule)

Aqui a pessoa vê a captura funcionando antes de gravar qualquer coisa.

Reescreva o parágrafo genérico abaixo na voz que você capturou. Mostre os dois lado a
lado: o genérico primeiro, a sua versão depois.

Parágrafo genérico (use exatamente este):

> Estamos muito felizes em anunciar que a nossa empresa segue buscando oferecer as
> melhores soluções para os nossos clientes. Com profissionalismo e dedicação,
> trabalhamos diariamente para superar expectativas e entregar excelência. Entre em
> contato conosco e descubra como podemos ajudar o seu negócio a crescer.

Depois pergunte, com estas palavras: **"Soa como você?"**

- Se ela aprovar, siga para o passo 5.
- Se ela disser que não, pergunte o que ficou estranho e onde. Ajuste, mostre de novo e
  pergunte de novo. Repita quantas vezes for preciso.
- Se ela aprovar "mais ou menos", trate como reprovação: pergunte o que falta.

**Grave cada rodada em `voz/anotacoes.md` na hora:** a versão que você mostrou e o que
ela respondeu. O que ela corrige aqui é a parte mais valiosa da conversa inteira ("ficou
formal demais", "eu nunca começaria assim"), e é isso que vira o `VOICE.md`. Se a
conversa cair no meio, essa rodada não pode se perder.

Só passe adiante com um "sim" claro.

## Passo 5: gravar o `VOICE.md`

Escreva `~/escritorio-ia/voz/VOICE.md` com estas partes, nesta ordem:

1. **Como eu escrevo**: as características observadas, cada uma com um exemplo curto
   tirado dos textos dela.
2. **Palavras e expressões que eu uso**: as recorrentes, mais as gírias e bordões que
   ela citou na entrevista.
3. **O que eu evito**: o que ela disse que nunca diria, mais o que ficou de fora nos
   textos dela.
4. **Formalidade, emojis, abertura e despedida**: as respostas da entrevista, em texto
   curto.
5. **Amostras**: 2 ou 3 trechos originais dela, colados inteiros, marcados como
   referência. É o que uma IA lê quando fica em dúvida.

Escreva o arquivo em primeira pessoa, como se fosse ela explicando o próprio jeito de
escrever. É dela.

## Fechamento

1. Mostre o caminho do arquivo criado.
2. Diga em uma frase o que muda daqui pra frente: toda skill do kit que escreve texto
   passa a ler este arquivo antes de começar.
3. Sugira o passo seguinte: `use a skill conteudo`, para escrever os posts da semana.
4. Lembre que o arquivo é texto: ela pode abrir, ler e editar quando quiser, e pode
   pedir para você ajustar sempre que um texto sair fora do tom.
