<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/run-17@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `O usuário não recebe informações específicas sobre o status do pedido, apenas um erro genérico.`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor porque os verbetes erro_interno_do_servidor, mensagens-de-erro-do-codigo, modos-de-injecao estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos/7/cancelar

STATUS HTTP: 500

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
{"detail": "erro interno (fault injection) em pedido"}

SINTOMA OBSERVADO: Cancelar a reserva 7 devolve 500; nao da pra saber pela resposta se o status mudou no banco ou nao.
```

## 3. Contraste com a segunda causa

erro_interno_do_servidor e não tipo_divergente: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: erro_interno_do_servidor, mensagens-de-erro-do-codigo, modos-de-injecao

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 0,98 | sim |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[erro_interno_do_servidor]`; verbetes citados: `erro_interno_do_servidor`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `modos-de-injecao` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `modos-de-injecao` |
| fonte_formato_valido | `[erro_interno_do_servidor]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["erro_interno_do_servidor"]} |
| fonte_contem_termo_da_causa | `erro_interno_do_servidor` | confere | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2600 | 1 | entrada | programa | ao_vivo | 2026-11-04T01:05:47 | caso run-17 |
| 2601 | 2 | candidatos | programa | ao_vivo | 2026-11-04T01:05:47 | 3 de 46 verbetes entregues |
| 2603 | 3 | prompt | programa | ao_vivo | 2026-11-04T01:05:47 | {"chars": 3544, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "cb1a0137ca43", "sha": "cb1a0137ca438f05"} |
| 2605 | 4 | inferencia | programa | ao_vivo | 2026-11-04T01:05:47 | diagnostico: 68,0 s |
| 2606 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T01:05:47 | causa_raiz: `erro_interno_do_servidor` |
| 2607 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T01:05:47 | campo: `nenhum` |
| 2608 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T01:05:47 | impacto: `O usuário não recebe informações específicas sobre o status do pedido, apenas um erro genérico.` |
| 2609 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T01:05:47 | fonte: `[erro_interno_do_servidor]` |
| 2610 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T01:05:47 | fonte_citada: `erro_interno_do_servidor` |
| 2611 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T01:05:47 | quatro_linhas_presentes: confere |
| 2612 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T01:05:47 | rotulo_no_conjunto: confere |
| 2613 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T01:05:47 | fonte_existe_na_biblioteca: confere |
| 2614 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T01:05:47 | fonte_estava_no_contexto: confere |
| 2615 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T01:05:47 | campo_existe_no_caso: nao_se_aplica |
| 2616 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T01:05:47 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2617 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T01:05:47 | notas_nos_verbetes_citados: informativo |
| 2618 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T01:05:47 | impacto: nao_verificavel |
| 2619 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T01:05:47 | fonte_formato_valido: confere |
| 2620 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T01:05:47 | fonte_contem_termo_da_causa: confere |
| 2621 | 20 | decisao | programa | ao_vivo | 2026-11-04T01:05:47 | diagnostico: escolha erro_interno_do_servidor; divergência não |

</details>

Nós de decisão:

- evento 2621, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 2601 (verbete_entregue, erro_interno_do_servidor), evento 2601 (verbete_entregue, mensagens-de-erro-do-codigo), evento 2601 (verbete_entregue, modos-de-injecao), evento 2605 (resposta), evento 2610 (verbete_citado, erro_interno_do_servidor); divergência: não; falha: nenhuma; prov.used: erro_interno_do_servidor, mensagens-de-erro-do-codigo, modos-de-injecao (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2600 a 2621 da trilha; hash dos eventos deste caso: `6ddc6ab03e5612ed`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
