# ! Alteracao de IA - Revisar: orquestrador da Fase 4 (26/10/2026, pacote P2), no molde de rodar_fase3b.ps1: confere
# a venv do AgenteCore (onde esta o Playwright), roda testar_fase4.py, roda executar_fase4.py no modo pedido e, ao
# fim, avaliar_fase4.py. Log em <Resultados>\<Saida>\fase4.log (o executar_fase4.py grava a linha FIM). Modo
# disponivel neste pacote: reproducao (corrida 17, sem modelo); os modos com modelo entram no P3 com a ponte de versao.
# ! Motivo: o plano aprovado (secao 6) fixa um comando por corrida com -Modo e -Saida, e o painel le o roadmap por
# esses comandos; o script e o lugar unico das conferencias de ambiente antes de cada corrida.
# ! Alteracao de IA - Revisar: em 27/10/2026 ganhou -Banco (qual banco de casos a corrida le), -Nome e -Titulo
# (arquivos e titulo da avaliacao), para a corrida de reproducao sobre os 36 ineditos da ficha 27.
# ! Motivo: a corrida 17 leu so os 72 casos de avaliacao e gravou reproducibilidade.{json,md}; a corrida sobre os
# ineditos precisa de pasta, arquivos e titulo proprios para nao regravar a leitura da corrida 17.
# ! Alteracao de IA - Revisar: em 27/10/2026 (pacote P3) ganhou os modos calibracao (corrida 16) e tela (corrida 18),
# com as conferencias dos modos com modelo copiadas de rodar_fase3b.ps1 (Ollama no PATH e no ar, nenhum modelo
# residente, RAM livre minima por modelo com espera), a versao do Ollama lida por /api/version antes e depois da corrida
# (codigo 1 se mudou, decisao 44), -K (lista de k da calibracao ou o k da tela), -Modelo, -Top, -Intervencoes e
# -Amostra, e a avaliacao com --pasta apontando para a pasta da corrida quando -Casos limita os casos.
# ! Motivo: plano aprovado, secao 6 (corridas 16 e 18) e regras R6 a R8; uma corrida parcial de fumaca nunca pode
# regravar os derivados oficiais de resultados_alvo\fase4 (limiares.json, calibracao, tela), e a regra R6 manda abortar
# se o Ollama se atualizar no meio da noite.
# ! Alteracao de IA - Revisar: em 01/11/2026 (pacote P4) ganhou o modo cura (corrida 19, sem modelo), -Repeticoes (repeticoes
# por celula, padrao 5), -Formas (as formas da quebra: harness, php ou as duas) e -Roteiros/-Modos (filtros para a fumaca);
# a avaliacao do modo e avaliar_fase4.py --cura.
# ! Motivo: plano aprovado, secao 6 (corrida 19: rodar_fase4.ps1 -Modo cura -Saida fase4_cura -Repeticoes 5) e ficha 29 c
# (as duas formas de quebra comparadas); uma fumaca com um roteiro e uma repeticao nunca grava derivado oficial.
#
# Uso (PowerShell, de dentro de experimentos\):
#   powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo reproducao -Saida fase4_reproducao
#   powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo reproducao -Saida fase4_reproducao_ineditos -Banco ineditos_fase4 -Nome reproducibilidade_ineditos -Titulo "Reproducao na tela (corrida 17 sobre os 36 ineditos da ficha 27)"
#   powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo calibracao -Saida fase4_calibracao -K 3,5
#   powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo tela -Saida fase4_tela
#   powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo cura -Saida fase4_cura -Repeticoes 5
#   -Casos N        limita aos N primeiros casos (0 = todos); com N > 0 a avaliacao grava na pasta da corrida, nao em fase4\
#   -Canal X        chromium (padrao) ou msedge
#   -Resultados X   pasta de resultados (padrao resultados_alvo)
#   -Banco X        avaliacao (padrao, os 72 casos), ineditos_fase4 (os 36 da ficha 27) ou todos (108)
#   -Nome X         nome dos arquivos da avaliacao em <Resultados>\fase4 (padrao reproducibilidade)
#   -Titulo X       titulo do relatorio .md da avaliacao
#   -K X            calibracao: lista de k separada por virgula (padrao 3,5); tela: um k (padrao: o de limiares.json)
#   -Modelo X       modelo do Ollama (padrao qwen2.5:7b)
#   -Top N          alternativas por posicao pedidas ao Ollama (padrao 20)
#   -Intervencoes   tela: roda as intervencoes da especificacao quando um gatilho dispara (padrao: desligadas)
#   -Amostra        tela: os 36 casos oficiais de avaliacao disparam o gatilho da amostra fixa
#   -Repeticoes N   cura: repeticoes por celula (roteiro x modo x forma; padrao 5)
#   -Formas X       cura: formas da quebra separadas por virgula (padrao harness,php)
#   -Roteiros X     cura: so estes roteiros do front legado, separados por virgula (fumaca); com filtro a avaliacao grava na pasta da corrida
#   -Modos X        cura: so estes modos de quebra, separados por virgula (fumaca)
param(
    [Parameter(Mandatory = $true)][ValidateSet("reproducao", "calibracao", "tela", "cura")][string]$Modo,
    [Parameter(Mandatory = $true)][string]$Saida,
    [int]$Casos = 0,
    [ValidateSet("chromium", "msedge")][string]$Canal = "chromium",
    [string]$Resultados = "resultados_alvo",
    [ValidateSet("avaliacao", "ineditos_fase4", "todos")][string]$Banco = "avaliacao",
    [string]$Nome = "",
    [string]$Titulo = "",
    [string]$K = "",
    [string]$Modelo = "qwen2.5:7b",
    [int]$Top = 20,
    [switch]$Intervencoes,
    [switch]$Amostra,
    [int]$Repeticoes = 5,
    [string]$Formas = "harness,php",
    [string]$Roteiros = "",
    [string]$Modos = ""
)
$ErrorActionPreference = "Stop"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:RESULTADOS_DIR = $Resultados
$Aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Aqui
$Inicio = Get-Date
$ComModelo = ($Modo -eq "calibracao") -or ($Modo -eq "tela")
$Venv = Join-Path $Aqui "..\.venv\Scripts\python.exe"
if (-not (Test-Path $Venv)) {
    Write-Host "!! venv do AgenteCore nao encontrada em $Venv (rode install.py primeiro)"
    exit 2
}
$Log = Join-Path (Join-Path (Join-Path $Aqui $Resultados) $Saida) "fase4.log"
# RAM livre minima por modelo (peso residente medido na 2-B + cache de contexto), em GB - o mesmo valor de rodar_fase3b.ps1.
$RamMinima = @{ "qwen2.5:7b" = 6.5; "qwen2.5-coder:7b" = 6.5; "qwen2.5-coder:3b" = 3.5 }

function Marco([string]$Msg) {
    $linha = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Msg
    Write-Host $linha
    $dir = Split-Path -Parent $Log
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
    # ! Alteracao de IA - Revisar: (01/11/2026) a linha passa a ser gravada por um System.IO.FileStream aberto em modo
    # Append com FileShare.ReadWrite (deixa outros processos lerem e escreverem no arquivo enquanto o Marco grava), por
    # um StreamWriter UTF-8 (o BOM so entra quando o arquivo esta vazio, igual ao Add-Content -Encoding utf8), e as
    # tentativas sobem de 10 para 60, de 500 ms (cerca de 30 s). Se nenhuma der certo, o Marco avisa no console com o
    # ultimo erro e a corrida segue: uma linha de log nunca derruba a corrida (essa parte ja vinha de 27/10, quando
    # duas tentativas da corrida 16 morreram na segunda linha de log por causa de $ErrorActionPreference = Stop).
    # ! Motivo: no fim da corrida 16 (27/10/2026, 23:53 e 23:54) a chamada de avaliar_fase4.py e a linha FIM ficaram
    # fora de fase4.log: 10 tentativas de 500 ms deram "O processo nao pode acessar o arquivo ... porque ele esta sendo
    # usado por outro processo" nas duas. Reproduzido em 01/11/2026 com outro processo segurando o arquivo: o
    # Add-Content falhou com os 7 modos de leitor testados, ate com um leitor que aceita escrita (Read/ReadWrite),
    # porque ele mesmo nao aceita leitores; o Python (open(..., "a")), que nunca falhou, aceita. O FileStream com
    # ReadWrite convive com esse leitor e grava na hora. Um leitor que nao aceita escrita (FileShare.Read, que so aceita
    # outros leitores, ou FileShare.None) bloqueia qualquer escritor, seja qual for o modo do escritor: contra esse so a
    # espera ajuda, e por isso a espera maior.
    $codificacao = New-Object System.Text.UTF8Encoding($true)
    $ultimoErro = ""
    for ($tentativa = 1; $tentativa -le 60; $tentativa++) {
        $fluxo = $null
        $escritor = $null
        $gravou = $false
        try {
            $fluxo = New-Object System.IO.FileStream($Log, [System.IO.FileMode]::Append, [System.IO.FileAccess]::Write, [System.IO.FileShare]::ReadWrite)
            $escritor = New-Object System.IO.StreamWriter($fluxo, $codificacao)
            $escritor.WriteLine($linha)
            $escritor.Flush()
            $gravou = $true
        } catch {
            $ultimoErro = $_.Exception.Message
        } finally {
            if ($escritor) { try { $escritor.Dispose() } catch { } } elseif ($fluxo) { try { $fluxo.Dispose() } catch { } }
        }
        if ($gravou) { return }
        Start-Sleep -Milliseconds 500
    }
    Write-Host "!! nao consegui gravar a linha acima em $Log depois de 60 tentativas ($ultimoErro); a corrida segue"
}
function RamLivreGB {
    return [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 1)
}
function Residentes {
    $saida = & ollama ps 2>$null
    if (-not $saida) { return -1 }
    return ($saida | Measure-Object -Line).Lines - 1
}
function VersaoOllama {
    try { return (Invoke-RestMethod -Uri "http://localhost:11434/api/version" -TimeoutSec 10).version } catch { return "" }
}
function EsperarRam($modelo) {
    $minimo = $RamMinima[$modelo]
    if (-not $minimo) { $minimo = 6.5 }
    $tentativas = 0
    while ((RamLivreGB) -lt $minimo -and $tentativas -lt 10) {
        Marco ("RAM livre {0} GB, {1} precisa de {2} GB - feche programas; nova checagem em 30 s" -f (RamLivreGB), $modelo, $minimo)
        Start-Sleep -Seconds 30
        $tentativas++
    }
    return ((RamLivreGB) -ge $minimo)
}

Marco "rodar_fase4.ps1: modo $Modo, saida $Saida, canal $Canal, resultados $Resultados, casos $Casos"
$VersaoInicio = ""
if ($ComModelo) {
    if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) { Marco "!! Ollama nao encontrado no PATH"; exit 2 }
    if ((Residentes) -lt 0) {
        Marco "servidor do Ollama nao responde - iniciando"
        Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
        $espera = 0
        while ((Residentes) -lt 0 -and $espera -lt 30) { Start-Sleep -Seconds 2; $espera++ }
        if ((Residentes) -lt 0) { Marco "!! o Ollama nao subiu; abra o aplicativo Ollama e rode de novo"; exit 2 }
    }
    if ((Residentes) -gt 0) {
        & ollama ps
        Marco "!! ha modelo residente no Ollama; regra do experimento: um modelo por vez (ollama stop <modelo>)"
        exit 2
    }
    $VersaoInicio = VersaoOllama
    if (-not $VersaoInicio) { Marco "!! o Ollama nao respondeu em /api/version"; exit 2 }
    Marco ("Ollama {0}; modelo {1}; RAM livre {2} GB" -f $VersaoInicio, $Modelo, (RamLivreGB))
    if (-not (EsperarRam $Modelo)) { Marco ("!! RAM livre {0} GB abaixo do minimo de {1} GB para {2}; libere memoria e relance" -f (RamLivreGB), $RamMinima[$Modelo], $Modelo); exit 2 }
}

Marco "testar_fase4.py"
& python testar_fase4.py
if ($LASTEXITCODE -ne 0) { Marco "!! testar_fase4.py falhou (codigo $LASTEXITCODE)"; exit 1 }

$Argumentos = @("executar_fase4.py", "--modo", $Modo, "--saida", $Saida, "--canal", $Canal, "--banco", $Banco)
if ($Casos -gt 0) { $Argumentos += @("--casos", "$Casos") }
if ($ComModelo) {
    $Argumentos += @("--modelo", $Modelo, "--top", "$Top")
    if ($K) { $Argumentos += @("--k", $K) }
    if ($Intervencoes) { $Argumentos += @("--intervencoes", "por_gatilho") }
    if ($Amostra) { $Argumentos += @("--amostra") }
}
$CuraParcial = $false
if ($Modo -eq "cura") {
    $Argumentos += @("--repeticoes", "$Repeticoes", "--formas", $Formas)
    if ($Roteiros) { $Argumentos += @("--roteiros", $Roteiros) }
    if ($Modos) { $Argumentos += @("--modos", $Modos) }
    # fumaca ou corrida filtrada: a avaliacao grava na pasta da corrida, nunca em resultados_alvo\fase4
    $CuraParcial = ($Roteiros -ne "") -or ($Modos -ne "") -or ($Repeticoes -ne 5) -or ($Formas -ne "harness,php")
}
Marco ("executar_fase4.py " + (($Argumentos | Select-Object -Skip 1) -join " "))
& $Venv @Argumentos
$CodigoExecutor = $LASTEXITCODE
if ($ComModelo) {
    $VersaoFim = VersaoOllama
    if ($VersaoFim -ne $VersaoInicio) {
        Marco ("!! a versao do Ollama mudou durante a corrida: {0} para {1}; a corrida nao vale como medida (decisao 44)" -f $VersaoInicio, $VersaoFim)
        exit 1
    }
}
if ($CodigoExecutor -ne 0) { Marco "!! executar_fase4.py saiu com codigo $CodigoExecutor"; exit $CodigoExecutor }

$Avaliacao = @("avaliar_fase4.py", "--$Modo", "--saida", $Saida)
if ($Nome) { $Avaliacao += @("--nome", $Nome) }
if ($Titulo) { $Avaliacao += @("--titulo", $Titulo) }
if (($Casos -gt 0) -or $CuraParcial) { $Avaliacao += @("--pasta", (Join-Path (Join-Path $Aqui $Resultados) $Saida)) }
Marco ("avaliar_fase4.py " + (($Avaliacao | Select-Object -Skip 1) -join " "))
& python @Avaliacao
if ($LASTEXITCODE -ne 0) { Marco "!! avaliar_fase4.py saiu com codigo $LASTEXITCODE"; exit $LASTEXITCODE }
$duracao = (Get-Date) - $Inicio
Marco ("FIM rodar_fase4.ps1 (modo {0}) - duracao total {1:d2}h{2:d2}" -f $Modo, [int][math]::Floor($duracao.TotalHours), $duracao.Minutes)
exit 0
