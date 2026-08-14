# Plano de implementação — AI Tools

Plano completo para construir este repositório. Escrito em 2026-08-14 para ser executado
por uma sessão futura do Claude Code ("goal"), sem depender de nenhuma conversa anterior.
Tudo que a execução precisa saber está neste arquivo. Ao final da execução, **apagar este
arquivo** — ele é andaime, não produto.

---

## 1. O que é este repositório

Kit entregue aos participantes do **Workshop de IA para Empreendedores** (Elder Moraes,
online, ~54 empreendedores não técnicos: joalheria, confeitaria, advocacia, contabilidade,
imobiliária, clínicas, marketing, audiovisual, mentorias — Brasil e Portugal). A pessoa
instala as skills no Claude Code e monta, na própria máquina, o "funcionário de IA" dela:
uma pasta que conhece o negócio, a voz capturada, tarefas ensinadas uma vez.

**Fonte de verdade do que cada skill precisa fazer ao vivo:** o deck do workshop, em
`/Users/eldermoraes/git/eldermoraes/daflow/talks/2026-08-workshop-ia-empreendedores/deck.md`.
Toda demo descrita lá tem que funcionar exatamente como descrita. Ler o deck inteiro antes
de começar.

**Princípios inegociáveis (valem para cada arquivo escrito):**

1. **Público leigo.** Tudo em pt-BR direto, sem jargão técnico, sem termos em inglês
   desnecessários, sem rótulos inventados. Um dono de confeitaria precisa entender cada
   frase. Palavras proibidas nos textos voltados ao usuário: fixture, workflow, prompt
   engineering, pipeline, payoff, framework, mindset. "Skill", "chat" e "post" são ok
   (a própria turma usa).
2. **Nada de promessa.** Zero "em breve", "vem aí", "próxima versão". O repositório nasce
   completo. O que não existe não é mencionado.
3. **Local primeiro.** Os dados do usuário vivem em `~/escritorio-ia/`, nunca dentro do
   clone do repositório (atualizações não podem tocar nos dados da pessoa).
4. **A IA não inventa.** Toda skill que coleta informação pergunta o que não sabe e marca
   pendências; nunca preenche lacuna com suposição.
5. **Conferência humana.** Toda skill que produz algo publicável ou estratégico termina
   lembrando, com naturalidade, que a pessoa revisa antes de usar.
6. **Dados de terceiros não entram.** Guardrail literal em toda skill que ingere dados
   (texto adaptável ao contexto da skill): "Esta pasta descreve o SEU negócio, nunca os
   clientes dele. Se aparecer nome, CPF, dado de saúde ou caso identificável de um cliente
   ou paciente, pare e peça uma versão sem identificação — descreva o padrão, não o caso."
7. **Compatibilidade.** Skills seguem o padrão aberto Agent Skills (`SKILL.md` com
   frontmatter YAML `name` + `description`). Funcionam no Claude Code (caminho principal)
   e no Codex/ChatGPT (compatível). Evitar dependência exclusiva do Claude Code fora do
   modo paralelo do `conselho` (que tem fallback sequencial).
8. **Voz do material.** Textos que o usuário lê (README, COMECE-AQUI, guias) soam como o
   Elder: direto, franco, sem hype. Referência de voz:
   `/Users/eldermoraes/git/eldermoraes/voz-autoral/elder-voice/` (ler VOICE.md e
   GLOSSARY.md). **Proibido** copiar o VOICE.md do Elder ou qualquer conteúdo autoral dele
   para dentro do repo — o que se aproveita é o método e o tom, nunca o material.

---

## 2. Estrutura final do repositório

```
ai-tools/
├── README.md            ← o que é, pré-requisitos, instalação em 2 passos, compatibilidade, licença
├── AGENTS.md            ← instruções canônicas para o agente (arquivo padrão vendor-neutral)
├── CLAUDE.md            ← uma linha exata: @AGENTS.md
├── INSTALL.md           ← roteiro que o PRÓPRIO agente segue ao instalar
├── COMECE-AQUI.md       ← mapa "o que você quer → qual skill usar" + primeiro passo
├── LICENSE              ← MIT
├── skills/
│   ├── meu-negocio/SKILL.md
│   ├── minha-voz/SKILL.md
│   ├── minha-marca/SKILL.md
│   ├── conselho/SKILL.md
│   ├── conteudo/SKILL.md
│   ├── radar/SKILL.md
│   ├── trafego/SKILL.md
│   ├── video/SKILL.md
│   └── telegram/
│       ├── SKILL.md
│       ├── telegram.py
│       └── test_telegram.py
├── modelos/
│   ├── radar.md         ← modelo preenchível do radar (usado no exercício do workshop)
│   └── conversa-exemplo-whatsapp.txt  ← conversa simulada p/ demo do WhatsApp (slide 32)
└── avancado/
    ├── meta-ads.md      ← guia de conexão do Meta Ads MCP
    ├── telegram.md      ← guia de SETUP da skill telegram (BotFather + token + --setup)
    ├── video-completo.md← guia do fluxo pesado de vídeo (render local)
    └── agendamento.md   ← guia: rodar o radar sozinho toda manhã (máquina ligada)
```

A pasta de dados que o INSTALL.md cria na máquina do usuário:

```
~/escritorio-ia/
├── negocio/    ← escrita pela meu-negocio
├── voz/        ← minha-voz
├── marca/      ← minha-marca
├── conselho/   ← vereditos salvos
├── conteudo/   ← posts gerados
└── radar/      ← relatórios (um arquivo por dia: AAAA-MM-DD.md)
```

---

## 3. Arquivos de fundação (fase 1)

### README.md
Seções, nesta ordem:
1. Uma frase do que é (sem slogan).
2. **Antes de instalar:** precisa de assinatura do Claude (pelo menos o plano Pro) e do
   Claude Code instalado — link da documentação oficial de instalação da Anthropic.
   Dizer o custo de frente, sem rodeio.
3. **Instalação em 2 passos:** (1) instale o Claude Code; (2) abra e cole o prompt:
   > Baixe o repositório https://github.com/eldermoraes/ai-tools e siga o INSTALL.md dele.
4. **Funciona com ChatGPT?** Sim: as skills seguem um padrão aberto lido também pelo
   Codex (o modo do ChatGPT que mexe em arquivos). O caminho guiado e testado é o Claude
   Code; pelo Codex funciona, por conta própria. Uma frase, sem tutorial.
5. **Suporte:** "Este material é fornecido como está, sem garantias e sem prazo de
   resposta. Travou? Cole o erro no seu Claude e peça ajuda — é a rota oficial, e
   funciona." Nada de prometer resposta a issues.
6. Licença MIT.

### CLAUDE.md
Conteúdo exato, uma linha: `@AGENTS.md`

### AGENTS.md
Instruções canônicas para qualquer agente operando neste repo/nas skills:
- idioma pt-BR com o usuário; tom simples, sem jargão;
- os dados do usuário vivem em `~/escritorio-ia/` — nunca gravar dados no clone do repo;
- toda skill lê `~/escritorio-ia/negocio/contexto.md` quando existir, antes de qualquer
  tarefa sobre o negócio;
- regra de dados de terceiros (princípio 6, texto completo);
- regra de conferência humana (princípio 5);
- nunca publicar, enviar ou postar nada em nome do usuário; entregar texto para ele usar.

### INSTALL.md
Roteiro imperativo que o agente executa. Passos:
1. Baixar o repositório como zip via `curl -L` do endpoint de archive do GitHub
   (**nunca `git clone`** — a máquina do leigo pode não ter git) e extrair em pasta
   temporária.
2. Copiar cada `skills/*/` para `~/.claude/skills/` (criar se não existir). Se o agente
   que está instalando não for o Claude Code (ex.: Codex), instalar no diretório de skills
   equivalente da própria ferramenta.
3. Copiar `modelos/` e `avancado/` para `~/escritorio-ia/_kit/` (referência local).
4. Criar `~/escritorio-ia/` com as 6 subpastas vazias.
5. Verificar: listar as 8 skills instaladas e as pastas criadas, mostrando ao usuário.
6. Avisar com estas palavras: "Feche e abra o Claude Code de novo — skill nova só carrega
   em conversa nova."
7. Sugerir o primeiro passo: "Depois de reabrir, diga: **use a skill meu-negocio**."
Incluir no fim uma seção "Telas que vão aparecer": explicar em linguagem leiga os pedidos
de permissão do Claude Code (criar pasta, escrever arquivo, buscar na internet) e o que
responder — a pessoa nunca viu isso e não pode achar que é vírus.

### COMECE-AQUI.md
Tabela literal (é a que o slide 08 do deck anuncia):

| Você quer | Use |
|---|---|
| A IA conhecer o seu negócio (comece por aqui) | `meu-negocio` |
| Posts e textos no SEU tom, sem cara de robô | `minha-voz`, depois `conteudo` |
| Editar vídeo: cortes e legendas a partir da transcrição | `video` |
| Analisar suas campanhas de anúncio | `trafego` (requer conexão — veja `avancado/meta-ads.md`) |
| Um conselho para uma decisão difícil | `conselho` |
| Um relatório do seu negócio toda manhã | `radar` |
| Receber arquivos e avisos no seu celular | `telegram` (requer configuração — veja `avancado/telegram.md`) |
| Identidade visual: cores, fontes, documentos com a sua cara | `minha-marca` |

Depois da tabela: o passo a passo mínimo do primeiro dia (meu-negocio → minha-voz →
conteudo), em 5 linhas; e a lista do que exige etapa extra (trafego, telegram,
agendamento, video-completo) com aviso honesto de que são o degrau seguinte.

### modelos/radar.md
Modelo preenchível usado ao vivo no exercício do slide 36 do deck. Campos:
"O que eu quero vigiar" (concorrentes, preços, setor, oportunidades — com exemplos por
ramo: imobiliária, confeitaria, advocacia), "As 2 perguntas que importam para mim",
"Meus canais/fontes preferidos (se tiver)". Instrução no topo: preencha hoje, rode amanhã
de manhã dizendo ao Claude "use a skill radar".

### modelos/conversa-exemplo-whatsapp.txt
Conversa simulada no formato EXATO da exportação nativa do WhatsApp
(`[dd/mm/aaaa hh:mm] Nome: mensagem`), ~40 mensagens entre uma dona de negócio fictícia
de um ramo que NÃO existe na turma (ex.: loja de aquários) e 3 clientes. Deve conter, de
propósito: 2 perguntas que se repetem, 1 follow-up esquecido, 1 venda que morreu no meio.
É a prop da demo do slide 32 — a análise ao vivo precisa achar essas 4 coisas.

### LICENSE
MIT padrão, ano 2026, Elder Moraes.

---

## 4. As 8 skills (fases 2 a 4)

Formato comum de todo `SKILL.md`: frontmatter YAML com `name` (slug) e `description`
(uma frase, em pt-BR, dizendo quando usar — o agente decide o disparo por ela); corpo em
pt-BR descrevendo comportamento passo a passo. Cada skill traz no topo do corpo a sua
**etiqueta de custo** com frequência sugerida (aparece na tabela do slide 34 do deck):

| Skill | Custo | Frequência sugerida |
|---|---|---|
| meu-negocio | $ | uma vez, e revisita quando o negócio mudar |
| minha-voz | $ | uma vez |
| minha-marca | $ | uma vez |
| conteudo | $ | toda semana |
| radar | $$ | toda manhã, quando você pedir |
| video | $ | por vídeo |
| trafego | $$ | 1-2x por semana |
| conselho | $$ a $$$ | só em decisão que vale o custo |
| telegram | $ | sempre que quiser algo no celular |

Regras de interação comuns: uma pergunta por vez; **gravar cada resposta em disco
imediatamente** (nunca acumular tudo na conversa — se a conversa compactar, nada se
perde); ao final, mostrar a lista dos arquivos criados/alterados.

### 4.1 `meu-negocio` — a pasta do negócio ($)
A skill âncora. Entrevista guiada que escreve `~/escritorio-ia/negocio/`.

- Abertura: explica em 2 frases o que vai acontecer e que dá para parar e retomar depois.
- Blocos da entrevista, cada um gravado no seu arquivo ao concluir:
  1. **O essencial** → `contexto.md` (o resumo que TODAS as outras skills leem primeiro):
     o que vende, para quem, preços, diferencial, canais, como prefere ser chamada.
  2. **Perguntas de clientes** → `perguntas-frequentes.md`: as ~10 perguntas que os
     clientes mais fazem, com a resposta que a pessoa dá.
  3. **Clientes e pendências** → `clientes-e-pendencias.md`: com quem está falando, o que
     deve a quem, follow-ups em aberto. Aqui o guardrail de terceiros é ativo: primeiro
     nome ou apelido basta; nada de documento, telefone, dado de saúde.
  4. **Regras do setor** → `regras.md`: o que o conselho de classe / regulação proíbe
     (advocacia, saúde, contabilidade, financeiro). A skill pergunta explicitamente; se a
     pessoa não for de setor regulado, registra "sem restrições específicas".
  5. **Números** (opcional, oferecido no fim): faturamento aproximado, custos, metas →
     `numeros.md`. Deixar claro que é opcional e fica só na máquina dela.
- Reexecutável: se os arquivos existem, vira modo atualização (mostra o que tem e pergunta
  o que mudou), nunca sobrescreve do zero.
- **Caso de uso embutido** (demo do slide 14): o corpo da skill ensina o agente que, quando
  o usuário colar uma mensagem de cliente, deve responder usando `contexto.md` +
  `perguntas-frequentes.md` no tom registrado, entregando RASCUNHO para a pessoa revisar e
  colar — nunca se oferecer para enviar.
- Ao final da primeira execução completa: sugere uma pergunta real de teste ("me pergunte
  algo sobre o seu negócio para ver a pasta funcionando").

### 4.2 `minha-voz` — a voz capturada ($)
- Pede 3 a 10 textos reais da pessoa (posts, e-mails, mensagens). Fallback embutido no
  texto da skill: "não tem textos à mão? Abra o WhatsApp e copie 3 mensagens que você
  mandou para clientes esta semana."
- Entrevista curta de tom: o que nunca diria, gírias e bordões, nível de formalidade,
  emojis sim/não, como cumprimenta e como se despede.
- Extrai padrões e grava `~/escritorio-ia/voz/VOICE.md`: características observadas com
  exemplos tirados dos textos da pessoa, lista do que evitar, 2-3 amostras originais como
  referência.
- **Validação obrigatória** (é a demo do slide 18): reescreve um parágrafo genérico
  (embutido na skill) na voz capturada e pergunta "soa como você?". Ajusta e repete até a
  pessoa aprovar. Só grava a versão final após aprovação.
- Método inspirado no sistema de voz autoral do Elder (estrutura VOICE/GLOSSARY), mas o
  arquivo gerado é 100% da pessoa.

### 4.3 `conteudo` — os posts da semana ($)
- Pré-requisito: lê `negocio/contexto.md` e `voz/VOICE.md`. Se faltarem, orienta rodar as
  skills anteriores primeiro (com a frase exata do comando).
- Fluxo (é o exercício do slide 21): pergunta (1) o assunto que a pessoa quer comunicar
  nesta semana e (2) pede o insumo: **3 tópicos escritos pela pessoa, ou a transcrição de
  um áudio de 1 minuto dela falando do assunto**. Sem insumo próprio, a skill avisa — com
  o texto da escada do deck (slide 20) resumido: "só o tema dá texto com cara de robô;
  quanto mais partir de você, mais parece você" — e insiste uma vez antes de aceitar
  seguir só com o tema.
- Pergunta os canais (Instagram, LinkedIn, WhatsApp, e-mail) e gera 3 rascunhos adaptados,
  um por vez, com aprovação entre eles.
- Grava em `~/escritorio-ia/conteudo/AAAA-SS-assunto.md`.
- Nunca posta, nunca agenda; fecha lembrando a conferência antes de publicar.

### 4.4 `conselho` — a decisão difícil ($$ a $$$)
A mais elaborada. Cinco conselheiros-papéis fixos (nunca pessoas reais): **financeiro
conservador, comercial agressivo, voz do cliente, operacional, visionário**. Todos leem
`negocio/contexto.md` (e `numeros.md` se existir) antes de opinar.

- Início: pede a decisão em uma frase + contexto que a pessoa quiser dar. Depois UMA
  pergunta: **"É uma decisão do dia a dia, uma decisão grande, ou a decisão máxima?"**
  com uma linha de custo/tempo para cada.
- **Dia a dia (padrão):** a skill escolhe os 3 conselheiros mais relevantes para aquela
  decisão (e diz quais escolheu e por quê — "para essa decisão eu chamei..."). Os 3 opinam
  em sequência, cada parecer independente (instrução: não citar nem concordar com os
  anteriores). Rodar os conselheiros no modelo rápido/barato disponível (no Claude Code,
  subagents em Haiku); a síntese final roda no modelo principal da sessão.
- **Decisão grande:** os 5 conselheiros, em 3 estágios (é a demo dos slides 26-27):
  (1) cada um opina SEM ver os outros — no Claude Code, subagents paralelos; em ferramenta
  sem subagents, sequencial com a mesma instrução de independência; (2) revisão às cegas:
  os pareceres voltam anonimizados como Conselheiro A-E e cada um é criticado/ranqueado
  sem autoria; (3) o presidente sintetiza: placar, divergência principal, recomendação.
- **Decisão máxima:** igual à grande, forçando o melhor modelo disponível na conta em
  todas as etapas. **Degradação graciosa obrigatória:** se o modelo topo não estiver
  disponível, avisar em UMA frase ("seu plano vai até o modelo X — rodando como decisão
  grande, que já é o conselho completo") e seguir. Nunca falhar por causa de modelo.
- **Progresso visível:** anunciar cada etapa enquanto roda ("o financeiro entregou o
  parecer... agora avaliam às cegas...") — silêncio longo faz o leigo achar que travou.
- Veredito gravado em `~/escritorio-ia/conselho/AAAA-MM-DD-tema.md`.
- Rodapé fixo em todo veredito: "Isto é análise para apoiar a SUA decisão. Não é
  aconselhamento financeiro nem jurídico."

### 4.5 `radar` — o relatório da manhã ($$)
- Primeira execução = configuração: o que vigiar (concorrentes, preços, setor,
  oportunidades), as 2 perguntas que importam, fontes preferidas. Grava em
  `~/escritorio-ia/radar/config.md`. Se `~/escritorio-ia/_kit/modelos/radar.md` já foi
  preenchido pela pessoa (exercício do workshop), importa dele.
- Execuções seguintes: busca na internet guiada pela config, cruza com
  `negocio/contexto.md`, entrega **"as 3 coisas que importam hoje"** com uma ação sugerida
  para cada, e grava `~/escritorio-ia/radar/AAAA-MM-DD.md`.
- Se rodar duas vezes no dia, atualiza o arquivo do dia (não duplica).
- No fim de cada relatório, uma linha fixa: "Quer receber isso no seu celular? Configure
  a skill `telegram` (guia em `avancado/telegram.md`). Quer que rode sozinho toda manhã?
  Guia em `avancado/agendamento.md` — exige a máquina ligada."

### 4.6 `trafego` — o diagnóstico de anúncios ($$)
- Primeiro passo sempre: verificar se o Meta Ads MCP está conectado (tentar listar as
  contas). Se não estiver: parar e indicar `avancado/meta-ads.md`, sem tentar improvisar.
- Três modos, oferecidos como pergunta única: **diagnóstico geral** (para onde o dinheiro
  vai, o que está caro comparado ao histórico da própria conta, campanha parada),
  **comparar criativos** (qual anúncio paga a conta e qual queima verba),
  **o que ajustar hoje** (a versão de 2 minutos).
- Saída em linguagem de dono: sem CPM/CTR sem tradução — "custo por pessoa alcançada",
  "de cada 100 que viram, X clicaram". Priorizada: no máximo 3 ajustes por vez.
- **SÓ LEITURA — regra literal no texto da skill:** "Nunca chame ferramentas que criam,
  alteram, ativam ou pausam campanhas, conjuntos, anúncios ou orçamentos
  (ads_update_*, ads_create_*, ads_activate_*). Se o usuário pedir para aplicar um
  ajuste, explique o passo a passo para ele fazer no Gerenciador de Anúncios."
- Rodapé: mesmo disclaimer do conselho.

### 4.7 `video` — cortes e legendas ($)
Caminho leve, 100% texto (funciona em qualquer máquina — é o que o slide 31 do deck
promete):
- Entrada: a transcrição do vídeo (a pessoa cola, ou aponta um arquivo .txt/.srt). Se ela
  só tem o vídeo, a skill orienta como obter transcrição (apps de transcrição do celular,
  YouTube) sem prometer fazer isso localmente.
- Saída 1 — **lista de cortes**: hesitações, repetições, erros regravados e silêncios
  identificáveis no texto, cada um com a marcação de tempo e o motivo, para a pessoa
  aplicar no editor que já usa (CapCut, InShot, o que for).
- Saída 2 — **legendas**: arquivo `.srt` limpo (sem os trechos cortados) que qualquer
  editor importa.
- Saída 3 (opcional) — **clipes**: sugestões de 2-3 trechos que funcionam sozinhos como
  vídeo curto, com início/fim e a razão.
- Aviso honesto no texto da skill: isso NÃO edita o vídeo; edita o mapa do vídeo. O fluxo
  que corta e renderiza sozinho é o `avancado/video-completo.md`.

### 4.8 `minha-marca` — a identidade visual ($)
- Entrevista curta: cores que já usa (ou de que gosta), 2-3 referências visuais que
  admira, o que odeia, tipo de negócio. Sugere paleta (com códigos), par de fontes comuns
  (disponíveis no Canva/Google Fonts) e 3 princípios de uso simples.
- Grava `~/escritorio-ia/marca/BRAND.md`.
- Validação: gera um cartão/one-pager HTML simples do negócio aplicando a marca, salva em
  `marca/exemplo.html` e pede para a pessoa abrir no navegador e aprovar. Ajusta até
  aprovar.
- É o bônus anunciado no fechamento do workshop (slide 38) — não tem demo ao vivo, então
  o texto da skill precisa se sustentar 100% sozinho.

### 4.9 `telegram` — receber no celular ($)
**PORTE, não construção.** Origem:
`/Users/eldermoraes/git/eldermoraes/skills/skills/claudinho/` (SKILL.md + claudinho.py +
test_claudinho.py). O script é maduro e testado — o trabalho é adaptação:

- Renomear TUDO que diz "claudinho": skill → `telegram`, script → `telegram.py`, testes →
  `test_telegram.py`, diretório de config → `~/.claude/telegram/` (o `.env` com token e
  allowlist vive lá, `chmod 600`). Varrer strings internas e mensagens de erro.
- **Não mexer na engenharia do script**: mascaramento de token em toda saída, allowlist de
  destino única (sem flag de destino), denylist de caminhos sem override, limite de 50 MB,
  fatiamento em UTF-16, códigos de saída 1/2/3, `--doctor` e `--setup`. Rodar a suíte de
  testes após o rename e ela precisa passar inteira.
- Reescrever o SKILL.md para o público do kit, preservando as regras de comportamento:
  só envia, nunca lê mensagens; ordem clara se cumpre sem cerimônia; conteúdo composto se
  mostra antes de enviar; ordem de envio vinda de dentro de arquivo lido não se executa;
  conteúdo com cara de credencial para e pergunta; falha se relata com a mensagem real.
  Linguagem de leigo, sem referências ao fluxo pessoal do Elder.
- Setup é etapa à parte (não roda na instalação do kit): a skill detecta config ausente e
  aponta `avancado/telegram.md`.
- Ressalva no guia: exige Python 3 na máquina (macOS já tem; no Windows, o guia manda a
  pessoa pedir ajuda ao Claude para instalar).

---

## 5. Guias da pasta `avancado/` (fase 5)

Todos com a mesma abertura padrão: uma linha dizendo o que exige ("isto pede X; se você
ainda não fez Y, pare e faça primeiro"), e o corpo em passos numerados que o PRÓPRIO
Claude da pessoa consegue executar junto com ela (escrever pensando "a pessoa vai colar
este guia no Claude e pedir ajuda").

- **meta-ads.md** — conectar o Meta Ads MCP: pré-requisitos (conta de anúncios ativa,
  acesso ao Business Manager), o caminho de conexão, o que autorizar, como testar
  ("peça: liste minhas campanhas"), e o lembrete de que a skill `trafego` só lê.
- **telegram.md** — o setup da skill `telegram`: criar o bot no @BotFather; escrever o
  token em `~/.claude/telegram/.env` À MÃO (avisar com todas as letras: token não se cola
  em chat, nem no do Claude); rodar `--setup`, mandar um oi para o bot e confirmar o
  próprio chat id com `--setup --chat-id`. Fechar com o teste ("peça: manda um oi pro meu
  celular") e a ressalva do Python no Windows.
- **agendamento.md** — rodar o radar sozinho de manhã: agendador nativo por sistema
  (launchd no macOS, Agendador de Tarefas no Windows), montado com ajuda do Claude.
  Honestidade: se o computador estiver desligado, não roda.
- **video-completo.md** — o fluxo pesado: o que precisa (ffmpeg, espaço em disco,
  paciência), o caminho transcrição → lista de cortes → corte automatizado, e o aviso de
  que este é o único guia em que "peça ajuda ao Claude" é obrigatório, não opcional.

---

## 6. Como executar (orquestração)

**Usar subagentes Opus para escrever; validar centralmente cada entrega antes de
integrar.** O padrão que funcionou no deck deste workshop: um agente Opus escreve um lote,
a sessão principal valida item a item contra este plano (checklist da fase), corrige o que
for pontual, devolve as lições ao agente na instrução do lote seguinte. Nunca integrar
sem validar. Instruir cada agente a retornar só "pronto" + decisões/dúvidas em 5 linhas
(não repetir o conteúdo na resposta).

**Fases e ordem (cada fase = um lote de escrita + uma validação + um commit):**

1. **Fundação:** README, AGENTS.md, CLAUDE.md, INSTALL.md, COMECE-AQUI.md, LICENSE,
   modelos/ (radar + conversa de exemplo).
2. **Trilho principal:** `meu-negocio`, `minha-voz`, `conteudo` — nesta ordem; são as
   skills dos exercícios ao vivo, a prioridade absoluta.
3. **Demos do Elder:** `conselho`, `radar`, `trafego`, `video`.
4. **Bônus e porte:** `minha-marca`; porte da skill `telegram` (seção 4.9 — adaptar,
   rodar a suíte de testes renomeada até passar inteira).
5. **Guias:** os 4 de `avancado/`.
6. **Teste de máquina limpa** (não pular): num diretório home simulado (`HOME` temporário
   ou usuário limpo), executar o INSTALL.md do zero como um leigo faria; rodar a entrevista
   completa da `meu-negocio` respondendo como uma dona de confeitaria fictícia; rodar
   `minha-voz` + `conteudo` com textos inventados; rodar `conselho` no modo dia a dia E no
   modo decisão grande; rodar `radar` (config + uma execução); rodar `video` com uma
   transcrição de teste; rodar `telegram --doctor` sem config e conferir que a mensagem
   aponta o guia (o envio real só o Elder testa, com bot dele); conferir que cada arquivo prometido apareceu no lugar certo, que
   nenhuma skill gravou nada dentro do clone e que nenhum texto viola os princípios da
   seção 1. Corrigir e repetir até passar inteiro.

**Checklist de validação de cada SKILL.md** (aplicar a todos):
- [ ] frontmatter `name` + `description` corretos; description dispara no pedido leigo
      ("quero um post", "me ajuda a decidir", "analisa minha campanha");
- [ ] uma pergunta por vez; grava em disco a cada resposta;
- [ ] lê `negocio/contexto.md` quando a tarefa envolve o negócio;
- [ ] guardrail de terceiros presente (quando ingere dados);
- [ ] fecha com conferência humana (quando produz material);
- [ ] etiqueta de custo + frequência no topo;
- [ ] zero jargão, zero inglês desnecessário, zero promessa;
- [ ] bate com a demo correspondente do deck (conferir slide a slide);
- [ ] nada gravado dentro do repositório clonado.

**Git:** commit por fase, mensagens curtas em português, push ao final de cada fase
(`git push origin main`). O repositório é privado até o dia do workshop.

**Ao terminar tudo:** apagar este `ai-tools.md`, commit final "repo pronto para o
workshop" e push.

---

## 7. O que este plano deliberadamente NÃO inclui

- **Escrever a skill de Telegram do zero**: ela é PORTADA de código existente e testado
  do Elder (seção 4.9). Não reescrever o script, não "melhorar" a engenharia dele, não
  adicionar recebimento de mensagens — só saída, por decisão de desenho.
- **Automação agendada como padrão**: o radar é sob demanda; agendar é guia avançado.
- **Qualquer conteúdo autoral do Elder** (VOICE.md dele, textos dele, dados de campanhas):
  o repo é template e método, nunca material pessoal.
- **Copiar qualquer coisa do produto "Fluxo Criativo"** (metodologia VTSD): nem comandos,
  nem termos (Quadro, Furadeira, Mandala, 8D, Light Copy), nem estruturas de funil/copy.
  As skills daqui LEEM e DIAGNOSTICAM ou executam com insumo do usuário; criação de
  estratégia de marketing é território de fora.
