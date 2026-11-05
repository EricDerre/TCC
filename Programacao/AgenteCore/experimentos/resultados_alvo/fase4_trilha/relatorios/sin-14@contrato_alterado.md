<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-14@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-14@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `formato_de_data_divergente` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,33) · **CONFLITO**: nenhum verbete entregue trata da causa respondida formato_de_data_divergente

**IMPACTO (declarado):** `O ícone de imagem quebrada indica que há um problema com a formatação da URL da imagem, que é interpretada incorretamente pelo front-end.`

Justificativa (gerada por molde): O agente respondeu formato_de_data_divergente no campo id porque o sinal id: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,38. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida formato_de_data_divergente. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,33); trate como hipótese e confira o campo id antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 2547): regras diff_contra_contrato; antes {"chars": 153}, depois {"chars": 153}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | texto | inteiro |
| imagem | imagem | imagem_url |

Trecho podado (hash `e968e16fdb341a27`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem_url": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

formato_de_data_divergente e não tipo_divergente: a escolha tem probabilidade 0,33 contra 0,38; verbete(s) na evidência: entidade-produto, contrato-produto, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,38 |  |
| formato_de_data_divergente | 0,33 | sim |
| resposta_truncada | 0,10 |  |
| campo_ausente | 0,09 |  |
| campo_renomeado | 0,09 |  |
| colecao_no_lugar_de_objeto | 0,05 |  |
| corpo_nao_e_json | 0,02 |  |
| corpo_vazio | 0,02 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "formato_de_data_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-14 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2546 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:26:22 | caso sin-14@contrato_alterado |
| 2547 | 2 | poda | programa | ao_vivo | 2026-11-05T01:26:22 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2548 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:26:22 | poda: escolha json/lista; id:tipo_diferente, imagem:renomeado; divergência não |
| 2549 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:26:22 | 3 de 39 verbetes entregues |
| 2550 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:26:22 | recuperacao: escolha entidade-produto,contrato-produto,campo_renomeado; divergência não |
| 2552 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:26:22 | {"etapa": "diagnostico", "sha": "1fe029cd1012c2c4", "prompt_sha256": "1fe029cd1012", "chars": 3586, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2554 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:26:22 | diagnostico: 39,3 s |
| 2555 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:26:22 | causa_raiz: `formato_de_data_divergente` |
| 2556 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:26:22 | campo: `nenhum` |
| 2557 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:26:22 | impacto: `O ícone de imagem quebrada indica que há um problema com a formatação da URL da imagem, que é interpretada incorretamente pelo front-end.` |
| 2558 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:26:22 | fonte: `[contrato-produto]` |
| 2559 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:26:22 | fonte_citada: `contrato-produto` |
| 2560 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:22 | quatro_linhas_presentes: confere |
| 2561 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:22 | rotulo_no_conjunto: confere |
| 2562 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:22 | fonte_existe_na_biblioteca: confere |
| 2563 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:22 | fonte_estava_no_contexto: confere |
| 2564 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:22 | campo_existe_no_caso: nao_se_aplica |
| 2565 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:22 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2566 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:22 | notas_nos_verbetes_citados: informativo |
| 2567 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:22 | impacto: nao_verificavel |
| 2568 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:22 | fonte_formato_valido: confere |
| 2569 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:26:22 | fonte_contem_termo_da_causa: nao_confere |
| 2570 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:26:22 | diagnostico: escolha formato_de_data_divergente; divergência sim |

</details>

Nós de decisão:

- evento 2548, `poda`: escolha `json/lista; id:tipo_diferente, imagem:renomeado`; resultado sinais_em_codigo; evidência: evento 2547 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, imagem (gen_ai: plan)
- evento 2550, `recuperacao`: escolha `entidade-produto,contrato-produto,campo_renomeado`; resultado verbetes_entregues; evidência: evento 2549 (verbete_entregue, entidade-produto), evento 2549 (verbete_entregue, contrato-produto), evento 2549 (verbete_entregue, campo_renomeado); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_renomeado (gen_ai: retrieval)
- evento 2570, `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido; evidência: evento 2547 (sinal_em_codigo), evento 2549 (verbete_entregue, entidade-produto), evento 2549 (verbete_entregue, contrato-produto), evento 2549 (verbete_entregue, campo_renomeado), evento 2554 (resposta), evento 2559 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2546 a 2570 da trilha; hash dos eventos deste caso: `889af35d60306c78`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
