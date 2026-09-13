**Universidade Cidade de São Paulo \- UNICID**  
**Curso de Ciência da Computação**

ERIC CONDE DERRE  
ERICK DO CARMO ESTEVES  
FERNANDO MATOS DE SOUZA  
GUILHERME PENHA DOS SANTOS  
JOÃO VICTOR FONSECA SILVA  
KENNEDY FERNANDO DE OLIVEIRA GUNDIM  
LEANDRO HENRIQUE DA SILVA PATRICIO  
PEDRO HENRIQUE TORRES GONÇALVES  
RAUL SILVESTRE MARINHO

**DESENVOLVIMENTO DE UM AGENTE DE QA END-TO-END (E2E) AUTÔNOMO COM CAPACIDADES DE SELF-HEALING:**  
Focado na Fronteira de Integração

São Paulo  
2026  
ERIC CONDE DERRE  
ERICK DO CARMO ESTEVES  
FERNANDO MATOS DE SOUZA  
GUILHERME PENHA DOS SANTOS  
JOÃO VICTOR FONSECA SILVA  
KENNEDY FERNANDO DE OLIVEIRA GUNDIM  
LEANDRO HENRIQUE DA SILVA PATRICIO  
PEDRO HENRIQUE TORRES GONÇALVES  
RAUL SILVESTRE MARINHO

**DESENVOLVIMENTO DE UM AGENTE DE QA END-TO-END (E2E) AUTÔNOMO COM CAPACIDADES DE SELF-HEALING:**  
Focado na Fronteira de Integração

|  | Projeto de pesquisa apresentado ao curso de Ciência da Computação da Universidade Cidade de São Paulo (UNICID), como requisito parcial para a elaboração do Trabalho de Conclusão de Curso. |
| :---- | :---- |

São Paulo  
2026

# **SUMÁRIO**

**1 INTRODUÇÃO**  
1.1 Contextualização e Delimitação do Tema  
1.2 Problema de Pesquisa  
1.3 Justificativa  
1.4 Objetivos  
**2 REFERENCIAL TEÓRICO**  
2.1 Evolução da Automação E2E e o Conceito de Self-Healing  
2.2 Fundamentos de Aprendizado de Máquina e Adaptação  
2.3 Automação E2E e Inteligência Artificial  
2.4 Gestão de Context Window em LLMs  
2.5 Detecção de Quebra de Contrato de API  
2.6 Recuperação de Conhecimento Prévio Aplicada à Localização de Falhas  
**3 METODOLOGIA**  
3.1 Infraestrutura e Orquestração Local  
3.2 Inteligência Artificial e Processamento LLM  
3.3 Comunicação e Mitigação de Gargalos  
3.4 Validação e Avaliação  
**4 RESULTADOS ESPERADOS**  
**5 CRONOGRAMA DE ATIVIDADES**  
**REFERÊNCIAS**  
**GLOSSÁRIO**

# **1 INTRODUÇÃO**

## **1.1 Contextualização e Delimitação do Tema**

A automação de testes End-to-End (E2E) tradicional enfrenta um alto custo de manutenção devido à fragilidade crônica de seus scripts. Uma alteração simples no CSS do Frontend ou a mudança invisível do tipo de um dado retornado por uma API, fenômeno conhecido como *Contract Drift* (Deriva de Contrato), quebra instantaneamente a esteira de CI/CD (Integração Contínua/Entrega Contínua), gerando perda de tempo em triagens manuais exaustivas.  
Embora a automação moderna baseada em Inteligência Artificial ofereça avanços, a literatura e a prática industrial demonstram que a IA não tem o intuito de substituir os engenheiros de qualidade (QA) ou os desenvolvedores, mas sim assumir as tarefas repetitivas. Dessa forma, os profissionais mantêm o controle sobre decisões de risco, estratégias de cobertura e testes exploratórios complexos.  
Neste escopo, o presente projeto delimita-se ao desenvolvimento de um Agente de QA End-to-End (E2E) autônomo com capacidades de *Self-Healing* (autocura), focado estritamente na fronteira de integração (Front-to-Back) da API.

## **1.2 Problema de Pesquisa**

Diante do cenário de fragilidade dos testes automatizados e das limitações de infraestrutura corporativa, levanta-se a seguinte questão de pesquisa: Como um Modelo de Linguagem Grande (LLM), aliado à interceptação bidimensional, pode diagnosticar autonomamente falhas na fronteira de integração Front-to-Back, sem a necessidade de acoplamento à lógica interna do servidor, operando sob restrições de hardware local?

## **1.3 Justificativa**

Este trabalho justifica-se pela necessidade de desenvolver ferramentas de assistência focadas em acelerar a Análise de Causa Raiz para as equipes técnicas. Tradicionalmente, quando ocorre uma falha silenciosa na integração cliente-servidor, perdem-se horas cruzando capturas de tela com logs de servidor para entender o desvio.  
O agente proposto atuará como um copiloto de depuração inteligente: ao unir a leitura estruturada da interface renderizada à interceptação nativa de rede do framework Playwright, ele pré-processa a falha e entrega ao desenvolvedor um diagnóstico rápido de onde o contrato da API divergiu do esperado pela interface. O projeto visa melhorar o tempo de resposta da equipe frente a bugs de API e reduzir o desgaste com a manutenção de rotinas frágeis, permitindo que o profissional foque na revisão da qualidade e na garantia da integridade da arquitetura de software.

## **1.4 Objetivos**

<!-- ! Alteração de IA - Revisar: objetivo geral reescrito — a inferência do LLM passa de "arquitetura de nuvem híbrida" para execução local, e o escopo do Self-Healing passa a ser explicitamente a cura de localizadores + diagnóstico, no lugar de "propor correções de código".
     ! Motivo: a implementação adotada roda o modelo integralmente na máquina do usuário (sem Google Colab, FastAPI de ponte ou Ngrok), para que a ferramenta seja utilizável fora do ambiente universitário sem custo e sem configuração de nuvem; e a correção autônoma de código-fonte da aplicação-alvo foi descartada por ser inviável de forma confiável com um modelo quantizado pequeno. -->

**Objetivo Geral:** Desenvolver, implementar e mensurar a eficácia de um Agente de QA E2E Autônomo, utilizando um LLM executado localmente para realizar o *Self-Healing* dos localizadores de scripts de teste e para produzir o diagnóstico de causa raiz a partir da análise conjunta da interface e da interceptação de rede, facilitando a depuração pela equipe.  
**Objetivos Específicos:**

> * Levantar a fundamentação teórica e preparar o ambiente base, pesquisando metodologias de automação com LLMs, extração de árvores de acessibilidade e quebra de contrato de APIs.  
> * Prototipar a camada de inferência local, configurando o orquestrador e o runtime de modelos (Ollama) para executar o modelo Qwen2.5-Coder quantizado integralmente na máquina do usuário, sem dependência de infraestrutura em nuvem.  
> * Implementar o Módulo de Filtragem de Contexto (DOM Pruning) para impedir o estouro da janela de contexto (Context Window) do LLM.  
> * Desenvolver o Agente de Interceptação e Self-Healing, integrando a automação visual para capturar requisições HTTP e codificar a lógica autônoma de correção.  
> * Mensurar e validar a precisão e performance do agente contra aplicações de teste, utilizando injeção de falhas sintéticas e Fuzzing de mutação de API.

# **2 REFERENCIAL TEÓRICO**

Este projeto fundamenta-se nos avanços documentados na literatura técnico-científica sobre a adoção de modelos generativos no ciclo de vida de desenvolvimento de software (SDLC) e nos fundamentos clássicos de aprendizado de máquina.

## **2.1 Evolução da Automação E2E e o Conceito de Self-Healing**

A automação de testes de software transitou de scripts manuais lineares para abordagens complexas de ponta a ponta (End-to-End \- E2E), projetadas para simular o comportamento de um usuário real em toda a pilha tecnológica da aplicação. Inicialmente, a automação E2E baseava-se em localizadores estáticos dentro do Document Object Model (DOM) — a estrutura HTML da página. Contudo, essa dependência tornava os testes frágeis e suscetíveis a quebras mediante qualquer alteração visual ou estrutural na interface gráfica.  
Para mitigar este problema, o conceito de autocura (*Self-Healing*) emergiu na interseção entre engenharia de software e inteligência artificial. Em sistemas distribuídos, a autocura refere-se à capacidade de um sistema detectar falhas ativamente, diagnosticar sua causa raiz e aplicar correções de forma autônoma. No contexto de testes de qualidade (QA), um agente dotado de *Self-Healing* utiliza algoritmos de busca e processamento de linguagem natural para identificar dinamicamente novos localizadores na interface ou interpretar desvios nas respostas do servidor (*Contract Drift*) quando o script original falha, restaurando assim o fluxo de execução sem a necessidade de intervenção humana imediata.

<!-- ! Alteração de IA - Revisar: acrescentado o parágrafo abaixo, delimitando o grau de autonomia adotado.
     ! Motivo: o texto original oscilava entre "aplicar correções autonomamente" (2.1 e glossário) e "copiloto que propõe correções" (1.3 e objetivo geral), o que deixaria a banca sem saber qual dos dois é entregue e tornaria a métrica Task Success ambígua. -->

Cabe delimitar o grau de autonomia adotado neste trabalho. A correção de localizador é gerada e **aplicada automaticamente** pelo agente em uma reexecução de verificação, o que permite medir objetivamente se o fluxo do teste foi de fato restaurado (Task Success). Contudo, a alteração não é incorporada de forma definitiva ao repositório de testes sem revisão: ela é registrada e **apresentada ao desenvolvedor como sugestão**. Essa delimitação preserva o caráter de copiloto descrito na justificativa, sem abrir mão da verificação automática necessária à avaliação quantitativa.

## **2.2 Fundamentos de Aprendizado de Máquina e Adaptação**

A transição de sistemas baseados em regras estritas para sistemas adaptativos (como os testes com *Self-Healing*) encontra sua base teórica no aprendizado de máquina. Segundo Faceli et al. (2025), os algoritmos de aprendizado de máquina permitem que sistemas computacionais extraiam padrões intrínsecos a partir de dados para a tomada de decisão autônoma, superando as limitações da programação puramente determinística. Ao invés de falhar imediatamente ante uma mudança no DOM, o sistema dotado de inteligência artificial utiliza o reconhecimento de padrões para inferir a intenção original do teste e sugerir a correção.

<!-- ! Alteração de IA - Revisar: a citação de Faceli et al. passa de 2021 para 2025 (3. ed.) e foi acrescentado o parágrafo abaixo, que aponta o Capítulo 10 (avaliação de modelos preditivos) e o Capítulo 7 (métodos conexionistas) como a base do desenho de avaliação e do modelo de linguagem empregado, com a ressalva de que os capítulos foram identificados pelo sumário da 3. ed.
     ! Motivo: o documento citava a 2. ed. de 2021, substituída pela 3. ed. de 2025, que é o exemplar adotado pelo projeto; e a única menção ao livro-texto era genérica ("extrair padrões a partir de dados"), sem ligar nenhum capítulo ao que a seção 3.4 mede — matriz de confusão, partição entre treino e teste e métricas de classificação multiclasse —, deixando o instrumental de avaliação do trabalho sem âncora no referencial teórico. A ressalva sobre o sumário é a mesma registrada na §6.8 do Memorial: o levantamento conferiu ficha catalográfica, ISBN, paginação e sumário na página da editora, mas não o conteúdo interno dos capítulos, de modo que o texto nomeia os capítulos pelos títulos e não cita página nem trecho. -->

A mesma obra fornece o instrumental de avaliação adotado neste projeto. O Capítulo 10, dedicado à avaliação de modelos preditivos, trata da partição dos dados entre treino e teste, da matriz de confusão e das métricas dela derivadas — acurácia, precisão, revocação e F1 —, bem como de suas médias macro e micro em problemas de classificação multiclasse, que é a forma assumida pela tarefa de diagnóstico deste trabalho: atribuir à falha observada uma entre várias causas raiz possíveis. O Capítulo 7, sobre métodos conexionistas, cobre as redes neurais profundas que servem de base à arquitetura de transformadores empregada pelos LLMs, situando o modelo de linguagem utilizado no mesmo arcabouço teórico (FACELI et al., 2025 — capítulos identificados pelo sumário da 3. ed.; conteúdo a conferir no exemplar).

## **2.3 Automação E2E e Inteligência Artificial**

Estudos recentes, como o GenIA-E2ETest (JÚNIOR et al., 2025), compõem a base metodológica que atesta a eficácia dos LLMs (Modelos de Linguagem Grandes) na interpretação de intenções textuais e tradução para comandos automatizados de interação de elementos de interface. A implementação do Playwright Healer Agent (BISWAS, 2026\) sustenta o diferencial arquitetural deste trabalho, validando que a interceptação do tráfego de rede aliada à IA mitiga drasticamente os falsos-positivos.

## **2.4 Gestão de Context Window em LLMs**

<!-- ! Alteração de IA - Revisar: a chamada do Prune4Web no parágrafo abaixo passa de "(ZHANG et al., 2026)" para "(ZHANG, J. et al., 2026)".
     ! Motivo: a lista de REFERÊNCIAS passou a ter dois autores de sobrenome Zhang com obras de 2026 — ZHANG, J. et al. (Prune4Web, poda da árvore de elementos) e ZHANG, G. et al. (admissão de itens na base de conhecimento, citado na seção 2.6). Sem a inicial do prenome, a chamada no texto não indica qual das duas entradas da lista está sendo referida. -->

A literatura comprova que sobrecarregar a memória de contexto (Context Window) dos LLMs com códigos HTML puros degrada seu raciocínio lógico, um fenômeno conhecido como Attention Dilution. Metodologias focadas em podar e limpar a árvore de elementos antes do processamento, como o Prune4Web (ZHANG, J. et al., 2026), formam a espinha dorsal das técnicas de filtragem utilizadas neste projeto para viabilizar inferências precisas com custo computacional reduzido.

<!-- ! Alteração de IA - Revisar: acrescentado o parágrafo abaixo, citando JOSEPH (2026) e fixando sobre qual estrutura a poda é aplicada.
     ! Motivo: JOSEPH constava nas REFERÊNCIAS sem ser citado no corpo (o que contraria a NBR 6023, segundo a qual a lista contém apenas obras citadas), e o texto original nomeava dois artefatos — "extração da árvore de acessibilidade" e "heurísticas de DOM Pruning" — sem nunca dizer se a poda incide sobre o DOM bruto ou sobre a árvore de acessibilidade, o que deixaria a implementação sem critério. -->

Complementarmente, Joseph (2026) demonstra que a extração da árvore de acessibilidade (*Accessibility Tree*) constitui, por si só, uma estratégia de redução de contexto de baixo custo, por expor apenas a projeção semântica dos elementos — seu papel (*role*), nome acessível e valor — em vez da árvore HTML completa. Este projeto adota essa abordagem como substrato: a poda é aplicada **sobre a árvore de acessibilidade**, e não sobre o DOM bruto, que passa a ser consultado apenas pontualmente, durante a resolução de um localizador na etapa de autocura.

<!-- ! Alteração de IA - Revisar: acrescentados os dois parágrafos abaixo — a contagem do contexto em tokens e o custo do português (CORRÊA et al., 2024 e 2026), e a diferença entre a janela nominal e a útil, com o corte silencioso do início do prompt no Ollama (KULIGOWSKI, 2026) e a perda de acerto conforme a posição do trecho relevante (LIU et al., 2024; CUCONASU et al., 2024).
     ! Motivo: a seção falava em "sobrecarregar a memória de contexto" e em poda, mas não dizia em que unidade o limite é contado nem o que acontece ao ultrapassá-lo. Sem isso, ficavam sem justificativa duas decisões da metodologia: estimar os tokens por caracteres antes de montar o prompt, conferi-los com a contagem real devolvida pelo runtime depois de cada inferência, e ordenar o prompt do conteúdo estável para o variável. O ponto prático é que o runtime descarta o começo do prompt — onde ficam as instruções e o esquema da resposta — sem devolver nenhum aviso na resposta da API. Os números de tokenização vêm da §6.7 do Memorial (`tokenizacao-e-arquitetura.md`) e os de posição no contexto, da §6.3 (`documentacao-como-contexto-rag.md`). -->

<!-- ! Alteração de IA - Revisar: (revisão 2, 12/09/2026) nos dois parágrafos abaixo, "apurar o orçamento com o tokenizador real de cada modelo" e "conferir o consumo de tokens antes de cada inferência" passaram a descrever o que o harness faz — estimativa por caracteres antes de montar o prompt e conferência com a contagem real de tokens que o runtime devolve depois de cada inferência, com a época interrompida quando o orçamento é ultrapassado —, e o valor de Liu et al. (2024) para o meio do contexto ganhou a posição (décima de vinte); e o motivo da tag anterior (acima) foi reescrito para descrever o mesmo procedimento. Na segunda passada da mesma data, o fim do segundo parágrafo passou a dizer que a estimativa é feita no início de cada época, sobre o maior prompt da época, e que só a conferência com a contagem real é feita após cada inferência.
     ! Motivo: o harness não carrega o tokenizador de nenhum modelo — quem conta os tokens é o próprio Ollama, depois da inferência (`prompt_eval_count`), e a guarda anterior à inferência é por caracteres; o texto prometia uma medição que o código não faz, e o relatório final citaria um procedimento inexistente. "No meio", sem a posição, não permite conferir o número na figura do artigo (o levantamento de 11/09/2026 registra cerca de 52,9% para o mesmo ponto). O marcador voltou à forma fixa do CLAUDE.md, com os dois-pontos logo depois de "Revisar", porque um filtro por "Revisar:" não achava a variante com o parêntese antes dos dois-pontos. E "antes de cada inferência" continuava impreciso: `guarda_estimativa` (`executar_fase3.py`) roda uma vez por época, sobre o maior prompt de diagnóstico entre os casos pendentes; a cada inferência roda só `guarda_tokens_reais`. -->

O limite dessa janela, contudo, não é contado em caracteres, e sim em *tokens* — as unidades discretas em que o texto é convertido pela tokenização, etapa que antecede qualquer processamento pelo modelo. A correspondência entre caracteres e tokens, e a fertilidade (tokens por palavra) que dela decorre, variam conforme o idioma e o tokenizador empregado. Para o português, Corrêa et al. (2026) medem, em corpus de cerca de 600 mil palavras, 2,88 caracteres por token no tokenizador nativo do modelo Tucano 2 e entre 2,71 e 2,72 caracteres por token nos tokenizadores de três modelos abertos recentes — faixa compatível com os 2,6 a 2,8 caracteres por token apurados nos ensaios preliminares deste projeto com os tokenizadores reais dos modelos avaliados. A diferença entre tokenizadores não é marginal: segundo Corrêa et al. (2024), o mesmo texto de 7.400 palavras em português consumiu 9.937 tokens com o tokenizador do TeenyTinyLlama e 14.813 com o do Sabiá-7B. A consequência prática é que o orçamento de contexto não pode ser fechado pela regra prática de estimar um token a cada quatro caracteres, formulada para o inglês: a estimativa por caracteres serve para montar o prompt, e é a contagem real de tokens devolvida pelo runtime depois de cada inferência que confirma se o orçamento foi respeitado.

Disso decorre a distinção entre a janela nominal e a janela efetivamente útil. Quando o prompt excede o limite configurado, o runtime Ollama descarta silenciosamente o início da conversa, sem qualquer campo de aviso na resposta de sua interface de programação, registrando o corte apenas em log de depuração (KULIGOWSKI, 2026) — e é justamente no início do prompt que ficam as instruções e o esquema da resposta esperada. Ainda que o conteúdo caiba na janela, a posição em que é colocado altera o desempenho. Liu et al. (2024) medem uma curva em U de aproveitamento no GPT-3.5-Turbo: com vinte documentos fornecidos ao modelo, o acerto é de 75,8% quando o documento relevante está na primeira posição, cai para 53,8% quando está na décima posição, no meio da lista, e sobe para 63,2% na última — no meio do contexto, o desempenho fica abaixo dos 56,1% obtidos pelo mesmo modelo sem contexto algum. Cuconasu et al. (2024) reproduzem o efeito em modelos abertos: no Llama2-7B, com um documento correto e 18 distratores, a acurácia é de 0,3781 quando o documento correto está junto à pergunta e de 0,1795 quando está no meio do contexto, comportamento consistente também em Falcon-7B, MPT-7B e Phi-2 (2,7B). As duas constatações — corte silencioso no início e perda no meio — sustentam duas providências adotadas neste projeto: ordenar o prompt do conteúdo mais estável para o mais variável e estimar, no início de cada época, o consumo de tokens do maior prompt da época e conferir a contagem real devolvida pelo runtime depois de cada inferência — um caso que ultrapasse o orçamento interrompe a época em vez de ser truncado em silêncio —, em vez de confiar na capacidade nominal declarada pelo runtime.

## **2.5 Detecção de Quebra de Contrato de API**

<!-- ! Alteração de IA - Revisar: subseção nova, citando MACIAK et al. (2026).
     ! Motivo: a referência constava na lista sem citação no corpo, e o Contract Drift — que é o objeto central do trabalho — não tinha nenhuma subseção própria no referencial, aparecendo apenas como definição solta na introdução e no glossário. -->

A verificação automatizada de contratos entre cliente e servidor é discutida por Maciak et al. (2026), que caracterizam a deriva de contrato (*API drift*) como uma classe de falha que escapa aos testes unitários de cada lado isoladamente, por se manifestar apenas na fronteira de integração. Os autores destacam que alterações silenciosas de tipo, remoção de campos e renomeações são detectáveis por comparação estrutural da resposta observada contra o contrato esperado — princípio que fundamenta o gatilho de erro adotado neste projeto, no qual a interceptação de rede compara a forma (chaves e tipos) do dado recebido com a esperada pela interface consumidora.

## **2.6 Recuperação de Conhecimento Prévio Aplicada à Localização de Falhas**

<!-- ! Alteração de IA - Revisar: subseção nova, citando SHI, LI e CHEN (2025).
     ! Motivo: a referência sobre RAG constava na lista sem nenhuma citação no corpo, e a arquitetura implementada inclui uma base de conhecimento consultada pelo modelo — sem esta subseção, esse componente ficaria sem fundamentação teórica no documento. -->

Shi, Li e Chen (2025) demonstram que a Geração Aumentada por Recuperação (*Retrieval-Augmented Generation* \- RAG), quando sensível à funcionalidade do trecho analisado, melhora a localização de falhas por LLMs ao fornecer ao modelo apenas o conhecimento pertinente ao defeito em questão, em vez de ampliar indiscriminadamente o contexto. Neste trabalho, o princípio é aplicado por meio de uma base de conhecimento curada sobre a aplicação-alvo — organizada por módulo e por entidade de negócio, e contendo regras de negócio e defeitos previamente conhecidos — recuperada seletivamente no momento do diagnóstico.

Cabe ressaltar que essa base é **estática e construída previamente**, de forma análoga ao conhecimento acumulado por um analista de QA sobre o sistema que testa. Ela não implica inspeção da lógica interna do servidor em tempo de execução, preservando a delimitação de escopo estabelecida na seção 1.2.

<!-- ! Alteração de IA - Revisar: acrescentados os dois parágrafos abaixo — o risco de o modelo seguir um trecho recuperado incorreto (WU; WU; ZOU, 2024; ZOU et al., 2025) e o regime em que o próprio modelo mantém a base de conhecimento, com a admissão de cada item decidida em código (SUZGUN et al., 2025; ZHANG, G. et al., 2026).
     ! Motivo: a seção descrevia a base como estática e curada à mão, sem registrar que documentação errada é adotada pelo modelo na maior parte dos casos, e portanto sem justificar por que a conferência de cada item precisa ser feita por regras em código e não pelo julgamento de outro modelo de linguagem. Era também o elo que faltava para a etapa descrita na seção 3.2, em que a base passa a ser mantida pelo próprio modelo. Os números de adesão a conteúdo recuperado incorreto vêm da §6.3 do Memorial (`documentacao-como-contexto-rag.md`) e os de memória gerida pelo modelo, da §6.6 (`memoria-gerida-pelo-modelo.md`). -->

A recuperação, porém, transfere ao material recuperado parte da responsabilidade pelo diagnóstico, e a literatura mede o custo de recuperar material incorreto. Wu, Wu e Zou (2024), em seis modelos de ponta e mais de mil e duzentas perguntas distribuídas por seis domínios, observam que os modelos abandonam conhecimento interno correto e adotam o conteúdo recuperado incorreto em mais de 60% dos casos, com adesão tanto maior quanto menor a confiança do modelo na própria resposta. Pelo lado da segurança, Zou et al. (2025) mostram que bastam cinco textos maliciosos por pergunta-alvo, inseridos em uma base com milhões de textos, para induzir em 90% dos casos a resposta escolhida pelo atacante. Daí a exigência, adotada neste trabalho, de que todo item da base de conhecimento — tanto os escritos à mão quanto os que venham a ser acrescentados depois — passe por uma conferência determinística, escrita em código, e não pelo julgamento do próprio modelo, antes de ficar disponível para recuperação.

Uma extensão natural dessa base é deixar que o próprio modelo a mantenha, acrescentando o que apura ao longo das execuções sem que seus pesos sejam alterados. Suzgun et al. (2025) demonstram que essa forma de aprendizado em tempo de teste produz ganho expressivo em modelos grandes, mas registram o limite que interessa diretamente a este projeto: em modelos menores os ganhos são atenuados por falta de competência para escrever bons registros, e o desempenho chega a cair quando material de baixa qualidade é recuperado — o gargalo está em quem escreve, e não em quem lê. Zhang, G. et al. (2026) quantificam o efeito de um portão de admissão calculado majoritariamente em código, que rejeitou 63,1% dos itens candidatos e elevou o F1 da tarefa de 0,541 para 0,583 com 31% menos latência, sendo que quatro dos cinco sinais avaliados são regras determinísticas que custam menos de 65 ms, contra 2.580 ms do único sinal julgado por outro modelo de linguagem. É esse arranjo — base mantida pelo modelo, com a admissão de cada item decidida em código — que a etapa experimental descrita na seção 3.2 submete a teste.

# **3 METODOLOGIA**

A pesquisa caracteriza-se como um projeto prático e aplicado (Pesquisa-Ação), voltado para a construção e validação de uma arquitetura de software escalável. A infraestrutura baseia-se nas seguintes camadas:

## **3.1 Infraestrutura e Orquestração Local**

A ferramenta principal de orquestração será o Playwright (com Node.js/Python). O Playwright comunica-se com o navegador via protocolos nativos e possui suporte embutido para interceptação e modificação de chamadas de rede em tempo real. Isso permite extrair a árvore de acessibilidade do DOM e escutar os códigos de status HTTP em segundo plano. Como contingência, o framework Cypress poderá ser acionado caso ocorram incompatibilidades críticas.

## **3.2 Inteligência Artificial e Processamento LLM**

<!-- ! Alteração de IA - Revisar: seção reescrita — a inferência sai do Google Colab (GPU T4) e passa a ser executada localmente via Ollama, com o modelo quantizado.
     ! Motivo: a dependência de nuvem contradizia o próprio problema de pesquisa (seção 1.2), que pergunta como operar "sob restrições de hardware local"; além disso, exigir configuração de Colab e túnel de rede inviabilizaria o uso da ferramenta fora do ambiente universitário. A execução local torna a resposta à pergunta de pesquisa direta, em vez de contornada. -->

O processamento semântico utilizará o modelo Qwen2.5-Coder em variante quantizada, executado **integralmente na máquina local** por meio do runtime Ollama. A quantização reduz a precisão numérica dos pesos do modelo, diminuindo o consumo de memória a ponto de viabilizar a inferência em CPU, sem GPU dedicada.

A escolha do porte do modelo (1,5B, 3B ou 7B de parâmetros) será definida experimentalmente, por comparação entre as variantes sob o mesmo hardware, considerando latência por inferência, pico de memória e qualidade do diagnóstico produzido. Adota-se como critério o **menor modelo que atenda à tarefa**, e não o maior que couber na máquina, uma vez que o agente compete por memória com o navegador automatizado, o servidor de aplicação e o banco de dados da aplicação-alvo durante a execução dos testes.

<!-- ! Alteração de IA - Revisar: acrescentado o parágrafo abaixo com o protocolo da Fase 3 — cópia da base de conhecimento por modelo, edição só por acréscimo, conferência em código antes de incorporar, três épocas e partição de 54 casos de aprendizado contra 36 de avaliação.
     ! Motivo: a seção 2.6 passou a tratar de base mantida pelo próprio modelo, mas a metodologia não dizia como isso seria executado nem medido. Sem a partição declarada, o ganho medido misturaria o que o modelo generaliza com o que ele apenas memorizou dos casos em que viu a causa correta; e sem a regra de só acrescentar, uma edição que apagasse conteúdo tornaria impossível reconstruir o que mudou entre duas épocas. -->

O regime de base de conhecimento mantida pelo próprio modelo, discutido na seção 2.6, será submetido a teste em uma etapa experimental dedicada — aqui designada **Fase 3** —, na qual cada modelo avaliado recebe uma cópia própria da base, permanecendo a base original intocada como ponto de partida comum a todos. A edição autorizada é apenas por acréscimo — nota em um item existente, retificação que aponte o trecho equivocado ou item novo —, nunca por remoção, de modo que toda alteração permaneça auditável pela comparação entre versões sucessivas. Nenhuma proposta de edição é incorporada sem passar antes por uma conferência escrita em código, e não pelo julgamento de outro modelo de linguagem, pelo motivo exposto na seção 2.6. O ciclo é repetido por três épocas, guardando-se a cópia da base ao final de cada uma, para que o desempenho possa ser lido época a época e não apenas ao final. Os casos são divididos em duas partições — 54 de aprendizado e 36 de avaliação —, e somente nos 54 o modelo tem acesso à causa correta e pode propor edições, enquanto os 36 nunca recebem retorno, o que separa o que o modelo generaliza do que ele apenas memoriza.

## **3.3 Comunicação e Mitigação de Gargalos**

<!-- ! Alteração de IA - Revisar: seção reescrita — removidos o túnel Ngrok e a API de ponte em FastAPI; a comunicação com o modelo passa a ser local (loopback). Detalhada a regra de truncamento de JSON.
     ! Motivo: com a inferência local (seção 3.2), não há servidor remoto a ser exposto, o que torna o túnel desnecessário. O truncamento também precisava de critério explícito: cortar indiscriminadamente destruiria justamente o sinal de quebra de contrato que o agente busca. -->

Com a inferência executada localmente, a comunicação entre o orquestrador e o modelo ocorre pela interface HTTP do próprio runtime, restrita à interface de loopback da máquina, dispensando exposição à rede externa e qualquer serviço de tunelamento. O framework FastAPI permanece em uso no projeto, porém no papel de API da aplicação-alvo submetida aos testes, e não como camada de integração com o modelo.

Para evitar o colapso da janela de contexto do LLM, aplicar-se-ão heurísticas estritas de poda sobre a árvore de acessibilidade (seção 2.4), enviando apenas os elementos semanticamente relevantes da interface, acompanhadas do truncamento dos dados JSON extensos interceptados na rede.

O truncamento observará uma restrição específica: reduz-se o **volume** do dado — encurtando listas extensas e cadeias de texto longas —, preservando-se integralmente suas **chaves e tipos**. Essa distinção é necessária porque a quebra de contrato manifesta-se na forma do dado, e não em sua quantidade; um truncamento que suprimisse campos eliminaria o próprio fenômeno que se pretende detectar.

## **3.4 Validação e Avaliação**

A avaliação evitará a subjetividade inerente às análises feitas puramente por IAs, adotando aplicações-alvo determinísticas. Aplicar-se-á técnicas de Fuzzing (injeção de dados anômalos e imprevistos) e Mutação Dinâmica para simular quebras de contrato reais em APIs. O sucesso do agente será avaliado quantitativamente por duas métricas principais: Tempo Médio de Reparo (MTTR) e Task Success (Sucesso da Tarefa), verificando na prática se a sugestão refatorada consegue restaurar a estabilidade do teste.

<!-- ! Alteração de IA - Revisar: acrescentadas as definições operacionais das métricas, o grupo de controle, o volume de execuções e as condições de determinismo.
     ! Motivo: o texto original comprometia-se com MTTR e Task Success sem definir fórmula, linha de base, critério de sucesso ou número de repetições, e os resultados esperados falavam em reduzir o MTTR "significativamente" — sem esses parâmetros, o Mês 5 chegaria sem protocolo e nenhum resultado seria defensável perante a banca. -->

**Aplicações-alvo.** Serão utilizadas duas aplicações de características deliberadamente distintas, ambas construídas e controladas pelo próprio grupo: uma aplicação monolítica legada, com renderização no servidor e acesso direto ao banco de dados, e uma interface moderna que consome uma API JSON por requisições assíncronas. A primeira exercita a abrangência do agente frente a sistemas legados; a segunda concentra os cenários de quebra de contrato, objeto central do trabalho.

**Definições operacionais.** O Tempo Médio de Reparo (MTTR) é medido como o intervalo entre a detecção da falha pelo agente e a restauração verificada do fluxo de execução, isto é, o instante em que a correção proposta é validada com sucesso na reexecução. O Task Success é definido como a proporção de cenários em que o fluxo foi restaurado e o roteiro de teste concluiu sem erro, sobre o total de cenários de falha injetados.

**Linha de base.** Como grupo de controle, os mesmos cenários serão resolvidos manualmente por integrantes do grupo, com o tempo cronometrado desde a apresentação da falha até a correção do teste. A comparação entre esse tempo e o MTTR do agente constitui o resultado central da avaliação.

**Volume e determinismo.** Cada configuração será submetida a cerca de dez cenários distintos, com cinco repetições cada, cobrindo os modos de falha injetados e a quebra de localizador. Para assegurar a reprodutibilidade, o banco de dados da aplicação-alvo é restaurado ao estado inicial entre execuções, o modo de falha é fixado por cenário, e a versão do navegador é mantida constante pelo próprio orquestrador, evitando variação decorrente de atualizações automáticas.

<!-- ! Alteração de IA - Revisar: acrescentado o bloco abaixo com as métricas e os testes da Fase 3 — acurácia balanceada como métrica primária, intervalo de confiança de Wilson, McNemar pareado, Q de Cochran com correção de Holm sobre as versões L0 a L3 da base, g de Cohen, contagem de casos que trocam de rótulo (*flips*), revisão humana por rubrica e a regra de só comparar etapas com prompts idênticos.
     ! Motivo: a seção definia MTTR e Task Success, que medem a etapa de autocura, e nada sobre a classificação da causa raiz, que é o resultado da Fase 3. Faltavam também o intervalo de confiança e o teste pareado: com cerca de noventa casos, reportar a taxa de acerto como ponto ou com intervalo de Wald entregaria cobertura menor que a declarada, e comparar quatro versões da base par a par sem teste conjunto e sem correção faria aparecer diferença apenas pelo número de comparações feitas. -->

**Métricas da Fase 3.** A métrica primária de comparação entre modelos e entre versões da base de conhecimento será a acurácia balanceada, isto é, a média das revocações obtidas em cada classe. A escolha é justificada, e não herdada: Opitz (2024) mostra que acurácia, F1 micro, macro e ponderada, kappa e coeficiente de correlação de Matthews diferem sistematicamente em viés e em sensibilidade à prevalência das classes, de modo que a métrica principal precisa ser argumentada e acompanhada das demais; e Collot et al. (2026) demonstram que a acurácia balanceada é a métrica alinhada à comparação de modelos sob desbalanceamento, por não depender da escolha arbitrária de uma classe positiva — propriedade decisiva aqui, porque o modo de falha previsto é o colapso do modelo em um único rótulo, que a acurácia simples não distingue de acerto genuíno.

**Inferência estatística.** Toda proporção será reportada com intervalo de confiança de 95% pelo método de escore de Wilson, e não pelo intervalo de Wald derivado do Teorema Central do Limite: Bowyer, Aitchison e Ivanova (2025) medem que, com cerca de cem itens, o intervalo de Wald entrega apenas 92,5% de cobertura real, degradando severamente em amostras menores, a ponto de produzir intervalos de largura zero ou fora do intervalo \[0,1\]. Como todos os contrastes incidem sobre os mesmos casos, a comparação entre duas condições usará o teste de McNemar pareado, que aproveita o pareamento como fonte de potência estatística. Para as quatro versões da base geradas ao longo das épocas (L0 a L3), o teste conjunto será o Q de Cochran — a generalização do McNemar para mais de duas condições pareadas —, seguido, quando significativo, de comparações par a par com correção de Holm, procedimento passo a passo que García e Herrera (2008) apontam como mais potente que as alternativas conservadoras de uso corrente (a leitura do artigo quanto ao conjunto exato de procedimentos comparados permanece a conferir). Ao lado de cada valor-p será reportado o tamanho de efeito pelo g de Cohen, uma vez que o valor-p isolado não informa magnitude.

<!-- ! Alteração de IA - Revisar: (revisão 2, 12/09/2026) no parágrafo abaixo, a amostra revista por pessoas passou de "diagnósticos produzidos" para "edições aceitas na base de conhecimento", com o tamanho (até trinta por modelo), a planilha por modelo, a rubrica (correta, parcial ou errada) e o fato de haver um único revisor. Na segunda passada da mesma data, o nome do arquivo (`revisao_edicoes__<modelo>.md`) e os rótulos em fonte monoespaçada saíram do corpo do parágrafo, que ficou em prosa com os rótulos em itálico; o nome do arquivo fica no Memorial (§7 do relatório da Fase 3).
     ! Motivo: o que o harness da Fase 3 manda para revisão humana é a edição que o modelo escreveu e a validação em código aceitou (`avaliar_fase3.py --gerar-revisao`), porque a validação diz se a edição pode entrar e só a leitura humana diz se ela está certa sobre o sistema; os diagnósticos são pontuados pelo gabarito, sem revisão. E com um só revisor não há medida de concordância a reportar. O marcador voltou à forma fixa do CLAUDE.md, com os dois-pontos logo depois de "Revisar", porque um filtro por "Revisar:" não achava a variante com o parêntese antes dos dois-pontos; e o parágrafo era a única linha do corpo do documento com trechos em crase — o resto marca termos técnicos em itálico (*flips*, *Accessibility Tree*), e na conversão para PDF a fonte monoespaçada e o `<modelo>` destoavam do padrão. -->

**Métrica de risco e revisão humana.** Além do acerto agregado, será contabilizado o número de trocas de rótulo (*flips*): casos individuais que mudam de resposta entre duas condições ainda que a média se mantenha. Dutta et al. (2024) medem que até 13,6% das respostas individuais trocam de rótulo entre esquemas de quantização do mesmo modelo com diferença de acurácia de até dois pontos percentuais, o que torna a média insuficiente como critério de aceitação de uma versão da base. Uma amostra das edições aceitas na base de conhecimento — até trinta por modelo, sorteadas de forma determinística e gravadas em uma planilha por modelo — será ainda revista por um único revisor do grupo segundo rubrica escrita previamente (*correta*, *parcial* ou *errada*), com os critérios fixados antes da leitura dos resultados; por haver um só revisor, o resultado é reportado como proporção, sem medida de concordância.

**Comparabilidade entre etapas.** A comparação entre as etapas experimentais só será feita com prompts idênticos, byte a byte. Sclar et al. (2024), avaliando 320 formatos semanticamente equivalentes em cerca de 53 tarefas, medem variação de até 76 pontos de acurácia e amplitude mediana de 6,4 pontos decorrentes apenas do formato do prompt — variação que não é eliminada por exemplos no prompt, por escala do modelo nem por ajuste por instrução. Diferenças entre etapas menores que essa amplitude não seriam atribuíveis ao desenho experimental; por isso o que não for comparável será apresentado lado a lado, e nunca como diferença testada.

# **4 RESULTADOS ESPERADOS**

<!-- ! Alteração de IA - Revisar: substituída a menção à "topologia de nuvem híbrida" pela execução local.
     ! Motivo: o resultado esperado afirmava comprovar a viabilidade em máquinas com restrição de hardware "através da topologia de nuvem híbrida" — o que era contraditório, pois recorrer a uma GPU em nuvem contorna a restrição em vez de demonstrar viabilidade sob ela. Com a inferência local, a afirmação passa a ser sustentada pelo próprio experimento. -->

Espera-se que o Agente de QA Autônomo reduza significativamente o Tempo Médio de Reparo (MTTR) associado à manutenção de testes E2E, quando comparado à correção manual dos mesmos cenários. Projetamos que o agente identifique com precisão a causa raiz de falhas de comunicação através da depuração bidimensional. Adicionalmente, o projeto deve comprovar a viabilidade técnica da orquestração de IA em máquinas com restrições de hardware, executando o modelo integralmente em ambiente local e sem custo de infraestrutura — condição que também torna a ferramenta aplicável fora do ambiente acadêmico.

# **5 CRONOGRAMA DE ATIVIDADES**

| Etapa / Mês | Atividade Prevista |
| :---- | :---- |
| Mês 1 | Revisão bibliográfica (LLMs, DOM Pruning, Contract Drift). |
| Mês 2 | Configuração do ambiente local e da camada de inferência (Ollama com Qwen2.5-Coder quantizado), incluindo a comparação entre portes de modelo. |
| Mês 3 | Desenvolvimento do Módulo de Filtragem de Contexto e extração da Accessibility Tree via Playwright. |
| Mês 4 | Codificação do fluxo de Self-Healing e lógica de interceptação do Agente. |
| Mês 5 | Testes práticos (Fuzzing) em aplicações-alvo e coleta de métricas (MTTR e Task Success). |
| Mês 6 | Redação, formatação ABNT e revisão dos capítulos do TCC. |
| Mês 7 | Finalização do documento e Defesa Final perante a banca. |

# **REFERÊNCIAS**

<!-- ! Alteração de IA - Revisar: FACELI et al. passa da 2. ed. (2021) para a 3. ed. (2025) e foram acrescentadas 15 referências, em ordem alfabética, correspondentes às citações incluídas nas seções 2.2, 2.4, 2.6, 3.2 e 3.4.
     ! Motivo: a edição citada não era a adotada pelo projeto, e a NBR 6023 exige que a lista contenha exatamente as obras citadas no corpo — as citações novas ficariam sem entrada, repetindo o defeito já corrigido antes com JOSEPH, MACIAK e SHI, que constavam na lista sem aparecer no texto. As entradas novas seguem o mesmo formato das sete já existentes (sobrenome em caixa-alta, iniciais do prenome, destaque no título do periódico, do evento ou da obra), e todas as entradas cujo endereço eletrônico consta de `Documentacao/memorial/2-pesquisa-e-literatura/referencias.md` — as novas e as antigas — receberam `Disponível em` e `Acesso em`, porque a maioria é de material só publicado na internet (preprints do arXiv, atas em repositório, uma issue do GitHub e um texto no Medium), que sem endereço não se localiza. Continuam sem endereço as cinco entradas cuja URL não existe em nenhum arquivo do repositório: BISWAS, JÚNIOR, MACIAK, SHI e ZHANG, J. -->

BISWAS, S. Enhancing End-to-End Test Stability Through AI-Assisted Self-Healing: A Case Study of Playwright Healer Agent Implementation. **International Journal of Scientific Engineering and Research**, v. 14, n. 1, p. 1-12, jan. 2026\.

BOWYER, S.; AITCHISON, L.; IVANOVA, D. R. Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints. In: **International Conference on Machine Learning (ICML)**, 42., 2025\. Disponível em: https://arxiv.org/abs/2503.01747. Acesso em: 11 set. 2026\.

COLLOT, S.; FRASER, C.; ZHAO, J.; SHEN, W. F.; WILLI, T.; LEONTIADIS, I. Balanced Accuracy: The Right Metric for Evaluating LLM Judges — Explained through Youden's J statistic. In: **Conference of the European Chapter of the Association for Computational Linguistics (EACL): Industry Track**, Rabat, Marrocos, 2026\. p. 927-936\. Disponível em: https://aclanthology.org/2026.eacl-industry.69/. Acesso em: 11 set. 2026\.

CORRÊA, N. K.; FALK, S.; FATIMAH, S.; SEN, A.; OLIVEIRA, N. de. TeenyTinyLlama: Open-Source Tiny Language Models Trained in Brazilian Portuguese. **Machine Learning with Applications**, v. 16, art. 100558, 2024\. Disponível em: https://arxiv.org/abs/2401.16640. Acesso em: 11 set. 2026\.

CORRÊA, N. K.; SEN, A.; FATIMAH, S.; FALK, S.; LANDGRAF, L.; KASTNER, J.; FLEK, L. Tucano 2 Cool: Better Open Source LLMs for Portuguese. **arXiv preprint**, 2026\. Disponível em: https://arxiv.org/abs/2603.03543. Acesso em: 11 set. 2026\.

CUCONASU, F.; TRAPPOLINI, G.; SICILIANO, F.; FILICE, S.; CAMPAGNANO, C.; MAAREK, Y.; TONELLOTTO, N.; SILVESTRI, F. The Power of Noise: Redefining Retrieval for RAG Systems. In: **International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR)**, 47., Washington, DC. Nova York: ACM, 2024\. p. 719-729\. Disponível em: https://arxiv.org/abs/2401.14887. Acesso em: 11 set. 2026\.

DUTTA, A.; KRISHNAN, S.; KWATRA, N.; RAMJEE, R. Accuracy is Not All You Need. In: **Advances in Neural Information Processing Systems (NeurIPS)**, 37., 2024\. Disponível em: https://arxiv.org/abs/2407.09141. Acesso em: 11 set. 2026\.

FACELI, K.; LORENA, A. C.; GAMA, J.; ALMEIDA, T. A.; CARVALHO, A. C. P. L. F. **Inteligência Artificial: uma abordagem de aprendizado de máquina**. 3\. ed. Rio de Janeiro: LTC, 2025\. Disponível em: https://www.grupogen.com.br/livro-inteligencia-artificial-uma-abordagem-de-aprendizado-de-maquina-katti-faceli-ana-carolina-lorena-joao-gama-tiago-a-de-almeida-e-andre-c-p-l-f-de-carvalho-editora-ltc-9788521639206. Acesso em: 11 set. 2026\.

GARCÍA, S.; HERRERA, F. An Extension on "Statistical Comparisons of Classifiers over Multiple Data Sets" for all Pairwise Comparisons. **Journal of Machine Learning Research**, v. 9, p. 2677-2694, 2008\. Disponível em: https://www.jmlr.org/papers/volume9/garcia08a/garcia08a.pdf. Acesso em: 11 set. 2026\.

JOSEPH, R. N. Beyond LLM-Based Test Automation: A Zero-Cost Self-Healing Approach Using DOM Accessibility Tree Extraction. **Preprint**, mar. 2026\. Disponível em: https://arxiv.org/abs/2603.20358. Acesso em: 11 set. 2026\.

JÚNIOR, E.; VALEJO, A. D. B.; VALVERDE-REBAZA, J.; NEVES, V. GenIA-E2ETest: A Generative AI-Based Approach for End-to-End Test Automation. In: **Simpósio Brasileiro de Engenharia de Software (SBES)**, Recife, PE, set. 2025\.

KULIGOWSKI, A. Chat History and Embedding Truncation Happens Silently with No User-Visible Indication. **Issue n. 14259, repositório ollama/ollama, GitHub**, fev. 2026\. Disponível em: https://github.com/ollama/ollama/issues/14259. Acesso em: 11 set. 2026\.

LIU, N. F.; LIN, K.; HEWITT, J.; PARANJAPE, A.; BEVILACQUA, M.; PETRONI, F.; LIANG, P. Lost in the Middle: How Language Models Use Long Contexts. **Transactions of the Association for Computational Linguistics**, v. 12, p. 157-173, 2024\. Disponível em: https://aclanthology.org/2024.tacl-1.9/. Acesso em: 11 set. 2026\.

MACIAK, T. et al. **Automated contract testing: How to detect API drift before it reaches production**. Medium, 2026\.

OPITZ, J. A Closer Look at Classification Evaluation Metrics and a Critical Reflection of Common Evaluation Practice. **Transactions of the Association for Computational Linguistics**, v. 12, p. 820-836, 2024\. Disponível em: https://aclanthology.org/2024.tacl-1.46/. Acesso em: 11 set. 2026\.

SCLAR, M.; CHOI, Y.; TSVETKOV, Y.; SUHR, A. Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I Learned to Start Worrying about Prompt Formatting. In: **International Conference on Learning Representations (ICLR)**, 12., Viena, 2024\. Disponível em: https://arxiv.org/abs/2310.11324. Acesso em: 11 set. 2026\.

SHI, X.; LI, Z.; CHEN, A. R. Enhancing LLM-based Fault Localization with a Functionality-Aware Retrieval-Augmented Generation Framework. **arXiv preprint**, 2025\.

SUZGUN, M.; YUKSEKGONUL, M.; BIANCHI, F.; JURAFSKY, D.; ZOU, J. Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory. **arXiv preprint**, 2025\. Disponível em: https://arxiv.org/abs/2504.07952. Acesso em: 11 set. 2026\.

WU, K.; WU, E.; ZOU, J. ClashEval: Quantifying the Tug-of-War Between an LLM's Internal Prior and External Evidence. In: **Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track**, 37., 2024\. Disponível em: https://arxiv.org/abs/2404.10198. Acesso em: 11 set. 2026\.

ZHANG, G.; JIANG, W.; WANG, X.; BEHR, A.; ZHAO, K.; FRIEDMAN, J.; CHU, X.; ANOUN, A. Adaptive Memory Admission Control for LLM Agents. **arXiv preprint**, 2026\. Disponível em: https://arxiv.org/abs/2603.04549. Acesso em: 11 set. 2026\.

ZHANG, J. et al. Prune4Web: DOM Tree Pruning Programming for Web Agent. In: **AAAI Conference on Artificial Intelligence**, 2026\.

ZOU, W.; GENG, R.; WANG, B.; JIA, J. PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models. In: **USENIX Security Symposium**, 34., Seattle, 2025\. p. 3827-3844\. Disponível em: https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag. Acesso em: 11 set. 2026\.

# **GLOSSÁRIO**

<!-- ! Alteração de IA - Revisar: removida a entrada "Ngrok"; ajustada a de "FastAPI"; acrescentadas as entradas Accessibility Tree, Attention Dilution, DOM Pruning, MTTR, Ollama, Quantização, RAG e Task Success.
     ! Motivo: o Ngrok deixou de ser usado com a inferência local (seção 3.3), e sua definição original ainda descrevia o túnel na direção oposta à que o texto propunha. Os termos acrescentados já eram empregados no corpo do trabalho sem constar do glossário. -->

<!-- ! Alteração de IA - Revisar: acrescentadas as entradas "Acurácia Balanceada", "Época (Fase 3)", "Fertilidade (tokens por palavra)" e "Tokenização", em ordem alfabética.
     ! Motivo: os quatro termos passaram a ser usados nas seções 2.4, 3.2 e 3.4 sem definição no glossário — o mesmo defeito que motivou a inclusão dos oito termos da revisão anterior. A entrada "Época" leva a etapa entre parênteses porque, fora da Fase 3, a palavra designa em aprendizado de máquina a passagem completa pelo conjunto de treinamento com atualização dos pesos do modelo, e aqui nenhum peso é atualizado: o que muda de uma época para a outra é o texto da base de conhecimento. -->

**Accessibility Tree (Árvore de Acessibilidade):** Estrutura derivada do DOM que expõe apenas a semântica dos elementos de uma página — seu papel (*role*), nome acessível e valor —, originalmente destinada a tecnologias assistivas. Por ser consideravelmente menor que a árvore HTML completa, é utilizada neste trabalho como base para a filtragem de contexto.  
**Acurácia Balanceada:** Média das revocações obtidas em cada classe, isto é, da proporção de acertos dentro de cada classe verdadeira, com o mesmo peso para todas elas. Diferentemente da acurácia simples, não é inflada quando o modelo passa a responder sempre o rótulo mais frequente, razão pela qual é adotada como métrica primária de comparação na Fase 3.  
**API (Application Programming Interface):** Conjunto de definições e protocolos padronizados que permite a comunicação e a troca de dados entre diferentes sistemas de software.  
**Attention Dilution (Diluição de Atenção):** Degradação da capacidade de raciocínio de um modelo de linguagem quando seu contexto é preenchido por grande volume de informação pouco relevante, dispersando a atenção do modelo em relação aos dados que de fato importam para a tarefa.  
**Contract Drift (Deriva de Contrato):** Alteração silenciosa ou não documentada na estrutura dos dados retornados por uma API (como a mudança de um tipo numérico para texto), quebrando as expectativas do cliente (interface) que consome esses dados.  
**DOM (Document Object Model):** Representação estruturada em forma de árvore do conteúdo de um documento HTML, utilizada pelos navegadores web para renderizar páginas e permitir interações via scripts.  
**DOM Pruning (Poda de Árvore):** Técnica de redução de contexto que descarta, antes do envio ao modelo de linguagem, os nós da árvore de elementos que não são relevantes para a tarefa em análise, preservando os elementos interativos e o caminho até o elemento de interesse.  
**End-to-End (E2E):** Abordagem de teste de software que valida o fluxo completo de uma aplicação, de ponta a ponta, simulando o comportamento de um usuário real desde a interface gráfica até a camada de banco de dados.  
**Época (Fase 3):** Cada passagem completa do conjunto de casos pelo agente durante a Fase 3, ao final da qual as edições aprovadas pela conferência em código são consolidadas em uma nova cópia da base de conhecimento. A cópia de cada época é preservada, de modo que o desempenho possa ser lido ao longo do ciclo e não apenas no final. Não há atualização dos pesos do modelo entre épocas: o que muda é o texto da base.  
**FastAPI:** Framework web moderno e de alto desempenho, utilizado na linguagem Python para a construção de APIs. Neste trabalho, é empregado na construção da API da aplicação-alvo submetida aos testes.  
**Fertilidade (tokens por palavra):** Razão entre o número de tokens produzidos pelo tokenizador e o número de palavras do texto original. Quanto maior a fertilidade, mais caro em contexto e em tempo de processamento fica o mesmo texto; para os tokenizadores de uso corrente ela é sistematicamente maior em português do que em inglês.  
**Fuzzing:** Técnica de teste de software que envolve fornecer dados inválidos, inesperados ou aleatórios como entrada para um sistema, a fim de expor vulnerabilidades, falhas de validação ou exceções não tratadas.  
**LLM (Large Language Model \- Modelo de Linguagem Grande):** Modelo avançado de inteligência artificial treinado em vastas quantidades de texto, capaz de compreender o contexto, raciocinar e gerar linguagem natural e código de programação estruturado.  
**MTTR (Mean Time To Repair \- Tempo Médio de Reparo):** Métrica que expressa o intervalo médio entre a detecção de uma falha e a restauração verificada do funcionamento. Neste trabalho, é medido entre a detecção da falha pelo agente e a validação bem-sucedida da correção proposta.  
**Ollama:** Runtime de código aberto para execução local de modelos de linguagem, responsável por gerenciar o download, o carregamento e a inferência dos modelos na própria máquina do usuário, sem dependência de serviços em nuvem.  
**Playwright / Cypress:** Frameworks modernos de automação de testes para aplicações web. Ambos permitem a simulação robusta de interações de usuários e possuem capacidades nativas de interceptação de tráfego de rede no navegador.  
**QA (Quality Assurance \- Garantia de Qualidade):** Conjunto de atividades preventivas e processos de engenharia de software focados em garantir que a aplicação atenda aos requisitos especificados e aos padrões operacionais antes do lançamento em produção.  
**Quantização:** Técnica de compressão de modelos de linguagem que reduz a precisão numérica de seus pesos, diminuindo significativamente o consumo de memória e viabilizando a inferência em hardware modesto, ao custo de uma perda controlada de precisão.  
**Qwen2.5-Coder:** Variante de modelo de linguagem de código aberto otimizada especificamente para tarefas de programação, tradução de sintaxe, depuração e raciocínio lógico voltado para software.  
**RAG (Retrieval-Augmented Generation \- Geração Aumentada por Recuperação):** Técnica em que se recupera, de uma base de conhecimento externa, apenas o material pertinente à pergunta em questão, fornecendo-o ao modelo de linguagem junto à solicitação, em vez de depender exclusivamente do conhecimento internalizado durante o treinamento.  
**Self-Healing (Autocura):** Capacidade intrínseca de um sistema distribuído, ou de um script de automação, de detectar ativamente falhas de execução em tempo real e aplicar correções estruturais autonomamente para continuar operando sem interrupções.  
**Task Success (Sucesso da Tarefa):** Métrica que expressa a proporção de cenários de falha em que o agente restaurou o fluxo de execução e o roteiro de teste concluiu sem erro, sobre o total de cenários submetidos.  
**Tokenização:** Conversão do texto em unidades discretas — os tokens — antes de qualquer processamento pelo modelo de linguagem. É a unidade em que se contam a janela de contexto e o custo de cada inferência, e sua correspondência com caracteres ou palavras varia conforme o idioma e o tokenizador empregado.