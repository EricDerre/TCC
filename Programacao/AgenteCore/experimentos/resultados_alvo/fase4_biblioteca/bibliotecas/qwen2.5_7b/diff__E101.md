<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-100 -> epoca-101), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-100 -> epoca-101

| Métrica | Valor |
|---|---|
| Arquivos novos | 6 |
| Arquivos removidos | 0 |
| Arquivos tocados | 9 |
| Linhas acrescentadas | 156 |
| Linhas removidas | 11 |
| Caracteres antes | 59838 |
| Caracteres depois | 70597 |
| Caracteres acrescentados | 10759 |
| Tokens estimados acrescentados | 4138 |

```diff
--- epoca-100/aprendidos/interface-frontend.md
+++ epoca-101/aprendidos/interface-frontend.md
@@ -9,6 +9,10 @@
 status: ativo
 palavras_chave: [atualizacao, dom, innerhtml, redirect]
 causas_relacionadas: [estado_da_tela_divergente, tipo_divergente]
+# ! Alteração por modelo qwen2.5:7b (E101, caso efe-10) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Adicionar a interface frontend como uma entidade, destacando a importância de atualizações corretas do DOM e a dependência de redirects.
+
+## Notas do modelo
+- [E101 · efe-10 · nota] Adicionar nota sobre a importância de atualizações corretas do DOM e a dependência de redirects na interface frontend. — Motivo: Este caso mostrou que a interface não atualiza corretamente o DOM mesmo com a API retornando dados atualizados, evidenciando a necessidade de melhor documentação sobre atualizações do DOM e redirects.
--- epoca-100/contratos/contrato-pedido.md
+++ epoca-101/contratos/contrato-pedido.md
@@ -11,9 +11,10 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaFront/cliente/index.php]
 endpoints: [GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
 tabelas: [tbpedido_reserva, tbusuarios]
-sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado]
-palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar]
+sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado, duas reservas iguais apos um unico post, registros com id consecutivo]
+palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar, post duplo, registros duplicados]
 causas_relacionadas: [formato_de_data_divergente, valor_fora_do_dominio, recurso_inexistente, campo_ausente]
+# ! Alteração por modelo qwen2.5:7b (E101, caso run-5) - Revisar: nota acrescentada.
 ---
 ## Resumo
 GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf.
@@ -24,3 +25,6 @@
 
 ## Causa
 cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
+
+## Notas do modelo
+- [E101 · run-5 · nota] Adicionar nota sobre a possibilidade de POST /api/pedidos inserir registros duplicados sem idempotência, causando registros com id consecutivo e duas respostas 201 para um único POST. — Motivo: Este caso mostrou que a falta de mecanismo de idempotência no POST /api/pedidos pode resultar em registros duplicados, algo não coberto nos verbetes existentes.
--- epoca-100/erros/colecao_no_lugar_de_objeto.md
+++ epoca-101/erros/colecao_no_lugar_de_objeto.md
@@ -12,9 +12,10 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_api.php]
 endpoints: [GET /api/produtos, GET /api/produtos/{id}]
 sintomas: [detalhe sem preencher campos, colchetes ao redor do valor, nenhum produto retornado]
-palavras_chave: [lista, array, colecao, objeto, unico, recurso, colchetes, detalhe, modal]
+palavras_chave: [lista, array, colecao, objeto, unico, recurso, colchetes, detalhe, modal, formato_de_resposta, estrutura_json]
 causas_relacionadas: [estrutura_aninhada_divergente, campo_ausente]
 # ! Alteração por modelo qwen2.5:7b (E1, caso sin-15) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E101, caso sin-15) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (["Carnes"]).
@@ -28,3 +29,4 @@
 
 ## Notas do modelo
 - [E1 · sin-15 · retificação de "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes'])."] Corrigir que o campo "tipo" deve ser tratado como uma string, não uma lista. — Motivo: O sintoma mostrou que o campo "tipo" foi tratado como uma lista, quando na verdade é uma string.
+- [E101 · sin-15 · nota] Adicionar nota sobre a necessidade de tratar a categoria como uma string, não uma lista, no front-end. — Motivo: Este caso mostrou que a categoria deve ser tratada como uma string, não uma lista, corrigindo a lacuna na documentação.
--- epoca-100/erros/contagem_inconsistente.md
+++ epoca-101/erros/contagem_inconsistente.md
@@ -12,9 +12,10 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_destaque.php]
 endpoints: [GET /api/produtos]
 tabelas: [tbprodutos]
-sintomas: [total diferente dos itens, pagina vazia com total positivo, quatro destaques mas cinco cartoes]
-palavras_chave: [contagem, total, itens, pagina, paginacao, quantidade, destaques, inconsistente, zero]
+sintomas: [total diferente dos itens, pagina vazia com total positivo, quatro destaques mas cinco cartoes, menos itens na interface, lista crua sem total]
+palavras_chave: [contagem, total, itens, pagina, paginacao, quantidade, destaques, inconsistente, zero, lista]
 causas_relacionadas: [estrutura_aninhada_divergente, dado_desatualizado, estado_da_tela_divergente]
+# ! Alteração por modelo qwen2.5:7b (E101, caso tra-14) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Dois números que deveriam bater não batem: total 14 e lista com 1; total 0 com itens; página 2 vazia com total 14; contador de destaques diferente dos cartões.
@@ -25,3 +26,6 @@
 
 ## Causa
 GET /api/produtos devolve a lista crua, sem total nem paginação (produtos.py:34-43); o seed tem 14 produtos, 5 em destaque. Envelope com total indica outra versão.
+
+## Notas do modelo
+- [E101 · tra-14 · nota] Adicionar nota sobre a necessidade de incluir o total na resposta da API /api/produtos, para evitar contagens inconsistentes. — Motivo: Este caso mostrou que a falta de total na resposta da API pode levar a contagens inconsistentes na interface, evidenciando a necessidade de incluir este campo.
--- epoca-100/erros/erro_interno_do_servidor.md
+++ epoca-101/erros/erro_interno_do_servidor.md
@@ -12,10 +12,11 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/conn/connect.php]
 endpoints: [GET /api/produtos, POST /api/pedidos]
 sintomas: [HTTP 500, Internal Server Error, fault injection error_500, falha intermitente]
-palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora, falha_interna, injetor, excecao_nao_tratada]
+palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora, falha_interna, injetor, excecao_nao_tratada, converte, errorfault]
 causas_relacionadas: [corpo_nao_e_json, tempo_de_resposta_excedido, limite_de_requisicoes]
 # ! Alteração por modelo qwen2.5:7b (E1, caso run-6) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5:7b (E1, caso run-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E101, caso run-12) - Revisar: nota acrescentada.
 ---
 ## Resumo
 500 com {"detail": ...}: falha própria da API. detail "fault injection: error_500 em produto" é o injetor; "Internal Server Error" é exceção não tratada.
@@ -30,3 +31,4 @@
 ## Notas do modelo
 - [E1 · run-6 · nota] Adicionar que este erro pode ocorrer devido a falhas no banco de dados ou em rotas, e que a mensagem genérica pode esconder problemas específicos. — Motivo: Este caso mostrou que a mensagem de erro genérica pode esconder problemas específicos, como falhas no banco de dados, que não são explicitamente mencionados na documentação.
 - [E1 · run-12 · nota] Adicionar que este erro pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota. — Motivo: Este caso mostrou que o erro interno do servidor pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota, evidenciando a necessidade de uma nota sobre esse comportamento.
+- [E101 · run-12 · nota] Adicionar que a conversão de ErrorFault em 500 pode ser causada por problemas na rota. — Motivo: Este caso mostrou que a documentação poderia ser mais detalhada sobre a origem do erro 500, ajudando a diferenciar de outros tipos de falhas.
--- epoca-100/erros/estado_da_tela_divergente.md
+++ epoca-101/erros/estado_da_tela_divergente.md
@@ -11,9 +11,12 @@
 status: ativo
 causa_raiz: estado_da_tela_divergente
 arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/reserva_cli.php]
-sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar]
-palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML]
+sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar, lista vazia, botao que nao muda, carregando..., botao inativo]
+palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML, fetch, redirect, cancelar, cliente_cancelar.php]
 causas_relacionadas: [localizador_quebrado, dado_desatualizado, corpo_vazio]
+# ! Alteração por modelo qwen2.5:7b (E101, caso efe-4) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E101, caso efe-8) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E101, caso efe-13) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A rede está certa — status e corpo conferem — e o usuário vê outra coisa: "Carregando" parado, lista vazia, botão que não muda.
@@ -24,3 +27,8 @@
 
 ## Causa
 produtos_api.php só limpa "Carregando..." no then() do fetch e substitui o grid por innerHTML; na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).
+
+## Notas do modelo
+- [E101 · efe-4 · retificação de "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7)."] Corrigir a lógica para atualizar o estado corretamente, independentemente de ser uma coleção ou um objeto. — Motivo: Este caso mostrou que a lógica de atualização do estado da tela não está adequada, precisando ser verificada e ajustada para lidar com diferentes tipos de respostas.
+- [E101 · efe-8 · nota] Adicionar nota sobre a necessidade de atualização correta do estado da tela após a resposta da API. — Motivo: Este caso mostrou que a documentação não aborda a atualização correta do estado da tela, diferentemente do tratamento do corpo da resposta.
+- [E101 · efe-13 · nota] O cancelamento depende de um redirect, o que pode causar divergência na interface. — Motivo: Este caso mostrou que a dependência de redirect para cancelamento pode levar a divergência na interface, mesmo com a resposta correta da API.
--- epoca-100/erros/limite_de_requisicoes.md
+++ epoca-101/erros/limite_de_requisicoes.md
@@ -12,8 +12,9 @@
 arquivos: [Programacao/CobaiaAPI/app/main.py, Programacao/CobaiaFront/produtos_api.php]
 endpoints: [GET /api/produtos]
 sintomas: [HTTP 429, too many requests, rate limit, para de funcionar apos varias tentativas]
-palavras_chave: [429, limite, rate limit, too many requests, retry_after, cota, excesso, recarregar]
+palavras_chave: [429, limite, rate limit, too many requests, retry_after, cota, excesso, recarregar, status de erro, limitador de requisicoes]
 causas_relacionadas: [tempo_de_resposta_excedido, erro_interno_do_servidor]
+# ! Alteração por modelo qwen2.5:7b (E101, caso run-3) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Status 429: o servidor ou um intermediário recusou por excesso de requisições num intervalo. Resposta rápida e com corpo — não é lentidão nem erro interno.
@@ -24,3 +25,6 @@
 
 ## Causa
 A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado.
+
+## Notas do modelo
+- [E101 · run-3 · retificação de "A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado."] Corrigir que o 429 pode ser emitido pelo próprio servidor ou intermediários, não necessariamente pelo CobaiaAPI. — Motivo: A retificação corrigirá a percepção de que o 429 sempre vem de um servidor diferente, permitindo que o próximo diagnóstico considere essa possibilidade.
--- epoca-100/erros/localizador_quebrado.md
+++ epoca-101/erros/localizador_quebrado.md
@@ -11,9 +11,10 @@
 causa_raiz: localizador_quebrado
 arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_geral.php]
 sintomas: [elemento nao encontrado, tempo esgotado procurando elemento, seletor casou dois elementos, texto do botao diferente]
-palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout, elemento, ambiguidade]
+palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout, elemento, ambiguidade, order by, consulta]
 causas_relacionadas: [estado_da_tela_divergente, recurso_inexistente]
 # ! Alteração por modelo qwen2.5:7b (E1, caso efe-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E101, caso efe-11) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado.
@@ -27,3 +28,4 @@
 
 ## Notas do modelo
 - [E1 · efe-12 · nota] Adicionado que o localizador pode ser ambíguo, encontrando mais de um elemento com o mesmo seletor. — Motivo: Este caso mostrou que o diagnóstico precisa considerar a ambiguidade no seletor, o que não estava claro na documentação original.
+- [E101 · efe-11 · nota] Adicionar que a falta de ORDER BY na consulta pode causar ordem aleatória indeterminada dos produtos. — Motivo: Este caso mostrou que a ordem dos produtos pode variar, indicando a necessidade de uma consulta ordenada.
--- epoca-100/erros/tipo_divergente.md
+++ epoca-101/erros/tipo_divergente.md
@@ -12,8 +12,11 @@
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py]
 endpoints: [GET /api/produtos, GET /api/pedidos]
 sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada]
-palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal]
+palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal, convercao, json]
 causas_relacionadas: [valor_fora_do_dominio, formato_de_data_divergente, escala_ou_unidade_errada]
+# ! Alteração por modelo qwen2.5:7b (E101, caso semt-6) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E101, caso semt-7) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E101, caso semt-10) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Chave certa com o tipo JSON errado: número entre aspas ("89.90"), booleano como texto ("Sim") ou número (1), inteiro como texto ("4").
@@ -24,3 +27,8 @@
 
 ## Causa
 O modo type_drift aplica str() ao campo-alvo (fault_injection.py:76). A API converte DECIMAL em número e 'Sim'/'Não' em booleano (_to_dict).
+
+## Notas do modelo
+- [E101 · semt-6 · nota] Adicionar nota sobre a necessidade de conversão correta do tipo id em inteiro no front-end, considerando que o backend retorna como string. — Motivo: Este caso mostrou que a conversão incorreta do tipo id pode causar confusões na interface, e a documentação não explicitava essa necessidade.
+- [E101 · semt-7 · retificação de "Chave certa com o tipo JSON errado: número entre aspas ('89.90'), booleano como texto ('Sim') ou número (1), inteiro como texto ('4'). Sinais: texto numérico com ponto ainda formata; a falha aparece ao ordenar ou somar; '89,90' com vírgula não converte; destaque fora de true/false sai literal."] Adicionar exemplo de campo "pessoas" como número em vez de string, causando inconsistência na contagem total de lugares reservados. — Motivo: O caso mostrou que a contagem total de lugares reservados está incorreta, indicando que o tipo do campo "pessoas" está divergindo do esperado, necessitando de um exemplo explícito na documentação.
+- [E101 · semt-10 · nota] Adicionar nota sobre a converção de tipos entre a API e a interface web, especificamente sobre o campo destaque que vem como texto em vez de booleano. — Motivo: Este caso mostra que a converção de tipos entre a API e a interface web precisa ser claramente documentada, pois o usuário pode interpretar incorretamente os dados.
--- epoca-100/aprendidos/atualizacao-da-tela.md
+++ epoca-101/aprendidos/atualizacao-da-tela.md
@@ -0,0 +1,21 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 101 a partir do caso efe-8 (Fase 3).
+# ! Motivo: Este caso demonstrou a necessidade de documentar a atualização correta do estado da tela, diferentemente do tratamento atual do corpo da resposta.
+id: atualizacao-da-tela
+titulo: Atualização da Tela após a API
+sistema: Ambos
+entidade_principal: Interface
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/cliente_cancelar.php]
+sintomas: [carregando..., lista vazia, botao inativo]
+palavras_chave: [fetch, innerhtml, redirect, promise]
+causas_relacionadas: [estado_da_tela_divergente]
+---
+## Resumo
+Adicionar verbete sobre a necessidade de atualização correta do estado da tela após a resposta da API, utilizando promises ou async/await.
+
+## Sinais
+- carregando...
+- lista vazia
+- botao inativo
--- epoca-100/aprendidos/campo_preco_ausente.md
+++ epoca-101/aprendidos/campo_preco_ausente.md
@@ -0,0 +1,19 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 101 a partir do caso sin-1 (Fase 3).
+# ! Motivo: Este novo verbete fornece um exemplo específico de campo ausente relacionado ao preço, ajudando a identificar rapidamente casos semelhantes no futuro.
+id: campo_preco_ausente
+titulo: Campo preço ausente
+sistema: CobaiaFront
+entidade_principal: Produto
+tipo: aprendido
+status: ativo
+sintomas: [botao com valor undefined, precos ausentes na interface]
+palavras_chave: [campo ausente, preco, interface web]
+causas_relacionadas: [campo_ausente]
+---
+## Resumo
+Um campo preço ausente na resposta da API resulta em botões sem informações relevantes na interface web.
+
+## Sinais
+- botao com valor undefined
+- precos ausentes na interface
--- epoca-100/aprendidos/formato_preco.md
+++ epoca-101/aprendidos/formato_preco.md
@@ -0,0 +1,14 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 101 a partir do caso tra-6 (Fase 3).
+# ! Motivo: Este verbete aborda a necessidade de formatação correta do preço no front-end, conforme mencionado na documentação, ajudando a diagnosticar casos futuros com formatos de preço incorretos.
+id: formato_preco
+titulo: Formato de preço errado
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: aprendido
+status: ativo
+palavras_chave: [formatacao, monetario, localidade]
+causas_relacionadas: [escala_ou_unidade_errada]
+---
+## Resumo
+Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro.
--- epoca-100/aprendidos/novo_verbete.md
+++ epoca-101/aprendidos/novo_verbete.md
@@ -0,0 +1,20 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 101 a partir do caso tra-3 (Fase 3).
+# ! Motivo: O caso mostrou que a junção entre tabelas estava incorreta, levando a categorias incorretas nos produtos, e a documentação não abordava explicitamente a necessidade de corrigir essa junção.
+id: novo_verbete
+titulo: Junção de tabelas incorreta
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaAPI/app/models.py]
+sintomas: [tipo_divergente, chave_de_juncao_errada]
+palavras_chave: [juncao, juncao incorreta, juncao de tabelas]
+causas_relacionadas: [chave_de_juncao_errada]
+---
+## Resumo
+Corrigir a junção entre tbprodutos e tbtipos, garantindo que id_tipo_produto esteja corretamente ligado a tbtipos.id_tipo.
+
+## Sinais
+- tipo_divergente
+- chave_de_juncao_errada
--- epoca-100/aprendidos/pessoas_incorretas.md
+++ epoca-101/aprendidos/pessoas_incorretas.md
@@ -0,0 +1,19 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 101 a partir do caso tra-5 (Fase 3).
+# ! Motivo: O caso demonstrou a necessidade de validação adicional para garantir que a quantidade de pessoas seja correta.
+id: pessoas_incorretas
+titulo: Inconsistência na quantidade de pessoas reservadas
+sistema: CobaiaAPI
+entidade_principal: Pedido
+tipo: aprendido
+status: ativo
+sintomas: [pessoas menor que 1, reserva nem ativa nem cancelada na tela]
+palavras_chave: [conversao, arredondamento, quantidade]
+causas_relacionadas: [escala_ou_unidade_errada, valor_fora_do_dominio]
+---
+## Resumo
+Adicionar validação no número de pessoas no pedido para evitar valores incorretos.
+
+## Sinais
+- pessoas menor que 1
+- reserva nem ativa nem cancelada na tela
--- epoca-100/aprendidos/validacao-na-api.md
+++ epoca-101/aprendidos/validacao-na-api.md
@@ -0,0 +1,14 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 101 a partir do caso semt-15 (Fase 3).
+# ! Motivo: O caso mostrou a necessidade de validar os campos na API para corresponder às restrições do formulário, evitando reservas inválidas.
+id: validacao-na-api
+titulo: Validação na API
+sistema: CobaiaAPI
+entidade_principal: Pedido
+tipo: aprendido
+status: ativo
+palavras_chave: [validacao, restricoes, formulario]
+causas_relacionadas: [valor_fora_do_dominio]
+---
+## Resumo
+Adicionar validação no status do pedido na API para evitar valores fora do domínio permitido pelo formulário.
```
