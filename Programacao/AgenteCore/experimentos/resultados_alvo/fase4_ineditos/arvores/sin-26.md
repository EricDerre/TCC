<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `sin-26`

Caso `sin-26` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/sin-26`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 25 afirmações (15 observado, 7 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (961 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (961 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3917 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (67,86), `contrato-produto` (66,00) e `campo_ausente` (45,13) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `campo_ausente`; o da entidade, em `entidade-produto`, `contrato-produto` e `campo_ausente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `nulo_inesperado` (37,38), `campo_renomeado` (32,69), `chave_de_juncao_errada` (31,71), `campo_preco_ausente` (29,31) e `pagina-produtos-api` (29,10) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 89 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `campo_ausente`, e o primeiro de fora, `nulo_inesperado`, só o texto do caso já punha o primeiro à frente (42,13 contra 35,38), e os reforços em código levaram a diferença a 7,75 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 67,86: 64,86 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 66,00: 63,00 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_ausente` | posição 3, pontuação 45,13: 42,13 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `nulo_inesperado` | posição 4, pontuação 37,38: 35,38 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_renomeado` | posição 5, pontuação 32,69: 29,69 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 6, pontuação 31,71: 29,71 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_preco_ausente` | posição 7, pontuação 29,31: 28,31 pelas palavras do caso, mais 1,0 por entidade |  |
| `pagina-produtos-api` | posição 8, pontuação 29,10: 27,10 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `resposta_truncada` (Resposta truncada); segunda: `campo_ausente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `resposta_truncada` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,020 contra 0,950 da escolhida; verbetes entregues que a sustentam: `contrato-produto` e `campo_ausente` (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,055; as maiores: `campo_renomeado` (0,020), `corpo_nao_e_json` (0,010) e `corpo_vazio` (0,010) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,950, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `campo_ausente` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `campo_ausente`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 8 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `resposta_truncada` | 0,950 | nenhum | sim |
| `campo_ausente` | 0,020 | `contrato-produto` e `campo_ausente` |  |
| `campo_renomeado` | 0,020 | `contrato-produto` e `campo_ausente` |  |
| `corpo_nao_e_json` | 0,010 | nenhum |  |
| `corpo_vazio` | 0,010 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,008 | `contrato-produto` |  |
| `tipo_divergente` | 0,004 | `entidade-produto` e `contrato-produto` |  |
| `contagem_inconsistente` | 0,001 | nenhum |  |
| `formato_de_data_divergente` | 0,001 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,000 | `campo_ausente` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê preços incorretos ou 'undefined' para alguns produtos, devido à lista truncada.
> FONTE: [contrato-produto], [campo_ausente]

Resposta inteira:

```text
CAUSA_RAIZ: resposta_truncada
CAMPO: preco
IMPACTO: O usuário vê preços incorretos ou 'undefined' para alguns produtos, devido à lista truncada.
FONTE: [contrato-produto], [campo_ausente]
```

## Rastro

Gerado dos eventos 249 a 274 da trilha; hash dos eventos deste caso: `43855b1f6738e30c` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/sin-26.md`.
