<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-8`

Caso `tra-8` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/tra-8@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (528 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (528 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3713 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contagem_inconsistente` (42,50), `entidade-produto` (38,95) e `estrutura_aninhada_divergente` (34,86) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contagem_inconsistente`, `entidade-produto` e `estrutura_aninhada_divergente`; o da entidade, em `contagem_inconsistente`, `entidade-produto` e `estrutura_aninhada_divergente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `contrato-produto` (30,01), `valor_fora_do_dominio` (17,84), `colecao_no_lugar_de_objeto` (16,83), `tipo_divergente` (16,80) e `nulo_inesperado` (15,22) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 38 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `estrutura_aninhada_divergente`, e o primeiro de fora, `contrato-produto`, só o texto do caso já punha o primeiro à frente (31,86 contra 27,01), e os reforços em código levaram a diferença a 4,85 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contagem_inconsistente` | posição 1, pontuação 42,50: 39,50 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 2, pontuação 38,95: 35,95 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 3, pontuação 34,86: 31,86 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 4, pontuação 30,01: 27,01 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `valor_fora_do_dominio` | posição 5, pontuação 17,84: 15,84 pelas palavras do caso, mais 2,0 por rota |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 16,83: 13,83 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tipo_divergente` | posição 7, pontuação 16,80: 13,80 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 8, pontuação 15,22: 13,22 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `contagem_inconsistente` (Contagem inconsistente); segunda: `estrutura_aninhada_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `contagem_inconsistente` (declarado).
- O modelo apontou o campo `total` (declarado).
- `total` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `estrutura_aninhada_divergente` (Estrutura aninhada divergente), ficou com probabilidade 0,011 contra 0,976 da escolhida; verbetes entregues que a sustentam: `contagem_inconsistente` e `estrutura_aninhada_divergente` (observado).
- As outras 10 alternativas lidas na resposta somam probabilidade 0,006; as maiores: `campo_ausente` (0,002), `campo_renomeado` (0,002) e `resposta_truncada` (0,001) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,976, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos?pagina=1`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contagem_inconsistente` (declarado).
- Verbete citado `contagem_inconsistente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contagem_inconsistente` e `estrutura_aninhada_divergente` (conferido).
- Leitura do verbete `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `contagem_inconsistente` | 0,976 | `contagem_inconsistente` e `estrutura_aninhada_divergente` | sim |
| `estrutura_aninhada_divergente` | 0,011 | `contagem_inconsistente` e `estrutura_aninhada_divergente` |  |
| `campo_ausente` | 0,002 | nenhum |  |
| `campo_renomeado` | 0,002 | `estrutura_aninhada_divergente` |  |
| `resposta_truncada` | 0,001 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `estado_da_tela_divergente` | 0,000 | `contagem_inconsistente` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `tipo_divergente` | 0,000 | `entidade-produto` |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A tela exibe cartões com um produto, mas informa 'Nenhum produto encontrado' devido à contagem inconsistente no total.
> FONTE: [contagem_inconsistente]

Resposta inteira:

```text
CAUSA_RAIZ: contagem_inconsistente
CAMPO: total
IMPACTO: A tela exibe cartões com um produto, mas informa 'Nenhum produto encontrado' devido à contagem inconsistente no total.
FONTE: [contagem_inconsistente]
```

## Rastro

Gerado dos eventos 1167 a 1188 da trilha; hash dos eventos deste caso: `9fb23feb88950c4b` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-8@fixture.md`.
