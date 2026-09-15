<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-0 -> epoca-3), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-0 -> epoca-3

| Métrica | Valor |
|---|---|
| Arquivos novos | 1 |
| Arquivos removidos | 0 |
| Arquivos tocados | 6 |
| Linhas acrescentadas | 62 |
| Linhas removidas | 12 |
| Caracteres antes | 47502 |
| Caracteres depois | 52901 |
| Caracteres acrescentados | 5399 |
| Tokens estimados acrescentados | 2077 |

```diff
--- epoca-0/contratos/contrato-pedido.md
+++ epoca-3/contratos/contrato-pedido.md
@@ -11,9 +11,11 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaFront/cliente/index.php]
 endpoints: [GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
 tabelas: [tbpedido_reserva, tbusuarios]
-sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado]
-palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar]
+sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado, status fora dos valores, status fora dos dois valores]
+palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar, pedido, api, contrato de pedidos, chave de juncao]
 causas_relacionadas: [formato_de_data_divergente, valor_fora_do_dominio, recurso_inexistente, campo_ausente]
+# ! Alteração por modelo qwen2.5-coder:3b (E2, caso lex-13) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:3b (E3, caso tra-2) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf.
@@ -24,3 +26,7 @@
 
 ## Causa
 cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
+
+## Notas do modelo
+- [E2 · lex-13 · retificação de "status fora dos dois valores"] Corrigido o contrato para aceitar apenas 'Em Análise' e 'Cancelado' como status. — Motivo: O erro estava ocorrendo porque o contrato não especificava os valores permitidos para o status, e o sistema estava retornando 'Em Análise' e 'Cancelado' como valores válidos. A correção agora especifica que apenas esses valores são aceitos.
+- [E3 · tra-2 · retificação de "status fora dos dois valores"] O contrato de pedidos permite apenas 'Em Análise' e 'Cancelado' como status. — Motivo: O trecho "status fora dos dois valores" foi retificado para "status fora do domínio", que é mais preciso e clara. A evidência deste caso é a correção no contrato de pedidos, que agora especifica os valores permitidos para o status.
--- epoca-0/erros/campo_renomeado.md
+++ epoca-3/erros/campo_renomeado.md
@@ -11,9 +11,10 @@
 causa_raiz: campo_renomeado
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaAPI/app/schemas.py]
 endpoints: [GET /api/produtos, GET /api/pedidos]
-sintomas: [chave desconhecida no lugar da esperada, _v2, campo com outro nome]
-palavras_chave: [renomead, outro nome, _v2, descricao, situacao, imagem_url, field_renamed, chave inesperada]
+sintomas: [chave desconhecida no lugar da esperada, _v2, campo com outro nome, campos ausentes ou renomeados]
+palavras_chave: [renomead, outro nome, _v2, descricao, situacao, imagem_url, field_renamed, chave inesperada, campo renomeado, contrato mudado]
 causas_relacionadas: [campo_ausente, estrutura_aninhada_divergente]
+# ! Alteração por modelo qwen2.5-coder:3b (E1, caso sin-9) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 O valor existe sob outra chave: falta a esperada e aparece uma desconhecida com o mesmo tipo e conteúdo (preco → preco_v2, nome → descricao, status → situacao).
@@ -24,3 +25,6 @@
 
 ## Causa
 O modo field_renamed troca o campo-alvo por <campo>_v2 (fault_injection.py). Fora dele: contrato mudou no servidor sem atualizar o cliente.
+
+## Notas do modelo
+- [E1 · sin-9 · retificação de "preco → preco_v2"] Corrigido o campo_renomeado para preencher o contrato esperado. — Motivo: O campo_renomeado estava causando inconsistências no contrato esperado, tornando o diagnóstico mais preciso para casos futuros.
--- epoca-0/erros/corpo_nao_e_json.md
+++ epoca-3/erros/corpo_nao_e_json.md
@@ -10,9 +10,11 @@
 status: ativo
 causa_raiz: corpo_nao_e_json
 arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaFront/produtos_api.php]
-sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json]
-palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type]
+sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, resposta html, texto legivel antes do json, xml ou aviso em texto]
+palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, parse falha, primeiro caractere]
 causas_relacionadas: [resposta_truncada, corpo_vazio, erro_interno_do_servidor]
+# ! Alteração por modelo qwen2.5-coder:3b (E1, caso lex-2) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:3b (E1, caso lex-12) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.
@@ -23,3 +25,7 @@
 
 ## Causa
 Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página.
+
+## Notas do modelo
+- [E1 · lex-2 · retificação de "o parse falha no primeiro caractere"] Corrige a descrição para especificar que o parse falha no primeiro caractere. — Motivo: O caso atual mostra que o erro ocorre no primeiro caractere, mas a descrição anterior não menciona isso. Esta correção ajuda a evitar confusão com outros tipos de erros de parse.
+- [E1 · lex-12 · retificação de "o parse falha no primeiro caractere"] Ajuste o trecho para "o parse falha no primeiro caractere da resposta". — Motivo: Este trecho melhor descreve o erro específico que pode ocorrer na análise da resposta, ajudando a evitar confusões futuras.
--- epoca-0/erros/dado_desatualizado.md
+++ epoca-3/erros/dado_desatualizado.md
@@ -11,9 +11,11 @@
 causa_raiz: dado_desatualizado
 arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/database.py]
 endpoints: [GET /api/pedidos, GET /api/produtos]
-sintomas: [reserva nova nao aparece, cancelamento volta a ativo ao recarregar, produto novo demora a aparecer]
-palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale]
+sintomas: [reserva nova nao aparece, cancelamento volta a ativo ao recarregar, produto novo demora a aparecer, carga de dados nao atualizada, leitura defasada, dados nao atualizados na api]
+palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale, api, leitura, atualizacao, leitura defasada, banco de dados]
 causas_relacionadas: [estado_da_tela_divergente, registro_duplicado, contagem_inconsistente]
+# ! Alteração por modelo qwen2.5-coder:3b (E1, caso run-11) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:3b (E2, caso run-14) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Uma escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga.
@@ -24,3 +26,7 @@
 
 ## Causa
 A CobaiaAPI consulta o banco a cada requisição (database.py) e não envia cache; leitura defasada indica proxy ou cache do navegador entre a página e a API.
+
+## Notas do modelo
+- [E1 · run-11 · retificação de "A escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga."] A API não envia cache, o que pode levar a leituras defasadas. — Motivo: A evidência deste caso é a descrição da leitura defasada, que mostra que a API não está enviando cache, causando a carga de dados não atualizada.
+- [E2 · run-14 · retificação de "A escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga."] A CobaiaAPI não envia cache, o que pode levar a leituras defasadas. — Motivo: A documentação não especifica que a API deve enviar cache, o que pode levar a leituras defasadas.
--- epoca-0/erros/estrutura_aninhada_divergente.md
+++ epoca-3/erros/estrutura_aninhada_divergente.md
@@ -11,9 +11,10 @@
 causa_raiz: estrutura_aninhada_divergente
 arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/schemas.py]
 endpoints: [GET /api/produtos]
-sintomas: [object Object, envelope data, lista dentro de objeto, campo virou objeto]
-palavras_chave: [aninhad, envelope, data, itens, objeto, nivel, profundidade, object Object, stringify]
+sintomas: [object Object, envelope data, lista dentro de objeto, campo virou objeto, campo como objeto no lugar de texto]
+palavras_chave: [aninhad, envelope, data, itens, objeto, nivel, profundidade, object Object, stringify, estrutura aninhada divergente, contrato produto]
 causas_relacionadas: [colecao_no_lugar_de_objeto, campo_renomeado, contagem_inconsistente]
+# ! Alteração por modelo qwen2.5-coder:3b (E3, caso sin-3) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Chaves existem, mas noutro nível: lista num envelope ({"data": {"itens": [...]}}) ou campo simples como objeto ({"id": 1, "nome": "Carnes"}).
@@ -24,3 +25,6 @@
 
 ## Causa
 Contrato real: lista crua na raiz e tipo como texto (produtos.py _to_dict); envelope ou aninhamento veio de outra versão ou intermediário.
+
+## Notas do modelo
+- [E3 · sin-3 · retificação de "chaves existem, mas noutro nível"] Adicione um novo campo "tipo" no contrato de /api/produtos para especificar que o campo deve ser um texto. — Motivo: O contrato atual não especifica que o campo "tipo" deve ser um texto, o que pode levar a erros de integração futuros.
--- epoca-0/erros/resposta_truncada.md
+++ epoca-3/erros/resposta_truncada.md
@@ -9,9 +9,10 @@
 status: ativo
 causa_raiz: resposta_truncada
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py]
-sintomas: [fim inesperado da entrada, json cortado, content-length menor que o corpo]
-palavras_chave: [truncad, cortad, incomplet, unexpected end, content-length, tamanho, parcial, malformed_json]
+sintomas: [fim inesperado da entrada, json cortado, content-length menor que o corpo, parse falha, json invalido]
+palavras_chave: [truncad, cortad, incomplet, unexpected end, content-length, tamanho, parcial, malformed_json, json parsing, api falha]
 causas_relacionadas: [corpo_nao_e_json, corpo_vazio, tempo_de_resposta_excedido]
+# ! Alteração por modelo qwen2.5-coder:3b (E2, caso lex-14) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 O corpo começa como JSON válido e termina no meio de um valor ou chave — faltam bytes; o parse falha com "Unexpected end of JSON input".
@@ -22,3 +23,6 @@
 
 ## Causa
 O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio.
+
+## Notas do modelo
+- [E2 · lex-14 · retificação de "o parse falha com 'Unexpected end of JSON input'."] Corrigir o parsing JSON para lidar com erros de truncamento. — Motivo: O erro de truncamento pode ser causado por problemas de comunicação, então melhorar o parsing JSON ajuda a evitar erros futuros.
--- epoca-0/aprendidos/estado_da_tela_divergente-correto.md
+++ epoca-3/aprendidos/estado_da_tela_divergente-correto.md
@@ -0,0 +1,20 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5-coder:3b na época 3 a partir do caso efe-13 (Fase 3).
+# ! Motivo: O novo verbete explica que o problema ocorre quando o then() limpa "Carregando..." e substitui o grid por innerHTML, o que pode causar a tela de mostrar conteúdo anterior.
+id: estado_da_tela_divergente-correto
+titulo: Estado da tela divergente corrigido
+sistema: Ambos
+entidade_principal: Interface
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/cliente_cancelar.php]
+sintomas: [tela mostra conteudo anterior, recarregar nao corrige]
+palavras_chave: [tela divergente, fetch, innerhtml]
+causas_relacionadas: [estado_da_tela_divergente]
+---
+## Resumo
+Corrigido o erro na limpeza do "Carregando..." no then() do fetch.
+
+## Sinais
+- tela mostra conteudo anterior
+- recarregar nao corrige
```
