<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-19`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-19@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `formato_de_data_divergente` · **CAMPO:** `data_pedido` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário recebe uma data com hora e fuso UTC, enquanto o contrato especifica apenas o formato de data (AAAA-MM-DD), dificultando a interpretação.`

Justificativa (gerada por molde): O agente respondeu formato_de_data_divergente no campo data_pedido porque os verbetes formato_de_data_divergente, contrato-pedido, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10T00:00:00Z", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: O campo data_pedido chega como '2026-09-10T00:00:00Z' (data e hora, com Z de UTC) em vez do formato so-data (AAAA-MM-DD) do contrato; quem espera so a data tem que lidar com hora e fuso que nao deveriam estar ali.
```

## 3. Contraste com a segunda causa

formato_de_data_divergente e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: formato_de_data_divergente, contrato-pedido, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| formato_de_data_divergente | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[formato_de_data_divergente]`; verbetes citados: `formato_de_data_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `formato_de_data_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `formato_de_data_divergente` | confere | contexto: `formato_de_data_divergente`, `contrato-pedido`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | confere | verbetes: `formato_de_data_divergente`, `contrato-pedido` |
| fonte_formato_valido | `[formato_de_data_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["formato_de_data_divergente"]} |
| fonte_contem_termo_da_causa | `formato_de_data_divergente` | confere | {"termo": "formato_de_data_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `data_pedido` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2346 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:55:35 | caso semt-19 |
| 2347 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:55:35 | 3 de 46 verbetes entregues |
| 2349 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:55:35 | {"chars": 3533, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "af816bbcf117", "sha": "af816bbcf117b6e4"} |
| 2351 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:55:35 | diagnostico: 71,7 s |
| 2352 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:55:35 | causa_raiz: `formato_de_data_divergente` |
| 2353 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:55:35 | campo: `data_pedido` |
| 2354 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:55:35 | impacto: `O usuário recebe uma data com hora e fuso UTC, enquanto o contrato especifica apenas o formato de data (AAAA-MM-DD), dificultando a interpretação.` |
| 2355 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:55:35 | fonte: `[formato_de_data_divergente]` |
| 2356 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:55:35 | fonte_citada: `formato_de_data_divergente` |
| 2357 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:55:35 | quatro_linhas_presentes: confere |
| 2358 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:55:35 | rotulo_no_conjunto: confere |
| 2359 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:55:35 | fonte_existe_na_biblioteca: confere |
| 2360 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:55:35 | fonte_estava_no_contexto: confere |
| 2361 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:55:35 | campo_existe_no_caso: confere |
| 2362 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:55:35 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2363 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:55:35 | notas_nos_verbetes_citados: informativo |
| 2364 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:55:35 | impacto: nao_verificavel |
| 2365 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:55:35 | fonte_formato_valido: confere |
| 2366 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:55:35 | fonte_contem_termo_da_causa: confere |
| 2367 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:55:35 | diagnostico: escolha formato_de_data_divergente; divergência não |

</details>

Nós de decisão:

- evento 2367, `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido; evidência: evento 2347 (verbete_entregue, formato_de_data_divergente), evento 2347 (verbete_entregue, contrato-pedido), evento 2347 (verbete_entregue, pedido-reserva), evento 2351 (resposta), evento 2356 (verbete_citado, formato_de_data_divergente); divergência: não; falha: nenhuma; prov.used: formato_de_data_divergente, contrato-pedido, pedido-reserva (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2346 a 2367 da trilha; hash dos eventos deste caso: `8208a3258a9d76ab`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
