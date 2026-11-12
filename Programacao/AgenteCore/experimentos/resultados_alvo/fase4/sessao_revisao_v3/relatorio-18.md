<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 18 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Limite de requisições (429) em `GET /api/produtos`

Caso `relatorio-18` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-18`: o caso `relatorio-18` na corrida `fase4_ineditos`; eventos 595 a 616 da trilha `trilha_ineditos.jsonl`, hash dos eventos `3a4fd6a256130d34` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Limite de requisições (429) em `GET /api/produtos`

## 3. Data, organização e autor

Observado em 06/11/2026 14:20:38 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-18`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 429 (a API barrou por excesso de requisições).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"detail": "limite de requisições excedido"}
```

4. Sintoma observado (texto do caso):

> A pagina Produtos (API) abre sem nenhum cartao; a linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI: HTTP 429'.

5. Observação adicional (texto do caso):

> A resposta traz o cabecalho Retry-After: 60.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A pagina Produtos (API) abre sem nenhum cartao; a linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI: HTTP 429'. |

Corpo recebido, como veio no caso:

```text
{"detail": "limite de requisições excedido"}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `limite_de_requisicoes` (Limite de requisições (429); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/limite_de_requisicoes.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/limite_de_requisicoes.md`).
- Verbetes entregues pela busca e não citados: `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`); `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`).
- Caso escrito: `relatorio-18` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-18` em `trilha_ineditos.jsonl`, eventos 595 a 616, hash dos eventos `3a4fd6a256130d34`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `limite_de_requisicoes` (Limite de requisições (429)). Campo: nenhum apontado. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,64 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `A página Produtos fica vazia, e a linha de status indica um erro de carregamento devido ao excesso de requisições.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu limite_de_requisicoes porque os verbetes limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,64); trate como hipótese e confira o caso antes de agir.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 429

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "limite de requisições excedido"}

SINTOMA OBSERVADO: A pagina Produtos (API) abre sem nenhum cartao; a linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI: HTTP 429'.

OBSERVAÇÃO ADICIONAL: A resposta traz o cabecalho Retry-After: 60.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> limite_de_requisicoes e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,64 contra 0,00; verbete(s) na evidência: limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `limite_de_requisicoes` (Limite de requisições (429)) | 0,64 | sim |
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[limite_de_requisicoes]`; verbetes citados: `limite_de_requisicoes` (Limite de requisições (429); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/limite_de_requisicoes.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/limite_de_requisicoes.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `limite_de_requisicoes` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `limite_de_requisicoes` | confere | contexto: `limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `limite_de_requisicoes` | confere | verbetes: `limite_de_requisicoes` |
| A linha FONTE só tem identificadores, no formato pedido | `[limite_de_requisicoes]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["limite_de_requisicoes"]} |
| O verbete citado fala da causa respondida | `limite_de_requisicoes` | confere | {"termo": "limite_de_requisicoes"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 595 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:20:38 | caso relatorio-18 |
| 596 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:20:38 | 3 de 39 verbetes entregues |
| 598 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:20:38 | diagnostico: 3888 caracteres; verbetes limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente |
| 600 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:20:38 | diagnostico: 76,9 s |
| 601 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:20:38 | causa_raiz: `limite_de_requisicoes` |
| 602 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:20:38 | campo: `nenhum` |
| 603 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:20:38 | impacto: `A página Produtos fica vazia, e a linha de status indica um erro de carregamento devido ao excesso de requisições.` |
| 604 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:20:38 | fonte: `[limite_de_requisicoes]` |
| 605 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:20:38 | fonte_citada: `limite_de_requisicoes` |
| 606 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | quatro_linhas_presentes: confere |
| 607 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | rotulo_no_conjunto: confere |
| 608 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | fonte_existe_na_biblioteca: confere |
| 609 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | fonte_estava_no_contexto: confere |
| 610 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | campo_existe_no_caso: nao_se_aplica |
| 611 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 612 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | notas_nos_verbetes_citados: informativo |
| 613 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | impacto: nao_verificavel |
| 614 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | fonte_formato_valido: confere |
| 615 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | fonte_contem_termo_da_causa: confere |
| 616 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:20:38 | diagnostico: escolha limite_de_requisicoes; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 616, decisão `diagnostico`: escolha `limite_de_requisicoes`; resultado rotulo_emitido.
  - Evidência: evento 596 (verbete_entregue: `limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente`); evento 600 (resposta); evento 605 (verbete_citado: `limite_de_requisicoes`).
  - Usou: `limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 595 a 616 da trilha; hash dos eventos deste caso: `3a4fd6a256130d34`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-18`

Caso `relatorio-18` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-18`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 22 afirmações (14 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (510 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (510 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3888 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `limite_de_requisicoes` (59,46), `contagem_inconsistente` (25,48) e `estrutura_aninhada_divergente` (24,59) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `limite_de_requisicoes`, `contagem_inconsistente` e `estrutura_aninhada_divergente`; o da entidade, em `contagem_inconsistente` e `estrutura_aninhada_divergente`; o do status, em `limite_de_requisicoes` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `tempo_de_resposta_excedido` (23,70), `mensagens-de-erro-do-codigo` (22,14), `pagina-produtos-api` (19,85), `corpo_vazio` (17,44) e `erro_interno_do_servidor` (13,12) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 429 e 43 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `estrutura_aninhada_divergente`, e o primeiro de fora, `tempo_de_resposta_excedido`, só o texto do caso já punha o primeiro à frente (21,59 contra 20,70), e os reforços em código levaram a diferença a 0,89 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `limite_de_requisicoes` | posição 1, pontuação 59,46: 56,46 pelas palavras do caso, mais 2,0 por rota e 1,0 por status | sim |
| `contagem_inconsistente` | posição 2, pontuação 25,48: 22,48 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 3, pontuação 24,59: 21,59 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tempo_de_resposta_excedido` | posição 4, pontuação 23,70: 20,70 pelas palavras do caso, mais 2,0 por rota e 1,0 por status |  |
| `mensagens-de-erro-do-codigo` | posição 5, pontuação 22,14: 22,14 pelas palavras do caso, sem reforço |  |
| `pagina-produtos-api` | posição 6, pontuação 19,85: 17,85 pelas palavras do caso, mais 2,0 por rota |  |
| `corpo_vazio` | posição 7, pontuação 17,44: 17,44 pelas palavras do caso, sem reforço |  |
| `erro_interno_do_servidor` | posição 8, pontuação 13,12: 11,12 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `limite_de_requisicoes` (Limite de requisições (429)); segunda: `tempo_de_resposta_excedido`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `limite_de_requisicoes` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `tempo_de_resposta_excedido` (Tempo de resposta excedido), ficou com probabilidade 0,000 contra 0,640 da escolhida; verbetes entregues que a sustentam: `limite_de_requisicoes` (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,640, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 429 (a API barrou por excesso de requisições) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `limite_de_requisicoes` (declarado).
- Verbete citado `limite_de_requisicoes`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `limite_de_requisicoes` (conferido).
- Leitura do verbete `limite_de_requisicoes` (Limite de requisições (429); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/limite_de_requisicoes.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/limite_de_requisicoes.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `limite_de_requisicoes` | 0,640 | `limite_de_requisicoes` | sim |
| `tempo_de_resposta_excedido` | 0,000 | `limite_de_requisicoes` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A página Produtos fica vazia, e a linha de status indica um erro de carregamento devido ao excesso de requisições.
> FONTE: [limite_de_requisicoes]

Resposta inteira:

```text
CAUSA_RAIZ: limite_de_requisicoes
CAMPO: nenhum
IMPACTO: A página Produtos fica vazia, e a linha de status indica um erro de carregamento devido ao excesso de requisições.
FONTE: [limite_de_requisicoes]
```

## Rastro

Gerado dos eventos 595 a 616 da trilha; hash dos eventos deste caso: `3a4fd6a256130d34` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-18.md`.
