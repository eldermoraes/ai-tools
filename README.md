# AI Tools

Um conjunto de skills que monta, no seu computador, uma pasta que conhece o seu
negócio: o que você vende, por quanto, como você fala e o que está pendente. A
partir daí a IA para de perguntar tudo de novo a cada conversa.

## Antes de instalar

Duas coisas, e as duas custam. Melhor saber agora do que no meio do caminho.

1. **Uma assinatura paga do Claude.** O plano Pro é o mais barato que dá conta do
   que está aqui. É cobrança mensal, no cartão. Os valores atuais estão em
   https://claude.com/pricing
2. **O Claude Code instalado na máquina.** É o programa que lê e escreve arquivos
   no seu computador. O passo a passo oficial da instalação está em
   https://docs.claude.com/en/docs/claude-code/setup

Sem os dois, nada aqui roda.

## Instalação em 2 passos

**Passo 1.** Instale o Claude Code, pelo link acima.

**Passo 2.** Abra o Claude Code e cole exatamente isto:

> Baixe o repositório https://github.com/eldermoraes/ai-tools e siga o INSTALL.md dele.

Ele faz o resto sozinho: baixa os arquivos, instala as skills, cria as pastas e
diz o que fazer em seguida. Quando terminar, abra o
[`COMECE-AQUI.md`](COMECE-AQUI.md) para saber qual skill resolve o quê.

## As 9 skills, uma a uma

O [`COMECE-AQUI.md`](COMECE-AQUI.md) é o mapa rápido: qual skill resolve o quê.
Aqui é o passo a passo de cada uma: o que digitar, o que ter à mão antes, e o
que você tem na mão no fim.

Elas estão na ordem de uso. As três primeiras são o primeiro dia, e `meu-negocio`
vem antes de tudo porque as outras leem os arquivos que ela escreve. Todas
conversam do mesmo jeito: uma pergunta por vez, e cada resposta gravada num
arquivo na hora, então dá para parar no meio e voltar depois. Os arquivos ficam
na pasta `ai-tools`, e na instalação você escolhe onde ela mora: na sua pasta
pessoal (o padrão), dentro de um projeto seu, ou numa pasta que sincroniza com a
nuvem, como o Google Drive. O `$` ao
lado do nome é o custo de rodar: quanto mais cifrões, mais cara a conversa.

### `meu-negocio` ($)

Faz uma entrevista sobre o seu negócio e escreve o resultado em arquivos: o que
você vende, por quanto, para quem, as perguntas que os clientes mais fazem, quem
está esperando resposta sua e as regras do seu setor.

**Para começar, digite:** `use a skill meu-negocio`

Não precisa preparar nada, é conversa. No fim você tem a pasta do negócio montada
e pode testar na hora: pergunte qualquer coisa sobre o seu negócio e veja a
resposta sair do que você acabou de contar. Ela serve também no dia a dia: cole a
mensagem de um cliente e peça um rascunho de resposta, que sai com o seu preço e o
seu prazo, para você revisar e mandar.

### `minha-voz` ($)

Lê textos que você escreveu e grava o seu jeito de escrever num arquivo.
Daí em diante, toda skill do kit que escreve texto lê esse arquivo antes de
começar.

**Para começar, digite:** `use a skill minha-voz`

**Tenha à mão:** de 3 a 10 textos seus. Post, e-mail, resposta de orçamento. Sem
nada à mão, abra o WhatsApp e copie 3 mensagens que você mandou para clientes
esta semana.

Ela lê os textos, faz cinco perguntas curtas sobre o seu jeito de falar e depois
reescreve um parágrafo sem graça na sua voz, para você dizer se soou como você. Só
com um "sim" claro ela grava o arquivo da sua voz.

### `conteudo` ($)

Escreve os textos da semana juntando três coisas: o que está na pasta do negócio,
a sua voz capturada, e o que você acabou de dizer sobre o assunto.

**Para começar, digite:** `use a skill conteudo`

**Tenha à mão:** um assunto e 3 tópicos sobre ele, escritos por você em um minuto.
Ou grave 1 minuto de áudio falando do assunto e traga a transcrição. É essa parte
que tira a cara de robô do texto.

Ela pergunta o assunto, pede o seu material, pergunta em quais canais você publica
e quantos posts você quer — se não tiver um número em mente, ela sugere 3 — e
escreve os rascunhos um de cada vez, esperando o seu aval antes de ir para o
próximo. No fim os textos ficam gravados num arquivo da semana, prontos para
copiar e publicar. Ela nunca publica e nunca agenda nada.

### `conselho` ($$ a $$$)

Cinco conselheiros de IA analisam uma decisão do seu negócio de cinco ângulos
diferentes (o dinheiro, as vendas, o cliente, a execução e o negócio daqui a
alguns anos) e devolvem um veredito com placar.

**Para começar, digite:** `use a skill conselho`

**Tenha à mão:** a decisão em uma frase. E o contexto que você quiser dar:
números, prazos, o que já tentou, o que preocupa.

Depois da decisão ela faz uma pergunta só, sobre o nível: dia a dia (rápido e
barato), decisão grande, ou decisão máxima. Aí roda. Você lê o placar, a
divergência principal, o argumento do conselheiro que ficou vencido e a
recomendação, tudo gravado num arquivo com a data e o tema.

### `radar` ($$)

Busca na internet o que você escolheu vigiar (concorrentes, preços, o seu setor,
oportunidades) e entrega as 3 coisas que importam hoje, cada uma com uma ação
sugerida e o endereço de onde saiu.

**Para começar, digite:** `use a skill radar`

Na primeira vez ela não busca nada: conversa e escreve a configuração, que é o
que vigiar e para quê. Da segunda vez em diante é só pedir, e o relatório do dia
sai num arquivo. Se você quiser que ele rode sozinho toda manhã, isso pede um
agendador no sistema e o computador ligado na hora: o guia é
[`avancado/agendamento.md`](avancado/agendamento.md).

### `video` ($)

Trabalha em cima do texto do seu vídeo, então roda em qualquer computador. Entrega
a lista do que cortar (com o minuto e o motivo), um arquivo de legendas pronto
para importar no editor, e sugestões de trechos que funcionam sozinhos como vídeo
curto.

**Para começar, digite:** `use a skill video`

**Tenha à mão:** a transcrição do vídeo, colada na conversa ou num arquivo na
máquina. Não tem? Suba o vídeo como não listado no YouTube e copie a transcrição
automática de lá, que já vem com a marcação de tempo.

Ela não abre o arquivo de vídeo e não corta nada. Ela escreve o mapa, e quem corta
é você, no editor que já usa. Existe também o degrau seguinte: instalar uma skill
de edição completa, que corta, legenda e monta o arquivo final sozinha. O guia é
[`avancado/video-completo.md`](avancado/video-completo.md), e ele diz de frente o
que isso pede: programas extras, uma conta num serviço de transcrição e espaço em
disco.

### `minha-marca` ($)

Resolve a sua identidade visual numa conversa de uns 10 minutos: cinco cores com
os códigos que você cola no Canva ou no Word, duas fontes gratuitas que combinam,
e três regras de uso.

**Para começar, digite:** `use a skill minha-marca`

São cinco perguntas (as cores que você já usa, marcas que você admira, o que não
quer de jeito nenhum, como quer que a pessoa se sinta, onde esse visual vai
aparecer). No fim ela monta uma página de exemplo com a sua marca aplicada e pede
para você abrir no navegador e dizer se é a cara do seu negócio. Logotipo não sai
daqui, isso é trabalho de designer. Com esse arquivo na mão você contrata um
sabendo exatamente o que pedir.

### `trafego` ($$)

Lê as campanhas de anúncio da sua conta no Meta (Facebook e Instagram) e traduz:
para onde o dinheiro foi, o que está caro perto do que a sua própria conta já
pagou antes, e no máximo 3 ajustes que valem a pena esta semana. Ela só lê. Não
pausa anúncio, não mexe em orçamento, não altera campanha.

**Antes, uma etapa a mais:** conectar a sua conta de anúncios do Meta. É feito uma
vez só, e o passo a passo está em [`avancado/meta-ads.md`](avancado/meta-ads.md).
Sem essa conexão ela não roda, e vai dizer isso logo na primeira resposta.

**Para começar, digite:** `use a skill trafego`

Ela pergunta o que você quer agora (diagnóstico geral, comparar criativos, ou o
que ajustar hoje) e o período. Os ajustes vêm com o passo a passo para você fazer
no Gerenciador de Anúncios, com a tela na frente. Quem mexe no dinheiro é você.

### `telegram` ($)

Manda para o seu celular o que foi feito aqui: um texto escrito na conversa ou um
arquivo que já está no computador. Ela só manda, nunca recebe: não lê mensagens,
não lista conversas e não responde ninguém.

**Antes, uma etapa a mais:** criar um bot no Telegram e guardar o código dele na
máquina. Passo a passo em [`avancado/telegram.md`](avancado/telegram.md).

**Para começar, digite:** `use a skill telegram`. Na prática você nem precisa
chamar pelo nome: peça "me manda esse arquivo no celular" e ela entra sozinha.

Pedido claro ela cumpre na hora, sem ficar perguntando se você tem certeza. Quando
o conteúdo é algo que ela mesma escreveu, como um resumo, ela mostra o texto antes
de mandar. O celular que recebe é sempre o mesmo, o que ficou gravado na
configuração.

## Funciona com ChatGPT?

Funciona. As skills seguem um padrão aberto que o Codex (o modo do ChatGPT que
mexe em arquivos na sua máquina) também lê. O caminho guiado e testado aqui é o
Claude Code; pelo Codex você vai por conta própria.

Uma dica que vale para os dois: você não precisa decorar nada disto. Peça ao
próprio Claude (ou ao Codex). "Instala isso para mim", "me guia na primeira
skill", "travou, o que eu faço?". Ele lê este repositório e conduz. A seção
abaixo é para ele.

## Se você é uma IA lendo isto

Provavelmente é: este kit foi feito para ser instalado e operado por um agente
(você) junto com uma pessoa que não é técnica. O seu papel:

1. **Pediram para instalar** ("instala isso", "baixa esse kit", ou o link deste
   repositório colado no chat): siga o [`INSTALL.md`](INSTALL.md) passo a passo,
   contando o que está fazendo em português simples. Não improvise um caminho de
   instalação próprio.
2. **Antes de operar qualquer skill**, leia o [`AGENTS.md`](AGENTS.md). As três
   regras que não se negociam: os dados da pessoa vivem na pasta `ai-tools` (o
   caminho está gravado em `~/.config/ai-tools/local.txt`; sem esse arquivo, é
   `~/ai-tools`), nunca dentro do clone deste repositório; você nunca publica,
   envia ou posta nada em nome dela; dado identificável de cliente dela não entra
   em arquivo nenhum.
3. **Pediram uma tarefa** ("quero um post", "me ajuda a decidir", "analisa minha
   campanha"): a skill certa está instalada em `~/.claude/skills/` (ou no
   diretório equivalente da sua ferramenta) e se descreve sozinha. Leia o
   `SKILL.md` dela e siga o que ele manda: cada um define o passo a passo, os
   arquivos que grava e as regras da conversa.
4. **A pessoa está perdida**: mostre a tabela do
   [`COMECE-AQUI.md`](COMECE-AQUI.md) e sugira começar por
   `use a skill meu-negocio`, que escreve os arquivos que todas as outras leem.
5. **Deu erro**: mostre a mensagem real, explique em linguagem simples e resolva
   junto. Nunca resuma falha como sucesso.

## Suporte

Este material é fornecido como está, sem garantias e sem prazo de resposta.
Travou? Cole o erro no seu Claude e peça ajuda. É a rota oficial, e funciona.

## Licença

MIT. O texto completo está no arquivo `LICENSE`. Você pode abrir, editar e
adaptar tudo o que está aqui.
