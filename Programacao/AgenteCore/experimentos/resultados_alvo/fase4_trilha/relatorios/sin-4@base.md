<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-4`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-4@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `id` · selo de probabilidade: **medio** (p = 0,86) · **CONFLITO**: a remoção do verbete colecao_no_lugar_de_objeto mudou a resposta de colecao_no_lugar_de_objeto para tipo_divergente; a troca do verbete colecao_no_lugar_de_objeto por um errado mudou a resposta de colecao_no_lugar_de_objeto para tipo_divergente

**IMPACTO (declarado):** `A tela de detalhe do produto não preenche nenhum campo porque a resposta é uma lista em vez de um objeto único.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo id porque o sinal destaque: esperado booleano (recurso unico, nao lista), recebido booleano está presente na resposta HTTP e os verbetes entidade-produto, colecao_no_lugar_de_objeto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,04. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete colecao_no_lugar_de_objeto mudou a resposta (de colecao_no_lugar_de_objeto para tipo_divergente), então ele pesou na decisão. A troca do verbete colecao_no_lugar_de_objeto por um verbete errado mudou a resposta (de colecao_no_lugar_de_objeto para tipo_divergente). A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a remoção do verbete colecao_no_lugar_de_objeto mudou a resposta de colecao_no_lugar_de_objeto para tipo_divergente; a troca do verbete colecao_no_lugar_de_objeto por um errado mudou a resposta de colecao_no_lugar_de_objeto para tipo_divergente.

## 2. Evidência

Poda de `corpo_http` (evento 212): regras diff_contra_contrato; antes {"chars": 149}, depois {"chars": 149}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| destaque | booleano (recurso unico, nao lista) | booleano |

Trecho podado (hash `211f0b0487cb794d`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não tipo_divergente: a escolha tem probabilidade 0,86 contra 0,04; verbete(s) na evidência: entidade-produto, colecao_no_lugar_de_objeto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,86 | sim |
| tipo_divergente | 0,04 |  |
| resposta_truncada | 0,03 |  |
| campo_ausente | 0,03 |  |
| campo_renomeado | 0,03 |  |
| corpo_nao_e_json | 0,01 |  |
| corpo_vazio | 0,01 |  |
| formato_de_data_divergente | 0,01 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| recurso_inexistente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[colecao_no_lugar_de_objeto]`; verbetes citados: `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `colecao_no_lugar_de_objeto`, `contrato-produto` |
| fonte_formato_valido | `[colecao_no_lugar_de_objeto]` | confere | {"ids": ["colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `colecao_no_lugar_de_objeto` | colecao_no_lugar_de_objeto | tipo_divergente | 0,86 | 0,38 | mudou a resposta: o verbete pesou na decisão |
| troca | `colecao_no_lugar_de_objeto` | colecao_no_lugar_de_objeto | tipo_divergente | 0,86 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| sem_documentacao | `` | colecao_no_lugar_de_objeto | colecao_no_lugar_de_objeto | 0,86 | 0,32 | sem efeito medido do contexto |
| repeticao_da_base | `` | colecao_no_lugar_de_objeto | colecao_no_lugar_de_objeto | 0,86 | 0,86 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-4 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 210 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:12:22 | caso sin-4 |
| 212 | 2 | poda | programa | ao_vivo | 2026-11-04T23:12:22 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 213 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:12:22 | poda: escolha json/lista; destaque:tipo_diferente; divergência não |
| 214 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:12:22 | 3 de 39 verbetes entregues |
| 215 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:12:22 | recuperacao: escolha entidade-produto,colecao_no_lugar_de_objeto,contrato-produto; divergência não |
| 217 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:12:22 | {"etapa": "diagnostico", "sha": "d1129b315aa67211", "prompt_sha256": "d1129b315aa6", "chars": 3790, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 219 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:12:22 | diagnostico: 75,9 s |
| 220 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:12:22 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 221 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:12:22 | campo: `id` |
| 222 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:12:22 | impacto: `A tela de detalhe do produto não preenche nenhum campo porque a resposta é uma lista em vez de um objeto único.` |
| 223 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:12:22 | fonte: `[colecao_no_lugar_de_objeto]` |
| 224 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:12:22 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 225 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:12:22 | quatro_linhas_presentes: confere |
| 226 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:12:22 | rotulo_no_conjunto: confere |
| 227 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:12:22 | fonte_existe_na_biblioteca: confere |
| 228 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:12:22 | fonte_estava_no_contexto: confere |
| 229 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:12:22 | campo_existe_no_caso: confere |
| 230 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:12:22 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 231 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:12:22 | notas_nos_verbetes_citados: informativo |
| 232 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:12:22 | impacto: nao_verificavel |
| 233 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:12:22 | fonte_formato_valido: confere |
| 234 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:12:22 | fonte_contem_termo_da_causa: confere |
| 237 | 23 | inferencia | programa | ao_vivo | 2026-11-04T23:12:22 | intervencao:remocao: 52,2 s |
| 238 | 24 | intervencao | verificacao | ao_vivo | 2026-11-04T23:12:22 | remocao de colecao_no_lugar_de_objeto: rótulo colecao_no_lugar_de_objeto para tipo_divergente |
| 241 | 25 | inferencia | programa | ao_vivo | 2026-11-04T23:12:22 | intervencao:troca: 62,5 s |
| 242 | 26 | intervencao | verificacao | ao_vivo | 2026-11-04T23:12:22 | troca de colecao_no_lugar_de_objeto: rótulo colecao_no_lugar_de_objeto para tipo_divergente |
| 245 | 27 | inferencia | programa | ao_vivo | 2026-11-04T23:12:22 | intervencao:sem_documentacao: 43,9 s |
| 246 | 28 | intervencao | verificacao | ao_vivo | 2026-11-04T23:12:22 | sem_documentacao de None: rótulo colecao_no_lugar_de_objeto para colecao_no_lugar_de_objeto |
| 247 | 29 | inferencia | programa | ao_vivo | 2026-11-04T23:12:22 | intervencao:repeticao_da_base: 17,2 s |
| 248 | 30 | intervencao | verificacao | ao_vivo | 2026-11-04T23:12:22 | repeticao_da_base de None: rótulo colecao_no_lugar_de_objeto para colecao_no_lugar_de_objeto |
| 249 | 31 | decisao | programa | ao_vivo | 2026-11-04T23:12:22 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência sim |

</details>

Nós de decisão:

- evento 213, `poda`: escolha `json/lista; destaque:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 212 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: destaque (gen_ai: plan)
- evento 215, `recuperacao`: escolha `entidade-produto,colecao_no_lugar_de_objeto,contrato-produto`; resultado verbetes_entregues; evidência: evento 214 (verbete_entregue, entidade-produto), evento 214 (verbete_entregue, colecao_no_lugar_de_objeto), evento 214 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, colecao_no_lugar_de_objeto, contrato-produto (gen_ai: retrieval)
- evento 249, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 212 (sinal_em_codigo), evento 214 (verbete_entregue, entidade-produto), evento 214 (verbete_entregue, colecao_no_lugar_de_objeto), evento 214 (verbete_entregue, contrato-produto), evento 219 (resposta), evento 224 (verbete_citado, colecao_no_lugar_de_objeto); divergência: sim; falha: nenhuma; prov.used: entidade-produto, colecao_no_lugar_de_objeto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 210 a 249 da trilha; hash dos eventos deste caso: `7a79490ba5236e82`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
