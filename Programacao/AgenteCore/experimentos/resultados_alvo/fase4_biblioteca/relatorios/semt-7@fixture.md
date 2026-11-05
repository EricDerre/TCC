<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-7`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-7@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `formato_de_data_divergente` · **CAMPO:** `data_pedido` · selo de probabilidade: **baixo** (p = 0,61)

**IMPACTO (declarado):** `A data de pedido exibida na tela administrativa está em um formato que o sistema não reconhece, causando inconsistência na contagem total de lugares reservados.`

Justificativa (gerada por molde): O agente respondeu formato_de_data_divergente no campo data_pedido porque os verbetes contrato-pedido, pedido-reserva, formato_de_data_divergente estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,21. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,61); trate como hipótese e confira o campo data_pedido antes de agir.

**Biblioteca:** 1 edição(ões) aplicada(s) ([tipo_divergente]), 0 para revisão humana, 1 recusada(s) (id_repetido).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso semt-7. A proposta 1 (retificacao em [tipo_divergente], peso 2) passou pela validação da Fase 3 e pelos filtros e entrou no lote. A proposta 2 (novo_verbete em [contagem_inconsistente]) foi recusada por a validação da Fase 3 com o código id_repetido: 'contagem_inconsistente' já é id de verbete ou nome de causa raiz.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | retificacao | `tipo_divergente` | aceita | nenhum | **aplicada** | 2 |
| 2 | novo_verbete | `contagem_inconsistente` | recusada: `id_repetido` | nenhum | recusada: `id_repetido` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": "4", "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A soma total de lugares reservados sai errada na tela administrativa.
```

## 3. Contraste com a segunda causa

formato_de_data_divergente e não tipo_divergente: a escolha tem probabilidade 0,61 contra 0,21; verbete(s) na evidência: contrato-pedido, pedido-reserva, formato_de_data_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| formato_de_data_divergente | 0,61 | sim |
| tipo_divergente | 0,21 |  |
| campo_ausente | 0,08 |  |
| campo_renomeado | 0,08 |  |
| valor_fora_do_dominio | 0,05 |  |
| contagem_inconsistente | 0,03 |  |
| escala_ou_unidade_errada | 0,01 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| nulo_inesperado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[formato_de_data_divergente]`; verbetes citados: `formato_de_data_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `formato_de_data_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `formato_de_data_divergente` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `formato_de_data_divergente` |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | confere | verbetes: `contrato-pedido`, `formato_de_data_divergente` |
| fonte_formato_valido | `[formato_de_data_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["formato_de_data_divergente"]} |
| fonte_contem_termo_da_causa | `formato_de_data_divergente` | confere | {"termo": "formato_de_data_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `data_pedido` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 941 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:40:08 | caso semt-7 |
| 942 | 2 | candidatos | programa | ao_vivo | 2026-11-03T22:40:08 | 3 de 40 verbetes entregues |
| 944 | 3 | prompt | programa | ao_vivo | 2026-11-03T22:40:08 | {"chars": 3190, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "611e0326dcc6", "sha": "611e0326dcc609a9"} |
| 946 | 4 | inferencia | programa | ao_vivo | 2026-11-03T22:40:08 | diagnostico: 37,2 s |
| 947 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T22:40:08 | causa_raiz: `formato_de_data_divergente` |
| 948 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T22:40:08 | campo: `data_pedido` |
| 949 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T22:40:08 | impacto: `A data de pedido exibida na tela administrativa está em um formato que o sistema não reconhece, causando inconsistência na contagem total de lugares reservados.` |
| 950 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T22:40:08 | fonte: `[formato_de_data_divergente]` |
| 951 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T22:40:08 | fonte_citada: `formato_de_data_divergente` |
| 952 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T22:40:08 | quatro_linhas_presentes: confere |
| 953 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T22:40:08 | rotulo_no_conjunto: confere |
| 954 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T22:40:08 | fonte_existe_na_biblioteca: confere |
| 955 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T22:40:08 | fonte_estava_no_contexto: confere |
| 956 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T22:40:08 | campo_existe_no_caso: confere |
| 957 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T22:40:08 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 958 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T22:40:08 | notas_nos_verbetes_citados: informativo |
| 959 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T22:40:08 | impacto: nao_verificavel |
| 960 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T22:40:08 | fonte_formato_valido: confere |
| 961 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T22:40:08 | fonte_contem_termo_da_causa: confere |
| 962 | 20 | decisao | programa | ao_vivo | 2026-11-03T22:40:08 | diagnostico: escolha formato_de_data_divergente; divergência não |
| 965 | 21 | inferencia | programa | ao_vivo | 2026-11-03T22:40:49 | proposta: 164,2 s |
| 967 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:40:49 | proposta 1: retificacao em [tipo_divergente]: aplicada |
| 969 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:40:49 | proposta 2: novo_verbete em [contagem_inconsistente]: recusada: id_repetido |
| 970 | 24 | decisao | programa | ao_vivo | 2026-11-03T22:40:49 | edicao_biblioteca: escolha proposta_1; divergência sim |

</details>

Nós de decisão:

- evento 962, `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido; evidência: evento 942 (verbete_entregue, contrato-pedido), evento 942 (verbete_entregue, pedido-reserva), evento 942 (verbete_entregue, formato_de_data_divergente), evento 946 (resposta), evento 951 (verbete_citado, formato_de_data_divergente); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, formato_de_data_divergente (gen_ai: chat)
- evento 970, `edicao_biblioteca`: escolha `proposta_1`; resultado lote; evidência: evento 946 (resposta), evento 965 (resposta), evento 967 (verbete_entregue, tipo_divergente); divergência: sim; falha: nenhuma; prov.used: contrato-pedido, formato_de_data_divergente, pedido-reserva, tipo_divergente

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 941 a 970 da trilha; hash dos eventos deste caso: `fa9c2cd4597a5f9c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
