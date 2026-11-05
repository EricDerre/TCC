<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-7@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-7@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `id_pedido` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O botão de cancelar reserva não funciona porque o campo `id_pedido` está ausente na resposta, impedindo a identificação do pedido a ser cancelado.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo id_pedido porque o sinal id_pedido: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes contrato-pedido, pedido-reserva, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_renomeado, ficou com probabilidade 0,01. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 2158): regras diff_contra_contrato; antes {"chars": 116}, depois {"chars": 116}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id_pedido | inteiro |  |

Trecho podado (hash `b88406ab40b56cca`):

```text
[{"pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

campo_ausente e não campo_renomeado: a escolha tem probabilidade 0,99 contra 0,01; verbete(s) na evidência: contrato-pedido, pedido-reserva, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,99 | sim |
| campo_renomeado | 0,01 |  |
| registro_duplicado | 0,00 |  |
| resposta_truncada | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-pedido`, `campo_ausente` |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"ids": ["contrato-pedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id_pedido` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-7 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2157 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:07:04 | caso sin-7@sonda |
| 2158 | 2 | poda | programa | ao_vivo | 2026-11-05T01:07:04 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2159 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:07:04 | poda: escolha json/lista; id_pedido:ausente; divergência não |
| 2160 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:07:04 | 3 de 39 verbetes entregues |
| 2161 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:07:04 | recuperacao: escolha contrato-pedido,pedido-reserva,campo_ausente; divergência não |
| 2163 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:07:04 | {"etapa": "diagnostico", "sha": "945f378c1274b32c", "prompt_sha256": "945f378c1274", "chars": 3483, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2164 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:07:04 | diagnostico: 56,4 s |
| 2165 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:07:04 | causa_raiz: `campo_ausente` |
| 2166 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:07:04 | campo: `id_pedido` |
| 2167 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:07:04 | impacto: `O botão de cancelar reserva não funciona porque o campo `id_pedido` está ausente na resposta, impedindo a identificação do pedido a ser cancelado.` |
| 2168 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:07:04 | fonte: `[contrato-pedido]` |
| 2169 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:07:04 | fonte_citada: `contrato-pedido` |
| 2170 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:07:04 | quatro_linhas_presentes: confere |
| 2171 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:07:04 | rotulo_no_conjunto: confere |
| 2172 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:07:04 | fonte_existe_na_biblioteca: confere |
| 2173 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:07:04 | fonte_estava_no_contexto: confere |
| 2174 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:07:04 | campo_existe_no_caso: confere |
| 2175 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:07:04 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2176 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:07:04 | notas_nos_verbetes_citados: informativo |
| 2177 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:07:04 | impacto: nao_verificavel |
| 2178 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:07:04 | fonte_formato_valido: confere |
| 2179 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:07:04 | fonte_contem_termo_da_causa: nao_confere |
| 2180 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:07:04 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 2159, `poda`: escolha `json/lista; id_pedido:ausente`; resultado sinais_em_codigo; evidência: evento 2158 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id_pedido (gen_ai: plan)
- evento 2161, `recuperacao`: escolha `contrato-pedido,pedido-reserva,campo_ausente`; resultado verbetes_entregues; evidência: evento 2160 (verbete_entregue, contrato-pedido), evento 2160 (verbete_entregue, pedido-reserva), evento 2160 (verbete_entregue, campo_ausente); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, campo_ausente (gen_ai: retrieval)
- evento 2180, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 2158 (sinal_em_codigo), evento 2160 (verbete_entregue, contrato-pedido), evento 2160 (verbete_entregue, pedido-reserva), evento 2160 (verbete_entregue, campo_ausente), evento 2164 (resposta), evento 2169 (verbete_citado, contrato-pedido); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2157 a 2180 da trilha; hash dos eventos deste caso: `7002daaa003d9809`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
