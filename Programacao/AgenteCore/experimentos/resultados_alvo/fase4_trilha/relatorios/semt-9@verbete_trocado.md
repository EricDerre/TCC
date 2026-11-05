<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-9@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-9@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `destaque` · selo de probabilidade: **baixo** (p = 0,46)

**IMPACTO (declarado):** `O produto é exibido como destacado na interface, mesmo que o campo destaque esteja com um valor inválido (2 em vez de Booleano).`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo destaque porque o sinal destaque: esperado booleano, recebido inteiro está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,23. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,46); trate como hipótese e confira o campo destaque antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 2751): regras diff_contra_contrato; antes {"chars": 146}, depois {"chars": 146}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| destaque | booleano | inteiro |

Trecho podado (hash `2203e279e833f5c4`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": 2}]
```

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,46 contra 0,23; verbete(s) na evidência: entidade-produto, contrato-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,46 | sim |
| campo_ausente | 0,23 |  |
| campo_renomeado | 0,23 |  |
| valor_fora_do_dominio | 0,17 |  |
| estrutura_aninhada_divergente | 0,12 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-9 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2750 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:36:34 | caso semt-9@verbete_trocado |
| 2751 | 2 | poda | programa | ao_vivo | 2026-11-05T01:36:34 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2752 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:36:34 | poda: escolha json/lista; destaque:tipo_diferente; divergência não |
| 2753 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:36:34 | 3 de 39 verbetes entregues |
| 2754 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:36:34 | recuperacao: escolha entidade-produto,contrato-produto,estrutura_aninhada_divergente; divergência não |
| 2755 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:36:34 | {"etapa": "diagnostico", "sha": "9e64a31ec20d52bd", "prompt_sha256": "9e64a31ec20d", "chars": 3642, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2757 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:36:34 | diagnostico: 16,9 s |
| 2758 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:36:34 | causa_raiz: `tipo_divergente` |
| 2759 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:36:34 | campo: `destaque` |
| 2760 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:36:34 | impacto: `O produto é exibido como destacado na interface, mesmo que o campo destaque esteja com um valor inválido (2 em vez de Booleano).` |
| 2761 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:36:34 | fonte: `[contrato-produto]` |
| 2762 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:36:34 | fonte_citada: `contrato-produto` |
| 2763 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:34 | quatro_linhas_presentes: confere |
| 2764 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:34 | rotulo_no_conjunto: confere |
| 2765 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:34 | fonte_existe_na_biblioteca: confere |
| 2766 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:34 | fonte_estava_no_contexto: confere |
| 2767 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:34 | campo_existe_no_caso: confere |
| 2768 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:34 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2769 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:34 | notas_nos_verbetes_citados: informativo |
| 2770 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:34 | impacto: nao_verificavel |
| 2771 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:34 | fonte_formato_valido: confere |
| 2772 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:34 | fonte_contem_termo_da_causa: nao_confere |
| 2773 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:36:34 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 2752, `poda`: escolha `json/lista; destaque:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 2751 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: destaque (gen_ai: plan)
- evento 2754, `recuperacao`: escolha `entidade-produto,contrato-produto,estrutura_aninhada_divergente`; resultado verbetes_entregues; evidência: evento 2753 (verbete_entregue, entidade-produto), evento 2753 (verbete_entregue, contrato-produto), evento 2753 (verbete_entregue, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, estrutura_aninhada_divergente (gen_ai: retrieval)
- evento 2773, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 2751 (sinal_em_codigo), evento 2753 (verbete_entregue, entidade-produto), evento 2753 (verbete_entregue, contrato-produto), evento 2753 (verbete_entregue, estrutura_aninhada_divergente), evento 2757 (resposta), evento 2762 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2750 a 2773 da trilha; hash dos eventos deste caso: `4085083a9d367eeb`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
