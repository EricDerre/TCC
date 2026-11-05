<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-3@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-3@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `imagem` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não vê a imagem do produto, resultando em cartões sem foto.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo imagem porque o sinal imagem: esperado texto|nulo, recebido None está presente na resposta HTTP e os verbetes entidade-produto, chave_de_juncao_errada, campo_ausente estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1547): regras diff_contra_contrato; antes {"chars": 119}, depois {"chars": 119}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | texto\|nulo |  |

Trecho podado (hash `55555e369bef5da7`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "destaque": true}]
```

## 3. Contraste com a segunda causa

campo_ausente e não formato_de_data_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, chave_de_juncao_errada, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 1,00 | sim |
| formato_de_data_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| nulo_inesperado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente]`; verbetes citados: `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `chave_de_juncao_errada`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `campo_ausente` |
| fonte_formato_valido | `[campo_ausente]` | confere | {"ids": ["campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-3 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1546 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:32:13 | caso efe-3@verbete_trocado |
| 1547 | 2 | poda | programa | ao_vivo | 2026-11-05T00:32:13 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1548 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:32:13 | poda: escolha json/lista; imagem:ausente; divergência não |
| 1549 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:32:13 | 3 de 39 verbetes entregues |
| 1550 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:32:13 | recuperacao: escolha entidade-produto,chave_de_juncao_errada,campo_ausente; divergência não |
| 1551 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:32:13 | {"etapa": "diagnostico", "sha": "38f9707140222f37", "prompt_sha256": "38f970714022", "chars": 3877, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1552 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:32:13 | diagnostico: 13,1 s |
| 1553 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:32:13 | causa_raiz: `campo_ausente` |
| 1554 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:32:13 | campo: `imagem` |
| 1555 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:32:13 | impacto: `O usuário não vê a imagem do produto, resultando em cartões sem foto.` |
| 1556 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:32:13 | fonte: `[campo_ausente]` |
| 1557 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:32:13 | fonte_citada: `campo_ausente` |
| 1558 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:13 | quatro_linhas_presentes: confere |
| 1559 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:13 | rotulo_no_conjunto: confere |
| 1560 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:13 | fonte_existe_na_biblioteca: confere |
| 1561 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:13 | fonte_estava_no_contexto: confere |
| 1562 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:13 | campo_existe_no_caso: confere |
| 1563 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:13 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1564 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:13 | notas_nos_verbetes_citados: informativo |
| 1565 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:13 | impacto: nao_verificavel |
| 1566 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:13 | fonte_formato_valido: confere |
| 1567 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:13 | fonte_contem_termo_da_causa: confere |
| 1568 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:32:13 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 1548, `poda`: escolha `json/lista; imagem:ausente`; resultado sinais_em_codigo; evidência: evento 1547 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: imagem (gen_ai: plan)
- evento 1550, `recuperacao`: escolha `entidade-produto,chave_de_juncao_errada,campo_ausente`; resultado verbetes_entregues; evidência: evento 1549 (verbete_entregue, entidade-produto), evento 1549 (verbete_entregue, chave_de_juncao_errada), evento 1549 (verbete_entregue, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, chave_de_juncao_errada, campo_ausente (gen_ai: retrieval)
- evento 1568, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 1547 (sinal_em_codigo), evento 1549 (verbete_entregue, entidade-produto), evento 1549 (verbete_entregue, chave_de_juncao_errada), evento 1549 (verbete_entregue, campo_ausente), evento 1552 (resposta), evento 1557 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, chave_de_juncao_errada, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1546 a 1568 da trilha; hash dos eventos deste caso: `59fcb6fbaa759ab8`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
