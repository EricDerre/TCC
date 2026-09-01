# TCC — Agente de QA E2E Autônomo — Ambiente "Cobaia"

Este repositório contém o ambiente-alvo ("cobaia") usado para validar o
**Agente de QA End-to-End (E2E) Autônomo com Capacidades de Self-Healing**,
projeto de pesquisa do curso de Ciência da Computação da UNICID. A
fundamentação teórica completa está em
[`Documentacao/Projeto de Pesquisa - ABNT 15287_2025 - V3.md`](Documentacao/Projeto%20de%20Pesquisa%20-%20ABNT%2015287_2025%20-%20V3.md).

Este README documenta apenas o **ambiente cobaia** (`Programacao/CobaiaFront`
+ `Programacao/CobaiaAPI`) — o agente em si (`Programacao/AgenteCore`) ainda
não foi implementado.

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
├── .claude/CLAUDE.md                       # regras de colaboração com IA neste repo
├── Documentacao/                           # projeto de pesquisa (ABNT) do TCC
└── Programacao/
    ├── AgenteCore/                         # (vazio — trabalho futuro)
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
| `.claude/` | **Não** | Config local do Claude Code, não faz parte do projeto. |

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
