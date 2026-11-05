<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-8@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-8@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê símbolos em vez dos acentos corretos na descrição do produto.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque o sinal id: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes contrato-produto, codificacao_incorreta, entidade-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1872): regras diff_contra_contrato; antes {"chars": 159}, depois {"chars": 159}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | texto | inteiro |

Trecho podado (hash `cd0b56c99381d9a7`):

```text
[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, codificacao_incorreta, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[codificacao_incorreta]`; verbetes citados: `codificacao_incorreta`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `codificacao_incorreta` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `codificacao_incorreta` | confere | contexto: `contrato-produto`, `codificacao_incorreta`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | confere | verbetes: `codificacao_incorreta` |
| fonte_formato_valido | `[codificacao_incorreta]` | confere | {"ids": ["codificacao_incorreta"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `codificacao_incorreta` | confere | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-8 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1871 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:50:23 | caso lex-8@contrato_alterado |
| 1872 | 2 | poda | programa | ao_vivo | 2026-11-05T00:50:23 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1873 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:50:23 | poda: escolha json/lista; id:tipo_diferente; divergência não |
| 1874 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:50:23 | 3 de 39 verbetes entregues |
| 1875 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:50:23 | recuperacao: escolha contrato-produto,codificacao_incorreta,entidade-produto; divergência não |
| 1877 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:50:23 | {"etapa": "diagnostico", "sha": "15980fc8b9e709a2", "prompt_sha256": "15980fc8b9e7", "chars": 3477, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1879 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:50:23 | diagnostico: 67,4 s |
| 1880 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:50:23 | causa_raiz: `codificacao_incorreta` |
| 1881 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:50:23 | campo: `nome` |
| 1882 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:50:23 | impacto: `O usuário vê símbolos em vez dos acentos corretos na descrição do produto.` |
| 1883 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:50:23 | fonte: `[codificacao_incorreta]` |
| 1884 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:50:23 | fonte_citada: `codificacao_incorreta` |
| 1885 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:23 | quatro_linhas_presentes: confere |
| 1886 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:23 | rotulo_no_conjunto: confere |
| 1887 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:23 | fonte_existe_na_biblioteca: confere |
| 1888 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:23 | fonte_estava_no_contexto: confere |
| 1889 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:23 | campo_existe_no_caso: confere |
| 1890 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:23 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1891 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:23 | notas_nos_verbetes_citados: informativo |
| 1892 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:23 | impacto: nao_verificavel |
| 1893 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:23 | fonte_formato_valido: confere |
| 1894 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:23 | fonte_contem_termo_da_causa: confere |
| 1895 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:50:23 | diagnostico: escolha codificacao_incorreta; divergência não |

</details>

Nós de decisão:

- evento 1873, `poda`: escolha `json/lista; id:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 1872 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id (gen_ai: plan)
- evento 1875, `recuperacao`: escolha `contrato-produto,codificacao_incorreta,entidade-produto`; resultado verbetes_entregues; evidência: evento 1874 (verbete_entregue, contrato-produto), evento 1874 (verbete_entregue, codificacao_incorreta), evento 1874 (verbete_entregue, entidade-produto); divergência: não; falha: nenhuma; prov.used: contrato-produto, codificacao_incorreta, entidade-produto (gen_ai: retrieval)
- evento 1895, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 1872 (sinal_em_codigo), evento 1874 (verbete_entregue, contrato-produto), evento 1874 (verbete_entregue, codificacao_incorreta), evento 1874 (verbete_entregue, entidade-produto), evento 1879 (resposta), evento 1884 (verbete_citado, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: contrato-produto, codificacao_incorreta, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1871 a 1895 da trilha; hash dos eventos deste caso: `b4934f152c496d06`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
