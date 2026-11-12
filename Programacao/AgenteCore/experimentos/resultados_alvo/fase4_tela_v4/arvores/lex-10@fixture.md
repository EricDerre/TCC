<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-10`

Caso `lex-10` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/lex-10@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (616 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (616 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3823 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (51,70), `resposta_truncada` (36,75) e `contrato-produto` (36,62) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; `resposta_truncada` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estrutura_aninhada_divergente` (19,41), `tipo_divergente` (16,68), `colecao_no_lugar_de_objeto` (15,97), `chave_de_juncao_errada` (15,80) e `nulo_inesperado` (15,71) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 53 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `estrutura_aninhada_divergente`, só o texto do caso já punha o primeiro à frente (33,62 contra 16,41), e os reforços em código levaram a diferença a 17,21 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 51,70: 48,70 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `resposta_truncada` | posição 2, pontuação 36,75: 36,75 pelas palavras do caso, sem reforço | sim |
| `contrato-produto` | posição 3, pontuação 36,62: 33,62 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 4, pontuação 19,41: 16,41 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tipo_divergente` | posição 5, pontuação 16,68: 13,68 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 15,97: 12,97 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 7, pontuação 15,80: 13,80 pelas palavras do caso, mais 2,0 por rota |  |
| `nulo_inesperado` | posição 8, pontuação 15,71: 13,71 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `resposta_truncada` (Resposta truncada); segunda: `corpo_nao_e_json`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `resposta_truncada` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `corpo_nao_e_json` (Corpo não é JSON), ficou com probabilidade 0,000 contra 1,000 da escolhida; verbetes entregues que a sustentam: `resposta_truncada` (observado).
- As outras 4 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `corpo_vazio` (0,000), `colecao_no_lugar_de_objeto` (0,000) e `limite_de_requisicoes` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 1,000, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `resposta_truncada` e `contrato-produto` (declarado).
- Os 2 verbetes citados (`resposta_truncada` e `contrato-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `resposta_truncada` confere; `contrato-produto` não confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `resposta_truncada` (conferido).
- Camada de leitura de cada verbete citado: `resposta_truncada` (Resposta truncada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/resposta_truncada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/resposta_truncada.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 9 de 10 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `resposta_truncada` | 1,000 | `resposta_truncada` | sim |
| `corpo_nao_e_json` | 0,000 | `resposta_truncada` |  |
| `corpo_vazio` | 0,000 | `resposta_truncada` |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` |  |
| `limite_de_requisicoes` | 0,000 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê uma lista incompleta de produtos, com apenas os dois primeiros itens exibidos.
> FONTE: [resposta_truncada] [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: resposta_truncada
CAMPO: nenhum
IMPACTO: O usuário vê uma lista incompleta de produtos, com apenas os dois primeiros itens exibidos.
FONTE: [resposta_truncada] [contrato-produto]
```

## Rastro

Gerado dos eventos 752 a 777 da trilha; hash dos eventos deste caso: `8e4cee2e8947d393` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-10@fixture.md`.
