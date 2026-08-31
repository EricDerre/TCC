# ! Alteração de IA - Revisar
# Bootstrap fino (Windows) para run.py.
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
