<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-25`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/run-25@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,70)

**IMPACTO (declarado):** `O usuário percebeu uma demora significativa na resposta, com 2,0 segundos contra 18 ms no modo normal, o que pode causar insatisfação e atrasos na experiência do usuário.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido no campo tempo_ms porque o sinal tempo_ms: esperado 18 ms (referência em modo normal), recebido 2016 ms está presente na resposta HTTP e os verbetes tempo_de_resposta_excedido, estado_da_tela_divergente, entidade-produto estavam entre os entregues ao modelo. A segunda causa, escala_ou_unidade_errada, ficou com probabilidade 0,24. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,70); trate como hipótese e confira o campo tempo_ms antes de agir.

## 2. Evidência

Poda de `arvore` (evento 1561): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 42}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 0 linha(s) da referência | 0 linha(s) novas |

Trecho podado (hash `667be4c895e37eea`):

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
  dialog
    heading "Cupim" level=4
    text "Cupim assado lentamente, bem macio"

```

Poda de `corpo_http` (evento 1563): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 135}, depois {"chars": 148}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tempo_ms | 18 ms (referência em modo normal) | 2016 ms |

Trecho podado (hash `fa21eb97841ccc71`):

```text
{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}
```

Interceptação (evento 1556): `GET /api/produtos` status 200; corpo `4b1bdd056e7a8c3b`, árvore `None`.

Interceptação (evento 1557): `GET /api/produtos/7` status 200; corpo `dc4fc628e02d16fb`, árvore `None`.

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não escala_ou_unidade_errada: a escolha tem probabilidade 0,70 contra 0,24; verbete(s) na evidência: tempo_de_resposta_excedido, estado_da_tela_divergente, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 0,70 | sim |
| escala_ou_unidade_errada | 0,24 |  |
| tipo_divergente | 0,05 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `tempo_de_resposta_excedido`, `estado_da_tela_divergente`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido` |
| fonte_formato_valido | `[tempo_de_resposta_excedido]` | confere | {"ids": ["tempo_de_resposta_excedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tempo_de_resposta_excedido` | confere | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids run-25 --k 3`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1548 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:26:28 | caso run-25 |
| 1549 | 2 | acao | programa | ao_vivo | 2026-11-06T12:26:59 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 101.2, "falhou": false} |
| 1550 | 3 | acao | programa | ao_vivo | 2026-11-06T12:26:59 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 28485.4, "falhou": false |
| 1551 | 4 | acao | programa | ao_vivo | 2026-11-06T12:26:59 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.9, "falhou": false} |
| 1552 | 5 | acao | programa | ao_vivo | 2026-11-06T12:26:59 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='7']", "url": null, "tempo_ms": 27.2, "falhou": false} |
| 1553 | 6 | acao | programa | ao_vivo | 2026-11-06T12:26:59 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 2393.5, "falhou": false} |
| 1554 | 7 | acao | programa | ao_vivo | 2026-11-06T12:26:59 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 1555 | 8 | acao | programa | ao_vivo | 2026-11-06T12:26:59 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 3.1, "falhou": false} |
| 1556 | 9 | interceptacao | programa | ao_vivo | 2026-11-06T12:26:59 | GET /api/produtos 200 |
| 1557 | 10 | interceptacao | programa | ao_vivo | 2026-11-06T12:26:59 | GET /api/produtos/7 200 |
| 1558 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | conferencia_do_roteiro: confere |
| 1559 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | conferencia_do_roteiro: confere |
| 1560 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | conferencia_do_roteiro: confere |
| 1561 | 14 | poda | programa | ao_vivo | 2026-11-06T12:26:59 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1563 | 15 | poda | programa | ao_vivo | 2026-11-06T12:26:59 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1564 | 16 | candidatos | programa | ao_vivo | 2026-11-06T12:26:59 | 3 de 39 verbetes entregues |
| 1566 | 17 | prompt | programa | ao_vivo | 2026-11-06T12:26:59 | {"etapa": "diagnostico", "sha": "8439e3f68bef1876", "prompt_sha256": "8439e3f68bef", "chars": 3458, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1568 | 18 | inferencia | programa | ao_vivo | 2026-11-06T12:26:59 | diagnostico: 72,0 s |
| 1569 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T12:26:59 | causa_raiz: `tempo_de_resposta_excedido` |
| 1570 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T12:26:59 | campo: `nenhum` |
| 1571 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T12:26:59 | impacto: `O usuário percebeu uma demora significativa na resposta, com 2,0 segundos contra 18 ms no modo normal, o que pode causar insatisfação e atrasos na experiência do usuário.` |
| 1572 | 22 | declaracao | modelo | ao_vivo | 2026-11-06T12:26:59 | fonte: `[tempo_de_resposta_excedido]` |
| 1573 | 23 | declaracao | modelo | ao_vivo | 2026-11-06T12:26:59 | fonte_citada: `tempo_de_resposta_excedido` |
| 1574 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | quatro_linhas_presentes: confere |
| 1575 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | rotulo_no_conjunto: confere |
| 1576 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | fonte_existe_na_biblioteca: confere |
| 1577 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | fonte_estava_no_contexto: confere |
| 1578 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | campo_existe_no_caso: nao_se_aplica |
| 1579 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1580 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | notas_nos_verbetes_citados: informativo |
| 1581 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | impacto: nao_verificavel |
| 1582 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | fonte_formato_valido: confere |
| 1583 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T12:26:59 | fonte_contem_termo_da_causa: confere |
| 1584 | 34 | decisao | programa | ao_vivo | 2026-11-06T12:26:59 | diagnostico: escolha tempo_de_resposta_excedido; divergência não |

</details>

Nós de decisão:

- evento 1584, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 1563 (sinal_em_codigo), evento 1561 (arvore_podada), evento 1557 (corpo_http), evento 1564 (verbete_entregue, tempo_de_resposta_excedido), evento 1564 (verbete_entregue, estado_da_tela_divergente), evento 1564 (verbete_entregue, entidade-produto), evento 1568 (resposta), evento 1573 (verbete_citado, tempo_de_resposta_excedido); divergência: não; falha: nenhuma; prov.used: tempo_de_resposta_excedido, estado_da_tela_divergente, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1548 a 1584 da trilha; hash dos eventos deste caso: `81ec071b32e87fd7`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
