<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `run-2`

Caso `run-2` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/run-2@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (333 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (333 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3445 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `tempo_de_resposta_excedido` (32,08), `limite_de_requisicoes` (16,53) e `estado_da_tela_divergente` (13,58) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `tempo_de_resposta_excedido` e `limite_de_requisicoes`; `estado_da_tela_divergente` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `corpo_nao_e_json` (11,28), `limites-do-sistema` (10,39), `contagem_inconsistente` (10,17), `corpo_vazio` (9,63) e `mensagens-de-erro-do-codigo` (9,19) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status nenhum e 21 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `estado_da_tela_divergente`, e o primeiro de fora, `corpo_nao_e_json`, só o texto do caso já punha o primeiro à frente (13,58 contra 11,28); a diferença final foi 2,30 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `tempo_de_resposta_excedido` | posição 1, pontuação 32,08: 30,08 pelas palavras do caso, mais 2,0 por rota | sim |
| `limite_de_requisicoes` | posição 2, pontuação 16,53: 14,53 pelas palavras do caso, mais 2,0 por rota | sim |
| `estado_da_tela_divergente` | posição 3, pontuação 13,58: 13,58 pelas palavras do caso, sem reforço | sim |
| `corpo_nao_e_json` | posição 4, pontuação 11,28: 11,28 pelas palavras do caso, sem reforço |  |
| `limites-do-sistema` | posição 5, pontuação 10,39: 10,39 pelas palavras do caso, sem reforço |  |
| `contagem_inconsistente` | posição 6, pontuação 10,17: 7,17 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `corpo_vazio` | posição 7, pontuação 9,63: 9,63 pelas palavras do caso, sem reforço |  |
| `mensagens-de-erro-do-codigo` | posição 8, pontuação 9,19: 9,19 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `tempo_de_resposta_excedido` (Tempo de resposta excedido); segunda: `limite_de_requisicoes`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `tempo_de_resposta_excedido` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `limite_de_requisicoes` (Limite de requisições (429)), ficou com probabilidade 0,000 contra 1,000 da escolhida; verbetes entregues que a sustentam: `tempo_de_resposta_excedido` e `limite_de_requisicoes` (observado).
- As outras 4 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `estado_da_tela_divergente` (0,000), `corpo_nao_e_json` (0,000) e `corpo_vazio` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 1,000, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status não registrado e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `tempo_de_resposta_excedido` (declarado).
- Verbete citado `tempo_de_resposta_excedido`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `tempo_de_resposta_excedido` e `limite_de_requisicoes` (conferido).
- Leitura do verbete `tempo_de_resposta_excedido` (Tempo de resposta excedido; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tempo_de_resposta_excedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tempo_de_resposta_excedido.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `tempo_de_resposta_excedido` | 1,000 | `tempo_de_resposta_excedido` e `limite_de_requisicoes` | sim |
| `limite_de_requisicoes` | 0,000 | `tempo_de_resposta_excedido` e `limite_de_requisicoes` |  |
| `estado_da_tela_divergente` | 0,000 | `estado_da_tela_divergente` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | `tempo_de_resposta_excedido` e `estado_da_tela_divergente` |  |
| `resposta_truncada` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A página fica carregando e depois exibe erro de rede, pois a requisição demorou mais do que o esperado e foi interrompida pelo cliente.
> FONTE: [tempo_de_resposta_excedido]

Resposta inteira:

```text
CAUSA_RAIZ: tempo_de_resposta_excedido
CAMPO: nenhum
IMPACTO: A página fica carregando e depois exibe erro de rede, pois a requisição demorou mais do que o esperado e foi interrompida pelo cliente.
FONTE: [tempo_de_resposta_excedido]
```

## Rastro

Gerado dos eventos 528 a 549 da trilha; hash dos eventos deste caso: `12d53307ed152093` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/run-2@fixture.md`.
