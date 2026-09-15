<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-0 -> epoca-1), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-0 -> epoca-1

| Métrica | Valor |
|---|---|
| Arquivos novos | 0 |
| Arquivos removidos | 0 |
| Arquivos tocados | 3 |
| Linhas acrescentadas | 20 |
| Linhas removidas | 6 |
| Caracteres antes | 47502 |
| Caracteres depois | 49429 |
| Caracteres acrescentados | 1927 |
| Tokens estimados acrescentados | 741 |

```diff
--- epoca-0/erros/campo_renomeado.md
+++ epoca-1/erros/campo_renomeado.md
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
+++ epoca-1/erros/corpo_nao_e_json.md
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
+++ epoca-1/erros/dado_desatualizado.md
@@ -11,9 +11,10 @@
 causa_raiz: dado_desatualizado
 arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/database.py]
 endpoints: [GET /api/pedidos, GET /api/produtos]
-sintomas: [reserva nova nao aparece, cancelamento volta a ativo ao recarregar, produto novo demora a aparecer]
-palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale]
+sintomas: [reserva nova nao aparece, cancelamento volta a ativo ao recarregar, produto novo demora a aparecer, carga de dados nao atualizada]
+palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale, api, leitura, atualizacao]
 causas_relacionadas: [estado_da_tela_divergente, registro_duplicado, contagem_inconsistente]
+# ! Alteração por modelo qwen2.5-coder:3b (E1, caso run-11) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Uma escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga.
@@ -24,3 +25,6 @@
 
 ## Causa
 A CobaiaAPI consulta o banco a cada requisição (database.py) e não envia cache; leitura defasada indica proxy ou cache do navegador entre a página e a API.
+
+## Notas do modelo
+- [E1 · run-11 · retificação de "A escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga."] A API não envia cache, o que pode levar a leituras defasadas. — Motivo: A evidência deste caso é a descrição da leitura defasada, que mostra que a API não está enviando cache, causando a carga de dados não atualizada.
```
