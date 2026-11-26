<!-- ! Alteração de IA - Revisar: arquivo GERADO por `Programacao/AgenteCore/experimentos/gerar_figuras_documentos.py` (05/11/2026); não editar à mão.
     ! Motivo: cada figura da documentação principal precisa de uma tabela ao lado para quem quer o número exato; saindo do mesmo script, figura e tabela não divergem. -->
# Dados das figuras

Os números de cada figura de [`Documentacao/figuras/`](.), lidos dos registros em `Programacao/AgenteCore/experimentos/resultados_alvo/` pelo script `gerar_figuras_documentos.py`.

## Como o agente trabalha

[Figura](como-o-agente-trabalha.png). Fonte: `fase4/calibracao.json` (`k_escolhido`, `metadados.modelo`).

| Dado | Valor |
|---|---|
| Verbetes entregues ao modelo (k) | 3 |
| Modelo | qwen2.5:7b |

## As peças do agente e por onde os dados passam

[Figura](arquitetura-do-agente.png). Fonte: `run.py` (`FRONT_PORT`, `API_PORT`, `HUB_PORT`), `fase4/calibracao.json` (`k_escolhido`, `metadados.modelo`) e o arquivo de cada peça.

| Peça | O que faz | O que guarda | Onde está no repositório |
|---|---|---|---|
| Aplicações-alvo | O site de demonstração (porta 8080), a API (porta 8000) e o banco de dados, com a falha armada | o banco de dados, restaurado a cada execução | Programacao/CobaiaFront, Programacao/CobaiaAPI, restaurar_banco.py |
| Navegador do agente | Roda o roteiro do cenário na página, com o Chromium do Playwright | nada | Programacao/AgenteCore/experimentos/navegador.py, Programacao/AgenteCore/experimentos/cenarios_fase4.py |
| Interceptador | Grava as chamadas à API e a árvore de acessibilidade da tela enquanto o roteiro roda | nada | Programacao/AgenteCore/experimentos/interceptador.py |
| Poda | Monta o caso com o que mudou contra a tela normal e corta o resto, em código | nada | Programacao/AgenteCore/experimentos/caso_ao_vivo.py, Programacao/AgenteCore/experimentos/poda.py |
| Busca na biblioteca | Escolhe os 3 verbetes mais parecidos com o caso | nada | Programacao/AgenteCore/experimentos/recuperacao.py |
| Biblioteca de produção | Os verbetes de documentação que a busca lê | os verbetes, em arquivos de texto | Programacao/AgenteCore/biblioteca_producao |
| Modelo local | O qwen2.5:7b, pelo Ollama, só com CPU, escolhe a causa numa lista fechada | nada | Programacao/AgenteCore/experimentos/cliente_ollama.py, Programacao/AgenteCore/experimentos/diagnostico_ao_vivo.py |
| Conferência e selo | Confere a resposta do modelo em código e dá o selo de confiança | nada | Programacao/AgenteCore/experimentos/diagnostico_ao_vivo.py |
| Cura do localizador | Acha outro seletor para o elemento e roda o roteiro de novo, sem o modelo | nada | Programacao/AgenteCore/experimentos/cura_seletor.py |
| Trilha | Recebe cada passo: o que o agente viu, o que o modelo respondeu e o que o código conferiu | um arquivo de linhas JSON por corrida | Programacao/AgenteCore/experimentos/trilha.py |
| Relatório e árvore de decisão | Saem da trilha gravada, em código, sem chamar o modelo de novo | os relatórios e as árvores, na pasta de cada corrida | Programacao/AgenteCore/experimentos/gerar_relatorio_raciocinio.py, Programacao/AgenteCore/experimentos/arvore_de_decisao.py |
| Hub central | Página local (porta 8765) em que o analista revê cada caso e dá o veredito | as revisões, num arquivo por caso | Programacao/AgenteCore/experimentos/hub.py |

## O que a documentação fez pelo acerto

[Figura](documentacao-e-acerto.png). Fonte: `fase3/comparacao_fases.json` (`nos_36_avaliacao`: `2B_A0`, `2B_A2`, `F3_L1`, `acerto_pct`).

| Modelo | Sem documentação | Biblioteca escrita à mão | Biblioteca escrita pelo modelo |
|---|---|---|---|
| qwen2.5:7b | 66,7 | 77,8 | 88,9 |
| granite4.2:8b | 72,2 | 80,6 | 80,6 |
| qwen2.5-coder:7b | 41,7 | 72,2 | 75,0 |
| qwen2.5-coder:3b | 19,4 | 69,4 | 72,2 |

## Por que o qwen2.5:7b com a primeira biblioteca dele

[Figura](escolha-do-modelo.png). Fonte: `fase3/decisao_modelo.json` (`regra_36.ranking`, `bootstrap.nos_36`).

| Modelo | Biblioteca | Acurácia balanceada (%) | Segundos por caso (mediana) | De (%) | Até (%) | Escolhido |
|---|---|---|---|---|---|---|
| qwen2.5:7b | L1 | 91,7 | 79,5 | 81,9 | 97,8 | sim |
| qwen2.5:7b | L3 | 86,2 | 53,9 | 75,0 | 96,7 |  |
| qwen2.5:7b | L2 | 84,2 | 80,6 | 72,2 | 94,0 |  |
| qwen2.5-coder:7b | L3 | 84,2 | 56,6 | 70,0 | 91,1 |  |
| granite4.2:8b | L0 | 83,3 | 129,4 | 70,6 | 92,8 |  |
| granite4.2:8b | L1 | 83,3 | 133,2 | 70,6 | 92,8 |  |
| granite4.2:8b | L2 | 83,3 | 131,2 | 70,6 | 92,8 |  |
| granite4.2:8b | L3 | 83,3 | 134,4 | 70,6 | 92,8 |  |
| qwen2.5:7b | L0 | 81,2 | 69,5 | 67,7 | 91,2 |  |
| qwen2.5-coder:7b | L0 | 80,0 | 70,7 | 66,7 | 88,9 |  |
| qwen2.5-coder:7b | L1 | 80,0 | 65,8 | 66,7 | 88,9 |  |
| qwen2.5-coder:7b | L2 | 80,0 | 66,8 | 67,7 | 88,9 |  |
| qwen2.5-coder:3b | L2 | 71,2 | 18,8 | 58,2 | 85,6 |  |
| qwen2.5-coder:3b | L3 | 71,2 | 20,9 | 57,7 | 85,5 |  |
| qwen2.5-coder:3b | L1 | 70,4 | 17,8 | 58,3 | 84,4 |  |
| qwen2.5-coder:3b | L0 | 68,8 | 32,2 | 55,4 | 82,4 |  |

## O que muda quando outro modelo lê a biblioteca

[Figura](quem-le-a-biblioteca.png). Fonte: `fase3/analise_fase3b.json` (`cruzada.celulas`).

| Quem lê | Casos certos com a biblioteca original | Casos certos com a biblioteca escrita pelo qwen2.5:7b | De | Ollama |
|---|---|---|---|---|
| qwen2.5:7b | 28 | 32 | 36 | 0.34.0 |
| qwen2.5-coder:7b | 29 | 30 | 36 | 0.34.4 |
| qwen2.5-coder:3b | 26 | 22 | 36 | 0.34.4 |

## O ganho se repete em casos nunca vistos?

[Figura](casos-ineditos.png). Fonte: `fase3/analise_fase3b.json` (`cruzada.celulas`, origem `fase3`; `ineditos.linhas`).

| Biblioteca | Casos de avaliação certos | Casos inéditos certos | De |
|---|---|---|---|
| L0 | 28 | 27 | 36 |
| L1 | 32 | 26 | 36 |
| L3 | 31 | 29 | 36 |

## Quando o agente diz que tem certeza, ele acerta?

[Figura](selo-de-confianca.png). Fonte: `fase4/calibracao.json` (`por_selo`, corrida 16, com k = 3).

| Selo | Casos | Certos | Errados | Erro (%) |
|---|---|---|---|---|
| Alto | 37 | 34 | 3 | 8,1 |
| Médio | 26 | 22 | 4 | 15,4 |
| Baixo | 27 | 12 | 15 | 55,6 |

## Quantos casos a tela consegue mostrar

[Figura](reproducao-na-tela.png). Fonte: `fase4/reproducibilidade.json` e `reproducibilidade_ineditos.json` (`resumo`, `fora_por_motivo`, corrida 17).

| Conjunto | Casos | Reproduzem na tela | Falha armada pelo próprio teste | Sem modo na API para a causa | A falha não passa pela tela |
|---|---|---|---|---|---|
| Casos de avaliação | 72 | 37 | 11 | 2 | 22 |
| Casos inéditos da ficha 27 | 36 | 25 | 6 | 1 | 4 |

## O agente acerta tanto lendo da tela?

[Figura](tela-e-caso-escrito.png). Fonte: `fase4/tela.json`, `tela_v2.json`, `tela_v3.json`, `tela_v4.json` e `tela_ineditos.json` (`resumo`, corridas 18, 18b, 18c, 18d e 18e).

| Leitura | Casos certos | De |
|---|---|---|
| Caso escrito (corrida 18d) | 30 | 37 |
| Tela, com os sinais novos da busca (corrida 18d) | 32 | 37 |
| Tela, com o prompt dentro do limite (corrida 18c) | 27 | 37 |
| Tela, com o caso ao vivo revisado (corrida 18b) | 26 | 37 |
| Tela, primeira versão do caso ao vivo (corrida 18) | 16 | 37 |
| Inéditos, caso escrito (corrida 18e) | 18 | 25 |
| Inéditos, tela (corrida 18e) | 22 | 25 |

## O prompt na tela cabe no limite?

[Figura](prompt-e-limite.png). Fonte: tokens de entrada medidos em `fase4/tela_v2.json`, `tela_v3.json`, `tela_v4.json` e `tela_ineditos.json` (`casos`) e em `fase4_ensaio_v2/`, `fase4_ensaio_v3/` e `fase4_ensaio_v4/` (`diagnosticos__cenarios.jsonl`); limite de 1409 tokens: maior prompt da calibração mais 10%.

| Conjunto | Corrida | Menor | Mediana | Maior | Acima do limite | De |
|---|---|---|---|---|---|---|
| Casos lidos da tela | Antes do corte (18b) | 1595 | 1803 | 2034 | 37 | 37 |
| Casos lidos da tela | Depois do corte (18c) | 1069 | 1239 | 1373 | 0 | 37 |
| Casos lidos da tela | Com os sinais da busca (18d) | 1069 | 1219 | 1385 | 0 | 37 |
| Casos lidos da tela | Inéditos, com os sinais da busca (18e) | 1080 | 1231 | 1829 | 2 | 25 |
| 10 cenários | Antes do corte (21b) | 1219 | 1689,5 | 1950 | 9 | 10 |
| 10 cenários | Depois do corte (21c) | 1107 | 1164,5 | 1340 | 0 | 10 |
| 10 cenários | Com os sinais da busca (21d) | 1107 | 1164,5 | 1385 | 0 | 10 |

## Quanto tempo o agente leva, cenário a cenário

[Figura](tempo-por-cenario.png). Fonte: `fase4/cenarios_v4.json` (`por_cenario`, `geral`, corrida 21d) e `fase4/cenarios_v2.json` (`geral`, corrida 21b, a média de antes do corte).

| Cenário | Tipo | Segundos da detecção ao resultado | Chegou ao resultado | Execuções |
|---|---|---|---|---|
| Resposta cortada no meio | contrato | 92,7 | 1 | 1 |
| Campo sumiu da resposta | contrato | 73,3 | 1 | 1 |
| Campo mudou de nome | contrato | 73,1 | 1 | 1 |
| Campo mudou de tipo | contrato | 73,4 | 1 | 1 |
| Preço na escala errada | contrato | 91,2 | 1 | 1 |
| API devolve erro 500 | contrato | 85,0 | 1 | 1 |
| Busca | localizador | 73,3 | 1 | 1 |
| Login do administrador | localizador | 42,3 | 1 | 1 |
| Lista de produtos do administrador | localizador | 66,4 | 1 | 1 |
| Reserva do cliente | localizador | 68,8 | 1 | 1 |

## O que acontece com o que o agente propõe

[Figura](funil-da-biblioteca.png). Fonte: `fase4/biblioteca.json` (`resumo`, `rejeicoes`, corrida 20) e `biblioteca_producao/fechamento.json` (`mantidas`).

| Etapa | Propostas que seguem | Barradas nesta etapa |
|---|---|---|
| Propostas do modelo | 92 | 0 |
| Passam pelo validador da Fase 3 | 36 | 56 |
| Passam pelos filtros da Fase 4 | 20 | 16 |
| Entram no lote (uma ficou segurada para revisão) | 19 | 1 |
| Ficam na biblioteca depois da revisão | 11 | 9 |

## Os sinais da trilha apontam os erros de verdade?

[Figura](sinais-da-trilha.png). Fonte: `fase4/trilha.json` (`sinais`, corrida 22).

| Sinal | Nota (TPR x TNR) | Erros que pegou | Erros | Acertos que acusou | Acertos |
|---|---|---|---|---|---|
| Regra alternativa (ficha 39 b), só por gatilho | 0,6 | 3 | 5 | 2 | 31 |
| Divergência, contada só quando há gatilho | 0,5 | 3 | 5 | 3 | 31 |
| Selo de confiança baixo | 0,5 | 3 | 5 | 4 | 31 |
| Tirar ou trocar o verbete citado muda a resposta | 0,5 | 4 | 5 | 13 | 31 |
| Regra alternativa (ficha 39 b), em todos os casos | 0,4 | 4 | 5 | 14 | 31 |
| Qualquer um dos sinais principais | 0,4 | 4 | 5 | 17 | 31 |
| Sem documentação, a resposta muda | 0,3 | 3 | 5 | 13 | 31 |
| Divergência registrada, como rodou na corrida 22 | 0,3 | 4 | 5 | 20 | 31 |
| Conferência em código não passa | 0,2 | 1 | 5 | 1 | 31 |
| Repetir a pergunta muda a resposta | 0,0 | 0 | 5 | 0 | 31 |

## Entregar mais verbetes ao modelo ajuda?

[Figura](quantos-verbetes.png). Fonte: `fase4/calibracao.json` (`por_k`, corrida 16).

| Verbetes (k) | Acurácia balanceada (%) | Tamanho do prompt (tokens, mediana) | Maior prompt (tokens) | Segundos por caso (mediana) |
|---|---|---|---|---|
| 3 | 81,5 | 1106,5 | 1281 | 55,4 |
| 5 | 75,7 | 1469,0 | 1668 | 60,5 |

## Onde a leitura da tela perde acertos

[Figura](tela-por-classe.png). Fonte: `fase4/tela_v4.json` (`por_classe`, corrida 18d).

| Classe de defeito | Casos | Certos na tela | Certos no caso escrito |
|---|---|---|---|
| Léxica | 8 | 8 | 7 |
| Sintática | 7 | 7 | 5 |
| Semântica | 8 | 6 | 5 |
| Tradução | 8 | 5 | 7 |
| Runtime | 5 | 5 | 5 |
| Efeito | 1 | 1 | 1 |

## E em casos que a biblioteca nunca viu?

[Figura](ineditos-por-classe.png). Fonte: `fase4/ineditos.json` (`por_classe`, `resumo`, `referencia`, corrida 24).

| Classe de defeito | Casos | Certos | Errados |
|---|---|---|---|
| Léxica | 6 | 6 | 0 |
| Sintática | 6 | 5 | 1 |
| Semântica | 6 | 4 | 2 |
| Tradução | 6 | 1 | 5 |
| Runtime | 6 | 5 | 1 |
| Efeito | 6 | 4 | 2 |

## Onde o tempo vai

[Figura](onde-vai-o-tempo.png). Fonte: `fase4/cura.json` (`resumo`, corrida 19), `fase4/tela_v4.json` (`resumo`, corrida 18d), `fase4/cenarios_v4.json` (`por_tipo`, corrida 21d).

| Etapa | Segundos (mediana) | Usa o modelo |
|---|---|---|
| Cura de localizador só em código | 0,6 | não |
| Diagnóstico de um caso escrito | 58,0 | sim |
| Diagnóstico de um caso da tela | 59,2 | sim |
| Localizador, da detecção à reexecução | 67,6 | sim |
| Contrato, da detecção ao diagnóstico conferido | 79,2 | sim |

## O agente repara mais rápido que uma pessoa?

[Figura](agente-e-pessoas.png). Fonte: `fase5/medicao.json` (`tempo.por_cenario`, `tempo.geral`, `lados` e `task_success.por_cenario`): a corrida 28b do agente, com cinco repetições por cenário, e as três sessões da linha de base manual, uma tentativa de cada integrante por cenário.

| Cenário | Tipo | Agente: tempo médio (s) | Agente: menor tempo (s) | Agente: maior tempo (s) | Pessoas: tempo médio (s) | Pessoas: menor tempo (s) | Pessoas: maior tempo (s) | Diferença, pessoas menos agente (s) | Agente: chegou ao resultado | Pessoas: chegaram ao resultado |
|---|---|---|---|---|---|---|---|---|---|---|
| Resposta cortada no meio | contrato | 81,7 | 78,7 | 85,9 | 109,6 | 50,2 | 151,5 | 27,9 | 4 de 5 | 1 de 3 |
| Campo sumiu da resposta | contrato | 67,0 | 66,4 | 67,8 | 111,3 | 95,0 | 127,7 | 44,4 | 5 de 5 | 1 de 3 |
| Campo mudou de nome | contrato | 65,3 | 64,9 | 65,9 | 236,5 | 211,5 | 261,5 | 171,2 | 5 de 5 | 2 de 3 |
| Campo mudou de tipo | contrato | 66,7 | 66,0 | 67,6 | 189,0 | 51,4 | 260,6 | 122,3 | 5 de 5 | 0 de 3 |
| Preço na escala errada | contrato | 80,4 | 78,8 | 82,9 | 280,6 | 35,2 | 454,5 | 200,2 | 5 de 5 | 1 de 3 |
| API devolve erro 500 | contrato | 76,6 | 75,0 | 77,3 | 121,8 | 37,8 | 174,9 | 45,2 | 5 de 5 | 1 de 3 |
| Busca | localizador | 65,4 | 64,9 | 65,8 | 385,3 | 289,5 | 481,0 | 319,8 | 5 de 5 | 2 de 3 |
| Login do administrador | localizador | 39,0 | 38,5 | 40,3 | 150,1 | 144,6 | 155,7 | 111,2 | 5 de 5 | 2 de 3 |
| Lista de produtos do administrador | localizador | 60,3 | 60,1 | 60,6 | 331,2 | 258,7 | 403,7 | 270,9 | 5 de 5 | 2 de 3 |
| Reserva do cliente | localizador | 61,0 | 60,0 | 63,1 | 281,6 | 167,7 | 395,4 | 220,6 | 5 de 5 | 2 de 3 |

## O relatório ajuda quem revisa?

[Figura](revisao-humana.png). Fonte: `fase4/leitura_revisao_v3.json` (`adesao`, `resumo`; sessão de revisão dos 36 relatórios da corrida 24).

| Grupo | Casos | Decisões apropriadas | Decisões não apropriadas |
|---|---|---|---|
| Diagnósticos certos | 25 | 20 | 5 |
| Diagnósticos errados | 11 | 10 | 1 |

## Mudar o agente melhora o diagnóstico?

[Figura](experimentos-pos-fase-4.png). Fonte: `fase4/sem_notas.json` (`resumo`, corrida 25), `fase4/segundo_passe.json` (`resumo`, corrida 26) e `fase4/analista.json` (`revisao`, `leituras`, corrida 27).

| Mudança testada | Casos da referência | Certos na referência | Casos com a mudança | Certos com a mudança | Valor-p |
|---|---|---|---|---|---|
| Biblioteca sem as notas do modelo (corrida 25) | 72 | 56 | 72 | 54 | 0,6875 |
| Segundo pedido ao modelo (corrida 26) | 72 | 56 | 72 | 54 | 0,625 |
| Analista de documentação: propostas julgadas corretas (corrida 27) | 20 | 1 | 8 | 3 | 0,0581 |
