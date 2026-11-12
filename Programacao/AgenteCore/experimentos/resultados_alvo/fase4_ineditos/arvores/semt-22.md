<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `semt-22`

Caso `semt-22` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/semt-22`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (645 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (645 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3546 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `nulo_inesperado` (67,67), `contrato-produto` (54,56) e `entidade-produto` (50,25) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `nulo_inesperado`, `contrato-produto` e `entidade-produto`; o da entidade, em `contrato-produto` e `entidade-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `campo_renomeado` (23,56), `tipo_divergente` (21,84), `pagina-produtos-api` (21,73), `valor_fora_do_dominio` (21,59) e `chave_de_juncao_errada` (21,50) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 59 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `campo_renomeado`, só o texto do caso já punha o primeiro à frente (47,25 contra 20,56), e os reforços em código levaram a diferença a 26,69 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `nulo_inesperado` | posição 1, pontuação 67,67: 65,67 pelas palavras do caso, mais 2,0 por rota | sim |
| `contrato-produto` | posição 2, pontuação 54,56: 51,56 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 3, pontuação 50,25: 47,25 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_renomeado` | posição 4, pontuação 23,56: 20,56 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tipo_divergente` | posição 5, pontuação 21,84: 18,84 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `pagina-produtos-api` | posição 6, pontuação 21,73: 19,73 pelas palavras do caso, mais 2,0 por rota |  |
| `valor_fora_do_dominio` | posição 7, pontuação 21,59: 19,59 pelas palavras do caso, mais 2,0 por rota |  |
| `chave_de_juncao_errada` | posição 8, pontuação 21,50: 19,50 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `nulo_inesperado` (Nulo inesperado); segunda: `tipo_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `nulo_inesperado` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 0,999 da escolhida; verbetes entregues que a sustentam: `contrato-produto` e `entidade-produto` (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `campo_renomeado` (0,000) e `valor_fora_do_dominio` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,999, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `nulo_inesperado` (declarado).
- Verbete citado `nulo_inesperado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `nulo_inesperado` (conferido).
- Leitura do verbete `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `nulo_inesperado` | 0,999 | `nulo_inesperado` | sim |
| `tipo_divergente` | 0,000 | `contrato-produto` e `entidade-produto` |  |
| `campo_ausente` | 0,000 | `nulo_inesperado` e `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `valor_fora_do_dominio` | 0,000 | `nulo_inesperado` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O preço dos produtos não é exibido corretamente na interface, mostrando 'R$ 0,00' para todos os itens, pois os preços retornados da API são nulos.
> FONTE: [nulo_inesperado]

Resposta inteira:

```text
CAUSA_RAIZ: nulo_inesperado
CAMPO: preco
IMPACTO: O preço dos produtos não é exibido corretamente na interface, mostrando 'R$ 0,00' para todos os itens, pois os preços retornados da API são nulos.
FONTE: [nulo_inesperado]
```

## Rastro

Gerado dos eventos 299 a 320 da trilha; hash dos eventos deste caso: `66f4ad34b6aaeda1` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/semt-22.md`.
