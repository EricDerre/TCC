# ! Alteração de IA - Revisar: bootstrap fino (Windows) que só garante a existência de
# um Python 3 e então delega toda a instalação para install.py.
# ! Motivo: resolve o ovo-e-galinha do instalador — install.py concentra a lógica real,
# mas precisa de um Python que pode não existir na máquina de quem clonou. Manter aqui
# apenas essa checagem evita reescrever a mesma lógica de instalação em PowerShell, Bash
# e Python; quando ela muda, muda num lugar só.
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
