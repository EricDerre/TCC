<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_cura/front-admin-produtos/texto_alterado/php/r1`: o que o agente fez, declarou e conferiu

Trilha `fase4_cura/front-admin-produtos/texto_alterado/php/r1`; modelo `(sem modelo: cura de seletor)`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**Cura de seletor:** aplicada: `papel_e_nome_parecido` (`role=button[name=" EXCLUIR ITEM"] >> nth=0`) · reexecução validada · mesmo elemento da referência: sim

Passo 11 do roteiro, localizador `role=button[name=/EXCLUIR$/] >> nth=0`: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("role=button[name=/EXCLUIR$/]").first

Da detecção à reexecução validada: 0,8 s (detecção 2026-11-01T20:09:03; validação 2026-11-01T20:09:04).

Justificativa (gerada por molde): O passo 11 (role=button[name=/EXCLUIR$/] >> nth=0) falhou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("role=button[name=/EXCLUIR$/]").first. Dos 6 candidatos previstos, 5 foram gerados da árvore podada e do alvo da referência; 4 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome_parecido` (role=button[name=" EXCLUIR ITEM"] >> nth=0), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 0,8 s.

## 2. Evidência

Alvo registrado na corrida de referência: button " EXCLUIR" (ocorrência 1; tag `button`; caminho `body > main:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(7) > button:nth-of-type(1)`; atributos {"class": "delete btn btn-xs btn-block btn-danger", "data-id": "1", "data-nome": "Picanha ao Alho"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | não gerado: a árvore podada não tem button " EXCLUIR" | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | confere | confere | confere | confere (" EXCLUIR ITEM" contra " EXCLUIR": similaridade 0.78 (limiar 0.6)) | confere (o roteiro chegou ao fim: 3 conferência(s) passaram em 0.64 s) | **sim** |
| `texto_contido` | `text=EXCLUIR >> nth=0` | confere | confere | **não confere** | confere ("EXCLUIR ITEM" contra " EXCLUIR": similaridade 0.67 (limiar 0.6)) | não tentado |  |
| `data_id` | `button[data-id="1"]` | confere | confere | confere | confere (" EXCLUIR ITEM" contra " EXCLUIR": similaridade 0.78 (limiar 0.6)) | não tentado |  |
| `caminho_do_ancestral_com_id` | `body > main:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(7) > button:nth-of-type(1)` | confere | confere | confere | confere (" EXCLUIR ITEM" contra " EXCLUIR": similaridade 0.78 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `body > main:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(7) >> role=button >> nth=1` | confere | confere | confere | confere (" EXCLUIR ITEM" contra " EXCLUIR": similaridade 0.78 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 2388): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 170}, depois {"linhas": 38}.

Trecho podado (hash `837d2e4dbe768226`):

```text
document "Produtos - Lista"
  navigation
    button "Olá, admin!" class="btn btn-danger navbar-btn disabled"
    link "ADMIN" href="index.php"
    link "PRODUTOS" href="produtos_lista.php"
    link "TIPOS" href="tipos_lista.php"
    link "USUÁRIOS" href="usuarios_lista.php"
  main
    heading "Lista de Produtos" level=2
    button "ADICIONAR" class="btn btn-block btn-primary btn-xs" href="produtos_insere.php"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"
    button " ALTERAR"
    button " EXCLUIR ITEM"

```

## 3. Contraste com a segunda causa

`papel_e_nome_parecido` (role=button[name=" EXCLUIR ITEM"] >> nth=0) e não `data_id` (button[data-id="1"]): o segundo também passou as verificações estáticas, mas vem depois na ordem fixa e o primeiro já tinha levado o roteiro ao fim.

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| papel_e_nome_parecido | 5 de 5 verificações | sim |
| data_id | 4 de 5 verificações |  |
| caminho_do_ancestral_com_id | 4 de 5 verificações |  |
| posicao_entre_irmaos | 4 de 5 verificações |  |
| texto_contido | 3 de 5 verificações |  |

## 4. FONTE declarada e conferida

Não se aplica: a cura de seletor roda sem modelo; nenhum verbete foi citado.

## 5. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 11 do roteiro, trocar o localizador `role=button[name=/EXCLUIR$/] >> nth=0` por `role=button[name=" EXCLUIR ITEM"] >> nth=0` (estratégia `papel_e_nome_parecido`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cura --saida fase4_cura_reexec --roteiros front-admin-produtos --modos texto_alterado --formas php --repeticoes 1`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2374 | 1 | entrada | programa | ao_vivo | 2026-11-01T20:08:57 | caso None |
| 2375 | 2 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 88.4, "falhou": false, "reexecucao": 0} |
| 2376 | 3 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 19.6, "falhou": false, "reexecucao": 0} |
| 2377 | 4 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 15.2, "falhou": false, "reexecucao": 0} |
| 2378 | 5 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 5.5, "falhou": false, "reexecucao": 0} |
| 2379 | 6 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 5, "acao": "clicar", "seletor": "button[type=submit]", "url": null, "tempo_ms": 93.9, "falhou": false, "reexecucao": 0} |
| 2380 | 7 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 6, "acao": "esperar", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 69.9, "falhou": false, "reexecucao": 0} |
| 2381 | 8 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 7, "acao": "abrir", "seletor": null, "url": "admin/produtos_lista.php", "tempo_ms": 163.5, "falhou": false, "reexecucao": 0} |
| 2382 | 9 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 8, "acao": "esperar", "seletor": "table.table tbody tr", "url": null, "tempo_ms": 17.6, "falhou": false, "reexecucao": 0} |
| 2383 | 10 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 9, "acao": "conferir", "seletor": "table.table tbody tr", "url": null, "tempo_ms": 10.0, "falhou": false, "reexecucao": 0} |
| 2384 | 11 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 10, "acao": "conferir", "seletor": "h2.breadcrumb", "url": null, "tempo_ms": 3.7, "falhou": false, "reexecucao": 0} |
| 2385 | 12 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 11, "acao": "clicar", "seletor": "role=button[name=/EXCLUIR$/] >> nth=0", "url": null, "tempo_ms": 5011.7, "falhou": true, "reexecucao": 0} |
| 2386 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T20:09:04 | conferencia_do_roteiro: confere |
| 2387 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T20:09:04 | conferencia_do_roteiro: confere |
| 2388 | 15 | poda | programa | ao_vivo | 2026-11-01T20:09:04 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 2389 | 16 | cura | programa | ao_vivo | 2026-11-01T20:09:04 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome_parecido; MTTR 0,8 s |
| 2390 | 17 | decisao | programa | ao_vivo | 2026-11-01T20:09:04 | cura: escolha papel_e_nome_parecido; divergência sim |
| 2391 | 18 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 88.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_parecido |
| 2392 | 19 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 20.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_parecid |
| 2393 | 20 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 14.9, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_parec |
| 2394 | 21 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 5.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_pareci |
| 2395 | 22 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 5, "acao": "clicar", "seletor": "button[type=submit]", "url": null, "tempo_ms": 88.3, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_par |
| 2396 | 23 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 6, "acao": "esperar", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 67.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_parecido |
| 2397 | 24 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 7, "acao": "abrir", "seletor": null, "url": "admin/produtos_lista.php", "tempo_ms": 76.6, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome |
| 2398 | 25 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 8, "acao": "esperar", "seletor": "table.table tbody tr", "url": null, "tempo_ms": 19.2, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_p |
| 2399 | 26 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 9, "acao": "conferir", "seletor": "table.table tbody tr", "url": null, "tempo_ms": 9.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_p |
| 2400 | 27 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 10, "acao": "conferir", "seletor": "h2.breadcrumb", "url": null, "tempo_ms": 3.6, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_parecid |
| 2401 | 28 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 11, "acao": "clicar", "seletor": "role=button[name=\" EXCLUIR ITEM\"] >> nth=0", "url": null, "tempo_ms": 15.2, "falhou": false, "reexecucao": 1, "ca |
| 2402 | 29 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 12, "acao": "esperar", "seletor": "#modalEdit", "url": null, "tempo_ms": 215.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_parecido" |
| 2403 | 30 | acao | programa | ao_vivo | 2026-11-01T20:09:04 | {"passo": 13, "acao": "conferir", "seletor": "#modalEdit span.nome", "url": null, "tempo_ms": 3.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_ |
| 2404 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T20:09:04 | conferencia_do_roteiro: confere |
| 2405 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T20:09:04 | conferencia_do_roteiro: confere |
| 2406 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T20:09:04 | conferencia_do_roteiro: confere |
| 2407 | 34 | decisao | programa | ao_vivo | 2026-11-01T20:09:04 | reexecucao: escolha validada; divergência não |

</details>

Nós de decisão:

- evento 2390, `cura`: escolha `papel_e_nome_parecido`; resultado cura_aplicada; evidência: evento 2389 (candidato_de_seletor), evento 2388 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome_parecido, texto_contido, data_id, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 2407, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 2389 (candidato_de_seletor), evento 2404 (sinal_em_codigo), evento 2405 (sinal_em_codigo), evento 2406 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome_parecido

Sem gabarito nem modelo: a cura de seletor é toda em código; a regra R3 separa o mesmo elemento da referência de outro que fez o roteiro passar.

## Rastro

Gerado dos eventos 2374 a 2407 da trilha; hash dos eventos deste caso: `cd4a726d2654f559`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
