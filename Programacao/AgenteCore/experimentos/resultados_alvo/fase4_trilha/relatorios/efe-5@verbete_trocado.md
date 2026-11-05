<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-5@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-5@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `seletor_incorreto` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,49) · **CONFLITO**: a causa respondida seletor_incorreto está fora das 23 permitidas; nenhum verbete entregue trata da causa respondida seletor_incorreto

**IMPACTO (declarado):** `O usuário vê dois botões "Saiba Mais..." em vez de um único botão.`

Justificativa (gerada por molde): O agente respondeu seletor_incorreto porque os verbetes tempo_de_resposta_excedido, ancora-saiba-mais, corpo_nao_e_json estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,38 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a causa respondida seletor_incorreto está fora das 23 permitidas; nenhum verbete entregue trata da causa respondida seletor_incorreto. Este nó está marcado com a falha rotulo_fora_da_taxonomia (origem: modelo). O agente não está seguro desta causa (probabilidade 0,49); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 1664): regras diff_contra_contrato; antes {"chars": 27}, depois {"chars": 27}.

Trecho podado (hash `48ffb95010655367`):

```text
(nenhuma requisicao falhou)
```

## 3. Contraste com a segunda causa

seletor_incorreto e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,49 contra 0,38; verbete(s) na evidência: tempo_de_resposta_excedido, ancora-saiba-mais, corpo_nao_e_json

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| seletor_incorreto | 0,49 | sim |
| estrutura_aninhada_divergente | 0,38 |  |
| colecao_no_lugar_de_objeto | 0,06 |  |
| localizador_quebrado | 0,03 |  |
| registro_duplicado | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| escala_ou_unidade_errada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| limite_de_requisicoes | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[ancora-saiba-mais]`; verbetes citados: `ancora-saiba-mais`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `ancora-saiba-mais` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `ancora-saiba-mais` | confere | contexto: `tempo_de_resposta_excedido`, `ancora-saiba-mais`, `corpo_nao_e_json` |
| Algum verbete do contexto trata da causa respondida | `seletor_incorreto` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[ancora-saiba-mais]` | confere | {"ids": ["ancora-saiba-mais"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `ancora-saiba-mais` | **não confere** | {"termo": "seletor_incorreto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-5 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1663 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:38:59 | caso efe-5@verbete_trocado |
| 1664 | 2 | poda | programa | ao_vivo | 2026-11-05T00:38:59 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1665 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:38:59 | poda: escolha sem_contrato; divergência não |
| 1666 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:38:59 | 3 de 39 verbetes entregues |
| 1667 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:38:59 | recuperacao: escolha tempo_de_resposta_excedido,ancora-saiba-mais,corpo_nao_e_json; divergência não |
| 1668 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:38:59 | {"etapa": "diagnostico", "sha": "bb363fc37e063a70", "prompt_sha256": "bb363fc37e06", "chars": 3809, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1670 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:38:59 | diagnostico: 15,1 s |
| 1671 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:38:59 | causa_raiz: `seletor_incorreto` |
| 1672 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:38:59 | campo: `nenhum` |
| 1673 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:38:59 | impacto: `O usuário vê dois botões "Saiba Mais..." em vez de um único botão.` |
| 1674 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:38:59 | fonte: `[ancora-saiba-mais]` |
| 1675 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:38:59 | fonte_citada: `ancora-saiba-mais` |
| 1676 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:38:59 | quatro_linhas_presentes: confere |
| 1677 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:38:59 | rotulo_no_conjunto: nao_confere |
| 1678 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:38:59 | fonte_existe_na_biblioteca: confere |
| 1679 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:38:59 | fonte_estava_no_contexto: confere |
| 1680 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:38:59 | campo_existe_no_caso: nao_se_aplica |
| 1681 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:38:59 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1682 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:38:59 | notas_nos_verbetes_citados: informativo |
| 1683 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:38:59 | impacto: nao_verificavel |
| 1684 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:38:59 | fonte_formato_valido: confere |
| 1685 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:38:59 | fonte_contem_termo_da_causa: nao_confere |
| 1686 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:38:59 | diagnostico: escolha seletor_incorreto; divergência sim |

</details>

Nós de decisão:

- evento 1665, `poda`: escolha `sem_contrato`; resultado sem_contrato; evidência: evento 1664 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1667, `recuperacao`: escolha `tempo_de_resposta_excedido,ancora-saiba-mais,corpo_nao_e_json`; resultado verbetes_entregues; evidência: evento 1666 (verbete_entregue, tempo_de_resposta_excedido), evento 1666 (verbete_entregue, ancora-saiba-mais), evento 1666 (verbete_entregue, corpo_nao_e_json); divergência: não; falha: nenhuma; prov.used: tempo_de_resposta_excedido, ancora-saiba-mais, corpo_nao_e_json (gen_ai: retrieval)
- evento 1686, `diagnostico`: escolha `seletor_incorreto`; resultado rotulo_emitido; evidência: evento 1666 (verbete_entregue, tempo_de_resposta_excedido), evento 1666 (verbete_entregue, ancora-saiba-mais), evento 1666 (verbete_entregue, corpo_nao_e_json), evento 1670 (resposta), evento 1675 (verbete_citado, ancora-saiba-mais); divergência: sim; falha: rotulo_fora_da_taxonomia; prov.used: tempo_de_resposta_excedido, ancora-saiba-mais, corpo_nao_e_json (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1663 a 1686 da trilha; hash dos eventos deste caso: `3a19c364fc3dc47f`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
