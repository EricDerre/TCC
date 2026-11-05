<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-4`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-4@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `formato_de_data_divergente` · **CAMPO:** `data_pedido` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A data da reserva aparece como 'Invalid Date' na listagem.`

Justificativa (gerada por molde): O agente respondeu formato_de_data_divergente no campo data_pedido porque os verbetes contrato-pedido, formato_de_data_divergente, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (palavra_chave_invalida, palavra_chave_invalida) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso semt-4. A proposta 1 (nota em [formato_de_data_divergente]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: '"invalid date"'. A proposta 2 (retificacao em [formato_de_data_divergente]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: '"invalid date"'.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `formato_de_data_divergente` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |
| 2 | retificacao | `formato_de_data_divergente` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "10/09/2026", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A data da reserva aparece como 'Invalid Date' na listagem.
```

## 3. Contraste com a segunda causa

formato_de_data_divergente e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-pedido, formato_de_data_divergente, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| formato_de_data_divergente | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[formato_de_data_divergente]`; verbetes citados: `formato_de_data_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `formato_de_data_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `formato_de_data_divergente` | confere | contexto: `contrato-pedido`, `formato_de_data_divergente`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | confere | verbetes: `contrato-pedido`, `formato_de_data_divergente` |
| fonte_formato_valido | `[formato_de_data_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["formato_de_data_divergente"]} |
| fonte_contem_termo_da_causa | `formato_de_data_divergente` | confere | {"termo": "formato_de_data_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `data_pedido` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 311 | 1 | entrada | programa | ao_vivo | 2026-11-03T21:32:38 | caso semt-4 |
| 312 | 2 | candidatos | programa | ao_vivo | 2026-11-03T21:32:38 | 3 de 40 verbetes entregues |
| 314 | 3 | prompt | programa | ao_vivo | 2026-11-03T21:32:38 | {"chars": 3177, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "896443610241", "sha": "89644361024146b2"} |
| 316 | 4 | inferencia | programa | ao_vivo | 2026-11-03T21:32:38 | diagnostico: 62,9 s |
| 317 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T21:32:38 | causa_raiz: `formato_de_data_divergente` |
| 318 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T21:32:38 | campo: `data_pedido` |
| 319 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T21:32:38 | impacto: `A data da reserva aparece como 'Invalid Date' na listagem.` |
| 320 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T21:32:38 | fonte: `[formato_de_data_divergente]` |
| 321 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T21:32:38 | fonte_citada: `formato_de_data_divergente` |
| 322 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T21:32:38 | quatro_linhas_presentes: confere |
| 323 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T21:32:38 | rotulo_no_conjunto: confere |
| 324 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T21:32:38 | fonte_existe_na_biblioteca: confere |
| 325 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T21:32:38 | fonte_estava_no_contexto: confere |
| 326 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T21:32:38 | campo_existe_no_caso: confere |
| 327 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T21:32:38 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 328 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T21:32:38 | notas_nos_verbetes_citados: informativo |
| 329 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T21:32:38 | impacto: nao_verificavel |
| 330 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T21:32:38 | fonte_formato_valido: confere |
| 331 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T21:32:38 | fonte_contem_termo_da_causa: confere |
| 332 | 20 | decisao | programa | ao_vivo | 2026-11-03T21:32:38 | diagnostico: escolha formato_de_data_divergente; divergência não |
| 335 | 21 | inferencia | programa | ao_vivo | 2026-11-03T21:33:45 | proposta: 172,0 s |
| 337 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:33:45 | proposta 1: nota em [formato_de_data_divergente]: recusada: palavra_chave_invalida |
| 339 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:33:45 | proposta 2: retificacao em [formato_de_data_divergente]: recusada: palavra_chave_invalida |
| 340 | 24 | decisao | programa | ao_vivo | 2026-11-03T21:33:45 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 332, `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido; evidência: evento 312 (verbete_entregue, contrato-pedido), evento 312 (verbete_entregue, formato_de_data_divergente), evento 312 (verbete_entregue, pedido-reserva), evento 316 (resposta), evento 321 (verbete_citado, formato_de_data_divergente); divergência: não; falha: nenhuma; prov.used: contrato-pedido, formato_de_data_divergente, pedido-reserva (gen_ai: chat)
- evento 340, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 316 (resposta), evento 335 (resposta), evento 337 (verbete_entregue, formato_de_data_divergente), evento 339 (verbete_entregue, formato_de_data_divergente); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: contrato-pedido, formato_de_data_divergente, pedido-reserva

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 311 a 340 da trilha; hash dos eventos deste caso: `68dabbc444150e54`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
