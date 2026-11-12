# ! Alteracao de IA - Revisar: (10/11/2026, ficha 63 opcao b, decisao 116) lancador da corrida 25, o experimento em texto da biblioteca de producao sem as
# notas do modelo e sem os verbetes aprendidos. Pergunta ao experimento_sem_notas.py qual versao do Ollama esta no ar e se falta a ponte dela; se falta, roda a
# ponte pelo rodar_fase3b.ps1 (a biblioteca original nos 36 casos de avaliacao, so com o qwen2.5:7b) e regrava pontes.json; para se a ponte nao for pareavel;
# roda a corrida pelo rodar_fase4.ps1 (que roda a bateria de testes, confere Ollama, RAM e versao, roda as 72 inferencias e grava a leitura) e, no fim, regera o
# painel e roda os testes dele. Para na primeira etapa que falhar.
# ! Motivo: o Eric escolheu no quadro medir quanto pesam as notas que o modelo escreveu na biblioteca, numa corrida lancada da janela dele. O Ollama da maquina
# esta na versao 0.40.15, que nao tem ponte registrada, e a regra R6 manda rodar a ponte antes de qualquer medida; as quatro pontes anteriores rodaram pelo
# rodar_fase3b.ps1, e este lancador usa o mesmo caminho, com o nome da pasta tirado da versao que estiver no ar (0.40.15 vira fase3b_ponte_04015). E um comando
# so, com a ponte, a corrida, a leitura e o painel, para nenhuma etapa ficar para tras. O registro dos numeros no roadmap e a republicacao do painel ficam para a
# proxima sessao do Claude, que le resultados_alvo\fase4\sem_notas.json.
#
# Uso, numa janela do PowerShell, com o VS Code e o aplicativo Claude fechados (a RAM livre precisa chegar a 6,5 GB):
#   powershell -ExecutionPolicy Bypass -File "C:\Users\Eric.Derre\Documents\TCC\Programacao\AgenteCore\experimentos\rodar_experimento_sem_notas.ps1"
#
# Duracao esperada: cerca de 40 minutos da ponte (a de 03/11/2026 levou 42) e cerca de 80 minutos da corrida. Relancar retoma: a ponte e a corrida continuam do
# caso em que pararam; a bateria de testes e a leitura repetem.
# Opcoes: -Saida (pasta da corrida, padrao fase4_sem_notas); -Casos (os N primeiros casos de cada banco, para fumaca: a ponte nao e exigida, a leitura fica na
# pasta da corrida e o painel nao e regerado); -SemPainel (nao regera o painel).
param(
    [string]$Saida = "fase4_sem_notas",
    [int]$Casos = 0,
    [switch]$SemPainel
)
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
$env:RESULTADOS_DIR = "resultados_alvo"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Raiz = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path

function Passo([string]$Msg) {
    Write-Host ("[{0}] {1}" -f (Get-Date -Format "dd/MM HH:mm:ss"), $Msg)
}
function Parar([string]$Msg, [int]$Codigo) {
    Passo ("!! {0} (codigo {1}); o lancador parou aqui" -f $Msg, $Codigo)
    exit $Codigo
}
function Residentes {
    $saida = & ollama ps 2>$null
    if (-not $saida) { return -1 }
    return ($saida | Measure-Object -Line).Lines - 1
}
function SituacaoDaPonte {
    # as linhas chave=valor que o experimento imprime: versao (a do Ollama no ar), falta (a pasta da ponte que falta) e pareavel (sim, nao ou vazio)
    $linhas = & python @("experimento_sem_notas.py", "--ponte")
    if ($LASTEXITCODE -ne 0) { Parar "experimento_sem_notas.py --ponte saiu com erro (o Ollama esta no ar?)" $LASTEXITCODE }
    $dado = @{}
    foreach ($linha in $linhas) {
        if ("$linha" -match "^([a-z]+)=(.*)$") { $dado[$Matches[1]] = $Matches[2] }
    }
    return $dado
}

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) { Parar "Ollama nao encontrado no PATH" 2 }
if ((Residentes) -lt 0) {
    Passo "servidor do Ollama nao responde - iniciando"
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    $espera = 0
    while ((Residentes) -lt 0 -and $espera -lt 30) { Start-Sleep -Seconds 2; $espera++ }
    if ((Residentes) -lt 0) { Parar "o Ollama nao subiu; abra o aplicativo Ollama e rode de novo" 2 }
}

$Ponte = SituacaoDaPonte
$Falta = $Ponte["falta"]
Passo ("Ollama {0}; ponte que falta: {1}" -f $Ponte["versao"], $(if ($Falta) { $Falta } else { "nenhuma" }))
if ($Casos -eq 0) {
    if ($Falta) {
        Passo ("ponte de versao (regra R6): rodar_fase3b.ps1 -Modo ponte -Saida {0}, cerca de 40 minutos" -f $Falta)
        & powershell -ExecutionPolicy Bypass -File ".\rodar_fase3b.ps1" -Modo ponte -Saida $Falta -Modelos qwen2.5:7b
        if ($LASTEXITCODE -ne 0) { Parar "rodar_fase3b.ps1 saiu com erro; relance este lancador para retomar a ponte" $LASTEXITCODE }
        Passo "pontes.json regravado com a ponte nova"
        & python @("avaliar_fase4.py", "--pontes")
        if ($LASTEXITCODE -ne 0) { Parar "avaliar_fase4.py --pontes saiu com erro" $LASTEXITCODE }
        $Ponte = SituacaoDaPonte
        if ($Ponte["falta"]) { Parar ("a ponte {0} rodou mas nao entrou em pontes.json (nao cobriu os 36 casos?); veja resultados_alvo\{0}\fase3b.log" -f $Falta) 1 }
    }
    if ($Ponte["pareavel"] -eq "nao") {
        Parar ("a ponte da versao {0} do Ollama nao e pareavel com a Fase 3 (b + c acima de 2): a comparacao com as corridas 22 e 24 nao vale. Nada mais roda; leve o resultado ao Claude" -f $Ponte["versao"]) 1
    }
    # ! Alteracao de IA - Revisar: (11/11/2026) a pasta da ponte da versao no ar entra no registro das areas so de leitura antes da corrida, por
    # testar_fase4.py --registrar-ponte, que so acrescenta essa pasta e recusa se outra area tiver mudado.
    # ! Motivo: a ponte cria a pasta resultados_alvo\fase3b_ponte_<versao>, e a bateria que o rodar_fase4.ps1 roda antes da corrida compara as pastas fase3b_* com o
    # registro. Em 11/11/2026 a ponte da 0.40.15 rodou ate o fim e a corrida 25 parou em 9 segundos, com a pasta nova acusada como area alterada.
    if ($Ponte["pasta"]) {
        Passo ("registro das areas so de leitura: testar_fase4.py --registrar-ponte {0}" -f $Ponte["pasta"])
        & python @("testar_fase4.py", "--registrar-ponte", $Ponte["pasta"])
        if ($LASTEXITCODE -ne 0) { Parar "testar_fase4.py --registrar-ponte recusou a pasta da ponte (outra area so de leitura mudou?). Nada mais roda; leve o resultado ao Claude" $LASTEXITCODE }
    }
}

$Argumentos = @("-Modo", "sem_notas", "-Saida", $Saida)
if ($Casos -gt 0) { $Argumentos += @("-Casos", "$Casos") }
Passo ("corrida 25: rodar_fase4.ps1 {0}, cerca de 80 minutos com os 72 casos" -f ($Argumentos -join " "))
if ($Casos -gt 0) {
    & powershell -ExecutionPolicy Bypass -File ".\rodar_fase4.ps1" -Modo sem_notas -Saida $Saida -Casos $Casos
} else {
    & powershell -ExecutionPolicy Bypass -File ".\rodar_fase4.ps1" -Modo sem_notas -Saida $Saida
}
if ($LASTEXITCODE -ne 0) { Parar "rodar_fase4.ps1 saiu com erro; relance este lancador para retomar do caso em que parou" $LASTEXITCODE }

if ((-not $SemPainel) -and ($Casos -eq 0)) {
    Passo "painel: gerar_dashboard.py, testar_painel_textos.py e testar_painel_topicos.py"
    & python (Join-Path $Raiz "ferramentas\gerar_dashboard.py")
    if ($LASTEXITCODE -ne 0) { Parar "gerar_dashboard.py saiu com erro" $LASTEXITCODE }
    & python (Join-Path $Raiz "ferramentas\testar_painel_textos.py")
    if ($LASTEXITCODE -ne 0) { Parar "testar_painel_textos.py falhou" $LASTEXITCODE }
    & python (Join-Path $Raiz "ferramentas\testar_painel_topicos.py")
    if ($LASTEXITCODE -ne 0) { Parar "testar_painel_topicos.py falhou" $LASTEXITCODE }
}

Passo ("FIM: a leitura da corrida 25 esta em resultados_alvo\fase4\sem_notas.md (e .json), com o veredito pela regra da decisao 116; o log em resultados_alvo\{0}\fase4.log" -f $Saida)
Passo "proxima sessao do Claude: ler sem_notas.json, registrar no roadmap e nas fichas e republicar o painel no mesmo endereco"
exit 0
