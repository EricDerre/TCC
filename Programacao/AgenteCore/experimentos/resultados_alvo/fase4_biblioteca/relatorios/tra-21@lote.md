<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-21@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê uma lista incompleta de produtos, com um item ausente que deveria estar presente.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente porque os verbetes contagem_inconsistente, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
(13 itens retornados; falta o id 13, "Hamburguer Artesanal")

SINTOMA OBSERVADO: GET /api/produtos devolve 13 itens; o cadastro (tbprodutos) tem 14 produtos. O Hamburguer Artesanal (id 13) nao aparece em nenhuma pagina do site.

OBSERVAÇÃO ADICIONAL: tbprodutos tem 14 linhas cadastradas, ids 1 a 14 (seed.sql); nao existe coluna de exclusao logica em tbprodutos.
```

## 3. Contraste com a segunda causa

contagem_inconsistente e não resposta_truncada: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: contagem_inconsistente, entidade-produto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,99 | sim |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente` |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contagem_inconsistente"]} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2554 | 1 | entrada | programa | ao_vivo | 2026-11-04T01:03:20 | caso tra-21 |
| 2555 | 2 | candidatos | programa | ao_vivo | 2026-11-04T01:03:20 | 3 de 46 verbetes entregues |
| 2557 | 3 | prompt | programa | ao_vivo | 2026-11-04T01:03:20 | {"chars": 3656, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "06303a0d2c91", "sha": "06303a0d2c916ce6"} |
| 2559 | 4 | inferencia | programa | ao_vivo | 2026-11-04T01:03:20 | diagnostico: 68,4 s |
| 2560 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T01:03:20 | causa_raiz: `contagem_inconsistente` |
| 2561 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T01:03:20 | campo: `nenhum` |
| 2562 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T01:03:20 | impacto: `O usuário vê uma lista incompleta de produtos, com um item ausente que deveria estar presente.` |
| 2563 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T01:03:20 | fonte: `[contagem_inconsistente]` |
| 2564 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T01:03:20 | fonte_citada: `contagem_inconsistente` |
| 2565 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T01:03:20 | quatro_linhas_presentes: confere |
| 2566 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T01:03:20 | rotulo_no_conjunto: confere |
| 2567 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T01:03:20 | fonte_existe_na_biblioteca: confere |
| 2568 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T01:03:20 | fonte_estava_no_contexto: confere |
| 2569 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T01:03:20 | campo_existe_no_caso: nao_se_aplica |
| 2570 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T01:03:20 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2571 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T01:03:20 | notas_nos_verbetes_citados: informativo |
| 2572 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T01:03:20 | impacto: nao_verificavel |
| 2573 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T01:03:20 | fonte_formato_valido: confere |
| 2574 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T01:03:20 | fonte_contem_termo_da_causa: confere |
| 2575 | 20 | decisao | programa | ao_vivo | 2026-11-04T01:03:20 | diagnostico: escolha contagem_inconsistente; divergência não |

</details>

Nós de decisão:

- evento 2575, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 2555 (verbete_entregue, contagem_inconsistente), evento 2555 (verbete_entregue, entidade-produto), evento 2555 (verbete_entregue, contrato-produto), evento 2559 (resposta), evento 2564 (verbete_citado, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2554 a 2575 da trilha; hash dos eventos deste caso: `14b94256798db78c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
