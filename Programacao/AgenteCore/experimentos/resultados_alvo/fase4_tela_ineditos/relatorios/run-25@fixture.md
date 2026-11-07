<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-25`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/run-25@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,83) · **CONFLITO**: nenhum verbete entregue trata da causa respondida tempo_de_resposta_excedido

**IMPACTO (declarado):** `O usuário vê um comportamento lento do sistema, com o modal demorando cerca de 2 segundos para abrir.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido porque os verbetes entidade-produto, ancora-saiba-mais, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,12. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida tempo_de_resposta_excedido. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/7

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}

SINTOMA OBSERVADO: Ao clicar em 'Saiba Mais...' do Cupim, nada acontece por cerca de 2 segundos e so entao o modal abre, com os dados certos. O roteiro espera o modal por 1 segundo e reprova por tempo.

OBSERVAÇÃO ADICIONAL: As outras requisicoes da mesma sessao responderam em menos de 100 ms.
```

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não tipo_divergente: a escolha tem probabilidade 0,83 contra 0,12; verbete(s) na evidência: entidade-produto, ancora-saiba-mais, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 0,83 | sim |
| tipo_divergente | 0,12 |  |
| colecao_no_lugar_de_objeto | 0,01 |  |
| resposta_truncada | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| formato_de_data_divergente | 0,01 |  |
| valor_fora_do_dominio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[ancora-saiba-mais]`; verbetes citados: `ancora-saiba-mais`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `ancora-saiba-mais` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `ancora-saiba-mais` | confere | contexto: `entidade-produto`, `ancora-saiba-mais`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[ancora-saiba-mais]` | confere | {"ids": ["ancora-saiba-mais"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `ancora-saiba-mais` | **não confere** | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids run-25 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1586 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:28:15 | caso run-25 |
| 1587 | 2 | candidatos | programa | ao_vivo | 2026-11-06T12:28:15 | 3 de 39 verbetes entregues |
| 1589 | 3 | prompt | programa | ao_vivo | 2026-11-06T12:28:15 | {"etapa": "diagnostico", "sha": "01f02331080023c8", "prompt_sha256": "01f023310800", "chars": 3593, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1591 | 4 | inferencia | programa | ao_vivo | 2026-11-06T12:28:15 | diagnostico: 73,5 s |
| 1592 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T12:28:15 | causa_raiz: `tempo_de_resposta_excedido` |
| 1593 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T12:28:15 | campo: `nenhum` |
| 1594 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T12:28:15 | impacto: `O usuário vê um comportamento lento do sistema, com o modal demorando cerca de 2 segundos para abrir.` |
| 1595 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T12:28:15 | fonte: `[ancora-saiba-mais]` |
| 1596 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T12:28:15 | fonte_citada: `ancora-saiba-mais` |
| 1597 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T12:28:15 | quatro_linhas_presentes: confere |
| 1598 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:28:15 | rotulo_no_conjunto: confere |
| 1599 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:28:15 | fonte_existe_na_biblioteca: confere |
| 1600 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:28:15 | fonte_estava_no_contexto: confere |
| 1601 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T12:28:15 | campo_existe_no_caso: nao_se_aplica |
| 1602 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T12:28:15 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1603 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T12:28:15 | notas_nos_verbetes_citados: informativo |
| 1604 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:28:15 | impacto: nao_verificavel |
| 1605 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:28:15 | fonte_formato_valido: confere |
| 1606 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:28:15 | fonte_contem_termo_da_causa: nao_confere |
| 1607 | 20 | decisao | programa | ao_vivo | 2026-11-06T12:28:15 | diagnostico: escolha tempo_de_resposta_excedido; divergência sim |

</details>

Nós de decisão:

- evento 1607, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 1587 (verbete_entregue, entidade-produto), evento 1587 (verbete_entregue, ancora-saiba-mais), evento 1587 (verbete_entregue, contrato-produto), evento 1591 (resposta), evento 1596 (verbete_citado, ancora-saiba-mais); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, ancora-saiba-mais, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1586 a 1607 da trilha; hash dos eventos deste caso: `4d3414dbce455dc6`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
