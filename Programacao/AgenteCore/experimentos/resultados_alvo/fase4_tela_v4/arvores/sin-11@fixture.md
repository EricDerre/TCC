<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-11`

Caso `sin-11` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/sin-11@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (491 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (491 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3676 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (37,10), `estrutura_aninhada_divergente` (32,35) e `contagem_inconsistente` (26,97) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `estrutura_aninhada_divergente` e `contagem_inconsistente`; o da entidade, em `entidade-produto`, `estrutura_aninhada_divergente` e `contagem_inconsistente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `contrato-produto` (25,86), `pagina-produtos-api` (15,07), `tipo_divergente` (14,98), `escala_ou_unidade_errada` (13,64) e `nulo_inesperado` (13,57) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 34 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `contagem_inconsistente`, e o primeiro de fora, `contrato-produto`, só o texto do caso já punha o primeiro à frente (23,97 contra 22,86), e os reforços em código levaram a diferença a 1,10 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 37,10: 34,10 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 2, pontuação 32,35: 29,35 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contagem_inconsistente` | posição 3, pontuação 26,97: 23,97 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 4, pontuação 25,86: 22,86 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `pagina-produtos-api` | posição 5, pontuação 15,07: 13,07 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 6, pontuação 14,98: 11,98 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `escala_ou_unidade_errada` | posição 7, pontuação 13,64: 10,64 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 8, pontuação 13,57: 11,57 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `estrutura_aninhada_divergente` (Estrutura aninhada divergente); segunda: `campo_ausente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `estrutura_aninhada_divergente` (declarado).
- O modelo apontou o campo `itens` (declarado).
- `itens` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,000 contra 1,000 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_renomeado` (0,000), `corpo_nao_e_json` (0,000) e `corpo_vazio` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 1,000, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `estrutura_aninhada_divergente` (declarado).
- Verbete citado `estrutura_aninhada_divergente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `estrutura_aninhada_divergente` e `contagem_inconsistente` (conferido).
- Leitura do verbete `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `estrutura_aninhada_divergente` | 1,000 | `estrutura_aninhada_divergente` e `contagem_inconsistente` | sim |
| `campo_ausente` | 0,000 | nenhum |  |
| `campo_renomeado` | 0,000 | `estrutura_aninhada_divergente` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `estrutura_aninhada_divergente` |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `tipo_divergente` | 0,000 | `entidade-produto` |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A interface web espera uma lista direta de produtos, mas recebe um objeto aninhado com uma chave "itens" contendo a lista, resultando em uma listagem vazia.
> FONTE: [estrutura_aninhada_divergente]

Resposta inteira:

```text
CAUSA_RAIZ: estrutura_aninhada_divergente
CAMPO: itens
IMPACTO: A interface web espera uma lista direta de produtos, mas recebe um objeto aninhado com uma chave "itens" contendo a lista, resultando em uma listagem vazia.
FONTE: [estrutura_aninhada_divergente]
```

## Rastro

Gerado dos eventos 873 a 894 da trilha; hash dos eventos deste caso: `51c93d7e9fee7ebf` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-11@fixture.md`.
