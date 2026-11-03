<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-2`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/run-2@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,85)

**IMPACTO (declarado):** `A interface exibe uma lista de produtos em vez de um único objeto, causando confusão no layout.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto porque o sinal arvore: esperado 0 linha(s) da referência, recebido 0 linha(s) novas está presente na tela e os verbetes entidade-produto, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,04 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 516): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 0 linha(s) da referência | 0 linha(s) novas |

Trecho podado (hash `e4870f4dbbc1b73d`):

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
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 517): regras diff_contra_contrato; antes {"chars": 2068}, depois {"chars": 174}.

Trecho podado (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 512): `GET /api/produtos` status 200; corpo `4b1bdd056e7a8c3b`, árvore `None`.

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não corpo_nao_e_json: a escolha tem probabilidade 0,85 contra 0,04; verbete(s) na evidência: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,85 | sim |
| corpo_nao_e_json | 0,04 |  |
| corpo_vazio | 0,04 |  |
| resposta_truncada | 0,04 |  |
| tipo_divergente | 0,03 |  |
| formato_de_data_divergente | 0,02 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [colecao_no_lugar_de_objeto]`; verbetes citados: `contrato-produto`, `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto`, `colecao_no_lugar_de_objeto` |
| fonte_formato_valido | `[contrato-produto] [colecao_no_lugar_de_objeto]` | confere | {"ids": ["contrato-produto", "colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids run-2 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 506 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:30:28 | caso run-2 |
| 507 | 2 | acao | programa | ao_vivo | 2026-11-01T11:30:56 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 111.0, "falhou": false} |
| 508 | 3 | acao | programa | ao_vivo | 2026-11-01T11:30:56 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 27997.1, "falhou": false |
| 509 | 4 | acao | programa | ao_vivo | 2026-11-01T11:30:56 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 4.9, "falhou": false} |
| 510 | 5 | acao | programa | ao_vivo | 2026-11-01T11:30:56 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 7.0, "falhou": false} |
| 511 | 6 | acao | programa | ao_vivo | 2026-11-01T11:30:56 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 8.0, "falhou": false} |
| 512 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T11:30:56 | GET /api/produtos 200 |
| 513 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | conferencia_do_roteiro: confere |
| 514 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | conferencia_do_roteiro: confere |
| 515 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | conferencia_do_roteiro: confere |
| 516 | 11 | poda | programa | ao_vivo | 2026-11-01T11:30:56 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 517 | 12 | poda | programa | ao_vivo | 2026-11-01T11:30:56 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 518 | 13 | candidatos | programa | ao_vivo | 2026-11-01T11:30:56 | 3 de 40 verbetes entregues |
| 520 | 14 | prompt | programa | ao_vivo | 2026-11-01T11:30:56 | {"etapa": "diagnostico", "sha": "64332b968215cf4b", "prompt_sha256": "64332b968215", "chars": 5509, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 522 | 15 | inferencia | programa | ao_vivo | 2026-11-01T11:30:56 | diagnostico: 37,1 s |
| 523 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T11:30:56 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 524 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T11:30:56 | campo: `nenhum` |
| 525 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T11:30:56 | impacto: `A interface exibe uma lista de produtos em vez de um único objeto, causando confusão no layout.` |
| 526 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T11:30:56 | fonte: `[contrato-produto] [colecao_no_lugar_de_objeto]` |
| 527 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T11:30:56 | fonte_citada: `contrato-produto` |
| 528 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T11:30:56 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 529 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | quatro_linhas_presentes: confere |
| 530 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | rotulo_no_conjunto: confere |
| 531 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | fonte_existe_na_biblioteca: confere |
| 532 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | fonte_existe_na_biblioteca: confere |
| 533 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | fonte_estava_no_contexto: confere |
| 534 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | fonte_estava_no_contexto: confere |
| 535 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | campo_existe_no_caso: nao_se_aplica |
| 536 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 537 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | notas_nos_verbetes_citados: informativo |
| 538 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | impacto: nao_verificavel |
| 539 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | fonte_formato_valido: confere |
| 540 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | fonte_contem_termo_da_causa: nao_confere |
| 541 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T11:30:56 | fonte_contem_termo_da_causa: confere |
| 542 | 35 | decisao | programa | ao_vivo | 2026-11-01T11:30:56 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 542, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 517 (sinal_em_codigo), evento 516 (arvore_podada), evento 512 (corpo_http), evento 518 (verbete_entregue, entidade-produto), evento 518 (verbete_entregue, contrato-produto), evento 518 (verbete_entregue, colecao_no_lugar_de_objeto), evento 522 (resposta), evento 527 (verbete_citado, contrato-produto), evento 528 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 506 a 542 da trilha; hash dos eventos deste caso: `2d2fb512b7c58f79`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
