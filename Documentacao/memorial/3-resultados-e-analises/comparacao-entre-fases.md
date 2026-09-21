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
# Comparação entre as fases

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Relatórios de cada fase em [fase-2a-relatorio-por-modelo.md](fase-2a-relatorio-por-modelo.md), [fase-2b-relatorio-por-modelo.md](fase-2b-relatorio-por-modelo.md) e [fase-3-relatorio-por-modelo.md](fase-3-relatorio-por-modelo.md). As tabelas deste arquivo são coladas de `resultados_alvo/fase3/comparacao_fases.md`, gerado por `comparar_fases.py` a partir de `experimentos/avaliacao.json` (2-A), `resultados_alvo/avaliacao.json` (2-B) e `resultados_alvo/fase3/avaliacao_fase3.json`. **Nenhum número é digitado à mão.** Gráficos 16 `comparacao-entre-fases` e 17 `custo-versus-acerto-tres-fases`.

<!-- ! Alteração de IA - Revisar: linha de estado nova (21/09/2026); a anterior fica como histórico, sem negrito.
     ! Motivo: a bateria da Fase 3 rodou em 13–15/09/2026 e `comparacao_fases.md` já existe em `resultados_alvo/fase3/`; o cabeçalho dizia "bateria não executada". §3–§6 são preenchidas pelo plano complementar de 21/09. -->
> **Estado em 21/09/2026: bateria concluída (13–15/09/2026); `comparacao_fases.md` gerada em 15/09 18:44; §3–§6 em preenchimento pelo plano complementar de 21/09/2026.**
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

*(a preencher: colar a tabela por modelo de `comparacao_fases.md`, recorte `nos_36_avaliacao` primeiro, depois `nos_90`)*

## 4. Ganhos, riscos e perdas de cada fase

### Fase 2-A — sem conhecimento do sistema
- **Ganhos:** *(a preencher)*
- **Riscos:** *(a preencher)*
- **Perdas:** *(a preencher)*

### Fase 2-B — biblioteca compartilhada, só leitura
- **Ganhos:** *(a preencher)*
- **Riscos:** *(a preencher)*
- **Perdas:** *(a preencher)*

### Fase 3 — biblioteca escrita pelo próprio modelo
- **Ganhos:** *(a preencher)*
- **Riscos:** *(a preencher)*
- **Perdas:** *(a preencher)*

## 5. Reprodutibilidade entre execuções

O pareamento **2-B A2 × Fase 3 L0** compara duas execuções da mesma condição, na mesma máquina, com o mesmo prompt e a mesma biblioteca. É a única medida do projeto sobre quanto o resultado varia sozinho, e ela calibra a leitura de todas as outras diferenças.

*(a preencher: `n_comuns`, b/c, Δ, p, nos 36 e nos 86 casos não alterados; se a diferença for grande, vira achado próprio em `achados-dos-modelos.md`)*

## 6. Decisão do modelo final

*(a preencher após a bateria da Fase 3 e a revisão humana das edições — escolha pela acurácia balanceada nos 36 de avaliação, com veto por autoenvenenamento, custo por caso na máquina-alvo e licença do modelo como critérios de desempate; ver decisão 36 e a pendência do padrão de produção em `../pendencias.md`)*
