<!-- ! Alteração de IA - Revisar: pasta nova com a memória portátil do Claude Code e as regras
     do projeto, mais os scripts de importar/exportar.
     ! Motivo: a memória do Claude (decisões do projeto, regra de comentário, regra de commit)
     fica em %USERPROFILE%\.claude\projects\<slug>\memory\ e a pasta .claude\ do repositório
     está no .gitignore — nada disso chega à máquina-alvo pelo git. Esta pasta É versionada e
     carrega tudo; o importar.ps1 coloca cada coisa no lugar certo da máquina de destino. -->

# Memória do Claude — portátil entre máquinas

O que o Claude Code sabe deste projeto fica **fora do repositório**: na pasta de memória do usuário (`%USERPROFILE%\.claude\projects\<slug>\memory\`) e no `.claude\CLAUDE.md` do repositório, que o `.gitignore` deixa de fora. Esta pasta carrega os dois pelo git.

## Conteúdo

| Item | O que é |
|---|---|
| `memory\MEMORY.md` | Índice da memória (uma linha por arquivo). |
| `memory\project-tcc-agente-qa-decisoes.md` | Decisões de arquitetura que não se deduzem do código: LLM local, escopo do self-healing, dois alvos, **máquina-alvo i5 e `RESULTADOS_DIR`**, um modelo por vez em CPU. |
| `memory\feedback-comentar-alteracoes-ia-motivo.md` | Regra do comentário `! Alteração de IA - Revisar` + motivo. |
| `memory\feedback-eric-nunca-commitar.md` | Nunca commitar por conta própria; sem comando git destrutivo sem confirmação. |
| `CLAUDE.md` | As regras do projeto que o Claude lê ao abrir o repositório. |
| `plano-aprovado-fase-2b.md` | O plano da Fase 2-B aprovado em 03/09/2026 (desenho experimental, biblioteca, métricas, revisão de código). |

## Na máquina-alvo (importar)

```powershell
powershell -ExecutionPolicy Bypass -File claude-memoria\importar.ps1
```

O script descobre o caminho do repositório nesta máquina, calcula o `<slug>` que o Claude Code usa (o caminho com `:` e `\` trocados por `-`) e copia a memória para lá e o `CLAUDE.md` para `.claude\`. Depois, abra o Claude Code na pasta do repositório.

## Na máquina de desenvolvimento (exportar, quando a memória mudar)

```powershell
powershell -ExecutionPolicy Bypass -File claude-memoria\exportar.ps1
```

Copia a memória atual e o `CLAUDE.md` para cá; aí é só commitar.
