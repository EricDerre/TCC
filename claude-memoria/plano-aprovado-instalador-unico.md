<!-- ! Alteração de IA - Revisar: em 18/11/2026 o arquivo `plano-instalador-unico.md` passou a ser este `plano-aprovado-instalador-unico.md`, com o parágrafo de estado trocado pelo cabeçalho de aprovação (data, decisões 138 a 143 e a resposta de cada ficha) e a linha da ficha 83 preenchida na seção 10; o resto do texto do plano não foi reescrito.
     ! Motivo: o Eric aprovou o plano como está e respondeu as fichas 78 a 83 no quadro da sessão; o rito do projeto pede o texto aprovado congelado neste nome, com as respostas no cabeçalho, antes de qualquer código. O que mudar depois entra num anexo de desvios no fim do arquivo. -->
<!-- ! Alteração de IA - Revisar: arquivo novo (18/11/2026) com o plano do instalador único e do teste dos instaladores em máquina limpa, escrito para a aprovação do Eric a partir da leitura do instalador atual (`install.cmd`, `install.ps1`, `install.sh`, `install.py`, `_env_common.py`, `run.py`, `Cobaia.py`, `build_exe.ps1`, `testar_instalador.py`), das medidas da máquina e das três pesquisas guardadas em `Documentacao/memorial/5-metodo-e-ferramental/dados/instalador/`, e das respostas dele às fichas 78 a 82 (decisões 138 a 142).
     ! Motivo: em 18/11/2026 o Eric pediu o teste dos instaladores "hit and run" em Windows, Linux e macOS, em máquina recém-criada, com e sem o Defender, com as versões das ferramentas conferidas e um instalador só. O rito do projeto pede o plano aprovado antes de qualquer código, e este trabalho mexe em arquivos que o lançador das corridas importa, então a ordem e as salvaguardas precisam estar escritas antes. Nenhum código foi escrito e nada foi instalado. -->

**Aprovado pelo Eric em 18/11/2026, como está (decisão 143).** As fichas 78 a 83 de [pendencias.md](../Documentacao/memorial/pendencias.md) foram respondidas no mesmo dia, no quadro da sessão: 78 (a), macOS pelo GitHub Actions (decisão 138); 79 (a), versão conferida e faixa aceita, com o modo `--reproduzir` (decisão 139); 80 (a), um núcleo, dois lançadores e o Python pelo `uv` (decisão 140); 81 (a), a matriz recomendada, com os testes leves de dia e os pesados depois da corrida 28 (decisão 141); 82, por uma opção que surgiu no quadro, o Windows 10 no PC de um integrante e o Windows Server 2022 de avaliação (decisão 142); 83 (a), este plano (decisão 143). Sobre a corrida 28 ele respondeu "Roda hoje à noite".

> Estado em 18/11/2026: aprovado; pacote I0 feito; execução por começar pelo pacote I1 (seção 5), que não usa a máquina. Livro-razão em `.superpowers/sdd/instalador/progress.md` (fora do git).

# Plano do instalador único e do teste em máquina limpa

Data: 18/11/2026. Máquina: a máquina-alvo das corridas (i5-1235U, 15,7 GB de memória, Windows 11 Pro 10.0.26200). Repositório: `C:\Users\Eric.Derre\Documents\TCC` (`main`, último commit `717f68c2`, com alterações no working tree que o Eric commita).

Notação: `RAIZ` = repositório; `DADOS` = `RAIZ\Documentacao\memorial\5-metodo-e-ferramental\dados\instalador`; `EXP` = `RAIZ\Programacao\AgenteCore\experimentos`; `SDD` = `RAIZ\.superpowers\sdd\instalador` (pasta nova, fora do git, com o livro-razão).

## 1. Contexto

### 1.1 O que foi pedido

Nas palavras do Eric, em 18/11/2026: testar os instaladores "hit and run" para Windows, Linux e macOS; no Windows, com e sem o Windows Defender ativo, em máquina virtual recém-criada de Windows 10 e de Windows 11, "evitando erros por conta de .net ou coisas do gênero"; nos três sistemas, conferir a versão das ferramentas e avaliar se o projeto fixa uma versão do Ollama ou usa sempre a mais recente; no Linux, usar o Linux de dentro do Windows e, se for o caso, máquina virtual com as distribuições mais usadas; no macOS, ver como simular dentro do Windows e preparar o instalador para as dependências do Mac; e "o instalador deve ser 1 só, reconhecendo o SO que ele está e fazendo os ajustes necessários".

### 1.2 O que existe hoje

| Arquivo | O que faz | De onde baixa |
|---|---|---|
| `install.cmd` | Atalho clicável: chama o `install.ps1` com `-ExecutionPolicy Bypass` | nada |
| `install.ps1` | Procura `python`, `python3` ou `py`; se não acha, `winget install Python.Python.3.14`; chama o `install.py` | `winget` |
| `install.sh` | Procura `python3` ou `python`; se não acha, `brew install python3` ou `apt-get install python3 python3-venv python3-pip`; chama o `install.py` | Homebrew ou `apt` |
| `install.py` | O núcleo: reconhece o sistema (`platform.system()`) e instala PHP, MariaDB, o banco `ti93phpdb01` (três `.sql`), a venv da CobaiaAPI, a venv do AgenteCore, o Chromium do Playwright, o Ollama e o modelo `qwen2.5:7b` | Windows: `winget` (`PHP.PHP.8.2`, `MariaDB.Server`, `Ollama.Ollama`) ou o zip oficial do MariaDB 11.8 com SHA-256 conferido, quando não há administrador. Linux: `apt-get` (`php`, `php-mysql`, `mariadb-server`); o Ollama não é instalado, só o comando é impresso. macOS: `brew` (`php`, `mariadb`, `--cask ollama`). Nos três: PyPI, o Chromium do Playwright e o registro de modelos do Ollama |
| `_env_common.py` | Funções comuns: achar PHP, MariaDB e Ollama, subir e desligar o MariaDB, as opções do PHP | nada |
| `run.py` | Sobe o MariaDB, o `php -S` na porta 8080 e o `uvicorn` na 8000 | nada |
| `Cobaia.py` e `Cobaia.exe` | Instala, sobe e abre o navegador; o `.exe` é gerado pelo PyInstaller (`build_exe.ps1`), sem assinatura | o mesmo do `install.py` |
| `testar_instalador.py` | 7 testes das partes sem rede (zip do MariaDB, SHA-256, extração, comando da API) | nada |

Versões: só o Playwright (`playwright==1.64.1` em `Programacao/AgenteCore/requirements.txt`) e a série do MariaDB no Windows (`MARIADB_SERIE = "11.8"`) são escolhidas pelo projeto. As dependências da CobaiaAPI têm piso (`>=`). O resto vem como o sistema entregar.

### 1.3 O que a leitura do código sugere que quebra em máquina limpa

Nenhuma destas foi testada. Cada uma é uma hipótese, e só vira conserto depois de a célula limpa mostrar a falha, com o erro literal gravado.

| Id | Sistema | Hipótese |
|---|---|---|
| HW1 | Windows | O `install.ps1` aceita como Python o atalho da Microsoft Store (`WindowsApps\python.exe`, que existe no Windows novo e não roda nada), e o instalador para antes de começar |
| HW2 | Windows | Sem o `winget` (Windows Sandbox; Windows novo antes de a Store se atualizar), o `install.ps1` e o `install.py` param com erro de comando não encontrado |
| HW3 | Windows | Depois de o `winget` instalar o Python, a mesma janela não o enxerga, e o instalador manda fechar e abrir o terminal |
| HW4 | Windows | O PHP 8.2 não abre sem o Visual C++ Redistributable (`vcruntime140.dll`); o pacote do `winget` declara essa dependência |
| HW5 | Windows | Com administrador, o `winget install MariaDB.Server` traz hoje a série 12 ou 13, e não a 11.8 que o projeto usa |
| HW6 | Windows | O Defender ou o SmartScreen barra ou atrasa o `Cobaia.exe` (sem assinatura, PyInstaller de um arquivo só) |
| HL1 | Linux | `./install.sh` dá "Permission denied": o arquivo está no git com o modo 100644, sem permissão de execução |
| HL2 | Linux | Com o `python3` presente e sem o `python3-venv`, a criação da venv falha |
| HL3 | Linux | Em distribuição sem `apt-get` (Fedora, Arch, openSUSE) o instalador para sem dizer o que fazer |
| HL4 | Linux e macOS | `_env_common.php_extension_flags` manda o PHP procurar as extensões na pasta ao lado do executável (`/usr/bin/ext`), que só existe no Windows; o `mysqli` não carrega e o site fica sem banco |
| HL5 | Linux | O Ollama não é instalado (o instalador só imprime o comando) e a instalação termina dizendo "Instalação concluída" |
| HL6 | Linux | O `playwright install chromium` não instala as bibliotecas do sistema, e o Chromium não abre |
| HL7 | Linux | Sem o systemd (o gerente de serviços, que no WSL pode vir desligado), `systemctl enable --now mariadb` falha e o plano B, subir o `mariadbd` direto como usuário comum, não sobe |
| HL8 | Linux | Com o Python 3.10 ou 3.11 da distribuição o instalador roda (ele pede 3.10), mas cinco arquivos dos experimentos parecem pedir o 3.12 (sonda por expressão regular, não conclusiva) |
| HL9 | Linux | Clonado no Windows e usado pelo WSL em `/mnt/c`, o `install.sh` vem com fim de linha do Windows (CRLF) e o shell recusa a primeira linha |
| HL10 | Linux | O root do MariaDB entra por `unix_socket`; o conserto que o instalador tenta (`ALTER USER` pelo `sudo`) nunca rodou |
| HM1 | macOS | Sem o Homebrew, o instalador para com um aviso (é o comportamento escrito hoje) |
| HM2 | macOS | O `brew install php` traz o PHP 8.5; o site legado foi validado no 8.2 |
| HM3 | macOS | O cask `ollama` mudou de nome para `ollama-app` no Homebrew |
| HM4 | macOS | O `brew services start mariadb` sobe, mas o root sem senha não foi conferido (o conserto só existe para Linux) |

### 1.4 O que já está decidido

| Tema | Decisão | Onde |
|---|---|---|
| macOS | Testado pelos executores de macOS do GitHub Actions (`macos-15` com modelo pequeno; `macos-15-intel` com o `qwen2.5:7b`); o commit e o push são do Eric; máquina virtual de macOS em PC fica fora pela licença da Apple | ficha 78, decisão 138 |
| Versões | `versoes.json` com a versão testada e a faixa aceita de cada ferramenta; modo `--reproduzir` com versão exata; conferência semanal com as versões mais novas | ficha 79, decisão 139 |
| Forma | Um núcleo (`install.py`), dois lançadores (`install.cmd`, `install.sh`); o Python vem pelo `uv` quando falta; o `Cobaia.exe` usa o mesmo passo | ficha 80, decisão 140 |
| Matriz | Windows 11 no Sandbox e em máquina virtual do Hyper-V (Defender ligado e desligado); Linux pelo WSL (Ubuntu 22.04, 24.04, 26.04; Debian 12, 13; Fedora 45 como melhor esforço; Arch e openSUSE com aviso); uma máquina virtual de Ubuntu 24.04; níveis N1 a N4 | ficha 81, decisão 141 |
| Windows 10 | Teste em máquina usada de um integrante e máquina virtual do Windows Server 2022 de avaliação; nenhum Windows 10 sem ativação | ficha 82, decisão 142 |
| Agenda | Testes leves de dia, com o ok do Eric a cada vez e sem corrida rodando; reinício e máquinas virtuais de Windows só depois de a corrida 28 terminar e ser lida | decisão 141 |
| Administrador | O Windows só pede confirmação: o Eric liga o Sandbox e o Hyper-V nesta máquina | decisão 141 |
| Onde os testes rodam | Pela janela do PowerShell do Eric, nunca de dentro do aplicativo Claude (pacote MSIX, camada privada de `AppData\Local`) | ficha 55, decisão 107 |
| Commit | Nada de commit nem de `git add` pela IA | `.claude/CLAUDE.md` |

### 1.5 A máquina

De `DADOS\medidas-da-maquina-2026-11-18.txt`: 15,7 GB de memória, 4,2 GB livres com o aplicativo aberto; 218,8 GB livres no disco; WSL 2.5.10.0 ativo, sem distribuição; `Containers-DisposableClientVM` (Windows Sandbox) e `Microsoft-Hyper-V-All` desativados; Defender com a proteção em tempo real ligada. Uma instalação completa ocupa cerca de 10 GB: Ollama 3.200 MB, pesos do `qwen2.5:7b` 4.466 MB, navegador do Playwright 718 MB, MariaDB 295 MB, venvs 95 MB e 242 MB.

## 2. Princípios que valem para o plano todo

1. **Falha antes do conserto.** Cada célula roda primeiro o instalador como está, e o erro literal fica gravado. Só então o conserto é escrito, com o teste unitário antes do código, e a célula roda de novo. Hipótese que o teste derrubar sai da lista sem conserto.
2. **Os três arquivos que as corridas importam não mudam antes da corrida 28.** `_env_common.py`, `install.py` e `run.py` são importados por `executar_fase4.py`, `linha_de_base_manual.py` e `restaurar_banco.py`. Até o Eric dizer que a corrida 28 terminou e foi lida, o código novo nasce em arquivos novos (pasta `instalador/`), que importam esses três sem alterá-los. Depois, os consertos são levados para dentro deles, com testes que fixam antes o comportamento atual no Windows da máquina-alvo.
3. **Nada pesado durante corrida.** Antes de cada célula, a pergunta ao Eric. Nenhuma bateria com banco durante uma corrida.
4. **Mudança de sistema é do Eric.** Ligar o Windows Sandbox e o Hyper-V, criar máquina virtual, desligar e religar o Defender (só dentro de máquina virtual, nunca na máquina real): a sessão entrega o roteiro e o comando.
5. **Download com o sim dele.** Todo download que não seja o do próprio instalador dentro da célula (imagem de sistema, imagem de distribuição) é pedido antes, com nome, origem e tamanho; quando o site não informa o tamanho, o roteiro lê o tamanho no cabeçalho do servidor antes de baixar.
6. **Arquivo baixado é conferido.** Tudo o que o instalador baixa por conta própria (o `uv`, o zip do PHP, o zip do MariaDB, o instalador do Ollama) tem o SHA-256 conferido contra o valor publicado, como o MariaDB portátil já faz.
7. **Evidência em arquivo, relatório por script.** Cada célula grava `registro.json` e `instalacao.log`; o relatório do Memorial sai de um script com `--check`. Nenhum número digitado.
8. **Nada na pasta do usuário que não precise.** O `uv`, o Python que ele traz e o PHP do Windows ficam em `RAIZ\.ferramentas\` (fora do git), não em `AppData`; o perfil do shell e o PATH do usuário não são alterados.

## 3. O desenho

### 3.1 As peças

| Peça | Novo ou alterado | O que faz |
|---|---|---|
| `versoes.json` | novo | Para cada ferramenta: versão testada, faixa aceita, de onde baixar e o SHA-256 quando o download é direto (seção 3.2) |
| `instalador/versoes.py` | novo | Lê o `versoes.json`, compara a versão encontrada com a testada e com a faixa, e devolve "igual", "na faixa" ou "fora da faixa" |
| `instalador/sistema.py` | novo | Diz a família do sistema: Windows; macOS com Homebrew; Linux de `apt` (Debian, Ubuntu, Mint), de `dnf` (Fedora) ou não suportado, lendo `/etc/os-release`; traz a tabela de nomes de pacote de cada família |
| `instalador/uv_fixado.txt` | novo, gerado | A versão do `uv` e o SHA-256 por sistema, em linhas `CHAVE=valor`, que o PowerShell e o shell conseguem ler sem Python; gerado do `versoes.json` por script com `--check` |
| `install.ps1` e `install.sh` | alterados | Procuram um Python 3.12 ou mais novo que funcione de verdade (rodam um comando de teste, que o atalho da Store não passa); se não acham, baixam o `uv` fixado para `RAIZ\.ferramentas\uv`, conferem o SHA-256, instalam o Python 3.14 em `RAIZ\.ferramentas\python` e chamam o núcleo com ele |
| `install.cmd`, `run.cmd`, `run.ps1`, `run.sh` | conferidos | Mudam só se o teste mostrar falha |
| `instalador/ferramentas.py` | novo | Instala o que falta, por família: PHP (Windows: zip oficial 8.2 com SHA-256 em `RAIZ\.ferramentas\php`; Linux: pacote da distribuição; macOS: `brew`), MariaDB (Windows: sempre o zip 11.8, o caminho que já existe; Linux e macOS: pacote e serviço), Ollama na versão testada (Windows: o instalador oficial da versão, em escopo de usuário; Linux e macOS: o script oficial com `OLLAMA_VERSION`), o navegador do Playwright (com `--with-deps` nas distribuições de `apt`) |
| `instalador/conferir.py` | novo | A prova da instalação, em quatro níveis (seção 3.3), e o `registro.json` |
| `install.py` | alterado só no pacote I3 | Passa a usar as peças acima e ganha `--conferir` e `--reproduzir`; até o I3, quem as chama é um ponto de entrada provisório, `instalador/nucleo.py`, que importa o `install.py` sem alterá-lo |
| `_env_common.py` e `run.py` | alterados só no pacote I3 | Os consertos que os testes confirmarem (por exemplo, as opções do PHP só no Windows) |
| `Cobaia.py` e `build_exe.ps1` | conferidos no I3 | O `.exe` é recompilado pelo Eric, na janela dele, depois do I3 |
| `.gitattributes` | novo | `*.sh` sempre com fim de linha do Linux; `*.cmd` e `*.ps1` com o do Windows |
| `testar_instalador.py` | ampliado | Os testes novos entram aqui, no mesmo formato sem pytest |
| `ferramentas/instalador_matriz/` | novo | Os roteiros das células (seção 4.3) e o leitor que gera o relatório |
| `.github/workflows/instalador.yml` | novo | As células do GitHub Actions (seção 4.2) |

O instalador continua idempotente: rodar de novo não duplica nada.

### 3.2 O `versoes.json`

Um registro por ferramenta, com estes campos: `testada` (a versão que o projeto conferiu), `aceita_de` e `aceita_ate` (a faixa; vazio quer dizer sem limite), `afeta_medida` (verdadeiro para o Ollama, o Playwright e o modelo: são as que o `--reproduzir` exige exatas), `origem` (de onde o valor de `testada` foi copiado) e, quando o download é direto, `url` e `sha256` por sistema.

De onde cada valor vem, sempre por script: a versão do Ollama, do registro da última corrida medida (`EXP\resultados_alvo`, só leitura); o Playwright, de `requirements.txt`; a série do MariaDB, de `install.MARIADB_SERIE`; o identificador e o tamanho do `qwen2.5:7b`, do registro de modelos do Ollama (`845dbda0ea48`; pesos com 4.683.073.952 bytes, em `DADOS\pesquisa-versoes-linux.md`); o Python, de `python --version` da venv do AgenteCore; o PHP, do executável em uso na máquina-alvo. As faixas aceitas saem do que a matriz mostrar funcionando: PHP de 8.1 a 8.5 e MariaDB de 10.6 a 13.0 são a faixa a testar, não uma promessa.

Regra do instalador, em modo normal: a ferramenta falta e dá para escolher a versão, instala a testada; ela existe dentro da faixa, usa e avisa a diferença; fora da faixa, para e explica como resolver. Em `--reproduzir`: qualquer diferença nas ferramentas com `afeta_medida` para o instalador, com o comando que instala a versão exata. O instalador nunca troca sozinho um Ollama que já está na máquina.

### 3.3 O que conta como instalação provada

`python install.py --conferir` (e o lançador, com o mesmo argumento) roda quatro níveis e grava o `registro.json`:

| Nível | O que prova | Como |
|---|---|---|
| N1 | O site e a API no ar | PHP acha o `mysqli`; MariaDB responde; as contagens do seed batem (`restaurar_banco.CONTAGENS_DO_SEED`: 4 tipos, 14 produtos, 2 usuários, 0 reservas); o CobaiaFront responde na 8080 com produto do seed na página; a CobaiaAPI responde na 8000 |
| N2 | O navegador do agente | A venv do AgenteCore importa o Playwright na versão fixada; o Chromium abre sem janela e carrega a página do CobaiaFront |
| N3 | O Ollama | O Ollama responde em `/api/version`; um modelo pequeno (trocado por `COBAIA_MODELO_LLM`) baixa e devolve texto, só em CPU |
| N4 | O modelo do projeto | O `qwen2.5:7b` baixa, o identificador confere com o do `versoes.json` e ele devolve texto. Só onde a memória der; onde não der, o registro diz "não coube", e isso não conta como falha do instalador |

O registro traz ainda: sistema, versão e arquitetura; memória; se há administrador; no Windows, o estado do Defender lido por `Get-MpComputerStatus`; a versão encontrada de cada ferramenta contra o `versoes.json`; o tempo de cada passo; e o erro literal de cada falha.

### 3.4 O caminho do lançador

Windows (`install.cmd` chama o `install.ps1`): (1) procura um Python 3.12 ou mais novo e roda nele um comando de teste; (2) se não há, baixa o `uv` fixado do GitHub pelo `Invoke-WebRequest`, confere o SHA-256 e instala o Python 3.14 em `RAIZ\.ferramentas`; (3) chama o `install.py`. Não usa o `winget` em nenhum passo.

Linux e macOS (`bash install.sh`, ou `./install.sh` depois do conserto da permissão; o arquivo é escrito para o `bash`, que vem nas distribuições da matriz e no macOS): os mesmos três passos, com `curl` ou `wget`; se não houver nenhum dos dois, o lançador diz qual pacote instalar. Os pacotes do sistema (PHP, MariaDB, bibliotecas do navegador) continuam vindo do gerenciador da distribuição, com `sudo`, e no macOS do Homebrew, que continua sendo pré-requisito declarado.

No Linux, o instalador avisa antes de mudar a entrada do root do MariaDB para senha vazia (é o que o `connect.php` do site legado exige) e só segue com a confirmação: numa máquina com um MariaDB em uso real isso não deve ser feito.

## 4. A matriz de testes

### 4.1 Células nesta máquina

| Id | Sistema | Como nasce limpa | Níveis | Quando |
|---|---|---|---|---|
| ALVO | Esta máquina, como está | Não é limpa: é a instalação que funciona hoje, e serve para provar que o `--conferir` acerta numa máquina boa | N1 a N4 | Depois da corrida 28 |
| L-U2404 | Ubuntu 24.04 no WSL | `wsl --import` da imagem oficial; `wsl --unregister` no fim | N1 a N4 | De dia, com ok |
| L-U2204, L-U2604, L-D12, L-D13 | Ubuntu 22.04 e 26.04, Debian 12 e 13 no WSL | idem | N1 a N3 | De dia, com ok |
| L-F45 | Fedora 45 no WSL | idem | N1 garantido; N2 e N3 como melhor esforço | De dia, com ok |
| L-ARCH, L-SUSE | Arch e openSUSE no WSL | idem | Só a mensagem de "não suportado", com a lista do que instalar à mão | De dia, com ok |
| W11-SB | Windows 11 no Windows Sandbox | Descartável a cada abertura; a pasta do pacote entra só para leitura | N1 a N3 | Depois da corrida 28 |
| W11-VM-D1 e W11-VM-D0 | Windows 11 Enterprise de avaliação no Hyper-V, com o Defender ligado e desligado | Ponto de restauração logo depois da instalação do Windows | N1 a N4 | Depois da corrida 28 |
| WS22-VM | Windows Server 2022 de avaliação no Hyper-V, com o Defender como vier e desligado | idem | N1 a N3 | Depois da corrida 28 |
| L-U2404-VM | Ubuntu 24.04 de mesa no Hyper-V | Instalação nova | N1 a N3, e o navegador com janela | Depois da corrida 28 |

Uma célula por vez. A memória do WSL fica limitada no `.wslconfig` durante os testes, e as máquinas virtuais recebem de 6 a 8 GB com o aplicativo Claude e o VS Code fechados. No disco, o pico é a máquina virtual de Windows 11 (até 64 GB, crescendo conforme o uso) mais uma instância de WSL (cerca de 10 GB com tudo instalado).

### 4.2 Células fora desta máquina

| Id | Sistema | Como | Níveis |
|---|---|---|---|
| M-15 | macOS 15, Apple Silicon, 7 GB | GitHub Actions, `macos-15` | N1 a N3 |
| M-15I | macOS 15, Intel, 14 GB | GitHub Actions, `macos-15-intel` | N1 a N4 |
| CI-WIN e CI-UBU | Windows Server e Ubuntu do GitHub | GitHub Actions; não são limpos (já trazem PHP, Python e banco), servem de conferência a cada push e uma vez por semana com as versões mais novas | N1 a N3 |
| W10-USADO | Windows 10 de um integrante | O integrante segue `roteiro-integrante.md` e devolve a pasta de evidência | N1 a N3 |

### 4.3 Como uma célula roda

O pacote que entra na célula é o que quem baixa do GitHub recebe: `ferramentas/instalador_matriz/empacotar.py` monta um zip com os arquivos rastreados e os novos do instalador, sem o `.git`, com o fim de linha que o GitHub entrega. Dentro da célula, o roteiro copia o pacote para uma pasta do usuário, roda o lançador como uma pessoa rodaria, roda o `--conferir` e copia `registro.json` e `instalacao.log` para `DADOS\celulas\<id>\<data e hora>\`. Os roteiros: `celula_wsl.ps1` (cria, roda e apaga a instância), `celula_sandbox.ps1` (gera o arquivo `.wsb`), `roteiro-hyperv.md` (o passo a passo das máquinas virtuais, feito pelo Eric) e `roteiro-integrante.md`.

Downloads que pedem o sim do Eric antes: as imagens `.wsl` oficiais de cada distribuição (endereços em `DADOS\pesquisa-versoes-linux.md`, seção 7; tamanho lido do servidor na hora); a imagem de avaliação do Windows 11 Enterprise e a do Windows Server 2022 (Centro de Avaliação da Microsoft, com registro dele); a imagem do Ubuntu 24.04 de mesa.

### 4.4 O que a matriz não prova

O WSL não prova o serviço que sobe no boot, o navegador com janela numa área de trabalho real nem o kernel da distribuição; a máquina virtual de Ubuntu cobre isso para uma distribuição só. O executor do GitHub já vem com o Homebrew e o Python: o Mac sem o Homebrew e o uso pela janela ficam sem prova. O Windows 10 de mesa limpo não é testado: o Windows Server 2022 é o sistema limpo mais próximo, e o PC do integrante é uma máquina usada. Windows e Linux em processador ARM ficam de fora. Nenhuma célula mede tempo de diagnóstico: isso é das corridas.

## 5. Pacotes, em ordem

### I0. Aprovação e registro (esta sessão; sem máquina)
Fichas 78 a 83, decisões 138 a 143, este plano congelado em `claude-memoria/plano-aprovado-instalador-unico.md`, a linha no roadmap, o painel regerado e republicado.

### I1. As peças sem rede (sem máquina; não toca nos três arquivos)
Testes antes do código, em `testar_instalador.py`: `instalador/versoes.py`, `instalador/sistema.py`, a montagem do `registro.json`, o gerador do `uv_fixado.txt` com `--check`, o empacotador. Depois o `versoes.json`, o `instalador/conferir.py` e os roteiros das células. `.gitattributes`. Pronto quando a bateria passa e o pacote sai igual em duas rodadas.

### I2. Linux pelo WSL (de dia, com o ok do Eric a cada célula)
Primeiro a rodada do instalador como está em L-U2404, para gravar as falhas; depois os consertos de Linux em `instalador/` e nos lançadores, e a célula de novo até N4. Em seguida as outras quatro de `apt`, o Fedora e as duas de aviso. Pronto quando cada célula tem o registro final e as hipóteses HL1 a HL10 estão marcadas como confirmada e consertada, ou derrubada.

### I3. A entrada nos três arquivos (só depois de o Eric dizer que a corrida 28 terminou e foi lida)
Testes que fixam o comportamento atual no Windows; os consertos entram em `_env_common.py`, `install.py` e `run.py`; o ponto de entrada provisório some; `testar_instalador.py`, `testar_fase4.py` e as baterias que importam esses arquivos passam; o Eric recompila o `Cobaia.exe` e roda a célula ALVO na janela dele.

### I4. Windows limpo (depois do I3; um reinício)
O Eric liga o Windows Sandbox e o Hyper-V de uma vez, com um reinício só. W11-SB primeiro, como está e depois consertado; depois W11-VM-D1, W11-VM-D0 e WS22-VM; por fim L-U2404-VM. Pronto quando HW1 a HW6 estão marcadas e as células têm o registro final.

### I5. GitHub Actions (depende de commit e push do Eric)
O `instalador.yml` com M-15, M-15I, CI-WIN e CI-UBU; o resultado de cada tarefa vai para o resumo da execução e para um arquivo anexo; a sessão lê e conserta. Pronto quando as quatro tarefas passam ou a falha está explicada no relatório, com HM1 a HM4 marcadas.

### I6. Windows 10 de um integrante
O roteiro vai para o integrante que o Eric indicar; a pasta de evidência volta e entra em `DADOS\celulas\W10-USADO\`.

### I7. Relatório e documentação (sem máquina)
`Documentacao/memorial/5-metodo-e-ferramental/relatorio-instalador-maquina-limpa.md`, gerado das evidências: o que passou, o que falhou e o que não pôde ser testado e por quê. `README.md` (seção "Instalar e rodar") e `DETALHES-TECNICOS.md` (seção "Instalação em detalhe" e "Troubleshooting") atualizados; uma aba no painel; `python ferramentas/gerar_dashboard.py`, as cinco baterias do painel e `ferramentas/conferir_docs.py`; painel republicado no mesmo endereço; nota de memória. Tudo no working tree para o Eric commitar.

## 6. Calendário

| Quando | O quê |
|---|---|
| 18/11 | I0 |
| A partir de 19/11, de dia | I1; I2 célula a célula, com o ok do Eric |
| Depois de a corrida 28 ser lida | I3 e I4 |
| Quando o Eric puder commitar e dar push | I5 |
| Quando o integrante puder | I6 |
| Até 02/12/2026 | I7 |

A Fase 5 tem a prioridade: qualquer conflito de máquina ou de agenda se resolve a favor dela.

## 7. Riscos e salvaguardas

| Risco | Salvaguarda |
|---|---|
| Um conserto mudar o ambiente das cobaias na véspera da corrida 28 | Princípio 2: os três arquivos só mudam no I3 |
| Um teste pesado tirar memória de uma corrida | Princípio 3 e a pergunta antes de cada célula |
| Instalar na camada privada do aplicativo Claude | Tudo roda pela janela do Eric; as ferramentas novas ficam em `RAIZ\.ferramentas`, que não passa pela camada privada |
| O `uv` ou outro download vir trocado | SHA-256 fixado no `versoes.json` e conferido antes de executar |
| O Sandbox ou o Hyper-V não conviver bem com o WSL 2 | Os três usam o mesmo hipervisor do Windows; se o Sandbox travar a máquina (há relato não oficial no 24H2), a célula W11-SB sai e a máquina virtual cobre o Windows 11 |
| A imagem de avaliação demorar a baixar ou expirar | Windows 11: 90 dias; Windows Server 2022: 180 dias; os testes cabem em dias |
| A versão do Ollama mudar durante o trabalho | O `versoes.json` guarda a testada; as corridas continuam com a regra da ponte (decisões 44 e 47); este trabalho não chama o Ollama da máquina real |
| Outra sessão editar o Memorial ao mesmo tempo | Numeração conferida logo antes de escrever; as páginas dos integrantes não são republicadas |
| O site legado não rodar no PHP 8.5 do Homebrew ou do Ubuntu 26.04 | A célula mostra; a saída é fixar `php@8.2` onde existir ou declarar a faixa, nunca reescrever o site |

## 8. Fora do escopo

Suporte completo a Fedora, Arch e openSUSE (o `dnf`, o `pacman` e o `zypper` com as bibliotecas do navegador); assinatura digital do `Cobaia.exe`; executável único para Linux e macOS; instalação sem internet; mudança no agente, nas corridas ou no harness de experimentos; máquina virtual de macOS; Windows 10 sem ativação.

## 9. Verificação fim a fim

O trabalho está pronto quando: (1) cada hipótese da seção 1.3 está marcada como confirmada e consertada, derrubada ou não testada, com o motivo; (2) cada célula da seção 4 tem o registro final em `DADOS\celulas\` ou a explicação de por que não rodou; (3) `testar_instalador.py` e as baterias que importam os três arquivos passam; (4) o relatório do Memorial sai do script com `--check` idêntico; (5) o README e o `DETALHES-TECNICOS.md` dizem o que o relatório diz; (6) o painel foi regerado, conferido e republicado no mesmo endereço; (7) nada foi commitado pela IA.

## 10. Decisões do Eric

| Ficha | Pergunta | Resposta |
|---|---|---|
| 78 | Como testar em macOS | (a) GitHub Actions (decisão 138) |
| 79 | Fixar versão ou a mais recente | (a) versão conferida e faixa, com `--reproduzir` (decisão 139) |
| 80 | A forma do instalador único | (a) um núcleo, dois lançadores, Python pelo `uv` (decisão 140) |
| 81 | A matriz de Windows 11 e de Linux | (a) recomendada (decisão 141) |
| 82 | O Windows 10 | máquina usada de um integrante e Windows Server 2022 de avaliação (decisão 142) |
| 83 | Este plano | (a) aprovado como está (decisão 143) |

## 11. Rastreabilidade

Pesquisas e medidas: `DADOS\pesquisa-macos.md`, `pesquisa-windows.md`, `pesquisa-versoes-linux.md`, `verificacao-licenca-windows-10.md`, `medidas-da-maquina-2026-11-18.txt`. Fichas 78 a 83 em `Documentacao/memorial/pendencias.md`; decisões 138 a 143 em `Documentacao/memorial/1-decisoes-e-historico/decisoes.md`. Livro-razão em `SDD\progress.md`.

## Anexo: desvios do plano aprovado

<!-- ! Alteração de IA - Revisar: anexo novo (18/11/2026) com os desvios do pacote I1 em relação ao texto aprovado; o texto das seções 1 a 11 não foi alterado.
     ! Motivo: o plano foi congelado na aprovação (decisão 143), e o que muda depois tem de ficar registrado à parte, para quem lê saber o que foi feito diferente do que o Eric aprovou e por quê. A revisão do pacote I1 apontou que os adiamentos e as mudanças fora da lista de arquivos estavam só no livro-razão, que fica fora do git. -->

| # | Data | O que mudou em relação ao texto aprovado | Motivo |
|---|---|---|---|
| 1 | 18/11/2026 | O pacote I1 não criou o `.gitattributes`, que a seção 5 lista nele; fica para o I2 | O arquivo é o conserto da suspeita HL9 (fim de linha do `install.sh`), e o princípio 1 pede a falha gravada antes do conserto; criá-lo antes da primeira célula esconderia o que se quer ver |
| 2 | 18/11/2026 | Os roteiros do Windows Sandbox, do Hyper-V e do integrante e o leitor que gera o relatório (seções 4.3 e 5, I1) ficam para os pacotes que os usam: I4, I6 e I7. O I1 entregou só o roteiro da célula de WSL (`ferramentas/instalador_matriz/celula_wsl.ps1`) | O I2 só precisa do roteiro do WSL; os outros dependem do que as primeiras células mostrarem e de a corrida 28 terminar |
| 3 | 18/11/2026 | O `.gitignore` ganhou a linha `.ferramentas/`, arquivo que a seção 3.1 não lista | O princípio 8 põe a pasta fora do git, e o empacotador já grava nela dois pacotes (63 MB e 56 MB) que um `git add -A` levaria para o commit |
| 4 | 18/11/2026 | Suspeita nova, HL11 (Linux), a somar às da seção 1.3: o `install.py` instala só `php` e `php-mysql`, e o site usa `mb_strimwidth`, que no Debian e no Ubuntu vem no pacote `php-mbstring`; sem ele, as páginas de produto dariam erro fatal | Achada ao escrever a tabela de pacotes de `instalador/sistema.py`. Sem teste, como as outras |
| 5 | 18/11/2026 | Uma distribuição de `apt` que não está na lista da decisão 141 (Linux Mint, outra versão do Ubuntu ou do Debian) é tratada como melhor esforço, e não como sem suporte | A decisão 141 só nomeia as suportadas; o instalador sabe usar o `apt` nelas, e recusar seria pior para quem tenta |
| 6 | 18/11/2026 | `ferramentas/conferir_docs.py`, fora da seção 3.1, passou a não cobrar a tag de um `__init__.py` de 0 byte | O `.claude/CLAUDE.md` já dispensa o arquivo vazio de propósito, e a conferência acusava `instalador\__init__.py` |
| 7 | 18/11/2026 | O tempo de cada passo (seção 3.3) existe, por enquanto, só por nível da prova e no total da célula; os passos do `install.py` ganham hora no I3 | O `install.py` não pode mudar antes de a corrida 28 terminar (princípio 2) |
| 8 | 18/11/2026 | A célula de WSL tira as pastas do Windows do PATH da instância (`appendWindowsPath=false` em `/etc/wsl.conf`) antes de rodar o instalador, o que a seção 4.3 não dizia; o `wsl.conf` original fica guardado na evidência | O WSL acrescenta o PATH do Windows ao da instância, e um Linux recém-instalado não tem isso |
| 9 | 18/11/2026 | A prova (`--conferir`) sai com código 1 também quando uma versão impede: fora da faixa, ou diferente da exata no modo `--reproduzir`; o `registro.json` traz a lista em `impedida_por_versao` | Detalha as seções 3.2 e 3.3, que diziam que o instalador para fora da faixa mas não diziam o que a prova faz |
| 10 | 18/11/2026 | No I1 o `versoes.json` traz endereço e SHA-256 só do `uv`; os do zip do PHP e do instalador do Ollama entram com `instalador/ferramentas.py`, no pacote que escrever o caminho de Windows | Esses dois downloads só passam a existir quando o instalador deixar de usar o `winget`, o que depende de a célula gravar a falha |

<!-- ! Alteração de IA - Revisar: desvios 11 a 16 (18 e 19/11/2026), do pacote I2 (Linux pelo WSL); o texto das seções 1 a 11 e os desvios 1 a 10 não foram alterados.
     ! Motivo: a primeira célula (L-U2404, rodada `20261118-193340`) mostrou que o `install.py` para no primeiro erro, e o roteiro da seção 4.3 só gravaria esse; para marcar as onze suspeitas numa rodada só, a célula passou a fazer mais do que o plano dizia, e a leitura da evidência trouxe duas suspeitas novas. O que mudou em relação ao texto aprovado fica aqui, e não só no livro-razão, que está fora do git. -->

| # | Data | O que mudou em relação ao texto aprovado | Motivo |
|---|---|---|---|
| 11 | 18/11/2026 | A rodada `como-esta` de uma célula de Linux roda, depois do instalador e da prova, as sondas das suspeitas (`ferramentas/instalador_matriz/sondas_suspeitas.sh`): cada uma testa uma suspeita em separado, com o mesmo comando que o instalador ou o `run.py` usaria, e grava o comando e a saída literal em `suspeitas/HLn.txt`; quando precisa passar de uma falha para testar a seguinte, aplica o contorno que uma pessoa aplicaria e o deixa escrito no arquivo. O roteiro ganhou os interruptores `-SemSondas` e `-SemSystemd`, e a evidência ganhou um leitor (`ferramentas/instalador_matriz/ler_celula.py`). A seção 4.3 só previa o instalador e a prova | O `install.py` para no primeiro erro (no Ubuntu 24.04, o root do MariaDB), e cada suspeita escondida atrás dele custaria mais uma rodada na janela do Eric. A HL7 (sem o systemd) não tem como aparecer numa imagem que já vem com o systemd ligado |
| 12 | 18/11/2026 | Duas suspeitas novas de Linux, a somar às da seção 1.3, as duas confirmadas na célula L-U2404. HL12: o instalador para em "Não foi possível subir o MariaDB" com o serviço no ar, porque testa "o banco está no ar" tentando entrar como root sem senha, e por isso nunca chega ao conserto do root (a HL10 dizia que esse conserto nunca tinha rodado; chamado à parte, ele funciona). HL13: `apt-get install php` traz junto o Apache, um servidor web na porta 80 que o projeto não usa | Achadas na leitura da evidência da rodada `20261118-193340` (`instalacao.log`, linhas 63 a 92 e 558 a 565; `suspeitas/HL10.txt`) |
| 13 | 19/11/2026 | As rodadas `como-esta` das outras distribuições usam o pacote guardado da primeira célula (`.ferramentas/pacote-como-esta/cobaia-pacote.tar.gz`, SHA-256 `c3db2ea3e998dda9aa57c1b2c6526dd2ea7a6e4484ca77bd649e5e17cd415a36`), passado ao roteiro por `-Pacote`; a seção 4.3 dizia que o pacote sai sempre do working tree | Depois dos consertos o working tree não tem mais o instalador antigo; o pacote guardado é o instalador como estava em 18/11/2026 |
| 14 | 19/11/2026 | O `install.ps1` não muda no I2; a seção 3.1 lista os dois lançadores juntos | As suspeitas do lançador do Windows (HW1 a HW3) não foram gravadas por nenhuma célula, e o princípio 1 pede a falha antes do conserto. O lançador do Windows fica para o I4, depois da célula W11-SB |
| 15 | 19/11/2026 | No Linux, o script oficial do Ollama é baixado para `.ferramentas/ollama/install.sh` e rodado com `OLLAMA_VERSION`, sem SHA-256 conferido; o princípio 6 pede a conferência de tudo o que o instalador baixa | O site do Ollama não publica o SHA-256 do script, que muda sem aviso. A versão que ele instala é conferida depois contra o `versoes.json`. Baixar o pacote da versão (1,5 GB) para dentro do projeto dispensaria o script, mas deixaria o Ollama sem o serviço do sistema que a prova e o agente esperam encontrar |
| 16 | 19/11/2026 | Uma célula fora da matriz da seção 4.1: L-U2404-SS, o Ubuntu 24.04 com o systemd desligado na instância (`-SemSystemd`), nos modos `como-esta` e `novo` | É a única forma de testar a HL7 nas imagens que vêm com o systemd ligado |

<!-- ! Alteração de IA - Revisar: desvios 17 a 21 (18 e 19/11/2026), ainda do pacote I2; na linha 16, "só no modo `como-esta`" passou a "nos modos `como-esta` e `novo`", porque a célula também rodou depois do conserto.
     ! Motivo: as rodadas `como-esta` das outras distribuições e a revisão dos consertos trouxeram uma decisão do Eric que muda a seção 3.4 (ficha 88), dois comportamentos novos do instalador que o plano não previa (recusar o root, proibir o `apt` de remover pacotes) e duas mudanças vindas de outras sessões (a corrida 28b no lugar da 28 no princípio 2; a evidência das células sem a tag). -->

| # | Data | O que mudou em relação ao texto aprovado | Motivo |
|---|---|---|---|
| 17 | 19/11/2026 | Numa distribuição de `apt`, sem `curl` nem `wget`, o lançador `install.sh` instala `curl` e `ca-certificates` pelo `sudo apt-get` e segue; a seção 3.4 dizia que ele pararia dizendo qual pacote instalar (decisão 148, ficha 88) | A célula L-D13 mostrou que a imagem do Debian 13 do WSL vem sem `python3`, `curl` e `wget`; o lançador antigo instalava o Python sozinho, e o novo pararia num passo manual que antes não existia |
| 18 | 18/11/2026 | Onde o princípio 2 e as seções 4.1, 5 e 6 dizem "corrida 28 terminada e lida", vale "corrida 28b rodada e lida" (decisões 145 e 146). A 28b foi lida em 19/11/2026, e a condição está cumprida; o pacote I2 seguiu sem tocar em `_env_common.py`, `install.py` e `run.py`, que entram no I3 | A corrida 28 de 18/11 não valeu como medida do agente e foi refeita a frio, como corrida 28b |
| 19 | 18/11/2026 | A saída capturada de uma célula (os arquivos da pasta `celulas/<id>/<data-hora>/`) não leva a tag de IA; `ferramentas/conferir_docs.py` e o `.claude/CLAUDE.md`, fora da seção 3.1, ganharam a exceção, e toda pasta de rodada precisa de um `celula.json` com a tag (decisão 147, ficha 87) | A primeira célula gravou 23 arquivos de saída e a conferência dos documentos passou a acusá-los em todas as sessões do projeto; pôr a tag dentro mudaria a evidência |
| 20 | 19/11/2026 | No Linux, o instalador novo recusa rodar como root (com `sudo ./install.sh`, por exemplo) e manda rodar como usuário comum; o plano não tratava do caso | Achado da revisão do pacote: como root a entrada do root do MariaDB passa no teste pelo `unix_socket` e nunca é trocada, a instalação termina "concluída" e o site e a API não funcionam para o usuário comum; as venvs e o navegador ficariam na pasta do root |
| 21 | 19/11/2026 | O `apt-get install` do instalador novo leva `--no-remove`: se o `apt` precisar remover um pacote para instalar outro, ele para com a explicação | Achado da revisão do pacote: numa máquina com o `mysql-server`, instalar o `mariadb-server` removeria o MySQL sem perguntar; o instalador antigo pulava o banco quando achava um cliente instalado |

<!-- ! Alteração de IA - Revisar: desvios 22 e 23 (19/11/2026), do fecho do pacote I2; o texto das seções 1 a 11 e os desvios 1 a 21 não foram alterados.
     ! Motivo: a célula do Fedora 45 gravou uma falha que nenhuma suspeita previa (o script oficial do Ollama para sem o `awk`), e o "pronto quando" do I2 na seção 5 fala em HL1 a HL10, quando o pacote fechou com quatorze suspeitas marcadas; sem as duas linhas o anexo não diria de onde veio o `gawk` na tabela do `dnf` nem quais suspeitas o pacote marcou. -->

| # | Data | O que mudou em relação ao texto aprovado | Motivo |
|---|---|---|---|
| 22 | 19/11/2026 | Suspeita nova de Linux, HL14, a somar às da seção 1.3, confirmada e consertada: no Fedora 45 do WSL o script oficial do Ollama para com `ERROR: The following tools are required but missing: - awk`. O conserto é o `gawk` nos pacotes de base do `dnf` (`instalador/sistema.py`) | Gravada na célula L-F45 em modo `novo`, rodada `20261119-134801` (o instalador saiu com erro depois de o site e a API estarem prontos); provado na rodada `20261119-144952`, em que a instalação termina e o N3 passa |
| 23 | 19/11/2026 | Onde a seção 5 diz que o I2 está pronto com "as hipóteses HL1 a HL10" marcadas, valem HL1 a HL14: a HL11 veio do desvio 4, a HL12 e a HL13 do desvio 12 e a HL14 do desvio 22. Todas ficaram confirmadas e consertadas, menos a segunda metade da HL10, derrubada (o conserto antigo do root do MariaDB funciona quando é chamado) | As quatro suspeitas a mais apareceram depois da aprovação do plano, e o estado de cada uma está em `.superpowers/sdd/instalador/progress.md` e nas pastas de `dados/instalador/celulas/` |

<!-- ! Alteração de IA - Revisar: desvios 24 a 31 (19/11/2026), do pacote I3 (a entrada dos consertos em `_env_common.py`, `install.py` e `run.py`); o texto das seções 1 a 11 e os desvios 1 a 23 não foram alterados.
     ! Motivo: o pacote levou os consertos de Linux para dentro dos arquivos que as corridas importam e apagou o ponto de entrada provisório (`instalador/nucleo.py` e `instalador/servicos.py`), como a seção 5 pede; no caminho, oito coisas saíram diferentes do texto aprovado (um arquivo que não precisou mudar, um que mudou sem estar previsto, o que a prova e a célula ALVO fazem a mais ou a menos) e precisam ficar escritas aqui, porque o livro-razão do pacote (`.superpowers/sdd/instalador/progress-i3.md`) está fora do git. -->

| # | Data | O que mudou em relação ao texto aprovado | Motivo |
|---|---|---|---|
| 24 | 19/11/2026 | O `run.py` não mudou de código no pacote I3; a seção 3.1 o lista entre os alterados nesse pacote | Os dois consertos de que ele precisava entraram nas funções do `_env_common.py` que ele já chama: as opções do `php -S` por sistema em `php_extension_flags` (suspeita HL4) e a subida do banco com e sem o systemd em `ensure_mariadb_running` (HL7 e HL12). Os lançadores `install.sh` e `run.sh` voltaram a chamar `install.py` e `run.py` |
| 25 | 19/11/2026 | No Linux, `_env_common.ensure_mariadb_running` deixou de tentar o servidor iniciado como processo direto quando o serviço não sobe; o plano não tratava do caso | A célula L-U2404-SS gravou que esse plano B não funciona como usuário comum (`Can't create/write to file './ddl_recovery.log' (Errcode: 13 "Permission denied")`), e o conserto provado nas células já não o tentava. No Windows e no macOS a função faz o que fazia |
| 26 | 19/11/2026 | O `Cobaia.py` mudou: ele para quando `install.main()` devolve um código diferente de zero. A seção 3.1 dizia que o arquivo seria só conferido | `install.main()` passou a receber argumentos (`--conferir`, `--ate`, `--reproduzir`) e a devolver o código de saída. No Windows um passo obrigatório que falha continua saindo por `sys.exit(1)`; rodando `python Cobaia.py` no Linux, sem a conferência o launcher subiria o site e a API numa instalação interrompida |
| 27 | 19/11/2026 | O tempo de cada passo da instalação, que o desvio 7 deixou para o I3, entrou assim: o `install.py` grava `.ferramentas/instalacao/passos.json` (resultado e segundos de cada passo), e a prova copia o conteúdo para a chave `instalacao` do `registro.json`. A seção 3.3 não nomeava arquivo nem chave | O instalador e a prova rodam em processos separados, e o arquivo, dentro de `.ferramentas/` (fora do git), leva um ao outro |
| 28 | 19/11/2026 | A célula ALVO tem roteiro próprio, `ferramentas/instalador_matriz/celula_alvo.ps1`, que a seção 4.3 não lista: restaura o banco das cobaias ao seed (`restaurar_banco.py`), roda a prova até o N4 e grava o `celula.json`. Ela não roda o instalador, usa por padrão o modelo pequeno `qwen2.5:0.5b-instruct` e recusa rodar com corrida em andamento, com o site ou a API já no ar, ou de dentro do aplicativo Claude | A seção 4.1 define a ALVO como a prova numa máquina boa; a prova confere as contagens do seed, e a última corrida pode ter deixado reservas no banco; o `qwen2.5:0.5b-instruct` já está no disco da máquina-alvo, então o N3 não baixa nada. O roteiro do WSL não serve, porque cria uma instância de Linux |
| 29 | 19/11/2026 | A prova só roda `ollama pull` quando o Ollama não lista o modelo em `/api/tags`, e falha sem baixar quando não consegue ler a lista; a seção 3.3 diz que o modelo "baixa" | A célula ALVO roda na máquina das corridas, onde o `qwen2.5:7b` das medidas já está baixado; um `pull` incondicional trocaria o modelo medido se a etiqueta mudasse no registro de modelos. Numa célula limpa o modelo nunca está lá, e o `pull` roda como antes |
| 30 | 19/11/2026 | No N1, a prova recusa quando a porta 8080 ou a 8000 já respondem antes de ela subir os serviços, e confere, depois de subir, se os dois processos seguem vivos; a seção 3.3 não dizia | Achado da revisão do pacote: com um `run.cmd` ou um `Cobaia.exe` aberto, o `php -S` e o `uvicorn` novos saíam por porta ocupada e a prova passava olhando o site e a API antigos, sem provar os arquivos que mudaram |
| 31 | 19/11/2026 | No Windows e no macOS, `python install.py --reproduzir` só avisa que a conferência exata das versões acontece na prova (`--conferir --reproduzir`); a seção 3.1 diz que o `install.py` ganha o `--reproduzir` no I3, sem separar os sistemas. No Linux o argumento vale na instalação | O caminho do Windows dentro do `install.py` (sem o `winget`, com o `versoes.json`) é do pacote I4, depois da célula W11-SB gravar as falhas (desvios 10 e 14); até lá os passos do Windows são os de sempre, fixados por 17 testes em `testar_instalador.py` |

<!-- ! Alteração de IA - Revisar: desvio 32 (19/11/2026), das rodadas do pacote I3 na janela do Eric; o texto das seções 1 a 11 e os desvios 1 a 31 não foram alterados.
     ! Motivo: a recompilação do `Cobaia.exe` não gravou o arquivo e o roteiro disse que tinha atualizado; consertar o `build_exe.ps1` não estava no texto aprovado (a seção 3.1 o dava como só conferido no I3), e a mudança precisa ficar escrita aqui, porque o livro-razão do pacote (`.superpowers/sdd/instalador/progress-i3.md`) está fora do git. -->

| # | Data | O que mudou em relação ao texto aprovado | Motivo |
|---|---|---|---|
| 32 | 19/11/2026 | O `build_exe.ps1` mudou; a seção 3.1 dizia que ele seria só conferido no I3. Ele agora só diz "Cobaia.exe atualizado" depois de conferir o código de saída do PyInstaller e a data do arquivo, roda o PyInstaller de dentro da pasta do projeto, guarda a saída do pip e do PyInstaller em `%TEMP%\cobaia-build.log` e aceita `-Saida` para compilar em outra pasta. A recompilação continua sendo do Eric, na janela dele | Na rodada de 19/11/2026 o roteiro durou 4 segundos na janela do Eric (registro de eventos do Windows PowerShell, 18:47:38 a 18:47:42): o pip respondeu, o PyInstaller não gravou o `Cobaia.spec` nem o `Cobaia.exe` (que ficou com a data de 07/11/2026) e a mensagem final saiu assim mesmo. A causa mais provável, reproduzida mas não vista na janela dele: chamado de uma janela aberta em `C:\Windows\System32`, o PyInstaller para em "Do not run pyinstaller from C:\Windows\System32" antes de gravar qualquer arquivo. O roteiro novo rodou duas vezes de dentro do aplicativo, compilando numa pasta de rascunho: numa pasta sem o `Cobaia.py` ele diz "FALHOU" e devolve 1; chamado de dentro de `C:\Windows\System32` ele compila. Rodado de novo pelo Eric às 19:38:29, na janela dele, o roteiro gravou o `Cobaia.exe` (9.258.900 bytes) |
