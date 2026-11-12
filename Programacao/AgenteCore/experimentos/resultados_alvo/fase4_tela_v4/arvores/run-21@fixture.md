<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `run-21`

Caso `run-21` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/run-21@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 25 afirmações (15 observado, 7 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (994 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (994 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4085 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (88,57), `contrato-produto` (57,95) e `tipo_divergente` (33,17) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `tipo_divergente`; o da entidade, em `entidade-produto`, `contrato-produto` e `tipo_divergente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estrutura_aninhada_divergente` (30,41), `chave_de_juncao_errada` (29,35), `nulo_inesperado` (28,94), `campo_ausente` (26,88) e `colecao_no_lugar_de_objeto` (26,78) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 82 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `tipo_divergente`, e o primeiro de fora, `estrutura_aninhada_divergente`, só o texto do caso já punha o primeiro à frente (30,17 contra 27,41), e os reforços em código levaram a diferença a 2,77 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 88,57: 85,57 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 57,95: 54,95 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `tipo_divergente` | posição 3, pontuação 33,17: 30,17 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 4, pontuação 30,41: 27,41 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 5, pontuação 29,35: 27,35 pelas palavras do caso, mais 2,0 por rota |  |
| `nulo_inesperado` | posição 6, pontuação 28,94: 26,94 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_ausente` | posição 7, pontuação 26,88: 23,88 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 8, pontuação 26,78: 23,78 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `registro_duplicado` (Registro duplicado); segunda: `colecao_no_lugar_de_objeto`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `registro_duplicado` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)), ficou com probabilidade 0,076 contra 0,895 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,031; as maiores: `campo_ausente` (0,010), `campo_renomeado` (0,010) e `resposta_truncada` (0,003) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,895, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `entidade-produto` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `entidade-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 8 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `registro_duplicado` | 0,895 | nenhum | sim |
| `colecao_no_lugar_de_objeto` | 0,076 | `contrato-produto` |  |
| `campo_ausente` | 0,010 | `contrato-produto` |  |
| `campo_renomeado` | 0,010 | `contrato-produto` |  |
| `resposta_truncada` | 0,003 | nenhum |  |
| `corpo_nao_e_json` | 0,002 | nenhum |  |
| `corpo_vazio` | 0,002 | nenhum |  |
| `tipo_divergente` | 0,002 | `entidade-produto`, `contrato-produto` e `tipo_divergente` |  |
| `recurso_inexistente` | 0,001 | `contrato-produto` |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` |  |
| `valor_fora_do_dominio` | 0,000 | `tipo_divergente` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê a Picanha ao Alho listada duas vezes seguidas, causando redundância na exibição dos produtos.
> FONTE: [contrato-produto] [entidade-produto]

Resposta inteira:

```text
CAUSA_RAIZ: registro_duplicado
CAMPO: id
IMPACTO: O usuário vê a Picanha ao Alho listada duas vezes seguidas, causando redundância na exibição dos produtos.
FONTE: [contrato-produto] [entidade-produto]
```

## Rastro

Gerado dos eventos 2171 a 2196 da trilha; hash dos eventos deste caso: `ecd6dbb1c7ca8a5b` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/run-21@fixture.md`.
