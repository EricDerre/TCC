<!-- ! Alteração de IA - Revisar: arquivo novo (01/10/2026) com a cópia integral do plano complementar de 21/09/2026,
     aprovado pelo Eric em modo de planejamento do Claude Code (fonte: `%USERPROFILE%\.claude\plans\delegated-hopping-steele.md`),
     com este cabeçalho acrescentado por cima; o texto do plano não foi reescrito.
     ! Motivo: o plano complementar só existia na pasta de planos do Claude Code, fora do repositório, e os handoffs de 21, 22 e
     23/09 apontam para aquele caminho. Em 01/10/2026 o mesmo arquivo passou a guardar o plano da Pré-Fase 4, e sem esta cópia o
     texto do plano complementar se perderia. Mesmo procedimento já usado para `plano-aprovado-fase-3.md`. -->

**Aprovado pelo Eric em 21/09/2026. Concluído em 01/10/2026.**

> Estado em 01/10/2026: todos os pacotes executados; as Fases 3 e 3-B estão fechadas (lista de fechamento em `Documentacao/memorial/3-resultados-e-analises/fase-3b-relatorio.md`, §9). Ficaram com o Eric as fichas 17 e 18 de `Documentacao/memorial/pendencias.md`. O que veio depois está em `plano-aprovado-pre-fase-4.md`.

# Plano complementar — fechar a pesquisa, decidir o modelo, Fase 3-B e ferramental do Claude

Data: 21/09/2026 · Máquina: i5-1235U, 15,7 GiB, Intel UHD integrada (sem CUDA), sessão RDP · Repositório: `C:\Users\Eric.Derre\Documents\TCC` (`main`, limpo em b9f9ad9)

> Este plano **complementa** o plano da Fase 3 (aprovado em 11/09/2026; cópia com anexo de desvios em `claude-memoria\plano-aprovado-fase-3.md`). O plano anterior **é concluído por inteiro aqui**: o que dele ficou aberto está na seção "Pendências do plano anterior" e cada pendência tem pacote e dono.

Notação: `RAIZ` = repositório; `EXP` = `RAIZ\Programacao\AgenteCore\experimentos`; `DOC` = `RAIZ\Documentacao\memorial`; `SDD` = `RAIZ\.superpowers\sdd\fase3b-e-fechamento` (pasta nova, fora do git); `CC` = `C:\Users\Eric.Derre\.claude\projects\c--Users-Eric-Derre-Documents-TCC\5c1c8fa0-31ce-4489-b7e9-314bf40961a1`.

## Contexto

- **Fase 3 concluída** (13/09 08:45 → 15/09 18:44; `FIM … 58h59` no `.ps1`, 57h59 entre marcos; 2.088 inferências; 0 falhas; Ollama 0.34.0; 3 relances = 1 por modelo). Resultados em `EXP\resultados_alvo\fase3\` (commit b9f9ad9): `avaliacao_fase3.json` (1.440 registros), `resumo_fase3.json` (13 seções; `revisao_humana: []`), `comparacao_fases.json/.md` (29 pareamentos), gráficos 12–17, `relatorio_fase3.html`, 3 planilhas `revisao_edicoes__*.md` com **63 edições sem avaliação** (o granite não tem planilha: 0 edições aceitas).
- **O que os números já dizem** (acerto % / acurácia balanceada %, nos 90 [nos 36]): granite L0 76,7/79,6 [80,6/83,3] e L3 igual (hash idêntico nas 4 épocas: 181 propostas, 0 aceitas, 133 por `texto_longo`); qwen2.5:7b L0 71,1/75,7 [77,8/81,2] → L1 76,7/**83,0** [88,9/**91,7**] → L3 77,8/80,7 [86,1/86,2] (61 aceitas, 9 verbetes novos, biblioteca 6.582 → 11.377 tokens); qwen2.5-coder:7b L0 71,1/75,8 → L1 74,4/78,9 → L3 72,2/75,4 (39 aceitas); 3b L0 65,6/71,5 → L3 67,8/72,6 (10 aceitas; omite TEXTO em 29–32 propostas por época). Nenhum McNemar com p < 0,05 (menor p = 0,1094); efeito mínimo detectável nos 36 = **19,4 pp**; autoenvenenamento máx. 5,6% nos 36 (H5 ok); `ouro_deslocado_por_novo` = 0 e MRR cai levemente em quem editou (H2 tende a não); `tentativas_de_decorar` = 0; nas épocas 2–3 as rejeições viram `duplicada`/`teto_notas_verbete` (saturação); prefill da proposta mais barato que o do diagnóstico em 11/12 (cache de prefixo agiu); custo mediano L3: granite 132,6 s, qwen2.5:7b 47,0 s, coder:7b 49,8 s, 3b 18,4 s; **2B_A2 × F3_L0 com b = c = 0 em 7 de 8 pareamentos** apesar de Ollama 0.33.3 → 0.34.0. Vereditos prováveis: H1 não (limite de amostra), H2 não, H3 invertido, H4 parcial, H5 sim, H6 sim (L1 melhor em 3 de 4).
- **Documentação parada em "bateria não executada"**: `fase-3-relatorio-por-modelo.md` (§2–§8 e §12 vazias, §1/§9 parciais), `comparacao-entre-fases.md` (§3–§6 vazias), achado 4.29 sem vereditos, decisões até 44, Memorial "Período coberto: 31/08 a 12/09", `plano-aprovado-fase-3.md` l.22 "aguardando decisão", livro-razão parado em 13/09, nenhum handoff desde 09/09, `fase3.log` fora do git.
- **Pesquisa bibliográfica**: rodada 1 integrada (§6.9.1–6.9.8; 154 aprovadas/12 rejeitadas; 175 referências). Rodada 2 (Workflow `wf_add7e8f0-e81`) caiu 3 vezes por limite de sessão e a crítica trocou a lista de lacunas a cada execução; valeu a lista de 13/09 (8 lacunas): 1 completa (agente autônomo de QA), 3 verificadas sem síntese (conflito contexto × conhecimento/sicofância; validação de artefatos gerados; prompting em estágios em modelos pequenos), 3 pesquisadas sem verificação (métricas de qualidade de documentação; aprender sem atualizar pesos/âncora no Faceli; taxonomia e rótulos-ouro), 1 sem pesquisa (recuperação em corpus pequeno e crescente); mapa de decisões nulo. Artefatos consolidados em `CC\workflows\wf_add7e8f0-e81.json` (`result.topicos`, 15 entradas) e no diário. **Retomar o Workflow antigo é risco alto** (cache reaproveitou só 2,5% e 8,3% nas retomadas; ~300 agentes e lista nova de lacunas).
- **Ambiente hoje**: Ollama **0.34.1** (mudou depois da bateria — qualquer teste novo precisa de ponte de versão); Claude Code 2.1.245 (estatística de cache só a partir de 2.1.251); Node 24, npm 11, Python 3.14, uv; sem Docker, sem `gh`; plugins ativos: superpowers, code-review, target-project-report, skill-creator, code-simplifier, claude-md-management, feature-dev, explanatory-output-style; nenhum servidor MCP; `.claude\` do projeto só com CLAUDE.md (52 linhas) e **ignorada pelo git** (`.gitignore` l.14).
- **Regras duras** (CLAUDE.md): nunca commitar (o Eric commita; nada de `git add` por conta própria — os comandos ficam prontos para ele); tag `! Alteração de IA - Revisar: <o quê>` + `! Motivo:` em todo trecho tocado; `.ps1` em UTF-8 com BOM e sem travessão; snake_case em português; sem jargão teórico; `base_conhecimento\` intocada; um modelo residente, `num_gpu=0`, `num_ctx=8192`; nenhum número digitado à mão em Markdown de resultados; perguntar antes de baterias longas; **executor oficial (`executar_fase3.py`), prompt pré-registrado (`estrategias.py`) e validador (`evolucao_biblioteca.py`) não mudam** — a Fase 3-B vive em arquivos novos.

## Decisões do Eric (21/09/2026)

| Tema | Decisão |
|---|---|
| codebase-memory-mcp | **Instalar com salvaguardas** (backup do PATH e das configurações; binário via npm, não o `install.ps1`; MCP em escopo de projeto configurado à mão; teste em cópia descartável; medir tokens antes/depois em 3 tarefas; desinstalar e documentar se falhar ou o Defender reagir). |
| mattpocock/skills | **Copiar 5 skills para `.claude\skills\` do projeto** (`research`, `domain-modeling`, `handoff`, `writing-for-agents`, `grill-with-docs`; MIT, com atribuição); as outras 21 avaliadas e registradas como descartadas com motivo. |
| Testes além da Fase 3 | **Análise primeiro, testes depois**: o menu (abaixo) já vem com custos; ao fim da análise eu indico o que acrescenta evidência e o Eric escolhe. Nome: **Fase 3-B** (a decisão 29 mantém Fase 4 = interceptador Playwright). |
| Processo | **Enxuto**: um revisor por entregável, conferências por script local, Sonnet/Haiku no mecânico, verificadores de citação em Sonnet, ondas ≤ 30 agentes, Workflow novo e curto para a pesquisa. |
| `.claude\` do projeto | **Estreitar o `.gitignore`** (ignorar só `.claude\settings.local.json`); `settings.json`, `rules\`, `skills\` versionados. |
| Ponte de versão 0.34.0 → 0.34.1 | **Pode rodar durante o dia** (2,5 h), assim que o executor da 3-B estiver testado. |
| `fase3.log` / `fase2b.log` | **Versionar** — comando `git add -f` deixado pronto; o Eric executa. |
| Plugin `explanatory-output-style` | **Desligar neste projeto**; registrado na documentação do ferramental. |

Explicitamente autorizado por este plano: **dois Workflows** (fan-out de agentes) — `pesquisa-r2` (P1, ≈ 85 agentes) e `pesquisa-llms-locais` (P5, ≈ 110 agentes) —, nunca simultâneos.

## Pendências do plano anterior (a concluir)

| Pendência | Pacote / dono |
|---|---|
| Relatórios da Fase 3 (§1–§9, §12) e comparação entre fases (§3–§6) | P2 |
| Revisão humana das 63 edições (`revisao_edicoes__*.md`, coluna "Avaliação" = `Correta`/`Parcial`/`Errada`) | Eric, entregue em P0; P2 apura |
| Rodada complementar da pesquisa (8 lacunas + mapa) | P1 |
| Vereditos H1–H6 no achado 4.29; achados 4.30+; decisões 45+ | P2 / P6 |
| Cabeçalhos "Estado em 12/09" dos dois relatórios; `plano-aprovado-fase-3.md` l.22; período do Memorial; livro-razão; handoff | P0 |
| Linhas de depuração (l.550/552) e parágrafo "O que ficou sem rodar" (l.34) do levantamento | P1 |
| `fase3.log`/`fase2b.log` fora do git | P0 (comando pronto; Eric executa) |
| Conferir Faceli 3. ed. (2025) com o exemplar; 5 referências ABNT sem URL; cronograma §5 do ABNT sem Fase 3; regerar PDF e retirar os 20 comentários | Eric (P6 só lista e prepara o texto) |
| `Tee-Object` em `rodar_fase2b.ps1` (grava UTF-16) | P6 — decisão do Eric: patch igual ao do `rodar_fase3.ps1` ou só registro |
| `install.py` aponta para o 3b "até a decisão sair" | Eric, depois da decisão (P6 prepara o texto) |

## Pacotes de trabalho

### P0 — Registro do que aconteceu (sessão 1, ~30 min, sem agentes)

- **Objetivo**: nenhum documento afirma que a bateria não rodou; o Eric recebe o que só ele faz.
- **Tarefas**: (1) `SDD\progress.md` (livro-razão novo) com a entrada da bateria 13–15/09 (início, fim, duração, relances, 0 falhas, versão) e `SDD\constraints.md` (rulings vigentes copiados de `.superpowers\sdd\delegated-hopping-steele\progress.md`); copiar `tools\snapshot.sh` e `tools\review-wt.sh` com `base=` apontando para a pasta nova. (2) Handoff `RAIZ\claude-memoria\contexto\2026-09-21-fase-3-concluida-e-plano-complementar.md` (estado, números-chave, o que falta, decisões deste plano). (3) Cabeçalhos: os dois relatórios → "Estado em 21/09/2026: bateria concluída 13–15/09; relatório em preenchimento"; `plano-aprovado-fase-3.md` l.22 → linha de estado nova; Memorial → "Período coberto: 31/08 a <data da sessão>". (4) `DOC\pendencias.md`: fechar "rodar a bateria" com data e duração; demais apontam para este plano. (5) Entregar ao Eric: caminho das 3 planilhas (63 linhas) e os comandos `git add -f EXP\resultados_alvo\fase3\fase3.log EXP\resultados_alvo\fase2b.log`.
- **Verificação**: `grep -rn "bateria não executada\|aguardando decisão\|31/08 a 12/09"` em `DOC` e `claude-memoria` vazio fora de motivos de tag; handoff existe.

### P4-lite — Economia de tokens antes de qualquer onda (sessão 1, início)

- (1) `claude update`; registrar a versão. (2) Medir: `/context`, `/usage`, `/plugin` (custo de contexto por plugin e aba Stats), `/insights`; `RAIZ\ferramentas\medir_tokens.py` (novo; lê `CC\*.jsonl` e `CC\subagents\**\*.jsonl`, soma `usage` por dia/modelo/tipo de agente, calcula a taxa de leitura de cache) → linha de base gravada em `SDD\medicao-antes.json`. (3) Desligar `explanatory-output-style` neste projeto (configuração de usuário; registrar). (4) `.gitignore`: trocar `.claude/` por `.claude/settings.local.json`. (5) `RAIZ\.claude\settings.json`: permissões de leitura via `/fewer-permission-prompts`; hook **PreToolUse em Python** (`RAIZ\ferramentas\gancho_pre_bash.py`, lê o JSON do stdin) que, para `testar_fase3*.py`, `avaliar_fase3*.py`, `rodar_*.ps1` e `git diff`, devolve `updatedInput` acrescentando `| python RAIZ\ferramentas\resumir_saida.py --cabeca 5 --cauda 40` (falhas e totais preservados); nunca hook que altere arquivo do repositório. (6) `RAIZ\.claude\rules\` com `paths:`: `powershell.md` (BOM, sem travessão), `experimentos.md` (stdlib, tag+motivo, snake_case, nunca `base_conhecimento\`), `documentacao.md` (números só de script; tag em `<!-- -->`; formato §6.9). (7) CLAUDE.md: seção "Economia de tokens" de ≤ 12 linhas (CLAUDE.md continua < 200 linhas). (8) Skills: copiar as 5 SKILL.md de mattpocock/skills para `RAIZ\.claude\skills\<nome>\SKILL.md` com cabeçalho de atribuição (MIT, URL, data, versão do commit).
- **Verificação**: hook testado com um comando de 500 linhas (saída ≤ 60 linhas, falhas preservadas); `/context` mostra as rules só nos arquivos certos; `git status` lista `.claude\settings.json`, `rules\`, `skills\`.

### P1 — Fechar a pesquisa bibliográfica (sessões 2–3)

- **Objetivo**: 8 sínteses novas verificadas e integradas (§6.9.9–6.9.16), mapa de decisões (§6.10), tudo o que foi rejeitado ou parcial registrado com motivo.
- **Tarefas**:
  1. `RAIZ\ferramentas\extrair_pesquisa.py` (novo, stdlib): lê `CC\workflows\wf_add7e8f0-e81.json` (`result.topicos`) e escreve `SDD\pesquisa\r2-entrada.json` por tópico da lista de 13/09 (`research.claims`, `verified`, `rejeitadas`, `synthesis`); imprime a conciliação e **para** se não bater com os fatos (conflito 20 = 15+5; validação 18 = 13+3+1+1; prompting 19 = 16+3; agente 20 = 20); fallback pelo diário (`label`).
  2. `SDD\pesquisa-r2.js` — Workflow novo (gerado por `extrair_pesquisa.py --gerar-workflow`, com a entrada inlinada; reaproveita CONTEXTO/REGRAS/schemas/prompts de `.superpowers\sdd\delegated-hopping-steele\pesquisa-fase3.js` l.126–175): 3 sínteses sobre as verificações prontas (conflito, validação, prompting) [modelo da sessão, effort high]; 56 verificações [`model: 'sonnet'`, effort medium] + 3 sínteses para métricas-doc, aprendizado-sem-pesos/Faceli e taxonomia; pesquisa + ≤ 20 verificações + síntese para recuperação-em-corpus-pequeno; **mapa de decisões** com entrada compacta (só `implicacoes_fase3_pt` + afirmações verificadas com número/condição/referência das 16 sínteses; **sem** lista ABNT) e schema `{linhas[≤30]{achado, numero, fonte, decisao_fase3}, riscos[]{risco, mitigacao, fonte}, metricas[]{metrica, fonte}, capitulos_faceli[]{capitulo, secao_memorial}}`. ≈ 85 agentes; sozinho na sessão; retomável por `resumeFromRunId`.
  3. `RAIZ\ferramentas\render_levantamento.py` (novo): JSON → Markdown no formato exato de §6.9.N (`#### 6.9.N Título (`key` — X aprovadas, Y rejeitadas)` / `*Título da síntese:*` / `##### Texto` / `##### Implicações para a Fase 3` com `* ` / `##### Lacunas` com `* ` / `##### Referências ABNT do tópico` com `- `) mais o bloco novo `##### Afirmações rejeitadas ou parciais (com motivo)`; gera §6.9.17 "Afirmações rejeitadas nas rodadas 1 e 2" e os blocos novos de `referencias.md` (`### <tema> (levantamento de 2x/09/2026)`) com dedup por chave normalizada (sobrenome + ano + 5 palavras do título) contra as 175 existentes e lista de quase-duplicatas para conferência; modo `--check` (regera e compara).
  4. Integração: `levantamento-2026-09-11-fase-3.md` (apagar l.550/552; substituir o parágrafo l.34; tabela de contagens com a rodada 2), `referencias.md`, novo `DOC\2-pesquisa-e-literatura\mapa-de-decisoes-fase-3.md` (§6.10, coluna "resultado medido na Fase 3" preenchida em P2), parágrafo-ponte em cada seção §6.1–6.8 apontando para as subseções novas. [eu escrevo; 1 revisor Sonnet confere fatos × JSON].
- **Verificação**: `render_levantamento.py --check` limpo; `conferir_docs.py` (P6) com 0 links quebrados; número de referências novas = número de `referencias_abnt` deduplicadas.
- **Custo**: ≈ 85 agentes (≈ 1,5 M tokens) + integração (≈ 0,2 M). **Dependências**: P4-lite antes.

### P2 — Análise decisória da Fase 3 (script na sessão 2; texto na sessão 4)

- **Objetivo**: decidir **modelo e estado da biblioteca** de produção pela regra pré-registrada, quantificar a robustez, preencher os relatórios com a literatura já integrada.
- **Ordem obrigatória** (para a decisão não parecer post-hoc): (1) **regra da decisão 36** — acurácia balanceada nos 36, veto por autoenvenenamento acima do limiar declarado, desempate por licença (o que `comparar_fases._melhor_f3`, l.233–249, já aplica por época); (2) robustez: bootstrap de casos (2.000 réplicas, `random.Random(20260921)`) sobre `avaliacao_fase3.json` → IC 95% da acurácia balanceada e **P(top-1)** por (modelo, L); estabilidade de ranking por coluna (2B_A0, 2B_A2, F3_L0..L3; nos 90 e nos 36; por classe; 2-A fora — máquina diferente); (3) fronteira de Pareto acerto balanceado × `segundos_mediana` × risco (`autoenvenenamento`, `adesao_cega_2B_A5_pct`, `fora_do_conjunto_pct`, `formato_ok_conteudo_errado_pct` de `comparacao_fases.json`); (4) escore ponderado com pesos **declarados** em `EXP\pesos_decisao.json` e varredura de sensibilidade (em que peso o vencedor troca) — só como análise de robustez.
- **Tarefas**: 1. `EXP\decidir_modelo.py` (novo, stdlib; CLI `--saida fase3 [--saidas-3b ...] --pesos EXP\pesos_decisao.json --semente 20260921`; saída `EXP\resultados_alvo\fase3\decisao_modelo.json` + `decisao_modelo.md` com `--check`); `EXP\gerar_graficos_decisao.py` (venv/matplotlib; figura 18 `18-decisao-pareto.*` em `resultados_alvo\graficos\`). Reutiliza `avaliar.wilson` l.144, `avaliar.mcnemar_exato` l.155, `avaliar_fase3.{acuracia_balanceada 189, holm 150, g_cohen 174, efeito_minimo_detectavel 231, slugs_da_saida 268, carregar_modelo 282, avaliar_registro_fase3 384, agregar_fase3 435, pareado_vs_l0 495, calcular_flips 577}`, `caminhos.fase3` l.42. 2. Testes em `EXP\testar_fase3b.py` (runner igual ao de `testar_fase3.py`): bootstrap reprodutível por semente, veto, Pareto com fixture de 3 modelos, `--check`. 3. Textos: `fase-3-relatorio-por-modelo.md` §1–§9, §11 (Ollama 0.34.0/0.34.1, `keep_alive: 0` entre modelos, MDE), §12; `comparacao-entre-fases.md` §3–§6; `achados-dos-modelos.md` 4.29 (vereditos) e 4.30–4.34 (granite anulado por `texto_longo`; reprodutibilidade b = c = 0 entre versões do runtime; saturação por `duplicada`/`teto_notas_verbete`; MDE como limite; L1 > L3); novo `DOC\3-resultados-e-analises\analise-decisoria-modelo-final.md` (pergunta → regra pré-registrada → resultado → robustez → custo → riscos → o que a literatura previa (§6.10) → decisão → limitações → o que a 3-B acrescentaria). Todo número copiado de `decisao_modelo.md` / `comparacao_fases.md` / `resumo_fase3.json`, com o nome do campo na primeira menção. 4. `revisao_humana` por modelo se o Eric tiver preenchido; senão §7 diz "sem avaliação" e o critério de qualidade das edições fica marcado como provisório.
- **Critério de aceite**: uma frase defensável — "modelo X com biblioteca L_y é o padrão porque [regra 36] + P(top-1) + custo mediano + riscos" — com todos os números rastreáveis a campos de JSON. Ao fim: a lista de quais testes do menu acrescentariam evidência (entrada da decisão do Eric sobre a 3-B).
- **Custo**: ≈ 6 agentes (≈ 0,6 M). **Dependências**: script — nenhuma; texto — P1 (mapa) e a ponte (P3.1).

### P3 — Fase 3-B: executor, ponte de versão e menu (executor e ponte na sessão 1; menu após P2)

- **Objetivo**: fechar as ameaças à validade que a decisão precisar, **sem tocar** em `executar_fase3.py`, `estrategias.py`, `evolucao_biblioteca.py`.
- **Tarefas**:
  1. `EXP\executar_fase3b.py` (novo, ~200 linhas): CLI `--modo {ponte,ineditos,cruzada,texto_max,a5} --saida <nome> --modelos ... [--doador <modelo>] [--versoes 0 1 3] [--texto-max 600]`. Prepara `caminhos.fase3(saida)`; copia com `shutil.copytree` as pastas fechadas `resultados_alvo\fase3\bibliotecas\<slug>\epoca-{n}` (o hash é preservado — `ARQUIVOS_IGNORADOS`, `evolucao_biblioteca.py` l.140); grava `particao.json` (oficial copiado, ou próprio com `particao: "avaliacao"` para os inéditos), `condicoes_3b.json` (modo, doador, `TEXTO_MAX`, versão do Ollama via `_versao_ollama` l.226) e `maquina.json` via `atualizar_maquina`/`maquina_atual` (l.239/204); chama `executar_fase3.rodar_epoca` (l.671) em modo "passada final" (`n = L+1`, `epocas = L`: lê `epoca-L` fechada, grava `diagnosticos__L{L}.jsonl`, não propõe) por (modelo, L); `cruzada`: uma `--saida` por doador; `texto_max`: copia `epoca-0` e `diagnosticos__L0.jsonl` do granite, faz `evo.TEXTO_MAX = N` em tempo de execução (o prompt continua dizendo 60–280: é ablação do validador), roda época 1 e passada final; `a5`: `executar_fase3.CONDICAO = "A5"` em tempo de execução. Descarrega no `finally` (`oll.descarregar` l.133; `um_modelo_por_vez`) e confere `versao_ollama` igual em todos os registros da saída.
  2. `EXP\avaliar_fase3b.py` (novo): `ponte`/`cruzada`/`texto_max` → `avaliar_fase3.avaliar_saida(c3)` l.1054 (os avisos "36 de 90" são esperados); `ineditos` → `avaliar_registro_fase3` l.384 (gabarito no registro) + `agregar_fase3`, `pareado_vs_l0`, `cochran_por_modelo`, `calcular_flips`, `rec.avaliar_recuperacao(verbetes, CASOS_INEDITOS)` (`recuperacao.py` l.314); grava `avaliacao_fase3.json`/`resumo_fase3.json` na pasta da saída.
  3. `EXP\rodar_fase3b.ps1` (novo; UTF-8 com BOM; sem travessão; `Marco/Rodar/EsperarRam/$RamMinima` copiados de `rodar_fase3.ps1`): `-Modo`, `-Saida`, `-Modelos`; roda `testar_fase3.py` e `testar_fase3b.py` antes; avalia ao fim; `FIM … modelos com falha`.
  4. Testes em `testar_fase3b.py`: cópia de snapshot preserva o hash; partição dos inéditos; `TEXTO_MAX` aplicado e restaurado; `avaliar_fase3b` em pasta sintética; hash de `base_conhecimento\` e de `resultados_alvo\fase3\` inalterados antes/depois.
  5. **Ponte de versão** (sessão 1, durante o dia, ~2,5 h): `rodar_fase3b.ps1 -Modo ponte -Saida fase3b_ponte` — L0 nos 36, 4 modelos (144 inferências). Leitura: b + c ≤ 2 por modelo nos 36 → F3 e 3-B pareáveis; senão a 3-B é lida só contra a própria ponte e §11 declara a ressalva.
  6. `EXP\banco_casos_ineditos.py` (só se o Eric escolher (a) após P2): 36 casos (2 por célula classe × nível; ids continuando a numeração) no formato `_c(...)` de `banco_casos.py`, validados por `taxonomia.validar_caso` e conferidos contra o código do Cobaia. **Regra de autoria**: o agente lê só `Programacao\Cobaia*`, `taxonomia.py`, `banco_casos*.py` — nunca `resultados_alvo\` (para não copiar as notas dos modelos). Gate: `bib.validar(bib.carregar(<L1/L3 de cada modelo>), CASOS_INEDITOS)` (l.325; sobreposição de 5-gramas ≤ 0,3) sem problema; o Eric confere 6 casos (1 por classe).
- **Verificação**: `rodar_fase3b.ps1` exit 0; `versao_ollama` = 0.34.1 em 100% dos registros da saída; `git status` sem mudança em `fase3\` nem em `base_conhecimento\`.
- **Custo**: ≈ 4 agentes (≈ 0,5 M); máquina: ponte 2,5 h; menu conforme escolha.

### P4 — Ferramental do Claude Code (restante; sessão 6, no início)

- (1) Plugins oficiais `pyright-lsp` (+ `php-lsp` se o PHP legado entrar na análise): instalar no início da sessão (ligar/desligar plugin ou MCP no meio invalida o cache de prefixo). (2) **codebase-memory-mcp com salvaguardas**, nesta ordem: `reg export HKCU\Environment SDD\backup-environment.reg` + cópia de `%USERPROFILE%\.claude.json`, `~\.claude\settings.json` e `RAIZ\.claude\settings.json`; `npm install -g codebase-memory-mcp` (nunca o `install.ps1`); conferir imediatamente que o PATH do usuário está íntegro e que o Windows Defender não alertou (se alertar: parar, desinstalar, registrar — máquina corporativa); `claude mcp add --scope project codebase-memory -- <comando do binário>` (gera `RAIZ\.mcp.json`; Eric commita se ficar); indexar primeiro **uma cópia descartável** de `EXP` + `Programacao\Cobaia*` no scratchpad, excluindo venvs, `resultados*`, `base_conhecimento`, `.superpowers`; só depois apontar para o repositório; medir com 3 tarefas fixas ("onde `TETO_TOKENS_CONTEXTO` é usado", "trace de `validar_proposta` → `aplicar_edicao`", "quais funções leem `fechamento.json`") antes (Grep/Read) e depois (MCP) por `/usage` e `medir_tokens.py`; **regra de permanência**: fica só se cortar ≥ 20% dos tokens nessas tarefas sem incidente; senão `claude mcp remove` + `npm uninstall -g` + restauração dos backups, tudo registrado. (3) 2 agentes Explore (Sonnet): "MCP, plugins e skills para Claude Code em 2026" e "economia de tokens e memória persistente" → tabela adotado / descartado / motivo (inclui os já avaliados: Context7 e Playwright MCP → reavaliar na Fase 4; Serena → não, 30 GB de RAM; GitHub MCP → preferir `gh`; filesystem/fetch/memory/sequential-thinking oficiais → redundantes; Repomix → CLI ocasional; ccusage → substituído por `medir_tokens.py`; mem0 → `claude-memoria\` já resolve). (4) Medir de novo e escrever `DOC\5-metodo-e-ferramental\ferramental-do-claude-code.md`: antes/depois, cache de prefixo (modelo/effort/plugins fixos no início; `/rewind` antes de `/compact`), a máquina não tem GPU utilizável (Intel UHD integrada, sem CUDA → "processamento local" = scripts em CPU; nunca LLM local auxiliar durante bateria), e a avaliação das 26 skills.
- **Verificação**: PATH íntegro (comparar com o `.reg`); `/context` e `/usage` registrados; `exportar.ps1` ainda funciona.
- **Custo**: ≈ 0,3 M.

### P5 — LLMs locais (sessão 5)

- (1) Veredito dos dois repositórios para o agente local, em `DOC\5-metodo-e-ferramental\ferramental-das-llms-locais.md`: MCP exige chamada de ferramenta via `/api/chat`, o harness usa `/api/generate` com prompt fixo (`cliente_ollama.py` l.60–95) e a Fase 4 não precisa de memória de repositório → **descartado com motivo**; skills Markdown ≈ verbetes de procedimento (o que a biblioteca já é) → ideia registrada para a Fase 4, não aplicável ao prompt pré-registrado. (2) Workflow `SDD\pesquisa-llms-locais.js` (mesma estrutura do `pesquisa-fase3.js`; pesquisa/síntese no modelo da sessão, ≤ 12 verificações Sonnet por tópico; mapa curto sem ABNT) com 8 tópicos: prompting para modelos pequenos e saída estruturada (GBNF/`format`); inferência em CPU (llama.cpp/Ollama: threads, quantização do KV, decodificação especulativa, batch); RAG em corpus pequeno (híbrido BM25 + embedding, rerank leve, reescrita de consulta); cache de respostas (o artigo do The New Stack + arXiv 2503.17603 e 2505.21889 + GPTCache/similares); modelos pequenos 2025–2026 e português (Qwen3, Gemma 3, Granite 4.x, Phi-4-mini, Tucano); frameworks de prompt/agente para modelos locais (DSPy, Outlines, guidance, clientes MCP para Ollama, Playwright MCP como interceptador); robustez a formato de prompt; verificadores/autoavaliação baratos. ≈ 110 agentes; sozinho na sessão; integração por `render_levantamento.py` em `DOC\2-pesquisa-e-literatura\levantamento-2026-09-2x-llms-locais.md` (§6.11) + `referencias.md`; tabela adotado/descartado/motivo. (3) `EXP\cache_respostas.py` (novo, ~80 linhas + teste): cache **exato** em SQLite (`chave = sha256(modelo|digest|prompt|json(options))`), `gerar_com_cache(...)` envolvendo `oll.gerar` sem alterá-lo, desligado por padrão (`CACHE_RESPOSTAS=1`), **recusa** quando `RESULTADOS_DIR` aponta para pasta de corrida oficial; uso previsto: laço de desenvolvimento da Fase 4 e demonstrações. (4) Documentar no §11 e no arquivo do ferramental: `keep_alive: 0` entre modelos apaga o cache KV (condição experimental); cache exato só fora de corrida medida; cache semântico **descartado** (não determinismo indefensável numa banca; embeddings na mesma CPU); o artigo não cita fontes (registrado). (5) Decisões 45+ (Fase 3-B; regra 36 antes de multicritério; ponte de versão obrigatória; cache; repositórios; ferramental; economia de tokens).
- **Custo**: ≈ 2,3 M. **Dependências**: P4-lite; nunca simultâneo ao Workflow de P1.

### P6 — Documentação e fechamento (sessão 6)

- (1) `Memorial de Desenvolvimento.md`: índice com `5-metodo-e-ferramental\`, §6.10, §6.11, `analise-decisoria-modelo-final.md`; período coberto. (2) `decisoes.md` 45+; `historico-por-commit.md` (6a4381f, b9f9ad9, próximo); `pendencias.md` (fechadas/novas). (3) `RAIZ\README.md`: seções Fase 3 (resultados) e Fase 3-B (scripts, saídas, `ferramentas\`). (4) Handoff final em `claude-memoria\contexto\` + `exportar.ps1`; memória do Claude atualizada. (5) `RAIZ\ferramentas\conferir_docs.py` (novo): links relativos, tag + motivo em todo arquivo tocado (busca por `de IA - Revisar`), frases obsoletas, H1–H6 idênticas em plano × achados × relatório, `--check` dos renders, BOM e ausência de travessão nos `.ps1`. (6) Uma revisão (Sonnet) por entregável de texto. (7) Comandos `git add -f` dos logs e a lista de arquivos para o Eric commitar.
- **Verificação**: `conferir_docs.py` limpo; `git status` lista só o previsto.

## Menu de testes complementares (Fase 3-B) — o Eric escolhe depois de P2

| Teste | Pergunta | Ameaça à validade que fecha | Inferências | Horas | Reaproveita | Autoria |
|---|---|---|---|---|---|---|
| Ponte de versão (obrigatória; já na sessão 1) | F3 (0.34.0) e 3-B (0.34.1) são pareáveis? | Instrumentação (runtime mudou) | 144 | 2,5 | `rodar_epoca` em passada final; `epoca-0` | 0 |
| (a) 36 inéditos × L0/L1/L3 × 4 modelos | O ganho de L1/L3 generaliza a casos nunca vistos? Quantas épocas? | Validade externa; os 36 de avaliação foram usados nas 3 fases; com 72 nunca vistos o MDE cai para ≈ 14 pp e o padrão b = 4 / c = 0 vira p < 0,01 — é o n que o MDE pediu, não p-hacking | 432 | 7,4 (só L0+L3: 5,0) | snapshots; `banco_casos_ineditos.py`; `avaliar_fase3b.py` | ~1 dia (Sonnet) + 6 casos conferidos pelo Eric |
| (b) cruzada essencial: L1 e L3 do qwen2.5:7b lidos por granite, coder:7b e 3b nos 36 | O ganho é da biblioteca ou de quem a lê? ("escreve o melhor, lê o mais barato" — revisita 4.25) | Confusão escritor × leitor | 216 | 4,0 (matriz completa 432: 7,4) | snapshots do doador; uma `--saida` por doador | 0 |
| (d) granite com `TEXTO_MAX` = 600, 1 época | O granite não sabe documentar ou foi barrado pelo teto? | Validade de construto de H4 | 54 + 90 | ≤ 6,2 | `diagnosticos__L0.jsonl` e `epoca-0` do granite | 0 |
| (c) A5 sobre L3 nos 36 (opcional, última prioridade) | Documentação própria muda a adesão cega? | H5 sob documentação própria | 144 | 2,5 | `CONDICAO = "A5"` em tempo de execução | 0 |
| (e) réplicas com temperatura alta | — | **descartado**: o cliente não fixa `seed`, T = 0,1 e b = c = 0 em 7/8 pareamentos já mostram determinismo prático; mexer na semente mudaria o caminho medido | — | — | — | — |
| (f) bootstrap, P(top-1), Pareto, sensibilidade | A decisão é robusta a 1–2 casos? | Decisão frágil | 0 | 0 | `decidir_modelo.py` | 0 |

Ordem recomendada se o Eric aprovar o conjunto: (b) → (d) → (a) (noites); (c) só para mais um argumento sobre H5.

## Regras de economia de tokens (valem para todo o plano)

1. Handoff lido no início de cada sessão; `/clear` entre pacotes; `/rewind` antes de `/compact`.
2. Modelo, `/effort` e plugins/MCP fixados **no início** da sessão (cache de prefixo): `high` nas sessões mecânicas (1, 2, 5), `max` nas de análise e escrita (3, 4, 6).
3. Implementadores mecânicos e verificadores de citação em Sonnet; o modelo da sessão só para síntese, mapa, análise, escrita e revisão de fatos. Um revisor por entregável; briefs ≤ 40 linhas; o revisor recebe o diff (`review-wt.sh`) só dos arquivos da tarefa.
4. Nunca dois Workflows ao mesmo tempo; ondas ≤ 30 agentes; agentes relatam só falhas e contagens.
5. Nada de JSON de resultados colado em prompt: agentes leem arquivos; saídas longas passam pelo hook `resumir_saida.py`.
6. Busca, contagem, render, dedup, conciliação, medição e verificação rodam em script local (`ferramentas\`), não em agente — mesmo que demorem.
7. `.claude\rules\` por caminho em vez de inflar o CLAUDE.md (< 200 linhas).
8. Medir antes/depois (`/context`, `/usage`, `medir_tokens.py`) e registrar em `ferramental-do-claude-code.md`.

## Calendário (sessões ≤ 5 h de limite; baterias sem o Claude)

| Sessão | Conteúdo | Máquina |
|---|---|---|
| S1 — 21/09 | P4-lite → P0 → `executar_fase3b.py` + testes → **ponte** durante o dia (2,5 h) | ponte |
| S2 — 22/09 | Workflow `pesquisa-r2` (sozinho) ‖ `decidir_modelo.py` e testes (arquivos disjuntos, sem segundo Workflow) | — |
| S3 — 23/09 | Integração de P1 + mapa (§6.10) + revisão | — |
| S4 — 24/09 | P2: textos, vereditos, análise decisória → lista dos testes que acrescentam evidência → **Eric escolhe a 3-B** | baterias escolhidas (noites seguintes) |
| S5 — 25/09 | Workflow `pesquisa-llms-locais` (sozinho) + `cache_respostas.py` + veredito dos repositórios | — |
| S6 — 28/09 | P4 restante (plugins, codebase-memory com salvaguardas, medição final) → integração da 3-B na análise (se rodou) → P6 → Eric commita | — |

## Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Limite de sessão derruba ondas (4× na Fase 3) | Ondas ≤ 30; Workflow sozinho; handoff por pacote; `resumeFromRunId`; Sonnet nos verificadores |
| Ollama atualiza no meio de uma bateria | Uma bateria por noite; `_conferir_versao_ollama` nos relances; `avaliar_fase3b.py` confere `versao_ollama` |
| Ponte mostra divergência 0.34.0 → 0.34.1 | 3-B lida só contra a própria ponte; §11 declara; a decisão fica na F3 |
| Eric não preenche as 63 avaliações a tempo | Entregue no dia 1; critério "qualidade das edições" marcado como provisório na decisão |
| Decisão parecer post-hoc | Regra 36 primeiro; multicritério só como sensibilidade; pesos declarados em arquivo |
| Casos inéditos contaminados ou fracos | Regra de leitura do autor; `bib.validar` contra L1/L3; `validar_caso`; amostra conferida pelo Eric |
| Número digitado à mão em Markdown | Renders com `--check`; `conferir_docs.py` |
| Mapa de decisões falhar de novo | Entrada compacta, schema fechado, sem ABNT (dedup local) |
| codebase-memory-mcp apagar o PATH ou disparar o Defender (máquina corporativa) | Backups (`.reg`, `.claude.json`, settings) antes; npm em vez do instalador; cópia descartável primeiro; regra de permanência; desinstalação registrada |
| Cache de prefixo do Claude invalidado no meio da sessão | Plugins/MCP/modelo/effort só no início da sessão |

## Verificação fim a fim

1. `PYTHONIOENCODING=utf-8 python EXP\testar_fase3.py` e `testar_fase3b.py` (Python do sistema e da venv) — todos ok.
2. `avaliar_fase3.py --saida fase3` regenerado em pasta temporária e comparado ao versionado (só `gerado_em` difere).
3. `rodar_fase3b.ps1` por modo: exit 0, "modelos com falha: nenhum", hashes de `resultados_alvo\fase3\` e `base_conhecimento\` inalterados, `versao_ollama` uniforme.
4. `decidir_modelo.py --check` e `render_levantamento.py --check` limpos.
5. `conferir_docs.py`: 0 links quebrados, tag + motivo em todo arquivo tocado, 0 frases obsoletas, H1–H6 idênticas, BOM/sem travessão nos `.ps1`.
6. `medir_tokens.py` antes/depois registrado; PATH íntegro após o MCP.
7. `git status` lista só os arquivos previstos; handoff atualizado; comandos `git add -f` prontos; **o Eric commita**.

## Fora do escopo

Fase 4 (interceptador Playwright, poda da árvore de acessibilidade, cura de seletor) e Fase 5 (MTTR); qualquer alteração em `executar_fase3.py`, `estrategias.py`, `evolucao_biblioteca.py` ou repetição da Fase 3; cache semântico; modelos novos (Qwen3, Gemma 3, Granite 4.x, Phi-4-mini, Tucano) em bateria — só na literatura; validação em Linux; fichamento formal; PDF do ABNT, referências sem URL e cronograma §5 (texto preparado; execução do Eric); troca do modelo padrão em `install.py` (Eric, após a decisão).
