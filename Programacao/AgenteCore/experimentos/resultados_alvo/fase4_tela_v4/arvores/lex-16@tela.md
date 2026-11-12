<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-16`

Caso `lex-16` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/lex-16@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 29 afirmações (21 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (21 linhas) e a diferença do corpo da resposta (50 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 47 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 54 nós a 21 linhas (observado).
- O que saiu, pelas regras em código: 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 2 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `25 linha(s) da referência`, recebido `4 linha(s) novas` (observado).
- A poda do corpo da resposta levou 47 caracteres a 50 caracteres: só a diferença contra o contrato esperado pela interface vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, no corpo inteiro (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4224 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 25 linha(s) da referência | 4 linha(s) novas |
| corpo inteiro | JSON completo e válido | corpo truncado |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 54 nós |  |
| a árvore podada | 21 linhas | sim |
| o corpo da resposta inteiro | 47 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface | 50 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `resposta_truncada` (38,43), `entidade-produto` (23,73) e `colecao_no_lugar_de_objeto` (23,42) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `colecao_no_lugar_de_objeto`; o da entidade, em `entidade-produto` e `colecao_no_lugar_de_objeto`; `resposta_truncada` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `limites-do-sistema` (21,08), `tempo_de_resposta_excedido` (19,59), `contagem_inconsistente` (18,24), `modos-de-injecao` (17,93) e `corpo_nao_e_json` (17,56) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 50 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `colecao_no_lugar_de_objeto`, e o primeiro de fora, `limites-do-sistema`, só pelo texto do caso o segundo estaria à frente (21,08 contra 20,42); os reforços em código viraram a ordem, com diferença final de 2,34 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `resposta_truncada` | posição 1, pontuação 38,43: 38,43 pelas palavras do caso, sem reforço | sim |
| `entidade-produto` | posição 2, pontuação 23,73: 20,73 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `colecao_no_lugar_de_objeto` | posição 3, pontuação 23,42: 20,42 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `limites-do-sistema` | posição 4, pontuação 21,08: 21,08 pelas palavras do caso, sem reforço |  |
| `tempo_de_resposta_excedido` | posição 5, pontuação 19,59: 18,59 pelas palavras do caso, mais 1,0 por status |  |
| `contagem_inconsistente` | posição 6, pontuação 18,24: 17,24 pelas palavras do caso, mais 1,0 por entidade |  |
| `modos-de-injecao` | posição 7, pontuação 17,93: 17,93 pelas palavras do caso, sem reforço |  |
| `corpo_nao_e_json` | posição 8, pontuação 17,56: 16,56 pelas palavras do caso, mais 1,0 por status |  |

## Decisão 3: a causa

Escolha: `resposta_truncada` (Resposta truncada); segunda: `corpo_nao_e_json`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `resposta_truncada` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `corpo_nao_e_json` (Corpo não é JSON), ficou com probabilidade 0,001 contra 0,999 da escolhida; verbetes entregues que a sustentam: `resposta_truncada` (observado).
- As outras 2 alternativas lidas na resposta somam probabilidade 0,001; as maiores: `corpo_vazio` (0,001) e `colecao_no_lugar_de_objeto` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,999, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `esperado JSON completo e válido, recebido corpo truncado` (observado).
- A linha FONTE cita `colecao_no_lugar_de_objeto` e `resposta_truncada` (declarado).
- Os 2 verbetes citados (`colecao_no_lugar_de_objeto` e `resposta_truncada`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `colecao_no_lugar_de_objeto` não confere; `resposta_truncada` confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `resposta_truncada` (conferido).
- Camada de leitura de cada verbete citado: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/colecao_no_lugar_de_objeto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/colecao_no_lugar_de_objeto.md`); `resposta_truncada` (Resposta truncada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/resposta_truncada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/resposta_truncada.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 9 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `resposta_truncada` | 0,999 | `resposta_truncada` | sim |
| `corpo_nao_e_json` | 0,001 | `resposta_truncada` |  |
| `corpo_vazio` | 0,001 | `resposta_truncada` |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `colecao_no_lugar_de_objeto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A resposta foi cortada, resultando em uma interface que exibe 144 linhas a menos e 1 linha a mais que a referência, pois não carregou os dados do produto corretamente.
> FONTE: [colecao_no_lugar_de_objeto] [resposta_truncada]

Resposta inteira:

```text
CAUSA_RAIZ: resposta_truncada
CAMPO: nenhum
IMPACTO: A resposta foi cortada, resultando em uma interface que exibe 144 linhas a menos e 1 linha a mais que a referência, pois não carregou os dados do produto corretamente.
FONTE: [colecao_no_lugar_de_objeto] [resposta_truncada]
```

## Rastro

Gerado dos eventos 1298 a 1330 da trilha; hash dos eventos deste caso: `91bc9a91182eb16e` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-16@tela.md`.
