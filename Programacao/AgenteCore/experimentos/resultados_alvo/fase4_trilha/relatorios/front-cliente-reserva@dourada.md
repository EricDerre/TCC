<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_trilha/qwen2.5_7b/front-cliente-reserva@dourada`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/front-cliente-reserva@dourada`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário não consegue avançar no processo de reserva, ficando preso na tela de login.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, corpo_nao_e_json, resposta_truncada estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Alvo registrado na corrida de referência: button "Reservar" (ocorrência 1; tag `input`; caminho `#reserva_login > input:nth-of-type(1)`; atributos {"id": "enviar", "class": "btn btn-danger btn-block", "name": "enviar", "type": "submit", "value": "Reservar"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=button[name="Reservar"]` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.581 s) | **sim** |
| `papel_e_nome_parecido` | não gerado: nenhum button da árvore podada tem nome parecido com "Reservar" acima do limiar 0.6 (o mais próximo, " CANCELAR", fica em 0.33) | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | `text=Reservar` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `#reserva_login > input:nth-of-type(1)` | **não confere** | não se aplica | não se aplica | não se aplica | não tentado |  |
| `posicao_entre_irmaos` | `#reserva_login >> role=button >> nth=0` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 4093): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 36}, depois {"linhas": 14}.

Trecho podado (hash `d5eb01145ff43b5f`):

```text
document "Área do cliente - Cliente Teste"
  main
    heading " Olá, Cliente Teste!" level=2
    text "Faça uma nova reserva"
    heading "Suas Reservas" level=2
    button " CANCELAR"
    heading "Faça sua Reserva" level=1
    button "Reservar" id="enviar" name="enviar" class="btn btn-danger btn-block"
    text "Número de Pessoas:"
    spinbutton "4"
    text "Data da Reserva:"
    textbox "Data da Reserva:" id="data_pedido" name="data_pedido" class="form-control"
    text "id do cliente:"
    textbox "id do cliente:" id="id_clientes" name="id_clientes" class="form-control"

```

## 3. Contraste com a segunda causa

localizador_quebrado e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: localizador_quebrado, corpo_nao_e_json, resposta_truncada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 0,99 | sim |
| tempo_de_resposta_excedido | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `corpo_nao_e_json`, `resposta_truncada` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| fonte_formato_valido | `[localizador_quebrado]` | confere | {"ids": ["localizador_quebrado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 11 do roteiro, trocar o localizador `#reserva_login > input[type=submit]` por `role=button[name="Reservar"]` (estratégia `papel_e_nome`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --casos 0`

## 6. Árvore completa

<details><summary>52 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 4080 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:38:06 | caso None |
| 4081 | 2 | acao | programa | ao_vivo | 2026-11-05T02:38:11 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 87.9, "falhou": false, "reexecucao": 0} |
| 4082 | 3 | acao | programa | ao_vivo | 2026-11-05T02:38:11 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 25.2, "falhou": false, "reexecucao": 0} |
| 4083 | 4 | acao | programa | ao_vivo | 2026-11-05T02:38:11 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 16.2, "falhou": false, "reexecucao": 0} |
| 4084 | 5 | acao | programa | ao_vivo | 2026-11-05T02:38:11 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 7.1, "falhou": false, "reexecucao": 0} |
| 4085 | 6 | acao | programa | ao_vivo | 2026-11-05T02:38:11 | {"passo": 5, "acao": "clicar", "seletor": "button[type=submit]", "url": null, "tempo_ms": 73.7, "falhou": false, "reexecucao": 0} |
| 4086 | 7 | acao | programa | ao_vivo | 2026-11-05T02:38:11 | {"passo": 6, "acao": "esperar", "seletor": "span.btn-info", "url": null, "tempo_ms": 118.3, "falhou": false, "reexecucao": 0} |
| 4087 | 8 | acao | programa | ao_vivo | 2026-11-05T02:38:11 | {"passo": 7, "acao": "clicar", "seletor": "span.btn-info", "url": null, "tempo_ms": 52.3, "falhou": false, "reexecucao": 0} |
| 4088 | 9 | acao | programa | ao_vivo | 2026-11-05T02:38:11 | {"passo": 8, "acao": "esperar", "seletor": "#reserva_login", "url": null, "tempo_ms": 7.0, "falhou": false, "reexecucao": 0} |
| 4089 | 10 | acao | programa | ao_vivo | 2026-11-05T02:38:11 | {"passo": 9, "acao": "preencher", "seletor": "#pessoas", "url": null, "tempo_ms": 9.8, "falhou": false, "reexecucao": 0} |
| 4090 | 11 | acao | programa | ao_vivo | 2026-11-05T02:38:11 | {"passo": 10, "acao": "preencher", "seletor": "#data_pedido", "url": null, "tempo_ms": 7.2, "falhou": false, "reexecucao": 0} |
| 4091 | 12 | acao | programa | ao_vivo | 2026-11-05T02:38:11 | {"passo": 11, "acao": "clicar", "seletor": "#reserva_login > input[type=submit]", "url": null, "tempo_ms": 5012.6, "falhou": true, "reexecucao": 0} |
| 4093 | 13 | poda | programa | ao_vivo | 2026-11-05T02:38:11 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 4094 | 14 | candidatos | programa | ao_vivo | 2026-11-05T02:38:11 | 3 de 39 verbetes entregues |
| 4096 | 15 | prompt | programa | ao_vivo | 2026-11-05T02:38:11 | {"etapa": "diagnostico", "sha": "fc583f186fcb9232", "prompt_sha256": "fc583f186fcb", "chars": 4913, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 4098 | 16 | inferencia | programa | ao_vivo | 2026-11-05T02:38:11 | diagnostico: 75,4 s |
| 4099 | 17 | declaracao | modelo | ao_vivo | 2026-11-05T02:38:11 | causa_raiz: `localizador_quebrado` |
| 4100 | 18 | declaracao | modelo | ao_vivo | 2026-11-05T02:38:11 | campo: `nenhum` |
| 4101 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T02:38:11 | impacto: `O usuário não consegue avançar no processo de reserva, ficando preso na tela de login.` |
| 4102 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T02:38:11 | fonte: `[localizador_quebrado]` |
| 4103 | 21 | declaracao | modelo | ao_vivo | 2026-11-05T02:38:11 | fonte_citada: `localizador_quebrado` |
| 4104 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:38:11 | quatro_linhas_presentes: confere |
| 4105 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T02:38:11 | rotulo_no_conjunto: confere |
| 4106 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T02:38:11 | fonte_existe_na_biblioteca: confere |
| 4107 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T02:38:11 | fonte_estava_no_contexto: confere |
| 4108 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T02:38:11 | campo_existe_no_caso: nao_se_aplica |
| 4109 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T02:38:11 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 4110 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T02:38:11 | notas_nos_verbetes_citados: informativo |
| 4111 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T02:38:11 | impacto: nao_verificavel |
| 4112 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T02:38:11 | fonte_formato_valido: confere |
| 4113 | 31 | verificacao | verificacao | ao_vivo | 2026-11-05T02:38:11 | fonte_contem_termo_da_causa: confere |
| 4114 | 32 | decisao | programa | ao_vivo | 2026-11-05T02:38:11 | diagnostico: escolha localizador_quebrado; divergência não |
| 4115 | 33 | cura | programa | ao_vivo | 2026-11-05T02:39:30 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 78,6 s |
| 4116 | 34 | decisao | programa | ao_vivo | 2026-11-05T02:39:30 | cura: escolha papel_e_nome; divergência sim |
| 4117 | 35 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 71.7, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 4118 | 36 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 24.7, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 4119 | 37 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 16.2, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cu |
| 4120 | 38 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 7.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cur |
| 4121 | 39 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 5, "acao": "clicar", "seletor": "button[type=submit]", "url": null, "tempo_ms": 55.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", " |
| 4122 | 40 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 6, "acao": "esperar", "seletor": "span.btn-info", "url": null, "tempo_ms": 124.2, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 4123 | 41 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 7, "acao": "clicar", "seletor": "span.btn-info", "url": null, "tempo_ms": 33.3, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado |
| 4124 | 42 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 8, "acao": "esperar", "seletor": "#reserva_login", "url": null, "tempo_ms": 4.7, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 4125 | 43 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 9, "acao": "preencher", "seletor": "#pessoas", "url": null, "tempo_ms": 6.6, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado":  |
| 4126 | 44 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 10, "acao": "preencher", "seletor": "#data_pedido", "url": null, "tempo_ms": 6.7, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 4127 | 45 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 11, "acao": "clicar", "seletor": "role=button[name=\"Reservar\"]", "url": null, "tempo_ms": 96.3, "falhou": false, "reexecucao": 1, "candidato": "pape |
| 4128 | 46 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 12, "acao": "abrir", "seletor": null, "url": "cliente/index.php?cliente=11122233344", "tempo_ms": 82.3, "falhou": false, "reexecucao": 1, "candidato": |
| 4129 | 47 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 13, "acao": "esperar", "seletor": "table.table tbody tr", "url": null, "tempo_ms": 21.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome" |
| 4130 | 48 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 14, "acao": "conferir", "seletor": "button.cancela[data-id]:not([data-id=''])", "url": null, "tempo_ms": 11.1, "falhou": false, "reexecucao": 1, "cand |
| 4131 | 49 | acao | programa | ao_vivo | 2026-11-05T02:39:30 | {"passo": 15, "acao": "conferir", "seletor": "table.table tbody", "url": null, "tempo_ms": 4.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", " |
| 4132 | 50 | verificacao | verificacao | ao_vivo | 2026-11-05T02:39:30 | conferencia_do_roteiro: confere |
| 4133 | 51 | verificacao | verificacao | ao_vivo | 2026-11-05T02:39:30 | conferencia_do_roteiro: confere |
| 4134 | 52 | decisao | programa | ao_vivo | 2026-11-05T02:39:30 | reexecucao: escolha validada; divergência não |

</details>

Nós de decisão:

- evento 4114, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 4093 (arvore_podada), evento 4094 (verbete_entregue, localizador_quebrado), evento 4094 (verbete_entregue, corpo_nao_e_json), evento 4094 (verbete_entregue, resposta_truncada), evento 4098 (resposta), evento 4103 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, corpo_nao_e_json, resposta_truncada (gen_ai: chat)
- evento 4116, `cura`: escolha `papel_e_nome`; resultado cura_aplicada; evidência: evento 4115 (candidato_de_seletor), evento 4093 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome, texto_contido, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 4134, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 4115 (candidato_de_seletor), evento 4132 (sinal_em_codigo), evento 4133 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 4080 a 4134 da trilha; hash dos eventos deste caso: `9af2f2eb248527a7`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
