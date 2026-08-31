# ! Alteração de IA - Revisar
# Recompila Cobaia.exe a partir de Cobaia.py (+ install.py/run.py/_env_common.py).
# Rode de novo sempre que qualquer um desses arquivos mudar -- o Cobaia.exe
# nao se autoatualiza.
$ErrorActionPreference = "Stop"

$buildVenv = Join-Path $env:TEMP "cobaia-build-venv"
if (-not (Test-Path $buildVenv)) {
    python -m venv $buildVenv
}
& "$buildVenv\Scripts\python.exe" -m pip install --quiet --upgrade pyinstaller

& "$buildVenv\Scripts\python.exe" -m PyInstaller `
    --onefile --console --name Cobaia `
    --distpath $PSScriptRoot --workpath (Join-Path $env:TEMP "cobaia-build") --specpath $PSScriptRoot `
    --noconfirm `
    (Join-Path $PSScriptRoot "Cobaia.py")

Write-Host ""
Write-Host "Cobaia.exe atualizado em $PSScriptRoot"
