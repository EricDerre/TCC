<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-5`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-5@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `pessoas` · selo de probabilidade: **baixo** (p = 0,76) · **CONFLITO**: nenhum verbete entregue trata da causa respondida contagem_inconsistente

**IMPACTO (declarado):** `O usuário vê uma quantidade diferente de pessoas reservadas em relação ao que foi solicitado.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo pessoas porque os verbetes contrato-pedido, pedido-reserva, valor_fora_do_dominio estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,21. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida contagem_inconsistente. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,76); trate como hipótese e confira o campo pessoas antes de agir.

**Biblioteca:** 1 edição(ões) aplicada(s) ([pessoas_incorretas]), 0 para revisão humana, 1 recusada(s) (duplicada).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso tra-5. A proposta 1 (retificacao em [escala_ou_unidade_errada]) foi recusada por a validação da Fase 3 com o código duplicada: [escala_ou_unidade_errada] já tem uma nota com este texto. A proposta 2 (novo_verbete em [pessoas_incorretas], peso 3) passou pela validação da Fase 3 e pelos filtros e entrou no lote.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | retificacao | `escala_ou_unidade_errada` | recusada: `duplicada` | nenhum | recusada: `duplicada` |  |
| 2 | novo_verbete | `pessoas_incorretas` | aceita | nenhum | **aplicada** | 3 |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 1, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A reserva foi feita para 4 pessoas mas a listagem mostra 1.

OBSERVAÇÃO ADICIONAL: O POST que criou a reserva enviou pessoas=4; o banco gravou 4.
```

## 3. Contraste com a segunda causa

contagem_inconsistente e não valor_fora_do_dominio: a escolha tem probabilidade 0,76 contra 0,21; verbete(s) na evidência: contrato-pedido, pedido-reserva, valor_fora_do_dominio

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,76 | sim |
| valor_fora_do_dominio | 0,21 |  |
| tipo_divergente | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| formato_de_data_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[pedido-reserva] [valor_fora_do_dominio]`; verbetes citados: `pedido-reserva`, `valor_fora_do_dominio`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `pedido-reserva` | confere |  |
| O verbete citado existe na biblioteca | `valor_fora_do_dominio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `pedido-reserva` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio` |
| O verbete citado estava no contexto entregue ao modelo | `valor_fora_do_dominio` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[pedido-reserva] [valor_fora_do_dominio]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["pedido-reserva", "valor_fora_do_dominio"]} |
| fonte_contem_termo_da_causa | `pedido-reserva` | **não confere** | {"termo": "contagem_inconsistente"} |
| fonte_contem_termo_da_causa | `valor_fora_do_dominio` | **não confere** | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `pessoas` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>28 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 418 | 1 | entrada | programa | ao_vivo | 2026-11-03T21:45:51 | caso tra-5 |
| 419 | 2 | candidatos | programa | ao_vivo | 2026-11-03T21:45:51 | 3 de 40 verbetes entregues |
| 421 | 3 | prompt | programa | ao_vivo | 2026-11-03T21:45:51 | {"chars": 3394, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "3b1a7c21e8b5", "sha": "3b1a7c21e8b5a90f"} |
| 423 | 4 | inferencia | programa | ao_vivo | 2026-11-03T21:45:51 | diagnostico: 69,2 s |
| 424 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T21:45:51 | causa_raiz: `contagem_inconsistente` |
| 425 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T21:45:51 | campo: `pessoas` |
| 426 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T21:45:51 | impacto: `O usuário vê uma quantidade diferente de pessoas reservadas em relação ao que foi solicitado.` |
| 427 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T21:45:51 | fonte: `[pedido-reserva] [valor_fora_do_dominio]` |
| 428 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T21:45:51 | fonte_citada: `pedido-reserva` |
| 429 | 10 | declaracao | modelo | ao_vivo | 2026-11-03T21:45:51 | fonte_citada: `valor_fora_do_dominio` |
| 430 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | quatro_linhas_presentes: confere |
| 431 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | rotulo_no_conjunto: confere |
| 432 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | fonte_existe_na_biblioteca: confere |
| 433 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | fonte_existe_na_biblioteca: confere |
| 434 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | fonte_estava_no_contexto: confere |
| 435 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | fonte_estava_no_contexto: confere |
| 436 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | campo_existe_no_caso: confere |
| 437 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 438 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | notas_nos_verbetes_citados: informativo |
| 439 | 20 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | impacto: nao_verificavel |
| 440 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | fonte_formato_valido: confere |
| 441 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | fonte_contem_termo_da_causa: nao_confere |
| 442 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T21:45:51 | fonte_contem_termo_da_causa: nao_confere |
| 443 | 24 | decisao | programa | ao_vivo | 2026-11-03T21:45:51 | diagnostico: escolha contagem_inconsistente; divergência sim |
| 446 | 25 | inferencia | programa | ao_vivo | 2026-11-03T21:47:04 | proposta: 163,4 s |
| 448 | 26 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:47:04 | proposta 1: retificacao em [escala_ou_unidade_errada]: recusada: duplicada |
| 450 | 27 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:47:04 | proposta 2: novo_verbete em [pessoas_incorretas]: aplicada |
| 451 | 28 | decisao | programa | ao_vivo | 2026-11-03T21:47:04 | edicao_biblioteca: escolha proposta_2; divergência sim |

</details>

Nós de decisão:

- evento 443, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 419 (verbete_entregue, contrato-pedido), evento 419 (verbete_entregue, pedido-reserva), evento 419 (verbete_entregue, valor_fora_do_dominio), evento 423 (resposta), evento 428 (verbete_citado, pedido-reserva), evento 429 (verbete_citado, valor_fora_do_dominio); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-pedido, pedido-reserva, valor_fora_do_dominio (gen_ai: chat)
- evento 451, `edicao_biblioteca`: escolha `proposta_2`; resultado lote; evidência: evento 423 (resposta), evento 446 (resposta), evento 448 (verbete_entregue, escala_ou_unidade_errada); divergência: sim; falha: nenhuma; prov.used: contrato-pedido, escala_ou_unidade_errada, pedido-reserva, valor_fora_do_dominio

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 418 a 451 da trilha; hash dos eventos deste caso: `d94b858151f6283d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
