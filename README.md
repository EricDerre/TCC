<!-- ! Alteração de IA - Revisar: documento inteiro gerado por IA (arquitetura, instalação,
     uso, decisões técnicas e problemas conhecidos do ambiente cobaia).
     ! Motivo: o repositório não tinha nenhuma documentação — quem clonasse não teria como
     saber que o CobaiaFront depende das extensões mbstring/output_buffering do PHP, que o
     banco é compartilhado entre os dois alvos, nem quais bugs foram deixados de propósito.
     Cada afirmação técnica aqui foi verificada executando, não deduzida do código. -->

# TCC — Agente de QA E2E Autônomo — Ambiente "Cobaia"

Este repositório contém o ambiente-alvo ("cobaia") usado para validar o
**Agente de QA End-to-End (E2E) Autônomo com Capacidades de Self-Healing**,
projeto de pesquisa do curso de Ciência da Computação da UNICID. A
fundamentação teórica completa está em
[`Documentacao/Projeto de Pesquisa - ABNT 15287_2025 - V3.md`](Documentacao/Projeto%20de%20Pesquisa%20-%20ABNT%2015287_2025%20-%20V3.md).

Este README documenta o **ambiente cobaia** (`Programacao/CobaiaFront`
+ `Programacao/CobaiaAPI`) e, na seção "AgenteCore — experimentos", a
biblioteca de documentação e a bateria de avaliação dos modelos locais que
já existem em `Programacao/AgenteCore`.

<!-- ! Alteração de IA - Revisar: a frase sobre o agente ainda não implementado passa a apontar
     para a Fase 4 (nome oficial da etapa, decisão nº 29 do plano aprovado da Fase 3).
     ! Motivo: a frase antiga ("ainda não foi implementado", sem mais contexto) ficou
     desatualizada depois que a Fase 3 (biblioteca gerida pelo próprio modelo) começou a ser
     implementada em cima da Fase 2-B; sem apontar a fase certa, o README dava a entender que
     nada tinha avançado desde a Fase 2-B. -->
<!-- ! Alteração de IA - Revisar: em 12/09/2026 "em implementação (Fase 3)" passou a "implementado,
     com piloto executado e bateria por rodar (Fase 3)".
     ! Motivo: os oito scripts da Fase 3 foram concluídos e revisados em 11–12/09/2026 e o piloto
     `rodar_fase3.ps1 -Piloto` rodou em 12/09; "em implementação" passou a descrever um estado
     que não existe mais, e o que ainda falta é a bateria completa (~60 h), não código. -->
O agente em si (interceptador, poda da árvore de acessibilidade, cura de
seletor) é a **Fase 4** do projeto, ainda não iniciada — ver a seção
"AgenteCore — experimentos com os modelos locais" para o que já está pronto
(Fase 2-B) e implementado, com piloto executado e bateria por rodar (Fase 3).

## Índice

- [Por que dois alvos](#por-que-dois-alvos)
- [Arquitetura](#arquitetura)
- [Stack técnica](#stack-técnica)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como rodar](#como-rodar)
- [Cobaia.exe — instalação + run + navegador em 1 clique](#cobaiaexe--instalação--run--navegador-em-1-clique)
- [Navegador recomendado para o agente](#navegador-recomendado-para-o-agente)
- [CobaiaFront — detalhes](#cobaiafront--detalhes)
- [CobaiaAPI — detalhes](#cobaiaapi--detalhes)
- [Testes e lint](#testes-e-lint)
- [O que é versionado e por quê](#o-que-é-versionado-e-por-quê)
- [Decisões técnicas e problemas resolvidos](#decisões-técnicas-e-problemas-resolvidos)
- [Problemas conhecidos (deixados de propósito)](#problemas-conhecidos-deixados-de-propósito)
- [Segurança](#segurança)
- [Troubleshooting](#troubleshooting)
- [Convenções para alterações por IA](#convenções-para-alterações-por-ia)

## Por que dois alvos

O núcleo da pesquisa é detectar **Contract Drift** (deriva de contrato) na
fronteira de integração Front-to-Back. Um site PHP+MySQL clássico, que
renderiza tudo no servidor, não tem essa fronteira — não há nenhuma
requisição JSON pra interceptar. Por isso o ambiente cobaia tem **dois
alvos**, deliberadamente separados:

| Alvo | O quê | Serve pra testar |
|---|---|---|
| **CobaiaFront** | Site PHP+MySQL legado e monolítico (cedido por um integrante do grupo), mantido **100% intocado** no código | Interceptação de requisições de página completa, erros PHP/SQL clássicos, sistemas legados sem API |
| **CobaiaAPI** + a aba "PRODUTOS (API)" dentro do próprio CobaiaFront | API JSON nova (Python/FastAPI), com mecanismo de injeção de falhas controlada | Contract Drift em contratos JSON reais — o foco principal do agente |

Os dois compartilham o **mesmo banco de dados** (`ti93phpdb01`) — uma
reserva criada por um dos lados aparece no outro. Isso evita dados
inconsistentes entre os alvos e simula um cenário realista (um backend,
dois clientes diferentes o consumindo).

## Arquitetura

```
                     ┌─────────────────────────────┐
   navegador  ─────► │  CobaiaFront (PHP 8.2)        │
                     │  php -S localhost:8080        │
                     │  produtos_api.php  ──fetch──┐ │
                     └──────────────┬───────────────┘ │
                                    │ mysqli           │ HTTP/JSON
                                    ▼                  ▼
                     ┌─────────────────────────────────────┐
                     │      MariaDB — banco ti93phpdb01      │
                     │  (root sem senha, único pra os dois)  │
                     └─────────────────────────────────────┘
                                    ▲
                                    │ SQLAlchemy + PyMySQL
                     ┌──────────────┴───────────────┐
   navegador/agente ─────► │  CobaiaAPI (FastAPI)          │
                     │  uvicorn localhost:8000       │
                     └────────────────────────────────┘
```

`run.py` sobe os três processos (PHP, MariaDB, uvicorn) juntos.
`install.py` cuida da instalação/configuração de tudo antes disso.

## Stack técnica

### CobaiaFront
- **Linguagem/execução:** PHP 8.2, servidor embutido (`php -S`) — sem
  Apache/Nginx (o projeto não usa `.htaccess`/mod_rewrite, então o servidor
  embutido é suficiente e muito mais simples de automatizar).
- **Banco:** MariaDB via extensão `mysqli`, sem ORM, queries diretas.
- **Frontend:** Bootstrap 3, jQuery, um pouco de AngularJS 1.6.9 (área do
  cliente), tudo via CDN ou vendorizado em `css/`/`js/`.
- **Email:** PHPMailer 5.2.27 (vendorizado, `PHPMailer/`), SMTP.
- **Extensões PHP obrigatórias:** `mysqli`, `pdo_mysql`, `mbstring` (ver
  [Decisões técnicas](#decisões-técnicas-e-problemas-resolvidos)).

### CobaiaAPI
- **Linguagem/execução:** Python 3.12+ (testado em 3.14), FastAPI + Uvicorn.
- **Banco:** SQLAlchemy 2.0 (estilo `Mapped`/`mapped_column`) + PyMySQL,
  apontando pro **mesmo** MariaDB do CobaiaFront.
- **Validação:** Pydantic v2 (schemas em `app/schemas.py`).
- **Config:** `pydantic-settings`, lida de `.env` (ver `.env.example`).
- **Testes:** pytest + `fastapi.testclient` (roda contra o banco real).
- **Lint:** ruff.

### Infraestrutura / instalador
- **Windows:** PHP e MariaDB instalados via `winget`
  (`PHP.PHP.8.2`, `MariaDB.Server`).
- **Linux:** `apt-get install php php-mysql mariadb-server`.
- **macOS:** `brew install php mariadb`.
- Todo o resto (schema, seed, venv, dependências Python) é feito por
  `install.py`, que roda igual nos três sistemas.

## Estrutura do repositório

```
TCC/
├── Cobaia.exe                               # Windows: instala + roda + abre o navegador, tudo em 1
├── Cobaia.py / build_exe.ps1 / Cobaia.spec  # fonte do Cobaia.exe e script pra recompilar
├── install.cmd / install.ps1 / install.sh / install.py   # instalador (chamado por Cobaia.exe também)
├── run.cmd / run.ps1 / run.sh / run.py                   # sobe CobaiaFront + CobaiaAPI juntos
├── _env_common.py                          # helpers compartilhados por install.py/run.py/Cobaia.py
├── .claude/                                # CLAUDE.md, settings.json (hooks, permissões), rules/ e skills/ do Claude Code — versionados; só settings.local.json fica fora
├── ferramentas/                            # scripts locais de apoio ao trabalho com IA: medição de tokens, resumo de saídas, conferência da documentação, pesquisa
├── claude-memoria/                         # memória do Claude + CLAUDE.md portáteis, com importar/exportar.ps1
├── Documentacao/                           # projeto de pesquisa (ABNT) do TCC e memorial de desenvolvimento
└── Programacao/
    ├── AgenteCore/
    │   ├── base_conhecimento/              # biblioteca de documentação do cobaia (Fase 2-B)
    │   │   ├── negocio/ contratos/ erros/ falhas_injetadas/ defeitos_conhecidos/
    │   │   └── INDICE.md                   # gerado por validar_banco.py --indice
    │   ├── experimentos/                   # bateria de avaliação dos modelos locais (ver seção abaixo)
    │   └── requirements.txt
    ├── CobaiaFront/                        # site PHP legado ("Churrascaria Fornalha")
    │   ├── banco/
    │   │   ├── bancoatualizado.sql         # schema original (tipos, produtos, usuários)
    │   │   ├── schema_completo.sql         # completa o schema (reservas, nível 'cli')
    │   │   └── seed.sql                    # dados de demonstração
    │   ├── admin/                          # painel admin (CRUD produtos/tipos/usuários)
    │   ├── cliente/                        # área do cliente (reservas)
    │   ├── conn/connect.php                # conexão MySQL (intocado)
    │   └── produtos_api.php                # NOVO: página que consome a CobaiaAPI via fetch
    └── CobaiaAPI/
        ├── app/
        │   ├── main.py                     # app FastAPI, CORS, routers
        │   ├── config.py                   # Settings via .env
        │   ├── database.py                 # engine/session SQLAlchemy
        │   ├── models.py                   # ORM nas MESMAS tabelas do CobaiaFront
        │   ├── schemas.py                  # contratos Pydantic (só p/ doc OpenAPI)
        │   ├── fault_injection.py          # mecanismo de injeção de falhas
        │   └── routers/{produtos,pedidos,admin_fault}.py
        ├── tests/
        ├── requirements.txt / requirements-dev.txt
        └── .env.example
```

## Pré-requisitos

- Windows 10/11, Linux ou macOS.
- Conexão com a internet (o instalador baixa PHP/MariaDB/pacotes Python se
  não estiverem instalados).
- **Windows:** `winget` (já vem no Windows 10 2004+/11). Não precisa rodar
  como Administrador para PHP; a instalação do MariaDB Server foi testada
  com sucesso **sem** elevação também.
- **Linux:** `sudo` disponível (`apt-get`), distro baseada em Debian/Ubuntu.
- **macOS:** [Homebrew](https://brew.sh) instalado.

Nada precisa ser pré-instalado manualmente além disso — o instalador cuida
do PHP, do MariaDB e do Python/venv.

## Instalação

No Windows, `Cobaia.exe` já faz instalação + run + abrir o navegador em um
só passo — ver [seção dedicada](#cobaiaexe--instalação--run--navegador-em-1-clique)
abaixo. O resto desta seção documenta o instalador "por partes"
(`install.*`), útil pra rodar só a instalação sem subir os serviços, ou no
Linux/macOS.

Um único comando, na raiz do repositório:

```
# Windows — clique duplo em install.cmd, ou pelo terminal:
install.cmd
```
```bash
# Linux / macOS
./install.sh
```

No Windows, use `install.cmd` (não `install.ps1` diretamente) — ele evita o
erro comum de *Execution Policy* do PowerShell (ver
[Troubleshooting](#troubleshooting)) sem precisar mudar nenhuma
configuração do sistema. `install.cmd` só chama `install.ps1` por baixo.

O que ele faz, em ordem (idempotente — pode rodar de novo a qualquer hora
sem duplicar nada):

1. Garante que existe Python 3 (instala via winget/apt/brew se faltar).
2. Instala PHP 8.2 se não encontrar (`winget`/`apt`/`brew`).
3. Instala MariaDB Server se não encontrar, e garante que está rodando —
   no Windows, como processo direto (não há serviço registrado, ver
   [Decisões técnicas](#decisões-técnicas-e-problemas-resolvidos)); no
   Linux/macOS, via `systemctl`/`brew services`.
4. Garante que o usuário `root` do banco está acessível sem senha (o que
   `Programacao/CobaiaFront/conn/connect.php`, intocado, espera).
5. Aplica, em ordem: `bancoatualizado.sql` → `schema_completo.sql` →
   `seed.sql`.
6. Cria o venv em `Programacao/CobaiaAPI/.venv` e instala as dependências
   (`requirements-dev.txt`, que já inclui as de produção).
7. **Se o `AgenteCore` já estiver implementado**, prepara também o ambiente
   do agente: venv próprio, dependências, o Chromium do Playwright, o Ollama
   e o download do modelo. Enquanto o `AgenteCore` estiver vazio, esse passo
   é pulado com uma mensagem — de propósito, para que quem só quer rodar o
   site não baixe alguns GB de navegador e modelo sem precisar.

Se algo faltar automatizar no seu SO específico, o script imprime uma
mensagem clara em vez de travar silenciosamente.

## Como rodar

```
# Windows — clique duplo em run.cmd, ou pelo terminal:
run.cmd
```
```bash
# Linux / macOS
./run.sh
```

Isso sobe os três processos (MariaDB se ainda não estiver rodando, PHP,
uvicorn) e imprime:

- **CobaiaFront:** http://localhost:8080
- **CobaiaAPI (docs interativas):** http://localhost:8000/docs

`Ctrl+C` encerra tudo.

### Contas de teste (já vêm no `seed.sql`)

| Login | Senha | Nível | Uso |
|---|---|---|---|
| `admin` | `admin123` | `sup` | Painel admin (`/admin/login.php`) — CRUD de produtos/tipos/usuários |
| `11122233344` | `123456` | `cli` | Área do cliente (`/admin/login.php`, mesmo formulário) — reservas |

14 produtos de exemplo já vêm cadastrados.

## Cobaia.exe — instalação + run + navegador em 1 clique

No Windows, `Cobaia.exe` (raiz do repositório) faz tudo de uma vez: roda a
instalação completa (idempotente — se já estiver tudo instalado, só
confirma e segue), sobe CobaiaFront + CobaiaAPI, e abre as duas URLs no
navegador padrão assim que os serviços respondem. É o jeito mais direto de
usar o projeto — inclusive pra demonstrar ao vivo no dia da banca.

```
# duplo clique em Cobaia.exe, ou pelo terminal:
.\Cobaia.exe
```

Fecha a janela (ou `Ctrl+C`) pra encerrar tudo (PHP, MariaDB, uvicorn).

**Sobre o aviso do Windows Defender/SmartScreen:** `Cobaia.exe` não é
assinado digitalmente (certificado de assinatura de código custa dinheiro e
não faz sentido pra um projeto acadêmico) — é esperado que o Windows mostre
"Windows protegeu seu PC" na primeira execução em uma máquina nova. Clique
em "Mais informações" → "Executar assim mesmo". O `.exe` é gerado a partir
do código-fonte deste mesmo repositório (`Cobaia.py`), sem nenhuma
dependência externa além do que já está documentado aqui.

**Reproduzindo/atualizando o `.exe`:** ele não se autoatualiza — depois de
mudar `Cobaia.py`, `install.py`, `run.py` ou `_env_common.py`, rode:
```powershell
.\build_exe.ps1
```
Isso usa [PyInstaller](https://pyinstaller.org) (instalado num venv
temporário só pra compilar, separado do venv da CobaiaAPI) e regrava
`Cobaia.exe` na raiz. **Importante:** o `.exe` empacota um interpretador
Python só pra rodar a lógica de orquestração (winget/pip/php/uvicorn) — ele
**não** usa esse interpretador embutido pra criar o venv da CobaiaAPI, isso
quebra (testado ao vivo: o layout do Python embutido no PyInstaller não é o
de uma instalação normal, faltam os arquivos que o módulo `venv` espera
copiar). Por isso, quando rodando como `.exe`, a criação do venv busca (ou
instala via winget, se faltar) um Python "de verdade" no sistema e delega a
criação pra ele via subprocesso — ver `find_or_install_real_python()` em
`_env_common.py`. As dependências da CobaiaAPI continuam indo exclusivamente
pra `Programacao/CobaiaAPI/.venv`, nunca pro ambiente do `.exe`.

Nos scripts (`install.cmd`/`.ps1`/`.sh`, sem ser via `.exe`), isso nem entra
em jogo — `sys.executable` ali já é um Python real, porque foi ele mesmo
quem rodou o script.

## Navegador recomendado para o agente

Esta pergunta é sobre qual navegador o **futuro `AgenteCore`** deve
automatizar (via Playwright) pra interceptar rede/coletar erros — não afeta
o CobaiaFront/CobaiaAPI em si, que funcionam em qualquer navegador
(Bootstrap 3 + jQuery + `fetch()`, nada específico de motor).

**Recomendação: o Chromium que o próprio Playwright baixa e fixa
(`playwright install chromium`), rodando headless — não o Chrome/Edge
instalado no sistema.**

O motor é Chromium em qualquer um dos casos; a diferença é *qual build*.
Motivos, considerando que o projeto precisa rodar em Windows **e Linux**, de
graça e localmente:

- **Reprodutibilidade dos resultados (o argumento decisivo pra um TCC).** A
  pesquisa mede MTTR e Task Success. O Chrome/Edge do sistema se
  autoatualiza sozinho e é diferente na máquina de cada um dos 9
  integrantes — dois runs do mesmo experimento podem cair em versões
  diferentes do navegador. O Playwright **fixa uma build exata de Chromium
  por versão do Playwright**: todo mundo (e a banca, meses depois) roda
  exatamente o mesmo motor.
- **Mesmo comando nos dois SOs.** `playwright install chromium` é idêntico
  em Windows e Linux e cabe direto no instalador. Usar o Chrome do sistema
  exigiria um caminho de instalação por SO (winget no Windows, repositório
  `.deb`/`.rpm` no Linux) — mais peças pra dar errado no "hit and run".
  No Linux, `playwright install --with-deps chromium` ainda instala
  sozinho as libs de sistema que o headless precisa (libnss3, libgbm1 etc.).
- **Não depende do que está instalado.** Máquina corporativa pode ter
  Chrome antigo, travado por política, ou nenhum.
- **Profundidade de interceptação:** o Chromium é o motor "de origem" do
  Playwright (boa parte da equipe veio do Puppeteer/Chrome DevTools) — os
  hooks de rede (`page.on('request'/'response')`, `route()`, corpo via
  `response.body()`) são os mais maduros ali, comparado ao wrapper usado
  para Firefox (Juggler) ou WebKit.
- **Headless** é o modo mais testado do mercado inteiro de automação —
  exatamente o que o agente precisa pra rodar em segundo plano.

**Alternativa (uma linha de diferença):** se em alguma máquina o download
de ~150 MB for um problema, ou se a política de TI só permitir binário já
homologado, dá pra apontar pro Chrome instalado com
`browser_type.launch(channel="chrome")` — funciona em Windows e Linux e não
muda mais nada no código. Só perde a garantia de versão fixa. (`channel="msedge"`
existe também, mas aí a portabilidade pro Linux fica pior, já que o Edge não
é padrão lá — por isso não é a recomendação.)

**WebKit/Firefox** não agregam aqui: não há necessidade de validar
comportamento de Safari, e o Firefox tem hooks de rede menos ricos no
Playwright.

Detalhe à parte: o navegador que o `webbrowser.open()` do `Cobaia.exe` abre
(nesta máquina, Firefox — o seu padrão) é só conveniência pra você olhar o
site, **não tem relação nenhuma** com qual navegador o `AgenteCore` vai
automatizar depois — o Playwright sempre sobe sua própria instância
isolada, independente do navegador padrão do sistema.

## CobaiaFront — detalhes

Site de restaurante ("Churrascaria Fornalha"): cardápio público, busca de
produtos, formulário de contato (PHPMailer), painel admin com CRUD
completo, e área de cliente com reservas.

Rotas principais:
- `/index.php` — home (destaques + produtos + carrossel)
- `/produtos_busca.php?buscar=X`, `/produtos_por_tipo.php?id_tipo=X`,
  `/produto_detalhes.php?id_produto=X`
- `/produtos_api.php` — **nova**, consome a CobaiaAPI via `fetch()`
- `/admin/login.php` → `/admin/index.php` (CRUD produtos/tipos/usuários)
- `/admin/login.php` → `/cliente/index.php?cliente=<login>` (reservas)

O código PHP em si não foi alterado, exceto um link novo de navegação em
`menu_publico.php` (marcado com `! Alteração de IA - Revisar`) apontando
pra `produtos_api.php`.

## CobaiaAPI — detalhes

Documentação interativa (Swagger UI) sempre disponível em
`http://localhost:8000/docs` enquanto o servidor estiver rodando.

| Endpoint | Método | Descrição |
|---|---|---|
| `/api/produtos` | GET | Lista todos os produtos |
| `/api/produtos/{id}` | GET | Detalhe de um produto (404 se não existir) |
| `/api/pedidos?login=<cpf>` | GET | Reservas de um cliente |
| `/api/pedidos` | POST | Cria reserva — `{id_clientes, pessoas, data_pedido}` |
| `/api/pedidos/{id}/cancelar` | POST | Cancela uma reserva |
| `/api/admin/fault-mode` | GET/POST | Liga/desliga modos de falha (ver abaixo) |

### Injeção de falhas (fault injection)

Mecanismo pensado pra viabilizar Fuzzing/Mutação Dinâmica contra a
CobaiaAPI — o agente de QA precisa de um jeito determinístico e
reproduzível de provocar falhas conhecidas.

```bash
curl -X POST http://localhost:8000/api/admin/fault-mode \
  -H "Content-Type: application/json" \
  -H "X-Admin-Token: troque-isto-localmente" \
  -d '{"mode": "type_drift", "target_field": "preco"}'
```

Modos disponíveis (`mode`):

| Modo | Efeito |
|---|---|
| `normal` | Comportamento padrão (default) |
| `error_500` | Responde HTTP 500 |
| `latency` | Atraso artificial de 2s antes de responder |
| `type_drift` | Muda o tipo do campo `target_field` (ex.: número → string) |
| `field_missing` | Remove `target_field` da resposta |
| `field_renamed` | Renomeia `target_field` para `<campo>_v2` |
| `malformed_json` | Responde um corpo JSON sintaticamente quebrado |

`probability` (0.0–1.0, default 1.0) controla a chance da falha disparar
por requisição — útil pra simular intermitência.

<!-- ! Alteração de IA - Revisar: documenta o modo de ativação por variável de ambiente.
     ! Motivo: só FAULT_MODE era lido do .env; sem FAULT_TARGET_FIELD os modos com
     campo-alvo não faziam nada no boot. Corrigido em app/config.py, e o README precisa
     dizer como usar, porque é o caminho das execuções determinísticas da Fase 5. -->
Para subir a API **já em modo de falha** (execuções determinísticas, sem
chamar o endpoint admin), defina no `.env`:

```
FAULT_MODE=type_drift
FAULT_TARGET_FIELD=preco
```

O token (`X-Admin-Token`) vem de `ADMIN_TOKEN` no `.env` (veja
`.env.example`); sem o header correto, o endpoint responde 403.

**Detalhe técnico importante:** as rotas montam a resposta como `dict` puro
e retornam via `JSONResponse(content=...)` explícito, em vez de deixar o
FastAPI serializar pelo `response_model` declarado — isso é o que permite a
injeção de falha realmente alterar o formato da resposta; se as rotas
dependessem do `response_model` normal, o Pydantic validaria e filtraria
silenciosamente qualquer campo alterado antes de sair pela rede.
`response_model` continua declarado nas rotas só pra gerar a documentação
OpenAPI do contrato "normal".

## AgenteCore — experimentos com os modelos locais

<!-- ! Alteração de IA - Revisar: seção nova descrevendo a bateria de experimentos e a
     biblioteca de documentação da Fase 2-B.
     ! Motivo: o README ainda dizia que o AgenteCore estava vazio; sem esta seção os
     integrantes não sabem a ordem dos scripts nem que nada deve rodar com outro modelo
     residente no Ollama. -->
Tudo em `Programacao/AgenteCore/experimentos/`, rodando com o Python da venv
do AgenteCore (`Programacao/AgenteCore/.venv`, criada pelo instalador).
**Regra de ouro: um modelo por vez** — os scripts conferem em `/api/ps` que
não há outro modelo residente, e toda inferência é forçada para CPU
(`num_gpu=0`) porque a tese afirma operar sob restrição de hardware local.

**Duas máquinas, duas pastas de resultado.** A Fase 2-A foi medida no Ryzen
de desenvolvimento (`resultados/`, `graficos/`, `relatorio.html` na raiz de
`experimentos/`). A Fase 2-B roda na **máquina-alvo** (notebook corporativo
i5-1235U, 16 GB, sem GPU) e grava em `resultados_alvo/` — é a variável de
ambiente `RESULTADOS_DIR` (lida por `caminhos.py`) que decide onde cada
script grava e lê, para os dois conjuntos nunca se sobrescreverem. Cada
registro leva o nome da máquina, e `maquina.json` guarda CPU, RAM, sistema e
versão do Ollama. Tempos só são comparáveis dentro da mesma pasta.

| Ordem | Script | O que faz |
|---|---|---|
| 1 | `validar_banco.py --indice` | Valida os 90 casos e a biblioteca (`base_conhecimento/`), mede a recuperação BM25 offline e regrava o `INDICE.md`. Não chama o Ollama. |
| 2 | `verificar_cache_prefixo.py` | Mede se o Ollama reaproveita o cache de KV com prefixo idêntico (decide o custo do braço "biblioteca inteira"). |
| 3 | `executar_bateria.py --modelos M --condicao A0..A5` | Roda os 90 casos; `A0` sem biblioteca (Fase 2-A), `A1` inteira, `A2` top-3 recuperada, `A3` só o verbete certo, `A4` distratores, `A5` verbete errado. Resumível: grava JSONL por caso. |
| 4 | `avaliar.py` | Pontua pelos gabaritos; Δ contra A0, McNemar pareado, IC de Wilson, ancoragem, flips de quantização. |
| 5 | `gerar_graficos.py` / `gerar_relatorio.py` | PNG/SVG para o documento e `relatorio.html` navegável, tudo a partir do JSONL. |
| — | `rodar_fase2b.ps1` | Orquestra a Fase 2-B inteira **na máquina-alvo**: confere Python/Ollama/RAM/disco, baixa os 8 modelos que faltarem, grava `maquina.json`, refaz a linha de base A0 lá, roda A1–A5 e a avaliação — tudo em `resultados_alvo/`. Um modelo por vez, resumível (Ctrl+C e relançar), ~30–45 h: `powershell -ExecutionPolicy Bypass -File .\rodar_fase2b.ps1`. |

A leitura dos resultados fica em `RESULTADO_FASE2.md` (primeira leva, 2 casos) e em
[`Documentacao/memorial/3-resultados-e-analises/fase-2a-relatorio-por-modelo.md`](Documentacao/memorial/3-resultados-e-analises/fase-2a-relatorio-por-modelo.md)
(Fase 2-A, 90 casos × 3 estratégias × 6 modelos) e em
[`fase-2b-relatorio-por-modelo.md`](Documentacao/memorial/3-resultados-e-analises/fase-2b-relatorio-por-modelo.md)
(Fase 2-B, biblioteca de documentação, 2.610 inferências na máquina-alvo).
Decisões, pesquisa e fontes estão em `Documentacao/Memorial de Desenvolvimento.md`
(índice) e na pasta `Documentacao/memorial/`.

### Fase 3 — biblioteca gerida pelo modelo

<!-- ! Alteração de IA - Revisar: subseção nova descrevendo a Fase 3 (biblioteca editada pelo
     próprio modelo, por modelo e por época) e os scripts que a implementam.
     ! Motivo: a Fase 3 só estava descrita no plano aprovado
     (`claude-memoria/plano-aprovado-fase-3.md`); sem esta subseção, quem abrisse o repositório
     não saberia que existe uma bateria nova em implementação, o que cada script novo faz, nem
     como rodar o piloto antes de comprometer a máquina pela bateria completa (~60 h). -->
A Fase 2-B mostrou que a biblioteca **recuperada** (top-3) sobe o acerto em
todos os modelos e que documentação errada é seguida em 93–96% dos casos. A
Fase 3 testa se o próprio modelo consegue **melhorar** essa documentação: em
cada "época", ele diagnostica os 90 casos com a biblioteca atual e, só nos
casos de aprendizado (54 dos 90, com gabarito), propõe acréscimos — nunca
reescreve nem apaga — que passam por validação em código antes de entrar.
Cada modelo evolui a **sua própria cópia** da biblioteca (a original em
`base_conhecimento/` nunca é escrita pela Fase 3); a cópia intocada continua
disponível como L0, o ponto de comparação de todas as épocas seguintes.

<!-- ! Alteração de IA - Revisar: em 12/09/2026 a tabela deixou de marcar seis scripts como
     "(em implementação)", passou a dizer "30 códigos de rejeição em 26 checagens" e registra o
     piloto `-Piloto` executado; a árvore de `resultados_alvo/fase3/` ganhou os arquivos que a
     implementação de fato grava (`maquina.json`, `fase3.log`, `diff__E<n>*`,
     `revisao_edicoes__<slug>.md`, gráficos 12–17 na pasta comum) e o parágrafo de custo cita a
     projeção do executor.
     ! Motivo: todos os scripts existem, foram revisados e rodaram juntos no piloto de
     12/09/2026 (1 modelo, 10 casos, 1 época, 00h13; retomada com hash idêntico) — a marca
     "(em implementação)" estava obsoleta. `CODIGOS_REJEICAO` em `evolucao_biblioteca.py` tem
     30 códigos (26 é o número de checagens). E a árvore omitia arquivos que existem em
     `resultados_alvo/fase3_piloto/` (conferida em 12/09/2026): os diffs de época são irmãos
     de `epoca-n/`, fora do snapshot (decisão registrada no livro-razão), e os gráficos da
     corrida oficial vão para `resultados_alvo/graficos/`, não para `fase3/`
     (`caminhos.fase3()`). O custo de ~60 h era só o do plano; o executor projeta 67,18 h. -->
| Script | O que faz | Como rodar |
|---|---|---|
| `evolucao_biblioteca.py` | Parser das propostas de edição do modelo, validador com 30 códigos de rejeição em 26 checagens de ordem fixa (cópia do caso, estouro de teto, vocabulário fora do padrão etc.), aplicação só por acréscimo, hash/diff/fechamento de cada época. | Usado pelos scripts abaixo; não é chamado direto. |
| `executar_fase3.py` | Laço por modelo e por época: diagnóstico com a biblioteca da época anterior, proposta de edição nos casos de aprendizado, validação e aplicação na época seguinte. Resumível por `(modelo, época, caso, tipo)`. | `python executar_fase3.py --modelos M --epocas 3 --saida fase3` |
| `avaliar_fase3.py` | Pontua por modelo × versão da biblioteca (L0..L3) × partição (aprendizado/avaliação/geral); McNemar pareado, Cochran Q entre as 4 épocas, IC de Wilson, flips de acerto↔erro entre épocas. | `python avaliar_fase3.py` |
| `comparar_fases.py` | Junta 2-A, 2-B e Fase 3 num só `comparacao_fases.json`/`.md`, com os pareamentos que fazem sentido entre fases. | `python comparar_fases.py` |
| `gerar_graficos_fase3.py` | Figuras 12–17: acerto por época, recuperação por época, motivos de rejeição das propostas, crescimento da biblioteca, comparação entre as três fases. | `python gerar_graficos_fase3.py` (venv com matplotlib) |
| `gerar_relatorio_fase3.py` | `relatorio_fase3.html` navegável por modelo/época/partição, com cada proposta de edição (prompt, resposta crua, decisão do validador). | `python gerar_relatorio_fase3.py` |
| `testar_fase3.py` | Testes em Python puro (sem pytest) do parser, do validador, da aplicação de edição e do hash/diff — sem chamar o Ollama, < 30 s. | `python testar_fase3.py` |
| `rodar_fase3.ps1` | Orquestrador da Fase 3 nesta máquina: valida a biblioteca, roda os testes, executa os 4 modelos em sequência, avalia, compara as fases e gera gráficos/relatório. O piloto `-Piloto` (1 modelo, 10 casos, 1 época) rodou em 12/09/2026 em 00h13, e o teste de retomada reconstruiu a `epoca-1` com o mesmo hash — validação do encanamento feita; a bateria completa ainda não rodou. | `.\rodar_fase3.ps1 -Piloto` (amostra pequena, 1 modelo, 1 época) antes da bateria completa: `.\rodar_fase3.ps1` |

Cada modelo grava em `resultados_alvo/fase3/`:

```
fase3/
  maquina.json               máquina, versão do Ollama, RAM e horário de início (relances são acrescentados, não sobrescrevem)
  particao.json              divisão determinística dos 90 casos em aprendizado (54) e avaliação (36)
  fase3.log                  registro corrido da execução, gravado pelo rodar_fase3.ps1 (*.log está no .gitignore)
  bibliotecas/<slug>/
    epoca-0..3/               snapshot completo da biblioteca do modelo ao fechar cada época (verbetes + INDICE.md + fechamento.json)
    diff__E<n>.{json,md}      o que a época n acrescentou em relação à anterior (irmão de epoca-n/, fora do snapshot)
    diff__E<n>__vs_original.{json,md}   idem, em relação à biblioteca original
    historico.jsonl           uma linha por edição aceita
  <slug>/
    diagnosticos__L0..L3.jsonl   diagnóstico dos 90 casos com cada versão da biblioteca
    propostas__E1..E3.jsonl      propostas de edição e a decisão do validador, por época
  avaliacao_fase3.json, resumo_fase3.json      métricas por modelo/época/partição
  comparacao_fases.json/.md                    2-A × 2-B × Fase 3 lado a lado
  revisao_edicoes__<slug>.md                   amostra de até 30 edições aceitas por modelo, para o Eric marcar Correta/Parcial/Errada
  relatorio_fase3.html                         relatório navegável
../graficos/12-…17-…          figuras 12–17 na pasta comum de gráficos (resultados_alvo/graficos/); só o piloto grava em fase3_piloto/graficos/
```

<!-- ! Alteração de IA - Revisar: segunda passada de 12/09/2026 — o comando da projeção
     ganhou `--modelos` com os quatro modelos.
     ! Motivo: `python executar_fase3.py --so-projecao` sozinho encerra com "the following
     arguments are required: --modelos" (`required=True` no argparse de `executar_fase3.py`);
     o 67,18 h só se reproduz com os quatro modelos na linha de comando, que é o que
     `rodar_fase3.ps1` faz antes da corrida (saída conferida em 12/09/2026). -->
Estimativa de custo: **~60 h de máquina** para os 4 modelos × 3 épocas no
plano; a projeção que o executor imprime (`python executar_fase3.py
--so-projecao --modelos granite4.2:8b qwen2.5:7b qwen2.5-coder:7b
qwen2.5-coder:3b` — `--modelos` é obrigatório; é o comando que `rodar_fase3.ps1`
roda antes da corrida —, com os ms/token medidos na 2-B) dá **67,18 h**. O piloto de 10
casos (`-Piloto`) rodou em 12/09/2026 em 00h13 — `qwen2.5-coder:3b`, 1 época,
0 de 6 propostas aceitas — e valida o encanamento, não o custo dos quatro
modelos. A bateria é **retomável**: interromper com Ctrl+C e rodar de novo
continua da mesma época e do mesmo caso, sem repetir trabalho já fechado.

<!-- ! Alteração de IA - Revisar: em 21/09/2026 entraram o parágrafo "Resultado da Fase 3", a subseção "Fase 3-B" e a seção "Ferramentas de apoio".
     ! Motivo: a bateria da Fase 3 rodou em 13–15/09/2026 e o README ainda descrevia só a preparação; a Fase 3-B (executor próprio, sem tocar nos scripts oficiais) e a pasta `ferramentas/` são novas no repositório e ninguém saberia para que servem sem esta descrição. Números só com origem: `resultados_alvo/fase3/fase3.log` e `comparacao_fases.md`. -->
**Resultado da Fase 3 (13–15/09/2026).** A bateria rodou na máquina-alvo de
13/09 08:45 a 15/09 18:44 (`FIM da Fase 3 - duracao total 58h59 - modelos com
falha: nenhum`, Ollama 0.34.0), 2.088 inferências, e os resultados estão em
`resultados_alvo/fase3/` (commit `b9f9ad9`). As tabelas por modelo e fase estão
em `resultados_alvo/fase3/comparacao_fases.md`; a leitura e a decisão do modelo
ficam no Memorial (`Documentacao/memorial/3-resultados-e-analises/`), em
preenchimento pelo plano complementar de 21/09/2026.

### Fase 3-B — ponte de versão e testes complementares

Depois da bateria o Ollama atualizou sozinho de 0.34.0 para 0.34.1. Qualquer
inferência nova passa antes por uma **ponte de versão** (L0 nos 36 casos de
avaliação, 4 modelos) que mede se o runtime novo reproduz o antigo; só então os
testes complementares que o Eric escolher (casos inéditos, troca cruzada de
bibliotecas entre modelos, granite com o teto de texto relaxado, verbete errado
plantado nas bibliotecas finais). Tudo roda por um executor **próprio**, que
lê **cópias** dos snapshots oficiais e nunca altera `executar_fase3.py`,
`estrategias.py`, `evolucao_biblioteca.py` nem `resultados_alvo/fase3/`.

| Script | O que faz | Como rodar |
|---|---|---|
| `executar_fase3b.py` | Modos `ponte`, `cruzada` (`--doador`, `--versoes`), `texto_max` (`--texto-max`, só granite), `a5` e `ineditos`; copia o snapshot pedido para a pasta da saída, grava `condicoes_3b.json` e `maquina.json` e chama a "passada final" de `executar_fase3.rodar_epoca` (só diagnóstico). | `python executar_fase3b.py --modo ponte --saida fase3b_ponte --modelos …` |
| `avaliar_fase3b.py` | Avalia a saída de um modo: os quatro primeiros delegam a `avaliar_fase3.avaliar_saida`; `ineditos` agrega com o gabarito de cada registro. | `python avaliar_fase3b.py --saida fase3b_ponte` |
| `testar_fase3b.py` | Testes sem LLM (cópia preserva o hash, modos aplicam e restauram `TEXTO_MAX`/`CONDICAO`, área oficial intocada antes e depois da suíte). | `python testar_fase3b.py` |
| `rodar_fase3b.ps1` | Orquestrador: testes, um modelo por vez com checagem de RAM (pula e lista o modelo se faltar memória; relançar retoma), avaliação ao fim. | `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo ponte -Saida fase3b_ponte` |

Cada modo grava em `resultados_alvo/<saida>/` a mesma árvore da Fase 3 (snapshots
copiados em `bibliotecas/<slug>/`, `diagnosticos__L<n>.jsonl` por modelo,
`avaliacao_fase3.json`, `resumo_fase3.json`) mais `condicoes_3b.json` (modo, doador,
versões, teto de texto, condição, versão do Ollama). A ponte de 21/09/2026 rodou só
para o `qwen2.5-coder:3b` (os modelos maiores foram pulados por falta de RAM livre
durante o dia); relançar o mesmo comando retoma os que faltam.

## Ferramentas de apoio ao trabalho com IA (`ferramentas/`)

Scripts em Python padrão, sem dependência, que fazem localmente o que antes se
pedia a agentes (regra registrada no `CLAUDE.md`: primeiro a máquina, depois o
modelo):

| Script | O que faz |
|---|---|
| `medir_tokens.py` | Soma o consumo de tokens do Claude Code a partir dos transcritos locais, por dia, modelo e tipo de agente (linha de base e medição "depois" das medidas de economia). |
| `resumir_saida.py` / `gancho_pre_bash.py` | Hook `PreToolUse` do Claude Code (`.claude/settings.json`) que encurta a saída de comandos longos (testes, baterias, `git diff`) antes de ela entrar no contexto. |
| `conferir_docs.py` | Confere a documentação antes de entregar: links relativos, tag `! Alteração de IA - Revisar` com `! Motivo` em todo arquivo tocado, frases obsoletas, hipóteses H1–H6 idênticas, BOM e ausência de travessão nos `.ps1`. |
| `extrair_pesquisa.py`, `render_levantamento.py`, `integrar_pesquisa.py` | Fecham a pesquisa bibliográfica por script: extraem os artefatos verificados, geram as subseções no formato do Memorial (com `--check`) e integram texto, referências (com dedup) e mapa de decisões. |

## Memória do Claude Code entre máquinas

<!-- ! Alteração de IA - Revisar: seção nova apontando para a pasta claude-memoria/.
     ! Motivo (nota de 21/09/2026: desde então `.claude/` é versionada, menos `settings.local.json`; a memória em `~/.claude/projects/` continua fora): a memória do Claude e o .claude/CLAUDE.md não viajavam pelo git (ficavam fora do
     repositório ou no .gitignore); quem for usar o Claude na máquina-alvo precisa saber
     que existe um importador. -->
O que o Claude Code sabe deste projeto (decisões, regra de comentário, regra de
commit) fica fora do repositório. A pasta [`claude-memoria/`](claude-memoria/)
carrega tudo pelo git: na máquina de destino, rode
`powershell -ExecutionPolicy Bypass -File claude-memoria\importar.ps1` uma vez e
abra o Claude Code na pasta do repositório. Detalhes no README de lá.

<!-- ! Alteração de IA - Revisar: nota sobre a correção do cálculo do `<slug>` usado por
     `importar.ps1`/`exportar.ps1` (a pasta de memória do Claude Code para este projeto).
     ! Motivo: até 10/09/2026 a regex do slug só trocava `:` e `\` por `-`, deixando o `.` de
     "Eric.Derre" intacto e apontando para uma pasta de memória que o Claude Code nunca usa
     (`c--Users-Eric.Derre-Documents-TCC`); o slug real desta máquina é
     `c--Users-Eric-Derre-Documents-TCC` (todo caractere fora de letra/número vira `-`).
     Corrigido em 11/09/2026 nos dois scripts — ver `claude-memoria/README.md`. -->
Quem já rodou `importar.ps1`/`exportar.ps1` antes de 11/09/2026 deve rodar de
novo depois de atualizar: o slug calculado mudou (era
`c--Users-Eric.Derre-Documents-TCC`, agora é `c--Users-Eric-Derre-Documents-TCC`).

## Testes e lint

```powershell
cd Programacao\CobaiaAPI
.venv\Scripts\python.exe -m pytest -v
.venv\Scripts\python.exe -m ruff check .
```
(No Linux/macOS: `.venv/bin/python -m pytest -v`.)

Os testes rodam contra o **banco real** (não há banco de testes isolado —
é um ambiente cobaia, não produção), então rode `install.ps1`/`install.sh`
pelo menos uma vez antes.

## O que é versionado e por quê

O repositório é deliberadamente "hit and run": versionamos **muito mais que
o normal** para que quem clonar precise do mínimo de passos. Fica de fora só
o que não funcionaria na máquina de outra pessoa, ou o que se regenera
sozinho — versionar essas coisas atrapalharia o "hit and run" em vez de
ajudar.

<!-- ! Alteração de IA - Revisar: em 12/09/2026 a tabela ganhou as duas linhas de `.superpowers/`
     e de `resultados_alvo/fase3_piloto/`, que já estavam no `.gitignore` (linhas 19 e 25).
     ! Motivo: as duas regras entraram no `.gitignore` em 11/09/2026 com comentário lá, mas esta
     tabela — que é onde o README explica o que fica fora do git e por quê — não as citava, e
     quem procurasse aqui o motivo de o piloto não estar versionado não achava. -->
| Item | Versionado? | Por quê |
|---|---|---|
| `Cobaia.exe` (8.6 MB) | **Sim** | É o próprio entregável "hit and run" do Windows: clonou, deu duplo clique, rodou — sem precisar nem de Python instalado pra compilar. Elimina o risco de "o build falhou 5 min antes da banca". Precisa ser recompilado (`build_exe.ps1`) quando `Cobaia.py`/`install.py`/`run.py`/`_env_common.py` mudarem. |
| `Cobaia.spec` | **Sim** | Receita de recompilação (arquivo texto pequeno). |
| `Programacao/CobaiaFront/` inteiro (16 MB, sendo 13 MB de imagens) | **Sim** | Imagens, CSS/JS do Bootstrap e PHPMailer são carregados localmente pelo site — sem eles o CobaiaFront não renderiza. Não há passo de build/download que os recupere. |
| `banco/*.sql` | **Sim** | Schema + seed. É o que faz o site funcionar de verdade. |
| `.env.example` | **Sim** | Template de configuração (o `.env` real fica de fora). |
| `Programacao/CobaiaAPI/.venv/` (67 MB) | **Não** | Verificado: o `pyvenv.cfg` grava caminhos absolutos desta máquina (`home = C:\Python314`) e a pasta tem 16 `.exe` + 14 `.pyd` (binários Windows) e nenhum `bin/`. É **inutilizável no Linux** e quebra em outra máquina Windows. São 67 MB que enganam quem clona — e o instalador recria a venv correta pra cada SO em ~30s. |
| `__pycache__/`, `*.pyc` | **Não** | Cache de bytecode: derivado, regenerado sozinho, muda a cada execução e polui o diff. |
| `.env` | **Não** | Configuração local. Use o `.env.example` como base. |
| `build/`, `dist/` | **Não** | Artefatos transitórios do PyInstaller (o `.exe` final é gravado na raiz, esses ficam no `%TEMP%`). |
| `node_modules/`, browsers do Playwright | **Não** | Trabalho futuro do AgenteCore — centenas de MB, específicos de cada SO, baixados por instalador. |
| `.claude/` (menos `settings.local.json`) | **Sim** | Configuração do projeto para o Claude Code: `CLAUDE.md`, `settings.json` (hook que resume saídas longas, permissões de leitura, plugin de estilo desligado), `rules/` por tipo de arquivo e `skills/` copiadas — precisa chegar à outra máquina pelo git (decisão do Eric, 21/09/2026). Só `settings.local.json` (permissões concedidas nesta máquina) fica de fora. |
| `.superpowers/` | **Não** | Rascunho de sessão do Claude Code (livro-razão, briefs e relatórios de tarefa da Fase 3); mesma natureza de `.claude/`. |
| `Programacao/AgenteCore/experimentos/resultados_alvo/fase3_piloto/` | **Não** | Piloto da Fase 3 (1 modelo, 10 casos, 1 época): existe para conferir o encanamento e calibrar o tempo antes das ~60 h; seus JSONL e snapshots confundiriam a leitura de `resultados_alvo/fase3/`, que é o que vale. |

O "hit and run" continua íntegro sem a venv, porque os dois caminhos a
recriam automaticamente:
- **Windows:** duplo clique em `Cobaia.exe` → instala (inclui criar a venv) → sobe tudo → abre o navegador.
- **Linux/macOS:** `./install.sh && ./run.sh` → mesma coisa.

## Decisões técnicas e problemas resolvidos

Documentado aqui porque cada um foi descoberto testando ao vivo, não
teorizado — importante pra quem for mexer no ambiente depois entender o
porquê:

- **XAMPP foi descartado.** O objetivo era um instalador silencioso e
  roteirizável em 3 SOs; o instalador GUI do XAMPP não se presta bem a
  isso. PHP e MariaDB nativos, instalados via linha de comando
  (`winget`/`apt`/`brew`), resolvem sem essa fricção.
- **MariaDB no Windows não registra serviço.** Testado nesta máquina sem
  privilégios de administrador: o `winget install MariaDB.Server` instala
  os binários e já inicializa o data dir (root sem senha), mas não registra
  um Windows Service (isso exigiria elevação). Por isso o MariaDB é sempre
  gerenciado como subprocesso direto no Windows, igual ao PHP e ao uvicorn
  — ver `_env_common.py::ensure_mariadb_running`.
- **`extension_dir` do PHP vem hardcoded errado.** O build Windows do PHP
  aponta por padrão pra `C:\php\ext`, que não bate com o caminho real de
  instalação do winget. `_env_common.py::php_extension_flags` calcula o
  caminho certo dinamicamente a partir do binário encontrado.
- **`mbstring` é obrigatória, não opcional.** `mb_strimwidth()` é usada em
  5 páginas de produtos (incluindo a home) — sem a extensão carregada, é
  **erro fatal**, não warning. Só foi percebido testando a home page a
  fundo (um teste superficial só com `grep` não pegou, porque o conteúdo
  antes do ponto de falha ainda aparecia no HTML).
- **`output_buffering` precisa estar ligado.** `cliente/index.php` ecoa
  HTML antes de `reserva_cli.php` incluir `admin/acesso_com.php`, que só
  então chama `session_start()` — um bug de ordenação pré-existente no
  código original. Um XAMPP/Apache real normalmente mascara isso porque
  `output_buffering` costuma vir ligado por padrão. Sem isso, a sessão de
  login não é retomada corretamente e a página trunca logo após a
  saudação. Resolvido via flag de configuração do PHP (não altera nenhum
  arquivo `.php`).
- **`vw_tbpedidos` usa `LEFT JOIN`, não `JOIN`.** Na primeira versão da
  view (criada do zero — o dump original não tinha essa tabela/view), um
  `JOIN` normal a partir de `tbpedido_reserva` fazia um cliente **sem
  nenhuma reserva ainda** sumir inteiramente da view — quebrando a
  saudação com "Trying to access array offset on value of type null".
  Corrigido fazendo `LEFT JOIN` a partir de `tbusuarios`, e usando
  `u.id_usuario` (não `pr.id_clientes`) como `id_clientes` — assim o campo
  continua correto mesmo sem nenhuma reserva prévia.

## Problemas conhecidos (deixados de propósito)

Decisão do grupo: manter `CobaiaFront` como veio, sem correções de código,
exceto o único caso de segurança justificado abaixo.

| Item | Situação |
|---|---|
| Link "Saiba Mais..." nas listagens de produtos | Aspas do `href` no lugar errado (bug do código original) — sempre abre `id_produto=` vazio. Não corrigido. |
| Senha de usuário: texto puro no insert, MD5 no update, sem hash no login | Inconsistência do código original. Não corrigido — o `seed.sql` sempre insere em texto puro, então não afeta o login das contas de teste. |
| Credencial SMTP real hardcoded em `rodape_contato_envia.php` | Decisão explícita do grupo: como é ambiente de teste sem dados reais, foi mantida como está. |

## Segurança

Este é um **ambiente de teste** (cobaia), não um sistema em produção:
credenciais fracas/hardcoded, SQL injection nas queries do CobaiaFront, e
CORS liberado (`*`) na CobaiaAPI são conhecidos e intencionalmente não
corrigidos — fazem parte do escopo de cenários que o agente de QA deve ser
capaz de lidar. Não reutilize esses padrões fora deste projeto.

## Troubleshooting

- **`.\install.ps1 : ... a execução de scripts foi desabilitada neste
  sistema` (PSSecurityException):** é a Execution Policy padrão do Windows,
  que bloqueia scripts `.ps1` não assinados — não é um bug do projeto. Use
  `install.cmd`/`run.cmd` em vez de chamar os `.ps1` diretamente (eles
  chamam o PowerShell com `-ExecutionPolicy Bypass`, que vale só pra aquela
  execução, sem mudar nenhuma configuração persistente do sistema). Se
  preferir rodar o `.ps1` direto mesmo assim:
  `powershell -ExecutionPolicy Bypass -File .\install.ps1`.
- **`winget install` parece ter funcionado mas o comando ainda não é
  encontrado:** normal — o PATH só atualiza numa sessão de terminal nova.
  `install.py`/`run.py` já lidam com isso procurando o executável
  diretamente nos caminhos de instalação conhecidos, sem depender do PATH.
- **Porta 8080 ou 8000 já em uso:** edite `FRONT_PORT`/`API_PORT` no topo
  de `run.py`.
- **Erro de conexão com o banco (`Access denied for user 'root'`):** o
  `connect.php` do CobaiaFront espera `root` sem senha. Rode o instalador
  de novo — ele tenta corrigir isso automaticamente; se persistir, ajuste
  manualmente (`ALTER USER 'root'@'localhost' IDENTIFIED BY '';`).
- **`ModuleNotFoundError` ao rodar a CobaiaAPI:** o venv não foi
  criado/atualizado. Rode `install.ps1`/`install.sh` de novo.

## Convenções para alterações por IA

Ver [`.claude/CLAUDE.md`](.claude/CLAUDE.md) para as regras completas de
colaboração com IA neste repositório (não commitar automaticamente, marcar
alterações com `! Alteração de IA - Revisar`, conferir colunas reais antes
de escrever SQL, priorizar causa raiz sobre contorno).
