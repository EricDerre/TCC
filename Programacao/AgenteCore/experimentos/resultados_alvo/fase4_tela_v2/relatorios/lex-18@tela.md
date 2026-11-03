<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-18`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/lex-18@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `formato_de_data_divergente` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,21) · **CONFLITO**: nenhum verbete entregue trata da causa respondida formato_de_data_divergente

**IMPACTO (declarado):** `A interface exibe preços com acentos ausentes e textos com acentos substituídos por underscores, o que causa confusão visual para o usuário.`

Justificativa (gerada por molde): O agente respondeu formato_de_data_divergente no campo resumo porque o sinal resumo: esperado "Garrafa 500ml, com ou sem gás" (referência em modo normal), recebido "Garrafa 500ml, com ou sem gÃ¡s" em 4 itens está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, contagem_inconsistente, ficou com probabilidade 0,16. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida formato_de_data_divergente. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,21); trate como hipótese e confira o campo resumo antes de agir.

## 2. Evidência

Poda de `arvore` (evento 1422): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1423): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2073}, depois {"chars": 412}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| resumo | "Garrafa 500ml, com ou sem gás" (referência em modo normal) | "Garrafa 500ml, com ou sem gÃ¡s" em 4 itens |

Trecho podado (hash `274a6c69751a98f7`):

```text
lista com 14 itens (referência em modo normal: 14); resumo diferente em 4 itens; por exemplo: {"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gÃ¡s", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}; {"id": 11, "nome": "Pão de Alho", "resumo": "PÃ£o de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}
```

Interceptação (evento 1418): `GET /api/produtos` status 200; corpo `40dfa78ee8bc48ac`, árvore `None`.

## 3. Contraste com a segunda causa

formato_de_data_divergente e não contagem_inconsistente: a escolha tem probabilidade 0,21 contra 0,16; verbete(s) na evidência: entidade-produto, contrato-produto, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| formato_de_data_divergente | 0,21 | sim |
| contagem_inconsistente | 0,16 |  |
| estrutura_aninhada_divergente | 0,15 |  |
| colecao_no_lugar_de_objeto | 0,10 |  |
| campo_ausente | 0,09 |  |
| campo_renomeado | 0,09 |  |
| valor_fora_do_dominio | 0,07 |  |
| tipo_divergente | 0,06 |  |
| corpo_nao_e_json | 0,05 |  |
| corpo_vazio | 0,05 |  |
| resposta_truncada | 0,05 |  |
| codificacao_incorreta | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "formato_de_data_divergente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "formato_de_data_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids lex-18 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1412 | 1 | entrada | programa | ao_vivo | 2026-11-01T15:02:42 | caso lex-18 |
| 1413 | 2 | acao | programa | ao_vivo | 2026-11-01T15:02:42 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 105.3, "falhou": false} |
| 1414 | 3 | acao | programa | ao_vivo | 2026-11-01T15:02:42 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.7, "falhou": false} |
| 1415 | 4 | acao | programa | ao_vivo | 2026-11-01T15:02:42 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.9, "falhou": false} |
| 1416 | 5 | acao | programa | ao_vivo | 2026-11-01T15:02:42 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 7.1, "falhou": false} |
| 1417 | 6 | acao | programa | ao_vivo | 2026-11-01T15:02:42 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 6.1, "falhou": false} |
| 1418 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T15:02:42 | GET /api/produtos 200 |
| 1419 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | conferencia_do_roteiro: confere |
| 1420 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | conferencia_do_roteiro: confere |
| 1421 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | conferencia_do_roteiro: confere |
| 1422 | 11 | poda | programa | ao_vivo | 2026-11-01T15:02:42 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1423 | 12 | poda | programa | ao_vivo | 2026-11-01T15:02:42 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1424 | 13 | candidatos | programa | ao_vivo | 2026-11-01T15:02:42 | 3 de 40 verbetes entregues |
| 1426 | 14 | prompt | programa | ao_vivo | 2026-11-01T15:02:42 | {"etapa": "diagnostico", "sha": "cde3decc199f1135", "prompt_sha256": "cde3decc199f", "chars": 6104, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1428 | 15 | inferencia | programa | ao_vivo | 2026-11-01T15:02:42 | diagnostico: 82,0 s |
| 1429 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T15:02:42 | causa_raiz: `formato_de_data_divergente` |
| 1430 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T15:02:42 | campo: `nenhum` |
| 1431 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T15:02:42 | impacto: `A interface exibe preços com acentos ausentes e textos com acentos substituídos por underscores, o que causa confusão visual para o usuário.` |
| 1432 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T15:02:42 | fonte: `[entidade-produto], [contrato-produto]` |
| 1433 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T15:02:42 | fonte_citada: `entidade-produto` |
| 1434 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T15:02:42 | fonte_citada: `contrato-produto` |
| 1435 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | quatro_linhas_presentes: confere |
| 1436 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | rotulo_no_conjunto: confere |
| 1437 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | fonte_existe_na_biblioteca: confere |
| 1438 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | fonte_existe_na_biblioteca: confere |
| 1439 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | fonte_estava_no_contexto: confere |
| 1440 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | fonte_estava_no_contexto: confere |
| 1441 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | campo_existe_no_caso: nao_se_aplica |
| 1442 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1443 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | notas_nos_verbetes_citados: informativo |
| 1444 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | impacto: nao_verificavel |
| 1445 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | fonte_formato_valido: confere |
| 1446 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | fonte_contem_termo_da_causa: nao_confere |
| 1447 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T15:02:42 | fonte_contem_termo_da_causa: nao_confere |
| 1448 | 35 | decisao | programa | ao_vivo | 2026-11-01T15:02:42 | diagnostico: escolha formato_de_data_divergente; divergência sim |

</details>

Nós de decisão:

- evento 1448, `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido; evidência: evento 1423 (sinal_em_codigo), evento 1422 (arvore_podada), evento 1418 (corpo_http), evento 1424 (verbete_entregue, entidade-produto), evento 1424 (verbete_entregue, contrato-produto), evento 1424 (verbete_entregue, contagem_inconsistente), evento 1428 (resposta), evento 1433 (verbete_citado, entidade-produto), evento 1434 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1412 a 1448 da trilha; hash dos eventos deste caso: `0c14611ddba86b16`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
