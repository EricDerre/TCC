<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-2`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-2@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A página fica carregando e depois exibe erro de rede, pois a requisição demorou mais do que o esperado e foi encerrada pelo cliente.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes tempo_de_resposta_excedido, limite_de_requisicoes, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, limite_de_requisicoes, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete tempo_de_resposta_excedido não mudou a resposta: sem efeito medido do contexto. A troca do verbete tempo_de_resposta_excedido por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1118): regras diff_contra_contrato; antes {"chars": 55}, depois {"chars": 55}.

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
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `tempo_de_resposta_excedido`, `limite_de_requisicoes`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido`, `limite_de_requisicoes` |
| fonte_formato_valido | `[tempo_de_resposta_excedido]` | confere | {"ids": ["tempo_de_resposta_excedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tempo_de_resposta_excedido` | confere | {"termo": "tempo_de_resposta_excedido"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `tempo_de_resposta_excedido` | tempo_de_resposta_excedido | tempo_de_resposta_excedido | 1,00 | 1,00 | sem efeito medido do contexto |
| troca | `tempo_de_resposta_excedido` | tempo_de_resposta_excedido | tempo_de_resposta_excedido | 1,00 | 0,99 | sem efeito medido do contexto |
| sem_documentacao | `` | tempo_de_resposta_excedido | tempo_de_resposta_excedido | 1,00 | 1,00 | sem efeito medido do contexto |
| repeticao_da_base | `` | tempo_de_resposta_excedido | tempo_de_resposta_excedido | 1,00 | 1,00 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-2 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1116 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:04:47 | caso run-2 |
| 1118 | 2 | poda | programa | ao_vivo | 2026-11-05T00:04:47 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1119 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:04:47 | poda: escolha nao_json; divergência não |
| 1120 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:04:47 | 3 de 39 verbetes entregues |
| 1121 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:04:47 | recuperacao: escolha tempo_de_resposta_excedido,limite_de_requisicoes,estado_da_tela_divergente; divergência não |
| 1123 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:04:47 | {"etapa": "diagnostico", "sha": "2c4d4396829210af", "prompt_sha256": "2c4d43968292", "chars": 3445, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1125 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:04:47 | diagnostico: 67,9 s |
| 1126 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:04:47 | causa_raiz: `tempo_de_resposta_excedido` |
| 1127 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:04:47 | campo: `nenhum` |
| 1128 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:04:47 | impacto: `A página fica carregando e depois exibe erro de rede, pois a requisição demorou mais do que o esperado e foi encerrada pelo cliente.` |
| 1129 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:04:47 | fonte: `[tempo_de_resposta_excedido]` |
| 1130 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:04:47 | fonte_citada: `tempo_de_resposta_excedido` |
| 1131 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:47 | quatro_linhas_presentes: confere |
| 1132 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:47 | rotulo_no_conjunto: confere |
| 1133 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:47 | fonte_existe_na_biblioteca: confere |
| 1134 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:47 | fonte_estava_no_contexto: confere |
| 1135 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:47 | campo_existe_no_caso: nao_se_aplica |
| 1136 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:47 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1137 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:47 | notas_nos_verbetes_citados: informativo |
| 1138 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:47 | impacto: nao_verificavel |
| 1139 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:47 | fonte_formato_valido: confere |
| 1140 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:47 | fonte_contem_termo_da_causa: confere |
| 1143 | 23 | inferencia | programa | ao_vivo | 2026-11-05T00:04:47 | intervencao:remocao: 61,7 s |
| 1144 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T00:04:47 | remocao de tempo_de_resposta_excedido: rótulo tempo_de_resposta_excedido para tempo_de_resposta_excedido |
| 1147 | 25 | inferencia | programa | ao_vivo | 2026-11-05T00:04:47 | intervencao:troca: 72,2 s |
| 1148 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T00:04:47 | troca de tempo_de_resposta_excedido: rótulo tempo_de_resposta_excedido para tempo_de_resposta_excedido |
| 1151 | 27 | inferencia | programa | ao_vivo | 2026-11-05T00:04:47 | intervencao:sem_documentacao: 39,6 s |
| 1152 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T00:04:47 | sem_documentacao de None: rótulo tempo_de_resposta_excedido para tempo_de_resposta_excedido |
| 1154 | 29 | inferencia | programa | ao_vivo | 2026-11-05T00:04:47 | intervencao:repeticao_da_base: 19,5 s |
| 1155 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T00:04:47 | repeticao_da_base de None: rótulo tempo_de_resposta_excedido para tempo_de_resposta_excedido |
| 1156 | 31 | decisao | programa | ao_vivo | 2026-11-05T00:04:47 | diagnostico: escolha tempo_de_resposta_excedido; divergência não |

</details>

Nós de decisão:

- evento 1119, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 1118 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1121, `recuperacao`: escolha `tempo_de_resposta_excedido,limite_de_requisicoes,estado_da_tela_divergente`; resultado verbetes_entregues; evidência: evento 1120 (verbete_entregue, tempo_de_resposta_excedido), evento 1120 (verbete_entregue, limite_de_requisicoes), evento 1120 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: tempo_de_resposta_excedido, limite_de_requisicoes, estado_da_tela_divergente (gen_ai: retrieval)
- evento 1156, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 1118 (sinal_em_codigo), evento 1120 (verbete_entregue, tempo_de_resposta_excedido), evento 1120 (verbete_entregue, limite_de_requisicoes), evento 1120 (verbete_entregue, estado_da_tela_divergente), evento 1125 (resposta), evento 1130 (verbete_citado, tempo_de_resposta_excedido); divergência: não; falha: nenhuma; prov.used: tempo_de_resposta_excedido, limite_de_requisicoes, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1116 a 1156 da trilha; hash dos eventos deste caso: `7ccd4515cacfc3fc`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
