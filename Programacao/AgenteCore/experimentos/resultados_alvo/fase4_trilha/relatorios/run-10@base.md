<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-10`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-10@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `limite_de_requisicoes` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,87)

**IMPACTO (declarado):** `O usuário recebe um erro indicando que o limite de requisições foi excedido, impedindo a visualização correta dos produtos.`

Justificativa (gerada por molde): O agente respondeu limite_de_requisicoes no campo id porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete limite_de_requisicoes não mudou a resposta: sem efeito medido do contexto. A troca do verbete limite_de_requisicoes por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 3419): regras diff_contra_contrato; antes {"chars": 52}, depois {"chars": 52}.

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

limite_de_requisicoes e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,87 contra 0,00; verbete(s) na evidência: limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| limite_de_requisicoes | 0,87 | sim |
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

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `limite_de_requisicoes` | limite_de_requisicoes | limite_de_requisicoes | 0,87 | 1,00 | sem efeito medido do contexto |
| troca | `limite_de_requisicoes` | limite_de_requisicoes | limite_de_requisicoes | 0,87 | 1,00 | sem efeito medido do contexto |
| sem_documentacao | `` | limite_de_requisicoes | limite_de_requisicoes | 0,87 | 1,00 | sem efeito medido do contexto |
| repeticao_da_base | `` | limite_de_requisicoes | limite_de_requisicoes | 0,87 | 0,87 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-10 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3417 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:08:50 | caso run-10 |
| 3419 | 2 | poda | programa | ao_vivo | 2026-11-05T02:08:50 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3420 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:08:50 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, detail:inesperado, retry_after:inesperado; divergência não |
| 3421 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:08:50 | 3 de 39 verbetes entregues |
| 3422 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:08:50 | recuperacao: escolha limite_de_requisicoes,contagem_inconsistente,estrutura_aninhada_divergente; divergência não |
| 3424 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:08:50 | {"etapa": "diagnostico", "sha": "942e6daccc5ad8b8", "prompt_sha256": "942e6daccc5a", "chars": 3774, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3426 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:08:50 | diagnostico: 71,4 s |
| 3427 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:08:50 | causa_raiz: `limite_de_requisicoes` |
| 3428 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:08:50 | campo: `nenhum` |
| 3429 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:08:50 | impacto: `O usuário recebe um erro indicando que o limite de requisições foi excedido, impedindo a visualização correta dos produtos.` |
| 3430 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:08:50 | fonte: `[limite_de_requisicoes]` |
| 3431 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:08:50 | fonte_citada: `limite_de_requisicoes` |
| 3432 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:50 | quatro_linhas_presentes: confere |
| 3433 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:50 | rotulo_no_conjunto: confere |
| 3434 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:50 | fonte_existe_na_biblioteca: confere |
| 3435 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:50 | fonte_estava_no_contexto: confere |
| 3436 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:50 | campo_existe_no_caso: nao_se_aplica |
| 3437 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:50 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3438 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:50 | notas_nos_verbetes_citados: informativo |
| 3439 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:50 | impacto: nao_verificavel |
| 3440 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:50 | fonte_formato_valido: confere |
| 3441 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:08:50 | fonte_contem_termo_da_causa: confere |
| 3444 | 23 | inferencia | programa | ao_vivo | 2026-11-05T02:08:50 | intervencao:remocao: 63,8 s |
| 3445 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T02:08:50 | remocao de limite_de_requisicoes: rótulo limite_de_requisicoes para limite_de_requisicoes |
| 3448 | 25 | inferencia | programa | ao_vivo | 2026-11-05T02:08:50 | intervencao:troca: 73,9 s |
| 3449 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T02:08:50 | troca de limite_de_requisicoes: rótulo limite_de_requisicoes para limite_de_requisicoes |
| 3452 | 27 | inferencia | programa | ao_vivo | 2026-11-05T02:08:50 | intervencao:sem_documentacao: 41,5 s |
| 3453 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T02:08:50 | sem_documentacao de None: rótulo limite_de_requisicoes para limite_de_requisicoes |
| 3455 | 29 | inferencia | programa | ao_vivo | 2026-11-05T02:08:50 | intervencao:repeticao_da_base: 18,0 s |
| 3456 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T02:08:50 | repeticao_da_base de None: rótulo limite_de_requisicoes para limite_de_requisicoes |
| 3457 | 31 | decisao | programa | ao_vivo | 2026-11-05T02:08:50 | diagnostico: escolha limite_de_requisicoes; divergência não |

</details>

Nós de decisão:

- evento 3420, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, detail:inesperado, retry_after:inesperado`; resultado sinais_em_codigo; evidência: evento 3419 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, detail, retry_after (gen_ai: plan)
- evento 3422, `recuperacao`: escolha `limite_de_requisicoes,contagem_inconsistente,estrutura_aninhada_divergente`; resultado verbetes_entregues; evidência: evento 3421 (verbete_entregue, limite_de_requisicoes), evento 3421 (verbete_entregue, contagem_inconsistente), evento 3421 (verbete_entregue, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente (gen_ai: retrieval)
- evento 3457, `diagnostico`: escolha `limite_de_requisicoes`; resultado rotulo_emitido; evidência: evento 3419 (sinal_em_codigo), evento 3421 (verbete_entregue, limite_de_requisicoes), evento 3421 (verbete_entregue, contagem_inconsistente), evento 3421 (verbete_entregue, estrutura_aninhada_divergente), evento 3426 (resposta), evento 3431 (verbete_citado, limite_de_requisicoes); divergência: não; falha: nenhuma; prov.used: limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3417 a 3457 da trilha; hash dos eventos deste caso: `92fec081d4f01d58`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
