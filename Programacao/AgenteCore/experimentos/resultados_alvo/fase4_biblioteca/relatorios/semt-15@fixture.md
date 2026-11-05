<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-15`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-15@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `pessoas` · selo de probabilidade: **baixo** (p = 0,67)

**IMPACTO (declarado):** `O restaurante não consegue alocar mesa porque a reserva tem 0 pessoas, o que é fora do domínio permitido pelo formulário que exige pelo menos 1 pessoa.`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo pessoas porque os verbetes contrato-pedido, pedido-reserva, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,17. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,67); trate como hipótese e confira o campo pessoas antes de agir.

**Biblioteca:** 1 edição(ões) aplicada(s) ([validacao-na-api]), 0 para revisão humana, 1 recusada(s) (duplicada).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso semt-15. A proposta 1 (retificacao em [valor_fora_do_dominio]) foi recusada por a validação da Fase 3 com o código duplicada: [valor_fora_do_dominio] já tem uma nota com este texto. A proposta 2 (novo_verbete em [validacao-na-api], peso 3) passou pela validação da Fase 3 e pelos filtros e entrou no lote.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | retificacao | `valor_fora_do_dominio` | recusada: `duplicada` | nenhum | recusada: `duplicada` |  |
| 2 | novo_verbete | `validacao-na-api` | aceita | nenhum | **aplicada** | 3 |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 0, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A reserva aparece na lista mas o restaurante nao consegue alocar mesa para ela.

OBSERVAÇÃO ADICIONAL: O formulario exige minimo de 1 pessoa (input com min=1).
```

## 3. Contraste com a segunda causa

valor_fora_do_dominio e não formato_de_data_divergente: a escolha tem probabilidade 0,67 contra 0,17; verbete(s) na evidência: contrato-pedido, pedido-reserva, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 0,67 | sim |
| formato_de_data_divergente | 0,17 |  |
| tipo_divergente | 0,09 |  |
| campo_ausente | 0,07 |  |
| campo_renomeado | 0,07 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[pedido-reserva]`; verbetes citados: `pedido-reserva`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `pedido-reserva` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `pedido-reserva` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `contrato-pedido`, `pedido-reserva` |
| fonte_formato_valido | `[pedido-reserva]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["pedido-reserva"]} |
| fonte_contem_termo_da_causa | `pedido-reserva` | **não confere** | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `pessoas` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1122 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:56:51 | caso semt-15 |
| 1123 | 2 | candidatos | programa | ao_vivo | 2026-11-03T22:56:51 | 3 de 40 verbetes entregues |
| 1125 | 3 | prompt | programa | ao_vivo | 2026-11-03T22:56:51 | {"chars": 3261, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "51bb506472a5", "sha": "51bb506472a50a8b"} |
| 1127 | 4 | inferencia | programa | ao_vivo | 2026-11-03T22:56:51 | diagnostico: 66,9 s |
| 1128 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T22:56:51 | causa_raiz: `valor_fora_do_dominio` |
| 1129 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T22:56:51 | campo: `pessoas` |
| 1130 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T22:56:51 | impacto: `O restaurante não consegue alocar mesa porque a reserva tem 0 pessoas, o que é fora do domínio permitido pelo formulário que exige pelo menos 1 pessoa.` |
| 1131 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T22:56:51 | fonte: `[pedido-reserva]` |
| 1132 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T22:56:51 | fonte_citada: `pedido-reserva` |
| 1133 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T22:56:51 | quatro_linhas_presentes: confere |
| 1134 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T22:56:51 | rotulo_no_conjunto: confere |
| 1135 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T22:56:51 | fonte_existe_na_biblioteca: confere |
| 1136 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T22:56:51 | fonte_estava_no_contexto: confere |
| 1137 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T22:56:51 | campo_existe_no_caso: confere |
| 1138 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T22:56:51 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1139 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T22:56:51 | notas_nos_verbetes_citados: informativo |
| 1140 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T22:56:51 | impacto: nao_verificavel |
| 1141 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T22:56:51 | fonte_formato_valido: confere |
| 1142 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T22:56:51 | fonte_contem_termo_da_causa: nao_confere |
| 1143 | 20 | decisao | programa | ao_vivo | 2026-11-03T22:56:51 | diagnostico: escolha valor_fora_do_dominio; divergência não |
| 1146 | 21 | inferencia | programa | ao_vivo | 2026-11-03T22:58:02 | proposta: 154,6 s |
| 1147 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:58:02 | proposta 1: retificacao em [valor_fora_do_dominio]: recusada: duplicada |
| 1149 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:58:02 | proposta 2: novo_verbete em [validacao-na-api]: aplicada |
| 1150 | 24 | decisao | programa | ao_vivo | 2026-11-03T22:58:02 | edicao_biblioteca: escolha proposta_2; divergência sim |

</details>

Nós de decisão:

- evento 1143, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 1123 (verbete_entregue, contrato-pedido), evento 1123 (verbete_entregue, pedido-reserva), evento 1123 (verbete_entregue, estado_da_tela_divergente), evento 1127 (resposta), evento 1132 (verbete_citado, pedido-reserva); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, estado_da_tela_divergente (gen_ai: chat)
- evento 1150, `edicao_biblioteca`: escolha `proposta_2`; resultado lote; evidência: evento 1127 (resposta), evento 1146 (resposta), evento 1147 (verbete_entregue, valor_fora_do_dominio); divergência: sim; falha: nenhuma; prov.used: contrato-pedido, estado_da_tela_divergente, pedido-reserva, valor_fora_do_dominio

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1122 a 1150 da trilha; hash dos eventos deste caso: `d8aba73694624b61`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
