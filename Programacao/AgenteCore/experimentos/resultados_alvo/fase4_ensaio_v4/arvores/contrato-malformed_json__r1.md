<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `contrato-malformed_json#1`

Caso `contrato-malformed_json#1` da corrida `fase4_ensaio_v4`, trilha `fase4_ensaio_v4/qwen2.5_7b/contrato-malformed_json#1`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 29 afirmações (21 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (21 linhas) e a diferença do corpo da resposta (50 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 47 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 54 nós a 21 linhas (observado).
- O que saiu, pelas regras em código: 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 2 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `22 linha(s) da referência`, recebido `4 linha(s) novas` (observado).
- A poda do corpo da resposta levou 47 caracteres a 50 caracteres: só a diferença contra o contrato esperado pela interface vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, no corpo inteiro (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3938 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 22 linha(s) da referência | 4 linha(s) novas |
| corpo inteiro | JSON completo e válido | corpo truncado |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 54 nós |  |
| a árvore podada | 21 linhas | sim |
| o corpo da resposta inteiro | 47 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface | 50 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `resposta_truncada` (33,07), `contagem_inconsistente` (26,07) e `entidade-produto` (23,08) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contagem_inconsistente` e `entidade-produto`; o da entidade, em `contagem_inconsistente` e `entidade-produto`; `resposta_truncada` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `limites-do-sistema` (19,76), `tempo_de_resposta_excedido` (17,97), `colecao_no_lugar_de_objeto` (17,63), `corpo_nao_e_json` (14,76) e `estrutura_aninhada_divergente` (14,61) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 45 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `limites-do-sistema`, só o texto do caso já punha o primeiro à frente (20,08 contra 19,76), e os reforços em código levaram a diferença a 3,32 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `resposta_truncada` | posição 1, pontuação 33,07: 33,07 pelas palavras do caso, sem reforço | sim |
| `contagem_inconsistente` | posição 2, pontuação 26,07: 23,07 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 3, pontuação 23,08: 20,08 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `limites-do-sistema` | posição 4, pontuação 19,76: 19,76 pelas palavras do caso, sem reforço |  |
| `tempo_de_resposta_excedido` | posição 5, pontuação 17,97: 14,97 pelas palavras do caso, mais 2,0 por rota e 1,0 por status |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 17,63: 14,63 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `corpo_nao_e_json` | posição 7, pontuação 14,76: 13,76 pelas palavras do caso, mais 1,0 por status |  |
| `estrutura_aninhada_divergente` | posição 8, pontuação 14,61: 11,61 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `resposta_truncada` (Resposta truncada); segunda: `corpo_nao_e_json`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `resposta_truncada` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `corpo_nao_e_json` (Corpo não é JSON), ficou com probabilidade 0,001 contra 0,999 da escolhida; verbetes entregues que a sustentam: `resposta_truncada` (observado).
- A outra alternativa lida na resposta, `corpo_vazio`, tem probabilidade 0,001 (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,999, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `esperado JSON completo e válido, recebido corpo truncado` (observado).
- A linha FONTE cita `resposta_truncada` (declarado).
- Verbete citado `resposta_truncada`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `resposta_truncada` (conferido).
- Leitura do verbete `resposta_truncada` (Resposta truncada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/resposta_truncada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/resposta_truncada.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `resposta_truncada` | 0,999 | `resposta_truncada` | sim |
| `corpo_nao_e_json` | 0,001 | `resposta_truncada` |  |
| `corpo_vazio` | 0,001 | `resposta_truncada` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A interface exibe uma mensagem de erro ao carregar produtos, pois a resposta da API é cortada e não pode ser interpretada corretamente, resultando em uma exibição vazia de cartões de produtos.
> FONTE: [resposta_truncada]

Resposta inteira:

```text
CAUSA_RAIZ: resposta_truncada
CAMPO: nenhum
IMPACTO: A interface exibe uma mensagem de erro ao carregar produtos, pois a resposta da API é cortada e não pode ser interpretada corretamente, resultando em uma exibição vazia de cartões de produtos.
FONTE: [resposta_truncada]
```

## Rastro

Gerado dos eventos 7 a 38 da trilha; hash dos eventos deste caso: `1a8231a6607840d1` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/contrato-malformed_json__r1.md`.
