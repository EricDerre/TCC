<!-- ! Alteração de IA - Revisar: relatório da Fase 2-B (biblioteca de documentação como
     contexto), por modelo, escrito em 09/09/2026 a partir de resultados_alvo/avaliacao.json,
     resultados_alvo/resumo_metricas.json e dos JSONL brutos gravados na máquina-alvo.
     ! Motivo: é a seção de resultados que responde à pergunta central da fase — documentação
     do sistema fecha a lacuna até 70–80%? — e, com o mesmo rigor da 2-A, diz por quê e a que
     custo. Nenhum número foi digitado à mão: todos saem de `RESULTADOS_DIR=resultados_alvo
     python avaliar.py` e dos cortes reproduzíveis citados em cada seção. -->
# Fase 2-B — biblioteca de documentação: relatório por modelo

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Leitura da Fase 2-A em [fase-2a-relatorio-por-modelo.md](fase-2a-relatorio-por-modelo.md). Gráficos em `Programacao/AgenteCore/experimentos/resultados_alvo/graficos/07…11`; respostas cruas em `resultados_alvo/relatorio.html`.

## 1. O que foi medido

| Item | Valor |
|---|---|
| Máquina | **máquina-alvo** `TARGET_TSP030`: Intel i5-1235U (10 núcleos, 12 threads), 15,7 GB de RAM (7,2 GB livres no início), sem GPU dedicada, Windows 11 Pro; Ollama 0.33.3; Python 3.14.7. Início 07/09/2026 09:18 |
| Casos | os mesmos 90 da Fase 2-A (6 classes × 3 níveis × 5), 23 causas raiz |
| Prompt | **linear**, fixo (decisão 19); teto de resposta 900 tokens em A0 e 600 nos braços com biblioteca |
| Biblioteca | 36 verbetes em `base_conhecimento/` (17,1 mil caracteres; 5.230 tokens no tokenizador do Qwen), validada antes de rodar |
| Condições | **A0** sem biblioteca (linha de base **refeita nesta máquina**) · **A1** biblioteca inteira como prefixo · **A2** 3 verbetes recuperados (filtro por frontmatter + BM25 + sinais em código) · **A3** só o verbete certo · **A4** 3 verbetes plausíveis mas errados · **A5** 1 verbete errado + registro de incidente falso afirmando a causa errada |
| Modelos | A0/A1/A2 nos 6 modelos; A3–A5 em `granite4.2:8b`, `qwen2.5-coder:3b` e `phi4-mini:3.8b`; ablação de quantização: `qwen2.5-coder:1.5b` em `q8_0` e `fp16` (A0) |
| Inferências | **2.610**, 0 erros de infraestrutura, todas só em CPU, um modelo residente por vez; 7 respostas cortadas no teto (6 do `coder:7b` em A1, 1 do Granite em A4) — contam como erro |
| Estatística | IC 95% de Wilson; Δ contra A0 pareado por caso com McNemar exato |

O `fase2b.log` da máquina-alvo (com a Verificação 0 do cache de prefixo nela) não veio no commit — `*.log` está no `.gitignore`. O comportamento do cache fica visível, ainda assim, nos tempos de prefill por condição (seção 8).

## 2. A mesma linha de base em duas máquinas

Antes de comparar condições, a pergunta preliminar: o A0 refeito no i5 reproduz o do Ryzen? Pareado caso a caso (mesmos 90 casos, mesmo prompt, mesma quantização):

| Modelo | Ryzen (2-A) | i5 (2-B) | Mesma resposta | só Ryzen / só i5 | p | Seg/caso Ryzen | Seg/caso i5 | Razão |
|---|---|---|---|---|---|---|---|---|
| `granite4.2:8b` | 67,8% | 66,7% | 91,1% | 3/2 | 1,00 | 45,7 | 83,0 | 1,8× |
| `qwen2.5:7b` | 53,3% | 57,8% | 95,6% | 0/4 | 0,13 | 17,1 | 38,0 | 2,2× |
| `qwen2.5-coder:7b` | 48,9% | 50,0% | **68,9%** | 7/8 | 1,00 | 25,9 | 51,3 | 2,0× |
| `qwen2.5-coder:3b` | 25,6% | 23,3% | 93,3% | 2/0 | 0,50 | 8,4 | 17,1 | 2,0× |
| `phi4-mini:3.8b` | 23,3% | 23,3% | 92,2% | 1/1 | 1,00 | 9,8 | 22,6 | 2,3× |
| `qwen2.5-coder:1.5b` | 5,6% | 5,6% | 97,8% | 0/0 | 1,00 | 5,2 | 8,3 | 1,6× |

**Acurácia reproduz; tempo não.** Nenhuma diferença de acerto é significativa e as respostas são idênticas em 91–98% dos casos — exceto no `qwen2.5-coder:7b` (68,9%), o modelo mais prolixo e menos estável entre máquinas, embora o acerto agregado seja o mesmo. A máquina-alvo é **2× mais lenta** (1,6–2,3×). A decisão de refazer A0 nela (decisão 25) foi correta pelo motivo certo: os tempos daqui em diante são os do i5, e o pareamento por caso ficou dentro da mesma máquina.

## 3. Resultado principal: recuperada vence, inteira não

| Modelo | A0 | A1 inteira | Δ | p | A2 recuperada | Δ | p | IC 95% de A2 |
|---|---|---|---|---|---|---|---|---|
| `granite4.2:8b` | 66,7% | 61,1% | −5,6 | 0,50 | **76,7%** | +10,0 | 0,12 | 66,9–84,2 |
| `qwen2.5-coder:7b` | 50,0% | 63,3% | +13,3 | 0,07 | **72,2%** | +22,2 | **0,0005** | 62,2–80,4 |
| `qwen2.5:7b` | 57,8% | 62,2% | +4,4 | 0,50 | **70,0%** | +12,2 | 0,07 | 59,9–78,5 |
| `qwen2.5-coder:3b` | 23,3% | 32,2% | +8,9 | 0,06 | **63,3%** | +40,0 | **<0,001** | 53,0–72,6 |
| `phi4-mini:3.8b` | 23,3% | 22,2% | −1,1 | 1,00 | 25,6% | +2,3 | 0,79 | 17,7–35,4 |
| `qwen2.5-coder:1.5b` | 5,6% | 6,7% | +1,1 | 1,00 | 16,7% | +11,1 | **0,002** | 10,4–25,7 |

*(gráfico 07; p do McNemar exato contra A0)*

- **Três modelos cruzam a meta de 70%** com a biblioteca recuperada: Granite 76,7%, `qwen2.5-coder:7b` 72,2% e `qwen2.5:7b` 70,0%. Nenhum chegava lá sem ela (**H3 confirmada**).
- **A2 ≥ A1 em todos os seis modelos** — e não só nos pequenos, como a literatura previa (**H2 confirmada, mais forte que o previsto**). No Granite a biblioteca inteira *piora* 5,6 pp; o verbete certo está no contexto 100% das vezes em A1 e mesmo assim o acerto cai (a sintática, onde ele acertava 93%, cai a 53%). É o *Context Rot* medido em casa: ~6 mil tokens de documentação, com o verbete certo dentro, rendem menos que 3 verbetes de ~1 mil tokens.
- **O maior ganho é do `qwen2.5-coder:3b`: +40 pp**, de 23,3% a 63,3%, sem perder um único caso (36 casos ganhos, 0 perdidos). Com a biblioteca recuperada ele fica a 3 pp do Granite sem biblioteca — a **1/4 do tempo** (29,7 s contra 83 s por caso no i5) e com 2,3 GB de RAM. O colapso em `corpo_nao_e_json` cai de 47% para 16% das respostas e ele passa a usar 24 rótulos em vez de 15 (**H4 confirmada**).
- **O `phi4-mini` não aproveita documentação nenhuma**: cita um verbete recebido em 0% (A1) e 12% (A2) das respostas. A biblioteca inteira reduz os rótulos inventados (23,3% → 3,3%) sem melhorar o acerto. É falha de seguir instrução, e contexto não a corrige.
- O `1.5b` sobe de 5,6% para 16,7% (significativo), mas continua respondendo `corpo_nao_e_json` em 78% dos casos e fica 2× mais prolixo (228 tokens de saída). Não faz a tarefa.

## 4. O teto é a recuperação, não o raciocínio

| Modelo | A3 (só o verbete certo) | A2 com o verbete certo entre os 3 (n = 71) | A2 sem (n = 19) |
|---|---|---|---|
| `granite4.2:8b` | **100,0%** (IC 95,9–100) | 91,5% | 21,1% |
| `qwen2.5:7b` | — | 81,7% | 26,3% |
| `qwen2.5-coder:7b` | — | 81,7% | 36,8% |
| `qwen2.5-coder:3b` | **92,2%** (IC 84,8–96,2) | 77,5% | 10,5% |
| `phi4-mini:3.8b` | 51,1% | 31,0% | 5,3% |
| `qwen2.5-coder:1.5b` | — | 21,1% | 0,0% |

*(gráficos 08 e 11)*

Com o verbete certo e só ele, o Granite acerta **todos os 90 casos** e o 3B, 83 de 90. Em A2 o recuperador coloca o verbete certo entre os três em **78,9%** dos casos — exatamente o hit@3 medido offline antes de rodar (achado 4.19), porque a recuperação é determinística — e, quando ele está lá, o Granite acerta 91,5%; quando não está, 21,1%. **A distância entre 76,7% (A2) e 100% (A3) é quase toda falha de recuperação.** Cada ponto de hit@3 vale, no Granite, cerca de 0,7 pp de acerto; levar o recuperador de 79% a 95% colocaria o Granite perto de 90% e o 3B perto de 75%.

Onde a recuperação falha, por classe (verbete certo entre os 3): léxica 93%, sintática 87%, efeito 87%, semântica 80%, runtime 80%, **tradução 47%**. É a classe de escala de preço, chave de junção e contagem — o sintoma vem em linguagem de negócio ("preços cem vezes maiores", "nome de outra pessoa") sem nenhum sinal estrutural que o código consiga extrair, e o BM25 sobre o texto não alcança o verbete.

## 5. O efeito por classe: onde a documentação age

Média dos seis modelos, acerto de causa:

| Classe | A0 | A1 | A2 | Δ A2−A0 | verbete certo no top-3 |
|---|---|---|---|---|---|
| Léxica | 52,2 | 57,8 | 72,2 | **+20,0** | 93,3% |
| Sintática | 35,6 | 24,4 | 54,4 | **+18,8** | 86,7% |
| Semântica | 35,6 | 37,8 | 55,6 | **+20,0** | 80,0% |
| Tradução | 22,2 | 26,7 | 26,7 | +4,5 | 46,7% |
| Runtime | 60,0 | 66,7 | 67,8 | +7,8 | 80,0% |
| Efeito | 21,1 | 34,4 | 47,8 | **+26,7** | 86,7% |

**H1 confirmada pela metade.** Efeito — a segunda classe mais difícil da 2-A — é a que mais ganha (+26,7 pp): o modelo passa a saber o que `produtos_api.php` faz com cada campo. Tradução, a mais difícil, **quase não ganha (+4,5 pp)** — não porque a documentação não sirva (em A3 o Granite acerta 100% dela), mas porque o recuperador não a entrega. A sintática em A1 cai (35,6 → 24,4): a biblioteca inteira é onde a distração pesa mais. Por nível, A2 sobe os três em ~17–20 pp; o nível 3 (lógica entre requisições) vai de 33,3% a 53,9%.

**Com × sem verbete de defeito conhecido** (a marcação da decisão 21): casos cuja causa tem verbete de defeito dedicado vão de 28,0% (A0) a 48,7% (A2); os demais, de 41,5% a 56,2%. **O ganho existe nos dois grupos** — não é consulta de gabarito, é raciocínio ancorado na descrição do sistema.

## 6. Adesão cega: a documentação é tratada como verdade — mesmo errada

| Modelo | A0 | A4: 3 verbetes plausíveis errados | respondeu a causa de um deles | A5: verbete errado + registro falso | seguiu a causa plantada |
|---|---|---|---|---|---|
| `granite4.2:8b` | 66,7% | **22,2%** (−44,5) | 73,3% | **6,7%** (−60,0) | **93,3%** |
| `qwen2.5-coder:3b` | 23,3% | 8,9% (−14,4) | 83,3% | 4,4% (−18,9) | **95,6%** |
| `phi4-mini:3.8b` | 23,3% | 14,4% (−8,9) | 21,1% | 5,6% (−17,7) | 30,0% |

*(gráfico 08; todas as quedas significativas, p ≤ 0,04)*

É o resultado mais importante da fase para o desenho do agente. Três verbetes plausíveis mas errados derrubam o Granite de 66,7% para 22,2% — abaixo do que ele acertava **sem documentação nenhuma** — e ele responde a causa de um dos distratores em 73% dos casos. Um único verbete errado acompanhado de um "registro de incidente" falso leva Granite e 3B a repetir a causa plantada em **93–96%** das respostas. Quanto melhor o modelo lê documentação, mais ele a obedece: o `phi4-mini`, que não a lê, é o menos afetado. A literatura previa adesão maior a evidência parafraseada (Li et al., ACL 2025) — os verbetes foram escritos assim de propósito, e o efeito veio inteiro, para o bem e para o mal.

**Consequência para a Fase 3:** a gestão da biblioteca pelo próprio modelo, prevista na decisão 13, precisa de validação por código como porta de entrada obrigatória. Um verbete errado não "ajuda menos" — envenena o diagnóstico quase sempre.

## 7. Quantização não explica o piso

`qwen2.5-coder:1.5b` no braço A0-linear, mesma máquina:

| Variante | Acerto | Respostas diferentes do Q4_K_M | flips ✓→✗ / ✗→✓ | Seg/caso |
|---|---|---|---|---|
| Q4_K_M (padrão) | 5,6% | — | — | 8,3 |
| q8_0 | 8,9% | 4 de 90 (4,4%) | 0 / 3 | 15,9 |
| fp16 | 8,9% | 4 de 90 (4,4%) | 0 / 3 | 17,0 |

*(gráfico 10)*

As duas precisões maiores mudam 4 respostas em 90 e recuperam 3 casos, nenhum perdido. O modelo de 1,5B falha por capacidade, não por quantização; e as variantes custam o dobro do tempo. Q4_K_M fica confirmado como padrão para todos os portes.

## 8. Custo na máquina-alvo

Mediana por caso, em segundos, no i5-1235U (prefill = ler o prompt; geração = escrever a resposta):

| Modelo | A0 prefill / ger. / total | A1 prefill / ger. / total | A2 prefill / ger. / total | Acerto A2 | Acerto por segundo (A2) |
|---|---|---|---|---|---|
| `granite4.2:8b` | 33,0 / 47,6 / **83,0** | 53,2 / 114,4 / 168,2 | 68,0 / 54,3 / **123,9** | 76,7% | 0,62 pp/s |
| `qwen2.5:7b` | 24,2 / 12,2 / 38,0 | 33,9 / 20,4 / 57,1 | 45,6 / 14,0 / **61,1** | 70,0% | 1,15 pp/s |
| `qwen2.5-coder:7b` | 23,5 / 25,5 / 51,3 | 34,9 / 21,4 / 61,2 | 45,7 / 15,7 / **66,6** | 72,2% | 1,08 pp/s |
| `qwen2.5-coder:3b` | 9,5 / 5,3 / 17,1 | 17,4 / 8,7 / 28,6 | 20,8 / 5,9 / **29,7** | 63,3% | **2,13 pp/s** |
| `phi4-mini:3.8b` | 14,4 / 5,9 / 22,6 | 20,8 / 19,4 / 42,7 | 24,8 / 8,9 / 35,6 | 25,6% | 0,72 pp/s |
| `qwen2.5-coder:1.5b` | 3,4 / 2,6 / 8,3 | 8,7 / 5,6 / 17,7 | 9,5 / 15,4 / 25,3 | 16,7% | 0,66 pp/s |

*(gráfico 09)*

- **O cache de prefixo funcionou na máquina-alvo**: o prefill de A1 (prompt de ~5,8 mil tokens) custa 1,5–1,8× o de A0 (~550 tokens), não 10×. Já A2 custa **mais prefill que A1** (68 s contra 53 s no Granite) porque o prefixo recuperado muda a cada caso e não é reaproveitado — exatamente o que a Verificação 0 no Ryzen (achado 4.21) previa. Ainda assim A2 é mais barato no total, porque A1 faz os modelos gerarem mais texto (o Granite passa de 47 s para 114 s de geração).
- A biblioteca recuperada custa, no total, **1,5× o tempo de A0** (Granite) a **1,7×** (3B). Na máquina corporativa, um diagnóstico do 3B com biblioteca sai em 30 s; do `qwen2.5:7b`, em 61 s; do Granite, em 124 s.
- Na fronteira de custo × acerto ficam três pontos: **`qwen2.5-coder:3b` + A2** (63% a 30 s, 2,3 GB), **`qwen2.5:7b` + A2** (70% a 61 s, 5,2 GB) e **Granite + A2** (77% a 124 s, 6,6 GB). Os demais são dominados.

## 9. Perfil por modelo, com a biblioteca

### `granite4.2:8b` — 76,7% com recuperação; 100% com o verbete certo
Ganha 10 pp com A2 (p = 0,12 — o IC de 90 casos não fecha, mas o teto de 100% em A3 e os 91,5% com o verbete presente dizem que o limite é o recuperador). Perde com a biblioteca inteira. Cita o verbete recebido em 100% das respostas — e é justamente por isso o mais vulnerável a documentação errada (93% de adesão à causa plantada). Custo alto no i5: 124 s por caso em A2. **Papel:** referência de acurácia; só vale como padrão se o tempo couber no fluxo.

### `qwen2.5-coder:7b` — 72,2%, o maior salto entre os 7B
De 50,0% a 72,2% (p = 0,0005). Efeito 26,7 → 73,3, sintática 46,7 → 73,3. É o único, além do 3B, em que a biblioteca inteira também ajuda de forma clara (+13,3), mas ela o faz cortar 6 respostas no teto de 600 tokens. Entre máquinas, é o menos estável (69% de respostas idênticas). **Papel:** alternativa ao generalista; não domina o `qwen2.5:7b` em custo.

### `qwen2.5:7b` — 70,0%, melhor acurácia por segundo acima da meta
+12,2 pp (p = 0,07). Léxica 40 → 86,7 (o maior ganho de classe do modelo); tradução cai de 60 para 46,7 — quando o recuperador erra, o verbete errado o afasta do que ele acertaria sozinho. 61 s por caso. **Papel:** candidato a padrão quando houver 6,5 GB livres.

### `qwen2.5-coder:3b` — 63,3%, de "não sustenta a tarefa" a candidato corporativo
+40 pp, sem perder caso. Sintática 13 → 73, semântica 13 → 53, tradução 0 → 40, efeito 0 → 47. A3: 92,2%. Adesão cega máxima (95,6%). 30 s por caso, 2,3 GB. **Papel:** o padrão natural para a máquina corporativa, desde que a biblioteca seja confiável.

### `phi4-mini:3.8b` — não lê a documentação
Sem ganho (25,6%); cita verbete em 12%; com o verbete certo e só ele chega a 51%, mas não consegue apontá-lo. Reduz rótulos inventados com a biblioteca inteira (3,3%) sem acertar mais. **Papel:** descartado.

### `qwen2.5-coder:1.5b` — o piso é o modelo
16,7% com A2, ainda 78% de `corpo_nao_e_json`, 2× mais prolixo; q8_0/fp16 não mudam o quadro. **Papel:** descartado.

## 10. Comparação com a Fase 2-A ("teste 1")

| | Fase 2-A (Ryzen, sem biblioteca) | Fase 2-B (i5, biblioteca recuperada) |
|---|---|---|
| Melhor acerto | 67,8% (`granite4.2:8b`) | **76,7%** (`granite4.2:8b`) |
| Modelos acima de 70% | nenhum | 3 (Granite, `coder:7b`, `qwen2.5:7b`) |
| Melhor custo-benefício | `qwen2.5:7b` 53,3% a 17 s | `qwen2.5-coder:3b` **63,3% a 30 s** (i5) |
| Efeito da estrutura de prompt | estágios não ajudam; nomes irrelevantes | (prompt fixo em linear) |
| Efeito do conhecimento do sistema | — | +10 a +40 pp conforme o modelo; +20 pp na média das classes que a recuperação alcança |
| Classe mais difícil | tradução (18,9%) | tradução (26,7%) — limitada pela recuperação, não pelo modelo |
| Modos de falha | confusão entre vizinhos; colapso num rótulo; rótulo inventado | o colapso do 3B se desfaz; o rótulo inventado do phi4 persiste; **surge a adesão cega** |

A lição das duas fases junta é uma frase: **para esta tarefa, saber do sistema vale mais que raciocinar em etapas** — e o modelo pequeno com documentação alcança o grande sem ela.

## 11. Ameaças à validade

- **Uma execução por condição**, temperatura 0,1; os ICs cobrem a amostragem de casos, não a variação entre execuções (que a seção 2 estima em 2–9% de respostas diferentes entre máquinas, 31% no `coder:7b`).
- **Recuperação determinística e comum**: os seis modelos receberam os mesmos 3 verbetes por caso — a variância de A2 é toda do modelo, e o hit@3 de 78,9% é uma constante do experimento, não do modelo.
- **A5 é um pior caso construído** (verbete errado + registro falso afirmando a causa); A4 usa os verbetes mais parecidos com o caso que não são o certo — o cenário realista de uma biblioteca com erro.
- Os 6 casos do `coder:7b` cortados em A1 contam como erro (sem eles, A1 subiria de 63,3% a 67,9%).
- Os 4 casos que contradizem o código (achado 4.20) foram mantidos; com o verbete certo o Granite acerta os 4, então a contradição não impediu o diagnóstico.
- O log da máquina-alvo com a Verificação 0 não foi versionado; o efeito do cache é inferido dos prefills.
- Só português, só Q4_K_M nos seis principais, uma máquina por fase.

## 12. Conclusões e o que decidir agora

1. **A biblioteca recuperada é o modo de operação do agente**: +10 a +40 pp, três modelos acima de 70%, custo de 1,5–1,7× o tempo sem biblioteca. A biblioteca inteira no prompt fica descartada como modo padrão.
2. **O próximo ganho está no recuperador**, não no modelo: hit@3 de 79% limita o Granite a 77%; o alvo de 95% é alcançável (hit@5 já é 90%) — testar k = 5, sinais em código para a classe de tradução e o embedding denso (`embeddinggemma`) como ablação offline, sem gastar inferência.
3. **Documentação errada é veneno, não ruído**: 93–96% de adesão à causa plantada. A gestão da biblioteca pelo modelo (Fase 3) só pode existir atrás de validação por código; e vale medir, na Fase 3, se pedir ao modelo para *confrontar* o verbete com a evidência reduz a adesão.
4. **Padrão de produção para a máquina corporativa** — decisão do Eric entre: `qwen2.5-coder:3b` + A2 (63%, 30 s, 2,3 GB; licença de pesquisa), `qwen2.5:7b` + A2 (70%, 61 s, 5,2 GB; Apache 2.0) e Granite + A2 (77%, 124 s, 6,6 GB; Apache 2.0).
5. `phi4-mini` e `qwen2.5-coder:1.5b` saem da comparação; Q4_K_M confirmado.
6. Corrigir os quatro fixtures do achado 4.20 antes de qualquer nova bateria; a partir daqui, a comparabilidade com a 2-A não precisa mais ser preservada caso a caso.
