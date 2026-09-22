<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
<!-- ! Alteração de IA - Revisar: em 11/09/2026 o achado 4.20 ganhou o parágrafo de
     fechamento (os 4 fixtures corrigidos, o efeito na recuperação e o achado colateral da
     biblioteca original) e foi acrescentado o 4.29, com o pré-registro da Fase 3.
     ! Motivo: 4.20 estava aberto desde a 2-B ("a correção fica registrada como pendência
     para depois da 2-B") e a correção foi feita antes de rodar a Fase 3 — sem o fechamento,
     quem lê não sabe o que mudou nos casos nem o que isso fez com o recuperador. O 4.29
     precisa existir ANTES da bateria: hipótese escrita depois de ver o resultado não é
     hipótese, e a Fase 3 é a que decide o modelo final do TCC. -->
<!-- ! Alteração de IA - Revisar: em 12/09/2026 as duas citações de relatórios de tarefa no
     fechamento do 4.20 (`task-1-report.md`, `task-4-report.md`) passaram a dizer onde esses
     arquivos ficam e que estão fora do git, e o 4.21 passou a nomear as versões do Ollama
     posteriores à Verificação 0. As hipóteses H1–H6 do 4.29 não mudaram.
     ! Motivo: `.superpowers/` está na linha 19 do `.gitignore`; quem clonar o repositório não
     acha esses relatórios e precisa saber que o reproduzível é o comando ao lado. E o 4.21
     dizia só "Ollama 0.33.2": a 2-B rodou em 0.33.3 e a Fase 3 roda em 0.34.0 (atualização
     automática em 12/09/2026), diferença que o relatório da Fase 3 declara em §11. -->
<!-- ! Alteração de IA - Revisar: segunda passada de 12/09/2026 — o 4.21 passou a dizer em que
     máquina e em que dia a Verificação 0 da tabela foi medida (Ryzen, 03/09/2026) e que na
     máquina-alvo a 2-B inteira, inclusive a Verificação 0 repetida nela, rodou em 0.33.3.
     ! Motivo: o relatório da Fase 3 (§1 e §11), a comparação entre fases (§1) e a §6.5 passaram
     a remeter ao 4.21 como "a Verificação 0 medida no Ryzen em 0.33.2", e o 4.21 não dizia a
     máquina. A tabela e o "0.33.2" entraram no commit 603c423 (03/09/2026), antes da decisão 25
     (07/09) que fez do i5 a máquina-alvo — o `verificar_cache_prefixo.py` desse commit registra
     "medido nesta máquina (Ollama 0.33.2, CPU): a repetição exata levou 105 ms", a linha B da
     tabela; na máquina-alvo o `fase2b.log` mostra a mesma verificação em 07/09/2026 09:29, com
     o `maquina.json` em 0.33.3. -->
<!-- ! Alteração de IA - Revisar: em 22/09/2026 o 4.29 recebeu os vereditos de H1–H6 (texto das hipóteses intacto) e
     entraram os achados 4.30 a 4.35, com os números da bateria de 13–15/09/2026 (campos de resumo_fase3.json,
     comparacao_fases.md e decisao_modelo.md citados no relatório da Fase 3, de onde os números são copiados).
     ! Motivo: o pré-registro prometia os vereditos "aqui, depois da bateria"; e os seis fatos novos da fase (Granite
     barrado pelo formato, reprodutibilidade entre versões do runtime, saturação, efeito mínimo como limite, pico em L1,
     edições redundantes ou erradas) precisam de número próprio para o documento final citar. -->
# Achados experimentais — modelos e experimentos (4.12 a 4.35)

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

**Fechamento (11/09/2026).** Os quatro casos foram corrigidos para o que `produtos_api.php` faz de verdade: em `sin-1` e `sin-2` o botão de preço passa a mostrar a palavra `undefined`, sem "R$" (`formatarPreco` devolve `String(preco)` quando `Number(preco)` não converte); em `semt-13` o preço aparece cru — `89,90`, sem "R$" e sem formatação —, porque o separador decimal veio como vírgula; e `efe-13` deixou de falar em cartões duplicados: como o grid é substituído inteiro a cada resposta, o sintoma real é a tela mostrar o preço antigo, porque a primeira resposta chegou depois da segunda. `id`, classe, nível, causa e campo dos quatro casos não mudaram — só o texto do sintoma, da observação, do corpo e da requisição. Efeito na recuperação offline, medido antes de qualquer inferência (números do relatório da tarefa de correção, `task-1-report.md` — relatório interno em `.superpowers/`, fora do git, `.gitignore` l. 19 —, reproduzíveis pela saída de `validar_banco.py --indice` e de `recuperacao.avaliar_recuperacao` sobre os 90 casos):

| Recuperação nos 90 casos (BM25 + sinais em código) | Antes | Depois |
|---|---|---|
| hit@1 | 37,8 | **38,9** |
| hit@3 | 78,9 | **80,0** |
| hit@5 | 90,0 | **91,1** |
| MRR | 0,584 | **0,596** |

Posição do verbete de ouro nos quatro casos, na mesma medição: `sin-1` 4 → **2**, `sin-2` 3 → **4**, `semt-13` 2 → **2**, `efe-13` 24 → **1**. O ganho agregado é quase todo de `efe-13`: com o sintoma antigo, nada divergia no fio de JSON e o recuperador não tinha sinal estrutural para acrescentar à consulta; com o novo, o caso cai no caminho de "nada divergiu, então a falha é de tela ou de lógica" e casa com o verbete `estado_da_tela_divergente`. `sin-2` perdeu uma posição (3 → 4, ainda dentro do hit@5): o texto do sintoma alimenta a consulta do BM25 e ficou um pouco menos parecido com o verbete `campo_renomeado`.

**O que isso faz com a comparação entre fases.** Os quatro casos caíram na partição de **aprendizado** da Fase 3 (sorteio por hash, decisão 31; conferido no relatório da tarefa da partição, `task-4-report.md` — relatório interno em `.superpowers/`, fora do git, `.gitignore` l. 19 —, e reproduzível por `resultados_alvo/fase3/particao.json` e por `evolucao_biblioteca.particionar`), de modo que os **36 casos de avaliação da Fase 3 são os mesmos 36 que a 2-B rodou, texto por texto** — o pareamento 2-B A2 × Fase 3 L0 nesses 36 não tem ressalva de fixture. Nos 90, o pareamento com as fases anteriores exclui os quatro: sobram 86 casos comparáveis. Daqui em diante, toda tabela que compare fases diz em qual dos dois conjuntos está.

**Achado colateral: a imprecisão também está na biblioteca.** O verbete `negocio/pagina-produtos-api.md` da biblioteca original lista `R$ NaN` entre os `sintomas` do frontmatter — a mesma descrição que o código não produz, agora dentro da documentação que o modelo consulta, e não nos casos de teste. Foi **mantida de propósito**: a biblioteca original é a versão L0 que os quatro modelos recebem na Fase 3 e é a mesma com que a 2-B rodou; corrigi-la agora tiraria o ponto de partida comum e a comparabilidade com a 2-B. Além disso, o campo `sintomas` do frontmatter não entra na checagem de sobreposição de 5-gramas do validador, que só olha o corpo do verbete — é uma imprecisão que nenhuma validação em código pega. Ela é alvo natural de uma `retificacao` na Fase 3, e fica registrada aqui para ser observada: se algum modelo apontar esse trecho, é o caso em que o modelo corrige a documentação contra o código, e não o contrário.

### 4.21 O cache de prefixo do Ollama funciona em CPU — e `prompt_eval_count` não é o sinal
Verificação 0 da Fase 2-B, medida com `verificar_cache_prefixo.py` no `qwen2.5-coder:3b`, no Ryzen de desenvolvimento em 03/09/2026 (Ollama 0.33.2, só CPU — na máquina-alvo a 2-B inteira rodou em 0.33.3, inclusive a Verificação 0 repetida nela em 07/09/2026 e registrada no `fase2b.log`, e a Fase 3 roda em 0.34.0; ver o relatório da Fase 3, §11), biblioteca inteira como prefixo:

| Chamada | Tokens reportados | Prefill |
|---|---|---|
| A — prefixo + caso 1 (primeira vez) | 5.723 | **80.653 ms** |
| B — o mesmo prompt repetido | 5.723 | **105 ms** |
| C — prefixo + caso 2 (só o fim muda) | 5.712 | **6.160 ms** |
| D — caso 1 sem prefixo | 493 | 4.557 ms |
| E — prefixo + caso 1, depois de D | 5.723 | 5.762 ms |

Três conclusões. (1) **O cache funciona**: a repetição exata custa 0,1% do prefill original, e um prompt que só muda no fim custa só o prefill do fim (~600 tokens em 6 s) — a biblioteca é paga uma vez por modelo e o braço "biblioteca inteira" é viável sem encolher. (2) O **`prompt_eval_count` não serve de diagnóstico**: o Ollama reporta o tamanho do prompt (5.723) mesmo quando reaproveitou 99,9% dele; o script foi corrigido para decidir pelo `prompt_eval_duration`. Sem essa medição, o veredito impresso teria sido "não funciona" e a biblioteca teria sido cortada à toa. (3) A contagem real do tokenizador do Qwen dá **5.230 tokens** para a biblioteca (a estimativa por caracteres, calibrada pelo pior tokenizador, dizia 6.582) e **~108 tokens/s** de prefill sem cache neste modelo e CPU — o prompt de A1 fica em 5.723 tokens, com 1.869 de folga para a resposta de 600.

### 4.22 A biblioteca recuperada sobe o acerto em todos os modelos; a inteira, não (Fase 2-B)
Na máquina-alvo (i5-1235U), 2.610 inferências: com 3 verbetes recuperados (A2), **três modelos cruzam 70%** — Granite 76,7%, `qwen2.5-coder:7b` 72,2%, `qwen2.5:7b` 70,0% — e o `qwen2.5-coder:3b` salta **de 23,3% para 63,3%** (+40 pp, 36 casos ganhos e nenhum perdido, p < 0,001). Com a biblioteca inteira no prompt (A1, ~5,8 mil tokens), o Granite **piora** 5,6 pp mesmo com o verbete certo presente em 100% dos casos — a sintática cai de 93% para 53%. É o *Context Rot* (6.3) medido no próprio experimento: presença não basta, quantidade e posição importam. Relatório completo em [fase-2b-relatorio-por-modelo.md](fase-2b-relatorio-por-modelo.md).

### 4.23 O teto é a recuperação
Com só o verbete certo (A3), o Granite acerta **100% dos 90 casos** e o 3B, 92,2%. Em A2 o verbete certo está entre os três em 78,9% dos casos (o hit@3 medido offline em 4.19, idêntico porque a recuperação é determinística); quando está, o Granite acerta 91,5%; quando não está, 21,1%. A diferença entre 76,7% e 100% é quase toda do recuperador. A classe de tradução é onde ele mais falha (verbete certo no top-3 em 46,7%) — e é a única classe que quase não ganha com a biblioteca (+4,5 pp), embora em A3 o Granite acerte 100% dela.

### 4.24 Adesão cega: documentação errada é veneno, não ruído
Três verbetes plausíveis mas errados (A4) derrubam o Granite de 66,7% para **22,2%** — abaixo de sem documentação — e ele responde a causa de um distrator em 73% dos casos. Um verbete errado com um "registro de incidente" falso (A5) leva Granite e 3B a repetir a causa plantada em **93–96%** das respostas. Quanto melhor o modelo lê documentação, mais a obedece: o `phi4-mini`, que não a lê (cita verbete em 0–12% das respostas), é o menos afetado (30%). Consequência direta para a Fase 3: a gestão da biblioteca pelo modelo só pode existir atrás de validação por código.

### 4.25 O 3B com documentação alcança o 8B sem documentação, a um quarto do custo
`qwen2.5-coder:3b` + A2: 63,3% em 29,7 s por caso e 2,3 GB. `granite4.2:8b` sem biblioteca: 66,7% em 83 s e 6,6 GB, na mesma máquina. Para a máquina corporativa, saber do sistema substitui porte de modelo — a lição que junta as duas fases: raciocinar em etapas não ajudou (4.16); conhecer o sistema ajudou.

### 4.26 A acurácia reproduz entre máquinas; o tempo não
A0 refeito no i5 contra o do Ryzen, pareado caso a caso: nenhuma diferença significativa de acerto; respostas idênticas em 91–98% dos casos, exceto `qwen2.5-coder:7b` (68,9%, o mais prolixo). Tempo 1,6–2,3× maior no i5. A decisão 25 (refazer A0 na máquina-alvo) custou 540 inferências e comprou o pareamento correto e a evidência de que os resultados da 2-A não eram artefato da máquina.

### 4.27 Quantização não explica o piso do 1,5B
`qwen2.5-coder:1.5b` em q8_0 e fp16: 8,9% contra 5,6% do Q4_K_M, 4 respostas diferentes em 90, nenhum caso perdido, e o dobro do tempo. O piso é capacidade do modelo. Q4_K_M confirmado para todos os portes.

### 4.28 A biblioteca inteira custa mais no que gera, não no que lê
Com o cache de prefixo, o prefill de A1 ficou em 1,5–1,8× o de A0 (não 10×); mas A1 faz os modelos escreverem mais (Granite: geração de 47 s para 114 s; `coder:7b` cortou 6 respostas no teto). A2 tem prefill maior que A1 (o prefixo muda a cada caso e não é reaproveitado) e ainda assim é mais barata no total. Documentação demais não só distrai — alonga a resposta.



### 4.29 Pré-registro da Fase 3
Escrito em 11/09/2026, **antes** de a bateria rodar. A Fase 3 ("teste 3", decisão 29) dá a cada modelo uma cópia da biblioteca e deixa que ele a edite, por acréscimo e atrás de validação em código, ao longo de três épocas; a pergunta é se o modelo melhora a documentação que consulta sem estragá-la. O desenho está em `claude-memoria/plano-aprovado-fase-3.md`. Os vereditos de cada hipótese entram **aqui**, depois da bateria, com os números que o avaliador produzir.

**Hipóteses, como foram registradas no plano (§4.4):**

- **H1** — Nos 36 de avaliação, acerto com L3 > L0 nos modelos de 7–8B (McNemar exato, α = 0,05).
- **H2** — O ganho concentra-se nas classes em que a recuperação é fraca (tradução: hit@3 = 46,7%), via aumento do hit@3 da biblioteca do modelo.
- **H3** — Nos 54 de aprendizado o ganho é maior que nos 36; a diferença quantifica a memorização.
- **H4** — A taxa de aceitação das propostas cresce com o porte; o 3B tem mais rejeições por formato.
- **H5** — Autoenvenenamento (casos certos em L(n) que viram errados em L(n+1), nos 36) fica abaixo de 10%; se superar o ganho, o modelo é vetado.
- **H6** — A curva não é monótona: reportar o melhor L e o L3, nunca só o último.

**Partição (decisão 31).** Em cada uma das 18 células classe×nível, os 5 casos são ordenados pelo hash `sha256("fase3:" + id)`; os 3 primeiros vão para **aprendizado** (54 no total) e os 2 últimos para **avaliação** (36). Só nos 54 o modelo vê a causa correta e propõe edição; os 36 nunca recebem feedback nem geram proposta. A partição é gravada em `fase3/particao.json` e reconferida a cada execução — divergência aborta a bateria.

**Protocolo, por modelo:**

1. **Época 0**, sem inferência: `L0` é a cópia intocada da biblioteca original, a mesma para os quatro modelos (o hash é conferido entre eles).
2. **Épocas 1 a 3**: os 90 casos na mesma ordem; o diagnóstico lê a biblioteca da época anterior, já fechada, na condição **A2** (3 verbetes recuperados), com o prompt de diagnóstico byte a byte igual ao da 2-B e teto de 600 tokens de resposta.
3. Nos 54 de aprendizado, logo depois do diagnóstico vem a **proposta de edição**, com a causa correta e o verbete dedicado à vista; o que a validação em código aceitar (decisão 33) é aplicado na pasta da época seguinte, de modo que os 90 casos de uma mesma época vejam sempre a mesma biblioteca.
4. **Fechamento da época**: a biblioteca inteira é validada, a conferência de somente-acréscimo tem de vir vazia, o índice é regerado e os diffs contra a época anterior e contra a original são gravados ao lado da pasta da época.
5. **Passada final**: os 90 casos diagnosticados com `L3`, sem proposta. São **4 × 90 diagnósticos + 3 × 54 propostas = 522 inferências por modelo**, e a passada com `L0` é a própria linha de base.

**O que já se sabe que vai limitar a leitura.** Os 54 de aprendizado são exatamente os casos cujas lacunas o modelo teve chance de documentar, então o ganho ali mistura aprender e decorar — é para isso que servem os 36. E a biblioteca de cada modelo passa a ser diferente, então o hit@k vira uma variável do experimento, não mais a constante de 78,9% comum aos seis modelos que a 2-B tinha (4.23).

**Vereditos (22/09/2026, bateria de 13–15/09/2026; números e campos em [fase-3-relatorio-por-modelo.md](fase-3-relatorio-por-modelo.md), §2–§6):**

- **H1 — Não confirmada.** Nos 36, L3 vs L0: `qwen2.5:7b` +8,3 pp (b/c 3/0, p = 0,25), `qwen2.5-coder:7b` +2,8 pp (3/2, p = 1,0), `granite4.2:8b` 0,0 pp (0/0). Nenhum p < 0,05 com efeito mínimo detectável de 19,4 pp — falta resolução, não sinal (4.33).
- **H2 — Não.** O hit@3 da biblioteca do modelo não subiu (80,0 → 77,8–78,9 nos 90 no `qwen2.5:7b`) e a tradução seguiu com o verbete de ouro no contexto em 46,7% dos casos; os 4 casos ganhos em L1 vieram de quatro classes diferentes.
- **H3 — Não; no vencedor, invertida.** `qwen2.5:7b` ganhou +11,1 pp nos 36 e +1,8 nos 54 em L1; `tentativas_de_decorar` = 0 em todas as épocas.
- **H4 — Parcial.** O 3B tem mais rejeições por formato (`bloco_malformado` em 91 de 151), mas a aceitação não cresce com o porte: 6,2%, 24,1%, 23,1% e **0%** no maior (4.30).
- **H5 — Sim.** Autoenvenenamento máximo 5,6% nos 36 (`qwen2.5:7b`, L1→L2), sob o teto de 10%; nenhum veto.
- **H6 — Sim.** `qwen2.5:7b` 81,2 → 91,7 (L1) → 84,2 → 86,2 de acurácia balanceada nos 36; o melhor L é L1 em três modelos nos 90 (4.34).

### 4.30 O Granite não documentou porque o formato não coube, não porque não soube
`granite4.2:8b` fez 181 propostas em três épocas e **nenhuma entrou**: 133 rejeitadas por `texto_longo` (o campo TEXTO passou de 280 caracteres), 26 por `bloco_malformado`, 25 respostas cortadas no teto de 700 tokens — com 508 a 528 tokens de saída por proposta contra 188 a 203 dos Coder e 322 a 368 do `qwen2.5:7b`. A biblioteca ficou idêntica nas quatro versões (hash `3196327e7fd5`) e a curva, plana (83,3% nos 36 em L0..L3). A literatura pedia esta leitura antes de vetar (mapa §6.10, linha 11: OUYANG et al., 2026 — a política de curadoria importa mais que o porte do curador): é incompatibilidade entre a política de edição (280 caracteres por nota) e o que o modelo escreve, não incapacidade de diagnosticar — no diagnóstico ele é o segundo da regra 36. O reteste com `TEXTO_MAX` = 600 (menu da 3-B, item d) é o que responderia; ficou inviável em 21/09 por RAM (8 GB exigidos, 7,8 GB livres) e o Granite saiu da 3-B (decisão 52). Consequência para a Fase 4: se o Granite voltar como escritor, o teto de texto é variável de desenho, não constante.

### 4.31 O resultado reproduz entre execuções e entre versões do runtime
Pareamento 2-B A2 × Fase 3 L0 (mesma máquina, mesmo prompt, mesma biblioteca; 0.33.3 → 0.34.0): **b = c = 0 em 6 dos 8 pareamentos** (nos 36 e nos 86 não alterados, para Granite, 3B e `qwen2.5:7b`); o `qwen2.5-coder:7b` tem 1/0 nos 36 e 2/3 nos 86 (p = 1,0) — o mesmo modelo que 4.26 apontou como o menos idêntico entre máquinas e o único com `formato_valido_pct` abaixo de 100 na Fase 3. A ponte de versão da 3-B (0.34.0 → 0.34.1, L0 nos 36, 21/09/2026) repetiu a medida: 0/0 no 3B, 0/0 no Coder 7B, 1/1 no `qwen2.5:7b` (`sin-14` e `tra-10`, casos que também oscilam entre versões da biblioteca), medianas de tempo dentro de 1,5 s das da bateria. Com temperatura 0,1 e sem semente fixa, o ruído entre execuções é de 0 a 2 casos em 36 — abaixo dos 4 casos do ganho do vencedor em L1 e muito abaixo do que o McNemar resolve. HE et al. (2025) mediram 80 completações distintas em 1.000 execuções a temperatura 0 (mapa, linha 21); aqui, com prompts de 1,1–1,4 mil tokens e resposta curta, a variação fica quase toda num modelo.

### 4.32 A biblioteca satura em três épocas sob a regra de só acréscimo
As edições aceitas caem de 40 para 12 e 9 no `qwen2.5:7b` e de 25 para 7 e 7 no `qwen2.5-coder:7b`; nas épocas 2 e 3 os motivos de rejeição dominantes são `duplicada` (89 no total, 53 no `qwen2.5:7b`) e `teto_notas_verbete` (35; 33 no `qwen2.5:7b`), não erros de formato. Com 36 verbetes originais, 6 notas por verbete e 6 verbetes novos por época, o que cabe acrescentar esgota rápido — e o modelo passa a propor de novo o que já está lá. É o comportamento previsto para um corpus pequeno sob portão determinístico (ZHANG, G. et al., 2026; mapa, linha 12) e diz que três épocas foram suficientes: mais épocas custariam máquina para rejeitar duplicatas. A saturação também explica a curva: o grosso da mudança acontece na E1 (8.639 dos 13.069 tokens acrescentados pelo `qwen2.5:7b`), e é L1 o pico (4.34).

### 4.33 Nenhum ganho alcança o efeito mínimo detectável — e isso é um resultado, não uma falha
Com 36 casos e 20% de pares discordantes supostos, o McNemar exato só aponta diferenças de **19,4 pp** (16,7 nos 54; 11,1 nos 90; `efeito_minimo_detectavel`). A maior diferença medida na fase foi +11,1 pp (`qwen2.5:7b`, L1 nos 36, b/c 4/0, p = 0,125); o menor p das 36 comparações pareadas foi 0,1094 e nenhum Q de Cochran chegou a 0,05. A literatura pedia que isso fosse dito nestas palavras (KOTAWALA, 2026; CARD et al., 2020; mapa, linhas 5–7): a amostra não resolve o efeito, e pescar um p entre 36 comparações seria o erro. Por isso a decisão do modelo não se apoia em teste de hipótese, e sim na convergência de critérios declarados antes (regra 36, P(top-1) por bootstrap, Pareto, sensibilidade — decisão 46) e na direção consistente dos flips (9 ganhos e 0 perdas do `qwen2.5:7b` entre L0 e qualquer L nos 36). O que fecharia a lacuna é n: 72 casos nunca vistos baixariam o efeito mínimo para cerca de 14 pp — é o item (a) do menu da 3-B.

### 4.34 O pico é L1, não L3
`qwen2.5:7b`: 91,7% de acurácia balanceada nos 36 em L1, 84,2 em L2, 86,2 em L3 (83,0 → 78,1 → 80,7 nos 90); `qwen2.5-coder:7b` nos 90: 78,9 (L1) → 77,8 → 75,4, abaixo de L0. A época 1 concentra as edições (4.32) e o que vem depois acrescenta notas repetitivas e retira dois casos (`sin-14`, `run-10`) que L1 tinha ganho. É a curva de subida e regressão que LIN (2026) descreve para automelhoria (mapa, linha 8) — em escala menor que os ~17 pontos de lá, mas com o mesmo formato. Consequência prática já aplicada: a regra 36 escolhe o melhor L e não o último, e a biblioteca de produção é L1, não L3; reportar só a última época teria escondido o resultado principal da fase.

### 4.35 As edições aceitas são, na maioria, redundantes ou erradas — e o ganho veio mesmo assim
Revisão das 63 edições amostradas (primeira passada por IA em 22/09/2026, conferida contra o código do cobaia; relatório §7): 23 corretas, 17 parciais, 23 erradas — e 21 das 23 corretas repetem o que o verbete original já dizia. No vencedor, 12 de 29 (41,4%) afirmam o que o código não faz ("a API lê dados antigos do banco"; "aplicar o fator correto na conversão de `valor_produto`"; "corrigir a lógica do LEFT JOIN"), e nas 10 edições da E1 — a biblioteca L1 escolhida — 3 são erradas. O validador em código garante forma, tetos e não-cópia, não verdade; e o ganho de L1 (+11,1 pp) aconteceu com essas notas dentro. Duas leituras, ambas previstas: agentes não usam necessariamente a experiência que escreveram e perturbar a memória quase não muda o resultado (ZHAO, W. et al., 2026; mapa, linha 17) — o que o modelo lê no prompt são o verbete de ouro e as notas coladas a ele, e a mudança no frontmatter (`sintomas`, `palavras_chave`) altera a consulta do recuperador; e documentação errada é obedecida (4.24; WU; WU; ZOU, 2024), o que torna o autoenvenenamento baixo (5,6%) um alívio e não uma prova. Consequências: (1) a biblioteca de produção precisa de curadoria humana da cópia L1 antes da Fase 4; (2) a troca cruzada da 3-B (L1 do `qwen2.5:7b` lida por outros modelos) e os casos inéditos são os testes que separam efeito do conteúdo de efeito da forma; (3) qualquer trabalho futuro de memória gerida pelo modelo precisa de um juiz de verdade — código, teste executável ou humano — e não só de um validador de forma.
