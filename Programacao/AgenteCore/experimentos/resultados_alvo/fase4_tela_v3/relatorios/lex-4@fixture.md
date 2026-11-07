<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-4`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/lex-4@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `Os nomes dos produtos aparecem com caracteres estranhos nos cartões.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque os verbetes entidade-produto, contrato-produto, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 12, "nome": "Queijo Coalho com P\u00c3\u00a3o", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true, "resumo": null}]

SINTOMA OBSERVADO: Os nomes dos produtos aparecem com caracteres estranhos nos cartoes.
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não formato_de_data_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 1,00 | sim |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids lex-4 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 104 | 1 | entrada | programa | ao_vivo | 2026-11-05T18:43:48 | caso lex-4 |
| 105 | 2 | candidatos | programa | ao_vivo | 2026-11-05T18:43:48 | 3 de 39 verbetes entregues |
| 107 | 3 | prompt | programa | ao_vivo | 2026-11-05T18:43:48 | {"etapa": "diagnostico", "sha": "6c3456ef7eaeda12", "prompt_sha256": "6c3456ef7eae", "chars": 3501, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 109 | 4 | inferencia | programa | ao_vivo | 2026-11-05T18:43:48 | diagnostico: 48,6 s |
| 110 | 5 | declaracao | modelo | ao_vivo | 2026-11-05T18:43:48 | causa_raiz: `codificacao_incorreta` |
| 111 | 6 | declaracao | modelo | ao_vivo | 2026-11-05T18:43:48 | campo: `nome` |
| 112 | 7 | declaracao | modelo | ao_vivo | 2026-11-05T18:43:48 | impacto: `Os nomes dos produtos aparecem com caracteres estranhos nos cartões.` |
| 113 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T18:43:48 | fonte: `[contrato-produto]` |
| 114 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T18:43:48 | fonte_citada: `contrato-produto` |
| 115 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T18:43:48 | quatro_linhas_presentes: confere |
| 116 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T18:43:48 | rotulo_no_conjunto: confere |
| 117 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T18:43:48 | fonte_existe_na_biblioteca: confere |
| 118 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T18:43:48 | fonte_estava_no_contexto: confere |
| 119 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T18:43:48 | campo_existe_no_caso: confere |
| 120 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T18:43:48 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 121 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T18:43:48 | notas_nos_verbetes_citados: informativo |
| 122 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T18:43:48 | impacto: nao_verificavel |
| 123 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T18:43:48 | fonte_formato_valido: confere |
| 124 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T18:43:48 | fonte_contem_termo_da_causa: nao_confere |
| 125 | 20 | decisao | programa | ao_vivo | 2026-11-05T18:43:48 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 125, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 105 (verbete_entregue, entidade-produto), evento 105 (verbete_entregue, contrato-produto), evento 105 (verbete_entregue, estado_da_tela_divergente), evento 109 (resposta), evento 114 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 104 a 125 da trilha; hash dos eventos deste caso: `499184fc2a36b19d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
