<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `contrato-type_drift#2`: o que o agente fez, declarou e conferiu

Trilha `fase5_agente_b/qwen2.5_7b/contrato-type_drift#2`; modelo `qwen2.5:7b`, Ollama 0.40.16, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê o preço como uma string em vez de um número, o que pode causar problemas na apresentação e cálculos.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal preco: esperado numero, recebido texto está presente na resposta HTTP e os verbetes contrato-produto, entidade-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 533): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 534): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2096}, depois {"chars": 17}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | texto |
| preco | 89.9 (referência em modo normal) | "89.9" em 14 itens |

Trecho podado (hash `b48b1bab39e02551`):

```text
{"preco": "89.9"}
```

Interceptação (evento 529): `GET /api/produtos` status 200; corpo `c7c256cfe391ed57`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, entidade-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [tipo_divergente]`; verbetes citados: `contrato-produto`, `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `contrato-produto`, `entidade-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto`, `entidade-produto`, `tipo_divergente` |
| fonte_formato_valido | `[contrato-produto] [tipo_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "tipo_divergente"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase5_agente_b_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 523 | 1 | entrada | programa | ao_vivo | 2026-11-18T21:50:59 | caso contrato-type_drift#2 |
| 524 | 2 | acao | programa | ao_vivo | 2026-11-18T21:50:59 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 178.1, "url": "produtos_api.php"} |
| 525 | 3 | acao | programa | ao_vivo | 2026-11-18T21:50:59 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 5.9, "url": null} |
| 526 | 4 | acao | programa | ao_vivo | 2026-11-18T21:50:59 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 1.9, "url": null} |
| 527 | 5 | acao | programa | ao_vivo | 2026-11-18T21:50:59 | {"acao": "conferir", "falhou": false, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 3.5, "url": null} |
| 528 | 6 | acao | programa | ao_vivo | 2026-11-18T21:50:59 | {"acao": "conferir", "falhou": false, "passo": 5, "seletor": "#produtos-api-status", "tempo_ms": 5.3, "url": null} |
| 529 | 7 | interceptacao | programa | ao_vivo | 2026-11-18T21:50:59 | GET /api/produtos 200 |
| 530 | 8 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | conferencia_do_roteiro: confere |
| 531 | 9 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | conferencia_do_roteiro: confere |
| 532 | 10 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | conferencia_do_roteiro: confere |
| 533 | 11 | poda | programa | ao_vivo | 2026-11-18T21:50:59 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 534 | 12 | poda | programa | ao_vivo | 2026-11-18T21:50:59 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 535 | 13 | candidatos | programa | ao_vivo | 2026-11-18T21:50:59 | 3 de 39 verbetes entregues |
| 536 | 14 | prompt | programa | ao_vivo | 2026-11-18T21:50:59 | {"chars": 3485, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "d2cd240be596", "sha": "d2cd240be5963f6f"} |
| 538 | 15 | inferencia | programa | ao_vivo | 2026-11-18T21:50:59 | diagnostico: 64,6 s |
| 539 | 16 | declaracao | modelo | ao_vivo | 2026-11-18T21:50:59 | causa_raiz: `tipo_divergente` |
| 540 | 17 | declaracao | modelo | ao_vivo | 2026-11-18T21:50:59 | campo: `preco` |
| 541 | 18 | declaracao | modelo | ao_vivo | 2026-11-18T21:50:59 | impacto: `O usuário vê o preço como uma string em vez de um número, o que pode causar problemas na apresentação e cálculos.` |
| 542 | 19 | declaracao | modelo | ao_vivo | 2026-11-18T21:50:59 | fonte: `[contrato-produto] [tipo_divergente]` |
| 543 | 20 | declaracao | modelo | ao_vivo | 2026-11-18T21:50:59 | fonte_citada: `contrato-produto` |
| 544 | 21 | declaracao | modelo | ao_vivo | 2026-11-18T21:50:59 | fonte_citada: `tipo_divergente` |
| 545 | 22 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | quatro_linhas_presentes: confere |
| 546 | 23 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | rotulo_no_conjunto: confere |
| 547 | 24 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | fonte_existe_na_biblioteca: confere |
| 548 | 25 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | fonte_existe_na_biblioteca: confere |
| 549 | 26 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | fonte_estava_no_contexto: confere |
| 550 | 27 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | fonte_estava_no_contexto: confere |
| 551 | 28 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | campo_existe_no_caso: confere |
| 552 | 29 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 553 | 30 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | notas_nos_verbetes_citados: informativo |
| 554 | 31 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | impacto: nao_verificavel |
| 555 | 32 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | fonte_formato_valido: confere |
| 556 | 33 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | fonte_contem_termo_da_causa: nao_confere |
| 557 | 34 | verificacao | verificacao | ao_vivo | 2026-11-18T21:50:59 | fonte_contem_termo_da_causa: confere |
| 558 | 35 | decisao | programa | ao_vivo | 2026-11-18T21:50:59 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 558, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 534 (sinal_em_codigo), evento 533 (arvore_podada), evento 529 (corpo_http), evento 535 (verbete_entregue, contrato-produto), evento 535 (verbete_entregue, entidade-produto), evento 535 (verbete_entregue, tipo_divergente), evento 538 (resposta), evento 543 (verbete_citado, contrato-produto), evento 544 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: contrato-produto, entidade-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 523 a 558 da trilha; hash dos eventos deste caso: `ec3d8fa62ea8acc7`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
