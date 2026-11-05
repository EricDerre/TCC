<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-19`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-19@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `id_pedido` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê um objeto comum em vez de uma lista, o que pode levar a erros no processamento do front-end.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo id_pedido porque os verbetes contrato-pedido, estado_da_tela_divergente, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos/7/cancelar

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto (recurso unico, nao lista)

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Cancelado", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A resposta de POST /api/pedidos/7/cancelar vem como lista com um item, em vez do objeto unico que o contrato descreve; ler resposta.status direto da undefined.
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não estrutura_aninhada_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-pedido, estado_da_tela_divergente, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 1,00 | sim |
| estrutura_aninhada_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `estado_da_tela_divergente`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `colecao_no_lugar_de_objeto` |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-pedido"]} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id_pedido` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2204 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:48:32 | caso sin-19 |
| 2205 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:48:32 | 3 de 46 verbetes entregues |
| 2207 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:48:32 | {"chars": 4254, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "74200cbbea59", "sha": "74200cbbea59b536"} |
| 2209 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:48:32 | diagnostico: 69,2 s |
| 2210 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:48:32 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 2211 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:48:32 | campo: `id_pedido` |
| 2212 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:48:32 | impacto: `O usuário vê um objeto comum em vez de uma lista, o que pode levar a erros no processamento do front-end.` |
| 2213 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:48:32 | fonte: `[contrato-pedido]` |
| 2214 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:48:32 | fonte_citada: `contrato-pedido` |
| 2215 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:48:32 | quatro_linhas_presentes: confere |
| 2216 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:48:32 | rotulo_no_conjunto: confere |
| 2217 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:48:32 | fonte_existe_na_biblioteca: confere |
| 2218 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:48:32 | fonte_estava_no_contexto: confere |
| 2219 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:48:32 | campo_existe_no_caso: confere |
| 2220 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:48:32 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2221 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:48:32 | notas_nos_verbetes_citados: informativo |
| 2222 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:48:32 | impacto: nao_verificavel |
| 2223 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:48:32 | fonte_formato_valido: confere |
| 2224 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:48:32 | fonte_contem_termo_da_causa: nao_confere |
| 2225 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:48:32 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 2225, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 2205 (verbete_entregue, contrato-pedido), evento 2205 (verbete_entregue, estado_da_tela_divergente), evento 2205 (verbete_entregue, colecao_no_lugar_de_objeto), evento 2209 (resposta), evento 2214 (verbete_citado, contrato-pedido); divergência: não; falha: nenhuma; prov.used: contrato-pedido, estado_da_tela_divergente, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2204 a 2225 da trilha; hash dos eventos deste caso: `2dd29b25619cf9fd`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
