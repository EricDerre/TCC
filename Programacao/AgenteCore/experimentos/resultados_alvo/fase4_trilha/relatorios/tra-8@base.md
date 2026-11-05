<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-8@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `total` · selo de probabilidade: **medio** (p = 0,98) · **CONFLITO**: a remoção do verbete contagem_inconsistente mudou a resposta de contagem_inconsistente para estrutura_aninhada_divergente; a troca do verbete contagem_inconsistente por um errado mudou a resposta de contagem_inconsistente para valor_fora_do_dominio; a inferência sem documentação mudou a resposta de contagem_inconsistente para campo_ausente

**IMPACTO (declarado):** `A tela exibe cartões com um produto, mas informa 'Nenhum produto encontrado' devido à contagem inconsistente no total.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo total porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,01. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete contagem_inconsistente mudou a resposta (de contagem_inconsistente para estrutura_aninhada_divergente), então ele pesou na decisão. (a probabilidade registrada é só um limite inferior: o rótulo saiu das alternativas devolvidas) A troca do verbete contagem_inconsistente por um verbete errado mudou a resposta (de contagem_inconsistente para valor_fora_do_dominio). (a probabilidade registrada é só um limite inferior: o rótulo saiu das alternativas devolvidas) A inferência sem documentação mudou a resposta (de contagem_inconsistente para campo_ausente). A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a remoção do verbete contagem_inconsistente mudou a resposta de contagem_inconsistente para estrutura_aninhada_divergente; a troca do verbete contagem_inconsistente por um errado mudou a resposta de contagem_inconsistente para valor_fora_do_dominio; a inferência sem documentação mudou a resposta de contagem_inconsistente para campo_ausente.

## 2. Evidência

Poda de `corpo_http` (evento 2929): regras diff_contra_contrato; antes {"chars": 172}, depois {"chars": 172}.

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

Trecho podado (hash `fea713f447abbe11`):

```text
{"total": 0, "itens": [{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]}
```

## 3. Contraste com a segunda causa

contagem_inconsistente e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,98 contra 0,01; verbete(s) na evidência: contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,98 | sim |
| estrutura_aninhada_divergente | 0,01 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

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
| remocao | `contagem_inconsistente` | contagem_inconsistente | estrutura_aninhada_divergente | 0,98 | 0,00 | mudou a resposta: o verbete pesou na decisão (só um limite inferior da queda: o rótulo saiu das alternativas devolvidas) |
| troca | `contagem_inconsistente` | contagem_inconsistente | valor_fora_do_dominio | 0,98 | 0,00 | mudou a resposta: o verbete pesou na decisão (só um limite inferior da queda: o rótulo saiu das alternativas devolvidas) |
| sem_documentacao | `` | contagem_inconsistente | campo_ausente | 0,98 | 0,22 | mudou a resposta: o verbete pesou na decisão |
| repeticao_da_base | `` | contagem_inconsistente | contagem_inconsistente | 0,98 | 0,97 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `total` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-8 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2927 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:43:15 | caso tra-8 |
| 2929 | 2 | poda | programa | ao_vivo | 2026-11-05T01:43:15 | corpo_http: 10 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2930 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:43:15 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado; divergência não |
| 2931 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:43:15 | 3 de 39 verbetes entregues |
| 2932 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:43:15 | recuperacao: escolha contagem_inconsistente,entidade-produto,estrutura_aninhada_divergente; divergência não |
| 2934 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:43:15 | {"etapa": "diagnostico", "sha": "8cc50e9cd975facc", "prompt_sha256": "8cc50e9cd975", "chars": 3713, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2936 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:43:15 | diagnostico: 36,8 s |
| 2937 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:43:15 | causa_raiz: `contagem_inconsistente` |
| 2938 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:43:15 | campo: `total` |
| 2939 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:43:15 | impacto: `A tela exibe cartões com um produto, mas informa 'Nenhum produto encontrado' devido à contagem inconsistente no total.` |
| 2940 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:43:15 | fonte: `[contagem_inconsistente]` |
| 2941 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:43:15 | fonte_citada: `contagem_inconsistente` |
| 2942 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:43:15 | quatro_linhas_presentes: confere |
| 2943 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:43:15 | rotulo_no_conjunto: confere |
| 2944 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:43:15 | fonte_existe_na_biblioteca: confere |
| 2945 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:43:15 | fonte_estava_no_contexto: confere |
| 2946 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:43:15 | campo_existe_no_caso: confere |
| 2947 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:43:15 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2948 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:43:15 | notas_nos_verbetes_citados: informativo |
| 2949 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:43:15 | impacto: nao_verificavel |
| 2950 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:43:15 | fonte_formato_valido: confere |
| 2951 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:43:15 | fonte_contem_termo_da_causa: confere |
| 2954 | 23 | inferencia | programa | ao_vivo | 2026-11-05T01:43:15 | intervencao:remocao: 38,7 s |
| 2955 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T01:43:15 | remocao de contagem_inconsistente: rótulo contagem_inconsistente para estrutura_aninhada_divergente |
| 2958 | 25 | inferencia | programa | ao_vivo | 2026-11-05T01:43:15 | intervencao:troca: 72,0 s |
| 2959 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T01:43:15 | troca de contagem_inconsistente: rótulo contagem_inconsistente para valor_fora_do_dominio |
| 2962 | 27 | inferencia | programa | ao_vivo | 2026-11-05T01:43:15 | intervencao:sem_documentacao: 34,4 s |
| 2963 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T01:43:15 | sem_documentacao de None: rótulo contagem_inconsistente para campo_ausente |
| 2965 | 29 | inferencia | programa | ao_vivo | 2026-11-05T01:43:15 | intervencao:repeticao_da_base: 19,0 s |
| 2966 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T01:43:15 | repeticao_da_base de None: rótulo contagem_inconsistente para contagem_inconsistente |
| 2967 | 31 | decisao | programa | ao_vivo | 2026-11-05T01:43:15 | diagnostico: escolha contagem_inconsistente; divergência sim |

</details>

Nós de decisão:

- evento 2930, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado`; resultado sinais_em_codigo; evidência: evento 2929 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, envelope, total, itens (gen_ai: plan)
- evento 2932, `recuperacao`: escolha `contagem_inconsistente,entidade-produto,estrutura_aninhada_divergente`; resultado verbetes_entregues; evidência: evento 2931 (verbete_entregue, contagem_inconsistente), evento 2931 (verbete_entregue, entidade-produto), evento 2931 (verbete_entregue, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente (gen_ai: retrieval)
- evento 2967, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 2929 (sinal_em_codigo), evento 2931 (verbete_entregue, contagem_inconsistente), evento 2931 (verbete_entregue, entidade-produto), evento 2931 (verbete_entregue, estrutura_aninhada_divergente), evento 2936 (resposta), evento 2941 (verbete_citado, contagem_inconsistente); divergência: sim; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2927 a 2967 da trilha; hash dos eventos deste caso: `9f1afa97238f0a8b`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
