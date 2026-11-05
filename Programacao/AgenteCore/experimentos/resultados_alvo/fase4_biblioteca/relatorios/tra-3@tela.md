<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-3`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-3@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **baixo** (p = 0,58)

**IMPACTO (declarado):** `O usuário vê categorias incorretas para alguns produtos, como "Bebidas" em vez de "Carnes".`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque o sinal tipo: esperado "Carnes" (referência em modo normal), recebido "Bebidas" em 4 itens está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, contagem_inconsistente, chave_de_juncao_errada estavam entre os entregues ao modelo. A segunda causa, chave_de_juncao_errada, ficou com probabilidade 0,32. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,58); trate como hipótese e confira o campo tipo antes de agir.

**Biblioteca:** 1 edição(ões) aplicada(s) ([novo_verbete]), 0 para revisão humana, 1 recusada(s) (duplicada).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso tra-3. A proposta 1 (retificacao em [chave_de_juncao_errada]) foi recusada por a validação da Fase 3 com o código duplicada: [chave_de_juncao_errada] já tem uma nota com este texto. A proposta 2 (novo_verbete em [novo_verbete], peso 3) passou pela validação da Fase 3 e pelos filtros e entrou no lote.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | retificacao | `chave_de_juncao_errada` | recusada: `duplicada` | nenhum | recusada: `duplicada` |  |
| 2 | novo_verbete | `novo_verbete` | aceita | nenhum | **aplicada** | 3 |

Poda de `arvore` (evento 382): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 384): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2068}, depois {"chars": 409}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | "Carnes" (referência em modo normal) | "Bebidas" em 4 itens |

Trecho podado (hash `5b2f70798bfcb548`):

```text
lista com 14 itens (referência em modo normal: 14); tipo diferente em 4 itens; por exemplo: {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}; {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Acompanhamentos", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false}
```

Interceptação (evento 378): `GET /api/produtos` status 200; corpo `0ef7077cc7a06cfa`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não chave_de_juncao_errada: a escolha tem probabilidade 0,58 contra 0,32; verbete(s) na evidência: entidade-produto, contrato-produto, contagem_inconsistente, chave_de_juncao_errada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,58 | sim |
| chave_de_juncao_errada | 0,32 |  |
| campo_ausente | 0,09 |  |
| campo_renomeado | 0,09 |  |
| valor_fora_do_dominio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [entidade-produto]`; verbetes citados: `contrato-produto`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente`, `chave_de_juncao_errada` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente`, `chave_de_juncao_errada` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto` |
| fonte_formato_valido | `[contrato-produto] [entidade-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "entidade-produto"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>39 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 371 | 1 | entrada | programa | ao_vivo | 2026-11-03T21:40:23 | caso tra-3 |
| 372 | 2 | acao | programa | ao_vivo | 2026-11-03T21:40:24 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 153.0, "url": "produtos_api.php"} |
| 373 | 3 | acao | programa | ao_vivo | 2026-11-03T21:40:24 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 6.5, "url": null} |
| 374 | 4 | acao | programa | ao_vivo | 2026-11-03T21:40:24 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 1.7, "url": null} |
| 375 | 5 | acao | programa | ao_vivo | 2026-11-03T21:40:24 | {"acao": "conferir", "falhou": false, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 12.8, "url": null} |
| 376 | 6 | acao | programa | ao_vivo | 2026-11-03T21:40:24 | {"acao": "conferir", "falhou": false, "passo": 5, "seletor": "#produtos-api-status", "tempo_ms": 4.2, "url": null} |
| 378 | 7 | interceptacao | programa | ao_vivo | 2026-11-03T21:40:24 | GET /api/produtos 200 |
| 379 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | conferencia_do_roteiro: confere |
| 380 | 9 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | conferencia_do_roteiro: confere |
| 381 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | conferencia_do_roteiro: confere |
| 382 | 11 | poda | programa | ao_vivo | 2026-11-03T21:40:24 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 384 | 12 | poda | programa | ao_vivo | 2026-11-03T21:40:24 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 385 | 13 | candidatos | programa | ao_vivo | 2026-11-03T21:40:24 | 3 de 40 verbetes entregues |
| 387 | 14 | prompt | programa | ao_vivo | 2026-11-03T21:40:24 | {"chars": 6738, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "56bc7a760273", "sha": "56bc7a7602730739"} |
| 389 | 15 | inferencia | programa | ao_vivo | 2026-11-03T21:40:24 | diagnostico: 126,7 s |
| 390 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T21:40:24 | causa_raiz: `tipo_divergente` |
| 391 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T21:40:24 | campo: `tipo` |
| 392 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T21:40:24 | impacto: `O usuário vê categorias incorretas para alguns produtos, como "Bebidas" em vez de "Carnes".` |
| 393 | 19 | declaracao | modelo | ao_vivo | 2026-11-03T21:40:24 | fonte: `[contrato-produto] [entidade-produto]` |
| 394 | 20 | declaracao | modelo | ao_vivo | 2026-11-03T21:40:24 | fonte_citada: `contrato-produto` |
| 395 | 21 | declaracao | modelo | ao_vivo | 2026-11-03T21:40:24 | fonte_citada: `entidade-produto` |
| 396 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | quatro_linhas_presentes: confere |
| 397 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | rotulo_no_conjunto: confere |
| 398 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | fonte_existe_na_biblioteca: confere |
| 399 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | fonte_existe_na_biblioteca: confere |
| 400 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | fonte_estava_no_contexto: confere |
| 401 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | fonte_estava_no_contexto: confere |
| 402 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | campo_existe_no_caso: confere |
| 403 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 404 | 30 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | notas_nos_verbetes_citados: informativo |
| 405 | 31 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | impacto: nao_verificavel |
| 406 | 32 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | fonte_formato_valido: confere |
| 407 | 33 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | fonte_contem_termo_da_causa: nao_confere |
| 408 | 34 | verificacao | verificacao | ao_vivo | 2026-11-03T21:40:24 | fonte_contem_termo_da_causa: nao_confere |
| 409 | 35 | decisao | programa | ao_vivo | 2026-11-03T21:40:24 | diagnostico: escolha tipo_divergente; divergência não |
| 412 | 36 | inferencia | programa | ao_vivo | 2026-11-03T21:42:34 | proposta: 191,7 s |
| 414 | 37 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:42:34 | proposta 1: retificacao em [chave_de_juncao_errada]: recusada: duplicada |
| 415 | 38 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:42:34 | proposta 2: novo_verbete em [novo_verbete]: aplicada |
| 416 | 39 | decisao | programa | ao_vivo | 2026-11-03T21:42:34 | edicao_biblioteca: escolha proposta_2; divergência sim |

</details>

Nós de decisão:

- evento 409, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 384 (sinal_em_codigo), evento 382 (arvore_podada), evento 378 (corpo_http), evento 385 (verbete_entregue, entidade-produto), evento 385 (verbete_entregue, contrato-produto), evento 385 (verbete_entregue, contagem_inconsistente), evento 385 (verbete_entregue, chave_de_juncao_errada), evento 389 (resposta), evento 394 (verbete_citado, contrato-produto), evento 395 (verbete_citado, entidade-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, contagem_inconsistente, chave_de_juncao_errada (gen_ai: chat)
- evento 416, `edicao_biblioteca`: escolha `proposta_2`; resultado lote; evidência: evento 384 (sinal_em_codigo), evento 382 (arvore_podada), evento 378 (corpo_http), evento 389 (resposta), evento 412 (resposta), evento 414 (verbete_entregue, chave_de_juncao_errada); divergência: sim; falha: nenhuma; prov.used: chave_de_juncao_errada, contagem_inconsistente, contrato-produto, entidade-produto

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 371 a 416 da trilha; hash dos eventos deste caso: `fd48f9249cd15c88`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
