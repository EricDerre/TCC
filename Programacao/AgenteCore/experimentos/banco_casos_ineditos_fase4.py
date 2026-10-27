#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo com 36 casos inéditos de falha de integração (2 por
# classe x nível, classes 1 a 6 e níveis 1 a 3 de taxonomia.py) para o conjunto de avaliação da
# Fase 4. Os ids continuam a numeração de banco_casos_ineditos.py (Fase 3-B), que vai até 21 em
# cada classe: lex-22 a lex-27, sin-22 a sin-27, semt-22 a semt-27, tra-22 a tra-27, run-22 a
# run-27 e efe-22 a efe-27.
# ! Motivo: a ficha 27 da Fase 4 pede 36 casos inéditos a mais para o conjunto de avaliação
# chegar a 108 casos (72 + 36), para que uma diferença de 4 ou 5 casos entre dois resultados
# deixe de ser tratada como ruído. Os cenários são novos de propósito: o teste mede se o agente
# generaliza para o que nunca viu, então nenhum caso repete a combinação causa + rota + campo
# dos casos que o autor chegou a ver (ver "De onde vêm os cenários" abaixo).
"""
36 casos inéditos (2 por classe x nível de taxonomia.py) para o conjunto de avaliação da Fase 4.
Mesma função _c(...) e mesmas constantes de banco_casos.py, mesmo formato de gabarito
(causa_raiz, campo_afetado, termos_esperados, termos_proibidos).

Cada caso leva "# fonte:" (arquivo:linha da CobaiaAPI ou do produtos_api.php que sustenta o corpo e
o sintoma) e "# modo da API:" (qual modo de fault_injection.py reproduz o caso, ou "sem modo" quando
é um cenário descrito). Níveis, pelo NIVEIS de taxonomia.py: 1 = sinal local e explícito (status de
erro, corpo que não parseia, campo ausente, valor absurdo); 2 = HTTP 200 e corpo que parseia, mas só
se percebe comparando com o contrato ou com uma segunda fonte; 3 = HTTP 200, corpo válido e tipos
corretos, e a falha só aparece cruzando duas requisições ou a requisição contra a tela.
"""
from banco_casos import CONTRATO_PEDIDO, CONTRATO_PRODUTO, _c

# De onde vêm os cenários: da leitura de CobaiaAPI/app/** (rotas, schemas e fault_injection.py, com
# os 7 modos antigos e os 14 de 26/10/2026), CobaiaFront/produtos_api.php, CobaiaFront/banco/*.sql
# e taxonomia.py. Os corpos dos casos de API foram conferidos por script contra a CobaiaAPI de
# verdade (app/** rodando com um SQLite em memória no lugar do MariaDB, semeado pelo seed.sql):
# mesmo status, mesmas chaves na mesma ordem, mesmos valores. As reações da tela (R$ 0,00,
# undefined, [object Object], Produto #4, destaque: True) foram conferidas rodando as funções
# formatarPreco e cartaoProduto copiadas de produtos_api.php:64-88. Para o formato do prompt e da
# pontuação foram lidos também estrategias.py, avaliar.py e recuperacao.py (só código) e a árvore
# real gravada em fixtures_fase4/arvore_produtos_api.json. Não foram lidos resultados_alvo/,
# base_conhecimento/, biblioteca_producao/, Documentacao/, claude-memoria/ nem os casos dos bancos
# existentes, com uma exceção por engano: o autor viu as linhas 36 a 185 de
# banco_casos_ineditos.py (casos lex-16 a lex-21 e sin-16 a sin-19, e o começo do sin-20). Nenhum
# caso daqui repete a combinação causa + rota + campo de nenhum deles; o mais próximo é o lex-27,
# que estraga o mesmo campo status de pedido do lex-21, mas num POST e com outra evidência.
#
# Folgas dos níveis que a própria taxonomia impõe: na classe 1 só a codificacao_incorreta tem corpo
# que parseia, então os níveis 2 e 3 dela são 4 casos dessa causa (varia campo, rota e tipo de
# evidência); na classe 5, limite_de_requisicoes e recurso_inexistente são status de erro (nível 1
# por definição) e erro_interno_do_servidor só aparece como parte do enredo do run-27. Ficaram sem
# caso próprio resposta_truncada (o único corpo truncado que a API produz é o texto fixo
# MALFORMED_BODY, fault_injection.py:90) e erro_interno_do_servidor.
#
# Convenções:
#  - A requisicao nunca cita o nome do modo, porque em vários casos ele é igual à causa e
#    entregaria a resposta.
#  - Corpo em JSON com os separadores padrão do json.dumps, como PRODUTO_OK; a API real manda sem
#    espaços, mas o conteúdo e a ordem das chaves são os mesmos. Os corpos de lista são recortes
#    (2 a 4 itens) da lista real de 14; quando a contagem importa, o caso diz o total.
#  - Nos corpos de pedido o status (coluna status de tbpedido_reserva: 'Em Análise' é a reserva
#    recém-criada, 'Cancelado' é a reserva cancelada pelo cliente) vem como 'Em Analise', sem
#    acento, igual ao CONTRATO_PEDIDO; a API real devolve 'Em Análise' (models.py:60). Só o lex-27,
#    que é de codificação, mantém o acento. Sintoma e observação são escritos sem acento, como nos
#    outros bancos; os trechos citados da tela e dos dados mantêm a grafia real.
#  - Árvore da tela no formato de ARVORE_CARTOES (banco_casos.py), mas sem "disabled" no botão de
#    preço: em produtos_api.php:81 ele só tem a classe "disable" (sem o atributo) e é clicável.
#  - As linhas citadas de fault_injection.py valem para a versão de 26/10/2026 22:43 (com o ramo
#    type_drift 4 linhas maior); se o arquivo mudar de novo, conferir as citações.


# ! Alteração de IA - Revisar: função nova que monta a árvore de acessibilidade da página
# Produtos (API) no formato de ARVORE_CARTOES (banco_casos.py), a partir dos cartões visíveis e,
# quando houver, do modal aberto.
# ! Motivo: os 6 casos da classe 6 precisam de árvores quase iguais, com variações pequenas (que
# cartões aparecem, se o modal está aberto e com que título); escrever as 6 à mão deixaria passar
# erro de digitação entre elas. A diferença para ARVORE_CARTOES é o botão de preço sem
# `disabled`: em produtos_api.php:81 ele só tem a classe "disable" e é clicável, como mostra a
# árvore real gravada em fixtures_fase4/arvore_produtos_api.json.
def _arvore(cartoes, modal=None):
    linhas = [
        'document "Churrascaria Fornalha - Produtos (API)"',
        "  navigation",
        '    link "PRODUTOS"',
        '    link "PRODUTOS (API)"',
        "  main",
        '    heading "Produtos via API" level=2',
    ]
    for nome, tipo, preco, id_produto in cartoes:
        linhas += [
            "    group",
            f'      heading "{nome}" level=3',
            f'      text "{tipo}"',
            f'      button "{preco}"',
            ('      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" '
             f'data-id="{id_produto}"'),
        ]
    if modal:
        titulo, descricao = modal
        linhas += [
            "  dialog",
            '    button "×" class="close"',
            f'    heading "{titulo}" level=4 id="modalDetalheTitulo"',
            f'    text "{descricao}" id="modalDetalheCorpo"',
        ]
    return "\n".join(linhas) + "\n"


# ! Alteração de IA - Revisar: lista que reúne os 36 casos, em ordem de classe e, dentro de cada
# classe, de nível (dois de nível 1, dois de nível 2, dois de nível 3).
# ! Motivo: o avaliador e o harness da Fase 4 percorrem uma lista só; manter a ordem por classe
# e nível deixa conferir de relance que cada par (classe, nível) tem exatamente 2 casos.
CASOS_INEDITOS_FASE4 = []

# ------------------------------------------------------------- CLASSE 1: lexica
# Causas usadas: corpo_nao_e_json, corpo_vazio e codificacao_incorreta (4 casos, porque é a única
# causa léxica cujo corpo parseia, o que os níveis 2 e 3 exigem).
CASOS_INEDITOS_FASE4 += [
    # fonte: CobaiaAPI/app/fault_injection.py:91 (HTML_DE_ERRO) e :231-232 (a resposta especial
    # devolve esse HTML com media_type text/html e status 200); CobaiaAPI/app/routers/produtos.py:
    # 47-49 (listar_produtos devolve a resposta especial antes de consultar o banco);
    # CobaiaFront/produtos_api.php:94-97 (resp.ok é true em 200, então cai em resp.json()) e
    # :106-109 (o catch escreve "Erro ao carregar produtos da CobaiaAPI: " + err.message na linha
    # de status, com a classe text-danger).
    # modo da API: corpo_nao_e_json (sem target_field), em GET /api/produtos.
    _c("lex-22", 1, 1, "corpo_nao_e_json", None,
       ["html", "nao e json", "text/html"], ["truncad", "erro_interno"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo="<html><body><h1>Erro</h1><p>Falha ao montar a resposta.</p></body></html>",
       sintoma="A pagina Produtos (API) abre sem nenhum cartao. A linha de status acima da grade "
               "fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI:' seguido de uma "
               "mensagem do navegador que cita o caractere inesperado '<' e diz que o texto nao "
               "e JSON valido. O status HTTP da resposta e 200.",
       observacao="O Content-Type da resposta e text/html, nao application/json."),
    # fonte: CobaiaAPI/app/fault_injection.py:229-230 (a resposta especial devolve Response com
    # content="" e media_type application/json) e CobaiaAPI/app/routers/produtos.py:60-62
    # (obter_produto devolve essa resposta antes de consultar o banco); CobaiaFront/
    # produtos_api.php:116-119 (resp.ok é true em 200 e cai em resp.json()) e :125-129 (o catch
    # escreve "Erro" no título e err.message no corpo do modal). Content-Length 0 conferido
    # rodando a rota real.
    # modo da API: corpo_vazio (sem target_field), em GET /api/produtos/6.
    _c("lex-23", 1, 1, "corpo_vazio", None,
       ["vazio", "sem corpo", "unexpected end"], ["truncad", "html"],
       requisicao="GET /api/produtos/6",
       status=200, contrato=CONTRATO_PRODUTO, corpo="",
       sintoma="Ao clicar em 'Saiba Mais...' da Maminha, o modal abre com 'Erro' no titulo e, no "
               "corpo, uma mensagem do navegador sobre 'Unexpected end of JSON input'. A resposta "
               "chegou com status 200 e Content-Length 0."),
    # fonte: CobaiaAPI/app/fault_injection.py:190-192 (codificacao_incorreta relê os bytes UTF-8
    # do campo como latin-1: valor.encode("utf-8").decode("latin-1")); CobaiaAPI/app/routers/
    # produtos.py:66-67 (obter_produto aplica apply_fault no dict do produto); CobaiaFront/banco/
    # seed.sql:30 (id 14: nome 'Abacaxi na Brasa', resumo 'Com canela e açúcar');
    # CobaiaFront/produtos_api.php:122 (o corpo do modal recebe p.resumo).
    # modo da API: codificacao_incorreta com target_field=resumo, em GET /api/produtos/14.
    _c("lex-24", 1, 2, "codificacao_incorreta", "resumo",
       ["codifica", "encoding", "acent"], ["fora_do_dominio", "tipo_divergente"],
       requisicao="GET /api/produtos/14",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e aÃ§Ãºcar", '
             '"tipo": "Sobremesas", "preco": 14.9, "imagem": "abacaxi.jpg", "destaque": false}',
       sintoma="O modal do Abacaxi na Brasa abre com o titulo certo, mas o texto de descricao "
               "aparece como 'Com canela e aÃ§Ãºcar': cada letra acentuada virou um par de "
               "simbolos estranhos."),
    # fonte: CobaiaAPI/app/fault_injection.py:190-192 e :79 (CAMPO_PADRAO: codificacao_incorreta
    # age em nome); CobaiaAPI/app/routers/produtos.py:52 (a lista aplica apply_fault em cada
    # item, então só os nomes com acento mudam); CobaiaFront/banco/seed.sql:27-29 (ids 11 a 13:
    # 'Pão de Alho', 'Queijo Coalho', 'Hambúrguer Artesanal'); CobaiaFront/produtos_api.php:76
    # (o título do cartão é p.nome).
    # modo da API: codificacao_incorreta (campo padrão nome), em GET /api/produtos.
    _c("lex-25", 1, 2, "codificacao_incorreta", "nome",
       ["codifica", "encoding", "utf", "acent"], ["fora_do_dominio", "tipo_divergente"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", '
             '"tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", '
             '"destaque": false}, '
             '{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", '
             '"tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", '
             '"destaque": true}, '
             '{"id": 13, "nome": "HambÃºrguer Artesanal", "resumo": "Blend da casa, pão '
             'brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", '
             '"destaque": false}]',
       sintoma="Na grade de acompanhamentos, os titulos 'PÃ£o de Alho' e 'HambÃºrguer "
               "Artesanal' aparecem com simbolos estranhos no lugar das letras acentuadas, "
               "enquanto 'Queijo Coalho' (sem acento no nome) aparece normal. A descricao de "
               "cada cartao, logo abaixo do titulo, esta com os acentos certos."),
    # fonte: CobaiaAPI/app/fault_injection.py:190-192; CobaiaAPI/app/routers/produtos.py:66-67;
    # CobaiaFront/banco/seed.sql:27 (id 11: 'Pão de Alho'); CobaiaFront/produtos_api.php:76 (o
    # título do cartão vem da listagem carregada antes) e :121 (o título do modal vem do
    # detalhe, p.nome).
    # modo da API: codificacao_incorreta (campo padrão nome), em GET /api/produtos/11, ligado
    # depois de a grade carregar (o cartão fica com o nome certo e o modal com o nome estragado).
    _c("lex-26", 1, 3, "codificacao_incorreta", "nome",
       ["codifica", "encoding", "utf", "acent"], ["desatualizad", "juncao"],
       requisicao="GET /api/produtos/11",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", '
             '"tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", '
             '"destaque": false}',
       sintoma="Na mesma tela, o cartao do Pão de Alho mostra o titulo 'Pão de Alho', mas o "
               "modal aberto pelo 'Saiba Mais...' desse mesmo cartao mostra o titulo 'PÃ£o de "
               "Alho'. A grade foi carregada antes do clique e as duas respostas chegaram com "
               "status 200.",
       observacao="A listagem GET /api/produtos, feita antes do clique, trouxe este produto "
                  "(id 11) com o nome 'Pão de Alho'; so a resposta do detalhe veio com os "
                  "simbolos estranhos."),
    # fonte: CobaiaAPI/app/fault_injection.py:190-192; CobaiaAPI/app/routers/pedidos.py:46-66
    # (criar_pedido grava a reserva com status 'Em Análise' e devolve o dict com apply_fault) e
    # :1-6 (a reserva criada pela API aparece na área do cliente do CobaiaFront, mesma tabela
    # tbpedido_reserva); CobaiaAPI/app/models.py:60 (enum 'Em Análise'/'Cancelado'). Nenhuma
    # página consome pedidos, então o sintoma é no nível da resposta.
    # modo da API: codificacao_incorreta com target_field=status, em POST /api/pedidos.
    _c("lex-27", 1, 3, "codificacao_incorreta", "status",
       ["codifica", "encoding", "acent"], ["fora_do_dominio", "tipo_divergente"],
       requisicao='POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 3, '
                  '"data_pedido": "2026-12-05"})',
       status=201, contrato=CONTRATO_PEDIDO,
       corpo='{"id_pedido": 10, "pessoas": 3, "data_pedido": "2026-12-05", '
             '"status": "Em AnÃ¡lise", "nome": "Cliente Teste", "cpf": "11122233344"}',
       sintoma="A reserva e criada (status 201), mas o campo status da resposta traz 'Em "
               "AnÃ¡lise', com simbolos estranhos no lugar do acento.",
       observacao="Consultando o banco direto, tbpedido_reserva guarda a reserva 10 com status "
                  "'Em Análise'."),
]

# ---------------------------------------------------------- CLASSE 2: sintatica
# Causas usadas: campo_ausente (2), campo_renomeado (2), estrutura_aninhada_divergente e
# colecao_no_lugar_de_objeto. No nível 3 a falha é intermitente: probability é a chance (de 0 a 1)
# de a falha disparar, e com valor menor que 1 o sorteio é feito item a item
# (fault_injection.py:118-119 e routers/produtos.py:52), então só alguns itens da mesma resposta
# perdem ou renomeiam o campo, e a cada recarga são outros.
CASOS_INEDITOS_FASE4 += [
    # fonte: CobaiaAPI/app/fault_injection.py:171-172 (field_missing tira o campo alvo do dict);
    # CobaiaAPI/app/routers/produtos.py:52 (a lista aplica apply_fault em cada item, então todos
    # perdem o campo); CobaiaFront/banco/seed.sql:21-22 (ids 5 e 6); CobaiaFront/
    # produtos_api.php:76 (o título do cartão é (p.nome || '(sem nome)')).
    # modo da API: field_missing com target_field=nome, em GET /api/produtos.
    _c("sin-22", 2, 1, "campo_ausente", "nome",
       ["ausente", "nome", "falt"], ["renomead", "nulo"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 5, "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", '
             '"preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}, '
             '{"id": 6, "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", '
             '"preco": 72.9, "imagem": "maminha.jpg", "destaque": false}]',
       sintoma="Todos os cartoes da grade aparecem com o titulo '(sem nome)'. As fotos, as "
               "descricoes, os precos e os botoes 'Saiba Mais...' continuam normais."),
    # fonte: CobaiaAPI/app/fault_injection.py:173-175 (field_renamed troca o campo por
    # <campo>_v2 e o põe no fim do objeto); CobaiaAPI/app/routers/produtos.py:66-67;
    # CobaiaFront/banco/seed.sql:26 (id 10: 'Refrigerante', resumo 'Lata 350ml, diversos
    # sabores'); CobaiaFront/produtos_api.php:122 (o corpo do modal é p.resumo || "(sem
    # descrição)").
    # modo da API: field_renamed com target_field=resumo, em GET /api/produtos/10.
    _c("sin-23", 2, 1, "campo_renomeado", "resumo",
       ["renomead", "resumo_v2", "resumo"], ["nulo", "aninhad"],
       requisicao="GET /api/produtos/10",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='{"id": 10, "nome": "Refrigerante", "tipo": "Bebidas", "preco": 7.0, '
             '"imagem": "refrigerante.png", "destaque": false, '
             '"resumo_v2": "Lata 350ml, diversos sabores"}',
       sintoma="O modal do Refrigerante abre com o titulo certo, mas o texto de descricao "
               "aparece como '(sem descrição)'."),
    # fonte: CobaiaAPI/app/fault_injection.py:193-194 (estrutura_aninhada_divergente embrulha o
    # valor em {"valor": ..., "moeda": "BRL"}, qualquer que seja o campo); CobaiaAPI/app/routers/
    # produtos.py:52; CobaiaFront/banco/seed.sql:19-20 (ids 3 e 4); CobaiaFront/
    # produtos_api.php:77 (se p.tipo é objeto, a tela escreve JSON.stringify(p.tipo)).
    # modo da API: estrutura_aninhada_divergente com target_field=tipo, em GET /api/produtos.
    _c("sin-24", 2, 2, "estrutura_aninhada_divergente", "tipo",
       ["aninhad", "objeto", "valor"], ["renomead", "truncad"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na '
             'hora", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 69.9, '
             '"imagem": "fraldinha.jpg", "destaque": false}, '
             '{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", '
             '"tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 79.9, '
             '"imagem": "costelona.jpg", "destaque": true}]',
       sintoma='Sob o nome de cada produto, a linha da categoria mostra o texto '
               '{"valor":"Carnes","moeda":"BRL"} em vez de apenas Carnes. O resto de cada '
               'cartao esta normal.'),
    # fonte: CobaiaAPI/app/routers/produtos.py:72-73 (colecao_no_lugar_de_objeto devolve [data]
    # no detalhe); CobaiaFront/produtos_api.php:121-122 (p.nome e p.resumo de um array são
    # undefined, então o título vira "Produto #" + id e o corpo "(sem descrição)");
    # CobaiaFront/banco/seed.sql:20 (id 4: 'Costelona').
    # modo da API: colecao_no_lugar_de_objeto (sem target_field), em GET /api/produtos/4.
    _c("sin-25", 2, 2, "colecao_no_lugar_de_objeto", None,
       ["colec", "lista", "array"], ["campo_ausente", "nulo"],
       requisicao="GET /api/produtos/4",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", '
             '"tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]',
       sintoma="Ao clicar em 'Saiba Mais...' da Costelona, o modal abre com o titulo 'Produto "
               "#4' e o texto '(sem descrição)', como se o produto nao tivesse dados."),
    # fonte: CobaiaAPI/app/fault_injection.py:118-119 (o sorteio de probability) e :171-172
    # (field_missing); CobaiaAPI/app/routers/produtos.py:52 (cada item da lista sorteia
    # sozinho); CobaiaFront/banco/seed.sql:24-26 (ids 8 a 10); CobaiaFront/produtos_api.php:64-67
    # (formatarPreco(undefined) devolve String(undefined), isto é, "undefined").
    # modo da API: field_missing com target_field=preco e probability=0.5, em GET /api/produtos
    # (sorteio deste recorte: id 8 sim, id 9 não, id 10 sim).
    _c("sin-26", 2, 3, "campo_ausente", "preco",
       ["ausente", "preco", "alguns"], ["renomead", "nulo"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", '
             '"tipo": "Bebidas", "imagem": "agua.png", "destaque": false}, '
             '{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", '
             '"tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", '
             '"destaque": true}, '
             '{"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", '
             '"tipo": "Bebidas", "imagem": "refrigerante.png", "destaque": false}]',
       sintoma="Na grade de bebidas, o botao de preco da Agua Mineral e o do Refrigerante "
               "mostram 'undefined', e o do Balde de Cerveja mostra 'R$ 45,00'. Ao recarregar a "
               "pagina, os produtos afetados mudam.",
       observacao="O corpo mostra so os itens de id 8 a 10; a lista completa tem 14."),
    # fonte: CobaiaAPI/app/fault_injection.py:118-119 e :173-175 (field_renamed troca imagem por
    # imagem_v2 e a põe no fim do objeto); CobaiaAPI/app/routers/produtos.py:52; CobaiaFront/
    # banco/seed.sql:28-30 (ids 12 a 14); CobaiaFront/produtos_api.php:74 (sem p.imagem o
    # cartão sai sem a tag <img>).
    # modo da API: field_renamed com target_field=imagem e probability=0.5, em GET /api/produtos
    # (sorteio deste recorte: id 12 sim, id 13 não, id 14 sim).
    _c("sin-27", 2, 3, "campo_renomeado", "imagem",
       ["renomead", "imagem_v2", "alguns"], ["nulo", "aninhad"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", '
             '"tipo": "Acompanhamentos", "preco": 22.9, "destaque": true, '
             '"imagem_v2": "queijo.png"}, '
             '{"id": 13, "nome": "Hambúrguer Artesanal", "resumo": "Blend da casa, pão '
             'brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", '
             '"destaque": false}, '
             '{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e açúcar", '
             '"tipo": "Sobremesas", "preco": 14.9, "destaque": false, '
             '"imagem_v2": "abacaxi.jpg"}]',
       sintoma="Na grade, o Queijo Coalho e o Abacaxi na Brasa aparecem sem foto, enquanto o "
               "Hamburguer Artesanal mostra a foto normalmente. Nome, categoria, preco e botoes "
               "estao certos nos tres. Ao recarregar a pagina, os cartoes sem foto mudam.",
       observacao="O corpo mostra so os itens de id 12 a 14; a lista completa tem 14."),
]

# --------------------------------------------------------- CLASSE 3: semantica
# Causas usadas: nulo_inesperado (2), valor_fora_do_dominio (2), tipo_divergente e
# formato_de_data_divergente. No nível 3 o tipo está certo (null num campo que o contrato aceita
# nulo; inteiro negativo), então a falha só aparece cruzando requisições.
CASOS_INEDITOS_FASE4 += [
    # fonte: CobaiaAPI/app/fault_injection.py:186-187 (nulo_inesperado troca o campo alvo por
    # None); CobaiaAPI/app/routers/produtos.py:52; CobaiaFront/produtos_api.php:64-66
    # (Number(null) é 0, então formatarPreco(null) escreve "R$ 0,00"); CobaiaFront/banco/
    # seed.sql:22-23 (ids 6 e 7).
    # modo da API: nulo_inesperado com target_field=preco, em GET /api/produtos.
    _c("semt-22", 3, 1, "nulo_inesperado", "preco",
       ["nulo", "null", "preco"], ["campo_ausente", "escala"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", '
             '"tipo": "Carnes", "preco": null, "imagem": "maminha.jpg", "destaque": false}, '
             '{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", '
             '"tipo": "Carnes", "preco": null, "imagem": "cupim.jpg", "destaque": true}]',
       sintoma="Todos os botoes de preco da grade mostram 'R$ 0,00'. Os nomes, as categorias e "
               "as fotos estao normais."),
    # fonte: CobaiaAPI/app/fault_injection.py:133-140 (_fora_do_dominio: o número vira
    # -abs(valor) - 1) e :188-189; CobaiaAPI/app/routers/produtos.py:52; CobaiaFront/
    # produtos_api.php:64-67 (formatarPreco escreve "R$ -80,90"); CobaiaFront/banco/seed.sql:20-21
    # (ids 4 e 5: 79.90 e 74.90).
    # modo da API: valor_fora_do_dominio com target_field=preco, em GET /api/produtos.
    _c("semt-23", 3, 1, "valor_fora_do_dominio", "preco",
       ["dominio", "negativ", "preco"], ["escala", "tipo_divergente"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", '
             '"tipo": "Carnes", "preco": -80.9, "imagem": "costelona.jpg", "destaque": true}, '
             '{"id": 5, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na '
             'pedra quente", "tipo": "Carnes", "preco": -75.9, "imagem": "alcatra_pedra.jpg", '
             '"destaque": false}]',
       sintoma="Os botoes de preco da grade mostram valores negativos, por exemplo 'R$ -80,90' "
               "na Costelona e 'R$ -75,90' na Alcatra na Pedra."),
    # fonte: CobaiaAPI/app/fault_injection.py:165-170 (type_drift: campo que já é texto vira o
    # inteiro 1 e os outros tipos viram str(valor); destaque é booleano, então str(True) dá
    # "True"); CobaiaAPI/app/routers/produtos.py:52; CobaiaFront/produtos_api.php:70 (destaque
    # diferente de true/false cai em String(p.destaque) e a tela escreve "destaque: True");
    # CobaiaFront/banco/seed.sql:17-18 (ids 1 e 2: 'Sim' e 'Não').
    # modo da API: type_drift com target_field=destaque, em GET /api/produtos.
    _c("semt-24", 3, 2, "tipo_divergente", "destaque",
       ["tipo", "texto", "bool"], ["fora_do_dominio", "nulo"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho '
             'laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", '
             '"destaque": "True"}, '
             '{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", '
             '"tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", '
             '"destaque": "False"}]',
       sintoma="Nos cartoes da grade, a linha de destaque mostra 'destaque: True' e 'destaque: "
               "False' (em ingles, com inicial maiuscula) em vez de 'destaque: Sim' e 'destaque: "
               "Não'."),
    # fonte: CobaiaAPI/app/fault_injection.py:128-130 (_data_br: AAAA-MM-DD vira DD/MM/AAAA) e
    # :184-185, com o campo padrão em :74 (data_pedido); CobaiaAPI/app/routers/pedidos.py:46-66
    # (criar_pedido devolve o dict com apply_fault); CobaiaAPI/app/schemas.py:35-38
    # (PedidoCreate.data_pedido é date). Nenhuma página consome pedidos, então o sintoma é no
    # nível da resposta.
    # modo da API: formato_de_data_divergente (campo padrão data_pedido), em POST /api/pedidos.
    _c("semt-25", 3, 2, "formato_de_data_divergente", "data_pedido",
       ["data", "formato", "iso"], ["tipo_divergente", "valor_fora"],
       requisicao='POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 6, '
                  '"data_pedido": "2026-12-20"})',
       status=201, contrato=CONTRATO_PEDIDO,
       corpo='{"id_pedido": 11, "pessoas": 6, "data_pedido": "20/12/2026", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}',
       sintoma="A reserva e criada (status 201), mas a resposta devolve a data como "
               "'20/12/2026' para uma reserva pedida com '2026-12-20'; quem le o campo como data "
               "ISO (AAAA-MM-DD) nao consegue interpretar o valor."),
    # fonte: CobaiaAPI/app/fault_injection.py:186-187; CobaiaAPI/app/routers/produtos.py:66-67;
    # CobaiaAPI/app/schemas.py:19 (ProdutoOut.resumo é Optional[str], então null é permitido pelo
    # contrato); CobaiaFront/produtos_api.php:78 (o cartão escreve p.resumo || '') e :122 (o modal
    # escreve "(sem descrição)"); CobaiaFront/banco/seed.sql:28 (id 12: 'Queijo coalho grelhado
    # com mel').
    # modo da API: nulo_inesperado com target_field=resumo, em GET /api/produtos/12, ligado
    # depois de a grade carregar.
    _c("semt-26", 3, 3, "nulo_inesperado", "resumo",
       ["nulo", "null", "resumo"], ["campo_ausente", "desatualizad"],
       requisicao="GET /api/produtos/12",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='{"id": 12, "nome": "Queijo Coalho", "resumo": null, "tipo": "Acompanhamentos", '
             '"preco": 22.9, "imagem": "queijo.png", "destaque": true}',
       sintoma="O cartao do Queijo Coalho na grade mostra a descricao 'Queijo coalho grelhado "
               "com mel', mas o modal aberto pelo 'Saiba Mais...' desse mesmo produto mostra "
               "'(sem descrição)'. As duas respostas chegaram com status 200.",
       observacao="A listagem GET /api/produtos, feita antes do clique, trouxe este produto "
                  "(id 12) com o resumo preenchido. O contrato permite resumo nulo (texto|nulo)."),
    # fonte: CobaiaAPI/app/fault_injection.py:133-140 (inteiro vira -abs(valor) - 1: os ids 1 e 2
    # viram -2 e -3) e :188-189; CobaiaAPI/app/routers/produtos.py:52 e :63-65 (db.get não acha o
    # id negativo e a rota devolve 404 "produto não encontrado"); CobaiaFront/produtos_api.php:82
    # (data-id usa p.id), :114-115 (o clique busca /api/produtos/ + id) e :116-119 e :125-129
    # (HTTP 404 vira "Erro" no título e "HTTP 404" no corpo do modal).
    # modo da API: valor_fora_do_dominio com target_field=id, em GET /api/produtos (o 404 vem de
    # GET /api/produtos/-2, conferido na rota real).
    _c("semt-27", 3, 3, "valor_fora_do_dominio", "id",
       ["negativ", "dominio", "-2"], ["recurso_inexistente", "campo_ausente"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": -2, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho '
             'laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", '
             '"destaque": true}, '
             '{"id": -3, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", '
             '"tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", '
             '"destaque": false}]',
       sintoma="A grade carrega os 14 cartoes sem erro, mas qualquer 'Saiba Mais...' abre o modal "
               "com 'Erro' no titulo e 'HTTP 404' no corpo. Ao clicar no botao da Picanha ao "
               "Alho, a requisicao disparada foi GET /api/produtos/-2 e a resposta foi 404.",
       observacao="O corpo mostra so os itens da Picanha ao Alho e da Picanha Simples; a lista "
                  "completa tem 14."),
]

# ---------------------------------------------------------- CLASSE 4: traducao
# Causas usadas: escala_ou_unidade_errada (3), chave_de_juncao_errada (2) e
# contagem_inconsistente. Aqui o dado é válido e do tipo certo nos três níveis: o que muda é
# quanta evidência o caso entrega (valor absurdo à vista, uma segunda fonte, ou duas requisições).
CASOS_INEDITOS_FASE4 += [
    # fonte: CobaiaAPI/app/fault_injection.py:181-183 (escala_ou_unidade_errada multiplica o
    # número por 100: round(valor * 100, 2)); CobaiaAPI/app/routers/produtos.py:52; CobaiaFront/
    # banco/seed.sql:24-25 (ids 8 e 9: 6.00 e 45.00); CobaiaFront/produtos_api.php:64-67
    # (formatarPreco escreve "R$ 600,00" e "R$ 4500,00").
    # modo da API: escala_ou_unidade_errada com target_field=preco, em GET /api/produtos.
    _c("tra-22", 4, 1, "escala_ou_unidade_errada", "preco",
       ["escala", "100", "centavos"], ["fora_do_dominio", "nulo"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", '
             '"tipo": "Bebidas", "preco": 600.0, "imagem": "agua.png", "destaque": false}, '
             '{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", '
             '"tipo": "Bebidas", "preco": 4500.0, "imagem": "balde_cerveja.png", '
             '"destaque": true}]',
       sintoma="Na grade de bebidas, a Agua Mineral aparece por 'R$ 600,00' e o Balde de "
               "Cerveja por 'R$ 4500,00'; nomes, categorias e fotos estao certos.",
       observacao="Antes da falha, a mesma grade mostrava a Agua Mineral por 'R$ 6,00' e o Balde "
                  "de Cerveja por 'R$ 45,00'."),
    # fonte: CobaiaAPI/app/fault_injection.py:181-183 (o inteiro também é multiplicado: 4 vira
    # 400); CobaiaAPI/app/routers/pedidos.py:46-66; CobaiaAPI/app/schemas.py:35-38
    # (PedidoCreate); CobaiaAPI/app/models.py:58 (tbpedido_reserva.pessoas grava o número
    # enviado). Nenhuma página consome pedidos, então o sintoma é no nível da resposta.
    # modo da API: escala_ou_unidade_errada com target_field=pessoas, em POST /api/pedidos.
    _c("tra-23", 4, 1, "escala_ou_unidade_errada", "pessoas",
       ["escala", "100", "pessoas"], ["fora_do_dominio", "tipo_divergente"],
       requisicao='POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 4, '
                  '"data_pedido": "2026-12-19"})',
       status=201, contrato=CONTRATO_PEDIDO,
       corpo='{"id_pedido": 12, "pessoas": 400, "data_pedido": "2026-12-19", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}',
       sintoma="A reserva e criada (status 201), mas a resposta mostra 400 pessoas para uma "
               "reserva pedida para 4.",
       observacao="Consultando o banco direto, tbpedido_reserva guarda a reserva 12 com 4 "
                  "pessoas."),
    # fonte: CobaiaAPI/app/fault_injection.py:212-215 (chave_de_juncao_errada gira o campo alvo
    # entre os itens: cada um recebe o valor do seguinte) e :76 (campo padrão tipo);
    # CobaiaAPI/app/routers/produtos.py:52; CobaiaFront/banco/seed.sql:23-26 (ids 7 a 10: Cupim é
    # Carnes; Água Mineral, Balde de Cerveja e Refrigerante são Bebidas); CobaiaFront/
    # produtos_api.php:77 (a categoria do cartão sai de p.tipo).
    # modo da API: chave_de_juncao_errada (campo padrão tipo), em GET /api/produtos. Na lista
    # toda só 4 itens ficam trocados: o último de cada tipo (ids 7, 10, 13 e 14).
    _c("tra-24", 4, 2, "chave_de_juncao_errada", "tipo",
       ["juncao", "trocad", "categoria"], ["fora_do_dominio", "tipo_divergente"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", '
             '"tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}, '
             '{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", '
             '"tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}, '
             '{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", '
             '"tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", '
             '"destaque": true}, '
             '{"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", '
             '"tipo": "Acompanhamentos", "preco": 7.0, "imagem": "refrigerante.png", '
             '"destaque": false}]',
       sintoma="Na grade, o Cupim aparece com a categoria 'Bebidas' e o Refrigerante com "
               "'Acompanhamentos'; a Agua Mineral e o Balde de Cerveja aparecem com 'Bebidas'. "
               "Os nomes, os precos e as fotos estao certos.",
       observacao="O corpo mostra so os itens de id 7 a 10; a lista completa tem 14."),
    # fonte: CobaiaAPI/app/fault_injection.py:210-211 (contagem_inconsistente devolve itens[:-1]:
    # o último item some); CobaiaAPI/app/routers/produtos.py:52; CobaiaFront/banco/seed.sql:30
    # (id 14, 'Abacaxi na Brasa', é o último produto e a única sobremesa) e :16-30 (a tabela
    # tem 14 produtos).
    # modo da API: contagem_inconsistente (sem target_field), em GET /api/produtos (13 itens).
    _c("tra-25", 4, 2, "contagem_inconsistente", None,
       ["contagem", "13", "14"], ["duplicad", "truncad"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", '
             '"tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", '
             '"destaque": true}, '
             '{"id": 13, "nome": "Hambúrguer Artesanal", "resumo": "Blend da casa, pão '
             'brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", '
             '"destaque": false}]',
       sintoma="A grade mostra 13 cartoes e termina no Hamburguer Artesanal; a unica sobremesa "
               "(Abacaxi na Brasa) nao aparece. A tabela tbprodutos tem 14 linhas.",
       observacao="O corpo mostra so os dois ultimos itens da lista recebida (13 itens no "
                  "total, ids de 1 a 13)."),
    # fonte: CobaiaAPI/app/fault_injection.py:212-215 (com target_field=id, cada item recebe o id
    # do seguinte); CobaiaAPI/app/routers/produtos.py:52 e :63 (o detalhe busca pelo id
    # recebido); CobaiaFront/produtos_api.php:82 (data-id usa p.id), :114-115 (o clique busca
    # /api/produtos/ + id) e :121-122 (o modal escreve nome e resumo do detalhe);
    # CobaiaFront/banco/seed.sql:19-22 (ids 3 a 6).
    # modo da API: chave_de_juncao_errada com target_field=id, em GET /api/produtos (o detalhe
    # de id 4 devolve a Costelona, conferido na rota real).
    _c("tra-26", 4, 3, "chave_de_juncao_errada", "id",
       ["juncao", "trocad", "vizinho"], ["estado_da_tela", "escala"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 4, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na '
             'hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", '
             '"destaque": false}, '
             '{"id": 5, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", '
             '"tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}, '
             '{"id": 6, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na '
             'pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", '
             '"destaque": false}]',
       sintoma="A grade aparece normal, mas cada 'Saiba Mais...' abre o produto vizinho: o botao "
               "do cartao da Fraldinha abre o modal da Costelona, o da Costelona abre o da "
               "Alcatra na Pedra e o da Alcatra na Pedra abre o da Maminha. O clique no cartao "
               "da Fraldinha disparou GET /api/produtos/4, que respondeu 200 com os dados da "
               "Costelona.",
       observacao="O corpo mostra so os cartoes da Fraldinha, da Costelona e da Alcatra na "
                  "Pedra; a lista completa tem 14."),
    # fonte: CobaiaAPI/app/fault_injection.py:181-183; CobaiaAPI/app/routers/produtos.py:66-67
    # (o detalhe aplica apply_fault no dict do produto); CobaiaFront/banco/seed.sql:18 (id 2:
    # 84.90). O modal só mostra nome e resumo (produtos_api.php:121-122), então a tela não
    # denuncia o preço; o sintoma vem da conferência do roteiro.
    # modo da API: escala_ou_unidade_errada com target_field=preco, em GET /api/produtos/2,
    # ligado depois de a grade carregar.
    _c("tra-27", 4, 3, "escala_ou_unidade_errada", "preco",
       ["escala", "100", "8490"], ["desatualizad", "fora_do_dominio"],
       requisicao="GET /api/produtos/2",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", '
             '"tipo": "Carnes", "preco": 8490.0, "imagem": "picanha_sem.jpg", '
             '"destaque": false}',
       sintoma="O modal da Picanha Simples abre normal (ele so mostra nome e descricao), mas a "
               "conferencia de preco do roteiro falha: o preco do detalhe nao bate com o do "
               "cartao.",
       observacao="A listagem GET /api/produtos, feita antes, trouxe este produto (id 2) com "
                  "preco 84.9, e o cartao mostra 'R$ 84,90'."),
]

# ----------------------------------------------------------- CLASSE 5: runtime
# Causas usadas: limite_de_requisicoes, recurso_inexistente, registro_duplicado (2),
# tempo_de_resposta_excedido e dado_desatualizado (esta sem modo na API: cenário descrito, porque
# a CobaiaAPI não tem cache).
CASOS_INEDITOS_FASE4 += [
    # fonte: CobaiaAPI/app/fault_injection.py:233-238 (limite_de_requisicoes devolve 429, que é
    # "muitas requisições", com {"detail": "limite de requisições excedido"} e o cabeçalho
    # Retry-After: 60, isto é, esperar 60 segundos antes de tentar de novo);
    # CobaiaAPI/app/routers/produtos.py:47-49; CobaiaFront/produtos_api.php:94-97 (resp.ok é
    # false, então vira Error("HTTP " + status)) e :106-109 (o catch escreve a mensagem na linha
    # de status).
    # modo da API: limite_de_requisicoes (sem target_field), em GET /api/produtos.
    _c("run-22", 5, 1, "limite_de_requisicoes", None,
       ["429", "limite", "retry-after"], ["500", "timeout"],
       requisicao="GET /api/produtos",
       status=429, contrato=CONTRATO_PRODUTO,
       corpo='{"detail": "limite de requisições excedido"}',
       sintoma="A pagina Produtos (API) abre sem nenhum cartao; a linha de status acima da grade "
               "fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI: HTTP 429'.",
       observacao="A resposta traz o cabecalho Retry-After: 60."),
    # fonte: CobaiaAPI/app/fault_injection.py:239 (recurso_inexistente devolve 404 {"detail":
    # "produto não encontrado"} mesmo com id válido) e CobaiaAPI/app/routers/produtos.py:60-62;
    # CobaiaFront/produtos_api.php:116-119 e :125-129 (HTTP 404 vira "Erro" no título e "HTTP
    # 404" no corpo do modal); CobaiaFront/banco/seed.sql:21 (o id 5 existe).
    # modo da API: recurso_inexistente (sem target_field), em GET /api/produtos/5, ligado
    # depois de a grade carregar.
    _c("run-23", 5, 1, "recurso_inexistente", None,
       ["404", "inexistente", "nao encontrado"], ["500", "timeout"],
       requisicao="GET /api/produtos/5",
       status=404, contrato=CONTRATO_PRODUTO,
       corpo='{"detail": "produto não encontrado"}',
       sintoma="A grade foi carregada com os 14 cartoes, entre eles o da Alcatra na Pedra; ao "
               "clicar no 'Saiba Mais...' desse cartao, o modal abre com 'Erro' no titulo e "
               "'HTTP 404' no corpo.",
       observacao="O id 5 aparece na listagem GET /api/produtos feita antes do clique, e GET "
                  "/api/produtos/5 respondeu 200 em chamadas anteriores."),
    # fonte: CobaiaAPI/app/fault_injection.py:208-209 (registro_duplicado devolve [itens[0],
    # dict(itens[0]), *itens[1:]]); CobaiaAPI/app/routers/produtos.py:52; CobaiaFront/banco/
    # seed.sql:17 (id 1) e :16-30 (a tabela tem 14 produtos); CobaiaFront/produtos_api.php:104
    # (cada item do array vira um cartão, então o repetido aparece duas vezes).
    # modo da API: registro_duplicado (sem target_field), em GET /api/produtos (15 itens).
    _c("run-24", 5, 2, "registro_duplicado", None,
       ["duplicad", "repetid", "15"], ["contagem_inconsistente", "truncad"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho '
             'laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", '
             '"destaque": true}, '
             '{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho '
             'laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", '
             '"destaque": true}, '
             '{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", '
             '"tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", '
             '"destaque": false}]',
       sintoma="A grade mostra o cartao da Picanha ao Alho duas vezes seguidas, identicos, e os "
               "outros produtos uma vez cada. A grade tem 15 cartoes; a tabela tbprodutos tem 14 "
               "linhas.",
       observacao="O corpo mostra so os 3 primeiros itens da lista recebida (15 itens no total)."),
    # fonte: CobaiaAPI/app/fault_injection.py:154-156 (latency faz time.sleep(2) em cada chamada
    # de apply_fault, uma por item); CobaiaAPI/app/routers/produtos.py:66-67 (o detalhe chama
    # apply_fault uma vez: 2 s; a lista chamaria 14 vezes: 28 s); CobaiaFront/produtos_api.php:
    # 115-123 (o modal só abre quando a resposta chega, sem indicador de carregamento);
    # CobaiaFront/banco/seed.sql:23 (id 7).
    # modo da API: latency (sem target_field), em GET /api/produtos/7 (uma espera de 2 s,
    # contada na rota real).
    _c("run-25", 5, 2, "tempo_de_resposta_excedido", None,
       ["tempo", "latencia", "demor"], ["500", "truncad"],
       requisicao="GET /api/produtos/7",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", '
             '"tipo": "Carnes", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}',
       sintoma="Ao clicar em 'Saiba Mais...' do Cupim, nada acontece por cerca de 2 segundos e so "
               "entao o modal abre, com os dados certos. O roteiro espera o modal por 1 segundo e "
               "reprova por tempo.",
       observacao="As outras requisicoes da mesma sessao responderam em menos de 100 ms."),
    # fonte: CobaiaAPI/app/routers/pedidos.py:69-82 (cancelar_pedido grava 'Cancelado' e faz
    # commit antes de responder) e :30-43 (listar_pedidos lê a mesma tabela tbpedido_reserva):
    # sem uma camada de cache entre o cliente e a API, a segunda resposta não poderia trazer o
    # status antigo. Cenário descrito, sem modo da API (a CobaiaAPI não tem cache próprio): a
    # resposta teria passado por um cache intermediário.
    # modo da API: sem modo (cenário descrito).
    _c("run-26", 5, 3, "dado_desatualizado", None,
       ["desatualizad", "cache", "antigo"], ["estado_da_tela", "valor_fora"],
       requisicao="GET /api/pedidos?login=11122233344",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 8, "pessoas": 2, "data_pedido": "2026-11-20", '
             '"status": "Cancelado", "nome": "Cliente Teste", "cpf": "11122233344"}, '
             '{"id_pedido": 9, "pessoas": 4, "data_pedido": "2026-12-05", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="Logo depois de POST /api/pedidos/9/cancelar responder 200 com status "
               "'Cancelado', a consulta GET /api/pedidos?login=11122233344 ainda lista a reserva "
               "9 como 'Em Analise'. A reserva 8, cancelada ontem, ja aparece como 'Cancelado'.",
       observacao="Uma consulta direta ao banco (tbpedido_reserva) ja mostra a reserva 9 como "
                  "'Cancelado'. A mesma consulta GET /api/pedidos repetida cerca de 5 minutos "
                  "depois traz o status novo."),
    # fonte: CobaiaAPI/app/routers/pedidos.py:53-66 (criar_pedido faz db.commit() ANTES de
    # apply_fault: se a falha sorteada for o 500, erro interno do servidor, a reserva já foi
    # gravada); CobaiaAPI/app/fault_injection.py:158-159 (error_500 levanta ErrorFault) e
    # :118-119 (com probability menor que 1 uma tentativa falha e a seguinte passa). Conferido
    # na rota real: a tentativa que respondeu 500 deixou a reserva gravada.
    # modo da API: error_500 com probability=0.5, em POST /api/pedidos (a 1ª tentativa sorteia a
    # falha, a 2ª não), seguido de GET /api/pedidos?login=11122233344.
    _c("run-27", 5, 3, "registro_duplicado", None,
       ["duplicad", "repetid", "500"], ["erro_interno", "contagem_inconsistente"],
       requisicao="GET /api/pedidos?login=11122233344",
       status=200, contrato=CONTRATO_PEDIDO,
       corpo='[{"id_pedido": 18, "pessoas": 4, "data_pedido": "2026-12-19", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}, '
             '{"id_pedido": 19, "pessoas": 4, "data_pedido": "2026-12-19", '
             '"status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]',
       sintoma="O roteiro envia POST /api/pedidos para uma reserva de 4 pessoas em 2026-12-19: a "
               "primeira tentativa respondeu 500, o roteiro tentou de novo e a segunda respondeu "
               "201. A consulta GET /api/pedidos seguinte lista duas reservas identicas (ids 18 "
               "e 19, mesma data e mesmo numero de pessoas), embora so uma tenha sido pedida.",
       observacao="O corpo mostra so as duas ultimas reservas do cliente. A resposta 500 da "
                  "primeira tentativa nao trouxe nenhuma reserva, so uma mensagem de erro."),
]

# ------------------------------------------------------------- CLASSE 6: efeito
# Causas usadas: localizador_quebrado (4) e estado_da_tela_divergente (2). A rede está normal e a
# falha está no roteiro ou na tela, então nenhum modo da API produz o defeito em si; só o efe-26
# usa um modo (latency com probability menor que 1) para fazer uma resposta chegar fora de ordem.
# Cenários descritos a partir do código de produtos_api.php, com a árvore da tela montada por
# _arvore (mesmos 14 produtos do seed.sql).
CASOS_INEDITOS_FASE4 += [
    # fonte: CobaiaFront/produtos_api.php:82 (o botão é criado com class "btn btn-info btn-xs
    # saiba-mais" e data-id, sem atributo id) e :69-88 (cartaoProduto); CobaiaFront/banco/
    # seed.sql:19-20 (ids 3 e 4).
    # modo da API: sem modo (a falha é do roteiro; GET /api/produtos responde 200 normal).
    _c("efe-22", 6, 1, "localizador_quebrado", None,
       ["seletor", "localizador", "data-id"], ["tempo_de_resposta", "campo_ausente"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na '
             'hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", '
             '"destaque": false}, '
             '{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", '
             '"tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]',
       arvore=_arvore([("Fraldinha", "Carnes", "R$ 69,90", 3),
                       ("Costelona", "Carnes", "R$ 79,90", 4)]),
       seletor_quebrado="#saiba-mais-3",
       sintoma="O passo 'abrir os detalhes da Fraldinha' do roteiro falha ao clicar em "
               "#saiba-mais-3: o Playwright espera 5 segundos e desiste sem ter encontrado nenhum "
               "elemento com esse seletor. A grade apareceu inteira, sem mensagem de erro, e GET "
               "/api/produtos respondeu 200."),
    # fonte: CobaiaFront/produtos_api.php:76 (o nome do produto é um h3 com strong) e :27 (o único
    # h2 da página é 'Produtos via API'); CobaiaFront/banco/seed.sql:22-23 (ids 6 e 7).
    # modo da API: sem modo (a falha é do roteiro; GET /api/produtos responde 200 normal).
    _c("efe-23", 6, 1, "localizador_quebrado", None,
       ["seletor", "localizador", "h3"], ["tempo_de_resposta", "campo_ausente"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", '
             '"tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}, '
             '{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", '
             '"tipo": "Carnes", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}]',
       arvore=_arvore([("Maminha", "Carnes", "R$ 72,90", 6),
                       ("Cupim", "Carnes", "R$ 76,90", 7)]),
       seletor_quebrado='h2:has-text("Cupim")',
       sintoma="A verificacao 'o titulo do Cupim esta visivel' do roteiro falha: o seletor "
               "h2:has-text(\"Cupim\") nao encontra nenhum elemento. O cartao do Cupim aparece "
               "normalmente na tela e GET /api/produtos respondeu 200."),
    # fonte: CobaiaFront/produtos_api.php:81-82 (dentro do mesmo <p> o primeiro botão é o de
    # preço, sem handler, e o 'Saiba Mais...' é o segundo) e :112-114 (o clique só reage a
    # elementos com a classe saiba-mais); CobaiaFront/banco/seed.sql:21-22 (ids 5 e 6).
    # modo da API: sem modo (a falha é do roteiro; GET /api/produtos responde 200 normal).
    _c("efe-24", 6, 2, "localizador_quebrado", None,
       ["seletor", "botao", "preco"], ["recurso_inexistente", "tempo_de_resposta"],
       requisicao="GET /api/produtos",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='[{"id": 5, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na '
             'pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", '
             '"destaque": false}, '
             '{"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", '
             '"tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}]',
       arvore=_arvore([("Alcatra na Pedra", "Carnes", "R$ 74,90", 5),
                       ("Maminha", "Carnes", "R$ 72,90", 6)]),
       seletor_quebrado='.thumbnail:has-text("Alcatra na Pedra") button >> nth=0',
       sintoma="O passo 'abrir os detalhes da Alcatra na Pedra' clica no seletor sem erro, mas o "
               "modal nao abre: o passo seguinte, que espera #modalDetalhe visivel, esgota o "
               "tempo. Depois do clique nao aparece nenhuma requisicao GET /api/produtos/5 na "
               "rede."),
    # fonte: CobaiaFront/produtos_api.php:45 (o título do modal é <h4 id="modalDetalheTitulo">, sem
    # a classe modal-title) e :121 (o título recebe p.nome); CobaiaFront/banco/seed.sql:19 (id 3).
    # modo da API: sem modo (a falha é do roteiro; GET /api/produtos/3 responde 200 normal).
    _c("efe-25", 6, 2, "localizador_quebrado", None,
       ["seletor", "localizador", "modal-title"], ["estado_da_tela", "tempo_de_resposta"],
       requisicao="GET /api/produtos/3",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na '
             'hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", '
             '"destaque": false}',
       arvore=_arvore([("Fraldinha", "Carnes", "R$ 69,90", 3),
                       ("Costelona", "Carnes", "R$ 79,90", 4)],
                      modal=("Fraldinha", "Corte grelhado na brasa, fatiado na hora")),
       seletor_quebrado="#modalDetalhe .modal-title",
       sintoma="Depois do clique em 'Saiba Mais...' da Fraldinha, o modal aparece na tela com o "
               "titulo 'Fraldinha', mas a verificacao do roteiro, que le o texto de "
               "'#modalDetalhe .modal-title', esgota o tempo sem encontrar o elemento. GET "
               "/api/produtos/3 respondeu 200 com os dados certos."),
    # fonte: CobaiaFront/produtos_api.php:112-130 (cada clique faz o seu fetch e escreve no mesmo
    # modal quando a resposta chega; nada cancela o fetch anterior nem confere se a resposta
    # ainda é a do último clique); CobaiaAPI/app/fault_injection.py:118-119 e :154-156 (com
    # latency e probability menor que 1 só alguns pedidos esperam 2 s); CobaiaFront/banco/
    # seed.sql:19 e :25 (ids 3 e 9).
    # modo da API: latency com probability=0.5, em GET /api/produtos/{id} (sorteio deste caso:
    # a requisição do id 3 espera 2 s, a do id 9 não).
    _c("efe-26", 6, 3, "estado_da_tela_divergente", None,
       ["estado", "tela", "ordem"], ["tempo_de_resposta", "chave_de_juncao"],
       requisicao="GET /api/produtos/9",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", '
             '"tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", '
             '"destaque": true}',
       arvore=_arvore([("Fraldinha", "Carnes", "R$ 69,90", 3),
                       ("Balde de Cerveja", "Bebidas", "R$ 45,00", 9)],
                      modal=("Fraldinha", "Corte grelhado na brasa, fatiado na hora")),
       sintoma="O roteiro clica em 'Saiba Mais...' da Fraldinha e, logo em seguida, no do Balde "
               "de Cerveja. As duas requisicoes (GET /api/produtos/3 e GET /api/produtos/9) "
               "respondem 200 com o corpo certo, mas a de id 3 chega cerca de 2 segundos depois "
               "da de id 9. O modal fica com o titulo e a descricao da Fraldinha; a verificacao "
               "esperava o Balde de Cerveja.",
       observacao="O corpo mostrado e o da ultima requisicao disparada (id 9); a resposta do id "
                  "3 tambem tinha o corpo certo."),
    # fonte: CobaiaFront/produtos_api.php:90-110 e :132 (a lista é buscada uma única vez, quando
    # a página abre; carregarProdutos() não é chamada de novo) e :104 (grid.innerHTML só é
    # reescrito por essa chamada); CobaiaFront/banco/seed.sql:18 (id 2: 84.90).
    # modo da API: sem modo (cenário descrito: o preço foi alterado no banco depois da carga).
    _c("efe-27", 6, 3, "estado_da_tela_divergente", None,
       ["estado", "tela", "recarreg"], ["dado_desatualizado", "escala"],
       requisicao="GET /api/produtos/2",
       status=200, contrato=CONTRATO_PRODUTO,
       corpo='{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", '
             '"tipo": "Carnes", "preco": 94.9, "imagem": "picanha_sem.jpg", '
             '"destaque": false}',
       arvore=_arvore([("Picanha ao Alho", "Carnes", "R$ 89,90", 1),
                       ("Picanha Simples", "Carnes", "R$ 84,90", 2)]),
       sintoma="A pagina foi aberta as 10:00 e mostrou a Picanha Simples por 'R$ 84,90'. As 10:05 "
               "o preco desse produto foi alterado no banco para 94,90. As 10:07 o roteiro "
               "consultou GET /api/produtos/2, que respondeu 200 com preco 94.9, e comparou com "
               "o cartao, que continua mostrando 'R$ 84,90'.",
       observacao="A pagina nao foi recarregada entre as 10:00 e as 10:07."),
]
