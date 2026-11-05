<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-11@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-11@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estrutura_aninhada_divergente` · **CAMPO:** `itens` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A interface web espera uma lista direta de produtos, mas recebe um objeto aninhado com uma chave "itens" contendo a lista, causando a listagem ficar vazia.`

Justificativa (gerada por molde): O agente respondeu estrutura_aninhada_divergente no campo itens porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes entidade-produto, estrutura_aninhada_divergente, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 2394): regras diff_contra_contrato; antes {"chars": 170}, depois {"chars": 170}.

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

estrutura_aninhada_divergente e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, estrutura_aninhada_divergente, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estrutura_aninhada_divergente | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[estrutura_aninhada_divergente]`; verbetes citados: `estrutura_aninhada_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `entidade-produto`, `estrutura_aninhada_divergente`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente`, `contagem_inconsistente` |
| fonte_formato_valido | `[estrutura_aninhada_divergente]` | confere | {"ids": ["estrutura_aninhada_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `estrutura_aninhada_divergente` | confere | {"termo": "estrutura_aninhada_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `itens` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-11 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2393 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:19:25 | caso sin-11@sonda |
| 2394 | 2 | poda | programa | ao_vivo | 2026-11-05T01:19:25 | corpo_http: 8 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2395 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:19:25 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, data:inesperado; divergência não |
| 2396 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:19:25 | 3 de 39 verbetes entregues |
| 2397 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:19:25 | recuperacao: escolha entidade-produto,estrutura_aninhada_divergente,contagem_inconsistente; divergência não |
| 2399 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:19:25 | {"etapa": "diagnostico", "sha": "4c70bf8a22f1ad64", "prompt_sha256": "4c70bf8a22f1", "chars": 3803, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2401 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:19:25 | diagnostico: 74,0 s |
| 2402 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:19:25 | causa_raiz: `estrutura_aninhada_divergente` |
| 2403 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:19:25 | campo: `itens` |
| 2404 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:19:25 | impacto: `A interface web espera uma lista direta de produtos, mas recebe um objeto aninhado com uma chave "itens" contendo a lista, causando a listagem ficar vazia.` |
| 2405 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:19:25 | fonte: `[estrutura_aninhada_divergente]` |
| 2406 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:19:25 | fonte_citada: `estrutura_aninhada_divergente` |
| 2407 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:19:25 | quatro_linhas_presentes: confere |
| 2408 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:19:25 | rotulo_no_conjunto: confere |
| 2409 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:19:25 | fonte_existe_na_biblioteca: confere |
| 2410 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:19:25 | fonte_estava_no_contexto: confere |
| 2411 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:19:25 | campo_existe_no_caso: confere |
| 2412 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:19:25 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2413 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:19:25 | notas_nos_verbetes_citados: informativo |
| 2414 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:19:25 | impacto: nao_verificavel |
| 2415 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:19:25 | fonte_formato_valido: confere |
| 2416 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:19:25 | fonte_contem_termo_da_causa: confere |
| 2417 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:19:25 | diagnostico: escolha estrutura_aninhada_divergente; divergência não |

</details>

Nós de decisão:

- evento 2395, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, data:inesperado`; resultado sinais_em_codigo; evidência: evento 2394 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, data (gen_ai: plan)
- evento 2397, `recuperacao`: escolha `entidade-produto,estrutura_aninhada_divergente,contagem_inconsistente`; resultado verbetes_entregues; evidência: evento 2396 (verbete_entregue, entidade-produto), evento 2396 (verbete_entregue, estrutura_aninhada_divergente), evento 2396 (verbete_entregue, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: entidade-produto, estrutura_aninhada_divergente, contagem_inconsistente (gen_ai: retrieval)
- evento 2417, `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido; evidência: evento 2394 (sinal_em_codigo), evento 2396 (verbete_entregue, entidade-produto), evento 2396 (verbete_entregue, estrutura_aninhada_divergente), evento 2396 (verbete_entregue, contagem_inconsistente), evento 2401 (resposta), evento 2406 (verbete_citado, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, estrutura_aninhada_divergente, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2393 a 2417 da trilha; hash dos eventos deste caso: `5b18bf197776fb75`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
