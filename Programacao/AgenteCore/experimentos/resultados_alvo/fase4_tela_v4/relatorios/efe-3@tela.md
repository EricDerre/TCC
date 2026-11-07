<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-3`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/efe-3@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `imagem` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê uma lista de produtos sem imagens, resultando em 14 linhas a menos na tela em comparação com a referência.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo imagem porque o sinal imagem: esperado texto|nulo, recebido None está presente na resposta HTTP e os verbetes contrato-produto, campo_ausente, entidade-produto estavam entre os entregues ao modelo. A segunda causa, chave_de_juncao_errada, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 562): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 179}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 564): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1718}, depois {"chars": 23}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | texto\|nulo |  |

Trecho podado (hash `93e777447b90d3bc`):

```text
{"imagem": "(ausente)"}
```

Interceptação (evento 558): `GET /api/produtos` status 200; corpo `1e2b37492d2f16bd`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não chave_de_juncao_errada: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: contrato-produto, campo_ausente, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,99 | sim |
| chave_de_juncao_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente]`; verbetes citados: `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `contrato-produto`, `campo_ausente`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto`, `campo_ausente` |
| fonte_formato_valido | `[campo_ausente]` | confere | {"ids": ["campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids efe-3 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 551 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:16:39 | caso efe-3 |
| 552 | 2 | acao | programa | ao_vivo | 2026-11-06T10:16:39 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 119.3, "falhou": false} |
| 553 | 3 | acao | programa | ao_vivo | 2026-11-06T10:16:39 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.0, "falhou": false} |
| 554 | 4 | acao | programa | ao_vivo | 2026-11-06T10:16:39 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.1, "falhou": false} |
| 555 | 5 | acao | programa | ao_vivo | 2026-11-06T10:16:39 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 556 | 6 | acao | programa | ao_vivo | 2026-11-06T10:16:39 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.3, "falhou": false} |
| 558 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T10:16:39 | GET /api/produtos 200 |
| 559 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | conferencia_do_roteiro: confere |
| 560 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | conferencia_do_roteiro: confere |
| 561 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | conferencia_do_roteiro: confere |
| 562 | 11 | poda | programa | ao_vivo | 2026-11-06T10:16:39 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 564 | 12 | poda | programa | ao_vivo | 2026-11-06T10:16:39 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 565 | 13 | candidatos | programa | ao_vivo | 2026-11-06T10:16:39 | 3 de 39 verbetes entregues |
| 567 | 14 | prompt | programa | ao_vivo | 2026-11-06T10:16:39 | {"etapa": "diagnostico", "sha": "15bf1362284bffd8", "prompt_sha256": "15bf1362284b", "chars": 3397, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 569 | 15 | inferencia | programa | ao_vivo | 2026-11-06T10:16:39 | diagnostico: 36,7 s |
| 570 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T10:16:39 | causa_raiz: `campo_ausente` |
| 571 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T10:16:39 | campo: `imagem` |
| 572 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T10:16:39 | impacto: `O usuário vê uma lista de produtos sem imagens, resultando em 14 linhas a menos na tela em comparação com a referência.` |
| 573 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T10:16:39 | fonte: `[campo_ausente]` |
| 574 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T10:16:39 | fonte_citada: `campo_ausente` |
| 575 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | quatro_linhas_presentes: confere |
| 576 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | rotulo_no_conjunto: confere |
| 577 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | fonte_existe_na_biblioteca: confere |
| 578 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | fonte_estava_no_contexto: confere |
| 579 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | campo_existe_no_caso: confere |
| 580 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 581 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | notas_nos_verbetes_citados: informativo |
| 582 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | impacto: nao_verificavel |
| 583 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | fonte_formato_valido: confere |
| 584 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T10:16:39 | fonte_contem_termo_da_causa: confere |
| 585 | 31 | decisao | programa | ao_vivo | 2026-11-06T10:16:39 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 585, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 564 (sinal_em_codigo), evento 562 (arvore_podada), evento 558 (corpo_http), evento 565 (verbete_entregue, contrato-produto), evento 565 (verbete_entregue, campo_ausente), evento 565 (verbete_entregue, entidade-produto), evento 569 (resposta), evento 574 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: contrato-produto, campo_ausente, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 551 a 585 da trilha; hash dos eventos deste caso: `fcd201db7c721cbe`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
