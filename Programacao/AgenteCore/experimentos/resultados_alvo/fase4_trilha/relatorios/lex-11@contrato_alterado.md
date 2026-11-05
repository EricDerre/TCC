<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-11@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-11@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `Alguns nomes de produtos são exibidos corrompidos, enquanto outros aparecem corretos.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo id porque o sinal id: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, codificacao_incorreta estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 2091): regras diff_contra_contrato; antes {"chars": 154}, depois {"chars": 154}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | texto | inteiro |

Trecho podado (hash `d4b4394eaa720f08`):

```text
[{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e acucar", "tipo": "Sobremesas", "preco": 14.9, "imagem": "abacaxi.jpg", "destaque": false}]
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, codificacao_incorreta

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[codificacao_incorreta]`; verbetes citados: `codificacao_incorreta`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `codificacao_incorreta` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `codificacao_incorreta` | confere | contexto: `entidade-produto`, `contrato-produto`, `codificacao_incorreta` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | confere | verbetes: `codificacao_incorreta` |
| fonte_formato_valido | `[codificacao_incorreta]` | confere | {"ids": ["codificacao_incorreta"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `codificacao_incorreta` | confere | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-11 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2090 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:01:46 | caso lex-11@contrato_alterado |
| 2091 | 2 | poda | programa | ao_vivo | 2026-11-05T01:01:46 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2092 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:01:46 | poda: escolha json/lista; id:tipo_diferente; divergência não |
| 2093 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:01:46 | 3 de 39 verbetes entregues |
| 2094 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:01:46 | recuperacao: escolha entidade-produto,contrato-produto,codificacao_incorreta; divergência não |
| 2096 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:01:46 | {"etapa": "diagnostico", "sha": "620ac7a34e3c35d8", "prompt_sha256": "620ac7a34e3c", "chars": 3493, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2098 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:01:46 | diagnostico: 50,0 s |
| 2099 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:01:46 | causa_raiz: `codificacao_incorreta` |
| 2100 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:01:46 | campo: `nenhum` |
| 2101 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:01:46 | impacto: `Alguns nomes de produtos são exibidos corrompidos, enquanto outros aparecem corretos.` |
| 2102 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:01:46 | fonte: `[codificacao_incorreta]` |
| 2103 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:01:46 | fonte_citada: `codificacao_incorreta` |
| 2104 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:46 | quatro_linhas_presentes: confere |
| 2105 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:46 | rotulo_no_conjunto: confere |
| 2106 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:46 | fonte_existe_na_biblioteca: confere |
| 2107 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:46 | fonte_estava_no_contexto: confere |
| 2108 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:46 | campo_existe_no_caso: nao_se_aplica |
| 2109 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:46 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2110 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:46 | notas_nos_verbetes_citados: informativo |
| 2111 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:46 | impacto: nao_verificavel |
| 2112 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:46 | fonte_formato_valido: confere |
| 2113 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:46 | fonte_contem_termo_da_causa: confere |
| 2114 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:01:46 | diagnostico: escolha codificacao_incorreta; divergência não |

</details>

Nós de decisão:

- evento 2092, `poda`: escolha `json/lista; id:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 2091 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id (gen_ai: plan)
- evento 2094, `recuperacao`: escolha `entidade-produto,contrato-produto,codificacao_incorreta`; resultado verbetes_entregues; evidência: evento 2093 (verbete_entregue, entidade-produto), evento 2093 (verbete_entregue, contrato-produto), evento 2093 (verbete_entregue, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, codificacao_incorreta (gen_ai: retrieval)
- evento 2114, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 2091 (sinal_em_codigo), evento 2093 (verbete_entregue, entidade-produto), evento 2093 (verbete_entregue, contrato-produto), evento 2093 (verbete_entregue, codificacao_incorreta), evento 2098 (resposta), evento 2103 (verbete_citado, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, codificacao_incorreta (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2090 a 2114 da trilha; hash dos eventos deste caso: `356ebe31c49f90df`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
