<!-- ! Alteração de IA - Revisar: handoff da sessão de 28/09/2026: correção dos casos efe-3/efe-10, sonda de detecção de correção (resultado negativo), painel interativo e roadmap.
     ! Motivo: o Eric vai arquitetar o novo plano a partir do roadmap; a próxima sessão precisa saber o que a sonda mostrou e o que o painel e o roadmap são, sem reler o chat. Continua o handoff de 23/09. -->
# Handoff — 28/09/2026: correção dos casos, sonda, painel e roadmap

Continua o handoff de [23/09](2026-09-23-pontas-soltas-e-3b.md) (as 13 perguntas de lá continuam abertas, menos a 13). Livro-razão: `.superpowers/sdd/fase3b-e-fechamento/progress.md`.

| Item | Estado |
|---|---|
| **Casos `efe-3` e `efe-10`** | Corrigidos em `banco_casos.py` / `banco_casos_extra.py` (achado 4.36, decisão 58): `efe-3` = cartão sem foto (estava nos 36 de avaliação: 1 caso não pareável byte a byte com a Fase 3 nas corridas futuras); `efe-10` = tela com preço antigo enquanto a API já devolve o novo (nos 54 de aprendizado). Testes 60/19 ok, `validar_banco.py` limpo, gate dos inéditos limpo. Registros da Fase 3 intocados |
| **Sonda de detecção de correção** | `sonda_correcao.py` (novo): época de aprendizado do executor oficial sobre cópia da L1 do `qwen2.5:7b`, só com os dois casos corrigidos; saída `resultados_alvo/fase3b_correcao/` (epoca-2 hash 1202f1be9a75). Resultado: o modelo **não percebe** a correção — repete as edições da época 1 (barradas por teto/duplicidade), erra o `efe-10` (`dado_desatualizado`) e emplaca um verbete genérico. Leitura e consequências em `roadmap.md` §3 e §4.2 |
| **Painel interativo** | `ferramentas/gerar_dashboard.py` → `Documentacao/dashboard/dashboard-fase3.html` (HTML único, 2 MB: 11 gráficos Chart.js, 27 tabelas dos blocos oficiais, 18 figuras embutidas, veredito por modelo, hipóteses H1–H6, método e limites; `--check`). Publicado como artefato privado do Eric em https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN (republicar pelo mesmo caminho depois da 3-B) |
| **Roadmap** | `Documentacao/memorial/roadmap.md`: estado por fase, corridas pendentes com comando/duração/o que fecha, esqueleto das Fases 4 e 5 (com o requisito do ciclo de correção) e a tabela para os pontos do Eric |
| **Documentação** | decisão 58; achado 4.36; pendências (13 fechada; 14 nova); histórico (linha de 28/09); Memorial (índice: painel e roadmap; período até 28/09); README (ferramentas e 3-B). `conferir_docs.py` limpo |
| **Lição de ferramenta** | O hook `gancho_pre_bash.py` reescreve comandos que contêm `testar_fase3*`/`avaliar_fase3*`/`rodar_*`: um heredoc no mesmo comando quebra (erro de sintaxe antes de executar) — rodar testes e heredocs em chamadas separadas |

## O que falta (ordem)
1. Eric responde às perguntas 1–12 (23/09) e 14 (28/09) em `pendencias.md` e encaixa os pontos dele no roadmap §7.
2. Corridas: cruzada (noite), conferência dos 6 inéditos, inéditos (noite), regeneração combinada; ver roadmap §2.
3. Novo plano (Fase 4) a partir do roadmap §4.
