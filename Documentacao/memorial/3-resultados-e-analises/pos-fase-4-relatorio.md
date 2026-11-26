<!-- ! Alteração de IA - Revisar: arquivo novo (25/11/2026): o relatório da Pós-Fase 4 (o que chega ao analista), escrito a partir do plano aprovado, do anexo de desvios dele, das decisões 94 a 129, 152, 157 e 163 e das leituras de `resultados_alvo/fase4/` e `resultados_alvo/fase4_analista/`. As tabelas são coladas por `colar_pos_fase4.py` (blocos `tb_f4_*`, conferidos por `colar_pos_fase4.py --check`); no texto corrido, cada número leva a origem num comentário HTML que começa por `fonte:`, logo depois da frase.
     ! Motivo: o plano põe o relatório no pacote Q8 e a fase passou por dez pacotes e três corridas com modelo, cada um com a sua leitura e o seu `--check`, mas sem um texto que diga, num lugar só, o que a fase perguntou, o que respondeu e o que ficou de fora. Nenhum número de resultado foi digitado à mão: o que não tem origem em leitura, em decisão ou no plano não entrou. -->
<!-- ! Alteração de IA - Revisar: (26/11/2026, Pós-Fase 4, pacote Q8) o relatório passa ao estado de 26/11/2026: a corrida curta da ficha 99 lida (seção 3.11), o hub como central aberta pelo `Cobaia.exe` (seção 3.10), os desvios 12 a 16 na seção 6 e as linhas novas da rastreabilidade; sai a marca de espera da ficha 99.
     ! Motivo: o relatório dizia que a corrida com as cobaias estava pendente e descrevia um hub que só abria por comando; a ficha 99 foi fechada em 25/11/2026 e a decisão 170 mudou o que o `.exe` abre. Os números da corrida curta vêm dos registros da pasta `fase4_fumaca_q7`, conferidos por script antes de entrar no texto. -->

# Pós-Fase 4: o que chega ao analista, relatório da fase

Estado em 26/11/2026: os pacotes Q0 a Q7 estão feitos. A corrida curta que prova o trace e a seleção pelo Git com as cobaias rodou em 25/11/2026 (ficha 99, seção 3.11), e na mesma noite o hub virou a central aberta pelo `Cobaia.exe` (decisão 170, seção 3.10). Do pacote Q8 (este relatório, o texto final do TCC e o arquivo Word), o texto está escrito, e o Word e o PDF saem uma vez só, no fim: quando a terceira execução do instalador e a prova do botão do hub estiverem lidas, ou em 30/11/2026 com o que estiver lido (decisões 158, 168 e 172).

## 1. O que a fase perguntou e o que respondeu

A Fase 4 fechou com o agente lendo a tela, diagnosticando, curando o localizador em código e gravando a trilha de cada passo. Ela não cuidou de quem lê: o relatório por caso e os verbetes chegavam ao analista em texto corrido, com jargão da IA, e a espera de cada diagnóstico não dava sinal de que a máquina não tinha travado. A Pós-Fase 4 muda o que chega ao analista sem mudar o que o agente mede: o prompt, a biblioteca de produção, a busca, a poda e a cura ficaram como estavam.<!-- fonte: plano-aprovado-pos-fase-4.md, seções 1.1 e 2, princípio 1 -->

<!-- ! Alteração de IA - Revisar: (26/11/2026, Pós-Fase 4, pacote Q8) as linhas do Q6, do Q7 e do Q8 passam ao estado de 26/11/2026.
     ! Motivo: a linha do Q7 dizia que a corrida com o modelo ainda não tinha rodado, a do Q6 não contava a central (decisão 170) e a do Q8 dava o texto como em andamento. -->
| Pacote | O que perguntou | O que respondeu |
|---|---|---|
| Q1 | O relatório por caso cabe no molde do relatório de defeitos do syllabus CTFL 4.0 (seção 5.5)? Os verbetes podem ser lidos sem jargão sem mudar o que o modelo lê? | Sim nos dois: relatório v3 gerado da trilha, e uma camada de leitura fora da biblioteca |
| Q2 | Dá para medir prolixidade e objetividade por código, com fonte e limiar declarados? | Sim: oito medidas em biblioteca padrão, limiares calibrados no corpus de referência |
| Q3 | A decisão do agente pode ser mostrada como árvore, sem jargão e sem esconder o que o modelo só declarou? | Sim: uma árvore por caso, cada afirmação com o rótulo da origem |
| Q4 | Dá para mostrar o andamento enquanto o modelo pensa, e a seleção de cenários pelo Git é viável? | Sim para os dois, com erro de estimativa medido e prova sobre o histórico do repositório |
| Q5 | Um leitor que não é o autor aceita o diagnóstico certo e recusa o errado? | Sim na maior parte dos casos, com o tempo não medido (seção 3.5) |
| Corrida 25 | As notas que o modelo escreveu na biblioteca pesam no diagnóstico? | Não saiu do ruído |
| Corrida 26 | Um segundo passe do diagnóstico, só nos casos com sinal, melhora o agente? | Não saiu do ruído |
| M1 e corrida 27 | Um analista de documentação (o modelo no papel de quem propõe edição de verbete) produz proposta aproveitável? | A forma melhora; a parcela correta ficou dentro do ruído |
| Q6 | Um hub à imagem de uma pull request reúne relatório, evidência, árvore, comentário e veredito? | Sim, provado em teste; desde 25/11/2026 é também a central aberta pelo `Cobaia.exe` (decisão 170) |
| Q7 | A seleção de cenários pelo Git é segura e foi conferida? | Provada em teste, em conta retrospectiva e numa corrida curta com o modelo, em que a regra mandou rodar os dez cenários; nenhuma seleção parcial rodou |
| Q8 | O texto final e o Word | Texto final escrito em 25 e 26/11/2026; o Word e o PDF saem uma vez só, no fim (decisões 158, 168 e 172) |

## 2. Como rodou

- **Q0 (07/11/2026):** pesquisa, fichas 49 a 54, decisões 101 a 104, plano aprovado (decisão 105). Sem código do agente.<!-- fonte: decisoes.md, decisões 101 a 105 -->
- **Q1 a Q4 (07 e 08/11/2026):** sem modelo, com testes escritos antes do código. A única parte com o modelo foi a fumaça da barra de progresso (uma inferência), rodada na janela do Eric em 08/11/2026 (decisão 112).<!-- fonte: decisoes.md, decisão 112; fumaca_progresso.md, cabeçalho -->
- **Q5 (09 e 10/11/2026):** a revisão dos 36 relatórios da corrida 24 e a curadoria das 39 leituras dos verbetes. Quem leu foi um analista de QA da empresa em que o Eric trabalha, que não participou do projeto nem conhecia o agente; o Eric só digitou ou colou as respostas dele na página (decisões 114 e 117).<!-- fonte: decisoes.md, decisões 114, 115 e 117; leitura_revisao_v3.md, segundo parágrafo -->
- **Corridas 25, 26 e 27 (noite de 11 para 12/11/2026):** o Eric lançou a fila das três pela janela dele, com o modelo `qwen2.5:7b` no Ollama.<!-- fonte: roadmap.md, §4.8, parágrafo da fila -->
- **Revisão às cegas da corrida 27 (16/11/2026):** feita pelo mesmo analista de QA, e não pelo Eric (decisão 129, que revê a 123).<!-- fonte: decisoes.md, decisão 129; quem_revisou.json, quem -->
- **Painel por fase (11/11/2026):** decisão 124.<!-- fonte: decisoes.md, decisão 124 -->
- **Q6 e Q7 (25/11/2026):** feitos inteiros antes do Q8 (decisão 152), pelo desenho aprovado no quadro (decisão 157), sem o modelo e sem as cobaias; a corrida curta do trace e da seleção foi autorizada pelo Eric (decisão 163) e ainda não tinha rodado.<!-- fonte: decisoes.md, decisões 152, 157 e 163 -->
- **Nenhuma corrida repetiu medida da Fase 4:** as leituras vigentes `tela_v4` (corrida 18d), `cenarios_v4` (21d) e `ineditos` (24) continuam valendo.<!-- fonte: plano-aprovado-pos-fase-4.md, seção 1.2 -->

## 3. O que cada entrega fez e mediu

### 3.1 Q1: o relatório por caso no molde da seção 5.5 e a camada de leitura dos verbetes

**O que foi feito.** O relatório v3 sai da trilha v2 e dos registros, com os campos que a seção 5.5 do syllabus CTFL 4.0 lista para um relatório de defeitos de teste dinâmico (identificador, título, data e autor, objeto e ambiente, contexto, descrição para reproduzir, resultado esperado contra real, severidade, prioridade, estado, referências). O que o código sabe é preenchido por código; severidade, prioridade e estado ficam para o analista (decisão 104). O relatório v2 continua para as corridas gravadas. Os 40 verbetes da biblioteca de produção não mudaram; nasceu uma camada de leitura fora dela (`Programacao/AgenteCore/biblioteca_producao_leitura/`), gerada do frontmatter e das seções do verbete e curada à mão, que é o que o relatório, a árvore e o hub citam (decisão 103). A busca e o prompt continuam lendo a biblioteca.<!-- fonte: decisoes.md, decisões 103 e 104 -->

**Resultado.** Cada caso do hub abre com o relatório em 17 blocos: 11 campos da seção 5.5 e 6 do que o agente fez.<!-- fonte: hub.md, parágrafo de abertura --> Os relatórios v3 foram regerados das trilhas gravadas das corridas 18d (74), 21d (10) e 24 (36), sem corrida nova.<!-- fonte: texto.md, tb_f4_texto_resumo, coluna Textos -->

**Limite.** A camada de leitura é uma leitura, não um verbete: o modelo não a vê. Mudar o que o modelo lê obrigaria a medir de novo (decisões 69 e 95). O que o syllabus chama de causa-raiz (o motivo fundamental, que pode ser humano ou de processo) fica fora do alcance do agente, que nomeia a causa entre as 23 categorias da biblioteca.<!-- fonte: plano-aprovado-pos-fase-4.md, seção 4, item 2 -->

### 3.2 Q2: filtros de texto em código

**O que foi feito.** `filtros_de_texto.py`, só com a biblioteca padrão, mede qualquer texto que chega ao analista com oito medidas: palavras por frase, Flesch adaptado ao português (índice de facilidade de leitura; abaixo de 50 só acende alarme), preenchimento por lista fechada, repetição interna, taxa de compressão, jargão e sigla sem expansão na primeira menção, densidade de termos do domínio e tamanho (este nunca como critério, porque o tamanho infla a nota de qualquer juiz-modelo). Os limiares calibrados vêm do percentil 95 do corpus de referência e são declarados como calibração.<!-- fonte: texto.md, parágrafo de abertura; plano-aprovado-pos-fase-4.md, seção 3.3 -->

**Resultado.** Antes, nenhum relatório v2 das três corridas passava em tudo; depois, todos os v3 passam, e as 39 leituras dos verbetes passam todas, contra 14 dos 39 verbetes originais.<!-- fonte: texto.md, tb_f4_texto_resumo, colunas Passam em tudo antes e depois -->

<!-- tabela:tb_f4_texto_resumo -->
| Grupo | Textos | Passam em tudo antes | Passam em tudo depois | Alarme do Flesch antes | Alarme do Flesch depois | Termos sem expansão antes (ocorrências) | Termos sem expansão depois (ocorrências) | Palavras antes (mediana) | Palavras depois (mediana) | De onde vem o antes |
|---|---|---|---|---|---|---|---|---|---|---|
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | 74 | 0 (0,0%) | 74 (100,0%) | 74 | 0 | 333 | 0 | 354 | 1030 | v2 gravado em 74 e regerado da trilha em 0 |
| corrida 21d (ensaio dos cenários da Fase 5) | 10 | 0 (0,0%) | 10 (100,0%) | 10 | 0 | 40 | 0 | 380 | 1104 | v2 gravado em 10 e regerado da trilha em 0 |
| corrida 24 (os 36 inéditos em texto) | 36 | 0 (0,0%) | 36 (100,0%) | 35 | 0 | 180 | 0 | 294 | 930 | v2 gravado em 0 e regerado da trilha em 36 |
| verbetes da biblioteca de produção e a camada de leitura | 39 | 14 (35,9%) | 39 (100,0%) | 15 | 3 | 12 | 0 | 95 | 277 | leitura gerada por biblioteca_leitura.py |
<!-- /tabela:tb_f4_texto_resumo -->

<!-- tabela:tb_f4_texto_medias -->
| Grupo | Versão | Textos | Passam em tudo | Alarme do Flesch | Palavras por frase (média) | Palavras por frase (máximo, média dos textos) | Flesch | Preenchimento | Repetição | Compressão | Termos sem expansão (média) | Densidade do domínio | Palavras (mediana) | Trechos em código (média) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | relatório v2 | 74 | 0 (0,0%) | 74 (100,0%) | 14,73 | 57,9 | 37,4 | 0,0000 | 0,0300 | 1,278 | 4,50 | 0,3410 | 354 | 36,7 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | relatório v3 | 74 | 74 (100,0%) | 0 (0,0%) | 15,98 | 50,7 | 64,9 | 0,0000 | 0,0110 | 1,201 | 0,00 | 0,2990 | 1030 | 109,7 |
| corrida 21d (ensaio dos cenários da Fase 5) | relatório v2 | 10 | 0 (0,0%) | 10 (100,0%) | 16,27 | 63,0 | 36,3 | 0,0000 | 0,0380 | 1,272 | 4,00 | 0,3490 | 380 | 45,8 |
| corrida 21d (ensaio dos cenários da Fase 5) | relatório v3 | 10 | 10 (100,0%) | 0 (0,0%) | 15,58 | 49,2 | 64,6 | 0,0000 | 0,0160 | 1,203 | 0,00 | 0,2980 | 1104 | 129,8 |
| corrida 24 (os 36 inéditos em texto) | relatório v2 | 36 | 0 (0,0%) | 35 (97,2%) | 13,95 | 52,2 | 36,6 | 0,0000 | 0,0360 | 1,295 | 5,00 | 0,3500 | 294 | 34,1 |
| corrida 24 (os 36 inéditos em texto) | relatório v3 | 36 | 36 (100,0%) | 0 (0,0%) | 15,71 | 50,3 | 62,8 | 0,0000 | 0,0100 | 1,190 | 0,00 | 0,3070 | 930 | 95,0 |
| verbetes da biblioteca de produção e a camada de leitura | verbete | 39 | 14 (35,9%) | 15 (38,5%) | 16,00 | 29,3 | 54,1 | 0,0010 | 0,0480 | 1,293 | 0,31 | 0,1500 | 95 | 0,0 |
| verbetes da biblioteca de produção e a camada de leitura | leitura | 39 | 39 (100,0%) | 3 (7,7%) | 14,26 | 32,2 | 57,8 | 0,0000 | 0,0050 | 1,195 | 0,00 | 0,2790 | 277 | 28,4 |
<!-- /tabela:tb_f4_texto_medias -->

**Como ler.** Cada linha é um grupo de textos; "antes" é o que existia (relatório v2 ou verbete) e "depois" é o v3 ou a leitura. Palavras por frase, preenchimento e repetição: menor é melhor. Flesch: maior é mais fácil de ler.

**Limite.** O limiar de palavras por frase calibrado no corpus (percentil 95) é bem maior do que os valores que o plano antecipou, porque os textos "! Motivo:" do corpus são quase sempre uma frase só, encadeada por ponto e vírgula e dois-pontos; o Eric aceitou o limiar calibrado (decisão 108, desvio 1), e a conta com os valores antecipados fica na leitura como segunda conta.<!-- fonte: plano-aprovado-pos-fase-4.md, anexo, desvio 1; decisoes.md, decisão 108 --> Os filtros dizem se o texto é curto e sem jargão; não dizem se ele é verdadeiro.

### 3.3 Q3: a árvore de decisão

**O que foi feito.** `arvore_de_decisao.py` lê a trilha v2 de um caso e emite a árvore em Markdown e em JSON, um nó por decisão do agente: o que o modelo lê (a poda), que verbetes entram, a causa escolhida contra a segunda e as demais, e a cura, quando houve. Cada afirmação leva um rótulo de origem: observado (o código mediu), conferido (o código checou o que o modelo disse), declarado (o modelo escreveu, sem garantia) e desconhecido (faltou dado; nunca vira percentual). A confiança sai em palavras (alta, média, baixa), com a taxa de acerto histórica da faixa (decisões 109 e 110).<!-- fonte: plano-aprovado-pos-fase-4.md, seção 3.4; decisoes.md, decisões 109 e 110 -->

**Resultado.** Na corrida 24, as 36 árvores têm 861 afirmações: 538 observadas, 215 conferidas e 108 declaradas; 10 árvores têm divergência entre o declarado e o conferido, e nenhuma teve cura de localizador.<!-- fonte: INDICE.md, fase4_ineditos/arvores, segundo parágrafo --> No hub, que junta quatro corridas, 43 casos têm divergência e 24 tiveram cura.<!-- fonte: hub.md, parágrafo de abertura -->

**Limite.** A árvore não separa, dentro da busca por palavras, o que veio do contrato, da referência e do sintoma, porque a trilha v2 não guarda a contribuição de cada termo; gravar isso mudaria o que o agente grava, o que a fase não faz (desvio 2).<!-- fonte: plano-aprovado-pos-fase-4.md, anexo, desvio 2 -->

### 3.4 Q4: a barra de progresso e o protótipo da seleção pelo Git

**Barra.** `progresso.py` estima o tempo restante de cada inferência em duas fases, com as taxas gravadas das respostas anteriores do mesmo modelo nesta máquina: o prefill (o modelo lendo o prompt) e a geração (o modelo escrevendo a resposta). A chamada ao modelo não é em fluxo, então a geração não é corrigida token a token (desvio 3, decisão 111).<!-- fonte: plano-aprovado-pos-fase-4.md, anexo, desvio 3 -->

<!-- tabela:tb_f4_progresso_taxas_qwen2_5_7b -->
| Medida | Mediana | P10 | P90 | Mínimo | Máximo | n | De onde vem |
|---|---|---|---|---|---|---|---|
| prefill (tokens por segundo) | 26,033 | 20,111 | 49,430 | 19,450 | 5918,803 | 120 | tokens_entrada / (prefill_ms / 1000) de cada registro em <corrida>/<modelo>/diagnosticos__*.jsonl das corridas vigentes |
| geração (tokens por segundo) | 4,283 | 4,191 | 4,338 | 3,446 | 4,475 | 120 | tokens_saida / (geracao_ms / 1000) de cada registro em <corrida>/<modelo>/diagnosticos__*.jsonl das corridas vigentes |
| tokens do prompt | 1189,000 | 1100,400 | 1376,900 | 1027,000 | 1580,000 | 120 | tokens_entrada de cada registro em diagnosticos__*.jsonl (a contagem real do prompt feita pelo Ollama) |
| tokens gerados | 63,000 | 56,000 | 75,000 | 45,000 | 88,000 | 120 | tokens_saida de cada registro em diagnosticos__*.jsonl (o que o modelo escreveu de fato, abaixo do teto) |
| caracteres por token do prompt | 3,120 | 3,056 | 3,194 | 2,986 | 3,346 | 120 | chars do evento prompt / tokens_entrada do evento inferencia (mesmo pai) da trilha v2 de cada corrida |
| carga do modelo (ms) | 32,000 | 28,000 | 37,100 | 13,000 | 9064,000 | 120 | carga_ms de cada registro em diagnosticos__*.jsonl (quase zero com o modelo residente; segundos na primeira chamada) |
<!-- /tabela:tb_f4_progresso_taxas_qwen2_5_7b -->

<!-- tabela:tb_f4_progresso_erro_fora_da_corrida_qwen2_5_7b -->
| Fase | n | Erro mediano (s) | Erro absoluto mediano (s) | Erro absoluto P90 (s) | Erro relativo mediano | Subestimadas |
|---|---|---|---|---|---|---|
| prefill | 120 | 0,1 | 9,9 | 23,2 | 18,7% | 59 de 120 |
| geração | 120 | -0,0 | 1,1 | 3,3 | 7,8% | 61 de 120 |
| prefill mais geração | 120 | -0,7 | 10,3 | 23,1 | 16,2% | 64 de 120 |
| tempo de relógio da chamada | 120 | -3,1 | 11,4 | 22,3 | 16,8% | 67 de 120 |
<!-- /tabela:tb_f4_progresso_erro_fora_da_corrida_qwen2_5_7b -->

**Como ler.** A primeira tabela é a taxa do modelo medida em 120 registros das corridas vigentes. A segunda é o erro da estimativa quando a barra usa as taxas das outras corridas (o que ela veria numa corrida nova): erro negativo quer dizer que a barra acabaria antes do real. O erro mediano de prefill mais geração ficou em 10,3 s absolutos, ou 16,2% do tempo.<!-- fonte: erro_progresso.md, tb_f4_progresso_erro_fora_da_corrida_qwen2_5_7b, linha prefill mais geração -->

<!-- tabela:tb_f4_progresso_fumaca -->
| Fase | n | Erro mediano (s) | Erro absoluto mediano (s) | Erro absoluto P90 (s) | Erro relativo mediano | Subestimadas |
|---|---|---|---|---|---|---|
| prefill | 1 | -0,0 | 0,0 | 0,0 | 0,1% | 1 de 1 |
| geração | 1 | 2,3 | 2,3 | 2,3 | 18,9% | 0 de 1 |
| prefill mais geração | 1 | 2,3 | 2,3 | 2,3 | 3,9% | 0 de 1 |
| tempo de relógio da chamada | 1 | -8,3 | 8,3 | 8,3 | 11,9% | 1 de 1 |
<!-- /tabela:tb_f4_progresso_fumaca -->

<!-- tabela:tb_f4_progresso_fumaca_inferencias -->
| Etapa | Tokens do prompt (estimados / reais) | Prefill estimado / medido (s) | Resposta estimada / medida (s) | Total estimado / medido (s) | Tempo de relógio (s) | Tokens gerados |
|---|---|---|---|---|---|---|
| lex-22 · diagnóstico | 1224 / 1204 | 47,0 / 47,1 | 14,7 / 12,4 | 61,7 / 59,4 | 70,0 | 55 |
<!-- /tabela:tb_f4_progresso_fumaca_inferencias -->

**Fumaça real.** Uma inferência de verdade, rodada na janela do Eric: o prefill estimado deu 47,0 s contra 47,1 s medidos, e o relógio marcou 70,0 s porque a carga do modelo (primeira chamada) não entra na estimativa.<!-- fonte: fumaca_progresso.md, tb_f4_progresso_fumaca_inferencias -->

**Seleção pelo Git (protótipo).** `impacto_git.py` cruza os arquivos alterados entre dois commits com os campos `arquivos:` e `endpoints:` dos verbetes e com as rotas dos cenários, e diz quais cenários rodar, sem modelo. O mapa liga 6 cenários base (10 do ensaio da Fase 5) e 39 verbetes a 33 arquivos da aplicação. Nos 8 pares de commits consecutivos que mexeram nas cobaias, a seleção rodaria tudo em 3, parte dos cenários em 3 e nada em 2.<!-- fonte: impacto_git.md, parágrafo de abertura --> As três regras vêm da literatura de seleção de testes e do Azure DevOps: arquivo fora do mapa roda tudo, nunca nada; a rodada completa volta em prazo fixo; e o que a seleção deixou de rodar é conferido contra a rodada completa.

<!-- tabela:tb_f4_impacto_pares -->
| Commit testado | Commit atual | Data | Assunto | Alterados | Fora da aplicação | Ignorados | No mapa | Fora do mapa | Veredito | Cenários selecionados | Deixados de fora |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `e854a0eb` | `ab4da6a1` | 2026-08-31 | Estrutura Base Auxiliada por IA - Claude - PT1 | 3873 | 10 | 3844 | 14 | 5 | roda tudo | api-catalogo, api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva | nenhum |
| `ab4da6a1` | `26432d2c` | 2026-08-31 | Parte 2 | 1762 | 10 | 1752 | 0 | 0 | nada a rodar | nenhum | api-catalogo, api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva |
| `26432d2c` | `084fce09` | 2026-09-01 | Correção comentários e nomenclatura normalizada | 21 | 8 | 1 | 9 | 3 | roda tudo | api-catalogo, api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva | nenhum |
| `084fce09` | `603c423e` | 2026-09-03 | Teste 1 Concluído, resultados, relatórios e refatoração geral + refatoração da documentação + inicio da preparaçãod a fase 2 de testes | 106 | 102 | 1 | 3 | 0 | seleção parcial | api-catalogo | api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva |
| `603c423e` | `3e8cfc14` | 2026-10-23 | Ajuste de gitignore com retirada de informações da venv e continuações das pesquisas pré fase 4 | 4381 | 2269 | 2112 | 0 | 0 | nada a rodar | nenhum | api-catalogo, api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva |
| `3e8cfc14` | `4f3b3e26` | 2026-10-27 | Fase 4 - Inicialização | 240 | 237 | 1 | 2 | 0 | seleção parcial | api-catalogo, api-detalhe | front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva |
| `4f3b3e26` | `633ebb27` | 2026-11-03 | Fase 4 - Inicio das rodadas + ajustes de parâmetros | 555 | 550 | 0 | 5 | 0 | seleção parcial | api-catalogo, api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva | nenhum |
| `633ebb27` | `717f68c2` | 2026-11-12 | Pós Parte 4 - Rodadas Q1 a Q4 + Refatoração dos painéis de dados e documentação | 2219 | 2218 | 0 | 0 | 1 | roda tudo | api-catalogo, api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva | nenhum |
<!-- /tabela:tb_f4_impacto_pares -->

**Limite.** O mapa é escrito à mão e aproximado, como o do Azure DevOps. A ponte por documentação em linguagem natural (verbete ligado a arquivo) não tem respaldo direto na literatura: é desenho nosso.<!-- fonte: plano-aprovado-pos-fase-4.md, seção 3.7 --> Os demais blocos da leitura (o mapa dos cenários e a explicação par a par) ficam só em `impacto_git.md`.

### 3.5 Q5: a revisão humana dos relatórios e a curadoria das 39 leituras

**O que foi feito.** Os 36 relatórios v3 da corrida 24, com a árvore, foram lidos por um analista de QA da empresa em que o Eric trabalha (decisão 117). O nome do caso, a classe e o nível ficaram escondidos. A revisão não foi feita pelo Eric: ele passou os relatórios ao analista e digitou ou colou as respostas na página. Por isso o tempo até a decisão entra como não medido: o que a página mediu foi a troca entre os dois, não uma leitura com o relatório à vista.<!-- fonte: leitura_revisao_v3.md, segundo parágrafo; decisoes.md, decisão 117 -->

**Resultado.** A adesão apropriada (aceitar o diagnóstico certo e recusar o errado) foi de 30 dos 36 relatórios, 83,3%, com intervalo de Wilson (faixa de 95% de confiança para uma proporção) de 68,1 a 92,1; o erro foi localizado em 10 dos 11 diagnósticos errados; a utilidade mediana foi 5,0.<!-- fonte: leitura_revisao_v3.md, tb_f4_revisao_v3_resumo -->

<!-- tabela:tb_f4_revisao_v3_resumo -->
| Relatórios | Com resposta do Eric, lendo na página | Com resposta de um analista, digitada ou colada pelo Eric | Diagnósticos certos | Diagnósticos errados | Adesão apropriada | Adesão (%) | Wilson 95% | Tempo mediano (s) | Erros achados | Utilidade mediana |
|---|---|---|---|---|---|---|---|---|---|---|
| 36 | 0 | 36 | 25 | 11 | 30 | 83,3 | 68,1 a 92,1 | não medido | 10 de 11 | 5,0 |
<!-- /tabela:tb_f4_revisao_v3_resumo -->

<!-- tabela:tb_f4_revisao_v3_adesao -->
| Grupo | Relatórios | Aceitou | Recusou | Apropriadas | Apropriadas (%) | Wilson 95% |
|---|---|---|---|---|---|---|
| diagnóstico certo | 25 | 20 | 5 | 20 | 80,0 | 60,9 a 91,1 |
| diagnóstico errado | 11 | 1 | 10 | 10 | 90,9 | 62,3 a 98,4 |
| todos | 36 | 21 | 15 | 30 | 83,3 | 68,1 a 92,1 |
<!-- /tabela:tb_f4_revisao_v3_adesao -->

<!-- tabela:tb_f4_revisao_v3_localizacao -->
| Grupo | Relatórios | Achou um erro | Não achou | Não viu erro | Achou (%) | Wilson 95% |
|---|---|---|---|---|---|---|
| diagnóstico errado | 11 | 10 | 0 | 1 | 90,9 | 62,3 a 98,4 |
| diagnóstico certo | 25 | 5 | 0 | 20 | 20,0 | 8,9 a 39,1 |
<!-- /tabela:tb_f4_revisao_v3_localizacao -->

**Como ler.** "Aceitou" e "Recusou" são a decisão do analista sobre o diagnóstico; "apropriada" é aceitar o certo ou recusar o errado. Os diagnósticos certos que ele recusou são, em boa parte, respostas fora dos verbetes entregues, que ele tratou como erro do agente.

**Curadoria das 39 leituras.** O analista aprovou 13 leituras como estavam e reescreveu 26; o Claude fez 77 trocas em 26 leituras onde havia fato errado ou formato quebrado, cada uma com o motivo, o antes e o depois em `curadoria_leituras/consertos.md`. Nenhum verbete da biblioteca mudou.<!-- fonte: decisoes.md, decisão 115 -->

**Limites.** Um só leitor, que não é o autor; uso de ferramenta de IA por ele não foi declarado, nem o que ele recebeu para ler; o tempo não foi medido. A medida com o tempo, num revisor do grupo lendo na página, continua possível e não foi feita (desvio 4).<!-- fonte: leitura_revisao_v3.md, segundo parágrafo; plano-aprovado-pos-fase-4.md, anexo, desvio 4 -->

### 3.6 O parecer do analista e a corrida 25 (a biblioteca sem as notas do modelo)

O analista de QA também escreveu um parecer sobre o projeto (`parecer-do-analista-2026-11-10.md`). Parte dele assume premissas que não são as do projeto (modelo de código, busca vetorial, treinamento); o que procede é que as notas que o modelo escreveu na biblioteca ficaram em forma de instrução, justamente no texto que o modelo lê.<!-- fonte: parecer-do-analista-2026-11-10.md, texto do parecer --> Daí a corrida 25 (decisão 116): a biblioteca de produção sem as notas do modelo e sem os verbetes aprendidos, lendo em texto os 72 casos (36 oficiais e 36 inéditos), pareados com o diagnóstico que a biblioteca inteira deu a cada um. A regra do veredito foi fixada antes da corrida: a diferença sai do ruído quando o teste pareado exato de McNemar (compara só os casos que mudaram de acerto para erro e de erro para acerto) dá p abaixo de 0,05.<!-- fonte: sem_notas.md, parágrafos de abertura -->

<!-- tabela:tb_f4_semnotas_resumo -->
| Casos | Acertos sem as notas | Acerto sem as notas (%) | Wilson 95% | Acertos na referência | Acerto na referência (%) | Passaram a acertar (b) | Passaram a errar (c) | Saldo | p do teste pareado | Mesmo rótulo | Tokens de entrada (mediana) sem as notas | Tokens de entrada (mediana) na referência | Segundos (mediana) sem as notas | Segundos (mediana) na referência | Veredito |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 72 | 54 | 75,0 | 63,9 a 83,6 | 56 | 77,8 | 2 | 4 | -2 | 0,688 | 64 | 1087,5 | 1181,0 | 57,63 | 66,35 | dentro do ruído |
<!-- /tabela:tb_f4_semnotas_resumo -->

<!-- tabela:tb_f4_semnotas_banco -->
| Banco | Referência | Casos | Acertos sem as notas | Acertos na referência | Passaram a acertar (b) | Passaram a errar (c) | p do teste pareado | Mesmo rótulo | Verbete certo entre os entregues, sem as notas | Verbete certo entre os entregues, na referência | Quais passaram a acertar | Quais passaram a errar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| os 36 oficiais de avaliação | corrida 22 | 36 | 30 | 31 | 1 | 2 | 1,000 | 31 | 30 | 30 | `sin-14` | `efe-3`, `run-10` |
| os 36 inéditos da ficha 27 | corrida 24 | 36 | 24 | 25 | 1 | 2 | 1,000 | 33 | 20 | 20 | `run-26` | `sin-27`, `tra-24` |
<!-- /tabela:tb_f4_semnotas_banco -->

**Como ler.** "b" são os casos que passaram a acertar sem as notas, "c" os que passaram a errar. Sem as notas o agente acertou 54 de 72 casos, contra 56 com a biblioteca inteira (b = 2, c = 4, p = 0,688): dentro do ruído, e o agente não muda.<!-- fonte: sem_notas.md, tb_f4_semnotas_resumo -->

**Limite.** A corrida rodou numa versão do Ollama diferente das corridas de referência; a ponte dessa versão (b = 1, c = 0 em 35 casos) ficou pareável com a Fase 3. No relançamento de 16/11/2026 a corrida regravou as condições com outra versão do Ollama; isso foi consertado e os arquivos voltaram ao estado do commit `717f68c2`.<!-- fonte: sem_notas.md, parágrafo do veredito; roadmap.md, §2.23 -->

### 3.7 A corrida 26: o segundo passe do diagnóstico

**O que foi feito.** Só nos casos das corridas 22 e 24 em que um sinal em código acendeu na primeira resposta (o selo baixo ou a FONTE divergente), o agente recebeu um segundo pedido de diagnóstico, uma única vez, com os três verbetes seguintes da mesma busca. A resposta final era escolhida por uma regra em código fixada antes da corrida (decisão 120).<!-- fonte: segundo_passe.md, parágrafos de abertura -->

<!-- tabela:tb_f4_segpasse_resumo -->
| Casos | Com sinal | Segundos passes feitos | Acertos da primeira resposta | Acertos da resposta final | A segunda consertaria | A segunda estragaria | Mesma causa nas duas | Trocas pela regra | Passaram a acertar (b) | Passaram a errar (c) | Saldo | p do teste pareado | Tokens de entrada (mediana) no segundo pedido | Tokens de entrada (mediana) no primeiro | Acima do limite de tokens | Segundos (mediana) no segundo pedido | Veredito |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 72 | 24 | 24 | 56 | 54 | 2 | 6 | 11 | 8 | 1 | 3 | -2 | 0,625 | 1260 | 1185 | 2 | 67,53 | dentro do ruído |
<!-- /tabela:tb_f4_segpasse_resumo -->

<!-- tabela:tb_f4_segpasse_sinal -->
| Sinal aceso na primeira resposta | Casos com segundo passe | Erros na primeira resposta | Acertos na primeira resposta | A segunda consertaria | A segunda estragaria | Mesma causa nas duas | Trocas pela regra | Passaram a acertar (b) | Passaram a errar (c) |
|---|---|---|---|---|---|---|---|---|---|
| só o selo baixo | 12 | 5 | 7 | 1 | 4 | 4 | 5 | 0 | 3 |
| só a FONTE divergente | 9 | 3 | 6 | 0 | 2 | 6 | 1 | 0 | 0 |
| os dois sinais | 3 | 2 | 1 | 1 | 0 | 1 | 2 | 1 | 0 |
<!-- /tabela:tb_f4_segpasse_sinal -->

<!-- tabela:tb_f4_segpasse_regras -->
| Se a escolha fosse | Trocas de causa | Passariam a acertar (b) | Passariam a errar (c) | Acertos nos casos todos | p do teste pareado |
|---|---|---|---|---|---|
| sempre a primeira (o agente de hoje) | 0 | 0 | 0 | 56 | 1,000 |
| sempre a segunda | 13 | 2 | 6 | 52 | 0,289 |
| a de maior probabilidade, sem olhar os sinais | 9 | 1 | 3 | 54 | 0,625 |
| a regra fixada antes da corrida | 8 | 1 | 3 | 54 | 0,625 |
<!-- /tabela:tb_f4_segpasse_regras -->

**Resultado.** Dos 24 casos com sinal, a segunda resposta consertaria 2 dos 10 erros e estragaria 6 dos 14 acertos; pela regra de escolha, o agente iria de 56 a 54 acertos em 72 (p = 0,625): dentro do ruído, contra o segundo passe. O segundo pedido custou, na mediana, 67,53 s por caso.<!-- fonte: segundo_passe.md, tb_f4_segpasse_resumo e parágrafo do resultado -->

### 3.8 A medida M1, a corrida 27 (analista de documentação) e a revisão às cegas

**O que foi feito.** A proposta do analista de documentação põe o modelo, depois do diagnóstico, num segundo papel: propor uma edição de verbete, que passa por cinco portões em código antes de uma pessoa julgar (decisão 121). A **M1** (sem modelo) aplicou os portões 3, 4 e 5 às propostas da corrida 20; a **corrida 27** (a M2) chamou o modelo no papel de analista nos 54 casos de aprendizado, com as instruções congeladas (decisão 122).<!-- fonte: portoes_m1.md, parágrafo de abertura; analista.md, parágrafo de abertura; decisoes.md, decisão 122 -->

**M1.** Na corrida 20 o modelo fez 92 propostas de edição em 54 casos; 20 passaram nos filtros de então e a revisão humana julgou 2 corretas, 9 parciais e 9 erradas. Os três portões em sequência deixam 1 edição, errada; o portão da forma de instrução recusaria 86 das 92 propostas e perderia as 2 corretas.<!-- fonte: portoes_m1.md, tb_f4_portoes_resumo e parágrafos de resultado -->

<!-- tabela:tb_f4_portoes_resumo -->
| Propostas | Casos | Revisadas por uma pessoa | Corretas | Parciais | Erradas | O portão 3 recusaria | O portão 4 recusaria | O portão 5 recusaria (das revisadas) | Sobram depois dos três | Sobram sem o portão da forma |
|---|---|---|---|---|---|---|---|---|---|---|
| 92 | 54 | 20 | 2 | 9 | 9 | 86 | 11 | 4 | 1 | 15 |
<!-- /tabela:tb_f4_portoes_resumo -->

<!-- tabela:tb_f4_portoes_sequencia -->
| Etapa | Edições que sobram | Corretas | Parciais | Erradas |
|---|---|---|---|---|
| passaram nos filtros de hoje e foram revisadas | 20 | 2 | 9 | 9 |
| depois do portão 3 (forma de instrução) | 2 | 0 | 1 | 1 |
| depois do portão 4 (filtros de texto) | 2 | 0 | 1 | 1 |
| depois do portão 5 (busca) | 1 | 0 | 0 | 1 |
| só os portões 4 e 5, sem o da forma | 15 | 1 | 8 | 6 |
| só o portão 5, o da busca | 16 | 2 | 8 | 6 |
<!-- /tabela:tb_f4_portoes_sequencia -->

**Corrida 27.** O analista respondeu em 54 casos: 0 abstenções, 20 respostas sem proposta válida e 34 propostas. Das 15 propostas com texto, 14 afirmam um fato e passam no portão da forma, contra 6 de 92 na corrida 20; passam nos filtros de hoje 8 (contra 20 de 92 na corrida 20).<!-- fonte: analista.md, parágrafo O que o analista respondeu em 54 casos -->

<!-- tabela:tb_f4_analista_resumo -->
| Casos | Abstenções | Sem proposta válida | Propostas | Sinais de busca | Notas | Retificações | Com texto | Afirmam um fato | Passam nos filtros de hoje | Passam nos cinco portões | Cópias do exemplo das instruções | Tokens lidos (mediana) | Tokens escritos (mediana) | Segundos (mediana) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 54 | 0 | 20 | 34 | 19 | 15 | 0 | 15 | 14 | 8 | 4 | 1 | 1153,5 | 110 | 49,36 |
<!-- /tabela:tb_f4_analista_resumo -->

<!-- tabela:tb_f4_analista_leituras -->
| Leitura | Corrida 27 | Corrida 20 | Teste | p | Veredito |
|---|---|---|---|---|---|
| abstenção | 0 de 54 | 0 de 54 | McNemar pareado por caso | 1,000 | dentro do ruído |
| forma do texto | 14 de 15 | 6 de 92 | Fisher | 0,000 | sai do ruído: mais afirmações na corrida 27 |
| parcela correta | 3 de 8 | 1 de 20 | Fisher | 0,058 | dentro do ruído |
<!-- /tabela:tb_f4_analista_leituras -->

<!-- tabela:tb_f4_analista_destino -->
| O que aconteceu com a resposta | Casos |
|---|---|
| abstenção | 0 |
| sem proposta válida | 20 |
| recusada pelo validador da Fase 3 | 8 |
| recusada pelos filtros da Fase 4 | 18 |
| recusada pela forma de instrução | 0 |
| recusada pelos filtros de texto | 0 |
| recusada pelo portão da busca | 4 |
| passa nos cinco portões | 4 |
<!-- /tabela:tb_f4_analista_destino -->

**Revisão às cegas.** As propostas da corrida 27 que passam nos filtros de hoje foram misturadas às 20 edições revisadas da corrida 20, em ordem embaralhada e sem a origem, e julgadas por um analista de QA da empresa em que o Eric trabalha (o mesmo da seção 3.5), que viu só o que a página mostra, sem abrir o repositório nem a chave da origem. Os comentários foram escritos por ele fora da página e colados depois; nenhuma ferramenta de IA os redigiu, pela declaração dele. Foram 28 itens, todos com veredito. A revisão não foi feita pelo Eric (decisão 129, que revê a 123).<!-- fonte: quem_revisou.json, quem, o_que_tinha_a_mao e comentarios; revisao_as_cegas.md, parágrafo de abertura; decisoes.md, decisão 129 --> Das 8 propostas da corrida 27 julgadas, 3 ficaram corretas, 4 parciais e 1 errada; as edições da corrida 20, julgadas de novo sem a origem, ficaram em 1 correta, 9 parciais e 10 erradas.<!-- fonte: analista.md, parágrafo A revisão humana às cegas -->

**Resultado.** A forma do texto melhorou de modo que sai do ruído (teste exato de Fisher, que compara duas proporções). A parcela correta, 3 de 8 contra 1 de 20, ficou dentro do ruído (p = 0,058).<!-- fonte: analista.md, tb_f4_analista_leituras --> Nenhum resultado muda o agente: a proposta é base de desenho para depois da Fase 5.<!-- fonte: decisoes.md, decisão 121 -->

**Limites.** Com 8 propostas julgadas, a parcela correta tem pouco poder para separar as duas corridas; o revisor é um só; e a corrida rodou numa versão do Ollama diferente da corrida 20, com a ponte pareável (b = 1, c = 0 em 35 casos).<!-- fonte: analista.md, parágrafo da ponte -->

### 3.9 O painel por fase (decisão 124)

A pedido do Eric em 11/11/2026, o painel do projeto passou a ser organizado por fase: o Roadmap mostra um cartão em linha por fase, cada fase tem uma aba de visão com o caminho em passos, o que ela mostrou, os tópicos e as corridas, o Início virou o resumo do projeto, os termos e métodos são explicados onde aparecem (glossário com resumo, diferença do projeto e fonte) e o texto do painel fala do grupo, não do nome do autor.<!-- fonte: decisoes.md, decisão 124 --> O plano não previa isso (desvio 7).<!-- fonte: plano-aprovado-pos-fase-4.md, anexo, desvio 7 -->

### 3.10 Q6: o hub central

**O que foi feito.** Uma aplicação local, servida só em 127.0.0.1 por `http.server` da biblioteca padrão, à imagem da revisão de uma pull request: lista de casos com filtros, o relatório v3 com a evidência ao lado, a árvore de decisão, a trilha, comentário preso ao trecho, comentário geral, veredito do analista em cinco valores, os campos de severidade, prioridade e estado da seção 5.5, a sugestão "a causa é outra" e as iterações do mesmo caso com "o que mudou". O agente só comenta, nunca aprova. A revisão fica em um arquivo JSONL por caso, fora da trilha. Entram também o trace do Playwright na falha (a gravação do navegador, passo a passo), a vista "Corrida ao vivo" com a barra de progresso e o botão que lança a corrida, que só funciona com `--permitir-execucao`.<!-- fonte: plano-aprovado-pos-fase-4.md, seção 3.6 e anexo, desvio 9; decisoes.md, decisão 157 -->

<!-- tabela:tb_f4_hub_corridas -->
| Corrida | Pasta | Modo | Modelo | Início | Casos no hub |
|---|---|---|---|---|---|
| corrida 18d | `fase4_tela_v4` | tela | `qwen2.5:7b` | 2026-11-06 | 74 |
| corrida 21d | `fase4_ensaio_v4` | cenarios | `qwen2.5:7b` | 2026-11-06 | 10 |
| corrida 24 | `fase4_ineditos` | ineditos | `qwen2.5:7b` | 2026-11-06 | 36 |
| corrida 28b | `fase5_agente_b` | cenarios | `qwen2.5:7b` | 2026-11-18 | 50 |
<!-- /tabela:tb_f4_hub_corridas -->

**Resultado.** O hub junta 170 casos com diagnóstico de 4 corridas, que são 83 casos distintos: 47 têm mais de uma iteração. O runner `testar_hub.py` tem 44 testes, 11 deles abrindo a página no navegador sem janela.<!-- fonte: hub.md, parágrafo de abertura -->

<!-- ! Alteração de IA - Revisar: (26/11/2026, Pós-Fase 4, pacote Q8) parágrafo novo, "O hub como central", e o parágrafo dos limites passa a contar a corrida curta e o botão.
     ! Motivo: em 25/11/2026 o Eric pediu o hub como central de tudo, aberta quando o `.exe` roda (ficha 109, decisão 170, desvio 16), e a seção só descrevia a página de revisão aberta por comando; o limite do trace dizia "sem as cobaias", o que a corrida curta mudou. -->
**O hub como central.** Em 25/11/2026, depois da corrida curta, o Eric pediu que o hub fosse a central do projeto, aberta quando o `Cobaia.exe` roda, e escolheu no quadro a central completa (ficha 109, decisão 170; desvio 16 do plano). O `run.py` passou a subir o hub junto com o site e a API (`start_hub`), com o Python da venv do AgenteCore, e o `Cobaia.py`, de que sai o `Cobaia.exe`, abre uma aba só, no hub; se o hub não sobe, abre o site e a API, como antes. O hub ganhou a vista "Início" (o que está no ar e os atalhos para o site, a API e o painel) e a vista "Métricas" (por corrida, lida dos registros gravados, com o resultado da Fase 5 no alto e a ressalva do Task Success). Aberto com `--pelo-exe`, ele libera o botão de rodar os dez cenários, e a corrida chama o `executar_fase4.py` com `--cobaias-no-ar`, opção nova e desligada por padrão, que usa o site, a API e o banco já no ar; `python hub.py` sozinho continua só mostrando o comando. O agente medido não muda, e a corrida lançada pela página é uso do produto, não medida do TCC. O runner `testar_central.py` tem 9 testes, sem modelo, sem banco e sem bater nas portas de verdade. O botão não foi visto lançando uma corrida com o modelo: nenhuma corrida com modelo sai de dentro do aplicativo do agente de apoio, e a prova fica para um clique do Eric no `.exe` recompilado.<!-- fonte: pendencias.md, ficha 109; decisoes.md, decisão 170; plano-aprovado-pos-fase-4.md, anexo, desvio 16 -->

**Limites.** O estudo do `visual-explainer` para o hub (decisão 126) está em `estudo-visual-explainer-para-o-hub.md` e rendeu duas ideias aplicadas. O trace foi provado primeiro numa página local que falha de propósito e nos pontos em que o executor o chama, sem as cobaias e sem o banco (desvio 10), e depois na corrida curta de 25/11/2026, com as cobaias e o modelo (seção 3.11). A prova do hub é por teste, não por uso de um analista, e o botão de rodar os cenários não foi provado numa corrida com o modelo.<!-- fonte: plano-aprovado-pos-fase-4.md, anexo, desvio 10 -->

### 3.11 Q7: a seleção de cenários pelo Git

**O que foi feito.** `impacto_git.py` ganhou a decisão para a corrida (`--decidir`), o registro do commit testado, a conferência contra a rodada completa (`--conferir`) e a conta histórica (`--conferir-historico`); `executar_fase4.py` ganhou `--selecao git`, `--desde` e `--completa-a-cada-dias` (prazo da rodada completa periódica, escolha desta implementação: a literatura diz que ela é periódica, sem dar o prazo).<!-- fonte: plano-aprovado-pos-fase-4.md, anexo, desvio 11 -->

**Resultado.** A conferência foi aplicada como conta retrospectiva aos 8 pares de commits do histórico, contra a rodada completa da corrida 28b, na qual 49 das 50 execuções tiveram Task Success (o único cenário com falha foi `contrato-malformed_json`). Dos 8 pares, 3 rodam tudo pela regra 1, 6 não deixam de fora nenhum cenário com falha e 2 deixariam de fora um cenário que falhou na rodada completa: é para esses que existe a regra da rodada completa periódica.<!-- fonte: conferencia_git.md, parágrafo de abertura -->

<!-- tabela:tb_f4_conferencia_pares -->
| Commit testado | Commit atual | Data | Veredito da seleção | Cenários selecionados | Deixados de fora | Falhas perdidas | Segura |
|---|---|---|---|---|---|---|---|
| `e854a0eb` | `ab4da6a1` | 2026-08-31 | roda tudo | 10 | 0 | nenhuma | sim |
| `ab4da6a1` | `26432d2c` | 2026-08-31 | nada a rodar | 0 | 10 | contrato-malformed_json | não |
| `26432d2c` | `084fce09` | 2026-09-01 | roda tudo | 10 | 0 | nenhuma | sim |
| `084fce09` | `603c423e` | 2026-09-03 | seleção parcial | 6 | 4 | nenhuma | sim |
| `603c423e` | `3e8cfc14` | 2026-10-23 | nada a rodar | 0 | 10 | contrato-malformed_json | não |
| `3e8cfc14` | `4f3b3e26` | 2026-10-27 | seleção parcial | 6 | 4 | nenhuma | sim |
| `4f3b3e26` | `633ebb27` | 2026-11-03 | seleção parcial | 10 | 0 | nenhuma | sim |
| `633ebb27` | `717f68c2` | 2026-11-12 | roda tudo | 10 | 0 | nenhuma | sim |
<!-- /tabela:tb_f4_conferencia_pares -->

**Como ler.** "Falhas perdidas" é o cenário que falhou na rodada completa e que a seleção teria deixado de fora; "Segura" é "sim" quando nenhuma falha seria perdida.

**Limite.** Nenhuma das seleções da tabela rodou de verdade, e nenhuma seleção parcial rodou até 26/11/2026: desde o último commit que tocou as cobaias, nada do mapa mudou, e qualquer ponto de partida anterior inclui um arquivo fora do mapa, que manda rodar tudo.<!-- fonte: plano-aprovado-pos-fase-4.md, anexo, desvio 11 -->

<!-- ! Alteração de IA - Revisar: (26/11/2026, Pós-Fase 4, pacote Q8) o parágrafo da corrida curta passa ao resultado lido, e sai a marca de espera.
     ! Motivo: o parágrafo dizia que a corrida curta estava por rodar; ela rodou em 25/11/2026, pela janela do Eric, e a ficha 99 foi fechada com a leitura dos registros da pasta `fase4_fumaca_q7`. -->
**A corrida curta da ficha 99.** A corrida curta que prova o trace do Playwright e a seleção pelo Git com as cobaias (lançador `rodar_fumaca_q7.ps1`, ficha 99, autorizada na decisão 163) rodou em 25/11/2026, pela janela do Eric, e gravou a pasta `resultados_alvo/fase4_fumaca_q7`: os dez cenários, uma execução de cada, com a seleção ligada desde o commit `717f68c2` e o trace na falha ligado. A seleção decidiu a corrida: do commit `717f68c2` ao `35617a47` mudaram 1034 arquivos, nenhum das cobaias, e, como nenhuma rodada completa estava registrada, a regra 2 mandou rodar os 10 cenários, sem deixar nenhum de fora.<!-- fonte: impacto_git.json de fase4_fumaca_q7, campo decisao --> O commit testado entrou no registro (`resultados_alvo/hub/commits_testados.jsonl`), e a decisão seguinte, com ele registrado, é "nada a rodar".<!-- fonte: commits_testados.jsonl; pendencias.md, ficha 99 --> O trace foi gravado em 8 das 10 execuções, as dos cenários em que a conferência do roteiro ou o passo do localizador falhou, cerca de 40 MB ao todo, e em nenhuma das 2 detectadas só pela resposta da API (`contrato-escala_ou_unidade_errada` e `contrato-type_drift`), em que o roteiro passa.<!-- fonte: cenarios.jsonl de fase4_fumaca_q7, campo origem_deteccao; pendencias.md, ficha 110 --> A conferência contra a corrida 28b não tem cenário deixado de fora e tem um resultado diferente: `contrato-malformed_json` teve Task Success aqui e em 4 de 5 execuções lá.<!-- fonte: conferencia_git.json de fase4_fumaca_q7, campo resumo --> As 10 execuções tiveram Task Success; os tempos não valem como medida, porque o trace estava ligado e a corrida é parcial. Continua sem prova uma seleção parcial rodando de verdade (desvio 11).

## 4. O que nenhuma medida mudou no agente

As corridas 25, 26 e 27 ficaram dentro do ruído no que decide: a biblioteca sem as notas do modelo, o segundo passe e o analista de documentação não mudam o agente.<!-- fonte: roadmap.md, §4.8, parágrafo das corridas 25 a 27; decisoes.md, decisões 116, 120 e 121 --> Em cada uma, a regra do veredito foi fixada antes da corrida e dizia que o agente só muda se a diferença sair do ruído, e por outra decisão. O agente das corridas 18d e 21d é, portanto, o que a Fase 5 mediu: a corrida 28b teve 49 execuções com Task Success em 50.<!-- fonte: conferencia_git.md, parágrafo de abertura -->

O que saiu do ruído foi a forma: os filtros de texto, o relatório v3 e a camada de leitura mudaram o que chega ao analista (seção 3.2), e a forma das propostas do analista de documentação melhorou (seção 3.8). Isso é medida do texto, não do acerto do diagnóstico.

## 5. Limitações

<!-- ! Alteração de IA - Revisar: (26/11/2026, Pós-Fase 4, pacote Q8) o item do hub e da seleção pelo Git passa ao que a corrida curta provou e ao limite do botão do hub.
     ! Motivo: o item dizia que a corrida com as cobaias estava pendente; ela rodou em 25/11/2026, e o que continua sem prova é o uso do hub por um analista, o botão lançando uma corrida com o modelo e uma seleção parcial. -->
- **Um leitor humano, que não é do grupo e não é o autor, e sem tempo medido** (seção 3.5): a adesão e a localização do erro têm um leitor só; o tempo até a decisão não foi medido.
- **Revisão às cegas com 8 propostas da corrida 27** (seção 3.8): a parcela correta tem pouco poder estatístico.
- **Versão do Ollama:** as corridas 25, 26 e 27 rodaram numa versão do Ollama diferente das de referência, com a ponte pareável; vale a conferência da ponte, e não uma comparação de tempo.<!-- fonte: sem_notas.md, parágrafo do veredito; segundo_passe.md, parágrafo do veredito -->
- **Filtros medem forma, não verdade** (seção 3.2); o limiar de palavras por frase é calibrado, não de fonte.
- **A árvore não separa os sinais da busca** (seção 3.3).
- **O hub foi provado em teste, sem uso por um analista,** e o botão de rodar os cenários não foi provado numa corrida com o modelo (seção 3.10); **a seleção pelo Git só decidiu uma corrida curta,** em que a regra mandou rodar os dez cenários, e nenhuma seleção parcial rodou (seção 3.11).
- **A barra erra por mais de 10 s na mediana** (10,3 s de erro absoluto em prefill mais geração), e a primeira chamada ainda inclui a carga do modelo (seção 3.4).<!-- fonte: erro_progresso.md, tb_f4_progresso_erro_fora_da_corrida_qwen2_5_7b -->
- **O texto do syllabus CTFL 4.0 não define "E2E" como nível de teste:** o agente é de teste de sistema e de integração de sistema, sobre tarefas de ponta a ponta (plano, parte 2).<!-- fonte: plano-aprovado-pos-fase-4.md, seção 4 -->

## 6. O que o plano previa e não saiu, ou saiu de outro jeito

<!-- ! Alteração de IA - Revisar: (26/11/2026, Pós-Fase 4, pacote Q8) a seção 6 passa a contar os desvios 12 a 16 do anexo do plano, e o parágrafo "Ficou sem data" passa ao estado de 26/11/2026.
     ! Motivo: o anexo do plano ganhou os desvios 12 a 15 no pacote Q8 e o 16 com o hub como central, e a seção parava no 11; o parágrafo final dava o texto do TCC como em andamento. -->
O plano aprovado não muda depois da aprovação; os desvios 1 a 18 estão no anexo dele (`claude-memoria/plano-aprovado-pos-fase-4.md`), com data e decisão. Resumo:<!-- fonte: plano-aprovado-pos-fase-4.md, anexo -->

| Desvio | O que mudou | Decisão |
|---|---|---|
| 1 | O limiar de palavras por frase é o calibrado, não o antecipado | 108 |
| 2 | A árvore não separa contrato, referência e sintoma na busca | 109 e 110 |
| 3 | A geração da barra não é corrigida token a token | 111 |
| 4 | O revisor e a amostra: um analista de QA, os 36 relatórios da corrida 24, tempo não medido | 113, 114 e 117 |
| 5 | A corrida 25, que o plano não previa | 116 |
| 6 | As corridas 26 e 27 e a medida M1, que o plano não previa | 120 a 123 |
| 7 | O painel por fase, a citação do Projeto CHULETA e duas ferramentas lidas | 124 a 128 |
| 8 | O Q6 e o Q7 feitos antes do Q8 | 152 |
| 9 | Um botão só para ativar o agente e rodar os cenários; iteração é cada diagnóstico do mesmo caso | 157 |
| 10 | O trace provado em página local, sem as cobaias | 157 |
| 11 | A conferência da seleção como conta retrospectiva | 152 e 157 |
| 12 | A fase entrou no documento do TCC nas seções 4.1.11, 4.1.12, 5.8, 6.7, 6.10.11 e 6.10.12, e não na 6.9 | nenhuma (pacote Q8) |
| 13 | As figuras: uma que já existia sem uso, duas geradas por script e a captura de tela do hub | nenhuma (pacote Q8) |
| 14 | O Q8 não coube numa sessão: o Word e o PDF esperaram a corrida curta e a segunda execução do instalador | 158 e 168 |
| 15 | O relatório 1 da sessão de revisão de 05/11/2026 foi respondido pelo analista de QA, e não pelo Eric | 166 |
| 16 | O hub como central aberta pelo `Cobaia.exe`, que o plano não previa | 170 |
| 17 | A geração do Word e do PDF passou a esperar a terceira execução do instalador e a prova do botão do hub, com data limite em 30/11/2026 | 172 |
| 18 | A seção 1.1 do documento recebeu o texto de um coautor, e o Word e o PDF finais saem como versão 5 | 173 e 174 |

**Ficou sem data:** a conferência em código que desmente a causa respondida pelo modelo vira regra do agente depois da Fase 5 (decisão 119), e o analista de documentação como regra do agente é base de desenho para depois da Fase 5 (decisão 121); nenhum dos dois tem data. Também ficam sem data a medida do tempo da revisão, num revisor do grupo lendo na página, a prova do botão do hub numa corrida com o modelo e uma seleção parcial rodando de verdade. O texto do TCC está escrito (pacote Q8), e o Word e o PDF saem uma vez só, no fim, com data limite em 30/11/2026 (decisões 158, 168 e 172).<!-- fonte: decisoes.md, decisões 119 e 121 -->

## 7. Rastreabilidade

<!-- ! Alteração de IA - Revisar: (26/11/2026, Pós-Fase 4, pacote Q8) as linhas do plano, das decisões, das fichas e do hub passam ao estado de 26/11/2026, e entra a linha da corrida curta.
     ! Motivo: a tabela parava nos desvios 1 a 11, na decisão 163 e na ficha 99, e não dizia onde estão os registros da corrida curta nem os testes da central. -->
| O quê | Onde |
|---|---|
| Plano e desvios 1 a 18 | `claude-memoria/plano-aprovado-pos-fase-4.md` |
| Decisões 94 a 129, 152, 157, 163, 164 a 168 e 170 a 174 | `Documentacao/memorial/1-decisoes-e-historico/decisoes.md` |
| Fichas 49 a 99, 103 a 107 e 109 a 112 | `Documentacao/memorial/pendencias.md` |
| Roadmap | `Documentacao/memorial/roadmap.md`, §4.8 e §2.23 a §2.25 |
| Filtros de texto (todos os blocos, inclusive critérios, termos e a tabela por texto) | `resultados_alvo/fase4/texto.{json,md}` |
| Revisão humana dos relatórios (os blocos de tempo, utilidade, avaliação e por caso) | `resultados_alvo/fase4/leitura_revisao_v3.{json,md}` |
| Barra de progresso | `resultados_alvo/fase4/taxas_progresso`, `erro_progresso` e `fumaca_progresso` |
| Seleção pelo Git e conferência | `resultados_alvo/fase4/impacto_git` (o mapa dos cenários e o par a par) e `conferencia_git` |
| Corrida 25 (os blocos por mudança, classe e caso) | `resultados_alvo/fase4/sem_notas.{json,md}` |
| Corrida 26 (por banco, alcance, motivos e caso) | `resultados_alvo/fase4/segundo_passe.{json,md}` |
| Medida M1 (os demais blocos) | `resultados_alvo/fase4/portoes_m1.{json,md}` |
| Corrida 27 (portões, lacuna, origem, códigos e caso) | `resultados_alvo/fase4/analista.{json,md}` |
| Revisão às cegas e quem revisou | `resultados_alvo/fase4_analista/revisao_as_cegas.{json,md}` e `quem_revisou.json` |
| Hub | `resultados_alvo/fase4/hub.{json,md}`, `testar_hub.py`, `testar_central.py` (a central), `estudo-visual-explainer-para-o-hub.md` |
| Corrida curta dos pacotes Q6 e Q7 (ficha 99) | `resultados_alvo/fase4_fumaca_q7/` (`impacto_git.json`, `conferencia_git.{json,md}`, `cenarios.jsonl`, `traces/`) e `resultados_alvo/hub/commits_testados.jsonl` |
| Curadoria das 39 leituras | `resultados_alvo/fase4/curadoria_leituras/` e `Programacao/AgenteCore/biblioteca_producao_leitura/` |
| Árvores de decisão e relatórios v3 | `arvores/` e `relatorios_v3/` na pasta de cada corrida (18d, 21d e 24) |
| Parecer do analista | `Documentacao/memorial/3-resultados-e-analises/parecer-do-analista-2026-11-10.md` |
| Colagem e conferência deste relatório | `Programacao/AgenteCore/experimentos/colar_pos_fase4.py` (`--check`) e `testar_relatorio_pos_fase4.py` |
