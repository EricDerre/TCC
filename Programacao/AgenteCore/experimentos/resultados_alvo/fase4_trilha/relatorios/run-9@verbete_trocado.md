<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-9@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-9@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida tempo_de_resposta_excedido

**IMPACTO (declarado):** `O usuário percebeu um aumento significativo no tempo de resposta da requisição, levando a uma experiência menos fluida.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido porque o sinal esperado JSON completo e válido, recebido corpo truncado está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida tempo_de_resposta_excedido. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 3393): regras diff_contra_contrato; antes {"chars": 171}, depois {"chars": 171}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo truncado |

Trecho podado (hash `23c095da61183dc8`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}] (recebido apos 9,4 s)
```

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 1,00 | sim |
| colecao_no_lugar_de_objeto | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-9 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3392 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:08:28 | caso run-9@verbete_trocado |
| 3393 | 2 | poda | programa | ao_vivo | 2026-11-05T02:08:28 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3394 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:08:28 | poda: escolha truncado; divergência não |
| 3395 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:08:28 | 3 de 39 verbetes entregues |
| 3396 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:08:28 | recuperacao: escolha entidade-produto,contrato-produto,tipo_divergente; divergência não |
| 3397 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:08:28 | {"etapa": "diagnostico", "sha": "e631cd4a4b04d1b8", "prompt_sha256": "e631cd4a4b04", "chars": 3634, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3399 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:08:28 | diagnostico: 16,1 s |
| 3400 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:08:28 | causa_raiz: `tempo_de_resposta_excedido` |
| 3401 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:08:28 | campo: `nenhum` |
| 3402 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:08:28 | impacto: `O usuário percebeu um aumento significativo no tempo de resposta da requisição, levando a uma experiência menos fluida.` |
| 3403 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:08:28 | fonte: `[contrato-produto]` |
| 3404 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:08:28 | fonte_citada: `contrato-produto` |
| 3405 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:28 | quatro_linhas_presentes: confere |
| 3406 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:28 | rotulo_no_conjunto: confere |
| 3407 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:28 | fonte_existe_na_biblioteca: confere |
| 3408 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:28 | fonte_estava_no_contexto: confere |
| 3409 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:28 | campo_existe_no_caso: nao_se_aplica |
| 3410 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:28 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 3411 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:28 | notas_nos_verbetes_citados: informativo |
| 3412 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:28 | impacto: nao_verificavel |
| 3413 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:28 | fonte_formato_valido: confere |
| 3414 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:28 | fonte_contem_termo_da_causa: nao_confere |
| 3415 | 23 | decisao | programa | ao_vivo | 2026-11-05T02:08:28 | diagnostico: escolha tempo_de_resposta_excedido; divergência sim |

</details>

Nós de decisão:

- evento 3394, `poda`: escolha `truncado`; resultado sinais_em_codigo; evidência: evento 3393 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3396, `recuperacao`: escolha `entidade-produto,contrato-produto,tipo_divergente`; resultado verbetes_entregues; evidência: evento 3395 (verbete_entregue, entidade-produto), evento 3395 (verbete_entregue, contrato-produto), evento 3395 (verbete_entregue, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: retrieval)
- evento 3415, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 3393 (sinal_em_codigo), evento 3395 (verbete_entregue, entidade-produto), evento 3395 (verbete_entregue, contrato-produto), evento 3395 (verbete_entregue, tipo_divergente), evento 3399 (resposta), evento 3404 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3392 a 3415 da trilha; hash dos eventos deste caso: `5aa8387ec7581ee7`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
