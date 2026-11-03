<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-16`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/sin-16@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `destaque` · selo de probabilidade: **medio** (p = 0,96)

**IMPACTO (declarado):** `O usuário vê os produtos sem a informação de destaque correta, com "undefined" em substituição a "Sim".`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo destaque porque o sinal destaque: esperado booleano, recebido None está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_renomeado, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1481): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 42}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `f90df6f477ad3eb8`):

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
    group
      heading "Picanha ao Alho" level=3
      text "Carnes"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: undefined"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: undefined"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: undefined"
      button "R$ 69,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"
  dialog
    heading "Picanha ao Alho" level=4
    text "Picanha grelhada com alho laminado na brasa"

```

Poda de `corpo_http` (evento 1483): regras diff_contra_contrato; antes {"chars": 145}, depois {"chars": 25}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| destaque | booleano |  |

Trecho podado (hash `dea02287a3373e04`):

```text
{"destaque": "(ausente)"}
```

Interceptação (evento 1474): `GET /api/produtos` status 200; corpo `67aa0b74224df738`, árvore `None`.

Interceptação (evento 1476): `GET /api/produtos/1` status 200; corpo `b11d0160488d8cdf`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não campo_renomeado: a escolha tem probabilidade 0,96 contra 0,00; verbete(s) na evidência: campo_ausente, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,96 | sim |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente] [contrato-produto]`; verbetes citados: `campo_ausente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `campo_ausente`, `contrato-produto`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `campo_ausente`, `contrato-produto` |
| fonte_formato_valido | `[campo_ausente] [contrato-produto]` | confere | {"ids": ["campo_ausente", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids sin-16 --k 3`

## 6. Árvore completa

<details><summary>38 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1465 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:06:33 | caso sin-16 |
| 1466 | 2 | acao | programa | ao_vivo | 2026-11-01T12:06:33 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 106.7, "falhou": false} |
| 1467 | 3 | acao | programa | ao_vivo | 2026-11-01T12:06:33 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 16.3, "falhou": false} |
| 1468 | 4 | acao | programa | ao_vivo | 2026-11-01T12:06:33 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.3, "falhou": false} |
| 1469 | 5 | acao | programa | ao_vivo | 2026-11-01T12:06:33 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='1']", "url": null, "tempo_ms": 23.7, "falhou": false} |
| 1470 | 6 | acao | programa | ao_vivo | 2026-11-01T12:06:33 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 216.0, "falhou": false} |
| 1471 | 7 | acao | programa | ao_vivo | 2026-11-01T12:06:33 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 4.0, "falhou": false} |
| 1472 | 8 | acao | programa | ao_vivo | 2026-11-01T12:06:33 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 3.8, "falhou": false} |
| 1474 | 9 | interceptacao | programa | ao_vivo | 2026-11-01T12:06:33 | GET /api/produtos 200 |
| 1476 | 10 | interceptacao | programa | ao_vivo | 2026-11-01T12:06:33 | GET /api/produtos/1 200 |
| 1477 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | conferencia_do_roteiro: confere |
| 1478 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | conferencia_do_roteiro: confere |
| 1479 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | conferencia_do_roteiro: confere |
| 1481 | 14 | poda | programa | ao_vivo | 2026-11-01T12:06:33 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1483 | 15 | poda | programa | ao_vivo | 2026-11-01T12:06:33 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1484 | 16 | candidatos | programa | ao_vivo | 2026-11-01T12:06:33 | 3 de 40 verbetes entregues |
| 1486 | 17 | prompt | programa | ao_vivo | 2026-11-01T12:06:33 | {"etapa": "diagnostico", "sha": "68b3bfc7599673a9", "prompt_sha256": "68b3bfc75996", "chars": 5480, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1488 | 18 | inferencia | programa | ao_vivo | 2026-11-01T12:06:33 | diagnostico: 97,3 s |
| 1489 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T12:06:33 | causa_raiz: `campo_ausente` |
| 1490 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T12:06:33 | campo: `destaque` |
| 1491 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T12:06:33 | impacto: `O usuário vê os produtos sem a informação de destaque correta, com "undefined" em substituição a "Sim".` |
| 1492 | 22 | declaracao | modelo | ao_vivo | 2026-11-01T12:06:33 | fonte: `[campo_ausente] [contrato-produto]` |
| 1493 | 23 | declaracao | modelo | ao_vivo | 2026-11-01T12:06:33 | fonte_citada: `campo_ausente` |
| 1494 | 24 | declaracao | modelo | ao_vivo | 2026-11-01T12:06:33 | fonte_citada: `contrato-produto` |
| 1495 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | quatro_linhas_presentes: confere |
| 1496 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | rotulo_no_conjunto: confere |
| 1497 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | fonte_existe_na_biblioteca: confere |
| 1498 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | fonte_existe_na_biblioteca: confere |
| 1499 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | fonte_estava_no_contexto: confere |
| 1500 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | fonte_estava_no_contexto: confere |
| 1501 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | campo_existe_no_caso: confere |
| 1502 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1503 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | notas_nos_verbetes_citados: informativo |
| 1504 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | impacto: nao_verificavel |
| 1505 | 35 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | fonte_formato_valido: confere |
| 1506 | 36 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | fonte_contem_termo_da_causa: confere |
| 1507 | 37 | verificacao | verificacao | ao_vivo | 2026-11-01T12:06:33 | fonte_contem_termo_da_causa: nao_confere |
| 1508 | 38 | decisao | programa | ao_vivo | 2026-11-01T12:06:33 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 1508, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 1483 (sinal_em_codigo), evento 1481 (arvore_podada), evento 1476 (corpo_http), evento 1484 (verbete_entregue, campo_ausente), evento 1484 (verbete_entregue, contrato-produto), evento 1484 (verbete_entregue, tipo_divergente), evento 1488 (resposta), evento 1493 (verbete_citado, campo_ausente), evento 1494 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1465 a 1508 da trilha; hash dos eventos deste caso: `1403b34ed26e917c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
