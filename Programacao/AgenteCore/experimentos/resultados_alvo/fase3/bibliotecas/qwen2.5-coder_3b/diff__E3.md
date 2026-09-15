<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-2 -> epoca-3), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-2 -> epoca-3

| Métrica | Valor |
|---|---|
| Arquivos novos | 1 |
| Arquivos removidos | 0 |
| Arquivos tocados | 2 |
| Linhas acrescentadas | 30 |
| Linhas removidas | 4 |
| Caracteres antes | 50963 |
| Caracteres depois | 52901 |
| Caracteres acrescentados | 1938 |
| Tokens estimados acrescentados | 745 |

```diff
--- epoca-2/contratos/contrato-pedido.md
+++ epoca-3/contratos/contrato-pedido.md
@@ -11,10 +11,11 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaFront/cliente/index.php]
 endpoints: [GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
 tabelas: [tbpedido_reserva, tbusuarios]
-sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado, status fora dos valores]
-palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar, pedido, api]
+sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado, status fora dos valores, status fora dos dois valores]
+palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar, pedido, api, contrato de pedidos, chave de juncao]
 causas_relacionadas: [formato_de_data_divergente, valor_fora_do_dominio, recurso_inexistente, campo_ausente]
 # ! Alteração por modelo qwen2.5-coder:3b (E2, caso lex-13) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:3b (E3, caso tra-2) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf.
@@ -28,3 +29,4 @@
 
 ## Notas do modelo
 - [E2 · lex-13 · retificação de "status fora dos dois valores"] Corrigido o contrato para aceitar apenas 'Em Análise' e 'Cancelado' como status. — Motivo: O erro estava ocorrendo porque o contrato não especificava os valores permitidos para o status, e o sistema estava retornando 'Em Análise' e 'Cancelado' como valores válidos. A correção agora especifica que apenas esses valores são aceitos.
+- [E3 · tra-2 · retificação de "status fora dos dois valores"] O contrato de pedidos permite apenas 'Em Análise' e 'Cancelado' como status. — Motivo: O trecho "status fora dos dois valores" foi retificado para "status fora do domínio", que é mais preciso e clara. A evidência deste caso é a correção no contrato de pedidos, que agora especifica os valores permitidos para o status.
--- epoca-2/erros/estrutura_aninhada_divergente.md
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
--- epoca-2/aprendidos/estado_da_tela_divergente-correto.md
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
