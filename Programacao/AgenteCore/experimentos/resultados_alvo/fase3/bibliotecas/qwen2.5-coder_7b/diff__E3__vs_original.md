<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-0 -> epoca-3), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-0 -> epoca-3

| Métrica | Valor |
|---|---|
| Arquivos novos | 0 |
| Arquivos removidos | 0 |
| Arquivos tocados | 18 |
| Linhas acrescentadas | 148 |
| Linhas removidas | 34 |
| Caracteres antes | 47502 |
| Caracteres depois | 67040 |
| Caracteres acrescentados | 19538 |
| Tokens estimados acrescentados | 7515 |

```diff
--- epoca-0/contratos/contrato-pedido.md
+++ epoca-3/contratos/contrato-pedido.md
@@ -11,9 +11,13 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaFront/cliente/index.php]
 endpoints: [GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
 tabelas: [tbpedido_reserva, tbusuarios]
-sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado]
-palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar]
+sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado, pessoas incorreta, data em formato errado, registro duplicado, duas reservas identicas, uma das reservas do cliente some da tela, status inesperado, reserva nem ativa nem cancelada]
+palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar, validacao, dados, entrada, idempotencia, unidade de trabalho, contrato pedido cpf ausente]
 causas_relacionadas: [formato_de_data_divergente, valor_fora_do_dominio, recurso_inexistente, campo_ausente]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-5) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso run-5) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso sin-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso semt-11) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf.
@@ -24,3 +28,9 @@
 
 ## Causa
 cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
+
+## Notas do modelo
+- [E1 · tra-5 · retificação de "pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado'"] Adicionar validação de dados no endpoint /api/pedidos para garantir que os valores de pessoas estejam no formato correto e que a data esteja no formato AAAA-MM-DD. — Motivo: A falta de validação de dados no endpoint /api/pedidos é a causa raiz do problema. A documentação não menciona a necessidade de validação dos dados de entrada, o que resultou em um erro de integração entre a interface web e a API.
+- [E1 · run-5 · retificação de "POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201;"] Adicionar verificação de idempotência para evitar inserções duplicadas. — Motivo: A falta de verificação de idempotência permite que o mesmo pedido seja inserido múltiplas vezes, causando registros duplicados. A adição de uma chave de idempotência garante que cada pedido seja inserido apenas uma vez.
+- [E1 · sin-12 · nota] Adicionar 'cpf' como campo obrigatório no contrato de pedido. — Motivo: O campo 'cpf' é crucial para identificar o cliente, e sua ausência causa inconsistência na tela do usuário.
+- [E1 · semt-11 · retificação de "status 'Em Análise'|'Cancelado'"] A API deve validar o status dos pedidos para garantir que seja 'Em Análise' ou 'Cancelado'. — Motivo: A falta de validação do status na API é a causa raiz do problema, conforme mostrado no caso atual, onde o status 'Concluido' não é reconhecido.
--- epoca-0/erros/campo_ausente.md
+++ epoca-3/erros/campo_ausente.md
@@ -11,9 +11,10 @@
 causa_raiz: campo_ausente
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
 endpoints: [GET /api/produtos, GET /api/pedidos]
-sintomas: [cartao sem titulo, sem nome, undefined na tela, botao que nao faz nada]
-palavras_chave: [ausente, falta, faltando, sem o campo, undefined, field_missing, chave]
+sintomas: [cartao sem titulo, sem nome, undefined na tela, botao que nao faz nada, cartoes sem titulo]
+palavras_chave: [ausente, falta, faltando, sem o campo, undefined, field_missing, chave, campo ausente, nome, contrato api]
 causas_relacionadas: [campo_renomeado, nulo_inesperado, estrutura_aninhada_divergente]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso sin-6) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Uma chave do contrato não vem no objeto — nem com nulo. No JavaScript a leitura vira undefined.
@@ -24,3 +25,6 @@
 
 ## Causa
 O modo field_missing remove o campo-alvo (fault_injection.py). Diferença para campo_renomeado: nenhuma chave nova aparece no lugar.
+
+## Notas do modelo
+- [E1 · sin-6 · nota] Adicionar nota em [campo_ausente] explicando que o campo "nome" pode estar ausente em respostas da API, causando cartões sem título. — Motivo: Esta nota ajuda a identificar rapidamente a causa da falha, pois o campo "nome" é essencial para o título dos cartões.
--- epoca-0/erros/campo_renomeado.md
+++ epoca-3/erros/campo_renomeado.md
@@ -11,9 +11,10 @@
 causa_raiz: campo_renomeado
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaAPI/app/schemas.py]
 endpoints: [GET /api/produtos, GET /api/pedidos]
-sintomas: [chave desconhecida no lugar da esperada, _v2, campo com outro nome]
-palavras_chave: [renomead, outro nome, _v2, descricao, situacao, imagem_url, field_renamed, chave inesperada]
+sintomas: [chave desconhecida no lugar da esperada, _v2, campo com outro nome, titulo vazio, preco e categoria corretos]
+palavras_chave: [renomead, outro nome, _v2, descricao, situacao, imagem_url, field_renamed, chave inesperada, renomeacao, campo-alvo, injeccao de falha]
 causas_relacionadas: [campo_ausente, estrutura_aninhada_divergente]
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso sin-9) - Revisar: nota acrescentada.
 ---
 ## Resumo
 O valor existe sob outra chave: falta a esperada e aparece uma desconhecida com o mesmo tipo e conteúdo (preco → preco_v2, nome → descricao, status → situacao).
@@ -24,3 +25,6 @@
 
 ## Causa
 O modo field_renamed troca o campo-alvo por <campo>_v2 (fault_injection.py). Fora dele: contrato mudou no servidor sem atualizar o cliente.
+
+## Notas do modelo
+- [E3 · sin-9 · nota] Adicionar nota explicando que o campo "nome" foi renomeado para "descricao" em versões mais recentes do sistema. — Motivo: Esta nota ajudará a explicar a renomeação do campo, permitindo que os desenvolvedores futuros entendam a mudança e evitem diagnósticos incorretos.
--- epoca-0/erros/contagem_inconsistente.md
+++ epoca-3/erros/contagem_inconsistente.md
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
--- epoca-0/erros/corpo_nao_e_json.md
+++ epoca-3/erros/corpo_nao_e_json.md
@@ -10,9 +10,13 @@
 status: ativo
 causa_raiz: corpo_nao_e_json
 arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaFront/produtos_api.php]
-sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json]
-palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type]
+sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, pagina html de erro 404, falha de parse, fatal error, memoria esgotada, resposta html, falha ao acessar de fora da rede local, resposta html em vez de json, falha em ambientes externos]
+palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, resposta json, erro 404, erro de memoria, php, conexao, resposta html, erro de integracao, ambiente externo, erro 500]
 causas_relacionadas: [resposta_truncada, corpo_vazio, erro_interno_do_servidor]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso lex-6) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E2, caso lex-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E2, caso lex-15) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso lex-15) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.
@@ -23,3 +27,9 @@
 
 ## Causa
 Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página.
+
+## Notas do modelo
+- [E1 · lex-6 · nota] Adicionar nota: A resposta deve ser um JSON válido, não uma página HTML de erro. — Motivo: A documentação atual não destaca que a resposta deve ser JSON, o que pode levar a diagnósticos incorretos quando a resposta não atende a este formato esperado.
+- [E2 · lex-12 · nota] Adicionar nota: Erros de memória em PHP podem causar respostas HTML inválidas, interrompendo a exibição de dados JSON. — Motivo: O erro de memória em PHP (Fatal error: Allowed memory size exhausted) é uma causa comum de respostas HTML inválidas, o que corresponde ao sintoma observado.
+- [E2 · lex-15 · nota] Adicionar nota explicando que a resposta deve ser JSON válido, não uma página HTML de erro. — Motivo: A nota ajudará a identificar rapidamente a causa da falha, que é a resposta HTML em vez de JSON, especialmente quando a resposta é 200 e o Content-Type indica JSON.
+- [E3 · lex-15 · nota] Adicionar nota explicando que erros de resposta HTML podem ocorrer em ambientes externos devido a falhas no servidor ou gateway. — Motivo: Esta nota ajuda a entender que a falha não é exclusiva do ambiente local, mas também pode afetar ambientes externos, explicando a inconsistência observada.
--- epoca-0/erros/corpo_vazio.md
+++ epoca-3/erros/corpo_vazio.md
@@ -10,9 +10,11 @@
 status: ativo
 causa_raiz: corpo_vazio
 arquivos: [Programacao/CobaiaFront/produtos_api.php]
-sintomas: [carregando indefinidamente, tela em branco sem erro, fim inesperado da entrada em corpo vazio]
-palavras_chave: [vazio, sem corpo, branco, 204, espacos, nenhum byte, carregando]
+sintomas: [carregando indefinidamente, tela em branco sem erro, fim inesperado da entrada em corpo vazio, tabela de reservas vazia, erro de carregamento, pagina de carregamento indefinido, dados nao retornados]
+palavras_chave: [vazio, sem corpo, branco, 204, espacos, nenhum byte, carregando, resposta vazia, erro de integracao, erro interno, rota errada]
 causas_relacionadas: [resposta_truncada, corpo_nao_e_json, estado_da_tela_divergente]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso lex-13) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso lex-3) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Status de sucesso e nenhum byte útil no corpo (vazio, só espaços, ou 204). Diferente de "[]", lista vazia, que é JSON válido.
@@ -23,3 +25,7 @@
 
 ## Causa
 Nenhuma rota da CobaiaAPI devolve 204 nem corpo vazio; se chega vazio, foi cortado antes de sair (servidor, proxy) ou a rota errada respondeu.
+
+## Notas do modelo
+- [E1 · lex-13 · nota] Adicionar nota: "Ocorre quando a API retorna uma resposta vazia, que pode ser devido a um erro interno ou a uma rota errada." — Motivo: Esta nota ajuda a identificar a causa raiz do problema, que é um corpo vazio, e fornece contexto sobre onde pode ocorrer.
+- [E3 · lex-3 · nota] Adicionar nota explicando que o corpo vazio pode ser causado por erros internos ou rotas incorretas. — Motivo: Esta nota ajuda a identificar rapidamente a causa do problema, facilitando o diagnóstico em casos sem corpo JSON válido.
--- epoca-0/erros/erro_interno_do_servidor.md
+++ epoca-3/erros/erro_interno_do_servidor.md
@@ -11,9 +11,12 @@
 causa_raiz: erro_interno_do_servidor
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/conn/connect.php]
 endpoints: [GET /api/produtos, POST /api/pedidos]
-sintomas: [HTTP 500, Internal Server Error, fault injection error_500, falha intermitente]
-palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora]
+sintomas: [HTTP 500, Internal Server Error, fault injection error_500, falha intermitente, intermitente sem padrao, em toda requisicao, banco inacessivel, erro interno do servidor, banco fora]
+palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora, injetor, banco inacessivel, defeito na rota, excecao nao tratada, falhas de banco de dados, injetores de erros]
 causas_relacionadas: [corpo_nao_e_json, tempo_de_resposta_excedido, limite_de_requisicoes]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso run-6) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso run-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso run-6) - Revisar: nota acrescentada.
 ---
 ## Resumo
 500 com {"detail": ...}: falha própria da API. detail "fault injection: error_500 em produto" é o injetor; "Internal Server Error" é exceção não tratada.
@@ -24,3 +27,8 @@
 
 ## Causa
 Rotas convertem ErrorFault em 500 (produtos.py:42). No site PHP, banco fora NÃO dá 500: imprime "Atenção ERRO" em HTML (connect.php:16).
+
+## Notas do modelo
+- [E1 · run-6 · nota] Adicionar nota explicando que o erro interno do servidor pode ocorrer devido a falhas no banco de dados ou defeitos na rota, além de ser intermitente. — Motivo: Esta nota ajudará a explicar a causa raiz do erro interno do servidor em rotas de produtos, que é um problema de infraestrutura relacionado ao banco de dados ou rotas.
+- [E1 · run-12 · nota] Adicionar nota explicando que o erro interno do servidor pode ser causado por falhas de banco de dados ou injetores de erros. — Motivo: Esta nota ajudará a identificar rapidamente falhas de banco de dados ou injetores de erros como a causa raiz do problema.
+- [E3 · run-6 · nota] Adicionar nota explicando que o erro interno do servidor pode ocorrer devido a falhas no banco de dados ou defeitos na rota, além de ser intermitente. Adicionar nota explicando que o erro interno do servidor pode ser causado por falhas de banco de dados ou injetores de erros. — Motivo: Esta nota ajudará a explicar as possíveis causas do erro interno do servidor, incluindo falhas no banco de dados e injetores de erros, o que pode ajudar a diagnosticar o problema corretamente.
--- epoca-0/erros/escala_ou_unidade_errada.md
+++ epoca-3/erros/escala_ou_unidade_errada.md
@@ -12,9 +12,13 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/models.py]
 endpoints: [GET /api/produtos, GET /api/pedidos]
 tabelas: [tbprodutos, tbpedido_reserva]
-sintomas: [precos cem vezes maiores, precos cem vezes menores, preco arredondado, data um dia antes, dobro de pessoas]
-palavras_chave: [escala, unidade, centavos, reais, fator, cem, arredond, fuso, dia, dobro, multiplic, divid]
+sintomas: [precos cem vezes maiores, precos cem vezes menores, preco arredondado, data um dia antes, dobro de pessoas, data deslocada um dia, precos arredondados, precisao financeira comprometida, precisao na comanda]
+palavras_chave: [escala, unidade, centavos, reais, fator, cem, arredond, fuso, dia, dobro, multiplic, divid, conversao, decimal, fuso horario, conversao de data, conversao de unidade, valor_produto, float]
 causas_relacionadas: [tipo_divergente, formato_de_data_divergente, chave_de_juncao_errada]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-6) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-9) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-12) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E2, caso tra-12) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Tipo e formato certos, mas o número está noutra escala ou unidade: centavos por reais (8990), fração (0.899), arredondado (90), data deslocada um dia, quantidade dobrada.
@@ -25,3 +29,9 @@
 
 ## Causa
 A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela.
+
+## Notas do modelo
+- [E1 · tra-6 · retificação de "float(valor_produto) direto do DECIMAL"] A conversão de valor_produto deve considerar a escala correta, convertendo DECIMAL(9,2) para float sem alteração. — Motivo: A evidência deste caso mostrou que a conversão direta de DECIMAL para float estava causando a escala errada, o que foi confirmado pela documentação do verbete [escala_ou_unidade_errada].
+- [E1 · tra-9 · retificação de "DATE em isoformat sem fuso"] A API deve converter a data para o fuso horário do cliente antes de retornar. — Motivo: A falta de conversão de fuso horário é a causa raiz do problema, conforme mostrado no caso atual.
+- [E1 · tra-12 · retificação de "float(valor_produto)"] A API deve converter DECIMAL para número considerando a escala correta (100 para centavos). — Motivo: A evidência deste caso mostrou que a API estava simplesmente convertendo DECIMAL para número sem considerar a escala correta, resultando em preços arredondados.
+- [E2 · tra-12 · retificação de "float(valor_produto)"] A conversão de DECIMAL para float deve considerar a escala correta, convertendo DECIMAL(9,2) para float sem alteração. — Motivo: Esta correção resolve o problema de preços arredondados, pois garante que o valor seja convertido corretamente sem perda de precisão. A evidência deste caso mostrou que a conversão direta estava causando o problema.
--- epoca-0/erros/estado_da_tela_divergente.md
+++ epoca-3/erros/estado_da_tela_divergente.md
@@ -11,9 +11,12 @@
 status: ativo
 causa_raiz: estado_da_tela_divergente
 arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/reserva_cli.php]
-sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar]
-palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML]
+sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar, lista vazia, botao inativo, botao de cancelar continua habilitado, reserva segue como ativa, tela nao reflete dados atualizados, estado inconsistente]
+palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML, atualizacao de estado, carregamento, interface, dependencia de redirect, carregamento de dados, interface do usuario]
 causas_relacionadas: [localizador_quebrado, dado_desatualizado, corpo_vazio]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-4) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-15) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso efe-13) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A rede está certa — status e corpo conferem — e o usuário vê outra coisa: "Carregando" parado, lista vazia, botão que não muda.
@@ -24,3 +27,8 @@
 
 ## Causa
 produtos_api.php só limpa "Carregando..." no then() do fetch e substitui o grid por innerHTML; na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).
+
+## Notas do modelo
+- [E1 · efe-4 · nota] Adicionar nota explicando que a atualização do estado da tela deve ocorrer após o carregamento dos dados. — Motivo: Esta nota ajudará a entender que a interface não está atualizando corretamente após o carregamento dos dados, o que é o problema observado neste caso.
+- [E1 · efe-15 · retificação de "cancelar depende do redirect (cliente_cancelar.php:7)"] Adicionar verificação de status na interface para refletir mudanças sem dependência de redirect. — Motivo: Este trecho demonstra que a interface depende de um redirect para atualizar o estado, o que pode não refletir corretamente as mudanças na API. A adição de uma verificação de status na interface resolveria este problema.
+- [E3 · efe-13 · nota] Adicionar nota explicando que a atualização do estado da tela deve ocorrer após o carregamento dos dados, evitando que a resposta mais antiga sobrescreva a mais nova. — Motivo: Esta nota ajuda a entender que a atualização da interface deve ocorrer após o carregamento dos dados, explicando a causa da divergência entre o estado da tela e a resposta da API.
--- epoca-0/erros/formato_de_data_divergente.md
+++ epoca-3/erros/formato_de_data_divergente.md
@@ -12,9 +12,10 @@
 arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py]
 endpoints: [GET /api/pedidos, POST /api/pedidos]
 tabelas: [tbpedido_reserva]
-sintomas: [Invalid Date, data como numero, data em formato brasileiro]
-palavras_chave: [data, formato, iso, AAAA-MM-DD, dd/mm/aaaa, timestamp, epoch, Invalid Date, data_pedido]
+sintomas: [Invalid Date, data como numero, data em formato brasileiro, formato_data_br, timestamp]
+palavras_chave: [data, formato, iso, AAAA-MM-DD, dd/mm/aaaa, timestamp, epoch, Invalid Date, data_pedido, data_iso, formato_data, api_resposta]
 causas_relacionadas: [escala_ou_unidade_errada, tipo_divergente]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso semt-4) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 data_pedido deve ser texto AAAA-MM-DD. Chega noutro formato (10/09/2026), como segundos (1789084800) ou com hora e fuso — e o cliente não interpreta.
@@ -25,3 +26,6 @@
 
 ## Causa
 A API devolve data_pedido.isoformat() (pedidos.py:23), sempre AAAA-MM-DD. Em escala_ou_unidade_errada a data é legível mas deslocada; aqui é ilegível.
+
+## Notas do modelo
+- [E1 · semt-4 · retificação de "data_pedido.isoformat()"] A API deve retornar a data no formato ISO (AAAA-MM-DD) conforme especificado no contrato. — Motivo: A documentação já menciona que a data deve ser no formato AAAA-MM-DD, mas o código da API está retornando a data em um formato não aceito pelo cliente.
--- epoca-0/erros/limite_de_requisicoes.md
+++ epoca-3/erros/limite_de_requisicoes.md
@@ -11,9 +11,10 @@
 causa_raiz: limite_de_requisicoes
 arquivos: [Programacao/CobaiaAPI/app/main.py, Programacao/CobaiaFront/produtos_api.php]
 endpoints: [GET /api/produtos]
-sintomas: [HTTP 429, too many requests, rate limit, para de funcionar apos varias tentativas]
-palavras_chave: [429, limite, rate limit, too many requests, retry_after, cota, excesso, recarregar]
+sintomas: [HTTP 429, too many requests, rate limit, para de funcionar apos varias tentativas, erro 429, recarregar muitas vezes]
+palavras_chave: [429, limite, rate limit, too many requests, retry_after, cota, excesso, recarregar, limitador, proxy, gateway]
 causas_relacionadas: [tempo_de_resposta_excedido, erro_interno_do_servidor]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso run-3) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Status 429: o servidor ou um intermediário recusou por excesso de requisições num intervalo. Resposta rápida e com corpo — não é lentidão nem erro interno.
@@ -24,3 +25,6 @@
 
 ## Causa
 A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado.
+
+## Notas do modelo
+- [E1 · run-3 · nota] Adicionar nota explicando que o 429 pode vir de um proxy, gateway ou servidor diferente do esperado. — Motivo: Esta nota ajudará a identificar que o 429 não é sempre do lado da CobaiaAPI, mas pode vir de outros componentes do sistema.
--- epoca-0/erros/localizador_quebrado.md
+++ epoca-3/erros/localizador_quebrado.md
@@ -10,9 +10,14 @@
 status: ativo
 causa_raiz: localizador_quebrado
 arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_geral.php]
-sintomas: [elemento nao encontrado, tempo esgotado procurando elemento, seletor casou dois elementos, texto do botao diferente]
-palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout]
+sintomas: [elemento nao encontrado, tempo esgotado procurando elemento, seletor casou dois elementos, texto do botao diferente, elementos reais de produtos_api.php, lista da api nao tem order by, roteiro nao localiza elementos, botoes desabilitados, confusao, tempo de resposta excedido, localizador quebrado, botoes de preco desabilitados]
+palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout, seletores, elementos, api, localizacao, ambiguidade, order by]
 causas_relacionadas: [estado_da_tela_divergente, recurso_inexistente]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-6) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-9) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E2, caso efe-6) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso efe-12) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado.
@@ -23,3 +28,10 @@
 
 ## Causa
 Elementos reais de produtos_api.php: #produtos-api-grid, .thumbnail, button.saiba-mais[data-id], #modalDetalhe; a lista da API não tem ORDER BY (produtos.py:38).
+
+## Notas do modelo
+- [E1 · efe-6 · nota] Adicionar nota explicando que o localizador pode ser quebrado devido à ausência de ORDER BY na lista da API, o que pode causar problemas de localização de elementos. — Motivo: Esta nota ajudará a identificar que o problema está no localizador e não nos dados, explicando a causa raiz do erro.
+- [E1 · efe-9 · nota] Adicionar exemplos de seletores corretos para diferentes elementos na documentação. — Motivo: A evidência deste caso mostrou que o problema estava no localizador, não no dado, e que a documentação não tinha exemplos claros de como selecionar elementos corretamente.
+- [E1 · efe-12 · nota] Adicionar nota sobre seletores quebrados e ambiguidade em elementos. — Motivo: A notificação ajudará a identificar problemas de seletores quebrados e ambiguidade em elementos, facilitando a correção desses problemas.
+- [E2 · efe-6 · nota] Adicionar ORDER BY na consulta SQL em produtos.py para garantir a ordem dos produtos na lista. — Motivo: A ausência de ORDER BY na lista da API pode causar problemas de localização de elementos, como o localizador quebrado, resultando em tempo de resposta excedido.
+- [E3 · efe-12 · nota] Adicionar nota explicando que seletores como nth-child podem ser ambíguos e que a ausência de ORDER BY na lista da API pode causar problemas de localização de elementos. — Motivo: Esta nota ajudará a explicar a causa raiz da falha e fornecerá exemplos de seletores corretos para diferentes elementos, melhorando a documentação e evitando falhas semelhantes no futuro.
--- epoca-0/erros/recurso_inexistente.md
+++ epoca-3/erros/recurso_inexistente.md
@@ -11,9 +11,10 @@
 causa_raiz: recurso_inexistente
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/routers/admin_fault.py]
 endpoints: [GET /api/produtos/{id}, GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
-sintomas: [HTTP 404, Not Found, produto nao encontrado, cliente nao encontrado, pedido nao encontrado, rota errada]
-palavras_chave: [404, not found, nao encontrado, inexistente, rota, endpoint, singular, plural, 403, 422, detail]
+sintomas: [HTTP 404, Not Found, produto nao encontrado, cliente nao encontrado, pedido nao encontrado, rota errada, paginas de erro inesperadas, feedback confuso]
+palavras_chave: [404, not found, nao encontrado, inexistente, rota, endpoint, singular, plural, 403, 422, detail, tratamento de erros, mensagens de erro, feedback ao usuario]
 causas_relacionadas: [erro_interno_do_servidor, localizador_quebrado]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso run-7) - Revisar: nota acrescentada.
 ---
 ## Resumo
 404: id ou rota inexistente. O detail diz qual: "produto não encontrado" (produtos.py:52), "cliente não encontrado" (pedidos.py:37,52), "pedido não encontrado" (pedidos.py:74); "Not Found" genérico é rota inexistente (ex.: /api/produto).
@@ -24,3 +25,6 @@
 
 ## Causa
 Cada 404 com mensagem vem de db.get/filter vazio na rota.
+
+## Notas do modelo
+- [E1 · run-7 · nota] Adicionar exemplos de mensagens de erro específicas para diferentes tipos de recursos inexistentes. — Motivo: Aumentar a clareza das mensagens de erro para que o usuário saiba exatamente o que aconteceu, facilitando diagnóstico e resolução.
--- epoca-0/erros/resposta_truncada.md
+++ epoca-3/erros/resposta_truncada.md
@@ -9,9 +9,11 @@
 status: ativo
 causa_raiz: resposta_truncada
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py]
-sintomas: [fim inesperado da entrada, json cortado, content-length menor que o corpo]
-palavras_chave: [truncad, cortad, incomplet, unexpected end, content-length, tamanho, parcial, malformed_json]
+sintomas: [fim inesperado da entrada, json cortado, content-length menor que o corpo, resposta incompleta, content-length inconsistente, listagem incompleta]
+palavras_chave: [truncad, cortad, incomplet, unexpected end, content-length, tamanho, parcial, malformed_json, resposta truncada, proxy, conexao]
 causas_relacionadas: [corpo_nao_e_json, corpo_vazio, tempo_de_resposta_excedido]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso lex-5) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso lex-14) - Revisar: nota acrescentada.
 ---
 ## Resumo
 O corpo começa como JSON válido e termina no meio de um valor ou chave — faltam bytes; o parse falha com "Unexpected end of JSON input".
@@ -22,3 +24,7 @@
 
 ## Causa
 O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio.
+
+## Notas do modelo
+- [E1 · lex-5 · retificação de "Content-Length menor que o esperado."] Adicionar verificação de Content-Length em produtos.py para garantir que a resposta não seja truncada. — Motivo: A verificação de Content-Length ajuda a identificar e corrigir casos de resposta truncada, garantindo que a resposta completa seja enviada ao cliente.
+- [E1 · lex-14 · nota] Adicionar nota explicando que a resposta pode ser truncada devido a limites de proxy ou conexões interrompidas. — Motivo: Esta nota ajudará a explicar a causa raiz da falha, que é a resposta truncada, e como ela pode ocorrer, facilitando o diagnóstico futuro.
--- epoca-0/erros/tempo_de_resposta_excedido.md
+++ epoca-3/erros/tempo_de_resposta_excedido.md
@@ -11,9 +11,11 @@
 causa_raiz: tempo_de_resposta_excedido
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
 endpoints: [GET /api/produtos]
-sintomas: [demora de segundos, timeout, conexao encerrada por tempo, carregando por muito tempo]
-palavras_chave: [timeout, lento, lentidao, demora, latencia, segundos, tempo esgotado, volume, 2 s]
+sintomas: [demora de segundos, timeout, conexao encerrada por tempo, carregando por muito tempo, conexao encerrada, tempo de espera, atraso no servidor, tempo de resposta excedido]
+palavras_chave: [timeout, lento, lentidao, demora, latencia, segundos, tempo esgotado, volume, 2 s, tempo de resposta, tempo limite, atraso]
 causas_relacionadas: [limite_de_requisicoes, erro_interno_do_servidor, corpo_vazio]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso run-15) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso efe-6) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A resposta demora além do aceitável ou nunca chega: sem status (conexão encerrada) ou 200 tardio. 429 e 500 respondem rápido com um código — aqui não.
@@ -24,3 +26,7 @@
 
 ## Causa
 O modo latency dorme 2 s fixos (fault_injection.py:66); atrasos maiores vêm de banco, rede ou carga; o fetch da página não tem tempo limite.
+
+## Notas do modelo
+- [E1 · run-15 · nota] Adicionar nota explicando que o tempo de resposta excedido pode ser causado por atrasos no servidor ou rede, além do modo latency dormindo 2 segundos fixos. — Motivo: Esta nota ajudará a explicar a causa raiz do problema, que é o atraso no servidor ou rede, além do modo latency dormindo 2 segundos fixos, o que pode não estar claro para os desenvolvedores.
+- [E3 · efe-6 · nota] Adicionar um tempo limite maior para as requisições do front-end. — Motivo: O caso atual demonstrou que o tempo de resposta excedido pode ser causado por atrasos no servidor ou rede, além do modo latency dormindo 2 segundos fixos. Adicionar um tempo limite maior pode resolver esse problema.
--- epoca-0/erros/tipo_divergente.md
+++ epoca-3/erros/tipo_divergente.md
@@ -11,9 +11,11 @@
 causa_raiz: tipo_divergente
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py]
 endpoints: [GET /api/produtos, GET /api/pedidos]
-sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada]
-palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal]
+sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada, preco como texto, destaque como texto, destaque como numero]
+palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal, conversao de tipos, api, json, destaque]
 causas_relacionadas: [valor_fora_do_dominio, formato_de_data_divergente, escala_ou_unidade_errada]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso semt-13) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E2, caso semt-10) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Chave certa com o tipo JSON errado: número entre aspas ("89.90"), booleano como texto ("Sim") ou número (1), inteiro como texto ("4").
@@ -24,3 +26,7 @@
 
 ## Causa
 O modo type_drift aplica str() ao campo-alvo (fault_injection.py:76). A API converte DECIMAL em número e 'Sim'/'Não' em booleano (_to_dict).
+
+## Notas do modelo
+- [E1 · semt-13 · retificação de "O modo type_drift aplica str() ao campo-alvo"] Ajustar a função de conversão de tipos para garantir que os valores sejam retornados no formato correto conforme o contrato. — Motivo: A evidência deste caso mostrou que a função de conversão de tipos estava aplicando str() ao campo-alvo, o que resultava em valores incorretamente formatados. A correção desta função deve resolver o problema de exibição incorreta dos preços.
+- [E2 · semt-10 · retificação de "destaque fora de true/false sai literal"] Ajustar a função de conversão de tipos para garantir que o valor 'Sim' seja convertido em true e 'Não' em false. — Motivo: A evidência deste caso mostrou que a função de conversão de tipos estava aplicando str() ao campo-alvo, o que resultava em valores não booleanos. Ajustar a função para retornar valores booleanos conforme o contrato corrigiria o problema.
--- epoca-0/negocio/entidade-produto.md
+++ epoca-3/negocio/entidade-produto.md
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
--- epoca-0/negocio/usuario-e-login.md
+++ epoca-3/negocio/usuario-e-login.md
@@ -10,9 +10,10 @@
 status: ativo
 arquivos: [Programacao/CobaiaFront/admin/login.php, Programacao/CobaiaFront/admin/acesso_com.php, Programacao/CobaiaAPI/app/models.py]
 tabelas: [tbusuarios]
-sintomas: [reserva com nome de outro usuario, saudacao vazia]
-palavras_chave: [usuario, login, cpf, senha, nivel, sup, cli, administrador, cliente, sessao]
+sintomas: [reserva com nome de outro usuario, saudacao vazia, nome incorreto em reservas]
+palavras_chave: [usuario, login, cpf, senha, nivel, sup, cli, administrador, cliente, sessao, juncao de usuarios, chave de juncao]
 causas_relacionadas: [chave_de_juncao_errada, nulo_inesperado]
+# ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-2) - Revisar: retificação acrescentada.
 ---
 ## Resumo
 Conta em tbusuarios: login_usuario, senha_usuario, nivel_usuario ('sup' admin, 'cli' cliente). Para o cliente o login é o CPF, que vira o campo cpf da API.
@@ -23,3 +24,6 @@
 
 ## Causa
 login.php:7 compara a senha em texto puro; 'sup' abre o painel, 'cli' abre cliente/index.php?cliente=<login>, falha vai a invasor.php.
+
+## Notas do modelo
+- [E1 · tra-2 · retificação de "nome ou cpf de outra pessoa na reserva: junção por id trocada"] Corrigir a junção entre tbusuarios e tbpedido_reserva para garantir que o nome do usuário correto seja exibido. — Motivo: A evidência deste caso mostrou que o nome incorreto estava sendo exibido devido a uma junção incorreta entre os registros de usuários e reservas. A correção desta junção resolve o problema.
```
