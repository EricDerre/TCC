<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre a árvore de decisão legível para o analista, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# Base C: árvore de decisão legível para o analista (levantamento de 7 nov. 2026)

Legenda de confiança: "aberta" = página aberta e lida nesta sessão; "snippet" = só resumo de busca; "memória" = dado bibliográfico que não consegui abrir.

## a) Explicações contrastivas e "por que não"

**1. MILLER, Tim. Explanation in artificial intelligence: insights from the social sciences. Artificial Intelligence, v. 267, p. 1-38, 2019. Preprint: arXiv:1706.07269. Disponível em: https://arxiv.org/abs/1706.07269. Acesso em: 7 nov. 2026.**
- Estabelece (página do arXiv, aberta): a explicação em IA deve se apoiar em filosofia, psicologia e ciência cognitiva sobre como pessoas definem, selecionam, avaliam e apresentam explicações; pessoas trazem vieses e expectativas sociais, e boa parte da IA explicável usa só a intuição dos pesquisadores.
- Atenção: o resumo não cita "contrastiva" nem "por que não". Que as pessoas pedem explicações contrastivas ("por que P e não Q") vem do corpo do artigo, que não consegui abrir (403 no editor). Volume e páginas vêm da memória.
- No ponto: justifica que cada nó mostre a escolhida contra as alternativas descartadas, em vez de só "porque a causa é X".

**2. LIM, Brian Y.; DEY, Anind K. Assessing demand for intelligibility in context-aware applications. In: INTERNATIONAL CONFERENCE ON UBIQUITOUS COMPUTING (UbiComp), 11., 2009. Anais [...]. ACM, 2009. p. 195-204. Disponível em: https://dblp.uni-trier.de/rec/conf/huc/LimD09.html. Acesso em: 7 nov. 2026.**
- Estabelece (snippet de busca, não abri o texto): com cenários de quatro aplicações reais, dois experimentos medem que informação os usuários querem de sistemas opacos, e discutem por que pedem certos tipos e como oferecê-los. O resumo não diz qual tipo foi mais pedido.
- Fonte complementar, só bibliográfica (página aberta): LIM, B. Y.; DEY, A. K.; AVRAHAMI, D. Why and why not explanations improve the intelligibility of context-aware intelligent systems. In: CHI, 27., 2009. Proceedings [...]. ACM, 2009. p. 2119-2128. DOI 10.1145/1518701.1519023. Disponível em: https://bibtex.github.io/CHI-2009-LimDA.html. Acesso em: 7 nov. 2026. Pelo título, é o estudo que testa as explicações "por que" e "por que não"; não li o resumo.
- No ponto: sustenta oferecer "por que" e "por que não" como tipos de pergunta do analista, sem exibir o interior do sistema inteiro.

## b) Fidelidade do raciocínio em texto

**3. TURPIN, Miles; MICHAEL, Julian; PEREZ, Ethan; BOWMAN, Samuel R. Language models don't always say what they think: unfaithful explanations in chain-of-thought prompting. In: NEURAL INFORMATION PROCESSING SYSTEMS (NeurIPS), 37., 2023. Disponível em: https://arxiv.org/abs/2305.04388. Acesso em: 7 nov. 2026.**
- Estabelece (aberta): a explicação em cadeia de pensamento pode deturpar sistematicamente a razão real da previsão. Ao inserir um viés (por exemplo, reordenar opções para a resposta ser sempre "A"), a resposta muda e o texto não menciona isso; o texto racionaliza a resposta errada, com queda de até 36% de acurácia em 13 tarefas (GPT-3.5 e Claude 1.0).
- No ponto: o raciocínio aberto do modelo não pode ser a justificativa de um nó.

**4. LANHAM, Tamera et al. Measuring faithfulness in chain-of-thought reasoning. Anthropic, 2023. arXiv:2307.13702. Disponível em: https://arxiv.org/abs/2307.13702. Acesso em: 7 nov. 2026.**
- Estabelece (aberta): a fidelidade varia por tarefa e tamanho do modelo; segundo o resumo, modelos maiores e mais capazes produzem raciocínio menos fiel na maioria das tarefas estudadas.
- No ponto: trocar de modelo ou de tamanho pode mudar o quanto o texto reflete o que ocorreu, mais um motivo para ancorar a árvore em sinais conferidos por código.

## c) Visualização de trilhas de agentes

**5. LANGCHAIN. LangSmith: observability concepts. Disponível em: https://docs.langchain.com/langsmith/observability-concepts. Acesso em: 7 nov. 2026.**
- Mostra (aberta): um "run" é uma unidade de trabalho (chamada de modelo, ferramenta, busca), equivalente a um span do OpenTelemetry; um "trace" é a árvore de runs de uma operação, com entradas e saídas completas e aninhamento preservado. Latência, tokens e custo: a página não confirma.

**6. LANGFUSE. Data model. Disponível em: https://langfuse.com/docs/observability/data-model. Acesso em: 7 nov. 2026.**
- Mostra (aberta): trace é uma operação; observações (span, generation, event) são os passos individuais e podem ser aninhadas. Campos de entrada, saída, custo e latência não aparecem nessa página.
- Complemento (aberta): https://langfuse.com/docs/observability/features/agent-graphs descreve as abas Árvore, Linha do tempo e Grafo, com o grafo inferido de tempos e aninhamento (Acesso em: 7 nov. 2026).

**7. OPENTELEMETRY. Semantic conventions for generative AI. Disponível em: https://github.com/open-telemetry/semantic-conventions-genai. Acesso em: 7 nov. 2026.**
- Mostra (aberta): as convenções migraram para esse repositório e cobrem spans, métricas e eventos de clientes GenAI e MCP. As páginas antigas em opentelemetry.io/docs/specs/semconv/gen-ai/ só apontam para lá. Os nomes de span de agente (invoke_agent, execute_tool) não consegui confirmar abrindo páginas.
- No ponto (5 a 7): essas ferramentas servem ao desenvolvedor (árvore de chamadas, entradas, saídas), não ao analista de QA. Confirmam que o modelo de dados passo a passo da trilha é o padrão, mas a árvore de decisão exige uma camada própria de leitura.

## d) Orientação para não especialistas

**8. AMERSHI, Saleema et al. Guidelines for human-AI interaction. In: CHI CONFERENCE ON HUMAN FACTORS IN COMPUTING SYSTEMS, 2019. Anais [...]. ACM, 2019. Disponível em: https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/. Acesso em: 7 nov. 2026.**
- Estabelece (página aberta): 18 diretrizes, validadas com 49 profissionais de design em 20 produtos; prêmio de menção honrosa no CHI 2019. O texto das diretrizes veio da biblioteca HAX (https://www.microsoft.com/en-us/haxtoolkit/library/, aberta): G1 "Make clear what the system can do"; G2 "Make clear how well the system can do what it can do" (ajudar a entender com que frequência pode errar); G11 "Make clear why the system did what it did" (acesso a uma explicação do comportamento).
- No ponto: G11 pede a explicação, G2 pede dizer a confiabilidade em linguagem comum (por exemplo, "esse tipo de diagnóstico costuma acertar X de 10"), sem jargão.

## O que isso fixa para o desenho

Cada nó mostra: a pergunta do passo em linguagem do sistema (o que estava sendo decidido); a alternativa escolhida e as descartadas, cada uma com o motivo de "por que não" (fonte 1 e 2); a evidência concreta citada (campo, trecho de resposta, verbete) em termos do sistema do analista; e uma confiança em palavras ("alta", "média", "baixa") com a taxa histórica de acerto dessa faixa em frases comuns, sem k, logprob nem hit@3 (fonte 8, G2). O analista deve poder abrir a evidência e conferi-la sozinho.

Deve ser declarado como vindo de código: a poda, a busca dos verbetes, as alternativas e suas probabilidades, a conferência das evidências e a divergência entre o dito e o conferido, além do texto de justificativa, montado por molde a partir de sinais conferidos. Deve ser declarado como vindo do modelo: apenas a escolha do rótulo e o que ele citou. O raciocínio aberto, se for exibido, fica separado, rotulado como "texto do modelo, sem garantia de refletir o que ele fez" (fontes 3 e 4). Quando houver divergência entre o que o modelo disse e o que o código conferiu, o nó mostra isso de forma explícita, em vez de esconder.

## O que não achei

Não abri o corpo de Miller (2019) nem o texto de Lim e Dey (2009), então o achado contrastivo e o ranking dos tipos de pergunta ("por que", "por que não") não foram conferidos por mim em página; o DOI do UbiComp 2009 não foi confirmado. Não confirmei custo e latência nas páginas de LangSmith e Langfuse, nem os nomes de span de agente do OpenTelemetry. Não encontrei fonte oficial dessas ferramentas voltada a usuários não técnicos. Também não achei estudo específico sobre árvores de decisão geradas por molde a partir de logs de agente de QA.
