<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-4`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-4@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `dado_desatualizado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: a inferência sem documentação mudou a resposta de dado_desatualizado para colecao_no_lugar_de_objeto

**IMPACTO (declarado):** `O usuário vê uma lista de pedidos antigos, sem a reserva recentemente criada.`

Justificativa (gerada por molde): O agente respondeu dado_desatualizado porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes contrato-pedido, dado_desatualizado, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. A remoção do verbete contrato-pedido não mudou a resposta: sem efeito medido do contexto. A troca do verbete contrato-pedido por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação mudou a resposta (de dado_desatualizado para colecao_no_lugar_de_objeto). (a probabilidade registrada é só um limite inferior: o rótulo saiu das alternativas devolvidas) A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a inferência sem documentação mudou a resposta de dado_desatualizado para colecao_no_lugar_de_objeto.

## 2. Evidência

Poda de `corpo_http` (evento 1209): regras diff_contra_contrato; antes {"chars": 224}, depois {"chars": 224}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `3eccd041da49c857`):

```text
POST devolveu {"id_pedido": 8, "status": "Em Analise", "pessoas": 6}. GET seguinte devolveu [{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

dado_desatualizado e não tempo_de_resposta_excedido: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-pedido, dado_desatualizado, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| dado_desatualizado | 1,00 | sim |
| tempo_de_resposta_excedido | 0,00 |  |
| registro_duplicado | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| tipo_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido], [dado_desatualizado]`; verbetes citados: `contrato-pedido`, `dado_desatualizado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado existe na biblioteca | `dado_desatualizado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `dado_desatualizado`, `pedido-reserva` |
| O verbete citado estava no contexto entregue ao modelo | `dado_desatualizado` | confere | contexto: `contrato-pedido`, `dado_desatualizado`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `dado_desatualizado` | confere | verbetes: `dado_desatualizado` |
| fonte_formato_valido | `[contrato-pedido], [dado_desatualizado]` | confere | {"ids": ["contrato-pedido", "dado_desatualizado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "dado_desatualizado"} |
| fonte_contem_termo_da_causa | `dado_desatualizado` | confere | {"termo": "dado_desatualizado"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `contrato-pedido` | dado_desatualizado | dado_desatualizado | 1,00 | 0,99 | sem efeito medido do contexto |
| troca | `contrato-pedido` | dado_desatualizado | dado_desatualizado | 1,00 | 1,00 | sem efeito medido do contexto |
| sem_documentacao | `` | dado_desatualizado | colecao_no_lugar_de_objeto | 1,00 | 0,00 | mudou a resposta: o verbete pesou na decisão (só um limite inferior da queda: o rótulo saiu das alternativas devolvidas) |
| repeticao_da_base | `` | dado_desatualizado | dado_desatualizado | 1,00 | 1,00 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-4 --sem-seletor`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1207 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:10:39 | caso run-4 |
| 1209 | 2 | poda | programa | ao_vivo | 2026-11-05T00:10:39 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1210 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:10:39 | poda: escolha nao_json; divergência não |
| 1211 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:10:39 | 3 de 39 verbetes entregues |
| 1212 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:10:39 | recuperacao: escolha contrato-pedido,dado_desatualizado,pedido-reserva; divergência não |
| 1214 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:10:39 | {"etapa": "diagnostico", "sha": "06ec125be14a2e3d", "prompt_sha256": "06ec125be14a", "chars": 3603, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1216 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:10:39 | diagnostico: 70,2 s |
| 1217 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:10:39 | causa_raiz: `dado_desatualizado` |
| 1218 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:10:39 | campo: `nenhum` |
| 1219 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:10:39 | impacto: `O usuário vê uma lista de pedidos antigos, sem a reserva recentemente criada.` |
| 1220 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:10:39 | fonte: `[contrato-pedido], [dado_desatualizado]` |
| 1221 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:10:39 | fonte_citada: `contrato-pedido` |
| 1222 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T00:10:39 | fonte_citada: `dado_desatualizado` |
| 1223 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | quatro_linhas_presentes: confere |
| 1224 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | rotulo_no_conjunto: confere |
| 1225 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | fonte_existe_na_biblioteca: confere |
| 1226 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | fonte_existe_na_biblioteca: confere |
| 1227 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | fonte_estava_no_contexto: confere |
| 1228 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | fonte_estava_no_contexto: confere |
| 1229 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | campo_existe_no_caso: nao_se_aplica |
| 1230 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1231 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | notas_nos_verbetes_citados: informativo |
| 1232 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | impacto: nao_verificavel |
| 1233 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | fonte_formato_valido: confere |
| 1234 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | fonte_contem_termo_da_causa: nao_confere |
| 1235 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:39 | fonte_contem_termo_da_causa: confere |
| 1238 | 27 | inferencia | programa | ao_vivo | 2026-11-05T00:10:39 | intervencao:remocao: 62,0 s |
| 1239 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T00:10:39 | remocao de contrato-pedido: rótulo dado_desatualizado para dado_desatualizado |
| 1241 | 29 | inferencia | programa | ao_vivo | 2026-11-05T00:10:39 | intervencao:troca: 68,9 s |
| 1242 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T00:10:39 | troca de contrato-pedido: rótulo dado_desatualizado para dado_desatualizado |
| 1245 | 31 | inferencia | programa | ao_vivo | 2026-11-05T00:10:39 | intervencao:sem_documentacao: 59,9 s |
| 1246 | 32 | intervencao | verificacao | ao_vivo | 2026-11-05T00:10:39 | sem_documentacao de None: rótulo dado_desatualizado para colecao_no_lugar_de_objeto |
| 1248 | 33 | inferencia | programa | ao_vivo | 2026-11-05T00:10:39 | intervencao:repeticao_da_base: 16,3 s |
| 1249 | 34 | intervencao | verificacao | ao_vivo | 2026-11-05T00:10:39 | repeticao_da_base de None: rótulo dado_desatualizado para dado_desatualizado |
| 1250 | 35 | decisao | programa | ao_vivo | 2026-11-05T00:10:39 | diagnostico: escolha dado_desatualizado; divergência sim |

</details>

Nós de decisão:

- evento 1210, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 1209 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1212, `recuperacao`: escolha `contrato-pedido,dado_desatualizado,pedido-reserva`; resultado verbetes_entregues; evidência: evento 1211 (verbete_entregue, contrato-pedido), evento 1211 (verbete_entregue, dado_desatualizado), evento 1211 (verbete_entregue, pedido-reserva); divergência: não; falha: nenhuma; prov.used: contrato-pedido, dado_desatualizado, pedido-reserva (gen_ai: retrieval)
- evento 1250, `diagnostico`: escolha `dado_desatualizado`; resultado rotulo_emitido; evidência: evento 1209 (sinal_em_codigo), evento 1211 (verbete_entregue, contrato-pedido), evento 1211 (verbete_entregue, dado_desatualizado), evento 1211 (verbete_entregue, pedido-reserva), evento 1216 (resposta), evento 1221 (verbete_citado, contrato-pedido), evento 1222 (verbete_citado, dado_desatualizado); divergência: sim; falha: nenhuma; prov.used: contrato-pedido, dado_desatualizado, pedido-reserva (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1207 a 1250 da trilha; hash dos eventos deste caso: `57cace524c554089`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
