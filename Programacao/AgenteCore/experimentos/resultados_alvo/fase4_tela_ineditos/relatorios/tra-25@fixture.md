<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-25`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/tra-25@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida resposta_truncada

**IMPACTO (declarado):** `A interface exibe apenas os dois últimos itens da lista, deixando de mostrar 11 itens importantes.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque os verbetes entidade-produto, contrato-produto, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}, {"id": 13, "nome": "Hambúrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}]

SINTOMA OBSERVADO: A grade mostra 13 cartoes e termina no Hamburguer Artesanal; a unica sobremesa (Abacaxi na Brasa) nao aparece. A tabela tbprodutos tem 14 linhas.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os dois ultimos itens da lista recebida (13 itens no total, ids de 1 a 13).
```

## 3. Contraste com a segunda causa

resposta_truncada e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [contagem_inconsistente]`; verbetes citados: `contrato-produto`, `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto] [contagem_inconsistente]` | confere | {"ids": ["contrato-produto", "contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "resposta_truncada"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | **não confere** | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids tra-25 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1206 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:13:19 | caso tra-25 |
| 1207 | 2 | candidatos | programa | ao_vivo | 2026-11-06T12:13:19 | 3 de 39 verbetes entregues |
| 1209 | 3 | prompt | programa | ao_vivo | 2026-11-06T12:13:19 | {"etapa": "diagnostico", "sha": "21ba22f783feed41", "prompt_sha256": "21ba22f783fe", "chars": 3913, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1211 | 4 | inferencia | programa | ao_vivo | 2026-11-06T12:13:19 | diagnostico: 60,2 s |
| 1212 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T12:13:19 | causa_raiz: `resposta_truncada` |
| 1213 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T12:13:19 | campo: `nenhum` |
| 1214 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T12:13:19 | impacto: `A interface exibe apenas os dois últimos itens da lista, deixando de mostrar 11 itens importantes.` |
| 1215 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T12:13:19 | fonte: `[contrato-produto] [contagem_inconsistente]` |
| 1216 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T12:13:19 | fonte_citada: `contrato-produto` |
| 1217 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T12:13:19 | fonte_citada: `contagem_inconsistente` |
| 1218 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | quatro_linhas_presentes: confere |
| 1219 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | rotulo_no_conjunto: confere |
| 1220 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | fonte_existe_na_biblioteca: confere |
| 1221 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | fonte_existe_na_biblioteca: confere |
| 1222 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | fonte_estava_no_contexto: confere |
| 1223 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | fonte_estava_no_contexto: confere |
| 1224 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | campo_existe_no_caso: nao_se_aplica |
| 1225 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1226 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | notas_nos_verbetes_citados: informativo |
| 1227 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | impacto: nao_verificavel |
| 1228 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | fonte_formato_valido: confere |
| 1229 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | fonte_contem_termo_da_causa: nao_confere |
| 1230 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T12:13:19 | fonte_contem_termo_da_causa: nao_confere |
| 1231 | 24 | decisao | programa | ao_vivo | 2026-11-06T12:13:19 | diagnostico: escolha resposta_truncada; divergência sim |

</details>

Nós de decisão:

- evento 1231, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 1207 (verbete_entregue, entidade-produto), evento 1207 (verbete_entregue, contrato-produto), evento 1207 (verbete_entregue, contagem_inconsistente), evento 1211 (resposta), evento 1216 (verbete_citado, contrato-produto), evento 1217 (verbete_citado, contagem_inconsistente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1206 a 1231 da trilha; hash dos eventos deste caso: `a0ef123b56b9522b`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
