<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Localizador (seletor) quebrado no passo 11 do roteiro `front-admin-produtos` (localizador `role=button[name=/EXCLUIR$/] >> nth=0`), curado pelo agente

Caso `localizador-front-admin-produtos#1` da corrida `fase4_ensaio_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ensaio_v4/qwen2.5_7b/localizador-front-admin-produtos#1`: o caso `localizador-front-admin-produtos#1` na corrida `fase4_ensaio_v4` (execução 1 do cenário `localizador-front-admin-produtos`); eventos 313 a 368 da trilha `trilha_cenarios.jsonl`, hash dos eventos `f0548bfd6fb24b0e` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Localizador (seletor) quebrado no passo 11 do roteiro `front-admin-produtos` (localizador `role=button[name=/EXCLUIR$/] >> nth=0`), curado pelo agente

## 3. Data, organização e autor

Observado em 06/11/2026 11:24:16 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 11:13:26 a 06/11/2026 11:26:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `cenarios`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

O roteiro `front-admin-produtos` do site PHP (CobaiaFront), a partir da página `admin/login.php`; o alvo do passo que falhou é button " EXCLUIR" (localizador `role=button[name=/EXCLUIR$/] >> nth=0`).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `front-admin-produtos` do site PHP (cenário `localizador-front-admin-produtos` do ensaio da Fase 5, execução 1); quebra de localizador `texto_alterado` (o texto do alvo (ou o seu valor ou placeholder) ganha uma palavra), forma `harness` (add_init_script no DOMContentLoaded). O passo 11 (clicar em `role=button[name=/EXCLUIR$/] >> nth=0`) falhou.

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `admin/login.php` (0,1 s).
2. Esperar aparecer `#login_usuario` (0,0 s).
3. Preencher `#login_usuario` (0,0 s).
4. Preencher `#senha_usuario` (0,0 s).
5. Clicar em `button[type=submit]` (0,1 s).
6. Esperar aparecer `h1.breadcrumb` (0,1 s).
7. Abrir `admin/produtos_lista.php` (0,1 s).
8. Esperar aparecer `table.table tbody tr` (0,0 s).
9. Conferir `table.table tbody tr` (0,0 s).
10. Conferir `h2.breadcrumb` (0,0 s).
11. Clicar em `role=button[name=/EXCLUIR$/] >> nth=0` (5,0 s): falhou aqui.

O passo 11 (localizador `role=button[name=/EXCLUIR$/] >> nth=0`) falhou com a mensagem abaixo (do navegador, como veio):

> TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("role=button[name=/EXCLUIR$/]").first

Como provocar a mesma quebra (forma `harness`, armada por add_init_script no DOMContentLoaded):

> os botões passam de "EXCLUIR" a "EXCLUIR ITEM"; o roteiro localiza pelo papel e pelo nome terminado em "EXCLUIR", primeira ocorrência

- Mutação `trocar_texto` no seletor `button.delete`, novo valor `EXCLUIR ITEM`.

As 2 conferências do roteiro conferem (a tabela do bloco 7 traz cada uma).

Sintoma, como o código o descreveu para o agente:

> A conferência 'passo 11 (clicar em role=button[name=/EXCLUIR$/] >> nth=0)' falhou: esperava clicar em role=button[name=/EXCLUIR$/] >> nth=0; viu TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("role=button[name=/EXCLUIR$/]").first.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 7. Resultado esperado e resultado real

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| conferência do roteiro `14 produtos na tabela` | 14 elementos | 14 elementos |
| conferência do roteiro `título da lista` | texto no padrão Lista de Produtos | Lista de Produtos |
| passo 11, localizador `role=button[name=/EXCLUIR$/] >> nth=0` | um elemento button " EXCLUIR" visível, como na referência | nenhum elemento em 5,0 s: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("role=button[name=/EXCLUIR$/]").first |

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: o caso não tem classe nem nível declarados; o roteiro parou no passo 11.

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: o caso não tem classe nem nível declarados. Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).
- Verbetes entregues pela busca e não citados: `valor_fora_do_dominio` (Valor fora do domínio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/valor_fora_do_dominio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/valor_fora_do_dominio.md`); `tempo_de_resposta_excedido` (Tempo de resposta excedido; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tempo_de_resposta_excedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tempo_de_resposta_excedido.md`).
- Caso escrito: `localizador-front-admin-produtos#1` em `cenarios_fase4.py` (catálogo dos dez cenários do ensaio da Fase 5, ficha 36).
- Trilha: `fase4_ensaio_v4/qwen2.5_7b/localizador-front-admin-produtos#1` em `trilha_cenarios.jsonl`, eventos 313 a 368, hash dos eventos `f0548bfd6fb24b0e`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/localizador-front-admin-produtos__r1.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `localizador_quebrado` (Localizador (seletor) quebrado). Campo: nenhum apontado. Confiança: o agente está seguro desta causa (probabilidade 0,99 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário não consegue clicar no botão de exclusão, resultando em uma interação ineficaz com a interface.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, valor_fora_do_dominio, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

Cura do localizador: aplicada `role=button[name=" EXCLUIR ITEM"] >> nth=0` (estratégia `papel_e_nome_parecido`: o elemento é achado pelo papel igual e pelo nome parecido com o do alvo); reexecução validada; é o mesmo elemento da referência.

Da detecção à reexecução validada: 66,4 s (detecção 06/11/2026 11:24:21; validação 06/11/2026 11:25:28).

Justificativa da cura (gerada por molde, copiada da trilha):

> O passo 11 (role=button[name=/EXCLUIR$/] >> nth=0) falhou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("role=button[name=/EXCLUIR$/]").first. Dos 6 candidatos previstos, 5 foram gerados da árvore podada e do alvo da referência; 4 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome_parecido` (role=button[name=" EXCLUIR ITEM"] >> nth=0), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 66,4 s.

## 13. Evidência

Alvo registrado na corrida de referência: button " EXCLUIR" (ocorrência 1; tag `button`; caminho `body > main:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(7) > button:nth-of-type(1)`).

Candidatos de localizador, na ordem fixa em que o código os tenta (limiar do nome parecido 0.6), e o resultado de cada verificação:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | não gerado: a árvore podada não tem button " EXCLUIR" | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | confere | confere | confere | confere (" EXCLUIR ITEM" contra " EXCLUIR": similaridade 0.78 (limiar 0.6)) | confere (o roteiro chegou ao fim: 3 conferência(s) passaram em 0.668 s) | sim |
| `texto_contido` | `text=EXCLUIR >> nth=0` | confere | confere | não confere | confere ("EXCLUIR ITEM" contra " EXCLUIR": similaridade 0.67 (limiar 0.6)) | não tentado |  |
| `data_id` | `button[data-id="1"]` | confere | confere | confere | confere (" EXCLUIR ITEM" contra " EXCLUIR": similaridade 0.78 (limiar 0.6)) | não tentado |  |
| `caminho_do_ancestral_com_id` | `body > main:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(7) > button:nth-of-type(1)` | confere | confere | confere | confere (" EXCLUIR ITEM" contra " EXCLUIR": similaridade 0.78 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `body > main:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(7) >> role=button >> nth=1` | confere | confere | confere | confere (" EXCLUIR ITEM" contra " EXCLUIR": similaridade 0.78 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 328), feita em código antes de montar o prompt: 170 nós antes, 38 linhas depois. Regras aplicadas: `cartoes_omitidos` 0, `decoracao_removida` 0, `headings_removidos` 0, `imagens_removidas` 14, `interativos_sem_nome_removidos` 3, `listas_achatadas` 116, `textos_sem_letra_removidos` 0.

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

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> localizador_quebrado e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: localizador_quebrado, valor_fora_do_dominio, tempo_de_resposta_excedido

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `localizador_quebrado` (Localizador (seletor) quebrado) | 0,99 | sim |
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 0,00 |  |
| `nulo_inesperado` (Nulo inesperado) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `valor_fora_do_dominio`, `tempo_de_resposta_excedido` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| A linha FONTE só tem identificadores, no formato pedido | `[localizador_quebrado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["localizador_quebrado"]} |
| O verbete citado fala da causa respondida | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 11 do roteiro, trocar o localizador `role=button[name=/EXCLUIR$/] >> nth=0` por `role=button[name=" EXCLUIR ITEM"] >> nth=0` (estratégia `papel_e_nome_parecido`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 17. Árvore completa

<details><summary>53 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 313 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:24:16 | roteiro front-admin-produtos, passo 10, localizador role=button[name=/EXCLUIR$/] >> nth=0 |
| 314 | 2 | acao | programa | ao_vivo | 2026-11-06T11:24:21 | passo 1: abrir admin/login.php |
| 315 | 3 | acao | programa | ao_vivo | 2026-11-06T11:24:21 | passo 2: esperar aparecer #login_usuario |
| 316 | 4 | acao | programa | ao_vivo | 2026-11-06T11:24:21 | passo 3: preencher #login_usuario |
| 317 | 5 | acao | programa | ao_vivo | 2026-11-06T11:24:21 | passo 4: preencher #senha_usuario |
| 318 | 6 | acao | programa | ao_vivo | 2026-11-06T11:24:21 | passo 5: clicar em button[type=submit] |
| 319 | 7 | acao | programa | ao_vivo | 2026-11-06T11:24:21 | passo 6: esperar aparecer h1.breadcrumb |
| 320 | 8 | acao | programa | ao_vivo | 2026-11-06T11:24:21 | passo 7: abrir admin/produtos_lista.php |
| 321 | 9 | acao | programa | ao_vivo | 2026-11-06T11:24:21 | passo 8: esperar aparecer table.table tbody tr |
| 322 | 10 | acao | programa | ao_vivo | 2026-11-06T11:24:21 | passo 9: conferir table.table tbody tr |
| 323 | 11 | acao | programa | ao_vivo | 2026-11-06T11:24:21 | passo 10: conferir h2.breadcrumb |
| 324 | 12 | acao | programa | ao_vivo | 2026-11-06T11:24:21 | passo 11: clicar em role=button[name=/EXCLUIR$/] >> nth=0 (falhou) |
| 325 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:21 | conferencia_do_roteiro: confere |
| 326 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:21 | conferencia_do_roteiro: confere |
| 328 | 15 | poda | programa | ao_vivo | 2026-11-06T11:24:21 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 329 | 16 | candidatos | programa | ao_vivo | 2026-11-06T11:24:21 | 3 de 39 verbetes entregues |
| 331 | 17 | prompt | programa | ao_vivo | 2026-11-06T11:24:21 | diagnostico: 3766 caracteres; verbetes localizador_quebrado, valor_fora_do_dominio, tempo_de_resposta_excedido |
| 333 | 18 | inferencia | programa | ao_vivo | 2026-11-06T11:24:21 | diagnostico: 63,1 s |
| 334 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:24:21 | causa_raiz: `localizador_quebrado` |
| 335 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:24:21 | campo: `nenhum` |
| 336 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:24:21 | impacto: `O usuário não consegue clicar no botão de exclusão, resultando em uma interação ineficaz com a interface.` |
| 337 | 22 | declaracao | modelo | ao_vivo | 2026-11-06T11:24:21 | fonte: `[localizador_quebrado]` |
| 338 | 23 | declaracao | modelo | ao_vivo | 2026-11-06T11:24:21 | fonte_citada: `localizador_quebrado` |
| 339 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:21 | quatro_linhas_presentes: confere |
| 340 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:21 | rotulo_no_conjunto: confere |
| 341 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:21 | fonte_existe_na_biblioteca: confere |
| 342 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:21 | fonte_estava_no_contexto: confere |
| 343 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:21 | campo_existe_no_caso: nao_se_aplica |
| 344 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:21 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 345 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:21 | notas_nos_verbetes_citados: informativo |
| 346 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:21 | impacto: nao_verificavel |
| 347 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:21 | fonte_formato_valido: confere |
| 348 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:21 | fonte_contem_termo_da_causa: confere |
| 349 | 34 | decisao | programa | ao_vivo | 2026-11-06T11:24:21 | diagnostico: escolha localizador_quebrado; divergência entre o declarado e o medido: não |
| 350 | 35 | cura | programa | ao_vivo | 2026-11-06T11:25:28 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome_parecido; MTTR 66,4 s |
| 351 | 36 | decisao | programa | ao_vivo | 2026-11-06T11:25:28 | cura: escolha papel_e_nome_parecido; divergência entre o declarado e o medido: sim |
| 352 | 37 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 1: abrir admin/login.php; reexecução 1 |
| 353 | 38 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 2: esperar aparecer #login_usuario; reexecução 1 |
| 354 | 39 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 3: preencher #login_usuario; reexecução 1 |
| 355 | 40 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 4: preencher #senha_usuario; reexecução 1 |
| 356 | 41 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 5: clicar em button[type=submit]; reexecução 1 |
| 357 | 42 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 6: esperar aparecer h1.breadcrumb; reexecução 1 |
| 358 | 43 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 7: abrir admin/produtos_lista.php; reexecução 1 |
| 359 | 44 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 8: esperar aparecer table.table tbody tr; reexecução 1 |
| 360 | 45 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 9: conferir table.table tbody tr; reexecução 1 |
| 361 | 46 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 10: conferir h2.breadcrumb; reexecução 1 |
| 362 | 47 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 11: clicar em role=button[name=" EXCLUIR ITEM"] >> nth=0; reexecução 1 |
| 363 | 48 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 12: esperar aparecer #modalEdit; reexecução 1 |
| 364 | 49 | acao | programa | ao_vivo | 2026-11-06T11:25:28 | passo 13: conferir #modalEdit span.nome; reexecução 1 |
| 365 | 50 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:28 | conferencia_do_roteiro: confere |
| 366 | 51 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:28 | conferencia_do_roteiro: confere |
| 367 | 52 | verificacao | verificacao | ao_vivo | 2026-11-06T11:25:28 | conferencia_do_roteiro: confere |
| 368 | 53 | decisao | programa | ao_vivo | 2026-11-06T11:25:28 | reexecucao: escolha validada; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 349, decisão `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido.
  - Evidência: evento 328 (arvore_podada); evento 329 (verbete_entregue: `localizador_quebrado`, `valor_fora_do_dominio`, `tempo_de_resposta_excedido`); evento 333 (resposta); evento 338 (verbete_citado: `localizador_quebrado`).
  - Usou: `localizador_quebrado`, `valor_fora_do_dominio`, `tempo_de_resposta_excedido`.
- evento 351, decisão `cura`: escolha `papel_e_nome_parecido`; resultado cura_aplicada.
  - Evidência: evento 350 (candidato_de_seletor); evento 328 (arvore_podada).
  - Usou: `papel_e_nome_parecido`, `texto_contido`, `data_id`, `caminho_do_ancestral_com_id`, `posicao_entre_irmaos`.
  - Divergência entre o declarado e o medido: sim; falha: nenhuma.
- evento 368, decisão `reexecucao`: escolha `validada`; resultado roteiro_concluido.
  - Evidência: evento 350 (candidato_de_seletor); evento 365 (sinal_em_codigo); evento 366 (sinal_em_codigo); evento 367 (sinal_em_codigo).
  - Usou: `papel_e_nome_parecido`.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 313 a 368 da trilha; hash dos eventos deste caso: `f0548bfd6fb24b0e`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
