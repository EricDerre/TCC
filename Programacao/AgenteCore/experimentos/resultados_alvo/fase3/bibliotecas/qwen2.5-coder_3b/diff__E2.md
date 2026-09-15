<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-1 -> epoca-2), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-1 -> epoca-2

| Métrica | Valor |
|---|---|
| Arquivos novos | 0 |
| Arquivos removidos | 0 |
| Arquivos tocados | 3 |
| Linhas acrescentadas | 16 |
| Linhas removidas | 6 |
| Caracteres antes | 49429 |
| Caracteres depois | 50963 |
| Caracteres acrescentados | 1534 |
| Tokens estimados acrescentados | 590 |

```diff
--- epoca-1/contratos/contrato-pedido.md
+++ epoca-2/contratos/contrato-pedido.md
@@ -11,9 +11,10 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaFront/cliente/index.php]
 endpoints: [GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
 tabelas: [tbpedido_reserva, tbusuarios]
-sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado]
-palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar]
+sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado, status fora dos valores]
+palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar, pedido, api]
 causas_relacionadas: [formato_de_data_divergente, valor_fora_do_dominio, recurso_inexistente, campo_ausente]
+# ! Alteração por modelo qwen2.5-coder:3b (E2, caso lex-13) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf.
@@ -24,3 +25,6 @@
 
 ## Causa
 cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
+
+## Notas do modelo
+- [E2 · lex-13 · retificação de "status fora dos dois valores"] Corrigido o contrato para aceitar apenas 'Em Análise' e 'Cancelado' como status. — Motivo: O erro estava ocorrendo porque o contrato não especificava os valores permitidos para o status, e o sistema estava retornando 'Em Análise' e 'Cancelado' como valores válidos. A correção agora especifica que apenas esses valores são aceitos.
--- epoca-1/erros/dado_desatualizado.md
+++ epoca-2/erros/dado_desatualizado.md
@@ -11,10 +11,11 @@
 causa_raiz: dado_desatualizado
 arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/database.py]
 endpoints: [GET /api/pedidos, GET /api/produtos]
-sintomas: [reserva nova nao aparece, cancelamento volta a ativo ao recarregar, produto novo demora a aparecer, carga de dados nao atualizada]
-palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale, api, leitura, atualizacao]
+sintomas: [reserva nova nao aparece, cancelamento volta a ativo ao recarregar, produto novo demora a aparecer, carga de dados nao atualizada, leitura defasada, dados nao atualizados na api]
+palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale, api, leitura, atualizacao, leitura defasada, banco de dados]
 causas_relacionadas: [estado_da_tela_divergente, registro_duplicado, contagem_inconsistente]
 # ! Alteração por modelo qwen2.5-coder:3b (E1, caso run-11) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:3b (E2, caso run-14) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Uma escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga.
@@ -28,3 +29,4 @@
 
 ## Notas do modelo
 - [E1 · run-11 · retificação de "A escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga."] A API não envia cache, o que pode levar a leituras defasadas. — Motivo: A evidência deste caso é a descrição da leitura defasada, que mostra que a API não está enviando cache, causando a carga de dados não atualizada.
+- [E2 · run-14 · retificação de "A escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga."] A CobaiaAPI não envia cache, o que pode levar a leituras defasadas. — Motivo: A documentação não especifica que a API deve enviar cache, o que pode levar a leituras defasadas.
--- epoca-1/erros/resposta_truncada.md
+++ epoca-2/erros/resposta_truncada.md
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
```
