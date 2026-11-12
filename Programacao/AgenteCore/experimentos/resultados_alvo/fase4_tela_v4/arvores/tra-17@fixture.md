<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-17`

Caso `tra-17` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/tra-17@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (586 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (586 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3677 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (54,01), `contrato-produto` (31,76) e `tipo_divergente` (23,79) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `tipo_divergente`; o da entidade, em `entidade-produto`, `contrato-produto` e `tipo_divergente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estrutura_aninhada_divergente` (22,25), `colecao_no_lugar_de_objeto` (20,45), `pagina-produtos-api` (19,73), `estado_da_tela_divergente` (19,25) e `chave_de_juncao_errada` (18,67) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 48 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `tipo_divergente`, e o primeiro de fora, `estrutura_aninhada_divergente`, só o texto do caso já punha o primeiro à frente (20,79 contra 19,25), e os reforços em código levaram a diferença a 1,54 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 54,01: 51,01 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 31,76: 28,76 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tipo_divergente` | posição 3, pontuação 23,79: 20,79 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 4, pontuação 22,25: 19,25 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 5, pontuação 20,45: 17,45 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `pagina-produtos-api` | posição 6, pontuação 19,73: 17,73 pelas palavras do caso, mais 2,0 por rota |  |
| `estado_da_tela_divergente` | posição 7, pontuação 19,25: 19,25 pelas palavras do caso, sem reforço |  |
| `chave_de_juncao_errada` | posição 8, pontuação 18,67: 16,67 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `tipo_divergente` (Tipo divergente); segunda: `campo_ausente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `tipo_divergente` (declarado).
- O modelo apontou o campo `tipo` (declarado).
- `tipo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,074 contra 0,878 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 4 alternativas lidas na resposta somam probabilidade 0,120; as maiores: `campo_renomeado` (0,074), `chave_de_juncao_errada` (0,042) e `valor_fora_do_dominio` (0,002) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,878, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `tipo_divergente` (declarado).
- Verbete citado `tipo_divergente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `entidade-produto`, `contrato-produto` e `tipo_divergente` (conferido).
- Leitura do verbete `tipo_divergente` (Tipo divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tipo_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tipo_divergente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `tipo_divergente` | 0,878 | `entidade-produto`, `contrato-produto` e `tipo_divergente` | sim |
| `campo_ausente` | 0,074 | `contrato-produto` |  |
| `campo_renomeado` | 0,074 | `contrato-produto` |  |
| `chave_de_juncao_errada` | 0,042 | `entidade-produto` |  |
| `valor_fora_do_dominio` | 0,002 | `tipo_divergente` |  |
| `formato_de_data_divergente` | 0,001 | `tipo_divergente` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê a categoria como 'CAR' em vez de 'Carnes'.
> FONTE: [tipo_divergente]

Resposta inteira:

```text
CAUSA_RAIZ: tipo_divergente
CAMPO: tipo
IMPACTO: O usuário vê a categoria como 'CAR' em vez de 'Carnes'.
FONTE: [tipo_divergente]
```

## Rastro

Gerado dos eventos 1888 a 1909 da trilha; hash dos eventos deste caso: `b15a8c1f3c4a51b7` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-17@fixture.md`.
