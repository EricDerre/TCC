<!-- ! Alteração de IA - Revisar: tabela gerada por comparar_fases.py a partir de comparacao_fases.json -- NÃO editar à mão.
     ! Motivo: é a tabela que compara as três fases de teste para decidir o modelo final do TCC; editar direto quebraria a garantia de que todo número do Memorial sai de script, e a próxima corrida de comparar_fases.py sobrescreveria a edição sem avisar. -->

# Comparação entre as fases 2-A, 2-B e 3

### Acerto por modelo e fase (90 casos)

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

### Acurácia balanceada por modelo e fase (90 casos)

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

### Acerto por modelo e fase (36 casos de avaliação)

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

### Acurácia balanceada por modelo e fase (36 casos de avaliação)

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

### Custo e prolixidade

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

### Modos de falha e riscos

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

### Pareamentos

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

## Leitura por fase

Fase 2-A: melhor modelo granite4.2:8b, 67,8% de acerto (braço linear, Ryzen, sem biblioteca).

Fase 2-B: melhor modelo granite4.2:8b, 76,7% em A2 (com recuperação); ganho médio de A0 para A2 de 16,3 pp (média sobre os modelos com pareamento nos 90 casos).

Fase 3: melhor modelo qwen2.5:7b, 83,0% de acurácia balanceada em L1 (acerto simples 76,7%); ganho médio de L0 para L3 nos 36 casos de avaliação de 3,5 pp. Risco: adesão cega média de 73,0% em A5 (2-B), autoenvenenamento médio de 2,1% na transição L2→L3 nos 36 casos de avaliação. Perda: 57,0 s/caso em 2-B A2 contra 61,9 s/caso em F3 L3.
