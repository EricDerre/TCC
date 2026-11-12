<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-27`

Caso `tra-27` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/tra-27`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (708 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (708 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3626 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (55,52), `contrato-produto` (40,12) e `pagina-produtos-api` (33,67) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `pagina-produtos-api`; o da entidade, em `entidade-produto` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estrutura_aninhada_divergente` (29,36), `colecao_no_lugar_de_objeto` (28,98), `campo_ausente` (27,15), `nulo_inesperado` (26,43) e `campo_renomeado` (24,18) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 66 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `pagina-produtos-api`, e o primeiro de fora, `estrutura_aninhada_divergente`, só o texto do caso já punha o primeiro à frente (31,67 contra 28,36), e os reforços em código levaram a diferença a 4,31 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 55,52: 52,52 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 40,12: 37,12 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pagina-produtos-api` | posição 3, pontuação 33,67: 31,67 pelas palavras do caso, mais 2,0 por rota | sim |
| `estrutura_aninhada_divergente` | posição 4, pontuação 29,36: 28,36 pelas palavras do caso, mais 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 5, pontuação 28,98: 25,98 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_ausente` | posição 6, pontuação 27,15: 26,15 pelas palavras do caso, mais 1,0 por entidade |  |
| `nulo_inesperado` | posição 7, pontuação 26,43: 26,43 pelas palavras do caso, sem reforço |  |
| `campo_renomeado` | posição 8, pontuação 24,18: 23,18 pelas palavras do caso, mais 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `tipo_divergente` (Tipo divergente); segunda: `valor_fora_do_dominio`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `tipo_divergente` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `valor_fora_do_dominio` (Valor fora do domínio), ficou com probabilidade 0,034 contra 0,958 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,009; as maiores: `campo_ausente` (0,003), `campo_renomeado` (0,003) e `formato_de_data_divergente` (0,002) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,958, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/2`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `entidade-produto` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `entidade-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `entidade-produto`, `contrato-produto` e `pagina-produtos-api` (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 9 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `tipo_divergente` | 0,958 | `entidade-produto`, `contrato-produto` e `pagina-produtos-api` | sim |
| `valor_fora_do_dominio` | 0,034 | nenhum |  |
| `campo_ausente` | 0,003 | `contrato-produto` |  |
| `campo_renomeado` | 0,003 | `contrato-produto` |  |
| `formato_de_data_divergente` | 0,002 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | `pagina-produtos-api` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O preço exibido no detalhe do produto difere do preço no cartão, causando confusão para o usuário.
> FONTE: [contrato-produto] [entidade-produto]

Resposta inteira:

```text
CAUSA_RAIZ: tipo_divergente
CAMPO: preco
IMPACTO: O preço exibido no detalhe do produto difere do preço no cartão, causando confusão para o usuário.
FONTE: [contrato-produto] [entidade-produto]
```

## Rastro

Gerado dos eventos 568 a 593 da trilha; hash dos eventos deste caso: `fefbdf2f30565248` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-27.md`.
