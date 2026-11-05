<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-1@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-1@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário não consegue acessar os detalhes do produto "Picanha ao Alho" ao clicar no botão "Saiba Mais...".`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, tempo_de_resposta_excedido, ancora-saiba-mais estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1340): regras diff_contra_contrato; antes {"chars": 27}, depois {"chars": 27}.

Trecho podado (hash `48ffb95010655367`):

```text
(nenhuma requisicao falhou)
```

## 3. Contraste com a segunda causa

localizador_quebrado e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: localizador_quebrado, tempo_de_resposta_excedido, ancora-saiba-mais

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 0,99 | sim |
| tempo_de_resposta_excedido | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `tempo_de_resposta_excedido`, `ancora-saiba-mais` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `ancora-saiba-mais` |
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
| 1339 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:21:12 | caso efe-1@sonda |
| 1340 | 2 | poda | programa | ao_vivo | 2026-11-05T00:21:12 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1341 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:21:12 | poda: escolha sem_contrato; divergência não |
| 1342 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:21:12 | 3 de 39 verbetes entregues |
| 1343 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:21:12 | recuperacao: escolha localizador_quebrado,tempo_de_resposta_excedido,ancora-saiba-mais; divergência não |
| 1345 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:21:12 | {"etapa": "diagnostico", "sha": "bb1c7e42987e6748", "prompt_sha256": "bb1c7e42987e", "chars": 3920, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1347 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:21:12 | diagnostico: 73,2 s |
| 1348 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:21:12 | causa_raiz: `localizador_quebrado` |
| 1349 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:21:12 | campo: `nenhum` |
| 1350 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:21:12 | impacto: `O usuário não consegue acessar os detalhes do produto "Picanha ao Alho" ao clicar no botão "Saiba Mais...".` |
| 1351 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:21:12 | fonte: `[localizador_quebrado]` |
| 1352 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:21:12 | fonte_citada: `localizador_quebrado` |
| 1353 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:21:12 | quatro_linhas_presentes: confere |
| 1354 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:21:12 | rotulo_no_conjunto: confere |
| 1355 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:21:12 | fonte_existe_na_biblioteca: confere |
| 1356 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:21:12 | fonte_estava_no_contexto: confere |
| 1357 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:21:12 | campo_existe_no_caso: nao_se_aplica |
| 1358 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:21:12 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1359 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:21:12 | notas_nos_verbetes_citados: informativo |
| 1360 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:21:12 | impacto: nao_verificavel |
| 1361 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:21:12 | fonte_formato_valido: confere |
| 1362 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:21:12 | fonte_contem_termo_da_causa: confere |
| 1363 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:21:12 | diagnostico: escolha localizador_quebrado; divergência não |

</details>

Nós de decisão:

- evento 1341, `poda`: escolha `sem_contrato`; resultado sem_contrato; evidência: evento 1340 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1343, `recuperacao`: escolha `localizador_quebrado,tempo_de_resposta_excedido,ancora-saiba-mais`; resultado verbetes_entregues; evidência: evento 1342 (verbete_entregue, localizador_quebrado), evento 1342 (verbete_entregue, tempo_de_resposta_excedido), evento 1342 (verbete_entregue, ancora-saiba-mais); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, tempo_de_resposta_excedido, ancora-saiba-mais (gen_ai: retrieval)
- evento 1363, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 1342 (verbete_entregue, localizador_quebrado), evento 1342 (verbete_entregue, tempo_de_resposta_excedido), evento 1342 (verbete_entregue, ancora-saiba-mais), evento 1347 (resposta), evento 1352 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, tempo_de_resposta_excedido, ancora-saiba-mais (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1339 a 1363 da trilha; hash dos eventos deste caso: `7c137d9a32cbce71`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
