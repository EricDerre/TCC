<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por comparar_qwen_coder.py a partir dos registros oficiais (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão — o comparativo do Memorial cola estes blocos. -->
# Comparativo qwen2.5:7b × qwen2.5-coder:7b — gerado em 2026-10-01

Fontes: resumo_metricas.json (Ryzen); resultados_alvo/resumo_metricas.json (+ avaliacao.json); resultados_alvo/fase3/resumo_fase3.json + avaliacao_fase3.json (gerado em 2026-09-29T11:04:10); comparacao_fases.json; decisao_modelo.json (gerado em 2026-10-01T09:43:39). Melhor versão nos 36: qwen2.5:7b L1, coder:7b L3. Casos inéditos (28/09): modelos rodados = ['qwen2.5-coder:3b', 'qwen2.5:7b'] — o qwen2.5-coder:7b não rodou lá. Estabilidade de ranking (top-1 em 36 cortes): qwen2.5:7b: 14; qwen2.5-coder:7b: 5.


<!-- tabela:cq_fase2a -->
| Fase 2-A (Ryzen) · estratégia | n | acerto qwen2.5:7b | acerto coder:7b | Δ (coder − qwen) | s/caso qwen2.5:7b | s/caso coder:7b |
|---|---|---|---|---|---|---|
| 2-A · estratégia linear | 90 | 53,3% | 48,9% | -4,4 pp | 17,1 | 25,9 |
| 2-A · estratégia compilador | 90 | 47,8% | 52,2% | +4,4 pp | 18,5 | 18,5 |
| 2-A · estratégia dominio | 90 | 48,9% | 48,9% | +0,0 pp | 17,5 | 17,4 |
<!-- /tabela:cq_fase2a -->

<!-- tabela:cq_fase2a_classe -->
| Fase 2-A · classe (3 estratégias) | n | qwen2.5:7b | coder:7b | Δ |
|---|---|---|---|---|
| 1 lexica | 45 | 60,0% | 68,9% | +8,9 pp |
| 2 sintatica | 45 | 51,1% | 40,0% | -11,1 pp |
| 3 semantica | 45 | 37,8% | 40,0% | +2,2 pp |
| 4 traducao | 45 | 37,8% | 22,2% | -15,6 pp |
| 5 runtime | 45 | 75,6% | 77,8% | +2,2 pp |
| 6 efeito | 45 | 37,8% | 51,1% | +13,3 pp |
<!-- /tabela:cq_fase2a_classe -->

<!-- tabela:cq_fase2b -->
| Fase 2-B (i5) · condição | n | acerto qwen2.5:7b | acerto coder:7b | Δ | contra A0 qwen2.5:7b | contra A0 coder:7b | forma ok/conteúdo errado qwen2.5:7b | … coder:7b | s/caso qwen2.5:7b | s/caso coder:7b |
|---|---|---|---|---|---|---|---|---|---|---|
| 2-B · A0 | 90 | 57,8% | 50,0% | -7,8 pp | — | — | 42,2% | 48,9% | 38,0 | 51,3 |
| 2-B · A1 | 90 | 62,2% | 63,3% | +1,1 pp | +4,4 pp (p = 0,5034) | +13,3 pp (p = 0,0730) | 37,8% | 30,0% | 57,1 | 61,2 |
| 2-B · A2 | 90 | 70,0% | 72,2% | +2,2 pp | +12,2 pp (p = 0,0708) | +22,2 pp (p = 0,0005) | 30,0% | 27,8% | 61,1 | 66,6 |
<!-- /tabela:cq_fase2b -->

<!-- tabela:cq_fase2b_classe -->
| Fase 2-B · A2 · classe | n | qwen2.5:7b | coder:7b | Δ |
|---|---|---|---|---|
| 1 lexica | 15 | 86,7% | 100,0% | +13,3 pp |
| 2 sintatica | 15 | 73,3% | 73,3% | +0,0 pp |
| 3 semantica | 15 | 73,3% | 60,0% | -13,3 pp |
| 4 traducao | 15 | 46,7% | 40,0% | -6,7 pp |
| 5 runtime | 15 | 80,0% | 86,7% | +6,7 pp |
| 6 efeito | 15 | 60,0% | 73,3% | +13,3 pp |
<!-- /tabela:cq_fase2b_classe -->

<!-- tabela:cq_fase2b_nivel -->
| Fase 2-B · A2 · nível | n | qwen2.5:7b | coder:7b | Δ |
|---|---|---|---|---|
| 1 fácil | 30 | 66,7% | 66,7% | +0,0 pp |
| 2 médio | 30 | 73,3% | 73,3% | +0,0 pp |
| 3 difícil | 30 | 70,0% | 76,7% | +6,7 pp |
<!-- /tabela:cq_fase2b_nivel -->

<!-- tabela:cq_confronto_2b -->
| Fase 2-B · confronto caso a caso | n | ambos acertam | nenhum | só o Coder | só o qwen | Δ | p (McNemar exato) |
|---|---|---|---|---|---|---|---|
| 2-B · A0 | 90 | 33 | 26 | 12 | 19 | -7,8 pp | 0,2810 |
| 2-B · A1 | 90 | 45 | 22 | 12 | 11 | +1,1 pp | 1,0000 |
| 2-B · A2 | 90 | 53 | 15 | 12 | 10 | +2,2 pp | 0,8318 |
<!-- /tabela:cq_confronto_2b -->

<!-- tabela:cq_fase3 -->
| Fase 3 · versão · conjunto | n | acerto qwen2.5:7b | acerto coder:7b | Δ acerto | balanceada qwen2.5:7b | balanceada coder:7b | Δ balanceada | s/caso qwen2.5:7b | s/caso coder:7b |
|---|---|---|---|---|---|---|---|---|---|
| F3 · L0 · 36 de avaliação | 36 | 77,8% | 75,0% | -2,8 pp | 81,2% | 80,0% | -1,2 pp | 69,5 | 70,7 |
| F3 · L1 · 36 de avaliação | 36 | 88,9% | 75,0% | -13,9 pp | 91,7% | 80,0% | -11,7 pp | 79,5 | 65,8 |
| F3 · L2 · 36 de avaliação | 36 | 83,3% | 75,0% | -8,3 pp | 84,2% | 80,0% | -4,2 pp | 80,6 | 66,8 |
| F3 · L3 · 36 de avaliação | 36 | 86,1% | 77,8% | -8,3 pp | 86,2% | 84,2% | -2,0 pp | 53,9 | 56,6 |
| F3 · L0 · 54 de aprendizado | 54 | 66,7% | 68,5% | +1,8 pp | 74,1% | 73,7% | -0,4 pp | 63,6 | 68,5 |
| F3 · L1 · 54 de aprendizado | 54 | 68,5% | 74,1% | +5,6 pp | 79,3% | 82,1% | +2,8 pp | 75,3 | 68,0 |
| F3 · L2 · 54 de aprendizado | 54 | 68,5% | 72,2% | +3,7 pp | 74,3% | 74,4% | +0,1 pp | 69,3 | 62,5 |
| F3 · L3 · 54 de aprendizado | 54 | 72,2% | 68,5% | -3,7 pp | 76,4% | 69,9% | -6,5 pp | 43,6 | 47,9 |
| F3 · L0 · 90 | 90 | 71,1% | 71,1% | +0,0 pp | 75,7% | 75,8% | +0,1 pp | 66,8 | 68,7 |
| F3 · L1 · 90 | 90 | 76,7% | 74,4% | -2,3 pp | 83,0% | 78,9% | -4,1 pp | 78,2 | 67,4 |
| F3 · L2 · 90 | 90 | 74,4% | 73,3% | -1,1 pp | 78,1% | 77,8% | -0,3 pp | 77,6 | 65,5 |
| F3 · L3 · 90 | 90 | 77,8% | 72,2% | -5,6 pp | 80,7% | 75,4% | -5,3 pp | 47,0 | 49,8 |
<!-- /tabela:cq_fase3 -->

<!-- tabela:cq_confronto_f3 -->
| Fase 3 · confronto caso a caso | n | ambos acertam | nenhum | só o Coder | só o qwen | Δ | p (McNemar exato) |
|---|---|---|---|---|---|---|---|
| F3 · L0 · 36 de avaliação | 36 | 23 | 4 | 4 | 5 | -2,8 pp | 1,0000 |
| F3 · L0 · 90 | 90 | 55 | 17 | 9 | 9 | +0,0 pp | 1,0000 |
| F3 · L1 · 36 de avaliação | 36 | 26 | 3 | 1 | 6 | -13,9 pp | 0,1250 |
| F3 · L1 · 90 | 90 | 59 | 13 | 8 | 10 | -2,2 pp | 0,8145 |
| F3 · L2 · 36 de avaliação | 36 | 25 | 4 | 2 | 5 | -8,3 pp | 0,4531 |
| F3 · L2 · 90 | 90 | 57 | 14 | 9 | 10 | -1,1 pp | 1,0000 |
| F3 · L3 · 36 de avaliação | 36 | 26 | 3 | 2 | 5 | -8,3 pp | 0,4531 |
| F3 · L3 · 90 | 90 | 56 | 11 | 9 | 14 | -5,6 pp | 0,4049 |
<!-- /tabela:cq_confronto_f3 -->

<!-- tabela:cq_fase3_classe_L0 -->
| Fase 3 · L0 · classe (90) | n | qwen2.5:7b | coder:7b | Δ |
|---|---|---|---|---|
| 1 lexica | 15 | 86,7% | 93,3% | +6,6 pp |
| 2 sintatica | 15 | 73,3% | 80,0% | +6,7 pp |
| 3 semantica | 15 | 80,0% | 60,0% | -20,0 pp |
| 4 traducao | 15 | 46,7% | 26,7% | -20,0 pp |
| 5 runtime | 15 | 80,0% | 93,3% | +13,3 pp |
| 6 efeito | 15 | 60,0% | 73,3% | +13,3 pp |
<!-- /tabela:cq_fase3_classe_L0 -->

<!-- tabela:cq_fase3_classe_L1 -->
| Fase 3 · L1 · classe (90) | n | qwen2.5:7b | coder:7b | Δ |
|---|---|---|---|---|
| 1 lexica | 15 | 86,7% | 93,3% | +6,6 pp |
| 2 sintatica | 15 | 80,0% | 80,0% | +0,0 pp |
| 3 semantica | 15 | 80,0% | 66,7% | -13,3 pp |
| 4 traducao | 15 | 46,7% | 40,0% | -6,7 pp |
| 5 runtime | 15 | 100,0% | 93,3% | -6,7 pp |
| 6 efeito | 15 | 66,7% | 73,3% | +6,6 pp |
<!-- /tabela:cq_fase3_classe_L1 -->

<!-- tabela:cq_fase3_classe_melhor -->
| Fase 3 · melhor versão de cada um (qwen L1, coder L3) · classe (90) | n | qwen2.5:7b | coder:7b | Δ |
|---|---|---|---|---|
| 1 lexica | 15 | 86,7% | 86,7% | +0,0 pp |
| 2 sintatica | 15 | 80,0% | 66,7% | -13,3 pp |
| 3 semantica | 15 | 80,0% | 73,3% | -6,7 pp |
| 4 traducao | 15 | 46,7% | 33,3% | -13,4 pp |
| 5 runtime | 15 | 100,0% | 86,7% | -13,3 pp |
| 6 efeito | 15 | 66,7% | 86,7% | +20,0 pp |
<!-- /tabela:cq_fase3_classe_melhor -->

<!-- tabela:cq_fase3_nivel_L0 -->
| Fase 3 · L0 · nível (90) | n | qwen2.5:7b | coder:7b | Δ |
|---|---|---|---|---|
| 1 fácil | 30 | 66,7% | 66,7% | +0,0 pp |
| 2 médio | 30 | 73,3% | 76,7% | +3,4 pp |
| 3 difícil | 30 | 73,3% | 70,0% | -3,3 pp |
<!-- /tabela:cq_fase3_nivel_L0 -->

<!-- tabela:cq_fase3_nivel_L1 -->
| Fase 3 · L1 · nível (90) | n | qwen2.5:7b | coder:7b | Δ |
|---|---|---|---|---|
| 1 fácil | 30 | 76,7% | 63,3% | -13,4 pp |
| 2 médio | 30 | 76,7% | 80,0% | +3,3 pp |
| 3 difícil | 30 | 76,7% | 80,0% | +3,3 pp |
<!-- /tabela:cq_fase3_nivel_L1 -->

<!-- tabela:cq_documentacao -->
| Época | propostas qwen2.5:7b | aceitas qwen2.5:7b | aceitas % qwen2.5:7b | propostas coder:7b | aceitas coder:7b | aceitas % coder:7b | tokens acrescentados qwen2.5:7b | … coder:7b | verbetes qwen2.5:7b | verbetes coder:7b |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 87 | 40 | 46,0% | 54 | 25 | 46,3% | 8639 | 4760 | 42 | 36 |
| 2 | 86 | 12 | 14,0% | 54 | 7 | 13,0% | 2643 | 1373 | 43 | 36 |
| 3 | 91 | 9 | 9,9% | 54 | 7 | 13,0% | 1787 | 1381 | 45 | 36 |
<!-- /tabela:cq_documentacao -->

<!-- tabela:cq_rejeicoes -->
| Motivos de rejeição (3 épocas) | qwen2.5:7b | coder:7b |
|---|---|---|
| duplicada | 53 | 33 |
| palavra_chave_invalida | 44 | 25 |
| teto_notas_verbete | 33 | 0 |
| id_repetido | 23 | 0 |
| trecho_nao_encontrado | 18 | 11 |
| arquivo_inexistente | 13 | 10 |
| motivo_longo | 0 | 26 |
| retificacao_sem_trecho | 0 | 15 |
<!-- /tabela:cq_rejeicoes -->

<!-- tabela:cq_revisao -->
| Revisão humana das edições aceitas | correta qwen2.5:7b | parcial qwen2.5:7b | errada qwen2.5:7b | correta coder:7b | parcial coder:7b | errada coder:7b |
|---|---|---|---|---|---|---|
| nota | 7 | 5 | 2 | 9 | 5 | 2 |
| retificacao | 2 | 2 | 6 | 1 | 2 | 5 |
| novo_verbete | 0 | 1 | 4 | — | — | — |
<!-- /tabela:cq_revisao -->

<!-- tabela:cq_recuperacao -->
| Versão | hit@3 nos 90 qwen2.5:7b | hit@3 nos 90 coder:7b | hit@3 nos 36 qwen2.5:7b | hit@3 nos 36 coder:7b | verbetes qwen2.5:7b | verbetes coder:7b |
|---|---|---|---|---|---|---|
| L0 | 80,0% | 80,0% | 86,1% | 86,1% | 36 | 36 |
| L1 | 77,8% | 81,1% | 83,3% | 86,1% | 42 | 36 |
| L2 | 78,9% | 78,9% | 83,3% | 83,3% | 43 | 36 |
| L3 | 78,9% | 80,0% | 86,1% | 86,1% | 45 | 36 |
<!-- /tabela:cq_recuperacao -->

<!-- tabela:cq_flips -->
| Transição · conjunto | ✓→✗ qwen2.5:7b | ✗→✓ qwen2.5:7b | autoenvenenamento qwen2.5:7b | ✓→✗ coder:7b | ✗→✓ coder:7b | autoenvenenamento coder:7b |
|---|---|---|---|---|---|---|
| L0→L1 · 36 | 0 | 4 | 0,0% | 0 | 0 | 0,0% |
| L0→L1 · 90 | 2 | 7 | 2,2% | 1 | 4 | 1,1% |
| L1→L2 · 36 | 2 | 0 | 5,6% | 1 | 1 | 2,8% |
| L1→L2 · 90 | 5 | 3 | 5,6% | 5 | 4 | 5,6% |
| L2→L3 · 36 | 1 | 2 | 2,8% | 1 | 2 | 2,8% |
| L2→L3 · 90 | 1 | 4 | 1,1% | 6 | 5 | 6,7% |
<!-- /tabela:cq_flips -->

<!-- tabela:cq_entre_fases -->
| Coluna · conjunto | acerto qwen2.5:7b | acerto coder:7b | Δ | balanceada qwen2.5:7b | balanceada coder:7b |
|---|---|---|---|---|---|
| 2A_linear_ryzen · nos 36 | 63,9% | 44,4% | -19,5 pp | 65,0% | 50,4% |
| 2B_A0 · nos 36 | 66,7% | 41,7% | -25,0 pp | 66,7% | 48,3% |
| 2B_A2 · nos 36 | 77,8% | 72,2% | -5,6 pp | 81,2% | 77,5% |
| F3_L0 · nos 36 | 77,8% | 75,0% | -2,8 pp | 81,2% | 80,0% |
| F3_L1 · nos 36 | 88,9% | 75,0% | -13,9 pp | 91,7% | 80,0% |
| F3_L2 · nos 36 | 83,3% | 75,0% | -8,3 pp | 84,2% | 80,0% |
| F3_L3 · nos 36 | 86,1% | 77,8% | -8,3 pp | 86,2% | 84,2% |
| F3_melhor · nos 36 | 88,9% | 77,8% | -11,1 pp | 91,7% | 84,2% |
| 2A_linear_ryzen · nos 90 | 53,3% | 48,9% | -4,4 pp | 60,1% | 54,9% |
| 2B_A0 · nos 90 | 57,8% | 50,0% | -7,8 pp | 64,5% | 56,9% |
| 2B_A2 · nos 90 | 70,0% | 72,2% | +2,2 pp | 74,9% | 75,2% |
| F3_L0 · nos 90 | 71,1% | 71,1% | +0,0 pp | 75,7% | 75,8% |
| F3_L1 · nos 90 | 76,7% | 74,4% | -2,3 pp | 83,0% | 78,9% |
| F3_L2 · nos 90 | 74,4% | 73,3% | -1,1 pp | 78,1% | 77,8% |
| F3_L3 · nos 90 | 77,8% | 72,2% | -5,6 pp | 80,7% | 75,4% |
| F3_melhor · nos 90 | 76,7% | 74,4% | -2,3 pp | 83,0% | 78,9% |
<!-- /tabela:cq_entre_fases -->

<!-- tabela:cq_riscos -->
| Risco | qwen2.5:7b | coder:7b |
|---|---|---|
| adesão cega à documentação errada (2-B A5) — não medida nos dois | — | — |
| teto com o verbete de ouro forçado (2-B A3) — não medido nos dois | — | — |
| tentativas de decorar o caso (Fase 3, total) | 0 | 0 |
| autoenvenenamento nos 36 por transição (Fase 3) | L0→L1 0,0% / L1→L2 5,6% / L2→L3 2,8% | L0→L1 0,0% / L1→L2 2,8% / L2→L3 2,8% |
<!-- /tabela:cq_riscos -->

<!-- tabela:cq_regra36 -->
| Posição | Modelo | L | balanceada (36) | acerto (36) | s/caso | autoenv. máx. | risco | vetado |
|---|---|---|---|---|---|---|---|---|
| 1 | qwen2.5:7b | L1 | 91,7% | 88,9% | 79,5 | 5,6% | 5,57 | não |
| 2 | qwen2.5:7b | L3 | 86,2% | 86,1% | 53,9 | 5,6% | 7,43 | não |
| 3 | qwen2.5:7b | L2 | 84,2% | 83,3% | 80,6 | 5,6% | 8,37 | não |
| 4 | qwen2.5-coder:7b | L3 | 84,2% | 77,8% | 56,6 | 2,8% | 8,33 | não |
| 9 | qwen2.5:7b | L0 | 81,2% | 77,8% | 69,5 | 5,6% | 10,20 | não |
| 10 | qwen2.5-coder:7b | L0 | 80,0% | 75,0% | 70,7 | 2,8% | 10,20 | não |
| 11 | qwen2.5-coder:7b | L1 | 80,0% | 75,0% | 65,8 | 2,8% | 10,20 | não |
| 12 | qwen2.5-coder:7b | L2 | 80,0% | 75,0% | 66,8 | 2,8% | 10,20 | não |
<!-- /tabela:cq_regra36 -->

<!-- tabela:cq_bootstrap -->
| Combinação | P(top-1) nos 36 | IC 95% nos 36 | P(top-1) nos 90 | IC 95% nos 90 |
|---|---|---|---|---|
| qwen2.5-coder:7b/L0 | 0,2% | 66,7–88,9 | 0,2% | 67,6–82,7 |
| qwen2.5-coder:7b/L1 | 0,0% | 66,7–88,9 | 9,8% | 70,5–85,8 |
| qwen2.5-coder:7b/L2 | 0,0% | 67,7–88,9 | 3,7% | 69,4–84,4 |
| qwen2.5-coder:7b/L3 | 0,5% | 70,0–91,1 | 1,0% | 66,3–82,8 |
| qwen2.5:7b/L0 | 0,2% | 67,7–91,2 | 0,4% | 67,4–82,8 |
| qwen2.5:7b/L1 | 77,6% | 81,9–97,8 | 50,0% | 75,9–88,3 |
| qwen2.5:7b/L2 | 0,0% | 72,2–94,0 | 0,2% | 70,6–85,2 |
| qwen2.5:7b/L3 | 15,2% | 75,0–96,7 | 17,2% | 73,7–87,5 |
<!-- /tabela:cq_bootstrap -->

<!-- tabela:cq_escore_pareto -->
| Combinação | escore ponderado | não dominado (Pareto) |
|---|---|---|
| qwen2.5:7b/L1 | 0,8942 | sim |
| qwen2.5:7b/L3 | 0,7897 | sim |
| qwen2.5-coder:7b/L3 | 0,6921 | não |
| qwen2.5:7b/L2 | 0,6788 | não |
| qwen2.5:7b/L0 | 0,5905 | não |
| qwen2.5-coder:7b/L1 | 0,5562 | não |
| qwen2.5-coder:7b/L2 | 0,5545 | não |
| qwen2.5-coder:7b/L0 | 0,5478 | não |
<!-- /tabela:cq_escore_pareto -->

<!-- tabela:cq_ponte -->
| Ponte de versão (0.34.1) · nos 36 | acerto | balanceada | b (só nova) | c (só F3) | p |
|---|---|---|---|---|---|
| qwen2.5-coder:7b | 75,0% | 80,0% | 0 | 0 | 1,0000 |
| qwen2.5:7b | 77,8% | 78,8% | 1 | 1 | 1,0000 |
<!-- /tabela:cq_ponte -->

<!-- tabela:cq_onde_vence -->
| Onde o Coder fica à frente | métrica | qwen2.5:7b | coder:7b | Δ | n | p |
|---|---|---|---|---|---|---|
| 2-A · estratégia compilador | acerto | 47,8 | 52,2 | +4,4 pp | 90 | — |
| 2-B · A1 | acerto | 62,2 | 63,3 | +1,1 pp | 90 | — |
| 2-B · A2 | acerto | 70,0 | 72,2 | +2,2 pp | 90 | — |
| F3 · L0 · 54 de aprendizado | acerto | 66,7 | 68,5 | +1,8 pp | 54 | — |
| F3 · L1 · 54 de aprendizado | acerto | 68,5 | 74,1 | +5,6 pp | 54 | — |
| F3 · L2 · 54 de aprendizado | acerto | 68,5 | 72,2 | +3,7 pp | 54 | — |
| 2B_A2 · nos 90 | acerto | 70,0 | 72,2 | +2,2 pp | — | — |
| F3 · L1 · 54 de aprendizado | acurácia balanceada | 79,3 | 82,1 | +2,8 pp | 54 | — |
| F3 · L2 · 54 de aprendizado | acurácia balanceada | 74,3 | 74,4 | +0,1 pp | 54 | — |
| F3 · L0 · 90 | acurácia balanceada | 75,7 | 75,8 | +0,1 pp | 90 | — |
| fase2b classe A2 · 1 lexica | acerto | 86,7 | 100,0 | +13,3 pp | 15 | — |
| fase2b classe A2 · 5 runtime | acerto | 80,0 | 86,7 | +6,7 pp | 15 | — |
| fase2b classe A2 · 6 efeito | acerto | 60,0 | 73,3 | +13,3 pp | 15 | — |
| fase2b nivel A2 · 3 difícil | acerto | 70,0 | 76,7 | +6,7 pp | 30 | — |
| fase3 classe L0 · 1 lexica | acerto | 86,7 | 93,3 | +6,6 pp | 15 | — |
| fase3 classe L0 · 2 sintatica | acerto | 73,3 | 80,0 | +6,7 pp | 15 | — |
| fase3 classe L0 · 5 runtime | acerto | 80,0 | 93,3 | +13,3 pp | 15 | — |
| fase3 classe L0 · 6 efeito | acerto | 60,0 | 73,3 | +13,3 pp | 15 | — |
| fase3 classe L1 · 1 lexica | acerto | 86,7 | 93,3 | +6,6 pp | 15 | — |
| fase3 classe L1 · 6 efeito | acerto | 66,7 | 73,3 | +6,6 pp | 15 | — |
| fase3 classe melhor · 6 efeito | acerto | 66,7 | 86,7 | +20,0 pp | 15 | — |
| fase3 nivel L0 · 2 médio | acerto | 73,3 | 76,7 | +3,4 pp | 30 | — |
| fase3 nivel L1 · 2 médio | acerto | 76,7 | 80,0 | +3,3 pp | 30 | — |
| fase3 nivel L1 · 3 difícil | acerto | 76,7 | 80,0 | +3,3 pp | 30 | — |
| 2-B · A1 (confronto direto) | casos só o Coder acertou − só o qwen acertou | 11 | 12 | +1,1 pp | 90 | 1,0000 |
| 2-B · A2 (confronto direto) | casos só o Coder acertou − só o qwen acertou | 10 | 12 | +2,2 pp | 90 | 0,8318 |
<!-- /tabela:cq_onde_vence -->
