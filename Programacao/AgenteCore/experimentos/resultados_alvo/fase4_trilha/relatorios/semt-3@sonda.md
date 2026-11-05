<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-3@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-3@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `status` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A reserva não aparece nem como ativa nem como cancelada na área do cliente, pois o status 'Pendente' está fora do domínio permitido ('Em Análise' ou 'Cancelado').`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo status porque o sinal status: esperado texto ('Em Analise' ou 'Cancelado'), recebido "Pendente" está presente na resposta HTTP e os verbetes contrato-pedido, estado_da_tela_divergente, valor_fora_do_dominio estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 621): regras diff_contra_contrato; antes {"chars": 130}, depois {"chars": 130}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| status | texto ('Em Analise' ou 'Cancelado') | "Pendente" |

Trecho podado (hash `592187265d51788d`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Pendente", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

valor_fora_do_dominio e não formato_de_data_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-pedido, estado_da_tela_divergente, valor_fora_do_dominio

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 1,00 | sim |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| registro_duplicado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `estado_da_tela_divergente`, `valor_fora_do_dominio` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `contrato-pedido`, `valor_fora_do_dominio` |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"ids": ["contrato-pedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `status` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-3 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 620 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:36:47 | caso semt-3@sonda |
| 621 | 2 | poda | programa | ao_vivo | 2026-11-04T23:36:47 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 622 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:36:47 | poda: escolha json/lista; status:fora_do_dominio; divergência não |
| 623 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:36:47 | 3 de 39 verbetes entregues |
| 624 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:36:47 | recuperacao: escolha contrato-pedido,estado_da_tela_divergente,valor_fora_do_dominio; divergência não |
| 626 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:36:47 | {"etapa": "diagnostico", "sha": "7363379e9eb14968", "prompt_sha256": "7363379e9eb1", "chars": 3731, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 627 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:36:47 | diagnostico: 63,1 s |
| 628 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:36:47 | causa_raiz: `valor_fora_do_dominio` |
| 629 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:36:47 | campo: `status` |
| 630 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:36:47 | impacto: `A reserva não aparece nem como ativa nem como cancelada na área do cliente, pois o status 'Pendente' está fora do domínio permitido ('Em Análise' ou 'Cancelado').` |
| 631 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:36:47 | fonte: `[contrato-pedido]` |
| 632 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:36:47 | fonte_citada: `contrato-pedido` |
| 633 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:36:47 | quatro_linhas_presentes: confere |
| 634 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:36:47 | rotulo_no_conjunto: confere |
| 635 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:36:47 | fonte_existe_na_biblioteca: confere |
| 636 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:36:47 | fonte_estava_no_contexto: confere |
| 637 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:36:47 | campo_existe_no_caso: confere |
| 638 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:36:47 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 639 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:36:47 | notas_nos_verbetes_citados: informativo |
| 640 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:36:47 | impacto: nao_verificavel |
| 641 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:36:47 | fonte_formato_valido: confere |
| 642 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:36:47 | fonte_contem_termo_da_causa: nao_confere |
| 643 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:36:47 | diagnostico: escolha valor_fora_do_dominio; divergência não |

</details>

Nós de decisão:

- evento 622, `poda`: escolha `json/lista; status:fora_do_dominio`; resultado sinais_em_codigo; evidência: evento 621 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: status (gen_ai: plan)
- evento 624, `recuperacao`: escolha `contrato-pedido,estado_da_tela_divergente,valor_fora_do_dominio`; resultado verbetes_entregues; evidência: evento 623 (verbete_entregue, contrato-pedido), evento 623 (verbete_entregue, estado_da_tela_divergente), evento 623 (verbete_entregue, valor_fora_do_dominio); divergência: não; falha: nenhuma; prov.used: contrato-pedido, estado_da_tela_divergente, valor_fora_do_dominio (gen_ai: retrieval)
- evento 643, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 621 (sinal_em_codigo), evento 623 (verbete_entregue, contrato-pedido), evento 623 (verbete_entregue, estado_da_tela_divergente), evento 623 (verbete_entregue, valor_fora_do_dominio), evento 627 (resposta), evento 632 (verbete_citado, contrato-pedido); divergência: não; falha: nenhuma; prov.used: contrato-pedido, estado_da_tela_divergente, valor_fora_do_dominio (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 620 a 643 da trilha; hash dos eventos deste caso: `18d7f800e45a3064`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
