<!-- ! Alteração de IA - Revisar: gerado por gerar_tabelas_relatorio_fase3.py a partir de resumo_fase3.json, decisao_modelo.json e fase3.log -- NÃO editar à mão.
     ! Motivo: são as tabelas coladas no relatório da Fase 3 do Memorial; o --check confere que cada bloco colado é idêntico ao regerado, para nenhum número entrar digitado. -->

# Tabelas do relatório da Fase 3

Fontes: `resumo` = `resumo_fase3.json`; `decisao` = `decisao_modelo.json`; `log` = `fase3.log`.

## cf_acerto_90

<!-- tabela:cf_acerto_90 -->
| Modelo | 2-A linear (Ryzen) | 2-B A0 | 2-B A2 | F3 L0 | F3 L3 | F3 melhor |
|---|---|---|---|---|---|---|
| granite4.2:8b | 67,8% [57,6–76,5] | 66,7% [56,4–75,5] | 76,7% [66,9–84,2] | 76,7% [66,9–84,2] | 75,6% [65,8–83,3] | **77,8% [68,2–85,1] (L1)** |
| phi4-mini:3.8b | 23,3% [15,8–33,1] | 23,3% [15,8–33,1] | **25,6% [17,7–35,4]** | — | — | — |
| qwen2.5-coder:1.5b | 5,6% [2,4–12,4] | 5,6% [2,4–12,4] | **16,7% [10,4–25,7]** | — | — | — |
| qwen2.5-coder:1.5b-instruct-fp16 | — | **8,9% [4,6–16,6]** | — | — | — | — |
| qwen2.5-coder:1.5b-instruct-q8_0 | **12,5% [5,9–24,7]** | 8,9% [4,6–16,6] | — | — | — | — |
| qwen2.5-coder:3b | 25,6% [17,7–35,4] | 23,3% [15,8–33,1] | 63,3% [53,0–72,6] | 65,6% [55,3–74,6] | **67,8% [57,6–76,5]** | 66,7% [56,4–75,5] (L1) |
| qwen2.5-coder:7b | 48,9% [38,8–59,0] | 50,0% [39,9–60,1] | 72,2% [62,2–80,4] | 71,1% [61,0–79,5] | 72,2% [62,2–80,4] | **74,4% [64,6–82,3] (L1)** |
| qwen2.5:7b | 53,3% [43,1–63,3] | 57,8% [47,5–67,5] | 70,0% [59,9–78,5] | 71,1% [61,0–79,5] | **77,8% [68,2–85,1]** | 76,7% [66,9–84,2] (L1) |
| **Média** | 33,9% (7 modelos) | 30,6% (8 modelos) | 54,1% (6 modelos) | 71,1% (4 modelos) | 73,3% (4 modelos) | 73,9% (4 modelos) |
<!-- /tabela:cf_acerto_90 -->

## cf_balanceada_90

<!-- tabela:cf_balanceada_90 -->
| Modelo | 2-A linear (Ryzen) | 2-B A0 | 2-B A2 | F3 L0 | F3 L3 | F3 melhor |
|---|---|---|---|---|---|---|
| granite4.2:8b | 74,7% | 72,3% | 79,9% | 79,6% | 78,7% | **80,2% (L1)** |
| phi4-mini:3.8b | 30,5% | **31,4%** | 30,2% | — | — | — |
| qwen2.5-coder:1.5b | 4,3% | 4,3% | **17,4%** | — | — | — |
| qwen2.5-coder:1.5b-instruct-fp16 | — | **10,9%** | — | — | — | — |
| qwen2.5-coder:1.5b-instruct-q8_0 | **13,6%** | 10,9% | — | — | — | — |
| qwen2.5-coder:3b | 36,2% | 33,4% | 70,2% | 71,5% | **72,6%** | **72,6% (L1)** |
| qwen2.5-coder:7b | 54,9% | 56,9% | 75,2% | 75,8% | 75,4% | **78,9% (L1)** |
| qwen2.5:7b | 60,1% | 64,5% | 74,9% | 75,7% | 80,7% | **83,0% (L1)** |
| **Média** | 39,2% (7 modelos) | 35,6% (8 modelos) | 58,0% (6 modelos) | 75,7% (4 modelos) | 76,8% (4 modelos) | 78,7% (4 modelos) |
<!-- /tabela:cf_balanceada_90 -->

## cf_acerto_36

<!-- tabela:cf_acerto_36 -->
| Modelo | 2-A linear (Ryzen) | 2-B A0 | 2-B A2 | F3 L0 | F3 L3 | F3 melhor |
|---|---|---|---|---|---|---|
| granite4.2:8b | 75,0% [58,9–86,2] | 72,2% [56,0–84,2] | **80,6% [65,0–90,2]** | **80,6% [65,0–90,2]** | **80,6% [65,0–90,2]** | **80,6% [65,0–90,2] (L0)** |
| phi4-mini:3.8b | **25,0% [13,8–41,1]** | 22,2% [11,7–38,1] | **25,0% [13,8–41,1]** | — | — | — |
| qwen2.5-coder:1.5b | 0,0% [0,0–9,6] | 0,0% [0,0–9,6] | **11,1% [4,4–25,3]** | — | — | — |
| qwen2.5-coder:1.5b-instruct-fp16 | — | **2,8% [0,5–14,2]** | — | — | — | — |
| qwen2.5-coder:1.5b-instruct-q8_0 | 0,0% [0,0–13,8] | **2,8% [0,5–14,2]** | — | — | — | — |
| qwen2.5-coder:3b | 19,4% [9,8–35,0] | 19,4% [9,8–35,0] | 69,4% [53,1–82,0] | 69,4% [53,1–82,0] | **72,2% [56,0–84,2]** | **72,2% [56,0–84,2] (L2)** |
| qwen2.5-coder:7b | 44,4% [29,5–60,4] | 41,7% [27,1–57,8] | 72,2% [56,0–84,2] | 75,0% [58,9–86,2] | **77,8% [61,9–88,3]** | **77,8% [61,9–88,3] (L3)** |
| qwen2.5:7b | 63,9% [47,6–77,5] | 66,7% [50,3–79,8] | 77,8% [61,9–88,3] | 77,8% [61,9–88,3] | 86,1% [71,3–93,9] | **88,9% [74,7–95,6] (L1)** |
| **Média** | 32,5% (7 modelos) | 28,5% (8 modelos) | 56,0% (6 modelos) | 75,7% (4 modelos) | 79,2% (4 modelos) | 79,9% (4 modelos) |
<!-- /tabela:cf_acerto_36 -->

## cf_balanceada_36

<!-- tabela:cf_balanceada_36 -->
| Modelo | 2-A linear (Ryzen) | 2-B A0 | 2-B A2 | F3 L0 | F3 L3 | F3 melhor |
|---|---|---|---|---|---|---|
| granite4.2:8b | 72,9% | 70,8% | **83,3%** | **83,3%** | **83,3%** | **83,3% (L0)** |
| phi4-mini:3.8b | **35,8%** | 30,8% | 28,3% | — | — | — |
| qwen2.5-coder:1.5b | 0,0% | 0,0% | **10,0%** | — | — | — |
| qwen2.5-coder:1.5b-instruct-fp16 | — | **5,0%** | — | — | — | — |
| qwen2.5-coder:1.5b-instruct-q8_0 | 0,0% | **5,0%** | — | — | — | — |
| qwen2.5-coder:3b | 23,3% | 23,3% | 68,8% | 68,8% | **71,2%** | **71,2% (L2)** |
| qwen2.5-coder:7b | 50,4% | 48,3% | 77,5% | 80,0% | **84,2%** | **84,2% (L3)** |
| qwen2.5:7b | 65,0% | 66,7% | 81,2% | 81,2% | 86,2% | **91,7% (L1)** |
| **Média** | 35,3% (7 modelos) | 31,2% (8 modelos) | 58,2% (6 modelos) | 78,3% (4 modelos) | 81,2% (4 modelos) | 82,6% (4 modelos) |

_Acerto = causa raiz correta, com IC de Wilson a 95%; acurácia balanceada = média do acerto por causa raiz presente no recorte (avaliar_fase3.acuracia_balanceada), a métrica primária do trabalho. **F3 melhor** = a versão da biblioteca (L0..L3) com a maior acurácia balanceada do modelo (em empate, a mais baixa) — a mesma versão nas tabelas de acerto e de acurácia balanceada. A média do rodapé diz quantos modelos entram em cada coluna quando o número difere entre elas._
<!-- /tabela:cf_balanceada_36 -->

## cf_custo

<!-- tabela:cf_custo -->
| Modelo | 2-A linear (Ryzen)* | 2-B A0 | 2-B A2 | F3 L0 | F3 L3 |
|---|---|---|---|---|---|
| granite4.2:8b | **45,7** s / **192** tok | 83,0 s / 197 tok | 123,9 s / 214 tok | 131,3 s / 233 tok | 132,6 s / 225 tok |
| phi4-mini:3.8b | **9,8** s / **41** tok | 22,6 s / 42 tok | 35,6 s / 77 tok | — | — |
| qwen2.5-coder:1.5b | **5,2** s / **90** tok | 8,3 s / 112 tok | 25,3 s / 228 tok | — | — |
| qwen2.5-coder:1.5b-instruct-fp16 | — | **17,0** s / **74** tok | — | — | — |
| qwen2.5-coder:1.5b-instruct-q8_0 | **8,6** s / **63** tok | 15,9 s / 95 tok | — | — | — |
| qwen2.5-coder:3b | **8,4** s / **50** tok | 17,1 s / 51 tok | 29,7 s / 56 tok | 30,8 s / 56 tok | 18,4 s / 56 tok |
| qwen2.5-coder:7b | **25,9** s / 106 tok | 51,3 s / 107 tok | 66,6 s / 87 tok | 68,7 s / **82** tok | 49,8 s / 90 tok |
| qwen2.5:7b | **17,1** s / **52** tok | 38,0 s / 54 tok | 61,1 s / 63 tok | 66,8 s / 62 tok | 47,0 s / 63 tok |
<!-- /tabela:cf_custo -->

## cf_riscos

<!-- tabela:cf_riscos -->
| Modelo | Fora do conjunto % | Formato ok / conteúdo errado % | Adesão cega A5 % | Teto A3 % | Tentativas de decorar (F3) | Autoenvenenamento L2→L3 (F3, 36 casos) % |
|---|---|---|---|---|---|---|
| granite4.2:8b | **0,0%** | 24,4% | 93,3% | **100,0%** | **0** | **0,0%** |
| phi4-mini:3.8b | 15,6% | 64,4% | **30,0%** | 51,1% | — | — |
| qwen2.5-coder:1.5b | **0,0%** | 83,3% | — | — | — | — |
| qwen2.5-coder:1.5b-instruct-fp16 | **0,0%** | 91,1% | — | — | — | — |
| qwen2.5-coder:1.5b-instruct-q8_0 | **0,0%** | 91,1% | — | — | — | — |
| qwen2.5-coder:3b | 2,2% | 32,2% | 95,6% | 92,2% | **0** | 2,8% |
| qwen2.5-coder:7b | **0,0%** | 24,4% | — | — | **0** | 2,8% |
| qwen2.5:7b | 3,3% | **22,2%** | — | — | **0** | 2,8% |
<!-- /tabela:cf_riscos -->

## cf_pareamentos

<!-- tabela:cf_pareamentos -->
_Sem negrito nesta tabela: cada linha compara duas fases diferentes do MESMO modelo (ex.: 2-B A2 × Fase 3 L0) -- não há "melhor valor" entre `a` e `b`, só um Δ e um p que dizem se a diferença é grande e se é distinguível do acaso._

| Modelo | a | b | Conjunto | n | Δ pp | b/c | p | Pareável? |
|---|---|---|---|---|---|---|---|---|
| granite4.2:8b | 2A_linear_ryzen | 2B_A0 | 90 | 90 | -1,1 | 2/3 | 1,0000 | acerto sim; tempo não (máquina diferente) |
| granite4.2:8b | 2B_A0 | 2B_A2 | 90 | 90 | 10,0 | 18/9 | 0,1221 | acerto sim; tempo sim |
| granite4.2:8b | 2B_A2 | F3_L0 | 86 | 86 | 0,0 | 0/0 | 1,0000 | acerto sim; tempo sim |
| granite4.2:8b | 2B_A2 | F3_L0 | 36 | 36 | 0,0 | 0/0 | 1,0000 | acerto sim; tempo sim |
| granite4.2:8b | F3_L0 | F3_L3 | 36 | 36 | 0,0 | 0/0 | 1,0000 | acerto sim; tempo sim |
| granite4.2:8b | F3_L0 | F3_L3 | 54 | 54 | -1,9 | 0/1 | 1,0000 | acerto sim; tempo sim |
| qwen2.5-coder:3b | 2A_linear_ryzen | 2B_A0 | 90 | 90 | -2,3 | 0/2 | 0,5000 | acerto sim; tempo não (máquina diferente) |
| qwen2.5-coder:3b | 2B_A0 | 2B_A2 | 90 | 90 | 40,0 | 36/0 | 0,0000* | acerto sim; tempo sim |
| qwen2.5-coder:3b | 2B_A2 | F3_L0 | 86 | 86 | 0,0 | 0/0 | 1,0000 | acerto sim; tempo sim |
| qwen2.5-coder:3b | 2B_A2 | F3_L0 | 36 | 36 | 0,0 | 0/0 | 1,0000 | acerto sim; tempo sim |
| qwen2.5-coder:3b | F3_L0 | F3_L3 | 36 | 36 | 2,8 | 1/0 | 1,0000 | acerto sim; tempo sim |
| qwen2.5-coder:3b | F3_L0 | F3_L3 | 54 | 54 | 1,8 | 2/1 | 1,0000 | acerto sim; tempo sim |
| qwen2.5-coder:7b | 2A_linear_ryzen | 2B_A0 | 90 | 90 | 1,1 | 8/7 | 1,0000 | acerto sim; tempo não (máquina diferente) |
| qwen2.5-coder:7b | 2B_A0 | 2B_A2 | 90 | 90 | 22,2 | 26/6 | 0,0005* | acerto sim; tempo sim |
| qwen2.5-coder:7b | 2B_A2 | F3_L0 | 86 | 86 | -1,2 | 2/3 | 1,0000 | acerto sim; tempo sim |
| qwen2.5-coder:7b | 2B_A2 | F3_L0 | 36 | 36 | 2,8 | 1/0 | 1,0000 | acerto sim; tempo sim |
| qwen2.5-coder:7b | F3_L0 | F3_L3 | 36 | 36 | 2,8 | 3/2 | 1,0000 | acerto sim; tempo sim |
| qwen2.5-coder:7b | F3_L0 | F3_L3 | 54 | 54 | 0,0 | 6/6 | 1,0000 | acerto sim; tempo sim |
| qwen2.5:7b | 2A_linear_ryzen | 2B_A0 | 90 | 90 | 4,5 | 4/0 | 0,1250 | acerto sim; tempo não (máquina diferente) |
| qwen2.5:7b | 2B_A0 | 2B_A2 | 90 | 90 | 12,2 | 21/10 | 0,0708 | acerto sim; tempo sim |
| qwen2.5:7b | 2B_A2 | F3_L0 | 86 | 86 | 0,0 | 0/0 | 1,0000 | acerto sim; tempo sim |
| qwen2.5:7b | 2B_A2 | F3_L0 | 36 | 36 | 0,0 | 0/0 | 1,0000 | acerto sim; tempo sim |
| qwen2.5:7b | F3_L0 | F3_L3 | 36 | 36 | 8,3 | 3/0 | 0,2500 | acerto sim; tempo sim |
| qwen2.5:7b | F3_L0 | F3_L3 | 54 | 54 | 5,5 | 5/2 | 0,4531 | acerto sim; tempo sim |
| phi4-mini:3.8b | 2A_linear_ryzen | 2B_A0 | 90 | 90 | 0,0 | 1/1 | 1,0000 | acerto sim; tempo não (máquina diferente) |
| phi4-mini:3.8b | 2B_A0 | 2B_A2 | 90 | 90 | 2,3 | 8/6 | 0,7905 | acerto sim; tempo sim |
| qwen2.5-coder:1.5b | 2A_linear_ryzen | 2B_A0 | 90 | 90 | 0,0 | 0/0 | 1,0000 | acerto sim; tempo não (máquina diferente) |
| qwen2.5-coder:1.5b | 2B_A0 | 2B_A2 | 90 | 90 | 11,1 | 10/0 | 0,0020* | acerto sim; tempo sim |
| qwen2.5-coder:1.5b-instruct-q8_0 | 2A_linear_ryzen | 2B_A0 | 90 | 48 | 0,0 | 0/0 | 1,0000 | acerto sim; tempo não (máquina diferente) |
<!-- /tabela:cf_pareamentos -->

## cf_leitura

<!-- tabela:cf_leitura -->
Fase 2-A: melhor modelo granite4.2:8b, 67,8% de acerto (braço linear, Ryzen, sem biblioteca).

Fase 2-B: melhor modelo granite4.2:8b, 76,7% em A2 (com recuperação); ganho médio de A0 para A2 de 16,3 pp (média sobre os modelos com pareamento nos 90 casos).

Fase 3: melhor modelo qwen2.5:7b, 83,0% de acurácia balanceada em L1 (acerto simples 76,7%); ganho médio de L0 para L3 nos 36 casos de avaliação de 3,5 pp. Risco: adesão cega média de 73,0% em A5 (2-B), autoenvenenamento médio de 2,1% na transição L2→L3 nos 36 casos de avaliação. Perda: 57,0 s/caso em 2-B A2 contra 61,9 s/caso em F3 L3.
<!-- /tabela:cf_leitura -->

## dm_regra_36

<!-- tabela:dm_regra_36 -->
Ranking por acurácia balanceada nos 36 casos de avaliação; veto quando o autoenvenenamento máximo do modelo (qualquer transição, nos 36) passa de 10,0%. Em empate, prevalece a licença mais permissiva (Apache-2.0 antes de MIT, antes das demais — decisão 36; os quatro modelos da Fase 3 são Apache-2.0, então o critério não separa ninguém hoje) e, persistindo o empate, a época (L) mais baixa -- mesmo critério de `comparar_fases._melhor_f3`: a ordem de iteração é L0..L3 e o máximo preserva o primeiro encontrado, porque afirmar que uma época mais tardia é melhor sem uma diferença medida não é uma alegação que o número sustenta; em empate remanescente (mesma época, modelos diferentes), o nome do modelo desempata só para o ranking sair sempre igual entre corridas.

| Modelo | L | Acurácia balanceada (36) | Acerto (36) | n | Autoenvenenamento máx. (36) | Vetado |
|---|---|---|---|---|---|---|
| qwen2.5:7b | L1 | 91,7% | 88,9% | 36 | 5,6% | não |
| qwen2.5:7b | L3 | 86,2% | 86,1% | 36 | 5,6% | não |
| qwen2.5:7b | L2 | 84,2% | 83,3% | 36 | 5,6% | não |
| qwen2.5-coder:7b | L3 | 84,2% | 77,8% | 36 | 2,8% | não |
| granite4.2:8b | L0 | 83,3% | 80,6% | 36 | 0,0% | não |
| granite4.2:8b | L1 | 83,3% | 80,6% | 36 | 0,0% | não |
| granite4.2:8b | L2 | 83,3% | 80,6% | 36 | 0,0% | não |
| granite4.2:8b | L3 | 83,3% | 80,6% | 36 | 0,0% | não |
| qwen2.5:7b | L0 | 81,2% | 77,8% | 36 | 5,6% | não |
| qwen2.5-coder:7b | L0 | 80,0% | 75,0% | 36 | 2,8% | não |
| qwen2.5-coder:7b | L1 | 80,0% | 75,0% | 36 | 2,8% | não |
| qwen2.5-coder:7b | L2 | 80,0% | 75,0% | 36 | 2,8% | não |
| qwen2.5-coder:3b | L2 | 71,2% | 72,2% | 36 | 2,8% | não |
| qwen2.5-coder:3b | L3 | 71,2% | 72,2% | 36 | 2,8% | não |
| qwen2.5-coder:3b | L1 | 70,4% | 72,2% | 36 | 2,8% | não |
| qwen2.5-coder:3b | L0 | 68,8% | 69,4% | 36 | 2,8% | não |

**Vencedor da regra 36:** qwen2.5:7b / L1 (91,7% de acurácia balanceada).
<!-- /tabela:dm_regra_36 -->

## dm_bootstrap

<!-- tabela:dm_bootstrap -->
IC 95% percentil da acurácia balanceada e P(top-1) = fração das réplicas em que o (modelo, L) tem a maior acurácia balanceada entre todos os candidatos da réplica.

### Nos 36 casos de avaliação

| Modelo | L | IC 95% bootstrap | P(top-1) |
|---|---|---|---|
| qwen2.5:7b | L1 | [81,9–97,8]% | 77,6% |
| qwen2.5:7b | L3 | [75,0–96,7]% | 15,2% |
| granite4.2:8b | L0 | [70,6–92,8]% | 5,8% |
| qwen2.5-coder:7b | L3 | [70,0–91,1]% | 0,5% |
| qwen2.5-coder:3b | L2 | [58,2–85,6]% | 0,2% |
| qwen2.5-coder:7b | L0 | [66,7–88,9]% | 0,2% |
| qwen2.5:7b | L0 | [67,7–91,2]% | 0,2% |
| qwen2.5-coder:3b | L1 | [58,3–84,4]% | 0,1% |
| qwen2.5-coder:3b | L0 | [55,4–82,4]% | 0,1% |
| granite4.2:8b | L1 | [70,6–92,8]% | 0,0% |
| granite4.2:8b | L2 | [70,6–92,8]% | 0,0% |
| granite4.2:8b | L3 | [70,6–92,8]% | 0,0% |
| qwen2.5-coder:3b | L3 | [57,7–85,5]% | 0,0% |
| qwen2.5-coder:7b | L1 | [66,7–88,9]% | 0,0% |
| qwen2.5-coder:7b | L2 | [67,7–88,9]% | 0,0% |
| qwen2.5:7b | L2 | [72,2–94,0]% | 0,0% |

### Nos 90 casos

| Modelo | L | IC 95% bootstrap | P(top-1) |
|---|---|---|---|
| qwen2.5:7b | L1 | [75,9–88,3]% | 50,0% |
| qwen2.5:7b | L3 | [73,7–87,5]% | 17,2% |
| granite4.2:8b | L1 | [72,0–87,0]% | 12,2% |
| qwen2.5-coder:7b | L1 | [70,5–85,8]% | 9,8% |
| granite4.2:8b | L0 | [71,4–86,4]% | 4,8% |
| qwen2.5-coder:7b | L2 | [69,4–84,4]% | 3,7% |
| qwen2.5-coder:7b | L3 | [66,3–82,8]% | 1,0% |
| qwen2.5:7b | L0 | [67,4–82,8]% | 0,4% |
| qwen2.5-coder:3b | L3 | [62,8–81,1]% | 0,2% |
| qwen2.5-coder:7b | L0 | [67,6–82,7]% | 0,2% |
| qwen2.5:7b | L2 | [70,6–85,2]% | 0,2% |
| qwen2.5-coder:3b | L2 | [62,3–80,3]% | 0,1% |
| qwen2.5-coder:3b | L1 | [63,7–79,5]% | 0,1% |
| granite4.2:8b | L2 | [69,6–85,2]% | 0,0% |
| granite4.2:8b | L3 | [70,8–85,8]% | 0,0% |
| qwen2.5-coder:3b | L0 | [62,3–78,8]% | 0,0% |
<!-- /tabela:dm_bootstrap -->

## dm_estabilidade

<!-- tabela:dm_estabilidade -->
36 cortes (por coluna de comparacao_fases.json nos 36/90 casos, e por classe de defeito nos 90 casos -- resumo_fase3.json não desmembra a classe por partição), cada um com o ranking dos modelos por acurácia balanceada; abaixo, em quantos cortes cada modelo ficou em 1º.

| Modelo | Nº de cortes em 1º (de 36) |
|---|---|
| granite4.2:8b | 16 |
| qwen2.5:7b | 14 |
| qwen2.5-coder:7b | 5 |
| qwen2.5-coder:3b | 1 |
<!-- /tabela:dm_estabilidade -->

## dm_pareto

<!-- tabela:dm_pareto -->
Maximizando acurácia balanceada (36) e minimizando segundos (mediana, 36) e risco (média simples de autoenvenenamento máximo, adesão cega, fora do conjunto e formato-ok-conteúdo-errado); 16 candidatos com os três números disponíveis (0 excluídos por dado incompleto). Não dominado = nenhum outro (modelo, L) é ao mesmo tempo mais certeiro, mais barato e menos arriscado.

| Modelo | L | Acurácia balanceada (36) | Segundos (mediana, 36) | Risco | Vetado |
|---|---|---|---|---|---|
| qwen2.5-coder:3b | L1 | 70,4% | 17,8 | 31,6 | não |
| qwen2.5-coder:3b | L2 | 71,2% | 18,8 | 31,6 | não |
| qwen2.5:7b | L1 | 91,7% | 79,5 | 5,6 | não |
| qwen2.5:7b | L3 | 86,2% | 53,9 | 7,4 | não |
<!-- /tabela:dm_pareto -->

## dm_escore

<!-- tabela:dm_escore -->
Pesos declarados em pesos_decisao.json (normalização mín-máx por critério; custo e risco invertidos, para 'menor' virar 'melhor'): acuracia_balanceada_36=0,5, acerto_36=0,1, custo_segundos=0,2, risco=0,2.

| Modelo | L | Score | Vetado |
|---|---|---|---|
| qwen2.5:7b | L1 | 0,9 | não |
| qwen2.5:7b | L3 | 0,8 | não |
| qwen2.5-coder:7b | L3 | 0,7 | não |
| qwen2.5:7b | L2 | 0,7 | não |
| qwen2.5:7b | L0 | 0,6 | não |
| qwen2.5-coder:7b | L1 | 0,6 | não |
| qwen2.5-coder:7b | L2 | 0,6 | não |
| qwen2.5-coder:7b | L0 | 0,5 | não |
| granite4.2:8b | L0 | 0,4 | não |
| granite4.2:8b | L2 | 0,4 | não |
| granite4.2:8b | L1 | 0,4 | não |
| granite4.2:8b | L3 | 0,4 | não |
| qwen2.5-coder:3b | L2 | 0,3 | não |
| qwen2.5-coder:3b | L3 | 0,3 | não |
| qwen2.5-coder:3b | L1 | 0,3 | não |
| qwen2.5-coder:3b | L0 | 0,2 | não |

**Vencedor do escore ponderado:** qwen2.5:7b / L1 (score 0,9).

**Sensibilidade** (varredura de 0 a 1 em passos de 0,05, renormalizando os demais pesos): em que peso o vencedor muda.

- `acuracia_balanceada_36`: peso 0,15 -- qwen2.5:7b/L3 passa a qwen2.5:7b/L1.
- `acerto_36`: o vencedor não muda em toda a varredura.
- `custo_segundos`: peso 0,50 -- qwen2.5:7b/L1 passa a qwen2.5:7b/L3; peso 0,75 -- qwen2.5:7b/L3 passa a qwen2.5-coder:3b/L1.
- `risco`: o vencedor não muda em toda a varredura.
<!-- /tabela:dm_escore -->

## dm_3b

<!-- tabela:dm_3b -->
### fase3b_ponte (modo `ponte`)

| Modelo | L | n | Acerto | Acurácia balanceada | n comuns c/ F3 | b | c | p (McNemar) | p (Holm) | g de Cohen |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen2.5-coder:3b | L0 | 36 | 69,4% | 68,8% | 36 | 0 | 0 | 1,0000 | 1,0000 | — |
| qwen2.5-coder:7b | L0 | 36 | 75,0% | 80,0% | 36 | 0 | 0 | 1,0000 | 1,0000 | — |
| qwen2.5:7b | L0 | 36 | 77,8% | 78,8% | 36 | 1 | 1 | 1,0000 | 1,0000 | 0,0 |
<!-- /tabela:dm_3b -->

## dm_revisao

<!-- tabela:dm_revisao -->
Fonte: planilhas revisao_edicoes__<slug>.md lidas direto da pasta da corrida.

| Modelo | n | Correta | Parcial | Errada | Sem avaliação |
|---|---|---|---|---|---|
| qwen2.5-coder:3b | 10 | 40,0% | 20,0% | 40,0% | 0,0% |
| qwen2.5-coder:7b | 24 | 41,7% | 29,2% | 29,2% | 0,0% |
| qwen2.5:7b | 29 | 31,0% | 27,6% | 41,4% | 0,0% |
<!-- /tabela:dm_revisao -->

## dm_frase

<!-- tabela:dm_frase -->
Pela regra pré-registrada (passo 1), o modelo recomendado para produção é **qwen2.5:7b** com a biblioteca no estado **L1** (91,7% de acurácia balanceada nos 36 casos de avaliação, sem veto por autoenvenenamento). O escore ponderado (passo 5) concorda com essa escolha.

A fronteira de Pareto (passo 4) tem 4 combinação(ões) não dominada(s). A varredura de sensibilidade (passo 5) trocou o vencedor em 3 ponto(s) dos pesos varridos.
<!-- /tabela:dm_frase -->

## curva_acerto

<!-- tabela:curva_acerto -->
| Modelo | L0 (36) | L1 (36) | L2 (36) | L3 (36) | L0 (54) | L1 (54) | L2 (54) | L3 (54) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | 80,6% | 80,6% | 80,6% | 80,6% | 74,1% | 75,9% | 70,4% | 72,2% |
| `qwen2.5-coder:7b` | 75,0% | 75,0% | 75,0% | 77,8% | 68,5% | 74,1% | 72,2% | 68,5% |
| `qwen2.5:7b` | 77,8% | 88,9% | 83,3% | 86,1% | 66,7% | 68,5% | 68,5% | 72,2% |
| `qwen2.5-coder:3b` | 69,4% | 72,2% | 72,2% | 72,2% | 63,0% | 63,0% | 63,0% | 64,8% |
<!-- /tabela:curva_acerto -->

## curva_balanceada

<!-- tabela:curva_balanceada -->
| Modelo | L0 (36) | L1 (36) | L2 (36) | L3 (36) | L0 (54) | L1 (54) | L2 (54) | L3 (54) | L0 (90) | L1 (90) | L2 (90) | L3 (90) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | 83,3% | 83,3% | 83,3% | 83,3% | 76,4% | 77,2% | 73,7% | 75,2% | 79,6% | 80,2% | 78,0% | 78,7% |
| `qwen2.5-coder:7b` | 80,0% | 80,0% | 80,0% | 84,2% | 73,7% | 82,1% | 74,4% | 69,9% | 75,8% | 78,9% | 77,8% | 75,4% |
| `qwen2.5:7b` | 81,2% | 91,7% | 84,2% | 86,2% | 74,1% | 79,3% | 74,3% | 76,4% | 75,7% | 83,0% | 78,1% | 80,7% |
| `qwen2.5-coder:3b` | 68,8% | 70,4% | 71,2% | 71,2% | 70,3% | 70,3% | 69,5% | 70,3% | 71,5% | 72,6% | 72,0% | 72,6% |
<!-- /tabela:curva_balanceada -->

## qualidade

<!-- tabela:qualidade -->
| Modelo | L | Rótulo mais frequente (parcela) | Rótulos distintos | Formato ok / conteúdo errado | Fora do conjunto | Citou verbete | Ouro no contexto | Contexto com nota | Verbete novo no contexto |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | L0 | `localizador_quebrado` (11,1%) | 20 | 19,4% | 0,0% | 100,0% | 86,1% | 0,0% | 0,0% |
| `granite4.2:8b` | L1 | `localizador_quebrado` (11,1%) | 20 | 19,4% | 0,0% | 100,0% | 86,1% | 0,0% | 0,0% |
| `granite4.2:8b` | L2 | `campo_renomeado` (11,1%) | 20 | 19,4% | 0,0% | 100,0% | 86,1% | 0,0% | 0,0% |
| `granite4.2:8b` | L3 | `localizador_quebrado` (11,1%) | 20 | 19,4% | 0,0% | 100,0% | 86,1% | 0,0% | 0,0% |
| `qwen2.5-coder:7b` | L0 | `estrutura_aninhada_divergente` (11,1%) | 19 | 25,0% | 2,8% | 100,0% | 86,1% | 0,0% | 0,0% |
| `qwen2.5-coder:7b` | L1 | `estrutura_aninhada_divergente` (11,1%) | 19 | 25,0% | 2,8% | 100,0% | 86,1% | 72,2% | 0,0% |
| `qwen2.5-coder:7b` | L2 | `estrutura_aninhada_divergente` (13,9%) | 19 | 25,0% | 2,8% | 100,0% | 83,3% | 100,0% | 0,0% |
| `qwen2.5-coder:7b` | L3 | `estrutura_aninhada_divergente` (13,9%) | 19 | 22,2% | 0,0% | 100,0% | 86,1% | 100,0% | 0,0% |
| `qwen2.5:7b` | L0 | `codificacao_incorreta` (8,3%) | 20 | 22,2% | 2,8% | 100,0% | 86,1% | 0,0% | 0,0% |
| `qwen2.5:7b` | L1 | `localizador_quebrado` (11,1%) | 20 | 11,1% | 0,0% | 100,0% | 83,3% | 94,4% | 0,0% |
| `qwen2.5:7b` | L2 | `localizador_quebrado` (11,1%) | 21 | 16,7% | 2,8% | 100,0% | 83,3% | 94,4% | 0,0% |
| `qwen2.5:7b` | L3 | `campo_ausente` (8,3%) | 20 | 13,9% | 2,8% | 100,0% | 86,1% | 94,4% | 0,0% |
| `qwen2.5-coder:3b` | L0 | `campo_ausente` (19,4%) | 18 | 30,6% | 0,0% | 100,0% | 86,1% | 0,0% | 0,0% |
| `qwen2.5-coder:3b` | L1 | `campo_ausente` (19,4%) | 18 | 27,8% | 0,0% | 100,0% | 86,1% | 8,3% | 0,0% |
| `qwen2.5-coder:3b` | L2 | `campo_ausente` (16,7%) | 18 | 27,8% | 0,0% | 100,0% | 86,1% | 36,1% | 0,0% |
| `qwen2.5-coder:3b` | L3 | `campo_ausente` (16,7%) | 18 | 27,8% | 0,0% | 100,0% | 86,1% | 50,0% | 0,0% |
<!-- /tabela:qualidade -->

## por_classe

<!-- tabela:por_classe -->
| Modelo | Classe (n) | L0 | L1 | L2 | L3 |
| --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | 1 lexica (15) | 86,7% | 86,7% | 86,7% | 86,7% |
| `granite4.2:8b` | 2 sintatica (15) | 93,3% | 93,3% | 86,7% | 93,3% |
| `granite4.2:8b` | 3 semantica (15) | 73,3% | 73,3% | 73,3% | 73,3% |
| `granite4.2:8b` | 4 traducao (15) | 33,3% | 33,3% | 26,7% | 26,7% |
| `granite4.2:8b` | 5 runtime (15) | 93,3% | 93,3% | 93,3% | 93,3% |
| `granite4.2:8b` | 6 efeito (15) | 80,0% | 86,7% | 80,0% | 80,0% |
| `qwen2.5-coder:7b` | 1 lexica (15) | 93,3% | 93,3% | 93,3% | 86,7% |
| `qwen2.5-coder:7b` | 2 sintatica (15) | 80,0% | 80,0% | 73,3% | 66,7% |
| `qwen2.5-coder:7b` | 3 semantica (15) | 60,0% | 66,7% | 73,3% | 73,3% |
| `qwen2.5-coder:7b` | 4 traducao (15) | 26,7% | 40,0% | 33,3% | 33,3% |
| `qwen2.5-coder:7b` | 5 runtime (15) | 93,3% | 93,3% | 93,3% | 86,7% |
| `qwen2.5-coder:7b` | 6 efeito (15) | 73,3% | 73,3% | 73,3% | 86,7% |
| `qwen2.5:7b` | 1 lexica (15) | 86,7% | 86,7% | 80,0% | 86,7% |
| `qwen2.5:7b` | 2 sintatica (15) | 73,3% | 80,0% | 73,3% | 80,0% |
| `qwen2.5:7b` | 3 semantica (15) | 80,0% | 80,0% | 86,7% | 86,7% |
| `qwen2.5:7b` | 4 traducao (15) | 46,7% | 46,7% | 53,3% | 60,0% |
| `qwen2.5:7b` | 5 runtime (15) | 80,0% | 100,0% | 86,7% | 86,7% |
| `qwen2.5:7b` | 6 efeito (15) | 60,0% | 66,7% | 66,7% | 66,7% |
| `qwen2.5-coder:3b` | 1 lexica (15) | 73,3% | 73,3% | 86,7% | 80,0% |
| `qwen2.5-coder:3b` | 2 sintatica (15) | 80,0% | 80,0% | 80,0% | 80,0% |
| `qwen2.5-coder:3b` | 3 semantica (15) | 53,3% | 53,3% | 60,0% | 66,7% |
| `qwen2.5-coder:3b` | 4 traducao (15) | 40,0% | 46,7% | 40,0% | 40,0% |
| `qwen2.5-coder:3b` | 5 runtime (15) | 93,3% | 93,3% | 86,7% | 86,7% |
| `qwen2.5-coder:3b` | 6 efeito (15) | 53,3% | 53,3% | 46,7% | 53,3% |
<!-- /tabela:por_classe -->

## por_nivel

<!-- tabela:por_nivel -->
| Modelo | Nível (n) | L0 | L1 | L2 | L3 |
| --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | 1 facil (30) | 73,3% | 73,3% | 73,3% | 73,3% |
| `granite4.2:8b` | 2 medio (30) | 76,7% | 76,7% | 76,7% | 76,7% |
| `granite4.2:8b` | 3 dificil (30) | 80,0% | 83,3% | 73,3% | 76,7% |
| `qwen2.5-coder:7b` | 1 facil (30) | 66,7% | 63,3% | 73,3% | 80,0% |
| `qwen2.5-coder:7b` | 2 medio (30) | 76,7% | 80,0% | 76,7% | 73,3% |
| `qwen2.5-coder:7b` | 3 dificil (30) | 70,0% | 80,0% | 70,0% | 63,3% |
| `qwen2.5:7b` | 1 facil (30) | 66,7% | 76,7% | 80,0% | 80,0% |
| `qwen2.5:7b` | 2 medio (30) | 73,3% | 76,7% | 73,3% | 80,0% |
| `qwen2.5:7b` | 3 dificil (30) | 73,3% | 76,7% | 70,0% | 73,3% |
| `qwen2.5-coder:3b` | 1 facil (30) | 66,7% | 66,7% | 63,3% | 66,7% |
| `qwen2.5-coder:3b` | 2 medio (30) | 63,3% | 63,3% | 70,0% | 70,0% |
| `qwen2.5-coder:3b` | 3 dificil (30) | 66,7% | 70,0% | 66,7% | 66,7% |
<!-- /tabela:por_nivel -->

## pareado

<!-- tabela:pareado -->
| Modelo | Partição (n) | L1 vs L0 | L2 vs L0 | L3 vs L0 | Q de Cochran (L0..L3) |
| --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | avaliacao (36) | 80,6%→80,6% (Δ 0,0 pp; b/c 0/0; p 1,0000; Holm 1,0000; g —) | 80,6%→80,6% (Δ 0,0 pp; b/c 0/0; p 1,0000; Holm 1,0000; g —) | 80,6%→80,6% (Δ 0,0 pp; b/c 0/0; p 1,0000; Holm 1,0000; g —) | Q 0,0, gl 3, p 1,0000 |
| `granite4.2:8b` | aprendizado (54) | 74,1%→75,9% (Δ 1,8 pp; b/c 1/0; p 1,0000; Holm 1,0000; g 0,5) | 74,1%→70,4% (Δ -3,7 pp; b/c 0/2; p 0,5000; Holm 1,0000; g -0,5) | 74,1%→72,2% (Δ -1,9 pp; b/c 0/1; p 1,0000; Holm 1,0000; g -0,5) | Q 6,0, gl 3, p 0,1116 |
| `granite4.2:8b` | todos (90) | 76,7%→77,8% (Δ 1,1 pp; b/c 1/0; p 1,0000; Holm 1,0000; g 0,5) | 76,7%→74,4% (Δ -2,3 pp; b/c 0/2; p 0,5000; Holm 1,0000; g -0,5) | 76,7%→75,6% (Δ -1,1 pp; b/c 0/1; p 1,0000; Holm 1,0000; g -0,5) | Q 6,0, gl 3, p 0,1116 |
| `qwen2.5-coder:7b` | avaliacao (36) | 75,0%→75,0% (Δ 0,0 pp; b/c 0/0; p 1,0000; Holm 1,0000; g —) | 75,0%→75,0% (Δ 0,0 pp; b/c 1/1; p 1,0000; Holm 1,0000; g 0,0) | 75,0%→77,8% (Δ 2,8 pp; b/c 3/2; p 1,0000; Holm 1,0000; g 0,1) | Q 0,5, gl 3, p 0,9124 |
| `qwen2.5-coder:7b` | aprendizado (54) | 68,5%→74,1% (Δ 5,6 pp; b/c 4/1; p 0,3750; Holm 1,0000; g 0,3) | 68,5%→72,2% (Δ 3,7 pp; b/c 4/2; p 0,6875; Holm 1,0000; g 0,2) | 68,5%→68,5% (Δ 0,0 pp; b/c 6/6; p 1,0000; Holm 1,0000; g 0,0) | Q 1,6, gl 3, p 0,6621 |
| `qwen2.5-coder:7b` | todos (90) | 71,1%→74,4% (Δ 3,3 pp; b/c 4/1; p 0,3750; Holm 1,0000; g 0,3) | 71,1%→73,3% (Δ 2,2 pp; b/c 5/3; p 0,7266; Holm 1,0000; g 0,1) | 71,1%→72,2% (Δ 1,1 pp; b/c 9/8; p 1,0000; Holm 1,0000; g 0,0) | Q 0,9, gl 3, p 0,8297 |
| `qwen2.5:7b` | avaliacao (36) | 77,8%→88,9% (Δ 11,1 pp; b/c 4/0; p 0,1250; Holm 0,3750; g 0,5) | 77,8%→83,3% (Δ 5,5 pp; b/c 2/0; p 0,5000; Holm 0,5000; g 0,5) | 77,8%→86,1% (Δ 8,3 pp; b/c 3/0; p 0,2500; Holm 0,5000; g 0,5) | Q 5,5, gl 3, p 0,1371 |
| `qwen2.5:7b` | aprendizado (54) | 66,7%→68,5% (Δ 1,8 pp; b/c 3/2; p 1,0000; Holm 1,0000; g 0,1) | 66,7%→68,5% (Δ 1,8 pp; b/c 4/3; p 1,0000; Holm 1,0000; g 0,1) | 66,7%→72,2% (Δ 5,5 pp; b/c 5/2; p 0,4531; Holm 1,0000; g 0,2) | Q 1,7, gl 3, p 0,6309 |
| `qwen2.5:7b` | todos (90) | 71,1%→76,7% (Δ 5,6 pp; b/c 7/2; p 0,1797; Holm 0,3594; g 0,3) | 71,1%→74,4% (Δ 3,3 pp; b/c 6/3; p 0,5078; Holm 0,5078; g 0,2) | 71,1%→77,8% (Δ 6,7 pp; b/c 8/2; p 0,1094; Holm 0,3282; g 0,3) | Q 4,8, gl 3, p 0,1834 |
| `qwen2.5-coder:3b` | avaliacao (36) | 69,4%→72,2% (Δ 2,8 pp; b/c 1/0; p 1,0000; Holm 1,0000; g 0,5) | 69,4%→72,2% (Δ 2,8 pp; b/c 2/1; p 1,0000; Holm 1,0000; g 0,2) | 69,4%→72,2% (Δ 2,8 pp; b/c 1/0; p 1,0000; Holm 1,0000; g 0,5) | Q 0,8, gl 3, p 0,8451 |
| `qwen2.5-coder:3b` | aprendizado (54) | 63,0%→63,0% (Δ 0,0 pp; b/c 0/0; p 1,0000; Holm 1,0000; g —) | 63,0%→63,0% (Δ 0,0 pp; b/c 2/2; p 1,0000; Holm 1,0000; g 0,0) | 63,0%→64,8% (Δ 1,8 pp; b/c 2/1; p 1,0000; Holm 1,0000; g 0,2) | Q 0,5, gl 3, p 0,9124 |
| `qwen2.5-coder:3b` | todos (90) | 65,6%→66,7% (Δ 1,1 pp; b/c 1/0; p 1,0000; Holm 1,0000; g 0,5) | 65,6%→66,7% (Δ 1,1 pp; b/c 4/3; p 1,0000; Holm 1,0000; g 0,1) | 65,6%→67,8% (Δ 2,2 pp; b/c 3/1; p 0,6250; Holm 1,0000; g 0,2) | Q 0,9, gl 3, p 0,8358 |
<!-- /tabela:pareado -->

## flips

<!-- tabela:flips -->
| Modelo | Partição (n) | L0→L1: ✓→✗ / ✗→✓ (autoenv.) | L1→L2: ✓→✗ / ✗→✓ (autoenv.) | L2→L3: ✓→✗ / ✗→✓ (autoenv.) |
| --- | --- | --- | --- | --- |
| `granite4.2:8b` | avaliacao (36) | 0 / 0 (0,0%) | 0 / 0 (0,0%) | 0 / 0 (0,0%) |
| `granite4.2:8b` | aprendizado (54) | 0 / 1 (0,0%) | 3 / 0 (5,6%) | 0 / 1 (0,0%) |
| `qwen2.5-coder:7b` | avaliacao (36) | 0 / 0 (0,0%) | 1 / 1 (2,8%) | 1 / 2 (2,8%) |
| `qwen2.5-coder:7b` | aprendizado (54) | 1 / 4 (1,9%) | 4 / 3 (7,4%) | 5 / 3 (9,3%) |
| `qwen2.5:7b` | avaliacao (36) | 0 / 4 (0,0%) | 2 / 0 (5,6%) | 1 / 2 (2,8%) |
| `qwen2.5:7b` | aprendizado (54) | 2 / 3 (3,7%) | 3 / 3 (5,6%) | 0 / 2 (0,0%) |
| `qwen2.5-coder:3b` | avaliacao (36) | 0 / 1 (0,0%) | 1 / 1 (2,8%) | 1 / 1 (2,8%) |
| `qwen2.5-coder:3b` | aprendizado (54) | 0 / 0 (0,0%) | 2 / 2 (3,7%) | 1 / 2 (1,9%) |
<!-- /tabela:flips -->

## mde

<!-- tabela:mde -->
| n | Pares discordantes supostos | b mínimo (p < 0,05) | Δ mínimo (pp) |
| --- | --- | --- | --- |
| 36 | 7 | 7 | 19,4 |
| 54 | 11 | 10 | 16,7 |
| 90 | 18 | 14 | 11,1 |
<!-- /tabela:mde -->

## recuperacao

<!-- tabela:recuperacao -->
| Modelo | L | Verbetes (novos) | Tokens est. | hit@1 / hit@3 / hit@5 / MRR (90) | hit@1 / hit@3 / hit@5 / MRR (36) | Ouro deslocado por novo | Ouro recuperável após edição |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | L0 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | — |
| `granite4.2:8b` | L1 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | 0 |
| `granite4.2:8b` | L2 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | 0 |
| `granite4.2:8b` | L3 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | 0 |
| `qwen2.5-coder:7b` | L0 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | — |
| `qwen2.5-coder:7b` | L1 | 36 (0) | 7977 | 37,8 / 80,0 / 90,0 / 0,587 | 38,9 / 86,1 / 91,7 / 0,616 | 0 | 0 |
| `qwen2.5-coder:7b` | L2 | 36 (0) | 8369 | 36,7 / 77,8 / 90,0 / 0,581 | 36,1 / 83,3 / 91,7 / 0,600 | 0 | 1 |
| `qwen2.5-coder:7b` | L3 | 36 (0) | 8765 | 37,8 / 78,9 / 90,0 / 0,589 | 36,1 / 86,1 / 91,7 / 0,603 | 0 | 0 |
| `qwen2.5:7b` | L0 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | — |
| `qwen2.5:7b` | L1 | 42 (6) | 9820 | 36,7 / 77,8 / 92,2 / 0,580 | 38,9 / 83,3 / 94,4 / 0,609 | 0 | 1 |
| `qwen2.5:7b` | L2 | 43 (7) | 10806 | 36,7 / 78,9 / 90,0 / 0,583 | 38,9 / 83,3 / 91,7 / 0,607 | 0 | 0 |
| `qwen2.5:7b` | L3 | 45 (9) | 11377 | 36,7 / 78,9 / 88,9 / 0,579 | 38,9 / 86,1 / 88,9 / 0,604 | 0 | 0 |
| `qwen2.5-coder:3b` | L0 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | — |
| `qwen2.5-coder:3b` | L1 | 36 (0) | 6831 | 38,9 / 80,0 / 92,2 / 0,595 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | 0 |
| `qwen2.5-coder:3b` | L2 | 36 (0) | 7037 | 37,8 / 80,0 / 92,2 / 0,591 | 36,1 / 86,1 / 94,4 / 0,607 | 0 | 0 |
| `qwen2.5-coder:3b` | L3 | 37 (1) | 7236 | 37,8 / 81,1 / 93,3 / 0,591 | 36,1 / 86,1 / 94,4 / 0,609 | 0 | 0 |
<!-- /tabela:recuperacao -->

## documentacao

<!-- tabela:documentacao -->
| Modelo | Época | Propostas | Aceitas | % | Notas | Retificações | Verbetes novos | NENHUMA | Sem FIM | Cortadas no teto | Tokens acrescentados (est.) | Biblioteca ao fechar (verbetes / tokens est.) | Aceitas quando errou / quando acertou |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | E1 | 58 | 0 | 0,0% | 0 | 0 | 0 | 1 | 17 | 9 | 0 | 36 / 6582 | 0 de 18 / 0 de 40 |
| `granite4.2:8b` | E2 | 62 | 0 | 0,0% | 0 | 0 | 0 | 0 | 16 | 8 | 0 | 36 / 6582 | 0 de 20 / 0 de 42 |
| `granite4.2:8b` | E3 | 61 | 0 | 0,0% | 0 | 0 | 0 | 0 | 17 | 8 | 0 | 36 / 6582 | 0 de 22 / 0 de 39 |
| `qwen2.5-coder:3b` | E1 | 54 | 4 | 7,4% | 0 | 4 | 0 | 0 | 12 | 0 | 741 | 36 / 6831 | 1 de 20 / 3 de 34 |
| `qwen2.5-coder:3b` | E2 | 54 | 3 | 5,6% | 0 | 3 | 0 | 0 | 8 | 0 | 590 | 36 / 7037 | 1 de 20 / 2 de 34 |
| `qwen2.5-coder:3b` | E3 | 53 | 3 | 5,7% | 0 | 2 | 1 | 1 | 8 | 0 | 745 | 37 / 7236 | 2 de 19 / 1 de 34 |
| `qwen2.5-coder:7b` | E1 | 54 | 25 | 46,3% | 14 | 11 | 0 | 0 | 54 | 0 | 4760 | 36 / 7977 | 6 de 17 / 19 de 37 |
| `qwen2.5-coder:7b` | E2 | 54 | 7 | 13,0% | 4 | 3 | 0 | 0 | 54 | 0 | 1373 | 36 / 8369 | 2 de 14 / 5 de 40 |
| `qwen2.5-coder:7b` | E3 | 54 | 7 | 13,0% | 7 | 0 | 0 | 0 | 54 | 0 | 1381 | 36 / 8765 | 1 de 15 / 6 de 39 |
| `qwen2.5:7b` | E1 | 87 | 40 | 46,0% | 12 | 22 | 6 | 0 | 87 | 0 | 8639 | 42 / 9820 | 14 de 29 / 26 de 58 |
| `qwen2.5:7b` | E2 | 86 | 12 | 14,0% | 6 | 5 | 1 | 1 | 84 | 0 | 2643 | 43 / 10806 | 3 de 28 / 9 de 58 |
| `qwen2.5:7b` | E3 | 91 | 9 | 9,9% | 6 | 1 | 2 | 0 | 89 | 0 | 1787 | 45 / 11377 | 5 de 30 / 4 de 61 |
<!-- /tabela:documentacao -->

## rejeicoes

<!-- tabela:rejeicoes -->
| Código de rejeição | `granite4.2:8b` | `qwen2.5-coder:7b` | `qwen2.5:7b` | `qwen2.5-coder:3b` | Total |
| --- | --- | --- | --- | --- | --- |
| `texto_longo` | 133 | 0 | 1 | 0 | 134 |
| `bloco_malformado` | 26 | 0 | 10 | 91 | 127 |
| `duplicada` | 0 | 33 | 53 | 3 | 89 |
| `palavra_chave_invalida` | 0 | 25 | 44 | 5 | 74 |
| `arquivo_inexistente` | 12 | 10 | 13 | 17 | 52 |
| `trecho_nao_encontrado` | 0 | 11 | 18 | 11 | 40 |
| `teto_notas_verbete` | 0 | 2 | 33 | 0 | 35 |
| `id_repetido` | 5 | 0 | 23 | 5 | 33 |
| `motivo_longo` | 0 | 26 | 2 | 3 | 31 |
| `texto_curto` | 0 | 1 | 2 | 14 | 17 |
| `retificacao_sem_trecho` | 0 | 15 | 0 | 1 | 16 |
| `vocabulario` | 2 | 0 | 3 | 0 | 5 |
| `operacao_invalida` | 3 | 0 | 0 | 0 | 3 |
| `alvo_inexistente` | 0 | 0 | 1 | 0 | 1 |
| `alvo_nao_visto` | 0 | 0 | 0 | 1 | 1 |
| **Total de rejeições** | 181 | 123 | 203 | 151 | 658 |
<!-- /tabela:rejeicoes -->

## custo

<!-- tabela:custo -->
| Modelo | Inferência | Mediana s (p95) | Prefill / geração (mediana, s) | Tokens de saída (média) | Prefill ms/token | Horas do modelo (log) |
| --- | --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | diagnóstico com L0 (época 1) | 131,3 (210,1) | 72,2 / 58,5 | 233 | 68,0 | 26h58 |
| `granite4.2:8b` | diagnóstico com L1 (época 2) | 130,9 (210,3) | 71,9 / 55,7 | 223 | 68,0 |  |
| `granite4.2:8b` | diagnóstico com L2 (época 3) | 132,3 (185,3) | 76,8 / 58,7 | 217 | 68,8 |  |
| `granite4.2:8b` | diagnóstico com L3 (passada final) | 132,6 (244,2) | 75,1 / 60,8 | 225 | — |  |
| `granite4.2:8b` | proposta na época 1 | 263,8 | — | 509 | 43,3 |  |
| `granite4.2:8b` | proposta na época 2 | 270,7 | — | 528 | 43,0 |  |
| `granite4.2:8b` | proposta na época 3 | 285,6 | — | 508 | 46,4 |  |
| `qwen2.5-coder:7b` | diagnóstico com L0 (época 1) | 68,7 (86,7) | 50,9 / 14,6 | 82 | 52,4 | 12h06 |
| `qwen2.5-coder:7b` | diagnóstico com L1 (época 2) | 67,4 (97,9) | 47,5 / 15,2 | 87 | 39,8 |  |
| `qwen2.5-coder:7b` | diagnóstico com L2 (época 3) | 65,5 (102,4) | 47,7 / 14,4 | 84 | 38,7 |  |
| `qwen2.5-coder:7b` | diagnóstico com L3 (passada final) | 49,8 (104,6) | 24,7 / 15,3 | 90 | — |  |
| `qwen2.5-coder:7b` | proposta na época 1 | 117,7 | — | 196 | 31,6 |  |
| `qwen2.5-coder:7b` | proposta na época 2 | 122,3 | — | 198 | 31,6 |  |
| `qwen2.5-coder:7b` | proposta na época 3 | 130,1 | — | 203 | 31,9 |  |
| `qwen2.5:7b` | diagnóstico com L0 (época 1) | 66,8 (78,8) | 51,1 / 13,8 | 62 | 52,4 | 13h53 |
| `qwen2.5:7b` | diagnóstico com L1 (época 2) | 78,2 (94,3) | 61,6 / 13,8 | 63 | 47,4 |  |
| `qwen2.5:7b` | diagnóstico com L2 (época 3) | 77,6 (102,4) | 61,6 / 14,1 | 63 | 43,1 |  |
| `qwen2.5:7b` | diagnóstico com L3 (passada final) | 47,0 (90,6) | 29,4 / 14,4 | 63 | — |  |
| `qwen2.5:7b` | proposta na época 1 | 154,5 | — | 322 | 31,5 |  |
| `qwen2.5:7b` | proposta na época 2 | 168,0 | — | 339 | 29,8 |  |
| `qwen2.5:7b` | proposta na época 3 | 174,7 | — | 368 | 29,1 |  |
| `qwen2.5-coder:3b` | diagnóstico com L0 (época 1) | 30,8 (36,9) | 22,5 / 6,0 | 56 | 21,2 | 05h02 |
| `qwen2.5-coder:3b` | diagnóstico com L1 (época 2) | 16,6 (36,4) | 8,8 / 5,9 | 56 | 8,5 |  |
| `qwen2.5-coder:3b` | diagnóstico com L2 (época 3) | 17,8 (35,9) | 9,5 / 5,8 | 56 | 9,0 |  |
| `qwen2.5-coder:3b` | diagnóstico com L3 (passada final) | 18,4 (35,1) | 9,8 / 5,9 | 56 | — |  |
| `qwen2.5-coder:3b` | proposta na época 1 | 57,8 | — | 194 | 15,0 |  |
| `qwen2.5-coder:3b` | proposta na época 2 | 57,5 | — | 189 | 15,1 |  |
| `qwen2.5-coder:3b` | proposta na época 3 | 56,8 | — | 188 | 14,9 |  |
<!-- /tabela:custo -->

## revisao

<!-- tabela:revisao -->
| Modelo | n | Correta | Parcial | Errada | Sem avaliação |
| --- | --- | --- | --- | --- | --- |
| `qwen2.5-coder:3b` | 10 | 40,0% | 20,0% | 40,0% | 0,0% |
| `qwen2.5-coder:7b` | 24 | 41,7% | 29,2% | 29,2% | 0,0% |
| `qwen2.5:7b` | 29 | 31,0% | 27,6% | 41,4% | 0,0% |

_Fonte: planilhas revisao_edicoes__<slug>.md lidas direto da pasta da corrida._
<!-- /tabela:revisao -->
