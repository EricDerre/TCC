<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-11`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-11@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `Alguns nomes vêm corrompidos com símbolos, devido a conversão de codificação duas vezes.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque os verbetes entidade-produto, codificacao_incorreta, contrato-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete codificacao_incorreta não mudou a resposta: sem efeito medido do contexto. A troca do verbete codificacao_incorreta por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1997): regras diff_contra_contrato; antes {"chars": 154}, depois {"chars": 154}.

Trecho podado (hash `d4b4394eaa720f08`):

```text
[{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e acucar", "tipo": "Sobremesas", "preco": 14.9, "imagem": "abacaxi.jpg", "destaque": false}]
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, codificacao_incorreta, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[codificacao_incorreta]`; verbetes citados: `codificacao_incorreta`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `codificacao_incorreta` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `codificacao_incorreta` | confere | contexto: `entidade-produto`, `codificacao_incorreta`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | confere | verbetes: `codificacao_incorreta` |
| fonte_formato_valido | `[codificacao_incorreta]` | confere | {"ids": ["codificacao_incorreta"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `codificacao_incorreta` | confere | {"termo": "codificacao_incorreta"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `codificacao_incorreta` | codificacao_incorreta | codificacao_incorreta | 1,00 | 0,93 | sem efeito medido do contexto |
| troca | `codificacao_incorreta` | codificacao_incorreta | codificacao_incorreta | 1,00 | 0,99 | sem efeito medido do contexto |
| sem_documentacao | `` | codificacao_incorreta | codificacao_incorreta | 1,00 | 1,00 | sem efeito medido do contexto |
| repeticao_da_base | `` | codificacao_incorreta | codificacao_incorreta | 1,00 | 1,00 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-11 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1995 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:56:44 | caso lex-11 |
| 1997 | 2 | poda | programa | ao_vivo | 2026-11-05T00:56:44 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1998 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:56:44 | poda: escolha json/lista; sem diferença; divergência não |
| 1999 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:56:44 | 3 de 39 verbetes entregues |
| 2000 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:56:44 | recuperacao: escolha entidade-produto,codificacao_incorreta,contrato-produto; divergência não |
| 2002 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:56:44 | {"etapa": "diagnostico", "sha": "2893e22bc2f80e63", "prompt_sha256": "2893e22bc2f8", "chars": 3495, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2004 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:56:44 | diagnostico: 59,6 s |
| 2005 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:56:44 | causa_raiz: `codificacao_incorreta` |
| 2006 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:56:44 | campo: `nome` |
| 2007 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:56:44 | impacto: `Alguns nomes vêm corrompidos com símbolos, devido a conversão de codificação duas vezes.` |
| 2008 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:56:44 | fonte: `[codificacao_incorreta]` |
| 2009 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:56:44 | fonte_citada: `codificacao_incorreta` |
| 2010 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:44 | quatro_linhas_presentes: confere |
| 2011 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:44 | rotulo_no_conjunto: confere |
| 2012 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:44 | fonte_existe_na_biblioteca: confere |
| 2013 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:44 | fonte_estava_no_contexto: confere |
| 2014 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:44 | campo_existe_no_caso: confere |
| 2015 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:44 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2016 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:44 | notas_nos_verbetes_citados: informativo |
| 2017 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:44 | impacto: nao_verificavel |
| 2018 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:44 | fonte_formato_valido: confere |
| 2019 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:56:44 | fonte_contem_termo_da_causa: confere |
| 2022 | 23 | inferencia | programa | ao_vivo | 2026-11-05T00:56:44 | intervencao:remocao: 37,6 s |
| 2023 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T00:56:44 | remocao de codificacao_incorreta: rótulo codificacao_incorreta para codificacao_incorreta |
| 2026 | 25 | inferencia | programa | ao_vivo | 2026-11-05T00:56:44 | intervencao:troca: 42,2 s |
| 2027 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T00:56:44 | troca de codificacao_incorreta: rótulo codificacao_incorreta para codificacao_incorreta |
| 2030 | 27 | inferencia | programa | ao_vivo | 2026-11-05T00:56:44 | intervencao:sem_documentacao: 41,9 s |
| 2031 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T00:56:44 | sem_documentacao de None: rótulo codificacao_incorreta para codificacao_incorreta |
| 2033 | 29 | inferencia | programa | ao_vivo | 2026-11-05T00:56:44 | intervencao:repeticao_da_base: 15,8 s |
| 2034 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T00:56:44 | repeticao_da_base de None: rótulo codificacao_incorreta para codificacao_incorreta |
| 2035 | 31 | decisao | programa | ao_vivo | 2026-11-05T00:56:44 | diagnostico: escolha codificacao_incorreta; divergência não |

</details>

Nós de decisão:

- evento 1998, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 1997 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 2000, `recuperacao`: escolha `entidade-produto,codificacao_incorreta,contrato-produto`; resultado verbetes_entregues; evidência: evento 1999 (verbete_entregue, entidade-produto), evento 1999 (verbete_entregue, codificacao_incorreta), evento 1999 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, codificacao_incorreta, contrato-produto (gen_ai: retrieval)
- evento 2035, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 1999 (verbete_entregue, entidade-produto), evento 1999 (verbete_entregue, codificacao_incorreta), evento 1999 (verbete_entregue, contrato-produto), evento 2004 (resposta), evento 2009 (verbete_citado, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: entidade-produto, codificacao_incorreta, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1995 a 2035 da trilha; hash dos eventos deste caso: `546a11cee170bbb0`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
