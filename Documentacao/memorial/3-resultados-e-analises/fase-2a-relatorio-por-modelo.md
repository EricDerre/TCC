<!-- ! Alteração de IA - Revisar: relatório da Fase 2-A, por modelo, escrito ao fim da bateria
     do Granite (03/09/2026), a partir de resumo_metricas.json, avaliacao.json e dos JSONL
     brutos em Programacao/AgenteCore/experimentos/resultados/.
     ! Motivo: o Memorial registra decisões e achados; faltava um documento que lesse os dados
     de cada modelo com o mesmo rigor — o que acerta, o que erra, a que custo — para a seção
     de resultados do TCC. Nenhum número aqui foi digitado à mão: todos saem dos scripts
     citados e podem ser regenerados com `python avaliar.py`. -->
# Fase 2-A — relatório por modelo

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Gráficos em `Programacao/AgenteCore/experimentos/graficos/01…06`; respostas cruas navegáveis em `experimentos/relatorio.html`.

## 1. O que foi medido

| Item | Valor |
|---|---|
| Casos | 90 fixtures do cobaia real: 6 classes (léxica, sintática, semântica, tradução, runtime, efeito) × 3 níveis × 5 casos; 23 causas raiz, todas presentes |
| Estratégias de prompt | linear; estágios com nomes de compilador; estágios com nomes de domínio (uma chamada por caso, nunca cadeia) |
| Modelos | 6, todos **Q4_K_M** (`ollama show`), digest gravado por registro |
| Inferências | **1.620** (6 × 90 × 3); 0 erros de infraestrutura |
| Execução | Ollama 0.33.2, **só CPU** (`num_gpu=0`, conferido em `/api/ps` a cada caso), `num_ctx=8192`, `temperature=0.1`, um modelo residente por vez (máximo observado: 1) |
| Teto de resposta | 400 tokens na primeira leva (registros sem o campo `teto_tokens`), 900 depois; 1.200 nos braços em estágios do Granite (refeitos após a primeira leva ter truncado 100% deles) |
| Máquina | Ryzen 7 5800H (8c/16t), 15,4 GB RAM, Windows 11; GTX 1650 presente e **não usada** |
| Métrica principal | acerto da **causa raiz** (rótulo do conjunto fechado); IC 95% de Wilson; comparações pareadas por caso com McNemar exato |

## 2. Quadro geral (braço linear)

| Modelo | Digest | RAM residente | **Causa** | IC 95% | Campo | Formato ok, causa errada | Fora do conjunto | Termo proibido | Seg/caso (mediana) | Tokens de saída (média) |
|---|---|---|---|---|---|---|---|---|---|---|
| `granite4.2:8b` | `f586c02fdecd` | 6,6 GB | **67,8%** | 57,6–76,5 | 87,8% | 32,2% | 0,0% | 16,7% | 45,7 | 192 |
| `qwen2.5:7b` | `845dbda0ea48` | 5,2 GB | **53,3%** | 43,1–63,3 | 81,1% | 46,7% | 1,1% | 7,8% | 17,1 | 52 |
| `qwen2.5-coder:7b` | `dae161e27b0e` | 5,2 GB | **48,9%** | 38,8–59,0 | 76,7% | 48,9% | 0,0% | 12,2% | 25,9 | 106 |
| `qwen2.5-coder:3b` | `f72c60cabf62` | 2,3 GB | **25,6%** | 17,7–35,4 | 73,3% | 74,4% | 0,0% | 4,4% | 8,4 | 50 |
| `phi4-mini:3.8b` | `78fad5d182a7` | 3,5 GB | **23,3%** | 15,8–33,1 | 33,3% | 76,7% | **25,6%** | 6,7% | 9,8 | 41 |
| `qwen2.5-coder:1.5b` | `d7372fd82851` | 1,3 GB | **5,6%** | 2,4–12,4 | 8,9% | 94,4% | 0,0% | 8,9% | 5,2 | 90 |

*Campo* = nomeou o campo afetado. *Formato ok, causa errada* = respondeu no formato pedido com o rótulo errado (o erro que passa despercebido numa validação só de parse). *Fora do conjunto* = rótulo que não existe. *Termo proibido* = a explicação contém um termo que denuncia diagnóstico numa direção errada conhecida.

**Leitura.** Só um modelo chega perto da meta de 70–80%: o Granite, a 2,7× o tempo do `qwen2.5:7b`. Os dois de 7B da mesma família ficam a 4,4 pp um do outro, dentro do intervalo de confiança. Abaixo de 5B o acerto de causa cai para um quarto ou menos — mas por motivos diferentes em cada modelo (seção 5). Nenhum modelo tem intervalo de confiança mais estreito que ±10 pp: com 90 casos, diferenças menores que isso entre modelos não devem ser lidas como reais.

## 3. Estratégias de prompt

| Modelo | Linear | Estágios (compilador) | Estágios (domínio) | linear × compilador | linear × domínio | compilador × domínio |
|---|---|---|---|---|---|---|
| `granite4.2:8b` | 67,8% | 52,2% | 48,9% | 20/6, **p = 0,009** | 23/6, **p = 0,002** | 13/10, p = 0,68 |
| `qwen2.5:7b` | 53,3% | 47,8% | 48,9% | 14/9, p = 0,41 | 13/9, p = 0,52 | 4/5, p = 1,00 |
| `qwen2.5-coder:7b` | 48,9% | 52,2% | 48,9% | 10/13, p = 0,68 | 10/10, p = 1,00 | 7/4, p = 0,55 |
| `qwen2.5-coder:3b` | 25,6% | 25,6% | 30,0% | 2/2, p = 1,00 | 1/5, p = 0,22 | 1/5, p = 0,22 |
| `phi4-mini:3.8b` | 23,3% | 16,7% | 16,7% | 11/5, p = 0,21 | 8/2, p = 0,11 | 7/7, p = 1,00 |
| `qwen2.5-coder:1.5b` | 5,6% | 6,7% | 10,0% | 0/1, p = 1,00 | 0/4, p = 0,13 | 0/3, p = 0,25 |
| **6 modelos, 540 pares** | **37,4%** | **33,5%** | **33,9%** | 57/36, **p = 0,037** | 55/36, p = 0,059 | 32/34, p = 0,90 |

*b/c = casos em que só a primeira / só a segunda estratégia acertou; p do McNemar exato.*

- **Estrutura em estágios não ajuda ninguém e prejudica o melhor modelo.** Nos cinco modelos de 1,5B a 7B as três estratégias empatam (nenhum p < 0,10). No Granite, linear é significativamente melhor: os braços em estágios produziram **15 e 18 respostas sem `CAUSA_RAIZ`** em 90, mesmo com teto de 1.200 tokens — o modelo esgota o orçamento percorrendo as etapas. Descontando essas respostas inválidas, o acerto entre as válidas fica em 62,7% (compilador) e 61,1% (domínio), ainda abaixo do linear. O p = 0,037 do agregado é inteiramente puxado pelo Granite.
- **Custo.** No Granite os estágios custam **5×**: 225–245 s por caso e ~970 tokens de saída contra 46 s e 192. Nos demais modelos o custo é igual ao linear.
- **O nome dos estágios (compilador × domínio) não faz diferença** (33,5% × 33,9%, p = 0,90). O efeito de +17 pp por alinhar nomes ao pré-treino relatado pelo PA-Tool não se reproduz aqui; o sinal é o previsto, mas de 0,4 pp.

## 4. Onde cada modelo acerta e erra

### 4.1 Por classe de erro (linear)

| Modelo | Léxica | Sintática | Semântica | Tradução | Runtime | Efeito |
|---|---|---|---|---|---|---|
| `granite4.2:8b` | 73,3 | **93,3** | 73,3 | 46,7 | 80,0 | 40,0 |
| `qwen2.5:7b` | 40,0 | 60,0 | 46,7 | 46,7 | 73,3 | **53,3** |
| `qwen2.5-coder:7b` | 60,0 | 53,3 | 53,3 | 13,3 | 73,3 | 40,0 |
| `qwen2.5-coder:3b` | 46,7 | 13,3 | 13,3 | 0,0 | 73,3 | 6,7 |
| `phi4-mini:3.8b` | 46,7 | 0,0 | 20,0 | 6,7 | 60,0 | 6,7 |
| `qwen2.5-coder:1.5b` | 33,3 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| **média** | 50,0 | 36,7 | 34,4 | **18,9** | **60,0** | 24,4 |

A ordem de dificuldade é a mesma em quase todos os modelos: **runtime** (status HTTP explícito: 500, 429, timeout) é a classe mais fácil; **tradução** (escala de preço, chave de junção, contagem) e **efeito** (tela divergente, seletor) são as mais difíceis. As duas classes difíceis exigem exatamente o que o prompt da 2-A não dá — conhecimento do sistema: o que é `valor_produto`, como a página monta o cartão, qual é a chave entre pedido e cliente. É a hipótese central da Fase 2-B.

### 4.2 Por nível de dificuldade (linear)

| Modelo | Fácil (1) | Médio (2) | Difícil (3) |
|---|---|---|---|
| `granite4.2:8b` | 70,0 | 76,7 | 56,7 |
| `qwen2.5:7b` | 53,3 | 60,0 | 46,7 |
| `qwen2.5-coder:7b` | 50,0 | 46,7 | 50,0 |
| `qwen2.5-coder:3b` | 20,0 | 30,0 | 26,7 |
| `phi4-mini:3.8b` | 20,0 | 26,7 | 23,3 |
| `qwen2.5-coder:1.5b` | 6,7 | 3,3 | 6,7 |
| **média** | 36,7 | 40,6 | 35,0 |

**Achado que contraria o desenho:** a escala de níveis — definida pela explicitude do sinal (1: status de erro ou JSON que não parseia; 2: contrato divergente; 3: lógica entre requisições) — **não ordena a dificuldade para os modelos**. O nível médio é o mais fácil na média, e só o Granite mostra a queda esperada no nível 3. A classe explica muito mais que o nível: um caso "fácil" de tradução é mais difícil que um caso "difícil" de runtime. Para o relatório final, isso sugere descrever dificuldade pela classe e tratar o nível como atributo secundário.

## 5. Uso do conjunto de rótulos e modos de falha

| Modelo | Rótulos distintos usados (de 23) | Rótulo mais usado | Fatia | Confusões mais comuns (esperada → respondida) |
|---|---|---|---|---|
| `granite4.2:8b` | 22 | `campo_ausente` | 12% | corpo_nao_e_json → erro_interno_do_servidor (3); estado_da_tela_divergente → campo_ausente (3) |
| `qwen2.5:7b` | 22 | `colecao_no_lugar_de_objeto` | 17% | campo_ausente → tipo_divergente (3); valor_fora_do_dominio → tipo_divergente (3); estado_da_tela_divergente → colecao_no_lugar_de_objeto (3) |
| `qwen2.5-coder:7b` | 20 | `estado_da_tela_divergente` | 9% | chave_de_juncao_errada → valor_fora_do_dominio (3); corpo_nao_e_json → erro_interno_do_servidor (2) |
| `qwen2.5-coder:3b` | 16 | `corpo_nao_e_json` | **42%** | campo_ausente → corpo_nao_e_json (6); estado_da_tela_divergente → corpo_nao_e_json (5) |
| `phi4-mini:3.8b` | 17 | `corpo_vazia` *(não existe)* | 24% | chave_de_juncao_errada → corpo_nao_e_json (5); resposta_truncada → corpo_vazia (4) |
| `qwen2.5-coder:1.5b` | **4** | `corpo_nao_e_json` | **92%** | tudo → corpo_nao_e_json |

Três modos de falha distintos, que a acurácia sozinha não separa:

1. **Confusão entre vizinhos** (Granite, `qwen2.5:7b`, `qwen2.5-coder:7b`): usam quase todo o conjunto e erram entre causas próximas — HTML de erro lido como 500, campo ausente lido como tipo divergente. É erro de diagnóstico, corrigível com contexto.
2. **Colapso para um rótulo** (`qwen2.5-coder:3b` em 42%, `qwen2.5-coder:1.5b` em 92%): o modelo responde a mesma causa independentemente do caso. O 3B ainda nomeia o campo certo em 73% dos casos — localiza, mas não classifica; o 1,5B não faz a tarefa.
3. **Falha de seguir instrução** (`phi4-mini`): 25,6% das respostas usam um rótulo que não está na lista (`corpo_vazia`, variações inventadas). Não é falta de diagnóstico, é falta de aderência ao formato — e é o modelo que mais se beneficia de saída restrita, ao custo documentado no Constraint Tax.

## 6. Perfil por modelo

### `granite4.2:8b` — o único perto da meta
**67,8%** de causa (IC 57,6–76,5), 87,8% de campo, 22 dos 23 rótulos, nenhum fora do conjunto. Quase perfeito em sintática (93,3%) e forte em runtime, léxica e semântica; cai em tradução (46,7%) e efeito (40,0%). É o mais prolixo dos modelos válidos (192 tokens) e o que mais cita hipóteses erradas antes de concluir (16,7% de termo proibido) — a explicação passeia, mas o rótulo final acerta. Custo: 45,7 s por caso e 6,6 GB residentes. Em estágios, desmorona: 5× o tempo e um terço das respostas sem conclusão. **Papel na 2-B:** modelo principal das ablações; a pergunta é se a biblioteca leva tradução e efeito para o patamar das outras classes.

### `qwen2.5:7b` — melhor relação acerto/tempo
**53,3%** (43,1–63,3), 81,1% de campo, 22 rótulos, 1,1% fora. É o melhor de todos em **efeito** (53,3%) e o segundo em runtime; o ponto fraco é léxica (40,0%) — confunde corpo HTML e truncado com outras causas. Responde em 17,1 s com 52 tokens: **3,2 pp de acerto por segundo**, contra 1,5 do Granite. Estratégia não muda nada. **Papel:** candidato natural a padrão de produção se a biblioteca o levar acima de 65%.

### `qwen2.5-coder:7b` — o par controlado
**48,9%** (38,8–59,0). Mesma base, tamanho, tokenizador e mês de treino que o `qwen2.5:7b`, diferindo só pelo ajuste em código — e fica 4,4 pp abaixo, mais lento (25,9 s) e mais prolixo (106 tokens). A diferença está dentro do intervalo de confiança, então a leitura correta é: **a especialização em código não ajuda nesta tarefa e custa 50% mais tempo**. Muito fraco em tradução (13,3%). É o único em que o braço "compilador" fica numericamente acima do linear (52,2%), sem significância.

### `qwen2.5-coder:3b` — localiza, não classifica
**25,6%** de causa, mas **73,3% de campo**: aponta o campo certo e responde `corpo_nao_e_json` para 42% dos casos. Acerta runtime (73,3%) e léxica (46,7%) e praticamente nada do resto (0% em tradução). 8,4 s e 2,3 GB. Era o padrão de produção desde a primeira leva (2 casos); com 90 casos, **não sustenta a tarefa de diagnóstico sozinho**. **Papel na 2-B:** modelo "mediano" das ablações — é o candidato mais interessante para medir se documentação substitui capacidade.

### `phi4-mini:3.8b` — não segue o conjunto fechado
**23,3%** de causa e 33,3% de campo; 0% em sintática. Um quarto das respostas usa rótulo inexistente. Rápido (9,8 s) e conciso (41 tokens). O problema não é raciocínio, é aderência: é o modelo em que um decodificador restrito ao conjunto mudaria mais o resultado — e onde a literatura avisa que isso derruba a acurácia semântica. **Papel:** piso não degenerado das ablações.

### `qwen2.5-coder:1.5b` — não faz a tarefa
**5,6%**, quatro rótulos, `corpo_nao_e_json` em 92% das respostas; os 33,3% em léxica vêm de esse rótulo ser léxico. É verboso (90 tokens; cinco respostas bateram no teto de 400 da primeira leva). Nada em estágios muda o quadro. Excluído das ablações; a ablação de quantização (`q8_0` e `fp16` no mesmo braço) responde se o Q4 explica parte disso.

## 7. Custo

| Modelo | Seg/caso (mediana) | Tokens de saída | RAM residente | Acerto por segundo |
|---|---|---|---|---|
| `qwen2.5-coder:1.5b` | 5,2 | 90 | 1,3 GB | 1,1 pp/s |
| `qwen2.5-coder:3b` | 8,4 | 50 | 2,3 GB | 3,0 pp/s |
| `phi4-mini:3.8b` | 9,8 | 41 | 3,5 GB | 2,4 pp/s |
| `qwen2.5:7b` | 17,1 | 52 | 5,2 GB | **3,1 pp/s** |
| `qwen2.5-coder:7b` | 25,9 | 106 | 5,2 GB | 1,9 pp/s |
| `granite4.2:8b` | 45,7 | 192 | 6,6 GB | 1,5 pp/s |

O tempo é dominado pela quantidade de texto gerado, não pelo porte (achado 4.13 do Memorial, confirmado): o `qwen2.5-coder:7b` é 50% mais lento que o irmão generalista porque escreve o dobro. Na fronteira de Pareto ficam só `qwen2.5:7b` e Granite; os demais são dominados (menos acerto e não mais rápidos que o `qwen2.5:7b` na razão acerto/tempo, ou menos acerto que o Granite). Toda a bateria coube em 16 GB com navegador, banco e servidores parados; com eles rodando, o Granite (6,6 GB) é o único que aperta.

## 8. Ameaças à validade

- **Uma execução por condição**, a `temperature=0.1`. A variação entre execuções não foi medida; o intervalo de Wilson cobre a amostragem dos casos, não a estocasticidade do modelo.
- **Intervalos largos**: com 90 casos, ±10 pp. As diferenças entre os dois 7B e entre as estratégias dos modelos pequenos não são conclusivas.
- **Primeira leva com teto de 400 tokens**, sem o campo `teto_tokens` gravado: 1 resposta do Granite e 5 do `1.5b` no braço linear atingiram esse limite. O do Granite vale no máximo 1,1 pp; o `1.5b` é degenerado independentemente disso.
- **Fixtures escritos à mão**: três descrevem sintomas que o código real não produz ("R$ NaN"; cartões duplicados — achado 4.20). Mantidos para comparabilidade; corrigir depois da 2-B.
- **Conjunto fechado de 23 rótulos** e gabarito único por caso: um diagnóstico correto por outro caminho conta como erro se o rótulo divergir.
- **Só Q4_K_M** e uma única máquina; a ablação de quantização cobre só o menor modelo.
- **Só português**; os modelos abaixo de 5B têm perda documentada nessa língua (PoETa v2).

## 9. Conclusões da Fase 2-A e o que a 2-B testa

1. Sem conhecimento do sistema, o teto é **67,8%** (Granite) e o melhor custo-benefício é **53,3% a 17 s** (`qwen2.5:7b`). A meta de 70–80% não foi atingida por nenhum modelo.
2. **Estrutura de raciocínio em estágios não ajuda** modelos de 1,5B a 8B nesta tarefa e prejudica o maior; o nome dos estágios é irrelevante. A Fase 2-B fixa o prompt linear.
3. As classes difíceis — **tradução e efeito** — são as que dependem de conhecer o sistema. A hipótese da 2-B é que a biblioteca de documentação age exatamente aí.
4. O nível de dificuldade por explicitude do sinal **não prevê** a dificuldade real; a classe prevê.
5. Três modos de falha diferentes (confusão entre vizinhos, colapso num rótulo, rótulo inventado) exigem remédios diferentes: contexto, capacidade e restrição de saída, respectivamente. A biblioteca só endereça o primeiro; medir se ajuda o segundo é o que os braços com `qwen2.5-coder:3b` respondem.
6. **Especialização em código não ajuda**: o par controlado `qwen2.5-coder:7b` × `qwen2.5:7b` empata em acerto e o especializado custa mais.

Hipóteses registradas antes de rodar a 2-B: **H1** a biblioteca sobe o acerto em tradução e efeito mais que nas demais classes; **H2** nos modelos abaixo de 5B, a biblioteca recuperada (top-3) rende mais que a biblioteca inteira; **H3** o Granite com biblioteca cruza 70%; **H4** o `qwen2.5-coder:3b` com biblioteca reduz o colapso em `corpo_nao_e_json`.
