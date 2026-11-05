<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-9@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `formato_de_data_divergente` · **CAMPO:** `data_pedido` · selo de probabilidade: **medio** (p = 0,94)

**IMPACTO (declarado):** `A reserva aparece um dia antes do que o cliente escolheu.`

Justificativa (gerada por molde): O agente respondeu formato_de_data_divergente no campo data_pedido porque os verbetes formato_de_data_divergente, contrato-pedido, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, escala_ou_unidade_errada, ficou com probabilidade 0,06. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (palavra_chave_invalida, palavra_chave_invalida) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso tra-9. A proposta 1 (retificacao em [formato_de_data_divergente]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: 'data noutro formato ou como numero; data deslocada um dia'. A proposta 2 (novo_verbete em [deslocamento_de_data]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: 'data noutro formato ou como numero; data deslocada um dia'.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | retificacao | `formato_de_data_divergente` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |
| 2 | novo_verbete | `deslocamento_de_data` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-09", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A reserva aparece sempre um dia antes do que o cliente escolheu.

OBSERVAÇÃO ADICIONAL: O cliente reservou para 2026-09-10; o banco gravou 2026-09-10.
```

## 3. Contraste com a segunda causa

formato_de_data_divergente e não escala_ou_unidade_errada: a escolha tem probabilidade 0,94 contra 0,06; verbete(s) na evidência: formato_de_data_divergente, contrato-pedido, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| formato_de_data_divergente | 0,94 | sim |
| escala_ou_unidade_errada | 0,06 |  |
| tipo_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| tempo_de_resposta_excedido | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[formato_de_data_divergente] [pedido-reserva]`; verbetes citados: `formato_de_data_divergente`, `pedido-reserva`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `formato_de_data_divergente` | confere |  |
| O verbete citado existe na biblioteca | `pedido-reserva` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `formato_de_data_divergente` | confere | contexto: `formato_de_data_divergente`, `contrato-pedido`, `pedido-reserva` |
| O verbete citado estava no contexto entregue ao modelo | `pedido-reserva` | confere | contexto: `formato_de_data_divergente`, `contrato-pedido`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | confere | verbetes: `formato_de_data_divergente`, `contrato-pedido` |
| fonte_formato_valido | `[formato_de_data_divergente] [pedido-reserva]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["formato_de_data_divergente", "pedido-reserva"]} |
| fonte_contem_termo_da_causa | `formato_de_data_divergente` | confere | {"termo": "formato_de_data_divergente"} |
| fonte_contem_termo_da_causa | `pedido-reserva` | **não confere** | {"termo": "formato_de_data_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `data_pedido` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>28 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1241 | 1 | entrada | programa | ao_vivo | 2026-11-03T23:10:43 | caso tra-9 |
| 1242 | 2 | candidatos | programa | ao_vivo | 2026-11-03T23:10:43 | 3 de 40 verbetes entregues |
| 1244 | 3 | prompt | programa | ao_vivo | 2026-11-03T23:10:43 | {"chars": 3269, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "ddaefcf144f4", "sha": "ddaefcf144f467e5"} |
| 1246 | 4 | inferencia | programa | ao_vivo | 2026-11-03T23:10:43 | diagnostico: 64,7 s |
| 1247 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T23:10:43 | causa_raiz: `formato_de_data_divergente` |
| 1248 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T23:10:43 | campo: `data_pedido` |
| 1249 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T23:10:43 | impacto: `A reserva aparece um dia antes do que o cliente escolheu.` |
| 1250 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T23:10:43 | fonte: `[formato_de_data_divergente] [pedido-reserva]` |
| 1251 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T23:10:43 | fonte_citada: `formato_de_data_divergente` |
| 1252 | 10 | declaracao | modelo | ao_vivo | 2026-11-03T23:10:43 | fonte_citada: `pedido-reserva` |
| 1253 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | quatro_linhas_presentes: confere |
| 1254 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | rotulo_no_conjunto: confere |
| 1255 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | fonte_existe_na_biblioteca: confere |
| 1256 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | fonte_existe_na_biblioteca: confere |
| 1257 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | fonte_estava_no_contexto: confere |
| 1258 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | fonte_estava_no_contexto: confere |
| 1259 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | campo_existe_no_caso: confere |
| 1260 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1261 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | notas_nos_verbetes_citados: informativo |
| 1262 | 20 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | impacto: nao_verificavel |
| 1263 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | fonte_formato_valido: confere |
| 1264 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | fonte_contem_termo_da_causa: confere |
| 1265 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T23:10:43 | fonte_contem_termo_da_causa: nao_confere |
| 1266 | 24 | decisao | programa | ao_vivo | 2026-11-03T23:10:43 | diagnostico: escolha formato_de_data_divergente; divergência não |
| 1269 | 25 | inferencia | programa | ao_vivo | 2026-11-03T23:11:52 | proposta: 173,4 s |
| 1271 | 26 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:11:52 | proposta 1: retificacao em [formato_de_data_divergente]: recusada: palavra_chave_invalida |
| 1272 | 27 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:11:52 | proposta 2: novo_verbete em [deslocamento_de_data]: recusada: palavra_chave_invalida |
| 1273 | 28 | decisao | programa | ao_vivo | 2026-11-03T23:11:52 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1266, `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido; evidência: evento 1242 (verbete_entregue, formato_de_data_divergente), evento 1242 (verbete_entregue, contrato-pedido), evento 1242 (verbete_entregue, pedido-reserva), evento 1246 (resposta), evento 1251 (verbete_citado, formato_de_data_divergente), evento 1252 (verbete_citado, pedido-reserva); divergência: não; falha: nenhuma; prov.used: formato_de_data_divergente, contrato-pedido, pedido-reserva (gen_ai: chat)
- evento 1273, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1246 (resposta), evento 1269 (resposta), evento 1271 (verbete_entregue, formato_de_data_divergente); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: contrato-pedido, escala_ou_unidade_errada, formato_de_data_divergente, pedido-reserva

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1241 a 1273 da trilha; hash dos eventos deste caso: `7d2f9123760a49f8`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
