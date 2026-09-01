# ! Alteração de IA - Revisar: bootstrap fino (Windows) que localiza o Python e chama
# run.py, sem nenhuma lógica de subida de serviço aqui.
# ! Motivo: run.py precisa gerenciar três processos (MariaDB, php -S e uvicorn) e
# encerrá-los juntos no Ctrl+C — controlar isso em PowerShell e em Bash separadamente
# duplicaria a parte mais frágil do projeto. O shell fica só como porta de entrada.
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
