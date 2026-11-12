<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-23`

Caso `sin-23` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/sin-23`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (512 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (512 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3626 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-produto` (30,62), `campo_renomeado` (27,94) e `entidade-produto` (26,39) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto` e `entidade-produto`; o da entidade, em `contrato-produto`, `campo_renomeado` e `entidade-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `campo_ausente` (22,44), `tipo_divergente` (17,37), `colecao_no_lugar_de_objeto` (17,12), `chave_de_juncao_errada` (16,15) e `pagina-produtos-api` (12,62) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 40 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `campo_ausente`, só o texto do caso já punha o primeiro à frente (23,39 contra 21,44), e os reforços em código levaram a diferença a 3,95 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-produto` | posição 1, pontuação 30,62: 27,62 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_renomeado` | posição 2, pontuação 27,94: 26,94 pelas palavras do caso, mais 1,0 por entidade | sim |
| `entidade-produto` | posição 3, pontuação 26,39: 23,39 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_ausente` | posição 4, pontuação 22,44: 21,44 pelas palavras do caso, mais 1,0 por entidade |  |
| `tipo_divergente` | posição 5, pontuação 17,37: 16,37 pelas palavras do caso, mais 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 17,12: 14,12 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 7, pontuação 16,15: 16,15 pelas palavras do caso, sem reforço |  |
| `pagina-produtos-api` | posição 8, pontuação 12,62: 10,62 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `campo_renomeado` (Campo renomeado); segunda: `tipo_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `campo_renomeado` (declarado).
- O modelo apontou o campo `resumo` (declarado).
- `resumo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 0,999 da escolhida; verbetes entregues que a sustentam: `contrato-produto` e `entidade-produto` (observado).
- As outras 7 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `chave_de_juncao_errada` (0,000) e `resposta_truncada` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,999, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/10`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `campo_renomeado` (declarado).
- Verbete citado `campo_renomeado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-produto` e `campo_renomeado` (conferido).
- Leitura do verbete `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `campo_renomeado` | 0,999 | `contrato-produto` e `campo_renomeado` | sim |
| `tipo_divergente` | 0,000 | `contrato-produto` e `entidade-produto` |  |
| `campo_ausente` | 0,000 | `contrato-produto` e `campo_renomeado` |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `dado_desatualizado` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O campo resumo foi renomeado para resumo_v2, mas a interface espera resumo, resultando em uma descrição não exibida corretamente.
> FONTE: [campo_renomeado]

Resposta inteira:

```text
CAUSA_RAIZ: campo_renomeado
CAMPO: resumo
IMPACTO: O campo resumo foi renomeado para resumo_v2, mas a interface espera resumo, resultando em uma descrição não exibida corretamente.
FONTE: [campo_renomeado]
```

## Rastro

Gerado dos eventos 176 a 197 da trilha; hash dos eventos deste caso: `0354be1bfb1f8a66` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-23.md`.
