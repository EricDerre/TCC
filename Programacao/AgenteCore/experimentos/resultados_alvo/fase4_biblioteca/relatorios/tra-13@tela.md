<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-13`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-13@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `imagem_fora_do_dominio` · **CAMPO:** `imagem` · selo de probabilidade: **baixo** (p = 0,20) · **CONFLITO**: a causa respondida imagem_fora_do_dominio está fora das 23 permitidas; nenhum verbete entregue trata da causa respondida imagem_fora_do_dominio

**IMPACTO (declarado):** `O usuário vê imagens diferentes das esperadas para os produtos listados.`

Justificativa (gerada por molde): O agente respondeu imagem_fora_do_dominio no campo imagem porque o sinal imagem: esperado "picanha_alho.jpg" (referência em modo normal), recebido "picanha_sem.jpg" em 14 itens está presente na resposta HTTP e os verbetes entidade-produto, contagem_inconsistente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,19 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a causa respondida imagem_fora_do_dominio está fora das 23 permitidas; nenhum verbete entregue trata da causa respondida imagem_fora_do_dominio. Este nó está marcado com a falha rotulo_fora_da_taxonomia (origem: modelo). O agente não está seguro desta causa (probabilidade 0,20); trate como hipótese e confira o campo imagem antes de agir.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 1 recusada(s) (redundante) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 1 edição(ões) para o caso tra-13. A proposta 1 (nota em [chave_de_juncao_errada]) foi recusada por o filtro redundancia com o código redundante: 50% dos 3-gramas do TEXTO já estão em [chave_de_juncao_errada].

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `chave_de_juncao_errada` | aceita | redundancia | recusada: `redundante` | 1 |

Poda de `arvore` (evento 1327): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1329): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2068}, depois {"chars": 428}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | "picanha_alho.jpg" (referência em modo normal) | "picanha_sem.jpg" em 14 itens |

Trecho podado (hash `c24d8d52b55fd44f`):

```text
lista com 14 itens (referência em modo normal: 14); imagem diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_sem.jpg", "destaque": true}; {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "fraldinha.jpg", "destaque": false}
```

Interceptação (evento 1323): `GET /api/produtos` status 200; corpo `d43cfde4c07461ea`, árvore `None`.

## 3. Contraste com a segunda causa

imagem_fora_do_dominio e não valor_fora_do_dominio: a escolha tem probabilidade 0,20 contra 0,19; verbete(s) na evidência: entidade-produto, contagem_inconsistente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| imagem_fora_do_dominio | 0,20 | sim |
| valor_fora_do_dominio | 0,19 |  |
| colecao_no_lugar_de_objeto | 0,16 |  |
| tipo_divergente | 0,15 |  |
| campo_ausente | 0,13 |  |
| campo_renomeado | 0,13 |  |
| formato_de_data_divergente | 0,10 |  |
| estrutura_aninhada_divergente | 0,03 |  |
| corpo_nao_e_json | 0,02 |  |
| corpo_vazio | 0,02 |  |
| resposta_truncada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto] [contagem_inconsistente]`; verbetes citados: `entidade-produto`, `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contagem_inconsistente`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `entidade-produto`, `contagem_inconsistente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `imagem_fora_do_dominio` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[entidade-produto] [contagem_inconsistente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["entidade-produto", "contagem_inconsistente"]} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "imagem_fora_do_dominio"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | **não confere** | {"termo": "imagem_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>38 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1316 | 1 | entrada | programa | ao_vivo | 2026-11-03T23:20:23 | caso tra-13 |
| 1317 | 2 | acao | programa | ao_vivo | 2026-11-03T23:20:23 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 145.4, "url": "produtos_api.php"} |
| 1318 | 3 | acao | programa | ao_vivo | 2026-11-03T23:20:23 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 8.2, "url": null} |
| 1319 | 4 | acao | programa | ao_vivo | 2026-11-03T23:20:23 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 2.7, "url": null} |
| 1320 | 5 | acao | programa | ao_vivo | 2026-11-03T23:20:23 | {"acao": "conferir", "falhou": false, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 3.8, "url": null} |
| 1321 | 6 | acao | programa | ao_vivo | 2026-11-03T23:20:23 | {"acao": "conferir", "falhou": false, "passo": 5, "seletor": "#produtos-api-status", "tempo_ms": 3.5, "url": null} |
| 1323 | 7 | interceptacao | programa | ao_vivo | 2026-11-03T23:20:23 | GET /api/produtos 200 |
| 1324 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | conferencia_do_roteiro: confere |
| 1325 | 9 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | conferencia_do_roteiro: confere |
| 1326 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | conferencia_do_roteiro: confere |
| 1327 | 11 | poda | programa | ao_vivo | 2026-11-03T23:20:23 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 1329 | 12 | poda | programa | ao_vivo | 2026-11-03T23:20:23 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1330 | 13 | candidatos | programa | ao_vivo | 2026-11-03T23:20:23 | 3 de 40 verbetes entregues |
| 1332 | 14 | prompt | programa | ao_vivo | 2026-11-03T23:20:23 | {"chars": 5715, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "ca7592962738", "sha": "ca75929627385833"} |
| 1334 | 15 | inferencia | programa | ao_vivo | 2026-11-03T23:20:23 | diagnostico: 90,4 s |
| 1335 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T23:20:23 | causa_raiz: `imagem_fora_do_dominio` |
| 1336 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T23:20:23 | campo: `imagem` |
| 1337 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T23:20:23 | impacto: `O usuário vê imagens diferentes das esperadas para os produtos listados.` |
| 1338 | 19 | declaracao | modelo | ao_vivo | 2026-11-03T23:20:23 | fonte: `[entidade-produto] [contagem_inconsistente]` |
| 1339 | 20 | declaracao | modelo | ao_vivo | 2026-11-03T23:20:23 | fonte_citada: `entidade-produto` |
| 1340 | 21 | declaracao | modelo | ao_vivo | 2026-11-03T23:20:23 | fonte_citada: `contagem_inconsistente` |
| 1341 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | quatro_linhas_presentes: confere |
| 1342 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | rotulo_no_conjunto: nao_confere |
| 1343 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | fonte_existe_na_biblioteca: confere |
| 1344 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | fonte_existe_na_biblioteca: confere |
| 1345 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | fonte_estava_no_contexto: confere |
| 1346 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | fonte_estava_no_contexto: confere |
| 1347 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | campo_existe_no_caso: confere |
| 1348 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1349 | 30 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | notas_nos_verbetes_citados: informativo |
| 1350 | 31 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | impacto: nao_verificavel |
| 1351 | 32 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | fonte_formato_valido: confere |
| 1352 | 33 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | fonte_contem_termo_da_causa: nao_confere |
| 1353 | 34 | verificacao | verificacao | ao_vivo | 2026-11-03T23:20:23 | fonte_contem_termo_da_causa: nao_confere |
| 1354 | 35 | decisao | programa | ao_vivo | 2026-11-03T23:20:23 | diagnostico: escolha imagem_fora_do_dominio; divergência sim |
| 1357 | 36 | inferencia | programa | ao_vivo | 2026-11-03T23:21:58 | proposta: 140,2 s |
| 1359 | 37 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:21:58 | proposta 1: nota em [chave_de_juncao_errada]: recusada: redundante |
| 1360 | 38 | decisao | programa | ao_vivo | 2026-11-03T23:21:58 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1354, `diagnostico`: escolha `imagem_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 1329 (sinal_em_codigo), evento 1327 (arvore_podada), evento 1323 (corpo_http), evento 1330 (verbete_entregue, entidade-produto), evento 1330 (verbete_entregue, contagem_inconsistente), evento 1330 (verbete_entregue, contrato-produto), evento 1334 (resposta), evento 1339 (verbete_citado, entidade-produto), evento 1340 (verbete_citado, contagem_inconsistente); divergência: sim; falha: rotulo_fora_da_taxonomia; prov.used: entidade-produto, contagem_inconsistente, contrato-produto (gen_ai: chat)
- evento 1360, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1329 (sinal_em_codigo), evento 1327 (arvore_podada), evento 1323 (corpo_http), evento 1334 (resposta), evento 1357 (resposta), evento 1359 (verbete_entregue, chave_de_juncao_errada); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: chave_de_juncao_errada, contagem_inconsistente, contrato-produto, entidade-produto

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1316 a 1360 da trilha; hash dos eventos deste caso: `38d4b8933a8fcccb`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
