# ! Alteração de IA - Revisar: bootstrap fino (Windows) que localiza o Python e chama
# run.py, sem nenhuma lógica de subida de serviço aqui.
# ! Motivo: run.py precisa gerenciar três processos (MariaDB, php -S e uvicorn) e
# encerrá-los juntos no Ctrl+C - controlar isso em PowerShell e em Bash separadamente
# duplicaria a parte mais frágil do projeto. O shell fica só como porta de entrada.
# ! Alteração de IA - Revisar: gravado em UTF-8 com BOM e travessão do comentário trocado por hífen (29/09/2026, ficha 9 de pendencias.md, decidida pelo Eric).
# ! Motivo: regra do CLAUDE.md para .ps1 - sem BOM o Windows PowerShell 5.1 lê o arquivo na codepage ANSI, e um travessão
# dentro de uma string encerraria a string no meio; aqui ele estava só em comentário (parse conferido em 21/09/2026),
# então a troca é por consistência e para silenciar o aviso de ferramentas/conferir_docs.py.
$ErrorActionPreference = "Stop"

$py = $null
foreach ($cmd in @("python", "python3", "py")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) { $py = $cmd; break }
}
if (-not $py) {
    Write-Host "[run.ps1] Python não encontrado. Rode .\install.ps1 primeiro."
    exit 1
}

& $py (Join-Path $PSScriptRoot "run.py")
