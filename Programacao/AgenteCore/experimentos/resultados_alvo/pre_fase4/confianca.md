<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por analisar_confianca.py a partir de os registros e os arquivos `logprobs__L<n>.jsonl` de `pre_fase4_confianca` (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Sonda de confiança: a probabilidade do rótulo separa acerto de erro?, gerada em 2026-10-06

Medida principal, fixada antes da corrida: probabilidade conjunta dos tokens do rótulo. A coluna de cada sinal traz a AUROC (0,5 é o mesmo que sortear; 1,0 separa tudo) e, entre colchetes, o intervalo de 95% por reamostragem dos casos (2000 réplicas, semente 20261001). A massa das alternativas é limite inferior: só entram as alternativas que o Ollama devolveu em cada posição.

<!-- tabela:tb_conf_resumo -->
| Recorte | Casos | Erros | Probabilidade conjunta do rótulo | Primeiro token do rótulo | 1 menos a massa de outra causa | Causa tratada por verbete do contexto | Causa na classe que a rota aponta | Mediana da conjunta nos certos | Mediana nos errados | Erros com a causa certa como segunda opção |
|---|---|---|---|---|---|---|---|---|---|---|
| todas as versões | 216 | 46 | 0,783 [0,684 a 0,882] | 0,765 [0,665 a 0,861] | 0,820 [0,691 a 0,915] | 0,541 [0,464 a 0,626] | 0,626 [0,503 a 0,751] | 0,992 | 0,846 | 25 de 46 |
| qwen2.5:7b, L0 | 72 | 19 | 0,814 [0,709 a 0,908] | 0,795 [0,687 a 0,892] | 0,834 [0,708 a 0,930] | 0,551 [0,468 a 0,643] | 0,681 [0,550 a 0,800] | 0,989 | 0,686 | 13 de 19 |
| qwen2.5:7b, L1 | 72 | 13 | 0,770 [0,637 a 0,893] | 0,748 [0,616 a 0,870] | 0,825 [0,671 a 0,939] | 0,496 [0,429 a 0,583] | 0,570 [0,423 a 0,727] | 0,996 | 0,883 | 6 de 13 |
| qwen2.5:7b, L1 curada | 72 | 14 | 0,752 [0,610 a 0,876] | 0,738 [0,596 a 0,862] | 0,791 [0,643 a 0,908] | 0,573 [0,464 a 0,695] | 0,613 [0,464 a 0,754] | 0,991 | 0,843 | 6 de 14 |
<!-- /tabela:tb_conf_resumo -->

Se o agente mandar para revisão humana a parcela de menor probabilidade conjunta: quantos erros ela pega, quantos acertos são revisados à toa e o risco no que sobra.

<!-- tabela:tb_conf_revisao -->
| Recorte | Parcela revisada | Casos revisados | Erros pegos | Acertos revisados à toa | Risco no que sobra |
|---|---|---|---|---|---|
| todas as versões | 10% | 22 | 14 de 46 | 8 | 16,5% |
| todas as versões | 20% | 43 | 18 de 46 | 25 | 16,2% |
| todas as versões | 30% | 65 | 26 de 46 | 39 | 13,2% |
| qwen2.5:7b, L0 | 10% | 7 | 6 de 19 | 1 | 20,0% |
| qwen2.5:7b, L0 | 20% | 14 | 8 de 19 | 6 | 19,0% |
| qwen2.5:7b, L0 | 30% | 22 | 11 de 19 | 11 | 16,0% |
| qwen2.5:7b, L1 | 10% | 7 | 4 de 13 | 3 | 13,9% |
| qwen2.5:7b, L1 | 20% | 14 | 5 de 13 | 9 | 13,8% |
| qwen2.5:7b, L1 | 30% | 22 | 8 de 13 | 14 | 10,0% |
| qwen2.5:7b, L1 curada | 10% | 7 | 4 de 14 | 3 | 15,4% |
| qwen2.5:7b, L1 curada | 20% | 14 | 4 de 14 | 10 | 17,2% |
| qwen2.5:7b, L1 curada | 30% | 22 | 7 de 14 | 15 | 14,0% |
<!-- /tabela:tb_conf_revisao -->

Acerto de cada biblioteca na mesma corrida (mesma versão do Ollama, mesmo dia, mesma máquina), nos 36 oficiais de avaliação, nos 36 inéditos e nos 72:

<!-- tabela:tb_conf_acerto -->
| Modelo | Biblioteca | Conjunto | Casos | Acertos | Acerto | s por diagnóstico (mediana) | Tokens do prompt (mediana) |
|---|---|---|---|---|---|---|---|
| `qwen2.5:7b` | L0 | oficiais | 36 | 28 | 77,8% | 69,2 | 1044 |
| `qwen2.5:7b` | L0 | ineditos | 36 | 25 | 69,4% | 69,7 | 1084 |
| `qwen2.5:7b` | L0 | todos | 72 | 53 | 73,6% | 69,2 | 1056 |
| `qwen2.5:7b` | L1 | oficiais | 36 | 33 | 91,7% | 75,0 | 1295 |
| `qwen2.5:7b` | L1 | ineditos | 36 | 26 | 72,2% | 67,6 | 1330 |
| `qwen2.5:7b` | L1 | todos | 72 | 59 | 81,9% | 70,5 | 1315 |
| `qwen2.5:7b` | L1 curada | oficiais | 36 | 31 | 86,1% | 61,0 | 1116 |
| `qwen2.5:7b` | L1 curada | ineditos | 36 | 27 | 75,0% | 61,1 | 1150 |
| `qwen2.5:7b` | L1 curada | todos | 72 | 58 | 80,6% | 61,1 | 1132 |
<!-- /tabela:tb_conf_acerto -->

Pares caso a caso: entre as bibliotecas da mesma corrida (b = casos que só a primeira acertou; c = só a segunda) e, para as versões que já tinham corrida nos mesmos casos, contra a corrida anterior (os casos de texto corrigido em 28/09 ficam fora da conta contra a Fase 3):

<!-- tabela:tb_conf_pares -->
| Comparação | Conjunto | Casos | Acerto da primeira | Acerto da segunda | b | c | Diferença | p (McNemar exato) | Rótulos diferentes | Casos que mudaram |
|---|---|---|---|---|---|---|---|---|---|---|
| L1 contra L0 | oficiais | 36 | 91,7% | 77,8% | 5 | 0 | +13,9 pp | 0,0625 | 7 | `efe-1`, `efe-3`, `run-10`, `sin-14`, `tra-8` |
| L1 contra L0 | ineditos | 36 | 72,2% | 69,4% | 1 | 0 | +2,8 pp | 1,0000 | 4 | `run-21` |
| L1 contra L0 | todos | 72 | 81,9% | 73,6% | 6 | 0 | +8,3 pp | 0,0312 | 11 | `efe-1`, `efe-3`, `run-10`, `run-21`, `sin-14`, `tra-8` |
| L1 curada contra L0 | oficiais | 36 | 86,1% | 77,8% | 3 | 0 | +8,3 pp | 0,2500 | 4 | `efe-3`, `run-10`, `tra-8` |
| L1 curada contra L0 | ineditos | 36 | 75,0% | 69,4% | 2 | 0 | +5,6 pp | 0,5000 | 5 | `run-21`, `semt-20` |
| L1 curada contra L0 | todos | 72 | 80,6% | 73,6% | 5 | 0 | +6,9 pp | 0,0625 | 9 | `efe-3`, `run-10`, `run-21`, `semt-20`, `tra-8` |
| L1 curada contra L1 | oficiais | 36 | 86,1% | 91,7% | 0 | 2 | -5,6 pp | 0,5000 | 4 | `efe-1`, `sin-14` |
| L1 curada contra L1 | ineditos | 36 | 75,0% | 72,2% | 1 | 0 | +2,8 pp | 1,0000 | 1 | `semt-20` |
| L1 curada contra L1 | todos | 72 | 80,6% | 81,9% | 1 | 2 | -1,4 pp | 1,0000 | 5 | `semt-20`, `efe-1`, `sin-14` |
| L0 contra a corrida `fase3` (mesmos casos) | oficiais | 35 | 80,0% | 80,0% | 0 | 0 | 0,0 pp | 1,0000 | 2 | nenhum |
| L0 contra a corrida `fase3b_ineditos` (mesmos casos) | ineditos | 36 | 69,4% | 75,0% | 0 | 2 | -5,6 pp | 0,5000 | 2 | `run-21`, `semt-20` |
| L1 contra a corrida `fase3` (mesmos casos) | oficiais | 35 | 91,4% | 91,4% | 0 | 0 | 0,0 pp | 1,0000 | 0 | nenhum |
| L1 contra a corrida `fase3b_ineditos` (mesmos casos) | ineditos | 36 | 72,2% | 72,2% | 0 | 0 | 0,0 pp | 1,0000 | 1 | nenhum |
<!-- /tabela:tb_conf_pares -->

Caso a caso, da menor probabilidade conjunta para a maior:

<!-- tabela:tb_conf_casos -->
| Caso | Biblioteca | Conjunto | Resultado | Causa respondida | Probabilidade conjunta | Primeiro token | Massa de outra causa | Segunda opção | Tratada por verbete do contexto | Na classe da rota |
|---|---|---|---|---|---|---|---|---|---|---|
| `sin-14` | L1 curada | oficiais | errado | `imagem_url_nao_esperado` | 0,021 | 0,232 | 0,756 | colecao_no_lugar_de_objeto (0,183) | não | não |
| `lex-18` | L1 | ineditos | errado | `campo_renomeado` | 0,214 | 0,232 | 0,776 | codificacao_incorreta (0,252) | sim | não |
| `sin-14` | L1 | oficiais | certo | `campo_renomeado` | 0,261 | 0,364 | 0,685 | formato_de_data_divergente (0,268) | sim | sim |
| `sin-14` | L0 | oficiais | errado | `colecao_no_lugar_de_objeto` | 0,275 | 0,276 | 0,619 | campo_ausente ou campo_renomeado (0,239) | sim | sim |
| `tra-15` | L0 | oficiais | errado | `tipo_divergente` | 0,306 | 0,306 | 0,691 | contagem_inconsistente (0,285) | não | não |
| `tra-15` | L1 curada | oficiais | errado | `tipo_divergente` | 0,306 | 0,306 | 0,691 | contagem_inconsistente (0,285) | não | não |
| `tra-10` | L0 | oficiais | certo | `chave_de_juncao_errada` | 0,394 | 0,395 | 0,591 | valor_fora_do_dominio (0,377) | sim | não |
| `tra-15` | L1 | oficiais | errado | `valor_fora_do_dominio` | 0,420 | 0,420 | 0,577 | tipo_divergente (0,309) | sim | não |
| `lex-18` | L1 curada | ineditos | errado | `campo_renomeado` | 0,451 | 0,459 | 0,540 | valor_fora_do_dominio (0,331) | sim | não |
| `semt-8` | L1 curada | oficiais | certo | `nulo_inesperado` | 0,454 | 0,454 | 0,526 | tipo_divergente (0,302) | sim | sim |
| `semt-20` | L0 | ineditos | errado | `tipo_divergente` | 0,461 | 0,461 | 0,537 | valor_fora_do_dominio (0,532) | sim | sim |
| `semt-21` | L1 curada | ineditos | errado | `campo_ausente` | 0,484 | 0,920 | 0,126 | campo_renomeado (0,050) | sim | não |
| `run-21` | L0 | ineditos | errado | `colecao_no_lugar_de_objeto` | 0,487 | 0,488 | 0,501 | registro_duplicado (0,491) | sim | não |
| `semt-21` | L1 | ineditos | errado | `campo_ausente` | 0,503 | 0,984 | 0,433 | campo_renomeado (0,419) | sim | não |
| `semt-21` | L0 | ineditos | errado | `campo_ausente` | 0,506 | 0,960 | 0,301 | campo_renomeado (0,263) | sim | não |
| `tra-17` | L0 | ineditos | errado | `estrutura_aninhada_divergente` | 0,522 | 0,522 | 0,470 | campo_ausente ou campo_renomeado (0,352) | sim | sim |
| `semt-20` | L1 curada | ineditos | certo | `valor_fora_do_dominio` | 0,525 | 0,525 | 0,473 | tipo_divergente (0,462) | sim | sim |
| `efe-3` | L1 curada | oficiais | certo | `campo_ausente` | 0,533 | 0,534 | 0,458 | colecao_no_lugar_de_objeto (0,259) | sim | sim |
| `tra-4` | L0 | oficiais | certo | `contagem_inconsistente` | 0,540 | 0,541 | 0,458 | estrutura_aninhada_divergente (0,456) | sim | não |
| `efe-3` | L0 | oficiais | errado | `colecao_no_lugar_de_objeto` | 0,546 | 0,547 | 0,448 | campo_ausente ou campo_renomeado (0,344) | sim | sim |
| `tra-19` | L0 | ineditos | certo | `escala_ou_unidade_errada` | 0,546 | 0,546 | 0,453 | valor_fora_do_dominio (0,380) | sim | não |
| `sin-4` | L0 | oficiais | certo | `colecao_no_lugar_de_objeto` | 0,550 | 0,551 | 0,412 | campo_ausente ou campo_renomeado (0,212) | sim | sim |
| `efe-3` | L1 | oficiais | certo | `campo_ausente` | 0,554 | 0,554 | 0,439 | tipo_divergente (0,356) | sim | sim |
| `run-10` | L0 | oficiais | errado | `[limite_de_requisicoes]` | 0,559 | 0,590 | 0,410 | limite_de_requisicoes (0,410) | não | não |
| `run-10` | L1 | oficiais | certo | `limite_de_requisicoes` | 0,579 | 0,579 | 0,000 | tempo_de_resposta_excedido (0,000) | sim | sim |
| `tra-19` | L1 curada | ineditos | certo | `escala_ou_unidade_errada` | 0,600 | 0,600 | 0,398 | valor_fora_do_dominio (0,152) | sim | não |
| `run-18` | L0 | ineditos | certo | `limite_de_requisicoes` | 0,603 | 0,603 | 0,000 | tempo_de_resposta_excedido (0,000) | sim | sim |
| `semt-20` | L1 | ineditos | errado | `tipo_divergente` | 0,616 | 0,616 | 0,382 | valor_fora_do_dominio (0,371) | sim | sim |
| `semt-14` | L0 | oficiais | certo | `nulo_inesperado` | 0,622 | 0,622 | 0,378 | tipo_divergente (0,364) | sim | sim |
| `tra-18` | L0 | ineditos | certo | `contagem_inconsistente` | 0,626 | 0,626 | 0,369 | registro_duplicado (0,347) | não | não |
| `tra-18` | L1 curada | ineditos | certo | `contagem_inconsistente` | 0,626 | 0,626 | 0,369 | registro_duplicado (0,347) | não | não |
| `efe-1` | L1 | oficiais | certo | `localizador_quebrado` | 0,631 | 0,631 | 0,356 | tempo_de_resposta_excedido (0,355) | sim | sim |
| `run-18` | L1 | ineditos | certo | `limite_de_requisicoes` | 0,633 | 0,633 | 0,000 | tempo_de_resposta_excedido (0,000) | sim | sim |
| `run-18` | L1 curada | ineditos | certo | `limite_de_requisicoes` | 0,633 | 0,633 | 0,000 | tempo_de_resposta_excedido (0,000) | sim | sim |
| `efe-2` | L0 | oficiais | certo | `estado_da_tela_divergente` | 0,639 | 0,639 | 0,353 | valor_fora_do_dominio (0,338) | sim | não |
| `efe-16` | L0 | ineditos | errado | `tempo_de_resposta_excedido` | 0,645 | 0,645 | 0,346 | localizador_quebrado (0,341) | sim | não |
| `run-21` | L1 curada | ineditos | certo | `registro_duplicado` | 0,649 | 0,649 | 0,338 | colecao_no_lugar_de_objeto (0,320) | não | não |
| `semt-8` | L1 | oficiais | certo | `nulo_inesperado` | 0,652 | 0,652 | 0,342 | tipo_divergente (0,260) | sim | sim |
| `run-10` | L1 curada | oficiais | certo | `limite_de_requisicoes` | 0,659 | 0,659 | 0,000 | nenhuma | sim | sim |
| `tra-8` | L1 | oficiais | certo | `contagem_inconsistente` | 0,665 | 0,666 | 0,330 | estrutura_aninhada_divergente (0,315) | sim | não |
| `efe-2` | L1 curada | oficiais | certo | `estado_da_tela_divergente` | 0,682 | 0,682 | 0,310 | valor_fora_do_dominio (0,298) | sim | não |
| `tra-8` | L0 | oficiais | errado | `estrutura_aninhada_divergente` | 0,686 | 0,686 | 0,270 | contagem_inconsistente (0,266) | sim | não |
| `semt-14` | L1 curada | oficiais | certo | `nulo_inesperado` | 0,698 | 0,698 | 0,302 | tipo_divergente (0,292) | sim | sim |
| `lex-8` | L1 curada | oficiais | certo | `codificacao_incorreta` | 0,709 | 0,709 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `run-16` | L1 | ineditos | certo | `recurso_inexistente` | 0,727 | 0,727 | 0,018 | registro_duplicado (0,013) | sim | sim |
| `sin-5` | L1 curada | oficiais | errado | `colecao_no_lugar_de_objeto` | 0,744 | 0,750 | 0,245 | campo_ausente ou campo_renomeado (0,132) | sim | sim |
| `efe-16` | L1 | ineditos | errado | `tempo_de_resposta_excedido` | 0,757 | 0,757 | 0,240 | localizador_quebrado (0,235) | sim | não |
| `efe-16` | L1 curada | ineditos | errado | `tempo_de_resposta_excedido` | 0,757 | 0,757 | 0,240 | localizador_quebrado (0,235) | sim | não |
| `lex-8` | L0 | oficiais | certo | `codificacao_incorreta` | 0,763 | 0,763 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `run-16` | L1 curada | ineditos | certo | `recurso_inexistente` | 0,764 | 0,764 | 0,017 | registro_duplicado (0,013) | sim | sim |
| `sin-4` | L1 curada | oficiais | certo | `colecao_no_lugar_de_objeto` | 0,786 | 0,787 | 0,202 | campo_ausente ou campo_renomeado (0,055) | sim | sim |
| `tra-18` | L1 | ineditos | certo | `contagem_inconsistente` | 0,796 | 0,796 | 0,201 | registro_duplicado (0,167) | não | não |
| `semt-1` | L1 curada | oficiais | certo | `tipo_divergente` | 0,821 | 0,821 | 0,175 | formato_de_data_divergente (0,141) | sim | sim |
| `efe-20` | L1 curada | ineditos | errado | `corpo_vazio` | 0,832 | 0,832 | 0,149 | contagem_inconsistente (0,128) | sim | sim |
| `lex-18` | L0 | ineditos | errado | `tipo_divergente` | 0,837 | 0,837 | 0,160 | codificacao_incorreta (0,070) | sim | não |
| `lex-8` | L1 | oficiais | certo | `codificacao_incorreta` | 0,842 | 0,842 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `run-13` | L0 | oficiais | certo | `registro_duplicado` | 0,846 | 0,846 | 0,000 | nenhuma | sim | não |
| `semt-14` | L1 | oficiais | certo | `nulo_inesperado` | 0,847 | 0,847 | 0,152 | tipo_divergente (0,144) | sim | sim |
| `run-13` | L1 | oficiais | certo | `registro_duplicado` | 0,851 | 0,851 | 0,000 | nenhuma | sim | não |
| `run-13` | L1 curada | oficiais | certo | `registro_duplicado` | 0,851 | 0,851 | 0,000 | nenhuma | sim | não |
| `run-16` | L0 | ineditos | certo | `recurso_inexistente` | 0,853 | 0,853 | 0,033 | registro_duplicado (0,030) | sim | sim |
| `lex-19` | L1 curada | ineditos | errado | `erro_interno_do_servidor` | 0,855 | 0,874 | 0,124 | corpo_nao_e_json ou corpo_vazio (0,124) | sim | não |
| `efe-20` | L1 | ineditos | errado | `corpo_vazio` | 0,856 | 0,856 | 0,127 | contagem_inconsistente (0,108) | sim | sim |
| `semt-8` | L0 | oficiais | certo | `nulo_inesperado` | 0,866 | 0,866 | 0,109 | valor_fora_do_dominio (0,085) | sim | sim |
| `lex-19` | L1 | ineditos | errado | `erro_interno_do_servidor` | 0,883 | 0,905 | 0,093 | corpo_nao_e_json ou corpo_vazio (0,093) | sim | não |
| `sin-5` | L0 | oficiais | errado | `colecao_no_lugar_de_objeto` | 0,903 | 0,906 | 0,092 | campo_ausente ou campo_renomeado (0,049) | sim | sim |
| `sin-7` | L1 | oficiais | certo | `campo_ausente` | 0,908 | 0,909 | 0,002 | nulo_inesperado (0,001) | sim | sim |
| `tra-16` | L1 | ineditos | errado | `contagem_inconsistente` | 0,909 | 0,909 | 0,088 | valor_fora_do_dominio (0,055) | não | sim |
| `tra-19` | L1 | ineditos | certo | `escala_ou_unidade_errada` | 0,910 | 0,910 | 0,089 | valor_fora_do_dominio (0,043) | sim | não |
| `run-21` | L1 | ineditos | certo | `registro_duplicado` | 0,912 | 0,912 | 0,078 | colecao_no_lugar_de_objeto (0,056) | não | não |
| `semt-17` | L1 curada | ineditos | certo | `nulo_inesperado` | 0,915 | 0,915 | 0,084 | colecao_no_lugar_de_objeto (0,046) | sim | sim |
| `semt-1` | L1 | oficiais | certo | `tipo_divergente` | 0,916 | 0,916 | 0,081 | formato_de_data_divergente (0,060) | sim | sim |
| `efe-19` | L1 curada | ineditos | errado | `localizador_quebrado` | 0,923 | 0,923 | 0,063 | resposta_truncada (0,019) | sim | não |
| `semt-16` | L1 curada | ineditos | certo | `tipo_divergente` | 0,923 | 0,923 | 0,076 | chave_de_juncao_errada (0,070) | sim | sim |
| `efe-20` | L0 | ineditos | errado | `contagem_inconsistente` | 0,929 | 0,931 | 0,068 | estado_da_tela_divergente (0,067) | sim | não |
| `efe-19` | L1 | ineditos | errado | `localizador_quebrado` | 0,932 | 0,933 | 0,056 | campo_ausente ou campo_renomeado (0,015) | sim | não |
| `tra-16` | L0 | ineditos | errado | `contagem_inconsistente` | 0,937 | 0,937 | 0,060 | valor_fora_do_dominio (0,021) | não | sim |
| `tra-16` | L1 curada | ineditos | errado | `contagem_inconsistente` | 0,937 | 0,937 | 0,060 | valor_fora_do_dominio (0,021) | não | sim |
| `semt-1` | L0 | oficiais | certo | `tipo_divergente` | 0,946 | 0,946 | 0,051 | valor_fora_do_dominio (0,029) | sim | sim |
| `efe-7` | L0 | oficiais | certo | `localizador_quebrado` | 0,949 | 0,950 | 0,000 | nenhuma | sim | sim |
| `tra-21` | L1 | ineditos | certo | `contagem_inconsistente` | 0,958 | 0,961 | 0,000 | resposta_truncada (0,000) | sim | sim |
| `efe-7` | L1 | oficiais | certo | `localizador_quebrado` | 0,960 | 0,960 | 0,000 | nenhuma | sim | sim |
| `tra-8` | L1 curada | oficiais | certo | `contagem_inconsistente` | 0,960 | 0,962 | 0,018 | estrutura_aninhada_divergente (0,014) | sim | não |
| `run-17` | L1 | ineditos | certo | `erro_interno_do_servidor` | 0,960 | 0,961 | 0,000 | tipo_divergente (0,000) | sim | sim |
| `run-17` | L1 curada | ineditos | certo | `erro_interno_do_servidor` | 0,960 | 0,961 | 0,000 | tipo_divergente (0,000) | sim | sim |
| `lex-19` | L0 | ineditos | errado | `erro_interno_do_servidor` | 0,961 | 0,982 | 0,017 | corpo_nao_e_json ou corpo_vazio (0,017) | sim | não |
| `tra-1` | L0 | oficiais | certo | `escala_ou_unidade_errada` | 0,962 | 0,962 | 0,023 | valor_fora_do_dominio (0,021) | sim | sim |
| `tra-11` | L0 | oficiais | certo | `contagem_inconsistente` | 0,962 | 0,963 | 0,000 | estrutura_aninhada_divergente (0,000) | sim | não |
| `semt-16` | L0 | ineditos | certo | `tipo_divergente` | 0,962 | 0,962 | 0,037 | chave_de_juncao_errada (0,030) | sim | sim |
| `run-17` | L0 | ineditos | certo | `erro_interno_do_servidor` | 0,963 | 0,964 | 0,000 | tipo_divergente (0,000) | sim | sim |
| `run-1` | L1 | oficiais | certo | `erro_interno_do_servidor` | 0,963 | 0,980 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | não |
| `run-1` | L1 curada | oficiais | certo | `erro_interno_do_servidor` | 0,963 | 0,980 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | não |
| `tra-17` | L1 | ineditos | errado | `tipo_divergente` | 0,964 | 0,964 | 0,035 | campo_ausente ou campo_renomeado (0,032) | sim | sim |
| `efe-1` | L0 | oficiais | errado | `tempo_de_resposta_excedido` | 0,965 | 0,965 | 0,021 | localizador_quebrado (0,021) | sim | não |
| `sin-7` | L0 | oficiais | certo | `campo_ausente` | 0,966 | 0,967 | 0,001 | campo_renomeado (0,001) | sim | sim |
| `tra-17` | L1 curada | ineditos | errado | `tipo_divergente` | 0,968 | 0,968 | 0,030 | chave_de_juncao_errada (0,019) | sim | sim |
| `sin-5` | L1 | oficiais | errado | `tipo_divergente` | 0,969 | 0,969 | 0,030 | campo_ausente ou campo_renomeado (0,015) | sim | sim |
| `semt-17` | L1 | ineditos | certo | `nulo_inesperado` | 0,969 | 0,969 | 0,031 | campo_ausente ou campo_renomeado (0,023) | sim | sim |
| `sin-18` | L1 curada | ineditos | certo | `estrutura_aninhada_divergente` | 0,969 | 0,969 | 0,030 | tipo_divergente (0,021) | sim | não |
| `tra-21` | L1 curada | ineditos | certo | `contagem_inconsistente` | 0,971 | 0,975 | 0,000 | colecao_no_lugar_de_objeto (0,000) | sim | sim |
| `run-1` | L0 | oficiais | certo | `erro_interno_do_servidor` | 0,973 | 0,983 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `tra-4` | L1 | oficiais | certo | `contagem_inconsistente` | 0,975 | 0,977 | 0,022 | estrutura_aninhada_divergente (0,021) | sim | não |
| `tra-4` | L1 curada | oficiais | certo | `contagem_inconsistente` | 0,976 | 0,979 | 0,007 | estrutura_aninhada_divergente (0,007) | sim | não |
| `tra-21` | L0 | ineditos | certo | `contagem_inconsistente` | 0,977 | 0,980 | 0,000 | colecao_no_lugar_de_objeto (0,000) | sim | sim |
| `sin-18` | L0 | ineditos | certo | `estrutura_aninhada_divergente` | 0,981 | 0,981 | 0,019 | tipo_divergente (0,017) | sim | não |
| `semt-9` | L0 | oficiais | errado | `tipo_divergente` | 0,983 | 0,983 | 0,016 | valor_fora_do_dominio (0,015) | sim | sim |
| `tra-11` | L1 | oficiais | certo | `contagem_inconsistente` | 0,983 | 0,986 | 0,000 | estrutura_aninhada_divergente (0,000) | sim | não |
| `sin-16` | L0 | ineditos | certo | `campo_ausente` | 0,984 | 0,984 | 0,000 | campo_renomeado (0,000) | sim | sim |
| `efe-1` | L1 curada | oficiais | errado | `tempo_de_resposta_excedido` | 0,985 | 0,985 | 0,011 | localizador_quebrado (0,011) | sim | não |
| `tra-11` | L1 curada | oficiais | certo | `contagem_inconsistente` | 0,985 | 0,986 | 0,000 | estrutura_aninhada_divergente (0,000) | sim | não |
| `semt-5` | L1 | oficiais | certo | `nulo_inesperado` | 0,985 | 0,985 | 0,009 | campo_ausente ou campo_renomeado (0,008) | sim | sim |
| `semt-5` | L1 curada | oficiais | certo | `nulo_inesperado` | 0,985 | 0,985 | 0,009 | campo_ausente ou campo_renomeado (0,008) | sim | sim |
| `sin-4` | L1 | oficiais | certo | `colecao_no_lugar_de_objeto` | 0,987 | 0,987 | 0,011 | tipo_divergente (0,006) | sim | sim |
| `lex-21` | L0 | ineditos | certo | `codificacao_incorreta` | 0,987 | 0,988 | 0,012 | campo_ausente ou campo_renomeado (0,011) | não | não |
| `lex-21` | L1 curada | ineditos | certo | `codificacao_incorreta` | 0,987 | 0,988 | 0,012 | campo_ausente ou campo_renomeado (0,011) | não | não |
| `efe-7` | L1 curada | oficiais | certo | `localizador_quebrado` | 0,988 | 0,988 | 0,000 | nenhuma | sim | sim |
| `sin-20` | L0 | ineditos | certo | `campo_ausente` | 0,988 | 0,988 | 0,010 | colecao_no_lugar_de_objeto (0,007) | sim | sim |
| `semt-17` | L0 | ineditos | certo | `nulo_inesperado` | 0,989 | 0,989 | 0,011 | campo_ausente ou campo_renomeado (0,005) | sim | sim |
| `semt-5` | L0 | oficiais | certo | `nulo_inesperado` | 0,989 | 0,989 | 0,006 | campo_ausente ou campo_renomeado (0,005) | sim | sim |
| `sin-10` | L1 curada | oficiais | certo | `campo_renomeado` | 0,990 | 0,991 | 0,001 | tipo_divergente (0,000) | sim | sim |
| `sin-7` | L1 curada | oficiais | certo | `campo_ausente` | 0,991 | 0,991 | 0,000 | campo_renomeado (0,000) | sim | sim |
| `efe-5` | L1 | oficiais | certo | `localizador_quebrado` | 0,991 | 0,991 | 0,000 | nulo_inesperado (0,000) | sim | sim |
| `efe-5` | L1 curada | oficiais | certo | `localizador_quebrado` | 0,991 | 0,991 | 0,000 | nulo_inesperado (0,000) | sim | sim |
| `efe-19` | L0 | ineditos | errado | `localizador_quebrado` | 0,991 | 0,992 | 0,007 | resposta_truncada (0,003) | sim | não |
| `semt-3` | L1 | oficiais | certo | `valor_fora_do_dominio` | 0,991 | 0,992 | 0,007 | tipo_divergente (0,003) | sim | sim |
| `semt-3` | L1 curada | oficiais | certo | `valor_fora_do_dominio` | 0,992 | 0,994 | 0,005 | formato_de_data_divergente (0,002) | sim | não |
| `sin-18` | L1 | ineditos | certo | `estrutura_aninhada_divergente` | 0,992 | 0,992 | 0,008 | tipo_divergente (0,006) | sim | não |
| `sin-10` | L0 | oficiais | certo | `campo_renomeado` | 0,992 | 0,993 | 0,000 | tipo_divergente (0,000) | sim | sim |
| `sin-10` | L1 | oficiais | certo | `campo_renomeado` | 0,993 | 0,994 | 0,002 | tipo_divergente (0,002) | sim | sim |
| `semt-9` | L1 curada | oficiais | errado | `tipo_divergente` | 0,993 | 0,993 | 0,005 | valor_fora_do_dominio (0,005) | sim | sim |
| `tra-1` | L1 curada | oficiais | certo | `escala_ou_unidade_errada` | 0,993 | 0,994 | 0,005 | valor_fora_do_dominio (0,005) | sim | sim |
| `sin-19` | L1 curada | ineditos | certo | `colecao_no_lugar_de_objeto` | 0,994 | 0,996 | 0,003 | estrutura_aninhada_divergente (0,003) | sim | sim |
| `run-4` | L0 | oficiais | certo | `dado_desatualizado` | 0,995 | 0,995 | 0,003 | tempo_de_resposta_excedido (0,002) | sim | sim |
| `run-4` | L1 curada | oficiais | certo | `dado_desatualizado` | 0,995 | 0,995 | 0,003 | tempo_de_resposta_excedido (0,002) | sim | sim |
| `efe-5` | L0 | oficiais | certo | `localizador_quebrado` | 0,995 | 0,995 | 0,000 | nulo_inesperado (0,000) | sim | sim |
| `semt-3` | L0 | oficiais | certo | `valor_fora_do_dominio` | 0,995 | 0,995 | 0,003 | estado_da_tela_divergente (0,001) | sim | sim |
| `sin-20` | L1 curada | ineditos | certo | `campo_ausente` | 0,995 | 0,996 | 0,003 | corpo_nao_e_json ou corpo_vazio (0,001) | sim | sim |
| `sin-17` | L0 | ineditos | certo | `campo_renomeado` | 0,996 | 0,998 | 0,000 | campo_ausente (0,000) | sim | não |
| `efe-14` | L1 | oficiais | certo | `localizador_quebrado` | 0,996 | 0,996 | 0,000 | nulo_inesperado (0,000) | sim | sim |
| `efe-14` | L1 curada | oficiais | certo | `localizador_quebrado` | 0,996 | 0,996 | 0,000 | nulo_inesperado (0,000) | sim | sim |
| `tra-1` | L1 | oficiais | certo | `escala_ou_unidade_errada` | 0,996 | 0,996 | 0,002 | valor_fora_do_dominio (0,001) | sim | sim |
| `sin-16` | L1 curada | ineditos | certo | `campo_ausente` | 0,996 | 0,996 | 0,000 | campo_renomeado (0,000) | sim | sim |
| `sin-20` | L1 | ineditos | certo | `campo_ausente` | 0,996 | 0,996 | 0,002 | resposta_truncada (0,001) | sim | sim |
| `sin-19` | L0 | ineditos | certo | `colecao_no_lugar_de_objeto` | 0,996 | 0,998 | 0,001 | estrutura_aninhada_divergente (0,001) | sim | sim |
| `sin-21` | L0 | ineditos | certo | `estrutura_aninhada_divergente` | 0,996 | 0,996 | 0,000 | tipo_divergente (0,000) | sim | não |
| `efe-14` | L0 | oficiais | certo | `localizador_quebrado` | 0,997 | 0,997 | 0,000 | estrutura_aninhada_divergente (0,000) | sim | sim |
| `run-20` | L1 curada | ineditos | certo | `dado_desatualizado` | 0,997 | 0,997 | 0,000 | valor_fora_do_dominio (0,000) | sim | sim |
| `sin-16` | L1 | ineditos | certo | `campo_ausente` | 0,997 | 0,997 | 0,000 | campo_renomeado (0,000) | sim | sim |
| `semt-16` | L1 | ineditos | certo | `tipo_divergente` | 0,997 | 0,997 | 0,003 | campo_ausente ou campo_renomeado (0,002) | sim | sim |
| `sin-17` | L1 | ineditos | certo | `campo_renomeado` | 0,997 | 1,000 | 0,001 | campo_ausente (0,001) | sim | não |
| `semt-9` | L1 | oficiais | errado | `tipo_divergente` | 0,997 | 0,997 | 0,002 | valor_fora_do_dominio (0,002) | sim | sim |
| `sin-17` | L1 curada | ineditos | certo | `campo_renomeado` | 0,997 | 1,000 | 0,000 | campo_ausente (0,000) | sim | não |
| `efe-21` | L1 | ineditos | errado | `nulo_inesperado` | 0,997 | 0,997 | 0,000 | tipo_divergente (0,000) | sim | sim |
| `tra-20` | L1 curada | ineditos | certo | `chave_de_juncao_errada` | 0,998 | 0,998 | 0,001 | campo_ausente ou campo_renomeado (0,001) | sim | sim |
| `tra-10` | L1 | oficiais | certo | `chave_de_juncao_errada` | 0,998 | 0,998 | 0,001 | campo_ausente ou campo_renomeado (0,001) | sim | não |
| `efe-21` | L0 | ineditos | errado | `nulo_inesperado` | 0,998 | 0,998 | 0,000 | tipo_divergente (0,000) | sim | não |
| `tra-10` | L1 curada | oficiais | certo | `chave_de_juncao_errada` | 0,998 | 0,998 | 0,001 | campo_ausente ou campo_renomeado (0,001) | sim | não |
| `run-20` | L0 | ineditos | certo | `dado_desatualizado` | 0,998 | 0,998 | 0,000 | valor_fora_do_dominio (0,000) | sim | sim |
| `lex-4` | L0 | oficiais | certo | `codificacao_incorreta` | 0,998 | 0,998 | 0,001 | tipo_divergente (0,001) | não | não |
| `sin-19` | L1 | ineditos | certo | `colecao_no_lugar_de_objeto` | 0,998 | 0,999 | 0,000 | estrutura_aninhada_divergente (0,000) | sim | sim |
| `efe-18` | L1 | ineditos | certo | `localizador_quebrado` | 0,998 | 0,999 | 0,000 | campo_ausente ou campo_renomeado (0,000) | sim | sim |
| `efe-18` | L1 curada | ineditos | certo | `localizador_quebrado` | 0,998 | 0,999 | 0,000 | campo_ausente ou campo_renomeado (0,000) | sim | sim |
| `run-9` | L1 | oficiais | certo | `tempo_de_resposta_excedido` | 0,998 | 0,998 | 0,001 | tipo_divergente (0,001) | não | não |
| `efe-21` | L1 curada | ineditos | errado | `nulo_inesperado` | 0,998 | 0,999 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `tra-20` | L0 | ineditos | certo | `chave_de_juncao_errada` | 0,999 | 0,999 | 0,000 | campo_ausente ou campo_renomeado (0,000) | sim | sim |
| `lex-4` | L1 curada | oficiais | certo | `codificacao_incorreta` | 0,999 | 0,999 | 0,001 | formato_de_data_divergente (0,001) | não | não |
| `efe-17` | L0 | ineditos | certo | `localizador_quebrado` | 0,999 | 0,999 | 0,000 | estrutura_aninhada_divergente (0,000) | sim | sim |
| `efe-2` | L1 | oficiais | certo | `estado_da_tela_divergente` | 0,999 | 0,999 | 0,001 | formato_de_data_divergente (0,000) | sim | não |
| `lex-4` | L1 | oficiais | certo | `codificacao_incorreta` | 0,999 | 0,999 | 0,001 | formato_de_data_divergente (0,000) | não | não |
| `efe-18` | L0 | ineditos | certo | `localizador_quebrado` | 0,999 | 0,999 | 0,000 | campo_ausente ou campo_renomeado (0,000) | sim | sim |
| `sin-21` | L1 curada | ineditos | certo | `estrutura_aninhada_divergente` | 0,999 | 0,999 | 0,000 | tipo_divergente (0,000) | sim | não |
| `run-9` | L0 | oficiais | certo | `tempo_de_resposta_excedido` | 0,999 | 0,999 | 0,001 | resposta_truncada (0,000) | sim | não |
| `run-4` | L1 | oficiais | certo | `dado_desatualizado` | 0,999 | 0,999 | 0,000 | tempo_de_resposta_excedido (0,000) | sim | sim |
| `lex-11` | L1 curada | oficiais | certo | `codificacao_incorreta` | 0,999 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `efe-17` | L1 | ineditos | certo | `localizador_quebrado` | 0,999 | 1,000 | 0,000 | estrutura_aninhada_divergente (0,000) | sim | sim |
| `lex-7` | L0 | oficiais | certo | `corpo_vazio` | 0,999 | 0,999 | 0,000 | resposta_truncada (0,000) | sim | n/d |
| `lex-21` | L1 | ineditos | certo | `codificacao_incorreta` | 0,999 | 1,000 | 0,000 | valor_fora_do_dominio (0,000) | não | não |
| `semt-18` | L0 | ineditos | certo | `tipo_divergente` | 0,999 | 0,999 | 0,000 | campo_ausente ou campo_renomeado (0,000) | sim | sim |
| `semt-18` | L1 curada | ineditos | certo | `tipo_divergente` | 0,999 | 0,999 | 0,000 | campo_ausente ou campo_renomeado (0,000) | sim | sim |
| `run-9` | L1 curada | oficiais | certo | `tempo_de_resposta_excedido` | 0,999 | 0,999 | 0,000 | tipo_divergente (0,000) | sim | não |
| `sin-11` | L1 curada | oficiais | certo | `estrutura_aninhada_divergente` | 0,999 | 0,999 | 0,000 | campo_ausente ou campo_renomeado (0,000) | sim | não |
| `lex-10` | L0 | oficiais | certo | `resposta_truncada` | 0,999 | 0,999 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `tra-20` | L1 | ineditos | certo | `chave_de_juncao_errada` | 0,999 | 0,999 | 0,000 | campo_ausente ou campo_renomeado (0,000) | sim | não |
| `efe-17` | L1 curada | ineditos | certo | `localizador_quebrado` | 0,999 | 1,000 | 0,000 | estrutura_aninhada_divergente (0,000) | sim | sim |
| `run-20` | L1 | ineditos | certo | `dado_desatualizado` | 0,999 | 0,999 | 0,000 | valor_fora_do_dominio (0,000) | sim | sim |
| `sin-11` | L0 | oficiais | certo | `estrutura_aninhada_divergente` | 0,999 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `lex-1` | L1 curada | oficiais | certo | `resposta_truncada` | 0,999 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `lex-7` | L1 | oficiais | certo | `corpo_vazio` | 0,999 | 1,000 | 0,000 | resposta_truncada (0,000) | sim | não |
| `lex-7` | L1 curada | oficiais | certo | `corpo_vazio` | 0,999 | 1,000 | 0,000 | corpo_nao_e_json (0,000) | sim | não |
| `lex-11` | L0 | oficiais | certo | `codificacao_incorreta` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `semt-18` | L1 | ineditos | certo | `tipo_divergente` | 1,000 | 1,000 | 0,000 | campo_ausente ou campo_renomeado (0,000) | sim | sim |
| `lex-16` | L0 | ineditos | certo | `resposta_truncada` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `run-2` | L0 | oficiais | certo | `tempo_de_resposta_excedido` | 1,000 | 1,000 | 0,000 | limite_de_requisicoes (0,000) | sim | sim |
| `lex-1` | L0 | oficiais | certo | `resposta_truncada` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `lex-20` | L0 | ineditos | certo | `resposta_truncada` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `run-2` | L1 curada | oficiais | certo | `tempo_de_resposta_excedido` | 1,000 | 1,000 | 0,000 | limite_de_requisicoes (0,000) | sim | sim |
| `sin-21` | L1 | ineditos | certo | `estrutura_aninhada_divergente` | 1,000 | 1,000 | 0,000 | tipo_divergente (0,000) | sim | não |
| `lex-11` | L1 | oficiais | certo | `codificacao_incorreta` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `lex-1` | L1 | oficiais | certo | `resposta_truncada` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `run-2` | L1 | oficiais | certo | `tempo_de_resposta_excedido` | 1,000 | 1,000 | 0,000 | limite_de_requisicoes (0,000) | sim | sim |
| `semt-19` | L1 | ineditos | certo | `formato_de_data_divergente` | 1,000 | 1,000 | 0,000 | tipo_divergente (0,000) | sim | sim |
| `lex-17` | L0 | ineditos | certo | `corpo_vazio` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json (0,000) | sim | não |
| `sin-11` | L1 | oficiais | certo | `estrutura_aninhada_divergente` | 1,000 | 1,000 | 0,000 | campo_ausente ou campo_renomeado (0,000) | sim | não |
| `lex-17` | L1 curada | ineditos | certo | `corpo_vazio` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json (0,000) | sim | não |
| `lex-10` | L1 | oficiais | certo | `resposta_truncada` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `lex-17` | L1 | ineditos | certo | `corpo_vazio` | 1,000 | 1,000 | 0,000 | resposta_truncada (0,000) | sim | sim |
| `semt-19` | L0 | ineditos | certo | `formato_de_data_divergente` | 1,000 | 1,000 | 0,000 | tipo_divergente (0,000) | sim | sim |
| `semt-19` | L1 curada | ineditos | certo | `formato_de_data_divergente` | 1,000 | 1,000 | 0,000 | tipo_divergente (0,000) | sim | sim |
| `lex-10` | L1 curada | oficiais | certo | `resposta_truncada` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `lex-20` | L1 | ineditos | certo | `resposta_truncada` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `run-19` | L0 | ineditos | certo | `tempo_de_resposta_excedido` | 1,000 | 1,000 | 0,000 | tipo_divergente (0,000) | sim | sim |
| `lex-16` | L1 | ineditos | certo | `resposta_truncada` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `run-19` | L1 | ineditos | certo | `tempo_de_resposta_excedido` | 1,000 | 1,000 | 0,000 | tipo_divergente (0,000) | sim | sim |
| `run-19` | L1 curada | ineditos | certo | `tempo_de_resposta_excedido` | 1,000 | 1,000 | 0,000 | tipo_divergente (0,000) | sim | sim |
| `lex-16` | L1 curada | ineditos | certo | `resposta_truncada` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
| `lex-20` | L1 curada | ineditos | certo | `resposta_truncada` | 1,000 | 1,000 | 0,000 | corpo_nao_e_json ou corpo_vazio (0,000) | sim | sim |
<!-- /tabela:tb_conf_casos -->

Rótulos iguais aos da corrida oficial da Fase 3 nos casos oficiais (sem os casos de texto corrigido em 28/09): `qwen2.5:7b` L0: 33 de 35; `qwen2.5:7b` L1: 35 de 35.
