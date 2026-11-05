<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-11`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-11@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `itens` · selo de probabilidade: **medio** (p = 0,98) · **CONFLITO**: a remoção do verbete contagem_inconsistente mudou a resposta de contagem_inconsistente para estrutura_aninhada_divergente; a troca do verbete contagem_inconsistente por um errado mudou a resposta de contagem_inconsistente para estrutura_aninhada_divergente

**IMPACTO (declarado):** `O usuário vê uma segunda página vazia, enquanto o total de produtos indica que há 14 itens.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo itens porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete contagem_inconsistente mudou a resposta (de contagem_inconsistente para estrutura_aninhada_divergente), então ele pesou na decisão. A troca do verbete contagem_inconsistente por um verbete errado mudou a resposta (de contagem_inconsistente para estrutura_aninhada_divergente). A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a remoção do verbete contagem_inconsistente mudou a resposta de contagem_inconsistente para estrutura_aninhada_divergente; a troca do verbete contagem_inconsistente por um errado mudou a resposta de contagem_inconsistente para estrutura_aninhada_divergente.

## 2. Evidência

Poda de `corpo_http` (evento 3147): regras diff_contra_contrato; antes {"chars": 26}, depois {"chars": 26}.

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

Trecho podado (hash `b11bbd4fe23d15d4`):

```text
{"total": 14, "itens": []}
```

## 3. Contraste com a segunda causa

contagem_inconsistente e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,98 | sim |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `estrutura_aninhada_divergente`, `tempo_de_resposta_excedido` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"ids": ["contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `contagem_inconsistente` | contagem_inconsistente | estrutura_aninhada_divergente | 0,98 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| troca | `contagem_inconsistente` | contagem_inconsistente | estrutura_aninhada_divergente | 0,98 | 0,34 | mudou a resposta: o verbete pesou na decisão |
| sem_documentacao | `` | contagem_inconsistente | contagem_inconsistente | 0,98 | 1,00 | sem efeito medido do contexto |
| repeticao_da_base | `` | contagem_inconsistente | contagem_inconsistente | 0,98 | 0,97 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `itens` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-11 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3145 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:53:15 | caso tra-11 |
| 3147 | 2 | poda | programa | ao_vivo | 2026-11-05T01:53:15 | corpo_http: 10 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3148 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:53:15 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado; divergência não |
| 3149 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:53:15 | 3 de 39 verbetes entregues |
| 3150 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:53:15 | recuperacao: escolha contagem_inconsistente,estrutura_aninhada_divergente,tempo_de_resposta_excedido; divergência não |
| 3152 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:53:15 | {"etapa": "diagnostico", "sha": "ae8bce6095974442", "prompt_sha256": "ae8bce609597", "chars": 3494, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3154 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:53:15 | diagnostico: 66,2 s |
| 3155 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:53:15 | causa_raiz: `contagem_inconsistente` |
| 3156 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:53:15 | campo: `itens` |
| 3157 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:53:15 | impacto: `O usuário vê uma segunda página vazia, enquanto o total de produtos indica que há 14 itens.` |
| 3158 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:53:15 | fonte: `[contagem_inconsistente]` |
| 3159 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:53:15 | fonte_citada: `contagem_inconsistente` |
| 3160 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:53:15 | quatro_linhas_presentes: confere |
| 3161 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:53:15 | rotulo_no_conjunto: confere |
| 3162 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:53:15 | fonte_existe_na_biblioteca: confere |
| 3163 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:53:15 | fonte_estava_no_contexto: confere |
| 3164 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:53:15 | campo_existe_no_caso: confere |
| 3165 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:53:15 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3166 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:53:15 | notas_nos_verbetes_citados: informativo |
| 3167 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:53:15 | impacto: nao_verificavel |
| 3168 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:53:15 | fonte_formato_valido: confere |
| 3169 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:53:15 | fonte_contem_termo_da_causa: confere |
| 3172 | 23 | inferencia | programa | ao_vivo | 2026-11-05T01:53:15 | intervencao:remocao: 59,4 s |
| 3173 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T01:53:15 | remocao de contagem_inconsistente: rótulo contagem_inconsistente para estrutura_aninhada_divergente |
| 3176 | 25 | inferencia | programa | ao_vivo | 2026-11-05T01:53:15 | intervencao:troca: 76,0 s |
| 3177 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T01:53:15 | troca de contagem_inconsistente: rótulo contagem_inconsistente para estrutura_aninhada_divergente |
| 3180 | 27 | inferencia | programa | ao_vivo | 2026-11-05T01:53:15 | intervencao:sem_documentacao: 37,8 s |
| 3181 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T01:53:15 | sem_documentacao de None: rótulo contagem_inconsistente para contagem_inconsistente |
| 3183 | 29 | inferencia | programa | ao_vivo | 2026-11-05T01:53:15 | intervencao:repeticao_da_base: 14,8 s |
| 3184 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T01:53:15 | repeticao_da_base de None: rótulo contagem_inconsistente para contagem_inconsistente |
| 3185 | 31 | decisao | programa | ao_vivo | 2026-11-05T01:53:15 | diagnostico: escolha contagem_inconsistente; divergência sim |

</details>

Nós de decisão:

- evento 3148, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado`; resultado sinais_em_codigo; evidência: evento 3147 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, envelope, total, itens (gen_ai: plan)
- evento 3150, `recuperacao`: escolha `contagem_inconsistente,estrutura_aninhada_divergente,tempo_de_resposta_excedido`; resultado verbetes_entregues; evidência: evento 3149 (verbete_entregue, contagem_inconsistente), evento 3149 (verbete_entregue, estrutura_aninhada_divergente), evento 3149 (verbete_entregue, tempo_de_resposta_excedido); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido (gen_ai: retrieval)
- evento 3185, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 3147 (sinal_em_codigo), evento 3149 (verbete_entregue, contagem_inconsistente), evento 3149 (verbete_entregue, estrutura_aninhada_divergente), evento 3149 (verbete_entregue, tempo_de_resposta_excedido), evento 3154 (resposta), evento 3159 (verbete_citado, contagem_inconsistente); divergência: sim; falha: nenhuma; prov.used: contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3145 a 3185 da trilha; hash dos eventos deste caso: `2ddea4c7e8990f5a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
