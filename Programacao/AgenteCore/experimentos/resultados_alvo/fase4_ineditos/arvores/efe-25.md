<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `efe-25`

Caso `efe-25` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/efe-25`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1427 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1427 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4610 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `localizador_quebrado` (43,18), `contrato-produto` (27,62) e `entidade-produto` (27,19) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto` e `entidade-produto`; o da entidade, em `localizador_quebrado` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estado_da_tela_divergente` (26,90), `ancora-saiba-mais` (25,99), `pagina-produtos-api` (21,85), `campo_ausente` (19,83) e `dado_desatualizado` (18,06) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Interface`, status 200 e 67 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `estado_da_tela_divergente`, só pelo texto do caso o segundo estaria à frente (25,90 contra 25,19); os reforços em código viraram a ordem, com diferença final de 0,29 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `localizador_quebrado` | posição 1, pontuação 43,18: 42,18 pelas palavras do caso, mais 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 27,62: 25,62 pelas palavras do caso, mais 2,0 por rota | sim |
| `entidade-produto` | posição 3, pontuação 27,19: 25,19 pelas palavras do caso, mais 2,0 por rota | sim |
| `estado_da_tela_divergente` | posição 4, pontuação 26,90: 25,90 pelas palavras do caso, mais 1,0 por entidade |  |
| `ancora-saiba-mais` | posição 5, pontuação 25,99: 24,99 pelas palavras do caso, mais 1,0 por entidade |  |
| `pagina-produtos-api` | posição 6, pontuação 21,85: 18,85 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_ausente` | posição 7, pontuação 19,83: 19,83 pelas palavras do caso, sem reforço |  |
| `dado_desatualizado` | posição 8, pontuação 18,06: 17,06 pelas palavras do caso, mais 1,0 por status |  |

## Decisão 3: a causa

Escolha: `localizador_quebrado` (Localizador (seletor) quebrado); segunda: `estado_da_tela_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `localizador_quebrado` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `estado_da_tela_divergente` (Estado da tela divergente da resposta), ficou com probabilidade 0,000 contra 0,959 da escolhida; verbetes entregues que a sustentam: `localizador_quebrado` (observado).
- As outras 2 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000) e `campo_renomeado` (0,000) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,959, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/3`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `localizador_quebrado` (declarado).
- Verbete citado `localizador_quebrado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `localizador_quebrado` (conferido).
- Leitura do verbete `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `localizador_quebrado` | 0,959 | `localizador_quebrado` | sim |
| `estado_da_tela_divergente` | 0,000 | `localizador_quebrado` |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário não consegue visualizar o detalhe do produto corretamente, pois o modal não carrega o título esperado.
> FONTE: [localizador_quebrado]

Resposta inteira:

```text
CAUSA_RAIZ: localizador_quebrado
CAMPO: nenhum
IMPACTO: O usuário não consegue visualizar o detalhe do produto corretamente, pois o modal não carrega o título esperado.
FONTE: [localizador_quebrado]
```

## Rastro

Gerado dos eventos 810 a 831 da trilha; hash dos eventos deste caso: `26088ac9bd4c3c76` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/efe-25.md`.
