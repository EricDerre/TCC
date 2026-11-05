<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-8@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-8@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,42)

**IMPACTO (declarado):** `O usuário vê 'R$ 0,00' em vez do preço correto de R$ 89,90.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal preco: esperado numero, recebido nulo está presente na resposta HTTP e os verbetes entidade-produto, tipo_divergente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,44. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,42); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 2637): regras diff_contra_contrato; antes {"chars": 149}, depois {"chars": 149}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | nulo |

Trecho podado (hash `c36e9bb22382f8e9`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": null, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 0,42 contra 0,44; verbete(s) na evidência: entidade-produto, tipo_divergente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 0,44 |  |
| tipo_divergente | 0,42 | sim |
| resposta_truncada | 0,05 |  |
| formato_de_data_divergente | 0,03 |  |
| nulo_inesperado | 0,03 |  |
| colecao_no_lugar_de_objeto | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| escala_ou_unidade_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-8 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2636 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:31:11 | caso semt-8@verbete_trocado |
| 2637 | 2 | poda | programa | ao_vivo | 2026-11-05T01:31:11 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2638 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:31:11 | poda: escolha json/lista; preco:nulo_inesperado; divergência não |
| 2639 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:31:11 | 3 de 39 verbetes entregues |
| 2640 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:31:11 | recuperacao: escolha entidade-produto,tipo_divergente,contrato-produto; divergência não |
| 2641 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:31:11 | {"etapa": "diagnostico", "sha": "9779b1ff8527ef5c", "prompt_sha256": "9779b1ff8527", "chars": 3540, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2643 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:31:11 | diagnostico: 15,6 s |
| 2644 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:31:11 | causa_raiz: `tipo_divergente` |
| 2645 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:31:11 | campo: `preco` |
| 2646 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:31:11 | impacto: `O usuário vê 'R$ 0,00' em vez do preço correto de R$ 89,90.` |
| 2647 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:31:11 | fonte: `[tipo_divergente]` |
| 2648 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:31:11 | fonte_citada: `tipo_divergente` |
| 2649 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:11 | quatro_linhas_presentes: confere |
| 2650 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:11 | rotulo_no_conjunto: confere |
| 2651 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:11 | fonte_existe_na_biblioteca: confere |
| 2652 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:11 | fonte_estava_no_contexto: confere |
| 2653 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:11 | campo_existe_no_caso: confere |
| 2654 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:11 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2655 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:11 | notas_nos_verbetes_citados: informativo |
| 2656 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:11 | impacto: nao_verificavel |
| 2657 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:11 | fonte_formato_valido: confere |
| 2658 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:11 | fonte_contem_termo_da_causa: confere |
| 2659 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:31:11 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 2638, `poda`: escolha `json/lista; preco:nulo_inesperado`; resultado sinais_em_codigo; evidência: evento 2637 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: preco (gen_ai: plan)
- evento 2640, `recuperacao`: escolha `entidade-produto,tipo_divergente,contrato-produto`; resultado verbetes_entregues; evidência: evento 2639 (verbete_entregue, entidade-produto), evento 2639 (verbete_entregue, tipo_divergente), evento 2639 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, contrato-produto (gen_ai: retrieval)
- evento 2659, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 2637 (sinal_em_codigo), evento 2639 (verbete_entregue, entidade-produto), evento 2639 (verbete_entregue, tipo_divergente), evento 2639 (verbete_entregue, contrato-produto), evento 2643 (resposta), evento 2648 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2636 a 2659 da trilha; hash dos eventos deste caso: `e438cc7334300a68`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
