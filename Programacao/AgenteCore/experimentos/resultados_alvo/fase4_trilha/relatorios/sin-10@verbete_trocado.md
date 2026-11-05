<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-10@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-10@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `chave_de_juncao_errada` · **CAMPO:** `situacao` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê a coluna de situação da reserva vazia, indicando um erro na junção dos dados.`

Justificativa (gerada por molde): O agente respondeu chave_de_juncao_errada no campo situacao porque o sinal status: esperado texto ('Em Analise' ou 'Cancelado'), recebido None está presente na resposta HTTP e os verbetes chave_de_juncao_errada, contrato-pedido, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 2303): regras diff_contra_contrato; antes {"chars": 134}, depois {"chars": 134}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| status | texto ('Em Analise' ou 'Cancelado') |  |
| situacao |  | texto |

Trecho podado (hash `00299f6488aedb89`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "situacao": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

chave_de_juncao_errada e não campo_ausente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: chave_de_juncao_errada, contrato-pedido, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| chave_de_juncao_errada | 0,99 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| registro_duplicado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[chave_de_juncao_errada]`; verbetes citados: `chave_de_juncao_errada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `chave_de_juncao_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `chave_de_juncao_errada` | confere | contexto: `chave_de_juncao_errada`, `contrato-pedido`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `chave_de_juncao_errada` | confere | verbetes: `chave_de_juncao_errada`, `pedido-reserva` |
| fonte_formato_valido | `[chave_de_juncao_errada]` | confere | {"ids": ["chave_de_juncao_errada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `chave_de_juncao_errada` | confere | {"termo": "chave_de_juncao_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `situacao` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-10 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2302 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:14:36 | caso sin-10@verbete_trocado |
| 2303 | 2 | poda | programa | ao_vivo | 2026-11-05T01:14:36 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2304 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:14:36 | poda: escolha json/lista; status:ausente, situacao:inesperado; divergência não |
| 2305 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:14:36 | 3 de 39 verbetes entregues |
| 2306 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:14:36 | recuperacao: escolha chave_de_juncao_errada,contrato-pedido,pedido-reserva; divergência não |
| 2307 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:14:36 | {"etapa": "diagnostico", "sha": "a340b1e2e4ec97a5", "prompt_sha256": "a340b1e2e4ec", "chars": 3952, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2308 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:14:36 | diagnostico: 16,5 s |
| 2309 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:14:36 | causa_raiz: `chave_de_juncao_errada` |
| 2310 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:14:36 | campo: `situacao` |
| 2311 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:14:36 | impacto: `O usuário vê a coluna de situação da reserva vazia, indicando um erro na junção dos dados.` |
| 2312 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:14:36 | fonte: `[chave_de_juncao_errada]` |
| 2313 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:14:36 | fonte_citada: `chave_de_juncao_errada` |
| 2314 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:36 | quatro_linhas_presentes: confere |
| 2315 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:36 | rotulo_no_conjunto: confere |
| 2316 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:36 | fonte_existe_na_biblioteca: confere |
| 2317 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:36 | fonte_estava_no_contexto: confere |
| 2318 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:36 | campo_existe_no_caso: confere |
| 2319 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:36 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2320 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:36 | notas_nos_verbetes_citados: informativo |
| 2321 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:36 | impacto: nao_verificavel |
| 2322 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:36 | fonte_formato_valido: confere |
| 2323 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:14:36 | fonte_contem_termo_da_causa: confere |
| 2324 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:14:36 | diagnostico: escolha chave_de_juncao_errada; divergência não |

</details>

Nós de decisão:

- evento 2304, `poda`: escolha `json/lista; status:ausente, situacao:inesperado`; resultado sinais_em_codigo; evidência: evento 2303 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: status, situacao (gen_ai: plan)
- evento 2306, `recuperacao`: escolha `chave_de_juncao_errada,contrato-pedido,pedido-reserva`; resultado verbetes_entregues; evidência: evento 2305 (verbete_entregue, chave_de_juncao_errada), evento 2305 (verbete_entregue, contrato-pedido), evento 2305 (verbete_entregue, pedido-reserva); divergência: não; falha: nenhuma; prov.used: chave_de_juncao_errada, contrato-pedido, pedido-reserva (gen_ai: retrieval)
- evento 2324, `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido; evidência: evento 2303 (sinal_em_codigo), evento 2305 (verbete_entregue, chave_de_juncao_errada), evento 2305 (verbete_entregue, contrato-pedido), evento 2305 (verbete_entregue, pedido-reserva), evento 2308 (resposta), evento 2313 (verbete_citado, chave_de_juncao_errada); divergência: não; falha: nenhuma; prov.used: chave_de_juncao_errada, contrato-pedido, pedido-reserva (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2302 a 2324 da trilha; hash dos eventos deste caso: `3e081902de64de42`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
