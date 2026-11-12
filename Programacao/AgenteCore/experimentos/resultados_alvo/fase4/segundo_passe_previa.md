<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por experimento_segundo_passe.py --previa a partir de `biblioteca_producao/`, `fase4_trilha` e `fase4_ineditos` (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Prévia sem modelo da corrida 26: o que o segundo passe do diagnóstico alcança, gerada em 2026-11-10

Sem modelo. Dos 72 casos das corridas 22 e 24, um sinal em código acendeu na primeira resposta de 24: 12 só com o selo baixo, 9 só com a FONTE divergente e 3 com os dois. Neles estão 10 dos 16 erros das duas corridas e 14 acertos; os outros 6 erros não acendem sinal e não têm segundo passe. A corrida 26 faz um segundo pedido por caso com sinal, com os 3 verbetes seguintes da mesma busca (posições 4 a 6) no lugar dos três primeiros. A busca refeita agora devolve os três verbetes gravados em 24 dos 24 casos, e o contexto do primeiro pedido se refaz igual em 24.

O que a corrida consegue enxergar. Dos 10 erros com sinal, o verbete da causa certa fica entre os seguintes em 3; em 3 ele já estava entre os três do primeiro pedido, e em 4 fica fora dos dois pedidos. Dos 14 acertos com sinal, 6 tinham o verbete da causa certa entre os três primeiros e deixam de recebê-lo no segundo pedido. No melhor cenário, com os 3 erros ao alcance consertados e nenhum acerto perdido, o teste pareado exato dá p = 0,250; para passar do corte seriam precisos 6 consertos sem nenhuma perda. O resultado não tem como sair do ruído: a corrida serve para contar quantos erros o segundo passe conserta e quantas respostas certas ele estraga.

O tamanho do prompt. O segundo pedido tem mediana estimada de 1277 tokens (máximo 1513), contra 1185 do primeiro nos mesmos casos; 6 dos 24 passam do limite de 1409 tokens que o plano da Fase 4 fixa para o prompt na tela (no primeiro pedido dos mesmos casos, que é em texto, o número acima do limite era 1). Pelo tempo das corridas de referência, as 24 inferências levam cerca de 25 minutos.

Regra fixada antes da corrida (decisão 120). A resposta final de cada caso é escolhida por regra em código: fica a primeira resposta, salvo quando a segunda dá outra causa da lista, não acende nenhum dos dois sinais (não cai no selo baixo, e algum verbete entregue no segundo pedido trata da causa respondida, com a FONTE dentro dos entregues) e tem probabilidade maior que a da primeira; só então fica a segunda. A diferença entre a resposta final e a primeira sai do ruído quando o teste pareado exato (McNemar, bilateral) dá p abaixo de 0,05, com a corrida completa e a ponte da versão do Ollama pareável com a Fase 3 (b + c até 2, decisão 47). Fora disso a diferença fica dentro do ruído e o agente não muda; se sair do ruído, mudar o agente é outra decisão.

<!-- tabela:tb_f4_segpasse_previa_resumo -->
| Casos | Com sinal | Erros com sinal | Acertos com sinal | Erros sem sinal | Erros com o verbete certo entre os seguintes | Erros com o verbete certo já entregue | Erros com o verbete certo fora dos dois pedidos | Acertos que perdem o verbete certo | p do melhor cenário | Consertos para sair do ruído | Tokens estimados (mediana) | Acima do limite de tokens | Minutos estimados |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 72 | 24 | 10 | 14 | 6 | 3 | 3 | 4 | 6 | 0,250 | 6 | 1277 | 6 | 25 |
<!-- /tabela:tb_f4_segpasse_previa_resumo -->
<!-- tabela:tb_f4_segpasse_previa_sinal -->
| Sinal aceso na primeira resposta | Casos | Erros | Acertos | Erros com o verbete certo entre os seguintes | Acertos que perdem o verbete certo |
|---|---|---|---|---|---|
| só o selo baixo | 12 | 5 | 7 | 1 | 6 |
| só a FONTE divergente | 9 | 3 | 6 | 1 | 0 |
| os dois sinais | 3 | 2 | 1 | 1 | 0 |
<!-- /tabela:tb_f4_segpasse_previa_sinal -->
<!-- tabela:tb_f4_segpasse_previa_banco -->
| Banco | Primeira resposta | Casos do banco | Com sinal | Erros com sinal | Acertos com sinal | Erros com o verbete certo entre os seguintes |
|---|---|---|---|---|---|---|
| os 36 oficiais de avaliação | corrida 22 | 36 | 8 | 3 | 5 | 1 |
| os 36 inéditos da ficha 27 | corrida 24 | 36 | 16 | 7 | 9 | 2 |
<!-- /tabela:tb_f4_segpasse_previa_banco -->
<!-- tabela:tb_f4_segpasse_previa_alternativas -->
| Desenho do segundo pedido | Verbetes no pedido | Erros com o verbete certo ao alcance | Tokens estimados (mediana) | Tokens estimados (máximo) | Acima do limite de tokens | O que ficou |
|---|---|---|---|---|---|---|
| 2 seguintes (posições 4 e 5), no lugar dos três primeiros | 2 | 3 | 1046,5 | 1284 | 0 | descartado: alcança os mesmos erros com um prompt menor, mas o pedido sai do k = 3 em que o selo foi calibrado |
| 3 seguintes (posições 4 a 6), no lugar dos três primeiros | 3 | 3 | 1277 | 1513 | 6 | escolhido: contexto novo, com o mesmo k = 3 do primeiro pedido e da calibração do selo |
| os três primeiros mais 2 seguintes (5 verbetes) | 5 | 3 | 1602,5 | 1897 | 23 | descartado: repete o contexto da primeira resposta e passa do limite de tokens; a corrida 16 já mediu 5 verbetes para todos os casos (5 ganhos, 8 perdas) |
| os três primeiros mais 3 seguintes (6 verbetes) | 6 | 3 | 1844,5 | 2135 | 24 | descartado: repete o contexto da primeira resposta e passa do limite de tokens em todos os casos |
| 7 seguintes (posições 4 a 10), no lugar dos três primeiros | 7 | 5 | 2069,5 | 2299 | 24 | descartado: alcança mais erros, mas o prompt quase dobra e fica fora do tamanho em que o selo foi calibrado |
<!-- /tabela:tb_f4_segpasse_previa_alternativas -->
<!-- tabela:tb_f4_segpasse_previa_casos -->
| Caso | Banco | Sinal | Gabarito | Primeira resposta | Certa | Probabilidade | Posição do verbete da causa certa na busca | Verbete da causa certa | Verbetes do primeiro pedido | Verbetes do segundo pedido | Tokens do primeiro pedido | Tokens estimados do segundo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-4` | avaliacao | só a FONTE divergente | `codificacao_incorreta` | `codificacao_incorreta` | sim | 1,000 | 13 | fora dos dois pedidos | `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente` | `nulo_inesperado`, `tipo_divergente`, `pagina-produtos-api` | 1110 | 1042 |
| `sin-5` | avaliacao | só o selo baixo | `campo_ausente` | `colecao_no_lugar_de_objeto` | não | 0,625 | 4 | entre os seguintes | `entidade-produto`, `contrato-produto`, `tipo_divergente` | `campo_ausente`, `campo_renomeado`, `valor_fora_do_dominio` | 1188 | 1176 |
| `efe-2` | avaliacao | só o selo baixo | `estado_da_tela_divergente` | `estado_da_tela_divergente` | sim | 0,718 | 2 | entre os três do primeiro pedido | `contrato-pedido`, `estado_da_tela_divergente`, `pedido-reserva` | `fluxo-reserva-e-cancelamento`, `valor_fora_do_dominio`, `consultas-sem-checagem` | 1055 | 1010 |
| `efe-3` | avaliacao | só o selo baixo | `campo_ausente` | `campo_ausente` | sim | 0,566 | 3 | entre os três do primeiro pedido | `entidade-produto`, `contrato-produto`, `campo_ausente` | `chave_de_juncao_errada`, `campo_renomeado`, `nulo_inesperado` | 1091 | 1247 |
| `lex-8` | avaliacao | só o selo baixo | `codificacao_incorreta` | `codificacao_incorreta` | sim | 0,749 | 1 | entre os três do primeiro pedido | `codificacao_incorreta`, `contrato-produto`, `entidade-produto` | `estado_da_tela_divergente`, `tipo_divergente`, `campo_renomeado` | 1116 | 1185 |
| `sin-14` | avaliacao | só o selo baixo | `campo_renomeado` | `colecao_no_lugar_de_objeto` | não | 0,301 | 3 | entre os três do primeiro pedido | `entidade-produto`, `contrato-produto`, `campo_renomeado` | `chave_de_juncao_errada`, `campo_ausente`, `tipo_divergente` | 1137 | 1252 |
| `semt-14` | avaliacao | só o selo baixo | `nulo_inesperado` | `nulo_inesperado` | sim | 0,740 | 3 | entre os três do primeiro pedido | `entidade-produto`, `contrato-produto`, `nulo_inesperado` | `chave_de_juncao_errada`, `tipo_divergente`, `valor_fora_do_dominio` | 1135 | 1360 |
| `tra-15` | avaliacao | os dois sinais | `escala_ou_unidade_errada` | `registro_duplicado` | não | 0,639 | 7 | fora dos dois pedidos | `contrato-pedido`, `pedido-reserva`, `fluxo-reserva-e-cancelamento` | `valor_fora_do_dominio`, `formato_de_data_divergente`, `chave_de_juncao_errada` | 1096 | 1289 |
| `lex-24` | ineditos | só a FONTE divergente | `codificacao_incorreta` | `codificacao_incorreta` | sim | 0,999 | 22 | fora dos dois pedidos | `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente` | `tipo_divergente`, `estrutura_aninhada_divergente`, `colecao_no_lugar_de_objeto` | 1149 | 1295 |
| `lex-25` | ineditos | só a FONTE divergente | `codificacao_incorreta` | `codificacao_incorreta` | sim | 0,998 | 7 | fora dos dois pedidos | `entidade-produto`, `contrato-produto`, `campo_renomeado` | `campo_ausente`, `chave_de_juncao_errada`, `nulo_inesperado` | 1341 | 1397 |
| `lex-26` | ineditos | só a FONTE divergente | `codificacao_incorreta` | `codificacao_incorreta` | sim | 1,000 | 5 | entre os seguintes | `entidade-produto`, `campo_ausente`, `pagina-produtos-api` | `contrato-produto`, `codificacao_incorreta`, `colecao_no_lugar_de_objeto` | 1176 | 1307 |
| `lex-27` | ineditos | os dois sinais | `codificacao_incorreta` | `codificacao_incorreta` | sim | 0,742 | 22 | fora dos dois pedidos | `contrato-pedido`, `pedido-reserva`, `formato_de_data_divergente` | `estado_da_tela_divergente`, `valor_fora_do_dominio`, `fluxo-reserva-e-cancelamento` | 1179 | 1190 |
| `sin-24` | ineditos | só o selo baixo | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | sim | 0,797 | 3 | entre os três do primeiro pedido | `contrato-produto`, `entidade-produto`, `estrutura_aninhada_divergente` | `colecao_no_lugar_de_objeto`, `chave_de_juncao_errada`, `campo_renomeado` | 1276 | 1496 |
| `sin-26` | ineditos | só a FONTE divergente | `campo_ausente` | `resposta_truncada` | não | 0,950 | 3 | entre os três do primeiro pedido | `entidade-produto`, `contrato-produto`, `campo_ausente` | `nulo_inesperado`, `campo_renomeado`, `chave_de_juncao_errada` | 1275 | 1434 |
| `sin-27` | ineditos | só o selo baixo | `campo_renomeado` | `campo_renomeado` | sim | 0,413 | 5 | entre os seguintes | `contrato-produto`, `entidade-produto`, `chave_de_juncao_errada` | `campo_ausente`, `campo_renomeado`, `nulo_inesperado` | 1469 | 1265 |
| `semt-27` | ineditos | só o selo baixo | `valor_fora_do_dominio` | `colecao_no_lugar_de_objeto` | não | 0,645 | 7 | fora dos dois pedidos | `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` | `pagina-produtos-api`, `estado_da_tela_divergente`, `contagem_inconsistente` | 1338 | 1260 |
| `tra-22` | ineditos | só o selo baixo | `escala_ou_unidade_errada` | `tipo_divergente` | não | 0,811 | 12 | fora dos dois pedidos | `entidade-produto`, `nulo_inesperado`, `contrato-produto` | `pagina-produtos-api`, `tipo_divergente`, `chave_de_juncao_errada` | 1246 | 1426 |
| `tra-23` | ineditos | só o selo baixo | `escala_ou_unidade_errada` | `valor_fora_do_dominio` | não | 0,649 | 16 | fora dos dois pedidos | `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio` | `estado_da_tela_divergente`, `fluxo-reserva-e-cancelamento`, `formato_de_data_divergente` | 1182 | 1110 |
| `tra-25` | ineditos | só a FONTE divergente | `contagem_inconsistente` | `resposta_truncada` | não | 0,997 | 3 | entre os três do primeiro pedido | `entidade-produto`, `contrato-produto`, `contagem_inconsistente` | `estrutura_aninhada_divergente`, `chave_de_juncao_errada`, `pagina-produtos-api` | 1267 | 1413 |
| `run-22` | ineditos | só o selo baixo | `limite_de_requisicoes` | `limite_de_requisicoes` | sim | 0,640 | 1 | entre os três do primeiro pedido | `limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente` | `tempo_de_resposta_excedido`, `mensagens-de-erro-do-codigo`, `pagina-produtos-api` | 1207 | 1004 |
| `run-24` | ineditos | só a FONTE divergente | `registro_duplicado` | `registro_duplicado` | sim | 0,970 | 15 | fora dos dois pedidos | `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` | `contagem_inconsistente`, `tipo_divergente`, `chave_de_juncao_errada` | 1376 | 1513 |
| `run-25` | ineditos | só a FONTE divergente | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | sim | 0,832 | 7 | fora dos dois pedidos | `entidade-produto`, `ancora-saiba-mais`, `contrato-produto` | `estado_da_tela_divergente`, `pagina-produtos-api`, `colecao_no_lugar_de_objeto` | 1160 | 1241 |
| `run-26` | ineditos | os dois sinais | `dado_desatualizado` | `registro_duplicado` | não | 0,757 | 5 | entre os seguintes | `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio` | `fluxo-reserva-e-cancelamento`, `dado_desatualizado`, `chave_de_juncao_errada` | 1292 | 1372 |
| `efe-27` | ineditos | só a FONTE divergente | `estado_da_tela_divergente` | `dado_desatualizado` | não | 0,875 | 5 | entre os seguintes | `entidade-produto`, `contrato-produto`, `nulo_inesperado` | `pagina-produtos-api`, `estado_da_tela_divergente`, `tipo_divergente` | 1409 | 1427 |
<!-- /tabela:tb_f4_segpasse_previa_casos -->
