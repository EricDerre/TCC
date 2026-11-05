<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-9@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-9@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: a FONTE cita o verbete tempo_de_resposta_excedido, fora do contexto entregue

**IMPACTO (declarado):** `O usuário percebeu um aumento significativo no tempo de resposta da requisição, levando a uma experiência negativa.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido porque o sinal esperado JSON completo e válido, recebido corpo truncado está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, resposta_truncada estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), 1 fora do contexto entregue (tempo_de_resposta_excedido). O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a FONTE cita o verbete tempo_de_resposta_excedido, fora do contexto entregue. Este nó está marcado com a falha citacao_fora_do_contexto (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 3368): regras diff_contra_contrato; antes {"chars": 171}, depois {"chars": 171}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo truncado |

Trecho podado (hash `23c095da61183dc8`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}] (recebido apos 9,4 s)
```

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não valor_fora_do_dominio: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, resposta_truncada, tempo_de_resposta_excedido

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 1,00 | sim |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | **não confere** | contexto: `entidade-produto`, `contrato-produto`, `resposta_truncada` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `resposta_truncada` |
| fonte_formato_valido | `[tempo_de_resposta_excedido]` | confere | {"ids": ["tempo_de_resposta_excedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tempo_de_resposta_excedido` | confere | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-9 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3367 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:07:14 | caso run-9@sonda |
| 3368 | 2 | poda | programa | ao_vivo | 2026-11-05T02:07:14 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3369 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:07:14 | poda: escolha truncado; divergência não |
| 3370 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:07:14 | 3 de 39 verbetes entregues |
| 3371 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:07:14 | recuperacao: escolha entidade-produto,contrato-produto,resposta_truncada; divergência não |
| 3373 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:07:14 | {"etapa": "diagnostico", "sha": "935acb7557b24d1a", "prompt_sha256": "935acb7557b2", "chars": 3874, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3375 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:07:14 | diagnostico: 70,4 s |
| 3376 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:07:14 | causa_raiz: `tempo_de_resposta_excedido` |
| 3377 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:07:14 | campo: `nenhum` |
| 3378 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:07:14 | impacto: `O usuário percebeu um aumento significativo no tempo de resposta da requisição, levando a uma experiência negativa.` |
| 3379 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:07:14 | fonte: `[tempo_de_resposta_excedido]` |
| 3380 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:07:14 | fonte_citada: `tempo_de_resposta_excedido` |
| 3381 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:07:14 | quatro_linhas_presentes: confere |
| 3382 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:07:14 | rotulo_no_conjunto: confere |
| 3383 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:07:14 | fonte_existe_na_biblioteca: confere |
| 3384 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:07:14 | fonte_estava_no_contexto: nao_confere |
| 3385 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:07:14 | campo_existe_no_caso: nao_se_aplica |
| 3386 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:07:14 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3387 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:07:14 | notas_nos_verbetes_citados: informativo |
| 3388 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:07:14 | impacto: nao_verificavel |
| 3389 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:07:14 | fonte_formato_valido: confere |
| 3390 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:07:14 | fonte_contem_termo_da_causa: confere |
| 3391 | 23 | decisao | programa | ao_vivo | 2026-11-05T02:07:14 | diagnostico: escolha tempo_de_resposta_excedido; divergência sim |

</details>

Nós de decisão:

- evento 3369, `poda`: escolha `truncado`; resultado sinais_em_codigo; evidência: evento 3368 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3371, `recuperacao`: escolha `entidade-produto,contrato-produto,resposta_truncada`; resultado verbetes_entregues; evidência: evento 3370 (verbete_entregue, entidade-produto), evento 3370 (verbete_entregue, contrato-produto), evento 3370 (verbete_entregue, resposta_truncada); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, resposta_truncada (gen_ai: retrieval)
- evento 3391, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 3368 (sinal_em_codigo), evento 3370 (verbete_entregue, entidade-produto), evento 3370 (verbete_entregue, contrato-produto), evento 3370 (verbete_entregue, resposta_truncada), evento 3375 (resposta), evento 3380 (verbete_citado, tempo_de_resposta_excedido); divergência: sim; falha: citacao_fora_do_contexto; prov.used: entidade-produto, contrato-produto, resposta_truncada, tempo_de_resposta_excedido (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3367 a 3391 da trilha; hash dos eventos deste caso: `bad605475b8b4b22`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
