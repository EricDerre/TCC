<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-17@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **baixo** (p = 0,79)

**IMPACTO (declarado):** `O usuário vê a categoria como 'CAR' em vez de 'Carnes'.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,17. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,79); trate como hipótese e confira o campo tipo antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "CAR", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: A categoria da Picanha ao Alho aparece como 'CAR' no card, em vez de 'Carnes'.

OBSERVAÇÃO ADICIONAL: tbtipos.id 1 tem sigla_tipo='CAR' e rotulo_tipo='Carnes'; o contrato usa o rotulo, nao a sigla.
```

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,79 contra 0,17; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,79 | sim |
| campo_ausente | 0,17 |  |
| campo_renomeado | 0,17 |  |
| chave_de_juncao_errada | 0,03 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente] [entidade-produto]`; verbetes citados: `tipo_divergente`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| fonte_formato_valido | `[tipo_divergente] [entidade-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["tipo_divergente", "entidade-produto"]} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2450 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:59:33 | caso tra-17 |
| 2451 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:59:33 | 3 de 46 verbetes entregues |
| 2453 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:59:33 | {"chars": 4275, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "75a180c41c5a", "sha": "75a180c41c5a164e"} |
| 2455 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:59:33 | diagnostico: 36,9 s |
| 2456 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:59:33 | causa_raiz: `tipo_divergente` |
| 2457 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:59:33 | campo: `tipo` |
| 2458 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:59:33 | impacto: `O usuário vê a categoria como 'CAR' em vez de 'Carnes'.` |
| 2459 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:59:33 | fonte: `[tipo_divergente] [entidade-produto]` |
| 2460 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:59:33 | fonte_citada: `tipo_divergente` |
| 2461 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T00:59:33 | fonte_citada: `entidade-produto` |
| 2462 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | quatro_linhas_presentes: confere |
| 2463 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | rotulo_no_conjunto: confere |
| 2464 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | fonte_existe_na_biblioteca: confere |
| 2465 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | fonte_existe_na_biblioteca: confere |
| 2466 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | fonte_estava_no_contexto: confere |
| 2467 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | fonte_estava_no_contexto: confere |
| 2468 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | campo_existe_no_caso: confere |
| 2469 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2470 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | notas_nos_verbetes_citados: informativo |
| 2471 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | impacto: nao_verificavel |
| 2472 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | fonte_formato_valido: confere |
| 2473 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | fonte_contem_termo_da_causa: confere |
| 2474 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T00:59:33 | fonte_contem_termo_da_causa: nao_confere |
| 2475 | 24 | decisao | programa | ao_vivo | 2026-11-04T00:59:33 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 2475, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 2451 (verbete_entregue, entidade-produto), evento 2451 (verbete_entregue, contrato-produto), evento 2451 (verbete_entregue, tipo_divergente), evento 2455 (resposta), evento 2460 (verbete_citado, tipo_divergente), evento 2461 (verbete_citado, entidade-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2450 a 2475 da trilha; hash dos eventos deste caso: `5b46c3854304aa53`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
