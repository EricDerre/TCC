<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-4@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-4@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `id` · selo de probabilidade: **medio** (p = 0,85)

**IMPACTO (declarado):** `A tela de detalhe do produto não preenche nenhum campo porque a resposta é uma lista ao invés de um objeto único.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo id porque o sinal destaque: esperado booleano (recurso unico, nao lista), recebido booleano está presente na resposta HTTP e os verbetes entidade-produto, colecao_no_lugar_de_objeto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,05 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 251): regras diff_contra_contrato; antes {"chars": 149}, depois {"chars": 149}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| destaque | booleano (recurso unico, nao lista) | booleano |

Trecho podado (hash `211f0b0487cb794d`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não resposta_truncada: a escolha tem probabilidade 0,85 contra 0,05; verbete(s) na evidência: entidade-produto, colecao_no_lugar_de_objeto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,85 | sim |
| resposta_truncada | 0,05 |  |
| tipo_divergente | 0,04 |  |
| corpo_nao_e_json | 0,02 |  |
| corpo_vazio | 0,02 |  |
| formato_de_data_divergente | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| recurso_inexistente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[colecao_no_lugar_de_objeto]`; verbetes citados: `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `colecao_no_lugar_de_objeto`, `contrato-produto` |
| fonte_formato_valido | `[colecao_no_lugar_de_objeto]` | confere | {"ids": ["colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-4 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 250 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:16:38 | caso sin-4@sonda |
| 251 | 2 | poda | programa | ao_vivo | 2026-11-04T23:16:38 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 252 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:16:38 | poda: escolha json/lista; destaque:tipo_diferente; divergência não |
| 253 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:16:38 | 3 de 39 verbetes entregues |
| 254 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:16:38 | recuperacao: escolha entidade-produto,colecao_no_lugar_de_objeto,contrato-produto; divergência não |
| 256 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:16:38 | {"etapa": "diagnostico", "sha": "85beec753de6fe09", "prompt_sha256": "85beec753de6", "chars": 3914, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 258 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:16:38 | diagnostico: 74,9 s |
| 259 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:16:38 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 260 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:16:38 | campo: `id` |
| 261 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:16:38 | impacto: `A tela de detalhe do produto não preenche nenhum campo porque a resposta é uma lista ao invés de um objeto único.` |
| 262 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:16:38 | fonte: `[colecao_no_lugar_de_objeto]` |
| 263 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:16:38 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 264 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:16:38 | quatro_linhas_presentes: confere |
| 265 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:16:38 | rotulo_no_conjunto: confere |
| 266 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:16:38 | fonte_existe_na_biblioteca: confere |
| 267 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:16:38 | fonte_estava_no_contexto: confere |
| 268 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:16:38 | campo_existe_no_caso: confere |
| 269 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:16:38 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 270 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:16:38 | notas_nos_verbetes_citados: informativo |
| 271 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:16:38 | impacto: nao_verificavel |
| 272 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:16:38 | fonte_formato_valido: confere |
| 273 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:16:38 | fonte_contem_termo_da_causa: confere |
| 274 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:16:38 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 252, `poda`: escolha `json/lista; destaque:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 251 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: destaque (gen_ai: plan)
- evento 254, `recuperacao`: escolha `entidade-produto,colecao_no_lugar_de_objeto,contrato-produto`; resultado verbetes_entregues; evidência: evento 253 (verbete_entregue, entidade-produto), evento 253 (verbete_entregue, colecao_no_lugar_de_objeto), evento 253 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, colecao_no_lugar_de_objeto, contrato-produto (gen_ai: retrieval)
- evento 274, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 251 (sinal_em_codigo), evento 253 (verbete_entregue, entidade-produto), evento 253 (verbete_entregue, colecao_no_lugar_de_objeto), evento 253 (verbete_entregue, contrato-produto), evento 258 (resposta), evento 263 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, colecao_no_lugar_de_objeto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 250 a 274 da trilha; hash dos eventos deste caso: `04d902a7fdf83a41`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
