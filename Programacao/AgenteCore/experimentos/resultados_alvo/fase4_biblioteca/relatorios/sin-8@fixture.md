<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-8@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê a listagem quebrada ao tentar percorrer o resultado, pois espera um objeto único mas recebe uma lista.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto porque os verbetes entidade-produto, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (duplicada, duplicada) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso sin-8. A proposta 1 (nota em [colecao_no_lugar_de_objeto]) foi recusada por a validação da Fase 3 com o código duplicada: [colecao_no_lugar_de_objeto] já tem uma nota com este texto. A proposta 2 (retificacao em [colecao_no_lugar_de_objeto]) foi recusada por a validação da Fase 3 com o código duplicada: [colecao_no_lugar_de_objeto] já tem uma nota com este texto.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `colecao_no_lugar_de_objeto` | recusada: `duplicada` | nenhum | recusada: `duplicada` |  |
| 2 | retificacao | `colecao_no_lugar_de_objeto` | recusada: `duplicada` | nenhum | recusada: `duplicada` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano (lista)

CORPO DA RESPOSTA:
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}

SINTOMA OBSERVADO: A listagem quebra ao tentar percorrer o resultado.
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não tipo_divergente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,99 | sim |
| tipo_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [colecao_no_lugar_de_objeto]`; verbetes citados: `contrato-produto`, `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto`, `colecao_no_lugar_de_objeto` |
| fonte_formato_valido | `[contrato-produto] [colecao_no_lugar_de_objeto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "colecao_no_lugar_de_objeto"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>29 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 706 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:15:42 | caso sin-8 |
| 707 | 2 | incidente | programa | ao_vivo | 2026-11-03T22:15:42 | {"detalhe": "nenhuma diferença medida contra o contrato, a referência e o roteiro", "tipo": "tela_nao_reproduz"} |
| 708 | 3 | candidatos | programa | ao_vivo | 2026-11-03T22:15:42 | 3 de 40 verbetes entregues |
| 710 | 4 | prompt | programa | ao_vivo | 2026-11-03T22:15:42 | {"chars": 3659, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "8e1ce5e5ccc1", "sha": "8e1ce5e5ccc160f7"} |
| 712 | 5 | inferencia | programa | ao_vivo | 2026-11-03T22:15:42 | diagnostico: 74,1 s |
| 713 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T22:15:42 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 714 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T22:15:42 | campo: `nenhum` |
| 715 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T22:15:42 | impacto: `O usuário vê a listagem quebrada ao tentar percorrer o resultado, pois espera um objeto único mas recebe uma lista.` |
| 716 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T22:15:42 | fonte: `[contrato-produto] [colecao_no_lugar_de_objeto]` |
| 717 | 10 | declaracao | modelo | ao_vivo | 2026-11-03T22:15:42 | fonte_citada: `contrato-produto` |
| 718 | 11 | declaracao | modelo | ao_vivo | 2026-11-03T22:15:42 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 719 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | quatro_linhas_presentes: confere |
| 720 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | rotulo_no_conjunto: confere |
| 721 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | fonte_existe_na_biblioteca: confere |
| 722 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | fonte_existe_na_biblioteca: confere |
| 723 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | fonte_estava_no_contexto: confere |
| 724 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | fonte_estava_no_contexto: confere |
| 725 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | campo_existe_no_caso: nao_se_aplica |
| 726 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 727 | 20 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | notas_nos_verbetes_citados: informativo |
| 728 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | impacto: nao_verificavel |
| 729 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | fonte_formato_valido: confere |
| 730 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | fonte_contem_termo_da_causa: nao_confere |
| 731 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T22:15:42 | fonte_contem_termo_da_causa: confere |
| 732 | 25 | decisao | programa | ao_vivo | 2026-11-03T22:15:42 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |
| 735 | 26 | inferencia | programa | ao_vivo | 2026-11-03T22:17:01 | proposta: 161,2 s |
| 737 | 27 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:17:01 | proposta 1: nota em [colecao_no_lugar_de_objeto]: recusada: duplicada |
| 738 | 28 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:17:01 | proposta 2: retificacao em [colecao_no_lugar_de_objeto]: recusada: duplicada |
| 739 | 29 | decisao | programa | ao_vivo | 2026-11-03T22:17:01 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 732, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 708 (verbete_entregue, entidade-produto), evento 708 (verbete_entregue, contrato-produto), evento 708 (verbete_entregue, colecao_no_lugar_de_objeto), evento 712 (resposta), evento 717 (verbete_citado, contrato-produto), evento 718 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)
- evento 739, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 712 (resposta), evento 735 (resposta), evento 737 (verbete_entregue, colecao_no_lugar_de_objeto), evento 738 (verbete_entregue, colecao_no_lugar_de_objeto); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: colecao_no_lugar_de_objeto, contrato-produto, entidade-produto

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 706 a 739 da trilha; hash dos eventos deste caso: `4e1ca273ba497826`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
