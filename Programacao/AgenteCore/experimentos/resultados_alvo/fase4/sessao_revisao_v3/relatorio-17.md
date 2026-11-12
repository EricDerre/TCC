<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 17 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Resposta truncada em `GET /api/produtos`

Caso `relatorio-17` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-17`: o caso `relatorio-17` na corrida `fase4_ineditos`; eventos 518 a 543 da trilha `trilha_ineditos.jsonl`, hash dos eventos `f5c0d6160c72a344` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Resposta truncada em `GET /api/produtos`

## 3. Data, organização e autor

Observado em 06/11/2026 14:17:25 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-17`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}, {"id": 13, "nome": "Hambúrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}]
```

4. Sintoma observado (texto do caso):

> A grade mostra 13 cartoes e termina no Hamburguer Artesanal; a unica sobremesa (Abacaxi na Brasa) nao aparece. A tabela tbprodutos tem 14 linhas.

5. Observação adicional (texto do caso):

> O corpo mostra so os dois ultimos itens da lista recebida (13 itens no total, ids de 1 a 13).


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A grade mostra 13 cartoes e termina no Hamburguer Artesanal; a unica sobremesa (Abacaxi na Brasa) nao aparece. A tabela tbprodutos tem 14 linhas. |

Corpo recebido, como veio no caso:

```text
[{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}, {"id": 13, "nome": "Hambúrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `relatorio-17` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-17` em `trilha_ineditos.jsonl`, eventos 518 a 543, hash dos eventos `f5c0d6160c72a344`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `resposta_truncada` (Resposta truncada). Campo: nenhum apontado. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `A interface exibe apenas os dois últimos itens da lista, deixando de mostrar 11 itens importantes.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu resposta_truncada porque os verbetes entidade-produto, contrato-produto, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}, {"id": 13, "nome": "Hambúrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}]

SINTOMA OBSERVADO: A grade mostra 13 cartoes e termina no Hamburguer Artesanal; a unica sobremesa (Abacaxi na Brasa) nao aparece. A tabela tbprodutos tem 14 linhas.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os dois ultimos itens da lista recebida (13 itens no total, ids de 1 a 13).
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> resposta_truncada e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, contagem_inconsistente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `resposta_truncada` (Resposta truncada) | 1,00 | sim |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `contagem_inconsistente` (Contagem inconsistente) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [contagem_inconsistente]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto] [contagem_inconsistente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "contagem_inconsistente"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "resposta_truncada"} |
| O verbete citado fala da causa respondida | `contagem_inconsistente` | não confere | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 518 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:17:25 | caso relatorio-17 |
| 519 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:17:25 | 3 de 39 verbetes entregues |
| 521 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:17:25 | diagnostico: 3913 caracteres; verbetes entidade-produto, contrato-produto, contagem_inconsistente |
| 523 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:17:25 | diagnostico: 60,9 s |
| 524 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:17:25 | causa_raiz: `resposta_truncada` |
| 525 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:17:25 | campo: `nenhum` |
| 526 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:17:25 | impacto: `A interface exibe apenas os dois últimos itens da lista, deixando de mostrar 11 itens importantes.` |
| 527 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:17:25 | fonte: `[contrato-produto] [contagem_inconsistente]` |
| 528 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:17:25 | fonte_citada: `contrato-produto` |
| 529 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T14:17:25 | fonte_citada: `contagem_inconsistente` |
| 530 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | quatro_linhas_presentes: confere |
| 531 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | rotulo_no_conjunto: confere |
| 532 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | fonte_existe_na_biblioteca: confere |
| 533 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | fonte_existe_na_biblioteca: confere |
| 534 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | fonte_estava_no_contexto: confere |
| 535 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | fonte_estava_no_contexto: confere |
| 536 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | campo_existe_no_caso: nao_se_aplica |
| 537 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 538 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | notas_nos_verbetes_citados: informativo |
| 539 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | impacto: nao_verificavel |
| 540 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | fonte_formato_valido: confere |
| 541 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | fonte_contem_termo_da_causa: nao_confere |
| 542 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T14:17:25 | fonte_contem_termo_da_causa: nao_confere |
| 543 | 24 | decisao | programa | ao_vivo | 2026-11-06T14:17:25 | diagnostico: escolha resposta_truncada; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 543, decisão `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido.
  - Evidência: evento 519 (verbete_entregue: `entidade-produto`, `contrato-produto`, `contagem_inconsistente`); evento 523 (resposta); evento 528 (verbete_citado: `contrato-produto`); evento 529 (verbete_citado: `contagem_inconsistente`).
  - Usou: `entidade-produto`, `contrato-produto`, `contagem_inconsistente`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 518 a 543 da trilha; hash dos eventos deste caso: `f5c0d6160c72a344`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-17`

Caso `relatorio-17` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-17`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (842 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (842 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3913 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (47,42), `contrato-produto` (44,90) e `contagem_inconsistente` (35,67) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `contagem_inconsistente`; o da entidade, em `entidade-produto`, `contrato-produto` e `contagem_inconsistente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estrutura_aninhada_divergente` (27,17), `chave_de_juncao_errada` (26,45), `pagina-produtos-api` (26,09), `tipo_divergente` (26,06) e `estado_da_tela_divergente` (22,87) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 79 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `contagem_inconsistente`, e o primeiro de fora, `estrutura_aninhada_divergente`, só o texto do caso já punha o primeiro à frente (32,67 contra 24,17), e os reforços em código levaram a diferença a 8,50 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 47,42: 44,42 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 44,90: 41,90 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contagem_inconsistente` | posição 3, pontuação 35,67: 32,67 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 4, pontuação 27,17: 24,17 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 5, pontuação 26,45: 24,45 pelas palavras do caso, mais 2,0 por rota |  |
| `pagina-produtos-api` | posição 6, pontuação 26,09: 24,09 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 7, pontuação 26,06: 23,06 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estado_da_tela_divergente` | posição 8, pontuação 22,87: 22,87 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `resposta_truncada` (Resposta truncada); segunda: `corpo_nao_e_json`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `resposta_truncada` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `corpo_nao_e_json` (Corpo não é JSON), ficou com probabilidade 0,001 contra 0,997 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,002; as maiores: `corpo_vazio` (0,001), `colecao_no_lugar_de_objeto` (0,001) e `campo_ausente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,997, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `contagem_inconsistente` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `contagem_inconsistente`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 7 de 10 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `resposta_truncada` | 0,997 | nenhum | sim |
| `corpo_nao_e_json` | 0,001 | nenhum |  |
| `corpo_vazio` | 0,001 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,001 | `contrato-produto` |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `tipo_divergente` | 0,000 | `entidade-produto` e `contrato-produto` |  |
| `estrutura_aninhada_divergente` | 0,000 | `contagem_inconsistente` |  |
| `contagem_inconsistente` | 0,000 | `contagem_inconsistente` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A interface exibe apenas os dois últimos itens da lista, deixando de mostrar 11 itens importantes.
> FONTE: [contrato-produto] [contagem_inconsistente]

Resposta inteira:

```text
CAUSA_RAIZ: resposta_truncada
CAMPO: nenhum
IMPACTO: A interface exibe apenas os dois últimos itens da lista, deixando de mostrar 11 itens importantes.
FONTE: [contrato-produto] [contagem_inconsistente]
```

## Rastro

Gerado dos eventos 518 a 543 da trilha; hash dos eventos deste caso: `f5c0d6160c72a344` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-17.md`.
