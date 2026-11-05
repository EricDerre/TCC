<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-18`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-18@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `id_pedido` · selo de probabilidade: **medio** (p = 0,96) · **CONFLITO**: nenhum verbete entregue trata da causa respondida contagem_inconsistente

**IMPACTO (declarado):** `O usuário vê uma lista incompleta de reservas, com apenas uma reserva do Cliente Teste, enquanto ele fez três reservas nos últimos meses.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo id_pedido porque os verbetes contrato-pedido, pedido-reserva, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, registro_duplicado, ficou com probabilidade 0,02 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida contagem_inconsistente. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A resposta de GET /api/pedidos traz so 1 reserva do Cliente Teste, mas ele fez 3 reservas nos ultimos meses; as outras duas nao aparecem nem como ativas nem como canceladas.

OBSERVAÇÃO ADICIONAL: A consulta filtra por id_clientes = cliente.id_usuario; as 3 reservas estao todas com o mesmo id_clientes no banco.
```

## 3. Contraste com a segunda causa

contagem_inconsistente e não registro_duplicado: a escolha tem probabilidade 0,96 contra 0,02; verbete(s) na evidência: contrato-pedido, pedido-reserva, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,96 | sim |
| registro_duplicado | 0,02 |  |
| chave_de_juncao_errada | 0,01 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido], [pedido-reserva]`; verbetes citados: `contrato-pedido`, `pedido-reserva`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado existe na biblioteca | `pedido-reserva` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `estado_da_tela_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `pedido-reserva` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-pedido], [pedido-reserva]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-pedido", "pedido-reserva"]} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "contagem_inconsistente"} |
| fonte_contem_termo_da_causa | `pedido-reserva` | **não confere** | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id_pedido` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2477 | 1 | entrada | programa | ao_vivo | 2026-11-04T01:00:14 | caso tra-18 |
| 2478 | 2 | candidatos | programa | ao_vivo | 2026-11-04T01:00:14 | 3 de 46 verbetes entregues |
| 2480 | 3 | prompt | programa | ao_vivo | 2026-11-04T01:00:14 | {"chars": 4008, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "5754dc279f1f", "sha": "5754dc279f1f098e"} |
| 2482 | 4 | inferencia | programa | ao_vivo | 2026-11-04T01:00:14 | diagnostico: 64,7 s |
| 2483 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T01:00:14 | causa_raiz: `contagem_inconsistente` |
| 2484 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T01:00:14 | campo: `id_pedido` |
| 2485 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T01:00:14 | impacto: `O usuário vê uma lista incompleta de reservas, com apenas uma reserva do Cliente Teste, enquanto ele fez três reservas nos últimos meses.` |
| 2486 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T01:00:14 | fonte: `[contrato-pedido], [pedido-reserva]` |
| 2487 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T01:00:14 | fonte_citada: `contrato-pedido` |
| 2488 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T01:00:14 | fonte_citada: `pedido-reserva` |
| 2489 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | quatro_linhas_presentes: confere |
| 2490 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | rotulo_no_conjunto: confere |
| 2491 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | fonte_existe_na_biblioteca: confere |
| 2492 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | fonte_existe_na_biblioteca: confere |
| 2493 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | fonte_estava_no_contexto: confere |
| 2494 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | fonte_estava_no_contexto: confere |
| 2495 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | campo_existe_no_caso: confere |
| 2496 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2497 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | notas_nos_verbetes_citados: informativo |
| 2498 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | impacto: nao_verificavel |
| 2499 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | fonte_formato_valido: confere |
| 2500 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | fonte_contem_termo_da_causa: nao_confere |
| 2501 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T01:00:14 | fonte_contem_termo_da_causa: nao_confere |
| 2502 | 24 | decisao | programa | ao_vivo | 2026-11-04T01:00:14 | diagnostico: escolha contagem_inconsistente; divergência sim |

</details>

Nós de decisão:

- evento 2502, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 2478 (verbete_entregue, contrato-pedido), evento 2478 (verbete_entregue, pedido-reserva), evento 2478 (verbete_entregue, estado_da_tela_divergente), evento 2482 (resposta), evento 2487 (verbete_citado, contrato-pedido), evento 2488 (verbete_citado, pedido-reserva); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-pedido, pedido-reserva, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2477 a 2502 da trilha; hash dos eventos deste caso: `2cbf3dfb1559b06d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
