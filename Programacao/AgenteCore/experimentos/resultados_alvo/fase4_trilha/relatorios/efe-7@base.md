<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-7`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-7@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,93)

**IMPACTO (declarado):** `O usuário não consegue acessar o detalhe do produto, vendo apenas o texto "Saiba Mais..." inativo.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente estavam entre os entregues ao modelo. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete localizador_quebrado não mudou a resposta: sem efeito medido do contexto. A troca do verbete localizador_quebrado por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 3607): regras diff_contra_contrato; antes {"chars": 27}, depois {"chars": 27}.

Trecho podado (hash `48ffb95010655367`):

```text
(nenhuma requisicao falhou)
```

## 3. Contraste com a segunda causa

localizador_quebrado sem alternativa registrada no nó

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 0,93 | sim |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `ancora-saiba-mais`, `estado_da_tela_divergente` |
| fonte_formato_valido | `[localizador_quebrado]` | confere | {"ids": ["localizador_quebrado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `localizador_quebrado` | localizador_quebrado | localizador_quebrado | 0,93 | 0,99 | sem efeito medido do contexto |
| troca | `localizador_quebrado` | localizador_quebrado | localizador_quebrado | 0,93 | 0,91 | sem efeito medido do contexto |
| sem_documentacao | `` | localizador_quebrado | localizador_quebrado | 0,93 | 1,00 | sem efeito medido do contexto |
| repeticao_da_base | `` | localizador_quebrado | localizador_quebrado | 0,93 | 0,96 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-7 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3606 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:19:39 | caso efe-7 |
| 3607 | 2 | poda | programa | ao_vivo | 2026-11-05T02:19:39 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3608 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:19:39 | poda: escolha sem_contrato; divergência não |
| 3609 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:19:39 | 3 de 39 verbetes entregues |
| 3610 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:19:39 | recuperacao: escolha localizador_quebrado,ancora-saiba-mais,estado_da_tela_divergente; divergência não |
| 3612 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:19:39 | {"etapa": "diagnostico", "sha": "64ec58ec3596ebbb", "prompt_sha256": "64ec58ec3596", "chars": 3853, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3614 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:19:39 | diagnostico: 55,8 s |
| 3615 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:19:39 | causa_raiz: `localizador_quebrado` |
| 3616 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:19:39 | campo: `nenhum` |
| 3617 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:19:39 | impacto: `O usuário não consegue acessar o detalhe do produto, vendo apenas o texto "Saiba Mais..." inativo.` |
| 3618 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:19:39 | fonte: `[localizador_quebrado]` |
| 3619 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:19:39 | fonte_citada: `localizador_quebrado` |
| 3620 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:39 | quatro_linhas_presentes: confere |
| 3621 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:39 | rotulo_no_conjunto: confere |
| 3622 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:39 | fonte_existe_na_biblioteca: confere |
| 3623 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:39 | fonte_estava_no_contexto: confere |
| 3624 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:39 | campo_existe_no_caso: nao_se_aplica |
| 3625 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:39 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3626 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:39 | notas_nos_verbetes_citados: informativo |
| 3627 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:39 | impacto: nao_verificavel |
| 3628 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:39 | fonte_formato_valido: confere |
| 3629 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:19:39 | fonte_contem_termo_da_causa: confere |
| 3632 | 23 | inferencia | programa | ao_vivo | 2026-11-05T02:19:39 | intervencao:remocao: 67,0 s |
| 3633 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T02:19:39 | remocao de localizador_quebrado: rótulo localizador_quebrado para localizador_quebrado |
| 3636 | 25 | inferencia | programa | ao_vivo | 2026-11-05T02:19:39 | intervencao:troca: 57,8 s |
| 3637 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T02:19:39 | troca de localizador_quebrado: rótulo localizador_quebrado para localizador_quebrado |
| 3640 | 27 | inferencia | programa | ao_vivo | 2026-11-05T02:19:39 | intervencao:sem_documentacao: 43,2 s |
| 3641 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T02:19:39 | sem_documentacao de None: rótulo localizador_quebrado para localizador_quebrado |
| 3642 | 29 | inferencia | programa | ao_vivo | 2026-11-05T02:19:39 | intervencao:repeticao_da_base: 15,8 s |
| 3643 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T02:19:39 | repeticao_da_base de None: rótulo localizador_quebrado para localizador_quebrado |
| 3644 | 31 | decisao | programa | ao_vivo | 2026-11-05T02:19:39 | diagnostico: escolha localizador_quebrado; divergência não |

</details>

Nós de decisão:

- evento 3608, `poda`: escolha `sem_contrato`; resultado sem_contrato; evidência: evento 3607 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3610, `recuperacao`: escolha `localizador_quebrado,ancora-saiba-mais,estado_da_tela_divergente`; resultado verbetes_entregues; evidência: evento 3609 (verbete_entregue, localizador_quebrado), evento 3609 (verbete_entregue, ancora-saiba-mais), evento 3609 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente (gen_ai: retrieval)
- evento 3644, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 3609 (verbete_entregue, localizador_quebrado), evento 3609 (verbete_entregue, ancora-saiba-mais), evento 3609 (verbete_entregue, estado_da_tela_divergente), evento 3614 (resposta), evento 3619 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3606 a 3644 da trilha; hash dos eventos deste caso: `bb5cf2855c96ec49`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
