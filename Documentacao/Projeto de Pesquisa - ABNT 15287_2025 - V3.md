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

A transição de sistemas baseados em regras estritas para sistemas adaptativos (como os testes com *Self-Healing*) encontra sua base teórica no aprendizado de máquina. Segundo Faceli et al. (2021), os algoritmos de aprendizado de máquina permitem que sistemas computacionais extraiam padrões intrínsecos a partir de dados para a tomada de decisão autônoma, superando as limitações da programação puramente determinística. Ao invés de falhar imediatamente ante uma mudança no DOM, o sistema dotado de inteligência artificial utiliza o reconhecimento de padrões para inferir a intenção original do teste e sugerir a correção.

## **2.3 Automação E2E e Inteligência Artificial**

Estudos recentes, como o GenIA-E2ETest (JÚNIOR et al., 2025), compõem a base metodológica que atesta a eficácia dos LLMs (Modelos de Linguagem Grandes) na interpretação de intenções textuais e tradução para comandos automatizados de interação de elementos de interface. A implementação do Playwright Healer Agent (BISWAS, 2026\) sustenta o diferencial arquitetural deste trabalho, validando que a interceptação do tráfego de rede aliada à IA mitiga drasticamente os falsos-positivos.

## **2.4 Gestão de Context Window em LLMs**

A literatura comprova que sobrecarregar a memória de contexto (Context Window) dos LLMs com códigos HTML puros degrada seu raciocínio lógico, um fenômeno conhecido como Attention Dilution. Metodologias focadas em podar e limpar a árvore de elementos antes do processamento, como o Prune4Web (ZHANG et al., 2026), formam a espinha dorsal das técnicas de filtragem utilizadas neste projeto para viabilizar inferências precisas com custo computacional reduzido.

<!-- ! Alteração de IA - Revisar: acrescentado o parágrafo abaixo, citando JOSEPH (2026) e fixando sobre qual estrutura a poda é aplicada.
     ! Motivo: JOSEPH constava nas REFERÊNCIAS sem ser citado no corpo (o que contraria a NBR 6023, segundo a qual a lista contém apenas obras citadas), e o texto original nomeava dois artefatos — "extração da árvore de acessibilidade" e "heurísticas de DOM Pruning" — sem nunca dizer se a poda incide sobre o DOM bruto ou sobre a árvore de acessibilidade, o que deixaria a implementação sem critério. -->

Complementarmente, Joseph (2026) demonstra que a extração da árvore de acessibilidade (*Accessibility Tree*) constitui, por si só, uma estratégia de redução de contexto de baixo custo, por expor apenas a projeção semântica dos elementos — seu papel (*role*), nome acessível e valor — em vez da árvore HTML completa. Este projeto adota essa abordagem como substrato: a poda é aplicada **sobre a árvore de acessibilidade**, e não sobre o DOM bruto, que passa a ser consultado apenas pontualmente, durante a resolução de um localizador na etapa de autocura.

## **2.5 Detecção de Quebra de Contrato de API**

<!-- ! Alteração de IA - Revisar: subseção nova, citando MACIAK et al. (2026).
     ! Motivo: a referência constava na lista sem citação no corpo, e o Contract Drift — que é o objeto central do trabalho — não tinha nenhuma subseção própria no referencial, aparecendo apenas como definição solta na introdução e no glossário. -->

A verificação automatizada de contratos entre cliente e servidor é discutida por Maciak et al. (2026), que caracterizam a deriva de contrato (*API drift*) como uma classe de falha que escapa aos testes unitários de cada lado isoladamente, por se manifestar apenas na fronteira de integração. Os autores destacam que alterações silenciosas de tipo, remoção de campos e renomeações são detectáveis por comparação estrutural da resposta observada contra o contrato esperado — princípio que fundamenta o gatilho de erro adotado neste projeto, no qual a interceptação de rede compara a forma (chaves e tipos) do dado recebido com a esperada pela interface consumidora.

## **2.6 Recuperação de Conhecimento Prévio Aplicada à Localização de Falhas**

<!-- ! Alteração de IA - Revisar: subseção nova, citando SHI, LI e CHEN (2025).
     ! Motivo: a referência sobre RAG constava na lista sem nenhuma citação no corpo, e a arquitetura implementada inclui uma base de conhecimento consultada pelo modelo — sem esta subseção, esse componente ficaria sem fundamentação teórica no documento. -->

Shi, Li e Chen (2025) demonstram que a Geração Aumentada por Recuperação (*Retrieval-Augmented Generation* \- RAG), quando sensível à funcionalidade do trecho analisado, melhora a localização de falhas por LLMs ao fornecer ao modelo apenas o conhecimento pertinente ao defeito em questão, em vez de ampliar indiscriminadamente o contexto. Neste trabalho, o princípio é aplicado por meio de uma base de conhecimento curada sobre a aplicação-alvo — organizada por módulo e por entidade de negócio, e contendo regras de negócio e defeitos previamente conhecidos — recuperada seletivamente no momento do diagnóstico.

Cabe ressaltar que essa base é **estática e construída previamente**, de forma análoga ao conhecimento acumulado por um analista de QA sobre o sistema que testa. Ela não implica inspeção da lógica interna do servidor em tempo de execução, preservando a delimitação de escopo estabelecida na seção 1.2.

# **3 METODOLOGIA**

A pesquisa caracteriza-se como um projeto prático e aplicado (Pesquisa-Ação), voltado para a construção e validação de uma arquitetura de software escalável. A infraestrutura baseia-se nas seguintes camadas:

## **3.1 Infraestrutura e Orquestração Local**

A ferramenta principal de orquestração será o Playwright (com Node.js/Python). O Playwright comunica-se com o navegador via protocolos nativos e possui suporte embutido para interceptação e modificação de chamadas de rede em tempo real. Isso permite extrair a árvore de acessibilidade do DOM e escutar os códigos de status HTTP em segundo plano. Como contingência, o framework Cypress poderá ser acionado caso ocorram incompatibilidades críticas.

## **3.2 Inteligência Artificial e Processamento LLM**

<!-- ! Alteração de IA - Revisar: seção reescrita — a inferência sai do Google Colab (GPU T4) e passa a ser executada localmente via Ollama, com o modelo quantizado.
     ! Motivo: a dependência de nuvem contradizia o próprio problema de pesquisa (seção 1.2), que pergunta como operar "sob restrições de hardware local"; além disso, exigir configuração de Colab e túnel de rede inviabilizaria o uso da ferramenta fora do ambiente universitário. A execução local torna a resposta à pergunta de pesquisa direta, em vez de contornada. -->

O processamento semântico utilizará o modelo Qwen2.5-Coder em variante quantizada, executado **integralmente na máquina local** por meio do runtime Ollama. A quantização reduz a precisão numérica dos pesos do modelo, diminuindo o consumo de memória a ponto de viabilizar a inferência em CPU, sem GPU dedicada.

A escolha do porte do modelo (1,5B, 3B ou 7B de parâmetros) será definida experimentalmente, por comparação entre as variantes sob o mesmo hardware, considerando latência por inferência, pico de memória e qualidade do diagnóstico produzido. Adota-se como critério o **menor modelo que atenda à tarefa**, e não o maior que couber na máquina, uma vez que o agente compete por memória com o navegador automatizado, o servidor de aplicação e o banco de dados da aplicação-alvo durante a execução dos testes.

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

BISWAS, S. Enhancing End-to-End Test Stability Through AI-Assisted Self-Healing: A Case Study of Playwright Healer Agent Implementation. **International Journal of Scientific Engineering and Research**, v. 14, n. 1, p. 1-12, jan. 2026\.

FACELI, K.; LORENA, A. C.; GAMA, J.; ALMEIDA, T. A.; CARVALHO, A. C. P. L. F. **Inteligência Artificial: uma abordagem de aprendizado de máquina**. 2\. ed. Rio de Janeiro: LTC, 2021\.

JOSEPH, R. N. Beyond LLM-Based Test Automation: A Zero-Cost Self-Healing Approach Using DOM Accessibility Tree Extraction. **Preprint**, mar. 2026\.

JÚNIOR, E.; VALEJO, A. D. B.; VALVERDE-REBAZA, J.; NEVES, V. GenIA-E2ETest: A Generative AI-Based Approach for End-to-End Test Automation. In: **Simpósio Brasileiro de Engenharia de Software (SBES)**, Recife, PE, set. 2025\.

MACIAK, T. et al. **Automated contract testing: How to detect API drift before it reaches production**. Medium, 2026\.

SHI, X.; LI, Z.; CHEN, A. R. Enhancing LLM-based Fault Localization with a Functionality-Aware Retrieval-Augmented Generation Framework. **arXiv preprint**, 2025\.

ZHANG, J. et al. Prune4Web: DOM Tree Pruning Programming for Web Agent. In: **AAAI Conference on Artificial Intelligence**, 2026\.

# **GLOSSÁRIO**

<!-- ! Alteração de IA - Revisar: removida a entrada "Ngrok"; ajustada a de "FastAPI"; acrescentadas as entradas Accessibility Tree, Attention Dilution, DOM Pruning, MTTR, Ollama, Quantização, RAG e Task Success.
     ! Motivo: o Ngrok deixou de ser usado com a inferência local (seção 3.3), e sua definição original ainda descrevia o túnel na direção oposta à que o texto propunha. Os termos acrescentados já eram empregados no corpo do trabalho sem constar do glossário. -->

**Accessibility Tree (Árvore de Acessibilidade):** Estrutura derivada do DOM que expõe apenas a semântica dos elementos de uma página — seu papel (*role*), nome acessível e valor —, originalmente destinada a tecnologias assistivas. Por ser consideravelmente menor que a árvore HTML completa, é utilizada neste trabalho como base para a filtragem de contexto.  
**API (Application Programming Interface):** Conjunto de definições e protocolos padronizados que permite a comunicação e a troca de dados entre diferentes sistemas de software.  
**Attention Dilution (Diluição de Atenção):** Degradação da capacidade de raciocínio de um modelo de linguagem quando seu contexto é preenchido por grande volume de informação pouco relevante, dispersando a atenção do modelo em relação aos dados que de fato importam para a tarefa.  
**Contract Drift (Deriva de Contrato):** Alteração silenciosa ou não documentada na estrutura dos dados retornados por uma API (como a mudança de um tipo numérico para texto), quebrando as expectativas do cliente (interface) que consome esses dados.  
**DOM (Document Object Model):** Representação estruturada em forma de árvore do conteúdo de um documento HTML, utilizada pelos navegadores web para renderizar páginas e permitir interações via scripts.  
**DOM Pruning (Poda de Árvore):** Técnica de redução de contexto que descarta, antes do envio ao modelo de linguagem, os nós da árvore de elementos que não são relevantes para a tarefa em análise, preservando os elementos interativos e o caminho até o elemento de interesse.  
**End-to-End (E2E):** Abordagem de teste de software que valida o fluxo completo de uma aplicação, de ponta a ponta, simulando o comportamento de um usuário real desde a interface gráfica até a camada de banco de dados.  
**FastAPI:** Framework web moderno e de alto desempenho, utilizado na linguagem Python para a construção de APIs. Neste trabalho, é empregado na construção da API da aplicação-alvo submetida aos testes.  
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