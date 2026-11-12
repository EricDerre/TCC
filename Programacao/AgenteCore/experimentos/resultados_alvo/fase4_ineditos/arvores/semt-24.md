<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `semt-24`

Caso `semt-24` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/semt-24`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (750 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (750 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3841 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (82,62), `tipo_divergente` (72,20) e `contrato-produto` (71,62) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `tipo_divergente` e `contrato-produto`; o da entidade, em `entidade-produto`, `tipo_divergente` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `valor_fora_do_dominio` (57,36), `estrutura_aninhada_divergente` (32,64), `chave_de_juncao_errada` (25,21), `nulo_inesperado` (24,27) e `colecao_no_lugar_de_objeto` (20,15) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 66 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `valor_fora_do_dominio`, só o texto do caso já punha o primeiro à frente (68,62 contra 55,36), e os reforços em código levaram a diferença a 14,26 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 82,62: 79,62 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tipo_divergente` | posição 2, pontuação 72,20: 69,20 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 71,62: 68,62 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `valor_fora_do_dominio` | posição 4, pontuação 57,36: 55,36 pelas palavras do caso, mais 2,0 por rota |  |
| `estrutura_aninhada_divergente` | posição 5, pontuação 32,64: 29,64 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 6, pontuação 25,21: 23,21 pelas palavras do caso, mais 2,0 por rota |  |
| `nulo_inesperado` | posição 7, pontuação 24,27: 22,27 pelas palavras do caso, mais 2,0 por rota |  |
| `colecao_no_lugar_de_objeto` | posição 8, pontuação 20,15: 17,15 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `tipo_divergente` (Tipo divergente); segunda: `campo_ausente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `tipo_divergente` (declarado).
- O modelo apontou o campo `destaque` (declarado).
- `destaque` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,003 contra 0,995 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 5 alternativas lidas na resposta somam probabilidade 0,004; as maiores: `campo_renomeado` (0,003), `valor_fora_do_dominio` (0,001) e `formato_de_data_divergente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,995, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `tipo_divergente` (declarado).
- Verbete citado `tipo_divergente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `entidade-produto`, `tipo_divergente` e `contrato-produto` (conferido).
- Leitura do verbete `tipo_divergente` (Tipo divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tipo_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tipo_divergente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `tipo_divergente` | 0,995 | `entidade-produto`, `tipo_divergente` e `contrato-produto` | sim |
| `campo_ausente` | 0,003 | `contrato-produto` |  |
| `campo_renomeado` | 0,003 | `contrato-produto` |  |
| `valor_fora_do_dominio` | 0,001 | `tipo_divergente` |  |
| `formato_de_data_divergente` | 0,000 | `tipo_divergente` |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê "destaque: True" e "destaque: False" em inglês, em vez de "destaque: Sim" e "destaque: Não".
> FONTE: [tipo_divergente]

Resposta inteira:

```text
CAUSA_RAIZ: tipo_divergente
CAMPO: destaque
IMPACTO: O usuário vê "destaque: True" e "destaque: False" em inglês, em vez de "destaque: Sim" e "destaque: Não".
FONTE: [tipo_divergente]
```

## Rastro

Gerado dos eventos 349 a 370 da trilha; hash dos eventos deste caso: `189e3de5ace07d9d` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/semt-24.md`.
