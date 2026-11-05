<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-3`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/run-3@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `limite_de_requisicoes` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida limite_de_requisicoes

**IMPACTO (declarado):** `O usuário vê uma mensagem de erro indicando que o limite de requisições foi excedido, e a página não carrega os produtos esperados.`

Justificativa (gerada por molde): O agente respondeu limite_de_requisicoes porque o sinal esperado lista, recebido objeto está presente na resposta HTTP e os verbetes contrato-produto, campo_ausente, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida limite_de_requisicoes. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

**Biblioteca:** 1 edição(ões) aplicada(s) ([limite_de_requisicoes]), 0 para revisão humana, 1 recusada(s) (texto_de_origem_proibida) · falha: `texto_de_origem_proibida`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso run-3. A proposta 1 (nota em [contrato-produto]) foi recusada por o filtro especificacao_10 com o código texto_de_origem_proibida: o TEXTO repete um trecho literal do corpo HTTP do caso: "limite de requisiçõe". A proposta 2 (retificacao em [limite_de_requisicoes], peso 2) passou pela validação da Fase 3 e pelos filtros e entrou no lote.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `contrato-produto` | aceita | especificacao_10 | recusada: `texto_de_origem_proibida` | 1 |
| 2 | retificacao | `limite_de_requisicoes` | aceita | nenhum | **aplicada** | 2 |

Poda de `arvore` (evento 461): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 54}, depois {"linhas": 21}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 22 linha(s) da referência | 4 linha(s) novas |

Trecho podado (hash `a9423873e702a2f0`):

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
    text "Erro ao carregar produtos da CobaiaAPI: HTTP 429"
    text "O melhor churrasco da Zona Leste"
    text "Av. Itaquera, 8266 - Itaquera - São Paulo - SP - CEP: 08295000  (11) 2185-9200 ✉"
    link "contato@churrasdafornalha.com.br" href="mailto:contato@churrasdafornalha.com.br?subject=Contato do Site&cc=matheuscs006@gmail.com"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 463): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 43}, depois {"chars": 198}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | lista | objeto |
| id | inteiro |  |
| nome | texto |  |
| resumo | texto\|nulo |  |
| tipo | texto |  |
| preco | numero |  |
| imagem | texto\|nulo |  |
| destaque | booleano |  |
| detail |  | texto |

Trecho podado (hash `48db9ba98a506208`):

```text
{"detail": "limite de requisições excedido", "id": "(ausente)", "nome": "(ausente)", "resumo": "(ausente)", "tipo": "(ausente)", "preco": "(ausente)", "imagem": "(ausente)", "destaque": "(ausente)"}
```

Interceptação (evento 458): `GET /api/produtos` status 429; corpo `de2031cacc5569c2`, árvore `None`.

## 3. Contraste com a segunda causa

limite_de_requisicoes e não tempo_de_resposta_excedido: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, campo_ausente, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| limite_de_requisicoes | 1,00 | sim |
| tempo_de_resposta_excedido | 0,00 |  |
| resposta_truncada | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| tipo_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `campo_ausente`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `limite_de_requisicoes` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "limite_de_requisicoes"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 453 | 1 | entrada | programa | ao_vivo | 2026-11-03T21:49:52 | caso run-3 |
| 454 | 2 | acao | programa | ao_vivo | 2026-11-03T21:49:52 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 85.0, "url": "produtos_api.php"} |
| 455 | 3 | acao | programa | ao_vivo | 2026-11-03T21:49:52 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 7.1, "url": null} |
| 456 | 4 | acao | programa | ao_vivo | 2026-11-03T21:49:52 | {"acao": "conferir", "falhou": true, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 2.1, "url": null} |
| 458 | 5 | interceptacao | programa | ao_vivo | 2026-11-03T21:49:52 | GET /api/produtos 429 |
| 459 | 6 | verificacao | verificacao | ao_vivo | 2026-11-03T21:49:52 | conferencia_do_roteiro: nao_confere |
| 461 | 7 | poda | programa | ao_vivo | 2026-11-03T21:49:52 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 463 | 8 | poda | programa | ao_vivo | 2026-11-03T21:49:52 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 464 | 9 | candidatos | programa | ao_vivo | 2026-11-03T21:49:52 | 3 de 40 verbetes entregues |
| 466 | 10 | prompt | programa | ao_vivo | 2026-11-03T21:49:52 | {"chars": 5661, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "fce968ea6e3e", "sha": "fce968ea6e3e353c"} |
| 468 | 11 | inferencia | programa | ao_vivo | 2026-11-03T21:49:52 | diagnostico: 108,8 s |
| 469 | 12 | declaracao | modelo | ao_vivo | 2026-11-03T21:49:52 | causa_raiz: `limite_de_requisicoes` |
| 470 | 13 | declaracao | modelo | ao_vivo | 2026-11-03T21:49:52 | campo: `nenhum` |
| 471 | 14 | declaracao | modelo | ao_vivo | 2026-11-03T21:49:52 | impacto: `O usuário vê uma mensagem de erro indicando que o limite de requisições foi excedido, e a página não carrega os produtos esperados.` |
| 472 | 15 | declaracao | modelo | ao_vivo | 2026-11-03T21:49:52 | fonte: `[contrato-produto]` |
| 473 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T21:49:52 | fonte_citada: `contrato-produto` |
| 474 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T21:49:52 | quatro_linhas_presentes: confere |
| 475 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T21:49:52 | rotulo_no_conjunto: confere |
| 476 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T21:49:52 | fonte_existe_na_biblioteca: confere |
| 477 | 20 | verificacao | verificacao | ao_vivo | 2026-11-03T21:49:52 | fonte_estava_no_contexto: confere |
| 478 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T21:49:52 | campo_existe_no_caso: nao_se_aplica |
| 479 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T21:49:52 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 480 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T21:49:52 | notas_nos_verbetes_citados: informativo |
| 481 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T21:49:52 | impacto: nao_verificavel |
| 482 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T21:49:52 | fonte_formato_valido: confere |
| 483 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T21:49:52 | fonte_contem_termo_da_causa: nao_confere |
| 484 | 27 | decisao | programa | ao_vivo | 2026-11-03T21:49:52 | diagnostico: escolha limite_de_requisicoes; divergência sim |
| 487 | 28 | inferencia | programa | ao_vivo | 2026-11-03T21:51:45 | proposta: 168,6 s |
| 489 | 29 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:51:45 | proposta 1: nota em [contrato-produto]: recusada: texto_de_origem_proibida |
| 491 | 30 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:51:45 | proposta 2: retificacao em [limite_de_requisicoes]: aplicada |
| 492 | 31 | decisao | programa | ao_vivo | 2026-11-03T21:51:45 | edicao_biblioteca: escolha proposta_2; divergência sim |

</details>

Nós de decisão:

- evento 484, `diagnostico`: escolha `limite_de_requisicoes`; resultado rotulo_emitido; evidência: evento 463 (sinal_em_codigo), evento 461 (arvore_podada), evento 458 (corpo_http), evento 464 (verbete_entregue, contrato-produto), evento 464 (verbete_entregue, campo_ausente), evento 464 (verbete_entregue, colecao_no_lugar_de_objeto), evento 468 (resposta), evento 473 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-produto, campo_ausente, colecao_no_lugar_de_objeto (gen_ai: chat)
- evento 492, `edicao_biblioteca`: escolha `proposta_2`; resultado lote; evidência: evento 463 (sinal_em_codigo), evento 461 (arvore_podada), evento 458 (corpo_http), evento 468 (resposta), evento 487 (resposta), evento 489 (verbete_entregue, contrato-produto), evento 491 (verbete_entregue, limite_de_requisicoes); divergência: sim; falha: texto_de_origem_proibida; prov.used: campo_ausente, colecao_no_lugar_de_objeto, contrato-produto, limite_de_requisicoes

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 453 a 492 da trilha; hash dos eventos deste caso: `3358812a69faac51`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
