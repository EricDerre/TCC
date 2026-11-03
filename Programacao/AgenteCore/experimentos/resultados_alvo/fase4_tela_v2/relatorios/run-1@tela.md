<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/run-1@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,99) · **CONFLITO**: nenhum verbete entregue trata da causa respondida erro_interno_do_servidor

**IMPACTO (declarado):** `O usuário vê uma mensagem de erro indicando que houve um problema ao carregar os produtos da API.`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor porque o sinal esperado lista, recebido objeto está presente na resposta HTTP e os verbetes contrato-produto, campo_ausente, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 3 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida erro_interno_do_servidor. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `arvore` (evento 456): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 54}, depois {"linhas": 21}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 22 linha(s) da referência | 4 linha(s) novas |

Trecho podado (hash `e9b6b8fff9529555`):

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
    text "Erro ao carregar produtos da CobaiaAPI: HTTP 500"
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

Poda de `corpo_http` (evento 458): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 50}, depois {"chars": 205}.

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

Trecho podado (hash `76e7cf76cde2ae11`):

```text
{"detail": "fault injection: error_500 em produto", "id": "(ausente)", "nome": "(ausente)", "resumo": "(ausente)", "tipo": "(ausente)", "preco": "(ausente)", "imagem": "(ausente)", "destaque": "(ausente)"}
```

Interceptação (evento 453): `GET /api/produtos` status 500; corpo `24067faf5d61b7b3`, árvore `None`.

## 3. Contraste com a segunda causa

erro_interno_do_servidor e não resposta_truncada: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: contrato-produto, campo_ausente, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 0,99 | sim |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| codificacao_incorreta | 0,00 |  |
| tipo_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [campo_ausente], [colecao_no_lugar_de_objeto]`; verbetes citados: `contrato-produto`, `campo_ausente`, `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `campo_ausente`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `contrato-produto`, `campo_ausente`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `contrato-produto`, `campo_ausente`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto], [campo_ausente], [colecao_no_lugar_de_objeto]` | confere | {"ids": ["contrato-produto", "campo_ausente", "colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "erro_interno_do_servidor"} |
| fonte_contem_termo_da_causa | `campo_ausente` | **não confere** | {"termo": "erro_interno_do_servidor"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | **não confere** | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids run-1 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 448 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:25:20 | caso run-1 |
| 449 | 2 | acao | programa | ao_vivo | 2026-11-01T14:25:20 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 119.5, "falhou": false} |
| 450 | 3 | acao | programa | ao_vivo | 2026-11-01T14:25:20 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 5.4, "falhou": false} |
| 451 | 4 | acao | programa | ao_vivo | 2026-11-01T14:25:20 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.4, "falhou": true} |
| 453 | 5 | interceptacao | programa | ao_vivo | 2026-11-01T14:25:20 | GET /api/produtos 500 |
| 454 | 6 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | conferencia_do_roteiro: nao_confere |
| 456 | 7 | poda | programa | ao_vivo | 2026-11-01T14:25:20 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 458 | 8 | poda | programa | ao_vivo | 2026-11-01T14:25:20 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 459 | 9 | candidatos | programa | ao_vivo | 2026-11-01T14:25:20 | 3 de 40 verbetes entregues |
| 461 | 10 | prompt | programa | ao_vivo | 2026-11-01T14:25:20 | {"etapa": "diagnostico", "sha": "77a01cfc61762ae3", "prompt_sha256": "77a01cfc6176", "chars": 5669, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 463 | 11 | inferencia | programa | ao_vivo | 2026-11-01T14:25:20 | diagnostico: 100,4 s |
| 464 | 12 | declaracao | modelo | ao_vivo | 2026-11-01T14:25:20 | causa_raiz: `erro_interno_do_servidor` |
| 465 | 13 | declaracao | modelo | ao_vivo | 2026-11-01T14:25:20 | campo: `nenhum` |
| 466 | 14 | declaracao | modelo | ao_vivo | 2026-11-01T14:25:20 | impacto: `O usuário vê uma mensagem de erro indicando que houve um problema ao carregar os produtos da API.` |
| 467 | 15 | declaracao | modelo | ao_vivo | 2026-11-01T14:25:20 | fonte: `[contrato-produto], [campo_ausente], [colecao_no_lugar_de_objeto]` |
| 468 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T14:25:20 | fonte_citada: `contrato-produto` |
| 469 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T14:25:20 | fonte_citada: `campo_ausente` |
| 470 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T14:25:20 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 471 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | quatro_linhas_presentes: confere |
| 472 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | rotulo_no_conjunto: confere |
| 473 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | fonte_existe_na_biblioteca: confere |
| 474 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | fonte_existe_na_biblioteca: confere |
| 475 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | fonte_existe_na_biblioteca: confere |
| 476 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | fonte_estava_no_contexto: confere |
| 477 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | fonte_estava_no_contexto: confere |
| 478 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | fonte_estava_no_contexto: confere |
| 479 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | campo_existe_no_caso: nao_se_aplica |
| 480 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 481 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | notas_nos_verbetes_citados: informativo |
| 482 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | impacto: nao_verificavel |
| 483 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | fonte_formato_valido: confere |
| 484 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | fonte_contem_termo_da_causa: nao_confere |
| 485 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | fonte_contem_termo_da_causa: nao_confere |
| 486 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T14:25:20 | fonte_contem_termo_da_causa: nao_confere |
| 487 | 35 | decisao | programa | ao_vivo | 2026-11-01T14:25:20 | diagnostico: escolha erro_interno_do_servidor; divergência sim |

</details>

Nós de decisão:

- evento 487, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 458 (sinal_em_codigo), evento 456 (arvore_podada), evento 453 (corpo_http), evento 459 (verbete_entregue, contrato-produto), evento 459 (verbete_entregue, campo_ausente), evento 459 (verbete_entregue, colecao_no_lugar_de_objeto), evento 463 (resposta), evento 468 (verbete_citado, contrato-produto), evento 469 (verbete_citado, campo_ausente), evento 470 (verbete_citado, colecao_no_lugar_de_objeto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-produto, campo_ausente, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 448 a 487 da trilha; hash dos eventos deste caso: `0628310b41eaea69`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
