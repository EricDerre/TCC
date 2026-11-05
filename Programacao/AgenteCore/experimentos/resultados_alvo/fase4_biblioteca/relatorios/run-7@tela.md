<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-7`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/run-7@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `recurso_inexistente` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê uma mensagem de erro indicando que o produto não foi encontrado, e a página exibe um erro ao carregar produtos da API.`

Justificativa (gerada por molde): O agente respondeu recurso_inexistente porque o sinal esperado lista, recebido objeto está presente na resposta HTTP e os verbetes contrato-produto, campo_ausente, colecao_no_lugar_de_objeto, recurso_inexistente estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 1 recusada(s) (palavra_chave_invalida) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 1 edição(ões) para o caso run-7. A proposta 1 (nota em [recurso_inexistente]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: 'db.get/filter vazio'.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `recurso_inexistente` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |

Poda de `arvore` (evento 1440): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 54}, depois {"linhas": 21}.

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

Poda de `corpo_http` (evento 1442): regras diff_contra_contrato; antes {"chars": 35}, depois {"chars": 190}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | lista | objeto |
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

Interceptação (evento 1437): `GET /api/produtos` status 404; corpo `ef0fe34e662a175d`, árvore `None`.

## 3. Contraste com a segunda causa

recurso_inexistente e não resposta_truncada: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, campo_ausente, colecao_no_lugar_de_objeto, recurso_inexistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| recurso_inexistente | 1,00 | sim |
| resposta_truncada | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| registro_duplicado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[recurso_inexistente]`; verbetes citados: `recurso_inexistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `recurso_inexistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `recurso_inexistente` | confere | contexto: `contrato-produto`, `campo_ausente`, `colecao_no_lugar_de_objeto`, `recurso_inexistente` |
| Algum verbete do contexto trata da causa respondida | `recurso_inexistente` | confere | verbetes: `contrato-produto`, `recurso_inexistente` |
| fonte_formato_valido | `[recurso_inexistente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["recurso_inexistente"]} |
| fonte_contem_termo_da_causa | `recurso_inexistente` | confere | {"termo": "recurso_inexistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>30 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1432 | 1 | entrada | programa | ao_vivo | 2026-11-03T23:31:58 | caso run-7 |
| 1433 | 2 | acao | programa | ao_vivo | 2026-11-03T23:31:58 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 88.5, "url": "produtos_api.php"} |
| 1434 | 3 | acao | programa | ao_vivo | 2026-11-03T23:31:58 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 6.2, "url": null} |
| 1435 | 4 | acao | programa | ao_vivo | 2026-11-03T23:31:58 | {"acao": "conferir", "falhou": true, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 1.6, "url": null} |
| 1437 | 5 | interceptacao | programa | ao_vivo | 2026-11-03T23:31:58 | GET /api/produtos 404 |
| 1438 | 6 | verificacao | verificacao | ao_vivo | 2026-11-03T23:31:58 | conferencia_do_roteiro: nao_confere |
| 1440 | 7 | poda | programa | ao_vivo | 2026-11-03T23:31:58 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 1442 | 8 | poda | programa | ao_vivo | 2026-11-03T23:31:58 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1443 | 9 | candidatos | programa | ao_vivo | 2026-11-03T23:31:58 | 3 de 40 verbetes entregues |
| 1445 | 10 | prompt | programa | ao_vivo | 2026-11-03T23:31:58 | {"chars": 6125, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "60693ba39cdf", "sha": "60693ba39cdfcbe4"} |
| 1447 | 11 | inferencia | programa | ao_vivo | 2026-11-03T23:31:58 | diagnostico: 112,8 s |
| 1448 | 12 | declaracao | modelo | ao_vivo | 2026-11-03T23:31:58 | causa_raiz: `recurso_inexistente` |
| 1449 | 13 | declaracao | modelo | ao_vivo | 2026-11-03T23:31:58 | campo: `nenhum` |
| 1450 | 14 | declaracao | modelo | ao_vivo | 2026-11-03T23:31:58 | impacto: `O usuário vê uma mensagem de erro indicando que o produto não foi encontrado, e a página exibe um erro ao carregar produtos da API.` |
| 1451 | 15 | declaracao | modelo | ao_vivo | 2026-11-03T23:31:58 | fonte: `[recurso_inexistente]` |
| 1452 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T23:31:58 | fonte_citada: `recurso_inexistente` |
| 1453 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T23:31:58 | quatro_linhas_presentes: confere |
| 1454 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T23:31:58 | rotulo_no_conjunto: confere |
| 1455 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T23:31:58 | fonte_existe_na_biblioteca: confere |
| 1456 | 20 | verificacao | verificacao | ao_vivo | 2026-11-03T23:31:58 | fonte_estava_no_contexto: confere |
| 1457 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T23:31:58 | campo_existe_no_caso: nao_se_aplica |
| 1458 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T23:31:58 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1459 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T23:31:58 | notas_nos_verbetes_citados: informativo |
| 1460 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T23:31:58 | impacto: nao_verificavel |
| 1461 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T23:31:58 | fonte_formato_valido: confere |
| 1462 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T23:31:58 | fonte_contem_termo_da_causa: confere |
| 1463 | 27 | decisao | programa | ao_vivo | 2026-11-03T23:31:58 | diagnostico: escolha recurso_inexistente; divergência não |
| 1466 | 28 | inferencia | programa | ao_vivo | 2026-11-03T23:33:55 | proposta: 121,7 s |
| 1468 | 29 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:33:55 | proposta 1: nota em [recurso_inexistente]: recusada: palavra_chave_invalida |
| 1469 | 30 | decisao | programa | ao_vivo | 2026-11-03T23:33:55 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1463, `diagnostico`: escolha `recurso_inexistente`; resultado rotulo_emitido; evidência: evento 1442 (sinal_em_codigo), evento 1440 (arvore_podada), evento 1437 (corpo_http), evento 1443 (verbete_entregue, contrato-produto), evento 1443 (verbete_entregue, campo_ausente), evento 1443 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1443 (verbete_entregue, recurso_inexistente), evento 1447 (resposta), evento 1452 (verbete_citado, recurso_inexistente); divergência: não; falha: nenhuma; prov.used: contrato-produto, campo_ausente, colecao_no_lugar_de_objeto, recurso_inexistente (gen_ai: chat)
- evento 1469, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1442 (sinal_em_codigo), evento 1440 (arvore_podada), evento 1437 (corpo_http), evento 1447 (resposta), evento 1466 (resposta), evento 1468 (verbete_entregue, recurso_inexistente); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: campo_ausente, colecao_no_lugar_de_objeto, contrato-produto, recurso_inexistente

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1432 a 1469 da trilha; hash dos eventos deste caso: `6260fd2e2c4f3634`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
