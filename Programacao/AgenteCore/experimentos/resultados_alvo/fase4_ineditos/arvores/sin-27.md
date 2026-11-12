<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-27`

Caso `sin-27` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/sin-27`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1060 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1060 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4579 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-produto` (65,47), `entidade-produto` (64,19) e `chave_de_juncao_errada` (44,06) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto`, `entidade-produto` e `chave_de_juncao_errada`; o da entidade, em `contrato-produto` e `entidade-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `campo_ausente` (42,81), `campo_renomeado` (41,51), `nulo_inesperado` (33,63), `contagem_inconsistente` (32,17) e `campo_preco_ausente` (23,69) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 99 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `chave_de_juncao_errada`, e o primeiro de fora, `campo_ausente`, só o texto do caso já punha o primeiro à frente (42,06 contra 39,81), e os reforços em código levaram a diferença a 1,25 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-produto` | posição 1, pontuação 65,47: 62,47 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 2, pontuação 64,19: 61,19 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `chave_de_juncao_errada` | posição 3, pontuação 44,06: 42,06 pelas palavras do caso, mais 2,0 por rota | sim |
| `campo_ausente` | posição 4, pontuação 42,81: 39,81 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_renomeado` | posição 5, pontuação 41,51: 38,51 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 6, pontuação 33,63: 31,63 pelas palavras do caso, mais 2,0 por rota |  |
| `contagem_inconsistente` | posição 7, pontuação 32,17: 29,17 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_preco_ausente` | posição 8, pontuação 23,69: 22,69 pelas palavras do caso, mais 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `campo_renomeado` (Campo renomeado); segunda: `valor_fora_do_dominio`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `campo_renomeado` (declarado).
- O modelo apontou o campo `imagem_v2` (declarado).
- `imagem_v2` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `valor_fora_do_dominio` (Valor fora do domínio), ficou com probabilidade 0,157 contra 0,413 da escolhida; verbetes entregues que a sustentam: `chave_de_juncao_errada` (observado).
- As outras 12 alternativas lidas na resposta somam probabilidade 0,416; as maiores: `tipo_divergente` (0,103), `chave_de_juncao_errada` (0,099) e `formato_de_data_divergente` (0,074) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,413, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` (declarado).
- Verbete citado `contrato-produto`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), não traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-produto` (conferido).
- Leitura do verbete `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `campo_renomeado` | 0,413 | `contrato-produto` | sim |
| `valor_fora_do_dominio` | 0,157 | `chave_de_juncao_errada` |  |
| `tipo_divergente` | 0,103 | `contrato-produto` e `entidade-produto` |  |
| `chave_de_juncao_errada` | 0,099 | `entidade-produto` e `chave_de_juncao_errada` |  |
| `formato_de_data_divergente` | 0,074 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,064 | `contrato-produto` |  |
| `escala_ou_unidade_errada` | 0,055 | `entidade-produto` e `chave_de_juncao_errada` |  |
| `estrutura_aninhada_divergente` | 0,011 | nenhum |  |
| `campo_ausente` | 0,007 | `contrato-produto` |  |
| `nulo_inesperado` | 0,001 | `chave_de_juncao_errada` |  |
| `resposta_truncada` | 0,001 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `estado_da_tela_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: Os itens sem foto mostram corretamente os nomes e preços, mas faltam as imagens, pois o campo correto é imagem, não imagem_v2.
> FONTE: [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: campo_renomeado
CAMPO: imagem_v2
IMPACTO: Os itens sem foto mostram corretamente os nomes e preços, mas faltam as imagens, pois o campo correto é imagem, não imagem_v2.
FONTE: [contrato-produto]
```

## Rastro

Gerado dos eventos 276 a 297 da trilha; hash dos eventos deste caso: `4cdcf8b16eb6767d` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-27.md`.
