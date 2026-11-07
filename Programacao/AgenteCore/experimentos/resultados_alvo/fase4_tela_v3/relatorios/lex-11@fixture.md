<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-11`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/lex-11@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `Alguns nomes vêm corrompidos com símbolos, devido a conversão de codificação duas vezes.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque os verbetes entidade-produto, codificacao_incorreta, contrato-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e acucar", "tipo": "Sobremesas", "preco": 14.9, "imagem": "abacaxi.jpg", "destaque": false}]

SINTOMA OBSERVADO: Alguns nomes vem certos e outros com simbolos, no mesmo carregamento.

OBSERVAÇÃO ADICIONAL: Os nomes corrompidos passaram por conversao de codificacao duas vezes.
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

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids lex-11 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 820 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:10:04 | caso lex-11 |
| 821 | 2 | candidatos | programa | ao_vivo | 2026-11-05T19:10:04 | 3 de 39 verbetes entregues |
| 823 | 3 | prompt | programa | ao_vivo | 2026-11-05T19:10:04 | {"etapa": "diagnostico", "sha": "2893e22bc2f80e63", "prompt_sha256": "2893e22bc2f8", "chars": 3495, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 825 | 4 | inferencia | programa | ao_vivo | 2026-11-05T19:10:04 | diagnostico: 61,3 s |
| 826 | 5 | declaracao | modelo | ao_vivo | 2026-11-05T19:10:04 | causa_raiz: `codificacao_incorreta` |
| 827 | 6 | declaracao | modelo | ao_vivo | 2026-11-05T19:10:04 | campo: `nome` |
| 828 | 7 | declaracao | modelo | ao_vivo | 2026-11-05T19:10:04 | impacto: `Alguns nomes vêm corrompidos com símbolos, devido a conversão de codificação duas vezes.` |
| 829 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T19:10:04 | fonte: `[codificacao_incorreta]` |
| 830 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T19:10:04 | fonte_citada: `codificacao_incorreta` |
| 831 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T19:10:04 | quatro_linhas_presentes: confere |
| 832 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T19:10:04 | rotulo_no_conjunto: confere |
| 833 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T19:10:04 | fonte_existe_na_biblioteca: confere |
| 834 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T19:10:04 | fonte_estava_no_contexto: confere |
| 835 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T19:10:04 | campo_existe_no_caso: confere |
| 836 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T19:10:04 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 837 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T19:10:04 | notas_nos_verbetes_citados: informativo |
| 838 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T19:10:04 | impacto: nao_verificavel |
| 839 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T19:10:04 | fonte_formato_valido: confere |
| 840 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T19:10:04 | fonte_contem_termo_da_causa: confere |
| 841 | 20 | decisao | programa | ao_vivo | 2026-11-05T19:10:04 | diagnostico: escolha codificacao_incorreta; divergência não |

</details>

Nós de decisão:

- evento 841, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 821 (verbete_entregue, entidade-produto), evento 821 (verbete_entregue, codificacao_incorreta), evento 821 (verbete_entregue, contrato-produto), evento 825 (resposta), evento 830 (verbete_citado, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: entidade-produto, codificacao_incorreta, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 820 a 841 da trilha; hash dos eventos deste caso: `0da3d70ca0d3f752`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
