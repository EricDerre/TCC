<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-24`

Caso `sin-24` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/sin-24`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (778 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (778 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3953 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-produto` (58,66), `entidade-produto` (55,50) e `estrutura_aninhada_divergente` (44,68) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto`, `entidade-produto` e `estrutura_aninhada_divergente`; o da entidade, em `contrato-produto`, `entidade-produto` e `estrutura_aninhada_divergente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `colecao_no_lugar_de_objeto` (40,38), `chave_de_juncao_errada` (38,18), `campo_renomeado` (37,75), `nulo_inesperado` (37,15) e `tipo_divergente` (32,56) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 72 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `estrutura_aninhada_divergente`, e o primeiro de fora, `colecao_no_lugar_de_objeto`, só o texto do caso já punha o primeiro à frente (41,68 contra 37,38), e os reforços em código levaram a diferença a 4,30 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-produto` | posição 1, pontuação 58,66: 55,66 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 2, pontuação 55,50: 52,50 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 3, pontuação 44,68: 41,68 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `colecao_no_lugar_de_objeto` | posição 4, pontuação 40,38: 37,38 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 5, pontuação 38,18: 36,18 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_renomeado` | posição 6, pontuação 37,75: 34,75 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 7, pontuação 37,15: 35,15 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 8, pontuação 32,56: 29,56 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `estrutura_aninhada_divergente` (Estrutura aninhada divergente); segunda: `campo_ausente`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `estrutura_aninhada_divergente` (declarado).
- O modelo apontou o campo `tipo` (declarado).
- `tipo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,092 contra 0,797 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,199; as maiores: `campo_renomeado` (0,092), `chave_de_juncao_errada` (0,083) e `tipo_divergente` (0,024) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,797, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `entidade-produto` e `contrato-produto` (declarado).
- Os 2 verbetes citados (`entidade-produto` e `contrato-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `estrutura_aninhada_divergente` (conferido).
- Camada de leitura de cada verbete citado: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 9 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `estrutura_aninhada_divergente` | 0,797 | `estrutura_aninhada_divergente` | sim |
| `campo_ausente` | 0,092 | `contrato-produto` |  |
| `campo_renomeado` | 0,092 | `contrato-produto` e `estrutura_aninhada_divergente` |  |
| `chave_de_juncao_errada` | 0,083 | `entidade-produto` |  |
| `tipo_divergente` | 0,024 | `contrato-produto` e `entidade-produto` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` e `estrutura_aninhada_divergente` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê a categoria com o formato completo {"valor":"Carnes","moeda":"BRL"} em vez de apenas "Carnes".
> FONTE: [entidade-produto] [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: estrutura_aninhada_divergente
CAMPO: tipo
IMPACTO: O usuário vê a categoria com o formato completo {"valor":"Carnes","moeda":"BRL"} em vez de apenas "Carnes".
FONTE: [entidade-produto] [contrato-produto]
```

## Rastro

Gerado dos eventos 199 a 224 da trilha; hash dos eventos deste caso: `86021fefb902713d` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-24.md`.
