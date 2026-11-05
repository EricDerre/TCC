<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-8@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,75)

**IMPACTO (declarado):** `A descrição da resposta aparece com símbolos no lugar dos acentos, devido à codificação incorreta dos caracteres.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta porque os verbetes codificacao_incorreta, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete codificacao_incorreta não mudou a resposta: sem efeito medido do contexto. A troca do verbete codificacao_incorreta por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,75); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

O caso, como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]

SINTOMA OBSERVADO: A descricao aparece com simbolos no lugar dos acentos.

OBSERVAÇÃO ADICIONAL: O cabecalho declara charset=utf-8 mas os bytes estao em latin-1.
```

Poda de `corpo_http` (evento 1780): regras diff_contra_contrato; antes {"chars": 159}, depois {"chars": 159}.

Trecho podado (hash `cd0b56c99381d9a7`):

```text
[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não corpo_nao_e_json: a escolha tem probabilidade 0,75 contra 0,00; verbete(s) na evidência: codificacao_incorreta, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 0,75 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[codificacao_incorreta]`; verbetes citados: `codificacao_incorreta`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `codificacao_incorreta` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `codificacao_incorreta` | confere | contexto: `codificacao_incorreta`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | confere | verbetes: `codificacao_incorreta` |
| fonte_formato_valido | `[codificacao_incorreta]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["codificacao_incorreta"]} |
| fonte_contem_termo_da_causa | `codificacao_incorreta` | confere | {"termo": "codificacao_incorreta"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `codificacao_incorreta` | codificacao_incorreta | codificacao_incorreta | 0,75 | 1,00 | sem efeito medido do contexto |
| troca | `codificacao_incorreta` | codificacao_incorreta | codificacao_incorreta | 0,75 | 1,00 | sem efeito medido do contexto |
| sem_documentacao | não se aplica | codificacao_incorreta | codificacao_incorreta | 0,75 | 1,00 | sem documentação a resposta fica a mesma |
| repeticao_da_base | não se aplica | codificacao_incorreta | codificacao_incorreta | 0,75 | 0,66 | o mesmo prompt manteve o rótulo |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-8 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1778 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:44:42 | caso lex-8 |
| 1780 | 2 | poda | programa | ao_vivo | 2026-11-05T00:44:42 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1781 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:44:42 | poda: escolha json/lista; sem diferença; divergência não |
| 1782 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:44:42 | 3 de 39 verbetes entregues |
| 1783 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:44:42 | recuperacao: escolha codificacao_incorreta,contrato-produto,entidade-produto; divergência não |
| 1785 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:44:42 | {"chars": 3479, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "3880ee6beee3", "sha": "3880ee6beee34def"} |
| 1787 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:44:42 | diagnostico: 68,6 s |
| 1788 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:44:42 | causa_raiz: `codificacao_incorreta` |
| 1789 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:44:42 | campo: `nenhum` |
| 1790 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:44:42 | impacto: `A descrição da resposta aparece com símbolos no lugar dos acentos, devido à codificação incorreta dos caracteres.` |
| 1791 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:44:42 | fonte: `[codificacao_incorreta]` |
| 1792 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:44:42 | fonte_citada: `codificacao_incorreta` |
| 1793 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:42 | quatro_linhas_presentes: confere |
| 1794 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:42 | rotulo_no_conjunto: confere |
| 1795 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:42 | fonte_existe_na_biblioteca: confere |
| 1796 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:42 | fonte_estava_no_contexto: confere |
| 1797 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:42 | campo_existe_no_caso: nao_se_aplica |
| 1798 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:42 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1799 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:42 | notas_nos_verbetes_citados: informativo |
| 1800 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:42 | impacto: nao_verificavel |
| 1801 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:42 | fonte_formato_valido: confere |
| 1802 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:42 | fonte_contem_termo_da_causa: confere |
| 1805 | 23 | inferencia | programa | ao_vivo | 2026-11-05T00:44:42 | intervencao:remocao: 61,6 s |
| 1806 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T00:44:42 | remocao de codificacao_incorreta: rótulo codificacao_incorreta para codificacao_incorreta |
| 1809 | 25 | inferencia | programa | ao_vivo | 2026-11-05T00:44:42 | intervencao:troca: 69,6 s |
| 1810 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T00:44:42 | troca de codificacao_incorreta: rótulo codificacao_incorreta para codificacao_incorreta |
| 1813 | 27 | inferencia | programa | ao_vivo | 2026-11-05T00:44:42 | intervencao:sem_documentacao: 35,0 s |
| 1814 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T00:44:42 | sem_documentacao de None: rótulo codificacao_incorreta para codificacao_incorreta |
| 1815 | 29 | inferencia | programa | ao_vivo | 2026-11-05T00:44:42 | intervencao:repeticao_da_base: 16,8 s |
| 1816 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T00:44:42 | repeticao_da_base de None: rótulo codificacao_incorreta para codificacao_incorreta |
| 1817 | 31 | decisao | programa | ao_vivo | 2026-11-05T00:44:42 | diagnostico: escolha codificacao_incorreta; divergência não |

</details>

Nós de decisão:

- evento 1781, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 1780 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1783, `recuperacao`: escolha `codificacao_incorreta,contrato-produto,entidade-produto`; resultado verbetes_entregues; evidência: evento 1782 (verbete_entregue, codificacao_incorreta), evento 1782 (verbete_entregue, contrato-produto), evento 1782 (verbete_entregue, entidade-produto); divergência: não; falha: nenhuma; prov.used: codificacao_incorreta, contrato-produto, entidade-produto (gen_ai: retrieval)
- evento 1817, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 1782 (verbete_entregue, codificacao_incorreta), evento 1782 (verbete_entregue, contrato-produto), evento 1782 (verbete_entregue, entidade-produto), evento 1787 (resposta), evento 1792 (verbete_citado, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: codificacao_incorreta, contrato-produto, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1778 a 1817 da trilha; hash dos eventos deste caso: `f54add810c42bd8f`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
