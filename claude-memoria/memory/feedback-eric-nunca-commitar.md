---
name: feedback-eric-nunca-commitar
description: Nunca commitar por conta própria nem usar comando git destrutivo sem confirmação — Eric commita ele mesmo
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f03b12ad-c757-4edb-aaa2-0cb57f2610aa
  modified: 2026-09-01T10:45:27.556Z
---

Nunca fazer commit por conta própria: as alterações ficam no working tree e o Eric revisa e commita ele mesmo. Nunca usar `git push --force`, `git reset --hard` ou outro comando destrutivo sem confirmação explícita.

**Why:** Ele é quem assina e revisa o que entra no histórico — commits automáticos tiram dele a revisão, e comando destrutivo pode apagar trabalho que ainda não foi revisado.

**How to apply:**
- Terminar a tarefa deixando tudo no working tree e dizer claramente o que mudou.
- Operações que só mexem no índice (`git rm --cached`, `git add`) também preparam o commit dele — oferecer e explicar em vez de executar por conta própria.
- Antes de qualquer comando que possa descartar trabalho, rodar `git status` e avisar.
- Relacionado: [[feedback-comentar-alteracoes-ia-motivo]] (o comentário existe justamente para essa revisão).
