<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-1@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: a troca do verbete resposta_truncada por um errado mudou a resposta de resposta_truncada para colecao_no_lugar_de_objeto; a inferência sem documentação mudou a resposta de resposta_truncada para colecao_no_lugar_de_objeto

**IMPACTO (declarado):** `A interface web recebe uma resposta incompleta, resultando em uma lista vazia e erro de interpretação.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque o sinal esperado JSON completo e válido, recebido corpo truncado está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, resposta_truncada estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete resposta_truncada não mudou a resposta: sem efeito medido do contexto. A troca do verbete resposta_truncada por um verbete errado mudou a resposta (de resposta_truncada para colecao_no_lugar_de_objeto). A inferência sem documentação mudou a resposta (de resposta_truncada para colecao_no_lugar_de_objeto). A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a troca do verbete resposta_truncada por um errado mudou a resposta de resposta_truncada para colecao_no_lugar_de_objeto; a inferência sem documentação mudou a resposta de resposta_truncada para colecao_no_lugar_de_objeto.

## 2. Evidência

Poda de `corpo_http` (evento 5): regras diff_contra_contrato; antes {"chars": 69}, depois {"chars": 69}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo truncado |

Trecho podado (hash `cabbea3716c8b731`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "tipo": "Carnes", "preco": 89.9
```

## 3. Contraste com a segunda causa

resposta_truncada e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, resposta_truncada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[resposta_truncada]`; verbetes citados: `resposta_truncada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `entidade-produto`, `contrato-produto`, `resposta_truncada` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | confere | verbetes: `resposta_truncada` |
| fonte_formato_valido | `[resposta_truncada]` | confere | {"ids": ["resposta_truncada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `resposta_truncada` | confere | {"termo": "resposta_truncada"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `resposta_truncada` | resposta_truncada | resposta_truncada | 1,00 | 0,48 | sem efeito medido do contexto |
| troca | `resposta_truncada` | resposta_truncada | colecao_no_lugar_de_objeto | 1,00 | 0,01 | mudou a resposta: o verbete pesou na decisão |
| sem_documentacao | `` | resposta_truncada | colecao_no_lugar_de_objeto | 1,00 | 0,01 | mudou a resposta: o verbete pesou na decisão |
| repeticao_da_base | `` | resposta_truncada | resposta_truncada | 1,00 | 1,00 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-1 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:00:46 | caso lex-1 |
| 5 | 2 | poda | programa | ao_vivo | 2026-11-04T23:00:46 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 6 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:00:46 | poda: escolha truncado; divergência não |
| 7 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:00:46 | 3 de 39 verbetes entregues |
| 8 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:00:46 | recuperacao: escolha entidade-produto,contrato-produto,resposta_truncada; divergência não |
| 10 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:00:46 | {"etapa": "diagnostico", "sha": "41b36b3c29481d70", "prompt_sha256": "41b36b3c2948", "chars": 3590, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 12 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:00:46 | diagnostico: 79,0 s |
| 13 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:00:46 | causa_raiz: `resposta_truncada` |
| 14 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:00:46 | campo: `nenhum` |
| 15 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:00:46 | impacto: `A interface web recebe uma resposta incompleta, resultando em uma lista vazia e erro de interpretação.` |
| 16 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:00:46 | fonte: `[resposta_truncada]` |
| 17 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:00:46 | fonte_citada: `resposta_truncada` |
| 18 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:00:46 | quatro_linhas_presentes: confere |
| 19 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:00:46 | rotulo_no_conjunto: confere |
| 20 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:00:46 | fonte_existe_na_biblioteca: confere |
| 21 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:00:46 | fonte_estava_no_contexto: confere |
| 22 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:00:46 | campo_existe_no_caso: nao_se_aplica |
| 23 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:00:46 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 24 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:00:46 | notas_nos_verbetes_citados: informativo |
| 25 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:00:46 | impacto: nao_verificavel |
| 26 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:00:46 | fonte_formato_valido: confere |
| 27 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:00:46 | fonte_contem_termo_da_causa: confere |
| 30 | 23 | inferencia | programa | ao_vivo | 2026-11-04T23:00:46 | intervencao:remocao: 43,5 s |
| 31 | 24 | intervencao | verificacao | ao_vivo | 2026-11-04T23:00:46 | remocao de resposta_truncada: rótulo resposta_truncada para resposta_truncada |
| 34 | 25 | inferencia | programa | ao_vivo | 2026-11-04T23:00:46 | intervencao:troca: 56,0 s |
| 35 | 26 | intervencao | verificacao | ao_vivo | 2026-11-04T23:00:46 | troca de resposta_truncada: rótulo resposta_truncada para colecao_no_lugar_de_objeto |
| 38 | 27 | inferencia | programa | ao_vivo | 2026-11-04T23:00:46 | intervencao:sem_documentacao: 41,3 s |
| 39 | 28 | intervencao | verificacao | ao_vivo | 2026-11-04T23:00:46 | sem_documentacao de None: rótulo resposta_truncada para colecao_no_lugar_de_objeto |
| 41 | 29 | inferencia | programa | ao_vivo | 2026-11-04T23:00:46 | intervencao:repeticao_da_base: 15,6 s |
| 42 | 30 | intervencao | verificacao | ao_vivo | 2026-11-04T23:00:46 | repeticao_da_base de None: rótulo resposta_truncada para resposta_truncada |
| 43 | 31 | decisao | programa | ao_vivo | 2026-11-04T23:00:46 | diagnostico: escolha resposta_truncada; divergência sim |

</details>

Nós de decisão:

- evento 6, `poda`: escolha `truncado`; resultado sinais_em_codigo; evidência: evento 5 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 8, `recuperacao`: escolha `entidade-produto,contrato-produto,resposta_truncada`; resultado verbetes_entregues; evidência: evento 7 (verbete_entregue, entidade-produto), evento 7 (verbete_entregue, contrato-produto), evento 7 (verbete_entregue, resposta_truncada); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, resposta_truncada (gen_ai: retrieval)
- evento 43, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 5 (sinal_em_codigo), evento 7 (verbete_entregue, entidade-produto), evento 7 (verbete_entregue, contrato-produto), evento 7 (verbete_entregue, resposta_truncada), evento 12 (resposta), evento 17 (verbete_citado, resposta_truncada); divergência: sim; falha: nenhuma; prov.used: entidade-produto, contrato-produto, resposta_truncada (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3 a 43 da trilha; hash dos eventos deste caso: `b0a28b623edb0e46`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
