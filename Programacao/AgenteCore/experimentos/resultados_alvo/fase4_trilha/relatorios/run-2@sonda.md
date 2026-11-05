<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-2@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-2@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A página fica carregando e depois exibe erro de rede, pois o cliente desistiu antes da resposta chegar.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes tempo_de_resposta_excedido, limite_de_requisicoes, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, limite_de_requisicoes, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1158): regras diff_contra_contrato; antes {"chars": 55}, depois {"chars": 55}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `f01d079c96a2a729`):

```text
(sem resposta apos 30s; conexao encerrada pelo cliente)
```

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não limite_de_requisicoes: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: tempo_de_resposta_excedido, limite_de_requisicoes, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 1,00 | sim |
| limite_de_requisicoes | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `tempo_de_resposta_excedido`, `limite_de_requisicoes`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido`, `limite_de_requisicoes` |
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
| 1157 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:09:12 | caso run-2@sonda |
| 1158 | 2 | poda | programa | ao_vivo | 2026-11-05T00:09:12 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1159 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:09:12 | poda: escolha nao_json; divergência não |
| 1160 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:09:12 | 3 de 39 verbetes entregues |
| 1161 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:09:12 | recuperacao: escolha tempo_de_resposta_excedido,limite_de_requisicoes,estado_da_tela_divergente; divergência não |
| 1163 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:09:12 | {"etapa": "diagnostico", "sha": "2caf6d491691c375", "prompt_sha256": "2caf6d491691", "chars": 3569, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1165 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:09:12 | diagnostico: 57,7 s |
| 1166 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:09:12 | causa_raiz: `tempo_de_resposta_excedido` |
| 1167 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:09:12 | campo: `nenhum` |
| 1168 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:09:12 | impacto: `A página fica carregando e depois exibe erro de rede, pois o cliente desistiu antes da resposta chegar.` |
| 1169 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:09:12 | fonte: `[tempo_de_resposta_excedido]` |
| 1170 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:09:12 | fonte_citada: `tempo_de_resposta_excedido` |
| 1171 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:09:12 | quatro_linhas_presentes: confere |
| 1172 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:09:12 | rotulo_no_conjunto: confere |
| 1173 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:09:12 | fonte_existe_na_biblioteca: confere |
| 1174 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:09:12 | fonte_estava_no_contexto: confere |
| 1175 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:09:12 | campo_existe_no_caso: nao_se_aplica |
| 1176 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:09:12 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1177 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:09:12 | notas_nos_verbetes_citados: informativo |
| 1178 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:09:12 | impacto: nao_verificavel |
| 1179 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:09:12 | fonte_formato_valido: confere |
| 1180 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:09:12 | fonte_contem_termo_da_causa: confere |
| 1181 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:09:12 | diagnostico: escolha tempo_de_resposta_excedido; divergência não |

</details>

Nós de decisão:

- evento 1159, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 1158 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1161, `recuperacao`: escolha `tempo_de_resposta_excedido,limite_de_requisicoes,estado_da_tela_divergente`; resultado verbetes_entregues; evidência: evento 1160 (verbete_entregue, tempo_de_resposta_excedido), evento 1160 (verbete_entregue, limite_de_requisicoes), evento 1160 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: tempo_de_resposta_excedido, limite_de_requisicoes, estado_da_tela_divergente (gen_ai: retrieval)
- evento 1181, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 1158 (sinal_em_codigo), evento 1160 (verbete_entregue, tempo_de_resposta_excedido), evento 1160 (verbete_entregue, limite_de_requisicoes), evento 1160 (verbete_entregue, estado_da_tela_divergente), evento 1165 (resposta), evento 1170 (verbete_citado, tempo_de_resposta_excedido); divergência: não; falha: nenhuma; prov.used: tempo_de_resposta_excedido, limite_de_requisicoes, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1157 a 1181 da trilha; hash dos eventos deste caso: `45c7d7b2d7c29ac9`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
