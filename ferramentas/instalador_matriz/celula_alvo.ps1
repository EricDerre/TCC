# ! Alteração de IA - Revisar: arquivo novo (19/11/2026, pacote I3 do instalador único): a célula ALVO da matriz de testes. Na
# máquina-alvo, como ela está, restaura o banco das cobaias ao seed (restaurar_banco.py), roda a prova da instalação
# (instalador/conferir.py) e grava a evidência em dados/instalador/celulas/ALVO/<data-hora>/, com o celula.json.
# ! Motivo: o plano aprovado (seção 4.1) pede a prova rodada numa máquina boa, para mostrar que ela acerta onde a instalação
# funciona, e o pacote I3 (seção 5) pede essa célula depois de _env_common.py, install.py e run.py mudarem: é a conferência de
# que os três arquivos seguem subindo o banco, o site e a API no Windows da máquina-alvo. O roteiro do WSL não serve aqui,
# porque cria uma instância de Linux. Este roteiro não instala nada (não chama o instalador nem baixa programa) e, com o modelo
# pequeno padrão, não baixa modelo: o qwen2.5:0.5b-instruct já está no disco desta máquina, e a prova só baixa modelo que falta.
# Roda na janela do PowerShell do Eric, nunca de dentro do aplicativo Claude, e recusa se houver corrida rodando.
param(
    [ValidateSet("N1", "N2", "N3", "N4")][string]$Ate = "N4",
    [string]$ModeloPequeno = "qwen2.5:0.5b-instruct",
    [switch]$Simular
)
$ErrorActionPreference = "Stop"

$Id = "ALVO"
$Raiz = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Carimbo = Get-Date -Format "yyyyMMdd-HHmmss"
$Evidencia = Join-Path $Raiz "Documentacao\memorial\5-metodo-e-ferramental\dados\instalador\celulas\$Id\$Carimbo"

function Write-Passo([string]$Texto) { Write-Host "[celula $Id] $Texto" }

# Roda o Python com a saida e os erros num arquivo de log e devolve o codigo de saida. Pelo cmd.exe: no Windows PowerShell
# 5.1 o 2>&1 de um programa transforma cada linha de erro em excecao, e o Stop derrubaria o roteiro no primeiro aviso.
function Invoke-ComLog([string]$Nome, [string]$Argumentos) {
    Write-Passo "python $Argumentos (saida em $Nome.log)"
    if ($Simular) { return 0 }
    $log = Join-Path $Evidencia "$Nome.log"
    & cmd /c "python $Argumentos > $log 2>&1"
    $codigo = $LASTEXITCODE
    [System.IO.File]::WriteAllText((Join-Path $Evidencia "saida_$Nome.txt"), "$codigo", (New-Object System.Text.UTF8Encoding($false)))
    return $codigo
}

# 1. Onde e quando este roteiro pode rodar.
if ($env:CLAUDECODE) { throw "este roteiro roda na janela do PowerShell do Eric, nunca de dentro do aplicativo Claude (pacote MSIX)" }
$corridas = @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
    Where-Object { $_.CommandLine -match "executar_fase|experimento_|linha_de_base_manual|avaliar_fase|sonda_" })
$lancadores = @(Get-CimInstance Win32_Process -Filter "Name='powershell.exe' OR Name='pwsh.exe'" |
    Where-Object { $_.CommandLine -match "rodar_fase|rodar_fila|rodar_experimento|rodar_sonda|rodar_pendencias|rodar_fumaca" })
$corridas = @($corridas) + @($lancadores)
if ($corridas.Count -gt 0) { throw "ha uma corrida rodando nesta maquina ($($corridas.Count) processo(s)); a celula nao roda agora" }
# ! Alteração de IA - Revisar: (19/11/2026, revisão do pacote I3, achado 1) a célula recusa quando o site (8080) ou a API (8000) já estão no ar.
# ! Motivo: a prova sobe o site e a API ela mesma; com um run.cmd ou um Cobaia.exe aberto, os processos novos sairiam por
# porta ocupada e a prova olharia os antigos, sem provar os arquivos que mudaram.
$emUso = @(Get-NetTCPConnection -State Listen -LocalPort 8080, 8000 -ErrorAction SilentlyContinue)
if ($emUso.Count -gt 0) { throw "o site (8080) ou a API (8000) ja estao no ar nesta maquina; feche o run.cmd ou o Cobaia.exe e rode a celula de novo" }
if ($Raiz -match " ") { throw "o caminho do repositorio tem espaco, e o roteiro nao trata isso: $Raiz" }
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "python nao encontrado no PATH desta janela" }

$inicio = Get-Date
if (-not $Simular) { New-Item -ItemType Directory -Force -Path $Evidencia | Out-Null }
$restaurar = 0
$conferir = 0
# ! Alteração de IA - Revisar: (19/11/2026, revisão do pacote I3, achado 7) as três configurações da janela são guardadas aqui e repostas no finally.
# ! Motivo: elas ficavam valendo na janela do PowerShell depois de o roteiro terminar, e um lançador de corrida aberto na mesma
# janela as herdaria.
$antes = @{ saida = [Console]::OutputEncoding; unbuffered = $env:PYTHONUNBUFFERED; ioencoding = $env:PYTHONIOENCODING }
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUNBUFFERED = "1"
$env:PYTHONIOENCODING = "utf-8"
Push-Location $Raiz
try {
    # 2. O banco das cobaias de volta ao seed: a prova confere as contagens do seed (4 tipos, 14 produtos, 2 usuarios, 0
    # reservas), e a ultima corrida pode ter deixado reservas.
    $restaurar = Invoke-ComLog "restaurar_banco" "restaurar_banco.py"
    # 3. A prova, ate o nivel pedido.
    $conferir = Invoke-ComLog "conferir" "-m instalador.conferir --celula $Id --saida $Evidencia --ate $Ate --modelo-pequeno $ModeloPequeno"
}
finally {
    Pop-Location
    [Console]::OutputEncoding = $antes.saida
    $env:PYTHONUNBUFFERED = $antes.unbuffered
    $env:PYTHONIOENCODING = $antes.ioencoding
    if (-not $Simular) {
        try {
            $saidas = [ordered]@{}
            Get-ChildItem -Path $Evidencia -Filter "saida_*.txt" -ErrorAction SilentlyContinue | Sort-Object Name | ForEach-Object {
                $saidas[$_.BaseName -replace "^saida_", ""] = (Get-Content $_.FullName -Raw).Trim()
            }
            $celula = [ordered]@{
                tag_ia = [ordered]@{
                    alteracao = "! Alteração de IA - Revisar: arquivo gerado por ferramentas/instalador_matriz/celula_alvo.ps1: o que a celula ALVO rodou e com que codigo de saida."
                    motivo = "! Motivo: o plano do instalador unico (decisao 143) pede a evidencia de cada celula em arquivo; a celula ALVO e a prova rodada na maquina-alvo como esta, depois de os tres arquivos do instalador mudarem."
                }
                id = $Id; modo = "novo"; ate = $Ate; modelo_pequeno = $ModeloPequeno
                imagem = "maquina-alvo como esta (sem imagem)"
                inicio = $inicio.ToString("s"); fim = (Get-Date).ToString("s")
                saidas = $saidas
            }
            $json = $celula | ConvertTo-Json -Depth 5
            [System.IO.File]::WriteAllText((Join-Path $Evidencia "celula.json"), $json, (New-Object System.Text.UTF8Encoding($false)))
            $saidas.GetEnumerator() | ForEach-Object { Write-Passo ("{0}: {1}" -f $_.Name, $_.Value) }
        }
        catch { Write-Passo "nao foi possivel gravar o celula.json: $($_.Exception.Message)" }
    }
}
Write-Passo "evidencia em $Evidencia"
Write-Passo "para ler: python ferramentas\instalador_matriz\ler_celula.py ALVO"
if ($restaurar -ne 0 -or $conferir -ne 0) { exit 1 }
