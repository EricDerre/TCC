<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-10@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-10@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `limite_de_requisicoes` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,84)

**IMPACTO (declarado):** `O usuário recebe um erro indicando que o limite de requisições foi excedido, impedindo a visualização correta dos produtos.`

Justificativa (gerada por molde): O agente respondeu limite_de_requisicoes no campo id porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 3459): regras diff_contra_contrato; antes {"chars": 52}, depois {"chars": 52}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | inteiro |  |
| nome | texto |  |
| resumo | texto\|nulo |  |
| tipo | texto |  |
| preco | numero |  |
| imagem | texto\|nulo |  |
| destaque | booleano |  |
| detail |  | texto |
| retry_after |  | inteiro |

Trecho podado (hash `40519305458cb4df`):

```text
{"detail": "rate limit exceeded", "retry_after": 30}
```

## 3. Contraste com a segunda causa

limite_de_requisicoes e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,84 contra 0,00; verbete(s) na evidência: limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| limite_de_requisicoes | 0,84 | sim |
| tempo_de_resposta_excedido | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[limite_de_requisicoes]`; verbetes citados: `limite_de_requisicoes`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `limite_de_requisicoes` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `limite_de_requisicoes` | confere | contexto: `limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `limite_de_requisicoes` | confere | verbetes: `limite_de_requisicoes` |
| fonte_formato_valido | `[limite_de_requisicoes]` | confere | {"ids": ["limite_de_requisicoes"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `limite_de_requisicoes` | confere | {"termo": "limite_de_requisicoes"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-10 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3458 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:13:23 | caso run-10@sonda |
| 3459 | 2 | poda | programa | ao_vivo | 2026-11-05T02:13:23 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3460 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:13:23 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, detail:inesperado, retry_after:inesperado; divergência não |
| 3461 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:13:23 | 3 de 39 verbetes entregues |
| 3462 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:13:23 | recuperacao: escolha limite_de_requisicoes,contagem_inconsistente,estrutura_aninhada_divergente; divergência não |
| 3464 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:13:23 | {"etapa": "diagnostico", "sha": "755d83a08f6907fd", "prompt_sha256": "755d83a08f69", "chars": 3893, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3465 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:13:23 | diagnostico: 59,7 s |
| 3466 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:13:23 | causa_raiz: `limite_de_requisicoes` |
| 3467 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:13:23 | campo: `nenhum` |
| 3468 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:13:23 | impacto: `O usuário recebe um erro indicando que o limite de requisições foi excedido, impedindo a visualização correta dos produtos.` |
| 3469 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:13:23 | fonte: `[limite_de_requisicoes]` |
| 3470 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:13:23 | fonte_citada: `limite_de_requisicoes` |
| 3471 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:13:23 | quatro_linhas_presentes: confere |
| 3472 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:13:23 | rotulo_no_conjunto: confere |
| 3473 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:13:23 | fonte_existe_na_biblioteca: confere |
| 3474 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:13:23 | fonte_estava_no_contexto: confere |
| 3475 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:13:23 | campo_existe_no_caso: nao_se_aplica |
| 3476 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:13:23 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3477 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:13:23 | notas_nos_verbetes_citados: informativo |
| 3478 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:13:23 | impacto: nao_verificavel |
| 3479 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:13:23 | fonte_formato_valido: confere |
| 3480 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:13:23 | fonte_contem_termo_da_causa: confere |
| 3481 | 23 | decisao | programa | ao_vivo | 2026-11-05T02:13:23 | diagnostico: escolha limite_de_requisicoes; divergência não |

</details>

Nós de decisão:

- evento 3460, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, detail:inesperado, retry_after:inesperado`; resultado sinais_em_codigo; evidência: evento 3459 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, detail, retry_after (gen_ai: plan)
- evento 3462, `recuperacao`: escolha `limite_de_requisicoes,contagem_inconsistente,estrutura_aninhada_divergente`; resultado verbetes_entregues; evidência: evento 3461 (verbete_entregue, limite_de_requisicoes), evento 3461 (verbete_entregue, contagem_inconsistente), evento 3461 (verbete_entregue, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente (gen_ai: retrieval)
- evento 3481, `diagnostico`: escolha `limite_de_requisicoes`; resultado rotulo_emitido; evidência: evento 3459 (sinal_em_codigo), evento 3461 (verbete_entregue, limite_de_requisicoes), evento 3461 (verbete_entregue, contagem_inconsistente), evento 3461 (verbete_entregue, estrutura_aninhada_divergente), evento 3465 (resposta), evento 3470 (verbete_citado, limite_de_requisicoes); divergência: não; falha: nenhuma; prov.used: limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3458 a 3481 da trilha; hash dos eventos deste caso: `ef3edeedfa78222b`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
