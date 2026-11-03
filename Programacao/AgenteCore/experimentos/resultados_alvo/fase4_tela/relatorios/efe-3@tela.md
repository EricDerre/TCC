<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-3`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/efe-3@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `imagem` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A tela não exibe as imagens dos produtos, causando uma experiência visual incompleta e potencialmente menos atraente para o usuário.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo imagem porque o sinal imagem: esperado texto|nulo, recebido None está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 578): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 179}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 580): regras diff_contra_contrato; antes {"chars": 1718}, depois {"chars": 23}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | texto\|nulo |  |

Trecho podado (hash `93e777447b90d3bc`):

```text
{"imagem": "(ausente)"}
```

Interceptação (evento 574): `GET /api/produtos` status 200; corpo `1e2b37492d2f16bd`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não resposta_truncada: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_ausente, contrato-produto, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 1,00 | sim |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente] [contrato-produto]`; verbetes citados: `campo_ausente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| fonte_formato_valido | `[campo_ausente] [contrato-produto]` | confere | {"ids": ["campo_ausente", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids efe-3 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 567 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:32:39 | caso efe-3 |
| 568 | 2 | acao | programa | ao_vivo | 2026-11-01T11:32:40 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 110.4, "falhou": false} |
| 569 | 3 | acao | programa | ao_vivo | 2026-11-01T11:32:40 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 5.6, "falhou": false} |
| 570 | 4 | acao | programa | ao_vivo | 2026-11-01T11:32:40 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.3, "falhou": false} |
| 571 | 5 | acao | programa | ao_vivo | 2026-11-01T11:32:40 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 3.7, "falhou": false} |
| 572 | 6 | acao | programa | ao_vivo | 2026-11-01T11:32:40 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 574 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T11:32:40 | GET /api/produtos 200 |
| 575 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | conferencia_do_roteiro: confere |
| 576 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | conferencia_do_roteiro: confere |
| 577 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | conferencia_do_roteiro: confere |
| 578 | 11 | poda | programa | ao_vivo | 2026-11-01T11:32:40 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 580 | 12 | poda | programa | ao_vivo | 2026-11-01T11:32:40 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 581 | 13 | candidatos | programa | ao_vivo | 2026-11-01T11:32:40 | 3 de 40 verbetes entregues |
| 583 | 14 | prompt | programa | ao_vivo | 2026-11-01T11:32:40 | {"etapa": "diagnostico", "sha": "758b4964e5c6f58e", "prompt_sha256": "758b4964e5c6", "chars": 5261, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 585 | 15 | inferencia | programa | ao_vivo | 2026-11-01T11:32:40 | diagnostico: 62,4 s |
| 586 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T11:32:40 | causa_raiz: `campo_ausente` |
| 587 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T11:32:40 | campo: `imagem` |
| 588 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T11:32:40 | impacto: `A tela não exibe as imagens dos produtos, causando uma experiência visual incompleta e potencialmente menos atraente para o usuário.` |
| 589 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T11:32:40 | fonte: `[campo_ausente] [contrato-produto]` |
| 590 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T11:32:40 | fonte_citada: `campo_ausente` |
| 591 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T11:32:40 | fonte_citada: `contrato-produto` |
| 592 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | quatro_linhas_presentes: confere |
| 593 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | rotulo_no_conjunto: confere |
| 594 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | fonte_existe_na_biblioteca: confere |
| 595 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | fonte_existe_na_biblioteca: confere |
| 596 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | fonte_estava_no_contexto: confere |
| 597 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | fonte_estava_no_contexto: confere |
| 598 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | campo_existe_no_caso: confere |
| 599 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 600 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | notas_nos_verbetes_citados: informativo |
| 601 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | impacto: nao_verificavel |
| 602 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | fonte_formato_valido: confere |
| 603 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | fonte_contem_termo_da_causa: confere |
| 604 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T11:32:40 | fonte_contem_termo_da_causa: nao_confere |
| 605 | 35 | decisao | programa | ao_vivo | 2026-11-01T11:32:40 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 605, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 580 (sinal_em_codigo), evento 578 (arvore_podada), evento 574 (corpo_http), evento 581 (verbete_entregue, campo_ausente), evento 581 (verbete_entregue, contrato-produto), evento 581 (verbete_entregue, campo_renomeado), evento 585 (resposta), evento 590 (verbete_citado, campo_ausente), evento 591 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 567 a 605 da trilha; hash dos eventos deste caso: `36dad00b567e8e16`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
