<!-- ! Alteração de IA - Revisar: relatório da comparação entre portes do Qwen2.5-Coder.
     ! Motivo: a metodologia (seção 3.2 do projeto de pesquisa) exige escolher o porte do
     modelo por comparação experimental, e não havia nenhum dado registrado. Todos os
     números abaixo foram medidos nesta máquina, não estimados. -->

# Fase 2 — Comparação dos portes do LLM local

## Como foi medido

- **Ollama 0.33.2**, modelos `qwen2.5-coder` nos portes 1.5B, 3B e 7B (quantização padrão do Ollama).
- **Somente CPU**, forçado por `num_gpu: 0` em toda inferência e **verificado** em `/api/ps`
  (`size_vram = 0` em todas as medições). Esta máquina tem uma GTX 1650 de 4 GB; medir com
  GPU inflaria o resultado e não sustentaria a afirmação de operar "sob restrições de
  hardware local" feita na seção 1.2.
- Máquina: AMD Ryzen 7 5800H (8 núcleos/16 threads), 15,4 GB de RAM, Windows 11.
- 3 repetições por combinação de modelo e tarefa; `temperature = 0.1`.
- Tarefas retiradas do cobaia real: diagnóstico de quebra de contrato em `GET /api/produtos`
  e cura de um localizador quebrado em `produtos_api.php`.
- Scripts: `benchmark_modelos.py`, `prompts_benchmark.py`, `teste_diff_previo.py`.

## Desempenho

| Modelo | Tarefa | Mediana (s) | Faixa (s) | Tokens ent./saída | Memória | Só CPU |
|---|---|---|---|---|---|---|
| qwen2.5-coder:1.5b | diagnóstico | 10,24 | 8,36–11,04 | 479/172 | 1116 MB | sim |
| qwen2.5-coder:1.5b | seletor | 2,49 | 2,30–2,50 | 369/10 | 1116 MB | sim |
| qwen2.5-coder:3b | diagnóstico | 5,98 | 5,68–6,16 | 479/52 | 2064 MB | sim |
| qwen2.5-coder:3b | seletor | 3,94 | 3,80–3,99 | 369/24 | 2064 MB | sim |
| qwen2.5-coder:7b | diagnóstico | 16,08 | 15,63–18,50 | 479/86 | 4828 MB | sim |
| qwen2.5-coder:7b | seletor | 6,45 | 5,39–6,55 | 369/22 | 4828 MB | sim |

Observação 1: **o 1.5B é o mais lento no diagnóstico apesar de ser o menor modelo**, porque é
de longe o mais prolixo (172 tokens de saída contra 52 do 3B). O tempo total é dominado pela
quantidade de texto gerado, não pelo tamanho do modelo — o que inverte a intuição de que o
menor porte seria sempre o mais rápido.

Observação 2: há variação entre execuções (o diagnóstico do 3B mediu 7,23 s numa rodada
anterior e 5,98 s nesta). Diferenças abaixo de ~1,5 s entre modelos não devem ser tratadas como
significativas; as separações que sustentam a decisão (3B contra 7B no diagnóstico, ~10 s) estão
bem acima desse ruído.

## Qualidade — achado principal

**Com o JSON da resposta enviado cru, os três portes erraram a causa raiz.** O cenário era um
campo renomeado (`preco` → `preco_v2`):

| Modelo | Diagnóstico com JSON cru | Correto? |
|---|---|---|
| 1.5B | Culpou `Number()` por incompatibilidade com `DECIMAL`; ainda inventou um bloco JSON de erro que não existia | Não |
| 3B | Culpou "conversão de número para string no PHP"; acertou só o nome do campo | Não |
| 7B | Culpou `Number()` por não converter decimais | Não |

Levantou-se a hipótese de que comparar chaves entre duas estruturas é trabalho de código, não
de modelo de linguagem. O teste A/B (`teste_diff_previo.py`) repetiu o mesmo cenário com a
divergência **já calculada em código** antes do envio:

| Modelo | Diagnóstico com diff pré-calculado | Correto? |
|---|---|---|
| 1.5B | Identificou `preco_v2`, mas embaralhou a causalidade | Parcial |
| 3B | "A API retornou um campo `preco_v2` que não estava previsto no contrato da interface" | **Sim** |
| 7B | Apontou o `preco` ausente e o `preco_v2` inesperado, ligando ao `formatarPreco()` | **Sim, mais completo** |

### Consequência para a arquitetura

O interceptador deve **calcular a divergência de contrato deterministicamente em código** e
enviar ao modelo o diff, nunca o JSON bruto para comparação. O modelo é ruim em comparação
estrutural e bom em explicar uma divergência já isolada. Isso também reduz o tamanho do prompt.

## Qualidade — cura de seletor

Pedido: substituir `button.btn-detalhes` para alcançar o botão do produto "Picanha ao Alho".

| Modelo | Resposta | Avaliação |
|---|---|---|
| 1.5B | `button.btn-info btn-xs saiba-mais` | **CSS inválido** (espaços = descendência); não casaria com nada |
| 3B | `button.btn-info.btn-xs.saiba-mais` e variantes | Válido, mas **ambíguo**: casa com os dois cartões |
| 7B | `button.btn-info.btn-xs.saiba-mais`, depois `button[data-id="1"]` | O 2º candidato é **correto e único** |

Isso confirma a necessidade da etapa de validação prevista no plano: só se aceita candidato que
resolva para **exatamente um** elemento na página viva. Sem ela, a resposta do 3B seria aceita e
o teste passaria a clicar no cartão errado silenciosamente.

## Decisão

**`qwen2.5-coder:3b` como padrão.** Diagnostica corretamente quando recebe o diff pré-calculado,
é o mais rápido dos três no diagnóstico (~6 s em CPU) e ocupa ~2 GB — o que importa porque o modelo divide os 16 GB da máquina
com o navegador automatizado, o MariaDB, o PHP e o uvicorn durante os experimentos.

- **1.5B descartado**: gerou CSS inválido, alucinou conteúdo e não acerta o diagnóstico.
- **7B como alternativa** quando a cura de seletor precisar de candidatos melhores: é o único que
  produziu um seletor único, mas custa 2,7× mais tempo (16 s contra 6 s) e 2,3× mais memória.

O porte pode ser trocado sem alterar código, pela variável de ambiente `COBAIA_MODELO_LLM`.

<!-- ! Alteração de IA - Revisar: nota de superação acrescentada na Fase 2-B.
     ! Motivo: a decisão acima foi tomada com 2 casos e 3 portes de uma família; a bateria
     ampliada mudou o quadro e o leitor precisa saber antes de citar este documento. -->

## Nota de superação (Fase 2-A, 03/09/2026)

A decisão de adotar `qwen2.5-coder:3b` como padrão foi tomada com **2 casos** e uma única
família de modelo. A bateria ampliada da Fase 2-A (90 casos × 3 estratégias × 6 modelos,
`resumo_metricas.json`) mediu acerto de causa raiz de **27,0%** para o 3b, contra **50,0%**
dos dois modelos de 7B e **67,8%** do `granite4.2:8b` (braço linear). O padrão de produção
será redecidido ao fim da Fase 2-B, com acerto × tempo × biblioteca; até lá, o valor em
`install.py` permanece por compatibilidade, não por evidência.
