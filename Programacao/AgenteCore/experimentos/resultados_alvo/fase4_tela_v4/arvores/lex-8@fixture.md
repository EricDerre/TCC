<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-8`

Caso `lex-8` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/lex-8@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (544 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (544 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3479 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `codificacao_incorreta` (28,02), `contrato-produto` (25,55) e `entidade-produto` (22,98) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto` e `entidade-produto`; o da entidade, em `contrato-produto` e `entidade-produto`; `codificacao_incorreta` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estado_da_tela_divergente` (19,57), `tipo_divergente` (19,06), `campo_renomeado` (17,69), `estrutura_aninhada_divergente` (16,62) e `colecao_no_lugar_de_objeto` (16,27) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 43 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `estado_da_tela_divergente`, só o texto do caso já punha o primeiro à frente (19,98 contra 19,57), e os reforços em código levaram a diferença a 3,41 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `codificacao_incorreta` | posição 1, pontuação 28,02: 28,02 pelas palavras do caso, sem reforço | sim |
| `contrato-produto` | posição 2, pontuação 25,55: 22,55 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 3, pontuação 22,98: 19,98 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estado_da_tela_divergente` | posição 4, pontuação 19,57: 19,57 pelas palavras do caso, sem reforço |  |
| `tipo_divergente` | posição 5, pontuação 19,06: 16,06 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_renomeado` | posição 6, pontuação 17,69: 14,69 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 7, pontuação 16,62: 13,62 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 8, pontuação 16,27: 13,27 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `codificacao_incorreta` (Codificação de caracteres incorreta); segunda: `corpo_nao_e_json`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `codificacao_incorreta` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `corpo_nao_e_json` (Corpo não é JSON), ficou com probabilidade 0,000 contra 0,679 da escolhida; verbetes entregues que a sustentam: `codificacao_incorreta` (observado).
- A outra alternativa lida na resposta, `corpo_vazio`, tem probabilidade 0,000 (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,679, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `codificacao_incorreta` (declarado).
- Verbete citado `codificacao_incorreta`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `codificacao_incorreta` (conferido).
- Leitura do verbete `codificacao_incorreta` (Codificação de caracteres incorreta; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/codificacao_incorreta.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/codificacao_incorreta.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `codificacao_incorreta` | 0,679 | `codificacao_incorreta` | sim |
| `corpo_nao_e_json` | 0,000 | `codificacao_incorreta` |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A descrição do produto aparece com símbolos no lugar dos acentos, tornando-a ilegível.
> FONTE: [codificacao_incorreta]

Resposta inteira:

```text
CAUSA_RAIZ: codificacao_incorreta
CAMPO: nenhum
IMPACTO: A descrição do produto aparece com símbolos no lugar dos acentos, tornando-a ilegível.
FONTE: [codificacao_incorreta]
```

## Rastro

Gerado dos eventos 701 a 722 da trilha; hash dos eventos deste caso: `7e2887827b2ef85d` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-8@fixture.md`.
