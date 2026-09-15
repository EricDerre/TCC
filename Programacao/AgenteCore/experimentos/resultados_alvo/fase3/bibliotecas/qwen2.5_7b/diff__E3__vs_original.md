<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-0 -> epoca-3), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-0 -> epoca-3

| Métrica | Valor |
|---|---|
| Arquivos novos | 9 |
| Arquivos removidos | 0 |
| Arquivos tocados | 23 |
| Linhas acrescentadas | 352 |
| Linhas removidas | 35 |
| Caracteres antes | 47502 |
| Caracteres depois | 81481 |
| Caracteres acrescentados | 33979 |
| Tokens estimados acrescentados | 13069 |

```diff
--- epoca-0/contratos/contrato-produto.md
+++ epoca-3/contratos/contrato-produto.md
@@ -11,9 +11,13 @@
 arquivos: [Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaAPI/app/routers/produtos.py]
 endpoints: [GET /api/produtos, GET /api/produtos/{id}]
 tabelas: [tbprodutos, tbtipos]
-sintomas: [chave a mais ou a menos, lista no lugar de objeto, preco como texto]
-palavras_chave: [contrato, produtos, id, nome, resumo, tipo, preco, imagem, destaque, lista, objeto, 404, produto nao encontrado]
+sintomas: [chave a mais ou a menos, lista no lugar de objeto, preco como texto, lista incompleta, ultimo item cortado, lista onde se espera objeto, ou o inverso, nulo_inesperado, valor_fora_do_dominio]
+palavras_chave: [contrato, produtos, id, nome, resumo, tipo, preco, imagem, destaque, lista, objeto, 404, produto nao encontrado, schema, json, campos, divergencia, convercao]
 causas_relacionadas: [campo_ausente, campo_renomeado, colecao_no_lugar_de_objeto, tipo_divergente, recurso_inexistente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-5) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-6) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-13) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso semt-6) - Revisar: nota acrescentada.
 ---
 ## Resumo
 GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.
@@ -24,3 +28,9 @@
 
 ## Causa
 Origem tbprodutos + rótulo de tbtipos (produtos.py _to_dict). preco sai 89.9 (número), embora o schema declare Decimal.
+
+## Notas do modelo
+- [E1 · lex-5 · nota] Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta. — Motivo: Destacar a necessidade de incluir o risco de truncamento de resposta no contrato, pois é uma causa comum de problemas de integração.
+- [E1 · sin-6 · retificação de "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano."] Corrigir "preco número" para "preco Decimal" para refletir o tipo correto em valor_produto. — Motivo: Este trecho mostra a divergência entre o tipo declarado no contrato e o tipo real na resposta, evidenciando a necessidade de manter a consistência entre ambos.
+- [E1 · sin-13 · retificação de "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano."] Adicionar observação sobre possíveis nomes diferentes para o campo tipo no verbete. — Motivo: O caso mostrou que o campo tipo pode ser renomeado ou ter seu tipo divergente, necessitando de uma observação explícita no verbete.
+- [E2 · semt-6 · nota] Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda a necessidade de converção correta do tipo de dados no front-end. — Motivo: Este caso mostrou que a documentação do contrato não aborda a necessidade de converção correta do tipo de dados no front-end, o que pode levar a erros como o ID vindo como uma string.
--- epoca-0/erros/campo_ausente.md
+++ epoca-3/erros/campo_ausente.md
@@ -11,9 +11,12 @@
 causa_raiz: campo_ausente
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
 endpoints: [GET /api/produtos, GET /api/pedidos]
-sintomas: [cartao sem titulo, sem nome, undefined na tela, botao que nao faz nada]
-palavras_chave: [ausente, falta, faltando, sem o campo, undefined, field_missing, chave]
+sintomas: [cartao sem titulo, sem nome, undefined na tela, botao que nao faz nada, nulo_inesperado, undefined no botao de preco]
+palavras_chave: [ausente, falta, faltando, sem o campo, undefined, field_missing, chave, front-end, json, campo ausente, formatacao]
 causas_relacionadas: [campo_renomeado, nulo_inesperado, estrutura_aninhada_divergente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-1) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E3, caso sin-1) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E3, caso sin-6) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Uma chave do contrato não vem no objeto — nem com nulo. No JavaScript a leitura vira undefined.
@@ -24,3 +27,8 @@
 
 ## Causa
 O modo field_missing remove o campo-alvo (fault_injection.py). Diferença para campo_renomeado: nenhuma chave nova aparece no lugar.
+
+## Notas do modelo
+- [E1 · sin-1 · nota] Adicionar nota sobre a remoção de campos no fault_injection.py. — Motivo: O caso demonstrou que a remoção de campos pode causar sintomas como 'undefined', indicando a necessidade de documentar melhor esse cenário.
+- [E3 · sin-1 · nota] Adicionar nota sobre a remoção de campos no fault_injection.py e a necessidade de formatação correta do preço no front-end. — Motivo: O sintoma mostrou que o campo preco estava ausente, indicando a necessidade de notas adicionais na documentação.
+- [E3 · sin-6 · nota] Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. — Motivo: O sintoma mostrou que a falta do campo "nome" causou o problema, e a nota ajudaria a prevenir futuros diagnósticos semelhantes.
--- epoca-0/erros/campo_renomeado.md
+++ epoca-3/erros/campo_renomeado.md
@@ -11,9 +11,10 @@
 causa_raiz: campo_renomeado
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaAPI/app/schemas.py]
 endpoints: [GET /api/produtos, GET /api/pedidos]
-sintomas: [chave desconhecida no lugar da esperada, _v2, campo com outro nome]
-palavras_chave: [renomead, outro nome, _v2, descricao, situacao, imagem_url, field_renamed, chave inesperada]
+sintomas: [chave desconhecida no lugar da esperada, _v2, campo com outro nome, titulo vazio, nome correto, categoria e preco corretos]
+palavras_chave: [renomead, outro nome, _v2, descricao, situacao, imagem_url, field_renamed, chave inesperada, campo-renomeado, contrato, cliente]
 causas_relacionadas: [campo_ausente, estrutura_aninhada_divergente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-9) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 O valor existe sob outra chave: falta a esperada e aparece uma desconhecida com o mesmo tipo e conteúdo (preco → preco_v2, nome → descricao, status → situacao).
@@ -24,3 +25,6 @@
 
 ## Causa
 O modo field_renamed troca o campo-alvo por <campo>_v2 (fault_injection.py). Fora dele: contrato mudou no servidor sem atualizar o cliente.
+
+## Notas do modelo
+- [E1 · sin-9 · retificação de "Fora dele: contrato mudou no servidor sem atualizar o cliente."] Corrigir a afirmação para "Contrato mudou no servidor sem atualizar o cliente e API não reflete as mudanças." — Motivo: O caso mostrou que a documentação não refletiu a necessidade de atualizar o cliente quando o contrato muda, causando a renomeação do campo sem que o cliente o refletisse.
--- epoca-0/erros/chave_de_juncao_errada.md
+++ epoca-3/erros/chave_de_juncao_errada.md
@@ -13,8 +13,9 @@
 endpoints: [GET /api/produtos, GET /api/pedidos]
 tabelas: [tbprodutos, tbtipos, tbusuarios, tbpedido_reserva]
 sintomas: [nome de outra pessoa na reserva, categoria errada, imagem de outro produto, nome da categoria no titulo]
-palavras_chave: [juncao, join, chave, id, fk, cliente errado, categoria errada, troca, admin, like, substring]
+palavras_chave: [juncao, join, chave, id, fk, cliente errado, categoria errada, troca, admin, like, substring, registro errado, campo derivado]
 causas_relacionadas: [nulo_inesperado, escala_ou_unidade_errada, valor_fora_do_dominio]
+# ! Alteração por modelo qwen2.5:7b (E1, caso tra-3) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Tipo e formato certos, mas o valor é de OUTRO registro: categoria ou imagem alheia no produto, nome ou cpf de outro usuário na reserva.
@@ -25,3 +26,6 @@
 
 ## Causa
 Junções: id_tipo_produto e id_clientes (models.py). No site, cliente/index.php:4 usa LIKE '%login%' — CPF substring de outro casa mais de um cliente.
+
+## Notas do modelo
+- [E1 · tra-3 · retificação de "Tipo e formato certos, mas o valor é de OUTRO registro: categoria ou imagem alheia no produto, nome ou cpf de outro usuário na reserva. Sinais: afeta campo derivado de junção (tipo, nome, cpf, imagem), não os próprios; o dado existe no banco, ligado ao registro errado. Causa: Junções: id_tipo_produto e id_clientes (models.py). No site, cliente/index.php:4 usa LIKE '%login%' — CPF substring de outro casa mais de um cliente."] Corrigir a junção entre tbprodutos e tbtipos, garantindo que id_tipo_produto esteja corretamente ligado a tbtipos.id_tipo. — Motivo: O sintoma mostrou que a categoria do produto estava incorreta, indicando uma junção errada entre as tabelas.
--- epoca-0/erros/colecao_no_lugar_de_objeto.md
+++ epoca-3/erros/colecao_no_lugar_de_objeto.md
@@ -14,6 +14,8 @@
 sintomas: [detalhe sem preencher campos, colchetes ao redor do valor, nenhum produto retornado]
 palavras_chave: [lista, array, colecao, objeto, unico, recurso, colchetes, detalhe, modal]
 causas_relacionadas: [estrutura_aninhada_divergente, campo_ausente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-8) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-15) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (["Carnes"]).
@@ -24,3 +26,7 @@
 
 ## Causa
 GET /api/produtos devolve lista, GET /api/produtos/{id} objeto (produtos.py); a página não confere a forma antes de ler os campos.
+
+## Notas do modelo
+- [E1 · sin-8 · retificação de "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes'])."] Corrigir que GET /api/produtos/{id} deve devolver um objeto, não uma lista. — Motivo: O caso mostrou que a documentação não especificava claramente que GET /api/produtos/{id} deve retornar um único objeto, causando confusão.
+- [E1 · sin-15 · retificação de "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes'])."] Corrigir que o campo "tipo" deve ser tratado como uma string, não uma lista. — Motivo: O sintoma mostrou que o campo "tipo" foi tratado como uma lista, quando na verdade é uma string.
--- epoca-0/erros/contagem_inconsistente.md
+++ epoca-3/erros/contagem_inconsistente.md
@@ -12,9 +12,11 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_destaque.php]
 endpoints: [GET /api/produtos]
 tabelas: [tbprodutos]
-sintomas: [total diferente dos itens, pagina vazia com total positivo, quatro destaques mas cinco cartoes]
-palavras_chave: [contagem, total, itens, pagina, paginacao, quantidade, destaques, inconsistente, zero]
+sintomas: [total diferente dos itens, pagina vazia com total positivo, quatro destaques mas cinco cartoes, contagem de destaques incorreta, renderizacao de cartoes]
+palavras_chave: [contagem, total, itens, pagina, paginacao, quantidade, destaques, inconsistente, zero, renderizacao, home]
 causas_relacionadas: [estrutura_aninhada_divergente, dado_desatualizado, estado_da_tela_divergente]
+# ! Alteração por modelo qwen2.5:7b (E2, caso tra-14) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso tra-14) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Dois números que deveriam bater não batem: total 14 e lista com 1; total 0 com itens; página 2 vazia com total 14; contador de destaques diferente dos cartões.
@@ -25,3 +27,7 @@
 
 ## Causa
 GET /api/produtos devolve a lista crua, sem total nem paginação (produtos.py:34-43); o seed tem 14 produtos, 5 em destaque. Envelope com total indica outra versão.
+
+## Notas do modelo
+- [E2 · tra-14 · nota] Adicionar nota sobre a necessidade de verificar a consistência entre a contagem de itens na resposta e a renderização na interface, especialmente em endpoints que retornam listas paginadas. — Motivo: Este caso mostrou que a inconsistência entre a contagem de itens na resposta e a renderização na interface é um problema comum, mas a documentação não destaca a importância de verificar essa consistência em endpoints paginados.
+- [E2 · tra-14 · retificação de "contador de destaques diferente dos cartões. Sinais: total e lista vêm de consultas diferentes; rótulo numérico que não corresponde ao renderizado."] Corrigir que destaque booleano saia literal, garantindo que seja convertido corretamente para True ou False. — Motivo: Esta retificação corrigirá a conversão do destaque booleano, mas também destaca a importância de verificar a consistência entre a contagem de itens na resposta e a renderização na interface, especialmente em endpoints paginados.
--- epoca-0/erros/corpo_nao_e_json.md
+++ epoca-3/erros/corpo_nao_e_json.md
@@ -10,9 +10,14 @@
 status: ativo
 causa_raiz: corpo_nao_e_json
 arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaFront/produtos_api.php]
-sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json]
-palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type]
+sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, parse_falho, listagem_nao_carrega, pagina de erro html em vez de json, aviso antes do json, parse falho no primeiro caractere]
+palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, erro de sintaxe, parse_falho, aviso, parse falho]
 causas_relacionadas: [resposta_truncada, corpo_vazio, erro_interno_do_servidor]
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-2) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-9) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso lex-2) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso lex-2) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E3, caso lex-6) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.
@@ -23,3 +28,10 @@
 
 ## Causa
 Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página.
+
+## Notas do modelo
+- [E1 · lex-2 · nota] Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. — Motivo: Este exemplo mostra que a documentação não abrange casos onde o erro é causado por uma página de erro HTML em vez de JSON, o que pode ser um sintoma comum de problemas de conexão ou falhas do servidor.
+- [E1 · lex-9 · nota] Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho. — Motivo: Este caso mostrou que XML também pode causar parse falho, mas a documentação não destaca isso.
+- [E2 · lex-2 · nota] Adicionar que sintomas podem incluir avisos antes do JSON e parse falhos no primeiro caractere. — Motivo: Este caso mostrou que avisos HTML podem preceder o JSON, causando parse falhos, e que sintomas específicos como esses devem ser documentados.
+- [E2 · lex-2 · nota] Adicionar exemplos específicos de sintomas, como "Página de erro HTML em vez de JSON" e "aviso antes do JSON", para melhor identificação de casos onde o corpo da resposta não é JSON. — Motivo: Este caso mostrou que precisamos de exemplos mais detalhados de sintomas para diagnóstico preciso, como avisos antes do JSON e parse falhos no primeiro caractere.
+- [E3 · lex-6 · nota] Adicionar que parse falhos podem ocorrer com qualquer tipo de corpo não JSON, não apenas HTML. — Motivo: Este caso mostrou que o parse falho pode ocorrer com respostas HTML, não apenas JSON, precisando ser explicitado na documentação.
--- epoca-0/erros/corpo_vazio.md
+++ epoca-3/erros/corpo_vazio.md
@@ -13,6 +13,8 @@
 sintomas: [carregando indefinidamente, tela em branco sem erro, fim inesperado da entrada em corpo vazio]
 palavras_chave: [vazio, sem corpo, branco, 204, espacos, nenhum byte, carregando]
 causas_relacionadas: [resposta_truncada, corpo_nao_e_json, estado_da_tela_divergente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-13) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-13) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Status de sucesso e nenhum byte útil no corpo (vazio, só espaços, ou 204). Diferente de "[]", lista vazia, que é JSON válido.
@@ -23,3 +25,7 @@
 
 ## Causa
 Nenhuma rota da CobaiaAPI devolve 204 nem corpo vazio; se chega vazio, foi cortado antes de sair (servidor, proxy) ou a rota errada respondeu.
+
+## Notas do modelo
+- [E1 · lex-13 · nota] Adicionar exemplo de sintoma: "Tabela de reservas vazia, sem erro." — Motivo: Este exemplo mostra que a falta de dados no corpo da resposta pode ser indiretamente observada pela ausência de conteúdo na interface, sem necessariamente retornar um erro, o que não estava claramente documentado.
+- [E1 · lex-13 · nota] Adicionar: "Nenhuma resposta ou resposta vazia pode ser retornada por nenhuma rota da CobaiaAPI." — Motivo: Este exemplo ilustra que a ausência de resposta ou resposta vazia é uma condição que deve ser explicitamente verificada, pois ela não retorna um erro HTTP, mas pode afetar a interface.
--- epoca-0/erros/dado_desatualizado.md
+++ epoca-3/erros/dado_desatualizado.md
@@ -11,9 +11,11 @@
 causa_raiz: dado_desatualizado
 arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/database.py]
 endpoints: [GET /api/pedidos, GET /api/produtos]
-sintomas: [reserva nova nao aparece, cancelamento volta a ativo ao recarregar, produto novo demora a aparecer]
-palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale]
+sintomas: [reserva nova nao aparece, cancelamento volta a ativo ao recarregar, produto novo demora a aparecer, status inconsistente, reserva cancelada aparecendo como ativa]
+palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale, api, get, php, leitura_defasada, atualizacao_em_tempo_real]
 causas_relacionadas: [estado_da_tela_divergente, registro_duplicado, contagem_inconsistente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso run-11) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso run-14) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Uma escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga.
@@ -24,3 +26,7 @@
 
 ## Causa
 A CobaiaAPI consulta o banco a cada requisição (database.py) e não envia cache; leitura defasada indica proxy ou cache do navegador entre a página e a API.
+
+## Notas do modelo
+- [E1 · run-11 · retificação de "Sinais: cabeçalhos Age ou Cache-Control: max-age no GET; o painel PHP (lê o banco direto) já mostra o dado; só a API atrasa."] Adicionar "A leitura defasada indica que a API está lendo dados antigos do banco, enquanto o painel PHP atualiza em tempo real." — Motivo: Este texto destaca a causa raiz do problema, mostrando que a desatualização dos dados é devido à API ler dados antigos do banco, enquanto o painel PHP atualiza em tempo real, o que não foi evidente no caso original.
+- [E2 · run-14 · nota] Notar que a desatualização pode ser causada por um cache intermediário ou do navegador. — Motivo: Este texto destaca a possibilidade de cache como causa de desatualização, ajudando a diferenciar casos onde a API está atualizada do cache do navegador ou proxy.
--- epoca-0/erros/erro_interno_do_servidor.md
+++ epoca-3/erros/erro_interno_do_servidor.md
@@ -12,8 +12,11 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/conn/connect.php]
 endpoints: [GET /api/produtos, POST /api/pedidos]
 sintomas: [HTTP 500, Internal Server Error, fault injection error_500, falha intermitente]
-palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora]
+palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora, falha_interna, injetor, excecao_nao_tratada, injecao de falha, excecao nao tratada]
 causas_relacionadas: [corpo_nao_e_json, tempo_de_resposta_excedido, limite_de_requisicoes]
+# ! Alteração por modelo qwen2.5:7b (E1, caso run-6) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso run-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso run-12) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 500 com {"detail": ...}: falha própria da API. detail "fault injection: error_500 em produto" é o injetor; "Internal Server Error" é exceção não tratada.
@@ -24,3 +27,8 @@
 
 ## Causa
 Rotas convertem ErrorFault em 500 (produtos.py:42). No site PHP, banco fora NÃO dá 500: imprime "Atenção ERRO" em HTML (connect.php:16).
+
+## Notas do modelo
+- [E1 · run-6 · nota] Adicionar que este erro pode ocorrer devido a falhas no banco de dados ou em rotas, e que a mensagem genérica pode esconder problemas específicos. — Motivo: Este caso mostrou que a mensagem de erro genérica pode esconder problemas específicos, como falhas no banco de dados, que não são explicitamente mencionados na documentação.
+- [E1 · run-12 · nota] Adicionar que este erro pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota. — Motivo: Este caso mostrou que o erro interno do servidor pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota, evidenciando a necessidade de uma nota sobre esse comportamento.
+- [E2 · run-12 · retificação de "500 com {'detail': ...}: falha própria da API. detail 'fault injection: error_500 em produto' é o injetor; 'Internal Server Error' é exceção não tratada."] Corrigir a estrutura da resposta da API para ser consistente, evitando envelopes ou campos simples aninhados, para padronizar o desenpacotamento dos dados. — Motivo: Este caso mostrou que a documentação não abrangia a necessidade de padronização na estrutura da resposta, o que pode levar a diagnósticos incorretos em casos futuros.
--- epoca-0/erros/escala_ou_unidade_errada.md
+++ epoca-3/erros/escala_ou_unidade_errada.md
@@ -13,8 +13,10 @@
 endpoints: [GET /api/produtos, GET /api/pedidos]
 tabelas: [tbprodutos, tbpedido_reserva]
 sintomas: [precos cem vezes maiores, precos cem vezes menores, preco arredondado, data um dia antes, dobro de pessoas]
-palavras_chave: [escala, unidade, centavos, reais, fator, cem, arredond, fuso, dia, dobro, multiplic, divid]
+palavras_chave: [escala, unidade, centavos, reais, fator, cem, arredond, fuso, dia, dobro, multiplic, divid, conversao]
 causas_relacionadas: [tipo_divergente, formato_de_data_divergente, chave_de_juncao_errada]
+# ! Alteração por modelo qwen2.5:7b (E1, caso tra-6) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso tra-12) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Tipo e formato certos, mas o número está noutra escala ou unidade: centavos por reais (8990), fração (0.899), arredondado (90), data deslocada um dia, quantidade dobrada.
@@ -25,3 +27,7 @@
 
 ## Causa
 A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela.
+
+## Notas do modelo
+- [E1 · tra-6 · retificação de "A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela."] Corrigir a conversão do valor_produto para float, aplicando o fator correto. — Motivo: Este caso mostrou que a conversão direta do DECIMAL para float sem aplicar o fator correto resulta em preços errados, evidenciando a necessidade de uma correção na documentação.
+- [E1 · tra-12 · retificação de "Sinais: todos os valores errados pelo mesmo fator: conversão de unidade; só o arredondamento errado. Causa: A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela."] Adicionar exemplo de conversão incorreta de valor_produto DECIMAL(9,2) para float, causando arredondamento. — Motivo: Este caso mostrou que a documentação não era suficiente para alertar sobre a necessidade de conversão correta do valor DECIMAL para float, o que resultou em arredondamento.
--- epoca-0/erros/estado_da_tela_divergente.md
+++ epoca-3/erros/estado_da_tela_divergente.md
@@ -11,9 +11,12 @@
 status: ativo
 causa_raiz: estado_da_tela_divergente
 arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/reserva_cli.php]
-sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar]
-palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML]
+sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar, lista vazia, botao que nao muda]
+palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML, cancelar, redirect]
 causas_relacionadas: [localizador_quebrado, dado_desatualizado, corpo_vazio]
+# ! Alteração por modelo qwen2.5:7b (E1, caso efe-4) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso efe-8) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso efe-10) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 A rede está certa — status e corpo conferem — e o usuário vê outra coisa: "Carregando" parado, lista vazia, botão que não muda.
@@ -24,3 +27,8 @@
 
 ## Causa
 produtos_api.php só limpa "Carregando..." no then() do fetch e substitui o grid por innerHTML; na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).
+
+## Notas do modelo
+- [E1 · efe-4 · retificação de "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7)."] Corrigir a lógica de cancelamento para não depender de redirect, garantindo a atualização do estado da tela. — Motivo: Este caso mostrou que a lógica de atualização da interface não está sincronizada com a resposta da API, evidenciando a necessidade de uma revisão na implementação do cancelamento.
+- [E1 · efe-8 · retificação de "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7)."] Corrigir a implementação do cancelamento para que não dependa apenas do redirect, mas também limpe o estado da tela corretamente. — Motivo: Esta retificação mostra que a implementação atual está incompleta e que o cancelamento deve ser tratado de forma mais robusta, o que pode ajudar a prevenir erros semelhantes no futuro.
+- [E1 · efe-10 · retificação de "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7)."] Corrigir a lógica de cancelamento para não depender do redirect, garantindo que a interface seja atualizada corretamente. — Motivo: Este caso mostrou que a lógica de atualização da interface pode estar incorreta, mesmo com dados corretos na rede. A documentação sobre o estado da tela divergente não foi explicita sobre a necessidade de atualização do DOM.
--- epoca-0/erros/estrutura_aninhada_divergente.md
+++ epoca-3/erros/estrutura_aninhada_divergente.md
@@ -11,9 +11,11 @@
 causa_raiz: estrutura_aninhada_divergente
 arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/schemas.py]
 endpoints: [GET /api/produtos]
-sintomas: [object Object, envelope data, lista dentro de objeto, campo virou objeto]
-palavras_chave: [aninhad, envelope, data, itens, objeto, nivel, profundidade, object Object, stringify]
+sintomas: [object Object, envelope data, lista dentro de objeto, campo virou objeto, envelope na raiz, campo como objeto]
+palavras_chave: [aninhad, envelope, data, itens, objeto, nivel, profundidade, object Object, stringify, estrutura, aninhamento, divergencia]
 causas_relacionadas: [colecao_no_lugar_de_objeto, campo_renomeado, contagem_inconsistente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-13) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso efe-11) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Chaves existem, mas noutro nível: lista num envelope ({"data": {"itens": [...]}}) ou campo simples como objeto ({"id": 1, "nome": "Carnes"}).
@@ -24,3 +26,7 @@
 
 ## Causa
 Contrato real: lista crua na raiz e tipo como texto (produtos.py _to_dict); envelope ou aninhamento veio de outra versão ou intermediário.
+
+## Notas do modelo
+- [E1 · sin-13 · retificação de "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'})."] Adicionar exemplo de estrutura aninhada divergente no verbete. — Motivo: O exemplo de sintoma observado mostrou que a estrutura pode variar entre um envelope e um campo simples, necessitando de um exemplo explícito no verbete.
+- [E1 · efe-11 · retificação de "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'})."] Corrigir a estrutura da resposta da API para ser consistente, evitando envelopes ou campos simples aninhados, para padronizar o desenpacotamento dos dados. — Motivo: Este caso mostrou que a estrutura da resposta pode variar, causando problemas de desenpacotamento, e a documentação não explicitava essa possibilidade.
--- epoca-0/erros/formato_de_data_divergente.md
+++ epoca-3/erros/formato_de_data_divergente.md
@@ -12,9 +12,10 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py]
 endpoints: [GET /api/pedidos, POST /api/pedidos]
 tabelas: [tbpedido_reserva]
-sintomas: [Invalid Date, data como numero, data em formato brasileiro]
-palavras_chave: [data, formato, iso, AAAA-MM-DD, dd/mm/aaaa, timestamp, epoch, Invalid Date, data_pedido]
+sintomas: [Invalid Date, data como numero, data em formato brasileiro, data noutro formato, data deslocada um dia]
+palavras_chave: [data, formato, iso, AAAA-MM-DD, dd/mm/aaaa, timestamp, epoch, Invalid Date, data_pedido, unidade]
 causas_relacionadas: [escala_ou_unidade_errada, tipo_divergente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso tra-9) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 data_pedido deve ser texto AAAA-MM-DD. Chega noutro formato (10/09/2026), como segundos (1789084800) ou com hora e fuso — e o cliente não interpreta.
@@ -25,3 +26,6 @@
 
 ## Causa
 A API devolve data_pedido.isoformat() (pedidos.py:23), sempre AAAA-MM-DD. Em escala_ou_unidade_errada a data é legível mas deslocada; aqui é ilegível.
+
+## Notas do modelo
+- [E1 · tra-9 · retificação de "data_pedido deve ser texto AAAA-MM-DD. Chega noutro formato (10/09/2026), como segundos (1789084800) ou com hora e fuso — e o cliente não interpreta."] Adicione que o formato ISO 8601 é obrigatório e que datas devem ser passadas no formato AAAA-MM-DD, sem hora ou fuso horário. Corrija que o timestamp deve ser convertido para o formato ISO 8601 antes de ser devolvido. — Motivo: Este caso mostrou que a documentação não esclareceu claramente que o formato ISO 8601 é obrigatório e que datas devem ser passadas no formato AAAA-MM-DD, sem hora ou fuso horário.
--- epoca-0/erros/limite_de_requisicoes.md
+++ epoca-3/erros/limite_de_requisicoes.md
@@ -12,8 +12,10 @@
 arquivos: [Programacao/CobaiaAPI/app/main.py, Programacao/CobaiaFront/produtos_api.php]
 endpoints: [GET /api/produtos]
 sintomas: [HTTP 429, too many requests, rate limit, para de funcionar apos varias tentativas]
-palavras_chave: [429, limite, rate limit, too many requests, retry_after, cota, excesso, recarregar]
+palavras_chave: [429, limite, rate limit, too many requests, retry_after, cota, excesso, recarregar, limitador, excesso_de_requisicoes]
 causas_relacionadas: [tempo_de_resposta_excedido, erro_interno_do_servidor]
+# ! Alteração por modelo qwen2.5:7b (E3, caso run-3) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E3, caso run-3) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Status 429: o servidor ou um intermediário recusou por excesso de requisições num intervalo. Resposta rápida e com corpo — não é lentidão nem erro interno.
@@ -24,3 +26,7 @@
 
 ## Causa
 A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado.
+
+## Notas do modelo
+- [E3 · run-3 · retificação de "Causa: A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado."] Corrigir que destaque booleano saia literal, garantindo que seja convertido corretamente para True ou False. — Motivo: Este trecho não aborda a questão do destaque booleano, que é relevante para diagnósticos futuros de inconsistências na interface.
+- [E3 · run-3 · nota] Adicionar nota sobre a necessidade de verificar a consistência entre a contagem de itens na resposta e a renderização na interface, especialmente em endpoints que retornam listas paginadas. — Motivo: Este trecho destaca a importância de verificar a consistência entre contagens e renderizações, que é crucial para diagnósticos futuros de inconsistências na interface.
--- epoca-0/erros/localizador_quebrado.md
+++ epoca-3/erros/localizador_quebrado.md
@@ -11,8 +11,11 @@
 causa_raiz: localizador_quebrado
 arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_geral.php]
 sintomas: [elemento nao encontrado, tempo esgotado procurando elemento, seletor casou dois elementos, texto do botao diferente]
-palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout]
+palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout, elemento, ambiguidade]
 causas_relacionadas: [estado_da_tela_divergente, recurso_inexistente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso efe-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso efe-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso efe-12) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado.
@@ -23,3 +26,8 @@
 
 ## Causa
 Elementos reais de produtos_api.php: #produtos-api-grid, .thumbnail, button.saiba-mais[data-id], #modalDetalhe; a lista da API não tem ORDER BY (produtos.py:38).
+
+## Notas do modelo
+- [E1 · efe-12 · nota] Adicionado que o localizador pode ser ambíguo, encontrando mais de um elemento com o mesmo seletor. — Motivo: Este caso mostrou que o diagnóstico precisa considerar a ambiguidade no seletor, o que não estava claro na documentação original.
+- [E2 · efe-12 · nota] Adicionar que o seletor pode ser ambíguo, encontrando mais de um elemento com o mesmo seletor. — Motivo: Este caso mostrou que a documentação não abrangia a possibilidade de um seletor ser ambíguo, encontrando mais de um elemento, o que pode causar erros na integração.
+- [E2 · efe-12 · retificação de "o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado."] Corrigir para "o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado. A lista da API não tem ORDER BY (produtos.py:38)." — Motivo: Este caso mostrou que a documentação não mencionava explicitamente que a falta de ORDER BY na API pode causar ambiguidade nos seletores, o que pode levar a erros na integração.
--- epoca-0/erros/recurso_inexistente.md
+++ epoca-3/erros/recurso_inexistente.md
@@ -12,8 +12,9 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/routers/admin_fault.py]
 endpoints: [GET /api/produtos/{id}, GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
 sintomas: [HTTP 404, Not Found, produto nao encontrado, cliente nao encontrado, pedido nao encontrado, rota errada]
-palavras_chave: [404, not found, nao encontrado, inexistente, rota, endpoint, singular, plural, 403, 422, detail]
+palavras_chave: [404, not found, nao encontrado, inexistente, rota, endpoint, singular, plural, 403, 422, detail, campo de busca errado]
 causas_relacionadas: [erro_interno_do_servidor, localizador_quebrado]
+# ! Alteração por modelo qwen2.5:7b (E1, caso run-7) - Revisar: nota acrescentada.
 ---
 ## Resumo
 404: id ou rota inexistente. O detail diz qual: "produto não encontrado" (produtos.py:52), "cliente não encontrado" (pedidos.py:37,52), "pedido não encontrado" (pedidos.py:74); "Not Found" genérico é rota inexistente (ex.: /api/produto).
@@ -24,3 +25,6 @@
 
 ## Causa
 Cada 404 com mensagem vem de db.get/filter vazio na rota.
+
+## Notas do modelo
+- [E1 · run-7 · nota] Adicionar um exemplo de campo de busca errado, como login × id, para ilustrar melhor a causa raiz. — Motivo: Este exemplo ilustra uma situação que pode causar confusão, mostrando que mesmo com um ID válido, o erro 404 pode ocorrer devido a um campo de busca incorreto.
--- epoca-0/erros/resposta_truncada.md
+++ epoca-3/erros/resposta_truncada.md
@@ -9,9 +9,12 @@
 status: ativo
 causa_raiz: resposta_truncada
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py]
-sintomas: [fim inesperado da entrada, json cortado, content-length menor que o corpo]
-palavras_chave: [truncad, cortad, incomplet, unexpected end, content-length, tamanho, parcial, malformed_json]
+sintomas: [fim inesperado da entrada, json cortado, content-length menor que o corpo, lista incompleta, ultimo item cortado, corpo cortado]
+palavras_chave: [truncad, cortad, incomplet, unexpected end, content-length, tamanho, parcial, malformed_json, truncamento, conexao, proxy]
 causas_relacionadas: [corpo_nao_e_json, corpo_vazio, tempo_de_resposta_excedido]
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-5) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-14) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso lex-14) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 O corpo começa como JSON válido e termina no meio de um valor ou chave — faltam bytes; o parse falha com "Unexpected end of JSON input".
@@ -22,3 +25,8 @@
 
 ## Causa
 O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio.
+
+## Notas do modelo
+- [E1 · lex-5 · retificação de "Fora dele: limite num proxy, conexão encerrada durante o envio."] Corrigir a descrição para incluir que o truncamento pode ser causado por limites de proxy ou interrupção de conexão. — Motivo: Esclarecer que limites de proxy ou interrupção de conexão podem causar truncamento, ajudando a diagnosticar casos futuros.
+- [E1 · lex-14 · nota] Adicione um exemplo de como verificar o Content-Length na documentação para evitar esse problema. — Motivo: Este caso mostrou que a verificação do Content-Length é crucial para detectar respostas truncadas, e a documentação não aborda isso explicitamente.
+- [E2 · lex-14 · retificação de "Fora dele: limite num proxy, conexão encerrada durante o envio."] Corrigir a descrição para incluir que o truncamento pode ser causado por limites de proxy ou interrupção de conexão. Adicione um exemplo de como verificar o Content-Length na documentação para evitar esse problema. — Motivo: Este caso mostrou que a documentação não abrangia todas as possíveis causas de truncamento da resposta, especificamente relacionadas a limites de proxy ou interrupção de conexão.
--- epoca-0/erros/tempo_de_resposta_excedido.md
+++ epoca-3/erros/tempo_de_resposta_excedido.md
@@ -12,8 +12,9 @@
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
 endpoints: [GET /api/produtos]
 sintomas: [demora de segundos, timeout, conexao encerrada por tempo, carregando por muito tempo]
-palavras_chave: [timeout, lento, lentidao, demora, latencia, segundos, tempo esgotado, volume, 2 s]
+palavras_chave: [timeout, lento, lentidao, demora, latencia, segundos, tempo esgotado, volume, 2 s, tempo limite, atraso, conexao encerrada]
 causas_relacionadas: [limite_de_requisicoes, erro_interno_do_servidor, corpo_vazio]
+# ! Alteração por modelo qwen2.5:7b (E3, caso run-15) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A resposta demora além do aceitável ou nunca chega: sem status (conexão encerrada) ou 200 tardio. 429 e 500 respondem rápido com um código — aqui não.
@@ -24,3 +25,6 @@
 
 ## Causa
 O modo latency dorme 2 s fixos (fault_injection.py:66); atrasos maiores vêm de banco, rede ou carga; o fetch da página não tem tempo limite.
+
+## Notas do modelo
+- [E3 · run-15 · nota] Adicionar que o erro pode ocorrer devido ao tempo limite de resposta configurado no sistema. — Motivo: Este caso mostrou que o tempo limite de resposta pode afetar a integração entre a interface e a API, especialmente quando há muitos produtos a serem listados.
--- epoca-0/erros/tipo_divergente.md
+++ epoca-3/erros/tipo_divergente.md
@@ -11,9 +11,11 @@
 causa_raiz: tipo_divergente
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py]
 endpoints: [GET /api/produtos, GET /api/pedidos]
-sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada]
-palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal]
+sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada, destaque booleano sai literal, categoria errada]
+palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal, convercao, destaque]
 causas_relacionadas: [valor_fora_do_dominio, formato_de_data_divergente, escala_ou_unidade_errada]
+# ! Alteração por modelo qwen2.5:7b (E1, caso semt-13) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E3, caso tra-3) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Chave certa com o tipo JSON errado: número entre aspas ("89.90"), booleano como texto ("Sim") ou número (1), inteiro como texto ("4").
@@ -24,3 +26,7 @@
 
 ## Causa
 O modo type_drift aplica str() ao campo-alvo (fault_injection.py:76). A API converte DECIMAL em número e 'Sim'/'Não' em booleano (_to_dict).
+
+## Notas do modelo
+- [E1 · semt-13 · retificação de "destaque fora de true/false sai literal."] Corrigir que destaque booleano saia literal, garantindo que seja convertido corretamente para True ou False. — Motivo: O caso mostrou que a conversão incorreta de booleano afeta a apresentação do preço, indicando a necessidade de corrigir essa conversão.
+- [E3 · tra-3 · nota] Notar que a junção errada pode afetar campos derivados como tipo, garantindo a precisão na apresentação dos produtos. — Motivo: O sintoma mostrou que a categoria estava incorreta, indicando que a converção incorreta de dados pode afetar a apresentação correta dos produtos.
--- epoca-0/erros/valor_fora_do_dominio.md
+++ epoca-3/erros/valor_fora_do_dominio.md
@@ -12,9 +12,10 @@
 arquivos: [Programacao/CobaiaFront/banco/schema_completo.sql, Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaFront/cliente/registrar_reserva.php]
 endpoints: [GET /api/pedidos, GET /api/produtos]
 tabelas: [tbpedido_reserva, tbprodutos]
-sintomas: [status desconhecido, pessoas zero, destaque 2, reserva sem botao de cancelar]
-palavras_chave: [dominio, enum, permitido, conjunto, status, Pendente, Concluido, pessoas, zero, negativo, destaque]
+sintomas: [status desconhecido, pessoas zero, destaque 2, reserva sem botao de cancelar, botao de cancelar some, status inesperado]
+palavras_chave: [dominio, enum, permitido, conjunto, status, Pendente, Concluido, pessoas, zero, negativo, destaque, validacao]
 causas_relacionadas: [tipo_divergente, formato_de_data_divergente, nulo_inesperado]
+# ! Alteração por modelo qwen2.5:7b (E1, caso semt-11) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Tipo certo, valor fora do conjunto permitido: status diferente de 'Em Análise'/'Cancelado', destaque diferente de true/false, pessoas menor que 1.
@@ -25,3 +26,6 @@
 
 ## Causa
 status e destaque são ENUM no banco (schema_completo.sql:37); pessoas ≥ 1 é só min= do HTML (registrar_reserva.php:55); a API não valida o que devolve.
+
+## Notas do modelo
+- [E1 · semt-11 · retificação de "Valor fora do domínio"] Adicionar validação no status do pedido na API para evitar valores fora do domínio. — Motivo: Este caso mostrou que a API não valida o status do pedido, permitindo valores inválidos como 'Concluido', o que afeta a exibição de botões na interface.
--- epoca-0/negocio/entidade-produto.md
+++ epoca-3/negocio/entidade-produto.md
@@ -11,9 +11,12 @@
 arquivos: [Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/banco/seed.sql]
 endpoints: [GET /api/produtos, GET /api/produtos/{id}]
 tabelas: [tbprodutos, tbtipos]
-sintomas: [nome da categoria no titulo do cartao, preco com grandeza estranha]
-palavras_chave: [produto, categoria, tipo, preco, destaque, imagem, resumo, cardapio, picanha]
+sintomas: [nome da categoria no titulo do cartao, preco com grandeza estranha, nulo_inesperado, escala_ou_unidade_errada, preco cru, separador decimal como virgula, incorreto, tipo errado]
+palavras_chave: [produto, categoria, tipo, preco, destaque, imagem, resumo, cardapio, picanha, convercao, valor, formatacao, decimal, separador]
 causas_relacionadas: [chave_de_juncao_errada, escala_ou_unidade_errada, tipo_divergente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-1) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso semt-13) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso tra-3) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90.
@@ -24,3 +27,8 @@
 
 ## Causa
 valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.
+
+## Notas do modelo
+- [E1 · sin-1 · retificação de "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano."] Corrigir a conversão do preço e destaque no _to_dict de produtos.py. — Motivo: O caso mostrou que a conversão incorreta de tipos pode levar a sintomas como 'undefined' e '89.9', indicando uma necessidade de revisão na conversão de tipos.
+- [E1 · semt-13 · nota] Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. — Motivo: O caso demonstra a importância de uma formatação correta do preço, independentemente da conversão do backend.
+- [E2 · tra-3 · retificação de "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano."] Corrigir a conversão do preço e destaque no _to_dict de produtos.py, garantindo que o preço seja convertido corretamente para Decimal. — Motivo: O caso mostrou que a conversão incorreta do tipo de dado no backend afeta a apresentação do produto no frontend, evidenciando a necessidade de manter a consistência dos tipos de dados.
--- epoca-0/negocio/pedido-reserva.md
+++ epoca-3/negocio/pedido-reserva.md
@@ -11,9 +11,12 @@
 arquivos: [Programacao/CobaiaFront/banco/schema_completo.sql, Programacao/CobaiaFront/cliente/reserva_cli.php, Programacao/CobaiaAPI/app/routers/pedidos.py]
 endpoints: [GET /api/pedidos]
 tabelas: [tbpedido_reserva, vw_tbpedidos, tbusuarios]
-sintomas: [status com texto desconhecido, reserva de outro cliente, linha de reserva vazia]
-palavras_chave: [reserva, pedido, status, em analise, cancelado, pessoas, data_pedido, id_clientes, view]
+sintomas: [status com texto desconhecido, reserva de outro cliente, linha de reserva vazia, reserva_incompleta, reserva_normal, reserva_nao_ativa_nem_cancelada, status_inesperado, reserva_vazia, cliente_sem_reserva]
+palavras_chave: [reserva, pedido, status, em analise, cancelado, pessoas, data_pedido, id_clientes, view, campos_nulos, renderizacao_incorreta, enum, validacao, left_join, nulo, renderizacao]
 causas_relacionadas: [valor_fora_do_dominio, nulo_inesperado, chave_de_juncao_errada]
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-12) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso semt-15) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso semt-15) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Reserva em tbpedido_reserva: id_pedido, id_clientes (chave para tbusuarios), pessoas, data_pedido, status. Status só admite 'Em Análise' (inicial) e 'Cancelado'.
@@ -24,3 +27,8 @@
 
 ## Causa
 A leitura usa vw_tbpedidos, LEFT JOIN de tbusuarios (schema_completo.sql:57): cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza.
+
+## Notas do modelo
+- [E1 · sin-12 · retificação de "cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza."] Corrigir a renderização para não exibir linhas com campos nulos quando o cliente não reservou. — Motivo: Este caso mostrou que a interface web exibe linhas incompletas, indicando uma falha na lógica de renderização quando os campos ausentes não são tratados adequadamente.
+- [E1 · semt-15 · retificação de "Status só admite 'Em Análise' (inicial) e 'Cancelado'."] Adicionar validação no backend para verificar se o status está dentro do domínio permitido. — Motivo: O caso mostrou que a API retorna um status inesperado, que não é tratado pelo frontend, causando o problema de reserva sem pessoas.
+- [E1 · semt-15 · retificação de "A leitura usa vw_tbpedidos, LEFT JOIN de tbusuarios (schema_completo.sql:57): cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza."] Corrigir a lógica do LEFT JOIN para evitar linhas nulas quando o cliente não tem reserva. — Motivo: O caso mostrou que a API retorna linhas nulas para clientes sem reserva, que são renderizadas pelo frontend, causando o problema de reserva não alocada.
--- epoca-0/aprendidos/arredondamento_incorreto.md
+++ epoca-3/aprendidos/arredondamento_incorreto.md
@@ -0,0 +1,20 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 3 a partir do caso tra-5 (Fase 3).
+# ! Motivo: O caso mostrou que a conversão direta do valor_produto pode levar a arredondamento errado, necessitando de uma correção no processo.
+id: arredondamento_incorreto
+titulo: Arredondamento incorreto
+sistema: CobaiaAPI
+entidade_principal: Pedido
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py]
+sintomas: [arredondamento errado, valor_fora_do_dominio]
+palavras_chave: [arredondamento, fator, conversao]
+causas_relacionadas: [escala_ou_unidade_errada]
+---
+## Resumo
+Adicionar exemplo de conversão incorreta de valor_produto DECIMAL(9,2) para float, causando arredondamento.
+
+## Sinais
+- arredondamento errado
+- valor_fora_do_dominio
--- epoca-0/aprendidos/atualizacao_imediata.md
+++ epoca-3/aprendidos/atualizacao_imediata.md
@@ -0,0 +1,15 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso efe-13 (Fase 3).
+# ! Motivo: Este novo verbete explica a prática atual de atualização imediata, que foi a causa da visualização de dados desatualizados neste caso.
+id: atualizacao_imediata
+titulo: Atualização imediata do grid
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/cliente_cancelar.php]
+palavras_chave: [innerhtml, sobrescrita, grid]
+causas_relacionadas: [estado_da_tela_divergente]
+---
+## Resumo
+O grid é atualizado imediatamente com innerHTML, independentemente do status da requisição. Isso pode resultar em visualização de dados antigos.
--- epoca-0/aprendidos/conversao-de-unidade.md
+++ epoca-3/aprendidos/conversao-de-unidade.md
@@ -0,0 +1,19 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso tra-6 (Fase 3).
+# ! Motivo: Este caso demonstra a importância de explicitar a necessidade de aplicar o fator correto na conversão de unidades monetárias, evitando erros de escala.
+id: conversao-de-unidade
+titulo: Conversão de unidade
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py]
+sintomas: [precos cem vezes menores]
+palavras_chave: [fator, decimal, unidade]
+causas_relacionadas: [escala_ou_unidade_errada]
+---
+## Resumo
+Adicionar instruções sobre a necessidade de aplicar o fator correto na conversão do valor_produto.
+
+## Sinais
+- precos cem vezes menores
--- epoca-0/aprendidos/conversao-de-valor.md
+++ epoca-3/aprendidos/conversao-de-valor.md
@@ -0,0 +1,20 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso tra-12 (Fase 3).
+# ! Motivo: Este caso demonstrou a necessidade de uma regra específica para a conversão de valores DECIMAL para float, para evitar arredondamentos incorretos.
+id: conversao-de-valor
+titulo: Conversão de valor DECIMAL para float
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py]
+sintomas: [arredondamento incorreto, valor fora do dominio]
+palavras_chave: [conversao, arredondamento, decimal, float]
+causas_relacionadas: [escala_ou_unidade_errada, valor_fora_do_dominio]
+---
+## Resumo
+Adicionar regra para conversão correta de valor DECIMAL para float no _to_dict.
+
+## Sinais
+- arredondamento incorreto
+- valor fora do dominio
--- epoca-0/aprendidos/interface-estados.md
+++ epoca-3/aprendidos/interface-estados.md
@@ -0,0 +1,19 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso efe-4 (Fase 3).
+# ! Motivo: Este novo verbete ajudaria a documentar a necessidade de estados consistentes na interface, facilitando diagnósticos futuros.
+id: interface-estados
+titulo: Estados da Interface
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: aprendido
+status: ativo
+sintomas: [lista vazia, botao que nao muda]
+palavras_chave: [estado, interface, atualizacao]
+causas_relacionadas: [estado_da_tela_divergente]
+---
+## Resumo
+Definir estados claros para a interface e garantir que a lógica de atualização esteja corretamente implementada.
+
+## Sinais
+- lista vazia
+- botao que nao muda
--- epoca-0/aprendidos/interface-frontend.md
+++ epoca-3/aprendidos/interface-frontend.md
@@ -0,0 +1,14 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso efe-10 (Fase 3).
+# ! Motivo: Este novo verbete ajudaria a documentar a interação entre a API e a interface, destacando a necessidade de atualizações corretas do DOM e a dependência de redirects, prevenindo divergências de estado.
+id: interface-frontend
+titulo: Interface Frontend
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: aprendido
+status: ativo
+palavras_chave: [atualizacao, dom, innerhtml, redirect]
+causas_relacionadas: [estado_da_tela_divergente, tipo_divergente]
+---
+## Resumo
+Adicionar a interface frontend como uma entidade, destacando a importância de atualizações corretas do DOM e a dependência de redirects.
--- epoca-0/aprendidos/rendezvous_hasta.md
+++ epoca-3/aprendidos/rendezvous_hasta.md
@@ -0,0 +1,20 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 2 a partir do caso efe-11 (Fase 3).
+# ! Motivo: Este caso mostrou que a sincronização entre a interface e a API pode ser um problema, especialmente quando há contagem inconsistente, indicando a necessidade de uma abordagem mais robusta para a sincronização.
+id: rendezvous_hasta
+titulo: Rendezvous até
+sistema: Ambos
+entidade_principal: Interface
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/cliente_cancelar.php]
+sintomas: [estado da tela divergente, contagem inconsistente]
+palavras_chave: [rendezvous, sincronizacao, estado_da_tela]
+causas_relacionadas: [estado_da_tela_divergente, contagem_inconsistente]
+---
+## Resumo
+Implementar rendezvous até para garantir que a interface esteja sincronizada com a resposta da API.
+
+## Sinais
+- estado da tela divergente
+- contagem inconsistente
--- epoca-0/aprendidos/rotas-inexistentes.md
+++ epoca-3/aprendidos/rotas-inexistentes.md
@@ -0,0 +1,20 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso run-8 (Fase 3).
+# ! Motivo: Este caso mostrou a necessidade de um verbete dedicado para rotas inexistentes, pois a documentação atual não abrange essa situação específica.
+id: rotas-inexistentes
+titulo: Rotas Inexistentes
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py]
+sintomas: [404 com id valido, rota inexistente]
+palavras_chave: [404, rotas, id, rota]
+causas_relacionadas: [recurso_inexistente]
+---
+## Resumo
+Adicionar um novo verbete para rotas inexistentes, especificando que um 404 com id válido pode indicar que a rota ou recurso buscado não existe.
+
+## Sinais
+- 404 com id valido
+- rota inexistente
--- epoca-0/aprendidos/soma_inconsistente.md
+++ epoca-3/aprendidos/soma_inconsistente.md
@@ -0,0 +1,20 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 3 a partir do caso semt-7 (Fase 3).
+# ! Motivo: O caso mostrou que a soma total de lugares reservados estava incorreta devido ao campo pessoas vindo como uma string, e a junção incorreta pode levar a linhas nulas.
+id: soma_inconsistente
+titulo: Soma inconsistente
+sistema: Ambos
+entidade_principal: Pedido
+tipo: aprendido
+status: ativo
+sintomas: [soma_total_incorreta, campos_nulos, juncao_incorreta]
+palavras_chave: [soma, tipo, juncao]
+causas_relacionadas: [tipo_divergente, chave_de_juncao_errada]
+---
+## Resumo
+Adicionar validação no backend para verificar se a soma de pessoas está correta e corrigir a lógica do LEFT JOIN para evitar linhas nulas.
+
+## Sinais
+- soma_total_incorreta
+- campos_nulos
+- juncao_incorreta
```
