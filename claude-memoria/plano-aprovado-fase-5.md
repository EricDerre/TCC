<!-- ! Alteração de IA - Revisar: em 16/11/2026 o arquivo `plano-fase-5.md` passou a ser este `plano-aprovado-fase-5.md`, com o parágrafo de estado trocado pelo cabeçalho de aprovação (data, decisões 130 a 133 e a resposta de cada ficha); o texto do plano não foi reescrito, e o comentário original logo abaixo fica como registro de quando ele era proposta.
     ! Motivo: o Eric aprovou o plano como está e respondeu as fichas 72 a 75 no quadro da sessão, todas pela recomendação; o rito das fases pede o texto aprovado congelado neste nome, com as respostas no cabeçalho, antes de qualquer código ou corrida da fase. -->
<!-- ! Alteração de IA - Revisar: arquivo novo (16/11/2026) com o plano da Fase 5 (a medição de valor: o agente contra a linha de base manual), escrito para a aprovação do Eric a partir do roadmap (§1, §2.20, §5 e §6), do protocolo da linha de base manual (versão 1, pacote P6 da Fase 4), do plano aprovado da Fase 4 (seção 3.9) e do da Pós-Fase 4 (seções 7 a 9), das decisões 47, 79, 93, 94 e 101, das fichas 35 e 36, do projeto ABNT (seção 3.4) e da leitura do código dos cenários e dos registros da corrida 21d. Nenhum código da fase foi escrito, nenhuma corrida rodou e o modelo não foi chamado.
     ! Motivo: em 16/11/2026 o Eric pediu para começar a Fase 5, e o rito das fases pede o plano aprovado antes de qualquer código ou corrida. As regras de leitura precisam estar escritas antes da primeira medida, para a comparação entre o agente e as pessoas não ser escolhida depois de ver os números. As escolhas que são dele estão nas fichas 72 a 75 de `Documentacao/memorial/pendencias.md`. Este arquivo vira `plano-aprovado-fase-5.md` só depois do sim dele. Os números citados foram lidos por script, em 16/11/2026, dos arquivos indicados em cada trecho (arquivo e campo); nenhum foi digitado de memória. -->

**Aprovado pelo Eric em 16/11/2026, como está (decisão 133).** As fichas 72 a 75 de [pendencias.md](../Documentacao/memorial/pendencias.md) foram respondidas no mesmo dia, no quadro da sessão, todas pela recomendação: 72 (a), três integrantes do grupo, um por vez, na máquina-alvo, com o Eric de facilitador, entre 19 e 24/11/2026 (decisão 130; os nomes e as datas ficaram por dizer); 73 (a), o protocolo da sessão passa à versão 2, com as três mudanças (decisão 131); 74 (a), o cenário como unidade da comparação (decisão 132); 75 (a), este plano (decisão 133). O texto abaixo não é reescrito: o que desviar dele durante a execução vai para o livro-razão e, no fechamento, para um anexo ao fim deste arquivo, como nos planos da Fase 4 e da Pós-Fase 4.

> Estado em 16/11/2026: aprovado; pacote F0 feito; execução por começar pelos pacotes F1 e F2 (seção 8). Livro-razão em `.superpowers/sdd/fase-5/progress.md` (fora do git), a abrir no F1.
>
> Estado em 25/11/2026: fase concluída (ficha 96, decisão 156). O texto aprovado abaixo não foi reescrito; o que a execução fez de diferente dele está no anexo, no fim do arquivo (desvios 1 a 38), e o resultado, no [relatório da fase](../Documentacao/memorial/3-resultados-e-analises/fase-5-relatorio.md).

# Plano da Fase 5: a medição de valor

Data: 16/11/2026. Máquina: a máquina-alvo das corridas da Fase 4 (i5-1235U, 16 GB, sem GPU utilizável, Windows 11 corporativo sem administrador). Repositório: `C:\Users\Eric.Derre\Documents\TCC` (`main`, último commit `717f68c2`).

Notação: `RAIZ` = repositório; `EXP` = `RAIZ\Programacao\AgenteCore\experimentos`; `RA` = `EXP\resultados_alvo`; `DOC` = `RAIZ\Documentacao\memorial`; `FER` = `RAIZ\ferramentas`; `SDD` = `RAIZ\.superpowers\sdd\fase-5` (pasta nova, fora do git); `PROTO` = `DOC\5-metodo-e-ferramental\protocolo-linha-de-base-manual.md`.

## 1. Contexto

### 1.1 O que a Fase 5 entrega

A Fase 5 responde à pergunta do quinto objetivo específico do projeto: o agente repara mais rápido que uma pessoa, e resolve tantos cenários quanto ela? O projeto ABNT (seção 3.4) define as duas medidas. O MTTR (tempo médio de reparo) vai da detecção da falha pelo agente até a correção validada na reexecução. O Task Success (sucesso da tarefa) é a parcela dos cenários de falha injetados em que o fluxo foi restaurado e o roteiro concluiu sem erro. A linha de base são os mesmos cenários resolvidos à mão por integrantes do grupo, com o tempo cronometrado, e a comparação entre os dois tempos é o resultado central da avaliação.

Sai desta fase: os dez cenários rodados pelo agente com cinco repetições (50 execuções); os mesmos dez resolvidos por três integrantes (30 tentativas); a leitura dos dois lados por script, com as regras fixadas neste plano antes de qualquer medida; a aba da medição no painel; o relatório da fase no Memorial; e o texto das seções do documento do TCC que recebem os números.

### 1.2 O que já está decidido (não se rediscute aqui)

| Tema | Decisão | Onde |
|---|---|---|
| As duas medidas | MTTR e Task Success, contra a linha de base manual cronometrada; cerca de dez cenários com cinco repetições; banco restaurado entre execuções; modo de falha fixo por cenário; navegador fixo; nas duas cobaias | projeto ABNT, seção 3.4 |
| Os dez cenários | seis de contrato em `produtos_api.php` (um por modo de falha da CobaiaAPI) e quatro de localizador no front legado (um por roteiro), em `cenarios_fase4.CENARIOS_DO_ENSAIO`; `latency` saiu e `escala_ou_unidade_errada` entrou (`TROCA_DA_FICHA_36`) | ficha 36, decisão 79 |
| O que conta como corrigido | localizador: o roteiro concluído sem erro com um localizador novo. Contrato: o agente não conserta a API, ele diagnostica; o cronômetro para no diagnóstico conferido em código, e o Task Success é a causa e o campo certos | ficha 35, decisão 79 |
| Linha de base | três integrantes, cada um nos dez cenários, numa sessão agendada com o protocolo escrito | ficha 36, decisão 79; `PROTO` |
| O agente que é medido | o das corridas 18d e 21d: `qwen2.5:7b`, k = 3, limiares de `limiares.json`, biblioteca de produção, prompt do diagnóstico congelado byte a byte, busca com os sinais contra a referência. Nada da Pós-Fase 4 mudou o que o agente mede | plano da Pós-Fase 4, seções 1.2 e 7; decisões 79, 91, 97 e 99 |
| Sem trace na falha | a Fase 5 roda sem o trace do Playwright; ele entra na interface para o analista, depois | decisão 93 |
| Ordem das fases | a Pós-Fase 4 (pacotes Q1 a Q5) veio antes; o hub (Q6), a integração com o Git (Q7) e a documentação final (Q8) vêm depois da Fase 5 | decisões 94 e 101 |
| Ponte de versão | toda noite medida começa conferindo a versão do Ollama contra `RA\fase4\pontes.json`; versão sem ponte roda antes a L0 nos 36 casos de avaliação; pareável com b + c até 2 | regra R6 do plano da Fase 4; decisões 44 e 47 |
| Medição | um modelo residente por vez; só CPU; `num_ctx` 8192; temperatura 0,1; corrida com modelo lançada da janela do Eric, com o aplicativo Claude e o VS Code fechados | decisões 44 e 69; `.claude/rules/experimentos.md` |
| Inferência estatística | toda proporção com intervalo de Wilson de 95%; comparação pareada pelo teste exato de McNemar; média com intervalo por reamostragem de semente fixa | projeto ABNT, seção 3.4; `avaliar.wilson`, `avaliar.mcnemar_exato`, `avaliar_fase4.bootstrap_media` |

### 1.3 O que a leitura de 16/11/2026 mostrou (só leitura)

**O ensaio vigente.** A corrida 21d (06/11/2026, pasta `RA\fase4_ensaio_v4`, leitura `RA\fase4\cenarios_v4.json`) rodou os dez cenários com uma repetição: 10 de 10 com Task Success (`geral.sucessos`), MTTR médio de 74,0 s (`geral.mttr_media_s`), 81,5 s no contrato e 62,7 s no localizador (`por_tipo`). O MTTR de uma execução foi de 42,3 s a 92,7 s (`mttr_s` em `cenarios.jsonl`), e quase todo ele é a inferência do modelo: de 39,6 s a 90,7 s (`segundos` em `diagnosticos__cenarios.jsonl`). O executor levou 808 s (linha FIM de `fase4.log`), dos quais 767,2 s dentro das dez execuções (`tempo.segundos_total`). O maior prompt teve 1385 tokens, abaixo do limite de 1409 (`prompt`). Navegador 156.0.8078.4 e o mesmo hash do banco, `9fe5e7cb64288c9d`, no começo da repetição.

**O que identifica o agente da 21d.** `condicoes_fase4.json` da corrida guarda a biblioteca de produção `95af35290860`, o hash do prompt fixo `2e42cf9c31826941`, o hash do índice da busca `11e763ba9cb1fdf4`, k = 3 e o Playwright 1.64.1. Desde a 21d o código do caso ao vivo passou da versão 4 à 5 (`caso_ao_vivo.VERSAO_DO_CASO`, o teto nas listas da decisão 99, que o próprio comentário do código diz não mudar nenhum prompt das corridas 18d e 21d), e a chamada ao modelo passou a ser observada pela barra de progresso (`executar_fase4.com_progresso`, pacote Q4).

**Ponte.** A última ponte registrada em `RA\fase4\pontes.json` é a da versão 0.40.16 do Ollama, de 16/11/2026 (pasta `fase3b_ponte_04016`, b = 1, c = 0, pareável). A 21d rodou na 0.40.14. As três últimas pontes levaram 00h42, 00h34 e 00h37 (linha FIM do `fase3b.log` de cada pasta).

**O que já existe para a noite.** `rodar_fase4.ps1 -Modo cenarios -Repeticoes N` roda a bateria `testar_fase4.py`, confere o Ollama, a memória livre e a versão antes e depois, chama `executar_fase4.py --modo cenarios` (banco restaurado e conferido por hash no começo de cada repetição, versão do navegador conferida em todas, retomada pelas execuções que faltam em `cenarios.jsonl`) e grava a leitura por `avaliar_fase4.py --cenarios`. Sem `-Nome`, essa leitura grava em `RA\fase4\cenarios.{json,md}`, que é a leitura da corrida 21: a noite da Fase 5 precisa de um nome próprio.

**O que já existe para as pessoas.** `PROTO` (versão 1) e o ajudante `linha_de_base_manual.py`, com `ordem`, `armar`, `conferir` e `desarmar`. A planilha `planilha-linha-de-base-manual.csv` já está sorteada (semente 20261104 mais o número do integrante) e em branco. A ficha da falha que a pessoa recebe é o texto que a detecção do agente gravou (`motivo_deteccao`), e ele é igual, cenário a cenário, nas quatro corridas do ensaio (21, 21b, 21c e 21d), conferido por script.

**O que falta.** Não existe leitura da planilha por script; `PROTO` diz que ela entra na Fase 5. Na versão 1 do protocolo é o facilitador quem anota à mão a hora de início e de fim. Não existe lançador da noite nem leitura que ponha os dois lados na mesma tabela. O painel tem o grupo "Fase 5" só com a aba de visão (`f-5`).

## 2. Princípios que valem para o plano todo

1. **As regras de leitura vêm antes da medida.** Como cada número é calculado, que intervalo o acompanha e o que conta como diferença estão na seção 5, e o código da leitura é escrito e testado com dados de mentira antes da noite do agente e antes da primeira sessão com pessoa.
2. **O agente não muda.** Prompt, biblioteca, busca, poda, cura e limiares ficam como estão na 21d; a noite só roda se o que identifica o agente bater com o que a 21d gravou.
3. **A primeira noite completa é a que vale.** Nenhuma corrida é repetida para melhorar o número. Relançar só retoma o que faltou.
4. **A mesma régua dos dois lados.** A falha é armada pelas mesmas funções, no mesmo navegador; o cronômetro começa e termina nos mesmos pontos; o que conta como corrigido é a mesma regra em código.
5. **Nenhum número digitado à mão.** O tempo das pessoas é gravado pela ferramenta, a planilha é preenchida a partir desse registro, e toda tabela sai de script com `--check`.
6. **Primeiro a máquina, depois o modelo.** Leitura, conferências e painel são código; o modelo só é chamado na noite medida, lançada pelo Eric.
7. **O que não foi medido fica dito.** Toda limitação da seção 12 entra no relatório da fase e no texto do TCC.
8. **Testes escritos antes** (`testar_fase5.py`, funções `teste_<nome>()`, runner que termina em `N testes ok`), tag e motivo em todo trecho, e nenhum teste com o banco durante a corrida.

## 3. A corrida do agente (corrida 28)

### 3.1 O que roda

Os dez cenários de `cenarios_fase4.CENARIOS_DO_ENSAIO`, com cinco repetições: 50 execuções, repetição por repetição, na ordem do catálogo. O banco é restaurado e conferido por hash no começo de cada repetição; os seis de contrato rodam na página que consome a CobaiaAPI, e os quatro de localizador, no front legado, com a quebra armada pelo harness no navegador. O executor é o do ensaio, sem mudança: `executar_fase4.py --modo cenarios --repeticoes 5`. A saída vai para `RA\fase5_agente\`, e a leitura do próprio ensaio aplicada a ela, para `RA\fase4\cenarios_fase5.{json,md}` (`-Nome cenarios_fase5`), sem tocar em nenhuma leitura da Fase 4.

**Justificativa.** São os cenários e as repetições que o projeto ABNT pede e que a decisão 79 fixou; o executor é o que as corridas 21 a 21d já exercitaram quatro vezes, e usar o mesmo código é o que deixa a noite comparável com o ensaio.

### 3.2 Tempo de máquina

Conta feita por script sobre os registros da 21d (rascunho `custo_fase5.py`, desta sessão; a versão versionada entra no pacote F1 como `avaliar_fase5.py --custo`): 50 execuções levam de 1,07 h (`tempo.estimativa_fase5_h`: 50 vezes a média de 76,7 s por execução) a 1,12 h (cinco vezes os 808 s do executor, contando o que ele gasta fora das execuções), mais a bateria de testes e a leitura, que na 21d somaram menos de um minuto. Se o Ollama tiver mudado de versão, a ponte entra antes, com cerca de 0h35 a 0h45 pelas três últimas. A noite inteira cabe em duas horas.

### 3.3 A ponte da versão do Ollama

Regra R6, sem mudança. A versão 0.40.16 já tem ponte (seção 1.3). O lançador confere a versão que está no ar na hora; se ela não tiver ponte completa em `pontes.json`, ele roda a ponte (`rodar_fase3b.ps1 -Modo ponte`, pasta `fase3b_ponte_<versão>`), grava a leitura (`avaliar_fase4.py --pontes`) e põe a pasta nova no registro das áreas só de leitura (`testar_fase4.py --registrar-ponte <pasta>`), como a fila de 11/11/2026 fez. Ponte não pareável (b + c acima de 2) para o lançador antes da corrida, e a decisão volta ao Eric numa ficha: a comparação com as pessoas não depende da ponte, mas "o agente como está na 21d" depende.

Se a versão mudar no meio da corrida, o `.ps1` já recusa a noite como medida (decisão 44). Nesse caso a pasta parcial é guardada com outro nome, como incidente, e a noite recomeça do zero numa pasta nova, com a ponte da versão nova: retomar misturaria duas versões nas 50 execuções.

### 3.4 O lançador

Arquivo novo `EXP\rodar_fase5.ps1` (UTF-8 com BOM, sem travessão nas strings), no molde de `rodar_fila_pre_fase5.ps1`. O Eric roda da janela dele, com o aplicativo Claude e o VS Code fechados e o notebook na tomada:

```
powershell -ExecutionPolicy Bypass -File "C:\Users\Eric.Derre\Documents\TCC\Programacao\AgenteCore\experimentos\rodar_fase5.ps1"
```

Etapas, parando na primeira que falhar, com o código dela:

1. Espera a memória livre chegar a 7,0 GB (o `rodar_fase4.ps1` exige 6,5 GB; a folga evita a queda na checagem dele, lição da corrida 18b) e confere que não há modelo residente.
2. Confere que o agente é o da 21d (`avaliar_fase5.py --antes`): biblioteca, prompt fixo, índice da busca, k, limiares e versão do navegador iguais aos de `RA\fase4_ensaio_v4\condicoes_fase4.json`. Diferença para aqui.
3. Ponte, se a versão do Ollama no ar não tiver (seção 3.3).
4. `rodar_fase4.ps1 -Modo cenarios -Saida fase5_agente -Repeticoes 5 -Nome cenarios_fase5 -Titulo "Fase 5: os dez cenários com cinco repetições (corrida 28)"`.
5. `avaliar_fase5.py --agente`, a leitura por cenário da seção 5.
6. O painel, uma vez, com as baterias dele.

Opções: `-Simular` só imprime os comandos, na ordem (é o que o teste do lançador usa); `-SemPainel`. Relançar retoma: as execuções já gravadas em `cenarios.jsonl` não rodam de novo.

### 3.5 Antes da noite, sem modelo

- A bateria `testar_fase5.py` e o teste do lançador com `-Simular` (a ordem das etapas, o `-Nome` sempre presente, a ponte antes da corrida).
- `avaliar_fase5.py --agente` rodado sobre a pasta da 21d, gravando numa pasta temporária: prova que a leitura nova lê um registro real e dá os mesmos 10 de 10 e 74,0 s da leitura vigente.
- `avaliar_fase5.py --antes`, que é a etapa 2 do lançador.

## 4. A sessão da linha de base manual

### 4.1 Quem participa

Três integrantes do grupo, cada um nos dez cenários, um por vez, na máquina-alvo, com o Eric como facilitador (`PROTO`, seção 4: quem conhece o catálogo dos modos de falha conduz e não resolve). Quem são, onde e até quando é a ficha 72. Antes de começar, cada integrante responde três perguntas, que ficam em `RA\fase5_manual\participantes.json` sem o nome (o repositório é público; a leitura fala em integrante 1, 2 e 3): quanto tempo de prática tem com teste ou com programação para a web; se já usou as ferramentas do desenvolvedor do navegador; e se já leu a lista dos dez cenários ou as causas esperadas no painel, no README, no documento do TCC ou no repositório. Quem já leu a lista não serve de integrante; se não houver substituto, participa e isso fica declarado na leitura. O autor do site legado conhece o HTML das quatro páginas dos cenários de localizador: se ele participar, o perfil dele diz isso.

### 4.2 O que cada um recebe

O que `PROTO` (seção 5) já fixa: a ficha da falha, o roteiro passo a passo, o contrato esperado e a lista das 23 causas nos cenários de contrato, e o navegador aberto no ponto em que o roteiro começa, com as ferramentas do desenvolvedor. A versão 2 do protocolo (ficha 73) acrescenta a definição de uma linha de cada causa, a do Apêndice A do documento do TCC: sem ela o tempo mediria a pessoa adivinhando o que o nome da causa quer dizer. A biblioteca do agente não é entregue: ela está no repositório, que a pessoa não pode abrir, e é parte do agente.

Pode e não pode ficam como em `PROTO`: navegar, inspecionar, ver a rede e consultar a documentação de seletores; sem código das cobaias, sem repositório, sem assistente de IA, sem conversa com outro integrante.

### 4.3 O roteiro do dia

Uma sessão por integrante, com cerca de duas horas reservadas: os dez cenários têm teto de 1h40 de cronômetro (dez vezes o limite de 10 minutos), e o resto é a abertura e o tempo de armar cada cenário.

1. **Abertura (10 min).** O facilitador lê um texto fixo: o que é medido, o que pode e o que não pode, o aviso da tela de login que volta sozinha em 30 s (`PROTO`, seção 4, item 6) e as três perguntas de perfil.
2. **Treino, sem cronômetro (15 min; ficha 73).** Um cenário de contrato fora dos dez (`latency`, o modo que saiu do catálogo pela troca da ficha 36) e um exercício de seletor numa página que não está nos quatro roteiros de localizador (o botão "Saiba mais" de `produtos_api.php`, sem quebra armada, conferido no console do navegador). Serve para a pessoa conhecer o material e a forma da resposta antes do primeiro cenário medido.
3. **Os dez cenários**, na ordem sorteada da planilha, com pausa livre entre um e outro (o cronômetro só corre com o cenário armado). Limite de 10 minutos por cenário, como em `PROTO`, seção 6.
4. **Fecho (5 min).** O facilitador anota o que fugiu do protocolo e pede à pessoa que não comente os cenários com os outros dois.

O facilitador não dá dica: as falas dele durante um cenário são as do texto fixo ("o tempo está correndo", "faltam dois minutos", "pode entregar quando quiser"), e qualquer outra coisa dita vai para as observações.

### 4.4 Como o tempo é cronometrado

Os pontos de começo e de fim são os de `PROTO`, seção 6, que espelham os do agente: começa quando o navegador do `armar` está aberto e a pessoa tem o material; no contrato, termina na entrega da causa e do campo, certa ou errada; no localizador, termina no `conferir` que diz "CORRIGIDO", descontado o tempo de restaurar o banco de cada tentativa.

O que muda na versão 2 (ficha 73) é quem anota. Hoje o facilitador copia a hora da tela para a planilha. A proposta é a ferramenta gravar cada evento, com a hora do relógio em milésimos, num registro da sessão (`RA\fase5_manual\sessao.jsonl`): o `armar` grava o início; um comando novo `entregar` grava o fim do cenário de contrato no instante em que o facilitador dá Enter, antes de digitar a causa e o campo, e confere que a causa está nas 23; o `conferir` grava cada tentativa de seletor, o resultado e os segundos do banco. No localizador a pessoa escreve o seletor num bloco de notas ao lado e o facilitador copia e cola. Um cronômetro de reserva (celular) e uma folha de papel correm em paralelo: se a ferramenta falhar num cenário, vale a anotação à mão, e a linha fica marcada como tal.

**Justificativa.** O MTTR do agente sai de relógio de máquina; anotar o das pessoas à mão põe, só de um lado, o erro de leitura e de cópia de 60 horários. Com o registro da ferramenta, o tempo das pessoas também não é digitado.

### 4.5 A planilha

Mesmas colunas e mesmo arquivo de `PROTO`, seção 8. Na versão 2 ela é preenchida por um comando novo, `linha_de_base_manual.py planilha`, a partir do registro da sessão: `inicio`, `fim`, `segundos`, `descontar_s`, `causa`, `campo`, `seletor`, `tentativas` e `corrigido`. O facilitador escreve só `observacoes`. O comando nunca troca uma célula já preenchida e avisa quando o registro e a planilha discordam.

### 4.6 A leitura da planilha por script

`avaliar_fase5.py --manual`, escrita com os testes antes. Ela lê a planilha (ponto e vírgula, BOM) e o registro da sessão, e recusa, dizendo a linha:

- planilha com menos de 30 linhas preenchidas (sai com código 2 e não mostra número nenhum, como a leitura da sessão de revisão);
- ordem, cenário ou tipo diferentes do sorteio;
- `segundos` que não seja o fim menos o início menos o desconto, com folga de 1 s;
- causa fora das 23, ou `corrigido` diferente do que a regra dá: no contrato, a própria leitura refaz a conta de `cenarios_fase4.task_success_contrato` com a causa e o campo entregues; no localizador, exige no registro da sessão um `conferir` que passou com o seletor da planilha;
- tempo acima do limite numa linha marcada como corrigida.

Os testes usam planilhas de mentira: uma completa, uma incompleta, uma com tempo que não fecha, uma com causa fora da lista, uma com estouro do limite, uma fora da ordem e uma com linha anotada à mão.

## 5. As regras de leitura, fixadas antes de qualquer medida

**L1. O que é uma medida.** Do agente, cada uma das 50 execuções (dez cenários, cinco repetições). Das pessoas, cada uma das 30 tentativas (dez cenários, três integrantes). Uma pessoa não repete cenário, porque depois da primeira vez já sabe a resposta.

**L2. A unidade é o cenário.** As cinco repetições do agente no mesmo cenário não são independentes (mesmo prompt, temperatura 0,1: na corrida 21b o rótulo se repetiu nos dez cenários), e os três integrantes resolvem a mesma falha. Por isso todo intervalo do tempo e todo veredito tratam o cenário como a unidade, com dez cenários, seis de contrato e quatro de localizador. Contar as 50 execuções como 50 medidas independentes daria intervalos estreitos demais. É a ficha 74.

**L3. MTTR do agente.** Por execução, o `mttr_s` que o executor grava: da detecção ao diagnóstico conferido em código (contrato) ou à reexecução validada, descontada a restauração do banco (localizador). Por cenário, a média das repetições que chegaram ao fim, com o mínimo e o máximo ao lado. No geral e por tipo, a média das médias dos cenários.

**L4. Tempo das pessoas.** Por tentativa, o fim menos o início menos o desconto. Por cenário, a média dos integrantes que chegaram ao fim, com o mínimo e o máximo. No geral e por tipo, a média das médias dos cenários.

**L5. Task Success.** Do agente, execuções com Task Success sobre 50; das pessoas, tentativas corrigidas sobre 30; no geral e por tipo, com intervalo de Wilson de 95%. Ao lado, a contagem por cenário: em quantos dos dez o agente acertou as cinco repetições, e em quantos os três integrantes acertaram.

**L6. Quem não chega ao fim.** Execução do agente sem fim de cronômetro e tentativa que estoura os 10 minutos ficam fora da média do tempo e dentro do Task Success, como `PROTO` já diz. A leitura traz uma segunda conta, declarada como piso: cada medida sem fim entra com 600 s, dos dois lados.

**L7. Os intervalos.** Task Success: Wilson de 95%. Tempo médio (agente, pessoas e a diferença): reamostragem dos cenários, 2000 reamostras, semente 20261104, sorteando dentro de cada tipo para a mistura de seis e quatro não mudar; o intervalo são os percentis 2,5 e 97,5 (`avaliar_fase4.bootstrap_media`). Por cenário não há intervalo: com cinco ou três medidas mostram-se o mínimo, a média e o máximo.

**L8. A comparação do tempo.** Por cenário, a diferença entre o tempo das pessoas e o MTTR do agente, e a razão entre os dois. No geral: a média das dez diferenças com o intervalo da L7, a razão entre as duas médias, e o teste exato dos sinais, bicaudal, sobre os dez cenários, que é a mesma conta binomial do McNemar exato que o projeto já usa (`avaliar.mcnemar_exato`), com um lado para os cenários em que o agente foi mais rápido e o outro para os em que as pessoas foram. Cenário em que a diferença das médias é menor que 5 s, a folga do cronômetro das pessoas, conta como empate e sai do teste. Cenário em que só um lado chegou ao fim conta para esse lado no teste e fica fora da média das diferenças.

**L9. O que conta como diferença.** A leitura só afirma que um lado repara mais rápido quando o intervalo de 95% da diferença média não contém zero e o teste dos sinais dá p abaixo de 0,05. Com dez cenários e nenhum empate, isso pede nove ou dez cenários na mesma direção (p = 0,0215 e p = 0,002; com oito de dez, p = 0,1094). Se o intervalo contém zero, a diferença está dentro do ruído. Se o intervalo não contém zero mas o teste não chega a 0,05, a leitura diz que a média pende para um lado sem que a direção se repita em cenários suficientes, e não dá veredito. Nos três casos os números são mostrados.

**L10. Por tipo de cenário, sem veredito.** Com seis cenários o teste só chega a 0,05 com seis de seis (p = 0,0312), e com quatro nunca chega (quatro de quatro dá p = 0,125). Contrato e localizador são mostrados lado a lado, com os intervalos, e o texto não afirma diferença por tipo.

**L11. A comparação do Task Success.** Os dois números lado a lado, com Wilson. Por cenário, a parcela do agente (sobre cinco) menos a das pessoas (sobre três); o teste dos sinais sobre os cenários em que as duas parcelas diferem. Com menos de seis cenários diferentes o teste não tem como chegar a 0,05 (cinco de cinco dá p = 0,0625), e a leitura diz que não há veredito.

**L12. O ruído de cada lado.** A tabela por cenário mostra a amplitude entre as repetições do agente e a amplitude entre as pessoas, e diz se as duas faixas se cruzam. É descrição, não regra de veredito.

**L13. O que é só descrição.** O tempo das pessoas pela posição na ordem (do primeiro ao décimo cenário de cada uma), para mostrar o aprendizado; o tempo total da execução do agente, que inclui a detecção; a segunda leitura do tempo só com as medidas que tiveram Task Success, que é a leitura estrita da definição do projeto ABNT; o rótulo do diagnóstico em cada repetição.

**L14. O que anula uma medida.** Só uma falha do protocolo anotada na hora, antes de qualquer número ser lido: máquina que travou, falha armada errado, interrupção de fora. O facilitador marca a linha como anulada nas observações; a leitura conta as anuladas à parte e não as substitui. Do lado do agente, nenhuma execução é anulada: o que falhar aparece como falhou.

**L15. Nada é escolhido depois.** As contas das regras L3 a L11 são as do código testado antes da noite; uma conta que só for pensada depois de ver os números entra no relatório marcada como exploratória.

## 6. Para onde vai o resultado

- **Registros.** `RA\fase5_agente\` (a corrida 28), `RA\fase5_manual\` (registro da sessão e perfil dos integrantes), a planilha em `DOC\5-metodo-e-ferramental\`, e os derivados em `RA\fase5\`: `agente.{json,md}`, `manual.{json,md}` e `medicao.{json,md}`, por `avaliar_fase5.py`, com `--check` e blocos `tb_f5_*`.
- **Painel.** Aba nova no grupo "Fase 5" de `FER\painel_topicos.py` (`NAV`, depois de `f-5`), com o id `medicao`: a pergunta no título ("O agente repara mais rápido que uma pessoa, e resolve tantos cenários quanto ela?"), a resposta em uma frase (em `FER\painel_leituras.py`), cartões com o MTTR do agente, o tempo das pessoas, a razão e o Task Success dos dois, dois gráficos (o tempo por cenário dos dois lados, com a faixa entre o mínimo e o máximo; o Task Success por cenário), o "Como ler" de cada um, a leitura curta e as tabelas completas recolhidas. Antes das medidas a aba mostra o que vai ser medido e as regras desta seção. Em `FER\painel_fases.py`: a faixa `(28, 28, "Fase 5")` em `FAIXAS_DE_CORRIDAS`, os passos da visão `f-5` apontando para a aba nova e, quando o README ganhar a descoberta, a entrada dela em `DESCOBERTAS`. Em `FER\painel_glossario.py`: o teste dos sinais, com o resumo, o que o projeto faz de diferente e a fonte original, conferida antes de entrar em `referencias.md`.
- **Relatório da fase.** `DOC\3-resultados-e-analises\fase-5-relatorio.md`: o que a fase perguntou e respondeu, como rodou, o agente, as pessoas, a comparação pelas regras L8 a L11, as limitações e o que o documento do TCC precisa carregar, com os blocos colados por `--colar`.
- **Documento do TCC** (`Documentacao\TCC - ABNT 14724 - V1.md`): o resumo e o abstract (o resultado central); a seção 5.1 (a etapa passa a concluída); a 5.7 (as regras desta seção, com o teste dos sinais resumido e citado na chamada); uma seção nova da Fase 5 depois da 6.7, com o gráfico e o "Como ler"; a Discussão (as limitações da seção 12); os dados crus na Análise aprofundada; a Conclusão (a resposta ao quinto objetivo e à expectativa da seção 4 do projeto ABNT); o glossário. A seção nova empurra a numeração da Discussão e da Análise aprofundada em uma casa, e a regra de `.claude/rules/documentacao.md` que cita a seção 6.9 muda junto. A figura sai de `gerar_figuras_documentos.py`.
- **README e roadmap.** A descoberta nova em "O que já descobrimos", com a figura; a linha da Fase 5 no §1, a corrida 28 no §2, a leitura no §2.26 e o §5.

## 7. Decisões do Eric: fichas 72 a 75

| Ficha | Decisão | Recomendação | Pacote |
|---|---|---|---|
| 72 | Quem faz a linha de base manual, onde e até quando | três integrantes do grupo que não leram a lista dos cenários, um por vez, na máquina-alvo, com o Eric de facilitador, até 24/11/2026 | F4 |
| 73 | O protocolo da sessão ganha a versão 2 antes de as sessões serem marcadas | sim, com as três mudanças: o tempo gravado pela ferramenta, o treino sem cronômetro e as perguntas de perfil com a definição das causas | F2 |
| 74 | A regra que diz se um lado foi mais rápido | o cenário como unidade, com o intervalo por reamostragem dos cenários e o teste dos sinais; por tipo, sem veredito | F1 |
| 75 | A aprovação deste plano | aprovar como está | F0 |

## 8. Pacotes, em ordem

Cada pacote com código segue o molde das fases anteriores: teste escrito e visto falhar pelo motivo certo antes do código, tag e motivo em todo trecho, nenhum número digitado à mão, hash das áreas só de leitura igual antes e depois.

### F0. Aprovação e registro (esta sessão; sem máquina)
Este plano, as fichas 72 a 75, a decisão do Eric, o texto congelado em `plano-aprovado-fase-5.md`, o roadmap e o painel. Nenhum código.

### F1. A leitura da Fase 5 e o lançador da noite (uma sessão; sem modelo)
- `EXP\avaliar_fase5.py`: `--custo`, `--antes`, `--agente`, `--manual`, `--comparar`, com `--check` e `--colar`; `EXP\testar_fase5.py`; `EXP\rodar_fase5.ps1` com `-Simular`.
- **Testes escritos antes:** a média por cenário e a média das médias; a reamostragem por tipo com semente fixa; o teste dos sinais com empate e com um lado sem fim; as frases da regra L9 nos três casos; a segunda conta com 600 s; a leitura da planilha (seção 4.6); o lançador simulado.
- **Entrega:** a leitura rodando sobre a pasta da 21d e sobre planilhas de mentira, sem gravar em `RA\fase5\`.
- **Depende de:** ficha 74.

### F2. O protocolo versão 2 e o ajudante (uma sessão; cobaias e navegador, sem modelo)
- `linha_de_base_manual.py` ganha o registro da sessão, `entregar`, `treino`, `planilha` e o perfil dos integrantes; `PROTO` passa à versão 2; o texto fixo do facilitador e a folha do integrante, com a definição das 23 causas, saem por comando, para não serem digitados.
- **Testes escritos antes:** o registro grava início, entrega e cada tentativa; `entregar` recusa causa fora das 23; `planilha` nunca troca célula preenchida; a ficha da falha continua igual à da 21d; o treino não usa nenhum dos dez cenários.
- **Entrega:** a fumaça com as cobaias reais, sem modelo, e o ensaio do facilitador: o Eric roda os dez cenários uma vez pelo nome, sem cronômetro (`PROTO`, seção 4, item 3).
- **Depende de:** ficha 73. Pode correr em paralelo com o F1: os arquivos não se cruzam.

### F3. A noite medida, corrida 28 (máquina; cerca de 1h10, até 2 h com a ponte)
O Eric lança o `rodar_fase5.ps1` da janela dele. Depende do F1 e da máquina livre. Não depende das pessoas.

### F4. As três sessões da linha de base (pessoas; cerca de 2 h cada)
Uma por integrante, com o Eric de facilitador, na máquina-alvo. Depende do F2 e da agenda dos três (ficha 72). Não depende da noite do agente: a ficha da falha vem do ensaio.

### F5. Leitura, painel e relatório da fase (uma sessão; sem máquina)
`avaliar_fase5.py --manual` e `--comparar`, a aba `medicao`, a faixa das corridas, o glossário, `fase-5-relatorio.md`, o roadmap, o README e a figura. Antes de registrar quem participou e quem facilitou, a pergunta ao Eric sobre quem de fato fez cada sessão. Depende do F3 e do F4.

### F6. As seções da Fase 5 no documento do TCC (uma sessão; sem máquina)
O texto das seções listadas na seção 6, com os números copiados por script e um revisor. O arquivo Word é regerado uma vez só, junto com o que o pacote Q8 da Pós-Fase 4 deve ao documento.

## 9. Corrida prevista (entra no roadmap §2 depois da aprovação)

| # | Corrida | Comando (em `EXP`) | Inferências e tempo estimado | Pré-requisito | O que fecha |
|---|---|---|---|---|---|
| 28 | A noite da Fase 5: os dez cenários com cinco repetições | `powershell -ExecutionPolicy Bypass -File rodar_fase5.ps1` (chama `rodar_fase4.ps1 -Modo cenarios -Saida fase5_agente -Repeticoes 5 -Nome cenarios_fase5`) | 50; de 1,07 h a 1,12 h pela corrida 21d, mais a ponte se o Ollama tiver mudado de versão | pacote F1; a máquina livre; ponte da versão do Ollama | o MTTR e o Task Success do agente |

As sessões das pessoas não são corrida e não levam número: entram no §5 do roadmap, com a data de cada uma.

## 10. Calendário

As reuniões com o orientador são às quartas e sextas, às 13h, até 02/12/2026.

| Data | O que acontece | Depende de |
|---|---|---|
| seg 16/11 | F0: plano apresentado, fichas respondidas | Eric |
| ter 17/11 | F1 e F2, em duas sessões | Claude |
| qua 18/11 | reunião: o plano e a data das sessões; ensaio do facilitador; à noite, a corrida 28 | Eric e a máquina |
| qui 19/11 a ter 24/11 | F4: as três sessões, uma por integrante | os três integrantes e o Eric |
| sex 20/11 | reunião: o agente já medido | |
| qua 25/11 | F5: leitura, painel republicado e relatório; reunião com o resultado | Claude |
| qui 26/11 e sex 27/11 | F6: as seções no documento; reunião de sexta com o texto | Claude e o Eric |
| sáb 28/11 a ter 01/12 | folga: sessão que atrasou, leitura do grupo, o Word | |
| qua 02/12 | última reunião | |

Ponto de controle em 24/11: se faltar sessão, o Eric decide numa ficha entre esperar até 27/11, usando a folga, ou fechar a leitura com quem fez, declarado como desvio.

## 11. Riscos e salvaguardas

| Risco | Salvaguarda |
|---|---|
| O Ollama se atualiza antes da noite ou no meio dela | Regra R6 no lançador; versão conferida antes e depois pelo `.ps1`; se mudar no meio, a pasta parcial vira incidente e a noite recomeça em pasta nova (seção 3.3) |
| A ponte da versão nova não é pareável | O lançador para; a decisão volta ao Eric numa ficha |
| Memória: o modelo pede 6,5 GB livres | Aplicativo Claude e VS Code fechados; o lançador espera 7,0 GB |
| O notebook dorme ou hiberna no meio da noite | Na tomada e com a suspensão desligada pelo Eric antes de lançar; relançar retoma |
| A leitura do ensaio gravar por cima da leitura da corrida 21 | O lançador passa sempre `-Nome cenarios_fase5`, e o teste dele confere |
| O código de hoje não ser o agente da 21d | `avaliar_fase5.py --antes` compara o que identifica o agente com `condicoes_fase4.json` da 21d e para se diferir |
| Algo usar o MariaDB durante a corrida | Nada roda em paralelo: nem bateria de testes, nem sessão do Claude com as cobaias, nem sessão com pessoa |
| Faltar integrante ou data | Ficha 72 com data-limite; ponto de controle em 24/11; folga de 28/11 a 01/12 |
| Integrante que já leu a lista dos cenários | As perguntas de perfil antes da sessão; substituto; se não houver, participa e fica declarado |
| A ferramenta falhar durante uma sessão | Cronômetro de reserva e folha de papel; a linha fica marcada como anotada à mão |
| O facilitador ajudar sem querer | Falas fixas; tudo o mais vai para as observações |
| Um cenário travar para a pessoa por defeito do ambiente | Regra L14: anulado na hora, contado à parte, sem substituição |
| Duas sessões do Claude na mesma pasta | F1 e F2 com arquivos disjuntos; reler antes de editar; roadmap e painel só na sessão que fecha |
| O calendário dividido com os pacotes Q6 a Q8 | A Fase 5 tem prioridade até 25/11; o que os outros pacotes fazem nesse intervalo é decisão fora deste plano |

## 12. Limitações declaradas

1. A falha é armada, não ocorrida, dos dois lados.
2. A pessoa parte da ficha que a detecção do agente escreveu: a detecção não é medida na pessoa, e o MTTR do agente também começa depois dela.
3. Nos seis cenários de contrato, corrigido quer dizer diagnosticado: causa e campo certos, sem conserto da API (ficha 35). A pessoa escolhe a causa numa lista fechada de 23, como o agente.
4. O agente lê a biblioteca dele; a pessoa conta com o que sabe e com a definição de uma linha de cada causa.
5. Três integrantes dão três tempos por cenário, e são estudantes do grupo que fez o projeto, não analistas de teste de fora. A ordem sorteada e o treino espalham o aprendizado, mas não o eliminam.
6. As cinco repetições do agente não são independentes; por isso a unidade é o cenário, e são dez.
7. Os dez cenários foram escolhidos pelo grupo, e os seis de contrato estão numa página só, quatro deles no mesmo campo (`preco`).
8. A quebra de localizador do agente é armada pelo harness, e a das pessoas, pela variante do PHP; a corrida 19 mediu as duas formas iguais nas 16 células.
9. O tempo do agente é o desta máquina, só em CPU; em outra máquina ele muda, e o da pessoa não.
10. O cronômetro das pessoas inclui o tempo de dizer a resposta e de o facilitador dar Enter, e a regra L8 trata diferença menor que 5 s como empate.
11. O limite de 10 minutos corta o tempo de quem não termina; a segunda conta da regra L6 é um piso.
12. O facilitador é o autor do projeto.
13. A noite roda sem o trace na falha (decisão 93) e com a barra de progresso ligada.
14. Com dez cenários, o teste só separa os lados quando quase todos apontam na mesma direção, e por tipo não há veredito.

## 13. Fora do escopo

Mudar o agente (prompt, biblioteca, busca, poda, cura, limiares); cenários novos ou mais repetições; uma segunda noite para medir a variação entre noites; integrantes de fora do grupo, salvo a ficha 72 dizer outra coisa; medir a detecção na pessoa; cura de contrato do lado do teste (ficha 35, opção b, não escolhida); o trace na falha, o hub, a integração com o Git e o relatório da Pós-Fase 4 (decisões 93 e 101; pacotes Q6 a Q8); gerar o arquivo Word; qualquer mudança no front PHP legado ou nas áreas só de leitura.

## 14. Verificação fim a fim

1. `PYTHONIOENCODING=utf-8 python EXP\testar_fase5.py` e as baterias anteriores (`testar_fase3.py`, `testar_fase3b.py`, `testar_pre_fase4.py`, `testar_fase4.py`, `testar_pos_fase4.py`): todas ok, com o hash das áreas só de leitura igual antes e depois.
2. `--check` limpo em `avaliar_fase5.py` (`--custo`, `--agente`, `--manual`, `--comparar`) e nos já existentes.
3. `RA\fase5_agente\`: 50 execuções em `cenarios.jsonl`, uma versão do Ollama e uma do navegador, o mesmo hash do banco no começo das cinco repetições, e a linha FIM no `fase4.log`.
4. A planilha com as 30 linhas, aceita por `avaliar_fase5.py --manual`, e o registro da sessão ao lado.
5. `python FER\gerar_dashboard.py`, as cinco baterias do painel (`testar_painel_textos.py`, `testar_painel_topicos.py`, `testar_painel_fases.py`, `testar_painel_glossario.py`, `testar_painel_grupo.py`), a aba nova conferida nos dois temas e em largura de celular, e o painel republicado no mesmo endereço.
6. `python FER\conferir_docs.py`: tudo ok; `git status` lista só o previsto; o Eric commita.

## 15. Rastreabilidade

| O quê | Onde |
|---|---|
| Método | projeto ABNT (`Documentacao\Projeto de Pesquisa - ABNT 15287_2025 - V3.md`), seção 3.4: definições operacionais, linha de base, volume e determinismo, inferência estatística |
| O que a Fase 4 deixou pronto | `claude-memoria\plano-aprovado-fase-4.md`, seção 3.9 e pacote P6; `DOC\3-resultados-e-analises\fase-4-relatorio.md`, seções 8 e 11 |
| Ordem das fases | `claude-memoria\plano-aprovado-pos-fase-4.md`, seções 7 a 9 |
| Decisões | `DOC\1-decisoes-e-historico\decisoes.md`: 44, 47, 79, 93, 94, 97, 99, 101 e 107 |
| Fichas | `DOC\pendencias.md`: 35 e 36 (fechadas), 72 a 75 |
| Roadmap | `DOC\roadmap.md`: §1 (linha da Fase 5), §2 (corridas 21 a 21d), §2.20, §5 e §6 |
| Protocolo e planilha | `PROTO`; `DOC\5-metodo-e-ferramental\planilha-linha-de-base-manual.csv` |
| Código lido | `EXP\cenarios_fase4.py`, `linha_de_base_manual.py`, `executar_fase4.py` (modo `cenarios`), `avaliar_fase4.py` (`--cenarios`, `bootstrap_media`), `avaliar.py` (`wilson`, `mcnemar_exato`), `rodar_fase4.ps1`, `rodar_fila_pre_fase5.ps1`, `testar_fase4.py` (`--registrar-ponte`); `FER\painel_topicos.py`, `painel_fases.py`, `painel_glossario.py` |
| Números citados | `RA\fase4\cenarios_v4.json` (`geral`, `por_tipo`, `tempo`, `prompt`, `navegador`, `banco`); `RA\fase4_ensaio_v4\cenarios.jsonl`, `condicoes_fase4.json`, `fase4.log` e `qwen2.5_7b\diagnosticos__cenarios.jsonl`; `RA\fase4\pontes.json`; `fase3b.log` das pastas `fase3b_ponte_04014`, `04015` e `04016`; os valores de p da seção 5, de `avaliar.mcnemar_exato` |
| Livro-razão | `SDD\progress.md` (fora do git), a abrir no F1 |

<!-- ! Alteração de IA - Revisar: anexo novo (25/11/2026, fechamento da Fase 5, ficha 96 e decisão 156) com os desvios do plano, copiados por script do livro-razão da fase (`.superpowers/sdd/fase-5/progress.md`, seção "Desvios do plano"), e uma linha de estado nova no alto do arquivo.
     ! Motivo: o rito das fases congela o texto aprovado e manda o que desviou dele para um anexo no fechamento; sem o anexo, quem lê o plano acharia, por exemplo, que as sessões foram presenciais, que a noite do agente foi a corrida 28 e que os três integrantes foram os previstos. O texto do plano acima não mudou uma letra. -->
## Anexo: desvios do plano (fechamento da fase, 25/11/2026)

A Fase 5 foi fechada em 25/11/2026 (ficha 96, decisão 156), com os pacotes F0 a F6 feitos. O texto aprovado acima não foi reescrito. O que a execução fez de diferente dele está abaixo, na ordem em que aconteceu, como o livro-razão da fase registrou; entre parênteses, o pacote ou a decisão de cada um. O resultado da fase e as limitações estão no [relatório da fase](../Documentacao/memorial/3-resultados-e-analises/fase-5-relatorio.md).

1. A faixa `(28, 28, "Fase 5")` de `painel_fases.FAIXAS_DE_CORRIDAS`, que a seção 6 do plano punha no pacote F5, entrou no F0: `testar_painel_fases.py` recusa corrida do roadmap sem fase, e a corrida 28 entra no roadmap depois da aprovação (seção 9 do plano).
2. Dois consertos no painel que a linha 28 do roadmap pediu, fora da lista de entregas do plano: `painel_topicos._corridas_que_faltam_f4` passou a parar na corrida 27 (a aba "Fechamento da fase" dizia que a corrida 28 faltava antes da Fase 5), com o teste escrito antes; e a linha da Fase 5 na tabela de estado do README passou a "Em andamento" (a visão da fase mostrava "Em andamento" e "Não iniciada" ao mesmo tempo).
3. (F1) Uma sexta opção em `avaliar_fase5.py`, `--situacao`, e uma guarda na etapa 4 do lançador, fora das seis etapas da seção 3.4: com as 50 execuções gravadas, o `rodar_fase5.ps1` não chama a corrida de novo. Motivo: a primeira noite completa é a que vale, e o relançamento da corrida 25 em 16/11 regravou `condicoes_fase4.json` com a versão do Ollama do relançamento.
4. (F1) `--antes`: param a noite os seis itens que a seção 3.4 lista (biblioteca, prompt fixo, índice da busca, k, limiares, navegador). Outros seis campos das condições (modelo, `top_logprobs`, teto de tokens, Playwright, versão do caso ao vivo, sinais da referência na busca) aparecem na tabela e só informam. Dos limiares sai `gravado_em`, que é a data do arquivo.
5. (F1) Regra L9, caso que o plano não escreve: o intervalo não contém zero e o teste dá p abaixo de 0,05, mas a maioria dos cenários aponta para o lado contrário ao da média. A leitura trata como "a média pende, sem veredito", que é a saída conservadora.
6. (F1) A segunda conta da regra L6 traz, além dos números, o que a regra L9 daria nela, com o rótulo de que não é o veredito da leitura.
7. (F1) Leitura da planilha, além da lista da seção 4.6: linha anulada é a que começa as observações com `ANULADA`; tempo acima de 600 s numa linha não corrigida conta como sem fim (protocolo, seção 6); linha sem `fim` com `segundos` ou com `corrigido` = sim é recusada; a marca de anotada à mão dispensa só o `conferir` no registro, e a regra do contrato é refeita do mesmo jeito; planilha regravada pelo Excel em cp1252 é lida assim.
8. (F1) O `rodar_fase5.ps1` tem uma linha com acento (o título da leitura, como o plano escreve); os outros lançadores são só ASCII. O teste confere o BOM e que só essa linha tem acento.
9. (F1) `DETALHES-TECNICOS.md` ganhou as linhas dos três arquivos novos, fora da lista de entregas do pacote.
10. (F2) A definição de uma linha de cada causa não veio do Apêndice A do documento do TCC, como a seção 4.2 do plano e a ficha 73 dizem: o Apêndice A só traz os 23 nomes e a descrição das seis classes. As 23 linhas foram escritas no pacote, em `linha_de_base_manual.DEFINICAO_DAS_CAUSAS`, sem citar campo, página ou a forma de armar a falha, e viraram a ficha 76, fechada em 16/11 pela opção (a) (decisão 134): ficam como foram escritas, e no F6 o Apêndice A ganha a mesma coluna.
11. (F2) As falas fixas são sete, e não as três da seção 4.3: às três do plano somam-se quatro que só repetem o que a ferramenta mostrou (causa fora da lista, seletor que não passou, seletor que passou, tempo esgotado). Sem elas o facilitador improvisaria a frase a cada resposta do `entregar` e do `conferir`.
12. (F2) O fim do contrato são dois eventos no registro, e não um: `entrega` (a hora do Enter, gravada na mesma hora) e `resposta` (a causa, o campo e o corrigido, depois de digitados). Se o comando cair entre os dois, o próximo `entregar` pede só a causa e o campo daquele Enter. Linha vazia no pedido da causa desfaz a entrega (o integrante entregou algo fora da lista) e o tempo segue.
13. (F2) Na planilha, `segundos` e `descontar_s` saem com vírgula decimal (o Excel em português lê `83.417` como 83417), e `inicio` e `fim` continuam em `HH:MM:SS`: os milésimos e a data ficam no registro. Por isso um cenário não pode atravessar a meia-noite, e `segundos` pode diferir em menos de 1 s da conta feita com as horas da planilha (é a folga de 1 s da seção 4.6).
14. (F2) O `entregar` não mostra na tela se a resposta está certa, e o `planilha` é rodado depois que o integrante sai: na versão 1 o corrigido do contrato já era preenchido depois da sessão, e saber se acertou um cenário muda o que a pessoa responde nos seguintes.
15. (F2) Fora da lista de entregas do pacote: o comando `ensaio` (o passo a passo do ensaio do facilitador, com os comandos montados do catálogo e um seletor que conserta cada cenário de localizador, `SELETOR_DO_ENSAIO`); o aviso do limite pela janela do `armar` (um fio que lê o registro a cada segundo e imprime a fala dos dois minutos e a do tempo esgotado); a recusa de gravar o registro sem `RESULTADOS_DIR=resultados_alvo`; a leitura da planilha em cp1252; o aviso no começo da seção 9 do protocolo (as regras de leitura são as do plano); as linhas em `DETALHES-TECNICOS.md`.
16. (F2) O perfil tem, além das três perguntas, a anotação do facilitador `conhece_o_codigo_das_cobaias` (com `o_que_conhece`), pedida pela sessão do plano em 16/11. Consequência a declarar na leitura: o repositório cita pelo nome o autor do site legado, então o número do integrante que levar essa anotação deixa de ser anônimo.
17. (F2) O roadmap e o painel foram editados pela sessão do F2, e não só "na sessão que fecha" (seção 11 do plano, risco das duas sessões na mesma pasta): cada arquivo foi relido antes de ser gravado, e o F1 já tinha fechado a parte dele.
18. (decisão 135) Os integrantes recebem um tutorial antes da sessão, que o plano não previa (a seção 4.2 dava a ficha, o roteiro, o contrato, a lista das causas com a definição e o navegador). Muda a limitação 4 da seção 12: a pessoa conta com o que sabe, com a definição das causas e com o tutorial. O tutorial ensina o uso das ferramentas do navegador e os jeitos de escrever um seletor, com exemplos de fora das cobaias; a regra de envio (os três no mesmo dia, antes da primeira sessão) foi escrita no protocolo pela sessão do F2 e não foi perguntada ao Eric numa ficha. A bateria `testar_linha_de_base.py` tem 20 testes desde então.
19. (decisão 136) As sessões da linha de base manual deixam de ser presenciais, na máquina-alvo e com o Eric de facilitador (seção 4 do plano; decisões 130 e 131), e passam a ser feitas por uma página publicada, uma por integrante, com o material de cada cenário capturado antes nesta máquina. Mudam as limitações da seção 12: a pessoa lê o registro em vez de investigar o site no ar (itens 2 e 4); não há facilitador ao lado, e as regras viram um combinado (item 12 deixa de valer como estava); o navegador, o aparelho e o relógio são os de cada um (itens 9 e 10); o seletor é só CSS, conferido na hora contra uma fotografia do HTML, com o roteiro de verdade rodado na importação. O protocolo foi à versão 3 (seção 11), e a forma presencial ficou como reserva. A corrida 28, a leitura (regras L1 a L15) e o formato do registro não mudam.
20. (adiantamento do F6) Parte do pacote F6 foi escrita em 16/11, antes da corrida 28 e das sessões, e não em 26 e 27/11 como o calendário da seção 10 do plano: o Apêndice A com a coluna das explicações, o método da linha de base e as regras de leitura na seção 5.7, as limitações conhecidas na seção 6.8 e seis entradas do glossário. O que depende dos números continua no F6. Consequência: o método da linha de base está escrito como o que o protocolo versão 3 prevê, e o F6 o acerta com o que de fato aconteceu.
21. (adiantamento do F6) No documento do TCC, a justificativa da regra L2 não repete a frase do plano "na corrida 21b o rótulo se repetiu nos dez cenários": diz que, quando o ensaio dos dez cenários foi repetido, o rótulo do diagnóstico se repetiu de uma corrida para a outra, e o comentário de origem aponta a linha da corrida 21c no roadmap §2 ("o rótulo igual ao da 21b em 10 de 10 cenários"), que é onde a repetição está registrada. O número fica só no comentário, porque os números da corrida 21c no documento são do pacote Q8.
22. (adiantamento do F6) A tabela das 23 causas do Apêndice A mudou de forma (de quatro colunas, em duas metades, para três), e não só ganhou uma coluna, como a decisão 134 diz: com a explicação ao lado, as duas metades não cabem na largura do texto.
23. (parte do F5 adiantada) A aba `medicao`, os passos da visão `f-5`, o teste dos sinais no glossário com a referência e o esqueleto do relatório da fase foram feitos em 16/11, antes do F3 (a corrida 28) e do F4 (as sessões); o plano põe o F5 em 25/11, depois dos dois. Ficou para 25/11 o que depende dos números.
24. (parte do F5 adiantada) Os dois gráficos da aba existem antes das medidas, com o lado ainda não medido fora do primeiro e como "por medir" no segundo: `testar_painel_topicos.py` exige uma leitura para todo gráfico e um gráfico para toda leitura. A resposta em uma frase escrita à mão em `painel_leituras.RESPOSTA_SIMPLES`, que a seção 6 do plano prevê, não foi escrita: o parágrafo do alto é gerado do estado dos arquivos e, com `medicao.json`, é a frase das regras L9 e L11.
25. (parte do F5 adiantada) Campo que o derivado não traz: antes das medidas só existe `custo.json`, sem as constantes das regras nem a lista dos cenários. A aba lê as constantes do texto do código (`EMPATE_S`, `ALFA` e `REPETICOES` de `avaliar_fase5.py`; `LIMITE_S` e `INTEGRANTES` de `linha_de_base_manual.py`; `REAMOSTRAS` e `SEMENTE_DA_REAMOSTRAGEM` de `avaliar_fase4.py`), com um teste que as compara com as do módulo, e os cenários, os integrantes e as linhas preenchidas, da planilha. Nenhum derivado ganhou campo, e a aba não faz conta de comparação: sem `medicao.json` não há razão, diferença nem frase.
26. (parte do F5 adiantada) `avaliar_fase5._fechar`, do F1, mudou: o `--check` com `--pasta` fora da pasta oficial não compara mais os blocos do relatório da fase. Não é regra de leitura. Fica por fazer, sem teste: `--colar` com `--pasta` fora da oficial ainda colaria no relatório uma leitura que não é a oficial.
27. (parte do F5 adiantada) O relatório nasceu com os blocos do agente, das pessoas e da comparação vazios. Até o `--colar` de cada leitura, o `--check` oficial dela sai com "blocos divergentes em fase-5-relatorio.md": a ordem é `--colar` e depois `--check`.
28. (F3, corrida 28) A noite levou 31 minutos, e não os 68 da seção 3.2 do plano: o plano não previu que o Ollama reaproveitaria, nas repetições 2 a 5, o prompt lido na repetição 1. A regra L2 (média das cinco repetições) dá 30,5 s; só a repetição 1, 64,4 s nos nove cenários com fim. O efeito no MTTR levou às fichas 84 e 86.
29. (F3, decisões 145 e 146) A corrida 28 foi lançada com o aplicativo Claude aberto (parado), contra a regra da medição do plano (seção 1.2), e o Eric decidiu refazer a noite: a corrida 28 fica como incidente e a corrida 28b roda em pasta nova, com tudo fechado e a frio (uma repetição por vez, o modelo descarregado entre elas). Contraria a frase do plano "a primeira noite completa é a que vale" (princípio 3): a noite nova não foi pedida para melhorar o número, e a frio o agente fica mais lento. O lançador e a leitura mudam (pasta nova, uma repetição por vez, conferência de que a noite foi a frio), com o teste antes do código.
30. (corrida 28b) Entraram com a noite a frio, todos com o teste antes: a conferência a frio na leitura (validade da noite, e não regra de comparação; o limite foi fixado sobre os registros da corrida 28, antes da noite nova), com a leitura oficial recusando a noite que não for completa e a frio; a sondagem do frio como condição para o lançador começar a corrida, na versão do Ollama que está no ar; a retomada pela primeira repetição incompleta; a leitura da corrida 28 guardada à parte (`--incidente 28`, seção 11 do relatório da fase); e a recusa de `--colar` com `--pasta` fora da pasta oficial. A estimativa de 68 minutos de `custo.json` ficou como está: com as cinco chamadas são cerca de 70.
31. (F4, decisão 149) A linha de base não foi feita pelos três integrantes da decisão 130: um deles respondeu que já tinha lido a lista dos cenários e foi substituído por um quarto integrante do grupo, na mesma página; vieram quatro códigos para três páginas, e o da sessão substituída ficou guardado sem ser importado.
32. (F4, decisão 150) A sessão da página 2 entrou com a pessoa tendo lido a lista dos cenários e sem o treino de seletor (plano, seção 4.3).
33. (F4) As sessões aconteceram de 18 a 24/11/2026, e não de 19 a 24/11/2026, e as datas não chegaram a ser marcadas antes.
34. (F5) A leitura das pessoas e a comparação rodaram em 24/11/2026, um dia antes do calendário.
35. (F5, decisão 151) A leitura ganha uma conta que o plano não tinha: a comparação sem a sessão de cada integrante, feita depois de ver os números e marcada como exploratória; não muda nenhum veredito das regras L9 e L11. Entrou em 24/11 por script (`avaliar_fase5.sem_um_integrante`, campo `sem_um_integrante` e bloco `tb_f5_medicao_sem_um_integrante`); nela o p do Task Success aparece mesmo quando sobram menos de seis cenários diferentes, caso em que a regra L11 não o calcula, com o que a regra daria na coluna ao lado.
36. (F5, decisão 151) A ressalva do Task Success na aba `medicao` é texto escrito à mão (`painel_leituras.RESSALVAS_DA_MEDICAO`), amarrado à corrida lida, e não a frase à mão do alto da aba que a seção 6 do plano previa (`RESPOSTA_SIMPLES`): o alto continua sendo as frases das regras L9 e L11, agora com o tempo dito como o resultado central e a ressalva colada na do Task Success.
37. (F5, decisão 151) No README e na figura da descoberta da fase, o Task Success não é desenhado nem apresentado como segundo resultado central: entra num parágrafo à parte, com a ressalva, e na tabela de dados da figura. O plano (seção 6) pedia a descoberta com a figura, sem dizer qual das duas medidas ela mostra.
38. (F6) As seções da Fase 5 entraram no documento do TCC em 24/11/2026, e não em 26 e 27/11/2026, parte delas adiantada em 16/11/2026 (desvios 20 a 22). O Word não foi regerado: sai uma vez só, com o pacote Q8, que também corta o resumo e acerta as frases da Fase 4 que ainda dão corridas como pendentes.

O que a fase deixa para depois, fora dela: o Word do documento do TCC, o corte do resumo e as frases da Fase 4 que ainda dão corridas como pendentes no documento, que são do pacote Q8 da Pós-Fase 4.
