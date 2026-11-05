<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/run-8@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `recurso_inexistente` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,96)

**IMPACTO (declarado):** `O usuário vê uma aba de produtos vazia, sem nenhum produto listado.`

Justificativa (gerada por molde): O agente respondeu recurso_inexistente porque os verbetes recurso_inexistente, contagem_inconsistente, estrutura_aninhada_divergente, rotas-inexistentes estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (palavra_chave_invalida, id_repetido) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso run-8. A proposta 1 (retificacao em [recurso_inexistente]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: 'db.get/filter vazio'. A proposta 2 (novo_verbete em [rotas-inexistentes]) foi recusada por a validação da Fase 3 com o código id_repetido: 'rotas-inexistentes' já é id de verbete ou nome de causa raiz.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | retificacao | `recurso_inexistente` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |
| 2 | novo_verbete | `rotas-inexistentes` | recusada: `id_repetido` | nenhum | recusada: `id_repetido` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produto

STATUS HTTP: 404

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "Not Found"}

SINTOMA OBSERVADO: A aba de produtos via API nunca carrega nada.

OBSERVAÇÃO ADICIONAL: O endpoint correto e /api/produtos, no plural.
```

## 3. Contraste com a segunda causa

recurso_inexistente e não resposta_truncada: a escolha tem probabilidade 0,96 contra 0,00; verbete(s) na evidência: recurso_inexistente, contagem_inconsistente, estrutura_aninhada_divergente, rotas-inexistentes

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| recurso_inexistente | 0,96 | sim |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[recurso_inexistente]`; verbetes citados: `recurso_inexistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `recurso_inexistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `recurso_inexistente` | confere | contexto: `recurso_inexistente`, `contagem_inconsistente`, `estrutura_aninhada_divergente`, `rotas-inexistentes` |
| Algum verbete do contexto trata da causa respondida | `recurso_inexistente` | confere | verbetes: `recurso_inexistente`, `rotas-inexistentes` |
| fonte_formato_valido | `[recurso_inexistente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["recurso_inexistente"]} |
| fonte_contem_termo_da_causa | `recurso_inexistente` | confere | {"termo": "recurso_inexistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1471 | 1 | entrada | programa | ao_vivo | 2026-11-03T23:36:01 | caso run-8 |
| 1472 | 2 | candidatos | programa | ao_vivo | 2026-11-03T23:36:01 | 3 de 40 verbetes entregues |
| 1474 | 3 | prompt | programa | ao_vivo | 2026-11-03T23:36:01 | {"chars": 3675, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "e9c35816dd29", "sha": "e9c35816dd295aed"} |
| 1476 | 4 | inferencia | programa | ao_vivo | 2026-11-03T23:36:01 | diagnostico: 67,4 s |
| 1477 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T23:36:01 | causa_raiz: `recurso_inexistente` |
| 1478 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T23:36:01 | campo: `nenhum` |
| 1479 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T23:36:01 | impacto: `O usuário vê uma aba de produtos vazia, sem nenhum produto listado.` |
| 1480 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T23:36:01 | fonte: `[recurso_inexistente]` |
| 1481 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T23:36:01 | fonte_citada: `recurso_inexistente` |
| 1482 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T23:36:01 | quatro_linhas_presentes: confere |
| 1483 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T23:36:01 | rotulo_no_conjunto: confere |
| 1484 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T23:36:01 | fonte_existe_na_biblioteca: confere |
| 1485 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T23:36:01 | fonte_estava_no_contexto: confere |
| 1486 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T23:36:01 | campo_existe_no_caso: nao_se_aplica |
| 1487 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T23:36:01 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1488 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T23:36:01 | notas_nos_verbetes_citados: informativo |
| 1489 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T23:36:01 | impacto: nao_verificavel |
| 1490 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T23:36:01 | fonte_formato_valido: confere |
| 1491 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T23:36:01 | fonte_contem_termo_da_causa: confere |
| 1492 | 20 | decisao | programa | ao_vivo | 2026-11-03T23:36:01 | diagnostico: escolha recurso_inexistente; divergência não |
| 1495 | 21 | inferencia | programa | ao_vivo | 2026-11-03T23:37:12 | proposta: 158,2 s |
| 1496 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:37:12 | proposta 1: retificacao em [recurso_inexistente]: recusada: palavra_chave_invalida |
| 1498 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:37:12 | proposta 2: novo_verbete em [rotas-inexistentes]: recusada: id_repetido |
| 1499 | 24 | decisao | programa | ao_vivo | 2026-11-03T23:37:12 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1492, `diagnostico`: escolha `recurso_inexistente`; resultado rotulo_emitido; evidência: evento 1472 (verbete_entregue, recurso_inexistente), evento 1472 (verbete_entregue, contagem_inconsistente), evento 1472 (verbete_entregue, estrutura_aninhada_divergente), evento 1472 (verbete_entregue, rotas-inexistentes), evento 1476 (resposta), evento 1481 (verbete_citado, recurso_inexistente); divergência: não; falha: nenhuma; prov.used: recurso_inexistente, contagem_inconsistente, estrutura_aninhada_divergente, rotas-inexistentes (gen_ai: chat)
- evento 1499, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1476 (resposta), evento 1495 (resposta), evento 1496 (verbete_entregue, recurso_inexistente), evento 1498 (verbete_entregue, rotas-inexistentes); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: contagem_inconsistente, estrutura_aninhada_divergente, recurso_inexistente, rotas-inexistentes

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1471 a 1499 da trilha; hash dos eventos deste caso: `e7b3f07a9330e7b8`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
