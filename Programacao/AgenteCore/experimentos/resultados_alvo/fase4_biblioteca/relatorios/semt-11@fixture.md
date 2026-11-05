<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-11`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-11@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `status` · selo de probabilidade: **medio** (p = 0,97)

**IMPACTO (declarado):** `O botão de cancelar não aparece porque o status 'Concluido' não está entre os valores permitidos ('Em Análise' ou 'Cancelado'), causando a lógica do sistema não reconhecer a reserva como válida para cancelamento.`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo status porque os verbetes contrato-pedido, estado_da_tela_divergente, valor_fora_do_dominio estavam entre os entregues ao modelo. A segunda causa, estado_da_tela_divergente, ficou com probabilidade 0,02. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 1 recusada(s) (arquivo_inexistente) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 1 edição(ões) para o caso semt-11. A proposta 1 (retificacao em [valor_fora_do_dominio]) foi recusada por a validação da Fase 3 com o código arquivo_inexistente: ARQUIVOS cita '[contrato-pedido]': não existe no repositório.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | retificacao | `valor_fora_do_dominio` | recusada: `arquivo_inexistente` | nenhum | recusada: `arquivo_inexistente` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Concluido", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: O botao de cancelar some para essa reserva, sem motivo aparente.
```

## 3. Contraste com a segunda causa

valor_fora_do_dominio e não estado_da_tela_divergente: a escolha tem probabilidade 0,97 contra 0,02; verbete(s) na evidência: contrato-pedido, estado_da_tela_divergente, valor_fora_do_dominio

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 0,97 | sim |
| estado_da_tela_divergente | 0,02 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| registro_duplicado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `estado_da_tela_divergente`, `valor_fora_do_dominio` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `contrato-pedido`, `valor_fora_do_dominio` |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-pedido"]} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `status` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1018 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:46:56 | caso semt-11 |
| 1019 | 2 | candidatos | programa | ao_vivo | 2026-11-03T22:46:56 | 3 de 40 verbetes entregues |
| 1021 | 3 | prompt | programa | ao_vivo | 2026-11-03T22:46:56 | {"chars": 3304, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "ff58021c303a", "sha": "ff58021c303a6a97"} |
| 1023 | 4 | inferencia | programa | ao_vivo | 2026-11-03T22:46:56 | diagnostico: 71,3 s |
| 1024 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T22:46:56 | causa_raiz: `valor_fora_do_dominio` |
| 1025 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T22:46:56 | campo: `status` |
| 1026 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T22:46:56 | impacto: `O botão de cancelar não aparece porque o status 'Concluido' não está entre os valores permitidos ('Em Análise' ou 'Cancelado'), causando a lógica do sistema não reconhecer a reserva como válida para cancelamento.` |
| 1027 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T22:46:56 | fonte: `[contrato-pedido]` |
| 1028 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T22:46:56 | fonte_citada: `contrato-pedido` |
| 1029 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T22:46:56 | quatro_linhas_presentes: confere |
| 1030 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T22:46:56 | rotulo_no_conjunto: confere |
| 1031 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T22:46:56 | fonte_existe_na_biblioteca: confere |
| 1032 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T22:46:56 | fonte_estava_no_contexto: confere |
| 1033 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T22:46:56 | campo_existe_no_caso: confere |
| 1034 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T22:46:56 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1035 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T22:46:56 | notas_nos_verbetes_citados: informativo |
| 1036 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T22:46:56 | impacto: nao_verificavel |
| 1037 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T22:46:56 | fonte_formato_valido: confere |
| 1038 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T22:46:56 | fonte_contem_termo_da_causa: nao_confere |
| 1039 | 20 | decisao | programa | ao_vivo | 2026-11-03T22:46:56 | diagnostico: escolha valor_fora_do_dominio; divergência não |
| 1042 | 21 | inferencia | programa | ao_vivo | 2026-11-03T22:48:12 | proposta: 122,3 s |
| 1044 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:48:12 | proposta 1: retificacao em [valor_fora_do_dominio]: recusada: arquivo_inexistente |
| 1045 | 23 | decisao | programa | ao_vivo | 2026-11-03T22:48:12 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1039, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 1019 (verbete_entregue, contrato-pedido), evento 1019 (verbete_entregue, estado_da_tela_divergente), evento 1019 (verbete_entregue, valor_fora_do_dominio), evento 1023 (resposta), evento 1028 (verbete_citado, contrato-pedido); divergência: não; falha: nenhuma; prov.used: contrato-pedido, estado_da_tela_divergente, valor_fora_do_dominio (gen_ai: chat)
- evento 1045, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1023 (resposta), evento 1042 (resposta), evento 1044 (verbete_entregue, valor_fora_do_dominio); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: contrato-pedido, estado_da_tela_divergente, valor_fora_do_dominio

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1018 a 1045 da trilha; hash dos eventos deste caso: `3e25b51a61ec99b1`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
