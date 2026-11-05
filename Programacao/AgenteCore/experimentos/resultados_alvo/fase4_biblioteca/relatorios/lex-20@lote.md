<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/lex-20@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O cliente recebe uma resposta incompleta, com a segunda reserva cortada no meio.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque os verbetes resposta_truncada, contrato-pedido, formato_de_data_divergente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 8, "pessoas": 2, "data_pedido": "2026-09-15", "sta

SINTOMA OBSERVADO: Quando o cliente tem mais de uma reserva, a segunda vem cortada no meio (a primeira sempre chega inteira); com uma reserva so, a resposta sempre chega completa.

OBSERVAÇÃO ADICIONAL: O Content-Length declarado no cabecalho bate com o tamanho do corpo recebido — nao e uma conexao interrompida no meio do caminho.
```

## 3. Contraste com a segunda causa

resposta_truncada e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: resposta_truncada, contrato-pedido, formato_de_data_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| registro_duplicado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[resposta_truncada]`; verbetes citados: `resposta_truncada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `resposta_truncada`, `contrato-pedido`, `formato_de_data_divergente` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | confere | verbetes: `resposta_truncada` |
| fonte_formato_valido | `[resposta_truncada]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["resposta_truncada"]} |
| fonte_contem_termo_da_causa | `resposta_truncada` | confere | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2089 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:42:19 | caso lex-20 |
| 2090 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:42:19 | 3 de 46 verbetes entregues |
| 2092 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:42:19 | {"chars": 3960, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "aebdd4196450", "sha": "aebdd4196450a52e"} |
| 2094 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:42:19 | diagnostico: 72,8 s |
| 2095 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:42:19 | causa_raiz: `resposta_truncada` |
| 2096 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:42:19 | campo: `nenhum` |
| 2097 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:42:19 | impacto: `O cliente recebe uma resposta incompleta, com a segunda reserva cortada no meio.` |
| 2098 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:42:19 | fonte: `[resposta_truncada]` |
| 2099 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:42:19 | fonte_citada: `resposta_truncada` |
| 2100 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:42:19 | quatro_linhas_presentes: confere |
| 2101 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:42:19 | rotulo_no_conjunto: confere |
| 2102 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:42:19 | fonte_existe_na_biblioteca: confere |
| 2103 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:42:19 | fonte_estava_no_contexto: confere |
| 2104 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:42:19 | campo_existe_no_caso: nao_se_aplica |
| 2105 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:42:19 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2106 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:42:19 | notas_nos_verbetes_citados: informativo |
| 2107 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:42:19 | impacto: nao_verificavel |
| 2108 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:42:19 | fonte_formato_valido: confere |
| 2109 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:42:19 | fonte_contem_termo_da_causa: confere |
| 2110 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:42:19 | diagnostico: escolha resposta_truncada; divergência não |

</details>

Nós de decisão:

- evento 2110, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 2090 (verbete_entregue, resposta_truncada), evento 2090 (verbete_entregue, contrato-pedido), evento 2090 (verbete_entregue, formato_de_data_divergente), evento 2094 (resposta), evento 2099 (verbete_citado, resposta_truncada); divergência: não; falha: nenhuma; prov.used: resposta_truncada, contrato-pedido, formato_de_data_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2089 a 2110 da trilha; hash dos eventos deste caso: `e6ca74916b7d0e57`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
