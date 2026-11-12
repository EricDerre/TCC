<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `run-1`

Caso `run-1` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/run-1@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (351 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (351 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3503 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `erro_interno_do_servidor` (44,78), `mensagens-de-erro-do-codigo` (29,28) e `contagem_inconsistente` (20,68) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `erro_interno_do_servidor` e `contagem_inconsistente`; o da entidade, em `contagem_inconsistente`; o do status, em `erro_interno_do_servidor` e `mensagens-de-erro-do-codigo` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (20,59), `estrutura_aninhada_divergente` (19,83), `modos-de-injecao` (16,87), `limite_de_requisicoes` (15,82) e `corpo_vazio` (12,61) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 500 e 26 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `contagem_inconsistente`, e o primeiro de fora, `pagina-produtos-api`, só pelo texto do caso o segundo estaria à frente (18,59 contra 17,68); os reforços em código viraram a ordem, com diferença final de 0,09 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `erro_interno_do_servidor` | posição 1, pontuação 44,78: 41,78 pelas palavras do caso, mais 2,0 por rota e 1,0 por status | sim |
| `mensagens-de-erro-do-codigo` | posição 2, pontuação 29,28: 28,28 pelas palavras do caso, mais 1,0 por status | sim |
| `contagem_inconsistente` | posição 3, pontuação 20,68: 17,68 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pagina-produtos-api` | posição 4, pontuação 20,59: 18,59 pelas palavras do caso, mais 2,0 por rota |  |
| `estrutura_aninhada_divergente` | posição 5, pontuação 19,83: 16,83 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `modos-de-injecao` | posição 6, pontuação 16,87: 15,87 pelas palavras do caso, mais 1,0 por status |  |
| `limite_de_requisicoes` | posição 7, pontuação 15,82: 13,82 pelas palavras do caso, mais 2,0 por rota |  |
| `corpo_vazio` | posição 8, pontuação 12,61: 12,61 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `erro_interno_do_servidor` (Erro interno do servidor (500)); segunda: `corpo_nao_e_json`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `erro_interno_do_servidor` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `corpo_nao_e_json` (Corpo não é JSON), ficou com probabilidade 0,000 contra 0,979 da escolhida; verbetes entregues que a sustentam: `erro_interno_do_servidor` e `mensagens-de-erro-do-codigo` (observado).
- As outras 4 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `corpo_vazio` (0,000), `tipo_divergente` (0,000) e `campo_ausente` (0,000) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,979, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 500 (a API falhou por erro interno) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `erro_interno_do_servidor` (declarado).
- Verbete citado `erro_interno_do_servidor`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `erro_interno_do_servidor` e `mensagens-de-erro-do-codigo` (conferido).
- Leitura do verbete `erro_interno_do_servidor` (Erro interno do servidor (500); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/erro_interno_do_servidor.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/erro_interno_do_servidor.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `erro_interno_do_servidor` | 0,979 | `erro_interno_do_servidor` e `mensagens-de-erro-do-codigo` | sim |
| `corpo_nao_e_json` | 0,000 | `erro_interno_do_servidor` e `mensagens-de-erro-do-codigo` |  |
| `corpo_vazio` | 0,000 | `mensagens-de-erro-do-codigo` |  |
| `tipo_divergente` | 0,000 | nenhum |  |
| `campo_ausente` | 0,000 | nenhum |  |
| `campo_renomeado` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A aba de produtos via API exibe a mensagem "Erro ao carregar produtos da CobaiaAPI: erro interno (fault injection)".
> FONTE: [erro_interno_do_servidor]

Resposta inteira:

```text
CAUSA_RAIZ: erro_interno_do_servidor
CAMPO: nenhum
IMPACTO: A aba de produtos via API exibe a mensagem "Erro ao carregar produtos da CobaiaAPI: erro interno (fault injection)".
FONTE: [erro_interno_do_servidor]
```

## Rastro

Gerado dos eventos 470 a 491 da trilha; hash dos eventos deste caso: `3b6c79022d914860` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/run-1@fixture.md`.
