<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
<!-- ! Alteração de IA - Revisar: acrescentada a linha do working tree de 11/09/2026, com o
     que a Fase 3 trouxe e ainda não foi commitado.
     ! Motivo: a tabela ia até 09/09 e o trabalho da Fase 3 (correção dos 4 fixtures, módulos
     novos do harness, pré-registro no Memorial) está todo no working tree, porque quem
     commita é o Eric. Sem a linha, quem abrir o histórico depois do commit não saberia
     separar o que entrou pela Fase 3 do que já vinha da 2-B. -->
<!-- ! Alteração de IA - Revisar: em 12/09/2026 a linha do working tree passou a cobrir
     11–12/09, a listar todos os scripts novos da Fase 3 (não só dois), a dizer "26 checagens
     que devolvem 30 códigos" e a registrar o piloto de 10 casos do orquestrador e as decisões
     até a 44.
     ! Motivo: a linha dizia "26 códigos de rejeição" e `CODIGOS_REJEICAO` tem 30; dizia
     "ambos novos" quando `avaliar_fase3.py`, `comparar_fases.py`, `gerar_graficos_fase3.py`,
     `gerar_relatorio_fase3.py` e `rodar_fase3.ps1` também são arquivos novos do mesmo working
     tree; e a data 11/09 deixava de fora o dia em que a implementação foi concluída, revisada
     e o piloto rodou. -->
# O que foi construído, por commit

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

## 3. O que foi construído (referência por commit)

O código não é o foco do relatório; segue apenas o resumo por commit.

| Commit | Data | Conteúdo |
|---|---|---|
| `e854a0e` | 31/08 | Clonagem do site PHP cedido (197 arquivos) — ponto de partida |
| `ab4da6a` | 31/08 | Estrutura base: instalador cross-platform, `CobaiaAPI` completa (FastAPI + SQLAlchemy + PyMySQL), schema e seed do banco, página `produtos_api.php`, mecanismo de injeção de falhas |
| `26432d2` | 31/08 | `Cobaia.exe` (PyInstaller), README, correções de empacotamento |
| `dc1a7b8` | 01/09 | `.gitignore` revisto com base em evidência; correção da regra para outros sistemas operacionais |
| `084fce0` | 01/09 | Retrofit dos comentários de IA (20 arquivos) e normalização de nomenclatura |
| `1b0c4b8` | 01/09 | Correções no projeto de pesquisa ABNT e ajustes de planejamento |
| `4299b19` | 02/09 | Preparação dos modelos e primeira leva de testes de prolixidade e eficiência |
| `603c423`, `9d9d998` | 02–03/09 | Fase 2-A: taxonomia (6 classes × 3 níveis, 23 causas raiz), banco de 90 casos, três estratégias de prompt, bateria resumível um modelo por vez, avaliação e 6 gráficos. Fase 2-B (preparada em 03/09): biblioteca base com 36 verbetes em `AgenteCore/base_conhecimento/`, módulos `biblioteca.py` (parser/validador), `recuperacao.py` (BM25 + sinais em código + contextos A1–A5), `validar_banco.py`, `verificar_cache_prefixo.py`, `gerar_relatorio.py`; `avaliar.py` com Δ, McNemar, Wilson, ancoragem e flips; 5 gráficos novos. Correções de revisão: `FAULT_TARGET_FIELD` no `.env` (o modo por variável de ambiente não agia sem campo-alvo), desligamento limpo do MariaDB via `mariadb-admin`, checagem exata do modelo no `ollama list`, 10 testes novos na CobaiaAPI (13 passando), decomposição de tempo do Ollama gravada por inferência |
| `7731b0f` | 07/09 | Preparação da 2-B para a máquina-alvo: `caminhos.py` (`RESULTADOS_DIR`), `rodar_fase2b.ps1` com checagens de ambiente e A0 refeito, `maquina` em cada registro, pasta `claude-memoria/` (memória e regras portáteis), regra de BOM para `.ps1` |
| `918f7e5` | 09/09 | **Fase 2-B concluída na máquina-alvo** (commit feito lá): 2.610 inferências em `resultados_alvo/`, `maquina.json`, avaliação, gráficos e `relatorio.html` |
| `b067d87` | 09/09 | Relatório da 2-B por modelo, achados 4.22–4.28, decisões 27–28, gráficos 07–11 corrigidos (variantes de quantização fora, rótulo de 100% sem colisão), passagem de bastão em `claude-memoria/contexto/`, `importar.ps1` com mesclagem |
| `6a4381f` | 11–13/09 | **Fase 3 — preparação, antes de a bateria rodar.** Casos: os 4 fixtures do achado 4.20 corrigidos em `banco_casos.py` e `banco_casos_extra.py`. Harness: `evolucao_biblioteca.py` (partição 54/36 por hash, parser das propostas, 26 checagens que devolvem 30 códigos de rejeição, aplicação por acréscimo, conferência de somente-acréscimo, hash/diff/fechamento de época), `executar_fase3.py` (laço de épocas, retomada por caso), `avaliar_fase3.py`, `comparar_fases.py`, `gerar_graficos_fase3.py`, `gerar_relatorio_fase3.py` e `rodar_fase3.ps1` — todos novos; `testar_fase3.py` com os testes da fase, sem pytest; `biblioteca.py`, `recuperacao.py`, `validar_banco.py`, `caminhos.py`, `estrategias.py` e `executar_bateria.py` alterados sem mudar o que a 2-B produz. Piloto de 10 casos do orquestrador executado em 12/09 (`rodar_fase3.ps1 -Piloto`, 00h13; resultados em `resultados_alvo/fase3_piloto/`, fora do git). Documentação: plano aprovado em `claude-memoria/plano-aprovado-fase-3.md`, decisões 29–44, fechamento do achado 4.20, pré-registro 4.29, esqueletos do relatório da Fase 3 e da comparação entre fases, índice e pendências atualizados, README e memória portátil. Os briefs e relatórios de cada tarefa ficam em `.superpowers/`, **fora do git** (linha 19 do `.gitignore`), assim como o `fase3.log` e a pasta `resultados_alvo/fase3_piloto/`. Os resultados da bateria (~60 h) ainda não existem. A lista exata do que entra no commit sai de `git status` na hora |
| `b9f9ad9` | 13–15/09 | **Fase 3 executada na máquina-alvo** (commit só de resultados, 732 arquivos): `rodar_fase3.ps1` de 13/09 08:45 a 15/09 18:44 (`FIM … 58h59`, 0 falhas, Ollama 0.34.0), 4 modelos × (4 × 90 diagnósticos + 3 × 54 propostas) = 2.088 inferências; `resultados_alvo/fase3/` com `avaliacao_fase3.json`, `resumo_fase3.json`, `comparacao_fases.json/.md`, snapshots das bibliotecas por época, `relatorio_fase3.html`, três planilhas de revisão humana (63 edições) e os gráficos 12–17 |
| `1eb5cca` | 21/09 | **Plano complementar — sessão 1.** Registro da bateria (cabeçalhos de estado, período do Memorial, pendências, handoff novo); economia de tokens (`.claude/settings.json` com hook que resume saídas longas e permissões de leitura, `.claude/rules/` por tipo de arquivo, seção nova no CLAUDE.md, `.gitignore` estreitado, cinco skills copiadas de mattpocock/skills, `ferramentas/medir_tokens.py`, `resumir_saida.py`, `gancho_pre_bash.py`, `conferir_docs.py`); rodada 2 da pesquisa fechada por Workflow novo e integrada por script (`extrair_pesquisa.py`, `render_levantamento.py`, `integrar_pesquisa.py`: §6.9.9–6.9.17, mapa de decisões §6.10, 103 referências novas, contagens da rodada 1 corrigidas); documentos do ferramental (`5-metodo-e-ferramental/`); executor da Fase 3-B (`executar_fase3b.py`, `avaliar_fase3b.py`, `rodar_fase3b.ps1`, `testar_fase3b.py`) e ponte de versão do Ollama 0.34.1 em execução; decisões 45–51 |
| *(working tree, não commitado)* | 22/09 | **Plano complementar — sessão 2: decisão do modelo e análise.** Ponte de versão relançada pelo Eric à noite (3 Qwen nos 36: b/c 0/0, 1/1, 0/0; Granite pulado 2× por RAM e fora da 3-B — decisão 52); revisão das 63 edições em primeira passada pela IA (decisão 53: 23 corretas, 17 parciais, 23 erradas; `decidir_modelo.py` lê as planilhas direto); `decisao_modelo.*` regenerados com a ponte e a revisão (colunas b/c na 3-B); `gerar_tabelas_relatorio_fase3.py` (decisão 54) e `tabelas_relatorio.md` (29 blocos); relatório da Fase 3 §1–§9, §11, §12 e comparação entre fases §3–§6 preenchidos; achado 4.29 com vereditos e achados 4.30–4.35; `analise-decisoria-modelo-final.md` novo; mapa §6.10 com a coluna "Resultado medido"; decisões 52–55; pendências, README, Memorial e handoff de 22/09. Na mesma sessão: P5 (Workflow `pesquisa-llms-locais`, 113 agentes → `levantamento-2026-09-22-llms-locais.md` §6.12, +64 referências, §7.9 adotado/adiado/descartado, `integrar_pesquisa_llms.py`, `cache_respostas.py` + testes) e P4 (`codebase-memory-mcp` instalado com salvaguardas, `.mcp.json` e `.cbmignore`, `pyright-lsp` ligado, levantamento de complementos em §7.10, medição de tokens). |

<!-- ! Alteração de IA - Revisar: em 21/09/2026 as duas linhas "working tree" receberam os hashes dos commits do Eric (b067d87 de 09/09 e 6a4381f de 13/09) e entraram as linhas do commit b9f9ad9 (resultados da Fase 3) e do working tree de 21/09. Em 22/09/2026 a linha do working tree de 21/09 recebeu o hash 1eb5cca (commit do Eric em 21/09) e entrou a linha do working tree de 22/09.
     ! Motivo: o histórico dizia "não commitado" para trabalho que o Eric commitou em 13 e 15/09; a bateria de 58 h não constava em nenhuma linha. Datas de `git log --date=short`. -->

**Componentes resultantes:** `CobaiaFront` (PHP legado, intocado exceto por um link de menu e uma página nova); `CobaiaAPI` (FastAPI, 5 endpoints, 7 modos de injeção de falha); instalador único (`install.*`/`run.*`/`Cobaia.exe`) idempotente para Windows e Linux; e `AgenteCore/experimentos` com o harness de benchmark.


