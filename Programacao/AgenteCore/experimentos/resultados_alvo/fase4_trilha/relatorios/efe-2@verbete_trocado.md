<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-2@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-2@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `registro_duplicado` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,36) · **CONFLITO**: nenhum verbete entregue trata da causa respondida registro_duplicado

**IMPACTO (declarado):** `A tela do cliente não reflete o status 'Cancelado' do pedido 7, mantendo-o como 'Em Análise'.`

Justificativa (gerada por molde): O agente respondeu registro_duplicado porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes contrato-pedido, valor_fora_do_dominio, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, estado_da_tela_divergente, ficou com probabilidade 0,39 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,36); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 1453): regras diff_contra_contrato; antes {"chars": 54}, depois {"chars": 54}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `9747f76426520e17`):

```text
A API devolveu {"id_pedido": 7, "status": "Cancelado"}
```

## 3. Contraste com a segunda causa

registro_duplicado e não estado_da_tela_divergente: a escolha tem probabilidade 0,36 contra 0,39; verbete(s) na evidência: contrato-pedido, valor_fora_do_dominio, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estado_da_tela_divergente | 0,39 |  |
| registro_duplicado | 0,36 | sim |
| dado_desatualizado | 0,15 |  |
| campo_ausente | 0,02 |  |
| campo_renomeado | 0,02 |  |
| resposta_truncada | 0,02 |  |
| chave_de_juncao_errada | 0,02 |  |
| valor_fora_do_dominio | 0,01 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| recurso_inexistente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `valor_fora_do_dominio`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"ids": ["contrato-pedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "registro_duplicado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-2 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1452 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:27:16 | caso efe-2@verbete_trocado |
| 1453 | 2 | poda | programa | ao_vivo | 2026-11-05T00:27:16 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1454 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:27:16 | poda: escolha nao_json; divergência não |
| 1455 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:27:16 | 3 de 39 verbetes entregues |
| 1456 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:27:16 | recuperacao: escolha contrato-pedido,valor_fora_do_dominio,pedido-reserva; divergência não |
| 1457 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:27:16 | {"etapa": "diagnostico", "sha": "6d92f55b37bbe4b8", "prompt_sha256": "6d92f55b37bb", "chars": 3456, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1458 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:27:16 | diagnostico: 15,7 s |
| 1459 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:27:16 | causa_raiz: `registro_duplicado` |
| 1460 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:27:16 | campo: `nenhum` |
| 1461 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:27:16 | impacto: `A tela do cliente não reflete o status 'Cancelado' do pedido 7, mantendo-o como 'Em Análise'.` |
| 1462 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:27:16 | fonte: `[contrato-pedido]` |
| 1463 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:27:16 | fonte_citada: `contrato-pedido` |
| 1464 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:16 | quatro_linhas_presentes: confere |
| 1465 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:16 | rotulo_no_conjunto: confere |
| 1466 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:16 | fonte_existe_na_biblioteca: confere |
| 1467 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:16 | fonte_estava_no_contexto: confere |
| 1468 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:16 | campo_existe_no_caso: nao_se_aplica |
| 1469 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:16 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1470 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:16 | notas_nos_verbetes_citados: informativo |
| 1471 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:16 | impacto: nao_verificavel |
| 1472 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:16 | fonte_formato_valido: confere |
| 1473 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:16 | fonte_contem_termo_da_causa: nao_confere |
| 1474 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:27:16 | diagnostico: escolha registro_duplicado; divergência sim |

</details>

Nós de decisão:

- evento 1454, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 1453 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1456, `recuperacao`: escolha `contrato-pedido,valor_fora_do_dominio,pedido-reserva`; resultado verbetes_entregues; evidência: evento 1455 (verbete_entregue, contrato-pedido), evento 1455 (verbete_entregue, valor_fora_do_dominio), evento 1455 (verbete_entregue, pedido-reserva); divergência: não; falha: nenhuma; prov.used: contrato-pedido, valor_fora_do_dominio, pedido-reserva (gen_ai: retrieval)
- evento 1474, `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido; evidência: evento 1453 (sinal_em_codigo), evento 1455 (verbete_entregue, contrato-pedido), evento 1455 (verbete_entregue, valor_fora_do_dominio), evento 1455 (verbete_entregue, pedido-reserva), evento 1458 (resposta), evento 1463 (verbete_citado, contrato-pedido); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-pedido, valor_fora_do_dominio, pedido-reserva (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1452 a 1474 da trilha; hash dos eventos deste caso: `864559019e7b736c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
