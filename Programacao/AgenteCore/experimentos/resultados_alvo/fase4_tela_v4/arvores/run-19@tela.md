<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `run-19`

Caso `run-19` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/run-19@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 29 afirmações (21 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (42 linhas) e a diferença do corpo da resposta (174 caracteres), não a página inteira.

- A página fez 2 chamadas à API: `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 2068 caracteres de corpo) e `GET /api/produtos/1` (status 200, 161 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 197 nós a 42 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 9 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `0 linha(s) da referência`, recebido `0 linha(s) novas` (observado).
- A poda do corpo da resposta levou 161 caracteres a 174 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, a primeira no campo `tempo_ms` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3539 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 0 linha(s) da referência | 0 linha(s) novas |
| campo tempo_ms | 16 ms (referência em modo normal) | 2012 ms |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 197 nós |  |
| a árvore podada | 42 linhas | sim |
| o corpo da resposta inteiro | 161 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 174 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `tempo_de_resposta_excedido` (47,81), `entidade-produto` (42,90) e `contrato-produto` (25,42) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; o do status, em `tempo_de_resposta_excedido` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estado_da_tela_divergente` (21,42), `tipo_divergente` (17,89), `pagina-produtos-api` (17,48), `valor_fora_do_dominio` (17,44) e `estrutura_aninhada_divergente` (15,66) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 53 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `estado_da_tela_divergente`, só o texto do caso já punha o primeiro à frente (22,42 contra 21,42), e os reforços em código levaram a diferença a 4,01 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `tempo_de_resposta_excedido` | posição 1, pontuação 47,81: 46,81 pelas palavras do caso, mais 1,0 por status | sim |
| `entidade-produto` | posição 2, pontuação 42,90: 39,90 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 25,42: 22,42 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estado_da_tela_divergente` | posição 4, pontuação 21,42: 21,42 pelas palavras do caso, sem reforço |  |
| `tipo_divergente` | posição 5, pontuação 17,89: 16,89 pelas palavras do caso, mais 1,0 por entidade |  |
| `pagina-produtos-api` | posição 6, pontuação 17,48: 15,48 pelas palavras do caso, mais 2,0 por rota |  |
| `valor_fora_do_dominio` | posição 7, pontuação 17,44: 17,44 pelas palavras do caso, sem reforço |  |
| `estrutura_aninhada_divergente` | posição 8, pontuação 15,66: 14,66 pelas palavras do caso, mais 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `tempo_de_resposta_excedido` (Tempo de resposta excedido); segunda: `tipo_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `tempo_de_resposta_excedido` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,018 contra 0,981 da escolhida; verbetes entregues que a sustentam: `entidade-produto` e `contrato-produto` (observado).
- As outras 6 alternativas lidas na resposta somam probabilidade 0,001; as maiores: `campo_ausente` (0,000), `campo_renomeado` (0,000) e `formato_de_data_divergente` (0,000) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,981, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `tempo_ms: esperado 16 ms (referência em modo normal), recebido 2012 ms` (observado).
- A linha FONTE cita `tempo_de_resposta_excedido` (declarado).
- Verbete citado `tempo_de_resposta_excedido`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `tempo_de_resposta_excedido` (conferido).
- Leitura do verbete `tempo_de_resposta_excedido` (Tempo de resposta excedido; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tempo_de_resposta_excedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tempo_de_resposta_excedido.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 10 de 10 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `tempo_de_resposta_excedido` | 0,981 | `tempo_de_resposta_excedido` | sim |
| `tipo_divergente` | 0,018 | `entidade-produto` e `contrato-produto` |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `resposta_truncada` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário experimentou uma resposta lenta, o que pode causar insatisfação e atrasos na experiência do usuário.
> FONTE: [tempo_de_resposta_excedido]

Resposta inteira:

```text
CAUSA_RAIZ: tempo_de_resposta_excedido
CAMPO: nenhum
IMPACTO: O usuário experimentou uma resposta lenta, o que pode causar insatisfação e atrasos na experiência do usuário.
FONTE: [tempo_de_resposta_excedido]
```

## Rastro

Gerado dos eventos 2078 a 2113 da trilha; hash dos eventos deste caso: `88c02123b0ed6352` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/run-19@tela.md`.
