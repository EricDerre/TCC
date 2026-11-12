<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-21`

Caso `sin-21` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/sin-21@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 30 afirmações (21 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (39 linhas) e a diferença do corpo da resposta (45 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 2404 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 193 nós a 39 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `3 linha(s) da referência`, recebido `3 linha(s) novas` (observado).
- A poda do corpo da resposta levou 2404 caracteres a 45 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 2 diferenças, a primeira no campo `tipo` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3992 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 3 linha(s) da referência | 3 linha(s) novas |
| campo tipo | texto | objeto |
| campo tipo | "Carnes" (referência em modo normal) | {"valor": "Carnes", "moeda": "BRL"} em 14 itens |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 193 nós |  |
| a árvore podada | 39 linhas | sim |
| o corpo da resposta inteiro | 2404 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 45 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `estrutura_aninhada_divergente` (174,99), `contrato-produto` (154,14) e `colecao_no_lugar_de_objeto` (129,37) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `estrutura_aninhada_divergente`, `contrato-produto` e `colecao_no_lugar_de_objeto`; o da entidade, em `estrutura_aninhada_divergente`, `contrato-produto` e `colecao_no_lugar_de_objeto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `entidade-produto` (94,03), `pagina-produtos-api` (77,60), `campo_renomeado` (68,23), `tipo_divergente` (59,85) e `nulo_inesperado` (55,68) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 122 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `colecao_no_lugar_de_objeto`, e o primeiro de fora, `entidade-produto`, só o texto do caso já punha o primeiro à frente (126,37 contra 91,03), e os reforços em código levaram a diferença a 35,34 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `estrutura_aninhada_divergente` | posição 1, pontuação 174,99: 171,99 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 154,14: 151,14 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `colecao_no_lugar_de_objeto` | posição 3, pontuação 129,37: 126,37 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 4, pontuação 94,03: 91,03 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `pagina-produtos-api` | posição 5, pontuação 77,60: 75,60 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_renomeado` | posição 6, pontuação 68,23: 65,23 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tipo_divergente` | posição 7, pontuação 59,85: 56,85 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 8, pontuação 55,68: 53,68 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `estrutura_aninhada_divergente` (Estrutura aninhada divergente); segunda: `tipo_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `estrutura_aninhada_divergente` (declarado).
- O modelo apontou o campo `tipo` (declarado).
- `tipo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 0,993 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 4 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `campo_renomeado` (0,000) e `escala_ou_unidade_errada` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,993, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `tipo: esperado texto, recebido objeto` (observado).
- A linha FONTE cita `estrutura_aninhada_divergente` e `contrato-produto` (declarado).
- Os 2 verbetes citados (`estrutura_aninhada_divergente` e `contrato-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `estrutura_aninhada_divergente` confere; `contrato-produto` não confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `estrutura_aninhada_divergente` e `colecao_no_lugar_de_objeto` (conferido).
- Camada de leitura de cada verbete citado: `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 13 de 14 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `estrutura_aninhada_divergente` | 0,993 | `estrutura_aninhada_divergente` e `colecao_no_lugar_de_objeto` | sim |
| `tipo_divergente` | 0,000 | `contrato-produto` |  |
| `campo_ausente` | 0,000 | `contrato-produto` e `colecao_no_lugar_de_objeto` |  |
| `campo_renomeado` | 0,000 | `estrutura_aninhada_divergente` e `contrato-produto` |  |
| `escala_ou_unidade_errada` | 0,000 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um campo "tipo" como um objeto em vez de um texto, causando confusão na exibição dos produtos.
> FONTE: [estrutura_aninhada_divergente] [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: estrutura_aninhada_divergente
CAMPO: tipo
IMPACTO: O usuário vê um campo "tipo" como um objeto em vez de um texto, causando confusão na exibição dos produtos.
FONTE: [estrutura_aninhada_divergente] [contrato-produto]
```

## Rastro

Gerado dos eventos 1542 a 1581 da trilha; hash dos eventos deste caso: `445a923a513bd676` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-21@tela.md`.
