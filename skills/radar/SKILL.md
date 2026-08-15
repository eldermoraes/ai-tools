---
name: radar
description: Monta e roda o relatório diário do negócio: busca na internet o que a pessoa escolheu vigiar (concorrentes, preços, o setor dela, oportunidades) e entrega as 3 coisas que importam hoje, cada uma com uma ação sugerida. Use quando ela pedir o radar, o relatório da manhã, um resumo do dia, notícias do setor dela, ou disser que quer saber o que os concorrentes andam fazendo.
---

# radar: o relatório da manhã

**Custo: $$ · Frequência sugerida: toda manhã, quando você pedir.**

Esta skill faz duas coisas diferentes, dependendo de quando é chamada.

**Na primeira vez** ela não busca nada: ela conversa e escreve a configuração, ou seja,
o que vigiar e para quê. **Nas vezes seguintes** ela busca, cruza com a pasta do
negócio e entrega as 3 coisas que importam hoje.

Tudo fica em `~/escritorio-ia/radar/`. Nunca grave nada dentro da pasta do repositório
baixado.

## Como você conduz esta conversa

- Uma pergunta por vez. Espere a resposta.
- **Grave cada resposta em disco na hora.** Não junte as respostas para escrever a
  configuração no fim: se a conversa cair, nada pode se perder.
- Português simples, sem termo técnico e sem palavra em inglês desnecessária.
- Você não inventa notícia. Se a busca não trouxer nada relevante, o relatório diz que
  não trouxe. Isso é resposta legítima.
- No fim, mostre o caminho completo dos arquivos criados ou alterados.

## O que fazer primeiro: descobrir em que ponto você está

Verifique, nesta ordem:

1. Existe `~/escritorio-ia/radar/config.md`? Se sim, **pule para "Rodar o radar"**.
2. Existe `~/escritorio-ia/_kit/modelos/radar.md` **preenchido pela pessoa**? Se sim,
   **importe** (próxima seção).
3. Nada disso? Faça a configuração conversando.

**Como saber se o modelo foi preenchido:** o arquivo `_kit/modelos/radar.md` vem com os
campos em branco (linhas que começam com `-` e não têm nada depois) e com exemplos em
itálico, que já vieram prontos. Se os campos continuam em branco, ou só têm o que já
veio no modelo, ele **não** foi preenchido. Trate como se não existisse e siga para a
configuração conversando.

## Importar o modelo preenchido

Muita gente preenche esse modelo à mão antes de rodar o radar pela primeira vez. Quando
ele estiver preenchido:

1. Leia o arquivo e transforme o que está lá em `~/escritorio-ia/radar/config.md`,
   organizado nas seções da próxima seção. Grave. O modelo tem um bloco final,
   **"Como eu quero receber"**, com três tamanhos de relatório (bem curto, médio,
   completo): se ela marcou um, registre na configuração e respeite na hora de
   escrever. Se não marcou nada, use o médio.
2. Mostre para a pessoa, em 4 ou 5 linhas, o que você entendeu que ela quer vigiar.
3. Pergunte só o que ficou faltando ou ambíguo. Uma pergunta por vez, e no máximo três.
   Se estiver tudo claro, não pergunte nada.
4. Diga que a configuração está pronta e rode o primeiro relatório na hora.

Nunca peça para ela repetir na conversa o que já escreveu no modelo.

## Configuração (primeira execução, sem modelo preenchido)

Explique em duas frases o que vai acontecer: você vai fazer algumas perguntas sobre o
que ela quer acompanhar, isso vira um arquivo no computador dela, e a partir daí é só
pedir o radar que o relatório sai.

Leia `~/escritorio-ia/negocio/contexto.md` antes de perguntar. Com ele em mãos, você
consegue sugerir o que vigiar em vez de perguntar no vácuo. Se ele não existir, diga em
uma frase que o radar fica mais afiado depois de rodar `use a skill meu-negocio`, e
siga assim mesmo.

Pergunte, uma de cada vez, gravando depois de cada resposta:

1. **Concorrentes.** Quem são os concorrentes que você quer acompanhar? Nome do negócio
   e, se ela tiver, o site ou o perfil.
2. **Preços.** Tem algum preço, custo ou matéria-prima que mexe com o seu bolso quando
   sobe ou desce?
3. **O setor.** Que assunto do seu ramo você não pode perder de vista? Regra nova,
   mudança de lei, tendência, moda que aparece e some.
4. **Oportunidades.** Que tipo de oportunidade valeria a pena aparecer na sua tela?
   Edital, licitação, evento, feira, parceria, cliente grande contratando.
5. **As 2 perguntas que importam.** Se o relatório de amanhã só pudesse responder duas
   perguntas suas, quais seriam? Insista para que saiam duas perguntas de verdade, com
   ponto de interrogação, não dois assuntos soltos.
6. **Fontes preferidas (opcional).** Você já acompanha algum site, portal, associação
   ou perfil? Se não tiver, tudo bem: a busca é aberta.

Se ela travar em alguma pergunta, ajude com exemplos do ramo dela. Se ainda assim não
souber, escreva `PENDENTE: <o que falta>` no arquivo e siga. Nunca preencha por ela.

Grave em `~/escritorio-ia/radar/config.md`, com uma seção por bloco acima e as
respostas com as palavras dela.

No fim da configuração, ofereça rodar o primeiro relatório agora. Se ela preferir rodar
amanhã de manhã, diga que basta pedir: **use a skill radar**.

## Regra sobre dados de outras pessoas

A configuração descreve o mercado, nunca os clientes dela. Concorrente é negócio, e
nome de negócio pode entrar. Cliente é pessoa, e não entra: nem nome, nem telefone, nem
o caso dele. Se ela quiser vigiar um cliente grande, registre o setor e o porte, não a
pessoa.

## Rodar o radar

Com `config.md` na mão:

1. **Leia** `config.md` e `~/escritorio-ia/negocio/contexto.md`.
2. **Avise que começou.** Uma linha, dizendo o que você vai procurar. Busca demora, e
   silêncio parece travamento.
3. **Busque na internet**, guiada pela configuração: os concorrentes, os preços, os
   assuntos do setor, as oportunidades. Priorize o que é recente, com data visível, e
   descarte o que não tem data.
4. **Cruze com o negócio.** A notícia só entra no relatório se você conseguir dizer o
   que ela muda para **este** negócio. Notícia interessante que não muda nada fica de
   fora.
5. **Escolha as 3 coisas que importam hoje.** Três, não cinco. O corte é o produto.
   Se o dia foi fraco e só houve duas, entregue duas e diga por quê. Se não houve nada,
   diga que não houve nada e cite o que você procurou.
6. **Grave e mostre.**

### O formato do relatório

Para cada uma das 3 coisas:

- **O que aconteceu:** duas ou três linhas, em português de dono, com a data.
- **Por que importa para você:** a ligação com o negócio dela, tirada de `contexto.md`.
  Se você não conseguir escrever esta linha com honestidade, o item não deveria estar
  no relatório.
- **A ação sugerida:** uma coisa concreta para hoje. "Subir o preço da linha X em 5%"
  vale; "ficar de olho no mercado" não vale.
- **Onde eu vi:** o endereço da fonte. Sempre. Sem fonte, o item não entra.

Depois dos três itens, responda as **2 perguntas que importam** da configuração, cada
uma em uma ou duas linhas, com o que a busca de hoje trouxe. Se a busca não respondeu,
escreva que hoje não respondeu. Isso é informação também.

Nada de opinião apresentada como fato. Se você está inferindo, escreva que está
inferindo.

### O arquivo do dia

Grave em `~/escritorio-ia/radar/AAAA-MM-DD.md`, um arquivo por dia.

**Se o arquivo de hoje já existir, atualize esse mesmo arquivo. Nunca crie um segundo
arquivo para o mesmo dia e nunca duplique o conteúdo.** Rodar duas vezes no mesmo dia é
normal: a pessoa rodou de manhã e voltou à tarde. Nesse caso:

- Mantenha o que continua valendo.
- Substitua o que mudou.
- Marque o que é novidade da segunda rodada, com o horário.
- Registre o horário de cada execução no topo do arquivo.

### A linha do fim

Todo relatório termina com estas duas frases, sempre:

> Quer receber isso no seu celular? Configure a skill `telegram` (guia em
> `~/escritorio-ia/_kit/avancado/telegram.md`). Quer que rode sozinho toda manhã? Guia
> em `~/escritorio-ia/_kit/avancado/agendamento.md` (exige a máquina ligada).

## Fechamento

1. Mostre as 3 coisas na tela, do jeito que ficaram no arquivo.
2. Mostre o caminho completo do arquivo do dia.
3. Feche lembrando, sem drama, que o que veio da internet ela confere antes de agir.
   Notícia sai errada, preço muda de novo, e a ação sugerida é sugestão. Quem decide
   é ela.

Se ela quiser mudar o que vigia, é só pedir: você abre `config.md`, mostra o que está
escrito, e edita só o trecho que ela apontar. Nunca reescreva a configuração inteira
por causa de um ajuste.
