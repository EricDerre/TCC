<!-- ! Alteração de IA - Revisar: handoff novo (21/09/2026) — estado depois da bateria da Fase 3 e o plano complementar aprovado.
     ! Motivo: o handoff anterior (09/09) para em "Fase 3 em implementação"; quatro sessões caíram por limite de tokens na Fase 3 e a bateria de 58 h não estava registrada em lugar narrativo nenhum. Quem abrir a próxima sessão lê este arquivo, não o chat. -->

# Passagem de bastão — 21/09/2026: Fase 3 concluída, plano complementar aprovado

Leia antes: `claude-memoria/contexto/2026-09-09-passagem-de-bastao-ryzen.md` (harness arquivo a arquivo, armadilhas pagas) e `claude-memoria/plano-aprovado-fase-3.md` (desenho da Fase 3 com o anexo de desvios). O plano complementar está em `C:\Users\Eric.Derre\.claude\plans\delegated-hopping-steele.md` (fora do git); o livro-razão desta rodada é `.superpowers/sdd/fase3b-e-fechamento/progress.md` (fora do git).

## 1. O que aconteceu desde 12/09

- **Bateria da Fase 3 executada pelo Eric**: `rodar_fase3.ps1`, 13/09 08:45 → 15/09 18:44, `FIM da Fase 3 - duracao total 58h59 - modelos com falha: nenhum` (57h59 entre marcos). 4 modelos × (4 × 90 diagnósticos + 3 × 54 propostas) = 2.088 inferências; Ollama 0.34.0; 3 relances em `maquina.json` = 1 por modelo, não interrupções. Commits: `6a4381f` (13/09, código + documentação) e `b9f9ad9` (15/09, só resultados: 732 arquivos).
- **Resultados** em `Programacao/AgenteCore/experimentos/resultados_alvo/fase3/`: `avaliacao_fase3.json` (1.440 registros), `resumo_fase3.json` (13 seções), `comparacao_fases.json/.md` (29 pareamentos), `relatorio_fase3.html`, gráficos 12–17 em `resultados_alvo/graficos/`, `revisao_edicoes__*.md` (3 planilhas, 63 linhas, **nenhuma avaliada**), `fase3.log` (fora do git até o `git add -f`).
- **Ollama passou a 0.34.1** depois da bateria: qualquer inferência nova precisa da ponte de versão (abaixo).

## 2. Números que mandam na leitura (copiados de `resumo_fase3.json` / `comparacao_fases.md`)

| Modelo | acerto / acurácia balanceada nos 90 (L0 → melhor L → L3) | nos 36 de avaliação (L0 → melhor) | edições aceitas | s/caso (L3, mediana) |
|---|---|---|---|---|
| granite4.2:8b | 76,7/79,6 → 77,8/80,2 (L1) → 75,6/78,7 | 80,6/83,3 → igual em todas (hash idêntico nas 4 épocas) | **0** de 181 propostas (133 `texto_longo`) | 132,6 |
| qwen2.5:7b | 71,1/75,7 → **76,7/83,0 (L1)** → 77,8/80,7 | 77,8/81,2 → **88,9/91,7 (L1)** | 61 (40/12/9); 9 verbetes novos; biblioteca 6.582 → 11.377 tokens | 47,0 |
| qwen2.5-coder:7b | 71,1/75,8 → 74,4/78,9 (L1) → 72,2/75,4 | 75,0/80,0 → 77,8/84,2 (L3) | 39 | 49,8 |
| qwen2.5-coder:3b | 65,6/71,5 → 67,8/72,6 (L3) | 69,4/68,8 → 72,2/71,2 (L2) | 10 (omite TEXTO em 29–32 propostas por época) | 18,4 |

- Nenhum McNemar com p < 0,05 (menor: qwen2.5:7b L3 × L0 nos 90, +6,7 pp, b = 8, c = 2, p = 0,1094; nos 36 L1 +11,1 pp, b = 4, c = 0, p = 0,125). Efeito mínimo detectável: 19,4 pp nos 36, 16,7 nos 54, 11,1 nos 90. Cochran Q nunca significativo.
- Autoenvenenamento máximo nos 36: 5,6% (H5 ok); pico 9,3% (coder:7b L2→L3 nos 54). `tentativas_de_decorar` = 0. Rejeições das épocas 2–3 dominadas por `duplicada` e `teto_notas_verbete` (saturação). `ouro_deslocado_por_novo` = 0; MRR nos 90 cai de 0,596 para 0,591/0,589/0,579 em quem editou.
- Reprodutibilidade 2B_A2 × F3_L0: b = c = 0 em 7 dos 8 pareamentos, apesar de Ollama 0.33.3 → 0.34.0.
- Vereditos prováveis (a fechar na análise): H1 não (limite de amostra), H2 não, H3 invertido, H4 parcial, H5 sim, H6 sim (L1 melhor em 3 de 4 pela acurácia balanceada).

## 3. Pesquisa bibliográfica (rodada 2)

Rodada 1 integrada (§6.9.1–6.9.8; 154 aprovadas/12 rejeitadas; 175 referências). Rodada 2 (Workflow `wf_add7e8f0-e81`) caiu 3 vezes por limite de sessão; a crítica trocou a lista de lacunas a cada execução; valeu a lista de 13/09 com 8 lacunas: 1 completa (agente autônomo de QA), 3 verificadas sem síntese (conflito contexto × conhecimento; validação de artefatos gerados; prompting em estágios em modelos pequenos), 3 pesquisadas sem verificação (métricas de qualidade de documentação; aprender sem atualizar pesos/Faceli; taxonomia e rótulos-ouro), 1 sem pesquisa (recuperação em corpus pequeno e crescente); mapa de decisões nulo. Artefatos: `…\5c1c8fa0-31ce-4489-b7e9-314bf40961a1\workflows\wf_add7e8f0-e81.json` (`result.topicos`, 15 entradas) e o diário `…\subagents\workflows\wf_add7e8f0-e81\journal.jsonl`. **Não retomar o Workflow antigo** (reaproveitou 2,5% e 8,3% do cache; rerodaria ~300 agentes): o plano manda um Workflow novo e curto com os artefatos como entrada fixa.

## 4. O plano complementar de 21/09 (aprovado) — pacotes e estado

| Pacote | O quê | Estado em 21/09 |
|---|---|---|
| P4-lite | economia de tokens: `.gitignore` estreitado, `.claude/{settings.json,rules/,skills/}` versionados, hook `ferramentas/gancho_pre_bash.py` → `resumir_saida.py`, `medir_tokens.py`, CLAUDE.md "Economia de tokens", plugin explanatory desligado no projeto, 5 skills copiadas (mattpocock/skills, commit c55ee460) | feito na S1 (`claude update` falhou sem npm — pendência do Eric); `ferramentas/conferir_docs.py` criado |
| P0 | registro da bateria, cabeçalhos de estado, pendências, este handoff | feito na S1 |
| P3.1 | `executar_fase3b.py`, `avaliar_fase3b.py`, `rodar_fase3b.ps1`, `testar_fase3b.py` + **ponte de versão** (`-Modo ponte`, 144 inferências, ~2,5 h, durante o dia) | entregue na S1 (9 testes; execução real de 2 casos); revisão Sonnet em andamento; **ponte lançada às 15:15 de 21/09** (`resultados_alvo/fase3b_ponte/`, ~33 s por diagnóstico no 3b) |
| P1 | Workflow `pesquisa-r2` (≈ 85 agentes; verificadores em Sonnet) → `render_levantamento.py` → §6.9.9–6.9.17, `referencias.md`, `mapa-de-decisoes-fase-3.md` (§6.10) | **feito na S1**: Workflow `pesquisa-r2` 82/82 (2 execuções), integração por `extrair_pesquisa.py` + `integrar_pesquisa.py` (§6.9.9–6.9.17, mapa §6.10, 103 referências novas, contagens da rodada 1 corrigidas para 154/2/3), revisão Sonnet aplicada (TAM et al. conferido na fonte); `render_levantamento.py --check` 16/16 |
| P2 | `decidir_modelo.py` (regra da decisão 36 primeiro; bootstrap, P(top-1), Pareto, sensibilidade) → relatórios §1–§12, comparação §3–§6, vereditos H1–H6, achados 4.30+, `analise-decisoria-modelo-final.md` | script em implementação (Sonnet, S1, brief `brief-p2-decidir-modelo.md`); texto S4 |
| P3 menu | Fase 3-B: (a) 36 casos inéditos × L0/L1/L3, (b) troca cruzada das bibliotecas do qwen2.5:7b, (d) granite com `TEXTO_MAX` 600, (c) A5 opcional; (e) réplicas descartadas | Eric escolhe depois de P2 |
| P5 | Workflow `pesquisa-llms-locais` (8 tópicos), `cache_respostas.py` (cache exato, fora de corrida medida), veredito dos 2 repositórios para as LLMs locais | S5 |
| P4 | plugins `pyright-lsp`/`php-lsp`; codebase-memory-mcp **com salvaguardas** (backup do PATH, npm, escopo projeto, cópia descartável, regra de permanência ≥ 20% de economia); levantamento de addons; `ferramental-do-claude-code.md` | documento escrito na S1 (avaliação das 26 skills, candidatos, medição-antes); instalações, levantamento aprofundado e medição-depois na S6 |
| P6 | Memorial (índice, `5-metodo-e-ferramental/`), decisões 45+, histórico, pendências, README, `conferir_docs.py`, handoff final | parcialmente na S1: índice com seção 5 e §6.10, decisões 45–51, histórico com b067d87/6a4381f/b9f9ad9, pendências atualizadas, `conferir_docs.py`; faltam README e handoff final |

Decisões do Eric em 21/09: instalar o codebase-memory-mcp com salvaguardas; copiar 5 skills; análise antes de testes novos (nome Fase 3-B; Fase 4 continua = interceptador Playwright); processo enxuto; `.gitignore` estreitado; ponte durante o dia; versionar os logs com `git add -f`; desligar o plugin explicativo.

## 5. Regras que valem sempre

Nunca commitar (o Eric commita; `git add` também é dele); tag `! Alteração de IA - Revisar` + `! Motivo:`; `.ps1` com BOM e sem travessão; nada em `base_conhecimento/`; `executar_fase3.py`, `estrategias.py` e `evolucao_biblioteca.py` intocados; nenhum número à mão em Markdown; um modelo residente, `num_gpu=0`, `num_ctx=8192`; perguntar antes de baterias longas; economia de tokens (CLAUDE.md, seção nova): primeiro a máquina, depois o modelo.
