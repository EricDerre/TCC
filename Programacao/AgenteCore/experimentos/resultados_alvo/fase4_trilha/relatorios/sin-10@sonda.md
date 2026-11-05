<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-10@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-10@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `situacao` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê a coluna de status vazia, pois a chave "situacao" não existe no contrato esperado pela interface.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo situacao porque o sinal status: esperado texto ('Em Analise' ou 'Cancelado'), recebido None está presente na resposta HTTP e os verbetes campo_renomeado, contrato-pedido, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 2274): regras diff_contra_contrato; antes {"chars": 134}, depois {"chars": 134}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
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
| campo_ausente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado] [contrato-pedido]`; verbetes citados: `campo_renomeado`, `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `campo_renomeado`, `contrato-pedido`, `pedido-reserva` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `campo_renomeado`, `contrato-pedido`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_renomeado` |
| fonte_formato_valido | `[campo_renomeado] [contrato-pedido]` | confere | {"ids": ["campo_renomeado", "contrato-pedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |
| fonte_contem_termo_da_causa | `contrato-pedido` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `situacao` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-10 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2273 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:13:35 | caso sin-10@sonda |
| 2274 | 2 | poda | programa | ao_vivo | 2026-11-05T01:13:35 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2275 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:13:35 | poda: escolha json/lista; status:ausente, situacao:inesperado; divergência não |
| 2276 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:13:35 | 3 de 39 verbetes entregues |
| 2277 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:13:35 | recuperacao: escolha campo_renomeado,contrato-pedido,pedido-reserva; divergência não |
| 2279 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:13:35 | {"etapa": "diagnostico", "sha": "de262c651d55ae72", "prompt_sha256": "de262c651d55", "chars": 3660, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2281 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:13:35 | diagnostico: 57,9 s |
| 2282 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:13:35 | causa_raiz: `campo_renomeado` |
| 2283 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:13:35 | campo: `situacao` |
| 2284 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:13:35 | impacto: `O usuário vê a coluna de status vazia, pois a chave "situacao" não existe no contrato esperado pela interface.` |
| 2285 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:13:35 | fonte: `[campo_renomeado] [contrato-pedido]` |
| 2286 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:13:35 | fonte_citada: `campo_renomeado` |
| 2287 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T01:13:35 | fonte_citada: `contrato-pedido` |
| 2288 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | quatro_linhas_presentes: confere |
| 2289 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | rotulo_no_conjunto: confere |
| 2290 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | fonte_existe_na_biblioteca: confere |
| 2291 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | fonte_existe_na_biblioteca: confere |
| 2292 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | fonte_estava_no_contexto: confere |
| 2293 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | fonte_estava_no_contexto: confere |
| 2294 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | campo_existe_no_caso: confere |
| 2295 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2296 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | notas_nos_verbetes_citados: informativo |
| 2297 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | impacto: nao_verificavel |
| 2298 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | fonte_formato_valido: confere |
| 2299 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | fonte_contem_termo_da_causa: confere |
| 2300 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T01:13:35 | fonte_contem_termo_da_causa: confere |
| 2301 | 27 | decisao | programa | ao_vivo | 2026-11-05T01:13:35 | diagnostico: escolha campo_renomeado; divergência não |

</details>

Nós de decisão:

- evento 2275, `poda`: escolha `json/lista; status:ausente, situacao:inesperado`; resultado sinais_em_codigo; evidência: evento 2274 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: status, situacao (gen_ai: plan)
- evento 2277, `recuperacao`: escolha `campo_renomeado,contrato-pedido,pedido-reserva`; resultado verbetes_entregues; evidência: evento 2276 (verbete_entregue, campo_renomeado), evento 2276 (verbete_entregue, contrato-pedido), evento 2276 (verbete_entregue, pedido-reserva); divergência: não; falha: nenhuma; prov.used: campo_renomeado, contrato-pedido, pedido-reserva (gen_ai: retrieval)
- evento 2301, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 2274 (sinal_em_codigo), evento 2276 (verbete_entregue, campo_renomeado), evento 2276 (verbete_entregue, contrato-pedido), evento 2276 (verbete_entregue, pedido-reserva), evento 2281 (resposta), evento 2286 (verbete_citado, campo_renomeado), evento 2287 (verbete_citado, contrato-pedido); divergência: não; falha: nenhuma; prov.used: campo_renomeado, contrato-pedido, pedido-reserva (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2273 a 2301 da trilha; hash dos eventos deste caso: `797b2e51029b89d6`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
