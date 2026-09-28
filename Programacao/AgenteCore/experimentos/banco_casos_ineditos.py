#!/usr/bin/env python3
# ! Alteração de IA - Revisar: banco de 36 casos inéditos (2 por classe x nível, classes
# 1-6, níveis 1-3 de taxonomia.py) para o teste "casos inéditos" da Fase 3-B — ids
# lex/sin/semt/tra/run/efe de 16 a 21, continuando a numeração dos 90 casos de
# banco_casos.py/banco_casos_extra.py (que vão até 15 em cada classe).
# ! Motivo: a Fase 3-B mede generalização, não memorização — os 90 casos foram usados nas
# Fases 2-A, 2-B e 3 (os 54 de aprendizado geraram as edições da biblioteca, e os 36 de
# avaliação foram vistos em quatro passadas por modelo), então testar de novo com eles não
# provaria nada sobre um caso nunca visto. Por regra do pedido que criou este arquivo, os
# cenários abaixo vêm só da leitura de CobaiaAPI/app/**, CobaiaFront/produtos_api.php e
# CobaiaFront/banco/*.sql (nunca de resultados_alvo/, base_conhecimento/, Documentacao/,
# claude-memoria/ ou notas/JSON/JSONL de experimentos/) — ler esses outros lugares
# contaminaria o teste, porque ele mede se o modelo generaliza para o que nunca viu.
"""
36 casos inéditos (2 por classe x nível de taxonomia.py) para a Fase 3-B. Mesma função
_c(...) e mesmas constantes de banco_casos.py que banco_casos_extra.py usa, mesmo formato
de gabarito (causa_raiz, campo_afetado, termos_esperados, termos_proibidos).

Cada caso vem com um comentário "fonte:" citando o arquivo/linha do cobaia (CobaiaAPI ou
CobaiaFront) que sustenta o sintoma descrito — a lição do banco atual é que descrever um
sintoma que o código real não produz invalida o caso (foi o que aconteceu com 4 fixtures
antigos sobre produtos_api.php, corrigidos em banco_casos.py/banco_casos_extra.py).

Como GET/POST /api/pedidos e /api/pedidos/{id}/cancelar não são consumidos por nenhuma
página do CobaiaFront (só produtos_api.php chama a CobaiaAPI — confirmado por busca em
todo o CobaiaFront por "fetch("/"8000"/"api/produtos"/"api/pedidos"), os casos que usam
esses dois endpoints descrevem o sintoma no nível da resposta/contrato (o que a chamada
devolve), não como uma tela específica reagiria — não existe tela para citar com verdade.
Os casos de /api/produtos e /api/produtos/{id} (via o modal "Saiba Mais..." de
produtos_api.php), por outro lado, descrevem o efeito visível real nessa página.
"""
from banco_casos import ARVORE_CARTOES, CONTRATO_PEDIDO, CONTRATO_PRODUTO, PRODUTO_OK, _c

CASOS_INEDITOS = []

# ------------------------------------------------------------- CLASSE 1: lexica
# Família de causas (igual aos 90): resposta_truncada, corpo_nao_e_json, corpo_vazio,
# codificacao_incorreta — "o corpo da resposta é sequer legível?".
CASOS_INEDITOS += [
    # fonte: CobaiaAPI/app/routers/produtos.py:19 (_MALFORMED_BODY) e :48-49
    # (obter_produto devolve esse texto quebrado quando state.mode == "malformed_json",
    # o mesmo texto de listar_produtos:36-37); CobaiaFront/produtos_api.php:115-124 (fetch
    # do modal: resp.ok é True em status 200, então cai em resp.json(), que estoura) e
    # :125-129 (catch escreve "Erro" no título e err.message no corpo do modal).
    _c("lex-16", 1, 1, "resposta_truncada", None,
       ["truncad", "incomplet", "nao e json"], ["timeout", "500"],
       requisicao="GET /api/produtos/1 (modo malformed_json ligado)",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "resposta truncada de propos',
       sintoma="Ao clicar em 'Saiba Mais...' da Picanha ao Alho, o modal abre mostrando "
               "'Erro' no titulo e uma mensagem de erro de interpretacao do JSON no "
               "corpo, mesmo com a resposta chegando em 200."),
    # fonte: CobaiaAPI/app/routers/pedidos.py:46-66 (criar_pedido — contrato normal
    # devolve JSONResponse(content=data, status_code=201) com o dict do pedido criado).
    _c("lex-17", 1, 1, "corpo_vazio", None,
       ["vazio", "sem corpo"], ["truncad", "404"],
       requisicao="POST /api/pedidos",
       status=201, contrato=CONTRATO_PEDIDO, corpo="",
       sintoma="A resposta de POST /api/pedidos chega com status 201 (Criado) mas corpo "
               "completamente vazio; o pedido recem-criado nao vem em lugar nenhum da "
               "resposta."),
    # fonte: CobaiaFront/produtos_api.php:78 (renderiza p.resumo cru no card, sem tratar
    # encoding) e CobaiaAPI/app/routers/produtos.py:26 (_to_dict, campo resumo);
    # CobaiaFront/banco/seed.sql:24 (id 8, resumo real "Garrafa 500ml, com ou sem gás").
    _c("lex-18", 1, 2, "codificacao_incorreta", "resumo",
       ["codifica", "encoding", "acent"], ["ausente", "renomead"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem '
             'gÃ¡s", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", '
             '"destaque": false}]',
       sintoma="O card da Agua Mineral mostra o resumo como 'Garrafa 500ml, com ou sem "
               "gÃ¡s'; o nome do produto, logo acima no mesmo card, aparece com o "
               "acento certo ('Água').",
       observacao="So o campo resumo veio com os bytes trocados; nome, no mesmo item, "
                   "chegou certo — nao e um problema de charset da resposta inteira."),
    # fonte: CobaiaAPI/app/routers/pedidos.py:69-82 (cancelar_pedido — contrato normal
    # devolve o JSON do pedido atualizado); mesma familia de falha de transporte que
    # lex-2/lex-6/lex-12/lex-15 ja usam (HTML no lugar do JSON esperado), aqui num
    # endpoint novo (cancelamento, nao listagem).
    _c("lex-19", 1, 2, "corpo_nao_e_json", None,
       ["html", "nao e json"], ["500", "timeout"],
       requisicao="POST /api/pedidos/7/cancelar",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='<html><head><title>500 Internal Server Error</title></head>'
             '<body><h1>Internal Server Error</h1></body></html>',
       sintoma="A resposta de POST /api/pedidos/7/cancelar chega com status 200 e "
               "Content-Type application/json, mas o corpo e uma pagina HTML de erro; "
               "nao da pra confirmar se a reserva foi cancelada de fato."),
    # fonte: CobaiaAPI/app/routers/pedidos.py:30-43 (listar_pedidos — contrato normal
    # serializa todos os itens da lista, um por um, sem limite de tamanho).
    _c("lex-20", 1, 3, "resposta_truncada", None,
       ["truncad", "incomplet", "cortad"], ["vazio", "500"],
       requisicao="GET /api/pedidos?login=11122233344",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}, '
             '{"id_pedido": 8, "pessoas": 2, "data_pedido": "2026-09-15", "sta',
       sintoma="Quando o cliente tem mais de uma reserva, a segunda vem cortada no "
               "meio (a primeira sempre chega inteira); com uma reserva so, a resposta "
               "sempre chega completa.",
       observacao="O Content-Length declarado no cabecalho bate com o tamanho do corpo "
                   "recebido — nao e uma conexao interrompida no meio do caminho."),
    # fonte: CobaiaAPI/app/models.py:60 (Enum "Em Análise"/"Cancelado" — valor literal
    # com acento) e app/routers/pedidos.py:24 (_to_dict, campo status).
    _c("lex-21", 1, 3, "codificacao_incorreta", "status",
       ["codifica", "encoding", "acent"], ["ausente", "domin"],
       requisicao="GET /api/pedidos?login=11122233344",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"status": "Em AnÃ¡lise", "nome": "Cliente Teste", "cpf": "11122233344"}, '
             '{"id_pedido": 8, "pessoas": 2, "data_pedido": "2026-09-15", '
             '"status": "Em Análise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="Na mesma resposta de GET /api/pedidos, a reserva 7 traz status "
               "'Em AnÃ¡lise' com simbolo no lugar do acento, e a reserva 8 (mesmo "
               "cliente, mesma consulta) traz 'Em Análise' certinho.",
       observacao="As duas reservas foram gravadas pelo mesmo formulario "
                   "(cliente/registrar_reserva.php), na mesma tabela tbpedido_reserva."),
]

# ---------------------------------------------------------- CLASSE 2: sintatica
# Família de causas (igual aos 90): campo_ausente, campo_renomeado,
# estrutura_aninhada_divergente, colecao_no_lugar_de_objeto — "a forma da resposta bate
# com a esperada?".
CASOS_INEDITOS += [
    # fonte: CobaiaAPI/tests/test_fault_injection.py:42-44 (test_field_missing_chega_ao_
    # fio testa exatamente este cenario: field_missing em "destaque" via GET
    # /api/produtos/1) e app/schemas.py:23 (ProdutoOut.destaque: bool, campo obrigatorio,
    # sem Optional); CobaiaFront/produtos_api.php:120-124 (o modal so le p.nome/p.resumo).
    _c("sin-16", 2, 1, "campo_ausente", "destaque",
       ["destaque", "ausente"], ["preco", "tipo"],
       requisicao="GET /api/produtos/1 (modo field_missing, campo destaque)",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg"}',
       sintoma="A resposta de GET /api/produtos/1 deixa de trazer o campo destaque; o "
               "modal 'Saiba Mais...' (que so le nome e resumo) continua abrindo "
               "normal, mas o campo e obrigatorio no contrato (ProdutoOut.destaque: "
               "bool, sem valor default)."),
    # fonte: CobaiaAPI/app/routers/pedidos.py:26 (_to_dict, "cpf": p.cliente.login_
    # usuario — o nome de campo real no contrato).
    _c("sin-17", 2, 1, "campo_renomeado", "cpf",
       ["renomead", "documento", "cpf"], ["ausente do banco", "tipo"],
       requisicao="GET /api/pedidos?login=11122233344",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"status": "Em Analise", "nome": "Cliente Teste", "documento": "11122233344"}]',
       sintoma="A resposta de GET /api/pedidos traz o campo documento no lugar de cpf; "
               "quem le o contrato antigo (CONTRATO_PEDIDO) nao encontra a chave cpf em "
               "lugar nenhum do item."),
    # fonte: CobaiaAPI/app/schemas.py:30 (PedidoOut.status: str) e app/routers/
    # pedidos.py:24 (_to_dict, "status": p.status — string simples no caminho normal).
    _c("sin-18", 2, 2, "estrutura_aninhada_divergente", "status",
       ["objeto", "aninhad", "status"], ["ausente", "nulo"],
       requisicao="GET /api/pedidos?login=11122233344",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"status": {"codigo": "EA", "descricao": "Em Analise"}, '
             '"nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="O campo status de cada reserva chega como objeto ({'codigo': ..., "
               "'descricao': ...}) em vez do texto simples que o contrato descreve; "
               "comparar direto com 'Em Analise'/'Cancelado' nunca bate."),
    # fonte: CobaiaAPI/app/routers/pedidos.py:69-82 (cancelar_pedido — devolve
    # JSONResponse(content=data) onde data e um dict UNICO, nunca uma lista).
    _c("sin-19", 2, 2, "colecao_no_lugar_de_objeto", None,
       ["lista", "objeto", "colec"], ["tipo", "nulo"],
       requisicao="POST /api/pedidos/7/cancelar",
       status=200, contrato=CONTRATO_PEDIDO + " (recurso unico, nao lista)",
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"status": "Cancelado", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="A resposta de POST /api/pedidos/7/cancelar vem como lista com um item, "
               "em vez do objeto unico que o contrato descreve; ler resposta.status "
               "direto da undefined."),
    # fonte: CobaiaFront/produtos_api.php:82 (data-id="' + p.id + '" no botao "Saiba "
    # "Mais...") e :112-119 (o clique le esse atributo e usa no fetch); CobaiaAPI/app/
    # routers/produtos.py:46 (produto_id: int — "undefined" nao passa na validacao "
    # "automatica da rota, vira 422, capturado pelo catch do modal, produtos_api.php:
    # 125-129).
    _c("sin-20", 2, 3, "campo_ausente", "id",
       ["id", "ausente", "undefined"], ["preco", "tipo"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[' + PRODUTO_OK + ', {"nome": "Fraldinha", "resumo": "Corte grelhado na '
             'brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, '
             '"imagem": "fraldinha.jpg", "destaque": false}]',
       sintoma='O card da Fraldinha aparece normal, com nome, preco e imagem certos, '
               'mas o botao \'Saiba Mais...\' fica com data-id="undefined"; clicar '
               "nele abre o modal mostrando 'Erro'.",
       observacao="So o segundo item da resposta nao traz id; o primeiro (Picanha ao "
                   "Alho) esta completo."),
    # fonte: CobaiaFront/produtos_api.php:77 (typeof p.tipo === "object" ? "
    # "JSON.stringify(p.tipo) : p.tipo — para uma STRING que por acaso contem texto "
    # "parecido com JSON, typeof e "string", entao o card imprime o texto cru) e
    # CobaiaAPI/app/routers/produtos.py:27 (_to_dict, tipo: p.tipo.rotulo_tipo,
    # normalmente string simples, nunca serializada de novo).
    _c("sin-21", 2, 3, "estrutura_aninhada_divergente", "tipo",
       ["aninhad", "serializad", "string"], ["ausente", "object object"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "{\'id\': 1, \'nome\': \'Carnes\'}", "preco": 89.9, '
             '"imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="A categoria do produto aparece como o texto literal {'id': 1, 'nome': "
               "'Carnes'} no card (aspas simples, no estilo de repr do Python), em vez "
               "de 'Carnes' — diferente de um objeto de verdade, que apareceria como "
               "[object Object].",
       observacao="tipo e uma STRING cujo conteudo por acaso parece um dicionario "
                   "serializado errado (aspas simples); nao e um objeto JSON aninhado "
                   "de verdade, por isso o card nao mostra [object Object]."),
]

# ---------------------------------------------------------- CLASSE 3: semantica
# Família de causas (igual aos 90): tipo_divergente, valor_fora_do_dominio,
# formato_de_data_divergente, nulo_inesperado — "os tipos e os dominios fazem sentido?".
CASOS_INEDITOS += [
    # fonte: CobaiaFront/produtos_api.php:77 (numero nao e "object", entao o card "
    # "imprime p.tipo cru) e CobaiaAPI/app/routers/produtos.py:27 (_to_dict, tipo: "
    # "p.tipo.rotulo_tipo, sempre string no caminho normal).
    _c("semt-16", 3, 1, "tipo_divergente", "tipo",
       ["tipo", "numero", "texto"], ["ausente", "aninhad"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": 1, "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="A categoria do produto aparece como o numero 1 no card, no lugar de "
               "'Carnes'."),
    # fonte: CobaiaFront/produtos_api.php:82 (data-id) — CONTRATO_PRODUTO declara "id: "
    # "inteiro", sem "|nulo"; CobaiaAPI/app/routers/produtos.py:46 (produto_id: int — "
    # ""null" tambem falha na validacao automatica da rota, 422, igual ao sin-20 mas "
    # "com valor nulo em vez de ausente).
    _c("semt-17", 3, 1, "nulo_inesperado", "id",
       ["nulo", "null", "id"], ["ausente do contrato", "tipo"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[' + PRODUTO_OK + ', {"id": null, "nome": "Fraldinha", "resumo": "Corte '
             'grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, '
             '"imagem": "fraldinha.jpg", "destaque": false}]',
       sintoma='O card da Fraldinha mostra nome, preco e imagem certos, mas o botao '
               '\'Saiba Mais...\' fica com data-id="null"; ao clicar, o modal abre '
               "mostrando 'Erro'."),
    # fonte: CobaiaAPI/app/fault_injection.py:79-80 (type_drift: data[field] =
    # str(data[field]) — str() do Python, nao json.dumps) e CobaiaFront/produtos_
    # api.php:70 (comparacao estrita p.destaque === true / === false; qualquer string
    # cai no else e vira String(p.destaque)).
    _c("semt-18", 3, 2, "tipo_divergente", "destaque",
       ["destaque", "tipo", "boolean"], ["ausente", "renomead"],
       requisicao="GET /api/produtos (modo type_drift, campo destaque)",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", '
             '"destaque": "True"}]',
       sintoma="O rotulo do card mostra 'destaque: True' (em ingles, T maiusculo) no "
               "lugar de 'Sim' ou 'Nao'.",
       observacao="O modo type_drift converte o valor com str() do Python, que gera "
                   "'True'/'False' com maiuscula — diferente de 'true'/'false' do JSON "
                   "e de 'Sim'/'Nao' do dominio do produto."),
    # fonte: CobaiaAPI/app/schemas.py:29 (PedidoOut.data_pedido: date, sem hora) e
    # app/models.py:59 (data_pedido: Mapped[date] = mapped_column(Date) — coluna DATE,
    # sem componente de hora, no banco).
    _c("semt-19", 3, 2, "formato_de_data_divergente", "data_pedido",
       ["data", "formato", "hora"], ["nulo", "ausente"],
       requisicao="GET /api/pedidos?login=11122233344",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10T00:00:00Z", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="O campo data_pedido chega como '2026-09-10T00:00:00Z' (data e hora, "
               "com Z de UTC) em vez do formato so-data (AAAA-MM-DD) do contrato; quem "
               "espera so a data tem que lidar com hora e fuso que nao deveriam "
               "estar ali."),
    # fonte: CobaiaFront/produtos_api.php:64-67 (formatarPreco: Number(-10) nao e NaN,
    # entao formata normal como "R$ -10,00" — nao ha checagem de sinal) e CobaiaAPI/
    # app/models.py:34 (valor_produto: DECIMAL(9,2), sem constraint de nao-negativo).
    _c("semt-20", 3, 3, "valor_fora_do_dominio", "preco",
       ["preco", "negativ", "domin"], ["tipo", "ausente"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "Carnes", "preco": -10, "imagem": "picanha_alho.jpg", '
             '"destaque": true}]',
       sintoma="O botao de preco da Picanha ao Alho mostra 'R$ -10,00'; o tipo do "
               "campo esta certo (numero), so o valor que nao faz sentido pra um "
               "preco."),
    # fonte: CobaiaFront/produtos_api.php:76 ((p.nome || '(sem nome)') — string vazia e
    # falsy em JS, cai no texto fixo de reserva, igual a nome ausente ou nulo).
    _c("semt-21", 3, 3, "valor_fora_do_dominio", "nome",
       ["nome", "vazio", "domin"], ["ausente do contrato", "tipo"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "", "resumo": "Picanha grelhada", "tipo": "Carnes", '
             '"preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]',
       sintoma="O card mostra o texto literal '(sem nome)' no lugar do nome do "
               "produto; o campo nome e do tipo certo (texto), so que vazio."),
]

# ---------------------------------------------------------- CLASSE 4: traducao
# Família de causas (igual aos 90): escala_ou_unidade_errada, chave_de_juncao_errada,
# contagem_inconsistente — "o mapeamento entre as camadas esta correto?".
CASOS_INEDITOS += [
    # fonte: CobaiaAPI/app/routers/pedidos.py:22 (_to_dict, "pessoas": p.pessoas — sem
    # nenhuma conversao) e CobaiaFront/cliente/registrar_reserva.php:55 (input pessoas,
    # gravado direto, sem conversao pra mesas).
    _c("tra-16", 4, 1, "escala_ou_unidade_errada", "pessoas",
       ["pessoas", "unidade", "escala", "mesa"], ["nulo", "tipo"],
       requisicao="GET /api/pedidos?login=11122233344",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 2, "data_pedido": "2026-09-10", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="A resposta de GET /api/pedidos traz pessoas=2 pra uma reserva que o "
               "cliente fez pra 8 pessoas; o numero bate com quantidade de mesas (a 4 "
               "lugares cada), nao com pessoas.",
       observacao="O formulario de reserva (cliente/registrar_reserva.php) grava o "
                   "numero de pessoas direto, sem nenhuma conversao pra mesas."),
    # fonte: CobaiaAPI/app/models.py:22-24 (Tipo com sigla_tipo e rotulo_tipo, colunas
    # separadas) e app/routers/produtos.py:27 (_to_dict usa p.tipo.rotulo_tipo, nao
    # sigla_tipo); CobaiaFront/banco/seed.sql:11 (id_tipo 1: sigla 'CAR', rotulo
    # 'Carnes').
    _c("tra-17", 4, 1, "chave_de_juncao_errada", "tipo",
       ["tipo", "juncao", "sigla", "rotulo"], ["ausente", "nulo"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", '
             '"tipo": "CAR", "preco": 89.9, "imagem": "picanha_alho.jpg", '
             '"destaque": true}]',
       sintoma="A categoria da Picanha ao Alho aparece como 'CAR' no card, em vez de "
               "'Carnes'.",
       observacao="tbtipos.id 1 tem sigla_tipo='CAR' e rotulo_tipo='Carnes'; o "
                   "contrato usa o rotulo, nao a sigla."),
    # fonte: CobaiaAPI/app/routers/pedidos.py:38 (listar_pedidos — filtro
    # PedidoReserva.id_clientes == cliente.id_usuario).
    _c("tra-18", 4, 2, "contagem_inconsistente", None,
       ["contagem", "inconsistent", "faltam", "sumiram"], ["tipo", "ausente do contrato"],
       requisicao="GET /api/pedidos?login=11122233344",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="A resposta de GET /api/pedidos traz so 1 reserva do Cliente Teste, mas "
               "ele fez 3 reservas nos ultimos meses; as outras duas nao aparecem nem "
               "como ativas nem como canceladas.",
       observacao="A consulta filtra por id_clientes = cliente.id_usuario; as 3 "
                   "reservas estao todas com o mesmo id_clientes no banco."),
    # fonte: CobaiaFront/banco/seed.sql:25 (id 9, "Balde de Cerveja", valor_produto
    # 45.00) e CobaiaAPI/app/routers/produtos.py:28 (_to_dict, preco:
    # float(p.valor_produto)).
    _c("tra-19", 4, 2, "escala_ou_unidade_errada", "preco",
       ["escala", "unidade", "dez"], ["tipo", "ausente"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", '
             '"tipo": "Bebidas", "preco": 4.5, "imagem": "balde_cerveja.png", '
             '"destaque": true}]',
       sintoma="O Balde de Cerveja aparece por 'R$ 4,50'; no cadastro custa R$ 45,00 "
               "— dez vezes mais.",
       observacao="tbprodutos.valor_produto do id 9 vale 45.00."),
    # fonte: CobaiaFront/banco/seed.sql:19-20 (ids 3 e 4, id_tipo_produto 1 pros dois)
    # e CobaiaAPI/app/models.py:27-38 (Produto.tipo via relationship) + app/routers/
    # produtos.py:27 (_to_dict, tipo: p.tipo.rotulo_tipo).
    _c("tra-20", 4, 3, "chave_de_juncao_errada", "tipo",
       ["juncao", "tipo", "carnes", "sobremesas"], ["ausente", "nulo"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, '
             'fatiado na hora", "tipo": "Sobremesas", "preco": 69.9, '
             '"imagem": "fraldinha.jpg", "destaque": false}, '
             '{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por '
             'horas", "tipo": "Sobremesas", "preco": 79.9, "imagem": "costelona.jpg", '
             '"destaque": true}]',
       sintoma="Fraldinha e Costelona (os dois cortes de carne) aparecem na categoria "
               "Sobremesas; os demais produtos de carne da listagem continuam certos "
               "em Carnes.",
       observacao="tbprodutos.id_tipo_produto de id 3 e id 4 aponta pra 1 (Carnes) no "
                   "banco; so esses dois produtos vem errados na resposta, o que "
                   "sugere troca pontual de id_tipo_produto pra 4 (Sobremesas) nesses "
                   "dois registros, nao um bug geral de juncao."),
    # fonte: CobaiaFront/banco/seed.sql:16-30 (14 produtos cadastrados, ids 1 a 14) e
    # CobaiaAPI/app/routers/produtos.py:34-38 (listar_produtos — db.query(Produto).
    # all(), sem filtro nem paginacao).
    _c("tra-21", 4, 3, "contagem_inconsistente", None,
       ["contagem", "inconsistent", "falta", "14"], ["tipo", "ausente do contrato"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='(13 itens retornados; falta o id 13, "Hamburguer Artesanal")',
       sintoma="GET /api/produtos devolve 13 itens; o cadastro (tbprodutos) tem 14 "
               "produtos. O Hamburguer Artesanal (id 13) nao aparece em nenhuma "
               "pagina do site.",
       observacao="tbprodutos tem 14 linhas cadastradas, ids 1 a 14 (seed.sql); nao "
                   "existe coluna de exclusao logica em tbprodutos."),
]

# ----------------------------------------------------------- CLASSE 5: runtime
# Família de causas (igual aos 90): erro_interno_do_servidor, tempo_de_resposta_
# excedido, limite_de_requisicoes, dado_desatualizado, registro_duplicado,
# recurso_inexistente — "o comportamento no tempo e no estado esta correto?".
CASOS_INEDITOS += [
    # fonte: CobaiaAPI/app/routers/pedidos.py:35-37 (listar_pedidos — if not cliente:
    # raise HTTPException(404, "cliente não encontrado")); CobaiaAPI/tests/test_fault_
    # injection.py:81-82 confirma esse mesmo caminho pra um login que nao existe.
    _c("run-16", 5, 1, "recurso_inexistente", None,
       ["404", "cliente", "nao encontrad"], ["500", "timeout"],
       requisicao="GET /api/pedidos?login=55566677788",
       status=404, contrato=CONTRATO_PEDIDO,
       corpo='{"detail": "cliente nao encontrado"}',
       sintoma="Consultar as reservas de um cpf que nunca fez cadastro (55566677788) "
               "devolve 404; a mensagem indica cliente nao encontrado, nao uma lista "
               "vazia de reservas."),
    # fonte: CobaiaAPI/app/routers/pedidos.py:78-81 (cancelar_pedido — except
    # ErrorFault: raise HTTPException(status_code=500, ...), mesmo mecanismo de
    # run-1/run-6 mas num endpoint novo, o de cancelamento).
    _c("run-17", 5, 1, "erro_interno_do_servidor", None,
       ["500", "erro interno", "servidor"], ["404", "timeout"],
       requisicao="POST /api/pedidos/7/cancelar",
       status=500, contrato=CONTRATO_PEDIDO,
       corpo='{"detail": "erro interno (fault injection) em pedido"}',
       sintoma="Cancelar a reserva 7 devolve 500; nao da pra saber pela resposta se o "
               "status mudou no banco ou nao."),
    # fonte: CobaiaAPI/app/routers/pedidos.py:46-66 (criar_pedido — contrato normal e
    # 201 com o pedido criado; 429 narrativo, mesmo padrao ja usado em run-3/run-10,
    # aqui num endpoint de escrita em vez de leitura).
    _c("run-18", 5, 2, "limite_de_requisicoes", None,
       ["429", "limite", "requisic"], ["500", "timeout"],
       requisicao="POST /api/pedidos (6a tentativa de reserva no mesmo minuto)",
       status=429, contrato=CONTRATO_PEDIDO,
       corpo='{"detail": "too many requests"}',
       sintoma="Ao tentar confirmar a reserva varias vezes seguidas em pouco tempo, a "
               "API passa a recusar com 429; a reserva nao chega a ser criada."),
    # fonte: CobaiaFront/produtos_api.php:115-124 (fetch do modal, sem timeout
    # configurado) e CobaiaAPI/app/fault_injection.py:70-72 (latency: time.sleep(2) —
    # o modo real soma 2s fixos; aqui o valor e maior, cenario narrativo como run-9 ja
    # usa, agora no endpoint de detalhe em vez de listagem).
    _c("run-19", 5, 2, "tempo_de_resposta_excedido", None,
       ["lenta", "tempo", "demora"], ["500", "429"],
       requisicao="GET /api/produtos/1 (clique em 'Saiba Mais...')",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='(recebido apos 7,8 s)',
       sintoma="O modal de detalhes demora quase 8 segundos pra abrir depois do "
               "clique; o mesmo clique respondia em menos de 200ms antes.",
       observacao="fetch() nao tem timeout configurado em produtos_api.php; o modal "
                   "so abre quando a Promise resolve, por mais que demore."),
    # fonte: CobaiaFront/admin/produtos_atualiza.php:24-31 (UPDATE tbprodutos SET ...
    # valor_produto = ... WHERE id_produto = $id — grava na MESMA tabela que a
    # CobaiaAPI le) e CobaiaAPI/app/routers/produtos.py:34-38 (listar_produtos —
    # db.query(Produto).all() a cada chamada, sem nenhum cache proprio).
    _c("run-20", 5, 3, "dado_desatualizado", "preco",
       ["cache", "desatualiz", "antig"], ["ausente", "tipo"],
       requisicao="admin atualiza preco da Fraldinha para R$ 74,90 -> GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='GET devolveu {"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na '
             'brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, '
             '"imagem": "fraldinha.jpg", "destaque": false} — o preco antigo, mesmo '
             'apos a atualizacao confirmada no painel.',
       sintoma="Depois de o administrador mudar o preco da Fraldinha pra R$ 74,90 no "
               "painel, GET /api/produtos continua devolvendo 69.9 por varios "
               "minutos.",
       observacao="tbprodutos e a mesma tabela do painel PHP e da CobaiaAPI; listar_"
                   "produtos le do banco a cada chamada, sem cache proprio — a "
                   "defasagem apontaria pra um cache fora da CobaiaAPI."),
    # fonte: CobaiaAPI/app/models.py:30 (id_produto: mapped_column(..., primary_key=
    # True) — chave primaria) e app/routers/produtos.py:34-38 (listar_produtos —
    # db.query(Produto).all(), sem join que hoje pudesse multiplicar linhas).
    _c("run-21", 5, 3, "registro_duplicado", None,
       ["duplicad", "repetid"], ["cache", "ausente"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[' + PRODUTO_OK + ', ' + PRODUTO_OK + ', {"id": 3, "nome": "Fraldinha", '
             '"resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", '
             '"preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}]',
       sintoma="A Picanha ao Alho aparece duas vezes seguidas na grade de produtos, "
               "com exatamente os mesmos dados.",
       observacao="tbprodutos.id_produto e chave primaria; nao tem como a linha "
                   "existir duas vezes na tabela — a duplicata esta na consulta ou na "
                   "montagem da resposta, nao no cadastro."),
]

# ------------------------------------------------------------ CLASSE 6: efeito
# Família de causas (igual aos 90): localizador_quebrado, estado_da_tela_divergente —
# "o que o usuario de fato ve esta correto?", sem erro de rede aparente.
CASOS_INEDITOS += [
    # fonte: CobaiaFront/produtos_api.php:82 (data-id vem de p.id) — a arvore de
    # acessibilidade do caso (ARVORE_CARTOES) so documenta os cards de data-id "1" e
    # "3", nao "2".
    _c("efe-16", 6, 1, "localizador_quebrado", None,
       ["seletor", "localizador", "data-id"], ["500", "tipo"],
       requisicao="(sem falha de rede) passo do roteiro: abrir detalhes do produto de "
                   "data-id=2",
       status=200, contrato="n/a", corpo="(nenhuma requisicao falhou)",
       arvore=ARVORE_CARTOES, seletor_quebrado="button[data-id='2']",
       sintoma="O roteiro falha por tempo esgotado; a pagina carregada agora so tem "
               "os cards de data-id 1 e 3 (o roteiro foi escrito pensando em outro "
               "estado da listagem)."),
    # fonte: CobaiaFront/produtos_api.php:76 (<h3> em volta do nome do produto —
    # nivel 3 de heading).
    _c("efe-17", 6, 1, "localizador_quebrado", None,
       ["seletor", "localizador", "heading", "nivel"], ["500", "ausente"],
       requisicao="(sem falha de rede) passo do roteiro: localizar o titulo "
                   "'Picanha ao Alho' como heading de nivel 2",
       status=200, contrato="n/a", corpo="(nenhuma requisicao falhou)",
       arvore=ARVORE_CARTOES, seletor_quebrado='heading "Picanha ao Alho" level=2',
       sintoma="O roteiro nao encontra o titulo do produto; na arvore de "
               "acessibilidade o nome do produto e um heading de nivel 3, nao 2."),
    # fonte: CobaiaFront/produtos_api.php:69-88 (cartaoProduto — nenhum atributo
    # data-testid e gerado em ponto nenhum da funcao).
    _c("efe-18", 6, 2, "localizador_quebrado", None,
       ["seletor", "localizador", "testid", "ausente"], ["500", "ambiguo"],
       requisicao="(sem falha de rede) passo do roteiro: localizar o card do produto "
                   "pelo atributo data-testid",
       status=200, contrato="n/a", corpo="(nenhuma requisicao falhou)",
       arvore=ARVORE_CARTOES, seletor_quebrado='[data-testid="produto-card"]',
       sintoma="O roteiro nao encontra nenhum card de produto; a pagina nao usa "
               "atributo data-testid em elemento nenhum."),
    # fonte: CobaiaFront/produtos_api.php:112-124 (o listener de clique dispara um
    # fetch por elemento clicado e preenche titulo+corpo do modal no mesmo .then(),
    # sem descartar respostas de cliques anteriores nem marcar qual foi o ultimo
    # clique) — mesma familia de causa do efe-13 (respostas fora de ordem), aqui no
    # fetch do modal de detalhe em vez do fetch da grade.
    _c("efe-19", 6, 2, "estado_da_tela_divergente", None,
       ["tela", "sobrescr", "ultimo clique", "anterior"], ["500", "cache", "ausente"],
       requisicao="clique em 'Saiba Mais...' da Fraldinha (data-id=3); antes da "
                   "resposta chegar, clique em 'Saiba Mais...' da Picanha ao Alho "
                   "(data-id=1); a resposta do produto 1 chega primeiro",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo="GET /api/produtos/1 responde em 150ms; GET /api/produtos/3 (disparado "
             "antes, pelo primeiro clique) responde em 900ms",
       sintoma="O ultimo produto clicado foi a Picanha ao Alho, mas o modal termina "
               "mostrando os dados da Fraldinha (o clique anterior); nenhum erro "
               "aparece no console, e cada resposta em separado esta correta.",
       observacao="Cada clique dispara um fetch independente pra /api/produtos/{id}; "
                   "nao ha verificacao de qual clique foi o mais recente antes de "
                   "preencher o modal."),
    # fonte: CobaiaFront/produtos_api.php:98-104 (bloco "if (!Array.isArray(produtos)
    # || produtos.length === 0) { status.textContent = ...; return; }" — o return sai
    # ANTES da linha 104, que e a unica que reescreve grid.innerHTML).
    _c("efe-20", 6, 3, "estado_da_tela_divergente", None,
       ["tela", "grade", "status", "antig"], ["500", "cache"],
       requisicao="GET /api/produtos (1a chamada, retornou 14 itens) seguido de uma "
                   "nova chamada de carregarProdutos() que devolveu lista vazia",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo="1a resposta: 14 itens. 2a resposta: []",
       sintoma="Depois da segunda chamada, a mensagem acima da grade diz 'Nenhum "
               "produto retornado pela API.', mas os 14 cards da primeira chamada "
               "continuam visiveis embaixo dela.",
       observacao="Quando a lista vem vazia, carregarProdutos() so atualiza o texto "
                   "de status e sai (return) antes de tocar em grid.innerHTML; se a "
                   "grade ja tinha conteudo de uma chamada anterior, ele fica do "
                   "jeito que estava."),
    # fonte: CobaiaFront/produtos_api.php:99-101 (if (!Array.isArray(produtos) ||
    # produtos.length === 0) — Array.isArray(null) e false, cai no mesmo ramo do
    # array vazio, com a mesma mensagem).
    _c("efe-21", 6, 3, "estado_da_tela_divergente", None,
       ["tela", "mensagem", "engan", "vazio"], ["500", "timeout"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO + " (lista)",
       corpo="null",
       sintoma="A pagina mostra 'Nenhum produto retornado pela API.', dando a "
               "entender que o cadastro esta vazio; na verdade a API devolveu null, "
               "nao uma lista vazia — sao situacoes diferentes que a tela nao "
               "diferencia.",
       observacao="produtos_api.php trata qualquer valor que nao seja array "
                   "(incluindo null) do mesmo jeito que uma lista vazia."),
]
