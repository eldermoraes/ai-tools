# Conectar a sua conta de anúncios do Meta

Isto pede uma conta de anúncios ativa no Facebook/Instagram e o seu acesso ao
Gerenciador de Negócios (Business Manager). Se você não anuncia hoje, ou se quem
anuncia por você é uma agência e você não tem login próprio, pare aqui: resolva o
acesso primeiro e volte depois.

Este guia serve para você e para o seu Claude ao mesmo tempo. O caminho mais curto
é abrir o Claude Code, colar este arquivo inteiro na conversa e escrever:

> Me ajuda a seguir este guia, passo a passo.

---

## Antes de começar

Três coisas precisam ser verdade:

1. **Você tem uma conta de anúncios ativa.** Entre em
   `business.facebook.com` e confirme que consegue ver suas campanhas.
2. **O login é seu.** O e-mail e a senha do Facebook que dão acesso a essa conta
   estão com você. Se a agência criou tudo na conta dela, peça para ela adicionar
   você como pessoa com acesso à conta de anúncios.
3. **Você já rodou a skill `meu-negocio`.** A análise fica muito melhor quando a
   IA sabe o que você vende e por quanto. Não é obrigatório, mas ajuda.

Você não precisa saber o que é MCP, API ou token para fazer isto. É uma tela de
autorização do próprio Facebook, igual a quando um aplicativo pede para entrar com
a sua conta.

---

## Passo 1: abrir a lista de conexões

No Claude Code, digite:

```
/mcp
```

Esse comando abre a lista de conexões disponíveis e mostra quais já estão ligadas.
Procure a conexão do Meta Ads (anúncios do Meta) na lista.

Se você não achar, ou se a tela parecer diferente do que este guia descreve, peça
ao Claude na mesma conversa:

> Quero conectar minha conta de anúncios do Meta aqui. Me mostra o caminho.

A lista de conexões muda de tempos em tempos. O seu Claude enxerga a versão atual;
este guia, não. Quando as duas discordarem, siga o que está na tela.

## Passo 2: autorizar

Ao escolher a conexão, o navegador abre numa página do próprio Facebook pedindo
autorização. Confira três coisas antes de clicar em qualquer botão:

- **O endereço é do Facebook.** Deve começar com `facebook.com`. Se for outro
  endereço, feche e comece de novo.
- **A conta logada é a sua.** Se o navegador estiver logado com outro perfil, saia
  e entre com o certo antes de autorizar.
- **As contas marcadas são as suas.** Se a tela listar contas de anúncio, páginas
  ou negócios, marque só o que é seu e o que você quer analisar. Deixe o resto
  desmarcado.

Autorize o acesso às informações das campanhas: as campanhas em si, os anúncios e
os resultados. É isso que a skill `trafego` lê.

Você nunca digita senha dentro do Claude. A senha, se for pedida, é digitada na
página do Facebook, no navegador. Se alguma tela pedir a sua senha dentro da
conversa com a IA, não digite: a conexão de verdade nunca pede isso ali.

## Passo 3: testar

Volte para o Claude Code e escreva exatamente isto:

> liste minhas campanhas

Se vier uma lista com os nomes das suas campanhas, está conectado. Pode fechar
este guia e ir para o Passo 4.

Se vier um erro, ou se ele disser que não encontrou a conexão:

- Feche e abra o Claude Code de novo. Conexão nova costuma valer só na conversa
  seguinte.
- Rode `/mcp` outra vez e confira se a conexão aparece como ligada.
- Se o erro continuar, cole o texto do erro na conversa e peça: "o que isso quer
  dizer e o que eu faço?". É a rota que funciona.

## Passo 4: usar

Com a conexão de pé, escreva:

> use a skill trafego

Ela vai perguntar o que você quer: um diagnóstico geral, uma comparação entre os
anúncios, ou os ajustes do dia. Escolha um e responda as perguntas.

---

## A skill `trafego` só lê

Isto é decisão de desenho, não limitação temporária.

A `trafego` lê os números e explica o que está acontecendo. Ela **não** cria
campanha, **não** pausa anúncio, **não** aumenta nem corta orçamento, **não**
liga nem desliga nada. Se você pedir para ela aplicar um ajuste, ela vai recusar e
explicar o passo a passo para você fazer no Gerenciador de Anúncios.

O motivo é simples: quem gasta o dinheiro é você. Uma IA que pode subir um
orçamento sozinha é uma IA que pode subir o orçamento errado enquanto você está
no almoço. A análise vem pronta; o clique é seu.

Pelo mesmo motivo, o que ela entrega é diagnóstico para você decidir. Não é
consultoria financeira. Leia, confira contra o que você conhece do seu negócio, e
decida.

---

## Como desconectar

Se você quiser cortar o acesso a qualquer momento, o caminho é o mesmo `/mcp` no
Claude Code, escolhendo a conexão e removendo. Você também pode revogar direto no
Facebook, em Configurações e privacidade → Configurações → Aplicativos e sites.
Revogar por lá derruba o acesso mesmo que o computador esteja desligado.
