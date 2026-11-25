# ! Alteracao de IA - Revisar: (16/11/2026, Fase 5, pacote F1, decisao 133) lancador da noite medida da Fase 5 (os dez cenarios da ficha 36 com cinco repeticoes,
# 50 execucoes), no molde de rodar_fila_pre_fase5.ps1. Seis etapas, parando na primeira que falhar, com o codigo dela: (1) espera a memoria livre chegar a
# 7,0 GB e confere que nao ha modelo residente no Ollama; (2) confere, sem chamar o modelo, que o agente de hoje e o da corrida 21d (avaliar_fase5.py --antes:
# biblioteca de producao, prompt fixo, indice da busca, k, limiares e versao do navegador iguais aos de resultados_alvo\fase4_ensaio_v4\condicoes_fase4.json); (3) roda
# a ponte da versao do Ollama que estiver no ar, se ela nao tiver ponte registrada (regra R6), e poe a pasta da ponte no registro das areas so de leitura; (4) roda a
# corrida pelo rodar_fase4.ps1 -Modo cenarios; (5) grava a leitura por cenario (avaliar_fase5.py --agente, em resultados_alvo\fase5\agente.{json,md}); (6) regera o
# painel uma vez e roda as cinco baterias dele.
# ! Motivo: o plano aprovado da Fase 5 (secao 3.4) pede um comando so para a noite, que o Eric lanca da janela dele com a maquina livre. Tres coisas nao podem
# depender de alguem lembrar na hora. Primeira: sem -Nome, o rodar_fase4.ps1 -Modo cenarios grava a leitura em resultados_alvo\fase4\cenarios.{json,md}, que e a
# leitura da corrida 21; por isso o nome da leitura esta na lista unica de argumentos que a corrida e a simulacao usam, e o teste do lancador confere. Segunda: o
# Ollama se atualiza sozinho, e uma versao sem ponte faria a corrida parar depois da bateria de testes (regra R6). Terceira: a noite so vale se o agente for o da
# corrida 21d, e isso e conferido antes de gastar a hora de maquina. A duracao que o lancador anuncia e lida de resultados_alvo\fase5\custo.json
# (avaliar_fase5.py --custo), e nao escrita aqui.
# ! Alteracao de IA - Revisar: (18/11/2026, corrida 28b, decisoes 145 e 146) a noite passa a rodar a frio, em pasta nova: a saida e resultados_alvo\fase5_agente_b e a
# leitura do ensaio, resultados_alvo\fase4\cenarios_fase5b.{json,md}. A etapa 4 roda uma repeticao por vez, de 1 a 5: antes de cada uma tira o modelo da memoria
# (ollama stop), confere que o ollama ps ficou vazio e que a versao do Ollama no ar e a das execucoes ja gravadas, e so entao chama o rodar_fase4.ps1 com
# -Repeticoes N, que roda as dez execucoes da repeticao N e pula as ja feitas. Antes da primeira repeticao, pede que a ultima sondagem do frio
# (rodar_sondagem_frio.ps1) tenha passado, na versao do Ollama que esta no ar. Relancar retoma na primeira repeticao incompleta, e com as 50 gravadas na pasta
# nova a corrida nao roda de novo.
# ! Motivo: a corrida 28 (18/11/2026, pasta fase5_agente) foi lancada com o aplicativo Claude aberto e, nas repeticoes 2 a 5, o Ollama reaproveitou o prompt lido na
# repeticao 1: a noite levou 31 minutos, e o MTTR dessas repeticoes caiu para menos da metade. O Eric decidiu refazer a noite com tudo fechado (decisao 145) e a
# frio (decisao 146). O executor do ensaio nao muda: chamado com -Repeticoes N na mesma pasta, ele retoma pelas execucoes ja gravadas em cenarios.jsonl, descarrega
# o modelo no fim de cada chamada e para se os diagnosticos ja gravados vieram de outra versao do Ollama (decisao 44). A pasta da corrida 28 e a leitura dela
# (cenarios_fase5) nao sao tocadas: ficam como registro do incidente.
#
# Uso, numa janela do PowerShell, com o VS Code e o aplicativo Claude fechados, o notebook na tomada e a suspensao desligada, depois de a sondagem ter passado:
#   powershell -ExecutionPolicy Bypass -File "C:\Users\Eric.Derre\Documents\TCC\Programacao\AgenteCore\experimentos\rodar_sondagem_frio.ps1"
#   powershell -ExecutionPolicy Bypass -File "C:\Users\Eric.Derre\Documents\TCC\Programacao\AgenteCore\experimentos\rodar_fase5.ps1"
#
# Relancar retoma: as execucoes ja gravadas em resultados_alvo\fase5_agente_b\cenarios.jsonl nao rodam de novo. Se o lancador ou o rodar_fase4.ps1 disser que a
# versao do Ollama mudou, NAO relance: a noite nao vale como medida, a pasta parcial vira incidente e a noite recomeca em pasta nova (plano, secao 3.3); leve a
# mensagem ao Claude.
# Opcoes:
#   -SemPainel   nao regera o painel no fim.
#   -Simular     so imprime, na ordem, os comandos que a noite rodaria; nao sobe o Ollama nem roda nada (e o que o teste do lancador usa).
param(
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
$Venv = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
$Custo = Join-Path $PSScriptRoot "resultados_alvo\fase5\custo.json"
$Modelo = "qwen2.5:7b"
$Saida = "fase5_agente_b"
$NomeDaLeitura = "cenarios_fase5b"
$Repeticoes = 5
# o rodar_fase4.ps1 exige 6,5 GB livres para o qwen2.5:7b; a folga evita a queda na checagem dele (licao da corrida 18b)
$RamMinimaGB = 7.0
$Titulo = "Fase 5: os dez cenários com cinco repetições (corrida 28b)"

function Passo([string]$Msg) {
    Write-Host ("[{0}] {1}" -f (Get-Date -Format "dd/MM HH:mm:ss"), $Msg)
}
function Parar([string]$Msg, [int]$Codigo) {
    Passo ("!! {0} (codigo {1}); a noite parou aqui" -f $Msg, $Codigo)
    exit $Codigo
}
function Simulado([string]$Comando) {
    Write-Host ("SIMULADO: {0}" -f $Comando)
}
# ! Alteracao de IA - Revisar: a lista dos argumentos de cada repeticao sai desta funcao; a chamada de verdade e a linha que -Simular imprime usam a mesma lista.
# ! Motivo: se a simulacao montasse o comando por outro caminho, o teste do lancador poderia passar com o -Nome so na linha simulada, e a noite gravaria por cima da
# leitura da corrida 21 em resultados_alvo\fase4\cenarios.{json,md}. So muda de uma repeticao para a outra o numero depois de -Repeticoes.
function ListaDeArgumentos([int]$N) {
    return @("-Modo", "cenarios", "-Saida", $Saida, "-Repeticoes", "$N", "-Nome", $NomeDaLeitura, "-Titulo", $Titulo)
}
function TextoDosArgumentos($Lista) {
    # os argumentos como se digitam: entre aspas os que tem espaco
    return (($Lista | ForEach-Object { if ("$_" -match "\s") { '"' + $_ + '"' } else { "$_" } }) -join " ")
}
function MinutosDoCusto([string]$Chave) {
    # a estimativa de minutos gravada por avaliar_fase5.py --custo; "?" quando o arquivo ou a chave faltam
    if (-not (Test-Path -LiteralPath $Custo)) { return "?" }
    $texto = [System.IO.File]::ReadAllText($Custo)
    if ($texto -match ('"' + $Chave + '"\s*:\s*(\d+)')) { return $Matches[1] }
    return "?"
}
function RamLivreGB {
    return [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 1)
}
# ! Alteracao de IA - Revisar: (18/11/2026) Residentes e DescarregarModelo chamam o ollama com a preferencia de erro em Continue, dentro de try.
# ! Motivo: com $ErrorActionPreference em Stop, o Windows PowerShell 5.1 trata como erro fatal qualquer linha que um comando nativo escreva no erro padrao quando ha
# redirecionamento (testado em 18/11/2026 com um comando que escreve no erro padrao e sai com 1: o script parava com RemoteException). O ollama stop de um modelo
# que ja nao esta carregado, ou o ollama ps com o servidor fora do ar, derrubaria a noite na conferencia, e nao pelo motivo de verdade.
function Residentes {
    $antes = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $saida = $null
    try { $saida = & ollama ps 2>$null } catch { $saida = $null }
    $ErrorActionPreference = $antes
    if (-not $saida) { return -1 }
    return ($saida | Measure-Object -Line).Lines - 1
}
function DescarregarModelo {
    # tira o modelo da memoria e confere pelo ollama ps; o que vale e a conferencia, porque o ollama stop reclama quando o modelo ja nao esta carregado
    $antes = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try { & ollama stop $Modelo 2>&1 | Out-Null } catch { }
    $ErrorActionPreference = $antes
    $espera = 0
    while ((Residentes) -gt 0 -and $espera -lt 15) { Start-Sleep -Seconds 2; $espera++ }
    if ((Residentes) -ne 0) { Parar "o modelo nao saiu da memoria depois do ollama stop, ou o Ollama nao responde (confira com ollama ps)" 2 }
}
function VersaoOllama {
    try { return (Invoke-RestMethod -Uri "http://localhost:11434/api/version" -TimeoutSec 10).version } catch { return "" }
}
function LinhasChaveValor($Linhas) {
    $dado = @{}
    foreach ($linha in $Linhas) {
        if ("$linha" -match "^([a-z_]+)=(.*)$") { $dado[$Matches[1]] = $Matches[2] }
    }
    return $dado
}
function SituacaoDaNoite {
    # as linhas chave=valor de avaliar_fase5.py --situacao: execucoes, esperadas, completa (sim ou nao), repeticoes_completas e versoes_ollama (a das execucoes ja gravadas)
    $linhas = & python @("avaliar_fase5.py", "--situacao")
    if ($LASTEXITCODE -ne 0) { Parar "avaliar_fase5.py --situacao saiu com erro" $LASTEXITCODE }
    return (LinhasChaveValor $linhas)
}
function SituacaoDaPonte {
    # as linhas chave=valor que experimento_sem_notas.py --ponte imprime: versao (a do Ollama no ar), falta (a pasta da ponte que falta), pareavel (sim, nao ou
    # vazio) e pasta (a pasta da ponte da versao no ar)
    $linhas = & python @("experimento_sem_notas.py", "--ponte")
    if ($LASTEXITCODE -ne 0) { Parar "experimento_sem_notas.py --ponte saiu com erro (o Ollama esta no ar?)" $LASTEXITCODE }
    return (LinhasChaveValor $linhas)
}
function GarantirPonte([string]$Corrida) {
    # regra R6: a corrida so vale com a ponte da versao do Ollama que esta no ar; e a mesma sequencia da fila rodar_fila_pre_fase5.ps1
    if ($Simular) {
        Simulado ("python experimento_sem_notas.py --ponte (antes da corrida {0}; se a ponte da versao faltar: rodar_fase3b.ps1 -Modo ponte e avaliar_fase4.py --pontes; depois testar_fase4.py --registrar-ponte)" -f $Corrida)
        return
    }
    $Ponte = SituacaoDaPonte
    $Falta = $Ponte["falta"]
    Passo ("antes da corrida {0}: Ollama {1}; ponte que falta: {2}" -f $Corrida, $Ponte["versao"], $(if ($Falta) { $Falta } else { "nenhuma" }))
    if ($Falta) {
        Passo ("ponte de versao (regra R6): rodar_fase3b.ps1 -Modo ponte -Saida {0}, de {1} a {2} minutos pelas tres ultimas" -f $Falta, (MinutosDoCusto "ponte_minutos_min"), (MinutosDoCusto "ponte_minutos_max"))
        & powershell -ExecutionPolicy Bypass -File ".\rodar_fase3b.ps1" -Modo ponte -Saida $Falta -Modelos qwen2.5:7b
        if ($LASTEXITCODE -ne 0) { Parar "rodar_fase3b.ps1 saiu com erro; relance o rodar_fase5.ps1 para retomar a ponte" $LASTEXITCODE }
        Passo "pontes.json regravado com a ponte nova"
        & python @("avaliar_fase4.py", "--pontes")
        if ($LASTEXITCODE -ne 0) { Parar "avaliar_fase4.py --pontes saiu com erro" $LASTEXITCODE }
        $Ponte = SituacaoDaPonte
        if ($Ponte["falta"]) { Parar ("a ponte {0} rodou mas nao entrou em pontes.json (nao cobriu os 36 casos?); veja resultados_alvo\{0}\fase3b.log" -f $Falta) 1 }
    }
    if ($Ponte["pareavel"] -eq "nao") {
        Parar ("a ponte da versao {0} do Ollama nao e pareavel com a Fase 3 (b + c acima de 2): o agente nao seria o da corrida 21d. A corrida {1} nao roda; a decisao volta ao Eric numa ficha, leve o resultado ao Claude" -f $Ponte["versao"], $Corrida) 1
    }
    # a ponte cria a pasta resultados_alvo\fase3b_ponte_<versao>, e a bateria que o rodar_fase4.ps1 roda antes da corrida compara as pastas fase3b_* com o registro
    # das areas so de leitura; testar_fase4.py --registrar-ponte so acrescenta essa pasta e recusa se outra area tiver mudado
    if ($Ponte["pasta"]) {
        Passo ("registro das areas so de leitura: testar_fase4.py --registrar-ponte {0}" -f $Ponte["pasta"])
        & python @("testar_fase4.py", "--registrar-ponte", $Ponte["pasta"])
        if ($LASTEXITCODE -ne 0) { Parar "testar_fase4.py --registrar-ponte recusou a pasta da ponte (outra area so de leitura mudou?). Nada mais roda; leve o resultado ao Claude" $LASTEXITCODE }
    }
}

$MinSemPonte = MinutosDoCusto "minutos_estimados_sem_ponte"
$MinComPonte = MinutosDoCusto "minutos_estimados_com_ponte"
Passo ("noite medida da Fase 5, a frio (corrida 28b): cerca de {0} minutos; ate {1} minutos se a ponte da versao do Ollama precisar rodar (pelos registros da corrida 21d, em resultados_alvo\fase5\custo.json){2}" -f $MinSemPonte, $MinComPonte, $(if ($Simular) { " (simulacao: nada roda)" } else { "" }))

# ---------------------------------------------------------------- etapa 1: memoria livre e nenhum modelo residente
Passo ("etapa 1 de 6: memoria livre de {0:N1} GB e nenhum modelo residente no Ollama" -f $RamMinimaGB)
if ($Simular) {
    Simulado ("esperar a memoria livre chegar a {0:N1} GB e conferir que nao ha modelo residente (ollama ps)" -f $RamMinimaGB)
} else {
    if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) { Parar "Ollama nao encontrado no PATH" 2 }
    if ((Residentes) -lt 0) {
        Passo "servidor do Ollama nao responde - iniciando"
        Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
        $espera = 0
        while ((Residentes) -lt 0 -and $espera -lt 30) { Start-Sleep -Seconds 2; $espera++ }
        if ((Residentes) -lt 0) { Parar "o Ollama nao subiu; abra o aplicativo Ollama e rode de novo" 2 }
    }
    if ((Residentes) -gt 0) {
        & ollama ps
        Parar "ha modelo residente no Ollama; regra do experimento: um modelo por vez (ollama stop <modelo>)" 2
    }
    $tentativas = 0
    while ((RamLivreGB) -lt $RamMinimaGB -and $tentativas -lt 20) {
        Passo ("memoria livre {0:N1} GB, a noite pede {1:N1} GB - feche o aplicativo Claude, o VS Code e o navegador; nova checagem em 30 s" -f (RamLivreGB), $RamMinimaGB)
        Start-Sleep -Seconds 30
        $tentativas++
    }
    if ((RamLivreGB) -lt $RamMinimaGB) { Parar ("memoria livre {0:N1} GB abaixo de {1:N1} GB depois de 10 minutos de espera; libere memoria e relance" -f (RamLivreGB), $RamMinimaGB) 2 }
    Passo ("memoria livre {0:N1} GB; nenhum modelo residente" -f (RamLivreGB))
}

# ---------------------------------------------------------------- etapa 2: o agente de hoje e o da corrida 21d
Passo "etapa 2 de 6: o agente de hoje e o da corrida 21d? (avaliar_fase5.py --antes, sem chamar o modelo; abre o navegador so para ler a versao)"
if ($Simular) {
    Simulado ("{0} avaliar_fase5.py --antes" -f $Venv)
} else {
    if (-not (Test-Path -LiteralPath $Venv)) { Parar ("venv do AgenteCore nao encontrada em {0} (rode install.py primeiro)" -f $Venv) 2 }
    & $Venv @("avaliar_fase5.py", "--antes")
    if ($LASTEXITCODE -ne 0) { Parar "avaliar_fase5.py --antes nao confirmou que o agente de hoje e o da corrida 21d (a tabela acima diz o que difere). A noite nao roda; leve o resultado ao Claude" $LASTEXITCODE }
}

# ---------------------------------------------------------------- etapa 3: a ponte da versao do Ollama (regra R6)
Passo "etapa 3 de 6: a ponte da versao do Ollama que esta no ar (regra R6)"
GarantirPonte "28b"

# ---------------------------------------------------------------- etapa 4: a corrida 28b, uma repeticao por vez, com o modelo descarregado entre elas
Passo ("etapa 4 de 6: corrida 28b (os dez cenarios com cinco repeticoes, 50 execucoes, uma repeticao por vez e a frio): cerca de {0} minutos" -f $MinSemPonte)
if ((ListaDeArgumentos 1) -notcontains "-Nome") { Parar "a lista de argumentos da corrida esta sem -Nome: a leitura do ensaio gravaria por cima da leitura da corrida 21" 2 }
if ($Simular) {
    Simulado "python avaliar_fase5.py --situacao (com as 50 execucoes ja gravadas a corrida nao roda de novo; se faltam, comeca na primeira repeticao incompleta)"
    Simulado "python avaliar_fase5.py --sondagem (a ultima sondagem do frio, de rodar_sondagem_frio.ps1, tem de ter passado, na versao do Ollama que esta no ar)"
    for ($N = 1; $N -le $Repeticoes; $N++) {
        Simulado ("ollama stop {0} (repeticao {1} de {2}: o modelo sai da memoria, para o prompt ser lido de novo)" -f $Modelo, $N, $Repeticoes)
        Simulado "ollama ps vazio e a versao do Ollama igual a das execucoes ja gravadas (avaliar_fase5.py --situacao)"
        Simulado ("powershell -ExecutionPolicy Bypass -File .\rodar_fase4.ps1 {0}" -f (TextoDosArgumentos (ListaDeArgumentos $N)))
    }
} else {
    # ! Alteracao de IA - Revisar: antes de chamar a corrida, o lancador pergunta a avaliar_fase5.py --situacao quantas execucoes e quantas repeticoes inteiras ja
    # estao gravadas na pasta nova; com a noite completa, a corrida nao e chamada de novo, e com repeticoes inteiras ja gravadas ele comeca na seguinte.
    # ! Motivo: a noite a frio e uma so (decisao 146). Relancar com as 50 gravadas faria o executor regravar condicoes_fase4.json da pasta da noite com a data e a
    # versao do Ollama do relancamento, como aconteceu no relancamento da corrida 25 em 16/11/2026; e chamar o executor para uma repeticao ja inteira so regravaria
    # as condicoes com um numero menor de repeticoes.
    $Noite = SituacaoDaNoite
    if ($Noite["completa"] -eq "sim") {
        Passo ("a noite ja esta completa ({0} de {1} execucoes em resultados_alvo\{2}): a corrida nao roda de novo; seguem a leitura e o painel" -f $Noite["execucoes"], $Noite["esperadas"], $Saida)
    } else {
        # ! Alteracao de IA - Revisar: sem a ultima sondagem do frio ter passado, na versao do Ollama que esta no ar, a noite nao comeca.
        # ! Motivo: a noite a frio so mede o que se quer se descarregar o modelo apagar o prompt que o Ollama guardou; e isso que o rodar_sondagem_frio.ps1 confere
        # em poucos minutos, antes de gastar a hora de maquina. A sondagem vale para a versao do Ollama em que foi feita.
        $Sondagem = LinhasChaveValor (& python @("avaliar_fase5.py", "--sondagem"))
        if ($LASTEXITCODE -ne 0) { Parar ("a sondagem do frio nao passou ou nao foi feita (situacao: {0}). Rode antes o rodar_sondagem_frio.ps1; se ele disser NAO PASSOU, a noite nao roda e o resultado vai ao Claude" -f $Sondagem["passou"]) 2 }
        $VersaoNoAr = VersaoOllama
        if (-not $VersaoNoAr) { Parar "o Ollama nao respondeu em /api/version" 2 }
        if ($Sondagem["versoes_ollama"] -ne $VersaoNoAr) { Parar ("a sondagem do frio ({0}) foi feita no Ollama {1}, e o que esta no ar e o {2}: rode o rodar_sondagem_frio.ps1 de novo" -f $Sondagem["pasta"], $Sondagem["versoes_ollama"], $VersaoNoAr) 2 }
        Passo ("sondagem do frio: passou ({0}, Ollama {1}); execucoes ja gravadas: {2} de {3}, {4} repeticao(oes) inteira(s)" -f $Sondagem["pasta"], $VersaoNoAr, $Noite["execucoes"], $Noite["esperadas"], $Noite["repeticoes_completas"])
        for ($N = [int]$Noite["repeticoes_completas"] + 1; $N -le $Repeticoes; $N++) {
            Passo ("repeticao {0} de {1}: o modelo sai da memoria (ollama stop), para o prompt ser lido de novo" -f $N, $Repeticoes)
            DescarregarModelo
            # decisao 44: uma noite so vale com uma versao do Ollama; a das execucoes ja gravadas tem de ser a que esta no ar
            $Noite = SituacaoDaNoite
            $VersaoNoAr = VersaoOllama
            if (-not $VersaoNoAr) { Parar "o Ollama nao respondeu em /api/version" 2 }
            if ($Noite["versoes_ollama"] -and ($Noite["versoes_ollama"] -ne $VersaoNoAr)) {
                Parar ("a versao do Ollama mudou entre as repeticoes: as execucoes ja gravadas sao do {0} e o que esta no ar e o {1}. NAO relance: a noite nao vale como medida (decisao 44), a pasta parcial vira incidente e a noite recomeca em pasta nova (plano, secao 3.3); leve ao Claude" -f $Noite["versoes_ollama"], $VersaoNoAr) 1
            }
            Passo ("repeticao {0} de {1}: ollama ps vazio, Ollama {2}; rodando as dez execucoes" -f $N, $Repeticoes, $VersaoNoAr)
            $ArgumentosDaRepeticao = ListaDeArgumentos $N
            & powershell -ExecutionPolicy Bypass -File ".\rodar_fase4.ps1" @ArgumentosDaRepeticao
            if ($LASTEXITCODE -ne 0) { Parar ("a repeticao {0} da corrida 28b (rodar_fase4.ps1 -Modo cenarios) saiu com erro. Se a mensagem acima diz que a versao do Ollama mudou, NAO relance e leve ao Claude (plano, secao 3.3); nos outros casos, relance o rodar_fase5.ps1 para retomar as execucoes que faltam" -f $N) $LASTEXITCODE }
        }
    }
}

# ---------------------------------------------------------------- etapa 5: a leitura por cenario
Passo "etapa 5 de 6: a leitura por cenario, pelas regras fixadas antes da noite, com a conferencia de que cada repeticao rodou a frio (avaliar_fase5.py --agente)"
if ($Simular) {
    Simulado "python avaliar_fase5.py --agente"
} else {
    & python @("avaliar_fase5.py", "--agente")
    if ($LASTEXITCODE -ne 0) { Parar "avaliar_fase5.py --agente nao gravou a leitura (a mensagem acima diz por que: a noite incompleta, ou alguma repeticao que nao rodou a frio). A corrida esta gravada em resultados_alvo\fase5_agente_b; leve o resultado ao Claude" $LASTEXITCODE }
}

# ---------------------------------------------------------------- etapa 6: o painel, uma vez, com as baterias dele
if (-not $SemPainel) {
    Passo "etapa 6 de 6: painel: regerar uma vez e rodar as cinco baterias dele"
    foreach ($Arquivo in @("gerar_dashboard.py", "testar_painel_textos.py", "testar_painel_topicos.py", "testar_painel_fases.py", "testar_painel_glossario.py", "testar_painel_grupo.py")) {
        $Caminho = Join-Path (Join-Path $Raiz "ferramentas") $Arquivo
        if ($Simular) {
            Simulado ("python {0}" -f $Caminho)
        } else {
            & python $Caminho
            if ($LASTEXITCODE -ne 0) { Parar ("{0} saiu com erro; a corrida e a leitura ja estao gravadas" -f $Arquivo) $LASTEXITCODE }
        }
    }
}

Passo "FIM da noite medida: a corrida em resultados_alvo\fase5_agente_b (log em fase4.log), a leitura do ensaio em resultados_alvo\fase4\cenarios_fase5b.{json,md} e a leitura por cenario em resultados_alvo\fase5\agente.{json,md}"
Passo "proxima sessao do Claude: avaliar_fase5.py --agente --colar e depois --check, conferir os blocos da noite e da conferencia a frio, registrar a corrida 28b no roadmap e republicar o painel; a comparacao com as pessoas sai depois das tres sessoes (avaliar_fase5.py --manual e --comparar)"
exit 0
