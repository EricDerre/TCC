<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-1@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-1@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,93)

**IMPACTO (declarado):** `A ordenação por preço fica errada, com 'R$ 9,90' aparecendo depois de 'R$ 89,90'.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal id: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes entidade-produto, tipo_divergente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,05. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 556): regras diff_contra_contrato; antes {"chars": 152}, depois {"chars": 152}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | texto | inteiro |
| preco | numero | texto |

Trecho podado (hash `20cdbc76d4a473bf`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": "89.90", "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

tipo_divergente e não formato_de_data_divergente: a escolha tem probabilidade 0,93 contra 0,05; verbete(s) na evidência: entidade-produto, tipo_divergente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,93 | sim |
| formato_de_data_divergente | 0,05 |  |
| valor_fora_do_dominio | 0,02 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| fonte_formato_valido | `[tipo_divergente]` | confere | {"ids": ["tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-1 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 555 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:31:24 | caso semt-1@contrato_alterado |
| 556 | 2 | poda | programa | ao_vivo | 2026-11-04T23:31:24 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato |
| 557 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:31:24 | poda: escolha json/lista; id:tipo_diferente, preco:tipo_diferente; divergência não |
| 558 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:31:24 | 3 de 39 verbetes entregues |
| 559 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:31:24 | recuperacao: escolha entidade-produto,tipo_divergente,contrato-produto; divergência não |
| 561 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:31:24 | {"etapa": "diagnostico", "sha": "ae7864f108eb1ea5", "prompt_sha256": "ae7864f108eb", "chars": 3558, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 562 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:31:24 | diagnostico: 40,6 s |
| 563 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:31:24 | causa_raiz: `tipo_divergente` |
| 564 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:31:24 | campo: `preco` |
| 565 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:31:24 | impacto: `A ordenação por preço fica errada, com 'R$ 9,90' aparecendo depois de 'R$ 89,90'.` |
| 566 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:31:24 | fonte: `[tipo_divergente]` |
| 567 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:31:24 | fonte_citada: `tipo_divergente` |
| 568 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:24 | quatro_linhas_presentes: confere |
| 569 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:24 | rotulo_no_conjunto: confere |
| 570 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:24 | fonte_existe_na_biblioteca: confere |
| 571 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:24 | fonte_estava_no_contexto: confere |
| 572 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:24 | campo_existe_no_caso: confere |
| 573 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:24 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 574 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:24 | notas_nos_verbetes_citados: informativo |
| 575 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:24 | impacto: nao_verificavel |
| 576 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:24 | fonte_formato_valido: confere |
| 577 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:31:24 | fonte_contem_termo_da_causa: confere |
| 578 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:31:24 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 557, `poda`: escolha `json/lista; id:tipo_diferente, preco:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 556 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, preco (gen_ai: plan)
- evento 559, `recuperacao`: escolha `entidade-produto,tipo_divergente,contrato-produto`; resultado verbetes_entregues; evidência: evento 558 (verbete_entregue, entidade-produto), evento 558 (verbete_entregue, tipo_divergente), evento 558 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, contrato-produto (gen_ai: retrieval)
- evento 578, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 556 (sinal_em_codigo), evento 558 (verbete_entregue, entidade-produto), evento 558 (verbete_entregue, tipo_divergente), evento 558 (verbete_entregue, contrato-produto), evento 562 (resposta), evento 567 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 555 a 578 da trilha; hash dos eventos deste caso: `8b0fdfec88050c9a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
