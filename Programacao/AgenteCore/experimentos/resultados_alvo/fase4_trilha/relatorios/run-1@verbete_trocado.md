<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-1@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-1@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A aba de produtos via API exibe uma mensagem de erro inesperada, impedindo a visualização correta dos produtos.`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor no campo id porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes estrutura_aninhada_divergente, mensagens-de-erro-do-codigo, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1089): regras diff_contra_contrato; antes {"chars": 44}, depois {"chars": 44}.

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

erro_interno_do_servidor e não estrutura_aninhada_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: estrutura_aninhada_divergente, mensagens-de-erro-do-codigo, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 1,00 | sim |
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[estrutura_aninhada_divergente] [mensagens-de-erro-do-codigo]`; verbetes citados: `estrutura_aninhada_divergente`, `mensagens-de-erro-do-codigo`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado existe na biblioteca | `mensagens-de-erro-do-codigo` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `estrutura_aninhada_divergente`, `mensagens-de-erro-do-codigo`, `contagem_inconsistente` |
| O verbete citado estava no contexto entregue ao modelo | `mensagens-de-erro-do-codigo` | confere | contexto: `estrutura_aninhada_divergente`, `mensagens-de-erro-do-codigo`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `mensagens-de-erro-do-codigo` |
| fonte_formato_valido | `[estrutura_aninhada_divergente] [mensagens-de-erro-do-codigo]` | confere | {"ids": ["estrutura_aninhada_divergente", "mensagens-de-erro-do-codigo"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `estrutura_aninhada_divergente` | **não confere** | {"termo": "erro_interno_do_servidor"} |
| fonte_contem_termo_da_causa | `mensagens-de-erro-do-codigo` | **não confere** | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-1 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1088 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:04:22 | caso run-1@verbete_trocado |
| 1089 | 2 | poda | programa | ao_vivo | 2026-11-05T00:04:22 | corpo_http: 8 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1090 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:04:22 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, detail:inesperado; divergência não |
| 1091 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:04:22 | 3 de 39 verbetes entregues |
| 1092 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:04:22 | recuperacao: escolha estrutura_aninhada_divergente,mensagens-de-erro-do-codigo,contagem_inconsistente; divergência não |
| 1093 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:04:22 | {"etapa": "diagnostico", "sha": "47282ce3a0799141", "prompt_sha256": "47282ce3a079", "chars": 3456, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1094 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:04:22 | diagnostico: 18,9 s |
| 1095 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:04:22 | causa_raiz: `erro_interno_do_servidor` |
| 1096 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:04:22 | campo: `nenhum` |
| 1097 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:04:22 | impacto: `A aba de produtos via API exibe uma mensagem de erro inesperada, impedindo a visualização correta dos produtos.` |
| 1098 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:04:22 | fonte: `[estrutura_aninhada_divergente] [mensagens-de-erro-do-codigo]` |
| 1099 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:04:22 | fonte_citada: `estrutura_aninhada_divergente` |
| 1100 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T00:04:22 | fonte_citada: `mensagens-de-erro-do-codigo` |
| 1101 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | quatro_linhas_presentes: confere |
| 1102 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | rotulo_no_conjunto: confere |
| 1103 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | fonte_existe_na_biblioteca: confere |
| 1104 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | fonte_existe_na_biblioteca: confere |
| 1105 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | fonte_estava_no_contexto: confere |
| 1106 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | fonte_estava_no_contexto: confere |
| 1107 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | campo_existe_no_caso: nao_se_aplica |
| 1108 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1109 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | notas_nos_verbetes_citados: informativo |
| 1110 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | impacto: nao_verificavel |
| 1111 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | fonte_formato_valido: confere |
| 1112 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | fonte_contem_termo_da_causa: nao_confere |
| 1113 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T00:04:22 | fonte_contem_termo_da_causa: nao_confere |
| 1114 | 27 | decisao | programa | ao_vivo | 2026-11-05T00:04:22 | diagnostico: escolha erro_interno_do_servidor; divergência não |

</details>

Nós de decisão:

- evento 1090, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, detail:inesperado`; resultado sinais_em_codigo; evidência: evento 1089 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, detail (gen_ai: plan)
- evento 1092, `recuperacao`: escolha `estrutura_aninhada_divergente,mensagens-de-erro-do-codigo,contagem_inconsistente`; resultado verbetes_entregues; evidência: evento 1091 (verbete_entregue, estrutura_aninhada_divergente), evento 1091 (verbete_entregue, mensagens-de-erro-do-codigo), evento 1091 (verbete_entregue, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: estrutura_aninhada_divergente, mensagens-de-erro-do-codigo, contagem_inconsistente (gen_ai: retrieval)
- evento 1114, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 1089 (sinal_em_codigo), evento 1091 (verbete_entregue, estrutura_aninhada_divergente), evento 1091 (verbete_entregue, mensagens-de-erro-do-codigo), evento 1091 (verbete_entregue, contagem_inconsistente), evento 1094 (resposta), evento 1099 (verbete_citado, estrutura_aninhada_divergente), evento 1100 (verbete_citado, mensagens-de-erro-do-codigo); divergência: não; falha: nenhuma; prov.used: estrutura_aninhada_divergente, mensagens-de-erro-do-codigo, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1088 a 1114 da trilha; hash dos eventos deste caso: `860a28cdca0a4006`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
