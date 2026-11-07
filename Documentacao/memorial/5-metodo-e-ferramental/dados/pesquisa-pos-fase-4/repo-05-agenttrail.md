<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre repositório sodiumsun/agenttrail, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# agenttrail (sodiumsun/agenttrail): levantamento para o TCC

Fontes lidas: página do repositório, README.md, docs/INGEST.md, docs/OBSERVABILITY.md e package.json (raw.githubusercontent.com, ramo HEAD), em 7 nov. 2026. Não há artigo ou paper citado; a página do GitHub não lista releases.

## 1 O que é e como funciona por dentro

- É um observador local de agentes de programação (Claude Code, Codex, pi e outros). Descrição da página: mostra o projeto como um mapa vivo do que cada agente está fazendo. Não roda agentes e não decide quando uma tarefa terminou.
- O que grava/lê: logs locais do Claude Code (`~/.claude/projects`) e do Codex (`~/.codex/sessions`), mudanças de arquivo via watcher, Git em modo leitura (branches, worktrees) e, opcionalmente, eventos de hooks do Claude Code. Lê só logs tocados nas últimas 2 horas e no máximo os últimos 2 MiB de cada um.
- Formato dos eventos de ingestão: JSON por POST em `127.0.0.1:<porta>/hook` (portas 5330 a 5344). Campos comuns: `hook_event_name`, `cwd`, `session_id`, `agent`. Tipos: SessionStart, PreToolUse, PostToolUse, PostToolUseFailure, TodoUpdate, Stop, SessionEnd, SubagentStop. Há `tool_use_id` e `files_written`.
- Não há campo de pai/filho: o doc de ingestão diz que não define parent. SubagentStop fecha "a linha de subagente aberta mais antiga", sem referenciar id.
- Estrutura de intenção: um `PLAN.md` com convenção própria (componentes `## Título {#id}`, tarefas `- [~] ... {#id}` com marcadores x, ~, !, vazio; campos `files:`, `needs:`, `links:`, `by:`, `from:`, `kind:`; seção `## decisions` com linhas datadas em texto livre).
- Como mostra: uma página estática em `localhost:5330` com cartões de componentes ligados por setas (`needs:`/`links:`), cartões de execução com ferramenta atual e trilha de arquivos, e uma visão inferida do Git quando não há plano. Há também um painel no app desktop Herdr e `GET /panel` (resumo versionado, somente leitura).
- Rótulos de evidência: "reportado", "observado", "inferido", "desconhecido"; progresso ausente nunca vira percentual. Isso é o ponto conceitualmente mais útil.
- Armazena em `~/.agenttrail` atividade recente, resumos e posições de leitura, com texto de comando encurtado (não guarda respostas completas nem saída de ferramenta).
- O doc de observabilidade diz expressamente que não há conceito de decisão, alternativa ou raciocínio, e que não oferece trilha completa de requisições ao modelo.

## 2 Pilha, dependências e exigências

- Linguagem: daemon Node sem dependências e página estática (a página não mostra o gráfico de linguagens; "não visto" a divisão exata).
- Exige Node 20 ou superior (package.json: `engines: node >=20`). Sem `dependencies` declaradas. Uso via `npx agenttrail`.
- GPU: não. Nuvem: não (liga só em 127.0.0.1, sem conta, sem telemetria, sem chamadas a modelo). Chave de API: não. Framework de agente específico: não, mas os adaptadores nativos são para Claude Code, Codex e pi; outros agentes precisam postar eventos.
- Windows: o README diz que é "não testado"; as verificações automáticas rodam em Linux e macOS. O endpoint de hook não exige token (qualquer processo local pode postar).
- Licença: MIT.
- Maturidade: 989 estrelas, 70 forks, 5 observadores, 147 commits na main; versão 0.4.1 (package.json). Releases: nenhuma listada na página. Data de criação: não vista (página não mostra). Data do último commit: não vista (a página não exibe datas). Contribuidores: seção sem entradas visíveis. O README cita um projeto aposentado, "Kitchen", ainda no npm como `agenttrail-kitchen`.
- O repositório tem `CLAUDE.md`, `AGENTS.md`, `PLAN.md`, `CONTRIBUTING.md`, e pastas `docs/`, `integrations/pi`, `herdr/`, `public/`, `test/`, `bin/`.

## 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

- Serve? Parcialmente, como observador do próprio trabalho de desenvolvimento. Lê automaticamente os logs do Claude Code e mostra sessões, ferramentas, arquivos tocados, subagentes e listas de tarefas (TaskCreate/TodoWrite). Isso encaixa com as ondas de subagentes e o livro-razão `.superpowers/sdd/`.
- Para quê: ver numa página quais sessões/subagentes mexeram em quais pastas, e ligar isso a um `PLAN.md`. O projeto já tem plano, fichas e painel próprio, então o ganho é pequeno e duplica o painel do projeto.
- Custo de instalar: baixo (`npx agenttrail`, nada instalado de forma permanente), mas exige Node 20 na máquina. Windows corporativo sem administrador: Node portátil seria necessário; Windows não é testado pelo autor, então caminhos de `~/.claude` e o watcher podem falhar.
- Custo de manter: o autor avisa que formatos de log locais mudam entre versões do agente; é preciso acompanhar o pacote. O `init` escreve em CLAUDE.md/AGENTS.md e hooks em `.claude/settings.local.json`; isso alteraria arquivos que a regra do projeto manda marcar com a tag de IA, então só se usaria sem `init` (observação passiva, que não grava nada).
- Conflito com a regra de economia: Node é um runtime a mais; não pesa em tokens, mas pesa em manutenção.

## 4 Aplicação dentro do agente ou do produto

- Como base da árvore de decisão lida da trilha v2: não como código nem como formato. O agenttrail registra o que o agente fez (ferramentas, arquivos, tarefas), não por que escolheu um caminho. Não existe alternativa considerada, motivo, evidência por escolha ou divergência. Também não existe `pai` entre eventos (só `session_id`, `tool_use_id`). A trilha v2 tem nós com id e pai, alternativas, evidências e divergência: é mais rica no que importa para "Decisão 1, 2, 3".
- Semelhança de formato: apenas superficial (um evento por passo em JSON, id de sessão, id de chamada). Um evento por linha JSONL não é o formato dele: ele usa POST de JSON e logs próprios dos agentes.
- Ideias aproveitáveis, sem importar nada: (a) os quatro rótulos de evidência (reportado, observado, inferido, desconhecido) para dizer ao analista de onde veio cada afirmação de uma Decisão, e a regra de nunca mostrar percentual quando falta dado; (b) a seção `decisions` datada do `PLAN.md` como modelo de registro curto e legível; (c) o mapa de componentes com setas `needs`/`links` como inspiração visual da árvore. Módulo: trilha e relatório (rótulos) e painel/hub do analista (visual).
- Conflitos com o contexto:
  - Windows 11 corporativo sem administrador: Node 20+ não faz parte do ambiente (exigiria runtime extra); o autor não testa em Windows.
  - Harness em Python só com biblioteca padrão e painel em HTML estático gerado por Python: um daemon Node e uma página própria quebram essa regra.
  - Prompt congelado e trilha v2 já definida: o formato do agenttrail não traz alternativas nem pai; adotá-lo exigiria remodelar a trilha.
  - Um modelo por vez, 16 GB, CPU: sem efeito direto (ele não chama modelo), mas rodar um daemon permanente é carga a mais.
  - Nada em nuvem: compatível (127.0.0.1 só).
  - Observar o agente de QA: ele lê logs do Claude Code e Codex; o agente do TCC usa Ollama e Playwright, sem adaptador, então só entraria por POST manual, o que replica o que a trilha já grava.

## 5 Risco, esforço e veredito

- Uso no Claude Code: risco baixo a médio (Windows não testado, Node a mais, `init` altera CLAUDE.md e hooks, endpoint sem token, formatos de log sujeitos a mudança). Esforço: cerca de 1 sessão de trabalho para experimentar passivamente com `npx`, mais manutenção eventual. Ganho marginal, porque o painel e o livro-razão do projeto já cobrem.
- Uso no agente/produto: como dependência, risco alto (quebra as regras de Python puro, estático e sem runtime extra). Como inspiração conceitual, risco nulo. Esforço: cerca de 0,5 sessão para copiar os rótulos de evidência e o texto das decisões para o relatório por caso e para a leitura da árvore.
- Veredito para o Claude Code: opcional e de baixo valor; testar só de forma passiva com `npx agenttrail` (sem `init`) se houver Node 20 portátil, senão dispensar.
- Veredito para o agente: não adotar como base nem como formato da árvore de decisão (não registra alternativas nem pai); aproveitar apenas a ideia dos rótulos reportado/observado/inferido/desconhecido e o registro datado de decisões, implementados em Python na trilha e no relatório.

## 6 Referências ABNT NBR 6023

SODIUMSUN. **agenttrail**: local observability for AI coding agents. Disponível em: https://github.com/sodiumsun/agenttrail. Acesso em: 7 nov. 2026.

SODIUMSUN. **agenttrail**: README.md. Disponível em: https://raw.githubusercontent.com/sodiumsun/agenttrail/HEAD/README.md. Acesso em: 7 nov. 2026.

SODIUMSUN. **agenttrail**: docs/INGEST.md. Disponível em: https://raw.githubusercontent.com/sodiumsun/agenttrail/HEAD/docs/INGEST.md. Acesso em: 7 nov. 2026.

SODIUMSUN. **agenttrail**: docs/OBSERVABILITY.md. Disponível em: https://raw.githubusercontent.com/sodiumsun/agenttrail/HEAD/docs/OBSERVABILITY.md. Acesso em: 7 nov. 2026.

Artigos citados pelo repositório: nenhum. Procurado no README, em docs/INGEST.md, docs/OBSERVABILITY.md e na página principal; só há links para o npm, o app Herdr (herdr.dev) e arquivos do próprio repositório.
