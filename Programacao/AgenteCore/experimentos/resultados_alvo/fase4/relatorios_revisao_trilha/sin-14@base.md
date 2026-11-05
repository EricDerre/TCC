<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-14`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-14@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `imagem_url` · selo de probabilidade: **baixo** (p = 0,30) · **CONFLITO**: a remoção do verbete contrato-produto mudou a resposta de colecao_no_lugar_de_objeto para formato_de_data_divergente; a troca do verbete contrato-produto por um errado mudou a resposta de colecao_no_lugar_de_objeto para formato_de_data_divergente; a inferência sem documentação mudou a resposta de colecao_no_lugar_de_objeto para campo_ausente

**IMPACTO (declarado):** `O ícone de imagem quebrado indica que o campo 'imagem_url' está presente, mas a interface não reconhece o formato correto.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo imagem_url porque o sinal imagem: esperado imagem, recebido imagem_url está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,17. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete contrato-produto mudou a resposta (de colecao_no_lugar_de_objeto para formato_de_data_divergente), então ele pesou na decisão. A troca do verbete contrato-produto por um verbete errado mudou a resposta (de colecao_no_lugar_de_objeto para formato_de_data_divergente). (a probabilidade registrada é só um limite inferior: o rótulo saiu das alternativas devolvidas) A inferência sem documentação mudou a resposta (de colecao_no_lugar_de_objeto para campo_ausente). A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a remoção do verbete contrato-produto mudou a resposta de colecao_no_lugar_de_objeto para formato_de_data_divergente; a troca do verbete contrato-produto por um errado mudou a resposta de colecao_no_lugar_de_objeto para formato_de_data_divergente; a inferência sem documentação mudou a resposta de colecao_no_lugar_de_objeto para campo_ausente. O agente não está seguro desta causa (probabilidade 0,30); trate como hipótese e confira o campo imagem_url antes de agir.

## 2. Evidência

O caso, como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem_url": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: Todos os cartoes mostram icone de imagem quebrada; o resto do dado esta certo.
```

Poda de `corpo_http` (evento 2449): regras diff_contra_contrato; antes {"chars": 153}, depois {"chars": 153}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | imagem | imagem_url |

Trecho podado (hash `e968e16fdb341a27`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem_url": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não tipo_divergente: a escolha tem probabilidade 0,30 contra 0,17; verbete(s) na evidência: entidade-produto, contrato-produto, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,30 | sim |
| tipo_divergente | 0,17 |  |
| resposta_truncada | 0,14 |  |
| formato_de_data_divergente | 0,13 |  |
| campo_ausente | 0,10 |  |
| campo_renomeado | 0,10 |  |
| corpo_nao_e_json | 0,02 |  |
| corpo_vazio | 0,02 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `contrato-produto` | colecao_no_lugar_de_objeto | formato_de_data_divergente | 0,30 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| troca | `contrato-produto` | colecao_no_lugar_de_objeto | formato_de_data_divergente | 0,30 | 0,00 | mudou a resposta: o verbete errado pesou na decisão (só um limite inferior da queda: o rótulo saiu das alternativas devolvidas) |
| sem_documentacao | não se aplica | colecao_no_lugar_de_objeto | campo_ausente | 0,30 | 0,02 | sem documentação a resposta muda: a documentação pesou na decisão |
| repeticao_da_base | não se aplica | colecao_no_lugar_de_objeto | colecao_no_lugar_de_objeto | 0,30 | 0,32 | o mesmo prompt manteve o rótulo |

## 5. Linha de ação

Confira o campo `imagem_url` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-14 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2447 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:21:07 | caso sin-14 |
| 2449 | 2 | poda | programa | ao_vivo | 2026-11-05T01:21:07 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2450 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:21:07 | poda: escolha json/lista; imagem:renomeado; divergência não |
| 2451 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:21:07 | 3 de 39 verbetes entregues |
| 2452 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:21:07 | recuperacao: escolha entidade-produto,contrato-produto,campo_renomeado; divergência não |
| 2454 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:21:07 | {"chars": 3588, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "f827f5e0b766", "sha": "f827f5e0b766d79a"} |
| 2456 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:21:07 | diagnostico: 52,2 s |
| 2457 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:21:07 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 2458 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:21:07 | campo: `imagem_url` |
| 2459 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:21:07 | impacto: `O ícone de imagem quebrado indica que o campo 'imagem_url' está presente, mas a interface não reconhece o formato correto.` |
| 2460 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:21:07 | fonte: `[contrato-produto]` |
| 2461 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:21:07 | fonte_citada: `contrato-produto` |
| 2462 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:21:07 | quatro_linhas_presentes: confere |
| 2463 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:21:07 | rotulo_no_conjunto: confere |
| 2464 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:21:07 | fonte_existe_na_biblioteca: confere |
| 2465 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:21:07 | fonte_estava_no_contexto: confere |
| 2466 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:21:07 | campo_existe_no_caso: confere |
| 2467 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:21:07 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2468 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:21:07 | notas_nos_verbetes_citados: informativo |
| 2469 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:21:07 | impacto: nao_verificavel |
| 2470 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:21:07 | fonte_formato_valido: confere |
| 2471 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:21:07 | fonte_contem_termo_da_causa: nao_confere |
| 2474 | 23 | inferencia | programa | ao_vivo | 2026-11-05T01:21:07 | intervencao:remocao: 76,1 s |
| 2475 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T01:21:07 | remocao de contrato-produto: rótulo colecao_no_lugar_de_objeto para formato_de_data_divergente |
| 2478 | 25 | inferencia | programa | ao_vivo | 2026-11-05T01:21:07 | intervencao:troca: 50,2 s |
| 2479 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T01:21:07 | troca de contrato-produto: rótulo colecao_no_lugar_de_objeto para formato_de_data_divergente |
| 2482 | 27 | inferencia | programa | ao_vivo | 2026-11-05T01:21:07 | intervencao:sem_documentacao: 33,7 s |
| 2483 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T01:21:07 | sem_documentacao de None: rótulo colecao_no_lugar_de_objeto para campo_ausente |
| 2485 | 29 | inferencia | programa | ao_vivo | 2026-11-05T01:21:07 | intervencao:repeticao_da_base: 18,6 s |
| 2486 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T01:21:07 | repeticao_da_base de None: rótulo colecao_no_lugar_de_objeto para colecao_no_lugar_de_objeto |
| 2487 | 31 | decisao | programa | ao_vivo | 2026-11-05T01:21:07 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência sim |

</details>

Nós de decisão:

- evento 2450, `poda`: escolha `json/lista; imagem:renomeado`; resultado sinais_em_codigo; evidência: evento 2449 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: imagem (gen_ai: plan)
- evento 2452, `recuperacao`: escolha `entidade-produto,contrato-produto,campo_renomeado`; resultado verbetes_entregues; evidência: evento 2451 (verbete_entregue, entidade-produto), evento 2451 (verbete_entregue, contrato-produto), evento 2451 (verbete_entregue, campo_renomeado); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_renomeado (gen_ai: retrieval)
- evento 2487, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 2449 (sinal_em_codigo), evento 2451 (verbete_entregue, entidade-produto), evento 2451 (verbete_entregue, contrato-produto), evento 2451 (verbete_entregue, campo_renomeado), evento 2456 (resposta), evento 2461 (verbete_citado, contrato-produto); divergência: sim; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2447 a 2487 da trilha; hash dos eventos deste caso: `bf397d9823f5dfcd`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
