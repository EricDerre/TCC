<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `semt-25`

Caso `semt-25` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/semt-25`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (675 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (675 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3564 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-pedido` (66,84), `formato_de_data_divergente` (65,75) e `pedido-reserva` (43,11) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-pedido` e `formato_de_data_divergente`; o da entidade, em `contrato-pedido`, `formato_de_data_divergente` e `pedido-reserva`; o do status, em `contrato-pedido` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `fluxo-reserva-e-cancelamento` (30,53), `valor_fora_do_dominio` (23,61), `chave_de_juncao_errada` (20,42), `consultas-sem-checagem` (19,32) e `estrutura_aninhada_divergente` (18,16) (observado).
- Sinais da consulta, tirados do caso em código: rota `POST /api/pedidos`, entidade `Pedido`, status 201 e 62 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `pedido-reserva`, e o primeiro de fora, `fluxo-reserva-e-cancelamento`, só o texto do caso já punha o primeiro à frente (42,11 contra 27,53), e os reforços em código levaram a diferença a 12,58 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-pedido` | posição 1, pontuação 66,84: 62,84 pelas palavras do caso, mais 2,0 por rota, 1,0 por entidade e 1,0 por status | sim |
| `formato_de_data_divergente` | posição 2, pontuação 65,75: 62,75 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pedido-reserva` | posição 3, pontuação 43,11: 42,11 pelas palavras do caso, mais 1,0 por entidade | sim |
| `fluxo-reserva-e-cancelamento` | posição 4, pontuação 30,53: 27,53 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `valor_fora_do_dominio` | posição 5, pontuação 23,61: 22,61 pelas palavras do caso, mais 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 6, pontuação 20,42: 19,42 pelas palavras do caso, mais 1,0 por entidade |  |
| `consultas-sem-checagem` | posição 7, pontuação 19,32: 18,32 pelas palavras do caso, mais 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 8, pontuação 18,16: 18,16 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `formato_de_data_divergente` (Formato de data divergente); segunda: `tipo_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `formato_de_data_divergente` (declarado).
- O modelo apontou o campo `data_pedido` (declarado).
- `data_pedido` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,015 contra 0,984 da escolhida; verbetes entregues que a sustentam: `formato_de_data_divergente` (observado).
- As outras 6 alternativas lidas na resposta somam probabilidade 0,002; as maiores: `campo_ausente` (0,001), `campo_renomeado` (0,001) e `valor_fora_do_dominio` (0,000) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,984, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 6, "data_pedido": "2026-12-20"})`, o status 201 (a API criou o registro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `formato_de_data_divergente` (declarado).
- Verbete citado `formato_de_data_divergente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-pedido` e `formato_de_data_divergente` (conferido).
- Leitura do verbete `formato_de_data_divergente` (Formato de data divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/formato_de_data_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/formato_de_data_divergente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `formato_de_data_divergente` | 0,984 | `contrato-pedido` e `formato_de_data_divergente` | sim |
| `tipo_divergente` | 0,015 | `formato_de_data_divergente` |  |
| `campo_ausente` | 0,001 | `contrato-pedido` |  |
| `campo_renomeado` | 0,001 | nenhum |  |
| `valor_fora_do_dominio` | 0,000 | `contrato-pedido` e `pedido-reserva` |  |
| `escala_ou_unidade_errada` | 0,000 | `formato_de_data_divergente` |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |
| `resposta_truncada` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário recebe uma data no formato '20/12/2026' em vez do esperado '2026-12-20', dificultando a interpretação da data ISO (AAAA-MM-DD).
> FONTE: [formato_de_data_divergente]

Resposta inteira:

```text
CAUSA_RAIZ: formato_de_data_divergente
CAMPO: data_pedido
IMPACTO: O usuário recebe uma data no formato '20/12/2026' em vez do esperado '2026-12-20', dificultando a interpretação da data ISO (AAAA-MM-DD).
FONTE: [formato_de_data_divergente]
```

## Rastro

Gerado dos eventos 372 a 393 da trilha; hash dos eventos deste caso: `741ca78bdb34b7ae` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/semt-25.md`.
