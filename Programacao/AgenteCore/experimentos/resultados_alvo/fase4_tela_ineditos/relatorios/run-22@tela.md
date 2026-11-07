<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-22`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/run-22@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `limite_de_requisicoes` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,78)

**IMPACTO (declarado):** `A interface exibiu um erro de limite de requisições, resultando em uma página vazia sem elementos de produtos.`

Justificativa (gerada por molde): O agente respondeu limite_de_requisicoes porque o sinal esperado lista, recebido objeto está presente na resposta HTTP e os verbetes limite_de_requisicoes, contagem_inconsistente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,78); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Poda de `arvore` (evento 1376): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 54}, depois {"linhas": 21}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 22 linha(s) da referência | 4 linha(s) novas |

Trecho podado (hash `a9423873e702a2f0`):

```text
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "Logotipo Fornalha"
    link "DESTAQUES" href="index.php#destaques"
    link "PRODUTOS" href="index.php#produtos"
    link "PRODUTOS (API)" href="produtos_api.php"
    button "TIPOS" class="dropdown-toggle"
    link "CONTATO" href="index.php#contato"
    searchbox "search" id="buscar" name="buscar" class="form-control"
  main
    heading "Produtos via API" level=2
    text "Erro ao carregar produtos da CobaiaAPI: HTTP 429"
    text "O melhor churrasco da Zona Leste"
    text "Av. Itaquera, 8266 - Itaquera - São Paulo - SP - CEP: 08295000  (11) 2185-9200 ✉"
    link "contato@churrasdafornalha.com.br" href="mailto:contato@churrasdafornalha.com.br?subject=Contato do Site&cc=matheuscs006@gmail.com"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 1378): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 43}, depois {"chars": 198}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| (corpo inteiro) | lista | objeto |
| id | inteiro |  |
| nome | texto |  |
| resumo | texto\|nulo |  |
| tipo | texto |  |
| preco | numero |  |
| imagem | texto\|nulo |  |
| destaque | booleano |  |
| detail |  | texto |

Trecho podado (hash `48db9ba98a506208`):

```text
{"detail": "limite de requisições excedido", "id": "(ausente)", "nome": "(ausente)", "resumo": "(ausente)", "tipo": "(ausente)", "preco": "(ausente)", "imagem": "(ausente)", "destaque": "(ausente)"}
```

Interceptação (evento 1373): `GET /api/produtos` status 429; corpo `de2031cacc5569c2`, árvore `None`.

## 3. Contraste com a segunda causa

limite_de_requisicoes e não resposta_truncada: a escolha tem probabilidade 0,78 contra 0,00; verbete(s) na evidência: limite_de_requisicoes, contagem_inconsistente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| limite_de_requisicoes | 0,78 | sim |
| resposta_truncada | 0,00 |  |
| tempo_de_resposta_excedido | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[limite_de_requisicoes]`; verbetes citados: `limite_de_requisicoes`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `limite_de_requisicoes` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `limite_de_requisicoes` | confere | contexto: `limite_de_requisicoes`, `contagem_inconsistente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `limite_de_requisicoes` | confere | verbetes: `limite_de_requisicoes` |
| fonte_formato_valido | `[limite_de_requisicoes]` | confere | {"ids": ["limite_de_requisicoes"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `limite_de_requisicoes` | confere | {"termo": "limite_de_requisicoes"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids run-22 --k 3`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1368 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:19:17 | caso run-22 |
| 1369 | 2 | acao | programa | ao_vivo | 2026-11-06T12:19:17 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 120.3, "falhou": false} |
| 1370 | 3 | acao | programa | ao_vivo | 2026-11-06T12:19:17 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 6.4, "falhou": false} |
| 1371 | 4 | acao | programa | ao_vivo | 2026-11-06T12:19:17 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.3, "falhou": true} |
| 1373 | 5 | interceptacao | programa | ao_vivo | 2026-11-06T12:19:17 | GET /api/produtos 429 |
| 1374 | 6 | verificacao | verificacao | ao_vivo | 2026-11-06T12:19:17 | conferencia_do_roteiro: nao_confere |
| 1376 | 7 | poda | programa | ao_vivo | 2026-11-06T12:19:17 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1378 | 8 | poda | programa | ao_vivo | 2026-11-06T12:19:17 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1379 | 9 | candidatos | programa | ao_vivo | 2026-11-06T12:19:17 | 3 de 39 verbetes entregues |
| 1381 | 10 | prompt | programa | ao_vivo | 2026-11-06T12:19:17 | {"etapa": "diagnostico", "sha": "57b1a5362baea567", "prompt_sha256": "57b1a5362bae", "chars": 4220, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1383 | 11 | inferencia | programa | ao_vivo | 2026-11-06T12:19:17 | diagnostico: 82,0 s |
| 1384 | 12 | declaracao | modelo | ao_vivo | 2026-11-06T12:19:17 | causa_raiz: `limite_de_requisicoes` |
| 1385 | 13 | declaracao | modelo | ao_vivo | 2026-11-06T12:19:17 | campo: `nenhum` |
| 1386 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T12:19:17 | impacto: `A interface exibiu um erro de limite de requisições, resultando em uma página vazia sem elementos de produtos.` |
| 1387 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T12:19:17 | fonte: `[limite_de_requisicoes]` |
| 1388 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T12:19:17 | fonte_citada: `limite_de_requisicoes` |
| 1389 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:19:17 | quatro_linhas_presentes: confere |
| 1390 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:19:17 | rotulo_no_conjunto: confere |
| 1391 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:19:17 | fonte_existe_na_biblioteca: confere |
| 1392 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T12:19:17 | fonte_estava_no_contexto: confere |
| 1393 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T12:19:17 | campo_existe_no_caso: nao_se_aplica |
| 1394 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T12:19:17 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1395 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T12:19:17 | notas_nos_verbetes_citados: informativo |
| 1396 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T12:19:17 | impacto: nao_verificavel |
| 1397 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T12:19:17 | fonte_formato_valido: confere |
| 1398 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T12:19:17 | fonte_contem_termo_da_causa: confere |
| 1399 | 27 | decisao | programa | ao_vivo | 2026-11-06T12:19:17 | diagnostico: escolha limite_de_requisicoes; divergência não |

</details>

Nós de decisão:

- evento 1399, `diagnostico`: escolha `limite_de_requisicoes`; resultado rotulo_emitido; evidência: evento 1378 (sinal_em_codigo), evento 1376 (arvore_podada), evento 1373 (corpo_http), evento 1379 (verbete_entregue, limite_de_requisicoes), evento 1379 (verbete_entregue, contagem_inconsistente), evento 1379 (verbete_entregue, contrato-produto), evento 1383 (resposta), evento 1388 (verbete_citado, limite_de_requisicoes); divergência: não; falha: nenhuma; prov.used: limite_de_requisicoes, contagem_inconsistente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1368 a 1399 da trilha; hash dos eventos deste caso: `d215e61b857ab1b4`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
