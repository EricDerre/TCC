<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-22`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/run-22@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `limite_de_requisicoes` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,63)

**IMPACTO (declarado):** `A página Produtos fica vazia, com uma mensagem de erro vermelha indicando um excedente de solicitações.`

Justificativa (gerada por molde): O agente respondeu limite_de_requisicoes porque os verbetes limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,63); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 429

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "limite de requisições excedido"}

SINTOMA OBSERVADO: A pagina Produtos (API) abre sem nenhum cartao; a linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI: HTTP 429'.

OBSERVAÇÃO ADICIONAL: A resposta traz o cabecalho Retry-After: 60.
```

## 3. Contraste com a segunda causa

limite_de_requisicoes e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,63 contra 0,00; verbete(s) na evidência: limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| limite_de_requisicoes | 0,63 | sim |
| tempo_de_resposta_excedido | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[limite_de_requisicoes]`; verbetes citados: `limite_de_requisicoes`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `limite_de_requisicoes` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `limite_de_requisicoes` | confere | contexto: `limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `limite_de_requisicoes` | confere | verbetes: `limite_de_requisicoes` |
| fonte_formato_valido | `[limite_de_requisicoes]` | confere | {"ids": ["limite_de_requisicoes"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `limite_de_requisicoes` | confere | {"termo": "limite_de_requisicoes"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids run-22 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1401 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:20:43 | caso run-22 |
| 1402 | 2 | candidatos | programa | ao_vivo | 2026-11-06T12:20:43 | 3 de 39 verbetes entregues |
| 1404 | 3 | prompt | programa | ao_vivo | 2026-11-06T12:20:43 | {"etapa": "diagnostico", "sha": "ddd770f52d3ef8b1", "prompt_sha256": "ddd770f52d3e", "chars": 3888, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1406 | 4 | inferencia | programa | ao_vivo | 2026-11-06T12:20:43 | diagnostico: 55,4 s |
| 1407 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T12:20:43 | causa_raiz: `limite_de_requisicoes` |
| 1408 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T12:20:43 | campo: `nenhum` |
| 1409 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T12:20:43 | impacto: `A página Produtos fica vazia, com uma mensagem de erro vermelha indicando um excedente de solicitações.` |
| 1410 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T12:20:43 | fonte: `[limite_de_requisicoes]` |
| 1411 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T12:20:43 | fonte_citada: `limite_de_requisicoes` |
| 1412 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T12:20:43 | quatro_linhas_presentes: confere |
| 1413 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:20:43 | rotulo_no_conjunto: confere |
| 1414 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:20:43 | fonte_existe_na_biblioteca: confere |
| 1415 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:20:43 | fonte_estava_no_contexto: confere |
| 1416 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T12:20:43 | campo_existe_no_caso: nao_se_aplica |
| 1417 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T12:20:43 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1418 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T12:20:43 | notas_nos_verbetes_citados: informativo |
| 1419 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:20:43 | impacto: nao_verificavel |
| 1420 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:20:43 | fonte_formato_valido: confere |
| 1421 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:20:43 | fonte_contem_termo_da_causa: confere |
| 1422 | 20 | decisao | programa | ao_vivo | 2026-11-06T12:20:43 | diagnostico: escolha limite_de_requisicoes; divergência não |

</details>

Nós de decisão:

- evento 1422, `diagnostico`: escolha `limite_de_requisicoes`; resultado rotulo_emitido; evidência: evento 1402 (verbete_entregue, limite_de_requisicoes), evento 1402 (verbete_entregue, contagem_inconsistente), evento 1402 (verbete_entregue, estrutura_aninhada_divergente), evento 1406 (resposta), evento 1411 (verbete_citado, limite_de_requisicoes); divergência: não; falha: nenhuma; prov.used: limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1401 a 1422 da trilha; hash dos eventos deste caso: `f4c5988f0e453868`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
