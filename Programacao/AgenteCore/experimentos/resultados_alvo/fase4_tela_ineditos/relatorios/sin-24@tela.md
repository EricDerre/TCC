<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-24`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/sin-24@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estrutura_aninhada_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê um campo "tipo" como um objeto em vez de um texto, causando confusão na exibição dos produtos.`

Justificativa (gerada por molde): O agente respondeu estrutura_aninhada_divergente no campo tipo porque o sinal tipo: esperado texto, recebido objeto está presente na resposta HTTP e os verbetes estrutura_aninhada_divergente, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 484): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `44439f441a244cf6`):

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
      text "{"valor":"Carnes","moeda":"BRL"}"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "{"valor":"Carnes","moeda":"BRL"}"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "{"valor":"Carnes","moeda":"BRL"}"
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

Poda de `corpo_http` (evento 486): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2404}, depois {"chars": 45}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | texto | objeto |
| tipo | "Carnes" (referência em modo normal) | {"valor": "Carnes", "moeda": "BRL"} em 14 itens |

Trecho podado (hash `8b29b8105a557dd2`):

```text
{"tipo": {"valor": "Carnes", "moeda": "BRL"}}
```

Interceptação (evento 479): `GET /api/produtos` status 200; corpo `8166f86042f25264`, árvore `None`.

## 3. Contraste com a segunda causa

estrutura_aninhada_divergente e não tipo_divergente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: estrutura_aninhada_divergente, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estrutura_aninhada_divergente | 0,99 | sim |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[estrutura_aninhada_divergente] [contrato-produto]`; verbetes citados: `estrutura_aninhada_divergente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `estrutura_aninhada_divergente`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `estrutura_aninhada_divergente`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente`, `colecao_no_lugar_de_objeto` |
| fonte_formato_valido | `[estrutura_aninhada_divergente] [contrato-produto]` | confere | {"ids": ["estrutura_aninhada_divergente", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `estrutura_aninhada_divergente` | confere | {"termo": "estrutura_aninhada_divergente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "estrutura_aninhada_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids sin-24 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 472 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:44:33 | caso sin-24 |
| 473 | 2 | acao | programa | ao_vivo | 2026-11-06T11:44:33 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 156.4, "falhou": false} |
| 474 | 3 | acao | programa | ao_vivo | 2026-11-06T11:44:33 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.5, "falhou": false} |
| 475 | 4 | acao | programa | ao_vivo | 2026-11-06T11:44:33 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.5, "falhou": false} |
| 476 | 5 | acao | programa | ao_vivo | 2026-11-06T11:44:33 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 5.7, "falhou": false} |
| 477 | 6 | acao | programa | ao_vivo | 2026-11-06T11:44:33 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.3, "falhou": false} |
| 479 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T11:44:33 | GET /api/produtos 200 |
| 480 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | conferencia_do_roteiro: confere |
| 481 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | conferencia_do_roteiro: confere |
| 482 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | conferencia_do_roteiro: confere |
| 484 | 11 | poda | programa | ao_vivo | 2026-11-06T11:44:33 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 486 | 12 | poda | programa | ao_vivo | 2026-11-06T11:44:33 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 487 | 13 | candidatos | programa | ao_vivo | 2026-11-06T11:44:33 | 3 de 39 verbetes entregues |
| 489 | 14 | prompt | programa | ao_vivo | 2026-11-06T11:44:33 | {"etapa": "diagnostico", "sha": "f307c8eb7ae6c3c9", "prompt_sha256": "f307c8eb7ae6", "chars": 3992, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 491 | 15 | inferencia | programa | ao_vivo | 2026-11-06T11:44:33 | diagnostico: 82,6 s |
| 492 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:44:33 | causa_raiz: `estrutura_aninhada_divergente` |
| 493 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:44:33 | campo: `tipo` |
| 494 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:44:33 | impacto: `O usuário vê um campo "tipo" como um objeto em vez de um texto, causando confusão na exibição dos produtos.` |
| 495 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:44:33 | fonte: `[estrutura_aninhada_divergente] [contrato-produto]` |
| 496 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:44:33 | fonte_citada: `estrutura_aninhada_divergente` |
| 497 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:44:33 | fonte_citada: `contrato-produto` |
| 498 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | quatro_linhas_presentes: confere |
| 499 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | rotulo_no_conjunto: confere |
| 500 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | fonte_existe_na_biblioteca: confere |
| 501 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | fonte_existe_na_biblioteca: confere |
| 502 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | fonte_estava_no_contexto: confere |
| 503 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | fonte_estava_no_contexto: confere |
| 504 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | campo_existe_no_caso: confere |
| 505 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 506 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | notas_nos_verbetes_citados: informativo |
| 507 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | impacto: nao_verificavel |
| 508 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | fonte_formato_valido: confere |
| 509 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | fonte_contem_termo_da_causa: confere |
| 510 | 34 | verificacao | verificacao | ao_vivo | 2026-11-06T11:44:33 | fonte_contem_termo_da_causa: nao_confere |
| 511 | 35 | decisao | programa | ao_vivo | 2026-11-06T11:44:33 | diagnostico: escolha estrutura_aninhada_divergente; divergência não |

</details>

Nós de decisão:

- evento 511, `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido; evidência: evento 486 (sinal_em_codigo), evento 484 (arvore_podada), evento 479 (corpo_http), evento 487 (verbete_entregue, estrutura_aninhada_divergente), evento 487 (verbete_entregue, contrato-produto), evento 487 (verbete_entregue, colecao_no_lugar_de_objeto), evento 491 (resposta), evento 496 (verbete_citado, estrutura_aninhada_divergente), evento 497 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: estrutura_aninhada_divergente, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 472 a 511 da trilha; hash dos eventos deste caso: `58e18280492a4354`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
