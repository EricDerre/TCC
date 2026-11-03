<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/tra-1@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `formato_de_data_divergente` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,48) · **CONFLITO**: nenhum verbete entregue trata da causa respondida formato_de_data_divergente

**IMPACTO (declarado):** `O preço dos produtos está sendo exibido com a escala incorreta, com valores 100 vezes maiores do que o esperado, resultando em preços exibidos incorretamente.`

Justificativa (gerada por molde): O agente respondeu formato_de_data_divergente porque o sinal arvore: esperado 3 linha(s) da referência, recebido 3 linha(s) novas está presente na tela e os verbetes entidade-produto, nulo_inesperado, pagina-produtos-api estavam entre os entregues ao modelo. A segunda causa, contagem_inconsistente, ficou com probabilidade 0,34 e nenhum verbete entregue a sustenta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida formato_de_data_divergente. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,48); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Poda de `arvore` (evento 340): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `b68e52486de88711`):

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
      button "R$ 8990,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 8490,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 6990,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 342): regras diff_contra_contrato; antes {"chars": 2096}, depois {"chars": 176}.

Trecho podado (hash `3ebb397453143dfc`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 8990.0, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 335): `GET /api/produtos` status 200; corpo `61ba8740c5fc1841`, árvore `None`.

## 3. Contraste com a segunda causa

formato_de_data_divergente e não contagem_inconsistente: a escolha tem probabilidade 0,48 contra 0,34; verbete(s) na evidência: entidade-produto, nulo_inesperado, pagina-produtos-api

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| formato_de_data_divergente | 0,48 | sim |
| contagem_inconsistente | 0,34 |  |
| nulo_inesperado | 0,10 |  |
| tipo_divergente | 0,02 |  |
| escala_ou_unidade_errada | 0,02 |  |
| valor_fora_do_dominio | 0,01 |  |
| resposta_truncada | 0,01 |  |
| corpo_nao_e_json | 0,01 |  |
| corpo_vazio | 0,01 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[sinais: preço com grandeza estranha]`; verbetes citados: nenhum.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca |  | não se aplica | nenhum verbete citado na linha FONTE |
| O verbete citado estava no contexto entregue ao modelo |  | não se aplica | nenhum verbete citado na linha FONTE |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[sinais: preço com grandeza estranha]` | não se aplica | nenhum verbete citado na linha FONTE |
| fonte_contem_termo_da_causa |  | não se aplica | sem causa ou sem verbete citado |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids tra-1 --k 3`

## 6. Árvore completa

<details><summary>30 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 328 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:22:15 | caso tra-1 |
| 329 | 2 | acao | programa | ao_vivo | 2026-11-01T11:22:16 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 117.4, "falhou": false} |
| 330 | 3 | acao | programa | ao_vivo | 2026-11-01T11:22:16 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.7, "falhou": false} |
| 331 | 4 | acao | programa | ao_vivo | 2026-11-01T11:22:16 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.9, "falhou": false} |
| 332 | 5 | acao | programa | ao_vivo | 2026-11-01T11:22:16 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 7.7, "falhou": false} |
| 333 | 6 | acao | programa | ao_vivo | 2026-11-01T11:22:16 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 4.8, "falhou": false} |
| 335 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T11:22:16 | GET /api/produtos 200 |
| 336 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | conferencia_do_roteiro: confere |
| 337 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | conferencia_do_roteiro: confere |
| 338 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | conferencia_do_roteiro: confere |
| 340 | 11 | poda | programa | ao_vivo | 2026-11-01T11:22:16 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 342 | 12 | poda | programa | ao_vivo | 2026-11-01T11:22:16 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 343 | 13 | candidatos | programa | ao_vivo | 2026-11-01T11:22:16 | 3 de 40 verbetes entregues |
| 345 | 14 | prompt | programa | ao_vivo | 2026-11-01T11:22:16 | {"etapa": "diagnostico", "sha": "f6cacfa518fafcc4", "prompt_sha256": "f6cacfa518fa", "chars": 5269, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 347 | 15 | inferencia | programa | ao_vivo | 2026-11-01T11:22:16 | diagnostico: 94,3 s |
| 348 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T11:22:16 | causa_raiz: `formato_de_data_divergente` |
| 349 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T11:22:16 | campo: `nenhum` |
| 350 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T11:22:16 | impacto: `O preço dos produtos está sendo exibido com a escala incorreta, com valores 100 vezes maiores do que o esperado, resultando em preços exibidos incorretamente.` |
| 351 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T11:22:16 | fonte: `[sinais: preço com grandeza estranha]` |
| 352 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | quatro_linhas_presentes: confere |
| 353 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | rotulo_no_conjunto: confere |
| 354 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | fonte_existe_na_biblioteca: nao_se_aplica |
| 355 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | fonte_estava_no_contexto: nao_se_aplica |
| 356 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | campo_existe_no_caso: nao_se_aplica |
| 357 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 358 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | notas_nos_verbetes_citados: nao_se_aplica |
| 359 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | impacto: nao_verificavel |
| 360 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | fonte_formato_valido: nao_se_aplica |
| 361 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T11:22:16 | fonte_contem_termo_da_causa: nao_se_aplica |
| 362 | 30 | decisao | programa | ao_vivo | 2026-11-01T11:22:16 | diagnostico: escolha formato_de_data_divergente; divergência sim |

</details>

Nós de decisão:

- evento 362, `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido; evidência: evento 342 (sinal_em_codigo), evento 340 (arvore_podada), evento 335 (corpo_http), evento 343 (verbete_entregue, entidade-produto), evento 343 (verbete_entregue, nulo_inesperado), evento 343 (verbete_entregue, pagina-produtos-api), evento 347 (resposta); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, nulo_inesperado, pagina-produtos-api (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 328 a 362 da trilha; hash dos eventos deste caso: `857543e21c8d3139`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
