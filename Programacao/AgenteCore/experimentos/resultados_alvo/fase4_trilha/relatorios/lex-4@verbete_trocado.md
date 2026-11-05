<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-4@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-4@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `Os nomes dos produtos aparecem com caracteres estranhos nos cartões.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque os verbetes entidade-produto, nulo_inesperado, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 161): regras diff_contra_contrato; antes {"chars": 156}, depois {"chars": 156}.

Trecho podado (hash `53a0170337e1ff5e`):

```text
[{"id": 12, "nome": "Queijo Coalho com P\u00c3\u00a3o", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true, "resumo": null}]
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não formato_de_data_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, nulo_inesperado, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 1,00 | sim |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `entidade-produto`, `nulo_inesperado`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"ids": ["nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | **não confere** | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-4 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 160 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:10:53 | caso lex-4@verbete_trocado |
| 161 | 2 | poda | programa | ao_vivo | 2026-11-04T23:10:53 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 162 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:10:53 | poda: escolha json/lista; sem diferença; divergência não |
| 163 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:10:53 | 3 de 39 verbetes entregues |
| 164 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:10:53 | recuperacao: escolha entidade-produto,nulo_inesperado,estado_da_tela_divergente; divergência não |
| 165 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:10:53 | {"etapa": "diagnostico", "sha": "0b04f03d8460fd2a", "prompt_sha256": "0b04f03d8460", "chars": 3341, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 167 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:10:53 | diagnostico: 13,3 s |
| 168 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:10:53 | causa_raiz: `codificacao_incorreta` |
| 169 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:10:53 | campo: `nome` |
| 170 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:10:53 | impacto: `Os nomes dos produtos aparecem com caracteres estranhos nos cartões.` |
| 171 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:10:53 | fonte: `[nulo_inesperado]` |
| 172 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:10:53 | fonte_citada: `nulo_inesperado` |
| 173 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:10:53 | quatro_linhas_presentes: confere |
| 174 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:10:53 | rotulo_no_conjunto: confere |
| 175 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:10:53 | fonte_existe_na_biblioteca: confere |
| 176 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:10:53 | fonte_estava_no_contexto: confere |
| 177 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:10:53 | campo_existe_no_caso: confere |
| 178 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:10:53 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 179 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:10:53 | notas_nos_verbetes_citados: informativo |
| 180 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:10:53 | impacto: nao_verificavel |
| 181 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:10:53 | fonte_formato_valido: confere |
| 182 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:10:53 | fonte_contem_termo_da_causa: nao_confere |
| 183 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:10:53 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 162, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 161 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 164, `recuperacao`: escolha `entidade-produto,nulo_inesperado,estado_da_tela_divergente`; resultado verbetes_entregues; evidência: evento 163 (verbete_entregue, entidade-produto), evento 163 (verbete_entregue, nulo_inesperado), evento 163 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, nulo_inesperado, estado_da_tela_divergente (gen_ai: retrieval)
- evento 183, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 163 (verbete_entregue, entidade-produto), evento 163 (verbete_entregue, nulo_inesperado), evento 163 (verbete_entregue, estado_da_tela_divergente), evento 167 (resposta), evento 172 (verbete_citado, nulo_inesperado); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, nulo_inesperado, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 160 a 183 da trilha; hash dos eventos deste caso: `16fb49735635ec7b`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
