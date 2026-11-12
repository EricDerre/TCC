<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-21`

Caso `tra-21` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/tra-21@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (585 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (585 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3656 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contagem_inconsistente` (39,41), `entidade-produto` (24,57) e `contrato-produto` (18,79) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contagem_inconsistente`, `entidade-produto` e `contrato-produto`; o da entidade, em `contagem_inconsistente`, `entidade-produto` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `localizador_quebrado` (16,89), `colecao_no_lugar_de_objeto` (16,65), `campo_ausente` (16,65), `tempo_de_resposta_excedido` (16,31) e `estrutura_aninhada_divergente` (15,90) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 47 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `localizador_quebrado`, só pelo texto do caso o segundo estaria à frente (16,89 contra 15,79); os reforços em código viraram a ordem, com diferença final de 1,90 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contagem_inconsistente` | posição 1, pontuação 39,41: 36,41 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 2, pontuação 24,57: 21,57 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 18,79: 15,79 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `localizador_quebrado` | posição 4, pontuação 16,89: 16,89 pelas palavras do caso, sem reforço |  |
| `colecao_no_lugar_de_objeto` | posição 5, pontuação 16,65: 13,65 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_ausente` | posição 6, pontuação 16,65: 13,65 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tempo_de_resposta_excedido` | posição 7, pontuação 16,31: 13,31 pelas palavras do caso, mais 2,0 por rota e 1,0 por status |  |
| `estrutura_aninhada_divergente` | posição 8, pontuação 15,90: 12,90 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `contagem_inconsistente` (Contagem inconsistente); segunda: `resposta_truncada`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `contagem_inconsistente` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `resposta_truncada` (Resposta truncada), ficou com probabilidade 0,003 contra 0,986 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 5 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `colecao_no_lugar_de_objeto` (0,000), `corpo_nao_e_json` (0,000) e `corpo_vazio` (0,000) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,986, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contagem_inconsistente` (declarado).
- Verbete citado `contagem_inconsistente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contagem_inconsistente` (conferido).
- Leitura do verbete `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `contagem_inconsistente` | 0,986 | `contagem_inconsistente` | sim |
| `resposta_truncada` | 0,003 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê uma lista incompleta de produtos, com um item ausente que deveria estar presente.
> FONTE: [contagem_inconsistente]

Resposta inteira:

```text
CAUSA_RAIZ: contagem_inconsistente
CAMPO: nenhum
IMPACTO: O usuário vê uma lista incompleta de produtos, com um item ausente que deveria estar presente.
FONTE: [contagem_inconsistente]
```

## Rastro

Gerado dos eventos 2055 a 2076 da trilha; hash dos eventos deste caso: `2f9f1603e36de699` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-21@fixture.md`.
