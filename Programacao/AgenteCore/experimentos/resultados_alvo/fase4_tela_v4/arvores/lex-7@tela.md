<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-7`

Caso `lex-7` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/lex-7@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 29 afirmações (21 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (21 linhas) e a diferença do corpo da resposta (0 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 0 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 54 nós a 21 linhas (observado).
- O que saiu, pelas regras em código: 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 2 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `25 linha(s) da referência`, recebido `4 linha(s) novas` (observado).
- A poda do corpo da resposta levou 0 caracteres a 0 caracteres: só a diferença contra o contrato esperado pela interface vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, no corpo inteiro (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3889 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 25 linha(s) da referência | 4 linha(s) novas |
| corpo inteiro | JSON completo e válido | corpo vazio |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 54 nós |  |
| a árvore podada | 21 linhas | sim |
| o corpo da resposta inteiro | 0 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface | 0 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `corpo_vazio` (20,25), `colecao_no_lugar_de_objeto` (19,00) e `tempo_de_resposta_excedido` (13,93) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `colecao_no_lugar_de_objeto`; o da entidade, em `colecao_no_lugar_de_objeto`; o do status, em `tempo_de_resposta_excedido`; `corpo_vazio` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `contagem_inconsistente` (13,45), `ancora-saiba-mais` (11,30), `corpo_nao_e_json` (10,55), `limites-do-sistema` (10,36) e `entidade-produto` (10,33) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 30 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `tempo_de_resposta_excedido`, e o primeiro de fora, `contagem_inconsistente`, só o texto do caso já punha o primeiro à frente (12,93 contra 12,45), e os reforços em código levaram a diferença a 0,48 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `corpo_vazio` | posição 1, pontuação 20,25: 20,25 pelas palavras do caso, sem reforço | sim |
| `colecao_no_lugar_de_objeto` | posição 2, pontuação 19,00: 16,00 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tempo_de_resposta_excedido` | posição 3, pontuação 13,93: 12,93 pelas palavras do caso, mais 1,0 por status | sim |
| `contagem_inconsistente` | posição 4, pontuação 13,45: 12,45 pelas palavras do caso, mais 1,0 por entidade |  |
| `ancora-saiba-mais` | posição 5, pontuação 11,30: 11,30 pelas palavras do caso, sem reforço |  |
| `corpo_nao_e_json` | posição 6, pontuação 10,55: 9,55 pelas palavras do caso, mais 1,0 por status |  |
| `limites-do-sistema` | posição 7, pontuação 10,36: 10,36 pelas palavras do caso, sem reforço |  |
| `entidade-produto` | posição 8, pontuação 10,33: 7,33 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `corpo_vazio` (Corpo vazio); segunda: `corpo_nao_e_json`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `corpo_vazio` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `corpo_nao_e_json` (Corpo não é JSON), ficou com probabilidade 0,000 contra 0,996 da escolhida; verbetes entregues que a sustentam: `corpo_vazio` (observado).
- As outras 2 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `resposta_truncada` (0,000) e `colecao_no_lugar_de_objeto` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,996, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `esperado JSON completo e válido, recebido corpo vazio` (observado).
- A linha FONTE cita `corpo_vazio` (declarado).
- Verbete citado `corpo_vazio`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `corpo_vazio` e `tempo_de_resposta_excedido` (conferido).
- Leitura do verbete `corpo_vazio` (Corpo vazio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/corpo_vazio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/corpo_vazio.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `corpo_vazio` | 0,996 | `corpo_vazio` e `tempo_de_resposta_excedido` | sim |
| `corpo_nao_e_json` | 0,000 | `corpo_vazio` |  |
| `resposta_truncada` | 0,000 | `corpo_vazio` |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `colecao_no_lugar_de_objeto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A tela exibe uma mensagem de erro indicando que os produtos não foram carregados corretamente, e o usuário não vê nenhum produto listado, embora a interface esperasse exibir detalhes de um produto específico.
> FONTE: [corpo_vazio]

Resposta inteira:

```text
CAUSA_RAIZ: corpo_vazio
CAMPO: nenhum
IMPACTO: A tela exibe uma mensagem de erro indicando que os produtos não foram carregados corretamente, e o usuário não vê nenhum produto listado, embora a interface esperasse exibir detalhes de um produto específico.
FONTE: [corpo_vazio]
```

## Rastro

Gerado dos eventos 610 a 640 da trilha; hash dos eventos deste caso: `294c44637689d499` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-7@tela.md`.
