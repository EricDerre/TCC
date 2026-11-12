<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `semt-21`

Caso `semt-21` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/semt-21@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 31 afirmações (21 observado, 7 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (39 linhas) e a diferença do corpo da resposta (278 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 2222 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 193 nós a 39 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `3 linha(s) da referência`, recebido `3 linha(s) novas` (observado).
- A poda do corpo da resposta levou 2222 caracteres a 278 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, a primeira no campo `nome` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3885 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 3 linha(s) da referência | 3 linha(s) novas |
| campo nome | "Picanha ao Alho" (referência em modo normal) | "Picanha ao Alho (inválido)" em 14 itens |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 193 nós |  |
| a árvore podada | 39 linhas | sim |
| o corpo da resposta inteiro | 2222 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 278 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `valor_fora_do_dominio` (417,15), `entidade-produto` (132,22) e `fluxo-reserva-e-cancelamento` (84,19) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `valor_fora_do_dominio` e `entidade-produto`; o da entidade, em `entidade-produto`; `fluxo-reserva-e-cancelamento` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `limites-do-sistema` (59,67), `contrato-produto` (54,68), `pedido-reserva` (48,65), `contagem_inconsistente` (48,36) e `corpo_vazio` (45,93) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 183 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `fluxo-reserva-e-cancelamento`, e o primeiro de fora, `limites-do-sistema`, só o texto do caso já punha o primeiro à frente (84,19 contra 59,67); a diferença final foi 24,52 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `valor_fora_do_dominio` | posição 1, pontuação 417,15: 415,15 pelas palavras do caso, mais 2,0 por rota | sim |
| `entidade-produto` | posição 2, pontuação 132,22: 129,22 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `fluxo-reserva-e-cancelamento` | posição 3, pontuação 84,19: 84,19 pelas palavras do caso, sem reforço | sim |
| `limites-do-sistema` | posição 4, pontuação 59,67: 59,67 pelas palavras do caso, sem reforço |  |
| `contrato-produto` | posição 5, pontuação 54,68: 51,68 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `pedido-reserva` | posição 6, pontuação 48,65: 48,65 pelas palavras do caso, sem reforço |  |
| `contagem_inconsistente` | posição 7, pontuação 48,36: 45,36 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `corpo_vazio` | posição 8, pontuação 45,93: 45,93 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `campo_renomeado` (Campo renomeado); segunda: `valor_fora_do_dominio`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `campo_renomeado` (declarado).
- O modelo apontou o campo `nome` (declarado).
- `nome` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `valor_fora_do_dominio` (Valor fora do domínio), ficou com probabilidade 0,000 contra 0,998 da escolhida; verbetes entregues que a sustentam: `valor_fora_do_dominio` e `fluxo-reserva-e-cancelamento` (observado).
- As outras 7 alternativas lidas na resposta somam probabilidade 0,001; as maiores: `campo_ausente` (0,000), `tipo_divergente` (0,000) e `formato_de_data_divergente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,998, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `nome: esperado "Picanha ao Alho" (referência em modo normal), recebido "Picanha ao Alho (inválido)" em 14 itens` (observado).
- A linha FONTE cita `entidade-produto` (declarado).
- Verbete citado `entidade-produto`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), não traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Leitura do verbete `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida campo_renomeado (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 9 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `campo_renomeado` | 0,998 | nenhum | sim |
| `valor_fora_do_dominio` | 0,000 | `valor_fora_do_dominio` e `fluxo-reserva-e-cancelamento` |  |
| `campo_ausente` | 0,000 | nenhum |  |
| `tipo_divergente` | 0,000 | `valor_fora_do_dominio` e `entidade-produto` |  |
| `formato_de_data_divergente` | 0,000 | `valor_fora_do_dominio` |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê nomes incorretos dos produtos na tela, com adição de parênteses e texto inválido.
> FONTE: [entidade-produto]

Resposta inteira:

```text
CAUSA_RAIZ: campo_renomeado
CAMPO: nome
IMPACTO: O usuário vê nomes incorretos dos produtos na tela, com adição de parênteses e texto inválido.
FONTE: [entidade-produto]
```

## Rastro

Gerado dos eventos 1792 a 1827 da trilha; hash dos eventos deste caso: `a8b8ede1beb4d7e9` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/semt-21@tela.md`.
