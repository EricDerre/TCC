<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `run-27`

Caso `run-27` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/run-27`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1042 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1042 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3887 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-pedido` (86,29), `pedido-reserva` (55,12) e `registro_duplicado` (44,82) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-pedido`, `pedido-reserva` e `registro_duplicado`; o da entidade, em `contrato-pedido`, `pedido-reserva` e `registro_duplicado` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `valor_fora_do_dominio` (38,97), `formato_de_data_divergente` (38,89), `chave_de_juncao_errada` (38,22), `estado_da_tela_divergente` (37,16) e `fluxo-reserva-e-cancelamento` (33,15) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/pedidos`, entidade `Pedido`, status 200 e 101 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `registro_duplicado`, e o primeiro de fora, `valor_fora_do_dominio`, só o texto do caso já punha o primeiro à frente (41,82 contra 35,97), e os reforços em código levaram a diferença a 5,85 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-pedido` | posição 1, pontuação 86,29: 83,29 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pedido-reserva` | posição 2, pontuação 55,12: 52,12 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `registro_duplicado` | posição 3, pontuação 44,82: 41,82 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `valor_fora_do_dominio` | posição 4, pontuação 38,97: 35,97 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `formato_de_data_divergente` | posição 5, pontuação 38,89: 35,89 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 6, pontuação 38,22: 35,22 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estado_da_tela_divergente` | posição 7, pontuação 37,16: 37,16 pelas palavras do caso, sem reforço |  |
| `fluxo-reserva-e-cancelamento` | posição 8, pontuação 33,15: 32,15 pelas palavras do caso, mais 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `registro_duplicado` (Registro duplicado); segunda: `tipo_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `registro_duplicado` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 1,000 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 2 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `erro_interno_do_servidor` (0,000) e `recurso_inexistente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 1,000, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/pedidos?login=11122233344`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-pedido` e `registro_duplicado` (declarado).
- Os 2 verbetes citados (`contrato-pedido` e `registro_duplicado`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `contrato-pedido` não confere; `registro_duplicado` confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `registro_duplicado` (conferido).
- Camada de leitura de cada verbete citado: `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`); `registro_duplicado` (Registro duplicado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/registro_duplicado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/registro_duplicado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 9 de 10 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `registro_duplicado` | 1,000 | `registro_duplicado` | sim |
| `tipo_divergente` | 0,000 | nenhum |  |
| `erro_interno_do_servidor` | 0,000 | nenhum |  |
| `recurso_inexistente` | 0,000 | `contrato-pedido` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê duas reservas iguais na lista, embora tenha solicitado apenas uma.
> FONTE: [contrato-pedido] [registro_duplicado]

Resposta inteira:

```text
CAUSA_RAIZ: registro_duplicado
CAMPO: nenhum
IMPACTO: O usuário vê duas reservas iguais na lista, embora tenha solicitado apenas uma.
FONTE: [contrato-pedido] [registro_duplicado]
```

## Rastro

Gerado dos eventos 714 a 739 da trilha; hash dos eventos deste caso: `efd2daf899ced71f` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/run-27.md`.
