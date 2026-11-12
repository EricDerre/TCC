<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `contrato-field_missing#1`

Caso `contrato-field_missing#1` da corrida `fase4_ensaio_v4`, trilha `fase4_ensaio_v4/qwen2.5_7b/contrato-field_missing#1`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 30 afirmações (21 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (39 linhas) e a diferença do corpo da resposta (22 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 1888 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 193 nós a 39 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `3 linha(s) da referência`, recebido `3 linha(s) novas` (observado).
- A poda do corpo da resposta levou 1888 caracteres a 22 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, a primeira no campo `preco` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3570 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 3 linha(s) da referência | 3 linha(s) novas |
| campo preco | numero | ausente |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 193 nós |  |
| a árvore podada | 39 linhas | sim |
| o corpo da resposta inteiro | 1888 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 22 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `campo_ausente` (149,55), `entidade-produto` (127,86) e `contrato-produto` (122,48) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `campo_ausente`, `entidade-produto` e `contrato-produto`; o da entidade, em `campo_ausente`, `entidade-produto` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `campo_preco_ausente` (113,10), `campo_renomeado` (85,14), `nulo_inesperado` (59,34), `localizador_quebrado` (40,52) e `pagina-produtos-api` (40,41) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 121 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `campo_preco_ausente`, só o texto do caso já punha o primeiro à frente (119,48 contra 112,10), e os reforços em código levaram a diferença a 9,39 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `campo_ausente` | posição 1, pontuação 149,55: 146,55 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 2, pontuação 127,86: 124,86 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 122,48: 119,48 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_preco_ausente` | posição 4, pontuação 113,10: 112,10 pelas palavras do caso, mais 1,0 por entidade |  |
| `campo_renomeado` | posição 5, pontuação 85,14: 82,14 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 6, pontuação 59,34: 57,34 pelas palavras do caso, mais 2,0 por rota |  |
| `localizador_quebrado` | posição 7, pontuação 40,52: 40,52 pelas palavras do caso, sem reforço |  |
| `pagina-produtos-api` | posição 8, pontuação 40,41: 38,41 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `campo_ausente` (Campo ausente); segunda: `resposta_truncada`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `campo_ausente` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `resposta_truncada` (Resposta truncada), ficou com probabilidade 0,000 contra 0,994 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 4 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `tipo_divergente` (0,000), `corpo_nao_e_json` (0,000) e `corpo_vazio` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,994, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `preco: esperado numero, recebido None` (observado).
- A linha FONTE cita `campo_ausente` e `contrato-produto` (declarado).
- Os 2 verbetes citados (`campo_ausente` e `contrato-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `campo_ausente` confere; `contrato-produto` não confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `campo_ausente` e `contrato-produto` (conferido).
- Camada de leitura de cada verbete citado: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 11 de 13 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `campo_ausente` | 0,994 | `campo_ausente` e `contrato-produto` | sim |
| `resposta_truncada` | 0,000 | nenhum |  |
| `tipo_divergente` | 0,000 | `entidade-produto` e `contrato-produto` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `campo_renomeado` | 0,000 | `campo_ausente` e `contrato-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário não vê o preço dos produtos, resultando em uma interface incompleta e potencialmente confusa.
> FONTE: [campo_ausente] [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: campo_ausente
CAMPO: preco
IMPACTO: O usuário não vê o preço dos produtos, resultando em uma interface incompleta e potencialmente confusa.
FONTE: [campo_ausente] [contrato-produto]
```

## Rastro

Gerado dos eventos 40 a 77 da trilha; hash dos eventos deste caso: `f59a32bccdd4744d` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/contrato-field_missing__r1.md`.
