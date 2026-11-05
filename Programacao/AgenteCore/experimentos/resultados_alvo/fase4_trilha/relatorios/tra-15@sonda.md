<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-15@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-15@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `registro_duplicado` · **CAMPO:** `pessoas` · selo de probabilidade: **baixo** (p = 0,72) · **CONFLITO**: nenhum verbete entregue trata da causa respondida registro_duplicado

**IMPACTO (declarado):** `O usuário vê que a reserva confirmada tem o dobro de pessoas do que foi solicitado.`

Justificativa (gerada por molde): O agente respondeu registro_duplicado no campo pessoas porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes contrato-pedido, pedido-reserva, fluxo-reserva-e-cancelamento estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,10 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,72); trate como hipótese e confira o campo pessoas antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 3278): regras diff_contra_contrato; antes {"chars": 173}, depois {"chars": 173}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `76db07a3faf27269`):

```text
POST enviou {"pessoas": 4}; GET devolveu [{"id_pedido": 8, "pessoas": 8, "data_pedido": "2026-09-12", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

registro_duplicado e não tipo_divergente: a escolha tem probabilidade 0,72 contra 0,10; verbete(s) na evidência: contrato-pedido, pedido-reserva, fluxo-reserva-e-cancelamento

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| registro_duplicado | 0,72 | sim |
| tipo_divergente | 0,10 |  |
| colecao_no_lugar_de_objeto | 0,06 |  |
| contagem_inconsistente | 0,05 |  |
| valor_fora_do_dominio | 0,03 |  |
| campo_ausente | 0,02 |  |
| campo_renomeado | 0,02 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[pedido-reserva]`; verbetes citados: `pedido-reserva`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `pedido-reserva` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `pedido-reserva` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `fluxo-reserva-e-cancelamento` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[pedido-reserva]` | confere | {"ids": ["pedido-reserva"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `pedido-reserva` | confere | {"termo": "registro_duplicado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `pessoas` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-15 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3277 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:02:51 | caso tra-15@sonda |
| 3278 | 2 | poda | programa | ao_vivo | 2026-11-05T02:02:51 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3279 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:02:51 | poda: escolha nao_json; divergência não |
| 3280 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:02:51 | 3 de 39 verbetes entregues |
| 3281 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:02:51 | recuperacao: escolha contrato-pedido,pedido-reserva,fluxo-reserva-e-cancelamento; divergência não |
| 3283 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:02:51 | {"etapa": "diagnostico", "sha": "8c82cec4bb5ee9ac", "prompt_sha256": "8c82cec4bb5e", "chars": 3512, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3285 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:02:51 | diagnostico: 53,0 s |
| 3286 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:02:51 | causa_raiz: `registro_duplicado` |
| 3287 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:02:51 | campo: `pessoas` |
| 3288 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:02:51 | impacto: `O usuário vê que a reserva confirmada tem o dobro de pessoas do que foi solicitado.` |
| 3289 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:02:51 | fonte: `[pedido-reserva]` |
| 3290 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:02:51 | fonte_citada: `pedido-reserva` |
| 3291 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:02:51 | quatro_linhas_presentes: confere |
| 3292 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:02:51 | rotulo_no_conjunto: confere |
| 3293 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:02:51 | fonte_existe_na_biblioteca: confere |
| 3294 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:02:51 | fonte_estava_no_contexto: confere |
| 3295 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:02:51 | campo_existe_no_caso: confere |
| 3296 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:02:51 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 3297 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:02:51 | notas_nos_verbetes_citados: informativo |
| 3298 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:02:51 | impacto: nao_verificavel |
| 3299 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:02:51 | fonte_formato_valido: confere |
| 3300 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:02:51 | fonte_contem_termo_da_causa: confere |
| 3301 | 23 | decisao | programa | ao_vivo | 2026-11-05T02:02:51 | diagnostico: escolha registro_duplicado; divergência sim |

</details>

Nós de decisão:

- evento 3279, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 3278 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3281, `recuperacao`: escolha `contrato-pedido,pedido-reserva,fluxo-reserva-e-cancelamento`; resultado verbetes_entregues; evidência: evento 3280 (verbete_entregue, contrato-pedido), evento 3280 (verbete_entregue, pedido-reserva), evento 3280 (verbete_entregue, fluxo-reserva-e-cancelamento); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, fluxo-reserva-e-cancelamento (gen_ai: retrieval)
- evento 3301, `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido; evidência: evento 3278 (sinal_em_codigo), evento 3280 (verbete_entregue, contrato-pedido), evento 3280 (verbete_entregue, pedido-reserva), evento 3280 (verbete_entregue, fluxo-reserva-e-cancelamento), evento 3285 (resposta), evento 3290 (verbete_citado, pedido-reserva); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-pedido, pedido-reserva, fluxo-reserva-e-cancelamento (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3277 a 3301 da trilha; hash dos eventos deste caso: `3703954df777c679`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
