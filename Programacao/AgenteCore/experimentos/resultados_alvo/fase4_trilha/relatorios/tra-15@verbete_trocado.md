<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-15@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-15@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `pessoas` · selo de probabilidade: **medio** (p = 0,96)

**IMPACTO (declarado):** `A reserva confirmada mostra o dobro de pessoas do que foi solicitado.`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo pessoas porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes valor_fora_do_dominio, pedido-reserva, fluxo-reserva-e-cancelamento estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,04. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 3303): regras diff_contra_contrato; antes {"chars": 173}, depois {"chars": 173}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `76db07a3faf27269`):

```text
POST enviou {"pessoas": 4}; GET devolveu [{"id_pedido": 8, "pessoas": 8, "data_pedido": "2026-09-12", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

valor_fora_do_dominio e não tipo_divergente: a escolha tem probabilidade 0,96 contra 0,04; verbete(s) na evidência: valor_fora_do_dominio, pedido-reserva, fluxo-reserva-e-cancelamento

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 0,96 | sim |
| tipo_divergente | 0,04 |  |
| contagem_inconsistente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[valor_fora_do_dominio]`; verbetes citados: `valor_fora_do_dominio`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `valor_fora_do_dominio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `valor_fora_do_dominio` | confere | contexto: `valor_fora_do_dominio`, `pedido-reserva`, `fluxo-reserva-e-cancelamento` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `valor_fora_do_dominio`, `pedido-reserva`, `fluxo-reserva-e-cancelamento` |
| fonte_formato_valido | `[valor_fora_do_dominio]` | confere | {"ids": ["valor_fora_do_dominio"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `valor_fora_do_dominio` | confere | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `pessoas` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-15 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3302 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:03:48 | caso tra-15@verbete_trocado |
| 3303 | 2 | poda | programa | ao_vivo | 2026-11-05T02:03:48 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3304 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:03:48 | poda: escolha nao_json; divergência não |
| 3305 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:03:48 | 3 de 39 verbetes entregues |
| 3306 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:03:48 | recuperacao: escolha valor_fora_do_dominio,pedido-reserva,fluxo-reserva-e-cancelamento; divergência não |
| 3307 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:03:48 | {"etapa": "diagnostico", "sha": "82a490767cf9c9cb", "prompt_sha256": "82a490767cf9", "chars": 3371, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3308 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:03:48 | diagnostico: 14,0 s |
| 3309 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:03:48 | causa_raiz: `valor_fora_do_dominio` |
| 3310 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:03:48 | campo: `pessoas` |
| 3311 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:03:48 | impacto: `A reserva confirmada mostra o dobro de pessoas do que foi solicitado.` |
| 3312 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:03:48 | fonte: `[valor_fora_do_dominio]` |
| 3313 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:03:48 | fonte_citada: `valor_fora_do_dominio` |
| 3314 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:03:48 | quatro_linhas_presentes: confere |
| 3315 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:03:48 | rotulo_no_conjunto: confere |
| 3316 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:03:48 | fonte_existe_na_biblioteca: confere |
| 3317 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:03:48 | fonte_estava_no_contexto: confere |
| 3318 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:03:48 | campo_existe_no_caso: confere |
| 3319 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:03:48 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3320 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:03:48 | notas_nos_verbetes_citados: informativo |
| 3321 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:03:48 | impacto: nao_verificavel |
| 3322 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:03:48 | fonte_formato_valido: confere |
| 3323 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:03:48 | fonte_contem_termo_da_causa: confere |
| 3324 | 23 | decisao | programa | ao_vivo | 2026-11-05T02:03:48 | diagnostico: escolha valor_fora_do_dominio; divergência não |

</details>

Nós de decisão:

- evento 3304, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 3303 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3306, `recuperacao`: escolha `valor_fora_do_dominio,pedido-reserva,fluxo-reserva-e-cancelamento`; resultado verbetes_entregues; evidência: evento 3305 (verbete_entregue, valor_fora_do_dominio), evento 3305 (verbete_entregue, pedido-reserva), evento 3305 (verbete_entregue, fluxo-reserva-e-cancelamento); divergência: não; falha: nenhuma; prov.used: valor_fora_do_dominio, pedido-reserva, fluxo-reserva-e-cancelamento (gen_ai: retrieval)
- evento 3324, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 3303 (sinal_em_codigo), evento 3305 (verbete_entregue, valor_fora_do_dominio), evento 3305 (verbete_entregue, pedido-reserva), evento 3305 (verbete_entregue, fluxo-reserva-e-cancelamento), evento 3308 (resposta), evento 3313 (verbete_citado, valor_fora_do_dominio); divergência: não; falha: nenhuma; prov.used: valor_fora_do_dominio, pedido-reserva, fluxo-reserva-e-cancelamento (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3302 a 3324 da trilha; hash dos eventos deste caso: `a21edcf31dbf1681`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
