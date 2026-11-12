<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Localizador (seletor) quebrado no passo 5 do roteiro `front-admin-login` (localizador `button.btn-primary`), curado pelo agente

Caso `localizador-front-admin-login#1` da corrida `fase4_ensaio_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ensaio_v4/qwen2.5_7b/localizador-front-admin-login#1`: o caso `localizador-front-admin-login#1` na corrida `fase4_ensaio_v4` (execução 1 do cenário `localizador-front-admin-login`); eventos 268 a 309 da trilha `trilha_cenarios.jsonl`, hash dos eventos `2d9b755a7eeefe52` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Localizador (seletor) quebrado no passo 5 do roteiro `front-admin-login` (localizador `button.btn-primary`), curado pelo agente

## 3. Data, organização e autor

Observado em 06/11/2026 11:23:25 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 11:13:26 a 06/11/2026 11:26:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `cenarios`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

O roteiro `front-admin-login` do site PHP (CobaiaFront), a partir da página `admin/login.php`; o alvo do passo que falhou é button "Entrar" (localizador `button.btn-primary`).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `front-admin-login` do site PHP (cenário `localizador-front-admin-login` do ensaio da Fase 5, execução 1); quebra de localizador `classe_trocada` (a classe que o localizador usa é trocada por outra), forma `harness` (add_init_script no DOMContentLoaded). O passo 5 (clicar em `button.btn-primary`) falhou.

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `admin/login.php` (0,1 s).
2. Esperar aparecer `#login_usuario` (0,0 s).
3. Preencher `#login_usuario` (0,0 s).
4. Preencher `#senha_usuario` (0,0 s).
5. Clicar em `button.btn-primary` (5,0 s): falhou aqui.

O passo 5 (localizador `button.btn-primary`) falhou com a mensagem abaixo (do navegador, como veio):

> TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.btn-primary")

Como provocar a mesma quebra (forma `harness`, armada por add_init_script no DOMContentLoaded):

> a classe `btn-primary` do botão Entrar vira `btn-entrar`; o roteiro localiza por `button.btn-primary`

- Mutação `trocar_classe` no seletor `form button[type=submit]`, novo valor `btn-entrar`.

Sintoma, como o código o descreveu para o agente:

> A conferência 'passo 5 (clicar em button.btn-primary)' falhou: esperava clicar em button.btn-primary; viu TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.btn-primary").

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 7. Resultado esperado e resultado real

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| passo 5, localizador `button.btn-primary` | um elemento button "Entrar" visível, como na referência | nenhum elemento em 5,0 s: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.btn-primary") |

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: o caso não tem classe nem nível declarados; o roteiro parou no passo 5.

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: o caso não tem classe nem nível declarados. Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).
- Verbetes entregues pela busca e não citados: `tempo_de_resposta_excedido` (Tempo de resposta excedido; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tempo_de_resposta_excedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tempo_de_resposta_excedido.md`); `limites-do-sistema` (O que o sistema não faz; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/limites-do-sistema.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/limites-do-sistema.md`).
- Caso escrito: `localizador-front-admin-login#1` em `cenarios_fase4.py` (catálogo dos dez cenários do ensaio da Fase 5, ficha 36).
- Trilha: `fase4_ensaio_v4/qwen2.5_7b/localizador-front-admin-login#1` em `trilha_cenarios.jsonl`, eventos 268 a 309, hash dos eventos `2d9b755a7eeefe52`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/localizador-front-admin-login__r1.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `localizador_quebrado` (Localizador (seletor) quebrado). Campo: nenhum apontado. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,98 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário não consegue clicar no botão de login, resultando em uma falha na autenticação.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, tempo_de_resposta_excedido, limites-do-sistema estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

Cura do localizador: aplicada `role=button[name="Entrar"]` (estratégia `papel_e_nome`: o elemento é achado pelo papel e pelo nome acessíveis, iguais aos do alvo); reexecução validada; é o mesmo elemento da referência.

Da detecção à reexecução validada: 42,3 s (detecção 06/11/2026 11:23:31; validação 06/11/2026 11:24:13).

Justificativa da cura (gerada por molde, copiada da trilha):

> O passo 5 (button.btn-primary) falhou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.btn-primary"). Dos 6 candidatos previstos, 4 foram gerados da árvore podada e do alvo da referência; 4 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome` (role=button[name="Entrar"]), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 42,3 s.

## 13. Evidência

Alvo registrado na corrida de referência: button "Entrar" (ocorrência 1; tag `button`; caminho `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > button:nth-of-type(1)`).

Candidatos de localizador, na ordem fixa em que o código os tenta (limiar do nome parecido 0.6), e o resultado de cada verificação:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=button[name="Entrar"]` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.319 s) | sim |
| `papel_e_nome_parecido` | não gerado: nenhum button da árvore podada tem nome parecido com "Entrar" acima do limiar 0.6 | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | `text=Entrar` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > button:nth-of-type(1)` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) >> role=button >> nth=0` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 275), feita em código antes de montar o prompt: 9 nós antes, 6 linhas depois. Regras aplicadas: `cartoes_omitidos` 0, `decoracao_removida` 0, `headings_removidos` 0, `imagens_removidas` 1, `interativos_sem_nome_removidos` 0, `listas_achatadas` 0, `textos_sem_letra_removidos` 0.

Trecho podado (hash `b43e3d9b0f628402`):

```text
document "Chuleta Quente - Login"
  text "Login"
  textbox "Login" id="login_usuario" name="login_usuario"
  text "Senha"
  textbox "Senha" id="senha_usuario" name="senha_usuario"
  button "Entrar" class="btn btn-entrar"

```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> localizador_quebrado e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: localizador_quebrado, tempo_de_resposta_excedido, limites-do-sistema

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `localizador_quebrado` (Localizador (seletor) quebrado) | 0,98 | sim |
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 0,00 |  |
| `nulo_inesperado` (Nulo inesperado) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `tempo_de_resposta_excedido`, `limites-do-sistema` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| A linha FONTE só tem identificadores, no formato pedido | `[localizador_quebrado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["localizador_quebrado"]} |
| O verbete citado fala da causa respondida | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 5 do roteiro, trocar o localizador `button.btn-primary` por `role=button[name="Entrar"]` (estratégia `papel_e_nome`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 17. Árvore completa

<details><summary>39 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 268 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:23:25 | roteiro front-admin-login, passo 4, localizador button.btn-primary |
| 269 | 2 | acao | programa | ao_vivo | 2026-11-06T11:23:31 | passo 1: abrir admin/login.php |
| 270 | 3 | acao | programa | ao_vivo | 2026-11-06T11:23:31 | passo 2: esperar aparecer #login_usuario |
| 271 | 4 | acao | programa | ao_vivo | 2026-11-06T11:23:31 | passo 3: preencher #login_usuario |
| 272 | 5 | acao | programa | ao_vivo | 2026-11-06T11:23:31 | passo 4: preencher #senha_usuario |
| 273 | 6 | acao | programa | ao_vivo | 2026-11-06T11:23:31 | passo 5: clicar em button.btn-primary (falhou) |
| 275 | 7 | poda | programa | ao_vivo | 2026-11-06T11:23:31 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 276 | 8 | candidatos | programa | ao_vivo | 2026-11-06T11:23:31 | 3 de 39 verbetes entregues |
| 278 | 9 | prompt | programa | ao_vivo | 2026-11-06T11:23:31 | diagnostico: 3567 caracteres; verbetes localizador_quebrado, tempo_de_resposta_excedido, limites-do-sistema |
| 280 | 10 | inferencia | programa | ao_vivo | 2026-11-06T11:23:31 | diagnostico: 39,6 s |
| 281 | 11 | declaracao | modelo | ao_vivo | 2026-11-06T11:23:31 | causa_raiz: `localizador_quebrado` |
| 282 | 12 | declaracao | modelo | ao_vivo | 2026-11-06T11:23:31 | campo: `nenhum` |
| 283 | 13 | declaracao | modelo | ao_vivo | 2026-11-06T11:23:31 | impacto: `O usuário não consegue clicar no botão de login, resultando em uma falha na autenticação.` |
| 284 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T11:23:31 | fonte: `[localizador_quebrado]` |
| 285 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T11:23:31 | fonte_citada: `localizador_quebrado` |
| 286 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:23:31 | quatro_linhas_presentes: confere |
| 287 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:23:31 | rotulo_no_conjunto: confere |
| 288 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:23:31 | fonte_existe_na_biblioteca: confere |
| 289 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:23:31 | fonte_estava_no_contexto: confere |
| 290 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:23:31 | campo_existe_no_caso: nao_se_aplica |
| 291 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:23:31 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 292 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:23:31 | notas_nos_verbetes_citados: informativo |
| 293 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:23:31 | impacto: nao_verificavel |
| 294 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:23:31 | fonte_formato_valido: confere |
| 295 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:23:31 | fonte_contem_termo_da_causa: confere |
| 296 | 26 | decisao | programa | ao_vivo | 2026-11-06T11:23:31 | diagnostico: escolha localizador_quebrado; divergência entre o declarado e o medido: não |
| 297 | 27 | cura | programa | ao_vivo | 2026-11-06T11:24:13 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 42,3 s |
| 298 | 28 | decisao | programa | ao_vivo | 2026-11-06T11:24:13 | cura: escolha papel_e_nome; divergência entre o declarado e o medido: sim |
| 299 | 29 | acao | programa | ao_vivo | 2026-11-06T11:24:13 | passo 1: abrir admin/login.php; reexecução 1 |
| 300 | 30 | acao | programa | ao_vivo | 2026-11-06T11:24:13 | passo 2: esperar aparecer #login_usuario; reexecução 1 |
| 301 | 31 | acao | programa | ao_vivo | 2026-11-06T11:24:13 | passo 3: preencher #login_usuario; reexecução 1 |
| 302 | 32 | acao | programa | ao_vivo | 2026-11-06T11:24:13 | passo 4: preencher #senha_usuario; reexecução 1 |
| 303 | 33 | acao | programa | ao_vivo | 2026-11-06T11:24:13 | passo 5: clicar em role=button[name="Entrar"]; reexecução 1 |
| 304 | 34 | acao | programa | ao_vivo | 2026-11-06T11:24:13 | passo 6: esperar aparecer h1.breadcrumb; reexecução 1 |
| 305 | 35 | acao | programa | ao_vivo | 2026-11-06T11:24:13 | passo 7: conferir h1.breadcrumb; reexecução 1 |
| 306 | 36 | acao | programa | ao_vivo | 2026-11-06T11:24:13 | passo 8: conferir ; reexecução 1 |
| 307 | 37 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:13 | conferencia_do_roteiro: confere |
| 308 | 38 | verificacao | verificacao | ao_vivo | 2026-11-06T11:24:13 | conferencia_do_roteiro: confere |
| 309 | 39 | decisao | programa | ao_vivo | 2026-11-06T11:24:13 | reexecucao: escolha validada; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 296, decisão `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido.
  - Evidência: evento 275 (arvore_podada); evento 276 (verbete_entregue: `localizador_quebrado`, `tempo_de_resposta_excedido`, `limites-do-sistema`); evento 280 (resposta); evento 285 (verbete_citado: `localizador_quebrado`).
  - Usou: `localizador_quebrado`, `tempo_de_resposta_excedido`, `limites-do-sistema`.
- evento 298, decisão `cura`: escolha `papel_e_nome`; resultado cura_aplicada.
  - Evidência: evento 297 (candidato_de_seletor); evento 275 (arvore_podada).
  - Usou: `papel_e_nome`, `texto_contido`, `caminho_do_ancestral_com_id`, `posicao_entre_irmaos`.
  - Divergência entre o declarado e o medido: sim; falha: nenhuma.
- evento 309, decisão `reexecucao`: escolha `validada`; resultado roteiro_concluido.
  - Evidência: evento 297 (candidato_de_seletor); evento 307 (sinal_em_codigo); evento 308 (sinal_em_codigo).
  - Usou: `papel_e_nome`.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 268 a 309 da trilha; hash dos eventos deste caso: `2d9b755a7eeefe52`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
