<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-5`

Caso `sin-5` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/sin-5@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (572 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (572 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3663 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (56,61), `contrato-produto` (44,84) e `tipo_divergente` (23,15) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `tipo_divergente`; o da entidade, em `entidade-produto`, `contrato-produto` e `tipo_divergente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `campo_ausente` (22,67), `campo_renomeado` (22,42), `valor_fora_do_dominio` (22,38), `chave_de_juncao_errada` (21,32) e `nulo_inesperado` (20,11) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 46 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `tipo_divergente`, e o primeiro de fora, `campo_ausente`, só o texto do caso já punha o primeiro à frente (20,15 contra 19,67), e os reforços em código levaram a diferença a 0,49 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 56,61: 53,61 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 44,84: 41,84 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tipo_divergente` | posição 3, pontuação 23,15: 20,15 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_ausente` | posição 4, pontuação 22,67: 19,67 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_renomeado` | posição 5, pontuação 22,42: 19,42 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `valor_fora_do_dominio` | posição 6, pontuação 22,38: 20,38 pelas palavras do caso, mais 2,0 por rota |  |
| `chave_de_juncao_errada` | posição 7, pontuação 21,32: 19,32 pelas palavras do caso, mais 2,0 por rota |  |
| `nulo_inesperado` | posição 8, pontuação 20,11: 18,11 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)); segunda: `tipo_divergente`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `colecao_no_lugar_de_objeto` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,344 contra 0,625 da escolhida; verbetes entregues que a sustentam: `entidade-produto`, `contrato-produto` e `tipo_divergente` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,045; as maiores: `campo_ausente` (0,015), `campo_renomeado` (0,015) e `estrutura_aninhada_divergente` (0,009) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,625, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` (declarado).
- Verbete citado `contrato-produto`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), não traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-produto` (conferido).
- Leitura do verbete `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 6 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `colecao_no_lugar_de_objeto` | 0,625 | `contrato-produto` | sim |
| `tipo_divergente` | 0,344 | `entidade-produto`, `contrato-produto` e `tipo_divergente` |  |
| `campo_ausente` | 0,015 | `contrato-produto` |  |
| `campo_renomeado` | 0,015 | `contrato-produto` |  |
| `estrutura_aninhada_divergente` | 0,009 | nenhum |  |
| `resposta_truncada` | 0,002 | nenhum |  |
| `formato_de_data_divergente` | 0,001 | `tipo_divergente` |  |
| `corpo_nao_e_json` | 0,001 | nenhum |  |
| `corpo_vazio` | 0,001 | nenhum |  |
| `valor_fora_do_dominio` | 0,000 | `tipo_divergente` |  |
| `estado_da_tela_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A resposta da API retorna uma lista de objetos em vez de um único objeto, o que causa inconsistência na exibição da descrição dos produtos na interface web.
> FONTE: [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: colecao_no_lugar_de_objeto
CAMPO: nenhum
IMPACTO: A resposta da API retorna uma lista de objetos em vez de um único objeto, o que causa inconsistência na exibição da descrição dos produtos na interface web.
FONTE: [contrato-produto]
```

## Rastro

Gerado dos eventos 231 a 252 da trilha; hash dos eventos deste caso: `683e389296e39151` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-5@fixture.md`.
