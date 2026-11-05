<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-13@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-13@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `registro_duplicado` · **CAMPO:** `id_pedido` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida registro_duplicado

**IMPACTO (declarado):** `O cliente recebeu duas cobranças para a mesma reserva, resultando em duplicidade na cobrança.`

Justificativa (gerada por molde): O agente respondeu registro_duplicado no campo id_pedido porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes formato_de_data_divergente, contrato-pedido, codificacao_incorreta estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 3582): regras diff_contra_contrato; antes {"chars": 54}, depois {"chars": 54}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `2dd19e03d4c54746`):

```text
Duas respostas 201, com id_pedido 8 e 9, mesmos dados.
```

## 3. Contraste com a segunda causa

registro_duplicado e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: formato_de_data_divergente, contrato-pedido, codificacao_incorreta

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| registro_duplicado | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `formato_de_data_divergente`, `contrato-pedido`, `codificacao_incorreta` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"ids": ["contrato-pedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "registro_duplicado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id_pedido` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-13 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3581 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:19:18 | caso run-13@verbete_trocado |
| 3582 | 2 | poda | programa | ao_vivo | 2026-11-05T02:19:18 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3583 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:19:18 | poda: escolha nao_json; divergência não |
| 3584 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:19:18 | 3 de 39 verbetes entregues |
| 3585 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:19:18 | recuperacao: escolha formato_de_data_divergente,contrato-pedido,codificacao_incorreta; divergência não |
| 3586 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:19:18 | {"etapa": "diagnostico", "sha": "2020d957b684725f", "prompt_sha256": "2020d957b684", "chars": 3301, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3588 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:19:18 | diagnostico: 14,5 s |
| 3589 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:19:18 | causa_raiz: `registro_duplicado` |
| 3590 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:19:18 | campo: `id_pedido` |
| 3591 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:19:18 | impacto: `O cliente recebeu duas cobranças para a mesma reserva, resultando em duplicidade na cobrança.` |
| 3592 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:19:18 | fonte: `[contrato-pedido]` |
| 3593 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:19:18 | fonte_citada: `contrato-pedido` |
| 3594 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:18 | quatro_linhas_presentes: confere |
| 3595 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:18 | rotulo_no_conjunto: confere |
| 3596 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:18 | fonte_existe_na_biblioteca: confere |
| 3597 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:18 | fonte_estava_no_contexto: confere |
| 3598 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:18 | campo_existe_no_caso: confere |
| 3599 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:18 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 3600 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:18 | notas_nos_verbetes_citados: informativo |
| 3601 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:18 | impacto: nao_verificavel |
| 3602 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:18 | fonte_formato_valido: confere |
| 3603 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:18 | fonte_contem_termo_da_causa: nao_confere |
| 3604 | 23 | decisao | programa | ao_vivo | 2026-11-05T02:19:18 | diagnostico: escolha registro_duplicado; divergência sim |

</details>

Nós de decisão:

- evento 3583, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 3582 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3585, `recuperacao`: escolha `formato_de_data_divergente,contrato-pedido,codificacao_incorreta`; resultado verbetes_entregues; evidência: evento 3584 (verbete_entregue, formato_de_data_divergente), evento 3584 (verbete_entregue, contrato-pedido), evento 3584 (verbete_entregue, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: formato_de_data_divergente, contrato-pedido, codificacao_incorreta (gen_ai: retrieval)
- evento 3604, `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido; evidência: evento 3582 (sinal_em_codigo), evento 3584 (verbete_entregue, formato_de_data_divergente), evento 3584 (verbete_entregue, contrato-pedido), evento 3584 (verbete_entregue, codificacao_incorreta), evento 3588 (resposta), evento 3593 (verbete_citado, contrato-pedido); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: formato_de_data_divergente, contrato-pedido, codificacao_incorreta (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3581 a 3604 da trilha; hash dos eventos deste caso: `59caeae10f4ed428`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
