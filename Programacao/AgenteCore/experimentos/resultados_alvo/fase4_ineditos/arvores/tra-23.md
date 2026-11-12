<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-23`

Caso `tra-23` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/tra-23`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (679 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (679 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3698 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-pedido` (54,95), `pedido-reserva` (48,66) e `valor_fora_do_dominio` (32,22) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-pedido`; o da entidade, em `contrato-pedido`, `pedido-reserva` e `valor_fora_do_dominio`; o do status, em `contrato-pedido` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estado_da_tela_divergente` (28,70), `fluxo-reserva-e-cancelamento` (28,28), `formato_de_data_divergente` (25,20), `chave_de_juncao_errada` (24,25) e `dado_desatualizado` (19,75) (observado).
- Sinais da consulta, tirados do caso em código: rota `POST /api/pedidos`, entidade `Pedido`, status 201 e 59 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `valor_fora_do_dominio`, e o primeiro de fora, `estado_da_tela_divergente`, só o texto do caso já punha o primeiro à frente (31,22 contra 28,70), e os reforços em código levaram a diferença a 3,52 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-pedido` | posição 1, pontuação 54,95: 50,95 pelas palavras do caso, mais 2,0 por rota, 1,0 por entidade e 1,0 por status | sim |
| `pedido-reserva` | posição 2, pontuação 48,66: 47,66 pelas palavras do caso, mais 1,0 por entidade | sim |
| `valor_fora_do_dominio` | posição 3, pontuação 32,22: 31,22 pelas palavras do caso, mais 1,0 por entidade | sim |
| `estado_da_tela_divergente` | posição 4, pontuação 28,70: 28,70 pelas palavras do caso, sem reforço |  |
| `fluxo-reserva-e-cancelamento` | posição 5, pontuação 28,28: 25,28 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `formato_de_data_divergente` | posição 6, pontuação 25,20: 22,20 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 7, pontuação 24,25: 23,25 pelas palavras do caso, mais 1,0 por entidade |  |
| `dado_desatualizado` | posição 8, pontuação 19,75: 18,75 pelas palavras do caso, mais 1,0 por status |  |

## Decisão 3: a causa

Escolha: `valor_fora_do_dominio` (Valor fora do domínio); segunda: `tipo_divergente`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `valor_fora_do_dominio` (declarado).
- O modelo apontou o campo `pessoas` (declarado).
- `pessoas` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,347 contra 0,649 da escolhida; verbetes entregues que a sustentam: `valor_fora_do_dominio` (observado).
- As outras 6 alternativas lidas na resposta somam probabilidade 0,007; as maiores: `campo_ausente` (0,003), `campo_renomeado` (0,003) e `formato_de_data_divergente` (0,000) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,649, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 4, "data_pedido": "2026-12-19"})`, o status 201 (a API criou o registro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `pedido-reserva` e `valor_fora_do_dominio` (declarado).
- Os 2 verbetes citados (`pedido-reserva` e `valor_fora_do_dominio`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `pedido-reserva` não confere; `valor_fora_do_dominio` confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-pedido`, `pedido-reserva` e `valor_fora_do_dominio` (conferido).
- Camada de leitura de cada verbete citado: `pedido-reserva` (Reserva de mesa (pedido); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/pedido-reserva.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/pedido-reserva.md`); `valor_fora_do_dominio` (Valor fora do domínio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/valor_fora_do_dominio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/valor_fora_do_dominio.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 10 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `valor_fora_do_dominio` | 0,649 | `contrato-pedido`, `pedido-reserva` e `valor_fora_do_dominio` | sim |
| `tipo_divergente` | 0,347 | `valor_fora_do_dominio` |  |
| `campo_ausente` | 0,003 | `contrato-pedido` |  |
| `campo_renomeado` | 0,003 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | `contrato-pedido` e `valor_fora_do_dominio` |  |
| `colecao_no_lugar_de_objeto` | 0,000 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | nenhum |  |
| `registro_duplicado` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê 400 pessoas reservadas em vez das 4 solicitadas.
> FONTE: [pedido-reserva] [valor_fora_do_dominio]

Resposta inteira:

```text
CAUSA_RAIZ: valor_fora_do_dominio
CAMPO: pessoas
IMPACTO: O usuário vê 400 pessoas reservadas em vez das 4 solicitadas.
FONTE: [pedido-reserva] [valor_fora_do_dominio]
```

## Rastro

Gerado dos eventos 468 a 493 da trilha; hash dos eventos deste caso: `b62b751f29151d15` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-23.md`.
