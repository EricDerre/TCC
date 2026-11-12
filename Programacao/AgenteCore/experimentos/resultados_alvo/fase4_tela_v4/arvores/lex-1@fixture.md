<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-1`

Caso `lex-1` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/lex-1@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (383 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (383 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3590 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (28,12), `contrato-produto` (21,43) e `resposta_truncada` (19,32) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; `resposta_truncada` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (14,39), `corpo_nao_e_json` (14,04), `mensagens-de-erro-do-codigo` (12,69), `colecao_no_lugar_de_objeto` (11,78) e `estrutura_aninhada_divergente` (11,68) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 28 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `resposta_truncada`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (19,32 contra 12,39); a diferença final foi 4,93 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 28,12: 25,12 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 21,43: 18,43 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `resposta_truncada` | posição 3, pontuação 19,32: 19,32 pelas palavras do caso, sem reforço | sim |
| `pagina-produtos-api` | posição 4, pontuação 14,39: 12,39 pelas palavras do caso, mais 2,0 por rota |  |
| `corpo_nao_e_json` | posição 5, pontuação 14,04: 13,04 pelas palavras do caso, mais 1,0 por status |  |
| `mensagens-de-erro-do-codigo` | posição 6, pontuação 12,69: 12,69 pelas palavras do caso, sem reforço |  |
| `colecao_no_lugar_de_objeto` | posição 7, pontuação 11,78: 8,78 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 8, pontuação 11,68: 8,68 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `resposta_truncada` (Resposta truncada); segunda: `corpo_nao_e_json`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `resposta_truncada` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `corpo_nao_e_json` (Corpo não é JSON), ficou com probabilidade 0,000 contra 1,000 da escolhida; verbetes entregues que a sustentam: `resposta_truncada` (observado).
- As outras 5 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `corpo_vazio` (0,000), `colecao_no_lugar_de_objeto` (0,000) e `campo_ausente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 1,000, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `resposta_truncada` (declarado).
- Verbete citado `resposta_truncada`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `resposta_truncada` (conferido).
- Leitura do verbete `resposta_truncada` (Resposta truncada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/resposta_truncada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/resposta_truncada.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `resposta_truncada` | 1,000 | `resposta_truncada` | sim |
| `corpo_nao_e_json` | 0,000 | `resposta_truncada` |  |
| `corpo_vazio` | 0,000 | `resposta_truncada` |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `tipo_divergente` | 0,000 | `entidade-produto` e `contrato-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A interface web recebe uma resposta incompleta, resultando em uma lista vazia e erro de interpretação.
> FONTE: [resposta_truncada]

Resposta inteira:

```text
CAUSA_RAIZ: resposta_truncada
CAMPO: nenhum
IMPACTO: A interface web recebe uma resposta incompleta, resultando em uma lista vazia e erro de interpretação.
FONTE: [resposta_truncada]
```

## Rastro

Gerado dos eventos 44 a 65 da trilha; hash dos eventos deste caso: `82a342e900da623d` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-1@fixture.md`.
