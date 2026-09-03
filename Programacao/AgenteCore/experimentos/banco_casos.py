#!/usr/bin/env python3
# ! Alteração de IA - Revisar: banco de 90 casos de falha (6 classes x 3 níveis x 5 casos).
# ! Motivo: a primeira leva de medições usou 2 casos, o que não sustenta afirmação sobre
# acerto por classe nem por dificuldade. O desenho balanceado é o que permite comparar os
# modelos sem viés de amostragem. Os casos são fixtures gravados, não chamadas ao vivo à
# CobaiaAPI, porque o mesmo caso precisa ser idêntico entre modelos e entre rodadas — com
# chamada ao vivo, latência e estado do banco virariam variáveis de confusão.
#
# Todos os dados vêm do cobaia real: contratos conferidos em CobaiaAPI/app/schemas.py e
# colunas em CobaiaFront/banco/schema_completo.sql. Vários cenários correspondem
# exatamente aos modos que app/fault_injection.py já implementa.

CONTRATO_PRODUTO = (
    "id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | "
    "preco: numero | imagem: texto|nulo | destaque: booleano"
)
CONTRATO_PEDIDO = (
    "id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | "
    "status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto"
)

PRODUTO_OK = ('{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
              '"tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}')

ARVORE_CARTOES = """document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Picanha ao Alho" level=3
      text "Carnes"
      button "R$ 89,90" disabled
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      button "R$ 69,90" disabled
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
"""


def _c(cid, classe, nivel, causa, campo, esperados, proibidos, **entrada):
    return {
        "id": cid, "classe": classe, "nivel": nivel, "entrada": entrada,
        "gabarito": {"causa_raiz": causa, "campo_afetado": campo,
                     "termos_esperados": esperados, "termos_proibidos": proibidos},
    }


CASOS = []

# ------------------------------------------------------------- CLASSE 1: lexica
CASOS += [
    _c("lex-1", 1, 1, "resposta_truncada", None,
       ["truncad", "incomplet", "cortad"], ["timeout", "autentic"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "tipo": "Carnes", "preco": 89.9',
       sintoma="A listagem fica vazia e o console acusa erro ao interpretar a resposta."),
    _c("lex-2", 1, 1, "corpo_nao_e_json", None,
       ["html", "nao e json", "nao era json"], ["campo", "tipo"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='<b>Warning</b>: mysqli_connect(): Access denied<br /><html><body>Erro</body></html>',
       sintoma="A listagem nao carrega; o console acusa token inesperado no inicio da resposta."),
    _c("lex-3", 1, 1, "corpo_vazio", None,
       ["vazio", "sem corpo"], ["truncad", "tipo"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO, corpo="",
       sintoma="A pagina fica em 'Carregando produtos' indefinidamente."),
    _c("lex-4", 1, 2, "codificacao_incorreta", "nome",
       ["codifica", "acent", "encoding", "utf"], ["truncad", "ausente"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 12, "nome": "Queijo Coalho com P\\u00c3\\u00a3o", "tipo": "Acompanhamentos", '
             '"preco": 22.9, "imagem": "queijo.png", "destaque": true, "resumo": null}]',
       sintoma="Os nomes dos produtos aparecem com caracteres estranhos nos cartoes."),
    _c("lex-5", 1, 3, "resposta_truncada", None,
       ["truncad", "interromp", "incomplet"], ["cache", "duplicad"],
       requisicao="GET /api/produtos (resposta em partes)", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[' + PRODUTO_OK + ', {"id": 2, "nome": "Fraldinha", "tipo": "Carnes", "pre',
       sintoma="Ora a lista carrega inteira, ora aparece so o primeiro cartao. "
               "O servidor registra 14 produtos enviados."),
]

# ---------------------------------------------------------- CLASSE 2: sintatica
CASOS += [
    _c("sin-1", 2, 1, "campo_ausente", "preco",
       ["preco", "ausente", "falta"], ["tipo", "renomead"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="Os cartoes exibem 'R$ NaN' no lugar do valor."),
    _c("sin-2", 2, 2, "campo_renomeado", "preco",
       ["renomead", "preco_v2"], ["decimal", "conversao numerica"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco_v2": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="Os cartoes exibem 'R$ NaN' no lugar do valor."),
    _c("sin-3", 2, 2, "estrutura_aninhada_divergente", "tipo",
       ["objeto", "aninhad", "tipo"], ["ausente", "nulo"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": {"id": 1, "nome": "Carnes"}, "preco": 89.9, '
             '"imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="A categoria do produto aparece como [object Object] no cartao."),
    _c("sin-4", 2, 1, "colecao_no_lugar_de_objeto", None,
       ["lista", "objeto", "colec"], ["tipo", "nulo"],
       requisicao="GET /api/produtos/1", status=200,
       contrato=CONTRATO_PRODUTO + " (recurso unico, nao lista)",
       corpo='[' + PRODUTO_OK + ']',
       sintoma="A tela de detalhe do produto nao preenche nenhum campo."),
    _c("sin-5", 2, 3, "campo_ausente", "resumo",
       ["resumo", "ausente", "alguns"], ["todos os itens"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[' + PRODUTO_OK + ', {"id": 2, "nome": "Fraldinha", "tipo": "Carnes", '
             '"preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}]',
       sintoma="Alguns cartoes mostram a descricao e outros nao, sem padrao aparente."),
]

# ---------------------------------------------------------- CLASSE 3: semantica
CASOS += [
    _c("semt-1", 3, 2, "tipo_divergente", "preco",
       ["tipo", "texto", "string"], ["ausente", "renomead"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": "89.90", "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="A ordenacao por preco fica errada: 'R$ 9,90' aparece depois de 'R$ 89,90'."),
    _c("semt-2", 3, 2, "tipo_divergente", "destaque",
       ["destaque", "boolean", "sim"], ["preco", "ausente"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": "Sim"}]',
       sintoma="Todos os produtos aparecem na secao de destaques, inclusive os que nao deveriam."),
    _c("semt-3", 3, 2, "valor_fora_do_dominio", "status",
       ["status", "domin", "pendente"], ["tipo", "ausente"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"status": "Pendente", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="A reserva nao aparece nem como ativa nem como cancelada na area do cliente."),
    _c("semt-4", 3, 2, "formato_de_data_divergente", "data_pedido",
       ["data", "formato", "iso"], ["ausente", "nulo"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "10/09/2026", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="A data da reserva aparece como 'Invalid Date' na listagem."),
    _c("semt-5", 3, 3, "nulo_inesperado", "nome",
       ["nulo", "null", "nome"], ["ausente do contrato", "tipo"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"status": "Em Analise", "nome": null, "cpf": "11122233344"}]',
       sintoma="A saudacao da area do cliente mostra 'Ola, !' — o restante da pagina carrega."),
]

# ---------------------------------------------------------- CLASSE 4: traducao
CASOS += [
    _c("tra-1", 4, 2, "escala_ou_unidade_errada", "preco",
       ["escala", "centavo", "unidade", "100"], ["tipo", "ausente"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 8990, "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="Os precos aparecem cem vezes maiores: 'R$ 8.990,00' para a picanha.",
       observacao="No banco, tbprodutos.valor_produto do id 1 vale 89.90."),
    _c("tra-2", 4, 3, "chave_de_juncao_errada", "nome",
       ["juncao", "join", "cliente errado", "chave"], ["nulo", "ausente"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"status": "Em Analise", "nome": "Administrador", "cpf": "11122233344"}]',
       sintoma="A reserva do Cliente Teste aparece com o nome do Administrador.",
       observacao="tbusuarios: id 1 = admin/Administrador (sup), id 2 = 11122233344/Cliente Teste (cli)."),
    _c("tra-3", 4, 2, "chave_de_juncao_errada", "tipo",
       ["tipo", "categoria", "juncao", "join"], ["ausente", "nulo"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Bebidas", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="A picanha aparece filtrada dentro da categoria Bebidas.",
       observacao="tbprodutos.id_tipo_produto do id 1 aponta para tbtipos.id_tipo 1 = Carnes."),
    _c("tra-4", 4, 3, "contagem_inconsistente", None,
       ["contagem", "total", "inconsistent", "14"], ["ausente", "tipo"],
       requisicao="GET /api/produtos?pagina=1", status=200,
       contrato=CONTRATO_PRODUTO + " | envelope: {total: inteiro, itens: lista}",
       corpo='{"total": 14, "itens": [' + PRODUTO_OK + ']}',
       sintoma="A tela informa '14 produtos encontrados' mas exibe apenas 1 cartao."),
    _c("tra-5", 4, 3, "escala_ou_unidade_errada", "pessoas",
       ["pessoas", "unidade", "mesa", "escala"], ["nulo", "tipo"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 1, "data_pedido": "2026-09-10", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="A reserva foi feita para 4 pessoas mas a listagem mostra 1.",
       observacao="O POST que criou a reserva enviou pessoas=4; o banco gravou 4."),
]

# ----------------------------------------------------------- CLASSE 5: runtime
CASOS += [
    _c("run-1", 5, 1, "erro_interno_do_servidor", None,
       ["500", "erro interno", "servidor"], ["tipo", "ausente"],
       requisicao="GET /api/produtos", status=500, contrato=CONTRATO_PRODUTO,
       corpo='{"detail": "erro interno (fault injection)"}',
       sintoma="A aba de produtos via API mostra a mensagem de erro ao carregar."),
    _c("run-2", 5, 1, "tempo_de_resposta_excedido", None,
       ["timeout", "tempo", "excedid", "lenta"], ["500", "tipo"],
       requisicao="GET /api/produtos", status=None, contrato=CONTRATO_PRODUTO,
       corpo="(sem resposta apos 30s; conexao encerrada pelo cliente)",
       sintoma="A pagina fica carregando e depois exibe erro de rede."),
    _c("run-3", 5, 2, "limite_de_requisicoes", None,
       ["429", "limite", "requisic"], ["500", "timeout"],
       requisicao="GET /api/produtos", status=429, contrato=CONTRATO_PRODUTO,
       corpo='{"detail": "too many requests"}',
       sintoma="Ao recarregar a pagina varias vezes seguidas, a listagem para de carregar."),
    _c("run-4", 5, 3, "dado_desatualizado", None,
       ["cache", "desatualiz", "velho", "antig"], ["ausente", "tipo"],
       requisicao="POST /api/pedidos -> 201 | GET /api/pedidos?login=11122233344 -> 200",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='POST devolveu {"id_pedido": 8, "status": "Em Analise", "pessoas": 6}. '
             'GET seguinte devolveu [' + '{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}' + ']',
       sintoma="A reserva recem-criada nao aparece na lista; aparece so depois de alguns minutos.",
       observacao="O cabecalho da resposta do GET traz Age: 240 e Cache-Control: max-age=300."),
    _c("run-5", 5, 3, "registro_duplicado", None,
       ["duplicad", "duplicat", "repetid"], ["cache", "ausente"],
       requisicao="POST /api/pedidos (enviado uma vez) | GET /api/pedidos?login=11122233344",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 8, "pessoas": 6, "data_pedido": "2026-09-12", "status": "Em Analise", '
             '"nome": "Cliente Teste", "cpf": "11122233344"}, '
             '{"id_pedido": 9, "pessoas": 6, "data_pedido": "2026-09-12", "status": "Em Analise", '
             '"nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="O cliente ve duas reservas identicas apos confirmar uma unica vez."),
]

# ------------------------------------------------------------ CLASSE 6: efeito
CASOS += [
    _c("efe-1", 6, 1, "localizador_quebrado", None,
       ["seletor", "localizador", "elemento"], ["500", "tipo"],
       requisicao="(sem falha de rede) passo do roteiro: abrir detalhes da Picanha ao Alho",
       status=200, contrato="n/a",
       corpo="(nenhuma requisicao falhou)", arvore=ARVORE_CARTOES,
       seletor_quebrado="button.btn-detalhes",
       sintoma="O roteiro falha por tempo esgotado ao procurar o botao de detalhes."),
    _c("efe-2", 6, 2, "estado_da_tela_divergente", "status",
       ["tela", "estado", "divergen", "cancelad"], ["ausente", "timeout"],
       requisicao="POST /api/pedidos/7/cancelar -> 200 | tela do cliente", status=200,
       contrato=CONTRATO_PEDIDO,
       corpo='A API devolveu {"id_pedido": 7, "status": "Cancelado"}',
       sintoma="A tela continua exibindo a reserva 7 como 'Em Analise' apos o cancelamento."),
    _c("efe-3", 6, 2, "campo_ausente", "imagem",
       ["imagem", "ausente", "quebrad"], ["preco", "timeout"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 89.9, "destaque": true}]',
       sintoma="Os cartoes aparecem com o icone de imagem quebrada, mas nome e preco corretos."),
    _c("efe-4", 6, 3, "estado_da_tela_divergente", None,
       ["vazia", "lista", "filtro", "tela"], ["500", "timeout", "truncad"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[' + PRODUTO_OK + ']',
       sintoma="A API respondeu com 1 produto e sem erro, mas a listagem na tela aparece vazia.",
       observacao="Nao ha erro no console. O filtro de categoria estava com 'Bebidas' selecionado."),
    _c("efe-5", 6, 3, "localizador_quebrado", None,
       ["seletor", "localizador", "ambigu", "dois"], ["500", "ausente"],
       requisicao="(sem falha de rede) passo do roteiro: clicar em Saiba Mais da Picanha ao Alho",
       status=200, contrato="n/a",
       corpo="(nenhuma requisicao falhou)", arvore=ARVORE_CARTOES,
       seletor_quebrado="button.saiba-mais",
       sintoma="O roteiro falha porque o seletor encontrou dois elementos em vez de um."),
]
