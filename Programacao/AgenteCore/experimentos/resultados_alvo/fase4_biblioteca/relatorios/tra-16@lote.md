<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-16`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-16@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `pessoas` · selo de probabilidade: **medio** (p = 0,94) · **CONFLITO**: nenhum verbete entregue trata da causa respondida contagem_inconsistente

**IMPACTO (declarado):** `O usuário vê uma quantidade de pessoas menor do que foi reservada, levando a uma percepção incorreta da reserva realizada.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo pessoas porque os verbetes contrato-pedido, pedido-reserva, fluxo-reserva-e-cancelamento estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,02. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida contagem_inconsistente. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 2, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A resposta de GET /api/pedidos traz pessoas=2 pra uma reserva que o cliente fez pra 8 pessoas; o numero bate com quantidade de mesas (a 4 lugares cada), nao com pessoas.

OBSERVAÇÃO ADICIONAL: O formulario de reserva (cliente/registrar_reserva.php) grava o numero de pessoas direto, sem nenhuma conversao pra mesas.
```

## 3. Contraste com a segunda causa

contagem_inconsistente e não valor_fora_do_dominio: a escolha tem probabilidade 0,94 contra 0,02; verbete(s) na evidência: contrato-pedido, pedido-reserva, fluxo-reserva-e-cancelamento

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,94 | sim |
| valor_fora_do_dominio | 0,02 |  |
| tipo_divergente | 0,02 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| formato_de_data_divergente | 0,01 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| registro_duplicado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[pedido-reserva], [contrato-pedido]`; verbetes citados: `pedido-reserva`, `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `pedido-reserva` | confere |  |
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `pedido-reserva` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `fluxo-reserva-e-cancelamento` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `fluxo-reserva-e-cancelamento` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[pedido-reserva], [contrato-pedido]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["pedido-reserva", "contrato-pedido"]} |
| fonte_contem_termo_da_causa | `pedido-reserva` | **não confere** | {"termo": "contagem_inconsistente"} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `pessoas` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2423 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:58:34 | caso tra-16 |
| 2424 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:58:34 | 3 de 46 verbetes entregues |
| 2426 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:58:34 | {"chars": 3586, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "31b5b9f677fd", "sha": "31b5b9f677fd38ef"} |
| 2428 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:58:34 | diagnostico: 55,0 s |
| 2429 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:58:34 | causa_raiz: `contagem_inconsistente` |
| 2430 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:58:34 | campo: `pessoas` |
| 2431 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:58:34 | impacto: `O usuário vê uma quantidade de pessoas menor do que foi reservada, levando a uma percepção incorreta da reserva realizada.` |
| 2432 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:58:34 | fonte: `[pedido-reserva], [contrato-pedido]` |
| 2433 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:58:34 | fonte_citada: `pedido-reserva` |
| 2434 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T00:58:34 | fonte_citada: `contrato-pedido` |
| 2435 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | quatro_linhas_presentes: confere |
| 2436 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | rotulo_no_conjunto: confere |
| 2437 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | fonte_existe_na_biblioteca: confere |
| 2438 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | fonte_existe_na_biblioteca: confere |
| 2439 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | fonte_estava_no_contexto: confere |
| 2440 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | fonte_estava_no_contexto: confere |
| 2441 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | campo_existe_no_caso: confere |
| 2442 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2443 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | notas_nos_verbetes_citados: informativo |
| 2444 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | impacto: nao_verificavel |
| 2445 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | fonte_formato_valido: confere |
| 2446 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | fonte_contem_termo_da_causa: nao_confere |
| 2447 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T00:58:34 | fonte_contem_termo_da_causa: nao_confere |
| 2448 | 24 | decisao | programa | ao_vivo | 2026-11-04T00:58:34 | diagnostico: escolha contagem_inconsistente; divergência sim |

</details>

Nós de decisão:

- evento 2448, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 2424 (verbete_entregue, contrato-pedido), evento 2424 (verbete_entregue, pedido-reserva), evento 2424 (verbete_entregue, fluxo-reserva-e-cancelamento), evento 2428 (resposta), evento 2433 (verbete_citado, pedido-reserva), evento 2434 (verbete_citado, contrato-pedido); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-pedido, pedido-reserva, fluxo-reserva-e-cancelamento (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2423 a 2448 da trilha; hash dos eventos deste caso: `cff5dace0be24a69`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
