<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-4`

Caso `lex-4` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/lex-4@tela`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 30 afirmações (21 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (45 linhas) e a diferença do corpo da resposta (243 caracteres), não a página inteira.

- A página chamou `GET /api/produtos` (status 200 (a API respondeu sem código de erro), 2071 caracteres de corpo) (observado).
- A poda da árvore de acessibilidade da tela levou 193 nós a 45 linhas (observado).
- O que saiu, pelas regras em código: 10 cartões iguais omitidos (ficam os primeiros e os que contêm o alvo), 1 elemento de decoração removido (separador, moldura ou figura), 1 título abaixo do nível 4 removido fora dos cartões, 16 imagens removidas, 8 botões e campos sem nome acessível removidos, 14 listas e grupos achatados (fica só o conteúdo) e 3 textos sem letra nem número removidos (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- A tela comparada com a referência (a mesma página sem falha injetada): esperado `1 linha(s) da referência`, recebido `7 linha(s) novas` (observado).
- A poda do corpo da resposta levou 2071 caracteres a 243 caracteres: só a diferença contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) vai ao modelo (observado).
- A comparação do corpo achou 1 diferença, a primeira no campo `nome` (a tabela das diferenças está abaixo) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3807 caracteres (observado).

| Onde | Esperado | Recebido |
|---|---|---|
| árvore de acessibilidade, contra a referência | 1 linha(s) da referência | 7 linha(s) novas |
| campo nome | "Água Mineral" (referência em modo normal) | "Ãgua Mineral" em 3 itens |

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 193 nós |  |
| a árvore podada | 45 linhas | sim |
| o corpo da resposta inteiro | 2071 caracteres |  |
| a diferença do corpo contra o contrato esperado pela interface e a resposta da mesma rota em modo normal (a referência) | 243 caracteres | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `codificacao_incorreta` (157,44), `entidade-produto` (75,29) e `contrato-produto` (56,32) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; `codificacao_incorreta` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estrutura_aninhada_divergente` (42,01), `tipo_divergente` (36,25), `chave_de_juncao_errada` (31,85), `campo_ausente` (30,46) e `nulo_inesperado` (29,25) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 121 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato e com a referência (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `estrutura_aninhada_divergente`, só o texto do caso já punha o primeiro à frente (53,32 contra 39,01), e os reforços em código levaram a diferença a 14,31 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `codificacao_incorreta` | posição 1, pontuação 157,44: 157,44 pelas palavras do caso, sem reforço | sim |
| `entidade-produto` | posição 2, pontuação 75,29: 72,29 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 56,32: 53,32 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 4, pontuação 42,01: 39,01 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tipo_divergente` | posição 5, pontuação 36,25: 33,25 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 6, pontuação 31,85: 29,85 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_ausente` | posição 7, pontuação 30,46: 27,46 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 8, pontuação 29,25: 27,25 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `codificacao_incorreta` (Codificação de caracteres incorreta); segunda: `tipo_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `codificacao_incorreta` (declarado).
- O modelo apontou o campo `nome` (declarado).
- `nome` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 0,989 da escolhida; verbetes entregues que a sustentam: `codificacao_incorreta`, `entidade-produto` e `contrato-produto` (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `corpo_nao_e_json` (0,000), `corpo_vazio` (0,000) e `valor_fora_do_dominio` (0,000) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,989, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- O sinal medido em código está presente na resposta HTTP: `nome: esperado "Água Mineral" (referência em modo normal), recebido "Ãgua Mineral" em 3 itens` (observado).
- A linha FONTE cita `codificacao_incorreta` e `entidade-produto` (declarado).
- Os 2 verbetes citados (`codificacao_incorreta` e `entidade-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `codificacao_incorreta` confere; `entidade-produto` não confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `codificacao_incorreta` (conferido).
- Camada de leitura de cada verbete citado: `codificacao_incorreta` (Codificação de caracteres incorreta; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/codificacao_incorreta.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/codificacao_incorreta.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 13 de 14 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `codificacao_incorreta` | 0,989 | `codificacao_incorreta` | sim |
| `tipo_divergente` | 0,000 | `codificacao_incorreta`, `entidade-produto` e `contrato-produto` |  |
| `corpo_nao_e_json` | 0,000 | `codificacao_incorreta` |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê nomes com acentos corrompidos em alguns itens do cardápio.
> FONTE: [codificacao_incorreta] [entidade-produto]

Resposta inteira:

```text
CAUSA_RAIZ: codificacao_incorreta
CAMPO: nome
IMPACTO: O usuário vê nomes com acentos corrompidos em alguns itens do cardápio.
FONTE: [codificacao_incorreta] [entidade-produto]
```

## Rastro

Gerado dos eventos 67 a 106 da trilha; hash dos eventos deste caso: `64f887099a7f6e06` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-4@tela.md`.
