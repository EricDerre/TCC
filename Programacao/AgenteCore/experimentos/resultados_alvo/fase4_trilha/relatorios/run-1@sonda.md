<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-1@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-1@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `A aba de produtos via API exibe a mensagem "Erro ao carregar produtos da CobaiaAPI: erro interno (fault injection)".`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor no campo id porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1065): regras diff_contra_contrato; antes {"chars": 44}, depois {"chars": 44}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | inteiro |  |
| nome | texto |  |
| resumo | texto\|nulo |  |
| tipo | texto |  |
| preco | numero |  |
| imagem | texto\|nulo |  |
| destaque | booleano |  |
| detail |  | texto |

Trecho podado (hash `6b438745dff984ef`):

```text
{"detail": "erro interno (fault injection)"}
```

## 3. Contraste com a segunda causa

erro_interno_do_servidor e não corpo_nao_e_json: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 0,98 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[erro_interno_do_servidor]`; verbetes citados: `erro_interno_do_servidor`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo` |
| fonte_formato_valido | `[erro_interno_do_servidor]` | confere | {"ids": ["erro_interno_do_servidor"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `erro_interno_do_servidor` | confere | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-1 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1064 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:03:27 | caso run-1@sonda |
| 1065 | 2 | poda | programa | ao_vivo | 2026-11-05T00:03:27 | corpo_http: 8 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1066 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:03:27 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, detail:inesperado; divergência não |
| 1067 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:03:27 | 3 de 39 verbetes entregues |
| 1068 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:03:27 | recuperacao: escolha erro_interno_do_servidor,mensagens-de-erro-do-codigo,contagem_inconsistente; divergência não |
| 1070 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:03:27 | {"etapa": "diagnostico", "sha": "7b0b90d2922d0882", "prompt_sha256": "7b0b90d2922d", "chars": 3625, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1071 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:03:27 | diagnostico: 51,2 s |
| 1072 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:03:27 | causa_raiz: `erro_interno_do_servidor` |
| 1073 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:03:27 | campo: `nenhum` |
| 1074 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:03:27 | impacto: `A aba de produtos via API exibe a mensagem "Erro ao carregar produtos da CobaiaAPI: erro interno (fault injection)".` |
| 1075 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:03:27 | fonte: `[erro_interno_do_servidor]` |
| 1076 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:03:27 | fonte_citada: `erro_interno_do_servidor` |
| 1077 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:03:27 | quatro_linhas_presentes: confere |
| 1078 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:03:27 | rotulo_no_conjunto: confere |
| 1079 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:03:27 | fonte_existe_na_biblioteca: confere |
| 1080 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:03:27 | fonte_estava_no_contexto: confere |
| 1081 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:03:27 | campo_existe_no_caso: nao_se_aplica |
| 1082 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:03:27 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1083 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:03:27 | notas_nos_verbetes_citados: informativo |
| 1084 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:03:27 | impacto: nao_verificavel |
| 1085 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:03:27 | fonte_formato_valido: confere |
| 1086 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:03:27 | fonte_contem_termo_da_causa: confere |
| 1087 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:03:27 | diagnostico: escolha erro_interno_do_servidor; divergência não |

</details>

Nós de decisão:

- evento 1066, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, detail:inesperado`; resultado sinais_em_codigo; evidência: evento 1065 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, detail (gen_ai: plan)
- evento 1068, `recuperacao`: escolha `erro_interno_do_servidor,mensagens-de-erro-do-codigo,contagem_inconsistente`; resultado verbetes_entregues; evidência: evento 1067 (verbete_entregue, erro_interno_do_servidor), evento 1067 (verbete_entregue, mensagens-de-erro-do-codigo), evento 1067 (verbete_entregue, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente (gen_ai: retrieval)
- evento 1087, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 1065 (sinal_em_codigo), evento 1067 (verbete_entregue, erro_interno_do_servidor), evento 1067 (verbete_entregue, mensagens-de-erro-do-codigo), evento 1067 (verbete_entregue, contagem_inconsistente), evento 1071 (resposta), evento 1076 (verbete_citado, erro_interno_do_servidor); divergência: não; falha: nenhuma; prov.used: erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1064 a 1087 da trilha; hash dos eventos deste caso: `2aa898b6d871b5e3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
