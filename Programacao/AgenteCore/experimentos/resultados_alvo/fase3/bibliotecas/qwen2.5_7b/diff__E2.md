<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-1 -> epoca-2), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-1 -> epoca-2

| Métrica | Valor |
|---|---|
| Arquivos novos | 1 |
| Arquivos removidos | 0 |
| Arquivos tocados | 8 |
| Linhas acrescentadas | 53 |
| Linhas removidas | 9 |
| Caracteres antes | 69963 |
| Caracteres depois | 76836 |
| Caracteres acrescentados | 6873 |
| Tokens estimados acrescentados | 2643 |

```diff
--- epoca-1/contratos/contrato-produto.md
+++ epoca-2/contratos/contrato-produto.md
@@ -11,12 +11,13 @@
 arquivos: [Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaAPI/app/routers/produtos.py]
 endpoints: [GET /api/produtos, GET /api/produtos/{id}]
 tabelas: [tbprodutos, tbtipos]
-sintomas: [chave a mais ou a menos, lista no lugar de objeto, preco como texto, lista incompleta, ultimo item cortado, lista onde se espera objeto, ou o inverso]
-palavras_chave: [contrato, produtos, id, nome, resumo, tipo, preco, imagem, destaque, lista, objeto, 404, produto nao encontrado, schema, json, campos, divergencia]
+sintomas: [chave a mais ou a menos, lista no lugar de objeto, preco como texto, lista incompleta, ultimo item cortado, lista onde se espera objeto, ou o inverso, nulo_inesperado, valor_fora_do_dominio]
+palavras_chave: [contrato, produtos, id, nome, resumo, tipo, preco, imagem, destaque, lista, objeto, 404, produto nao encontrado, schema, json, campos, divergencia, convercao]
 causas_relacionadas: [campo_ausente, campo_renomeado, colecao_no_lugar_de_objeto, tipo_divergente, recurso_inexistente]
 # ! Alteração por modelo qwen2.5:7b (E1, caso lex-5) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5:7b (E1, caso sin-6) - Revisar: retificação acrescentada.
 # ! Alteração por modelo qwen2.5:7b (E1, caso sin-13) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso semt-6) - Revisar: nota acrescentada.
 ---
 ## Resumo
 GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.
@@ -32,3 +33,4 @@
 - [E1 · lex-5 · nota] Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta. — Motivo: Destacar a necessidade de incluir o risco de truncamento de resposta no contrato, pois é uma causa comum de problemas de integração.
 - [E1 · sin-6 · retificação de "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano."] Corrigir "preco número" para "preco Decimal" para refletir o tipo correto em valor_produto. — Motivo: Este trecho mostra a divergência entre o tipo declarado no contrato e o tipo real na resposta, evidenciando a necessidade de manter a consistência entre ambos.
 - [E1 · sin-13 · retificação de "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano."] Adicionar observação sobre possíveis nomes diferentes para o campo tipo no verbete. — Motivo: O caso mostrou que o campo tipo pode ser renomeado ou ter seu tipo divergente, necessitando de uma observação explícita no verbete.
+- [E2 · semt-6 · nota] Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda a necessidade de converção correta do tipo de dados no front-end. — Motivo: Este caso mostrou que a documentação do contrato não aborda a necessidade de converção correta do tipo de dados no front-end, o que pode levar a erros como o ID vindo como uma string.
--- epoca-1/erros/contagem_inconsistente.md
+++ epoca-2/erros/contagem_inconsistente.md
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
--- epoca-1/erros/corpo_nao_e_json.md
+++ epoca-2/erros/corpo_nao_e_json.md
@@ -10,11 +10,13 @@
 status: ativo
 causa_raiz: corpo_nao_e_json
 arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaFront/produtos_api.php]
-sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, parse_falho, listagem_nao_carrega]
-palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, erro de sintaxe, parse_falho]
+sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, parse_falho, listagem_nao_carrega, pagina de erro html em vez de json, aviso antes do json, parse falho no primeiro caractere]
+palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, erro de sintaxe, parse_falho, aviso, parse falho]
 causas_relacionadas: [resposta_truncada, corpo_vazio, erro_interno_do_servidor]
 # ! Alteração por modelo qwen2.5:7b (E1, caso lex-2) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5:7b (E1, caso lex-9) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso lex-2) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso lex-2) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.
@@ -29,3 +31,5 @@
 ## Notas do modelo
 - [E1 · lex-2 · nota] Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. — Motivo: Este exemplo mostra que a documentação não abrange casos onde o erro é causado por uma página de erro HTML em vez de JSON, o que pode ser um sintoma comum de problemas de conexão ou falhas do servidor.
 - [E1 · lex-9 · nota] Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho. — Motivo: Este caso mostrou que XML também pode causar parse falho, mas a documentação não destaca isso.
+- [E2 · lex-2 · nota] Adicionar que sintomas podem incluir avisos antes do JSON e parse falhos no primeiro caractere. — Motivo: Este caso mostrou que avisos HTML podem preceder o JSON, causando parse falhos, e que sintomas específicos como esses devem ser documentados.
+- [E2 · lex-2 · nota] Adicionar exemplos específicos de sintomas, como "Página de erro HTML em vez de JSON" e "aviso antes do JSON", para melhor identificação de casos onde o corpo da resposta não é JSON. — Motivo: Este caso mostrou que precisamos de exemplos mais detalhados de sintomas para diagnóstico preciso, como avisos antes do JSON e parse falhos no primeiro caractere.
--- epoca-1/erros/dado_desatualizado.md
+++ epoca-2/erros/dado_desatualizado.md
@@ -12,9 +12,10 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/database.py]
 endpoints: [GET /api/pedidos, GET /api/produtos]
 sintomas: [reserva nova nao aparece, cancelamento volta a ativo ao recarregar, produto novo demora a aparecer, status inconsistente, reserva cancelada aparecendo como ativa]
-palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale, api, get, php]
+palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale, api, get, php, leitura_defasada, atualizacao_em_tempo_real]
 causas_relacionadas: [estado_da_tela_divergente, registro_duplicado, contagem_inconsistente]
 # ! Alteração por modelo qwen2.5:7b (E1, caso run-11) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso run-14) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Uma escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga.
@@ -28,3 +29,4 @@
 
 ## Notas do modelo
 - [E1 · run-11 · retificação de "Sinais: cabeçalhos Age ou Cache-Control: max-age no GET; o painel PHP (lê o banco direto) já mostra o dado; só a API atrasa."] Adicionar "A leitura defasada indica que a API está lendo dados antigos do banco, enquanto o painel PHP atualiza em tempo real." — Motivo: Este texto destaca a causa raiz do problema, mostrando que a desatualização dos dados é devido à API ler dados antigos do banco, enquanto o painel PHP atualiza em tempo real, o que não foi evidente no caso original.
+- [E2 · run-14 · nota] Notar que a desatualização pode ser causada por um cache intermediário ou do navegador. — Motivo: Este texto destaca a possibilidade de cache como causa de desatualização, ajudando a diferenciar casos onde a API está atualizada do cache do navegador ou proxy.
--- epoca-1/erros/erro_interno_do_servidor.md
+++ epoca-2/erros/erro_interno_do_servidor.md
@@ -12,10 +12,11 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/conn/connect.php]
 endpoints: [GET /api/produtos, POST /api/pedidos]
 sintomas: [HTTP 500, Internal Server Error, fault injection error_500, falha intermitente]
-palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora, falha_interna, injetor, excecao_nao_tratada]
+palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora, falha_interna, injetor, excecao_nao_tratada, injecao de falha, excecao nao tratada]
 causas_relacionadas: [corpo_nao_e_json, tempo_de_resposta_excedido, limite_de_requisicoes]
 # ! Alteração por modelo qwen2.5:7b (E1, caso run-6) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5:7b (E1, caso run-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso run-12) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 500 com {"detail": ...}: falha própria da API. detail "fault injection: error_500 em produto" é o injetor; "Internal Server Error" é exceção não tratada.
@@ -30,3 +31,4 @@
 ## Notas do modelo
 - [E1 · run-6 · nota] Adicionar que este erro pode ocorrer devido a falhas no banco de dados ou em rotas, e que a mensagem genérica pode esconder problemas específicos. — Motivo: Este caso mostrou que a mensagem de erro genérica pode esconder problemas específicos, como falhas no banco de dados, que não são explicitamente mencionados na documentação.
 - [E1 · run-12 · nota] Adicionar que este erro pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota. — Motivo: Este caso mostrou que o erro interno do servidor pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota, evidenciando a necessidade de uma nota sobre esse comportamento.
+- [E2 · run-12 · retificação de "500 com {'detail': ...}: falha própria da API. detail 'fault injection: error_500 em produto' é o injetor; 'Internal Server Error' é exceção não tratada."] Corrigir a estrutura da resposta da API para ser consistente, evitando envelopes ou campos simples aninhados, para padronizar o desenpacotamento dos dados. — Motivo: Este caso mostrou que a documentação não abrangia a necessidade de padronização na estrutura da resposta, o que pode levar a diagnósticos incorretos em casos futuros.
--- epoca-1/erros/localizador_quebrado.md
+++ epoca-2/erros/localizador_quebrado.md
@@ -14,6 +14,8 @@
 palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout, elemento, ambiguidade]
 causas_relacionadas: [estado_da_tela_divergente, recurso_inexistente]
 # ! Alteração por modelo qwen2.5:7b (E1, caso efe-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso efe-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso efe-12) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado.
@@ -27,3 +29,5 @@
 
 ## Notas do modelo
 - [E1 · efe-12 · nota] Adicionado que o localizador pode ser ambíguo, encontrando mais de um elemento com o mesmo seletor. — Motivo: Este caso mostrou que o diagnóstico precisa considerar a ambiguidade no seletor, o que não estava claro na documentação original.
+- [E2 · efe-12 · nota] Adicionar que o seletor pode ser ambíguo, encontrando mais de um elemento com o mesmo seletor. — Motivo: Este caso mostrou que a documentação não abrangia a possibilidade de um seletor ser ambíguo, encontrando mais de um elemento, o que pode causar erros na integração.
+- [E2 · efe-12 · retificação de "o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado."] Corrigir para "o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado. A lista da API não tem ORDER BY (produtos.py:38)." — Motivo: Este caso mostrou que a documentação não mencionava explicitamente que a falta de ORDER BY na API pode causar ambiguidade nos seletores, o que pode levar a erros na integração.
--- epoca-1/erros/resposta_truncada.md
+++ epoca-2/erros/resposta_truncada.md
@@ -14,6 +14,7 @@
 causas_relacionadas: [corpo_nao_e_json, corpo_vazio, tempo_de_resposta_excedido]
 # ! Alteração por modelo qwen2.5:7b (E1, caso lex-5) - Revisar: retificação acrescentada.
 # ! Alteração por modelo qwen2.5:7b (E1, caso lex-14) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso lex-14) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 O corpo começa como JSON válido e termina no meio de um valor ou chave — faltam bytes; o parse falha com "Unexpected end of JSON input".
@@ -28,3 +29,4 @@
 ## Notas do modelo
 - [E1 · lex-5 · retificação de "Fora dele: limite num proxy, conexão encerrada durante o envio."] Corrigir a descrição para incluir que o truncamento pode ser causado por limites de proxy ou interrupção de conexão. — Motivo: Esclarecer que limites de proxy ou interrupção de conexão podem causar truncamento, ajudando a diagnosticar casos futuros.
 - [E1 · lex-14 · nota] Adicione um exemplo de como verificar o Content-Length na documentação para evitar esse problema. — Motivo: Este caso mostrou que a verificação do Content-Length é crucial para detectar respostas truncadas, e a documentação não aborda isso explicitamente.
+- [E2 · lex-14 · retificação de "Fora dele: limite num proxy, conexão encerrada durante o envio."] Corrigir a descrição para incluir que o truncamento pode ser causado por limites de proxy ou interrupção de conexão. Adicione um exemplo de como verificar o Content-Length na documentação para evitar esse problema. — Motivo: Este caso mostrou que a documentação não abrangia todas as possíveis causas de truncamento da resposta, especificamente relacionadas a limites de proxy ou interrupção de conexão.
--- epoca-1/negocio/entidade-produto.md
+++ epoca-2/negocio/entidade-produto.md
@@ -11,11 +11,12 @@
 arquivos: [Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/banco/seed.sql]
 endpoints: [GET /api/produtos, GET /api/produtos/{id}]
 tabelas: [tbprodutos, tbtipos]
-sintomas: [nome da categoria no titulo do cartao, preco com grandeza estranha, nulo_inesperado, escala_ou_unidade_errada, preco cru, separador decimal como virgula]
+sintomas: [nome da categoria no titulo do cartao, preco com grandeza estranha, nulo_inesperado, escala_ou_unidade_errada, preco cru, separador decimal como virgula, incorreto, tipo errado]
 palavras_chave: [produto, categoria, tipo, preco, destaque, imagem, resumo, cardapio, picanha, convercao, valor, formatacao, decimal, separador]
 causas_relacionadas: [chave_de_juncao_errada, escala_ou_unidade_errada, tipo_divergente]
 # ! Alteração por modelo qwen2.5:7b (E1, caso sin-1) - Revisar: retificação acrescentada.
 # ! Alteração por modelo qwen2.5:7b (E1, caso semt-13) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E2, caso tra-3) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90.
@@ -30,3 +31,4 @@
 ## Notas do modelo
 - [E1 · sin-1 · retificação de "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano."] Corrigir a conversão do preço e destaque no _to_dict de produtos.py. — Motivo: O caso mostrou que a conversão incorreta de tipos pode levar a sintomas como 'undefined' e '89.9', indicando uma necessidade de revisão na conversão de tipos.
 - [E1 · semt-13 · nota] Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. — Motivo: O caso demonstra a importância de uma formatação correta do preço, independentemente da conversão do backend.
+- [E2 · tra-3 · retificação de "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano."] Corrigir a conversão do preço e destaque no _to_dict de produtos.py, garantindo que o preço seja convertido corretamente para Decimal. — Motivo: O caso mostrou que a conversão incorreta do tipo de dado no backend afeta a apresentação do produto no frontend, evidenciando a necessidade de manter a consistência dos tipos de dados.
--- epoca-1/aprendidos/rendezvous_hasta.md
+++ epoca-2/aprendidos/rendezvous_hasta.md
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
```
