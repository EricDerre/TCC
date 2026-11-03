<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_cura/front-busca/texto_alterado/harness/r3`: o que o agente fez, declarou e conferiu

Trilha `fase4_cura/front-busca/texto_alterado/harness/r3`; modelo `(sem modelo: cura de seletor)`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**Cura de seletor:** aplicada: `papel_e_nome` (`role=searchbox[name="search"]`) · reexecução validada · mesmo elemento da referência: sim

Passo 2 do roteiro, localizador `input[placeholder="Buscar produto"]`: TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("input[placeholder=\"Buscar produto\"]") to be visible

Da detecção à reexecução validada: 0,5 s (detecção 2026-11-01T20:00:51; validação 2026-11-01T20:00:51).

Justificativa (gerada por molde): O passo 2 (input[placeholder="Buscar produto"]) falhou: TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("input[placeholder=\"Buscar produto\"]") to be visible. Dos 6 candidatos previstos, 3 foram gerados da árvore podada e do alvo da referência; 3 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome` (role=searchbox[name="search"]), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 0,5 s.

## 2. Evidência

Alvo registrado na corrida de referência: searchbox "search" (ocorrência 1; tag `input`; caminho `#form-busca > div:nth-of-type(1) > input:nth-of-type(1)`; atributos {"id": "buscar", "class": "form-control", "name": "buscar", "type": "search", "placeholder": "Buscar produto", "aria-label": "search"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=searchbox[name="search"]` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.349 s) | **sim** |
| `papel_e_nome_parecido` | não gerado: nenhum searchbox da árvore podada tem nome parecido com "search" acima do limiar 0.6 | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | não gerado: o alvo da referência não tem texto visível | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `#form-busca > div:nth-of-type(1) > input:nth-of-type(1)` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `#form-busca > div:nth-of-type(1) >> role=searchbox >> nth=0` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 410): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 250}, depois {"linhas": 37}.

Trecho podado (hash `6836fa2765f89784`):

```text
document "Churrascaria Fornalha"
  navigation
    link "Logotipo Fornalha"
    link "DESTAQUES" href="index.php#destaques"
    link "PRODUTOS" href="index.php#produtos"
    link "PRODUTOS (API)" href="produtos_api.php"
    button "TIPOS" class="dropdown-toggle"
    link "CONTATO" href="index.php#contato"
    searchbox "search" id="buscar" name="buscar" class="form-control"
  main
    heading "Destaques" level=2
    group
      heading "Picanha ao Alho" level=3
      text "Carnes"
      text "Picanha grelhada com alho laminado na b..."
      button "R$ 89,90" class="btn btn-default disable"
      link "Saiba Mais..." href="produto_detalhes.php?id_produto=1"
    group
      heading "Costelona" level=3
      text "Carnes"
      text "Costela assada lentamente por horas"
      button "R$ 79,90" class="btn btn-default disable"
      link "Saiba Mais..." href="produto_detalhes.php?id_produto=4"
    group
      heading "Cupim" level=3
      text "Carnes"
      text "Cupim assado lentamente, bem macio"
      button "R$ 76,90" class="btn btn-default disable"
      link "Saiba Mais..." href="produto_detalhes.php?id_produto=7"
    text "(mais 16 cartões omitidos pela poda)"
    heading "Produtos Gerais" level=2
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

## 3. Contraste com a segunda causa

`papel_e_nome` (role=searchbox[name="search"]) e não `caminho_do_ancestral_com_id` (#form-busca > div:nth-of-type(1) > input:nth-of-type(1)): o segundo também passou as verificações estáticas, mas vem depois na ordem fixa e o primeiro já tinha levado o roteiro ao fim.

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| papel_e_nome | 5 de 5 verificações | sim |
| caminho_do_ancestral_com_id | 4 de 5 verificações |  |
| posicao_entre_irmaos | 4 de 5 verificações |  |

## 4. FONTE declarada e conferida

Não se aplica: a cura de seletor roda sem modelo; nenhum verbete foi citado.

## 5. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 2 do roteiro, trocar o localizador `input[placeholder="Buscar produto"]` por `role=searchbox[name="search"]` (estratégia `papel_e_nome`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cura --saida fase4_cura_reexec --roteiros front-busca --modos texto_alterado --formas harness --repeticoes 1`

## 6. Árvore completa

<details><summary>18 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 407 | 1 | entrada | programa | ao_vivo | 2026-11-01T20:00:45 | caso None |
| 408 | 2 | acao | programa | ao_vivo | 2026-11-01T20:00:51 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "index.php", "tempo_ms": 180.1, "falhou": false, "reexecucao": 0} |
| 409 | 3 | acao | programa | ao_vivo | 2026-11-01T20:00:51 | {"passo": 2, "acao": "esperar", "seletor": "input[placeholder=\"Buscar produto\"]", "url": null, "tempo_ms": 5012.1, "falhou": true, "reexecucao": 0} |
| 410 | 4 | poda | programa | ao_vivo | 2026-11-01T20:00:51 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 411 | 5 | cura | programa | ao_vivo | 2026-11-01T20:00:51 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 0,5 s |
| 412 | 6 | decisao | programa | ao_vivo | 2026-11-01T20:00:51 | cura: escolha papel_e_nome; divergência sim |
| 413 | 7 | acao | programa | ao_vivo | 2026-11-01T20:00:51 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "index.php", "tempo_ms": 165.7, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado": f |
| 414 | 8 | acao | programa | ao_vivo | 2026-11-01T20:00:51 | {"passo": 2, "acao": "esperar", "seletor": "role=searchbox[name=\"search\"]", "url": null, "tempo_ms": 4.1, "falhou": false, "reexecucao": 1, "candidato": "pape |
| 415 | 9 | acao | programa | ao_vivo | 2026-11-01T20:00:51 | {"passo": 3, "acao": "preencher", "seletor": "role=searchbox[name=\"search\"]", "url": null, "tempo_ms": 7.3, "falhou": false, "reexecucao": 1, "candidato": "pa |
| 416 | 10 | acao | programa | ao_vivo | 2026-11-01T20:00:51 | {"passo": 4, "acao": "clicar", "seletor": "#form-busca button[type=submit]", "url": null, "tempo_ms": 85.1, "falhou": false, "reexecucao": 1, "candidato": "pape |
| 417 | 11 | acao | programa | ao_vivo | 2026-11-01T20:00:51 | {"passo": 5, "acao": "esperar", "seletor": ".thumbnail", "url": null, "tempo_ms": 34.2, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado": |
| 418 | 12 | acao | programa | ao_vivo | 2026-11-01T20:00:51 | {"passo": 6, "acao": "conferir", "seletor": ".thumbnail", "url": null, "tempo_ms": 10.9, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado" |
| 419 | 13 | acao | programa | ao_vivo | 2026-11-01T20:00:51 | {"passo": 7, "acao": "conferir", "seletor": "h2.breadcrumb", "url": null, "tempo_ms": 4.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 420 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T20:00:51 | conferencia_do_roteiro: confere |
| 421 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T20:00:51 | conferencia_do_roteiro: confere |
| 422 | 16 | decisao | programa | ao_vivo | 2026-11-01T20:00:51 | reexecucao: escolha validada; divergência não |
| 423 | 17 | incidente | programa | ao_vivo | 2026-11-01T20:00:51 | {"tipo": "cdn_fora_do_har", "url": "https://code.jquery.com/jquery-2.2.0.min-js", "host": "code.jquery.com", "decisao": "har", "tipo_recurso": "script", "quando |
| 424 | 18 | incidente | programa | ao_vivo | 2026-11-01T20:00:51 | {"tipo": "cdn_fora_do_har", "url": "https://cdn.jsdelivr.net/npm/slick/slick.min.js", "host": "cdn.jsdelivr.net", "decisao": "har", "tipo_recurso": "script", "q |

</details>

Nós de decisão:

- evento 412, `cura`: escolha `papel_e_nome`; resultado cura_aplicada; evidência: evento 411 (candidato_de_seletor), evento 410 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 422, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 411 (candidato_de_seletor), evento 420 (sinal_em_codigo), evento 421 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome

Sem gabarito nem modelo: a cura de seletor é toda em código; a regra R3 separa o mesmo elemento da referência de outro que fez o roteiro passar.

## Rastro

Gerado dos eventos 407 a 424 da trilha; hash dos eventos deste caso: `d44e015435c9479f`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
