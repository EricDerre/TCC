<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/semt-9@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O produto Picanha ao Alho aparece na seção de destaque, mesmo não estando marcado como destaque no cadastro.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo destaque porque os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

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

tipo_divergente e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| fonte_formato_valido | `[tipo_divergente]` | confere | {"ids": ["tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids semt-9 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1057 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:19:46 | caso semt-9 |
| 1058 | 2 | candidatos | programa | ao_vivo | 2026-11-05T19:19:46 | 3 de 39 verbetes entregues |
| 1060 | 3 | prompt | programa | ao_vivo | 2026-11-05T19:19:46 | {"etapa": "diagnostico", "sha": "94bb644b83ad84aa", "prompt_sha256": "94bb644b83ad", "chars": 3558, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1062 | 4 | inferencia | programa | ao_vivo | 2026-11-05T19:19:46 | diagnostico: 36,8 s |
| 1063 | 5 | declaracao | modelo | ao_vivo | 2026-11-05T19:19:46 | causa_raiz: `tipo_divergente` |
| 1064 | 6 | declaracao | modelo | ao_vivo | 2026-11-05T19:19:46 | campo: `destaque` |
| 1065 | 7 | declaracao | modelo | ao_vivo | 2026-11-05T19:19:46 | impacto: `O produto Picanha ao Alho aparece na seção de destaque, mesmo não estando marcado como destaque no cadastro.` |
| 1066 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T19:19:46 | fonte: `[tipo_divergente]` |
| 1067 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T19:19:46 | fonte_citada: `tipo_divergente` |
| 1068 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T19:19:46 | quatro_linhas_presentes: confere |
| 1069 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T19:19:46 | rotulo_no_conjunto: confere |
| 1070 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T19:19:46 | fonte_existe_na_biblioteca: confere |
| 1071 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T19:19:46 | fonte_estava_no_contexto: confere |
| 1072 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T19:19:46 | campo_existe_no_caso: confere |
| 1073 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T19:19:46 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1074 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T19:19:46 | notas_nos_verbetes_citados: informativo |
| 1075 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T19:19:46 | impacto: nao_verificavel |
| 1076 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T19:19:46 | fonte_formato_valido: confere |
| 1077 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T19:19:46 | fonte_contem_termo_da_causa: confere |
| 1078 | 20 | decisao | programa | ao_vivo | 2026-11-05T19:19:46 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1078, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1058 (verbete_entregue, entidade-produto), evento 1058 (verbete_entregue, contrato-produto), evento 1058 (verbete_entregue, tipo_divergente), evento 1062 (resposta), evento 1067 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1057 a 1078 da trilha; hash dos eventos deste caso: `86589b5ffc2762c3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
