<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-16`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/sin-16@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê uma tela com 14 linhas a menos, pois o campo destaque ausente não é exibido corretamente, causando um desbalanceamento na visualização dos produtos.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo destaque porque o sinal destaque: esperado booleano, recebido None está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_renomeado, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1435): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 42}.

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

Poda de `corpo_http` (evento 1437): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 145}, depois {"chars": 25}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| destaque | booleano |  |

Trecho podado (hash `dea02287a3373e04`):

```text
{"destaque": "(ausente)"}
```

Interceptação (evento 1428): `GET /api/produtos` status 200; corpo `67aa0b74224df738`, árvore `None`.

Interceptação (evento 1430): `GET /api/produtos/1` status 200; corpo `b11d0160488d8cdf`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não campo_renomeado: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,99 | sim |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente]`; verbetes citados: `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto`, `campo_ausente` |
| fonte_formato_valido | `[campo_ausente]` | confere | {"ids": ["campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids sin-16 --k 3`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1419 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:32:26 | caso sin-16 |
| 1420 | 2 | acao | programa | ao_vivo | 2026-11-05T19:32:27 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 172.2, "falhou": false} |
| 1421 | 3 | acao | programa | ao_vivo | 2026-11-05T19:32:27 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.6, "falhou": false} |
| 1422 | 4 | acao | programa | ao_vivo | 2026-11-05T19:32:27 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.7, "falhou": false} |
| 1423 | 5 | acao | programa | ao_vivo | 2026-11-05T19:32:27 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='1']", "url": null, "tempo_ms": 15.8, "falhou": false} |
| 1424 | 6 | acao | programa | ao_vivo | 2026-11-05T19:32:27 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 210.0, "falhou": false} |
| 1425 | 7 | acao | programa | ao_vivo | 2026-11-05T19:32:27 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 4.3, "falhou": false} |
| 1426 | 8 | acao | programa | ao_vivo | 2026-11-05T19:32:27 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 3.7, "falhou": false} |
| 1428 | 9 | interceptacao | programa | ao_vivo | 2026-11-05T19:32:27 | GET /api/produtos 200 |
| 1430 | 10 | interceptacao | programa | ao_vivo | 2026-11-05T19:32:27 | GET /api/produtos/1 200 |
| 1431 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | conferencia_do_roteiro: confere |
| 1432 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | conferencia_do_roteiro: confere |
| 1433 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | conferencia_do_roteiro: confere |
| 1435 | 14 | poda | programa | ao_vivo | 2026-11-05T19:32:27 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1437 | 15 | poda | programa | ao_vivo | 2026-11-05T19:32:27 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1438 | 16 | candidatos | programa | ao_vivo | 2026-11-05T19:32:27 | 3 de 39 verbetes entregues |
| 1440 | 17 | prompt | programa | ao_vivo | 2026-11-05T19:32:27 | {"etapa": "diagnostico", "sha": "0c00e923c64b81c0", "prompt_sha256": "0c00e923c64b", "chars": 3485, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1442 | 18 | inferencia | programa | ao_vivo | 2026-11-05T19:32:27 | diagnostico: 54,5 s |
| 1443 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T19:32:27 | causa_raiz: `campo_ausente` |
| 1444 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T19:32:27 | campo: `destaque` |
| 1445 | 21 | declaracao | modelo | ao_vivo | 2026-11-05T19:32:27 | impacto: `O usuário vê uma tela com 14 linhas a menos, pois o campo destaque ausente não é exibido corretamente, causando um desbalanceamento na visualização dos produtos.` |
| 1446 | 22 | declaracao | modelo | ao_vivo | 2026-11-05T19:32:27 | fonte: `[campo_ausente]` |
| 1447 | 23 | declaracao | modelo | ao_vivo | 2026-11-05T19:32:27 | fonte_citada: `campo_ausente` |
| 1448 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | quatro_linhas_presentes: confere |
| 1449 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | rotulo_no_conjunto: confere |
| 1450 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | fonte_existe_na_biblioteca: confere |
| 1451 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | fonte_estava_no_contexto: confere |
| 1452 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | campo_existe_no_caso: confere |
| 1453 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1454 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | notas_nos_verbetes_citados: informativo |
| 1455 | 31 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | impacto: nao_verificavel |
| 1456 | 32 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | fonte_formato_valido: confere |
| 1457 | 33 | verificacao | verificacao | ao_vivo | 2026-11-05T19:32:27 | fonte_contem_termo_da_causa: confere |
| 1458 | 34 | decisao | programa | ao_vivo | 2026-11-05T19:32:27 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 1458, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 1437 (sinal_em_codigo), evento 1435 (arvore_podada), evento 1430 (corpo_http), evento 1438 (verbete_entregue, entidade-produto), evento 1438 (verbete_entregue, contrato-produto), evento 1438 (verbete_entregue, campo_ausente), evento 1442 (resposta), evento 1447 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1419 a 1458 da trilha; hash dos eventos deste caso: `636ab59577e6a41c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
