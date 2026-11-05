<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-1@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-1@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `id` · selo de probabilidade: **medio** (p = 0,95)

**IMPACTO (declarado):** `O usuário vê uma lista vazia, enquanto espera um objeto com detalhes do produto.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo id porque o sinal esperado JSON completo e válido, recebido corpo truncado está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,03 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 70): regras diff_contra_contrato; antes {"chars": 69}, depois {"chars": 69}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo truncado |

Trecho podado (hash `cabbea3716c8b731`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "tipo": "Carnes", "preco": 89.9
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não corpo_nao_e_json: a escolha tem probabilidade 0,95 contra 0,03; verbete(s) na evidência: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,95 | sim |
| corpo_nao_e_json | 0,03 |  |
| corpo_vazio | 0,03 |  |
| resposta_truncada | 0,02 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [colecao_no_lugar_de_objeto]`; verbetes citados: `contrato-produto`, `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto`, `colecao_no_lugar_de_objeto` |
| fonte_formato_valido | `[contrato-produto], [colecao_no_lugar_de_objeto]` | confere | {"ids": ["contrato-produto", "colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-1 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 69 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:05:57 | caso lex-1@verbete_trocado |
| 70 | 2 | poda | programa | ao_vivo | 2026-11-04T23:05:57 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 71 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:05:57 | poda: escolha truncado; divergência não |
| 72 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:05:57 | 3 de 39 verbetes entregues |
| 73 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:05:57 | recuperacao: escolha entidade-produto,contrato-produto,colecao_no_lugar_de_objeto; divergência não |
| 74 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:05:57 | {"etapa": "diagnostico", "sha": "37097b9bcb72744d", "prompt_sha256": "37097b9bcb72", "chars": 3697, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 75 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:05:57 | diagnostico: 16,7 s |
| 76 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:05:57 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 77 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:05:57 | campo: `id` |
| 78 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:05:57 | impacto: `O usuário vê uma lista vazia, enquanto espera um objeto com detalhes do produto.` |
| 79 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:05:57 | fonte: `[contrato-produto], [colecao_no_lugar_de_objeto]` |
| 80 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:05:57 | fonte_citada: `contrato-produto` |
| 81 | 13 | declaracao | modelo | ao_vivo | 2026-11-04T23:05:57 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 82 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | quatro_linhas_presentes: confere |
| 83 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | rotulo_no_conjunto: confere |
| 84 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | fonte_existe_na_biblioteca: confere |
| 85 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | fonte_existe_na_biblioteca: confere |
| 86 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | fonte_estava_no_contexto: confere |
| 87 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | fonte_estava_no_contexto: confere |
| 88 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | campo_existe_no_caso: confere |
| 89 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 90 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | notas_nos_verbetes_citados: informativo |
| 91 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | impacto: nao_verificavel |
| 92 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | fonte_formato_valido: confere |
| 93 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | fonte_contem_termo_da_causa: nao_confere |
| 94 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T23:05:57 | fonte_contem_termo_da_causa: confere |
| 95 | 27 | decisao | programa | ao_vivo | 2026-11-04T23:05:57 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 71, `poda`: escolha `truncado`; resultado sinais_em_codigo; evidência: evento 70 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 73, `recuperacao`: escolha `entidade-produto,contrato-produto,colecao_no_lugar_de_objeto`; resultado verbetes_entregues; evidência: evento 72 (verbete_entregue, entidade-produto), evento 72 (verbete_entregue, contrato-produto), evento 72 (verbete_entregue, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: retrieval)
- evento 95, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 70 (sinal_em_codigo), evento 72 (verbete_entregue, entidade-produto), evento 72 (verbete_entregue, contrato-produto), evento 72 (verbete_entregue, colecao_no_lugar_de_objeto), evento 75 (resposta), evento 80 (verbete_citado, contrato-produto), evento 81 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 69 a 95 da trilha; hash dos eventos deste caso: `53d71803285f7e22`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
