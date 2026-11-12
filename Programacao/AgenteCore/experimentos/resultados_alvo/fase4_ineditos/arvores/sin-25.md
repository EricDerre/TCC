<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-25`

Caso `sin-25` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/sin-25`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (551 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (551 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3865 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `colecao_no_lugar_de_objeto` (36,47), `contrato-produto` (32,54) e `entidade-produto` (28,31) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `colecao_no_lugar_de_objeto`, `contrato-produto` e `entidade-produto`; o da entidade, em `colecao_no_lugar_de_objeto`, `contrato-produto` e `entidade-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `tipo_divergente` (23,76), `pagina-produtos-api` (23,35), `estrutura_aninhada_divergente` (21,74), `chave_de_juncao_errada` (21,07) e `estado_da_tela_divergente` (20,77) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 49 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `tipo_divergente`, só o texto do caso já punha o primeiro à frente (25,31 contra 22,76), e os reforços em código levaram a diferença a 4,55 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `colecao_no_lugar_de_objeto` | posição 1, pontuação 36,47: 33,47 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 32,54: 29,54 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 3, pontuação 28,31: 25,31 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tipo_divergente` | posição 4, pontuação 23,76: 22,76 pelas palavras do caso, mais 1,0 por entidade |  |
| `pagina-produtos-api` | posição 5, pontuação 23,35: 21,35 pelas palavras do caso, mais 2,0 por rota |  |
| `estrutura_aninhada_divergente` | posição 6, pontuação 21,74: 20,74 pelas palavras do caso, mais 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 7, pontuação 21,07: 21,07 pelas palavras do caso, sem reforço |  |
| `estado_da_tela_divergente` | posição 8, pontuação 20,77: 20,77 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)); segunda: `tipo_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `colecao_no_lugar_de_objeto` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 0,994 da escolhida; verbetes entregues que a sustentam: `contrato-produto` e `entidade-produto` (observado).
- As outras 7 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `campo_renomeado` (0,000) e `corpo_nao_e_json` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,994, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/4`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `colecao_no_lugar_de_objeto` (declarado).
- Verbete citado `colecao_no_lugar_de_objeto`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `colecao_no_lugar_de_objeto` e `contrato-produto` (conferido).
- Leitura do verbete `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/colecao_no_lugar_de_objeto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/colecao_no_lugar_de_objeto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `colecao_no_lugar_de_objeto` | 0,994 | `colecao_no_lugar_de_objeto` e `contrato-produto` | sim |
| `tipo_divergente` | 0,000 | `contrato-produto` e `entidade-produto` |  |
| `campo_ausente` | 0,000 | `colecao_no_lugar_de_objeto` e `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,000 | `colecao_no_lugar_de_objeto` |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um modal com título e texto incorretos, pois a resposta contém uma coleção em vez de um único objeto.
> FONTE: [colecao_no_lugar_de_objeto]

Resposta inteira:

```text
CAUSA_RAIZ: colecao_no_lugar_de_objeto
CAMPO: id
IMPACTO: O usuário vê um modal com título e texto incorretos, pois a resposta contém uma coleção em vez de um único objeto.
FONTE: [colecao_no_lugar_de_objeto]
```

## Rastro

Gerado dos eventos 226 a 247 da trilha; hash dos eventos deste caso: `d5321028273d3d0e` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-25.md`.
