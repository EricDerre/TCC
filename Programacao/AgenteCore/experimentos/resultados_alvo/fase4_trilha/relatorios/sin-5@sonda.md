<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-5@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-5@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `A resposta da API está retornando uma lista de produtos ao invés de um único objeto, o que causa inconsistência na exibição dos detalhes dos produtos na interface web.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto porque os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,02. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 375): regras diff_contra_contrato; antes {"chars": 260}, depois {"chars": 260}.

Trecho podado (hash `ab8ef2dc7ba007c9`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Fraldinha", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}]
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não tipo_divergente: a escolha tem probabilidade 0,98 contra 0,02; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,98 | sim |
| tipo_divergente | 0,02 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-5 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 374 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:23:19 | caso sin-5@sonda |
| 375 | 2 | poda | programa | ao_vivo | 2026-11-04T23:23:19 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 376 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:23:19 | poda: escolha json/lista; sem diferença; divergência não |
| 377 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:23:19 | 3 de 39 verbetes entregues |
| 378 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:23:19 | recuperacao: escolha entidade-produto,contrato-produto,tipo_divergente; divergência não |
| 380 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:23:19 | {"etapa": "diagnostico", "sha": "a93a9eacf0cf2afa", "prompt_sha256": "a93a9eacf0cf", "chars": 3787, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 382 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:23:19 | diagnostico: 76,5 s |
| 383 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:23:19 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 384 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:23:19 | campo: `nenhum` |
| 385 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:23:19 | impacto: `A resposta da API está retornando uma lista de produtos ao invés de um único objeto, o que causa inconsistência na exibição dos detalhes dos produtos na interface web.` |
| 386 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:23:19 | fonte: `[entidade-produto], [contrato-produto]` |
| 387 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:23:19 | fonte_citada: `entidade-produto` |
| 388 | 13 | declaracao | modelo | ao_vivo | 2026-11-04T23:23:19 | fonte_citada: `contrato-produto` |
| 389 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | quatro_linhas_presentes: confere |
| 390 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | rotulo_no_conjunto: confere |
| 391 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | fonte_existe_na_biblioteca: confere |
| 392 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | fonte_existe_na_biblioteca: confere |
| 393 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | fonte_estava_no_contexto: confere |
| 394 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | fonte_estava_no_contexto: confere |
| 395 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | campo_existe_no_caso: nao_se_aplica |
| 396 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 397 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | notas_nos_verbetes_citados: informativo |
| 398 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | impacto: nao_verificavel |
| 399 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | fonte_formato_valido: confere |
| 400 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | fonte_contem_termo_da_causa: confere |
| 401 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T23:23:19 | fonte_contem_termo_da_causa: nao_confere |
| 402 | 27 | decisao | programa | ao_vivo | 2026-11-04T23:23:19 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 376, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 375 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 378, `recuperacao`: escolha `entidade-produto,contrato-produto,tipo_divergente`; resultado verbetes_entregues; evidência: evento 377 (verbete_entregue, entidade-produto), evento 377 (verbete_entregue, contrato-produto), evento 377 (verbete_entregue, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: retrieval)
- evento 402, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 377 (verbete_entregue, entidade-produto), evento 377 (verbete_entregue, contrato-produto), evento 377 (verbete_entregue, tipo_divergente), evento 382 (resposta), evento 387 (verbete_citado, entidade-produto), evento 388 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 374 a 402 da trilha; hash dos eventos deste caso: `b6bc8998d1bde4ed`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
