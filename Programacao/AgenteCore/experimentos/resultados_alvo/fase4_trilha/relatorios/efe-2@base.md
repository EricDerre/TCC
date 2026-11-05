<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-2`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-2@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estado_da_tela_divergente` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,72) · **CONFLITO**: a troca do verbete estado_da_tela_divergente por um errado mudou a resposta de estado_da_tela_divergente para registro_duplicado; a inferência sem documentação mudou a resposta de estado_da_tela_divergente para tipo_divergente

**IMPACTO (declarado):** `A tela do cliente não reflete o status 'Cancelado' do pedido 7, continuando a exibir 'Em Analise'.`

Justificativa (gerada por molde): O agente respondeu estado_da_tela_divergente porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes contrato-pedido, estado_da_tela_divergente, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,19. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete estado_da_tela_divergente não mudou a resposta: sem efeito medido do contexto. A troca do verbete estado_da_tela_divergente por um verbete errado mudou a resposta (de estado_da_tela_divergente para registro_duplicado). A inferência sem documentação mudou a resposta (de estado_da_tela_divergente para tipo_divergente). A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a troca do verbete estado_da_tela_divergente por um errado mudou a resposta de estado_da_tela_divergente para registro_duplicado; a inferência sem documentação mudou a resposta de estado_da_tela_divergente para tipo_divergente. O agente não está seguro desta causa (probabilidade 0,72); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 1390): regras diff_contra_contrato; antes {"chars": 54}, depois {"chars": 54}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `9747f76426520e17`):

```text
A API devolveu {"id_pedido": 7, "status": "Cancelado"}
```

## 3. Contraste com a segunda causa

estado_da_tela_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 0,72 contra 0,19; verbete(s) na evidência: contrato-pedido, estado_da_tela_divergente, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estado_da_tela_divergente | 0,72 | sim |
| valor_fora_do_dominio | 0,19 |  |
| chave_de_juncao_errada | 0,04 |  |
| registro_duplicado | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| dado_desatualizado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[estado_da_tela_divergente]`; verbetes citados: `estado_da_tela_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estado_da_tela_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estado_da_tela_divergente` | confere | contexto: `contrato-pedido`, `estado_da_tela_divergente`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `estado_da_tela_divergente` | confere | verbetes: `estado_da_tela_divergente` |
| fonte_formato_valido | `[estado_da_tela_divergente]` | confere | {"ids": ["estado_da_tela_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `estado_da_tela_divergente` | confere | {"termo": "estado_da_tela_divergente"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `estado_da_tela_divergente` | estado_da_tela_divergente | estado_da_tela_divergente | 0,72 | 0,61 | sem efeito medido do contexto |
| troca | `estado_da_tela_divergente` | estado_da_tela_divergente | registro_duplicado | 0,72 | 0,36 | mudou a resposta: o verbete pesou na decisão |
| sem_documentacao | `` | estado_da_tela_divergente | tipo_divergente | 0,72 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| repeticao_da_base | `` | estado_da_tela_divergente | estado_da_tela_divergente | 0,72 | 0,66 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-2 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1388 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:22:53 | caso efe-2 |
| 1390 | 2 | poda | programa | ao_vivo | 2026-11-05T00:22:53 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1391 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:22:53 | poda: escolha nao_json; divergência não |
| 1392 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:22:53 | 3 de 39 verbetes entregues |
| 1393 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:22:53 | recuperacao: escolha contrato-pedido,estado_da_tela_divergente,pedido-reserva; divergência não |
| 1395 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:22:53 | {"etapa": "diagnostico", "sha": "95b413b548f45bea", "prompt_sha256": "95b413b548f4", "chars": 3416, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1397 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:22:53 | diagnostico: 48,0 s |
| 1398 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:22:53 | causa_raiz: `estado_da_tela_divergente` |
| 1399 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:22:53 | campo: `nenhum` |
| 1400 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:22:53 | impacto: `A tela do cliente não reflete o status 'Cancelado' do pedido 7, continuando a exibir 'Em Analise'.` |
| 1401 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:22:53 | fonte: `[estado_da_tela_divergente]` |
| 1402 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:22:53 | fonte_citada: `estado_da_tela_divergente` |
| 1403 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:53 | quatro_linhas_presentes: confere |
| 1404 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:53 | rotulo_no_conjunto: confere |
| 1405 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:53 | fonte_existe_na_biblioteca: confere |
| 1406 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:53 | fonte_estava_no_contexto: confere |
| 1407 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:53 | campo_existe_no_caso: nao_se_aplica |
| 1408 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:53 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1409 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:53 | notas_nos_verbetes_citados: informativo |
| 1410 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:53 | impacto: nao_verificavel |
| 1411 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:53 | fonte_formato_valido: confere |
| 1412 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:53 | fonte_contem_termo_da_causa: confere |
| 1415 | 23 | inferencia | programa | ao_vivo | 2026-11-05T00:22:53 | intervencao:remocao: 50,7 s |
| 1416 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T00:22:53 | remocao de estado_da_tela_divergente: rótulo estado_da_tela_divergente para estado_da_tela_divergente |
| 1419 | 25 | inferencia | programa | ao_vivo | 2026-11-05T00:22:53 | intervencao:troca: 38,5 s |
| 1420 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T00:22:53 | troca de estado_da_tela_divergente: rótulo estado_da_tela_divergente para registro_duplicado |
| 1423 | 27 | inferencia | programa | ao_vivo | 2026-11-05T00:22:53 | intervencao:sem_documentacao: 37,4 s |
| 1424 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T00:22:53 | sem_documentacao de None: rótulo estado_da_tela_divergente para tipo_divergente |
| 1425 | 29 | inferencia | programa | ao_vivo | 2026-11-05T00:22:53 | intervencao:repeticao_da_base: 17,1 s |
| 1426 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T00:22:53 | repeticao_da_base de None: rótulo estado_da_tela_divergente para estado_da_tela_divergente |
| 1427 | 31 | decisao | programa | ao_vivo | 2026-11-05T00:22:53 | diagnostico: escolha estado_da_tela_divergente; divergência sim |

</details>

Nós de decisão:

- evento 1391, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 1390 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1393, `recuperacao`: escolha `contrato-pedido,estado_da_tela_divergente,pedido-reserva`; resultado verbetes_entregues; evidência: evento 1392 (verbete_entregue, contrato-pedido), evento 1392 (verbete_entregue, estado_da_tela_divergente), evento 1392 (verbete_entregue, pedido-reserva); divergência: não; falha: nenhuma; prov.used: contrato-pedido, estado_da_tela_divergente, pedido-reserva (gen_ai: retrieval)
- evento 1427, `diagnostico`: escolha `estado_da_tela_divergente`; resultado rotulo_emitido; evidência: evento 1390 (sinal_em_codigo), evento 1392 (verbete_entregue, contrato-pedido), evento 1392 (verbete_entregue, estado_da_tela_divergente), evento 1392 (verbete_entregue, pedido-reserva), evento 1397 (resposta), evento 1402 (verbete_citado, estado_da_tela_divergente); divergência: sim; falha: nenhuma; prov.used: contrato-pedido, estado_da_tela_divergente, pedido-reserva (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1388 a 1427 da trilha; hash dos eventos deste caso: `14d77c8584b191dd`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
