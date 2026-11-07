<!-- ! Alteração de IA - Revisar: (05/11/2026) arquivo novo com a parte técnica que saiu do README: arquitetura, instalação em detalhe, os sistemas de teste, cada script e os valores de cada rodada. As seções vieram inteiras, com as tags antigas de cada trecho, e as tabelas de script com células enormes foram quebradas em partes.
     ! Motivo: o Eric pediu (05/11/2026) que as questões mais técnicas, com o dado em si, como o peso de k e os valores específicos de cada rodada, ficassem num documento à parte do README, para a página principal ficar legível; fica na raiz para os links relativos continuarem valendo. -->
<!-- ! Alteração de IA - Revisar: documento inteiro gerado por IA (arquitetura, instalação,
     uso, decisões técnicas e problemas conhecidos do ambiente cobaia).
     ! Motivo: o repositório não tinha nenhuma documentação; quem clonasse não teria como
     saber que o CobaiaFront depende das extensões mbstring/output_buffering do PHP, que o
     banco é compartilhado entre os dois alvos, nem quais bugs foram deixados de propósito.
     Cada afirmação técnica aqui foi verificada executando, não deduzida do código. -->
<!-- ! Alteração de IA - Revisar: (26/10/2026) 4 trecho(s) corrigido(s) por script no fechamento da Pré-Fase 4, depois da revisão deste documento por um revisor (frases desatualizadas, contradições entre seções, números de decisão e de ficha, texto sem travessão nem seta); a lista com o trecho antigo, o novo e o motivo de cada um está em `Documentacao/memorial/5-metodo-e-ferramental/dados/revisao-pre-fase-4-2026-10-26.json`.
     ! Motivo: o fechamento (P7) previa um revisor por documento de texto; as correções entram declaradas, como as das sínteses da pesquisa, para o texto continuar rastreável. -->
<!-- ! Alteração de IA - Revisar: revisão de 30/09/2026 a pedido do Eric: cabeçalho novo (nome do projeto, selos, resumo,
     estado por fase e resultado principal, mapa da documentação), seções de contribuição, citação, licença e autores,
     índice regerado a partir dos títulos, títulos sem travessão, e todos os travessões e setas do texto corrido trocados
     por vírgula, dois-pontos ou palavras (blocos de código, comandos e diagramas ficaram como estavam).
     ! Motivo: o README descrevia só o ambiente cobaia e ainda dizia que a bateria da Fase 3 estava por rodar e que a Fase 4
     era o próximo passo sem nada antes; o repositório passou a ter os padrões de comunidade do GitHub (código de conduta,
     guia de contribuição, licença, política de segurança, modelos de issue e de pull request) e o Eric pediu tom mais sério,
     sem travessões e setas, mantendo a árvore do repositório e o restante do conteúdo. -->
# Detalhes técnicos

A parte técnica do projeto: como cada peça funciona, cada script e os valores de cada rodada. Para entender o projeto e ver os resultados em figuras, comece pelo [README](README.md); os números exatos de cada figura estão em [Dados das figuras](Documentacao/figuras/dados-das-figuras.md).

## Índice

- [Estado e valores de cada rodada](#estado-e-valores-de-cada-rodada)
- [Mapa da documentação](#mapa-da-documentação)
- [Por que dois alvos](#por-que-dois-alvos)
- [Arquitetura](#arquitetura)
- [Stack técnica](#stack-técnica)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Instalação em detalhe](#instalação-em-detalhe)
- [Navegador recomendado para o agente](#navegador-recomendado-para-o-agente)
- [CobaiaFront em detalhe](#cobaiafront-em-detalhe)
- [CobaiaAPI em detalhe](#cobaiaapi-em-detalhe)
- [AgenteCore: experimentos com os modelos locais](#agentecore-experimentos-com-os-modelos-locais)
- [Ferramentas de apoio ao trabalho com IA (`ferramentas/`)](#ferramentas-de-apoio-ao-trabalho-com-ia-ferramentas)
- [Memória do Claude Code entre máquinas](#memória-do-claude-code-entre-máquinas)
- [Testes e lint](#testes-e-lint)
- [O que é versionado e por quê](#o-que-é-versionado-e-por-quê)
- [Decisões técnicas e problemas resolvidos](#decisões-técnicas-e-problemas-resolvidos)
- [Problemas conhecidos (deixados de propósito)](#problemas-conhecidos-deixados-de-propósito)
- [Segurança](#segurança)
- [Troubleshooting](#troubleshooting)

## Estado e valores de cada rodada

### Fases

| Fase | O que é | Estado |
|---|---|---|
| 1 | Ambiente e sistemas cobaia | Concluída |
| 2-A | Prompts sem documentação, seis modelos, máquina de desenvolvimento | Concluída |
| 2-B | Biblioteca de documentação escrita à mão, seis condições, máquina-alvo | Concluída |
| 3 | Biblioteca gerida pelo próprio modelo, quatro modelos, três épocas | Concluída em 15/09/2026 |
| 3-B | Pontes de versão, casos inéditos, troca cruzada e sondas | Concluída em 01/10/2026 |
| Pré-Fase 4 | Pesquisa antes da Fase 4: modelos grandes lendo os pesos do disco (repositório colibri), atlas visual das competências e raciocínio aberto | Concluída em 26/10/2026 (relatório fechado; parte B da pesquisa integrada; especificação da trilha aprovada; corrida 13 cancelada) |
| 4 | O agente na tela: interceptação, poda da árvore de acessibilidade, cura de seletor, biblioteca em produção e trilha aberta | Concluída em 06/11/2026: pacotes P0 a P8 e corridas 16 a 24 ([relatório da fase](Documentacao/memorial/3-resultados-e-analises/fase-4-relatorio.md); regra R2 cumprida na corrida 18d, no limite exato, decisões 97 e 98; medida com revisor humano em aberto, decisão 95) |
| Pós-Fase 4 | Ajustes e ideias focadas no visual do projeto: tipo de resposta e formatação, com possibilidade de gráficos ou de um dashboard dinâmico (decisão 94) | Não iniciada |
| 5 | Medição de valor (tempo de reparo e sucesso da tarefa) | Não iniciada |

### Resultado principal

**Decisão 52, 22/09/2026:**

- Pela regra fixada antes da bateria, o modelo padrão do agente é o `qwen2.5:7b` com a biblioteca no estado L1, a primeira época escrita por ele, curada em 29/09/2026 e guardada em `Programacao/AgenteCore/biblioteca_producao/`.
- O comparativo com o `qwen2.5-coder:7b`, os 36 casos inéditos, a curadoria, o experimento do recuperador, a ablação base × instruct e as cinco rodadas de pesquisa bibliográfica estão no [painel do projeto](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN), com uma aba por tópico.
- Uma cópia do painel fica em `Documentacao/dashboard/painel-do-projeto.html`.
- Os números citados neste documento vêm dos registros em `resultados_alvo/` e do Memorial.

<!-- ! Alteração de IA - Revisar: (26/10/2026) o parágrafo de estado e a linha da Pré-Fase 4 na tabela de fases passaram a "concluída".
     ! Motivo: a Pré-Fase 4 fechou em 26/10/2026 (relatório fechado, parte B da pesquisa integrada, especificação da trilha aprovada, decisões 75 a 78); o README dizia "em andamento desde 01/10". -->
<!-- ! Alteração de IA - Revisar: (03/11/2026, Fase 4, pacote P5) o parágrafo de estado ganhou o pacote P5 pronto (biblioteca em produção e ciclo de correção) e a corrida 20 à espera do sim do Eric.
     ! Motivo: o parágrafo dizia "próximo pacote: P5"; o P5 foi feito em 03/11 e o README é a porta de entrada do repositório. -->
<!-- ! Alteração de IA - Revisar: (01/11/2026, noite, Fase 4, pacote P4) o parágrafo de estado ganhou o pacote P4 pronto e a corrida 19 feita, com os números de `resultados_alvo/fase4/cura.json` (blocos `tb_f4_cura_resumo`), e o próximo pacote passou a ser o P5.
     ! Motivo: o parágrafo dizia "próximo pacote: P4"; a cura de seletor foi feita e medida em 01/11 à noite, e o README é a porta de entrada do repositório. -->
<!-- ! Alteração de IA - Revisar: (27/10/2026, Fase 4, pacote P3) o parágrafo de estado e a linha da Fase 4 na tabela de fases passaram de "em planejamento" para "em andamento", com os pacotes prontos e as corridas com modelo por rodar; em 28/10/2026 os dois ganharam a corrida 16 feita (calibração do selo, 27/10 à noite).
     ! Motivo: o plano da Fase 4 foi aprovado em 26/10 (decisão 79) e os pacotes P0 a P3 ficaram prontos entre 26 e 27/10; o README ainda dizia que a fase estava em planejamento. A corrida 16 rodou em 27/10 (20:46 a 23:54) e gravou `limiares.json`; sem a atualização o README diria que ela ainda esperava o sim do Eric. Em 01/11/2026 a corrida 18 rodou e não cumpriu a regra R2 (o caso ao vivo volta para revisão, ficha 37); o README passou a dizer isso. -->
<!-- ! Alteração de IA - Revisar: (04/11/2026, Fase 4, pacote P6) o parágrafo de estado ganhou o pacote P6 pronto (os cenários da Fase 5 e o protocolo da linha de base manual) e a corrida 21 à espera da promoção do lote da corrida 20; a data do parágrafo passou a 04/11/2026.
     ! Motivo: o parágrafo dizia "próximo pacote: P6"; o P6 foi feito em 04/11 e o README é a porta de entrada do repositório. -->
<!-- ! Alteração de IA - Revisar: (04/11/2026 à noite, Fase 4, pacote P7) o parágrafo de estado ganhou o pacote P7 pronto (a avaliação da própria trilha) e a corrida 22 à espera do sim do Eric.
     ! Motivo: o parágrafo dizia "próximo pacote: P7"; o P7 foi feito na mesma noite e o README é a porta de entrada do repositório. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026) o parágrafo de estado ganhou a corrida 22 feita; as linhas de `avaliar_fase4.py` e `testar_fase4.py` ganharam os relatórios da sessão de revisão, o sinal por gatilho e a contagem de testes.
     ! Motivo: a corrida rodou na noite de 04 para 05/11 e a leitura achou cinco defeitos do P7, consertados com teste; o README é a porta de entrada do repositório. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026, pacote P8) o parágrafo de estado foi reescrito com a Fase 4 concluída, a linha da Fase 4 na tabela também, e entraram o relatório da fase na lista de documentos, `testar_sessao_revisao.py` nos testes e o `--colar` pela leitura vigente na linha de `avaliar_fase4.py`.
     ! Motivo: a fase fechou com o relatório; o parágrafo contava pacote por pacote e dizia que a fase estava em andamento. O detalhe de cada corrida está no relatório, no roadmap e no painel. Números de `resultados_alvo/fase4/*.json`, lidos por script. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026, pacote P8) 9 trecho(s) corrigido(s) por script no fechamento da Fase 4, depois da revisão deste documento por um revisor; a lista com o trecho antigo, o novo e o motivo de cada um está em `Documentacao/memorial/5-metodo-e-ferramental/dados/revisao-fase-4-2026-11-05.json`.
     ! Motivo: o plano aprovado (P8) prevê um revisor por documento de texto; as correções entram declaradas, para o texto continuar rastreável. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026, depois do P8) o parágrafo de estado e a linha da Fase 4 na tabela de fases passaram a dizer que as fichas 42 a 45 foram respondidas e que faltam corridas antes da Fase 5.
     ! Motivo: o README dizia que as fichas estavam abertas e a fase concluída; as decisões 90 a 92 pedem as corridas 18c, 21c, 23 e 24 antes da Fase 5. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026) "Resultado principal" e "Estado em 05/11/2026" viraram subseções com listas, um assunto por item.
     ! Motivo: o Eric reclamou (05/11/2026) que os assuntos mais novos estavam sem formatação e poluíam a leitura; os dois blocos eram parágrafos corridos de 10 linhas. Nenhum fato foi tirado. -->
<!-- ! Alteração de IA - Revisar: (06/11/2026) a tabela de fases, o estado e o que a Fase 4 mediu ganham a corrida 24, e a Fase 4 passa a concluída.
     ! Motivo: era a última pendência da fase. Números de `ineditos.json`, lidos por script. -->
<!-- ! Alteração de IA - Revisar: (06/11/2026, decisões 97 a 99) a tabela de fases, o estado e o que a Fase 4 mediu passam às corridas 18d, 21d e 18e, com a regra R2 pelos casos que a tela perde.
     ! Motivo: a regra fechou com os sinais novos da busca, e a corrida seguinte da fila é a 24. Números de `tela_v4.json`, `tela_ineditos.json` e `cenarios_v4.json`, lidos por script. -->
<!-- ! Alteração de IA - Revisar: (06/11/2026, decisão 98) a tabela de fases e o resumo do diagnóstico na tela citam as corridas que faltam e a regra R2 pelos casos que a tela perde.
     ! Motivo: a tabela ainda dizia que só faltava a corrida 24, e a leitura da regra mudou antes da corrida 18d. Números dos campos `b` e `c` de `tela_v3.json`. -->
### Estado em 06/11/2026

- Fases 1, 2-A, 2-B, 3 e 3-B concluídas.
- Pré-Fase 4, uma pausa de pesquisa antes do agente na tela, concluída em 26/10 (decisões 75 a 78).
- Fase 4, o agente na tela, com os pacotes P0 a P8 feitos em 05/11, as corridas 18d, 21d, 18e e 24 em 06/11 e o [relatório da fase](Documentacao/memorial/3-resultados-e-analises/fase-4-relatorio.md).
- O agente lê a tela, diagnostica, cura localizador em código, propõe acréscimos à biblioteca atrás de validação e grava uma trilha aberta de cada passo.

#### O que a Fase 4 mediu

- Reprodução: a tela reproduz 37 dos 72 casos de avaliação.
- Diagnóstico na tela: 32 acertos de 37 na tela e 30 no caso escrito (corrida 18d, com os sinais novos da busca, decisão 97), mesmo rótulo em 28. A tela perde 3 casos e ganha 5; o limite é de 3 perdidos, e a regra R2 fecha sem folga (decisão 98; pela soma dos dois lados, 8). O verbete certo chega em 36 de 37, e com ele são 32 acertos de 36. Nos 25 inéditos, que a busca nunca viu (corrida 18e): 22 na tela e 18 no caso escrito, com a tela perdendo 0 e ganhando 4.
- Biblioteca final em casos inéditos (corrida 24, em texto): 25 de 36 (69,4%; Wilson 95% de 53,1 a 82,0), contra 31 de 36 nos casos de avaliação, que não são os mesmos. Com o verbete certo, 18 de 20; sem ele, 7 de 16.
- Cura de localizador: 160 de 160 quebras armadas curadas em código.
- Ensaio dos dez cenários, com uma repetição por cenário: 10 de 10 com Task Success (Wilson 95% de 72,2 a 100,0%; a rodada anterior deu 9 de 10, antes de um conserto na cura) e MTTR médio de 74,0 s com o prompt dentro do limite e os sinais novos da busca (72,5 s na corrida anterior; 105,2 s antes do corte), sem linha de base manual ainda.
- Experimento dos itens da decisão 55, nos 90 casos: 70 acertos com o exemplar e 67 com os rótulos em palavras, contra 68 na corrida 16, sem se separar do acaso (decisão 91).
<!-- ! Alteração de IA - Revisar: (05/11/2026) a medida com revisor humano passou a em aberto (decisão 95), e a tabela das fases ganhou a Pós-Fase 4 (decisão 94).
     ! Motivo: o Eric pediu "em aberto" nesta data; o texto dizia limitação declarada, sem nova sessão. -->
- Avaliação da trilha: a medida com revisor humano da especificação da trilha está em aberto: será feita depois da Pós-Fase 4 (decisão 95).

#### O que falta antes da Fase 5

- As fichas 42 a 45 foram respondidas em 05/11 (decisões 90 a 93).
- Três delas pedem trabalho antes da próxima fase, a Fase 5, que mede o agente contra a linha de base manual: encurtar o prompt na tela e repetir as corridas 18 e 21, o experimento da decisão 55 e os 36 inéditos da ficha 27.
- Esses números ainda podem mudar.

#### Modelo padrão e onde ver os números

- O modelo padrão continua o `qwen2.5:7b` com a biblioteca L1 curada, por acréscimo validado (decisão 52).
- Números, gráficos e a leitura de cada resultado estão no [painel do projeto](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN).

<!-- ! Alteração de IA - Revisar: a lista abaixo ganhou o item da cópia no repositório da disciplina (22/10/2026, decisão 72).
     ! Motivo: o orientador passou a acompanhar o TCC por um repositório próprio, e quem lê este README precisa saber que aquele é cópia, que este é o principal e qual script mantém os dois iguais. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026) a lista abaixo ganhou o item do documento do TCC: a fonte em Markdown e o .docx da versão 2.
     ! Motivo: o README não citava o documento desde a versão 1, de 03/11/2026; quem chegava ao repositório por esta lista achava o projeto de pesquisa, mas não o texto do TCC. O Eric disse sim ao acréscimo em 05/11/2026. -->
## Mapa da documentação

- [Painel do projeto](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN): estado por fase, pendências, roadmap e os resultados, numa página só; gerado por `ferramentas/gerar_dashboard.py`.
- [Memorial de Desenvolvimento](Documentacao/Memorial%20de%20Desenvolvimento.md): índice de tudo o que foi decidido, pesquisado, medido e analisado, em `Documentacao/memorial/` (decisões numeradas, levantamentos bibliográficos com afirmações verificadas, relatórios por fase, análise decisória, método e ferramental).
- [Roadmap](Documentacao/memorial/roadmap.md) e [pendências](Documentacao/memorial/pendencias.md): o que falta rodar e as decisões, em fichas.
- [Relatório da Fase 4](Documentacao/memorial/3-resultados-e-analises/fase-4-relatorio.md): o agente na tela, corrida a corrida, as regras R1 a R8, as limitações declaradas e o que o documento do TCC precisa carregar.
- [Projeto de pesquisa (ABNT NBR 15287)](Documentacao/Projeto%20de%20Pesquisa%20-%20ABNT%2015287_2025%20-%20V3.md) e o PDF beta gerado a partir dele.
- [Documento do TCC (ABNT NBR 14724)](Documentacao/TCC%20-%20ABNT%2014724%20-%20V1.md) e o [.docx da versão 3](Documentacao/TCC_v3_20261105.docx), de 05/11/2026, gerado a partir dele por `ferramentas/gerar_tcc_docx.py` no molde do orientador: texto provisório, com a Fase 4 até a corrida 22, à espera da leitura do grupo e dos números das corridas 18c, 21c, 23 e 24; as corridas 18c, 21c e 23 já rodaram, e as figuras dela já mudaram em `Documentacao/figuras/`, com o texto ainda por atualizar. O nome do arquivo-fonte fica "V1" em todas as versões, porque o gerador lê esse caminho.
- Registros oficiais das baterias em `Programacao/AgenteCore/experimentos/resultados_alvo/` (JSON, logs, gráficos e relatórios navegáveis).
- Cópia no repositório da disciplina, a pedido do orientador: [unicid-projeto-software-2026-2/squad-24-projeto](https://github.com/unicid-projeto-software-2026-2/squad-24-projeto) (privado, acesso pela organização da disciplina), com este repositório, sem a `.claude/` nem a `.venv` da CobaiaAPI, na subpasta `projeto/`, mantida por `ferramentas/sincronizar_orientador.py`, e o épico, as features e os requisitos no modelo do orientador em `docs/`; este repositório é o principal e toda alteração sai primeiro aqui (decisão 72).

## Por que dois alvos

O núcleo da pesquisa é detectar **Contract Drift** (deriva de contrato) na
fronteira de integração Front-to-Back. Um site PHP+MySQL clássico, que
renderiza tudo no servidor, não tem essa fronteira, não há nenhuma
requisição JSON pra interceptar. Por isso o ambiente cobaia tem **dois
alvos**, deliberadamente separados:

| Alvo | O quê | Serve pra testar |
|---|---|---|
<!-- ! Alteração de IA - Revisar: (01/11/2026, Fase 4, pacote P4) a célula do CobaiaFront deixa de dizer "100% intocado": o front ganhou a variante de quebra de localizador (`quebra.php`), ligada só por parâmetro de URL ou cookie e desligada por padrão.
     ! Motivo: ficha 29, opção c (decisão 80): o Eric decidiu medir a cura de seletor também com a quebra feita no HTML que o PHP devolve; sem a correção o README contradiria o código. -->
| **CobaiaFront** | Site PHP+MySQL legado e monolítico (cedido por um integrante do grupo), mantido intocado no código, com uma única exceção: a variante de quebra de localizador da Fase 4 (`quebra.php`, ligada só por `?quebra=<modo>` ou pelo cookie `quebra`; desligada, o site é o de sempre) | Interceptação de requisições de página completa, erros PHP/SQL clássicos, sistemas legados sem API |
| **CobaiaAPI** + a aba "PRODUTOS (API)" dentro do próprio CobaiaFront | API JSON nova (Python/FastAPI), com mecanismo de injeção de falhas controlada | Contract Drift em contratos JSON reais, o foco principal do agente |

Os dois compartilham o **mesmo banco de dados** (`ti93phpdb01`), uma
reserva criada por um dos lados aparece no outro. Isso evita dados
inconsistentes entre os alvos e simula um cenário realista (um backend,
dois clientes diferentes o consumindo).

## Arquitetura

```
                     ┌─────────────────────────────┐
   navegador  ─────► │  CobaiaFront (PHP 8.2)        │
                     │  php -S localhost:8080        │
                     │  produtos_api.php  ──fetch──┐ │
                     └──────────────┬───────────────┘ │
                                    │ mysqli           │ HTTP/JSON
                                    ▼                  ▼
                     ┌─────────────────────────────────────┐
                     │      MariaDB · banco ti93phpdb01      │
                     │  (root sem senha, único pra os dois)  │
                     └─────────────────────────────────────┘
                                    ▲
                                    │ SQLAlchemy + PyMySQL
                     ┌──────────────┴───────────────┐
   navegador/agente ─────► │  CobaiaAPI (FastAPI)          │
                     │  uvicorn localhost:8000       │
                     └────────────────────────────────┘
```

`run.py` sobe os três processos (PHP, MariaDB, uvicorn) juntos.
`install.py` cuida da instalação/configuração de tudo antes disso.

## Stack técnica

### CobaiaFront
- **Linguagem/execução:** PHP 8.2, servidor embutido (`php -S`), sem
  Apache/Nginx (o projeto não usa `.htaccess`/mod_rewrite, então o servidor
  embutido é suficiente e muito mais simples de automatizar).
- **Banco:** MariaDB via extensão `mysqli`, sem ORM, queries diretas.
- **Frontend:** Bootstrap 3, jQuery, um pouco de AngularJS 1.6.9 (área do
  cliente), tudo via CDN ou vendorizado em `css/`/`js/`.
- **Email:** PHPMailer 5.2.27 (vendorizado, `PHPMailer/`), SMTP.
- **Extensões PHP obrigatórias:** `mysqli`, `pdo_mysql`, `mbstring` (ver
  [Decisões técnicas](#decisões-técnicas-e-problemas-resolvidos)).

### CobaiaAPI
- **Linguagem/execução:** Python 3.12+ (testado em 3.14), FastAPI + Uvicorn.
- **Banco:** SQLAlchemy 2.0 (estilo `Mapped`/`mapped_column`) + PyMySQL,
  apontando pro **mesmo** MariaDB do CobaiaFront.
- **Validação:** Pydantic v2 (schemas em `app/schemas.py`).
- **Config:** `pydantic-settings`, lida de `.env` (ver `.env.example`).
- **Testes:** pytest + `fastapi.testclient` (roda contra o banco real).
- **Lint:** ruff.

### Infraestrutura / instalador
- **Windows:** PHP e MariaDB instalados via `winget`
  (`PHP.PHP.8.2`, `MariaDB.Server`).
- **Linux:** `apt-get install php php-mysql mariadb-server`.
- **macOS:** `brew install php mariadb`.
- Todo o resto (schema, seed, venv, dependências Python) é feito por
  `install.py`, que roda igual nos três sistemas.

## Estrutura do repositório

```
TCC/
├── README.md                                # porta de entrada: o projeto, as figuras e como rodar
├── DETALHES-TECNICOS.md                     # este arquivo
├── Cobaia.exe                               # Windows: instala + roda + abre o navegador, tudo em 1
├── Cobaia.py / build_exe.ps1 / Cobaia.spec  # fonte do Cobaia.exe e script pra recompilar
├── install.cmd / install.ps1 / install.sh / install.py   # instalador (chamado por Cobaia.exe também)
├── run.cmd / run.ps1 / run.sh / run.py                   # sobe CobaiaFront + CobaiaAPI juntos
├── _env_common.py                          # helpers compartilhados por install.py/run.py/Cobaia.py
├── LICENSE / CITATION.cff                  # licença MIT e citação do repositório
├── CONTRIBUTING.md / CODE_OF_CONDUCT.md / SECURITY.md    # como contribuir, conduta e política de segurança
├── .github/                                # modelos de issue e de pull request
├── .claude/                                # CLAUDE.md, settings.json (hooks, permissões), rules/ e skills/ do Claude Code (versionados; só settings.local.json fica fora)
├── ferramentas/                            # scripts locais de apoio: painel do projeto, documento do TCC, medição de tokens, resumo de saídas, conferência da documentação, pesquisa, PDF do ABNT
├── claude-memoria/                         # memória do Claude + CLAUDE.md portáteis (importar/exportar.ps1) e os handoffs de sessão em contexto/
├── Documentacao/
│   ├── Projeto de Pesquisa - ABNT 15287_2025 - V3.md   # projeto de pesquisa; o PDF beta V4 é gerado a partir dele
│   ├── TCC - ABNT 14724 - V1.md            # fonte do documento do TCC (o nome fica "V1" em todas as versões, porque o gerador lê esse caminho)
│   ├── TCC_v<versão>_<AAAAMMDD>.docx       # documento do TCC em Word, gerado por ferramentas/gerar_tcc_docx.py
│   ├── figuras/                            # figuras do README, do documento do TCC e dados-das-figuras.md (geradas por gerar_figuras_documentos.py)
│   ├── Memorial de Desenvolvimento.md      # índice do memorial
│   ├── memorial/                           # decisões numeradas, pesquisa bibliográfica, resultados e análises, projeto ABNT, método e ferramental, pendências, roadmap
│   ├── dashboard/painel-do-projeto.html    # painel do projeto (gerado por ferramentas/gerar_dashboard.py; publicado no claude.ai)
│   ├── dashboard/sessao-revisao-trilha.html    # sessão de revisão dos relatórios da corrida 22 (gerada por ferramentas/sessao_revisao.py; publicada no claude.ai)
│   └── notebooks/                          # (fora do git) notebooks de apoio do livro-texto (Faceli et al., 3. ed.), baixados por quem tem o livro
└── Programacao/
    ├── AgenteCore/
    │   ├── base_conhecimento/              # biblioteca de documentação original do cobaia (Fase 2-B); nunca escrita por script
    │   │   ├── negocio/ contratos/ erros/ falhas_injetadas/ defeitos_conhecidos/
    │   │   └── INDICE.md                   # gerado por validar_banco.py --indice
    │   ├── biblioteca_producao/            # cópia curada da biblioteca L1 do qwen2.5:7b (ponto de partida da Fase 4)
    │   ├── experimentos/                   # baterias de avaliação dos modelos locais (Fases 2-A, 2-B, 3, 3-B e 4) e os registros em resultados_alvo/
    │   └── requirements.txt
    ├── CobaiaFront/                        # site PHP legado ("Churrascaria Fornalha")
    │   ├── banco/
    │   │   ├── bancoatualizado.sql         # schema original (tipos, produtos, usuários)
    │   │   ├── schema_completo.sql         # completa o schema (reservas, nível 'cli')
    │   │   └── seed.sql                    # dados de demonstração
    │   ├── admin/                          # painel admin (CRUD produtos/tipos/usuários)
    │   ├── cliente/                        # área do cliente (reservas)
    │   ├── conn/connect.php                # conexão MySQL (intocado)
    │   └── produtos_api.php                # NOVO: página que consome a CobaiaAPI via fetch
    └── CobaiaAPI/
        ├── app/
        │   ├── main.py                     # app FastAPI, CORS, routers
        │   ├── config.py                   # Settings via .env
        │   ├── database.py                 # engine/session SQLAlchemy
        │   ├── models.py                   # ORM nas MESMAS tabelas do CobaiaFront
        │   ├── schemas.py                  # contratos Pydantic (só p/ doc OpenAPI)
        │   ├── fault_injection.py          # mecanismo de injeção de falhas
        │   └── routers/{produtos,pedidos,admin_fault}.py
        ├── tests/
        ├── requirements.txt / requirements-dev.txt
        └── .env.example
```

## Instalação em detalhe

### Pré-requisitos

- Windows 10/11, Linux ou macOS.
- Conexão com a internet (o instalador baixa PHP/MariaDB/pacotes Python se
  não estiverem instalados).
- **Windows:** `winget` (já vem no Windows 10 2004+/11). Não precisa rodar
  como Administrador para PHP; a instalação do MariaDB Server foi testada
  com sucesso **sem** elevação também.
- **Linux:** `sudo` disponível (`apt-get`), distro baseada em Debian/Ubuntu.
- **macOS:** [Homebrew](https://brew.sh) instalado.

Nada precisa ser pré-instalado manualmente além disso, o instalador cuida
do PHP, do MariaDB e do Python/venv.

<!-- ! Alteração de IA - Revisar: parágrafo novo (26/10/2026, Fase 4, pacote P0) sobre a máquina sem administrador: PHP pelo winget em escopo de usuário e MariaDB pelo zip oficial em `%LOCALAPPDATA%`, que `_env_common.py` passou a procurar.
     ! Motivo: na máquina-alvo i5 (corporativa, sem administrador) as cobaias nunca tinham subido e o MSI do `MariaDB.Server` não foi tentado por exigir elevação; sem o parágrafo, quem clonar o repositório numa máquina assim rodaria o instalador e pararia no MariaDB. -->
**Máquina sem administrador (conferido em 26/10/2026 na máquina-alvo i5):** o PHP continua vindo do `winget` em escopo de usuário (`PHP.PHP.8.2`, zip em `%LOCALAPPDATA%\Microsoft\WinGet\Packages`), e o MariaDB foi instalado pelo zip oficial em vez do MSI: extraído em `%LOCALAPPDATA%\MariaDB\mariadb-<versão>-winx64\`, com a pasta de dados criada por `bin\mariadb-install-db.exe --datadir=%LOCALAPPDATA%\MariaDB\data --port=3306` (root sem senha). `run.py` e `install.py` acham o cliente, o servidor e o `my.ini` nesse lugar (`_env_common.py`), e o servidor sobe como processo comum, sem serviço.
<!-- ! Alteração de IA - Revisar: a frase final passou de "o passo é manual" para o que o install.py faz agora (26/10/2026, à noite).
     ! Motivo: `install.ensure_mariadb_installed` ganhou o caminho portátil (`instalar_mariadb_portatil`: API de downloads, pergunta, SHA-256, extração e `mariadb-install-db.exe`); o README dizia que o passo era manual. -->
Sem administrador, o `install.py` faz isso sozinho: pergunta antes de baixar, confere o SHA-256 que o site do MariaDB publica, extrai, cria a pasta de dados e segue para o schema e o seed. `COBAIA_MARIADB_PORTATIL=1` dispensa a pergunta e força o portátil mesmo com administrador; `=0` força o MSI do winget. A API da CobaiaAPI sobe por `python -m uvicorn` da venv dela (`run.py`), não pelo lançador `uvicorn.exe`, porque uma venv movida de pasta deixa os lançadores `.exe` sem funcionar e sem mensagem.

### O que o instalador faz

No Windows, `Cobaia.exe` já faz instalação + run + abrir o navegador em um
só passo; ver [seção dedicada](#cobaiaexe-instalação-execução-e-navegador-em-um-clique)
abaixo. O resto desta seção documenta o instalador "por partes"
(`install.*`), útil pra rodar só a instalação sem subir os serviços, ou no
Linux/macOS.

Um único comando, na raiz do repositório:

```
# Windows: clique duplo em install.cmd, ou pelo terminal:
install.cmd
```
```bash
# Linux / macOS
./install.sh
```

No Windows, use `install.cmd` (não `install.ps1` diretamente), ele evita o
erro comum de *Execution Policy* do PowerShell (ver
[Troubleshooting](#troubleshooting)) sem precisar mudar nenhuma
configuração do sistema. `install.cmd` só chama `install.ps1` por baixo.

O que ele faz, em ordem (idempotente, pode rodar de novo a qualquer hora
sem duplicar nada):

1. Garante que existe Python 3 (instala via winget/apt/brew se faltar).
2. Instala PHP 8.2 se não encontrar (`winget`/`apt`/`brew`).
3. Instala MariaDB Server se não encontrar, e garante que está rodando,
   no Windows, como processo direto (não há serviço registrado, ver
   [Decisões técnicas](#decisões-técnicas-e-problemas-resolvidos)); no
   Linux/macOS, via `systemctl`/`brew services`.
4. Garante que o usuário `root` do banco está acessível sem senha (o que
   `Programacao/CobaiaFront/conn/connect.php`, intocado, espera).
5. Aplica, em ordem: `bancoatualizado.sql`, depois `schema_completo.sql` e
   por fim `seed.sql`.
6. Cria o venv em `Programacao/CobaiaAPI/.venv` e instala as dependências
   (`requirements-dev.txt`, que já inclui as de produção).
7. Prepara o ambiente do `AgenteCore`: venv própria, dependências, o
   Chromium do Playwright, o Ollama e o download do modelo padrão
   (`qwen2.5:7b`; a variável de ambiente `COBAIA_MODELO_LLM` troca o modelo).
   São alguns GB, então esse passo é o último e pode ser interrompido por quem
   só quer rodar o site.

Se algo faltar automatizar no seu SO específico, o script imprime uma
mensagem clara em vez de travar silenciosamente.

### Como rodar

```
# Windows: clique duplo em run.cmd, ou pelo terminal:
run.cmd
```
```bash
# Linux / macOS
./run.sh
```

Isso sobe os três processos (MariaDB se ainda não estiver rodando, PHP,
uvicorn) e imprime:

- **CobaiaFront:** http://localhost:8080
- **CobaiaAPI (docs interativas):** http://localhost:8000/docs

`Ctrl+C` encerra tudo.

#### Contas de teste (já vêm no `seed.sql`)

| Login | Senha | Nível | Uso |
|---|---|---|---|
| `admin` | `admin123` | `sup` | Painel admin (`/admin/login.php`), CRUD de produtos/tipos/usuários |
| `11122233344` | `123456` | `cli` | Área do cliente (`/admin/login.php`, mesmo formulário), reservas |

14 produtos de exemplo já vêm cadastrados.

### Cobaia.exe: instalação, execução e navegador em um clique

No Windows, `Cobaia.exe` (raiz do repositório) faz tudo de uma vez: roda a
instalação completa (idempotente, se já estiver tudo instalado, só
confirma e segue), sobe CobaiaFront + CobaiaAPI, e abre as duas URLs no
navegador padrão assim que os serviços respondem. É o jeito mais direto de
usar o projeto, inclusive pra demonstrar ao vivo no dia da banca.

```
# duplo clique em Cobaia.exe, ou pelo terminal:
.\Cobaia.exe
```

Fecha a janela (ou `Ctrl+C`) pra encerrar tudo (PHP, MariaDB, uvicorn).

**Sobre o aviso do Windows Defender/SmartScreen:** `Cobaia.exe` não é
assinado digitalmente (certificado de assinatura de código custa dinheiro e
não faz sentido pra um projeto acadêmico), é esperado que o Windows mostre
"Windows protegeu seu PC" na primeira execução em uma máquina nova. Clique
em "Mais informações" e depois em "Executar assim mesmo". O `.exe` é gerado a partir
do código-fonte deste mesmo repositório (`Cobaia.py`), sem nenhuma
dependência externa além do que já está documentado aqui.

**Reproduzindo/atualizando o `.exe`:** ele não se autoatualiza, depois de
mudar `Cobaia.py`, `install.py`, `run.py` ou `_env_common.py`, rode:
```powershell
.\build_exe.ps1
```
Isso usa [PyInstaller](https://pyinstaller.org) (instalado num venv
temporário só pra compilar, separado do venv da CobaiaAPI) e regrava
`Cobaia.exe` na raiz. **Importante:** o `.exe` empacota um interpretador
Python só pra rodar a lógica de orquestração (winget/pip/php/uvicorn), ele
**não** usa esse interpretador embutido pra criar o venv da CobaiaAPI, isso
quebra (testado ao vivo: o layout do Python embutido no PyInstaller não é o
de uma instalação normal, faltam os arquivos que o módulo `venv` espera
copiar). Por isso, quando rodando como `.exe`, a criação do venv busca (ou
instala via winget, se faltar) um Python "de verdade" no sistema e delega a
criação pra ele via subprocesso; ver `find_or_install_real_python()` em
`_env_common.py`. As dependências da CobaiaAPI continuam indo exclusivamente
pra `Programacao/CobaiaAPI/.venv`, nunca pro ambiente do `.exe`.

Nos scripts (`install.cmd`/`.ps1`/`.sh`, sem ser via `.exe`), isso nem entra
em jogo, `sys.executable` ali já é um Python real, porque foi ele mesmo
quem rodou o script.

## Navegador recomendado para o agente

Esta pergunta é sobre qual navegador o **`AgenteCore` da Fase 4** deve
automatizar (via Playwright) pra interceptar rede/coletar erros, não afeta
o CobaiaFront/CobaiaAPI em si, que funcionam em qualquer navegador
(Bootstrap 3 + jQuery + `fetch()`, nada específico de motor).

**Recomendação: o Chromium que o próprio Playwright baixa e fixa
(`playwright install chromium`), rodando headless, não o Chrome/Edge
instalado no sistema.**

O motor é Chromium em qualquer um dos casos; a diferença é *qual build*.
Motivos, considerando que o projeto precisa rodar em Windows **e Linux**, de
graça e localmente:

- **Reprodutibilidade dos resultados (o argumento decisivo pra um TCC).** A
  pesquisa mede MTTR e Task Success. O Chrome/Edge do sistema se
  autoatualiza sozinho e é diferente na máquina de cada um dos 9
  integrantes, dois runs do mesmo experimento podem cair em versões
  diferentes do navegador. O Playwright **fixa uma build exata de Chromium
  por versão do Playwright**: todo mundo (e a banca, meses depois) roda
  exatamente o mesmo motor.
- **Mesmo comando nos dois SOs.** `playwright install chromium` é idêntico
  em Windows e Linux e cabe direto no instalador. Usar o Chrome do sistema
  exigiria um caminho de instalação por SO (winget no Windows, repositório
  `.deb`/`.rpm` no Linux), mais peças pra dar errado no "hit and run".
  No Linux, `playwright install --with-deps chromium` ainda instala
  sozinho as libs de sistema que o headless precisa (libnss3, libgbm1 etc.).
- **Não depende do que está instalado.** Máquina corporativa pode ter
  Chrome antigo, travado por política, ou nenhum.
- **Profundidade de interceptação:** o Chromium é o motor "de origem" do
  Playwright (boa parte da equipe veio do Puppeteer/Chrome DevTools), os
  hooks de rede (`page.on('request'/'response')`, `route()`, corpo via
  `response.body()`) são os mais maduros ali, comparado ao wrapper usado
  para Firefox (Juggler) ou WebKit.
- **Headless** é o modo mais testado do mercado inteiro de automação,
  exatamente o que o agente precisa pra rodar em segundo plano.

**Alternativa (uma linha de diferença):** se em alguma máquina o download
de ~150 MB for um problema, ou se a política de TI só permitir binário já
homologado, dá pra apontar pro Chrome instalado com
`browser_type.launch(channel="chrome")`, funciona em Windows e Linux e não
muda mais nada no código. Só perde a garantia de versão fixa. (`channel="msedge"`
existe também, mas aí a portabilidade pro Linux fica pior, já que o Edge não
é padrão lá, por isso não é a recomendação.)

**WebKit/Firefox** não agregam aqui: não há necessidade de validar
comportamento de Safari, e o Firefox tem hooks de rede menos ricos no
Playwright.

Detalhe à parte: o navegador que o `webbrowser.open()` do `Cobaia.exe` abre
(nesta máquina, Firefox, o seu padrão) é só conveniência pra você olhar o
site, **não tem relação nenhuma** com qual navegador o `AgenteCore` vai
automatizar depois, o Playwright sempre sobe sua própria instância
isolada, independente do navegador padrão do sistema.

## CobaiaFront em detalhe

Site de restaurante ("Churrascaria Fornalha"): cardápio público, busca de
produtos, formulário de contato (PHPMailer), painel admin com CRUD
completo, e área de cliente com reservas.

Rotas principais:
- `/index.php`: home (destaques + produtos + carrossel)
- `/produtos_busca.php?buscar=X`, `/produtos_por_tipo.php?id_tipo=X`,
  `/produto_detalhes.php?id_produto=X`
- `/produtos_api.php`: **nova**, consome a CobaiaAPI via `fetch()`
- `/admin/login.php`, que leva a `/admin/index.php` (CRUD produtos/tipos/usuários)
- `/admin/login.php`, que leva a `/cliente/index.php?cliente=<login>` (reservas)

O código PHP em si não foi alterado, exceto um link novo de navegação em
`menu_publico.php` (marcado com `! Alteração de IA - Revisar`) apontando
pra `produtos_api.php` e, desde a Fase 4 (pacote P4), a variante de quebra de
localizador da ficha 29, opção c (decisão 80).

<!-- ! Alteração de IA - Revisar: parágrafo novo (01/11/2026, Fase 4, pacote P4) sobre a variante de quebra de localizador do front.
     ! Motivo: quem abre o repositório precisa saber que `quebra.php` existe, como se liga e que, desligada, o front se comporta como antes; sem o parágrafo, as trocas por `quebra_*()` nas quatro páginas pareceriam alterações sem dono. -->
**Variante de quebra de localizador (Fase 4, P4):** `quebra.php` lê o modo
pelo parâmetro de URL `?quebra=<modo>` (que também grava o cookie `quebra`,
para as páginas seguintes do mesmo roteiro) ou pelo cookie; os modos são
`id_renomeado`, `classe_trocada`, `texto_alterado` e `estrutura_alterada`.
Com o modo ligado, quatro páginas devolvem o HTML com o alvo do roteiro
alterado (o campo de busca em `menu_publico.php`, o campo de login e o botão
Entrar em `admin/login.php`, o botão EXCLUIR em `admin/produtos_lista.php` e o
botão Reservar em `cliente/registrar_reserva.php`); sem modo, ou com um valor
fora da lista, cada função devolve o valor normal e o HTML é o de sempre. O
harness da Fase 4 arma as mesmas quebras pelo navegador
(`cenarios_fase4.QUEBRAS`), e a corrida 19 compara as duas formas.

## CobaiaAPI em detalhe

Documentação interativa (Swagger UI) sempre disponível em
`http://localhost:8000/docs` enquanto o servidor estiver rodando.

| Endpoint | Método | Descrição |
|---|---|---|
| `/api/produtos` | GET | Lista todos os produtos |
| `/api/produtos/{id}` | GET | Detalhe de um produto (404 se não existir) |
| `/api/pedidos?login=<cpf>` | GET | Reservas de um cliente |
| `/api/pedidos` | POST | Cria reserva, `{id_clientes, pessoas, data_pedido}` |
| `/api/pedidos/{id}/cancelar` | POST | Cancela uma reserva |
| `/api/admin/fault-mode` | GET/POST | Liga/desliga modos de falha (ver abaixo) |

### Injeção de falhas (fault injection)

Mecanismo pensado pra viabilizar Fuzzing/Mutação Dinâmica contra a
CobaiaAPI, o agente de QA precisa de um jeito determinístico e
reproduzível de provocar falhas conhecidas.

```bash
curl -X POST http://localhost:8000/api/admin/fault-mode \
  -H "Content-Type: application/json" \
  -H "X-Admin-Token: troque-isto-localmente" \
  -d '{"mode": "type_drift", "target_field": "preco"}'
```

Modos disponíveis (`mode`):

| Modo | Efeito |
|---|---|
| `normal` | Comportamento padrão (default) |
| `error_500` | Responde HTTP 500 |
| `latency` | Atraso artificial de 2s antes de responder |
| `type_drift` | Muda o tipo do campo `target_field` (número ou booleano vira string; string vira o inteiro 1) |
| `field_missing` | Remove `target_field` da resposta |
| `field_renamed` | Renomeia `target_field` para `<campo>_v2` |
| `malformed_json` | Responde um corpo JSON sintaticamente quebrado (truncado) |

<!-- ! Alteração de IA - Revisar: tabela dos quatorze modos novos da ficha 28 (26/10/2026, Fase 4, pacote P2), um por
     causa da taxonomia do AgenteCore, com o nome da própria causa e o campo alvo padrão quando o modo usa campo.
     ! Motivo: os sete modos acima produzem só 6 das 23 causas e só 20 dos 72 casos de avaliação reproduzem na tela;
     a Fase 4 avalia o agente na tela e precisa de um modo por causa; a implementação está em
     `app/fault_injection.py` (apply_fault, apply_fault_lista, resposta_especial) com um teste por modo em
     `tests/test_fault_injection.py`. -->
Modos acrescentados na Fase 4 (cada um leva o nome da causa que produz; `target_field` é opcional nos que
têm campo padrão):

| Modo | Efeito | Campo padrão |
|---|---|---|
| `escala_ou_unidade_errada` | Multiplica o campo numérico por 100 (preço em centavos) | `preco` |
| `formato_de_data_divergente` | Data ISO vira `DD/MM/AAAA` (só nos pedidos, que têm data) | `data_pedido` |
| `chave_de_juncao_errada` | Cada item recebe o `tipo` do item seguinte; no detalhe, o tipo de outro produto | `tipo` |
| `contagem_inconsistente` | A lista vem com um item a menos | |
| `nulo_inesperado` | O campo vem `null` | `tipo` |
| `valor_fora_do_dominio` | Preço negativo, `destaque` vira `"talvez"`, `status` vira `"Pendente"` | `preco` |
| `codificacao_incorreta` | O texto do campo sai com os acentos estragados (UTF-8 lido como Latin-1) | `nome` |
| `registro_duplicado` | O primeiro item da lista vem repetido | |
| `estrutura_aninhada_divergente` | O campo vira um objeto `{"valor": ..., "moeda": "BRL"}` | `preco` |
| `colecao_no_lugar_de_objeto` | `GET /api/produtos/{id}` responde uma lista com um item em vez do objeto | |
| `corpo_vazio` | HTTP 200 com corpo vazio | |
| `corpo_nao_e_json` | HTTP 200 com um HTML de erro no lugar do JSON | |
| `limite_de_requisicoes` | HTTP 429 com `Retry-After: 60` | |
| `recurso_inexistente` | HTTP 404 mesmo com id válido (e na lista) | |

`probability` (0.0–1.0, default 1.0) controla a chance da falha disparar
por requisição, útil pra simular intermitência. Nos modos de item ela é
sorteada por item; nos de lista, uma vez por lista; os de resposta inteira
(`malformed_json`, `corpo_vazio`, `corpo_nao_e_json`, `limite_de_requisicoes`,
`recurso_inexistente`) ignoram a probabilidade.

<!-- ! Alteração de IA - Revisar: documenta o modo de ativação por variável de ambiente.
     ! Motivo: só FAULT_MODE era lido do .env; sem FAULT_TARGET_FIELD os modos com
     campo-alvo não faziam nada no boot. Corrigido em app/config.py, e o README precisa
     dizer como usar, porque é o caminho das execuções determinísticas da Fase 5. -->
Para subir a API **já em modo de falha** (execuções determinísticas, sem
chamar o endpoint admin), defina no `.env`:

```
FAULT_MODE=type_drift
FAULT_TARGET_FIELD=preco
```

O token (`X-Admin-Token`) vem de `ADMIN_TOKEN` no `.env` (veja
`.env.example`); sem o header correto, o endpoint responde 403.

**Detalhe técnico importante:** as rotas montam a resposta como `dict` puro
e retornam via `JSONResponse(content=...)` explícito, em vez de deixar o
FastAPI serializar pelo `response_model` declarado, isso é o que permite a
injeção de falha realmente alterar o formato da resposta; se as rotas
dependessem do `response_model` normal, o Pydantic validaria e filtraria
silenciosamente qualquer campo alterado antes de sair pela rede.
`response_model` continua declarado nas rotas só pra gerar a documentação
OpenAPI do contrato "normal".

## AgenteCore: experimentos com os modelos locais

<!-- ! Alteração de IA - Revisar: (05/11/2026) tabelas de script separadas por fase e células longas quebradas em listas e tabelas menores, sem tirar fato.
     ! Motivo: o Eric pediu (05/11/2026) que os assuntos mais novos tivessem formatação legível, porque a tabela da Fase 3-B juntava scripts de três fases (3-B, Pré-Fase 4 e Fase 4) e tinha células de até 4,4 mil caracteres (`executar_fase4.py`, `avaliar_fase4.py`, `testar_fase4.py`); agora cada fase tem a sua tabela, e o que não cabe numa célula vai para lista logo abaixo. Os parágrafos de resultado, custo e testes da Fase 3 e da 3-B viraram listas curtas. Nenhum nome, número, data ou decisão foi tirado. -->

<!-- ! Alteração de IA - Revisar: seção nova descrevendo a bateria de experimentos e a
     biblioteca de documentação da Fase 2-B.
     ! Motivo: o README ainda dizia que o AgenteCore estava vazio; sem esta seção os
     integrantes não sabem a ordem dos scripts nem que nada deve rodar com outro modelo
     residente no Ollama. -->
Tudo em `Programacao/AgenteCore/experimentos/`, rodando com o Python da venv
do AgenteCore (`Programacao/AgenteCore/.venv`, criada pelo instalador).
**Regra de ouro: um modelo por vez**, os scripts conferem em `/api/ps` que
não há outro modelo residente, e toda inferência é forçada para CPU
(`num_gpu=0`) porque a tese afirma operar sob restrição de hardware local.

**Duas máquinas, duas pastas de resultado.** A Fase 2-A foi medida no Ryzen
de desenvolvimento (`resultados/`, `graficos/`, `relatorio.html` na raiz de
`experimentos/`). A Fase 2-B rodou na **máquina-alvo** (notebook corporativo
i5-1235U, 16 GB, sem GPU) e grava em `resultados_alvo/`, é a variável de
ambiente `RESULTADOS_DIR` (lida por `caminhos.py`) que decide onde cada
script grava e lê, para os dois conjuntos nunca se sobrescreverem. Cada
registro leva o nome da máquina, e `maquina.json` guarda CPU, RAM, sistema e
versão do Ollama. Tempos só são comparáveis dentro da mesma pasta.

| Ordem | Script | O que faz |
|---|---|---|
| 1 | `validar_banco.py --indice` | Valida os 90 casos e a biblioteca (`base_conhecimento/`), mede a recuperação BM25 offline e regrava o `INDICE.md`. Não chama o Ollama. |
| 2 | `verificar_cache_prefixo.py` | Mede se o Ollama reaproveita o cache de KV com prefixo idêntico (decide o custo do braço "biblioteca inteira"). |
| 3 | `executar_bateria.py --modelos M --condicao A0..A5` | Roda os 90 casos; `A0` sem biblioteca (Fase 2-A), `A1` inteira, `A2` top-3 recuperada, `A3` só o verbete certo, `A4` distratores, `A5` verbete errado. Resumível: grava JSONL por caso. |
| 4 | `avaliar.py` | Pontua pelos gabaritos; Δ contra A0, McNemar pareado, IC de Wilson, ancoragem, flips de quantização. |
| 5 | `gerar_graficos.py` / `gerar_relatorio.py` | PNG/SVG para o documento e `relatorio.html` navegável, tudo a partir do JSONL. |
| todos | `rodar_fase2b.ps1` | Orquestra a Fase 2-B inteira **na máquina-alvo**: confere Python/Ollama/RAM/disco, baixa os 8 modelos que faltarem, grava `maquina.json`, refaz a linha de base A0 lá, roda A1–A5 e a avaliação, tudo em `resultados_alvo/`. Um modelo por vez, resumível (Ctrl+C e relançar), ~30–45 h: `powershell -ExecutionPolicy Bypass -File .\rodar_fase2b.ps1`. |

A leitura dos resultados fica em `RESULTADO_FASE2.md` (primeira leva, 2 casos) e em
[`Documentacao/memorial/3-resultados-e-analises/fase-2a-relatorio-por-modelo.md`](Documentacao/memorial/3-resultados-e-analises/fase-2a-relatorio-por-modelo.md)
(Fase 2-A, 90 casos × 3 estratégias × 6 modelos) e em
[`fase-2b-relatorio-por-modelo.md`](Documentacao/memorial/3-resultados-e-analises/fase-2b-relatorio-por-modelo.md)
(Fase 2-B, biblioteca de documentação, 2.610 inferências na máquina-alvo).
Decisões, pesquisa e fontes estão em `Documentacao/Memorial de Desenvolvimento.md`
(índice) e na pasta `Documentacao/memorial/`.

### Fase 3: biblioteca gerida pelo modelo

<!-- ! Alteração de IA - Revisar: subseção nova descrevendo a Fase 3 (biblioteca editada pelo
     próprio modelo, por modelo e por época) e os scripts que a implementam.
     ! Motivo: a Fase 3 só estava descrita no plano aprovado
     (`claude-memoria/plano-aprovado-fase-3.md`); sem esta subseção, quem abrisse o repositório
     não saberia que existe uma bateria nova em implementação, o que cada script novo faz, nem
     como rodar o piloto antes de comprometer a máquina pela bateria completa (~60 h). -->
A Fase 2-B mostrou que a biblioteca **recuperada** (top-3) sobe o acerto em
todos os modelos e que documentação errada é seguida em 93–96% dos casos. A
Fase 3 testa se o próprio modelo consegue **melhorar** essa documentação: em
cada "época", ele diagnostica os 90 casos com a biblioteca atual e, só nos
casos de aprendizado (54 dos 90, com gabarito), propõe acréscimos, nunca
reescreve nem apaga, que passam por validação em código antes de entrar.
Cada modelo evolui a **sua própria cópia** da biblioteca (a original em
`base_conhecimento/` nunca é escrita pela Fase 3); a cópia intocada continua
disponível como L0, o ponto de comparação de todas as épocas seguintes.

<!-- ! Alteração de IA - Revisar: em 12/09/2026 a tabela deixou de marcar seis scripts como
     "(em implementação)", passou a dizer "30 códigos de rejeição em 26 checagens" e registra o
     piloto `-Piloto` executado; a árvore de `resultados_alvo/fase3/` ganhou os arquivos que a
     implementação de fato grava (`maquina.json`, `fase3.log`, `diff__E<n>*`,
     `revisao_edicoes__<slug>.md`, gráficos 12–17 na pasta comum) e o parágrafo de custo cita a
     projeção do executor.
     ! Motivo: todos os scripts existem, foram revisados e rodaram juntos no piloto de
     12/09/2026 (1 modelo, 10 casos, 1 época, 00h13; retomada com hash idêntico), a marca
     "(em implementação)" estava obsoleta. `CODIGOS_REJEICAO` em `evolucao_biblioteca.py` tem
     30 códigos (26 é o número de checagens). E a árvore omitia arquivos que existem em
     `resultados_alvo/fase3_piloto/` (conferida em 12/09/2026): os diffs de época são irmãos
     de `epoca-n/`, fora do snapshot (decisão registrada no livro-razão), e os gráficos da
     corrida oficial vão para `resultados_alvo/graficos/`, não para `fase3/`
     (`caminhos.fase3()`). O custo de ~60 h era só o do plano; o executor projeta 67,18 h. -->
| Script | O que faz | Como rodar |
|---|---|---|
| `evolucao_biblioteca.py` | Parser das propostas de edição do modelo, validador com 30 códigos de rejeição em 26 checagens de ordem fixa (cópia do caso, estouro de teto, vocabulário fora do padrão etc.), aplicação só por acréscimo, hash/diff/fechamento de cada época. | Usado pelos scripts abaixo; não é chamado direto. |
| `executar_fase3.py` | Laço por modelo e por época: diagnóstico com a biblioteca da época anterior, proposta de edição nos casos de aprendizado, validação e aplicação na época seguinte. Resumível por `(modelo, época, caso, tipo)`. | `python executar_fase3.py --modelos M --epocas 3 --saida fase3` |
| `avaliar_fase3.py` | Pontua por modelo × versão da biblioteca (L0..L3) × partição (aprendizado/avaliação/geral); McNemar pareado, Cochran Q entre as 4 épocas, IC de Wilson, trocas entre acerto e erro entre épocas. | `python avaliar_fase3.py` |
| `comparar_fases.py` | Junta 2-A, 2-B e Fase 3 num só `comparacao_fases.json`/`.md`, com os pareamentos que fazem sentido entre fases. | `python comparar_fases.py` |
| `gerar_graficos_fase3.py` | Figuras 12–17: acerto por época, recuperação por época, motivos de rejeição das propostas, crescimento da biblioteca, comparação entre as três fases. | `python gerar_graficos_fase3.py` (venv com matplotlib) |
| `gerar_relatorio_fase3.py` | `relatorio_fase3.html` navegável por modelo/época/partição, com cada proposta de edição (prompt, resposta crua, decisão do validador). | `python gerar_relatorio_fase3.py` |
| `testar_fase3.py` | Testes em Python puro (sem pytest) do parser, do validador, da aplicação de edição e do hash/diff, sem chamar o Ollama, < 30 s. | `python testar_fase3.py` |
| `rodar_fase3.ps1` | Orquestrador da Fase 3 nesta máquina: valida a biblioteca, roda os testes, executa os 4 modelos em sequência, avalia, compara as fases e gera gráficos/relatório. | `.\rodar_fase3.ps1 -Piloto` (amostra pequena, 1 modelo, 1 época) antes da bateria completa: `.\rodar_fase3.ps1` |

Sobre o `rodar_fase3.ps1`:

- O piloto `-Piloto` (1 modelo, 10 casos, 1 época) rodou em 12/09/2026 em 00h13, e o teste de retomada reconstruiu a `epoca-1` com o mesmo hash, validação do encanamento feita.
- A bateria completa rodou em 13–15/09/2026 (57h59, 0 falhas; ver "Resultado da Fase 3" abaixo).

<!-- ! Alteração de IA - Revisar: na tabela acima, a linha de `rodar_fase3.ps1` deixou de dizer que "a bateria completa ainda não rodou".
     ! Motivo: a bateria rodou em 13–15/09/2026 (57h59, 0 falhas; parágrafo "Resultado da Fase 3" abaixo) e a frase, esquecida na revisão de 21/09, contradizia o resto da seção. -->
<!-- ! Alteração de IA - Revisar: duração da Fase 3 corrigida de 58h59 para 57h59 em 30/09/2026, na linha de `rodar_fase3.ps1` da tabela acima e no parágrafo "Resultado da Fase 3".
     ! Motivo: a bateria rodou de 13/09 08:45:25 a 15/09 18:44:56 pelos marcos do `fase3.log`; a linha FIM do log diz 58h59 porque o script convertia as horas com `[int]`, que no PowerShell arredonda para o inteiro mais próximo. O defeito apareceu na ponte de 30/09 (1h46 gravadas como 02h46) e foi corrigido nos três scripts de bateria. -->
Cada modelo grava em `resultados_alvo/fase3/`:

<!-- ! Alteração de IA - Revisar: na árvore abaixo, o fase3.log passou a "versionado" (29/09/2026).
     ! Motivo: desde 29/09 o .gitignore tem uma exceção ao *.log para resultados_alvo/**/*.log, a pedido do Eric (decisão 63); a nota antiga dizia que o log ficava fora do git. -->
```
fase3/
  maquina.json               máquina, versão do Ollama, RAM e horário de início (relances são acrescentados, não sobrescrevem)
  particao.json              divisão determinística dos 90 casos em aprendizado (54) e avaliação (36)
  fase3.log                  registro corrido da execução, gravado pelo rodar_fase3.ps1 (versionado: exceção ao *.log no .gitignore)
  bibliotecas/<slug>/
    epoca-0..3/               snapshot completo da biblioteca do modelo ao fechar cada época (verbetes + INDICE.md + fechamento.json)
    diff__E<n>.{json,md}      o que a época n acrescentou em relação à anterior (irmão de epoca-n/, fora do snapshot)
    diff__E<n>__vs_original.{json,md}   idem, em relação à biblioteca original
    historico.jsonl           uma linha por edição aceita
  <slug>/
    diagnosticos__L0..L3.jsonl   diagnóstico dos 90 casos com cada versão da biblioteca
    propostas__E1..E3.jsonl      propostas de edição e a decisão do validador, por época
  avaliacao_fase3.json, resumo_fase3.json      métricas por modelo/época/partição
  comparacao_fases.json/.md                    2-A × 2-B × Fase 3 lado a lado
  revisao_edicoes__<slug>.md                   amostra de até 30 edições aceitas por modelo, para o Eric marcar Correta/Parcial/Errada
  relatorio_fase3.html                         relatório navegável
../graficos/12-…17-…          figuras 12–17 na pasta comum de gráficos (resultados_alvo/graficos/); só o piloto grava em fase3_piloto/graficos/
```

<!-- ! Alteração de IA - Revisar: segunda passada de 12/09/2026, o comando da projeção
     ganhou `--modelos` com os quatro modelos.
     ! Motivo: `python executar_fase3.py --so-projecao` sozinho encerra com "the following
     arguments are required: --modelos" (`required=True` no argparse de `executar_fase3.py`);
     o 67,18 h só se reproduz com os quatro modelos na linha de comando, que é o que
     `rodar_fase3.ps1` faz antes da corrida (saída conferida em 12/09/2026). -->
**Estimativa de custo:**

- No plano: **~60 h de máquina** para os 4 modelos × 3 épocas.
- A projeção que o executor imprime, com os ms/token medidos na 2-B, dá **67,18 h**. `--modelos` é obrigatório, e este é o comando que `rodar_fase3.ps1` roda antes da corrida:

```
python executar_fase3.py --so-projecao --modelos granite4.2:8b qwen2.5:7b qwen2.5-coder:7b qwen2.5-coder:3b
```

- O piloto de 10 casos (`-Piloto`) rodou em 12/09/2026 em 00h13, `qwen2.5-coder:3b`, 1 época, 0 de 6 propostas aceitas. Ele valida o encanamento, não o custo dos quatro modelos.
- A bateria é **retomável**: interromper com Ctrl+C e rodar de novo continua da mesma época e do mesmo caso, sem repetir trabalho já fechado.

<!-- ! Alteração de IA - Revisar: em 21/09/2026 entraram o parágrafo "Resultado da Fase 3", a subseção "Fase 3-B" e a seção "Ferramentas de apoio".
     ! Motivo: a bateria da Fase 3 rodou em 13–15/09/2026 e o README ainda descrevia só a preparação; a Fase 3-B (executor próprio, sem tocar nos scripts oficiais) e a pasta `ferramentas/` são novas no repositório e ninguém saberia para que servem sem esta descrição. Números só com origem: `resultados_alvo/fase3/fase3.log` e `comparacao_fases.md`. -->
**Resultado da Fase 3 (13–15/09/2026):**

- A bateria rodou na máquina-alvo de 13/09 08:45 a 15/09 18:44 (57h59, sem falhas, Ollama 0.34.0).
- A linha `FIM` do `fase3.log` diz 58h59 porque o script arredondava a hora.
- Foram 2.088 inferências, e os resultados estão em `resultados_alvo/fase3/` (commit `b9f9ad9`).
- As tabelas por modelo e fase estão em `resultados_alvo/fase3/comparacao_fases.md`.
- A leitura está no Memorial (`Documentacao/memorial/3-resultados-e-analises/`, relatório e comparação preenchidos em 22/09/2026).
- **Decisão do modelo (22/09/2026, decisão 52): `qwen2.5:7b` com a biblioteca no estado L1**, pela regra pré-registrada (`decidir_modelo.py`, que grava `resultados_alvo/fase3/decisao_modelo.md`).
- Números da decisão: 91,7% de acurácia balanceada nos 36 casos de avaliação, sem veto por autoenvenenamento; P(top-1) de 77,6% no bootstrap.
- Análise completa em `Documentacao/memorial/3-resultados-e-analises/analise-decisoria-modelo-final.md`.
- As tabelas do Memorial saem de `gerar_tabelas_relatorio_fase3.py` como blocos conferidos por `--check` (`resultados_alvo/fase3/tabelas_relatorio.md`).

### Fase 3-B: ponte de versão e testes complementares

Depois da bateria o Ollama atualizou sozinho de 0.34.0 para 0.34.1 e, em 30/09,
para 0.34.4. Qualquer inferência nova passa antes por uma **ponte de versão** (L0
nos 36 casos de avaliação) que mede se o runtime novo reproduz o antigo; só então os
testes complementares escolhidos em 23/09/2026 (decisão 56): os 36 casos inéditos,
que rodaram em 28/09, e a troca cruzada de bibliotecas entre modelos, que rodou de
30/09 para 01/10; a sonda de detecção de correção, a ablação base × instruct e o
experimento do recuperador entraram depois. Tudo roda por um executor **próprio**, que
lê **cópias** dos snapshots oficiais e nunca altera `executar_fase3.py`,
`estrategias.py`, `evolucao_biblioteca.py` nem `resultados_alvo/fase3/`.

| Script | O que faz | Como rodar |
|---|---|---|
| `executar_fase3b.py` | Modos `ponte`, `cruzada` (`--doador`, `--versoes`), `texto_max` (`--texto-max`, só granite), `a5` e `ineditos`; copia o snapshot pedido para a pasta da saída, grava `condicoes_3b.json` e `maquina.json` e chama a "passada final" de `executar_fase3.rodar_epoca` (só diagnóstico). | `python executar_fase3b.py --modo ponte --saida fase3b_ponte --modelos …` |
| `avaliar_fase3b.py` | Avalia a saída de um modo: os quatro primeiros delegam a `avaliar_fase3.avaliar_saida`; `ineditos` agrega com o gabarito de cada registro. | `python avaliar_fase3b.py --saida fase3b_ponte` |
| `testar_fase3b.py` | Testes sem LLM (cópia preserva o hash, modos aplicam e restauram `TEXTO_MAX`/`CONDICAO`, área oficial intocada antes e depois da suíte). | `python testar_fase3b.py` |
| `rodar_fase3b.ps1` | Orquestrador: testes, um modelo por vez com checagem de RAM (pula e lista o modelo se faltar memória; relançar retoma), avaliação ao fim. | `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo ponte -Saida fase3b_ponte` |
| `decidir_modelo.py` (+ `pesos_decisao.json`, `gerar_graficos_decisao.py`) | Decide modelo e estado da biblioteca pela regra pré-registrada (decisão 36) e mede a robustez; grava `decisao_modelo.json/.md` (documento derivado) e a figura 18. | `python decidir_modelo.py --saida fase3 --saidas-3b fase3b_ponte` (`--check` confere) |
| `gerar_tabelas_relatorio_fase3.py` | Tabelas do relatório da Fase 3, da comparação entre fases e da análise decisória (Memorial) a partir de `resumo_fase3.json`, `comparacao_fases.md`, `decisao_modelo.md` e `fase3.log`, como blocos `<!-- tabela:NOME -->`; `--check` acusa qualquer bloco colado que difira do regerado. | `python gerar_tabelas_relatorio_fase3.py --saida fase3 [--check]` |
| `sonda_correcao.py` | Sonda de **detecção de correção** (28/09/2026, decisão 58): roda uma época de aprendizado do executor oficial sobre uma cópia de um snapshot fechado, só com os casos corrigidos, e imprime o que o modelo diagnosticou e propôs ao rever um caso cuja documentação (escrita por ele mesmo) ficou desatualizada; saída em `resultados_alvo/<saida>/`. | `RESULTADOS_DIR=resultados_alvo python sonda_correcao.py --saida fase3b_correcao --modelo qwen2.5:7b --versao 1 --casos efe-3 efe-10` |
| `curar_biblioteca.py` | Curadoria da biblioteca L1 do `qwen2.5:7b` (29/09/2026, ficha 2), em dois passos (`--listar` e `--curar`, descritos abaixo da tabela); grava `curadoria.json`. | `RESULTADOS_DIR=resultados_alvo python curar_biblioteca.py --listar` |
| `comparar_qwen_coder.py` | Comparativo `qwen2.5:7b` × `qwen2.5-coder:7b` em todas as fases (29/09/2026, ficha 4); grava `resultados_alvo/fase3/comparativo_qwen_coder.{json,md}`. | `RESULTADOS_DIR=resultados_alvo python comparar_qwen_coder.py` |
| `experimento_recuperador.py` | Experimento offline do recuperador (29/09/2026, ficha 11f): BM25 com sinais × embedding denso (`embeddinggemma:300m`, consulta por termos e por texto) × híbrido RRF. | `RESULTADOS_DIR=resultados_alvo python experimento_recuperador.py --embedding embeddinggemma:300m` |
| `analisar_fase3b.py` | Análise de fechamento da Fase 3-B (01/10/2026); grava `resultados_alvo/fase3/analise_fase3b.{json,md}`. | `RESULTADOS_DIR=resultados_alvo python analisar_fase3b.py [--check]` |

O que não coube nas células da tabela:

- `sonda_correcao.py`, desde o P5 (03/11/2026):
  - `--recuperacao-por-id`: os verbetes ligados ao caso pelo id entram no contexto, por `biblioteca_fase4.com_recuperacao_por_id`.
  - `--origem`: outra época fechada no lugar da L1 oficial.
  - `rodar_sonda` e `resumo_da_sonda`: chamados pelo modo `biblioteca` de `executar_fase4.py` na mesma sessão do Ollama.
  - `menciona_correcao`: a resposta fala da correção registrada?
- `decidir_modelo.py`:
  - Mede a robustez com bootstrap, estabilidade, Pareto e escore ponderado com sensibilidade.
  - Pareia as saídas da 3-B com a Fase 3 e apura a revisão das edições.
- `curar_biblioteca.py`:
  - `--listar` escreve a planilha `resultados_alvo/fase3/curadoria_L1__qwen2.5_7b.md` (40 edições da época 1, 10 com veredito da planilha oficial).
  - `--curar --destino ../biblioteca_producao` reconstrói a cópia de produção a partir da época 0, reaplicando só o que não for *Errada*, depois de conferir que reaplicar tudo reproduz o hash oficial; grava `curadoria.json`.
- `comparar_qwen_coder.py`:
  - Faz tabelas, o confronto caso a caso (McNemar exato), o confronto nos 36 inéditos por versão e por classe (06/10/2026) e a lista de toda célula em que o Coder fica à frente.
  - `--colar` cola os blocos em `Documentacao/memorial/3-resultados-e-analises/comparativo-qwen25-7b-vs-coder-7b.md`; `--check` confere.
- `experimento_recuperador.py`:
  - Roda com k = 1/3/5, nos 90 oficiais e nos 36 inéditos, com as bibliotecas L0/L1/L3.
  - Saída em `resultados_alvo/recuperador/` (`.json` registro, `.md` derivado com `--check`).
- `analisar_fase3b.py`:
  - Cobre as pontes de versão, os casos que mudam entre corridas iguais, os inéditos somados aos oficiais (72 casos) e a troca cruzada pareada contra a ponte, contra a própria biblioteca e contra o doador.
  - Desde 06/10/2026 traz também o Coder 7B contra o qwen nos mesmos inéditos (corrida 7) e a adesão cega com a L3 própria (corrida 5).
  - `--colar` cola os blocos em `Documentacao/memorial/3-resultados-e-analises/fase-3b-relatorio.md`; `--check` confere.

Cada modo grava em `resultados_alvo/<saida>/` a mesma árvore da Fase 3 (snapshots
copiados em `bibliotecas/<slug>/`, `diagnosticos__L<n>.jsonl` por modelo,
`avaliacao_fase3.json`, `resumo_fase3.json`) mais `condicoes_3b.json` (modo, doador,
versões, teto de texto, condição, versão do Ollama). A ponte de 21/09/2026 cobriu
`qwen2.5-coder:3b`, `qwen2.5:7b` e `qwen2.5-coder:7b` (b/c 0/0, 1/1 e 0/0 nos 36:
pareáveis com a Fase 3); o `granite4.2:8b` foi pulado duas vezes por RAM (8 GB
exigidos, 7,8 GB livres) e ficou fora da 3-B (decisão 52).

<!-- ! Alteração de IA - Revisar: parágrafo novo (01/10/2026) com o resultado da Fase 3-B, a linha de `analisar_fase3b.py` na tabela acima e o estado da 3-B no topo e na tabela de fases.
     ! Motivo: a troca cruzada rodou de 30/09 para 01/10 e era o último teste previsto; o README ainda dizia que ela estava pendente. Números de `resultados_alvo/fase3/analise_fase3b.json`. -->
**Resultado da Fase 3-B (01/10/2026):**

- A segunda ponte, em Ollama 0.34.4, deixou o `qwen2.5-coder:7b` fora do limite (b/c 3/1 nos 36); por isso a troca cruzada é lida contra essa ponte.
- Nos 36 casos inéditos o ganho da biblioteca L1 não reaparece: 72,2% contra 75,0% com a biblioteca original; a L3 chega a 80,6%.
- Na troca cruzada, a biblioteca escrita pelo `qwen2.5:7b` dá 1 caso de saldo ao Coder 7B e tira 4 do Coder 3B, contra 88,9% de acerto quando lida por quem a escreveu.
- Conclusão: o padrão do agente é o modelo com a biblioteca que ele mesmo escreveu (decisão 69).
- Com a mesma entrada, entre corridas iguais mudam de 0 a 3 casos em 36.
- A análise sai de `analisar_fase3b.py`, e o relatório, com a lista de fechamento das Fases 3 e 3-B, está em `Documentacao/memorial/3-resultados-e-analises/fase-3b-relatorio.md`.

<!-- ! Alteração de IA - Revisar: parágrafo abaixo com os testes da 3-B escolhidos pelo Eric em 23/09/2026, os comandos na forma que o Windows PowerShell aceita por -File (listas separadas por vírgula) e o efeito da decisão do modelo no instalador.
     ! Motivo: o texto anterior dizia "testes a escolher"; a escolha saiu (decisão 56) e o comando registrado antes nas pendências, com a lista separada por espaço, falha na vinculação de parâmetros do PowerShell (conferido em 23/09/2026 com um script de teste). O `install.py` passou a baixar o `qwen2.5:7b` e os outros modelos ficam só como registro. -->
**Testes da 3-B escolhidos (23/09/2026, decisão 56), já rodados: os casos inéditos em 28/09 e a troca cruzada de 30/09 para 01/10.**

Na ordem escolhida, primeiro a **troca cruzada**, as bibliotecas L1 e L3 do `qwen2.5:7b` lidas pelos dois Coder nos 36 casos de avaliação:

```
powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo cruzada -Saida fase3b_cruzada_qwen -Doador qwen2.5:7b -Versoes 1,3 -Modelos qwen2.5-coder:7b,qwen2.5-coder:3b
```

Depois os **casos inéditos** (`banco_casos_ineditos.py`: 36 casos novos, 2 por célula classe × nível, escritos só a partir do código do cobaia, ids `lex-16` a `efe-21`), com o `qwen2.5:7b` e o 3B em L0, L1 e L3:

```
powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo ineditos -Saida fase3b_ineditos -Versoes 0,1,3 -Modelos qwen2.5:7b,qwen2.5-coder:3b
```

- As listas vão separadas por **vírgula** (`-File` do Windows PowerShell 5.1 vincula `a b` como dois argumentos e falha).
- Com a decisão tomada, o `install.py` passou a baixar o `qwen2.5:7b` por padrão.
- Os outros modelos ficam só como registro histórico, resultados, gráficos e o veredito de cada um em `Documentacao/memorial/3-resultados-e-analises/analise-decisoria-modelo-final.md` §8.
- O painel do projeto reúne pendências em fichas, roadmap com os comandos prontos e todos os números dos testes numa página só:
  - arquivo: `Documentacao/dashboard/painel-do-projeto.html` (gerado por `ferramentas/gerar_dashboard.py`);
  - publicado em https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN para leitura de qualquer lugar.
- O estado por fase, com o que falta rodar, está em `Documentacao/memorial/roadmap.md`.
- As decisões que esperam resposta, em fichas, estão em `Documentacao/memorial/pendencias.md`.

### Pré-Fase 4: scripts

<!-- ! Alteração de IA - Revisar: linhas novas (01/10/2026) para os scripts da Pré-Fase 4 nas duas tabelas, a fase na tabela de fases e no estado do topo.
     ! Motivo: decisão 70 (pausa de pesquisa antes da Fase 4); os scripts são novos no repositório e o README é a porta de entrada que diz o que cada um faz. -->
| Script | O que faz | Como rodar |
|---|---|---|
| `viabilidade_modelos_grandes.py` | Para cada família de modelo do repositório colibri, diz se cabe no disco e na RAM desta máquina, quanto o disco custaria por token e quanto levaria a nossa resposta mediana nas velocidades medidas por terceiros. | - |
| `sondar_logprobs.py` | Confere com três chamadas o que o Ollama devolve de probabilidade por token (`logprobs`, `top_logprobs`) e traz o gancho `com_logprobs`, que acrescenta os dois campos à chamada de `cliente_ollama.gerar` sem mudar o que ela devolve. | - |
| `sonda_confianca.py` (+ `rodar_sonda_confianca.ps1`) | O modelo decidido com a biblioteca dele nos 36 casos oficiais de avaliação e nos 36 inéditos, com o mesmo executor e o mesmo prompt da Fase 3; grava a probabilidade de cada token em `logprobs__L<n>.jsonl`. | - |
| `analisar_confianca.py` | Analisa a sonda de confiança: acha nos tokens gravados o trecho do rótulo da causa e mede se a probabilidade dele separa acerto de erro. | - |
| `pre_fase4.py` | Pasta dos derivados da fase (`resultados_alvo/pre_fase4/`) e a rotina comum de gravar, conferir (`--check`) e colar os blocos de tabela de cada script no relatório. | - |
| `trilha.py` | A trilha do agente: o arquivo bruto com uma linha JSON por evento, em três camadas que não se misturam. | - |
| `gerar_relatorio_raciocinio.py` | Gera, só da trilha, o relatório para humanos de cada diagnóstico (passo a passo nas três camadas; a resposta certa aparece numa seção só), o índice de cada corrida e os indicadores somados. | - |
| `gerar_atlas.py` | O atlas do projeto com os dados já medidos, pelo método do `expert_atlas` do colibri: para cada versão da biblioteca, em quantos casos de cada classe de defeito cada verbete entrou no contexto. | - |
| `testar_pre_fase4.py` | Testes sem LLM da Pré-Fase 4 (leitura do disco, gancho das probabilidades, conta de viabilidade, sonda de confiança com Ollama de mentira, trilha, relatório de raciocínio, atlas, pastas oficiais intocadas antes e depois). | - |

O que não coube nas células da tabela:

- `viabilidade_modelos_grandes.py` grava `resultados_alvo/pre_fase4/viabilidade_modelos_grandes.{json,md}` (`--check`, `--colar`).
- `sonda_confianca.py`:
  - Grava a probabilidade ao lado do registro, que mantém as 37 chaves oficiais.
  - Com `--curada` (`-Curada` no `.ps1`) roda também a cópia curada da L1 (`biblioteca_producao/`), gravada como L100 e lida como "L1 curada" nas análises (ficha 18).
- `analisar_confianca.py`:
  - Calcula a probabilidade conjunta do trecho do rótulo (a medida principal, fixada antes da corrida), a do primeiro token e a massa das alternativas que levariam a outra causa.
  - Mede se separam acerto de erro (AUROC com intervalo por reamostragem dos casos, risco por cobertura, quantos erros uma parcela de revisão humana pega), ao lado dos dois sinais que não custam inferência.
  - Desde 06/10/2026 mede também o acerto de cada biblioteca e os pares caso a caso (a cópia curada contra a L1 e a L0; contra as corridas anteriores), com a rota da cópia curada recalculada pela busca.
  - Grava `resultados_alvo/pre_fase4/confianca.{json,md}` (`--check`, `--colar`). O script da noite roda a análise no fim.
- `trilha.py`:
  - Cada evento traz o caso, os verbetes que a busca pontuou e entregou, o prompt, a resposta, o que o modelo declarou e o que o código conferiu.
  - O adaptador remonta a trilha das corridas já gravadas, sem rodar modelo, e diz até onde o prompt remontado está provado.
  - `--errata` recupera do git o texto antigo dos dois casos corrigidos em 28/09.
- `gerar_relatorio_raciocinio.py`: `--vitrine` grava as trilhas e os relatórios versionados em `resultados_alvo/pre_fase4/` (`--check`, `--colar`).
- `gerar_atlas.py`:
  - Mede também a especialização, a validação deixando um caso de fora, as citações e as trocas entre causas de cada corrida e a rota de cada caso.
  - Grava `resultados_alvo/pre_fase4/atlas.{json,md}` (`--check`, `--colar`).

### Fase 4: o agente na tela

<!-- ! Alteração de IA - Revisar: linhas dos módulos da Fase 4 (26/10/2026, pacotes P0 a P2 do plano aprovado) e, em 27/10/2026, a linha do banco de inéditos da ficha 27 e as opções `--banco` (executor) e `--nome`/`--titulo` (avaliador) com a corrida sobre os inéditos; ainda em 27/10/2026 (pacote P3), a linha de `diagnostico_ao_vivo.py` e os modos `calibracao` e `tela`, as leituras `--calibracao`, `--tela` e `--pontes` e os testes do P3 nas linhas de `executar_fase4.py`, `avaliar_fase4.py` e `testar_fase4.py`.
     ! Motivo: a Fase 4 é a do agente na tela e entrou no harness em arquivos novos (navegador, interceptador, poda, caso ao vivo, cenários, orquestrador, avaliação), mais a trilha v2 e o relatório v2 em `trilha.py` e `gerar_relatorio_raciocinio.py`; quem abre o repositório precisa achar cada um pelo nome. O banco de inéditos da Fase 4 é um arquivo a mais no mesmo molde de `banco_casos_ineditos.py` e precisa constar aqui com o seu estado (ainda não conferido pelo Eric, ainda fora do executor). O P3 é o primeiro pacote com modelo: quem for lançar as corridas 16 e 18 precisa achar aqui o módulo do diagnóstico, os modos e o que cada leitura grava. -->
<!-- ! Alteração de IA - Revisar: (01/11/2026, Fase 4, pacote P4) as linhas de `cenarios_fase4.py`, `executar_fase4.py`, `avaliar_fase4.py` e `testar_fase4.py` ganharam a cura de seletor (modo `cura`, leitura `--cura`, catálogo de quebras, testes do P4) e entrou a linha de `cura_seletor.py`.
     ! Motivo: o pacote P4 é o da cura de seletor e da corrida 19; quem abre o repositório precisa achar o módulo e os modos pelo nome. -->
<!-- ! Alteração de IA - Revisar: (04/11/2026, Fase 4, pacote P6) as linhas de `cenarios_fase4.py`, `executar_fase4.py`, `avaliar_fase4.py` e `testar_fase4.py` ganharam os cenários da Fase 5 (catálogo do ensaio, modo `cenarios`, leitura `--cenarios`, testes do P6) e entrou a linha de `linha_de_base_manual.py`.
     ! Motivo: o pacote P6 é o dos cenários da Fase 5 e da corrida 21; quem abre o repositório precisa achar o módulo, o modo e o ajudante da linha de base manual pelo nome. -->
<!-- ! Alteração de IA - Revisar: (04/11/2026 à noite, Fase 4, pacote P7) as linhas de `executar_fase4.py`, `avaliar_fase4.py` e `testar_fase4.py` ganharam a avaliação da própria trilha (modo `avaliacao_trilha`, leitura `--trilha`, testes do P7) e entrou a linha de `avaliacao_trilha.py`.
     ! Motivo: o pacote P7 é o da avaliação da trilha e da corrida 22; quem abre o repositório precisa achar o módulo, o modo e a leitura pelo nome. -->
| Script | O que faz | Como rodar |
|---|---|---|
| `ambiente_fase4.py` | (P0) Grava `resultados_alvo/fase4/ambiente.json` com as versões do Python, do Playwright, do navegador e do Ollama, o canal do navegador e o que a máquina tem das cobaias (`--check` compara com a máquina atual). | - |
| `navegador.py` | (P0) Abre o Chromium fixo do Playwright em headless (ou o Edge pelo canal `msedge`) e captura a árvore de acessibilidade como texto (snapshot ARIA) e como nós (papel, nome, profundidade, atributos); `--fixture URL` grava uma amostra em `fixtures_fase4/`. | - |
| `interceptador.py` | (P2) Escuta as chamadas da página à CobaiaAPI (método, caminho, status, tempo, hash do corpo) e monta a aresta "chamada HTTP" entre a página PHP e a rota. | - |
| `poda.py` | (P2) A poda em código: reduz a árvore ao que o roteiro toca e ao entorno, na forma textual dos casos gravados, com contagens e regras; compara o corpo HTTP com o contrato textual e devolve só o diff e o trecho em disputa. | - |
| `caso_ao_vivo.py` | (P2) O caso ao vivo no formato dos casos gravados, sem gabarito: contrato, sintoma e a montagem com as chaves que o prompt congelado conhece. | - |
| `cenarios_fase4.py` | (P2) O catálogo de cenários das duas cobaias em dados, o executor que roda os passos no Playwright e o critério de Task Success da Fase 5; cresceu nos pacotes P4 e P6 (lista abaixo). | - |
| `diagnostico_ao_vivo.py` | (P3) O diagnóstico ao vivo do agente, sem gabarito: contexto da busca, prompt congelado, uma inferência com as probabilidades por token e o registro com as 37 chaves oficiais; lista por pacote abaixo. | - |
| `cura_seletor.py` | (P4) A cura de seletor, sem modelo: gera os seis candidatos da árvore podada e do alvo registrado na corrida de referência, verifica cada um em código e escolhe o primeiro que passa. | - |
| `biblioteca_fase4.py` | (P5) A biblioteca em produção e o ciclo de correção, sem mudar `evolucao_biblioteca.py`; lista abaixo. | - |
| `banco_casos_ineditos_fase4.py` | (ficha 27) Mais 36 casos inéditos para o conjunto de avaliação (2 por célula classe × nível, ids `lex-22` a `efe-27`, no mesmo formato de `banco_casos.py`). | - |
| `executar_fase4.py` (+ `rodar_fase4.ps1`) | Orquestrador no molde do da 3-B, com um modo por corrida (tabela de modos abaixo). | - |
| `avaliar_fase4.py` | Lê as corridas e grava os derivados em `resultados_alvo/fase4/`, com uma opção por leitura (tabela abaixo). | - |
| `testar_fase4.py` | Testes sem LLM da Fase 4, listados por pacote abaixo. | - |
| `linha_de_base_manual.py` | (P6) O ajudante da sessão da linha de base manual da Fase 5 ([protocolo](Documentacao/memorial/5-metodo-e-ferramental/protocolo-linha-de-base-manual.md)), com quatro comandos (lista abaixo). | `python linha_de_base_manual.py armar --vez 1 3` |
| `avaliacao_trilha.py` | (P7) A avaliação da própria trilha (especificação da trilha, seção 12); lista abaixo. | usado por `executar_fase4.py --modo avaliacao_trilha` e `avaliar_fase4.py --trilha` |
| `corridas_em_texto.py` | (decisões 91 e 92) As corridas 23 e 24, em texto: as condições do experimento como transformação do prompt pronto, a leitura da linha CAUSA_RAIZ inteira e os resumos das duas. | modos `experimento_prompt` e `ineditos` de `executar_fase4.py` |
| `conferir_corte_tela.py` | (decisões 90, 96, 97 e 99) Hoje compara com as corridas 18d, 18e e 21d, diz se o prompt ficou igual byte a byte, mede com o Ollama os que mudaram de tamanho (`--medir-tokens`) e grava `teto_prompt_tela.json`; as conferências anteriores ficam em `corte_prompt_tela.json` e `busca_prompt_tela.json`. Monta sem modelo, com as cobaias de verdade, o prompt das corridas 18c e 21c e compara com o guardado: tokens estimados, verbetes recuperados e verbete certo. | grava `resultados_alvo/fase4/corte_prompt_tela.json` |
| `gerar_conferencia_ineditos.py` | (decisão 92) O documento da conferência dos 36 inéditos: cada caso, o que a corrida 17 viu e a pré-análise. | grava `resultados_alvo/fase4/conferencia_ineditos.{json,md}` |
| `rodar_pendencias_fase4.ps1` | Fila das corridas 18c, 21c e 23 pelo `rodar_fase4.ps1`, parando na primeira que falhar. | janela do Eric |
| `gerar_figuras_documentos.py` (+ `testar_figuras_documentos.py`) | Figuras do README e do documento do TCC, em `Documentacao/figuras/`, e a tabela de cada uma em `dados-das-figuras.md`, tudo lido dos JSON de `resultados_alvo/`. | `../.venv/Scripts/python.exe gerar_figuras_documentos.py` (com matplotlib); `--check` confere sem desenhar |
| `cache_respostas.py` (+ `testar_cache_respostas.py`) | Cache **exato** de respostas do Ollama (SQLite; chave = modelo, digest, prompt, opções) para reexecuções de conveniência e para o laço de desenvolvimento da Fase 4. | `set CACHE_RESPOSTAS=1` e `gerar_com_cache(...)` no lugar de `cliente_ollama.gerar` |

O que não coube nas células da tabela:

- `interceptador.py`:
  - Captura a árvore com os atributos do DOM dos interativos.
  - Aplica a lista de hosts permitidos: CDNs servidas do HAR em `fixtures_fase4/cdn.har`; o mapa do rodapé é bloqueado sem incidente; qualquer outro host vira incidente.
  - `--gravar-har` regrava o HAR.
- `poda.py`:
  - O entorno que a poda mantém é: interativos, textos, estados, marcos; os cartões além dos três primeiros e do alvo viram uma linha de contagem.
  - O diff do corpo com o contrato aponta: campo ausente, renomeado, tipo diferente, fora do domínio, nulo, forma, corpo vazio, não JSON ou truncado.
  - Desde 05/11/2026 (decisão 89), `diff_contrato` compara todos os itens de uma lista e trata número em campo booleano pela regra da biblioteca.
- `caso_ao_vivo.py`:
  - Contrato lido do `openapi.json` da CobaiaAPI (`fixtures_fase4/openapi.json`, com o ajuste do `preco`).
  - Sintoma por molde em código: a conferência que falhou, o diff do corpo e o diff da árvore contra a referência em modo normal; nunca o nome do modo nem da causa.
- `cura_seletor.py`:
  - Os seis candidatos seguem a ordem fixa do plano: papel e nome; papel e nome parecido acima do limiar 0,6; texto contido; `data-id`; caminho a partir do ancestral com id; posição entre os irmãos do mesmo papel.
  - A verificação em código segue a ordem fixa: um elemento só, visível e habilitado, mesmo papel, nome parecido, efeito na reexecução.
  - Escolhe o primeiro que passa, com todos os candidatos e o resultado de cada verificação no evento `cura` da trilha v2 e os nós `cura` e `reexecucao`.
  - A regra R3 usa a impressão do DOM (mesmo elemento contra outro elemento).
  - Traz as funções que descrevem o alvo e resolvem os candidatos na página do Playwright.
- `banco_casos_ineditos_fase4.py`:
  - Entregue em 27/10/2026 por um agente que leu só o código das cobaias e os 14 modos novos.
  - Cada caso anota a fonte (arquivo:linha) e o modo da API que o reproduz, ou "sem modo" quando é um cenário descrito.
  - Os corpos foram cruzados com a CobaiaAPI real no mesmo dia.
  - O Eric os conferiu em 06/11/2026, sem mudar nenhum (ficha 46, decisão 100). O modelo leu 25 deles na corrida 18e; os 36 em texto são a corrida 24: 25 de 36. <!-- ! Alteração de IA - Revisar: (05/11/2026) a frase deixa de dizer que os casos ainda não entram no executor. ! Motivo: dizia "antes da corrida 16" e "ainda não entram", mas a corrida 17 os leu pelo --banco em 27/10, e a decisão 92 fixou a corrida 24 para ler esses casos com o modelo. -->
- `cache_respostas.py`: desligado por padrão (`CACHE_RESPOSTAS=1` liga), recusa em `resultados_alvo/` e marca todo acerto com `do_cache=True` e tempos zerados; nunca entra numa corrida medida (decisão 48).

#### `cenarios_fase4.py`, por pacote

- P2:
  - O catálogo de cenários das duas cobaias em dados: catálogo e detalhe em `produtos_api.php`; busca, login do administrador, lista de produtos e reserva do cliente no front legado.
  - O executor que roda os passos no Playwright capturando a árvore e parando na primeira conferência que falha.
  - A tabela causa para modo de injeção, o cronômetro do MTTR e o critério de Task Success da Fase 5.
- P4 (01/11/2026):
  - O catálogo das 16 quebras de localizador (`QUEBRAS`): quatro roteiros do front legado x quatro modos, cada célula com o localizador do passo do alvo, o alvo e as mutações.
  - O script determinístico que o harness injeta por `add_init_script` (`script_de_quebra`).
  - `armar_quebra` nas duas formas (harness e cookie da variante do PHP) e `cenario_com_localizador`.
- P6 (04/11/2026):
  - Os dez cenários do ensaio da Fase 5 (`CENARIOS_DO_ENSAIO`): seis de contrato em `produtos_api.php`, um por modo, com `latency` trocado por `escala_ou_unidade_errada` em `preco` para cobrir as cinco classes de contrato, `TROCA_DA_FICHA_36`, e quatro de localizador, um por roteiro do front legado com um modo de quebra.
  - O cronômetro em relógio monotônico (`mttr_monotonico`).
  - A conferência do diagnóstico e o Task Success do contrato pela ficha 35 (`diagnostico_conferido`, `task_success_contrato`).
  - A troca do localizador quebrado por outro seletor (`roteiro_com_seletor`, a mesma na cura e na linha de base manual).
  - A ficha da falha de um roteiro que parou (`motivo_do_roteiro`).

#### `diagnostico_ao_vivo.py`, por pacote

- P3:
  - O contexto da busca (a irmã do ramo A2 de `recuperacao.contexto`) e o prompt congelado.
  - Uma inferência com as probabilidades por token e o registro com as 37 chaves oficiais.
  - A probabilidade lida no primeiro token do rótulo depois de `CAUSA_RAIZ:` e as conferências em código.
  - O selo pelos limiares de `resultados_alvo/fase4/limiares.json` (ficha 31).
  - Os gatilhos de intervenção: probabilidade, FONTE divergente, amostra fixa.
  - As quatro intervenções da especificação quando pedidas: remoção por marcador neutro, troca por verbete errado, sem documentação, repetição da base.
  - O nó de decisão `diagnostico` na trilha v2, com a justificativa e o contraste pelo molde.
  - A sondagem dos logprobs que abre toda noite medida.
- P5 (03/11/2026): `contexto_ao_vivo`, `montar_prompt` e `diagnosticar` aceitam `extras`, os verbetes recuperados pelo id do caso, postos depois dos k da busca e registrados no evento `candidatos` (`por_id`).

#### `biblioteca_fase4.py` (P5)

- Origem e estado de cada verbete (`status` controlado: não corrigido ou corrigido).
- Os casos ligados a um verbete pelas notas `[E1 · caso · …]` e pelo caso de origem.
- A recuperação por id: os verbetes do caso entram no contexto depois dos k da busca; `com_recuperacao_por_id` liga isso no executor congelado da Fase 3, para a sonda.
- As parcelas de contexto da calibração (regra dos 40%: nota em verbete presente em 40% ou mais dos contextos vai para revisão humana).
- Os 13 filtros em código da decisão 65 (`FILTROS`, cada um com o código que recusa), listados abaixo, e a regra da especificação da trilha: nenhum trecho literal de corpo HTTP entra numa proposta.
- `propor_p5`: a proposta como continuação literal do prompt do diagnóstico; o validador da Fase 3 primeiro, os filtros depois; a edição gravada só quando passa por tudo; os eventos `edicao_biblioteca` e o nó de decisão na trilha v2.
- O gatilho de correção (`evidencia_de_correcao` e `detectar_correcao`): marca corrigido só quando a reexecução passa e o fio e a árvore mudaram.
- `corrigir` acrescenta as seções "Solução sugerida" e "Solução aplicada" com data e avança só a linha do status, com `conferir_correcao` e `fechar_correcoes`.
- `avaliar_lote` (regra R5: b maior ou igual a c nos 36 inéditos, senão em espera).
- `regra_r4`: precisão, revocação e kappa da marca contra o conjunto desligado.
- Os comandos do Eric:
  - `--planilha`;
  - `--promover`: o lote aceito e revisado entra em `biblioteca_producao/`;
  - `--espera`: os aprendidos nunca recuperados vão para `aprendidos_em_espera/` (ficha 32).

Os 13 filtros da decisão 65:

1. Evidência obrigatória.
2. Atomicidade.
3. Abstenção válida.
4. Fonte confiável, contra o código das cobaias e o `openapi.json`.
5. Granularidade.
6. Peso por tipo, com orçamento por verbete.
7. Redundância por 3-gramas.
8. Proveniência.
9. Auditoria por etapa.
10. Conflito determinístico.
11. Métricas por rodada.
12. Revisão humana amostral, com planilha.
13. Regra dos 40%.

#### `linha_de_base_manual.py` (P6), os quatro comandos

- `ordem`: sorteia com semente fixa a ordem dos dez cenários de cada integrante e grava a planilha modelo.
- `armar`: restaura o banco, liga a falha do cenário da vez pelas mesmas funções da corrida e abre o mesmo Chromium para o integrante, com a ficha da falha da corrida 21, o roteiro e, no contrato, o contrato esperado e as 23 causas, sem mostrar o nome do cenário.
- `conferir`: roda o roteiro de localizador com o seletor do integrante e diz se ele chegou ao fim sem erro.
- `desarmar`: volta a CobaiaAPI ao modo normal.

#### `avaliacao_trilha.py` (P7)

- Os nós de decisão em código: `poda` (o diff do contrato contra o corpo do caso) e `recuperacao` (os verbetes que a busca entregou, emitido por um gancho de `diagnostico_ao_vivo.diagnosticar`).
- A sonda de pós-racionalização: um trecho que afirma a causa respondida, plantado só na memória num verbete entregue que a FONTE não citou.
- As mutações programadas, que alteram só a entrada do agente: `mutar_contrato`, a troca do verbete citado no resultado da busca e `quebra_do_seletor` (com uma mutação extra que troca o nome acessível do alvo).
- O nó que cada mutação tem de fazer divergir primeiro (`NO_PREVISTO`).
- O diff entre duas trilhas da mesma corrida (`diff_entre_trilhas`, sobre `trilha.diff_contra_referencia`).
- TPR x TNR (`tpr_tnr`) e os sinais de um caso.
- A amostra da sessão de revisão sorteada com semente fixa.

#### `executar_fase4.py` (+ `rodar_fase4.ps1`): modos

| Modo | Corrida | O que faz | O que grava | Opções |
|---|---|---|---|---|
| `reproducao` | 17 | Liga o modo de cada caso de avaliação na CobaiaAPI, roda o roteiro, poda, monta o caso ao vivo e decide se a tela reproduz o caso (regra R1). | `reproducao.jsonl`, `fora.json`, `condicoes_fase4.json`, a trilha v2 da corrida e o log com a linha FIM. | `--banco`: `avaliacao`, `ineditos_fase4` ou `todos` |
| `calibracao` | 16 | Calibra o selo de confiança: sondagem dos logprobs, ponte de versão pela regra R6 e a L1 curada nos 90 casos oficiais. | Os limiares do selo em `limiares.json` (pela regra R8). | `--k` |
| `tela` | 18 | Cada caso que reproduziu na corrida 17 montado na tela e diagnosticado por `diagnostico_ao_vivo.py`; o mesmo caso lido do fixture na mesma sessão. | `tela.jsonl` por caso, trilha v2 caso a caso, relatórios v2 por caso. | `--casos` |
| `cura` | 19 | Cura de seletor sem modelo, em cada célula (roteiro x modo de quebra x forma x repetição). | `cura.jsonl`, a trilha v2 e os relatórios por execução. | `--repeticoes`, `--formas`, `--roteiros`, `--modos` (`-Repeticoes`, `-Formas`, `-Roteiros`, `-Modos` no `.ps1`) |
| `biblioteca` | 20 | Os 54 casos de aprendizado diagnosticados com recuperação por id e a proposta de edição filtrada; o ciclo de correção sem modelo; a sonda de 28/09 repetida. | `biblioteca.jsonl`, `correcoes.jsonl`, `lote.json`, `revisao_do_lote.md`, `sonda.json`, a trilha v2 e os relatórios por caso. | `--base-ineditos` (`corrida12` ou `propria`), `--sem-sonda`, `--sem-correcao` |
| `cenarios` | 21 | Os dez cenários da ficha 36: o contrato pelo caminho do modo `tela` e o localizador pelo do modo `cura`. | `cenarios.jsonl` (com a ficha da falha de cada detecção em `motivo_deteccao`), a trilha v2 e os relatórios por execução. | `--repeticoes` |
| `avaliacao_trilha` | 22 | Os 36 casos de avaliação lidos do fixture, sem gabarito, e a mutação do seletor nos quatro roteiros de localizador. | `avaliacao.jsonl`, `seletor.jsonl`, os registros de 37 chaves por etapa, a trilha v2 e os relatórios por caso. | `--sem-seletor` (`-SemSeletor`) |
| `experimento_prompt` | 23 | Os 90 casos em texto, uma condição por item da decisão 55, com a biblioteca e o k da corrida 16. | `qwen2.5_7b/diagnosticos__<condição>.jsonl` |
| `ineditos` | 24 | Os 36 inéditos da ficha 27 em texto, pelo diagnóstico do agente, com a biblioteca de produção. | `qwen2.5_7b/diagnosticos__ineditos.jsonl`, `logprobs__ineditos.jsonl`, `ineditos.jsonl`, `trilha_ineditos.jsonl` |

O que não coube nas células da tabela:

- Observações gerais dos modos com modelo (P3 em diante):
  - Todo modo sobe as cobaias e restaura o banco antes.
  - A versão do Ollama é conferida a cada caso, e a corrida para se ela mudar.
  - `--casos` faz uma corrida parcial, que nunca grava derivado oficial.
- `reproducao` (corrida 17):
  - `--banco` escolhe os casos: `avaliacao` (os 72, padrão), `ineditos_fase4` (os 36 da ficha 27) ou `todos` (108).
  - Em 27/10/2026 rodou sobre os inéditos (`fase4_reproducao_ineditos`): os 25 com tela e modo reproduzem, 11 fora.
- `calibracao` (corrida 16):
  - Sondagem dos logprobs no Ollama instalado.
  - Ponte de versão pela regra R6 quando a versão não está em `resultados_alvo/fase4/pontes.json`.
  - A L1 curada nos 90 casos oficiais com cada `--k`, a regra R8 e os limiares do selo em `limiares.json`.
- `tela` (corrida 18): cada caso que reproduziu na corrida 17 é montado na tela como lá e diagnosticado por `diagnostico_ao_vivo.py`, e o mesmo caso é lido do fixture na mesma sessão do Ollama.
- `cura` (P4, corrida 19, sem modelo), o caminho de cada célula:
  - A corrida de referência sem quebra registra o alvo do passo.
  - O roteiro roda com a quebra armada até o passo falhar (detecção).
  - Os candidatos são verificados na página aberta.
  - O primeiro que passa é reexecutado do começo com a quebra armada de novo (fim do cronômetro do MTTR).
- `biblioteca` (P5, corrida 20, com modelo):
  - Os 54 casos de aprendizado (da tela os que reproduzem, do fixture os outros) são diagnosticados com recuperação por id e, na continuação do prompt, a proposta de edição é filtrada por `biblioteca_fase4.propor_p5` e gravada na `epoca-101`.
  - A regra R5 nos 36 inéditos contra a cópia curada: `--base-ineditos corrida12` (a corrida 12) ou `propria` (diagnosticada na mesma sessão).
  - O ciclo de correção sem modelo: os casos ligados a notas e com tela, metade com o modo desligado por `conjunto_de_correcao`, antes e depois, gatilho, `epoca-102`.
  - A sonda de 28/09 repetida com recuperação por id (`epoca-103`).
  - `--sem-sonda` e `--sem-correcao` servem para a fumaça.
- `cenarios` (P6, corrida 21, com modelo):
  - O contrato segue o caminho do modo `tela`: detecção pela conferência do roteiro ou, quando a tela não mostra, pelo fio (regra R1); o cronômetro para no diagnóstico conferido em código (ficha 35).
  - O localizador segue o do modo `cura`: o diagnóstico entre a detecção e a cura; o cronômetro para na reexecução validada, descontada a restauração do banco.
  - O banco é restaurado e conferido por hash no começo de cada repetição, e a versão do navegador é igual em todas.
  - Relançar retoma das execuções que faltam.
  - Depois da corrida 21: com um diagnóstico no meio, os candidatos da cura são verificados numa página refeita até o passo que falhou (`Cura._refazer_ate_o_passo`), porque a página da detecção pode mudar enquanto o modelo pensa.
- `avaliacao_trilha` (P7, corrida 22, com modelo):
  - Cada caso tem a inferência de base: os nós `poda` e `recuperacao` em código antes do `diagnostico`, as quatro intervenções pela amostra fixa, a sonda de pós-racionalização e as mutações verbete trocado e contrato alterado.
  - No fim, com as cobaias e o navegador, vem a mutação do seletor nos quatro roteiros de localizador: a execução dourada com a quebra do catálogo e a mutada com o nome do alvo trocado, as duas com o diagnóstico no meio.
  - `--sem-seletor` (`-SemSeletor`) pula o bloco do seletor na fumaça.
  - Relançar retoma dos casos e roteiros que faltam.

#### `avaliar_fase4.py`: leituras

| Opção | Corrida | O que lê | O que grava |
|---|---|---|---|
| `--reproducao` | 17 | A corrida por classe, nível e modo, com o custo por cenário e os tamanhos. | `resultados_alvo/fase4/reproducibilidade.{json,md}` (`--check`, `--colar`) |
| `--nome` e `--titulo` | outra corrida | A mesma leitura para outra corrida sem regravar a da 17. | `reproducibilidade_ineditos.{json,md}` para os 36 inéditos da ficha 27 |
| `--calibracao` | 16 | Acerto e acurácia balanceada por k, AUROC da probabilidade do rótulo e da conjunta com intervalo, revisão humana por parcela, curva risco-cobertura, regra R8, ponte e sondagem. | `calibracao.{json,md}` e `limiares.json` |
| `--tela` | 18 | Acerto na tela e no fixture, concordância, regra R2 com b e c (c até o limite, decisão 98; a soma ao lado), selos, gatilhos, divergências, tempos, tamanho da trilha, o prompt da tela contra o maior da calibração. | `tela.{json,md}` |
| `--pontes` | - | As pontes já rodadas. | `pontes.json`, regravado |
| `--pasta` | corrida parcial | Manda os derivados de uma corrida parcial para a pasta dela. | A pasta da corrida parcial |
| `--cura` | 19 | Regra R3: taxa de cura por modo, roteiro e forma, mesmo elemento contra outro elemento, MTTR da detecção à reexecução validada, o rendimento de cada estratégia, a comparação harness contra PHP. | `cura.{json,md}` |
| `--biblioteca` | 20 | Casos da tela e do fixture, acerto, o que cada filtro barrou, o lote, a regra R5 com b e c, a regra R4 com precisão e revocação, a sonda caso a caso contra 28/09, a recuperação dos aprendidos. | `biblioteca.{json,md}` (blocos `tb_f4_biblioteca_*`) |
| `--cenarios` | 21 | Task Success com intervalo de Wilson e MTTR médio com intervalo por reamostragem de semente fixa, no geral, por tipo e por cenário. | `cenarios.{json,md}` (blocos `tb_f4_cenarios_*`) |
| `--cenarios` com `--nome cenarios_v2` e `--titulo` | 21b | A leitura da corrida 21b. | `cenarios_v2` |
| `--tela` com `--nome tela_v3` e `--titulo`, e `--cenarios` com `--nome cenarios_v3` e `--titulo` | 18c e 21c | As leituras vigentes, com o prompt dentro do limite; a da tela conta também o acerto com e sem o verbete certo no contexto e o acerto por selo. | `tela_v3`, `cenarios_v3` |
| `--experimento_prompt` | 23 | Cada condição contra a corrida 16, caso a caso: acerto, acurácia balanceada, b e c, trocas de rótulo, a forma da resposta e o custo. | `experimento_prompt.{json,md}` (blocos `tb_f4_exp_*`) |
| `--ineditos` | 24 | Os 36 inéditos da ficha 27 lidos pelo modelo: acerto, por classe, nível e selo, com e sem o verbete certo no contexto, e a comparação com a corrida 18e. | `ineditos.{json,md}` (blocos `tb_f4_ineditos_*`) |
| `--trilha` | 22 | O acerto de cada caso contra o gabarito e TPR x TNR de cada sinal da trilha contra os erros reais. | `trilha.{json,md}` (blocos `tb_f4_trilha_*`), os relatórios da sessão de revisão em `relatorios_revisao_trilha/` e a planilha `revisao_trilha.md`, nunca regravada depois de preenchida |
| `--revisao` | 22 | A planilha `revisao_trilha.md` preenchida contra o acerto de cada caso em `trilha.json`: adesão apropriada, localização do erro, tempo até a decisão e utilidade. | `leitura_revisao_trilha.{json,md}` (blocos `tb_f4_revisao_*`) |

O que não coube nas células da tabela:

- `--cenarios` lê também: a ficha da falha de cada cenário, o tempo por execução, a estimativa da Fase 5, as execuções sem Task Success, a versão do navegador e o hash do banco.
- `--trilha` lê também:
  - as intervenções com o limite inferior;
  - a repetição da base;
  - a sonda de pós-racionalização;
  - as três mutações contra o nó previsto;
  - a divergência contada só por gatilho;
  - o controle da sonda;
  - as inferências de mesmo prompt;
  - a amostra de até 12 relatórios sorteada com semente fixa.
- `--revisao`:
  - Não sai enquanto houver relatório em branco.
  - Separa a resposta própria do revisor dos pareceres do Claude aprovados sem resposta própria e sem tempo medido (decisões 85 e 86), e por isso não cumpre a medida com revisor humano, que fica em aberto (decisão 95).
- Os blocos de cada prefixo no relatório da fase vêm de uma leitura só (`LEITURA_NO_RELATORIO`: `reproducibilidade`, `tela_v3` e `cenarios_v3`, as vigentes):
  - o `--colar` recusa as outras e a corrida que não bate com o `.md` gravado;
  - o `--check` delas confere só os próprios arquivos.

#### `testar_fase4.py`: testes por pacote

- Base (P0 a P2):
  - Ambiente, parser da árvore, fixtures e hashes das áreas só de leitura.
  - Trilha v2: leitor v1 sem perda, cabeçalho, nó de decisão, limites, diff de referência.
  - Molde e relatório v2, restauração do banco, poda, diff do contrato, interceptador, HAR, caso ao vivo, cenários, seleção dos casos da corrida 17 e a avaliação.
  - Os testes de integração com as cobaias são pulados com aviso quando as portas 8080 e 8000 não respondem.
  - `--gravar-hashes` grava a linha de base das áreas só de leitura.
- P3 (27/10/2026):
  - O diagnóstico ao vivo com Ollama de mentira: prompt igual ao do fixture, registro com as 37 chaves, probabilidade no token certo, limiares e selo, gatilhos e divergência, nó com as intervenções e a justificativa.
  - As partes puras dos modos novos (ponte R6, regra R8, casos que reproduzem).
  - As leituras `--calibracao` e `--tela` com `--check`.
  - O `rodar_fase4.ps1`: BOM, sem travessão, parse pelo PowerShell.
- P4 (01/11/2026):
  - Os candidatos na ordem fixa sobre a árvore congelada.
  - A verificação que recusa dois elementos, invisível e outro papel, e a escolha do primeiro que passa.
  - A trilha e o relatório com todos os candidatos.
  - O catálogo de quebras e a variante do PHP (`php -l`).
  - A quebra armada determinística (com o Playwright da venv).
  - O modo `cura` e a leitura `--cura` com `--check`.
- P5 (03/11/2026), 54 testes:
  - Origem, estado e recuperação por id.
  - Os 13 filtros com o exemplo mínimo recusado e o contraexemplo aceito.
  - A regra dos 40% nos contextos reais da calibração.
  - A correção que nunca remove bytes e só avança o estado.
  - O gatilho com os dois diffs.
  - O lote com c maior que b em espera.
  - O fluxo de proposta com Ollama de mentira e a trilha v2.
  - O modo `biblioteca` e a leitura `--biblioteca` com `--check`.
- P6 (04/11/2026):
  - O catálogo dos dez cenários, o cronômetro da detecção à validação e o Task Success só com o roteiro concluído sem erro.
  - O banco restaurado e conferido por hash em cada repetição, a versão do navegador igual em todas e a ficha da falha.
  - O modo `cenarios` e a leitura `--cenarios` com reamostragem e Wilson, e o ajudante da linha de base manual.
  - Depois da promoção de 04/11: a espera que guarda no `fechamento.json` o registro da promoção, com os testes do P5 lendo a cópia da L1 que a calibração leu e não a produção ao vivo.
  - Depois da corrida 21: a cura verificada numa página refeita depois do diagnóstico e a linha de ação do relatório nos casos com diagnóstico e cura (76 testes).
- P7 (04/11/2026):
  - TPR e TNR contra um gabarito sintético.
  - Cada mutação alterando só o nó previsto numa trilha de referência sintética.
  - A inferência de base com os nós `poda`, `recuperacao` e `diagnostico` e o limite inferior da intervenção contado pela leitura.
  - A sonda plantando só num verbete não citado.
  - As mutações ao vivo com o Ollama de mentira, as partes puras do modo `avaliacao_trilha`, a leitura `--trilha` com `--check` e a planilha da sessão de revisão.
  - Depois da corrida 22: a linha do `.ps1` que chama a leitura, executada para cada modo, o relatório de um caso de texto mostrando o caso, o controle da sonda e os números em três casas (97 testes).

## Ferramentas de apoio ao trabalho com IA (`ferramentas/`)

Scripts em Python padrão, sem dependência, que fazem localmente o que antes se
pedia a agentes (regra registrada no `CLAUDE.md`: primeiro a máquina, depois o
modelo):

<!-- ! Alteração de IA - Revisar: na tabela abaixo, a linha de `medir_tokens.py` ganhou a opção `--agentes` (29/09/2026).
     ! Motivo: a regra de permanência do servidor MCP comparou a mesma tarefa feita por subagentes com ferramentas diferentes, e o agregado por dia, modelo e tipo misturava todos os subagentes da sessão. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026, decisão 89) a linha de `poda.py` diz o que mudou em `diff_contrato`, e a de `testar_fase4.py` tem a contagem nova.
     ! Motivo: quem abre o repositório precisa saber que a poda mudou depois das corridas e onde está a medida disso. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026, sessão de revisão) entrou a linha de `sessao_revisao.py` na tabela abaixo, `--revisao` na linha de `avaliar_fase4.py` e a página na árvore do repositório.
     ! Motivo: quem abre o repositório precisa achar a página da sessão, o gerador e a leitura pelo nome. -->
<!-- ! Alteração de IA - Revisar: na tabela abaixo, a linha de `gerar_dashboard.py` foi reescrita e entrou a linha de `painel_topicos.py` (30/09/2026).
     ! Motivo: o Eric pediu a aba do comparativo qwen × Coder e que o painel fosse o compilador das análises, com uma aba por tópico; a linha antiga ainda descrevia o painel só com as abas de 28/09. -->
<!-- ! Alteração de IA - Revisar: na tabela abaixo entrou a linha de `sincronizar_orientador.py` (22/10/2026).
     ! Motivo: é o script que mantém a cópia no repositório do orientador igual ao commit deste (decisão 72); sem a linha, a tabela que lista as ferramentas deixaria de fora justamente a que o Eric roda a cada entrega. -->
<!-- ! Alteração de IA - Revisar: na tabela abaixo, as linhas de `integrar_pesquisa_pre_fase4.py` e `correcoes_pesquisa_pre_fase4.py` citam a numeração nova do levantamento da Pré-Fase 4 (23/10/2026: 14 tópicos; rejeitadas em §6.14.15 e mapas em §6.14.16); em 26/10/2026 a contagem das correções passou a 391, com as duas ondas da parte B.
     ! Motivo: a parte B ganhou três tópicos em 23/10/2026 e as duas subseções finais mudaram de número; a tabela citava §6.14.12 e §6.14.13. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026) células da tabela abaixo acima de cerca de 300 caracteres foram encurtadas e o resto foi para a lista "O que não coube nas células" logo depois da tabela.
     ! Motivo: o Eric reclamou (05/11/2026) da leitura; a tabela segue com as colunas `Script | O que faz` e como primeira tabela da seção, porque o painel do projeto (`ferramentas/painel_topicos.py`) lê essa tabela por script. Nenhum fato foi tirado. -->
| Script | O que faz |
|---|---|
| `gerar_dashboard.py` | Painel do projeto (`Documentacao/dashboard/painel-do-projeto.html`, HTML único), o compilador das análises: lê os JSON de resultado e as figuras 01–18, monta os gráficos e recebe as abas por tópico de `painel_topicos.py`; `--check` regera e compara. |
| `medir_disco.py` | Pré-Fase 4: mede a vazão de leitura do disco no desenho do `iobench` do colibri (blocos de 19 MB, 64 leituras, 8 threads), passando pelo cache do sistema e por fora dele, e grava `resultados_alvo/pre_fase4/disco.json` com a descrição da máquina. |
| `integrar_pesquisa_documentacao.py` | Rodada 4 do levantamento (29/09/2026, qualidade da documentação autogerida): `--montar` junta pesquisa + verificação + síntese em `r4-final.json`; `--check`. |
| `integrar_pesquisa_pre_fase4.py` (+ `testar_integrar_pesquisa_pre_fase4.py`) | Rodada 5 do levantamento (01/10/2026, Pré-Fase 4), em duas partes, a B em duas ondas: integra as duas partes ao Memorial, com numeração fixa; `--check`. |
| `correcoes_pesquisa_pre_fase4.py` | As 391 correções declaradas das sínteses e dos mapas da rodada 5 (trecho antigo, novo e motivo), que o integrador aplica e lista no §6.14.15 do levantamento. |
| `gerar_pdf_abnt.py` | PDF (versão beta) do projeto de pesquisa a partir do Markdown, sem as marcações de IA (retiradas só da cópia), com folha de estilo ABNT e impressão pelo Microsoft Edge em modo sem janela; grava `Documentacao/Projeto de Pesquisa - ABNT 15287_2025 - V4-beta.pdf`. |
| `painel_textos.py` (+ `testar_painel_textos.py`) | Leitura das fichas de `pendencias.md` e das tabelas de `roadmap.md` para o painel, e conversão do resto dos dois documentos em HTML; o teste confere o formato dos arquivos reais. |
| `painel_topicos.py` (+ `testar_painel_topicos.py`) | Abas por tópico do painel (30/09/2026). Cada aba: pergunta, resposta em uma frase, números-chave, um ou dois gráficos, leitura curta e tabelas recolhidas; nenhum número digitado à mão. |
| `painel_leituras.py` | Regras de leitura do painel, aplicadas à página montada: um "Como ler" por gráfico e por figura, a resposta direta de cada aba, e as tabelas de dados e figuras repetidas em "Mais informações". O teste acusa gráfico sem explicação. |
| `sessao_revisao.py` (+ `testar_sessao_revisao.py`) | Sessão de revisão dos relatórios da trilha (Fase 4, P7): gera `Documentacao/dashboard/sessao-revisao-trilha.html` só da planilha `revisao_trilha.md` e dos relatórios dela, publicada como [página da sessão](https://claude.ai/artifact/7UrQ4gaqHj9qnvo22tfDgS); `--gravar` passa as respostas do banco da página para a planilha, conferindo os valores. |
| `painel_atlas.py` | Aba Atlas do painel (01/10/2026): o mapa dos verbetes pelas seis classes de defeito, desenhado em SVG no próprio Python; lê `resultados_alvo/pre_fase4/atlas.json`. |
| `painel_explorador.py` | Explorador de casos da aba "Raciocínio aberto" do painel (01/10/2026): de cada trilha versionada, o recorte por caso das três camadas (o que o programa fez, o que o modelo declarou, o que o código conferiu) e, à parte e recolhida, a avaliação contra o gabarito. |
| `medir_tokens.py` | Soma o consumo de tokens do Claude Code a partir dos transcritos locais, por dia, modelo e tipo de agente (linha de base e medição "depois" das medidas de economia). `--agentes rótulo=id,...` soma só os subagentes pedidos (usado na regra de permanência do servidor MCP, 29/09/2026). |
| `resumir_saida.py` / `gancho_pre_bash.py` | Hook `PreToolUse` do Claude Code (`.claude/settings.json`) que encurta a saída de comandos longos (testes, baterias, `git diff`) antes de ela entrar no contexto. |
| `conferir_docs.py` | Confere a documentação antes de entregar: links relativos, tag `! Alteração de IA - Revisar` com `! Motivo` em todo arquivo tocado, frases obsoletas, hipóteses H1–H6 idênticas, BOM e ausência de travessão nos `.ps1`. |
| `sincronizar_orientador.py` (+ `testar_sincronizar_orientador.py`) | Cópia do TCC no repositório da disciplina (decisão 72): replica os arquivos rastreados do commit HEAD deste repositório em `../squad-24-projeto/projeto/` (clone do repositório do orientador); ensaio por padrão, `--aplicar` grava, `--check` devolve 1 fora de sincronia. |
| `gerar_tcc_docx.py` (+ `testar_gerar_tcc_docx.py`) | Documento do TCC em Word a partir de `Documentacao/TCC - ABNT 14724 - V1.md`, no molde do orientador: troca só o corpo do `.docx`, mantém estilos e cabeçalho, e monta sumário e listas como campos do Word; `--copiar-para` grava a cópia em `TCC/` do clone. |
| `replicar_commits_orientador.py` (+ `testar_replicar_commits_orientador.py`) | Cópia commit a commit no clone do repositório da disciplina (decisão 84): lista os commits do principal que o clone ainda não tem e, com `--aplicar`, copia cada um e o commita no clone com a mesma mensagem e o hash de origem; o push é do Eric. |
| `extrair_pesquisa.py`, `render_levantamento.py`, `integrar_pesquisa.py`, `integrar_pesquisa_llms.py` | Fecham as pesquisas bibliográficas por script: extraem os artefatos verificados, geram as subseções no formato do Memorial (com `--check`) e integram texto, referências (com dedup), mapa de decisões (Fase 3) e mapa adotado/adiado/descartado (LLMs locais, §6.12 e §7.9). |

O que não coube nas células da tabela:

- `gerar_dashboard.py`:
  - Navegação em cinco grupos: Projeto, Modelos, Biblioteca, Fases anteriores, Pesquisa e método.
  - Abas Início (estado por fase, o que depende do Eric, mapa do painel), Pendências (um cartão por ficha de `pendencias.md`, com filtro), Roadmap (fases e corridas de `roadmap.md`, com o comando pronto) e as abas dos testes.
  - Lê `resumo_fase3.json`, `comparacao_fases.json`, `decisao_modelo.json`, os resumos das Fases 2-A/2-B, os 29 blocos de `tabelas_relatorio.md` e as figuras 01–18.
  - Monta gráficos (Chart.js, paleta validada da regra de gráficos, com tema escuro).
- `integrar_pesquisa_documentacao.py`:
  - `--montar` lê `.superpowers/sdd/fase3b-e-fechamento/pesquisa/r4/`.
  - A integração grava `levantamento-2026-09-29-documentacao-autogerida.md` (§6.13), o bloco de referências e a linha no índice do Memorial.
- `integrar_pesquisa_pre_fase4.py`:
  - Numeração fixa: §6.14.1 a §6.14.14 (os três últimos acrescentados em 23/10/2026), §6.14.15 rejeitadas e §6.14.16 mapas, um por Workflow.
  - Regrava o bloco de referências sem repetir fonte (pela chave das outras rodadas e pelo endereço) e a linha do índice.
  - Troca pelo número medido a expressão imprecisa do contexto dado aos agentes e declara a troca.
- `correcoes_pesquisa_pre_fase4.py`:
  - As 391 correções vêm de 156 da parte A em 05/10/2026 e 120 da onda 1 mais 115 da onda 2 da parte B em 23/10/2026.
  - Cada trecho tem de aparecer uma vez só no texto do agente, senão a integração para.
- `painel_textos.py`:
  - As fichas seguem `### N. Título` + campos Estado / Quem decide / O que é / Por que importa / Opções / Recomendação / Decisão.
  - Das tabelas de `roadmap.md` lê o estado por fase e as corridas com a coluna Estado.
- `painel_topicos.py`: as abas são qwen × Coder (`comparativo_qwen_coder.json`), Fase 3-B (`fase3b_ineditos/resumo_fase3.json`, ponte, sonda, corridas), curadoria da L1 (`curadoria.json` + planilha), recuperador (`experimento_recuperador.json`), ablação base × instruct (`ablacao_base_instruct/resumo_metricas.json`), pesquisa (títulos dos levantamentos e o mapa de filtros da rodada 4) e ferramental (esta tabela e a medição do servidor MCP).
- `sessao_revisao.py`: mostra um relatório por vez, com `relatorio-N` no lugar do nome do caso, e tem o tempo até a decisão medido com o relatório à vista.
- `painel_atlas.py`: o mapa é movido por um script simples na página (biblioteca, quem leu, caso); a aba traz também o detalhe de cada verbete, a rota de cada caso, o acerto por causa com as trocas e um passeio guiado.
- `sincronizar_orientador.py`:
  - Compara cada arquivo pelo hash do git, apaga o que saiu daqui e deixa de fora a `.venv` da CobaiaAPI e a `.claude/`.
  - Escreve o commit e a contagem no README do clone.
  - O commit e o push no clone são do Eric.

## Memória do Claude Code entre máquinas

<!-- ! Alteração de IA - Revisar: seção nova apontando para a pasta claude-memoria/.
     ! Motivo (nota de 21/09/2026: desde então `.claude/` é versionada, menos `settings.local.json`; a memória em `~/.claude/projects/` continua fora): a memória do Claude e o .claude/CLAUDE.md não viajavam pelo git (ficavam fora do
     repositório ou no .gitignore); quem for usar o Claude na máquina-alvo precisa saber
     que existe um importador. -->
O que o Claude Code sabe deste projeto (decisões, regra de comentário, regra de
commit) fica fora do repositório. A pasta [`claude-memoria/`](claude-memoria/)
carrega tudo pelo git: na máquina de destino, rode
`powershell -ExecutionPolicy Bypass -File claude-memoria\importar.ps1` uma vez e
abra o Claude Code na pasta do repositório. Detalhes no README de lá.

<!-- ! Alteração de IA - Revisar: nota sobre a correção do cálculo do `<slug>` usado por
     `importar.ps1`/`exportar.ps1` (a pasta de memória do Claude Code para este projeto).
     ! Motivo: até 10/09/2026 a regex do slug só trocava `:` e `\` por `-`, deixando o `.` de
     "Eric.Derre" intacto e apontando para uma pasta de memória que o Claude Code nunca usa
     (`c--Users-Eric.Derre-Documents-TCC`); o slug real desta máquina é
     `c--Users-Eric-Derre-Documents-TCC` (todo caractere fora de letra/número vira `-`).
     Corrigido em 11/09/2026 nos dois scripts; ver `claude-memoria/README.md`. -->
Quem já rodou `importar.ps1`/`exportar.ps1` antes de 11/09/2026 deve rodar de
novo depois de atualizar: o slug calculado mudou (era
`c--Users-Eric.Derre-Documents-TCC`, agora é `c--Users-Eric-Derre-Documents-TCC`).

## Testes e lint

```powershell
cd Programacao\CobaiaAPI
.venv\Scripts\python.exe -m pytest -v
.venv\Scripts\python.exe -m ruff check .
```
(No Linux/macOS: `.venv/bin/python -m pytest -v`.)

<!-- ! Alteração de IA - Revisar: o bloco de comandos abaixo ganhou `testar_sincronizar_orientador.py` (22/10/2026).
     ! Motivo: é o teste do script que grava a cópia no repositório do orientador (decisão 72); a lista de testes que rodam sem modelo precisa cobrir tudo o que o Eric roda antes de entregar. -->
<!-- ! Alteração de IA - Revisar: o bloco ganhou `testar_fase4.py` e `testar_instalador.py` (26/10/2026).
     ! Motivo: são os testes da Fase 4 e dos scripts da raiz (instalador sem administrador e run.py), escritos antes do código; a lista precisa cobrir tudo o que roda sem modelo. -->
Experimentos, painel e documentação, sem chamar modelo nenhum:

```powershell
cd Programacao\AgenteCore\experimentos
python testar_fase3.py
python testar_fase3b.py
python testar_pre_fase4.py
python testar_fase4.py
python testar_figuras_documentos.py
cd ..\..\..
python testar_instalador.py
python ferramentas/testar_painel_textos.py
python ferramentas/testar_painel_topicos.py
python ferramentas/testar_integrar_pesquisa_pre_fase4.py
python ferramentas/testar_sincronizar_orientador.py
python ferramentas/testar_sessao_revisao.py
python ferramentas/testar_gerar_tcc_docx.py
python ferramentas/gerar_dashboard.py --check
python ferramentas/conferir_docs.py
```

Os testes da CobaiaAPI rodam contra o **banco real** (não há banco de testes isolado,
é um ambiente cobaia, não produção), então rode `install.ps1`/`install.sh`
pelo menos uma vez antes.

## O que é versionado e por quê

O repositório é deliberadamente "hit and run": versionamos **muito mais que
o normal** para que quem clonar precise do mínimo de passos. Fica de fora só
o que não funcionaria na máquina de outra pessoa, ou o que se regenera
sozinho, versionar essas coisas atrapalharia o "hit and run" em vez de
ajudar.

<!-- ! Alteração de IA - Revisar: em 12/09/2026 a tabela ganhou as duas linhas de `.superpowers/`
     e de `resultados_alvo/fase3_piloto/`, que já estavam no `.gitignore` (linhas 19 e 25).
     ! Motivo: as duas regras entraram no `.gitignore` em 11/09/2026 com comentário lá, mas esta
     tabela, que é onde o README explica o que fica fora do git e por quê, não as citava, e
     quem procurasse aqui o motivo de o piloto não estar versionado não achava. -->
<!-- ! Alteração de IA - Revisar: na tabela abaixo, a linha de `.mcp.json`/`.cbmignore` passou a "Não, removidos" (29/09/2026).
     ! Motivo: a linha dizia que os dois ficavam se a regra de permanência fosse cumprida; ela foi medida e o servidor saiu. -->
| Item | Versionado? | Por quê |
|---|---|---|
| `Cobaia.exe` (8.6 MB) | **Sim** | É o próprio entregável "hit and run" do Windows: clonou, deu duplo clique, rodou, sem precisar nem de Python instalado pra compilar. Elimina o risco de "o build falhou 5 min antes da banca". Precisa ser recompilado (`build_exe.ps1`) quando `Cobaia.py`/`install.py`/`run.py`/`_env_common.py` mudarem. |
| `Cobaia.spec` | **Sim** | Receita de recompilação (arquivo texto pequeno). |
| `Programacao/CobaiaFront/` inteiro (16 MB, sendo 13 MB de imagens) | **Sim** | Imagens, CSS/JS do Bootstrap e PHPMailer são carregados localmente pelo site, sem eles o CobaiaFront não renderiza. Não há passo de build/download que os recupere. |
| `banco/*.sql` | **Sim** | Schema + seed. É o que faz o site funcionar de verdade. |
| `.env.example` | **Sim** | Template de configuração (o `.env` real fica de fora). |
| `Programacao/CobaiaAPI/.venv/` (67 MB) | **Não** | Verificado: o `pyvenv.cfg` grava caminhos absolutos desta máquina (`home = C:\Python314`) e a pasta tem 16 `.exe` + 14 `.pyd` (binários Windows) e nenhum `bin/`. É **inutilizável no Linux** e quebra em outra máquina Windows. São 67 MB que enganam quem clona, e o instalador recria a venv correta pra cada SO em ~30s. |
| `__pycache__/`, `*.pyc` | **Não** | Cache de bytecode: derivado, regenerado sozinho, muda a cada execução e polui o diff. |
| `.env` | **Não** | Configuração local. Use o `.env.example` como base. |
| `build/`, `dist/` | **Não** | Artefatos transitórios do PyInstaller (o `.exe` final é gravado na raiz, esses ficam no `%TEMP%`). |
| `node_modules/`, browsers do Playwright | **Não** | Usados pelo AgenteCore desde a Fase 4, centenas de MB, específicos de cada SO, baixados por instalador. |
| `.claude/` (menos `settings.local.json`) | **Sim** | Configuração do projeto para o Claude Code: `CLAUDE.md`, `settings.json` (hook que resume saídas longas, permissões de leitura, plugin de estilo desligado), `rules/` por tipo de arquivo e `skills/` copiadas, precisa chegar à outra máquina pelo git (decisão do Eric, 21/09/2026). Só `settings.local.json` (permissões concedidas nesta máquina) fica de fora. |
| `.superpowers/` | **Não** | Rascunho de sessão do Claude Code (livro-razão, briefs e relatórios de tarefa da Fase 3); mesma natureza de `.claude/`. |
| `.mcp.json`, `.cbmignore` | **Não, removidos em 29/09/2026** | Registro do servidor `codebase-memory-mcp` em escopo de projeto e as exclusões do índice (22/09/2026, decisão 49). A regra de permanência foi medida em 29/09 com três tarefas fixas (grep × servidor, duas vezes cada): o servidor gastou 8,6% a mais de tokens no total e 4,3% a menos nos novos, sem chegar aos 20% de corte, e saiu junto com o pacote npm (decisão 62; ferramental §7.2). |
| `Documentacao/notebooks/` | **Não** | Notebooks e dados de apoio do livro-texto (Faceli et al., 3. ed., 2025), baixados pelo QR code do livro: material dos autores e da editora, sem licença declarada, 330 MB em 53 mil arquivos que nenhum script do projeto usa. Quem tem o livro baixa a pasta por conta própria; ela é citada no fichamento (decisão 68). |
| `resultados_alvo/**/*.log` | **Sim** | Registro corrido de cada bateria (início e fim de cada modelo, relances, falhas, versão do Ollama); exceção ao `*.log` genérico desde 29/09/2026 (decisão 63). |
| `Documentacao/dashboard/painel-do-projeto.html` | **Sim** | Gerado por `ferramentas/gerar_dashboard.py` a partir dos registros; versionado para o painel abrir em qualquer clone, e `--check` acusa qualquer edição manual. |
| `Programacao/AgenteCore/experimentos/resultados_alvo/fase3_piloto/` | **Não** | Piloto da Fase 3 (1 modelo, 10 casos, 1 época): existe para conferir o encanamento e calibrar o tempo antes das ~60 h; seus JSONL e snapshots confundiriam a leitura de `resultados_alvo/fase3/`, que é o que vale. |

O "hit and run" continua íntegro sem a venv, porque os dois caminhos a
recriam automaticamente:
- **Windows:** duplo clique em `Cobaia.exe`: instala (inclui criar a venv), sobe tudo e abre o navegador.
- **Linux/macOS:** `./install.sh && ./run.sh` faz a mesma coisa.

## Decisões técnicas e problemas resolvidos

Documentado aqui porque cada um foi descoberto testando ao vivo, não
teorizado, importante pra quem for mexer no ambiente depois entender o
porquê:

- **XAMPP foi descartado.** O objetivo era um instalador silencioso e
  roteirizável em 3 SOs; o instalador GUI do XAMPP não se presta bem a
  isso. PHP e MariaDB nativos, instalados via linha de comando
  (`winget`/`apt`/`brew`), resolvem sem essa fricção.
- **MariaDB no Windows não registra serviço.** Testado nesta máquina sem
  privilégios de administrador: o `winget install MariaDB.Server` instala
  os binários e já inicializa o data dir (root sem senha), mas não registra
  um Windows Service (isso exigiria elevação). Por isso o MariaDB é sempre
  gerenciado como subprocesso direto no Windows, igual ao PHP e ao uvicorn; 
  ver `_env_common.py::ensure_mariadb_running`.
- **`extension_dir` do PHP vem hardcoded errado.** O build Windows do PHP
  aponta por padrão pra `C:\php\ext`, que não bate com o caminho real de
  instalação do winget. `_env_common.py::php_extension_flags` calcula o
  caminho certo dinamicamente a partir do binário encontrado.
- **`mbstring` é obrigatória, não opcional.** `mb_strimwidth()` é usada em
  5 páginas de produtos (incluindo a home), sem a extensão carregada, é
  **erro fatal**, não warning. Só foi percebido testando a home page a
  fundo (um teste superficial só com `grep` não pegou, porque o conteúdo
  antes do ponto de falha ainda aparecia no HTML).
- **`output_buffering` precisa estar ligado.** `cliente/index.php` ecoa
  HTML antes de `reserva_cli.php` incluir `admin/acesso_com.php`, que só
  então chama `session_start()`, um bug de ordenação pré-existente no
  código original. Um XAMPP/Apache real normalmente mascara isso porque
  `output_buffering` costuma vir ligado por padrão. Sem isso, a sessão de
  login não é retomada corretamente e a página trunca logo após a
  saudação. Resolvido via flag de configuração do PHP (não altera nenhum
  arquivo `.php`).
- **`vw_tbpedidos` usa `LEFT JOIN`, não `JOIN`.** Na primeira versão da
  view (criada do zero, o dump original não tinha essa tabela/view), um
  `JOIN` normal a partir de `tbpedido_reserva` fazia um cliente **sem
  nenhuma reserva ainda** sumir inteiramente da view, quebrando a
  saudação com "Trying to access array offset on value of type null".
  Corrigido fazendo `LEFT JOIN` a partir de `tbusuarios`, e usando
  `u.id_usuario` (não `pr.id_clientes`) como `id_clientes`, assim o campo
  continua correto mesmo sem nenhuma reserva prévia.

## Problemas conhecidos (deixados de propósito)

Decisão do grupo: manter `CobaiaFront` como veio, sem correções de código,
exceto o único caso de segurança justificado abaixo.

| Item | Situação |
|---|---|
| Link "Saiba Mais..." nas listagens de produtos | Aspas do `href` no lugar errado (bug do código original), sempre abre `id_produto=` vazio. Não corrigido. |
| Senha de usuário: texto puro no insert, MD5 no update, sem hash no login | Inconsistência do código original. Não corrigido, o `seed.sql` sempre insere em texto puro, então não afeta o login das contas de teste. |
| Credencial SMTP real hardcoded em `rodape_contato_envia.php` | Decisão explícita do grupo: como é ambiente de teste sem dados reais, foi mantida como está. |

## Segurança

Este é um **ambiente de teste** (cobaia), não um sistema em produção:
credenciais fracas/hardcoded, SQL injection nas queries do CobaiaFront, e
CORS liberado (`*`) na CobaiaAPI são conhecidos e intencionalmente não
corrigidos, fazem parte do escopo de cenários que o agente de QA deve ser
capaz de lidar. Não reutilize esses padrões fora deste projeto. A política de
segurança do repositório, com o canal privado para relatar problemas reais nos
instaladores e nas ferramentas, está em [SECURITY.md](SECURITY.md).

## Troubleshooting

- **`.\install.ps1 : ... a execução de scripts foi desabilitada neste
  sistema` (PSSecurityException):** é a Execution Policy padrão do Windows,
  que bloqueia scripts `.ps1` não assinados, não é um bug do projeto. Use
  `install.cmd`/`run.cmd` em vez de chamar os `.ps1` diretamente (eles
  chamam o PowerShell com `-ExecutionPolicy Bypass`, que vale só pra aquela
  execução, sem mudar nenhuma configuração persistente do sistema). Se
  preferir rodar o `.ps1` direto mesmo assim:
  `powershell -ExecutionPolicy Bypass -File .\install.ps1`.
- **`winget install` parece ter funcionado mas o comando ainda não é
  encontrado:** normal, o PATH só atualiza numa sessão de terminal nova.
  `install.py`/`run.py` já lidam com isso procurando o executável
  diretamente nos caminhos de instalação conhecidos, sem depender do PATH.
- **Porta 8080 ou 8000 já em uso:** edite `FRONT_PORT`/`API_PORT` no topo
  de `run.py`.
- **Erro de conexão com o banco (`Access denied for user 'root'`):** o
  `connect.php` do CobaiaFront espera `root` sem senha. Rode o instalador
  de novo, ele tenta corrigir isso automaticamente; se persistir, ajuste
  manualmente (`ALTER USER 'root'@'localhost' IDENTIFIED BY '';`).
- **`ModuleNotFoundError` ao rodar a CobaiaAPI:** o venv não foi
  criado/atualizado. Rode `install.ps1`/`install.sh` de novo.
