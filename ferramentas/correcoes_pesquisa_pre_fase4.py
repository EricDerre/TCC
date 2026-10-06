#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (05/10/2026) com as correções declaradas das sínteses e do mapa da parte A
# da rodada 5 da pesquisa (Pré-Fase 4), que integrar_pesquisa_pre_fase4.py aplica ao texto dos agentes antes de
# gravar o levantamento §6.14. Cada item diz onde (chave do tópico ou `mapa:A`), o trecho exato como o agente
# escreveu (`de`, que tem de aparecer uma única vez), a forma corrigida (`para`) e o motivo, tirado da afirmação
# verificada que a frase citava.
# ! Motivo: em 01/10/2026 seis revisores (um por tópico e um para o mapa) conferiram as sínteses contra as afirmações
# verificadas e apontaram 104 trechos, quase todos frase mais forte que a fonte (requisito no lugar de hardware da
# medida, "único" sem fonte, condição de medição omitida, conclusão da síntese escrita como se fosse da fonte), alguns
# números e citações erradas (RAM mínima do colibri, limiar do top-p, tamanho que veio da página de tags do Ollama e
# não do model card) e uma contradição entre a leitura do mapa e as linhas dele (OLMoE e LFM2 "candidatos" numa parte
# e descartados noutra). Também entrou aqui a correção do erro meu achado na mesma revisão: a síntese e o mapa
# comparavam a RAM livre (cerca de 7 GB) com o mínimo de 16 GB do repositório, e o mínimo se compara com a RAM
# instalada, que nesta máquina é exatamente 16 GB. As correções ficam declaradas (não escondidas no texto) para o
# levantamento continuar rastreável: o §6.14.12 lista cada trecho, como ficou e por quê, e o cabeçalho avisa.
"""As correções são dados, não código: a lista CORRECOES_DA_REVISAO é lida por integrar_pesquisa_pre_fase4.py. Para
acrescentar uma, copiar o trecho exato do texto do agente em `de` (ele é conferido: tem de aparecer uma vez só) e
escrever `para` e `motivo` sem travessão nem seta."""
from __future__ import annotations

DATA_DAS_CORRECOES = "05/10/2026"

ATLAS = "r5-atlas-e-especializacao"
BASE = "r5-base-de-pesquisa-do-colibri"
MOE = "r5-moe-pequenos-em-cpu"
PESOS = "r5-pesos-em-disco"
COLIBRI = "r5-colibri-leitura-integral"
MAPA = "mapa:A"


def _c(onde: str, de: str, para: str, motivo: str) -> dict:
    return {"onde": onde, "de": de, "para": para, "motivo": motivo}


# ------------------------------------------------------------------ §6.14.5 atlas e especialização
_CUSTO_DA_SONDA = "nenhuma fonte mede o custo de extrair ativações e treinar sondas em CPU; a própria lacuna da síntese diz que a viabilidade é inferida, não verificada."
_UM_QUARTO = "é declaração qualitativa dos próprios autores, sobre o Claude 3.5 Haiku, e não uma taxa de cobertura medida."
_GPU_DAS_SAES = ("as fontes verificadas não declaram exigência de GPU nem de pesos em precisão cheia: o README do circuit-tracer trata a GPU como caso "
                 "normal e não documenta execução só em CPU, e o Gemma Scope relata o custo do conjunto inteiro.")
_WANG = "a citação ficava ambígua com WANG; HAYOU; NALISNICK (2026), do mesmo ano; a inicial do primeiro autor distingue as duas."
_CORRECOES_DO_ATLAS = [
    _c(ATLAS, "não é um termo estabelecido na literatura de Mixture-of-Experts (MoE)",
       "não aparece como termo nas fontes de Mixture-of-Experts (MoE) levantadas nesta rodada",
       "nenhuma afirmação verificada sustenta a ausência do termo na literatura inteira; o que as fontes permitem dizer é que não o usam."),
    _c(ATLAS, "Daí resulta que a frequência de seleção mistura preferência por magnitude com qualquer noção de competência.",
       "Uma leitura possível, desta síntese e não dos autores, é que a frequência de seleção mistura preferência por magnitude com qualquer noção de competência.",
       "a fonte afirma que o roteador tende a escolher especialistas de norma de saída maior; a consequência para a leitura das frequências é inferência da síntese."),
    _c(ATLAS, "cerca de 60% no top-8 após 1% do pré-treino e cerca de 80% após 40%",
       "cerca de 60% no top-8 após 1% do pré-treino e até cerca de 80% após 40%",
       "o número sustentado pela verificação é \"até cerca de 80%\" após 40% do pré-treino."),
    _c(ATLAS, "o método FAST liberou 240 SAEs, treinados nas camadas 4, 12, 18, 20 e 25, e relata",
       "o método FAST treinou SAEs nas camadas 4, 12, 18, 20 e 25 desse modelo (os 240 SAEs liberados são o total para os modelos Qwen2.5 Instruct de 0,5B a 7B e "
       "Llama-3.x Instruct de 1B a 8B) e relata",
       "os 240 SAEs são o total do trabalho, para várias famílias e tamanhos, não só para o Qwen2.5-7B-Instruct."),
    _c(ATLAS, "para o Gemma 2 2B, 9B e 27B, consumindo",
       "para o Gemma 2 2B e 9B (todas as camadas) e 27B (só camadas selecionadas), consumindo",
       "condição da afirmação verificada: no modelo de 27B só camadas selecionadas receberam SAEs."),
    _c(ATLAS, "Serve também, como experimento opcional e barato, uma sonda linear",
       "Serve também, como experimento opcional cujo custo nesta máquina não foi medido, uma sonda linear", _CUSTO_DA_SONDA),
    _c(ATLAS, "a ferramenta compatível com a CPU da máquina-alvo é uma sonda linear ou uma diferença de médias em modelo pequeno",
       "a ferramenta mais simples a tentar é uma sonda linear ou uma diferença de médias em modelo pequeno, com custo na CPU da máquina-alvo ainda não medido",
       _CUSTO_DA_SONDA),
    _c(ATLAS, "que exigem pesos em precisão cheia e GPU, recursos que a i5-1235U sem GPU utilizável e com cerca de 7 GB livres não oferece",
       "que as fontes descrevem em infraestrutura de laboratório ou com a GPU como caso normal, sem documentar execução só em CPU; nada disso foi medido numa "
       "máquina como a i5-1235U, sem GPU utilizável e com cerca de 7 GB livres", _GPU_DAS_SAES),
    _c(ATLAS, "O circuit-tracer não oferece transcoders para Qwen2.5 e pressupõe GPU (cerca de 15 GB para o Gemma-2-2B)",
       "O circuit-tracer não oferece transcoders para Qwen2.5, e o README dele trata a GPU como caso normal (cerca de 15 GB para o Gemma-2-2B), sem documentar "
       "execução só em CPU",
       "\"pressupõe GPU\" é mais forte que o verificado: o README toma a GPU como caso normal e não documenta execução só em CPU."),
    _c(ATLAS, "operam sobre pesos em precisão cheia e não sobre o GGUF Q4_K_M servido pelo Ollama; o agente local não pode usá-los sem trocar a pilha de inferência",
       "foram treinados sobre ativações do modelo original, e a fonte não diz em que precisão dos pesos operam nem se valem para o GGUF Q4_K_M servido pelo Ollama; "
       "usá-los no agente local dependeria de extrair ativações do modelo, o que não foi verificado na pilha atual",
       "a afirmação verificada (parcial) cobre a existência dos SAEs e o valor do MSE; precisão dos pesos e compatibilidade com GGUF não foram verificadas."),
    _c(ATLAS, "porque o roteamento reflete geometria e sintaxe, não domínio (JIANG et al., 2024; WANG; HAYOU; NALISNICK, 2026)",
       "porque, em parte dos modelos medidos, o roteamento acompanha a geometria dos estados ocultos e a sintaxe, e não o domínio (JIANG et al., 2024; WANG; HAYOU; "
       "NALISNICK, 2026), enquanto o OLMoE mostra especialização por domínio (MUENNIGHOFF et al., 2025)",
       "o resultado não é geral: o OLMoE mostra especialização por domínio e por vocabulário, e os autores do trabalho sobre geometria dizem \"não necessariamente\"."),
    _c(ATLAS, "porque o roteamento reflete a geometria dos estados ocultos e mostra cerca de 60% de sobreposição até entre problemas diferentes",
       "porque, nos cinco MoEs medidos em tarefas de matemática, o roteamento acompanha a geometria dos estados ocultos, com cerca de 60% de sobreposição até entre "
       "problemas diferentes, e não necessariamente a competência de domínio",
       "condição da medida (cinco MoEs, tarefas de matemática) e o \"não necessariamente\" dos autores."),
    _c(ATLAS, "é a propriedade que tornaria viável o carregamento sob demanda do SSD num MoE; ela não diz nada sobre competência temática",
       "é uma propriedade que, por inferência desta síntese e não da fonte, favoreceria o carregamento sob demanda do SSD num MoE; ela não diz nada sobre competência temática",
       "o artigo do Mixtral mede a repetição de especialista entre tokens; a ligação com leitura do SSD não está nele."),
    _c(ATLAS, "e a cobertura de cerca de um quarto dos prompts (KORZNIKOV et al., 2026; LINDSEY et al., 2025)",
       "e a compreensão satisfatória, segundo os próprios autores, em cerca de um quarto dos prompts testados no Claude 3.5 Haiku (KORZNIKOV et al., 2026; LINDSEY et al., 2025)",
       _UM_QUARTO),
    _c(ATLAS, "com compreensão satisfatória em cerca de um quarto dos prompts; não serve",
       "com compreensão satisfatória, segundo os autores, em cerca de um quarto dos prompts testados no Claude 3.5 Haiku; não serve", _UM_QUARTO),
    _c(ATLAS, "num preprint sem revisão por pares (WANG et al., 2026) [parcial]", "num preprint sem revisão por pares (WANG, J. et al., 2026) [parcial]", _WANG),
    _c(ATLAS, "exigem retreino em GPU e não se aplicam ao agente local nem à Fase 4 (WANG et al., 2026 - afirmacao 10)",
       "foram alegados para MoEs grandes das séries Qwen, DeepSeek e GLM, com 15% dos recursos de treino, num preprint sem revisão por pares; como o modelo do agente "
       "é denso, não se aplicam ao agente local nem à Fase 4 (WANG, J. et al., 2026 - afirmacao 10)",
       "\"retreino em GPU\" não está na afirmação verificada, que fala em 15% dos recursos de treino em MoEs grandes; " + _WANG),
    _c(ATLAS, "e deixar claro que o resultado depende de como o MoE foi treinado",
       "e registrar que, segundo a hipótese dos autores do OLMoE, o resultado depende de como o MoE foi treinado",
       "atribuir a especialização pequena do Mixtral ao upcycling é hipótese dos autores, não resultado medido."),
    _c(ATLAS, "pois SAEs empataram com direções aleatórias (0,87 contra 0,90 em interpretabilidade)",
       "pois, num preprint que testou várias arquiteturas de SAE, eles empataram com baselines aleatórios (0,87 contra 0,90 em interpretabilidade); o resultado é "
       "sobre SAEs, e estendê-lo a outras figuras é cautela desta síntese",
       "o resultado verificado é sobre SAEs e vem de um preprint."),
    _c(ATLAS, "embora expliquem 71% da variância (KORZNIKOV et al., 2026)",
       "embora expliquem 71% da variância, resultado de um preprint (KORZNIKOV et al., 2026)",
       "a fonte é um preprint, condição que o texto omitia."),
    _c(ATLAS, "considerando o custo de referência do Gemma Scope (mais de 20% do compute do GPT-3 e cerca de 20 PiB de ativações)",
       "tomando como ordem de grandeza o custo do conjunto inteiro do Gemma Scope, com mais de 400 SAEs para três modelos (mais de 20% do compute do GPT-3 e cerca "
       "de 20 PiB de ativações); o custo de um único SAE para um modelo de 7B não está nas fontes",
       "o custo verificado é o do conjunto inteiro do Gemma Scope, não o de treinar um SAE."),
    _c(ATLAS, "Em comum, essas fontes sustentam a mesma cautela", "Na leitura desta síntese, essas fontes pedem a mesma cautela",
       "a conclusão comum é da síntese; nenhuma fonte a enuncia."),
    _c(ATLAS, "todas usam temas gerais, matemática ou código",
       "as fontes de roteamento usam temas gerais, matemática ou código, e as de interpretabilidade usam outros dados (imagens, conjuntos de sondagem, prompts avulsos)",
       "a lista de tipos de dado não cobria todas as fontes do tópico (o Activation Atlas usa imagens; a sondagem, 113 conjuntos de dados)."),
]

# ------------------------------------------------------------------ §6.14.2 base de pesquisa do colibri
_RAM_DO_COLIBRI = ("o mínimo de 16 GB do repositório se compara com a RAM instalada, que nesta máquina é igual a ele, e não com a RAM livre; a faixa de 0,05 a 0,1 "
                   "token/s foi medida numa máquina de 25 GB cujo hardware o README não detalha; e o GLM-5.2 não cabe no disco livre (aviso sobre a memória, no cabeçalho).")
_HARDWARE_DA_MEDIDA = "as fontes informam o hardware em que mediram, não requisitos mínimos."
_FUSAO = "a queda verificada é na média de código do Qwen3-30B-A3B; o MC-SMoE relata virtualmente nenhuma perda em 8 benchmarks de NLU."
_CORRECOES_DA_BASE = [
    _c(BASE, "Com cerca de 7 GB livres, abaixo dos 16 GB mínimos do colibri, a expectativa razoável fica no máximo na faixa de 0,05 a 0,1 token/s (JUSTVUGG, 2026).",
       "A máquina-alvo tem instalada exatamente a RAM mínima que o colibri declara para o GLM-5.2 (16 GB) e não tem espaço livre em disco para ele. Não há medida "
       "numa máquina dessa classe: a referência mais próxima no README é a máquina de 25 GB, de hardware não detalhado, que fica de 0,05 a 0,1 token/s a frio "
       "(JUSTVUGG, 2026), e tomá-la como teto para a máquina-alvo é extrapolação desta síntese.", _RAM_DO_COLIBRI),
    _c(BASE, "mostram que o custo dominante é a falha de cache",
       "mostram que reduzir as falhas de cache baixa o tempo por token, sem decompor o custo a ponto de dizer qual parcela domina",
       "nenhuma das duas fontes decompõe o custo por token; elas medem o ganho ao reduzir as falhas de cache."),
    _c(BASE, "Rodar o colibri na máquina-alvo, com cerca de 7 GB livres e abaixo dos 16 GB mínimos, levaria a 0,05-0,1 token/s, ou cerca de 10 a 20 minutos para 61 tokens, "
       "contra 47 a 78 s atuais",
       "Rodar o GLM-5.2 pelo colibri na máquina-alvo não é possível hoje (o modelo não cabe no disco livre, e a RAM instalada é exatamente o mínimo declarado de 16 GB). "
       "Na máquina de 25 GB do README, de hardware não detalhado, ele fica em 0,05-0,1 token/s a frio, o que daria cerca de 10 a 20 minutos para 61 tokens, contra "
       "47 a 78 s atuais", _RAM_DO_COLIBRI),
    _c(BASE, "A política padrão do colibri não altera precisão nem semântica do roteador, então citar poda, fusão ou re-roteamento como recurso do motor seria incorreto no TCC",
       "A política padrão do colibri nunca altera em silêncio a precisão nem a semântica do roteador, o que admite mudança explícita por opção; citar poda, fusão ou "
       "re-roteamento como comportamento padrão do motor seria incorreto no TCC",
       "o README diz \"never silently changes\", o que admite mudança explícita (o CACHE_ROUTE e o top-p são opcionais)."),
    _c(BASE, "a única evidência próxima da máquina-alvo (16 GB, llama.cpp com mmap, NVMe Gen3) indica que a falha de cache domina o tempo por token, com cortes de 43,6% a "
       "49,8% ao reduzi-la",
       "a evidência mais próxima da máquina-alvo é a de uma placa embarcada Jetson Orin NX (16 GB, llama.cpp com mmap, NVMe Gen3), que não é um x86 só com CPU: nela, "
       "reutilizar especialistas recentes cortou o tempo por token em 43,6% a 49,8%, sem que o estudo decomponha o custo",
       "o Jetson Orin NX é placa embarcada com GPU, não CPU x86; e a fonte não decompõe o custo por token."),
    _c(BASE, "HybriMoE e KTransformers, que exigem GPU discreta, AMX ou AVX-512 e centenas de GB de RAM",
       "HybriMoE e KTransformers, medidos com GPU discreta (RTX A6000 com Xeon Gold 5220R no primeiro; GPU de 24 GB, Xeon com AMX e centenas de GB de RAM no segundo), "
       "que é o hardware das medidas e não um requisito declarado", _HARDWARE_DA_MEDIDA),
    _c(BASE, "Os ganhos do KTransformers dependem de AMX ou AVX-512, GPU de 24 GB e centenas de GB de RAM",
       "Os ganhos do KTransformers foram medidos num Xeon com AMX, com GPU de 24 GB e centenas de GB de RAM", _HARDWARE_DA_MEDIDA),
    _c(BASE, "ScMoE, EASY-EP e OD-MoE, que dependem de várias GPUs ou de vários nós", "ScMoE, EASY-EP e OD-MoE, medidos com várias GPUs ou vários nós", _HARDWARE_DA_MEDIDA),
    _c(BASE, "custaram de 6 a 11 pontos de acurácia no Mixtral-8x7B, margem incompatível com a estabilidade atual do agente; não devem entrar na Fase 4",
       "custaram de 6 a 11 pontos de acurácia média no Mixtral-8x7B (0,57 com 40% de compressão e 0,52 com 60%, contra 0,63, em GPU A100). A perda menor é da ordem da "
       "variação de 0 a 3 casos em 36 entre corridas iguais do agente, então chamá-la de incompatível pediria medição própria; como o modelo decidido é denso, não "
       "entram na Fase 4",
       "a fonte dá 0,57 e 0,52 contra 0,63, em A100; \"incompatível\" era juízo da síntese sem comparação com a variação medida do agente."),
    _c(BASE, "O SERE só ganha com lote grande e QPS de 16 a 24",
       "O ganho do SERE foi medido com decodificação em lote e QPS de 16 a 24 e depende do tamanho do lote e da taxa de requisições",
       "a fonte diz que o ganho depende do lote e da taxa de requisições e informa as condições da medida; não diz que só há ganho com lote grande."),
    _c(BASE, "A carga sob demanda guiada por previsão depende de paralelizar a carga entre 10 nós; um único notebook não reproduz o ganho, o que reforça",
       "A carga sob demanda guiada por previsão (OD-MoE) foi medida numa bancada de 10 nós de borda com GPUs de menos de 1 GB; não há medida num único notebook, o que, "
       "na leitura desta síntese, reforça",
       "a fonte descreve o arranjo da medida, não uma dependência; e não há medida em notebook."),
    _c(BASE, "(perplexidade de 0,1% a 3% pior); como entre corridas iguais",
       "(perplexidade de 0,1% a 3% pior, com queda abaixo de 0,1% no MMLU e no GSM8K); como entre corridas iguais",
       "a fonte também mede a exatidão (MMLU e GSM8K), com queda abaixo de 0,1%; só a perplexidade dava a impressão de perda maior."),
    _c(BASE, "pois perde muito em tarefas gerativas e o agente gera respostas de 4 linhas fixas",
       "pois, na média de código do Qwen3-30B-A3B com 50% dos especialistas, caiu para 0,364 a 0,397 contra 0,558 do original (em NLU, o MC-SMoE relata virtualmente "
       "nenhuma perda); estender a queda a outras tarefas gerativas, como as 4 linhas fixas do agente, é inferência desta síntese", _FUSAO),
    _c(BASE, "a fusão de especialistas, também pelo resultado negativo em tarefas gerativas (LASBY et al., 2026)",
       "a fusão de especialistas, também pela queda medida em código (LASBY et al., 2026), embora em NLU o MC-SMoE relate virtualmente nenhuma perda (LI et al., 2024)", _FUSAO),
    _c(BASE, "e obteve 1,33x no prefill e 1,70x na decodificação sobre o kTransformers",
       "e obteve aceleração média de 1,33x no prefill e de 1,70x na decodificação sobre o kTransformers", "a fonte fala em aceleração média."),
    _c(BASE, "atinge cerca de 75% da velocidade de uma implantação totalmente em cache de GPU, usando 1/3 da memória",
       "atinge cerca de 75% da velocidade de decodificação de uma implantação totalmente em cache de GPU, usando 1/3 da memória de GPU",
       "qualificadores da afirmação verificada: velocidade de decodificação e memória de GPU."),
    _c(BASE, "medidos apenas em GPU e em modelos de dezenas a centenas de bilhões de parâmetros",
       "medidos apenas em GPU e em modelos de dezenas de bilhões a 1 trilhão de parâmetros", "o MoBE foi medido até no Kimi-K2, de 1 trilhão de parâmetros."),
    _c(BASE, "o colibri como motor de produção, porque a 0,05 a 0,1 token/s inviabiliza o laço de diagnóstico",
       "o colibri como motor de produção, porque a faixa de 0,05 a 0,1 token/s, medida a frio numa máquina de 25 GB, já inviabilizaria o laço de diagnóstico",
       "a faixa é de outra máquina; na máquina-alvo o GLM-5.2 nem cabe no disco."),
]

# ------------------------------------------------------------------ §6.14.4 MoE pequenos em CPU
_COMPRESSAO = "a fonte dos super experts mede poda em pesos completos, não quantização; a fonte de quantização cobre só 4 bits."
_VERSOES_DO_OLLAMA = "a issue do Qwen3:30B-A3B no aparelho de 12 GB (#12615) é de outubro de 2025 e não informa a versão do Ollama."
_RECUSA_DO_OLLAMA = "os relatos de recusa são das versões 0.4.7 e 0.5.7 e de uma issue sem versão; o comportamento na 0.34.4 não foi verificado."
_CORRECOES_DOS_MOE = [
    _c(MOE, "Também não serve a compressão agressiva (Q2/Q3 ou poda) para encaixar um MoE médio em 16 GB, pela fragilidade dos super experts.",
       "Também fica sem apoio a compressão agressiva para encaixar um MoE médio em 16 GB: a poda de 3 super experts, medida em pesos completos, derrubou o "
       "Qwen3-30B-A3B, e nenhuma fonte verificada mede quantização abaixo de 4 bits em MoE; descartar Q2 e Q3 é cautela desta síntese, não resultado medido.", _COMPRESSAO),
    _c(MOE, "Quantizações abaixo de Q4 ou poda de especialistas para encaixar um MoE médio em 16 GB não devem ser tentadas. Podar 3 super experts do Qwen3-30B-A3B elevou "
       "a perplexidade de 8,70 para 59,86",
       "A poda de especialistas para encaixar um MoE médio em 16 GB não deve ser tentada sem medição: podar 3 super experts do Qwen3-30B-A3B, em pesos completos, elevou "
       "a perplexidade de 8,70 para 59,86. Sobre quantização abaixo de Q4 em MoE não há fonte verificada nesta rodada, e evitá-la é cautela desta síntese", _COMPRESSAO),
    _c(MOE, "Esses relatos são das versões 0.4.7 e 0.5.7, e o comportamento na 0.34.4 não foi verificado",
       "Os relatos das issues #7942 e #8654 são das versões 0.4.7 e 0.5.7, o da issue #12615 é de outubro de 2025 e não informa a versão, e o comportamento na 0.34.4 "
       "não foi verificado", _VERSOES_DO_OLLAMA),
    _c(MOE, "As issues citadas são de versões 0.4.7 e 0.5.7.", "As issues citadas são das versões 0.4.7 e 0.5.7 e de outubro de 2025, esta sem versão informada.",
       _VERSOES_DO_OLLAMA),
    _c(MOE, "O segundo grupo reúne os MoE de porte médio, mais fortes que o qwen2.5:7b mas maiores que a RAM.",
       "O segundo grupo reúne os MoE de porte médio, maiores que a RAM e, no único caso com comparação na mesma avaliação (o Qwen3-30B-A3B), com MMLU acima do "
       "Qwen2.5-7B base.",
       "só o Qwen3-30B-A3B tem comparação com o Qwen2.5-7B na mesma avaliação; os escores do Granite e do Qwen3.6 vêm de avaliações de outras origens ou de outro benchmark."),
    _c(MOE, "é mais forte que o denso decidido, mas ocupa de 19 a 24 GB e o Ollama recusa ou derruba modelos maiores que a memória disponível",
       "nos números publicados, o Qwen3-30B-A3B base supera o Qwen2.5-7B base em MMLU (os outros dois não têm comparação na mesma avaliação), mas o grupo ocupa de 19 a "
       "24 GB, e há relatos de que o Ollama, em versões anteriores à 0.34.4, recusou ou derrubou modelos maiores que a memória disponível",
       "comparações de MMLU de origens diferentes não sustentam \"mais forte\"; e " + _RECUSA_DO_OLLAMA),
    _c(MOE, "Rodar um MoE maior que a RAM exigiria trocar o servidor por llama.cpp com mmap, já que o Ollama recusa ou derruba esses modelos",
       "Rodar um MoE maior que a RAM poderia exigir trocar o servidor por llama.cpp com mmap, já que há relatos, em versões antigas do Ollama, de recusa ou queda com "
       "esses modelos (comportamento não verificado na 0.34.4)", _RECUSA_DO_OLLAMA),
    _c(MOE, "A quantização pós-treino se comporta de outro modo em MoE, então seria preciso repetir os 36 casos",
       "A quantização pós-treino convencional de 4 bits perdeu exatidão em MoE num estudo em GPU (não em GGUF), então seria preciso repetir os 36 casos",
       "a fonte mede PTQ de 4 bits em GPU; não trata de GGUF."),
    _c(MOE, "O Qwen3-30B-A3B supera o Qwen2.5-7B em MMLU (81,38 contra 74,16) e em benchmarks multilíngues.",
       "O Qwen3-30B-A3B base supera o Qwen2.5-7B base em MMLU (81,38 contra 74,16); no MMMLU, a comparação verificada é com o Qwen3-8B (81,46 contra 75,72), não com o "
       "Qwen2.5-7B.", "a comparação multilíngue verificada é com o Qwen3-8B."),
    _c(MOE, "um MoE pequeno de 4 a 5 GB (Granite 4.0 H Tiny, OLMoE ou LFM2-8B-A1B). Ele cabe nos cerca de 7 GB livres com num_ctx=8192 e decodifica de 1,8 a 3,1 vezes "
       "mais rápido que um denso de 4B em CPU.",
       "um MoE pequeno (Granite 4.0 H Tiny, com 4,2 GB; OLMoE em Q4_K_M, com 4,21 GB; LFM2-8B-A1B, de tamanho não verificado). Os dois arquivos medidos são menores que "
       "os cerca de 7 GB livres, mas o tamanho não inclui o KV cache de num_ctx=8192, e caber não foi medido. Em Q4_0, o LFM2-8B-A1B e o Granite 4.0 H Tiny "
       "decodificaram de 1,8 a 3,1 vezes mais rápido que um denso de 4B num Ryzen AI 9 HX 370 e num Galaxy S25; o OLMoE não entrou nessa medida.",
       "o tamanho do LFM2 não foi verificado; os tamanhos do Ollama não incluem KV cache; e a medida de velocidade cobre só LFM2 e Granite Tiny, em Q4_0."),
    _c(MOE, "O preço é um MMLU inferior ao do qwen2.5:7b e um risco maior",
       "O preço provável é um MMLU publicado abaixo do Qwen2.5-7B base, em avaliações de origens diferentes, e um risco maior",
       "os MMLU vêm de avaliações de origens diferentes (IBM, Ai2, Liquid e Qwen)."),
    _c(MOE, "e entrega cerca de 2 tok/s mesmo em hardware muito superior",
       "e a medida verificada dela, com o GLM-5.2 (cerca de 254 GB, na quantização UD-Q2_K_XL) numa NVIDIA GB10 de 128 GB, ficou em cerca de 2 tok/s, número de um "
       "modelo muito maior que os MoE médios e que não se transfere para eles",
       "o número é do GLM-5.2 de cerca de 254 GB, modelo muito maior que os MoE médios do grupo."),
    _c(MOE, "o GLM-5.2 decodificou a cerca de 2,20 tok/s", "o GLM-5.2 (cerca de 254 GB, na quantização UD-Q2_K_XL) decodificou a cerca de 2,20 tok/s",
       "condição da medida: o tamanho e a quantização do modelo."),
    _c(MOE, "Os escores são MMLU 64,84, MMLU-Pro 37,42, IFEval 77,58, IFBench 25,85 e MMMLU 55,26. O pré-treino teve cerca de 55% de inglês, 25% de conteúdo multilíngue e "
       "20% de código. O modelo foi depreciado em favor do LFM2.5-8B-A1B (maio de 2026, IFEval 91,84), cujas velocidades publicadas usam hardware de banda muito maior.",
       "Os escores que a verificação sustentou são MMLU 64,84, IFEval 77,58 e IFBench 25,85. O pesquisador trouxe ainda MMLU-Pro 37,42, MMMLU 55,26, a composição do "
       "pré-treino (cerca de 55% de inglês, 25% de conteúdo multilíngue e 20% de código) e a depreciação em favor do LFM2.5-8B-A1B (maio de 2026, IFEval 91,84), com "
       "velocidades publicadas em hardware de banda muito maior; esses dados não estão entre os números que a verificação sustentou.",
       "a afirmação teve suporte parcial: o verificador sustentou parâmetros, especialistas e três escores."),
    _c(MOE, "O MoE pequeno com melhor velocidade, o LFM2-8B-A1B, tem IFBench de 25,85",
       "O MoE pequeno mais rápido na medida da própria Liquid (contra o Granite 4.0 H Tiny e um denso de 4B; o OLMoE não entrou), o LFM2-8B-A1B, tem IFBench de 25,85",
       "a comparação de velocidade verificada cobre só LFM2, Granite Tiny e Qwen3-4B, no relatório da Liquid."),
    _c(MOE, "Tem MMLU-Pro de 85,2, o raciocínio vem ligado por padrão e a tag Q4_K_M ocupa 24 GB no Ollama [parcial] (QWEN TEAM, 2026).",
       "Tem MMLU-Pro de 85,2 e o raciocínio vem ligado por padrão (QWEN TEAM, 2026). A tag Q4_K_M ocupa 24 GB segundo a página de tags do Ollama consultada em "
       "01/10/2026, fonte que não é o model card e não entrou nas referências do tópico [parcial].",
       "o tamanho de 24 GB vem da página de tags do Ollama, não do model card citado."),
    _c(MOE, "tem 24 GB em Q4_K_M e o raciocínio vem ligado por padrão, o que inflaria a resposta mediana atual de 61 tokens",
       "tem 24 GB em Q4_K_M (tamanho lido na página de tags do Ollama, não no model card) e o raciocínio vem ligado por padrão, o que tenderia a inflar a resposta "
       "mediana atual de 61 tokens", "atribuição do tamanho; e o efeito na resposta é expectativa, não medida."),
    _c(MOE, "em Q4_K_M tem 4,21 GB. A própria Ai2",
       "em Q4_K_M tem 4,21 GB (tamanho lido no repositório allenai/OLMoE-1B-7B-0125-Instruct-GGUF, no Hugging Face, que não está entre as referências do tópico). A própria Ai2",
       "o tamanho do GGUF vem do repositório do Hugging Face, não do blog citado."),
    _c(MOE, "Tem 4,2 GB, licença Apache 2.0 e português declarado, mas MMLU de 68,65",
       "Tem 4,2 GB na biblioteca do Ollama (OLLAMA, 2026 - afirmação 15), licença Apache 2.0 e português declarado, mas MMLU de 68,65",
       "o tamanho de 4,2 GB vem da página de tags do Ollama, não do model card da IBM."),
    _c(MOE, "Servem de teto de expectativa, não de previsão para a máquina-alvo com Q4_K_M",
       "Servem de referência de outro hardware e de outra quantização, não de teto nem de previsão para a máquina-alvo com Q4_K_M",
       "nenhuma fonte sustenta que o valor seja um teto para o i5-1235U."),
    _c(MOE, "O único dado vem de uma GB10 com 128 GB de memória unificada.",
       "Os dados verificados vêm de uma GB10 com 128 GB de memória unificada (PR do llama.cpp) e de um M5 Pro com SSD Apple (leituras por fatia, na discussão do llama.cpp).",
       "a discussão do llama.cpp também traz medidas de leitura seletiva num M5 Pro com SSD Apple."),
    _c(MOE, "O ganho de velocidade desses modelos está medido em CPU de notebook.",
       "O ganho de velocidade de dois desses modelos (LFM2-8B-A1B e Granite-4.0-H-Tiny) está medido na CPU de um notebook e na de um celular.",
       "a medida cobre dois dos três modelos e inclui um celular (Galaxy S25)."),
    _c(MOE, "Num Galaxy S25 (Snapdragon 8 Elite), os valores foram 48,6, 39,2 e 17,2 tok/s.",
       "Num Galaxy S25 (Snapdragon 8 Elite), com prompt de 1K tokens, os valores foram 48,6, 39,2 e 17,2 tok/s.", "condição da medida."),
    _c(MOE, "Esse é o custo dominante por diagnóstico no projeto.",
       "Nos registros da Fase 3 do projeto, o prefill toma a maior parte do tempo de cada diagnóstico (aviso 1 do cabeçalho).",
       "fato do projeto, com a medida declarada no cabeçalho, não das fontes."),
]

# ------------------------------------------------------------------ §6.14.3 pesos fora da RAM
_PAGINACAO = "os números de leitura e escrita do estudo são da descarga do cache KV, e o arquivo de paginação não está no estudo: é hipótese da síntese."
_INGENUO = "o número de carregamento ingênuo é do OPT-6.7B num Apple M1 Max com cerca de metade do modelo na DRAM; a transposição para esta máquina é inferência."
_RELATO_M1 = ("o relato é de um MacBook M1 com o Qwen3-30B-A3B; o melhor valor medido foi 4,7 tok/s, e o teto de cômputo de 4,4 tok/s é do benchmark em C, não um "
              "teto para o i5-1235U.")
_GARGALO = "só duas fontes medem o peso da E/S; generalizar a todas era mais forte que o verificado."
_CORRECOES_DOS_PESOS = [
    _c(PESOS, "Na máquina-alvo, ele viria do arquivo de paginação sob pressão de memória.",
       "Na máquina-alvo, por hipótese desta síntese e não do estudo, ele viria do arquivo de paginação sob pressão de memória.", _PAGINACAO),
    _c(PESOS, "A leitura de pesos quase não escreve no SSD (2,0 GiB/s de leitura contra 11,0 MiB/s de escrita no estudo), então o risco de escrita vem da troca",
       "No estudo, a descarga de pesos é essencialmente carga de leitura (os 2,0 GiB/s de leitura contra 11,0 MiB/s de escrita são da descarga do cache KV, não dos "
       "pesos); que o risco de escrita venha da troca é hipótese desta síntese, não do estudo", _PAGINACAO),
    _c(PESOS, "e vigiar o arquivo de paginação como fonte real de escrita (REN et al., 2025)",
       "e vigiar o arquivo de paginação como fonte provável de escrita, hipótese desta síntese apoiada em que a descarga de pesos é carga de leitura (REN et al., 2025)",
       _PAGINACAO),
    _c(PESOS, "embora ele seja apontado como o risco real de escrita",
       "embora esta síntese o trate como o risco provável de escrita (a documentação do colibri, no tópico da leitura integral, aponta o swap como o que desgasta o disco)",
       "nenhuma fonte deste tópico aponta o arquivo de paginação; quem aponta o swap é o repositório colibri."),
    _c(PESOS, "e a descarga só reproduziria o regime ingênuo de frações de token por segundo (ALIZADEH et al., 2024)",
       "e a descarga não tem o que ganhar: a única medida de carregamento ingênuo de um denso desse porte (OPT-6.7B com cerca de metade do modelo na DRAM, num Apple M1 "
       "Max com SSD acima de 6 GiB/s) ficou em frações de token por segundo (ALIZADEH et al., 2024), e esperar regime parecido na máquina-alvo é inferência desta síntese",
       _INGENUO),
    _c(PESOS, "e ler pesos do SSD só reproduziria o regime ingênuo de cerca de 0,46 tok/s",
       "e a medida disponível de carregamento ingênuo do SSD, de cerca de 0,46 tok/s, é do OPT-6.7B num Apple M1 Max com cerca de metade do modelo na DRAM, sem repetição "
       "em x86 nem com o qwen2.5:7b", _INGENUO),
    _c(PESOS, "o PowerInfer-2 caiu de 11,68 para 2,13 tok/s, e a máquina-alvo tem esse mesmo orçamento livre",
       "o PowerInfer-2 caiu de 11,68 para 2,13 tok/s com o TurboSparse-Mixtral-47B num celular OnePlus 12 (NPU e CPU, UFS 4.0); a máquina-alvo tem orçamento livre "
       "parecido, mas outro hardware e outro modelo, então o número vale como alerta, não como previsão",
       "condições da medida: celular com NPU e modelo esparsificado de 47B."),
    _c(PESOS, "e não para o prefill, que domina o custo.",
       "e não para o prefill, que nos registros da Fase 3 deste projeto toma a maior parte do tempo de cada diagnóstico (aviso 1 do cabeçalho), fato do projeto e não "
       "das fontes.", "nenhuma afirmação verificada diz que o prefill domina o custo; é medida do projeto, declarada no cabeçalho."),
    _c(PESOS, "Nesses trabalhos, até o NVMe de ponta é o gargalo, então",
       "Em dois desses trabalhos a E/S pesa mesmo com armazenamento rápido (o SSD-LLaMA usa até 77,7% da banda de um NVMe PCIe 5.0, e no baseline LLMFlash, em celular, "
       "a E/S responde por 77% da latência), então", _GARGALO),
    _c(PESOS, "pois não há evidência verificada a favor e até o NVMe é gargalo",
       "pois não há evidência verificada a favor e, em dois dos trabalhos, a E/S já pesa mesmo com armazenamento rápido", _GARGALO),
    _c(PESOS, "quando só há 7 GB de memória disponível, e a E/S responde por 77% da latência no baseline LLMFlash [parcial]",
       "quando só há 7 GB de memória disponível. Em outro cenário do mesmo artigo (Mistral-7B com 50% dos pesos FFN descarregados), a E/S responde por 77% da latência "
       "no baseline LLMFlash [parcial]", "os 77% são de outro cenário do artigo, não do caso com 7 GB."),
    _c(PESOS, "O relato do llama.cpp é o único próximo da máquina-alvo. Ele só seria útil para trocar o modelo por um MoE maior que a RAM, com teto de cerca de 4 tok/s na "
       "decodificação e sem contar o prefill",
       "O relato comunitário do llama.cpp, num MacBook M1 de 16 GB com o Qwen3-30B-A3B, é o mais próximo da máquina-alvo entre as fontes, embora seja de outra "
       "arquitetura. Ele só seria útil para trocar o modelo por um MoE maior que a RAM; nele a decodificação ficou entre 3,81 e 4,7 tok/s (teto de cômputo de 4,4 tok/s "
       "no benchmark em C), sem contar o prefill", _RELATO_M1),
    _c(PESOS, "usar cerca de 4 tok/s na decodificação como teto otimista e cerca de 0,9 tok/s como referência do carregamento ingênuo, sem contar o prefill",
       "a única referência é um relato comunitário num MacBook M1 com o Qwen3-30B-A3B: de 3,81 a 4,7 tok/s na decodificação lendo só os especialistas ativos e cerca de "
       "0,9 tok/s lendo camadas inteiras, sem contar o prefill; são números de outra arquitetura, não um teto para o i5-1235U", _RELATO_M1),
    _c(PESOS, "O único cenário só com CPU e especialistas no SSD é um relato comunitário, não revisado por pares.",
       "Entre as fontes deste tópico, o único cenário só com CPU e especialistas no SSD é um relato comunitário, não revisado por pares.",
       "o tópico da leitura integral do colibri traz outros cenários só com CPU; a exclusividade vale para as fontes deste tópico."),
    _c(PESOS, "é uma alavanca mais promissora para a máquina-alvo do que descarregar pesos",
       "é uma alavanca a medir na máquina-alvo, por inferência desta síntese (a observação do Fiddler é de Xeons executando especialistas do Mixtral, e nenhuma fonte "
       "compara essa alavanca com a descarga de pesos)", "nenhuma fonte compara as duas alavancas."),
    _c(PESOS, "No prefill, ficam ativos 55,9 de 60 especialistas por camada",
       "No prefill do Qwen1.5-MoE, medido no MMLU, ficam ativos em média 55,9 de 60 especialistas por camada", "condição da medida."),
    _c(PESOS, "Com prompts típicos, todos os especialistas ficam ativos no prefill, mesmo com lote 1",
       "Segundo os autores, em cargas típicas os prompts são longos o bastante para que todos os especialistas fiquem ativos no prefill, mesmo com lote 1",
       "é afirmação dos autores sobre cargas típicas, não medida nos prompts do projeto."),
    _c(PESOS, "Como o qwen2.5:7b usa SwiGLU, essa linha não se aplica ao modelo do projeto.",
       "Como o qwen2.5:7b usa SwiGLU, os métodos dessa linha que dependem de esparsidade de ativação (o \"LLM in a flash\" e o PowerInfer) não se aplicam ao modelo do "
       "projeto; o FlexGen não depende disso e fica de fora por otimizar vazão em lote.", "o FlexGen não depende de ativação ReLU."),
    _c(PESOS, "O trabalho canônico para modelos densos lidos de flash é", "Para modelos densos lidos de flash, o trabalho levantado nesta rodada é",
       "a verificação chama de clássico e canônico o FlexGen; para o \"LLM in a flash\" não há essa qualificação."),
    _c(PESOS, "reduz esse tempo em apenas 5 a 14%", "reduz esse tempo em 5 a 14%", "o \"apenas\" é juízo da síntese."),
    _c(PESOS, "O ganho é de 4 a 5x na CPU e de 20 a 25x na GPU",
       "O ganho declarado pelos autores é de 4 a 5x na CPU e de 20 a 25x na GPU (a razão entre os 2.196 ms e os cerca de 163 ms dá um fator maior; a afirmação "
       "verificada não diz contra que linha de base os autores contam os 4 a 5x)",
       "os dois números da fonte não se conciliam na leitura, e a verificação não resolve a base de comparação."),
]

# ------------------------------------------------------------------ §6.14.1 o repositório colibri por inteiro
_SO_O_OLMOE = "a exclusividade era inferência: pela tabela do README, o DeepSeek V4 Flash cabe no disco livre e pede 16 GB de RAM, que é a instalada."
_GGUF = "nenhuma afirmação verificada trata de GGUF."
_TABELA_DE_MEDICOES = "a afirmação verificada cobre a tabela de medições do repositório, não o repositório inteiro."
_BENCHMARKS_MD = "os valores da tabela de medições vêm do docs/benchmarks.md, que não estava citado na frase."
_AJUSTES = "\"supõem RAM de sobra\" não está na fonte; o que há é a condição das medidas (Strix Halo de 128 GB) e o PIN, que rende com uso repetido."
_CORRECOES_DO_COLIBRI = [
    _c(COLIBRI, "que pede pelo menos 24 a 32 GB de RAM, NVMe rápido e centenas de GB livres",
       "que pede, conforme o modelo, de 16 GB de RAM no mínimo (GLM-5.2, com 24 GB para uso confortável; DeepSeek V4 Flash, de 16 a 32 GB) a 32 GB ou mais (Kimi K3), "
       "além de NVMe rápido e centenas de GB livres; a máquina-alvo tem instalada exatamente a RAM mínima do GLM-5.2 e não tem o espaço livre em disco que ele pede",
       "erro de número: a tabela do README pede 16 GB no mínimo para o GLM-5.2 e para o DeepSeek V4 Flash; 24 a 32 GB vale para uso confortável ou para outros modelos."),
    _c(COLIBRI, "O único modelo que cabe na máquina-alvo, o OLMoE, trocaria o modelo e invalidaria a biblioteca L1.",
       "O único modelo da tabela de requisitos que cabe com folga na máquina-alvo é o OLMoE, e adotá-lo trocaria o modelo e invalidaria a biblioteca L1. O DeepSeek V4 "
       "Flash (cerca de 167 GB, de 16 a 32 GB de RAM) cabe no disco livre e fica no mínimo de RAM, sem medida publicada numa máquina de 16 GB.", _SO_O_OLMOE),
    _c(COLIBRI, "O único modelo do colibri que cabe na máquina-alvo é o OLMoE-1B-7B int8, mas nele o modelo fica inteiro na RAM",
       "O único modelo da tabela do colibri que cabe com folga na máquina-alvo é o OLMoE-1B-7B int8 (o DeepSeek V4 Flash cabe no disco livre e fica no mínimo de RAM, de "
       "16 a 32 GB); no OLMoE, porém, o modelo fica inteiro na RAM", _SO_O_OLMOE),
    _c(COLIBRI, "O único caso medido com 16 GB e só CPU é um Apple M3 base.", "O caso medido com 16 GB e só CPU que a verificação encontrou é um Apple M3 base.",
       "\"único\" não está na afirmação verificada."),
    _c(COLIBRI, "O colibri não lê GGUF e não fornece logprobs nem seed pela API.",
       "O colibri usa formatos de pesos próprios (se ele lê GGUF não foi verificado nas fontes), rejeita logprobs nas rotas comuns da API, embora a rota /v1/brio devolva "
       "a probabilidade de cada opção, e aceita seed sem efeito.",
       _GGUF + " A API tem a rota /v1/brio, que devolve a probabilidade de cada opção."),
    _c(COLIBRI, "Os formatos próprios do colibri impedem reaproveitar os GGUF do Ollama",
       "Os formatos de pesos do colibri são próprios; se os GGUF do Ollama podem ser reaproveitados não foi verificado nas fontes", _GGUF),
    _c(COLIBRI, "O agente não consegue usar o Brio pela API do colibri, que rejeita logprobs e ignora seed. Uma eventual pontuação de opções teria de ser implementada sobre "
       "outro motor que exponha logprobs, e essa viabilidade precisa ser verificada no Ollama 0.34.4",
       "O Brio existe na API do colibri como rota própria (/v1/brio), que devolve a probabilidade de cada opção; as rotas comuns rejeitam logprobs e ignoram seed, e "
       "usá-lo pediria trocar o motor do agente. Uma pontuação de opções no motor atual depende de logprobs no Ollama 0.34.4, disponibilidade que a sonda do projeto "
       "confirmou em 01/10/2026 (aviso 3 do cabeçalho)",
       "a API expõe a rota /v1/brio; e a disponibilidade de logprobs no Ollama foi verificada depois de a síntese ser escrita."),
    _c(COLIBRI, "Não foi verificado se o Ollama 0.34.4 expõe logprobs pelo endpoint /api/generate, o que é condição para aplicar a ideia do Brio no agente local.",
       "Quando esta síntese foi escrita, não estava verificado se o Ollama 0.34.4 expõe logprobs pelo endpoint /api/generate, condição para aplicar a ideia do Brio no "
       "agente local; a sonda do projeto verificou em 01/10/2026 que expõe (aviso 3 do cabeçalho).", "o estado mudou depois da escrita."),
    _c(COLIBRI, "As outras máquinas com pouca RAM ficam no mesmo patamar.",
       "As outras máquinas de 24 a 32 GB ficam, a frio, na mesma ordem de grandeza; a quente, uma delas chegou a cerca de 0,5 tok/s, e a máquina de RAM não informada "
       "(Core Ultra 9 285K) ficou entre 0,26 e 0,42 tok/s.",
       "os valores a quente e os da máquina de RAM não informada são maiores; \"mesmo patamar\" só vale a frio."),
    _c(COLIBRI, "os dados Intel com Windows nativo são de máquinas com 24 a 32 GB",
       "os dados Intel são de máquinas com 24 a 32 GB ou, no caso do Core Ultra 9 285K, de RAM não informada", "a fonte não informa a RAM do Core Ultra 9 285K."),
    _c(COLIBRI, "O Brio foi medido com 2 a 4 opções e um prefixo curto.",
       "O Brio foi medido com uma pergunta de 3 opções, um JSON de 4 campos e uma medida por item; o tamanho do prefixo não é informado.",
       "a fonte informa só esses três casos, sem o tamanho do prefixo."),
    _c(COLIBRI, "Não há método publicado para visualizar competências de modelos densos: o expert atlas depende, por construção, do roteador MoE.",
       "O documento do expert atlas não trata de modelos densos, e o atlas depende, por construção, do roteador MoE; os métodos publicados para modelos densos (sondas, "
       "autoencoders esparsos, grafos de atribuição) estão no tópico do atlas e da especialização.",
       "a afirmação verificada diz só que o documento não trata de modelos densos; métodos para eles existem e estão em outro tópico."),
    _c(COLIBRI, "a medição mais próxima (i5-12600K, 32 GB, Windows 11 nativo, MinGW) deu 0,08 tok/s",
       "a medição mais próxima (GLM-5.2 int4 a frio num i5-12600K com 32 GB, Windows 11 nativo, MinGW) deu 0,08 tok/s", "faltavam o modelo e a condição a frio."),
    _c(COLIBRI, "O aquecimento em leitura contínua também pesa num notebook com NVMe sem dissipador",
       "O aquecimento em horas de leitura contínua, que o repositório aponta sem medir, também pode pesar no NVMe de um notebook (se o desta máquina tem dissipador não "
       "foi verificado)", "o risco é qualitativo na fonte, e o dissipador do NVMe desta máquina não foi verificado."),
    _c(COLIBRI, "Não há nenhuma medição com HD mecânico. Que o esquema", "Na tabela de medições do repositório não há nenhuma linha com HD mecânico. Que o esquema",
       _TABELA_DE_MEDICOES),
    _c(COLIBRI, "Não há nenhuma medição do colibri com HD mecânico:", "A tabela de medições do colibri não tem nenhuma linha com HD mecânico:", _TABELA_DE_MEDICOES),
    _c(COLIBRI, "o repositório não tem nenhuma linha com HD", "a tabela de medições do repositório não tem nenhuma linha com HD", _TABELA_DE_MEDICOES),
    _c(COLIBRI, "Não há comparação numérica entre o histórico de roteamento e o LRU",
       "O documento de telemetria de roteamento não traz comparação numérica entre o histórico de roteamento e o LRU",
       "a verificação cobre o documento de telemetria, não o repositório inteiro."),
    _c(COLIBRI, "Nenhuma das seis hipóteses abertas do colibri trata de máquinas de 16 GB só com CPU nem de modelos densos. Adotá-lo seria pesquisa de infraestrutura fora "
       "do escopo do TCC",
       "Das seis hipóteses abertas do colibri, só a do planejamento automático pelo hardware cita notebooks, sem falar de 16 GB só com CPU, e nenhuma trata de modelos "
       "densos. Adotá-lo seria, na leitura desta síntese, pesquisa de infraestrutura fora do escopo do TCC", "a terceira hipótese cita notebooks."),
    _c(COLIBRI, "e emite aviso, mas esconde 38% dos especialistas distintos.",
       "e emite aviso de perda. O README do atlas mede, sem informar o limiar, que o corte top-p esconde 38% dos especialistas distintos (JUSTVUGG et al., 2026g).",
       "os 38% são do README do atlas, sem limiar informado, e a citação certa é a 2026g."),
    _c(COLIBRI, "[parcial] (BOPOF, 2026). A 0,08 tok/s", "[parcial] (BOPOF, 2026; a tabela de medições é JUSTVUGG et al., 2026b). A 0,08 tok/s", _BENCHMARKS_MD),
    _c(COLIBRI, "chegou a 16,3 e 19,1 tok/s [parcial] (GOURAVKARGWAL, 2026).",
       "chegou a 16,3 e 19,1 tok/s [parcial] (GOURAVKARGWAL, 2026; os valores de 3,69 e 4,18 tok/s são da tabela de medições, JUSTVUGG et al., 2026b).", _BENCHMARKS_MD),
    _c(COLIBRI, "Sua release mais recente é a v1.12.1, de 24/09/2026", "A release mais recente na data da consulta (01/10/2026) é a v1.12.1, de 24/09/2026",
       "\"mais recente\" só vale na data da consulta."),
    _c(COLIBRI, "0,30 tok/s a quente na CPU e 0,42 tok/s com GPU e auto-pin",
       "0,30 tok/s a quente na CPU, com a decodificação especulativa MTP ligada (2,2 a 2,3 tokens por passada), e 0,42 tok/s com GPU e auto-pin",
       "o valor a quente é com MTP."),
    _c(COLIBRI, "Num Ryzen 9 9950X, trocar um NVMe", "Num Ryzen 9 9950X com 123 GB de RAM, trocar um NVMe", "condição da medida: RAM muito acima da máquina-alvo."),
    _c(COLIBRI, "Num Threadripper PRO 7965WX, dois NVMe independentes", "Num Threadripper PRO 7965WX com 123 GB de RAM e DIRECT=1, dois NVMe independentes",
       "condição da medida: RAM muito acima da máquina-alvo e leitura com O_DIRECT."),
    _c(COLIBRI, "Pelo mesmo motivo, o NUCLEUS padrão é 0,90", "Por um motivo vizinho, o ruído da cauda da distribuição em int4, o NUCLEUS padrão é 0,90",
       "a fonte dá motivos diferentes: laços sem fim para o gs64, cauda ruidosa do int4 para o NUCLEUS."),
    _c(COLIBRI, "Os ajustes finos supõem RAM de sobra. O DIRECT=1 ganhou 65% num Strix Halo, mas",
       "Os ajustes finos foram medidos em máquinas com muita RAM. O DIRECT=1 ganhou 65% num Strix Halo de 128 GB, mas", _AJUSTES),
    _c(COLIBRI, "Os ajustes DIRECT, PIN e RAM_GB supõem RAM de sobra e uso repetido. Com cerca de 7 GB livres, 88% dariam",
       "Os ajustes DIRECT, PIN e RAM_GB foram medidos em máquinas com muita RAM, e o PIN rende com uso repetido. Pela conta desta síntese, com cerca de 7 GB livres, os "
       "88% que o RAM_GB usa por padrão dariam", _AJUSTES),
    _c(COLIBRI, "correção pela taxa de base e replicação deixando um de fora", "correção pela taxa de base, exigência de replicação e validação deixando um prompt de fora",
       "são dois passos distintos no método do atlas."),
]

# ------------------------------------------------------------------ §6.14.13 mapa da parte A
_RAM_NO_MAPA = "o mínimo de 16 GB se compara com a RAM instalada, que nesta máquina é igual a ele, não com a RAM livre (aviso sobre a memória, no cabeçalho)."
_TETO_DE_RAM = "o que a fonte sustenta é o teto de RAM naquela máquina de 32 GB; nesta, o disco barra antes e a RAM instalada é a mínima declarada."
_CORRECOES_DO_MAPA = [
    _c(MAPA, "Os MoEs pequenos que cabem (granite4:tiny-h, OLMoE, LFM2) são candidatos a experimento depois da Fase 4, com cronometragem própria, por dois motivos: em CPU "
       "o ganho não acompanha a razão de parâmetros ativos, e o prefill de cerca de 1.300 tokens ativa quase todos os especialistas.",
       "Dos MoEs pequenos que cabem, só o granite4:tiny-h fica como candidato a experimento depois da Fase 4, que é a linha adiada do mapa; o OLMoE e o LFM2-8B-A1B "
       "estão descartados nas linhas próprias. Qualquer experimento pede cronometragem própria, por dois motivos: em CPU o ganho medido não acompanhou a razão de "
       "parâmetros ativos, e as fontes indicam que o prefill de cerca de 1.300 tokens ativa quase todos os especialistas (medido no Qwen1.5-MoE; para outros modelos "
       "é afirmação dos autores sobre cargas típicas).",
       "a leitura contradizia as linhas do mapa, que descartam o OLMoE e o LFM2; e a ativação de quase todos os especialistas no prefill foi medida num modelo só."),
    _c(MAPA, "mudam a saída e foram medidas em GPU.",
       "mudam a saída e foram medidas, na maior parte, em GPU (o roteamento ciente de cache foi medido em celulares, e o top-p do colibri, em CPU).",
       "nem tudo foi medido em GPU."),
    _c(MAPA, "Tudo foi medido em GPU e pressupõe um MoE",
       "As medidas com hardware informado são de GPU (o artigo que mede a fusão em código não detalha o hardware) e todas pressupõem um MoE",
       "o artigo do REAP não detalha o hardware."),
    _c(MAPA, "mas foi medida em MoEs de 30B a 671B em clusters de GPU",
       "mas o EASY-EP foi medido num MoE de 671B em nós de 8 GPUs, e o REAP, em MoEs de 20B a 1T, sem hardware detalhado", "condições das duas fontes."),
    _c(MAPA, "A leitura de pesos quase não escreve no disco: no estudo de descarga, 2,0 GiB/s de leitura contra 11,0 MiB/s de escrita.",
       "No estudo de descarga, a descarga de pesos é essencialmente carga de leitura; os 2,0 GiB/s de leitura contra 11,0 MiB/s de escrita são da descarga do cache KV, "
       "não dos pesos.", "os números são da descarga do cache KV, não dos pesos."),
    _c(MAPA, "sem contar o prefill de cerca de 1.300 tokens, que ativa quase todos os especialistas (55,9 de 60 por camada)",
       "sem contar o prefill de cerca de 1.300 tokens; em outro MoE, o Qwen1.5-MoE medido no MMLU, o prefill ativou em média 55,9 dos 60 especialistas de cada camada",
       "o número é do Qwen1.5-MoE (60 especialistas), não do modelo de 30B do relato (128 especialistas)."),
    _c(MAPA, "O carregamento ingênuo de metade de um 7B a partir do SSD custou 2.196 ms por token.",
       "O carregamento ingênuo do OPT-6.7B com cerca de metade do modelo na DRAM, num Apple M1 Max, custou 2.196 ms por token.", "condições da medida."),
    _c(MAPA, "Ler pesos do SSD só reproduziria o regime ingênuo de cerca de 0,46 tok/s medido para um 7B.",
       "A medida disponível de carregamento ingênuo do SSD, de cerca de 0,46 tok/s, é do OPT-6.7B num Apple M1 Max com cerca de metade do modelo na DRAM.", _INGENUO),
    _c(MAPA, "Exigiria trocar o Ollama pelo llama.cpp e levaria a escritas de troca no SSD.",
       "Pelos relatos de versões antigas do Ollama, poderia exigir trocá-lo pelo llama.cpp, e a paginação levaria, por hipótese, a escritas de troca no SSD.",
       "a recusa do Ollama vem de relatos antigos, não verificados na 0.34.4, e as escritas de troca são hipótese."),
    _c(MAPA, "O Ollama recusa ou derruba modelos maiores que a memória disponível mesmo com mmap.",
       "Há relatos, em versões antigas do Ollama, de recusa ou queda com modelos maiores que a memória disponível mesmo com mmap; o comportamento na 0.34.4 não foi verificado.",
       _RECUSA_DO_OLLAMA),
    _c(MAPA, "(81,38 contra 74,16), mas ocupa 19 GB.", "(81,38 contra 74,16, medidos nos modelos base em BF16, sem quantização), mas ocupa 19 GB em Q4_K_M.",
       "condição da medida: modelos base, sem quantização."),
    _c(MAPA, "o top-p 0,7 esconde 38% dos especialistas; o SERE perde 1,9 p.p. e só ganha com lote e QPS de 16 a 24",
       "o corte top-p esconde 38% dos especialistas distintos, em medida do README do atlas que não informa o limiar; o SERE perde 1,9 p.p. e foi medido com decodificação "
       "em lote e QPS de 16 a 24, condições de que o ganho depende",
       "os 38% não têm limiar informado; o SERE foi medido nessas condições, e a fonte não diz que só há ganho com lote grande."),
    _c(MAPA, "O Ollama, porém, não expõe estados ocultos, e o qwen2.5:7b", "Não foi verificado, porém, se o Ollama permite extrair estados ocultos, e o qwen2.5:7b",
       "a lacuna da síntese do atlas diz que isso não foi verificado."),
    _c(MAPA, "já que prompts em português passam por um espaço próximo do inglês",
       "já que, no Llama-2 com prompts não ingleses, as camadas do meio decodificam o token correto com probabilidade maior em inglês, o que pode valer também para "
       "prompts em português", "o resultado é do Llama-2; para português e para o Qwen2.5 é extrapolação."),
    _c(MAPA, "Treinar SAEs custa mais de 20% do compute de treino do GPT-3 e cerca de 20 PiB de ativações. Os SAEs do FAST operam em precisão cheia, não sobre o GGUF, e o "
       "circuit-tracer não tem transcoders para Qwen2.5 e pressupõe GPU.",
       "O conjunto inteiro do Gemma Scope (mais de 400 SAEs, para três modelos) custou mais de 20% do compute de treino do GPT-3 e cerca de 20 PiB de ativações; o custo "
       "de um SAE isolado não está nas fontes. Para os SAEs do FAST, a fonte não diz se valem para o GGUF quantizado. O circuit-tracer não tem transcoders para Qwen2.5, "
       "e o README dele trata a GPU como caso normal, sem documentar execução só em CPU.",
       "o custo verificado é do conjunto inteiro; precisão e GGUF não foram verificados para o FAST; e \"pressupõe GPU\" é mais forte que o README."),
    _c(MAPA, "e os grafos de atribuição explicam satisfatoriamente só cerca de um quarto dos prompts",
       "e os grafos de atribuição, segundo os próprios autores, dão compreensão satisfatória em cerca de um quarto dos prompts testados no Claude 3.5 Haiku", _UM_QUARTO),
    _c(MAPA, "Cada token frio exige cerca de 11 GB de leituras aleatórias, que é justamente o padrão",
       "No GLM-5.2, cada token frio exige cerca de 11 GB de leituras aleatórias, que é justamente o padrão", "o número é do GLM-5.2."),
    _c(MAPA, "e a energia por token chega a cerca de 12 vezes a da memória rápida",
       "e, num estudo de modelagem com o DeepSeek-R1, a energia por token chega a até cerca de 12 vezes a de manter tudo em HBM, memória de servidor",
       "condições da fonte: modelagem, DeepSeek-R1, comparação com HBM."),
    _c(MAPA, "Aquecimento do NVMe de notebook, sem dissipador, em horas de leitura contínua",
       "Aquecimento do NVMe de notebook em horas de leitura contínua (risco que o repositório aponta sem medir; se o desta máquina tem dissipador não foi verificado)",
       "o risco é qualitativo na fonte, e o dissipador do NVMe desta máquina não foi verificado."),
    _c(MAPA, "Operar com a memória no limite derruba o desempenho de forma abrupta: o PowerInfer-2 caiu de 11,68 para 2,13 tok/s com 7 GB disponíveis, o mesmo orçamento "
       "livre da máquina-alvo.",
       "Operar com a memória no limite pode derrubar o desempenho: num celular OnePlus 12 (NPU e CPU, modelo esparsificado de 47B), o PowerInfer-2 caiu de 11,68 para "
       "2,13 tok/s com 7 GB disponíveis, orçamento parecido com o livre da máquina-alvo, em outro hardware e com outro modelo.",
       "condições da medida: celular com NPU e modelo esparsificado de 47B."),
    _c(MAPA, "e tratar os números publicados como teto, não como previsão", "e tratar os números publicados como referência de outro hardware, não como previsão",
       "nenhuma fonte sustenta que os valores sejam um teto para o i5-1235U."),
    _c(MAPA, "A cabeça MTP em int4 zerou a aceitação de rascunhos.", "No GLM-5.2, a cabeça MTP em int4 zerou a aceitação de rascunhos.", "o número é do GLM-5.2."),
    _c(MAPA, "Os formatos do colibri também impedem reaproveitar os GGUF do Ollama, então",
       "Os formatos de pesos do colibri são próprios (se ele lê GGUF não foi verificado), então", _GGUF),
    _c(MAPA, "e o prompt de cerca de 1.300 tokens pesa mais que os 61 tokens de saída",
       "e, nos registros da Fase 3 do projeto, o prefill do prompt de cerca de 1.300 tokens toma mais tempo que a geração dos 61 tokens de saída (aviso 1 do cabeçalho)",
       "fato do projeto, com a medida no cabeçalho, não das fontes."),
    _c(MAPA, "Num M3 de 16 GB rodou a 3,69 a 4,18 tok/s, limitado por RAM e CPU.",
       "Num M3 de 16 GB rodou a 3,69 tok/s a frio e a 4,18 tok/s a quente, este limitado por RAM e CPU, não pelo disco.",
       "a limitação por RAM e CPU vale para a corrida a quente."),
    _c(MAPA, "Esses ajustes supõem RAM de sobra e uso repetido.", "Esses ajustes foram medidos em máquinas com muita RAM, e o PIN rende com uso repetido.", _AJUSTES),
    _c(MAPA, "Não cabe. O guia pede cerca de 400 GB livres em NVMe e a máquina tem 218 GB. A RAM livre, de cerca de 7 GB, fica abaixo do mínimo de 16 GB.",
       "Não cabe no disco. O guia pede cerca de 400 GB livres em NVMe e a máquina tem 218 GB. Na RAM, a máquina tem instalado exatamente o mínimo que o repositório "
       "declara (16 GB), com cerca de 7 GB livres no início de uma corrida.", _RAM_NO_MAPA),
    _c(MAPA, "e a máquina tem 15,69 GB no total", "e a máquina tem menos que isso instalado",
       "15,69 GB é o que o Windows enxerga; o total instalado está no aviso sobre a memória, no cabeçalho."),
    _c(MAPA, "Nesta máquina a restrição que manda é a RAM, não o disco.",
       "Na medição de 0,08 tok/s, o próprio autor aponta o teto de RAM, e não o disco, como a restrição decisiva, com 32 GB; nesta máquina o GLM-5.2 nem cabe no disco "
       "livre, e a RAM instalada é a mínima declarada.", _TETO_DE_RAM),
    _c(MAPA, "O SATA só pioraria um cenário que já é inviável pela RAM.",
       "O SATA só pioraria um cenário que já é inviável nesta máquina pelo espaço em disco e pela RAM no mínimo declarado.", _TETO_DE_RAM),
    _c(MAPA, "O GLM-5.2 do atlas não cabe, e o único MoE que cabe é o OLMoE, no limite dos cerca de 7 GB livres e sem relação com o modelo decidido. Exigiria instalar ou "
       "compilar um binário que o Smart App Control bloqueia.",
       "O GLM-5.2 do atlas não cabe no disco livre, e o único MoE da tabela do colibri que cabe com folga na RAM instalada é o OLMoE, cujo contêiner int8 de 6,9 GB fica no "
       "limite dos cerca de 7 GB livres no início de uma corrida, sem relação com o modelo decidido. Exigiria instalar o binário publicado ou compilar um (o Smart App "
       "Control bloqueia binários compilados localmente; se bloqueia o publicado não foi verificado).",
       "o Smart App Control bloqueia binários compilados localmente; as releases trazem binários prontos, cujo bloqueio não foi verificado."),
    _c(MAPA, "Nesta máquina nenhuma das duas se cumpre. O GLM-5.2 nem cabe nos 218 GB livres, e a RAM livre fica abaixo do mínimo de 16 GB.",
       "Nesta máquina a primeira esbarra no disco e a segunda não se cumpre: o GLM-5.2 nem cabe nos 218 GB livres, e a RAM instalada é exatamente o mínimo que o "
       "repositório declara, sem sobra.", _RAM_NO_MAPA),
    _c(MAPA, "Um segundo SSD ou ajustes finos não mudam a ordem de grandeza, porque o limite é a RAM.",
       "Um segundo SSD ou ajustes finos não mudariam a ordem de grandeza: na medição mais próxima, o próprio autor aponta o teto de RAM, e não o disco, como a restrição.",
       _TETO_DE_RAM),
    _c(MAPA, "Não se sabe se o Ollama 0.34.4 expõe logprobs e reaproveitamento de prefixo suficientes para uma escolha fechada como a do Brio.",
       "Quando o mapa foi escrito não se sabia se o Ollama 0.34.4 expõe logprobs (a sonda do projeto confirmou em 01/10/2026 que expõe, aviso 3 do cabeçalho); o "
       "reaproveitamento de prefixo para uma escolha fechada como a do Brio continua sem verificação.", "o estado mudou depois da escrita."),
    _c(MAPA, "Quanto ao expert atlas, a literatura mostra que ele é um histograma", "Quanto ao expert atlas, a documentação do próprio colibri mostra que ele é um histograma",
       "a descrição do atlas vem do README do repositório, não da literatura."),
    _c(MAPA, "o roteamento segue geometria, sintaxe e identidade do token, e SAEs empatam com baselines aleatórios.",
       "em parte dos modelos medidos o roteamento segue geometria, sintaxe e identidade do token (o OLMoE mostra especialização por domínio), e SAEs empataram com "
       "baselines aleatórios num preprint.", "o OLMoE mostra especialização por domínio; o empate dos SAEs é de um preprint."),
    _c(MAPA, "Sondas lineares e SAEs exigiriam outra pilha e mais memória.",
       "Sondas lineares e SAEs pediriam extrair ativações do modelo, o que não foi verificado na pilha atual, e mais memória.",
       "se a pilha atual permite extrair ativações não foi verificado."),
    _c(MAPA, "Ambos cabem. O OLMoE, porém,", "O arquivo do OLMoE cabe, e o tamanho do LFM2-8B-A1B não foi verificado. O OLMoE, porém,",
       "o tamanho do LFM2-8B-A1B não foi verificado."),
    _c(MAPA, "O teto otimista de cerca de 4 tok/s não inclui o prefill dos prompts do TCC.",
       "Esses números não incluem o prefill dos prompts do TCC e são de outra arquitetura, não um teto para o i5-1235U.", _RELATO_M1),
    _c(MAPA, "Dependem de GPU dedicada, AMX ou AVX-512 e centenas de GB de RAM, e o i5-1235U",
       "Foram medidos com GPU dedicada (e, no caso do KTransformers, com Xeon com AMX e centenas de GB de RAM), e o i5-1235U", _HARDWARE_DA_MEDIDA),
]

CORRECOES_DA_REVISAO: list[dict] = (_CORRECOES_DO_COLIBRI + _CORRECOES_DA_BASE + _CORRECOES_DOS_PESOS + _CORRECOES_DOS_MOE + _CORRECOES_DO_ATLAS
                                    + _CORRECOES_DO_MAPA)
