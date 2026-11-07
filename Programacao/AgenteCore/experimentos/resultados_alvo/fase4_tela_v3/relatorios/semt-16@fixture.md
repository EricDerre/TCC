<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-16`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/semt-16@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,97)

**IMPACTO (declarado):** `O usuário vê o número 1 em vez do nome da categoria 'Carnes'.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,02. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": 1, "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: A categoria do produto aparece como o numero 1 no card, no lugar de 'Carnes'.
```

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,97 contra 0,02; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,97 | sim |
| campo_ausente | 0,02 |  |
| campo_renomeado | 0,02 |  |
| chave_de_juncao_errada | 0,01 |  |
| valor_fora_do_dominio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

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

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids semt-16 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1648 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:39:12 | caso semt-16 |
| 1649 | 2 | candidatos | programa | ao_vivo | 2026-11-05T19:39:12 | 3 de 39 verbetes entregues |
| 1651 | 3 | prompt | programa | ao_vivo | 2026-11-05T19:39:12 | {"etapa": "diagnostico", "sha": "9d2eb101012c2507", "prompt_sha256": "9d2eb101012c", "chars": 3553, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1653 | 4 | inferencia | programa | ao_vivo | 2026-11-05T19:39:12 | diagnostico: 34,2 s |
| 1654 | 5 | declaracao | modelo | ao_vivo | 2026-11-05T19:39:12 | causa_raiz: `tipo_divergente` |
| 1655 | 6 | declaracao | modelo | ao_vivo | 2026-11-05T19:39:12 | campo: `tipo` |
| 1656 | 7 | declaracao | modelo | ao_vivo | 2026-11-05T19:39:12 | impacto: `O usuário vê o número 1 em vez do nome da categoria 'Carnes'.` |
| 1657 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T19:39:12 | fonte: `[tipo_divergente]` |
| 1658 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T19:39:12 | fonte_citada: `tipo_divergente` |
| 1659 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:12 | quatro_linhas_presentes: confere |
| 1660 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:12 | rotulo_no_conjunto: confere |
| 1661 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:12 | fonte_existe_na_biblioteca: confere |
| 1662 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:12 | fonte_estava_no_contexto: confere |
| 1663 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:12 | campo_existe_no_caso: confere |
| 1664 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:12 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1665 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:12 | notas_nos_verbetes_citados: informativo |
| 1666 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:12 | impacto: nao_verificavel |
| 1667 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:12 | fonte_formato_valido: confere |
| 1668 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:12 | fonte_contem_termo_da_causa: confere |
| 1669 | 20 | decisao | programa | ao_vivo | 2026-11-05T19:39:12 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1669, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1649 (verbete_entregue, entidade-produto), evento 1649 (verbete_entregue, contrato-produto), evento 1649 (verbete_entregue, tipo_divergente), evento 1653 (resposta), evento 1658 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1648 a 1669 da trilha; hash dos eventos deste caso: `70b43ef43fcb03c5`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
