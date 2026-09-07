# ! Alteração de IA - Revisar: importa, nesta máquina, a memória do Claude Code e as regras do
# projeto (.claude\CLAUDE.md) trazidas do computador de desenvolvimento.
# ! Motivo: a memória do Claude fica FORA do repositório, em
# %USERPROFILE%\.claude\projects\<slug>\memory\, e a pasta .claude\ do projeto está no
# .gitignore - nada disso viaja pelo git. Sem importar, o Claude da máquina-alvo começa sem as
# decisões do projeto (LLM local, um modelo por vez, máquina-alvo, RESULTADOS_DIR) nem as
# regras de comentário e de commit. O <slug> é o caminho absoluto do repositório com ':' e '\'
# trocados por '-' (ex.: c--Users-EricDerre-Documents-TCC) - é assim que o Claude Code nomeia
# a pasta do projeto, e é por isso que o script calcula o slug a partir de onde o repositório
# está NESTA máquina, em vez de copiar o nome da pasta de origem.
#
# Uso (PowerShell, de qualquer pasta):
#   powershell -ExecutionPolicy Bypass -File claude-memoria\importar.ps1
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path.TrimEnd("\")
$slug = $repo -replace '[:\\/]', '-'
$slug = $slug.Substring(0, 1).ToLower() + $slug.Substring(1)

$destinoMemoria = Join-Path $env:USERPROFILE ".claude\projects\$slug\memory"
New-Item -ItemType Directory -Force -Path $destinoMemoria | Out-Null
Copy-Item -Path (Join-Path $PSScriptRoot "memory\*.md") -Destination $destinoMemoria -Force

$destinoRegras = Join-Path $repo ".claude"
New-Item -ItemType Directory -Force -Path $destinoRegras | Out-Null
Copy-Item -Path (Join-Path $PSScriptRoot "CLAUDE.md") -Destination (Join-Path $destinoRegras "CLAUDE.md") -Force

Write-Host "Memoria importada em ${destinoMemoria}:"
Get-ChildItem $destinoMemoria -Filter *.md | ForEach-Object { Write-Host ("  " + $_.Name) }
Write-Host "Regras do projeto copiadas para $destinoRegras\CLAUDE.md"
Write-Host "Abra o Claude Code na pasta $repo - a memoria desse projeto e lida do slug '$slug'."
