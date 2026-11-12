<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `semt-26`

Caso `semt-26` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/semt-26`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (771 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (771 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3672 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-produto` (49,04), `nulo_inesperado` (38,59) e `entidade-produto` (36,07) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto` e `entidade-produto`; o da entidade, em `contrato-produto` e `entidade-produto`; `nulo_inesperado` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (29,14), `colecao_no_lugar_de_objeto` (26,89), `campo_renomeado` (25,69), `campo_ausente` (22,80) e `estado_da_tela_divergente` (22,79) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 74 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (33,07 contra 27,14), e os reforços em código levaram a diferença a 6,92 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-produto` | posição 1, pontuação 49,04: 46,04 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `nulo_inesperado` | posição 2, pontuação 38,59: 38,59 pelas palavras do caso, sem reforço | sim |
| `entidade-produto` | posição 3, pontuação 36,07: 33,07 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pagina-produtos-api` | posição 4, pontuação 29,14: 27,14 pelas palavras do caso, mais 2,0 por rota |  |
| `colecao_no_lugar_de_objeto` | posição 5, pontuação 26,89: 23,89 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_renomeado` | posição 6, pontuação 25,69: 24,69 pelas palavras do caso, mais 1,0 por entidade |  |
| `campo_ausente` | posição 7, pontuação 22,80: 21,80 pelas palavras do caso, mais 1,0 por entidade |  |
| `estado_da_tela_divergente` | posição 8, pontuação 22,79: 22,79 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `nulo_inesperado` (Nulo inesperado); segunda: `campo_ausente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `nulo_inesperado` (declarado).
- O modelo apontou o campo `resumo` (declarado).
- `resumo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,040 contra 0,892 da escolhida; verbetes entregues que a sustentam: `contrato-produto` e `nulo_inesperado` (observado).
- As outras 10 alternativas lidas na resposta somam probabilidade 0,103; as maiores: `campo_renomeado` (0,040), `chave_de_juncao_errada` (0,039) e `valor_fora_do_dominio` (0,009) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,892, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/12`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `nulo_inesperado` (declarado).
- Verbete citado `nulo_inesperado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `nulo_inesperado` (conferido).
- Leitura do verbete `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `nulo_inesperado` | 0,892 | `nulo_inesperado` | sim |
| `campo_ausente` | 0,040 | `contrato-produto` e `nulo_inesperado` |  |
| `campo_renomeado` | 0,040 | `contrato-produto` |  |
| `chave_de_juncao_errada` | 0,039 | `nulo_inesperado` e `entidade-produto` |  |
| `valor_fora_do_dominio` | 0,009 | `nulo_inesperado` |  |
| `tipo_divergente` | 0,008 | `contrato-produto` e `entidade-produto` |  |
| `formato_de_data_divergente` | 0,003 | nenhum |  |
| `resposta_truncada` | 0,002 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,001 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê uma descrição no cardápio, mas no modal, o campo 'Saiba Mais...' está vazio.
> FONTE: [nulo_inesperado]

Resposta inteira:

```text
CAUSA_RAIZ: nulo_inesperado
CAMPO: resumo
IMPACTO: O usuário vê uma descrição no cardápio, mas no modal, o campo 'Saiba Mais...' está vazio.
FONTE: [nulo_inesperado]
```

## Rastro

Gerado dos eventos 395 a 416 da trilha; hash dos eventos deste caso: `d4c192c507f326d8` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/semt-26.md`.
