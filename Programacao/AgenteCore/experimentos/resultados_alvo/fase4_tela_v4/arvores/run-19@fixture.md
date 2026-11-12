<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `run-19`

Caso `run-19` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/run-19@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (558 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (558 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3233 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `tempo_de_resposta_excedido` (29,41), `pagina-produtos-api` (18,87) e `registro_duplicado` (17,54) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `pagina-produtos-api`; o do status, em `tempo_de_resposta_excedido`; `registro_duplicado` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `codificacao_incorreta` (14,99), `colecao_no_lugar_de_objeto` (14,78), `ancora-saiba-mais` (14,59), `localizador_quebrado` (14,30) e `campo_ausente` (12,20) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 40 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `registro_duplicado`, e o primeiro de fora, `codificacao_incorreta`, só o texto do caso já punha o primeiro à frente (17,54 contra 14,99); a diferença final foi 2,55 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `tempo_de_resposta_excedido` | posição 1, pontuação 29,41: 28,41 pelas palavras do caso, mais 1,0 por status | sim |
| `pagina-produtos-api` | posição 2, pontuação 18,87: 16,87 pelas palavras do caso, mais 2,0 por rota | sim |
| `registro_duplicado` | posição 3, pontuação 17,54: 17,54 pelas palavras do caso, sem reforço | sim |
| `codificacao_incorreta` | posição 4, pontuação 14,99: 14,99 pelas palavras do caso, sem reforço |  |
| `colecao_no_lugar_de_objeto` | posição 5, pontuação 14,78: 11,78 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `ancora-saiba-mais` | posição 6, pontuação 14,59: 14,59 pelas palavras do caso, sem reforço |  |
| `localizador_quebrado` | posição 7, pontuação 14,30: 14,30 pelas palavras do caso, sem reforço |  |
| `campo_ausente` | posição 8, pontuação 12,20: 11,20 pelas palavras do caso, mais 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `tempo_de_resposta_excedido` (Tempo de resposta excedido); segunda: `tipo_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `tempo_de_resposta_excedido` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 1,000 da escolhida; verbetes entregues que a sustentam: `pagina-produtos-api` (observado).
- A outra alternativa lida na resposta, `formato_de_data_divergente`, tem probabilidade 0,000 (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 1,000, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/1 (clique em 'Saiba Mais...')`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `tempo_de_resposta_excedido` (declarado).
- Verbete citado `tempo_de_resposta_excedido`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `tempo_de_resposta_excedido` (conferido).
- Leitura do verbete `tempo_de_resposta_excedido` (Tempo de resposta excedido; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tempo_de_resposta_excedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tempo_de_resposta_excedido.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `tempo_de_resposta_excedido` | 1,000 | `tempo_de_resposta_excedido` | sim |
| `tipo_divergente` | 0,000 | `pagina-produtos-api` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário espera por cerca de 8 segundos antes de ver os detalhes do produto, o que causa uma experiência ruim e pode levar ao abandono do site.
> FONTE: [tempo_de_resposta_excedido]

Resposta inteira:

```text
CAUSA_RAIZ: tempo_de_resposta_excedido
CAMPO: nenhum
IMPACTO: O usuário espera por cerca de 8 segundos antes de ver os detalhes do produto, o que causa uma experiência ruim e pode levar ao abandono do site.
FONTE: [tempo_de_resposta_excedido]
```

## Rastro

Gerado dos eventos 2115 a 2136 da trilha; hash dos eventos deste caso: `aadddfed408e60ec` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/run-19@fixture.md`.
