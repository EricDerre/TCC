<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-23`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/sin-23@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `resumo` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê "(sem descrição)" em vez do resumo do produto.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo resumo porque os verbetes contrato-produto, campo_renomeado, entidade-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/10

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 10, "nome": "Refrigerante", "tipo": "Bebidas", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false, "resumo_v2": "Lata 350ml, diversos sabores"}

SINTOMA OBSERVADO: O modal do Refrigerante abre com o titulo certo, mas o texto de descricao aparece como '(sem descrição)'.
```

## 3. Contraste com a segunda causa

campo_renomeado e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, campo_renomeado, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| dado_desatualizado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado]`; verbetes citados: `campo_renomeado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `contrato-produto`, `campo_renomeado`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `contrato-produto`, `campo_renomeado` |
| fonte_formato_valido | `[campo_renomeado]` | confere | {"ids": ["campo_renomeado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `resumo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids sin-23 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 449 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:43:29 | caso sin-23 |
| 450 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:43:29 | 3 de 39 verbetes entregues |
| 452 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:43:29 | {"etapa": "diagnostico", "sha": "7224624bce7ffe16", "prompt_sha256": "7224624bce7f", "chars": 3626, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 454 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:43:29 | diagnostico: 59,8 s |
| 455 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:43:29 | causa_raiz: `campo_renomeado` |
| 456 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:43:29 | campo: `resumo` |
| 457 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:43:29 | impacto: `O usuário vê "(sem descrição)" em vez do resumo do produto.` |
| 458 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:43:29 | fonte: `[campo_renomeado]` |
| 459 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:43:29 | fonte_citada: `campo_renomeado` |
| 460 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:43:29 | quatro_linhas_presentes: confere |
| 461 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:43:29 | rotulo_no_conjunto: confere |
| 462 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:43:29 | fonte_existe_na_biblioteca: confere |
| 463 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:43:29 | fonte_estava_no_contexto: confere |
| 464 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:43:29 | campo_existe_no_caso: confere |
| 465 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:43:29 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 466 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:43:29 | notas_nos_verbetes_citados: informativo |
| 467 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:43:29 | impacto: nao_verificavel |
| 468 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:43:29 | fonte_formato_valido: confere |
| 469 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:43:29 | fonte_contem_termo_da_causa: confere |
| 470 | 20 | decisao | programa | ao_vivo | 2026-11-06T11:43:29 | diagnostico: escolha campo_renomeado; divergência não |

</details>

Nós de decisão:

- evento 470, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 450 (verbete_entregue, contrato-produto), evento 450 (verbete_entregue, campo_renomeado), evento 450 (verbete_entregue, entidade-produto), evento 454 (resposta), evento 459 (verbete_citado, campo_renomeado); divergência: não; falha: nenhuma; prov.used: contrato-produto, campo_renomeado, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 449 a 470 da trilha; hash dos eventos deste caso: `c21209229ee43d45`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
