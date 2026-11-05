<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-101 -> epoca-102), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-101 -> epoca-102

| Métrica | Valor |
|---|---|
| Arquivos novos | 0 |
| Arquivos removidos | 0 |
| Arquivos tocados | 4 |
| Linhas acrescentadas | 32 |
| Linhas removidas | 4 |
| Caracteres antes | 70597 |
| Caracteres depois | 72871 |
| Caracteres acrescentados | 2274 |
| Tokens estimados acrescentados | 875 |

```diff
--- epoca-101/erros/campo_renomeado.md
+++ epoca-102/erros/campo_renomeado.md
@@ -7,7 +7,7 @@
 sistema: CobaiaAPI
 entidade_principal: Produto
 tipo: erro
-status: ativo
+status: corrigido
 causa_raiz: campo_renomeado
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaAPI/app/schemas.py]
 endpoints: [GET /api/produtos, GET /api/pedidos]
@@ -15,6 +15,7 @@
 palavras_chave: [renomead, outro nome, _v2, descricao, situacao, imagem_url, field_renamed, chave inesperada, campo-renomeado, contrato, cliente]
 causas_relacionadas: [campo_ausente, estrutura_aninhada_divergente]
 # ! Alteração por modelo qwen2.5:7b (E1, caso sin-9) - Revisar: retificação acrescentada.
+# ! Alteração pelo harness da Fase 4 (correção, caso sin-9, 2026-11-04) - Revisar: status avançou de ativo para corrigido.
 ---
 ## Resumo
 O valor existe sob outra chave: falta a esperada e aparece uma desconhecida com o mesmo tipo e conteúdo (preco → preco_v2, nome → descricao, status → situacao).
@@ -26,5 +27,11 @@
 ## Causa
 O modo field_renamed troca o campo-alvo por <campo>_v2 (fault_injection.py). Fora dele: contrato mudou no servidor sem atualizar o cliente.
 
+## Solução sugerida
+- [sin-9 · 2026-11-04] Corrigir a afirmação para "Contrato mudou no servidor sem atualizar o cliente e API não reflete as mudanças."
+
+## Solução aplicada
+- [sin-9 · 2026-11-04] Em 2026-11-04, o cenário api-catalogo do caso sin-9 voltou a passar com o modo field_renamed desligado: no fio, o campo nome voltou ao corpo; 1 diferença contra o contrato antes e 0 depois; na tela, 3 linhas da árvore voltaram e 3 sumiram.
+
 ## Notas do modelo
 - [E1 · sin-9 · retificação de "Fora dele: contrato mudou no servidor sem atualizar o cliente."] Corrigir a afirmação para "Contrato mudou no servidor sem atualizar o cliente e API não reflete as mudanças." — Motivo: O caso mostrou que a documentação não refletiu a necessidade de atualizar o cliente quando o contrato muda, causando a renomeação do campo sem que o cliente o refletisse.
--- epoca-101/erros/corpo_nao_e_json.md
+++ epoca-102/erros/corpo_nao_e_json.md
@@ -7,7 +7,7 @@
 sistema: Ambos
 entidade_principal: Infraestrutura
 tipo: erro
-status: ativo
+status: corrigido
 causa_raiz: corpo_nao_e_json
 arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaFront/produtos_api.php]
 sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, parse_falho, listagem_nao_carrega]
@@ -15,6 +15,7 @@
 causas_relacionadas: [resposta_truncada, corpo_vazio, erro_interno_do_servidor]
 # ! Alteração por modelo qwen2.5:7b (E1, caso lex-2) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5:7b (E1, caso lex-9) - Revisar: nota acrescentada.
+# ! Alteração pelo harness da Fase 4 (correção, caso lex-9, 2026-11-04) - Revisar: status avançou de ativo para corrigido.
 ---
 ## Resumo
 A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.
@@ -26,6 +27,12 @@
 ## Causa
 Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página.
 
+## Solução sugerida
+- [lex-9 · 2026-11-04] Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho.
+
+## Solução aplicada
+- [lex-9 · 2026-11-04] Em 2026-11-04, o cenário api-catalogo do caso lex-9 voltou a passar com o modo corpo_nao_e_json desligado: no fio, 1 diferença contra o contrato antes e 0 depois; na tela, 22 linhas da árvore voltaram e 4 sumiram.
+
 ## Notas do modelo
 - [E1 · lex-2 · nota] Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. — Motivo: Este exemplo mostra que a documentação não abrange casos onde o erro é causado por uma página de erro HTML em vez de JSON, o que pode ser um sintoma comum de problemas de conexão ou falhas do servidor.
 - [E1 · lex-9 · nota] Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho. — Motivo: Este caso mostrou que XML também pode causar parse falho, mas a documentação não destaca isso.
--- epoca-101/erros/estrutura_aninhada_divergente.md
+++ epoca-102/erros/estrutura_aninhada_divergente.md
@@ -7,7 +7,7 @@
 sistema: CobaiaAPI
 entidade_principal: Produto
 tipo: erro
-status: ativo
+status: corrigido
 causa_raiz: estrutura_aninhada_divergente
 arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/schemas.py]
 endpoints: [GET /api/produtos]
@@ -15,6 +15,7 @@
 palavras_chave: [aninhad, envelope, data, itens, objeto, nivel, profundidade, object Object, stringify, estrutura, aninhamento, divergencia]
 causas_relacionadas: [colecao_no_lugar_de_objeto, campo_renomeado, contagem_inconsistente]
 # ! Alteração por modelo qwen2.5:7b (E1, caso sin-13) - Revisar: retificação acrescentada.
+# ! Alteração pelo harness da Fase 4 (correção, caso sin-13, 2026-11-04) - Revisar: status avançou de ativo para corrigido.
 ---
 ## Resumo
 Chaves existem, mas noutro nível: lista num envelope ({"data": {"itens": [...]}}) ou campo simples como objeto ({"id": 1, "nome": "Carnes"}).
@@ -26,5 +27,11 @@
 ## Causa
 Contrato real: lista crua na raiz e tipo como texto (produtos.py _to_dict); envelope ou aninhamento veio de outra versão ou intermediário.
 
+## Solução sugerida
+- [sin-13 · 2026-11-04] Adicionar exemplo de estrutura aninhada divergente no verbete.
+
+## Solução aplicada
+- [sin-13 · 2026-11-04] Em 2026-11-04, o cenário api-catalogo do caso sin-13 voltou a passar com o modo estrutura_aninhada_divergente desligado: no fio, o campo tipo voltou ao corpo; 1 diferença contra o contrato antes e 0 depois; 14 valores voltaram ao da referência; na tela, 3 linhas da árvore voltaram e 3 sumiram.
+
 ## Notas do modelo
 - [E1 · sin-13 · retificação de "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'})."] Adicionar exemplo de estrutura aninhada divergente no verbete. — Motivo: O exemplo de sintoma observado mostrou que a estrutura pode variar entre um envelope e um campo simples, necessitando de um exemplo explícito no verbete.
--- epoca-101/erros/recurso_inexistente.md
+++ epoca-102/erros/recurso_inexistente.md
@@ -7,7 +7,7 @@
 sistema: CobaiaAPI
 entidade_principal: Infraestrutura
 tipo: erro
-status: ativo
+status: corrigido
 causa_raiz: recurso_inexistente
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/routers/admin_fault.py]
 endpoints: [GET /api/produtos/{id}, GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
@@ -15,6 +15,7 @@
 palavras_chave: [404, not found, nao encontrado, inexistente, rota, endpoint, singular, plural, 403, 422, detail, campo de busca errado]
 causas_relacionadas: [erro_interno_do_servidor, localizador_quebrado]
 # ! Alteração por modelo qwen2.5:7b (E1, caso run-7) - Revisar: nota acrescentada.
+# ! Alteração pelo harness da Fase 4 (correção, caso run-7, 2026-11-04) - Revisar: status avançou de ativo para corrigido.
 ---
 ## Resumo
 404: id ou rota inexistente. O detail diz qual: "produto não encontrado" (produtos.py:52), "cliente não encontrado" (pedidos.py:37,52), "pedido não encontrado" (pedidos.py:74); "Not Found" genérico é rota inexistente (ex.: /api/produto).
@@ -26,5 +27,11 @@
 ## Causa
 Cada 404 com mensagem vem de db.get/filter vazio na rota.
 
+## Solução sugerida
+- [run-7 · 2026-11-04] Adicionar um exemplo de campo de busca errado, como login × id, para ilustrar melhor a causa raiz.
+
+## Solução aplicada
+- [run-7 · 2026-11-04] Em 2026-11-04, o cenário api-detalhe do caso run-7 voltou a passar com o modo recurso_inexistente desligado: no fio, os campos id, nome, resumo, tipo, preco, imagem, destaque, detail voltaram ao corpo; 9 diferenças contra o contrato antes e 1 depois; na tela, 25 linhas da árvore voltaram e 4 sumiram.
+
 ## Notas do modelo
 - [E1 · run-7 · nota] Adicionar um exemplo de campo de busca errado, como login × id, para ilustrar melhor a causa raiz. — Motivo: Este exemplo ilustra uma situação que pode causar confusão, mostrando que mesmo com um ID válido, o erro 404 pode ocorrer devido a um campo de busca incorreto.
```
