<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `semt-23`

Caso `semt-23` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/semt-23`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (706 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (706 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3797 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (43,80), `contrato-produto` (42,09) e `tipo_divergente` (29,90) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `tipo_divergente`; o da entidade, em `entidade-produto`, `contrato-produto` e `tipo_divergente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `nulo_inesperado` (27,67), `pagina-produtos-api` (24,66), `chave_de_juncao_errada` (23,28), `valor_fora_do_dominio` (23,20) e `estrutura_aninhada_divergente` (23,06) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 63 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `tipo_divergente`, e o primeiro de fora, `nulo_inesperado`, só o texto do caso já punha o primeiro à frente (26,90 contra 25,67), e os reforços em código levaram a diferença a 2,23 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 43,80: 40,80 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 42,09: 39,09 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tipo_divergente` | posição 3, pontuação 29,90: 26,90 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `nulo_inesperado` | posição 4, pontuação 27,67: 25,67 pelas palavras do caso, mais 2,0 por rota |  |
| `pagina-produtos-api` | posição 5, pontuação 24,66: 22,66 pelas palavras do caso, mais 2,0 por rota |  |
| `chave_de_juncao_errada` | posição 6, pontuação 23,28: 21,28 pelas palavras do caso, mais 2,0 por rota |  |
| `valor_fora_do_dominio` | posição 7, pontuação 23,20: 21,20 pelas palavras do caso, mais 2,0 por rota |  |
| `estrutura_aninhada_divergente` | posição 8, pontuação 23,06: 20,06 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `tipo_divergente` (Tipo divergente); segunda: `valor_fora_do_dominio`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `tipo_divergente` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `valor_fora_do_dominio` (Valor fora do domínio), ficou com probabilidade 0,057 contra 0,908 da escolhida; verbetes entregues que a sustentam: `tipo_divergente` (observado).
- As outras 5 alternativas lidas na resposta somam probabilidade 0,024; as maiores: `colecao_no_lugar_de_objeto` (0,022), `campo_ausente` (0,001) e `campo_renomeado` (0,001) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,908, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `entidade-produto` e `contrato-produto` (declarado).
- Os 2 verbetes citados (`entidade-produto` e `contrato-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `entidade-produto`, `contrato-produto` e `tipo_divergente` (conferido).
- Camada de leitura de cada verbete citado: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 9 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `tipo_divergente` | 0,908 | `entidade-produto`, `contrato-produto` e `tipo_divergente` | sim |
| `valor_fora_do_dominio` | 0,057 | `tipo_divergente` |  |
| `colecao_no_lugar_de_objeto` | 0,022 | `contrato-produto` |  |
| `campo_ausente` | 0,001 | `contrato-produto` |  |
| `campo_renomeado` | 0,001 | `contrato-produto` |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` e `tipo_divergente` |  |
| `formato_de_data_divergente` | 0,000 | `tipo_divergente` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: Os usuários vêem valores negativos no preço dos produtos, como 'R$ -80,90' e 'R$ -75,90', que são incorretos e não refletem os preços reais.
> FONTE: [entidade-produto], [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: tipo_divergente
CAMPO: preco
IMPACTO: Os usuários vêem valores negativos no preço dos produtos, como 'R$ -80,90' e 'R$ -75,90', que são incorretos e não refletem os preços reais.
FONTE: [entidade-produto], [contrato-produto]
```

## Rastro

Gerado dos eventos 322 a 347 da trilha; hash dos eventos deste caso: `b48e48f9d7ba6734` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/semt-23.md`.
