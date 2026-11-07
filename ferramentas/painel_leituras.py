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
