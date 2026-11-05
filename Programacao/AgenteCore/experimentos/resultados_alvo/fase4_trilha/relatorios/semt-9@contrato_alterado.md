<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-9@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-9@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O produto Picanha ao Alho aparece na seção de destaque, mesmo não estando marcado como destaque no cadastro.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo destaque porque o sinal id: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 2776): regras diff_contra_contrato; antes {"chars": 146}, depois {"chars": 146}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | texto | inteiro |
| destaque | booleano | inteiro |

Trecho podado (hash `2203e279e833f5c4`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": 2}]
```

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| fonte_formato_valido | `[tipo_divergente]` | confere | {"ids": ["tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-9 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2775 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:36:55 | caso semt-9@contrato_alterado |
| 2776 | 2 | poda | programa | ao_vivo | 2026-11-05T01:36:55 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2777 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:36:55 | poda: escolha json/lista; id:tipo_diferente, destaque:tipo_diferente; divergência não |
| 2778 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:36:55 | 3 de 39 verbetes entregues |
| 2779 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:36:55 | recuperacao: escolha entidade-produto,contrato-produto,tipo_divergente; divergência não |
| 2781 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:36:55 | {"etapa": "diagnostico", "sha": "54930a822a2e26f7", "prompt_sha256": "54930a822a2e", "chars": 3556, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2782 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:36:55 | diagnostico: 37,8 s |
| 2783 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:36:55 | causa_raiz: `tipo_divergente` |
| 2784 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:36:55 | campo: `destaque` |
| 2785 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:36:55 | impacto: `O produto Picanha ao Alho aparece na seção de destaque, mesmo não estando marcado como destaque no cadastro.` |
| 2786 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:36:55 | fonte: `[tipo_divergente]` |
| 2787 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:36:55 | fonte_citada: `tipo_divergente` |
| 2788 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:55 | quatro_linhas_presentes: confere |
| 2789 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:55 | rotulo_no_conjunto: confere |
| 2790 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:55 | fonte_existe_na_biblioteca: confere |
| 2791 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:55 | fonte_estava_no_contexto: confere |
| 2792 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:55 | campo_existe_no_caso: confere |
| 2793 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:55 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2794 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:55 | notas_nos_verbetes_citados: informativo |
| 2795 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:55 | impacto: nao_verificavel |
| 2796 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:55 | fonte_formato_valido: confere |
| 2797 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:36:55 | fonte_contem_termo_da_causa: confere |
| 2798 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:36:55 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 2777, `poda`: escolha `json/lista; id:tipo_diferente, destaque:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 2776 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, destaque (gen_ai: plan)
- evento 2779, `recuperacao`: escolha `entidade-produto,contrato-produto,tipo_divergente`; resultado verbetes_entregues; evidência: evento 2778 (verbete_entregue, entidade-produto), evento 2778 (verbete_entregue, contrato-produto), evento 2778 (verbete_entregue, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: retrieval)
- evento 2798, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 2776 (sinal_em_codigo), evento 2778 (verbete_entregue, entidade-produto), evento 2778 (verbete_entregue, contrato-produto), evento 2778 (verbete_entregue, tipo_divergente), evento 2782 (resposta), evento 2787 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2775 a 2798 da trilha; hash dos eventos deste caso: `69f247d899c2ebb1`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
