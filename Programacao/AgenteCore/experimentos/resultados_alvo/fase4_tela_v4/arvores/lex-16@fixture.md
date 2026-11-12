<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-16`

Caso `lex-16` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/lex-16@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (505 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (505 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3839 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `resposta_truncada` (35,73), `entidade-produto` (26,96) e `corpo_nao_e_json` (24,43) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`; o da entidade, em `entidade-produto`; o do status, em `corpo_nao_e_json`; `resposta_truncada` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `mensagens-de-erro-do-codigo` (21,80), `pagina-produtos-api` (19,16), `ancora-saiba-mais` (15,84), `corpo_vazio` (15,48) e `modos-de-injecao` (13,98) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 40 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `corpo_nao_e_json`, e o primeiro de fora, `mensagens-de-erro-do-codigo`, só o texto do caso já punha o primeiro à frente (23,43 contra 21,80), e os reforços em código levaram a diferença a 2,63 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `resposta_truncada` | posição 1, pontuação 35,73: 35,73 pelas palavras do caso, sem reforço | sim |
| `entidade-produto` | posição 2, pontuação 26,96: 23,96 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `corpo_nao_e_json` | posição 3, pontuação 24,43: 23,43 pelas palavras do caso, mais 1,0 por status | sim |
| `mensagens-de-erro-do-codigo` | posição 4, pontuação 21,80: 21,80 pelas palavras do caso, sem reforço |  |
| `pagina-produtos-api` | posição 5, pontuação 19,16: 17,16 pelas palavras do caso, mais 2,0 por rota |  |
| `ancora-saiba-mais` | posição 6, pontuação 15,84: 15,84 pelas palavras do caso, sem reforço |  |
| `corpo_vazio` | posição 7, pontuação 15,48: 15,48 pelas palavras do caso, sem reforço |  |
| `modos-de-injecao` | posição 8, pontuação 13,98: 13,98 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `resposta_truncada` (Resposta truncada); segunda: `corpo_nao_e_json`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `resposta_truncada` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `corpo_nao_e_json` (Corpo não é JSON), ficou com probabilidade 0,000 contra 1,000 da escolhida; verbetes entregues que a sustentam: `resposta_truncada` e `corpo_nao_e_json` (observado).
- A outra alternativa lida na resposta, `corpo_vazio`, tem probabilidade 0,000 (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 1,000, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/1 (modo malformed_json ligado)`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `resposta_truncada` (declarado).
- Verbete citado `resposta_truncada`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `resposta_truncada` e `corpo_nao_e_json` (conferido).
- Leitura do verbete `resposta_truncada` (Resposta truncada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/resposta_truncada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/resposta_truncada.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `resposta_truncada` | 1,000 | `resposta_truncada` e `corpo_nao_e_json` | sim |
| `corpo_nao_e_json` | 0,000 | `resposta_truncada` e `corpo_nao_e_json` |  |
| `corpo_vazio` | 0,000 | `resposta_truncada` e `corpo_nao_e_json` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um erro ao tentar interpretar o JSON, mesmo com a resposta retornando um código 200.
> FONTE: [resposta_truncada]

Resposta inteira:

```text
CAUSA_RAIZ: resposta_truncada
CAMPO: nenhum
IMPACTO: O usuário vê um erro ao tentar interpretar o JSON, mesmo com a resposta retornando um código 200.
FONTE: [resposta_truncada]
```

## Rastro

Gerado dos eventos 1332 a 1353 da trilha; hash dos eventos deste caso: `31956ebe816d5ab4` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-16@fixture.md`.
