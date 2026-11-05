<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-5`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/lex-5@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê uma lista incompleta de produtos, recebendo apenas o primeiro item ou uma lista vazia.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque os verbetes entidade-produto, contrato-produto, resposta_truncada estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (sem_evidencia_do_caso, id_repetido) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso lex-5. A proposta 1 (nota em [resposta_truncada]) foi recusada por o filtro evidencia_obrigatoria com o código sem_evidencia_do_caso: o MOTIVO não cita nenhum termo da evidência do caso (campo, status, rota, sintoma, chaves do corpo). A proposta 2 (novo_verbete em [resposta_truncada]) foi recusada por a validação da Fase 3 com o código id_repetido: 'resposta_truncada' já é id de verbete ou nome de causa raiz.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `resposta_truncada` | aceita | evidencia_obrigatoria | recusada: `sem_evidencia_do_caso` | 1 |
| 2 | novo_verbete | `resposta_truncada` | recusada: `id_repetido` | nenhum | recusada: `id_repetido` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos (resposta em partes)

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Fraldinha", "tipo": "Carnes", "pre

SINTOMA OBSERVADO: Ora a lista carrega inteira, ora aparece so o primeiro cartao. O servidor registra 14 produtos enviados.
```

## 3. Contraste com a segunda causa

resposta_truncada e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, resposta_truncada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[resposta_truncada]`; verbetes citados: `resposta_truncada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `entidade-produto`, `contrato-produto`, `resposta_truncada` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | confere | verbetes: `resposta_truncada` |
| fonte_formato_valido | `[resposta_truncada]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["resposta_truncada"]} |
| fonte_contem_termo_da_causa | `resposta_truncada` | confere | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 93 | 1 | entrada | programa | ao_vivo | 2026-11-03T21:10:12 | caso lex-5 |
| 94 | 2 | candidatos | programa | ao_vivo | 2026-11-03T21:10:12 | 3 de 40 verbetes entregues |
| 96 | 3 | prompt | programa | ao_vivo | 2026-11-03T21:10:12 | {"chars": 3778, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "127ebd016915", "sha": "127ebd0169151153"} |
| 98 | 4 | inferencia | programa | ao_vivo | 2026-11-03T21:10:12 | diagnostico: 73,2 s |
| 99 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T21:10:12 | causa_raiz: `resposta_truncada` |
| 100 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T21:10:12 | campo: `nenhum` |
| 101 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T21:10:12 | impacto: `O usuário vê uma lista incompleta de produtos, recebendo apenas o primeiro item ou uma lista vazia.` |
| 102 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T21:10:12 | fonte: `[resposta_truncada]` |
| 103 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T21:10:12 | fonte_citada: `resposta_truncada` |
| 104 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T21:10:12 | quatro_linhas_presentes: confere |
| 105 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T21:10:12 | rotulo_no_conjunto: confere |
| 106 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T21:10:12 | fonte_existe_na_biblioteca: confere |
| 107 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T21:10:12 | fonte_estava_no_contexto: confere |
| 108 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T21:10:12 | campo_existe_no_caso: nao_se_aplica |
| 109 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T21:10:12 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 110 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T21:10:12 | notas_nos_verbetes_citados: informativo |
| 111 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T21:10:12 | impacto: nao_verificavel |
| 112 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T21:10:12 | fonte_formato_valido: confere |
| 113 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T21:10:12 | fonte_contem_termo_da_causa: confere |
| 114 | 20 | decisao | programa | ao_vivo | 2026-11-03T21:10:12 | diagnostico: escolha resposta_truncada; divergência não |
| 117 | 21 | inferencia | programa | ao_vivo | 2026-11-03T21:11:29 | proposta: 170,4 s |
| 119 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:11:29 | proposta 1: nota em [resposta_truncada]: recusada: sem_evidencia_do_caso |
| 121 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:11:29 | proposta 2: novo_verbete em [resposta_truncada]: recusada: id_repetido |
| 122 | 24 | decisao | programa | ao_vivo | 2026-11-03T21:11:29 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 114, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 94 (verbete_entregue, entidade-produto), evento 94 (verbete_entregue, contrato-produto), evento 94 (verbete_entregue, resposta_truncada), evento 98 (resposta), evento 103 (verbete_citado, resposta_truncada); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, resposta_truncada (gen_ai: chat)
- evento 122, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 98 (resposta), evento 117 (resposta), evento 119 (verbete_entregue, resposta_truncada), evento 121 (verbete_entregue, resposta_truncada); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: contrato-produto, entidade-produto, resposta_truncada

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 93 a 122 da trilha; hash dos eventos deste caso: `b760f9f4bea1f544`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
