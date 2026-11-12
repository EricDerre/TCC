<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-16`

Caso `sin-16` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/sin-16@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 30 afirmações (21 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (42 linhas) e a diferença do corpo da resposta (25 caracteres), não a página inteira.

- A página fez 2 chamadas à API: `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 1835 caracteres de corpo) e `GET /api/produtos/1` (status 200, 145 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 197 nós a 42 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 9 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `3 linha(s) da referência`, recebido `3 linha(s) novas` (observado).
- A poda do corpo da resposta levou 145 caracteres a 25 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, a primeira no campo `destaque` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3485 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 3 linha(s) da referência | 3 linha(s) novas |
| campo destaque | booleano | ausente |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 197 nós |  |
| a árvore podada | 42 linhas | sim |
| o corpo da resposta inteiro | 145 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 25 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (51,38), `contrato-produto` (38,84) e `campo_ausente` (27,47) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto`, `contrato-produto` e `campo_ausente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `tipo_divergente` (24,13), `valor_fora_do_dominio` (18,96), `colecao_no_lugar_de_objeto` (18,86), `modos-de-injecao` (18,14) e `campo_renomeado` (17,69) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 41 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `campo_ausente`, e o primeiro de fora, `tipo_divergente`, só o texto do caso já punha o primeiro à frente (26,47 contra 23,13), e os reforços em código levaram a diferença a 3,34 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 51,38: 48,38 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 38,84: 35,84 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_ausente` | posição 3, pontuação 27,47: 26,47 pelas palavras do caso, mais 1,0 por entidade | sim |
| `tipo_divergente` | posição 4, pontuação 24,13: 23,13 pelas palavras do caso, mais 1,0 por entidade |  |
| `valor_fora_do_dominio` | posição 5, pontuação 18,96: 18,96 pelas palavras do caso, sem reforço |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 18,86: 15,86 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `modos-de-injecao` | posição 7, pontuação 18,14: 18,14 pelas palavras do caso, sem reforço |  |
| `campo_renomeado` | posição 8, pontuação 17,69: 16,69 pelas palavras do caso, mais 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `campo_ausente` (Campo ausente); segunda: `campo_renomeado`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `campo_ausente` (declarado).
- O modelo apontou o campo `destaque` (declarado).
- `destaque` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_renomeado` (Campo renomeado), ficou com probabilidade 0,000 contra 0,992 da escolhida; verbetes entregues que a sustentam: `contrato-produto` e `campo_ausente` (observado).
- As outras 4 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `corpo_nao_e_json` (0,000), `corpo_vazio` (0,000) e `tipo_divergente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,992, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `destaque: esperado booleano, recebido None` (observado).
- A linha FONTE cita `campo_ausente` (declarado).
- Verbete citado `campo_ausente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-produto` e `campo_ausente` (conferido).
- Leitura do verbete `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 11 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `campo_ausente` | 0,992 | `contrato-produto` e `campo_ausente` | sim |
| `campo_renomeado` | 0,000 | `contrato-produto` e `campo_ausente` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `tipo_divergente` | 0,000 | `entidade-produto` e `contrato-produto` |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O campo destaque não foi incluído na resposta, resultando em uma exibição incompleta da página com 14 linhas a menos.
> FONTE: [campo_ausente]

Resposta inteira:

```text
CAUSA_RAIZ: campo_ausente
CAMPO: destaque
IMPACTO: O campo destaque não foi incluído na resposta, resultando em uma exibição incompleta da página com 14 linhas a menos.
FONTE: [campo_ausente]
```

## Rastro

Gerado dos eventos 1414 a 1453 da trilha; hash dos eventos deste caso: `9c6de28ef5afb3cf` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-16@tela.md`.
