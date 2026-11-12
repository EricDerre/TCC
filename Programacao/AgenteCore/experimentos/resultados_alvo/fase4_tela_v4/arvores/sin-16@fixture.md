<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-16`

Caso `sin-16` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/sin-16@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (639 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (639 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3595 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (50,64), `contrato-produto` (48,75) e `campo_ausente` (33,98) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto`, `contrato-produto` e `campo_ausente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `tipo_divergente` (29,66), `campo_renomeado` (29,11), `colecao_no_lugar_de_objeto` (27,52), `estrutura_aninhada_divergente` (25,31) e `chave_de_juncao_errada` (22,97) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 53 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `campo_ausente`, e o primeiro de fora, `tipo_divergente`, só o texto do caso já punha o primeiro à frente (32,98 contra 28,66), e os reforços em código levaram a diferença a 4,32 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 50,64: 47,64 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 48,75: 45,75 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_ausente` | posição 3, pontuação 33,98: 32,98 pelas palavras do caso, mais 1,0 por entidade | sim |
| `tipo_divergente` | posição 4, pontuação 29,66: 28,66 pelas palavras do caso, mais 1,0 por entidade |  |
| `campo_renomeado` | posição 5, pontuação 29,11: 28,11 pelas palavras do caso, mais 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 27,52: 24,52 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 7, pontuação 25,31: 24,31 pelas palavras do caso, mais 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 8, pontuação 22,97: 22,97 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `campo_ausente` (Campo ausente); segunda: `campo_renomeado`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `campo_ausente` (declarado).
- O modelo apontou o campo `destaque` (declarado).
- `destaque` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_renomeado` (Campo renomeado), ficou com probabilidade 0,000 contra 0,997 da escolhida; verbetes entregues que a sustentam: `contrato-produto` e `campo_ausente` (observado).
- As outras 4 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `corpo_nao_e_json` (0,000), `corpo_vazio` (0,000) e `tipo_divergente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,997, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/1 (modo field_missing, campo destaque)`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `campo_ausente` (declarado).
- Verbete citado `campo_ausente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-produto` e `campo_ausente` (conferido).
- Leitura do verbete `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `campo_ausente` | 0,997 | `contrato-produto` e `campo_ausente` | sim |
| `campo_renomeado` | 0,000 | `contrato-produto` e `campo_ausente` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `tipo_divergente` | 0,000 | `entidade-produto` e `contrato-produto` |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O campo destaque, obrigatório no contrato, não é retornado na resposta, causando inconsistência na exibição do produto.
> FONTE: [campo_ausente]

Resposta inteira:

```text
CAUSA_RAIZ: campo_ausente
CAMPO: destaque
IMPACTO: O campo destaque, obrigatório no contrato, não é retornado na resposta, causando inconsistência na exibição do produto.
FONTE: [campo_ausente]
```

## Rastro

Gerado dos eventos 1455 a 1476 da trilha; hash dos eventos deste caso: `cd7bdd5dd4763a57` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-16@fixture.md`.
