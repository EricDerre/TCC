<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `semt-1`

Caso `semt-1` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/semt-1@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (469 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (469 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3560 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (49,93), `tipo_divergente` (39,62) e `contrato-produto` (32,47) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `tipo_divergente` e `contrato-produto`; o da entidade, em `entidade-produto`, `tipo_divergente` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `nulo_inesperado` (24,26), `escala_ou_unidade_errada` (20,21), `pagina-produtos-api` (19,59), `campo_renomeado` (18,63) e `estrutura_aninhada_divergente` (17,76) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 37 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `nulo_inesperado`, só o texto do caso já punha o primeiro à frente (29,47 contra 22,26), e os reforços em código levaram a diferença a 8,21 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 49,93: 46,93 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tipo_divergente` | posição 2, pontuação 39,62: 36,62 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 32,47: 29,47 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `nulo_inesperado` | posição 4, pontuação 24,26: 22,26 pelas palavras do caso, mais 2,0 por rota |  |
| `escala_ou_unidade_errada` | posição 5, pontuação 20,21: 17,21 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `pagina-produtos-api` | posição 6, pontuação 19,59: 17,59 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_renomeado` | posição 7, pontuação 18,63: 15,63 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 8, pontuação 17,76: 14,76 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `tipo_divergente` (Tipo divergente); segunda: `formato_de_data_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `tipo_divergente` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `formato_de_data_divergente` (Formato de data divergente), ficou com probabilidade 0,045 contra 0,929 da escolhida; verbetes entregues que a sustentam: `tipo_divergente` (observado).
- As outras 7 alternativas lidas na resposta somam probabilidade 0,025; as maiores: `valor_fora_do_dominio` (0,022), `campo_ausente` (0,001) e `campo_renomeado` (0,001) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,929, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
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
| `tipo_divergente` | 0,929 | `entidade-produto`, `tipo_divergente` e `contrato-produto` | sim |
| `formato_de_data_divergente` | 0,045 | `tipo_divergente` |  |
| `valor_fora_do_dominio` | 0,022 | `tipo_divergente` |  |
| `campo_ausente` | 0,001 | `contrato-produto` |  |
| `campo_renomeado` | 0,001 | `contrato-produto` |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` e `tipo_divergente` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A ordenação por preço fica errada, com 'R$ 9,90' aparecendo depois de 'R$ 89,90'.
> FONTE: [tipo_divergente]

Resposta inteira:

```text
CAUSA_RAIZ: tipo_divergente
CAMPO: preco
IMPACTO: A ordenação por preço fica errada, com 'R$ 9,90' aparecendo depois de 'R$ 89,90'.
FONTE: [tipo_divergente]
```

## Rastro

Gerado dos eventos 294 a 315 da trilha; hash dos eventos deste caso: `8762d1f03f51443a` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/semt-1@fixture.md`.
