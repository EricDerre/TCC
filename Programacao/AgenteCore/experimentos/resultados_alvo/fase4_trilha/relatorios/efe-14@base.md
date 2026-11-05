<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-14`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-14@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: a remoção do verbete localizador_quebrado mudou a resposta de localizador_quebrado para estado_da_tela_divergente; a troca do verbete localizador_quebrado por um errado mudou a resposta de localizador_quebrado para estado_da_tela_divergente

**IMPACTO (declarado):** `O usuário não consegue acessar as informações detalhadas do produto ao clicar no botão "Saiba Mais...".`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, nulo_inesperado, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. A remoção do verbete localizador_quebrado mudou a resposta (de localizador_quebrado para estado_da_tela_divergente), então ele pesou na decisão. A troca do verbete localizador_quebrado por um verbete errado mudou a resposta (de localizador_quebrado para estado_da_tela_divergente). A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a remoção do verbete localizador_quebrado mudou a resposta de localizador_quebrado para estado_da_tela_divergente; a troca do verbete localizador_quebrado por um errado mudou a resposta de localizador_quebrado para estado_da_tela_divergente.

## 2. Evidência

Poda de `corpo_http` (evento 3696): regras diff_contra_contrato; antes {"chars": 27}, depois {"chars": 27}.

Trecho podado (hash `48ffb95010655367`):

```text
(nenhuma requisicao falhou)
```

## 3. Contraste com a segunda causa

localizador_quebrado e não nulo_inesperado: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 1,00 | sim |
| nulo_inesperado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado] [ancora-saiba-mais]`; verbetes citados: `localizador_quebrado`, `ancora-saiba-mais`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado existe na biblioteca | `ancora-saiba-mais` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `estado_da_tela_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `ancora-saiba-mais` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `ancora-saiba-mais`, `estado_da_tela_divergente` |
| fonte_formato_valido | `[localizador_quebrado] [ancora-saiba-mais]` | confere | {"ids": ["localizador_quebrado", "ancora-saiba-mais"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |
| fonte_contem_termo_da_causa | `ancora-saiba-mais` | **não confere** | {"termo": "localizador_quebrado"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `localizador_quebrado` | localizador_quebrado | estado_da_tela_divergente | 1,00 | 0,04 | mudou a resposta: o verbete pesou na decisão |
| troca | `localizador_quebrado` | localizador_quebrado | estado_da_tela_divergente | 1,00 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| sem_documentacao | `` | localizador_quebrado | localizador_quebrado | 1,00 | 1,00 | sem efeito medido do contexto |
| repeticao_da_base | `` | localizador_quebrado | localizador_quebrado | 1,00 | 1,00 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-14 --sem-seletor`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3695 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:25:06 | caso efe-14 |
| 3696 | 2 | poda | programa | ao_vivo | 2026-11-05T02:25:06 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3697 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:25:06 | poda: escolha sem_contrato; divergência não |
| 3698 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:25:06 | 3 de 39 verbetes entregues |
| 3699 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:25:06 | recuperacao: escolha localizador_quebrado,ancora-saiba-mais,estado_da_tela_divergente; divergência não |
| 3701 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:25:06 | {"etapa": "diagnostico", "sha": "f220ca3b2d36ec82", "prompt_sha256": "f220ca3b2d36", "chars": 3965, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3703 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:25:06 | diagnostico: 46,9 s |
| 3704 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:25:06 | causa_raiz: `localizador_quebrado` |
| 3705 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:25:06 | campo: `nenhum` |
| 3706 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:25:06 | impacto: `O usuário não consegue acessar as informações detalhadas do produto ao clicar no botão "Saiba Mais...".` |
| 3707 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:25:06 | fonte: `[localizador_quebrado] [ancora-saiba-mais]` |
| 3708 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:25:06 | fonte_citada: `localizador_quebrado` |
| 3709 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T02:25:06 | fonte_citada: `ancora-saiba-mais` |
| 3710 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | quatro_linhas_presentes: confere |
| 3711 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | rotulo_no_conjunto: confere |
| 3712 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | fonte_existe_na_biblioteca: confere |
| 3713 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | fonte_existe_na_biblioteca: confere |
| 3714 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | fonte_estava_no_contexto: confere |
| 3715 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | fonte_estava_no_contexto: confere |
| 3716 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | campo_existe_no_caso: nao_se_aplica |
| 3717 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3718 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | notas_nos_verbetes_citados: informativo |
| 3719 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | impacto: nao_verificavel |
| 3720 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | fonte_formato_valido: confere |
| 3721 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | fonte_contem_termo_da_causa: confere |
| 3722 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T02:25:06 | fonte_contem_termo_da_causa: nao_confere |
| 3725 | 27 | inferencia | programa | ao_vivo | 2026-11-05T02:25:06 | intervencao:remocao: 48,7 s |
| 3726 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T02:25:06 | remocao de localizador_quebrado: rótulo localizador_quebrado para estado_da_tela_divergente |
| 3729 | 29 | inferencia | programa | ao_vivo | 2026-11-05T02:25:06 | intervencao:troca: 59,8 s |
| 3730 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T02:25:06 | troca de localizador_quebrado: rótulo localizador_quebrado para estado_da_tela_divergente |
| 3733 | 31 | inferencia | programa | ao_vivo | 2026-11-05T02:25:06 | intervencao:sem_documentacao: 67,1 s |
| 3734 | 32 | intervencao | verificacao | ao_vivo | 2026-11-05T02:25:06 | sem_documentacao de None: rótulo localizador_quebrado para localizador_quebrado |
| 3735 | 33 | inferencia | programa | ao_vivo | 2026-11-05T02:25:06 | intervencao:repeticao_da_base: 18,1 s |
| 3736 | 34 | intervencao | verificacao | ao_vivo | 2026-11-05T02:25:06 | repeticao_da_base de None: rótulo localizador_quebrado para localizador_quebrado |
| 3737 | 35 | decisao | programa | ao_vivo | 2026-11-05T02:25:06 | diagnostico: escolha localizador_quebrado; divergência sim |

</details>

Nós de decisão:

- evento 3697, `poda`: escolha `sem_contrato`; resultado sem_contrato; evidência: evento 3696 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3699, `recuperacao`: escolha `localizador_quebrado,ancora-saiba-mais,estado_da_tela_divergente`; resultado verbetes_entregues; evidência: evento 3698 (verbete_entregue, localizador_quebrado), evento 3698 (verbete_entregue, ancora-saiba-mais), evento 3698 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente (gen_ai: retrieval)
- evento 3737, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 3698 (verbete_entregue, localizador_quebrado), evento 3698 (verbete_entregue, ancora-saiba-mais), evento 3698 (verbete_entregue, estado_da_tela_divergente), evento 3703 (resposta), evento 3708 (verbete_citado, localizador_quebrado), evento 3709 (verbete_citado, ancora-saiba-mais); divergência: sim; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3695 a 3737 da trilha; hash dos eventos deste caso: `8f440ebfd865929f`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
