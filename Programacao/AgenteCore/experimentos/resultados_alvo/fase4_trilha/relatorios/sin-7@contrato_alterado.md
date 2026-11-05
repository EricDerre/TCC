<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-7@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-7@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `status` · selo de probabilidade: **baixo** (p = 0,60) · **CONFLITO**: nenhum verbete entregue trata da causa respondida campo_renomeado

**IMPACTO (declarado):** `O botão de cancelar reserva não funciona porque a resposta da API não contém o campo `status` com o valor `Cancelado`, o que impede a detecção do pedido para cancelamento.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo status porque o sinal id_pedido: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes contrato-pedido, pedido-reserva, valor_fora_do_dominio estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,16. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida campo_renomeado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,60); trate como hipótese e confira o campo status antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 2207): regras diff_contra_contrato; antes {"chars": 116}, depois {"chars": 116}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id_pedido | inteiro |  |
| pessoas | texto | inteiro |

Trecho podado (hash `b88406ab40b56cca`):

```text
[{"pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

campo_renomeado e não campo_ausente: a escolha tem probabilidade 0,60 contra 0,16; verbete(s) na evidência: contrato-pedido, pedido-reserva, valor_fora_do_dominio

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 0,60 | sim |
| campo_ausente | 0,16 |  |
| valor_fora_do_dominio | 0,12 |  |
| tipo_divergente | 0,04 |  |
| resposta_truncada | 0,04 |  |
| formato_de_data_divergente | 0,02 |  |
| estado_da_tela_divergente | 0,02 |  |
| nulo_inesperado | 0,01 |  |
| registro_duplicado | 0,01 |  |
| colecao_no_lugar_de_objeto | 0,01 |  |
| recurso_inexistente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| erro_interno_do_servidor | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"ids": ["contrato-pedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `status` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-7 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2206 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:08:26 | caso sin-7@contrato_alterado |
| 2207 | 2 | poda | programa | ao_vivo | 2026-11-05T01:08:26 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2208 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:08:26 | poda: escolha json/lista; id_pedido:ausente, pessoas:tipo_diferente; divergência não |
| 2209 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:08:26 | 3 de 39 verbetes entregues |
| 2210 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:08:26 | recuperacao: escolha contrato-pedido,pedido-reserva,valor_fora_do_dominio; divergência não |
| 2212 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:08:26 | {"etapa": "diagnostico", "sha": "e2a527490f5c4fba", "prompt_sha256": "e2a527490f5c", "chars": 3488, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2214 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:08:26 | diagnostico: 54,6 s |
| 2215 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:08:26 | causa_raiz: `campo_renomeado` |
| 2216 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:08:26 | campo: `status` |
| 2217 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:08:26 | impacto: `O botão de cancelar reserva não funciona porque a resposta da API não contém o campo `status` com o valor `Cancelado`, o que impede a detecção do pedido para cancelamento.` |
| 2218 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:08:26 | fonte: `[contrato-pedido]` |
| 2219 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:08:26 | fonte_citada: `contrato-pedido` |
| 2220 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:08:26 | quatro_linhas_presentes: confere |
| 2221 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:08:26 | rotulo_no_conjunto: confere |
| 2222 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:08:26 | fonte_existe_na_biblioteca: confere |
| 2223 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:08:26 | fonte_estava_no_contexto: confere |
| 2224 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:08:26 | campo_existe_no_caso: confere |
| 2225 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:08:26 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2226 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:08:26 | notas_nos_verbetes_citados: informativo |
| 2227 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:08:26 | impacto: nao_verificavel |
| 2228 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:08:26 | fonte_formato_valido: confere |
| 2229 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:08:26 | fonte_contem_termo_da_causa: nao_confere |
| 2230 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:08:26 | diagnostico: escolha campo_renomeado; divergência sim |

</details>

Nós de decisão:

- evento 2208, `poda`: escolha `json/lista; id_pedido:ausente, pessoas:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 2207 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id_pedido, pessoas (gen_ai: plan)
- evento 2210, `recuperacao`: escolha `contrato-pedido,pedido-reserva,valor_fora_do_dominio`; resultado verbetes_entregues; evidência: evento 2209 (verbete_entregue, contrato-pedido), evento 2209 (verbete_entregue, pedido-reserva), evento 2209 (verbete_entregue, valor_fora_do_dominio); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, valor_fora_do_dominio (gen_ai: retrieval)
- evento 2230, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 2207 (sinal_em_codigo), evento 2209 (verbete_entregue, contrato-pedido), evento 2209 (verbete_entregue, pedido-reserva), evento 2209 (verbete_entregue, valor_fora_do_dominio), evento 2214 (resposta), evento 2219 (verbete_citado, contrato-pedido); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-pedido, pedido-reserva, valor_fora_do_dominio (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2206 a 2230 da trilha; hash dos eventos deste caso: `2c84d6e19f998c04`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
