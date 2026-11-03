<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-18`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/lex-18@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `resumo` · selo de probabilidade: **baixo** (p = 0,49) · **CONFLITO**: nenhum verbete entregue trata da causa respondida valor_fora_do_dominio

**IMPACTO (declarado):** `O resumo exibido na tela contém caracteres inválidos, como 'Ã¡' em vez de 'á'.`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo resumo porque os verbetes contrato-produto, entidade-produto, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,36. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida valor_fora_do_dominio. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,49); trate como hipótese e confira o campo resumo antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gÃ¡s", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}]

SINTOMA OBSERVADO: O card da Agua Mineral mostra o resumo como 'Garrafa 500ml, com ou sem gÃ¡s'; o nome do produto, logo acima no mesmo card, aparece com o acento certo ('Água').

OBSERVAÇÃO ADICIONAL: So o campo resumo veio com os bytes trocados; nome, no mesmo item, chegou certo — nao e um problema de charset da resposta inteira.
```

## 3. Contraste com a segunda causa

valor_fora_do_dominio e não campo_ausente: a escolha tem probabilidade 0,49 contra 0,36; verbete(s) na evidência: contrato-produto, entidade-produto, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 0,49 | sim |
| campo_ausente | 0,36 |  |
| campo_renomeado | 0,36 |  |
| tipo_divergente | 0,06 |  |
| formato_de_data_divergente | 0,05 |  |
| chave_de_juncao_errada | 0,02 |  |
| codificacao_incorreta | 0,01 |  |
| nulo_inesperado | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `resumo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids lex-18 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1442 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:05:21 | caso lex-18 |
| 1443 | 2 | candidatos | programa | ao_vivo | 2026-11-01T12:05:21 | 3 de 40 verbetes entregues |
| 1445 | 3 | prompt | programa | ao_vivo | 2026-11-01T12:05:21 | {"etapa": "diagnostico", "sha": "e5aa55514c0bc015", "prompt_sha256": "e5aa55514c0b", "chars": 3637, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1447 | 4 | inferencia | programa | ao_vivo | 2026-11-01T12:05:21 | diagnostico: 67,5 s |
| 1448 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T12:05:21 | causa_raiz: `valor_fora_do_dominio` |
| 1449 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T12:05:21 | campo: `resumo` |
| 1450 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T12:05:21 | impacto: `O resumo exibido na tela contém caracteres inválidos, como 'Ã¡' em vez de 'á'.` |
| 1451 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T12:05:21 | fonte: `[contrato-produto]` |
| 1452 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T12:05:21 | fonte_citada: `contrato-produto` |
| 1453 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:05:21 | quatro_linhas_presentes: confere |
| 1454 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T12:05:21 | rotulo_no_conjunto: confere |
| 1455 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T12:05:21 | fonte_existe_na_biblioteca: confere |
| 1456 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T12:05:21 | fonte_estava_no_contexto: confere |
| 1457 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T12:05:21 | campo_existe_no_caso: confere |
| 1458 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T12:05:21 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1459 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T12:05:21 | notas_nos_verbetes_citados: informativo |
| 1460 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T12:05:21 | impacto: nao_verificavel |
| 1461 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T12:05:21 | fonte_formato_valido: confere |
| 1462 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T12:05:21 | fonte_contem_termo_da_causa: nao_confere |
| 1463 | 20 | decisao | programa | ao_vivo | 2026-11-01T12:05:21 | diagnostico: escolha valor_fora_do_dominio; divergência sim |

</details>

Nós de decisão:

- evento 1463, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 1443 (verbete_entregue, contrato-produto), evento 1443 (verbete_entregue, entidade-produto), evento 1443 (verbete_entregue, estado_da_tela_divergente), evento 1447 (resposta), evento 1452 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-produto, entidade-produto, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1442 a 1463 da trilha; hash dos eventos deste caso: `0aef133122336989`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
