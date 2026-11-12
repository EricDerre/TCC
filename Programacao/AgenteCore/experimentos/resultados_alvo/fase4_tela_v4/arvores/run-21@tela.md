<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `run-21`

Caso `run-21` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/run-21@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 29 afirmações (21 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (39 linhas) e a diferença do corpo da resposta (301 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 2230 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 203 nós a 39 linhas (observado).
- O que saiu, pelas regras em código: 12 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 17 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `6 linha(s) da referência`, recebido `6 linha(s) novas` (observado).
- A poda do corpo da resposta levou 2230 caracteres a 301 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, a primeira no campo `itens` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3773 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 6 linha(s) da referência | 6 linha(s) novas |
| campo itens | 14 itens (referência em modo normal) | o id 1 ("Picanha ao Alho") aparece 2 vezes |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 203 nós |  |
| a árvore podada | 39 linhas | sim |
| o corpo da resposta inteiro | 2230 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 301 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (107,54), `contrato-produto` (56,20) e `registro_duplicado` (47,02) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; `registro_duplicado` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `contagem_inconsistente` (39,92), `estrutura_aninhada_divergente` (39,31), `tipo_divergente` (34,67), `colecao_no_lugar_de_objeto` (32,93) e `valor_fora_do_dominio` (29,26) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 104 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `registro_duplicado`, e o primeiro de fora, `contagem_inconsistente`, só o texto do caso já punha o primeiro à frente (47,02 contra 36,92); a diferença final foi 7,09 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 107,54: 104,54 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 56,20: 53,20 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `registro_duplicado` | posição 3, pontuação 47,02: 47,02 pelas palavras do caso, sem reforço | sim |
| `contagem_inconsistente` | posição 4, pontuação 39,92: 36,92 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 5, pontuação 39,31: 36,31 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tipo_divergente` | posição 6, pontuação 34,67: 31,67 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 7, pontuação 32,93: 29,93 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `valor_fora_do_dominio` | posição 8, pontuação 29,26: 27,26 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `registro_duplicado` (Registro duplicado); segunda: `campo_ausente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `registro_duplicado` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,000 contra 0,999 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 2 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_renomeado` (0,000) e `valor_fora_do_dominio` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,999, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `itens: esperado 14 itens (referência em modo normal), recebido o id 1 ("Picanha ao Alho") aparece 2 vezes` (observado).
- A linha FONTE cita `registro_duplicado` (declarado).
- Verbete citado `registro_duplicado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `registro_duplicado` (conferido).
- Leitura do verbete `registro_duplicado` (Registro duplicado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/registro_duplicado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/registro_duplicado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `registro_duplicado` | 0,999 | `registro_duplicado` | sim |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A interface exibe 10 cartões a mais, com a Picanha ao Alho duplicada, causando confusão no usuário.
> FONTE: [registro_duplicado]

Resposta inteira:

```text
CAUSA_RAIZ: registro_duplicado
CAMPO: nenhum
IMPACTO: A interface exibe 10 cartões a mais, com a Picanha ao Alho duplicada, causando confusão no usuário.
FONTE: [registro_duplicado]
```

## Rastro

Gerado dos eventos 2138 a 2169 da trilha; hash dos eventos deste caso: `137e9d93f8b047b9` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/run-21@tela.md`.
