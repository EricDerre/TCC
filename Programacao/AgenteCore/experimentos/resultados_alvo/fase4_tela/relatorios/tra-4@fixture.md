<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-4`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/tra-4@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `total` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `A tela informa '14 produtos encontrados' mas exibe apenas 1 cartão, devido à contagem inconsistente entre o total informado e o número de itens retornados.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo total porque os verbetes contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,01. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos?pagina=1

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano | envelope: {total: inteiro, itens: lista}

CORPO DA RESPOSTA:
{"total": 14, "itens": [{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]}

SINTOMA OBSERVADO: A tela informa '14 produtos encontrados' mas exibe apenas 1 cartao.
```

## 3. Contraste com a segunda causa

contagem_inconsistente e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,98 contra 0,01; verbete(s) na evidência: contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,98 | sim |
| estrutura_aninhada_divergente | 0,01 |  |
| estado_da_tela_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `entidade-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"ids": ["contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `total` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids tra-4 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 423 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:26:23 | caso tra-4 |
| 424 | 2 | candidatos | programa | ao_vivo | 2026-11-01T11:26:23 | 3 de 40 verbetes entregues |
| 426 | 3 | prompt | programa | ao_vivo | 2026-11-01T11:26:23 | {"etapa": "diagnostico", "sha": "badf6c006acb9f9b", "prompt_sha256": "badf6c006acb", "chars": 3587, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 428 | 4 | inferencia | programa | ao_vivo | 2026-11-01T11:26:23 | diagnostico: 69,9 s |
| 429 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T11:26:23 | causa_raiz: `contagem_inconsistente` |
| 430 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T11:26:23 | campo: `total` |
| 431 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T11:26:23 | impacto: `A tela informa '14 produtos encontrados' mas exibe apenas 1 cartão, devido à contagem inconsistente entre o total informado e o número de itens retornados.` |
| 432 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T11:26:23 | fonte: `[contagem_inconsistente]` |
| 433 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T11:26:23 | fonte_citada: `contagem_inconsistente` |
| 434 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:26:23 | quatro_linhas_presentes: confere |
| 435 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T11:26:23 | rotulo_no_conjunto: confere |
| 436 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T11:26:23 | fonte_existe_na_biblioteca: confere |
| 437 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T11:26:23 | fonte_estava_no_contexto: confere |
| 438 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T11:26:23 | campo_existe_no_caso: confere |
| 439 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T11:26:23 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 440 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T11:26:23 | notas_nos_verbetes_citados: informativo |
| 441 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T11:26:23 | impacto: nao_verificavel |
| 442 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T11:26:23 | fonte_formato_valido: confere |
| 443 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T11:26:23 | fonte_contem_termo_da_causa: confere |
| 444 | 20 | decisao | programa | ao_vivo | 2026-11-01T11:26:23 | diagnostico: escolha contagem_inconsistente; divergência não |

</details>

Nós de decisão:

- evento 444, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 424 (verbete_entregue, contagem_inconsistente), evento 424 (verbete_entregue, entidade-produto), evento 424 (verbete_entregue, estrutura_aninhada_divergente), evento 428 (resposta), evento 433 (verbete_citado, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 423 a 444 da trilha; hash dos eventos deste caso: `b247f00fc85c70ba`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
