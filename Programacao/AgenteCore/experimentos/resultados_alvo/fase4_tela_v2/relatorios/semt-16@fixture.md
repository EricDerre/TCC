<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-16`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/semt-16@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,95)

**IMPACTO (declarado):** `O usuário vê o número 1 em vez do nome 'Carnes' para a categoria do produto.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, chave_de_juncao_errada, ficou com probabilidade 0,04. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

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

tipo_divergente e não chave_de_juncao_errada: a escolha tem probabilidade 0,95 contra 0,04; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,95 | sim |
| chave_de_juncao_errada | 0,04 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| valor_fora_do_dominio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

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

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids semt-16 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1710 | 1 | entrada | programa | ao_vivo | 2026-11-01T15:14:04 | caso semt-16 |
| 1711 | 2 | candidatos | programa | ao_vivo | 2026-11-01T15:14:04 | 3 de 40 verbetes entregues |
| 1713 | 3 | prompt | programa | ao_vivo | 2026-11-01T15:14:04 | {"etapa": "diagnostico", "sha": "2a766cb84520743c", "prompt_sha256": "2a766cb84520", "chars": 3395, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1715 | 4 | inferencia | programa | ao_vivo | 2026-11-01T15:14:04 | diagnostico: 46,4 s |
| 1716 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T15:14:04 | causa_raiz: `tipo_divergente` |
| 1717 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T15:14:04 | campo: `tipo` |
| 1718 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T15:14:04 | impacto: `O usuário vê o número 1 em vez do nome 'Carnes' para a categoria do produto.` |
| 1719 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T15:14:04 | fonte: `[tipo_divergente] [contrato-produto]` |
| 1720 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T15:14:04 | fonte_citada: `tipo_divergente` |
| 1721 | 10 | declaracao | modelo | ao_vivo | 2026-11-01T15:14:04 | fonte_citada: `contrato-produto` |
| 1722 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | quatro_linhas_presentes: confere |
| 1723 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | rotulo_no_conjunto: confere |
| 1724 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | fonte_existe_na_biblioteca: confere |
| 1725 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | fonte_existe_na_biblioteca: confere |
| 1726 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | fonte_estava_no_contexto: confere |
| 1727 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | fonte_estava_no_contexto: confere |
| 1728 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | campo_existe_no_caso: confere |
| 1729 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1730 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | notas_nos_verbetes_citados: informativo |
| 1731 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | impacto: nao_verificavel |
| 1732 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | fonte_formato_valido: confere |
| 1733 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | fonte_contem_termo_da_causa: confere |
| 1734 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T15:14:04 | fonte_contem_termo_da_causa: nao_confere |
| 1735 | 24 | decisao | programa | ao_vivo | 2026-11-01T15:14:04 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1735, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1711 (verbete_entregue, entidade-produto), evento 1711 (verbete_entregue, contrato-produto), evento 1711 (verbete_entregue, tipo_divergente), evento 1715 (resposta), evento 1720 (verbete_citado, tipo_divergente), evento 1721 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1710 a 1735 da trilha; hash dos eventos deste caso: `8c91e4d82fc4337b`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
