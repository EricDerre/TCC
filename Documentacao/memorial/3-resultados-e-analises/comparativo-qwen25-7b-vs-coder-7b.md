<!-- ! Alteração de IA - Revisar: documento novo (29/09/2026) — análise comparativa entre qwen2.5:7b e qwen2.5-coder:7b em tudo o que foi medido (Fases 2-A, 2-B e 3, ponte de versão, análise decisória), com o confronto caso a caso e a lista de toda célula em que o Coder fica à frente. Os blocos `<!-- tabela:cq_… -->` são colados por `comparar_qwen_coder.py --colar` a partir de `resultados_alvo/fase3/comparativo_qwen_coder.md` e conferidos por `--check`; a prosa cita números desses blocos, com o nome do bloco na primeira menção.
     ! Motivo: o Eric pediu (ficha 4, 29/09/2026) "uma análise comparativa profunda entre os resultados do qwen 2.5 7b e do qwen 2.5 coder 7b, pois pode ser que em alguns cenários o coder seja mais interessante (os dados mostram taxa de acertos maior no coder em alguns pontos)". A análise decisória (§8.1) só dava o veredito resumido; aqui cada ponto em que o Coder aparece à frente é localizado, medido contra o ruído e explicado. -->
# Comparativo qwen2.5:7b × qwen2.5-coder:7b — 29/09/2026

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Complementa a [análise decisória](analise-decisoria-modelo-final.md) (§8.1, veredito por modelo) e a [comparação entre fases](comparacao-entre-fases.md). Tabelas geradas por `Programacao/AgenteCore/experimentos/comparar_qwen_coder.py` (`resultados_alvo/fase3/comparativo_qwen_coder.md`; `--check` confere os blocos deste arquivo); nenhum número digitado à mão.

**Pergunta.** Os dois modelos de 7 bilhões de parâmetros da família Qwen2.5 — o de instrução geral (`qwen2.5:7b`, escolhido na decisão 52) e a variante para código (`qwen2.5-coder:7b`) — foram medidos lado a lado nas três fases. Em alguns pontos o Coder aparece com acerto maior. Em que cenários ele seria de fato mais interessante, e a decisão 52 se sustenta?

## 1. Resposta curta

- **Nos casos que nenhum modelo viu com a causa correta (os 36 de avaliação da Fase 3), o qwen2.5:7b fica à frente em todas as versões da biblioteca.** No confronto caso a caso (bloco `cq_confronto_f3`, McNemar exato sobre os mesmos casos), com a biblioteca L1 há 6 casos que só o qwen acerta contra 1 que só o Coder acerta (p = 0,125); com L0, 5 contra 4; com L2 e L3, 5 contra 2. Nos 90 casos o placar é 9 a 9 em L0 e pende levemente para o qwen nas versões seguintes (10 a 8, 10 a 9, 14 a 9).
- **O Coder fica à frente em 26 células** (bloco `cq_onde_vence`), todas pequenas — de +0,1 a +6,7 pontos percentuais em conjuntos de 54 a 90 casos — ou em fatias de 15 casos (uma classe), em que a troca de um único caso vale 6,7 pontos. Nenhuma delas tem p < 0,05; as duas medidas caso a caso em que ele lidera (2-B, condições A1 e A2) dão p = 1,000 e p = 0,832.
- **Onde o padrão se repete:** classes léxica, runtime e efeito (a forma do corpo da resposta e o que a tela mostra) e os 54 casos de aprendizado da Fase 3 — os casos em que o modelo viu a causa correta e propôs edições. **Onde o qwen é claramente melhor:** semântica e tradução, as duas classes difíceis, e os casos nunca vistos.
- **Como escritor da biblioteca, o Coder é mais contido e um pouco mais certo:** 25 edições aceitas na época 1 contra 40 (bloco `cq_documentacao`); 41,7% das edições revisadas corretas contra 31,0% (bloco `cq_revisao`, planilhas de revisão); nenhuma rejeição por `teto_notas_verbete` ou `id_repetido` (bloco `cq_rejeicoes`); e a biblioteca dele mantém o hit@3 do recuperador em 81,1% com L1, enquanto a do qwen cai para 77,8% (bloco `cq_recuperacao`).
- **A decisão 52 se mantém.** Pela regra pré-registrada (bloco `cq_regra36`), a melhor combinação do Coder (L3) fica em 4º lugar, com 84,2% de acurácia balanceada nos 36 contra 91,7% do qwen com L1; no bootstrap (bloco `cq_bootstrap`) a probabilidade de o Coder ser o primeiro é de no máximo 0,5% nos 36; ele é dominado na fronteira de Pareto (bloco `cq_escore_pareto`) e fica em primeiro em 5 dos 36 cortes de estabilidade, contra 14 do qwen.

## 2. Como ler as tabelas

Fontes: `resumo_metricas.json` da Fase 2-A (máquina de desenvolvimento, Ryzen — tempos não comparáveis aos da máquina-alvo), `resultados_alvo/resumo_metricas.json` e `avaliacao.json` da Fase 2-B (i5), `resumo_fase3.json` e `avaliacao_fase3.json` da Fase 3 (i5), `comparacao_fases.json` e `decisao_modelo.json`. "Δ" é sempre Coder menos qwen: positivo = Coder à frente. O **confronto caso a caso** conta, sobre os mesmos casos, quantos só o Coder acertou (b) e quantos só o qwen acertou (c); o teste de McNemar exato diz se essa assimetria é maior do que se esperaria por acaso. Referência de ruído: na Fase 3 o efeito mínimo detectável nos 36 casos é de 19,4 pontos percentuais (`resumo_fase3.json`, `efeito_minimo_detectavel`) — nenhuma diferença deste documento chega perto disso; numa classe de 15 casos, cada caso vale 6,7 pontos. O Coder 7B **não rodou nos 36 casos inéditos** de 28/09 (só o qwen2.5:7b e o Coder 3B), e a troca cruzada (Coder lendo a biblioteca escrita pelo qwen) rodou em 01/10/2026; o resultado dela e a medição que ainda falta estão na seção 9.

## 3. Fase 2-A — prompts sem documentação (Ryzen)

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

Com a estratégia vencedora da fase (o prompt linear, adotado dali em diante), o qwen fica 4,4 pontos à frente (53,3% contra 48,9%); o Coder só passa à frente com o prompt em estágios de compilador (+4,4), que foi descartado por não ajudar os modelos de 7B (Memorial §4). Por classe, somando as três estratégias, o Coder lidera em léxica (+8,9) e efeito (+13,3) e perde em sintática (−11,1) e tradução (−15,6) — o mesmo desenho que reaparece nas fases seguintes.

## 4. Fase 2-B — biblioteca escrita à mão (i5)

<!-- tabela:cq_fase2b -->
| Fase 2-B (i5) · condição | n | acerto qwen2.5:7b | acerto coder:7b | Δ | contra A0 qwen2.5:7b | contra A0 coder:7b | forma ok/conteúdo errado qwen2.5:7b | … coder:7b | s/caso qwen2.5:7b | s/caso coder:7b |
|---|---|---|---|---|---|---|---|---|---|---|
| 2-B · A0 | 90 | 57,8% | 50,0% | -7,8 pp | — | — | 42,2% | 48,9% | 38,0 | 51,3 |
| 2-B · A1 | 90 | 62,2% | 63,3% | +1,1 pp | +4,4 pp (p = 0,5034) | +13,3 pp (p = 0,0730) | 37,8% | 30,0% | 57,1 | 61,2 |
| 2-B · A2 | 90 | 70,0% | 72,2% | +2,2 pp | +12,2 pp (p = 0,0708) | +22,2 pp (p = 0,0005) | 30,0% | 27,8% | 61,1 | 66,6 |
<!-- /tabela:cq_fase2b -->

<!-- tabela:cq_confronto_2b -->
| Fase 2-B · confronto caso a caso | n | ambos acertam | nenhum | só o Coder | só o qwen | Δ | p (McNemar exato) |
|---|---|---|---|---|---|---|---|
| 2-B · A0 | 90 | 33 | 26 | 12 | 19 | -7,8 pp | 0,2810 |
| 2-B · A1 | 90 | 45 | 22 | 12 | 11 | +1,1 pp | 1,0000 |
| 2-B · A2 | 90 | 53 | 15 | 12 | 10 | +2,2 pp | 0,8318 |
<!-- /tabela:cq_confronto_2b -->

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

Sem documentação (A0) o qwen está 7,8 pontos à frente (57,8% contra 50,0%; confronto 19 a 12, p = 0,281). A documentação recuperada (A2) ajuda mais o Coder do que o qwen — +22,2 pontos contra A0 (p = 0,0005) contra +12,2 (p = 0,0708), coluna "contra A0" do bloco `cq_fase2b` — e com ela os dois empatam: 72,2% contra 70,0%, confronto 12 a 10 (p = 0,832). É o primeiro ponto em que "o Coder acerta mais": ele parte de mais baixo e aproveita mais o verbete certo. Por classe em A2, lidera em léxica (100% contra 86,7%), runtime e efeito (+6,7 e +13,3) e perde em semântica (−13,3) e tradução (−6,7); por nível, empata em fácil e médio e passa 6,7 pontos à frente em difícil — duas trocas de caso em 30.

## 5. Fase 3 — biblioteca gerida pelo modelo (i5)

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

A tabela separa os 36 casos de avaliação (nunca viram a causa correta) dos 54 de aprendizado (viram, e o modelo propôs edições a partir deles). O padrão é nítido: **nos 54 de aprendizado o Coder fica à frente em L0, L1 e L2** (+1,8, +5,6 e +3,7 pontos de acerto; +2,8 de acurácia balanceada em L1), **e nos 36 de avaliação fica atrás em todas as versões** (−2,8, −13,9, −8,3 e −8,3). Os 54 são exatamente os casos em que cada modelo escreveu notas sobre a causa correta; a vantagem do Coder ali é o efeito da própria documentação sobre os casos que a geraram, não sobre casos novos. O confronto caso a caso confirma: nos 36 com L1, 6 casos só o qwen acerta contra 1 só o Coder (p = 0,125 — a menor probabilidade deste documento, ainda acima do limiar); nos 90, o placar vai de 9 a 9 (L0) a 14 a 9 (L3), sempre a favor do qwen ou empatado.

<!-- tabela:cq_fase3_classe_L0 -->
<!-- /tabela:cq_fase3_classe_L0 -->

<!-- tabela:cq_fase3_classe_L1 -->
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
<!-- /tabela:cq_fase3_nivel_L0 -->

<!-- tabela:cq_fase3_nivel_L1 -->
<!-- /tabela:cq_fase3_nivel_L1 -->

Por classe (90 casos, 15 por classe), o Coder lidera em léxica, runtime e efeito com a biblioteca original (+6,6, +13,3 e +13,3) e em sintática (+6,7); com L1 a vantagem em runtime some (o qwen chega a 100%) e sobra léxica e efeito (+6,6 cada). Na melhor versão de cada um (qwen L1, Coder L3), o Coder só lidera em efeito (+20,0 — três casos em 15) e perde em sintática, semântica, tradução e runtime (−13,3 cada) e em tradução (−13,4). Em semântica e tradução o qwen está 13 a 20 pontos à frente em todas as versões: são as classes em que a resposta exige comparar o dado com o contrato e com a regra de negócio, e não reconhecer a forma. Por nível, o Coder leva vantagem pequena em médio e difícil com L1 (+3,3 cada) e perde por 13,4 pontos em fácil — o que sugere que a diferença não é de "dificuldade", mas de classe.

## 6. O Coder como escritor da biblioteca

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

Aqui está a parte em que o Coder é de fato diferente, e para melhor. Ele propõe menos (54 propostas por época — uma por caso de aprendizado — contra 86 a 91 do qwen) com a mesma taxa de aceitação na época 1 (46,3% contra 46,0%), o que dá 25 edições aceitas contra 40. Os motivos de rejeição mostram o temperamento de cada um: o qwen é barrado por `duplicada` (53), `teto_notas_verbete` (33) e `id_repetido` (23) — insiste na mesma nota e no mesmo verbete; o Coder por `motivo_longo` (26) e `retificacao_sem_trecho` (15) — escreve demais no campo do motivo e retifica sem apontar o trecho. Na revisão humana (amostra de até 30 edições por modelo), 41,7% das edições do Coder são corretas contra 31,0% do qwen; as notas do Coder são 9 corretas, 5 parciais e 2 erradas, contra 7, 5 e 2; nas retificações os dois erram na maior parte (5 de 8 e 6 de 10). O Coder não criou verbete novo (o qwen criou 6, dos quais 4 errados na revisão). Consequência para o recuperador: a biblioteca do Coder continua com 36 verbetes e mantém o hit@3 em 81,1% nos 90 com L1, enquanto a do qwen, com 42 verbetes, cai para 77,8%. As trocas de rótulo entre épocas são parecidas nos dois (autoenvenenamento máximo nos 36: 2,8% no Coder, 5,6% no qwen).

Em uma frase: **o Coder escreve menos e melhor, mas o que ele escreve não o faz acertar mais nos casos novos** — e é o acerto nos casos novos que a regra de decisão mede.

## 7. Decisão e robustez

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

<!-- tabela:cq_riscos -->
| Risco | qwen2.5:7b | coder:7b |
|---|---|---|
| adesão cega à documentação errada (2-B A5) — não medida nos dois | — | — |
| teto com o verbete de ouro forçado (2-B A3) — não medido nos dois | — | — |
| tentativas de decorar o caso (Fase 3, total) | 0 | 0 |
| autoenvenenamento nos 36 por transição (Fase 3) | L0→L1 0,0% / L1→L2 5,6% / L2→L3 2,8% | L0→L1 0,0% / L1→L2 2,8% / L2→L3 2,8% |
<!-- /tabela:cq_riscos -->

Nos 36 casos de avaliação, coluna a coluna das três fases (bloco `cq_entre_fases`), o qwen está à frente em todas as oito colunas — de −2,8 (Fase 3, L0) a −25,0 pontos (2-B sem documentação). Nos 90, o Coder lidera em uma coluna (2-B A2, +2,2) e empata em outra (Fase 3 L0). A regra pré-registrada, o bootstrap, a fronteira de Pareto e o escore ponderado apontam o mesmo: a melhor combinação do Coder (L3, 84,2% balanceada) fica atrás de três combinações do qwen; a probabilidade de o Coder ser o melhor em reamostragens dos casos é de 0,5% ou menos nos 36 e chega a 9,8% nos 90 só com L1; o escore ponderado do Coder L3 (0,6921) é dominado — o qwen L3 é ao mesmo tempo mais certeiro e mais barato. A ponte de versão do Ollama (0.34.0 → 0.34.1) não trocou nenhum rótulo do Coder (b = c = 0) e trocou um em cada sentido no qwen: os dois são pareáveis com a Fase 3. Custo: com a biblioteca L1 o Coder é um pouco mais rápido (67,4 s contra 78,2 s por diagnóstico nos 90, bloco `cq_fase3`), porque a biblioteca dele tem menos notas para ler; com L0 e L3 os tempos são equivalentes.

## 8. Todas as células em que o Coder fica à frente

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

Em grupos: (1) a estratégia de compilador da 2-A, descartada; (2) as condições A1 e A2 da 2-B, com +1,1 e +2,2 pontos e confrontos caso a caso de p = 1,000 e p = 0,832; (3) os 54 casos de aprendizado da Fase 3 em L0, L1 e L2 (de +0,1 a +5,6), que são os casos sobre os quais o próprio modelo escreveu; (4) as classes léxica, runtime e efeito e a sintática em L0, com 15 casos cada (um caso = 6,7 pontos); (5) o nível difícil da 2-B e os níveis médio e difícil da Fase 3 com L1 (+3,3 a +6,7 em 30 casos). Nenhum grupo sobrevive ao teste pareado, e o único conjunto em que a diferença poderia ser lida como "generalização" — os 36 de avaliação — vai todo para o qwen.

<!-- ! Alteração de IA - Revisar: em 01/10/2026 os itens 2 e 4 do §9 ganharam o resultado da troca cruzada e o §10 ganhou uma linha.
     ! Motivo: os dois itens terminavam em "troca cruzada pendente"; a corrida rodou e o comparativo precisa dizer o que ela respondeu. Números de `analise_fase3b.json`. -->
## 9. Em que cenários o Coder seria mais interessante — e o que falta medir

1. **Diagnóstico das classes léxica, runtime e efeito.** É onde o Coder aparece à frente com mais constância (2-A, 2-B A2 e Fase 3 L0). Mas cada classe tem 15 casos por fase, e a vantagem some ou inverte de uma versão da biblioteca para outra (runtime: +13,3 em L0, −6,7 em L1). Um roteamento por classe — mandar esses casos para o Coder — não é defensável com esse n. **O que fecharia a questão:** rodar o Coder 7B nos 36 casos inéditos (108 diagnósticos, cerca de 2 h de máquina; comando no roadmap) e comparar por classe com o qwen, que já rodou lá.
2. **Leitor da biblioteca escrita pelo qwen.** A troca cruzada (Coder 7B e 3B lendo L1 e L3 do qwen nos 36) responde se o ganho da L1 é da biblioteca ou de quem a escreveu. Se o Coder, lendo a L1 do qwen, alcançar ou passar os 88,9% do qwen, o arranjo "um escreve, outro lê" entra em pauta; se ficar nos 75,0% que tem com a própria biblioteca, a vantagem é do leitor. A ideia de "lê o mais barato" não se aplica aqui: os dois 7B custam parecido (66 a 78 s por diagnóstico). **Resultado (01/10/2026):** o Coder 7B, lendo a L1 do qwen, acerta 83,3% nos 36: não alcança os 88,9% do qwen (b/c 1/3 contra ele, p = 0,625) e fica 1 caso de saldo acima do próprio L0 na mesma versão do Ollama (80,6%; b/c 3/2). O arranjo "um escreve, outro lê" não entra em pauta, e o 3B, com a mesma biblioteca, perde 4 casos de saldo ([fase-3b-relatorio.md](fase-3b-relatorio.md) §5).
3. **Escritor de notas.** O Coder escreve menos edições, com mais corretas e sem duplicar; se a Fase 4 separar o momento de escrever (fora da corrida, revisado) do momento de diagnosticar, ele é o candidato natural a escritor — mas isso exige dois modelos de 7B alternando na mesma máquina (só um fica residente por vez) e dobra o tempo. Fica como opção a medir depois da troca cruzada, não como decisão.
4. **O que mudaria a decisão 52:** o Coder vencer o qwen nos casos inéditos (não medido), ou ler a biblioteca do qwen melhor do que o próprio qwen (troca cruzada pendente). Sem uma das duas, a variante de instrução geral continua sendo o modelo do agente — e nas duas classes difíceis (semântica e tradução) a vantagem do qwen é a maior de todas. **Resultado (01/10/2026):** a troca cruzada rodou e a segunda condição não se cumpriu; a primeira (o Coder 7B nos casos inéditos) segue sem medida e é uma das opções da ficha 17.

## 10. O que muda no projeto

- Decisão 52 mantida (modelo `qwen2.5:7b`); este documento é a fundamentação do veredito "segundo escritor, sem ganho nos 36" da análise decisória §8.1.
- Projeto de pesquisa ABNT, modificações 1 e 2 (modelo da família Qwen2.5 com a variante definida experimentalmente; critério da decisão 36 no lugar de "o menor modelo que atenda"): a análise não muda os textos propostos em 23/09 — a variante escolhida é a de instrução geral, pela regra pré-registrada; a aplicação aguarda o Eric (ficha 10).
- Roadmap: corrida opcional nova — Coder 7B nos 36 inéditos (`-Modo ineditos -Saida fase3b_ineditos_coder7b -Versoes 0,1,3 -Modelos qwen2.5-coder:7b`; 108 diagnósticos, ~2 h) — só se o Eric quiser fechar o cenário 1; a troca cruzada (corrida 1) já responde o cenário 2.
- Troca cruzada rodada em 01/10/2026: decisão 52 mantida; o padrão é o `qwen2.5:7b` com a biblioteca que ele mesmo escreveu (decisão 69). Na ponte de 30/09 (Ollama 0.34.4) o Coder 7B acertou 80,6% em L0, 2 casos acima do qwen (75,0%), dentro da variação entre corridas iguais (achado 4.43).
