<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-26`

Caso `tra-26` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/tra-26`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1192 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1192 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4117 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (53,71), `contrato-produto` (53,31) e `ancora-saiba-mais` (44,46) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; `ancora-saiba-mais` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (37,39), `campo_ausente` (36,72), `estrutura_aninhada_divergente` (33,29), `chave_de_juncao_errada` (32,79) e `tipo_divergente` (31,75) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 103 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `ancora-saiba-mais`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (44,46 contra 35,39); a diferença final foi 7,07 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 53,71: 50,71 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 53,31: 50,31 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `ancora-saiba-mais` | posição 3, pontuação 44,46: 44,46 pelas palavras do caso, sem reforço | sim |
| `pagina-produtos-api` | posição 4, pontuação 37,39: 35,39 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_ausente` | posição 5, pontuação 36,72: 33,72 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 6, pontuação 33,29: 30,29 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 7, pontuação 32,79: 30,79 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 8, pontuação 31,75: 28,75 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)); segunda: `campo_ausente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `colecao_no_lugar_de_objeto` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,031 contra 0,915 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,081; as maiores: `campo_renomeado` (0,031), `resposta_truncada` (0,027) e `estrutura_aninhada_divergente` (0,012) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,915, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
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
| `colecao_no_lugar_de_objeto` | 0,915 | `contrato-produto` | sim |
| `campo_ausente` | 0,031 | `contrato-produto` |  |
| `campo_renomeado` | 0,031 | `contrato-produto` |  |
| `resposta_truncada` | 0,027 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,012 | nenhum |  |
| `tipo_divergente` | 0,009 | `entidade-produto` e `contrato-produto` |  |
| `corpo_nao_e_json` | 0,001 | nenhum |  |
| `corpo_vazio` | 0,001 | nenhum |  |
| `chave_de_juncao_errada` | 0,001 | `entidade-produto` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `estado_da_tela_divergente` | 0,000 | `ancora-saiba-mais` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê o conteúdo do produto vizinho ao clicar no "Saiba Mais...".
> FONTE: [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: colecao_no_lugar_de_objeto
CAMPO: id
IMPACTO: O usuário vê o conteúdo do produto vizinho ao clicar no "Saiba Mais...".
FONTE: [contrato-produto]
```

## Rastro

Gerado dos eventos 545 a 566 da trilha; hash dos eventos deste caso: `322098fc80ac1989` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-26.md`.
