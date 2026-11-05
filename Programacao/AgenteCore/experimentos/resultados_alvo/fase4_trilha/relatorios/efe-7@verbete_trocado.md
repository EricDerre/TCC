<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-7@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-7@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,89)

**IMPACTO (declarado):** `O usuário não consegue acessar o detalhe do produto, vendo apenas o texto "Saiba Mais..." inativo.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes tempo_de_resposta_excedido, ancora-saiba-mais, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, estado_da_tela_divergente, ficou com probabilidade 0,06. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 3671): regras diff_contra_contrato; antes {"chars": 27}, depois {"chars": 27}.

Trecho podado (hash `48ffb95010655367`):

```text
(nenhuma requisicao falhou)
```

## 3. Contraste com a segunda causa

localizador_quebrado e não estado_da_tela_divergente: a escolha tem probabilidade 0,89 contra 0,06; verbete(s) na evidência: tempo_de_resposta_excedido, ancora-saiba-mais, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 0,89 | sim |
| estado_da_tela_divergente | 0,06 |  |
| nulo_inesperado | 0,01 |  |
| escala_ou_unidade_errada | 0,00 |  |
| tempo_de_resposta_excedido | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| limite_de_requisicoes | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[ancora-saiba-mais]`; verbetes citados: `ancora-saiba-mais`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `ancora-saiba-mais` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `ancora-saiba-mais` | confere | contexto: `tempo_de_resposta_excedido`, `ancora-saiba-mais`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `ancora-saiba-mais`, `estado_da_tela_divergente` |
| fonte_formato_valido | `[ancora-saiba-mais]` | confere | {"ids": ["ancora-saiba-mais"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `ancora-saiba-mais` | **não confere** | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-7 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3670 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:24:43 | caso efe-7@verbete_trocado |
| 3671 | 2 | poda | programa | ao_vivo | 2026-11-05T02:24:43 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3672 | 3 | decisao | programa | ao_vivo | 2026-11-05T02:24:43 | poda: escolha sem_contrato; divergência não |
| 3673 | 4 | candidatos | programa | ao_vivo | 2026-11-05T02:24:43 | 3 de 39 verbetes entregues |
| 3674 | 5 | decisao | programa | ao_vivo | 2026-11-05T02:24:43 | recuperacao: escolha tempo_de_resposta_excedido,ancora-saiba-mais,estado_da_tela_divergente; divergência não |
| 3675 | 6 | prompt | programa | ao_vivo | 2026-11-05T02:24:43 | {"etapa": "diagnostico", "sha": "5d13675ee35b4fc4", "prompt_sha256": "5d13675ee35b", "chars": 3616, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3677 | 7 | inferencia | programa | ao_vivo | 2026-11-05T02:24:43 | diagnostico: 16,1 s |
| 3678 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T02:24:43 | causa_raiz: `localizador_quebrado` |
| 3679 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T02:24:43 | campo: `nenhum` |
| 3680 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T02:24:43 | impacto: `O usuário não consegue acessar o detalhe do produto, vendo apenas o texto "Saiba Mais..." inativo.` |
| 3681 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:24:43 | fonte: `[ancora-saiba-mais]` |
| 3682 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:24:43 | fonte_citada: `ancora-saiba-mais` |
| 3683 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T02:24:43 | quatro_linhas_presentes: confere |
| 3684 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T02:24:43 | rotulo_no_conjunto: confere |
| 3685 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T02:24:43 | fonte_existe_na_biblioteca: confere |
| 3686 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:24:43 | fonte_estava_no_contexto: confere |
| 3687 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:24:43 | campo_existe_no_caso: nao_se_aplica |
| 3688 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:24:43 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3689 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:24:43 | notas_nos_verbetes_citados: informativo |
| 3690 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:24:43 | impacto: nao_verificavel |
| 3691 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:24:43 | fonte_formato_valido: confere |
| 3692 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:24:43 | fonte_contem_termo_da_causa: nao_confere |
| 3693 | 23 | decisao | programa | ao_vivo | 2026-11-05T02:24:43 | diagnostico: escolha localizador_quebrado; divergência não |

</details>

Nós de decisão:

- evento 3672, `poda`: escolha `sem_contrato`; resultado sem_contrato; evidência: evento 3671 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3674, `recuperacao`: escolha `tempo_de_resposta_excedido,ancora-saiba-mais,estado_da_tela_divergente`; resultado verbetes_entregues; evidência: evento 3673 (verbete_entregue, tempo_de_resposta_excedido), evento 3673 (verbete_entregue, ancora-saiba-mais), evento 3673 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: tempo_de_resposta_excedido, ancora-saiba-mais, estado_da_tela_divergente (gen_ai: retrieval)
- evento 3693, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 3673 (verbete_entregue, tempo_de_resposta_excedido), evento 3673 (verbete_entregue, ancora-saiba-mais), evento 3673 (verbete_entregue, estado_da_tela_divergente), evento 3677 (resposta), evento 3682 (verbete_citado, ancora-saiba-mais); divergência: não; falha: nenhuma; prov.used: tempo_de_resposta_excedido, ancora-saiba-mais, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3670 a 3693 da trilha; hash dos eventos deste caso: `bced842fdd88d99e`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
