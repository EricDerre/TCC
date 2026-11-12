<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-20`

Caso `sin-20` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/sin-20@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 30 afirmações (21 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (39 linhas) e a diferença do corpo da resposta (19 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 1965 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 193 nós a 39 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `3 linha(s) da referência`, recebido `3 linha(s) novas` (observado).
- A poda do corpo da resposta levou 1965 caracteres a 19 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, a primeira no campo `id` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3425 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 3 linha(s) da referência | 3 linha(s) novas |
| campo id | inteiro | ausente |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 193 nós |  |
| a árvore podada | 39 linhas | sim |
| o corpo da resposta inteiro | 1965 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 19 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `campo_ausente` (132,80), `contrato-produto` (106,51) e `entidade-produto` (92,41) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `campo_ausente`, `contrato-produto` e `entidade-produto`; o da entidade, em `campo_ausente`, `contrato-produto` e `entidade-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `campo_preco_ausente` (73,35), `campo_renomeado` (57,44), `localizador_quebrado` (56,89), `colecao_no_lugar_de_objeto` (44,36) e `estrutura_aninhada_divergente` (42,28) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 97 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `campo_preco_ausente`, só o texto do caso já punha o primeiro à frente (89,41 contra 72,35), e os reforços em código levaram a diferença a 19,06 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `campo_ausente` | posição 1, pontuação 132,80: 129,80 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 106,51: 103,51 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 3, pontuação 92,41: 89,41 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_preco_ausente` | posição 4, pontuação 73,35: 72,35 pelas palavras do caso, mais 1,0 por entidade |  |
| `campo_renomeado` | posição 5, pontuação 57,44: 54,44 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `localizador_quebrado` | posição 6, pontuação 56,89: 56,89 pelas palavras do caso, sem reforço |  |
| `colecao_no_lugar_de_objeto` | posição 7, pontuação 44,36: 41,36 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 8, pontuação 42,28: 39,28 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `campo_ausente` (Campo ausente); segunda: `resposta_truncada`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `campo_ausente` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `resposta_truncada` (Resposta truncada), ficou com probabilidade 0,000 contra 0,986 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 3 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `corpo_nao_e_json` (0,000), `corpo_vazio` (0,000) e `campo_renomeado` (0,000) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,986, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `id: esperado inteiro, recebido None` (observado).
- A linha FONTE cita `campo_ausente` e `contrato-produto` (declarado).
- Os 2 verbetes citados (`campo_ausente` e `contrato-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `campo_ausente` confere; `contrato-produto` não confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `campo_ausente` e `contrato-produto` (conferido).
- Camada de leitura de cada verbete citado: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 13 de 14 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `campo_ausente` | 0,986 | `campo_ausente` e `contrato-produto` | sim |
| `resposta_truncada` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `campo_renomeado` | 0,000 | `campo_ausente` e `contrato-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um botão "Saiba Mais..." sem o identificador do produto, resultando em uma experiência interativa quebrada.
> FONTE: [campo_ausente] [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: campo_ausente
CAMPO: id
IMPACTO: O usuário vê um botão "Saiba Mais..." sem o identificador do produto, resultando em uma experiência interativa quebrada.
FONTE: [campo_ausente] [contrato-produto]
```

## Rastro

Gerado dos eventos 1478 a 1517 da trilha; hash dos eventos deste caso: `f972df23cfa567e6` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-20@tela.md`.
