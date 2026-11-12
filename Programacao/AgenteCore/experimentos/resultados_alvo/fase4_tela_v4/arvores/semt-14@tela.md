<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `semt-14`

Caso `semt-14` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/semt-14@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 30 afirmações (21 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (39 linhas) e a diferença do corpo da resposta (14 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 1978 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 193 nós a 39 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `3 linha(s) da referência`, recebido `3 linha(s) novas` (observado).
- A poda do corpo da resposta levou 1978 caracteres a 14 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 2 diferenças, a primeira no campo `tipo` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3350 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 3 linha(s) da referência | 3 linha(s) novas |
| campo tipo | texto | nulo |
| campo tipo | "Carnes" (referência em modo normal) | null em 14 itens |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 193 nós |  |
| a árvore podada | 39 linhas | sim |
| o corpo da resposta inteiro | 1978 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 14 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `nulo_inesperado` (217,67), `contrato-produto` (124,25) e `entidade-produto` (91,32) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `nulo_inesperado`, `contrato-produto` e `entidade-produto`; o da entidade, em `contrato-produto` e `entidade-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `tipo_divergente` (59,57), `chave_de_juncao_errada` (53,32), `usuario-e-login` (49,82), `valor_fora_do_dominio` (42,78) e `estrutura_aninhada_divergente` (42,73) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 107 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `tipo_divergente`, só o texto do caso já punha o primeiro à frente (88,32 contra 56,57), e os reforços em código levaram a diferença a 31,75 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `nulo_inesperado` | posição 1, pontuação 217,67: 215,67 pelas palavras do caso, mais 2,0 por rota | sim |
| `contrato-produto` | posição 2, pontuação 124,25: 121,25 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 3, pontuação 91,32: 88,32 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tipo_divergente` | posição 4, pontuação 59,57: 56,57 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 5, pontuação 53,32: 51,32 pelas palavras do caso, mais 2,0 por rota |  |
| `usuario-e-login` | posição 6, pontuação 49,82: 49,82 pelas palavras do caso, sem reforço |  |
| `valor_fora_do_dominio` | posição 7, pontuação 42,78: 40,78 pelas palavras do caso, mais 2,0 por rota |  |
| `estrutura_aninhada_divergente` | posição 8, pontuação 42,73: 39,73 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `nulo_inesperado` (Nulo inesperado); segunda: `tipo_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `nulo_inesperado` (declarado).
- O modelo apontou o campo `tipo` (declarado).
- `tipo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 0,997 da escolhida; verbetes entregues que a sustentam: `contrato-produto` e `entidade-produto` (observado).
- As outras 4 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `campo_renomeado` (0,000) e `valor_fora_do_dominio` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,997, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `tipo: esperado texto, recebido nulo` (observado).
- A linha FONTE cita `nulo_inesperado` (declarado).
- Verbete citado `nulo_inesperado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `nulo_inesperado` (conferido).
- Leitura do verbete `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 11 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `nulo_inesperado` | 0,997 | `nulo_inesperado` | sim |
| `tipo_divergente` | 0,000 | `contrato-produto` e `entidade-produto` |  |
| `campo_ausente` | 0,000 | `nulo_inesperado` e `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `valor_fora_do_dominio` | 0,000 | `nulo_inesperado` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um campo tipo como null, o que pode causar erros na exibição dos produtos na interface.
> FONTE: [nulo_inesperado]

Resposta inteira:

```text
CAUSA_RAIZ: nulo_inesperado
CAMPO: tipo
IMPACTO: O usuário vê um campo tipo como null, o que pode causar erros na exibição dos produtos na interface.
FONTE: [nulo_inesperado]
```

## Rastro

Gerado dos eventos 1075 a 1110 da trilha; hash dos eventos deste caso: `240d36216c14ea89` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/semt-14@tela.md`.
