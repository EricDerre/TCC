<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-12`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-12@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `formato_de_data_divergente` · **CAMPO:** `data_pedido` · selo de probabilidade: **medio** (p = 0,84)

**IMPACTO (declarado):** `O usuário vê uma data em formato de timestamp em vez da data ISO esperada.`

Justificativa (gerada por molde): O agente respondeu formato_de_data_divergente no campo data_pedido porque os verbetes contrato-pedido, pedido-reserva, formato_de_data_divergente estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,15. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 1 recusada(s) (palavra_chave_invalida) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 1 edição(ões) para o caso semt-12. A proposta 1 (retificacao em [formato_de_data_divergente]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: '"invalid date"'.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | retificacao | `formato_de_data_divergente` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": 1789084800, "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A data da reserva aparece como 1789084800 na listagem.
```

## 3. Contraste com a segunda causa

formato_de_data_divergente e não tipo_divergente: a escolha tem probabilidade 0,84 contra 0,15; verbete(s) na evidência: contrato-pedido, pedido-reserva, formato_de_data_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| formato_de_data_divergente | 0,84 | sim |
| tipo_divergente | 0,15 |  |
| escala_ou_unidade_errada | 0,01 |  |
| valor_fora_do_dominio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| tempo_de_resposta_excedido | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[formato_de_data_divergente]`; verbetes citados: `formato_de_data_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `formato_de_data_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `formato_de_data_divergente` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `formato_de_data_divergente` |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | confere | verbetes: `contrato-pedido`, `formato_de_data_divergente` |
| fonte_formato_valido | `[formato_de_data_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["formato_de_data_divergente"]} |
| fonte_contem_termo_da_causa | `formato_de_data_divergente` | confere | {"termo": "formato_de_data_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `data_pedido` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1047 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:50:18 | caso semt-12 |
| 1048 | 2 | candidatos | programa | ao_vivo | 2026-11-03T22:50:18 | 3 de 40 verbetes entregues |
| 1050 | 3 | prompt | programa | ao_vivo | 2026-11-03T22:50:18 | {"chars": 3171, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "2e6626b74f01", "sha": "2e6626b74f01053b"} |
| 1052 | 4 | inferencia | programa | ao_vivo | 2026-11-03T22:50:18 | diagnostico: 33,4 s |
| 1053 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T22:50:18 | causa_raiz: `formato_de_data_divergente` |
| 1054 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T22:50:18 | campo: `data_pedido` |
| 1055 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T22:50:18 | impacto: `O usuário vê uma data em formato de timestamp em vez da data ISO esperada.` |
| 1056 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T22:50:18 | fonte: `[formato_de_data_divergente]` |
| 1057 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T22:50:18 | fonte_citada: `formato_de_data_divergente` |
| 1058 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T22:50:18 | quatro_linhas_presentes: confere |
| 1059 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T22:50:18 | rotulo_no_conjunto: confere |
| 1060 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T22:50:18 | fonte_existe_na_biblioteca: confere |
| 1061 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T22:50:18 | fonte_estava_no_contexto: confere |
| 1062 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T22:50:18 | campo_existe_no_caso: confere |
| 1063 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T22:50:18 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1064 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T22:50:18 | notas_nos_verbetes_citados: informativo |
| 1065 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T22:50:18 | impacto: nao_verificavel |
| 1066 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T22:50:18 | fonte_formato_valido: confere |
| 1067 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T22:50:18 | fonte_contem_termo_da_causa: confere |
| 1068 | 20 | decisao | programa | ao_vivo | 2026-11-03T22:50:18 | diagnostico: escolha formato_de_data_divergente; divergência não |
| 1071 | 21 | inferencia | programa | ao_vivo | 2026-11-03T22:50:55 | proposta: 128,2 s |
| 1073 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:50:55 | proposta 1: retificacao em [formato_de_data_divergente]: recusada: palavra_chave_invalida |
| 1074 | 23 | decisao | programa | ao_vivo | 2026-11-03T22:50:55 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1068, `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido; evidência: evento 1048 (verbete_entregue, contrato-pedido), evento 1048 (verbete_entregue, pedido-reserva), evento 1048 (verbete_entregue, formato_de_data_divergente), evento 1052 (resposta), evento 1057 (verbete_citado, formato_de_data_divergente); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, formato_de_data_divergente (gen_ai: chat)
- evento 1074, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1052 (resposta), evento 1071 (resposta), evento 1073 (verbete_entregue, formato_de_data_divergente); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: contrato-pedido, formato_de_data_divergente, pedido-reserva

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1047 a 1074 da trilha; hash dos eventos deste caso: `59c28dabb1d6041c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
