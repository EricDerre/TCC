<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-8@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-8@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `total` · selo de probabilidade: **baixo** (p = 0,75)

**IMPACTO (declarado):** `A tela exibe cartões com produtos, mas informa 'Nenhum produto encontrado' devido ao valor zero no campo total.`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo total porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes valor_fora_do_dominio, entidade-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,20. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,75); trate como hipótese e confira o campo total antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 2993): regras diff_contra_contrato; antes {"chars": 172}, depois {"chars": 172}.

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

valor_fora_do_dominio e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,75 contra 0,20; verbete(s) na evidência: valor_fora_do_dominio, entidade-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 0,75 | sim |
| estrutura_aninhada_divergente | 0,20 |  |
| tipo_divergente | 0,01 |  |
| resposta_truncada | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[valor_fora_do_dominio]`; verbetes citados: `valor_fora_do_dominio`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `valor_fora_do_dominio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `valor_fora_do_dominio` | confere | contexto: `valor_fora_do_dominio`, `entidade-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `valor_fora_do_dominio` |
| fonte_formato_valido | `[valor_fora_do_dominio]` | confere | {"ids": ["valor_fora_do_dominio"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `valor_fora_do_dominio` | confere | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `total` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-8 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2992 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:47:21 | caso tra-8@verbete_trocado |
| 2993 | 2 | poda | programa | ao_vivo | 2026-11-05T01:47:21 | corpo_http: 10 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2994 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:47:21 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado; divergência não |
| 2995 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:47:21 | 3 de 39 verbetes entregues |
| 2996 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:47:21 | recuperacao: escolha valor_fora_do_dominio,entidade-produto,estrutura_aninhada_divergente; divergência não |
| 2997 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:47:21 | {"etapa": "diagnostico", "sha": "f20271a3dfa7788e", "prompt_sha256": "f20271a3dfa7", "chars": 3716, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2999 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:47:21 | diagnostico: 16,8 s |
| 3000 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:47:21 | causa_raiz: `valor_fora_do_dominio` |
| 3001 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:47:21 | campo: `total` |
| 3002 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:47:21 | impacto: `A tela exibe cartões com produtos, mas informa 'Nenhum produto encontrado' devido ao valor zero no campo total.` |
| 3003 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:47:21 | fonte: `[valor_fora_do_dominio]` |
| 3004 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:47:21 | fonte_citada: `valor_fora_do_dominio` |
| 3005 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:21 | quatro_linhas_presentes: confere |
| 3006 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:21 | rotulo_no_conjunto: confere |
| 3007 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:21 | fonte_existe_na_biblioteca: confere |
| 3008 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:21 | fonte_estava_no_contexto: confere |
| 3009 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:21 | campo_existe_no_caso: confere |
| 3010 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:21 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3011 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:21 | notas_nos_verbetes_citados: informativo |
| 3012 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:21 | impacto: nao_verificavel |
| 3013 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:21 | fonte_formato_valido: confere |
| 3014 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:21 | fonte_contem_termo_da_causa: confere |
| 3015 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:47:21 | diagnostico: escolha valor_fora_do_dominio; divergência não |

</details>

Nós de decisão:

- evento 2994, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, envelope:ausente, total:inesperado, itens:inesperado`; resultado sinais_em_codigo; evidência: evento 2993 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, envelope, total, itens (gen_ai: plan)
- evento 2996, `recuperacao`: escolha `valor_fora_do_dominio,entidade-produto,estrutura_aninhada_divergente`; resultado verbetes_entregues; evidência: evento 2995 (verbete_entregue, valor_fora_do_dominio), evento 2995 (verbete_entregue, entidade-produto), evento 2995 (verbete_entregue, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: valor_fora_do_dominio, entidade-produto, estrutura_aninhada_divergente (gen_ai: retrieval)
- evento 3015, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 2993 (sinal_em_codigo), evento 2995 (verbete_entregue, valor_fora_do_dominio), evento 2995 (verbete_entregue, entidade-produto), evento 2995 (verbete_entregue, estrutura_aninhada_divergente), evento 2999 (resposta), evento 3004 (verbete_citado, valor_fora_do_dominio); divergência: não; falha: nenhuma; prov.used: valor_fora_do_dominio, entidade-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2992 a 3015 da trilha; hash dos eventos deste caso: `accd6d86dfe7cc5b`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
