<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-27`

Caso `lex-27` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/lex-27`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 25 afirmações (15 observado, 7 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (716 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (716 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3605 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-pedido` (53,64), `pedido-reserva` (48,64) e `formato_de_data_divergente` (34,03) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-pedido` e `formato_de_data_divergente`; o da entidade, em `contrato-pedido`, `pedido-reserva` e `formato_de_data_divergente`; o do status, em `contrato-pedido` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estado_da_tela_divergente` (33,18), `valor_fora_do_dominio` (32,48), `fluxo-reserva-e-cancelamento` (23,11), `chave_de_juncao_errada` (20,45) e `campo_renomeado` (17,48) (observado).
- Sinais da consulta, tirados do caso em código: rota `POST /api/pedidos`, entidade `Pedido`, status 201 e 64 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `formato_de_data_divergente`, e o primeiro de fora, `estado_da_tela_divergente`, só pelo texto do caso o segundo estaria à frente (33,18 contra 31,03); os reforços em código viraram a ordem, com diferença final de 0,85 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-pedido` | posição 1, pontuação 53,64: 49,64 pelas palavras do caso, mais 2,0 por rota, 1,0 por entidade e 1,0 por status | sim |
| `pedido-reserva` | posição 2, pontuação 48,64: 47,64 pelas palavras do caso, mais 1,0 por entidade | sim |
| `formato_de_data_divergente` | posição 3, pontuação 34,03: 31,03 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estado_da_tela_divergente` | posição 4, pontuação 33,18: 33,18 pelas palavras do caso, sem reforço |  |
| `valor_fora_do_dominio` | posição 5, pontuação 32,48: 31,48 pelas palavras do caso, mais 1,0 por entidade |  |
| `fluxo-reserva-e-cancelamento` | posição 6, pontuação 23,11: 20,11 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 7, pontuação 20,45: 19,45 pelas palavras do caso, mais 1,0 por entidade |  |
| `campo_renomeado` | posição 8, pontuação 17,48: 17,48 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `codificacao_incorreta` (Codificação de caracteres incorreta); segunda: `campo_ausente`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `codificacao_incorreta` (declarado).
- O modelo apontou o campo `status` (declarado).
- `status` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,255 contra 0,742 da escolhida; verbetes entregues que a sustentam: `contrato-pedido` (observado).
- As outras 7 alternativas lidas na resposta somam probabilidade 0,258; as maiores: `campo_renomeado` (0,255), `resposta_truncada` (0,001) e `valor_fora_do_dominio` (0,001) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,742, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 3, "data_pedido": "2026-12-05"})`, o status 201 (a API criou o registro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-pedido` (declarado).
- Verbete citado `contrato-pedido`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), não traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Leitura do verbete `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 6 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `codificacao_incorreta` | 0,742 | nenhum | sim |
| `campo_ausente` | 0,255 | `contrato-pedido` |  |
| `campo_renomeado` | 0,255 | nenhum |  |
| `resposta_truncada` | 0,001 | nenhum |  |
| `valor_fora_do_dominio` | 0,001 | `contrato-pedido` e `pedido-reserva` |  |
| `tipo_divergente` | 0,001 | `formato_de_data_divergente` |  |
| `formato_de_data_divergente` | 0,000 | `contrato-pedido` e `formato_de_data_divergente` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um status com caracteres estranhos no lugar do acento, indicando um erro na codificação.
> FONTE: [contrato-pedido]

Resposta inteira:

```text
CAUSA_RAIZ: codificacao_incorreta
CAMPO: status
IMPACTO: O usuário vê um status com caracteres estranhos no lugar do acento, indicando um erro na codificação.
FONTE: [contrato-pedido]
```

## Rastro

Gerado dos eventos 130 a 151 da trilha; hash dos eventos deste caso: `3bfdbee025a159ff` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-27.md`.
