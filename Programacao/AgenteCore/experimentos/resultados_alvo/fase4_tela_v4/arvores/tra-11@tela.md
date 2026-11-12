<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-11`

Caso `tra-11` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/tra-11@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 29 afirmações (21 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (39 linhas) e a diferença do corpo da resposta (277 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 1928 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 183 nós a 39 linhas (observado).
- O que saiu, pelas regras em código: 10 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 15 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `1 linha(s) da referência`, recebido `1 linha(s) novas` (observado).
- A poda do corpo da resposta levou 1928 caracteres a 277 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, a primeira no campo `itens` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3922 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 1 linha(s) da referência | 1 linha(s) novas |
| campo itens | 14 itens (referência em modo normal) | falta o id 14 ("Abacaxi na Brasa") |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 183 nós |  |
| a árvore podada | 39 linhas | sim |
| o corpo da resposta inteiro | 1928 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 277 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (85,88), `contagem_inconsistente` (63,35) e `contrato-produto` (55,61) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contagem_inconsistente` e `contrato-produto`; o da entidade, em `entidade-produto`, `contagem_inconsistente` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estrutura_aninhada_divergente` (42,06), `colecao_no_lugar_de_objeto` (33,70), `tipo_divergente` (32,26), `pagina-produtos-api` (29,66) e `campo_ausente` (28,43) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 99 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `estrutura_aninhada_divergente`, só o texto do caso já punha o primeiro à frente (52,61 contra 39,06), e os reforços em código levaram a diferença a 13,55 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 85,88: 82,88 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contagem_inconsistente` | posição 2, pontuação 63,35: 60,35 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 55,61: 52,61 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 4, pontuação 42,06: 39,06 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 5, pontuação 33,70: 30,70 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tipo_divergente` | posição 6, pontuação 32,26: 29,26 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `pagina-produtos-api` | posição 7, pontuação 29,66: 27,66 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_ausente` | posição 8, pontuação 28,43: 25,43 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `contagem_inconsistente` (Contagem inconsistente); segunda: `resposta_truncada`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `contagem_inconsistente` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `resposta_truncada` (Resposta truncada), ficou com probabilidade 0,204 contra 0,777 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 6 alternativas lidas na resposta somam probabilidade 0,014; as maiores: `colecao_no_lugar_de_objeto` (0,013), `corpo_nao_e_json` (0,001) e `corpo_vazio` (0,001) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,777, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `itens: esperado 14 itens (referência em modo normal), recebido falta o id 14 ("Abacaxi na Brasa")` (observado).
- A linha FONTE cita `contagem_inconsistente` (declarado).
- Verbete citado `contagem_inconsistente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contagem_inconsistente` (conferido).
- Leitura do verbete `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `contagem_inconsistente` | 0,777 | `contagem_inconsistente` | sim |
| `resposta_truncada` | 0,204 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,013 | `contrato-produto` |  |
| `corpo_nao_e_json` | 0,001 | nenhum |  |
| `corpo_vazio` | 0,001 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,000 | `contagem_inconsistente` |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê uma lista com um item a menos do que esperado, resultando em uma exibição incompleta dos produtos.
> FONTE: [contagem_inconsistente]

Resposta inteira:

```text
CAUSA_RAIZ: contagem_inconsistente
CAMPO: nenhum
IMPACTO: O usuário vê uma lista com um item a menos do que esperado, resultando em uma exibição incompleta dos produtos.
FONTE: [contagem_inconsistente]
```

## Rastro

Gerado dos eventos 1190 a 1218 da trilha; hash dos eventos deste caso: `21e9fd0adc64fbd8` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-11@tela.md`.
