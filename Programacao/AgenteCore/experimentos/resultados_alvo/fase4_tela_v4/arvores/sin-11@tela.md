<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-11`

Caso `sin-11` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/sin-11@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 30 afirmações (21 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (39 linhas) e a diferença do corpo da resposta (42 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 2404 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 193 nós a 39 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `3 linha(s) da referência`, recebido `3 linha(s) novas` (observado).
- A poda do corpo da resposta levou 2404 caracteres a 42 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 2 diferenças, a primeira no campo `preco` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3834 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 3 linha(s) da referência | 3 linha(s) novas |
| campo preco | numero | objeto |
| campo preco | 89.9 (referência em modo normal) | {"valor": 89.9, "moeda": "BRL"} em 14 itens |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 193 nós |  |
| a árvore podada | 39 linhas | sim |
| o corpo da resposta inteiro | 2404 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 42 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-produto` (175,26), `estrutura_aninhada_divergente` (171,27) e `entidade-produto` (127,13) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto`, `estrutura_aninhada_divergente` e `entidade-produto`; o da entidade, em `contrato-produto`, `estrutura_aninhada_divergente` e `entidade-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `colecao_no_lugar_de_objeto` (116,99), `pagina-produtos-api` (94,04), `campo_renomeado` (85,31), `campo_ausente` (81,83) e `nulo_inesperado` (67,07) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 140 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `colecao_no_lugar_de_objeto`, só o texto do caso já punha o primeiro à frente (124,13 contra 113,99), e os reforços em código levaram a diferença a 10,15 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-produto` | posição 1, pontuação 175,26: 172,26 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 2, pontuação 171,27: 168,27 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 3, pontuação 127,13: 124,13 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `colecao_no_lugar_de_objeto` | posição 4, pontuação 116,99: 113,99 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `pagina-produtos-api` | posição 5, pontuação 94,04: 92,04 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_renomeado` | posição 6, pontuação 85,31: 82,31 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_ausente` | posição 7, pontuação 81,83: 78,83 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 8, pontuação 67,07: 65,07 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `estrutura_aninhada_divergente` (Estrutura aninhada divergente); segunda: `campo_ausente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `estrutura_aninhada_divergente` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,004 contra 0,957 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,006; as maiores: `campo_renomeado` (0,004), `tipo_divergente` (0,002) e `corpo_nao_e_json` (0,000) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,957, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `preco: esperado numero, recebido objeto` (observado).
- A linha FONTE cita `estrutura_aninhada_divergente` (declarado).
- Verbete citado `estrutura_aninhada_divergente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `estrutura_aninhada_divergente` (conferido).
- Leitura do verbete `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 9 de 10 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `estrutura_aninhada_divergente` | 0,957 | `estrutura_aninhada_divergente` | sim |
| `campo_ausente` | 0,004 | `contrato-produto` |  |
| `campo_renomeado` | 0,004 | `contrato-produto` e `estrutura_aninhada_divergente` |  |
| `tipo_divergente` | 0,002 | `contrato-produto` e `entidade-produto` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` e `estrutura_aninhada_divergente` |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A interface exibe um preço em formato inválido, causando confusão para o usuário.
> FONTE: [estrutura_aninhada_divergente]

Resposta inteira:

```text
CAUSA_RAIZ: estrutura_aninhada_divergente
CAMPO: preco
IMPACTO: A interface exibe um preço em formato inválido, causando confusão para o usuário.
FONTE: [estrutura_aninhada_divergente]
```

## Rastro

Gerado dos eventos 838 a 871 da trilha; hash dos eventos deste caso: `9ba1c6113c6f4614` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-11@tela.md`.
