<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-24`

Caso `tra-24` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/tra-24`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1155 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1155 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4674 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (69,03), `contrato-produto` (52,67) e `chave_de_juncao_errada` (31,12) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `chave_de_juncao_errada`; o da entidade, em `entidade-produto` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `nulo_inesperado` (28,10), `tipo_divergente` (27,76), `estrutura_aninhada_divergente` (27,15), `estado_da_tela_divergente` (25,79) e `campo_renomeado` (24,67) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 88 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `chave_de_juncao_errada`, e o primeiro de fora, `nulo_inesperado`, só o texto do caso já punha o primeiro à frente (29,12 contra 26,10), e os reforços em código levaram a diferença a 3,02 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 69,03: 66,03 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 52,67: 49,67 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `chave_de_juncao_errada` | posição 3, pontuação 31,12: 29,12 pelas palavras do caso, mais 2,0 por rota | sim |
| `nulo_inesperado` | posição 4, pontuação 28,10: 26,10 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 5, pontuação 27,76: 24,76 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 6, pontuação 27,15: 24,15 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estado_da_tela_divergente` | posição 7, pontuação 25,79: 25,79 pelas palavras do caso, sem reforço |  |
| `campo_renomeado` | posição 8, pontuação 24,67: 21,67 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `chave_de_juncao_errada` (Chave de junção errada); segunda: `tipo_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `chave_de_juncao_errada` (declarado).
- O modelo apontou o campo `tipo` (declarado).
- `tipo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,036 contra 0,915 da escolhida; verbetes entregues que a sustentam: `entidade-produto` e `contrato-produto` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,029; as maiores: `colecao_no_lugar_de_objeto` (0,019), `campo_ausente` (0,004) e `campo_renomeado` (0,004) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,915, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
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
| `chave_de_juncao_errada` | 0,915 | `entidade-produto` e `chave_de_juncao_errada` | sim |
| `tipo_divergente` | 0,036 | `entidade-produto` e `contrato-produto` |  |
| `colecao_no_lugar_de_objeto` | 0,019 | `contrato-produto` |  |
| `campo_ausente` | 0,004 | `contrato-produto` |  |
| `campo_renomeado` | 0,004 | `contrato-produto` |  |
| `estrutura_aninhada_divergente` | 0,002 | nenhum |  |
| `resposta_truncada` | 0,001 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `valor_fora_do_dominio` | 0,000 | `chave_de_juncao_errada` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: Os produtos são exibidos com categorias incorretas, misturando itens de diferentes tipos.
> FONTE: [chave_de_juncao_errada]

Resposta inteira:

```text
CAUSA_RAIZ: chave_de_juncao_errada
CAMPO: tipo
IMPACTO: Os produtos são exibidos com categorias incorretas, misturando itens de diferentes tipos.
FONTE: [chave_de_juncao_errada]
```

## Rastro

Gerado dos eventos 495 a 516 da trilha; hash dos eventos deste caso: `f27bc1e9d1758c80` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-24.md`.
