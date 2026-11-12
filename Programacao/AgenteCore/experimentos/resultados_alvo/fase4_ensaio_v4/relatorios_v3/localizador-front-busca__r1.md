<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Localizador (seletor) quebrado no passo 2 do roteiro `front-busca` (localizador `#buscar`), curado pelo agente

Caso `localizador-front-busca#1` da corrida `fase4_ensaio_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ensaio_v4/qwen2.5_7b/localizador-front-busca#1`: o caso `localizador-front-busca#1` na corrida `fase4_ensaio_v4` (execução 1 do cenário `localizador-front-busca`); eventos 225 a 264 da trilha `trilha_cenarios.jsonl`, hash dos eventos `5749715a12eca74e` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Localizador (seletor) quebrado no passo 2 do roteiro `front-busca` (localizador `#buscar`), curado pelo agente

## 3. Data, organização e autor

Observado em 06/11/2026 11:22:04 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 11:13:26 a 06/11/2026 11:26:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `cenarios`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

O roteiro `front-busca` do site PHP (CobaiaFront), a partir da página `index.php`; o alvo do passo que falhou é searchbox "search" (localizador `#buscar`).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `front-busca` do site PHP (cenário `localizador-front-busca` do ensaio da Fase 5, execução 1); quebra de localizador `id_renomeado` (o id (ou o atributo identificador) do alvo é renomeado), forma `harness` (add_init_script no DOMContentLoaded). O passo 2 (esperar aparecer `#buscar`) falhou.

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `index.php` (0,2 s).
2. Esperar aparecer `#buscar` (5,0 s): falhou aqui.

O passo 2 (localizador `#buscar`) falhou com a mensagem abaixo (do navegador, como veio):

> TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("#buscar") to be visible

Como provocar a mesma quebra (forma `harness`, armada por add_init_script no DOMContentLoaded):

> o campo de busca perde o id `buscar` (vira `buscar_v2`); o roteiro localiza por `#buscar`

- Mutação `renomear_id` no seletor `#buscar`, novo valor `buscar_v2`.

Sintoma, como o código o descreveu para o agente:

> A conferência 'passo 2 (esperar #buscar visível)' falhou: esperava esperar #buscar visível; viu TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("#buscar") to be visible.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 7. Resultado esperado e resultado real

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| passo 2, localizador `#buscar` | um elemento searchbox "search" visível, como na referência | nenhum elemento em 5,0 s: TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("#buscar") to be visible |

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: o caso não tem classe nem nível declarados; o roteiro parou no passo 2.

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: o caso não tem classe nem nível declarados. Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).
- Verbetes entregues pela busca e não citados: `tempo_de_resposta_excedido` (Tempo de resposta excedido; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tempo_de_resposta_excedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tempo_de_resposta_excedido.md`); `limites-do-sistema` (O que o sistema não faz; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/limites-do-sistema.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/limites-do-sistema.md`).
- Caso escrito: `localizador-front-busca#1` em `cenarios_fase4.py` (catálogo dos dez cenários do ensaio da Fase 5, ficha 36).
- Trilha: `fase4_ensaio_v4/qwen2.5_7b/localizador-front-busca#1` em `trilha_cenarios.jsonl`, eventos 225 a 264, hash dos eventos `5749715a12eca74e`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/localizador-front-busca__r1.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `localizador_quebrado` (Localizador (seletor) quebrado). Campo: nenhum apontado. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,91 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário não consegue iniciar uma busca, pois o seletor do campo de busca não está sendo encontrado.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, tempo_de_resposta_excedido, limites-do-sistema estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

Cura do localizador: aplicada `role=searchbox[name="search"]` (estratégia `papel_e_nome`: o elemento é achado pelo papel e pelo nome acessíveis, iguais aos do alvo); reexecução validada; é o mesmo elemento da referência.

Da detecção à reexecução validada: 73,3 s (detecção 06/11/2026 11:22:10; validação 06/11/2026 11:23:23).

Justificativa da cura (gerada por molde, copiada da trilha):

> O passo 2 (#buscar) falhou: TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("#buscar") to be visible. Dos 6 candidatos previstos, 3 foram gerados da árvore podada e do alvo da referência; 3 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome` (role=searchbox[name="search"]), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 73,3 s.

## 13. Evidência

Alvo registrado na corrida de referência: searchbox "search" (ocorrência 1; tag `input`; caminho `#form-busca > div:nth-of-type(1) > input:nth-of-type(1)`).

Candidatos de localizador, na ordem fixa em que o código os tenta (limiar do nome parecido 0.6), e o resultado de cada verificação:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=searchbox[name="search"]` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.399 s) | sim |
| `papel_e_nome_parecido` | não gerado: nenhum searchbox da árvore podada tem nome parecido com "search" acima do limiar 0.6 | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | não gerado: o alvo da referência não tem texto visível | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `#form-busca > div:nth-of-type(1) > input:nth-of-type(1)` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `#form-busca > div:nth-of-type(1) >> role=searchbox >> nth=0` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 229), feita em código antes de montar o prompt: 250 nós antes, 37 linhas depois. Regras aplicadas: `cartoes_omitidos` 16, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 21, `interativos_sem_nome_removidos` 14, `listas_achatadas` 18, `textos_sem_letra_removidos` 3.

Trecho podado (hash `81a89f6a009d036c`):

```text
document "Churrascaria Fornalha"
  navigation
    link "Logotipo Fornalha"
    link "DESTAQUES" href="index.php#destaques"
    link "PRODUTOS" href="index.php#produtos"
    link "PRODUTOS (API)" href="produtos_api.php"
    button "TIPOS" class="dropdown-toggle"
    link "CONTATO" href="index.php#contato"
    searchbox "search" id="buscar_v2" name="buscar" class="form-control"
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

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> localizador_quebrado e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,91 contra 0,00; verbete(s) na evidência: localizador_quebrado, tempo_de_resposta_excedido, limites-do-sistema

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `localizador_quebrado` (Localizador (seletor) quebrado) | 0,91 | sim |
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 0,00 |  |

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

Sugestão (o agente não altera a aplicação): no passo 2 do roteiro, trocar o localizador `#buscar` por `role=searchbox[name="search"]` (estratégia `papel_e_nome`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 17. Árvore completa

<details><summary>37 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 225 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:22:04 | roteiro front-busca, passo 1, localizador #buscar |
| 226 | 2 | acao | programa | ao_vivo | 2026-11-06T11:22:10 | passo 1: abrir index.php |
| 227 | 3 | acao | programa | ao_vivo | 2026-11-06T11:22:10 | passo 2: esperar aparecer #buscar (falhou) |
| 229 | 4 | poda | programa | ao_vivo | 2026-11-06T11:22:10 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 230 | 5 | candidatos | programa | ao_vivo | 2026-11-06T11:22:10 | 3 de 39 verbetes entregues |
| 232 | 6 | prompt | programa | ao_vivo | 2026-11-06T11:22:10 | diagnostico: 3586 caracteres; verbetes localizador_quebrado, tempo_de_resposta_excedido, limites-do-sistema |
| 234 | 7 | inferencia | programa | ao_vivo | 2026-11-06T11:22:10 | diagnostico: 70,5 s |
| 235 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:22:10 | causa_raiz: `localizador_quebrado` |
| 236 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:22:10 | campo: `nenhum` |
| 237 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T11:22:10 | impacto: `O usuário não consegue iniciar uma busca, pois o seletor do campo de busca não está sendo encontrado.` |
| 238 | 11 | declaracao | modelo | ao_vivo | 2026-11-06T11:22:10 | fonte: `[localizador_quebrado]` |
| 239 | 12 | declaracao | modelo | ao_vivo | 2026-11-06T11:22:10 | fonte_citada: `localizador_quebrado` |
| 240 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:22:10 | quatro_linhas_presentes: confere |
| 241 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:22:10 | rotulo_no_conjunto: confere |
| 242 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:22:10 | fonte_existe_na_biblioteca: confere |
| 243 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:22:10 | fonte_estava_no_contexto: confere |
| 244 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:22:10 | campo_existe_no_caso: nao_se_aplica |
| 245 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:22:10 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 246 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:22:10 | notas_nos_verbetes_citados: informativo |
| 247 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:22:10 | impacto: nao_verificavel |
| 248 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:22:10 | fonte_formato_valido: confere |
| 249 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:22:10 | fonte_contem_termo_da_causa: confere |
| 250 | 23 | decisao | programa | ao_vivo | 2026-11-06T11:22:10 | diagnostico: escolha localizador_quebrado; divergência entre o declarado e o medido: não |
| 251 | 24 | cura | programa | ao_vivo | 2026-11-06T11:23:23 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 73,3 s |
| 252 | 25 | decisao | programa | ao_vivo | 2026-11-06T11:23:23 | cura: escolha papel_e_nome; divergência entre o declarado e o medido: sim |
| 253 | 26 | acao | programa | ao_vivo | 2026-11-06T11:23:23 | passo 1: abrir index.php; reexecução 1 |
| 254 | 27 | acao | programa | ao_vivo | 2026-11-06T11:23:23 | passo 2: esperar aparecer role=searchbox[name="search"]; reexecução 1 |
| 255 | 28 | acao | programa | ao_vivo | 2026-11-06T11:23:23 | passo 3: preencher role=searchbox[name="search"]; reexecução 1 |
| 256 | 29 | acao | programa | ao_vivo | 2026-11-06T11:23:23 | passo 4: clicar em #form-busca button[type=submit]; reexecução 1 |
| 257 | 30 | acao | programa | ao_vivo | 2026-11-06T11:23:23 | passo 5: esperar aparecer .thumbnail; reexecução 1 |
| 258 | 31 | acao | programa | ao_vivo | 2026-11-06T11:23:23 | passo 6: conferir .thumbnail; reexecução 1 |
| 259 | 32 | acao | programa | ao_vivo | 2026-11-06T11:23:23 | passo 7: conferir h2.breadcrumb; reexecução 1 |
| 260 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:23:23 | conferencia_do_roteiro: confere |
| 261 | 34 | verificacao | verificacao | ao_vivo | 2026-11-06T11:23:23 | conferencia_do_roteiro: confere |
| 262 | 35 | decisao | programa | ao_vivo | 2026-11-06T11:23:23 | reexecucao: escolha validada; divergência entre o declarado e o medido: não |
| 263 | 36 | incidente | programa | ao_vivo | 2026-11-06T11:23:23 | {"decisao": "har", "host": "code.jquery.com", "quando": "2026-11-06T11:22:04", "tipo": "cdn_fora_do_har", "tipo_recurso": "script", "url": "https://code.jquery. |
| 264 | 37 | incidente | programa | ao_vivo | 2026-11-06T11:23:23 | {"decisao": "har", "host": "cdn.jsdelivr.net", "quando": "2026-11-06T11:22:04", "tipo": "cdn_fora_do_har", "tipo_recurso": "script", "url": "https://cdn.jsdeliv |

</details>

Nós de decisão, na ordem:

- evento 250, decisão `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido.
  - Evidência: evento 229 (arvore_podada); evento 230 (verbete_entregue: `localizador_quebrado`, `tempo_de_resposta_excedido`, `limites-do-sistema`); evento 234 (resposta); evento 239 (verbete_citado: `localizador_quebrado`).
  - Usou: `localizador_quebrado`, `tempo_de_resposta_excedido`, `limites-do-sistema`.
- evento 252, decisão `cura`: escolha `papel_e_nome`; resultado cura_aplicada.
  - Evidência: evento 251 (candidato_de_seletor); evento 229 (arvore_podada).
  - Usou: `papel_e_nome`, `caminho_do_ancestral_com_id`, `posicao_entre_irmaos`.
  - Divergência entre o declarado e o medido: sim; falha: nenhuma.
- evento 262, decisão `reexecucao`: escolha `validada`; resultado roteiro_concluido.
  - Evidência: evento 251 (candidato_de_seletor); evento 260 (sinal_em_codigo); evento 261 (sinal_em_codigo).
  - Usou: `papel_e_nome`.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 225 a 264 da trilha; hash dos eventos deste caso: `5749715a12eca74e`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
