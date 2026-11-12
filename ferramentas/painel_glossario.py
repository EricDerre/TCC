# ! Alteração de IA - Revisar: arquivo novo (11/11/2026) com o glossário do painel: a lista dos termos e dos métodos (`TERMOS`), a aba "Glossário e métodos"
# (`secao_glossario`), a marcação do termo na primeira vez em que ele aparece em cada aba, com a explicação curta ao passar o mouse, tocar ou focar (`anotar`,
# `CSS`, `script`), e a lista "Termos e métodos desta aba" no fim de cada aba.
# ! Motivo: o Eric pediu, em 11/11/2026, que o painel explique métodos, palavras específicas e termos técnicos onde eles aparecem, como o documento do TCC faz,
# porque ele vai ser lido por quem não acompanhou o projeto; e que todo método venha com um resumo na chamada, com o que o projeto faz de diferente e a citação.
# A explicação fica num lugar só (aqui), para a mesma palavra não ganhar duas definições, e segue o glossário e a seção 5.7 do documento do TCC, em linguagem mais
# direta. As fontes são copiadas de `referencias.md` pela chave (o bloco "Métodos clássicos de medida", de 11/11/2026, traz a referência original de cada método,
# conferida uma a uma), para a mesma referência não ser escrita em dois lugares. Nenhum número de resultado entra nas explicações.
"""Glossário do painel: termos, métodos, a aba e a marcação nas outras abas."""
from __future__ import annotations

import html
import json
import re

GRUPOS =[("metodo", "Métodos de medida e de comparação"), ("modelo", "O modelo de linguagem e a execução"), ("agente", "O agente e o teste"),
          ("biblioteca", "A biblioteca de documentação"), ("projeto", "A organização do projeto")]

# Cada termo: id, nome, grupo, padrões (expressões regulares, a mais específica primeiro), curto (a dica), explicacao, no_projeto (o que o projeto faz, e o que
# faz de diferente do método como ele costuma ser usado) e fontes ("ref:<começo da linha em referencias.md>"; a chave precisa achar uma linha só).
TERMOS: list[dict] = [
    {"id": "wilson", "termo": "Intervalo de Wilson", "grupo": "metodo", "padroes": [r"intervalos? de confiança de 95% pelo método de escore de Wilson", r"intervalos? de Wilson", r"IC de Wilson", r"Wilson 95%", r"\bWilson\b"],
     "curto": "Faixa em que a taxa verdadeira provavelmente está. Funciona com poucos casos e nunca passa de 0% nem de 100%.",
     "explicacao": "Uma taxa medida em poucos casos é uma amostra, não a taxa verdadeira. O intervalo de Wilson diz entre quais valores a taxa verdadeira deve estar, com 95% de confiança.",
     "no_projeto": "Toda taxa de acerto do projeto vem com esse intervalo. Ele entrou no lugar do intervalo mais comum, o de Wald, que erra a cobertura quando os casos são poucos, como os casos de avaliação deste projeto.",
     "fontes": ["ref:WILSON, E. B.", "ref:BOWYER, S."]},
    {"id": "ic", "termo": "Intervalo de confiança (IC)", "grupo": "metodo", "padroes": [r"intervalos? de confiança", r"\bIC\b"],
     "curto": "A faixa de valores em que o valor verdadeiro provavelmente está. Quanto menos casos, mais larga a faixa.",
     "explicacao": "Um resultado medido numa amostra muda se a amostra mudar. O intervalo de confiança de 95% mostra o tamanho dessa incerteza: duas taxas com faixas que se cruzam muito não podem ser dadas como diferentes só pelo número.",
     "no_projeto": "Para as taxas, o projeto usa o intervalo de Wilson. Na escolha do modelo, usa também o bootstrap.",
     "fontes": []},
    {"id": "mcnemar", "termo": "Teste de McNemar", "grupo": "metodo", "padroes": [r"teste exato de McNemar", r"teste de McNemar", r"McNemar exato", r"\bMcNemar\b", r"teste pareado exato", r"teste pareado"],
     "curto": "Compara duas condições nos mesmos casos, olhando só os casos em que uma acertou e a outra errou.",
     "explicacao": "Quando duas condições leem os mesmos casos, o que as separa são os casos em que elas discordam: b conta os que só a condição nova acertou, e c os que só a antiga acertou. O teste pergunta se a diferença entre b e c poderia aparecer só por acaso, e a resposta é o valor p.",
     "no_projeto": "O projeto usa a forma exata, de dois lados, porque os casos discordantes são poucos. A forma aproximada, mais comum, não serve para tão poucos casos.",
     "fontes": ["ref:McNEMAR, Quinn.", "ref:RASCHKA, S.", "ref:DIETTERICH, T. G."]},
    {"id": "valor-p", "termo": "Valor p", "grupo": "metodo", "padroes": [r"valor[- ]p\b", r"p abaixo de 0,05", r"p &lt; 0,05", r"p < 0,05"],
     "curto": "A chance de uma diferença daquele tamanho aparecer só por acaso. Abaixo de 0,05, o projeto trata a diferença como fora do ruído.",
     "explicacao": "O valor p não diz o tamanho da diferença nem se ela importa: diz só o quanto ela seria comum se as duas condições fossem iguais.",
     "no_projeto": "Com poucos casos, um p alto não prova que não há diferença. Por isso o projeto mostra junto o efeito mínimo detectável e toma as decisões pela soma de vários critérios.",
     "fontes": []},
    {"id": "bootstrap", "termo": "Bootstrap", "grupo": "metodo", "padroes": [r"\bbootstrap\b", r"reamostragens"],
     "curto": "Sorteia os casos de novo, com reposição, milhares de vezes, para ver quanto o resultado balança.",
     "explicacao": "Cada sorteio monta um conjunto de casos do mesmo tamanho, em que alguns casos se repetem e outros ficam de fora. Refazendo a conta em cada conjunto, vê-se em quantos deles a conclusão se mantém.",
     "no_projeto": "Foi usado na escolha do modelo, com semente fixa: a cada sorteio dos casos, qual combinação de modelo e biblioteca ficaria em primeiro.",
     "fontes": ["ref:EFRON, B."]},
    {"id": "acuracia-balanceada", "termo": "Acurácia balanceada", "grupo": "metodo", "padroes": [r"acurácia balanceada"],
     "curto": "Média do acerto calculado causa por causa. Cada causa pesa igual, então acertar só a causa mais comum não infla o número.",
     "explicacao": "No acerto simples, um modelo que responde sempre a mesma causa pode parecer bom se essa causa for frequente. Na acurácia balanceada, cada causa conta o mesmo, e esse modelo cai.",
     "no_projeto": "É a medida principal da escolha do modelo, porque o defeito que se esperava era justamente o modelo cair numa causa só.",
     "fontes": ["ref:BRODERSEN, Kay Henning", "ref:OPITZ, J.", "ref:COLLOT, S."]},
    {"id": "cochran", "termo": "Q de Cochran", "grupo": "metodo", "padroes": [r"Q de Cochran"],
     "curto": "Teste que diz se três ou mais condições, medidas nos mesmos casos, diferem entre si.",
     "explicacao": "É a extensão do teste de McNemar para mais de duas condições. Se ele não acusa diferença, as comparações duas a duas nem começam.",
     "no_projeto": "Usado para as quatro versões da biblioteca, de L0 a L3, antes de comparar cada uma com a original.",
     "fontes": ["ref:COCHRAN, W. G."]},
    {"id": "holm", "termo": "Correção de Holm", "grupo": "metodo", "padroes": [r"correção de Holm", r"\bHolm\b"],
     "curto": "Ajuste aplicado quando se fazem várias comparações de uma vez, para o acaso não passar por descoberta.",
     "explicacao": "Quanto mais comparações, maior a chance de alguma parecer significativa por sorte. A correção de Holm aperta o corte de cada uma, da mais forte para a mais fraca.",
     "no_projeto": "Aplicada às comparações duas a duas entre as versões da biblioteca.",
     "fontes": ["ref:HOLM, S.", "ref:GARCÍA, S."]},
    {"id": "g-cohen", "termo": "g de Cohen", "grupo": "metodo", "padroes": [r"g de Cohen"],
     "curto": "Tamanho do efeito num teste pareado: quanto os casos discordantes pendem para um dos lados.",
     "explicacao": "O valor p diz se a diferença pode ser acaso; o g diz se ela é grande ou pequena.",
     "no_projeto": "Aparece ao lado de cada valor p das comparações entre versões da biblioteca. O projeto usa a forma com sinal: zero quando as trocas se anulam, +0,5 quando toda troca foi para melhor e −0,5 quando toda foi para pior.",
     "fontes": ["ref:COHEN, J. **Statistical power", "ref:MANGIAFICO, S. S."]},
    {"id": "mde", "termo": "Efeito mínimo detectável", "grupo": "metodo", "padroes": [r"efeito mínimo detectável"],
     "curto": "A menor diferença que a amostra consegue mostrar. Com poucos casos, só diferenças grandes aparecem como significativas.",
     "explicacao": "É uma conta feita antes de ler o resultado: dado o número de casos, de que tamanho a diferença precisa ser para o teste acusar.",
     "no_projeto": "A conta supõe que um quinto dos casos discorde entre as duas condições. Ela mostra o limite da amostra pequena deste projeto: um ganho real pode existir e não aparecer no teste, e o relatório diz isso em vez de afirmar que não há efeito.",
     "fontes": []},
    {"id": "auroc", "termo": "AUROC", "grupo": "metodo", "padroes": [r"\bAUROC\b"],
     "curto": "Mede se uma nota de confiança separa acerto de erro: 0,5 é acaso e 1 é separação perfeita.",
     "explicacao": "A sigla quer dizer área sob a curva ROC. Sorteando um caso certo e um errado, é a chance de o certo ter a nota maior.",
     "no_projeto": "A nota medida é a probabilidade que o modelo deu à causa respondida. Foi por essa medida que ela virou o selo de confiança do agente.",
     "fontes": ["ref:FAWCETT, Tom."]},
    {"id": "bm25", "termo": "BM25, a busca por palavras", "grupo": "metodo", "padroes": [r"\bBM25\b", r"busca por palavras"],
     "curto": "Ordena os verbetes pelo quanto as palavras do caso aparecem neles, com mais peso para as palavras raras.",
     "explicacao": "É uma fórmula clássica de busca em texto. Ela não entende o significado: conta palavras, desconta as que aparecem em todo lugar e compensa o tamanho de cada documento.",
     "no_projeto": "É a busca do agente, com a ajuda de sinais calculados em código a partir do que mudou na tela. A busca por significado foi medida ao lado dela e não rendeu mais, por isso não entrou.",
     "fontes": ["ref:ROBERTSON, Stephen E.", "ref:MANNING, Christopher D."]},
    {"id": "hit-k", "termo": "hit@k e MRR", "grupo": "metodo", "padroes": [r"hit@\d", r"hit@k", r"\bMRR\b"],
     "curto": "hit@3 é a parcela dos casos em que o verbete certo está entre os três entregues. MRR mede em que posição ele costuma aparecer.",
     "explicacao": "São medidas da busca, e não do modelo: dizem se a documentação certa chegou ao prompt. O MRR é a média do inverso da posição do primeiro verbete certo: vale 1 quando ele vem em primeiro, 0,5 quando vem em segundo, e assim por diante.",
     "no_projeto": "O projeto acompanha a busca à parte do modelo, porque um diagnóstico errado pode vir de o verbete da causa certa não ter chegado ao prompt.",
     "fontes": ["ref:VOORHEES, Ellen M."]},
    {"id": "pareto", "termo": "Fronteira de Pareto", "grupo": "metodo", "padroes": [r"fronteira de Pareto", r"não dominad[ao]s?"],
     "curto": "Conjunto das opções em que nenhuma outra é melhor em tudo ao mesmo tempo.",
     "explicacao": "Uma opção sai da fronteira quando existe outra que é igual ou melhor em todos os critérios. As que ficam são as escolhas defensáveis.",
     "no_projeto": "Na escolha do modelo, os critérios foram a acurácia balanceada, o tempo por diagnóstico e o risco. Serviu para conferir se a combinação escolhida pela regra principal também se sustentava por esses três lados.",
     "fontes": []},
    {"id": "tpr-tnr", "termo": "TPR e TNR", "grupo": "metodo", "padroes": [r"TPR x TNR", r"TPR vezes TNR", r"\bTPR\b", r"\bTNR\b"],
     "curto": "TPR é a parcela dos erros que um sinal pega. TNR é a parcela dos acertos que ele deixa em paz. O produto dos dois vale 0,25 para um sinal jogado ao acaso.",
     "explicacao": "Um sinal de alerta só serve se pega os erros sem acender em tudo. Multiplicar as duas parcelas castiga o sinal que acerta de um lado só.",
     "no_projeto": "É a medida usada para avaliar a trilha do agente: se a divergência que ele sinaliza aponta os erros de verdade.",
     "fontes": ["ref:GUAN, Melody Y."]},
    {"id": "mttr", "termo": "MTTR", "grupo": "metodo", "padroes": [r"\bMTTR\b", r"tempo médio de reparo"],
     "curto": "Tempo médio de reparo: da detecção da falha até o resultado conferido.",
     "explicacao": "É a medida de quanto tempo o problema fica sem resposta.",
     "no_projeto": "Na quebra de localizador, o tempo vai até a reexecução passar. Na quebra de contrato, vai até o diagnóstico conferido em código, porque o agente não conserta a API. Os dois tempos não medem a mesma coisa e são lidos em separado.",
     "fontes": []},
    {"id": "task-success", "termo": "Task Success", "grupo": "metodo", "padroes": [r"Task Success"],
     "curto": "Parcela dos cenários em que o agente chegou ao resultado certo.",
     "explicacao": "É a taxa de sucesso da tarefa: de todos os cenários de falha, em quantos o agente terminou com o resultado esperado.",
     "no_projeto": "Na quebra de localizador, conta o roteiro que conclui sem erro depois da cura. Na quebra de contrato, conta o diagnóstico com a causa e o campo certos.",
     "fontes": []},
    {"id": "flesch", "termo": "Índice de Flesch", "grupo": "metodo", "padroes": [r"\bFlesch\b"],
     "curto": "Índice de facilidade de leitura, calculado do tamanho das frases e das palavras. Quanto maior, mais fácil de ler.",
     "explicacao": "A fórmula original foi feita para o inglês. Para o português existe uma adaptação, com outros pesos.",
     "no_projeto": "O projeto usa a fórmula adaptada ao português, com os pesos do NILC-Metrix, e só como alarme: um texto abaixo do corte acende um aviso, mas não é aprovado nem reprovado por esse número.",
     "fontes": ["ref:FLESCH, Rudolph.", "ref:MARTINS, Teresa B. F.", "ref:LEAL, Sidney Evaldo"]},
    {"id": "percentil", "termo": "Percentil 95", "grupo": "metodo", "padroes": [r"percentil 95"],
     "curto": "O valor abaixo do qual ficam 95% das medidas.",
     "explicacao": "Serve de corte: o que passa dele está entre os 5% mais extremos.",
     "no_projeto": "É assim que os filtros de texto foram calibrados: os limites vêm dos textos que o próprio repositório já tinha, e não de um número escolhido de antemão.",
     "fontes": []},
    {"id": "troca-de-rotulo", "termo": "Troca de rótulo e autoenvenenamento", "grupo": "metodo", "padroes": [r"trocas? de rótulo", r"autoenvenenamento"],
     "curto": "Casos que mudam de resposta entre duas condições, mesmo quando a média fica igual. Quando um certo vira errado depois de o modelo editar a biblioteca, o projeto chama de autoenvenenamento.",
     "explicacao": "A média pode esconder trocas: três casos passam a acertar, três passam a errar, e o total não muda. Contar as trocas mostra o que a média não mostra.",
     "no_projeto": "O autoenvenenamento foi critério de veto na escolha do modelo: uma biblioteca que estraga respostas certas não entra.",
     "fontes": ["ref:DUTTA, A."]},
    {"id": "pre-registro", "termo": "Regra pré-registrada", "grupo": "metodo", "padroes": [r"pré-registrad[ao]s?", r"fixad[ao] antes da corrida", r"regras? R\d"],
     "curto": "Regra escrita antes de ver o resultado, para o resultado não escolher a régua.",
     "explicacao": "Quem decide a regra depois de ver os números tende a escolher a regra que favorece o que queria concluir.",
     "no_projeto": "Cada corrida do projeto tem a regra de leitura escrita e testada antes de rodar, com o que conta como cumprido e o que vira limitação declarada.",
     "fontes": []},

    {"id": "llm", "termo": "Modelo de linguagem (LLM)", "grupo": "modelo", "padroes": [r"\bLLMs?\b", r"modelos? de linguagem", r"modelos? loca(?:l|is)", r"\bmodelos?\b"],
     "curto": "Programa que lê um texto e escreve a continuação mais provável. Aqui ele roda na própria máquina, sem internet.",
     "explicacao": "A sigla vem do inglês, large language model. O modelo não consulta a internet nem aprende durante o uso: responde só com o que recebeu no texto de entrada.",
     "no_projeto": "O agente usa um modelo pequeno, que cabe num computador de escritório sem placa de vídeo. O modelo lê o caso e a documentação e responde a causa da falha, o campo afetado e de onde tirou a resposta. A cura do localizador, as conferências e os relatórios são feitos em código.", "fontes": []},
    {"id": "token", "termo": "Token", "grupo": "modelo", "padroes": [r"\btokens?\b"],
     "curto": "Pedaço de palavra que o modelo lê e escreve. O tempo e o custo do modelo se medem em tokens.",
     "explicacao": "Uma palavra comum vira um ou dois tokens; uma palavra rara ou um nome de campo vira vários.", "no_projeto": "", "fontes": []},
    {"id": "prompt", "termo": "Prompt", "grupo": "modelo", "padroes": [r"\bprompts?\b"],
     "curto": "O texto inteiro entregue ao modelo: a instrução, os verbetes da documentação e os dados do caso.",
     "explicacao": "Mudar o formato do prompt muda a resposta do modelo, mesmo sem mudar o conteúdo.",
     "no_projeto": "A parte fixa do prompt está congelada e conferida por código a cada corrida, para duas corridas poderem ser comparadas.", "fontes": ["ref:SCLAR, M."]},
    {"id": "janela-de-contexto", "termo": "Janela de contexto", "grupo": "modelo", "padroes": [r"janela de contexto"],
     "curto": "Quanto texto o modelo consegue ler de uma vez. O que não cabe fica de fora.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "prefill", "termo": "Prefill", "grupo": "modelo", "padroes": [r"\bprefill\b"],
     "curto": "A parte do tempo que o modelo gasta lendo o prompt, antes de começar a responder.",
     "explicacao": "Num computador sem placa de vídeo, ler o prompt costuma demorar mais que escrever a resposta.", "no_projeto": "", "fontes": []},
    {"id": "temperatura", "termo": "Temperatura", "grupo": "modelo", "padroes": [r"\btemperatura\b"],
     "curto": "Quanto o modelo varia ao escolher cada palavra. O projeto usa um valor baixo, para a resposta quase não mudar entre execuções.",
     "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "quantizacao", "termo": "Quantização", "grupo": "modelo", "padroes": [r"quantizaç(?:ão|ões)"],
     "curto": "Versão comprimida do modelo, que cabe na memória de um computador comum ao custo de alguma precisão.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "probabilidade-da-resposta", "termo": "Probabilidade da resposta", "grupo": "modelo",
     "padroes": [r"probabilidade d[oa] (?:rótulo|resposta|causa respondida)", r"primeiro token d[oa] (?:rótulo|causa|resposta)", r"\blogprobs?\b"],
     "curto": "A chance que o próprio modelo deu à causa que respondeu, lida no primeiro pedaço da resposta.",
     "explicacao": "A cada pedaço que escreve, o modelo calcula a chance de cada alternativa. A chance da alternativa escolhida diz o quanto ele hesitou.",
     "no_projeto": "É o número que vira o selo de confiança. Ele é lido antes da temperatura e só no primeiro pedaço da causa, que é onde a escolha acontece.", "fontes": []},
    {"id": "selo", "termo": "Selo de confiança", "grupo": "modelo", "padroes": [r"selos? de confiança", r"selo (?:baixo|médio|alto)"],
     "curto": "Etiqueta baixo, médio ou alto que o agente põe em cada diagnóstico, pela probabilidade da causa respondida.",
     "explicacao": "O selo não diz se a resposta está certa: diz o quanto vale conferir. Selo baixo manda o caso para uma pessoa.",
     "no_projeto": "Os cortes entre baixo, médio e alto foram fixados na calibração, nos casos com resposta conhecida.", "fontes": []},
    {"id": "calibracao", "termo": "Calibração", "grupo": "modelo", "padroes": [r"calibraç(?:ão|ões)"],
     "curto": "A corrida que fixou os cortes do selo de confiança e quantos verbetes entregar ao modelo, medindo nos casos com resposta conhecida.",
     "explicacao": "", "no_projeto": "Mexer no prompt ou no que o modelo lê desfaz a calibração e pede medir de novo.", "fontes": []},
    {"id": "ollama", "termo": "Ollama", "grupo": "modelo", "padroes": [r"\bOllama\b"],
     "curto": "O programa que roda o modelo de linguagem na máquina local.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "ponte", "termo": "Ponte de versão", "grupo": "modelo", "padroes": [r"pontes? de versão", r"\bpareáve(?:l|is)\b"],
     "curto": "Quando o Ollama se atualiza, o projeto relê os mesmos casos na versão nova para provar que os resultados continuam comparáveis.",
     "explicacao": "A ponte compara caso a caso com a medida antiga. Se poucos casos mudam, as corridas das duas versões são pareáveis, isto é, podem ser comparadas.",
     "no_projeto": "É regra do projeto: nenhuma medida numa versão nova do Ollama sem a ponte antes.", "fontes": []},

    {"id": "e2e", "termo": "Teste de ponta a ponta (E2E)", "grupo": "agente", "padroes": [r"\bE2E\b", r"ponta a ponta"],
     "curto": "Um roteiro que usa o sistema como uma pessoa usaria, pela tela, do começo ao fim.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "qa", "termo": "QA", "grupo": "agente", "padroes": [r"\bQA\b"],
     "curto": "Garantia de qualidade: o trabalho de testar o sistema antes de ele chegar a quem usa.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "self-healing", "termo": "Cura de seletor (self-healing)", "grupo": "agente", "padroes": [r"self-healing", r"cura de seletor", r"\bautocura\b"],
     "curto": "Quando o roteiro quebra porque um elemento da tela mudou, o agente acha o elemento de novo e segue o teste.",
     "explicacao": "É o conserto do teste, e não do sistema: o botão continua lá, só mudou de nome ou de lugar.",
     "no_projeto": "A cura é feita em código, sem o modelo de linguagem, e só vale quando a reexecução do roteiro passa.", "fontes": []},
    {"id": "localizador", "termo": "Localizador ou seletor", "grupo": "agente", "padroes": [r"localizador(?:es)?", r"seletor(?:es)?"],
     "curto": "O endereço de um elemento da tela, como um botão, que o roteiro usa para clicar ou ler.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "cobaia", "termo": "Cobaias", "grupo": "agente", "padroes": [r"\bcobaias?\b", r"CobaiaFront", r"CobaiaAPI"],
     "curto": "Os dois sistemas de teste do projeto: um site em PHP e uma API. Neles as falhas são ligadas de propósito.",
     "explicacao": "A CobaiaFront é o site em PHP do Projeto CHULETA, de Pedro Henrique Torres Gonçalves, integrante do grupo, usado aqui como o sistema sob teste. A CobaiaAPI é uma API escrita para este projeto, com os modos de falha.",
     "no_projeto": "", "fontes": []},
    {"id": "falha-injetada", "termo": "Falha injetada", "grupo": "agente", "padroes": [r"falhas? injetadas?", r"injeção de falhas?", r"modos? de falha"],
     "curto": "Defeito ligado de propósito na cobaia, para saber de antemão qual é a resposta certa.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "contrato", "termo": "Contrato da API", "grupo": "agente", "padroes": [r"quebras? de contrato", r"contrato da API", r"falhas? de contrato"],
     "curto": "O combinado entre a tela e a API: quais campos vêm e de que tipo. Quando a API muda sem avisar, o contrato quebra.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "causa-raiz", "termo": "Causa raiz", "grupo": "agente", "padroes": [r"causas? raiz", r"\btaxonomia\b"],
     "curto": "O motivo de fundo da falha. O agente escolhe uma causa numa lista fechada, a taxonomia do projeto.",
     "explicacao": "A lista tem 23 causas, agrupadas em seis classes, cada uma com a pergunta que o analista faz para chegar a ela: da resposta ilegível até o efeito que a pessoa vê na tela.", "no_projeto": "", "fontes": []},
    {"id": "gabarito", "termo": "Gabarito", "grupo": "agente", "padroes": [r"\bgabaritos?\b"],
     "curto": "A resposta certa de cada caso, conhecida de antemão. O agente nunca a vê; ela só entra na conferência.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "caso-escrito", "termo": "Caso escrito e caso ao vivo", "grupo": "agente", "padroes": [r"casos? escritos?", r"casos? ao vivo", r"\bfixtures?\b"],
     "curto": "Caso escrito é a falha descrita em texto. Caso ao vivo é a mesma falha lida da tela, pelo navegador.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "ineditos", "termo": "Casos inéditos", "grupo": "agente", "padroes": [r"casos inéditos", r"\binéditos\b"],
     "curto": "Casos escritos depois, que nenhuma versão da biblioteca viu. Servem para saber se o resultado vale fora dos casos de sempre.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "particao", "termo": "Casos de aprendizado e de avaliação", "grupo": "agente", "padroes": [r"casos de avaliação", r"casos de aprendizado"],
     "curto": "Os casos foram divididos em dois grupos: nos de aprendizado o modelo vê a resposta certa; nos de avaliação, nunca.",
     "explicacao": "", "no_projeto": "Toda decisão do projeto é tomada nos casos de avaliação.", "fontes": []},
    {"id": "poda", "termo": "Poda", "grupo": "agente", "padroes": [r"\bpoda\b"],
     "curto": "Redução feita em código: da árvore da tela e do corpo da resposta, fica só o que importa para o passo em análise.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "arvore-de-acessibilidade", "termo": "Árvore de acessibilidade", "grupo": "agente", "padroes": [r"árvores? de acessibilidade"],
     "curto": "A descrição da tela que o navegador entrega a leitores de tela: botões, campos e textos, com nome e papel.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "playwright", "termo": "Playwright", "grupo": "agente", "padroes": [r"\bPlaywright\b"],
     "curto": "A ferramenta que abre o navegador e executa o roteiro de teste.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "trilha", "termo": "Trilha", "grupo": "agente", "padroes": [r"trilha de raciocínio", r"trilha aberta", r"\btrilhas?\b"],
     "curto": "O registro de cada passo do agente: o que ele viu, o que o modelo respondeu e o que o código conferiu.",
     "explicacao": "", "no_projeto": "O relatório que a pessoa lê é montado em código a partir da trilha.", "fontes": []},
    {"id": "arvore-de-decisao", "termo": "Árvore de decisão", "grupo": "agente", "padroes": [r"árvores? de decisão"],
     "curto": "A trilha de um caso contada em passos: o que foi lido, que verbetes entraram, a causa escolhida e a confiança.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "fonte-divergente", "termo": "FONTE divergente", "grupo": "agente", "padroes": [r"FONTE divergente"],
     "curto": "Sinal em código que acende quando o modelo cita um verbete que não recebeu, ou quando nenhum verbete entregue trata da causa respondida.",
     "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "adesao-apropriada", "termo": "Adesão apropriada", "grupo": "agente", "padroes": [r"adesão apropriada"],
     "curto": "A pessoa aceitar o diagnóstico quando ele está certo e recusar quando está errado.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "ctfl", "termo": "CTFL e ISTQB", "grupo": "agente", "padroes": [r"\bCTFL\b", r"\bISTQB\b", r"\bsyllabus\b"],
     "curto": "O programa de estudo da certificação básica de teste de software do ISTQB. O relatório do agente segue o molde de relatório de defeito dele.",
     "explicacao": "", "no_projeto": "", "fontes": ["ref:ISTQB."]},

    {"id": "verbete", "termo": "Verbete", "grupo": "biblioteca", "padroes": [r"\bverbetes?\b"],
     "curto": "Uma página da documentação que o agente consulta: o que é o defeito, como aparece e qual é a causa.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "biblioteca", "termo": "Biblioteca de documentação", "grupo": "biblioteca", "padroes": [r"biblioteca de produção", r"biblioteca de (?:conhecimento|documentação)", r"\bL1 curada\b", r"\bL0\b", r"\bbibliotecas?\b"],
     "curto": "O conjunto dos verbetes. L0 é a versão escrita à mão; L1 a L3 são as que o modelo editou; a de produção é a L1 depois de revisada.",
     "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "epoca", "termo": "Época", "grupo": "biblioteca", "padroes": [r"\bépocas?\b"],
     "curto": "Uma rodada em que o modelo lê os casos e propõe edições na biblioteca. Não é treino: o modelo não muda, só a documentação.",
     "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "nota-do-modelo", "termo": "Notas do modelo e verbetes aprendidos", "grupo": "biblioteca", "padroes": [r"notas? do modelo", r"verbetes? aprendidos?", r"retificaç(?:ão|ões)"],
     "curto": "O que o próprio modelo acrescentou à biblioteca: uma observação, uma correção de trecho ou um verbete novo.",
     "explicacao": "", "no_projeto": "Toda proposta passa por conferência em código antes de entrar. Na biblioteca de produção, passa também pela revisão de uma pessoa.", "fontes": []},
    {"id": "recuperacao", "termo": "Recuperação", "grupo": "biblioteca", "padroes": [r"recuperaç(?:ão|ões)", r"\brecuperador\b"],
     "curto": "A etapa que busca na biblioteca os verbetes mais parecidos com o caso, antes de o modelo responder.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "adesao-cega", "termo": "Adesão cega", "grupo": "biblioteca", "padroes": [r"adesão cega"],
     "curto": "Quando o modelo segue a documentação mesmo estando errada. É o risco que os filtros em código existem para conter.", "explicacao": "", "no_projeto": "", "fontes": []},

    {"id": "api", "termo": "API", "grupo": "agente", "padroes": [r"\bAPIs?\b"],
     "curto": "A parte do sistema que entrega os dados para a tela. A tela pede, a API responde.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "carimbo", "termo": "Carimbo de conflito", "grupo": "agente", "padroes": [r"carimbos? de conflito"],
     "curto": "Marca do relatório que acende quando uma conferência em código não confere ou quando uma intervenção muda a causa respondida.",
     "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "intervencao", "termo": "Intervenção e gatilho", "grupo": "agente", "padroes": [r"intervenç(?:ão|ões)", r"\bgatilhos?\b"],
     "curto": "Intervenção é uma pergunta extra ao modelo com uma mudança de propósito, como tirar um verbete, para ver se a resposta muda. Gatilho é o sinal que a dispara.",
     "explicacao": "Cada pergunta extra custa o tempo de um diagnóstico inteiro. Por isso as intervenções rodam só quando um sinal acende, como a probabilidade baixa da causa respondida ou a FONTE divergente.",
     "no_projeto": "", "fontes": []},
    {"id": "cot", "termo": "Raciocínio passo a passo (CoT)", "grupo": "modelo", "padroes": [r"\bCoT\b", r"chain of thought", r"cadeias? de pensamento"],
     "curto": "Pedir ao modelo que escreva o raciocínio antes da resposta. A sigla vem do inglês, chain of thought.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "cpu", "termo": "CPU e GPU", "grupo": "modelo", "padroes": [r"\bCPU\b", r"\bGPU\b", r"placa de vídeo"],
     "curto": "CPU é o processador comum do computador. GPU é a placa de vídeo, que roda modelos bem mais rápido. O projeto roda só em CPU.",
     "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "rag", "termo": "RAG", "grupo": "biblioteca", "padroes": [r"\bRAG\b"],
     "curto": "Técnica em que se busca, numa base de documentos, só o trecho que importa para a pergunta, e se entrega esse trecho ao modelo junto com ela.",
     "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "validacao-em-codigo", "termo": "Conferência em código", "grupo": "biblioteca", "padroes": [r"validaç(?:ão|ões) em código", r"conferências? em código", r"filtros em código", r"\bvalidador(?:es)?\b"],
     "curto": "Checagem feita por um programa, com regra fixa, e não por outro modelo de linguagem. Toda edição da biblioteca passa por ela antes de entrar.",
     "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "ciclo-de-correcao", "termo": "Ciclo de correção", "grupo": "biblioteca", "padroes": [r"ciclos? de correção"],
     "curto": "A marcação, em código, de um verbete como corrigido quando o caso ligado a ele volta a passar, com o registro do que mudou.",
     "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "recuperacao-por-id", "termo": "Recuperação por id", "grupo": "biblioteca", "padroes": [r"recuperaç(?:ão|ões) por id"],
     "curto": "A entrega ao modelo dos verbetes ligados a um caso pelas notas ou pelo caso de origem, sem depender da busca por palavras. Usada quando um caso é reapresentado.",
     "explicacao": "", "no_projeto": "", "fontes": []},

    {"id": "diagnostico", "termo": "Diagnóstico", "grupo": "agente", "padroes": [r"\bdiagnósticos?\b"],
     "curto": "A resposta do agente para uma falha: a causa, o campo afetado e de onde ele tirou a resposta.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "acerto", "termo": "Acerto", "grupo": "metodo", "padroes": [r"acerto simples", r"taxas? de acerto", r"\bacertos?\b"],
     "curto": "A parcela dos casos em que a causa respondida é a certa.",
     "explicacao": "É a conta mais direta: de todos os casos, em quantos a resposta bateu com o gabarito.",
     "no_projeto": "O acerto simples vem sempre com o intervalo de Wilson. Para comparar modelos, a medida principal é a acurácia balanceada, que não se deixa enganar por um modelo que responde sempre a mesma causa.",
     "fontes": []},
    {"id": "hipotese", "termo": "Hipótese", "grupo": "metodo", "padroes": [r"\bhipóteses?\b"],
     "curto": "Uma afirmação escrita antes da medição, que o resultado confirma ou não.",
     "explicacao": "Escrever a hipótese antes impede que ela seja ajustada depois para caber no resultado.",
     "no_projeto": "As seis hipóteses da Fase 3 foram escritas antes da bateria, e o texto delas não muda: cada veredito entra em uma linha à parte.",
     "fontes": []},
    {"id": "ablacao", "termo": "Ablação", "grupo": "metodo", "padroes": [r"ablaç(?:ão|ões)"],
     "curto": "Tirar uma parte do sistema para ver o que acontece sem ela.",
     "explicacao": "Se o resultado piora sem a parte, ela faz diferença. Se fica igual, ela não era o que explicava o resultado.",
     "no_projeto": "O projeto usou ablações para separar o efeito da documentação certa, da errada e do ajuste do modelo por instrução.",
     "fontes": []},
    {"id": "sonda", "termo": "Sonda", "grupo": "projeto", "padroes": [r"\bsondas?\b", r"\bsondagem\b"],
     "curto": "Um teste pequeno e rápido, para responder a uma pergunta antes de gastar uma corrida inteira.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "troca-cruzada", "termo": "Troca cruzada", "grupo": "biblioteca", "padroes": [r"trocas? cruzadas?"],
     "curto": "A biblioteca escrita por um modelo, lida por outro, para saber se o ganho é da biblioteca ou de quem a lê.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "curadoria", "termo": "Curadoria", "grupo": "biblioteca", "padroes": [r"\bcuradorias?\b", r"\bcurad[ao]s?\b"],
     "curto": "A revisão, por uma pessoa, do que entra ou fica na biblioteca.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "embedding", "termo": "Busca por significado (embedding)", "grupo": "biblioteca", "padroes": [r"busca por significado", r"\bembeddings?\b"],
     "curto": "Busca que compara o sentido do texto, e não as palavras: cada texto vira uma lista de números, e textos de sentido parecido ficam próximos.",
     "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "maquina-alvo", "termo": "Máquina-alvo", "grupo": "projeto", "padroes": [r"máquinas?-alvo"],
     "curto": "O computador de escritório, sem placa de vídeo, em que o agente precisa rodar. Os tempos do projeto só valem medidos nela.",
     "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "harness", "termo": "Harness", "grupo": "projeto", "padroes": [r"\bharness\b"],
     "curto": "O código que executa os experimentos e os cenários e grava os registros de cada corrida.", "explicacao": "", "no_projeto": "", "fontes": []},

    {"id": "corrida", "termo": "Corrida", "grupo": "projeto", "padroes": [r"\bcorridas?\b"],
     "curto": "Uma execução medida do agente, com número, comando, data e registro guardado.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "ficha", "termo": "Ficha", "grupo": "projeto", "padroes": [r"\bfichas?\b"],
     "curto": "Uma decisão pendente posta por escrito: o que é, por que importa, as opções e a recomendação.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "hub", "termo": "Hub", "grupo": "projeto", "padroes": [r"\bhub\b"],
     "curto": "A tela em que uma pessoa revisa os relatórios do agente, no estilo de uma revisão de código.", "explicacao": "", "no_projeto": "", "fontes": []},
    {"id": "limiar", "termo": "Limiar", "grupo": "projeto", "padroes": [r"\blimiar(?:es)?\b"],
     "curto": "O valor de corte de uma medida: acima dele vale uma coisa, abaixo vale outra.", "explicacao": "", "no_projeto": "", "fontes": []},
]

_POR_ID = {t["id"]: t for t in TERMOS}
# Onde a marcação não entra: código, comandos, títulos, rótulos de tabela e de botão, a navegação e os próprios cartões de número.
_SEM_MARCA = {"code", "pre", "a", "button", "h1", "h2", "h3", "h4", "summary", "script", "style", "canvas", "svg", "select", "option", "th", "label", "textarea", "title", "nav",
              "aside", "figcaption", "dt"}
_CLASSES_SEM_MARCA = {"kpi", "chip", "numero", "termo", "cmd", "termos-da-aba", "marca", "tag", "rotulo", "dica-termo", "legenda-cadeia", "filtros"}
_VAZIOS = {"br", "img", "input", "hr", "meta", "link", "col", "source", "wbr"}
_RE_PARTES = re.compile(r"(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<!--.*?-->|<[^>]+>)", re.DOTALL)
_RE_SECAO = re.compile(r'<section id="([^"]+)"[^>]*>')


def _padrao_geral() -> tuple[re.Pattern, list[str]]:
    """Uma expressão só com todos os padrões, os mais longos primeiro, e a lista que diz de qual termo é cada grupo."""
    pares = sorted(((p, t["id"]) for t in TERMOS for p in t["padroes"]), key=lambda x: -len(x[0]))
    return re.compile("|".join(f"({p})" for p, _ in pares), re.IGNORECASE), [i for _, i in pares]


_PADRAO, _DONO = _padrao_geral()


def fonte(chave: str, referencias_md: str) -> str | None:
    """O texto da fonte: a linha de `referencias.md` que começa pela chave (sem o negrito e sem a marca de conferência), ou a entrada clássica."""
    valor = chave.partition(":")[2]
    linhas = [l[2:] for l in referencias_md.splitlines() if l.startswith("- " + valor)]
    if len(linhas) != 1:
        return None
    return re.sub(r"\s*\*\(suporte parcial[^)]*\)\*", "", linhas[0]).replace("**", "").strip()


def fontes_que_faltam(referencias_md: str) -> list[str]:
    """As chaves de fonte que não resolvem (nenhuma linha, mais de uma, ou clássica sem entrada); o teste exige lista vazia."""
    return [f"{t['id']}: {c}" for t in TERMOS for c in t["fontes"] if not fonte(c, referencias_md)]


def _entrada(t: dict, referencias_md: str) -> str:
    partes = [f'<h3>{html.escape(t["termo"])}</h3>', f'<p class="lead-termo">{html.escape(t["curto"])}</p>']
    if t["explicacao"]:
        partes.append(f'<p>{html.escape(t["explicacao"])}</p>')
    if t["no_projeto"]:
        partes.append(f'<p><strong>Neste projeto.</strong> {html.escape(t["no_projeto"])}</p>')
    fontes = [f for f in (fonte(c, referencias_md) for c in t["fontes"]) if f]
    if fontes:
        partes.append('<p class="nota"><strong>Fonte.</strong> ' + "<br>".join(html.escape(f) for f in fontes) + "</p>")
    return f'<article class="entrada-termo" id="termo-{t["id"]}">' + "".join(partes) + "</article>"


def secao_glossario(referencias_md: str) -> str:
    blocos = []
    for chave, titulo in GRUPOS:
        itens = sorted((t for t in TERMOS if t["grupo"] == chave), key=lambda t: t["termo"].lower())
        blocos.append(f"<h2>{html.escape(titulo)}</h2>\n<div class=\"entradas-termo\">" + "".join(_entrada(t, referencias_md) for t in itens) + "</div>")
    n_metodos = sum(1 for t in TERMOS if t["grupo"] == "metodo")
    return (f'<section id="glossario" hidden>\n<h1>Glossário e métodos</h1>\n'
            f'<p class="lead">As palavras do projeto e os métodos de medida, em linguagem direta. São {len(TERMOS)} entradas, {n_metodos} delas de método, cada método com o que '
            'ele responde, o que o projeto faz com ele e a fonte. Nas outras abas, a primeira vez que um termo aparece ele vem sublinhado em pontilhado: passar o mouse, tocar '
            'ou focar mostra a explicação curta, e o fim de cada aba lista os termos que ela usou.</p>\n' + "\n".join(blocos) + "\n</section>")


def dados_js() -> dict:
    return {t["id"]: {"t": t["termo"], "c": t["curto"]} for t in TERMOS}


def _classes(tag: str) -> str:
    # as duas formas de aspas: os cartões de número do gerador saem com class='kpi'
    m = re.search(r"""\bclass=(?:"([^"]*)"|'([^']*)')""", tag)
    return (m.group(1) or m.group(2) or "") if m else ""


def _anotar_secao(corpo: str) -> tuple[str, list[str]]:
    """Marca, no corpo de uma aba, a primeira ocorrência de cada termo fora de código, título, botão e afins; devolve o corpo e os termos marcados, em ordem."""
    partes = _RE_PARTES.split(corpo)
    pilha: list[tuple[str, bool]] = []       # (nome da marcação, se ela ou alguma de cima impede a marca)
    usados: list[str] = []

    def troca(m: re.Match) -> str:
        termo = _DONO[m.lastindex - 1]
        if termo in usados:
            return m.group(0)
        usados.append(termo)
        return f'<span class="termo" tabindex="0" data-termo="{termo}">{m.group(0)}</span>'

    for i, parte in enumerate(partes):
        if i % 2 == 0:
            if parte.strip() and not (pilha and pilha[-1][1]):
                partes[i] = _PADRAO.sub(troca, parte)
            continue
        if parte.startswith(("<!--", "<script", "<style")):
            continue
        nome = re.match(r"</?\s*([a-zA-Z0-9]+)", parte)
        if not nome:
            continue
        nome = nome.group(1).lower()
        if parte.startswith("</"):
            for j in range(len(pilha) - 1, -1, -1):
                if pilha[j][0] == nome:
                    del pilha[j:]
                    break
        elif nome not in _VAZIOS and not parte.endswith("/>"):
            # a classe é comparada inteira: "numeros" não é "numero", e uma classe parecida não pode tirar a marca de um bloco inteiro
            impede = (pilha[-1][1] if pilha else False) or nome in _SEM_MARCA or not _CLASSES_SEM_MARCA.isdisjoint(_classes(parte).split())
            pilha.append((nome, impede))
    return "".join(partes), usados


def _lista_da_aba(ids: list[str], referencias_md: str) -> str:
    linhas = []
    for i in sorted(ids, key=lambda x: _POR_ID[x]["termo"].lower()):
        t = _POR_ID[i]
        extra = f' <span class="nota">Neste projeto: {html.escape(t["no_projeto"])}</span>' if t["grupo"] == "metodo" and t["no_projeto"] else ""
        fontes = [f for f in (fonte(c, referencias_md) for c in t["fontes"]) if f]
        cita = f' <span class="nota">Fonte: {"<br>".join(html.escape(f) for f in fontes)}</span>' if fontes else ""
        linhas.append(f'<dt><a href="#glossario" data-ir="glossario|termo-{i}">{html.escape(t["termo"])}</a></dt><dd>{html.escape(t["curto"])}{extra}{cita}</dd>')
    return (f'<details class="termos-da-aba"><summary>Termos e métodos desta aba ({len(ids)})</summary><dl>{"".join(linhas)}</dl>'
            '<p class="nota">A lista completa, com a explicação de cada um, está na aba <a href="#glossario" data-ir="glossario|">Glossário e métodos</a>.</p></details>')


def anotar(pagina: str, referencias_md: str = "") -> str:
    """A página com os termos marcados na primeira ocorrência de cada aba e a lista "Termos e métodos desta aba" no fim de cada uma. A aba do glossário não é
    marcada. Aplicar duas vezes dá o mesmo resultado, porque o que já está marcado não é marcado de novo."""
    saida, pos = [], 0
    for m in _RE_SECAO.finditer(pagina):
        fim = pagina.find("</section>", m.end())
        if fim < 0 or m.start() < pos:
            continue
        saida.append(pagina[pos:m.end()])
        corpo = pagina[m.end():fim]
        if m.group(1) != "glossario" and 'class="termos-da-aba"' not in corpo:
            corpo, usados = _anotar_secao(corpo)
            if usados:
                corpo += _lista_da_aba(usados, referencias_md) + "\n"
        saida.append(corpo)
        pos = fim
    saida.append(pagina[pos:])
    return "".join(saida)


CSS = r"""
/* glossário (11/11/2026): o termo marcado, a dica, a lista do fim de cada aba e as entradas da aba Glossário e métodos */
.termo{border-bottom:1px dotted var(--acento);cursor:help}.termo:focus-visible{outline:2px solid var(--acento);outline-offset:2px;border-radius:3px}
.dica-termo{position:absolute;z-index:20;background:var(--bg2);color:var(--ink);border:1px solid var(--acento);border-radius:10px;box-shadow:var(--sombra);padding:10px 12px;font:13px/1.45 var(--fb)}
.dica-termo b{display:block;font:600 14px var(--fd);margin-bottom:3px}.dica-termo span{display:block}.dica-termo a{display:inline-block;margin-top:6px;color:var(--acento);font-weight:600;text-decoration:none}
.termos-da-aba{margin-top:28px}.termos-da-aba dl{margin:8px 0 0;display:grid;grid-template-columns:minmax(140px,220px) 1fr;gap:6px 14px}
.termos-da-aba dt{font-weight:600}.termos-da-aba dt a{color:var(--acento);text-decoration:none}.termos-da-aba dd{margin:0}.termos-da-aba dd .nota{display:block}
@media (max-width:640px){.termos-da-aba dl{grid-template-columns:1fr}.termos-da-aba dd{margin-bottom:6px}}
.entradas-termo{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));gap:12px}
.entrada-termo{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:14px 16px}.entrada-termo h3{margin:0 0 4px}.entrada-termo.realce{outline:3px solid var(--acento);outline-offset:2px}
.lead-termo{font-size:15px;margin:0 0 6px}
"""


def script() -> str:
    """O script da dica: os dados do glossário e a abertura ao passar o mouse, tocar, focar e apertar Enter; Esc fecha."""
    dados = json.dumps(dados_js(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return ("<script>window.GLOSSARIO = " + dados + r""";
(function(){
  const G = window.GLOSSARIO || {}; let dica = null, dono = null;
  function fechar(){ if(dica){ dica.remove(); dica = null; dono = null; } }
  function abrir(el){ if(dono === el) return; fechar(); const g = G[el.dataset.termo]; if(!g) return;
    dica = document.createElement('div'); dica.className = 'dica-termo'; dica.setAttribute('role', 'tooltip'); dono = el;
    const b = document.createElement('b'); b.textContent = g.t; const s = document.createElement('span'); s.textContent = g.c;
    const a = document.createElement('a'); a.href = '#glossario'; a.textContent = 'ver no glossário';
    a.addEventListener('click', e => { e.preventDefault(); const id = 'termo-' + el.dataset.termo; fechar(); if(typeof irPara === 'function') irPara('glossario', id); });
    dica.append(b, s, a); document.body.appendChild(dica);
    const r = el.getBoundingClientRect(), larg = Math.min(340, window.innerWidth - 24); dica.style.width = larg + 'px';
    const x = Math.min(r.left, window.innerWidth - 12 - larg);
    dica.style.left = (Math.max(12, x) + window.scrollX) + 'px'; dica.style.top = (r.bottom + window.scrollY + 6) + 'px'; }
  document.addEventListener('click', e => { const t = e.target.closest ? e.target.closest('.termo') : null;
    if(t){ abrir(t); } else if(!(e.target.closest && e.target.closest('.dica-termo'))) fechar(); });
  document.addEventListener('keydown', e => { if(e.key === 'Escape') fechar();
    const f = document.activeElement; if((e.key === 'Enter' || e.key === ' ') && f && f.classList && f.classList.contains('termo')){ e.preventDefault(); abrir(f); } });
  document.addEventListener('mouseover', e => { const t = e.target.closest ? e.target.closest('.termo') : null; if(t) abrir(t); });
  document.addEventListener('mouseout', e => { const t = e.target.closest ? e.target.closest('.termo') : null;
    if(t) setTimeout(() => { if(dica && !dica.matches(':hover') && !t.matches(':hover')) fechar(); }, 300); });
})();
</script>""")
