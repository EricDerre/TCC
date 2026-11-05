<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de biblioteca.jsonl, propostas, lote.json, reavaliacao, correcoes.jsonl e sonda.json da corrida (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Biblioteca em produção e ciclo de correção (corrida 20), gerada em 2026-11-04

Cada caso de aprendizado foi diagnosticado (da tela quando reproduz, do fixture nos outros) e, na continuação do mesmo prompt, o modelo propôs edições; o validador congelado da Fase 3 decide primeiro e os 13 filtros em código da decisão 65 depois; a regra dos 40% segura para revisão humana a nota em verbete presente em 40% ou mais dos contextos da calibração. A regra R5 compara o lote com a cópia curada nos 36 inéditos (b e c); a regra R4 compara a marca corrigido do ciclo de correção com o conjunto de casos cujo modo o harness desligou. A sonda repete a de 28/09/2026 com a recuperação por id ligada.


<!-- tabela:tb_f4_biblioteca_resumo -->
| Casos de aprendizado | Da tela | Do fixture | Acertos do diagnóstico | Acerto (%) | Propostas | Aceitas (lote) | Abstenções (NENHUMA) | Para revisão humana | Recusadas pelos filtros do P5 | Recusadas pela Fase 3 | Taxa de rejeição (%) | Casos com verbete pelo id | Inferências | Segundos | Trilha (bytes) | k | Base dos inéditos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 54 | 24 | 30 | 37 | 68,5 | 92 | 19 | 0 | 1 | 16 | 56 | 78,3 | 10 | 158 | 16466,1 | 3347613 | 3 | corrida12 |
<!-- /tabela:tb_f4_biblioteca_resumo -->

<!-- tabela:tb_f4_biblioteca_filtros -->
| Filtro em código (decisão 65) | Propostas barradas ou seguradas |
|---|---|
| `evidencia_obrigatoria` | 6 |
| `atomicidade` | 1 |
| `abstencao_valida` | 0 |
| `fonte_confiavel` | 5 |
| `granularidade` | 0 |
| `peso_por_tipo` | 0 |
| `redundancia` | 3 |
| `proveniencia` | 0 |
| `auditoria_por_etapa` | 0 |
| `conflito_deterministico` | 0 |
| `metricas_por_rodada` | 0 |
| `revisao_humana_amostral` | 0 |
| `regra_dos_40` | 1 |
<!-- /tabela:tb_f4_biblioteca_filtros -->

<!-- tabela:tb_f4_biblioteca_rejeicoes -->
| Quem recusou | Código | Propostas |
|---|---|---|
| validador da Fase 3 | `arquivo_inexistente` | 4 |
| validador da Fase 3 | `duplicada` | 14 |
| validador da Fase 3 | `id_repetido` | 12 |
| validador da Fase 3 | `palavra_chave_invalida` | 15 |
| validador da Fase 3 | `retificacao_sem_trecho` | 1 |
| validador da Fase 3 | `teto_notas_verbete` | 1 |
| validador da Fase 3 | `teto_verbetes_novos` | 3 |
| validador da Fase 3 | `texto_curto` | 2 |
| validador da Fase 3 | `texto_longo` | 2 |
| validador da Fase 3 | `trecho_nao_encontrado` | 2 |
| filtros do P5 | `mensagem_nao_encontrada_no_codigo` | 5 |
| filtros do P5 | `redundante` | 3 |
| filtros do P5 | `sem_evidencia_do_caso` | 6 |
| filtros do P5 | `texto_de_origem_proibida` | 1 |
| filtros do P5 | `texto_nao_atomico` | 1 |
<!-- /tabela:tb_f4_biblioteca_rejeicoes -->

<!-- tabela:tb_f4_biblioteca_lote -->
| Edições no lote | Para revisão humana | Peso somado | Por tipo | Hash do lote | Notas na cópia | Verbetes | Verbetes novos |
|---|---|---|---|---|---|---|---|
| 19 | 1 | 34 | `nota` 10, `novo_verbete` 6, `retificacao` 3 | 9f3154eee72d | 22 | 46 | 10 |
<!-- /tabela:tb_f4_biblioteca_lote -->

<!-- tabela:tb_f4_biblioteca_reavaliacao -->
| Inéditos pareados | Acerto com a cópia curada (%) | Acerto com o lote (%) | b (passaram a acertar) | c (passaram a errar) | p (McNemar exato) | Veredito R5 | Casos que mudaram | Base |
|---|---|---|---|---|---|---|---|---|
| 36 | 75,0 | 75,0 | 0 | 0 | 1,000 | aceito | nenhum | pre_fase4_confianca (corrida 12, cópia curada 1fca10f1a6f6, Ollama 0.34.4) |
<!-- /tabela:tb_f4_biblioteca_reavaliacao -->

<!-- tabela:tb_f4_biblioteca_correcao -->
| Casos com sintoma antes | Modo desligado | Modo mantido | Marcados corrigido | Certos | Falsos positivos | Perdidos | Precisão (%) | Revocação (%) | Kappa | Sem sintoma antes |
|---|---|---|---|---|---|---|---|---|---|---|
| 9 | 4 | 5 | 4 | 4 | 0 | 0 | 100,0 | 100,0 | 1,000 | `sin-15` |
<!-- /tabela:tb_f4_biblioteca_correcao -->

<!-- tabela:tb_f4_biblioteca_correcao_casos -->
| Caso | Modo | Verbetes | Modo desligado | Reproduziu antes | Passou depois | Fio mudou | Árvore mudou | Marcado | Motivo |
|---|---|---|---|---|---|---|---|---|---|
| `lex-2` | `corpo_nao_e_json` | `corpo_nao_e_json` | não | sim | não | não | não | não | a reexecução ainda falha: nada a marcar |
| `lex-9` | `corpo_nao_e_json` | `corpo_nao_e_json` | sim | sim | sim | sim | sim | sim | o roteiro passou e o fio e a árvore mudaram entre a corrida que falhava e a que passou |
| `run-7` | `recurso_inexistente` | `recurso_inexistente` | sim | sim | sim | sim | sim | sim | o roteiro passou e o fio e a árvore mudaram entre a corrida que falhava e a que passou |
| `semt-13` | `type_drift` | `entidade-produto` | não | sim | sim | não | não | não | o roteiro passou, mas nada mudou no fio (corpo e tempo da chamada iguais): sem evidência de correção |
| `sin-1` | `field_missing` | `campo_ausente` | não | sim | não | não | não | não | a reexecução ainda falha: nada a marcar |
| `sin-13` | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | sim | sim | sim | sim | sim | sim | o roteiro passou e o fio e a árvore mudaram entre a corrida que falhava e a que passou |
| `sin-15` | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | sim | não | sim | não | não | não | o roteiro passou, mas nada mudou no fio (corpo e tempo da chamada iguais): sem evidência de correção |
| `sin-9` | `field_renamed` | `campo_renomeado` | sim | sim | sim | sim | sim | sim | o roteiro passou e o fio e a árvore mudaram entre a corrida que falhava e a que passou |
| `tra-12` | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | não | sim | sim | não | não | não | o roteiro passou, mas nada mudou no fio (corpo e tempo da chamada iguais): sem evidência de correção |
| `tra-3` | `chave_de_juncao_errada` | `chave_de_juncao_errada` | não | sim | sim | não | não | não | o roteiro passou, mas nada mudou no fio (corpo e tempo da chamada iguais): sem evidência de correção |
<!-- /tabela:tb_f4_biblioteca_correcao_casos -->

<!-- tabela:tb_f4_biblioteca_sonda -->
| Caso | Rótulo agora | Acertou | Propostas | Aceitas | NENHUMA | Motivos de recusa | Menciona a correção | Verbetes pelo id | Rótulo em 28/09 | Propostas em 28/09 | Aceitas em 28/09 | Mudou a proposta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `efe-3` | campo_ausente | sim | 2 | 1 | não | `duplicada` | não | nenhum | campo_ausente | 2 | 0 | sim |
| `lex-9` | corpo_nao_e_json | sim | 2 | 2 | não | nenhum | não | nenhum | não medido | não medido | não medido | sem sonda anterior |
| `sin-9` | campo_renomeado | sim | 2 | 0 | não | `bloco_malformado`, `bloco_malformado` | não | nenhum | não medido | não medido | não medido | sem sonda anterior |
| `sin-13` | estrutura_aninhada_divergente | sim | 2 | 0 | não | `duplicada`, `duplicada` | não | nenhum | não medido | não medido | não medido | sem sonda anterior |
| `sin-15` | colecao_no_lugar_de_objeto | sim | 2 | 1 | não | `trecho_nao_encontrado` | não | nenhum | não medido | não medido | não medido | sem sonda anterior |
| `run-7` | recurso_inexistente | sim | 2 | 0 | não | `palavra_chave_invalida`, `palavra_chave_invalida` | não | nenhum | não medido | não medido | não medido | sem sonda anterior |
| `efe-10` | dado_desatualizado | não | 2 | 0 | não | `duplicada`, `duplicada` | não | `interface-frontend` | dado_desatualizado | 2 | 1 | sim |
<!-- /tabela:tb_f4_biblioteca_sonda -->

<!-- tabela:tb_f4_biblioteca_revisao -->
| Verbete | Operação | Caso | Peso | Parcela na calibração (%) |
|---|---|---|---|---|
| `contrato-produto` | nota | `efe-4` | 1 | 42,2 |
<!-- /tabela:tb_f4_biblioteca_revisao -->

<!-- tabela:tb_f4_biblioteca_recuperacao -->
| Verbete aprendido | Vezes na calibração (k = 3) | Vezes pelo id nesta corrida |
|---|---|---|
| `atualizacao_imediata` | 0 | 1 |
| `interface-estados` | 0 | 1 |
| `interface-frontend` | 0 | 1 |
| `rotas-inexistentes` | 0 | 1 |
<!-- /tabela:tb_f4_biblioteca_recuperacao -->

<!-- tabela:tb_f4_biblioteca_casos -->
| Caso | Origem | Rótulo | Acertou | Selo | Propostas | Aceitas | Para revisão | Recusadas | NENHUMA | Pelo id | Verbetes editados | Segundos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-2` | tela | corpo_nao_e_json | sim | alto | 1 | 0 | 0 | `mensagem_nao_encontrada_no_codigo` | não |  |  | 229,7 |
| `lex-3` | tela | corpo_vazio | sim | medio | 2 | 0 | 0 | `duplicada`, `id_repetido` | não |  |  | 281,4 |
| `lex-5` | fixture | resposta_truncada | sim | alto | 2 | 0 | 0 | `sem_evidencia_do_caso`, `id_repetido` | não |  |  | 243,6 |
| `sin-1` | tela | campo_ausente | sim | alto | 2 | 1 | 0 | `texto_nao_atomico` | não |  | `campo_preco_ausente` | 251,7 |
| `sin-2` | tela | campo_renomeado | sim | medio | 2 | 0 | 0 | `mensagem_nao_encontrada_no_codigo`, `mensagem_nao_encontrada_no_codigo` | não |  |  | 262,5 |
| `sin-3` | tela | tipo_divergente | não | medio | 2 | 0 | 0 | `duplicada`, `duplicada` | não |  |  | 276,5 |
| `semt-2` | tela | tipo_divergente | sim | alto | 2 | 0 | 0 | `texto_curto`, `arquivo_inexistente` | não |  |  | 266,7 |
| `semt-4` | fixture | formato_de_data_divergente | sim | alto | 2 | 0 | 0 | `palavra_chave_invalida`, `palavra_chave_invalida` | não |  |  | 234,9 |
| `tra-2` | fixture | nome_nulo_vindo_da_view | não | medio | 1 | 0 | 0 | `arquivo_inexistente` | não |  |  | 213,8 |
| `tra-3` | tela | tipo_divergente | não | baixo | 2 | 1 | 0 | `duplicada` | não | `chave_de_juncao_errada` | `novo_verbete` | 318,3 |
| `tra-5` | fixture | contagem_inconsistente | não | baixo | 2 | 1 | 0 | `duplicada` | não |  | `pessoas_incorretas` | 232,6 |
| `run-3` | tela | limite_de_requisicoes | sim | alto | 2 | 1 | 0 | `texto_de_origem_proibida` | não |  | `limite_de_requisicoes` | 277,4 |
| `run-5` | fixture | registro_duplicado | sim | alto | 2 | 1 | 0 | `id_repetido` | não |  | `contrato-pedido` | 234,7 |
| `efe-4` | fixture | colecao_no_lugar_de_objeto | não | baixo | 2 | 1 | 1 |  | não | `interface-estados` | `estado_da_tela_divergente` | 234,3 |
| `lex-6` | fixture | recurso_inexistente | não | baixo | 1 | 0 | 0 | `palavra_chave_invalida` | não |  |  | 203,9 |
| `lex-9` | tela | corpo_nao_e_json | sim | medio | 1 | 0 | 0 | `mensagem_nao_encontrada_no_codigo` | não |  |  | 142,2 |
| `lex-12` | tela | corpo_nao_e_json | sim | medio | 1 | 0 | 0 | `arquivo_inexistente` | não |  |  | 149,6 |
| `sin-6` | tela | campo_ausente | sim | alto | 2 | 0 | 0 | `palavra_chave_invalida`, `id_repetido` | não |  |  | 246,6 |
| `sin-8` | fixture | colecao_no_lugar_de_objeto | sim | medio | 2 | 0 | 0 | `duplicada`, `duplicada` | não |  |  | 235,3 |
| `sin-9` | tela | campo_renomeado | sim | alto | 2 | 0 | 0 | `sem_evidencia_do_caso`, `id_repetido` | não | `campo_renomeado` |  | 243,8 |
| `sin-12` | fixture | colecao_no_lugar_de_objeto | não | baixo | 2 | 0 | 0 | `texto_curto`, `id_repetido` | não |  |  | 218,5 |
| `sin-13` | tela | tipo_divergente | não | medio | 1 | 0 | 0 | `duplicada` | não | `estrutura_aninhada_divergente` |  | 270,3 |
| `sin-15` | fixture | colecao_no_lugar_de_objeto | sim | medio | 2 | 1 | 0 | `redundante` | não |  | `colecao_no_lugar_de_objeto` | 186,8 |
| `semt-6` | tela | contagem_inconsistente | não | medio | 2 | 1 | 0 | `palavra_chave_invalida` | não |  | `tipo_divergente` | 257,9 |
| `semt-7` | fixture | formato_de_data_divergente | não | baixo | 2 | 1 | 0 | `id_repetido` | não |  | `tipo_divergente` | 201,4 |
| `semt-10` | tela | tipo_divergente | sim | alto | 2 | 1 | 0 | `sem_evidencia_do_caso` | não |  | `tipo_divergente` | 188,8 |
| `semt-11` | fixture | valor_fora_do_dominio | sim | medio | 1 | 0 | 0 | `arquivo_inexistente` | não |  |  | 193,6 |
| `semt-12` | fixture | formato_de_data_divergente | sim | medio | 1 | 0 | 0 | `palavra_chave_invalida` | não |  |  | 161,5 |
| `semt-13` | tela | tipo_divergente | sim | alto | 1 | 0 | 0 | `teto_notas_verbete` | não | `entidade-produto` |  | 214,9 |
| `semt-15` | fixture | valor_fora_do_dominio | sim | baixo | 2 | 1 | 0 | `duplicada` | não |  | `validacao-na-api` | 221,5 |
| `tra-6` | tela | escala_ou_unidade_errada | sim | baixo | 2 | 1 | 0 | `duplicada` | não |  | `formato_preco` | 285,8 |
| `tra-7` | tela | campo_renomeado | não | medio | 2 | 0 | 0 | `duplicada`, `id_repetido` | não |  |  | 297,9 |
| `tra-9` | fixture | formato_de_data_divergente | não | medio | 2 | 0 | 0 | `palavra_chave_invalida`, `palavra_chave_invalida` | não |  |  | 238,0 |
| `tra-12` | tela | escala_ou_unidade_errada | sim | medio | 2 | 0 | 0 | `duplicada`, `trecho_nao_encontrado` | não | `escala_ou_unidade_errada` |  | 325,2 |
| `tra-13` | tela | imagem_fora_do_dominio | não | baixo | 1 | 0 | 0 | `redundante` | não |  |  | 230,6 |
| `tra-14` | tela | contagem_inconsistente | sim | medio | 2 | 1 | 0 | `palavra_chave_invalida` | não |  | `contagem_inconsistente` | 233,6 |
| `run-6` | fixture | erro_interno_do_servidor | sim | medio | 1 | 0 | 0 | `texto_longo` | não |  |  | 203,8 |
| `run-7` | tela | recurso_inexistente | sim | alto | 1 | 0 | 0 | `palavra_chave_invalida` | não | `recurso_inexistente` |  | 234,6 |
| `run-8` | fixture | recurso_inexistente | sim | medio | 2 | 0 | 0 | `palavra_chave_invalida`, `id_repetido` | não | `rotas-inexistentes` |  | 225,6 |
| `run-11` | fixture | valor_fora_do_dominio | não | medio | 1 | 0 | 0 | `sem_evidencia_do_caso` | não |  |  | 185,6 |
| `run-12` | fixture | erro_interno_do_servidor | sim | medio | 2 | 1 | 0 | `duplicada` | não |  | `erro_interno_do_servidor` | 237,5 |
| `run-14` | fixture | dado_desatualizado | sim | alto | 1 | 0 | 0 | `palavra_chave_invalida` | não |  |  | 179,9 |
| `run-15` | tela | tempo_de_resposta_excedido | sim | medio | 1 | 0 | 0 | `sem_evidencia_do_caso` | não |  |  | 221,8 |
| `efe-6` | fixture | localizador_quebrado | sim | medio | 2 | 0 | 0 | `palavra_chave_invalida`, `id_repetido` | não |  |  | 239,7 |
| `efe-8` | fixture | estado_da_tela_divergente | sim | medio | 2 | 2 | 0 |  | não |  | `estado_da_tela_divergente`, `atualizacao-da-tela` | 224,3 |
| `efe-9` | fixture | localizador_quebrado | sim | alto | 2 | 0 | 0 | `palavra_chave_invalida`, `palavra_chave_invalida` | não |  |  | 227,0 |
| `efe-10` | fixture | valor_fora_do_dominio | não | baixo | 2 | 1 | 0 | `trecho_nao_encontrado` | não | `interface-frontend` | `interface-frontend` | 236,3 |
| `efe-11` | fixture | localizador_quebrado | não | baixo | 2 | 1 | 0 | `teto_verbetes_novos` | não |  | `localizador_quebrado` | 221,8 |
| `efe-12` | fixture | localizador_quebrado | sim | alto | 2 | 0 | 0 | `redundante`, `texto_longo` | não |  |  | 266,7 |
| `efe-13` | fixture | dado_desatualizado | não | medio | 2 | 1 | 0 | `teto_verbetes_novos` | não | `atualizacao_imediata` | `estado_da_tela_divergente` | 217,7 |
| `efe-15` | fixture | estado_da_tela_divergente | sim | alto | 2 | 0 | 0 | `id_repetido`, `sem_evidencia_do_caso` | não |  |  | 225,3 |
| `lex-13` | fixture | corpo_vazio | sim | alto | 1 | 0 | 0 | `id_repetido` | não |  |  | 183,2 |
| `lex-14` | fixture | resposta_truncada | sim | alto | 2 | 0 | 0 | `duplicada`, `teto_verbetes_novos` | não |  |  | 226,3 |
| `lex-15` | tela | corpo_nao_e_json | sim | medio | 2 | 0 | 0 | `mensagem_nao_encontrada_no_codigo`, `retificacao_sem_trecho` | não |  |  | 196,6 |
<!-- /tabela:tb_f4_biblioteca_casos -->
