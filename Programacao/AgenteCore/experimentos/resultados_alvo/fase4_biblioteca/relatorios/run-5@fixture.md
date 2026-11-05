<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-5`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/run-5@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `registro_duplicado` · **CAMPO:** `id_pedido` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida registro_duplicado

**IMPACTO (declarado):** `O cliente vê duas reservas identicas após confirmar uma única vez.`

Justificativa (gerada por molde): O agente respondeu registro_duplicado no campo id_pedido porque os verbetes contrato-pedido, pedido-reserva, formato_de_data_divergente estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

**Biblioteca:** 1 edição(ões) aplicada(s) ([contrato-pedido]), 0 para revisão humana, 1 recusada(s) (id_repetido).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso run-5. A proposta 1 (novo_verbete em [registro_duplicado]) foi recusada por a validação da Fase 3 com o código id_repetido: 'registro_duplicado' já é id de verbete ou nome de causa raiz. A proposta 2 (nota em [contrato-pedido], peso 1) passou pela validação da Fase 3 e pelos filtros e entrou no lote.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | novo_verbete | `registro_duplicado` | recusada: `id_repetido` | nenhum | recusada: `id_repetido` |  |
| 2 | nota | `contrato-pedido` | aceita | nenhum | **aplicada** | 1 |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos (enviado uma vez) | GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 8, "pessoas": 6, "data_pedido": "2026-09-12", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 9, "pessoas": 6, "data_pedido": "2026-09-12", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: O cliente ve duas reservas identicas apos confirmar uma unica vez.
```

## 3. Contraste com a segunda causa

registro_duplicado e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-pedido, pedido-reserva, formato_de_data_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| registro_duplicado | 1,00 | sim |
| colecao_no_lugar_de_objeto | 0,00 |  |
| resposta_truncada | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| recurso_inexistente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `formato_de_data_divergente` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-pedido"]} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "registro_duplicado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id_pedido` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 494 | 1 | entrada | programa | ao_vivo | 2026-11-03T21:54:39 | caso run-5 |
| 495 | 2 | candidatos | programa | ao_vivo | 2026-11-03T21:54:39 | 3 de 40 verbetes entregues |
| 497 | 3 | prompt | programa | ao_vivo | 2026-11-03T21:54:39 | {"chars": 3355, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "e14972c1eb99", "sha": "e14972c1eb994680"} |
| 499 | 4 | inferencia | programa | ao_vivo | 2026-11-03T21:54:39 | diagnostico: 66,0 s |
| 500 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T21:54:39 | causa_raiz: `registro_duplicado` |
| 501 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T21:54:39 | campo: `id_pedido` |
| 502 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T21:54:39 | impacto: `O cliente vê duas reservas identicas após confirmar uma única vez.` |
| 503 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T21:54:39 | fonte: `[contrato-pedido]` |
| 504 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T21:54:39 | fonte_citada: `contrato-pedido` |
| 505 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T21:54:39 | quatro_linhas_presentes: confere |
| 506 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T21:54:39 | rotulo_no_conjunto: confere |
| 507 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T21:54:39 | fonte_existe_na_biblioteca: confere |
| 508 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T21:54:39 | fonte_estava_no_contexto: confere |
| 509 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T21:54:39 | campo_existe_no_caso: confere |
| 510 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T21:54:39 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 511 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T21:54:39 | notas_nos_verbetes_citados: informativo |
| 512 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T21:54:39 | impacto: nao_verificavel |
| 513 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T21:54:39 | fonte_formato_valido: confere |
| 514 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T21:54:39 | fonte_contem_termo_da_causa: nao_confere |
| 515 | 20 | decisao | programa | ao_vivo | 2026-11-03T21:54:39 | diagnostico: escolha registro_duplicado; divergência sim |
| 518 | 21 | inferencia | programa | ao_vivo | 2026-11-03T21:55:49 | proposta: 168,7 s |
| 520 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:55:49 | proposta 1: novo_verbete em [registro_duplicado]: recusada: id_repetido |
| 522 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:55:49 | proposta 2: nota em [contrato-pedido]: aplicada |
| 523 | 24 | decisao | programa | ao_vivo | 2026-11-03T21:55:49 | edicao_biblioteca: escolha proposta_2; divergência sim |

</details>

Nós de decisão:

- evento 515, `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido; evidência: evento 495 (verbete_entregue, contrato-pedido), evento 495 (verbete_entregue, pedido-reserva), evento 495 (verbete_entregue, formato_de_data_divergente), evento 499 (resposta), evento 504 (verbete_citado, contrato-pedido); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-pedido, pedido-reserva, formato_de_data_divergente (gen_ai: chat)
- evento 523, `edicao_biblioteca`: escolha `proposta_2`; resultado lote; evidência: evento 499 (resposta), evento 518 (resposta), evento 520 (verbete_entregue, registro_duplicado), evento 522 (verbete_entregue, contrato-pedido); divergência: sim; falha: nenhuma; prov.used: contrato-pedido, formato_de_data_divergente, pedido-reserva, registro_duplicado

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 494 a 523 da trilha; hash dos eventos deste caso: `9a1bbc7dbb7393d4`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
