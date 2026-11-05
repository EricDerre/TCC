<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-3`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-3@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `status` · selo de probabilidade: **alto** (p = 0,99) · **CONFLITO**: a inferência sem documentação mudou a resposta de valor_fora_do_dominio para tipo_divergente

**IMPACTO (declarado):** `A reserva não aparece nem como ativa nem como cancelada na área do cliente, pois o status 'Pendente' está fora do domínio permitido ('Em Análise' ou 'Cancelado').`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo status porque o sinal status: esperado texto ('Em Analise' ou 'Cancelado'), recebido "Pendente" está presente na resposta HTTP e os verbetes contrato-pedido, estado_da_tela_divergente, valor_fora_do_dominio estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete contrato-pedido não mudou a resposta: sem efeito medido do contexto. A troca do verbete contrato-pedido por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação mudou a resposta (de valor_fora_do_dominio para tipo_divergente). A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a inferência sem documentação mudou a resposta de valor_fora_do_dominio para tipo_divergente.

## 2. Evidência

Poda de `corpo_http` (evento 582): regras diff_contra_contrato; antes {"chars": 130}, depois {"chars": 130}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| status | texto ('Em Analise' ou 'Cancelado') | "Pendente" |

Trecho podado (hash `592187265d51788d`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Pendente", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

valor_fora_do_dominio e não tipo_divergente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: contrato-pedido, estado_da_tela_divergente, valor_fora_do_dominio

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 0,99 | sim |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| registro_duplicado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `estado_da_tela_divergente`, `valor_fora_do_dominio` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `contrato-pedido`, `valor_fora_do_dominio` |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"ids": ["contrato-pedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "valor_fora_do_dominio"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `contrato-pedido` | valor_fora_do_dominio | valor_fora_do_dominio | 0,99 | 0,99 | sem efeito medido do contexto |
| troca | `contrato-pedido` | valor_fora_do_dominio | valor_fora_do_dominio | 0,99 | 0,93 | sem efeito medido do contexto |
| sem_documentacao | `` | valor_fora_do_dominio | tipo_divergente | 0,99 | 0,10 | mudou a resposta: o verbete pesou na decisão |
| repeticao_da_base | `` | valor_fora_do_dominio | valor_fora_do_dominio | 0,99 | 0,99 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `status` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-3 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 580 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:32:08 | caso semt-3 |
| 582 | 2 | poda | programa | ao_vivo | 2026-11-04T23:32:08 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 583 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:32:08 | poda: escolha json/lista; status:fora_do_dominio; divergência não |
| 584 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:32:08 | 3 de 39 verbetes entregues |
| 585 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:32:08 | recuperacao: escolha contrato-pedido,estado_da_tela_divergente,valor_fora_do_dominio; divergência não |
| 587 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:32:08 | {"etapa": "diagnostico", "sha": "dd594ab2de4acb3c", "prompt_sha256": "dd594ab2de4a", "chars": 3612, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 589 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:32:08 | diagnostico: 76,2 s |
| 590 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:32:08 | causa_raiz: `valor_fora_do_dominio` |
| 591 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:32:08 | campo: `status` |
| 592 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:32:08 | impacto: `A reserva não aparece nem como ativa nem como cancelada na área do cliente, pois o status 'Pendente' está fora do domínio permitido ('Em Análise' ou 'Cancelado').` |
| 593 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:32:08 | fonte: `[contrato-pedido]` |
| 594 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:32:08 | fonte_citada: `contrato-pedido` |
| 595 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:32:08 | quatro_linhas_presentes: confere |
| 596 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:32:08 | rotulo_no_conjunto: confere |
| 597 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:32:08 | fonte_existe_na_biblioteca: confere |
| 598 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:32:08 | fonte_estava_no_contexto: confere |
| 599 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:32:08 | campo_existe_no_caso: confere |
| 600 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:32:08 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 601 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:32:08 | notas_nos_verbetes_citados: informativo |
| 602 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:32:08 | impacto: nao_verificavel |
| 603 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:32:08 | fonte_formato_valido: confere |
| 604 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:32:08 | fonte_contem_termo_da_causa: nao_confere |
| 607 | 23 | inferencia | programa | ao_vivo | 2026-11-04T23:32:08 | intervencao:remocao: 69,5 s |
| 608 | 24 | intervencao | verificacao | ao_vivo | 2026-11-04T23:32:08 | remocao de contrato-pedido: rótulo valor_fora_do_dominio para valor_fora_do_dominio |
| 611 | 25 | inferencia | programa | ao_vivo | 2026-11-04T23:32:08 | intervencao:troca: 67,5 s |
| 612 | 26 | intervencao | verificacao | ao_vivo | 2026-11-04T23:32:08 | troca de contrato-pedido: rótulo valor_fora_do_dominio para valor_fora_do_dominio |
| 615 | 27 | inferencia | programa | ao_vivo | 2026-11-04T23:32:08 | intervencao:sem_documentacao: 41,2 s |
| 616 | 28 | intervencao | verificacao | ao_vivo | 2026-11-04T23:32:08 | sem_documentacao de None: rótulo valor_fora_do_dominio para tipo_divergente |
| 617 | 29 | inferencia | programa | ao_vivo | 2026-11-04T23:32:08 | intervencao:repeticao_da_base: 20,2 s |
| 618 | 30 | intervencao | verificacao | ao_vivo | 2026-11-04T23:32:08 | repeticao_da_base de None: rótulo valor_fora_do_dominio para valor_fora_do_dominio |
| 619 | 31 | decisao | programa | ao_vivo | 2026-11-04T23:32:08 | diagnostico: escolha valor_fora_do_dominio; divergência sim |

</details>

Nós de decisão:

- evento 583, `poda`: escolha `json/lista; status:fora_do_dominio`; resultado sinais_em_codigo; evidência: evento 582 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: status (gen_ai: plan)
- evento 585, `recuperacao`: escolha `contrato-pedido,estado_da_tela_divergente,valor_fora_do_dominio`; resultado verbetes_entregues; evidência: evento 584 (verbete_entregue, contrato-pedido), evento 584 (verbete_entregue, estado_da_tela_divergente), evento 584 (verbete_entregue, valor_fora_do_dominio); divergência: não; falha: nenhuma; prov.used: contrato-pedido, estado_da_tela_divergente, valor_fora_do_dominio (gen_ai: retrieval)
- evento 619, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 582 (sinal_em_codigo), evento 584 (verbete_entregue, contrato-pedido), evento 584 (verbete_entregue, estado_da_tela_divergente), evento 584 (verbete_entregue, valor_fora_do_dominio), evento 589 (resposta), evento 594 (verbete_citado, contrato-pedido); divergência: sim; falha: nenhuma; prov.used: contrato-pedido, estado_da_tela_divergente, valor_fora_do_dominio (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 580 a 619 da trilha; hash dos eventos deste caso: `d17f16efa0b9247a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
