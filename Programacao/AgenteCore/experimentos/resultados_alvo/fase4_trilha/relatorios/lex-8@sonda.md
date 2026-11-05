<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-8@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-8@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,66)

**IMPACTO (declarado):** `A descrição da resposta aparece com símbolos no lugar dos acentos, devido à codificação incorreta dos caracteres.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta porque os verbetes codificacao_incorreta, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,66); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 1819): regras diff_contra_contrato; antes {"chars": 159}, depois {"chars": 159}.

Trecho podado (hash `cd0b56c99381d9a7`):

```text
[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não corpo_nao_e_json: a escolha tem probabilidade 0,66 contra 0,00; verbete(s) na evidência: codificacao_incorreta, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 0,66 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[codificacao_incorreta]`; verbetes citados: `codificacao_incorreta`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `codificacao_incorreta` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `codificacao_incorreta` | confere | contexto: `codificacao_incorreta`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | confere | verbetes: `codificacao_incorreta` |
| fonte_formato_valido | `[codificacao_incorreta]` | confere | {"ids": ["codificacao_incorreta"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `codificacao_incorreta` | confere | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-8 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1818 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:48:58 | caso lex-8@sonda |
| 1819 | 2 | poda | programa | ao_vivo | 2026-11-05T00:48:58 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1820 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:48:58 | poda: escolha json/lista; sem diferença; divergência não |
| 1821 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:48:58 | 3 de 39 verbetes entregues |
| 1822 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:48:58 | recuperacao: escolha codificacao_incorreta,contrato-produto,entidade-produto; divergência não |
| 1824 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:48:58 | {"etapa": "diagnostico", "sha": "06eda3a65176f344", "prompt_sha256": "06eda3a65176", "chars": 3598, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1825 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:48:58 | diagnostico: 59,5 s |
| 1826 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:48:58 | causa_raiz: `codificacao_incorreta` |
| 1827 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:48:58 | campo: `nenhum` |
| 1828 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:48:58 | impacto: `A descrição da resposta aparece com símbolos no lugar dos acentos, devido à codificação incorreta dos caracteres.` |
| 1829 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:48:58 | fonte: `[codificacao_incorreta]` |
| 1830 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:48:58 | fonte_citada: `codificacao_incorreta` |
| 1831 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:48:58 | quatro_linhas_presentes: confere |
| 1832 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:48:58 | rotulo_no_conjunto: confere |
| 1833 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:48:58 | fonte_existe_na_biblioteca: confere |
| 1834 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:48:58 | fonte_estava_no_contexto: confere |
| 1835 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:48:58 | campo_existe_no_caso: nao_se_aplica |
| 1836 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:48:58 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1837 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:48:58 | notas_nos_verbetes_citados: informativo |
| 1838 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:48:58 | impacto: nao_verificavel |
| 1839 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:48:58 | fonte_formato_valido: confere |
| 1840 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:48:58 | fonte_contem_termo_da_causa: confere |
| 1841 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:48:58 | diagnostico: escolha codificacao_incorreta; divergência não |

</details>

Nós de decisão:

- evento 1820, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 1819 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1822, `recuperacao`: escolha `codificacao_incorreta,contrato-produto,entidade-produto`; resultado verbetes_entregues; evidência: evento 1821 (verbete_entregue, codificacao_incorreta), evento 1821 (verbete_entregue, contrato-produto), evento 1821 (verbete_entregue, entidade-produto); divergência: não; falha: nenhuma; prov.used: codificacao_incorreta, contrato-produto, entidade-produto (gen_ai: retrieval)
- evento 1841, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 1821 (verbete_entregue, codificacao_incorreta), evento 1821 (verbete_entregue, contrato-produto), evento 1821 (verbete_entregue, entidade-produto), evento 1825 (resposta), evento 1830 (verbete_citado, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: codificacao_incorreta, contrato-produto, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1818 a 1841 da trilha; hash dos eventos deste caso: `e53721d7650e32d3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
