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
| `contexto\` | **Passagem de bastão entre sessões/máquinas**: o que não cabe na memória — como o harness está montado, armadilhas já pagas, estado das fases, próximas fases e o jeito de trabalhar. Um arquivo por sessão encerrada. O Claude deve ler o mais recente na primeira sessão numa máquina nova. |

## Na máquina de destino (importar — **adiciona, não substitui**)

```powershell
powershell -ExecutionPolicy Bypass -File claude-memoria\importar.ps1
```

O script descobre o caminho do repositório nesta máquina, calcula o `<slug>` que o Claude Code usa (o caminho com `:` e `\` trocados por `-`) e **mescla** com o que já existe lá: arquivo novo é copiado; arquivo idêntico é ignorado; o índice `MEMORY.md` recebe só as linhas que faltam; qualquer outro arquivo que exista com conteúdo diferente é **preservado**, e a versão recebida fica ao lado como `<nome>.recebido-<data>.md` para o Claude ou o Eric conciliarem. O mesmo vale para o `CLAUDE.md` em `.claude\`. Depois, abra o Claude Code na pasta do repositório e peça para ele ler `claude-memoria\contexto\`.

## Na máquina de desenvolvimento (exportar, quando a memória mudar)

```powershell
powershell -ExecutionPolicy Bypass -File claude-memoria\exportar.ps1
```

Copia a memória atual e o `CLAUDE.md` para cá; aí é só commitar.
