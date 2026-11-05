<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-1@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,93) · **CONFLITO**: a troca do verbete tipo_divergente por um errado mudou a resposta de tipo_divergente para formato_de_data_divergente

**IMPACTO (declarado):** `A ordenação por preço fica errada, com 'R$ 9,90' aparecendo depois de 'R$ 89,90'.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal preco: esperado numero, recebido texto está presente na resposta HTTP e os verbetes entidade-produto, tipo_divergente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,05. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete tipo_divergente não mudou a resposta: sem efeito medido do contexto. A troca do verbete tipo_divergente por um verbete errado mudou a resposta (de tipo_divergente para formato_de_data_divergente). A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a troca do verbete tipo_divergente por um errado mudou a resposta de tipo_divergente para formato_de_data_divergente.

## 2. Evidência

Poda de `corpo_http` (evento 460): regras diff_contra_contrato; antes {"chars": 152}, depois {"chars": 152}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | texto |

Trecho podado (hash `20cdbc76d4a473bf`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": "89.90", "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

tipo_divergente e não formato_de_data_divergente: a escolha tem probabilidade 0,93 contra 0,05; verbete(s) na evidência: entidade-produto, tipo_divergente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,93 | sim |
| formato_de_data_divergente | 0,05 |  |
| valor_fora_do_dominio | 0,02 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| fonte_formato_valido | `[tipo_divergente]` | confere | {"ids": ["tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `tipo_divergente` | tipo_divergente | tipo_divergente | 0,93 | 0,91 | sem efeito medido do contexto |
| troca | `tipo_divergente` | tipo_divergente | formato_de_data_divergente | 0,93 | 0,44 | mudou a resposta: o verbete pesou na decisão |
| sem_documentacao | `` | tipo_divergente | tipo_divergente | 0,93 | 0,79 | sem efeito medido do contexto |
| repeticao_da_base | `` | tipo_divergente | tipo_divergente | 0,93 | 0,93 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-1 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 458 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:25:50 | caso semt-1 |
| 460 | 2 | poda | programa | ao_vivo | 2026-11-04T23:25:50 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 461 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:25:50 | poda: escolha json/lista; preco:tipo_diferente; divergência não |
| 462 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:25:50 | 3 de 39 verbetes entregues |
| 463 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:25:50 | recuperacao: escolha entidade-produto,tipo_divergente,contrato-produto; divergência não |
| 465 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:25:50 | {"etapa": "diagnostico", "sha": "9cbbd5d7decc1a4a", "prompt_sha256": "9cbbd5d7decc", "chars": 3560, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 467 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:25:50 | diagnostico: 64,0 s |
| 468 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:25:50 | causa_raiz: `tipo_divergente` |
| 469 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:25:50 | campo: `preco` |
| 470 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:25:50 | impacto: `A ordenação por preço fica errada, com 'R$ 9,90' aparecendo depois de 'R$ 89,90'.` |
| 471 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:25:50 | fonte: `[tipo_divergente]` |
| 472 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:25:50 | fonte_citada: `tipo_divergente` |
| 473 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:50 | quatro_linhas_presentes: confere |
| 474 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:50 | rotulo_no_conjunto: confere |
| 475 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:50 | fonte_existe_na_biblioteca: confere |
| 476 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:50 | fonte_estava_no_contexto: confere |
| 477 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:50 | campo_existe_no_caso: confere |
| 478 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:50 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 479 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:50 | notas_nos_verbetes_citados: informativo |
| 480 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:50 | impacto: nao_verificavel |
| 481 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:50 | fonte_formato_valido: confere |
| 482 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:50 | fonte_contem_termo_da_causa: confere |
| 485 | 23 | inferencia | programa | ao_vivo | 2026-11-04T23:25:50 | intervencao:remocao: 58,4 s |
| 486 | 24 | intervencao | verificacao | ao_vivo | 2026-11-04T23:25:50 | remocao de tipo_divergente: rótulo tipo_divergente para tipo_divergente |
| 489 | 25 | inferencia | programa | ao_vivo | 2026-11-04T23:25:50 | intervencao:troca: 58,1 s |
| 490 | 26 | intervencao | verificacao | ao_vivo | 2026-11-04T23:25:50 | troca de tipo_divergente: rótulo tipo_divergente para formato_de_data_divergente |
| 493 | 27 | inferencia | programa | ao_vivo | 2026-11-04T23:25:50 | intervencao:sem_documentacao: 32,4 s |
| 494 | 28 | intervencao | verificacao | ao_vivo | 2026-11-04T23:25:50 | sem_documentacao de None: rótulo tipo_divergente para tipo_divergente |
| 495 | 29 | inferencia | programa | ao_vivo | 2026-11-04T23:25:50 | intervencao:repeticao_da_base: 17,1 s |
| 496 | 30 | intervencao | verificacao | ao_vivo | 2026-11-04T23:25:50 | repeticao_da_base de None: rótulo tipo_divergente para tipo_divergente |
| 497 | 31 | decisao | programa | ao_vivo | 2026-11-04T23:25:50 | diagnostico: escolha tipo_divergente; divergência sim |

</details>

Nós de decisão:

- evento 461, `poda`: escolha `json/lista; preco:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 460 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: preco (gen_ai: plan)
- evento 463, `recuperacao`: escolha `entidade-produto,tipo_divergente,contrato-produto`; resultado verbetes_entregues; evidência: evento 462 (verbete_entregue, entidade-produto), evento 462 (verbete_entregue, tipo_divergente), evento 462 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, contrato-produto (gen_ai: retrieval)
- evento 497, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 460 (sinal_em_codigo), evento 462 (verbete_entregue, entidade-produto), evento 462 (verbete_entregue, tipo_divergente), evento 462 (verbete_entregue, contrato-produto), evento 467 (resposta), evento 472 (verbete_citado, tipo_divergente); divergência: sim; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 458 a 497 da trilha; hash dos eventos deste caso: `3864e431af296d4a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
