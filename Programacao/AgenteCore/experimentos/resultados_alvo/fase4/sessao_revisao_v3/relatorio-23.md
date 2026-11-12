<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 23 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Nulo inesperado em `GET /api/produtos/12`, campo `resumo`

Caso `relatorio-23` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-23`: o caso `relatorio-23` na corrida `fase4_ineditos`; eventos 395 a 416 da trilha `trilha_ineditos.jsonl`, hash dos eventos `d4c192c507f326d8` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Nulo inesperado em `GET /api/produtos/12`, campo `resumo`

## 3. Data, organização e autor

Observado em 06/11/2026 14:11:23 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/12` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-23`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/12`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"id": 12, "nome": "Queijo Coalho", "resumo": null, "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}
```

4. Sintoma observado (texto do caso):

> O cartao do Queijo Coalho na grade mostra a descricao 'Queijo coalho grelhado com mel', mas o modal aberto pelo 'Saiba Mais...' desse mesmo produto mostra '(sem descrição)'. As duas respostas chegaram com status 200.

5. Observação adicional (texto do caso):

> A listagem GET /api/produtos, feita antes do clique, trouxe este produto (id 12) com o resumo preenchido. O contrato permite resumo nulo (texto|nulo).


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/12` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O cartao do Queijo Coalho na grade mostra a descricao 'Queijo coalho grelhado com mel', mas o modal aberto pelo 'Saiba Mais...' desse mesmo produto mostra '(sem descrição)'. As duas respostas chegaram com status 200. |

Corpo recebido, como veio no caso:

```text
{"id": 12, "nome": "Queijo Coalho", "resumo": null, "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`).
- Verbetes entregues pela busca e não citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `relatorio-23` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-23` em `trilha_ineditos.jsonl`, eventos 395 a 416, hash dos eventos `d4c192c507f326d8`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `nulo_inesperado` (Nulo inesperado). Campo: `resumo`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,89 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê uma descrição no cardápio, mas no modal, o campo 'Saiba Mais...' está vazio.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu nulo_inesperado no campo resumo porque os verbetes contrato-produto, nulo_inesperado, entidade-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,04. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/12

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 12, "nome": "Queijo Coalho", "resumo": null, "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}

SINTOMA OBSERVADO: O cartao do Queijo Coalho na grade mostra a descricao 'Queijo coalho grelhado com mel', mas o modal aberto pelo 'Saiba Mais...' desse mesmo produto mostra '(sem descrição)'. As duas respostas chegaram com status 200.

OBSERVAÇÃO ADICIONAL: A listagem GET /api/produtos, feita antes do clique, trouxe este produto (id 12) com o resumo preenchido. O contrato permite resumo nulo (texto|nulo).
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> nulo_inesperado e não campo_ausente: a escolha tem probabilidade 0,89 contra 0,04; verbete(s) na evidência: contrato-produto, nulo_inesperado, entidade-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `nulo_inesperado` (Nulo inesperado) | 0,89 | sim |
| `campo_ausente` (Campo ausente) | 0,04 |  |
| `campo_renomeado` (Campo renomeado) | 0,04 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,04 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,01 |  |
| `tipo_divergente` (Tipo divergente) | 0,01 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `contrato-produto`, `nulo_inesperado`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| A linha FONTE só tem identificadores, no formato pedido | `[nulo_inesperado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["nulo_inesperado"]} |
| O verbete citado fala da causa respondida | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `resumo` no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 395 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:11:23 | caso relatorio-23 |
| 396 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:11:23 | 3 de 39 verbetes entregues |
| 398 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:11:23 | diagnostico: 3672 caracteres; verbetes contrato-produto, nulo_inesperado, entidade-produto |
| 400 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:11:23 | diagnostico: 72,7 s |
| 401 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:11:23 | causa_raiz: `nulo_inesperado` |
| 402 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:11:23 | campo: `resumo` |
| 403 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:11:23 | impacto: `O usuário vê uma descrição no cardápio, mas no modal, o campo 'Saiba Mais...' está vazio.` |
| 404 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:11:23 | fonte: `[nulo_inesperado]` |
| 405 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:11:23 | fonte_citada: `nulo_inesperado` |
| 406 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | quatro_linhas_presentes: confere |
| 407 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | rotulo_no_conjunto: confere |
| 408 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | fonte_existe_na_biblioteca: confere |
| 409 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | fonte_estava_no_contexto: confere |
| 410 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | campo_existe_no_caso: confere |
| 411 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 412 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | notas_nos_verbetes_citados: informativo |
| 413 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | impacto: nao_verificavel |
| 414 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | fonte_formato_valido: confere |
| 415 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | fonte_contem_termo_da_causa: confere |
| 416 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:11:23 | diagnostico: escolha nulo_inesperado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 416, decisão `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido.
  - Evidência: evento 396 (verbete_entregue: `contrato-produto`, `nulo_inesperado`, `entidade-produto`); evento 400 (resposta); evento 405 (verbete_citado: `nulo_inesperado`).
  - Usou: `contrato-produto`, `nulo_inesperado`, `entidade-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 395 a 416 da trilha; hash dos eventos deste caso: `d4c192c507f326d8`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-23`

Caso `relatorio-23` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-23`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (771 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (771 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3672 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-produto` (49,04), `nulo_inesperado` (38,59) e `entidade-produto` (36,07) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto` e `entidade-produto`; o da entidade, em `contrato-produto` e `entidade-produto`; `nulo_inesperado` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (29,14), `colecao_no_lugar_de_objeto` (26,89), `campo_renomeado` (25,69), `campo_ausente` (22,80) e `estado_da_tela_divergente` (22,79) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 74 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (33,07 contra 27,14), e os reforços em código levaram a diferença a 6,92 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-produto` | posição 1, pontuação 49,04: 46,04 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `nulo_inesperado` | posição 2, pontuação 38,59: 38,59 pelas palavras do caso, sem reforço | sim |
| `entidade-produto` | posição 3, pontuação 36,07: 33,07 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pagina-produtos-api` | posição 4, pontuação 29,14: 27,14 pelas palavras do caso, mais 2,0 por rota |  |
| `colecao_no_lugar_de_objeto` | posição 5, pontuação 26,89: 23,89 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_renomeado` | posição 6, pontuação 25,69: 24,69 pelas palavras do caso, mais 1,0 por entidade |  |
| `campo_ausente` | posição 7, pontuação 22,80: 21,80 pelas palavras do caso, mais 1,0 por entidade |  |
| `estado_da_tela_divergente` | posição 8, pontuação 22,79: 22,79 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `nulo_inesperado` (Nulo inesperado); segunda: `campo_ausente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `nulo_inesperado` (declarado).
- O modelo apontou o campo `resumo` (declarado).
- `resumo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,040 contra 0,892 da escolhida; verbetes entregues que a sustentam: `contrato-produto` e `nulo_inesperado` (observado).
- As outras 10 alternativas lidas na resposta somam probabilidade 0,103; as maiores: `campo_renomeado` (0,040), `chave_de_juncao_errada` (0,039) e `valor_fora_do_dominio` (0,009) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,892, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/12`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `nulo_inesperado` (declarado).
- Verbete citado `nulo_inesperado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `nulo_inesperado` (conferido).
- Leitura do verbete `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `nulo_inesperado` | 0,892 | `nulo_inesperado` | sim |
| `campo_ausente` | 0,040 | `contrato-produto` e `nulo_inesperado` |  |
| `campo_renomeado` | 0,040 | `contrato-produto` |  |
| `chave_de_juncao_errada` | 0,039 | `nulo_inesperado` e `entidade-produto` |  |
| `valor_fora_do_dominio` | 0,009 | `nulo_inesperado` |  |
| `tipo_divergente` | 0,008 | `contrato-produto` e `entidade-produto` |  |
| `formato_de_data_divergente` | 0,003 | nenhum |  |
| `resposta_truncada` | 0,002 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,001 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê uma descrição no cardápio, mas no modal, o campo 'Saiba Mais...' está vazio.
> FONTE: [nulo_inesperado]

Resposta inteira:

```text
CAUSA_RAIZ: nulo_inesperado
CAMPO: resumo
IMPACTO: O usuário vê uma descrição no cardápio, mas no modal, o campo 'Saiba Mais...' está vazio.
FONTE: [nulo_inesperado]
```

## Rastro

Gerado dos eventos 395 a 416 da trilha; hash dos eventos deste caso: `d4c192c507f326d8` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-23.md`.
