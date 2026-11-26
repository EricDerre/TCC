<!-- ! Alteração de IA - Revisar: arquivo novo (25/11/2026, pacote I7 do instalador único, decisão 153): relatório do que foi provado em cada sistema pelo instalador, com quatro blocos gerados por `ferramentas/instalador_matriz/relatorio.py --colar` (resumo, matriz, rodadas e não testadas) e o resto escrito à mão (o que foi pedido, como ler, as suspeitas de Linux e o que nenhuma célula prova).
     ! Motivo: o README dizia "Windows 10/11, Linux ou macOS" sem dizer em qual deles o instalador tinha rodado de verdade. Os níveis, as rodadas e a lista do que não foi testado vêm dos arquivos de evidência por script, para o texto não ficar para trás quando o GitHub Actions entregar as primeiras rodadas; nenhum número de resultado foi digitado fora dos blocos. -->

# Relatório do instalador em máquina limpa

Este relatório diz, sistema por sistema, o que o instalador do projeto (o `install.cmd` no Windows, o `install.sh` no Linux e no macOS, e o `install.py` por trás dos dois) provou fazer numa máquina recém-criada, o que falhou e o que nunca foi testado. As tabelas das seções 3, 4, 6 e 7 são escritas por `ferramentas/instalador_matriz/relatorio.py` a partir das pastas de [dados/instalador/celulas/](dados/instalador/celulas/); o resto é texto escrito à mão.

## 1. O que foi pedido e o que foi decidido

O Eric pediu que o instalador funcionasse em Windows, Linux e macOS e que isso fosse provado em máquina nova, e não só na máquina em que o projeto foi feito. As decisões do projeto que moldaram o teste (texto completo em [decisoes.md](../1-decisoes-e-historico/decisoes.md)):

- **Decisão 138:** o macOS é testado nas máquinas de macOS do GitHub Actions, porque a licença do macOS não deixa simulá-lo dentro do Windows.
- **Decisão 139:** as versões das ferramentas passam a ter um registro só, o `versoes.json`, com a versão testada e a faixa aceita de cada uma; uma conferência semanal avisa quando uma versão nova quebra a instalação.
- **Decisão 140:** o instalador é um núcleo (`install.py`) com dois lançadores finos; quando não há um Python novo o bastante, o lançador baixa o `uv`, confere o SHA-256 e instala o Python dentro da pasta do projeto.
- **Decisão 141:** a matriz de testes (Windows 11 no Sandbox e em máquina virtual, Linux pelo WSL, Ubuntu de mesa em máquina virtual), com quatro níveis de prova e os testes leves de dia.
- **Decisão 142:** o Windows 10 não entra como máquina limpa; um integrante com o sistema licenciado faria o teste como máquina usada.
- **Decisão 143:** o plano está aprovado; cada célula limpa roda primeiro o instalador como ele está, para gravar a falha, e só depois o conserto é escrito, com o teste antes do código.
- **Decisão 147:** a saída capturada de um teste (os arquivos de uma pasta de rodada) não leva a tag de IA; o `celula.json` da pasta leva.
- **Decisão 153 (25/11/2026):** a prova em máquina nova antes da entrega é a do GitHub Actions (Windows, Ubuntu e macOS); o Sandbox, a máquina virtual e o Windows 10 de um integrante ficam declarados como não testados.
- **Decisão 160 (25/11/2026):** depois de a primeira execução do fluxo falhar nas quatro máquinas, os três problemas são consertados antes da entrega: a célula do Ubuntu tira o MySQL que a máquina do GitHub já traz, o macOS passa a tratar o root do MariaDB como o Linux, e o Windows só aceita executável do MariaDB.
- **Decisão 161 (25/11/2026):** no macOS o instalador instala o MariaDB da série 11.8 pelo Homebrew (fórmula `mariadb@11.8`), a série testada no projeto, e não a fórmula comum, que acompanha a versão mais nova.
- **Decisão 162 (25/11/2026):** o Mac com processador Intel entra como melhor esforço, porque o Homebrew deixou de publicar pacote pronto do PHP e do MariaDB para ele; a célula `M-15I` continua no fluxo.

O plano completo está em [plano-aprovado-instalador-unico.md](../../../claude-memoria/plano-aprovado-instalador-unico.md).

## 2. Como ler

**Célula.** Uma célula é um jeito de rodar o teste: uma máquina (ou uma instância do WSL) e o que se pede dela. Cada vez que uma célula roda, sai uma pasta de **rodada**, `celulas/<id>/<data-hora>/`, com o `celula.json` (o que rodou e com que código de saída) e, quando a prova chegou a rodar, o `registro.json` (o resultado de cada nível, o erro literal de cada falha e a versão de cada ferramenta contra o `versoes.json`).

**Os quatro níveis da prova** (`python install.py --conferir`, com `--ate` para parar antes):

| Nível | O que prova |
|---|---|
| N1 | O site e a API no ar: o PHP acha o `mysqli`, o MariaDB responde, as contagens do seed batem, o CobaiaFront responde com um produto do seed na página e a CobaiaAPI responde. |
| N2 | O navegador do agente: a venv do AgenteCore importa o Playwright na versão fixada, e o Chromium abre sem janela e carrega a página do CobaiaFront. |
| N3 | O Ollama: ele responde em `/api/version`, e um modelo pequeno baixa e devolve texto, só em CPU. |
| N4 | O modelo do projeto: o `qwen2.5:7b` baixa, o identificador confere com o do `versoes.json` e ele devolve texto. Só roda onde a memória der; onde não der, o registro diz "não coube", e isso não conta como falha do instalador. |

**Os dois modos.** `como-esta` é a rodada que roda o instalador do jeito que ele estava antes dos consertos, para gravar a falha de verdade (princípio do plano: a falha vem antes do conserto). `novo` é a rodada que roda o instalador depois dos consertos. Num mesmo id, a primeira rodada costuma ser `como-esta` e a última `novo`.

**Onde rodou.** `WSL` é uma instância limpa de Linux dentro do Windows do Eric, criada da imagem oficial e apagada no fim; `máquina-alvo` é o Windows do projeto como ele está; `GitHub Actions` é uma máquina que o GitHub cria para a execução.

## 3. O resumo

<!-- tb_inst_resumo:inicio -->
| Célula | Sistema | Como a máquina nasce | Onde rodou | Nível alcançado na última rodada | Prova pedida até | Maior nível em rodada novo |
|---|---|---|---|---|---|---|
| ALVO | Windows 11 da máquina-alvo | a máquina do projeto como está: o instalador não rodou nesta célula, só a prova, sobre a instalação que já existia | máquina-alvo | N4 | N4 | N4 |
| L-U2404 | Ubuntu 24.04 | WSL: imagem oficial importada e apagada no fim | WSL | N3 | N3 | N4 |
| L-U2404-SS | Ubuntu 24.04 sem systemd | WSL: imagem oficial, com o systemd desligado na instância | WSL | N3 | N3 | N3 |
| L-U2204 | Ubuntu 22.04 | WSL: imagem oficial importada e apagada no fim | WSL | N3 | N3 | N3 |
| L-U2604 | Ubuntu 26.04 | WSL: imagem oficial importada e apagada no fim | WSL | N3 | N3 | N3 |
| L-D12 | Debian 12 | WSL: imagem oficial importada e apagada no fim | WSL | N3 | N3 | N3 |
| L-D13 | Debian 13 | WSL: imagem oficial importada e apagada no fim | WSL | N3 | N3 | N3 |
| L-F45 | Fedora 45 (melhor esforço) | WSL: imagem oficial importada e apagada no fim | WSL | N1 | N3 | N1 |
| L-ARCH | Arch Linux (sem suporte) | WSL: imagem oficial importada e apagada no fim | WSL | N0 | N1 | N0 |
| L-SUSE | openSUSE (sem suporte) | WSL: imagem oficial importada e apagada no fim | WSL | N0 | N1 | N0 |
| CI-UBU | Ubuntu 24.04 do GitHub Actions | executor do GitHub; já traz Python, PHP e o MySQL 8.0, e a célula remove o MySQL antes do instalador; não é limpo | GitHub Actions | N4 | N4 | N4 |
| CI-WIN | Windows Server 2025 do GitHub Actions | executor do GitHub; já traz Python, PHP e banco, não é limpo | GitHub Actions | N4 | N4 | N4 |
| M-15 | macOS 15, Apple Silicon | executor do GitHub; já traz o Homebrew e o Python, não é limpo | GitHub Actions | N3 | N3 | N3 |
| M-15I | macOS 15, Intel (melhor esforço) | executor do GitHub; já traz o Homebrew e o Python, não é limpo | GitHub Actions | N4 | N4 | N4 |

Cada linha é uma célula de teste, e a coluna "Como a máquina nasce" diz o que ela é: na `ALVO` só a prova rodou. Nível alcançado é o maior nível da prova que passou sem nenhum nível abaixo dele ter falhado; N0 quer dizer que nenhum nível passou, "sem prova" quer dizer que a rodada parou antes de gravar o `registro.json`, e "não terminou" quer dizer que o GitHub cortou a tarefa antes do fim. Rodada `novo` é a que roda o instalador já com os consertos; `como-esta` é a que roda o instalador antes deles, para gravar a falha. A última coluna olha todas as rodadas `novo` da célula, porque a última rodada pode ter pedido menos níveis que uma anterior.
<!-- tb_inst_resumo:fim -->

## 4. O que passou e o que falhou, por sistema

<!-- tb_inst_matriz:inicio -->
| Célula | Rodadas | Primeira rodada | Última rodada |
|---|---|---|---|
| ALVO | 1 | 20261119-184751, novo, até N4: alcançou N4 | a mesma rodada |
| CI-UBU | 4 | 20261125-155844, novo, até N4: alcançou N0. N1: o MariaDB não respondeu (ensure_mariadb_running) | 20261126-110552, novo, preparo remover-mysql, até N4: alcançou N4 |
| CI-WIN | 4 | 20261125-155844, como-esta, até N4: alcançou N0. N1: o MariaDB não respondeu (ensure_mariadb_running) | 20261126-110559, novo, até N4: alcançou N4 |
| L-ARCH | 2 | 20261119-162745, como-esta, até N1: sem prova (a rodada parou antes de gravar o registro.json) | 20261119-162821, novo, até N1: alcançou N0. N1: cliente do MariaDB não encontrado (find_mysql_cli) |
| L-D12 | 2 | 20261119-151002, como-esta, até N3: alcançou N0. N1: o MariaDB não respondeu (ensure_mariadb_running) | 20261119-161617, novo, até N3: alcançou N3 |
| L-D13 | 2 | 20261119-083308, como-esta, até N3: alcançou N0. N1: o MariaDB não respondeu (ensure_mariadb_running) | 20261119-133320, novo, até N3: alcançou N3 |
| L-F45 | 3 | 20261119-085043, como-esta, até N3: alcançou N0. N1: cliente do MariaDB não encontrado (find_mysql_cli) | 20261119-144952, novo, até N3: alcançou N1. N2: eatures=CDPScreenshotNewSurface --allow-pre-commit-input --disable-hang-monitor --disable-ipc-flooding-protection --disable-popup-blocking --disable-prompt-on-repost --disable-renderer-backgrounding - |
| L-SUSE | 2 | 20261119-163121, como-esta, até N1: sem prova (a rodada parou antes de gravar o registro.json) | 20261119-163154, novo, até N1: alcançou N0. N1: cliente do MariaDB não encontrado (find_mysql_cli) |
| L-U2204 | 2 | 20261119-075036, como-esta, até N3: alcançou N0. N1: o MariaDB não respondeu (ensure_mariadb_running) | 20261119-130456, novo, até N3: alcançou N3 |
| L-U2404 | 6 | 20261118-193340, como-esta, até N3: alcançou N0. N1: o MariaDB não respondeu (ensure_mariadb_running) | 20261119-185423, novo, até N3: alcançou N3 |
| L-U2404-SS | 3 | 20261119-085151, como-esta, até N3: alcançou N0. N1: o MariaDB não respondeu (ensure_mariadb_running) | 20261119-125404, novo, até N3: alcançou N3 |
| L-U2604 | 2 | 20261119-082731, como-esta, até N3: alcançou N0. N1: o MariaDB não respondeu (ensure_mariadb_running) | 20261119-131225, novo, até N3: alcançou N3 |
| M-15 | 4 | 20261125-155840, como-esta, até N3: alcançou N0. N1: o MariaDB não respondeu (ensure_mariadb_running) | 20261126-110603, novo, até N3: alcançou N3 |
| M-15I | 4 | 20261125-155847, como-esta, até N4: alcançou N0. N1: o MariaDB não respondeu (ensure_mariadb_running) | 20261126-110601, novo, até N4: alcançou N4 |
<!-- tb_inst_matriz:fim -->

<!-- ! Alteração de IA - Revisar: (25/11/2026, conserto da revisão do I5/I7) o parágrafo do Linux pelo WSL e o da máquina-alvo deixam de afirmar nível alcançado em palavras e passam a dizer só quais células existem e qual é a regra de cada uma (decisão 141); o nível se lê na tabela gerada logo acima.
     ! Motivo: o texto à mão dizia "chegaram ao nível pedido na última rodada" e "o site e a API sobem"; quando uma rodada nova entrasse por `importar_actions.py` o bloco gerado mudaria e esta frase ficaria desatualizada sem o `--check` acusar. Nenhum nível fica escrito fora dos blocos. -->
**Linux pelo WSL.** As células são `L-U2404`, `L-U2404-SS` (sem systemd), `L-U2204`, `L-U2604`, `L-D12` e `L-D13` (Ubuntu e Debian, suportadas: o instalador tem de chegar ao nível pedido), `L-F45` (Fedora, melhor esforço: o navegador do agente depende de bibliotecas do sistema que o instalador só instala no Debian e no Ubuntu, e o plano deixa isso fora do escopo) e `L-ARCH` e `L-SUSE` (Arch Linux e openSUSE, sem suporte: o resultado esperado é a mensagem de "sem suporte" com a lista do que instalar à mão, e o nível baixo dessas duas linhas não é um defeito). A primeira rodada de cada distribuição foi no modo `como-esta`, para gravar a falha, e as falhas estão na seção 5 com a mensagem de erro de cada uma. O nível de cada rodada se lê na tabela acima, nunca neste texto.

**Windows da máquina-alvo.** A célula `ALVO` roda só a prova, nesta máquina, que não é limpa e onde o instalador não rodou: ela serve para mostrar que o `--conferir` acerta numa instalação que já funcionava. Não prova que o instalador do Windows funciona numa máquina nova.

<!-- ! Alteração de IA - Revisar: (25/11/2026, depois da primeira execução do fluxo) o parágrafo do GitHub Actions deixa de dizer que a primeira execução ainda vai acontecer e passa a dizer o que ela gravou e o que foi consertado em seguida, sem afirmar nível em palavras.
     ! Motivo: a execução 45650086543 (commit `9badcba8`) rodou em 25/11/2026 e falhou nas quatro células; o texto antigo dizia "até lá as quatro células aparecem como ainda sem rodada" e que o Windows e o macOS seguiam os passos antigos, o que deixou de ser verdade com os consertos das decisões 160 a 162. -->
<!-- ! Alteração de IA - Revisar: (25/11/2026, depois da segunda execução do fluxo) o parágrafo do GitHub Actions ganha o que a segunda execução gravou e o que ficou para a terceira, ainda sem afirmar nível em palavras.
     ! Motivo: a execução 45727470052 (commit `f305dee1`) rodou com os consertos da primeira; o texto dizia que nenhum conserto tinha sido visto rodando, o que deixou de ser verdade para o Ubuntu e para o macOS, e ela achou duas falhas novas (linhas HW9 e HM7 da seção 5). -->
<!-- ! Alteração de IA - Revisar: (26/11/2026, depois da terceira execução do fluxo) o parágrafo do GitHub Actions troca "a terceira execução é a prova" pelo que ela gravou; as linhas HW2, HW9 e HM7 da seção 5 passam a dizer que o conserto rodou, e entra a HM8.
     ! Motivo: a execução 45731004628 (commit `35617a47`) rodou na noite de 25/11/2026 com os consertos da segunda; o texto ainda dizia que o conserto do Windows e o do Ollama no macOS não tinham sido vistos rodando, e o instalador do Mac Intel parou num ponto novo, que fica declarado (decisão 153). -->
**GitHub Actions (Windows, Ubuntu e macOS em Apple Silicon e em Intel).** O fluxo está em [`.github/workflows/instalador.yml`](../../../.github/workflows/instalador.yml), e o resultado de cada execução entra aqui pelo `importar_actions.py` e pelo `relatorio.py --colar`. A primeira execução, de 25/11/2026 (execução 45650086543, commit `9badcba8`), falhou nas quatro células, cada uma por um motivo que a seção 5 conta (linhas HL15, HW7, HW8 e HM4). Os consertos foram escritos no mesmo dia (decisões 160 a 162): a célula do Ubuntu remove o MySQL que a máquina do GitHub traz antes de rodar o instalador, e declara esse preparo na evidência; o macOS passou para o mesmo fluxo por pacotes do Linux, com o MariaDB da fórmula `mariadb@11.8` do Homebrew; o Windows só aceita executável do MariaDB e traz o Ollama pelo instalador oficial, na versão testada. A segunda execução (45727470052, commit `f305dee1`) rodou com esses consertos: no Ubuntu a instalação foi até o fim; nos dois macOS a prova passou, mas o instalador ainda saiu como interrompido, por causa do último passo do script do Ollama (linha HM7); no Windows a busca nova funcionou e a instalação parou no passo seguinte, a criação da pasta de dados do MariaDB (linha HW9). A terceira execução (45731004628, commit `35617a47`) rodou com os consertos dessas duas falhas: no Ubuntu, no Windows e no macOS de Apple Silicon a instalação foi até o fim e a prova passou; no macOS com processador Intel a prova passou, mas o instalador parou ao baixar o `qwen2.5:7b` (linha HM8), o que fica declarado como limite do melhor esforço. A quarta execução (45807394622, commit `77fad232`, disparada por mudanças no `run.py` e no `Cobaia.py`) repetiu o mesmo resultado nas quatro células. O nível de cada célula se lê nas tabelas geradas, nunca nesta frase. O Mac com processador Intel (`M-15I`) é melhor esforço: o Homebrew não publica mais pacote pronto do PHP e do MariaDB para ele, e a máquina Intel do GitHub só os recebeu prontos porque usa as fórmulas de 24/08/2026.

## 5. As suspeitas levantadas na leitura do código e o que cada célula mostrou

<!-- ! Alteração de IA - Revisar: (25/11/2026, depois da primeira execução do fluxo) a abertura da seção passa a dizer quais suspeitas de Windows e de macOS a primeira execução do GitHub Actions exercitou, e a tabela ganha as linhas HL15, HW1 a HW8 e HM1 a HM6.
     ! Motivo: o texto antigo dizia que as suspeitas de Windows e de macOS seguiam sem teste até a primeira execução do fluxo; ela rodou em 25/11/2026 (execução 45650086543) e gravou três falhas que a leitura do código não tinha previsto com esse desenho (o MySQL do executor no Ubuntu e no Windows, e o código de saída do `install.cmd`). -->
Antes de rodar qualquer célula, a leitura do código do instalador levantou suspeitas de falha em máquina limpa: as de Linux têm o prefixo HL, as de Windows HW e as de macOS HM. As células de Linux gravaram o erro literal de cada uma antes do conserto, e todas as de Linux tiveram teste. A primeira execução do fluxo do GitHub Actions (execução 45650086543, de 25/11/2026) exercitou parte das de Windows e de macOS e achou outras (HL15, HW7, HW8); as que dependem de faltar o Python, o `winget`, o PHP do Windows ou o Homebrew seguem sem teste, porque as máquinas do GitHub já trazem tudo isso. A segunda execução (45727470052) rodou com os consertos da primeira e achou mais duas (HW9 e HM7); a terceira (45731004628) rodou com os consertos dessas duas, levou o Windows até o fim e achou a HM8, que fica declarada. Onde a coluna "Estado" diz "conserto escrito", o conserto ainda não tinha sido visto rodando quando este texto foi escrito: a rodada `novo` seguinte da célula é a prova. Os arquivos de evidência estão nas pastas de rodada citadas na última coluna.

| Id | O que se suspeitava | Estado | Erro literal | Evidência |
|---|---|---|---|---|
| HL1 | O `install.sh` não tem permissão de execução no pacote. | Confirmada e consertada: o modo executável entra pelo índice do git, e a rodada `novo` rodou `./install.sh` direto. | `timeout: failed to run command ‘./install.sh’: Permission denied`, código 126 | [instalacao_direto.log](dados/instalador/celulas/L-U2404/20261118-193340/instalacao_direto.log), [HL1.txt](dados/instalador/celulas/L-U2404/20261118-193340/suspeitas/HL1.txt) |
| HL2 | Sem o pacote `python3-venv`, a venv não é criada. | Confirmada e consertada: o pacote entra na lista do `apt`. | `The virtual environment was not created successfully because ensurepip is not available. On Debian/Ubuntu systems, you need to install the python3-venv package` | [HL2.txt](dados/instalador/celulas/L-U2404/20261118-193340/suspeitas/HL2.txt) |
| HL3 | O instalador antigo só sabe o `apt`; em Fedora, Arch e openSUSE manda fazer a coisa errada. | Confirmada e consertada: o caminho do `dnf` existe e os sistemas sem suporte recebem uma mensagem com a lista do que instalar à mão. | `sudo: apt-get: command not found`, e no Arch `Gerenciador de pacotes não reconhecido. Instale Python 3 manualmente e rode ./install.sh de novo.` | [Fedora, instalacao.log](dados/instalador/celulas/L-F45/20261119-085043/instalacao.log), [Arch, instalacao.log](dados/instalador/celulas/L-ARCH/20261119-162745/instalacao.log) |
| HL4 | As opções `-d extension_dir=...` que o `run.py` passa ao PHP são do Windows e escondem as extensões no Linux. | Confirmada e consertada: as opções passaram a depender do sistema. | `Error: Class "mysqli" not found in .../conn/connect.php:13`, com o site respondendo `HTTP 500` | [HL4.txt](dados/instalador/celulas/L-U2404/20261118-193340/suspeitas/HL4.txt) |
| HL5 | O instalador não instala o Ollama no Linux (só imprime o comando e segue). | Confirmada na primeira metade: o instalador imprime o comando e devolve `None`; que ele segue até "Instalação concluída" depois disso é leitura do código. Consertada: o script oficial é baixado e rodado. | `sem ollama no PATH` | [HL5.txt](dados/instalador/celulas/L-U2404/20261118-193340/suspeitas/HL5.txt) |
| HL6 | O Chromium do Playwright não abre sem bibliotecas do sistema. | Confirmada e consertada com `playwright install --with-deps` (Debian e Ubuntu). No Fedora o instalador só avisa quais faltam. | `chrome-headless-shell: error while loading shared libraries: libnspr4.so: cannot open shared object file` | [HL6.txt](dados/instalador/celulas/L-U2404/20261118-193340/suspeitas/HL6.txt) |
| HL7 | Sem systemd (como numa instância de WSL sem ele), o serviço do MariaDB não sobe. | Confirmada e consertada: o instalador usa `service` quando não há systemd. | `System has not been booted with systemd as init system (PID 1). Can't operate.` | [HL7.txt](dados/instalador/celulas/L-U2404-SS/20261119-085151/suspeitas/HL7.txt) |
| HL8 | O Python do sistema pode ser velho demais para o código do projeto. | Confirmada e consertada: o lançador traz o Python pelo `uv` quando o do sistema não serve. | `SyntaxError: f-string expression part cannot include a backslash` | [HL8.txt](dados/instalador/celulas/L-U2204/20261119-075036/suspeitas/HL8.txt) |
| HL9 | Um clone feito no Windows traz o `install.sh` com fim de linha do Windows. | Confirmada e consertada pelo `.gitattributes`, que fixa o fim de linha dos roteiros. | `bash install.sh`: `line 7: set: pipefail: invalid option name`; `./install.sh`: `/usr/bin/env: ‘bash\r’: No such file or directory` | [HL9.txt](dados/instalador/celulas/L-U2404/20261118-193340/suspeitas/HL9.txt) |
| HL10 | O root do MariaDB no Linux entra pelo `unix_socket`, e o `connect.php` do site precisa de root sem senha. | Metade confirmada, metade derrubada: o root realmente entra pelo `unix_socket`; o conserto antigo do root funciona quando é chamado, e o defeito real era a HL12. A entrada do root passou a ter ordem nova e pergunta antes. | `ERROR 1698 (28000): Access denied for user 'root'@'localhost'` | [HL10.txt](dados/instalador/celulas/L-U2404/20261118-193340/suspeitas/HL10.txt) |
| HL11 | O site usa `mb_strimwidth`, que no Debian e no Ubuntu vem no pacote `php-mbstring`. | Confirmada e consertada: o pacote entra na lista. | `PHP Fatal error: Uncaught Error: Call to undefined function mb_strimwidth()` | [HL11.txt](dados/instalador/celulas/L-U2404/20261118-193340/suspeitas/HL11.txt) |
| HL12 | (achada na primeira célula) O instalador testa "o banco está no ar" tentando entrar como root sem senha, e nunca chega ao conserto do root. | Confirmada e consertada: o banco passou a ser ligado antes, com e sem systemd. | `Não foi possível subir o MariaDB. Verifique a instalação e rode o instalador de novo.`, com o serviço no ar | [instalacao.log](dados/instalador/celulas/L-U2404/20261118-193340/instalacao.log) |
| HL13 | (achada na primeira célula) `apt-get install php php-mysql` traz um servidor Apache que o projeto não usa. | Confirmada e consertada: o instalador pede `php-cli`, sem o pacote que puxa o Apache. | `apache2 apache2-bin apache2-data apache2-utils libapache2-mod-php...` na lista de pacotes novos | [instalacao.log](dados/instalador/celulas/L-U2404/20261118-193340/instalacao.log) |
| HL14 | (achada na célula do Fedora) O script oficial do Ollama exige o `awk`, que a imagem do Fedora não traz. | Confirmada e consertada: o `gawk` entra nos pacotes de base do `dnf`. | `>>> ERROR: The following tools are required but missing:` seguido de `  - awk` | [instalacao.log](dados/instalador/celulas/L-F45/20261119-134801/instalacao.log) |
| HL15 | (achada na célula `CI-UBU`) A máquina já tem outro servidor de banco: a do GitHub traz o MySQL 8.0. | Confirmada, e o instalador fez o que foi desenhado para fazer: parou e disse o motivo, sem remover o banco de ninguém. Ele não mudou; a célula passou a remover o MySQL antes do instalador e a declarar esse preparo na evidência (decisão 160). Na rodada seguinte, com o preparo, a instalação foi até o fim. | `E: Packages need to be removed but remove is disabled.`, seguido de `Instalação interrompida: o apt-get não conseguiu instalar: php-cli php-mysql php-mbstring mariadb-server.` | [instalacao.log](dados/instalador/celulas/CI-UBU/20261125-155844/instalacao.log), [estado_inicial.txt](dados/instalador/celulas/CI-UBU/20261125-155844/estado_inicial.txt); com o preparo: [preparo.log](dados/instalador/celulas/CI-UBU/20261126-001605/preparo.log), [celula.json](dados/instalador/celulas/CI-UBU/20261126-001605/celula.json) |
| HW1 | O `install.ps1` aceita como Python o atalho da Microsoft Store, que não roda nada. | Sem teste: a máquina do GitHub já traz um Python de verdade, e as células do Windows limpo saíram de antes da entrega (decisão 153). | - | - |
| HW2 | Sem o `winget`, o `install.ps1` e o `install.py` param com erro de comando não encontrado. | Sem teste: a máquina do GitHub tem o `winget` (v1.11.510 no estado inicial da célula), então nenhuma célula gravou o instalador sem ele. O Ollama do Windows deixou de vir do `winget` por outro motivo: ele instalava a versão do dia, e não a testada, e o `ollama pull` seguinte rodava sem esperar o servidor nem conferir o resultado; o Ollama passou a vir do instalador oficial, na versão testada (seção 3.2 do plano aprovado). Na terceira execução esse instalador oficial instalou o Ollama 0.40.16 no Windows do GitHub e o modelo respondeu. O Python e o PHP continuam vindo do `winget` quando faltam. | - | [estado_inicial.txt](dados/instalador/celulas/CI-WIN/20261125-155844/estado_inicial.txt); [registro.json](dados/instalador/celulas/CI-WIN/20261126-004542/registro.json) |
| HW3 | Depois de o `winget` instalar o Python, a mesma janela não o enxerga. | Sem teste, pelo mesmo motivo da HW1. | - | - |
| HW4 | O PHP 8.2 não abre sem o Visual C++ Redistributable. | Sem teste: a máquina do GitHub já traz o PHP. | - | - |
| HW5 | Com administrador, o `winget install MariaDB.Server` traz a série 12 ou 13, e não a 11.8. | Sem teste: na célula o MariaDB vem do zip da série 11.8. O caminho do MSI pelo `winget` continua valendo para quem tem administrador e não tem MySQL, e não foi provado em máquina nova. | - | - |
| HW6 | O Defender ou o SmartScreen barra ou atrasa o `Cobaia.exe`. | Sem teste: as células do Windows limpo com o Defender saíram de antes da entrega (decisão 153). | - | - |
| HW7 | (achada na célula `CI-WIN`) O instalador aceita o cliente do MySQL como se fosse o do MariaDB. | Confirmada e consertada: as buscas só aceitam executável cujo `--version` diga MariaDB, e com um MySQL na máquina o MariaDB vem do zip portátil, ao lado dele (decisão 160). Na rodada seguinte o instalador avisou do MySQL, baixou o zip do MariaDB e conferiu o SHA-256; a falha seguinte dessa rodada é a HW9. | `Cliente MariaDB/MySQL já disponível: C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.EXE` e, em seguida, `Não foi possível subir o MariaDB. Verifique a instalação e rode o instalador de novo.` | [instalacao.log](dados/instalador/celulas/CI-WIN/20261125-155844/instalacao.log), [estado_inicial.txt](dados/instalador/celulas/CI-WIN/20261125-155844/estado_inicial.txt); depois do conserto: [instalacao.log](dados/instalador/celulas/CI-WIN/20261126-001604/instalacao.log) |
| HW8 | (achada na célula `CI-WIN`) O `install.cmd` sai com código 0 mesmo quando a instalação para. | Confirmada e consertada: o `install.ps1` repassa o código do `install.py` (e os argumentos, que antes se perdiam) e o `install.cmd` devolve esse código depois do `pause`. Na rodada seguinte a instalação parou e o `install.cmd` saiu com código 1. | `Códigos de saída: {"instalador": "0", "conferir": "1"}` com `Resultado gravado pelo instalador: interrompida` | [celula.json](dados/instalador/celulas/CI-WIN/20261125-155844/celula.json); depois do conserto: [celula.json](dados/instalador/celulas/CI-WIN/20261126-001604/celula.json) |
| HW9 | (achada na célula `CI-WIN`, na segunda execução) Num clone novo a pasta `.mariadb` não existe, e o `mariadb-install-db.exe` não cria a pasta de cima da pasta de dados. | Confirmada e consertada: o instalador cria a pasta antes e para ali se o MariaDB portátil não ficou pronto, em vez de tentar subir um servidor sem dados. Na máquina do projeto a pasta já existia desde 07/11/2026, e por isso o defeito nunca tinha aparecido. Na rodada seguinte (terceira execução) a pasta foi criada, o MariaDB portátil subiu e a instalação foi até o fim. | `FATAL ERROR: Can't create data directory 'D:\a\TCC\TCC\.mariadb\data' (one or more intermediate directories do not exist)` | [instalacao.log](dados/instalador/celulas/CI-WIN/20261126-001604/instalacao.log); depois do conserto: [instalacao.log](dados/instalador/celulas/CI-WIN/20261126-004542/instalacao.log), [celula.json](dados/instalador/celulas/CI-WIN/20261126-004542/celula.json) |
| HM1 | Sem o Homebrew, o instalador para com um aviso. | Sem teste: a máquina do GitHub já traz o Homebrew. | - | - |
| HM2 | O `brew install php` traz o PHP 8.5; o site foi validado no 8.2. | Vem mesmo o 8.5, e o site funciona nele: na rodada `novo` das duas células de macOS o site e a API responderam com o PHP 8.5.12 (Apple Silicon, trazido pelo `brew install php`) e com o 8.5.9 (Intel, que a máquina já trazia), os dois dentro da faixa que o `versoes.json` aceita. | - | [registro.json](dados/instalador/celulas/M-15/20261126-001559/registro.json), [registro.json](dados/instalador/celulas/M-15I/20261126-001606/registro.json) |
| HM3 | O cask `ollama` mudou de nome no Homebrew. | Deixou de valer: no macOS o Ollama passou a vir do script oficial, na versão testada, e não mais do Homebrew. | - | - |
| HM4 | O `brew services start mariadb` sobe, mas o root sem senha não foi conferido. | Confirmada, e pior do que a suspeita: o root do MariaDB só entra pelo usuário root do sistema, o instalador leu essa recusa como banco desligado, tentou subir um segundo servidor e parou. Consertada: o macOS passou para o fluxo por pacotes do Linux, o serviço é conferido pelo `mariadb-admin ping`, e o root é acertado pela conta do usuário que instalou o MariaDB (decisão 160). Na rodada seguinte, nas duas células, o banco subiu pelo Homebrew, o root foi acertado e o site e a API responderam. | `Não foi possível subir o MariaDB. Verifique a instalação e rode o instalador de novo.`, logo depois de o Homebrew responder que o serviço do MariaDB tinha subido | [instalacao.log](dados/instalador/celulas/M-15/20261125-155840/instalacao.log); [instalacao.log](dados/instalador/celulas/M-15I/20261125-155847/instalacao.log); depois do conserto: [registro.json](dados/instalador/celulas/M-15/20261126-001559/registro.json), [registro.json](dados/instalador/celulas/M-15I/20261126-001606/registro.json) |
| HM5 | (achada na leitura da fórmula do Homebrew) A fórmula `mariadb` acompanha a versão mais nova, que saiu da faixa aceita. | Tratada antes de falhar: em 25/11/2026 a fórmula estava na 13.1.2 (`Formula/m/mariadb.rb` do Homebrew) e o `versoes.json` aceita até a 13.0; o instalador pararia no fim com "a versão de mariadb impede seguir". Ele passou a instalar a fórmula `mariadb@11.8` (decisão 161), e na rodada seguinte o Homebrew entregou o MariaDB 11.8.10 na célula de Apple Silicon e o 11.8.9 na Intel. | - | [registro.json](dados/instalador/celulas/M-15/20261126-001559/registro.json), [registro.json](dados/instalador/celulas/M-15I/20261126-001606/registro.json) |
| HM6 | (achada na leitura das fórmulas do Homebrew) Não há pacote pronto do PHP nem do MariaDB para Mac com processador Intel. | Declarada: em 25/11/2026 o bloco `bottle` das fórmulas `php`, `mariadb` e `mariadb@11.8` só trazia Apple Silicon e Linux; num Mac Intel o Homebrew compila do código-fonte. O Mac Intel entra como melhor esforço, e a célula `M-15I` continua (decisão 162). Na rodada seguinte a máquina Intel do GitHub, que usa as fórmulas de 24/08/2026, ainda recebeu os pacotes prontos: o passo dos pacotes levou 32,5 s. Num Mac Intel com o Homebrew de hoje isso não vale. | - | [estado_inicial.txt](dados/instalador/celulas/M-15I/20261126-001606/estado_inicial.txt), [passos.json](dados/instalador/celulas/M-15I/20261126-001606/passos.json) |
| HM7 | (achada nas duas células de macOS, na segunda execução) O último passo do script oficial do Ollama, que abre o aplicativo pelo nome, falha logo depois de instalar. | Confirmada e consertada: o script roda sem esse passo (`OLLAMA_NO_START`) e o instalador abre o aplicativo pelo caminho, sem parar se não der. Nas duas células a prova passou mesmo com o instalador interrompido, porque o Ollama já estava instalado e a prova sobe o servidor e baixa o modelo sozinha. Na rodada seguinte (terceira execução) o script terminou sem erro nas duas células e o aplicativo foi aberto pelo caminho; na de Apple Silicon a instalação foi até o fim, e na Intel parou mais adiante, ao baixar o modelo (HM8). | `Unable to find application named 'Ollama'`, seguido de `Instalação interrompida: o script do Ollama saiu com erro; a mensagem dele está logo acima.` | [instalacao.log](dados/instalador/celulas/M-15/20261126-001559/instalacao.log), [instalacao.log](dados/instalador/celulas/M-15I/20261126-001606/instalacao.log); depois do conserto: [instalacao.log](dados/instalador/celulas/M-15/20261126-004539/instalacao.log), [instalacao.log](dados/instalador/celulas/M-15I/20261126-004542/instalacao.log) |
| HM8 | (achada na célula `M-15I`, na terceira execução) No Mac com processador Intel, o `ollama pull qwen2.5:7b` do instalador cai logo depois de o aplicativo do Ollama ser aberto. | Confirmada e não consertada: aconteceu nas execuções em que o instalador chegou a esse passo (a terceira e a quarta). A causa não foi investigada. Na mesma rodada a prova baixou o mesmo modelo minutos depois e ele respondeu, com o identificador conferindo. Fica declarada (decisão 153): no Mac Intel, que é melhor esforço (decisão 162), o instalador pode parar nesse passo com tudo o mais instalado; as saídas, que não foram testadas, são rodar o `./install.sh` de novo ou baixar o modelo à mão. No Mac de Apple Silicon, que baixa o modelo pequeno na célula, isso não apareceu. | `Error: unexpected EOF`, seguido de "Instalação interrompida: `ollama pull qwen2.5:7b` falhou; a mensagem está logo acima." | [instalacao.log](dados/instalador/celulas/M-15I/20261126-004542/instalacao.log), [registro.json](dados/instalador/celulas/M-15I/20261126-004542/registro.json); quarta execução: [instalacao.log](dados/instalador/celulas/M-15I/20261126-110601/instalacao.log) |

<!-- ! Alteração de IA - Revisar: (26/11/2026, decisão 180) a seção 6 passa a se chamar "Limitações e trabalho futuro" e ganha duas tabelas geradas por `relatorio.py` (blocos `limites` e `futuro`), antes da lista das células que não rodaram; o que nenhuma célula prova vira a subseção 6.3.
     ! Motivo: o Eric pediu que os sistemas em que o instalador não foi provado até o fim fiquem declarados com duas palavras, limitação e trabalho futuro. A seção dizia só o que não foi testado, e quem lia a tabela do resumo não via que "N3" numa célula que pediu N3 também é um limite: o modelo do projeto não foi provado ali. As duas tabelas saem das pastas de rodada, para nenhum nível ficar digitado. -->
## 6. Limitações e trabalho futuro

O instalador foi provado até o fim em poucos sistemas, e o resto fica declarado com duas palavras (decisão 180, de 26/11/2026): **limitação** é o que o projeto entrega hoje em cada sistema, ou seja, até onde a prova chegou; **trabalho futuro** é o que falta provar. "Até o fim" quer dizer a instalação concluída e a prova até o N4, com o modelo do projeto respondendo, numa máquina em que o instalador rodou. As duas tabelas abaixo são escritas por `relatorio.py` a partir das pastas de rodada.

### 6.1 Limitação: até onde cada sistema foi provado

<!-- tb_inst_limites:inicio -->
**Provado até o fim** (instalação concluída e prova até o N4): Ubuntu 24.04 (`L-U2404`, WSL); Ubuntu 24.04 do GitHub Actions (`CI-UBU`, GitHub Actions); Windows Server 2025 do GitHub Actions (`CI-WIN`, GitHub Actions).

| Célula | Sistema | Onde rodou | Até onde a prova chegou | Maior nível pedido | Instalador na última rodada | Limitação |
|---|---|---|---|---|---|---|
| ALVO | Windows 11 da máquina-alvo | máquina-alvo | N4 | N4 | não rodou | só a prova rodou, sobre a instalação que já existia; o instalador não rodou nesta máquina |
| L-U2404-SS | Ubuntu 24.04 sem systemd | WSL | N3 | N3 | concluído | o N4, com o modelo do projeto respondendo, não foi pedido nesta célula |
| L-U2204 | Ubuntu 22.04 | WSL | N3 | N3 | concluído | o N4, com o modelo do projeto respondendo, não foi pedido nesta célula |
| L-U2604 | Ubuntu 26.04 | WSL | N3 | N3 | concluído | o N4, com o modelo do projeto respondendo, não foi pedido nesta célula |
| L-D12 | Debian 12 | WSL | N3 | N3 | concluído | o N4, com o modelo do projeto respondendo, não foi pedido nesta célula |
| L-D13 | Debian 13 | WSL | N3 | N3 | concluído | o N4, com o modelo do projeto respondendo, não foi pedido nesta célula |
| L-F45 | Fedora 45 (melhor esforço) | WSL | N1 | N3 | concluído | a prova ficou abaixo do nível pedido (melhor esforço) |
| L-ARCH | Arch Linux (sem suporte) | WSL | N0 | N1 | interrompido | sem suporte, de propósito: o instalador para e diz o que instalar à mão |
| L-SUSE | openSUSE (sem suporte) | WSL | N0 | N1 | interrompido | sem suporte, de propósito: o instalador para e diz o que instalar à mão |
| M-15 | macOS 15, Apple Silicon | GitHub Actions | N3 | N3 | concluído | o N4, com o modelo do projeto respondendo, não foi pedido nesta célula |
| M-15I | macOS 15, Intel (melhor esforço) | GitHub Actions | N4 | N4 | interrompido | a prova passou, mas o instalador não foi até o fim (melhor esforço) |

"Até onde a prova chegou" é o maior nível alcançado numa rodada `novo`, que é a do instalador depois dos consertos (na célula em que só a prova rodou, é o nível da última rodada). "Maior nível pedido" existe porque nem toda célula pede o N4. "Instalador na última rodada" diz se o instalador terminou, parou no meio ou nem rodou.
<!-- tb_inst_limites:fim -->

### 6.2 Trabalho futuro: o que falta provar

<!-- tb_inst_futuro:inicio -->
| O que falta provar | Por que ficou de fora |
|---|---|
| A prova até o N4, com o modelo do projeto respondendo, em: Ubuntu 24.04 sem systemd (`L-U2404-SS`), Ubuntu 22.04 (`L-U2204`), Ubuntu 26.04 (`L-U2604`), Debian 12 (`L-D12`), Debian 13 (`L-D13`), macOS 15, Apple Silicon (`M-15`) | essas células pediram a prova só até o N3 |
| O instalador até o fim em: macOS 15, Intel (melhor esforço) (`M-15I`) | na última rodada a prova passou e o instalador foi interrompido (seção 5 do relatório do instalador) |
| O nível pedido em: Fedora 45 (melhor esforço) (`L-F45`) (ficou no N1 de N3) | melhor esforço: o instalador não instala tudo de que esse sistema precisa |
| Windows 11 no Windows Sandbox (`W11-SB`) | decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions; esta pedia ligar um recurso do Windows e reiniciar a máquina do projeto |
| Windows 11 Enterprise de avaliação em máquina virtual, com o Defender ligado (`W11-VM-D1`) | decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions; esta pedia baixar a imagem de avaliação e criar uma máquina virtual no Hyper-V |
| Windows 11 Enterprise de avaliação em máquina virtual, com o Defender desligado (`W11-VM-D0`) | decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions; esta pedia baixar a imagem de avaliação e criar uma máquina virtual no Hyper-V |
| Windows Server 2022 de avaliação em máquina virtual (`WS22-VM`) | decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions; esta pedia baixar a imagem de avaliação e criar uma máquina virtual no Hyper-V |
| Ubuntu 24.04 de mesa em máquina virtual (`L-U2404-VM`) | decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions; esta pedia baixar a imagem do Ubuntu de mesa e criar uma máquina virtual no Hyper-V |
| Windows 10 de um integrante (`W10-USADO`) | decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions; esta pedia o computador de um integrante |
| O MariaDB instalado pelo MSI do `winget`, no Windows com administrador e sem MySQL | a célula do Windows usa o zip portátil do MariaDB; o outro caminho não foi exercitado em máquina nova |
| O Python e o PHP trazidos pelo `winget`, no Windows | a máquina do GitHub já traz os dois |
| Um Mac sem o Homebrew | a máquina do GitHub já traz o Homebrew |
| Windows e Linux em processador ARM | nenhuma célula da matriz roda nesses processadores |
<!-- tb_inst_futuro:fim -->

As células abaixo estavam na matriz do plano e não foram rodadas:

<!-- tb_inst_nao_testadas:inicio -->
| Célula | Sistema | Por que não foi testada |
|---|---|---|
| W11-SB | Windows 11 no Windows Sandbox | decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions; esta pedia ligar um recurso do Windows e reiniciar a máquina do projeto |
| W11-VM-D1 | Windows 11 Enterprise de avaliação em máquina virtual, com o Defender ligado | decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions; esta pedia baixar a imagem de avaliação e criar uma máquina virtual no Hyper-V |
| W11-VM-D0 | Windows 11 Enterprise de avaliação em máquina virtual, com o Defender desligado | decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions; esta pedia baixar a imagem de avaliação e criar uma máquina virtual no Hyper-V |
| WS22-VM | Windows Server 2022 de avaliação em máquina virtual | decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions; esta pedia baixar a imagem de avaliação e criar uma máquina virtual no Hyper-V |
| L-U2404-VM | Ubuntu 24.04 de mesa em máquina virtual | decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions; esta pedia baixar a imagem do Ubuntu de mesa e criar uma máquina virtual no Hyper-V |
| W10-USADO | Windows 10 de um integrante | decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions; esta pedia o computador de um integrante |
<!-- tb_inst_nao_testadas:fim -->

### 6.3 O que nenhuma célula prova

Mesmo com todas as células do GitHub rodadas, há coisas que a matriz não prova (seção 4.4 do plano):

- **O WSL não é um Linux instalado.** Ele não prova o serviço que sobe no boot, o navegador com janela numa área de trabalho real nem o kernel da distribuição.
- **Os executores do GitHub não são máquinas limpas.** Eles já trazem Python, PHP, banco e, no macOS, o Homebrew. Cada célula grava o que a máquina trazia antes do instalador (`estado_inicial.txt`), para a leitura saber o que foi aproveitado. O Mac sem o Homebrew e o uso pela janela ficam sem prova.
- **A máquina de Ubuntu do GitHub traz o MySQL, e a célula o remove.** O instalador não troca o banco de ninguém, e por isso a célula `CI-UBU` tira o MySQL antes de rodá-lo. O que essa célula prova é a instalação numa máquina de onde o MySQL já saiu; numa máquina com o MySQL instalado o instalador para e diz o motivo (linha HL15 da seção 5).
- **No Windows, só um dos dois caminhos do MariaDB é exercitado.** A célula `CI-WIN` usa o zip portátil da série 11.8. O caminho do MSI pelo `winget`, que continua valendo para quem tem administrador e não tem MySQL, não foi provado em máquina nova; o PHP e o Python do Windows também não, porque a máquina do GitHub já traz os dois.
- **O Mac com processador Intel é melhor esforço.** O Homebrew deixou de publicar pacote pronto do PHP e do MariaDB para ele, e num Mac Intel atualizado a instalação compila os dois do código-fonte. A máquina Intel do GitHub é uma imagem antiga e ainda pode trazer os pacotes prontos; o que a célula `M-15I` mostra vale para essa imagem. Nela a prova passou, mas o instalador parou ao baixar o `qwen2.5:7b` (linha HM8 da seção 5), e isso não foi consertado.
- **O Windows 10 de mesa limpo não é testado.** O Windows Server de avaliação seria o sistema limpo mais próximo, e o computador de um integrante seria uma máquina usada; nenhum dos dois rodou.
- **Windows e Linux em processador ARM ficam de fora.**
- **Nenhuma célula mede tempo de diagnóstico.** Isso é das corridas do agente.

## 7. Todas as rodadas

<!-- tb_inst_rodadas:inicio -->
| Célula | Rodada | Onde | Modo | Até | Alcançou | N1 | N2 | N3 | N4 | Commit | Versão impede |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ALVO | 20261119-184751 | máquina-alvo | novo | N4 | N4 | passou | passou | passou | passou | - | - |
| CI-UBU | 20261125-155844 | GitHub Actions | novo | N4 | N0 | falhou | nao_rodou | falhou | nao_rodou | 9badcba8 | mariadb |
| CI-UBU | 20261126-001605 | GitHub Actions | novo | N4 | N4 | passou | passou | passou | passou | f305dee1 | - |
| CI-UBU | 20261126-004541 | GitHub Actions | novo | N4 | N4 | passou | passou | passou | passou | 35617a47 | - |
| CI-UBU | 20261126-110552 | GitHub Actions | novo | N4 | N4 | passou | passou | passou | passou | 77fad232 | - |
| CI-WIN | 20261125-155844 | GitHub Actions | como-esta | N4 | N0 | falhou | nao_rodou | falhou | nao_rodou | 9badcba8 | mariadb |
| CI-WIN | 20261126-001604 | GitHub Actions | novo | N4 | N0 | falhou | nao_rodou | falhou | nao_rodou | f305dee1 | - |
| CI-WIN | 20261126-004542 | GitHub Actions | novo | N4 | N4 | passou | passou | passou | passou | 35617a47 | - |
| CI-WIN | 20261126-110559 | GitHub Actions | novo | N4 | N4 | passou | passou | passou | passou | 77fad232 | - |
| L-ARCH | 20261119-162745 | WSL | como-esta | N1 | sem prova | - | - | - | - | - | - |
| L-ARCH | 20261119-162821 | WSL | novo | N1 | N0 | falhou | nao_rodou | nao_rodou | nao_rodou | - | - |
| L-D12 | 20261119-151002 | WSL | como-esta | N3 | N0 | falhou | nao_rodou | falhou | nao_rodou | - | python |
| L-D12 | 20261119-161617 | WSL | novo | N3 | N3 | passou | passou | passou | nao_rodou | - | - |
| L-D13 | 20261119-083308 | WSL | como-esta | N3 | N0 | falhou | nao_rodou | falhou | nao_rodou | - | - |
| L-D13 | 20261119-133320 | WSL | novo | N3 | N3 | passou | passou | passou | nao_rodou | - | - |
| L-F45 | 20261119-085043 | WSL | como-esta | N3 | N0 | falhou | nao_rodou | falhou | nao_rodou | - | - |
| L-F45 | 20261119-134801 | WSL | novo | N3 | N1 | passou | falhou | falhou | nao_rodou | - | - |
| L-F45 | 20261119-144952 | WSL | novo | N3 | N1 | passou | falhou | passou | nao_rodou | - | - |
| L-SUSE | 20261119-163121 | WSL | como-esta | N1 | sem prova | - | - | - | - | - | - |
| L-SUSE | 20261119-163154 | WSL | novo | N1 | N0 | falhou | nao_rodou | nao_rodou | nao_rodou | - | - |
| L-U2204 | 20261119-075036 | WSL | como-esta | N3 | N0 | falhou | nao_rodou | falhou | nao_rodou | - | python |
| L-U2204 | 20261119-130456 | WSL | novo | N3 | N3 | passou | passou | passou | nao_rodou | - | - |
| L-U2404 | 20261118-193340 | WSL | como-esta | N3 | N0 | falhou | nao_rodou | falhou | nao_rodou | - | - |
| L-U2404 | 20261119-090917 | WSL | novo | N3 | N0 | falhou | nao_rodou | falhou | nao_rodou | - | - |
| L-U2404 | 20261119-094340 | WSL | novo | N3 | N1 | passou | falhou | passou | nao_rodou | - | - |
| L-U2404 | 20261119-095322 | WSL | novo | N3 | N3 | passou | passou | passou | nao_rodou | - | - |
| L-U2404 | 20261119-163315 | WSL | novo | N4 | N4 | passou | passou | passou | passou | - | - |
| L-U2404 | 20261119-185423 | WSL | novo | N3 | N3 | passou | passou | passou | nao_rodou | - | - |
| L-U2404-SS | 20261119-085151 | WSL | como-esta | N3 | N0 | falhou | nao_rodou | falhou | nao_rodou | - | - |
| L-U2404-SS | 20261119-095855 | WSL | novo | N3 | N3 | passou | passou | passou | nao_rodou | - | - |
| L-U2404-SS | 20261119-125404 | WSL | novo | N3 | N3 | passou | passou | passou | nao_rodou | - | - |
| L-U2604 | 20261119-082731 | WSL | como-esta | N3 | N0 | falhou | nao_rodou | falhou | nao_rodou | - | - |
| L-U2604 | 20261119-131225 | WSL | novo | N3 | N3 | passou | passou | passou | nao_rodou | - | - |
| M-15 | 20261125-155840 | GitHub Actions | como-esta | N3 | N0 | falhou | nao_rodou | falhou | nao_rodou | 9badcba8 | - |
| M-15 | 20261126-001559 | GitHub Actions | novo | N3 | N3 | passou | passou | passou | nao_rodou | f305dee1 | - |
| M-15 | 20261126-004539 | GitHub Actions | novo | N3 | N3 | passou | passou | passou | nao_rodou | 35617a47 | - |
| M-15 | 20261126-110603 | GitHub Actions | novo | N3 | N3 | passou | passou | passou | nao_rodou | 77fad232 | - |
| M-15I | 20261125-155847 | GitHub Actions | como-esta | N4 | N0 | falhou | nao_rodou | falhou | nao_rodou | 9badcba8 | - |
| M-15I | 20261126-001606 | GitHub Actions | novo | N4 | N4 | passou | passou | passou | passou | f305dee1 | - |
| M-15I | 20261126-004542 | GitHub Actions | novo | N4 | N4 | passou | passou | passou | passou | 35617a47 | - |
| M-15I | 20261126-110601 | GitHub Actions | novo | N4 | N4 | passou | passou | passou | passou | 77fad232 | - |
<!-- tb_inst_rodadas:fim -->

## 8. Como repetir

Os roteiros do Windows rodam na janela do PowerShell do Eric, nunca de dentro do aplicativo Claude, e recusam rodar com uma corrida do agente em andamento.

- **Linux pelo WSL** (cria a instância da imagem oficial `.wsl`, roda o instalador e a prova, copia a evidência e apaga a instância): `.\ferramentas\instalador_matriz\celula_wsl.ps1 -Id <id da célula> -Imagem <caminho do arquivo .wsl> -Modo novo -Ate <nível>`; roteiro em [celula_wsl.ps1](../../../ferramentas/instalador_matriz/celula_wsl.ps1).
- **Máquina-alvo como está:** `.\ferramentas\instalador_matriz\celula_alvo.ps1 -Ate N4`; roteiro em [celula_alvo.ps1](../../../ferramentas/instalador_matriz/celula_alvo.ps1).
- **GitHub Actions:** na página Actions do repositório, abrir o fluxo "Instalador em máquina nova" e usar "Run workflow" (ele também roda a cada mudança nos arquivos do instalador e uma vez por semana). No fim da execução, baixar o pacote `celula-<id>` de cada célula. Roteiro e fluxo: [celula_actions.py](../../../ferramentas/instalador_matriz/celula_actions.py) e [instalador.yml](../../../.github/workflows/instalador.yml).
- **Trazer a evidência do GitHub para o repositório:** `python ferramentas/instalador_matriz/importar_actions.py celula-CI-UBU.zip celula-CI-WIN.zip celula-M-15.zip celula-M-15I.zip`; ele confere cada rodada (tag, id, nome da pasta) e não regrava uma rodada que já existe.
- **Reescrever este relatório e os blocos do README e do DETALHES-TECNICOS:** `python ferramentas/instalador_matriz/relatorio.py --colar`; para só conferir sem gravar, `python ferramentas/instalador_matriz/relatorio.py --check`.
- **Ler uma rodada:** `python ferramentas/instalador_matriz/ler_celula.py <id da célula>` (a rodada mais recente) ou o caminho de uma pasta de rodada.

### Como ler a primeira execução do fluxo

<!-- ! Alteração de IA - Revisar: (25/11/2026, conserto da revisão do I5/I7) subseção nova com o que olhar na primeira execução do GitHub Actions.
     ! Motivo: no Windows o código de saída do `install.cmd` não é o do instalador (o `install.ps1` não repassa o código e o `install.cmd` termina em `pause`), então ler só o `celula.json` enganaria; e as horas, as versões do Python e a validade dos pacotes confundiriam quem abrisse a evidência sem saber. -->
- **Resultado do instalador:** na primeira execução (commit `9badcba8`) o código de saída do `install.cmd` não era o do instalador, porque o `install.ps1` não repassava o código e o `install.cmd` terminava em `pause`; nessa rodada vale o campo `resultado` do `passos.json` (copiado também para o `celula.json` como `resultado_do_instalador`) e o fim do `instalacao.log`. Desde o conserto de 25/11/2026 os dois lançadores devolvem o código do `install.py`.
- **Rodada que não terminou:** o `celula.json` é gravado no começo da célula com `"terminou": false` e regravado no fim; uma tarefa cortada pelo GitHub sobe só a primeira versão, e a tabela mostra "não terminou" no lugar do nível.
- **Python de cada executor:** a versão está no `estado_inicial.txt`; o `install.py` e a prova pedem o Python 3.10 ou mais novo para abrir.
- **Horas:** as horas do `celula.json` e o nome da pasta das células do GitHub estão em UTC (o `celula.json` traz `"fuso": "UTC"`); as das células do WSL e da `ALVO` estão na hora local.
- **Validade dos pacotes:** os pacotes de evidência ficam 30 dias no GitHub; baixe e importe antes disso.
- **Ações do fluxo:** `actions/checkout@v4` e `actions/upload-artifact@v4` estão presas pela etiqueta da versão, e não pelo identificador do commit, porque o fluxo só lê o repositório e não usa segredo.
- **Modo de cada célula:** na primeira execução a `CI-UBU` rodou no modo `novo` e a `CI-WIN`, a `M-15` e a `M-15I` no modo `como-esta`, porque no Windows e no macOS o instalador ainda seguia os passos antigos. Desde os consertos de 25/11/2026 as quatro rodam no modo `novo`.
- **Preparo:** a `CI-UBU` remove o MySQL da máquina do GitHub antes do instalador. O `celula.json` da rodada traz a chave `preparo`, com cada comando e o código de saída, e a pasta traz o `preparo.log`. A rodada da primeira execução não tem preparo: foi ela que gravou o instalador parando por causa do MySQL.
- **Estado inicial na página:** desde os consertos de 25/11/2026 o resumo de cada célula na página da execução traz também o estado inicial da máquina (o mesmo do `estado_inicial.txt`), e dá para ler a execução pela página antes de baixar o pacote.
