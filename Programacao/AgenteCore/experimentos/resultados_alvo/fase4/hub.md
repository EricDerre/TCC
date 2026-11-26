<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por hub.py --resumo a partir de as trilhas das corridas em resultados_alvo/ e o código do hub (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# O que o hub central mostra (Pós-Fase 4, pacote Q6), gerada em 2026-11-25

O hub junta 170 casos com diagnóstico, de 4 corridas; são 83 casos distintos, porque o mesmo caso diagnosticado mais de uma vez aparece como iterações (47 casos têm mais de uma, e o que tem mais tem 6). Em 43 casos o que o modelo declarou não bate com o que o código conferiu, e em 24 houve cura de localizador. Cada caso abre com o relatório em 17 blocos (11 campos da seção 5.5 do syllabus e 6 do que o agente fez). O runner `testar_hub.py` tem 44 testes, 11 deles abrindo a página no navegador sem janela.

<!-- tabela:tb_f4_hub_corridas -->
| Corrida | Pasta | Modo | Modelo | Início | Casos no hub |
|---|---|---|---|---|---|
| corrida 18d | `fase4_tela_v4` | tela | `qwen2.5:7b` | 2026-11-06 | 74 |
| corrida 21d | `fase4_ensaio_v4` | cenarios | `qwen2.5:7b` | 2026-11-06 | 10 |
| corrida 24 | `fase4_ineditos` | ineditos | `qwen2.5:7b` | 2026-11-06 | 36 |
| corrida 28b | `fase5_agente_b` | cenarios | `qwen2.5:7b` | 2026-11-18 | 50 |
<!-- /tabela:tb_f4_hub_corridas -->
