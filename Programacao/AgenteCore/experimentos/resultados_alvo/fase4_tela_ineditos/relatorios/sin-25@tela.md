<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-25`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/sin-25@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `id` · selo de probabilidade: **medio** (p = 0,92)

**IMPACTO (declarado):** `A tela exibe informações incorretas, mostrando 2 linhas a menos e 2 a mais que a referência.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo id porque o sinal esperado objeto, recebido lista está presente na resposta HTTP e os verbetes colecao_no_lugar_de_objeto, contrato-produto, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 559): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 41}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 2 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `d5173f7cbffdeeca`):

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
  dialog
    text "(sem descrição)"

```

Poda de `corpo_http` (evento 561): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 146}, depois {"chars": 157}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| (corpo inteiro) | objeto | lista |

Trecho podado (hash `20a658eef608ccf4`):

```text
{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}
```

Interceptação (evento 552): `GET /api/produtos` status 200; corpo `4b1bdd056e7a8c3b`, árvore `None`.

Interceptação (evento 554): `GET /api/produtos/4` status 200; corpo `b5fb4f34501576cc`, árvore `None`.

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não corpo_nao_e_json: a escolha tem probabilidade 0,92 contra 0,00; verbete(s) na evidência: colecao_no_lugar_de_objeto, contrato-produto, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,92 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[colecao_no_lugar_de_objeto]`; verbetes citados: `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `colecao_no_lugar_de_objeto`, `contrato-produto`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `colecao_no_lugar_de_objeto`, `contrato-produto` |
| fonte_formato_valido | `[colecao_no_lugar_de_objeto]` | confere | {"ids": ["colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids sin-25 --k 3`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 544 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:47:12 | caso sin-25 |
| 545 | 2 | acao | programa | ao_vivo | 2026-11-06T11:47:13 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 88.0, "falhou": false} |
| 546 | 3 | acao | programa | ao_vivo | 2026-11-06T11:47:13 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.4, "falhou": false} |
| 547 | 4 | acao | programa | ao_vivo | 2026-11-06T11:47:13 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.0, "falhou": false} |
| 548 | 5 | acao | programa | ao_vivo | 2026-11-06T11:47:13 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='4']", "url": null, "tempo_ms": 16.6, "falhou": false} |
| 549 | 6 | acao | programa | ao_vivo | 2026-11-06T11:47:13 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 215.2, "falhou": false} |
| 550 | 7 | acao | programa | ao_vivo | 2026-11-06T11:47:13 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 3.9, "falhou": false} |
| 551 | 8 | acao | programa | ao_vivo | 2026-11-06T11:47:13 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 3.1, "falhou": false} |
| 552 | 9 | interceptacao | programa | ao_vivo | 2026-11-06T11:47:13 | GET /api/produtos 200 |
| 554 | 10 | interceptacao | programa | ao_vivo | 2026-11-06T11:47:13 | GET /api/produtos/4 200 |
| 555 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | conferencia_do_roteiro: confere |
| 556 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | conferencia_do_roteiro: confere |
| 557 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | conferencia_do_roteiro: confere |
| 559 | 14 | poda | programa | ao_vivo | 2026-11-06T11:47:13 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 561 | 15 | poda | programa | ao_vivo | 2026-11-06T11:47:13 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 562 | 16 | candidatos | programa | ao_vivo | 2026-11-06T11:47:13 | 3 de 39 verbetes entregues |
| 564 | 17 | prompt | programa | ao_vivo | 2026-11-06T11:47:13 | {"etapa": "diagnostico", "sha": "c6f2ff4094a89d87", "prompt_sha256": "c6f2ff4094a8", "chars": 3942, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 566 | 18 | inferencia | programa | ao_vivo | 2026-11-06T11:47:13 | diagnostico: 78,6 s |
| 567 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:47:13 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 568 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:47:13 | campo: `id` |
| 569 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:47:13 | impacto: `A tela exibe informações incorretas, mostrando 2 linhas a menos e 2 a mais que a referência.` |
| 570 | 22 | declaracao | modelo | ao_vivo | 2026-11-06T11:47:13 | fonte: `[colecao_no_lugar_de_objeto]` |
| 571 | 23 | declaracao | modelo | ao_vivo | 2026-11-06T11:47:13 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 572 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | quatro_linhas_presentes: confere |
| 573 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | rotulo_no_conjunto: confere |
| 574 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | fonte_existe_na_biblioteca: confere |
| 575 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | fonte_estava_no_contexto: confere |
| 576 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | campo_existe_no_caso: confere |
| 577 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 578 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | notas_nos_verbetes_citados: informativo |
| 579 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | impacto: nao_verificavel |
| 580 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | fonte_formato_valido: confere |
| 581 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:47:13 | fonte_contem_termo_da_causa: confere |
| 582 | 34 | decisao | programa | ao_vivo | 2026-11-06T11:47:13 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 582, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 561 (sinal_em_codigo), evento 559 (arvore_podada), evento 554 (corpo_http), evento 562 (verbete_entregue, colecao_no_lugar_de_objeto), evento 562 (verbete_entregue, contrato-produto), evento 562 (verbete_entregue, estado_da_tela_divergente), evento 566 (resposta), evento 571 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: colecao_no_lugar_de_objeto, contrato-produto, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 544 a 582 da trilha; hash dos eventos deste caso: `b80e75711d7ca545`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
