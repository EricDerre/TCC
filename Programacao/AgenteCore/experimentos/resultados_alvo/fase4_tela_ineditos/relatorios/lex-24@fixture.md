<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-24`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/lex-24@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `resumo` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `O texto de descrição do Abacaxi na Brasa aparece corrompido com símbolos estranhos.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo resumo porque os verbetes entidade-produto, contrato-produto, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/14

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e aÃ§Ãºcar", "tipo": "Sobremesas", "preco": 14.9, "imagem": "abacaxi.jpg", "destaque": false}

SINTOMA OBSERVADO: O modal do Abacaxi na Brasa abre com o titulo certo, mas o texto de descricao aparece como 'Com canela e aÃ§Ãºcar': cada letra acentuada virou um par de simbolos estranhos.
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
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "codificacao_incorreta"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `resumo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids lex-24 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 170 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:34:24 | caso lex-24 |
| 171 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:34:24 | 3 de 39 verbetes entregues |
| 173 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:34:24 | {"etapa": "diagnostico", "sha": "06f3061f1ab7f1e0", "prompt_sha256": "06f3061f1ab7", "chars": 3606, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 175 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:34:24 | diagnostico: 73,7 s |
| 176 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:34:24 | causa_raiz: `codificacao_incorreta` |
| 177 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:34:24 | campo: `resumo` |
| 178 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:34:24 | impacto: `O texto de descrição do Abacaxi na Brasa aparece corrompido com símbolos estranhos.` |
| 179 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:34:24 | fonte: `[entidade-produto], [contrato-produto]` |
| 180 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:34:24 | fonte_citada: `entidade-produto` |
| 181 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T11:34:24 | fonte_citada: `contrato-produto` |
| 182 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | quatro_linhas_presentes: confere |
| 183 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | rotulo_no_conjunto: confere |
| 184 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | fonte_existe_na_biblioteca: confere |
| 185 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | fonte_existe_na_biblioteca: confere |
| 186 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | fonte_estava_no_contexto: confere |
| 187 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | fonte_estava_no_contexto: confere |
| 188 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | campo_existe_no_caso: confere |
| 189 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 190 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | notas_nos_verbetes_citados: informativo |
| 191 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | impacto: nao_verificavel |
| 192 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | fonte_formato_valido: confere |
| 193 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | fonte_contem_termo_da_causa: nao_confere |
| 194 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:34:24 | fonte_contem_termo_da_causa: nao_confere |
| 195 | 24 | decisao | programa | ao_vivo | 2026-11-06T11:34:24 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 195, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 171 (verbete_entregue, entidade-produto), evento 171 (verbete_entregue, contrato-produto), evento 171 (verbete_entregue, estado_da_tela_divergente), evento 175 (resposta), evento 180 (verbete_citado, entidade-produto), evento 181 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 170 a 195 da trilha; hash dos eventos deste caso: `0d4ece6a1c002ce6`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
