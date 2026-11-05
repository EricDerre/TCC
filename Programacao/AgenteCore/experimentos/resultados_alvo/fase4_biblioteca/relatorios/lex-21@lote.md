<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/lex-21@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `status` · selo de probabilidade: **medio** (p = 0,96) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `O usuário recebeu um status com caracteres inválidos, o que pode causar confusão e erros na interpretação dos dados.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo status porque os verbetes contrato-pedido, pedido-reserva, formato_de_data_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,03. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em AnÃ¡lise", "nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 8, "pessoas": 2, "data_pedido": "2026-09-15", "status": "Em Análise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: Na mesma resposta de GET /api/pedidos, a reserva 7 traz status 'Em AnÃ¡lise' com simbolo no lugar do acento, e a reserva 8 (mesmo cliente, mesma consulta) traz 'Em Análise' certinho.

OBSERVAÇÃO ADICIONAL: As duas reservas foram gravadas pelo mesmo formulario (cliente/registrar_reserva.php), na mesma tabela tbpedido_reserva.
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não campo_ausente: a escolha tem probabilidade 0,96 contra 0,03; verbete(s) na evidência: contrato-pedido, pedido-reserva, formato_de_data_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 0,96 | sim |
| campo_ausente | 0,03 |  |
| campo_renomeado | 0,03 |  |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `formato_de_data_divergente` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-pedido"]} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `status` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2112 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:43:36 | caso lex-21 |
| 2113 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:43:36 | 3 de 46 verbetes entregues |
| 2115 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:43:36 | {"chars": 3769, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "71f890928108", "sha": "71f890928108cf9f"} |
| 2117 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:43:36 | diagnostico: 74,6 s |
| 2118 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:43:36 | causa_raiz: `codificacao_incorreta` |
| 2119 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:43:36 | campo: `status` |
| 2120 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:43:36 | impacto: `O usuário recebeu um status com caracteres inválidos, o que pode causar confusão e erros na interpretação dos dados.` |
| 2121 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:43:36 | fonte: `[contrato-pedido]` |
| 2122 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:43:36 | fonte_citada: `contrato-pedido` |
| 2123 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:43:36 | quatro_linhas_presentes: confere |
| 2124 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:43:36 | rotulo_no_conjunto: confere |
| 2125 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:43:36 | fonte_existe_na_biblioteca: confere |
| 2126 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:43:36 | fonte_estava_no_contexto: confere |
| 2127 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:43:36 | campo_existe_no_caso: confere |
| 2128 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:43:36 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2129 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:43:36 | notas_nos_verbetes_citados: informativo |
| 2130 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:43:36 | impacto: nao_verificavel |
| 2131 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:43:36 | fonte_formato_valido: confere |
| 2132 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:43:36 | fonte_contem_termo_da_causa: nao_confere |
| 2133 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:43:36 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 2133, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 2113 (verbete_entregue, contrato-pedido), evento 2113 (verbete_entregue, pedido-reserva), evento 2113 (verbete_entregue, formato_de_data_divergente), evento 2117 (resposta), evento 2122 (verbete_citado, contrato-pedido); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-pedido, pedido-reserva, formato_de_data_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2112 a 2133 da trilha; hash dos eventos deste caso: `3469a761bfde2de7`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
