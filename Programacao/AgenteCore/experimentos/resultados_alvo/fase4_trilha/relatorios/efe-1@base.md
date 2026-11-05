<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-1@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,90) · **CONFLITO**: a remoção do verbete tempo_de_resposta_excedido mudou a resposta de tempo_de_resposta_excedido para localizador_quebrado; a troca do verbete tempo_de_resposta_excedido por um errado mudou a resposta de tempo_de_resposta_excedido para localizador_quebrado

**IMPACTO (declarado):** `O usuário não consegue acessar os detalhes do produto "Picanha ao Alho" devido ao tempo de resposta excedido.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido porque os verbetes localizador_quebrado, tempo_de_resposta_excedido, ancora-saiba-mais estavam entre os entregues ao modelo. A segunda causa, localizador_quebrado, ficou com probabilidade 0,08. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete tempo_de_resposta_excedido mudou a resposta (de tempo_de_resposta_excedido para localizador_quebrado), então ele pesou na decisão. A troca do verbete tempo_de_resposta_excedido por um verbete errado mudou a resposta (de tempo_de_resposta_excedido para localizador_quebrado). A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a remoção do verbete tempo_de_resposta_excedido mudou a resposta de tempo_de_resposta_excedido para localizador_quebrado; a troca do verbete tempo_de_resposta_excedido por um errado mudou a resposta de tempo_de_resposta_excedido para localizador_quebrado.

## 2. Evidência

Poda de `corpo_http` (evento 1302): regras diff_contra_contrato; antes {"chars": 27}, depois {"chars": 27}.

Trecho podado (hash `48ffb95010655367`):

```text
(nenhuma requisicao falhou)
```

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não localizador_quebrado: a escolha tem probabilidade 0,90 contra 0,08; verbete(s) na evidência: localizador_quebrado, tempo_de_resposta_excedido, ancora-saiba-mais

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 0,90 | sim |
| localizador_quebrado | 0,08 |  |
| limite_de_requisicoes | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `localizador_quebrado`, `tempo_de_resposta_excedido`, `ancora-saiba-mais` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido` |
| fonte_formato_valido | `[tempo_de_resposta_excedido]` | confere | {"ids": ["tempo_de_resposta_excedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tempo_de_resposta_excedido` | confere | {"termo": "tempo_de_resposta_excedido"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `tempo_de_resposta_excedido` | tempo_de_resposta_excedido | localizador_quebrado | 0,90 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| troca | `tempo_de_resposta_excedido` | tempo_de_resposta_excedido | localizador_quebrado | 0,90 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| sem_documentacao | `` | tempo_de_resposta_excedido | tempo_de_resposta_excedido | 0,90 | 1,00 | sem efeito medido do contexto |
| repeticao_da_base | `` | tempo_de_resposta_excedido | tempo_de_resposta_excedido | 0,90 | 0,88 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-1 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1300 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:16:40 | caso efe-1 |
| 1302 | 2 | poda | programa | ao_vivo | 2026-11-05T00:16:40 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1303 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:16:40 | poda: escolha sem_contrato; divergência não |
| 1304 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:16:40 | 3 de 39 verbetes entregues |
| 1305 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:16:40 | recuperacao: escolha localizador_quebrado,tempo_de_resposta_excedido,ancora-saiba-mais; divergência não |
| 1307 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:16:40 | {"etapa": "diagnostico", "sha": "be9c0e6665c336d1", "prompt_sha256": "be9c0e6665c3", "chars": 3796, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1309 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:16:40 | diagnostico: 74,8 s |
| 1310 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:16:40 | causa_raiz: `tempo_de_resposta_excedido` |
| 1311 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:16:40 | campo: `nenhum` |
| 1312 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:16:40 | impacto: `O usuário não consegue acessar os detalhes do produto "Picanha ao Alho" devido ao tempo de resposta excedido.` |
| 1313 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:16:40 | fonte: `[tempo_de_resposta_excedido]` |
| 1314 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:16:40 | fonte_citada: `tempo_de_resposta_excedido` |
| 1315 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:16:40 | quatro_linhas_presentes: confere |
| 1316 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:16:40 | rotulo_no_conjunto: confere |
| 1317 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:16:40 | fonte_existe_na_biblioteca: confere |
| 1318 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:16:40 | fonte_estava_no_contexto: confere |
| 1319 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:16:40 | campo_existe_no_caso: nao_se_aplica |
| 1320 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:16:40 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1321 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:16:40 | notas_nos_verbetes_citados: informativo |
| 1322 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:16:40 | impacto: nao_verificavel |
| 1323 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:16:40 | fonte_formato_valido: confere |
| 1324 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:16:40 | fonte_contem_termo_da_causa: confere |
| 1327 | 23 | inferencia | programa | ao_vivo | 2026-11-05T00:16:40 | intervencao:remocao: 59,3 s |
| 1328 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T00:16:40 | remocao de tempo_de_resposta_excedido: rótulo tempo_de_resposta_excedido para localizador_quebrado |
| 1330 | 25 | inferencia | programa | ao_vivo | 2026-11-05T00:16:40 | intervencao:troca: 66,3 s |
| 1331 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T00:16:40 | troca de tempo_de_resposta_excedido: rótulo tempo_de_resposta_excedido para localizador_quebrado |
| 1334 | 27 | inferencia | programa | ao_vivo | 2026-11-05T00:16:40 | intervencao:sem_documentacao: 48,0 s |
| 1335 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T00:16:40 | sem_documentacao de None: rótulo tempo_de_resposta_excedido para tempo_de_resposta_excedido |
| 1336 | 29 | inferencia | programa | ao_vivo | 2026-11-05T00:16:40 | intervencao:repeticao_da_base: 18,8 s |
| 1337 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T00:16:40 | repeticao_da_base de None: rótulo tempo_de_resposta_excedido para tempo_de_resposta_excedido |
| 1338 | 31 | decisao | programa | ao_vivo | 2026-11-05T00:16:40 | diagnostico: escolha tempo_de_resposta_excedido; divergência sim |

</details>

Nós de decisão:

- evento 1303, `poda`: escolha `sem_contrato`; resultado sem_contrato; evidência: evento 1302 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1305, `recuperacao`: escolha `localizador_quebrado,tempo_de_resposta_excedido,ancora-saiba-mais`; resultado verbetes_entregues; evidência: evento 1304 (verbete_entregue, localizador_quebrado), evento 1304 (verbete_entregue, tempo_de_resposta_excedido), evento 1304 (verbete_entregue, ancora-saiba-mais); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, tempo_de_resposta_excedido, ancora-saiba-mais (gen_ai: retrieval)
- evento 1338, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 1304 (verbete_entregue, localizador_quebrado), evento 1304 (verbete_entregue, tempo_de_resposta_excedido), evento 1304 (verbete_entregue, ancora-saiba-mais), evento 1309 (resposta), evento 1314 (verbete_citado, tempo_de_resposta_excedido); divergência: sim; falha: nenhuma; prov.used: localizador_quebrado, tempo_de_resposta_excedido, ancora-saiba-mais (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1300 a 1338 da trilha; hash dos eventos deste caso: `ed2db2f96b2ff0a4`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
