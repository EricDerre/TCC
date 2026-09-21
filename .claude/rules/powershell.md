---
paths:
  - "**/*.ps1"
---
<!-- ! Alteração de IA - Revisar: regra carregada só ao editar .ps1 (21/09/2026).
     ! Motivo: tirar do CLAUDE.md o detalhe que só importa em PowerShell (economia de contexto por turno) sem perder a regra. -->
# PowerShell (.ps1)
- Gravar sempre em UTF-8 **com BOM** (primeiros bytes EF BB BF) e usar `-` no lugar do travessão `—` nas strings: o Windows PowerShell 5.1 lê `.ps1` sem BOM na codepage ANSI e o travessão vira `â€”`, encerrando a string.
- Conferir depois de gravar: `powershell -NoProfile -Command "[System.IO.File]::ReadAllBytes('arquivo.ps1')[0..2]"` e `[scriptblock]::Create((Get-Content -Raw arquivo.ps1))`.
- `Tee-Object` grava UTF-16 no PowerShell 5.1: usar `ForEach-Object` + `Add-Content -Encoding utf8` (como em `rodar_fase3.ps1`).
- `$env:PYTHONUNBUFFERED = "1"` e `[Console]::OutputEncoding` UTF-8 antes de chamar Python quando a saída vai para log.
- Tag `# ! Alteração de IA - Revisar: …` + `# ! Motivo: …` em todo trecho tocado.
