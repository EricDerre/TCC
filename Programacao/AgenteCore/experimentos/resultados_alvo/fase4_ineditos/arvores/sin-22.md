<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-22`

Caso `sin-22` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/sin-22`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (665 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (665 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3621 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (46,49), `contrato-produto` (45,93) e `campo_ausente` (34,45) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `campo_ausente`; o da entidade, em `entidade-produto`, `contrato-produto` e `campo_ausente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `campo_renomeado` (26,42), `chave_de_juncao_errada` (26,07), `campo_preco_ausente` (25,59), `tipo_divergente` (21,84) e `nulo_inesperado` (21,78) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 56 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `campo_ausente`, e o primeiro de fora, `campo_renomeado`, só o texto do caso já punha o primeiro à frente (31,45 contra 23,42), e os reforços em código levaram a diferença a 8,03 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 46,49: 43,49 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 45,93: 42,93 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_ausente` | posição 3, pontuação 34,45: 31,45 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_renomeado` | posição 4, pontuação 26,42: 23,42 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 5, pontuação 26,07: 24,07 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_preco_ausente` | posição 6, pontuação 25,59: 24,59 pelas palavras do caso, mais 1,0 por entidade |  |
| `tipo_divergente` | posição 7, pontuação 21,84: 18,84 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 8, pontuação 21,78: 19,78 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `campo_ausente` (Campo ausente); segunda: `colecao_no_lugar_de_objeto`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `campo_ausente` (declarado).
- O modelo apontou o campo `nome` (declarado).
- `nome` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)), ficou com probabilidade 0,046 contra 0,944 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 7 alternativas lidas na resposta somam probabilidade 0,009; as maiores: `corpo_nao_e_json` (0,003), `corpo_vazio` (0,003) e `tipo_divergente` (0,002) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,944, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
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
| `campo_ausente` | 0,944 | `contrato-produto` e `campo_ausente` | sim |
| `colecao_no_lugar_de_objeto` | 0,046 | `contrato-produto` |  |
| `corpo_nao_e_json` | 0,003 | nenhum |  |
| `corpo_vazio` | 0,003 | nenhum |  |
| `tipo_divergente` | 0,002 | `entidade-produto` e `contrato-produto` |  |
| `resposta_truncada` | 0,001 | nenhum |  |
| `campo_renomeado` | 0,000 | `contrato-produto` e `campo_ausente` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,000 | `campo_ausente` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O título dos cartões na interface web aparece como '(sem nome)', pois o campo "nome" está ausente na resposta da API.
> FONTE: [campo_ausente]

Resposta inteira:

```text
CAUSA_RAIZ: campo_ausente
CAMPO: nome
IMPACTO: O título dos cartões na interface web aparece como '(sem nome)', pois o campo "nome" está ausente na resposta da API.
FONTE: [campo_ausente]
```

## Rastro

Gerado dos eventos 153 a 174 da trilha; hash dos eventos deste caso: `d1ef7256b1088f02` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-22.md`.
