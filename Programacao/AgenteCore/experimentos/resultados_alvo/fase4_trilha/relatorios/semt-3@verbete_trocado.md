<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-3@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-3@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `status` · selo de probabilidade: **medio** (p = 0,93)

**IMPACTO (declarado):** `A reserva não aparece nem como ativa nem como cancelada na área do cliente, pois o status 'Pendente' não está dentro do domínio permitido ('Em Análise' ou 'Cancelado').`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo status porque o sinal status: esperado texto ('Em Analise' ou 'Cancelado'), recebido "Pendente" está presente na resposta HTTP e os verbetes formato_de_data_divergente, estado_da_tela_divergente, valor_fora_do_dominio estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,04. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 645): regras diff_contra_contrato; antes {"chars": 130}, depois {"chars": 130}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| status | texto ('Em Analise' ou 'Cancelado') | "Pendente" |

Trecho podado (hash `592187265d51788d`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Pendente", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

valor_fora_do_dominio e não formato_de_data_divergente: a escolha tem probabilidade 0,93 contra 0,04; verbete(s) na evidência: formato_de_data_divergente, estado_da_tela_divergente, valor_fora_do_dominio

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 0,93 | sim |
| formato_de_data_divergente | 0,04 |  |
| tipo_divergente | 0,02 |  |
| estado_da_tela_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[valor_fora_do_dominio]`; verbetes citados: `valor_fora_do_dominio`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `valor_fora_do_dominio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `valor_fora_do_dominio` | confere | contexto: `formato_de_data_divergente`, `estado_da_tela_divergente`, `valor_fora_do_dominio` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `valor_fora_do_dominio` |
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
| 644 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:37:54 | caso semt-3@verbete_trocado |
| 645 | 2 | poda | programa | ao_vivo | 2026-11-04T23:37:54 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 646 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:37:54 | poda: escolha json/lista; status:fora_do_dominio; divergência não |
| 647 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:37:54 | 3 de 39 verbetes entregues |
| 648 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:37:54 | recuperacao: escolha formato_de_data_divergente,estado_da_tela_divergente,valor_fora_do_dominio; divergência não |
| 649 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:37:54 | {"etapa": "diagnostico", "sha": "ec686b595f7f001b", "prompt_sha256": "ec686b595f7f", "chars": 3457, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 650 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:37:54 | diagnostico: 21,0 s |
| 651 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:37:54 | causa_raiz: `valor_fora_do_dominio` |
| 652 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:37:54 | campo: `status` |
| 653 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:37:54 | impacto: `A reserva não aparece nem como ativa nem como cancelada na área do cliente, pois o status 'Pendente' não está dentro do domínio permitido ('Em Análise' ou 'Cancelado').` |
| 654 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:37:54 | fonte: `[valor_fora_do_dominio]` |
| 655 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:37:54 | fonte_citada: `valor_fora_do_dominio` |
| 656 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:37:54 | quatro_linhas_presentes: confere |
| 657 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:37:54 | rotulo_no_conjunto: confere |
| 658 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:37:54 | fonte_existe_na_biblioteca: confere |
| 659 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:37:54 | fonte_estava_no_contexto: confere |
| 660 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:37:54 | campo_existe_no_caso: confere |
| 661 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:37:54 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 662 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:37:54 | notas_nos_verbetes_citados: informativo |
| 663 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:37:54 | impacto: nao_verificavel |
| 664 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:37:54 | fonte_formato_valido: confere |
| 665 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:37:54 | fonte_contem_termo_da_causa: confere |
| 666 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:37:54 | diagnostico: escolha valor_fora_do_dominio; divergência não |

</details>

Nós de decisão:

- evento 646, `poda`: escolha `json/lista; status:fora_do_dominio`; resultado sinais_em_codigo; evidência: evento 645 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: status (gen_ai: plan)
- evento 648, `recuperacao`: escolha `formato_de_data_divergente,estado_da_tela_divergente,valor_fora_do_dominio`; resultado verbetes_entregues; evidência: evento 647 (verbete_entregue, formato_de_data_divergente), evento 647 (verbete_entregue, estado_da_tela_divergente), evento 647 (verbete_entregue, valor_fora_do_dominio); divergência: não; falha: nenhuma; prov.used: formato_de_data_divergente, estado_da_tela_divergente, valor_fora_do_dominio (gen_ai: retrieval)
- evento 666, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 645 (sinal_em_codigo), evento 647 (verbete_entregue, formato_de_data_divergente), evento 647 (verbete_entregue, estado_da_tela_divergente), evento 647 (verbete_entregue, valor_fora_do_dominio), evento 650 (resposta), evento 655 (verbete_citado, valor_fora_do_dominio); divergência: não; falha: nenhuma; prov.used: formato_de_data_divergente, estado_da_tela_divergente, valor_fora_do_dominio (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 644 a 666 da trilha; hash dos eventos deste caso: `689afdedd868d7f5`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
