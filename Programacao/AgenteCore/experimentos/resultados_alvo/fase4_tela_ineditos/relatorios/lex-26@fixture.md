<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-26`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/lex-26@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `O usuário vê o título do cartão corretamente, mas o modal exibe o título com caracteres estranhos.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque os verbetes entidade-produto, campo_ausente, pagina-produtos-api estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/11

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}

SINTOMA OBSERVADO: Na mesma tela, o cartao do Pão de Alho mostra o titulo 'Pão de Alho', mas o modal aberto pelo 'Saiba Mais...' desse mesmo cartao mostra o titulo 'PÃ£o de Alho'. A grade foi carregada antes do clique e as duas respostas chegaram com status 200.

OBSERVAÇÃO ADICIONAL: A listagem GET /api/produtos, feita antes do clique, trouxe este produto (id 11) com o nome 'Pão de Alho'; so a resposta do detalhe veio com os simbolos estranhos.
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, campo_ausente, pagina-produtos-api

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente] [entidade-produto]`; verbetes citados: `campo_ausente`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `campo_ausente`, `pagina-produtos-api` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `campo_ausente`, `pagina-produtos-api` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[campo_ausente] [entidade-produto]` | confere | {"ids": ["campo_ausente", "entidade-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | **não confere** | {"termo": "codificacao_incorreta"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids lex-26 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 309 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:38:41 | caso lex-26 |
| 310 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:38:41 | 3 de 39 verbetes entregues |
| 312 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:38:41 | {"etapa": "diagnostico", "sha": "9ab7aa070bbbb0d1", "prompt_sha256": "9ab7aa070bbb", "chars": 3654, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 314 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:38:41 | diagnostico: 74,8 s |
| 315 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:38:41 | causa_raiz: `codificacao_incorreta` |
| 316 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:38:41 | campo: `nome` |
| 317 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:38:41 | impacto: `O usuário vê o título do cartão corretamente, mas o modal exibe o título com caracteres estranhos.` |
| 318 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:38:41 | fonte: `[campo_ausente] [entidade-produto]` |
| 319 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:38:41 | fonte_citada: `campo_ausente` |
| 320 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T11:38:41 | fonte_citada: `entidade-produto` |
| 321 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | quatro_linhas_presentes: confere |
| 322 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | rotulo_no_conjunto: confere |
| 323 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | fonte_existe_na_biblioteca: confere |
| 324 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | fonte_existe_na_biblioteca: confere |
| 325 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | fonte_estava_no_contexto: confere |
| 326 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | fonte_estava_no_contexto: confere |
| 327 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | campo_existe_no_caso: confere |
| 328 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 329 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | notas_nos_verbetes_citados: informativo |
| 330 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | impacto: nao_verificavel |
| 331 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | fonte_formato_valido: confere |
| 332 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | fonte_contem_termo_da_causa: nao_confere |
| 333 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:38:41 | fonte_contem_termo_da_causa: nao_confere |
| 334 | 24 | decisao | programa | ao_vivo | 2026-11-06T11:38:41 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 334, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 310 (verbete_entregue, entidade-produto), evento 310 (verbete_entregue, campo_ausente), evento 310 (verbete_entregue, pagina-produtos-api), evento 314 (resposta), evento 319 (verbete_citado, campo_ausente), evento 320 (verbete_citado, entidade-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, campo_ausente, pagina-produtos-api (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 309 a 334 da trilha; hash dos eventos deste caso: `b38f43ffbc82aa58`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
