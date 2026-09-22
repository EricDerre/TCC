<!-- ! Alteração de IA - Revisar: arquivo criado em 22/09/2026 (P2 do plano complementar de 21/09/2026) com a análise
     decisória do modelo final do TCC: pergunta, regra pré-registrada, resultado, robustez, custo, riscos, o que a literatura
     previa, decisão, limitações e o que a Fase 3-B acrescentaria. As tabelas são blocos `<!-- tabela:NOME -->` colados de
     `resultados_alvo/fase3/tabelas_relatorio.md` (seções de `decisao_modelo.md` reexpostas como `dm_*` por
     `gerar_tabelas_relatorio_fase3.py`, conferidas por `--check`); os demais números vêm do relatório da Fase 3, com o campo
     citado na primeira menção.
     ! Motivo: a decisão do modelo é o resultado central do TCC e precisava de um documento único que a banca leia de ponta a
     ponta — regra antes do dado, robustez depois, riscos e limites por último — sem número digitado à mão e sem
     depender do chat em que foi tomada. -->
# Análise decisória — o modelo final e o estado da biblioteca

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Números de `resultados_alvo/fase3/decisao_modelo.md` (gerado por `decidir_modelo.py`; `--check` limpo em 22/09/2026), de `resumo_fase3.json` e de `comparacao_fases.md`, citados pelo campo; leitura completa da bateria em [fase-3-relatorio-por-modelo.md](fase-3-relatorio-por-modelo.md) e das três fases em [comparacao-entre-fases.md](comparacao-entre-fases.md); o que a literatura previa está no [mapa de decisões](../2-pesquisa-e-literatura/mapa-de-decisoes-fase-3.md) (§6.10). Decisões 36, 46, 47 e 52 em [decisoes.md](../1-decisoes-e-historico/decisoes.md).

> **Estado em 22/09/2026: decisão tomada — `qwen2.5:7b` com a biblioteca no estado L1 — pela regra pré-registrada, confirmada pelo Eric (decisão 52). Ponte de versão feita em três modelos; Granite sem ponte. Revisão das edições em primeira passada por IA. Testes da Fase 3-B a escolher (§10).**

## 1. A pergunta

Qual modelo local, e com que estado da biblioteca de conhecimento (L0 original ou L1..L3 editada pelo próprio modelo), passa a ser o padrão do agente de QA nas fases seguintes (interceptador Playwright e cura de seletor)? A pergunta tem duas partes porque a Fase 3 mostrou que o estado da biblioteca muda o acerto tanto quanto o modelo (relatório §3), e porque a biblioteca de produção é uma cópia concreta — a pasta `epoca-N` de um modelo —, não uma abstração.

## 2. A regra, escrita antes do dado

A ordem dos critérios foi fixada antes da bateria (decisão 36, 11/09/2026) e reafirmada antes da leitura dos resultados (decisão 46, 21/09/2026), para a escolha não parecer ajustada ao que saiu:

1. **Regra 36**: ranking por acurácia balanceada nos 36 casos de avaliação (macro-recall por causa raiz, `acuracia_balanceada_pct` — a métrica que penaliza colapso num rótulo, COLLOT et al., 2026; mapa, linha 1); **veto** quando o autoenvenenamento máximo nos 36 (`flips` → `autoenvenenamento_pct`) passa de 10%; desempate por licença mais permissiva, depois pela época mais baixa.
2. **Robustez** (só depois): bootstrap por caso (2.000 réplicas, semente 20260921) com intervalo de 95% e P(top-1); estabilidade do ranking por corte; fronteira de Pareto (acurácia × segundos × risco); escore ponderado com pesos declarados em `pesos_decisao.json` antes de olhar o resultado (0,5 acurácia balanceada; 0,1 acerto; 0,2 custo; 0,2 risco) e varredura de sensibilidade — o escore não decide, só diz quão frágil a decisão é.
3. **Ponte de versão** obrigatória antes de qualquer inferência nova entrar na mesma tabela (decisão 47), porque o Ollama passou de 0.34.0 para 0.34.1 depois da bateria.

Os quatro candidatos são os modelos da Fase 3 — `granite4.2:8b`, `qwen2.5:7b`, `qwen2.5-coder:7b`, `qwen2.5-coder:3b` — em cada uma das quatro versões da biblioteca, 16 combinações (modelo, L).

## 3. O resultado da regra

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

**`qwen2.5:7b` em L1** vence por 5,5 pontos sobre a própria L3 e por 8,4 sobre o Granite (que é o mesmo número em L0..L3 porque não editou a biblioteca). Nenhum veto: o autoenvenenamento máximo é 5,6% no vencedor e 0,0–2,8% nos demais. A licença não separa ninguém (os quatro são Apache-2.0).

## 4. Robustez

**Bootstrap por caso.** Em 2.000 reamostragens dos 36 (e dos 90), a combinação com a maior acurácia balanceada é `qwen2.5:7b`/L1 em **77,6%** das réplicas nos 36 e em **50,0%** nos 90; o segundo colocado é a própria L3 do mesmo modelo (15,2% e 17,2%). Somando as versões editadas do `qwen2.5:7b`, o modelo é o primeiro em 92,8% das réplicas nos 36. O intervalo de 95% da acurácia balanceada de L1 nos 36 é largo — [81,9–97,8]% — e sobrepõe o do Granite ([70,6–92,8]%): a vantagem é provável, não certa.

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

**Estabilidade do ranking.** Em 36 cortes (colunas de `comparacao_fases.json` nos 36 e nos 90, e classes de defeito nos 90), o Granite fica em primeiro em 16 e o `qwen2.5:7b` em 14 — o Granite é o mais estável nos cortes antigos (2-A, 2-B, L0) e por classe; o `qwen2.5:7b` domina os cortes das versões editadas. Lido com a coluna "Nº de cortes em 1º", o resultado diz que a escolha depende de a biblioteca editada valer: **sem edição (L0), o Granite é o melhor modelo** (83,3% contra 81,2% nos 36); com L1, o `qwen2.5:7b` passa à frente.

<!-- tabela:dm_estabilidade -->
36 cortes (por coluna de comparacao_fases.json nos 36/90 casos, e por classe de defeito nos 90 casos -- resumo_fase3.json não desmembra a classe por partição), cada um com o ranking dos modelos por acurácia balanceada; abaixo, em quantos cortes cada modelo ficou em 1º.

| Modelo | Nº de cortes em 1º (de 36) |
|---|---|
| granite4.2:8b | 16 |
| qwen2.5:7b | 14 |
| qwen2.5-coder:7b | 5 |
| qwen2.5-coder:3b | 1 |
<!-- /tabela:dm_estabilidade -->

**Fronteira de Pareto** (acurácia balanceada nos 36 × segundos por caso, mediana nos 36 × risco = média de autoenvenenamento, adesão cega, fora do conjunto e formato-ok-conteúdo-errado): quatro combinações não dominadas — o 3B em L1 e L2 (barato, 17,8–18,8 s, risco 31,6 pela adesão cega de 95,6% em A5) e o `qwen2.5:7b` em L1 e L3. O Granite e o Coder 7B são dominados pelo `qwen2.5:7b`: mais lentos ou menos certeiros sem serem menos arriscados.

<!-- tabela:dm_pareto -->
Maximizando acurácia balanceada (36) e minimizando segundos (mediana, 36) e risco (média simples de autoenvenenamento máximo, adesão cega, fora do conjunto e formato-ok-conteúdo-errado); 16 candidatos com os três números disponíveis (0 excluídos por dado incompleto). Não dominado = nenhum outro (modelo, L) é ao mesmo tempo mais certeiro, mais barato e menos arriscado.

| Modelo | L | Acurácia balanceada (36) | Segundos (mediana, 36) | Risco | Vetado |
|---|---|---|---|---|---|
| qwen2.5-coder:3b | L1 | 70,4% | 17,8 | 31,6 | não |
| qwen2.5-coder:3b | L2 | 71,2% | 18,8 | 31,6 | não |
| qwen2.5:7b | L1 | 91,7% | 79,5 | 5,6 | não |
| qwen2.5:7b | L3 | 86,2% | 53,9 | 7,4 | não |
<!-- /tabela:dm_pareto -->

**Escore ponderado e sensibilidade.** Com os pesos declarados, `qwen2.5:7b`/L1 soma 0,9 e a L3 0,8. A varredura de 0 a 1 em cada peso, renormalizando os outros, troca o vencedor em três pontos: com o peso da acurácia balanceada abaixo de 0,15 a L3 passa à frente da L1 (a L3 é mais barata na tabela, §5); com o peso do custo em 0,50 idem; e com o peso do custo em 0,75 o 3B em L1 vence. O peso do acerto simples e o do risco não mudam o vencedor em nenhum ponto. **Só uma preferência forte por custo tira a decisão do `qwen2.5:7b`**, e a primeira alternativa é a outra versão do mesmo modelo.

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

## 5. Custo

Na máquina-alvo (i5-1235U, só CPU; relatório §9): o `qwen2.5:7b` custa 66,8 s por diagnóstico com L0 e 78,2 s com L1 nos 90 (`segundos_mediana`; 69,5 e 79,5 s nos 36), 155–175 s por proposta, 13h53 na bateria inteira — contra 131,3 s por diagnóstico e 26h58 do Granite e 30,8 s e 05h02 do 3B. A biblioteca anotada encarece o prefill (51,1 → 61,6 s no diagnóstico), como o mapa previa (linha 9). O custo da L3 na tabela do Pareto (53,9 s nos 36) é o da passada final, medida sem propostas intercaladas e com o cache do runtime em outro estado; não é evidência de que a L3 seja mais barata que a L1 (relatório §9, cuidado 2). Na Fase 4 o que importa é o custo de um diagnóstico com L1, e ele reproduz entre corridas: a ponte de versão deu 68,0 s para L0 nos 36 (69,5 s na bateria).

## 6. Riscos

- **Autoenvenenamento** (H5): 5,6% no máximo nos 36 (`qwen2.5:7b`, L1→L2: os dois casos ganhos em L1 que L2 devolve, `sin-14` e `run-10`), 9,3% nos 54 (Coder 7B, L2→L3). Sob o teto declarado; não é veto.
- **Qualidade das edições** (revisão em primeira passada por IA, decisão 53; relatório §7): 23 corretas, 17 parciais e 23 erradas em 63; no vencedor, 12 de 29 erradas (41,4%) e nenhuma correta que o verbete já não dissesse; nas 10 edições da época 1 — a L1 escolhida — 3 erradas. O ganho de L1 não pode ser creditado à verdade do conteúdo (achado 4.35), e a cópia de produção precisa de curadoria (§8).

<!-- tabela:dm_revisao -->
Fonte: planilhas revisao_edicoes__<slug>.md lidas direto da pasta da corrida.

| Modelo | n | Correta | Parcial | Errada | Sem avaliação |
|---|---|---|---|---|---|
| qwen2.5-coder:3b | 10 | 40,0% | 20,0% | 40,0% | 0,0% |
| qwen2.5-coder:7b | 24 | 41,7% | 29,2% | 29,2% | 0,0% |
| qwen2.5:7b | 29 | 31,0% | 27,6% | 41,4% | 0,0% |
<!-- /tabela:dm_revisao -->

- **Recuperação**: hit@3 nos 90 de 80,0 (L0) para 77,8 (L1) e MRR de 0,596 para 0,580 no `qwen2.5:7b` — a biblioteca maior piora levemente o recuperador (IDF do BM25; mapa, linha 22); nenhum verbete novo recuperado nos 36 (`verbete_novo_no_contexto_pct` = 0,0).
- **Saturação**: 40 → 12 → 9 edições aceitas por época; `duplicada` e `teto_notas_verbete` dominam as rejeições das épocas 2 e 3 (achado 4.32). Não é risco para L1; é o motivo de L1 ser o pico.
- **Colapso num rótulo e rótulo inventado**: não ocorrem (parcela máxima do rótulo mais frequente 11,1% no `qwen2.5:7b` nos 36; fora do conjunto ≤ 2,8%).
- **Ponte de versão** (decisão 47): três modelos pareáveis com a Fase 3 sob 0.34.1 — 3B b/c 0/0, Coder 7B 0/0, `qwen2.5:7b` 1/1 (p = 1,0); o Granite não rodou (8 GB de RAM exigidos, 7,8 GB livres em duas tentativas) e saiu da 3-B (decisão 52).

<!-- tabela:dm_3b -->
### fase3b_ponte (modo `ponte`)

| Modelo | L | n | Acerto | Acurácia balanceada | n comuns c/ F3 | b | c | p (McNemar) | p (Holm) | g de Cohen |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen2.5-coder:3b | L0 | 36 | 69,4% | 68,8% | 36 | 0 | 0 | 1,0000 | 1,0000 | — |
| qwen2.5-coder:7b | L0 | 36 | 75,0% | 80,0% | 36 | 0 | 0 | 1,0000 | 1,0000 | — |
| qwen2.5:7b | L0 | 36 | 77,8% | 78,8% | 36 | 1 | 1 | 1,0000 | 1,0000 | 0,0 |
<!-- /tabela:dm_3b -->

## 7. O que a literatura previa

Das 28 linhas do mapa de decisões (§6.10.1, coluna "Resultado medido na Fase 3", preenchida em 22/09/2026), as que pesam na decisão:

| Previsão (mapa) | Medido |
|---|---|
| Acurácia balanceada como métrica primária, por penalizar colapso (linha 1) | Aplicada; nenhum colapso ocorreu, então acerto e acurácia balanceada ordenam os modelos quase igual — a exceção é o Granite, 80,6% de acerto e 83,3% balanceada nos 36 |
| Subida e regressão da automelhoria; reportar o melhor L (linhas 8, 23) | Confirmado: pico em L1 e regressão no `qwen2.5:7b` e no Coder 7B nos 90 (achado 4.34) |
| Ganho atenuado em curadores pequenos; o 8B barrado é política, não porte (linhas 10, 11) | Confirmado: 3B com +2,8 pp; Granite com 0 de 181 por `texto_longo` (achado 4.30) |
| Sem oráculo externo a autocorreção degrada; documentação errada é obedecida (linhas 13, 15) | O validador em código segurou a forma (658 rejeições) mas não a verdade (23 de 63 erradas); o autoenvenenamento ficou baixo mesmo assim |
| Agentes não usam o que escreveram; ablação necessária antes de creditar o ganho ao conteúdo (linha 17) | Não rodada; a revisão das edições aponta no mesmo sentido — o ganho vem da forma (notas no contexto, frontmatter), não da verdade (achado 4.35) |
| n = 36 não resolve; efeito mínimo antes do p (linhas 5, 6) | 19,4 pp de efeito mínimo; maior ganho 11,1 pp; nenhum p < 0,05 (achado 4.33) |
| Runtime muda; ponte antes de misturar tabelas (linha 21) | Feito: 0/0, 0/0, 1/1 nos 36; 2-B A2 × F3 L0 idêntico em 6 de 8 (achado 4.31) |
| Custo por acerto e Pareto, com prefill separado de geração (linhas 27, 16 da §6.10.3) | Feito (§4 e §5) |

## 8. Decisão

<!-- tabela:dm_frase -->
Pela regra pré-registrada (passo 1), o modelo recomendado para produção é **qwen2.5:7b** com a biblioteca no estado **L1** (91,7% de acurácia balanceada nos 36 casos de avaliação, sem veto por autoenvenenamento). O escore ponderado (passo 5) concorda com essa escolha.

A fronteira de Pareto (passo 4) tem 4 combinação(ões) não dominada(s). A varredura de sensibilidade (passo 5) trocou o vencedor em 3 ponto(s) dos pesos varridos.
<!-- /tabela:dm_frase -->

**Modelo do TCC: `qwen2.5:7b`. Estado da biblioteca: L1** (`resultados_alvo/fase3/bibliotecas/qwen2.5_7b/epoca-1/`, hash `3394d203cab9`). Confirmado pelo Eric em 22/09/2026 (decisão 52) com o Granite sem ponte de versão: o Granite não vence em critério nenhum da decisão, não editou a biblioteca e o reteste com teto de texto maior exigiria RAM que a máquina não tem.

**O que vai para a produção.** A regra escolhe o estado *medido*; o estado *implantado* é o medido menos o que a revisão humana reprovar. A cópia L1 tem 40 edições da época 1 (12 notas, 22 retificações, 6 verbetes novos); 10 foram revisadas (3 erradas: a retificação em `contrato-produto` sobre "nomes diferentes para o campo tipo", o verbete novo `conversao-de-unidade` e a retificação em `dado_desatualizado` sobre a API ler dados antigos do banco). Antes da Fase 4: revisar as 30 restantes, remover as reprovadas numa **cópia** (o snapshot oficial não muda) e registrar o hash da cópia curada. É pendência do Eric em [pendencias.md](../pendencias.md), junto com o padrão de `install.py`.

**O que a decisão não diz.** Não diz que a biblioteca escrita pelo modelo é melhor que a original por conter conhecimento verdadeiro — diz que, medida nos 36 casos nunca vistos, a versão L1 produziu 4 acertos a mais e nenhum a menos, com custo de prefill maior e notas de qualidade duvidosa. E não diz que o `qwen2.5:7b` é melhor que o Granite em geral: sem edição, o Granite acerta mais e é mais estável entre cortes; com edição, só o `qwen2.5:7b` conseguiu escrever no formato exigido.

## 9. Limitações

1. **Amostra**: 36 casos de avaliação; efeito mínimo detectável de 19,4 pp; a decisão é por convergência de critérios, sob incerteza declarada (P(top-1) 77,6%).
2. **Teste reutilizado**: os 36 são os mesmos da 2-B e foram vistos em quatro passadas por modelo; o contraste com os 54 (H3) e `tentativas_de_decorar` = 0 não indicam memorização, mas só casos inéditos fecham a questão (ZHU et al., 2025; mapa, risco 6).
3. **Revisão das edições por IA**, um único revisor, vereditos provisórios (decisão 53).
4. **Custo por versão** medido em momentos diferentes da mesma corrida (relatório §9); o custo de L1 é o número que vale, e ele é maior que o de L0.
5. **Granite sem ponte e sem reteste**: a leitura "barrado pelo formato, não incapaz" (4.30) fica como hipótese plausível, não medida.
6. **Uma execução por condição**, temperatura 0,1, sem semente; o ruído medido é de 0 a 2 casos em 36 (4.31).
7. **Escritor e leitor confundidos**: a biblioteca L1 do `qwen2.5:7b` só foi lida por ele; se o ganho é da biblioteca ou do leitor, só a troca cruzada diz.

## 10. O que a Fase 3-B acrescentaria — para o Eric escolher

Menu do plano complementar (decisão 45), com o que a análise mostrou. O Granite está fora de todos (decisão 52); as horas são estimativas pelas medianas da bateria e da ponte.

| Item | Pergunta que fecha | Inferências / horas | O que acrescenta à decisão | Recomendação |
|---|---|---|---|---|
| **(b) Troca cruzada**: L1 e L3 do `qwen2.5:7b` lidas por `qwen2.5-coder:7b` e `qwen2.5-coder:3b`, nos 36 (`rodar_fase3b.ps1 -Modo cruzada -Doador qwen2.5:7b`) | O ganho é da biblioteca ou de quem a lê? (limitação 7; ablação da linha 17 do mapa na forma que o executor já tem) | 144 / ~2,5 h (uma noite) | Se os outros leitores também ganham com a L1 do `qwen2.5:7b`, a biblioteca vale por si e pode ser o padrão para qualquer modelo; se não, o padrão é o par (modelo, biblioteca) | **Primeiro** — barato, sem autoria, responde à maior ressalva da decisão |
| **(a) 36 casos inéditos** (2 por célula classe × nível), `qwen2.5:7b` em L0, L1 e L3 e 3B em L0 e L1 | O ganho generaliza a casos nunca vistos? Com 72 casos o efeito mínimo cai para ~14 pp (4.33) | 180 / ~3 h de máquina + ~1 dia de autoria (Sonnet lendo só o código do cobaia) + 6 casos conferidos pelo Eric | Fecha a limitação 2 (teste reutilizado) — a ressalva que uma banca fará primeiro | **Segundo** — o teste mais forte; depende de autoria |
| (c) A5 sobre L3 nos 36 (`-Modo a5`) | A documentação própria muda a adesão cega? | 72 / ~1,3 h (dois modelos) | Mais um argumento sobre H5; não muda a decisão | Última prioridade |
| (d) Granite com `TEXTO_MAX` = 600 | O Granite documenta com teto maior? | 144 / ~6 h | Responderia a 4.30; não muda a decisão | **Inviável** por RAM (decisão 52) |
| (e) Réplicas com temperatura alta | — | — | — | Descartado no plano (o cliente não fixa semente; b = c = 0 já mede o determinismo prático) |

Ordem recomendada: **(b) numa noite; (a) depois da autoria; (c) só se sobrar máquina**. Cada item roda por `executar_fase3b.py` sobre cópias dos snapshots oficiais (nada em `resultados_alvo/fase3/` muda) e entra em `decisao_modelo.md` §6 por `--saidas-3b`.

## 11. Rastreabilidade

| Número | Onde nasce | Como conferir |
|---|---|---|
| Ranking, veto, bootstrap, Pareto, escore, sensibilidade, 3-B, revisão | `decisao_modelo.json` / `.md` | `python decidir_modelo.py --saida fase3 --saidas-3b fase3b_ponte --check` (com `RESULTADOS_DIR=resultados_alvo`) |
| Curvas, pareados, flips, efeito mínimo, recuperação, documentação, custo | `resumo_fase3.json` → `tabelas_relatorio.md` | `python gerar_tabelas_relatorio_fase3.py --saida fase3 --check` (confere também os blocos deste arquivo, do relatório e da comparação) |
| Três fases lado a lado | `comparacao_fases.md` | `python comparar_fases.py --check` |
| Ponte de versão | `resultados_alvo/fase3b_ponte/` | `python avaliar_fase3b.py --saida fase3b_ponte` regenera a avaliação da ponte |
| Vereditos das edições | `revisao_edicoes__<slug>.md` | Leitura humana; apurados por `decidir_modelo.py` |
