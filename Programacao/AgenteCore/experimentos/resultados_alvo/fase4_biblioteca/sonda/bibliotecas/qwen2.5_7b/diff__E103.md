<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-102 -> epoca-103), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-102 -> epoca-103

| Métrica | Valor |
|---|---|
| Arquivos novos | 1 |
| Arquivos removidos | 0 |
| Arquivos tocados | 3 |
| Linhas acrescentadas | 26 |
| Linhas removidas | 2 |
| Caracteres antes | 72871 |
| Caracteres depois | 74788 |
| Caracteres acrescentados | 1917 |
| Tokens estimados acrescentados | 737 |

```diff
--- epoca-102/contratos/contrato-produto.md
+++ epoca-103/contratos/contrato-produto.md
@@ -12,9 +12,10 @@
 endpoints: [GET /api/produtos, GET /api/produtos/{id}]
 tabelas: [tbprodutos, tbtipos]
 sintomas: [chave a mais ou a menos, lista no lugar de objeto, preco como texto, lista incompleta, ultimo item cortado]
-palavras_chave: [contrato, produtos, id, nome, resumo, tipo, preco, imagem, destaque, lista, objeto, 404, produto nao encontrado, schema, json]
+palavras_chave: [contrato, produtos, id, nome, resumo, tipo, preco, imagem, destaque, lista, objeto, 404, produto nao encontrado, schema, json, api, front-end]
 causas_relacionadas: [campo_ausente, campo_renomeado, colecao_no_lugar_de_objeto, tipo_divergente, recurso_inexistente]
 # ! Alteração por modelo qwen2.5:7b (E1, caso lex-5) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E103, caso sin-15) - Revisar: nota acrescentada.
 ---
 ## Resumo
 GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.
@@ -28,3 +29,4 @@
 
 ## Notas do modelo
 - [E1 · lex-5 · nota] Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta. — Motivo: Destacar a necessidade de incluir o risco de truncamento de resposta no contrato, pois é uma causa comum de problemas de integração.
+- [E103 · sin-15 · nota] Adicionar nota sobre a necessidade de tratar a categoria como uma string, não uma lista, no front-end. — Motivo: Este trecho não destaca a necessidade de tratar a categoria como uma string no front-end, o que contribuiu para a confusão no diagnóstico atual.
--- epoca-102/erros/campo_ausente.md
+++ epoca-103/erros/campo_ausente.md
@@ -12,9 +12,10 @@
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
 endpoints: [GET /api/produtos, GET /api/pedidos]
 sintomas: [cartao sem titulo, sem nome, undefined na tela, botao que nao faz nada, nulo_inesperado]
-palavras_chave: [ausente, falta, faltando, sem o campo, undefined, field_missing, chave]
+palavras_chave: [ausente, falta, faltando, sem o campo, undefined, field_missing, chave, campo ausente, json, front-end]
 causas_relacionadas: [campo_renomeado, nulo_inesperado, estrutura_aninhada_divergente]
 # ! Alteração por modelo qwen2.5:7b (E1, caso sin-1) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E103, caso efe-3) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Uma chave do contrato não vem no objeto — nem com nulo. No JavaScript a leitura vira undefined.
@@ -28,3 +29,4 @@
 
 ## Notas do modelo
 - [E1 · sin-1 · nota] Adicionar nota sobre a remoção de campos no fault_injection.py. — Motivo: O caso demonstrou que a remoção de campos pode causar sintomas como 'undefined', indicando a necessidade de documentar melhor esse cenário.
+- [E103 · efe-3 · nota] Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. — Motivo: Este caso mostrou que a falta de um campo no JSON pode causar problemas visuais no front-end, evidenciando a importância de manter a consistência entre o contrato e a implementação.
--- epoca-102/erros/corpo_nao_e_json.md
+++ epoca-103/erros/corpo_nao_e_json.md
@@ -16,6 +16,7 @@
 # ! Alteração por modelo qwen2.5:7b (E1, caso lex-2) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5:7b (E1, caso lex-9) - Revisar: nota acrescentada.
 # ! Alteração pelo harness da Fase 4 (correção, caso lex-9, 2026-11-04) - Revisar: status avançou de ativo para corrigido.
+# ! Alteração por modelo qwen2.5:7b (E103, caso lex-9) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.
@@ -36,3 +37,4 @@
 ## Notas do modelo
 - [E1 · lex-2 · nota] Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. — Motivo: Este exemplo mostra que a documentação não abrange casos onde o erro é causado por uma página de erro HTML em vez de JSON, o que pode ser um sintoma comum de problemas de conexão ou falhas do servidor.
 - [E1 · lex-9 · nota] Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho. — Motivo: Este caso mostrou que XML também pode causar parse falho, mas a documentação não destaca isso.
+- [E103 · lex-9 · nota] Adicionar um exemplo de sintoma específico, como "Página de erro XML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. — Motivo: Este caso mostrou que XML também pode causar parse falho, mas a documentação não explicitava isso.
--- epoca-102/aprendidos/corpo_xml_nao_e_json.md
+++ epoca-103/aprendidos/corpo_xml_nao_e_json.md
@@ -0,0 +1,18 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 103 a partir do caso lex-9 (Fase 3).
+# ! Motivo: Este caso mostrou que XML também pode causar parse falho, mas a documentação não explicitava isso.
+id: corpo_xml_nao_e_json
+titulo: Corpo não é XML
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: aprendido
+status: ativo
+sintomas: [pagina de erro xml em vez de json]
+palavras_chave: [xml, parse, erro]
+causas_relacionadas: [corpo_nao_e_json]
+---
+## Resumo
+Adicionar um exemplo de sintoma específico, como "Página de erro XML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON.
+
+## Sinais
+- pagina de erro xml em vez de json
```
