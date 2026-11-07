<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py --experimento_prompt a partir de `fase4_experimento` contra `fase4_calibracao/k3 (corrida 16)` (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Experimento dos itens da decisão 55 (corrida 23), gerada em 2026-11-05

O prompt do agente não muda em nenhuma condição: este número vai para o TCC e não decide nada na Fase 5 (decisão 91). b é o número de casos que só a condição acerta, e c, os que só a corrida 16 acerta. A corrida 16 rodou em outra versão do Ollama, e duas corridas iguais já variaram de 0 a 3 casos em 36 (Fase 3-B), então uma diferença de poucos casos não separa a condição do acaso.

<!-- tabela:tb_f4_exp_resumo -->
| Condição | Casos | Acertos | Acerto (%) | Acurácia balanceada (%) | b | c | p (McNemar) | Nos 36 de avaliação | Trocas de rótulo | Fora do conjunto ou sem rótulo | Tokens de entrada (mediana) | Segundos (mediana) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| corrida 16 (k = 3) | 90 | 68 | 75,6 | 81,5 |  |  |  | 31 de 36 |  |  | 1106,5 | 55,36 |
| `exemplar` | 90 | 70 | 77,8 | 83,3 | 6 | 4 | 0,754 | 29 de 36 | 17 | 1 | 1282,5 | 69,56 |
| `rotulos_por_extenso` | 90 | 67 | 74,4 | 79,7 | 5 | 6 | 1,000 | 30 de 36 | 17 | 2 | 1089,5 | 40,64 |
<!-- /tabela:tb_f4_exp_resumo -->
<!-- tabela:tb_f4_exp_mudaram -->
| Condição | Caso | Gabarito | Corrida 16 | Na condição | Efeito |
|---|---|---|---|---|---|
| `exemplar` | `efe-1` | `localizador_quebrado` | `tempo_de_resposta_excedido` | `localizador_quebrado` | ganhou |
| `exemplar` | `efe-3` | `campo_ausente` | `campo_ausente` | `colecao_no_lugar_de_objeto` | perdeu |
| `exemplar` | `lex-3` | `corpo_vazio` | `tempo_de_resposta_excedido` | `corpo_vazio` | ganhou |
| `exemplar` | `lex-6` | `corpo_nao_e_json` | `recurso_inexistente` | `corpo_nao_e_json` | ganhou |
| `exemplar` | `semt-1` | `tipo_divergente` | `tipo_divergente` | `formato_de_data_divergente` | perdeu |
| `exemplar` | `semt-13` | `tipo_divergente` | `tipo_divergente` | `escala_ou_unidade_errada` | perdeu |
| `exemplar` | `semt-6` | `tipo_divergente` | `colecao_no_lugar_de_objeto` | `tipo_divergente` | ganhou |
| `exemplar` | `semt-8` | `nulo_inesperado` | `nulo_inesperado` | `valor_fora_do_dominio` | perdeu |
| `exemplar` | `sin-2` | `campo_renomeado` | `tipo_divergente` | `campo_renomeado` | ganhou |
| `exemplar` | `tra-12` | `escala_ou_unidade_errada` | `tipo_divergente` | `escala_ou_unidade_errada` | ganhou |
| `rotulos_por_extenso` | `efe-2` | `estado_da_tela_divergente` | `estado_da_tela_divergente` | `valor_fora_do_dominio` | perdeu |
| `rotulos_por_extenso` | `efe-6` | `localizador_quebrado` | `localizador_quebrado` | `tempo_de_resposta_excedido` | perdeu |
| `rotulos_por_extenso` | `efe-8` | `estado_da_tela_divergente` | `estado_da_tela_divergente` | `colecao_no_lugar_de_objeto` | perdeu |
| `rotulos_por_extenso` | `run-10` | `limite_de_requisicoes` | `limite_de_requisicoes` | `[limite_de_requisicoes] Limite de requisições` | perdeu |
| `rotulos_por_extenso` | `semt-13` | `tipo_divergente` | `tipo_divergente` | `formato_de_data_divergente` | perdeu |
| `rotulos_por_extenso` | `semt-6` | `tipo_divergente` | `colecao_no_lugar_de_objeto` | `tipo_divergente` | ganhou |
| `rotulos_por_extenso` | `semt-8` | `nulo_inesperado` | `nulo_inesperado` | `tipo_divergente` | perdeu |
| `rotulos_por_extenso` | `sin-14` | `campo_renomeado` | `colecao_no_lugar_de_objeto` | `campo_renomeado` | ganhou |
| `rotulos_por_extenso` | `sin-2` | `campo_renomeado` | `tipo_divergente` | `campo_renomeado` | ganhou |
| `rotulos_por_extenso` | `sin-5` | `campo_ausente` | `colecao_no_lugar_de_objeto` | `campo_ausente` | ganhou |
| `rotulos_por_extenso` | `tra-3` | `chave_de_juncao_errada` | `tipo_divergente` | `chave_de_juncao_errada` | ganhou |
<!-- /tabela:tb_f4_exp_mudaram -->
