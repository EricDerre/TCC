<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `semt-27`

Caso `semt-27` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/semt-27`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (933 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (933 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4108 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (93,01), `contrato-produto` (51,37) e `estrutura_aninhada_divergente` (36,07) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `estrutura_aninhada_divergente`; o da entidade, em `entidade-produto`, `contrato-produto` e `estrutura_aninhada_divergente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (34,14), `estado_da_tela_divergente` (32,72), `contagem_inconsistente` (28,73), `valor_fora_do_dominio` (27,98) e `tipo_divergente` (27,85) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 87 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `estrutura_aninhada_divergente`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (33,07 contra 32,14), e os reforços em código levaram a diferença a 1,93 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 93,01: 90,01 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 51,37: 48,37 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 3, pontuação 36,07: 33,07 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pagina-produtos-api` | posição 4, pontuação 34,14: 32,14 pelas palavras do caso, mais 2,0 por rota |  |
| `estado_da_tela_divergente` | posição 5, pontuação 32,72: 32,72 pelas palavras do caso, sem reforço |  |
| `contagem_inconsistente` | posição 6, pontuação 28,73: 25,73 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `valor_fora_do_dominio` | posição 7, pontuação 27,98: 25,98 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 8, pontuação 27,85: 24,85 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)); segunda: `campo_ausente`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `colecao_no_lugar_de_objeto` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,177 contra 0,645 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 11 alternativas lidas na resposta somam probabilidade 0,351; as maiores: `campo_renomeado` (0,177), `resposta_truncada` (0,074) e `tipo_divergente` (0,049) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,645, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` (declarado).
- Verbete citado `contrato-produto`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), não traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-produto` e `estrutura_aninhada_divergente` (conferido).
- Leitura do verbete `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `colecao_no_lugar_de_objeto` | 0,645 | `contrato-produto` e `estrutura_aninhada_divergente` | sim |
| `campo_ausente` | 0,177 | `contrato-produto` |  |
| `campo_renomeado` | 0,177 | `contrato-produto` e `estrutura_aninhada_divergente` |  |
| `resposta_truncada` | 0,074 | nenhum |  |
| `tipo_divergente` | 0,049 | `entidade-produto` e `contrato-produto` |  |
| `estrutura_aninhada_divergente` | 0,036 | `estrutura_aninhada_divergente` |  |
| `corpo_nao_e_json` | 0,005 | nenhum |  |
| `corpo_vazio` | 0,005 | nenhum |  |
| `valor_fora_do_dominio` | 0,004 | nenhum |  |
| `chave_de_juncao_errada` | 0,001 | `entidade-produto` |  |
| `estado_da_tela_divergente` | 0,001 | nenhum |  |
| `formato_de_data_divergente` | 0,001 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um erro ao tentar acessar detalhes de um produto específico, pois a requisição GET está sendo feita com um ID inválido (-2 e -3) em vez do ID correto do produto.
> FONTE: [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: colecao_no_lugar_de_objeto
CAMPO: id
IMPACTO: O usuário vê um erro ao tentar acessar detalhes de um produto específico, pois a requisição GET está sendo feita com um ID inválido (-2 e -3) em vez do ID correto do produto.
FONTE: [contrato-produto]
```

## Rastro

Gerado dos eventos 418 a 439 da trilha; hash dos eventos deste caso: `67b8a5451d5833dc` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/semt-27.md`.
