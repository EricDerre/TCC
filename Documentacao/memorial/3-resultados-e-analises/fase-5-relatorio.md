<!-- ! Alteração de IA - Revisar: arquivo novo (16/11/2026): o esqueleto do relatório da Fase 5 (a medição de valor: o agente contra a linha de base manual), com as partes que a seção 6 do plano aprovado lista. Está preenchido o que já se sabe sem número medido: o que a fase pergunta, como ela roda, os pacotes F0 a F2, as decisões 130 a 136, as regras de leitura, as limitações e os desvios do plano. Os blocos `tb_f5_custo_*` foram colados por `avaliar_fase5.py --custo --colar`. As seções do agente, das pessoas e da comparação têm os blocos `tb_f5_agente_*`, `tb_f5_manual_*` e `tb_f5_medicao_*` vazios, nos nomes que a leitura gera, e a palavra "aguarda" no lugar do texto.
     ! Motivo: o plano põe o relatório no pacote F5, em 25/11/2026, depois da corrida 28 e das três sessões. Esta parte foi adiantada enquanto as pessoas fazem as sessões, para o dia 25 ficar só com o que depende dos números. Nenhum número de resultado foi digitado: os do custo vêm dos blocos colados, e os demais entram por `--colar` quando os derivados existirem. Enquanto um bloco estiver vazio, o `--check` da leitura dele acusa diferença neste arquivo: é o esperado, e o conserto é rodar a mesma leitura com `--colar`. -->

# Fase 5: a medição de valor, relatório da fase

<!-- ! Alteração de IA - Revisar: (18/11/2026, leitura da corrida 28) o estado passou a dizer que a corrida 28 rodou e que o lado do agente está lido; as seções 2.3, 2.5, 4, 7 e 8 ganharam o texto da noite, e os seis blocos `tb_f5_agente_*` foram colados por `avaliar_fase5.py --agente --colar`.
     ! Motivo: o relatório dizia que a corrida 28 ainda não tinha acontecido e trazia "aguarda" no lado do agente. Os números do texto novo vêm de `resultados_alvo/fase5/agente.json`, de `fase5_agente/fase4.log` e de `fase5_agente/progresso_medidas.jsonl`, lidos por script; a média da primeira repetição e as faixas por repetição são contas feitas depois de ver os números, fora das regras L1 a L15, e estão marcadas assim onde aparecem. -->
<!-- ! Alteração de IA - Revisar: (18/11/2026, depois das respostas do Eric no quadro) o estado, as seções 2.3, 2.5, 4, 7 e 8 passaram a dizer que a corrida 28 não vale como a medida do agente (decisão 145) e que a noite nova, a corrida 28b, roda a frio (decisão 146).
     ! Motivo: o texto de horas antes dizia que o lado do agente estava lido e que a ficha 84 estava em aberto; o Eric disse no quadro que lançou a noite com o aplicativo Claude aberto e decidiu refazê-la. Os blocos `tb_f5_agente_*` continuam colados na seção 4 como registro do incidente, até a leitura passar a apontar para a pasta da corrida 28b. -->
<!-- ! Alteração de IA - Revisar: (18/11/2026, código da corrida 28b) o estado, as seções 2.3, 2.5, 4, 7, 8 e 10 e a seção nova 11 passaram a separar a corrida 28, guardada como incidente, da corrida 28b, que é a medida do agente: a seção 4 voltou a aguardar a noite nova, com os blocos `tb_f5_agente_*` vazios, e os números da corrida 28 foram para a seção 11, em blocos `tb_f5_incidente28_*`, colados por `avaliar_fase5.py --incidente 28 --colar`.
     ! Motivo: a seção 4 é o lado do agente na comparação, e trazia os números de uma corrida que o Eric decidiu não usar (decisão 145); quem abrisse o relatório leria 30,5 s como o MTTR do agente. O lançador e a leitura passaram a apontar para a pasta nova, e os dois textos precisam dizer a mesma coisa. -->
<!-- ! Alteração de IA - Revisar: (19/11/2026, leitura da corrida 28b) o estado e as seções 2.3, 2.5 e 4 passaram a dizer que a corrida 28b rodou, a frio e com tudo fechado, e que o lado do agente está lido; os sete blocos `tb_f5_agente_*` foram colados por `avaliar_fase5.py --agente --colar`.
     ! Motivo: o relatório dizia que a seção 4 aguardava a corrida 28b. Os números do texto novo vêm de `resultados_alvo/fase5/agente.json`, de `resultados_alvo/fase4/cenarios_v4.json`, de `fase5_agente_b/fase4.log` e de `fase5_agente_b/cenarios.jsonl`, lidos por script; como a noite foi lançada vem da resposta do Eric no quadro em 19/11/2026. -->
<!-- ! Alteração de IA - Revisar: (24/11/2026, leitura das pessoas e comparação) o estado e as seções 1, 2.4, 2.5, 2.6, 5, 6, 7, 8 e 9 passaram a trazer as sessões da linha de base manual e a comparação; os blocos `tb_f5_manual_*` e `tb_f5_medicao_*` foram colados por `avaliar_fase5.py --manual --colar` e `--comparar --colar`.
     ! Motivo: o relatório dizia "aguarda" no lado das pessoas e na comparação. As sessões chegaram por código em 24/11/2026 e a leitura rodou no mesmo dia, depois de o Eric decidir no quadro quais sessões entram (decisões 149 e 150), antes de qualquer tempo ser aberto. Os números do texto vêm de `resultados_alvo/fase5/manual.json` e `medicao.json`, lidos por script; a conta sem a sessão de um integrante é de rascunho, feita depois de ver os números, e está marcada assim onde aparece (decisão 151). Nenhum nome de integrante é escrito com o número dele. -->
<!-- ! Alteração de IA - Revisar: (25/11/2026, fechamento da Fase 5, ficha 96 e decisão 156) o título deixou de dizer "esqueleto", o estado passou a dizer que a fase está concluída, a tabela dos pacotes e a das decisões foram fechadas, e a seção 8 aponta para o anexo do plano aprovado.
     ! Motivo: o Eric fechou a fase em 25/11/2026, depois da revisão geral do projeto; o relatório ainda se chamava esqueleto e dizia que faltava o fechamento. As contagens das baterias vêm da última linha de cada uma, rodadas em 25/11/2026. -->
> Estado em 25/11/2026: **fase concluída** (ficha 96, decisão 156), com os pacotes F0 a F6 feitos. O agente foi medido na corrida 28b, em 18/11/2026, com o aplicativo Claude e o VS Code fechados e a frio (decisões 145 e 146); a corrida 28, da mesma data, não vale como medida, e os números dela estão na seção 11, como registro do incidente. As sessões da linha de base manual chegaram em 24/11/2026, e a leitura pelas regras do plano deu o agente mais rápido que as pessoas nos dez cenários (seção 6). O veredito do Task Success depende da sessão de um integrante só, e é lido com essa ressalva (decisão 151). Os desvios do plano (seção 8) estão também no anexo do [plano aprovado](../../../claude-memoria/plano-aprovado-fase-5.md). Ficam para o pacote Q8 da Pós-Fase 4, fora da fase: o Word do documento do TCC, o corte do resumo e as frases da Fase 4 que ainda dão corridas como pendentes no documento.

Plano da fase: [plano-aprovado-fase-5.md](../../../claude-memoria/plano-aprovado-fase-5.md), aprovado em 16/11/2026 (decisão 133). O texto do plano não é reescrito: o que desviou dele está na seção 8.

## 1. O que a fase pergunta e o que ela respondeu

A Fase 5 responde à pergunta do quinto objetivo específico do projeto: **o agente repara mais rápido que uma pessoa, e resolve tantos cenários quanto ela?**

São duas medidas, definidas no projeto de pesquisa (seção 3.4):

- **MTTR (tempo médio de reparo).** O tempo que vai da detecção da falha pelo agente até a correção validada na reexecução.
- **Task Success (sucesso da tarefa).** A parcela dos cenários de falha em que o fluxo foi restaurado e o roteiro concluiu sem erro.

A linha de base são os mesmos cenários resolvidos por pessoas, com o tempo cronometrado. A comparação entre os dois tempos é o resultado central da avaliação do trabalho.

**O que a fase respondeu.** A resposta sai da leitura que põe os dois lados na mesma tabela (`avaliar_fase5.py --comparar`), e a frase dela é escrita pelo código, pelas regras L9 e L11 (seção 3), para ninguém redigir a conclusão depois de ver os números. A leitura rodou em 24/11/2026 (seção 6):

- **No tempo, sim: o agente reparou mais rápido que as pessoas.** O MTTR médio do agente foi de 66,3 s, contra 219,7 s das pessoas. A diferença média por cenário foi de 153,4 s (de 109,0 a 196,1 s), o agente foi mais rápido nos dez cenários, e o teste dos sinais deu p = 0,0020. É o resultado central da fase.
- **No Task Success, sim pelas regras, com uma ressalva.** O agente resolveu 49 de 50 execuções, e as pessoas, 14 de 30 tentativas; a parcela do agente foi maior nos dez cenários (p = 0,0020). Esse veredito depende da sessão de um integrante só, que não corrigiu nenhum cenário: sem ela, numa conta feita depois de ver os números, o Task Success fica sem veredito (seção 6, decisão 151).

A expectativa do projeto de pesquisa (seção 4) era que o agente reduzisse o MTTR "significativamente" contra a correção manual dos mesmos cenários. Nos dez cenários medidos o tempo médio do agente foi cerca de um terço do das pessoas (razão de 3,31 entre as médias).

## 2. Como a fase roda

### 2.1 Os dez cenários

São os dez cenários de `cenarios_fase4.CENARIOS_DO_ENSAIO` (ficha 36, decisão 79): seis de contrato, na página que consome a CobaiaAPI, um por modo de falha, e quatro de localizador, no site legado, um por roteiro. A falha é armada pelas mesmas funções dos dois lados.

O que conta como corrigido (ficha 35, decisão 79):

- **Localizador.** O roteiro concluído sem erro com um localizador novo. O cronômetro vai até a reexecução validada, descontada a restauração do banco.
- **Contrato.** O agente não conserta a API: ele diagnostica. O cronômetro para no diagnóstico conferido em código, e o Task Success é a causa e o campo certos. A pessoa escolhe a causa na mesma lista fechada de 23 causas.

Os dois tipos não medem a mesma coisa e são lidos em separado.

### 2.2 O agente que é medido

É o agente das corridas 18d e 21d: o modelo `qwen2.5:7b`, três verbetes entregues ao modelo, os limiares de `limiares.json`, a biblioteca de produção, o prompt do diagnóstico congelado e a busca com os sinais contra a referência. Nada da Pós-Fase 4 mudou o que o agente mede. Antes de rodar, o lançador confere que o agente de hoje é o da corrida 21d (`avaliar_fase5.py --antes`): a biblioteca, o prompt fixo, o índice da busca, o número de verbetes, os limiares e a versão do navegador. Se um deles diferir, a noite não roda.

### 2.3 A noite do agente (a corrida 28 e a noite refeita, corrida 28b)

Os dez cenários com cinco repetições, 50 execuções, com o banco restaurado e conferido por hash no começo de cada repetição. O lançador é `Programacao/AgenteCore/experimentos/rodar_fase5.ps1`, rodado pelo Eric da janela dele, com o aplicativo Claude e o VS Code fechados. As etapas, parando na primeira que falhar:

1. Espera a memória livre e confere que não há modelo residente no Ollama.
2. Confere que o agente de hoje é o da corrida 21d.
3. Roda a ponte de versão, se a versão do Ollama no ar ainda não tiver uma.
4. Roda a corrida. Na corrida 28 foi uma chamada só (`rodar_fase4.ps1 -Modo cenarios -Saida fase5_agente -Repeticoes 5 -Nome cenarios_fase5`). Na corrida 28b é uma chamada por repetição, na pasta nova (`-Saida fase5_agente_b -Repeticoes N -Nome cenarios_fase5b`, com N de 1 a 5), e antes de cada uma o lançador tira o modelo da memória (`ollama stop`), confere que o `ollama ps` ficou vazio e que a versão do Ollama é a das execuções já gravadas. Com as 50 execuções já gravadas, a corrida não é chamada de novo.
5. Grava a leitura por cenário (`avaliar_fase5.py --agente`).
6. Regera o painel e roda as baterias dele.

A primeira noite completa é a que vale: nenhuma corrida é repetida para melhorar o número, e relançar só retoma o que faltou.

O tempo de máquina estimado para a noite, pelos registros da corrida 21d:

<!-- tabela:tb_f5_custo_resumo -->
| Execuções da noite | Segundos por execução na corrida 21d (média) | Horas pela média das execuções | Segundos do executor na corrida 21d | Horas pelo executor inteiro | Segundos fora do executor na corrida 21d (bateria de testes e leitura) | Ponte, se o Ollama mudou de versão (min) | Noite sem a ponte (min) | Noite com a ponte (min) |
|---|---|---|---|---|---|---|---|---|
| 50 (10 cenários x 5 repetições) | 76,7 | 1,07 | 808 | 1,12 | 26 | 34 a 42 | 68 | 110 |
<!-- /tabela:tb_f5_custo_resumo -->

As três últimas pontes de versão, de onde sai a duração da ponte:

<!-- tabela:tb_f5_custo_pontes -->
| Ponte (pasta em `resultados_alvo/`) | Versão do Ollama | Data | Duração (min) |
|---|---|---|---|
| `fase3b_ponte_04014` | 0.40.14 | 2026-11-03 | 42 |
| `fase3b_ponte_04015` | 0.40.15 | 2026-11-11 | 34 |
| `fase3b_ponte_04016` | 0.40.16 | 2026-11-16 | 37 |
<!-- /tabela:tb_f5_custo_pontes -->

**Como a noite rodou.** Em 18/11/2026, das 18:46 às 19:17, pelo lançador: 50 de 50 execuções, 1832 s de executor e 00h31 de ponta a ponta (`fase5_agente/fase4.log`), com a versão 0.40.16 do Ollama do começo ao fim. A ponte não rodou, porque essa versão já tinha a dela, registrada em 16/11/2026 (terceira linha da tabela acima). A bateria `testar_fase4.py` rodou antes da corrida, e a leitura da corrida 21 não foi tocada.

O que fugiu do previsto foi a duração: 31 minutos, e não os 68 da estimativa. A estimativa multiplicou por cinco o tempo da corrida 21d, que rodou cada cenário uma vez. Na corrida 28 o Ollama guardou o prompt já lido de cada cenário e o reaproveitou nas repetições seguintes. O registro da barra de progresso (`fase5_agente/progresso_medidas.jsonl`) mostra: na repetição 1, a leitura do prompt (`medido.prefill_s`) somou 462,4 s nas dez inferências, com 1505 dos 11966 tokens de entrada vindos do que estava guardado (`medido.tokens_em_cache`); em cada uma das repetições 2 a 5, somou de 43,8 a 45,3 s, com 10975 dos 11966 tokens guardados. A geração da resposta não mudou: de 133,3 a 142,0 s por repetição. Pelo log, a repetição 1 levou 11 minutos e 38 segundos, e cada uma das outras quatro, cerca de 4 minutos e 36 segundos. O que isso faz com o MTTR está na seção 11.

**O que o Eric decidiu sobre a noite, em 18/11/2026.** Perguntado no quadro, ele disse que lançou a corrida com o aplicativo Claude aberto, sem sessão trabalhando; o plano pede o aplicativo Claude e o VS Code fechados. O log mostra 8,9 GB de RAM livre no começo, acima dos 7,0 GB que o lançador pede, e a recomendação era manter a noite com a limitação declarada. Ele decidiu refazer: a corrida 28 fica registrada como incidente e não entra na comparação (ficha 85, decisão 145). A noite nova, a corrida 28b, roda em pasta nova, com tudo fechado, e a frio: uma repetição por vez, com o modelo descarregado do Ollama entre elas, para o prompt ser lido de novo em cada repetição (ficha 86, decisão 146). Antes dela, uma sondagem curta pela janela do Eric confirma que descarregar o modelo apaga o prompt guardado.

**Como a noite nova roda (corrida 28b).** O executor do ensaio não muda. Lido o código dele (`executar_fase4.py`, modo `cenarios`): chamado com `--repeticoes N` na mesma pasta, ele pula as execuções que já estão em `cenarios.jsonl` e roda só as da repetição que falta; regrava `condicoes_fase4.json` a cada chamada, com o número de repetições daquela chamada; escreve uma linha FIM por chamada, com as execuções somadas até ali; descarrega o modelo no fim de cada chamada; e para, antes de carregar o modelo, se os diagnósticos já gravados vieram de outra versão do Ollama (decisão 44). Por isso o lançador `rodar_fase5.ps1` chama o `rodar_fase4.ps1` cinco vezes, uma por repetição, e relançar retoma na primeira repetição incompleta. Antes da noite, a sondagem `rodar_sondagem_frio.ps1` faz duas inferências do mesmo cenário, pelo mesmo caminho, com o modelo descarregado entre elas, e grava numa pasta própria (`resultados_alvo/fase5_sondagem_frio_<data>_<hora>`); `avaliar_fase5.py --sondagem` diz se ela passou, isto é, se nenhuma das duas inferências reaproveitou token do que o Ollama tinha guardado. Sem a última sondagem ter passado, na versão do Ollama que está no ar, o lançador não começa a corrida. Depois da noite, a leitura confere repetição por repetição que o prompt foi lido de novo (seção 4), e só grava em `resultados_alvo/fase5` a noite completa e a frio.

**Como a noite nova rodou (corrida 28b).** Em 18/11/2026. A sondagem do frio, às 21:27, passou (`resultados_alvo/fase5_sondagem_frio_20261118_212709`). A noite foi das 21:33 às 22:38, em cinco chamadas, uma por repetição: de 730 a 740 s de executor por repetição, 3671 s nas cinco (`fase5_agente_b/fase4.log`), com 8,6 a 9,1 GB de RAM livre no começo de cada chamada e a versão 0.40.16 do Ollama do começo ao fim. A ponte não rodou. Perguntado no quadro em 19/11/2026, o Eric disse que lançou a sondagem e a noite da janela dele, com o aplicativo Claude e o VS Code fechados do começo ao fim ("Sim, tudo fechado"). Nada fugiu do previsto: a estimativa era de cerca de 70 minutos, e a noite levou cerca de 65.

### 2.4 As sessões das pessoas

Três integrantes do grupo, cada um nos dez cenários, numa ordem sorteada com semente fixa, com limite de 10 minutos por cenário (decisões 130 e 131). Desde a decisão 136, a sessão é feita por uma página publicada, uma por integrante, sem instalar nada: a falha de cada cenário é armada antes, na máquina-alvo, e a página entrega o registro capturado (a chamada à API, a foto da tela e o HTML sem script). A página cronometra, guarda a sessão e, no localizador, confere o seletor na hora contra a fotografia do HTML. Depois da sessão, os dados são trazidos por `linha_de_base_manual.py importar`, que roda o roteiro de verdade com o seletor entregue, e a planilha é preenchida por `linha_de_base_manual.py planilha`.

Antes da sessão cada integrante recebe o [tutorial](../5-metodo-e-ferramental/tutorial-do-integrante.md) (decisão 135) e faz um treino sem cronômetro, com um cenário de contrato e um exercício de seletor de fora dos dez. O [protocolo](../5-metodo-e-ferramental/protocolo-linha-de-base-manual.md) está na versão 3; a forma presencial, com facilitador, ficou como reserva.

**Como as sessões aconteceram.** As três páginas foram compartilhadas por link, e as sessões chegaram por código em 24/11/2026: quatro códigos para três páginas, guardados como vieram em `resultados_alvo/fase5_manual/recebido/`, com o índice em `recebido.json`. O banco das páginas ficou vazio, porque quem entra só pelo link não grava nele. As três sessões que entram na leitura são de 18/11/2026 (página 2), 23/11/2026 (página 1) e 24/11/2026 (página 3), feitas por integrantes do grupo, cada um no seu aparelho, sem facilitador ao lado. Quem fez cada uma foi perguntado ao Eric no quadro antes do registro, e os nomes não são gravados com a página.

O que fugiu do protocolo, e o que o Eric decidiu no quadro antes de qualquer tempo ser aberto:

- **Duas sessões na página 1, de duas pessoas.** Quem fez a primeira respondeu no perfil que já tinha lido a lista dos cenários; um quarto integrante do grupo fez a página depois, como substituto, sem ver a sessão da primeira nem conversar com ela. Entra só a sessão do substituto, que é o que o protocolo diz para quem já leu a lista quando há substituto (ficha 89, decisão 149). A outra ficou guardada como recebida, sem ser importada e sem os tempos abertos.
- **A sessão da página 2.** Quem a fez também respondeu que já tinha lido a lista, e o treino veio sem o exercício de seletor. Não havia substituto, e a sessão entra com as duas coisas declaradas (ficha 90, decisão 150).
- **Nenhuma linha anulada.** As três sessões que entram não trazem aviso de que algo de fora atrapalhou um cenário (regra L14, decisão 137).

O perfil dos três, sem o nome (`resultados_alvo/fase5_manual/participantes.json`): o integrante 1 tem seis meses de programação para a web, já tinha usado as ferramentas do desenvolvedor e não tinha lido a lista; o integrante 2 respondeu "não muito tempo" de prática, nunca tinha usado as ferramentas e já tinha lido a lista; o integrante 3 tem de um a dois meses de programação para a web, nunca tinha usado as ferramentas e não tinha lido a lista. Nenhum dos três conhece o código das cobaias.

A importação rodou em 24/11/2026 com as cobaias no ar (`linha_de_base_manual.py importar`): o roteiro de verdade foi rodado com os seletores que passaram na página e não acusou diferença, e a planilha saiu com as 30 linhas preenchidas e nenhum aviso (`linha_de_base_manual.py planilha`).

### 2.5 Os pacotes

| Pacote | O que é | Estado em 25/11/2026 |
|---|---|---|
| F0 | O plano, as fichas 72 a 75 e a aprovação | feito em 16/11/2026 |
| F1 | A leitura (`avaliar_fase5.py`), os testes dela (`testar_fase5.py`) e o lançador da noite (`rodar_fase5.ps1`) | feito em 16/11/2026 |
| F2 | O protocolo da sessão, o ajudante (`linha_de_base_manual.py`), o tutorial e as páginas da sessão (`sessao_pelo_artefato.py`), com os testes (`testar_linha_de_base.py`) | feito em 16/11/2026 |
| F3 | A noite medida | a corrida 28 rodou em 18/11/2026 e não vale como medida (decisão 145); a corrida 28b, a frio (decisão 146), rodou em 18/11/2026 com tudo fechado e foi lida em 19/11/2026: é a medida do agente |
| F4 | As três sessões da linha de base manual | feitas de 18 a 24/11/2026, pela página, e importadas em 24/11/2026 (decisões 149 e 150) |
| F5 | A leitura dos dois lados, o painel, este relatório, o roadmap, o README e a figura | a leitura das pessoas e a comparação rodaram em 24/11/2026, com este relatório, o roadmap e o painel; a descoberta no README com a figura, a ressalva na aba do painel e a tabela por script da conta sem cada integrante entraram no mesmo dia (decisão 151) |
| F6 | As seções da Fase 5 no documento do TCC | feito em 24/11/2026 e conferido em 25/11/2026 (seção 6.8 nova, resumo, abstract, 5.1, 5.7, Discussão, Análise aprofundada, Conclusão e glossário); o Word sai com o pacote Q8 |

### 2.6 As decisões da fase

| Decisão | O que ficou decidido |
|---|---|
| 130 | A linha de base manual é feita por três integrantes do grupo que não leram a lista dos cenários (ficha 72) |
| 131 | O protocolo da sessão passa à versão 2: a ferramenta grava a hora de cada evento e preenche a planilha, há um treino sem cronômetro, e a pessoa recebe a explicação de uma linha de cada causa e responde as perguntas de perfil (ficha 73) |
| 132 | Na comparação, a unidade é o cenário: o intervalo sai da reamostragem dos cenários, e o veredito, do teste dos sinais; por tipo de cenário não há veredito (ficha 74) |
| 133 | O plano da Fase 5 está aprovado como foi escrito (ficha 75) |
| 134 | A folha do integrante leva as 23 explicações de uma linha como foram escritas no pacote F2, e o Apêndice A do documento do TCC ganha a mesma coluna (ficha 76) |
| 135 | Os integrantes recebem um tutorial antes da sessão |
| 136 | As sessões são feitas por uma página publicada, uma por integrante, com o material de cada cenário capturado antes |
| 137 | A página pergunta, no fim de cada cenário, se algo de fora atrapalhou, e a anulação da linha é decidida na importação, pelo motivo e antes de qualquer tempo (ficha 77) |
| 144 | O tempo do agente na corrida 28 em duas leituras lado a lado (ficha 84); perdeu o efeito no mesmo dia, com as duas seguintes |
| 145 | A corrida 28 não vale como a medida do agente, e a noite é refeita com o aplicativo Claude e o VS Code fechados (ficha 85) |
| 146 | A noite refeita, a corrida 28b, roda a frio: uma repetição por vez, com o modelo descarregado entre elas (ficha 86) |
| 149 | Na página 1, onde vieram duas sessões, entra só a do substituto; a outra fica guardada sem ser importada (ficha 89) |
| 150 | A sessão da página 2 entra, com duas coisas declaradas: a pessoa já tinha lido a lista e não fez o treino de seletor (ficha 90) |
| 151 | A leitura fica como as regras deram, e o veredito do Task Success é declarado como dependente da sessão de um integrante; o resultado central é o do tempo (ficha 91) |
| 154 | Os nomes dos integrantes da linha de base não ficam em arquivo do repositório |
| 156 | A Fase 5 está concluída em 25/11/2026; o Word, o corte do resumo e as frases da Fase 4 no documento do TCC ficam para o pacote Q8 (ficha 96) |

O texto completo de cada uma está em [decisoes.md](../1-decisoes-e-historico/decisoes.md).

## 3. As regras de leitura, fixadas antes de qualquer medida

As regras L1 a L15 estão na seção 5 do plano e foram escritas em código (`avaliar_fase5.py`) e testadas com dados de mentira (`testar_fase5.py`) antes da noite do agente e da primeira sessão. O resumo delas:

- **O que é uma medida (L1).** Do agente, cada execução; das pessoas, cada tentativa. Uma pessoa não repete cenário.
- **A unidade é o cenário (L2).** As repetições do agente no mesmo cenário não são independentes, e os integrantes resolvem a mesma falha. Todo intervalo do tempo e todo veredito tratam o cenário como a unidade.
- **O tempo de cada lado (L3 e L4).** Por cenário, a média de quem chegou ao fim do cronômetro, com o mínimo e o máximo. No geral e por tipo, a média das médias dos cenários.
- **Task Success (L5).** A parcela de cada lado com o intervalo de Wilson de 95% e, ao lado, em quantos cenários todas as medidas acertaram.
- **Quem não chega ao fim (L6).** Fica fora da média do tempo e dentro do Task Success. Uma segunda conta, declarada como piso, põe o limite de tempo no lugar, dos dois lados.
- **Os intervalos (L7).** O do tempo médio sai da reamostragem dos cenários, com semente fixa, sorteando dentro de cada tipo. Por cenário não há intervalo.
- **A comparação do tempo (L8).** Por cenário, a diferença e a razão. No geral, a média das diferenças com o intervalo, a razão entre as médias e o teste exato dos sinais sobre os cenários (DIXON; MOOD, 1946), que é a conta binomial do teste de McNemar exato que o projeto já usa (`avaliar.mcnemar_exato`). Diferença menor que a folga do cronômetro das pessoas conta como empate e sai do teste.
- **O que conta como diferença (L9).** A leitura só afirma que um lado repara mais rápido quando o intervalo de 95% da diferença média não contém zero e o teste dos sinais dá p abaixo do corte. Com o zero dentro do intervalo, a diferença está dentro do ruído. Com o intervalo sem o zero e o teste sem chegar ao corte, a média pende para um lado e a leitura não dá veredito.
- **Por tipo de cenário, sem veredito (L10).** Os cenários de cada tipo são poucos para o teste separar os lados.
- **A comparação do Task Success (L11).** Os dois números com Wilson e o teste dos sinais sobre os cenários em que as duas parcelas diferem; com poucos cenários diferentes, a leitura diz que não há veredito.
- **O que é só descrição (L12 e L13).** As faixas de cada lado, o tempo das pessoas pela posição na ordem, o tempo total do agente e o tempo só das medidas com Task Success.
- **O que anula uma medida (L14).** Só uma falha do protocolo anotada na hora. Do lado do agente, nenhuma execução é anulada.
- **Nada é escolhido depois (L15).** Uma conta pensada depois de ver os números entra neste relatório marcada como exploratória.

As constantes de cada regra (a folga do empate, o limite de tempo, o corte do teste, as reamostras e a semente) saem gravadas em `medicao.json`, no campo `regras`, e são coladas na seção 6.

## 4. O agente (corrida 28b)

O lado do agente na comparação é a corrida 28b: a noite refeita em 18/11/2026 com o aplicativo Claude e o VS Code fechados e a frio (decisões 145 e 146), gravada em `resultados_alvo/fase5_agente_b`. Os blocos abaixo foram colados em 19/11/2026 por `avaliar_fase5.py --agente --colar`, e `avaliar_fase5.py --agente --check` confere que batem com os registros. Os números da corrida 28, que não vale como a medida do agente, estão na seção 11.

O agente no geral:

<!-- tabela:tb_f5_agente_resumo -->
| Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Cenários com todas certas | Com fim de cronômetro | Sem fim | MTTR médio (s) | Reamostragem 95% (s) | Segunda conta, com 600 s para quem não chegou ao fim (s) | Reamostragem 95% da segunda conta (s) | Só com Task Success (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 49 | 98,0 | 89,5 a 99,6 | 9 de 10 | 49 | 1 | 66,3 | 60,9 a 71,5 | 76,7 | 61,3 a 101,7 | 66,3 |
<!-- /tabela:tb_f5_agente_resumo -->

Por tipo de cenário:

<!-- tabela:tb_f5_agente_por_tipo -->
| Tipo | Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Cenários com todas certas | Com fim de cronômetro | Sem fim | MTTR médio (s) | Reamostragem 95% (s) | Segunda conta, com 600 s para quem não chegou ao fim (s) | Reamostragem 95% da segunda conta (s) | Só com Task Success (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| contrato | 30 | 29 | 96,7 | 83,3 a 99,4 | 5 de 6 | 29 | 1 | 73,0 | 67,7 a 78,4 | 90,2 | 67,7 a 129,7 | 73,0 |
| localizador | 20 | 20 | 100,0 | 83,9 a 100,0 | 4 de 4 | 20 | 0 | 56,4 | 44,5 a 64,2 | 56,4 | 44,5 a 64,2 | 56,4 |
<!-- /tabela:tb_f5_agente_por_tipo -->

Cenário a cenário:

<!-- tabela:tb_f5_agente_por_cenario -->
| Cenário | Tipo | Execuções | Task Success | Com fim | MTTR médio (s) | Mínimo (s) | Máximo (s) | Segunda conta (s) | Só com Task Success (s) | Rótulo do diagnóstico em cada repetição | Tempo total da execução (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | 5 | 4 | 4 | 81,7 | 78,7 | 85,9 | 185,3 | 81,7 | `resposta_truncada`, `resposta_truncada`, `resposta_truncada`, `resposta_truncada`, `resposta_truncada` | 80,7 |
| `contrato-field_missing` | contrato | 5 | 5 | 5 | 67,0 | 66,4 | 67,8 | 67,0 | 67,0 | `campo_ausente`, `campo_ausente`, `campo_ausente`, `campo_ausente`, `campo_ausente` | 67,5 |
| `contrato-field_renamed` | contrato | 5 | 5 | 5 | 65,3 | 64,9 | 65,9 | 65,3 | 65,3 | `campo_renomeado`, `campo_renomeado`, `campo_renomeado`, `campo_renomeado`, `campo_renomeado` | 65,7 |
| `contrato-type_drift` | contrato | 5 | 5 | 5 | 66,7 | 66,0 | 67,6 | 66,7 | 66,7 | `tipo_divergente`, `tipo_divergente`, `tipo_divergente`, `tipo_divergente`, `tipo_divergente` | 67,1 |
| `contrato-escala_ou_unidade_errada` | contrato | 5 | 5 | 5 | 80,4 | 78,8 | 82,9 | 80,4 | 80,4 | `escala_ou_unidade_errada`, `escala_ou_unidade_errada`, `escala_ou_unidade_errada`, `escala_ou_unidade_errada`, `escala_ou_unidade_errada` | 80,8 |
| `contrato-error_500` | contrato | 5 | 5 | 5 | 76,6 | 75,0 | 77,3 | 76,6 | 76,6 | `erro_interno_do_servidor`, `erro_interno_do_servidor`, `erro_interno_do_servidor`, `erro_interno_do_servidor`, `erro_interno_do_servidor` | 76,9 |
| `localizador-front-busca` | localizador | 5 | 5 | 5 | 65,4 | 64,9 | 65,8 | 65,4 | 65,4 | `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado` | 71,3 |
| `localizador-front-admin-login` | localizador | 5 | 5 | 5 | 39,0 | 38,5 | 40,3 | 39,0 | 39,0 | `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado` | 44,7 |
| `localizador-front-admin-produtos` | localizador | 5 | 5 | 5 | 60,3 | 60,1 | 60,6 | 60,3 | 60,3 | `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado` | 66,7 |
| `localizador-front-cliente-reserva` | localizador | 5 | 5 | 5 | 61,0 | 60,0 | 63,1 | 61,0 | 61,0 | `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado` | 68,3 |
<!-- /tabela:tb_f5_agente_por_cenario -->

A noite conferida (as execuções gravadas, se a noite está completa e se foi a frio, a versão do Ollama e a do navegador, o hash do banco e a linha de fim no log):

<!-- tabela:tb_f5_agente_noite -->
| Execuções gravadas | Esperadas | Noite completa | Noite a frio | Versões do Ollama nos diagnósticos | Versões do navegador | Hash do banco no começo das repetições | Linha FIM no log | Tempo total das execuções (s) | Tempo total médio por cenário (s) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 50 | sim | sim | 0.40.16 | 156.0.8078.4 | 9fe5e7cb64288c9d | sim | 3448,6 | 69,0 |
<!-- /tabela:tb_f5_agente_noite -->

A conferência de que cada repetição rodou a frio. A repetição vale a frio quando a primeira inferência dela não reaproveitou nenhum token do que o Ollama tinha guardado e, no máximo, metade dos tokens de entrada da repetição veio guardada (`medido.tokens_em_cache` em `progresso_medidas.jsonl`). O limite foi fixado em 18/11/2026, antes da noite, com os registros da corrida 28 (seção 11). É conferência de validade da noite, e não regra de comparação: a leitura só grava em `resultados_alvo/fase5` a noite em que as cinco repetições passam.

<!-- tabela:tb_f5_agente_frio -->
| Repetição | Inferências | Tokens de entrada | Tokens que vieram do que o Ollama tinha guardado | Parcela guardada (%) | Guardados na primeira inferência | Leitura do prompt, somada (s) | Carga do modelo, somada (s) | A frio |
|---|---|---|---|---|---|---|---|---|
| 1 | 10 | 11966 | 1505 | 12,6 | 0 | 474,2 | 6,9 | sim |
| 2 | 10 | 11966 | 1505 | 12,6 | 0 | 473,8 | 6,4 | sim |
| 3 | 10 | 11966 | 1505 | 12,6 | 0 | 468,8 | 6,1 | sim |
| 4 | 10 | 11966 | 1505 | 12,6 | 0 | 471,0 | 6,1 | sim |
| 5 | 10 | 11966 | 1505 | 12,6 | 0 | 474,4 | 6,4 | sim |
<!-- /tabela:tb_f5_agente_frio -->

O agente medido contra o da corrida 21d:

<!-- tabela:tb_f5_agente_identidade -->
| Item | Na corrida | Na corrida 21d | Igual | Para a noite se diferir |
|---|---|---|---|---|
| biblioteca de produção (hash) | `95af35290860` | `95af35290860` | sim | sim |
| prompt fixo do diagnóstico (hash) | `2e42cf9c31826941` | `2e42cf9c31826941` | sim | sim |
| índice da busca (hash) | `11e763ba9cb1fdf4` | `11e763ba9cb1fdf4` | sim | sim |
| k (verbetes entregues ao modelo) | `3` | `3` | sim | sim |
| limiares do selo | `baixo até 0,8318, alto a partir de 0,9898, k 3 (conteúdo 13a02982)` | `baixo até 0,8318, alto a partir de 0,9898, k 3 (conteúdo 13a02982)` | sim | sim |
| versão do navegador | `156.0.8078.4` | `156.0.8078.4` | sim | sim |
| modelo | `qwen2.5:7b` | `qwen2.5:7b` | sim | não |
| alternativas por posição (top_logprobs) | `20` | `20` | sim | não |
| teto de tokens da resposta | `600` | `600` | sim | não |
| Playwright | `1.64.1` | `1.64.1` | sim | não |
| versão do código do caso ao vivo | `5` | `4` | não | não |
| busca com os sinais contra a referência | `True` | `True` | sim | não |
<!-- /tabela:tb_f5_agente_identidade -->

As execuções que não chegaram ao resultado:

<!-- tabela:tb_f5_agente_sem_sucesso -->
| Cenário | Repetição | Tipo | Detectou | Rótulo do diagnóstico | Causa esperada | Falha da cura | MTTR (s) | Segundos |
|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | 1 | contrato | sim | `resposta_truncada` | `resposta_truncada` | n/d | n/d | 76,1 |
<!-- /tabela:tb_f5_agente_sem_sucesso -->

**Leitura do lado do agente.** A noite vale: 50 de 50 execuções, uma versão só do Ollama e uma do navegador, o banco com o mesmo hash no começo das cinco repetições, a linha FIM no log, o agente igual ao da corrida 21d nos seis itens que parariam a noite, e a frio nas cinco repetições. Em cada uma, 1505 dos 11966 tokens de entrada vieram do que o Ollama tinha guardado (12,6%), nenhum deles na primeira inferência, e a leitura do prompt somou de 468,8 a 474,4 s. O agente teve Task Success em 49 de 50 execuções (98,0%, intervalo de Wilson de 89,5% a 99,6%), com 9 dos 10 cenários certos nas cinco repetições, e MTTR médio de 66,3 s (de 60,9 a 71,5 s): 73,0 s no contrato e 56,4 s no localizador. A segunda conta, com 600 s no lugar da execução que não fechou o cronômetro, dá 76,7 s (de 61,3 a 101,7 s). Dentro de cada cenário as cinco repetições ficaram próximas: a maior distância entre o mínimo e o máximo é a de `contrato-malformed_json`, de 78,7 a 85,9 s.

**A execução sem Task Success.** De novo a primeira de `contrato-malformed_json`, a mesma da corrida 28 (seção 11). O rótulo saiu certo, mas a resposta do modelo veio sem a linha FONTE (`conferencia.linhas.FONTE` falso em `fase5_agente_b/cenarios.jsonl`); o diagnóstico não foi conferido em código e o cronômetro não fechou. Nas outras quatro repetições o cenário passou. Nas duas corridas ela é a primeira inferência da noite; por que só ela sai sem a linha não foi apurado.

**Contra a corrida 21d.** Com uma repetição e a versão 0.40.14 do Ollama, a corrida 21d tinha dado Task Success em 10 de 10 e MTTR médio de 74,0 s (`resultados_alvo/fase4/cenarios_v4.json`, campo `geral.mttr_media_s`). A corrida 28b ficou cerca de 8 s abaixo, com o mesmo agente; a 21d não gravou o tempo de cada etapa da inferência, e não dá para dizer de onde vem a diferença.

## 5. As pessoas (linha de base manual)

**Aguarda as três sessões.** Os blocos abaixo são colados por `avaliar_fase5.py --manual --colar` depois que a planilha tiver as 30 linhas. A leitura não mostra número nenhum antes de a planilha estar completa e conferida.

As pessoas no geral:

<!-- tabela:tb_f5_manual_resumo -->
| Tentativas | Task Success | Task Success (%) | Wilson 95% (%) | Cenários com todas certas | Com fim de cronômetro | Sem fim | Tempo médio (s) | Reamostragem 95% (s) | Segunda conta, com 600 s para quem não chegou ao fim (s) | Reamostragem 95% da segunda conta (s) | Só com Task Success (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 30 | 14 | 46,7 | 30,2 a 63,9 | 0 de 10 | 24 | 6 | 219,7 | 172,3 a 264,7 | 289,8 | 241,0 a 339,6 | 246,0 |
<!-- /tabela:tb_f5_manual_resumo -->

Por tipo de cenário:

<!-- tabela:tb_f5_manual_por_tipo -->
| Tipo | Tentativas | Task Success | Task Success (%) | Wilson 95% (%) | Cenários com todas certas | Com fim de cronômetro | Sem fim | Tempo médio (s) | Reamostragem 95% (s) | Segunda conta, com 600 s para quem não chegou ao fim (s) | Reamostragem 95% da segunda conta (s) | Só com Task Success (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| contrato | 18 | 6 | 33,3 | 16,3 a 56,3 | 0 de 6 | 16 | 2 | 174,8 | 125,7 a 228,6 | 222,2 | 153,4 a 291,0 | 213,2 |
| localizador | 12 | 8 | 66,7 | 39,1 a 86,2 | 0 de 4 | 8 | 4 | 287,0 | 183,0 a 359,3 | 391,4 | 322,0 a 439,6 | 287,0 |
<!-- /tabela:tb_f5_manual_por_tipo -->

Cenário a cenário:

<!-- tabela:tb_f5_manual_por_cenario -->
| Cenário | Tipo | Tentativas | Corrigidas | Com fim | Tempo médio (s) | Mínimo (s) | Máximo (s) | Segunda conta (s) | Só as corrigidas (s) |
|---|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | 3 | 1 | 3 | 109,6 | 50,2 | 151,5 | 109,6 | 127,2 |
| `contrato-field_missing` | contrato | 3 | 1 | 2 | 111,3 | 95,0 | 127,7 | 274,2 | 95,0 |
| `contrato-field_renamed` | contrato | 3 | 2 | 2 | 236,5 | 211,5 | 261,5 | 357,7 | 236,5 |
| `contrato-type_drift` | contrato | 3 | 0 | 3 | 189,0 | 51,4 | 260,6 | 189,0 | n/d |
| `contrato-escala_ou_unidade_errada` | contrato | 3 | 1 | 3 | 280,6 | 35,2 | 454,5 | 280,6 | 454,5 |
| `contrato-error_500` | contrato | 3 | 1 | 3 | 121,8 | 37,8 | 174,9 | 121,8 | 152,6 |
| `localizador-front-busca` | localizador | 3 | 2 | 2 | 385,3 | 289,5 | 481,0 | 456,8 | 385,3 |
| `localizador-front-admin-login` | localizador | 3 | 2 | 2 | 150,1 | 144,6 | 155,7 | 300,1 | 150,1 |
| `localizador-front-admin-produtos` | localizador | 3 | 2 | 2 | 331,2 | 258,7 | 403,7 | 420,8 | 331,2 |
| `localizador-front-cliente-reserva` | localizador | 3 | 2 | 2 | 281,6 | 167,7 | 395,4 | 387,7 | 281,6 |
<!-- /tabela:tb_f5_manual_por_cenario -->

Pela posição na ordem de cada integrante (só descrição):

<!-- tabela:tb_f5_manual_por_posicao -->
| Posição na ordem do integrante | Tentativas | Corrigidas | Com fim | Tempo médio (s) |
|---|---|---|---|---|
| 1 | 3 | 2 | 3 | 250,3 |
| 2 | 3 | 0 | 3 | 152,6 |
| 3 | 3 | 1 | 2 | 163,8 |
| 4 | 3 | 2 | 2 | 275,5 |
| 5 | 3 | 2 | 3 | 91,6 |
| 6 | 3 | 1 | 2 | 239,7 |
| 7 | 3 | 1 | 2 | 332,1 |
| 8 | 3 | 1 | 2 | 141,7 |
| 9 | 3 | 2 | 2 | 324,4 |
| 10 | 3 | 2 | 3 | 219,0 |
<!-- /tabela:tb_f5_manual_por_posicao -->

Por integrante (só descrição; o integrante é um número):

<!-- tabela:tb_f5_manual_por_integrante -->
| Integrante | Tentativas | Corrigidas | Com fim | Tempo médio (s) | Tempo somado (s) |
|---|---|---|---|---|---|
| 1 | 10 | 5 | 10 | 213,9 | 2138,9 |
| 2 | 10 | 0 | 4 | 43,6 | 174,5 |
| 3 | 10 | 9 | 10 | 278,2 | 2781,7 |
<!-- /tabela:tb_f5_manual_por_integrante -->

As linhas da planilha (as anuladas na hora, as anotadas à mão e as sem fim de cronômetro):

<!-- tabela:tb_f5_manual_linhas -->
| Linhas esperadas | Preenchidas | Anuladas na hora (fora de toda conta) | Anotadas à mão | Sem fim de cronômetro (estourou o limite ou não entregou) |
|---|---|---|---|---|
| 30 | 30 | nenhuma | nenhuma | linha 14 (integrante 2, ordem 3, `localizador-front-busca`); linha 15 (integrante 2, ordem 4, `localizador-front-admin-login`); linha 17 (integrante 2, ordem 6, `localizador-front-cliente-reserva`); linha 18 (integrante 2, ordem 7, `localizador-front-admin-produtos`); linha 19 (integrante 2, ordem 8, `contrato-field_renamed`); linha 20 (integrante 2, ordem 9, `contrato-field_missing`) |
<!-- /tabela:tb_f5_manual_linhas -->

**Leitura do lado das pessoas.** As 30 linhas da planilha estão preenchidas e nenhuma foi anulada. Das 30 tentativas, 14 tiveram Task Success (46,7%, intervalo de Wilson de 30,2% a 63,9%), e nenhum cenário foi corrigido pelos três. Chegaram ao fim do cronômetro 24; as 6 que não chegaram são do integrante 2: os quatro cenários de localizador e dois de contrato. O tempo médio, pela média de quem chegou ao fim em cada cenário, foi de 219,7 s (de 172,3 a 264,7 s): 174,8 s no contrato e 287,0 s no localizador. A segunda conta, com 600 s para quem não chegou ao fim, dá 289,8 s (de 241,0 a 339,6 s).

**Os três integrantes saíram muito diferentes** (bloco por integrante, que é só descrição). O integrante 1 corrigiu 5 de 10 e o integrante 3, 9 de 10, os dois chegando ao fim do cronômetro nos dez cenários. O integrante 2 não corrigiu nenhum: entregou quatro cenários de contrato, com 43,6 s de média, e deixou seis sem entrega. No contrato o cronômetro para na entrega da causa e do campo, certa ou errada. Por isso as entregas rápidas e erradas do integrante 2 puxam para baixo o tempo médio das pessoas nesses quatro cenários, o que favorece as pessoas na comparação do tempo, e puxam para baixo o Task Success delas, o que favorece o agente na comparação do Task Success (seção 6).

## 6. A comparação (regras L8 a L11)

**Aguarda os dois lados.** Os blocos abaixo são colados por `avaliar_fase5.py --comparar --colar`.

O resumo da comparação do tempo, com a frase da regra L9:

<!-- tabela:tb_f5_medicao_resumo -->
| MTTR médio do agente (s) | Reamostragem 95% (s) | Tempo médio das pessoas (s) | Reamostragem 95% (s) | Diferença média por cenário, pessoas menos agente (s) | Reamostragem 95% da diferença (s) | Razão entre as médias | Cenários com os dois lados | Agente mais rápido | Pessoas mais rápidas | Empates | p do teste dos sinais | Leitura pela regra L9 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 66,3 | 60,9 a 71,5 | 219,7 | 172,3 a 264,7 | 153,4 | 109,0 a 196,1 | 3,31 | 10 | 10 | 0 | 0 | 0,0020 | O agente reparou mais rápido que as pessoas: a diferença média por cenário (tempo das pessoas menos MTTR do agente) foi de 153,4 s, com intervalo de 95% de 109,0 a 196,1 s, que não contém zero, e o teste dos sinais deu p = 0,0020 (10 cenários com o agente mais rápido, nenhum cenário com as pessoas mais rápidas e nenhum empate). |
<!-- /tabela:tb_f5_medicao_resumo -->

O tempo por cenário, dos dois lados:

<!-- tabela:tb_f5_medicao_tempo_por_cenario -->
| Cenário | Tipo | MTTR médio do agente (s) | Faixa do agente (s) | Tempo médio das pessoas (s) | Faixa das pessoas (s) | Diferença, pessoas menos agente (s) | Razão | Quem foi mais rápido | As faixas se cruzam |
|---|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | 81,7 | 78,7 a 85,9 | 109,6 | 50,2 a 151,5 | 27,9 | 1,34 | agente | sim |
| `contrato-field_missing` | contrato | 67,0 | 66,4 a 67,8 | 111,3 | 95,0 a 127,7 | 44,4 | 1,66 | agente | não |
| `contrato-field_renamed` | contrato | 65,3 | 64,9 a 65,9 | 236,5 | 211,5 a 261,5 | 171,2 | 3,62 | agente | não |
| `contrato-type_drift` | contrato | 66,7 | 66,0 a 67,6 | 189,0 | 51,4 a 260,6 | 122,3 | 2,83 | agente | sim |
| `contrato-escala_ou_unidade_errada` | contrato | 80,4 | 78,8 a 82,9 | 280,6 | 35,2 a 454,5 | 200,2 | 3,49 | agente | sim |
| `contrato-error_500` | contrato | 76,6 | 75,0 a 77,3 | 121,8 | 37,8 a 174,9 | 45,2 | 1,59 | agente | sim |
| `localizador-front-busca` | localizador | 65,4 | 64,9 a 65,8 | 385,3 | 289,5 a 481,0 | 319,8 | 5,89 | agente | não |
| `localizador-front-admin-login` | localizador | 39,0 | 38,5 a 40,3 | 150,1 | 144,6 a 155,7 | 111,2 | 3,85 | agente | não |
| `localizador-front-admin-produtos` | localizador | 60,3 | 60,1 a 60,6 | 331,2 | 258,7 a 403,7 | 270,9 | 5,49 | agente | não |
| `localizador-front-cliente-reserva` | localizador | 61,0 | 60,0 a 63,1 | 281,6 | 167,7 a 395,4 | 220,6 | 4,62 | agente | não |
<!-- /tabela:tb_f5_medicao_tempo_por_cenario -->

O tempo por tipo de cenário, sem veredito (regra L10):

<!-- tabela:tb_f5_medicao_tempo_por_tipo -->
| Tipo | Cenários com os dois lados | Diferença média, pessoas menos agente (s) | Reamostragem 95% (s) | Razão entre as médias | Agente mais rápido | Pessoas mais rápidas | Empates | Sem medida |
|---|---|---|---|---|---|---|---|---|
| contrato | 6 | 101,9 | 52,0 a 156,4 | 2,40 | 6 | 0 | 0 | 0 |
| localizador | 4 | 230,6 | 138,5 a 295,4 | 5,09 | 4 | 0 | 0 | 0 |
<!-- /tabela:tb_f5_medicao_tempo_por_tipo -->

A segunda conta, com o limite de tempo no lugar de quem não chegou ao fim (regra L6; é um piso, e não o veredito):

<!-- tabela:tb_f5_medicao_piso -->
| Segunda conta: quem não chegou ao fim entra com 600 s | Cenários com os dois lados | Diferença média, pessoas menos agente (s) | Reamostragem 95% (s) | Razão entre as médias | Agente mais rápido | Pessoas mais rápidas | Empates | p do teste dos sinais | O que a regra L9 daria nesta conta |
|---|---|---|---|---|---|---|---|---|---|
| piso, não é o veredito da leitura | 10 | 213,1 | 149,2 a 272,8 | 3,78 | 9 | 1 | 0 | 0,0215 | veredito (agente) |
<!-- /tabela:tb_f5_medicao_piso -->

O Task Success dos dois lados (regra L11):

<!-- tabela:tb_f5_medicao_task_success -->
| Lado | Medidas | Task Success | Task Success (%) | Wilson 95% (%) | Cenários com todas certas |
|---|---|---|---|---|---|
| agente | 50 | 49 | 98,0 | 89,5 a 99,6 | 9 de 10 |
| pessoas | 30 | 14 | 46,7 | 30,2 a 63,9 | 0 de 10 |
<!-- /tabela:tb_f5_medicao_task_success -->

O Task Success por cenário:

<!-- tabela:tb_f5_medicao_task_success_por_cenario -->
| Cenário | Tipo | Agente | Agente (%) | Pessoas | Pessoas (%) | Diferença (pontos) | Parcela maior |
|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | 4 de 5 | 80,0 | 1 de 3 | 33,3 | 46,7 | agente |
| `contrato-field_missing` | contrato | 5 de 5 | 100,0 | 1 de 3 | 33,3 | 66,7 | agente |
| `contrato-field_renamed` | contrato | 5 de 5 | 100,0 | 2 de 3 | 66,7 | 33,3 | agente |
| `contrato-type_drift` | contrato | 5 de 5 | 100,0 | 0 de 3 | 0,0 | 100,0 | agente |
| `contrato-escala_ou_unidade_errada` | contrato | 5 de 5 | 100,0 | 1 de 3 | 33,3 | 66,7 | agente |
| `contrato-error_500` | contrato | 5 de 5 | 100,0 | 1 de 3 | 33,3 | 66,7 | agente |
| `localizador-front-busca` | localizador | 5 de 5 | 100,0 | 2 de 3 | 66,7 | 33,3 | agente |
| `localizador-front-admin-login` | localizador | 5 de 5 | 100,0 | 2 de 3 | 66,7 | 33,3 | agente |
| `localizador-front-admin-produtos` | localizador | 5 de 5 | 100,0 | 2 de 3 | 66,7 | 33,3 | agente |
| `localizador-front-cliente-reserva` | localizador | 5 de 5 | 100,0 | 2 de 3 | 66,7 | 33,3 | agente |
<!-- /tabela:tb_f5_medicao_task_success_por_cenario -->

O que é só descrição (regra L13):

<!-- tabela:tb_f5_medicao_descricao -->
| Só descrição (regra L13) | Agente | Pessoas | Diferença, pessoas menos agente (s) |
|---|---|---|---|
| tempo médio só com as medidas que tiveram Task Success (s) | 66,3 em 10 cenários | 246,0 em 9 cenários | 179,7 |
| tempo total médio da execução do agente, com a detecção (s) | 69,0 | não se aplica | não se aplica |
<!-- /tabela:tb_f5_medicao_descricao -->

**Leitura da comparação: o tempo (regra L9).** Veredito: o agente reparou mais rápido que as pessoas. O MTTR médio do agente foi de 66,3 s (de 60,9 a 71,5 s), contra 219,7 s das pessoas (de 172,3 a 264,7 s). A diferença média por cenário foi de 153,4 s, com intervalo de 109,0 a 196,1 s, que não contém zero; o agente foi mais rápido nos dez cenários, sem empate, e o teste dos sinais deu p = 0,0020. A razão entre as médias é 3,31. Na segunda conta, que põe 600 s no lugar de quem não chegou ao fim, a diferença sobe para 213,1 s e o agente fica mais rápido em 9 cenários: em `contrato-malformed_json` a execução do agente que não fechou o cronômetro pesa, e as pessoas ficam na frente. A regra L9 daria o mesmo veredito nessa conta (p = 0,0215).

**Por tipo de cenário (regra L10), sem veredito.** No contrato a diferença média foi de 101,9 s (de 52,0 a 156,4 s), com razão de 2,40; no localizador, de 230,6 s (de 138,5 a 295,4 s), com razão de 5,09. Em quatro dos seis cenários de contrato as faixas dos dois lados se cruzam: pelo menos uma pessoa foi mais rápida que o agente naquele cenário. Nos quatro de localizador nenhuma faixa se cruza.

**O Task Success (regra L11).** Veredito pelas regras: o agente resolveu mais cenários que as pessoas. Foram 49 de 50 execuções do agente (98,0%, intervalo de Wilson de 89,5% a 99,6%) contra 14 de 30 tentativas das pessoas (46,7%, de 30,2% a 63,9%); a parcela do agente foi maior nos dez cenários, e o teste dos sinais deu p = 0,0020.

**A ressalva do Task Success (ficha 91, decisão 151).** Esse veredito depende da sessão do integrante 2, que não corrigiu nenhum dos dez cenários e deixou seis sem entrega; é a sessão de quem já tinha lido a lista e não fez o treino de seletor (decisão 150). Numa conta de rascunho, feita depois de ver os números e fora das regras L1 a L15, sem essa sessão as pessoas ficam com 14 de 20, a parcela do agente é maior em 5 cenários e igual em 5, e o teste dos sinais dá p = 0,0625: o Task Success fica sem veredito. No tempo nada muda: sem ela o agente continua mais rápido nos dez cenários. Sem a sessão do integrante 1 ou sem a do integrante 3, os dois vereditos continuam. O Eric decidiu que a leitura fica como as regras deram, com a ressalva declarada, e que o resultado central da fase é o do tempo; a regra L14 só deixa anular medida por falha do protocolo anotada na hora, e não pelo resultado. A tabela dessa conta, gerada por script e marcada como exploratória, é o bloco logo abaixo (`tb_f5_medicao_sem_um_integrante`); os números dela são os mesmos da conta de rascunho citada neste parágrafo.

<!-- ! Alteração de IA - Revisar: (24/11/2026, ficha 91, decisão 151) bloco novo, `tb_f5_medicao_sem_um_integrante`, colado por `avaliar_fase5.py --comparar --colar` de `resultados_alvo/fase5/medicao.md` (campo `sem_um_integrante` de `medicao.json`); a última frase do parágrafo acima passou a apontar para ele.
     ! Motivo: a conta sem a sessão de cada integrante estava no relatório só como conta de rascunho, com números digitados. O Eric decidiu que ela entra como tabela gerada por script, marcada como exploratória: foi pensada depois de ver os números (regra L15) e não muda nenhum veredito. Os outros blocos desta seção não mudaram, e `avaliar_fase5.py --comparar --check` confere todos. -->
A mesma comparação refeita sem a sessão de um integrante por vez, com as regras L2 a L11 aplicadas às medidas que sobram. Como ler: cada linha tira uma sessão; as colunas do tempo dizem em quantos cenários cada lado foi mais rápido, a diferença média e o que a regra L9 daria; as do Task Success, em quantos cenários a parcela de cada lado foi maior e o que a regra L11 daria. O veredito da leitura continua sendo o das três sessões.

<!-- tabela:tb_f5_medicao_sem_um_integrante -->
| Conta exploratória de 24/11/2026, feita depois de ver os números; não é o veredito da leitura | Tentativas das pessoas que sobram | Corrigidas | Tempo médio das pessoas (s) | Diferença média por cenário, pessoas menos agente (s) | Reamostragem 95% (s) | Cenários com o agente mais rápido | Com as pessoas mais rápidas | Empates | p do teste dos sinais no tempo | O que a regra L9 daria | Cenários com a parcela do agente maior | Com a das pessoas maior | Iguais | p do teste dos sinais no Task Success | O que a regra L11 daria |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sem a sessão do integrante 1 | 20 | 9 | 237,4 | 171,1 | 112,2 a 222,7 | 10 | 0 | 0 | 0,0020 | veredito: o agente mais rápido | 10 | 0 | 0 | 0,0020 | veredito: o agente resolveu mais |
| sem a sessão do integrante 2 | 20 | 14 | 246,0 | 179,7 | 127,3 a 235,6 | 10 | 0 | 0 | 0,0020 | veredito: o agente mais rápido | 5 | 0 | 5 | 0,0625 | sem veredito (menos de 6 cenários diferentes) |
| sem a sessão do integrante 3 | 20 | 5 | 175,7 | 109,3 | 78,6 a 139,2 | 10 | 0 | 0 | 0,0020 | veredito: o agente mais rápido | 10 | 0 | 0 | 0,0020 | veredito: o agente resolveu mais |
<!-- /tabela:tb_f5_medicao_sem_um_integrante -->

**Contra a expectativa do projeto de pesquisa (seção 4).** A expectativa era que o agente reduzisse o MTTR "significativamente" contra a correção manual dos mesmos cenários. Nos dez cenários o tempo médio do agente foi cerca de um terço do das pessoas, com o agente na frente em todos. O que esse resultado não cobre está na seção 7.

## 7. Limitações

São as catorze da seção 12 do plano, com o que as decisões 134, 135 e 136 mudaram nelas. Todas entram no texto do TCC.

1. **A falha é armada, e não ocorrida, dos dois lados.**
2. **A pessoa parte da ficha que a detecção do agente escreveu.** A detecção não é medida na pessoa, e o MTTR do agente também começa depois dela. *Mudou com a decisão 136:* a pessoa lê o registro capturado antes (a chamada à API, a foto da tela e o HTML sem script) em vez de investigar o site no ar.
3. **Nos seis cenários de contrato, corrigido quer dizer diagnosticado:** a causa e o campo certos, sem conserto da API. A pessoa escolhe a causa numa lista fechada de 23, como o agente.
4. **O agente lê a biblioteca dele; a pessoa conta com o que sabe e com a definição de uma linha de cada causa.** *Mudou com as decisões 134 e 135:* as 23 definições foram escritas no pacote F2, e não copiadas do Apêndice A, que só tinha os nomes; e a pessoa recebe antes um tutorial, que ensina o uso das ferramentas do navegador e os jeitos de escrever um seletor, com exemplos de fora das cobaias.
5. **Três integrantes dão três tempos por cenário, e são estudantes do grupo que fez o projeto,** e não analistas de teste de fora. A ordem sorteada e o treino espalham o aprendizado, mas não o eliminam. *Mudou com a decisão 149:* um dos três previstos foi substituído por um quarto integrante do grupo, e nenhum dos três que entram na leitura conhece o código das cobaias (anotação do perfil).
6. **As cinco repetições do agente não são independentes;** por isso a unidade é o cenário, e são dez.
7. **Os dez cenários foram escolhidos pelo grupo,** e os seis de contrato estão numa página só, quatro deles no mesmo campo.
8. **A quebra de localizador do agente é armada pelo harness, e a das pessoas, pela variante do PHP;** a corrida 19 mediu as duas formas iguais. *Mudou com a decisão 136:* a pessoa entrega um seletor só em CSS, conferido na hora contra uma fotografia do HTML; o roteiro de verdade só roda na importação da sessão.
9. **O tempo do agente é o desta máquina, só em CPU.** *Mudou com a decisão 136:* o navegador, o aparelho e o relógio das pessoas passaram a ser os de cada integrante, e não os da máquina-alvo.
10. **O cronômetro das pessoas inclui o tempo de registrar a resposta,** e a regra L8 trata diferença menor que a folga do cronômetro como empate. *Mudou com a decisão 136:* quem registra o fim é a própria página, e não um facilitador.
11. **O limite de 10 minutos corta o tempo de quem não termina;** a segunda conta da regra L6 é um piso.
12. **O facilitador era o autor do projeto.** *Mudou com a decisão 136:* não há facilitador ao lado. O que pode e o que não pode durante a sessão virou um combinado com o integrante, sem ninguém para conferir.
13. **A noite roda sem o trace na falha** (decisão 93) e com a barra de progresso ligada.
14. **Com dez cenários, o teste só separa os lados quando quase todos apontam na mesma direção,** e por tipo não há veredito.

15. **(Da corrida 28.) O Ollama guarda o prompt já lido e o reaproveita quando o mesmo cenário se repete.** Na corrida 28 isso derrubou o MTTR das repetições 2 a 5 para menos da metade do da primeira (seções 2.3 e 11). Na corrida 28b o modelo é descarregado entre as repetições (decisão 146), e a leitura confere, repetição por repetição, que o prompt foi lido de novo (seção 4, bloco `tb_f5_agente_frio`). Dentro de uma repetição, o começo do prompt que os cenários dividem continua vindo guardado de um cenário para o outro, como na corrida 21d, e a primeira execução de cada repetição paga a carga do modelo.

O que as sessões das pessoas acrescentaram, em 24/11/2026:

16. **Duas das três pessoas que entram têm pouca prática, e uma delas tinha lido a lista dos cenários.** Pelo perfil, a prática vai de "não muito tempo" a seis meses de programação para a web, e duas nunca tinham usado as ferramentas do desenvolvedor. A linha de base mede estudantes no começo da prática, e não analistas de teste; com gente mais experiente o tempo das pessoas tende a ser outro.
17. **A sessão do integrante 2 entrou fora de duas regras do protocolo, declaradas:** a pessoa já tinha lido a lista dos cenários e não fez o treino de seletor (decisão 150). Ela não corrigiu nenhum cenário e deixou seis sem entrega.
18. **O veredito do Task Success depende dessa sessão** (decisão 151): sem ela, numa conta feita depois de ver os números, o Task Success fica sem veredito, e o do tempo continua. O resultado central da fase é o do tempo.
19. **No contrato, a entrega errada também para o cronômetro.** Uma resposta rápida e errada entra na média do tempo das pessoas como tempo curto. Isso favorece as pessoas na comparação do tempo; a linha "só com Task Success" da descrição (seção 6) mostra o tempo de quem acertou.
20. **A página 1 teve duas sessões, e só a do substituto entrou** (decisão 149). A outra não foi aberta. Sem facilitador ao lado, que os dois não se falaram sobre os cenários é a palavra do grupo, e não um registro.
21. **As sessões foram feitas em dias e aparelhos diferentes, de 18 a 24/11/2026,** com os endereços das páginas nas mãos dos integrantes desde 17/11/2026. Entre a primeira e a última sessão passaram seis dias, em que os integrantes podiam ter conversado.

## 8. Desvios do plano

Do livro-razão da fase, na ordem em que aconteceram. No fechamento da fase, em 25/11/2026, os 38 foram copiados por script para o anexo do [plano aprovado](../../../claude-memoria/plano-aprovado-fase-5.md), com o texto inteiro de cada um; aqui ficam resumidos.

1. A faixa da corrida 28 no painel entrou no pacote F0, e não no F5: o teste do painel recusa corrida do roadmap sem fase.
2. Dois consertos no painel que a linha da corrida 28 no roadmap pediu, fora da lista de entregas do plano.
3. (F1) Uma sexta opção na leitura, `--situacao`, e uma guarda no lançador: com as 50 execuções gravadas, a corrida não é chamada de novo.
4. (F1) Na conferência do agente contra o da corrida 21d, seis itens param a noite, os da seção 3.4 do plano; outros seis aparecem na tabela e só informam.
5. (F1) Um caso da regra L9 que o plano não escreve: o intervalo sem o zero e o teste abaixo do corte, mas com a maioria dos cenários do lado contrário ao da média. A leitura trata como "a média pende, sem veredito".
6. (F1) A segunda conta da regra L6 traz também o que a regra L9 daria nela, com o rótulo de que não é o veredito.
7. (F1) A leitura da planilha confere mais do que a lista da seção 4.6: a linha anulada, o tempo acima do limite numa linha não corrigida, a linha sem fim e a planilha regravada pelo Excel.
8. (F1) O lançador tem uma linha com acento, a do título da leitura.
9. (F1) `DETALHES-TECNICOS.md` ganhou as linhas dos arquivos novos.
10. (F2) As 23 definições de uma linha foram escritas no pacote, e não copiadas do Apêndice A do documento do TCC, que só traz os nomes (ficha 76, decisão 134).
11. (F2) As falas fixas do facilitador são sete, e não três.
12. (F2) O fim do cenário de contrato são dois eventos no registro da sessão, e não um.
13. (F2) Na planilha, os segundos saem com vírgula decimal, e as horas, sem os milésimos.
14. (F2) A ferramenta não mostra à pessoa se a resposta está certa, e a planilha é preenchida depois que ela sai.
15. (F2) Comandos e conferências fora da lista de entregas do pacote, entre eles o `ensaio` do facilitador.
16. (F2) O perfil tem, além das três perguntas, a anotação de quem conhece o código das cobaias. O número do integrante que levar essa anotação deixa de ser anônimo, porque o repositório cita o autor do site legado.
17. (F2) O roadmap e o painel foram editados pela sessão do F2, e não só pela sessão que fecha.
18. (decisão 135) Os integrantes recebem um tutorial antes da sessão, que o plano não previa. Muda a limitação 4.
19. (decisão 136) As sessões deixam de ser presenciais, na máquina-alvo e com facilitador, e passam a ser feitas por uma página publicada. Mudam as limitações 2, 4, 8, 9, 10 e 12. A corrida 28, as regras de leitura e o formato do registro não mudam.
20. (F6, em parte) Parte do pacote F6 foi escrita em 16/11/2026, antes da corrida 28 e das sessões: no documento do TCC entraram o Apêndice A com a coluna das explicações, o método da linha de base e as regras de leitura na seção 5.7, as limitações conhecidas e as entradas novas do glossário.
21. (F6, em parte) No documento do TCC, a justificativa da regra L2 não repete a frase do plano sobre a corrida 21b: diz que, quando o ensaio dos dez cenários foi repetido, o rótulo do diagnóstico se repetiu de uma corrida para a outra.
22. (F6, em parte) A tabela das 23 causas do Apêndice A mudou de forma, de duas metades lado a lado para três colunas, e não só ganhou uma coluna, como a decisão 134 diz.
23. (F5, em parte) A aba do painel, a entrada do teste dos sinais no glossário, a referência original dele e este esqueleto foram feitos em 16/11/2026, antes da corrida 28 (F3) e das sessões (F4), e não em 25/11/2026. Nada foi gravado nas pastas dos resultados da fase.
24. (F5, em parte) Os dois gráficos da aba existem antes das medidas, com o lado ainda não medido fora do primeiro e como "por medir" no segundo: o teste do painel exige uma leitura para todo gráfico e um gráfico para toda leitura. A resposta em uma frase da aba é gerada do estado dos arquivos e, com a comparação gravada, é a frase das regras L9 e L11; a frase escrita à mão em `painel_leituras.py`, que a seção 6 do plano previa, fica para depois dos números.
25. (F5, em parte) Antes das medidas só existe o derivado do custo, que não traz as constantes das regras nem a lista dos cenários. A aba lê as constantes do texto do código da leitura, com um teste que as compara com as do módulo, e os cenários, os integrantes e as linhas preenchidas, da planilha. Nenhum derivado ganhou campo, e a aba não faz conta de comparação.
26. (F5, em parte) O `--check` da leitura feito com `--pasta` fora da pasta oficial dos derivados deixou de comparar os blocos deste relatório, que são os da leitura oficial. Nenhuma regra de leitura mudou.
27. (F5, em parte) Este relatório nasceu com os blocos do agente, das pessoas e da comparação vazios. Até o `--colar` de cada leitura, o `--check` oficial dela acusa blocos divergentes aqui: a ordem é `--colar` e depois `--check`.

28. (F3) A noite levou 31 minutos, e não os 68 que a seção 3.2 do plano estimava: o plano não previu que o Ollama reaproveitaria, nas repetições 2 a 5, o prompt lido na repetição 1. O efeito no MTTR virou a limitação 15 e as fichas 84 e 86.
29. (F3) A corrida 28 foi lançada com o aplicativo Claude aberto, e o plano pede o aplicativo Claude e o VS Code fechados. O Eric decidiu refazer a noite (decisão 145), e a noite nova, a corrida 28b, roda uma repetição por vez, com o modelo descarregado entre elas (decisão 146). É desvio da frase do plano "a primeira noite completa é a que vale": a noite nova não foi pedida para melhorar o número, e a frio o agente fica mais lento. O lançador e a leitura mudam para a pasta nova, com o teste antes do código.
30. (corrida 28b) Três coisas que o plano não previa entraram com a noite a frio, todas escritas e testadas antes dela. A leitura confere, por repetição, que o prompt foi lido de novo, e só grava a noite completa e a frio: é conferência de validade da noite, com o limite fixado antes da corrida 28b sobre os registros da corrida 28, e não regra de comparação (as regras L1 a L15 não mudam). O lançador roda uma repetição por vez e só começa se a sondagem do frio tiver passado na versão do Ollama que está no ar. E a leitura da corrida 28 fica guardada à parte (`resultados_alvo/fase5_incidente_28`, blocos `tb_f5_incidente28_*`, seção 11), fora da comparação.

31. (F4, decisão 149) A linha de base não foi feita pelos três integrantes da decisão 130: um deles respondeu que já tinha lido a lista dos cenários e foi substituído por um quarto integrante do grupo, na mesma página. Vieram quatro códigos para três páginas; o da sessão substituída ficou guardado sem ser importado.
32. (F4, decisão 150) A sessão da página 2 entrou com a pessoa tendo lido a lista dos cenários e sem o treino de seletor, que o plano (seção 4.3) põe antes do primeiro cenário medido.
33. (F4) As sessões aconteceram de 18 a 24/11/2026, e não de 19 a 24/11/2026, como a decisão 130 previa: uma delas foi feita na véspera do intervalo. As datas não chegaram a ser marcadas antes das sessões.
34. (F5) A leitura das pessoas e a comparação rodaram em 24/11/2026, um dia antes do calendário do plano, porque as sessões já tinham chegado.
35. (F5, decisão 151) A leitura ganha uma conta que o plano não tinha: a comparação sem a sessão de cada integrante, feita depois de ver os números e marcada como exploratória. Ela não muda nenhum veredito das regras L9 e L11; serve para dizer do que cada veredito depende.

<!-- ! Alteração de IA - Revisar: (25/11/2026, pacote F6 conferido) os desvios 36 a 38 entraram na lista, e o estado e as linhas F5 e F6 da tabela dos pacotes passaram a dizer que a descoberta, a tabela exploratória e o texto do TCC estão feitos.
     ! Motivo: a lista parava no desvio 35, e o livro-razão da fase já tinha o 36 e o 37, da sessão da aba do painel; o 38 é do pacote F6, feito em 24/11/2026. Sem eles o anexo de desvios do fechamento sairia incompleto. -->
36. (F5, decisão 151) Na aba do painel, a ressalva do Task Success é um texto escrito à mão, amarrado à corrida lida, e o alto da aba continua sendo as frases das regras L9 e L11, com o tempo dito como o resultado central; o plano previa uma frase à mão no alto da aba.
37. (F5, decisão 151) No README e na figura da descoberta da fase, o Task Success não é desenhado nem apresentado como segundo resultado central: entra num parágrafo à parte, com a ressalva, e na tabela de dados da figura.
38. (F6) As seções da Fase 5 entraram no documento do TCC em 24/11/2026, e não em 26 e 27/11/2026, parte delas adiantada em 16/11/2026 (desvios 20 a 22). O Word não foi regerado: sai uma vez só, com o pacote Q8 da Pós-Fase 4, que também corta o resumo e acerta as frases da Fase 4 que ainda dão corridas como pendentes.

## 9. O que o documento do TCC precisa carregar

Da seção 6 do plano, para o pacote F6:

- O resumo e o abstract, com o resultado central.
- A seção 5.1, com a etapa concluída.
- A seção 5.7, com as regras de leitura e o teste dos sinais resumido e citado na chamada (DIXON; MOOD, 1946).
- Uma seção nova da Fase 5 depois da 6.7, com o gráfico e o "Como ler". Ela empurra em uma casa a numeração da Discussão e da Análise aprofundada.
- A Discussão, com as limitações da seção 7 deste relatório.
- Os dados crus na Análise aprofundada.
- A Conclusão, com a resposta ao quinto objetivo e à expectativa da seção 4 do projeto de pesquisa.
- O glossário e, no Apêndice A, a coluna com as 23 explicações de uma linha (decisão 134).
- A figura da comparação, gerada por `gerar_figuras_documentos.py`.

**Os números que entram em cada lugar** estão nas seções 4, 5 e 6, desde 24/11/2026. O texto do TCC leva o resultado do tempo como o central e o do Task Success com a ressalva da decisão 151; a substituição de um integrante (decisão 149), a sessão declarada (decisão 150) e as limitações 16 a 21 entram na Discussão.

## 10. Rastreabilidade

| O quê | Onde |
|---|---|
| Plano da fase | [plano-aprovado-fase-5.md](../../../claude-memoria/plano-aprovado-fase-5.md) |
| Decisões | [decisoes.md](../1-decisoes-e-historico/decisoes.md): 130 a 136; da Fase 4, 79, 93 e 101 |
| Fichas | [pendencias.md](../pendencias.md): 72 a 76 |
| Roadmap | [roadmap.md](../roadmap.md): a linha da Fase 5 no §1, a corrida 28 no §2 e o §5 |
| Protocolo, tutorial e planilha | [protocolo-linha-de-base-manual.md](../5-metodo-e-ferramental/protocolo-linha-de-base-manual.md), [tutorial-do-integrante.md](../5-metodo-e-ferramental/tutorial-do-integrante.md) e `planilha-linha-de-base-manual.csv`, na mesma pasta |
| Leitura | `Programacao/AgenteCore/experimentos/avaliar_fase5.py`, com os derivados em `resultados_alvo/fase5/` (`custo`, `agente`, `manual` e `medicao`, cada um em `.json` e `.md`) |
| Testes | `testar_fase5.py` (a leitura e o lançador) e `testar_linha_de_base.py` (o ajudante, o tutorial e as páginas da sessão), na mesma pasta |
| Lançador da noite | `Programacao/AgenteCore/experimentos/rodar_fase5.ps1` (corrida 28b, uma repetição por vez) e, antes dele, a sondagem do frio, `rodar_sondagem_frio.ps1` |
| Registros | `resultados_alvo/fase5_agente_b/` (a corrida 28b, a medida do agente), `resultados_alvo/fase5_agente/` (a corrida 28, incidente, com a leitura guardada em `resultados_alvo/fase5_incidente_28/`), `resultados_alvo/fase5_sondagem_frio_<data>_<hora>/` (as sondagens do frio), `resultados_alvo/fase5_manual/` (o registro das sessões e o perfil dos integrantes) e `resultados_alvo/fase5_material/` (o material capturado para as páginas) |
| Painel | a aba "Agente contra pessoa" (`medicao`), no grupo da Fase 5, e a entrada "Teste dos sinais" no glossário |
| Fonte do teste dos sinais | [referencias.md](../2-pesquisa-e-literatura/referencias.md), bloco "Métodos clássicos de medida": DIXON; MOOD, 1946 |

## 11. Incidente: a corrida 28, fora da comparação

<!-- ! Alteração de IA - Revisar: seção nova (18/11/2026) com a leitura da corrida 28 como incidente. Os blocos `tb_f5_incidente28_*` são colados por `avaliar_fase5.py --incidente 28 --colar`, de `resultados_alvo/fase5_incidente_28/agente.md`, e `avaliar_fase5.py --incidente 28 --check` confere que batem com os registros da corrida; os dois parágrafos de leitura vieram da seção 4, sem reescrita.
     ! Motivo: os números da corrida 28 precisam continuar no relatório, porque foi ela que mostrou o reaproveitamento do prompt e levou à forma da noite nova, mas não no lugar do lado do agente. Com outro prefixo de bloco, o `--agente --colar` da corrida 28b não tem como colar por cima deles, nem eles no lugar dos da medida. -->

**Esta corrida não vale como a medida do agente.** A corrida 28 rodou em 18/11/2026, lançada com o aplicativo Claude aberto, e o Eric decidiu refazer a noite (decisão 145); nas repetições 2 a 5 dela o Ollama reaproveitou o prompt lido na repetição 1, e por isso a noite nova roda a frio (decisão 146). Os registros ficam intactos em `resultados_alvo/fase5_agente/`, e a leitura deles, em `resultados_alvo/fase5_incidente_28/`. Nada desta seção entra na comparação com as pessoas.

O agente no geral, na corrida 28:

<!-- tabela:tb_f5_incidente28_resumo -->
| Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Cenários com todas certas | Com fim de cronômetro | Sem fim | MTTR médio (s) | Reamostragem 95% (s) | Segunda conta, com 600 s para quem não chegou ao fim (s) | Reamostragem 95% da segunda conta (s) | Só com Task Success (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 49 | 98,0 | 89,5 a 99,6 | 9 de 10 | 49 | 1 | 30,5 | 27,2 a 33,8 | 42,0 | 28,8 a 64,9 | 30,5 |
<!-- /tabela:tb_f5_incidente28_resumo -->

Por tipo de cenário:

<!-- tabela:tb_f5_incidente28_por_tipo -->
| Tipo | Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Cenários com todas certas | Com fim de cronômetro | Sem fim | MTTR médio (s) | Reamostragem 95% (s) | Segunda conta, com 600 s para quem não chegou ao fim (s) | Reamostragem 95% da segunda conta (s) | Só com Task Success (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| contrato | 30 | 29 | 96,7 | 83,3 a 99,4 | 5 de 6 | 29 | 1 | 28,0 | 25,4 a 30,5 | 47,3 | 27,9 a 83,8 | 28,0 |
| localizador | 20 | 20 | 100,0 | 83,9 a 100,0 | 4 de 4 | 20 | 0 | 34,2 | 26,8 a 41,6 | 34,2 | 26,8 a 41,6 | 34,2 |
<!-- /tabela:tb_f5_incidente28_por_tipo -->

Cenário a cenário:

<!-- tabela:tb_f5_incidente28_por_cenario -->
| Cenário | Tipo | Execuções | Task Success | Com fim | MTTR médio (s) | Mínimo (s) | Máximo (s) | Segunda conta (s) | Só com Task Success (s) | Rótulo do diagnóstico em cada repetição | Tempo total da execução (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | 5 | 4 | 4 | 22,1 | 21,9 | 22,3 | 137,7 | 22,1 | `resposta_truncada`, `resposta_truncada`, `resposta_truncada`, `resposta_truncada`, `resposta_truncada` | 32,1 |
| `contrato-field_missing` | contrato | 5 | 5 | 5 | 27,6 | 17,9 | 66,2 | 27,6 | 27,6 | `campo_ausente`, `campo_ausente`, `campo_ausente`, `campo_ausente`, `campo_ausente` | 27,9 |
| `contrato-field_renamed` | contrato | 5 | 5 | 5 | 26,3 | 16,3 | 65,1 | 26,3 | 26,3 | `campo_renomeado`, `campo_renomeado`, `campo_renomeado`, `campo_renomeado`, `campo_renomeado` | 26,7 |
| `contrato-type_drift` | contrato | 5 | 5 | 5 | 29,0 | 18,2 | 67,5 | 29,0 | 29,0 | `tipo_divergente`, `tipo_divergente`, `tipo_divergente`, `tipo_divergente`, `tipo_divergente` | 29,4 |
| `contrato-escala_ou_unidade_errada` | contrato | 5 | 5 | 5 | 32,4 | 19,3 | 80,1 | 32,4 | 32,4 | `escala_ou_unidade_errada`, `escala_ou_unidade_errada`, `escala_ou_unidade_errada`, `escala_ou_unidade_errada`, `escala_ou_unidade_errada` | 32,8 |
| `contrato-error_500` | contrato | 5 | 5 | 5 | 30,8 | 18,2 | 76,6 | 30,8 | 30,8 | `erro_interno_do_servidor`, `erro_interno_do_servidor`, `erro_interno_do_servidor`, `erro_interno_do_servidor`, `erro_interno_do_servidor` | 31,1 |
| `localizador-front-busca` | localizador | 5 | 5 | 5 | 44,4 | 38,8 | 65,2 | 44,4 | 44,4 | `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado` | 49,8 |
| `localizador-front-admin-login` | localizador | 5 | 5 | 5 | 38,8 | 38,3 | 39,5 | 38,8 | 38,8 | `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado` | 44,2 |
| `localizador-front-admin-produtos` | localizador | 5 | 5 | 5 | 27,4 | 19,0 | 60,3 | 27,4 | 27,4 | `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado` | 33,2 |
| `localizador-front-cliente-reserva` | localizador | 5 | 5 | 5 | 26,2 | 17,2 | 60,0 | 26,2 | 26,2 | `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado`, `localizador_quebrado` | 32,5 |
<!-- /tabela:tb_f5_incidente28_por_cenario -->

A noite conferida:

<!-- tabela:tb_f5_incidente28_noite -->
| Execuções gravadas | Esperadas | Noite completa | Noite a frio | Versões do Ollama nos diagnósticos | Versões do navegador | Hash do banco no começo das repetições | Linha FIM no log | Tempo total das execuções (s) | Tempo total médio por cenário (s) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 50 | sim | não | 0.40.16 | 156.0.8078.4 | 9fe5e7cb64288c9d | sim | 1698,0 | 34,0 |
<!-- /tabela:tb_f5_incidente28_noite -->

A conferência a frio, repetição por repetição. É nesta tabela que o limite da seção 4 foi fixado: a repetição 1, que leu o prompt de novo, passa; as repetições 2 a 5, em que a primeira inferência já veio com o prompt guardado, não passam.

<!-- tabela:tb_f5_incidente28_frio -->
| Repetição | Inferências | Tokens de entrada | Tokens que vieram do que o Ollama tinha guardado | Parcela guardada (%) | Guardados na primeira inferência | Leitura do prompt, somada (s) | Carga do modelo, somada (s) | A frio |
|---|---|---|---|---|---|---|---|---|
| 1 | 10 | 11966 | 1505 | 12,6 | 0 | 462,4 | 8,7 | sim |
| 2 | 10 | 11966 | 10975 | 91,7 | 1217 | 45,3 | 0,3 | não |
| 3 | 10 | 11966 | 10975 | 91,7 | 1217 | 45,0 | 0,3 | não |
| 4 | 10 | 11966 | 10975 | 91,7 | 1217 | 44,3 | 0,3 | não |
| 5 | 10 | 11966 | 10975 | 91,7 | 1217 | 43,8 | 0,2 | não |
<!-- /tabela:tb_f5_incidente28_frio -->

O agente da corrida 28 contra o da corrida 21d:

<!-- tabela:tb_f5_incidente28_identidade -->
| Item | Na corrida | Na corrida 21d | Igual | Para a noite se diferir |
|---|---|---|---|---|
| biblioteca de produção (hash) | `95af35290860` | `95af35290860` | sim | sim |
| prompt fixo do diagnóstico (hash) | `2e42cf9c31826941` | `2e42cf9c31826941` | sim | sim |
| índice da busca (hash) | `11e763ba9cb1fdf4` | `11e763ba9cb1fdf4` | sim | sim |
| k (verbetes entregues ao modelo) | `3` | `3` | sim | sim |
| limiares do selo | `baixo até 0,8318, alto a partir de 0,9898, k 3 (conteúdo 13a02982)` | `baixo até 0,8318, alto a partir de 0,9898, k 3 (conteúdo 13a02982)` | sim | sim |
| versão do navegador | `156.0.8078.4` | `156.0.8078.4` | sim | sim |
| modelo | `qwen2.5:7b` | `qwen2.5:7b` | sim | não |
| alternativas por posição (top_logprobs) | `20` | `20` | sim | não |
| teto de tokens da resposta | `600` | `600` | sim | não |
| Playwright | `1.64.1` | `1.64.1` | sim | não |
| versão do código do caso ao vivo | `5` | `4` | não | não |
| busca com os sinais contra a referência | `True` | `True` | sim | não |
<!-- /tabela:tb_f5_incidente28_identidade -->

As execuções que não chegaram ao resultado:

<!-- tabela:tb_f5_incidente28_sem_sucesso -->
| Cenário | Repetição | Tipo | Detectou | Rótulo do diagnóstico | Causa esperada | Falha da cura | MTTR (s) | Segundos |
|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | 1 | contrato | sim | `resposta_truncada` | `resposta_truncada` | n/d | n/d | 70,9 |
<!-- /tabela:tb_f5_incidente28_sem_sucesso -->

**Leitura da corrida 28, pela regra do plano.** Pelos registros a noite está inteira: 50 de 50 execuções, uma versão só do Ollama e uma do navegador, o banco com o mesmo hash no começo das cinco repetições, a linha FIM no log e o agente igual ao da corrida 21d nos seis itens que parariam a noite. O agente teve Task Success em 49 de 50 execuções (98,0%, intervalo de Wilson de 89,5% a 99,6%), com 9 dos 10 cenários certos nas cinco repetições, e MTTR médio de 30,5 s (de 27,2 a 33,8 s). A execução sem Task Success foi a primeira de `contrato-malformed_json`: o rótulo saiu certo, mas a resposta do modelo veio sem a linha FONTE (`conferencia.linhas.FONTE` falso em `fase5_agente/cenarios.jsonl`), o diagnóstico não foi conferido em código e o cronômetro não fechou.

**O que a média das cinco repetições esconde.** Só a repetição 1 leu o prompt inteiro; nas outras quatro o Ollama reaproveitou o que tinha guardado (seção 2.3). Na tabela por cenário isso aparece na distância entre o mínimo e o máximo: o máximo é a repetição 1. Pelas linhas de cada execução no log, o MTTR da repetição 1 ficou entre 38,5 e 80,1 s nos nove cenários que fecharam o cronômetro, com média de 64,4 s, e o das repetições 2 a 5, entre 16,3 e 39,6 s. A corrida 21d, com uma repetição e a versão 0.40.14 do Ollama, tinha dado média de 74,0 s (`resultados_alvo/fase4/cenarios_v4.json`, campo `geral.mttr_media_s`). Uma falha de verdade aparece uma vez, e o agente lê o prompt inteiro, como na repetição 1. A média de 64,4 s e as faixas por repetição foram calculadas depois de ver os números, fora das regras L1 a L15: valem como descrição, e não como veredito. Foi isso que levou à forma da noite nova: na corrida 28b o modelo é descarregado entre as repetições, para as cinco medirem o mesmo que a repetição 1 (ficha 86, decisão 146). A ficha 84, respondida antes pelo Eric (as duas leituras lado a lado, decisão 144), deixou de ter efeito com isso. As três fichas foram respondidas em 18/11/2026, antes de qualquer sessão das pessoas ser trazida para o repositório.
