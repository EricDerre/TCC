<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-3@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-3@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `imagem` · selo de probabilidade: **baixo** (p = 0,43)

**IMPACTO (declarado):** `Os cartões não exibem a imagem, pois o campo imagem está ausente em todos os objetos retornados.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo imagem porque o sinal id: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,40. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,43); trate como hipótese e confira o campo imagem antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 1571): regras diff_contra_contrato; antes {"chars": 119}, depois {"chars": 119}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | texto | inteiro |
| imagem | texto\|nulo |  |

Trecho podado (hash `55555e369bef5da7`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "destaque": true}]
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não campo_ausente: a escolha tem probabilidade 0,43 contra 0,40; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,43 | sim |
| campo_ausente | 0,40 |  |
| campo_renomeado | 0,40 |  |
| tipo_divergente | 0,08 |  |
| resposta_truncada | 0,06 |  |
| corpo_nao_e_json | 0,02 |  |
| corpo_vazio | 0,02 |  |
| formato_de_data_divergente | 0,01 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [campo_ausente]`; verbetes citados: `contrato-produto`, `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto] [campo_ausente]` | confere | {"ids": ["contrato-produto", "campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |
| fonte_contem_termo_da_causa | `campo_ausente` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-3 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1570 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:32:30 | caso efe-3@contrato_alterado |
| 1571 | 2 | poda | programa | ao_vivo | 2026-11-05T00:32:30 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1572 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:32:30 | poda: escolha json/lista; id:tipo_diferente, imagem:ausente; divergência não |
| 1573 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:32:30 | 3 de 39 verbetes entregues |
| 1574 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:32:30 | recuperacao: escolha entidade-produto,contrato-produto,campo_ausente; divergência não |
| 1576 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:32:30 | {"etapa": "diagnostico", "sha": "f73c1560b2297ca8", "prompt_sha256": "f73c1560b229", "chars": 3417, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1578 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:32:30 | diagnostico: 38,6 s |
| 1579 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:32:30 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 1580 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:32:30 | campo: `imagem` |
| 1581 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:32:30 | impacto: `Os cartões não exibem a imagem, pois o campo imagem está ausente em todos os objetos retornados.` |
| 1582 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:32:30 | fonte: `[contrato-produto] [campo_ausente]` |
| 1583 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:32:30 | fonte_citada: `contrato-produto` |
| 1584 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T00:32:30 | fonte_citada: `campo_ausente` |
| 1585 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | quatro_linhas_presentes: confere |
| 1586 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | rotulo_no_conjunto: confere |
| 1587 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | fonte_existe_na_biblioteca: confere |
| 1588 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | fonte_existe_na_biblioteca: confere |
| 1589 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | fonte_estava_no_contexto: confere |
| 1590 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | fonte_estava_no_contexto: confere |
| 1591 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | campo_existe_no_caso: confere |
| 1592 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1593 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | notas_nos_verbetes_citados: informativo |
| 1594 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | impacto: nao_verificavel |
| 1595 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | fonte_formato_valido: confere |
| 1596 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | fonte_contem_termo_da_causa: nao_confere |
| 1597 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T00:32:30 | fonte_contem_termo_da_causa: nao_confere |
| 1598 | 27 | decisao | programa | ao_vivo | 2026-11-05T00:32:30 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 1572, `poda`: escolha `json/lista; id:tipo_diferente, imagem:ausente`; resultado sinais_em_codigo; evidência: evento 1571 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, imagem (gen_ai: plan)
- evento 1574, `recuperacao`: escolha `entidade-produto,contrato-produto,campo_ausente`; resultado verbetes_entregues; evidência: evento 1573 (verbete_entregue, entidade-produto), evento 1573 (verbete_entregue, contrato-produto), evento 1573 (verbete_entregue, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: retrieval)
- evento 1598, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 1571 (sinal_em_codigo), evento 1573 (verbete_entregue, entidade-produto), evento 1573 (verbete_entregue, contrato-produto), evento 1573 (verbete_entregue, campo_ausente), evento 1578 (resposta), evento 1583 (verbete_citado, contrato-produto), evento 1584 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1570 a 1598 da trilha; hash dos eventos deste caso: `af6cbc6cf0f2f866`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
