<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-5`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/sin-5@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,62)

**IMPACTO (declarado):** `A resposta apresenta uma lista onde se esperava um único objeto, causando inconsistência na exibição da descrição dos produtos.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto porque os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,34. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,62); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Fraldinha", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}]

SINTOMA OBSERVADO: Alguns cartoes mostram a descricao e outros nao, sem padrao aparente.
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não tipo_divergente: a escolha tem probabilidade 0,62 contra 0,34; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,62 | sim |
| tipo_divergente | 0,34 |  |
| campo_ausente | 0,02 |  |
| campo_renomeado | 0,02 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids sin-5 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 227 | 1 | entrada | programa | ao_vivo | 2026-11-05T18:47:56 | caso sin-5 |
| 228 | 2 | candidatos | programa | ao_vivo | 2026-11-05T18:47:56 | 3 de 39 verbetes entregues |
| 230 | 3 | prompt | programa | ao_vivo | 2026-11-05T18:47:56 | {"etapa": "diagnostico", "sha": "1de106465d28a1b3", "prompt_sha256": "1de106465d28", "chars": 3663, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 232 | 4 | inferencia | programa | ao_vivo | 2026-11-05T18:47:56 | diagnostico: 56,8 s |
| 233 | 5 | declaracao | modelo | ao_vivo | 2026-11-05T18:47:56 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 234 | 6 | declaracao | modelo | ao_vivo | 2026-11-05T18:47:56 | campo: `nenhum` |
| 235 | 7 | declaracao | modelo | ao_vivo | 2026-11-05T18:47:56 | impacto: `A resposta apresenta uma lista onde se esperava um único objeto, causando inconsistência na exibição da descrição dos produtos.` |
| 236 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T18:47:56 | fonte: `[contrato-produto]` |
| 237 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T18:47:56 | fonte_citada: `contrato-produto` |
| 238 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T18:47:56 | quatro_linhas_presentes: confere |
| 239 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T18:47:56 | rotulo_no_conjunto: confere |
| 240 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T18:47:56 | fonte_existe_na_biblioteca: confere |
| 241 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T18:47:56 | fonte_estava_no_contexto: confere |
| 242 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T18:47:56 | campo_existe_no_caso: nao_se_aplica |
| 243 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T18:47:56 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 244 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T18:47:56 | notas_nos_verbetes_citados: informativo |
| 245 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T18:47:56 | impacto: nao_verificavel |
| 246 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T18:47:56 | fonte_formato_valido: confere |
| 247 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T18:47:56 | fonte_contem_termo_da_causa: nao_confere |
| 248 | 20 | decisao | programa | ao_vivo | 2026-11-05T18:47:56 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 248, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 228 (verbete_entregue, entidade-produto), evento 228 (verbete_entregue, contrato-produto), evento 228 (verbete_entregue, tipo_divergente), evento 232 (resposta), evento 237 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 227 a 248 da trilha; hash dos eventos deste caso: `af388398950fe6ae`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
