<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `efe-26`

Caso `efe-26` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/efe-26`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1579 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1579 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4893 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (48,48), `contrato-produto` (35,88) e `colecao_no_lugar_de_objeto` (32,02) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `colecao_no_lugar_de_objeto`; o da entidade, em `entidade-produto`, `contrato-produto` e `colecao_no_lugar_de_objeto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (30,76), `estado_da_tela_divergente` (29,63), `ancora-saiba-mais` (28,67), `tempo_de_resposta_excedido` (27,29) e `corpo_nao_e_json` (24,08) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 86 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `colecao_no_lugar_de_objeto`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (29,02 contra 28,76), e os reforços em código levaram a diferença a 1,26 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 48,48: 45,48 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 35,88: 32,88 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `colecao_no_lugar_de_objeto` | posição 3, pontuação 32,02: 29,02 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pagina-produtos-api` | posição 4, pontuação 30,76: 28,76 pelas palavras do caso, mais 2,0 por rota |  |
| `estado_da_tela_divergente` | posição 5, pontuação 29,63: 29,63 pelas palavras do caso, sem reforço |  |
| `ancora-saiba-mais` | posição 6, pontuação 28,67: 28,67 pelas palavras do caso, sem reforço |  |
| `tempo_de_resposta_excedido` | posição 7, pontuação 27,29: 26,29 pelas palavras do caso, mais 1,0 por status |  |
| `corpo_nao_e_json` | posição 8, pontuação 24,08: 23,08 pelas palavras do caso, mais 1,0 por status |  |

## Decisão 3: a causa

Escolha: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)); segunda: `tempo_de_resposta_excedido`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `colecao_no_lugar_de_objeto` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tempo_de_resposta_excedido` (Tempo de resposta excedido), ficou com probabilidade 0,044 contra 0,906 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,056; as maiores: `tipo_divergente` (0,025), `campo_ausente` (0,009) e `campo_renomeado` (0,009) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,906, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/9`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `colecao_no_lugar_de_objeto` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `colecao_no_lugar_de_objeto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `contrato-produto` não confere; `colecao_no_lugar_de_objeto` confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-produto` e `colecao_no_lugar_de_objeto` (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/colecao_no_lugar_de_objeto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/colecao_no_lugar_de_objeto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 10 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `colecao_no_lugar_de_objeto` | 0,906 | `contrato-produto` e `colecao_no_lugar_de_objeto` | sim |
| `tempo_de_resposta_excedido` | 0,044 | nenhum |  |
| `tipo_divergente` | 0,025 | `entidade-produto` e `contrato-produto` |  |
| `campo_ausente` | 0,009 | `contrato-produto` e `colecao_no_lugar_de_objeto` |  |
| `campo_renomeado` | 0,009 | `contrato-produto` |  |
| `resposta_truncada` | 0,007 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,005 | `colecao_no_lugar_de_objeto` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê o título e a descrição da Fraldinha no modal, mesmo após clicar no botão do Balde de Cerveja.
> FONTE: [contrato-produto], [colecao_no_lugar_de_objeto]

Resposta inteira:

```text
CAUSA_RAIZ: colecao_no_lugar_de_objeto
CAMPO: id
IMPACTO: O usuário vê o título e a descrição da Fraldinha no modal, mesmo após clicar no botão do Balde de Cerveja.
FONTE: [contrato-produto], [colecao_no_lugar_de_objeto]
```

## Rastro

Gerado dos eventos 833 a 858 da trilha; hash dos eventos deste caso: `93af00621c521043` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/efe-26.md`.
