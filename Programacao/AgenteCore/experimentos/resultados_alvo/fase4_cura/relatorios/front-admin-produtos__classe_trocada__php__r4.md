<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_cura/front-admin-produtos/classe_trocada/php/r4`: o que o agente fez, declarou e conferiu

Trilha `fase4_cura/front-admin-produtos/classe_trocada/php/r4`; modelo `(sem modelo: cura de seletor)`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**Cura de seletor:** aplicada: `papel_e_nome` (`role=button[name=" EXCLUIR"] >> nth=0`) · reexecução validada · mesmo elemento da referência: sim

Passo 11 do roteiro, localizador `button.delete[data-id='1']`: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.delete[data-id='1']")

Da detecção à reexecução validada: 0,8 s (detecção 2026-11-01T20:08:18; validação 2026-11-01T20:08:19).

Justificativa (gerada por molde): O passo 11 (button.delete[data-id='1']) falhou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.delete[data-id='1']"). Dos 6 candidatos previstos, 5 foram gerados da árvore podada e do alvo da referência; 4 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome` (role=button[name=" EXCLUIR"] >> nth=0), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 0,8 s.

## 2. Evidência

Alvo registrado na corrida de referência: button " EXCLUIR" (ocorrência 1; tag `button`; caminho `body > main:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(7) > button:nth-of-type(1)`; atributos {"class": "delete btn btn-xs btn-block btn-danger", "data-id": "1", "data-nome": "Picanha ao Alho"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | confere | confere | confere | confere (" EXCLUIR" contra " EXCLUIR": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 3 conferência(s) passaram em 0.692 s) | **sim** |
| `papel_e_nome_parecido` | não gerado: nenhum button da árvore podada tem nome parecido com " EXCLUIR" acima do limiar 0.6 (o mais próximo, "ADICIONAR", fica em 0.33) | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | `text=EXCLUIR >> nth=0` | confere | confere | **não confere** | confere ("EXCLUIR" contra " EXCLUIR": similaridade 0.88 (limiar 0.6)) | não tentado |  |
| `data_id` | `button[data-id="1"]` | confere | confere | confere | confere (" EXCLUIR" contra " EXCLUIR": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `caminho_do_ancestral_com_id` | `body > main:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(7) > button:nth-of-type(1)` | confere | confere | confere | confere (" EXCLUIR" contra " EXCLUIR": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `body > main:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(7) >> role=button >> nth=1` | confere | confere | confere | confere (" EXCLUIR" contra " EXCLUIR": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 2147): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 170}, depois {"linhas": 38}.

Trecho podado (hash `47dd3fba16c41d04`):

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
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"
    button " ALTERAR"
    button " EXCLUIR"

```

## 3. Contraste com a segunda causa

`papel_e_nome` (role=button[name=" EXCLUIR"] >> nth=0) e não `data_id` (button[data-id="1"]): o segundo também passou as verificações estáticas, mas vem depois na ordem fixa e o primeiro já tinha levado o roteiro ao fim.

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| papel_e_nome | 5 de 5 verificações | sim |
| data_id | 4 de 5 verificações |  |
| caminho_do_ancestral_com_id | 4 de 5 verificações |  |
| posicao_entre_irmaos | 4 de 5 verificações |  |
| texto_contido | 3 de 5 verificações |  |

## 4. FONTE declarada e conferida

Não se aplica: a cura de seletor roda sem modelo; nenhum verbete foi citado.

## 5. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 11 do roteiro, trocar o localizador `button.delete[data-id='1']` por `role=button[name=" EXCLUIR"] >> nth=0` (estratégia `papel_e_nome`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cura --saida fase4_cura_reexec --roteiros front-admin-produtos --modos classe_trocada --formas php --repeticoes 1`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2133 | 1 | entrada | programa | ao_vivo | 2026-11-01T20:08:12 | caso None |
| 2134 | 2 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 85.3, "falhou": false, "reexecucao": 0} |
| 2135 | 3 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 20.4, "falhou": false, "reexecucao": 0} |
| 2136 | 4 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 12.6, "falhou": false, "reexecucao": 0} |
| 2137 | 5 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 6.6, "falhou": false, "reexecucao": 0} |
| 2138 | 6 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 5, "acao": "clicar", "seletor": "button[type=submit]", "url": null, "tempo_ms": 84.4, "falhou": false, "reexecucao": 0} |
| 2139 | 7 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 6, "acao": "esperar", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 69.0, "falhou": false, "reexecucao": 0} |
| 2140 | 8 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 7, "acao": "abrir", "seletor": null, "url": "admin/produtos_lista.php", "tempo_ms": 112.7, "falhou": false, "reexecucao": 0} |
| 2141 | 9 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 8, "acao": "esperar", "seletor": "table.table tbody tr", "url": null, "tempo_ms": 19.2, "falhou": false, "reexecucao": 0} |
| 2142 | 10 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 9, "acao": "conferir", "seletor": "table.table tbody tr", "url": null, "tempo_ms": 9.0, "falhou": false, "reexecucao": 0} |
| 2143 | 11 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 10, "acao": "conferir", "seletor": "h2.breadcrumb", "url": null, "tempo_ms": 4.1, "falhou": false, "reexecucao": 0} |
| 2144 | 12 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 11, "acao": "clicar", "seletor": "button.delete[data-id='1']", "url": null, "tempo_ms": 5007.0, "falhou": true, "reexecucao": 0} |
| 2145 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T20:08:19 | conferencia_do_roteiro: confere |
| 2146 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T20:08:19 | conferencia_do_roteiro: confere |
| 2147 | 15 | poda | programa | ao_vivo | 2026-11-01T20:08:19 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 2148 | 16 | cura | programa | ao_vivo | 2026-11-01T20:08:19 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 0,8 s |
| 2149 | 17 | decisao | programa | ao_vivo | 2026-11-01T20:08:19 | cura: escolha papel_e_nome; divergência sim |
| 2150 | 18 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 82.2, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 2151 | 19 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 20.9, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 2152 | 20 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 14.6, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cu |
| 2153 | 21 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 6.3, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cur |
| 2154 | 22 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 5, "acao": "clicar", "seletor": "button[type=submit]", "url": null, "tempo_ms": 79.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", " |
| 2155 | 23 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 6, "acao": "esperar", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 88.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 2156 | 24 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 7, "acao": "abrir", "seletor": null, "url": "admin/produtos_lista.php", "tempo_ms": 95.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome |
| 2157 | 25 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 8, "acao": "esperar", "seletor": "table.table tbody tr", "url": null, "tempo_ms": 23.9, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", |
| 2158 | 26 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 9, "acao": "conferir", "seletor": "table.table tbody tr", "url": null, "tempo_ms": 9.3, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", |
| 2159 | 27 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 10, "acao": "conferir", "seletor": "h2.breadcrumb", "url": null, "tempo_ms": 3.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 2160 | 28 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 11, "acao": "clicar", "seletor": "role=button[name=\" EXCLUIR\"] >> nth=0", "url": null, "tempo_ms": 43.4, "falhou": false, "reexecucao": 1, "candida |
| 2161 | 29 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 12, "acao": "esperar", "seletor": "#modalEdit", "url": null, "tempo_ms": 205.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado |
| 2162 | 30 | acao | programa | ao_vivo | 2026-11-01T20:08:19 | {"passo": 13, "acao": "conferir", "seletor": "#modalEdit span.nome", "url": null, "tempo_ms": 4.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome" |
| 2163 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T20:08:19 | conferencia_do_roteiro: confere |
| 2164 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T20:08:19 | conferencia_do_roteiro: confere |
| 2165 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T20:08:19 | conferencia_do_roteiro: confere |
| 2166 | 34 | decisao | programa | ao_vivo | 2026-11-01T20:08:19 | reexecucao: escolha validada; divergência não |

</details>

Nós de decisão:

- evento 2149, `cura`: escolha `papel_e_nome`; resultado cura_aplicada; evidência: evento 2148 (candidato_de_seletor), evento 2147 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome, texto_contido, data_id, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 2166, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 2148 (candidato_de_seletor), evento 2163 (sinal_em_codigo), evento 2164 (sinal_em_codigo), evento 2165 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome

Sem gabarito nem modelo: a cura de seletor é toda em código; a regra R3 separa o mesmo elemento da referência de outro que fez o roteiro passar.

## Rastro

Gerado dos eventos 2133 a 2166 da trilha; hash dos eventos deste caso: `ddca5aabb5537c89`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
