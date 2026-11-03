<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/semt-9@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê o produto como destacado mesmo não estando marcado no cadastro.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo destaque porque os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": 2}]

SINTOMA OBSERVADO: O produto aparece na secao de destaques mesmo nao estando marcado no cadastro.
```

## 3. Contraste com a segunda causa

tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,99 | sim |
| valor_fora_do_dominio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente] [contrato-produto]`; verbetes citados: `tipo_divergente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| fonte_formato_valido | `[tipo_divergente] [contrato-produto]` | confere | {"ids": ["tipo_divergente", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids semt-9 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1089 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:52:24 | caso semt-9 |
| 1090 | 2 | candidatos | programa | ao_vivo | 2026-11-01T11:52:24 | 3 de 40 verbetes entregues |
| 1092 | 3 | prompt | programa | ao_vivo | 2026-11-01T11:52:24 | {"etapa": "diagnostico", "sha": "a6ddde9b9aceb425", "prompt_sha256": "a6ddde9b9ace", "chars": 3400, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1094 | 4 | inferencia | programa | ao_vivo | 2026-11-01T11:52:24 | diagnostico: 47,1 s |
| 1095 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T11:52:24 | causa_raiz: `tipo_divergente` |
| 1096 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T11:52:24 | campo: `destaque` |
| 1097 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T11:52:24 | impacto: `O usuário vê o produto como destacado mesmo não estando marcado no cadastro.` |
| 1098 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T11:52:24 | fonte: `[tipo_divergente] [contrato-produto]` |
| 1099 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T11:52:24 | fonte_citada: `tipo_divergente` |
| 1100 | 10 | declaracao | modelo | ao_vivo | 2026-11-01T11:52:24 | fonte_citada: `contrato-produto` |
| 1101 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | quatro_linhas_presentes: confere |
| 1102 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | rotulo_no_conjunto: confere |
| 1103 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | fonte_existe_na_biblioteca: confere |
| 1104 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | fonte_existe_na_biblioteca: confere |
| 1105 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | fonte_estava_no_contexto: confere |
| 1106 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | fonte_estava_no_contexto: confere |
| 1107 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | campo_existe_no_caso: confere |
| 1108 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1109 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | notas_nos_verbetes_citados: informativo |
| 1110 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | impacto: nao_verificavel |
| 1111 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | fonte_formato_valido: confere |
| 1112 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | fonte_contem_termo_da_causa: confere |
| 1113 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:52:24 | fonte_contem_termo_da_causa: nao_confere |
| 1114 | 24 | decisao | programa | ao_vivo | 2026-11-01T11:52:24 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1114, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1090 (verbete_entregue, entidade-produto), evento 1090 (verbete_entregue, contrato-produto), evento 1090 (verbete_entregue, tipo_divergente), evento 1094 (resposta), evento 1099 (verbete_citado, tipo_divergente), evento 1100 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1089 a 1114 da trilha; hash dos eventos deste caso: `4f1bf39f85c345e1`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
