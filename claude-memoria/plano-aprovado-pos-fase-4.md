<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): o plano da Pós-Fase 4, escrito a partir do pedido do Eric de 07/11/2026 em três partes e das quatro respostas dele no quadro da sessão (fichas 49 a 52, decisões 101 a 104). Aprovado pelo Eric no mesmo dia, no quadro da sessão (ficha 54, decisão 105), com a ficha 53 respondida por "nenhum" (decisão 106); o arquivo passou de `plano-pos-fase-4.md` a `plano-aprovado-pos-fase-4.md`, sem mudança de texto.
     ! Motivo: a decisão 94 abriu a Pós-Fase 4 "a especificar pelo Eric", e ele especificou nesta data; sem o plano escrito, as decisões ficariam só no quadro da sessão, e o que conflita com decisões anteriores (93, 69, 91, 95) precisa estar registrado antes de qualquer código. Os números vêm dos arquivos de pesquisa em `Documentacao/memorial/5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`, do syllabus CTFL 4.0 e dos JSON das corridas; nenhum digitado à mão. -->

# Plano da Pós-Fase 4: o que chega ao analista (aprovado em 07/11/2026)

Estado: **aprovado pelo Eric em 07/11/2026, como está** (ficha 54 de [pendencias.md](../Documentacao/memorial/pendencias.md), decisão 105; a ficha 53, sobre testar repositórios, foi respondida por "nenhum", decisão 106). As quatro decisões que o plano incorpora foram tomadas por ele no quadro da sessão do mesmo dia (fichas 49 a 52, decisões 101 a 104). O texto não muda depois da aprovação; o que desviar dele entra no anexo, como no plano da Fase 4. A pesquisa que embasa cada ponto está no [levantamento da Pós-Fase 4](../Documentacao/memorial/2-pesquisa-e-literatura/levantamento-2026-11-07-pos-fase-4.md) (§6.15).

## 1. Contexto

### 1.1 O que a Pós-Fase 4 entrega

A Fase 4 fechou em 06/11/2026 com o agente lendo a tela, diagnosticando, curando localizador em código e gravando a trilha de cada passo. O que ela não fez foi cuidar de quem lê: o relatório por caso e os verbetes chegam ao analista em texto corrido, com jargão da IA, e a espera de 40 a 130 segundos por diagnóstico deixa a CPU em 99% sem nenhum sinal de que a máquina não travou. A Pós-Fase 4 muda o que chega ao analista, sem mudar o que o agente mede.

O pedido do Eric (07/11/2026) tem três partes:

1. **Parte 1, o visual e a usabilidade do agente:** um hub central à imagem de uma pull request (GitHub e Azure DevOps), onde o analista vê a região do artefato em revisão, comenta no trecho e na revisão, ativa e roda os testes, lê respostas e relatórios; integração com o Git, para o agente ler o que mudou e preparar os testes pelos contratos; uma barra de progresso enquanto o modelo pensa; a árvore de decisão do caso, Decisão 1, Decisão 2, Decisão 3, com as alternativas e o motivo de cada escolha, sem jargão; e a normalização das respostas junto da revisão dos verbetes, em linguagem de comentário em código, com filtros determinísticos medidos por métricas de pesquisa e de mercado. Tudo embasado em fontes.
2. **Parte 2, o syllabus do ISTQB (tradução do BSTQB):** validar se o projeto está dentro dos parâmetros e se cabe o nome de teste de ponta a ponta; o que faltar entra no projeto; o documento entra como referência e bibliografia do TCC.
3. **Parte 3, oito repositórios do GitHub:** validar a viabilidade de cada um para o Claude Code e para o agente, mesmo que nenhum entre, porque a pesquisa fica registrada.

### 1.2 O que já está decidido e não se rediscute aqui

- **Tudo roda na máquina do dev de QA** (decisões de arquitetura; confirmada hoje pela decisão 102): Windows 11 corporativo sem administrador, i5-1235U, 16 GB, sem GPU, Ollama nativo.
- **O prompt do diagnóstico está congelado byte a byte** (decisões 79 e 91): nada desta fase o toca.
- **A biblioteca de produção só muda por lote aceito** e trocar o que o modelo lê obriga a medir de novo (decisões 69 e 95).
- **As leituras vigentes da Fase 4 continuam valendo:** `tela_v4` (corrida 18d), `cenarios_v4` (21d), `ineditos` (24). Nada desta fase repete corrida.
- **A medida com revisor humano está em aberto até as respostas serem normalizadas** (decisão 95, ficha 40): é esta fase que a destrava.
- **A interface para o analista ficou para depois da Fase 5** (decisão 93). A decisão 101 divide: o que muda o que o analista lê entra antes da Fase 5; o hub e a integração com o Git, depois.
- **O prompt e a trilha não ganham segunda chamada ao modelo** (regra da Pré-Fase 4): o relatório para humanos sai por script do arquivo bruto.

### 1.3 As quatro decisões de 07/11/2026 (fichas 49 a 52)

| Ficha | Pergunta | Decisão do Eric | Efeito no plano |
|---|---|---|---|
| 49 | O hub é a interface que a decisão 93 deixou para depois da Fase 5. Como fica a ordem? | **Dividir** (decisão 101) | Antes da Fase 5: barra de progresso, árvore de decisão, filtros e normalização, camada de leitura dos verbetes, revisão humana. Depois: hub e integração com o Git, desenhados e com viabilidade provada agora |
| 50 | VM ou servidor, como o orientador sugeriu? | **Fica local** (decisão 102) | A VM fica registrada como "viável só num servidor", com as fontes (§6.15, base E) |
| 51 | Normalizar os verbetes muda o que o modelo lê. Como tratar? | **Camada de leitura** (decisão 103) | Os verbetes da biblioteca não mudam; nasce uma camada de leitura fora dela, gerada por código e curada à mão, que é o que o relatório, o hub e a revisão humana mostram |
| 52 | O syllabus pede o relatório de defeitos da seção 5.5. Adotar como esqueleto? | **Adotar a 5.5** (decisão 104) | O relatório por caso e o hub seguem os campos da 5.5; o que o código sabe é preenchido por código, e severidade, prioridade e estado ficam para o analista |

### 1.4 O que a leitura de 07/11/2026 mostrou (só leitura, nada mudou)

- **A integração com o Git já tem o mapa:** dos 40 verbetes da biblioteca de produção, 38 declaram `arquivos:` e 24 declaram `endpoints:` no frontmatter; os cenários declaram `requisicao` e `esquema`. Um `git diff --name-only` entre o commit testado e o novo, cruzado com esses campos, seleciona os cenários sem modelo. É a mesma forma do `TIA.UserMapFile` do Azure DevOps, um mapa escrito à mão e aproximado, e da seleção por arquivo do Ekstazi (32% menos tempo em média, e 54% nas suítes mais longas, em 615 revisões de 32 projetos). O agente de hoje não precisa mudar de estrutura: a seleção roda antes de `executar_fase4.py --modo cenarios`.
- **O relatório por caso (v2) tem seis seções fixas** (veredito, evidência, contraste com a segunda causa, FONTE declarada e conferida, linha de ação, árvore completa) e o nó `diagnostico` da trilha v2 guarda a escolha, as alternativas com probabilidade, a segunda causa, o que cada alternativa tem de verbete que a sustenta, as verificações em código, os gatilhos e a justificativa por molde. A árvore de decisão e o relatório no molde da 5.5 saem desses dados, sem nada novo gravado pelo agente.
- **O Ollama só devolve as durações no fim da resposta;** em fluxo, entrega a contagem de tokens gerados. A estimativa de tempo restante vem das taxas de prefill e de geração das respostas anteriores do mesmo modelo nesta máquina, e o projeto já mediu que o prefill é de 79% a 83% do tempo.
- **A regra de escrita do Eric existe por escrito** na memória do repositório TargetERP (o resumo técnico da OC em árvore, "Motivo:" em linha própria, código de situação com significado, nada de jargão) e é a mesma regra dos comentários de IA deste repositório. É ela que os filtros medem.
- **O syllabus CTFL 4.0 não define "E2E" como nível de teste:** "tarefas de ponta a ponta" são o conteúdo funcional do Teste de Sistema (seção 2.2.1, p. 26) e a camada de cima da pirâmide (5.1.6, p. 45). Detalhe na parte 2.

## 2. Princípios que valem para o plano todo

1. **Nada muda o que o agente mede.** Prompt, biblioteca, busca, poda e cura ficam como estão. Toda saída nova para o analista é gerada por código a partir da trilha e dos registros já gravados.
2. **Primeiro a máquina, depois o modelo.** Filtros, árvore, relatório, seleção por diff e barra de progresso são código. Nenhuma segunda chamada ao modelo.
3. **O que o modelo escreveu fica rotulado como texto do modelo**, separado do que o código conferiu (Turpin et al., 2023; Lanham et al., 2023: o raciocínio em texto não é garantia do que o modelo fez).
4. **A IA nunca aprova sozinha.** No hub, o veredito é do analista; o agente comenta (como a revisão do Copilot no Azure DevOps, que sai sempre como comentário).
5. **Toda regra de texto tem fonte e limiar declarado**, e os limiares calibrados no nosso corpus são declarados como calibração, não como valor de fonte.
6. **Testes escritos antes** (TDD), fumaça sem modelo sobre as trilhas já gravadas, e nenhum teste com banco durante corrida.
7. **Tudo embasado:** cada ponto do plano aponta a subseção do levantamento §6.15 que o sustenta.

## 3. Parte 1: o que chega ao analista

### 3.1 O relatório por caso no molde do relatório de defeitos (ISTQB 5.5; decisão 104)

O relatório v3 é gerado da trilha v2 e dos registros, com os campos que a seção 5.5 do syllabus lista para um relatório de defeitos de teste dinâmico (p. 50):

| Campo da 5.5 | De onde sai | Quem preenche |
|---|---|---|
| Identificador único | id do caso e id da trilha | código |
| Título com resumo breve | causa escolhida em palavras e o campo afetado | código, pelo molde |
| Data, organização e autor | data da corrida; autor "agente (qwen2.5:7b, biblioteca `hash`)" | código |
| Objeto de teste e ambiente | cobaia, página, rota; `ambiente.json`, versão do Ollama, hash da biblioteca | código |
| Contexto | roteiro, passo, modo de injeção, cenário | código |
| Descrição para reproduzir | os passos do roteiro até a falha, a requisição, o status, a resposta (trecho) | código |
| Resultado esperado contra real | contrato e referência em modo normal contra o corpo recebido (o diff que a poda e o caso ao vivo já calculam) | código |
| Severidade e prioridade | em branco, com a classe e o nível do caso ao lado como sugestão | analista, no hub |
| Estado | aberto, por padrão | analista, no hub |
| Referências | verbetes citados (pela camada de leitura), caso escrito, trilha | código |

O que o v2 tem e o v3 mantém: veredito com selo em palavras, evidência, contraste com a segunda causa, FONTE declarada e conferida, linha de ação, árvore. O que muda é a ordem e a linguagem: a regra de escrita do Eric (seção 1.4) e os filtros da seção 3.3 valem para cada frase gerada pelo molde. Os relatórios das corridas 18d, 21d e 24 são regerados das trilhas gravadas, sem corrida nova; os v2 ficam como estão nas pastas das corridas.

### 3.2 A camada de leitura dos verbetes (decisão 103)

Os 40 verbetes da biblioteca de produção não mudam (o hash `95af35290860` continua). Nasce `Programacao/AgenteCore/biblioteca_producao_leitura/` (nome a confirmar no pacote), com um arquivo por verbete, gerado por código a partir do frontmatter e das seções (o que é, como aparece na tela, o que conferir, onde está no código) e curado à mão por quem lê, na linguagem da seção 1.4. O relatório, a árvore e o hub citam a camada de leitura; a busca e o prompt continuam lendo a biblioteca. Um teste garante que cada verbete da biblioteca tem a sua leitura e que nenhuma leitura entra no prompt (hash do prompt fixo inalterado). A revisão humana da decisão 95 lê esta camada.

### 3.3 Os filtros determinísticos de prolixidade e objetividade

`filtros_de_texto.py`, só biblioteca padrão, mede qualquer texto que chega ao analista (relatório v3, camada de leitura, texto livre do modelo) e devolve as oito métricas da base D do levantamento, com a fonte de cada uma:

| Métrica | Limiar | De onde vem o limiar |
|---|---|---|
| Palavras por frase (média e máximo) | média até 20, máximo 30 por frase | calibração no corpus de referência; a Lei 15.263/2025 (art. 5) e a ISO 24495-1 só dizem "frases curtas" |
| Flesch adaptado ao português | 50 ou mais, como alarme | fórmula do NILC-Metrix (Leal et al., 2023): 248,835 - 1,015 x palavras por frase - 84,6 x sílabas por palavra; faixa "fácil" de Martins et al. (1996) |
| Razão de preenchimento por lista fechada | percentil 95 do corpus | guia de tom do Google; Zhang, Das e Zhang (2024) |
| Repetição interna (trigramas repetidos) | percentil 95 do corpus | ataque da lista repetitiva de Zheng et al. (2023): dois dos três juízes-modelo testados caíram em 91,3% dos casos, e o terceiro em 8,7% |
| Taxa de compressão contra o resumo que o conteúdo pede | calibração | definição de verboso como "comprimível" (Zhang, Das e Zhang, 2024); o denominador é desenho nosso |
| Jargão e sigla sem expansão na primeira menção, por lista fechada | zero | Lei 15.263/2025, art. 5 |
| Densidade de termos do domínio por palavra | só para comparar | Adams et al. (2023), adaptado a lista fechada |
| Tamanho em palavras | nunca como critério | Dubois et al. (2024), Zheng et al. (2023): o tamanho infla a nota de qualquer juiz-modelo |

O corpus de referência da calibração são os textos "Motivo:" dos comentários de IA deste repositório, que seguem a regra, e o exemplo canônico do resumo técnico do Eric (memória `feedback-resumo-tecnico-aba-ocorrencia`). Nenhum texto do repositório TargetERP é copiado para cá. O filtro grava uma leitura antes e depois para os relatórios das três corridas vigentes e para a camada de leitura, e o painel ganha a aba "O que chega ao analista".

### 3.4 A árvore de decisão

`arvore_de_decisao.py` lê a trilha v2 de um caso e emite a árvore em Markdown e em JSON (para o hub): um nó por decisão do agente, na ordem em que aconteceram.

- **Decisão 1, o que o modelo lê:** o que a poda tirou e manteve, e por quê (regra em código).
- **Decisão 2, que verbetes entram:** os três entregues, os que ficaram de fora com a pontuação, e o sinal que decidiu (contrato, referência, sintoma).
- **Decisão 3, a causa:** a escolhida contra a segunda e as demais alternativas, a confiança em palavras ("alta", "média", "baixa", com a taxa de acerto histórica dessa faixa na calibração, em frase comum, sem k, logprob nem hit@3), a evidência citada (campo, trecho, verbete pela camada de leitura) e a divergência, quando o que o modelo disse não bate com o que o código conferiu.
- **Decisão 4, a cura**, quando houver: o candidato escolhido, os descartados e o motivo (verificação em código).

Cada afirmação leva um rótulo de origem: **observado** (o código mediu), **conferido** (o código checou o que o modelo disse), **declarado** (o modelo escreveu, sem garantia) e **desconhecido** (faltou dado; nunca vira percentual). Os rótulos vêm da ideia do repositório agenttrail (base C e repo 5 do levantamento), implementados em Python. O raciocínio aberto do modelo, se exibido, fica em bloco separado com o rótulo "texto do modelo". Base: Miller (2019) e Lim e Dey (2009) para a explicação contrastiva; Turpin et al. (2023) e Lanham et al. (2023) para a fidelidade; Amershi et al. (2019), diretrizes G2 e G11.

### 3.5 A barra de progresso

`progresso.py` estima o tempo restante de cada inferência em duas fases, com as taxas gravadas das respostas anteriores do mesmo modelo nesta máquina: a de prefill (tokens do prompt, contados antes de enviar, divididos pela taxa de prefill) e a de geração (tokens gerados contra o teto de saída, corrigida pelo fluxo token a token). A barra começa indeterminada com a etapa nomeada ("lendo o caso, N tokens"), vira determinada assim que a estimativa existe, sem trocar de forma, nunca para perto do fim e permite cancelar. Base: Nielsen (1993), limites de 0,1, 1 e 10 segundos; Myers (1985), 86,1% dos sujeitos preferem o indicador; Harrison et al. (2007), pausas no fim parecem mais lentas; Apple HIG e Material, determinado quando a duração é estimável. Entra no terminal (`rodar_fase4.ps1` e `executar_fase4.py`) e grava um arquivo de estado em JSON que o hub lê. Teste com Ollama de mentira, sem máquina.

### 3.6 O hub central (depois da Fase 5; decisão 101)

Uma aplicação local, servida por `http.server` da biblioteca padrão, com a página no padrão do painel (HTML e JS gerados por Python), à imagem da revisão de PR (base A do levantamento):

1. a região do artefato à vista: o relatório v3 com a evidência ao lado (resposta, árvore da tela, contrato);
2. comentário ancorado em trecho, comentário geral da revisão e threads com estado (ativo, resolvido, não será tratado), com rascunho enviado junto com o veredito;
3. veredito do analista em cinco valores, como no Azure DevOps (aprovar, aprovar com sugestões, aguardar o autor, rejeitar, comentar), e o agente só comenta;
4. iterações numeradas, com "o que mudou desde a sua última revisão" quando o agente refaz o diagnóstico, e marca de lido que se invalida;
5. a sugestão estruturada "a causa é outra", com a causa corrigida e autoria, que vira dado para o TCC;
6. severidade, prioridade e estado da 5.5, preenchidos aqui;
7. os botões: ativar o agente, rodar os cenários, ver a barra de progresso (3.5), abrir a árvore (3.4).

Os comentários ficam em JSONL por caso, fora da trilha. O que o hub não precisa: diff de linhas, branches, merge, revisores obrigatórios. A pesquisa pede foco em compreensão e brevidade (Bacchelli e Bird, 2013; Cynthia et al., 2026: sugestão ancorada é o maior preditor de resolução, e comentário longo é menos atendido). O trace do Playwright na falha, o "Cérebro ao vivo" e o explorador com a trilha v2 (decisão 93) entram aqui.

### 3.7 A integração com o Git (depois da Fase 5; viabilidade provada agora)

`impacto_git.py`: a corrida grava o commit das cobaias que testou; na próxima, `git diff --name-only <testado> HEAD` dá os arquivos alterados, que casam com `arquivos:` e `endpoints:` dos verbetes e com as rotas dos cenários; a seleção diz quais cenários rodar e por quê (que verbete, que endpoint). Três regras da base E: arquivo fora do mapa roda tudo, nunca nada; rodada completa periódica; a seleção é conferida contra a rodada completa e o que ela deixou de rodar fica registrado. A literatura sustenta a seleção por arquivo (Rothermel e Harrold, 1997; Gligoric, Eloussi e Marinov, 2015; Memon et al., 2017) e o mapa à mão (Azure DevOps, `TIA.UserMapFile`); o que não tem respaldo direto é a ponte por documentação em linguagem natural, que é nossa. O protótipo de viabilidade (meia sessão, sem ligar ao agente: só o mapa e a seleção sobre o histórico do próprio repositório) sai antes da Fase 5 para o TCC dizer "provado em código"; a ligação ao agente e ao hub vem depois.

### 3.8 A VM e o servidor (decisão 102)

Registrado, com as fontes da base E: WSL 2 e Docker Desktop exigem administrador na primeira habilitação; o Hyper-V só existe nas edições Pro e Enterprise e a página de requisitos não confirma a exigência de administrador; o WSL 2 fica por padrão com metade da RAM e retém o cache do modelo até ser desligado; a sobrecarga de CPU medida por terceiros fica entre 5% e 15%. Resposta ao orientador: viável só num servidor, onde alguém com administrador mantém a virtualização e a RAM é dedicada; na máquina do dev de QA, a execução nativa continua.

## 4. Parte 2: o projeto contra o syllabus CTFL 4.0

O que o syllabus diz (tradução do BSTQB, revisão de 06/01/2025; páginas do PDF que o orientador subiu em 06/11/2026):

- **Níveis de teste (2.2.1, p. 26):** cinco níveis; o Teste de Sistema "geralmente inclui o teste funcional de tarefas de ponta a ponta", e o Teste de Integração de Sistema cobre "as interfaces do sistema e de outros sistemas e serviços externos". "E2E" não é um nível: é o conteúdo das tarefas testadas.
- **Pirâmide (5.1.6, p. 45):** "a camada superior representa testes complexos, de alto nível e de ponta a ponta"; "outro modelo popular define testes de unidade, testes de integração e testes de ponta a ponta".
- **Tipos (2.2.2, p. 27):** funcional, não funcional, caixa-preta ("baseado em especificações") e caixa-branca.
- **Confirmação e regressão (2.2.3, p. 28):** "é aconselhável realizar primeiro uma análise de impacto para otimizar a extensão do teste de regressão"; a regressão é "forte candidata à automação".
- **Manutenção (2.3, p. 28):** "a análise de impacto pode ser feita antes de uma alteração".
- **Processo (1.4.1, p. 17):** na execução, "as anomalias são analisadas para identificar suas causas prováveis", o que permite relatá-las.
- **Erro, defeito, falha e causa-raiz (1.2.3, p. 16):** "uma causa-raiz é um motivo fundamental para a ocorrência de um problema", identificada pela análise de causa-raiz quando ocorre uma falha.
- **Relatório de defeitos (5.5, p. 50):** a lista de campos da seção 3.1 deste plano.
- **Ferramentas e automação (6.1 e 6.2, p. 53 e 54):** ferramentas de execução e de gerenciamento de defeitos; entre os riscos, "confiar demais em uma ferramenta, ignorando a necessidade do pensamento crítico humano".

Onde o projeto cabe: o agente roda testes **funcionais, caixa-preta, automatizados, de regressão e de confirmação**, no nível de **sistema e de integração de sistema** (o front PHP e a API são dois sistemas, e a fronteira entre eles é o objeto), sobre **tarefas de ponta a ponta** (abrir a página, listar, abrir o detalhe, entrar, reservar: da interface até o banco). A detecção, a análise das causas prováveis e o relatório são as atividades de execução e de gerenciamento de defeitos do syllabus; o diagnóstico é apoio à depuração, que o syllabus separa do teste (1.1); a cura de localizador é manutenção automatizada do testware (1.4.3, p. 18, e 2.3, p. 28). Pelo syllabus, o nome "agente de QA de ponta a ponta" se sustenta, com a precisão de que o nível é teste de sistema e de integração de sistema.

O que o syllabus pede e o projeto não tinha, e o que entra:

1. **O relatório de defeitos da 5.5** como esqueleto do relatório por caso (decisão 104; seção 3.1).
2. **A terminologia erro, defeito, falha e causa-raiz** no TCC e no relatório: o agente observa a **falha** na tela, localiza o **defeito** na resposta da API (o desvio do contrato ou da referência) e nomeia uma **causa** entre 23 categorias; a causa-raiz no sentido pleno do syllabus (o motivo fundamental, que pode ser humano ou de processo) fica fora do alcance do agente, e o TCC diz isso.
3. **A análise de impacto antes da regressão** (2.2.3 e 2.3) como base formal da integração com o Git (seção 3.7).
4. **Os riscos da automação (6.2)** como base do princípio "a IA nunca aprova sozinha" e da revisão humana (decisão 95).
5. **A distinção teste contra depuração (1.1)** para posicionar o agente com honestidade: ele testa e apoia a depuração.

O que entra no TCC: a referência do syllabus na bibliografia; a seção 4 (fundamentação) ganha o parágrafo dos níveis e tipos com as páginas acima; a seção 5 (método) nomeia o nível e os tipos; o glossário alinha "E2E" ao texto do syllabus; a seção 6.9 usa a 5.5 ao descrever o relatório. Referência: ISTQB. **Certified Tester Foundation Level (CTFL) Syllabus**: versão 4.0. Tradução: BSTQB. [S. l.]: International Software Testing Qualifications Board, 2023. 66 p. Versão de lançamento de 21 abr. 2023; tradução revisada em 6 jan. 2025. Disponível em: https://bstqb.qa/. Acesso em: 7 nov. 2026. Ressalva: em 07/11/2026 o endereço antigo `bstqb.org.br/b9/sobre-ctfl` redirecionava para `bstqb.qa`, cuja página inicial não traz o link do PDF; conferir a página de download antes da versão final do TCC (o PDF lido está em `TCC/syllabus_ctfl_4.0br.pdf` do repositório da disciplina; a leitura completa, com as citações e as páginas, é o §6.15.6).

## 5. Parte 3: os oito repositórios

Cada um foi lido por um subagente (página e README; alguns também docs/ e artigo), com veredito separado para o Claude Code e para o agente; os arquivos completos estão em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/` e o resumo no §6.15.

| Repositório | Interesse do Eric | Para o Claude Code | Para o agente | O que fica |
|---|---|---|---|---|
| dimensional-drawing | alto | não adotar; no máximo uma figura pontual | não serve | nada |
| rag-anything | médio | não adotar | não: exige embedding (descartado por medição, decisão 61), três modelos e nuvem por padrão | nada |
| mcptoon | alto | só se o número de servidores MCP crescer (`mcptoon bench`) | não: recodificar o contexto reabre o prompt congelado | trabalho futuro |
| Understand-Anything | muito alto | opcional e de baixo valor; testar uma vez nas cobaias, sem adotar | não: depende de LLM e Node; a ideia de impacto por diff vale, em Python local | a ideia da seção 3.7 |
| agenttrail | alto | opcional; só passivo, com Node 20 portátil, sem `init` | não como base nem formato: não registra alternativas nem pai | os rótulos de evidência e o registro datado de decisões (seção 3.4) |
| eagle-4 | médio | não serve | não: exige GPU, SGLang ou vLLM e segundo modelo residente | citação de trabalho relacionado |
| GEPA | muito alto | opcional e adiável: só para subagente com métrica automática | **não é filtro de respostas**: é otimizador offline de prompt por evolução com reflexão em texto; no máximo experimento no prompt de cura, no lugar do DSPy adiado | candidato futuro para o prompt de cura |
| claude-obsidian | médio | não instalar: a escrita só roda em WSL, Linux ou macOS | não serve | o lint de notas órfãs, por script |

A ficha 53 perguntou ao Eric se algum dos dois "opcionais" (Understand-Anything nas cobaias; agenttrail passivo) valia uma sessão de teste: nenhum (decisão 106, 07/11/2026); os vereditos ficam como leitura, com as fontes, e o esforço vai para os pacotes Q1 a Q5.

## 6. Decisões do Eric

Fechadas em 07/11/2026: fichas 49 a 52 (decisões 101 a 104; seção 1.3), 53 (nenhum repositório ganha sessão de teste; decisão 106) e 54 (este plano, aprovado como está; decisão 105).

## 7. Ordem de construção, TDD e o que cada pacote entrega

Pacotes Q0 a Q8. Os cinco primeiros vêm antes da Fase 5; os três últimos, depois (decisão 101). Toda sessão começa com os testes escritos, e a fumaça roda sem modelo sobre as trilhas já gravadas.

### Q0. Registro e pesquisa (sessão de 07/11/2026; feito)
Levantamento §6.15 integrado por script com `--check`; fichas 49 a 54; decisões 101 a 104; este plano; roadmap §4.8; painel. Nenhum código do agente.

### Q1. Relatório v3 no molde da 5.5 e camada de leitura dos verbetes (sessões 2 e 3; sem máquina)
`gerar_relatorio_raciocinio.py` ganha o relatório v3 (o v2 continua, para as corridas gravadas); `biblioteca_producao_leitura/` gerada e curada; testes: 37 trilhas da 18d, 10 da 21d e 36 da 24 regeram sem erro, cada campo da 5.5 presente, hash do prompt fixo inalterado, nenhuma leitura entra no prompt.

### Q2. Filtros determinísticos (sessão 4; sem máquina)
`filtros_de_texto.py` com as oito métricas, a calibração no corpus e a leitura antes e depois; `avaliar_fase4.py --texto` grava `resultados_alvo/fase4/texto.{json,md}`; aba "O que chega ao analista". Testes com textos de controle (um bom, um prolixo, um com jargão).

### Q3. Árvore de decisão (sessões 5 e 6; sem máquina)
`arvore_de_decisao.py`, Markdown e JSON, com os rótulos de origem; o explorador do painel ganha a árvore; testes sobre as 83 trilhas das corridas vigentes, incluindo um caso com divergência e um com cura.

### Q4. Barra de progresso (sessão 7; máquina por minutos)
`progresso.py` com as duas fases e o arquivo de estado; ligado ao terminal; teste com Ollama de mentira e uma fumaça real de um caso, para medir o erro da estimativa.

### Q5. Revisão humana (sessão 8; sem máquina; depende de um revisor do grupo)
A sessão da decisão 95 (ficha 40) com o relatório v3 e a árvore, pelo protocolo que já existe (`sessao_revisao.py`), lida por `avaliar_fase4.py --revisao`. Fecha a limitação declarada da Fase 4.

Fase 5 roda depois do Q5, com o agente como está nas corridas 18d e 21d.

### Q6. Hub central (sessões 9 a 12; sem máquina, salvo a fumaça)
Servidor local, página, comentários ancorados, threads, veredito, iterações, campos da 5.5; os três itens da decisão 93; testes com o navegador headless sobre a página.

### Q7. Integração com o Git (sessões 12 e 13; máquina por minutos)
Protótipo de viabilidade antes da Fase 5 (meia sessão, na Q4); depois da Fase 5, a seleção ligada ao `executar_fase4.py` e ao hub, com as três regras da base E e a conferência contra a rodada completa.

### Q8. Documentação e TCC (sessão 14)
Relatório da Pós-Fase 4; a parte 2 no documento do TCC (seções 4, 5, 6.9 e glossário); figuras; painel; memória.

## 8. Custo estimado

Cerca de 14 sessões de trabalho, 8 antes da Fase 5 e 6 depois; máquina só por minutos (fumaças), nenhuma noite. A revisão humana (Q5) depende de um integrante do grupo; a Fase 5 depende dos três.

## 9. Riscos e salvaguardas

- **Calendário:** a Fase 5 é a medida de valor do TCC e depende de pessoas; por isso ela vem logo depois do Q5, e o hub fica para depois.
- **Filtros que reprovam o que o molde escreve:** o limiar é calibrado no corpus da regra, e o molde é ajustado até passar; a leitura antes e depois fica registrada.
- **Camada de leitura que diverge do verbete:** o teste confere que cada leitura cita o id do verbete e os mesmos campos do frontmatter; a curadoria é do Eric.
- **Estimativa de tempo errada:** a barra prefere errar para acabar depois e nunca congela perto do fim (Harrison et al., 2007).
- **Mapa do Git desatualizado:** arquivo fora do mapa roda tudo, e a conferência contra a rodada completa mede o que a seleção perdeu.
- **Hub como aplicação:** fica no padrão do painel (Python e HTML estático), sem runtime novo.

## 10. Fora do escopo

Mudar o prompt, a biblioteca de produção, a busca ou a poda; repetir corridas; GEPA ou DSPy no prompt de cura (candidato futuro); qualquer VM ou servidor; a Fase 5.

## 11. Rastreabilidade

| O quê | Onde |
|---|---|
| Pesquisa | `2-pesquisa-e-literatura/levantamento-2026-11-07-pos-fase-4.md` (§6.15) e os 13 arquivos em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/` |
| Fichas | [pendencias.md](../Documentacao/memorial/pendencias.md): 49 a 54 |
| Decisões | [decisoes.md](../Documentacao/memorial/1-decisoes-e-historico/decisoes.md): 101 a 106 |
| Roadmap | §4.8 |
| Syllabus | `TCC/syllabus_ctfl_4.0br.pdf` no repositório da disciplina |
| Livro-razão | `.superpowers/sdd/pos-fase-4/progress.md` (fora do git), a abrir no Q1 |

## Anexo: desvios do plano

Nenhum até 07/11/2026. Como no plano da Fase 4, o texto acima não muda depois da aprovação; o que desviar dele entra aqui, com a data e o motivo.
