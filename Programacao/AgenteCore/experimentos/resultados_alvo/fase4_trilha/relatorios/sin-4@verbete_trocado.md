<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-4@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-4@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,64)

**IMPACTO (declarado):** `O campo preço não está no formato esperado, causando a tela de detalhe do produto não preencher nenhum campo.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal destaque: esperado booleano (recurso unico, nao lista), recebido booleano está presente na resposta HTTP e os verbetes entidade-produto, estado_da_tela_divergente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,32. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,64); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 276): regras diff_contra_contrato; antes {"chars": 149}, depois {"chars": 149}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| destaque | booleano (recurso unico, nao lista) | booleano |

Trecho podado (hash `211f0b0487cb794d`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,64 contra 0,32; verbete(s) na evidência: entidade-produto, estado_da_tela_divergente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,64 | sim |
| campo_ausente | 0,32 |  |
| campo_renomeado | 0,32 |  |
| resposta_truncada | 0,02 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| recurso_inexistente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `estado_da_tela_divergente`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `estado_da_tela_divergente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto` |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-4 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 275 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:17:57 | caso sin-4@verbete_trocado |
| 276 | 2 | poda | programa | ao_vivo | 2026-11-04T23:17:57 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 277 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:17:57 | poda: escolha json/lista; destaque:tipo_diferente; divergência não |
| 278 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:17:57 | 3 de 39 verbetes entregues |
| 279 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:17:57 | recuperacao: escolha entidade-produto,estado_da_tela_divergente,contrato-produto; divergência não |
| 280 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:17:57 | {"etapa": "diagnostico", "sha": "8438417ee67439bd", "prompt_sha256": "8438417ee674", "chars": 3510, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 281 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:17:57 | diagnostico: 16,6 s |
| 282 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:17:57 | causa_raiz: `tipo_divergente` |
| 283 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:17:57 | campo: `preco` |
| 284 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:17:57 | impacto: `O campo preço não está no formato esperado, causando a tela de detalhe do produto não preencher nenhum campo.` |
| 285 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:17:57 | fonte: `[entidade-produto], [contrato-produto]` |
| 286 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:17:57 | fonte_citada: `entidade-produto` |
| 287 | 13 | declaracao | modelo | ao_vivo | 2026-11-04T23:17:57 | fonte_citada: `contrato-produto` |
| 288 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | quatro_linhas_presentes: confere |
| 289 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | rotulo_no_conjunto: confere |
| 290 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | fonte_existe_na_biblioteca: confere |
| 291 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | fonte_existe_na_biblioteca: confere |
| 292 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | fonte_estava_no_contexto: confere |
| 293 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | fonte_estava_no_contexto: confere |
| 294 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | campo_existe_no_caso: confere |
| 295 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 296 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | notas_nos_verbetes_citados: informativo |
| 297 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | impacto: nao_verificavel |
| 298 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | fonte_formato_valido: confere |
| 299 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | fonte_contem_termo_da_causa: nao_confere |
| 300 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T23:17:57 | fonte_contem_termo_da_causa: nao_confere |
| 301 | 27 | decisao | programa | ao_vivo | 2026-11-04T23:17:57 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 277, `poda`: escolha `json/lista; destaque:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 276 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: destaque (gen_ai: plan)
- evento 279, `recuperacao`: escolha `entidade-produto,estado_da_tela_divergente,contrato-produto`; resultado verbetes_entregues; evidência: evento 278 (verbete_entregue, entidade-produto), evento 278 (verbete_entregue, estado_da_tela_divergente), evento 278 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, estado_da_tela_divergente, contrato-produto (gen_ai: retrieval)
- evento 301, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 276 (sinal_em_codigo), evento 278 (verbete_entregue, entidade-produto), evento 278 (verbete_entregue, estado_da_tela_divergente), evento 278 (verbete_entregue, contrato-produto), evento 281 (resposta), evento 286 (verbete_citado, entidade-produto), evento 287 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, estado_da_tela_divergente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 275 a 301 da trilha; hash dos eventos deste caso: `978e59e43ab0ccf4`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
