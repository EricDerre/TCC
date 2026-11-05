<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-11@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-11@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `itens` · selo de probabilidade: **baixo** (p = 0,45) · **CONFLITO**: nenhum verbete entregue trata da causa respondida colecao_no_lugar_de_objeto

**IMPACTO (declarado):** `A interface web exibe uma lista vazia, pois espera uma coleção de produtos, mas recebe um único objeto.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo itens porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes entidade-produto, tipo_divergente, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,42. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida colecao_no_lugar_de_objeto. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,45); trate como hipótese e confira o campo itens antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 2419): regras diff_contra_contrato; antes {"chars": 170}, depois {"chars": 170}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | inteiro |  |
| nome | texto |  |
| resumo | texto\|nulo |  |
| tipo | texto |  |
| preco | numero |  |
| imagem | texto\|nulo |  |
| destaque | booleano (lista na raiz) |  |
| data |  | objeto |

Trecho podado (hash `ee7c1bf27169245d`):

```text
{"data": {"itens": [{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]}}
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não tipo_divergente: a escolha tem probabilidade 0,45 contra 0,42; verbete(s) na evidência: entidade-produto, tipo_divergente, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,45 | sim |
| tipo_divergente | 0,42 |  |
| estrutura_aninhada_divergente | 0,03 |  |
| campo_ausente | 0,03 |  |
| campo_renomeado | 0,03 |  |
| resposta_truncada | 0,03 |  |
| corpo_nao_e_json | 0,01 |  |
| corpo_vazio | 0,01 |  |
| formato_de_data_divergente | 0,01 |  |
| contagem_inconsistente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente] [entidade-produto]`; verbetes citados: `tipo_divergente`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `tipo_divergente`, `contagem_inconsistente` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `tipo_divergente`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[tipo_divergente] [entidade-produto]` | confere | {"ids": ["tipo_divergente", "entidade-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `itens` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-11 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2418 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:20:43 | caso sin-11@verbete_trocado |
| 2419 | 2 | poda | programa | ao_vivo | 2026-11-05T01:20:43 | corpo_http: 8 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2420 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:20:43 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, data:inesperado; divergência não |
| 2421 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:20:43 | 3 de 39 verbetes entregues |
| 2422 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:20:43 | recuperacao: escolha entidade-produto,tipo_divergente,contagem_inconsistente; divergência não |
| 2423 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:20:43 | {"etapa": "diagnostico", "sha": "21ca5528b2ce714b", "prompt_sha256": "21ca5528b2ce", "chars": 3592, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2425 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:20:43 | diagnostico: 17,4 s |
| 2426 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:20:43 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 2427 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:20:43 | campo: `itens` |
| 2428 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:20:43 | impacto: `A interface web exibe uma lista vazia, pois espera uma coleção de produtos, mas recebe um único objeto.` |
| 2429 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:20:43 | fonte: `[tipo_divergente] [entidade-produto]` |
| 2430 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:20:43 | fonte_citada: `tipo_divergente` |
| 2431 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T01:20:43 | fonte_citada: `entidade-produto` |
| 2432 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | quatro_linhas_presentes: confere |
| 2433 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | rotulo_no_conjunto: confere |
| 2434 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | fonte_existe_na_biblioteca: confere |
| 2435 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | fonte_existe_na_biblioteca: confere |
| 2436 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | fonte_estava_no_contexto: confere |
| 2437 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | fonte_estava_no_contexto: confere |
| 2438 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | campo_existe_no_caso: confere |
| 2439 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2440 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | notas_nos_verbetes_citados: informativo |
| 2441 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | impacto: nao_verificavel |
| 2442 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | fonte_formato_valido: confere |
| 2443 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | fonte_contem_termo_da_causa: nao_confere |
| 2444 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T01:20:43 | fonte_contem_termo_da_causa: nao_confere |
| 2445 | 27 | decisao | programa | ao_vivo | 2026-11-05T01:20:43 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência sim |

</details>

Nós de decisão:

- evento 2420, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, data:inesperado`; resultado sinais_em_codigo; evidência: evento 2419 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, data (gen_ai: plan)
- evento 2422, `recuperacao`: escolha `entidade-produto,tipo_divergente,contagem_inconsistente`; resultado verbetes_entregues; evidência: evento 2421 (verbete_entregue, entidade-produto), evento 2421 (verbete_entregue, tipo_divergente), evento 2421 (verbete_entregue, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, contagem_inconsistente (gen_ai: retrieval)
- evento 2445, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 2419 (sinal_em_codigo), evento 2421 (verbete_entregue, entidade-produto), evento 2421 (verbete_entregue, tipo_divergente), evento 2421 (verbete_entregue, contagem_inconsistente), evento 2425 (resposta), evento 2430 (verbete_citado, tipo_divergente), evento 2431 (verbete_citado, entidade-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, tipo_divergente, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2418 a 2445 da trilha; hash dos eventos deste caso: `3c828b40b5382961`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
