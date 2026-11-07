<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): a leitura do syllabus CTFL 4.0 do ISTQB, na tradução do BSTQB, contra o projeto (parte 2 do pedido do Eric), com as citações literais e a página de cada uma. É um dos arquivos de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15 (subseção 6.15.6).
     ! Motivo: o professor subiu o PDF ao repositório da disciplina em 06/11/2026 e o Eric pediu para validar se o projeto está nos parâmetros do syllabus e se é teste de ponta a ponta de fato, com o documento entrando como referência e bibliografia do TCC. As páginas foram localizadas por busca da frase citada no texto extraído do PDF (PyMuPDF), conferidas contra o rodapé "Página N de 66"; nada foi citado de memória. -->
# O projeto contra o syllabus CTFL 4.0 do ISTQB, na tradução do BSTQB

Leitura feita em 7 nov. 2026 pelo Claude, na sessão principal, sobre o PDF que o orientador subiu em 06/11/2026 ao repositório da disciplina (`TCC/syllabus_ctfl_4.0br.pdf`, commit `f469ecd`). O texto foi extraído com PyMuPDF; as páginas citadas são as do rodapé do PDF ("Página N de 66"), localizadas por busca da frase citada no texto extraído. Nas citações, a hifenização de quebra de linha do PDF foi desfeita e nada mais mudou; dois deslizes da tradução ("Uma equívoco", "Os Teste de Regressão") ficam como estão na fonte. O documento é a versão 4.0 do syllabus, com data de lançamento 21/04/2023 em todas as páginas, na tradução do BSTQB revisada em 29/02/2024 (correção de erros gramaticais), 28/06/2024 (adequação visual) e 06/01/2025 (adequação ao novo padrão visual do ISTQB), segundo o histórico da página 3.

Referência: ISTQB. **Certified Tester Foundation Level (CTFL) Syllabus**: versão 4.0. Tradução: BSTQB. [S. l.]: International Software Testing Qualifications Board, 2023. 66 p. Versão de lançamento de 21 abr. 2023; tradução revisada em 6 jan. 2025. Disponível em: https://bstqb.qa/. Acesso em: 7 nov. 2026. (Em 7 nov. 2026 o endereço antigo `bstqb.org.br/b9/sobre-ctfl`, que a comunidade cita como a página de download, redirecionava para `bstqb.qa`, cuja página inicial não traz o link do PDF; conferir a página de download antes da versão final do TCC. O original em inglês, versão 4.0.1 de 2024, está no site do ISTQB em `www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf`, endereço visto só em resultado de busca e não aberto nesta leitura.)

## 1 As perguntas do Eric

Duas: o projeto está dentro dos parâmetros e dos métodos do syllabus? E é de fato teste de ponta a ponta (E2E)? Depois: o que o syllabus pede e o projeto não tem, para entrar; e como citar o documento no TCC.

## 2 O que o syllabus diz, seção a seção

### 2.1 O que é teste, e teste contra depuração (seção 1.1, p. 14 e 15)

"O teste de software é um conjunto de atividades para descobrir defeitos e avaliar a qualidade dos artefatos de software. Esses artefatos, quando estão sendo testados, são conhecidos como objetos de teste." O syllabus avisa contra a ideia de que testar "consistem apenas na execução de testes (ou seja, executar o software e verificar os resultados dos testes)" e separa verificação de validação: "verificar se o sistema atende aos requisitos especificados" e "checar se o sistema atende às necessidades dos usuários". O objetivo de aprendizagem FL-1.1.2 é "Diferenciar teste de depuração" (p. 13), e a seção 1.1.2 diz: "O teste e a depuração são atividades distintas." e "Quando o teste dinâmico (ver capítulo 4) aciona uma falha, a depuração se preocupa em encontrar as causas dessa falha (defeitos), analisar essas causas e eliminá-las." O processo de depuração descrito é "Reproduzir uma falha", "Diagnosticar (encontrar a causa principal)" e "Corrigir a causa", e "O teste de confirmação subsequente verifica se as correções resolveram o problema." (p. 15).

No projeto: o agente roda os roteiros e compara o que vê com o contrato e com a referência em modo normal (verificação); não valida necessidades de usuário. O diagnóstico do agente (a causa entre as 23 da taxonomia) é a etapa "Diagnosticar" da depuração, feita em apoio a quem corrige; a cura de localizador é "Corrigir a causa" só no testware; e a reexecução depois da cura é o teste de confirmação. O TCC deve dizer isso com essas palavras: o agente testa e apoia a depuração.

### 2.2 Erro, defeito, falha e causa-raiz (seção 1.2.3, p. 16)

"Se um defeito no código for executado, o sistema poderá deixar de fazer o que deveria fazer ou fazer algo que não deveria, causando uma falha." E: "Uma causa-raiz é um motivo fundamental para a ocorrência de um problema (p. ex., uma situação que leva a um erro). As causas-raiz são identificadas por meio da análise de causa-raiz, que normalmente é realizada quando ocorre uma falha ou quando um defeito é identificado."

No projeto: o agente observa a falha na tela, localiza o defeito na resposta da API (o desvio do contrato ou da referência) e nomeia uma causa entre 23 categorias. A "causa raiz" do projeto é mais estreita que a do syllabus: é a categoria do defeito observado, não o motivo fundamental (que pode ser humano ou de processo). O TCC passa a usar os três termos no sentido do syllabus e declara essa diferença no glossário.

### 2.3 Os sete princípios (seção 1.3, p. 16)

"O teste mostra a presença, não a ausência de defeitos. Os testes podem mostrar que os defeitos estão presentes no objeto de teste, mas não podem provar que não há defeitos (Buxton 1970)." e "Testes exaustivos são impossíveis. Testar tudo não é viável, exceto em casos triviais (Manna 1978)."

No projeto: o relatório por caso diz o que o agente encontrou e nunca que "não há defeitos"; os dez cenários da Fase 5 e os 72 casos de avaliação são uma amostra, e o TCC já declara isso como limitação.

### 2.4 Atividades de teste: execução, comparação, registro e análise das anomalias (seção 1.4.1, p. 17)

"A Execução do Teste inclui a execução dos testes de acordo com o cronograma de execução ("rodar" o teste). A execução do teste pode ser manual ou automatizada." e "Os resultados reais dos testes são comparados com os resultados esperados. Os resultados do teste são registrados. As anomalias são analisadas para identificar suas causas prováveis. Essa análise nos permite relatar as anomalias com base nas falhas observadas (ver seção 5.5)."

No projeto: é o laço do agente, na ordem do syllabus: rodar o roteiro (Playwright), comparar o real com o esperado (contrato e referência em modo normal), registrar (a trilha v2), analisar as causas prováveis (o diagnóstico, com a causa escolhida e as alternativas) e relatar (o relatório por caso, que a seção 5.5 molda).

### 2.5 Testware (seção 1.4.3, p. 18)

"O testware é criado como produto de trabalho de saída das atividades de teste descritas na seção 1.4.1."

No projeto: roteiros, localizadores, cenários, contratos, a biblioteca de verbetes e a trilha são testware. A cura de localizador (Fase 4, pacote P4) é manutenção automatizada do testware: quando o localizador de um passo quebra, o código acha outro e o roteiro passa de novo.

### 2.6 Níveis de teste (seção 2.2.1, p. 26)

"O Teste de Sistema concentra-se no comportamento geral e nos recursos de todo um sistema ou produto, geralmente incluindo o teste funcional de tarefas de ponta a ponta e o teste não funcional de características de qualidade." e "O Teste de Integração de Sistema concentra-se no teste das interfaces do sistema e de outros sistemas e serviços externos. O teste de integração do sistema requer ambientes de teste adequados, de preferência semelhantes ao ambiente operacional."

No projeto: "E2E" não é um nível de teste no syllabus; "tarefas de ponta a ponta" é o conteúdo funcional do Teste de Sistema. O agente percorre a tarefa inteira (abrir a página, listar, abrir o detalhe, entrar, reservar), do front PHP, pela API, até o banco, e a fronteira entre o front e a API é o objeto que ele mais examina: nível de sistema, com conteúdo de integração de sistema (duas aplicações e o banco). O ambiente é o das cobaias reais, levantado nesta máquina.

### 2.7 Tipos de teste (seção 2.2.2, p. 27)

"O Teste Caixa-Preta (ver seção 4.2) é baseado em especificações e deriva testes da documentação externa ao objeto de teste. O principal objetivo do teste caixa-preta é verificar o comportamento do sistema em relação às suas especificações." E sobre os não funcionais: "Muitos testes não funcionais são derivados de testes funcionais, pois usam os mesmos testes funcionais, mas verificam se, ao executar a função, uma restrição não funcional é atendida (p. ex., verificar se uma função é executada dentro de um tempo especificado ou se uma função pode ser portada para uma nova plataforma)."

No projeto: os contratos (esquemas da API) são a especificação, e o agente não lê o código das cobaias: teste funcional, caixa-preta. O sinal "tempo acima do orçamento" do caso ao vivo é um teste não funcional derivado do funcional, exatamente como o exemplo do syllabus.

### 2.8 Teste de confirmação, teste de regressão e análise de impacto (seções 2.2.3 e 2.3, p. 28)

"Os Teste de Regressão confirmam que nenhuma consequência adversa foi causada por uma alteração, inclusive uma correção que já tenha sido confirmada após o teste." e "É aconselhável realizar primeiro uma análise de impacto para otimizar a extensão do teste de regressão. A análise de impacto mostra quais partes do software podem ser afetadas." e "os testes de regressão são fortes candidatos à automação. A automação desses testes deve começar no início do projeto." Na manutenção (2.3): "A análise de impacto pode ser feita antes de uma alteração, para ajudar a decidir se a alteração deve ser feita, com base nas possíveis consequências em outras áreas do sistema."

No projeto: os cenários da Fase 5 são testes de regressão automatizados sobre as cobaias; a reexecução depois da cura é teste de confirmação; e a integração com o Git (pacote Q7 do plano da Pós-Fase 4) é a análise de impacto que o syllabus manda fazer antes da regressão: o diff do commit, cruzado com os arquivos e endpoints declarados nos verbetes, diz que cenários rodar.

### 2.9 Pirâmide e quadrantes de teste (seções 5.1.6 e 5.1.7, p. 45)

"A camada superior representa testes complexos, de alto nível e de ponta a ponta. Esses testes de alto nível geralmente são mais lentos do que os testes das camadas inferiores e, normalmente, verificam uma grande parte da funcionalidade, de modo que, em geral, são necessários apenas alguns deles para obter uma cobertura razoável." e "Outro modelo popular define testes de unidade (componente), testes de integração (integração de componente) e testes de ponta a ponta." Sobre os quadrantes: "Os quadrantes de teste, definidos por Brian Marick (Marick 2003, Crispin 2008), agrupam os níveis de teste com os tipos de teste, as atividades, as técnicas de teste e os produtos de trabalho apropriados no desenvolvimento ágil de software."

No projeto: o agente está no topo da pirâmide: poucos testes (dez cenários), lentos (minutos por cenário, com o modelo em CPU), cobertura larga (a tarefa inteira). É isso que explica, no TCC, por que o número de cenários é pequeno e por que o tempo até o resultado se mede em minutos; e é a segunda passagem do syllabus em que "ponta a ponta" nomeia o que o agente faz.

### 2.10 Relatório de defeitos (seção 5.5, p. 50 e 51)

"Um relatório de defeitos registrado durante um teste dinâmico normalmente possui: Um identificador exclusivo; Um título com um breve resumo da anomalia que está sendo relatada; A data em que a anomalia foi observada, a organização emissora e o autor, incluindo seu cargo; A identificação do objeto de teste e do ambiente de teste; O contexto do defeito (p. ex., caso de teste que está sendo executado, atividade de teste que está sendo realizada, fase do SDLC e outras informações relevantes, como a técnica de teste, a lista de verificação ou os dados de teste que estão sendo usados); A descrição da falha para permitir a reprodução e a resolução, incluindo as etapas que detectaram a anomalia e todos os registros de teste relevantes, despejos de banco de dados, capturas de tela ou gravações; Os resultados esperados e os resultados reais; A severidade do defeito (grau de impacto) nos interesses dos stakeholders ou nos requisitos; A prioridade de correção; O status do defeito (p. ex., aberto, adiado, duplicado, aguardando correção, aguardando teste de confirmação, reaberto, fechado, rejeitado); As referências (p. ex., ao caso de teste)." E: "Alguns desses dados podem ser incluídos automaticamente ao usar ferramentas de gerenciamento de defeitos (p. ex., identificador, data, autor e status inicial). Modelos de documentos para um relatório de defeitos e exemplos de relatórios de defeitos podem ser encontrados na norma ISO/IEC/IEEE 29119-3".

No projeto: o relatório v2 por caso tem seis seções fixas (veredito, evidência, contraste com a segunda causa, FONTE declarada e conferida, linha de ação, árvore) e não tem metade desses campos. É o que a decisão 104 adota como esqueleto do relatório v3 (tabela na seção 4).

### 2.11 Ferramentas e os riscos da automação (seções 6.1 e 6.2, p. 53 e 54)

Entre as ferramentas da 6.1: "Ferramentas de gerenciamento: aumentam a eficiência do processo de teste, facilitando o gerenciamento do SDLC, dos requisitos, dos testes, dos defeitos e da configuração" e "Ferramentas de execução e cobertura de testes: facilitam a execução de testes automatizados e a medição da cobertura". Entre os riscos da 6.2: "Expectativas irreais sobre os benefícios de uma ferramenta (incluindo funcionalidade e facilidade de uso)"; "Estimativas imprecisas de tempo, custos e esforço necessários para introduzir uma ferramenta, manter scripts de teste e alterar o processo de teste manual existente"; "Usar uma ferramenta de teste quando o teste manual é mais apropriado"; "Confiar demais em uma ferramenta, por exemplo, ignorando a necessidade do pensamento crítico humano"; e "Usar um software de código aberto que pode ser abandonado".

No projeto: o agente é uma ferramenta de execução (roda os roteiros) e de gerenciamento de defeitos (produz o relatório). Dos riscos, três já têm resposta no desenho: manter scripts de teste é o que a cura de localizador ataca; "confiar demais em uma ferramenta" é o motivo do princípio "a IA nunca aprova sozinha" e da revisão humana (decisão 95); e a dependência de código aberto (Ollama, Playwright, qwen2.5:7b) fica declarada no TCC com as versões fixadas. A Fase 5 responde ao risco das "estimativas imprecisas" medindo o tempo do agente contra a linha de base manual.

## 3 Onde o projeto cabe

| Dimensão do syllabus | O projeto | Seção e página |
|---|---|---|
| Nível de teste | sistema e integração de sistema: front PHP, API e banco, com a fronteira front e API como objeto principal | 2.2.1, p. 26 |
| Conteúdo | tarefas de ponta a ponta: abrir a página, listar, abrir o detalhe, entrar, reservar | 2.2.1, p. 26; 5.1.6, p. 45 |
| Tipo | funcional, caixa-preta, baseado em especificação (os contratos); o tempo acima do orçamento é um teste não funcional derivado do funcional | 2.2.2, p. 27 |
| Confirmação e regressão | reexecução depois da cura (confirmação); cenários da Fase 5 (regressão automatizada); análise de impacto pelo Git antes da regressão | 2.2.3 e 2.3, p. 28 |
| Atividades | executar, comparar o real com o esperado, registrar (trilha), analisar as causas prováveis (diagnóstico), relatar (relatório) | 1.4.1, p. 17 |
| Testware e manutenção | roteiros, localizadores, contratos, biblioteca de verbetes, trilha; a cura é manutenção automatizada do testware | 1.4.3, p. 18 |
| Teste contra depuração | o agente testa e apoia a depuração: diagnostica a causa, corrige só o testware | 1.1, p. 14 e 15 |
| Pirâmide | topo: poucos testes, lentos, cobertura larga | 5.1.6, p. 45 |
| Ferramenta | execução e gerenciamento de defeitos; os riscos da 6.2 têm resposta no desenho | 6.1 e 6.2, p. 53 e 54 |
| Relatório de defeitos | campos da 5.5 adotados como esqueleto do relatório v3 (decisão 104) | 5.5, p. 50 e 51 |

Resposta às duas perguntas. Dentro dos parâmetros: sim. O agente faz o que o syllabus descreve como execução de teste dinâmico, funcional, caixa-preta, automatizado, de regressão e de confirmação, com análise das anomalias e relato; o que ele faz a mais (diagnosticar a causa e curar o localizador) é apoio à depuração e manutenção do testware, que o syllabus também descreve. Ponta a ponta: sim, com uma precisão. O syllabus não define "E2E" como nível; "ponta a ponta" nomeia as tarefas testadas no nível de sistema e a camada de cima da pirâmide. O nome "agente de QA de ponta a ponta" se sustenta quando o TCC diz que o nível é teste de sistema e de integração de sistema.

## 4 O que o syllabus pede e o projeto não tinha

1. O relatório de defeitos da seção 5.5 como esqueleto do relatório por caso (decisão 104). Quem preenche cada campo:

| Campo da 5.5 | De onde sai | Quem preenche |
|---|---|---|
| Identificador exclusivo | id do caso e id da trilha | código |
| Título com resumo breve | causa escolhida em palavras e o campo afetado | código, pelo molde |
| Data, organização e autor | data da corrida; autor "agente (qwen2.5:7b, biblioteca de produção pelo hash)" | código |
| Objeto de teste e ambiente | cobaia, página, rota; `ambiente.json`, versão do Ollama, hash da biblioteca | código |
| Contexto | roteiro, passo, modo de injeção, cenário | código |
| Descrição para reproduzir | os passos do roteiro até a falha, a requisição, o status, a resposta (trecho) | código |
| Resultados esperados e reais | contrato e referência em modo normal contra o corpo recebido (o diff que a poda e o caso ao vivo já calculam) | código |
| Severidade e prioridade | em branco, com a classe e o nível do caso ao lado como sugestão | analista, no hub |
| Status | aberto, por padrão | analista, no hub |
| Referências | verbetes citados (pela camada de leitura), caso escrito, trilha | código |

2. A terminologia erro, defeito, falha e causa-raiz no sentido do syllabus, com a diferença declarada: a "causa raiz" do projeto é a categoria do defeito observado (seção 2.2 acima).
3. A análise de impacto antes da regressão (2.2.3 e 2.3) como base formal da integração com o Git.
4. Os riscos da automação (6.2) como base do princípio "a IA nunca aprova sozinha" e da revisão humana (decisão 95).
5. A distinção teste contra depuração (1.1): o agente testa e apoia a depuração.
6. O primeiro princípio (1.3): o relatório nunca afirma ausência de defeitos.

## 5 Como citar no TCC

A referência acima entra na bibliografia; as citações no texto seguem a forma (ISTQB, 2023, p. 26). Onde entra: a seção 4 (fundamentação) ganha o parágrafo dos níveis e tipos (2.2.1 e 2.2.2), a terminologia (1.2.3) e a pirâmide (5.1.6); a seção 5 (método) nomeia o nível e os tipos e cita a análise de impacto (2.2.3 e 2.3) e os riscos da automação (6.2); a seção 6.9 descreve o relatório v3 pelos campos da 5.5; o glossário alinha "E2E", "defeito", "falha" e "causa raiz" ao texto do syllabus.

## 6 O que esta leitura não cobre

Só as seções listadas foram lidas por inteiro. Os capítulos 3 (teste estático) e 4 (técnicas de teste) não foram aplicados ao projeto: as técnicas de caixa-preta da seção 4.2 (partição de equivalência, valores-limite, tabela de decisão) poderiam descrever como o banco de 90 casos foi desenhado (duas por classe de causa e por nível), e isso fica como possível acréscimo ao TCC, a conferir contra o texto do capítulo 4. O capítulo 5 foi lido só nas seções 5.1.6, 5.1.7 e 5.5.
