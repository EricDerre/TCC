<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-13`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-13@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `registro_duplicado` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,84)

**IMPACTO (declarado):** `O usuário recebeu duas cobranças para a mesma reserva, resultando em duplicidade na cobrança.`

Justificativa (gerada por molde): O agente respondeu registro_duplicado porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes registro_duplicado, contrato-pedido, codificacao_incorreta estavam entre os entregues ao modelo. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete registro_duplicado não mudou a resposta: sem efeito medido do contexto. A troca do verbete registro_duplicado por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 3513): regras diff_contra_contrato; antes {"chars": 54}, depois {"chars": 54}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `2dd19e03d4c54746`):

```text
Duas respostas 201, com id_pedido 8 e 9, mesmos dados.
```

## 3. Contraste com a segunda causa

registro_duplicado sem alternativa registrada no nó

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| registro_duplicado | 0,84 | sim |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[registro_duplicado]`; verbetes citados: `registro_duplicado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `registro_duplicado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `registro_duplicado` | confere | contexto: `registro_duplicado`, `contrato-pedido`, `codificacao_incorreta` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | confere | verbetes: `registro_duplicado` |
| fonte_formato_valido | `[registro_duplicado]` | confere | {"ids": ["registro_duplicado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `registro_duplicado` | confere | {"termo": "registro_duplicado"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `registro_duplicado` | registro_duplicado | registro_duplicado | 0,84 | 1,00 | sem efeito medido do contexto |
| troca | `registro_duplicado` | registro_duplicado | registro_duplicado | 0,84 | 1,00 | sem efeito medido do contexto |
| sem_documentacao | `` | registro_duplicado | registro_duplicado | 0,84 | 1,00 | sem efeito medido do contexto |
| repeticao_da_base | `` | registro_duplicado | registro_duplicado | 0,84 | 0,85 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-13 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3511 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:14:51 | caso run-13 |
| 3513 | 2 | poda | programa | ao_vivo | 2026-11-05T02:14:51 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3514 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:14:51 | poda: escolha nao_json; divergência não |
| 3515 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:14:51 | 3 de 39 verbetes entregues |
| 3516 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:14:51 | recuperacao: escolha registro_duplicado,contrato-pedido,codificacao_incorreta; divergência não |
| 3518 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:14:51 | {"etapa": "diagnostico", "sha": "6cb38042344129e1", "prompt_sha256": "6cb380423441", "chars": 3257, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3520 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:14:51 | diagnostico: 61,3 s |
| 3521 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:14:51 | causa_raiz: `registro_duplicado` |
| 3522 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:14:51 | campo: `nenhum` |
| 3523 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:14:51 | impacto: `O usuário recebeu duas cobranças para a mesma reserva, resultando em duplicidade na cobrança.` |
| 3524 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:14:51 | fonte: `[registro_duplicado]` |
| 3525 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:14:51 | fonte_citada: `registro_duplicado` |
| 3526 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:51 | quatro_linhas_presentes: confere |
| 3527 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:51 | rotulo_no_conjunto: confere |
| 3528 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:51 | fonte_existe_na_biblioteca: confere |
| 3529 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:51 | fonte_estava_no_contexto: confere |
| 3530 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:51 | campo_existe_no_caso: nao_se_aplica |
| 3531 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:51 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3532 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:51 | notas_nos_verbetes_citados: informativo |
| 3533 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:51 | impacto: nao_verificavel |
| 3534 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:51 | fonte_formato_valido: confere |
| 3535 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:14:51 | fonte_contem_termo_da_causa: confere |
| 3538 | 23 | inferencia | programa | ao_vivo | 2026-11-05T02:14:51 | intervencao:remocao: 45,5 s |
| 3539 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T02:14:51 | remocao de registro_duplicado: rótulo registro_duplicado para registro_duplicado |
| 3542 | 25 | inferencia | programa | ao_vivo | 2026-11-05T02:14:51 | intervencao:troca: 46,0 s |
| 3543 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T02:14:51 | troca de registro_duplicado: rótulo registro_duplicado para registro_duplicado |
| 3546 | 27 | inferencia | programa | ao_vivo | 2026-11-05T02:14:51 | intervencao:sem_documentacao: 37,5 s |
| 3547 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T02:14:51 | sem_documentacao de None: rótulo registro_duplicado para registro_duplicado |
| 3549 | 29 | inferencia | programa | ao_vivo | 2026-11-05T02:14:51 | intervencao:repeticao_da_base: 14,3 s |
| 3550 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T02:14:51 | repeticao_da_base de None: rótulo registro_duplicado para registro_duplicado |
| 3551 | 31 | decisao | programa | ao_vivo | 2026-11-05T02:14:51 | diagnostico: escolha registro_duplicado; divergência não |

</details>

Nós de decisão:

- evento 3514, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 3513 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3516, `recuperacao`: escolha `registro_duplicado,contrato-pedido,codificacao_incorreta`; resultado verbetes_entregues; evidência: evento 3515 (verbete_entregue, registro_duplicado), evento 3515 (verbete_entregue, contrato-pedido), evento 3515 (verbete_entregue, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: registro_duplicado, contrato-pedido, codificacao_incorreta (gen_ai: retrieval)
- evento 3551, `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido; evidência: evento 3513 (sinal_em_codigo), evento 3515 (verbete_entregue, registro_duplicado), evento 3515 (verbete_entregue, contrato-pedido), evento 3515 (verbete_entregue, codificacao_incorreta), evento 3520 (resposta), evento 3525 (verbete_citado, registro_duplicado); divergência: não; falha: nenhuma; prov.used: registro_duplicado, contrato-pedido, codificacao_incorreta (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3511 a 3551 da trilha; hash dos eventos deste caso: `4b26eefa154d1d35`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
