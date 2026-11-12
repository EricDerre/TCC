<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `run-22`

Caso `run-22` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/run-22`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

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

Gerado dos eventos 595 a 616 da trilha; hash dos eventos deste caso: `3a4fd6a256130d34` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/run-22.md`.
