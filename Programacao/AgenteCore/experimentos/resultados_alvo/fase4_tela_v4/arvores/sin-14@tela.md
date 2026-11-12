<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-14`

Caso `sin-14` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/sin-14@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 30 afirmações (21 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (39 linhas) e a diferença do corpo da resposta (33 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 2110 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 179 nós a 39 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 2 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `0 linha(s) da referência`, recebido `0 linha(s) novas` (observado).
- A poda do corpo da resposta levou 2110 caracteres a 33 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, a primeira no campo `imagem` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3492 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 0 linha(s) da referência | 0 linha(s) novas |
| campo imagem | imagem | imagem_v2 |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 179 nós |  |
| a árvore podada | 39 linhas | sim |
| o corpo da resposta inteiro | 2110 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 33 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `campo_ausente` (154,19), `contrato-produto` (141,67) e `campo_renomeado` (133,15) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `campo_ausente`, `contrato-produto` e `campo_renomeado`; o da entidade, em `campo_ausente`, `contrato-produto` e `campo_renomeado` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `entidade-produto` (100,88), `chave_de_juncao_errada` (99,14), `campo_preco_ausente` (70,29), `nulo_inesperado` (52,90) e `tipo_divergente` (46,39) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 160 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `campo_renomeado`, e o primeiro de fora, `entidade-produto`, só o texto do caso já punha o primeiro à frente (130,15 contra 97,88), e os reforços em código levaram a diferença a 32,27 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `campo_ausente` | posição 1, pontuação 154,19: 151,19 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 141,67: 138,67 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_renomeado` | posição 3, pontuação 133,15: 130,15 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 4, pontuação 100,88: 97,88 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 5, pontuação 99,14: 97,14 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_preco_ausente` | posição 6, pontuação 70,29: 69,29 pelas palavras do caso, mais 1,0 por entidade |  |
| `nulo_inesperado` | posição 7, pontuação 52,90: 50,90 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 8, pontuação 46,39: 43,39 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `campo_renomeado` (Campo renomeado); segunda: `campo_ausente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `campo_renomeado` (declarado).
- O modelo apontou o campo `imagem` (declarado).
- `imagem` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,000 contra 0,998 da escolhida; verbetes entregues que a sustentam: `campo_ausente`, `contrato-produto` e `campo_renomeado` (observado).
- As outras 3 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `tipo_divergente` (0,000), `corpo_nao_e_json` (0,000) e `corpo_vazio` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,998, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `imagem: esperado imagem, recebido imagem_v2` (observado).
- A linha FONTE cita `campo_renomeado` (declarado).
- Verbete citado `campo_renomeado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `campo_ausente`, `contrato-produto` e `campo_renomeado` (conferido).
- Leitura do verbete `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 11 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `campo_renomeado` | 0,998 | `campo_ausente`, `contrato-produto` e `campo_renomeado` | sim |
| `campo_ausente` | 0,000 | `campo_ausente`, `contrato-produto` e `campo_renomeado` |  |
| `tipo_divergente` | 0,000 | `contrato-produto` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um campo desconhecido "imagem_v2" na resposta, o que pode causar confusão e dificuldade na integração da interface com a API.
> FONTE: [campo_renomeado]

Resposta inteira:

```text
CAUSA_RAIZ: campo_renomeado
CAMPO: imagem
IMPACTO: O usuário vê um campo desconhecido "imagem_v2" na resposta, o que pode causar confusão e dificuldade na integração da interface com a API.
FONTE: [campo_renomeado]
```

## Rastro

Gerado dos eventos 896 a 930 da trilha; hash dos eventos deste caso: `70b16354c8b50a0a` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-14@tela.md`.
