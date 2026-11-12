<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-11`

Caso `tra-11` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/tra-11@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (391 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (391 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3494 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contagem_inconsistente` (47,84), `estrutura_aninhada_divergente` (22,43) e `tempo_de_resposta_excedido` (13,69) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contagem_inconsistente`, `estrutura_aninhada_divergente` e `tempo_de_resposta_excedido`; o da entidade, em `contagem_inconsistente` e `estrutura_aninhada_divergente`; o do status, em `tempo_de_resposta_excedido` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `dado_desatualizado` (13,31), `entidade-produto` (12,26), `escala_ou_unidade_errada` (10,25), `campo_renomeado` (8,66) e `colecao_no_lugar_de_objeto` (8,46) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 23 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `tempo_de_resposta_excedido`, e o primeiro de fora, `dado_desatualizado`, só o texto do caso já punha o primeiro à frente (10,69 contra 10,31), e os reforços em código levaram a diferença a 0,37 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contagem_inconsistente` | posição 1, pontuação 47,84: 44,84 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 2, pontuação 22,43: 19,43 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tempo_de_resposta_excedido` | posição 3, pontuação 13,69: 10,69 pelas palavras do caso, mais 2,0 por rota e 1,0 por status | sim |
| `dado_desatualizado` | posição 4, pontuação 13,31: 10,31 pelas palavras do caso, mais 2,0 por rota e 1,0 por status |  |
| `entidade-produto` | posição 5, pontuação 12,26: 9,26 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `escala_ou_unidade_errada` | posição 6, pontuação 10,25: 7,25 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_renomeado` | posição 7, pontuação 8,66: 5,66 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 8, pontuação 8,46: 5,46 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `contagem_inconsistente` (Contagem inconsistente); segunda: `estrutura_aninhada_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `contagem_inconsistente` (declarado).
- O modelo apontou o campo `itens` (declarado).
- `itens` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `estrutura_aninhada_divergente` (Estrutura aninhada divergente), ficou com probabilidade 0,000 contra 0,979 da escolhida; verbetes entregues que a sustentam: `contagem_inconsistente` e `estrutura_aninhada_divergente` (observado).
- As outras 6 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `campo_renomeado` (0,000) e `corpo_nao_e_json` (0,000) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,979, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos?pagina=2`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contagem_inconsistente` (declarado).
- Verbete citado `contagem_inconsistente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contagem_inconsistente` e `estrutura_aninhada_divergente` (conferido).
- Leitura do verbete `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `contagem_inconsistente` | 0,979 | `contagem_inconsistente` e `estrutura_aninhada_divergente` | sim |
| `estrutura_aninhada_divergente` | 0,000 | `contagem_inconsistente` e `estrutura_aninhada_divergente` |  |
| `campo_ausente` | 0,000 | nenhum |  |
| `campo_renomeado` | 0,000 | `estrutura_aninhada_divergente` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | `tempo_de_resposta_excedido` |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `estado_da_tela_divergente` | 0,000 | `contagem_inconsistente` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê uma segunda página vazia, enquanto o total de produtos é de 14.
> FONTE: [contagem_inconsistente]

Resposta inteira:

```text
CAUSA_RAIZ: contagem_inconsistente
CAMPO: itens
IMPACTO: O usuário vê uma segunda página vazia, enquanto o total de produtos é de 14.
FONTE: [contagem_inconsistente]
```

## Rastro

Gerado dos eventos 1220 a 1241 da trilha; hash dos eventos deste caso: `32c2b849720dbe49` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-11@fixture.md`.
