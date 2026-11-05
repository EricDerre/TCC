<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/lex-17@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `corpo_vazio` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não recebe informações sobre o pedido criado, o que pode levar a confusão sobre se o pedido foi realmente registrado.`

Justificativa (gerada por molde): O agente respondeu corpo_vazio porque os verbetes contrato-pedido, corpo_vazio, registro_duplicado estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos

STATUS HTTP: 201

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:


SINTOMA OBSERVADO: A resposta de POST /api/pedidos chega com status 201 (Criado) mas corpo completamente vazio; o pedido recem-criado nao vem em lugar nenhum da resposta.
```

## 3. Contraste com a segunda causa

corpo_vazio e não resposta_truncada: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-pedido, corpo_vazio, registro_duplicado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| corpo_vazio | 1,00 | sim |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| registro_duplicado | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[corpo_vazio]`; verbetes citados: `corpo_vazio`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `corpo_vazio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `corpo_vazio` | confere | contexto: `contrato-pedido`, `corpo_vazio`, `registro_duplicado` |
| Algum verbete do contexto trata da causa respondida | `corpo_vazio` | confere | verbetes: `corpo_vazio` |
| fonte_formato_valido | `[corpo_vazio]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["corpo_vazio"]} |
| fonte_contem_termo_da_causa | `corpo_vazio` | confere | {"termo": "corpo_vazio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2020 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:38:36 | caso lex-17 |
| 2021 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:38:36 | 3 de 46 verbetes entregues |
| 2023 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:38:36 | {"chars": 3417, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "f7ffc5fec920", "sha": "f7ffc5fec9206a15"} |
| 2025 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:38:36 | diagnostico: 64,4 s |
| 2026 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:38:36 | causa_raiz: `corpo_vazio` |
| 2027 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:38:36 | campo: `nenhum` |
| 2028 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:38:36 | impacto: `O usuário não recebe informações sobre o pedido criado, o que pode levar a confusão sobre se o pedido foi realmente registrado.` |
| 2029 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:38:36 | fonte: `[corpo_vazio]` |
| 2030 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:38:36 | fonte_citada: `corpo_vazio` |
| 2031 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:38:36 | quatro_linhas_presentes: confere |
| 2032 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:38:36 | rotulo_no_conjunto: confere |
| 2033 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:38:36 | fonte_existe_na_biblioteca: confere |
| 2034 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:38:36 | fonte_estava_no_contexto: confere |
| 2035 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:38:36 | campo_existe_no_caso: nao_se_aplica |
| 2036 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:38:36 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2037 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:38:36 | notas_nos_verbetes_citados: informativo |
| 2038 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:38:36 | impacto: nao_verificavel |
| 2039 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:38:36 | fonte_formato_valido: confere |
| 2040 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:38:36 | fonte_contem_termo_da_causa: confere |
| 2041 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:38:36 | diagnostico: escolha corpo_vazio; divergência não |

</details>

Nós de decisão:

- evento 2041, `diagnostico`: escolha `corpo_vazio`; resultado rotulo_emitido; evidência: evento 2021 (verbete_entregue, contrato-pedido), evento 2021 (verbete_entregue, corpo_vazio), evento 2021 (verbete_entregue, registro_duplicado), evento 2025 (resposta), evento 2030 (verbete_citado, corpo_vazio); divergência: não; falha: nenhuma; prov.used: contrato-pedido, corpo_vazio, registro_duplicado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2020 a 2041 da trilha; hash dos eventos deste caso: `1067b09f3ac6b895`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
