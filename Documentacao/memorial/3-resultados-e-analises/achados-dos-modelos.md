<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Achados experimentais — modelos e experimentos (4.12 a 4.20)

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

## 4. Achados experimentais (continuação)

### 4.12 Modelos pequenos erram a causa raiz quando recebem o JSON cru
No cenário de campo renomeado (`preco` → `preco_v2`), **os três portes testados erraram**: 1.5B e 7B culparam a conversão numérica por "não lidar com decimais"; o 3B acertou apenas o nome do campo. O 1.5B ainda **inventou um bloco JSON de erro que não existia** na entrada.

Levantou-se a hipótese de que comparar chaves entre estruturas é trabalho de código, não de modelo de linguagem. Repetindo o mesmo cenário com a divergência **pré-calculada em código**, 3B e 7B passaram a acertar — o 3B respondeu literalmente *"a API retornou um campo `preco_v2` que não estava previsto no contrato da interface"*.

**Consequência arquitetural:** o interceptador calcula o diff de contrato deterministicamente e envia o diff ao modelo, nunca o JSON bruto para comparação. Isso foi posteriormente confirmado pela literatura (ver seção 6.2).

### 4.13 O modelo menor é o mais lento
Contra a intuição, o 1.5B levou 10,24 s no diagnóstico contra 5,98 s do 3B — porque gera 172 tokens onde o 3B gera 52. **O tempo é dominado pela prolixidade, não pelo tamanho do modelo.**

### 4.14 Candidatos de seletor são plausíveis mas ambíguos
Na tarefa de cura de localizador: o 1.5B devolveu **CSS sintaticamente inválido** (espaços no lugar de pontos); o 3B devolveu seletores válidos mas que casam com **dois** cartões; só o 7B produziu um seletor único, no segundo candidato. Isso valida a etapa de validação prevista: aceita-se apenas candidato que resolva para **exatamente um** elemento na página viva. Sem ela, a resposta do 3B seria aceita e o teste passaria a clicar no cartão errado silenciosamente.

### 4.15 Cython não traria ganho neste projeto
Ver [validacao-cython.md](validacao-cython.md) (seção 7 do memorial).

### 4.16 Linear × estágios: empate nos modelos pequenos, vantagem clara no melhor modelo (Fase 2-A)
**Correção de leitura.** A primeira leitura deste resultado usou o agregado por estratégia (37,4% linear × 29,7% × 31,1%), que estava **inflado**: incluía os 90 casos lineares do Granite, mas só 4 e 3 casos dos braços em estágios dele. Refeito por modelo e com teste pareado por caso (McNemar exato, ver 6.5):

| Modelo | Linear | Estágios (compilador) | Estágios (domínio) | linear × compilador | linear × domínio |
|---|---|---|---|---|---|
| `granite4.2:8b` | **67,8%** | 52,2% | 48,9% | 20/6, **p = 0,009** | 23/6, **p = 0,002** |
| `qwen2.5:7b` | 53,3% | 47,8% | 48,9% | 14/9, p = 0,41 | 13/9, p = 0,52 |
| `qwen2.5-coder:7b` | 48,9% | 52,2% | 48,9% | 10/13, p = 0,68 | 10/10, p = 1,00 |
| `qwen2.5-coder:3b` | 25,6% | 25,6% | 30,0% | 2/2, p = 1,00 | 1/5, p = 0,22 |
| `phi4-mini:3.8b` | 23,3% | 16,7% | 16,7% | 11/5, p = 0,21 | 8/2, p = 0,11 |
| `qwen2.5-coder:1.5b` | 5,6% | 6,7% | 10,0% | 0/1, p = 1,00 | 0/4, p = 0,13 |

*(b/c = casos em que só a primeira / só a segunda estratégia acertou.)*

Nos cinco modelos de 1,5B a 7B, a média por modelo é **31,3% × 29,8% × 30,9%** e, agrupando os 450 pares, **nenhuma diferença é significativa** (linear × compilador p = 0,46; linear × domínio p = 0,90). Com os seis modelos (540 pares, Granite completo): 37,4% × 33,5% × 33,9%, linear × compilador p = 0,037 — significância inteiramente puxada pelo Granite, o melhor modelo, em que linear é claramente superior porque os braços em estágios muitas vezes **não concluem** (15 e 18 respostas sem `CAUSA_RAIZ` em 90, mesmo com teto de 1.200 tokens; entre as válidas, 62,7% e 61,1%, ainda abaixo do linear) — percorrer etapas faz esse modelo esgotar o orçamento antes de responder. Leitura completa por modelo em [fase-2a-relatorio-por-modelo.md](fase-2a-relatorio-por-modelo.md). Três desdobramentos: (a) o prior da literatura (6.2) de que decompor a tarefa em fases prejudica classificação em modelos pequenos **não se confirma nem se refuta** aqui — não há efeito da estrutura nos modelos de 1,5B a 7B, e há efeito negativo no de 8B; (b) o efeito do *nome* dos estágios (compilador × domínio: 29,8% × 30,9%) tem o sinal previsto pelo PA-Tool, mas é 1 pp e não significativo, contra os +17 pp daquele trabalho; (c) o custo, sim, difere: os braços em estágios geram mais texto de saída em todos os modelos (ver `tokens_saida_medio` em `resumo_metricas.json`).

**Consequência:** a Fase 2-B fixa o prompt em linear (decisão 19) — não porque "vence", mas porque não é pior em nenhum modelo, é a mais barata em tokens e é significativamente melhor no melhor modelo.

### 4.17 Dois modos de falha distintos nos modelos pequenos
A análise por rótulo revelou que "acerto baixo" esconde dois comportamentos diferentes. O `qwen2.5-coder:1.5b` usa apenas **8 dos 23 rótulos** e responde `corpo_nao_e_json` em **84% dos casos** — não está fazendo a tarefa, está repetindo um rótulo. O `phi4-mini:3.8b` responde **fora do conjunto fechado em 17,8%** das vezes (rótulos inventados), uma falha de seguir instrução, não de diagnóstico. Os dois têm acurácia parecida (7,4% e 18,9%) por razões opostas. Por isso o `1.5b` fica fora das ablações da Fase 2-B (decisão 24) e a métrica `fora_do_conjunto` passa a ser reportada sempre.

### 4.18 O tokenizador real gasta mais tokens do que a estimativa
Medido nos 90 prompts lineares da Fase 2-A (caracteres ÷ `prompt_eval_count`): **Granite 2,62**, **Qwen2.5 2,83** e **phi4-mini 3,19 caracteres por token**, contra 3,3 que havia sido estimado (e 664 tokens de mediana no tokenizador do GPT-2, medido na validação do GPT-2). Consequência direta: a biblioteca de 36 verbetes, escrita com ~550 caracteres por verbete, ficava em ~7,6 mil tokens no pior tokenizador e o prompt do braço "biblioteca inteira" ultrapassaria o `num_ctx` de 8.192 — e o Ollama, nesse caso, **descarta o começo do prompt em silêncio**, justamente a biblioteca. Três providências: os verbetes foram reescritos para ~470 caracteres (≈6,5 mil tokens no total); o teto de resposta nos braços com biblioteca caiu de 900 para 600 tokens (a maior resposta linear da Fase 2-A ficou abaixo disso, e o avaliador acusa qualquer resposta cortada sem `CAUSA_RAIZ`); e a bateria ganhou duas guardas — uma estimativa antes de inferir e a contagem real do tokenizador na primeira inferência, abortando se o prompt encostar no contexto.

### 4.19 A recuperação precisa de sinais calculados em código
Com BM25 apenas sobre o texto do sintoma, o verbete certo ficou entre os 3 recuperados em **58,9%** dos 90 casos (hit@5 72,2%, MRR 0,470), e num caso de resposta truncada ficou em **35º de 36**: o texto humano ("a listagem fica vazia e o console acusa erro") não carrega o sinal estrutural que separa as classes léxica e sintática. Acrescentando à consulta termos calculados em código — o corpo parseia? está cortado? é HTML? que chaves faltam, sobram ou mudaram de tipo contra o contrato, item a item? e, quando *nada* diverge no fio, esse próprio "nada" como sinal — o hit@3 subiu a **78,9%**, o hit@5 a **90,0%** e o MRR a **0,584**. É a mesma conclusão de 4.12 aplicada ao recuperador: comparar estrutura é trabalho de código. Os sinais entram **só na consulta de recuperação**; o prompt do modelo continua idêntico ao da Fase 2-A, para a linha de base seguir comparável. Os casos que restam mal posicionados são os de lógica entre requisições (duplicação na tela, escala dobrada), que nenhum sinal sintático alcança — e que são, por construção, os de nível 3.

### 4.20 Documentar o sistema expôs divergências entre os casos e o código
Escrever verbetes fiéis ao código revelou que alguns *fixtures* do banco descrevem sintomas que o código real não produz: `produtos_api.php` imprime o preço cru ou `undefined` quando o campo não converte — nunca "R$ NaN", que aparece em três casos —, e substitui o grid por `innerHTML` a cada carga, o que torna impossível a duplicação de cartões do caso `efe-13`. A biblioteca segue o código (é a fonte da verdade); os casos foram **mantidos como estão** para não quebrar a comparabilidade com a Fase 2-A, e a correção fica registrada como pendência para depois da 2-B. É também um resultado: em três casos a documentação vai *contradizer* a evidência apresentada, e o comportamento do modelo nesses casos é informativo sobre adesão à documentação.

### 4.21 O cache de prefixo do Ollama funciona em CPU — e `prompt_eval_count` não é o sinal
Verificação 0 da Fase 2-B, medida com `verificar_cache_prefixo.py` no `qwen2.5-coder:3b` (Ollama 0.33.2, só CPU), biblioteca inteira como prefixo:

| Chamada | Tokens reportados | Prefill |
|---|---|---|
| A — prefixo + caso 1 (primeira vez) | 5.723 | **80.653 ms** |
| B — o mesmo prompt repetido | 5.723 | **105 ms** |
| C — prefixo + caso 2 (só o fim muda) | 5.712 | **6.160 ms** |
| D — caso 1 sem prefixo | 493 | 4.557 ms |
| E — prefixo + caso 1, depois de D | 5.723 | 5.762 ms |

Três conclusões. (1) **O cache funciona**: a repetição exata custa 0,1% do prefill original, e um prompt que só muda no fim custa só o prefill do fim (~600 tokens em 6 s) — a biblioteca é paga uma vez por modelo e o braço "biblioteca inteira" é viável sem encolher. (2) O **`prompt_eval_count` não serve de diagnóstico**: o Ollama reporta o tamanho do prompt (5.723) mesmo quando reaproveitou 99,9% dele; o script foi corrigido para decidir pelo `prompt_eval_duration`. Sem essa medição, o veredito impresso teria sido "não funciona" e a biblioteca teria sido cortada à toa. (3) A contagem real do tokenizador do Qwen dá **5.230 tokens** para a biblioteca (a estimativa por caracteres, calibrada pelo pior tokenizador, dizia 6.582) e **~108 tokens/s** de prefill sem cache neste modelo e CPU — o prompt de A1 fica em 5.723 tokens, com 1.869 de folga para a resposta de 600.


