<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-2 -> epoca-3), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-2 -> epoca-3

| Métrica | Valor |
|---|---|
| Arquivos novos | 2 |
| Arquivos removidos | 0 |
| Arquivos tocados | 5 |
| Linhas acrescentadas | 64 |
| Linhas removidas | 6 |
| Caracteres antes | 76836 |
| Caracteres depois | 81481 |
| Caracteres acrescentados | 4645 |
| Tokens estimados acrescentados | 1787 |

```diff
--- epoca-2/erros/campo_ausente.md
+++ epoca-3/erros/campo_ausente.md
@@ -11,10 +11,12 @@
 causa_raiz: campo_ausente
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
 endpoints: [GET /api/produtos, GET /api/pedidos]
-sintomas: [cartao sem titulo, sem nome, undefined na tela, botao que nao faz nada, nulo_inesperado]
-palavras_chave: [ausente, falta, faltando, sem o campo, undefined, field_missing, chave]
+sintomas: [cartao sem titulo, sem nome, undefined na tela, botao que nao faz nada, nulo_inesperado, undefined no botao de preco]
+palavras_chave: [ausente, falta, faltando, sem o campo, undefined, field_missing, chave, front-end, json, campo ausente, formatacao]
 causas_relacionadas: [campo_renomeado, nulo_inesperado, estrutura_aninhada_divergente]
 # ! Alteração por modelo qwen2.5:7b (E1, caso sin-1) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E3, caso sin-1) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E3, caso sin-6) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Uma chave do contrato não vem no objeto — nem com nulo. No JavaScript a leitura vira undefined.
@@ -28,3 +30,5 @@
 
 ## Notas do modelo
 - [E1 · sin-1 · nota] Adicionar nota sobre a remoção de campos no fault_injection.py. — Motivo: O caso demonstrou que a remoção de campos pode causar sintomas como 'undefined', indicando a necessidade de documentar melhor esse cenário.
+- [E3 · sin-1 · nota] Adicionar nota sobre a remoção de campos no fault_injection.py e a necessidade de formatação correta do preço no front-end. — Motivo: O sintoma mostrou que o campo preco estava ausente, indicando a necessidade de notas adicionais na documentação.
+- [E3 · sin-6 · nota] Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. — Motivo: O sintoma mostrou que a falta do campo "nome" causou o problema, e a nota ajudaria a prevenir futuros diagnósticos semelhantes.
--- epoca-2/erros/corpo_nao_e_json.md
+++ epoca-3/erros/corpo_nao_e_json.md
@@ -17,6 +17,7 @@
 # ! Alteração por modelo qwen2.5:7b (E1, caso lex-9) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5:7b (E2, caso lex-2) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5:7b (E2, caso lex-2) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E3, caso lex-6) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.
@@ -33,3 +34,4 @@
 - [E1 · lex-9 · nota] Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho. — Motivo: Este caso mostrou que XML também pode causar parse falho, mas a documentação não destaca isso.
 - [E2 · lex-2 · nota] Adicionar que sintomas podem incluir avisos antes do JSON e parse falhos no primeiro caractere. — Motivo: Este caso mostrou que avisos HTML podem preceder o JSON, causando parse falhos, e que sintomas específicos como esses devem ser documentados.
 - [E2 · lex-2 · nota] Adicionar exemplos específicos de sintomas, como "Página de erro HTML em vez de JSON" e "aviso antes do JSON", para melhor identificação de casos onde o corpo da resposta não é JSON. — Motivo: Este caso mostrou que precisamos de exemplos mais detalhados de sintomas para diagnóstico preciso, como avisos antes do JSON e parse falhos no primeiro caractere.
+- [E3 · lex-6 · nota] Adicionar que parse falhos podem ocorrer com qualquer tipo de corpo não JSON, não apenas HTML. — Motivo: Este caso mostrou que o parse falho pode ocorrer com respostas HTML, não apenas JSON, precisando ser explicitado na documentação.
--- epoca-2/erros/limite_de_requisicoes.md
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
--- epoca-2/erros/tempo_de_resposta_excedido.md
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
--- epoca-2/erros/tipo_divergente.md
+++ epoca-3/erros/tipo_divergente.md
@@ -11,10 +11,11 @@
 causa_raiz: tipo_divergente
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py]
 endpoints: [GET /api/produtos, GET /api/pedidos]
-sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada, destaque booleano sai literal]
-palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal, convercao]
+sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada, destaque booleano sai literal, categoria errada]
+palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal, convercao, destaque]
 causas_relacionadas: [valor_fora_do_dominio, formato_de_data_divergente, escala_ou_unidade_errada]
 # ! Alteração por modelo qwen2.5:7b (E1, caso semt-13) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E3, caso tra-3) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Chave certa com o tipo JSON errado: número entre aspas ("89.90"), booleano como texto ("Sim") ou número (1), inteiro como texto ("4").
@@ -28,3 +29,4 @@
 
 ## Notas do modelo
 - [E1 · semt-13 · retificação de "destaque fora de true/false sai literal."] Corrigir que destaque booleano saia literal, garantindo que seja convertido corretamente para True ou False. — Motivo: O caso mostrou que a conversão incorreta de booleano afeta a apresentação do preço, indicando a necessidade de corrigir essa conversão.
+- [E3 · tra-3 · nota] Notar que a junção errada pode afetar campos derivados como tipo, garantindo a precisão na apresentação dos produtos. — Motivo: O sintoma mostrou que a categoria estava incorreta, indicando que a converção incorreta de dados pode afetar a apresentação correta dos produtos.
--- epoca-2/aprendidos/arredondamento_incorreto.md
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
--- epoca-2/aprendidos/soma_inconsistente.md
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
