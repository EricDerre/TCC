<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-4@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-4@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `dado_desatualizado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A reserva recém-criada não aparece na lista, aparecendo apenas após alguns minutos, devido a um atraso no cache do navegador ou proxy.`

Justificativa (gerada por molde): O agente respondeu dado_desatualizado porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes contrato-pedido, dado_desatualizado, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, registro_duplicado, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1252): regras diff_contra_contrato; antes {"chars": 224}, depois {"chars": 224}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `3eccd041da49c857`):

```text
POST devolveu {"id_pedido": 8, "status": "Em Analise", "pessoas": 6}. GET seguinte devolveu [{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

dado_desatualizado e não registro_duplicado: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-pedido, dado_desatualizado, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| dado_desatualizado | 1,00 | sim |
| registro_duplicado | 0,00 |  |
| tempo_de_resposta_excedido | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[dado_desatualizado]`; verbetes citados: `dado_desatualizado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `dado_desatualizado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `dado_desatualizado` | confere | contexto: `contrato-pedido`, `dado_desatualizado`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `dado_desatualizado` | confere | verbetes: `dado_desatualizado` |
| fonte_formato_valido | `[dado_desatualizado]` | confere | {"ids": ["dado_desatualizado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `dado_desatualizado` | confere | {"termo": "dado_desatualizado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-4 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1251 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:15:20 | caso run-4@sonda |
| 1252 | 2 | poda | programa | ao_vivo | 2026-11-05T00:15:20 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1253 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:15:20 | poda: escolha nao_json; divergência não |
| 1254 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:15:20 | 3 de 39 verbetes entregues |
| 1255 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:15:20 | recuperacao: escolha contrato-pedido,dado_desatualizado,pedido-reserva; divergência não |
| 1257 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:15:20 | {"etapa": "diagnostico", "sha": "3a3d48b662595e89", "prompt_sha256": "3a3d48b66259", "chars": 3719, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1259 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:15:20 | diagnostico: 55,6 s |
| 1260 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:15:20 | causa_raiz: `dado_desatualizado` |
| 1261 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:15:20 | campo: `nenhum` |
| 1262 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:15:20 | impacto: `A reserva recém-criada não aparece na lista, aparecendo apenas após alguns minutos, devido a um atraso no cache do navegador ou proxy.` |
| 1263 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:15:20 | fonte: `[dado_desatualizado]` |
| 1264 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:15:20 | fonte_citada: `dado_desatualizado` |
| 1265 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:15:20 | quatro_linhas_presentes: confere |
| 1266 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:15:20 | rotulo_no_conjunto: confere |
| 1267 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:15:20 | fonte_existe_na_biblioteca: confere |
| 1268 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:15:20 | fonte_estava_no_contexto: confere |
| 1269 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:15:20 | campo_existe_no_caso: nao_se_aplica |
| 1270 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:15:20 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1271 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:15:20 | notas_nos_verbetes_citados: informativo |
| 1272 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:15:20 | impacto: nao_verificavel |
| 1273 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:15:20 | fonte_formato_valido: confere |
| 1274 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:15:20 | fonte_contem_termo_da_causa: confere |
| 1275 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:15:20 | diagnostico: escolha dado_desatualizado; divergência não |

</details>

Nós de decisão:

- evento 1253, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 1252 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1255, `recuperacao`: escolha `contrato-pedido,dado_desatualizado,pedido-reserva`; resultado verbetes_entregues; evidência: evento 1254 (verbete_entregue, contrato-pedido), evento 1254 (verbete_entregue, dado_desatualizado), evento 1254 (verbete_entregue, pedido-reserva); divergência: não; falha: nenhuma; prov.used: contrato-pedido, dado_desatualizado, pedido-reserva (gen_ai: retrieval)
- evento 1275, `diagnostico`: escolha `dado_desatualizado`; resultado rotulo_emitido; evidência: evento 1252 (sinal_em_codigo), evento 1254 (verbete_entregue, contrato-pedido), evento 1254 (verbete_entregue, dado_desatualizado), evento 1254 (verbete_entregue, pedido-reserva), evento 1259 (resposta), evento 1264 (verbete_citado, dado_desatualizado); divergência: não; falha: nenhuma; prov.used: contrato-pedido, dado_desatualizado, pedido-reserva (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1251 a 1275 da trilha; hash dos eventos deste caso: `0514fda5ad5c8f54`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
