<!-- ! Alteração de IA - Revisar: handoff da sessão 3 do plano complementar (23/09/2026): decisões do Eric (3-B, revisão, cópia L1, commit), diagnóstico do servidor MCP, correções de fato (licença do 3B, listas do .ps1), limpeza dos outros modelos, casos inéditos, revisão do projeto ABNT e as doze decisões que ficaram para o Eric responder.
     ! Motivo: o Eric vai arquitetar um novo plano depois de responder às pendências; a próxima sessão precisa achar num só lugar o que foi fechado, o que depende dele e os comandos certos da 3-B (os anteriores falhavam na vinculação de parâmetros do PowerShell). -->
# Handoff — 23/09/2026: pontas soltas fechadas antes do novo plano

Continua os handoffs de [21/09](2026-09-21-fase-3-concluida-e-plano-complementar.md) e [22/09](2026-09-22-decisao-do-modelo-e-analise.md). Livro-razão: `.superpowers/sdd/fase3b-e-fechamento/progress.md` (fora do git). Plano complementar: `~/.claude/plans/delegated-hopping-steele.md` — o que falta dele está na seção "Plano complementar" abaixo.

## O que o Eric decidiu em 23/09

| Item | Decisão |
|---|---|
| Testes da 3-B | O recomendado: (b) troca cruzada, depois (a) casos inéditos (decisão 56) |
| Revisão das 63 edições | Vereditos da primeira passada por IA aceitos como estão |
| Cópia L1 | "Está ok" — falta dizer se fica como está ou se a IA faz a primeira passada das 30 edições restantes (pergunta 2 das pendências) |
| Commit | `f86e65d` (22/09) contém tudo da sessão 2; os dois logs continuam fora do git |
| Outros modelos | "Limpa": ficam só resultados, gráficos e o veredito por modelo; a remoção dos pesos no Ollama aguarda confirmação (pergunta 3) |

## O que mudou em 23/09

| Item | Estado |
|---|---|
| **Servidor MCP `codebase-memory`** | **Não subiu**: `claude mcp list` (binário nativo 2.1.278 da extensão) = "Pending approval"; `~/.claude.json` com `enabledMcpjsonServers: []` e `hasTrustDialogAccepted: false`. Depende de o Eric aprovar (`/mcp`) ou de `enableAllProjectMcpServers: true`. `pyright-lsp` também não instalou (não consta em `installed_plugins.json`). Atalho do npm continua quebrado (`@anthropic-ai/claude-code@2.1.245` sem o `.exe`). Registrado em `ferramental-do-claude-code.md` §7.2 e §7.6 |
| **`rodar_fase3b.ps1`** | Pelo `-File` do Windows PowerShell 5.1, `-Modelos a,b` chegava como UMA string e `-Versoes 1,3` (em `[int[]]`) virava 13; `a b` vinculava só o primeiro. O script agora divide as duas listas por vírgula (`[string[]]$Versoes` + `[int]`); testado com o bloco copiado. A ponte de 21/09 não sofreu (usou os modelos padrão) |
| **Licença do `qwen2.5-coder:3b`** | Qwen Research License (model card no Hugging Face: "qwen-research"), não Apache-2.0. `LICENCAS`/`ORDEM_LICENCA` corrigidos em `decidir_modelo.py`; a frase da seção 1 do `decisao_modelo.md` lista as licenças do JSON; `decisao_modelo.*` e `tabelas_relatorio.md` regenerados; ranking inalterado; `--check` limpos (decisão 57) |
| **Limpeza dos modelos** | `install.py` baixa `qwen2.5:7b` por padrão (`COBAIA_MODELO_LLM` continua mandando); veredito por modelo em `analise-decisoria-modelo-final.md` §8.1 (Granite, Coder 7B, 3B, e phi4-mini/1.5b da 2-B); README com a linha obsoleta da bateria corrigida e os testes escolhidos. Scripts congelados e `resultados_alvo/` intocados |
| **Casos inéditos** | `banco_casos_ineditos.py` escrito por agente Sonnet sob a regra de leitura só do cobaia (36 casos, ids 16–21 por classe, 2 por célula, cada um com `fonte:` arquivo:linha). Gate mecânico limpo (contagens, `validar_caso`, ids, nenhum repetido dos 90, nenhuma sobreposição de 5-gramas com L0 e com L1/L3 do `qwen2.5:7b` e do 3B); fatos de código conferidos pelo controlador (`_MALFORMED_BODY`, `formatarPreco`, heading `<h3>`, ramo da lista vazia, seed 8/9/13, enum de status, `_to_dict`); teste de fumaça do modo `ineditos` numa cópia temporária (1 diagnóstico do 3B em 41 s, avaliado; pasta oficial intocada). `testar_fase3b.py`: o teste de ausência do módulo passou a simular a ausência e ganhou um teste positivo dos 36. O Eric confere `lex-16`, `sin-20`, `semt-18`, `tra-19`, `run-20`, `efe-20`. Achado do agente: `efe-3` e `efe-10` dos 90 descrevem sintomas que o código não produz (pendência 13) |
| **Regeneração de `resumo_fase3.json`** | Ensaio numa cópia (`scratchpad/dryrun`): só `resumo_fase3.json` mudaria (`metadados.gerado_em` + `revisao_humana`, 7 blocos modelo × operação); `avaliacao_fase3.json` idêntico. Aguarda o "pode gravar" (pergunta 1) |
| **Projeto ABNT** | Revisão ponto a ponto contra o que foi feito em `4-projeto-de-pesquisa-abnt/correcoes-aplicadas.md` §5.1: 7 pontos que batem, 11 modificações propostas (modelo Qwen2.5 em vez de Coder, critério da decisão 36, linha da Fase 3, sequência das fases, revisão por IA, fuzzing × injeção determinística, reprodutibilidade, 5 referências com URL, Faceli, referencial do TCC final, marcações/PDF) e a posição no cronograma (fim do Mês 2; Fases 4 e 5 = Meses 3–5, não iniciadas). Nada aplicado ao documento |
| **Referências sem URL** | JÚNIOR (SOL SBC 37006; arXiv 2510.01024), SHI (arXiv 2509.20552), ZHANG J. (AAAI 40(41) 34710–34718; arXiv 2511.21398), BISWAS (só ResearchGate 399515915), MACIAK (Medium assinado "InstaTunnel" — autoria a confirmar) |
| **Documentação** | decisões 56–57; pendências (fechamentos + bloco "Abertas em 23/09/2026" com as 12 perguntas); histórico (`f86e65d` + linha de 23/09); Memorial até 23/09; `conferir_docs.py` "tudo ok" |

## Plano complementar — o que falta dele

- **P3.6** `banco_casos_ineditos.py`: feito nesta sessão; falta o Eric conferir 6 casos e a corrida (a).
- **P3 menu**: (b) cruzada e (a) inéditos escolhidos, não rodados; (c) só se sobrar máquina; (d) inviável; (e) descartado.
- **P4 regra de permanência do MCP**: bloqueada até o servidor ser aprovado.
- **P6 integração da 3-B** (relatório §11/§12, análise §10 e §9, `--saidas-3b`, tabelas, handoff final): quando (b) e (a) rodarem.
- Tudo o mais (P0, P4-lite, P1, P2, P3.1–3.5, P4 instalação/levantamento/medição, P5, P6 documentação) está feito; o script do Workflow P5 foi copiado para `.superpowers/sdd/fase3b-e-fechamento/pesquisa-llms-locais.js`.

## Comandos da 3-B (listas por vírgula)

```
# troca cruzada (144 inferências, ~2,5 h; espera 6,5 GB de RAM livre para o Coder 7B)
powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo cruzada -Saida fase3b_cruzada_qwen -Doador qwen2.5:7b -Versoes 1,3 -Modelos qwen2.5-coder:7b,qwen2.5-coder:3b
# casos inéditos (216 inferências, ~3 h), depois da conferência dos 6 casos
powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo ineditos -Saida fase3b_ineditos -Versoes 0,1,3 -Modelos qwen2.5:7b,qwen2.5-coder:3b
# integração (cruzada) e conferências
RESULTADOS_DIR=resultados_alvo python decidir_modelo.py --saida fase3 --saidas-3b fase3b_ponte fase3b_cruzada_qwen [--check]
RESULTADOS_DIR=resultados_alvo python gerar_tabelas_relatorio_fase3.py --saida fase3 [--check]
python ferramentas/conferir_docs.py
```

## O que falta (ordem)

1. **Eric** responde às 12 perguntas do bloco de 23/09 em `pendencias.md` (regeneração, cópia L1, Ollama, lançamento da cruzada, MCP/pyright, atalho npm, logs, `Tee-Object`, BOM dos três `.ps1`, ABNT item a item, pendências antigas, 6 casos inéditos).
2. Rodar (b) numa noite; conferir os 6 casos; rodar (a).
3. P6: integrar a 3-B, regerar tabelas, handoff final, memória.
4. Novo plano do Eric (Fase 4: interceptador Playwright, poda da árvore de acessibilidade, cura de seletor; ferramental adotado na decisão 55).
