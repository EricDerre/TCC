<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `run-1`

Caso `run-1` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/run-1@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 29 afirmações (21 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (21 linhas) e a diferença do corpo da resposta (205 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 500 (a API falhou por erro interno), 50 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 54 nós a 21 linhas (observado).
- O que saiu, pelas regras em código: 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 2 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `22 linha(s) da referência`, recebido `4 linha(s) novas` (observado).
- A poda do corpo da resposta levou 50 caracteres a 205 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 9 diferenças, no corpo inteiro (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4228 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 22 linha(s) da referência | 4 linha(s) novas |
| corpo inteiro | lista | objeto |
| campo id | inteiro | ausente |
| campo nome | texto | ausente |
| campo resumo | texto\|nulo | ausente |
| campo tipo | texto | ausente |
| campo preco | numero | ausente |
| campo imagem | texto\|nulo | ausente |
| campo destaque | booleano | ausente |
| campo detail |  | texto |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 54 nós |  |
| a árvore podada | 21 linhas | sim |
| o corpo da resposta inteiro | 50 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 205 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `erro_interno_do_servidor` (44,14), `contagem_inconsistente` (37,93) e `contrato-produto` (35,88) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `erro_interno_do_servidor`, `contagem_inconsistente` e `contrato-produto`; o da entidade, em `contagem_inconsistente` e `contrato-produto`; o do status, em `erro_interno_do_servidor` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estrutura_aninhada_divergente` (34,38), `modos-de-injecao` (30,58), `mensagens-de-erro-do-codigo` (29,79), `entidade-produto` (27,86) e `colecao_no_lugar_de_objeto` (27,78) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 500 e 63 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `estrutura_aninhada_divergente`, só o texto do caso já punha o primeiro à frente (32,88 contra 31,38), e os reforços em código levaram a diferença a 1,51 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `erro_interno_do_servidor` | posição 1, pontuação 44,14: 41,14 pelas palavras do caso, mais 2,0 por rota e 1,0 por status | sim |
| `contagem_inconsistente` | posição 2, pontuação 37,93: 34,93 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 35,88: 32,88 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 4, pontuação 34,38: 31,38 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `modos-de-injecao` | posição 5, pontuação 30,58: 29,58 pelas palavras do caso, mais 1,0 por status |  |
| `mensagens-de-erro-do-codigo` | posição 6, pontuação 29,79: 28,79 pelas palavras do caso, mais 1,0 por status |  |
| `entidade-produto` | posição 7, pontuação 27,86: 24,86 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 8, pontuação 27,78: 24,78 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `erro_interno_do_servidor` (Erro interno do servidor (500)); segunda: `resposta_truncada`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `erro_interno_do_servidor` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `resposta_truncada` (Resposta truncada), ficou com probabilidade 0,000 contra 0,991 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 5 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `corpo_nao_e_json` (0,000), `corpo_vazio` (0,000) e `campo_ausente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,991, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `esperado lista, recebido objeto` (observado).
- A linha FONTE cita `erro_interno_do_servidor` e `contrato-produto` (declarado).
- Os 2 verbetes citados (`erro_interno_do_servidor` e `contrato-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `erro_interno_do_servidor` confere; `contrato-produto` não confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `erro_interno_do_servidor` (conferido).
- Camada de leitura de cada verbete citado: `erro_interno_do_servidor` (Erro interno do servidor (500); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/erro_interno_do_servidor.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/erro_interno_do_servidor.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 9 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `erro_interno_do_servidor` | 0,991 | `erro_interno_do_servidor` | sim |
| `resposta_truncada` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | `erro_interno_do_servidor` |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `tipo_divergente` | 0,000 | `contrato-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê uma página de erro sem detalhes, enquanto a interface esperava uma lista de produtos formatada corretamente.
> FONTE: [erro_interno_do_servidor] [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: erro_interno_do_servidor
CAMPO: nenhum
IMPACTO: O usuário vê uma página de erro sem detalhes, enquanto a interface esperava uma lista de produtos formatada corretamente.
FONTE: [erro_interno_do_servidor] [contrato-produto]
```

## Rastro

Gerado dos eventos 433 a 468 da trilha; hash dos eventos deste caso: `2d965b60e454e8cb` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/run-1@tela.md`.
