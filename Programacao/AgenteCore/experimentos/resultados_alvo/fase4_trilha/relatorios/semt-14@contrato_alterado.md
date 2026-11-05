<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-14@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-14@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `tipo` · selo de probabilidade: **baixo** (p = 0,82)

**IMPACTO (declarado):** `O filtro por categoria não exibe corretamente os produtos, pois alguns tipos estão ausentes na resposta.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo tipo porque o sinal id: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,17. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,82); trate como hipótese e confira o campo tipo antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 2899): regras diff_contra_contrato; antes {"chars": 272}, depois {"chars": 272}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | texto | inteiro |

Trecho podado (hash `10463dd6558b8e48`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 8, "nome": "Agua Mineral", "resumo": "500ml", "tipo": null, "preco": 6.0, "imagem": "agua.png", "destaque": false}]
```

## 3. Contraste com a segunda causa

nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 0,82 contra 0,17; verbete(s) na evidência: entidade-produto, contrato-produto, nulo_inesperado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,82 | sim |
| tipo_divergente | 0,17 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| valor_fora_do_dominio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [nulo_inesperado]`; verbetes citados: `contrato-produto`, `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| fonte_formato_valido | `[contrato-produto], [nulo_inesperado]` | confere | {"ids": ["contrato-produto", "nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "nulo_inesperado"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-14 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2898 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:42:31 | caso semt-14@contrato_alterado |
| 2899 | 2 | poda | programa | ao_vivo | 2026-11-05T01:42:31 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2900 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:42:31 | poda: escolha json/lista; id:tipo_diferente; divergência não |
| 2901 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:42:31 | 3 de 39 verbetes entregues |
| 2902 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:42:31 | recuperacao: escolha entidade-produto,contrato-produto,nulo_inesperado; divergência não |
| 2904 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:42:31 | {"etapa": "diagnostico", "sha": "93b7292fb85b5719", "prompt_sha256": "93b7292fb85b", "chars": 3493, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2905 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:42:31 | diagnostico: 40,4 s |
| 2906 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:42:31 | causa_raiz: `nulo_inesperado` |
| 2907 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:42:31 | campo: `tipo` |
| 2908 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:42:31 | impacto: `O filtro por categoria não exibe corretamente os produtos, pois alguns tipos estão ausentes na resposta.` |
| 2909 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:42:31 | fonte: `[contrato-produto], [nulo_inesperado]` |
| 2910 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:42:31 | fonte_citada: `contrato-produto` |
| 2911 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T01:42:31 | fonte_citada: `nulo_inesperado` |
| 2912 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | quatro_linhas_presentes: confere |
| 2913 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | rotulo_no_conjunto: confere |
| 2914 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | fonte_existe_na_biblioteca: confere |
| 2915 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | fonte_existe_na_biblioteca: confere |
| 2916 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | fonte_estava_no_contexto: confere |
| 2917 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | fonte_estava_no_contexto: confere |
| 2918 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | campo_existe_no_caso: confere |
| 2919 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2920 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | notas_nos_verbetes_citados: informativo |
| 2921 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | impacto: nao_verificavel |
| 2922 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | fonte_formato_valido: confere |
| 2923 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | fonte_contem_termo_da_causa: nao_confere |
| 2924 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:31 | fonte_contem_termo_da_causa: confere |
| 2925 | 27 | decisao | programa | ao_vivo | 2026-11-05T01:42:31 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 2900, `poda`: escolha `json/lista; id:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 2899 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id (gen_ai: plan)
- evento 2902, `recuperacao`: escolha `entidade-produto,contrato-produto,nulo_inesperado`; resultado verbetes_entregues; evidência: evento 2901 (verbete_entregue, entidade-produto), evento 2901 (verbete_entregue, contrato-produto), evento 2901 (verbete_entregue, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, nulo_inesperado (gen_ai: retrieval)
- evento 2925, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 2899 (sinal_em_codigo), evento 2901 (verbete_entregue, entidade-produto), evento 2901 (verbete_entregue, contrato-produto), evento 2901 (verbete_entregue, nulo_inesperado), evento 2905 (resposta), evento 2910 (verbete_citado, contrato-produto), evento 2911 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, nulo_inesperado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2898 a 2925 da trilha; hash dos eventos deste caso: `374c8db41babd32a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
