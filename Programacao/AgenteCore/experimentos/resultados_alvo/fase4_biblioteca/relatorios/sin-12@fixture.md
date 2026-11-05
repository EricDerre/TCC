<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-12`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-12@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,59) · **CONFLITO**: nenhum verbete entregue trata da causa respondida colecao_no_lugar_de_objeto

**IMPACTO (declarado):** `A interface web exibe uma reserva incompleta, enquanto outra reserva aparece normalmente.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto porque os verbetes contrato-pedido, pedido-reserva, formato_de_data_divergente estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,19 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida colecao_no_lugar_de_objeto. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,59); trate como hipótese e confira o caso antes de agir.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (texto_curto, id_repetido) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso sin-12. A proposta 1 (nota em [campo_ausente]) foi recusada por a validação da Fase 3 com o código texto_curto: TEXTO com 57 caracteres (mínimo 60). A proposta 2 (novo_verbete em [campo_ausente]) foi recusada por a validação da Fase 3 com o código id_repetido: 'campo_ausente' já é id de verbete ou nome de causa raiz.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `campo_ausente` | recusada: `texto_curto` | nenhum | recusada: `texto_curto` |  |
| 2 | novo_verbete | `campo_ausente` | recusada: `id_repetido` | nenhum | recusada: `id_repetido` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 8, "pessoas": 2, "data_pedido": "2026-09-15", "status": "Em Analise", "nome": "Cliente Teste"}]

SINTOMA OBSERVADO: Uma das reservas do cliente some da tela; a outra aparece normalmente.
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não resposta_truncada: a escolha tem probabilidade 0,59 contra 0,19; verbete(s) na evidência: contrato-pedido, pedido-reserva, formato_de_data_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,59 | sim |
| resposta_truncada | 0,19 |  |
| formato_de_data_divergente | 0,09 |  |
| registro_duplicado | 0,05 |  |
| estrutura_aninhada_divergente | 0,02 |  |
| chave_de_juncao_errada | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| valor_fora_do_dominio | 0,01 |  |
| estado_da_tela_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| nulo_inesperado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `formato_de_data_divergente` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-pedido"]} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 783 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:23:59 | caso sin-12 |
| 784 | 2 | candidatos | programa | ao_vivo | 2026-11-03T22:23:59 | 3 de 40 verbetes entregues |
| 786 | 3 | prompt | programa | ao_vivo | 2026-11-03T22:23:59 | {"chars": 3299, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "2e9041ab3ff2", "sha": "2e9041ab3ff22591"} |
| 788 | 4 | inferencia | programa | ao_vivo | 2026-11-03T22:23:59 | diagnostico: 64,2 s |
| 789 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T22:23:59 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 790 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T22:23:59 | campo: `nenhum` |
| 791 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T22:23:59 | impacto: `A interface web exibe uma reserva incompleta, enquanto outra reserva aparece normalmente.` |
| 792 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T22:23:59 | fonte: `[contrato-pedido]` |
| 793 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T22:23:59 | fonte_citada: `contrato-pedido` |
| 794 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T22:23:59 | quatro_linhas_presentes: confere |
| 795 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T22:23:59 | rotulo_no_conjunto: confere |
| 796 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T22:23:59 | fonte_existe_na_biblioteca: confere |
| 797 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T22:23:59 | fonte_estava_no_contexto: confere |
| 798 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T22:23:59 | campo_existe_no_caso: nao_se_aplica |
| 799 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T22:23:59 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 800 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T22:23:59 | notas_nos_verbetes_citados: informativo |
| 801 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T22:23:59 | impacto: nao_verificavel |
| 802 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T22:23:59 | fonte_formato_valido: confere |
| 803 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T22:23:59 | fonte_contem_termo_da_causa: nao_confere |
| 804 | 20 | decisao | programa | ao_vivo | 2026-11-03T22:23:59 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência sim |
| 807 | 21 | inferencia | programa | ao_vivo | 2026-11-03T22:25:07 | proposta: 154,3 s |
| 809 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:25:07 | proposta 1: nota em [campo_ausente]: recusada: texto_curto |
| 811 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:25:07 | proposta 2: novo_verbete em [campo_ausente]: recusada: id_repetido |
| 812 | 24 | decisao | programa | ao_vivo | 2026-11-03T22:25:07 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 804, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 784 (verbete_entregue, contrato-pedido), evento 784 (verbete_entregue, pedido-reserva), evento 784 (verbete_entregue, formato_de_data_divergente), evento 788 (resposta), evento 793 (verbete_citado, contrato-pedido); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-pedido, pedido-reserva, formato_de_data_divergente (gen_ai: chat)
- evento 812, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 788 (resposta), evento 807 (resposta), evento 809 (verbete_entregue, campo_ausente), evento 811 (verbete_entregue, campo_ausente); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: campo_ausente, contrato-pedido, formato_de_data_divergente, pedido-reserva

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 783 a 812 da trilha; hash dos eventos deste caso: `2dc58ecbb0d0afcd`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
