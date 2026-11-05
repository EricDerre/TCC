<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de os registros, as linhas laterais, a sondagem e a ponte da corrida 16 (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Calibração e ponte da Fase 4 (corrida 16), gerada em 2026-10-28

A probabilidade do rótulo é lida no primeiro token depois de CAUSA_RAIZ: (especificação da trilha, seção 14); a conjunta é a medida da corrida 12. O selo segue a ficha 31 (a): baixo é a parcela de 30% de menor probabilidade (gatilho de intervenção e de revisão humana), alto fica acima da mediana dos acertos, médio entre os dois (regra R7). A regra R8 escolhe o k; a regra R6 confere a ponte de versão contra a Fase 3 (decisão 47).


<!-- tabela:tb_f4_calibracao_resumo -->
| Ollama | Modelo | Casos | k medidos | k escolhido (R8) | Selo baixo até (p) | Selo alto a partir de (p) | Ponte pareável (R6) | Sondagem dos logprobs |
|---|---|---|---|---|---|---|---|---|
| 0.40.2 | `qwen2.5:7b` | 90 | 3, 5 | 3 | 0,832 | 0,990 | sim | ok |
<!-- /tabela:tb_f4_calibracao_resumo -->

<!-- tabela:tb_f4_calibracao_por_k -->
| k | Casos | Completo | Acertos | Acerto (%) | Acurácia balanceada (%) | Nos 36 de avaliação (%) | Nos 54 de aprendizado (%) | s por diagnóstico (mediana) | Tokens de entrada (mediana) | Tokens de entrada (máximo) | AUROC p do rótulo [IC 95%] | AUROC p conjunta [IC 95%] | Sem rótulo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 90 | sim | 68 | 75,6 | 81,5 | 86,1 | 68,5 | 55,4 | 1106,5 | 1281 | 0,799 [0,670; 0,902] | 0,791 [0,661; 0,897] | 0 |
| 5 | 90 | sim | 65 | 72,2 | 75,7 | 77,8 | 68,5 | 60,5 | 1469,0 | 1668 | 0,793 [0,677; 0,893] | 0,816 [0,701; 0,910] | 0 |
<!-- /tabela:tb_f4_calibracao_por_k -->

<!-- tabela:tb_f4_calibracao_revisao -->
| k | Parcela revisada | Casos revisados | Erros pegos | Acertos revisados à toa | Risco no que sobra |
|---|---|---|---|---|---|
| 3 | 10% | 9 | 7 de 22 | 2 | 18,5% |
| 3 | 20% | 18 | 10 de 22 | 8 | 16,7% |
| 3 | 30% | 27 | 15 de 22 | 12 | 11,1% |
| 5 | 10% | 9 | 7 de 25 | 2 | 22,2% |
| 5 | 20% | 18 | 12 de 25 | 6 | 18,1% |
| 5 | 30% | 27 | 16 de 25 | 11 | 14,3% |
<!-- /tabela:tb_f4_calibracao_revisao -->

<!-- tabela:tb_f4_calibracao_selos -->
| Selo | Casos | Certos | Errados | Erro (%) | Casos errados |
|---|---|---|---|---|---|
| baixo | 27 | 12 | 15 | 55,6 | `efe-10`, `efe-11`, `efe-4`, `lex-6`, `semt-6`, `semt-7`, `sin-12`, `sin-14`, `sin-2`, `sin-5`, `tra-12`, `tra-15`, `tra-3`, `tra-5`, `tra-7` |
| medio | 26 | 22 | 4 | 15,4 | `efe-1`, `run-11`, `tra-2`, `tra-9` |
| alto | 37 | 34 | 3 | 8,1 | `efe-13`, `lex-3`, `semt-9` |
<!-- /tabela:tb_f4_calibracao_selos -->

<!-- tabela:tb_f4_calibracao_r8 -->
| Acurácia balanceada k = 3 (%) | Acurácia balanceada k = 5 (%) | b (só k = 5 acerta) | c (só k = 3 acerta) | p (McNemar exato) | k escolhido | Motivo |
|---|---|---|---|---|---|---|
| 81,5 | 75,7 | 5 | 8 | 0,581 | 3 | k = 3 acerta mais por acurácia balanceada (81,5% contra 75,7%) |
<!-- /tabela:tb_f4_calibracao_r8 -->

<!-- tabela:tb_f4_calibracao_ponte -->
| Ollama | Corrida da ponte | Feita nesta corrida | Casos pareados | b (só a ponte acerta) | c (só a Fase 3 acerta) | Pareável (b + c até o limite) | Casos de texto corrigido fora da conta |
|---|---|---|---|---|---|---|---|
| 0.40.2 | fase3b_ponte_0402 | não | 35 | 1 | 0 | sim (limite 2) | efe-3 |
<!-- /tabela:tb_f4_calibracao_ponte -->

<!-- tabela:tb_f4_calibracao_sondagem -->
| Ollama | Tokens com probabilidade | Alternativas por posição (máx.) | Bytes por token | Texto remontado bate | Probabilidade antes ou depois da temperatura | Resposta igual sem logprobs | Rótulo lido | p do rótulo | Avisos |
|---|---|---|---|---|---|---|---|---|---|
| 0.40.2 | 63 | 20 | sim | sim | antes | não | resposta_truncada | 1,000 | a resposta com logprobs difere da resposta sem logprobs no mesmo prompt |
<!-- /tabela:tb_f4_calibracao_sondagem -->

<!-- tabela:tb_f4_calibracao_casos -->
| Caso | Partição | Gabarito | Rótulo | Resultado | p do rótulo | p conjunta | Segunda causa | Selo |
|---|---|---|---|---|---|---|---|---|
| `sin-14` | avaliacao | `campo_renomeado` | `colecao_no_lugar_de_objeto` | errado | 0,301 | 0,300 | tipo_divergente | baixo |
| `tra-15` | avaliacao | `escala_ou_unidade_errada` | `tipo_divergente` | errado | 0,421 | 0,421 | valor_fora_do_dominio | baixo |
| `semt-6` | aprendizado | `tipo_divergente` | `colecao_no_lugar_de_objeto` | errado | 0,443 | 0,442 | tipo_divergente | baixo |
| `sin-1` | aprendizado | `campo_ausente` | `campo_ausente` | certo | 0,484 | 0,481 | tipo_divergente | baixo |
| `run-3` | aprendizado | `limite_de_requisicoes` | `limite_de_requisicoes` | certo | 0,524 | 0,524 | não medido | baixo |
| `efe-11` | aprendizado | `estado_da_tela_divergente` | `localizador_quebrado` | errado | 0,533 | 0,533 | contagem_inconsistente | baixo |
| `efe-4` | aprendizado | `estado_da_tela_divergente` | `colecao_no_lugar_de_objeto` | errado | 0,568 | 0,567 | tipo_divergente | baixo |
| `tra-12` | aprendizado | `escala_ou_unidade_errada` | `tipo_divergente` | errado | 0,569 | 0,569 | valor_fora_do_dominio | baixo |
| `lex-6` | aprendizado | `corpo_nao_e_json` | `recurso_inexistente` | errado | 0,577 | 0,577 | corpo_nao_e_json | baixo |
| `efe-3` | avaliacao | `campo_ausente` | `campo_ausente` | certo | 0,585 | 0,584 | colecao_no_lugar_de_objeto | baixo |
| `semt-13` | aprendizado | `tipo_divergente` | `tipo_divergente` | certo | 0,598 | 0,598 | formato_de_data_divergente | baixo |
| `tra-7` | aprendizado | `chave_de_juncao_errada` | `campo_renomeado` | errado | 0,600 | 0,549 | estrutura_aninhada_divergente | baixo |
| `semt-7` | aprendizado | `tipo_divergente` | `formato_de_data_divergente` | errado | 0,605 | 0,605 | tipo_divergente | baixo |
| `efe-2` | avaliacao | `estado_da_tela_divergente` | `estado_da_tela_divergente` | certo | 0,643 | 0,642 | valor_fora_do_dominio | baixo |
| `run-10` | avaliacao | `limite_de_requisicoes` | `limite_de_requisicoes` | certo | 0,660 | 0,660 | tempo_de_resposta_excedido | baixo |
| `semt-15` | aprendizado | `valor_fora_do_dominio` | `valor_fora_do_dominio` | certo | 0,665 | 0,665 | formato_de_data_divergente | baixo |
| `sin-12` | aprendizado | `campo_ausente` | `colecao_no_lugar_de_objeto` | errado | 0,679 | 0,677 | resposta_truncada | baixo |
| `semt-14` | avaliacao | `nulo_inesperado` | `nulo_inesperado` | certo | 0,740 | 0,740 | tipo_divergente | baixo |
| `lex-8` | avaliacao | `codificacao_incorreta` | `codificacao_incorreta` | certo | 0,749 | 0,749 | corpo_nao_e_json | baixo |
| `sin-2` | aprendizado | `campo_renomeado` | `tipo_divergente` | errado | 0,751 | 0,751 | campo_ausente | baixo |
| `efe-10` | aprendizado | `estado_da_tela_divergente` | `valor_fora_do_dominio` | errado | 0,751 | 0,749 | tipo_divergente | baixo |
| `sin-5` | avaliacao | `campo_ausente` | `colecao_no_lugar_de_objeto` | errado | 0,758 | 0,753 | campo_ausente | baixo |
| `tra-5` | aprendizado | `escala_ou_unidade_errada` | `contagem_inconsistente` | errado | 0,760 | 0,760 | valor_fora_do_dominio | baixo |
| `lex-2` | aprendizado | `corpo_nao_e_json` | `corpo_nao_e_json` | certo | 0,774 | 0,724 | erro_interno_do_servidor | baixo |
| `semt-1` | avaliacao | `tipo_divergente` | `tipo_divergente` | certo | 0,777 | 0,777 | formato_de_data_divergente | baixo |
| `tra-3` | aprendizado | `chave_de_juncao_errada` | `tipo_divergente` | errado | 0,792 | 0,792 | chave_de_juncao_errada | baixo |
| `semt-8` | avaliacao | `nulo_inesperado` | `nulo_inesperado` | certo | 0,832 | 0,832 | tipo_divergente | baixo |
| `semt-12` | aprendizado | `formato_de_data_divergente` | `formato_de_data_divergente` | certo | 0,841 | 0,841 | tipo_divergente | medio |
| `tra-2` | aprendizado | `chave_de_juncao_errada` | `nome_nulo_vindo_da_view` | errado | 0,851 | 0,826 | campo_ausente | medio |
| `run-13` | avaliacao | `registro_duplicado` | `registro_duplicado` | certo | 0,853 | 0,853 | não medido | medio |
| `efe-6` | aprendizado | `localizador_quebrado` | `localizador_quebrado` | certo | 0,865 | 0,865 | tempo_de_resposta_excedido | medio |
| `tra-8` | avaliacao | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,876 | 0,873 | estrutura_aninhada_divergente | medio |
| `sin-4` | avaliacao | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | 0,880 | 0,880 | tipo_divergente | medio |
| `tra-14` | aprendizado | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,881 | 0,880 | tipo_divergente | medio |
| `run-8` | aprendizado | `recurso_inexistente` | `recurso_inexistente` | certo | 0,930 | 0,930 | não medido | medio |
| `tra-9` | aprendizado | `escala_ou_unidade_errada` | `formato_de_data_divergente` | errado | 0,940 | 0,940 | escala_ou_unidade_errada | medio |
| `run-12` | aprendizado | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | 0,942 | 0,939 | corpo_nao_e_json | medio |
| `semt-2` | aprendizado | `tipo_divergente` | `tipo_divergente` | certo | 0,956 | 0,956 | valor_fora_do_dominio | medio |
| `run-7` | aprendizado | `recurso_inexistente` | `recurso_inexistente` | certo | 0,957 | 0,957 | registro_duplicado | medio |
| `sin-6` | aprendizado | `campo_ausente` | `campo_ausente` | certo | 0,960 | 0,959 | colecao_no_lugar_de_objeto | medio |
| `semt-11` | aprendizado | `valor_fora_do_dominio` | `valor_fora_do_dominio` | certo | 0,966 | 0,966 | estado_da_tela_divergente | medio |
| `sin-9` | aprendizado | `campo_renomeado` | `campo_renomeado` | certo | 0,971 | 0,962 | tipo_divergente | medio |
| `run-11` | aprendizado | `dado_desatualizado` | `valor_fora_do_dominio` | errado | 0,975 | 0,975 | estado_da_tela_divergente | medio |
| `sin-15` | aprendizado | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | 0,980 | 0,980 | estrutura_aninhada_divergente | medio |
| `efe-1` | avaliacao | `localizador_quebrado` | `tempo_de_resposta_excedido` | errado | 0,980 | 0,980 | localizador_quebrado | medio |
| `tra-4` | avaliacao | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,982 | 0,979 | estrutura_aninhada_divergente | medio |
| `run-1` | avaliacao | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | 0,985 | 0,971 | corpo_nao_e_json | medio |
| `tra-11` | avaliacao | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,986 | 0,985 | estrutura_aninhada_divergente | medio |
| `run-6` | aprendizado | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | 0,987 | 0,983 | corpo_nao_e_json | medio |
| `sin-8` | aprendizado | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | 0,989 | 0,988 | estrutura_aninhada_divergente | medio |
| `semt-5` | avaliacao | `nulo_inesperado` | `nulo_inesperado` | certo | 0,989 | 0,989 | campo_ausente | medio |
| `efe-8` | aprendizado | `estado_da_tela_divergente` | `estado_da_tela_divergente` | certo | 0,990 | 0,989 | formato_de_data_divergente | medio |
| `efe-7` | avaliacao | `localizador_quebrado` | `localizador_quebrado` | certo | 0,990 | 0,989 | não medido | medio |
| `lex-12` | aprendizado | `corpo_nao_e_json` | `corpo_nao_e_json` | certo | 0,990 | 0,976 | corpo_vazio | alto |
| `sin-7` | avaliacao | `campo_ausente` | `campo_ausente` | certo | 0,990 | 0,990 | campo_renomeado | alto |
| `lex-13` | aprendizado | `corpo_vazio` | `corpo_vazio` | certo | 0,990 | 0,990 | resposta_truncada | alto |
| `semt-10` | aprendizado | `tipo_divergente` | `tipo_divergente` | certo | 0,991 | 0,991 | campo_ausente | alto |
| `efe-5` | avaliacao | `localizador_quebrado` | `localizador_quebrado` | certo | 0,993 | 0,993 | nulo_inesperado | alto |
| `sin-10` | avaliacao | `campo_renomeado` | `campo_renomeado` | certo | 0,994 | 0,993 | tipo_divergente | alto |
| `semt-3` | avaliacao | `valor_fora_do_dominio` | `valor_fora_do_dominio` | certo | 0,994 | 0,992 | formato_de_data_divergente | alto |
| `tra-13` | aprendizado | `chave_de_juncao_errada` | `chave_de_juncao_errada` | certo | 0,994 | 0,994 | campo_ausente | alto |
| `semt-9` | avaliacao | `valor_fora_do_dominio` | `tipo_divergente` | errado | 0,995 | 0,995 | valor_fora_do_dominio | alto |
| `tra-6` | aprendizado | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | certo | 0,995 | 0,995 | valor_fora_do_dominio | alto |
| `lex-9` | aprendizado | `corpo_nao_e_json` | `corpo_nao_e_json` | certo | 0,996 | 0,971 | corpo_vazio | alto |
| `tra-1` | avaliacao | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | certo | 0,996 | 0,996 | valor_fora_do_dominio | alto |
| `lex-15` | aprendizado | `corpo_nao_e_json` | `corpo_nao_e_json` | certo | 0,997 | 0,979 | erro_interno_do_servidor | alto |
| `efe-13` | aprendizado | `estado_da_tela_divergente` | `dado_desatualizado` | errado | 0,997 | 0,997 | valor_fora_do_dominio | alto |
| `run-4` | avaliacao | `dado_desatualizado` | `dado_desatualizado` | certo | 0,997 | 0,997 | tempo_de_resposta_excedido | alto |
| `run-5` | aprendizado | `registro_duplicado` | `registro_duplicado` | certo | 0,998 | 0,998 | colecao_no_lugar_de_objeto | alto |
| `lex-4` | avaliacao | `codificacao_incorreta` | `codificacao_incorreta` | certo | 0,999 | 0,998 | formato_de_data_divergente | alto |
| `tra-10` | avaliacao | `chave_de_juncao_errada` | `chave_de_juncao_errada` | certo | 0,999 | 0,999 | campo_ausente | alto |
| `efe-9` | aprendizado | `localizador_quebrado` | `localizador_quebrado` | certo | 0,999 | 0,999 | campo_ausente | alto |
| `efe-14` | avaliacao | `localizador_quebrado` | `localizador_quebrado` | certo | 0,999 | 0,999 | nulo_inesperado | alto |
| `efe-15` | aprendizado | `estado_da_tela_divergente` | `estado_da_tela_divergente` | certo | 0,999 | 0,998 | formato_de_data_divergente | alto |
| `run-9` | avaliacao | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | 0,999 | 0,999 | tipo_divergente | alto |
| `sin-13` | aprendizado | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | 0,999 | 0,999 | tipo_divergente | alto |
| `sin-3` | aprendizado | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | 0,999 | 0,999 | campo_ausente | alto |
| `efe-12` | aprendizado | `localizador_quebrado` | `localizador_quebrado` | certo | 0,999 | 0,999 | nulo_inesperado | alto |
| `run-2` | avaliacao | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | 0,999 | 0,999 | limite_de_requisicoes | alto |
| `run-14` | aprendizado | `dado_desatualizado` | `dado_desatualizado` | certo | 0,999 | 0,999 | tempo_de_resposta_excedido | alto |
| `run-15` | aprendizado | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | 0,999 | 0,999 | limite_de_requisicoes | alto |
| `lex-3` | aprendizado | `corpo_vazio` | `tempo_de_resposta_excedido` | errado | 0,999 | 0,999 | resposta_truncada | alto |
| `lex-7` | avaliacao | `corpo_vazio` | `corpo_vazio` | certo | 1,000 | 0,999 | corpo_nao_e_json | alto |
| `lex-11` | avaliacao | `codificacao_incorreta` | `codificacao_incorreta` | certo | 1,000 | 0,999 | corpo_nao_e_json | alto |
| `lex-1` | avaliacao | `resposta_truncada` | `resposta_truncada` | certo | 1,000 | 1,000 | corpo_nao_e_json | alto |
| `semt-4` | aprendizado | `formato_de_data_divergente` | `formato_de_data_divergente` | certo | 1,000 | 1,000 | tipo_divergente | alto |
| `sin-11` | avaliacao | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | 1,000 | 1,000 | campo_ausente | alto |
| `lex-5` | aprendizado | `resposta_truncada` | `resposta_truncada` | certo | 1,000 | 1,000 | corpo_nao_e_json | alto |
| `lex-10` | avaliacao | `resposta_truncada` | `resposta_truncada` | certo | 1,000 | 1,000 | corpo_nao_e_json | alto |
| `lex-14` | aprendizado | `resposta_truncada` | `resposta_truncada` | certo | 1,000 | 1,000 | formato_de_data_divergente | alto |
<!-- /tabela:tb_f4_calibracao_casos -->
