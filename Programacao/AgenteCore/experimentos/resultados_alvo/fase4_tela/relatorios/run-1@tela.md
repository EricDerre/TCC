<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/run-1@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,99) · **CONFLITO**: nenhum verbete entregue trata da causa respondida erro_interno_do_servidor

**IMPACTO (declarado):** `O usuário vê uma mensagem de erro inesperada na página, sem os dados esperados de produtos.`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor porque o sinal esperado lista, recebido objeto está presente na resposta HTTP e os verbetes contrato-produto, campo_ausente, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida erro_interno_do_servidor. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `arvore` (evento 454): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 54}, depois {"linhas": 21}.

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

Poda de `corpo_http` (evento 456): regras diff_contra_contrato; antes {"chars": 50}, depois {"chars": 205}.

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

Interceptação (evento 451): `GET /api/produtos` status 500; corpo `24067faf5d61b7b3`, árvore `None`.

## 3. Contraste com a segunda causa

erro_interno_do_servidor e não campo_ausente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: contrato-produto, campo_ausente, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 0,99 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| codificacao_incorreta | 0,00 |  |
| tipo_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [campo_ausente]`; verbetes citados: `contrato-produto`, `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `campo_ausente`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `contrato-produto`, `campo_ausente`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto], [campo_ausente]` | confere | {"ids": ["contrato-produto", "campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "erro_interno_do_servidor"} |
| fonte_contem_termo_da_causa | `campo_ausente` | **não confere** | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids run-1 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 446 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:27:37 | caso run-1 |
| 447 | 2 | acao | programa | ao_vivo | 2026-11-01T11:27:38 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 108.0, "falhou": false} |
| 448 | 3 | acao | programa | ao_vivo | 2026-11-01T11:27:38 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 5.3, "falhou": false} |
| 449 | 4 | acao | programa | ao_vivo | 2026-11-01T11:27:38 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.4, "falhou": true} |
| 451 | 5 | interceptacao | programa | ao_vivo | 2026-11-01T11:27:38 | GET /api/produtos 500 |
| 452 | 6 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | conferencia_do_roteiro: nao_confere |
| 454 | 7 | poda | programa | ao_vivo | 2026-11-01T11:27:38 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 456 | 8 | poda | programa | ao_vivo | 2026-11-01T11:27:38 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato |
| 457 | 9 | candidatos | programa | ao_vivo | 2026-11-01T11:27:38 | 3 de 40 verbetes entregues |
| 459 | 10 | prompt | programa | ao_vivo | 2026-11-01T11:27:38 | {"etapa": "diagnostico", "sha": "77c330c08569b730", "prompt_sha256": "77c330c08569", "chars": 5539, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 461 | 11 | inferencia | programa | ao_vivo | 2026-11-01T11:27:38 | diagnostico: 97,4 s |
| 462 | 12 | declaracao | modelo | ao_vivo | 2026-11-01T11:27:38 | causa_raiz: `erro_interno_do_servidor` |
| 463 | 13 | declaracao | modelo | ao_vivo | 2026-11-01T11:27:38 | campo: `nenhum` |
| 464 | 14 | declaracao | modelo | ao_vivo | 2026-11-01T11:27:38 | impacto: `O usuário vê uma mensagem de erro inesperada na página, sem os dados esperados de produtos.` |
| 465 | 15 | declaracao | modelo | ao_vivo | 2026-11-01T11:27:38 | fonte: `[contrato-produto], [campo_ausente]` |
| 466 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T11:27:38 | fonte_citada: `contrato-produto` |
| 467 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T11:27:38 | fonte_citada: `campo_ausente` |
| 468 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | quatro_linhas_presentes: confere |
| 469 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | rotulo_no_conjunto: confere |
| 470 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | fonte_existe_na_biblioteca: confere |
| 471 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | fonte_existe_na_biblioteca: confere |
| 472 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | fonte_estava_no_contexto: confere |
| 473 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | fonte_estava_no_contexto: confere |
| 474 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | campo_existe_no_caso: nao_se_aplica |
| 475 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 476 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | notas_nos_verbetes_citados: informativo |
| 477 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | impacto: nao_verificavel |
| 478 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | fonte_formato_valido: confere |
| 479 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | fonte_contem_termo_da_causa: nao_confere |
| 480 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T11:27:38 | fonte_contem_termo_da_causa: nao_confere |
| 481 | 31 | decisao | programa | ao_vivo | 2026-11-01T11:27:38 | diagnostico: escolha erro_interno_do_servidor; divergência sim |

</details>

Nós de decisão:

- evento 481, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 456 (sinal_em_codigo), evento 454 (arvore_podada), evento 451 (corpo_http), evento 457 (verbete_entregue, contrato-produto), evento 457 (verbete_entregue, campo_ausente), evento 457 (verbete_entregue, colecao_no_lugar_de_objeto), evento 461 (resposta), evento 466 (verbete_citado, contrato-produto), evento 467 (verbete_citado, campo_ausente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-produto, campo_ausente, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 446 a 481 da trilha; hash dos eventos deste caso: `174259068b060f5e`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
