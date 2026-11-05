<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-10@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-10@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `situacao` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê a coluna de status vazia, pois a chave "situacao" foi renomeada para "status" no servidor, mas a interface ainda espera "situacao".`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo situacao porque o sinal id_pedido: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes campo_renomeado, contrato-pedido, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 2327): regras diff_contra_contrato; antes {"chars": 134}, depois {"chars": 134}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id_pedido | texto | inteiro |
| status | texto ('Em Analise' ou 'Cancelado') |  |
| situacao |  | texto |

Trecho podado (hash `00299f6488aedb89`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "situacao": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

campo_renomeado e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_renomeado, contrato-pedido, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| campo_ausente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado]`; verbetes citados: `campo_renomeado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `campo_renomeado`, `contrato-pedido`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_renomeado` |
| fonte_formato_valido | `[campo_renomeado]` | confere | {"ids": ["campo_renomeado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `situacao` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-10 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2326 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:14:57 | caso sin-10@contrato_alterado |
| 2327 | 2 | poda | programa | ao_vivo | 2026-11-05T01:14:57 | corpo_http: 3 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2328 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:14:57 | poda: escolha json/lista; id_pedido:tipo_diferente, status:ausente, situacao:inesperado; divergência não |
| 2329 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:14:57 | 3 de 39 verbetes entregues |
| 2330 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:14:57 | recuperacao: escolha campo_renomeado,contrato-pedido,pedido-reserva; divergência não |
| 2332 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:14:57 | {"etapa": "diagnostico", "sha": "ad8c6afb0a994310", "prompt_sha256": "ad8c6afb0a99", "chars": 3545, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2334 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:14:57 | diagnostico: 41,0 s |
| 2335 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:14:57 | causa_raiz: `campo_renomeado` |
| 2336 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:14:57 | campo: `situacao` |
| 2337 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:14:57 | impacto: `O usuário vê a coluna de status vazia, pois a chave "situacao" foi renomeada para "status" no servidor, mas a interface ainda espera "situacao".` |
| 2338 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:14:57 | fonte: `[campo_renomeado]` |
| 2339 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:14:57 | fonte_citada: `campo_renomeado` |
| 2340 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:57 | quatro_linhas_presentes: confere |
| 2341 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:57 | rotulo_no_conjunto: confere |
| 2342 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:57 | fonte_existe_na_biblioteca: confere |
| 2343 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:57 | fonte_estava_no_contexto: confere |
| 2344 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:57 | campo_existe_no_caso: confere |
| 2345 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:57 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2346 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:57 | notas_nos_verbetes_citados: informativo |
| 2347 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:57 | impacto: nao_verificavel |
| 2348 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:57 | fonte_formato_valido: confere |
| 2349 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:57 | fonte_contem_termo_da_causa: confere |
| 2350 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:14:57 | diagnostico: escolha campo_renomeado; divergência não |

</details>

Nós de decisão:

- evento 2328, `poda`: escolha `json/lista; id_pedido:tipo_diferente, status:ausente, situacao:inesperado`; resultado sinais_em_codigo; evidência: evento 2327 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id_pedido, status, situacao (gen_ai: plan)
- evento 2330, `recuperacao`: escolha `campo_renomeado,contrato-pedido,pedido-reserva`; resultado verbetes_entregues; evidência: evento 2329 (verbete_entregue, campo_renomeado), evento 2329 (verbete_entregue, contrato-pedido), evento 2329 (verbete_entregue, pedido-reserva); divergência: não; falha: nenhuma; prov.used: campo_renomeado, contrato-pedido, pedido-reserva (gen_ai: retrieval)
- evento 2350, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 2327 (sinal_em_codigo), evento 2329 (verbete_entregue, campo_renomeado), evento 2329 (verbete_entregue, contrato-pedido), evento 2329 (verbete_entregue, pedido-reserva), evento 2334 (resposta), evento 2339 (verbete_citado, campo_renomeado); divergência: não; falha: nenhuma; prov.used: campo_renomeado, contrato-pedido, pedido-reserva (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2326 a 2350 da trilha; hash dos eventos deste caso: `7e76eae190880737`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
