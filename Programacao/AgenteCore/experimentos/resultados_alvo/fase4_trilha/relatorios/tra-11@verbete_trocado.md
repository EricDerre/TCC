<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-11@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-11@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estrutura_aninhada_divergente` · **CAMPO:** `itens` · selo de probabilidade: **baixo** (p = 0,63)

**IMPACTO (declarado):** `A interface exibe uma lista vazia, enquanto o backend indica que há 14 produtos disponíveis.`

Justificativa (gerada por molde): O agente respondeu estrutura_aninhada_divergente no campo itens porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes escala_ou_unidade_errada, estrutura_aninhada_divergente, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, contagem_inconsistente, ficou com probabilidade 0,33. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,63); trate como hipótese e confira o campo itens antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 3212): regras diff_contra_contrato; antes {"chars": 26}, depois {"chars": 26}.

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

estrutura_aninhada_divergente e não contagem_inconsistente: a escolha tem probabilidade 0,63 contra 0,33; verbete(s) na evidência: escala_ou_unidade_errada, estrutura_aninhada_divergente, tempo_de_resposta_excedido

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estrutura_aninhada_divergente | 0,63 | sim |
| contagem_inconsistente | 0,33 |  |
| resposta_truncada | 0,02 |  |
| escala_ou_unidade_errada | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[estrutura_aninhada_divergente]`; verbetes citados: `estrutura_aninhada_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `escala_ou_unidade_errada`, `estrutura_aninhada_divergente`, `tempo_de_resposta_excedido` |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[estrutura_aninhada_divergente]` | confere | {"ids": ["estrutura_aninhada_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `estrutura_aninhada_divergente` | confere | {"termo": "estrutura_aninhada_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `itens` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-11 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3211 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:58:32 | caso tra-11@verbete_trocado |
| 3212 | 2 | poda | programa | ao_vivo | 2026-11-05T01:58:32 | corpo_http: 10 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3213 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:58:32 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado; divergência não |
| 3214 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:58:32 | 3 de 39 verbetes entregues |
| 3215 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:58:32 | recuperacao: escolha escala_ou_unidade_errada,estrutura_aninhada_divergente,tempo_de_resposta_excedido; divergência não |
| 3216 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:58:32 | {"etapa": "diagnostico", "sha": "dd99b2937d91ad13", "prompt_sha256": "dd99b2937d91", "chars": 3782, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3218 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:58:32 | diagnostico: 15,6 s |
| 3219 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:58:32 | causa_raiz: `estrutura_aninhada_divergente` |
| 3220 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:58:32 | campo: `itens` |
| 3221 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:58:32 | impacto: `A interface exibe uma lista vazia, enquanto o backend indica que há 14 produtos disponíveis.` |
| 3222 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:58:32 | fonte: `[estrutura_aninhada_divergente]` |
| 3223 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:58:32 | fonte_citada: `estrutura_aninhada_divergente` |
| 3224 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:32 | quatro_linhas_presentes: confere |
| 3225 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:32 | rotulo_no_conjunto: confere |
| 3226 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:32 | fonte_existe_na_biblioteca: confere |
| 3227 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:32 | fonte_estava_no_contexto: confere |
| 3228 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:32 | campo_existe_no_caso: confere |
| 3229 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:32 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3230 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:32 | notas_nos_verbetes_citados: informativo |
| 3231 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:32 | impacto: nao_verificavel |
| 3232 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:32 | fonte_formato_valido: confere |
| 3233 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:32 | fonte_contem_termo_da_causa: confere |
| 3234 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:58:32 | diagnostico: escolha estrutura_aninhada_divergente; divergência não |

</details>

Nós de decisão:

- evento 3213, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado`; resultado sinais_em_codigo; evidência: evento 3212 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, envelope, total, itens (gen_ai: plan)
- evento 3215, `recuperacao`: escolha `escala_ou_unidade_errada,estrutura_aninhada_divergente,tempo_de_resposta_excedido`; resultado verbetes_entregues; evidência: evento 3214 (verbete_entregue, escala_ou_unidade_errada), evento 3214 (verbete_entregue, estrutura_aninhada_divergente), evento 3214 (verbete_entregue, tempo_de_resposta_excedido); divergência: não; falha: nenhuma; prov.used: escala_ou_unidade_errada, estrutura_aninhada_divergente, tempo_de_resposta_excedido (gen_ai: retrieval)
- evento 3234, `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido; evidência: evento 3212 (sinal_em_codigo), evento 3214 (verbete_entregue, escala_ou_unidade_errada), evento 3214 (verbete_entregue, estrutura_aninhada_divergente), evento 3214 (verbete_entregue, tempo_de_resposta_excedido), evento 3218 (resposta), evento 3223 (verbete_citado, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: escala_ou_unidade_errada, estrutura_aninhada_divergente, tempo_de_resposta_excedido (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3211 a 3234 da trilha; hash dos eventos deste caso: `01c0d213648326b0`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
