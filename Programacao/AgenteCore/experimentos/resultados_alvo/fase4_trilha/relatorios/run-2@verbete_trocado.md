<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-2@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-2@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 0,99) · **CONFLITO**: a FONTE cita o verbete tempo_de_resposta_excedido, fora do contexto entregue

**IMPACTO (declarado):** `A página fica carregando e depois exibe erro de rede, pois a requisição demora mais de 30 segundos e é cancelada pelo cliente.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes corpo_nao_e_json, limite_de_requisicoes, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, estado_da_tela_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), 1 fora do contexto entregue (tempo_de_resposta_excedido). O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a FONTE cita o verbete tempo_de_resposta_excedido, fora do contexto entregue. Este nó está marcado com a falha citacao_fora_do_contexto (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 1183): regras diff_contra_contrato; antes {"chars": 55}, depois {"chars": 55}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `f01d079c96a2a729`):

```text
(sem resposta apos 30s; conexao encerrada pelo cliente)
```

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não estado_da_tela_divergente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: corpo_nao_e_json, limite_de_requisicoes, estado_da_tela_divergente, tempo_de_resposta_excedido

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 0,99 | sim |
| estado_da_tela_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| limite_de_requisicoes | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | **não confere** | contexto: `corpo_nao_e_json`, `limite_de_requisicoes`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `limite_de_requisicoes` |
| fonte_formato_valido | `[tempo_de_resposta_excedido]` | confere | {"ids": ["tempo_de_resposta_excedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tempo_de_resposta_excedido` | confere | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-2 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1182 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:10:14 | caso run-2@verbete_trocado |
| 1183 | 2 | poda | programa | ao_vivo | 2026-11-05T00:10:14 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1184 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:10:14 | poda: escolha nao_json; divergência não |
| 1185 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:10:14 | 3 de 39 verbetes entregues |
| 1186 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:10:14 | recuperacao: escolha corpo_nao_e_json,limite_de_requisicoes,estado_da_tela_divergente; divergência não |
| 1187 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:10:14 | {"etapa": "diagnostico", "sha": "1246df8e484d53f5", "prompt_sha256": "1246df8e484d", "chars": 3687, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1189 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:10:14 | diagnostico: 18,8 s |
| 1190 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:10:14 | causa_raiz: `tempo_de_resposta_excedido` |
| 1191 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:10:14 | campo: `nenhum` |
| 1192 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:10:14 | impacto: `A página fica carregando e depois exibe erro de rede, pois a requisição demora mais de 30 segundos e é cancelada pelo cliente.` |
| 1193 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:10:14 | fonte: `[tempo_de_resposta_excedido]` |
| 1194 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:10:14 | fonte_citada: `tempo_de_resposta_excedido` |
| 1195 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:14 | quatro_linhas_presentes: confere |
| 1196 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:14 | rotulo_no_conjunto: confere |
| 1197 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:14 | fonte_existe_na_biblioteca: confere |
| 1198 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:14 | fonte_estava_no_contexto: nao_confere |
| 1199 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:14 | campo_existe_no_caso: nao_se_aplica |
| 1200 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:14 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1201 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:14 | notas_nos_verbetes_citados: informativo |
| 1202 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:14 | impacto: nao_verificavel |
| 1203 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:14 | fonte_formato_valido: confere |
| 1204 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:10:14 | fonte_contem_termo_da_causa: confere |
| 1205 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:10:14 | diagnostico: escolha tempo_de_resposta_excedido; divergência sim |

</details>

Nós de decisão:

- evento 1184, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 1183 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1186, `recuperacao`: escolha `corpo_nao_e_json,limite_de_requisicoes,estado_da_tela_divergente`; resultado verbetes_entregues; evidência: evento 1185 (verbete_entregue, corpo_nao_e_json), evento 1185 (verbete_entregue, limite_de_requisicoes), evento 1185 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: corpo_nao_e_json, limite_de_requisicoes, estado_da_tela_divergente (gen_ai: retrieval)
- evento 1205, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 1183 (sinal_em_codigo), evento 1185 (verbete_entregue, corpo_nao_e_json), evento 1185 (verbete_entregue, limite_de_requisicoes), evento 1185 (verbete_entregue, estado_da_tela_divergente), evento 1189 (resposta), evento 1194 (verbete_citado, tempo_de_resposta_excedido); divergência: sim; falha: citacao_fora_do_contexto; prov.used: corpo_nao_e_json, limite_de_requisicoes, estado_da_tela_divergente, tempo_de_resposta_excedido (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1182 a 1205 da trilha; hash dos eventos deste caso: `16afde0e097ba2b4`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
