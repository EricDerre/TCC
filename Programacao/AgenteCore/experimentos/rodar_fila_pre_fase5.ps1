# ! Alteracao de IA - Revisar: (11/11/2026, decisoes 116, 120 e 121) fila das tres corridas em texto que rodam antes da Fase 5, uma depois da outra: a corrida 25
# (a biblioteca sem as notas do modelo) pelo lancador dela, que roda antes a ponte da versao do Ollama quando falta; a corrida 26 (o segundo passe do diagnostico)
# e a corrida 27 (o analista de documentacao, medida M2) pelo rodar_fase4.ps1, que roda a bateria de testes, confere Ollama, RAM e versao, roda o modelo e grava a
# leitura de cada uma. Antes das corridas 26 e 27 a fila confere de novo a ponte da versao do Ollama que estiver no ar e a roda se faltar. Depois da corrida 27
# gera a pagina e a planilha da revisao humana as cegas e, no fim, regera o painel uma vez so e roda os testes dele. Para na primeira etapa que falhar, com o
# codigo dela.
# ! Motivo: o Eric escolheu no quadro medir as tres coisas antes da Fase 5 (fichas 63, 66 e 67) e lanca corridas longas da janela dele, uma vez so, com a maquina
# livre; em fila, nenhuma etapa fica para tras. O Ollama se atualiza sozinho, e uma versao nova no meio da fila deixaria a corrida seguinte sem ponte (regra R6):
# por isso a conferencia da ponte se repete antes de cada corrida. O codigo e o lancador da corrida 25 nao mudam: a fila so chama o lancador dela com -SemPainel.
# As duracoes que a fila anuncia sao lidas das previas sem modelo gravadas em resultados_alvo\fase4, e nao escritas aqui.
#
# Uso, numa janela do PowerShell, com o VS Code e o aplicativo Claude fechados (a RAM livre precisa chegar a 6,5 GB):
#   powershell -ExecutionPolicy Bypass -File "C:\Users\Eric.Derre\Documents\TCC\Programacao\AgenteCore\experimentos\rodar_fila_pre_fase5.ps1"
#
# Relancar retoma: a ponte e cada corrida continuam do caso em que pararam; a bateria de testes e a leitura de cada corrida repetem.
# Opcoes:
#   -Etapas X    quais corridas rodar, separadas por virgula (padrao 25,26,27); a ordem e sempre 25, 26, 27. Exemplo: -Etapas 25,26 deixa a corrida 27 para
#                outro dia (o prompt dela foi aprovado como esta em 11/11/2026, ficha 68 e decisao 122).
#   -SemPainel   nao regera o painel no fim.
#   -Simular     so imprime, na ordem, os comandos que a fila rodaria; nao sobe o Ollama nem roda nada (e o que o teste da fila usa).
# Cada corrida tambem roda sozinha:
#   corrida 25:  powershell -ExecutionPolicy Bypass -File ".\rodar_experimento_sem_notas.ps1"
#   corrida 26:  powershell -ExecutionPolicy Bypass -File ".\rodar_fase4.ps1" -Modo segundo_passe -Saida fase4_segundo_passe
#   corrida 27:  powershell -ExecutionPolicy Bypass -File ".\rodar_fase4.ps1" -Modo analista -Saida fase4_analista
# Sozinhas, as corridas 26 e 27 pedem a ponte da versao do Ollama ja registrada em pontes.json; a fila e o lancador da corrida 25 cuidam disso.
param(
    [string]$Etapas = "25,26,27",
    [switch]$SemPainel,
    [switch]$Simular
)
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
$env:RESULTADOS_DIR = "resultados_alvo"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Raiz = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$Previas = Join-Path $PSScriptRoot "resultados_alvo\fase4"

function Passo([string]$Msg) {
    Write-Host ("[{0}] {1}" -f (Get-Date -Format "dd/MM HH:mm:ss"), $Msg)
}
function Parar([string]$Msg, [int]$Codigo) {
    Passo ("!! {0} (codigo {1}); a fila parou aqui" -f $Msg, $Codigo)
    exit $Codigo
}
function Simulado([string]$Comando) {
    Write-Host ("SIMULADO: {0}" -f $Comando)
}
function MinutosDaPrevia([string]$Arquivo, [string]$Chave) {
    # a estimativa de minutos gravada na previa sem modelo de cada corrida; "?" quando o arquivo ou a chave faltam
    $caminho = Join-Path $Previas $Arquivo
    if (-not (Test-Path -LiteralPath $caminho)) { return "?" }
    $texto = [System.IO.File]::ReadAllText($caminho)
    if ($texto -match ('"' + $Chave + '"\s*:\s*(\d+)')) { return $Matches[1] }
    return "?"
}
function Residentes {
    $saida = & ollama ps 2>$null
    if (-not $saida) { return -1 }
    return ($saida | Measure-Object -Line).Lines - 1
}
function SituacaoDaPonte {
    # as linhas chave=valor que o experimento da corrida 25 imprime: versao (a do Ollama no ar), falta (a pasta da ponte que falta) e pareavel (sim, nao ou vazio)
    $linhas = & python @("experimento_sem_notas.py", "--ponte")
    if ($LASTEXITCODE -ne 0) { Parar "experimento_sem_notas.py --ponte saiu com erro (o Ollama esta no ar?)" $LASTEXITCODE }
    $dado = @{}
    foreach ($linha in $linhas) {
        if ("$linha" -match "^([a-z]+)=(.*)$") { $dado[$Matches[1]] = $Matches[2] }
    }
    return $dado
}
function GarantirPonte([string]$Corrida) {
    # regra R6: a corrida so vale com a ponte da versao do Ollama que esta no ar; se o Ollama se atualizou desde a etapa anterior, a ponte roda de novo aqui
    if ($Simular) {
        Simulado ("python experimento_sem_notas.py --ponte (antes da corrida {0}; se a ponte da versao faltar: rodar_fase3b.ps1 -Modo ponte e avaliar_fase4.py --pontes; depois testar_fase4.py --registrar-ponte)" -f $Corrida)
        return
    }
    $Ponte = SituacaoDaPonte
    $Falta = $Ponte["falta"]
    Passo ("antes da corrida {0}: Ollama {1}; ponte que falta: {2}" -f $Corrida, $Ponte["versao"], $(if ($Falta) { $Falta } else { "nenhuma" }))
    if ($Falta) {
        Passo ("ponte de versao (regra R6): rodar_fase3b.ps1 -Modo ponte -Saida {0}" -f $Falta)
        & powershell -ExecutionPolicy Bypass -File ".\rodar_fase3b.ps1" -Modo ponte -Saida $Falta -Modelos qwen2.5:7b
        if ($LASTEXITCODE -ne 0) { Parar "rodar_fase3b.ps1 saiu com erro; relance a fila para retomar a ponte" $LASTEXITCODE }
        Passo "pontes.json regravado com a ponte nova"
        & python @("avaliar_fase4.py", "--pontes")
        if ($LASTEXITCODE -ne 0) { Parar "avaliar_fase4.py --pontes saiu com erro" $LASTEXITCODE }
        $Ponte = SituacaoDaPonte
        if ($Ponte["falta"]) { Parar ("a ponte {0} rodou mas nao entrou em pontes.json (nao cobriu os 36 casos?); veja resultados_alvo\{0}\fase3b.log" -f $Falta) 1 }
    }
    if ($Ponte["pareavel"] -eq "nao") {
        Parar ("a ponte da versao {0} do Ollama nao e pareavel com a Fase 3 (b + c acima de 2): a corrida {1} nao teria veredito. Nada mais roda; leve o resultado ao Claude" -f $Ponte["versao"], $Corrida) 1
    }
    # ! Alteracao de IA - Revisar: (11/11/2026) a pasta da ponte da versao no ar entra no registro das areas so de leitura antes da corrida, por
    # testar_fase4.py --registrar-ponte, que so acrescenta essa pasta e recusa se outra area tiver mudado.
    # ! Motivo: a ponte cria a pasta resultados_alvo\fase3b_ponte_<versao>, e a bateria que o rodar_fase4.ps1 roda antes de cada corrida compara as pastas fase3b_* com
    # o registro. Em 11/11/2026 a corrida 25 parou assim, logo depois da ponte da 0.40.15; se o Ollama se atualizar no meio da fila, o mesmo aconteceria aqui.
    if ($Ponte["pasta"]) {
        Passo ("registro das areas so de leitura: testar_fase4.py --registrar-ponte {0}" -f $Ponte["pasta"])
        & python @("testar_fase4.py", "--registrar-ponte", $Ponte["pasta"])
        if ($LASTEXITCODE -ne 0) { Parar "testar_fase4.py --registrar-ponte recusou a pasta da ponte (outra area so de leitura mudou?). Nada mais roda; leve o resultado ao Claude" $LASTEXITCODE }
    }
}

$Validas = @("25", "26", "27")
$Pedidas = @($Etapas -split "[,\s]+" | Where-Object { $_ -ne "" })
foreach ($Etapa in $Pedidas) {
    if ($Validas -notcontains $Etapa) {
        Write-Host ("!! etapa desconhecida: {0}; use 25, 26 ou 27, separadas por virgula" -f $Etapa)
        exit 2
    }
}
if ($Pedidas.Count -eq 0) {
    Write-Host "!! nenhuma etapa pedida; use 25, 26 ou 27, separadas por virgula"
    exit 2
}
$Min25 = MinutosDaPrevia "sem_notas_previa.json" "minutos_estimados_pela_mediana_das_referencias"
$Min26 = MinutosDaPrevia "segundo_passe_previa.json" "minutos_estimados"
$Min27 = MinutosDaPrevia "analista_previa.json" "minutos_estimados"
Passo ("fila antes da Fase 5: corridas {0}{1}" -f (($Validas | Where-Object { $Pedidas -contains $_ }) -join ", "), $(if ($Simular) { " (simulacao: nada roda)" } else { "" }))

if (-not $Simular) {
    if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) { Parar "Ollama nao encontrado no PATH" 2 }
    if ((Residentes) -lt 0) {
        Passo "servidor do Ollama nao responde - iniciando"
        Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
        $espera = 0
        while ((Residentes) -lt 0 -and $espera -lt 30) { Start-Sleep -Seconds 2; $espera++ }
        if ((Residentes) -lt 0) { Parar "o Ollama nao subiu; abra o aplicativo Ollama e rode de novo" 2 }
    }
}

if ($Pedidas -contains "25") {
    Passo ("corrida 25 (a biblioteca sem as notas do modelo): o lancador dela roda antes a ponte da versao do Ollama, se faltar, e depois a corrida, cerca de {0} minutos" -f $Min25)
    if ($Simular) {
        Simulado "powershell -ExecutionPolicy Bypass -File .\rodar_experimento_sem_notas.ps1 -SemPainel"
    } else {
        & powershell -ExecutionPolicy Bypass -File ".\rodar_experimento_sem_notas.ps1" -SemPainel
        if ($LASTEXITCODE -ne 0) { Parar "a corrida 25 (rodar_experimento_sem_notas.ps1) saiu com erro; relance a fila para retomar" $LASTEXITCODE }
    }
}

if ($Pedidas -contains "26") {
    GarantirPonte "26"
    Passo ("corrida 26 (o segundo passe do diagnostico): cerca de {0} minutos" -f $Min26)
    if ($Simular) {
        Simulado "powershell -ExecutionPolicy Bypass -File .\rodar_fase4.ps1 -Modo segundo_passe -Saida fase4_segundo_passe"
    } else {
        & powershell -ExecutionPolicy Bypass -File ".\rodar_fase4.ps1" -Modo segundo_passe -Saida fase4_segundo_passe
        if ($LASTEXITCODE -ne 0) { Parar "a corrida 26 (rodar_fase4.ps1 -Modo segundo_passe) saiu com erro; relance a fila para retomar do caso em que parou" $LASTEXITCODE }
    }
}

if ($Pedidas -contains "27") {
    GarantirPonte "27"
    Passo ("corrida 27 (o analista de documentacao, medida M2): cerca de {0} minutos" -f $Min27)
    if ($Simular) {
        Simulado "powershell -ExecutionPolicy Bypass -File .\rodar_fase4.ps1 -Modo analista -Saida fase4_analista"
    } else {
        & powershell -ExecutionPolicy Bypass -File ".\rodar_fase4.ps1" -Modo analista -Saida fase4_analista
        if ($LASTEXITCODE -ne 0) { Parar "a corrida 27 (rodar_fase4.ps1 -Modo analista) saiu com erro; relance a fila para retomar do caso em que parou" $LASTEXITCODE }
    }
    Passo "revisao humana as cegas das propostas: a pagina, a planilha e a chave da origem (sem modelo)"
    $Revisao = Join-Path $Raiz "ferramentas\revisao_propostas.py"
    if ($Simular) {
        Simulado ("python {0} --gerar" -f $Revisao)
    } else {
        & python $Revisao --gerar
        if ($LASTEXITCODE -ne 0) { Parar "revisao_propostas.py --gerar saiu com erro; a corrida 27 e a leitura dela ja estao gravadas" $LASTEXITCODE }
    }
}

if (-not $SemPainel) {
    Passo "painel: regerar uma vez e rodar os dois testes dele"
    foreach ($Arquivo in @("gerar_dashboard.py", "testar_painel_textos.py", "testar_painel_topicos.py")) {
        $Caminho = Join-Path (Join-Path $Raiz "ferramentas") $Arquivo
        if ($Simular) {
            Simulado ("python {0}" -f $Caminho)
        } else {
            & python $Caminho
            if ($LASTEXITCODE -ne 0) { Parar ("{0} saiu com erro; as corridas e as leituras ja estao gravadas" -f $Arquivo) $LASTEXITCODE }
        }
    }
}

Passo "FIM da fila: as leituras estao em resultados_alvo\fase4 (sem_notas, segundo_passe e analista, .md e .json), cada uma com o veredito pela regra fixada antes; o log de cada corrida em resultados_alvo\<pasta da corrida>\fase4.log"
Passo "proxima sessao do Claude: ler os tres JSON, registrar no roadmap e nas fichas, publicar a pagina da revisao as cegas (ficha 69) e republicar o painel no mesmo endereco"
exit 0
