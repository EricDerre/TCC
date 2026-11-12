<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-20`

Caso `tra-20` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/tra-20@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (985 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (985 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4504 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (60,67), `contrato-produto` (45,84) e `chave_de_juncao_errada` (45,36) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `chave_de_juncao_errada`; o da entidade, em `entidade-produto` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `tipo_divergente` (34,59), `contrato-pedido` (27,97), `valor_fora_do_dominio` (25,31), `colecao_no_lugar_de_objeto` (24,88) e `nulo_inesperado` (24,87) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 91 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `chave_de_juncao_errada`, e o primeiro de fora, `tipo_divergente`, só o texto do caso já punha o primeiro à frente (43,36 contra 31,59), e os reforços em código levaram a diferença a 10,77 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 60,67: 57,67 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 45,84: 42,84 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `chave_de_juncao_errada` | posição 3, pontuação 45,36: 43,36 pelas palavras do caso, mais 2,0 por rota | sim |
| `tipo_divergente` | posição 4, pontuação 34,59: 31,59 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `contrato-pedido` | posição 5, pontuação 27,97: 27,97 pelas palavras do caso, sem reforço |  |
| `valor_fora_do_dominio` | posição 6, pontuação 25,31: 23,31 pelas palavras do caso, mais 2,0 por rota |  |
| `colecao_no_lugar_de_objeto` | posição 7, pontuação 24,88: 21,88 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 8, pontuação 24,87: 22,87 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `chave_de_juncao_errada` (Chave de junção errada); segunda: `campo_ausente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `chave_de_juncao_errada` (declarado).
- O modelo apontou o campo `tipo` (declarado).
- `tipo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,001 contra 0,997 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,002; as maiores: `campo_renomeado` (0,001), `tipo_divergente` (0,001) e `valor_fora_do_dominio` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,997, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `chave_de_juncao_errada` (declarado).
- Verbete citado `chave_de_juncao_errada`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `entidade-produto` e `chave_de_juncao_errada` (conferido).
- Leitura do verbete `chave_de_juncao_errada` (Chave de junção errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/chave_de_juncao_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/chave_de_juncao_errada.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `chave_de_juncao_errada` | 0,997 | `entidade-produto` e `chave_de_juncao_errada` | sim |
| `campo_ausente` | 0,001 | `contrato-produto` |  |
| `campo_renomeado` | 0,001 | `contrato-produto` |  |
| `tipo_divergente` | 0,001 | `entidade-produto` e `contrato-produto` |  |
| `valor_fora_do_dominio` | 0,000 | `chave_de_juncao_errada` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `registro_duplicado` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: Os produtos Fraldinha e Costelona, que são cortes de carne, aparecem incorretamente na categoria Sobremesas na interface web.
> FONTE: [chave_de_juncao_errada]

Resposta inteira:

```text
CAUSA_RAIZ: chave_de_juncao_errada
CAMPO: tipo
IMPACTO: Os produtos Fraldinha e Costelona, que são cortes de carne, aparecem incorretamente na categoria Sobremesas na interface web.
FONTE: [chave_de_juncao_errada]
```

## Rastro

Gerado dos eventos 2003 a 2024 da trilha; hash dos eventos deste caso: `b38bacc68d54d8f3` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-20@fixture.md`.
