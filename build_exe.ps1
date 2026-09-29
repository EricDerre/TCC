# ! Alteração de IA - Revisar: recompila Cobaia.exe a partir de Cobaia.py (+ install.py/run.py/_env_common.py).
# ! Motivo: o Cobaia.exe não se autoatualiza - rode de novo sempre que qualquer um desses arquivos mudar.
# ! Alteração de IA - Revisar: gravado em UTF-8 com BOM (29/09/2026, ficha 9 de pendencias.md, decidida pelo Eric).
# ! Motivo: regra do CLAUDE.md para .ps1 - sem BOM o Windows PowerShell 5.1 lê o arquivo na codepage ANSI, e um travessão
# dentro de uma string encerraria a string no meio; aqui ele estava só em comentário (parse conferido em 21/09/2026),
# então a troca é por consistência e para silenciar o aviso de ferramentas/conferir_docs.py.
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
