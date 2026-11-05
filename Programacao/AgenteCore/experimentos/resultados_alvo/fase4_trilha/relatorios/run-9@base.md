<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-9@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário percebeu um aumento significativo no tempo de resposta da requisição, levando a uma experiência menos fluida.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido porque o sinal esperado JSON completo e válido, recebido corpo truncado está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, resposta_truncada estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete resposta_truncada não mudou a resposta: sem efeito medido do contexto. A troca do verbete resposta_truncada por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 3328): regras diff_contra_contrato; antes {"chars": 171}, depois {"chars": 171}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo truncado |

Trecho podado (hash `23c095da61183dc8`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}] (recebido apos 9,4 s)
```

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, resposta_truncada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[resposta_truncada]`; verbetes citados: `resposta_truncada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `entidade-produto`, `contrato-produto`, `resposta_truncada` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `resposta_truncada` |
| fonte_formato_valido | `[resposta_truncada]` | confere | {"ids": ["resposta_truncada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `resposta_truncada` | **não confere** | {"termo": "tempo_de_resposta_excedido"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `resposta_truncada` | tempo_de_resposta_excedido | tempo_de_resposta_excedido | 1,00 | 0,99 | sem efeito medido do contexto |
| troca | `resposta_truncada` | tempo_de_resposta_excedido | tempo_de_resposta_excedido | 1,00 | 1,00 | sem efeito medido do contexto |
| sem_documentacao | `` | tempo_de_resposta_excedido | tempo_de_resposta_excedido | 1,00 | 1,00 | sem efeito medido do contexto |
| repeticao_da_base | `` | tempo_de_resposta_excedido | tempo_de_resposta_excedido | 1,00 | 1,00 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-9 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3326 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:04:08 | caso run-9 |
| 3328 | 2 | poda | programa | ao_vivo | 2026-11-05T02:04:08 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3329 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:04:08 | poda: escolha truncado; divergência não |
| 3330 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:04:08 | 3 de 39 verbetes entregues |
| 3331 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:04:08 | recuperacao: escolha entidade-produto,contrato-produto,resposta_truncada; divergência não |
| 3333 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:04:08 | {"etapa": "diagnostico", "sha": "732550e48ff82416", "prompt_sha256": "732550e48ff8", "chars": 3750, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3335 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:04:08 | diagnostico: 53,7 s |
| 3336 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:04:08 | causa_raiz: `tempo_de_resposta_excedido` |
| 3337 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:04:08 | campo: `nenhum` |
| 3338 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:04:08 | impacto: `O usuário percebeu um aumento significativo no tempo de resposta da requisição, levando a uma experiência menos fluida.` |
| 3339 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:04:08 | fonte: `[resposta_truncada]` |
| 3340 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:04:08 | fonte_citada: `resposta_truncada` |
| 3341 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:04:08 | quatro_linhas_presentes: confere |
| 3342 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:04:08 | rotulo_no_conjunto: confere |
| 3343 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:04:08 | fonte_existe_na_biblioteca: confere |
| 3344 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:04:08 | fonte_estava_no_contexto: confere |
| 3345 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:04:08 | campo_existe_no_caso: nao_se_aplica |
| 3346 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:04:08 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3347 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:04:08 | notas_nos_verbetes_citados: informativo |
| 3348 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:04:08 | impacto: nao_verificavel |
| 3349 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:04:08 | fonte_formato_valido: confere |
| 3350 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:04:08 | fonte_contem_termo_da_causa: nao_confere |
| 3353 | 23 | inferencia | programa | ao_vivo | 2026-11-05T02:04:08 | intervencao:remocao: 37,0 s |
| 3354 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T02:04:08 | remocao de resposta_truncada: rótulo tempo_de_resposta_excedido para tempo_de_resposta_excedido |
| 3357 | 25 | inferencia | programa | ao_vivo | 2026-11-05T02:04:08 | intervencao:troca: 42,3 s |
| 3358 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T02:04:08 | troca de resposta_truncada: rótulo tempo_de_resposta_excedido para tempo_de_resposta_excedido |
| 3361 | 27 | inferencia | programa | ao_vivo | 2026-11-05T02:04:08 | intervencao:sem_documentacao: 30,7 s |
| 3362 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T02:04:08 | sem_documentacao de None: rótulo tempo_de_resposta_excedido para tempo_de_resposta_excedido |
| 3364 | 29 | inferencia | programa | ao_vivo | 2026-11-05T02:04:08 | intervencao:repeticao_da_base: 17,8 s |
| 3365 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T02:04:08 | repeticao_da_base de None: rótulo tempo_de_resposta_excedido para tempo_de_resposta_excedido |
| 3366 | 31 | decisao | programa | ao_vivo | 2026-11-05T02:04:08 | diagnostico: escolha tempo_de_resposta_excedido; divergência não |

</details>

Nós de decisão:

- evento 3329, `poda`: escolha `truncado`; resultado sinais_em_codigo; evidência: evento 3328 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3331, `recuperacao`: escolha `entidade-produto,contrato-produto,resposta_truncada`; resultado verbetes_entregues; evidência: evento 3330 (verbete_entregue, entidade-produto), evento 3330 (verbete_entregue, contrato-produto), evento 3330 (verbete_entregue, resposta_truncada); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, resposta_truncada (gen_ai: retrieval)
- evento 3366, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 3328 (sinal_em_codigo), evento 3330 (verbete_entregue, entidade-produto), evento 3330 (verbete_entregue, contrato-produto), evento 3330 (verbete_entregue, resposta_truncada), evento 3335 (resposta), evento 3340 (verbete_citado, resposta_truncada); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, resposta_truncada (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3326 a 3366 da trilha; hash dos eventos deste caso: `12a2412f7a395360`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
