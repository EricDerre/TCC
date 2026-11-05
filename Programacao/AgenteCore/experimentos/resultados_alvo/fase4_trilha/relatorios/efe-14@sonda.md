<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-14@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-14@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O roteiro não acha o elemento correto, encontrando mais de um ou nenhum, o que causa falhas aleatórias no funcionamento do sistema.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, nulo_inesperado, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 3739): regras diff_contra_contrato; antes {"chars": 27}, depois {"chars": 27}.

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
| estado_da_tela_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `ancora-saiba-mais`, `estado_da_tela_divergente` |
| fonte_formato_valido | `[localizador_quebrado]` | confere | {"ids": ["localizador_quebrado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-14 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3738 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:29:10 | caso efe-14@sonda |
| 3739 | 2 | poda | programa | ao_vivo | 2026-11-05T02:29:10 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3740 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:29:10 | poda: escolha sem_contrato; divergência não |
| 3741 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:29:10 | 3 de 39 verbetes entregues |
| 3742 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:29:10 | recuperacao: escolha localizador_quebrado,ancora-saiba-mais,estado_da_tela_divergente; divergência não |
| 3744 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:29:10 | {"etapa": "diagnostico", "sha": "12eca715bb4a4829", "prompt_sha256": "12eca715bb4a", "chars": 4083, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3746 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:29:10 | diagnostico: 59,8 s |
| 3747 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:29:10 | causa_raiz: `localizador_quebrado` |
| 3748 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:29:10 | campo: `nenhum` |
| 3749 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:29:10 | impacto: `O roteiro não acha o elemento correto, encontrando mais de um ou nenhum, o que causa falhas aleatórias no funcionamento do sistema.` |
| 3750 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:29:10 | fonte: `[localizador_quebrado]` |
| 3751 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:29:10 | fonte_citada: `localizador_quebrado` |
| 3752 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:29:10 | quatro_linhas_presentes: confere |
| 3753 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:29:10 | rotulo_no_conjunto: confere |
| 3754 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:29:10 | fonte_existe_na_biblioteca: confere |
| 3755 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:29:10 | fonte_estava_no_contexto: confere |
| 3756 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:29:10 | campo_existe_no_caso: nao_se_aplica |
| 3757 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:29:10 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3758 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:29:10 | notas_nos_verbetes_citados: informativo |
| 3759 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:29:10 | impacto: nao_verificavel |
| 3760 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:29:10 | fonte_formato_valido: confere |
| 3761 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:29:10 | fonte_contem_termo_da_causa: confere |
| 3762 | 23 | decisao | programa | ao_vivo | 2026-11-05T02:29:10 | diagnostico: escolha localizador_quebrado; divergência não |

</details>

Nós de decisão:

- evento 3740, `poda`: escolha `sem_contrato`; resultado sem_contrato; evidência: evento 3739 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3742, `recuperacao`: escolha `localizador_quebrado,ancora-saiba-mais,estado_da_tela_divergente`; resultado verbetes_entregues; evidência: evento 3741 (verbete_entregue, localizador_quebrado), evento 3741 (verbete_entregue, ancora-saiba-mais), evento 3741 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente (gen_ai: retrieval)
- evento 3762, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 3741 (verbete_entregue, localizador_quebrado), evento 3741 (verbete_entregue, ancora-saiba-mais), evento 3741 (verbete_entregue, estado_da_tela_divergente), evento 3746 (resposta), evento 3751 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3738 a 3762 da trilha; hash dos eventos deste caso: `484160b6ad886c28`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
