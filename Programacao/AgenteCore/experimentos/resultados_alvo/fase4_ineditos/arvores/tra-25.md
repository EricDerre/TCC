<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-25`

Caso `tra-25` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/tra-25`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (842 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (842 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3913 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (47,42), `contrato-produto` (44,90) e `contagem_inconsistente` (35,67) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `contagem_inconsistente`; o da entidade, em `entidade-produto`, `contrato-produto` e `contagem_inconsistente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estrutura_aninhada_divergente` (27,17), `chave_de_juncao_errada` (26,45), `pagina-produtos-api` (26,09), `tipo_divergente` (26,06) e `estado_da_tela_divergente` (22,87) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 79 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `contagem_inconsistente`, e o primeiro de fora, `estrutura_aninhada_divergente`, só o texto do caso já punha o primeiro à frente (32,67 contra 24,17), e os reforços em código levaram a diferença a 8,50 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 47,42: 44,42 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 44,90: 41,90 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contagem_inconsistente` | posição 3, pontuação 35,67: 32,67 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 4, pontuação 27,17: 24,17 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 5, pontuação 26,45: 24,45 pelas palavras do caso, mais 2,0 por rota |  |
| `pagina-produtos-api` | posição 6, pontuação 26,09: 24,09 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 7, pontuação 26,06: 23,06 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estado_da_tela_divergente` | posição 8, pontuação 22,87: 22,87 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `resposta_truncada` (Resposta truncada); segunda: `corpo_nao_e_json`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `resposta_truncada` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `corpo_nao_e_json` (Corpo não é JSON), ficou com probabilidade 0,001 contra 0,997 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,002; as maiores: `corpo_vazio` (0,001), `colecao_no_lugar_de_objeto` (0,001) e `campo_ausente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,997, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `contagem_inconsistente` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `contagem_inconsistente`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 7 de 10 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `resposta_truncada` | 0,997 | nenhum | sim |
| `corpo_nao_e_json` | 0,001 | nenhum |  |
| `corpo_vazio` | 0,001 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,001 | `contrato-produto` |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `tipo_divergente` | 0,000 | `entidade-produto` e `contrato-produto` |  |
| `estrutura_aninhada_divergente` | 0,000 | `contagem_inconsistente` |  |
| `contagem_inconsistente` | 0,000 | `contagem_inconsistente` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A interface exibe apenas os dois últimos itens da lista, deixando de mostrar 11 itens importantes.
> FONTE: [contrato-produto] [contagem_inconsistente]

Resposta inteira:

```text
CAUSA_RAIZ: resposta_truncada
CAMPO: nenhum
IMPACTO: A interface exibe apenas os dois últimos itens da lista, deixando de mostrar 11 itens importantes.
FONTE: [contrato-produto] [contagem_inconsistente]
```

## Rastro

Gerado dos eventos 518 a 543 da trilha; hash dos eventos deste caso: `f5c0d6160c72a344` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-25.md`.
