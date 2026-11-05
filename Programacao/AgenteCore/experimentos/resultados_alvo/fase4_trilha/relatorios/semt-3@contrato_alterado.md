<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-3@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-3@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `status` · selo de probabilidade: **medio** (p = 0,94)

**IMPACTO (declarado):** `O usuário vê uma reserva que nem está ativa nem cancelada na área do cliente.`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo status porque o sinal id_pedido: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes contrato-pedido, valor_fora_do_dominio, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, estado_da_tela_divergente, ficou com probabilidade 0,02 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 669): regras diff_contra_contrato; antes {"chars": 130}, depois {"chars": 130}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id_pedido | texto | inteiro |
| status | texto ('Em Analise' ou 'Cancelado') | "Pendente" |

Trecho podado (hash `592187265d51788d`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Pendente", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

valor_fora_do_dominio e não estado_da_tela_divergente: a escolha tem probabilidade 0,94 contra 0,02; verbete(s) na evidência: contrato-pedido, valor_fora_do_dominio, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 0,94 | sim |
| estado_da_tela_divergente | 0,02 |  |
| campo_ausente | 0,02 |  |
| campo_renomeado | 0,02 |  |
| formato_de_data_divergente | 0,01 |  |
| tipo_divergente | 0,01 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| registro_duplicado | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| dado_desatualizado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[valor_fora_do_dominio]`; verbetes citados: `valor_fora_do_dominio`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `valor_fora_do_dominio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `valor_fora_do_dominio` | confere | contexto: `contrato-pedido`, `valor_fora_do_dominio`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `contrato-pedido`, `valor_fora_do_dominio`, `pedido-reserva` |
| fonte_formato_valido | `[valor_fora_do_dominio]` | confere | {"ids": ["valor_fora_do_dominio"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `valor_fora_do_dominio` | confere | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `status` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-3 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 668 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:38:19 | caso semt-3@contrato_alterado |
| 669 | 2 | poda | programa | ao_vivo | 2026-11-04T23:38:19 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato |
| 670 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:38:19 | poda: escolha json/lista; id_pedido:tipo_diferente, status:fora_do_dominio; divergência não |
| 671 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:38:19 | 3 de 39 verbetes entregues |
| 672 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:38:19 | recuperacao: escolha contrato-pedido,valor_fora_do_dominio,pedido-reserva; divergência não |
| 674 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:38:19 | {"etapa": "diagnostico", "sha": "b70c6d58e8926048", "prompt_sha256": "b70c6d58e892", "chars": 3511, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 676 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:38:19 | diagnostico: 66,8 s |
| 677 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:38:19 | causa_raiz: `valor_fora_do_dominio` |
| 678 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:38:19 | campo: `status` |
| 679 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:38:19 | impacto: `O usuário vê uma reserva que nem está ativa nem cancelada na área do cliente.` |
| 680 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:38:19 | fonte: `[valor_fora_do_dominio]` |
| 681 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:38:19 | fonte_citada: `valor_fora_do_dominio` |
| 682 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:38:19 | quatro_linhas_presentes: confere |
| 683 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:38:19 | rotulo_no_conjunto: confere |
| 684 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:38:19 | fonte_existe_na_biblioteca: confere |
| 685 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:38:19 | fonte_estava_no_contexto: confere |
| 686 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:38:19 | campo_existe_no_caso: confere |
| 687 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:38:19 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 688 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:38:19 | notas_nos_verbetes_citados: informativo |
| 689 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:38:19 | impacto: nao_verificavel |
| 690 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:38:19 | fonte_formato_valido: confere |
| 691 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:38:19 | fonte_contem_termo_da_causa: confere |
| 692 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:38:19 | diagnostico: escolha valor_fora_do_dominio; divergência não |

</details>

Nós de decisão:

- evento 670, `poda`: escolha `json/lista; id_pedido:tipo_diferente, status:fora_do_dominio`; resultado sinais_em_codigo; evidência: evento 669 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id_pedido, status (gen_ai: plan)
- evento 672, `recuperacao`: escolha `contrato-pedido,valor_fora_do_dominio,pedido-reserva`; resultado verbetes_entregues; evidência: evento 671 (verbete_entregue, contrato-pedido), evento 671 (verbete_entregue, valor_fora_do_dominio), evento 671 (verbete_entregue, pedido-reserva); divergência: não; falha: nenhuma; prov.used: contrato-pedido, valor_fora_do_dominio, pedido-reserva (gen_ai: retrieval)
- evento 692, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 669 (sinal_em_codigo), evento 671 (verbete_entregue, contrato-pedido), evento 671 (verbete_entregue, valor_fora_do_dominio), evento 671 (verbete_entregue, pedido-reserva), evento 676 (resposta), evento 681 (verbete_citado, valor_fora_do_dominio); divergência: não; falha: nenhuma; prov.used: contrato-pedido, valor_fora_do_dominio, pedido-reserva (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 668 a 692 da trilha; hash dos eventos deste caso: `d4e634a9096b7b99`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
