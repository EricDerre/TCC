<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-5`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/sin-5@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,76)

**IMPACTO (declarado):** `A resposta apresenta uma lista de produtos em vez de um único objeto, o que causa inconsistência na exibição dos detalhes dos produtos na interface.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto porque os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,14. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,76); trate como hipótese e confira o caso antes de agir.

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

colecao_no_lugar_de_objeto e não campo_ausente: a escolha tem probabilidade 0,76 contra 0,14; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,76 | sim |
| campo_ausente | 0,14 |  |
| campo_renomeado | 0,14 |  |
| tipo_divergente | 0,07 |  |
| resposta_truncada | 0,01 |  |
| corpo_nao_e_json | 0,01 |  |
| corpo_vazio | 0,01 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids sin-5 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 246 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:18:40 | caso sin-5 |
| 247 | 2 | candidatos | programa | ao_vivo | 2026-11-01T11:18:40 | 3 de 40 verbetes entregues |
| 249 | 3 | prompt | programa | ao_vivo | 2026-11-01T11:18:40 | {"etapa": "diagnostico", "sha": "2d49654015a78a59", "prompt_sha256": "2d49654015a7", "chars": 3528, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 251 | 4 | inferencia | programa | ao_vivo | 2026-11-01T11:18:40 | diagnostico: 48,3 s |
| 252 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T11:18:40 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 253 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T11:18:40 | campo: `nenhum` |
| 254 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T11:18:40 | impacto: `A resposta apresenta uma lista de produtos em vez de um único objeto, o que causa inconsistência na exibição dos detalhes dos produtos na interface.` |
| 255 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T11:18:40 | fonte: `[contrato-produto]` |
| 256 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T11:18:40 | fonte_citada: `contrato-produto` |
| 257 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:18:40 | quatro_linhas_presentes: confere |
| 258 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T11:18:40 | rotulo_no_conjunto: confere |
| 259 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T11:18:40 | fonte_existe_na_biblioteca: confere |
| 260 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T11:18:40 | fonte_estava_no_contexto: confere |
| 261 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T11:18:40 | campo_existe_no_caso: nao_se_aplica |
| 262 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T11:18:40 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 263 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T11:18:40 | notas_nos_verbetes_citados: informativo |
| 264 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T11:18:40 | impacto: nao_verificavel |
| 265 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T11:18:40 | fonte_formato_valido: confere |
| 266 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T11:18:40 | fonte_contem_termo_da_causa: nao_confere |
| 267 | 20 | decisao | programa | ao_vivo | 2026-11-01T11:18:40 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 267, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 247 (verbete_entregue, entidade-produto), evento 247 (verbete_entregue, contrato-produto), evento 247 (verbete_entregue, campo_ausente), evento 251 (resposta), evento 256 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 246 a 267 da trilha; hash dos eventos deste caso: `4477cead0140009d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
