# ! Alteração de IA - Revisar: bootstrap fino (Windows) que só garante a existência de
# um Python 3 e então delega toda a instalação para install.py.
# ! Motivo: resolve o ovo-e-galinha do instalador - install.py concentra a lógica real,
# mas precisa de um Python que pode não existir na máquina de quem clonou. Manter aqui
# apenas essa checagem evita reescrever a mesma lógica de instalação em PowerShell, Bash
# e Python; quando ela muda, muda num lugar só.
# ! Alteração de IA - Revisar: gravado em UTF-8 com BOM e travessão do comentário trocado por hífen (29/09/2026, ficha 9 de pendencias.md, decidida pelo Eric).
# ! Motivo: regra do CLAUDE.md para .ps1 - sem BOM o Windows PowerShell 5.1 lê o arquivo na codepage ANSI, e um travessão
# dentro de uma string encerraria a string no meio; aqui ele estava só em comentário (parse conferido em 21/09/2026),
# então a troca é por consistência e para silenciar o aviso de ferramentas/conferir_docs.py.
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

# ! Alteração de IA - Revisar: (25/11/2026, consertos da primeira execução do Actions) a última chamada passa os argumentos (`@args`) ao install.py e o script termina com `exit $LASTEXITCODE`.
# ! Motivo: execução 45650086543 do GitHub Actions, célula CI-WIN: o install.py parou em "Não foi possível subir o MariaDB" e mesmo assim `powershell -File install.ps1` saiu com código 0, porque o script não devolvia o código do Python; e `install.cmd --conferir` não chegava ao install.py, porque os argumentos não eram repassados.
& $py (Join-Path $PSScriptRoot "install.py") @args
exit $LASTEXITCODE
