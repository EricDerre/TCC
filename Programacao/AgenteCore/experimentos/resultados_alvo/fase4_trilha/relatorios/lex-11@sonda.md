<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-11@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-11@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `Alguns nomes dos produtos aparecem corrompidos com símbolos, enquanto outros são exibidos corretamente.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque os verbetes entidade-produto, codificacao_incorreta, contrato-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 2037): regras diff_contra_contrato; antes {"chars": 154}, depois {"chars": 154}.

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
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[codificacao_incorreta]`; verbetes citados: `codificacao_incorreta`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `codificacao_incorreta` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `codificacao_incorreta` | confere | contexto: `entidade-produto`, `codificacao_incorreta`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | confere | verbetes: `codificacao_incorreta` |
| fonte_formato_valido | `[codificacao_incorreta]` | confere | {"ids": ["codificacao_incorreta"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `codificacao_incorreta` | confere | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-11 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2036 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:00:06 | caso lex-11@sonda |
| 2037 | 2 | poda | programa | ao_vivo | 2026-11-05T01:00:06 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2038 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:00:06 | poda: escolha json/lista; sem diferença; divergência não |
| 2039 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:00:06 | 3 de 39 verbetes entregues |
| 2040 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:00:06 | recuperacao: escolha entidade-produto,codificacao_incorreta,contrato-produto; divergência não |
| 2042 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:00:06 | {"etapa": "diagnostico", "sha": "cce354b389ad8824", "prompt_sha256": "cce354b389ad", "chars": 3614, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2044 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:00:06 | diagnostico: 73,6 s |
| 2045 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:00:06 | causa_raiz: `codificacao_incorreta` |
| 2046 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:00:06 | campo: `nome` |
| 2047 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:00:06 | impacto: `Alguns nomes dos produtos aparecem corrompidos com símbolos, enquanto outros são exibidos corretamente.` |
| 2048 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:00:06 | fonte: `[codificacao_incorreta]` |
| 2049 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:00:06 | fonte_citada: `codificacao_incorreta` |
| 2050 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:00:06 | quatro_linhas_presentes: confere |
| 2051 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:00:06 | rotulo_no_conjunto: confere |
| 2052 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:00:06 | fonte_existe_na_biblioteca: confere |
| 2053 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:00:06 | fonte_estava_no_contexto: confere |
| 2054 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:00:06 | campo_existe_no_caso: confere |
| 2055 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:00:06 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2056 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:00:06 | notas_nos_verbetes_citados: informativo |
| 2057 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:00:06 | impacto: nao_verificavel |
| 2058 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:00:06 | fonte_formato_valido: confere |
| 2059 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:00:06 | fonte_contem_termo_da_causa: confere |
| 2060 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:00:06 | diagnostico: escolha codificacao_incorreta; divergência não |

</details>

Nós de decisão:

- evento 2038, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 2037 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 2040, `recuperacao`: escolha `entidade-produto,codificacao_incorreta,contrato-produto`; resultado verbetes_entregues; evidência: evento 2039 (verbete_entregue, entidade-produto), evento 2039 (verbete_entregue, codificacao_incorreta), evento 2039 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, codificacao_incorreta, contrato-produto (gen_ai: retrieval)
- evento 2060, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 2039 (verbete_entregue, entidade-produto), evento 2039 (verbete_entregue, codificacao_incorreta), evento 2039 (verbete_entregue, contrato-produto), evento 2044 (resposta), evento 2049 (verbete_citado, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: entidade-produto, codificacao_incorreta, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2036 a 2060 da trilha; hash dos eventos deste caso: `79feaac030118534`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
