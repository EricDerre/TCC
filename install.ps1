# ! Alteração de IA - Revisar
# Bootstrap fino (Windows): garante que existe Python 3, depois delega tudo pra install.py.
$ErrorActionPreference = "Stop"

function Get-PythonCmd {
    foreach ($cmd in @("python", "python3", "py")) {
        if (Get-Command $cmd -ErrorAction SilentlyContinue) { return $cmd }
    }
    return $null
}

$py = Get-PythonCmd
if (-not $py) {
    Write-Host "[install.ps1] Python não encontrado -- instalando via winget..."
    winget install --id Python.Python.3.14 -e --accept-package-agreements --accept-source-agreements
    $py = Get-PythonCmd
    if (-not $py) {
        Write-Host "[install.ps1] Python foi instalado mas ainda nao aparece nesta sessao do terminal."
        Write-Host "[install.ps1] Feche e reabra o terminal e rode .\install.ps1 de novo."
        exit 1
    }
}

& $py (Join-Path $PSScriptRoot "install.py")
