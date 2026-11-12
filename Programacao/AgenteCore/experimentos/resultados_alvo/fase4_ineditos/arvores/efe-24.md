<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `efe-24`

Caso `efe-24` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/efe-24`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1421 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1421 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4604 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `localizador_quebrado` (47,43), `contrato-produto` (45,80) e `entidade-produto` (42,62) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto` e `entidade-produto`; o da entidade, em `localizador_quebrado` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (26,62), `tipo_divergente` (26,56), `campo_ausente` (26,06), `valor_fora_do_dominio` (25,61) e `nulo_inesperado` (24,70) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Interface`, status 200 e 89 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (40,62 contra 23,62), e os reforços em código levaram a diferença a 16,00 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `localizador_quebrado` | posição 1, pontuação 47,43: 46,43 pelas palavras do caso, mais 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 45,80: 43,80 pelas palavras do caso, mais 2,0 por rota | sim |
| `entidade-produto` | posição 3, pontuação 42,62: 40,62 pelas palavras do caso, mais 2,0 por rota | sim |
| `pagina-produtos-api` | posição 4, pontuação 26,62: 23,62 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tipo_divergente` | posição 5, pontuação 26,56: 24,56 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_ausente` | posição 6, pontuação 26,06: 24,06 pelas palavras do caso, mais 2,0 por rota |  |
| `valor_fora_do_dominio` | posição 7, pontuação 25,61: 23,61 pelas palavras do caso, mais 2,0 por rota |  |
| `nulo_inesperado` | posição 8, pontuação 24,70: 22,70 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `localizador_quebrado` (Localizador (seletor) quebrado); segunda: `estrutura_aninhada_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `localizador_quebrado` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `estrutura_aninhada_divergente` (Estrutura aninhada divergente), ficou com probabilidade 0,000 contra 0,998 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 12 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `campo_renomeado` (0,000) e `resposta_truncada` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,998, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `localizador_quebrado` (declarado).
- Verbete citado `localizador_quebrado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `localizador_quebrado` (conferido).
- Leitura do verbete `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `localizador_quebrado` | 0,998 | `localizador_quebrado` | sim |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `tipo_divergente` | 0,000 | `contrato-produto` e `entidade-produto` |  |
| `nulo_inesperado` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `estado_da_tela_divergente` | 0,000 | `localizador_quebrado` |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `tempo_de_resposta_excedido` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário não consegue abrir os detalhes do produto Alcatra na Pedra, pois o modal não aparece após o clique.
> FONTE: [localizador_quebrado]

Resposta inteira:

```text
CAUSA_RAIZ: localizador_quebrado
CAMPO: nenhum
IMPACTO: O usuário não consegue abrir os detalhes do produto Alcatra na Pedra, pois o modal não aparece após o clique.
FONTE: [localizador_quebrado]
```

## Rastro

Gerado dos eventos 787 a 808 da trilha; hash dos eventos deste caso: `4fe6aac6ea9e32c2` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/efe-24.md`.
