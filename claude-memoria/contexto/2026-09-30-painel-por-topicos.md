<!-- ! Alteração de IA - Revisar: handoff da sessão de 30/09/2026 — o painel do projeto virou o compilador das análises (abas por tópico).
     ! Motivo: a próxima sessão precisa saber como acrescentar uma aba nova e o que ainda depende do Eric, sem reler o chat. Continua o handoff de 29/09. -->
# Handoff — 30/09/2026: painel como compilador das análises

Continua o handoff de [29/09](2026-09-29-decisoes-e-frentes.md). Livro-razão: `.superpowers/sdd/fase3b-e-fechamento/progress.md`.

| Frente | Estado |
|---|---|
| **Pedido do Eric** | "Coloca no painel a aba do comparativo do qwen 2.5 7b e o coder" e "vamos fazer esse painel ser o grande compilador / centralizador das análises e dados, com cada aba específica falando sobre os tópicos ... sumarizado e focando no visual" (decisão 64) |
| **O que foi feito** | `ferramentas/painel_topicos.py` (novo): `NAV` (cinco grupos, 18 abas, uma linha de descrição cada — alimenta a barra e o mapa do painel), `SLOTS` (cor de cada modelo na paleta validada), sete `secao_*` (qwen × Coder, Fase 3-B, curadoria da L1, recuperador, ablação, pesquisa, ferramental), `JS_TOPICOS`/`DESENHAR_TOPICOS`/`SELETORES_TOPICOS`/`CSS_TOPICOS`, `montar(ctx)`. `gerar_dashboard.py`: tokens `--s1..--s8` (claro e escuro), `cor(m)` lê o token, `MAPA_DESENHO`/`SELETORES` gerados, filtro genérico de tabela (`.filtro-tabela`), redesenho ao trocar o tema, `cartoes_corridas(road, numeros, sufixo)`, mapa do painel na aba Início, `scroll-margin-top` + rolagem para o topo no link direto. Testes: `testar_painel_topicos.py` (8) e `testar_painel_textos.py` (12). Cópia versionada da medição do MCP em `5-metodo-e-ferramental/dados/` |
| **Padrão de uma aba** | Pergunta no `h1`; resposta em uma frase (`p.lead`, com os números lidos do JSON); `kpis` (5 ou 6 cartões — 7 deixa um sozinho na segunda linha); um ou dois `<div class="chart">` com função em `JS_TOPICOS`; tabelas de duelo/heat; `leitura` (3 itens); `fontes`. Tabelas completas em `detalhes`. Nada digitado à mão |
| **Como conferir** | `python ferramentas/gerar_dashboard.py` e `--check`; captura com o Edge sem janela: `msedge --headless=new --screenshot=x.png --window-size=1300,2400 --virtual-time-budget=8000 file:///.../painel-do-projeto.html#<aba>` (o headless renderiza no tema escuro) |
| **Lições** | A coluna Veredito do mapa da rodada 4 vem em negrito (`**adotado**`): limpar `*` antes de classificar; a paleta antiga reprovava no validador da regra de gráficos (`node .../dataviz/scripts/validate_palette.js`), a de referência passa nos dois temas; `getComputedStyle` no `documentElement` lê os tokens do tema ativo; a rolagem para a âncora do `#hash` esconde o topo da seção sob o cabeçalho fixo |

## O que falta (ordem)
1. Eric: troca cruzada à noite (corrida 1); conferir a planilha de curadoria; ler o comparativo (agora também na aba qwen × Coder) e liberar os itens 1–2 do ABNT; Faceli no exemplar (11e); decidir a ficha 16; commit (`git add -A` pega tudo).
2. Depois da cruzada: integração da 3-B (corrida 6) e a aba Fase 3-B ganha o resultado (mesma função `secao_tres_b`, ler `fase3b_cruzada_qwen`).
3. Toda análise nova: aba em `painel_topicos.py` (regra em `.claude/rules/documentacao.md`), regerar, testar, republicar em https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN.
