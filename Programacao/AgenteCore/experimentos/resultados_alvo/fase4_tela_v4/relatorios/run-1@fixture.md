<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/run-1@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `A aba de produtos via API exibe a mensagem "Erro ao carregar produtos da CobaiaAPI: erro interno (fault injection)".`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor porque os verbetes erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 500

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "erro interno (fault injection)"}

SINTOMA OBSERVADO: A aba de produtos via API mostra a mensagem de erro ao carregar.
```

## 3. Contraste com a segunda causa

erro_interno_do_servidor e não corpo_nao_e_json: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 0,98 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[erro_interno_do_servidor]`; verbetes citados: `erro_interno_do_servidor`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo` |
| fonte_formato_valido | `[erro_interno_do_servidor]` | confere | {"ids": ["erro_interno_do_servidor"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `erro_interno_do_servidor` | confere | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-1 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 470 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:12:53 | caso run-1 |
| 471 | 2 | candidatos | programa | ao_vivo | 2026-11-06T10:12:53 | 3 de 39 verbetes entregues |
| 473 | 3 | prompt | programa | ao_vivo | 2026-11-06T10:12:53 | {"etapa": "diagnostico", "sha": "4933583fbab8816a", "prompt_sha256": "4933583fbab8", "chars": 3503, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 475 | 4 | inferencia | programa | ao_vivo | 2026-11-06T10:12:53 | diagnostico: 60,3 s |
| 476 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T10:12:53 | causa_raiz: `erro_interno_do_servidor` |
| 477 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T10:12:53 | campo: `nenhum` |
| 478 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T10:12:53 | impacto: `A aba de produtos via API exibe a mensagem "Erro ao carregar produtos da CobaiaAPI: erro interno (fault injection)".` |
| 479 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T10:12:53 | fonte: `[erro_interno_do_servidor]` |
| 480 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T10:12:53 | fonte_citada: `erro_interno_do_servidor` |
| 481 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | quatro_linhas_presentes: confere |
| 482 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | rotulo_no_conjunto: confere |
| 483 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | fonte_existe_na_biblioteca: confere |
| 484 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | fonte_estava_no_contexto: confere |
| 485 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | campo_existe_no_caso: nao_se_aplica |
| 486 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 487 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | notas_nos_verbetes_citados: informativo |
| 488 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | impacto: nao_verificavel |
| 489 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | fonte_formato_valido: confere |
| 490 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | fonte_contem_termo_da_causa: confere |
| 491 | 20 | decisao | programa | ao_vivo | 2026-11-06T10:12:53 | diagnostico: escolha erro_interno_do_servidor; divergência não |

</details>

Nós de decisão:

- evento 491, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 471 (verbete_entregue, erro_interno_do_servidor), evento 471 (verbete_entregue, mensagens-de-erro-do-codigo), evento 471 (verbete_entregue, contagem_inconsistente), evento 475 (resposta), evento 480 (verbete_citado, erro_interno_do_servidor); divergência: não; falha: nenhuma; prov.used: erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 470 a 491 da trilha; hash dos eventos deste caso: `3b6c79022d914860`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
