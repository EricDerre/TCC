<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_cura/front-cliente-reserva/id_renomeado/harness/r5`: o que o agente fez, declarou e conferiu

Trilha `fase4_cura/front-cliente-reserva/id_renomeado/harness/r5`; modelo `(sem modelo: cura de seletor)`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**Cura de seletor:** aplicada: `papel_e_nome` (`role=button[name="Reservar"]`) · reexecução validada · mesmo elemento da referência: sim

Passo 11 do roteiro, localizador `#enviar`: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("#enviar")

Da detecção à reexecução validada: 0,7 s (detecção 2026-11-01T20:11:08; validação 2026-11-01T20:11:09).

Justificativa (gerada por molde): O passo 11 (#enviar) falhou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("#enviar"). Dos 6 candidatos previstos, 4 foram gerados da árvore podada e do alvo da referência; 4 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome` (role=button[name="Reservar"]), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 0,7 s.

## 2. Evidência

Alvo registrado na corrida de referência: button "Reservar" (ocorrência 1; tag `input`; caminho `#reserva_login > input:nth-of-type(1)`; atributos {"id": "enviar", "class": "btn btn-danger btn-block", "name": "enviar", "type": "submit", "value": "Reservar"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=button[name="Reservar"]` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.637 s) | **sim** |
| `papel_e_nome_parecido` | não gerado: nenhum button da árvore podada tem nome parecido com "Reservar" acima do limiar 0.6 (o mais próximo, " CANCELAR", fica em 0.33) | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | `text=Reservar` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `#reserva_login > input:nth-of-type(1)` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `#reserva_login >> role=button >> nth=0` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 3034): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 36}, depois {"linhas": 14}.

Trecho podado (hash `b6fe8b199e6086bc`):

```text
document "Área do cliente - Cliente Teste"
  main
    heading " Olá, Cliente Teste!" level=2
    text "Faça uma nova reserva"
    heading "Suas Reservas" level=2
    button " CANCELAR"
    heading "Faça sua Reserva" level=1
    text "Número de Pessoas:"
    spinbutton "4"
    text "Data da Reserva:"
    textbox "Data da Reserva:" id="data_pedido" name="data_pedido" class="form-control"
    text "id do cliente:"
    textbox "id do cliente:" id="id_clientes" name="id_clientes" class="form-control"
    button "Reservar" id="enviar_reserva" name="enviar" class="btn btn-danger btn-block"

```

## 3. Contraste com a segunda causa

`papel_e_nome` (role=button[name="Reservar"]) e não `texto_contido` (text=Reservar): o segundo também passou as verificações estáticas, mas vem depois na ordem fixa e o primeiro já tinha levado o roteiro ao fim.

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| papel_e_nome | 5 de 5 verificações | sim |
| texto_contido | 4 de 5 verificações |  |
| caminho_do_ancestral_com_id | 4 de 5 verificações |  |
| posicao_entre_irmaos | 4 de 5 verificações |  |

## 4. FONTE declarada e conferida

Não se aplica: a cura de seletor roda sem modelo; nenhum verbete foi citado.

## 5. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 11 do roteiro, trocar o localizador `#enviar` por `role=button[name="Reservar"]` (estratégia `papel_e_nome`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cura --saida fase4_cura_reexec --roteiros front-cliente-reserva --modos id_renomeado --formas harness --repeticoes 1`

## 6. Árvore completa

<details><summary>33 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3022 | 1 | entrada | programa | ao_vivo | 2026-11-01T20:11:03 | caso None |
| 3023 | 2 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 75.1, "falhou": false, "reexecucao": 0} |
| 3024 | 3 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 21.9, "falhou": false, "reexecucao": 0} |
| 3025 | 4 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 14.7, "falhou": false, "reexecucao": 0} |
| 3026 | 5 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 6.1, "falhou": false, "reexecucao": 0} |
| 3027 | 6 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 5, "acao": "clicar", "seletor": "button[type=submit]", "url": null, "tempo_ms": 80.2, "falhou": false, "reexecucao": 0} |
| 3028 | 7 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 6, "acao": "esperar", "seletor": "span.btn-info", "url": null, "tempo_ms": 130.3, "falhou": false, "reexecucao": 0} |
| 3029 | 8 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 7, "acao": "clicar", "seletor": "span.btn-info", "url": null, "tempo_ms": 35.6, "falhou": false, "reexecucao": 0} |
| 3030 | 9 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 8, "acao": "esperar", "seletor": "#reserva_login", "url": null, "tempo_ms": 3.0, "falhou": false, "reexecucao": 0} |
| 3031 | 10 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 9, "acao": "preencher", "seletor": "#pessoas", "url": null, "tempo_ms": 4.5, "falhou": false, "reexecucao": 0} |
| 3032 | 11 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 10, "acao": "preencher", "seletor": "#data_pedido", "url": null, "tempo_ms": 4.4, "falhou": false, "reexecucao": 0} |
| 3033 | 12 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 11, "acao": "clicar", "seletor": "#enviar", "url": null, "tempo_ms": 5012.8, "falhou": true, "reexecucao": 0} |
| 3034 | 13 | poda | programa | ao_vivo | 2026-11-01T20:11:09 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 3035 | 14 | cura | programa | ao_vivo | 2026-11-01T20:11:09 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 0,7 s |
| 3036 | 15 | decisao | programa | ao_vivo | 2026-11-01T20:11:09 | cura: escolha papel_e_nome; divergência sim |
| 3037 | 16 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 92.7, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 3038 | 17 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 21.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 3039 | 18 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 14.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cu |
| 3040 | 19 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 5.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cur |
| 3041 | 20 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 5, "acao": "clicar", "seletor": "button[type=submit]", "url": null, "tempo_ms": 70.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", " |
| 3042 | 21 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 6, "acao": "esperar", "seletor": "span.btn-info", "url": null, "tempo_ms": 138.3, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 3043 | 22 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 7, "acao": "clicar", "seletor": "span.btn-info", "url": null, "tempo_ms": 35.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado |
| 3044 | 23 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 8, "acao": "esperar", "seletor": "#reserva_login", "url": null, "tempo_ms": 3.2, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 3045 | 24 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 9, "acao": "preencher", "seletor": "#pessoas", "url": null, "tempo_ms": 4.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado":  |
| 3046 | 25 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 10, "acao": "preencher", "seletor": "#data_pedido", "url": null, "tempo_ms": 6.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 3047 | 26 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 11, "acao": "clicar", "seletor": "role=button[name=\"Reservar\"]", "url": null, "tempo_ms": 94.0, "falhou": false, "reexecucao": 1, "candidato": "pape |
| 3048 | 27 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 12, "acao": "abrir", "seletor": null, "url": "cliente/index.php?cliente=11122233344", "tempo_ms": 111.6, "falhou": false, "reexecucao": 1, "candidato" |
| 3049 | 28 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 13, "acao": "esperar", "seletor": "table.table tbody tr", "url": null, "tempo_ms": 17.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome" |
| 3050 | 29 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 14, "acao": "conferir", "seletor": "button.cancela[data-id]:not([data-id=''])", "url": null, "tempo_ms": 9.5, "falhou": false, "reexecucao": 1, "candi |
| 3051 | 30 | acao | programa | ao_vivo | 2026-11-01T20:11:09 | {"passo": 15, "acao": "conferir", "seletor": "table.table tbody", "url": null, "tempo_ms": 3.2, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", " |
| 3052 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T20:11:09 | conferencia_do_roteiro: confere |
| 3053 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T20:11:09 | conferencia_do_roteiro: confere |
| 3054 | 33 | decisao | programa | ao_vivo | 2026-11-01T20:11:09 | reexecucao: escolha validada; divergência não |

</details>

Nós de decisão:

- evento 3036, `cura`: escolha `papel_e_nome`; resultado cura_aplicada; evidência: evento 3035 (candidato_de_seletor), evento 3034 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome, texto_contido, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 3054, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 3035 (candidato_de_seletor), evento 3052 (sinal_em_codigo), evento 3053 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome

Sem gabarito nem modelo: a cura de seletor é toda em código; a regra R3 separa o mesmo elemento da referência de outro que fez o roteiro passar.

## Rastro

Gerado dos eventos 3022 a 3054 da trilha; hash dos eventos deste caso: `b7e216a4c60ed654`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
