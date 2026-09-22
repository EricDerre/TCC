<!-- ! Alteração de IA - Revisar: handoff da sessão 2 do plano complementar (22/09/2026): decisão do modelo fechada, ponte de versão, revisão das edições em primeira passada, relatórios preenchidos, e o que falta (3-B, P5, P4, P6).
     ! Motivo: a próxima sessão (ou a outra máquina) precisa retomar sem reler o chat; o handoff de 21/09 continua válido para o que ele descreve e este só acrescenta o que mudou. -->
# Handoff — 22/09/2026: decisão do modelo e análise da Fase 3

Continua o handoff de [21/09](2026-09-21-fase-3-concluida-e-plano-complementar.md) (plano complementar, ferramental, executor da 3-B). Livro-razão: `.superpowers/sdd/fase3b-e-fechamento/progress.md` (fora do git). Plano: `~/.claude/plans/delegated-hopping-steele.md`.

## O que mudou em 22/09

| Item | Estado |
|---|---|
| **Decisão do modelo** | **`qwen2.5:7b` com a biblioteca L1** (decisão 52, confirmada pelo Eric). Regra 36: 91,7% de acurácia balanceada nos 36; P(top-1) 77,6% (36) / 50,0% (90); Pareto: 3B L1/L2 e `qwen2.5:7b` L1/L3 não dominados; sensibilidade: só peso de custo ≥ 0,50 troca o vencedor. `resultados_alvo/fase3/decisao_modelo.{json,md}` (`--check` limpo). |
| **Ponte de versão (0.34.0 → 0.34.1)** | 3 modelos nos 36 (21/09 à noite): 3B 0/0, Coder 7B 0/0, `qwen2.5:7b` 1/1 (`sin-14`, `tra-10`); medianas iguais às da bateria (±1,5 s). Granite pulado 2× por RAM (7,8 < 8 GB) — fora da 3-B por decisão do Eric. `decisao_modelo.md` §6 (agora com colunas b e c). |
| **Revisão das 63 edições** | Primeira passada pelo Claude (decisão 53): 23 corretas (21 redundantes), 17 parciais, 23 erradas; `qwen2.5:7b` 9/8/12 (41,4% erradas). `decidir_modelo.resumo_revisao_humana` lê as planilhas direto (`fonte`), sem regravar `resumo_fase3.json`. Teste novo (18/18). |
| **Relatórios do Memorial** | `fase-3-relatorio-por-modelo.md` §1–§9, §11, §12 preenchidos; `comparacao-entre-fases.md` §3–§6; achado 4.29 com vereditos (H1 não, H2 não, H3 não/invertida, H4 parcial, H5 sim, H6 sim) e achados 4.30–4.35; `analise-decisoria-modelo-final.md` novo; mapa §6.10 com a coluna "Resultado medido" (28 linhas). |
| **Tabelas por script** | `gerar_tabelas_relatorio_fase3.py` (decisão 54): 29 blocos (`curva_*`, `qualidade`, `por_classe`, `por_nivel`, `pareado`, `flips`, `mde`, `recuperacao`, `documentacao`, `rejeicoes`, `custo`, `revisao`, `cf_*` de `comparacao_fases.md`, `dm_*` de `decisao_modelo.md`) em `resultados_alvo/fase3/tabelas_relatorio.md`; `--check` confere o derivado e os blocos colados nos três documentos. |
| **Documentação** | decisões 52–54; pendências (bloco "Abertas pela análise decisória"); histórico com 1eb5cca; README (decisão, scripts, ponte); Memorial (período, índice). |
| **Claude Code** | Atualizado pelo Eric em 22/09. A versão instalada não pôde ser lida de dentro da sessão: o atalho antigo do npm (`%AppData%\npm\claude.ps1`) aponta para um `claude.exe` que não existe mais — sinal de que a atualização foi pela instalação nativa; conferir com `claude --version` num terminal novo e, se o atalho do npm ainda estiver no PATH, removê-lo (`npm uninstall -g @anthropic-ai/claude-code`). |

## P5 e P4, feitas na mesma sessão

| Item | Estado |
|---|---|
| **Levantamento das LLMs locais (P5)** | Workflow `pesquisa-llms-locais` (113 agentes, 4,3 M tokens, 21 min): 8 tópicos, 94 afirmações aprovadas, 2 rejeitadas, 34 não verificadas (teto de 12 por tópico); integrado por `ferramentas/integrar_pesquisa_llms.py` em `levantamento-2026-09-22-llms-locais.md` (§6.12.1–6.12.10), 64 referências novas (342 no total), §7.9 do ferramental das LLMs com a tabela adotado/adiado/descartado (35 linhas), decisão 55. `--check` limpo. |
| **`cache_respostas.py`** | Cache exato, desligado por padrão, recusa em `resultados_alvo/`, `do_cache=True` com tempos zerados; 4 testes. |
| **P4** | `codebase-memory-mcp` 0.11.0 instalado com salvaguardas (PATH inalterado, Defender sem alerta, cópia descartável indexada); `.mcp.json` + `.cbmignore` na raiz (vigoram na próxima abertura; regra de permanência a aplicar então); `pyright-lsp` ligado em `.claude/settings.json`; levantamento de complementos em `ferramental-do-claude-code.md` §7.10 (relatórios em `.superpowers/sdd/fase3b-e-fechamento/report-p4-*.md`); medição "depois" em §7.5. |
| **Numeração** | §6.11 = análise decisória (mapa §6.10.4); §6.12 = levantamento das LLMs locais; §7.7–7.9 = ferramental das LLMs; §7.10 = complementos do Claude Code. |

## Fatos que a próxima sessão precisa saber

- **Correção de contagem**: 2-B A2 × F3 L0 tem b = c = 0 em **6 de 8** pareamentos (o Coder 7B tem 1/0 nos 36 e 2/3 nos 86), não "7 de 8" como o plano, o mapa (coluna de critério) e o handoff de 21/09 diziam; a coluna "Resultado medido" do mapa (linha 21) registra a divergência.
- Um dos 4 ganhos do `qwen2.5:7b` em L1 (`run-10`) é o modelo ter escrito o rótulo entre colchetes em L0 e L2; o avaliador conta como errado. Está dito no relatório §3.
- O custo por versão dentro da corrida não é comparável (passada final mais barata; prefill sobe com a biblioteca anotada) — relatório §9 e §11; o Pareto usa o custo medido mesmo assim.
- O prefill da proposta é menor que o do diagnóstico em **10** das 12 épocas (não 11: as exceções são as épocas 2 e 3 do 3B).
- Os registros oficiais em `resultados_alvo/fase3/` não mudaram (só nasceram `decisao_modelo.*`, `tabelas_relatorio.md` e as planilhas preenchidas — documentos derivados, permitidos pela regra).

## O que falta (ordem)

1. **Eric**: escolher os testes da 3-B (recomendação: (b) cruzada numa noite, depois (a) inéditos); revisar os 63 vereditos; autorizar a regeneração combinada de `resumo_fase3.json`; curadoria da cópia L1; `install.py`; commit; `git add -f` dos dois logs.
2. **Próxima sessão (início)**: confirmar o servidor MCP e o `pyright-lsp` na abertura; aplicar a regra de permanência do `codebase-memory-mcp` (três tarefas fixas pelas ferramentas MCP × grep; `medir_tokens.py`); registrar em `ferramental-do-claude-code.md` §7.2.
3. **P6 (quando a 3-B rodar)**: integrar (`decidir_modelo.py --saidas-3b fase3b_ponte fase3b_cruzada_qwen …`; relatório §11/§12; análise §10 e §8), regerar tabelas (`gerar_tabelas_relatorio_fase3.py` + `preencher_blocos`), handoff final, memória, `conferir_docs.py` limpo.
4. Feito nesta sessão: P0, P1, P2, P3 (menos os testes que o Eric escolher), P4 (menos a regra de permanência), P5 inteira.

## Comandos úteis

```
# decisão (com a ponte) e conferência
RESULTADOS_DIR=resultados_alvo python decidir_modelo.py --saida fase3 --saidas-3b fase3b_ponte --check
# tabelas do Memorial
RESULTADOS_DIR=resultados_alvo python gerar_tabelas_relatorio_fase3.py --saida fase3 --check
# documentação
python ferramentas/conferir_docs.py
```
