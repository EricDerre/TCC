<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-7`

Caso `lex-7` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/lex-7@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (300 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (300 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3534 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `corpo_vazio` (28,51), `ancora-saiba-mais` (11,17) e `colecao_no_lugar_de_objeto` (9,70) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `colecao_no_lugar_de_objeto`; o da entidade, em `colecao_no_lugar_de_objeto`; o do status, em `corpo_vazio`; `ancora-saiba-mais` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `recurso_inexistente` (7,20), `campo_ausente` (6,93), `pagina-produtos-api` (6,74), `entidade-produto` (6,35) e `mensagens-de-erro-do-codigo` (6,05) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 204 e 14 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `colecao_no_lugar_de_objeto`, e o primeiro de fora, `recurso_inexistente`, só o texto do caso já punha o primeiro à frente (6,70 contra 5,20), e os reforços em código levaram a diferença a 2,50 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `corpo_vazio` | posição 1, pontuação 28,51: 27,51 pelas palavras do caso, mais 1,0 por status | sim |
| `ancora-saiba-mais` | posição 2, pontuação 11,17: 11,17 pelas palavras do caso, sem reforço | sim |
| `colecao_no_lugar_de_objeto` | posição 3, pontuação 9,70: 6,70 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `recurso_inexistente` | posição 4, pontuação 7,20: 5,20 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_ausente` | posição 5, pontuação 6,93: 5,93 pelas palavras do caso, mais 1,0 por entidade |  |
| `pagina-produtos-api` | posição 6, pontuação 6,74: 4,74 pelas palavras do caso, mais 2,0 por rota |  |
| `entidade-produto` | posição 7, pontuação 6,35: 3,35 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `mensagens-de-erro-do-codigo` | posição 8, pontuação 6,05: 6,05 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `corpo_vazio` (Corpo vazio); segunda: `resposta_truncada`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `corpo_vazio` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `resposta_truncada` (Resposta truncada), ficou com probabilidade 0,000 contra 0,999 da escolhida; verbetes entregues que a sustentam: `corpo_vazio` (observado).
- A outra alternativa lida na resposta, `corpo_nao_e_json`, tem probabilidade 0,000 (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,999, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/1`, o status 204 (a API respondeu sem corpo) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `corpo_vazio` (declarado).
- Verbete citado `corpo_vazio`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `corpo_vazio` (conferido).
- Leitura do verbete `corpo_vazio` (Corpo vazio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/corpo_vazio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/corpo_vazio.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `corpo_vazio` | 0,999 | `corpo_vazio` | sim |
| `resposta_truncada` | 0,000 | `corpo_vazio` |  |
| `corpo_nao_e_json` | 0,000 | `corpo_vazio` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A tela de detalhe abre em branco, sem exibir nenhum produto ou mensagem de erro.
> FONTE: [corpo_vazio]

Resposta inteira:

```text
CAUSA_RAIZ: corpo_vazio
CAMPO: nenhum
IMPACTO: A tela de detalhe abre em branco, sem exibir nenhum produto ou mensagem de erro.
FONTE: [corpo_vazio]
```

## Rastro

Gerado dos eventos 642 a 663 da trilha; hash dos eventos deste caso: `7de053b8818800b9` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-7@fixture.md`.
