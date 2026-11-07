<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-23`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/sin-23@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `resumo` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê um campo com um nome diferente, "resumo_v2", em vez do campo esperado "resumo".`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo resumo porque o sinal resumo: esperado resumo, recebido resumo_v2 está presente na resposta HTTP e os verbetes contrato-produto, entidade-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 420): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 4 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `39405291027d14f3`):

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
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
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
    heading "Refrigerante" level=4
    text "(sem descrição)"

```

Poda de `corpo_http` (evento 422): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 148}, depois {"chars": 45}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| resumo | resumo | resumo_v2 |

Trecho podado (hash `24db40c1d4c10d8b`):

```text
{"resumo_v2": "Lata 350ml, diversos sabores"}
```

Interceptação (evento 413): `GET /api/produtos` status 200; corpo `b9c8b4f9b4e77bc5`, árvore `None`.

Interceptação (evento 415): `GET /api/produtos/10` status 200; corpo `7f86118ff808363f`, árvore `None`.

## 3. Contraste com a segunda causa

campo_renomeado e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, entidade-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 1,00 | sim |
| campo_ausente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [entidade-produto]`; verbetes citados: `contrato-produto`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `campo_ausente` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `contrato-produto`, `campo_ausente` |
| fonte_formato_valido | `[contrato-produto] [entidade-produto]` | confere | {"ids": ["contrato-produto", "entidade-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_renomeado"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `resumo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids sin-23 --k 3`

## 6. Árvore completa

<details><summary>38 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 404 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:42:13 | caso sin-23 |
| 405 | 2 | acao | programa | ao_vivo | 2026-11-06T11:42:14 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 114.1, "falhou": false} |
| 406 | 3 | acao | programa | ao_vivo | 2026-11-06T11:42:14 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 9.5, "falhou": false} |
| 407 | 4 | acao | programa | ao_vivo | 2026-11-06T11:42:14 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.2, "falhou": false} |
| 408 | 5 | acao | programa | ao_vivo | 2026-11-06T11:42:14 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='10']", "url": null, "tempo_ms": 18.2, "falhou": false} |
| 409 | 6 | acao | programa | ao_vivo | 2026-11-06T11:42:14 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 203.9, "falhou": false} |
| 410 | 7 | acao | programa | ao_vivo | 2026-11-06T11:42:14 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 3.8, "falhou": false} |
| 411 | 8 | acao | programa | ao_vivo | 2026-11-06T11:42:14 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 3.0, "falhou": false} |
| 413 | 9 | interceptacao | programa | ao_vivo | 2026-11-06T11:42:14 | GET /api/produtos 200 |
| 415 | 10 | interceptacao | programa | ao_vivo | 2026-11-06T11:42:14 | GET /api/produtos/10 200 |
| 416 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | conferencia_do_roteiro: confere |
| 417 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | conferencia_do_roteiro: confere |
| 418 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | conferencia_do_roteiro: confere |
| 420 | 14 | poda | programa | ao_vivo | 2026-11-06T11:42:14 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 422 | 15 | poda | programa | ao_vivo | 2026-11-06T11:42:14 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 423 | 16 | candidatos | programa | ao_vivo | 2026-11-06T11:42:14 | 3 de 39 verbetes entregues |
| 425 | 17 | prompt | programa | ao_vivo | 2026-11-06T11:42:14 | {"etapa": "diagnostico", "sha": "ef56dd949a845f9f", "prompt_sha256": "ef56dd949a84", "chars": 3460, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 427 | 18 | inferencia | programa | ao_vivo | 2026-11-06T11:42:14 | diagnostico: 70,9 s |
| 428 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:42:14 | causa_raiz: `campo_renomeado` |
| 429 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:42:14 | campo: `resumo` |
| 430 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:42:14 | impacto: `O usuário vê um campo com um nome diferente, "resumo_v2", em vez do campo esperado "resumo".` |
| 431 | 22 | declaracao | modelo | ao_vivo | 2026-11-06T11:42:14 | fonte: `[contrato-produto] [entidade-produto]` |
| 432 | 23 | declaracao | modelo | ao_vivo | 2026-11-06T11:42:14 | fonte_citada: `contrato-produto` |
| 433 | 24 | declaracao | modelo | ao_vivo | 2026-11-06T11:42:14 | fonte_citada: `entidade-produto` |
| 434 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | quatro_linhas_presentes: confere |
| 435 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | rotulo_no_conjunto: confere |
| 436 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | fonte_existe_na_biblioteca: confere |
| 437 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | fonte_existe_na_biblioteca: confere |
| 438 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | fonte_estava_no_contexto: confere |
| 439 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | fonte_estava_no_contexto: confere |
| 440 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | campo_existe_no_caso: confere |
| 441 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 442 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | notas_nos_verbetes_citados: informativo |
| 443 | 34 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | impacto: nao_verificavel |
| 444 | 35 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | fonte_formato_valido: confere |
| 445 | 36 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | fonte_contem_termo_da_causa: nao_confere |
| 446 | 37 | verificacao | verificacao | ao_vivo | 2026-11-06T11:42:14 | fonte_contem_termo_da_causa: nao_confere |
| 447 | 38 | decisao | programa | ao_vivo | 2026-11-06T11:42:14 | diagnostico: escolha campo_renomeado; divergência não |

</details>

Nós de decisão:

- evento 447, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 422 (sinal_em_codigo), evento 420 (arvore_podada), evento 415 (corpo_http), evento 423 (verbete_entregue, contrato-produto), evento 423 (verbete_entregue, entidade-produto), evento 423 (verbete_entregue, campo_ausente), evento 427 (resposta), evento 432 (verbete_citado, contrato-produto), evento 433 (verbete_citado, entidade-produto); divergência: não; falha: nenhuma; prov.used: contrato-produto, entidade-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 404 a 447 da trilha; hash dos eventos deste caso: `a4102f06ddfb7a32`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
