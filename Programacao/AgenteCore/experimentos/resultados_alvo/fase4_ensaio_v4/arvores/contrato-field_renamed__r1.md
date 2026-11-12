<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `contrato-field_renamed#1`

Caso `contrato-field_renamed#1` da corrida `fase4_ensaio_v4`, trilha `fase4_ensaio_v4/qwen2.5_7b/contrato-field_renamed#1`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 30 afirmações (21 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (39 linhas) e a diferença do corpo da resposta (18 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 2110 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 193 nós a 39 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `3 linha(s) da referência`, recebido `3 linha(s) novas` (observado).
- A poda do corpo da resposta levou 2110 caracteres a 18 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, a primeira no campo `preco` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3650 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 3 linha(s) da referência | 3 linha(s) novas |
| campo preco | preco | preco_v2 |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 193 nós |  |
| a árvore podada | 39 linhas | sim |
| o corpo da resposta inteiro | 2110 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 18 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `campo_renomeado` (212,84), `campo_ausente` (183,81) e `contrato-produto` (143,96) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `campo_renomeado`, `campo_ausente` e `contrato-produto`; o da entidade, em `campo_renomeado`, `campo_ausente` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `entidade-produto` (120,68), `campo_preco_ausente` (113,10), `nulo_inesperado` (86,36), `chave_de_juncao_errada` (53,57) e `tipo_divergente` (48,83) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 177 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `entidade-produto`, só o texto do caso já punha o primeiro à frente (140,96 contra 117,68), e os reforços em código levaram a diferença a 23,28 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `campo_renomeado` | posição 1, pontuação 212,84: 209,84 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_ausente` | posição 2, pontuação 183,81: 180,81 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 143,96: 140,96 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 4, pontuação 120,68: 117,68 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_preco_ausente` | posição 5, pontuação 113,10: 112,10 pelas palavras do caso, mais 1,0 por entidade |  |
| `nulo_inesperado` | posição 6, pontuação 86,36: 84,36 pelas palavras do caso, mais 2,0 por rota |  |
| `chave_de_juncao_errada` | posição 7, pontuação 53,57: 51,57 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 8, pontuação 48,83: 45,83 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `campo_renomeado` (Campo renomeado); segunda: `tipo_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `campo_renomeado` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 0,998 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 3 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `corpo_nao_e_json` (0,000) e `corpo_vazio` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,998, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `preco: esperado preco, recebido preco_v2` (observado).
- A linha FONTE cita `campo_renomeado` (declarado).
- Verbete citado `campo_renomeado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `campo_renomeado`, `campo_ausente` e `contrato-produto` (conferido).
- Leitura do verbete `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 9 de 10 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `campo_renomeado` | 0,998 | `campo_renomeado`, `campo_ausente` e `contrato-produto` | sim |
| `tipo_divergente` | 0,000 | `contrato-produto` |  |
| `campo_ausente` | 0,000 | `campo_renomeado`, `campo_ausente` e `contrato-produto` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um preço incorreto, exibido como "undefined" em vez do valor esperado.
> FONTE: [campo_renomeado]

Resposta inteira:

```text
CAUSA_RAIZ: campo_renomeado
CAMPO: preco
IMPACTO: O usuário vê um preço incorreto, exibido como "undefined" em vez do valor esperado.
FONTE: [campo_renomeado]
```

## Rastro

Gerado dos eventos 79 a 111 da trilha; hash dos eventos deste caso: `30390002a6cb8f01` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/contrato-field_renamed__r1.md`.
