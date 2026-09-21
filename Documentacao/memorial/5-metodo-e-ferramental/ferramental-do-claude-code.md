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

**Decisão do Eric (21/09/2026): instalar com salvaguardas**, na sessão 6 e no início da sessão (ligar um servidor MCP no meio invalida o cache de prefixo): backup do PATH (`reg export HKCU\Environment`) e dos arquivos de configuração; binário via `npm install -g`, nunca o `install.ps1`; conferência imediata do PATH e do Defender (alerta = parar, desinstalar, registrar — máquina corporativa); MCP em escopo de projeto (`.mcp.json`) configurado à mão; indexação primeiro de uma cópia descartável, excluindo venvs, `resultados*`, `base_conhecimento` e `.superpowers`; medição em três tarefas fixas antes (Grep/Read) e depois (MCP). **Regra de permanência**: fica só se cortar ao menos 20% dos tokens dessas tarefas sem incidente; senão sai e o resultado fica registrado aqui. *(Estado: pendente — sessão 6.)*

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

Leitura: o custo faturável dominante é a saída gerada (750 mil tokens no período), e a leitura de cache já cobre mais de 90% da entrada — as medidas que mais pesam são as que reduzem saída e número de agentes (scripts no lugar de agentes, um revisor por entregável, resumos de saída), não as que mexem no cache. A medição **depois** (mesmo script, mesmos cortes) entra na sessão 6, ao lado da leitura do `/context`, do `/usage` e do painel Stats do `/plugin`.

## 7.6 O que fica para a sessão 6

1. Instalar `pyright-lsp` (e `php-lsp`, se couber) no início da sessão.
2. Instalar o `codebase-memory-mcp` com as salvaguardas de 7.2 e aplicar a regra de permanência.
3. Levantamento aprofundado de complementos (dois agentes de leitura: "MCP, plugins e skills para Claude Code em 2026" e "economia de tokens e memória persistente"), ampliando a tabela 7.3.
4. Medição "depois" e fechamento desta seção; atualização do Claude Code pelo Eric (`claude update` sem acesso ao npm nesta máquina).
