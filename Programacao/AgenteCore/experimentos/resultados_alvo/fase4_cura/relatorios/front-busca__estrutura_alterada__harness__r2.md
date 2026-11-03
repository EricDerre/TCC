<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_cura/front-busca/estrutura_alterada/harness/r2`: o que o agente fez, declarou e conferiu

Trilha `fase4_cura/front-busca/estrutura_alterada/harness/r2`; modelo `(sem modelo: cura de seletor)`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**Cura de seletor:** aplicada: `papel_e_nome` (`role=searchbox[name="search"]`) · reexecução validada · mesmo elemento da referência: sim

Passo 2 do roteiro, localizador `#form-busca > div > input`: TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("#form-busca > div > input") to be visible

Da detecção à reexecução validada: 0,5 s (detecção 2026-11-01T20:01:44; validação 2026-11-01T20:01:44).

Justificativa (gerada por molde): O passo 2 (#form-busca > div > input) falhou: TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("#form-busca > div > input") to be visible. Dos 6 candidatos previstos, 3 foram gerados da árvore podada e do alvo da referência; 2 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome` (role=searchbox[name="search"]), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 0,5 s.

## 2. Evidência

Alvo registrado na corrida de referência: searchbox "search" (ocorrência 1; tag `input`; caminho `#form-busca > div:nth-of-type(1) > input:nth-of-type(1)`; atributos {"id": "buscar", "class": "form-control", "name": "buscar", "type": "search", "placeholder": "Buscar produto", "aria-label": "search"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=searchbox[name="search"]` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.377 s) | **sim** |
| `papel_e_nome_parecido` | não gerado: nenhum searchbox da árvore podada tem nome parecido com "search" acima do limiar 0.6 | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | não gerado: o alvo da referência não tem texto visível | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `#form-busca > div:nth-of-type(1) > input:nth-of-type(1)` | **não confere** | não se aplica | não se aplica | não se aplica | não tentado |  |
| `posicao_entre_irmaos` | `#form-busca > div:nth-of-type(1) >> role=searchbox >> nth=0` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 574): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 250}, depois {"linhas": 37}.

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

`papel_e_nome` (role=searchbox[name="search"]) e não `posicao_entre_irmaos` (#form-busca > div:nth-of-type(1) >> role=searchbox >> nth=0): o segundo também passou as verificações estáticas, mas vem depois na ordem fixa e o primeiro já tinha levado o roteiro ao fim.

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| papel_e_nome | 5 de 5 verificações | sim |
| posicao_entre_irmaos | 4 de 5 verificações |  |
| caminho_do_ancestral_com_id | 0 de 5 verificações |  |

## 4. FONTE declarada e conferida

Não se aplica: a cura de seletor roda sem modelo; nenhum verbete foi citado.

## 5. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 2 do roteiro, trocar o localizador `#form-busca > div > input` por `role=searchbox[name="search"]` (estratégia `papel_e_nome`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cura --saida fase4_cura_reexec --roteiros front-busca --modos estrutura_alterada --formas harness --repeticoes 1`

## 6. Árvore completa

<details><summary>18 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 571 | 1 | entrada | programa | ao_vivo | 2026-11-01T20:01:38 | caso None |
| 572 | 2 | acao | programa | ao_vivo | 2026-11-01T20:01:44 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "index.php", "tempo_ms": 182.5, "falhou": false, "reexecucao": 0} |
| 573 | 3 | acao | programa | ao_vivo | 2026-11-01T20:01:44 | {"passo": 2, "acao": "esperar", "seletor": "#form-busca > div > input", "url": null, "tempo_ms": 5004.0, "falhou": true, "reexecucao": 0} |
| 574 | 4 | poda | programa | ao_vivo | 2026-11-01T20:01:44 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 575 | 5 | cura | programa | ao_vivo | 2026-11-01T20:01:44 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 0,5 s |
| 576 | 6 | decisao | programa | ao_vivo | 2026-11-01T20:01:44 | cura: escolha papel_e_nome; divergência sim |
| 577 | 7 | acao | programa | ao_vivo | 2026-11-01T20:01:44 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "index.php", "tempo_ms": 177.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado": f |
| 578 | 8 | acao | programa | ao_vivo | 2026-11-01T20:01:44 | {"passo": 2, "acao": "esperar", "seletor": "role=searchbox[name=\"search\"]", "url": null, "tempo_ms": 4.6, "falhou": false, "reexecucao": 1, "candidato": "pape |
| 579 | 9 | acao | programa | ao_vivo | 2026-11-01T20:01:44 | {"passo": 3, "acao": "preencher", "seletor": "role=searchbox[name=\"search\"]", "url": null, "tempo_ms": 5.9, "falhou": false, "reexecucao": 1, "candidato": "pa |
| 580 | 10 | acao | programa | ao_vivo | 2026-11-01T20:01:44 | {"passo": 4, "acao": "clicar", "seletor": "#form-busca button[type=submit]", "url": null, "tempo_ms": 99.7, "falhou": false, "reexecucao": 1, "candidato": "pape |
| 581 | 11 | acao | programa | ao_vivo | 2026-11-01T20:01:44 | {"passo": 5, "acao": "esperar", "seletor": ".thumbnail", "url": null, "tempo_ms": 32.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado": |
| 582 | 12 | acao | programa | ao_vivo | 2026-11-01T20:01:44 | {"passo": 6, "acao": "conferir", "seletor": ".thumbnail", "url": null, "tempo_ms": 11.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado" |
| 583 | 13 | acao | programa | ao_vivo | 2026-11-01T20:01:44 | {"passo": 7, "acao": "conferir", "seletor": "h2.breadcrumb", "url": null, "tempo_ms": 5.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 584 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T20:01:44 | conferencia_do_roteiro: confere |
| 585 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T20:01:44 | conferencia_do_roteiro: confere |
| 586 | 16 | decisao | programa | ao_vivo | 2026-11-01T20:01:44 | reexecucao: escolha validada; divergência não |
| 587 | 17 | incidente | programa | ao_vivo | 2026-11-01T20:01:44 | {"tipo": "cdn_fora_do_har", "url": "https://code.jquery.com/jquery-2.2.0.min-js", "host": "code.jquery.com", "decisao": "har", "tipo_recurso": "script", "quando |
| 588 | 18 | incidente | programa | ao_vivo | 2026-11-01T20:01:44 | {"tipo": "cdn_fora_do_har", "url": "https://cdn.jsdelivr.net/npm/slick/slick.min.js", "host": "cdn.jsdelivr.net", "decisao": "har", "tipo_recurso": "script", "q |

</details>

Nós de decisão:

- evento 576, `cura`: escolha `papel_e_nome`; resultado cura_aplicada; evidência: evento 575 (candidato_de_seletor), evento 574 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 586, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 575 (candidato_de_seletor), evento 584 (sinal_em_codigo), evento 585 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome

Sem gabarito nem modelo: a cura de seletor é toda em código; a regra R3 separa o mesmo elemento da referência de outro que fez o roteiro passar.

## Rastro

Gerado dos eventos 571 a 588 da trilha; hash dos eventos deste caso: `903ffc8ab4095a83`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
