<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-14`

Caso `sin-14` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/sin-14@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (474 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (474 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3588 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (38,92), `contrato-produto` (32,15) e `campo_renomeado` (27,42) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `campo_renomeado`; o da entidade, em `entidade-produto`, `contrato-produto` e `campo_renomeado` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `chave_de_juncao_errada` (19,63), `campo_ausente` (19,42), `tipo_divergente` (15,91), `nulo_inesperado` (13,84) e `valor_fora_do_dominio` (12,70) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 36 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `campo_renomeado`, e o primeiro de fora, `chave_de_juncao_errada`, só o texto do caso já punha o primeiro à frente (24,42 contra 17,63), e os reforços em código levaram a diferença a 7,78 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 38,92: 35,92 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 32,15: 29,15 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_renomeado` | posição 3, pontuação 27,42: 24,42 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `chave_de_juncao_errada` | posição 4, pontuação 19,63: 17,63 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_ausente` | posição 5, pontuação 19,42: 16,42 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tipo_divergente` | posição 6, pontuação 15,91: 12,91 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 7, pontuação 13,84: 11,84 pelas palavras do caso, mais 2,0 por rota |  |
| `valor_fora_do_dominio` | posição 8, pontuação 12,70: 10,70 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)); segunda: `tipo_divergente`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `colecao_no_lugar_de_objeto` (declarado).
- O modelo apontou o campo `imagem_url` (declarado).
- `imagem_url` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,170 contra 0,309 da escolhida; verbetes entregues que a sustentam: `entidade-produto` e `contrato-produto` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,533; as maiores: `resposta_truncada` (0,159), `formato_de_data_divergente` (0,137) e `campo_ausente` (0,090) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,309, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
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
- Conferências em código com veredito: 7 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `colecao_no_lugar_de_objeto` | 0,309 | `contrato-produto` | sim |
| `tipo_divergente` | 0,170 | `entidade-produto` e `contrato-produto` |  |
| `resposta_truncada` | 0,159 | nenhum |  |
| `formato_de_data_divergente` | 0,137 | nenhum |  |
| `campo_ausente` | 0,090 | `contrato-produto` e `campo_renomeado` |  |
| `campo_renomeado` | 0,090 | `contrato-produto` e `campo_renomeado` |  |
| `corpo_nao_e_json` | 0,026 | nenhum |  |
| `corpo_vazio` | 0,026 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,004 | `campo_renomeado` |  |
| `chave_de_juncao_errada` | 0,002 | `entidade-produto` |  |
| `valor_fora_do_dominio` | 0,001 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O ícone de imagem quebrado indica que a URL da imagem está sendo tratada como uma coleção, resultando em erros de exibição.
> FONTE: [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: colecao_no_lugar_de_objeto
CAMPO: imagem_url
IMPACTO: O ícone de imagem quebrado indica que a URL da imagem está sendo tratada como uma coleção, resultando em erros de exibição.
FONTE: [contrato-produto]
```

## Rastro

Gerado dos eventos 932 a 953 da trilha; hash dos eventos deste caso: `ad4d093cb10bd1af` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-14@fixture.md`.
