<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-2 -> epoca-3), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-2 -> epoca-3

| Métrica | Valor |
|---|---|
| Arquivos novos | 0 |
| Arquivos removidos | 0 |
| Arquivos tocados | 7 |
| Linhas acrescentadas | 29 |
| Linhas removidas | 13 |
| Caracteres antes | 63449 |
| Caracteres depois | 67040 |
| Caracteres acrescentados | 3591 |
| Tokens estimados acrescentados | 1381 |

```diff
--- epoca-2/erros/campo_renomeado.md
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
--- epoca-2/erros/corpo_nao_e_json.md
+++ epoca-3/erros/corpo_nao_e_json.md
@@ -10,12 +10,13 @@
 status: ativo
 causa_raiz: corpo_nao_e_json
 arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaFront/produtos_api.php]
-sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, pagina html de erro 404, falha de parse, fatal error, memoria esgotada, resposta html, falha ao acessar de fora da rede local, resposta html em vez de json]
-palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, resposta json, erro 404, erro de memoria, php, conexao, resposta html, erro de integracao]
+sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, pagina html de erro 404, falha de parse, fatal error, memoria esgotada, resposta html, falha ao acessar de fora da rede local, resposta html em vez de json, falha em ambientes externos]
+palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, resposta json, erro 404, erro de memoria, php, conexao, resposta html, erro de integracao, ambiente externo, erro 500]
 causas_relacionadas: [resposta_truncada, corpo_vazio, erro_interno_do_servidor]
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso lex-6) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5-coder:7b (E2, caso lex-12) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5-coder:7b (E2, caso lex-15) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso lex-15) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.
@@ -31,3 +32,4 @@
 - [E1 · lex-6 · nota] Adicionar nota: A resposta deve ser um JSON válido, não uma página HTML de erro. — Motivo: A documentação atual não destaca que a resposta deve ser JSON, o que pode levar a diagnósticos incorretos quando a resposta não atende a este formato esperado.
 - [E2 · lex-12 · nota] Adicionar nota: Erros de memória em PHP podem causar respostas HTML inválidas, interrompendo a exibição de dados JSON. — Motivo: O erro de memória em PHP (Fatal error: Allowed memory size exhausted) é uma causa comum de respostas HTML inválidas, o que corresponde ao sintoma observado.
 - [E2 · lex-15 · nota] Adicionar nota explicando que a resposta deve ser JSON válido, não uma página HTML de erro. — Motivo: A nota ajudará a identificar rapidamente a causa da falha, que é a resposta HTML em vez de JSON, especialmente quando a resposta é 200 e o Content-Type indica JSON.
+- [E3 · lex-15 · nota] Adicionar nota explicando que erros de resposta HTML podem ocorrer em ambientes externos devido a falhas no servidor ou gateway. — Motivo: Esta nota ajuda a entender que a falha não é exclusiva do ambiente local, mas também pode afetar ambientes externos, explicando a inconsistência observada.
--- epoca-2/erros/corpo_vazio.md
+++ epoca-3/erros/corpo_vazio.md
@@ -10,10 +10,11 @@
 status: ativo
 causa_raiz: corpo_vazio
 arquivos: [Programacao/CobaiaFront/produtos_api.php]
-sintomas: [carregando indefinidamente, tela em branco sem erro, fim inesperado da entrada em corpo vazio, tabela de reservas vazia, erro de carregamento]
-palavras_chave: [vazio, sem corpo, branco, 204, espacos, nenhum byte, carregando, resposta vazia, erro de integracao]
+sintomas: [carregando indefinidamente, tela em branco sem erro, fim inesperado da entrada em corpo vazio, tabela de reservas vazia, erro de carregamento, pagina de carregamento indefinido, dados nao retornados]
+palavras_chave: [vazio, sem corpo, branco, 204, espacos, nenhum byte, carregando, resposta vazia, erro de integracao, erro interno, rota errada]
 causas_relacionadas: [resposta_truncada, corpo_nao_e_json, estado_da_tela_divergente]
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso lex-13) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso lex-3) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Status de sucesso e nenhum byte útil no corpo (vazio, só espaços, ou 204). Diferente de "[]", lista vazia, que é JSON válido.
@@ -27,3 +28,4 @@
 
 ## Notas do modelo
 - [E1 · lex-13 · nota] Adicionar nota: "Ocorre quando a API retorna uma resposta vazia, que pode ser devido a um erro interno ou a uma rota errada." — Motivo: Esta nota ajuda a identificar a causa raiz do problema, que é um corpo vazio, e fornece contexto sobre onde pode ocorrer.
+- [E3 · lex-3 · nota] Adicionar nota explicando que o corpo vazio pode ser causado por erros internos ou rotas incorretas. — Motivo: Esta nota ajuda a identificar rapidamente a causa do problema, facilitando o diagnóstico em casos sem corpo JSON válido.
--- epoca-2/erros/erro_interno_do_servidor.md
+++ epoca-3/erros/erro_interno_do_servidor.md
@@ -11,11 +11,12 @@
 causa_raiz: erro_interno_do_servidor
 arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/conn/connect.php]
 endpoints: [GET /api/produtos, POST /api/pedidos]
-sintomas: [HTTP 500, Internal Server Error, fault injection error_500, falha intermitente, intermitente sem padrao, em toda requisicao, banco inacessivel]
-palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora, injetor, banco inacessivel, defeito na rota, excecao nao tratada]
+sintomas: [HTTP 500, Internal Server Error, fault injection error_500, falha intermitente, intermitente sem padrao, em toda requisicao, banco inacessivel, erro interno do servidor, banco fora]
+palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora, injetor, banco inacessivel, defeito na rota, excecao nao tratada, falhas de banco de dados, injetores de erros]
 causas_relacionadas: [corpo_nao_e_json, tempo_de_resposta_excedido, limite_de_requisicoes]
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso run-6) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso run-12) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso run-6) - Revisar: nota acrescentada.
 ---
 ## Resumo
 500 com {"detail": ...}: falha própria da API. detail "fault injection: error_500 em produto" é o injetor; "Internal Server Error" é exceção não tratada.
@@ -30,3 +31,4 @@
 ## Notas do modelo
 - [E1 · run-6 · nota] Adicionar nota explicando que o erro interno do servidor pode ocorrer devido a falhas no banco de dados ou defeitos na rota, além de ser intermitente. — Motivo: Esta nota ajudará a explicar a causa raiz do erro interno do servidor em rotas de produtos, que é um problema de infraestrutura relacionado ao banco de dados ou rotas.
 - [E1 · run-12 · nota] Adicionar nota explicando que o erro interno do servidor pode ser causado por falhas de banco de dados ou injetores de erros. — Motivo: Esta nota ajudará a identificar rapidamente falhas de banco de dados ou injetores de erros como a causa raiz do problema.
+- [E3 · run-6 · nota] Adicionar nota explicando que o erro interno do servidor pode ocorrer devido a falhas no banco de dados ou defeitos na rota, além de ser intermitente. Adicionar nota explicando que o erro interno do servidor pode ser causado por falhas de banco de dados ou injetores de erros. — Motivo: Esta nota ajudará a explicar as possíveis causas do erro interno do servidor, incluindo falhas no banco de dados e injetores de erros, o que pode ajudar a diagnosticar o problema corretamente.
--- epoca-2/erros/estado_da_tela_divergente.md
+++ epoca-3/erros/estado_da_tela_divergente.md
@@ -11,11 +11,12 @@
 status: ativo
 causa_raiz: estado_da_tela_divergente
 arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/reserva_cli.php]
-sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar, lista vazia, botao inativo, botao de cancelar continua habilitado, reserva segue como ativa]
-palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML, atualizacao de estado, carregamento, interface, dependencia de redirect]
+sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar, lista vazia, botao inativo, botao de cancelar continua habilitado, reserva segue como ativa, tela nao reflete dados atualizados, estado inconsistente]
+palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML, atualizacao de estado, carregamento, interface, dependencia de redirect, carregamento de dados, interface do usuario]
 causas_relacionadas: [localizador_quebrado, dado_desatualizado, corpo_vazio]
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-4) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-15) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso efe-13) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A rede está certa — status e corpo conferem — e o usuário vê outra coisa: "Carregando" parado, lista vazia, botão que não muda.
@@ -30,3 +31,4 @@
 ## Notas do modelo
 - [E1 · efe-4 · nota] Adicionar nota explicando que a atualização do estado da tela deve ocorrer após o carregamento dos dados. — Motivo: Esta nota ajudará a entender que a interface não está atualizando corretamente após o carregamento dos dados, o que é o problema observado neste caso.
 - [E1 · efe-15 · retificação de "cancelar depende do redirect (cliente_cancelar.php:7)"] Adicionar verificação de status na interface para refletir mudanças sem dependência de redirect. — Motivo: Este trecho demonstra que a interface depende de um redirect para atualizar o estado, o que pode não refletir corretamente as mudanças na API. A adição de uma verificação de status na interface resolveria este problema.
+- [E3 · efe-13 · nota] Adicionar nota explicando que a atualização do estado da tela deve ocorrer após o carregamento dos dados, evitando que a resposta mais antiga sobrescreva a mais nova. — Motivo: Esta nota ajuda a entender que a atualização da interface deve ocorrer após o carregamento dos dados, explicando a causa da divergência entre o estado da tela e a resposta da API.
--- epoca-2/erros/localizador_quebrado.md
+++ epoca-3/erros/localizador_quebrado.md
@@ -10,13 +10,14 @@
 status: ativo
 causa_raiz: localizador_quebrado
 arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_geral.php]
-sintomas: [elemento nao encontrado, tempo esgotado procurando elemento, seletor casou dois elementos, texto do botao diferente, elementos reais de produtos_api.php, lista da api nao tem order by, roteiro nao localiza elementos, botoes desabilitados, confusao, tempo de resposta excedido, localizador quebrado]
+sintomas: [elemento nao encontrado, tempo esgotado procurando elemento, seletor casou dois elementos, texto do botao diferente, elementos reais de produtos_api.php, lista da api nao tem order by, roteiro nao localiza elementos, botoes desabilitados, confusao, tempo de resposta excedido, localizador quebrado, botoes de preco desabilitados]
 palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout, seletores, elementos, api, localizacao, ambiguidade, order by]
 causas_relacionadas: [estado_da_tela_divergente, recurso_inexistente]
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-6) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-9) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-12) - Revisar: nota acrescentada.
 # ! Alteração por modelo qwen2.5-coder:7b (E2, caso efe-6) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso efe-12) - Revisar: nota acrescentada.
 ---
 ## Resumo
 Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado.
@@ -33,3 +34,4 @@
 - [E1 · efe-9 · nota] Adicionar exemplos de seletores corretos para diferentes elementos na documentação. — Motivo: A evidência deste caso mostrou que o problema estava no localizador, não no dado, e que a documentação não tinha exemplos claros de como selecionar elementos corretamente.
 - [E1 · efe-12 · nota] Adicionar nota sobre seletores quebrados e ambiguidade em elementos. — Motivo: A notificação ajudará a identificar problemas de seletores quebrados e ambiguidade em elementos, facilitando a correção desses problemas.
 - [E2 · efe-6 · nota] Adicionar ORDER BY na consulta SQL em produtos.py para garantir a ordem dos produtos na lista. — Motivo: A ausência de ORDER BY na lista da API pode causar problemas de localização de elementos, como o localizador quebrado, resultando em tempo de resposta excedido.
+- [E3 · efe-12 · nota] Adicionar nota explicando que seletores como nth-child podem ser ambíguos e que a ausência de ORDER BY na lista da API pode causar problemas de localização de elementos. — Motivo: Esta nota ajudará a explicar a causa raiz da falha e fornecerá exemplos de seletores corretos para diferentes elementos, melhorando a documentação e evitando falhas semelhantes no futuro.
--- epoca-2/erros/tempo_de_resposta_excedido.md
+++ epoca-3/erros/tempo_de_resposta_excedido.md
@@ -11,10 +11,11 @@
 causa_raiz: tempo_de_resposta_excedido
 arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
 endpoints: [GET /api/produtos]
-sintomas: [demora de segundos, timeout, conexao encerrada por tempo, carregando por muito tempo, conexao encerrada, tempo de espera, atraso no servidor]
-palavras_chave: [timeout, lento, lentidao, demora, latencia, segundos, tempo esgotado, volume, 2 s, tempo de resposta]
+sintomas: [demora de segundos, timeout, conexao encerrada por tempo, carregando por muito tempo, conexao encerrada, tempo de espera, atraso no servidor, tempo de resposta excedido]
+palavras_chave: [timeout, lento, lentidao, demora, latencia, segundos, tempo esgotado, volume, 2 s, tempo de resposta, tempo limite, atraso]
 causas_relacionadas: [limite_de_requisicoes, erro_interno_do_servidor, corpo_vazio]
 # ! Alteração por modelo qwen2.5-coder:7b (E1, caso run-15) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5-coder:7b (E3, caso efe-6) - Revisar: nota acrescentada.
 ---
 ## Resumo
 A resposta demora além do aceitável ou nunca chega: sem status (conexão encerrada) ou 200 tardio. 429 e 500 respondem rápido com um código — aqui não.
@@ -28,3 +29,4 @@
 
 ## Notas do modelo
 - [E1 · run-15 · nota] Adicionar nota explicando que o tempo de resposta excedido pode ser causado por atrasos no servidor ou rede, além do modo latency dormindo 2 segundos fixos. — Motivo: Esta nota ajudará a explicar a causa raiz do problema, que é o atraso no servidor ou rede, além do modo latency dormindo 2 segundos fixos, o que pode não estar claro para os desenvolvedores.
+- [E3 · efe-6 · nota] Adicionar um tempo limite maior para as requisições do front-end. — Motivo: O caso atual demonstrou que o tempo de resposta excedido pode ser causado por atrasos no servidor ou rede, além do modo latency dormindo 2 segundos fixos. Adicionar um tempo limite maior pode resolver esse problema.
```
