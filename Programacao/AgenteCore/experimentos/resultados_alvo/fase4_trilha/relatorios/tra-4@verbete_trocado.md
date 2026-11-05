<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-4@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-4@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `destaque` · selo de probabilidade: **baixo** (p = 0,63)

**IMPACTO (declarado):** `O campo "destaque" foi convertido em booleano, mas foi exibido como texto, causando a tela exibir apenas um cartão.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo destaque porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes tipo_divergente, entidade-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,36. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,63); trate como hipótese e confira o campo destaque antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 1000): regras diff_contra_contrato; antes {"chars": 173}, depois {"chars": 173}.

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

tipo_divergente e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,63 contra 0,36; verbete(s) na evidência: tipo_divergente, entidade-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,63 | sim |
| estrutura_aninhada_divergente | 0,36 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `tipo_divergente`, `entidade-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `tipo_divergente`, `entidade-produto` |
| fonte_formato_valido | `[tipo_divergente]` | confere | {"ids": ["tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-4 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 999 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:58:43 | caso tra-4@verbete_trocado |
| 1000 | 2 | poda | programa | ao_vivo | 2026-11-04T23:58:43 | corpo_http: 10 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1001 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:58:43 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado; divergência não |
| 1002 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:58:43 | 3 de 39 verbetes entregues |
| 1003 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:58:43 | recuperacao: escolha tipo_divergente,entidade-produto,estrutura_aninhada_divergente; divergência não |
| 1004 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:58:43 | {"etapa": "diagnostico", "sha": "e67fe808853d12d4", "prompt_sha256": "e67fe808853d", "chars": 3740, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1006 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:58:43 | diagnostico: 16,6 s |
| 1007 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:58:43 | causa_raiz: `tipo_divergente` |
| 1008 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:58:43 | campo: `destaque` |
| 1009 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:58:43 | impacto: `O campo "destaque" foi convertido em booleano, mas foi exibido como texto, causando a tela exibir apenas um cartão.` |
| 1010 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:58:43 | fonte: `[tipo_divergente]` |
| 1011 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:58:43 | fonte_citada: `tipo_divergente` |
| 1012 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:58:43 | quatro_linhas_presentes: confere |
| 1013 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:58:43 | rotulo_no_conjunto: confere |
| 1014 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:58:43 | fonte_existe_na_biblioteca: confere |
| 1015 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:58:43 | fonte_estava_no_contexto: confere |
| 1016 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:58:43 | campo_existe_no_caso: confere |
| 1017 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:58:43 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1018 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:58:43 | notas_nos_verbetes_citados: informativo |
| 1019 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:58:43 | impacto: nao_verificavel |
| 1020 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:58:43 | fonte_formato_valido: confere |
| 1021 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:58:43 | fonte_contem_termo_da_causa: confere |
| 1022 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:58:43 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1001, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado`; resultado sinais_em_codigo; evidência: evento 1000 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, envelope, total, itens (gen_ai: plan)
- evento 1003, `recuperacao`: escolha `tipo_divergente,entidade-produto,estrutura_aninhada_divergente`; resultado verbetes_entregues; evidência: evento 1002 (verbete_entregue, tipo_divergente), evento 1002 (verbete_entregue, entidade-produto), evento 1002 (verbete_entregue, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: tipo_divergente, entidade-produto, estrutura_aninhada_divergente (gen_ai: retrieval)
- evento 1022, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1000 (sinal_em_codigo), evento 1002 (verbete_entregue, tipo_divergente), evento 1002 (verbete_entregue, entidade-produto), evento 1002 (verbete_entregue, estrutura_aninhada_divergente), evento 1006 (resposta), evento 1011 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: tipo_divergente, entidade-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 999 a 1022 da trilha; hash dos eventos deste caso: `039e0954fc9b1844`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
