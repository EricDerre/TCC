#!/usr/bin/env python3
# ! Alteração de IA - Revisar: completa o banco de casos até 90 (6 classes x 3 níveis x 5).
# ! Motivo: com 5 casos por classe, cada acerto ou erro valia 20 pontos percentuais no
# gráfico — resolução grossa demais para comparar modelos. Com 5 casos por célula
# (classe x nível), cada célula fica com granularidade de 20% mas a classe inteira cai
# para ~6,7%, que é o que torna a comparação por classe legível.
#
# As variações dentro de uma mesma classe trocam o campo, o endpoint e a entidade de
# propósito: isso mede se o modelo generaliza o tipo de falha ou se só reconhece o caso
# específico que já viu. Mesma origem dos dados dos casos base (schemas.py e
# schema_completo.sql).
from banco_casos import ARVORE_CARTOES, CONTRATO_PEDIDO, CONTRATO_PRODUTO, PRODUTO_OK, _c

CASOS_EXTRA = []

# ------------------------------------------------- CLASSE 1: lexica (faltam n1x2, n2x4, n3x4)
CASOS_EXTRA += [
    _c("lex-6", 1, 1, "corpo_nao_e_json", None, ["html", "nao e json"], ["campo", "cache"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='<!DOCTYPE html><html><head><title>404 Not Found</title></head></html>',
       sintoma="A area do cliente nao lista nenhuma reserva e o console acusa erro de parsing."),
    _c("lex-7", 1, 1, "corpo_vazio", None, ["vazio", "sem corpo"], ["truncad", "500"],
       requisicao="GET /api/produtos/1", status=204, contrato=CONTRATO_PRODUTO, corpo="",
       sintoma="A tela de detalhe abre em branco, sem mensagem de erro."),
    _c("lex-8", 1, 2, "codificacao_incorreta", "resumo",
       ["codifica", "acent", "encoding"], ["truncad", "nulo"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", '
             '"tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]',
       sintoma="A descricao aparece com simbolos no lugar dos acentos.",
       observacao="O cabecalho declara charset=utf-8 mas os bytes estao em latin-1."),
    _c("lex-9", 1, 2, "corpo_nao_e_json", None, ["xml", "nao e json"], ["campo", "tipo"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='<?xml version="1.0"?><produtos><produto><id>1</id></produto></produtos>',
       sintoma="A listagem nao carrega. O cabecalho diz application/json."),
    _c("lex-10", 1, 3, "resposta_truncada", None,
       ["truncad", "incomplet", "tamanho"], ["cache", "500"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[' + PRODUTO_OK + ', {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre',
       sintoma="A lista carrega parcialmente. So acontece quando ha mais de 10 produtos.",
       observacao="Content-Length declara 4096; o corpo recebido tem 4096 bytes exatos."),
    _c("lex-11", 1, 3, "codificacao_incorreta", "nome",
       ["codifica", "encoding", "duplo"], ["truncad", "ausente"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e acucar", '
             '"tipo": "Sobremesas", "preco": 14.9, "imagem": "abacaxi.jpg", "destaque": false}]',
       sintoma="Alguns nomes vem certos e outros com simbolos, no mesmo carregamento.",
       observacao="Os nomes corrompidos passaram por conversao de codificacao duas vezes."),
    _c("lex-12", 1, 3, "corpo_nao_e_json", None, ["html", "erro", "php"], ["timeout", "429"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='<b>Fatal error</b>: Allowed memory size exhausted<br />[' + PRODUTO_OK + ']',
       sintoma="Intermitente: as vezes a lista carrega, as vezes nao.",
       observacao="Quando falha, ha texto antes do JSON valido."),
]

# --------------------------------------------- CLASSE 2: sintatica (faltam n1x3, n2x3, n3x4)
CASOS_EXTRA += [
    _c("sin-6", 2, 1, "campo_ausente", "nome", ["nome", "ausente"], ["preco", "tipo"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, '
             '"imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="Os cartoes aparecem sem titulo."),
    _c("sin-7", 2, 1, "campo_ausente", "id_pedido", ["id_pedido", "ausente"], ["status", "nome"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", '
             '"nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="O botao de cancelar reserva nao funciona; nada acontece ao clicar."),
    _c("sin-8", 2, 1, "colecao_no_lugar_de_objeto", None, ["objeto", "lista"], ["ausente", "tipo"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO + " (lista)",
       corpo=PRODUTO_OK,
       sintoma="A listagem quebra ao tentar percorrer o resultado."),
    _c("sin-9", 2, 2, "campo_renomeado", "nome", ["renomead", "descricao", "nome"], ["ausente do banco"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "descricao": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="Os cartoes aparecem com titulo vazio, mas com preco e categoria corretos."),
    _c("sin-10", 2, 2, "campo_renomeado", "status", ["renomead", "situacao", "status"], ["domin"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"situacao": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="A coluna de situacao da reserva aparece vazia na area do cliente."),
    _c("sin-11", 2, 2, "estrutura_aninhada_divergente", None,
       ["envelope", "aninhad", "data"], ["ausente", "tipo"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO + " (lista na raiz)",
       corpo='{"data": {"itens": [' + PRODUTO_OK + ']}}',
       sintoma="A listagem fica vazia mesmo com a API respondendo com sucesso."),
    _c("sin-12", 2, 3, "campo_ausente", "cpf", ["cpf", "ausente", "alguns"], ["todos"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", '
             '"nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 8, "pessoas": 2, '
             '"data_pedido": "2026-09-15", "status": "Em Analise", "nome": "Cliente Teste"}]',
       sintoma="Uma das reservas do cliente some da tela; a outra aparece normalmente."),
    _c("sin-13", 2, 3, "estrutura_aninhada_divergente", "tipo",
       ["aninhad", "objeto", "inconsistent"], ["ausente"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[' + PRODUTO_OK + ', {"id": 2, "nome": "Fraldinha", "resumo": "Corte nobre", '
             '"tipo": {"id": 1, "nome": "Carnes"}, "preco": 69.9, "imagem": "fraldinha.jpg", '
             '"destaque": false}]',
       sintoma="Parte dos cartoes mostra a categoria e parte mostra [object Object]."),
    _c("sin-14", 2, 3, "campo_renomeado", "imagem", ["renomead", "imagem", "url"], ["ausente do banco"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 89.9, "imagem_url": "picanha_alho.jpg", "destaque": true}]',
       sintoma="Todos os cartoes mostram icone de imagem quebrada; o resto do dado esta certo."),
    _c("sin-15", 2, 3, "colecao_no_lugar_de_objeto", "tipo", ["lista", "tipo", "colec"], ["ausente"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": ["Carnes"], "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="A categoria aparece como 'Carnes' com colchetes ao redor no cartao."),
]

# --------------------------------------------- CLASSE 3: semantica (faltam n1x5, n2x1, n3x4)
CASOS_EXTRA += [
    _c("semt-6", 3, 1, "tipo_divergente", "id", ["id", "tipo", "texto"], ["ausente", "nulo"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": "1", "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="O link de detalhes do produto leva para uma pagina de produto nao encontrado."),
    _c("semt-7", 3, 1, "tipo_divergente", "pessoas", ["pessoas", "tipo", "texto"], ["ausente"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": "4", "data_pedido": "2026-09-10", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="A soma total de lugares reservados sai errada na tela administrativa."),
    _c("semt-8", 3, 1, "nulo_inesperado", "preco", ["nulo", "null", "preco"], ["ausente", "renomead"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": null, "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="O cartao exibe 'R$ 0,00' para um produto que custa 89,90."),
    _c("semt-9", 3, 1, "valor_fora_do_dominio", "destaque", ["destaque", "domin", "talvez"], ["tipo texto"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": 2}]',
       sintoma="O produto aparece na secao de destaques mesmo nao estando marcado no cadastro."),
    _c("semt-10", 3, 1, "tipo_divergente", "destaque", ["destaque", "tipo", "numero"], ["ausente"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": 1}]',
       sintoma="Todos os produtos aparecem como destaque na home."),
    _c("semt-11", 3, 2, "valor_fora_do_dominio", "status", ["status", "domin", "concluid"], ["tipo"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"status": "Concluido", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="O botao de cancelar some para essa reserva, sem motivo aparente."),
    _c("semt-12", 3, 3, "formato_de_data_divergente", "data_pedido",
       ["data", "formato", "timestamp"], ["nulo", "ausente"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": 1789084800, '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="A data da reserva aparece como 1789084800 na listagem."),
    _c("semt-13", 3, 3, "tipo_divergente", "preco", ["preco", "tipo", "virgula"], ["ausente"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": "89,90", "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="O cartao mostra 'R$ NaN'. Outros produtos com preco inteiro aparecem certos.",
       observacao="O separador decimal veio como virgula, no formato brasileiro."),
    _c("semt-14", 3, 3, "nulo_inesperado", "tipo", ["nulo", "tipo", "categoria"], ["ausente do contrato"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[' + PRODUTO_OK + ', {"id": 8, "nome": "Agua Mineral", "resumo": "500ml", '
             '"tipo": null, "preco": 6.0, "imagem": "agua.png", "destaque": false}]',
       sintoma="O filtro por categoria deixa de listar alguns produtos que existem no cadastro."),
    _c("semt-15", 3, 3, "valor_fora_do_dominio", "pessoas", ["pessoas", "domin", "negativ", "zero"], ["nulo"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 0, "data_pedido": "2026-09-10", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="A reserva aparece na lista mas o restaurante nao consegue alocar mesa para ela.",
       observacao="O formulario exige minimo de 1 pessoa (input com min=1)."),
]

# ---------------------------------------------- CLASSE 4: traducao (faltam n1x5, n2x3, n3x2)
CASOS_EXTRA += [
    _c("tra-6", 4, 1, "escala_ou_unidade_errada", "preco", ["escala", "divid", "unidade"], ["tipo"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 0.899, "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="Todos os precos aparecem cem vezes menores: 'R$ 0,90' para a picanha."),
    _c("tra-7", 4, 1, "chave_de_juncao_errada", "id", ["id", "juncao", "troca"], ["ausente"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Carnes", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="O titulo do cartao mostra o nome da categoria em vez do nome do produto.",
       observacao="tbprodutos.descri_produto do id 1 e 'Picanha ao Alho'; 'Carnes' e o rotulo_tipo."),
    _c("tra-8", 4, 1, "contagem_inconsistente", None, ["contagem", "total", "zero"], ["vazio", "500"],
       requisicao="GET /api/produtos?pagina=1", status=200,
       contrato=CONTRATO_PRODUTO + " | envelope: {total: inteiro, itens: lista}",
       corpo='{"total": 0, "itens": [' + PRODUTO_OK + ']}',
       sintoma="A tela informa 'Nenhum produto encontrado' mas exibe cartoes."),
    _c("tra-9", 4, 1, "escala_ou_unidade_errada", "data_pedido",
       ["data", "fuso", "unidade", "dia"], ["formato invalido"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-09", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="A reserva aparece sempre um dia antes do que o cliente escolheu.",
       observacao="O cliente reservou para 2026-09-10; o banco gravou 2026-09-10."),
    _c("tra-10", 4, 1, "chave_de_juncao_errada", "cpf", ["cpf", "juncao", "cliente"], ["nulo"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "admin"}]',
       sintoma="A reserva do cliente aparece vinculada ao login do administrador."),
    _c("tra-11", 4, 2, "contagem_inconsistente", None, ["contagem", "total", "pagina"], ["cache"],
       requisicao="GET /api/produtos?pagina=2", status=200,
       contrato=CONTRATO_PRODUTO + " | envelope: {total: inteiro, itens: lista}",
       corpo='{"total": 14, "itens": []}',
       sintoma="A segunda pagina da listagem aparece vazia, mesmo havendo 14 produtos."),
    _c("tra-12", 4, 2, "escala_ou_unidade_errada", "preco", ["preco", "arredond", "escala"], ["tipo"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 90, "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="Os precos aparecem arredondados; o total da comanda nao fecha com o cadastro.",
       observacao="tbprodutos.valor_produto e DECIMAL(9,2) e vale 89.90 para o id 1."),
    _c("tra-13", 4, 2, "chave_de_juncao_errada", "imagem", ["imagem", "troca", "juncao"], ["ausente"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 89.9, "imagem": "agua.png", "destaque": true}]',
       sintoma="Os cartoes carregam a imagem de outro produto.",
       observacao="tbprodutos.imagem_produto do id 1 e 'picanha_alho.jpg'."),
    _c("tra-14", 4, 3, "contagem_inconsistente", None, ["contagem", "destaque", "total"], ["ausente"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='(14 itens; 5 com destaque=true)',
       sintoma="A home informa '4 destaques' mas renderiza 5 cartoes na secao.",
       observacao="No banco, 5 produtos tem destaque_produto = 'Sim'."),
    _c("tra-15", 4, 3, "escala_ou_unidade_errada", "pessoas", ["pessoas", "escala", "dobr"], ["nulo"],
       requisicao="POST /api/pedidos (pessoas=4) -> GET /api/pedidos", status=200,
       contrato=CONTRATO_PEDIDO,
       corpo='POST enviou {"pessoas": 4}; GET devolveu [{"id_pedido": 8, "pessoas": 8, '
             '"data_pedido": "2026-09-12", "status": "Em Analise", "nome": "Cliente Teste", '
             '"cpf": "11122233344"}]',
       sintoma="A reserva confirmada mostra o dobro de pessoas do que foi solicitado."),
]

# ----------------------------------------------- CLASSE 5: runtime (faltam n1x3, n2x4, n3x3)
CASOS_EXTRA += [
    _c("run-6", 5, 1, "erro_interno_do_servidor", None, ["500", "erro interno"], ["429", "timeout"],
       requisicao="POST /api/pedidos", status=500, contrato=CONTRATO_PEDIDO,
       corpo='{"detail": "Internal Server Error"}',
       sintoma="A confirmacao da reserva falha com mensagem generica de erro."),
    _c("run-7", 5, 1, "recurso_inexistente", None, ["404", "inexistent", "nao encontrad"], ["500"],
       requisicao="GET /api/produtos/999", status=404, contrato=CONTRATO_PRODUTO,
       corpo='{"detail": "produto nao encontrado"}',
       sintoma="O link de detalhes de um produto leva a uma pagina de erro."),
    _c("run-8", 5, 1, "recurso_inexistente", None, ["404", "rota", "endpoint"], ["500", "timeout"],
       requisicao="GET /api/produto", status=404, contrato=CONTRATO_PRODUTO,
       corpo='{"detail": "Not Found"}',
       sintoma="A aba de produtos via API nunca carrega nada.",
       observacao="O endpoint correto e /api/produtos, no plural."),
    _c("run-9", 5, 2, "tempo_de_resposta_excedido", None, ["lenta", "tempo", "latenc"], ["500", "429"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[' + PRODUTO_OK + '] (recebido apos 9,4 s)',
       sintoma="A listagem carrega, mas demora quase 10 segundos.",
       observacao="O mesmo endpoint respondia em 120 ms na semana anterior."),
    _c("run-10", 5, 2, "limite_de_requisicoes", None, ["429", "limite"], ["500", "cache"],
       requisicao="GET /api/produtos (12a requisicao em 1 min)", status=429,
       contrato=CONTRATO_PRODUTO,
       corpo='{"detail": "rate limit exceeded", "retry_after": 30}',
       sintoma="Durante a execucao do roteiro de teste, a partir de certo ponto tudo falha."),
    _c("run-11", 5, 2, "dado_desatualizado", "status", ["cache", "desatualiz"], ["ausente"],
       requisicao="POST /api/pedidos/7/cancelar -> 200 | GET /api/pedidos?login=11122233344",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='POST confirmou status Cancelado. GET devolveu status "Em Analise".',
       sintoma="A reserva cancelada volta a aparecer como ativa ao recarregar a pagina."),
    _c("run-12", 5, 2, "erro_interno_do_servidor", None, ["500", "intermitent"], ["429"],
       requisicao="GET /api/produtos (1 em cada 3 tentativas)", status=500,
       contrato=CONTRATO_PRODUTO, corpo='{"detail": "erro interno"}',
       sintoma="A listagem falha de forma intermitente, sem padrao de horario."),
    _c("run-13", 5, 3, "registro_duplicado", None, ["duplicad", "reenvio", "repetid"], ["cache"],
       requisicao="POST /api/pedidos (clique duplo no botao)", status=201, contrato=CONTRATO_PEDIDO,
       corpo='Duas respostas 201, com id_pedido 8 e 9, mesmos dados.',
       sintoma="O cliente reclama de cobranca em duplicidade da mesma reserva."),
    _c("run-14", 5, 3, "dado_desatualizado", None, ["cache", "desatualiz", "produto novo"], ["404"],
       requisicao="POST admin cadastra produto -> GET /api/produtos", status=200,
       contrato=CONTRATO_PRODUTO,
       corpo='GET devolveu 14 itens; o produto recem-cadastrado (id 15) nao esta na lista.',
       sintoma="Produto cadastrado pelo painel nao aparece na aba de API por varios minutos.",
       observacao="O painel PHP mostra o produto imediatamente; so a API atrasa."),
    _c("run-15", 5, 3, "tempo_de_resposta_excedido", None, ["timeout", "lent", "volume"], ["500"],
       requisicao="GET /api/produtos", status=None, contrato=CONTRATO_PRODUTO,
       corpo='(conexao encerrada por tempo esgotado apos 30 s)',
       sintoma="A listagem so falha quando ha mais de 200 produtos cadastrados.",
       observacao="Com 14 produtos o mesmo endpoint responde em 120 ms."),
]

# ------------------------------------------------ CLASSE 6: efeito (faltam n1x4, n2x3, n3x3)
CASOS_EXTRA += [
    _c("efe-6", 6, 1, "localizador_quebrado", None, ["seletor", "localizador", "classe"], ["500"],
       requisicao="(sem falha de rede) passo: clicar no botao de detalhes", status=200,
       contrato="n/a", corpo="(nenhuma requisicao falhou)", arvore=ARVORE_CARTOES,
       seletor_quebrado="#btnDetalhes",
       sintoma="O roteiro falha por tempo esgotado ao procurar o elemento pelo identificador."),
    _c("efe-7", 6, 1, "localizador_quebrado", None, ["seletor", "texto", "rotulo"], ["timeout de rede"],
       requisicao="(sem falha de rede) passo: clicar em 'Ver mais'", status=200,
       contrato="n/a", corpo="(nenhuma requisicao falhou)", arvore=ARVORE_CARTOES,
       seletor_quebrado="text=Ver mais",
       sintoma="O roteiro nao encontra o botao; na tela o texto e 'Saiba Mais...'."),
    _c("efe-8", 6, 1, "estado_da_tela_divergente", None, ["tela", "vazia", "estado"], ["500", "404"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[' + PRODUTO_OK + ']',
       sintoma="A API respondeu 1 produto com sucesso, mas a tela mostra 'Carregando...' parado."),
    _c("efe-9", 6, 1, "localizador_quebrado", None, ["seletor", "atributo", "data-id"], ["500"],
       requisicao="(sem falha de rede) passo: abrir detalhes do produto 1", status=200,
       contrato="n/a", corpo="(nenhuma requisicao falhou)", arvore=ARVORE_CARTOES,
       seletor_quebrado="button[data-produto='1']",
       sintoma="O roteiro nao localiza o botao; o atributo presente na pagina e data-id."),
    _c("efe-10", 6, 2, "estado_da_tela_divergente", "preco", ["tela", "preco", "divergen"], ["ausente"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='[' + PRODUTO_OK + ']',
       sintoma="A API devolveu preco 89.9, mas o cartao exibe 'R$ 0,00'.",
       observacao="Nao ha erro no console; o dado chegou correto na rede."),
    _c("efe-11", 6, 2, "estado_da_tela_divergente", None, ["ordem", "tela", "divergen"], ["500"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='(14 itens, na ordem de id 1 a 14)',
       sintoma="Os cartoes aparecem em ordem aleatoria a cada recarregamento da pagina."),
    _c("efe-12", 6, 2, "localizador_quebrado", None, ["seletor", "ambigu", "dois", "unico"], ["ausente"],
       requisicao="(sem falha de rede) passo: clicar no primeiro botao de preco", status=200,
       contrato="n/a", corpo="(nenhuma requisicao falhou)", arvore=ARVORE_CARTOES,
       seletor_quebrado="button[disabled]",
       sintoma="O roteiro falha porque o seletor casou com dois botoes de preco."),
    _c("efe-13", 6, 3, "estado_da_tela_divergente", None, ["tela", "duplicad", "acumul"], ["500", "cache"],
       requisicao="GET /api/produtos (chamado duas vezes)", status=200, contrato=CONTRATO_PRODUTO,
       corpo='(14 itens em cada uma das duas respostas)',
       sintoma="A listagem mostra 28 cartoes, com cada produto repetido duas vezes.",
       observacao="A pagina nao limpa o container antes de renderizar a segunda resposta."),
    _c("efe-14", 6, 3, "localizador_quebrado", None, ["seletor", "ordem", "posic", "indice"], ["500"],
       requisicao="(sem falha de rede) passo: clicar no botao do segundo cartao", status=200,
       contrato="n/a", corpo="(nenhuma requisicao falhou)", arvore=ARVORE_CARTOES,
       seletor_quebrado="div.thumbnail:nth-child(3) button.saiba-mais",
       sintoma="O roteiro funciona em alguns dias e falha em outros.",
       observacao="A ordem dos produtos na resposta nao e garantida pela API."),
    _c("efe-15", 6, 3, "estado_da_tela_divergente", "status", ["tela", "status", "estado"], ["cache"],
       requisicao="POST /api/pedidos/7/cancelar -> 200 | tela permanece aberta", status=200,
       contrato=CONTRATO_PEDIDO,
       corpo='A API confirmou {"id_pedido": 7, "status": "Cancelado"}',
       sintoma="O botao de cancelar continua habilitado e a reserva segue como ativa na tela.",
       observacao="Recarregando a pagina, o estado aparece correto."),
]

# --- fecha a grade da classe 1 (faltavam 2 casos de nivel 2 e 1 de nivel 3) ---
CASOS_EXTRA += [
    _c("lex-13", 1, 2, "corpo_vazio", None, ["vazio", "sem corpo", "branco"], ["truncad", "404"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo="   ",
       sintoma="A area do cliente mostra a tabela de reservas sem nenhuma linha, sem erro."),
    _c("lex-14", 1, 2, "resposta_truncada", None, ["truncad", "incomplet"], ["vazio", "500"],
       requisicao="GET /api/pedidos?login=11122233344", status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "sta',
       sintoma="A listagem de reservas nao renderiza e o console acusa fim inesperado da entrada."),
    _c("lex-15", 1, 3, "corpo_nao_e_json", None, ["html", "proxy", "nao e json"], ["timeout", "429"],
       requisicao="GET /api/produtos", status=200, contrato=CONTRATO_PRODUTO,
       corpo='<html><head><title>Gateway</title></head><body>Servico indisponivel</body></html>',
       sintoma="Falha so quando acessado de fora da rede local; dentro da rede funciona.",
       observacao="O cabecalho Content-Type continua dizendo application/json."),
]
