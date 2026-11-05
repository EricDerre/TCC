<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-14`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-14@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,97)

**IMPACTO (declarado):** `A interface exibe menos itens do que o esperado, causando uma experiência descontinuada para o usuário.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo itens porque o sinal itens: esperado 14 itens (referência em modo normal), recebido falta o id 14 ("Abacaxi na Brasa") está presente na resposta HTTP e os verbetes entidade-produto, contagem_inconsistente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,02 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 1 edição(ões) aplicada(s) ([contagem_inconsistente]), 0 para revisão humana, 1 recusada(s) (palavra_chave_invalida).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso tra-14. A proposta 1 (nota em [contagem_inconsistente], peso 1) passou pela validação da Fase 3 e pelos filtros e entrou no lote. A proposta 2 (novo_verbete em [contagem_total_inconsistente]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: 'total de itens na interface diferente do esperado'.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `contagem_inconsistente` | aceita | nenhum | **aplicada** | 1 |
| 2 | novo_verbete | `contagem_total_inconsistente` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |

Poda de `arvore` (evento 1370): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 183}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1372): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1928}, depois {"chars": 277}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| itens | 14 itens (referência em modo normal) | falta o id 14 ("Abacaxi na Brasa") |

Trecho podado (hash `9675592a8385ee52`):

```text
lista com 13 itens (referência em modo normal: 14); falta o id 14 ("Abacaxi na Brasa"); primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1367): `GET /api/produtos` status 200; corpo `4f6d409f5a92ce2d`, árvore `None`.

## 3. Contraste com a segunda causa

contagem_inconsistente e não resposta_truncada: a escolha tem probabilidade 0,97 contra 0,02; verbete(s) na evidência: entidade-produto, contagem_inconsistente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,97 | sim |
| resposta_truncada | 0,02 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `entidade-produto`, `contagem_inconsistente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente` |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contagem_inconsistente"]} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1362 | 1 | entrada | programa | ao_vivo | 2026-11-03T23:24:23 | caso tra-14 |
| 1363 | 2 | acao | programa | ao_vivo | 2026-11-03T23:24:23 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 111.0, "url": "produtos_api.php"} |
| 1364 | 3 | acao | programa | ao_vivo | 2026-11-03T23:24:23 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 7.9, "url": null} |
| 1365 | 4 | acao | programa | ao_vivo | 2026-11-03T23:24:23 | {"acao": "conferir", "falhou": true, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 2.4, "url": null} |
| 1367 | 5 | interceptacao | programa | ao_vivo | 2026-11-03T23:24:23 | GET /api/produtos 200 |
| 1368 | 6 | verificacao | verificacao | ao_vivo | 2026-11-03T23:24:23 | conferencia_do_roteiro: nao_confere |
| 1370 | 7 | poda | programa | ao_vivo | 2026-11-03T23:24:23 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 1372 | 8 | poda | programa | ao_vivo | 2026-11-03T23:24:23 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1373 | 9 | candidatos | programa | ao_vivo | 2026-11-03T23:24:23 | 3 de 40 verbetes entregues |
| 1375 | 10 | prompt | programa | ao_vivo | 2026-11-03T23:24:23 | {"chars": 5701, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "b57fa2963b32", "sha": "b57fa2963b324100"} |
| 1377 | 11 | inferencia | programa | ao_vivo | 2026-11-03T23:24:23 | diagnostico: 74,2 s |
| 1378 | 12 | declaracao | modelo | ao_vivo | 2026-11-03T23:24:23 | causa_raiz: `contagem_inconsistente` |
| 1379 | 13 | declaracao | modelo | ao_vivo | 2026-11-03T23:24:23 | campo: `nenhum` |
| 1380 | 14 | declaracao | modelo | ao_vivo | 2026-11-03T23:24:23 | impacto: `A interface exibe menos itens do que o esperado, causando uma experiência descontinuada para o usuário.` |
| 1381 | 15 | declaracao | modelo | ao_vivo | 2026-11-03T23:24:23 | fonte: `[contagem_inconsistente]` |
| 1382 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T23:24:23 | fonte_citada: `contagem_inconsistente` |
| 1383 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T23:24:23 | quatro_linhas_presentes: confere |
| 1384 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T23:24:23 | rotulo_no_conjunto: confere |
| 1385 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T23:24:23 | fonte_existe_na_biblioteca: confere |
| 1386 | 20 | verificacao | verificacao | ao_vivo | 2026-11-03T23:24:23 | fonte_estava_no_contexto: confere |
| 1387 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T23:24:23 | campo_existe_no_caso: nao_se_aplica |
| 1388 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T23:24:23 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1389 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T23:24:23 | notas_nos_verbetes_citados: informativo |
| 1390 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T23:24:23 | impacto: nao_verificavel |
| 1391 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T23:24:23 | fonte_formato_valido: confere |
| 1392 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T23:24:23 | fonte_contem_termo_da_causa: confere |
| 1393 | 27 | decisao | programa | ao_vivo | 2026-11-03T23:24:23 | diagnostico: escolha contagem_inconsistente; divergência não |
| 1396 | 28 | inferencia | programa | ao_vivo | 2026-11-03T23:25:41 | proposta: 159,4 s |
| 1398 | 29 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:25:41 | proposta 1: nota em [contagem_inconsistente]: aplicada |
| 1400 | 30 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:25:41 | proposta 2: novo_verbete em [contagem_total_inconsistente]: recusada: palavra_chave_invalida |
| 1401 | 31 | decisao | programa | ao_vivo | 2026-11-03T23:25:41 | edicao_biblioteca: escolha proposta_1; divergência sim |

</details>

Nós de decisão:

- evento 1393, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 1372 (sinal_em_codigo), evento 1370 (arvore_podada), evento 1367 (corpo_http), evento 1373 (verbete_entregue, entidade-produto), evento 1373 (verbete_entregue, contagem_inconsistente), evento 1373 (verbete_entregue, contrato-produto), evento 1377 (resposta), evento 1382 (verbete_citado, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contagem_inconsistente, contrato-produto (gen_ai: chat)
- evento 1401, `edicao_biblioteca`: escolha `proposta_1`; resultado lote; evidência: evento 1372 (sinal_em_codigo), evento 1370 (arvore_podada), evento 1367 (corpo_http), evento 1377 (resposta), evento 1396 (resposta), evento 1398 (verbete_entregue, contagem_inconsistente); divergência: sim; falha: nenhuma; prov.used: contagem_inconsistente, contrato-produto, entidade-produto

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1362 a 1401 da trilha; hash dos eventos deste caso: `7da8d7d551e05525`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
