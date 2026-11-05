<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-4@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-4@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `id` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `A tela de detalhe do produto não preenche nenhum campo porque a resposta é uma lista contendo um objeto, em vez de um objeto único.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo id porque o sinal id: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 304): regras diff_contra_contrato; antes {"chars": 149}, depois {"chars": 149}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | texto | inteiro |
| destaque | booleano (recurso unico, nao lista) | booleano |

Trecho podado (hash `211f0b0487cb794d`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não tipo_divergente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,99 | sim |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| recurso_inexistente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [colecao_no_lugar_de_objeto]`; verbetes citados: `contrato-produto`, `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto`, `colecao_no_lugar_de_objeto` |
| fonte_formato_valido | `[contrato-produto], [colecao_no_lugar_de_objeto]` | confere | {"ids": ["contrato-produto", "colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-4 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 303 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:18:17 | caso sin-4@contrato_alterado |
| 304 | 2 | poda | programa | ao_vivo | 2026-11-04T23:18:17 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato |
| 305 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:18:17 | poda: escolha json/lista; id:tipo_diferente, destaque:tipo_diferente; divergência não |
| 306 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:18:17 | 3 de 39 verbetes entregues |
| 307 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:18:17 | recuperacao: escolha entidade-produto,contrato-produto,colecao_no_lugar_de_objeto; divergência não |
| 309 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:18:17 | {"etapa": "diagnostico", "sha": "308e3ad2984c32f5", "prompt_sha256": "308e3ad2984c", "chars": 3788, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 311 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:18:17 | diagnostico: 44,1 s |
| 312 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:18:17 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 313 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:18:17 | campo: `id` |
| 314 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:18:17 | impacto: `A tela de detalhe do produto não preenche nenhum campo porque a resposta é uma lista contendo um objeto, em vez de um objeto único.` |
| 315 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:18:17 | fonte: `[contrato-produto], [colecao_no_lugar_de_objeto]` |
| 316 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:18:17 | fonte_citada: `contrato-produto` |
| 317 | 13 | declaracao | modelo | ao_vivo | 2026-11-04T23:18:17 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 318 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | quatro_linhas_presentes: confere |
| 319 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | rotulo_no_conjunto: confere |
| 320 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | fonte_existe_na_biblioteca: confere |
| 321 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | fonte_existe_na_biblioteca: confere |
| 322 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | fonte_estava_no_contexto: confere |
| 323 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | fonte_estava_no_contexto: confere |
| 324 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | campo_existe_no_caso: confere |
| 325 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 326 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | notas_nos_verbetes_citados: informativo |
| 327 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | impacto: nao_verificavel |
| 328 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | fonte_formato_valido: confere |
| 329 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | fonte_contem_termo_da_causa: nao_confere |
| 330 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T23:18:17 | fonte_contem_termo_da_causa: confere |
| 331 | 27 | decisao | programa | ao_vivo | 2026-11-04T23:18:17 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 305, `poda`: escolha `json/lista; id:tipo_diferente, destaque:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 304 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, destaque (gen_ai: plan)
- evento 307, `recuperacao`: escolha `entidade-produto,contrato-produto,colecao_no_lugar_de_objeto`; resultado verbetes_entregues; evidência: evento 306 (verbete_entregue, entidade-produto), evento 306 (verbete_entregue, contrato-produto), evento 306 (verbete_entregue, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: retrieval)
- evento 331, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 304 (sinal_em_codigo), evento 306 (verbete_entregue, entidade-produto), evento 306 (verbete_entregue, contrato-produto), evento 306 (verbete_entregue, colecao_no_lugar_de_objeto), evento 311 (resposta), evento 316 (verbete_citado, contrato-produto), evento 317 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 303 a 331 da trilha; hash dos eventos deste caso: `437d2ff2a24ffb44`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
