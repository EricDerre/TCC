<!-- ! Alteração de IA - Revisar: arquivo criado em 11/09/2026 como esqueleto da leitura das três
     fases juntas — o que é comparável entre elas, quais tabelas o `comparar_fases.py` gera, e os
     lugares dos ganhos, riscos e perdas de cada fase e da escolha do modelo final, marcados
     com "(a preencher ... após a bateria)".
     ! Motivo: as três fases rodaram em condições diferentes (Ryzen × i5; fixtures do achado 4.20
     antes e depois da correção; prompts fixados) e, sem dizer antes o que pareia com o quê, a
     comparação vira soma de porcentagens de experimentos diferentes. As ressalvas estão escritas
     antes de existir número para elas justamente por isso; as tabelas serão coladas de
     `comparacao_fases.md`, que sai de script. -->
<!-- ! Alteração de IA - Revisar: em 12/09/2026 a §1 ganhou o quarto fator que mudou entre as
     fases — a versão do Ollama (0.33.3 na 2-B, 0.34.0 na Fase 3) — e a nota de estado passou
     para 12/09.
     ! Motivo: o Ollama atualizou sozinho em 12/09/2026, antes da bateria da Fase 3, e não foi
     revertido; a §1 listava máquina, fixtures e prompts como as únicas diferenças, e o
     pareamento 2-B A2 × F3 L0 (que esta seção apresenta como medida de reprodutibilidade)
     passa a medir também o efeito da versão — sem dizer isso, o leitor atribuiria a ruído de
     execução o que pode ser mudança do runtime. -->
<!-- ! Alteração de IA - Revisar: segunda passada de 12/09/2026 — em §1, "O runtime", a
     Verificação 0 em 0.33.2 deixou de ser atribuída à 2-B nesta máquina e passou a ser a do
     achado 4.21, medida no Ryzen em 03/09/2026; a 2-B inteira, Verificação 0 incluída, rodou em
     0.33.3.
     ! Motivo: o "0.33.2" vem do commit 603c423 (03/09/2026), anterior à decisão 25 (07/09) que
     fez do i5 a máquina-alvo; o `maquina.json` da 2-B registra 0.33.3 desde 07/09 09:18 e o
     `fase2b.log` mostra a Verificação 0 às 09:29 do mesmo dia. Dizer que a 2-B teve uma parte em
     0.33.2 inventava uma terceira versão no pareamento 2-B A2 × F3 L0. -->
<!-- ! Alteração de IA - Revisar: em 22/09/2026 as seções §3–§6 foram preenchidas; as tabelas são blocos `cf_*`
     colados de `resultados_alvo/fase3/tabelas_relatorio.md` (seções de `comparacao_fases.md` reexpostas por
     `gerar_tabelas_relatorio_fase3.py`, conferidas por `--check`); a reprodutibilidade (§5) e a decisão (§6) citam
     o relatório da Fase 3 e a análise decisória.
     ! Motivo: o esqueleto dizia "(a preencher)" em quatro seções desde 11/09; colar as tabelas à mão quebraria a
     regra de nenhum número digitado, por isso o bloco marcado. -->
# Comparação entre as fases

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Relatórios de cada fase em [fase-2a-relatorio-por-modelo.md](fase-2a-relatorio-por-modelo.md), [fase-2b-relatorio-por-modelo.md](fase-2b-relatorio-por-modelo.md) e [fase-3-relatorio-por-modelo.md](fase-3-relatorio-por-modelo.md). As tabelas deste arquivo são coladas de `resultados_alvo/fase3/comparacao_fases.md`, gerado por `comparar_fases.py` a partir de `experimentos/avaliacao.json` (2-A), `resultados_alvo/avaliacao.json` (2-B) e `resultados_alvo/fase3/avaliacao_fase3.json`. **Nenhum número é digitado à mão.** Gráficos 16 `comparacao-entre-fases` e 17 `custo-versus-acerto-tres-fases`.

<!-- ! Alteração de IA - Revisar: linha de estado nova (21/09/2026); a anterior fica como histórico, sem negrito.
     ! Motivo: a bateria da Fase 3 rodou em 13–15/09/2026 e `comparacao_fases.md` já existe em `resultados_alvo/fase3/`; o cabeçalho dizia "bateria não executada". §3–§6 são preenchidas pelo plano complementar de 21/09. -->
> **Estado em 22/09/2026: bateria concluída (13–15/09/2026); `comparacao_fases.md` gerada em 15/09 18:44; §3–§6 preenchidas em 22/09/2026 (blocos `cf_*` conferidos por `gerar_tabelas_relatorio_fase3.py --check`); decisão do modelo em §6 e em [analise-decisoria-modelo-final.md](analise-decisoria-modelo-final.md).**
>
> Estado anterior (21/09/2026): bateria concluída; §3–§6 em preenchimento pelo plano complementar de 21/09/2026.
>
> Estado anterior (12/09/2026): pré-registrado; a bateria ainda não tinha rodado (implementação concluída e revisada; piloto de 10 casos rodado em 12/09/2026). As seções 1 e 2 valem como estão. As demais estão marcadas com *(a preencher…)*.

## 1. O que é comparável, e o que não é

Quatro coisas mudaram entre as fases. Cada tabela precisa dizer qual delas a afeta.

**A máquina.** A Fase 2-A rodou no Ryzen de desenvolvimento; a 2-B e a Fase 3 rodam na máquina-alvo (i5-1235U, decisão 25). O achado 4.26 mediu exatamente esse efeito refazendo a linha de base nas duas máquinas: **o acerto reproduz** (nenhuma diferença significativa, respostas idênticas em 91–98% dos casos, exceto `qwen2.5-coder:7b` com 68,9%), **o tempo não** (o i5 é 1,6–2,3× mais lento). Consequência: acerto da 2-A pode ser comparado com o das fases seguintes; **segundos por caso, não** — no gráfico 17 os pontos da 2-A vão com marcador vazado, e nas tabelas a coluna `maquina` acompanha cada número.

**Os fixtures.** Os 4 casos do achado 4.20 (`sin-1`, `sin-2`, `semt-13`, `efe-13`) foram corrigidos antes da Fase 3 (decisão 34) e caíram todos na partição de aprendizado. Então: nos **36 de avaliação**, Fase 3 e 2-B rodaram exatamente o mesmo texto e o pareamento não tem ressalva; nos **90**, a comparação com 2-A e 2-B vale sobre os **86 casos não alterados**. Toda tabela diz em qual dos dois conjuntos está.

**Os prompts.** O prompt de diagnóstico da Fase 3 é byte a byte o mesmo da 2-B, de propósito: formatação de prompt muda o resultado, e comparar fases com prompts diferentes mediria a formatação em vez do conhecimento. Entre 2-A e 2-B, o que mudou foi a presença da biblioteca e o teto de resposta (900 tokens em A0, 600 nos braços com biblioteca), e isso está dito em cada linha. Já as **estratégias de prompt** (linear × estágios) só existem na 2-A: a partir da 2-B o prompt é fixo em linear (decisão 19), então essa coluna aparece como "sem dado" nas fases seguintes.

**O runtime.** A 2-B rodou inteira em Ollama 0.33.3 na máquina-alvo, inclusive a Verificação 0 do cache de prefixo registrada no `fase2b.log` (o achado 4.21, Verificação 0 medida no Ryzen em 03/09/2026, é que rodou em 0.33.2); antes da bateria da Fase 3 o Ollama atualizou sozinho para **0.34.0** (12/09/2026) e não foi revertido — máquina corporativa, atualização automática. É um fator não controlado, e só entre fases: o pareamento **2-B A2 × Fase 3 L0** nos 36 e nos 86 casos mede o ruído de execução **somado** ao efeito da versão, sem separar os dois. Todas as comparações internas à Fase 3 (L0..L3, modelo contra modelo) são na mesma versão, gravada em `maquina.json` e, pela decisão 44, em todo registro.

**Duas colunas com significados diferentes de "sem biblioteca".** `2B_A0` é o modelo sem documentação nenhuma; `F3_L0` é o modelo com a biblioteca original recuperada, isto é, a mesma condição de `2B_A2`. O par que mede reprodutibilidade é **`2B_A2` × `F3_L0`** — mesma máquina, mesmo prompt, mesma biblioteca, execuções diferentes; o que ele mostrar é o ruído de execução que separa qualquer dois números deste arquivo.

**Só os 4 modelos da Fase 3** aparecem nas colunas completas: `granite4.2:8b`, `qwen2.5:7b`, `qwen2.5-coder:7b` e `qwen2.5-coder:3b`. `phi4-mini:3.8b` e `qwen2.5-coder:1.5b` ficam nas fases em que rodaram.

## 2. As tabelas que `comparar_fases.py` gera

O script grava `comparacao_fases.json` e `comparacao_fases.md` em `resultados_alvo/fase3/`. O conteúdo:

- **Quadro por modelo**, nas colunas `2A_linear_ryzen`, `2B_A0`, `2B_A2`, `F3_L0` e `F3_L3`, com `n`, acerto e IC 95%, acurácia balanceada, mediana de segundos por caso, tokens de saída, fora do conjunto, formato-ok-conteúdo-errado, hit@3 e a máquina em que foi medido — repetido em dois recortes: **`nos_90`** e **`nos_36_avaliacao`**.
- **Modos de falha** lado a lado: colapso num rótulo, rótulo inventado e adesão cega (`adesao_cega_2B_A5_pct`, que existe só para `granite4.2:8b` e `qwen2.5-coder:3b` — dos quatro modelos desta comparação, foram os que rodaram o braço A5 da 2-B).
- **Medidas que só a Fase 3 tem**: `tentativas_de_decorar_F3` (propostas rejeitadas por copiar o caso) e `autoenvenenamento_F3` (casos certos que viram errados de uma versão da biblioteca para a seguinte).
- **Pareamentos**, cada um com `n_comuns`, b/c, Δ em pontos percentuais, p do McNemar exato e as colunas `mesma_maquina` e `mesmos_fixtures` dizendo se o par é comparável: (2-A × 2-B A0), (2-B A0 × 2-B A2), (**2-B A2 × Fase 3 L0**, nos 36 e nos 86 não alterados) e (Fase 3 L0 × L3, nos 36 e nos 54).

## 3. Quadro das três fases

Tabelas de `comparacao_fases.md` (gerado por `comparar_fases.py`), coladas como blocos conferidos. Primeiro os 36 de avaliação (o mesmo texto nas três fases), depois os 90 (nos 86 não alterados para as colunas 2-A e 2-B).

**Acerto nos 36** (IC de Wilson a 95%):

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

**Acurácia balanceada nos 36**:

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

**Acerto nos 90**:

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

**Acurácia balanceada nos 90**:

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

**Custo e prolixidade** (segundos por caso, mediana / tokens de saída, média; a coluna 2-A é do Ryzen e não compara em tempo):

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

**Modos de falha e riscos**:

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

**Leitura por fase**, como o script a escreve:

<!-- tabela:cf_leitura -->
Fase 2-A: melhor modelo granite4.2:8b, 67,8% de acerto (braço linear, Ryzen, sem biblioteca).

Fase 2-B: melhor modelo granite4.2:8b, 76,7% em A2 (com recuperação); ganho médio de A0 para A2 de 16,3 pp (média sobre os modelos com pareamento nos 90 casos).

Fase 3: melhor modelo qwen2.5:7b, 83,0% de acurácia balanceada em L1 (acerto simples 76,7%); ganho médio de L0 para L3 nos 36 casos de avaliação de 3,5 pp. Risco: adesão cega média de 73,0% em A5 (2-B), autoenvenenamento médio de 2,1% na transição L2→L3 nos 36 casos de avaliação. Perda: 57,0 s/caso em 2-B A2 contra 61,9 s/caso em F3 L3.
<!-- /tabela:cf_leitura -->

Três leituras que as tabelas sustentam. (1) O salto grande do trabalho é da 2-A para a 2-B A2 — conhecer o sistema (média de 33,9% para 54,1% nos 90; 3B de 25,6% para 63,3%) — e o da Fase 3 é pequeno e de um modelo só: a média dos quatro vai de 78,3% (F3 L0) para 82,6% (F3 melhor) de acurácia balanceada nos 36, e o `qwen2.5:7b` responde por quase tudo (81,2% → 91,7%). (2) A coluna "F3 melhor" é L1 em três modelos nos 90 e nunca é L3 no `qwen2.5:7b` — a curva sobe e regride (relatório da Fase 3, H6). (3) O custo cresce a cada fase que acrescenta contexto (Granite 83,0 → 123,9 → 131,3 s de A0 a F3 L0), e a Fase 3 não encareceu a leitura além disso: a tabela de custo mostra F3 L0 dentro de 2–5 s de 2-B A2 nos quatro modelos.

## 4. Ganhos, riscos e perdas de cada fase

### Fase 2-A — sem conhecimento do sistema
- **Ganhos:** a linha de base sem conhecimento do sistema — 33,9% de acerto médio nos 90 (7 modelos) e o `granite4.2:8b` em 67,8%; o achado de que raciocinar em estágios não ajuda os modelos pequenos (4.16) e a escolha do prompt linear (decisão 19), que todas as fases seguintes herdaram.
- **Riscos:** dois modos de falha nos modelos pequenos — colapso num rótulo (`qwen2.5-coder:1.5b`, um rótulo em 84% das respostas) e rótulo inventado (`phi4-mini:3.8b`, 17,8% fora do conjunto; 4.17); os 4 fixtures do 4.20 ainda descreviam sintomas que o código não produz.
- **Perdas:** o tempo não é comparável com as fases seguintes (Ryzen; 4.26) e as estratégias em estágios custaram inferência sem trazer resultado.

### Fase 2-B — biblioteca compartilhada, só leitura
- **Ganhos:** +16,3 pp de A0 para A2 na média dos modelos pareados ("Leitura por fase"); o 3B de 23,3% para 63,3% (36 casos ganhos, nenhum perdido; 4.22, 4.25); três modelos acima de 70% nos 90; o recuperador com sinais em código (hit@3 78,9%; 4.19) e a evidência de que o teto é a recuperação (4.23: 100% com o verbete certo).
- **Riscos:** adesão cega de 93–96% a um verbete errado com "registro de incidente" (A5; 4.24) — o risco que a Fase 3 precisou controlar com validação em código; a biblioteca inteira no prompt piora o Granite (Context Rot; 4.22).
- **Perdas:** o tempo por caso sobe com a biblioteca (Granite 83,0 → 123,9 s; `qwen2.5:7b` 38,0 → 61,1 s) e a biblioteca era estática: nada do que o modelo aprendia num caso servia ao seguinte.

### Fase 3 — biblioteca escrita pelo próprio modelo
- **Ganhos:** o vencedor sobe de 81,2% para 91,7% de acurácia balanceada nos 36 em L1 (acerto 77,8% → 88,9%, b/c 4/0) sem envenenar (autoenvenenamento máximo 5,6%); a média dos quatro vai de 78,3% (F3 L0) para 82,6% (F3 melhor) nos 36; 0 tentativas de decorar; o validador em código barrou 658 propostas e deixou passar 110, sem que a biblioteca perdesse uma linha (só acréscimo conferido a cada fechamento).
- **Riscos:** 41,4% das edições do vencedor estão erradas na revisão (relatório §7) e as corretas são redundantes — o ganho não é da verdade do conteúdo (achado 4.35); a recuperação ficou um pouco pior em quem editou (MRR 0,596 → 0,579–0,589); a biblioteca satura em três épocas (`duplicada`, `teto_notas_verbete`; 4.32); o ganho fica abaixo do efeito mínimo detectável de 19,4 pp (4.33); o Granite não conseguiu documentar sob o formato (4.30).
- **Perdas:** custo — 61,9 s/caso em F3 L3 contra 57,0 em 2-B A2 ("Leitura por fase") e 58h59 de máquina para as 2.088 inferências; a biblioteca do `qwen2.5:7b` cresceu 73% em tokens (6.582 → 11.377), o que encarece o prefill (relatório §9); e o estado da biblioteca deixou de ser variável controlada entre modelos (relatório §11).

## 5. Reprodutibilidade entre execuções

O pareamento **2-B A2 × Fase 3 L0** compara duas execuções da mesma condição, na mesma máquina, com o mesmo prompt e a mesma biblioteca. É a única medida do projeto sobre quanto o resultado varia sozinho, e ela calibra a leitura de todas as outras diferenças.

Do bloco `cf_pareamentos` (`comparacao_fases.md`; linhas `2B_A2` × `F3_L0`):

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

Nos 36, b/c = 0/0 nos quatro modelos exceto o `qwen2.5-coder:7b` (1/0, Δ +2,8 pp, p = 1,0); nos 86 não alterados, 0/0 no Granite, no 3B e no `qwen2.5:7b`, e 2/3 no Coder 7B (Δ −1,2 pp, p = 1,0) — **b = c = 0 em 6 dos 8 pareamentos e no máximo 5 discordâncias em 86** apesar da mudança de runtime (0.33.3 → 0.34.0). É o mesmo modelo, `qwen2.5-coder:7b`, que 4.26 apontou como o menos idêntico entre máquinas (68,9%) e o único com `formato_valido_pct` abaixo de 100 na Fase 3: a variação entre execuções mora nele. A ponte de versão da 3-B (0.34.0 → 0.34.1; relatório §11) repetiu a medida: 0/0, 0/0 e 1/1 nos 36 em três modelos. O ruído de execução que separa dois números deste arquivo é, portanto, de 0 a 2 casos em 36 — e é isso que calibra a leitura do +11,1 pp (4 casos) do `qwen2.5:7b` em L1: acima do ruído, abaixo do que o teste resolve (achado 4.31).

## 6. Decisão do modelo final

Pela regra pré-registrada (decisão 36, aplicada por `decidir_modelo.py` — `decisao_modelo.md` §1): **`qwen2.5:7b` com a biblioteca no estado L1**, 91,7% de acurácia balanceada nos 36 (acerto 88,9%), autoenvenenamento máximo 5,6% (sem veto), licença Apache-2.0 como os demais. Robustez (`decisao_modelo.md` §2–§5): P(top-1) de 77,6% nos 36 e 50,0% nos 90 (2.000 réplicas por caso); fronteira de Pareto com quatro não dominados (3B em L1 e L2, `qwen2.5:7b` em L1 e L3); o escore ponderado concorda, e só troca de vencedor com peso de custo de 0,50 (L3 do mesmo modelo) ou 0,75 (3B em L1). Confirmada pelo Eric em 22/09/2026 (decisão 52), com o `granite4.2:8b` sem ponte de versão. A análise completa — riscos, o que a literatura previa, limitações e o que a 3-B acrescentaria — está em [analise-decisoria-modelo-final.md](analise-decisoria-modelo-final.md); o padrão de produção (`install.py`) e a curadoria da cópia L1 ficam em [../pendencias.md](../pendencias.md).
