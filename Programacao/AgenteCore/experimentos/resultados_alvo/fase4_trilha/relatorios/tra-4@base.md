<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-4`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-4@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `total` · selo de probabilidade: **medio** (p = 0,97) · **CONFLITO**: a remoção do verbete contagem_inconsistente mudou a resposta de contagem_inconsistente para estrutura_aninhada_divergente; a troca do verbete contagem_inconsistente por um errado mudou a resposta de contagem_inconsistente para tipo_divergente; a inferência sem documentação mudou a resposta de contagem_inconsistente para estrutura_aninhada_divergente

**IMPACTO (declarado):** `A tela informa '14 produtos encontrados' mas exibe apenas 1 cartão, devido à contagem inconsistente entre o total informado e o número de itens retornados.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo total porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete contagem_inconsistente mudou a resposta (de contagem_inconsistente para estrutura_aninhada_divergente), então ele pesou na decisão. A troca do verbete contagem_inconsistente por um verbete errado mudou a resposta (de contagem_inconsistente para tipo_divergente). A inferência sem documentação mudou a resposta (de contagem_inconsistente para estrutura_aninhada_divergente). A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a remoção do verbete contagem_inconsistente mudou a resposta de contagem_inconsistente para estrutura_aninhada_divergente; a troca do verbete contagem_inconsistente por um errado mudou a resposta de contagem_inconsistente para tipo_divergente; a inferência sem documentação mudou a resposta de contagem_inconsistente para estrutura_aninhada_divergente.

## 2. Evidência

Poda de `corpo_http` (evento 935): regras diff_contra_contrato; antes {"chars": 173}, depois {"chars": 173}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | inteiro |  |
| nome | texto |  |
| resumo | texto\|nulo |  |
| tipo | texto |  |
| preco | numero |  |
| imagem | texto\|nulo |  |
| destaque | booleano |  |
| envelope | {total: inteiro, itens: lista} |  |
| total |  | inteiro |
| itens |  | lista |

Trecho podado (hash `a1c81e466ab33c3a`):

```text
{"total": 14, "itens": [{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]}
```

## 3. Contraste com a segunda causa

contagem_inconsistente e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,97 contra 0,00; verbete(s) na evidência: contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,97 | sim |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `entidade-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"ids": ["contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `contagem_inconsistente` | contagem_inconsistente | estrutura_aninhada_divergente | 0,97 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| troca | `contagem_inconsistente` | contagem_inconsistente | tipo_divergente | 0,97 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| sem_documentacao | `` | contagem_inconsistente | estrutura_aninhada_divergente | 0,97 | 0,23 | mudou a resposta: o verbete pesou na decisão |
| repeticao_da_base | `` | contagem_inconsistente | contagem_inconsistente | 0,97 | 0,97 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `total` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-4 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 933 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:52:50 | caso tra-4 |
| 935 | 2 | poda | programa | ao_vivo | 2026-11-04T23:52:50 | corpo_http: 10 diferença(s) contra o contrato; regras diff_contra_contrato |
| 936 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:52:50 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado; divergência não |
| 937 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:52:50 | 3 de 39 verbetes entregues |
| 938 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:52:50 | recuperacao: escolha contagem_inconsistente,entidade-produto,estrutura_aninhada_divergente; divergência não |
| 940 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:52:50 | {"etapa": "diagnostico", "sha": "665cb5f18097f207", "prompt_sha256": "665cb5f18097", "chars": 3720, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 942 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:52:50 | diagnostico: 74,7 s |
| 943 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:52:50 | causa_raiz: `contagem_inconsistente` |
| 944 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:52:50 | campo: `total` |
| 945 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:52:50 | impacto: `A tela informa '14 produtos encontrados' mas exibe apenas 1 cartão, devido à contagem inconsistente entre o total informado e o número de itens retornados.` |
| 946 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:52:50 | fonte: `[contagem_inconsistente]` |
| 947 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:52:50 | fonte_citada: `contagem_inconsistente` |
| 948 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:52:50 | quatro_linhas_presentes: confere |
| 949 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:52:50 | rotulo_no_conjunto: confere |
| 950 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:52:50 | fonte_existe_na_biblioteca: confere |
| 951 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:52:50 | fonte_estava_no_contexto: confere |
| 952 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:52:50 | campo_existe_no_caso: confere |
| 953 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:52:50 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 954 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:52:50 | notas_nos_verbetes_citados: informativo |
| 955 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:52:50 | impacto: nao_verificavel |
| 956 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:52:50 | fonte_formato_valido: confere |
| 957 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:52:50 | fonte_contem_termo_da_causa: confere |
| 960 | 23 | inferencia | programa | ao_vivo | 2026-11-04T23:52:50 | intervencao:remocao: 65,0 s |
| 961 | 24 | intervencao | verificacao | ao_vivo | 2026-11-04T23:52:50 | remocao de contagem_inconsistente: rótulo contagem_inconsistente para estrutura_aninhada_divergente |
| 964 | 25 | inferencia | programa | ao_vivo | 2026-11-04T23:52:50 | intervencao:troca: 76,7 s |
| 965 | 26 | intervencao | verificacao | ao_vivo | 2026-11-04T23:52:50 | troca de contagem_inconsistente: rótulo contagem_inconsistente para tipo_divergente |
| 968 | 27 | inferencia | programa | ao_vivo | 2026-11-04T23:52:50 | intervencao:sem_documentacao: 44,0 s |
| 969 | 28 | intervencao | verificacao | ao_vivo | 2026-11-04T23:52:50 | sem_documentacao de None: rótulo contagem_inconsistente para estrutura_aninhada_divergente |
| 971 | 29 | inferencia | programa | ao_vivo | 2026-11-04T23:52:50 | intervencao:repeticao_da_base: 19,2 s |
| 972 | 30 | intervencao | verificacao | ao_vivo | 2026-11-04T23:52:50 | repeticao_da_base de None: rótulo contagem_inconsistente para contagem_inconsistente |
| 973 | 31 | decisao | programa | ao_vivo | 2026-11-04T23:52:50 | diagnostico: escolha contagem_inconsistente; divergência sim |

</details>

Nós de decisão:

- evento 936, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado`; resultado sinais_em_codigo; evidência: evento 935 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, envelope, total, itens (gen_ai: plan)
- evento 938, `recuperacao`: escolha `contagem_inconsistente,entidade-produto,estrutura_aninhada_divergente`; resultado verbetes_entregues; evidência: evento 937 (verbete_entregue, contagem_inconsistente), evento 937 (verbete_entregue, entidade-produto), evento 937 (verbete_entregue, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente (gen_ai: retrieval)
- evento 973, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 935 (sinal_em_codigo), evento 937 (verbete_entregue, contagem_inconsistente), evento 937 (verbete_entregue, entidade-produto), evento 937 (verbete_entregue, estrutura_aninhada_divergente), evento 942 (resposta), evento 947 (verbete_citado, contagem_inconsistente); divergência: sim; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 933 a 973 da trilha; hash dos eventos deste caso: `0f69e90890c7efd4`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
