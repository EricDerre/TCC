<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-1@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-1@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `formato_de_data_divergente` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,46) · **CONFLITO**: nenhum verbete entregue trata da causa respondida formato_de_data_divergente

**IMPACTO (declarado):** `O usuário vê a ordenação incorreta do preço, com 'R$ 9,90' aparecendo após 'R$ 89,90'.`

Justificativa (gerada por molde): O agente respondeu formato_de_data_divergente no campo preco porque o sinal preco: esperado numero, recebido texto está presente na resposta HTTP e os verbetes entidade-produto, nulo_inesperado, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,46. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida formato_de_data_divergente. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,46); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 528): regras diff_contra_contrato; antes {"chars": 152}, depois {"chars": 152}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | texto |

Trecho podado (hash `20cdbc76d4a473bf`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": "89.90", "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

formato_de_data_divergente e não tipo_divergente: a escolha tem probabilidade 0,46 contra 0,46; verbete(s) na evidência: entidade-produto, nulo_inesperado, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,46 |  |
| formato_de_data_divergente | 0,46 | sim |
| valor_fora_do_dominio | 0,05 |  |
| escala_ou_unidade_errada | 0,03 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `nulo_inesperado`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `nulo_inesperado`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "formato_de_data_divergente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "formato_de_data_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-1 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 527 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:31:00 | caso semt-1@verbete_trocado |
| 528 | 2 | poda | programa | ao_vivo | 2026-11-04T23:31:00 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 529 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:31:00 | poda: escolha json/lista; preco:tipo_diferente; divergência não |
| 530 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:31:00 | 3 de 39 verbetes entregues |
| 531 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:31:00 | recuperacao: escolha entidade-produto,nulo_inesperado,contrato-produto; divergência não |
| 532 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:31:00 | {"etapa": "diagnostico", "sha": "a6ce4e5f4a0d4f58", "prompt_sha256": "a6ce4e5f4a0d", "chars": 3370, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 533 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:31:00 | diagnostico: 19,7 s |
| 534 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:31:00 | causa_raiz: `formato_de_data_divergente` |
| 535 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:31:00 | campo: `nenhum` |
| 536 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:31:00 | impacto: `O usuário vê a ordenação incorreta do preço, com 'R$ 9,90' aparecendo após 'R$ 89,90'.` |
| 537 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:31:00 | fonte: `[entidade-produto], [contrato-produto]` |
| 538 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:31:00 | fonte_citada: `entidade-produto` |
| 539 | 13 | declaracao | modelo | ao_vivo | 2026-11-04T23:31:00 | fonte_citada: `contrato-produto` |
| 540 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | quatro_linhas_presentes: confere |
| 541 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | rotulo_no_conjunto: confere |
| 542 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | fonte_existe_na_biblioteca: confere |
| 543 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | fonte_existe_na_biblioteca: confere |
| 544 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | fonte_estava_no_contexto: confere |
| 545 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | fonte_estava_no_contexto: confere |
| 546 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | campo_existe_no_caso: nao_se_aplica |
| 547 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 548 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | notas_nos_verbetes_citados: informativo |
| 549 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | impacto: nao_verificavel |
| 550 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | fonte_formato_valido: confere |
| 551 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | fonte_contem_termo_da_causa: nao_confere |
| 552 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:00 | fonte_contem_termo_da_causa: nao_confere |
| 553 | 27 | decisao | programa | ao_vivo | 2026-11-04T23:31:00 | diagnostico: escolha formato_de_data_divergente; divergência sim |

</details>

Nós de decisão:

- evento 529, `poda`: escolha `json/lista; preco:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 528 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: preco (gen_ai: plan)
- evento 531, `recuperacao`: escolha `entidade-produto,nulo_inesperado,contrato-produto`; resultado verbetes_entregues; evidência: evento 530 (verbete_entregue, entidade-produto), evento 530 (verbete_entregue, nulo_inesperado), evento 530 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, nulo_inesperado, contrato-produto (gen_ai: retrieval)
- evento 553, `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido; evidência: evento 528 (sinal_em_codigo), evento 530 (verbete_entregue, entidade-produto), evento 530 (verbete_entregue, nulo_inesperado), evento 530 (verbete_entregue, contrato-produto), evento 533 (resposta), evento 538 (verbete_citado, entidade-produto), evento 539 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, nulo_inesperado, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 527 a 553 da trilha; hash dos eventos deste caso: `7edbac08aa2e4398`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
