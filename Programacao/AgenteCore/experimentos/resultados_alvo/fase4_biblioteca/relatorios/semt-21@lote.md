<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-21@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_vazio` · **CAMPO:** `nome` · selo de probabilidade: **baixo** (p = 0,76) · **CONFLITO**: a causa respondida campo_vazio está fora das 23 permitidas; nenhum verbete entregue trata da causa respondida campo_vazio

**IMPACTO (declarado):** `O usuário vê o texto literal '(sem nome)' em vez do nome do produto.`

Justificativa (gerada por molde): O agente respondeu campo_vazio no campo nome porque os verbetes contrato-produto, entidade-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,32. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a causa respondida campo_vazio está fora das 23 permitidas; nenhum verbete entregue trata da causa respondida campo_vazio. Este nó está marcado com a falha rotulo_fora_da_taxonomia (origem: modelo). O agente não está seguro desta causa (probabilidade 0,76); trate como hipótese e confira o campo nome antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: O card mostra o texto literal '(sem nome)' no lugar do nome do produto; o campo nome e do tipo certo (texto), so que vazio.
```

## 3. Contraste com a segunda causa

campo_vazio e não campo_ausente: a escolha tem probabilidade 0,76 contra 0,32; verbete(s) na evidência: contrato-produto, entidade-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_vazio | 0,76 | sim |
| campo_ausente | 0,32 |  |
| corpo_nao_e_json | 0,23 |  |
| corpo_vazio | 0,23 |  |
| campo_renomeado | 0,06 |  |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto] [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `campo_vazio` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[entidade-produto] [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["entidade-produto", "contrato-produto"]} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "campo_vazio"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_vazio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2396 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:57:31 | caso semt-21 |
| 2397 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:57:31 | 3 de 46 verbetes entregues |
| 2399 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:57:31 | {"chars": 4189, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "807b6cfd7e4d", "sha": "807b6cfd7e4da0f8"} |
| 2401 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:57:31 | diagnostico: 59,0 s |
| 2402 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:57:31 | causa_raiz: `campo_vazio` |
| 2403 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:57:31 | campo: `nome` |
| 2404 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:57:31 | impacto: `O usuário vê o texto literal '(sem nome)' em vez do nome do produto.` |
| 2405 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:57:31 | fonte: `[entidade-produto] [contrato-produto]` |
| 2406 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:57:31 | fonte_citada: `entidade-produto` |
| 2407 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T00:57:31 | fonte_citada: `contrato-produto` |
| 2408 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | quatro_linhas_presentes: confere |
| 2409 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | rotulo_no_conjunto: nao_confere |
| 2410 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | fonte_existe_na_biblioteca: confere |
| 2411 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | fonte_existe_na_biblioteca: confere |
| 2412 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | fonte_estava_no_contexto: confere |
| 2413 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | fonte_estava_no_contexto: confere |
| 2414 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | campo_existe_no_caso: confere |
| 2415 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2416 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | notas_nos_verbetes_citados: informativo |
| 2417 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | impacto: nao_verificavel |
| 2418 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | fonte_formato_valido: confere |
| 2419 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | fonte_contem_termo_da_causa: nao_confere |
| 2420 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T00:57:31 | fonte_contem_termo_da_causa: nao_confere |
| 2421 | 24 | decisao | programa | ao_vivo | 2026-11-04T00:57:31 | diagnostico: escolha campo_vazio; divergência sim |

</details>

Nós de decisão:

- evento 2421, `diagnostico`: escolha `campo_vazio`; resultado rotulo_emitido; evidência: evento 2397 (verbete_entregue, contrato-produto), evento 2397 (verbete_entregue, entidade-produto), evento 2397 (verbete_entregue, tipo_divergente), evento 2401 (resposta), evento 2406 (verbete_citado, entidade-produto), evento 2407 (verbete_citado, contrato-produto); divergência: sim; falha: rotulo_fora_da_taxonomia; prov.used: contrato-produto, entidade-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2396 a 2421 da trilha; hash dos eventos deste caso: `dd0d95d14b93b9cf`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
