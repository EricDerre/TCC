<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-14@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-14@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,92)

**IMPACTO (declarado):** `O filtro por categoria não exibe produtos cujo tipo é nulo, resultando na exclusão acidental de alguns itens do cadastro.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo tipo porque os verbetes entidade-produto, tipo_divergente, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,08. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 2874): regras diff_contra_contrato; antes {"chars": 272}, depois {"chars": 272}.

Trecho podado (hash `10463dd6558b8e48`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 8, "nome": "Agua Mineral", "resumo": "500ml", "tipo": null, "preco": 6.0, "imagem": "agua.png", "destaque": false}]
```

## 3. Contraste com a segunda causa

nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 0,92 contra 0,08; verbete(s) na evidência: entidade-produto, tipo_divergente, nulo_inesperado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,92 | sim |
| tipo_divergente | 0,08 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `entidade-produto`, `tipo_divergente`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"ids": ["nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-14 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2873 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:42:11 | caso semt-14@verbete_trocado |
| 2874 | 2 | poda | programa | ao_vivo | 2026-11-05T01:42:11 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2875 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:42:11 | poda: escolha json/lista; sem diferença; divergência não |
| 2876 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:42:11 | 3 de 39 verbetes entregues |
| 2877 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:42:11 | recuperacao: escolha entidade-produto,tipo_divergente,nulo_inesperado; divergência não |
| 2878 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:42:11 | {"etapa": "diagnostico", "sha": "af92eefce33bb4c7", "prompt_sha256": "af92eefce33b", "chars": 3525, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2880 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:42:11 | diagnostico: 16,0 s |
| 2881 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:42:11 | causa_raiz: `nulo_inesperado` |
| 2882 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:42:11 | campo: `tipo` |
| 2883 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:42:11 | impacto: `O filtro por categoria não exibe produtos cujo tipo é nulo, resultando na exclusão acidental de alguns itens do cadastro.` |
| 2884 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:42:11 | fonte: `[nulo_inesperado]` |
| 2885 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:42:11 | fonte_citada: `nulo_inesperado` |
| 2886 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:11 | quatro_linhas_presentes: confere |
| 2887 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:11 | rotulo_no_conjunto: confere |
| 2888 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:11 | fonte_existe_na_biblioteca: confere |
| 2889 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:11 | fonte_estava_no_contexto: confere |
| 2890 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:11 | campo_existe_no_caso: confere |
| 2891 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:11 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2892 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:11 | notas_nos_verbetes_citados: informativo |
| 2893 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:11 | impacto: nao_verificavel |
| 2894 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:11 | fonte_formato_valido: confere |
| 2895 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:42:11 | fonte_contem_termo_da_causa: confere |
| 2896 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:42:11 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 2875, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 2874 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 2877, `recuperacao`: escolha `entidade-produto,tipo_divergente,nulo_inesperado`; resultado verbetes_entregues; evidência: evento 2876 (verbete_entregue, entidade-produto), evento 2876 (verbete_entregue, tipo_divergente), evento 2876 (verbete_entregue, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, nulo_inesperado (gen_ai: retrieval)
- evento 2896, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 2876 (verbete_entregue, entidade-produto), evento 2876 (verbete_entregue, tipo_divergente), evento 2876 (verbete_entregue, nulo_inesperado), evento 2880 (resposta), evento 2885 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, nulo_inesperado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2873 a 2896 da trilha; hash dos eventos deste caso: `4b14fc46da3954ef`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
