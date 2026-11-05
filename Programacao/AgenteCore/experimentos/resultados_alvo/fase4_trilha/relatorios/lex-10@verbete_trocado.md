<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-10@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-10@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,98) · **CONFLITO**: nenhum verbete entregue trata da causa respondida resposta_truncada

**IMPACTO (declarado):** `O usuário vê uma lista incompleta de produtos, com apenas 10 itens exibidos, mesmo que o Content-Length indique que o corpo da resposta tem o tamanho esperado.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque o sinal esperado JSON completo e válido, recebido corpo truncado está presente na resposta HTTP e os verbetes entidade-produto, estrutura_aninhada_divergente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,02. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 1967): regras diff_contra_contrato; antes {"chars": 209}, depois {"chars": 209}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo truncado |

Trecho podado (hash `65cfd6ce781c21db`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre
```

## 3. Contraste com a segunda causa

resposta_truncada e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,98 contra 0,02; verbete(s) na evidência: entidade-produto, estrutura_aninhada_divergente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 0,98 | sim |
| colecao_no_lugar_de_objeto | 0,02 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [estrutura_aninhada_divergente]`; verbetes citados: `contrato-produto`, `estrutura_aninhada_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `estrutura_aninhada_divergente`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `entidade-produto`, `estrutura_aninhada_divergente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto], [estrutura_aninhada_divergente]` | confere | {"ids": ["contrato-produto", "estrutura_aninhada_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "resposta_truncada"} |
| fonte_contem_termo_da_causa | `estrutura_aninhada_divergente` | **não confere** | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-10 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1966 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:56:17 | caso lex-10@verbete_trocado |
| 1967 | 2 | poda | programa | ao_vivo | 2026-11-05T00:56:17 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1968 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:56:17 | poda: escolha truncado; divergência não |
| 1969 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:56:17 | 3 de 39 verbetes entregues |
| 1970 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:56:17 | recuperacao: escolha entidade-produto,estrutura_aninhada_divergente,contrato-produto; divergência não |
| 1971 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:56:17 | {"etapa": "diagnostico", "sha": "e4863076e9f97dbe", "prompt_sha256": "e4863076e9f9", "chars": 3791, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1973 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:56:17 | diagnostico: 20,8 s |
| 1974 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:56:17 | causa_raiz: `resposta_truncada` |
| 1975 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:56:17 | campo: `nenhum` |
| 1976 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:56:17 | impacto: `O usuário vê uma lista incompleta de produtos, com apenas 10 itens exibidos, mesmo que o Content-Length indique que o corpo da resposta tem o tamanho esperado.` |
| 1977 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:56:17 | fonte: `[contrato-produto], [estrutura_aninhada_divergente]` |
| 1978 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:56:17 | fonte_citada: `contrato-produto` |
| 1979 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T00:56:17 | fonte_citada: `estrutura_aninhada_divergente` |
| 1980 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | quatro_linhas_presentes: confere |
| 1981 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | rotulo_no_conjunto: confere |
| 1982 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | fonte_existe_na_biblioteca: confere |
| 1983 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | fonte_existe_na_biblioteca: confere |
| 1984 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | fonte_estava_no_contexto: confere |
| 1985 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | fonte_estava_no_contexto: confere |
| 1986 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | campo_existe_no_caso: nao_se_aplica |
| 1987 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1988 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | notas_nos_verbetes_citados: informativo |
| 1989 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | impacto: nao_verificavel |
| 1990 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | fonte_formato_valido: confere |
| 1991 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | fonte_contem_termo_da_causa: nao_confere |
| 1992 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:17 | fonte_contem_termo_da_causa: nao_confere |
| 1993 | 27 | decisao | programa | ao_vivo | 2026-11-05T00:56:17 | diagnostico: escolha resposta_truncada; divergência sim |

</details>

Nós de decisão:

- evento 1968, `poda`: escolha `truncado`; resultado sinais_em_codigo; evidência: evento 1967 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1970, `recuperacao`: escolha `entidade-produto,estrutura_aninhada_divergente,contrato-produto`; resultado verbetes_entregues; evidência: evento 1969 (verbete_entregue, entidade-produto), evento 1969 (verbete_entregue, estrutura_aninhada_divergente), evento 1969 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, estrutura_aninhada_divergente, contrato-produto (gen_ai: retrieval)
- evento 1993, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 1967 (sinal_em_codigo), evento 1969 (verbete_entregue, entidade-produto), evento 1969 (verbete_entregue, estrutura_aninhada_divergente), evento 1969 (verbete_entregue, contrato-produto), evento 1973 (resposta), evento 1978 (verbete_citado, contrato-produto), evento 1979 (verbete_citado, estrutura_aninhada_divergente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, estrutura_aninhada_divergente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1966 a 1993 da trilha; hash dos eventos deste caso: `e325dbf399ff592c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
