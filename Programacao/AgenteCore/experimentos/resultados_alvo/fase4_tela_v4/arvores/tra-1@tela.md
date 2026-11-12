<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-1`

Caso `tra-1` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/tra-1@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 30 afirmações (21 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (39 linhas) e a diferença do corpo da resposta (270 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 2096 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 193 nós a 39 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `3 linha(s) da referência`, recebido `3 linha(s) novas` (observado).
- A poda do corpo da resposta levou 2096 caracteres a 270 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, a primeira no campo `preco` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4196 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 3 linha(s) da referência | 3 linha(s) novas |
| campo preco | 89.9 (referência em modo normal) | 8990.0 em 14 itens |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 193 nós |  |
| a árvore podada | 39 linhas | sim |
| o corpo da resposta inteiro | 2096 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 270 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `escala_ou_unidade_errada` (594,53), `entidade-produto` (85,15) e `tempo_de_resposta_excedido` (56,56) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `escala_ou_unidade_errada`, `entidade-produto` e `tempo_de_resposta_excedido`; o da entidade, em `escala_ou_unidade_errada` e `entidade-produto`; o do status, em `tempo_de_resposta_excedido` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `contrato-produto` (53,46), `estrutura_aninhada_divergente` (41,30), `tipo_divergente` (37,10), `corpo_nao_e_json` (34,80) e `limite_de_requisicoes` (34,56) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 221 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `tempo_de_resposta_excedido`, e o primeiro de fora, `contrato-produto`, só o texto do caso já punha o primeiro à frente (53,56 contra 50,46), e os reforços em código levaram a diferença a 3,10 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `escala_ou_unidade_errada` | posição 1, pontuação 594,53: 591,53 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 2, pontuação 85,15: 82,15 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tempo_de_resposta_excedido` | posição 3, pontuação 56,56: 53,56 pelas palavras do caso, mais 2,0 por rota e 1,0 por status | sim |
| `contrato-produto` | posição 4, pontuação 53,46: 50,46 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 5, pontuação 41,30: 38,30 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tipo_divergente` | posição 6, pontuação 37,10: 34,10 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `corpo_nao_e_json` | posição 7, pontuação 34,80: 33,80 pelas palavras do caso, mais 1,0 por status |  |
| `limite_de_requisicoes` | posição 8, pontuação 34,56: 32,56 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `escala_ou_unidade_errada` (Escala ou unidade errada); segunda: `tipo_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `escala_ou_unidade_errada` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 0,980 da escolhida; verbetes entregues que a sustentam: `escala_ou_unidade_errada` e `entidade-produto` (observado).
- As outras 6 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `valor_fora_do_dominio` (0,000), `formato_de_data_divergente` (0,000) e `campo_ausente` (0,000) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,980, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `preco: esperado 89.9 (referência em modo normal), recebido 8990.0 em 14 itens` (observado).
- A linha FONTE cita `escala_ou_unidade_errada` (declarado).
- Verbete citado `escala_ou_unidade_errada`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `escala_ou_unidade_errada` e `entidade-produto` (conferido).
- Leitura do verbete `escala_ou_unidade_errada` (Escala ou unidade errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/escala_ou_unidade_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/escala_ou_unidade_errada.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 11 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `escala_ou_unidade_errada` | 0,980 | `escala_ou_unidade_errada` e `entidade-produto` | sim |
| `tipo_divergente` | 0,000 | `escala_ou_unidade_errada` e `entidade-produto` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | `escala_ou_unidade_errada` |  |
| `campo_ausente` | 0,000 | nenhum |  |
| `campo_renomeado` | 0,000 | nenhum |  |
| `estado_da_tela_divergente` | 0,000 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê preços com escalas incorretas, como R$ 8990,00 em vez de R$ 89,90.
> FONTE: [escala_ou_unidade_errada]

Resposta inteira:

```text
CAUSA_RAIZ: escala_ou_unidade_errada
CAMPO: preco
IMPACTO: O usuário vê preços com escalas incorretas, como R$ 8990,00 em vez de R$ 89,90.
FONTE: [escala_ou_unidade_errada]
```

## Rastro

Gerado dos eventos 317 a 352 da trilha; hash dos eventos deste caso: `85c7c88c583e7a1d` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-1@tela.md`.
