<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por progresso.py --taxas a partir de diagnosticos__*.jsonl e trilha_*.jsonl das corridas vigentes (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Taxas do modelo para a barra de progresso (Pós-Fase 4, pacote Q4), gerada em 2026-11-08

A barra estima o prefill pelos tokens do prompt (caracteres divididos pelos caracteres por token) divididos pela taxa de prefill, e a geração pela mediana de tokens gerados dividida pela taxa de geração, com o teto como máximo. Tudo vem dos registros das corridas `fase4_tela_v4`, `fase4_ensaio_v4`, `fase4_ineditos`; a mediana entra na estimativa e os percentis 10 e 90 dizem o intervalo.

## qwen2.5:7b (120 registros; máquina TARGET_TSP030; Ollama 0.40.14; teto 600 tokens)

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

Fontes da barra: Nielsen (1993): limites de 0,1 s, 1 s e 10 s; acima de 10 s, indicador de fração concluída com estimativa; Myers (1985): 86,1% dos sujeitos preferem o indicador de fração concluída, que distingue espera de travamento; Harrison et al. (2007): pausas perto do fim parecem mais lentas; a barra nunca para antes de concluir; Apple HIG (2023) e Material Components: determinado quando a duração é estimável, trocando de indeterminado sem mudar o formato; Ollama, API reference: prompt_eval_count, prompt_eval_duration, eval_count e eval_duration só chegam no fim da resposta.
