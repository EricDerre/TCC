<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-2@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-2@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estado_da_tela_divergente` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `A tela do cliente não reflete o status 'Cancelado' do pedido 7, continuando a exibir 'Em Analise'.`

Justificativa (gerada por molde): O agente respondeu estado_da_tela_divergente porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes contrato-pedido, estado_da_tela_divergente, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, chave_de_juncao_errada, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1429): regras diff_contra_contrato; antes {"chars": 54}, depois {"chars": 54}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `9747f76426520e17`):

```text
A API devolveu {"id_pedido": 7, "status": "Cancelado"}
```

## 3. Contraste com a segunda causa

estado_da_tela_divergente e não chave_de_juncao_errada: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: contrato-pedido, estado_da_tela_divergente, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estado_da_tela_divergente | 0,99 | sim |
| chave_de_juncao_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| registro_duplicado | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| dado_desatualizado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[estado_da_tela_divergente]`; verbetes citados: `estado_da_tela_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estado_da_tela_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estado_da_tela_divergente` | confere | contexto: `contrato-pedido`, `estado_da_tela_divergente`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `estado_da_tela_divergente` | confere | verbetes: `estado_da_tela_divergente` |
| fonte_formato_valido | `[estado_da_tela_divergente]` | confere | {"ids": ["estado_da_tela_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `estado_da_tela_divergente` | confere | {"termo": "estado_da_tela_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-2 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1428 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:26:09 | caso efe-2@sonda |
| 1429 | 2 | poda | programa | ao_vivo | 2026-11-05T00:26:09 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1430 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:26:09 | poda: escolha nao_json; divergência não |
| 1431 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:26:09 | 3 de 39 verbetes entregues |
| 1432 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:26:09 | recuperacao: escolha contrato-pedido,estado_da_tela_divergente,pedido-reserva; divergência não |
| 1434 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:26:09 | {"etapa": "diagnostico", "sha": "408fccf07a5d7737", "prompt_sha256": "408fccf07a5d", "chars": 3539, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1435 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:26:09 | diagnostico: 63,3 s |
| 1436 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:26:09 | causa_raiz: `estado_da_tela_divergente` |
| 1437 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:26:09 | campo: `nenhum` |
| 1438 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:26:09 | impacto: `A tela do cliente não reflete o status 'Cancelado' do pedido 7, continuando a exibir 'Em Analise'.` |
| 1439 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:26:09 | fonte: `[estado_da_tela_divergente]` |
| 1440 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:26:09 | fonte_citada: `estado_da_tela_divergente` |
| 1441 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:26:09 | quatro_linhas_presentes: confere |
| 1442 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:26:09 | rotulo_no_conjunto: confere |
| 1443 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:26:09 | fonte_existe_na_biblioteca: confere |
| 1444 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:26:09 | fonte_estava_no_contexto: confere |
| 1445 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:26:09 | campo_existe_no_caso: nao_se_aplica |
| 1446 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:26:09 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1447 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:26:09 | notas_nos_verbetes_citados: informativo |
| 1448 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:26:09 | impacto: nao_verificavel |
| 1449 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:26:09 | fonte_formato_valido: confere |
| 1450 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:26:09 | fonte_contem_termo_da_causa: confere |
| 1451 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:26:09 | diagnostico: escolha estado_da_tela_divergente; divergência não |

</details>

Nós de decisão:

- evento 1430, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 1429 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1432, `recuperacao`: escolha `contrato-pedido,estado_da_tela_divergente,pedido-reserva`; resultado verbetes_entregues; evidência: evento 1431 (verbete_entregue, contrato-pedido), evento 1431 (verbete_entregue, estado_da_tela_divergente), evento 1431 (verbete_entregue, pedido-reserva); divergência: não; falha: nenhuma; prov.used: contrato-pedido, estado_da_tela_divergente, pedido-reserva (gen_ai: retrieval)
- evento 1451, `diagnostico`: escolha `estado_da_tela_divergente`; resultado rotulo_emitido; evidência: evento 1429 (sinal_em_codigo), evento 1431 (verbete_entregue, contrato-pedido), evento 1431 (verbete_entregue, estado_da_tela_divergente), evento 1431 (verbete_entregue, pedido-reserva), evento 1435 (resposta), evento 1440 (verbete_citado, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: contrato-pedido, estado_da_tela_divergente, pedido-reserva (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1428 a 1451 da trilha; hash dos eventos deste caso: `963a5856625b3818`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
