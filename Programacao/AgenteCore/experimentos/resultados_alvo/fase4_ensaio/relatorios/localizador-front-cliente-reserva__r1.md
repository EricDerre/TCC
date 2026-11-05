<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_ensaio/qwen2.5_7b/localizador-front-cliente-reserva#1`: o que o agente fez, declarou e conferiu

Trilha `fase4_ensaio/qwen2.5_7b/localizador-front-cliente-reserva#1`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário não consegue avançar no processo de reserva, ficando preso na tela inicial.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, corpo_nao_e_json, resposta_truncada estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Alvo registrado na corrida de referência: button "Reservar" (ocorrência 1; tag `input`; caminho `#reserva_login > input:nth-of-type(1)`; atributos {"id": "enviar", "class": "btn btn-danger btn-block", "name": "enviar", "type": "submit", "value": "Reservar"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=button[name="Reservar"]` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.711 s) | **sim** |
| `papel_e_nome_parecido` | não gerado: nenhum button da árvore podada tem nome parecido com "Reservar" acima do limiar 0.6 (o mais próximo, " CANCELAR", fica em 0.33) | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | `text=Reservar` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `#reserva_login > input:nth-of-type(1)` | **não confere** | não se aplica | não se aplica | não se aplica | não tentado |  |
| `posicao_entre_irmaos` | `#reserva_login >> role=button >> nth=0` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 393): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 36}, depois {"linhas": 14}.

Trecho podado (hash `d5eb01145ff43b5f`):

```text
document "Área do cliente - Cliente Teste"
  main
    heading " Olá, Cliente Teste!" level=2
    text "Faça uma nova reserva"
    heading "Suas Reservas" level=2
    button " CANCELAR"
    heading "Faça sua Reserva" level=1
    button "Reservar" id="enviar" name="enviar" class="btn btn-danger btn-block"
    text "Número de Pessoas:"
    spinbutton "4"
    text "Data da Reserva:"
    textbox "Data da Reserva:" id="data_pedido" name="data_pedido" class="form-control"
    text "id do cliente:"
    textbox "id do cliente:" id="id_clientes" name="id_clientes" class="form-control"

```

## 3. Contraste com a segunda causa

localizador_quebrado e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: localizador_quebrado, corpo_nao_e_json, resposta_truncada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 0,99 | sim |
| tempo_de_resposta_excedido | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `corpo_nao_e_json`, `resposta_truncada` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| fonte_formato_valido | `[localizador_quebrado]` | confere | {"ids": ["localizador_quebrado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>52 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 380 | 1 | entrada | programa | ao_vivo | 2026-11-04T20:35:18 | caso None |
| 381 | 2 | acao | programa | ao_vivo | 2026-11-04T20:35:23 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 74.6, "falhou": false, "reexecucao": 0} |
| 382 | 3 | acao | programa | ao_vivo | 2026-11-04T20:35:23 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 25.2, "falhou": false, "reexecucao": 0} |
| 383 | 4 | acao | programa | ao_vivo | 2026-11-04T20:35:23 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 15.0, "falhou": false, "reexecucao": 0} |
| 384 | 5 | acao | programa | ao_vivo | 2026-11-04T20:35:23 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 7.7, "falhou": false, "reexecucao": 0} |
| 385 | 6 | acao | programa | ao_vivo | 2026-11-04T20:35:23 | {"passo": 5, "acao": "clicar", "seletor": "button[type=submit]", "url": null, "tempo_ms": 71.6, "falhou": false, "reexecucao": 0} |
| 386 | 7 | acao | programa | ao_vivo | 2026-11-04T20:35:23 | {"passo": 6, "acao": "esperar", "seletor": "span.btn-info", "url": null, "tempo_ms": 113.1, "falhou": false, "reexecucao": 0} |
| 387 | 8 | acao | programa | ao_vivo | 2026-11-04T20:35:23 | {"passo": 7, "acao": "clicar", "seletor": "span.btn-info", "url": null, "tempo_ms": 32.9, "falhou": false, "reexecucao": 0} |
| 388 | 9 | acao | programa | ao_vivo | 2026-11-04T20:35:23 | {"passo": 8, "acao": "esperar", "seletor": "#reserva_login", "url": null, "tempo_ms": 5.3, "falhou": false, "reexecucao": 0} |
| 389 | 10 | acao | programa | ao_vivo | 2026-11-04T20:35:23 | {"passo": 9, "acao": "preencher", "seletor": "#pessoas", "url": null, "tempo_ms": 6.1, "falhou": false, "reexecucao": 0} |
| 390 | 11 | acao | programa | ao_vivo | 2026-11-04T20:35:23 | {"passo": 10, "acao": "preencher", "seletor": "#data_pedido", "url": null, "tempo_ms": 5.9, "falhou": false, "reexecucao": 0} |
| 391 | 12 | acao | programa | ao_vivo | 2026-11-04T20:35:23 | {"passo": 11, "acao": "clicar", "seletor": "#reserva_login > input[type=submit]", "url": null, "tempo_ms": 5014.5, "falhou": true, "reexecucao": 0} |
| 393 | 13 | poda | programa | ao_vivo | 2026-11-04T20:35:23 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 394 | 14 | candidatos | programa | ao_vivo | 2026-11-04T20:35:23 | 3 de 39 verbetes entregues |
| 396 | 15 | prompt | programa | ao_vivo | 2026-11-04T20:35:23 | {"etapa": "diagnostico", "sha": "fc583f186fcb9232", "prompt_sha256": "fc583f186fcb", "chars": 4913, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 398 | 16 | inferencia | programa | ao_vivo | 2026-11-04T20:35:23 | diagnostico: 77,0 s |
| 399 | 17 | declaracao | modelo | ao_vivo | 2026-11-04T20:35:23 | causa_raiz: `localizador_quebrado` |
| 400 | 18 | declaracao | modelo | ao_vivo | 2026-11-04T20:35:23 | campo: `nenhum` |
| 401 | 19 | declaracao | modelo | ao_vivo | 2026-11-04T20:35:23 | impacto: `O usuário não consegue avançar no processo de reserva, ficando preso na tela inicial.` |
| 402 | 20 | declaracao | modelo | ao_vivo | 2026-11-04T20:35:23 | fonte: `[localizador_quebrado]` |
| 403 | 21 | declaracao | modelo | ao_vivo | 2026-11-04T20:35:23 | fonte_citada: `localizador_quebrado` |
| 404 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T20:35:23 | quatro_linhas_presentes: confere |
| 405 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T20:35:23 | rotulo_no_conjunto: confere |
| 406 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T20:35:23 | fonte_existe_na_biblioteca: confere |
| 407 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T20:35:23 | fonte_estava_no_contexto: confere |
| 408 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T20:35:23 | campo_existe_no_caso: nao_se_aplica |
| 409 | 27 | verificacao | verificacao | ao_vivo | 2026-11-04T20:35:23 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 410 | 28 | verificacao | verificacao | ao_vivo | 2026-11-04T20:35:23 | notas_nos_verbetes_citados: informativo |
| 411 | 29 | verificacao | verificacao | ao_vivo | 2026-11-04T20:35:23 | impacto: nao_verificavel |
| 412 | 30 | verificacao | verificacao | ao_vivo | 2026-11-04T20:35:23 | fonte_formato_valido: confere |
| 413 | 31 | verificacao | verificacao | ao_vivo | 2026-11-04T20:35:23 | fonte_contem_termo_da_causa: confere |
| 414 | 32 | decisao | programa | ao_vivo | 2026-11-04T20:35:23 | diagnostico: escolha localizador_quebrado; divergência não |
| 415 | 33 | cura | programa | ao_vivo | 2026-11-04T20:36:43 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 79,9 s |
| 416 | 34 | decisao | programa | ao_vivo | 2026-11-04T20:36:43 | cura: escolha papel_e_nome; divergência sim |
| 417 | 35 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 98.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 418 | 36 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 23.9, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 419 | 37 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 16.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cu |
| 420 | 38 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 9.3, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cur |
| 421 | 39 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 5, "acao": "clicar", "seletor": "button[type=submit]", "url": null, "tempo_ms": 59.5, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", " |
| 422 | 40 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 6, "acao": "esperar", "seletor": "span.btn-info", "url": null, "tempo_ms": 184.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 423 | 41 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 7, "acao": "clicar", "seletor": "span.btn-info", "url": null, "tempo_ms": 41.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado |
| 424 | 42 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 8, "acao": "esperar", "seletor": "#reserva_login", "url": null, "tempo_ms": 5.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 425 | 43 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 9, "acao": "preencher", "seletor": "#pessoas", "url": null, "tempo_ms": 6.9, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado":  |
| 426 | 44 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 10, "acao": "preencher", "seletor": "#data_pedido", "url": null, "tempo_ms": 5.5, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 427 | 45 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 11, "acao": "clicar", "seletor": "role=button[name=\"Reservar\"]", "url": null, "tempo_ms": 89.3, "falhou": false, "reexecucao": 1, "candidato": "pape |
| 428 | 46 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 12, "acao": "abrir", "seletor": null, "url": "cliente/index.php?cliente=11122233344", "tempo_ms": 119.4, "falhou": false, "reexecucao": 1, "candidato" |
| 429 | 47 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 13, "acao": "esperar", "seletor": "table.table tbody tr", "url": null, "tempo_ms": 23.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome" |
| 430 | 48 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 14, "acao": "conferir", "seletor": "button.cancela[data-id]:not([data-id=''])", "url": null, "tempo_ms": 9.1, "falhou": false, "reexecucao": 1, "candi |
| 431 | 49 | acao | programa | ao_vivo | 2026-11-04T20:36:43 | {"passo": 15, "acao": "conferir", "seletor": "table.table tbody", "url": null, "tempo_ms": 4.6, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", " |
| 432 | 50 | verificacao | verificacao | ao_vivo | 2026-11-04T20:36:43 | conferencia_do_roteiro: confere |
| 433 | 51 | verificacao | verificacao | ao_vivo | 2026-11-04T20:36:43 | conferencia_do_roteiro: confere |
| 434 | 52 | decisao | programa | ao_vivo | 2026-11-04T20:36:43 | reexecucao: escolha validada; divergência não |

</details>

Nós de decisão:

- evento 414, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 393 (arvore_podada), evento 394 (verbete_entregue, localizador_quebrado), evento 394 (verbete_entregue, corpo_nao_e_json), evento 394 (verbete_entregue, resposta_truncada), evento 398 (resposta), evento 403 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, corpo_nao_e_json, resposta_truncada (gen_ai: chat)
- evento 416, `cura`: escolha `papel_e_nome`; resultado cura_aplicada; evidência: evento 415 (candidato_de_seletor), evento 393 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome, texto_contido, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 434, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 415 (candidato_de_seletor), evento 432 (sinal_em_codigo), evento 433 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 380 a 434 da trilha; hash dos eventos deste caso: `a68a4a7ca2b23b70`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
