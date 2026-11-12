<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `run-23`

Caso `run-23` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/run-23`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (606 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (606 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3566 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `recurso_inexistente` (50,44), `contrato-produto` (28,80) e `mensagens-de-erro-do-codigo` (25,66) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `recurso_inexistente` e `contrato-produto`; o da entidade, em `contrato-produto`; o do status, em `recurso_inexistente`, `contrato-produto` e `mensagens-de-erro-do-codigo` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `contagem_inconsistente` (25,24), `pagina-produtos-api` (24,78), `ancora-saiba-mais` (24,26), `entidade-produto` (20,22) e `colecao_no_lugar_de_objeto` (19,84) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 404 e 51 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `mensagens-de-erro-do-codigo`, e o primeiro de fora, `contagem_inconsistente`, só o texto do caso já punha o primeiro à frente (24,66 contra 24,24), e os reforços em código levaram a diferença a 0,43 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `recurso_inexistente` | posição 1, pontuação 50,44: 47,44 pelas palavras do caso, mais 2,0 por rota e 1,0 por status | sim |
| `contrato-produto` | posição 2, pontuação 28,80: 24,80 pelas palavras do caso, mais 2,0 por rota, 1,0 por entidade e 1,0 por status | sim |
| `mensagens-de-erro-do-codigo` | posição 3, pontuação 25,66: 24,66 pelas palavras do caso, mais 1,0 por status | sim |
| `contagem_inconsistente` | posição 4, pontuação 25,24: 24,24 pelas palavras do caso, mais 1,0 por entidade |  |
| `pagina-produtos-api` | posição 5, pontuação 24,78: 22,78 pelas palavras do caso, mais 2,0 por rota |  |
| `ancora-saiba-mais` | posição 6, pontuação 24,26: 24,26 pelas palavras do caso, sem reforço |  |
| `entidade-produto` | posição 7, pontuação 20,22: 17,22 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 8, pontuação 19,84: 16,84 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `recurso_inexistente` (Recurso inexistente (404 e vizinhos)); segunda: `registro_duplicado`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `recurso_inexistente` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `registro_duplicado` (Registro duplicado), ficou com probabilidade 0,000 contra 0,996 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 3 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `campo_renomeado` (0,000) e `resposta_truncada` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,996, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/5`, o status 404 (a API não achou o recurso) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `recurso_inexistente` (declarado).
- Verbete citado `recurso_inexistente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `recurso_inexistente`, `contrato-produto` e `mensagens-de-erro-do-codigo` (conferido).
- Leitura do verbete `recurso_inexistente` (Recurso inexistente (404 e vizinhos); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/recurso_inexistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/recurso_inexistente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `recurso_inexistente` | 0,996 | `recurso_inexistente`, `contrato-produto` e `mensagens-de-erro-do-codigo` | sim |
| `registro_duplicado` | 0,000 | nenhum |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `resposta_truncada` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um erro "HTTP 404" ao tentar acessar detalhes do produto, indicando que o recurso não existe.
> FONTE: [recurso_inexistente]

Resposta inteira:

```text
CAUSA_RAIZ: recurso_inexistente
CAMPO: id
IMPACTO: O usuário vê um erro "HTTP 404" ao tentar acessar detalhes do produto, indicando que o recurso não existe.
FONTE: [recurso_inexistente]
```

## Rastro

Gerado dos eventos 618 a 639 da trilha; hash dos eventos deste caso: `43860baed69d86cb` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/run-23.md`.
