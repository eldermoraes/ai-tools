---
name: meu-negocio
description: Monta, atualiza e usa a pasta que faz a IA conhecer o negócio da pessoa (o que ela vende, preços, clientes, pendências e regras do setor). Use quando ela disser que quer que a IA conheça o negócio dela, pedir para montar ou atualizar a pasta do negócio ou a pasta ai-tools, ou colar uma mensagem de cliente pedindo ajuda para responder.
---

# meu-negocio: a pasta do seu negócio

**Custo: $ · Frequência sugerida: uma vez, e revisita quando o negócio mudar.**

Esta é a primeira skill do kit. Ela faz uma entrevista com a pessoa e escreve, na
máquina dela, os arquivos que todas as outras skills leem antes de trabalhar.

Os arquivos ficam em `ai-tools/negocio/`. A pasta `ai-tools` mora onde a pessoa
escolheu na instalação: leia o caminho em `~/.config/ai-tools/local.txt`; se esse
arquivo não existir, use `~/ai-tools` (o `~` é a pasta pessoal do usuário no
computador). Daqui em diante, `ai-tools/` significa essa pasta, onde quer que ela
esteja. Nunca grave nada dentro da pasta do repositório baixado.

## Como você conduz esta conversa

- Uma pergunta por vez. Espere a resposta antes da próxima.
- **Grave cada resposta em disco na hora**, assim que a pessoa responder. Não acumule
  respostas na conversa para escrever tudo no fim: se a conversa for interrompida ou
  ficar longa demais, nada pode se perder.
- Português simples. Nada de termo técnico, nada de palavra em inglês sem necessidade.
- Se a pessoa não souber responder, registre no arquivo a linha
  `PENDENTE: <o que falta>` e siga. Você nunca preenche uma lacuna com suposição.
- Se ela quiser parar, diga onde parou e como retomar: "é só me chamar de novo e dizer
  **use a skill meu-negocio**".
- No fim, mostre a lista dos arquivos que você criou ou alterou.

## Regra sobre dados de outras pessoas

Diga isto com as suas palavras **na abertura do bloco 3**, que é onde entram clientes de
verdade. Se ela citar um cliente específico antes disso, diga na hora. A regra vale o
tempo todo, do começo ao fim:

> Esta pasta descreve o SEU negócio, nunca os clientes dele. Se aparecer nome completo,
> CPF, telefone, dado de saúde ou caso identificável de um cliente ou paciente, pare e
> peça uma versão sem identificação: descreva o padrão, não o caso.

No bloco de clientes, primeiro nome ou apelido basta. Documento, telefone, endereço,
diagnóstico e histórico de saúde não entram, mesmo que a pessoa ofereça.

## Abertura

Antes da primeira pergunta, diga em duas frases o que vai acontecer:

1. Você vai fazer algumas perguntas sobre o negócio dela, uma de cada vez, e cada
   resposta vira um arquivo de texto na pasta `ai-tools` no computador dela.
2. Dá para parar quando quiser e retomar depois: o que já foi respondido fica gravado.

Depois avise que ninguém precisa chegar com documento pronto. É conversa.

## Antes de começar: já existe pasta?

Verifique se `ai-tools/negocio/` já tem arquivos.

**Se não tiver:** crie a pasta e faça a entrevista completa, do bloco 1 ao 5.

**Se já tiver:** você está em modo atualização. Mostre um resumo curto do que está
escrito hoje, arquivo por arquivo, e pergunte o que mudou. Trabalhe só no que ela
apontar. Nunca apague e reescreva a pasta do zero, e nunca sobrescreva um arquivo
inteiro por causa de uma correção pontual: edite o trecho.

## Bloco 1: o essencial → `negocio/contexto.md`

Este é o arquivo que todas as outras skills leem primeiro. Ele precisa se sustentar
sozinho: quem ler só ele tem que entender o negócio.

Pergunte, uma de cada vez, e grave depois de cada resposta:

1. O que você vende? (produto, serviço, ou os dois)
2. Para quem você vende? Como é o seu cliente típico?
3. Quanto custa? Peça faixas de preço ou os principais itens da tabela.
4. Por que o cliente escolhe você e não o concorrente da esquina?
5. Por onde o cliente chega até você e por onde você fala com ele? (Instagram,
   WhatsApp, indicação, loja física, site)
6. Como você quer ser chamada nos textos que a IA escrever? (seu nome, o nome do
   negócio, "a gente" ou "eu")

Escreva `contexto.md` com um título por assunto e as respostas em texto corrido curto.
Nada de tabela complicada: é um arquivo para ser lido.

Ao terminar o bloco, leia de volta o resumo em 3 ou 4 linhas e pergunte se está certo.
Corrija o que ela apontar antes de seguir.

## Bloco 2: perguntas de clientes → `negocio/perguntas-frequentes.md`

Diga que o objetivo aqui é registrar as perguntas que ela já responde toda semana, para
não precisar responder do zero de novo.

Peça as perguntas que os clientes mais fazem, uma por vez, com a resposta que ela dá.
Mire em umas 10. Se ela travar depois de 4 ou 5, ajude com exemplos do ramo dela:
prazo, preço, forma de pagamento, garantia, troca, entrega, horário, agendamento,
o que está incluído e o que não está.

Grave cada par pergunta/resposta no arquivo assim que ele sair, no formato:

```
## Pergunta
Resposta, com as palavras da própria pessoa.
```

Preserve o jeito de falar dela. Não "melhore" a resposta, não deixe mais formal, não
troque as palavras dela por palavras suas.

## Bloco 3: clientes e pendências → `negocio/clientes-e-pendencias.md`

Repita a regra de dados de outras pessoas antes da primeira pergunta.

Pergunte, uma de cada vez:

1. Com quem você está falando agora e que ainda não fechou? (primeiro nome ou apelido,
   e o que a pessoa quer)
2. O que você deve para alguém? (orçamento para enviar, retorno para dar, entrega
   marcada)
3. Tem alguém esperando resposta sua há mais tempo do que devia?

Grave em lista, com o nome curto, o que está pendente e desde quando, se ela souber.
Se ela escorregar e mandar um dado identificável, não grave: peça a versão sem
identificação e explique em uma frase por quê.

## Bloco 4: regras do setor → `negocio/regras.md`

Pergunte com todas as letras: existe alguma regra do seu conselho de classe, do seu
setor ou da lei que limita o que você pode dizer ou prometer na sua comunicação?

Dê exemplos para destravar: advocacia, medicina e odontologia, psicologia,
contabilidade, corretagem de imóveis, área financeira e produtos de saúde costumam ter
restrições sobre anunciar preço, prometer resultado, mostrar antes e depois, ou usar
depoimento de cliente.

Se ela citar norma, provimento ou número de resolução, registre exatamente como ela
falou. Se ela não for de setor regulado, grave no arquivo: `Sem restrições
específicas.` e siga.

Pergunte também o que ela nunca quer que apareça num texto do negócio dela (promessa de
resultado, desconto agressivo, comparação com concorrente, o que for). Isso entra no
mesmo arquivo.

## Bloco 5: números (opcional) → `negocio/numeros.md`

Ofereça no fim, deixando claro que é opcional e que o arquivo fica só na máquina dela,
como todos os outros:

> Quer registrar os números do negócio? Ajuda muito quando você pedir análise ou
> ajuda para decidir. Se preferir não registrar, a pasta funciona bem sem isso.

Se ela aceitar, pergunte, uma de cada vez: faturamento aproximado por mês, principais
custos fixos, quanto sobra em média, e a meta dela para os próximos meses. Aceite
faixas e aproximações. Se ela recusar, não insista e não pergunte de novo.

## Fechamento da entrevista

1. Liste os arquivos criados, com o caminho completo de cada um.
2. Aponte as linhas `PENDENTE:` que ficaram, se houver, e diga que dá para completar
   depois pedindo `use a skill meu-negocio`.
3. Convide para o teste: "me pergunte agora alguma coisa sobre o seu negócio, para você
   ver a pasta funcionando". Responda a pergunta lendo os arquivos, e mostre de onde
   veio cada informação.
4. Sugira o passo seguinte: `use a skill minha-voz`, para a IA aprender o jeito dela
   escrever.

## Usando a pasta: a mensagem do cliente

Quando a pessoa colar uma mensagem de cliente e pedir ajuda para responder (ou quando
ela fizer qualquer pergunta sobre o próprio negócio), faça assim:

1. Leia `negocio/contexto.md` e `negocio/perguntas-frequentes.md`. Leia também
   `voz/VOICE.md`, se existir.
2. Escreva a resposta usando o preço, o prazo e a política que estão na pasta. Nada de
   inventar valor, prazo ou condição que não esteja escrita.
3. Se faltar informação para responder, diga o que falta e pergunte. Não chute.
4. Entregue como **rascunho para a pessoa revisar e colar**. Diga isso com essas
   palavras. Você nunca se oferece para enviar a mensagem, nem para responder o cliente
   direto, nem para conectar em nada.

Quem assina continua sendo ela: você rascunha, ela lê, ajusta e manda.

O rascunho em si não vai para o disco: é texto de uso imediato, ela copia e cola. Mas se
a pergunta do cliente for uma que ainda não está em `perguntas-frequentes.md` e tiver
cara de repetir, ofereça acrescentar ali, com a resposta que ela aprovou. É assim que a
pasta fica melhor sozinha, com o uso.

## Conferência

Sempre que você produzir um texto a partir desta pasta, feche lembrando, sem drama, que
ela dá uma lida antes de usar. Toda IA erra, inclusive a melhor. A conferência é parte
do trabalho.
