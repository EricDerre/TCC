<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `efe-3`

Caso `efe-3` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/efe-3@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (463 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (463 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3419 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (43,93), `contrato-produto` (36,12) e `campo_ausente` (24,98) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `campo_ausente`; o da entidade, em `entidade-produto`, `contrato-produto` e `campo_ausente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `chave_de_juncao_errada` (19,70), `campo_renomeado` (17,57), `nulo_inesperado` (15,47), `valor_fora_do_dominio` (15,02) e `tipo_divergente` (14,56) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 33 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `campo_ausente`, e o primeiro de fora, `chave_de_juncao_errada`, só o texto do caso já punha o primeiro à frente (21,98 contra 17,70), e os reforços em código levaram a diferença a 5,28 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 43,93: 40,93 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 36,12: 33,12 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_ausente` | posição 3, pontuação 24,98: 21,98 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `chave_de_juncao_errada` | posição 4, pontuação 19,70: 17,70 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_renomeado` | posição 5, pontuação 17,57: 14,57 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 6, pontuação 15,47: 13,47 pelas palavras do caso, mais 2,0 por rota |  |
| `valor_fora_do_dominio` | posição 7, pontuação 15,02: 13,02 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 8, pontuação 14,56: 11,56 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `campo_ausente` (Campo ausente); segunda: `colecao_no_lugar_de_objeto`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `campo_ausente` (declarado).
- O modelo apontou o campo `imagem` (declarado).
- `imagem` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)), ficou com probabilidade 0,257 contra 0,566 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,196; as maiores: `resposta_truncada` (0,091), `tipo_divergente` (0,040) e `corpo_nao_e_json` (0,027) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,566, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `campo_ausente` (declarado).
- Verbete citado `campo_ausente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-produto` e `campo_ausente` (conferido).
- Leitura do verbete `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `campo_ausente` | 0,566 | `contrato-produto` e `campo_ausente` | sim |
| `colecao_no_lugar_de_objeto` | 0,257 | `contrato-produto` |  |
| `resposta_truncada` | 0,091 | nenhum |  |
| `tipo_divergente` | 0,040 | `entidade-produto` e `contrato-produto` |  |
| `corpo_nao_e_json` | 0,027 | nenhum |  |
| `corpo_vazio` | 0,027 | nenhum |  |
| `formato_de_data_divergente` | 0,008 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,001 | `campo_ausente` |  |
| `campo_renomeado` | 0,001 | `contrato-produto` e `campo_ausente` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: Os cartões aparecem sem foto nenhuma, pois o campo imagem está ausente na resposta.
> FONTE: [campo_ausente]

Resposta inteira:

```text
CAUSA_RAIZ: campo_ausente
CAMPO: imagem
IMPACTO: Os cartões aparecem sem foto nenhuma, pois o campo imagem está ausente na resposta.
FONTE: [campo_ausente]
```

## Rastro

Gerado dos eventos 587 a 608 da trilha; hash dos eventos deste caso: `bca09de578611d85` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/efe-3@fixture.md`.
