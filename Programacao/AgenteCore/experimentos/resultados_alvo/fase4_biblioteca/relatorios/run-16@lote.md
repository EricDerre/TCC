<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-16`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/run-16@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `recurso_inexistente` · **CAMPO:** `cpf` · selo de probabilidade: **baixo** (p = 0,80)

**IMPACTO (declarado):** `O usuário recebe uma mensagem de erro inesperada, indicando que o cliente não foi encontrado, ao invés de uma lista vazia de pedidos.`

Justificativa (gerada por molde): O agente respondeu recurso_inexistente no campo cpf porque os verbetes recurso_inexistente, contrato-pedido, mensagens-de-erro-do-codigo estavam entre os entregues ao modelo. A segunda causa, registro_duplicado, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,80); trate como hipótese e confira o campo cpf antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=55566677788

STATUS HTTP: 404

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
{"detail": "cliente nao encontrado"}

SINTOMA OBSERVADO: Consultar as reservas de um cpf que nunca fez cadastro (55566677788) devolve 404; a mensagem indica cliente nao encontrado, nao uma lista vazia de reservas.
```

## 3. Contraste com a segunda causa

recurso_inexistente e não registro_duplicado: a escolha tem probabilidade 0,80 contra 0,00; verbete(s) na evidência: recurso_inexistente, contrato-pedido, mensagens-de-erro-do-codigo

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| recurso_inexistente | 0,80 | sim |
| registro_duplicado | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| erro_interno_do_servidor | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[recurso_inexistente]`; verbetes citados: `recurso_inexistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `recurso_inexistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `recurso_inexistente` | confere | contexto: `recurso_inexistente`, `contrato-pedido`, `mensagens-de-erro-do-codigo` |
| Algum verbete do contexto trata da causa respondida | `recurso_inexistente` | confere | verbetes: `recurso_inexistente`, `contrato-pedido`, `mensagens-de-erro-do-codigo` |
| fonte_formato_valido | `[recurso_inexistente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["recurso_inexistente"]} |
| fonte_contem_termo_da_causa | `recurso_inexistente` | confere | {"termo": "recurso_inexistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `cpf` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2577 | 1 | entrada | programa | ao_vivo | 2026-11-04T01:04:32 | caso run-16 |
| 2578 | 2 | candidatos | programa | ao_vivo | 2026-11-04T01:04:32 | 3 de 46 verbetes entregues |
| 2580 | 3 | prompt | programa | ao_vivo | 2026-11-04T01:04:32 | {"chars": 3479, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "895f2a793a19", "sha": "895f2a793a194488"} |
| 2582 | 4 | inferencia | programa | ao_vivo | 2026-11-04T01:04:32 | diagnostico: 70,1 s |
| 2583 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T01:04:32 | causa_raiz: `recurso_inexistente` |
| 2584 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T01:04:32 | campo: `cpf` |
| 2585 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T01:04:32 | impacto: `O usuário recebe uma mensagem de erro inesperada, indicando que o cliente não foi encontrado, ao invés de uma lista vazia de pedidos.` |
| 2586 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T01:04:32 | fonte: `[recurso_inexistente]` |
| 2587 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T01:04:32 | fonte_citada: `recurso_inexistente` |
| 2588 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T01:04:32 | quatro_linhas_presentes: confere |
| 2589 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T01:04:32 | rotulo_no_conjunto: confere |
| 2590 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T01:04:32 | fonte_existe_na_biblioteca: confere |
| 2591 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T01:04:32 | fonte_estava_no_contexto: confere |
| 2592 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T01:04:32 | campo_existe_no_caso: confere |
| 2593 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T01:04:32 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2594 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T01:04:32 | notas_nos_verbetes_citados: informativo |
| 2595 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T01:04:32 | impacto: nao_verificavel |
| 2596 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T01:04:32 | fonte_formato_valido: confere |
| 2597 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T01:04:32 | fonte_contem_termo_da_causa: confere |
| 2598 | 20 | decisao | programa | ao_vivo | 2026-11-04T01:04:32 | diagnostico: escolha recurso_inexistente; divergência não |

</details>

Nós de decisão:

- evento 2598, `diagnostico`: escolha `recurso_inexistente`; resultado rotulo_emitido; evidência: evento 2578 (verbete_entregue, recurso_inexistente), evento 2578 (verbete_entregue, contrato-pedido), evento 2578 (verbete_entregue, mensagens-de-erro-do-codigo), evento 2582 (resposta), evento 2587 (verbete_citado, recurso_inexistente); divergência: não; falha: nenhuma; prov.used: recurso_inexistente, contrato-pedido, mensagens-de-erro-do-codigo (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2577 a 2598 da trilha; hash dos eventos deste caso: `b6de61dbbbbf0944`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
