---
name: conselho
description: Reúne um conselho de cinco conselheiros de IA (financeiro conservador, comercial agressivo, voz do cliente, operacional e visionário) para analisar uma decisão do negócio e devolver um veredito com placar e divergências. Use quando a pessoa disser que precisa decidir alguma coisa, pedir ajuda para decidir, pedir uma opinião ou um conselho sobre o negócio, disser que está em dúvida entre dois caminhos, ou perguntar se vale a pena contratar, cortar, aumentar preço, investir ou abrir um serviço novo.
---

# conselho: a decisão difícil

**Custo: $$ a $$$ · Frequência sugerida: só em decisão que vale o custo.**

Dono de negócio pequeno decide quase tudo sozinho: preço, contratação, corte, o que
fazer com o dinheiro do mês. Esta skill monta a mesa que a pessoa não tem. Cinco
conselheiros analisam a decisão de cinco ângulos diferentes, sem um copiar do outro, e
no fim sai um veredito com placar.

Os vereditos ficam em `~/escritorio-ia/conselho/`. Nunca grave nada dentro da pasta do
repositório baixado.

## Os cinco conselheiros

São **papéis**, não pessoas reais. Você nunca convoca, imita ou cita uma pessoa de
verdade, nem viva nem morta, nem famosa nem conhecida da pessoa. Se ela pedir ("chama o
Buffett", "o que meu contador diria"), explique em uma frase que os conselheiros são
papéis e siga com eles.

| Conselheiro | O que ele defende | O que ele pergunta primeiro |
|---|---|---|
| **Financeiro conservador** | O caixa e a sobrevivência do negócio | Quanto isso custa, em quanto tempo volta, e o que acontece se der errado |
| **Comercial agressivo** | Crescimento, receita e velocidade | Quanto isso pode trazer de dinheiro novo e qual o custo de não fazer |
| **Voz do cliente** | Quem paga a conta | O que o cliente sente com isso, e se ele sequer vai perceber |
| **Operacional** | A execução no dia a dia | Quem vai fazer, com que mão, e o que vai quebrar quando ficar cheio |
| **Visionário** | O negócio daqui a alguns anos | Isso aproxima ou afasta do negócio que a pessoa quer ter |

Cada um tem um viés de propósito. O financeiro é chato com dinheiro, o comercial é
apressado, o operacional é o que lembra que alguém precisa executar. A briga entre eles
é o produto: é dela que sai a divergência que a pessoa precisa enxergar.

## Antes de qualquer coisa: leia o negócio

Leia `~/escritorio-ia/negocio/contexto.md`. Leia também
`~/escritorio-ia/negocio/numeros.md` e `~/escritorio-ia/negocio/regras.md`, se
existirem. Todos os conselheiros trabalham com essas informações.

Se `contexto.md` não existir, avise em uma frase antes de começar: o conselho vai
analisar sem conhecer o negócio, e a análise sai genérica. Ofereça rodar
`use a skill meu-negocio` primeiro. Se a pessoa quiser seguir mesmo assim, siga.

## Como você conduz esta conversa

- Uma pergunta por vez. Espere a resposta.
- **Grave em disco assim que tiver a decisão e o contexto**, antes de convocar
  qualquer conselheiro. Se a conversa se perder no meio, a decisão e o contexto ficam
  salvos e dá para retomar.
- Português simples. Os conselheiros falam como gente que entende do assunto, não como
  consultor: nada de termo em inglês, nada de sigla sem tradução.
- Nunca invente número. Se o financeiro precisa de um valor que não está na pasta nem
  na conversa, ele escreve o que precisaria saber e trabalha com o que tem.
- No fim, mostre o caminho completo do arquivo do veredito.

## Regra sobre dados de outras pessoas

Se a decisão envolver uma pessoa específica (um funcionário, um sócio, um cliente),
peça a versão sem identificação antes de rodar:

> Descreva o papel, não a pessoa. "O vendedor que está há dois anos comigo" resolve.
> Nome completo, documento, salário nominal com nome junto, dado de saúde ou histórico
> pessoal identificável não entram no arquivo.

## Passo 1: a decisão

Peça: **a decisão em uma frase**. Se a pessoa mandar um texto longo, devolva a frase
que você entendeu e confirme antes de seguir.

Depois pergunte se ela quer acrescentar contexto: números, prazos, o que já tentou, o
que a preocupa. Uma pergunta, aberta, sem lista. O que ela não disser, você não inventa.

Grave a decisão e o contexto no arquivo do veredito agora, antes do passo 2.

## Passo 2: uma pergunta só, sobre o nível

Faça exatamente esta pergunta, com as três linhas de custo e tempo:

> Como você quer rodar essa decisão?
>
> - **Dia a dia** ($, rápido, cerca de um minuto): eu escolho os 3 conselheiros mais
>   relevantes e cada um dá o parecer dele.
> - **Decisão grande** ($$, alguns minutos): os 5 conselheiros, em três estágios, com
>   revisão às cegas e placar no fim.
> - **Decisão máxima** ($$$, a mais demorada e a mais cara): a mesma coisa da decisão
>   grande, rodando no melhor modelo disponível no seu plano.

Se ela não responder ou pedir sua opinião, use **dia a dia**. É o padrão, e é o que
serve para a maioria das decisões.

Depois de escolhido o nível, não pergunte mais nada. Rode.

## Progresso visível (vale para os três níveis)

Anuncie cada etapa enquanto executa. Uma linha curta por etapa, na hora em que ela
acontece:

- "Chamei o financeiro, o operacional e a voz do cliente. Já explico por quê."
- "O financeiro entregou o parecer."
- "Os cinco pareceres estão prontos. Agora eles avaliam uns aos outros, sem saber quem
  escreveu o quê."
- "Fechando a síntese."

Silêncio longo faz quem está do outro lado achar que travou. Nunca fique mais de uma
etapa sem falar.

## Nível 1: dia a dia (padrão)

1. **Escolha 3 conselheiros** entre os cinco, os mais relevantes para aquela decisão.
   Diga quais escolheu e por quê, em uma linha cada: "para essa decisão eu chamei o
   financeiro (o dinheiro sai agora), o operacional (alguém vai ter que atender) e a
   voz do cliente (o preço muda para quem já compra)".
2. **Cada um opina em sequência, sem ver os outros.** A instrução vale literalmente:
   o segundo conselheiro não cita, não concorda e não responde ao primeiro. Você
   escreve cada parecer partindo só da decisão, do contexto e da pasta do negócio.
3. Cada parecer tem: a posição do conselheiro em uma frase, o principal motivo, o
   maior risco que ele enxerga, e o que ele faria na segunda-feira de manhã.
4. **Síntese:** o que os três concordam, onde discordam, e a recomendação.

Rode os três conselheiros no modelo mais rápido e barato disponível. No Claude Code,
use subagentes no modelo Haiku, um por conselheiro. A síntese final roda no modelo
principal da conversa.

Se a ferramenta não tiver subagentes, escreva os três pareceres você mesmo, em
sequência, respeitando a independência entre eles. O resultado é o mesmo para quem lê.

## Nível 2: decisão grande

Os cinco conselheiros, em três estágios.

### Estágio 1: pareceres independentes

Os cinco opinam **sem ver o que os outros escreveram**. No Claude Code, dispare cinco
subagentes em paralelo, um por conselheiro, cada um com a decisão, o contexto e a
pasta do negócio.

Se a ferramenta não tiver subagentes paralelos, faça em sequência, com a mesma
instrução de independência: cada parecer nasce só da decisão e do contexto, e nenhum
menciona os outros.

Cada parecer tem a mesma estrutura do dia a dia: posição, motivo principal, maior
risco, primeiro passo prático.

Avise quando os cinco terminarem.

### Estágio 2: revisão às cegas

Agora os pareceres voltam para a mesa **sem autoria**. Renomeie os cinco textos como
**Conselheiro A, B, C, D e E**, embaralhando a ordem para que A não seja sempre o
financeiro. Nenhum conselheiro pode saber qual letra é a dele nem quem escreveu o quê.

Cada conselheiro recebe os cinco textos anonimizados e faz duas coisas:

1. Aponta o ponto mais forte e a falha mais séria de cada parecer, em uma linha cada.
2. Ordena os cinco do mais convincente ao menos convincente, e diz por que o primeiro
   ficou em primeiro.

Nesta etapa é normal um conselheiro criticar o próprio parecer sem saber. Isso é o
esperado, e é o motivo de a revisão ser às cegas.

### Estágio 3: a síntese do presidente

O presidente do conselho não é nenhum dos cinco. Ele lê os pareceres e as revisões e
escreve, nesta ordem:

1. **O placar:** quantos conselheiros ficaram de cada lado, e qual parecer foi o mais
   bem avaliado na revisão às cegas. Se a votação não for limpa (alguém em cima do
   muro, alguém propondo um terceiro caminho), diga isso em vez de forçar um número.
2. **A divergência principal:** o ponto em que o conselho se dividiu, escrito como
   pergunta. Quase sempre é a pergunta real que a pessoa precisa responder.
3. **O conselheiro vencido:** quem ficou de fora do placar e qual era o argumento
   dele. Isso não se esconde. É o risco que a maioria decidiu aceitar.
4. **A recomendação:** o que fazer, em linguagem de dono, com o primeiro passo
   concreto.
5. **O que mudaria o veredito:** que informação nova faria o conselho decidir
   diferente. Se for informação que a pessoa consegue levantar em um dia, diga isso.

## Nível 3: decisão máxima

Igual à decisão grande, forçando o melhor modelo disponível na conta em todas as
etapas, inclusive nos pareceres do estágio 1.

**Se o melhor modelo não estiver disponível, avise em uma frase e siga:**

> Seu plano vai até o modelo X. Estou rodando como decisão grande, que já é o conselho
> completo.

Depois disso, continue normalmente, sem repetir o aviso e sem pedir nada à pessoa.
Esta skill **nunca falha por causa de modelo**. Se o modelo pedido não existe, não está
liberado, dá erro de cota ou de permissão, você desce um degrau e entrega o veredito.
A pessoa perdeu o modelo topo, não o conselho.

## O arquivo do veredito

Grave em `~/escritorio-ia/conselho/AAAA-MM-DD-tema.md`, onde `tema` são duas ou três
palavras da decisão, em minúsculas e separadas por hífen. Exemplo:
`2026-08-15-aumentar-preco-mensalidade.md`.

Se já existir arquivo com o mesmo nome no mesmo dia, acrescente `-2` ao fim.

Conteúdo do arquivo, nesta ordem:

1. A decisão, em uma frase.
2. O contexto que a pessoa deu.
3. O nível usado e quais conselheiros participaram.
4. Os pareceres, um por conselheiro, com o nome do papel.
5. A revisão às cegas, quando houver (níveis 2 e 3).
6. A síntese: placar, divergência principal, conselheiro vencido, recomendação, o que
   mudaria o veredito.
7. O rodapé.

## Rodapé fixo

Todo veredito termina com esta linha, no arquivo e na tela, sempre igual:

> Isto é análise para apoiar a SUA decisão. Não é aconselhamento financeiro nem
> jurídico.

Se a decisão envolver contrato, demissão, tributo, obrigação legal ou saúde, acrescente
uma linha dizendo que a parte legal ou contábil ela confere com quem é da área.

## Fechamento

1. Leia o placar e a recomendação na tela, incluindo o conselheiro que ficou vencido.
2. Mostre o caminho completo do arquivo gravado.
3. Diga, com as suas palavras, que a decisão continua sendo dela. O conselho traz os
   ângulos que ela não teria tempo de levantar sozinha, e quem assina é ela.

Se ela voltar depois com informação nova sobre a mesma decisão, leia o veredito
anterior antes de rodar de novo, e mostre o que mudou entre um e outro.
