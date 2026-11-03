<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-4`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/tra-4@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,39) · **CONFLITO**: nenhum verbete entregue trata da causa respondida contagem_inconsistente

**IMPACTO (declarado):** `O usuário vê uma lista com 10 produtos a menos do que o esperado, resultando em uma exibição incompleta.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente porque o sinal arvore: esperado 1 linha(s) da referência, recebido 1 linha(s) novas está presente na tela e os verbetes entidade-produto, colecao_no_lugar_de_objeto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,37 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida contagem_inconsistente. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,39); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Poda de `arvore` (evento 395): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 183}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 1 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `7c54fbd0508aace9`):

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
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 69,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 10 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 396): regras diff_contra_contrato; antes {"chars": 1928}, depois {"chars": 174}.

Trecho podado (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 392): `GET /api/produtos` status 200; corpo `4f6d409f5a92ce2d`, árvore `None`.

## 3. Contraste com a segunda causa

contagem_inconsistente e não resposta_truncada: a escolha tem probabilidade 0,39 contra 0,37; verbete(s) na evidência: entidade-produto, colecao_no_lugar_de_objeto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,39 | sim |
| resposta_truncada | 0,37 |  |
| colecao_no_lugar_de_objeto | 0,17 |  |
| corpo_nao_e_json | 0,02 |  |
| corpo_vazio | 0,02 |  |
| estrutura_aninhada_divergente | 0,02 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [colecao_no_lugar_de_objeto]`; verbetes citados: `contrato-produto`, `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto] [colecao_no_lugar_de_objeto]` | confere | {"ids": ["contrato-produto", "colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "contagem_inconsistente"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | **não confere** | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids tra-4 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 387 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:25:07 | caso tra-4 |
| 388 | 2 | acao | programa | ao_vivo | 2026-11-01T11:25:07 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 155.0, "falhou": false} |
| 389 | 3 | acao | programa | ao_vivo | 2026-11-01T11:25:07 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 13.2, "falhou": false} |
| 390 | 4 | acao | programa | ao_vivo | 2026-11-01T11:25:07 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 4.5, "falhou": true} |
| 392 | 5 | interceptacao | programa | ao_vivo | 2026-11-01T11:25:07 | GET /api/produtos 200 |
| 393 | 6 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | conferencia_do_roteiro: nao_confere |
| 395 | 7 | poda | programa | ao_vivo | 2026-11-01T11:25:07 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 396 | 8 | poda | programa | ao_vivo | 2026-11-01T11:25:07 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 397 | 9 | candidatos | programa | ao_vivo | 2026-11-01T11:25:07 | 3 de 40 verbetes entregues |
| 399 | 10 | prompt | programa | ao_vivo | 2026-11-01T11:25:07 | {"etapa": "diagnostico", "sha": "70fb2bccfa3bff25", "prompt_sha256": "70fb2bccfa3b", "chars": 5652, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 401 | 11 | inferencia | programa | ao_vivo | 2026-11-01T11:25:07 | diagnostico: 72,2 s |
| 402 | 12 | declaracao | modelo | ao_vivo | 2026-11-01T11:25:07 | causa_raiz: `contagem_inconsistente` |
| 403 | 13 | declaracao | modelo | ao_vivo | 2026-11-01T11:25:07 | campo: `nenhum` |
| 404 | 14 | declaracao | modelo | ao_vivo | 2026-11-01T11:25:07 | impacto: `O usuário vê uma lista com 10 produtos a menos do que o esperado, resultando em uma exibição incompleta.` |
| 405 | 15 | declaracao | modelo | ao_vivo | 2026-11-01T11:25:07 | fonte: `[contrato-produto] [colecao_no_lugar_de_objeto]` |
| 406 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T11:25:07 | fonte_citada: `contrato-produto` |
| 407 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T11:25:07 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 408 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | quatro_linhas_presentes: confere |
| 409 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | rotulo_no_conjunto: confere |
| 410 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | fonte_existe_na_biblioteca: confere |
| 411 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | fonte_existe_na_biblioteca: confere |
| 412 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | fonte_estava_no_contexto: confere |
| 413 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | fonte_estava_no_contexto: confere |
| 414 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | campo_existe_no_caso: nao_se_aplica |
| 415 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 416 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | notas_nos_verbetes_citados: informativo |
| 417 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | impacto: nao_verificavel |
| 418 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | fonte_formato_valido: confere |
| 419 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | fonte_contem_termo_da_causa: nao_confere |
| 420 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T11:25:07 | fonte_contem_termo_da_causa: nao_confere |
| 421 | 31 | decisao | programa | ao_vivo | 2026-11-01T11:25:07 | diagnostico: escolha contagem_inconsistente; divergência sim |

</details>

Nós de decisão:

- evento 421, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 396 (sinal_em_codigo), evento 395 (arvore_podada), evento 392 (corpo_http), evento 397 (verbete_entregue, entidade-produto), evento 397 (verbete_entregue, colecao_no_lugar_de_objeto), evento 397 (verbete_entregue, contrato-produto), evento 401 (resposta), evento 406 (verbete_citado, contrato-produto), evento 407 (verbete_citado, colecao_no_lugar_de_objeto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, colecao_no_lugar_de_objeto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 387 a 421 da trilha; hash dos eventos deste caso: `3b91f951ba3e8055`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
