<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `semt-17`

Caso `semt-17` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/semt-17@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (710 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (710 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3611 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (65,18), `contrato-produto` (58,51) e `nulo_inesperado` (45,54) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `nulo_inesperado`; o da entidade, em `entidade-produto` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `chave_de_juncao_errada` (33,37), `pagina-produtos-api` (33,13), `ancora-saiba-mais` (31,43), `estrutura_aninhada_divergente` (25,50) e `campo_ausente` (24,80) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 65 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `nulo_inesperado`, e o primeiro de fora, `chave_de_juncao_errada`, só o texto do caso já punha o primeiro à frente (43,54 contra 31,37), e os reforços em código levaram a diferença a 12,17 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 65,18: 62,18 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 58,51: 55,51 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `nulo_inesperado` | posição 3, pontuação 45,54: 43,54 pelas palavras do caso, mais 2,0 por rota | sim |
| `chave_de_juncao_errada` | posição 4, pontuação 33,37: 31,37 pelas palavras do caso, mais 2,0 por rota |  |
| `pagina-produtos-api` | posição 5, pontuação 33,13: 31,13 pelas palavras do caso, mais 2,0 por rota |  |
| `ancora-saiba-mais` | posição 6, pontuação 31,43: 31,43 pelas palavras do caso, sem reforço |  |
| `estrutura_aninhada_divergente` | posição 7, pontuação 25,50: 22,50 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_ausente` | posição 8, pontuação 24,80: 21,80 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `nulo_inesperado` (Nulo inesperado); segunda: `colecao_no_lugar_de_objeto`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `nulo_inesperado` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)), ficou com probabilidade 0,056 contra 0,913 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 10 alternativas lidas na resposta somam probabilidade 0,050; as maiores: `campo_ausente` (0,010), `campo_renomeado` (0,010) e `corpo_nao_e_json` (0,010) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,913, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `nulo_inesperado` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `nulo_inesperado`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `contrato-produto` não confere; `nulo_inesperado` confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `nulo_inesperado` (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 10 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `nulo_inesperado` | 0,913 | `nulo_inesperado` | sim |
| `colecao_no_lugar_de_objeto` | 0,056 | `contrato-produto` |  |
| `campo_ausente` | 0,010 | `contrato-produto` e `nulo_inesperado` |  |
| `campo_renomeado` | 0,010 | `contrato-produto` |  |
| `corpo_nao_e_json` | 0,010 | nenhum |  |
| `corpo_vazio` | 0,010 | nenhum |  |
| `tipo_divergente` | 0,007 | `entidade-produto` e `contrato-produto` |  |
| `resposta_truncada` | 0,002 | nenhum |  |
| `valor_fora_do_dominio` | 0,001 | `nulo_inesperado` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` e `nulo_inesperado` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um botão com `data-id="null"` ao clicar, o modal exibe um erro, pois o `id` nulo não pode ser usado para buscar detalhes do produto.
> FONTE: [contrato-produto], [nulo_inesperado]

Resposta inteira:

```text
CAUSA_RAIZ: nulo_inesperado
CAMPO: id
IMPACTO: O usuário vê um botão com `data-id="null"` ao clicar, o modal exibe um erro, pois o `id` nulo não pode ser usado para buscar detalhes do produto.
FONTE: [contrato-produto], [nulo_inesperado]
```

## Rastro

Gerado dos eventos 1703 a 1728 da trilha; hash dos eventos deste caso: `7379ab88f3ec7ef2` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/semt-17@fixture.md`.
