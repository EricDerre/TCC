<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py --segundo_passe a partir de `fase4_segundo_passe` (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# O segundo passe do diagnóstico, só nos casos com sinal (corrida 26), gerada em 2026-11-12

Só nos casos das corridas 22 (os oficiais de avaliação) e 24 (os inéditos da ficha 27) em que um sinal em código acendeu na primeira resposta, o selo baixo ou a FONTE divergente, o agente recebeu um segundo pedido de diagnóstico, uma única vez: o mesmo prompt congelado, o mesmo modelo e os 3 verbetes seguintes da mesma busca (posições 4 a 6) no lugar dos três primeiros. A primeira resposta é a que a corrida de referência gravou e não foi repetida, e o segundo pedido não fala dela. São 24 casos com sinal em 72 (corrida 26, decisão 120).

Regra fixada antes da corrida (decisão 120). A resposta final de cada caso é escolhida por regra em código: fica a primeira resposta, salvo quando a segunda dá outra causa da lista, não acende nenhum dos dois sinais (não cai no selo baixo, e algum verbete entregue no segundo pedido trata da causa respondida, com a FONTE dentro dos entregues) e tem probabilidade maior que a da primeira; só então fica a segunda. A diferença entre a resposta final e a primeira sai do ruído quando o teste pareado exato (McNemar, bilateral) dá p abaixo de 0,05, com a corrida completa e a ponte da versão do Ollama pareável com a Fase 3 (b + c até 2, decisão 47). Fora disso a diferença fica dentro do ruído e o agente não muda; se sair do ruído, mudar o agente é outra decisão.

Veredito: dentro do ruído. A corrida rodou em outra versão do Ollama que as corridas de referência; a ponte dessa versão (`fase3b_ponte_04015`) deu b = 1 e c = 0 em 35 casos, pareável com a Fase 3 (limite 2).

Se a segunda resposta valesse sempre, ela consertaria 2 dos 10 erros com sinal e estragaria 6 dos 14 acertos com sinal; a causa respondida foi a mesma em 11 casos. Pela regra de escolha, a resposta trocou em 8 casos: 1 passaram a acertar e 3 passaram a errar, e o agente iria de 56 a 54 acertos em 72. O segundo pedido teve mediana de 1260 tokens de entrada, contra 1185 do primeiro nos mesmos casos, e de 67,53 s por caso. 2 dos 24 segundos pedidos passaram do limite de 1409 tokens que o plano da Fase 4 fixa para o prompt na tela.

<!-- tabela:tb_f4_segpasse_resumo -->
| Casos | Com sinal | Segundos passes feitos | Acertos da primeira resposta | Acertos da resposta final | A segunda consertaria | A segunda estragaria | Mesma causa nas duas | Trocas pela regra | Passaram a acertar (b) | Passaram a errar (c) | Saldo | p do teste pareado | Tokens de entrada (mediana) no segundo pedido | Tokens de entrada (mediana) no primeiro | Acima do limite de tokens | Segundos (mediana) no segundo pedido | Veredito |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 72 | 24 | 24 | 56 | 54 | 2 | 6 | 11 | 8 | 1 | 3 | -2 | 0,625 | 1260 | 1185 | 2 | 67,53 | dentro do ruído |
<!-- /tabela:tb_f4_segpasse_resumo -->
<!-- tabela:tb_f4_segpasse_sinal -->
| Sinal aceso na primeira resposta | Casos com segundo passe | Erros na primeira resposta | Acertos na primeira resposta | A segunda consertaria | A segunda estragaria | Mesma causa nas duas | Trocas pela regra | Passaram a acertar (b) | Passaram a errar (c) |
|---|---|---|---|---|---|---|---|---|---|
| só o selo baixo | 12 | 5 | 7 | 1 | 4 | 4 | 5 | 0 | 3 |
| só a FONTE divergente | 9 | 3 | 6 | 0 | 2 | 6 | 1 | 0 | 0 |
| os dois sinais | 3 | 2 | 1 | 1 | 0 | 1 | 2 | 1 | 0 |
<!-- /tabela:tb_f4_segpasse_sinal -->
<!-- tabela:tb_f4_segpasse_banco -->
| Banco | Primeira resposta | Casos do banco | Com sinal | Casos com segundo passe | Erros na primeira resposta | Acertos na primeira resposta | A segunda consertaria | A segunda estragaria | Mesma causa nas duas | Trocas pela regra | Passaram a acertar (b) | Passaram a errar (c) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| os 36 oficiais de avaliação | corrida 22 | 36 | 8 | 8 | 3 | 5 | 0 | 3 | 2 | 4 | 0 | 2 |
| os 36 inéditos da ficha 27 | corrida 24 | 36 | 16 | 16 | 7 | 9 | 2 | 3 | 9 | 4 | 1 | 1 |
<!-- /tabela:tb_f4_segpasse_banco -->
<!-- tabela:tb_f4_segpasse_alcance -->
| Onde está o verbete da causa certa | Casos com segundo passe | Erros na primeira resposta | Acertos na primeira resposta | A segunda consertaria | A segunda estragaria | Mesma causa nas duas | Trocas pela regra | Passaram a acertar (b) | Passaram a errar (c) |
|---|---|---|---|---|---|---|---|---|---|
| entre os três do primeiro pedido | 9 | 3 | 6 | 0 | 4 | 3 | 4 | 0 | 3 |
| entre os seguintes | 5 | 3 | 2 | 1 | 0 | 3 | 2 | 1 | 0 |
| fora dos dois pedidos | 10 | 4 | 6 | 1 | 2 | 5 | 2 | 0 | 0 |
<!-- /tabela:tb_f4_segpasse_alcance -->
<!-- tabela:tb_f4_segpasse_regras -->
| Se a escolha fosse | Trocas de causa | Passariam a acertar (b) | Passariam a errar (c) | Acertos nos casos todos | p do teste pareado |
|---|---|---|---|---|---|
| sempre a primeira (o agente de hoje) | 0 | 0 | 0 | 56 | 1,000 |
| sempre a segunda | 13 | 2 | 6 | 52 | 0,289 |
| a de maior probabilidade, sem olhar os sinais | 9 | 1 | 3 | 54 | 0,625 |
| a regra fixada antes da corrida | 8 | 1 | 3 | 54 | 0,625 |
<!-- /tabela:tb_f4_segpasse_regras -->
<!-- tabela:tb_f4_segpasse_motivos -->
| O que a regra de escolha achou | Casos | Fica |
|---|---|---|
| a segunda resposta não traz uma causa da lista | 0 | a primeira |
| as duas respostas dão a mesma causa | 11 | a primeira |
| a segunda resposta cai no selo baixo | 4 | a primeira |
| a segunda resposta acende a FONTE divergente | 0 | a primeira |
| a probabilidade da segunda não passa a da primeira | 1 | a primeira |
| a segunda dá outra causa da lista, sem sinal aceso e com probabilidade maior | 8 | a segunda |
<!-- /tabela:tb_f4_segpasse_motivos -->
<!-- tabela:tb_f4_segpasse_casos -->
| Caso | Banco | Sinal | Gabarito | Primeira resposta | Certa | Probabilidade | Segunda resposta | Certa | Probabilidade | Selo da segunda | FONTE divergente na segunda | A segunda sozinha | Fica | Motivo | Mudou | Verbete da causa certa | Verbetes do segundo pedido | Tokens de entrada do segundo pedido |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-4` | avaliacao | só a FONTE divergente | `codificacao_incorreta` | `codificacao_incorreta` | sim | 1,000 | `codificacao_incorreta` | sim | 1,000 | alto | sim | continua certo | a primeira | as duas respostas dão a mesma causa |  | fora dos dois pedidos | `nulo_inesperado`, `tipo_divergente`, `pagina-produtos-api` | 1058 |
| `sin-5` | avaliacao | só o selo baixo | `campo_ausente` | `colecao_no_lugar_de_objeto` | não | 0,625 | `campo_renomeado` | não | 0,998 | alto | não | continua errado | a segunda | a segunda dá outra causa da lista, sem sinal aceso e com probabilidade maior |  | entre os seguintes | `campo_ausente`, `campo_renomeado`, `valor_fora_do_dominio` | 1138 |
| `efe-2` | avaliacao | só o selo baixo | `estado_da_tela_divergente` | `estado_da_tela_divergente` | sim | 0,718 | `valor_fora_do_dominio` | não | 0,906 | medio | não | estragaria | a segunda | a segunda dá outra causa da lista, sem sinal aceso e com probabilidade maior | perda | entre os três do primeiro pedido | `fluxo-reserva-e-cancelamento`, `valor_fora_do_dominio`, `consultas-sem-checagem` | 1025 |
| `efe-3` | avaliacao | só o selo baixo | `campo_ausente` | `campo_ausente` | sim | 0,566 | `nulo_inesperado` | não | 0,500 | baixo | não | estragaria | a primeira | a segunda resposta cai no selo baixo |  | entre os três do primeiro pedido | `chave_de_juncao_errada`, `campo_renomeado`, `nulo_inesperado` | 1208 |
| `lex-8` | avaliacao | só o selo baixo | `codificacao_incorreta` | `codificacao_incorreta` | sim | 0,749 | `codificacao_incorreta` | sim | 0,997 | alto | sim | continua certo | a primeira | as duas respostas dão a mesma causa |  | entre os três do primeiro pedido | `estado_da_tela_divergente`, `tipo_divergente`, `campo_renomeado` | 1143 |
| `sin-14` | avaliacao | só o selo baixo | `campo_renomeado` | `colecao_no_lugar_de_objeto` | não | 0,301 | `tipo_divergente` | não | 0,506 | baixo | não | continua errado | a primeira | a segunda resposta cai no selo baixo |  | entre os três do primeiro pedido | `chave_de_juncao_errada`, `campo_ausente`, `tipo_divergente` | 1219 |
| `semt-14` | avaliacao | só o selo baixo | `nulo_inesperado` | `nulo_inesperado` | sim | 0,740 | `chave_de_juncao_errada` | não | 1,000 | alto | não | estragaria | a segunda | a segunda dá outra causa da lista, sem sinal aceso e com probabilidade maior | perda | entre os três do primeiro pedido | `chave_de_juncao_errada`, `tipo_divergente`, `valor_fora_do_dominio` | 1302 |
| `tra-15` | avaliacao | os dois sinais | `escala_ou_unidade_errada` | `registro_duplicado` | não | 0,639 | `valor_fora_do_dominio` | não | 0,980 | medio | não | continua errado | a segunda | a segunda dá outra causa da lista, sem sinal aceso e com probabilidade maior |  | fora dos dois pedidos | `valor_fora_do_dominio`, `formato_de_data_divergente`, `chave_de_juncao_errada` | 1252 |
| `lex-24` | ineditos | só a FONTE divergente | `codificacao_incorreta` | `codificacao_incorreta` | sim | 0,999 | `codificacao_incorreta` | sim | 0,999 | alto | sim | continua certo | a primeira | as duas respostas dão a mesma causa |  | fora dos dois pedidos | `tipo_divergente`, `estrutura_aninhada_divergente`, `colecao_no_lugar_de_objeto` | 1284 |
| `lex-25` | ineditos | só a FONTE divergente | `codificacao_incorreta` | `codificacao_incorreta` | sim | 0,998 | `codificacao_incorreta` | sim | 1,000 | alto | sim | continua certo | a primeira | as duas respostas dão a mesma causa |  | fora dos dois pedidos | `campo_ausente`, `chave_de_juncao_errada`, `nulo_inesperado` | 1370 |
| `lex-26` | ineditos | só a FONTE divergente | `codificacao_incorreta` | `codificacao_incorreta` | sim | 1,000 | `codificacao_incorreta` | sim | 0,993 | alto | não | continua certo | a primeira | as duas respostas dão a mesma causa |  | entre os seguintes | `contrato-produto`, `codificacao_incorreta`, `colecao_no_lugar_de_objeto` | 1290 |
| `lex-27` | ineditos | os dois sinais | `codificacao_incorreta` | `codificacao_incorreta` | sim | 0,742 | `codificacao_incorreta` | sim | 0,978 | medio | sim | continua certo | a primeira | as duas respostas dão a mesma causa |  | fora dos dois pedidos | `estado_da_tela_divergente`, `valor_fora_do_dominio`, `fluxo-reserva-e-cancelamento` | 1171 |
| `sin-24` | ineditos | só o selo baixo | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | sim | 0,797 | `colecao_no_lugar_de_objeto` | não | 0,968 | medio | não | estragaria | a segunda | a segunda dá outra causa da lista, sem sinal aceso e com probabilidade maior | perda | entre os três do primeiro pedido | `colecao_no_lugar_de_objeto`, `chave_de_juncao_errada`, `campo_renomeado` | 1432 |
| `sin-26` | ineditos | só a FONTE divergente | `campo_ausente` | `resposta_truncada` | não | 0,950 | `nulo_inesperado` | não | 0,999 | alto | não | continua errado | a segunda | a segunda dá outra causa da lista, sem sinal aceso e com probabilidade maior |  | entre os três do primeiro pedido | `nulo_inesperado`, `campo_renomeado`, `chave_de_juncao_errada` | 1392 |
| `sin-27` | ineditos | só o selo baixo | `campo_renomeado` | `campo_renomeado` | sim | 0,413 | `campo_renomeado` | sim | 0,765 | baixo | não | continua certo | a primeira | as duas respostas dão a mesma causa |  | entre os seguintes | `campo_ausente`, `campo_renomeado`, `nulo_inesperado` | 1268 |
| `semt-27` | ineditos | só o selo baixo | `valor_fora_do_dominio` | `colecao_no_lugar_de_objeto` | não | 0,645 | `valor_fora_do_dominio` | sim | 0,610 | baixo | sim | consertaria | a primeira | a segunda resposta cai no selo baixo |  | fora dos dois pedidos | `pagina-produtos-api`, `estado_da_tela_divergente`, `contagem_inconsistente` | 1242 |
| `tra-22` | ineditos | só o selo baixo | `escala_ou_unidade_errada` | `tipo_divergente` | não | 0,811 | `tipo_divergente` | não | 0,999 | alto | não | continua errado | a primeira | as duas respostas dão a mesma causa |  | fora dos dois pedidos | `pagina-produtos-api`, `tipo_divergente`, `chave_de_juncao_errada` | 1380 |
| `tra-23` | ineditos | só o selo baixo | `escala_ou_unidade_errada` | `valor_fora_do_dominio` | não | 0,649 | `tipo_divergente` | não | 0,907 | medio | não | continua errado | a segunda | a segunda dá outra causa da lista, sem sinal aceso e com probabilidade maior |  | fora dos dois pedidos | `estado_da_tela_divergente`, `fluxo-reserva-e-cancelamento`, `formato_de_data_divergente` | 1136 |
| `tra-25` | ineditos | só a FONTE divergente | `contagem_inconsistente` | `resposta_truncada` | não | 0,997 | `resposta_truncada` | não | 0,997 | alto | sim | continua errado | a primeira | as duas respostas dão a mesma causa |  | entre os três do primeiro pedido | `estrutura_aninhada_divergente`, `chave_de_juncao_errada`, `pagina-produtos-api` | 1385 |
| `run-22` | ineditos | só o selo baixo | `limite_de_requisicoes` | `limite_de_requisicoes` | sim | 0,640 | `limite_de_requisicoes` | sim | 0,999 | alto | não | continua certo | a primeira | as duas respostas dão a mesma causa |  | entre os três do primeiro pedido | `tempo_de_resposta_excedido`, `mensagens-de-erro-do-codigo`, `pagina-produtos-api` | 1061 |
| `run-24` | ineditos | só a FONTE divergente | `registro_duplicado` | `registro_duplicado` | sim | 0,970 | `contagem_inconsistente` | não | 0,952 | medio | não | estragaria | a primeira | a probabilidade da segunda não passa a da primeira |  | fora dos dois pedidos | `contagem_inconsistente`, `tipo_divergente`, `chave_de_juncao_errada` | 1465 |
| `run-25` | ineditos | só a FONTE divergente | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | sim | 0,832 | `estado_da_tela_divergente` | não | 0,553 | baixo | não | estragaria | a primeira | a segunda resposta cai no selo baixo |  | fora dos dois pedidos | `estado_da_tela_divergente`, `pagina-produtos-api`, `colecao_no_lugar_de_objeto` | 1205 |
| `run-26` | ineditos | os dois sinais | `dado_desatualizado` | `registro_duplicado` | não | 0,757 | `dado_desatualizado` | sim | 0,999 | alto | não | consertaria | a segunda | a segunda dá outra causa da lista, sem sinal aceso e com probabilidade maior | ganho | entre os seguintes | `fluxo-reserva-e-cancelamento`, `dado_desatualizado`, `chave_de_juncao_errada` | 1378 |
| `efe-27` | ineditos | só a FONTE divergente | `estado_da_tela_divergente` | `dado_desatualizado` | não | 0,875 | `dado_desatualizado` | não | 0,543 | baixo | não | continua errado | a primeira | as duas respostas dão a mesma causa |  | entre os seguintes | `pagina-produtos-api`, `estado_da_tela_divergente`, `tipo_divergente` | 1403 |
<!-- /tabela:tb_f4_segpasse_casos -->
