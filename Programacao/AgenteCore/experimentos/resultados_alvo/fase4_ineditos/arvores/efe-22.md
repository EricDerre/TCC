<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `efe-22`

Caso `efe-22` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/efe-22`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1393 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1393 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4576 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-produto` (45,85), `localizador_quebrado` (44,99) e `entidade-produto` (41,95) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto` e `entidade-produto`; o da entidade, em `localizador_quebrado` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (30,08), `ancora-saiba-mais` (29,72), `tipo_divergente` (27,15), `estado_da_tela_divergente` (26,46) e `chave_de_juncao_errada` (24,91) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Interface`, status 200 e 81 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (39,95 contra 27,08), e os reforços em código levaram a diferença a 11,87 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-produto` | posição 1, pontuação 45,85: 43,85 pelas palavras do caso, mais 2,0 por rota | sim |
| `localizador_quebrado` | posição 2, pontuação 44,99: 43,99 pelas palavras do caso, mais 1,0 por entidade | sim |
| `entidade-produto` | posição 3, pontuação 41,95: 39,95 pelas palavras do caso, mais 2,0 por rota | sim |
| `pagina-produtos-api` | posição 4, pontuação 30,08: 27,08 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `ancora-saiba-mais` | posição 5, pontuação 29,72: 28,72 pelas palavras do caso, mais 1,0 por entidade |  |
| `tipo_divergente` | posição 6, pontuação 27,15: 25,15 pelas palavras do caso, mais 2,0 por rota |  |
| `estado_da_tela_divergente` | posição 7, pontuação 26,46: 25,46 pelas palavras do caso, mais 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 8, pontuação 24,91: 22,91 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `localizador_quebrado` (Localizador (seletor) quebrado); segunda: `campo_ausente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `localizador_quebrado` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,000 contra 0,990 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 4 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_renomeado` (0,000), `chave_de_juncao_errada` (0,000) e `tipo_divergente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,990, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `localizador_quebrado` (declarado).
- Verbete citado `localizador_quebrado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `localizador_quebrado` (conferido).
- Leitura do verbete `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `localizador_quebrado` | 0,990 | `localizador_quebrado` | sim |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` |  |
| `tipo_divergente` | 0,000 | `contrato-produto` e `entidade-produto` |  |
| `nulo_inesperado` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário não consegue abrir os detalhes da Fraldinha, pois o seletor #saiba-mais-3 não encontra nenhum elemento correspondente na página.
> FONTE: [localizador_quebrado]

Resposta inteira:

```text
CAUSA_RAIZ: localizador_quebrado
CAMPO: nenhum
IMPACTO: O usuário não consegue abrir os detalhes da Fraldinha, pois o seletor #saiba-mais-3 não encontra nenhum elemento correspondente na página.
FONTE: [localizador_quebrado]
```

## Rastro

Gerado dos eventos 741 a 762 da trilha; hash dos eventos deste caso: `9ab0baf477d84a4f` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/efe-22.md`.
