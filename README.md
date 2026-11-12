<!-- ! Alteração de IA - Revisar: (05/11/2026) README refeito como porta de entrada: o que é o projeto, como o agente trabalha, onde está, o que já descobriu (figura, como ler e o que mostra) e como rodar. O detalhe técnico saiu para `DETALHES-TECNICOS.md`, com as tags antigas de cada trecho.
     ! Motivo: o Eric pediu (05/11/2026) uma revisão geral: o README tinha 96 mil caracteres, com tabelas cujas células passavam de 4 mil, e quem chegava não achava o resultado no meio dos dados. O pedido foi deixar a leitura com gráficos e a explicação de cada um, em linguagem direta, e os valores de cada rodada num documento à parte. O histórico das versões anteriores está no git. -->
# Agente de QA E2E Autônomo com Self-Healing

[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-2ea44f)](LICENSE)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](Programacao/CobaiaAPI/requirements.txt)
[![PHP 8.2](https://img.shields.io/badge/PHP-8.2-777BB4?logo=php&logoColor=white)](Programacao/CobaiaFront)
[![Modelo local](https://img.shields.io/badge/LLM%20local-Ollama%20%C2%B7%20qwen2.5%3A7b-1f6feb)](Programacao/AgenteCore/experimentos)
[![Painel do projeto](https://img.shields.io/badge/painel-do%20projeto-8957e5)](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN)

Trabalho de Conclusão de Curso em Ciência da Computação (Universidade Cidade de São Paulo, 2026). É um agente de testes que abre um sistema web como uma pessoa abriria, percebe quando algo quebrou, diz por que quebrou e, quando a causa é só um seletor que mudou, conserta o próprio teste. Tudo roda na máquina de quem testa: o modelo de linguagem é local (Ollama, só CPU, sem nuvem).

<!-- ! Alteração de IA - Revisar: (11/11/2026) a linha de estado passa a dizer a Fase 4 concluída e a Pós-Fase 4 em andamento, como a tabela "Onde o projeto está".
     ! Motivo: a linha ainda dizia, com data de 05/11/2026, que a Fase 4 estava em andamento com uma corrida por fazer; a fase fechou em 06/11/2026, e a tabela logo abaixo já dizia isso. -->
> **Em 11/11/2026:** a Fase 4, em que o agente passou a trabalhar na tela de verdade, está concluída. A Pós-Fase 4, que cuida do que o agente entrega a quem lê, está em andamento, com três corridas por rodar antes da Fase 5.

| Quero... | Vá para |
|---|---|
| Entender o projeto e ver os resultados | as seções abaixo |
| Explorar cada resultado, um assunto por aba | [Painel do projeto](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN) |
| Ler o trabalho formal, nas normas da ABNT | [Documento do TCC em Word](Documentacao/TCC_v3_20261105.docx) e a [fonte em Markdown](Documentacao/TCC%20-%20ABNT%2014724%20-%20V1.md) |
| Ver scripts, configurações e os valores de cada rodada | [Detalhes técnicos](DETALHES-TECNICOS.md) |
| Ver o número exato por trás de cada figura | [Dados das figuras](Documentacao/figuras/dados-das-figuras.md) |
| Saber o que foi decidido e por quê | [Memorial](Documentacao/Memorial%20de%20Desenvolvimento.md), [roadmap](Documentacao/memorial/roadmap.md), [pendências](Documentacao/memorial/pendencias.md) e [relatório da Fase 4](Documentacao/memorial/3-resultados-e-analises/fase-4-relatorio.md) |
| Ver a cópia no repositório da disciplina | [squad-24-projeto](https://github.com/unicid-projeto-software-2026-2/squad-24-projeto) (privado; este repositório é o principal) |
| Instalar e rodar | [Instalar e rodar](#instalar-e-rodar) |

## O problema

Quando o front-end e a API de um sistema evoluem separados, a API pode mudar o formato de uma resposta sem avisar: um campo some, muda de nome ou de tipo. O teste de ponta a ponta falha, mas a mensagem raramente diz o motivo, e alguém precisa abrir o navegador, comparar a resposta com o combinado e achar a causa. Esse desencontro se chama **deriva de contrato**, e é o foco deste trabalho.

O segundo problema é mais simples. A tela muda um `id` ou um texto, o **localizador** do teste não acha mais o botão, e o teste quebra sem que o sistema tenha defeito nenhum.

O agente trata os dois: explica a causa da deriva de contrato e conserta sozinho o localizador. Ele também mantém a própria **biblioteca**, um conjunto de **verbetes**, fichas curtas de documentação sobre o sistema testado (um contrato, um erro conhecido, uma regra de negócio).

## Como o agente trabalha

![Fluxo do agente em seis passos, do roteiro na tela até os três resultados, com a trilha embaixo](Documentacao/figuras/como-o-agente-trabalha.png)

**Como ler:** siga as setas a partir do passo 1. O azul é código comum, que dá sempre o mesmo resultado. O laranja é o passo em que o modelo responde. As caixas cinza são o que sai no fim, e a trilha, embaixo, guarda tudo para quem for revisar.

**A ideia central:** o modelo dá a opinião e o código confere. Nada que o modelo escreve vai para a biblioteca, nem chega a quem lê como certeza, sem passar por uma conferência em código.

## Onde o projeto está

| Fase | A pergunta que ela responde | Estado |
|---|---|---|
| 1 | Temos um ambiente de teste controlado, com falhas que se repetem? | Concluída |
| 2-A | Um modelo local consegue diagnosticar sem documentação nenhuma? | Concluída |
| 2-B | Documentação escrita por pessoas ajuda? | Concluída |
| 3 | O próprio modelo consegue manter essa documentação? Qual modelo fica? | Concluída |
| 3-B | O resultado se sustenta com casos novos e com outro modelo lendo? | Concluída |
| Pré-Fase 4 | Modelos maiores cabem nesta máquina? Dá para abrir o raciocínio do agente? | Concluída |
| 4 | O agente funciona na tela de verdade, e não só em casos escritos? | Concluída |
<!-- ! Alteração de IA - Revisar: (07/11/2026, pacote Q1) a linha da Pós-Fase 4 passa a "Em andamento" e o item da lista abaixo diz o que já existe.
     ! Motivo: o pacote Q1 gerou o relatório por caso no molde do syllabus e a camada de leitura dos verbetes; "Não iniciada" e "hoje os verbetes são difíceis de entender" sozinhos ficariam atrasados. -->
<!-- ! Alteração de IA - Revisar: (08/11/2026, pacote Q3) a linha da Pós-Fase 4 diz que o Q3 também está feito.
     ! Motivo: o pacote Q3 gerou a árvore de decisão de cada caso; sem a frase, a tabela pararia no Q2. -->
<!-- ! Alteração de IA - Revisar: (08/11/2026, pacote Q4) a linha da Pós-Fase 4 diz que o Q4 também está feito.
     ! Motivo: o pacote Q4 entregou a barra de progresso e o protótipo da seleção pelo diff do Git; sem a frase, a tabela pararia no Q3. -->
<!-- ! Alteração de IA - Revisar: (10/11/2026, pacote Q5) a linha da Pós-Fase 4 diz que o Q5 também está feito.
     ! Motivo: o pacote Q5 fez a medida com revisor humano dos relatórios; sem a frase, a tabela pararia no Q4. -->
| Pós-Fase 4 | O que o agente entrega é fácil de ler e de usar? | Em andamento (Q1 e Q2 feitos em 07/11/2026; Q3 e Q4 em 08/11/2026; Q5 em 10/11/2026) |
| 5 | Ele resolve mais rápido que uma pessoa? | Não iniciada |

**O que falta antes da Fase 5:**

<!-- ! Alteração de IA - Revisar: (07/11/2026, pacote Q2) a linha da Pós-Fase 4 na tabela acima diz que o Q2 também está feito, e o item abaixo ganhou os filtros de texto.
     ! Motivo: o pacote Q2 passou a medir em código cada texto que chega ao analista e ajustou o molde do relatório até passar; sem a frase, o leitor acharia que só a camada de leitura existe. -->
<!-- ! Alteração de IA - Revisar: (08/11/2026, pacote Q4) o item abaixo ganhou a barra de progresso e o protótipo da seleção pelo diff do Git.
     ! Motivo: são as duas entregas do pacote Q4 (plano da Pós-Fase 4, seções 3.5 e 3.7); sem a frase, o leitor não saberia que existem. -->
<!-- ! Alteração de IA - Revisar: (10/11/2026, depois das fichas 62 e 63) o item abaixo passou a dizer que os 36 relatórios foram lidos por um analista de QA da empresa.
     ! Motivo: o Eric declarou no quadro quem é o analista e que as 36 respostas são dele (decisão 117, que fecha a ficha 62). -->
<!-- ! Alteração de IA - Revisar: (10/11/2026, tarde) o item abaixo passou a dizer que quase todos os relatórios foram lidos por um analista, que o tempo de leitura não foi medido e que as leituras dos verbetes foram curadas.
     ! Motivo: o texto da manhã dizia que o Eric tinha lido os 36 relatórios; ele declarou que passou os relatórios a um analista (decisão 114), e a curadoria das 39 leituras foi aplicada com consertos (decisão 115). -->
<!-- ! Alteração de IA - Revisar: (10/11/2026, pacote Q5) o item abaixo ganhou a sessão com revisor humano dos relatórios.
     ! Motivo: é a medida da especificação da trilha que a Fase 4 deixou em aberto (ficha 40, decisão 113); sem a frase, o leitor acharia que ninguém leu os relatórios novos. -->
<!-- ! Alteração de IA - Revisar: (08/11/2026, pacote Q3) o item abaixo ganhou a árvore de decisão por caso.
     ! Motivo: o pacote Q3 é a terceira entrega do que chega ao analista (plano da Pós-Fase 4, seção 3.4); sem a frase, o leitor não saberia que a árvore existe. -->
- rever o que o agente entrega ao analista, porque hoje os verbetes são difíceis de entender (desde 07/11/2026 existe uma camada de leitura dos verbetes, gerada por código e curada em 10/11/2026 por um analista, com consertos no que era fato errado; o relatório por caso segue o molde do relatório de defeitos do syllabus CTFL 4.0; e filtros em código medem cada texto que chega ao analista, com limiares calibrados nos comentários deste repositório: todos os relatórios passam, e as leituras dos verbetes passam todas depois da curadoria; e, desde 08/11/2026, cada caso tem uma árvore de decisão lida da trilha gravada, com o que o modelo leu, que verbetes entraram, a causa contra a segunda, a cura quando houve e a origem de cada afirmação: o que o código mediu, o que ele conferiu, o que o modelo só declarou e o que faltou; e, também desde 08/11/2026, enquanto o modelo pensa uma barra de progresso diz quanto falta, estimando pelas taxas das corridas anteriores desta máquina, com o erro medido nos registros gravados, e um protótipo lê o que mudou no Git para dizer quais cenários rodar e por quê, provado no histórico do próprio repositório; e, em 09 e 10/11/2026, os 36 relatórios da corrida 24 foram lidos no formato novo, um por vez e às cegas, todos por um analista de QA da empresa, que não participou do projeto, a quem o Eric passou os relatórios: ele decidiu certo na maior parte deles e deu a nota máxima de utilidade à maioria, mas o tempo de leitura não foi medido e é um leitor só);
- a Pós-Fase 4: ajustes e ideias para o visual do projeto, com o tipo de resposta e a formatação, e talvez gráficos ou um dashboard dinâmico sobre cada assunto (decisão 94).

## O que já descobrimos

Cada figura responde a uma pergunta. O número exato de cada uma está em [Dados das figuras](Documentacao/figuras/dados-das-figuras.md), e as condições de cada rodada, em [Detalhes técnicos](DETALHES-TECNICOS.md).

<!-- fonte dos números desta seção: Documentacao/figuras/dados-das-figuras.md, gerado de resultados_alvo/ por gerar_figuras_documentos.py; adesão ao verbete errado: fase3/comparacao_fases.json, adesao_cega_2B_A5_pct; margem do ensaio: fase4/cenarios_v4.json, geral; verbete certo no contexto: fase4/tela_v4.json e tela_ineditos.json, verbete_certo; a regra da tela: campos b e c de tela_v4.json e tela_ineditos.json; a corrida 24: fase4/ineditos.json; erros pegos pelo selo baixo: fase4/calibracao.json, limiares; lote nos inéditos: fase4/biblioteca.json, regra_r5 e relatório da Fase 4, seção 7. -->

### A documentação faz diferença?

![Quatro linhas, uma por modelo, do acerto sem documentação até o acerto com a biblioteca escrita pelo modelo](Documentacao/figuras/documentacao-e-acerto.png)

**Como ler:** cada linha é um modelo, e cada ponto é quanto ele acertou nos mesmos 36 casos. Da esquerda para a direita, o modelo recebe mais ajuda. Linha subindo quer dizer mais causas certas.

**O que isso mostra:** a documentação certa ajuda os quatro modelos da figura, e quem acertava menos ganha mais: o `qwen2.5-coder:3b` sai de 19% para 69%. Só o `qwen2.5:7b` ganha mais de um caso com a biblioteca que ele mesmo escreveu, de 78% para 89%, e mesmo isso fica abaixo do que 36 casos conseguem comprovar. A linha do `granite4.2:8b` fica reta no último trecho porque nenhuma edição dele foi aceita. O outro lado é o risco: na Fase 2-B, o `granite4.2:8b` e o `qwen2.5-coder:3b` seguiram um verbete errado, acompanhado de um registro de incidente falso, em 93% e 96% dos casos. É por isso que nada entra na biblioteca sem conferência.

### Qual modelo ficou?

![Pontos por modelo: tempo por caso no eixo horizontal e acurácia balanceada no vertical, com o escolhido em destaque](Documentacao/figuras/escolha-do-modelo.png)

**Como ler:** cada ponto é um modelo com a biblioteca num certo estado. Quanto mais alto, mais acerta; quanto mais à esquerda, mais rápido. A **acurácia balanceada** é o acerto calculado causa por causa, com o mesmo peso para todas, para que responder sempre a causa mais comum não pareça bom. A linha vertical no ponto escolhido mostra a incerteza: com só 36 casos, o valor verdadeiro pode estar em qualquer lugar dela. Entre versões da biblioteca de um mesmo modelo, o tempo não se compara, porque foi medido em momentos diferentes da corrida.

**O que isso mostra:** pela regra fixada antes de rodar, ficou o `qwen2.5:7b` com a primeira versão da biblioteca escrita por ele (decisão 52), depois curada e guardada em `Programacao/AgenteCore/biblioteca_producao/`. O `qwen2.5-coder:3b` é bem mais rápido, mas acerta menos, e o `granite4.2:8b` acerta perto, mas leva mais de 120 segundos por caso.

### A biblioteca serve para qualquer modelo?

![Pares de barras: casos certos de cada modelo com a biblioteca original e com a biblioteca escrita pelo qwen2.5:7b](Documentacao/figuras/quem-le-a-biblioteca.png)

**Como ler:** cada par de barras é o mesmo modelo lendo os mesmos 36 casos. A barra cinza usa a biblioteca original, e a azul, a que o `qwen2.5:7b` escreveu.

**O que isso mostra:** quem escreveu ganha 4 casos, o `qwen2.5-coder:7b` ganha 1 e o `qwen2.5-coder:3b` perde 4. Por isso o padrão do agente é o modelo com a biblioteca que ele mesmo escreveu (decisão 69). E o ganho não é garantido em casos novos: em 36 casos inéditos, essa versão fez 26 certos, contra 27 da biblioteca original ([figura dos casos inéditos](Documentacao/figuras/casos-ineditos.png)).

### O agente sabe quando pode estar errado?

![Barras por selo de confiança, alto, médio e baixo, com os casos certos e errados de cada um](Documentacao/figuras/selo-de-confianca.png)

**Como ler:** cada barra reúne os casos que receberam o mesmo selo. O azul são os certos, e o laranja, os errados. O selo vem da probabilidade que o próprio modelo dá à causa que escolheu.

**O que isso mostra:** o selo separa os extremos. No alto, são 3 erros em 37 casos; no baixo, 15 em 27. Mandar para revisão só o selo baixo pega 15 dos 22 erros olhando 27 dos 90 casos. Os cortes de cada selo foram calculados nesses mesmos casos, então esse resultado ainda precisa se repetir em casos novos.

### Ler da tela é tão bom quanto ler um caso escrito?

![Sete barras: casos certos lendo o caso escrito e lendo da tela, nas quatro versões do caso montado a partir dela, e embaixo os casos inéditos](Documentacao/figuras/tela-e-caso-escrito.png)

**Como ler:** as cinco barras de cima são os mesmos 37 casos. A primeira é o modelo lendo o caso escrito à mão, e as outras, o mesmo caso montado a partir da tela, da versão mais nova para a primeira. As duas de baixo são 25 casos inéditos, que a busca nunca tinha visto. Mais casos certos é melhor.

<!-- ! Alteração de IA - Revisar: (06/11/2026, decisões 97 a 99) este parágrafo e o item sobre a leitura da tela passam às corridas 18d e 18e; a regra é dita pelos casos que a tela perde, com a soma citada.
     ! Motivo: a regra fechou com os sinais novos da busca, pela leitura fixada antes da corrida, e o texto antigo dizia que a tela ainda perdia. Números de `tela_v3.json`, `tela_v4.json` e `tela_ineditos.json`, lidos por script. -->
**O que isso mostra:** ler da tela passou à frente do caso escrito: 32 contra 30 nos 37 casos, e 22 contra 18 nos 25 inéditos. A primeira versão dava 16, porque a montagem não dizia o que tinha mudado contra a tela normal. O que mudou por último foi a busca: ela passou a usar o que o caso mede contra a tela normal, e o verbete certo foi de 21 para 36 dos 37 casos, sem nada a mais no texto que o modelo recebe. Isso não quer dizer que o modelo lê melhor da tela: o caso da tela leva uma medida que o caso escrito não tem, e com tão poucos casos a diferença entre os dois lados não se separa do acaso.

A regra aceita que a tela perca no máximo 3 casos para o caso escrito. Ela perdeu 3 e ganhou 5, e nos inéditos perdeu 0 e ganhou 4: a regra fecha, no limite exato (decisões 97 e 98). Até a rodada anterior a conta somava os dois lados, o que daria 8; a leitura que olha só o que a tela perde foi fixada antes desta rodada, sem saber o resultado dela. Os 3 casos perdidos são a mesma confusão: item faltando na lista lido como resposta cortada. E o prompt, o texto que o modelo recebe, cabe no limite do plano ([figura do limite](Documentacao/figuras/prompt-e-limite.png)): dois casos inéditos passaram, porque a lista não tinha teto, e isso foi corrigido sem mudar os outros (decisão 99).

<!-- ! Alteração de IA - Revisar: (06/11/2026) subseção nova com a corrida 24, e a Fase 4 marcada como concluída na tabela de fases, com a Pós-Fase 4 na linha seguinte.
     ! Motivo: era a última pendência da fase, e é a única medida da biblioteca final em casos que ela nunca viu. Números de `ineditos.json`, lidos por script. -->
### E em casos que a biblioteca nunca viu?

![Barras por classe de defeito, com os casos certos e errados entre 36 casos inéditos](Documentacao/figuras/ineditos-por-classe.png)

**Como ler:** cada barra é uma classe de defeito, com seis casos que nenhuma biblioteca tinha visto, lidos em texto. O azul são as causas certas, e o laranja, as erradas. Mais azul é melhor.

**O que isso mostra:** a biblioteca final acerta 25 dos 36, contra 31 de 36 nos casos de avaliação. Não são os mesmos casos, então a diferença não mede só a biblioteca, e o número fica perto do que a Fase 3-B mediu em outros 36 inéditos (26 de 36). O que mais pesa é de novo o verbete certo: quando ele chega ao modelo, são 18 de 20; quando não chega, 7 de 16. A classe de tradução é a mais fraca, com 1 de 6.

### Quanto tempo o agente leva?

![Barras por cenário de falha, com os segundos da detecção até o resultado](Documentacao/figuras/tempo-por-cenario.png)

**Como ler:** cada barra é um cenário de falha, rodado uma vez, do momento em que o agente percebe a falha até ter o resultado. No azul, o resultado é o diagnóstico conferido. No laranja, é o teste passando de novo depois do conserto.

**O que isso mostra:** os 10 cenários chegaram ao resultado, em 74 segundos na média. Encurtar o prompt tirou cerca de 30% do tempo (eram 105 segundos), sem mudar nenhuma causa respondida, e os sinais novos da busca não mudaram esse resultado. Quase todo esse tempo é o modelo pensando ([figura de onde vai o tempo](Documentacao/figuras/onde-vai-o-tempo.png)): o conserto de localizador só em código levou 0,64 segundo e funcionou nas 160 quebras armadas.

### O que o agente escreve entra na biblioteca sem controle?

![Funil: propostas do modelo, as que passam por cada conferência e as que ficam na biblioteca](Documentacao/figuras/funil-da-biblioteca.png)

**Como ler:** de cima para baixo, quantas propostas sobrevivem a cada conferência. Ao lado de cada etapa, o motivo mais comum de quem ficou pelo caminho.

**O que isso mostra:** das 92 propostas do modelo, 19 chegaram ao lote, e 11 ficaram na biblioteca depois da revisão. Esse lote não mudou nenhum acerto nos 36 casos inéditos. O que encurtou a distância da tela foi revisar a montagem do caso e a busca, não a biblioteca.

<!-- ! Alteração de IA - Revisar: (05/11/2026) a medida com revisor humano passou a em aberto (decisão 95), e a lista do que falta antes da Fase 5 ganhou a Pós-Fase 4 (decisão 94).
     ! Motivo: o Eric pediu "em aberto" nesta data, porque a revisão será feita depois de as respostas serem normalizadas; o texto dizia só que ela não foi feita. -->
### O que ainda não dá para afirmar

- **Que o agente é mais rápido que uma pessoa.** Ainda não há a medida com pessoas; ela é a Fase 5.
- **Que os 10 de 10 se repetem.** Foi uma repetição por cenário, e com dez execuções a margem de incerteza vai de 72% a 100%.
- **Que o conserto de localizador funciona em qualquer quebra.** As 160 quebras foram armadas de propósito, com o elemento certo ainda na página.
- **Que o modelo lê melhor da tela do que de um caso escrito.** A tela passou à frente nas duas medidas, mas o caso da tela leva uma medida contra a tela normal que o caso escrito não tem, e a diferença não se separa do acaso nesse número de casos. A regra que compara os dois lados fechou sem folga: a tela perde 3 casos, e o limite é 3. Os sinais novos da busca foram escritos olhando os 37 casos, e a conferência são 25 casos inéditos.
- **Que um exemplar resolvido ou os rótulos em palavras ajudam o modelo.** Testamos os dois nos 90 casos: trocam a resposta em alguns casos, para os dois lados, e o saldo não se separa do acaso (decisão 91).
- **Quanto a biblioteca ajuda nos casos que ela nunca viu.** A última corrida mede só a biblioteca final; esses casos não foram lidos sem ela.
- **Que os sinais da trilha apontam os erros.** A corrida teve só 5 erros, poucos para pôr os sinais em ordem ([figura dos sinais](Documentacao/figuras/sinais-da-trilha.png)).
- **Que o relatório ajuda quem revisa.** Em aberto: a medida com revisor humano será feita depois que a Pós-Fase 4 normalizar e melhorar as respostas; por agora vale a pré-análise do agente de apoio (decisões 85, 86 e 95).

## Os dois sistemas de teste

Medir sem depender de opinião pede um ambiente controlado. Por isso o repositório traz dois sistemas "cobaia", que compartilham o mesmo banco de dados, e falhas que podem ser ligadas e desligadas sempre do mesmo jeito.

| Sistema | O que é | Para que serve |
|---|---|---|
| **CobaiaFront** | Site PHP legado de um restaurante, mantido como veio | Falhas de página completa e erros clássicos de sistema antigo |
| **CobaiaAPI** | API JSON em Python (FastAPI), com injeção de falhas | Deriva de contrato em respostas reais, o foco do agente |

<!-- ! Alteração de IA - Revisar: (11/11/2026) parágrafo novo com a origem do CobaiaFront, o Projeto CHULETA, e o caminho da nota que lista o que este trabalho acrescentou e mudou nele.
     ! Motivo: o Eric pediu a citação correta do projeto de onde veio a parte PHP da cobaia; nenhum arquivo do repositório dizia de onde o site veio, e a tabela acima diz "mantido como veio" sem dizer de quem. O repositório de origem foi conferido pela API do GitHub em 11/11/2026. -->
O CobaiaFront é o [Projeto CHULETA](https://github.com/pedrohtgoncalvesgit/Projeto-CHULETA), de Pedro Henrique Torres Gonçalves, integrante do grupo, cedido pelo autor para servir de sistema sob teste. O que este trabalho acrescentou e mudou no site está em [`Programacao/CobaiaFront/ORIGEM.md`](Programacao/CobaiaFront/ORIGEM.md).

A avaliação usa 90 casos de falha com a resposta certa conhecida, e as regras de decisão são fixadas antes de cada rodada. A arquitetura e o detalhe de cada sistema estão em [Detalhes técnicos](DETALHES-TECNICOS.md#arquitetura).

## Instalar e rodar

Precisa de Windows 10/11, Linux ou macOS e de internet: o instalador baixa PHP, MariaDB e os pacotes Python que faltarem. No Linux, ele usa `sudo` e `apt-get`; no macOS, o [Homebrew](https://brew.sh).

**No Windows, o caminho mais curto** é dar dois cliques em `Cobaia.exe`: ele instala, sobe tudo e abre o navegador. Na primeira vez, o Windows pode mostrar "Windows protegeu seu PC", porque o arquivo não é assinado; clique em "Mais informações" e depois em "Executar assim mesmo".

**Por partes**, na raiz do repositório:

```
# Windows (clique duplo ou pelo terminal)
install.cmd
run.cmd
```

```bash
# Linux / macOS
./install.sh
./run.sh
```

Depois de subir:

- **CobaiaFront:** http://localhost:8080
- **CobaiaAPI (documentação interativa):** http://localhost:8000/docs

`Ctrl+C` encerra tudo. As contas de teste já vêm no banco:

| Login | Senha | Uso |
|---|---|---|
| `admin` | `admin123` | Painel do administrador (`/admin/login.php`) |
| `11122233344` | `123456` | Área do cliente, com reservas (mesmo formulário) |

Máquina sem administrador, o que o instalador faz passo a passo, os testes e as soluções para erros comuns estão em [Detalhes técnicos](DETALHES-TECNICOS.md#instalação-em-detalhe).

## Estrutura do repositório

```
TCC/
├── README.md                 # esta página
├── DETALHES-TECNICOS.md      # scripts, configurações e os valores de cada rodada
├── Cobaia.exe                # Windows: instala, roda e abre o navegador
├── install.* / run.*         # instalador e inicialização, nos três sistemas
├── ferramentas/              # scripts locais: painel, documento do TCC, conferências
├── claude-memoria/           # memória do Claude e os registros de passagem entre sessões
├── Documentacao/
│   ├── TCC - ABNT 14724 - V1.md   # fonte do documento do TCC (o nome fica "V1" em todas as versões)
│   ├── TCC_v3_20261105.docx       # documento do TCC em Word
│   ├── figuras/                   # as figuras desta página e a tabela de cada uma
│   ├── dashboard/                 # o painel do projeto
│   └── memorial/                  # decisões, pesquisa, relatórios, roadmap e pendências
└── Programacao/
    ├── AgenteCore/               # o agente, a biblioteca e as baterias de avaliação
    ├── CobaiaFront/              # o site PHP legado
    └── CobaiaAPI/                # a API com injeção de falhas
```

A árvore completa está em [Detalhes técnicos](DETALHES-TECNICOS.md#estrutura-do-repositório).

## Segurança

Este é um **ambiente de teste**: as senhas fracas, a injeção de SQL no CobaiaFront e o CORS liberado na CobaiaAPI são conhecidos e ficam de propósito, porque fazem parte do que o agente precisa enfrentar. Não reutilize esses padrões fora deste projeto. Problemas reais nos instaladores e nas ferramentas seguem a [política de segurança](SECURITY.md).

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

<!-- ! Alteração de IA - Revisar: (11/11/2026) a seção passa a dizer como citar o projeto de origem do CobaiaFront, e o `CITATION.cff` ganhou a mesma referência.
     ! Motivo: pedido do Eric em 11/11/2026: o site PHP da cobaia é o Projeto CHULETA, e quem usa essa parte do repositório precisa citar o autor dela. -->
O site de teste em PHP tem origem própria. Quem usar o CobaiaFront deve citar
também o projeto de onde ele veio:

> GONÇALVES, P. H. T. **Projeto CHULETA.** 2024. Repositório:
> https://github.com/pedrohtgoncalvesgit/Projeto-CHULETA.

## Licença

O código e a documentação deste repositório estão sob a [licença MIT](LICENSE).
<!-- ! Alteração de IA - Revisar: (11/11/2026) frase nova sobre a licença do CobaiaFront, que vem do Projeto CHULETA.
     ! Motivo: o repositório de origem não traz arquivo de licença (conferido em 11/11/2026); sem a frase, não ficava dito sob que licença o site é distribuído aqui nem que o autor dele assina a licença deste repositório. -->
O CobaiaFront vem do Projeto CHULETA
([origem](Programacao/CobaiaFront/ORIGEM.md)): o repositório de origem não traz
arquivo de licença, e aqui o site é distribuído sob a licença MIT deste
repositório, da qual o autor do site é um dos titulares.
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
