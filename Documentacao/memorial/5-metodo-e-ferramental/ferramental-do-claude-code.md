<!-- ! Alteração de IA - Revisar: arquivo novo (21/09/2026) com o levantamento do ferramental do Claude Code usado no projeto: o que foi avaliado, o que foi adotado, o que foi descartado e por quê, as regras de economia de tokens e a medição de consumo antes das mudanças.
     ! Motivo: o Eric pediu (21/09/2026) que os dois repositórios indicados fossem instalados e que outros complementos e práticas de economia de tokens fossem pesquisados, e que tudo — inclusive o descartado — ficasse documentado como insumo do documento final do TCC. Os números de estrelas e de issues vieram da API do GitHub em 21/09/2026; os de consumo, de `ferramentas/medir_tokens.py` sobre os transcritos locais. O que ainda depende da sessão 6 (instalações e medição "depois") está marcado. -->

# Ferramental do agente de apoio (Claude Code) — avaliação, adoção e economia de tokens

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Este arquivo trata do **Claude Code**, o agente que ajuda a desenvolver e documentar o TCC; o ferramental das **LLMs locais** do próprio agente de QA está em [ferramental-das-llms-locais.md](ferramental-das-llms-locais.md).

## 7.1 A máquina e o que ela limita

| Item | Valor (21/09/2026) |
|---|---|
| CPU | Intel Core i5-1235U, 10 núcleos (2 P + 8 E), 12 threads |
| RAM | 15,7 GiB |
| GPU | Intel UHD Graphics integrada (memória compartilhada); **sem NVIDIA/CUDA** (`nvidia-smi` inexistente); sessão por RDP |
| Claude Code | 2.1.245 (a atualização pelo `claude update` falhou sem acesso ao npm; a estatística de cache do `/usage` existe a partir da 2.1.251) |
| Node / npm / Python / uv / Docker | 24.19.0 / 11.17.0 / 3.14.7 / presente / ausente |

Consequência para a regra do Eric ("tudo que a máquina resolve, roda na máquina"): **processamento local aqui é CPU** — scripts Python, `grep`, índices em SQLite. Não há GPU utilizável para embeddings nem para um modelo auxiliar, e um modelo local auxiliar competiria por CPU e RAM com as baterias do TCC, contaminando as medições de tempo; por isso ele não entra como subagente do Claude.

## 7.2 Os dois repositórios indicados pelo Eric

### `DeusData/codebase-memory-mcp`

| Campo | Valor |
|---|---|
| O que é | Servidor MCP em C: indexa o repositório com tree-sitter (funções, classes, chamadas, rotas) num grafo em SQLite, com embeddings embutidos no binário; ~15 ferramentas (`search_graph`, `trace_path`, `get_architecture`, …) |
| Licença / versão / atividade | MIT / v0.11.0 (pré-1.0) / 43.946 estrelas, 597 issues abertas, último push em 21/09/2026 |
| Instalação oficial | `install.ps1` que autoconfigura os clientes detectados; também npm, Winget, Chocolatey, Scoop |
| Riscos encontrados (issues abertas) | "Windows 11 - Installation CBM Deletes all user path variables except itself" (04/09/2026); "Windows v0.10.8 installer fails while configuring multiple agents"; "Windows Defender report: Win32/Peardis.C" (07/2026); daemon indexando `C:\Windows\system32` por diretório de trabalho errado |
| Ganho esperado neste repositório | Baixo: o código autoral é pequeno (concentrado em `Programacao/AgenteCore/experimentos/`), os 731 arquivos `.md` de prosa não se beneficiam de análise sintática e a venv/PyInstaller versionados inflariam o índice |

**Decisão do Eric (21/09/2026): instalar com salvaguardas**, na sessão 6 e no início da sessão (ligar um servidor MCP no meio invalida o cache de prefixo): backup do PATH (`reg export HKCU\Environment`) e dos arquivos de configuração; binário via `npm install -g`, nunca o `install.ps1`; conferência imediata do PATH e do Defender (alerta = parar, desinstalar, registrar — máquina corporativa); MCP em escopo de projeto (`.mcp.json`) configurado à mão; indexação primeiro de uma cópia descartável, excluindo venvs, `resultados*`, `base_conhecimento` e `.superpowers`; medição em três tarefas fixas antes (Grep/Read) e depois (MCP). **Regra de permanência**: fica só se cortar ao menos 20% dos tokens dessas tarefas sem incidente; senão sai e o resultado fica registrado aqui.

<!-- ! Alteração de IA - Revisar: registro da instalação com salvaguardas feita em 22/09/2026 (P4), com o resultado de cada salvaguarda e o teste na cópia descartável.
     ! Motivo: o Eric decidiu instalar com salvaguardas; cada passo precisa ficar registrado com o que aconteceu (PATH, Defender, índice), e a regra de permanência só pode ser aplicada numa sessão em que o servidor esteja ativo — o que fica dito aqui para a próxima. -->
**Instalação feita em 22/09/2026 (P4), passo a passo:**

| Salvaguarda | O que aconteceu |
|---|---|
| Backups antes | `reg export HKCU\Environment` (5 KB), cópia de `~/.claude.json`, `~/.claude/settings.json` e `.claude/settings.json` em `.superpowers/sdd/fase3b-e-fechamento/backups-p4/` (fora do git) |
| Binário via npm, nunca o `install.ps1` | `npm install -g codebase-memory-mcp@latest` instalou a 0.11.0; o `postinstall` (download do binário, 301 MB, `bin/codebase-memory-mcp.exe`) só rodou com `--allow-scripts=codebase-memory-mcp`, porque o npm desta máquina bloqueia scripts de instalação por padrão |
| PATH do usuário | Lido antes e depois (`HKCU:\Environment\Path`): **inalterado** — o npm só criou os atalhos em `%AppData%\npm` |
| Windows Defender | Proteção em tempo real ligada; nenhuma detecção na última hora (`Get-MpThreatDetection` vazio) depois do download do binário |
| Cópia descartável primeiro | 83 arquivos (`experimentos/*.py`, `CobaiaAPI/app`, `tests`, `CobaiaFront/*.php` sem PHPMailer) copiados para o scratchpad da sessão e indexados com `CBM_CACHE_DIR` também no scratchpad: 7,7 s, 994 nós e 4.568 arestas, cache de 12 MB; **25 dos ~40 `.php` legados saíram como "parse unusable"** (o analisador não lê o PHP misturado com HTML do CobaiaFront) e 1 parcial |
| As três tarefas fixas, pela CLI do servidor (antes = `grep`) | (1) usos de `TETO_TOKENS_CONTEXTO`: `search_code --mode compact` devolve 5 símbolos com as 10 linhas, ~700 bytes contra ~900 do grep; (2) rastro `validar_proposta → aplicar_edicao`: `trace_path` lista 45 chamadas de saída em 2 saltos (o grep dá as 14 linhas de definição e uso em ~1,2 KB), mas o caminho passa por `executar_fase3.py`, que o grafo mostra como chamador, não como caminho; (3) quem lê `fechamento.json`: `search_graph` devolve **50 funções vagamente relacionadas** (busca semântica), contra 14 linhas exatas do grep — pior |
| Registro em escopo de projeto | `.mcp.json` na raiz (servidor `codebase-memory`, comando `codebase-memory-mcp`) e `.cbmignore` (venvs, `resultados*`, `base_conhecimento`, `.superpowers`, PHPMailer, imagens, `Documentacao/`, `*.jsonl`); entram em vigor na próxima abertura do Claude Code, que pede confirmação do servidor de projeto. O Eric decide se commita os dois arquivos |

*(Estado: instalado e registrado; **regra de permanência a aplicar na primeira sessão com o servidor ativo** — repetir as três tarefas pelas ferramentas MCP e comparar os tokens com `medir_tokens.py`. Leitura preliminar pela CLI: ganho pequeno em busca de símbolo, nenhum em busca textual, e o PHP legado fica fora do grafo — a tendência é sair, salvo se a Fase 4 usar `trace_path` com frequência.)*

### `mattpocock/skills`

| Campo | Valor |
|---|---|
| O que é | 26 skills em Markdown (SKILL.md com frontmatter) para agentes de código; MIT; 266.812 estrelas; último push em 18/09/2026 |
| Instalação | Como plugin (`/plugin marketplace add mattpocock/skills` + `/plugin install mattpocock-skills@mattpocock`) ou cópia dos arquivos para `.claude/skills/` |
| Custo | A descrição de cada skill entra no contexto a cada turno: 26 descrições somadas às ~18 já ativas dobrariam esse custo fixo |
| Sobreposição | Sem colisão de nomes com o plugin `superpowers` (skills de plugin têm namespace), mas cinco pares se sobrepõem em conteúdo: `tdd`, `code-review`, `diagnosing-bugs`, `grill-me`, `to-tickets` |

**Decisão do Eric (21/09/2026): copiar cinco skills para o projeto** (`.claude/skills/`, commit `c55ee460` de 18/09/2026, com tag de atribuição MIT após o frontmatter): `research`, `domain-modeling`, `handoff`, `writing-for-agents`, `grill-with-docs`. Avaliação das 26:

| Skill | Decisão | Motivo |
|---|---|---|
| `research` | **adotada** | investigação contra fontes primárias com registro em Markdown — é o fluxo da revisão bibliográfica do TCC |
| `domain-modeling` | **adotada** | terminologia consistente (CONTEXT.md, ADRs) — o TCC precisa de vocabulário estável entre Memorial, código e ABNT |
| `handoff` | **adotada** | compacta a conversa em documento de passagem — é o que `claude-memoria/contexto/` faz à mão; economia direta de tokens |
| `writing-for-agents` | **adotada** | disciplina para documentação lida por agentes — vale para `claude-memoria/`, `CLAUDE.md` e `.claude/rules/` |
| `grill-with-docs` | **adotada** | entrevista de alinhamento que atualiza documentação de contexto — cobre o que o `brainstorming` do superpowers não grava |
| `tdd`, `code-review`, `diagnosing-bugs`, `grill-me`, `to-tickets` | descartadas | repetem `test-driven-development`, `requesting-code-review`, `systematic-debugging`, `brainstorming` e `writing-plans` do superpowers, que o processo do projeto já usa |
| `triage`, `to-spec`, `wayfinder`, `implement` | descartadas | dependem de um rastreador de issues (o projeto é solo e sem tracker) |
| `improve-codebase-architecture`, `codebase-design`, `prototype` | descartadas | orientadas a produto em desenvolvimento contínuo; o harness de experimentos é pequeno e congelado depois de cada bateria |
| `setup-matt-pocock-skills`, `ask-matt`, `wait-what`, `grilling` | descartadas | infraestrutura da coleção (configuração, roteamento, primitiva interna) sem valor isolado |
| `resolving-merge-conflicts`, `wizard`, `teach`, `to-questionnaire` | descartadas | sem cenário no projeto (sem conflitos de merge, sem walkthroughs, sem ensino multi-sessão, sem questionários) |
| pastas `deprecated/` e `in-progress/` | descartadas | o próprio autor as marca como obsoletas ou inacabadas |

Para as LLMs locais, o que os dois repositórios significam está em [ferramental-das-llms-locais.md](ferramental-das-llms-locais.md).

## 7.3 Outros complementos avaliados

Levantamento preliminar de 21/09/2026 (estrelas pela API do GitHub na data); o aprofundamento com dois agentes de leitura entra na sessão 6 e amplia esta tabela.

| Complemento | Tipo | Decisão | Motivo |
|---|---|---|---|
| `pyright-lsp` (plugin oficial) | análise de código Python | **adotar na sessão 6** | entrega o principal ganho prometido pelo servidor de memória de código (ir à definição, referências, diagnóstico após cada edição) com risco quase nulo; vigiar a memória (pyright é pesado) |
| `php-lsp` (plugin oficial, `intelephense`) | análise de PHP | adotar na sessão 6 se o PHP legado entrar na análise | 93 arquivos `.php` do cobaia; navegação simbólica onde o `grep` mais gasta |
| `/insights`, `/skill-doctor`, aba Stats do `/plugin` | medição oficial | adotar (sem instalação) | mostram custo de contexto e uso por skill; com 8 plugins ativos, o maior ganho pode ser remover, não adicionar |
| `explanatory-output-style` (plugin oficial) | estilo de resposta | **desligado neste projeto** (decisão do Eric, 21/09) | acrescentava blocos didáticos em toda resposta; custo fixo por turno |
| Context7 (62.267 ★) | documentação de bibliotecas sob demanda | reavaliar na Fase 4 | útil para Playwright; cada servidor MCP conectado é risco de invalidação de cache |
| Playwright MCP (Microsoft, 37.424 ★) | automação de navegador | reavaliar na Fase 4 | o TCC usará Playwright na fase seguinte; agora não |
| Serena (29.662 ★) | ferramentas semânticas via LSP | **descartado** | sobrepõe os plugins oficiais de LSP e tem issue de consumo de ~30 GB de RAM (inviável com 15,7 GiB) |
| GitHub MCP (33.097 ★) / plugin `github` | integração GitHub | descartado | a documentação oficial recomenda o CLI `gh` por ser mais econômico em contexto; `gh` ainda não está instalado |
| MCP oficiais `filesystem`, `fetch`, `memory`, `sequential-thinking` | referência do protocolo | descartados | redundantes com Read/Glob/Grep/WebFetch, com `claude-memoria/` e com o raciocínio estendido nativo |
| Repomix (28.439 ★) | empacota o repositório num arquivo | descartado como MCP; CLI ocasional | num repositório com venv versionada geraria um arquivo gigante sem `.repomixignore` cuidadoso |
| ccusage (18.660 ★) | medição de tokens pelos JSONL locais | substituído por `ferramentas/medir_tokens.py` | mesma leitura, sem dependência npm, com atribuição por tipo de agente |
| mem0 (65.760 ★) | memória persistente para agentes | descartado | pesado e orientado a produção; `claude-memoria/` já resolve de forma auditável, o que é metodologicamente melhor para um trabalho acadêmico |
| awesome-claude-code (54.382 ★) | lista curada | fonte para a sessão 6 | não é um complemento em si |

## 7.4 Práticas de economia de tokens adotadas em 21/09/2026

| Prática | Onde está | O que faz |
|---|---|---|
| Primeiro a máquina, depois o modelo | `CLAUDE.md` (seção "Economia de tokens") e `ferramentas/` | busca, contagem, render, dedup, conciliação, medição e verificação em scripts Python; o modelo lê só o resumo |
| Hook `PreToolUse` que resume saídas longas | `.claude/settings.json` → `ferramentas/gancho_pre_bash.py` → `resumir_saida.py` | comandos verbosos (`testar_fase3*.py`, `avaliar_fase3*.py`, `rodar_*.ps1`, `git diff`) chegam ao contexto com cabeça, cauda e linhas de falha (500 linhas viram 51 no teste) |
| Regras por tipo de arquivo | `.claude/rules/{powershell,experimentos,documentacao}.md` | as convenções carregam só quando o arquivo daquele tipo é editado; `CLAUDE.md` fica com 64 linhas |
| Permissões de leitura sem confirmação | `.claude/settings.json` (`permissions.allow`) | `git status/diff/log`, `ls`, `grep`, testes sem LLM, medição — menos interrupções |
| Modelo, esforço e plugins fixados no início da sessão; `/clear` entre pacotes; `/rewind` antes de `/compact` | regra de trabalho | o cache de prefixo da Anthropic é por prefixo exato; mudar modelo, esforço ou servidor MCP no meio da sessão o invalida |
| Sonnet no trabalho mecânico e nas verificações de citação; um revisor por entregável; ondas de até 30 agentes; nunca dois Workflows ao mesmo tempo | regra de trabalho | na Fase 3 cada onda de revisão custou ~1,6 M tokens e o limite de sessão caiu quatro vezes |
| Conferências por script | `ferramentas/conferir_docs.py`, `render_levantamento.py --check`, `decidir_modelo.py --check` | links, tags com motivo, frases obsoletas, hipóteses, BOM, formato das seções e números gerados — sem revisor por agente |
| Configuração versionada | `.gitignore` estreitado para `.claude/settings.local.json` | `settings.json`, `rules/` e `skills/` chegam à outra máquina pelo git |

## 7.5 Medição de consumo

`ferramentas/medir_tokens.py` soma o `usage` de cada resposta do modelo nos transcritos locais (`~/.claude/projects/<projeto>/`), uma vez por resposta (dedup por identificador da mensagem), por dia, por modelo e por tipo de agente (principal, subagente, workflow).

**Antes das medidas** (linha de base gravada em 21/09/2026, antes de qualquer mudança desta rodada; 5.271 respostas do modelo desde 09/09):

| Corte | Respostas | Entrada nova | Cache criado | Cache lido | Saída | Cache lido / entrada |
|---|---|---|---|---|---|---|
| 11/09 | 2.225 | 6.424 | 8.336.150 | 125.409.549 | 327.555 | 93,8% |
| 12/09 | 1.621 | 11.768 | 14.238.341 | 346.564.698 | 278.494 | 96,1% |
| 13/09 | 1.331 | 3.190 | 3.522.114 | 32.928.113 | 65.963 | 90,3% |
| principal (todas as datas) | 264 | 5.954 | 4.846.060 | 142.696.970 | 535.937 | 96,7% |
| subagentes | 1.781 | 4.870 | 12.084.173 | 282.239.308 | 151.071 | 95,9% |
| workflows | 3.226 | 11.264 | 10.294.179 | 91.589.803 | 63.548 | 89,9% |
| **total de saída** | | | | | **750.556** | |

Leitura: o custo faturável dominante é a saída gerada (750 mil tokens no período), e a leitura de cache já cobre mais de 90% da entrada — as medidas que mais pesam são as que reduzem saída e número de agentes (scripts no lugar de agentes, um revisor por entregável, resumos de saída), não as que mexem no cache.

<!-- ! Alteração de IA - Revisar: medição "depois" acrescentada em 22/09/2026 (mesmo script, mesmos cortes), cobrindo as duas sessões do plano complementar (21 e 22/09).
     ! Motivo: a seção prometia a medição depois das medidas; os números mostram que o custo não caiu — mudou de lugar —, e dizer isso é mais útil do que prometer economia. -->
**Depois das medidas** (medição de 22/09/2026 ao fim da sessão 2 do plano complementar; 6.738 → 7.166 respostas desde 09/09):

| Corte | Respostas | Saída | Cache lido / entrada |
|---|---|---|---|
| 21/09 (sessão 1: P0, P4-lite, P1 com Workflow de 82 agentes, P3.1, P2.1) | 1.206 | 360.262 | 96,2% |
| 22/09 (sessão 2: análise e textos, P5 com Workflow de 113 agentes, P4) | 780 | 267.173 | 92,2% |
| principal (todas as datas) | 430 | 1.048.609 | 97,4% |
| subagentes (todas as datas) | 2.069 | 157.076 | 95,9% |
| workflows (todas as datas) | 4.667 | 100.855 | 89,4% |
| **total de saída** | | **1.306.540** | |

Leitura honesta: as duas sessões do plano complementar geraram 627 mil tokens de saída em 1.986 respostas, contra 750 mil em 5.271 respostas nas sessões de 11–13/09. O custo por sessão **não caiu**: ele mudou de lugar. Os agentes passaram de 5.007 para 1.729 respostas (Workflows menores, um revisor por entregável, verificações em Sonnet), mas o laço principal, que antes despachava e agora escreve os documentos e os scripts diretamente, subiu de 536 mil para 1.049 mil tokens de saída acumulados (+513 mil nas duas sessões). O que mudou de fato foi a **previsibilidade**: nas quatro sessões de 11–13/09 o limite de sessão derrubou ondas de agentes quatro vezes; em 21–22/09, uma vez (21/09, 13:20), com retomada por `resumeFromRunId`, e nenhum trabalho se perdeu. A leitura de cache seguiu acima de 89% em todos os cortes; a economia de entrada já estava feita antes das medidas. O que ainda pode reduzir a saída é o que a §7.10 aponta: `effort` baixo nos subagentes mecânicos e o estilo `Concise` nas respostas ao Eric.

## 7.6 O que foi feito em 22/09/2026 e o que fica

<!-- ! Alteração de IA - Revisar: seção reescrita em 22/09/2026 — a lista "para a sessão 6" virou o registro do que foi feito na sessão 2 do plano complementar e do que resta.
     ! Motivo: a P4 foi antecipada (instalação, plugin, levantamento de complementos, medição) enquanto o Workflow da pesquisa das LLMs locais rodava; deixar a lista antiga faria o leitor procurar uma sessão 6 que não existe mais nesse formato. -->
1. **`pyright-lsp`** ligado em `.claude/settings.json` do projeto (`enabledPlugins`); instala do marketplace oficial na próxima abertura da sessão. `php-lsp` fica de fora até o PHP legado entrar na Fase 4.
2. **`codebase-memory-mcp`** instalado com as salvaguardas e registrado em escopo de projeto (7.2); regra de permanência a aplicar na primeira sessão com o servidor ativo.
3. **Levantamento de complementos**: dois agentes de leitura (Sonnet) sobre "MCP, plugins e skills para Claude Code em 2026" e "economia de tokens e memória persistente" — resultado em 7.7, com o veredito de cada item.
4. **Medição "depois"** em 7.5; atualização do Claude Code feita pelo Eric em 22/09 (o atalho antigo do npm ficou quebrado — ver `pendencias.md`).
5. Fica: aplicar a regra de permanência do servidor MCP; confirmar a instalação do `pyright-lsp`; repetir a medição ao fim da Fase 4.

## 7.10 Levantamento de complementos (22/09/2026): adotado, adiado e descartado

<!-- ! Alteração de IA - Revisar: seção nova (22/09/2026) com o resultado dos dois agentes de leitura (Sonnet) sobre MCP/plugins/skills e sobre economia de tokens/memória, revisto pelo controlador; relatórios completos em `.superpowers/sdd/fase3b-e-fechamento/report-p4-*.md` (fora do git). A numeração pula para 7.10 porque 7.7–7.9 estão em ferramental-das-llms-locais.md.
     ! Motivo: o plano complementar (P4.3) pedia esse levantamento com veredito e motivo para cada item, inclusive o descartado; os vereditos que mexem em configuração ficam como sugestão ao Eric — nada de configuração foi alterado por pedido de agente. -->

Dois agentes de leitura, só com busca na web (documentação oficial do Claude Code e da API, consultada em 22/09/2026; repositório `anthropics/claude-plugins-official`; blogs de 2026 onde indicado). O veredito abaixo é o do controlador, à luz das regras do projeto (CLAUDE.md, decisões 49 e 50); onde difere do agente, o motivo diz por quê.

**O que a documentação oficial confirma sobre o que o projeto já faz**

| Prática do projeto | O que a documentação diz | Fonte |
|---|---|---|
| Hook `PreToolUse` que resume saídas longas | É o exemplo oficial de "offload processing to hooks": um hook que filtra a saída de testes reduz "dezenas de milhares" de tokens para "centenas"; saída de hook acima de 10.000 caracteres vai para arquivo e o modelo recebe só um preview | code.claude.com/docs/en/costs; /context-window |
| Regras por caminho em `.claude/rules/`, CLAUDE.md < 200 linhas | Meta oficial: "target under 200 lines per CLAUDE.md file"; regras com `paths:` só entram no contexto quando um arquivo correspondente é lido, e editar CLAUDE.md no meio da sessão não invalida o cache, mas só aplica após `/clear`, `/compact` ou reinício | code.claude.com/docs/en/memory; /prompt-caching |
| Modelo, esforço e plugins fixados no início; `/rewind` antes de `/compact` | "Pick your model and effort level at the top of a session, then save /compact for natural breaks"; o que invalida o prefixo: troca de modelo, de effort, fast mode, conectar/desconectar MCP com tools não deferidas, plugin com MCP, `/compact`, excesso de imagens, upgrade do Claude Code; `/rewind` reaproveita um prefixo já em cache, `/compact` reconstrói | code.claude.com/docs/en/prompt-caching |
| Sonnet nos subagentes mecânicos; um Workflow por vez | Cada subagente tem cache próprio (TTL de 5 min por padrão, mesmo em assinatura; `subagentPromptCacheTtl` a partir da 2.1.242); num fan-out com o mesmo prefixo, os agentes além do primeiro esperam até 5 s para ler o cache que o primeiro escreveu — dois Workflows simultâneos disputariam prefixos | code.claude.com/docs/en/prompt-caching; /sub-agents |
| Scripts locais para busca, contagem e render | É o princípio de "context engineering just-in-time" da Anthropic; ferramentas de linha de comando são "mais eficientes em contexto que servidores MCP porque não acrescentam listagem por ferramenta" | anthropic.com/engineering/effective-context-engineering-for-ai-agents; /costs |
| Memória em `~/.claude/projects/<projeto>/memory/` + handoffs versionados | Auto memory grava notas `user`/`feedback`/`project`/`reference` com índice `MEMORY.md` (só as 200 primeiras linhas ou 25 KB entram por sessão), por repositório e local à máquina — o que justifica os handoffs versionados em `claude-memoria/` para atravessar máquinas | code.claude.com/docs/en/memory |
| Cache de prefixo como base da economia | Leitura de cache a 0,1× do preço de entrada (0,025× em Fable 5.1); escrita a 1,25× (5 min) ou 2× (1 h); TTL de 5 min renovado a cada uso, 1 h por padrão na conversa principal só em plano Claude dentro do uso incluso | platform.claude.com/docs/en/build-with-claude/prompt-caching; code.claude.com/docs/en/prompt-caching |

**Itens novos, com veredito**

| Item | Veredito | Motivo |
|---|---|---|
| `pyright-lsp` (plugin oficial) | **Adotado** (ligado em 22/09) | Diagnósticos e navegação sem grep; exige o binário `pyright-langserver`, a conferir na próxima abertura |
| `php-lsp` (Intelephense) | **Adiado** (o agente sugeriu adotar) | O PHP legado só entra na análise na Fase 4; instalar antes soma um servidor de linguagem sem uso |
| Outros 9 LSP oficiais | Descartado | Linguagens ausentes do repositório |
| Effort baixo nos subagentes mecânicos | **Adotado nos Workflows** | A documentação de effort recomenda `low` para subagentes; os verificadores de citação já rodam em `medium` e os mecânicos passam a `low` nos próximos scripts |
| `/context` e `/usage` (estatística de cache, ≥ 2.1.251) | **Adotado** como rotina de início e fim de sessão | Diagnóstico local, sem tokens; complementa `medir_tokens.py` |
| `/fewer-permission-prompts` | Já adotado (21/09) | A página oficial não foi localizada pelo agente; o comando existe no CLI e gerou a allowlist de `.claude/settings.json` |
| Output style `Concise` | Sugestão ao Eric | Reduz tokens de saída e a troca não invalida o cache; muda o estilo das respostas, então é escolha dele |
| Status line com `prompt_cache` | Sugestão ao Eric | Monitoramento contínuo sem tokens; schema dos campos não confirmado na página `statusline` |
| `subagentPromptCacheTtl: "1h"` | Adiado | Só compensa se as ondas de agentes ficarem mais de 5 min entre chamadas do mesmo agente; medir antes |
| Tool Search / ferramentas diferidas | Já é o padrão | Só relevante se o número de tools MCP crescer; é o que mantém o `codebase-memory-mcp` barato em contexto |
| `security-guidance` (camada 1: regex local) | Adiado | Zero tokens, mas o repositório é ambiente cobaia com falhas de segurança deixadas de propósito (README): os alertas seriam ruído; as camadas 2–3 chamam Opus a cada turno — descartadas |
| `commit-commands` | **Descartado** (o agente sugeriu adotar) | Regra do projeto: o Claude nunca commita; o Eric commita ele mesmo |
| `code-review`, `pr-review-toolkit`, `claude-security` | Adiado / adiado / descartado | Um revisor por entregável já cobre; auditoria de segurança de múltiplos agentes é excesso para o escopo |
| `github`, `sentry` (MCP embutidos) | Descartado | `gh` preferido; sem produção monitorada |
| `claude-code-setup` | Adiado | Sem README verificado |
| `obra/superpowers` (já em uso) | Manter e medir | A skill `using-superpowers` entra em toda conversa; conferir o custo em `/context` |
| `obra/superpowers-marketplace`, `-lab` | Adiado | Experimentais |
| `anthropics/skills` (docx, pptx, xlsx…) | Manter só o usado | Úteis para o texto do TCC; nada a expandir |
| mem0 / OpenMemory, Letta, Zep | Descartado | Servidor externo de memória com custo de manutenção e invalidação de cache; CLAUDE.md + auto memory + handoffs versionados já resolvem |
| Regressão de TTL relatada em mar/2026 | Registrado, sem ação | Relato de usuários; a documentação atual descreve os dois TTLs |
| "Task budgets" (orçamento de tokens por laço) | Não coberto | O agente esgotou o orçamento de buscas; fica como lacuna |

**Limites**: as páginas oficiais são "vivas", sem data de publicação (usada a data de consulta); custos de contexto por plugin só aparecem no painel `/plugin`, não foram medidos; o `marketplace.json` foi lido truncado (~70 de 200+ plugins); o percentual do auto-compact e o limite de saída de MCP (~25k tokens) não têm fonte oficial; nada foi testado na prática.
