<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-4@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-4@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `Os nomes dos produtos aparecem com caracteres estranhos nos cartões.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque os verbetes entidade-produto, contrato-produto, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 137): regras diff_contra_contrato; antes {"chars": 156}, depois {"chars": 156}.

Trecho podado (hash `53a0170337e1ff5e`):

```text
[{"id": 12, "nome": "Queijo Coalho com P\u00c3\u00a3o", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true, "resumo": null}]
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto]`; verbetes citados: `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[entidade-produto]` | confere | {"ids": ["entidade-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | confere | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-4 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 136 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:09:44 | caso lex-4@sonda |
| 137 | 2 | poda | programa | ao_vivo | 2026-11-04T23:09:44 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 138 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:09:44 | poda: escolha json/lista; sem diferença; divergência não |
| 139 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:09:44 | 3 de 39 verbetes entregues |
| 140 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:09:44 | recuperacao: escolha entidade-produto,contrato-produto,estado_da_tela_divergente; divergência não |
| 142 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:09:44 | {"etapa": "diagnostico", "sha": "7516a8f9f4f7e55a", "prompt_sha256": "7516a8f9f4f7", "chars": 3620, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 143 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:09:44 | diagnostico: 64,4 s |
| 144 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:09:44 | causa_raiz: `codificacao_incorreta` |
| 145 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:09:44 | campo: `nome` |
| 146 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:09:44 | impacto: `Os nomes dos produtos aparecem com caracteres estranhos nos cartões.` |
| 147 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:09:44 | fonte: `[entidade-produto]` |
| 148 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:09:44 | fonte_citada: `entidade-produto` |
| 149 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:09:44 | quatro_linhas_presentes: confere |
| 150 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:09:44 | rotulo_no_conjunto: confere |
| 151 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:09:44 | fonte_existe_na_biblioteca: confere |
| 152 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:09:44 | fonte_estava_no_contexto: confere |
| 153 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:09:44 | campo_existe_no_caso: confere |
| 154 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:09:44 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 155 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:09:44 | notas_nos_verbetes_citados: informativo |
| 156 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:09:44 | impacto: nao_verificavel |
| 157 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:09:44 | fonte_formato_valido: confere |
| 158 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:09:44 | fonte_contem_termo_da_causa: confere |
| 159 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:09:44 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 138, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 137 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 140, `recuperacao`: escolha `entidade-produto,contrato-produto,estado_da_tela_divergente`; resultado verbetes_entregues; evidência: evento 139 (verbete_entregue, entidade-produto), evento 139 (verbete_entregue, contrato-produto), evento 139 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, estado_da_tela_divergente (gen_ai: retrieval)
- evento 159, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 139 (verbete_entregue, entidade-produto), evento 139 (verbete_entregue, contrato-produto), evento 139 (verbete_entregue, estado_da_tela_divergente), evento 143 (resposta), evento 148 (verbete_citado, entidade-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 136 a 159 da trilha; hash dos eventos deste caso: `c99c06a2c8d0e046`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
