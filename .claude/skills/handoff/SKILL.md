---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---
<!-- ! Alteração de IA - Revisar: copiado em 21/09/2026 de https://github.com/mattpocock/skills (skills/productivity/handoff/SKILL.md, commit c55ee46073ed, licença MIT, Copyright (c) 2026 Matt Pocock), sem alteração no conteúdo.
     ! Motivo: decisão do Eric (21/09/2026) de adotar 5 skills desta coleção copiando os arquivos para o projeto em vez de instalar o plugin com as 26 (5 delas repetem o superpowers e as 26 dobrariam o custo fixo de contexto por turno); a origem e o commit ficam aqui para atualização e atribuição. -->

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
