<!-- ! Alteração de IA - Revisar: regra de comentário expandida (agora exige "o quê" + "motivo") e registro da convenção de nomes deste repo. -->
<!-- ! Motivo: a versão anterior pedia só a tag `! Alteração de IA - Revisar` solta, o que deixava 8 arquivos com marcador cru e sem contexto — quem revisasse teria de reabrir a investigação para entender o porquê de cada mudança. -->

# Regras do projeto (TCC - Agente de QA E2E)

## O que NÃO fazer

- **Nunca commitar por conta própria.** O Eric commita ele mesmo; deixe as alterações no working tree. Operações que só mexem no índice (`git rm --cached`, `git add`) também preparam o commit dele — ofereça e explique, não execute por conta própria.
- **Nunca usar `git push --force`, `git reset --hard`, ou outro comando destrutivo** sem confirmação explícita. Antes de qualquer comando que possa descartar trabalho, rode `git status` e avise.
- **Antes de escrever SQL, confira as colunas reais das tabelas** (não assuma nomes por convenção).

## Comentar alterações de IA (o quê + motivo)

Todo código/arquivo criado ou alterado por IA leva a tag `! Alteração de IA - Revisar` — e **ela nunca fica sozinha**. Sempre acompanhada de:

1. **O que foi feito** — na mesma linha da tag.
2. **O motivo** — linha seguinte, começando com `! Motivo:`: qual era o defeito/sintoma anterior e por que a forma escolhida resolve com segurança.

Formato:

```python
# ! Alteração de IA - Revisar: passa a criar o venv chamando `python -m venv` como subprocesso.
# ! Motivo: rodando de dentro do Cobaia.exe (PyInstaller), venv.EnvBuilder falhava ao copiar
# venvlauncher.exe — o interpretador embutido não tem o layout de uma instalação normal.
```

Regras de escrita:
- Linguagem técnica, mas **amarrada ao processo real**, não ao conceito. Cite a função/fluxo afetado, a tabela, a tela ou a mensagem de erro real.
- **Sem jargão teórico**: nada de "guard-rail", "race condition", "snapshot", "last writer wins". Descreva o que acontece.
- **Código de situação/domínio sempre com o significado junto**, na primeira menção do bloco — ex.: `status 'Em Análise'` / `'Cancelado'` em `tbpedido_reserva`.
- O comentário precisa fazer sentido lido isolado no código, sem depender do chat.
- Vale para arquivo novo, linha alterada e variável/declaração acrescentada.
Sintaxe por linguagem: `#` (Python, shell, PowerShell, YAML) · `//` (PHP, JS) · `--` (SQL) · `<!-- -->` (HTML, Markdown) · `rem` (batch). Em Python, a docstring de módulo logo abaixo da tag também serve como explicação.

**Exceções (não recebem tag):**
- Arquivo vazio de propósito (`__init__.py` de 0 byte) — marcar quebraria a vazidade.
- Binário (`Cobaia.exe`) — fica coberto pela tag no fonte que o gera (`Cobaia.py`).
- Arquivo regenerado por ferramenta (`Cobaia.spec`, reescrito pelo PyInstaller a cada `build_exe.ps1`) — a tag seria apagada no próximo build; fica coberta pela tag no `build_exe.ps1`.

**Caso especial `.cmd`/`.bat`:** usar o marcador **sem acento** (`! Alteracao de IA - Revisar`). Testado: o `cmd.exe` lê o arquivo na codepage OEM e os bytes UTF-8 de `ç`/`ã` re-tokenizam a linha `rem`, fazendo o script imprimir um erro espúrio antes de rodar. Por isso, ao procurar marcadores no repositório, buscar por **`de IA - Revisar`** (trecho comum às duas formas).

**Caso especial `.ps1`:** gravar sempre em **UTF-8 com BOM** e, nas strings, usar `-` em vez do travessão `—`. Testado em 07/09/2026: o Windows PowerShell 5.1 lê `.ps1` sem BOM na codepage ANSI, e o travessão (bytes E2 80 94) vira `â€”`, em que o byte 94 é `”` — aspas de fechamento válidas para o PowerShell —, encerrando a string no meio e quebrando o parse do arquivo inteiro ("Token 'feche' inesperado"). A ferramenta de escrita da IA grava sem BOM; conferir com `[System.IO.File]::ReadAllBytes` (primeiros bytes EF BB BF).

## Convenção de nomes neste repositório

- **Python: PEP8 snake_case** (`find_php`, `ensure_mariadb_running`, `apply_fault`) — é o que o ruff configurado espera e o que todo o código atual usa.
- **PHP: o padrão do código legado** (`$row_produtos`, `id_produto`).
- A convenção CamelCase com prefixo húngaro (`nuLinhasReservadas`, `strComando`, `FunEstornaReservaTransf`) é **do projeto ERP, não deste repositório** — não usar aqui.

## Preferências de execução

- Ao investigar um bug ou comportamento inesperado, prefira achar e corrigir a causa raiz a aplicar um contorno "bom o suficiente", mesmo que custe mais iteração.

<!-- ! Alteração de IA - Revisar: seção "Economia de tokens" acrescentada em 21/09/2026 (regras do plano complementar).
     ! Motivo: quatro sessões da Fase 3 caíram por limite de tokens; o Eric pediu que tudo que a máquina resolve (buscas, contagens, scripts) rode localmente e que o modelo só receba o resumo. -->
## Economia de tokens (regra do Eric, 21/09/2026)

- **Primeiro a máquina, depois o modelo**: busca, contagem, render de tabela, dedup, conciliação, medição e verificação rodam em script local (`ferramentas/`, Python padrão), mesmo que demorem; o modelo lê só o resumo.
- Não há GPU utilizável (Intel UHD integrada, sem CUDA): "processamento local" é CPU; nunca usar LLM local como auxiliar durante uma bateria do TCC.
- Saídas longas passam pelo hook `ferramentas/gancho_pre_bash.py` → `resumir_saida.py`; não colar JSON de resultados em prompt — agentes leem arquivos.
- Modelo, `/effort` e plugins/MCP fixados no início da sessão (cache de prefixo); `/clear` entre pacotes; `/rewind` antes de `/compact`.
- Subagentes: Sonnet/Haiku no trabalho mecânico e nas verificações de citação; um revisor por entregável; ondas ≤ 30 agentes; nunca dois Workflows ao mesmo tempo; agentes relatam só falhas e contagens.
- Regras por tipo de arquivo vivem em `.claude/rules/` (este arquivo fica abaixo de 200 linhas).
- Medir antes/depois com `python ferramentas/medir_tokens.py` e registrar em `Documentacao/memorial/5-metodo-e-ferramental/`.
