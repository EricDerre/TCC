<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-4`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-4@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `Os nomes dos produtos aparecem com caracteres estranhos nos cartões.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque os verbetes entidade-produto, contrato-produto, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete contrato-produto não mudou a resposta: sem efeito medido do contexto. A troca do verbete contrato-produto por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 99): regras diff_contra_contrato; antes {"chars": 156}, depois {"chars": 156}.

Trecho podado (hash `53a0170337e1ff5e`):

```text
[{"id": 12, "nome": "Queijo Coalho com P\u00c3\u00a3o", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true, "resumo": null}]
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não formato_de_data_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 1,00 | sim |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "codificacao_incorreta"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `contrato-produto` | codificacao_incorreta | codificacao_incorreta | 1,00 | 1,00 | sem efeito medido do contexto |
| troca | `contrato-produto` | codificacao_incorreta | codificacao_incorreta | 1,00 | 1,00 | sem efeito medido do contexto |
| sem_documentacao | `` | codificacao_incorreta | codificacao_incorreta | 1,00 | 1,00 | sem efeito medido do contexto |
| repeticao_da_base | `` | codificacao_incorreta | codificacao_incorreta | 1,00 | 1,00 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-4 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 97 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:06:20 | caso lex-4 |
| 99 | 2 | poda | programa | ao_vivo | 2026-11-04T23:06:20 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 100 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:06:20 | poda: escolha json/lista; sem diferença; divergência não |
| 101 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:06:20 | 3 de 39 verbetes entregues |
| 102 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:06:20 | recuperacao: escolha entidade-produto,contrato-produto,estado_da_tela_divergente; divergência não |
| 104 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:06:20 | {"etapa": "diagnostico", "sha": "6c3456ef7eaeda12", "prompt_sha256": "6c3456ef7eae", "chars": 3501, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 106 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:06:20 | diagnostico: 47,9 s |
| 107 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:06:20 | causa_raiz: `codificacao_incorreta` |
| 108 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:06:20 | campo: `nome` |
| 109 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:06:20 | impacto: `Os nomes dos produtos aparecem com caracteres estranhos nos cartões.` |
| 110 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:06:20 | fonte: `[contrato-produto]` |
| 111 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:06:20 | fonte_citada: `contrato-produto` |
| 112 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:06:20 | quatro_linhas_presentes: confere |
| 113 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:06:20 | rotulo_no_conjunto: confere |
| 114 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:06:20 | fonte_existe_na_biblioteca: confere |
| 115 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:06:20 | fonte_estava_no_contexto: confere |
| 116 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:06:20 | campo_existe_no_caso: confere |
| 117 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:06:20 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 118 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:06:20 | notas_nos_verbetes_citados: informativo |
| 119 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:06:20 | impacto: nao_verificavel |
| 120 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:06:20 | fonte_formato_valido: confere |
| 121 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:06:20 | fonte_contem_termo_da_causa: nao_confere |
| 124 | 23 | inferencia | programa | ao_vivo | 2026-11-04T23:06:20 | intervencao:remocao: 50,4 s |
| 125 | 24 | intervencao | verificacao | ao_vivo | 2026-11-04T23:06:20 | remocao de contrato-produto: rótulo codificacao_incorreta para codificacao_incorreta |
| 127 | 25 | inferencia | programa | ao_vivo | 2026-11-04T23:06:20 | intervencao:troca: 55,8 s |
| 128 | 26 | intervencao | verificacao | ao_vivo | 2026-11-04T23:06:20 | troca de contrato-produto: rótulo codificacao_incorreta para codificacao_incorreta |
| 131 | 27 | inferencia | programa | ao_vivo | 2026-11-04T23:06:20 | intervencao:sem_documentacao: 32,3 s |
| 132 | 28 | intervencao | verificacao | ao_vivo | 2026-11-04T23:06:20 | sem_documentacao de None: rótulo codificacao_incorreta para codificacao_incorreta |
| 133 | 29 | inferencia | programa | ao_vivo | 2026-11-04T23:06:20 | intervencao:repeticao_da_base: 13,4 s |
| 134 | 30 | intervencao | verificacao | ao_vivo | 2026-11-04T23:06:20 | repeticao_da_base de None: rótulo codificacao_incorreta para codificacao_incorreta |
| 135 | 31 | decisao | programa | ao_vivo | 2026-11-04T23:06:20 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 100, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 99 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 102, `recuperacao`: escolha `entidade-produto,contrato-produto,estado_da_tela_divergente`; resultado verbetes_entregues; evidência: evento 101 (verbete_entregue, entidade-produto), evento 101 (verbete_entregue, contrato-produto), evento 101 (verbete_entregue, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, estado_da_tela_divergente (gen_ai: retrieval)
- evento 135, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 101 (verbete_entregue, entidade-produto), evento 101 (verbete_entregue, contrato-produto), evento 101 (verbete_entregue, estado_da_tela_divergente), evento 106 (resposta), evento 111 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 97 a 135 da trilha; hash dos eventos deste caso: `08e7789f14447af3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
