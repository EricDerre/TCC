<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-25`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/lex-25@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `Os títulos dos produtos exibem caracteres inválidos nos lugares de acentuação, enquanto as descrições estão corretas.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque os verbetes entidade-produto, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}, {"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}, {"id": 13, "nome": "HambÃºrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}]

SINTOMA OBSERVADO: Na grade de acompanhamentos, os titulos 'PÃ£o de Alho' e 'HambÃºrguer Artesanal' aparecem com simbolos estranhos no lugar das letras acentuadas, enquanto 'Queijo Coalho' (sem acento no nome) aparece normal. A descricao de cada cartao, logo abaixo do titulo, esta com os acentos certos.
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "codificacao_incorreta"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids lex-25 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 238 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:36:34 | caso lex-25 |
| 239 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:36:34 | 3 de 39 verbetes entregues |
| 241 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:36:34 | {"etapa": "diagnostico", "sha": "74a2d71b525e26b4", "prompt_sha256": "74a2d71b525e", "chars": 4147, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 243 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:36:34 | diagnostico: 67,6 s |
| 244 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:36:34 | causa_raiz: `codificacao_incorreta` |
| 245 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:36:34 | campo: `nome` |
| 246 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:36:34 | impacto: `Os títulos dos produtos exibem caracteres inválidos nos lugares de acentuação, enquanto as descrições estão corretas.` |
| 247 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:36:34 | fonte: `[entidade-produto], [contrato-produto]` |
| 248 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:36:34 | fonte_citada: `entidade-produto` |
| 249 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T11:36:34 | fonte_citada: `contrato-produto` |
| 250 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | quatro_linhas_presentes: confere |
| 251 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | rotulo_no_conjunto: confere |
| 252 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | fonte_existe_na_biblioteca: confere |
| 253 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | fonte_existe_na_biblioteca: confere |
| 254 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | fonte_estava_no_contexto: confere |
| 255 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | fonte_estava_no_contexto: confere |
| 256 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | campo_existe_no_caso: confere |
| 257 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 258 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | notas_nos_verbetes_citados: informativo |
| 259 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | impacto: nao_verificavel |
| 260 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | fonte_formato_valido: confere |
| 261 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | fonte_contem_termo_da_causa: nao_confere |
| 262 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:36:34 | fonte_contem_termo_da_causa: nao_confere |
| 263 | 24 | decisao | programa | ao_vivo | 2026-11-06T11:36:34 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 263, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 239 (verbete_entregue, entidade-produto), evento 239 (verbete_entregue, contrato-produto), evento 239 (verbete_entregue, campo_renomeado), evento 243 (resposta), evento 248 (verbete_citado, entidade-produto), evento 249 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 238 a 263 da trilha; hash dos eventos deste caso: `826039bccfc1f4d0`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
