<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-8@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-8@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `total` · selo de probabilidade: **medio** (p = 0,91)

**IMPACTO (declarado):** `A tela exibe cartões com um produto, mas informa 'Nenhum produto encontrado' devido à contagem inconsistente no total.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo total porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,04. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 2969): regras diff_contra_contrato; antes {"chars": 172}, depois {"chars": 172}.

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

contagem_inconsistente e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,91 contra 0,04; verbete(s) na evidência: contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,91 | sim |
| estrutura_aninhada_divergente | 0,04 |  |
| resposta_truncada | 0,02 |  |
| corpo_nao_e_json | 0,01 |  |
| corpo_vazio | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| estado_da_tela_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `entidade-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"ids": ["contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `total` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-8 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2968 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:46:40 | caso tra-8@sonda |
| 2969 | 2 | poda | programa | ao_vivo | 2026-11-05T01:46:40 | corpo_http: 10 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2970 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:46:40 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado; divergência não |
| 2971 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:46:40 | 3 de 39 verbetes entregues |
| 2972 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:46:40 | recuperacao: escolha contagem_inconsistente,entidade-produto,estrutura_aninhada_divergente; divergência não |
| 2974 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:46:40 | {"etapa": "diagnostico", "sha": "833b371bd478514d", "prompt_sha256": "833b371bd478", "chars": 3833, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2975 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:46:40 | diagnostico: 37,1 s |
| 2976 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:46:40 | causa_raiz: `contagem_inconsistente` |
| 2977 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:46:40 | campo: `total` |
| 2978 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:46:40 | impacto: `A tela exibe cartões com um produto, mas informa 'Nenhum produto encontrado' devido à contagem inconsistente no total.` |
| 2979 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:46:40 | fonte: `[contagem_inconsistente]` |
| 2980 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:46:40 | fonte_citada: `contagem_inconsistente` |
| 2981 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:46:40 | quatro_linhas_presentes: confere |
| 2982 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:46:40 | rotulo_no_conjunto: confere |
| 2983 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:46:40 | fonte_existe_na_biblioteca: confere |
| 2984 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:46:40 | fonte_estava_no_contexto: confere |
| 2985 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:46:40 | campo_existe_no_caso: confere |
| 2986 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:46:40 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2987 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:46:40 | notas_nos_verbetes_citados: informativo |
| 2988 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:46:40 | impacto: nao_verificavel |
| 2989 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:46:40 | fonte_formato_valido: confere |
| 2990 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:46:40 | fonte_contem_termo_da_causa: confere |
| 2991 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:46:40 | diagnostico: escolha contagem_inconsistente; divergência não |

</details>

Nós de decisão:

- evento 2970, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado`; resultado sinais_em_codigo; evidência: evento 2969 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, envelope, total, itens (gen_ai: plan)
- evento 2972, `recuperacao`: escolha `contagem_inconsistente,entidade-produto,estrutura_aninhada_divergente`; resultado verbetes_entregues; evidência: evento 2971 (verbete_entregue, contagem_inconsistente), evento 2971 (verbete_entregue, entidade-produto), evento 2971 (verbete_entregue, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente (gen_ai: retrieval)
- evento 2991, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 2969 (sinal_em_codigo), evento 2971 (verbete_entregue, contagem_inconsistente), evento 2971 (verbete_entregue, entidade-produto), evento 2971 (verbete_entregue, estrutura_aninhada_divergente), evento 2975 (resposta), evento 2980 (verbete_citado, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2968 a 2991 da trilha; hash dos eventos deste caso: `748b03a839cce4ab`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
