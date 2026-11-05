<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-11@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-11@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `itens` · selo de probabilidade: **medio** (p = 0,96)

**IMPACTO (declarado):** `O usuário vê uma segunda página vazia, enquanto espera por 14 itens.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo itens porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 3187): regras diff_contra_contrato; antes {"chars": 26}, depois {"chars": 26}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | inteiro |  |
| nome | texto |  |
| resumo | texto\|nulo |  |
| tipo | texto |  |
| preco | numero |  |
| imagem | texto\|nulo |  |
| destaque | booleano |  |
| envelope | {total: inteiro, itens: lista} |  |
| total |  | inteiro |
| itens |  | lista |

Trecho podado (hash `b11bbd4fe23d15d4`):

```text
{"total": 14, "itens": []}
```

## 3. Contraste com a segunda causa

contagem_inconsistente e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,96 contra 0,00; verbete(s) na evidência: contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,96 | sim |
| estrutura_aninhada_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `estrutura_aninhada_divergente`, `tempo_de_resposta_excedido` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"ids": ["contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `itens` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-11 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3186 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:57:33 | caso tra-11@sonda |
| 3187 | 2 | poda | programa | ao_vivo | 2026-11-05T01:57:33 | corpo_http: 10 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3188 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:57:33 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado; divergência não |
| 3189 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:57:33 | 3 de 39 verbetes entregues |
| 3190 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:57:33 | recuperacao: escolha contagem_inconsistente,estrutura_aninhada_divergente,tempo_de_resposta_excedido; divergência não |
| 3192 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:57:33 | {"etapa": "diagnostico", "sha": "cae609a8499a1b6a", "prompt_sha256": "cae609a8499a", "chars": 3614, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3194 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:57:33 | diagnostico: 54,9 s |
| 3195 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:57:33 | causa_raiz: `contagem_inconsistente` |
| 3196 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:57:33 | campo: `itens` |
| 3197 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:57:33 | impacto: `O usuário vê uma segunda página vazia, enquanto espera por 14 itens.` |
| 3198 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:57:33 | fonte: `[contagem_inconsistente]` |
| 3199 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:57:33 | fonte_citada: `contagem_inconsistente` |
| 3200 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:57:33 | quatro_linhas_presentes: confere |
| 3201 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:57:33 | rotulo_no_conjunto: confere |
| 3202 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:57:33 | fonte_existe_na_biblioteca: confere |
| 3203 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:57:33 | fonte_estava_no_contexto: confere |
| 3204 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:57:33 | campo_existe_no_caso: confere |
| 3205 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:57:33 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3206 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:57:33 | notas_nos_verbetes_citados: informativo |
| 3207 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:57:33 | impacto: nao_verificavel |
| 3208 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:57:33 | fonte_formato_valido: confere |
| 3209 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:57:33 | fonte_contem_termo_da_causa: confere |
| 3210 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:57:33 | diagnostico: escolha contagem_inconsistente; divergência não |

</details>

Nós de decisão:

- evento 3188, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado`; resultado sinais_em_codigo; evidência: evento 3187 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, envelope, total, itens (gen_ai: plan)
- evento 3190, `recuperacao`: escolha `contagem_inconsistente,estrutura_aninhada_divergente,tempo_de_resposta_excedido`; resultado verbetes_entregues; evidência: evento 3189 (verbete_entregue, contagem_inconsistente), evento 3189 (verbete_entregue, estrutura_aninhada_divergente), evento 3189 (verbete_entregue, tempo_de_resposta_excedido); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido (gen_ai: retrieval)
- evento 3210, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 3187 (sinal_em_codigo), evento 3189 (verbete_entregue, contagem_inconsistente), evento 3189 (verbete_entregue, estrutura_aninhada_divergente), evento 3189 (verbete_entregue, tempo_de_resposta_excedido), evento 3194 (resposta), evento 3199 (verbete_citado, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3186 a 3210 da trilha; hash dos eventos deste caso: `e6f9f1b0ebbabcf5`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
