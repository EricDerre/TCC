<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-23`

Caso `lex-23` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/lex-23`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (449 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (449 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3839 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `resposta_truncada` (34,83), `corpo_nao_e_json` (24,54) e `corpo_vazio` (23,45) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da status entrou em `corpo_nao_e_json`; `resposta_truncada` e `corpo_vazio` pontuaram só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `ancora-saiba-mais` (17,81), `pagina-produtos-api` (15,67), `tempo_de_resposta_excedido` (13,66), `entidade-produto` (11,48) e `limite_de_requisicoes` (10,81) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 32 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `corpo_vazio`, e o primeiro de fora, `ancora-saiba-mais`, só o texto do caso já punha o primeiro à frente (23,45 contra 17,81); a diferença final foi 5,64 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `resposta_truncada` | posição 1, pontuação 34,83: 34,83 pelas palavras do caso, sem reforço | sim |
| `corpo_nao_e_json` | posição 2, pontuação 24,54: 23,54 pelas palavras do caso, mais 1,0 por status | sim |
| `corpo_vazio` | posição 3, pontuação 23,45: 23,45 pelas palavras do caso, sem reforço | sim |
| `ancora-saiba-mais` | posição 4, pontuação 17,81: 17,81 pelas palavras do caso, sem reforço |  |
| `pagina-produtos-api` | posição 5, pontuação 15,67: 13,67 pelas palavras do caso, mais 2,0 por rota |  |
| `tempo_de_resposta_excedido` | posição 6, pontuação 13,66: 12,66 pelas palavras do caso, mais 1,0 por status |  |
| `entidade-produto` | posição 7, pontuação 11,48: 8,48 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `limite_de_requisicoes` | posição 8, pontuação 10,81: 10,81 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `corpo_vazio` (Corpo vazio); segunda: `resposta_truncada`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `corpo_vazio` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `resposta_truncada` (Resposta truncada), ficou com probabilidade 0,013 contra 0,987 da escolhida; verbetes entregues que a sustentam: `resposta_truncada`, `corpo_nao_e_json` e `corpo_vazio` (observado).
- A outra alternativa lida na resposta, `corpo_nao_e_json`, tem probabilidade 0,004 (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,987, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/6`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `corpo_vazio` (declarado).
- Verbete citado `corpo_vazio`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `resposta_truncada`, `corpo_nao_e_json` e `corpo_vazio` (conferido).
- Leitura do verbete `corpo_vazio` (Corpo vazio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/corpo_vazio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/corpo_vazio.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `corpo_vazio` | 0,987 | `resposta_truncada`, `corpo_nao_e_json` e `corpo_vazio` | sim |
| `resposta_truncada` | 0,013 | `resposta_truncada`, `corpo_nao_e_json` e `corpo_vazio` |  |
| `corpo_nao_e_json` | 0,004 | `resposta_truncada`, `corpo_nao_e_json` e `corpo_vazio` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um modal com o título "Erro" e uma mensagem de "Unexpected end of JSON input", indicando que a resposta da API está vazia.
> FONTE: [corpo_vazio]

Resposta inteira:

```text
CAUSA_RAIZ: corpo_vazio
CAMPO: nenhum
IMPACTO: O usuário vê um modal com o título "Erro" e uma mensagem de "Unexpected end of JSON input", indicando que a resposta da API está vazia.
FONTE: [corpo_vazio]
```

## Rastro

Gerado dos eventos 26 a 47 da trilha; hash dos eventos deste caso: `c5b232ff6e29922b` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-23.md`.
