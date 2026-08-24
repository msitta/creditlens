<h1><center> Registro de decisões </center></h1>

Cada entrada: o que foi decidido, por quê, e o que faria eu mudar de ideia.
Decisão sem condição de reversão é palpite bem escrito.

Entrada revista não se apaga: emenda-se, com ponteiro para a nova. O rastro é o ativo.

---

## 03/08/2026 — Recorte: pessoa jurídica, Paraná, 2019 a 2026

**Por quê:** cabe no prazo de um mês e é o mercado que eu conheço de perto. 2019 dá pré-pandemia como linha de base.

**O que me faria mudar:** se o Paraná mostrar comportamento atípico frente ao Brasil, o recorte vira limitação séria e é necessário declarar isso.

> **Emendada em 20/08/2026:** recorte ampliado para nacional. O denominador do Paraná era pequeno demais para o segmento fintech (0,07% do crédito estadual), e proporção sobre denominador pequeno não é estável — o mesmo raciocínio do piso de 1%.

---

## 03/08/2026 — Tratar `-1` como ausência, não como valor

**Por quê:** o `-1` em `numero_de_operacoes` é supressão por sigilo, não quantidade. Somar ou tirar média com ele produz resultado errado sem erro aparente. Guardei também uma coluna marcando onde a supressão ocorreu, porque ela é informação: indica onde há poucas operações.

**O que me faria mudar:** nada. Manter o `-1` como número é erro, não escolha.

---

## 04/08/2026 — Medir em `carteira_ativa`, não em contagem

**Por quê:** contagem de linhas trata operação de dez mil e de dez milhões como iguais. `numero_de_operacoes` está incompleto em 28,9% das linhas por causa da supressão, e o que falta não é aleatório — concentra-se nas células pequenas.   
Saldo em reais é a única das três medidas sem viés conhecido aqui.

**O que me faria mudar:** se a pergunta virasse "quantas empresas", saldo não serve. Mas essa pergunta não tem resposta nesta base.

---

## 04/08/2026 — Hipótese original testada e rejeitada

**Hipótese:** o banco tradicional não consegue enquadrar parte relevante das pequenas empresas, e elas pagam caro por isso.

**Teste:** fatia de porte indisponível dentro de cada segmento, no mês mais recente.

**Resultado:** Banco 1%, Fintech 31%, Instituição de pagamento 11%. O banco sabe o faturamento de quase todas as empresas para as quais empresta. A hipótese não se sustenta.

**O que ficou no lugar:** o campo vazio descreve o método de quem concedeu, não a empresa. A série passa a medir quanto do crédito é concedido sem olhar faturamento, e a que velocidade esse fenômeno cresce.

---

## 04/08/2026 — Piso de 1% para incluir um segmento no gráfico

**Por quê:** a linha de Instituição de pagamento oscilava entre 97% e zero. Investigando, a causa é denominador pequeno: com carteira reduzida, poucos contratos deslocam a proporção inteira. Proporção sem volume não é estável.

**Como apliquei:** o piso vale para todos os segmentos, não só para o que eu queria excluir. Se derrubasse a fintech, teria que aceitar.

**O que me faria mudar:** se o segmento crescer e passar o piso, ele volta ao gráfico.

---

## Em aberto

**Transição de versão V1→V2 da base.** Se a subida do `porte_indisponivel` na fintech coincidir com a migração metodológica, o achado pode refletir mudança de coleta, e não comportamento de mercado. Teste desenhado: marcar o corte na série e comparar os dois segmentos — se só a fintech se move, a versão não explica o fenômeno. Não publicar conclusão antes disso.

**Movimento inexplicado em julho/2025 na linha de banco.** Enfraquece o argumento do banco como controle imóvel naquele mês específico. Declarado como caveat em aberto, não resolvido.

---

## Modelo para as próximas

## DD/MM/AAAA — [decisão]

**Por quê:**

**O que me faria mudar:**
