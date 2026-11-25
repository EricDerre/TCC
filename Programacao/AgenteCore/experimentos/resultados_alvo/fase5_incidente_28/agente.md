<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase5.py a partir de cenarios.jsonl, condicoes_fase4.json, fase4.log e progresso_medidas.jsonl da corrida (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Fase 5 do Memorial cola estes blocos, e as contas são as das regras L1 a L15 do plano aprovado, fixadas antes das medidas. -->
# O agente na Fase 5: MTTR e Task Success dos dez cenários (corrida 28, incidente), gerada em 2026-11-18

**Esta corrida não vale como a medida do agente.** A corrida 28, de 18/11/2026, foi lançada com o aplicativo Claude aberto, e o plano pede a corrida com o aplicativo Claude e o VS Code fechados; o Eric decidiu refazer a noite (decisão 145). Nas repetições 2 a 5 dela, o Ollama reaproveitou o prompt lido na repetição 1, e por isso a noite nova, a corrida 28b, roda a frio (decisão 146). Os números ficam como registro do incidente e não entram na comparação com as pessoas.

Corrida lida: `fase5_agente`. Os dez cenários da ficha 36, com o agente inteiro em cada execução. No contrato, o MTTR vai da detecção ao diagnóstico conferido em código e o Task Success é a causa e o campo certos; no localizador, o MTTR vai da detecção à reexecução validada, descontada a restauração do banco, e o Task Success é o roteiro concluído sem erro. A unidade é o cenário (regra L2): por cenário, a média de quem chegou ao fim do cronômetro, com o mínimo e o máximo; no geral e por tipo, a média das médias dos cenários. O intervalo do tempo é a reamostragem dos cenários dentro de cada tipo (2000 reamostras, semente 20261104); o do Task Success é o de Wilson. Quem não chegou ao fim do cronômetro fica fora da média do tempo e dentro do Task Success; a segunda conta põe 600 s no lugar e vale como piso. Nenhuma execução é anulada: a que falhou aparece na última tabela. O tempo total da execução inclui a detecção e é só descrição.

A noite vale a frio quando, em cada repetição, a primeira inferência não reaproveitou nenhum token do que o Ollama tinha guardado e no máximo 50% dos tokens de entrada da repetição vieram guardados. É conferência de validade da noite, fixada antes da corrida 28b com os registros da corrida 28, e não regra de comparação. O que ela não cobre: dentro de uma repetição, o começo do prompt que os cenários dividem continua vindo guardado de um cenário para o outro, e a primeira execução de cada repetição paga a carga do modelo. Nesta corrida: as repetições 2, 3, 4 e 5 não rodaram a frio: a primeira inferência já veio com tokens guardados pelo Ollama, ou mais de 50% dos tokens de entrada da repetição vieram guardados.


<!-- tabela:tb_f5_incidente28_resumo -->
| Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Cenários com todas certas | Com fim de cronômetro | Sem fim | MTTR médio (s) | Reamostragem 95% (s) | Segunda conta, com 600 s para quem não chegou ao fim (s) | Reamostragem 95% da segunda conta (s) | Só com Task Success (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 49 | 98,0 | 89,5 a 99,6 | 9 de 10 | 49 | 1 | 30,5 | 27,2 a 33,8 | 42,0 | 28,8 a 64,9 | 30,5 |
<!-- /tabela:tb_f5_incidente28_resumo -->

<!-- tabela:tb_f5_incidente28_por_tipo -->
| Tipo | Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Cenários com todas certas | Com fim de cronômetro | Sem fim | MTTR médio (s) | Reamostragem 95% (s) | Segunda conta, com 600 s para quem não chegou ao fim (s) | Reamostragem 95% da segunda conta (s) | Só com Task Success (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| contrato | 30 | 29 | 96,7 | 83,3 a 99,4 | 5 de 6 | 29 | 1 | 28,0 | 25,4 a 30,5 | 47,3 | 27,9 a 83,8 | 28,0 |
| localizador | 20 | 20 | 100,0 | 83,9 a 100,0 | 4 de 4 | 20 | 0 | 34,2 | 26,8 a 41,6 | 34,2 | 26,8 a 41,6 | 34,2 |
<!-- /tabela:tb_f5_incidente28_por_tipo -->

<!-- tabela:tb_f5_incidente28_por_cenario -->
| Cenário | Tipo | Execuções | Task Success | Com fim | MTTR médio (s) | Mínimo (s) | Máximo (s) | Segunda conta (s) | Só com Task Success (s) | Rótulo do diagnóstico em cada repetição | Tempo total da execução (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | 5 | 4 | 4 | 22,1 | 21,9 | 22,3 | 137,7 | 22,1 | `resposta_truncada`, `resposta_truncada`, `resposta_truncada`, `resposta_truncada`, `resposta_truncada` | 32,1 |
| `contrato-field_missing` | contrato | 5 | 5 | 5 | 27,6 | 17,9 | 66,2 | 27,6 | 27,6 | `campo_ausente`, `campo_ausente`, `campo_ausente`, `campo_ausente`, `campo_ausente` | 27,9 |
| `contrato-field_renamed` | contrato | 5 | 5 | 5 | 26,3 | 16,3 | 65,1 | 26,3 | 26,3 | `campo_renomeado`, `campo_renomeado`, `campo_renomeado`, `campo_renomeado`, `campo_renomeado` | 26,7 |
| `contrato-type_drift` | contrato | 5 | 5 | 5 | 29,0 | 18,2 | 67,5 | 29,0 | 29,0 | `tipo_divergente`, `tipo_divergente`, `tipo_divergente`, `tipo_divergente`, `tipo_divergente` | 29,4 |
| `contrato-escala_ou_unidade_errada` | contrato | 5 | 5 | 5 | 32,4 | 19,3 | 80,1 | 32,4 | 32,4 | `escala_ou_unidade_errada`, `escala_ou_unidade_errada`, `escala_ou_unidade_errada`, `escala_ou_unidade_errada`, `escala_ou_unidade_errada` | 32,8 |
| `contrato-error_500` | contrato | 5 | 5 | 5 | 30,8 | 18,2 | 76,6 | 30,8 | 30,8 | `erro_interno_do_servidor`, `erro_interno_do_servidor`, `erro_interno_do_servidor`, `erro_interno_do_servidor`, `erro_interno_do_servidor` | 31,1 |
| `localizador-front-busca` | localizador | 5 | 5 | 5 | 44,4 | 38,8 | 65,2 | 44,4 | 44,4 | `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado` | 49,8 |
| `localizador-front-admin-login` | localizador | 5 | 5 | 5 | 38,8 | 38,3 | 39,5 | 38,8 | 38,8 | `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado` | 44,2 |
| `localizador-front-admin-produtos` | localizador | 5 | 5 | 5 | 27,4 | 19,0 | 60,3 | 27,4 | 27,4 | `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado` | 33,2 |
| `localizador-front-cliente-reserva` | localizador | 5 | 5 | 5 | 26,2 | 17,2 | 60,0 | 26,2 | 26,2 | `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado` | 32,5 |
<!-- /tabela:tb_f5_incidente28_por_cenario -->

<!-- tabela:tb_f5_incidente28_noite -->
| Execuções gravadas | Esperadas | Noite completa | Noite a frio | Versões do Ollama nos diagnósticos | Versões do navegador | Hash do banco no começo das repetições | Linha FIM no log | Tempo total das execuções (s) | Tempo total médio por cenário (s) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 50 | sim | não | 0.40.16 | 156.0.8078.4 | 9fe5e7cb64288c9d | sim | 1698,0 | 34,0 |
<!-- /tabela:tb_f5_incidente28_noite -->

<!-- tabela:tb_f5_incidente28_frio -->
| Repetição | Inferências | Tokens de entrada | Tokens que vieram do que o Ollama tinha guardado | Parcela guardada (%) | Guardados na primeira inferência | Leitura do prompt, somada (s) | Carga do modelo, somada (s) | A frio |
|---|---|---|---|---|---|---|---|---|
| 1 | 10 | 11966 | 1505 | 12,6 | 0 | 462,4 | 8,7 | sim |
| 2 | 10 | 11966 | 10975 | 91,7 | 1217 | 45,3 | 0,3 | não |
| 3 | 10 | 11966 | 10975 | 91,7 | 1217 | 45,0 | 0,3 | não |
| 4 | 10 | 11966 | 10975 | 91,7 | 1217 | 44,3 | 0,3 | não |
| 5 | 10 | 11966 | 10975 | 91,7 | 1217 | 43,8 | 0,2 | não |
<!-- /tabela:tb_f5_incidente28_frio -->

<!-- tabela:tb_f5_incidente28_identidade -->
| Item | Na corrida | Na corrida 21d | Igual | Para a noite se diferir |
|---|---|---|---|---|
| biblioteca de produção (hash) | `95af35290860` | `95af35290860` | sim | sim |
| prompt fixo do diagnóstico (hash) | `2e42cf9c31826941` | `2e42cf9c31826941` | sim | sim |
| índice da busca (hash) | `11e763ba9cb1fdf4` | `11e763ba9cb1fdf4` | sim | sim |
| k (verbetes entregues ao modelo) | `3` | `3` | sim | sim |
| limiares do selo | `baixo até 0,8318, alto a partir de 0,9898, k 3 (conteúdo 13a02982)` | `baixo até 0,8318, alto a partir de 0,9898, k 3 (conteúdo 13a02982)` | sim | sim |
| versão do navegador | `156.0.8078.4` | `156.0.8078.4` | sim | sim |
| modelo | `qwen2.5:7b` | `qwen2.5:7b` | sim | não |
| alternativas por posição (top_logprobs) | `20` | `20` | sim | não |
| teto de tokens da resposta | `600` | `600` | sim | não |
| Playwright | `1.64.1` | `1.64.1` | sim | não |
| versão do código do caso ao vivo | `5` | `4` | não | não |
| busca com os sinais contra a referência | `True` | `True` | sim | não |
<!-- /tabela:tb_f5_incidente28_identidade -->

<!-- tabela:tb_f5_incidente28_sem_sucesso -->
| Cenário | Repetição | Tipo | Detectou | Rótulo do diagnóstico | Causa esperada | Falha da cura | MTTR (s) | Segundos |
|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | 1 | contrato | sim | `resposta_truncada` | `resposta_truncada` | n/d | n/d | 70,9 |
<!-- /tabela:tb_f5_incidente28_sem_sucesso -->
