<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-13@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-13@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `registro_duplicado` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,79)

**IMPACTO (declarado):** `O usuário recebeu duas confirmações de reserva, resultando em uma cobrança duplicada.`

Justificativa (gerada por molde): O agente respondeu registro_duplicado porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes registro_duplicado, contrato-pedido, codificacao_incorreta estavam entre os entregues ao modelo. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,79); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 3553): regras diff_contra_contrato; antes {"chars": 54}, depois {"chars": 54}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `2dd19e03d4c54746`):

```text
Duas respostas 201, com id_pedido 8 e 9, mesmos dados.
```

## 3. Contraste com a segunda causa

registro_duplicado sem alternativa registrada no nó

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| registro_duplicado | 0,79 | sim |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[registro_duplicado] [contrato-pedido]`; verbetes citados: `registro_duplicado`, `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `registro_duplicado` | confere |  |
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `registro_duplicado` | confere | contexto: `registro_duplicado`, `contrato-pedido`, `codificacao_incorreta` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `registro_duplicado`, `contrato-pedido`, `codificacao_incorreta` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | confere | verbetes: `registro_duplicado` |
| fonte_formato_valido | `[registro_duplicado] [contrato-pedido]` | confere | {"ids": ["registro_duplicado", "contrato-pedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `registro_duplicado` | confere | {"termo": "registro_duplicado"} |
| fonte_contem_termo_da_causa | `contrato-pedido` | confere | {"termo": "registro_duplicado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-13 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3552 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:18:20 | caso run-13@sonda |
| 3553 | 2 | poda | programa | ao_vivo | 2026-11-05T02:18:20 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3554 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:18:20 | poda: escolha nao_json; divergência não |
| 3555 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:18:20 | 3 de 39 verbetes entregues |
| 3556 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:18:20 | recuperacao: escolha registro_duplicado,contrato-pedido,codificacao_incorreta; divergência não |
| 3558 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:18:20 | {"etapa": "diagnostico", "sha": "8d402cfec7d87543", "prompt_sha256": "8d402cfec7d8", "chars": 3373, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3560 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:18:20 | diagnostico: 54,1 s |
| 3561 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:18:20 | causa_raiz: `registro_duplicado` |
| 3562 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:18:20 | campo: `nenhum` |
| 3563 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:18:20 | impacto: `O usuário recebeu duas confirmações de reserva, resultando em uma cobrança duplicada.` |
| 3564 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:18:20 | fonte: `[registro_duplicado] [contrato-pedido]` |
| 3565 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:18:20 | fonte_citada: `registro_duplicado` |
| 3566 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T02:18:20 | fonte_citada: `contrato-pedido` |
| 3567 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | quatro_linhas_presentes: confere |
| 3568 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | rotulo_no_conjunto: confere |
| 3569 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | fonte_existe_na_biblioteca: confere |
| 3570 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | fonte_existe_na_biblioteca: confere |
| 3571 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | fonte_estava_no_contexto: confere |
| 3572 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | fonte_estava_no_contexto: confere |
| 3573 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | campo_existe_no_caso: nao_se_aplica |
| 3574 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3575 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | notas_nos_verbetes_citados: informativo |
| 3576 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | impacto: nao_verificavel |
| 3577 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | fonte_formato_valido: confere |
| 3578 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | fonte_contem_termo_da_causa: confere |
| 3579 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T02:18:20 | fonte_contem_termo_da_causa: confere |
| 3580 | 27 | decisao | programa | ao_vivo | 2026-11-05T02:18:20 | diagnostico: escolha registro_duplicado; divergência não |

</details>

Nós de decisão:

- evento 3554, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 3553 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3556, `recuperacao`: escolha `registro_duplicado,contrato-pedido,codificacao_incorreta`; resultado verbetes_entregues; evidência: evento 3555 (verbete_entregue, registro_duplicado), evento 3555 (verbete_entregue, contrato-pedido), evento 3555 (verbete_entregue, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: registro_duplicado, contrato-pedido, codificacao_incorreta (gen_ai: retrieval)
- evento 3580, `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido; evidência: evento 3553 (sinal_em_codigo), evento 3555 (verbete_entregue, registro_duplicado), evento 3555 (verbete_entregue, contrato-pedido), evento 3555 (verbete_entregue, codificacao_incorreta), evento 3560 (resposta), evento 3565 (verbete_citado, registro_duplicado), evento 3566 (verbete_citado, contrato-pedido); divergência: não; falha: nenhuma; prov.used: registro_duplicado, contrato-pedido, codificacao_incorreta (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3552 a 3580 da trilha; hash dos eventos deste caso: `192815fa458e4a22`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
