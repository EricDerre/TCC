<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-1@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-1@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não consegue acessar os detalhes do produto "Picanha ao Alho" devido ao tempo esgotado na busca pelo botão de detalhes.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, estado_da_tela_divergente, ancora-saiba-mais estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1365): regras diff_contra_contrato; antes {"chars": 27}, depois {"chars": 27}.

Trecho podado (hash `48ffb95010655367`):

```text
(nenhuma requisicao falhou)
```

## 3. Contraste com a segunda causa

localizador_quebrado e não tempo_de_resposta_excedido: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: localizador_quebrado, estado_da_tela_divergente, ancora-saiba-mais

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 1,00 | sim |
| tempo_de_resposta_excedido | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| nulo_inesperado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `estado_da_tela_divergente`, `ancora-saiba-mais` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `estado_da_tela_divergente`, `ancora-saiba-mais` |
| fonte_formato_valido | `[localizador_quebrado]` | confere | {"ids": ["localizador_quebrado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-1 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1364 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:22:29 | caso efe-1@verbete_trocado |
| 1365 | 2 | poda | programa | ao_vivo | 2026-11-05T00:22:29 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1366 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:22:29 | poda: escolha sem_contrato; divergência não |
| 1367 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:22:29 | 3 de 39 verbetes entregues |
| 1368 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:22:29 | recuperacao: escolha localizador_quebrado,estado_da_tela_divergente,ancora-saiba-mais; divergência não |
| 1369 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:22:29 | {"etapa": "diagnostico", "sha": "7db709c9bf54eec5", "prompt_sha256": "7db709c9bf54", "chars": 3884, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1370 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:22:29 | diagnostico: 18,0 s |
| 1371 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:22:29 | causa_raiz: `localizador_quebrado` |
| 1372 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:22:29 | campo: `nenhum` |
| 1373 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:22:29 | impacto: `O usuário não consegue acessar os detalhes do produto "Picanha ao Alho" devido ao tempo esgotado na busca pelo botão de detalhes.` |
| 1374 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:22:29 | fonte: `[localizador_quebrado]` |
| 1375 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:22:29 | fonte_citada: `localizador_quebrado` |
| 1376 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:29 | quatro_linhas_presentes: confere |
| 1377 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:29 | rotulo_no_conjunto: confere |
| 1378 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:29 | fonte_existe_na_biblioteca: confere |
| 1379 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:29 | fonte_estava_no_contexto: confere |
| 1380 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:29 | campo_existe_no_caso: nao_se_aplica |
| 1381 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:29 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1382 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:29 | notas_nos_verbetes_citados: informativo |
| 1383 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:29 | impacto: nao_verificavel |
| 1384 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:29 | fonte_formato_valido: confere |
| 1385 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:22:29 | fonte_contem_termo_da_causa: confere |
| 1386 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:22:29 | diagnostico: escolha localizador_quebrado; divergência não |

</details>

Nós de decisão:

- evento 1366, `poda`: escolha `sem_contrato`; resultado sem_contrato; evidência: evento 1365 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1368, `recuperacao`: escolha `localizador_quebrado,estado_da_tela_divergente,ancora-saiba-mais`; resultado verbetes_entregues; evidência: evento 1367 (verbete_entregue, localizador_quebrado), evento 1367 (verbete_entregue, estado_da_tela_divergente), evento 1367 (verbete_entregue, ancora-saiba-mais); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, estado_da_tela_divergente, ancora-saiba-mais (gen_ai: retrieval)
- evento 1386, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 1367 (verbete_entregue, localizador_quebrado), evento 1367 (verbete_entregue, estado_da_tela_divergente), evento 1367 (verbete_entregue, ancora-saiba-mais), evento 1370 (resposta), evento 1375 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, estado_da_tela_divergente, ancora-saiba-mais (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1364 a 1386 da trilha; hash dos eventos deste caso: `3559dd4c013d9179`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
