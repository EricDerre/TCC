<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Localizador (seletor) quebrado no passo 11 do roteiro `front-cliente-reserva` (localizador `#reserva_login > input[type=submit]`), curado pelo agente

Caso `localizador-front-cliente-reserva#1` da corrida `fase4_ensaio_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ensaio_v4/qwen2.5_7b/localizador-front-cliente-reserva#1`: o caso `localizador-front-cliente-reserva#1` na corrida `fase4_ensaio_v4` (execução 1 do cenário `localizador-front-cliente-reserva`); eventos 372 a 426 da trilha `trilha_cenarios.jsonl`, hash dos eventos `488b6fcc4671f9b1` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Localizador (seletor) quebrado no passo 11 do roteiro `front-cliente-reserva` (localizador `#reserva_login > input[type=submit]`), curado pelo agente

## 3. Data, organização e autor

Observado em 06/11/2026 11:25:32 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 11:13:26 a 06/11/2026 11:26:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `cenarios`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

O roteiro `front-cliente-reserva` do site PHP (CobaiaFront), a partir da página `admin/login.php`; o alvo do passo que falhou é button "Reservar" (localizador `#reserva_login > input[type=submit]`).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `front-cliente-reserva` do site PHP (cenário `localizador-front-cliente-reserva` do ensaio da Fase 5, execução 1); quebra de localizador `estrutura_alterada` (o alvo é envolvido num contêiner novo e trocado de posição entre os irmãos), forma `harness` (add_init_script no DOMContentLoaded). O passo 11 (clicar em `#reserva_login > input[type=submit]`) falhou.

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `admin/login.php` (0,1 s).
2. Esperar aparecer `#login_usuario` (0,0 s).
3. Preencher `#login_usuario` (0,0 s).
4. Preencher `#senha_usuario` (0,0 s).
5. Clicar em `button[type=submit]` (0,1 s).
6. Esperar aparecer `span.btn-info` (0,2 s).
7. Clicar em `span.btn-info` (0,0 s).
8. Esperar aparecer `#reserva_login` (0,0 s).
9. Preencher `#pessoas` (0,0 s).
10. Preencher `#data_pedido` (0,0 s).
11. Clicar em `#reserva_login > input[type=submit]` (5,0 s): falhou aqui.

O passo 11 (localizador `#reserva_login > input[type=submit]`) falhou com a mensagem abaixo (do navegador, como veio):

> TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("#reserva_login > input[type=submit]")

Como provocar a mesma quebra (forma `harness`, armada por add_init_script no DOMContentLoaded):

> o botão é envolvido num `div.acoes` e passa para o começo do formulário; o roteiro localiza por `#reserva_login > input[type=submit]`

- Mutação `envolver_e_mover` no seletor `#enviar`.

Sintoma, como o código o descreveu para o agente:

> A conferência 'passo 11 (clicar em #reserva_login > input[type=submit])' falhou: esperava clicar em #reserva_login > input[type=submit]; viu TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("#reserva_login > input[type=submit]").

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 7. Resultado esperado e resultado real

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| passo 11, localizador `#reserva_login > input[type=submit]` | um elemento button "Reservar" visível, como na referência | nenhum elemento em 5,0 s: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("#reserva_login > input[type=submit]") |

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: o caso não tem classe nem nível declarados; o roteiro parou no passo 11.

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: o caso não tem classe nem nível declarados. Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).
- Verbetes entregues pela busca e não citados: `corpo_nao_e_json` (Corpo não é JSON; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/corpo_nao_e_json.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/corpo_nao_e_json.md`); `resposta_truncada` (Resposta truncada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/resposta_truncada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/resposta_truncada.md`).
- Caso escrito: `localizador-front-cliente-reserva#1` em `cenarios_fase4.py` (catálogo dos dez cenários do ensaio da Fase 5, ficha 36).
- Trilha: `fase4_ensaio_v4/qwen2.5_7b/localizador-front-cliente-reserva#1` em `trilha_cenarios.jsonl`, eventos 372 a 426, hash dos eventos `488b6fcc4671f9b1`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/localizador-front-cliente-reserva__r1.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `localizador_quebrado` (Localizador (seletor) quebrado). Campo: nenhum apontado. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário não consegue clicar no botão de login de reserva devido ao seletor quebrado, resultando em um TimeoutError.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, corpo_nao_e_json, resposta_truncada estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

Cura do localizador: aplicada `role=button[name="Reservar"]` (estratégia `papel_e_nome`: o elemento é achado pelo papel e pelo nome acessíveis, iguais aos do alvo); reexecução validada; é o mesmo elemento da referência.

Da detecção à reexecução validada: 68,8 s (detecção 06/11/2026 11:25:37; validação 06/11/2026 11:26:46).

Justificativa da cura (gerada por molde, copiada da trilha):

> O passo 11 (#reserva_login > input[type=submit]) falhou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("#reserva_login > input[type=submit]"). Dos 6 candidatos previstos, 4 foram gerados da árvore podada e do alvo da referência; 3 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome` (role=button[name="Reservar"]), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 68,8 s.

## 13. Evidência

Alvo registrado na corrida de referência: button "Reservar" (ocorrência 1; tag `input`; caminho `#reserva_login > input:nth-of-type(1)`).

Candidatos de localizador, na ordem fixa em que o código os tenta (limiar do nome parecido 0.6), e o resultado de cada verificação:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=button[name="Reservar"]` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.638 s) | sim |
| `papel_e_nome_parecido` | não gerado: nenhum button da árvore podada tem nome parecido com "Reservar" acima do limiar 0.6 (o mais próximo, " CANCELAR", fica em 0.33) | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | `text=Reservar` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `#reserva_login > input:nth-of-type(1)` | não confere | não se aplica | não se aplica | não se aplica | não tentado |  |
| `posicao_entre_irmaos` | `#reserva_login >> role=button >> nth=0` | confere | confere | confere | confere ("Reservar" contra "Reservar": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 385), feita em código antes de montar o prompt: 36 nós antes, 14 linhas depois. Regras aplicadas: `cartoes_omitidos` 0, `decoracao_removida` 1, `headings_removidos` 0, `imagens_removidas` 0, `interativos_sem_nome_removidos` 0, `listas_achatadas` 13, `textos_sem_letra_removidos` 0.

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

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> localizador_quebrado e não tempo_de_resposta_excedido: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: localizador_quebrado, corpo_nao_e_json, resposta_truncada

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `localizador_quebrado` (Localizador (seletor) quebrado) | 1,00 | sim |
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 0,00 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |
| `nulo_inesperado` (Nulo inesperado) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `corpo_nao_e_json`, `resposta_truncada` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| A linha FONTE só tem identificadores, no formato pedido | `[localizador_quebrado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["localizador_quebrado"]} |
| O verbete citado fala da causa respondida | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 11 do roteiro, trocar o localizador `#reserva_login > input[type=submit]` por `role=button[name="Reservar"]` (estratégia `papel_e_nome`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 17. Árvore completa

<details><summary>52 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 372 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:25:32 | roteiro front-cliente-reserva, passo 10, localizador #reserva_login > input[type=submit] |
| 373 | 2 | acao | programa | ao_vivo | 2026-11-06T11:25:37 | passo 1: abrir admin/login.php |
| 374 | 3 | acao | programa | ao_vivo | 2026-11-06T11:25:37 | passo 2: esperar aparecer #login_usuario |
| 375 | 4 | acao | programa | ao_vivo | 2026-11-06T11:25:37 | passo 3: preencher #login_usuario |
| 376 | 5 | acao | programa | ao_vivo | 2026-11-06T11:25:37 | passo 4: preencher #senha_usuario |
| 377 | 6 | acao | programa | ao_vivo | 2026-11-06T11:25:37 | passo 5: clicar em button[type=submit] |
| 378 | 7 | acao | programa | ao_vivo | 2026-11-06T11:25:37 | passo 6: esperar aparecer span.btn-info |
| 379 | 8 | acao | programa | ao_vivo | 2026-11-06T11:25:37 | passo 7: clicar em span.btn-info |
| 380 | 9 | acao | programa | ao_vivo | 2026-11-06T11:25:37 | passo 8: esperar aparecer #reserva_login |
| 381 | 10 | acao | programa | ao_vivo | 2026-11-06T11:25:37 | passo 9: preencher #pessoas |
| 382 | 11 | acao | programa | ao_vivo | 2026-11-06T11:25:37 | passo 10: preencher #data_pedido |
| 383 | 12 | acao | programa | ao_vivo | 2026-11-06T11:25:37 | passo 11: clicar em #reserva_login > input[type=submit] (falhou) |
| 385 | 13 | poda | programa | ao_vivo | 2026-11-06T11:25:37 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 386 | 14 | candidatos | programa | ao_vivo | 2026-11-06T11:25:37 | 3 de 39 verbetes entregues |
| 388 | 15 | prompt | programa | ao_vivo | 2026-11-06T11:25:37 | diagnostico: 4116 caracteres; verbetes localizador_quebrado, corpo_nao_e_json, resposta_truncada |
| 390 | 16 | inferencia | programa | ao_vivo | 2026-11-06T11:25:37 | diagnostico: 65,5 s |
| 391 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:25:37 | causa_raiz: `localizador_quebrado` |
| 392 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:25:37 | campo: `nenhum` |
| 393 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:25:37 | impacto: `O usuário não consegue clicar no botão de login de reserva devido ao seletor quebrado, resultando em um TimeoutError.` |
| 394 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:25:37 | fonte: `[localizador_quebrado]` |
| 395 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:25:37 | fonte_citada: `localizador_quebrado` |
| 396 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:37 | quatro_linhas_presentes: confere |
| 397 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:37 | rotulo_no_conjunto: confere |
| 398 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:37 | fonte_existe_na_biblioteca: confere |
| 399 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:37 | fonte_estava_no_contexto: confere |
| 400 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:37 | campo_existe_no_caso: nao_se_aplica |
| 401 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:37 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 402 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:37 | notas_nos_verbetes_citados: informativo |
| 403 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:37 | impacto: nao_verificavel |
| 404 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:37 | fonte_formato_valido: confere |
| 405 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:37 | fonte_contem_termo_da_causa: confere |
| 406 | 32 | decisao | programa | ao_vivo | 2026-11-06T11:25:37 | diagnostico: escolha localizador_quebrado; divergência entre o declarado e o medido: não |
| 407 | 33 | cura | programa | ao_vivo | 2026-11-06T11:26:46 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 68,8 s |
| 408 | 34 | decisao | programa | ao_vivo | 2026-11-06T11:26:46 | cura: escolha papel_e_nome; divergência entre o declarado e o medido: sim |
| 409 | 35 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 1: abrir admin/login.php; reexecução 1 |
| 410 | 36 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 2: esperar aparecer #login_usuario; reexecução 1 |
| 411 | 37 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 3: preencher #login_usuario; reexecução 1 |
| 412 | 38 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 4: preencher #senha_usuario; reexecução 1 |
| 413 | 39 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 5: clicar em button[type=submit]; reexecução 1 |
| 414 | 40 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 6: esperar aparecer span.btn-info; reexecução 1 |
| 415 | 41 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 7: clicar em span.btn-info; reexecução 1 |
| 416 | 42 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 8: esperar aparecer #reserva_login; reexecução 1 |
| 417 | 43 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 9: preencher #pessoas; reexecução 1 |
| 418 | 44 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 10: preencher #data_pedido; reexecução 1 |
| 419 | 45 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 11: clicar em role=button[name="Reservar"]; reexecução 1 |
| 420 | 46 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 12: abrir cliente/index.php?cliente=11122233344; reexecução 1 |
| 421 | 47 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 13: esperar aparecer table.table tbody tr; reexecução 1 |
| 422 | 48 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 14: conferir button.cancela[data-id]:not([data-id='']); reexecução 1 |
| 423 | 49 | acao | programa | ao_vivo | 2026-11-06T11:26:46 | passo 15: conferir table.table tbody; reexecução 1 |
| 424 | 50 | verificacao | verificacao | ao_vivo | 2026-11-06T11:26:46 | conferencia_do_roteiro: confere |
| 425 | 51 | verificacao | verificacao | ao_vivo | 2026-11-06T11:26:46 | conferencia_do_roteiro: confere |
| 426 | 52 | decisao | programa | ao_vivo | 2026-11-06T11:26:46 | reexecucao: escolha validada; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 406, decisão `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido.
  - Evidência: evento 385 (arvore_podada); evento 386 (verbete_entregue: `localizador_quebrado`, `corpo_nao_e_json`, `resposta_truncada`); evento 390 (resposta); evento 395 (verbete_citado: `localizador_quebrado`).
  - Usou: `localizador_quebrado`, `corpo_nao_e_json`, `resposta_truncada`.
- evento 408, decisão `cura`: escolha `papel_e_nome`; resultado cura_aplicada.
  - Evidência: evento 407 (candidato_de_seletor); evento 385 (arvore_podada).
  - Usou: `papel_e_nome`, `texto_contido`, `caminho_do_ancestral_com_id`, `posicao_entre_irmaos`.
  - Divergência entre o declarado e o medido: sim; falha: nenhuma.
- evento 426, decisão `reexecucao`: escolha `validada`; resultado roteiro_concluido.
  - Evidência: evento 407 (candidato_de_seletor); evento 424 (sinal_em_codigo); evento 425 (sinal_em_codigo).
  - Usou: `papel_e_nome`.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 372 a 426 da trilha; hash dos eventos deste caso: `488b6fcc4671f9b1`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
