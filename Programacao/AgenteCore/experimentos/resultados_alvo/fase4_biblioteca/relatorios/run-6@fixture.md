<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-6`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/run-6@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário recebe uma mensagem genérica de erro sem detalhes específicos sobre o que falhou.`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor porque os verbetes erro_interno_do_servidor, mensagens-de-erro-do-codigo, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 1 recusada(s) (texto_longo) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 1 edição(ões) para o caso run-6. A proposta 1 (retificacao em [erro_interno_do_servidor]) foi recusada por a validação da Fase 3 com o código texto_longo: TEXTO com 282 caracteres (máximo 280).

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | retificacao | `erro_interno_do_servidor` | recusada: `texto_longo` | nenhum | recusada: `texto_longo` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos

STATUS HTTP: 500

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
{"detail": "Internal Server Error"}

SINTOMA OBSERVADO: A confirmacao da reserva falha com mensagem generica de erro.
```

## 3. Contraste com a segunda causa

erro_interno_do_servidor e não corpo_nao_e_json: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: erro_interno_do_servidor, mensagens-de-erro-do-codigo, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 0,99 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[erro_interno_do_servidor]`; verbetes citados: `erro_interno_do_servidor`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo` |
| fonte_formato_valido | `[erro_interno_do_servidor]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["erro_interno_do_servidor"]} |
| fonte_contem_termo_da_causa | `erro_interno_do_servidor` | confere | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1403 | 1 | entrada | programa | ao_vivo | 2026-11-03T23:28:26 | caso run-6 |
| 1404 | 2 | candidatos | programa | ao_vivo | 2026-11-03T23:28:26 | 3 de 40 verbetes entregues |
| 1406 | 3 | prompt | programa | ao_vivo | 2026-11-03T23:28:26 | {"chars": 3624, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "ea043ad1b098", "sha": "ea043ad1b09831d7"} |
| 1408 | 4 | inferencia | programa | ao_vivo | 2026-11-03T23:28:26 | diagnostico: 68,7 s |
| 1409 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T23:28:26 | causa_raiz: `erro_interno_do_servidor` |
| 1410 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T23:28:26 | campo: `nenhum` |
| 1411 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T23:28:26 | impacto: `O usuário recebe uma mensagem genérica de erro sem detalhes específicos sobre o que falhou.` |
| 1412 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T23:28:26 | fonte: `[erro_interno_do_servidor]` |
| 1413 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T23:28:26 | fonte_citada: `erro_interno_do_servidor` |
| 1414 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T23:28:26 | quatro_linhas_presentes: confere |
| 1415 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T23:28:26 | rotulo_no_conjunto: confere |
| 1416 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T23:28:26 | fonte_existe_na_biblioteca: confere |
| 1417 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T23:28:26 | fonte_estava_no_contexto: confere |
| 1418 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T23:28:26 | campo_existe_no_caso: nao_se_aplica |
| 1419 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T23:28:26 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1420 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T23:28:26 | notas_nos_verbetes_citados: informativo |
| 1421 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T23:28:26 | impacto: nao_verificavel |
| 1422 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T23:28:26 | fonte_formato_valido: confere |
| 1423 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T23:28:26 | fonte_contem_termo_da_causa: confere |
| 1424 | 20 | decisao | programa | ao_vivo | 2026-11-03T23:28:26 | diagnostico: escolha erro_interno_do_servidor; divergência não |
| 1427 | 21 | inferencia | programa | ao_vivo | 2026-11-03T23:29:38 | proposta: 135,1 s |
| 1429 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:29:38 | proposta 1: retificacao em [erro_interno_do_servidor]: recusada: texto_longo |
| 1430 | 23 | decisao | programa | ao_vivo | 2026-11-03T23:29:38 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1424, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 1404 (verbete_entregue, erro_interno_do_servidor), evento 1404 (verbete_entregue, mensagens-de-erro-do-codigo), evento 1404 (verbete_entregue, estrutura_aninhada_divergente), evento 1408 (resposta), evento 1413 (verbete_citado, erro_interno_do_servidor); divergência: não; falha: nenhuma; prov.used: erro_interno_do_servidor, mensagens-de-erro-do-codigo, estrutura_aninhada_divergente (gen_ai: chat)
- evento 1430, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1408 (resposta), evento 1427 (resposta), evento 1429 (verbete_entregue, erro_interno_do_servidor); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: erro_interno_do_servidor, estrutura_aninhada_divergente, mensagens-de-erro-do-codigo

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1403 a 1430 da trilha; hash dos eventos deste caso: `618c2191a068674b`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
