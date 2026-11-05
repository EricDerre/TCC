<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-11@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-11@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 0,99) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `Alguns nomes vêm corrompidos e com símbolos estranhos, devido a uma codificação incorreta.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque os verbetes entidade-produto, estado_da_tela_divergente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 2062): regras diff_contra_contrato; antes {"chars": 154}, depois {"chars": 154}.

Trecho podado (hash `d4b4394eaa720f08`):

```text
[{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e acucar", "tipo": "Sobremesas", "preco": 14.9, "imagem": "abacaxi.jpg", "destaque": false}]
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não formato_de_data_divergente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: entidade-produto, estado_da_tela_divergente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 0,99 | sim |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [estado_da_tela_divergente]`; verbetes citados: `entidade-produto`, `estado_da_tela_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `estado_da_tela_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `estado_da_tela_divergente`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `estado_da_tela_divergente` | confere | contexto: `entidade-produto`, `estado_da_tela_divergente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[entidade-produto], [estado_da_tela_divergente]` | confere | {"ids": ["entidade-produto", "estado_da_tela_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "codificacao_incorreta"} |
| fonte_contem_termo_da_causa | `estado_da_tela_divergente` | **não confere** | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-11 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2061 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:01:23 | caso lex-11@verbete_trocado |
| 2062 | 2 | poda | programa | ao_vivo | 2026-11-05T01:01:23 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2063 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:01:23 | poda: escolha json/lista; sem diferença; divergência não |
| 2064 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:01:23 | 3 de 39 verbetes entregues |
| 2065 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:01:23 | recuperacao: escolha entidade-produto,estado_da_tela_divergente,contrato-produto; divergência não |
| 2066 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:01:23 | {"etapa": "diagnostico", "sha": "96aa6d392e468ebe", "prompt_sha256": "96aa6d392e46", "chars": 3594, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2068 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:01:23 | diagnostico: 18,4 s |
| 2069 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:01:23 | causa_raiz: `codificacao_incorreta` |
| 2070 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:01:23 | campo: `nome` |
| 2071 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:01:23 | impacto: `Alguns nomes vêm corrompidos e com símbolos estranhos, devido a uma codificação incorreta.` |
| 2072 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:01:23 | fonte: `[entidade-produto], [estado_da_tela_divergente]` |
| 2073 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:01:23 | fonte_citada: `entidade-produto` |
| 2074 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T01:01:23 | fonte_citada: `estado_da_tela_divergente` |
| 2075 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | quatro_linhas_presentes: confere |
| 2076 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | rotulo_no_conjunto: confere |
| 2077 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | fonte_existe_na_biblioteca: confere |
| 2078 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | fonte_existe_na_biblioteca: confere |
| 2079 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | fonte_estava_no_contexto: confere |
| 2080 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | fonte_estava_no_contexto: confere |
| 2081 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | campo_existe_no_caso: confere |
| 2082 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2083 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | notas_nos_verbetes_citados: informativo |
| 2084 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | impacto: nao_verificavel |
| 2085 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | fonte_formato_valido: confere |
| 2086 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | fonte_contem_termo_da_causa: nao_confere |
| 2087 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T01:01:23 | fonte_contem_termo_da_causa: nao_confere |
| 2088 | 27 | decisao | programa | ao_vivo | 2026-11-05T01:01:23 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 2063, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 2062 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 2065, `recuperacao`: escolha `entidade-produto,estado_da_tela_divergente,contrato-produto`; resultado verbetes_entregues; evidência: evento 2064 (verbete_entregue, entidade-produto), evento 2064 (verbete_entregue, estado_da_tela_divergente), evento 2064 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, estado_da_tela_divergente, contrato-produto (gen_ai: retrieval)
- evento 2088, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 2064 (verbete_entregue, entidade-produto), evento 2064 (verbete_entregue, estado_da_tela_divergente), evento 2064 (verbete_entregue, contrato-produto), evento 2068 (resposta), evento 2073 (verbete_citado, entidade-produto), evento 2074 (verbete_citado, estado_da_tela_divergente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, estado_da_tela_divergente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2061 a 2088 da trilha; hash dos eventos deste caso: `efe32c4cb1304551`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
