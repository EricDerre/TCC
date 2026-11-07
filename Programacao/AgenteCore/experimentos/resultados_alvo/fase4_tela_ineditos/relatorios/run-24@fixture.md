<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-24`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/run-24@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `registro_duplicado` · **CAMPO:** `id` · selo de probabilidade: **medio** (p = 0,97) · **CONFLITO**: nenhum verbete entregue trata da causa respondida registro_duplicado

**IMPACTO (declarado):** `O usuário vê a Picanha ao Alho duplicada na grade, enquanto os outros produtos aparecem uma única vez.`

Justificativa (gerada por molde): O agente respondeu registro_duplicado no campo id porque os verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,01 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": false}]

SINTOMA OBSERVADO: A grade mostra o cartao da Picanha ao Alho duas vezes seguidas, identicos, e os outros produtos uma vez cada. A grade tem 15 cartoes; a tabela tbprodutos tem 14 linhas.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os 3 primeiros itens da lista recebida (15 itens no total).
```

## 3. Contraste com a segunda causa

registro_duplicado e não resposta_truncada: a escolha tem probabilidade 0,97 contra 0,01; verbete(s) na evidência: entidade-produto, contrato-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| registro_duplicado | 0,97 | sim |
| resposta_truncada | 0,01 |  |
| corpo_nao_e_json | 0,01 |  |
| corpo_vazio | 0,01 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| recurso_inexistente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [estrutura_aninhada_divergente]`; verbetes citados: `contrato-produto`, `estrutura_aninhada_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto] [estrutura_aninhada_divergente]` | confere | {"ids": ["contrato-produto", "estrutura_aninhada_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "registro_duplicado"} |
| fonte_contem_termo_da_causa | `estrutura_aninhada_divergente` | **não confere** | {"termo": "registro_duplicado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids run-24 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1517 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:25:15 | caso run-24 |
| 1518 | 2 | candidatos | programa | ao_vivo | 2026-11-06T12:25:15 | 3 de 39 verbetes entregues |
| 1520 | 3 | prompt | programa | ao_vivo | 2026-11-06T12:25:15 | {"etapa": "diagnostico", "sha": "1b56416b192aa1ed", "prompt_sha256": "1b56416b192a", "chars": 4201, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1522 | 4 | inferencia | programa | ao_vivo | 2026-11-06T12:25:15 | diagnostico: 67,7 s |
| 1523 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T12:25:15 | causa_raiz: `registro_duplicado` |
| 1524 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T12:25:15 | campo: `id` |
| 1525 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T12:25:15 | impacto: `O usuário vê a Picanha ao Alho duplicada na grade, enquanto os outros produtos aparecem uma única vez.` |
| 1526 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T12:25:15 | fonte: `[contrato-produto] [estrutura_aninhada_divergente]` |
| 1527 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T12:25:15 | fonte_citada: `contrato-produto` |
| 1528 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T12:25:15 | fonte_citada: `estrutura_aninhada_divergente` |
| 1529 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | quatro_linhas_presentes: confere |
| 1530 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | rotulo_no_conjunto: confere |
| 1531 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | fonte_existe_na_biblioteca: confere |
| 1532 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | fonte_existe_na_biblioteca: confere |
| 1533 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | fonte_estava_no_contexto: confere |
| 1534 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | fonte_estava_no_contexto: confere |
| 1535 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | campo_existe_no_caso: confere |
| 1536 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1537 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | notas_nos_verbetes_citados: informativo |
| 1538 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | impacto: nao_verificavel |
| 1539 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | fonte_formato_valido: confere |
| 1540 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | fonte_contem_termo_da_causa: nao_confere |
| 1541 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T12:25:15 | fonte_contem_termo_da_causa: nao_confere |
| 1542 | 24 | decisao | programa | ao_vivo | 2026-11-06T12:25:15 | diagnostico: escolha registro_duplicado; divergência sim |

</details>

Nós de decisão:

- evento 1542, `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido; evidência: evento 1518 (verbete_entregue, entidade-produto), evento 1518 (verbete_entregue, contrato-produto), evento 1518 (verbete_entregue, estrutura_aninhada_divergente), evento 1522 (resposta), evento 1527 (verbete_citado, contrato-produto), evento 1528 (verbete_citado, estrutura_aninhada_divergente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1517 a 1542 da trilha; hash dos eventos deste caso: `57b7707b7169293c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
