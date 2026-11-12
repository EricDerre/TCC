<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `semt-21`

Caso `semt-21` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/semt-21@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (500 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (500 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3591 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-produto` (41,13), `entidade-produto` (37,16) e `tipo_divergente` (28,35) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto`, `entidade-produto` e `tipo_divergente`; o da entidade, em `contrato-produto`, `entidade-produto` e `tipo_divergente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estrutura_aninhada_divergente` (27,46), `campo_renomeado` (24,29), `chave_de_juncao_errada` (24,09), `campo_ausente` (22,04) e `estado_da_tela_divergente` (20,84) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 39 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `tipo_divergente`, e o primeiro de fora, `estrutura_aninhada_divergente`, só o texto do caso já punha o primeiro à frente (25,35 contra 24,46), e os reforços em código levaram a diferença a 0,89 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-produto` | posição 1, pontuação 41,13: 38,13 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 2, pontuação 37,16: 34,16 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tipo_divergente` | posição 3, pontuação 28,35: 25,35 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 4, pontuação 27,46: 24,46 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_renomeado` | posição 5, pontuação 24,29: 21,29 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 6, pontuação 24,09: 22,09 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_ausente` | posição 7, pontuação 22,04: 19,04 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estado_da_tela_divergente` | posição 8, pontuação 20,84: 20,84 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `campo_ausente` (Campo ausente); segunda: `campo_renomeado`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `campo_ausente` (declarado).
- O modelo apontou o campo `nome` (declarado).
- `nome` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_renomeado` (Campo renomeado), ficou com probabilidade 0,280 contra 0,960 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,065; as maiores: `corpo_nao_e_json` (0,028), `corpo_vazio` (0,028) e `valor_fora_do_dominio` (0,005) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,960, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` (declarado).
- Verbete citado `contrato-produto`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), não traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-produto` (conferido).
- Leitura do verbete `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `campo_ausente` | 0,960 | `contrato-produto` | sim |
| `campo_renomeado` | 0,280 | `contrato-produto` |  |
| `corpo_nao_e_json` | 0,028 | nenhum |  |
| `corpo_vazio` | 0,028 | nenhum |  |
| `valor_fora_do_dominio` | 0,005 | `tipo_divergente` |  |
| `tipo_divergente` | 0,004 | `contrato-produto`, `entidade-produto` e `tipo_divergente` |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` |  |
| `nulo_inesperado` | 0,000 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` |  |
| `formato_de_data_divergente` | 0,000 | `tipo_divergente` |  |
| `resposta_truncada` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê "(sem nome)" em vez do nome do produto.
> FONTE: [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: campo_ausente
CAMPO: nome
IMPACTO: O usuário vê "(sem nome)" em vez do nome do produto.
FONTE: [contrato-produto]
```

## Rastro

Gerado dos eventos 1829 a 1850 da trilha; hash dos eventos deste caso: `b89d6b5af635bb48` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/semt-21@fixture.md`.
