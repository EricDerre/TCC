<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-7@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-7@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,94)

**IMPACTO (declarado):** `O usuário não consegue acessar o detalhe do produto ao clicar em "Saiba Mais...", resultando em uma experiência interrompida.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente estavam entre os entregues ao modelo. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 3646): regras diff_contra_contrato; antes {"chars": 27}, depois {"chars": 27}.

Trecho podado (hash `48ffb95010655367`):

```text
(nenhuma requisicao falhou)
```

## 3. Contraste com a segunda causa

localizador_quebrado sem alternativa registrada no nó

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 0,94 | sim |

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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-7 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3645 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:23:43 | caso efe-7@sonda |
| 3646 | 2 | poda | programa | ao_vivo | 2026-11-05T02:23:43 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3647 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:23:43 | poda: escolha sem_contrato; divergência não |
| 3648 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:23:43 | 3 de 39 verbetes entregues |
| 3649 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:23:43 | recuperacao: escolha localizador_quebrado,ancora-saiba-mais,estado_da_tela_divergente; divergência não |
| 3651 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:23:43 | {"etapa": "diagnostico", "sha": "ea229b96d41564a4", "prompt_sha256": "ea229b96d415", "chars": 3971, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3653 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:23:43 | diagnostico: 56,8 s |
| 3654 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:23:43 | causa_raiz: `localizador_quebrado` |
| 3655 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:23:43 | campo: `nenhum` |
| 3656 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:23:43 | impacto: `O usuário não consegue acessar o detalhe do produto ao clicar em "Saiba Mais...", resultando em uma experiência interrompida.` |
| 3657 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:23:43 | fonte: `[localizador_quebrado]` |
| 3658 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:23:43 | fonte_citada: `localizador_quebrado` |
| 3659 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:23:43 | quatro_linhas_presentes: confere |
| 3660 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:23:43 | rotulo_no_conjunto: confere |
| 3661 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:23:43 | fonte_existe_na_biblioteca: confere |
| 3662 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:23:43 | fonte_estava_no_contexto: confere |
| 3663 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:23:43 | campo_existe_no_caso: nao_se_aplica |
| 3664 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:23:43 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3665 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:23:43 | notas_nos_verbetes_citados: informativo |
| 3666 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:23:43 | impacto: nao_verificavel |
| 3667 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:23:43 | fonte_formato_valido: confere |
| 3668 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:23:43 | fonte_contem_termo_da_causa: confere |
| 3669 | 23 | decisao | programa | ao_vivo | 2026-11-05T02:23:43 | diagnostico: escolha localizador_quebrado; divergência não |

</details>

Nós de decisão:

- evento 3647, `poda`: escolha `sem_contrato`; resultado sem_contrato; evidência: evento 3646 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3649, `recuperacao`: escolha `localizador_quebrado,ancora-saiba-mais,estado_da_tela_divergente`; resultado verbetes_entregues; evidência: evento 3648 (verbete_entregue, localizador_quebrado), evento 3648 (verbete_entregue, ancora-saiba-mais), evento 3648 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente (gen_ai: retrieval)
- evento 3669, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 3648 (verbete_entregue, localizador_quebrado), evento 3648 (verbete_entregue, ancora-saiba-mais), evento 3648 (verbete_entregue, estado_da_tela_divergente), evento 3653 (resposta), evento 3658 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3645 a 3669 da trilha; hash dos eventos deste caso: `837e91b45be9352e`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
