<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/sin-21@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estrutura_aninhada_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê um campo "tipo" como um objeto em vez de um texto, causando confusão na exibição dos produtos.`

Justificativa (gerada por molde): O agente respondeu estrutura_aninhada_divergente no campo tipo porque o sinal tipo: esperado texto, recebido objeto está presente na resposta HTTP e os verbetes estrutura_aninhada_divergente, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1554): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1556): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2404}, depois {"chars": 45}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | texto | objeto |
| tipo | "Carnes" (referência em modo normal) | {"valor": "Carnes", "moeda": "BRL"} em 14 itens |

Trecho podado (hash `8b29b8105a557dd2`):

```text
{"tipo": {"valor": "Carnes", "moeda": "BRL"}}
```

Interceptação (evento 1549): `GET /api/produtos` status 200; corpo `8166f86042f25264`, árvore `None`.

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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-21 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1542 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:51:04 | caso sin-21 |
| 1543 | 2 | acao | programa | ao_vivo | 2026-11-06T10:51:04 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 115.8, "falhou": false} |
| 1544 | 3 | acao | programa | ao_vivo | 2026-11-06T10:51:04 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 9.8, "falhou": false} |
| 1545 | 4 | acao | programa | ao_vivo | 2026-11-06T10:51:04 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.7, "falhou": false} |
| 1546 | 5 | acao | programa | ao_vivo | 2026-11-06T10:51:04 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 5.9, "falhou": false} |
| 1547 | 6 | acao | programa | ao_vivo | 2026-11-06T10:51:04 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 4.0, "falhou": false} |
| 1549 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T10:51:04 | GET /api/produtos 200 |
| 1550 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | conferencia_do_roteiro: confere |
| 1551 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | conferencia_do_roteiro: confere |
| 1552 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | conferencia_do_roteiro: confere |
| 1554 | 11 | poda | programa | ao_vivo | 2026-11-06T10:51:04 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1556 | 12 | poda | programa | ao_vivo | 2026-11-06T10:51:04 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1557 | 13 | candidatos | programa | ao_vivo | 2026-11-06T10:51:04 | 3 de 39 verbetes entregues |
| 1559 | 14 | prompt | programa | ao_vivo | 2026-11-06T10:51:04 | {"etapa": "diagnostico", "sha": "f307c8eb7ae6c3c9", "prompt_sha256": "f307c8eb7ae6", "chars": 3992, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1561 | 15 | inferencia | programa | ao_vivo | 2026-11-06T10:51:04 | diagnostico: 83,8 s |
| 1562 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T10:51:04 | causa_raiz: `estrutura_aninhada_divergente` |
| 1563 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T10:51:04 | campo: `tipo` |
| 1564 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T10:51:04 | impacto: `O usuário vê um campo "tipo" como um objeto em vez de um texto, causando confusão na exibição dos produtos.` |
| 1565 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T10:51:04 | fonte: `[estrutura_aninhada_divergente] [contrato-produto]` |
| 1566 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T10:51:04 | fonte_citada: `estrutura_aninhada_divergente` |
| 1567 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T10:51:04 | fonte_citada: `contrato-produto` |
| 1568 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | quatro_linhas_presentes: confere |
| 1569 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | rotulo_no_conjunto: confere |
| 1570 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | fonte_existe_na_biblioteca: confere |
| 1571 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | fonte_existe_na_biblioteca: confere |
| 1572 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | fonte_estava_no_contexto: confere |
| 1573 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | fonte_estava_no_contexto: confere |
| 1574 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | campo_existe_no_caso: confere |
| 1575 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1576 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | notas_nos_verbetes_citados: informativo |
| 1577 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | impacto: nao_verificavel |
| 1578 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | fonte_formato_valido: confere |
| 1579 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | fonte_contem_termo_da_causa: confere |
| 1580 | 34 | verificacao | verificacao | ao_vivo | 2026-11-06T10:51:04 | fonte_contem_termo_da_causa: nao_confere |
| 1581 | 35 | decisao | programa | ao_vivo | 2026-11-06T10:51:04 | diagnostico: escolha estrutura_aninhada_divergente; divergência não |

</details>

Nós de decisão:

- evento 1581, `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido; evidência: evento 1556 (sinal_em_codigo), evento 1554 (arvore_podada), evento 1549 (corpo_http), evento 1557 (verbete_entregue, estrutura_aninhada_divergente), evento 1557 (verbete_entregue, contrato-produto), evento 1557 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1561 (resposta), evento 1566 (verbete_citado, estrutura_aninhada_divergente), evento 1567 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: estrutura_aninhada_divergente, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1542 a 1581 da trilha; hash dos eventos deste caso: `445a923a513bd676`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
