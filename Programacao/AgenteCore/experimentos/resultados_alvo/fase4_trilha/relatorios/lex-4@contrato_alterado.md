<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-4@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-4@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `Os nomes dos produtos aparecem com caracteres estranhos nos cartões.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque o sinal id: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes contrato-produto, entidade-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, chave_de_juncao_errada, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 186): regras diff_contra_contrato; antes {"chars": 156}, depois {"chars": 156}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | texto | inteiro |

Trecho podado (hash `53a0170337e1ff5e`):

```text
[{"id": 12, "nome": "Queijo Coalho com P\u00c3\u00a3o", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true, "resumo": null}]
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não chave_de_juncao_errada: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, entidade-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 1,00 | sim |
| chave_de_juncao_errada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-4 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 185 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:11:10 | caso lex-4@contrato_alterado |
| 186 | 2 | poda | programa | ao_vivo | 2026-11-04T23:11:10 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 187 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:11:10 | poda: escolha json/lista; id:tipo_diferente; divergência não |
| 188 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:11:10 | 3 de 39 verbetes entregues |
| 189 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:11:10 | recuperacao: escolha contrato-produto,entidade-produto,tipo_divergente; divergência não |
| 191 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:11:10 | {"etapa": "diagnostico", "sha": "1aec66170f17d67f", "prompt_sha256": "1aec66170f17", "chars": 3556, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 192 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:11:10 | diagnostico: 67,8 s |
| 193 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:11:10 | causa_raiz: `codificacao_incorreta` |
| 194 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:11:10 | campo: `nome` |
| 195 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:11:10 | impacto: `Os nomes dos produtos aparecem com caracteres estranhos nos cartões.` |
| 196 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:11:10 | fonte: `[contrato-produto]` |
| 197 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:11:10 | fonte_citada: `contrato-produto` |
| 198 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:11:10 | quatro_linhas_presentes: confere |
| 199 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:11:10 | rotulo_no_conjunto: confere |
| 200 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:11:10 | fonte_existe_na_biblioteca: confere |
| 201 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:11:10 | fonte_estava_no_contexto: confere |
| 202 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:11:10 | campo_existe_no_caso: confere |
| 203 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:11:10 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 204 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:11:10 | notas_nos_verbetes_citados: informativo |
| 205 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:11:10 | impacto: nao_verificavel |
| 206 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:11:10 | fonte_formato_valido: confere |
| 207 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:11:10 | fonte_contem_termo_da_causa: nao_confere |
| 208 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:11:10 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 187, `poda`: escolha `json/lista; id:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 186 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id (gen_ai: plan)
- evento 189, `recuperacao`: escolha `contrato-produto,entidade-produto,tipo_divergente`; resultado verbetes_entregues; evidência: evento 188 (verbete_entregue, contrato-produto), evento 188 (verbete_entregue, entidade-produto), evento 188 (verbete_entregue, tipo_divergente); divergência: não; falha: nenhuma; prov.used: contrato-produto, entidade-produto, tipo_divergente (gen_ai: retrieval)
- evento 208, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 186 (sinal_em_codigo), evento 188 (verbete_entregue, contrato-produto), evento 188 (verbete_entregue, entidade-produto), evento 188 (verbete_entregue, tipo_divergente), evento 192 (resposta), evento 197 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-produto, entidade-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 185 a 208 da trilha; hash dos eventos deste caso: `4a8f6eacdfc8605c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
