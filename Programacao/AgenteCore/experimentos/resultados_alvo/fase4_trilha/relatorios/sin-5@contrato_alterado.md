<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-5@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-5@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `id` · selo de probabilidade: **baixo** (p = 0,69)

**IMPACTO (declarado):** `A interface exibe descrições inconsistentemente, mostrando-as para alguns produtos mas não para outros, devido à estrutura da resposta JSON não correspondendo ao esperado.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo id porque o sinal id: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,27. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,69); trate como hipótese e confira o campo id antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 429): regras diff_contra_contrato; antes {"chars": 260}, depois {"chars": 260}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | texto | inteiro |

Trecho podado (hash `ab8ef2dc7ba007c9`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Fraldinha", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}]
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não tipo_divergente: a escolha tem probabilidade 0,69 contra 0,27; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,69 | sim |
| tipo_divergente | 0,27 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [tipo_divergente]`; verbetes citados: `contrato-produto`, `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto] [tipo_divergente]` | confere | {"ids": ["contrato-produto", "tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-5 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 428 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:25:01 | caso sin-5@contrato_alterado |
| 429 | 2 | poda | programa | ao_vivo | 2026-11-04T23:25:01 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 430 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:25:01 | poda: escolha json/lista; id:tipo_diferente; divergência não |
| 431 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:25:01 | 3 de 39 verbetes entregues |
| 432 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:25:01 | recuperacao: escolha entidade-produto,contrato-produto,tipo_divergente; divergência não |
| 434 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:25:01 | {"etapa": "diagnostico", "sha": "da5a22ee2151e347", "prompt_sha256": "da5a22ee2151", "chars": 3661, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 436 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:25:01 | diagnostico: 45,6 s |
| 437 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:25:01 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 438 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:25:01 | campo: `id` |
| 439 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:25:01 | impacto: `A interface exibe descrições inconsistentemente, mostrando-as para alguns produtos mas não para outros, devido à estrutura da resposta JSON não correspondendo ao esperado.` |
| 440 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:25:01 | fonte: `[contrato-produto] [tipo_divergente]` |
| 441 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:25:01 | fonte_citada: `contrato-produto` |
| 442 | 13 | declaracao | modelo | ao_vivo | 2026-11-04T23:25:01 | fonte_citada: `tipo_divergente` |
| 443 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | quatro_linhas_presentes: confere |
| 444 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | rotulo_no_conjunto: confere |
| 445 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | fonte_existe_na_biblioteca: confere |
| 446 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | fonte_existe_na_biblioteca: confere |
| 447 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | fonte_estava_no_contexto: confere |
| 448 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | fonte_estava_no_contexto: confere |
| 449 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | campo_existe_no_caso: confere |
| 450 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 451 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | notas_nos_verbetes_citados: informativo |
| 452 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | impacto: nao_verificavel |
| 453 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | fonte_formato_valido: confere |
| 454 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | fonte_contem_termo_da_causa: nao_confere |
| 455 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T23:25:01 | fonte_contem_termo_da_causa: nao_confere |
| 456 | 27 | decisao | programa | ao_vivo | 2026-11-04T23:25:01 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 430, `poda`: escolha `json/lista; id:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 429 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id (gen_ai: plan)
- evento 432, `recuperacao`: escolha `entidade-produto,contrato-produto,tipo_divergente`; resultado verbetes_entregues; evidência: evento 431 (verbete_entregue, entidade-produto), evento 431 (verbete_entregue, contrato-produto), evento 431 (verbete_entregue, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: retrieval)
- evento 456, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 429 (sinal_em_codigo), evento 431 (verbete_entregue, entidade-produto), evento 431 (verbete_entregue, contrato-produto), evento 431 (verbete_entregue, tipo_divergente), evento 436 (resposta), evento 441 (verbete_citado, contrato-produto), evento 442 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 428 a 456 da trilha; hash dos eventos deste caso: `534edd87a4de7477`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
