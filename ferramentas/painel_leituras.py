#!/usr/bin/env python3
# ! Alteração de IA - Revisar: módulo novo (05/11/2026) que dá ao painel a leitura de cada gráfico e recolhe os dados crus: depois de montada a
# página, `aplicar` põe um parágrafo "Como ler" abaixo de cada gráfico e de cada figura e leva as tabelas de dados e as figuras repetidas para um
# bloco "Mais informações". Os textos ficam aqui, um por gráfico, e não trazem número de resultado.
# ! Motivo: o Eric pediu (05/11/2026) o painel com o gráfico e a análise à vista e os dados brutos em "mais informações", como já estava na aba da
# Fase 3, porque "cuspir dados" não explica nada. Eram 77 tabelas à vista, com 746 linhas, e nenhum gráfico dizia como ser lido. Fazer isso na página
# montada, e não em cada uma das 30 abas, garante a mesma regra em todas, e o teste acusa gráfico novo que chegue sem explicação.
"""Leitura dos gráficos e recolhimento dos dados crus do painel. Uso: `aplicar(html_da_pagina)`, chamado por gerar_dashboard.py."""
from __future__ import annotations

import re

# texto de cada gráfico, pelo id do <canvas>: o que é cada marca, para que lado é melhor e o que usar de cuidado. Sem número de resultado: esses ficam na leitura da aba.
COMO_LER_GRAFICO = {
    "g-curvas": "cada linha é um modelo. Da esquerda para a direita, a biblioteca ganha as edições de cada época: L0 é a original, e L1 a L3, as versões que o modelo escreveu. Linha subindo quer dizer que a biblioteca ajudou naquele conjunto de casos. A acurácia balanceada dá o mesmo peso a cada causa, para que responder sempre a causa mais comum não pareça bom.",
    "g-fases": "cada grupo de barras é uma etapa do trabalho, e cada cor, um modelo. Compare a mesma cor de um grupo para o outro: subir quer dizer que aquela etapa ajudou o modelo. Sem barra de uma cor, aquele modelo não rodou ali.",
    "g-doc": "cada grupo é uma época, e cada barra conta as edições de um modelo que passaram pelo validador. Barras caindo de uma época para a outra querem dizer que o modelo tem cada vez menos o que acrescentar.",
    "g-rej": "cada barra é um motivo de recusa, do mais comum para o menos comum, e as cores dizem de qual modelo veio cada recusa. Barra de uma cor só aponta um problema daquele modelo; barra com todas as cores, um problema de todos.",
    "g-rec": "cada linha é um modelo. A altura é a parcela dos casos em que o verbete certo ficou entre os três entregues ao modelo. Linha caindo quer dizer que a biblioteca cresceu e a busca passou a achar menos o verbete certo.",
    "g-custo": "cada grupo é uma versão da biblioteca, e cada barra é o tempo que um modelo levou por diagnóstico, no valor do meio entre os casos. Quanto menor, mais rápido. A última versão foi medida em outro momento da corrida, e por isso esse tempo não prova que ela é mais barata.",
    "g-rev": "cada barra é um modelo e soma 100% das edições revisadas dele. Verde são as corretas, amarelo as parciais e vermelho as erradas. Quanto mais verde, mais confiável o que o modelo escreve.",
    "g-boot": "o teste sorteia os casos de novo, muitas vezes, e conta quem fica em primeiro em cada sorteio. A barra é a parcela de sorteios que cada combinação de modelo e biblioteca venceu. Uma barra bem maior que as outras quer dizer que a escolha não dependeu da sorte dos casos.",
    "g-pareto": "cada ponto é um modelo com a biblioteca num certo estado. Quanto mais alto, mais acerta; quanto mais à esquerda, mais rápido. Os losangos são as combinações que nenhuma outra supera ao mesmo tempo em acerto, tempo e risco. Entre versões da biblioteca de um mesmo modelo, o tempo não se compara, porque foi medido em momentos diferentes da corrida.",
    "g-f2b": "cada grupo é uma condição: A0 sem documentação, A1 a biblioteca inteira, A2 os três verbetes mais parecidos, A3 só o verbete certo, A4 verbetes parecidos, mas errados, e A5 um verbete errado com um registro falso. Cada cor é um modelo. Compare a mesma cor entre os grupos: A3 mostra até onde o modelo chega, e A5, o quanto ele segue o erro. Só três modelos rodaram de A3 a A5.",
    "g-f2a": "cada grupo é uma forma de prompt, e cada cor, um modelo. Barras da mesma cor com alturas parecidas entre os grupos querem dizer que a forma do prompt pouco importa para aquele modelo.",
    "g-mod-classe": "cada grupo é uma classe de defeito, e cada cor, um modelo. Grupo com barras baixas é uma classe difícil para todos; barra destoando no grupo é um modelo que se sai melhor ou pior ali. O seletor troca a versão da biblioteca.",
    "g-mod-nivel": "cada grupo é um nível de dificuldade, e cada cor, um modelo. Se a barra não cai do fácil para o difícil, o nível não explica o que o modelo acerta.",
    "g-cmp-etapas": "cada linha é um modelo, e o eixo de baixo segue as etapas do trabalho, da esquerda para a direita. Linha subindo quer dizer que a etapa ajudou. O primeiro ponto foi medido em outra máquina; o acerto se compara entre máquinas, e o tempo, não. Os seletores trocam os casos e a medida.",
    "g-cq-traj": "cada linha é um dos dois modelos, e o eixo de baixo segue as etapas do trabalho. A linha mais alta em cada ponto é a do modelo que acertou mais ali. Linhas que se cruzam querem dizer que nenhum dos dois é melhor em tudo.",
    "g-cq-conf": "cada grupo é uma condição. As barras contam só os casos em que um modelo acertou e o outro errou, porque os casos em que os dois acertam ou erram juntos não dizem quem é melhor. Barras de tamanhos parecidos querem dizer empate.",
    "g-cq-rev": "cada barra é um modelo e soma 100% das edições revisadas dele. Verde são as corretas, amarelo as parciais e vermelho as erradas.",
    "g-tb-gen": "cada cor é um modelo. A linha cheia são os 36 casos oficiais, e a tracejada, os 36 inéditos, que nenhum modelo viu antes. Da esquerda para a direita, a biblioteca cresce. Se as duas linhas da mesma cor sobem juntas, o ganho vale também para casos novos.",
    "g-tb-rec": "cada grupo é uma versão da biblioteca. A barra cheia são os inéditos, e a clara, os oficiais; a altura é a parcela de casos em que o verbete certo ficou entre os três entregues. Barra cheia abaixo da clara quer dizer que a busca acha menos nos casos novos.",
    "g-cur-op": "cada barra é um tipo de edição, e as cores dizem como a revisão a julgou: verde correta, amarelo parcial e vermelho errada. Barra com muito vermelho aponta um tipo de edição que pede mais cuidado.",
    "g-rec-met": "cada grupo é um método de busca, e cada cor, um conjunto de casos. Quanto mais alta a barra, mais vezes o verbete certo apareceu entre os primeiros. Os seletores trocam a biblioteca e a medida.",
    "g-abl": "cada grupo é um modelo numa condição. As três barras dizem quanto ele acerta, quanto responde no formato pedido e quanto inventa um rótulo fora da lista. O bom é ter as duas primeiras altas e a terceira baixa.",
    "g-fer-mcp": "cada grupo é uma tarefa, e as duas barras são os tokens gastos por subagentes iguais, um só com busca de texto e outro com o servidor. Barra menor é menos consumo. O seletor conta ou não a leitura de cache.",
    "g-cz-leit": "cada cor é um modelo lendo a biblioteca, e o eixo de baixo é a versão dela. A linha cheia é ele lendo a biblioteca do doador, e a tracejada, a própria. A linha do doador é a referência: mostra o que a biblioteca rende com quem a escreveu.",
    "g-cz-trocas": "cada linha compara um leitor com uma biblioteca. A barra verde, para a direita, conta os casos que ele passou a acertar, e a vermelha, para a esquerda, os que deixou de acertar. O que importa é o saldo entre as duas.",
    "g-co-min": "cada barra é o tempo de uma resposta do nosso tamanho. A azul é o diagnóstico inteiro de hoje, e as outras são o colibri só gerando a resposta, em máquinas de terceiros. Quanto mais longa, mais espera.",
    "g-ra-sus": "cada grupo é uma corrida. As duas barras comparam o acerto quando algum verbete entregue trata da causa respondida e quando nenhum trata. Distância grande entre as duas quer dizer que o agente pode usar esse sinal para desconfiar da resposta.",
    "g-ra-conf": "cada grupo é um sinal, e cada cor, uma biblioteca. A altura (AUROC) mede o quanto o sinal separa erros de acertos: 0,5 é o mesmo que sortear, e 1 separa tudo. Quanto mais alta, melhor o sinal para decidir o que revisar.",
    "g-ce-temas": "cada barra é um tema, e as cores contam as opções avaliadas nele: verde serve agora, a cor do meio só com outra máquina, outro motor ou depois da Fase 4, e vermelho não serve.",
    "g-pe-rodadas": "cada barra é uma rodada de pesquisa e soma as afirmações que os agentes checaram. Verde são as aprovadas, vermelho as rejeitadas e a última cor, as que não deu para verificar.",
    "g-rep-classe": "cada grupo é uma classe de defeito. Para cada conjunto de casos há duas barras: quantos têm tela e modo de falha, e quantos reproduzem de fato. Barras iguais querem dizer que tudo o que dava para rodar reproduziu; barras baixas apontam uma classe que quase não passa pela tela.",
    "g-cal-k": "cada grupo é um número de verbetes entregues ao modelo (k). As barras mostram o acerto, a acurácia balanceada e o quanto a probabilidade separa erros de acertos (AUROC, multiplicada por 100). Mais alto é melhor nas três.",
    "g-cal-curva": "a linha mostra o que acontece se o agente só responder nos casos em que mais confia. À esquerda, ele responde poucos casos; à direita, todos. A altura é a parcela de erros entre os respondidos. Linha caindo para a esquerda quer dizer que a probabilidade serve para escolher o que mandar para revisão.",
    "g-tela-corridas": "cada grupo é uma corrida, da mais antiga para a mais nova. As barras contam os acertos lendo da tela, os acertos lendo o caso escrito e os casos com a mesma causa nos dois lados. O bom é ver as três altas e próximas: barras distantes querem dizer que ler da tela muda o diagnóstico.",
    "g-tela-verbete": "cada barra junta os casos de um lado (tela ou caso escrito) em que o verbete da causa certa chegou ou não ao modelo. Verde são os acertos, e vermelho, os erros. Muito verde com o verbete e bem menos sem ele quer dizer que o acerto depende de a busca entregar o verbete certo.",
    # ! Alteração de IA - Revisar: (06/11/2026, decisões 97 e 98) o "Como ler" do gráfico novo da regra, e o do gráfico por classe com as corridas que ele mostra agora.
    # ! Motivo: gráfico novo entra com o texto aqui, e o gráfico por classe passou a comparar a tela antes e depois dos sinais da busca.
    "g-tela-regra": "cada grupo é uma corrida, e o último são os inéditos. A barra vermelha conta os casos em que só o caso escrito acerta, e a verde, os casos em que só a tela acerta. A linha é o limite da regra: a barra vermelha pode chegar até ela. Vermelha abaixo ou na linha quer dizer que ler da tela não piorou o diagnóstico.",
    # ! Alteração de IA - Revisar: (06/11/2026) o "Como ler" dos dois gráficos da corrida 24.
    # ! Motivo: gráfico novo entra com o texto aqui, e o teste acusa se faltar.
    "g-ined-classe": "cada linha é uma classe de defeito, com seis casos que a biblioteca nunca viu. A parte verde são os acertos, e a vermelha, os erros. Mais verde é melhor, e a linha com mais vermelho é onde o agente mais erra.",
    "g-ined-verbete": "cada barra junta os casos em que o verbete da causa certa chegou ou não ao modelo. Verde são os acertos, e vermelho, os erros. Muito verde com o verbete e bem menos sem ele quer dizer que o acerto depende de a busca entregar o verbete certo.",
    "g-pos4-fontes": "cada linha é uma leitura da rodada, e o comprimento da barra é quantas fontes com endereço ela cita. A cor é a parte do pedido: as bases do visual, o syllabus e os repositórios. Barra comprida não quer dizer leitura melhor: nenhuma fonte foi verificada por um segundo agente.",
    "g-tela-classe": "cada grupo é uma classe de defeito. A primeira barra é o total de casos, e as outras, os acertos lendo da tela, antes e depois dos sinais novos da busca, e lendo o caso escrito. Quanto mais perto do total, melhor.",
    "g-exp-acerto": "cada grupo é uma condição: a corrida 16, sem mudança, e as duas variações do prompt. As barras são o acerto nos 90 casos e nos casos de avaliação. Alturas parecidas entre os grupos querem dizer que a variação não mudou o acerto.",
    "g-exp-trocas": "cada linha é uma condição, comparada caso a caso com a corrida 16. A barra verde conta os casos que só a condição acerta, e a vermelha, os que só a corrida 16 acerta. Barras de tamanhos parecidos querem dizer empate: o saldo é o que importa.",
    "g-tela-rotulos": "cada linha é uma causa. As barras dizem quantas vezes ela é a resposta certa (gabarito) e quantas vezes o modelo a deu, lendo da tela e lendo o caso escrito. Barra de tela muito maior que o gabarito quer dizer que o modelo está escolhendo essa causa demais.",
    "g-cura-modo": "cada barra é um modo de quebra e soma as execuções. Verde são as curadas pelo mesmo elemento da referência; amarelo, por outro elemento; vermelho, as não curadas. Só verde quer dizer que a cura achou sempre o elemento certo.",
    "g-cura-roteiro": "a mesma conta do gráfico anterior, agora por roteiro de teste. Passe o cursor sobre a barra para ver o tempo de cada um.",
    "g-bib-filtros": "cada barra é um filtro em código, e o tamanho é quantas propostas ele barrou ou segurou. Filtro sem barra não barrou nada nesta corrida, o que não quer dizer que sobre: ele protege contra o que testa.",
    "g-bib-reavaliacao": "as duas barras são o acerto nos 36 inéditos, antes e depois do lote. Alturas iguais querem dizer que o lote não piorou nem ajudou nesses casos.",
    "g-cen-mttr": "cada linha é um cenário de falha, e as barras são os segundos entre perceber a falha e ter o resultado, nas duas últimas rodadas do ensaio. Quanto menor, mais rápido. Nos cenários de contrato, o resultado é o diagnóstico conferido em código; nos de localizador, o teste passando de novo. Por isso os dois tipos não medem a mesma coisa.",
    "g-cen-ts": "cada linha é um cenário. A barra verde conta as execuções que chegaram ao resultado (Task Success), e a vermelha, as que não chegaram. Com uma repetição por cenário, é um ensaio, não uma medida final.",
    "g-tri-sinais": "cada grupo é uma forma de contar um sinal de alerta. A primeira barra é a parcela dos erros que ele pegou; a segunda, a dos acertos que deixou em paz; a terceira multiplica as duas. Um sinal jogado ao acaso dá 0,25 na terceira: perto disso, ele não serve para separar erro de acerto.",
    "g-tri-mutacoes": "cada linha é um tipo de mudança feita de propósito na entrada do agente. Verde conta as vezes em que a trilha apontou o passo certo; vermelho, outro passo; amarelo, nenhuma diferença; e a última cor, os casos em que a mudança não tinha onde agir. Verde cheio é o esperado por construção: mostra que a trilha registra a mudança, não que o modelo acertou.",
    # ! Alteração de IA - Revisar: (07/11/2026, Pós-Fase 4, pacote Q2) o "Como ler" dos dois gráficos da aba "O que chega ao analista".
    # ! Motivo: gráfico novo entra com o texto aqui, e o teste acusa se faltar.
    "g-texto-criterios": "cada grupo é um critério dos filtros de texto, e cada cor, um conjunto de textos: os relatórios antes (v2) e depois (v3), e os verbetes antes e a camada de leitura depois. A altura é a parcela de textos que ficam dentro do limiar. Barra cheia quer dizer que todo texto do conjunto passa naquele critério; compare a mesma cor clara com a escura ao lado para ver o que o molde novo mudou.",
    "g-texto-termos": "cada linha é um termo da lista fechada de jargão e siglas, e as barras contam em quantos textos ele aparece sem o significado na primeira menção: a clara antes (relatórios v2 e verbetes), a escura depois (relatórios v3 e camada de leitura). Barra escura em zero quer dizer que o molde passou a explicar o termo; barra escura que fica é texto do próprio verbete, que a curadoria reescreve.",
    # ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q4) o "Como ler" dos dois gráficos da aba "Barra e Git".
    # ! Motivo: gráfico novo entra com o texto aqui, e o teste acusa se faltar.
    "g-prog-erro": "cada grupo é uma fase da inferência (ler o prompt, escrever a resposta, as duas juntas), e as barras são o erro da estimativa da barra de progresso em segundos, medido nas inferências já gravadas com as taxas das outras corridas: a primeira barra é o erro mediano em valor absoluto, a segunda é o erro que nove em cada dez inferências não passam. Quanto mais baixas, mais a barra acerta; a fase do prefill concentra o erro.",
    # ! Alteração de IA - Revisar: (10/11/2026, Pós-Fase 4, pacote Q5) os dois gráficos da aba "Revisão humana".
    # ! Motivo: todo gráfico novo entra com o "Como ler" (o teste acusa se faltar).
    "g-revv3-adesao": "cada barra é um grupo de relatórios (diagnóstico certo, diagnóstico errado), e a altura é quantos foram lidos. A parte na cor de acerto é a decisão apropriada (aceitou o certo ou recusou o errado); a parte na cor de alerta é a decisão inapropriada. Quanto maior a parte de acerto, melhor.",
    "g-semnotas-contexto": "cada barra é um banco de casos, e a altura é quantos casos ele tem. As cores dizem o que muda no contexto entregue ao modelo quando as notas saem: os mesmos verbetes sem o texto das notas, os mesmos em outra ordem, ou um verbete trocado pela busca. Quanto maior a primeira parte, mais a corrida isola o efeito do texto das notas.",
    "g-semnotas-pares": "cada grupo é um banco de casos. A barra da biblioteca inteira são os acertos das corridas de referência; quando a corrida 25 tiver rodado, entra ao lado a barra dos acertos sem as notas do modelo, nos mesmos casos. Barras da mesma altura dizem que as notas não mudaram o resultado; a diferença só conta se passar no teste pareado, que está no cartão do veredito.",
    # ! Alteração de IA - Revisar: (10/11/2026, decisão 120) o "Como ler" dos dois gráficos da aba "Segundo passe" (corrida 26).
    # ! Motivo: todo gráfico novo entra com o texto aqui, e o teste acusa se faltar; os dois textos valem antes e depois de a corrida rodar.
    "g-segpasse-alcance": "cada barra é um grupo de casos pelo sinal que acendeu na primeira resposta (só o selo baixo, só a FONTE divergente, os dois), e a altura é quantos casos ele tem. As cores dizem onde está o verbete da causa certa: nos erros, entre os verbetes que o segundo pedido entrega (os únicos que ele tem chance de consertar pelo verbete), já entregue no primeiro pedido, ou fora dos dois; nos acertos, se o caso perde no segundo pedido o verbete certo que tinha no primeiro. Quanto maior a primeira parte e menor a dos acertos que perdem o verbete, mais o segundo passe tem a ganhar.",
    "g-segpasse-resultado": "cada grupo é um sinal aceso na primeira resposta. As duas primeiras barras são os erros e os acertos da primeira resposta nesses casos; quando a corrida 26 tiver rodado, entram ao lado quantos desses erros a segunda resposta consertaria e quantos acertos ela estragaria se valesse sempre, e quantos casos passaram a acertar e a errar pela regra de escolha. O segundo passe só compensa se as barras de conserto passarem as de estrago; a diferença só conta se passar no teste pareado, que está no cartão do veredito.",
    # ! Alteração de IA - Revisar: (10/11/2026, decisão 121) o "Como ler" dos gráficos da aba "Analista de documentação" (a medida M1).
    # ! Motivo: todo gráfico novo entra com o texto aqui, e o teste acusa se faltar.
    "g-analista-portoes": "cada grupo é um dos três portões novos da proposta, e as barras contam, entre as edições da corrida 20 que uma pessoa revisou, quantas ele recusaria: as que a pessoa julgou erradas, as parciais e as corretas. Um portão bom tem as duas primeiras barras altas e a terceira no zero, porque recusar edição correta é perda.",
    "g-analista-sequencia": "cada linha é uma etapa: as edições que passaram nos filtros de hoje, o que sobra depois de cada portão aplicado em sequência e, nas duas últimas linhas, o que sobraria com outras combinações. As cores dividem o que sobra pelo veredito da revisão humana. Quanto menor a parte das erradas e maior a das corretas no fim, melhor os portões separam; uma linha curta só com erradas quer dizer que os portões barraram o que servia.",
    # ! Alteração de IA - Revisar: (11/11/2026, decisão 121) o "Como ler" dos dois gráficos da corrida 27 (medida M2) na aba "Analista de documentação".
    # ! Motivo: todo gráfico novo entra com o texto aqui, e o teste acusa se faltar; os dois textos valem antes e depois de a corrida rodar.
    "g-analista-leituras": "cada grupo é uma das três leituras que a regra compara com a corrida 20, e a altura é o percentual do total daquela leitura: os casos em que o modelo respondeu que não há o que acrescentar (a abstenção), as propostas com texto que afirmam um fato em vez de dar uma ordem, e as propostas que a revisão humana julgou corretas. A barra da corrida 20 já existe; a da corrida 27 entra ao lado quando ela tiver rodado, e a da terceira leitura só depois da revisão às cegas. Passar o cursor mostra a contagem. Nas três, mais alto é melhor; a diferença só conta se passar no teste exato, que está no cartão de cada leitura.",
    "g-analista-casos": "os dois grupos são os casos com lacuna na documentação (o diagnóstico errou, ou nenhum verbete entregue tratava da causa respondida) e os casos sem lacuna. As duas primeiras barras dizem quantos casos cada grupo tem e em quantos a proposta de desenho chamaria o analista; quando a corrida 27 tiver rodado, entram ao lado as abstenções, as propostas e as que passam nos cinco portões. O comportamento que se quer é proposta onde há lacuna e abstenção onde não há.",
    # ! Alteração de IA - Revisar: (10/11/2026, decisão 118) o "Como ler" dos quatro gráficos da aba "Fluxo do agente".
    # ! Motivo: todo gráfico novo entra com o texto aqui, e o teste acusa se faltar.
    "g-fluxo-conferencia": "cada linha é uma corrida já gravada, e o comprimento da barra é quantos erros ela teve. A primeira cor são os erros em que uma das conferências de exemplo desmente, por um fato medido no próprio caso, a causa que o modelo respondeu; a segunda, os erros que elas não marcam. Quanto maior a primeira parte, mais erros a conferência avisaria; nenhuma delas marca um acerto.",
    "g-fluxo-posicao": "cada grupo é uma faixa de posições na lista da busca, e a altura é quantos erros tinham o verbete da causa certa naquela faixa, em cada corrida. Só os três primeiros chegam ao modelo. Barras logo depois da terceira posição são erros que um segundo passe com mais verbetes alcançaria; barras mais à direita são erros que nem dez verbetes alcançam.",
    "g-fluxo-custo": "cada barra é uma forma de entregar o caso ao analista de documentação, e o comprimento é o tempo de uma chamada nesta máquina, em segundos. A primeira é a proposta de edição como é hoje, medida na corrida 20; as outras são estimadas pelas taxas de leitura e de escrita do modelo. Quanto mais curta, melhor.",
    "g-fluxo-afirmacoes": "cada linha é um tópico da pesquisa, e o comprimento é quantas afirmações o leitor tirou das fontes. As cores dizem o que a segunda leitura fez com elas: confirmou, corrigiu o número ou a condição, rejeitou ou não conseguiu conferir. Quanto maior a parte confirmada, mais o tópico se apoia no que as fontes dizem como está.",
    "g-revv3-utilidade": "cada grupo é uma nota de utilidade, de 1 (o relatório não ajudou) a 5 (decidiu só com ele), e a altura é quantos relatórios receberam a nota, separados em diagnóstico certo e errado. Barras altas à direita querem dizer que o relatório bastou.",
    "g-git-pares": "cada barra é um commit que mexeu nas cobaias, comparado com o commit anterior que também mexeu nelas, e a altura é quantos dos cenários base a seleção pelo diff do Git mandaria rodar. A cor diz o veredito: barra cheia na cor de alerta é a regra 1 (um arquivo da aplicação fora do mapa manda rodar tudo); barra parcial é a seleção pelos arquivos no mapa; barra vazia quer dizer que só arquivos ignorados mudaram, e vale a rodada completa periódica.",
    # ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q3) o "Como ler" dos dois gráficos da aba "Árvore de decisão".
    # ! Motivo: gráfico novo entra com o texto aqui, e o teste acusa se faltar.
    "g-arvore-rotulos": "cada linha é uma corrida, e as cores dividem as afirmações das árvores dela pela origem: observado é o que o código mediu, conferido é o que ele checou do que o modelo disse, declarado é o que o modelo escreveu sem garantia, e desconhecido é o que faltou na trilha. Quanto maior a parte do observado e do conferido, mais a árvore se apoia em medida, e menos em texto do modelo.",
    "g-arvore-confianca": "cada linha é uma corrida, e as cores contam os casos por faixa de confiança do agente, lida na probabilidade da causa respondida contra os cortes da calibração: alta, média e baixa. A barra só diz quantos casos caíram em cada faixa; a taxa de acerto de cada faixa na corrida de calibração está escrita em cada árvore.",
}

# texto de cada figura estática, pelo número
COMO_LER_FIGURA = {
    "01": "cada barra é um modelo, e a altura é a parcela de casos com a causa certa, juntas as três formas de prompt.",
    "02": "cada grupo é um modelo, e cada cor, uma forma de prompt. Barras de alturas parecidas no grupo querem dizer que a forma do prompt pouco importou para aquele modelo.",
    "03": "cada linha é um modelo e cada coluna, uma classe de defeito. O número é a porcentagem de acerto, e quanto mais escura a célula, maior ele é.",
    "04": "cada grupo é um modelo, e cada cor, um nível de dificuldade. Se o difícil não fica abaixo do fácil, o nível não explica o que o modelo acerta.",
    "05": "cada ponto é um modelo. Quanto mais alto, mais acerta; quanto mais à esquerda, menos tempo leva por resposta. O melhor lugar é o canto de cima, à esquerda.",
    "06": "cada barra é a parcela de respostas bem formatadas, mas com a causa errada: o erro que passa despercebido. Quanto menor, melhor.",
    "07": "cada grupo é um modelo: sem biblioteca, com a biblioteca inteira no prompt e com os três verbetes recuperados. A última barra acima das outras quer dizer que recuperar rende mais que entregar tudo.",
    "08": "cada grupo é um modelo, e a linha tracejada é o acerto dele sem documentação. Azul: só o verbete certo. Laranja: verbetes parecidos, mas errados. Verde: um verbete errado com um registro falso.",
    "09": "cada ponto é um modelo numa condição. O eixo de baixo é o tempo gasto lendo o prompt, e o da esquerda, o acerto. Ponto mais à direita sem subir quer dizer que ler mais não trouxe mais acerto.",
    "10": "cada grupo é uma forma de guardar os pesos do mesmo modelo. A barra azul é a forma padrão, e a laranja, a variante; o texto acima diz quantas respostas mudaram de lado. Barras baixas nas duas querem dizer que mais precisão não tirou o modelo do piso.",
    "11": "cada grupo é um modelo, e as barras separam três perguntas: o verbete certo chegou ao modelo, a resposta citou um verbete recebido e a causa está certa. Citar muito e acertar pouco quer dizer que o modelo usa a documentação, mas não acerta com ela.",
    "12": "cada quadro é um modelo, com o acerto por versão da biblioteca. A linha cheia são os 36 casos de avaliação, e a tracejada, os 54 de aprendizado. Linha reta quer dizer que a biblioteca não mudou nada para aquele modelo.",
    "13": "cada grupo é um modelo, e cada barra, uma versão da biblioteca. A altura é a parcela dos 36 casos em que o verbete certo ficou entre os três entregues. Barras iguais querem dizer que escrever mais não mudou o que a busca encontra.",
    "14": "cada quadro é um modelo. Verde são as propostas aceitas; laranja, as recusadas, por motivo; azul, os casos em que o modelo decidiu não propor nada. As escalas diferem de um quadro para outro.",
    "15": "cada linha é um modelo, e a altura é o tamanho da biblioteca dele em cada versão. A linha tracejada é o tamanho da original. Linha subindo muito quer dizer que o modelo escreve muito; linha colada na tracejada, que nada do que ele escreveu entrou.",
    "16": "cada grupo é um modelo, e cada tom, uma etapa, do mais claro para o mais escuro. Compare os tons dentro do grupo: escurecer e subir quer dizer que a etapa ajudou. \"Sem dado\" é modelo que não rodou ali.",
    "17": "cada ponto é um modelo numa etapa. Quanto mais alto, mais acerta; quanto mais à esquerda, menos tempo por caso. O marcador vazado é a Fase 2-A, medida em outra máquina, e por isso o tempo dele não se compara com os demais.",
    "18": "cada ponto é um modelo com a biblioteca num certo estado, e a linha vertical é a margem de incerteza. Os pontos verdes com contorno são os que nenhum outro supera ao mesmo tempo em acerto, tempo e risco. Entre versões da biblioteca de um mesmo modelo, o tempo não se compara, porque foi medido em momentos diferentes da corrida.",
}

# figuras que repetem um gráfico da mesma aba, ou que detalham o que o gráfico já mostra: ficam recolhidas
FIGURAS_RECOLHIDAS = {"07", "11", "12", "13", "14", "15", "16", "18"}

# tabelas de texto que são o conteúdo da aba, e não dados de um gráfico: (aba, primeira coluna). O resto vai para "Mais informações".
TABELAS_A_VISTA = {
    ("hipoteses", "Hipótese"), ("fechamento", "#"), ("fechamentof4", "Regra"),
    ("roadmap", "Frente"), ("roadmap", "Ponto"), ("roadmap", "Caso corrigido"),
    # ! Alteração de IA - Revisar: (05/11/2026, decisão 92) a tabela dos casos para olhar fica à vista na aba da conferência.
    # ! Motivo: no painel publicado ela saiu recolhida em "Mais informações", e é por ela que o Eric começa a conferência da ficha 46.
    ("conferencia", "Caso"),
    # ! Alteração de IA - Revisar: (07/11/2026) o mapa dos vereditos e as decisões do quadro ficam à vista na aba da Pós-Fase 4.
    # ! Motivo: são o conteúdo da aba, não os dados de um gráfico; é por eles que o Eric responde as fichas 53 e 54.
    ("posfase4", "Leitura"), ("posfase4", "Ficha"),
    # ! Alteração de IA - Revisar: (07/11/2026, Pós-Fase 4, Q2) a tabela das oito métricas com o limiar e a fonte, e a do que o plano antecipou para as frases, ficam à vista na aba dos filtros de texto.
    # ! Motivo: são o conteúdo da aba (o plano pede cada métrica com o limiar e a fonte declarados), não os dados de um gráfico.
    ("texto", "Métrica"), ("texto", "Grupo"),
    # ! Alteração de IA - Revisar: (10/11/2026, decisão 118) o mapa das opções e as fichas respondidas ficam à vista na aba "Fluxo do agente".
    # ! Motivo: são o conteúdo da aba (o que já é assim, o que espera decisão e o que sai), não os dados de um gráfico; é por eles que o Eric responde as fichas 65 a 67.
    ("fluxo", "Tema"), ("fluxo", "Ficha"),
}

# ! Alteração de IA - Revisar: (05/11/2026) a resposta de cada aba em linguagem direta, sem número; os cartões e os gráficos trazem os números, e o parágrafo antigo, com todos eles, fica em "Mais informações".
# ! Motivo: o primeiro parágrafo dessas abas era o resultado inteiro numa frase só ("b + c = 17, limite da regra R2 = 3; p = 0,000"), o que o Eric chamou de "cuspir dados". Quando a leitura vigente de uma aba mudar (18c e 21c, por exemplo), reler a frase dela aqui: é texto escrito à mão, e o parágrafo antigo, que continua gerado dos JSON, é a referência.
RESPOSTA_SIMPLES = {
    "decisao": "O modelo foi escolhido por uma regra escrita antes de ver os resultados: mais acerto nos casos de avaliação, sem piorar com a própria biblioteca. Depois, os testes de robustez conferiram se a escolha dependia da sorte dos casos.",
    "comparativo": "Em alguns pontos, mas em nada que mude a escolha. O Coder fica à frente em diferenças pequenas, quase todas nos casos de aprendizado; nos casos de avaliação, o qwen2.5:7b vence com todas as versões da biblioteca. Nos casos inéditos o Coder passa à frente, dentro da variação normal entre corridas, e isso fica como limitação declarada (decisão 73).",
    "tresb": "Só em parte. Em casos que nenhum modelo tinha visto, o ganho da primeira versão da biblioteca não se repete, e o da terceira é pequeno demais para este número de casos comprovar. O resto da aba mostra as demais medidas da fase e o quanto o resultado varia sozinho entre corridas iguais.",
    "recuperador": "Não. Medida nesta máquina, a busca por palavras com sinais em código acha o verbete certo mais vezes que a busca por significado (embedding), e a mistura das duas fica abaixo da primeira sozinha. A busca híbrida saiu do desenho da Fase 4 (decisão 61).",
    "ablacao": "Não. Sem o ajuste por instrução, o modelo pequeno copia a forma dos verbetes, mas inventa a causa, e não acerta nenhum caso. Com o ajuste e do mesmo tamanho, acerta muito pouco. O ajuste é necessário, mas não basta: o piso da família está no tamanho do modelo.",
    "pesquisa": "Cada tópico foi pesquisado por um agente, cada afirmação foi verificada por outro agente contra a fonte, e a síntese entrou no Memorial, com as referências na norma. Esta aba mostra o tamanho do levantamento e o que dele entrou no projeto.",
    "cruzada": "Não é da biblioteca sozinha. Os dois modelos Coder leram a biblioteca escrita pelo qwen2.5:7b, nos mesmos casos e com a mesma busca: um ganhou pouco, e o outro perdeu. Lida por quem a escreveu, ela rende mais. Por isso o padrão do agente é o modelo com a biblioteca que ele mesmo escreveu (decisão 69).",
    "colibri": "Só no limite, e não para o agente. O colibri roda modelos gigantes lendo do disco, a cada token, só a parte que o modelo aciona. Nesta máquina, quase nenhum cabe com folga, e nas máquinas maiores em que foi medido ele ainda levaria bem mais tempo que um diagnóstico de hoje. A decisão 75 fechou essa via como motor do agente.",
    "atlas": "Dá para ver. O atlas mostra que verbetes a busca entrega para cada tipo de defeito e o que o modelo faz com eles. Quando a busca aponta a classe certa, o modelo acerta bem mais, e os verbetes novos que ele mesmo escreveu nunca chegaram ao contexto de nenhum caso.",
    "reproducao": "Pouco mais da metade dos casos de avaliação, e mais nos inéditos. Todo caso que tem uma página por onde passar e um modo de falha na API reproduz; os outros não passam pela tela. Esta corrida roda sem modelo: só confere se a falha aparece.",
    "calibracao": "Entregar 3 verbetes ao modelo acerta mais que entregar 5, e a probabilidade que o modelo dá à própria resposta serve para separar o que merece revisão. Com isso, cada diagnóstico sai com um selo de confiança: alto, médio ou baixo.",
    # ! Alteração de IA - Revisar: (07/11/2026, Pós-Fase 4, Q2) a resposta da aba dos filtros de texto, sem número.
    # ! Motivo: a regra das abas é a resposta em linguagem direta; os números ficam nos cartões, nos gráficos e no parágrafo recolhido.
    # ! Alteração de IA - Revisar: (08/11/2026) a resposta da aba "O que chega ao analista" cita o fechamento da ficha 56 (decisão 108, opção a: o limiar de frase fica o calibrado).
    # ! Motivo: o Eric respondeu a ficha no quadro da sessão em 08/11/2026; sem a frase, a resposta deixaria o limiar de frase como pendente.
    "texto": "Sim nos relatórios, e em parte nos verbetes. Depois do ajuste do molde, todo relatório v3 passa nos filtros em código: explica cada termo da lista fechada na primeira vez que o usa, cita como citação o que veio do caso e do navegador e não repete as mesmas frases em blocos vizinhos; os relatórios v2 reprovavam todos. Na camada de leitura, depois da curadoria, todas as leituras passam, contra uma parte dos verbetes como estão; a curadoria foi feita por um analista, a quem o Eric passou as leituras, e o Claude consertou o que era fato errado ou formato quebrado. Os limiares vêm do corpus dos comentários deste repositório e são declarados como calibração, e o limiar de frase ficou o calibrado por decisão do Eric (ficha 56, fechada em 08/11/2026, decisão 108); o Flesch é só alarme.",
    # ! Alteração de IA - Revisar: (06/11/2026, decisão 98) a frase da aba diz o que a regra que compara os dois lados olha.
    # ! Motivo: o Eric fixou, antes da corrida 18d, que a regra conta os casos que a tela perde para o caso escrito; a frase antiga só dizia "fora do limite", sem dizer de quê.
    "tela": "Não em todos os casos, mas a tela não perde mais do que a regra aceita. Depois que a busca passou a usar o que o caso mede contra a tela normal, o verbete certo chega ao modelo em quase todos os casos, e o agente passou a acertar mais lendo da tela do que lendo o caso escrito, também em casos que a busca nunca tinha visto. O que a tela ainda perde é quase sempre a mesma confusão: item faltando na lista lido como resposta cortada. Isso não quer dizer que o modelo lê melhor da tela: o caso da tela leva uma medida que o caso escrito não tem (decisões 97 e 98).",
    "cura": "Sim, nas quebras armadas nesta corrida: o código achou outro seletor e o roteiro passou de novo em todas, em menos de um segundo, sem usar o modelo. Os 100% vêm do desenho da corrida: o elemento certo continua na página, e um sinônimo no lugar do texto não seria curado.",
    "biblioteca": "Só em parte. Os filtros em código seguram a maior parte do que o modelo propõe, mas o que sobra não mudou nenhum acerto nos casos inéditos: não piorou, e também não ajudou. A marca de corrigido funciona porque é dada em código; o modelo, sozinho, não percebe a correção.",
    "cenarios": "Todos os cenários chegaram ao resultado, em pouco mais de um minuto cada, com o prompt dentro do limite. Encurtar o prompt tirou cerca de um terço do tempo, sem mudar nenhuma causa, e os sinais novos da busca não mudaram esse resultado. É um ensaio, com uma repetição por cenário e sem a comparação com pessoas: serve para estimar a Fase 5, não para dizer se esse tempo é bom.",
    # ! Alteração de IA - Revisar: (06/11/2026) a resposta da aba da corrida 24, sem número, e a do fechamento, com a corrida feita.
    # ! Motivo: a regra das abas é a resposta em linguagem direta; o fechamento ainda dizia que faltava a corrida dos inéditos.
    "ineditosf4": "Menos do que nos casos de avaliação. Em texto, o agente acerta cerca de sete em cada dez casos que a biblioteca nunca viu, contra quase nove em dez nos casos de avaliação, e o que mais pesa é de novo o verbete certo chegar ao modelo. A classe de tradução é onde ele mais erra. Os dois conjuntos não são os mesmos casos, então a diferença não mede só a biblioteca, e esta corrida não diz quanto a biblioteca ajuda neles, porque não houve leitura sem ela.",
    "experimento": "Não dá para dizer que mudam. Tanto o exemplar resolvido quanto os rótulos em palavras trocam a resposta em alguns casos, para os dois lados, e o saldo fica dentro do que corridas iguais já variam. O prompt do agente continua como está (decisão 91), e o número vai para o TCC.",
    "trilha": "Em parte. Com as intervenções em todos os casos, o sinal principal quase não separa erro de acerto; contado só onde um gatilho dispararia, separa melhor, mas essa conta sai de uma corrida que não rodou assim. A trilha registra a mudança no passo certo, como esperado. A corrida teve poucos erros, e a medida com revisor humano não foi feita.",
    "fechamentof4": "Nas regras, sim. Todas as regras do plano foram cumpridas, algumas com ressalva, inclusive a que compara a tela com o caso escrito, que fechou com a busca nova e no limite exato. O limite do prompt passou a ser cumprido com o caso encurtado. Falta a medida com revisor humano, que está em aberto e será feita depois da Pós-Fase 4. A corrida dos inéditos rodou, com os casos conferidos, e a biblioteca final acerta menos neles do que nos casos de avaliação. Antes da Fase 5 vem a Pós-Fase 4.",
    # ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q4) a resposta da aba "Barra e Git", sem número.
    # ! Motivo: a regra das abas é a resposta em linguagem direta; os números ficam nos cartões, nos gráficos e no parágrafo gerado, em "Mais informações".
    "progresso": "Em parte, nos dois casos. A barra estima o tempo pelas taxas que o modelo mostrou nas corridas anteriores desta máquina e acerta na média, mas cada inferência pode fugir cerca de um quinto, quase sempre na leitura do prompt, porque o Ollama reaproveita parte do prompt anterior e isso só se sabe depois. Por isso ela nunca para: chega a 90% no tempo estimado e segue devagar até a resposta chegar. A seleção pelo diff do Git funciona no histórico real do repositório: aponta os cenários e os verbetes atingidos por cada arquivo, roda tudo quando um arquivo da aplicação está fora do mapa e registra o que deixou de rodar; o que ela ainda não prova é quanto perderia, porque isso exige rodar os cenários.",
    # ! Alteração de IA - Revisar: (10/11/2026, Pós-Fase 4, pacote Q5) a resposta da aba "Revisão humana", sem número; corrigida no mesmo dia para dizer que quase todas as
    # respostas vieram de um analista e que o tempo de leitura não foi medido (decisão 114): a primeira versão dizia que o revisor tinha decidido em meio minuto.
    # ! Motivo: a regra das abas é a resposta em linguagem direta; os números ficam nos cartões, nos gráficos e no parágrafo gerado, em "Mais informações".
    "semnotas": "Ainda não se sabe: a corrida que mede isso está pronta e espera o Eric rodar. O que já dá para dizer sem o modelo é que as notas chegam a todos os casos: cada contexto das corridas de referência trazia ao menos uma nota, e quase todas estão escritas como instrução. Sem elas, o texto entregue ao modelo muda em todos os casos, mas o verbete da causa certa continua entre os entregues nos mesmos casos de antes. A regra do veredito foi escrita antes da corrida: a diferença só conta se passar no teste pareado dos casos.",
    "revisaov3": "Sim, na maior parte das vezes, com uma ressalva sobre como foi lido. Os relatórios foram lidos por um analista de QA da empresa, que não participou do projeto nem conhecia o agente; o Eric passou cada relatório a ele e digitou ou colou a resposta na página. Lendo o relatório v3 com a árvore de decisão, ele aceitou quase todos os diagnósticos certos, recusou quase todos os errados e achou onde o agente errou em quase todos os errados, com a nota máxima de utilidade na maioria. Os poucos certos que ele recusou foram respostas fora dos verbetes entregues, que ele tratou como erro do agente. O tempo de leitura não foi medido, porque a página mediu a troca entre os dois e não a leitura, e não foi declarado o que ele recebeu para ler nem se usou alguma ferramenta.",
    # ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q3) a resposta da aba "Árvore de decisão", sem número.
    # ! Motivo: a regra das abas é a resposta em linguagem direta; os números ficam nos cartões, nos gráficos e no parágrafo gerado, em "Mais informações".
    "arvore": "Sim, para cada caso. A árvore mostra, na ordem, o que o modelo leu depois da poda e por qual regra, que verbetes a busca entregou e quais ficaram de fora, a causa escolhida contra a segunda com a confiança em palavras, e a cura do localizador quando houve, com os candidatos descartados e o motivo. Cada frase diz de onde veio: o que o código mediu, o que ele conferiu do que o modelo disse, o que o modelo só declarou e o que faltou na trilha. O que o modelo escreveu fica à parte, e a taxa de acerto de cada faixa de confiança só aparece quando a calibração existe; sem ela, a frase diz que não sabe, em vez de inventar um número.",
    # ! Alteração de IA - Revisar: (10/11/2026, decisão 118) a resposta da aba "Fluxo do agente", sem número.
    # ! Motivo: a regra das abas é a resposta em linguagem direta; os números ficam nos cartões, nos gráficos e no parágrafo gerado, em "Mais informações".
    "fluxo": "Nenhuma das três entra no agente antes da Fase 5, e de cada uma sobra uma forma menor, feita em código. O roteiro de raciocínio escrito pelo modelo não entra: custa tempo, não tem ganho medido neste porte de modelo e estraga a leitura do selo de confiança; o que cabe é a lista de conferência feita em código, depois da resposta. Pedir ao modelo que reveja a própria resposta também não entra, porque neste porte a revisão troca mais certo por errado; um segundo passe disparado por sinal e com outra busca tem apoio na literatura, mas aqui alcançaria poucos erros, e o que falta é a primeira busca entregar o verbete certo. A separação de um analista de documentação tem apoio como desenho, e o valor dela está no rótulo dado por uma pessoa e nos portões que medem cada edição antes de aceitar, não em o modelo escrever melhor. As três viraram fichas, e a decisão é do Eric.",
    # ! Alteração de IA - Revisar: (10/11/2026, decisão 120) a resposta da aba "Segundo passe" (corrida 26), sem número, escrita para antes de a corrida rodar.
    # ! Motivo: a regra das abas é a resposta em linguagem direta; os números ficam nos cartões, nos gráficos e no parágrafo gerado, em "Mais informações". Quando a corrida rodar,
    # a sessão que ler o resultado troca este texto pelo que ele disser.
    "segpasse": "Ainda não se sabe: a corrida que mede isso está pronta e espera o Eric rodar. O que a conta sem modelo já diz é que o ganho possível é pequeno. Os dois sinais acendem em um terço dos casos e pegam a maior parte dos erros, mas só em poucos deles o verbete da causa certa está entre os que o segundo pedido entrega, e parte dos acertos perde no segundo pedido o verbete certo que tinha no primeiro. Por isso o resultado não tem como passar do corte do teste pareado: a corrida serve para contar quantos erros o segundo pedido conserta e quantas respostas certas ele estraga. A regra que escolhe entre as duas respostas foi escrita antes: fica a primeira, salvo quando a segunda dá outra causa, não acende sinal e é mais provável.",
    # ! Alteração de IA - Revisar: (10/11/2026, decisão 121) a resposta da aba "Analista de documentação", sem número: o que a medida M1 mostrou e o que a corrida 27 ainda vai medir.
    # ! Motivo: a regra das abas é a resposta em linguagem direta; os números ficam nos cartões, nos gráficos e no parágrafo gerado, em "Mais informações". Quando a corrida 27
    # rodar e as propostas forem revisadas, a sessão que ler o resultado completa este texto.
    "analista": "Em parte, e a segunda pergunta ainda não tem resposta. A primeira medida rodou sem modelo, sobre as propostas que o modelo já tinha feito. O portão que recusa texto escrito como instrução barraria quase tudo, inclusive as poucas edições que a pessoa julgou corretas: do jeito que o modelo escreve hoje, ele esvazia o lote, e só serve junto de um prompt que peça a frase como ela vai ficar no verbete. O portão que refaz a busca barra uma parte das edições erradas sem perder nenhuma correta. Os filtros de texto barram pouco. Juntos, os três deixariam passar quase nada, e o pouco que passa a pessoa tinha julgado errado: nenhum portão em código diz se a frase é verdadeira, e a aprovação de uma pessoa continua sendo a porta final. Se a entrada própria e uma proposta por caso mudam o que o modelo escreve é o que a corrida seguinte mede, e ela espera o Eric rodar.",
    # ! Alteração de IA - Revisar: (07/11/2026) a resposta da aba da Pós-Fase 4, sem número.
    # ! Motivo: a regra das abas é a resposta em linguagem direta; os números ficam nos cartões e no parágrafo gerado, em "Mais informações".
    "posfase4": "Dividida. O que muda o que o analista lê (o relatório no molde do relatório de defeitos do syllabus, a camada de leitura dos verbetes, os filtros, a árvore de decisão e a barra de progresso) entra antes da Fase 5; o hub à imagem de uma pull request e a integração com o Git ficam para depois dela. Tudo roda na máquina do dev, sem VM. Dos oito repositórios, nenhum entra como peça do agente: ficam três ideias e dois candidatos futuros. O plano foi aprovado em 07/11/2026, e o primeiro pacote começa na próxima sessão.",
}

# ! Alteração de IA - Revisar: (05/11/2026) os cartões de corrida ficam à vista só no Roadmap e no fechamento da Fase 4; nas outras abas, em "Mais informações".
# ! Motivo: cada cartão traz o comando e o resultado inteiro da corrida numa frase de centenas de caracteres, e nas abas por tópico eles repetiam, depois do gráfico, os números que o Eric pediu para tirar da frente.
CORRIDAS_A_VISTA = {"roadmap", "fechamentof4"}

CSS = """
.como-ler{background:var(--acento2);border-left:3px solid var(--acento);border-radius:0 6px 6px 0;padding:8px 12px;margin:8px 0 14px;font-size:14px;max-width:none}
details.mais-info{margin:10px 0}details.mais-info>summary{font-weight:600;color:var(--ink2)}
.kpi b{overflow-wrap:anywhere}
"""

_FIM_TABELA = "</table></div>"
_TOKEN = re.compile(r'<section id="([^"]+)"|<details\b|</details>|<h([123])\b[^>]*>(.*?)</h\2>|<figure><img|<div class="filtros filtro-tabela"[^>]*>|<div class="tabela[^"]*"[^>]*>|<div class="corridas">', re.S)
_SEM_TAG = re.compile(r"<[^>]+>")


def _como_ler(texto: str) -> str:
    return f'<p class="como-ler"><strong>Como ler:</strong> {texto}</p>'


def _fim_do_div(texto: str, ini: int) -> int:
    """Posição logo depois do </div> que fecha o <div> que começa em `ini`."""
    prof = 0
    for m in re.finditer(r"<div\b|</div>", texto[ini:]):
        prof += 1 if m.group(0) == "<div" else -1
        if prof == 0:
            return ini + m.end()
    raise ValueError("div sem fechamento")


def _recolher(main: str) -> str:
    """Percorre a página na ordem: o que está fora de um <details> e não é conteúdo da aba vai para um bloco "Mais informações"."""
    saida: list[str] = []
    pos = 0
    prof = 0
    aba = ""
    titulo = ""
    vistos: dict[tuple[str, str], int] = {}
    i_titulo = -1

    def tira_o_que_acompanha() -> str:
        """Antes de recolher: a nota colada na tabela vai junto, e o título sem mais nada embaixo sai, porque o nome dele já vira o do bloco."""
        trecho = saida[-1] if saida else ""
        notas = re.fullmatch(r'\s*((?:(?:<p class="nota[^"]*">|<p>Blocos? )(?:(?!</p>).)*</p>\s*)*)', trecho, re.S)
        if not notas:
            return ""
        saida[-1] = ""
        if len(saida) - 2 == i_titulo and i_titulo >= 0:
            saida[i_titulo] = ""
        return notas.group(1).strip()

    def resumo(rotulo: str) -> str:
        chave = (aba, rotulo)
        vistos[chave] = vistos.get(chave, 0) + 1
        return f"Mais informações: {rotulo}" + (f" ({vistos[chave]})" if vistos[chave] > 1 else "")

    while True:
        m = _TOKEN.search(main, pos)
        if not m:
            saida.append(main[pos:])
            return "".join(saida)
        saida.append(main[pos:m.start()])
        t = m.group(0)
        pos = m.end()
        if t.startswith("<section"):
            aba, titulo = m.group(1), ""
            saida.append(t)
        elif t.startswith("<details"):
            prof += 1
            saida.append(t)
        elif t == "</details>":
            prof -= 1
            saida.append(t)
        elif m.group(2):
            titulo = _SEM_TAG.sub("", m.group(3)).strip()
            saida.append(t)
            i_titulo = len(saida) - 1 if m.group(2) != "1" else -1
        elif t.startswith('<div class="corridas"'):
            fim = _fim_do_div(main, m.start())
            bloco = main[m.start():fim]
            pos = fim
            if prof or aba in CORRIDAS_A_VISTA:
                saida.append(bloco)
            else:
                nota = tira_o_que_acompanha()
                saida.append(f'<details class="mais-info"><summary>{resumo(titulo or "as corridas")}</summary>{nota}{bloco}</details>')
        elif t.startswith("<figure"):
            fim = main.index("</figure>", m.start()) + len("</figure>")
            bloco = main[m.start():fim]
            pos = fim
            num = re.search(r"<figcaption>Figura (\d+)", bloco)
            n = num.group(1) if num else ""
            corpo = bloco + (_como_ler(COMO_LER_FIGURA[n]) if n in COMO_LER_FIGURA else "")
            if n in FIGURAS_RECOLHIDAS and prof == 0:
                nome = _SEM_TAG.sub("", re.search(r'alt="([^"]*)"', bloco).group(1))
                corpo = f'<details class="mais-info"><summary>{resumo("figura " + n + ", " + nome)}</summary>{corpo}</details>'
            saida.append(corpo)
        else:
            # tabela, com a barra de filtro dela quando há: os dois ficam juntos
            ini = m.start()
            if "filtro-tabela" in t:
                fim_filtro = main.index("</div>", m.end()) + len("</div>")
                prox = re.compile(r'\s*<div class="tabela[^"]*"[^>]*>').match(main, fim_filtro)
                if not prox:
                    saida.append(t)
                    continue
                ini_tabela = prox.start()
            else:
                ini_tabela = ini
            fim = main.index(_FIM_TABELA, ini_tabela) + len(_FIM_TABELA)
            bloco = main[ini:fim]
            pos = fim
            th = re.search(r"<th[^>]*>(.*?)</th>", bloco, re.S)
            primeira = _SEM_TAG.sub("", th.group(1)).strip() if th else ""
            if prof or (aba, primeira) in TABELAS_A_VISTA:
                saida.append(bloco)
            else:
                nota = tira_o_que_acompanha()
                saida.append(f'<details class="mais-info"><summary>{resumo(titulo or "dados")}</summary>{nota}{bloco}</details>')


def _respostas_simples(main: str) -> str:
    """Troca o primeiro parágrafo das abas de RESPOSTA_SIMPLES pela frase direta e leva o parágrafo antigo, com os números, para "Mais informações"."""
    for aba, texto in RESPOSTA_SIMPLES.items():
        m = re.search(rf'(<section id="{aba}"[^>]*>.*?)<p class="lead">(.*?)</p>', main, re.S)
        if not m or "</section>" in m.group(1):
            continue  # o teste confere na página real que toda frase daqui entrou
        novo = (f'{m.group(1)}<p class="lead">{texto}</p><details class="mais-info"><summary>Mais informações: a resposta com todos os números</summary>'
                f'<p>{m.group(2)}</p></details>')
        main = main[:m.start()] + novo + main[m.end():]
    return main


def aplicar(pagina: str) -> str:
    """Aplica as duas regras só dentro de <main>, para não tocar em estilos e scripts, e acrescenta o estilo dos blocos."""
    ini = pagina.index("<main>")
    fim = pagina.index("</main>", ini)
    main = _recolher(_respostas_simples(pagina[ini:fim]))

    def com_leitura(m: re.Match) -> str:
        texto = COMO_LER_GRAFICO.get(m.group(2))
        return m.group(1) + (_como_ler(texto) if texto else "")

    main = re.sub(r'(<div class="chart[^"]*"><canvas id="([^"]+)"></canvas></div>)', com_leitura, main)
    return (pagina[:ini] + main + pagina[fim:]).replace("</style>", CSS + "</style>", 1)
