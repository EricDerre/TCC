# ! Alteração de IA - Revisar: exporta para esta pasta (versionada) a memória atual do Claude
# Code desta máquina e as regras do projeto, para levá-las a outra máquina pelo git.
# ! Motivo: é o caminho inverso do importar.ps1. Sem ele, cada máquina acumula memória própria
# e as decisões registradas numa não chegam à outra. Rodar antes de commitar quando a memória
# tiver mudado (o Claude avisa quando grava uma memória nova).
#
# Uso (PowerShell, de qualquer pasta):
#   powershell -ExecutionPolicy Bypass -File claude-memoria\exportar.ps1
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path.TrimEnd("\")
# ! Alteração de IA - Revisar: troca a regex do slug de '[:\\/]' para '[^A-Za-z0-9]', igual ao
# importar.ps1.
# ! Motivo: o Claude Code troca TODO caractere nao alfanumerico por '-' ao nomear a pasta do
# projeto em %USERPROFILE%\.claude\projects\; a regex antiga so cobria ':' e '\' e deixava o
# '.' de "Eric.Derre" intacto, calculando um slug (`c--Users-Eric.Derre-Documents-TCC`)
# diferente do real (`c--Users-Eric-Derre-Documents-TCC`) - a memoria exportada por este
# script saia da pasta errada. Confirmado em 11/09/2026.
$slug = $repo -replace '[^A-Za-z0-9]', '-'
$slug = $slug.Substring(0, 1).ToLower() + $slug.Substring(1)

$origemMemoria = Join-Path $env:USERPROFILE ".claude\projects\$slug\memory"
if (-not (Test-Path $origemMemoria)) { throw "Nao ha memoria do Claude para este repositorio em $origemMemoria" }
New-Item -ItemType Directory -Force -Path (Join-Path $PSScriptRoot "memory") | Out-Null
Copy-Item -Path (Join-Path $origemMemoria "*.md") -Destination (Join-Path $PSScriptRoot "memory") -Force
Copy-Item -Path (Join-Path $repo ".claude\CLAUDE.md") -Destination (Join-Path $PSScriptRoot "CLAUDE.md") -Force

Write-Host "Exportado de ${origemMemoria}:"
Get-ChildItem (Join-Path $PSScriptRoot "memory") -Filter *.md | ForEach-Object { Write-Host ("  " + $_.Name) }
Write-Host "Regras do projeto copiadas de $repo\.claude\CLAUDE.md"
Write-Host "Agora e so commitar a pasta claude-memoria\ e, na outra maquina, rodar importar.ps1."
