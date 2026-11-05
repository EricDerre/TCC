<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-4`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/efe-4@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `id` · selo de probabilidade: **baixo** (p = 0,53)

**IMPACTO (declarado):** `A interface exibe uma lista vazia porque espera um objeto, mas recebeu uma coleção com um único item.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo id porque os verbetes entidade-produto, estado_da_tela_divergente, contrato-produto, interface-estados estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,38. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,53); trate como hipótese e confira o campo id antes de agir.

**Biblioteca:** 1 edição(ões) aplicada(s) ([estado_da_tela_divergente]), 1 para revisão humana ([contrato-produto]), 0 recusada(s).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso efe-4. A proposta 1 (nota em [contrato-produto]) passou pelas validações, mas ficou segurada para revisão humana: [contrato-produto] esteve em 42.2% dos contextos da calibração (limiar 40%). A proposta 2 (retificacao em [estado_da_tela_divergente], peso 2) passou pela validação da Fase 3 e pelos filtros e entrou no lote.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `contrato-produto` | aceita | regra_dos_40 | para revisão humana | 1 |
| 2 | retificacao | `estado_da_tela_divergente` | aceita | nenhum | **aplicada** | 2 |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: A API respondeu com 1 produto e sem erro, mas a listagem na tela aparece vazia.

OBSERVAÇÃO ADICIONAL: Nao ha erro no console. O filtro de categoria estava com 'Bebidas' selecionado.
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não tipo_divergente: a escolha tem probabilidade 0,53 contra 0,38; verbete(s) na evidência: entidade-produto, estado_da_tela_divergente, contrato-produto, interface-estados

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,53 | sim |
| tipo_divergente | 0,38 |  |
| campo_ausente | 0,04 |  |
| campo_renomeado | 0,04 |  |
| resposta_truncada | 0,02 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| formato_de_data_divergente | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `estado_da_tela_divergente`, `contrato-produto`, `interface-estados` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 525 | 1 | entrada | programa | ao_vivo | 2026-11-03T21:58:42 | caso efe-4 |
| 526 | 2 | candidatos | programa | ao_vivo | 2026-11-03T21:58:42 | 3 de 40 verbetes entregues |
| 528 | 3 | prompt | programa | ao_vivo | 2026-11-03T21:58:42 | {"chars": 3697, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "118e28fbfb13", "sha": "118e28fbfb13b770"} |
| 530 | 4 | inferencia | programa | ao_vivo | 2026-11-03T21:58:42 | diagnostico: 71,4 s |
| 531 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T21:58:42 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 532 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T21:58:42 | campo: `id` |
| 533 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T21:58:42 | impacto: `A interface exibe uma lista vazia porque espera um objeto, mas recebeu uma coleção com um único item.` |
| 534 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T21:58:42 | fonte: `[contrato-produto]` |
| 535 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T21:58:42 | fonte_citada: `contrato-produto` |
| 536 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T21:58:42 | quatro_linhas_presentes: confere |
| 537 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T21:58:42 | rotulo_no_conjunto: confere |
| 538 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T21:58:42 | fonte_existe_na_biblioteca: confere |
| 539 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T21:58:42 | fonte_estava_no_contexto: confere |
| 540 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T21:58:42 | campo_existe_no_caso: confere |
| 541 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T21:58:42 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 542 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T21:58:42 | notas_nos_verbetes_citados: informativo |
| 543 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T21:58:42 | impacto: nao_verificavel |
| 544 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T21:58:42 | fonte_formato_valido: confere |
| 545 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T21:58:42 | fonte_contem_termo_da_causa: nao_confere |
| 546 | 20 | decisao | programa | ao_vivo | 2026-11-03T21:58:42 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |
| 549 | 21 | inferencia | programa | ao_vivo | 2026-11-03T21:59:58 | proposta: 162,9 s |
| 551 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:59:58 | proposta 1: nota em [contrato-produto]: para revisão humana |
| 553 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:59:58 | proposta 2: retificacao em [estado_da_tela_divergente]: aplicada |
| 554 | 24 | decisao | programa | ao_vivo | 2026-11-03T21:59:58 | edicao_biblioteca: escolha proposta_2; divergência não |

</details>

Nós de decisão:

- evento 546, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 526 (verbete_entregue, entidade-produto), evento 526 (verbete_entregue, estado_da_tela_divergente), evento 526 (verbete_entregue, contrato-produto), evento 526 (verbete_entregue, interface-estados), evento 530 (resposta), evento 535 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, estado_da_tela_divergente, contrato-produto, interface-estados (gen_ai: chat)
- evento 554, `edicao_biblioteca`: escolha `proposta_2`; resultado lote; evidência: evento 530 (resposta), evento 549 (resposta), evento 551 (verbete_entregue, contrato-produto), evento 553 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: contrato-produto, entidade-produto, estado_da_tela_divergente, interface-estados

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 525 a 554 da trilha; hash dos eventos deste caso: `d4844ac7464bbf8d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
