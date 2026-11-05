<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-10@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-10@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `limite_de_requisicoes` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida limite_de_requisicoes

**IMPACTO (declarado):** `O usuário recebe um erro de limite de requisições, impedindo a execução correta do roteiro de teste.`

Justificativa (gerada por molde): O agente respondeu limite_de_requisicoes no campo id porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes valor_fora_do_dominio, contagem_inconsistente, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida limite_de_requisicoes. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 3483): regras diff_contra_contrato; antes {"chars": 52}, depois {"chars": 52}.

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

limite_de_requisicoes e não valor_fora_do_dominio: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: valor_fora_do_dominio, contagem_inconsistente, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| limite_de_requisicoes | 1,00 | sim |
| valor_fora_do_dominio | 0,00 |  |
| tempo_de_resposta_excedido | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[valor_fora_do_dominio] [contagem_inconsistente]`; verbetes citados: `valor_fora_do_dominio`, `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `valor_fora_do_dominio` | confere |  |
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `valor_fora_do_dominio` | confere | contexto: `valor_fora_do_dominio`, `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `valor_fora_do_dominio`, `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `limite_de_requisicoes` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[valor_fora_do_dominio] [contagem_inconsistente]` | confere | {"ids": ["valor_fora_do_dominio", "contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `valor_fora_do_dominio` | **não confere** | {"termo": "limite_de_requisicoes"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | **não confere** | {"termo": "limite_de_requisicoes"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-10 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3482 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:14:27 | caso run-10@verbete_trocado |
| 3483 | 2 | poda | programa | ao_vivo | 2026-11-05T02:14:27 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3484 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:14:27 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, detail:inesperado, retry_after:inesperado; divergência não |
| 3485 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:14:27 | 3 de 39 verbetes entregues |
| 3486 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:14:27 | recuperacao: escolha valor_fora_do_dominio,contagem_inconsistente,estrutura_aninhada_divergente; divergência não |
| 3487 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:14:27 | {"etapa": "diagnostico", "sha": "c117d5485ab3a1ef", "prompt_sha256": "c117d5485ab3", "chars": 3627, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3489 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:14:27 | diagnostico: 18,2 s |
| 3490 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:14:27 | causa_raiz: `limite_de_requisicoes` |
| 3491 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:14:27 | campo: `nenhum` |
| 3492 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:14:27 | impacto: `O usuário recebe um erro de limite de requisições, impedindo a execução correta do roteiro de teste.` |
| 3493 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:14:27 | fonte: `[valor_fora_do_dominio] [contagem_inconsistente]` |
| 3494 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:14:27 | fonte_citada: `valor_fora_do_dominio` |
| 3495 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T02:14:27 | fonte_citada: `contagem_inconsistente` |
| 3496 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | quatro_linhas_presentes: confere |
| 3497 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | rotulo_no_conjunto: confere |
| 3498 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | fonte_existe_na_biblioteca: confere |
| 3499 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | fonte_existe_na_biblioteca: confere |
| 3500 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | fonte_estava_no_contexto: confere |
| 3501 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | fonte_estava_no_contexto: confere |
| 3502 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | campo_existe_no_caso: nao_se_aplica |
| 3503 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 3504 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | notas_nos_verbetes_citados: informativo |
| 3505 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | impacto: nao_verificavel |
| 3506 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | fonte_formato_valido: confere |
| 3507 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | fonte_contem_termo_da_causa: nao_confere |
| 3508 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:27 | fonte_contem_termo_da_causa: nao_confere |
| 3509 | 27 | decisao | programa | ao_vivo | 2026-11-05T02:14:27 | diagnostico: escolha limite_de_requisicoes; divergência sim |

</details>

Nós de decisão:

- evento 3484, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, detail:inesperado, retry_after:inesperado`; resultado sinais_em_codigo; evidência: evento 3483 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, detail, retry_after (gen_ai: plan)
- evento 3486, `recuperacao`: escolha `valor_fora_do_dominio,contagem_inconsistente,estrutura_aninhada_divergente`; resultado verbetes_entregues; evidência: evento 3485 (verbete_entregue, valor_fora_do_dominio), evento 3485 (verbete_entregue, contagem_inconsistente), evento 3485 (verbete_entregue, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: valor_fora_do_dominio, contagem_inconsistente, estrutura_aninhada_divergente (gen_ai: retrieval)
- evento 3509, `diagnostico`: escolha `limite_de_requisicoes`; resultado rotulo_emitido; evidência: evento 3483 (sinal_em_codigo), evento 3485 (verbete_entregue, valor_fora_do_dominio), evento 3485 (verbete_entregue, contagem_inconsistente), evento 3485 (verbete_entregue, estrutura_aninhada_divergente), evento 3489 (resposta), evento 3494 (verbete_citado, valor_fora_do_dominio), evento 3495 (verbete_citado, contagem_inconsistente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: valor_fora_do_dominio, contagem_inconsistente, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3482 a 3509 da trilha; hash dos eventos deste caso: `af41f36e0f8f49d0`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
