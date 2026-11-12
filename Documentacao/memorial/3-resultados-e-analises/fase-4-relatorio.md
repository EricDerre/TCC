<!-- ! Alteração de IA - Revisar: relatório novo (05/11/2026, pacote P8) da Fase 4: o que cada corrida (16 a 22) mediu, as regras R1 a R8, o que fica como limitação e o que a próxima versão do documento do TCC precisa carregar. As tabelas são coladas por `avaliar_fase4.py --colar` (blocos `tb_f4_*`, conferidos por `--check`): os blocos das corridas 18 e 21 são os das repetições 18b e 21b, que são as leituras vigentes, e os da corrida 17 são os dos 72 casos. O texto foi montado por script a partir dos mesmos JSON.
     ! Motivo: o plano aprovado (seção 5, P8) pede o relatório da fase; sem ele, a leitura de cada corrida ficava espalhada no roadmap §2.8 a §2.15 e nas abas do painel, e as limitações das decisões 82 e 85 a 89 não tinham um lugar único para o documento do TCC citar. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026, depois do P8) o relatório passou a dizer as respostas do Eric às fichas 42 a 45 (decisões 90 a 93): título, estado, seção 5 (limite do prompt, com a medida de `resultados_alvo/fase4/prompt_tela_blocos.json`, lida por script), seções 8, 10, 11, 12, 13, 14 e 15.
     ! Motivo: as seções diziam "sem decisão" e "para o Eric decidir", e três respostas pedem corridas antes da Fase 5; sem a mudança, o relatório e a aba do painel que o lê mandariam a fase para a Fase 5 sem elas, e a seção 15 mandaria o documento do TCC declarar como não feito o que agora vai rodar. -->
# Fase 4: o agente na tela, relatório (05/11/2026)

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). O plano é [`claude-memoria/plano-aprovado-fase-4.md`](../../../claude-memoria/plano-aprovado-fase-4.md) (decisões 79 e 80), e os desvios dele estão no anexo daquele arquivo. A primeira leitura de cada corrida, com os detalhes de lançamento e os defeitos achados, está no [roadmap](../roadmap.md), §2.8 a §2.15; os gráficos estão no grupo Fase 4 do [painel](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN). As tabelas saem de `avaliar_fase4.py` (pasta `resultados_alvo/fase4/`), são coladas aqui por `--colar` e conferidas por `--check`. Os números do texto foram lidos dos mesmos JSON por script, nenhum digitado à mão, e as probabilidades e os MTTR da cura aparecem com três casas.

> **Estado em 06/11/2026:** os pacotes P0 a P8 estão feitos, e as corridas 16 a 24, com as repetições 18d, 21d e 18e, rodaram e foram lidas. O agente lê a tela, diagnostica, cura localizador em código, propõe acréscimos à biblioteca atrás de validação e grava uma trilha aberta de cada passo. A medida com revisor humano da especificação da trilha está em aberto: será feita depois de a Pós-Fase 4 normalizar as respostas (seção 9.5, decisão 95). A poda foi consertada depois das corridas, sem corrida nova (seção 9.6). Quatro pontos que o plano previa não saíram, e o Eric respondeu as fichas 42 a 45 no mesmo dia (decisões 90 a 93, seção 13). As corridas 18c, 21c e 23 rodaram em 05/11/2026 à noite, e as corridas 18d, 21d e 18e, com os sinais novos da busca, em 06/11/2026: a regra R2 fechou pela leitura fixada antes delas (decisões 97 e 98), e as leituras da 18d e da 21d são as que valem. A corrida 24 rodou no mesmo dia, com a conferência do Eric feita (ficha 46, decisão 100; seção 7.1), e a fase fica concluída. Antes da Fase 5 vem a Pós-Fase 4 (decisão 94). Nada foi commitado: quem commita é o Eric.

## 1. O que a fase perguntou e o que ela respondeu

| Pergunta | Resposta | Onde |
|---|---|---|
| A tela reproduz os casos de avaliação? | Em parte: 37 dos 72 casos (51,4%), todos os que têm tela e modo de injeção, pela regra R1 como rodou, mais larga que o texto do plano, e 25 dos 36 inéditos da ficha 27. O resto continua avaliado só em texto. | Seção 3, corrida 17 |
| Com quantos verbetes o agente lê e onde ficam os limiares do selo de confiança? | k = 3 pela regra R8 (81,5% contra 75,7% de acurácia balanceada). Selo baixo até p = 0,832 e alto a partir de p = 0,990. A probabilidade do rótulo separa acerto de erro (AUROC 0,799), mas 3 erros saem com selo alto: é triagem, não barreira. | Seção 4, corrida 16 |
| O agente dá o mesmo diagnóstico ao caso lido da tela e ao caso escrito? | Não em todos os casos, mas a tela não piora, pela regra fixada: mesmo rótulo em 28 de 37 casos, 32 acertos na tela contra 30 no fixture; a tela perde 3 casos e ganha 5, e o limite é de 3 perdidos (decisão 98; pela soma dos dois lados, 8; p = 0,727). Nos 25 inéditos, 22 contra 18, e a tela perde 0 e ganha 4. O que mudou foi a busca: o verbete certo chega em 36 de 37 na tela. O caso da tela leva uma medida que o caso escrito não tem, então isso não diz que o modelo lê melhor da tela. | Seção 5, corridas 18 a 18e |
| Um exemplar resolvido ou os rótulos em palavras mudam o acerto? | Não dá para dizer: 70 de 90 com o exemplar (b = 6, c = 4, p = 0,754) e 67 de 90 com os rótulos em palavras (b = 5, c = 6, p = 1,000), contra 68 de 90 na corrida 16. O prompt do agente continua congelado (decisão 91). | Seção 4.1, corrida 23 |
| A cura de seletor em código funciona? | Nas quebras armadas, sim: 160 de 160, sempre pelo mesmo elemento, MTTR mediano de 0,639 s, sem modelo. As duas formas de quebra deram a mesma árvore e o mesmo resultado em 16 das 16 células. Os 100% vêm do desenho da corrida. | Seção 6, corrida 19 |
| O que o agente propõe para a biblioteca passa pelos filtros e ajuda? | 19 de 92 propostas entraram no lote. A regra R5 aceitou o lote com b = 0 e c = 0: não piorou, e também não mudou acerto nenhum nos 36 inéditos. O ciclo de correção marcou certo (precisão e revocação de 100,0% em 9 casos), e o modelo não percebe a correção registrada (0 de 7 a mencionam). | Seção 7, corrida 20 |
| A biblioteca final acerta em casos que nunca viu? | Menos que nos casos de avaliação: 25 de 36 (69,4%; Wilson 95% de 53,1 a 82,0), contra 31 de 36 nos casos de avaliação, que não são os mesmos. Com o verbete certo, 18 de 20; sem ele, 7 de 16. A classe de tradução faz 1 de 6. Há uma condição só: a corrida não diz quanto a biblioteca ajuda nesses casos. | Seção 7.1, corrida 24 |
| Quanto tempo o agente inteiro leva e em quantos cenários acerta? | 10 de 10 com Task Success (a tarefa concluída, pelo critério da ficha 35) na repetição, com Wilson 95% de 72,2 a 100,0%, e MTTR (tempo da detecção ao reparo validado) médio de 74,0 s com o prompt dentro do limite e os sinais novos da busca (72,5 s na 21c; 105,2 s antes do corte), quase todo do modelo. Uma repetição por cenário, sem linha de base manual. | Seção 8, corridas 21, 21b, 21c e 21d |
| A divergência da trilha aponta os erros reais? | Com as intervenções em todos os casos, quase não: TPR x TNR (erros pegos vezes acertos deixados em paz) de 0,284 contra 0,250 do acaso. Contada por gatilho, 0,542, numa corrida que não rodou assim. São só 5 erros. Nas mutações, o nó previsto em 100%, o que é esperado por construção. | Seções 9.1 a 9.3, corrida 22 |
| O relatório por caso ajuda um revisor humano a decidir? | Feita em parte em 09 e 10/11/2026, no pacote Q5 da Pós-Fase 4, sobre os 36 relatórios v3 da corrida 24: 35 lidos por um analista, a quem o Eric passou os relatórios, e 1 pelo Eric (ficha 40, decisões 113 e 114; leitura em `resultados_alvo/fase4/leitura_revisao_v3.md`). Ficaram medidas a adesão, a localização do erro e a utilidade; o tempo até a decisão não. A sessão de 05/11 (1 resposta do Eric e 10 pareceres do Claude aprovados, decisões 85 e 86) fica como registro. | Seção 9.5 |

## 2. Como a fase rodou

Máquina: i5-1235U, 16 GB, só CPU, a mesma das fases anteriores; `qwen2.5:7b`, `num_ctx` 8192, temperatura 0,1, um modelo residente por vez; Python 3.14.7, Playwright 1.64.1 e Chromium 156.0.8078.4 em modo headless (`resultados_alvo/fase4/ambiente.json`). As cobaias nunca tinham subido nesta máquina corporativa: o P0 instalou PHP e MariaDB portátil sem administrador, e o `install.py` passou a cobrir esse caminho (roadmap §1).

| Corrida | Pasta em `resultados_alvo/` | Quando | Executor (s) | Inferências | Ollama | Biblioteca |
|---|---|---|---|---|---|---|
| 17, reprodução (72 casos) | `fase4_reproducao` | 26/10, 22:39 | 111 | 0 | sem modelo | |
| 17, reprodução (36 inéditos) | `fase4_reproducao_ineditos` | 27/10, 17:52 | 64 | 0 | sem modelo | |
| 16, calibração | `fase4_calibracao` | 27/10, 20:46 | 11219 | 183 | 0.40.2 | L1 curada, `1fca10f1a6f6` |
| 18, tela e fixture | `fase4_tela` | 01/11, 11:09 | 5077 | 74 | 0.40.2 | `1fca10f1a6f6` |
| 18b, repetição | `fase4_tela_v2` | 01/11, 14:06 | 5316 | 74 | 0.40.2 | `1fca10f1a6f6` |
| 19, cura de seletor | `fase4_cura` | 01/11, 19:58 | 1006 | 0 | sem modelo | |
| 20, biblioteca | `fase4_biblioteca` | 03/11, 21:01, e 04/11, 16:24 | 1749 no relançamento; a primeira parte levou 4h45 (roadmap §2.12) | 158 | 0.40.14 | `1fca10f1a6f6` |
| 21, ensaio dos cenários | `fase4_ensaio` | 04/11, 20:19 | 1037 | 10 | 0.40.14 | `95af35290860` |
| 21b, repetição | `fase4_ensaio_v2` | 04/11, 21:31 | 1121 | 10 | 0.40.14 | `95af35290860` |
| 22, avaliação da trilha | `fase4_trilha` | 04/11, 23:00 | 13202 | 277 | 0.40.14 | `95af35290860` |
| 18c, repetição com o prompt no limite | `fase4_tela_v3` | 05/11, 18:39 | 4596 | 74 | 0.40.14 | `95af35290860` |
| 21c, repetição com o prompt no limite | `fase4_ensaio_v3` | 05/11, 19:56 | 794 | 10 | 0.40.14 | `95af35290860` |
| 23, experimento em texto | `fase4_experimento` | 05/11, 20:09 | 10581 | 180 | 0.40.14 | `1fca10f1a6f6`, a da corrida 16 |
| 18d, com os sinais da busca (a que vale) | `fase4_tela_v4` | 06/11, 09:53 | 4770 | 74 | 0.40.14 | `95af35290860` |
| 21d, com os sinais da busca (a vigente) | `fase4_ensaio_v4` | 06/11, 11:13 | 808 | 10 | 0.40.14 | `95af35290860` |
| 18e, os inéditos na tela | `fase4_tela_ineditos` | 06/11, 11:26 | 3739 | 50 | 0.40.14 | `95af35290860` |
| 24, os 36 inéditos em texto | `fase4_ineditos` | 06/11, 13:52 | 2610 | 36 | 0.40.14 | `95af35290860` |

Somando o executor de cada corrida e a primeira parte da corrida 20, foram 15h50 de máquina, sem contar a ponte do Ollama 0.40.14 nem as partidas que caíram antes de começar. O plano estimava de 11h06 a 15h55 sem as repetições 18b e 21b. As corridas 18c, 21c e 23, pedidas depois do fechamento (decisões 90 e 91), somam mais 4h26 de executor, em fila, por `rodar_pendencias_fase4.ps1`, e as corridas 18d, 21d e 18e (decisão 97), mais 2h35, na mesma fila, e a corrida 24, mais 0h43.

**Regra R6 (ponte de versão).** A versão 0.40.2 já tinha ponte (`fase3b_ponte_0402`: b = 1, c = 0 em 35 casos). Em 03/11 o Ollama se atualizou sozinho para 0.40.14, o executor recusou a corrida até haver ponte, e a ponte `fase3b_ponte_04014` deu b = 1, c = 0 em 35 casos, dentro do limite de 2 (decisão 47). Os limiares do selo vêm da 0.40.2 e não foram recalibrados: a ponte iguala os rótulos, e a sondagem iguala a probabilidade num caso, não a curva inteira.

## 3. Reprodução na tela (corrida 17, regra R1)

Um caso reproduz quando, com o modo e o campo do caso ligados na CobaiaAPI, a chamada sai do normal (status, contrato, tempo, corpo ou árvore diferentes da referência em modo normal) ou uma conferência do roteiro falha. A contagem é em código, sem modelo. Dos 72 casos de avaliação, 37 têm tela e modo e os 37 reproduzem (51,4% dos 72). Ficam de fora 35: 11 armados pelo harness (ficha 29), 2 sem modo para a causa `dado_desatualizado` e 22 sem tela: 20 de rotas de pedidos, que nenhuma página consome, e 2 de catálogo (`run-10`, `semt-18`). Esses 2 de catálogo ficaram de fora por um defeito achado no fechamento: a requisição deles traz uma anotação entre parênteses, e a expressão de `selecionar_casos` não a aceita, embora `produtos_api.php` consuma a rota. A corrida não foi repetida, e o código não mudou. A ficha 28 acrescentou 14 modos de injeção, porque os sete de antes só alcançavam 20 dos 72 casos (plano, seção 1.3).

**A regra R1, como rodou, é mais larga que o texto do plano.** O plano (seção 5) pedia o roteiro falhando no passo esperado e o campo do gabarito no caso ao vivo. A corrida rodou três vezes em 26/10, as duas primeiras calibraram a regra, e a terceira é a que vale (roadmap §2.8); o código final (`executar_fase4.reproduz`) não confere o campo do gabarito, e só 12 dos 37 casos derrubam uma conferência do roteiro. Então os 37 de 37 dizem que a falha injetada muda o fio ou a tela, não que o campo certo aparece no caso ao vivo. Essa pergunta é a das seções 5 e 8.

Nos inéditos da ficha 27, a mesma corrida (`reproducibilidade_ineditos.json`) deu 25 de 36 (69,4%), com 11 de fora: 6 armados pelo harness (ficha 29), 1 sem modo para a causa `dado_desatualizado` e 4 sem tela, de rotas de pedidos. Essa é a única medida desses 36 casos: nenhuma corrida com modelo os leu (ficha 44).

O custo é baixo: mediana de 0,275 s por cenário e máximo de 31,027 s, no `latency`, que dorme por item. A árvore cai de 193 nós para 39 linhas na mediana. Os blocos abaixo são os da leitura dos 72 casos; os dos inéditos têm os mesmos nomes e ficam em `reproducibilidade_ineditos.md`.

<!-- tabela:tb_f4_reproducao_resumo -->
| Casos de avaliação | Com tela e modo | Reproduzem na tela | Fora (sem tela, sem modo ou pelo harness) | Reproduzem (% dos casos) | Reproduzem (% dos com tela) | Roteiro falhou | Com erro do harness |
|---|---|---|---|---|---|---|---|
| 72 | 37 | 37 | 35 | 51,4 | 100,0 | 12 | 0 |
<!-- /tabela:tb_f4_reproducao_resumo -->

<!-- tabela:tb_f4_reproducao_por_classe -->
| Classe | Casos | Com tela e modo | Reproduzem | Fora | Reproduzem (%) |
|---|---|---|---|---|---|
| 1 | 12 | 8 | 8 | 4 | 66,7 |
| 2 | 12 | 7 | 7 | 5 | 58,3 |
| 3 | 12 | 8 | 8 | 4 | 66,7 |
| 4 | 12 | 8 | 8 | 4 | 66,7 |
| 5 | 12 | 5 | 5 | 7 | 41,7 |
| 6 | 12 | 1 | 1 | 11 | 8,3 |
<!-- /tabela:tb_f4_reproducao_por_classe -->

<!-- tabela:tb_f4_reproducao_por_nivel -->
| Nível | Casos | Com tela e modo | Reproduzem | Fora | Reproduzem (%) |
|---|---|---|---|---|---|
| 1 | 24 | 13 | 13 | 11 | 54,2 |
| 2 | 24 | 11 | 11 | 13 | 45,8 |
| 3 | 24 | 13 | 13 | 11 | 54,2 |
<!-- /tabela:tb_f4_reproducao_por_nivel -->

<!-- tabela:tb_f4_reproducao_custo -->
| Tempo por cenário (mediana, s) | Tempo por cenário (máximo, s) | Tempo total dos cenários (s) | Tempo da chamada à API (mediana, ms) | Árvore antes da poda (mediana, nós) | Árvore depois (mediana, linhas) | Corpo HTTP (mediana, caracteres) | Caso ao vivo (mediana, caracteres) |
|---|---|---|---|---|---|---|---|
| 0,275 | 31,027 | 97,6 | 19,3 | 193 | 39 | 2068 | 2603 |
<!-- /tabela:tb_f4_reproducao_custo -->

<details><summary>Por modo de injeção (tb_f4_reproducao_por_modo)</summary>

<!-- tabela:tb_f4_reproducao_por_modo -->
| Modo de injeção | Casos | Reproduzem | Motivos registrados |
|---|---|---|---|
| `chave_de_juncao_errada` | 2 | 2 | corpo diferente da referência em modo normal |
| `codificacao_incorreta` | 4 | 4 | corpo diferente da referência em modo normal; árvore diferente da referência: 4 linha(s) a menos e 4 a mais; corpo diferente da referência em modo normal; árvore diferente da referência: 6 linha(s) a menos e 6 a mais |
| `colecao_no_lugar_de_objeto` | 1 | 1 | diff do contrato: forma_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 2 linha(s) a menos e 2 a mais |
| `contagem_inconsistente` | 4 | 4 | corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou |
| `corpo_vazio` | 1 | 1 | corpo vazio; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou |
| `error_500` | 1 | 1 | status 500; diff do contrato: ausente, forma_diferente, inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou |
| `escala_ou_unidade_errada` | 2 | 2 | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `estrutura_aninhada_divergente` | 2 | 2 | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou |
| `field_missing` | 4 | 4 | diff do contrato: ausente; corpo diferente da referência em modo normal; diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 0 a mais; diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `field_renamed` | 1 | 1 | diff do contrato: renomeado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 0 a mais |
| `latency` | 3 | 3 | tempo de resposta 2013 ms acima do orçamento de 1000 ms; tempo de resposta 28024 ms acima do orçamento de 1000 ms; tempo de resposta 28028 ms acima do orçamento de 1000 ms |
| `malformed_json` | 3 | 3 | corpo truncado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou; corpo truncado; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou |
| `nulo_inesperado` | 3 | 3 | diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal; diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `registro_duplicado` | 1 | 1 | corpo diferente da referência em modo normal; árvore diferente da referência: 0 linha(s) a menos e 10 a mais; conferência 'grid com 14 cartões' falhou |
| `type_drift` | 2 | 2 | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `valor_fora_do_dominio` | 3 | 3 | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou; corpo diferente da referência em modo normal; árvore diferente da referência: 28 linha(s) a menos e 28 a mais; diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
<!-- /tabela:tb_f4_reproducao_por_modo -->

</details>

<details><summary>Caso a caso (tb_f4_reproducao_casos)</summary>

<!-- tabela:tb_f4_reproducao_casos -->
| Caso | Classe | Nível | Causa | Modo | Campo | Cenário | Reproduz | Motivo | Status | Segundos |
|---|---|---|---|---|---|---|---|---|---|---|
| `lex-1` | 1 | 1 | `resposta_truncada` | `malformed_json` |  | api-catalogo | sim | corpo truncado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,2 |
| `lex-4` | 1 | 2 | `codificacao_incorreta` | `codificacao_incorreta` | `nome` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 6 linha(s) a menos e 6 a mais | 200 | 0,3 |
| `sin-4` | 2 | 1 | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` |  | api-detalhe | sim | diff do contrato: forma_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 2 linha(s) a menos e 2 a mais | 200 | 0,5 |
| `sin-5` | 2 | 3 | `campo_ausente` | `field_missing` | `resumo` | api-catalogo | sim | diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,4 |
| `semt-1` | 3 | 2 | `tipo_divergente` | `type_drift` | `preco` | api-catalogo | sim | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal | 200 | 0,5 |
| `tra-1` | 4 | 2 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `preco` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `tra-4` | 4 | 3 | `contagem_inconsistente` | `contagem_inconsistente` |  | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,3 |
| `run-1` | 5 | 1 | `erro_interno_do_servidor` | `error_500` |  | api-catalogo | sim | status 500; diff do contrato: ausente, forma_diferente, inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou | 500 | 0,2 |
| `run-2` | 5 | 1 | `tempo_de_resposta_excedido` | `latency` |  | api-catalogo | sim | tempo de resposta 28024 ms acima do orçamento de 1000 ms | 200 | 28,3 |
| `efe-3` | 6 | 2 | `campo_ausente` | `field_missing` | `imagem` | api-catalogo | sim | diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 0 a mais | 200 | 0,2 |
| `lex-7` | 1 | 1 | `corpo_vazio` | `corpo_vazio` |  | api-detalhe | sim | corpo vazio; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou | 200 | 0,2 |
| `lex-8` | 1 | 2 | `codificacao_incorreta` | `codificacao_incorreta` | `resumo` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 4 linha(s) a menos e 4 a mais | 200 | 0,3 |
| `lex-10` | 1 | 3 | `resposta_truncada` | `malformed_json` |  | api-catalogo | sim | corpo truncado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,2 |
| `lex-11` | 1 | 3 | `codificacao_incorreta` | `codificacao_incorreta` | `nome` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 6 linha(s) a menos e 6 a mais | 200 | 0,3 |
| `sin-11` | 2 | 2 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` |  | api-catalogo | sim | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou | 200 | 0,2 |
| `sin-14` | 2 | 3 | `campo_renomeado` | `field_renamed` | `imagem` | api-catalogo | sim | diff do contrato: renomeado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 0 a mais | 200 | 0,2 |
| `semt-8` | 3 | 1 | `nulo_inesperado` | `nulo_inesperado` | `preco` | api-catalogo | sim | diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,2 |
| `semt-9` | 3 | 1 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | `destaque` | api-catalogo | sim | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `semt-14` | 3 | 3 | `nulo_inesperado` | `nulo_inesperado` | `tipo` | api-catalogo | sim | diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `tra-8` | 4 | 1 | `contagem_inconsistente` | `contagem_inconsistente` |  | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,3 |
| `tra-11` | 4 | 2 | `contagem_inconsistente` | `contagem_inconsistente` |  | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,2 |
| `run-9` | 5 | 2 | `tempo_de_resposta_excedido` | `latency` |  | api-catalogo | sim | tempo de resposta 28028 ms acima do orçamento de 1000 ms | 200 | 28,7 |
| `lex-16` | 1 | 1 | `resposta_truncada` | `malformed_json` |  | api-detalhe | sim | corpo truncado; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou | 200 | 0,2 |
| `lex-18` | 1 | 2 | `codificacao_incorreta` | `codificacao_incorreta` | `resumo` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 4 linha(s) a menos e 4 a mais | 200 | 0,3 |
| `sin-16` | 2 | 1 | `campo_ausente` | `field_missing` | `destaque` | api-detalhe | sim | diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,6 |
| `sin-20` | 2 | 3 | `campo_ausente` | `field_missing` | `id` | api-catalogo | sim | diff do contrato: ausente; corpo diferente da referência em modo normal | 200 | 0,3 |
| `sin-21` | 2 | 3 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `tipo` | api-catalogo | sim | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `semt-16` | 3 | 1 | `tipo_divergente` | `type_drift` | `tipo` | api-catalogo | sim | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `semt-17` | 3 | 1 | `nulo_inesperado` | `nulo_inesperado` | `id` | api-catalogo | sim | diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal | 200 | 0,3 |
| `semt-20` | 3 | 3 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | `preco` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou | 200 | 0,3 |
| `semt-21` | 3 | 3 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | `nome` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 28 linha(s) a menos e 28 a mais | 200 | 0,3 |
| `tra-17` | 4 | 1 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | `tipo` | api-catalogo | sim | corpo diferente da referência em modo normal | 200 | 0,3 |
| `tra-19` | 4 | 2 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `preco` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `tra-20` | 4 | 3 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | `tipo` | api-catalogo | sim | corpo diferente da referência em modo normal | 200 | 0,3 |
| `tra-21` | 4 | 3 | `contagem_inconsistente` | `contagem_inconsistente` |  | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,3 |
| `run-19` | 5 | 2 | `tempo_de_resposta_excedido` | `latency` |  | api-detalhe | sim | tempo de resposta 2013 ms acima do orçamento de 1000 ms | 200 | 31,0 |
| `run-21` | 5 | 3 | `registro_duplicado` | `registro_duplicado` |  | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 0 linha(s) a menos e 10 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,2 |
<!-- /tabela:tb_f4_reproducao_casos -->

</details>

<details><summary>Os casos de fora, com o motivo (tb_f4_reproducao_fora)</summary>

<!-- tabela:tb_f4_reproducao_fora -->
| Caso | Classe | Nível | Causa | Por que ficou fora |
|---|---|---|---|---|
| `semt-3` | 3 | 2 | `valor_fora_do_dominio` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `semt-5` | 3 | 3 | `nulo_inesperado` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `run-4` | 5 | 3 | `dado_desatualizado` | sem modo para a causa dado_desatualizado |
| `efe-1` | 6 | 1 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-2` | 6 | 2 | `estado_da_tela_divergente` | armada pelo harness (ficha 29): estado_da_tela_divergente |
| `efe-5` | 6 | 3 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `sin-7` | 2 | 1 | `campo_ausente` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `sin-10` | 2 | 2 | `campo_renomeado` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `tra-10` | 4 | 1 | `chave_de_juncao_errada` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `tra-15` | 4 | 3 | `escala_ou_unidade_errada` | sem tela: a rota 'POST /api/pedidos (pessoas=4) -> GET /api/pedidos' não é consumida por página nenhuma |
| `run-10` | 5 | 2 | `limite_de_requisicoes` | sem tela: a rota 'GET /api/produtos (12a requisicao em 1 min)' não é consumida por página nenhuma |
| `run-13` | 5 | 3 | `registro_duplicado` | sem tela: a rota 'POST /api/pedidos (clique duplo no botao)' não é consumida por página nenhuma |
| `efe-7` | 6 | 1 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-14` | 6 | 3 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `lex-17` | 1 | 1 | `corpo_vazio` | sem tela: a rota 'POST /api/pedidos' não é consumida por página nenhuma |
| `lex-19` | 1 | 2 | `corpo_nao_e_json` | sem tela: a rota 'POST /api/pedidos/7/cancelar' não é consumida por página nenhuma |
| `lex-20` | 1 | 3 | `resposta_truncada` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `lex-21` | 1 | 3 | `codificacao_incorreta` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `sin-17` | 2 | 1 | `campo_renomeado` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `sin-18` | 2 | 2 | `estrutura_aninhada_divergente` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `sin-19` | 2 | 2 | `colecao_no_lugar_de_objeto` | sem tela: a rota 'POST /api/pedidos/7/cancelar' não é consumida por página nenhuma |
| `semt-18` | 3 | 2 | `tipo_divergente` | sem tela: a rota 'GET /api/produtos (modo type_drift, campo destaque)' não é consumida por página nenhuma |
| `semt-19` | 3 | 2 | `formato_de_data_divergente` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `tra-16` | 4 | 1 | `escala_ou_unidade_errada` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `tra-18` | 4 | 2 | `contagem_inconsistente` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `run-16` | 5 | 1 | `recurso_inexistente` | sem tela: a rota 'GET /api/pedidos?login=55566677788' não é consumida por página nenhuma |
| `run-17` | 5 | 1 | `erro_interno_do_servidor` | sem tela: a rota 'POST /api/pedidos/7/cancelar' não é consumida por página nenhuma |
| `run-18` | 5 | 2 | `limite_de_requisicoes` | sem tela: a rota 'POST /api/pedidos (6a tentativa de reserva no mesmo minuto)' não é consumida por página nenhuma |
| `run-20` | 5 | 3 | `dado_desatualizado` | sem modo para a causa dado_desatualizado |
| `efe-16` | 6 | 1 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-17` | 6 | 1 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-18` | 6 | 2 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-19` | 6 | 2 | `estado_da_tela_divergente` | armada pelo harness (ficha 29): estado_da_tela_divergente |
| `efe-20` | 6 | 3 | `estado_da_tela_divergente` | armada pelo harness (ficha 29): estado_da_tela_divergente |
| `efe-21` | 6 | 3 | `estado_da_tela_divergente` | armada pelo harness (ficha 29): estado_da_tela_divergente |
<!-- /tabela:tb_f4_reproducao_fora -->

</details>

## 4. Calibração (corrida 16, regras R6, R7 e R8)

A L1 curada leu os 90 casos oficiais com k = 3 e com k = 5, gravando a probabilidade de cada token (`logprobs`). A regra R8 só deixaria o k = 5 entrar se ele acertasse mais. Não acertou: 68 de 90 com k = 3 (81,5% de acurácia balanceada) contra 65 com k = 5 (75,7%), b/c 5/8, p = 0,581. E o k = 5 custa mais: 60,5 s e 1.469,0 tokens de entrada na mediana, contra 55,4 s e 1.106,5.

Os limiares (regra R7, ficha 31 a) foram gravados em `limiares.json` antes da primeira corrida na tela: baixo até p = 0,832, os 30% de menor probabilidade, que pegam 15 dos 22 erros e revisam 12 acertos à toa; alto a partir de p = 0,990, a mediana dos acertos. Por selo: baixo erra 15 de 27 (55,6%), médio 4 de 26 (15,4%) e alto 3 de 37 (8,1%: `efe-13`, `lex-3`, `semt-9`).

A probabilidade do rótulo continua sendo triagem, não barreira: AUROC 0,799 [0,670; 0,902] com k = 3, e o selo alto avisa sem dispensar a conferência. A sondagem repetida no Ollama novo deu a mesma probabilidade num caso (roadmap §2.12).

<!-- tabela:tb_f4_calibracao_resumo -->
| Ollama | Modelo | Casos | k medidos | k escolhido (R8) | Selo baixo até (p) | Selo alto a partir de (p) | Ponte pareável (R6) | Sondagem dos logprobs |
|---|---|---|---|---|---|---|---|---|
| 0.40.2 | `qwen2.5:7b` | 90 | 3, 5 | 3 | 0,832 | 0,990 | sim | ok |
<!-- /tabela:tb_f4_calibracao_resumo -->

<!-- tabela:tb_f4_calibracao_por_k -->
| k | Casos | Completo | Acertos | Acerto (%) | Acurácia balanceada (%) | Nos 36 de avaliação (%) | Nos 54 de aprendizado (%) | s por diagnóstico (mediana) | Tokens de entrada (mediana) | Tokens de entrada (máximo) | AUROC p do rótulo [IC 95%] | AUROC p conjunta [IC 95%] | Sem rótulo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 90 | sim | 68 | 75,6 | 81,5 | 86,1 | 68,5 | 55,4 | 1106,5 | 1281 | 0,799 [0,670; 0,902] | 0,791 [0,661; 0,897] | 0 |
| 5 | 90 | sim | 65 | 72,2 | 75,7 | 77,8 | 68,5 | 60,5 | 1469,0 | 1668 | 0,793 [0,677; 0,893] | 0,816 [0,701; 0,910] | 0 |
<!-- /tabela:tb_f4_calibracao_por_k -->

<!-- tabela:tb_f4_calibracao_r8 -->
| Acurácia balanceada k = 3 (%) | Acurácia balanceada k = 5 (%) | b (só k = 5 acerta) | c (só k = 3 acerta) | p (McNemar exato) | k escolhido | Motivo |
|---|---|---|---|---|---|---|
| 81,5 | 75,7 | 5 | 8 | 0,581 | 3 | k = 3 acerta mais por acurácia balanceada (81,5% contra 75,7%) |
<!-- /tabela:tb_f4_calibracao_r8 -->

<!-- tabela:tb_f4_calibracao_revisao -->
| k | Parcela revisada | Casos revisados | Erros pegos | Acertos revisados à toa | Risco no que sobra |
|---|---|---|---|---|---|
| 3 | 10% | 9 | 7 de 22 | 2 | 18,5% |
| 3 | 20% | 18 | 10 de 22 | 8 | 16,7% |
| 3 | 30% | 27 | 15 de 22 | 12 | 11,1% |
| 5 | 10% | 9 | 7 de 25 | 2 | 22,2% |
| 5 | 20% | 18 | 12 de 25 | 6 | 18,1% |
| 5 | 30% | 27 | 16 de 25 | 11 | 14,3% |
<!-- /tabela:tb_f4_calibracao_revisao -->

<!-- tabela:tb_f4_calibracao_selos -->
| Selo | Casos | Certos | Errados | Erro (%) | Casos errados |
|---|---|---|---|---|---|
| baixo | 27 | 12 | 15 | 55,6 | `efe-10`, `efe-11`, `efe-4`, `lex-6`, `semt-6`, `semt-7`, `sin-12`, `sin-14`, `sin-2`, `sin-5`, `tra-12`, `tra-15`, `tra-3`, `tra-5`, `tra-7` |
| medio | 26 | 22 | 4 | 15,4 | `efe-1`, `run-11`, `tra-2`, `tra-9` |
| alto | 37 | 34 | 3 | 8,1 | `efe-13`, `lex-3`, `semt-9` |
<!-- /tabela:tb_f4_calibracao_selos -->

<!-- tabela:tb_f4_calibracao_ponte -->
| Ollama | Corrida da ponte | Feita nesta corrida | Casos pareados | b (só a ponte acerta) | c (só a Fase 3 acerta) | Pareável (b + c até o limite) | Casos de texto corrigido fora da conta |
|---|---|---|---|---|---|---|---|
| 0.40.2 | fase3b_ponte_0402 | não | 35 | 1 | 0 | sim (limite 2) | efe-3 |
<!-- /tabela:tb_f4_calibracao_ponte -->

<!-- tabela:tb_f4_calibracao_sondagem -->
| Ollama | Tokens com probabilidade | Alternativas por posição (máx.) | Bytes por token | Texto remontado bate | Probabilidade antes ou depois da temperatura | Resposta igual sem logprobs | Rótulo lido | p do rótulo | Avisos |
|---|---|---|---|---|---|---|---|---|---|
| 0.40.2 | 63 | 20 | sim | sim | antes | não | resposta_truncada | 1,000 | a resposta com logprobs difere da resposta sem logprobs no mesmo prompt |
<!-- /tabela:tb_f4_calibracao_sondagem -->

<details><summary>Caso a caso, do k escolhido (tb_f4_calibracao_casos)</summary>

<!-- tabela:tb_f4_calibracao_casos -->
| Caso | Partição | Gabarito | Rótulo | Resultado | p do rótulo | p conjunta | Segunda causa | Selo |
|---|---|---|---|---|---|---|---|---|
| `sin-14` | avaliacao | `campo_renomeado` | `colecao_no_lugar_de_objeto` | errado | 0,301 | 0,300 | tipo_divergente | baixo |
| `tra-15` | avaliacao | `escala_ou_unidade_errada` | `tipo_divergente` | errado | 0,421 | 0,421 | valor_fora_do_dominio | baixo |
| `semt-6` | aprendizado | `tipo_divergente` | `colecao_no_lugar_de_objeto` | errado | 0,443 | 0,442 | tipo_divergente | baixo |
| `sin-1` | aprendizado | `campo_ausente` | `campo_ausente` | certo | 0,484 | 0,481 | tipo_divergente | baixo |
| `run-3` | aprendizado | `limite_de_requisicoes` | `limite_de_requisicoes` | certo | 0,524 | 0,524 | não medido | baixo |
| `efe-11` | aprendizado | `estado_da_tela_divergente` | `localizador_quebrado` | errado | 0,533 | 0,533 | contagem_inconsistente | baixo |
| `efe-4` | aprendizado | `estado_da_tela_divergente` | `colecao_no_lugar_de_objeto` | errado | 0,568 | 0,567 | tipo_divergente | baixo |
| `tra-12` | aprendizado | `escala_ou_unidade_errada` | `tipo_divergente` | errado | 0,569 | 0,569 | valor_fora_do_dominio | baixo |
| `lex-6` | aprendizado | `corpo_nao_e_json` | `recurso_inexistente` | errado | 0,577 | 0,577 | corpo_nao_e_json | baixo |
| `efe-3` | avaliacao | `campo_ausente` | `campo_ausente` | certo | 0,585 | 0,584 | colecao_no_lugar_de_objeto | baixo |
| `semt-13` | aprendizado | `tipo_divergente` | `tipo_divergente` | certo | 0,598 | 0,598 | formato_de_data_divergente | baixo |
| `tra-7` | aprendizado | `chave_de_juncao_errada` | `campo_renomeado` | errado | 0,600 | 0,549 | estrutura_aninhada_divergente | baixo |
| `semt-7` | aprendizado | `tipo_divergente` | `formato_de_data_divergente` | errado | 0,605 | 0,605 | tipo_divergente | baixo |
| `efe-2` | avaliacao | `estado_da_tela_divergente` | `estado_da_tela_divergente` | certo | 0,643 | 0,642 | valor_fora_do_dominio | baixo |
| `run-10` | avaliacao | `limite_de_requisicoes` | `limite_de_requisicoes` | certo | 0,660 | 0,660 | tempo_de_resposta_excedido | baixo |
| `semt-15` | aprendizado | `valor_fora_do_dominio` | `valor_fora_do_dominio` | certo | 0,665 | 0,665 | formato_de_data_divergente | baixo |
| `sin-12` | aprendizado | `campo_ausente` | `colecao_no_lugar_de_objeto` | errado | 0,679 | 0,677 | resposta_truncada | baixo |
| `semt-14` | avaliacao | `nulo_inesperado` | `nulo_inesperado` | certo | 0,740 | 0,740 | tipo_divergente | baixo |
| `lex-8` | avaliacao | `codificacao_incorreta` | `codificacao_incorreta` | certo | 0,749 | 0,749 | corpo_nao_e_json | baixo |
| `sin-2` | aprendizado | `campo_renomeado` | `tipo_divergente` | errado | 0,751 | 0,751 | campo_ausente | baixo |
| `efe-10` | aprendizado | `estado_da_tela_divergente` | `valor_fora_do_dominio` | errado | 0,751 | 0,749 | tipo_divergente | baixo |
| `sin-5` | avaliacao | `campo_ausente` | `colecao_no_lugar_de_objeto` | errado | 0,758 | 0,753 | campo_ausente | baixo |
| `tra-5` | aprendizado | `escala_ou_unidade_errada` | `contagem_inconsistente` | errado | 0,760 | 0,760 | valor_fora_do_dominio | baixo |
| `lex-2` | aprendizado | `corpo_nao_e_json` | `corpo_nao_e_json` | certo | 0,774 | 0,724 | erro_interno_do_servidor | baixo |
| `semt-1` | avaliacao | `tipo_divergente` | `tipo_divergente` | certo | 0,777 | 0,777 | formato_de_data_divergente | baixo |
| `tra-3` | aprendizado | `chave_de_juncao_errada` | `tipo_divergente` | errado | 0,792 | 0,792 | chave_de_juncao_errada | baixo |
| `semt-8` | avaliacao | `nulo_inesperado` | `nulo_inesperado` | certo | 0,832 | 0,832 | tipo_divergente | baixo |
| `semt-12` | aprendizado | `formato_de_data_divergente` | `formato_de_data_divergente` | certo | 0,841 | 0,841 | tipo_divergente | medio |
| `tra-2` | aprendizado | `chave_de_juncao_errada` | `nome_nulo_vindo_da_view` | errado | 0,851 | 0,826 | campo_ausente | medio |
| `run-13` | avaliacao | `registro_duplicado` | `registro_duplicado` | certo | 0,853 | 0,853 | não medido | medio |
| `efe-6` | aprendizado | `localizador_quebrado` | `localizador_quebrado` | certo | 0,865 | 0,865 | tempo_de_resposta_excedido | medio |
| `tra-8` | avaliacao | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,876 | 0,873 | estrutura_aninhada_divergente | medio |
| `sin-4` | avaliacao | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | 0,880 | 0,880 | tipo_divergente | medio |
| `tra-14` | aprendizado | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,881 | 0,880 | tipo_divergente | medio |
| `run-8` | aprendizado | `recurso_inexistente` | `recurso_inexistente` | certo | 0,930 | 0,930 | não medido | medio |
| `tra-9` | aprendizado | `escala_ou_unidade_errada` | `formato_de_data_divergente` | errado | 0,940 | 0,940 | escala_ou_unidade_errada | medio |
| `run-12` | aprendizado | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | 0,942 | 0,939 | corpo_nao_e_json | medio |
| `semt-2` | aprendizado | `tipo_divergente` | `tipo_divergente` | certo | 0,956 | 0,956 | valor_fora_do_dominio | medio |
| `run-7` | aprendizado | `recurso_inexistente` | `recurso_inexistente` | certo | 0,957 | 0,957 | registro_duplicado | medio |
| `sin-6` | aprendizado | `campo_ausente` | `campo_ausente` | certo | 0,960 | 0,959 | colecao_no_lugar_de_objeto | medio |
| `semt-11` | aprendizado | `valor_fora_do_dominio` | `valor_fora_do_dominio` | certo | 0,966 | 0,966 | estado_da_tela_divergente | medio |
| `sin-9` | aprendizado | `campo_renomeado` | `campo_renomeado` | certo | 0,971 | 0,962 | tipo_divergente | medio |
| `run-11` | aprendizado | `dado_desatualizado` | `valor_fora_do_dominio` | errado | 0,975 | 0,975 | estado_da_tela_divergente | medio |
| `sin-15` | aprendizado | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | 0,980 | 0,980 | estrutura_aninhada_divergente | medio |
| `efe-1` | avaliacao | `localizador_quebrado` | `tempo_de_resposta_excedido` | errado | 0,980 | 0,980 | localizador_quebrado | medio |
| `tra-4` | avaliacao | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,982 | 0,979 | estrutura_aninhada_divergente | medio |
| `run-1` | avaliacao | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | 0,985 | 0,971 | corpo_nao_e_json | medio |
| `tra-11` | avaliacao | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,986 | 0,985 | estrutura_aninhada_divergente | medio |
| `run-6` | aprendizado | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | 0,987 | 0,983 | corpo_nao_e_json | medio |
| `sin-8` | aprendizado | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | 0,989 | 0,988 | estrutura_aninhada_divergente | medio |
| `semt-5` | avaliacao | `nulo_inesperado` | `nulo_inesperado` | certo | 0,989 | 0,989 | campo_ausente | medio |
| `efe-8` | aprendizado | `estado_da_tela_divergente` | `estado_da_tela_divergente` | certo | 0,990 | 0,989 | formato_de_data_divergente | medio |
| `efe-7` | avaliacao | `localizador_quebrado` | `localizador_quebrado` | certo | 0,990 | 0,989 | não medido | medio |
| `lex-12` | aprendizado | `corpo_nao_e_json` | `corpo_nao_e_json` | certo | 0,990 | 0,976 | corpo_vazio | alto |
| `sin-7` | avaliacao | `campo_ausente` | `campo_ausente` | certo | 0,990 | 0,990 | campo_renomeado | alto |
| `lex-13` | aprendizado | `corpo_vazio` | `corpo_vazio` | certo | 0,990 | 0,990 | resposta_truncada | alto |
| `semt-10` | aprendizado | `tipo_divergente` | `tipo_divergente` | certo | 0,991 | 0,991 | campo_ausente | alto |
| `efe-5` | avaliacao | `localizador_quebrado` | `localizador_quebrado` | certo | 0,993 | 0,993 | nulo_inesperado | alto |
| `sin-10` | avaliacao | `campo_renomeado` | `campo_renomeado` | certo | 0,994 | 0,993 | tipo_divergente | alto |
| `semt-3` | avaliacao | `valor_fora_do_dominio` | `valor_fora_do_dominio` | certo | 0,994 | 0,992 | formato_de_data_divergente | alto |
| `tra-13` | aprendizado | `chave_de_juncao_errada` | `chave_de_juncao_errada` | certo | 0,994 | 0,994 | campo_ausente | alto |
| `semt-9` | avaliacao | `valor_fora_do_dominio` | `tipo_divergente` | errado | 0,995 | 0,995 | valor_fora_do_dominio | alto |
| `tra-6` | aprendizado | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | certo | 0,995 | 0,995 | valor_fora_do_dominio | alto |
| `lex-9` | aprendizado | `corpo_nao_e_json` | `corpo_nao_e_json` | certo | 0,996 | 0,971 | corpo_vazio | alto |
| `tra-1` | avaliacao | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | certo | 0,996 | 0,996 | valor_fora_do_dominio | alto |
| `lex-15` | aprendizado | `corpo_nao_e_json` | `corpo_nao_e_json` | certo | 0,997 | 0,979 | erro_interno_do_servidor | alto |
| `efe-13` | aprendizado | `estado_da_tela_divergente` | `dado_desatualizado` | errado | 0,997 | 0,997 | valor_fora_do_dominio | alto |
| `run-4` | avaliacao | `dado_desatualizado` | `dado_desatualizado` | certo | 0,997 | 0,997 | tempo_de_resposta_excedido | alto |
| `run-5` | aprendizado | `registro_duplicado` | `registro_duplicado` | certo | 0,998 | 0,998 | colecao_no_lugar_de_objeto | alto |
| `lex-4` | avaliacao | `codificacao_incorreta` | `codificacao_incorreta` | certo | 0,999 | 0,998 | formato_de_data_divergente | alto |
| `tra-10` | avaliacao | `chave_de_juncao_errada` | `chave_de_juncao_errada` | certo | 0,999 | 0,999 | campo_ausente | alto |
| `efe-9` | aprendizado | `localizador_quebrado` | `localizador_quebrado` | certo | 0,999 | 0,999 | campo_ausente | alto |
| `efe-14` | avaliacao | `localizador_quebrado` | `localizador_quebrado` | certo | 0,999 | 0,999 | nulo_inesperado | alto |
| `efe-15` | aprendizado | `estado_da_tela_divergente` | `estado_da_tela_divergente` | certo | 0,999 | 0,998 | formato_de_data_divergente | alto |
| `run-9` | avaliacao | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | 0,999 | 0,999 | tipo_divergente | alto |
| `sin-13` | aprendizado | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | 0,999 | 0,999 | tipo_divergente | alto |
| `sin-3` | aprendizado | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | 0,999 | 0,999 | campo_ausente | alto |
| `efe-12` | aprendizado | `localizador_quebrado` | `localizador_quebrado` | certo | 0,999 | 0,999 | nulo_inesperado | alto |
| `run-2` | avaliacao | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | 0,999 | 0,999 | limite_de_requisicoes | alto |
| `run-14` | aprendizado | `dado_desatualizado` | `dado_desatualizado` | certo | 0,999 | 0,999 | tempo_de_resposta_excedido | alto |
| `run-15` | aprendizado | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | 0,999 | 0,999 | limite_de_requisicoes | alto |
| `lex-3` | aprendizado | `corpo_vazio` | `tempo_de_resposta_excedido` | errado | 0,999 | 0,999 | resposta_truncada | alto |
| `lex-7` | avaliacao | `corpo_vazio` | `corpo_vazio` | certo | 1,000 | 0,999 | corpo_nao_e_json | alto |
| `lex-11` | avaliacao | `codificacao_incorreta` | `codificacao_incorreta` | certo | 1,000 | 0,999 | corpo_nao_e_json | alto |
| `lex-1` | avaliacao | `resposta_truncada` | `resposta_truncada` | certo | 1,000 | 1,000 | corpo_nao_e_json | alto |
| `semt-4` | aprendizado | `formato_de_data_divergente` | `formato_de_data_divergente` | certo | 1,000 | 1,000 | tipo_divergente | alto |
| `sin-11` | avaliacao | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | 1,000 | 1,000 | campo_ausente | alto |
| `lex-5` | aprendizado | `resposta_truncada` | `resposta_truncada` | certo | 1,000 | 1,000 | corpo_nao_e_json | alto |
| `lex-10` | avaliacao | `resposta_truncada` | `resposta_truncada` | certo | 1,000 | 1,000 | corpo_nao_e_json | alto |
| `lex-14` | aprendizado | `resposta_truncada` | `resposta_truncada` | certo | 1,000 | 1,000 | formato_de_data_divergente | alto |
<!-- /tabela:tb_f4_calibracao_casos -->

</details>

<!-- ! Alteração de IA - Revisar: (05/11/2026, decisão 91) seção nova com a leitura da corrida 23.
     ! Motivo: a ficha 34 (a) e a decisão 79 mandaram medir os dois itens, e o número vai para o TCC. Números de `resultados_alvo/fase4/tela_v3.json`, `cenarios_v3.json` e `experimento_prompt.json`, lidos por script. -->
### 4.1 O experimento dos itens da decisão 55 (corrida 23)

A decisão 55 deixou para medir dois itens da literatura: um exemplar resolvido fixo no prompt e a forma dos rótulos. A corrida 23 mede cada um em separado, em texto, nos 90 casos, com a mesma biblioteca e o mesmo k da corrida 16. O prompt do agente não muda em nenhuma condição: cada uma é uma transformação de texto do prompt pronto, conferida em teste (`corridas_em_texto.py`), e o número vai para o TCC sem decidir nada na Fase 5 (decisão 91).

**Nenhuma das duas se separa do acaso.** Na corrida 16, 68 de 90 (75,6%; acurácia balanceada de 81,5%). Com o exemplar, 70 de 90 (77,8%; 83,3%), b = 6, c = 4, p = 0,754. Com os rótulos em palavras, 67 de 90 (74,4%; 79,7%), b = 5, c = 6, p = 1,000. Nos 36 casos de avaliação, a corrida 16 acertou 31, o exemplar 29 e os rótulos em palavras 30. As duas condições trocam a causa em 17 dos 90 casos, para os dois lados, e duas corridas iguais já variaram de 0 a 3 casos em 36 (Fase 3-B).

**O exemplar custa tempo e não puxa a resposta.** Ele leva o prompt de 1106,5 para 1282,5 tokens (medianas), e o tempo por caso foi de 69,6 s, contra 40,6 s da outra condição, na mesma sessão. A causa do exemplar, `erro_interno_do_servidor`, foi respondida 3 vezes, como na corrida 16 (3): o modelo não copia o exemplo.

**O modelo escreve como a lista pede.** Com os rótulos em palavras, 87 das 90 respostas vieram em palavras, 1 com o nome oficial e 2 fora da lista. Uma das 2 é `run-10`: a causa certa veio entre colchetes, com o título do verbete (`[limite_de_requisicoes] Limite de requisições`), e conta como fora da lista, como no leitor oficial; contada como certa, o saldo fica empatado e nada muda. Para a Pós-Fase 4, isso quer dizer que mostrar o nome da causa em palavras a quem lê não pede mudar o prompt: um mapa em código basta.

**Cuidado na comparação.** A corrida 16 rodou no Ollama 0.40.2, e as condições no 0.40.14. A ponte entre as duas versões deu b + c dentro do limite (seção 2), então o acerto se compara; o tempo, não. Um teste confere que a leitura nova da linha CAUSA_RAIZ devolve o mesmo acerto do leitor oficial nos 90 registros da corrida 16.

<!-- tabela:tb_f4_exp_resumo -->
| Condição | Casos | Acertos | Acerto (%) | Acurácia balanceada (%) | b | c | p (McNemar) | Nos 36 de avaliação | Trocas de rótulo | Fora do conjunto ou sem rótulo | Tokens de entrada (mediana) | Segundos (mediana) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| corrida 16 (k = 3) | 90 | 68 | 75,6 | 81,5 |  |  |  | 31 de 36 |  |  | 1106,5 | 55,36 |
| `exemplar` | 90 | 70 | 77,8 | 83,3 | 6 | 4 | 0,754 | 29 de 36 | 17 | 1 | 1282,5 | 69,56 |
| `rotulos_por_extenso` | 90 | 67 | 74,4 | 79,7 | 5 | 6 | 1,000 | 30 de 36 | 17 | 2 | 1089,5 | 40,64 |
<!-- /tabela:tb_f4_exp_resumo -->

<details><summary>Os casos que mudaram de certo para errado ou o contrário (tb_f4_exp_mudaram)</summary>

<!-- tabela:tb_f4_exp_mudaram -->
| Condição | Caso | Gabarito | Corrida 16 | Na condição | Efeito |
|---|---|---|---|---|---|
| `exemplar` | `efe-1` | `localizador_quebrado` | `tempo_de_resposta_excedido` | `localizador_quebrado` | ganhou |
| `exemplar` | `efe-3` | `campo_ausente` | `campo_ausente` | `colecao_no_lugar_de_objeto` | perdeu |
| `exemplar` | `lex-3` | `corpo_vazio` | `tempo_de_resposta_excedido` | `corpo_vazio` | ganhou |
| `exemplar` | `lex-6` | `corpo_nao_e_json` | `recurso_inexistente` | `corpo_nao_e_json` | ganhou |
| `exemplar` | `semt-1` | `tipo_divergente` | `tipo_divergente` | `formato_de_data_divergente` | perdeu |
| `exemplar` | `semt-13` | `tipo_divergente` | `tipo_divergente` | `escala_ou_unidade_errada` | perdeu |
| `exemplar` | `semt-6` | `tipo_divergente` | `colecao_no_lugar_de_objeto` | `tipo_divergente` | ganhou |
| `exemplar` | `semt-8` | `nulo_inesperado` | `nulo_inesperado` | `valor_fora_do_dominio` | perdeu |
| `exemplar` | `sin-2` | `campo_renomeado` | `tipo_divergente` | `campo_renomeado` | ganhou |
| `exemplar` | `tra-12` | `escala_ou_unidade_errada` | `tipo_divergente` | `escala_ou_unidade_errada` | ganhou |
| `rotulos_por_extenso` | `efe-2` | `estado_da_tela_divergente` | `estado_da_tela_divergente` | `valor_fora_do_dominio` | perdeu |
| `rotulos_por_extenso` | `efe-6` | `localizador_quebrado` | `localizador_quebrado` | `tempo_de_resposta_excedido` | perdeu |
| `rotulos_por_extenso` | `efe-8` | `estado_da_tela_divergente` | `estado_da_tela_divergente` | `colecao_no_lugar_de_objeto` | perdeu |
| `rotulos_por_extenso` | `run-10` | `limite_de_requisicoes` | `limite_de_requisicoes` | `[limite_de_requisicoes] Limite de requisições` | perdeu |
| `rotulos_por_extenso` | `semt-13` | `tipo_divergente` | `tipo_divergente` | `formato_de_data_divergente` | perdeu |
| `rotulos_por_extenso` | `semt-6` | `tipo_divergente` | `colecao_no_lugar_de_objeto` | `tipo_divergente` | ganhou |
| `rotulos_por_extenso` | `semt-8` | `nulo_inesperado` | `nulo_inesperado` | `tipo_divergente` | perdeu |
| `rotulos_por_extenso` | `sin-14` | `campo_renomeado` | `colecao_no_lugar_de_objeto` | `campo_renomeado` | ganhou |
| `rotulos_por_extenso` | `sin-2` | `campo_renomeado` | `tipo_divergente` | `campo_renomeado` | ganhou |
| `rotulos_por_extenso` | `sin-5` | `campo_ausente` | `colecao_no_lugar_de_objeto` | `campo_ausente` | ganhou |
| `rotulos_por_extenso` | `tra-3` | `chave_de_juncao_errada` | `tipo_divergente` | `chave_de_juncao_errada` | ganhou |
<!-- /tabela:tb_f4_exp_mudaram -->

</details>

## 5. A tela contra o caso escrito (corridas 18, 18b, 18c, 18d e 18e, regra R2)

<!-- ! Alteração de IA - Revisar: (06/11/2026, decisão 98) a seção 5, a seção 1, a linha R2 da seção 10 e as seções 12, 14 e 15 passam a dizer a regra R2 pelos casos que a tela perde, com a soma ao lado.
     ! Motivo: o Eric fixou essa leitura antes da corrida 18d, porque a soma contaria como defeito o caso que só a tela acerta; o que a regra dizia até a 18c continua aqui, e os números vêm dos campos `b`, `c` e `discordantes` de `tela.json`, `tela_v2.json` e `tela_v3.json`. -->
A regra R2 pede que, nos casos que reproduzem, o rótulo do caso lido da tela e o do mesmo caso lido do fixture (o caso escrito), na mesma sessão do Ollama, difiram em no máximo 3 casos, que é a variação entre corridas iguais. O texto do plano não diz para que lado. Até a corrida 18c, a conta foi b + c até 3, em que b são os casos que só a tela acerta e c, os que só o caso escrito acerta. Em 06/11/2026, antes da corrida 18d e sem conhecer o resultado dela, o Eric fixou a leitura pelo que a regra protege, a tela não piorar: c até 3, com b e a soma ao lado (ficha 48, decisão 98). Nas corridas 18, 18b e 18c o estado é o mesmo nas duas contas: c foi 16, 7 e 5, e a soma, 17, 9 e 7.

**A corrida 18 mediu um defeito do caso de entrada, não o agente** (`tela.json`): mesmo rótulo em 16 de 37, 16 acertos na tela contra 31 no fixture, b = 1, c = 16, p = 0,0003. Em 22 dos 37 casos a poda não achou diferença de campo contra o contrato e levou ao modelo o primeiro produto da lista, normal; `colecao_no_lugar_de_objeto` saiu 12 vezes na tela. A decisão 81 (ficha 37) passou a levar ao caso ao vivo o que mudou contra a referência em modo normal, no CORPO e no SINTOMA, e a corrida foi repetida em pasta nova.

**A corrida 18b corrigiu o caso de entrada (decisão 82)** (`tela_v2.json`): mesmo rótulo em 26 de 37 (70,3%), 26 acertos na tela (70,3%) contra 31 no fixture (83,8%), b = 2, c = 7, p = 0,180. Nos 22 casos sem diferença de campo, 16 dão o mesmo rótulo (eram 5) e 15 acertam na tela (eram 5); `colecao_no_lugar_de_objeto` cai de 12 para 2 na tela. Entre as duas corridas, 11 casos passaram a acertar na tela, 1 deixou (`sin-11`) e o rótulo da tela mudou em 17.

**Na 18b, a regra R2 ficou como limitação declarada (decisão 82):** b + c = 9 continuou acima do limite de 3. O limite não mudou, o saldo é de +10 acertos na tela contra a corrida 18, e o molde do sintoma não passou por terceira revisão, porque descrever melhor sem citar a causa começaria a escrever a resposta no sintoma. O teste pareado não separa os dois lados nesses 37 casos (p = 0,180), mas o limite da regra é o da variação entre corridas iguais, e 9 casos é o triplo dele. O que sobra são, na maior parte, confusões entre rótulos vizinhos; `semt-21` e `run-19` não têm essa leitura. Os 11 erros na tela: `lex-8`, `codificacao_incorreta` lido como `formato_de_data_divergente`; `sin-11`, `estrutura_aninhada_divergente` lido como `tipo_divergente`; `semt-9`, `valor_fora_do_dominio` lido como `tipo_divergente`; `lex-18`, `codificacao_incorreta` lido como `formato_de_data_divergente`; `sin-21`, `estrutura_aninhada_divergente` lido como `tipo_divergente`; `semt-17`, `nulo_inesperado` lido como `campo_ausente`; `semt-20`, `valor_fora_do_dominio` lido como `tipo_divergente`; `semt-21`, `valor_fora_do_dominio` lido como `campo_renomeado`; `tra-17`, `chave_de_juncao_errada` lido como `tipo_divergente`; `tra-20`, `chave_de_juncao_errada` lido como `tipo_divergente`; `run-19`, `tempo_de_resposta_excedido` lido como `colecao_no_lugar_de_objeto`. Em resumo, o agente na tela acerta menos que o mesmo agente lendo o caso que uma pessoa escreveu, e esta fase não fechou essa diferença.

**O prompt da tela passou do limite do plano, e o Eric decidiu encurtar e repetir (ficha 42, decisão 90).** O plano (seção 3.3) fixou antes de rodar que o prompt ao vivo não passa o maior prompt da calibração (1281 tokens) em mais de 10% (1409 tokens), e que, se passar, a poda aperta antes da próxima corrida. Nas duas corridas os 37 prompts passaram do limite: o maior foi de 1939 tokens na 18 e de 2034 na 18b, porque a revisão do caso ao vivo acrescentou texto. A poda não apertou. Nos dez cenários, 9 de 10 prompts passam do limite. O limite importa por dois motivos: os limiares do selo foram calibrados com prompts menores, e o tempo do diagnóstico cresce com o prompt (seção 8). A medida sem modelo nos prompts guardados (`medir_prompt_tela.py`, `resultados_alvo/fase4/prompt_tela_blocos.json`) mostra que só a árvore não basta: reduzida ao título e ao que difere da referência em modo normal, ela ainda deixa 12 de 37 prompts da corrida 18b e 5 de 10 da 21b acima de 1409 tokens, e sem nenhuma árvore ficam 4 e 1. Tirando também a linha OBSERVAÇÃO ADICIONAL e as listas `faltam` e `sobram` do SINTOMA, sobram 1 e 3, por causa de linhas repetidas e de linhas que a referência podada não tem, que o corte em código trata. As corridas 18c e 21c repetem a 18b e a 21b em pasta nova, com o caso ao vivo encurtado e o prompt fixo intacto; o resultado vem a seguir.

<!-- ! Alteração de IA - Revisar: (05/11/2026) parágrafo novo com o corte do caso ao vivo e a conferência sem modelo, antes da corrida 18c (decisões 90 e 96).
     ! Motivo: a decisão 90 mandou conferir sem modelo os prompts novos e os verbetes recuperados; o resultado da conferência fica registrado antes das corridas, e os números vêm de `resultados_alvo/fase4/corte_prompt_tela.json`. -->
**O corte, conferido sem modelo (decisões 90 e 96).** O caso ao vivo passou a levar só o que difere da referência em modo normal: a árvore fica com o título e as linhas que mudaram, o SINTOMA guarda a contagem de linhas e perde as listas, e a linha OBSERVAÇÃO ADICIONAL sai do prompt. `conferir_corte_tela.py` monta, sem modelo e com as cobaias de verdade, o prompt que as corridas 18c e 21c mandariam: os 47 ficam abaixo de 1409 tokens, com o maior em 1395 nos 37 casos da 18b e 1358 nos 10 da 21b, estimados pela razão de tokens por caractere de cada prompt guardado. O corte sozinho derrubava o verbete certo no contexto, porque a busca compara o corpo com o contrato e um trecho podado parece ter campos ausentes; com a busca lendo o corpo inteiro (decisão 96), o verbete certo vai de 15 para 21 dos 37 casos e de 5 para 9 dos 10 cenários (medido nos registros; a conferência dizia 1 na 21b, porque não achava o prompt guardado dos quatro cenários de localizador). No caso escrito, com os mesmos verbetes de produção, são 27 dos 37. Isso é a conferência; a medida é a corrida 18c.

<!-- ! Alteração de IA - Revisar: (05/11/2026, decisões 90 e 96) parágrafos novos com a leitura da corrida 18c, que passa a ser a vigente; os blocos abaixo são dela.
     ! Motivo: a decisão 90 diz que a leitura nova passa a valer quando a corrida rodar. Números de `resultados_alvo/fase4/tela_v3.json`, `cenarios_v3.json` e `experimento_prompt.json`, lidos por script. -->
**A corrida 18c** (`tela_v3.json`): os 37 prompts ficaram dentro do limite, de 1069 a 1373 tokens (na 18b, de 1595 a 2034). Mesmo rótulo em 28 de 37 (75,7%), 27 acertos na tela (73,0%) contra 30 no fixture (81,1%), b = 2, c = 5, p = 0,453. O tempo por caso na tela caiu de 82,5 s para 52,0 s (medianas). No fixture, que não encurtou, foi de 51,5 s para 55,0 s: o ganho vem do prompt menor, não da versão do Ollama.

**Na 18c, a regra R2 seguiu como limitação declarada (decisão 82):** a tela perde 5 casos para o caso escrito e ganha 2. São 5 contra o limite de 3 pela leitura da decisão 98, e a soma dos dois lados, a conta de até então, dá 7. O molde do sintoma não passou por terceira revisão, porque a decisão 90 só alcança o que sai do prompt. Caso a caso contra a 18b, passaram a acertar na tela `semt-17`, `sin-11`, `sin-21`, e deixaram de acertar `tra-4`, `tra-8`, em que a falta do último item da lista passou a ser lida como `resposta_truncada`, com selo baixo. A causa na tela mudou em 8 dos 37 casos. A 18c trocou também a versão do Ollama e a biblioteca (a de produção, `95af35290860`, no lugar da curada), e o fixture serve de controle: ali a causa mudou em 1 (`semt-20`).

**Na 18c, o que separava a tela do caso escrito era a busca** (`tela_v3.json`, campo `verbete_certo`). Com o verbete da causa certa entre os entregues, a tela acerta 19 de 21 e o fixture 26 de 27; sem ele, 8 de 16 e 4 de 10. A diferença é quantas vezes o verbete chega: 21 na tela (eram 15 na 18b, antes de a busca ler o corpo inteiro, decisão 96) e 27 no fixture. Dos 10 erros na tela, 8 são de casos sem o verbete certo, e 7 respondem `tipo_divergente`: essa causa sai 9 vezes na tela, 5 no fixture, e é o gabarito de 2 casos. O Eric decidiu mexer na busca (ficha 47, decisão 97): os sinais novos, conferidos sem modelo, levam o verbete certo a 36 dos 37 casos, e a medida com o modelo são as corridas 18d, 21d e 18e, a seguir. Se um dia for preciso voltar, a chave `caso_ao_vivo.SINAIS_DA_REFERENCIA_NA_BUSCA` devolve a busca à da 18c.

**Na 18c, o selo ficou mais útil com o prompt do tamanho da calibração** (`tela_v3.json`, campo `acerto_por_selo`): selo alto acerta 14 de 15, médio 7 de 9 e baixo 6 de 13; na 18b eram 9 de 11, 15 de 18 e 2 de 8. O único erro com selo alto é `semt-9`. São poucos casos: é triagem, não barreira.

<!-- ! Alteração de IA - Revisar: (06/11/2026, decisões 97 a 99) parágrafos novos com a leitura das corridas 18d e 18e; os blocos abaixo passam a ser da 18d.
     ! Motivo: a regra R2 fechou na 18d pela leitura fixada antes dela, e o agente fica com os sinais novos da busca. Números de `tela_v3.json`, `tela_v4.json`, `tela_ineditos.json` e `teto_prompt_tela.json`, lidos por script. -->
**A corrida 18d é a que vale agora, e os blocos abaixo são dela** (`tela_v4.json`): com os sinais da busca, o verbete certo chega ao modelo em 36 dos 37 casos na tela (eram 21), contra 27 no fixture, como a conferência sem modelo previa. O acerto na tela foi de 27 para 32 (86,5%), e o do fixture ficou em 30 (81,1%). Mesmo rótulo em 28 de 37 (75,7%), b = 5, c = 3, p = 0,727. Os 37 prompts ficaram dentro do limite, de 1069 a 1385 tokens, e o tempo por caso foi de 52,0 s para 59,2 s na tela e de 55,0 s para 58,0 s no fixture (medianas).

**A regra R2 fechou, pela leitura fixada antes da corrida (decisão 98):** a tela perde 3 casos para o fixture, no limite exato, e ganha 5. Pela conta de antes, a soma dá 8, e a regra ficaria fora pelo lado bom; as duas contas ficam no bloco `tb_f4_tela_resumo`. Não há folga: corridas iguais já variaram até 3 casos, e o teste pareado não separa os dois lados (p = 0,727). A limitação declarada pela decisão 82 valia enquanto a regra estivesse fora, e deixa de valer para a leitura vigente.

**O fixture é o controle:** da 18c para a 18d, na mesma versão do Ollama e com a mesma biblioteca, a causa mudou em 0 dos 37 casos no fixture, que não recebe os sinais. Na tela mudou em 7: passaram a acertar `lex-8`, `lex-18`, `semt-20`, `tra-17`, `tra-20` e `run-19`, e deixou de acertar `tra-21`. A diferença é dos sinais. **Isso não quer dizer que o modelo lê melhor da tela:** o caso da tela leva a medida contra a referência em modo normal, que o caso escrito não tem. O que a corrida mostra é que, quando o verbete certo chega, o modelo acerta nos dois lados: 32 de 36 na tela e 26 de 27 no fixture.

**O que a tela ainda perde é uma confusão só:** `contagem_inconsistente` lido como `resposta_truncada` em `tra-4`, `tra-8` e `tra-21`, os três com o verbete certo entregue e selo baixo. A falta de um item da lista parece, ao modelo, uma resposta cortada: não é a busca, é a leitura de dois verbetes vizinhos. Erram nos dois lados `semt-9` e `semt-21`, com selo alto; `semt-9` é o único caso sem o verbete certo. O selo alto acerta 18 de 20, o médio 12 de 12 e o baixo 2 de 5, com os limiares da corrida 16.

**A conferência limpa é a corrida 18e** (`tela_ineditos.json`): os sinais foram escritos olhando os 37 casos, e os 25 inéditos da ficha 27 que reproduzem na tela não foram olhados antes. Neles, 22 acertos na tela (88,0%) contra 18 no fixture (72,0%), mesmo rótulo em 19 de 25, b = 4 (`sin-26`, `semt-23`, `tra-22` e `tra-27`), c = 0, p = 0,125; o verbete certo chega em 23 de 25 na tela e em 14 no fixture. O ganho da busca se repete em casos novos, e a tela não perde nenhum. São 25 casos, e a conferência do Eric (ficha 46), feita depois desta corrida, não mudou nenhum deles (decisão 100). Depois desta leitura, esses casos não servem mais de conferência limpa para outro ajuste na busca.

**Dois prompts da 18e passaram do limite, e o caso ao vivo ganhou um teto (decisão 99):** `semt-27`, em que todos os ids vêm trocados por negativos, com 1829 tokens, e `tra-26`, com seis campos diferentes, com 1620: a comparação escrevia tudo o que falta, sobra ou difere. Os dois erram também no fixture, então não podem entrar em c, e a regra R2 não depende deles. O teto (até 3 ids por cláusula, até 3 ids repetidos e até 2 campos com detalhe) os leva a 1367 e 1387 tokens, medidos com o próprio Ollama (`teto_prompt_tela.json`), e não muda os prompts das corridas 18d e 21d: 44 de 47 ficaram iguais byte a byte, e os outros 3 só mudam o tempo da referência medido na hora. Em `semt-27` há um segundo efeito, que ficou como está: a busca conta cada id trocado como item faltando ou sobrando e vai para `contagem_inconsistente`, mesmo com a lista do mesmo tamanho. Mexer nisso agora seria ajustar olhando os inéditos.

<!-- tabela:tb_f4_tela_verbete -->
| Lado | Verbete da causa certa entre os entregues | Casos | Acertos | Acerto (%) |
|---|---|---|---|---|
| tela | sim | 36 | 32 | 88,9 |
| tela | não | 1 | 0 | 0,0 |
| fixture | sim | 27 | 26 | 96,3 |
| fixture | não | 10 | 4 | 40,0 |
<!-- /tabela:tb_f4_tela_verbete -->

<!-- tabela:tb_f4_tela_selo -->
| Selo na tela | Casos | Acertos | Acerto (%) |
|---|---|---|---|
| alto | 20 | 18 | 90,0 |
| medio | 12 | 12 | 100,0 |
| baixo | 5 | 2 | 40,0 |
<!-- /tabela:tb_f4_tela_selo -->

<!-- tabela:tb_f4_tela_resumo -->
| Casos | Reproduzem na tela | Acerto na tela | Acerto no fixture | Concordam (mesmo rótulo) | Concordância (%) | b (só a tela acerta) | c (só o fixture acerta) | b + c | Limite R2 (c) | Dentro do limite | b + c até o limite (conta de antes) | p (McNemar exato) | Selos na tela (alto / médio / baixo) | Gatilhos na tela | Divergências na tela | s por caso na tela (mediana) | s por caso no fixture (mediana) | Trilha (bytes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 37 | 37 | 32 (86,5%) | 30 (81,1%) | 28 | 75,7 | 5 | 3 | 8 | 3 | sim | não | 0,727 | 20 / 12 / 5 | 6 | 5 | 59,2 | 58,0 | 2051641 |
<!-- /tabela:tb_f4_tela_resumo -->

<!-- tabela:tb_f4_tela_por_classe -->
| Classe | Casos | Acerto na tela | Acerto no fixture | Concordam |
|---|---|---|---|---|
| 1 | 8 | 8 | 7 | 7 |
| 2 | 7 | 7 | 5 | 5 |
| 3 | 8 | 6 | 5 | 6 |
| 4 | 8 | 5 | 7 | 4 |
| 5 | 5 | 5 | 5 | 5 |
| 6 | 1 | 1 | 1 | 1 |
<!-- /tabela:tb_f4_tela_por_classe -->

<!-- tabela:tb_f4_tela_rotulos -->
| Rótulo | Dado na tela | Dado no fixture | É o gabarito de |
|---|---|---|---|
| `campo_ausente` | 4 | 4 | 4 |
| `resposta_truncada` | 6 | 3 | 3 |
| `codificacao_incorreta` | 4 | 3 | 4 |
| `tipo_divergente` | 3 | 5 | 2 |
| `contagem_inconsistente` | 1 | 4 | 4 |
| `nulo_inesperado` | 3 | 3 | 3 |
| `tempo_de_resposta_excedido` | 3 | 3 | 3 |
| `escala_ou_unidade_errada` | 2 | 2 | 2 |
| `estrutura_aninhada_divergente` | 2 | 2 | 2 |
| `chave_de_juncao_errada` | 2 | 1 | 2 |
| `colecao_no_lugar_de_objeto` | 1 | 3 | 1 |
| `valor_fora_do_dominio` | 1 | 1 | 3 |
| `campo_renomeado` | 2 | 0 | 1 |
| `corpo_vazio` | 1 | 1 | 1 |
| `erro_interno_do_servidor` | 1 | 1 | 1 |
| `registro_duplicado` | 1 | 1 | 1 |
<!-- /tabela:tb_f4_tela_rotulos -->

<!-- tabela:tb_f4_tela_corpo -->
| Casos com o caso ao vivo lido | Sem diferença contra o contrato | Desses, mesmo rótulo | Desses, acerto na tela | Desses, colecao_no_lugar_de_objeto na tela | Com diferença contra o contrato | Desses, mesmo rótulo | Desses, acerto na tela | Sintoma "Nenhuma diferença medida" |
|---|---|---|---|---|---|---|---|---|
| 37 | 22 | 15 | 18 | 0 | 15 | 13 | 14 | 0 |
<!-- /tabela:tb_f4_tela_corpo -->

<details><summary>Caso a caso da corrida 18b (tb_f4_tela_casos)</summary>

<!-- tabela:tb_f4_tela_casos -->
| Caso | Classe | Gabarito | Rótulo na tela | Rótulo no fixture | Tela | Fixture | Concordam | p tela | Selo tela | p fixture | Selo fixture | Gatilho | Divergência | s tela | s fixture | Diferenças contra o contrato | CORPO do caso ao vivo (começo) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-1` | 1 | `resposta_truncada` | `resposta_truncada` | `resposta_truncada` | certo | certo | sim | 0,999 | alto | 1,000 | alto | não | não | 87,8 | 69,1 | 0 | `...[{"id": 1, "nome": "resposta truncada de propos` |
| `lex-4` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `codificacao_incorreta` | certo | certo | sim | 0,989 | medio | 0,999 | alto | não | não | 76,4 | 51,1 | 0 | `lista com 14 itens (referência em modo normal: 14); nome dif` |
| `sin-4` | 2 | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | certo | sim | 0,998 | alto | 0,865 | medio | não | não | 84,1 | 40,2 | 1 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `sin-5` | 2 | `campo_ausente` | `campo_ausente` | `colecao_no_lugar_de_objeto` | certo | errado | não | 0,949 | medio | 0,625 | baixo | não | não | 67,5 | 58,9 | 1 | `{"resumo": "(ausente)"}` |
| `semt-1` | 3 | `tipo_divergente` | `tipo_divergente` | `tipo_divergente` | certo | certo | sim | 0,999 | alto | 0,929 | medio | não | não | 71,3 | 73,7 | 1 | `{"preco": "89.9"}` |
| `tra-1` | 4 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | certo | certo | sim | 0,980 | medio | 0,996 | alto | não | não | 88,5 | 83,5 | 0 | `lista com 14 itens (referência em modo normal: 14); preco di` |
| `tra-4` | 4 | `contagem_inconsistente` | `resposta_truncada` | `contagem_inconsistente` | errado | certo | não | 0,507 | baixo | 0,968 | medio | sim | sim | 68,7 | 77,7 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `run-1` | 5 | `erro_interno_do_servidor` | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | certo | sim | 0,991 | alto | 0,979 | medio | não | não | 83,9 | 60,3 | 9 | `{"detail": "fault injection: error_500 em produto", "id": "(` |
| `run-2` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | certo | sim | 0,999 | alto | 1,000 | alto | não | não | 54,5 | 70,5 | 0 | `lista com 14 itens, igual à referência em modo normal; prime` |
| `efe-3` | 6 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 0,989 | medio | 0,566 | baixo | não | não | 36,7 | 48,8 | 1 | `{"imagem": "(ausente)"}` |
| `lex-7` | 1 | `corpo_vazio` | `corpo_vazio` | `corpo_vazio` | certo | certo | sim | 0,996 | alto | 0,999 | alto | não | não | 80,8 | 58,0 | 0 | n/d |
| `lex-8` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `codificacao_incorreta` | certo | certo | sim | 0,981 | medio | 0,679 | baixo | não | não | 42,5 | 64,8 | 0 | `lista com 14 itens (referência em modo normal: 14); resumo d` |
| `lex-10` | 1 | `resposta_truncada` | `resposta_truncada` | `resposta_truncada` | certo | certo | sim | 0,999 | alto | 1,000 | alto | não | sim | 16,0 | 75,5 | 0 | `...[{"id": 1, "nome": "resposta truncada de propos` |
| `lex-11` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `codificacao_incorreta` | certo | certo | sim | 0,989 | medio | 1,000 | alto | não | não | 43,3 | 71,1 | 0 | `lista com 14 itens (referência em modo normal: 14); nome dif` |
| `sin-11` | 2 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | certo | sim | 0,957 | medio | 1,000 | alto | não | não | 76,0 | 77,3 | 1 | `{"preco": {"valor": 89.9, "moeda": "BRL"}}` |
| `sin-14` | 2 | `campo_renomeado` | `campo_renomeado` | `colecao_no_lugar_de_objeto` | certo | errado | não | 0,998 | alto | 0,309 | baixo | não | não | 70,6 | 55,6 | 1 | `{"imagem_v2": "picanha_alho.jpg"}` |
| `semt-8` | 3 | `nulo_inesperado` | `nulo_inesperado` | `nulo_inesperado` | certo | certo | sim | 0,996 | alto | 0,850 | medio | não | não | 68,5 | 70,3 | 1 | `{"preco": null}` |
| `semt-9` | 3 | `valor_fora_do_dominio` | `tipo_divergente` | `tipo_divergente` | errado | errado | sim | 0,998 | alto | 0,998 | alto | não | não | 73,4 | 54,3 | 1 | `{"destaque": "talvez"}` |
| `semt-14` | 3 | `nulo_inesperado` | `nulo_inesperado` | `nulo_inesperado` | certo | certo | sim | 0,997 | alto | 0,740 | baixo | não | não | 35,6 | 54,2 | 1 | `{"tipo": null}` |
| `tra-8` | 4 | `contagem_inconsistente` | `resposta_truncada` | `contagem_inconsistente` | errado | certo | não | 0,474 | baixo | 0,976 | medio | sim | sim | 15,5 | 38,1 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `tra-11` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | `contagem_inconsistente` | certo | certo | sim | 0,777 | baixo | 0,979 | medio | sim | não | 48,9 | 68,7 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `run-9` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | certo | sim | 0,999 | alto | 0,999 | alto | não | não | 55,7 | 55,8 | 0 | `lista com 14 itens, igual à referência em modo normal; prime` |
| `lex-16` | 1 | `resposta_truncada` | `resposta_truncada` | `resposta_truncada` | certo | certo | sim | 0,999 | alto | 1,000 | alto | não | não | 88,2 | 54,1 | 0 | `...[{"id": 1, "nome": "resposta truncada de propos` |
| `lex-18` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `valor_fora_do_dominio` | certo | errado | não | 0,981 | medio | 0,423 | baixo | não | não | 42,6 | 58,0 | 0 | `lista com 14 itens (referência em modo normal: 14); resumo d` |
| `sin-16` | 2 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 0,992 | alto | 0,997 | alto | não | não | 52,8 | 39,0 | 1 | `{"destaque": "(ausente)"}` |
| `sin-20` | 2 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 0,986 | medio | 0,997 | alto | não | não | 54,0 | 46,2 | 1 | `{"id": "(ausente)"}` |
| `sin-21` | 2 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | certo | sim | 0,993 | alto | 0,999 | alto | não | não | 83,8 | 69,2 | 1 | `{"tipo": {"valor": "Carnes", "moeda": "BRL"}}` |
| `semt-16` | 3 | `tipo_divergente` | `tipo_divergente` | `tipo_divergente` | certo | certo | sim | 0,999 | alto | 0,960 | medio | não | não | 36,7 | 51,9 | 1 | `{"tipo": 1}` |
| `semt-17` | 3 | `nulo_inesperado` | `nulo_inesperado` | `nulo_inesperado` | certo | certo | sim | 0,972 | medio | 0,913 | medio | não | não | 37,1 | 60,7 | 1 | `{"id": null}` |
| `semt-20` | 3 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | `tipo_divergente` | certo | errado | não | 0,644 | baixo | 0,527 | baixo | sim | não | 81,5 | 36,7 | 0 | `lista com 14 itens (referência em modo normal: 14); preco di` |
| `semt-21` | 3 | `valor_fora_do_dominio` | `campo_renomeado` | `campo_ausente` | errado | errado | não | 0,998 | alto | 0,960 | medio | sim | sim | 44,9 | 51,5 | 0 | `lista com 14 itens (referência em modo normal: 14); nome dif` |
| `tra-17` | 4 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | `tipo_divergente` | certo | errado | não | 0,995 | alto | 0,878 | medio | não | não | 85,5 | 35,3 | 0 | `lista com 14 itens (referência em modo normal: 14); tipo dif` |
| `tra-19` | 4 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | certo | certo | sim | 0,980 | medio | 0,612 | baixo | não | não | 17,8 | 43,1 | 0 | `lista com 14 itens (referência em modo normal: 14); preco di` |
| `tra-20` | 4 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | `chave_de_juncao_errada` | certo | certo | sim | 0,995 | alto | 0,997 | alto | não | não | 17,9 | 71,2 | 0 | `lista com 14 itens (referência em modo normal: 14); tipo dif` |
| `tra-21` | 4 | `contagem_inconsistente` | `resposta_truncada` | `contagem_inconsistente` | errado | certo | não | 0,791 | baixo | 0,986 | medio | sim | sim | 47,3 | 54,7 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `run-19` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | certo | sim | 0,981 | medio | 1,000 | alto | não | não | 71,2 | 61,1 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `run-21` | 5 | `registro_duplicado` | `registro_duplicado` | `registro_duplicado` | certo | certo | sim | 0,999 | alto | 0,895 | medio | não | não | 59,2 | 65,5 | 0 | `lista com 15 itens (referência em modo normal: 14); o id 1 (` |
<!-- /tabela:tb_f4_tela_casos -->

</details>

## 6. Cura de seletor (corrida 19, regra R3)

Quatro roteiros do front legado, quatro modos de quebra (`id_renomeado`, `classe_trocada`, `texto_alterado`, `estrutura_alterada`), as duas formas da ficha 29 (c), armada pelo harness no navegador e feita no HTML pela variante do front PHP, e cinco repetições: 160 execuções, sem modelo. Uma cura só conta quando a conferência final do roteiro passa na reexecução (regra R3). Foram 160 quebras e 160 curas (100,0%), 160 pelo mesmo elemento da referência e 0 por outro. O MTTR do agente sem modelo teve mediana de 0,639 s (mínimo 0,355, máximo 0,887).

**As duas formas de quebra (decisão 80):** a árvore de acessibilidade da página quebrada é a mesma em 16 das 16 células comparadas, e o resultado (quebrou, curou, estratégia) também é o mesmo em 16. Nos modos testados, a quebra armada no navegador representa a que a variante do PHP produz.

**O que os 100% querem dizer:** vêm do desenho da corrida. A quebra é armada, não ocorrida. Em cada célula o passo do alvo usa o estilo de localizador que o modo quebra, porque com os localizadores do P2 só 3 das 16 células quebrariam (roadmap §2.11). A mudança de texto acrescenta uma palavra, e um sinônimo ficaria abaixo do limiar do nome (0,6). A corrida 21 mostrou o que esta não via: com o modelo pensando entre a detecção e a cura, a página pode mudar sozinha (seção 8).

<!-- tabela:tb_f4_cura_resumo -->
| Execuções | Quebras detectadas | Não quebrou | Curadas | Não curadas | Taxa de cura (%) | Mesmo elemento | Outro elemento | MTTR mediana (s) | MTTR mínimo (s) | MTTR máximo (s) | Reexecuções (mediana) | Repetições | Limiar do nome | Formas | Tempo limite (ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 160 | 160 | 0 | 160 | 0 | 100,0 | 160 | 0 | 0,639 | 0,355 | 0,887 | 1,0 | 5 | 0,6 | harness, php | 5000 |
<!-- /tabela:tb_f4_cura_resumo -->

<!-- tabela:tb_f4_cura_por_modo -->
| Modo de quebra | Execuções | Quebraram | Curadas | Taxa de cura (%) | Mesmo elemento | Outro elemento | Não curadas | Não quebrou | MTTR mediana (s) | MTTR máximo (s) | Estratégias aplicadas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `id_renomeado` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,617 | 0,887 | `papel_e_nome` 40 |
| `classe_trocada` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,631 | 0,824 | `papel_e_nome` 40 |
| `texto_alterado` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,675 | 0,886 | `papel_e_nome` 10, `papel_e_nome_parecido` 30 |
| `estrutura_alterada` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,619 | 0,822 | `papel_e_nome` 40 |
<!-- /tabela:tb_f4_cura_por_modo -->

<!-- tabela:tb_f4_cura_por_roteiro -->
| Roteiro | Execuções | Quebraram | Curadas | Taxa de cura (%) | Mesmo elemento | Outro elemento | Não curadas | Não quebrou | MTTR mediana (s) | MTTR máximo (s) | Estratégias aplicadas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `front-busca` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,510 | 0,713 | `papel_e_nome` 40 |
| `front-admin-login` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,395 | 0,448 | `papel_e_nome` 30, `papel_e_nome_parecido` 10 |
| `front-admin-produtos` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,776 | 0,887 | `papel_e_nome` 30, `papel_e_nome_parecido` 10 |
| `front-cliente-reserva` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,714 | 0,886 | `papel_e_nome` 30, `papel_e_nome_parecido` 10 |
<!-- /tabela:tb_f4_cura_por_roteiro -->

<!-- tabela:tb_f4_cura_por_forma -->
| Forma da quebra | Execuções | Quebraram | Curadas | Taxa de cura (%) | Mesmo elemento | Outro elemento | Não curadas | Não quebrou | MTTR mediana (s) | MTTR máximo (s) | Estratégias aplicadas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `harness` | 80 | 80 | 80 | 100,0 | 80 | 0 | 0 | 0 | 0,632 | 0,886 | `papel_e_nome` 65, `papel_e_nome_parecido` 15 |
| `php` | 80 | 80 | 80 | 100,0 | 80 | 0 | 0 | 0 | 0,639 | 0,887 | `papel_e_nome` 65, `papel_e_nome_parecido` 15 |
<!-- /tabela:tb_f4_cura_por_forma -->

<!-- tabela:tb_f4_cura_formas -->
| Células comparadas (harness e php) | Mesma árvore da página quebrada | Árvore diferente em | Mesmo resultado (quebrou, curou, estratégia) |
|---|---|---|---|
| 16 | 16 | nenhuma | 16 |
<!-- /tabela:tb_f4_cura_formas -->

<!-- tabela:tb_f4_cura_estrategias -->
| Estratégia | Gerada | Passou as estáticas | Reexecutada | Aplicada (curou) | Recusada em resolve_um_elemento | Recusada em visivel_e_habilitado | Recusada em mesmo_papel | Recusada em nome_parecido | Recusada em efeito_na_reexecucao |
|---|---|---|---|---|---|---|---|---|---|
| `papel_e_nome` | 130 | 130 | 130 | 130 | 0 | 0 | 0 | 0 | 0 |
| `papel_e_nome_parecido` | 30 | 30 | 30 | 30 | 0 | 0 | 0 | 0 | 0 |
| `texto_contido` | 110 | 70 | 0 | 0 | 0 | 0 | 40 | 0 | 0 |
| `data_id` | 40 | 30 | 0 | 0 | 10 | 0 | 0 | 0 | 0 |
| `caminho_do_ancestral_com_id` | 160 | 120 | 0 | 0 | 40 | 0 | 0 | 0 | 0 |
| `posicao_entre_irmaos` | 160 | 150 | 0 | 0 | 0 | 0 | 0 | 10 | 0 |
<!-- /tabela:tb_f4_cura_estrategias -->

<!-- tabela:tb_f4_cura_outro_elemento -->
| Execução | Roteiro | Modo | Forma | Estratégia aplicada | Seletor curado | MTTR (s) |
|---|---|---|---|---|---|---|
| nenhuma |  |  |  |  |  |  |
<!-- /tabela:tb_f4_cura_outro_elemento -->

<!-- tabela:tb_f4_cura_nao_curadas -->
| Execução | Roteiro | Modo | Forma | Falha | Reexecuções | Fora do passo do alvo | Erro |
|---|---|---|---|---|---|---|---|
| nenhuma |  |  |  |  |  |  |  |
<!-- /tabela:tb_f4_cura_nao_curadas -->

<details><summary>Execução a execução (tb_f4_cura_execucoes)</summary>

<!-- tabela:tb_f4_cura_execucoes -->
| Execução | Localizador | Quebrou | Passo | Curada | Estratégia | Seletor curado | Mesmo elemento | Falha | MTTR (s) | Reexecuções | Segundos |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `front-busca/id_renomeado/harness/r1` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,519 | 1 | 5,8 |
| `front-busca/id_renomeado/harness/r2` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,511 | 1 | 5,8 |
| `front-busca/id_renomeado/harness/r3` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,476 | 1 | 5,8 |
| `front-busca/id_renomeado/harness/r4` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,539 | 1 | 5,8 |
| `front-busca/id_renomeado/harness/r5` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,514 | 1 | 5,8 |
| `front-busca/id_renomeado/php/r1` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,562 | 1 | 5,9 |
| `front-busca/id_renomeado/php/r2` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,506 | 1 | 5,8 |
| `front-busca/id_renomeado/php/r3` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,508 | 1 | 5,8 |
| `front-busca/id_renomeado/php/r4` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,489 | 1 | 5,8 |
| `front-busca/id_renomeado/php/r5` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,503 | 1 | 5,8 |
| `front-busca/classe_trocada/harness/r1` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,623 | 1 | 5,9 |
| `front-busca/classe_trocada/harness/r2` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,506 | 1 | 5,8 |
| `front-busca/classe_trocada/harness/r3` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,490 | 1 | 5,8 |
| `front-busca/classe_trocada/harness/r4` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,498 | 1 | 5,8 |
| `front-busca/classe_trocada/harness/r5` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,511 | 1 | 5,8 |
| `front-busca/classe_trocada/php/r1` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,502 | 1 | 5,8 |
| `front-busca/classe_trocada/php/r2` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,511 | 1 | 5,8 |
| `front-busca/classe_trocada/php/r3` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,547 | 1 | 5,8 |
| `front-busca/classe_trocada/php/r4` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,492 | 1 | 5,8 |
| `front-busca/classe_trocada/php/r5` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,522 | 1 | 5,8 |
| `front-busca/texto_alterado/harness/r1` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,536 | 1 | 5,8 |
| `front-busca/texto_alterado/harness/r2` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,517 | 1 | 5,8 |
| `front-busca/texto_alterado/harness/r3` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,479 | 1 | 5,8 |
| `front-busca/texto_alterado/harness/r4` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,461 | 1 | 5,7 |
| `front-busca/texto_alterado/harness/r5` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,520 | 1 | 5,8 |
| `front-busca/texto_alterado/php/r1` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,713 | 1 | 6,0 |
| `front-busca/texto_alterado/php/r2` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,502 | 1 | 5,9 |
| `front-busca/texto_alterado/php/r3` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,483 | 1 | 5,8 |
| `front-busca/texto_alterado/php/r4` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,536 | 1 | 5,8 |
| `front-busca/texto_alterado/php/r5` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,528 | 1 | 5,8 |
| `front-busca/estrutura_alterada/harness/r1` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,583 | 1 | 5,9 |
| `front-busca/estrutura_alterada/harness/r2` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,504 | 1 | 5,8 |
| `front-busca/estrutura_alterada/harness/r3` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,520 | 1 | 5,8 |
| `front-busca/estrutura_alterada/harness/r4` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,498 | 1 | 5,8 |
| `front-busca/estrutura_alterada/harness/r5` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,489 | 1 | 5,8 |
| `front-busca/estrutura_alterada/php/r1` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,499 | 1 | 5,8 |
| `front-busca/estrutura_alterada/php/r2` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,599 | 1 | 5,9 |
| `front-busca/estrutura_alterada/php/r3` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,509 | 1 | 5,8 |
| `front-busca/estrutura_alterada/php/r4` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,511 | 1 | 5,8 |
| `front-busca/estrutura_alterada/php/r5` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,496 | 1 | 5,8 |
| `front-admin-login/id_renomeado/harness/r1` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,402 | 1 | 5,6 |
| `front-admin-login/id_renomeado/harness/r2` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,373 | 1 | 5,6 |
| `front-admin-login/id_renomeado/harness/r3` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,377 | 1 | 5,6 |
| `front-admin-login/id_renomeado/harness/r4` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,396 | 1 | 5,6 |
| `front-admin-login/id_renomeado/harness/r5` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,387 | 1 | 5,6 |
| `front-admin-login/id_renomeado/php/r1` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,365 | 1 | 5,5 |
| `front-admin-login/id_renomeado/php/r2` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,440 | 1 | 5,6 |
| `front-admin-login/id_renomeado/php/r3` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,431 | 1 | 5,6 |
| `front-admin-login/id_renomeado/php/r4` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,442 | 1 | 5,6 |
| `front-admin-login/id_renomeado/php/r5` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,401 | 1 | 5,6 |
| `front-admin-login/classe_trocada/harness/r1` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,388 | 1 | 5,6 |
| `front-admin-login/classe_trocada/harness/r2` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,398 | 1 | 5,6 |
| `front-admin-login/classe_trocada/harness/r3` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,376 | 1 | 5,6 |
| `front-admin-login/classe_trocada/harness/r4` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,399 | 1 | 5,7 |
| `front-admin-login/classe_trocada/harness/r5` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,384 | 1 | 5,6 |
| `front-admin-login/classe_trocada/php/r1` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,414 | 1 | 5,6 |
| `front-admin-login/classe_trocada/php/r2` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,393 | 1 | 5,6 |
| `front-admin-login/classe_trocada/php/r3` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,404 | 1 | 5,6 |
| `front-admin-login/classe_trocada/php/r4` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,390 | 1 | 5,6 |
| `front-admin-login/classe_trocada/php/r5` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,407 | 1 | 5,7 |
| `front-admin-login/texto_alterado/harness/r1` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,355 | 1 | 5,6 |
| `front-admin-login/texto_alterado/harness/r2` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,406 | 1 | 5,6 |
| `front-admin-login/texto_alterado/harness/r3` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,372 | 1 | 5,6 |
| `front-admin-login/texto_alterado/harness/r4` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,407 | 1 | 5,7 |
| `front-admin-login/texto_alterado/harness/r5` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,373 | 1 | 5,6 |
| `front-admin-login/texto_alterado/php/r1` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,405 | 1 | 5,7 |
| `front-admin-login/texto_alterado/php/r2` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,371 | 1 | 5,6 |
| `front-admin-login/texto_alterado/php/r3` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,448 | 1 | 5,7 |
| `front-admin-login/texto_alterado/php/r4` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,391 | 1 | 5,6 |
| `front-admin-login/texto_alterado/php/r5` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,356 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/harness/r1` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,401 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/harness/r2` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,407 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/harness/r3` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,378 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/harness/r4` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,383 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/harness/r5` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,400 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/php/r1` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,370 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/php/r2` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,390 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/php/r3` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,387 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/php/r4` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,433 | 1 | 5,7 |
| `front-admin-login/estrutura_alterada/php/r5` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,403 | 1 | 5,7 |
| `front-admin-produtos/id_renomeado/harness/r1` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,745 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/harness/r2` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,793 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/harness/r3` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,772 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/harness/r4` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,792 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/harness/r5` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,746 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/php/r1` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,776 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/php/r2` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,887 | 1 | 6,4 |
| `front-admin-produtos/id_renomeado/php/r3` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,791 | 1 | 6,4 |
| `front-admin-produtos/id_renomeado/php/r4` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,746 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/php/r5` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,825 | 1 | 6,4 |
| `front-admin-produtos/classe_trocada/harness/r1` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,746 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/harness/r2` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,793 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/harness/r3` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,746 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/harness/r4` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,777 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/harness/r5` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,779 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/php/r1` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,746 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/php/r2` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,776 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/php/r3` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,761 | 1 | 6,2 |
| `front-admin-produtos/classe_trocada/php/r4` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,824 | 1 | 6,4 |
| `front-admin-produtos/classe_trocada/php/r5` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,802 | 1 | 6,4 |
| `front-admin-produtos/texto_alterado/harness/r1` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,747 | 1 | 6,3 |
| `front-admin-produtos/texto_alterado/harness/r2` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,773 | 1 | 6,3 |
| `front-admin-produtos/texto_alterado/harness/r3` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,754 | 1 | 6,3 |
| `front-admin-produtos/texto_alterado/harness/r4` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,775 | 1 | 6,3 |
| `front-admin-produtos/texto_alterado/harness/r5` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,747 | 1 | 6,2 |
| `front-admin-produtos/texto_alterado/php/r1` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,774 | 1 | 6,4 |
| `front-admin-produtos/texto_alterado/php/r2` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,780 | 1 | 6,3 |
| `front-admin-produtos/texto_alterado/php/r3` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,774 | 1 | 6,4 |
| `front-admin-produtos/texto_alterado/php/r4` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,770 | 1 | 6,3 |
| `front-admin-produtos/texto_alterado/php/r5` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,762 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/harness/r1` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,777 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/harness/r2` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,810 | 1 | 6,4 |
| `front-admin-produtos/estrutura_alterada/harness/r3` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,741 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/harness/r4` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,808 | 1 | 6,4 |
| `front-admin-produtos/estrutura_alterada/harness/r5` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,796 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/php/r1` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,755 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/php/r2` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,787 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/php/r3` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,787 | 1 | 6,4 |
| `front-admin-produtos/estrutura_alterada/php/r4` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,754 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/php/r5` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,789 | 1 | 6,3 |
| `front-cliente-reserva/id_renomeado/harness/r1` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,705 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/harness/r2` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,766 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/harness/r3` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,735 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/harness/r4` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,711 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/harness/r5` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,737 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/php/r1` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,671 | 1 | 6,8 |
| `front-cliente-reserva/id_renomeado/php/r2` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,689 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/php/r3` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,730 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/php/r4` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,706 | 1 | 6,8 |
| `front-cliente-reserva/id_renomeado/php/r5` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,686 | 1 | 6,8 |
| `front-cliente-reserva/classe_trocada/harness/r1` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,721 | 1 | 6,8 |
| `front-cliente-reserva/classe_trocada/harness/r2` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,715 | 1 | 6,8 |
| `front-cliente-reserva/classe_trocada/harness/r3` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,754 | 1 | 7,0 |
| `front-cliente-reserva/classe_trocada/harness/r4` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,786 | 1 | 7,0 |
| `front-cliente-reserva/classe_trocada/harness/r5` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,754 | 1 | 6,9 |
| `front-cliente-reserva/classe_trocada/php/r1` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,743 | 1 | 6,8 |
| `front-cliente-reserva/classe_trocada/php/r2` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,707 | 1 | 6,9 |
| `front-cliente-reserva/classe_trocada/php/r3` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,640 | 1 | 6,8 |
| `front-cliente-reserva/classe_trocada/php/r4` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,671 | 1 | 6,8 |
| `front-cliente-reserva/classe_trocada/php/r5` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,714 | 1 | 6,9 |
| `front-cliente-reserva/texto_alterado/harness/r1` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,719 | 1 | 6,8 |
| `front-cliente-reserva/texto_alterado/harness/r2` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,728 | 1 | 6,8 |
| `front-cliente-reserva/texto_alterado/harness/r3` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,886 | 1 | 7,0 |
| `front-cliente-reserva/texto_alterado/harness/r4` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,734 | 1 | 6,9 |
| `front-cliente-reserva/texto_alterado/harness/r5` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,771 | 1 | 6,9 |
| `front-cliente-reserva/texto_alterado/php/r1` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,683 | 1 | 6,8 |
| `front-cliente-reserva/texto_alterado/php/r2` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,774 | 1 | 7,0 |
| `front-cliente-reserva/texto_alterado/php/r3` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,666 | 1 | 6,8 |
| `front-cliente-reserva/texto_alterado/php/r4` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,781 | 1 | 6,9 |
| `front-cliente-reserva/texto_alterado/php/r5` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,708 | 1 | 6,9 |
| `front-cliente-reserva/estrutura_alterada/harness/r1` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,641 | 1 | 6,7 |
| `front-cliente-reserva/estrutura_alterada/harness/r2` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,822 | 1 | 7,0 |
| `front-cliente-reserva/estrutura_alterada/harness/r3` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,674 | 1 | 7,0 |
| `front-cliente-reserva/estrutura_alterada/harness/r4` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,763 | 1 | 6,9 |
| `front-cliente-reserva/estrutura_alterada/harness/r5` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,711 | 1 | 6,9 |
| `front-cliente-reserva/estrutura_alterada/php/r1` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,694 | 1 | 6,8 |
| `front-cliente-reserva/estrutura_alterada/php/r2` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,711 | 1 | 6,8 |
| `front-cliente-reserva/estrutura_alterada/php/r3` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,638 | 1 | 6,8 |
| `front-cliente-reserva/estrutura_alterada/php/r4` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,739 | 1 | 6,9 |
| `front-cliente-reserva/estrutura_alterada/php/r5` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,663 | 1 | 6,7 |
<!-- /tabela:tb_f4_cura_execucoes -->

</details>

## 7. Biblioteca em produção e ciclo de correção (corrida 20, regras R4 e R5)

Os 54 casos de aprendizado (24 lidos da tela e 30 do fixture) foram diagnosticados, e na continuação do mesmo prompt o modelo propôs edições. Acerto do diagnóstico: 37 de 54 (68,5%). Das 92 propostas, 56 caíram no validador da Fase 3, 16 nos filtros em código da decisão 65, 1 foi segurada para revisão humana pela regra dos 40% e 19 entraram no lote. O modelo nunca respondeu `NENHUMA` (0 abstenções).

**Regra R5:** nos 36 inéditos pareados, 75,0% com a cópia curada e 75,0% com o lote, b = 0, c = 0: lote aceito. Aceito quer dizer que não piorou. Nenhum caso mudou de acerto, então o lote também não ajudou nesses casos. A base é a corrida 12, em Ollama 0.34.4, e a reavaliação rodou em 0.40.14: as duas versões têm ponte contra a Fase 3, cada uma dentro do limite, mas o par não rodou na mesma versão.

**O que entrou na produção não é o lote inteiro.** A planilha do lote, com as 19 edições e a que ficou segurada, foi pré-revisada pelo Claude e aprovada pelo Eric sem mudança: 2 Correta, 9 Parcial, 9 Errada. O `--promover` aplicou as que não são Errada (11 mantidas) e levou a produção de `1fca10f1a6f6` a `5fc1e7354553`; o `--espera` tirou do índice os 4 aprendidos que a busca nunca entregou (ficha 32), e a produção ficou em `95af35290860`, com 39 verbetes. Essa biblioteca final não passou pela reavaliação da R5. A corrida 22 a leu nos 36 casos de avaliação, com 31 acertos, o mesmo total da L1 curada na corrida 16 (31 de 36), comparação de totais, sem parear.

**Regra R4 (ciclo de correção, em código):** dos 9 casos com sintoma antes, o harness desligou o modo em 4 e manteve em 5. A marca `corrigido` foi dada a 4, com 4 certas, 0 falsos positivos e 0 perdidas: precisão de 100,0%, revocação de 100,0%. São poucos casos, e o gatilho exige reexecução passando, fio mudado e árvore mudada, o que um modo desligado produz por construção.

**Sonda de 28/09 repetida com recuperação por id:** 7 casos, 6 acertam o diagnóstico, 2 mudaram a proposta e 0 mencionam a correção registrada. Como em 28/09, o modelo não percebe a correção. Por isso a marca é dada em código.

<!-- tabela:tb_f4_biblioteca_resumo -->
| Casos de aprendizado | Da tela | Do fixture | Acertos do diagnóstico | Acerto (%) | Propostas | Aceitas (lote) | Abstenções (NENHUMA) | Para revisão humana | Recusadas pelos filtros do P5 | Recusadas pela Fase 3 | Taxa de rejeição (%) | Casos com verbete pelo id | Inferências | Segundos | Trilha (bytes) | k | Base dos inéditos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 54 | 24 | 30 | 37 | 68,5 | 92 | 19 | 0 | 1 | 16 | 56 | 78,3 | 10 | 158 | 16466,1 | 3347613 | 3 | corrida12 |
<!-- /tabela:tb_f4_biblioteca_resumo -->

<!-- tabela:tb_f4_biblioteca_filtros -->
| Filtro em código (decisão 65) | Propostas barradas ou seguradas |
|---|---|
| `evidencia_obrigatoria` | 6 |
| `atomicidade` | 1 |
| `abstencao_valida` | 0 |
| `fonte_confiavel` | 5 |
| `granularidade` | 0 |
| `peso_por_tipo` | 0 |
| `redundancia` | 3 |
| `proveniencia` | 0 |
| `auditoria_por_etapa` | 0 |
| `conflito_deterministico` | 0 |
| `metricas_por_rodada` | 0 |
| `revisao_humana_amostral` | 0 |
| `regra_dos_40` | 1 |
<!-- /tabela:tb_f4_biblioteca_filtros -->

<!-- tabela:tb_f4_biblioteca_rejeicoes -->
| Quem recusou | Código | Propostas |
|---|---|---|
| validador da Fase 3 | `arquivo_inexistente` | 4 |
| validador da Fase 3 | `duplicada` | 14 |
| validador da Fase 3 | `id_repetido` | 12 |
| validador da Fase 3 | `palavra_chave_invalida` | 15 |
| validador da Fase 3 | `retificacao_sem_trecho` | 1 |
| validador da Fase 3 | `teto_notas_verbete` | 1 |
| validador da Fase 3 | `teto_verbetes_novos` | 3 |
| validador da Fase 3 | `texto_curto` | 2 |
| validador da Fase 3 | `texto_longo` | 2 |
| validador da Fase 3 | `trecho_nao_encontrado` | 2 |
| filtros do P5 | `mensagem_nao_encontrada_no_codigo` | 5 |
| filtros do P5 | `redundante` | 3 |
| filtros do P5 | `sem_evidencia_do_caso` | 6 |
| filtros do P5 | `texto_de_origem_proibida` | 1 |
| filtros do P5 | `texto_nao_atomico` | 1 |
<!-- /tabela:tb_f4_biblioteca_rejeicoes -->

<!-- tabela:tb_f4_biblioteca_lote -->
| Edições no lote | Para revisão humana | Peso somado | Por tipo | Hash do lote | Notas na cópia | Verbetes | Verbetes novos |
|---|---|---|---|---|---|---|---|
| 19 | 1 | 34 | `nota` 10, `novo_verbete` 6, `retificacao` 3 | 9f3154eee72d | 22 | 46 | 10 |
<!-- /tabela:tb_f4_biblioteca_lote -->

<!-- tabela:tb_f4_biblioteca_reavaliacao -->
| Inéditos pareados | Acerto com a cópia curada (%) | Acerto com o lote (%) | b (passaram a acertar) | c (passaram a errar) | p (McNemar exato) | Veredito R5 | Casos que mudaram | Base |
|---|---|---|---|---|---|---|---|---|
| 36 | 75,0 | 75,0 | 0 | 0 | 1,000 | aceito | nenhum | pre_fase4_confianca (corrida 12, cópia curada 1fca10f1a6f6, Ollama 0.34.4) |
<!-- /tabela:tb_f4_biblioteca_reavaliacao -->

<!-- tabela:tb_f4_biblioteca_correcao -->
| Casos com sintoma antes | Modo desligado | Modo mantido | Marcados corrigido | Certos | Falsos positivos | Perdidos | Precisão (%) | Revocação (%) | Kappa | Sem sintoma antes |
|---|---|---|---|---|---|---|---|---|---|---|
| 9 | 4 | 5 | 4 | 4 | 0 | 0 | 100,0 | 100,0 | 1,000 | `sin-15` |
<!-- /tabela:tb_f4_biblioteca_correcao -->

<details><summary>Ciclo de correção, caso a caso (tb_f4_biblioteca_correcao_casos)</summary>

<!-- tabela:tb_f4_biblioteca_correcao_casos -->
| Caso | Modo | Verbetes | Modo desligado | Reproduziu antes | Passou depois | Fio mudou | Árvore mudou | Marcado | Motivo |
|---|---|---|---|---|---|---|---|---|---|
| `lex-2` | `corpo_nao_e_json` | `corpo_nao_e_json` | não | sim | não | não | não | não | a reexecução ainda falha: nada a marcar |
| `lex-9` | `corpo_nao_e_json` | `corpo_nao_e_json` | sim | sim | sim | sim | sim | sim | o roteiro passou e o fio e a árvore mudaram entre a corrida que falhava e a que passou |
| `run-7` | `recurso_inexistente` | `recurso_inexistente` | sim | sim | sim | sim | sim | sim | o roteiro passou e o fio e a árvore mudaram entre a corrida que falhava e a que passou |
| `semt-13` | `type_drift` | `entidade-produto` | não | sim | sim | não | não | não | o roteiro passou, mas nada mudou no fio (corpo e tempo da chamada iguais): sem evidência de correção |
| `sin-1` | `field_missing` | `campo_ausente` | não | sim | não | não | não | não | a reexecução ainda falha: nada a marcar |
| `sin-13` | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | sim | sim | sim | sim | sim | sim | o roteiro passou e o fio e a árvore mudaram entre a corrida que falhava e a que passou |
| `sin-15` | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | sim | não | sim | não | não | não | o roteiro passou, mas nada mudou no fio (corpo e tempo da chamada iguais): sem evidência de correção |
| `sin-9` | `field_renamed` | `campo_renomeado` | sim | sim | sim | sim | sim | sim | o roteiro passou e o fio e a árvore mudaram entre a corrida que falhava e a que passou |
| `tra-12` | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | não | sim | sim | não | não | não | o roteiro passou, mas nada mudou no fio (corpo e tempo da chamada iguais): sem evidência de correção |
| `tra-3` | `chave_de_juncao_errada` | `chave_de_juncao_errada` | não | sim | sim | não | não | não | o roteiro passou, mas nada mudou no fio (corpo e tempo da chamada iguais): sem evidência de correção |
<!-- /tabela:tb_f4_biblioteca_correcao_casos -->

</details>

<!-- tabela:tb_f4_biblioteca_sonda -->
| Caso | Rótulo agora | Acertou | Propostas | Aceitas | NENHUMA | Motivos de recusa | Menciona a correção | Verbetes pelo id | Rótulo em 28/09 | Propostas em 28/09 | Aceitas em 28/09 | Mudou a proposta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `efe-3` | campo_ausente | sim | 2 | 1 | não | `duplicada` | não | nenhum | campo_ausente | 2 | 0 | sim |
| `lex-9` | corpo_nao_e_json | sim | 2 | 2 | não | nenhum | não | nenhum | não medido | não medido | não medido | sem sonda anterior |
| `sin-9` | campo_renomeado | sim | 2 | 0 | não | `bloco_malformado`, `bloco_malformado` | não | nenhum | não medido | não medido | não medido | sem sonda anterior |
| `sin-13` | estrutura_aninhada_divergente | sim | 2 | 0 | não | `duplicada`, `duplicada` | não | nenhum | não medido | não medido | não medido | sem sonda anterior |
| `sin-15` | colecao_no_lugar_de_objeto | sim | 2 | 1 | não | `trecho_nao_encontrado` | não | nenhum | não medido | não medido | não medido | sem sonda anterior |
| `run-7` | recurso_inexistente | sim | 2 | 0 | não | `palavra_chave_invalida`, `palavra_chave_invalida` | não | nenhum | não medido | não medido | não medido | sem sonda anterior |
| `efe-10` | dado_desatualizado | não | 2 | 0 | não | `duplicada`, `duplicada` | não | `interface-frontend` | dado_desatualizado | 2 | 1 | sim |
<!-- /tabela:tb_f4_biblioteca_sonda -->

<!-- tabela:tb_f4_biblioteca_revisao -->
| Verbete | Operação | Caso | Peso | Parcela na calibração (%) |
|---|---|---|---|---|
| `contrato-produto` | nota | `efe-4` | 1 | 42,2 |
<!-- /tabela:tb_f4_biblioteca_revisao -->

<!-- tabela:tb_f4_biblioteca_recuperacao -->
| Verbete aprendido | Vezes na calibração (k = 3) | Vezes pelo id nesta corrida |
|---|---|---|
| `atualizacao_imediata` | 0 | 1 |
| `interface-estados` | 0 | 1 |
| `interface-frontend` | 0 | 1 |
| `rotas-inexistentes` | 0 | 1 |
<!-- /tabela:tb_f4_biblioteca_recuperacao -->

<details><summary>Os casos de aprendizado (tb_f4_biblioteca_casos)</summary>

<!-- tabela:tb_f4_biblioteca_casos -->
| Caso | Origem | Rótulo | Acertou | Selo | Propostas | Aceitas | Para revisão | Recusadas | NENHUMA | Pelo id | Verbetes editados | Segundos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-2` | tela | corpo_nao_e_json | sim | alto | 1 | 0 | 0 | `mensagem_nao_encontrada_no_codigo` | não |  |  | 229,7 |
| `lex-3` | tela | corpo_vazio | sim | medio | 2 | 0 | 0 | `duplicada`, `id_repetido` | não |  |  | 281,4 |
| `lex-5` | fixture | resposta_truncada | sim | alto | 2 | 0 | 0 | `sem_evidencia_do_caso`, `id_repetido` | não |  |  | 243,6 |
| `sin-1` | tela | campo_ausente | sim | alto | 2 | 1 | 0 | `texto_nao_atomico` | não |  | `campo_preco_ausente` | 251,7 |
| `sin-2` | tela | campo_renomeado | sim | medio | 2 | 0 | 0 | `mensagem_nao_encontrada_no_codigo`, `mensagem_nao_encontrada_no_codigo` | não |  |  | 262,5 |
| `sin-3` | tela | tipo_divergente | não | medio | 2 | 0 | 0 | `duplicada`, `duplicada` | não |  |  | 276,5 |
| `semt-2` | tela | tipo_divergente | sim | alto | 2 | 0 | 0 | `texto_curto`, `arquivo_inexistente` | não |  |  | 266,7 |
| `semt-4` | fixture | formato_de_data_divergente | sim | alto | 2 | 0 | 0 | `palavra_chave_invalida`, `palavra_chave_invalida` | não |  |  | 234,9 |
| `tra-2` | fixture | nome_nulo_vindo_da_view | não | medio | 1 | 0 | 0 | `arquivo_inexistente` | não |  |  | 213,8 |
| `tra-3` | tela | tipo_divergente | não | baixo | 2 | 1 | 0 | `duplicada` | não | `chave_de_juncao_errada` | `novo_verbete` | 318,3 |
| `tra-5` | fixture | contagem_inconsistente | não | baixo | 2 | 1 | 0 | `duplicada` | não |  | `pessoas_incorretas` | 232,6 |
| `run-3` | tela | limite_de_requisicoes | sim | alto | 2 | 1 | 0 | `texto_de_origem_proibida` | não |  | `limite_de_requisicoes` | 277,4 |
| `run-5` | fixture | registro_duplicado | sim | alto | 2 | 1 | 0 | `id_repetido` | não |  | `contrato-pedido` | 234,7 |
| `efe-4` | fixture | colecao_no_lugar_de_objeto | não | baixo | 2 | 1 | 1 |  | não | `interface-estados` | `estado_da_tela_divergente` | 234,3 |
| `lex-6` | fixture | recurso_inexistente | não | baixo | 1 | 0 | 0 | `palavra_chave_invalida` | não |  |  | 203,9 |
| `lex-9` | tela | corpo_nao_e_json | sim | medio | 1 | 0 | 0 | `mensagem_nao_encontrada_no_codigo` | não |  |  | 142,2 |
| `lex-12` | tela | corpo_nao_e_json | sim | medio | 1 | 0 | 0 | `arquivo_inexistente` | não |  |  | 149,6 |
| `sin-6` | tela | campo_ausente | sim | alto | 2 | 0 | 0 | `palavra_chave_invalida`, `id_repetido` | não |  |  | 246,6 |
| `sin-8` | fixture | colecao_no_lugar_de_objeto | sim | medio | 2 | 0 | 0 | `duplicada`, `duplicada` | não |  |  | 235,3 |
| `sin-9` | tela | campo_renomeado | sim | alto | 2 | 0 | 0 | `sem_evidencia_do_caso`, `id_repetido` | não | `campo_renomeado` |  | 243,8 |
| `sin-12` | fixture | colecao_no_lugar_de_objeto | não | baixo | 2 | 0 | 0 | `texto_curto`, `id_repetido` | não |  |  | 218,5 |
| `sin-13` | tela | tipo_divergente | não | medio | 1 | 0 | 0 | `duplicada` | não | `estrutura_aninhada_divergente` |  | 270,3 |
| `sin-15` | fixture | colecao_no_lugar_de_objeto | sim | medio | 2 | 1 | 0 | `redundante` | não |  | `colecao_no_lugar_de_objeto` | 186,8 |
| `semt-6` | tela | contagem_inconsistente | não | medio | 2 | 1 | 0 | `palavra_chave_invalida` | não |  | `tipo_divergente` | 257,9 |
| `semt-7` | fixture | formato_de_data_divergente | não | baixo | 2 | 1 | 0 | `id_repetido` | não |  | `tipo_divergente` | 201,4 |
| `semt-10` | tela | tipo_divergente | sim | alto | 2 | 1 | 0 | `sem_evidencia_do_caso` | não |  | `tipo_divergente` | 188,8 |
| `semt-11` | fixture | valor_fora_do_dominio | sim | medio | 1 | 0 | 0 | `arquivo_inexistente` | não |  |  | 193,6 |
| `semt-12` | fixture | formato_de_data_divergente | sim | medio | 1 | 0 | 0 | `palavra_chave_invalida` | não |  |  | 161,5 |
| `semt-13` | tela | tipo_divergente | sim | alto | 1 | 0 | 0 | `teto_notas_verbete` | não | `entidade-produto` |  | 214,9 |
| `semt-15` | fixture | valor_fora_do_dominio | sim | baixo | 2 | 1 | 0 | `duplicada` | não |  | `validacao-na-api` | 221,5 |
| `tra-6` | tela | escala_ou_unidade_errada | sim | baixo | 2 | 1 | 0 | `duplicada` | não |  | `formato_preco` | 285,8 |
| `tra-7` | tela | campo_renomeado | não | medio | 2 | 0 | 0 | `duplicada`, `id_repetido` | não |  |  | 297,9 |
| `tra-9` | fixture | formato_de_data_divergente | não | medio | 2 | 0 | 0 | `palavra_chave_invalida`, `palavra_chave_invalida` | não |  |  | 238,0 |
| `tra-12` | tela | escala_ou_unidade_errada | sim | medio | 2 | 0 | 0 | `duplicada`, `trecho_nao_encontrado` | não | `escala_ou_unidade_errada` |  | 325,2 |
| `tra-13` | tela | imagem_fora_do_dominio | não | baixo | 1 | 0 | 0 | `redundante` | não |  |  | 230,6 |
| `tra-14` | tela | contagem_inconsistente | sim | medio | 2 | 1 | 0 | `palavra_chave_invalida` | não |  | `contagem_inconsistente` | 233,6 |
| `run-6` | fixture | erro_interno_do_servidor | sim | medio | 1 | 0 | 0 | `texto_longo` | não |  |  | 203,8 |
| `run-7` | tela | recurso_inexistente | sim | alto | 1 | 0 | 0 | `palavra_chave_invalida` | não | `recurso_inexistente` |  | 234,6 |
| `run-8` | fixture | recurso_inexistente | sim | medio | 2 | 0 | 0 | `palavra_chave_invalida`, `id_repetido` | não | `rotas-inexistentes` |  | 225,6 |
| `run-11` | fixture | valor_fora_do_dominio | não | medio | 1 | 0 | 0 | `sem_evidencia_do_caso` | não |  |  | 185,6 |
| `run-12` | fixture | erro_interno_do_servidor | sim | medio | 2 | 1 | 0 | `duplicada` | não |  | `erro_interno_do_servidor` | 237,5 |
| `run-14` | fixture | dado_desatualizado | sim | alto | 1 | 0 | 0 | `palavra_chave_invalida` | não |  |  | 179,9 |
| `run-15` | tela | tempo_de_resposta_excedido | sim | medio | 1 | 0 | 0 | `sem_evidencia_do_caso` | não |  |  | 221,8 |
| `efe-6` | fixture | localizador_quebrado | sim | medio | 2 | 0 | 0 | `palavra_chave_invalida`, `id_repetido` | não |  |  | 239,7 |
| `efe-8` | fixture | estado_da_tela_divergente | sim | medio | 2 | 2 | 0 |  | não |  | `estado_da_tela_divergente`, `atualizacao-da-tela` | 224,3 |
| `efe-9` | fixture | localizador_quebrado | sim | alto | 2 | 0 | 0 | `palavra_chave_invalida`, `palavra_chave_invalida` | não |  |  | 227,0 |
| `efe-10` | fixture | valor_fora_do_dominio | não | baixo | 2 | 1 | 0 | `trecho_nao_encontrado` | não | `interface-frontend` | `interface-frontend` | 236,3 |
| `efe-11` | fixture | localizador_quebrado | não | baixo | 2 | 1 | 0 | `teto_verbetes_novos` | não |  | `localizador_quebrado` | 221,8 |
| `efe-12` | fixture | localizador_quebrado | sim | alto | 2 | 0 | 0 | `redundante`, `texto_longo` | não |  |  | 266,7 |
| `efe-13` | fixture | dado_desatualizado | não | medio | 2 | 1 | 0 | `teto_verbetes_novos` | não | `atualizacao_imediata` | `estado_da_tela_divergente` | 217,7 |
| `efe-15` | fixture | estado_da_tela_divergente | sim | alto | 2 | 0 | 0 | `id_repetido`, `sem_evidencia_do_caso` | não |  |  | 225,3 |
| `lex-13` | fixture | corpo_vazio | sim | alto | 1 | 0 | 0 | `id_repetido` | não |  |  | 183,2 |
| `lex-14` | fixture | resposta_truncada | sim | alto | 2 | 0 | 0 | `duplicada`, `teto_verbetes_novos` | não |  |  | 226,3 |
| `lex-15` | tela | corpo_nao_e_json | sim | medio | 2 | 0 | 0 | `mensagem_nao_encontrada_no_codigo`, `retificacao_sem_trecho` | não |  |  | 196,6 |
<!-- /tabela:tb_f4_biblioteca_casos -->

</details>

### 7.1 Os 36 inéditos da ficha 27, em texto (corrida 24)

<!-- ! Alteração de IA - Revisar: (06/11/2026, decisões 92 e 100) subseção nova com a leitura da corrida 24, e os blocos `tb_f4_ineditos_*`.
     ! Motivo: é a única medida da biblioteca final em casos que ela nunca viu, e o número vai para o TCC. Números de `ineditos.json`, `conferencia_ineditos.json`, `calibracao.json` e `analise_fase3b.json`, lidos por script. -->
A biblioteca de produção (`95af35290860`) leu em texto os 36 inéditos da ficha 27, escritos por um agente que só leu o código das cobaias e conferidos pelo Eric antes da corrida (ficha 46, decisão 100), com k = 3 e o prompt congelado. Rodou em 06/11/2026, de 13:52 a 14:35 (executor 2610 s), com 8,8 GB livres, no Ollama 0.40.14.

**O resultado** (`ineditos.json`): 25 de 36 (69,4%; Wilson 95% de 53,1 a 82,0), com acurácia balanceada de 71,4%. Nos 36 casos de avaliação, com a mesma biblioteca, foram 31 de 36 (corrida 22). Não são os mesmos casos, e os autores são outros, então não há comparação caso a caso, e a diferença não mede só a biblioteca. O número fica perto do que a Fase 3-B mediu em outros 36 inéditos: 26 de 36 com a primeira biblioteca do mesmo modelo.

**O verbete certo pesa de novo** (bloco `tb_f4_ineditos_verbete`): com ele no contexto, 18 de 20; sem ele, 7 de 16. Em texto ele chega em 20 dos 36 casos, porque os sinais da busca (decisão 97) só existem na tela, e 9 dos 11 erros são de casos sem ele.

**Onde erra** (blocos `tb_f4_ineditos_classe` e `tb_f4_ineditos_nivel`): a tradução faz 1 de 6, e as outras classes ficam de 4 a 6 de 6. O nível 3, feito para enganar, faz 5 de 12, contra 9 de 12 no nível 1 e 11 de 12 no nível 2. As respostas erradas mais comuns são `tipo_divergente` (3), `colecao_no_lugar_de_objeto` (3), `resposta_truncada` (2). Dos 10 casos que a pré-análise apontou, 5 erram (`semt-27`, `tra-27`, `run-26`, `efe-26` e `efe-27`); dos outros 26, 6.

**A repetição bate** (bloco `tb_f4_ineditos_18e`): os 25 casos que a corrida 18e também leu em texto deram o mesmo rótulo em 25, com o mesmo prompt, a mesma versão do Ollama e a mesma biblioteca. Lidos da tela, os mesmos casos fazem 22, contra 18 em texto: é o efeito dos sinais da busca, e só nos casos que têm tela. Os outros 11, sem tela, fazem 7.

**O selo** (bloco `tb_f4_ineditos_selo`): o alto acerta 12 de 13, o médio 9 de 15 e o baixo 4 de 8, com os limiares da corrida 16; na calibração eram 34 de 37, 22 de 26 e 12 de 27. O único erro com selo alto é `tra-25`, e o selo médio perde mais aqui que na calibração. Continua sendo triagem, não barreira.

**O que esta corrida não diz:** há uma condição só, a biblioteca final, então ela não diz quanto a biblioteca ajuda nestes casos, porque eles não foram lidos sem biblioteca. E valem as ressalvas da conferência (decisão 100, seção 12).

<!-- tabela:tb_f4_ineditos_resumo -->
| Casos | Acertos | Acerto (%) | Wilson 95% | Acurácia balanceada (%) | Verbete certo no contexto | Fora do conjunto ou sem rótulo | Tokens de entrada (mediana) | Segundos (mediana) | Os 36 oficiais, com a mesma biblioteca (corrida 22) |
|---|---|---|---|---|---|---|---|---|---|
| 36 | 25 | 69,4 | 53,1 a 82,0 | 71,4 | 20 | 0 | 1247,5 | 68,38 | 31 de 36 (86,1%) |
<!-- /tabela:tb_f4_ineditos_resumo -->

<!-- tabela:tb_f4_ineditos_verbete -->
| Verbete da causa certa entre os entregues | Casos | Acertos | Acerto (%) |
|---|---|---|---|
| sim | 20 | 18 | 90,0 |
| não | 16 | 7 | 43,8 |
<!-- /tabela:tb_f4_ineditos_verbete -->

<!-- tabela:tb_f4_ineditos_classe -->
| Classe | Casos | Acertos | Erros |
|---|---|---|---|
| 1 | 6 | 6 | 0 |
| 2 | 6 | 5 | 1 |
| 3 | 6 | 4 | 2 |
| 4 | 6 | 1 | 5 |
| 5 | 6 | 5 | 1 |
| 6 | 6 | 4 | 2 |
<!-- /tabela:tb_f4_ineditos_classe -->

<!-- tabela:tb_f4_ineditos_nivel -->
| Nível | Casos | Acertos | Erros |
|---|---|---|---|
| 1 | 12 | 9 | 3 |
| 2 | 12 | 11 | 1 |
| 3 | 12 | 5 | 7 |
<!-- /tabela:tb_f4_ineditos_nivel -->

<!-- tabela:tb_f4_ineditos_selo -->
| Selo | Casos | Acertos | Erros |
|---|---|---|---|
| alto | 13 | 12 | 1 |
| baixo | 8 | 4 | 4 |
| medio | 15 | 9 | 6 |
<!-- /tabela:tb_f4_ineditos_selo -->

<!-- tabela:tb_f4_ineditos_18e -->
| Casos também lidos na corrida 18e | Mesmo rótulo do caso escrito da 18e | Acertos aqui | Acertos no caso escrito da 18e | Acertos na tela da 18e |
|---|---|---|---|---|
| 25 | 25 | 18 | 18 | 22 |
<!-- /tabela:tb_f4_ineditos_18e -->

<!-- tabela:tb_f4_ineditos_casos -->
| Caso | Classe | Nível | Gabarito | Rótulo | Certo | Probabilidade | Selo | Verbete certo no contexto |
|---|---|---|---|---|---|---|---|---|
| `lex-22` | 1 | 1 | `corpo_nao_e_json` | `corpo_nao_e_json` | sim | 0,920 | medio | sim |
| `lex-23` | 1 | 1 | `corpo_vazio` | `corpo_vazio` | sim | 0,987 | medio | sim |
| `lex-24` | 1 | 2 | `codificacao_incorreta` | `codificacao_incorreta` | sim | 0,999 | alto | não |
| `lex-25` | 1 | 2 | `codificacao_incorreta` | `codificacao_incorreta` | sim | 0,998 | alto | não |
| `lex-26` | 1 | 3 | `codificacao_incorreta` | `codificacao_incorreta` | sim | 1,000 | alto | não |
| `lex-27` | 1 | 3 | `codificacao_incorreta` | `codificacao_incorreta` | sim | 0,742 | baixo | não |
| `sin-22` | 2 | 1 | `campo_ausente` | `campo_ausente` | sim | 0,944 | medio | sim |
| `sin-23` | 2 | 1 | `campo_renomeado` | `campo_renomeado` | sim | 0,999 | alto | sim |
| `sin-24` | 2 | 2 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | sim | 0,797 | baixo | sim |
| `sin-25` | 2 | 2 | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | sim | 0,994 | alto | sim |
| `sin-26` | 2 | 3 | `campo_ausente` | `resposta_truncada` | não | 0,950 | medio | sim |
| `sin-27` | 2 | 3 | `campo_renomeado` | `campo_renomeado` | sim | 0,413 | baixo | não |
| `semt-22` | 3 | 1 | `nulo_inesperado` | `nulo_inesperado` | sim | 0,999 | alto | sim |
| `semt-23` | 3 | 1 | `valor_fora_do_dominio` | `tipo_divergente` | não | 0,908 | medio | não |
| `semt-24` | 3 | 2 | `tipo_divergente` | `tipo_divergente` | sim | 0,995 | alto | sim |
| `semt-25` | 3 | 2 | `formato_de_data_divergente` | `formato_de_data_divergente` | sim | 0,984 | medio | sim |
| `semt-26` | 3 | 3 | `nulo_inesperado` | `nulo_inesperado` | sim | 0,892 | medio | sim |
| `semt-27` | 3 | 3 | `valor_fora_do_dominio` | `colecao_no_lugar_de_objeto` | não | 0,645 | baixo | não |
| `tra-22` | 4 | 1 | `escala_ou_unidade_errada` | `tipo_divergente` | não | 0,811 | baixo | não |
| `tra-23` | 4 | 1 | `escala_ou_unidade_errada` | `valor_fora_do_dominio` | não | 0,649 | baixo | não |
| `tra-24` | 4 | 2 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | sim | 0,915 | medio | sim |
| `tra-25` | 4 | 2 | `contagem_inconsistente` | `resposta_truncada` | não | 0,997 | alto | sim |
| `tra-26` | 4 | 3 | `chave_de_juncao_errada` | `colecao_no_lugar_de_objeto` | não | 0,915 | medio | não |
| `tra-27` | 4 | 3 | `escala_ou_unidade_errada` | `tipo_divergente` | não | 0,958 | medio | não |
| `run-22` | 5 | 1 | `limite_de_requisicoes` | `limite_de_requisicoes` | sim | 0,640 | baixo | sim |
| `run-23` | 5 | 1 | `recurso_inexistente` | `recurso_inexistente` | sim | 0,996 | alto | sim |
| `run-24` | 5 | 2 | `registro_duplicado` | `registro_duplicado` | sim | 0,970 | medio | não |
| `run-25` | 5 | 2 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | sim | 0,832 | medio | não |
| `run-26` | 5 | 3 | `dado_desatualizado` | `registro_duplicado` | não | 0,757 | baixo | não |
| `run-27` | 5 | 3 | `registro_duplicado` | `registro_duplicado` | sim | 1,000 | alto | sim |
| `efe-22` | 6 | 1 | `localizador_quebrado` | `localizador_quebrado` | sim | 0,990 | alto | sim |
| `efe-23` | 6 | 1 | `localizador_quebrado` | `localizador_quebrado` | sim | 1,000 | alto | sim |
| `efe-24` | 6 | 2 | `localizador_quebrado` | `localizador_quebrado` | sim | 0,998 | alto | sim |
| `efe-25` | 6 | 2 | `localizador_quebrado` | `localizador_quebrado` | sim | 0,959 | medio | sim |
| `efe-26` | 6 | 3 | `estado_da_tela_divergente` | `colecao_no_lugar_de_objeto` | não | 0,906 | medio | não |
| `efe-27` | 6 | 3 | `estado_da_tela_divergente` | `dado_desatualizado` | não | 0,875 | medio | não |
<!-- /tabela:tb_f4_ineditos_casos -->

## 8. Os dez cenários da Fase 5 (corridas 21, 21b, 21c e 21d)

O agente inteiro nos dez cenários da ficha 36, seis de contrato e quatro de localizador, com uma repetição. No contrato (ficha 35), o MTTR vai da detecção ao diagnóstico conferido em código, e o Task Success é a causa e o campo certos. No localizador, o MTTR vai da detecção à reexecução validada, e o Task Success é o roteiro concluído sem erro depois da cura. Os dois MTTR não medem a mesma coisa, e nenhum deles tem linha de base ainda. Os blocos abaixo são os da corrida 21d, a leitura vigente (`cenarios_v4.json`); a 21c fica como a medida do corte (`cenarios_v3.json`), a 21b como a de antes dele (`cenarios_v2.json`), e a 21, como o registro de como o defeito da cura apareceu (`cenarios.json`).

**Corrida 21:** 9 de 10 (Wilson 95% de 59,6 a 98,2%), MTTR médio de 101,1 s nas 9 execuções que chegaram ao fim do cronômetro. O login ficou sem cura (`candidato_invalido`): `admin/login.php` tem um recarregamento automático de 30 s, e os candidatos eram verificados na página da detecção, parada enquanto o modelo pensava. A corrida 19 não via isso porque não tinha modelo no meio. O conserto (`Cura._refazer_ate_o_passo`) verifica os candidatos numa página refeita até o passo que falhou, e o tempo de refazer entra no MTTR.

**Corrida 21b:** 10 de 10 (Wilson 95% de 72,2 a 100,0%), MTTR médio de 105,2 s (reamostragem 95% de 90,6 a 118,0; mediana 114,3 s). Contrato: 6 de 6, MTTR médio de 114,7 s. Localizador: 4 de 4, MTTR médio de 90,8 s. Entre as duas corridas, o rótulo se repetiu em 10 de 10 cenários e a resposta inteira em 4 de 10: com temperatura 0,1 o texto varia sem mudar a causa.

<!-- ! Alteração de IA - Revisar: (05/11/2026, decisão 90) parágrafo novo com a leitura da corrida 21c, que passa a ser a vigente.
     ! Motivo: a decisão 90 diz que a leitura nova passa a valer quando a corrida rodar, e a 21c mede o efeito do corte: da 21b para ela só mudou o tamanho do prompt. Números de `resultados_alvo/fase4/tela_v3.json`, `cenarios_v3.json` e `experimento_prompt.json`, lidos por script. -->
**Corrida 21c:** 10 de 10 (Wilson 95% de 72,2 a 100,0%), MTTR médio de 72,5 s (reamostragem 95% de 63,9 a 80,0; mediana 72,6 s), contra 105,2 s na 21b: 31% a menos. Contrato: 6 de 6, MTTR médio de 79,9 s (era 114,7 s). Localizador: 4 de 4, MTTR médio de 61,5 s (era 90,8 s). Da 21b para a 21c só mudou o tamanho do prompt: mesma versão do Ollama, mesma biblioteca, e o rótulo igual em 10 de 10 cenários. Os prompts foram de 1107 a 1340 tokens, nenhum acima do limite; na 21b, 9 de 10 passavam, o maior com 1950. O diagnóstico levou de 39,5 a 87,5 s, e a leitura do prompt é a mediana de 78,8% do tempo dele. A estimativa da Fase 5, dez cenários com cinco repetições, cai para 1,05 h de máquina.

<!-- ! Alteração de IA - Revisar: (06/11/2026, decisão 97) parágrafo novo com a leitura da corrida 21d, que passa a ser a vigente.
     ! Motivo: da 21c para a 21d só mudou a busca, e a corrida diz se os sinais mexeram nos dez cenários da Fase 5. Números de `cenarios_v3.json` e `cenarios_v4.json`, lidos por script. -->
**Corrida 21d, a vigente:** 10 de 10 (Wilson 95% de 72,2 a 100,0%), MTTR médio de 74,0 s (reamostragem 95% de 64,9 a 81,8; mediana 73,3 s), contra 72,5 s na 21c: dentro da margem. Contrato: 6 de 6, MTTR médio de 81,5 s. Localizador: 4 de 4, MTTR médio de 62,7 s. Da 21c para a 21d só mudou a busca, e o rótulo foi igual em 10 de 10 cenários: os sinais não mexeram nos dez cenários. O maior prompt tem 1385 tokens, nenhum acima do limite. A estimativa da Fase 5 fica em 1,07 h de máquina.

**O que domina o tempo é o modelo.** Na 21b, o diagnóstico levou de 61,0 a 133,4 s, e descontado ele sobram de 2,0 a 3,6 s. Dentro do diagnóstico, a mediana de 83,1% do tempo é a leitura do prompt (`prefill_ms` sobre `total_ms`), o que amarra o MTTR ao tamanho do prompt: os tokens de entrada vão de 1219 a 1950 (ficha 42, decisão 90). A estimativa da Fase 5 era de 1,5 h de máquina nessa corrida.

<!-- tabela:tb_f4_cenarios_resumo -->
| Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Detectadas | Com MTTR | MTTR médio (s) | Reamostragem 95% (s) | MTTR mediano (s) | Navegador | Banco no começo das repetições |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 10 | 100,0 | 72,2 a 100,0 | 10 | 10 | 74,0 | 64,9 a 81,8 | 73,3 | 156.0.8078.4 | o mesmo hash em todas: 9fe5e7cb64288c9d |
<!-- /tabela:tb_f4_cenarios_resumo -->

<!-- tabela:tb_f4_cenarios_por_tipo -->
| Tipo | Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Detectadas | Com MTTR | MTTR médio (s) | Reamostragem 95% (s) | MTTR mediano (s) |
|---|---|---|---|---|---|---|---|---|---|
| contrato | 6 | 6 | 100,0 | 61,0 a 100,0 | 6 | 6 | 81,5 | 75,2 a 88,5 | 79,2 |
| localizador | 4 | 4 | 100,0 | 51,0 a 100,0 | 4 | 4 | 62,7 | 48,9 a 71,6 | 67,6 |
<!-- /tabela:tb_f4_cenarios_por_tipo -->

<!-- tabela:tb_f4_cenarios_tempo -->
| Execuções | Segundos por execução (média) | Segundos no total | Estimativa da Fase 5 (10 cenários x 5 repetições, h) | Detecção pela conferência do roteiro | Detecção pelo fio (regra R1) | Detecção pelo passo do localizador |
|---|---|---|---|---|---|---|
| 10 | 76,7 | 767,2 | 1,1 | 4 | 2 | 4 |
<!-- /tabela:tb_f4_cenarios_tempo -->

<!-- tabela:tb_f4_cenarios_sem_sucesso -->
| Cenário | Repetição | Tipo | Detectou | Rótulo do diagnóstico | Causa esperada | Falha da cura | Segundos |
|---|---|---|---|---|---|---|---|
| nenhuma |  |  |  |  |  |  |  |
<!-- /tabela:tb_f4_cenarios_sem_sucesso -->

<details><summary>Cenário a cenário, com o que a detecção acusou (tb_f4_cenarios_por_cenario)</summary>

<!-- tabela:tb_f4_cenarios_por_cenario -->
| Cenário | Tipo | Modo | Classe | Causa esperada | Execuções | Task Success | MTTR médio (s) | MTTR mediano (s) | Rótulos do diagnóstico | Segundos por execução | O que a detecção acusou |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | `malformed_json` | 1 | `resposta_truncada` | 1 | 1 | 92,7 | 92,7 | `resposta_truncada` 1 | 93,0 | a conferência "grid com 14 cartões" (passo 3) falhou: esperado 14 elementos, observado 0 elementos |
| `contrato-field_missing` | contrato | `field_missing` | 2 | `campo_ausente` | 1 | 1 | 73,3 | 73,3 | `campo_ausente` 1 | 73,7 | a conferência "preço do primeiro cartão" (passo 4) falhou: esperado texto no padrão ^R\$ \d+,\d{2}$, observado undefined |
| `contrato-field_renamed` | contrato | `field_renamed` | 2 | `campo_renomeado` | 1 | 1 | 73,1 | 73,1 | `campo_renomeado` 1 | 73,6 | a conferência "preço do primeiro cartão" (passo 4) falhou: esperado texto no padrão ^R\$ \d+,\d{2}$, observado undefined |
| `contrato-type_drift` | contrato | `type_drift` | 3 | `tipo_divergente` | 1 | 1 | 73,4 | 73,4 | `tipo_divergente` 1 | 73,9 | o roteiro passou na tela, mas o fio acusou: diff do contrato: tipo_diferente; corpo diferente da referência em modo normal |
| `contrato-escala_ou_unidade_errada` | contrato | `escala_ou_unidade_errada` | 4 | `escala_ou_unidade_errada` | 1 | 1 | 91,2 | 91,2 | `escala_ou_unidade_errada` 1 | 91,5 | o roteiro passou na tela, mas o fio acusou: corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `contrato-error_500` | contrato | `error_500` | 5 | `erro_interno_do_servidor` | 1 | 1 | 85,0 | 85,0 | `erro_interno_do_servidor` 1 | 85,3 | a conferência "grid com 14 cartões" (passo 3) falhou: esperado 14 elementos, observado 0 elementos |
| `localizador-front-busca` | localizador | `id_renomeado` | 6 | `localizador_quebrado` | 1 | 1 | 73,3 | 73,3 | `localizador_quebrado` 1 | 79,2 | o passo 2 (esperar #buscar visível) não terminou: TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("#buscar") to be visible |
| `localizador-front-admin-login` | localizador | `classe_trocada` | 6 | `localizador_quebrado` | 1 | 1 | 42,3 | 42,3 | `localizador_quebrado` 1 | 48,0 | o passo 5 (clicar em button.btn-primary) não terminou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.btn-primary") |
| `localizador-front-admin-produtos` | localizador | `texto_alterado` | 6 | `localizador_quebrado` | 1 | 1 | 66,4 | 66,4 | `localizador_quebrado` 1 | 72,8 | o passo 11 (clicar em role=button[name=/EXCLUIR$/] >> nth=0) não terminou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("role=button[name=/EXCLUIR$/]").first |
| `localizador-front-cliente-reserva` | localizador | `estrutura_alterada` | 6 | `localizador_quebrado` | 1 | 1 | 68,8 | 68,8 | `localizador_quebrado` 1 | 76,1 | o passo 11 (clicar em #reserva_login > input[type=submit]) não terminou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("#reserva_login > input[type=submit]") |
<!-- /tabela:tb_f4_cenarios_por_cenario -->

</details>

## 9. Avaliação da própria trilha (corrida 22)

Os 36 casos oficiais de avaliação, lidos do fixture, sem gabarito no agente, com a biblioteca de produção: 31 de 36 certos (86,1%), 5 erros, 277 inferências. A especificação da trilha (seção 12) faz três perguntas, e as tabelas abaixo respondem às duas primeiras; a terceira, com revisor humano, não foi medida (seção 9.5).

### 9.1 A divergência contra os erros reais: as duas contas do carimbo de conflito (decisão 88)

A medida é TPR (a parcela dos erros que o sinal pega) vezes TNR (a parcela dos acertos que ele deixa em paz); um sinal jogado ao acaso dá 0,250. O carimbo de conflito do relatório acende por conferência em código que não confere ou por intervenção que muda o rótulo. Essa regra fica como está (ficha 39), e as duas contas vão juntas:

- **Com as intervenções em todos os casos**, como a corrida 22 rodou por causa da amostra fixa: o sinal `divergencia` pegou 4 dos 5 erros e acusou 20 dos 31 acertos, TPR x TNR de 0,284. Quase não separa erro de acerto, porque as intervenções mudam o rótulo também quando o modelo está certo: a documentação pesar na resposta é o esperado.
- **Por gatilho**, como o agente roda fora da avaliação: o sinal `por_gatilho` pegaria 3 dos 5 erros e acusaria 3 dos 31 acertos, TPR x TNR de 0,542. **Essa contagem sai da corrida 22, que não rodou assim:** as intervenções rodaram nos 36 casos, e a conta só olha onde a probabilidade baixa ou a FONTE divergente (a linha da resposta em que o modelo cita os verbetes que usou) as dispararia. Nenhuma corrida mediu o agente rodando por gatilho nesses casos.

O selo baixo sozinho, sem nenhuma inferência a mais, dá 0,523 (3 dos 5 erros e 4 dos 31 acertos). A opção (b) da ficha 39, contada por gatilho (`regra_b_por_gatilho`), daria 0,561, com 2 alarmes falsos contra 3: tiraria 1 alarme falso, ao custo de mudar a especificação e o molde. Com só 5 erros, nenhuma conta separa as opções: o intervalo de Wilson do TPR vai de 37,6 a 96,4% na divergência e de 23,1 a 88,2% por gatilho.

<!-- tabela:tb_f4_trilha_resumo -->
| Casos | Acertos | Erros | Acerto (%) | TPR da divergência | TNR da divergência | TPR x TNR | Acaso | TPR x TNR só por gatilho | Inferências | Intervenções | Com limite inferior | Repetição manteve o rótulo | FONTE verificada pela remoção | Pós-racionalização (%) | s por caso (média) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 36 | 31 | 5 | 86,1 | 0,800 | 0,355 | 0,284 | 0,250 | 0,542 | 277 | 144 | 7 | 36 de 36 | 13 de 36 | 19,4 | 349,8 |
<!-- /tabela:tb_f4_trilha_resumo -->

<!-- tabela:tb_f4_trilha_sinais -->
| Sinal | O que é | Erros | Acertos | Pegou (VP) | Deixou passar (FN) | Acusou acerto (FP) | Deixou em paz (VN) | TPR | TNR | TPR x TNR | Acaso | TPR, Wilson 95% (%) | TNR, Wilson 95% (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `divergencia` | a divergência registrada no nó de diagnóstico (o declarado difere do medido, ou uma intervenção mudou o rótulo) | 5 | 31 | 4 | 1 | 20 | 11 | 0,800 | 0,355 | 0,284 | 0,250 | 37,6 a 96,4 | 21,1 a 53,1 |
| `por_gatilho` | a divergência como ficaria fora da avaliação: conferência em código que não confere, ou intervenção que mudou o rótulo só onde a probabilidade baixa ou a FONTE divergente a dispararia (contada desta corrida, não rodada assim) | 5 | 31 | 3 | 2 | 3 | 28 | 0,600 | 0,903 | 0,542 | 0,250 | 23,1 a 88,2 | 75,1 a 96,7 |
| `regra_b` | a opção (b) da ficha 39, com as intervenções em todos os casos: conferência em código que não confere, ou remoção ou troca que mudou o rótulo | 5 | 31 | 4 | 1 | 14 | 17 | 0,800 | 0,548 | 0,439 | 0,250 | 37,6 a 96,4 | 37,8 a 70,8 |
| `regra_b_por_gatilho` | a opção (b) da ficha 39 fora da avaliação: conferência em código que não confere, ou remoção ou troca que mudou o rótulo só onde a probabilidade baixa ou a FONTE divergente a dispararia (contada desta corrida, não rodada assim) | 5 | 31 | 3 | 2 | 2 | 29 | 0,600 | 0,935 | 0,561 | 0,250 | 23,1 a 88,2 | 79,3 a 98,2 |
| `remocao_ou_troca` | a remoção do verbete citado ou a troca por um verbete errado mudou o rótulo | 5 | 31 | 4 | 1 | 13 | 18 | 0,800 | 0,581 | 0,465 | 0,250 | 37,6 a 96,4 | 40,8 a 73,6 |
| `sem_documentacao` | a inferência sem documentação mudou o rótulo | 5 | 31 | 3 | 2 | 13 | 18 | 0,600 | 0,581 | 0,348 | 0,250 | 23,1 a 88,2 | 40,8 a 73,6 |
| `repeticao_mudou` | a repetição da inferência de base mudou o rótulo (variação natural) | 5 | 31 | 0 | 5 | 0 | 31 | 0,000 | 1,000 | 0,000 | 0,250 | 0,0 a 43,4 | 89,0 a 100,0 |
| `selo_baixo` | o selo de probabilidade do rótulo é baixo | 5 | 31 | 3 | 2 | 4 | 27 | 0,600 | 0,871 | 0,523 | 0,250 | 23,1 a 88,2 | 71,1 a 94,9 |
| `falha` | uma conferência em código não conferiu (falha da taxonomia no nó) | 5 | 31 | 1 | 4 | 1 | 30 | 0,200 | 0,968 | 0,194 | 0,250 | 3,6 a 62,4 | 83,8 a 99,4 |
| `qualquer` | qualquer um de: conferência em código, remoção ou troca, selo baixo | 5 | 31 | 4 | 1 | 17 | 14 | 0,800 | 0,452 | 0,361 | 0,250 | 37,6 a 96,4 | 29,2 a 62,2 |
<!-- /tabela:tb_f4_trilha_sinais -->

### 9.2 Intervenções, sonda de pós-racionalização e o mesmo prompt duas vezes

A remoção do verbete citado mudou o rótulo em 13 de 36 casos, a troca por um verbete errado em 17 e a inferência sem documentação em 16. Em 7 das 144 intervenções o rótulo original saiu das alternativas devolvidas, e a queda de probabilidade ficou só como limite inferior. Com o mesmo prompt, a repetição da base manteve o rótulo em 36 de 36 e deu resposta idêntica em 16: a variação natural não explica as mudanças das intervenções.

Na sonda, um trecho que afirma a causa respondida é plantado num verbete entregue que a FONTE não citou: 8 de 36 casos passaram a citá-lo, 2 mudaram o rótulo, e a pós-racionalização (citar com o mesmo rótulo) ficou em 7 de 36 (19,4%). O controle, a repetição da base sem nada plantado, dá 2 de 36 (5,6%). Isso mede a consistência da FONTE, não fidelidade ao que o modelo faz por dentro (especificação, seção 5). A FONTE foi verificada pela remoção em 13 de 36 casos; nos outros 23, tirar o verbete citado não mudou o rótulo.

Limitação de desenho: a mutação do verbete e a intervenção de troca montam o mesmo prompt nos 36 casos. Foram inferências sem medida nova sobre o modelo; serviram de segunda medida da variação.

<!-- tabela:tb_f4_trilha_intervencoes -->
| Intervenção | O que é | Rodou em | Mudou o rótulo | Limite inferior | Queda média de p |
|---|---|---|---|---|---|
| `remocao` | o verbete citado sai do contexto (marcador neutro no lugar) | 36 | 13 | 2 | 0,297 |
| `troca` | o verbete citado vira um verbete errado | 36 | 17 | 2 | 0,370 |
| `sem_documentacao` | a inferência sem documentação nenhuma | 36 | 16 | 3 | 0,353 |
| `repeticao_da_base` | a inferência de base repetida | 36 | 0 | 0 | 0,003 |
<!-- /tabela:tb_f4_trilha_intervencoes -->

<!-- tabela:tb_f4_trilha_sonda -->
| Casos | Com verbete não citado (alvo) | Sem alvo | FONTE passou a citar o plantado | Rótulo mudou | Pós-racionalização (cita e mantém o rótulo) | Taxa (%) | Controle: casos com a repetição da base | Controle: a repetição cita o mesmo verbete, sem nada plantado | Controle (%) |
|---|---|---|---|---|---|---|---|---|---|
| 36 | 36 | 0 | 8 | 2 | 7 | 19,4 | 36 | 2 | 5,6 |
<!-- /tabela:tb_f4_trilha_sonda -->

<!-- tabela:tb_f4_trilha_mesmo_prompt -->
| Par de inferências | O que é | Pares | Mesmo prompt | Mesma resposta | Mesma FONTE | Mesmo rótulo |
|---|---|---|---|---|---|---|
| `repeticao_da_base` | a inferência de base e a repetição dela | 36 | 36 | 16 | 33 | 36 |
| `verbete_trocado_e_troca` | a mutação do verbete e a intervenção de troca | 36 | 36 | 12 | 28 | 34 |
<!-- /tabela:tb_f4_trilha_mesmo_prompt -->

### 9.3 Mutações: a trilha aponta o nó certo?

O primeiro nó que divergiu da trilha da base foi o previsto em 36 de 36 no verbete trocado, 17 de 17 no contrato alterado (19 casos sem alvo) e 4 de 4 no seletor quebrado. Os 100% são esperados por construção: os nós `poda` e `recuperacao` saem em código da entrada mutada, e o diff é determinístico. Isso prova que a trilha registra a mudança no nó certo e que nenhum nó anterior muda. O que diz algo sobre o modelo é o rótulo, que mudou em 17, 3 e 0 casos, respectivamente. Na tabela do seletor, o MTTR da mutada é menor que o da dourada, mas não serve para comparar: a mutada roda logo depois da dourada e aproveita o prompt em cache (roadmap §2.15).

<!-- tabela:tb_f4_trilha_mutacoes -->
| Mutação | Nó previsto | Casos | Aplicáveis | Sem alvo | Apontou o nó previsto | Apontou outro nó | Sem divergência | Rótulo mudou | Previsto (%) |
|---|---|---|---|---|---|---|---|---|---|
| `verbete_trocado` | `recuperacao` | 36 | 36 | 0 | 36 | 0 | 0 | 17 | 100,0 |
| `contrato_alterado` | `poda` | 36 | 17 | 19 | 17 | 0 | 0 | 3 | 100,0 |
| `seletor_quebrado` | `cura` | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 100,0 |
<!-- /tabela:tb_f4_trilha_mutacoes -->

<!-- tabela:tb_f4_trilha_seletor -->
| Roteiro | Modo dourado | Modo mutado | Cura dourada | Cura mutada | Rótulo dourado | Rótulo mutado | Primeiro nó divergente | Previsto (cura) | MTTR dourada (s) | MTTR mutada (s) |
|---|---|---|---|---|---|---|---|---|---|---|
| `front-busca` | `id_renomeado` | `id_renomeado+nome_do_alvo` | `papel_e_nome` | `papel_e_nome_parecido` | `localizador_quebrado` | `localizador_quebrado` | `cura` | sim | 86,3 | 61,0 |
| `front-admin-login` | `classe_trocada` | `classe_trocada+nome_do_alvo` | `papel_e_nome` | `papel_e_nome_parecido` | `localizador_quebrado` | `localizador_quebrado` | `cura` | sim | 57,9 | 41,1 |
| `front-admin-produtos` | `texto_alterado` | `texto_alterado+nome_do_alvo` | `papel_e_nome_parecido` | `papel_e_nome_parecido` | `localizador_quebrado` | `localizador_quebrado` | `cura` | sim | 84,0 | 58,5 |
| `front-cliente-reserva` | `estrutura_alterada` | `estrutura_alterada+nome_do_alvo` | `papel_e_nome` | `papel_e_nome_parecido` | `localizador_quebrado` | `localizador_quebrado` | `cura` | sim | 78,6 | 48,9 |
<!-- /tabela:tb_f4_trilha_seletor -->

### 9.4 Caso a caso

<!-- tabela:tb_f4_trilha_amostra -->
| Posição | Caso | Classe | Relatório |
|---|---|---|---|
| 1 | `run-4` | 5 | `relatorios_revisao_trilha/run-4@base.md` |
| 2 | `run-1` | 5 | `relatorios_revisao_trilha/run-1@base.md` |
| 3 | `lex-10` | 1 | `relatorios_revisao_trilha/lex-10@base.md` |
| 4 | `semt-9` | 3 | `relatorios_revisao_trilha/semt-9@base.md` |
| 5 | `tra-15` | 4 | `relatorios_revisao_trilha/tra-15@base.md` |
| 6 | `sin-11` | 2 | `relatorios_revisao_trilha/sin-11@base.md` |
| 7 | `lex-8` | 1 | `relatorios_revisao_trilha/lex-8@base.md` |
| 8 | `efe-1` | 6 | `relatorios_revisao_trilha/efe-1@base.md` |
| 9 | `semt-5` | 3 | `relatorios_revisao_trilha/semt-5@base.md` |
| 10 | `sin-5` | 2 | `relatorios_revisao_trilha/sin-5@base.md` |
| 11 | `sin-14` | 2 | `relatorios_revisao_trilha/sin-14@base.md` |
<!-- /tabela:tb_f4_trilha_amostra -->

<details><summary>Os 36 casos (tb_f4_trilha_casos)</summary>

<!-- tabela:tb_f4_trilha_casos -->
| Caso | Classe | Gabarito | Rótulo | Resultado | p | Selo | Falha | Divergência | Por gatilho | Remoção ou troca | Sem documentação | Intervenções | Limite inferior | Repetição manteve | Sonda | Verbete trocado | Contrato alterado | s no caso |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-1` | 1 | `resposta_truncada` | `resposta_truncada` | certo | 1,000 | alto | não medido | sim | não | sim | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 334,4 |
| `lex-4` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | certo | 1,000 | alto | causa_sem_verbete_que_a_trate | sim | sim | não | não | 4 | 0 | sim | cita o plantado, mesmo rótulo | recuperacao | poda | 361,8 |
| `sin-4` | 2 | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | 0,862 | medio | não medido | sim | não | sim | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 403,5 |
| `sin-5` | 2 | `campo_ausente` | `colecao_no_lugar_de_objeto` | errado | 0,625 | baixo | não medido | sim | sim | sim | sim | 4 | 0 | sim | cita o plantado, mesmo rótulo | recuperacao | poda | 405,0 |
| `semt-1` | 3 | `tipo_divergente` | `tipo_divergente` | certo | 0,929 | medio | não medido | sim | não | sim | não | 4 | 0 | sim | cita o plantado, mesmo rótulo | recuperacao | poda | 377,8 |
| `semt-3` | 3 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | certo | 0,991 | alto | não medido | sim | não | não | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 442,0 |
| `semt-5` | 3 | `nulo_inesperado` | `nulo_inesperado` | certo | 1,000 | alto | não medido | sim | não | não | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 377,5 |
| `tra-1` | 4 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | certo | 0,993 | alto | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 421,9 |
| `tra-4` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,968 | medio | não medido | sim | não | sim | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 375,9 |
| `run-1` | 5 | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | 0,984 | medio | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 341,2 |
| `run-2` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | 1,000 | alto | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 351,6 |
| `run-4` | 5 | `dado_desatualizado` | `dado_desatualizado` | certo | 0,997 | alto | não medido | sim | não | não | sim | 4 | 1 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 361,9 |
| `efe-1` | 6 | `localizador_quebrado` | `tempo_de_resposta_excedido` | errado | 0,902 | medio | não medido | sim | não | sim | não | 4 | 0 | sim | cita o plantado, rótulo mudou | recuperacao | sem alvo | 372,6 |
| `efe-2` | 6 | `estado_da_tela_divergente` | `estado_da_tela_divergente` | certo | 0,718 | baixo | não medido | sim | sim | sim | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 284,9 |
| `efe-3` | 6 | `campo_ausente` | `campo_ausente` | certo | 0,566 | baixo | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, rótulo mudou | recuperacao | poda | 335,0 |
| `efe-5` | 6 | `localizador_quebrado` | `localizador_quebrado` | certo | 0,975 | medio | não medido | sim | não | sim | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 366,6 |
| `lex-7` | 1 | `corpo_vazio` | `corpo_vazio` | certo | 0,999 | alto | não medido | sim | não | sim | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 322,6 |
| `lex-8` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | certo | 0,749 | baixo | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 412,2 |
| `lex-10` | 1 | `resposta_truncada` | `resposta_truncada` | certo | 1,000 | alto | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 309,6 |
| `lex-11` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | certo | 1,000 | alto | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 355,5 |
| `sin-7` | 2 | `campo_ausente` | `campo_ausente` | certo | 0,910 | medio | não medido | sim | não | não | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 404,4 |
| `sin-10` | 2 | `campo_renomeado` | `campo_renomeado` | certo | 0,994 | alto | não medido | sim | não | sim | não | 4 | 0 | sim | cita o plantado, mesmo rótulo | recuperacao | poda | 377,7 |
| `sin-11` | 2 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | 1,000 | alto | não medido | sim | não | sim | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 324,8 |
| `sin-14` | 2 | `campo_renomeado` | `colecao_no_lugar_de_objeto` | errado | 0,301 | baixo | não medido | sim | sim | sim | sim | 4 | 1 | sim | cita o plantado, mesmo rótulo | recuperacao | poda | 358,2 |
| `semt-8` | 3 | `nulo_inesperado` | `nulo_inesperado` | certo | 0,857 | medio | não medido | sim | não | sim | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 307,9 |
| `semt-9` | 3 | `valor_fora_do_dominio` | `tipo_divergente` | errado | 0,998 | alto | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 323,7 |
| `semt-14` | 3 | `nulo_inesperado` | `nulo_inesperado` | certo | 0,740 | baixo | não medido | sim | sim | não | sim | 4 | 1 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 338,3 |
| `tra-8` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,976 | medio | não medido | sim | não | sim | sim | 4 | 2 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 269,0 |
| `tra-10` | 4 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | certo | 0,995 | alto | não medido | sim | não | não | sim | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | poda | 330,6 |
| `tra-11` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | certo | 0,979 | medio | não medido | sim | não | sim | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 338,9 |
| `tra-15` | 4 | `escala_ou_unidade_errada` | `registro_duplicado` | errado | 0,639 | baixo | causa_sem_verbete_que_a_trate | sim | sim | sim | sim | 4 | 2 | sim | cita o plantado, mesmo rótulo | recuperacao | sem alvo | 314,2 |
| `run-9` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | 0,999 | alto | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 282,5 |
| `run-10` | 5 | `limite_de_requisicoes` | `limite_de_requisicoes` | certo | 0,871 | medio | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 360,7 |
| `run-13` | 5 | `registro_duplicado` | `registro_duplicado` | certo | 0,839 | medio | não medido | não | não | não | não | 4 | 0 | sim | cita o plantado, mesmo rótulo | recuperacao | sem alvo | 287,6 |
| `efe-7` | 6 | `localizador_quebrado` | `localizador_quebrado` | certo | 0,933 | medio | não medido | não | não | não | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 326,8 |
| `efe-14` | 6 | `localizador_quebrado` | `localizador_quebrado` | certo | 0,999 | alto | não medido | sim | não | sim | não | 4 | 0 | sim | não cita o plantado, mesmo rótulo | recuperacao | sem alvo | 334,6 |
<!-- /tabela:tb_f4_trilha_casos -->

</details>

<!-- ! Alteração de IA - Revisar: (10/11/2026, Pós-Fase 4, pacote Q5) a medida com revisor humano foi feita: título desta seção, frase no fim dela, a tabela de abertura e a lista da seção 15.
     ! Motivo: o relatório dizia que a medida estava em aberto pela decisão 95; com a sessão feita pelo Eric (ficha 40, opção b, decisão 113), quem lê precisa saber onde está a leitura e a limitação. -->
<!-- ! Alteração de IA - Revisar: (10/11/2026, tarde) os quatro trechos desta medida foram reescritos: quem leu quase todos os relatórios foi um analista, a quem o Eric passou os relatórios, e o tempo até a decisão não foi medido (decisão 114).
     ! Motivo: os trechos da manhã diziam que o Eric tinha lido os 36 relatórios; ele declarou no quadro que colou as respostas de um analista, e o registro da página confirma. -->
### 9.5 A medida com revisor humano: em aberto em 05/11, feita em parte em 10/11/2026 (decisões 85, 86, 95, 113 e 114)

<!-- ! Alteração de IA - Revisar: (10/11/2026, decisão 117) este trecho e o item da seção 15 passaram a dizer que os 36 relatórios foram lidos por um analista de QA da empresa.
     ! Motivo: o Eric declarou no quadro quem é o analista e que as 36 respostas são dele; o texto dizia 35 do analista e 1 do Eric e remetia à ficha 62, que fechou. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026, decisão 95) a medida com revisor humano passou de limitação declarada a em aberto, neste trecho, no estado do relatório, na tabela de abertura, na seção 12 e na lista da seção 15.
     ! Motivo: o Eric pediu "em aberto": usou a pré-análise por agora, e a revisão será feita depois de as respostas serem normalizadas na Pós-Fase 4. O relato do que aconteceu na sessão de 05/11 não muda. -->

A especificação da trilha (seção 12 c) pede, com um revisor humano, o acerto da localização do erro, o tempo até a decisão e a adesão apropriada, isto é, aceitar o diagnóstico quando está certo e recusar quando está errado. **Essa medida ainda não foi feita e está em aberto: será feita depois que a Pós-Fase 4 normalizar e melhorar as respostas (decisão 95, que revê a 87).** Por agora vale a pré-análise do Claude que o Eric usou. **Feita em parte em 09 e 10/11/2026 (pacote Q5 da Pós-Fase 4; fichas 40 e 62, decisões 113, 114 e 117):** os 36 relatórios v3 com a árvore de decisão da corrida 24 foram lidos um por vez, sem o nome do caso, a classe nem o nível, todos por um analista de QA da empresa, que não participou do projeto nem conhecia o agente e a quem o Eric passou os relatórios. Ficaram medidas a adesão apropriada, a localização do erro e a utilidade; o tempo até a decisão não, porque a página mediu a troca entre os dois. A leitura está em `resultados_alvo/fase4/leitura_revisao_v3.md` e na aba "Revisão humana" do painel; a declaração de quem leu está em `sessao_revisao_v3/quem_leu.json`, e é um leitor só.

O que aconteceu: a amostra tem 11 relatórios, não os 12 do plano, porque a corrida teve só 5 erros: são os 5 e mais 6 acertos. O Eric respondeu o relatório 1, e só esse tem resposta própria dele e tempo medido (307 s). Depois pediu uma pré-análise do Claude e escolheu lê-la (decisão 85), e aprovou o parecer do Claude nos outros 10 relatórios, sem resposta própria e sem tempo medido (decisão 86).

**O parecer do Claude acertar não é essa medida.** O parecer cobre os 11 relatórios, inclusive o 1, e acertou 11 de 11 decisões e 11 de 11 causas (Wilson 95% da decisão: 74,1 a 100,0%). Mas quem o escreveu sabia quantos erros a amostra tem, já tinha visto os nomes dos casos e consultou a biblioteca. Isso mostra que a evidência para julgar estava no relatório e na biblioteca, para um leitor forte e avisado. Não mostra quanto o relatório ajuda um analista, nem quanto tempo ele leva. Na maior parte, a adesão, a localização e a utilidade das tabelas abaixo são do Claude; as tabelas separam quem decidiu.

Dois pontos para quem for citar. Dos 5 erros, 4 estavam à vista no próprio relatório; o de `semt-9` tem selo alto, nenhum conflito e todas as conferências certas, e a recusa só veio da biblioteca. E, no relatório 1 (`run-4`), o Eric marcou que achou o erro num diagnóstico que avaliou como certo; ele pode ter lido "erro" como o defeito do sistema, e a resposta fica como ele deu.

<!-- tabela:tb_f4_revisao_resumo -->
| Relatórios | Com resposta do revisor | Com parecer aprovado | Diagnósticos certos | Diagnósticos errados | Adesão apropriada | Adesão (%) | Wilson 95% | Tempo mediano (s) | Erros achados | Utilidade mediana |
|---|---|---|---|---|---|---|---|---|---|---|
| 11 | 1 | 10 | 6 | 5 | 11 | 100,0 | 74,1 a 100,0 | 307 | 4 de 5 | 4 |
<!-- /tabela:tb_f4_revisao_resumo -->

<!-- tabela:tb_f4_revisao_origem -->
| Quem decidiu | Relatórios | Decisões apropriadas | Apropriadas (%) | Wilson 95% | Avaliação igual ao gabarito |
|---|---|---|---|---|---|
| resposta do revisor | 1 | 1 | 100,0 | 20,7 a 100,0 | 1 |
| parecer do Claude aprovado | 10 | 10 | 100,0 | 72,2 a 100,0 | 10 |
<!-- /tabela:tb_f4_revisao_origem -->

<!-- tabela:tb_f4_revisao_parecer -->
| Relatórios | Decisões apropriadas | Apropriadas (%) | Wilson 95% | Causa certa | Causa certa (%) | Avaliação igual ao gabarito | Errou a decisão | Errou a causa |
|---|---|---|---|---|---|---|---|---|
| 11 | 11 | 100,0 | 74,1 a 100,0 | 11 | 100,0 | 11 | nenhum | nenhum |
<!-- /tabela:tb_f4_revisao_parecer -->

<!-- tabela:tb_f4_revisao_adesao -->
| Grupo | Relatórios | Aceitou | Recusou | Apropriadas | Apropriadas (%) | Wilson 95% |
|---|---|---|---|---|---|---|
| diagnóstico certo | 6 | 6 | 0 | 6 | 100,0 | 61,0 a 100,0 |
| diagnóstico errado | 5 | 0 | 5 | 5 | 100,0 | 56,6 a 100,0 |
| todos | 11 | 6 | 5 | 11 | 100,0 | 74,1 a 100,0 |
<!-- /tabela:tb_f4_revisao_adesao -->

<!-- tabela:tb_f4_revisao_localizacao -->
| Grupo | Relatórios | Achou um erro | Não achou | Não viu erro | Achou (%) | Wilson 95% |
|---|---|---|---|---|---|---|
| diagnóstico errado | 5 | 4 | 1 | 0 | 80,0 | 37,6 a 96,4 |
| diagnóstico certo | 6 | 1 | 0 | 5 | 16,7 | 3,0 a 56,4 |
<!-- /tabela:tb_f4_revisao_localizacao -->

<!-- tabela:tb_f4_revisao_tempo -->
| Grupo | Relatórios | Mediana (s) | Mínimo (s) | Máximo (s) |
|---|---|---|---|---|
| todos | 1 | 307 | 307 | 307 |
| diagnóstico certo | 1 | 307 | 307 | 307 |
| diagnóstico errado | 0 | não medido | não medido | não medido |
| aceitos | 1 | 307 | 307 | 307 |
| recusados | 0 | não medido | não medido | não medido |
<!-- /tabela:tb_f4_revisao_tempo -->

<!-- tabela:tb_f4_revisao_utilidade -->
| Grupo | Relatórios | Mediana | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|
| todos | 11 | 4 | 0 | 1 | 4 | 4 | 2 |
| diagnóstico certo | 6 | 3,5 | 0 | 0 | 3 | 3 | 0 |
| diagnóstico errado | 5 | 4 | 0 | 1 | 1 | 1 | 2 |
<!-- /tabela:tb_f4_revisao_utilidade -->

<!-- tabela:tb_f4_revisao_avaliacao -->
| Diagnóstico | Revisor disse certo | Revisor disse errado |
|---|---|---|
| certo | 6 | 0 |
| errado | 0 | 5 |
<!-- /tabela:tb_f4_revisao_avaliacao -->

<details><summary>Relatório a relatório (tb_f4_revisao_casos)</summary>

<!-- tabela:tb_f4_revisao_casos -->
| # | Caso | Gabarito | Rótulo | Resultado | Selo | Quem decidiu | Tempo (s) | Erro localizado | Decisão | Apropriada | Utilidade | Avaliação | Causa no parecer do Claude | Comentário |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `run-4` | `dado_desatualizado` | `dado_desatualizado` | certo | alto | resposta do revisor | 307 | sim | aceitar | sim | 4 | certo | `dado_desatualizado` |  |
| 2 | `run-1` | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | medio | parecer do Claude aprovado | não medido | n.a. | aceitar | sim | 3 | certo | `erro_interno_do_servidor` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 3 | `lex-10` | `resposta_truncada` | `resposta_truncada` | certo | alto | parecer do Claude aprovado | não medido | n.a. | aceitar | sim | 4 | certo | `resposta_truncada` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 4 | `semt-9` | `valor_fora_do_dominio` | `tipo_divergente` | errado | alto | parecer do Claude aprovado | não medido | não | recusar | sim | 2 | errado | `valor_fora_do_dominio` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 5 | `tra-15` | `escala_ou_unidade_errada` | `registro_duplicado` | errado | baixo | parecer do Claude aprovado | não medido | sim | recusar | sim | 4 | errado | `escala_ou_unidade_errada` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 6 | `sin-11` | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | alto | parecer do Claude aprovado | não medido | n.a. | aceitar | sim | 3 | certo | `estrutura_aninhada_divergente` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 7 | `lex-8` | `codificacao_incorreta` | `codificacao_incorreta` | certo | baixo | parecer do Claude aprovado | não medido | n.a. | aceitar | sim | 3 | certo | `codificacao_incorreta` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 8 | `efe-1` | `localizador_quebrado` | `tempo_de_resposta_excedido` | errado | medio | parecer do Claude aprovado | não medido | sim | recusar | sim | 5 | errado | `localizador_quebrado` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 9 | `semt-5` | `nulo_inesperado` | `nulo_inesperado` | certo | alto | parecer do Claude aprovado | não medido | n.a. | aceitar | sim | 4 | certo | `nulo_inesperado` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 10 | `sin-5` | `campo_ausente` | `colecao_no_lugar_de_objeto` | errado | baixo | parecer do Claude aprovado | não medido | sim | recusar | sim | 3 | errado | `campo_ausente` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 11 | `sin-14` | `campo_renomeado` | `colecao_no_lugar_de_objeto` | errado | baixo | parecer do Claude aprovado | não medido | sim | recusar | sim | 5 | errado | `campo_renomeado` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
<!-- /tabela:tb_f4_revisao_casos -->

</details>

### 9.6 A poda foi consertada depois das corridas, sem corrida nova (decisão 89)

A pré-análise da sessão achou dois defeitos em `poda.diff_contrato`: ela só olhava o primeiro item de uma lista, e chamava todo número em campo booleano de tipo diferente, enquanto a biblioteca separa 0 e 1 (tipo diferente) dos outros números (valor fora do domínio). Os dois foram consertados, com teste, depois de todas as corridas, e nenhuma corrida foi refeita.

A comparação da poda de antes com a de agora, sem modelo, está em `resultados_alvo/fase4/poda_antes_e_depois.json`. Nos casos de texto ela muda em 5 dos 65 casos com contrato (`sin-5`, `semt-9`, `semt-14`, `sin-20`, `semt-17`), mas nesses casos o prompt leva o corpo inteiro e **a poda não chega ao modelo**: ela só alimenta a trilha, a tabela do contrato e a justificativa do relatório. Por isso os erros de `sin-5` e `semt-9` na corrida 22 não vieram desses defeitos. **Só na tela o trecho da poda vai ao prompt**, e ali nenhum dos 209 corpos guardados nas 7 corridas na tela muda, 158 deles listas com mais de um item, inclusive os cenários da Fase 5. Então as corridas continuam valendo como rodaram, e a Fase 5 sai comparável com elas, com a poda consertada.

## 10. As regras da fase, uma a uma

| Regra | O que ela pede | Corrida | Resultado | Estado |
|---|---|---|---|---|
| R1 | Um caso reproduz quando a chamada sai do normal ou uma conferência do roteiro falha; o plano pedia também o passo esperado e o campo do gabarito | 17 | 37 de 37 nos 72 casos e 25 de 25 nos inéditos | Cumprida, com ressalva: como rodou, é mais larga que o texto do plano |
| R2 | A tela não piora: rótulos na tela e no fixture diferem em no máximo 3 casos; desde a decisão 98, a tela não perde mais de 3 casos para o fixture | 18d, 18e | 18d: c = 3, b = 5, b + c = 8, p = 0,727. 18e, nos inéditos: c = 0, b = 4, b + c = 4, p = 0,125. Na 18c: c = 5, b = 2; na 18b: c = 7, b = 2 | Cumprida, com ressalva: no limite exato, pela leitura fixada antes da 18d (decisão 98); pela soma dos dois lados ficaria fora |
| R3 | Uma cura só conta com o roteiro passando na reexecução | 19, 21b, 21c, 21d | 160 de 160 sem modelo; 4 de 4 com o modelo no meio, nas três repetições | Cumprida, com ressalva: os 100% vêm do desenho da corrida 19 |
| R4 | Precisão e revocação da marca `corrigido` contra os modos desligados | 20 | 100,0% e 100,0% em 9 casos | Medida: o plano não fixou limite |
| R5 | O lote entra se b for maior ou igual a c nos 36 inéditos | 20 | b = 0, c = 0: aceito | Cumprida, com ressalva: nenhum caso mudou, e a biblioteca promovida não foi reavaliada |
| R6 | Ponte de versão antes de toda noite medida | todas | Pontes em 0.40.2 e 0.40.14, b + c até 2 | Cumprida |
| R7 | Limiares do selo gravados antes da primeira corrida na tela | 16 | `limiares.json`, baixo até 0,832 e alto a partir de 0,990 | Cumprida, com ressalva: calibrados em 0.40.2; com o corte, os prompts da tela ficaram dentro do limite |
| R8 | k = 5 só entra se acertar mais que k = 3 | 16 | k = 3 | Cumprida |
| Prompt na tela (plano, seção 3.3) | O prompt ao vivo não passa o maior da calibração em mais de 10%; se passar, a poda aperta | 18c, 21c, 18d, 21d, 18e | Nenhum prompt acima de 1409 tokens nas corridas 18c, 21c, 18d e 21d: o maior com 1373, 1340, 1385 e 1385. Nas corridas 18b e 21b passavam 37 de 37 e 9 de 10. Na 18e, 2 de 25 passaram (1829 e 1620), e o teto nas listas os leva a 1367 e 1387 (decisão 99) | Cumprida, com ressalva: só nas repetições, depois das decisões 90 e 99 |

## 11. O que a Fase 4 entrega à Fase 5

- **Cenários e leitura:** os dez cenários em `cenarios_fase4.CENARIOS_DO_ENSAIO`, com a troca de `latency` por `escala_ou_unidade_errada` registrada; `rodar_fase4.ps1 -Modo cenarios -Repeticoes N` e `avaliar_fase4.py --cenarios`. A noite estimada é de 1,07 h, pela corrida 21d.
- **Cronômetro e critério:** MTTR e Task Success como a ficha 35 fixou, com o banco restaurado e conferido por hash a cada repetição (`9fe5e7cb64288c9d`) e o navegador fixo (156.0.8078.4).
- **Linha de base manual:** o [protocolo](../5-metodo-e-ferramental/protocolo-linha-de-base-manual.md), o ajudante `linha_de_base_manual.py` e a [planilha](../5-metodo-e-ferramental/planilha-linha-de-base-manual.csv). A sessão com os três integrantes depende do grupo e ainda não foi marcada.
- **Agente:** `qwen2.5:7b`, k = 3, limiares de `limiares.json`, biblioteca de produção `95af35290860` (39 verbetes), poda consertada (seção 9.6), sinais da busca contra a referência (decisão 97), teto nas listas do caso ao vivo (decisão 99), trilha v2 e relatório v2 por caso.
- **Antes da noite da Fase 5:** a Pós-Fase 4 (decisão 94) e a ponte, se o Ollama mudar de versão (regra R6).

## 12. Limitações

- **A medida com revisor humano foi feita em parte depois, no pacote Q5 da Pós-Fase 4** (fichas 40 e 62, decisões 113, 114 e 117; seção 9.5): na sessão de 05/11, 1 resposta do Eric e 10 pareceres do Claude aprovados (decisões 85, 86 e 95); em 09 e 10/11/2026, os 36 relatórios v3 da corrida 24 foram lidos por um analista de QA da empresa, a quem o Eric passou os relatórios (`resultados_alvo/fase4/leitura_revisao_v3.md`): adesão, localização do erro e utilidade medidas, tempo até a decisão não.
- **A regra R1 rodou mais larga que o texto do plano** (seção 3): não confere o campo do gabarito, e só 12 dos 37 casos derrubam uma conferência do roteiro.
- **A regra R2 fechou no limite exato, e por uma leitura fixada depois da 18c** (decisões 97 e 98, seção 5): a tela perde 3 casos para o caso escrito, e o limite é 3; pela soma dos dois lados, a conta usada até a 18c, são 8. A leitura foi fixada antes da 18d, sem conhecer o resultado, e as duas contas saem em toda leitura. Corridas iguais já variaram até 3 casos, então outra corrida pode passar do limite.
- **Os sinais da busca foram escritos olhando os 37 casos da 18d** (decisão 97): a conferência limpa é a 18e, com 25 casos, e esses casos deixam de servir de conferência limpa para outro ajuste na busca. A corrida 24 releu esses 25 em texto e deu o mesmo rótulo nos 25.
- **A tela leva uma medida que o caso escrito não tem** (seção 5): a tela à frente do fixture diz que a medida contra a referência ajuda a busca, não que o modelo lê melhor da tela.
- **Quando a chave `id` muda em todos os itens, a comparação lê tudo como faltando e sobrando** (decisão 99): o teto resolve o tamanho do prompt, e a busca de `semt-27` continua indo para `contagem_inconsistente`. Ficou registrado, sem mexer, porque esses casos são a conferência limpa.
- **A corrida 18c mudou três coisas de uma vez contra a 18b:** o caso ao vivo, a versão do Ollama e a biblioteca. O fixture serve de controle (a causa mudou em 1 de 37), mas a comparação não isola cada efeito.
- **A conta do carimbo por gatilho não vem de uma corrida que rodou assim** (decisão 88, seção 9.1), e 5 erros não sustentam ordenar os sinais.
- **A poda foi consertada depois das corridas, sem corrida nova** (decisão 89, seção 9.6): nenhum corpo guardado muda, e nos casos de texto ela não chega ao modelo.
- **O limite do prompt na tela só foi cumprido nas repetições** (plano, seção 3.3; decisão 90): as corridas 18, 18b e 21b passaram dele, e os prompts da 18c, da 21c, da 18d e da 21d cabem. Na 18e, 2 de 25 passaram, e o teto da decisão 99 veio depois da corrida. As leituras de antes ficam nos arquivos delas.
- **A corrida 24 tem uma condição só** (decisão 92, seção 7.1): mede a biblioteca final em casos inéditos, não quanto ela ajuda neles, e não são os mesmos casos dos 36 de avaliação. Os casos que a R5 usa são outro conjunto, os 36 inéditos da Fase 3-B.
- **A conferência dos inéditos seguiu as recomendações do Claude em todos os casos** (decisão 100): o Eric leu os 10 apontados, um a um, e passou os olhos nos outros 26, numa lista de uma linha por caso. As recomendações foram escritas por quem já tinha visto os resultados da corrida 18e, e o quadro não os mostrou. Ficaram aceitas três tensões: `semt-26` tem o gabarito `nulo_inesperado` com um contrato que aceita nulo; `run-26` é um cenário descrito, que a CobaiaAPI não produz; e o sintoma de `tra-27` cita uma conferência de preço que o roteiro do detalhe não tem.
- **O experimento dos itens da decisão 55 não separa nenhum dos dois do acaso** (ficha 34 a; decisão 91, seção 4.1): compara com a corrida 16, de outra versão do Ollama, e não muda o agente.
- **O trace do Playwright na falha não existe** (ficha 33; decisão 93): as corridas guardam a árvore, o corpo e os eventos na trilha, e a Fase 5 roda assim.
- **A quebra de localizador é armada, não ocorrida** (seção 6), e os 100% da corrida 19 vêm do desenho dela.
- **MTTR e Task Success são de um ensaio:** uma repetição por cenário, intervalos largos e nenhuma linha de base manual; a comparação é da Fase 5.
- **As corridas até a 18c e a 21c podiam, em tese, ter um caso sem a chamada capturada:** 1 em 25 execuções do modo error_500 saía assim, porque a corrida lia os registros enquanto a resposta ainda era guardada. Nenhum prompt guardado saiu sem status, e o conserto (`Interceptador.esperar_respostas`) deu 0 em 100 em cada um de três modos.
- **Os limiares vêm do Ollama 0.40.2**, e as corridas 18c, 18d, 18e e 20 a 23 rodaram em 0.40.14 (seção 2).
- **A revisão do lote foi a pré-revisão do Claude aprovada pelo Eric**, sem mudança, e a biblioteca promovida não foi reavaliada nos inéditos (seção 7).
- **Em 5 dos 36 casos da corrida 22, 2 deles na amostra**, a justificativa gravada atribui a resposta ao sinal "recebido corpo nao_json", mas o corpo desses fixtures é texto corrido; o defeito foi consertado para as próximas corridas, e a frase fica nesses relatórios porque está gravada na trilha (roadmap §2.15). Os 133 relatórios de `fase4_trilha/relatorios/` não mostram o caso; os 11 da sessão foram regerados da mesma trilha com isso corrigido.
- **Só 37 dos 72 casos têm tela e modo.** As rotas de pedidos não têm página, a classe de efeito entra pela quebra armada, e `run-10`, `semt-18` ficaram de fora por um defeito da seleção (seção 3): os outros seguem avaliados só em texto.
- **Texto de agente:** os documentos desta fase foram escritos pelo Claude. No fechamento, este relatório, os achados, o roadmap, o README e o handoff tiveram um revisor cada, que conferiu coerência, frases desatualizadas e números sem origem; as correções estão em `5-metodo-e-ferramental/dados/revisao-fase-4-2026-11-05.json`. O que o revisor não cobre é o mérito das decisões.

## 13. O que o plano previa e não saiu

A lista completa dos desvios, com o motivo de cada um, está no anexo do [plano aprovado](../../../claude-memoria/plano-aprovado-fase-4.md). Quatro pontos dependiam do Eric e viraram as fichas 42 a 45 de [pendencias.md](../pendencias.md). Ele respondeu as quatro em 05/11/2026, no quadro da sessão (decisões 90 a 93), e três pedem trabalho antes da Fase 5:

- **Ficha 42, decisão 90, opção (b):** o limite do prompt na tela (seção 5). O caso ao vivo encurta, sem tocar no prompt fixo, e as corridas 18 e 21 foram repetidas em pasta nova: a 18c e a 21c rodaram em 05/11/2026 à noite, em 01h17 e 00h13 (seções 5 e 8). As leituras que valem agora são as das repetições seguintes, a 18d e a 21d (decisão 97).
- **Ficha 43, decisão 91, opção (a):** o experimento em texto nos 90 casos que a ficha 34 (a) mandou fazer, com o exemplar resolvido fixo e a forma dos rótulos, não entrou na tabela de corridas do plano. Foi escrito em código novo (`corridas_em_texto.py`) e rodou como corrida 23, em 02h56 (seção 4.1); o prompt do agente continua congelado, também na Fase 5.
- **Ficha 44, decisão 92, opção (a):** os 36 inéditos da ficha 27 não têm conferência registrada e, até então, nenhuma corrida com modelo os tinha lido; depois disso, a corrida 18e leu 25 deles (decisão 97). O Eric conferiu os 36 em 06/11/2026, sem mudar nenhum (ficha 46, decisão 100), e a corrida 24 os diagnosticou em texto com a biblioteca de produção, em 00h43 (seção 7.1).
- **Ficha 45, decisão 93, opção (a):** o trace do Playwright na falha (ficha 33), a aba "Cérebro ao vivo" e o explorador de casos lendo a trilha v2 (plano, seção 3.8) não foram feitos nesta fase. Os três entram na interface para o analista, que o Eric especifica, para depois da Fase 5 (roadmap §7), e a Fase 5 roda sem trace.

O `painel_fase4.py` do plano não foi criado: as abas da fase ficaram em `ferramentas/painel_topicos.py`, uma por análise, como manda a regra do painel, e o fechamento ganhou a aba "Fechamento da fase", lida deste relatório.

## 14. Rastreabilidade

| O quê | Onde |
|---|---|
| Leituras por corrida | `resultados_alvo/fase4/`: `reproducibilidade`, `reproducibilidade_ineditos`, `calibracao`, `tela`, `tela_v2`, `tela_v3`, `tela_v4`, `tela_ineditos`, `cura`, `biblioteca`, `cenarios`, `cenarios_v2`, `cenarios_v3`, `cenarios_v4`, `experimento_prompt`, `conferencia_ineditos` (com as respostas do Eric em `conferencia_ineditos_respostas.json`), `ineditos`, `trilha`, `leitura_revisao_trilha` (`.json` e `.md`), `limiares.json`, `pontes.json`, `ambiente.json`, `poda_antes_e_depois.json`, `prompt_tela_blocos.json` (`medir_prompt_tela.py`), `corte_prompt_tela.json`, `busca_prompt_tela.json` e `teto_prompt_tela.json` (`conferir_corte_tela.py`) |
| Qual leitura está nos blocos deste relatório | `avaliar_fase4.LEITURA_NO_RELATORIO`: `reproducibilidade`, `tela_v4` e `cenarios_v4`; `--colar` recusa as outras, e o `--check` delas confere só os próprios arquivos |
| Corridas (registros, trilhas, relatórios por caso, logs) | `resultados_alvo/fase4_*/`, nunca regravadas |
| Comandos de conferência | em `Programacao/AgenteCore/experimentos`, `RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py <modo> --saida <pasta> --check`, com as corridas certas: `--reproducao --saida fase4_reproducao`; `--calibracao --saida fase4_calibracao`; `--tela --saida fase4_tela_v4 --nome tela_v4`; `--tela --saida fase4_tela_ineditos --nome tela_ineditos`; `--cura --saida fase4_cura`; `--biblioteca --saida fase4_biblioteca`; `--cenarios --saida fase4_ensaio_v4 --nome cenarios_v4`; `--experimento_prompt --saida fase4_experimento`; `--ineditos --saida fase4_ineditos`; `--trilha --saida fase4_trilha`; `--revisao` |
| Sessão de revisão | `resultados_alvo/fase4/revisao_trilha.md` (planilha), `revisao_trilha_respostas.json` (a resposta crua), `pre_analise_revisao_trilha.md` (o parecer do Claude), `relatorios_revisao_trilha/`, `ferramentas/sessao_revisao.py` |
| Decisões | [decisoes.md](../1-decisoes-e-historico/decisoes.md): 79 e 80 (plano), 81 e 82 (caso ao vivo e R2), 85 a 87 (revisão), 88 (carimbo), 89 (poda), 90 a 93 (fichas 42 a 45), 94 e 95 (Pós-Fase 4 e revisor humano), 96 (a busca lê o corpo inteiro), 97 (sinais da busca contra a referência), 98 (a regra R2 pelos casos que a tela perde), 99 (o teto nas listas do caso ao vivo), 100 (a conferência dos 36 inéditos) |
| Fichas | [pendencias.md](../pendencias.md): 26 a 39 e 41 a 48 fechadas; 40 aberta |
| Especificação da trilha | [especificacao-trilha-e-relatorio.md](../5-metodo-e-ferramental/especificacao-trilha-e-relatorio.md) |
| Plano e desvios | `claude-memoria/plano-aprovado-fase-4.md` (anexo), `.superpowers/sdd/fase-4/progress.md` (fora do git) |
| Painel | grupo Fase 4 de `ferramentas/painel_topicos.py`, publicado em https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN |
| Testes | `testar_fase4.py`, `testar_pre_fase4.py`, `ferramentas/testar_painel_topicos.py`, `ferramentas/testar_sessao_revisao.py` |

## 15. O que a próxima versão do documento do TCC precisa carregar

<!-- ! Alteração de IA - Revisar: (05/11/2026) a abertura da seção 15 ganhou a versão 3 do documento.
     ! Motivo: a seção 6 do documento mudou de forma no mesmo dia; quem procurasse um item da lista na seção 6.7 não acharia sem o aviso. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026) abertura da seção 15 reescrita: a versão 2 do documento do TCC saiu com os 12 itens aplicados, e para a próxima ficam os trechos dos itens 6 e 11 que dependem das corridas 18c, 21c, 23 e 24.
     ! Motivo: a abertura dizia que o texto parava em 01/11/2026 e que a atualização dependia de o Eric pedir; a versão 2 já saiu e cobre até a corrida 22, e quem lesse a seção aqui ou na aba "Fechamento da fase" do painel acharia que a lista ainda não tinha sido aplicada. A lista fica como estava, porque é o registro do que a versão 2 carregou. -->
A versão 2 do documento saiu em 05/11/2026, com o sim do Eric e os 12 itens abaixo aplicados: [`Documentacao/TCC_v2_20261105.docx`](../../TCC_v2_20261105.docx), gerado de [`Documentacao/TCC - ABNT 14724 - V1.md`](../../TCC%20-%20ABNT%2014724%20-%20V1.md), com o estado de cada item no [registro da conferência](../5-metodo-e-ferramental/dados/revisao-tcc-v2-2026-11-05.json). A lista fica como registro do que ela carregou. A versão 3, do mesmo dia (`Documentacao/TCC_v3_20261105.docx`), reorganizou a seção 6 com figuras e levou as tabelas e os valores para a seção 6.9, sem número novo de corrida; os trechos que a lista pede nas seções 6.7 e 6.8 estão agora nas duas e na 6.9. Para a próxima versão valem os trechos dos itens 6 e 11 que dependem de corrida: os números das corridas 18c e 21c, com a 18b e a 21b como a leitura anterior, e os das corridas 23 e 24. O .docx sai de `ferramentas/gerar_tcc_docx.py`, com a versão e a data novas no bloco `## Dados`. Os itens:

1. **Seção 6.7, título e fecho:** tirar "em andamento até 01/11/2026" e o parágrafo "Faltam o P5...". Entram as corridas 20, 21, 21b e 22 com os números das seções 7, 8 e 9 deste relatório. As corridas 18 e 21 aparecem com as repetições como leituras vigentes (18b, decisão 82; 21b, roadmap §2.14).
2. **Seções 6.7 e 6.8, a medida com revisor humano:** dizer que ela não foi feita (decisões 85, 86 e 87), com 1 resposta do Eric e 10 pareceres do Claude aprovados, e que o parecer acertar 11 de 11 não é essa medida, porque quem o escreveu sabia quantos erros a amostra tem e consultou a biblioteca. Usar o texto da seção 9.5.
3. **Seção 6.8, o carimbo de conflito:** as duas contas juntas (TPR x TNR de 0,284 com as intervenções em todos os casos e de 0,542 por gatilho), dizendo que a segunda sai de uma corrida que não rodou assim, e que 5 erros não ordenam os sinais (decisão 88).
4. **Seção 6.7, a poda consertada depois das corridas** (decisão 89): nos casos de texto o prompt leva o corpo inteiro e a poda não chega ao modelo; só na tela o trecho dela vai ao prompt, e nenhum corpo guardado muda.
5. **Seções 5.7 e 6.7, a regra R1:** ela rodou mais larga que o texto do plano; os 37 de 72 dizem que a falha injetada muda o fio ou a tela (seção 3).
6. **Seções 6.7 e 6.8, a regra R2 e o limite do prompt:** a regra R2 continua como limitação (decisão 82); acrescentar o limite da seção 3.3 do plano e a decisão 90. Quando as corridas 18c e 21c rodarem, os números da regra R2 e do MTTR passam a ser os delas, com a 18b e a 21b como a leitura anterior; antes disso, o texto diz que as duas vão ser repetidas.
7. **Seção 6.8, terceira parte:** a frase "o ciclo de correção da biblioteca (pacote P5) é a próxima tentativa de fechar essa distância" ficou velha. O P5 rodou, o lote não mudou acerto nenhum nos inéditos (b = 0, c = 0), e o que encurtou a distância foi a revisão do caso ao vivo. A mesma parte ganha a cura com o modelo no meio (a corrida 21 achou o defeito do recarregamento da página, e a 21b conferiu o conserto) e o MTTR com modelo (105,2 s, sem linha de base).
8. **Seção 6.8, as três limitações finais:** a linha de base manual segue sem medida. Acrescentar que o MTTR do contrato e o do localizador não medem a mesma coisa (ficha 35).
9. **Seção 7:** atualizar o estado dos objetivos 3 e 4 e o parágrafo "O que falta", que ainda lista os pacotes P5 a P8 e as corridas 20 a 22. Ficam a Fase 5, a interface para o analista, a revisão humana das marcações e a revisão final das referências.
10. **Seções 5.5 a 5.7:** conferir contra o que rodou: a recuperação por id, os filtros da decisão 65, a avaliação da trilha, o critério da ficha 35 e o fato de só as corridas na tela levarem o trecho da poda ao prompt. A seção 5.8 conta "84 decisões" e passa a 93.
11. **Seções 6.7 e 7, as decisões 91 a 93:** o experimento da decisão 55 (corrida 23) e os 36 inéditos (corrida 24) entram com os números quando rodarem, e até lá como pendentes, não como não feitos; o trace na falha, o "Cérebro ao vivo" e o explorador com a trilha v2 entram como não feitos na Fase 4, com a interface para o analista depois da Fase 5.
12. **Apêndice B:** acrescentar este relatório, `resultados_alvo/fase4/` e a página da sessão de revisão.

Depois da versão 3, a próxima versão precisa levar também: a medida com revisor humano como "em aberto", e não como limitação sem nova sessão (decisão 95: resumo, abstract, tabela da seção 5.1 e seções 5.7, 6.7, 6.8 e 6.9), e a Pós-Fase 4 na tabela das fases e no parágrafo do que falta (decisão 94). As corridas 18c, 21c e 23 também rodaram: a próxima versão leva os números delas (seções 4.1, 5 e 8 deste relatório) no lugar dos da 18b e da 21b. As figuras `tela-e-caso-escrito`, `prompt-e-limite`, `tempo-por-cenario`, `onde-vai-o-tempo` e `tela-por-classe` já mudaram em `Documentacao/figuras/`, e as legendas e o texto do documento ainda citam as corridas 18b e 21b: o texto precisa ser revisto antes de gerar o documento de novo. Em 06/11/2026 rodaram as corridas 18d, 21d e 18e: a próxima versão leva os números delas (seções 5 e 8) como a leitura vigente, com a regra R2 cumprida no limite exato, as duas contas e a data em que a leitura foi fixada (decisões 97 e 98), a conferência nos inéditos e o aviso de que o caso da tela leva uma medida que o caso escrito não tem; o teto nas listas (decisão 99) entra na descrição do caso ao vivo; e a conferência dos inéditos entra como feita, com as duas ressalvas da decisão 100. A corrida 24 também rodou: a próxima versão leva o número dela (25 de 36, seção 7.1), com o aviso de que há uma condição só, e a Fase 4 entra como concluída, com a Pós-Fase 4 na frente da Fase 5.
