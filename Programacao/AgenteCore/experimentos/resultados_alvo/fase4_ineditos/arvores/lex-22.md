<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-22`

Caso `lex-22` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/lex-22`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 22 afirmações (14 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (689 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (689 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3820 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `corpo_nao_e_json` (74,50), `mensagens-de-erro-do-codigo` (37,90) e `corpo_vazio` (34,48) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da status entrou em `corpo_nao_e_json`; `mensagens-de-erro-do-codigo` e `corpo_vazio` pontuaram só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `limite_de_requisicoes` (33,57), `erro_interno_do_servidor` (30,08), `valor_fora_do_dominio` (27,06), `pagina-produtos-api` (25,60) e `tempo_de_resposta_excedido` (20,36) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 63 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `corpo_vazio`, e o primeiro de fora, `limite_de_requisicoes`, só o texto do caso já punha o primeiro à frente (34,48 contra 31,57); a diferença final foi 0,90 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `corpo_nao_e_json` | posição 1, pontuação 74,50: 73,50 pelas palavras do caso, mais 1,0 por status | sim |
| `mensagens-de-erro-do-codigo` | posição 2, pontuação 37,90: 37,90 pelas palavras do caso, sem reforço | sim |
| `corpo_vazio` | posição 3, pontuação 34,48: 34,48 pelas palavras do caso, sem reforço | sim |
| `limite_de_requisicoes` | posição 4, pontuação 33,57: 31,57 pelas palavras do caso, mais 2,0 por rota |  |
| `erro_interno_do_servidor` | posição 5, pontuação 30,08: 28,08 pelas palavras do caso, mais 2,0 por rota |  |
| `valor_fora_do_dominio` | posição 6, pontuação 27,06: 25,06 pelas palavras do caso, mais 2,0 por rota |  |
| `pagina-produtos-api` | posição 7, pontuação 25,60: 23,60 pelas palavras do caso, mais 2,0 por rota |  |
| `tempo_de_resposta_excedido` | posição 8, pontuação 20,36: 17,36 pelas palavras do caso, mais 2,0 por rota e 1,0 por status |  |

## Decisão 3: a causa

Escolha: `corpo_nao_e_json` (Corpo não é JSON); segunda: `corpo_vazio`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `corpo_nao_e_json` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `corpo_vazio` (Corpo vazio), ficou com probabilidade 0,000 contra 0,920 da escolhida; verbetes entregues que a sustentam: `corpo_nao_e_json`, `mensagens-de-erro-do-codigo` e `corpo_vazio` (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,920, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `corpo_nao_e_json` (declarado).
- Verbete citado `corpo_nao_e_json`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `corpo_nao_e_json`, `mensagens-de-erro-do-codigo` e `corpo_vazio` (conferido).
- Leitura do verbete `corpo_nao_e_json` (Corpo não é JSON; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/corpo_nao_e_json.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/corpo_nao_e_json.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `corpo_nao_e_json` | 0,920 | `corpo_nao_e_json`, `mensagens-de-erro-do-codigo` e `corpo_vazio` | sim |
| `corpo_vazio` | 0,000 | `corpo_nao_e_json`, `mensagens-de-erro-do-codigo` e `corpo_vazio` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: A página Produtos exibe uma mensagem de erro e não carrega nenhum cartão de produto.
> FONTE: [corpo_nao_e_json]

Resposta inteira:

```text
CAUSA_RAIZ: corpo_nao_e_json
CAMPO: nenhum
IMPACTO: A página Produtos exibe uma mensagem de erro e não carrega nenhum cartão de produto.
FONTE: [corpo_nao_e_json]
```

## Rastro

Gerado dos eventos 3 a 24 da trilha; hash dos eventos deste caso: `f63b07f1c84b3e79` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-22.md`.
