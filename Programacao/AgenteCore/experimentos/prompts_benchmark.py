# ! Alteração de IA - Revisar: cenários reais usados para comparar os portes do modelo.
# ! Motivo: a comparação entre 1.5B/3B/7B só é útil se as tarefas forem as mesmas que o
# agente executará de verdade. Por isso os dados abaixo são do cobaia real — o contrato
# de GET /api/produtos e a árvore de acessibilidade de produtos_api.php — e não exemplos
# genéricos, que fariam qualquer modelo parecer adequado.

INSTRUCAO_DIAGNOSTICO = """Você analisa falhas de integração entre uma interface web e sua API.
Responda em português, em no máximo 6 linhas, cobrindo exatamente:
1. CAUSA RAIZ: o que divergiu do contrato esperado.
2. CAMPO: o nome do campo afetado.
3. IMPACTO: o que o usuário vê na tela por causa disso.
Não sugira código. Não repita o JSON."""

# Cenário real: CobaiaAPI em modo de falha "field_renamed" no campo preco.
# A página produtos_api.php lê p.preco para montar o card; com o campo renomeado,
# a leitura resulta em indefinido e o preço aparece quebrado no cartão.
CENARIO_DIAGNOSTICO = """REQUISIÇÃO
GET http://localhost:8000/api/produtos
Origem: http://localhost:8080/produtos_api.php

RESPOSTA
HTTP 200 application/json
[
  {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa",
   "tipo": "Carnes", "preco_v2": 89.9, "imagem": "picanha_alho.jpg", "destaque": true},
  {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto",
   "tipo": "Carnes", "preco_v2": 84.9, "imagem": "picanha_sem.jpg", "destaque": false}
]
(lista truncada: 14 itens no total, mesmas chaves em todos)

CONTRATO ESPERADO PELA INTERFACE
id: inteiro | nome: texto | resumo: texto | tipo: texto | preco: número | imagem: texto | destaque: booleano

SINTOMA OBSERVADO NA INTERFACE
Os cartões de produto exibem "R$ NaN" no lugar do valor.

CONHECIMENTO PRÉVIO DO SISTEMA
- A função formatarPreco() em produtos_api.php converte o campo preco com Number() antes de exibir.
- O campo preco vem da coluna valor_produto (DECIMAL 9,2) da tabela tbprodutos."""

INSTRUCAO_SELETOR = """Você conserta localizadores quebrados de teste automatizado.
Receberá a árvore de acessibilidade da página e o seletor que falhou.
Responda APENAS com até 3 seletores CSS candidatos, um por linha, sem numeração,
sem explicação e sem crase. O primeiro deve ser o mais provável."""

# Árvore de acessibilidade podada da página produtos_api.php, no formato role "nome".
CENARIO_SELETOR = """SELETOR QUE FALHOU
button.btn-detalhes

INTENÇÃO DO PASSO DE TESTE
Abrir os detalhes do produto "Picanha ao Alho" a partir do cartão dele.

ÁRVORE DE ACESSIBILIDADE (podada)
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "DESTAQUES"
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Picanha ao Alho" level=3
      text "Carnes"
      text "Picanha grelhada com alho laminado na brasa"
      button "R$ 89,90" disabled
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      button "R$ 84,90" disabled
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2\""""

TAREFAS = [
    {"nome": "diagnostico", "instrucao": INSTRUCAO_DIAGNOSTICO, "cenario": CENARIO_DIAGNOSTICO},
    {"nome": "seletor", "instrucao": INSTRUCAO_SELETOR, "cenario": CENARIO_SELETOR},
]
