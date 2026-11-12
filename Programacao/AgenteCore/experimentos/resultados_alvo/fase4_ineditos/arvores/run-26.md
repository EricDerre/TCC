<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `run-26`

Caso `run-26` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/run-26`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (981 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (981 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4000 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-pedido` (83,59), `pedido-reserva` (81,08) e `valor_fora_do_dominio` (57,97) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-pedido`, `pedido-reserva` e `valor_fora_do_dominio`; o da entidade, em `contrato-pedido`, `pedido-reserva` e `valor_fora_do_dominio` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `fluxo-reserva-e-cancelamento` (47,92), `dado_desatualizado` (45,98), `chave_de_juncao_errada` (39,19), `usuario-e-login` (34,88) e `estado_da_tela_divergente` (34,61) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/pedidos`, entidade `Pedido`, status 200 e 95 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `valor_fora_do_dominio`, e o primeiro de fora, `fluxo-reserva-e-cancelamento`, só o texto do caso já punha o primeiro à frente (54,97 contra 46,92), e os reforços em código levaram a diferença a 10,05 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-pedido` | posição 1, pontuação 83,59: 80,59 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pedido-reserva` | posição 2, pontuação 81,08: 78,08 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `valor_fora_do_dominio` | posição 3, pontuação 57,97: 54,97 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `fluxo-reserva-e-cancelamento` | posição 4, pontuação 47,92: 46,92 pelas palavras do caso, mais 1,0 por entidade |  |
| `dado_desatualizado` | posição 5, pontuação 45,98: 42,98 pelas palavras do caso, mais 2,0 por rota e 1,0 por status |  |
| `chave_de_juncao_errada` | posição 6, pontuação 39,19: 36,19 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `usuario-e-login` | posição 7, pontuação 34,88: 34,88 pelas palavras do caso, sem reforço |  |
| `estado_da_tela_divergente` | posição 8, pontuação 34,61: 34,61 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `registro_duplicado` (Registro duplicado); segunda: `dado_desatualizado`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `registro_duplicado` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `dado_desatualizado` (Dado desatualizado (cache)), ficou com probabilidade 0,216 contra 0,757 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 10 alternativas lidas na resposta somam probabilidade 0,017; as maiores: `estado_da_tela_divergente` (0,010), `tempo_de_resposta_excedido` (0,002) e `resposta_truncada` (0,001) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,757, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/pedidos?login=11122233344`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-pedido` (declarado).
- Verbete citado `contrato-pedido`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), não traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Leitura do verbete `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 5 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `registro_duplicado` | 0,757 | nenhum | sim |
| `dado_desatualizado` | 0,216 | nenhum |  |
| `estado_da_tela_divergente` | 0,010 | nenhum |  |
| `tempo_de_resposta_excedido` | 0,002 | nenhum |  |
| `resposta_truncada` | 0,001 | nenhum |  |
| `nulo_inesperado` | 0,001 | `pedido-reserva` e `valor_fora_do_dominio` |  |
| `valor_fora_do_dominio` | 0,001 | `contrato-pedido`, `pedido-reserva` e `valor_fora_do_dominio` |  |
| `campo_ausente` | 0,001 | `contrato-pedido` |  |
| `campo_renomeado` | 0,001 | nenhum |  |
| `contagem_inconsistente` | 0,000 | nenhum |  |
| `recurso_inexistente` | 0,000 | `contrato-pedido` |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê reservas com status inconsistente, onde algumas reservas não refletem o status atualizado.
> FONTE: [contrato-pedido]

Resposta inteira:

```text
CAUSA_RAIZ: registro_duplicado
CAMPO: nenhum
IMPACTO: O usuário vê reservas com status inconsistente, onde algumas reservas não refletem o status atualizado.
FONTE: [contrato-pedido]
```

## Rastro

Gerado dos eventos 691 a 712 da trilha; hash dos eventos deste caso: `8211e6707f45b278` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/run-26.md`.
