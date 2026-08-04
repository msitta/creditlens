# Registro de decisões

Cada entrada: o que foi decidido, por quê, e o que faria eu mudar de ideia.
A última coluna é a que salva numa entrevista — decisão sem condição de
reversão é palpite bem escrito.

**Reescreva cada "por quê" com suas palavras.** Se não sair natural, você não
vai defender aquilo em pé na frente de alguém.

---

## 2026-08-03 — Recorte: pessoa jurídica, Paraná, 2019 a 2026

**Por quê:** cabe no prazo de um mês e é o mercado que eu conheço de perto.
2019 dá pré-pandemia como linha de base.

**O que me faria mudar:** se o Paraná mostrar comportamento atípico frente ao
Brasil, o recorte vira limitação séria e preciso declarar isso.

---

## 2026-08-03 — Tratar `-1` como ausência, não como valor

**Por quê:** o `-1` em `numero_de_operacoes` é supressão por sigilo, não
quantidade. Somar ou tirar média com ele produz resultado errado sem erro
aparente. Guardei também uma coluna marcando onde a supressão ocorreu, porque
ela é informação: indica onde há poucas operações.

**O que me faria mudar:** nada. Manter o `-1` como número é erro, não escolha.

---

## 2026-08-04 — Medir em `carteira_ativa`, não em contagem

**Por quê:** contagem de linhas trata operação de dez mil e de dez milhões como
iguais. `numero_de_operacoes` está incompleto em 28,9% das linhas por causa da
supressão, e o que falta não é aleatório — concentra-se nas células pequenas.
Saldo em reais é a única das três medidas sem viés conhecido aqui.

**O que me faria mudar:** se a pergunta virasse "quantas empresas", saldo não
serve. Mas essa pergunta não tem resposta nesta base.

---

## 2026-08-04 — Hipótese original testada e rejeitada

**Hipótese:** o banco tradicional não consegue enquadrar parte relevante das
pequenas empresas, e elas pagam caro por isso.

**Teste:** fatia de porte indisponível dentro de cada segmento, no mês mais
recente.

**Resultado:** Banco 1%, Fintech 31%, Instituição de pagamento 11%. O banco
sabe o faturamento de quase tudo que empresta. A hipótese não se sustenta.

**O que ficou no lugar:** o campo vazio descreve o método de quem concedeu, não
a empresa. A série passa a medir quanto do crédito é concedido sem olhar
faturamento, e a que velocidade isso cresce.

---

## 2026-08-04 — Piso de 1% para incluir um segmento no gráfico

**Por quê:** a linha de Instituição de pagamento oscilava entre 97% e zero.
Investigando, a causa é denominador pequeno: com carteira reduzida, poucos
contratos deslocam a proporção inteira. Proporção sem volume não é estável.

**Como apliquei:** o piso vale para todos os segmentos, não só para o que eu
queria excluir. Se derrubasse a fintech, teria que aceitar.

**O que me faria mudar:** se o segmento crescer e passar o piso, ele volta ao
gráfico.

---

## Modelo para as próximas

## AAAA-MM-DD — [decisão]

**Por quê:**

**O que me faria mudar:**
