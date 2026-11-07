<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/lex-8@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,68)

**IMPACTO (declarado):** `A descrição do produto aparece com símbolos no lugar dos acentos, tornando-a ilegível.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta porque os verbetes codificacao_incorreta, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,68); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]

SINTOMA OBSERVADO: A descricao aparece com simbolos no lugar dos acentos.

OBSERVAÇÃO ADICIONAL: O cabecalho declara charset=utf-8 mas os bytes estao em latin-1.
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não corpo_nao_e_json: a escolha tem probabilidade 0,68 contra 0,00; verbete(s) na evidência: codificacao_incorreta, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 0,68 | sim |
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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids lex-8 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 701 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:21:27 | caso lex-8 |
| 702 | 2 | candidatos | programa | ao_vivo | 2026-11-06T10:21:27 | 3 de 39 verbetes entregues |
| 704 | 3 | prompt | programa | ao_vivo | 2026-11-06T10:21:27 | {"etapa": "diagnostico", "sha": "3880ee6beee34def", "prompt_sha256": "3880ee6beee3", "chars": 3479, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 706 | 4 | inferencia | programa | ao_vivo | 2026-11-06T10:21:27 | diagnostico: 64,8 s |
| 707 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T10:21:27 | causa_raiz: `codificacao_incorreta` |
| 708 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T10:21:27 | campo: `nenhum` |
| 709 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T10:21:27 | impacto: `A descrição do produto aparece com símbolos no lugar dos acentos, tornando-a ilegível.` |
| 710 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T10:21:27 | fonte: `[codificacao_incorreta]` |
| 711 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T10:21:27 | fonte_citada: `codificacao_incorreta` |
| 712 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:21:27 | quatro_linhas_presentes: confere |
| 713 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:21:27 | rotulo_no_conjunto: confere |
| 714 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:21:27 | fonte_existe_na_biblioteca: confere |
| 715 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:21:27 | fonte_estava_no_contexto: confere |
| 716 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T10:21:27 | campo_existe_no_caso: nao_se_aplica |
| 717 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T10:21:27 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 718 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T10:21:27 | notas_nos_verbetes_citados: informativo |
| 719 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:21:27 | impacto: nao_verificavel |
| 720 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:21:27 | fonte_formato_valido: confere |
| 721 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:21:27 | fonte_contem_termo_da_causa: confere |
| 722 | 20 | decisao | programa | ao_vivo | 2026-11-06T10:21:27 | diagnostico: escolha codificacao_incorreta; divergência não |

</details>

Nós de decisão:

- evento 722, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 702 (verbete_entregue, codificacao_incorreta), evento 702 (verbete_entregue, contrato-produto), evento 702 (verbete_entregue, entidade-produto), evento 706 (resposta), evento 711 (verbete_citado, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: codificacao_incorreta, contrato-produto, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 701 a 722 da trilha; hash dos eventos deste caso: `7e2887827b2ef85d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
