<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-4`

Caso `sin-4` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/sin-4@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (476 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (476 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3790 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (39,28), `colecao_no_lugar_de_objeto` (36,36) e `contrato-produto` (32,29) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `colecao_no_lugar_de_objeto` e `contrato-produto`; o da entidade, em `entidade-produto`, `colecao_no_lugar_de_objeto` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estado_da_tela_divergente` (25,34), `estrutura_aninhada_divergente` (23,82), `pagina-produtos-api` (21,93), `tipo_divergente` (17,32) e `campo_ausente` (17,00) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 40 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `estado_da_tela_divergente`, só o texto do caso já punha o primeiro à frente (29,29 contra 25,34), e os reforços em código levaram a diferença a 6,94 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 39,28: 36,28 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `colecao_no_lugar_de_objeto` | posição 2, pontuação 36,36: 33,36 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 32,29: 29,29 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estado_da_tela_divergente` | posição 4, pontuação 25,34: 25,34 pelas palavras do caso, sem reforço |  |
| `estrutura_aninhada_divergente` | posição 5, pontuação 23,82: 22,82 pelas palavras do caso, mais 1,0 por entidade |  |
| `pagina-produtos-api` | posição 6, pontuação 21,93: 19,93 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 7, pontuação 17,32: 16,32 pelas palavras do caso, mais 1,0 por entidade |  |
| `campo_ausente` | posição 8, pontuação 17,00: 16,00 pelas palavras do caso, mais 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)); segunda: `tipo_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `colecao_no_lugar_de_objeto` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,040 contra 0,865 da escolhida; verbetes entregues que a sustentam: `entidade-produto` e `contrato-produto` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,133; as maiores: `campo_ausente` (0,033), `campo_renomeado` (0,033) e `resposta_truncada` (0,031) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,865, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/1`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `colecao_no_lugar_de_objeto` (declarado).
- Verbete citado `colecao_no_lugar_de_objeto`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `colecao_no_lugar_de_objeto` e `contrato-produto` (conferido).
- Leitura do verbete `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/colecao_no_lugar_de_objeto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/colecao_no_lugar_de_objeto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `colecao_no_lugar_de_objeto` | 0,865 | `colecao_no_lugar_de_objeto` e `contrato-produto` | sim |
| `tipo_divergente` | 0,040 | `entidade-produto` e `contrato-produto` |  |
| `campo_ausente` | 0,033 | `colecao_no_lugar_de_objeto` e `contrato-produto` |  |
| `campo_renomeado` | 0,033 | `contrato-produto` |  |
| `resposta_truncada` | 0,031 | nenhum |  |
| `corpo_nao_e_json` | 0,011 | nenhum |  |
| `corpo_vazio` | 0,011 | nenhum |  |
| `formato_de_data_divergente` | 0,007 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,005 | `colecao_no_lugar_de_objeto` |  |
| `recurso_inexistente` | 0,001 | `contrato-produto` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê uma tela de detalhe do produto vazia, pois a resposta contém uma lista em vez de um único objeto.
> FONTE: [colecao_no_lugar_de_objeto]

Resposta inteira:

```text
CAUSA_RAIZ: colecao_no_lugar_de_objeto
CAMPO: id
IMPACTO: O usuário vê uma tela de detalhe do produto vazia, pois a resposta contém uma lista em vez de um único objeto.
FONTE: [colecao_no_lugar_de_objeto]
```

## Rastro

Gerado dos eventos 171 a 192 da trilha; hash dos eventos deste caso: `bb1cfafbb8c92814` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-4@fixture.md`.
