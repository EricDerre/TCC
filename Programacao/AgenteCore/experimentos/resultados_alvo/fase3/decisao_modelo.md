<!-- ! Alteração de IA - Revisar: gerado por decidir_modelo.py a partir de comparacao_fases.json, resumo_fase3.json e avaliacao_fase3.json -- NÃO editar à mão.
     ! Motivo: é o documento que decide o modelo e o estado da biblioteca (L0..L3) de produção do TCC; editar direto quebraria a garantia de que todo número do Memorial sai de script, e a próxima corrida de decidir_modelo.py sobrescreveria a edição sem avisar. -->

# Decisão de modelo e estado da biblioteca

## 1. Regra da decisão 36 (pré-registrada)

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

## 2. Bootstrap por caso (2000 réplicas, semente 20260921)

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

## 3. Estabilidade do ranking

36 cortes (por coluna de comparacao_fases.json nos 36/90 casos, e por classe de defeito nos 90 casos -- resumo_fase3.json não desmembra a classe por partição), cada um com o ranking dos modelos por acurácia balanceada; abaixo, em quantos cortes cada modelo ficou em 1º.

| Modelo | Nº de cortes em 1º (de 36) |
|---|---|
| granite4.2:8b | 16 |
| qwen2.5:7b | 14 |
| qwen2.5-coder:7b | 5 |
| qwen2.5-coder:3b | 1 |

## 4. Fronteira de Pareto

Maximizando acurácia balanceada (36) e minimizando segundos (mediana, 36) e risco (média simples de autoenvenenamento máximo, adesão cega, fora do conjunto e formato-ok-conteúdo-errado); 16 candidatos com os três números disponíveis (0 excluídos por dado incompleto). Não dominado = nenhum outro (modelo, L) é ao mesmo tempo mais certeiro, mais barato e menos arriscado.

| Modelo | L | Acurácia balanceada (36) | Segundos (mediana, 36) | Risco | Vetado |
|---|---|---|---|---|---|
| qwen2.5-coder:3b | L1 | 70,4% | 17,8 | 31,6 | não |
| qwen2.5-coder:3b | L2 | 71,2% | 18,8 | 31,6 | não |
| qwen2.5:7b | L1 | 91,7% | 79,5 | 5,6 | não |
| qwen2.5:7b | L3 | 86,2% | 53,9 | 7,4 | não |

## 5. Escore ponderado e sensibilidade

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

## 6. Fase 3-B

Sem 3-B: nenhuma das saídas em `--saidas-3b` tinha `avaliacao_fase3.json` no momento desta corrida.

## 7. Revisão humana

Nenhuma edição foi revisada manualmente até esta corrida -- a planilha revisao_edicoes__<slug>.md (avaliar_fase3.gerar_planilha_revisao) está vazia ou não foi preenchida.

## Frase da decisão

Pela regra pré-registrada (passo 1), o modelo recomendado para produção é **qwen2.5:7b** com a biblioteca no estado **L1** (91,7% de acurácia balanceada nos 36 casos de avaliação, sem veto por autoenvenenamento). O escore ponderado (passo 5) concorda com essa escolha.

A fronteira de Pareto (passo 4) tem 4 combinação(ões) não dominada(s). A varredura de sensibilidade (passo 5) trocou o vencedor em 3 ponto(s) dos pesos varridos.
