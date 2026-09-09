# ! Alteração de IA - Revisar: importa, nesta máquina, a memória do Claude Code e as regras do
# projeto trazidas de outra máquina - MESCLANDO com o que já existe aqui, sem sobrescrever.
# ! Motivo: a memória do Claude fica FORA do repositório, em
# %USERPROFILE%\.claude\projects\<slug>\memory\, e a pasta .claude\ do projeto está no
# .gitignore - nada disso viaja pelo git. A primeira versão deste script copiava por cima
# (-Force); a partir de 09/09/2026 a máquina-alvo passa a ser a principal e tem memória
# própria, então o pedido do Eric é ADICIONAR, nunca substituir. Regras: arquivo que não
# existe aqui e copiado; arquivo identico e ignorado; MEMORY.md (o indice) recebe as linhas
# que faltam; qualquer outro arquivo que exista com conteudo diferente e preservado, e a
# versao recebida fica ao lado como <nome>.recebido-<data>.md para o Claude/Eric conciliar.
# O <slug> e o caminho absoluto do repositorio com ':' e '\' trocados por '-' (ex.:
# c--Users-EricDerre-Documents-TCC), como o Claude Code nomeia a pasta do projeto; por isso
# e calculado a partir de onde o repositorio esta NESTA maquina.
#
# Uso (PowerShell, de qualquer pasta):
#   powershell -ExecutionPolicy Bypass -File claude-memoria\importar.ps1
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path.TrimEnd("\")
$slug = $repo -replace '[:\\/]', '-'
$slug = $slug.Substring(0, 1).ToLower() + $slug.Substring(1)
$carimbo = Get-Date -Format "yyyyMMdd-HHmm"
$utf8 = New-Object System.Text.UTF8Encoding($false)

function Ler($caminho) { return [System.IO.File]::ReadAllText($caminho, [System.Text.Encoding]::UTF8) }

function Mesclar($origem, $destino, $rotulo) {
    if (-not (Test-Path $destino)) {
        Copy-Item -Path $origem -Destination $destino
        Write-Host ("  novo      " + $rotulo)
        return
    }
    $a = Ler $origem
    $b = Ler $destino
    if ($a -eq $b) { Write-Host ("  igual     " + $rotulo); return }
    if ((Split-Path $destino -Leaf) -eq "MEMORY.md") {
        # Indice: uma linha por memoria. Acrescenta as linhas recebidas que ainda nao existem.
        $existentes = $b -split "`r?`n"
        $novas = @()
        foreach ($linha in ($a -split "`r?`n")) {
            if ($linha.Trim() -ne "" -and ($existentes -notcontains $linha)) { $novas += $linha }
        }
        if ($novas.Count -gt 0) {
            $texto = $b.TrimEnd("`r", "`n") + "`n" + ($novas -join "`n") + "`n"
            [System.IO.File]::WriteAllText($destino, $texto, $utf8)
            Write-Host ("  mesclado  " + $rotulo + " (+" + $novas.Count + " linha(s))")
        } else {
            Write-Host ("  mantido   " + $rotulo + " (ja continha tudo)")
        }
        return
    }
    $lado = [System.IO.Path]::ChangeExtension($destino, $null).TrimEnd(".") + ".recebido-" + $carimbo + ".md"
    Copy-Item -Path $origem -Destination $lado
    Write-Host ("  DIFERENTE " + $rotulo + " -> mantido o daqui; versao recebida em " + (Split-Path $lado -Leaf) + " para conciliar")
}

$destinoMemoria = Join-Path $env:USERPROFILE ".claude\projects\$slug\memory"
New-Item -ItemType Directory -Force -Path $destinoMemoria | Out-Null
Write-Host "Memoria -> ${destinoMemoria}:"
foreach ($arq in Get-ChildItem (Join-Path $PSScriptRoot "memory") -Filter *.md) {
    Mesclar $arq.FullName (Join-Path $destinoMemoria $arq.Name) $arq.Name
}

$destinoRegras = Join-Path $repo ".claude"
New-Item -ItemType Directory -Force -Path $destinoRegras | Out-Null
Write-Host "Regras -> ${destinoRegras}:"
Mesclar (Join-Path $PSScriptRoot "CLAUDE.md") (Join-Path $destinoRegras "CLAUDE.md") "CLAUDE.md"

Write-Host ""
Write-Host "Contexto das sessoes anteriores (leia na primeira sessao): claude-memoria\contexto\"
Write-Host "Abra o Claude Code na pasta $repo - a memoria deste projeto e lida do slug '$slug'."
