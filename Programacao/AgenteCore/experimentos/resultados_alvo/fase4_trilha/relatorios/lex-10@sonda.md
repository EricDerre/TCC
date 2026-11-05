<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-10@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-10@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê uma lista incompleta de produtos, com apenas dois itens em vez dos esperados 14.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque o sinal esperado JSON completo e válido, recebido corpo truncado está presente na resposta HTTP e os verbetes entidade-produto, resposta_truncada, contrato-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1942): regras diff_contra_contrato; antes {"chars": 209}, depois {"chars": 209}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo truncado |

Trecho podado (hash `65cfd6ce781c21db`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre
```

## 3. Contraste com a segunda causa

resposta_truncada e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, resposta_truncada, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[resposta_truncada]`; verbetes citados: `resposta_truncada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `entidade-produto`, `resposta_truncada`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | confere | verbetes: `resposta_truncada` |
| fonte_formato_valido | `[resposta_truncada]` | confere | {"ids": ["resposta_truncada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `resposta_truncada` | confere | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-10 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1941 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:55:03 | caso lex-10@sonda |
| 1942 | 2 | poda | programa | ao_vivo | 2026-11-05T00:55:03 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1943 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:55:03 | poda: escolha truncado; divergência não |
| 1944 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:55:03 | 3 de 39 verbetes entregues |
| 1945 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:55:03 | recuperacao: escolha entidade-produto,resposta_truncada,contrato-produto; divergência não |
| 1947 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:55:03 | {"etapa": "diagnostico", "sha": "8818c5138cbccf77", "prompt_sha256": "8818c5138cbc", "chars": 3938, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1949 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:55:03 | diagnostico: 70,0 s |
| 1950 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:55:03 | causa_raiz: `resposta_truncada` |
| 1951 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:55:03 | campo: `nenhum` |
| 1952 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:55:03 | impacto: `O usuário vê uma lista incompleta de produtos, com apenas dois itens em vez dos esperados 14.` |
| 1953 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:55:03 | fonte: `[resposta_truncada]` |
| 1954 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:55:03 | fonte_citada: `resposta_truncada` |
| 1955 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:55:03 | quatro_linhas_presentes: confere |
| 1956 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:55:03 | rotulo_no_conjunto: confere |
| 1957 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:55:03 | fonte_existe_na_biblioteca: confere |
| 1958 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:55:03 | fonte_estava_no_contexto: confere |
| 1959 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:55:03 | campo_existe_no_caso: nao_se_aplica |
| 1960 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:55:03 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1961 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:55:03 | notas_nos_verbetes_citados: informativo |
| 1962 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:55:03 | impacto: nao_verificavel |
| 1963 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:55:03 | fonte_formato_valido: confere |
| 1964 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:55:03 | fonte_contem_termo_da_causa: confere |
| 1965 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:55:03 | diagnostico: escolha resposta_truncada; divergência não |

</details>

Nós de decisão:

- evento 1943, `poda`: escolha `truncado`; resultado sinais_em_codigo; evidência: evento 1942 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1945, `recuperacao`: escolha `entidade-produto,resposta_truncada,contrato-produto`; resultado verbetes_entregues; evidência: evento 1944 (verbete_entregue, entidade-produto), evento 1944 (verbete_entregue, resposta_truncada), evento 1944 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, resposta_truncada, contrato-produto (gen_ai: retrieval)
- evento 1965, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 1942 (sinal_em_codigo), evento 1944 (verbete_entregue, entidade-produto), evento 1944 (verbete_entregue, resposta_truncada), evento 1944 (verbete_entregue, contrato-produto), evento 1949 (resposta), evento 1954 (verbete_citado, resposta_truncada); divergência: não; falha: nenhuma; prov.used: entidade-produto, resposta_truncada, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1941 a 1965 da trilha; hash dos eventos deste caso: `cea14b063a30e330`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
