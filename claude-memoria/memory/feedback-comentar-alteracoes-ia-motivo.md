---
name: feedback-comentar-alteracoes-ia-motivo
description: "Toda alteração de código por IA leva, junto à tag \"! Alteração de IA - Revisar\", comentário com O QUE foi feito e o MOTIVO"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f03b12ad-c757-4edb-aaa2-0cb57f2610aa
  modified: 2026-09-01T10:45:20.511Z
---

Em QUALQUER alteração de código feita por IA, a marca `! Alteração de IA - Revisar` **nunca fica sozinha**: sempre acompanhada de comentário explicando **o que foi feito** e **o motivo**, em linguagem técnica mas amarrada à regra de negócio e ao comportamento anterior do código (citar a função/fluxo afetado, o defeito/sintoma que motivou, e por que a forma escolhida é segura).

**Why:** Eric revisa e mantém essas alterações depois, e commita ele mesmo — o revisor precisa entender o contexto sem reabrir a investigação. Ver [[feedback-eric-nunca-commitar]].

**How to apply:**
- Formato: primeira linha `! Alteração de IA - Revisar: <o que foi feito>`, seguida de `! Motivo: <sintoma/defeito anterior e por que a mudança resolve>`, no mesmo nível de indentação do bloco alterado.
- Sintaxe por linguagem: `#` (Python/shell/PowerShell/YAML), `//` (PHP/JS), `--` (SQL), `<!-- -->` (HTML/Markdown), `rem` (batch). Em Python, docstring de módulo logo abaixo da tag também vale.
- **Sem jargão teórico** — descrever pelo processo real, não pelo conceito: "marca os itens do pedido originador como pendentes de transferência (situacao 'AB' -> 'PE')" em vez de "claim atômico". Nada de "guard-rail", "last writer wins", "snapshot", "race condition".
- **Códigos de situação/domínio sempre com o significado junto**, na primeira menção de cada bloco: 'AB' (em aberto), 'PE' (pendente de transferência), 'CA' (cancelado), 'FA' (faturado), 'FE' (transferência efetivada). Vale para comentários, mensagens, relatórios e resumos.
- **Não usar código de cadastro do cliente como terminologia** (ex.: "TC"): escrever o nome real ("pedido de transferência de estoque"); o código só como referência literal entre aspas.
- O comentário deve fazer sentido lido isolado no código, sem depender do chat (mas pode citar funções, tabelas, telas e mensagens de erro reais).
- Vale para código novo, linhas alteradas e variáveis/declarações acrescentadas.
- Arquivo vazio de propósito (ex.: `__init__.py` de 0 byte) **não** recebe tag — marcar quebraria a vazidade.

**Escopo por projeto (importante):**
- O **princípio do comentário acima vale em todos os projetos**.
- Já a convenção de **nomes** que acompanha esta regra — CamelCase com prefixo húngaro (`nuLinhasReservadas`, `strComando`, `booCancPedTransf`, `FunEstornaReservaTransf`) e os códigos de domínio ('AB'/'PE'/'TC', pedido de transferência, ARZ) — é **específica do ERP**, de onde a regra veio.
- No **TCC (Agente de QA E2E)** isso não se aplica: Python segue PEP8 snake_case (ruff configurado) e PHP segue o padrão do código legado. Decidido explicitamente com o Eric. Ver [[project-tcc-agente-qa-decisoes]].
