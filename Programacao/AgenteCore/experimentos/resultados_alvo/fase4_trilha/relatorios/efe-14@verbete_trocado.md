<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-14@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-14@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estado_da_tela_divergente` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,78)

**IMPACTO (declarado):** `O usuário vê um botão "Saiba Mais..." inativo, mesmo após clicar nele, pois o estado da tela não foi atualizado corretamente.`

Justificativa (gerada por molde): O agente respondeu estado_da_tela_divergente porque os verbetes corpo_vazio, ancora-saiba-mais, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,16. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,78); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 3764): regras diff_contra_contrato; antes {"chars": 27}, depois {"chars": 27}.

Trecho podado (hash `48ffb95010655367`):

```text
(nenhuma requisicao falhou)
```

## 3. Contraste com a segunda causa

estado_da_tela_divergente e não corpo_nao_e_json: a escolha tem probabilidade 0,78 contra 0,16; verbete(s) na evidência: corpo_vazio, ancora-saiba-mais, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estado_da_tela_divergente | 0,78 | sim |
| corpo_nao_e_json | 0,16 |  |
| corpo_vazio | 0,16 |  |
| resposta_truncada | 0,04 |  |
| nulo_inesperado | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| localizador_quebrado | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[estado_da_tela_divergente]`; verbetes citados: `estado_da_tela_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estado_da_tela_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estado_da_tela_divergente` | confere | contexto: `corpo_vazio`, `ancora-saiba-mais`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `estado_da_tela_divergente` | confere | verbetes: `corpo_vazio`, `ancora-saiba-mais`, `estado_da_tela_divergente` |
| fonte_formato_valido | `[estado_da_tela_divergente]` | confere | {"ids": ["estado_da_tela_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `estado_da_tela_divergente` | confere | {"termo": "estado_da_tela_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-14 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3763 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:30:14 | caso efe-14@verbete_trocado |
| 3764 | 2 | poda | programa | ao_vivo | 2026-11-05T02:30:14 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3765 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:30:14 | poda: escolha sem_contrato; divergência não |
| 3766 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:30:14 | 3 de 39 verbetes entregues |
| 3767 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:30:14 | recuperacao: escolha corpo_vazio,ancora-saiba-mais,estado_da_tela_divergente; divergência não |
| 3768 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:30:14 | {"etapa": "diagnostico", "sha": "a7af24f14b31c39a", "prompt_sha256": "a7af24f14b31", "chars": 3866, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3770 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:30:14 | diagnostico: 20,0 s |
| 3771 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:30:14 | causa_raiz: `estado_da_tela_divergente` |
| 3772 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:30:14 | campo: `nenhum` |
| 3773 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:30:14 | impacto: `O usuário vê um botão "Saiba Mais..." inativo, mesmo após clicar nele, pois o estado da tela não foi atualizado corretamente.` |
| 3774 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:30:14 | fonte: `[estado_da_tela_divergente]` |
| 3775 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:30:14 | fonte_citada: `estado_da_tela_divergente` |
| 3776 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:30:14 | quatro_linhas_presentes: confere |
| 3777 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:30:14 | rotulo_no_conjunto: confere |
| 3778 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:30:14 | fonte_existe_na_biblioteca: confere |
| 3779 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:30:14 | fonte_estava_no_contexto: confere |
| 3780 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:30:14 | campo_existe_no_caso: nao_se_aplica |
| 3781 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:30:14 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3782 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:30:14 | notas_nos_verbetes_citados: informativo |
| 3783 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:30:14 | impacto: nao_verificavel |
| 3784 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:30:14 | fonte_formato_valido: confere |
| 3785 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:30:14 | fonte_contem_termo_da_causa: confere |
| 3786 | 23 | decisao | programa | ao_vivo | 2026-11-05T02:30:14 | diagnostico: escolha estado_da_tela_divergente; divergência não |

</details>

Nós de decisão:

- evento 3765, `poda`: escolha `sem_contrato`; resultado sem_contrato; evidência: evento 3764 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3767, `recuperacao`: escolha `corpo_vazio,ancora-saiba-mais,estado_da_tela_divergente`; resultado verbetes_entregues; evidência: evento 3766 (verbete_entregue, corpo_vazio), evento 3766 (verbete_entregue, ancora-saiba-mais), evento 3766 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: corpo_vazio, ancora-saiba-mais, estado_da_tela_divergente (gen_ai: retrieval)
- evento 3786, `diagnostico`: escolha `estado_da_tela_divergente`; resultado rotulo_emitido; evidência: evento 3766 (verbete_entregue, corpo_vazio), evento 3766 (verbete_entregue, ancora-saiba-mais), evento 3766 (verbete_entregue, estado_da_tela_divergente), evento 3770 (resposta), evento 3775 (verbete_citado, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: corpo_vazio, ancora-saiba-mais, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3763 a 3786 da trilha; hash dos eventos deste caso: `5fb87578894d91eb`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
