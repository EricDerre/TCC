<!-- ! Alteração de IA - Revisar: documento novo (10/11/2026): o parecer de um analista sobre o agente e o TCC, como o Eric o colou na sessão, e a leitura ponto a ponto contra o que o repositório mostra. Os números vêm de `ineditos.json`, `trilha.json`, `experimento_prompt.json`, `taxas_progresso.json`, `leitura_revisao_v3.json` e da biblioteca de produção, lidos por script, nenhum digitado de cabeça.
     ! Motivo: a regra do Memorial pede que tudo o que foi avaliado fique registrado com o motivo, inclusive o que não entra; o parecer parte de três premissas que não são as deste projeto (o modelo, a busca e as épocas), e sem a leitura ponto a ponto as recomendações dele pareceriam trabalho por fazer. -->
# Parecer de um analista sobre o agente e o TCC, e a leitura dele (10/11/2026)

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). A decisão sobre o que entra no projeto é a ficha 63 de [pendencias.md](../pendencias.md), fechada em 10/11/2026 pela opção (b): um experimento em texto antes da Fase 5, a corrida 25 (decisão 116). As ideias que o Eric tirou do parecer para o fluxo do agente estão na ficha 64, fechada pela opção (a): vão para pesquisa em sessão própria, sem mudar o agente (decisão 118).

## 1. De onde veio

Em 10/11/2026 o Eric colou na sessão o parecer de um analista sobre os pontos da revisão e o TCC em si (o texto inteiro está na seção 6). O mesmo analista respondeu os 36 relatórios da sessão de revisão (decisões 114 e 117) e escreveu os textos da curadoria das leituras (decisão 115). Pela declaração do Eric, é um analista de QA da empresa em que ele trabalha, que atua com teste de software e não participou do projeto nem conhecia o agente (ficha 62, fechada pela decisão 117). Pelo que o parecer cita, ele leu as cobaias, a biblioteca de produção e as leituras dos verbetes; não cita nenhuma corrida nem nenhum resultado.

## 2. Três premissas do parecer que não são as deste projeto

| O parecer supõe | O que o repositório mostra |
|---|---|
| O modelo é o Qwen2.5-Coder | O modelo do agente é o `qwen2.5:7b` (decisão 52, mantida pela 73 depois da comparação com o Coder 7B; `executar_fase4.MODELO_PADRAO`). |
| A busca é vetorial, por similaridade de embeddings (o significado do texto em números) | A busca é por palavras (BM25), com reforços em código para a rota, a entidade e o status (`recuperacao.py`). A busca por embeddings foi medida e descartada (decisão 61). |
| As épocas são rodadas de treinamento, e as notas são ruído de treinamento | O modelo nunca é treinado. Época é a rodada em que ele propôs acréscimos à biblioteca, aceitos ou barrados por validação em código (Fase 3 e corrida 20 da Fase 4). |

Há uma quarta confusão, que vem da curadoria: o parecer fala como se ela tivesse limpado o que o modelo lê ("poluíam", "o antigo `novo_verbete.md`"). A curadoria mexeu só na camada de leitura (`biblioteca_producao_leitura/`), que o modelo nunca lê (decisão 103; `testar_pos_fase4.py` confere que nenhuma leitura entra no prompt). A biblioteca que o modelo lê não mudou: continua com o `novo_verbete.md` e com as notas.

## 3. Ponto a ponto

| Ponto do parecer | O que o repositório mostra | Leitura |
|---|---|---|
| **1. Ruído no que a busca recupera:** notas legadas e instruções imperativas, como o `novo_verbete.md` | É verdade que estão lá: a biblioteca que o modelo lê tem 26 notas do modelo em 20 verbetes, 25 delas escritas como instrução ("Adicionar", "Corrigir"), e 3 verbetes aprendidos, 2 com o resumo em forma de instrução (`atualizacao-da-tela`, `novo_verbete`). A revisão do lote da corrida 20 já tinha julgado a maior parte das propostas como parcial ou errada (roadmap §2.12). O efeito no acerto foi medido uma vez, na Fase 3: a cópia curada da biblioteca rende como a biblioteca inteira (corrida 12, decisão 71). O efeito do lote da Fase 4 não foi isolado. | Procede como observação; o mecanismo não é o do parecer, porque não há espaço vetorial. Limpar a biblioteca que o modelo lê muda o que as corridas 16 a 24 mediram: é a opção (b) da ficha 63. |
| **1. Confusão entre causas vizinhas** (`tipo_divergente` com `valor_fora_do_dominio`) | Medido. Os 11 erros da corrida 24 estão na tabela abaixo: em 9 deles o verbete certo não estava entre os três entregues. Com o verbete certo no prompt o agente acerta 18 de 20; sem ele, 7 de 16 (`ineditos.json`, campo `verbete_certo`). | Procede e já está medido. O que mais pesa não é a nota: é o verbete certo não chegar ao modelo. |
| **1. Falta de um ciclo em que a LLM confere se a correção resolveu o sintoma** | A correção que o agente faz é a cura de localizador, em código, e ela já é conferida pela reexecução do roteiro (`cura_seletor.py`, regra R3; corrida 19, roadmap §2.11). O modelo não executa correção nenhuma: ele diagnostica. A reavaliação do diagnóstico pelo próprio modelo foi medida na corrida 22: o produto TPR x TNR da divergência sinalizada (a parcela dos erros que ela pega vezes a parcela dos acertos que ela poupa) fica em 0,284, contra 0,250 do acaso, com as intervenções em todos os casos, e em 0,542 contada só onde um gatilho dispararia; e o modelo citou um verbete plantado em 8 de 36 casos (`trilha.json`, campos `resumo`, `sinais` e `sonda`). | Não se aplica como está: não há correção feita pela LLM para conferir. Um segundo passe de reavaliação é uma segunda chamada ao modelo (princípio 2 do plano da Pós-Fase 4) e, neste modelo, a autoavaliação foi medida como fraca. |
| **1. Propagação da API para a tela:** o modelo perde a causa de ponta a ponta | Medido, e é o ponto mais fraco do agente: na classe 4 (tradução: o mapeamento entre as camadas está errado) a corrida 24 acerta 1 de 6 (`ineditos.json`, campo `por_classe`). O caso ao vivo já leva ao modelo os dois lados: o sintoma da tela e o corpo da resposta contra o contrato e contra a referência (`caso_ao_vivo.py`). | Procede. Entra no TCC como limitação declarada e trabalho futuro; o que falta nesses casos é o verbete certo na busca, não o raciocínio em passos. |
| **2.A.1 Levar ao prompt os sintomas e a causa, não o verbete inteiro** | O prompt já não leva o verbete inteiro: leva a forma compacta (`biblioteca.render`: resumo, sinais e causa, mais as notas e as correções), só dos três verbetes mais bem pontuados (k = 3 pela regra R8, corrida 16), e a busca já casa o sintoma do caso com os campos `sintomas` e `palavras_chave` (`recuperacao.py`). A Fase 2-B comparou entregar a biblioteca inteira (condição A1) com recuperar três verbetes (A2) e ficou com a recuperação (roadmap §1; `comparacao-entre-fases.md`). | Já é assim, salvo as notas: tirá-las do prompt é a mesma mudança do primeiro ponto. |
| **2.A.2 Apontar a busca só para os verbetes curados** (`curado: sim`) | `curado: sim` existe só na camada de leitura, que é para o analista. Pôr a busca e o prompt em cima dela troca a biblioteca que o modelo lê: a calibração do selo de confiança (corrida 16), os limiares e as leituras vigentes deixam de valer (decisões 69, 95 e 103). | Conflita com a decisão 103. Como experimento em texto, é a opção (b) da ficha 63. |
| **2.B.1 Raciocínio em três passos antes de responder** (observação, hipótese, plano de ação) | Medido na Fase 2-A, com seis modelos: o prompt em estágios empata com o linear nos modelos de 1,5B a 7B e é pior no melhor modelo, com custo maior (relatório da Fase 2-A, seção 3). Na corrida 23, um exemplar resolvido no prompt mudou 6 casos para um lado e 4 para o outro, sem sair do ruído (`experimento_prompt.json`). No agente, a probabilidade que vira o selo de confiança é lida no primeiro token do rótulo (`diagnostico_ao_vivo.py`): texto antes do rótulo desfaz a calibração. E cada 100 tokens a mais custam cerca de 23 s nesta máquina (geração a 4,28 tokens por segundo, `taxas_progresso.json`). | Já medido e descartado. O passo 3 (decidir ajuste no corpo da resposta da API ou no estado) está fora do escopo: o agente só cura localizador. |
| **2.B.2 Depois da correção, validar a tela de novo e, se falhar, reavaliar as causas vizinhas** | A validação depois da cura existe (a reexecução do roteiro). Para o diagnóstico não há como saber, em uso, que ele falhou: não há gabarito. O que o agente faz é marcar a confiança e os gatilhos de revisão, e quem decide é a pessoa (princípio 4 do plano da Pós-Fase 4: a IA nunca aprova sozinha). | A parte que se aplica já existe; a outra depende de um sinal de erro que o agente não tem. |
| **2.C.1 Montar um benchmark com os 7 modos do injetor e medir com e sem a biblioteca** | É o que o projeto faz desde a Fase 2: 90 casos em seis classes, com e sem documentação (Fase 2-B, condições A0 a A5; `comparacao-entre-fases.md`), quatro modelos em três épocas (Fase 3), casos inéditos (Fase 3-B e corrida 24) e, na Fase 4, a tela com os modos de injeção da CobaiaAPI (os 7 originais e os 14 novos, roadmap §1) e dez cenários para a Fase 5. | Já feito; o parecer não tinha os resultados à mão. Fica o lembrete de pôr essa comparação em destaque no TCC. |

Os 11 erros da corrida 24 (`ineditos.json`, campo `casos`):

| Caso | Causa certa | Causa respondida | O verbete certo estava entre os três entregues |
|---|---|---|---|
| `sin-26` | `campo_ausente` | `resposta_truncada` | sim |
| `semt-23` | `valor_fora_do_dominio` | `tipo_divergente` | não |
| `semt-27` | `valor_fora_do_dominio` | `colecao_no_lugar_de_objeto` | não |
| `tra-22` | `escala_ou_unidade_errada` | `tipo_divergente` | não |
| `tra-23` | `escala_ou_unidade_errada` | `valor_fora_do_dominio` | não |
| `tra-25` | `contagem_inconsistente` | `resposta_truncada` | sim |
| `tra-26` | `chave_de_juncao_errada` | `colecao_no_lugar_de_objeto` | não |
| `tra-27` | `escala_ou_unidade_errada` | `tipo_divergente` | não |
| `run-26` | `dado_desatualizado` | `registro_duplicado` | não |
| `efe-26` | `estado_da_tela_divergente` | `colecao_no_lugar_de_objeto` | não |
| `efe-27` | `estado_da_tela_divergente` | `dado_desatualizado` | não |

## 4. O que fica do parecer

- **As notas e os verbetes aprendidos escritos como instrução estão na biblioteca que o modelo lê.** É a observação mais concreta do parecer e está certa. Se o projeto mede o efeito de tirá-los ou deixa como limitação declarada é a ficha 63.
- **A classe de tradução é onde o agente mais erra.** O parecer chegou a isso lendo os verbetes; as corridas já mostravam. Entra no TCC com o número.
- **A comparação com e sem a biblioteca precisa aparecer cedo no TCC.** Ela existe desde a Fase 2-B; se um leitor atento não a encontrou, o documento precisa mostrá-la melhor.

O que não entra, com o motivo: a busca nas leituras curadas (conflita com a decisão 103 e desfaz a calibração), o raciocínio em passos (medido na Fase 2-A e na corrida 23), o ciclo de reavaliação pelo modelo (segunda chamada ao modelo, e a autoavaliação dele foi medida como fraca na corrida 22) e a correção do corpo da resposta ou do estado pelo agente (fora do escopo: só cura de localizador).

## 5. O que este parecer não é

Não é uma revisão dos resultados: o analista não viu as corridas. E os textos que ele escreveu na curadoria repetiam as três premissas da seção 2; os consertos estão em `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md` (decisão 115).

## 6. O parecer como foi recebido

O texto abaixo é o que o Eric colou na sessão, sem mudança.

```text
Parecer Técnico: Foco na LLM e no Agente de Self-Healing (TCC)
Reorientando a análise estritamente para o escopo central do seu projeto — o Agente Autônomo de Garantia de Qualidade e a LLM (Qwen2.5-Coder) —, a infraestrutura subintendida (`CobaiaFront` e `CobaiaAPI`) não deve ser tratada como o produto final, mas sim como o ambiente de teste, o "banco de provas" e a fronteira de observabilidade onde o agente opera.

A eficácia do seu agente de Self-Healing depende diretamente de como a LLM consome o contexto, interpreta os sinais de erro, navega pela base de conhecimento (`biblioteca_producao`) e formula correções. Abaixo estão os pontos críticos e as melhorias arquiteturais para otimizar o desempenho da IA.

1. Gargalos Atuais sob a Ótica da LLM e do Agente

* Ruído e Poluição Vetorial no RAG (Retrieval-Augmented Generation):

   * O problema: A presença de anotações legadas, instruções imperativas (ex: o antigo `novo_verbete.md` que dizia "Corrigir a junção...") e notas redundantes geradas nas Fases 3 e 4 poluíam o espaço vetorial. Isso fazia com que a LLM recuperasse trechos contraditórios ou ambíguos na hora de diagnosticar uma falha.

   * Impacto no Agente: Confusão semântica na inferência, levando o agente a propor diagnósticos genéricos ou a citar causas vizinhas incorretas (confundindo `tipo_divergente` com `valor_fora_do_dominio`).

* Falta de Estruturação Dinâmica de Feedback (Self-Correction Loop):

   * O problema: Nos testes iniciais, o agente dependia de um ciclo de recuperação puramente estático baseado nos verbetes estáticos, sem um mecanismo formalizado de reflection onde a LLM avalia se a ação corretiva executada via Playwright realmente resolveu o sintoma visual na tela.

* Complexidade do Contexto de Integração (Front vs API):

   * O problema: Como os erros propagam-se de forma encadeada (ex: um erro de tipo gerado na API (`type_drift`) que explode como um erro de renderização no JavaScript do front-end (`NaN` ou `Invalid Date`)), a LLM frequentemente perdia o rastro da causalidade de ponta a ponta se o verbete consultado focasse apenas em uma das pontas.

2. O Que Implementar e Ajustar com Foco na LLM
Para maximizar a acurácia, a taxa de sucesso de autocorreção e a elegância do seu TCC, implemente as seguintes melhorias focadas no agente e no uso do modelo de linguagem:

A. Otimização do Pipeline de RAG e Recuperação de Contexto

1. Curadoria Semântica Baseada em Sintomas (Prompt Context Injection):

   * Em vez de injetar o verbete inteiro cegamente no prompt do Qwen2.5-Coder, estruture a recuperação para priorizar os blocos de Sintomas (`sintomas` do cabeçalho) e Causas Raiz. O agente deve correlacionar primeiro o log do Playwright/browser com o sintoma exato para então puxar a instrução de correção.

2. Taxonomia Vetorial Limpa (O Legado dos 39 Verbetes):

   * Garanta que o motor de busca vetorial do seu agenteponte exclusivamente para os verbetes curados (`curado: sim`). A ausência de ruídos de treinamento assegura que a embeddings similarity acerte o verbete correto de primeira.

B. Refinamento do Prompt System e Capacidades do Agente (Agentic Workflow)

1. Implementar um Framework de Raciocínio Estruturado (Chain-of-Thought para QA):

   * Forçar o Qwen2.5-Coder a seguir um loop explícito de raciocínio antes de disparar uma ação de correção:

      * Passo 1 (Observação): Analisar o screenshot/HTML do Playwright ou o stack trace da API.

      * Passo 2 (Hipótese): Mapear o sintoma para a taxonomia da `biblioteca_producao`.

      * Passo 3 (Plano de Ação): Decidir se a autocorreção exige ajuste no payload da API, reescrita de seletor ou manipulação do estado.

2. Ciclo de Auto-Avaliação (Reflection Loop):

   * Adicione uma etapa onde, após a LLM executar a correção (ex: alterar um script ou injetar um mock), o agente valida novamente a interface para confirmar se o erro sumiu. Caso contrário, o agente deve reavaliar as causas vizinhas listadas no verbete (ex: se falhou em `recurso_inexistente`, checar `localizador_quebrado`).

C. Uso Inteligente do Injetor de Falhas como "Treino" para a LLM

1. Avaliação por Cenários Determinísticos (Benchmark de IA):

   * Utilize os 7 modos do injetor de falhas (`error_500`, `latency`, `type_drift`, `malformed_json`, etc.) para montar uma suíte de benchmark automatizada para o agente.

   * Meça quantitativamente para o texto do TCC: Em X execuções de falhas injetadas aleatoriamente, quantas vezes a LLM identificou a causa raiz correta utilizando a biblioteca de verbetes versus sem ela? Isso dará o embasamento científico e numérico robusto que a banca de Computação espera ver no seu trabalho.
```
