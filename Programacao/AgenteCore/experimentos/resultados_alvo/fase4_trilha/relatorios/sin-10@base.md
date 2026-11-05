<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-10`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-10@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `situacao` · selo de probabilidade: **alto** (p = 0,99) · **CONFLITO**: a troca do verbete campo_renomeado por um errado mudou a resposta de campo_renomeado para chave_de_juncao_errada

**IMPACTO (declarado):** `O usuário vê a coluna de status vazia, pois a chave 'situacao' foi renomeada para 'status' no servidor, mas a interface ainda espera 'situacao'.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo situacao porque o sinal status: esperado texto ('Em Analise' ou 'Cancelado'), recebido None está presente na resposta HTTP e os verbetes campo_renomeado, contrato-pedido, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete campo_renomeado não mudou a resposta: sem efeito medido do contexto. A troca do verbete campo_renomeado por um verbete errado mudou a resposta (de campo_renomeado para chave_de_juncao_errada). A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a troca do verbete campo_renomeado por um errado mudou a resposta de campo_renomeado para chave_de_juncao_errada.

## 2. Evidência

Poda de `corpo_http` (evento 2234): regras diff_contra_contrato; antes {"chars": 134}, depois {"chars": 134}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| status | texto ('Em Analise' ou 'Cancelado') |  |
| situacao |  | texto |

Trecho podado (hash `00299f6488aedb89`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "situacao": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

campo_renomeado e não tipo_divergente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: campo_renomeado, contrato-pedido, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 0,99 | sim |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| campo_ausente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado]`; verbetes citados: `campo_renomeado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `campo_renomeado`, `contrato-pedido`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_renomeado` |
| fonte_formato_valido | `[campo_renomeado]` | confere | {"ids": ["campo_renomeado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `campo_renomeado` | campo_renomeado | campo_renomeado | 0,99 | 0,99 | sem efeito medido do contexto |
| troca | `campo_renomeado` | campo_renomeado | chave_de_juncao_errada | 0,99 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| sem_documentacao | `` | campo_renomeado | campo_renomeado | 0,99 | 1,00 | sem efeito medido do contexto |
| repeticao_da_base | `` | campo_renomeado | campo_renomeado | 0,99 | 0,99 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `situacao` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-10 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2232 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:09:24 | caso sin-10 |
| 2234 | 2 | poda | programa | ao_vivo | 2026-11-05T01:09:24 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2235 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:09:24 | poda: escolha json/lista; status:ausente, situacao:inesperado; divergência não |
| 2236 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:09:24 | 3 de 39 verbetes entregues |
| 2237 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:09:24 | recuperacao: escolha campo_renomeado,contrato-pedido,pedido-reserva; divergência não |
| 2239 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:09:24 | {"etapa": "diagnostico", "sha": "ec9fc5cf77416e6d", "prompt_sha256": "ec9fc5cf7741", "chars": 3547, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2241 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:09:24 | diagnostico: 71,4 s |
| 2242 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:09:24 | causa_raiz: `campo_renomeado` |
| 2243 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:09:24 | campo: `situacao` |
| 2244 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:09:24 | impacto: `O usuário vê a coluna de status vazia, pois a chave 'situacao' foi renomeada para 'status' no servidor, mas a interface ainda espera 'situacao'.` |
| 2245 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:09:24 | fonte: `[campo_renomeado]` |
| 2246 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:09:24 | fonte_citada: `campo_renomeado` |
| 2247 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:09:24 | quatro_linhas_presentes: confere |
| 2248 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:09:24 | rotulo_no_conjunto: confere |
| 2249 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:09:24 | fonte_existe_na_biblioteca: confere |
| 2250 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:09:24 | fonte_estava_no_contexto: confere |
| 2251 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:09:24 | campo_existe_no_caso: confere |
| 2252 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:09:24 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2253 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:09:24 | notas_nos_verbetes_citados: informativo |
| 2254 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:09:24 | impacto: nao_verificavel |
| 2255 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:09:24 | fonte_formato_valido: confere |
| 2256 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:09:24 | fonte_contem_termo_da_causa: confere |
| 2259 | 23 | inferencia | programa | ao_vivo | 2026-11-05T01:09:24 | intervencao:remocao: 49,3 s |
| 2260 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T01:09:24 | remocao de campo_renomeado: rótulo campo_renomeado para campo_renomeado |
| 2263 | 25 | inferencia | programa | ao_vivo | 2026-11-05T01:09:24 | intervencao:troca: 75,6 s |
| 2264 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T01:09:24 | troca de campo_renomeado: rótulo campo_renomeado para chave_de_juncao_errada |
| 2267 | 27 | inferencia | programa | ao_vivo | 2026-11-05T01:09:24 | intervencao:sem_documentacao: 34,3 s |
| 2268 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T01:09:24 | sem_documentacao de None: rótulo campo_renomeado para campo_renomeado |
| 2270 | 29 | inferencia | programa | ao_vivo | 2026-11-05T01:09:24 | intervencao:repeticao_da_base: 15,6 s |
| 2271 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T01:09:24 | repeticao_da_base de None: rótulo campo_renomeado para campo_renomeado |
| 2272 | 31 | decisao | programa | ao_vivo | 2026-11-05T01:09:24 | diagnostico: escolha campo_renomeado; divergência sim |

</details>

Nós de decisão:

- evento 2235, `poda`: escolha `json/lista; status:ausente, situacao:inesperado`; resultado sinais_em_codigo; evidência: evento 2234 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: status, situacao (gen_ai: plan)
- evento 2237, `recuperacao`: escolha `campo_renomeado,contrato-pedido,pedido-reserva`; resultado verbetes_entregues; evidência: evento 2236 (verbete_entregue, campo_renomeado), evento 2236 (verbete_entregue, contrato-pedido), evento 2236 (verbete_entregue, pedido-reserva); divergência: não; falha: nenhuma; prov.used: campo_renomeado, contrato-pedido, pedido-reserva (gen_ai: retrieval)
- evento 2272, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 2234 (sinal_em_codigo), evento 2236 (verbete_entregue, campo_renomeado), evento 2236 (verbete_entregue, contrato-pedido), evento 2236 (verbete_entregue, pedido-reserva), evento 2241 (resposta), evento 2246 (verbete_citado, campo_renomeado); divergência: sim; falha: nenhuma; prov.used: campo_renomeado, contrato-pedido, pedido-reserva (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2232 a 2272 da trilha; hash dos eventos deste caso: `e2a948f3950afff0`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
