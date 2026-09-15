<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-1 -> epoca-2), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-1 -> epoca-2

| Métrica | Valor |
|---|---|
| Arquivos novos | 0 |
| Arquivos removidos | 0 |
| Arquivos tocados | 6 |
| Linhas acrescentadas | 28 |
| Linhas removidas | 10 |
| Caracteres antes | 59878 |
| Caracteres depois | 63449 |
| Caracteres acrescentados | 3571 |
| Tokens estimados acrescentados | 1373 |

```diff
--- epoca-1/erros/contagem_inconsistente.md
+++ epoca-2/erros/contagem_inconsistente.md
@@ -12,9 +12,10 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_destaque.php]
 endpoints: [GET /api/produtos]
 tabelas: [tbprodutos]
-sintomas: [total diferente dos itens, pagina vazia com total positivo, quatro destaques mas cinco cartoes]
-palavras_chave: [contagem, total, itens, pagina, paginacao, quantidade, destaques, inconsistente, zero]
+sintomas: [total diferente dos itens, pagina vazia com total positivo, quatro destaques mas cinco cartoes, total e lista com numeros diferentes, renderizacao incorreta de destaques]
+palavras_chave: [contagem, total, itens, pagina, paginacao, quantidade, destaques, inconsistente, zero, consulta de produtos, contagem de itens, inconsistencia]
 causas_relacionadas: [estrutura_aninhada_divergente, dado_desatualizado, estado_da_tela_divergente]
+# ! Alteração por modelo qwen2.5-coder:7b (E2, caso tra-14) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Dois números que deveriam bater não batem: total 14 e lista com 1; total 0 com itens; página 2 vazia com total 14; contador de destaques diferente dos cartões.
@@ -25,3 +26,6 @@
 
 ## Causa
 GET /api/produtos devolve a lista crua, sem total nem paginação (produtos.py:34-43); o seed tem 14 produtos, 5 em destaque. Envelope com total indica outra versão.
+
+## Notas do modelo
+- [E2 · tra-14 · nota] Adicionar nota explicando que a contagem de destaques deve ser extraída da lista de produtos retornada pela API, em vez de uma consulta separada. — Motivo: Esta nota ajuda a entender que a contagem de destaques deve ser baseada na lista de produtos retornada, o que explica a inconsistência observada.
--- epoca-1/erros/corpo_nao_e_json.md
+++ epoca-2/erros/corpo_nao_e_json.md
@@ -10,10 +10,12 @@
 status: ativo
 causa_raiz: corpo_nao_e_json
 arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaFront/produtos_api.php]
-sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, pagina html de erro 404, falha de parse]
-palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, resposta json, erro 404]
+sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, pagina html de erro 404, falha de parse, fatal error, memoria esgotada, resposta html, falha ao acessar de fora da rede local, resposta html em vez de json]
+palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, resposta json, erro 404, erro de memoria, php, conexao, resposta html, erro de integracao]
 causas_relacionadas: [resposta_truncada, corpo_vazio, erro_interno_do_servidor]
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso lex-6) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E2, caso lex-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E2, caso lex-15) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.
@@ -27,3 +29,5 @@
 
 ## Notas do modelo
 - [E1 · lex-6 · nota] Adicionar nota: A resposta deve ser um JSON válido, não uma página HTML de erro. — Motivo: A documentação atual não destaca que a resposta deve ser JSON, o que pode levar a diagnósticos incorretos quando a resposta não atende a este formato esperado.
+- [E2 · lex-12 · nota] Adicionar nota: Erros de memória em PHP podem causar respostas HTML inválidas, interrompendo a exibição de dados JSON. — Motivo: O erro de memória em PHP (Fatal error: Allowed memory size exhausted) é uma causa comum de respostas HTML inválidas, o que corresponde ao sintoma observado.
+- [E2 · lex-15 · nota] Adicionar nota explicando que a resposta deve ser JSON válido, não uma página HTML de erro. — Motivo: A nota ajudará a identificar rapidamente a causa da falha, que é a resposta HTML em vez de JSON, especialmente quando a resposta é 200 e o Content-Type indica JSON.
--- epoca-1/erros/escala_ou_unidade_errada.md
+++ epoca-2/erros/escala_ou_unidade_errada.md
@@ -12,12 +12,13 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/models.py]
 endpoints: [GET /api/produtos, GET /api/pedidos]
 tabelas: [tbprodutos, tbpedido_reserva]
-sintomas: [precos cem vezes maiores, precos cem vezes menores, preco arredondado, data um dia antes, dobro de pessoas, data deslocada um dia, precos arredondados, precisao financeira comprometida]
-palavras_chave: [escala, unidade, centavos, reais, fator, cem, arredond, fuso, dia, dobro, multiplic, divid, conversao, decimal, fuso horario, conversao de data, conversao de unidade, valor_produto]
+sintomas: [precos cem vezes maiores, precos cem vezes menores, preco arredondado, data um dia antes, dobro de pessoas, data deslocada um dia, precos arredondados, precisao financeira comprometida, precisao na comanda]
+palavras_chave: [escala, unidade, centavos, reais, fator, cem, arredond, fuso, dia, dobro, multiplic, divid, conversao, decimal, fuso horario, conversao de data, conversao de unidade, valor_produto, float]
 causas_relacionadas: [tipo_divergente, formato_de_data_divergente, chave_de_juncao_errada]
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-6) - Revisar: retificação acrescentada.
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-9) - Revisar: retificação acrescentada.
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-12) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E2, caso tra-12) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Tipo e formato certos, mas o número está noutra escala ou unidade: centavos por reais (8990), fração (0.899), arredondado (90), data deslocada um dia, quantidade dobrada.
@@ -33,3 +34,4 @@
 - [E1 · tra-6 · retificação de "float(valor_produto) direto do DECIMAL"] A conversão de valor_produto deve considerar a escala correta, convertendo DECIMAL(9,2) para float sem alteração. — Motivo: A evidência deste caso mostrou que a conversão direta de DECIMAL para float estava causando a escala errada, o que foi confirmado pela documentação do verbete [escala_ou_unidade_errada].
 - [E1 · tra-9 · retificação de "DATE em isoformat sem fuso"] A API deve converter a data para o fuso horário do cliente antes de retornar. — Motivo: A falta de conversão de fuso horário é a causa raiz do problema, conforme mostrado no caso atual.
 - [E1 · tra-12 · retificação de "float(valor_produto)"] A API deve converter DECIMAL para número considerando a escala correta (100 para centavos). — Motivo: A evidência deste caso mostrou que a API estava simplesmente convertendo DECIMAL para número sem considerar a escala correta, resultando em preços arredondados.
+- [E2 · tra-12 · retificação de "float(valor_produto)"] A conversão de DECIMAL para float deve considerar a escala correta, convertendo DECIMAL(9,2) para float sem alteração. — Motivo: Esta correção resolve o problema de preços arredondados, pois garante que o valor seja convertido corretamente sem perda de precisão. A evidência deste caso mostrou que a conversão direta estava causando o problema.
--- epoca-1/erros/localizador_quebrado.md
+++ epoca-2/erros/localizador_quebrado.md
@@ -10,12 +10,13 @@
 status: ativo
 causa_raiz: localizador_quebrado
 arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_geral.php]
-sintomas: [elemento nao encontrado, tempo esgotado procurando elemento, seletor casou dois elementos, texto do botao diferente, elementos reais de produtos_api.php, lista da api nao tem order by, roteiro nao localiza elementos, botoes desabilitados, confusao]
-palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout, seletores, elementos, api, localizacao, ambiguidade]
+sintomas: [elemento nao encontrado, tempo esgotado procurando elemento, seletor casou dois elementos, texto do botao diferente, elementos reais de produtos_api.php, lista da api nao tem order by, roteiro nao localiza elementos, botoes desabilitados, confusao, tempo de resposta excedido, localizador quebrado]
+palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout, seletores, elementos, api, localizacao, ambiguidade, order by]
 causas_relacionadas: [estado_da_tela_divergente, recurso_inexistente]
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-6) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-9) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E2, caso efe-6) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado.
@@ -31,3 +32,4 @@
 - [E1 · efe-6 · nota] Adicionar nota explicando que o localizador pode ser quebrado devido à ausência de ORDER BY na lista da API, o que pode causar problemas de localização de elementos. — Motivo: Esta nota ajudará a identificar que o problema está no localizador e não nos dados, explicando a causa raiz do erro.
 - [E1 · efe-9 · nota] Adicionar exemplos de seletores corretos para diferentes elementos na documentação. — Motivo: A evidência deste caso mostrou que o problema estava no localizador, não no dado, e que a documentação não tinha exemplos claros de como selecionar elementos corretamente.
 - [E1 · efe-12 · nota] Adicionar nota sobre seletores quebrados e ambiguidade em elementos. — Motivo: A notificação ajudará a identificar problemas de seletores quebrados e ambiguidade em elementos, facilitando a correção desses problemas.
+- [E2 · efe-6 · nota] Adicionar ORDER BY na consulta SQL em produtos.py para garantir a ordem dos produtos na lista. — Motivo: A ausência de ORDER BY na lista da API pode causar problemas de localização de elementos, como o localizador quebrado, resultando em tempo de resposta excedido.
--- epoca-1/erros/tipo_divergente.md
+++ epoca-2/erros/tipo_divergente.md
@@ -11,10 +11,11 @@
 causa_raiz: tipo_divergente
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py]
 endpoints: [GET /api/produtos, GET /api/pedidos]
-sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada, preco como texto, destaque como texto]
-palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal, conversao de tipos, api, json]
+sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada, preco como texto, destaque como texto, destaque como numero]
+palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal, conversao de tipos, api, json, destaque]
 causas_relacionadas: [valor_fora_do_dominio, formato_de_data_divergente, escala_ou_unidade_errada]
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso semt-13) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E2, caso semt-10) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Chave certa com o tipo JSON errado: número entre aspas ("89.90"), booleano como texto ("Sim") ou número (1), inteiro como texto ("4").
@@ -28,3 +29,4 @@
 
 ## Notas do modelo
 - [E1 · semt-13 · retificação de "O modo type_drift aplica str() ao campo-alvo"] Ajustar a função de conversão de tipos para garantir que os valores sejam retornados no formato correto conforme o contrato. — Motivo: A evidência deste caso mostrou que a função de conversão de tipos estava aplicando str() ao campo-alvo, o que resultava em valores incorretamente formatados. A correção desta função deve resolver o problema de exibição incorreta dos preços.
+- [E2 · semt-10 · retificação de "destaque fora de true/false sai literal"] Ajustar a função de conversão de tipos para garantir que o valor 'Sim' seja convertido em true e 'Não' em false. — Motivo: A evidência deste caso mostrou que a função de conversão de tipos estava aplicando str() ao campo-alvo, o que resultava em valores não booleanos. Ajustar a função para retornar valores booleanos conforme o contrato corrigiria o problema.
--- epoca-1/negocio/entidade-produto.md
+++ epoca-2/negocio/entidade-produto.md
@@ -14,6 +14,7 @@
 sintomas: [nome da categoria no titulo do cartao, preco com grandeza estranha]
 palavras_chave: [produto, categoria, tipo, preco, destaque, imagem, resumo, cardapio, picanha]
 causas_relacionadas: [chave_de_juncao_errada, escala_ou_unidade_errada, tipo_divergente]
+# ! Alteração por modelo qwen2.5-coder:7b (E2, caso tra-7) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90.
@@ -24,3 +25,6 @@
 
 ## Causa
 valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.
+
+## Notas do modelo
+- [E2 · tra-7 · retificação de "14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90."] Corrigir a descrição do produto 1 para "14 produtos; o id 1 é Picanha ao Alho, Carnes, Picanha ao Alho, 89,90." — Motivo: A descrição do produto 1 está incorreta, o nome do produto e a categoria estão misturados. A correção desta informação na documentação ajudará a evitar diagnósticos incorretos no futuro.
```
