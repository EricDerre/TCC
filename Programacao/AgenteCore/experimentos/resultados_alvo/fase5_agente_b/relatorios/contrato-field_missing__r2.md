<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `contrato-field_missing#2`: o que o agente fez, declarou e conferiu

Trilha `fase5_agente_b/qwen2.5_7b/contrato-field_missing#2`; modelo `qwen2.5:7b`, Ollama 0.40.16, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `preco` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário não vê o preço do produto, resultando em uma interface incompleta e potencialmente confusa.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo preco porque o sinal preco: esperado numero, recebido None está presente na resposta HTTP e os verbetes campo_ausente, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 466): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `714120f74ce44bb6`):

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
      text "destaque: Sim"
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 467): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1888}, depois {"chars": 22}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero |  |

Trecho podado (hash `eba906ccfeea5e6e`):

```text
{"preco": "(ausente)"}
```

Interceptação (evento 463): `GET /api/produtos` status 200; corpo `560029372ed43f7a`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não resposta_truncada: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: campo_ausente, entidade-produto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,99 | sim |
| resposta_truncada | 0,00 |  |
| tipo_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente], [contrato-produto]`; verbetes citados: `campo_ausente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `campo_ausente`, `entidade-produto`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `campo_ausente`, `contrato-produto` |
| fonte_formato_valido | `[campo_ausente], [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_ausente", "contrato-produto"]} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase5_agente_b_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>33 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 458 | 1 | entrada | programa | ao_vivo | 2026-11-18T21:48:41 | caso contrato-field_missing#2 |
| 459 | 2 | acao | programa | ao_vivo | 2026-11-18T21:48:41 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 125.1, "url": "produtos_api.php"} |
| 460 | 3 | acao | programa | ao_vivo | 2026-11-18T21:48:41 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 7.7, "url": null} |
| 461 | 4 | acao | programa | ao_vivo | 2026-11-18T21:48:41 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 1.7, "url": null} |
| 462 | 5 | acao | programa | ao_vivo | 2026-11-18T21:48:41 | {"acao": "conferir", "falhou": true, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 3.5, "url": null} |
| 463 | 6 | interceptacao | programa | ao_vivo | 2026-11-18T21:48:41 | GET /api/produtos 200 |
| 464 | 7 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | conferencia_do_roteiro: confere |
| 465 | 8 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | conferencia_do_roteiro: nao_confere |
| 466 | 9 | poda | programa | ao_vivo | 2026-11-18T21:48:41 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 467 | 10 | poda | programa | ao_vivo | 2026-11-18T21:48:41 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 468 | 11 | candidatos | programa | ao_vivo | 2026-11-18T21:48:41 | 3 de 39 verbetes entregues |
| 469 | 12 | prompt | programa | ao_vivo | 2026-11-18T21:48:41 | {"chars": 3570, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "2b8b0adf7818", "sha": "2b8b0adf7818cc7b"} |
| 471 | 13 | inferencia | programa | ao_vivo | 2026-11-18T21:48:41 | diagnostico: 65,7 s |
| 472 | 14 | declaracao | modelo | ao_vivo | 2026-11-18T21:48:41 | causa_raiz: `campo_ausente` |
| 473 | 15 | declaracao | modelo | ao_vivo | 2026-11-18T21:48:41 | campo: `preco` |
| 474 | 16 | declaracao | modelo | ao_vivo | 2026-11-18T21:48:41 | impacto: `O usuário não vê o preço do produto, resultando em uma interface incompleta e potencialmente confusa.` |
| 475 | 17 | declaracao | modelo | ao_vivo | 2026-11-18T21:48:41 | fonte: `[campo_ausente], [contrato-produto]` |
| 476 | 18 | declaracao | modelo | ao_vivo | 2026-11-18T21:48:41 | fonte_citada: `campo_ausente` |
| 477 | 19 | declaracao | modelo | ao_vivo | 2026-11-18T21:48:41 | fonte_citada: `contrato-produto` |
| 478 | 20 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | quatro_linhas_presentes: confere |
| 479 | 21 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | rotulo_no_conjunto: confere |
| 480 | 22 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | fonte_existe_na_biblioteca: confere |
| 481 | 23 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | fonte_existe_na_biblioteca: confere |
| 482 | 24 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | fonte_estava_no_contexto: confere |
| 483 | 25 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | fonte_estava_no_contexto: confere |
| 484 | 26 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | campo_existe_no_caso: confere |
| 485 | 27 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 486 | 28 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | notas_nos_verbetes_citados: informativo |
| 487 | 29 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | impacto: nao_verificavel |
| 488 | 30 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | fonte_formato_valido: confere |
| 489 | 31 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | fonte_contem_termo_da_causa: confere |
| 490 | 32 | verificacao | verificacao | ao_vivo | 2026-11-18T21:48:41 | fonte_contem_termo_da_causa: nao_confere |
| 491 | 33 | decisao | programa | ao_vivo | 2026-11-18T21:48:41 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 491, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 467 (sinal_em_codigo), evento 466 (arvore_podada), evento 463 (corpo_http), evento 468 (verbete_entregue, campo_ausente), evento 468 (verbete_entregue, entidade-produto), evento 468 (verbete_entregue, contrato-produto), evento 471 (resposta), evento 476 (verbete_citado, campo_ausente), evento 477 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, entidade-produto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 458 a 491 da trilha; hash dos eventos deste caso: `8df4595f3cbe7a61`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
