<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-14@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-14@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `imagem_url` · selo de probabilidade: **medio** (p = 0,92)

**IMPACTO (declarado):** `O ícone de imagem quebrado indica que o front-end está tentando renderizar uma URL de imagem que não foi retornada no formato esperado.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo imagem_url porque o sinal imagem: esperado imagem, recebido imagem_url está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,04 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 2489): regras diff_contra_contrato; antes {"chars": 153}, depois {"chars": 153}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | imagem | imagem_url |

Trecho podado (hash `e968e16fdb341a27`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem_url": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não formato_de_data_divergente: a escolha tem probabilidade 0,92 contra 0,04; verbete(s) na evidência: entidade-produto, contrato-produto, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,92 | sim |
| formato_de_data_divergente | 0,04 |  |
| resposta_truncada | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem_url` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-14 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2488 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:25:02 | caso sin-14@sonda |
| 2489 | 2 | poda | programa | ao_vivo | 2026-11-05T01:25:02 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2490 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:25:02 | poda: escolha json/lista; imagem:renomeado; divergência não |
| 2491 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:25:02 | 3 de 39 verbetes entregues |
| 2492 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:25:02 | recuperacao: escolha entidade-produto,contrato-produto,campo_renomeado; divergência não |
| 2494 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:25:02 | {"etapa": "diagnostico", "sha": "7502a9266a71a309", "prompt_sha256": "7502a9266a71", "chars": 3712, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2496 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:25:02 | diagnostico: 54,1 s |
| 2497 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:25:02 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 2498 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:25:02 | campo: `imagem_url` |
| 2499 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:25:02 | impacto: `O ícone de imagem quebrado indica que o front-end está tentando renderizar uma URL de imagem que não foi retornada no formato esperado.` |
| 2500 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:25:02 | fonte: `[entidade-produto], [contrato-produto]` |
| 2501 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:25:02 | fonte_citada: `entidade-produto` |
| 2502 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T01:25:02 | fonte_citada: `contrato-produto` |
| 2503 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | quatro_linhas_presentes: confere |
| 2504 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | rotulo_no_conjunto: confere |
| 2505 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | fonte_existe_na_biblioteca: confere |
| 2506 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | fonte_existe_na_biblioteca: confere |
| 2507 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | fonte_estava_no_contexto: confere |
| 2508 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | fonte_estava_no_contexto: confere |
| 2509 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | campo_existe_no_caso: confere |
| 2510 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2511 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | notas_nos_verbetes_citados: informativo |
| 2512 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | impacto: nao_verificavel |
| 2513 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | fonte_formato_valido: confere |
| 2514 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | fonte_contem_termo_da_causa: confere |
| 2515 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T01:25:02 | fonte_contem_termo_da_causa: nao_confere |
| 2516 | 27 | decisao | programa | ao_vivo | 2026-11-05T01:25:02 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 2490, `poda`: escolha `json/lista; imagem:renomeado`; resultado sinais_em_codigo; evidência: evento 2489 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: imagem (gen_ai: plan)
- evento 2492, `recuperacao`: escolha `entidade-produto,contrato-produto,campo_renomeado`; resultado verbetes_entregues; evidência: evento 2491 (verbete_entregue, entidade-produto), evento 2491 (verbete_entregue, contrato-produto), evento 2491 (verbete_entregue, campo_renomeado); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_renomeado (gen_ai: retrieval)
- evento 2516, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 2489 (sinal_em_codigo), evento 2491 (verbete_entregue, entidade-produto), evento 2491 (verbete_entregue, contrato-produto), evento 2491 (verbete_entregue, campo_renomeado), evento 2496 (resposta), evento 2501 (verbete_citado, entidade-produto), evento 2502 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2488 a 2516 da trilha; hash dos eventos deste caso: `0fb2cc3e67b1b5a8`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
