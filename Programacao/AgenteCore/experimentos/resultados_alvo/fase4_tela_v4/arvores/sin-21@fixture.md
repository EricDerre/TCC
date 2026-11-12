<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-21`

Caso `sin-21` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/sin-21@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (847 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (847 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3879 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `estrutura_aninhada_divergente` (68,72), `entidade-produto` (60,79) e `pagina-produtos-api` (49,05) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `estrutura_aninhada_divergente`, `entidade-produto` e `pagina-produtos-api`; o da entidade, em `estrutura_aninhada_divergente` e `entidade-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `tipo_divergente` (48,56), `contrato-produto` (48,33), `colecao_no_lugar_de_objeto` (40,73), `chave_de_juncao_errada` (30,07) e `campo_renomeado` (29,84) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 76 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `pagina-produtos-api`, e o primeiro de fora, `tipo_divergente`, só o texto do caso já punha o primeiro à frente (47,05 contra 45,56), e os reforços em código levaram a diferença a 0,49 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `estrutura_aninhada_divergente` | posição 1, pontuação 68,72: 65,72 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 2, pontuação 60,79: 57,79 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pagina-produtos-api` | posição 3, pontuação 49,05: 47,05 pelas palavras do caso, mais 2,0 por rota | sim |
| `tipo_divergente` | posição 4, pontuação 48,56: 45,56 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `contrato-produto` | posição 5, pontuação 48,33: 45,33 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 40,73: 37,73 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 7, pontuação 30,07: 28,07 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_renomeado` | posição 8, pontuação 29,84: 26,84 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `estrutura_aninhada_divergente` (Estrutura aninhada divergente); segunda: `tipo_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `estrutura_aninhada_divergente` (declarado).
- O modelo apontou o campo `tipo` (declarado).
- `tipo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 0,999 da escolhida; verbetes entregues que a sustentam: `entidade-produto` e `pagina-produtos-api` (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `campo_renomeado` (0,000) e `corpo_nao_e_json` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,999, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `estrutura_aninhada_divergente` (declarado).
- Verbete citado `estrutura_aninhada_divergente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `estrutura_aninhada_divergente` (conferido).
- Leitura do verbete `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `estrutura_aninhada_divergente` | 0,999 | `estrutura_aninhada_divergente` | sim |
| `tipo_divergente` | 0,000 | `entidade-produto` e `pagina-produtos-api` |  |
| `campo_ausente` | 0,000 | nenhum |  |
| `campo_renomeado` | 0,000 | `estrutura_aninhada_divergente` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | `pagina-produtos-api` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `estado_da_tela_divergente` | 0,000 | `pagina-produtos-api` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê a categoria do produto como o texto literal {'id': 1, 'nome': 'Carnes'} em vez de 'Carnes'.
> FONTE: [estrutura_aninhada_divergente]

Resposta inteira:

```text
CAUSA_RAIZ: estrutura_aninhada_divergente
CAMPO: tipo
IMPACTO: O usuário vê a categoria do produto como o texto literal {'id': 1, 'nome': 'Carnes'} em vez de 'Carnes'.
FONTE: [estrutura_aninhada_divergente]
```

## Rastro

Gerado dos eventos 1583 a 1604 da trilha; hash dos eventos deste caso: `c662158d6c4e2115` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-21@fixture.md`.
