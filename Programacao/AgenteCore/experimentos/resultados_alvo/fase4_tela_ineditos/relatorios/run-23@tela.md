<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-23`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/run-23@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `recurso_inexistente` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,97)

**IMPACTO (declarado):** `O usuário vê uma mensagem de erro indicando que o produto não foi encontrado, e a interface exibe um número incorreto de elementos.`

Justificativa (gerada por molde): O agente respondeu recurso_inexistente porque o sinal esperado lista, recebido objeto está presente na resposta HTTP e os verbetes recurso_inexistente, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1436): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 54}, depois {"linhas": 21}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 25 linha(s) da referência | 4 linha(s) novas |

Trecho podado (hash `91d530cffd3d2542`):

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
    text "Erro ao carregar produtos da CobaiaAPI: HTTP 404"
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

Poda de `corpo_http` (evento 1438): regras diff_contra_contrato; antes {"chars": 35}, depois {"chars": 190}.

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

Trecho podado (hash `43658020d88bc125`):

```text
{"detail": "produto não encontrado", "id": "(ausente)", "nome": "(ausente)", "resumo": "(ausente)", "tipo": "(ausente)", "preco": "(ausente)", "imagem": "(ausente)", "destaque": "(ausente)"}
```

Interceptação (evento 1433): `GET /api/produtos` status 404; corpo `ef0fe34e662a175d`, árvore `None`.

## 3. Contraste com a segunda causa

recurso_inexistente e não resposta_truncada: a escolha tem probabilidade 0,97 contra 0,00; verbete(s) na evidência: recurso_inexistente, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| recurso_inexistente | 0,97 | sim |
| resposta_truncada | 0,00 |  |
| registro_duplicado | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[recurso_inexistente]`; verbetes citados: `recurso_inexistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `recurso_inexistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `recurso_inexistente` | confere | contexto: `recurso_inexistente`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `recurso_inexistente` | confere | verbetes: `recurso_inexistente`, `contrato-produto` |
| fonte_formato_valido | `[recurso_inexistente]` | confere | {"ids": ["recurso_inexistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `recurso_inexistente` | confere | {"termo": "recurso_inexistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids run-23 --k 3`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1428 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:21:43 | caso run-23 |
| 1429 | 2 | acao | programa | ao_vivo | 2026-11-06T12:21:43 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 106.8, "falhou": false} |
| 1430 | 3 | acao | programa | ao_vivo | 2026-11-06T12:21:43 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 6.3, "falhou": false} |
| 1431 | 4 | acao | programa | ao_vivo | 2026-11-06T12:21:43 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.9, "falhou": true} |
| 1433 | 5 | interceptacao | programa | ao_vivo | 2026-11-06T12:21:43 | GET /api/produtos 404 |
| 1434 | 6 | verificacao | verificacao | ao_vivo | 2026-11-06T12:21:43 | conferencia_do_roteiro: nao_confere |
| 1436 | 7 | poda | programa | ao_vivo | 2026-11-06T12:21:43 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1438 | 8 | poda | programa | ao_vivo | 2026-11-06T12:21:43 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1439 | 9 | candidatos | programa | ao_vivo | 2026-11-06T12:21:43 | 3 de 39 verbetes entregues |
| 1441 | 10 | prompt | programa | ao_vivo | 2026-11-06T12:21:43 | {"etapa": "diagnostico", "sha": "59bd7d99721f0bc8", "prompt_sha256": "59bd7d99721f", "chars": 4288, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1443 | 11 | inferencia | programa | ao_vivo | 2026-11-06T12:21:43 | diagnostico: 86,4 s |
| 1444 | 12 | declaracao | modelo | ao_vivo | 2026-11-06T12:21:43 | causa_raiz: `recurso_inexistente` |
| 1445 | 13 | declaracao | modelo | ao_vivo | 2026-11-06T12:21:43 | campo: `nenhum` |
| 1446 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T12:21:43 | impacto: `O usuário vê uma mensagem de erro indicando que o produto não foi encontrado, e a interface exibe um número incorreto de elementos.` |
| 1447 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T12:21:43 | fonte: `[recurso_inexistente]` |
| 1448 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T12:21:43 | fonte_citada: `recurso_inexistente` |
| 1449 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:21:43 | quatro_linhas_presentes: confere |
| 1450 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:21:43 | rotulo_no_conjunto: confere |
| 1451 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:21:43 | fonte_existe_na_biblioteca: confere |
| 1452 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T12:21:43 | fonte_estava_no_contexto: confere |
| 1453 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T12:21:43 | campo_existe_no_caso: nao_se_aplica |
| 1454 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T12:21:43 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1455 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T12:21:43 | notas_nos_verbetes_citados: informativo |
| 1456 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T12:21:43 | impacto: nao_verificavel |
| 1457 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T12:21:43 | fonte_formato_valido: confere |
| 1458 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T12:21:43 | fonte_contem_termo_da_causa: confere |
| 1459 | 27 | decisao | programa | ao_vivo | 2026-11-06T12:21:43 | diagnostico: escolha recurso_inexistente; divergência não |

</details>

Nós de decisão:

- evento 1459, `diagnostico`: escolha `recurso_inexistente`; resultado rotulo_emitido; evidência: evento 1438 (sinal_em_codigo), evento 1436 (arvore_podada), evento 1433 (corpo_http), evento 1439 (verbete_entregue, recurso_inexistente), evento 1439 (verbete_entregue, contrato-produto), evento 1439 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1443 (resposta), evento 1448 (verbete_citado, recurso_inexistente); divergência: não; falha: nenhuma; prov.used: recurso_inexistente, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1428 a 1459 da trilha; hash dos eventos deste caso: `1279b8e085069406`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
