<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-18`

Caso `lex-18` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/lex-18@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 30 afirmações (21 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (39 linhas) e a diferença do corpo da resposta (245 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 2073 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 193 nós a 39 linhas (observado).
- O que saiu, pelas regras em código: 11 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `0 linha(s) da referência`, recebido `0 linha(s) novas` (observado).
- A poda do corpo da resposta levou 2073 caracteres a 245 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, a primeira no campo `resumo` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3739 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 0 linha(s) da referência | 0 linha(s) novas |
| campo resumo | "Garrafa 500ml, com ou sem gás" (referência em modo normal) | "Garrafa 500ml, com ou sem gÃ¡s" em 4 itens |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 193 nós |  |
| a árvore podada | 39 linhas | sim |
| o corpo da resposta inteiro | 2073 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 245 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `codificacao_incorreta` (207,24), `entidade-produto` (75,66) e `contrato-produto` (57,64) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; `codificacao_incorreta` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `tipo_divergente` (43,12), `estrutura_aninhada_divergente` (40,59), `chave_de_juncao_errada` (36,15), `nulo_inesperado` (30,27) e `valor_fora_do_dominio` (28,78) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 136 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `tipo_divergente`, só o texto do caso já punha o primeiro à frente (54,64 contra 40,12), e os reforços em código levaram a diferença a 14,52 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `codificacao_incorreta` | posição 1, pontuação 207,24: 207,24 pelas palavras do caso, sem reforço | sim |
| `entidade-produto` | posição 2, pontuação 75,66: 72,66 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 57,64: 54,64 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tipo_divergente` | posição 4, pontuação 43,12: 40,12 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 5, pontuação 40,59: 37,59 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 6, pontuação 36,15: 34,15 pelas palavras do caso, mais 2,0 por rota |  |
| `nulo_inesperado` | posição 7, pontuação 30,27: 28,27 pelas palavras do caso, mais 2,0 por rota |  |
| `valor_fora_do_dominio` | posição 8, pontuação 28,78: 26,78 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `codificacao_incorreta` (Codificação de caracteres incorreta); segunda: `tipo_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `codificacao_incorreta` (declarado).
- O modelo apontou o campo `resumo` (declarado).
- `resumo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,007 contra 0,981 da escolhida; verbetes entregues que a sustentam: `codificacao_incorreta`, `entidade-produto` e `contrato-produto` (observado).
- As outras 10 alternativas lidas na resposta somam probabilidade 0,008; as maiores: `valor_fora_do_dominio` (0,004), `formato_de_data_divergente` (0,002) e `campo_ausente` (0,001) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,981, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `resumo: esperado "Garrafa 500ml, com ou sem gás" (referência em modo normal), recebido "Garrafa 500ml, com ou sem gÃ¡s" em 4 itens` (observado).
- A linha FONTE cita `codificacao_incorreta` (declarado).
- Verbete citado `codificacao_incorreta`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `codificacao_incorreta` (conferido).
- Leitura do verbete `codificacao_incorreta` (Codificação de caracteres incorreta; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/codificacao_incorreta.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/codificacao_incorreta.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 11 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `codificacao_incorreta` | 0,981 | `codificacao_incorreta` | sim |
| `tipo_divergente` | 0,007 | `codificacao_incorreta`, `entidade-produto` e `contrato-produto` |  |
| `valor_fora_do_dominio` | 0,004 | nenhum |  |
| `formato_de_data_divergente` | 0,002 | nenhum |  |
| `campo_ausente` | 0,001 | `contrato-produto` |  |
| `campo_renomeado` | 0,001 | `contrato-produto` |  |
| `corpo_nao_e_json` | 0,000 | `codificacao_incorreta` |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê resumos corrompidos em 4 itens, com caracteres acentuados errados.
> FONTE: [codificacao_incorreta]

Resposta inteira:

```text
CAUSA_RAIZ: codificacao_incorreta
CAMPO: resumo
IMPACTO: O usuário vê resumos corrompidos em 4 itens, com caracteres acentuados errados.
FONTE: [codificacao_incorreta]
```

## Rastro

Gerado dos eventos 1355 a 1385 da trilha; hash dos eventos deste caso: `39b4f9c6390babe6` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-18@tela.md`.
