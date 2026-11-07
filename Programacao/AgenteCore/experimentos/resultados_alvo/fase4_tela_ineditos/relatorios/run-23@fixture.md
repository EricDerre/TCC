<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-23`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/run-23@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `recurso_inexistente` · **CAMPO:** `id` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê um erro "HTTP 404" ao tentar acessar detalhes do produto com ID 5, mesmo que esse ID esteja presente na lista de produtos.`

Justificativa (gerada por molde): O agente respondeu recurso_inexistente no campo id porque os verbetes recurso_inexistente, contrato-produto, mensagens-de-erro-do-codigo estavam entre os entregues ao modelo. A segunda causa, registro_duplicado, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/5

STATUS HTTP: 404

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "produto não encontrado"}

SINTOMA OBSERVADO: A grade foi carregada com os 14 cartoes, entre eles o da Alcatra na Pedra; ao clicar no 'Saiba Mais...' desse cartao, o modal abre com 'Erro' no titulo e 'HTTP 404' no corpo.

OBSERVAÇÃO ADICIONAL: O id 5 aparece na listagem GET /api/produtos feita antes do clique, e GET /api/produtos/5 respondeu 200 em chamadas anteriores.
```

## 3. Contraste com a segunda causa

recurso_inexistente e não registro_duplicado: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: recurso_inexistente, contrato-produto, mensagens-de-erro-do-codigo

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| recurso_inexistente | 1,00 | sim |
| registro_duplicado | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| resposta_truncada | 0,00 |  |
| localizador_quebrado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[recurso_inexistente]`; verbetes citados: `recurso_inexistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `recurso_inexistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `recurso_inexistente` | confere | contexto: `recurso_inexistente`, `contrato-produto`, `mensagens-de-erro-do-codigo` |
| Algum verbete do contexto trata da causa respondida | `recurso_inexistente` | confere | verbetes: `recurso_inexistente`, `contrato-produto`, `mensagens-de-erro-do-codigo` |
| fonte_formato_valido | `[recurso_inexistente]` | confere | {"ids": ["recurso_inexistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `recurso_inexistente` | confere | {"termo": "recurso_inexistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids run-23 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1461 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:23:14 | caso run-23 |
| 1462 | 2 | candidatos | programa | ao_vivo | 2026-11-06T12:23:14 | 3 de 39 verbetes entregues |
| 1464 | 3 | prompt | programa | ao_vivo | 2026-11-06T12:23:14 | {"etapa": "diagnostico", "sha": "97d4f7694a7cefab", "prompt_sha256": "97d4f7694a7c", "chars": 3566, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1466 | 4 | inferencia | programa | ao_vivo | 2026-11-06T12:23:14 | diagnostico: 56,6 s |
| 1467 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T12:23:14 | causa_raiz: `recurso_inexistente` |
| 1468 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T12:23:14 | campo: `id` |
| 1469 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T12:23:14 | impacto: `O usuário vê um erro "HTTP 404" ao tentar acessar detalhes do produto com ID 5, mesmo que esse ID esteja presente na lista de produtos.` |
| 1470 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T12:23:14 | fonte: `[recurso_inexistente]` |
| 1471 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T12:23:14 | fonte_citada: `recurso_inexistente` |
| 1472 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T12:23:14 | quatro_linhas_presentes: confere |
| 1473 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:23:14 | rotulo_no_conjunto: confere |
| 1474 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:23:14 | fonte_existe_na_biblioteca: confere |
| 1475 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:23:14 | fonte_estava_no_contexto: confere |
| 1476 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T12:23:14 | campo_existe_no_caso: confere |
| 1477 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T12:23:14 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1478 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T12:23:14 | notas_nos_verbetes_citados: informativo |
| 1479 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:23:14 | impacto: nao_verificavel |
| 1480 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:23:14 | fonte_formato_valido: confere |
| 1481 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:23:14 | fonte_contem_termo_da_causa: confere |
| 1482 | 20 | decisao | programa | ao_vivo | 2026-11-06T12:23:14 | diagnostico: escolha recurso_inexistente; divergência não |

</details>

Nós de decisão:

- evento 1482, `diagnostico`: escolha `recurso_inexistente`; resultado rotulo_emitido; evidência: evento 1462 (verbete_entregue, recurso_inexistente), evento 1462 (verbete_entregue, contrato-produto), evento 1462 (verbete_entregue, mensagens-de-erro-do-codigo), evento 1466 (resposta), evento 1471 (verbete_citado, recurso_inexistente); divergência: não; falha: nenhuma; prov.used: recurso_inexistente, contrato-produto, mensagens-de-erro-do-codigo (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1461 a 1482 da trilha; hash dos eventos deste caso: `d64c8575bfebb591`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
