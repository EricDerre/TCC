<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-4`

Caso `sin-4` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/sin-4@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 30 afirmações (21 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (41 linhas) e a diferença do corpo da resposta (174 caracteres), não a página inteira.

- A página fez 2 chamadas à API: `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 2068 caracteres de corpo) e `GET /api/produtos/1` (status 200, 163 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 197 nós a 41 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 9 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `2 linha(s) da referência`, recebido `1 linha(s) novas` (observado).
- A poda do corpo da resposta levou 163 caracteres a 174 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, no corpo inteiro (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3953 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 2 linha(s) da referência | 1 linha(s) novas |
| corpo inteiro | objeto | lista |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 197 nós |  |
| a árvore podada | 41 linhas | sim |
| o corpo da resposta inteiro | 163 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 174 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (44,55), `colecao_no_lugar_de_objeto` (34,99) e `contrato-produto` (33,15) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `colecao_no_lugar_de_objeto` e `contrato-produto`; o da entidade, em `entidade-produto`, `colecao_no_lugar_de_objeto` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estado_da_tela_divergente` (27,39), `estrutura_aninhada_divergente` (25,57), `tipo_divergente` (18,61), `valor_fora_do_dominio` (18,32) e `pagina-produtos-api` (17,37) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 48 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `estado_da_tela_divergente`, só o texto do caso já punha o primeiro à frente (30,15 contra 27,39), e os reforços em código levaram a diferença a 5,76 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 44,55: 41,55 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `colecao_no_lugar_de_objeto` | posição 2, pontuação 34,99: 31,99 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 33,15: 30,15 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estado_da_tela_divergente` | posição 4, pontuação 27,39: 27,39 pelas palavras do caso, sem reforço |  |
| `estrutura_aninhada_divergente` | posição 5, pontuação 25,57: 24,57 pelas palavras do caso, mais 1,0 por entidade |  |
| `tipo_divergente` | posição 6, pontuação 18,61: 17,61 pelas palavras do caso, mais 1,0 por entidade |  |
| `valor_fora_do_dominio` | posição 7, pontuação 18,32: 18,32 pelas palavras do caso, sem reforço |  |
| `pagina-produtos-api` | posição 8, pontuação 17,37: 15,37 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)); segunda: `resposta_truncada`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `colecao_no_lugar_de_objeto` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `resposta_truncada` (Resposta truncada), ficou com probabilidade 0,001 contra 0,998 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 6 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `corpo_nao_e_json` (0,000), `corpo_vazio` (0,000) e `estrutura_aninhada_divergente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,998, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `esperado objeto, recebido lista` (observado).
- A linha FONTE cita `colecao_no_lugar_de_objeto` (declarado).
- Verbete citado `colecao_no_lugar_de_objeto`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `colecao_no_lugar_de_objeto` e `contrato-produto` (conferido).
- Leitura do verbete `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/colecao_no_lugar_de_objeto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/colecao_no_lugar_de_objeto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 11 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `colecao_no_lugar_de_objeto` | 0,998 | `colecao_no_lugar_de_objeto` e `contrato-produto` | sim |
| `resposta_truncada` | 0,001 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,000 | `colecao_no_lugar_de_objeto` |  |
| `campo_ausente` | 0,000 | `colecao_no_lugar_de_objeto` e `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `tipo_divergente` | 0,000 | `entidade-produto` e `contrato-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A tela exibe uma lista incompleta de produtos, mostrando 2 linhas a menos e 2 a mais que a referência.
> FONTE: [colecao_no_lugar_de_objeto]

Resposta inteira:

```text
CAUSA_RAIZ: colecao_no_lugar_de_objeto
CAMPO: id
IMPACTO: A tela exibe uma lista incompleta de produtos, mostrando 2 linhas a menos e 2 a mais que a referência.
FONTE: [colecao_no_lugar_de_objeto]
```

## Rastro

Gerado dos eventos 131 a 169 da trilha; hash dos eventos deste caso: `37c4b3c7c46d2fdd` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-4@tela.md`.
