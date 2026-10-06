<!-- ! Alteração de IA - Revisar: documento inteiro gerado por IA (arquitetura, instalação,
     uso, decisões técnicas e problemas conhecidos do ambiente cobaia).
     ! Motivo: o repositório não tinha nenhuma documentação; quem clonasse não teria como
     saber que o CobaiaFront depende das extensões mbstring/output_buffering do PHP, que o
     banco é compartilhado entre os dois alvos, nem quais bugs foram deixados de propósito.
     Cada afirmação técnica aqui foi verificada executando, não deduzida do código. -->
<!-- ! Alteração de IA - Revisar: revisão de 30/09/2026 a pedido do Eric: cabeçalho novo (nome do projeto, selos, resumo,
     estado por fase e resultado principal, mapa da documentação), seções de contribuição, citação, licença e autores,
     índice regerado a partir dos títulos, títulos sem travessão, e todos os travessões e setas do texto corrido trocados
     por vírgula, dois-pontos ou palavras (blocos de código, comandos e diagramas ficaram como estavam).
     ! Motivo: o README descrevia só o ambiente cobaia e ainda dizia que a bateria da Fase 3 estava por rodar e que a Fase 4
     era o próximo passo sem nada antes; o repositório passou a ter os padrões de comunidade do GitHub (código de conduta,
     guia de contribuição, licença, política de segurança, modelos de issue e de pull request) e o Eric pediu tom mais sério,
     sem travessões e setas, mantendo a árvore do repositório e o restante do conteúdo. -->
# Agente de QA E2E Autônomo com Self-Healing

[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-2ea44f)](LICENSE)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](Programacao/CobaiaAPI/requirements.txt)
[![PHP 8.2](https://img.shields.io/badge/PHP-8.2-777BB4?logo=php&logoColor=white)](Programacao/CobaiaFront)
[![Modelo local](https://img.shields.io/badge/LLM%20local-Ollama%20%C2%B7%20qwen2.5%3A7b-1f6feb)](Programacao/AgenteCore/experimentos)
[![Painel do projeto](https://img.shields.io/badge/painel-do%20projeto-8957e5)](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN)

Trabalho de Conclusão de Curso em Ciência da Computação (Universidade Cidade de
São Paulo, 2026): um agente de QA end-to-end que roda com um modelo de linguagem
local (Ollama, só CPU, sem nuvem), diagnostica falhas na fronteira de integração
entre o front-end e a API (deriva de contrato) e mantém a própria biblioteca de
conhecimento sobre o sistema testado. Este repositório reúne o ambiente-alvo (dois
sistemas "cobaia"), as baterias de avaliação dos modelos locais (Fases 2-A, 2-B,
3 e 3-B), as ferramentas de apoio, o memorial de desenvolvimento e o projeto de
pesquisa no padrão ABNT.

**Estado em 01/10/2026:** Fases 1, 2-A, 2-B, 3 e 3-B concluídas (a 3-B com a
troca cruzada de bibliotecas rodada em 01/10); Pré-Fase 4, uma pausa de pesquisa
antes do agente na tela, em andamento desde 01/10; Fase 4, o agente na tela, em
planejamento. Modelo padrão do agente: `qwen2.5:7b` com a biblioteca no estado L1
(decisão 52). Números, gráficos e a leitura de cada resultado estão no
[painel do projeto](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN).

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Estado do projeto e resultados](#estado-do-projeto-e-resultados)
- [Documentação](#documentação)
- [Por que dois alvos](#por-que-dois-alvos)
- [Arquitetura](#arquitetura)
- [Stack técnica](#stack-técnica)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como rodar](#como-rodar)
- [Cobaia.exe: instalação, execução e navegador em um clique](#cobaiaexe-instalação-execução-e-navegador-em-um-clique)
- [Navegador recomendado para o agente](#navegador-recomendado-para-o-agente)
- [CobaiaFront em detalhe](#cobaiafront-em-detalhe)
- [CobaiaAPI em detalhe](#cobaiaapi-em-detalhe)
- [AgenteCore: experimentos com os modelos locais](#agentecore-experimentos-com-os-modelos-locais)
- [Ferramentas de apoio ao trabalho com IA (`ferramentas/`)](#ferramentas-de-apoio-ao-trabalho-com-ia-ferramentas)
- [Memória do Claude Code entre máquinas](#memória-do-claude-code-entre-máquinas)
- [Testes e lint](#testes-e-lint)
- [O que é versionado e por quê](#o-que-é-versionado-e-por-quê)
- [Decisões técnicas e problemas resolvidos](#decisões-técnicas-e-problemas-resolvidos)
- [Problemas conhecidos (deixados de propósito)](#problemas-conhecidos-deixados-de-propósito)
- [Segurança](#segurança)
- [Troubleshooting](#troubleshooting)
- [Como contribuir](#como-contribuir)
- [Como citar](#como-citar)
- [Licença](#licença)
- [Autores](#autores)
- [Convenções para alterações por IA](#convenções-para-alterações-por-ia)

## Sobre o projeto

O objetivo é um agente de QA end-to-end que roda inteiramente na máquina de quem
testa, com um modelo de linguagem local, e que:

- **detecta deriva de contrato** (contract drift) na fronteira entre o front-end
  e a API, o ponto em que sistemas legados e serviços novos mais quebram;
- **mantém a própria biblioteca de conhecimento** sobre o sistema-alvo: em cada
  época o modelo diagnostica as falhas e propõe acréscimos à documentação, que só
  entram depois de uma validação em código;
- **cura seletores** quando a interface muda (self-healing), a etapa prevista
  para a Fase 4.

Para medir isso sem depender de opinião, o repositório tem um ambiente-alvo
controlado (dois sistemas "cobaia" com injeção determinística de falhas), 90
casos de falha com gabarito e uma bateria de avaliação que compara modelos e
versões da biblioteca por regras fixadas antes de rodar.

## Estado do projeto e resultados

| Fase | O que é | Estado |
|---|---|---|
| 1 | Ambiente e sistemas cobaia | Concluída |
| 2-A | Prompts sem documentação, seis modelos, máquina de desenvolvimento | Concluída |
| 2-B | Biblioteca de documentação escrita à mão, seis condições, máquina-alvo | Concluída |
| 3 | Biblioteca gerida pelo próprio modelo, quatro modelos, três épocas | Concluída em 15/09/2026 |
| 3-B | Pontes de versão, casos inéditos, troca cruzada e sondas | Concluída em 01/10/2026 |
| Pré-Fase 4 | Pesquisa antes da Fase 4: modelos grandes lendo os pesos do disco (repositório colibri), atlas visual das competências e raciocínio aberto | Em andamento desde 01/10/2026 |
| 4 | O agente na tela: interceptação, poda da árvore de acessibilidade, cura de seletor | Em planejamento |
| 5 | Medição de valor (tempo de reparo e sucesso da tarefa) | Não iniciada |

**Resultado principal (decisão 52, 22/09/2026):** pela regra fixada antes da
bateria, o modelo padrão do agente é o `qwen2.5:7b` com a biblioteca no estado
L1, a primeira época escrita por ele, curada em 29/09/2026 e guardada em
`Programacao/AgenteCore/biblioteca_producao/`. O comparativo com o
`qwen2.5-coder:7b`, os 36 casos inéditos, a curadoria, o experimento do
recuperador, a ablação base × instruct e as quatro rodadas de pesquisa
bibliográfica estão no [painel do projeto](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN), com uma
aba por tópico; uma cópia do painel fica em
`Documentacao/dashboard/painel-do-projeto.html`. Os números citados neste README
vêm dos registros em `resultados_alvo/` e do Memorial.

## Documentação

- [Painel do projeto](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN): estado por fase, pendências, roadmap e os resultados, numa página só; gerado por `ferramentas/gerar_dashboard.py`.
- [Memorial de Desenvolvimento](Documentacao/Memorial%20de%20Desenvolvimento.md): índice de tudo o que foi decidido, pesquisado, medido e analisado, em `Documentacao/memorial/` (decisões numeradas, levantamentos bibliográficos com afirmações verificadas, relatórios por fase, análise decisória, método e ferramental).
- [Roadmap](Documentacao/memorial/roadmap.md) e [pendências](Documentacao/memorial/pendencias.md): o que falta rodar e as decisões, em fichas.
- [Projeto de pesquisa (ABNT NBR 15287)](Documentacao/Projeto%20de%20Pesquisa%20-%20ABNT%2015287_2025%20-%20V3.md) e o PDF beta gerado a partir dele.
- Registros oficiais das baterias em `Programacao/AgenteCore/experimentos/resultados_alvo/` (JSON, logs, gráficos e relatórios navegáveis).

## Por que dois alvos

O núcleo da pesquisa é detectar **Contract Drift** (deriva de contrato) na
fronteira de integração Front-to-Back. Um site PHP+MySQL clássico, que
renderiza tudo no servidor, não tem essa fronteira, não há nenhuma
requisição JSON pra interceptar. Por isso o ambiente cobaia tem **dois
alvos**, deliberadamente separados:

| Alvo | O quê | Serve pra testar |
|---|---|---|
| **CobaiaFront** | Site PHP+MySQL legado e monolítico (cedido por um integrante do grupo), mantido **100% intocado** no código | Interceptação de requisições de página completa, erros PHP/SQL clássicos, sistemas legados sem API |
| **CobaiaAPI** + a aba "PRODUTOS (API)" dentro do próprio CobaiaFront | API JSON nova (Python/FastAPI), com mecanismo de injeção de falhas controlada | Contract Drift em contratos JSON reais, o foco principal do agente |

Os dois compartilham o **mesmo banco de dados** (`ti93phpdb01`), uma
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
                     │      MariaDB · banco ti93phpdb01      │
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
- **Linguagem/execução:** PHP 8.2, servidor embutido (`php -S`), sem
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
├── LICENSE / CITATION.cff                  # licença MIT e citação do repositório
├── CONTRIBUTING.md / CODE_OF_CONDUCT.md / SECURITY.md    # como contribuir, conduta e política de segurança
├── .github/                                # modelos de issue e de pull request
├── .claude/                                # CLAUDE.md, settings.json (hooks, permissões), rules/ e skills/ do Claude Code (versionados; só settings.local.json fica fora)
├── ferramentas/                            # scripts locais de apoio: painel do projeto, medição de tokens, resumo de saídas, conferência da documentação, pesquisa, PDF do ABNT
├── claude-memoria/                         # memória do Claude + CLAUDE.md portáteis (importar/exportar.ps1) e os handoffs de sessão em contexto/
├── Documentacao/
│   ├── Projeto de Pesquisa - ABNT 15287_2025 - V3.md   # projeto de pesquisa; o PDF beta V4 é gerado a partir dele
│   ├── Memorial de Desenvolvimento.md      # índice do memorial
│   ├── memorial/                           # decisões numeradas, pesquisa bibliográfica, resultados e análises, projeto ABNT, método e ferramental, pendências, roadmap
│   ├── dashboard/painel-do-projeto.html    # painel do projeto (gerado por ferramentas/gerar_dashboard.py; publicado no claude.ai)
│   └── notebooks/                          # (fora do git) notebooks de apoio do livro-texto (Faceli et al., 3. ed.), baixados por quem tem o livro
└── Programacao/
    ├── AgenteCore/
    │   ├── base_conhecimento/              # biblioteca de documentação original do cobaia (Fase 2-B); nunca escrita por script
    │   │   ├── negocio/ contratos/ erros/ falhas_injetadas/ defeitos_conhecidos/
    │   │   └── INDICE.md                   # gerado por validar_banco.py --indice
    │   ├── biblioteca_producao/            # cópia curada da biblioteca L1 do qwen2.5:7b (ponto de partida da Fase 4)
    │   ├── experimentos/                   # baterias de avaliação dos modelos locais (Fases 2-A, 2-B, 3 e 3-B) e os registros em resultados_alvo/
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

Nada precisa ser pré-instalado manualmente além disso, o instalador cuida
do PHP, do MariaDB e do Python/venv.

## Instalação

No Windows, `Cobaia.exe` já faz instalação + run + abrir o navegador em um
só passo; ver [seção dedicada](#cobaiaexe-instalação-execução-e-navegador-em-um-clique)
abaixo. O resto desta seção documenta o instalador "por partes"
(`install.*`), útil pra rodar só a instalação sem subir os serviços, ou no
Linux/macOS.

Um único comando, na raiz do repositório:

```
# Windows: clique duplo em install.cmd, ou pelo terminal:
install.cmd
```
```bash
# Linux / macOS
./install.sh
```

No Windows, use `install.cmd` (não `install.ps1` diretamente), ele evita o
erro comum de *Execution Policy* do PowerShell (ver
[Troubleshooting](#troubleshooting)) sem precisar mudar nenhuma
configuração do sistema. `install.cmd` só chama `install.ps1` por baixo.

O que ele faz, em ordem (idempotente, pode rodar de novo a qualquer hora
sem duplicar nada):

1. Garante que existe Python 3 (instala via winget/apt/brew se faltar).
2. Instala PHP 8.2 se não encontrar (`winget`/`apt`/`brew`).
3. Instala MariaDB Server se não encontrar, e garante que está rodando,
   no Windows, como processo direto (não há serviço registrado, ver
   [Decisões técnicas](#decisões-técnicas-e-problemas-resolvidos)); no
   Linux/macOS, via `systemctl`/`brew services`.
4. Garante que o usuário `root` do banco está acessível sem senha (o que
   `Programacao/CobaiaFront/conn/connect.php`, intocado, espera).
5. Aplica, em ordem: `bancoatualizado.sql`, depois `schema_completo.sql` e
   por fim `seed.sql`.
6. Cria o venv em `Programacao/CobaiaAPI/.venv` e instala as dependências
   (`requirements-dev.txt`, que já inclui as de produção).
7. Prepara o ambiente do `AgenteCore`: venv própria, dependências, o
   Chromium do Playwright, o Ollama e o download do modelo padrão
   (`qwen2.5:7b`; a variável de ambiente `COBAIA_MODELO_LLM` troca o modelo).
   São alguns GB, então esse passo é o último e pode ser interrompido por quem
   só quer rodar o site.

Se algo faltar automatizar no seu SO específico, o script imprime uma
mensagem clara em vez de travar silenciosamente.

## Como rodar

```
# Windows: clique duplo em run.cmd, ou pelo terminal:
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
| `admin` | `admin123` | `sup` | Painel admin (`/admin/login.php`), CRUD de produtos/tipos/usuários |
| `11122233344` | `123456` | `cli` | Área do cliente (`/admin/login.php`, mesmo formulário), reservas |

14 produtos de exemplo já vêm cadastrados.

## Cobaia.exe: instalação, execução e navegador em um clique

No Windows, `Cobaia.exe` (raiz do repositório) faz tudo de uma vez: roda a
instalação completa (idempotente, se já estiver tudo instalado, só
confirma e segue), sobe CobaiaFront + CobaiaAPI, e abre as duas URLs no
navegador padrão assim que os serviços respondem. É o jeito mais direto de
usar o projeto, inclusive pra demonstrar ao vivo no dia da banca.

```
# duplo clique em Cobaia.exe, ou pelo terminal:
.\Cobaia.exe
```

Fecha a janela (ou `Ctrl+C`) pra encerrar tudo (PHP, MariaDB, uvicorn).

**Sobre o aviso do Windows Defender/SmartScreen:** `Cobaia.exe` não é
assinado digitalmente (certificado de assinatura de código custa dinheiro e
não faz sentido pra um projeto acadêmico), é esperado que o Windows mostre
"Windows protegeu seu PC" na primeira execução em uma máquina nova. Clique
em "Mais informações" e depois em "Executar assim mesmo". O `.exe` é gerado a partir
do código-fonte deste mesmo repositório (`Cobaia.py`), sem nenhuma
dependência externa além do que já está documentado aqui.

**Reproduzindo/atualizando o `.exe`:** ele não se autoatualiza, depois de
mudar `Cobaia.py`, `install.py`, `run.py` ou `_env_common.py`, rode:
```powershell
.\build_exe.ps1
```
Isso usa [PyInstaller](https://pyinstaller.org) (instalado num venv
temporário só pra compilar, separado do venv da CobaiaAPI) e regrava
`Cobaia.exe` na raiz. **Importante:** o `.exe` empacota um interpretador
Python só pra rodar a lógica de orquestração (winget/pip/php/uvicorn), ele
**não** usa esse interpretador embutido pra criar o venv da CobaiaAPI, isso
quebra (testado ao vivo: o layout do Python embutido no PyInstaller não é o
de uma instalação normal, faltam os arquivos que o módulo `venv` espera
copiar). Por isso, quando rodando como `.exe`, a criação do venv busca (ou
instala via winget, se faltar) um Python "de verdade" no sistema e delega a
criação pra ele via subprocesso; ver `find_or_install_real_python()` em
`_env_common.py`. As dependências da CobaiaAPI continuam indo exclusivamente
pra `Programacao/CobaiaAPI/.venv`, nunca pro ambiente do `.exe`.

Nos scripts (`install.cmd`/`.ps1`/`.sh`, sem ser via `.exe`), isso nem entra
em jogo, `sys.executable` ali já é um Python real, porque foi ele mesmo
quem rodou o script.

## Navegador recomendado para o agente

Esta pergunta é sobre qual navegador o **`AgenteCore` da Fase 4** deve
automatizar (via Playwright) pra interceptar rede/coletar erros, não afeta
o CobaiaFront/CobaiaAPI em si, que funcionam em qualquer navegador
(Bootstrap 3 + jQuery + `fetch()`, nada específico de motor).

**Recomendação: o Chromium que o próprio Playwright baixa e fixa
(`playwright install chromium`), rodando headless, não o Chrome/Edge
instalado no sistema.**

O motor é Chromium em qualquer um dos casos; a diferença é *qual build*.
Motivos, considerando que o projeto precisa rodar em Windows **e Linux**, de
graça e localmente:

- **Reprodutibilidade dos resultados (o argumento decisivo pra um TCC).** A
  pesquisa mede MTTR e Task Success. O Chrome/Edge do sistema se
  autoatualiza sozinho e é diferente na máquina de cada um dos 9
  integrantes, dois runs do mesmo experimento podem cair em versões
  diferentes do navegador. O Playwright **fixa uma build exata de Chromium
  por versão do Playwright**: todo mundo (e a banca, meses depois) roda
  exatamente o mesmo motor.
- **Mesmo comando nos dois SOs.** `playwright install chromium` é idêntico
  em Windows e Linux e cabe direto no instalador. Usar o Chrome do sistema
  exigiria um caminho de instalação por SO (winget no Windows, repositório
  `.deb`/`.rpm` no Linux), mais peças pra dar errado no "hit and run".
  No Linux, `playwright install --with-deps chromium` ainda instala
  sozinho as libs de sistema que o headless precisa (libnss3, libgbm1 etc.).
- **Não depende do que está instalado.** Máquina corporativa pode ter
  Chrome antigo, travado por política, ou nenhum.
- **Profundidade de interceptação:** o Chromium é o motor "de origem" do
  Playwright (boa parte da equipe veio do Puppeteer/Chrome DevTools), os
  hooks de rede (`page.on('request'/'response')`, `route()`, corpo via
  `response.body()`) são os mais maduros ali, comparado ao wrapper usado
  para Firefox (Juggler) ou WebKit.
- **Headless** é o modo mais testado do mercado inteiro de automação,
  exatamente o que o agente precisa pra rodar em segundo plano.

**Alternativa (uma linha de diferença):** se em alguma máquina o download
de ~150 MB for um problema, ou se a política de TI só permitir binário já
homologado, dá pra apontar pro Chrome instalado com
`browser_type.launch(channel="chrome")`, funciona em Windows e Linux e não
muda mais nada no código. Só perde a garantia de versão fixa. (`channel="msedge"`
existe também, mas aí a portabilidade pro Linux fica pior, já que o Edge não
é padrão lá, por isso não é a recomendação.)

**WebKit/Firefox** não agregam aqui: não há necessidade de validar
comportamento de Safari, e o Firefox tem hooks de rede menos ricos no
Playwright.

Detalhe à parte: o navegador que o `webbrowser.open()` do `Cobaia.exe` abre
(nesta máquina, Firefox, o seu padrão) é só conveniência pra você olhar o
site, **não tem relação nenhuma** com qual navegador o `AgenteCore` vai
automatizar depois, o Playwright sempre sobe sua própria instância
isolada, independente do navegador padrão do sistema.

## CobaiaFront em detalhe

Site de restaurante ("Churrascaria Fornalha"): cardápio público, busca de
produtos, formulário de contato (PHPMailer), painel admin com CRUD
completo, e área de cliente com reservas.

Rotas principais:
- `/index.php`: home (destaques + produtos + carrossel)
- `/produtos_busca.php?buscar=X`, `/produtos_por_tipo.php?id_tipo=X`,
  `/produto_detalhes.php?id_produto=X`
- `/produtos_api.php`: **nova**, consome a CobaiaAPI via `fetch()`
- `/admin/login.php`, que leva a `/admin/index.php` (CRUD produtos/tipos/usuários)
- `/admin/login.php`, que leva a `/cliente/index.php?cliente=<login>` (reservas)

O código PHP em si não foi alterado, exceto um link novo de navegação em
`menu_publico.php` (marcado com `! Alteração de IA - Revisar`) apontando
pra `produtos_api.php`.

## CobaiaAPI em detalhe

Documentação interativa (Swagger UI) sempre disponível em
`http://localhost:8000/docs` enquanto o servidor estiver rodando.

| Endpoint | Método | Descrição |
|---|---|---|
| `/api/produtos` | GET | Lista todos os produtos |
| `/api/produtos/{id}` | GET | Detalhe de um produto (404 se não existir) |
| `/api/pedidos?login=<cpf>` | GET | Reservas de um cliente |
| `/api/pedidos` | POST | Cria reserva, `{id_clientes, pessoas, data_pedido}` |
| `/api/pedidos/{id}/cancelar` | POST | Cancela uma reserva |
| `/api/admin/fault-mode` | GET/POST | Liga/desliga modos de falha (ver abaixo) |

### Injeção de falhas (fault injection)

Mecanismo pensado pra viabilizar Fuzzing/Mutação Dinâmica contra a
CobaiaAPI, o agente de QA precisa de um jeito determinístico e
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
| `type_drift` | Muda o tipo do campo `target_field` (ex.: número vira string) |
| `field_missing` | Remove `target_field` da resposta |
| `field_renamed` | Renomeia `target_field` para `<campo>_v2` |
| `malformed_json` | Responde um corpo JSON sintaticamente quebrado |

`probability` (0.0–1.0, default 1.0) controla a chance da falha disparar
por requisição, útil pra simular intermitência.

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
FastAPI serializar pelo `response_model` declarado, isso é o que permite a
injeção de falha realmente alterar o formato da resposta; se as rotas
dependessem do `response_model` normal, o Pydantic validaria e filtraria
silenciosamente qualquer campo alterado antes de sair pela rede.
`response_model` continua declarado nas rotas só pra gerar a documentação
OpenAPI do contrato "normal".

## AgenteCore: experimentos com os modelos locais

<!-- ! Alteração de IA - Revisar: seção nova descrevendo a bateria de experimentos e a
     biblioteca de documentação da Fase 2-B.
     ! Motivo: o README ainda dizia que o AgenteCore estava vazio; sem esta seção os
     integrantes não sabem a ordem dos scripts nem que nada deve rodar com outro modelo
     residente no Ollama. -->
Tudo em `Programacao/AgenteCore/experimentos/`, rodando com o Python da venv
do AgenteCore (`Programacao/AgenteCore/.venv`, criada pelo instalador).
**Regra de ouro: um modelo por vez**, os scripts conferem em `/api/ps` que
não há outro modelo residente, e toda inferência é forçada para CPU
(`num_gpu=0`) porque a tese afirma operar sob restrição de hardware local.

**Duas máquinas, duas pastas de resultado.** A Fase 2-A foi medida no Ryzen
de desenvolvimento (`resultados/`, `graficos/`, `relatorio.html` na raiz de
`experimentos/`). A Fase 2-B rodou na **máquina-alvo** (notebook corporativo
i5-1235U, 16 GB, sem GPU) e grava em `resultados_alvo/`, é a variável de
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
| todos | `rodar_fase2b.ps1` | Orquestra a Fase 2-B inteira **na máquina-alvo**: confere Python/Ollama/RAM/disco, baixa os 8 modelos que faltarem, grava `maquina.json`, refaz a linha de base A0 lá, roda A1–A5 e a avaliação, tudo em `resultados_alvo/`. Um modelo por vez, resumível (Ctrl+C e relançar), ~30–45 h: `powershell -ExecutionPolicy Bypass -File .\rodar_fase2b.ps1`. |

A leitura dos resultados fica em `RESULTADO_FASE2.md` (primeira leva, 2 casos) e em
[`Documentacao/memorial/3-resultados-e-analises/fase-2a-relatorio-por-modelo.md`](Documentacao/memorial/3-resultados-e-analises/fase-2a-relatorio-por-modelo.md)
(Fase 2-A, 90 casos × 3 estratégias × 6 modelos) e em
[`fase-2b-relatorio-por-modelo.md`](Documentacao/memorial/3-resultados-e-analises/fase-2b-relatorio-por-modelo.md)
(Fase 2-B, biblioteca de documentação, 2.610 inferências na máquina-alvo).
Decisões, pesquisa e fontes estão em `Documentacao/Memorial de Desenvolvimento.md`
(índice) e na pasta `Documentacao/memorial/`.

### Fase 3: biblioteca gerida pelo modelo

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
casos de aprendizado (54 dos 90, com gabarito), propõe acréscimos, nunca
reescreve nem apaga, que passam por validação em código antes de entrar.
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
     12/09/2026 (1 modelo, 10 casos, 1 época, 00h13; retomada com hash idêntico), a marca
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
| `avaliar_fase3.py` | Pontua por modelo × versão da biblioteca (L0..L3) × partição (aprendizado/avaliação/geral); McNemar pareado, Cochran Q entre as 4 épocas, IC de Wilson, trocas entre acerto e erro entre épocas. | `python avaliar_fase3.py` |
| `comparar_fases.py` | Junta 2-A, 2-B e Fase 3 num só `comparacao_fases.json`/`.md`, com os pareamentos que fazem sentido entre fases. | `python comparar_fases.py` |
| `gerar_graficos_fase3.py` | Figuras 12–17: acerto por época, recuperação por época, motivos de rejeição das propostas, crescimento da biblioteca, comparação entre as três fases. | `python gerar_graficos_fase3.py` (venv com matplotlib) |
| `gerar_relatorio_fase3.py` | `relatorio_fase3.html` navegável por modelo/época/partição, com cada proposta de edição (prompt, resposta crua, decisão do validador). | `python gerar_relatorio_fase3.py` |
| `testar_fase3.py` | Testes em Python puro (sem pytest) do parser, do validador, da aplicação de edição e do hash/diff, sem chamar o Ollama, < 30 s. | `python testar_fase3.py` |
| `rodar_fase3.ps1` | Orquestrador da Fase 3 nesta máquina: valida a biblioteca, roda os testes, executa os 4 modelos em sequência, avalia, compara as fases e gera gráficos/relatório. O piloto `-Piloto` (1 modelo, 10 casos, 1 época) rodou em 12/09/2026 em 00h13, e o teste de retomada reconstruiu a `epoca-1` com o mesmo hash, validação do encanamento feita; a bateria completa rodou em 13–15/09/2026 (57h59, 0 falhas; ver "Resultado da Fase 3" abaixo). | `.\rodar_fase3.ps1 -Piloto` (amostra pequena, 1 modelo, 1 época) antes da bateria completa: `.\rodar_fase3.ps1` |

<!-- ! Alteração de IA - Revisar: na tabela acima, a linha de `rodar_fase3.ps1` deixou de dizer que "a bateria completa ainda não rodou".
     ! Motivo: a bateria rodou em 13–15/09/2026 (57h59, 0 falhas; parágrafo "Resultado da Fase 3" abaixo) e a frase, esquecida na revisão de 21/09, contradizia o resto da seção. -->
<!-- ! Alteração de IA - Revisar: duração da Fase 3 corrigida de 58h59 para 57h59 em 30/09/2026, na linha de `rodar_fase3.ps1` da tabela acima e no parágrafo "Resultado da Fase 3".
     ! Motivo: a bateria rodou de 13/09 08:45:25 a 15/09 18:44:56 pelos marcos do `fase3.log`; a linha FIM do log diz 58h59 porque o script convertia as horas com `[int]`, que no PowerShell arredonda para o inteiro mais próximo. O defeito apareceu na ponte de 30/09 (1h46 gravadas como 02h46) e foi corrigido nos três scripts de bateria. -->
Cada modelo grava em `resultados_alvo/fase3/`:

<!-- ! Alteração de IA - Revisar: na árvore abaixo, o fase3.log passou a "versionado" (29/09/2026).
     ! Motivo: desde 29/09 o .gitignore tem uma exceção ao *.log para resultados_alvo/**/*.log, a pedido do Eric (decisão 63); a nota antiga dizia que o log ficava fora do git. -->
```
fase3/
  maquina.json               máquina, versão do Ollama, RAM e horário de início (relances são acrescentados, não sobrescrevem)
  particao.json              divisão determinística dos 90 casos em aprendizado (54) e avaliação (36)
  fase3.log                  registro corrido da execução, gravado pelo rodar_fase3.ps1 (versionado: exceção ao *.log no .gitignore)
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

<!-- ! Alteração de IA - Revisar: segunda passada de 12/09/2026, o comando da projeção
     ganhou `--modelos` com os quatro modelos.
     ! Motivo: `python executar_fase3.py --so-projecao` sozinho encerra com "the following
     arguments are required: --modelos" (`required=True` no argparse de `executar_fase3.py`);
     o 67,18 h só se reproduz com os quatro modelos na linha de comando, que é o que
     `rodar_fase3.ps1` faz antes da corrida (saída conferida em 12/09/2026). -->
Estimativa de custo: **~60 h de máquina** para os 4 modelos × 3 épocas no
plano; a projeção que o executor imprime (`python executar_fase3.py
--so-projecao --modelos granite4.2:8b qwen2.5:7b qwen2.5-coder:7b
qwen2.5-coder:3b`, `--modelos` é obrigatório; é o comando que `rodar_fase3.ps1`
roda antes da corrida, com os ms/token medidos na 2-B) dá **67,18 h**. O piloto de 10
casos (`-Piloto`) rodou em 12/09/2026 em 00h13, `qwen2.5-coder:3b`, 1 época,
0 de 6 propostas aceitas, e valida o encanamento, não o custo dos quatro
modelos. A bateria é **retomável**: interromper com Ctrl+C e rodar de novo
continua da mesma época e do mesmo caso, sem repetir trabalho já fechado.

<!-- ! Alteração de IA - Revisar: em 21/09/2026 entraram o parágrafo "Resultado da Fase 3", a subseção "Fase 3-B" e a seção "Ferramentas de apoio".
     ! Motivo: a bateria da Fase 3 rodou em 13–15/09/2026 e o README ainda descrevia só a preparação; a Fase 3-B (executor próprio, sem tocar nos scripts oficiais) e a pasta `ferramentas/` são novas no repositório e ninguém saberia para que servem sem esta descrição. Números só com origem: `resultados_alvo/fase3/fase3.log` e `comparacao_fases.md`. -->
**Resultado da Fase 3 (13–15/09/2026).** A bateria rodou na máquina-alvo de
13/09 08:45 a 15/09 18:44 (57h59, sem falhas, Ollama 0.34.0; a linha `FIM` do
`fase3.log` diz 58h59 porque o script arredondava a hora), 2.088 inferências, e
os resultados estão em
`resultados_alvo/fase3/` (commit `b9f9ad9`). As tabelas por modelo e fase estão
em `resultados_alvo/fase3/comparacao_fases.md`; a leitura está no Memorial
(`Documentacao/memorial/3-resultados-e-analises/`, relatório e comparação
preenchidos em 22/09/2026). **Decisão do modelo (22/09/2026, decisão 52):
`qwen2.5:7b` com a biblioteca no estado L1**, pela regra pré-registrada
(`decidir_modelo.py`, que grava `resultados_alvo/fase3/decisao_modelo.md`: 91,7% de
acurácia balanceada nos 36 casos de avaliação, sem veto por autoenvenenamento;
P(top-1) de 77,6% no bootstrap); análise completa em
`Documentacao/memorial/3-resultados-e-analises/analise-decisoria-modelo-final.md`.
As tabelas do Memorial saem de `gerar_tabelas_relatorio_fase3.py` como blocos
conferidos por `--check` (`resultados_alvo/fase3/tabelas_relatorio.md`).

### Fase 3-B: ponte de versão e testes complementares

Depois da bateria o Ollama atualizou sozinho de 0.34.0 para 0.34.1 e, em 30/09,
para 0.34.4. Qualquer inferência nova passa antes por uma **ponte de versão** (L0
nos 36 casos de avaliação) que mede se o runtime novo reproduz o antigo; só então os
testes complementares escolhidos em 23/09/2026 (decisão 56): os 36 casos inéditos,
que rodaram em 28/09, e a troca cruzada de bibliotecas entre modelos, que rodou de
30/09 para 01/10; a sonda de detecção de correção, a ablação base × instruct e o
experimento do recuperador entraram depois. Tudo roda por um executor **próprio**, que
lê **cópias** dos snapshots oficiais e nunca altera `executar_fase3.py`,
`estrategias.py`, `evolucao_biblioteca.py` nem `resultados_alvo/fase3/`.

| Script | O que faz | Como rodar |
|---|---|---|
| `executar_fase3b.py` | Modos `ponte`, `cruzada` (`--doador`, `--versoes`), `texto_max` (`--texto-max`, só granite), `a5` e `ineditos`; copia o snapshot pedido para a pasta da saída, grava `condicoes_3b.json` e `maquina.json` e chama a "passada final" de `executar_fase3.rodar_epoca` (só diagnóstico). | `python executar_fase3b.py --modo ponte --saida fase3b_ponte --modelos …` |
| `avaliar_fase3b.py` | Avalia a saída de um modo: os quatro primeiros delegam a `avaliar_fase3.avaliar_saida`; `ineditos` agrega com o gabarito de cada registro. | `python avaliar_fase3b.py --saida fase3b_ponte` |
| `testar_fase3b.py` | Testes sem LLM (cópia preserva o hash, modos aplicam e restauram `TEXTO_MAX`/`CONDICAO`, área oficial intocada antes e depois da suíte). | `python testar_fase3b.py` |
| `rodar_fase3b.ps1` | Orquestrador: testes, um modelo por vez com checagem de RAM (pula e lista o modelo se faltar memória; relançar retoma), avaliação ao fim. | `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo ponte -Saida fase3b_ponte` |
| `decidir_modelo.py` (+ `pesos_decisao.json`, `gerar_graficos_decisao.py`) | Decide modelo e estado da biblioteca pela regra pré-registrada (decisão 36) e mede a robustez (bootstrap, estabilidade, Pareto, escore ponderado com sensibilidade), pareia as saídas da 3-B com a Fase 3 e apura a revisão das edições; grava `decisao_modelo.json/.md` (documento derivado) e a figura 18. | `python decidir_modelo.py --saida fase3 --saidas-3b fase3b_ponte` (`--check` confere) |
| `gerar_tabelas_relatorio_fase3.py` | Tabelas do relatório da Fase 3, da comparação entre fases e da análise decisória (Memorial) a partir de `resumo_fase3.json`, `comparacao_fases.md`, `decisao_modelo.md` e `fase3.log`, como blocos `<!-- tabela:NOME -->`; `--check` acusa qualquer bloco colado que difira do regerado. | `python gerar_tabelas_relatorio_fase3.py --saida fase3 [--check]` |
| `sonda_correcao.py` | Sonda de **detecção de correção** (28/09/2026, decisão 58): roda uma época de aprendizado do executor oficial sobre uma cópia de um snapshot fechado, só com os casos corrigidos, e imprime o que o modelo diagnosticou e propôs ao rever um caso cuja documentação (escrita por ele mesmo) ficou desatualizada; saída em `resultados_alvo/<saida>/`. | `RESULTADOS_DIR=resultados_alvo python sonda_correcao.py --saida fase3b_correcao --modelo qwen2.5:7b --versao 1 --casos efe-3 efe-10` |
| `curar_biblioteca.py` | Curadoria da biblioteca L1 do `qwen2.5:7b` (29/09/2026, ficha 2): `--listar` escreve a planilha `resultados_alvo/fase3/curadoria_L1__qwen2.5_7b.md` (40 edições da época 1, 10 com veredito da planilha oficial); `--curar --destino ../biblioteca_producao` reconstrói a cópia de produção a partir da época 0 reaplicando só o que não for *Errada*, depois de conferir que reaplicar tudo reproduz o hash oficial; grava `curadoria.json`. | `RESULTADOS_DIR=resultados_alvo python curar_biblioteca.py --listar` |
| `comparar_qwen_coder.py` | Comparativo `qwen2.5:7b` × `qwen2.5-coder:7b` em todas as fases (29/09/2026, ficha 4): tabelas, confronto caso a caso (McNemar exato) e a lista de toda célula em que o Coder fica à frente; grava `resultados_alvo/fase3/comparativo_qwen_coder.{json,md}`; `--colar` cola os blocos em `Documentacao/memorial/3-resultados-e-analises/comparativo-qwen25-7b-vs-coder-7b.md`; `--check`. | `RESULTADOS_DIR=resultados_alvo python comparar_qwen_coder.py` |
| `experimento_recuperador.py` | Experimento offline do recuperador (29/09/2026, ficha 11f): BM25 com sinais × embedding denso (`embeddinggemma:300m`, consulta por termos e por texto) × híbrido RRF, k = 1/3/5, nos 90 oficiais e nos 36 inéditos, bibliotecas L0/L1/L3; saída em `resultados_alvo/recuperador/` (`.json` registro, `.md` derivado com `--check`). | `RESULTADOS_DIR=resultados_alvo python experimento_recuperador.py --embedding embeddinggemma:300m` |
| `analisar_fase3b.py` | Análise de fechamento da Fase 3-B (01/10/2026): pontes de versão, casos que mudam entre corridas iguais, inéditos somados aos oficiais (72 casos) e troca cruzada pareada contra a ponte, contra a própria biblioteca e contra o doador; grava `resultados_alvo/fase3/analise_fase3b.{json,md}`; `--colar` cola os blocos em `Documentacao/memorial/3-resultados-e-analises/fase-3b-relatorio.md`; `--check`. | `RESULTADOS_DIR=resultados_alvo python analisar_fase3b.py [--check]` |
| `viabilidade_modelos_grandes.py` | Pré-Fase 4: para cada família de modelo do repositório colibri, se cabe no disco e na RAM desta máquina, quanto o disco custaria por token e quanto levaria a nossa resposta mediana nas velocidades medidas por terceiros; grava `resultados_alvo/pre_fase4/viabilidade_modelos_grandes.{json,md}` (`--check`, `--colar`). |
| `sondar_logprobs.py` | Pré-Fase 4: confere com três chamadas o que o Ollama devolve de probabilidade por token (`logprobs`, `top_logprobs`) e traz o gancho `com_logprobs`, que acrescenta os dois campos à chamada de `cliente_ollama.gerar` sem mudar o que ela devolve. |
| `sonda_confianca.py` (+ `rodar_sonda_confianca.ps1`) | Pré-Fase 4: o modelo decidido com a biblioteca dele nos 36 casos oficiais de avaliação e nos 36 inéditos, com o mesmo executor e o mesmo prompt da Fase 3, gravando a probabilidade de cada token em `logprobs__L<n>.jsonl` ao lado do registro (que mantém as 37 chaves oficiais). |
| `analisar_confianca.py` | Pré-Fase 4: analisa a sonda de confiança. Acha nos tokens gravados o trecho do rótulo da causa, calcula a probabilidade conjunta dele (a medida principal, fixada antes da corrida), a do primeiro token e a massa das alternativas que levariam a outra causa, e mede se separam acerto de erro (AUROC com intervalo por reamostragem dos casos, risco por cobertura, quantos erros uma parcela de revisão humana pega), ao lado dos dois sinais que não custam inferência; grava `resultados_alvo/pre_fase4/confianca.{json,md}` (`--check`, `--colar`). O script da noite roda a análise no fim. |
| `pre_fase4.py` | Pré-Fase 4: pasta dos derivados da fase (`resultados_alvo/pre_fase4/`) e a rotina comum de gravar, conferir (`--check`) e colar os blocos de tabela de cada script no relatório. |
| `trilha.py` | Pré-Fase 4: a trilha do agente, o arquivo bruto com uma linha JSON por evento (o caso, os verbetes que a busca pontuou e entregou, o prompt, a resposta, o que o modelo declarou e o que o código conferiu), em três camadas que não se misturam; o adaptador remonta a trilha das corridas já gravadas, sem rodar modelo, e diz até onde o prompt remontado está provado; `--errata` recupera do git o texto antigo dos dois casos corrigidos em 28/09. |
| `gerar_relatorio_raciocinio.py` | Pré-Fase 4: gera, só da trilha, o relatório para humanos de cada diagnóstico (passo a passo nas três camadas; a resposta certa aparece numa seção só), o índice de cada corrida e os indicadores somados; `--vitrine` grava as trilhas e os relatórios versionados em `resultados_alvo/pre_fase4/` (`--check`, `--colar`). |
| `gerar_atlas.py` | Pré-Fase 4: o atlas do projeto com os dados já medidos, pelo método do `expert_atlas` do colibri: para cada versão da biblioteca, em quantos casos de cada classe de defeito cada verbete entrou no contexto, a especialização, a validação deixando um caso de fora, as citações e as trocas entre causas de cada corrida e a rota de cada caso; grava `resultados_alvo/pre_fase4/atlas.{json,md}` (`--check`, `--colar`). |
| `testar_pre_fase4.py` | Testes sem LLM da Pré-Fase 4 (leitura do disco, gancho das probabilidades, conta de viabilidade, sonda de confiança com Ollama de mentira, trilha, relatório de raciocínio, atlas, pastas oficiais intocadas antes e depois). |
| `cache_respostas.py` (+ `testar_cache_respostas.py`) | Cache **exato** de respostas do Ollama (SQLite; chave = modelo, digest, prompt, opções) para reexecuções de conveniência e para o laço de desenvolvimento da Fase 4; desligado por padrão (`CACHE_RESPOSTAS=1` liga), recusa em `resultados_alvo/` e marca todo acerto com `do_cache=True` e tempos zerados, nunca entra numa corrida medida (decisão 48). | `set CACHE_RESPOSTAS=1` e `gerar_com_cache(...)` no lugar de `cliente_ollama.gerar` |

Cada modo grava em `resultados_alvo/<saida>/` a mesma árvore da Fase 3 (snapshots
copiados em `bibliotecas/<slug>/`, `diagnosticos__L<n>.jsonl` por modelo,
`avaliacao_fase3.json`, `resumo_fase3.json`) mais `condicoes_3b.json` (modo, doador,
versões, teto de texto, condição, versão do Ollama). A ponte de 21/09/2026 cobriu
`qwen2.5-coder:3b`, `qwen2.5:7b` e `qwen2.5-coder:7b` (b/c 0/0, 1/1 e 0/0 nos 36:
pareáveis com a Fase 3); o `granite4.2:8b` foi pulado duas vezes por RAM (8 GB
exigidos, 7,8 GB livres) e ficou fora da 3-B (decisão 52).

<!-- ! Alteração de IA - Revisar: linhas novas (01/10/2026) para os scripts da Pré-Fase 4 nas duas tabelas, a fase na tabela de fases e no estado do topo.
     ! Motivo: decisão 70 (pausa de pesquisa antes da Fase 4); os scripts são novos no repositório e o README é a porta de entrada que diz o que cada um faz. -->
<!-- ! Alteração de IA - Revisar: parágrafo novo (01/10/2026) com o resultado da Fase 3-B, a linha de `analisar_fase3b.py` na tabela acima e o estado da 3-B no topo e na tabela de fases.
     ! Motivo: a troca cruzada rodou de 30/09 para 01/10 e era o último teste previsto; o README ainda dizia que ela estava pendente. Números de `resultados_alvo/fase3/analise_fase3b.json`. -->
**Resultado da Fase 3-B (01/10/2026).** A segunda ponte, em Ollama 0.34.4, deixou o `qwen2.5-coder:7b` fora do limite (b/c 3/1 nos 36), e por isso a troca cruzada é lida contra essa ponte. Nos 36 casos inéditos o ganho da biblioteca L1 não reaparece (72,2% contra 75,0% com a biblioteca original; a L3 chega a 80,6%). Na troca cruzada, a biblioteca escrita pelo `qwen2.5:7b` dá 1 caso de saldo ao Coder 7B e tira 4 do Coder 3B, contra 88,9% de acerto quando lida por quem a escreveu: o padrão do agente é o modelo com a biblioteca que ele mesmo escreveu (decisão 69). Com a mesma entrada, entre corridas iguais mudam de 0 a 3 casos em 36. A análise sai de `analisar_fase3b.py`, e o relatório, com a lista de fechamento das Fases 3 e 3-B, está em `Documentacao/memorial/3-resultados-e-analises/fase-3b-relatorio.md`.

<!-- ! Alteração de IA - Revisar: parágrafo abaixo com os testes da 3-B escolhidos pelo Eric em 23/09/2026, os comandos na forma que o Windows PowerShell aceita por -File (listas separadas por vírgula) e o efeito da decisão do modelo no instalador.
     ! Motivo: o texto anterior dizia "testes a escolher"; a escolha saiu (decisão 56) e o comando registrado antes nas pendências, com a lista separada por espaço, falha na vinculação de parâmetros do PowerShell (conferido em 23/09/2026 com um script de teste). O `install.py` passou a baixar o `qwen2.5:7b` e os outros modelos ficam só como registro. -->
**Testes da 3-B escolhidos (23/09/2026, decisão 56).** Primeiro a **troca cruzada**, as bibliotecas L1 e L3 do `qwen2.5:7b` lidas pelos dois Coder nos 36 casos de avaliação:

```
powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo cruzada -Saida fase3b_cruzada_qwen -Doador qwen2.5:7b -Versoes 1,3 -Modelos qwen2.5-coder:7b,qwen2.5-coder:3b
```

Depois os **casos inéditos** (`banco_casos_ineditos.py`: 36 casos novos, 2 por célula classe × nível, escritos só a partir do código do cobaia, ids `lex-16` a `efe-21`), com o `qwen2.5:7b` e o 3B em L0, L1 e L3:

```
powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo ineditos -Saida fase3b_ineditos -Versoes 0,1,3 -Modelos qwen2.5:7b,qwen2.5-coder:3b
```

As listas vão separadas por **vírgula** (`-File` do Windows PowerShell 5.1 vincula `a b` como dois argumentos e falha). Com a decisão tomada, o `install.py` passou a baixar o `qwen2.5:7b` por padrão; os outros modelos ficam só como registro histórico, resultados, gráficos e o veredito de cada um em `Documentacao/memorial/3-resultados-e-analises/analise-decisoria-modelo-final.md` §8. O painel do projeto, pendências em fichas, roadmap com os comandos prontos e todos os números dos testes numa página só, está em `Documentacao/dashboard/painel-do-projeto.html` (gerado por `ferramentas/gerar_dashboard.py` e publicado em https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN para leitura de qualquer lugar); o estado por fase, com o que falta rodar, em `Documentacao/memorial/roadmap.md`, e as decisões que esperam resposta, em fichas, em `Documentacao/memorial/pendencias.md`.

## Ferramentas de apoio ao trabalho com IA (`ferramentas/`)

Scripts em Python padrão, sem dependência, que fazem localmente o que antes se
pedia a agentes (regra registrada no `CLAUDE.md`: primeiro a máquina, depois o
modelo):

<!-- ! Alteração de IA - Revisar: na tabela abaixo, a linha de `medir_tokens.py` ganhou a opção `--agentes` (29/09/2026).
     ! Motivo: a regra de permanência do servidor MCP comparou a mesma tarefa feita por subagentes com ferramentas diferentes, e o agregado por dia, modelo e tipo misturava todos os subagentes da sessão. -->
<!-- ! Alteração de IA - Revisar: na tabela abaixo, a linha de `gerar_dashboard.py` foi reescrita e entrou a linha de `painel_topicos.py` (30/09/2026).
     ! Motivo: o Eric pediu a aba do comparativo qwen × Coder e que o painel fosse o compilador das análises, com uma aba por tópico; a linha antiga ainda descrevia o painel só com as abas de 28/09. -->
| Script | O que faz |
|---|---|
| `gerar_dashboard.py` | Painel do projeto (`Documentacao/dashboard/painel-do-projeto.html`, HTML único), o compilador das análises: navegação em cinco grupos (Projeto, Modelos, Biblioteca, Fases anteriores, Pesquisa e método), abas Início (estado por fase, o que depende do Eric, mapa do painel), Pendências (um cartão por ficha de `pendencias.md`, com filtro), Roadmap (fases e corridas de `roadmap.md`, com o comando pronto) e as abas dos testes, lê `resumo_fase3.json`, `comparacao_fases.json`, `decisao_modelo.json`, os resumos das Fases 2-A/2-B, os 29 blocos de `tabelas_relatorio.md` e as figuras 01–18, monta gráficos (Chart.js, paleta validada da regra de gráficos, com tema escuro) e recebe as abas por tópico de `painel_topicos.py`; `--check` regera e compara. |
| `medir_disco.py` | Pré-Fase 4: mede a vazão de leitura do disco no desenho do `iobench` do colibri (blocos de 19 MB, 64 leituras, 8 threads), passando pelo cache do sistema e por fora dele, e grava `resultados_alvo/pre_fase4/disco.json` com a descrição da máquina. |
| `integrar_pesquisa_documentacao.py` | Rodada 4 do levantamento (29/09/2026, qualidade da documentação autogerida): `--montar` junta pesquisa + verificação + síntese de `.superpowers/sdd/fase3b-e-fechamento/pesquisa/r4/` em `r4-final.json`; a integração grava `levantamento-2026-09-29-documentacao-autogerida.md` (§6.13), o bloco de referências e a linha no índice do Memorial; `--check`. |
| `integrar_pesquisa_pre_fase4.py` (+ `testar_integrar_pesquisa_pre_fase4.py`) | Rodada 5 do levantamento (01/10/2026, Pré-Fase 4), em duas partes: integra ao Memorial as partes que já rodaram, com numeração fixa (§6.14.1 a §6.14.11, §6.14.12 rejeitadas, §6.14.13 mapas), regrava o bloco de referências sem repetir fonte (pela chave das outras rodadas e pelo endereço) e a linha do índice; troca pelo número medido a expressão imprecisa do contexto dado aos agentes e declara a troca; `--check`. |
| `correcoes_pesquisa_pre_fase4.py` | As 156 correções declaradas das sínteses e do mapa da parte A da rodada 5 (trecho antigo, novo e motivo), que o integrador aplica e lista no §6.14.12 do levantamento; cada trecho tem de aparecer uma vez só no texto do agente, senão a integração para |
| `gerar_pdf_abnt.py` | PDF (versão beta) do projeto de pesquisa a partir do Markdown, sem as marcações de IA (retiradas só da cópia), com folha de estilo ABNT e impressão pelo Microsoft Edge em modo sem janela; grava `Documentacao/Projeto de Pesquisa - ABNT 15287_2025 - V4-beta.pdf`. |
| `painel_textos.py` (+ `testar_painel_textos.py`) | Leitura das fichas de `pendencias.md` (`### N. Título` + campos Estado / Quem decide / O que é / Por que importa / Opções / Recomendação / Decisão) e das tabelas de `roadmap.md` (estado por fase; corridas com a coluna Estado) para o painel, e conversão do resto dos dois documentos em HTML; o teste confere o formato dos arquivos reais. |
| `painel_topicos.py` (+ `testar_painel_topicos.py`) | Abas por tópico do painel (30/09/2026): qwen × Coder (`comparativo_qwen_coder.json`), Fase 3-B (`fase3b_ineditos/resumo_fase3.json`, ponte, sonda, corridas), curadoria da L1 (`curadoria.json` + planilha), recuperador (`experimento_recuperador.json`), ablação base × instruct (`ablacao_base_instruct/resumo_metricas.json`), pesquisa (títulos dos levantamentos e o mapa de filtros da rodada 4) e ferramental (esta tabela e a medição do servidor MCP). Cada aba: pergunta, resposta em uma frase, números-chave, um ou dois gráficos, leitura curta e tabelas recolhidas; nenhum número digitado à mão. |
| `painel_atlas.py` | Aba Atlas do painel (01/10/2026): o mapa dos verbetes pelas seis classes de defeito, desenhado em SVG no próprio Python e movido por um script simples na página (biblioteca, quem leu, caso), o detalhe de cada verbete, a rota de cada caso, o acerto por causa com as trocas e um passeio guiado; lê `resultados_alvo/pre_fase4/atlas.json`. |
| `painel_explorador.py` | Explorador de casos da aba "Raciocínio aberto" do painel (01/10/2026): de cada trilha versionada, o recorte por caso das três camadas (o que o programa fez, o que o modelo declarou, o que o código conferiu) e, à parte e recolhida, a avaliação contra o gabarito. |
| `medir_tokens.py` | Soma o consumo de tokens do Claude Code a partir dos transcritos locais, por dia, modelo e tipo de agente (linha de base e medição "depois" das medidas de economia). `--agentes rótulo=id,...` soma só os subagentes pedidos (usado na regra de permanência do servidor MCP, 29/09/2026). |
| `resumir_saida.py` / `gancho_pre_bash.py` | Hook `PreToolUse` do Claude Code (`.claude/settings.json`) que encurta a saída de comandos longos (testes, baterias, `git diff`) antes de ela entrar no contexto. |
| `conferir_docs.py` | Confere a documentação antes de entregar: links relativos, tag `! Alteração de IA - Revisar` com `! Motivo` em todo arquivo tocado, frases obsoletas, hipóteses H1–H6 idênticas, BOM e ausência de travessão nos `.ps1`. |
| `extrair_pesquisa.py`, `render_levantamento.py`, `integrar_pesquisa.py`, `integrar_pesquisa_llms.py` | Fecham as pesquisas bibliográficas por script: extraem os artefatos verificados, geram as subseções no formato do Memorial (com `--check`) e integram texto, referências (com dedup), mapa de decisões (Fase 3) e mapa adotado/adiado/descartado (LLMs locais, §6.12 e §7.9). |

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
     Corrigido em 11/09/2026 nos dois scripts; ver `claude-memoria/README.md`. -->
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

Experimentos, painel e documentação, sem chamar modelo nenhum:

```powershell
cd Programacao\AgenteCore\experimentos
python testar_fase3.py
python testar_fase3b.py
python testar_pre_fase4.py
cd ..\..\..
python ferramentas/testar_painel_textos.py
python ferramentas/testar_painel_topicos.py
python ferramentas/testar_integrar_pesquisa_pre_fase4.py
python ferramentas/gerar_dashboard.py --check
python ferramentas/conferir_docs.py
```

Os testes da CobaiaAPI rodam contra o **banco real** (não há banco de testes isolado,
é um ambiente cobaia, não produção), então rode `install.ps1`/`install.sh`
pelo menos uma vez antes.

## O que é versionado e por quê

O repositório é deliberadamente "hit and run": versionamos **muito mais que
o normal** para que quem clonar precise do mínimo de passos. Fica de fora só
o que não funcionaria na máquina de outra pessoa, ou o que se regenera
sozinho, versionar essas coisas atrapalharia o "hit and run" em vez de
ajudar.

<!-- ! Alteração de IA - Revisar: em 12/09/2026 a tabela ganhou as duas linhas de `.superpowers/`
     e de `resultados_alvo/fase3_piloto/`, que já estavam no `.gitignore` (linhas 19 e 25).
     ! Motivo: as duas regras entraram no `.gitignore` em 11/09/2026 com comentário lá, mas esta
     tabela, que é onde o README explica o que fica fora do git e por quê, não as citava, e
     quem procurasse aqui o motivo de o piloto não estar versionado não achava. -->
<!-- ! Alteração de IA - Revisar: na tabela abaixo, a linha de `.mcp.json`/`.cbmignore` passou a "Não, removidos" (29/09/2026).
     ! Motivo: a linha dizia que os dois ficavam se a regra de permanência fosse cumprida; ela foi medida e o servidor saiu. -->
| Item | Versionado? | Por quê |
|---|---|---|
| `Cobaia.exe` (8.6 MB) | **Sim** | É o próprio entregável "hit and run" do Windows: clonou, deu duplo clique, rodou, sem precisar nem de Python instalado pra compilar. Elimina o risco de "o build falhou 5 min antes da banca". Precisa ser recompilado (`build_exe.ps1`) quando `Cobaia.py`/`install.py`/`run.py`/`_env_common.py` mudarem. |
| `Cobaia.spec` | **Sim** | Receita de recompilação (arquivo texto pequeno). |
| `Programacao/CobaiaFront/` inteiro (16 MB, sendo 13 MB de imagens) | **Sim** | Imagens, CSS/JS do Bootstrap e PHPMailer são carregados localmente pelo site, sem eles o CobaiaFront não renderiza. Não há passo de build/download que os recupere. |
| `banco/*.sql` | **Sim** | Schema + seed. É o que faz o site funcionar de verdade. |
| `.env.example` | **Sim** | Template de configuração (o `.env` real fica de fora). |
| `Programacao/CobaiaAPI/.venv/` (67 MB) | **Não** | Verificado: o `pyvenv.cfg` grava caminhos absolutos desta máquina (`home = C:\Python314`) e a pasta tem 16 `.exe` + 14 `.pyd` (binários Windows) e nenhum `bin/`. É **inutilizável no Linux** e quebra em outra máquina Windows. São 67 MB que enganam quem clona, e o instalador recria a venv correta pra cada SO em ~30s. |
| `__pycache__/`, `*.pyc` | **Não** | Cache de bytecode: derivado, regenerado sozinho, muda a cada execução e polui o diff. |
| `.env` | **Não** | Configuração local. Use o `.env.example` como base. |
| `build/`, `dist/` | **Não** | Artefatos transitórios do PyInstaller (o `.exe` final é gravado na raiz, esses ficam no `%TEMP%`). |
| `node_modules/`, browsers do Playwright | **Não** | Trabalho futuro do AgenteCore, centenas de MB, específicos de cada SO, baixados por instalador. |
| `.claude/` (menos `settings.local.json`) | **Sim** | Configuração do projeto para o Claude Code: `CLAUDE.md`, `settings.json` (hook que resume saídas longas, permissões de leitura, plugin de estilo desligado), `rules/` por tipo de arquivo e `skills/` copiadas, precisa chegar à outra máquina pelo git (decisão do Eric, 21/09/2026). Só `settings.local.json` (permissões concedidas nesta máquina) fica de fora. |
| `.superpowers/` | **Não** | Rascunho de sessão do Claude Code (livro-razão, briefs e relatórios de tarefa da Fase 3); mesma natureza de `.claude/`. |
| `.mcp.json`, `.cbmignore` | **Não, removidos em 29/09/2026** | Registro do servidor `codebase-memory-mcp` em escopo de projeto e as exclusões do índice (22/09/2026, decisão 49). A regra de permanência foi medida em 29/09 com três tarefas fixas (grep × servidor, duas vezes cada): o servidor gastou 8,6% a mais de tokens no total e 4,3% a menos nos novos, sem chegar aos 20% de corte, e saiu junto com o pacote npm (decisão 62; ferramental §7.2). |
| `Documentacao/notebooks/` | **Não** | Notebooks e dados de apoio do livro-texto (Faceli et al., 3. ed., 2025), baixados pelo QR code do livro: material dos autores e da editora, sem licença declarada, 330 MB em 53 mil arquivos que nenhum script do projeto usa. Quem tem o livro baixa a pasta por conta própria; ela é citada no fichamento (decisão 68). |
| `resultados_alvo/**/*.log` | **Sim** | Registro corrido de cada bateria (início e fim de cada modelo, relances, falhas, versão do Ollama); exceção ao `*.log` genérico desde 29/09/2026 (decisão 63). |
| `Documentacao/dashboard/painel-do-projeto.html` | **Sim** | Gerado por `ferramentas/gerar_dashboard.py` a partir dos registros; versionado para o painel abrir em qualquer clone, e `--check` acusa qualquer edição manual. |
| `Programacao/AgenteCore/experimentos/resultados_alvo/fase3_piloto/` | **Não** | Piloto da Fase 3 (1 modelo, 10 casos, 1 época): existe para conferir o encanamento e calibrar o tempo antes das ~60 h; seus JSONL e snapshots confundiriam a leitura de `resultados_alvo/fase3/`, que é o que vale. |

O "hit and run" continua íntegro sem a venv, porque os dois caminhos a
recriam automaticamente:
- **Windows:** duplo clique em `Cobaia.exe`: instala (inclui criar a venv), sobe tudo e abre o navegador.
- **Linux/macOS:** `./install.sh && ./run.sh` faz a mesma coisa.

## Decisões técnicas e problemas resolvidos

Documentado aqui porque cada um foi descoberto testando ao vivo, não
teorizado, importante pra quem for mexer no ambiente depois entender o
porquê:

- **XAMPP foi descartado.** O objetivo era um instalador silencioso e
  roteirizável em 3 SOs; o instalador GUI do XAMPP não se presta bem a
  isso. PHP e MariaDB nativos, instalados via linha de comando
  (`winget`/`apt`/`brew`), resolvem sem essa fricção.
- **MariaDB no Windows não registra serviço.** Testado nesta máquina sem
  privilégios de administrador: o `winget install MariaDB.Server` instala
  os binários e já inicializa o data dir (root sem senha), mas não registra
  um Windows Service (isso exigiria elevação). Por isso o MariaDB é sempre
  gerenciado como subprocesso direto no Windows, igual ao PHP e ao uvicorn; 
  ver `_env_common.py::ensure_mariadb_running`.
- **`extension_dir` do PHP vem hardcoded errado.** O build Windows do PHP
  aponta por padrão pra `C:\php\ext`, que não bate com o caminho real de
  instalação do winget. `_env_common.py::php_extension_flags` calcula o
  caminho certo dinamicamente a partir do binário encontrado.
- **`mbstring` é obrigatória, não opcional.** `mb_strimwidth()` é usada em
  5 páginas de produtos (incluindo a home), sem a extensão carregada, é
  **erro fatal**, não warning. Só foi percebido testando a home page a
  fundo (um teste superficial só com `grep` não pegou, porque o conteúdo
  antes do ponto de falha ainda aparecia no HTML).
- **`output_buffering` precisa estar ligado.** `cliente/index.php` ecoa
  HTML antes de `reserva_cli.php` incluir `admin/acesso_com.php`, que só
  então chama `session_start()`, um bug de ordenação pré-existente no
  código original. Um XAMPP/Apache real normalmente mascara isso porque
  `output_buffering` costuma vir ligado por padrão. Sem isso, a sessão de
  login não é retomada corretamente e a página trunca logo após a
  saudação. Resolvido via flag de configuração do PHP (não altera nenhum
  arquivo `.php`).
- **`vw_tbpedidos` usa `LEFT JOIN`, não `JOIN`.** Na primeira versão da
  view (criada do zero, o dump original não tinha essa tabela/view), um
  `JOIN` normal a partir de `tbpedido_reserva` fazia um cliente **sem
  nenhuma reserva ainda** sumir inteiramente da view, quebrando a
  saudação com "Trying to access array offset on value of type null".
  Corrigido fazendo `LEFT JOIN` a partir de `tbusuarios`, e usando
  `u.id_usuario` (não `pr.id_clientes`) como `id_clientes`, assim o campo
  continua correto mesmo sem nenhuma reserva prévia.

## Problemas conhecidos (deixados de propósito)

Decisão do grupo: manter `CobaiaFront` como veio, sem correções de código,
exceto o único caso de segurança justificado abaixo.

| Item | Situação |
|---|---|
| Link "Saiba Mais..." nas listagens de produtos | Aspas do `href` no lugar errado (bug do código original), sempre abre `id_produto=` vazio. Não corrigido. |
| Senha de usuário: texto puro no insert, MD5 no update, sem hash no login | Inconsistência do código original. Não corrigido, o `seed.sql` sempre insere em texto puro, então não afeta o login das contas de teste. |
| Credencial SMTP real hardcoded em `rodape_contato_envia.php` | Decisão explícita do grupo: como é ambiente de teste sem dados reais, foi mantida como está. |

## Segurança

Este é um **ambiente de teste** (cobaia), não um sistema em produção:
credenciais fracas/hardcoded, SQL injection nas queries do CobaiaFront, e
CORS liberado (`*`) na CobaiaAPI são conhecidos e intencionalmente não
corrigidos, fazem parte do escopo de cenários que o agente de QA deve ser
capaz de lidar. Não reutilize esses padrões fora deste projeto. A política de
segurança do repositório, com o canal privado para relatar problemas reais nos
instaladores e nas ferramentas, está em [SECURITY.md](SECURITY.md).

## Troubleshooting

- **`.\install.ps1 : ... a execução de scripts foi desabilitada neste
  sistema` (PSSecurityException):** é a Execution Policy padrão do Windows,
  que bloqueia scripts `.ps1` não assinados, não é um bug do projeto. Use
  `install.cmd`/`run.cmd` em vez de chamar os `.ps1` diretamente (eles
  chamam o PowerShell com `-ExecutionPolicy Bypass`, que vale só pra aquela
  execução, sem mudar nenhuma configuração persistente do sistema). Se
  preferir rodar o `.ps1` direto mesmo assim:
  `powershell -ExecutionPolicy Bypass -File .\install.ps1`.
- **`winget install` parece ter funcionado mas o comando ainda não é
  encontrado:** normal, o PATH só atualiza numa sessão de terminal nova.
  `install.py`/`run.py` já lidam com isso procurando o executável
  diretamente nos caminhos de instalação conhecidos, sem depender do PATH.
- **Porta 8080 ou 8000 já em uso:** edite `FRONT_PORT`/`API_PORT` no topo
  de `run.py`.
- **Erro de conexão com o banco (`Access denied for user 'root'`):** o
  `connect.php` do CobaiaFront espera `root` sem senha. Rode o instalador
  de novo, ele tenta corrigir isso automaticamente; se persistir, ajuste
  manualmente (`ALTER USER 'root'@'localhost' IDENTIFIED BY '';`).
- **`ModuleNotFoundError` ao rodar a CobaiaAPI:** o venv não foi
  criado/atualizado. Rode `install.ps1`/`install.sh` de novo.

## Como contribuir

Leia o [guia de contribuição](CONTRIBUTING.md) (fluxo de trabalho, convenções,
o que nunca muda e os testes obrigatórios) e o
[código de conduta](CODE_OF_CONDUCT.md). Defeitos e propostas entram por issue,
com os modelos em `.github/ISSUE_TEMPLATE/`; pull requests seguem o modelo em
`.github/PULL_REQUEST_TEMPLATE.md`. Problemas de segurança reais seguem a
[política de segurança](SECURITY.md), pelo canal privado do GitHub.

## Como citar

O arquivo [`CITATION.cff`](CITATION.cff) alimenta o botão "Cite this repository"
do GitHub. Em texto:

> DERRE, E. C. et al. **Desenvolvimento de um agente de QA end-to-end (E2E)
> autônomo com capacidades de self-healing: focado na fronteira de integração.**
> Trabalho de Conclusão de Curso (Ciência da Computação). Universidade Cidade de
> São Paulo, São Paulo, 2026. Repositório: https://github.com/EricDerre/TCC.

## Licença

O código e a documentação deste repositório estão sob a [licença MIT](LICENSE).
Componentes de terceiros mantêm as próprias licenças: Bootstrap 3.3.7 e jQuery
(MIT) e PHPMailer 5.2.27 (LGPL 2.1, com o texto em
`Programacao/CobaiaFront/PHPMailer/LICENSE`) no CobaiaFront; AngularJS 1.6.9 e
Chart.js 4.4.1 carregados de CDN (MIT). Os notebooks de apoio do livro-texto
(Faceli et al., 3. ed., 2025) são material dos autores e da editora, ficam fora
do repositório e não estão cobertos por esta licença. Os modelos de
linguagem não são distribuídos aqui: o Ollama os baixa sob a licença de cada um
(Apache 2.0 para o `qwen2.5:7b` e o `qwen2.5-coder:7b`; Qwen Research License
para o `qwen2.5-coder:3b`).

## Autores

Grupo de Ciência da Computação da Universidade Cidade de São Paulo (UNICID),
2026: Eric Conde Derre, Erick do Carmo Esteves, Guilherme Penha dos Santos,
João Victor Fonseca Silva, Kennedy Fernando de Oliveira Gundim, Leandro
Henrique da Silva Patricio e Pedro Henrique Torres Gonçalves. O repositório é
mantido por
[@EricDerre](https://github.com/EricDerre).

## Convenções para alterações por IA

Ver [`.claude/CLAUDE.md`](.claude/CLAUDE.md) para as regras completas de
colaboração com IA neste repositório (não commitar automaticamente, marcar
alterações com `! Alteração de IA - Revisar`, conferir colunas reais antes
de escrever SQL, priorizar causa raiz sobre contorno).
