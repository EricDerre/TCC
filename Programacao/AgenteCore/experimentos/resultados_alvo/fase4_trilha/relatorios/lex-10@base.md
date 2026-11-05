<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-10`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-10@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê uma lista incompleta de produtos, com apenas os dois primeiros itens exibidos.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque o sinal esperado JSON completo e válido, recebido corpo truncado está presente na resposta HTTP e os verbetes entidade-produto, resposta_truncada, contrato-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. A remoção do verbete resposta_truncada não mudou a resposta: sem efeito medido do contexto. A troca do verbete resposta_truncada por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1899): regras diff_contra_contrato; antes {"chars": 209}, depois {"chars": 209}.

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
| limite_de_requisicoes | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[resposta_truncada] [contrato-produto]`; verbetes citados: `resposta_truncada`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `entidade-produto`, `resposta_truncada`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `resposta_truncada`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | confere | verbetes: `resposta_truncada` |
| fonte_formato_valido | `[resposta_truncada] [contrato-produto]` | confere | {"ids": ["resposta_truncada", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `resposta_truncada` | confere | {"termo": "resposta_truncada"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "resposta_truncada"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `resposta_truncada` | resposta_truncada | resposta_truncada | 1,00 | 0,86 | sem efeito medido do contexto |
| troca | `resposta_truncada` | resposta_truncada | resposta_truncada | 1,00 | 0,98 | sem efeito medido do contexto |
| sem_documentacao | `` | resposta_truncada | resposta_truncada | 1,00 | 0,99 | sem efeito medido do contexto |
| repeticao_da_base | `` | resposta_truncada | resposta_truncada | 1,00 | 1,00 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-10 --sem-seletor`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1897 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:51:35 | caso lex-10 |
| 1899 | 2 | poda | programa | ao_vivo | 2026-11-05T00:51:35 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1900 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:51:35 | poda: escolha truncado; divergência não |
| 1901 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:51:35 | 3 de 39 verbetes entregues |
| 1902 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:51:35 | recuperacao: escolha entidade-produto,resposta_truncada,contrato-produto; divergência não |
| 1904 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:51:35 | {"etapa": "diagnostico", "sha": "eb7cf66afb2f0013", "prompt_sha256": "eb7cf66afb2f", "chars": 3823, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1906 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:51:35 | diagnostico: 72,5 s |
| 1907 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:51:35 | causa_raiz: `resposta_truncada` |
| 1908 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:51:35 | campo: `nenhum` |
| 1909 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:51:35 | impacto: `O usuário vê uma lista incompleta de produtos, com apenas os dois primeiros itens exibidos.` |
| 1910 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:51:35 | fonte: `[resposta_truncada] [contrato-produto]` |
| 1911 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:51:35 | fonte_citada: `resposta_truncada` |
| 1912 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T00:51:35 | fonte_citada: `contrato-produto` |
| 1913 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | quatro_linhas_presentes: confere |
| 1914 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | rotulo_no_conjunto: confere |
| 1915 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | fonte_existe_na_biblioteca: confere |
| 1916 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | fonte_existe_na_biblioteca: confere |
| 1917 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | fonte_estava_no_contexto: confere |
| 1918 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | fonte_estava_no_contexto: confere |
| 1919 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | campo_existe_no_caso: nao_se_aplica |
| 1920 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1921 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | notas_nos_verbetes_citados: informativo |
| 1922 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | impacto: nao_verificavel |
| 1923 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | fonte_formato_valido: confere |
| 1924 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | fonte_contem_termo_da_causa: confere |
| 1925 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T00:51:35 | fonte_contem_termo_da_causa: nao_confere |
| 1928 | 27 | inferencia | programa | ao_vivo | 2026-11-05T00:51:35 | intervencao:remocao: 38,4 s |
| 1929 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T00:51:35 | remocao de resposta_truncada: rótulo resposta_truncada para resposta_truncada |
| 1932 | 29 | inferencia | programa | ao_vivo | 2026-11-05T00:51:35 | intervencao:troca: 41,8 s |
| 1933 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T00:51:35 | troca de resposta_truncada: rótulo resposta_truncada para resposta_truncada |
| 1936 | 31 | inferencia | programa | ao_vivo | 2026-11-05T00:51:35 | intervencao:sem_documentacao: 35,6 s |
| 1937 | 32 | intervencao | verificacao | ao_vivo | 2026-11-05T00:51:35 | sem_documentacao de None: rótulo resposta_truncada para resposta_truncada |
| 1938 | 33 | inferencia | programa | ao_vivo | 2026-11-05T00:51:35 | intervencao:repeticao_da_base: 16,2 s |
| 1939 | 34 | intervencao | verificacao | ao_vivo | 2026-11-05T00:51:35 | repeticao_da_base de None: rótulo resposta_truncada para resposta_truncada |
| 1940 | 35 | decisao | programa | ao_vivo | 2026-11-05T00:51:35 | diagnostico: escolha resposta_truncada; divergência não |

</details>

Nós de decisão:

- evento 1900, `poda`: escolha `truncado`; resultado sinais_em_codigo; evidência: evento 1899 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1902, `recuperacao`: escolha `entidade-produto,resposta_truncada,contrato-produto`; resultado verbetes_entregues; evidência: evento 1901 (verbete_entregue, entidade-produto), evento 1901 (verbete_entregue, resposta_truncada), evento 1901 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, resposta_truncada, contrato-produto (gen_ai: retrieval)
- evento 1940, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 1899 (sinal_em_codigo), evento 1901 (verbete_entregue, entidade-produto), evento 1901 (verbete_entregue, resposta_truncada), evento 1901 (verbete_entregue, contrato-produto), evento 1906 (resposta), evento 1911 (verbete_citado, resposta_truncada), evento 1912 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, resposta_truncada, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1897 a 1940 da trilha; hash dos eventos deste caso: `94ecf20acd0c2fe8`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
