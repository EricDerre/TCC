<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-5@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-5@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `resumo` · selo de probabilidade: **baixo** (p = 0,74)

**IMPACTO (declarado):** `A ausência do campo "resumo" em alguns produtos causa inconsistência na exibição de descrições, resultando em cartões sem descrição.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo resumo porque os verbetes entidade-produto, campo_ausente, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,26. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,74); trate como hipótese e confira o campo resumo antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 404): regras diff_contra_contrato; antes {"chars": 260}, depois {"chars": 260}.

Trecho podado (hash `ab8ef2dc7ba007c9`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Fraldinha", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}]
```

## 3. Contraste com a segunda causa

campo_ausente e não tipo_divergente: a escolha tem probabilidade 0,74 contra 0,26; verbete(s) na evidência: entidade-produto, campo_ausente, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,74 | sim |
| tipo_divergente | 0,26 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente]`; verbetes citados: `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `campo_ausente`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `campo_ausente` |
| fonte_formato_valido | `[campo_ausente]` | confere | {"ids": ["campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `resumo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-5 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 403 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:24:40 | caso sin-5@verbete_trocado |
| 404 | 2 | poda | programa | ao_vivo | 2026-11-04T23:24:40 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 405 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:24:40 | poda: escolha json/lista; sem diferença; divergência não |
| 406 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:24:40 | 3 de 39 verbetes entregues |
| 407 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:24:40 | recuperacao: escolha entidade-produto,campo_ausente,tipo_divergente; divergência não |
| 408 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:24:40 | {"etapa": "diagnostico", "sha": "ed7763be4a09b5c6", "prompt_sha256": "ed7763be4a09", "chars": 3558, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 410 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:24:40 | diagnostico: 16,7 s |
| 411 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:24:40 | causa_raiz: `campo_ausente` |
| 412 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:24:40 | campo: `resumo` |
| 413 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:24:40 | impacto: `A ausência do campo "resumo" em alguns produtos causa inconsistência na exibição de descrições, resultando em cartões sem descrição.` |
| 414 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:24:40 | fonte: `[campo_ausente]` |
| 415 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:24:40 | fonte_citada: `campo_ausente` |
| 416 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:24:40 | quatro_linhas_presentes: confere |
| 417 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:24:40 | rotulo_no_conjunto: confere |
| 418 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:24:40 | fonte_existe_na_biblioteca: confere |
| 419 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:24:40 | fonte_estava_no_contexto: confere |
| 420 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:24:40 | campo_existe_no_caso: confere |
| 421 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:24:40 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 422 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:24:40 | notas_nos_verbetes_citados: informativo |
| 423 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:24:40 | impacto: nao_verificavel |
| 424 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:24:40 | fonte_formato_valido: confere |
| 425 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:24:40 | fonte_contem_termo_da_causa: confere |
| 426 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:24:40 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 405, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 404 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 407, `recuperacao`: escolha `entidade-produto,campo_ausente,tipo_divergente`; resultado verbetes_entregues; evidência: evento 406 (verbete_entregue, entidade-produto), evento 406 (verbete_entregue, campo_ausente), evento 406 (verbete_entregue, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, campo_ausente, tipo_divergente (gen_ai: retrieval)
- evento 426, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 406 (verbete_entregue, entidade-produto), evento 406 (verbete_entregue, campo_ausente), evento 406 (verbete_entregue, tipo_divergente), evento 410 (resposta), evento 415 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, campo_ausente, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 403 a 426 da trilha; hash dos eventos deste caso: `9acb22e5793df10e`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
