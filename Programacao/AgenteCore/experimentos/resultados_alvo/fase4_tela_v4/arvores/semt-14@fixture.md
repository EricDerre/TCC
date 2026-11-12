<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `semt-14`

Caso `semt-14` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/semt-14@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (594 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (594 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3495 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (57,23), `contrato-produto` (48,41) e `nulo_inesperado` (43,04) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `nulo_inesperado`; o da entidade, em `entidade-produto` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `chave_de_juncao_errada` (26,77), `tipo_divergente` (25,28), `valor_fora_do_dominio` (22,24), `estrutura_aninhada_divergente` (20,43) e `campo_renomeado` (20,09) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 49 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `nulo_inesperado`, e o primeiro de fora, `chave_de_juncao_errada`, só o texto do caso já punha o primeiro à frente (41,04 contra 24,77), e os reforços em código levaram a diferença a 16,27 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 57,23: 54,23 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 48,41: 45,41 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `nulo_inesperado` | posição 3, pontuação 43,04: 41,04 pelas palavras do caso, mais 2,0 por rota | sim |
| `chave_de_juncao_errada` | posição 4, pontuação 26,77: 24,77 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 5, pontuação 25,28: 22,28 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `valor_fora_do_dominio` | posição 6, pontuação 22,24: 20,24 pelas palavras do caso, mais 2,0 por rota |  |
| `estrutura_aninhada_divergente` | posição 7, pontuação 20,43: 17,43 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_renomeado` | posição 8, pontuação 20,09: 17,09 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `nulo_inesperado` (Nulo inesperado); segunda: `tipo_divergente`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `nulo_inesperado` (declarado).
- O modelo apontou o campo `tipo` (declarado).
- `tipo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,250 contra 0,740 da escolhida; verbetes entregues que a sustentam: `entidade-produto` e `contrato-produto` (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,015; as maiores: `campo_ausente` (0,006), `campo_renomeado` (0,006) e `valor_fora_do_dominio` (0,002) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,740, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `nulo_inesperado` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `nulo_inesperado`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `contrato-produto` não confere; `nulo_inesperado` confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `nulo_inesperado` (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 10 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `nulo_inesperado` | 0,740 | `nulo_inesperado` | sim |
| `tipo_divergente` | 0,250 | `entidade-produto` e `contrato-produto` |  |
| `campo_ausente` | 0,006 | `contrato-produto` e `nulo_inesperado` |  |
| `campo_renomeado` | 0,006 | `contrato-produto` |  |
| `valor_fora_do_dominio` | 0,002 | `nulo_inesperado` |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` e `nulo_inesperado` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `resposta_truncada` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O filtro por categoria não exibe corretamente os produtos, pois alguns tipos estão ausentes na resposta.
> FONTE: [contrato-produto], [nulo_inesperado]

Resposta inteira:

```text
CAUSA_RAIZ: nulo_inesperado
CAMPO: tipo
IMPACTO: O filtro por categoria não exibe corretamente os produtos, pois alguns tipos estão ausentes na resposta.
FONTE: [contrato-produto], [nulo_inesperado]
```

## Rastro

Gerado dos eventos 1112 a 1137 da trilha; hash dos eventos deste caso: `3f5602e433b7efb2` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/semt-14@fixture.md`.
