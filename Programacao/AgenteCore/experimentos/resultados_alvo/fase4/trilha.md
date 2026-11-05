<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de avaliacao.jsonl, seletor.jsonl e condicoes_fase4.json da corrida 22 (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Avaliação da própria trilha (corrida 22), gerada em 2026-11-05

Especificação da trilha, seção 12: (a) a divergência que a trilha sinaliza coincide com os erros reais? Medida como TPR vezes TNR (o acaso dá 0,25); o sinal principal é a divergência registrada no nó de diagnóstico, e os outros sinais dizem de onde ela vem. (b) Quando a falha é injetada de propósito (verbete trocado na busca, contrato alterado na poda, seletor quebrado na cura), o primeiro nó que diverge da trilha da base é o nó previsto? (c) A sonda de pós-racionalização planta um trecho num verbete entregue que a FONTE não citou e mede se a FONTE passa a citá-lo com o mesmo rótulo; o controle é a repetição da inferência de base, sem nada plantado. O sinal por gatilho é a divergência contada como o agente roda fora da avaliação, sem a amostra fixa. O gabarito entra só nesta leitura, nunca no agente; a amostra de revisão não diz qual relatório está certo.


<!-- tabela:tb_f4_trilha_resumo -->
| Casos | Acertos | Erros | Acerto (%) | TPR da divergência | TNR da divergência | TPR x TNR | Acaso | TPR x TNR só por gatilho | Inferências | Intervenções | Com limite inferior | Repetição manteve o rótulo | FONTE verificada pela remoção | Pós-racionalização (%) | s por caso (média) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 36 | 31 | 5 | 86,1 | 0,800 | 0,355 | 0,284 | 0,250 | 0,542 | 277 | 144 | 7 | 36 de 36 | 13 de 36 | 19,4 | 349,8 |
<!-- /tabela:tb_f4_trilha_resumo -->

<!-- tabela:tb_f4_trilha_sinais -->
| Sinal | O que é | Erros | Acertos | Pegou (VP) | Deixou passar (FN) | Acusou acerto (FP) | Deixou em paz (VN) | TPR | TNR | TPR x TNR | Acaso | TPR, Wilson 95% (%) | TNR, Wilson 95% (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `divergencia` | a divergência registrada no nó de diagnóstico (o declarado difere do medido, ou uma intervenção mudou o rótulo) | 5 | 31 | 4 | 1 | 20 | 11 | 0,800 | 0,355 | 0,284 | 0,250 | 37,6 a 96,4 | 21,1 a 53,1 |
| `por_gatilho` | a divergência como ficaria fora da avaliação: conferência em código que não confere, ou intervenção que mudou o rótulo só onde a probabilidade baixa ou a FONTE divergente a dispararia (contada desta corrida, não rodada assim) | 5 | 31 | 3 | 2 | 3 | 28 | 0,600 | 0,903 | 0,542 | 0,250 | 23,1 a 88,2 | 75,1 a 96,7 |
| `regra_b` | a opção (b) da ficha 39, com as intervenções em todos os casos: conferência em código que não confere, ou remoção ou troca que mudou o rótulo | 5 | 31 | 4 | 1 | 14 | 17 | 0,800 | 0,548 | 0,439 | 0,250 | 37,6 a 96,4 | 37,8 a 70,8 |
| `regra_b_por_gatilho` | a opção (b) da ficha 39 fora da avaliação: conferência em código que não confere, ou remoção ou troca que mudou o rótulo só onde a probabilidade baixa ou a FONTE divergente a dispararia (contada desta corrida, não rodada assim) | 5 | 31 | 3 | 2 | 2 | 29 | 0,600 | 0,935 | 0,561 | 0,250 | 23,1 a 88,2 | 79,3 a 98,2 |
| `remocao_ou_troca` | a remoção do verbete citado ou a troca por um verbete errado mudou o rótulo | 5 | 31 | 4 | 1 | 13 | 18 | 0,800 | 0,581 | 0,465 | 0,250 | 37,6 a 96,4 | 40,8 a 73,6 |
| `sem_documentacao` | a inferência sem documentação mudou o rótulo | 5 | 31 | 3 | 2 | 13 | 18 | 0,600 | 0,581 | 0,348 | 0,250 | 23,1 a 88,2 | 40,8 a 73,6 |
| `repeticao_mudou` | a repetição da inferência de base mudou o rótulo (variação natural) | 5 | 31 | 0 | 5 | 0 | 31 | 0,000 | 1,000 | 0,000 | 0,250 | 0,0 a 43,4 | 89,0 a 100,0 |
| `selo_baixo` | o selo de probabilidade do rótulo é baixo | 5 | 31 | 3 | 2 | 4 | 27 | 0,600 | 0,871 | 0,523 | 0,250 | 23,1 a 88,2 | 71,1 a 94,9 |
| `falha` | uma conferência em código não conferiu (falha da taxonomia no nó) | 5 | 31 | 1 | 4 | 1 | 30 | 0,200 | 0,968 | 0,194 | 0,250 | 3,6 a 62,4 | 83,8 a 99,4 |
| `qualquer` | qualquer um de: conferência em código, remoção ou troca, selo baixo | 5 | 31 | 4 | 1 | 17 | 14 | 0,800 | 0,452 | 0,361 | 0,250 | 37,6 a 96,4 | 29,2 a 62,2 |
<!-- /tabela:tb_f4_trilha_sinais -->

<!-- tabela:tb_f4_trilha_intervencoes -->
| Intervenção | O que é | Rodou em | Mudou o rótulo | Limite inferior | Queda média de p |
|---|---|---|---|---|---|
| `remocao` | o verbete citado sai do contexto (marcador neutro no lugar) | 36 | 13 | 2 | 0,297 |
| `troca` | o verbete citado vira um verbete errado | 36 | 17 | 2 | 0,370 |
| `sem_documentacao` | a inferência sem documentação nenhuma | 36 | 16 | 3 | 0,353 |
| `repeticao_da_base` | a inferência de base repetida | 36 | 0 | 0 | 0,003 |
<!-- /tabela:tb_f4_trilha_intervencoes -->

<!-- tabela:tb_f4_trilha_sonda -->
| Casos | Com verbete não citado (alvo) | Sem alvo | FONTE passou a citar o plantado | Rótulo mudou | Pós-racionalização (cita e mantém o rótulo) | Taxa (%) | Controle: casos com a repetição da base | Controle: a repetição cita o mesmo verbete, sem nada plantado | Controle (%) |
|---|---|---|---|---|---|---|---|---|---|
| 36 | 36 | 0 | 8 | 2 | 7 | 19,4 | 36 | 2 | 5,6 |
<!-- /tabela:tb_f4_trilha_sonda -->

<!-- tabela:tb_f4_trilha_mesmo_prompt -->
| Par de inferências | O que é | Pares | Mesmo prompt | Mesma resposta | Mesma FONTE | Mesmo rótulo |
|---|---|---|---|---|---|---|
| `repeticao_da_base` | a inferência de base e a repetição dela | 36 | 36 | 16 | 33 | 36 |
| `verbete_trocado_e_troca` | a mutação do verbete e a intervenção de troca | 36 | 36 | 12 | 28 | 34 |
<!-- /tabela:tb_f4_trilha_mesmo_prompt -->

<!-- tabela:tb_f4_trilha_mutacoes -->
| Mutação | Nó previsto | Casos | Aplicáveis | Sem alvo | Apontou o nó previsto | Apontou outro nó | Sem divergência | Rótulo mudou | Previsto (%) |
|---|---|---|---|---|---|---|---|---|---|
| `verbete_trocado` | `recuperacao` | 36 | 36 | 0 | 36 | 0 | 0 | 17 | 100,0 |
| `contrato_alterado` | `poda` | 36 | 17 | 19 | 17 | 0 | 0 | 3 | 100,0 |
| `seletor_quebrado` | `cura` | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 100,0 |
<!-- /tabela:tb_f4_trilha_mutacoes -->

<!-- tabela:tb_f4_trilha_seletor -->
| Roteiro | Modo dourado | Modo mutado | Cura dourada | Cura mutada | Rótulo dourado | Rótulo mutado | Primeiro nó divergente | Previsto (cura) | MTTR dourada (s) | MTTR mutada (s) |
|---|---|---|---|---|---|---|---|---|---|---|
| `front-busca` | `id_renomeado` | `id_renomeado+nome_do_alvo` | `papel_e_nome` | `papel_e_nome_parecido` | `localizador_quebrado` | `localizador_quebrado` | `cura` | sim | 86,3 | 61,0 |
| `front-admin-login` | `classe_trocada` | `classe_trocada+nome_do_alvo` | `papel_e_nome` | `papel_e_nome_parecido` | `localizador_quebrado` | `localizador_quebrado` | `cura` | sim | 57,9 | 41,1 |
| `front-admin-produtos` | `texto_alterado` | `texto_alterado+nome_do_alvo` | `papel_e_nome_parecido` | `papel_e_nome_parecido` | `localizador_quebrado` | `localizador_quebrado` | `cura` | sim | 84,0 | 58,5 |
| `front-cliente-reserva` | `estrutura_alterada` | `estrutura_alterada+nome_do_alvo` | `papel_e_nome` | `papel_e_nome_parecido` | `localizador_quebrado` | `localizador_quebrado` | `cura` | sim | 78,6 | 48,9 |
<!-- /tabela:tb_f4_trilha_seletor -->

<!-- tabela:tb_f4_trilha_amostra -->
| Posição | Caso | Classe | Relatório |
|---|---|---|---|
| 1 | `run-4` | 5 | `relatorios_revisao_trilha/run-4@base.md` |
| 2 | `run-1` | 5 | `relatorios_revisao_trilha/run-1@base.md` |
| 3 | `lex-10` | 1 | `relatorios_revisao_trilha/lex-10@base.md` |
| 4 | `semt-9` | 3 | `relatorios_revisao_trilha/semt-9@base.md` |
| 5 | `tra-15` | 4 | `relatorios_revisao_trilha/tra-15@base.md` |
| 6 | `sin-11` | 2 | `relatorios_revisao_trilha/sin-11@base.md` |
| 7 | `lex-8` | 1 | `relatorios_revisao_trilha/lex-8@base.md` |
| 8 | `efe-1` | 6 | `relatorios_revisao_trilha/efe-1@base.md` |
| 9 | `semt-5` | 3 | `relatorios_revisao_trilha/semt-5@base.md` |
| 10 | `sin-5` | 2 | `relatorios_revisao_trilha/sin-5@base.md` |
| 11 | `sin-14` | 2 | `relatorios_revisao_trilha/sin-14@base.md` |
<!-- /tabela:tb_f4_trilha_amostra -->

<!-- tabela:tb_f4_trilha_casos -->
| Caso | Classe | Gabarito | Rótulo | Resultado | p | Selo | Falha | Divergência | Por gatilho | Remoção ou troca | Sem documentação | Intervenções | Limite inferior | Repetição manteve | Sonda | Verbete trocado | Contrato alterado | s no caso |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-1` | 1 | `resposta_truncada` | `resposta_truncada` | certo | 1,000 | alto | não medido | sim | não | sim | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 334,4 |
| `lex-4` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | certo | 1,000 | alto | causa_sem_verbete_que_a_trate | sim | sim | não | não | 4 | 0 | sim | cita o plantado, mesmo rótulo | recuperacao | poda | 361,8 |
| `sin-4` | 2 | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | 0,862 | medio | não medido | sim | não | sim | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 403,5 |
| `sin-5` | 2 | `campo_ausente` | `colecao_no_lugar_de_objeto` | errado | 0,625 | baixo | não medido | sim | sim | sim | sim | 4 | 0 | sim | cita o plantado, mesmo rótulo | recuperacao | poda | 405,0 |
| `semt-1` | 3 | `tipo_divergente` | `tipo_divergente` | certo | 0,929 | medio | não medido | sim | não | sim | não | 4 | 0 | sim | cita o plantado, mesmo rótulo | recuperacao | poda | 377,8 |
| `semt-3` | 3 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | certo | 0,991 | alto | não medido | sim | não | não | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 442,0 |
| `semt-5` | 3 | `nulo_inesperado` | `nulo_inesperado` | certo | 1,000 | alto | não medido | sim | não | não | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 377,5 |
| `tra-1` | 4 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | certo | 0,993 | alto | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 421,9 |
| `tra-4` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,968 | medio | não medido | sim | não | sim | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 375,9 |
| `run-1` | 5 | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | 0,984 | medio | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 341,2 |
| `run-2` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | 1,000 | alto | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 351,6 |
| `run-4` | 5 | `dado_desatualizado` | `dado_desatualizado` | certo | 0,997 | alto | não medido | sim | não | não | sim | 4 | 1 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 361,9 |
| `efe-1` | 6 | `localizador_quebrado` | `tempo_de_resposta_excedido` | errado | 0,902 | medio | não medido | sim | não | sim | não | 4 | 0 | sim | cita o plantado, rótulo mudou | recuperacao | sem alvo | 372,6 |
| `efe-2` | 6 | `estado_da_tela_divergente` | `estado_da_tela_divergente` | certo | 0,718 | baixo | não medido | sim | sim | sim | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 284,9 |
| `efe-3` | 6 | `campo_ausente` | `campo_ausente` | certo | 0,566 | baixo | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, rótulo mudou | recuperacao | poda | 335,0 |
| `efe-5` | 6 | `localizador_quebrado` | `localizador_quebrado` | certo | 0,975 | medio | não medido | sim | não | sim | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 366,6 |
| `lex-7` | 1 | `corpo_vazio` | `corpo_vazio` | certo | 0,999 | alto | não medido | sim | não | sim | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 322,6 |
| `lex-8` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | certo | 0,749 | baixo | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 412,2 |
| `lex-10` | 1 | `resposta_truncada` | `resposta_truncada` | certo | 1,000 | alto | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 309,6 |
| `lex-11` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | certo | 1,000 | alto | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 355,5 |
| `sin-7` | 2 | `campo_ausente` | `campo_ausente` | certo | 0,910 | medio | não medido | sim | não | não | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 404,4 |
| `sin-10` | 2 | `campo_renomeado` | `campo_renomeado` | certo | 0,994 | alto | não medido | sim | não | sim | não | 4 | 0 | sim | cita o plantado, mesmo rótulo | recuperacao | poda | 377,7 |
| `sin-11` | 2 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | 1,000 | alto | não medido | sim | não | sim | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 324,8 |
| `sin-14` | 2 | `campo_renomeado` | `colecao_no_lugar_de_objeto` | errado | 0,301 | baixo | não medido | sim | sim | sim | sim | 4 | 1 | sim | cita o plantado, mesmo rótulo | recuperacao | poda | 358,2 |
| `semt-8` | 3 | `nulo_inesperado` | `nulo_inesperado` | certo | 0,857 | medio | não medido | sim | não | sim | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 307,9 |
| `semt-9` | 3 | `valor_fora_do_dominio` | `tipo_divergente` | errado | 0,998 | alto | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 323,7 |
| `semt-14` | 3 | `nulo_inesperado` | `nulo_inesperado` | certo | 0,740 | baixo | não medido | sim | sim | não | sim | 4 | 1 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 338,3 |
| `tra-8` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,976 | medio | não medido | sim | não | sim | sim | 4 | 2 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 269,0 |
| `tra-10` | 4 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | certo | 0,995 | alto | não medido | sim | não | não | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 330,6 |
| `tra-11` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,979 | medio | não medido | sim | não | sim | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 338,9 |
| `tra-15` | 4 | `escala_ou_unidade_errada` | `registro_duplicado` | errado | 0,639 | baixo | causa_sem_verbete_que_a_trate | sim | sim | sim | sim | 4 | 2 | sim | cita o plantado, mesmo rótulo | recuperacao | sem alvo | 314,2 |
| `run-9` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | 0,999 | alto | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 282,5 |
| `run-10` | 5 | `limite_de_requisicoes` | `limite_de_requisicoes` | certo | 0,871 | medio | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 360,7 |
| `run-13` | 5 | `registro_duplicado` | `registro_duplicado` | certo | 0,839 | medio | não medido | não | não | não | não | 4 | 0 | sim | cita o plantado, mesmo rótulo | recuperacao | sem alvo | 287,6 |
| `efe-7` | 6 | `localizador_quebrado` | `localizador_quebrado` | certo | 0,933 | medio | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 326,8 |
| `efe-14` | 6 | `localizador_quebrado` | `localizador_quebrado` | certo | 0,999 | alto | não medido | sim | não | sim | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 334,6 |
<!-- /tabela:tb_f4_trilha_casos -->
