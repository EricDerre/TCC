<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-14@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-14@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `formato_de_data_divergente` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,80) · **CONFLITO**: nenhum verbete entregue trata da causa respondida formato_de_data_divergente

**IMPACTO (declarado):** `O ícone de imagem quebrada indica que o formato da URL da imagem está incorreto ou inválido.`

Justificativa (gerada por molde): O agente respondeu formato_de_data_divergente no campo imagem porque o sinal imagem: esperado imagem, recebido imagem_url está presente na resposta HTTP e os verbetes entidade-produto, chave_de_juncao_errada, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,04. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida formato_de_data_divergente. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,80); trate como hipótese e confira o campo imagem antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 2518): regras diff_contra_contrato; antes {"chars": 153}, depois {"chars": 153}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | imagem | imagem_url |

Trecho podado (hash `e968e16fdb341a27`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem_url": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

formato_de_data_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 0,80 contra 0,04; verbete(s) na evidência: entidade-produto, chave_de_juncao_errada, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| formato_de_data_divergente | 0,80 | sim |
| valor_fora_do_dominio | 0,04 |  |
| chave_de_juncao_errada | 0,03 |  |
| escala_ou_unidade_errada | 0,02 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| tipo_divergente | 0,01 |  |
| nulo_inesperado | 0,01 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| erro_interno_do_servidor | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| dado_desatualizado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado] [chave_de_juncao_errada]`; verbetes citados: `campo_renomeado`, `chave_de_juncao_errada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado existe na biblioteca | `chave_de_juncao_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `entidade-produto`, `chave_de_juncao_errada`, `campo_renomeado` |
| O verbete citado estava no contexto entregue ao modelo | `chave_de_juncao_errada` | confere | contexto: `entidade-produto`, `chave_de_juncao_errada`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[campo_renomeado] [chave_de_juncao_errada]` | confere | {"ids": ["campo_renomeado", "chave_de_juncao_errada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_renomeado` | **não confere** | {"termo": "formato_de_data_divergente"} |
| fonte_contem_termo_da_causa | `chave_de_juncao_errada` | **não confere** | {"termo": "formato_de_data_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-14 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2517 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:26:00 | caso sin-14@verbete_trocado |
| 2518 | 2 | poda | programa | ao_vivo | 2026-11-05T01:26:00 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2519 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:26:00 | poda: escolha json/lista; imagem:renomeado; divergência não |
| 2520 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:26:00 | 3 de 39 verbetes entregues |
| 2521 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:26:00 | recuperacao: escolha entidade-produto,chave_de_juncao_errada,campo_renomeado; divergência não |
| 2522 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:26:00 | {"etapa": "diagnostico", "sha": "ee8d71caf8221a8f", "prompt_sha256": "ee8d71caf822", "chars": 4046, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2524 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:26:00 | diagnostico: 17,6 s |
| 2525 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:26:00 | causa_raiz: `formato_de_data_divergente` |
| 2526 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:26:00 | campo: `nenhum` |
| 2527 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:26:00 | impacto: `O ícone de imagem quebrada indica que o formato da URL da imagem está incorreto ou inválido.` |
| 2528 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:26:00 | fonte: `[campo_renomeado] [chave_de_juncao_errada]` |
| 2529 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:26:00 | fonte_citada: `campo_renomeado` |
| 2530 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T01:26:00 | fonte_citada: `chave_de_juncao_errada` |
| 2531 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | quatro_linhas_presentes: confere |
| 2532 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | rotulo_no_conjunto: confere |
| 2533 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | fonte_existe_na_biblioteca: confere |
| 2534 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | fonte_existe_na_biblioteca: confere |
| 2535 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | fonte_estava_no_contexto: confere |
| 2536 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | fonte_estava_no_contexto: confere |
| 2537 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | campo_existe_no_caso: nao_se_aplica |
| 2538 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2539 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | notas_nos_verbetes_citados: informativo |
| 2540 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | impacto: nao_verificavel |
| 2541 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | fonte_formato_valido: confere |
| 2542 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | fonte_contem_termo_da_causa: nao_confere |
| 2543 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:00 | fonte_contem_termo_da_causa: nao_confere |
| 2544 | 27 | decisao | programa | ao_vivo | 2026-11-05T01:26:00 | diagnostico: escolha formato_de_data_divergente; divergência sim |

</details>

Nós de decisão:

- evento 2519, `poda`: escolha `json/lista; imagem:renomeado`; resultado sinais_em_codigo; evidência: evento 2518 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: imagem (gen_ai: plan)
- evento 2521, `recuperacao`: escolha `entidade-produto,chave_de_juncao_errada,campo_renomeado`; resultado verbetes_entregues; evidência: evento 2520 (verbete_entregue, entidade-produto), evento 2520 (verbete_entregue, chave_de_juncao_errada), evento 2520 (verbete_entregue, campo_renomeado); divergência: não; falha: nenhuma; prov.used: entidade-produto, chave_de_juncao_errada, campo_renomeado (gen_ai: retrieval)
- evento 2544, `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido; evidência: evento 2518 (sinal_em_codigo), evento 2520 (verbete_entregue, entidade-produto), evento 2520 (verbete_entregue, chave_de_juncao_errada), evento 2520 (verbete_entregue, campo_renomeado), evento 2524 (resposta), evento 2529 (verbete_citado, campo_renomeado), evento 2530 (verbete_citado, chave_de_juncao_errada); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, chave_de_juncao_errada, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2517 a 2544 da trilha; hash dos eventos deste caso: `f940965e5bf86c09`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
