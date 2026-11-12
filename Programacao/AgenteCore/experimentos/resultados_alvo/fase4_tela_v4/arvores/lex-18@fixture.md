<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-18`

Caso `lex-18` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/lex-18@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 25 afirmações (15 observado, 7 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (710 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (710 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3744 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-produto` (38,13), `entidade-produto` (35,89) e `estado_da_tela_divergente` (26,71) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto` e `entidade-produto`; o da entidade, em `contrato-produto` e `entidade-produto`; `estado_da_tela_divergente` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `campo_renomeado` (25,75), `campo_ausente` (22,75), `pagina-produtos-api` (21,62), `nulo_inesperado` (21,53) e `estrutura_aninhada_divergente` (21,38) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 64 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `estado_da_tela_divergente`, e o primeiro de fora, `campo_renomeado`, só o texto do caso já punha o primeiro à frente (26,71 contra 22,75); a diferença final foi 0,96 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-produto` | posição 1, pontuação 38,13: 35,13 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 2, pontuação 35,89: 32,89 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estado_da_tela_divergente` | posição 3, pontuação 26,71: 26,71 pelas palavras do caso, sem reforço | sim |
| `campo_renomeado` | posição 4, pontuação 25,75: 22,75 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_ausente` | posição 5, pontuação 22,75: 19,75 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `pagina-produtos-api` | posição 6, pontuação 21,62: 19,62 pelas palavras do caso, mais 2,0 por rota |  |
| `nulo_inesperado` | posição 7, pontuação 21,53: 19,53 pelas palavras do caso, mais 2,0 por rota |  |
| `estrutura_aninhada_divergente` | posição 8, pontuação 21,38: 18,38 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `valor_fora_do_dominio` (Valor fora do domínio); segunda: `campo_ausente`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `valor_fora_do_dominio` (declarado).
- O modelo apontou o campo `resumo` (declarado).
- `resumo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,216 contra 0,423 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 10 alternativas lidas na resposta somam probabilidade 0,563; as maiores: `campo_renomeado` (0,216), `codificacao_incorreta` (0,133) e `formato_de_data_divergente` (0,091) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,423, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `entidade-produto` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `entidade-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida valor_fora_do_dominio (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 8 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `valor_fora_do_dominio` | 0,423 | nenhum | sim |
| `campo_ausente` | 0,216 | `contrato-produto` |  |
| `campo_renomeado` | 0,216 | `contrato-produto` |  |
| `codificacao_incorreta` | 0,133 | nenhum |  |
| `formato_de_data_divergente` | 0,091 | nenhum |  |
| `chave_de_juncao_errada` | 0,075 | `entidade-produto` |  |
| `tipo_divergente` | 0,045 | `contrato-produto` e `entidade-produto` |  |
| `nulo_inesperado` | 0,001 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | `estado_da_tela_divergente` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O resumo exibido na tela contém caracteres errados, indicando um problema de codificação.
> FONTE: [contrato-produto], [entidade-produto]

Resposta inteira:

```text
CAUSA_RAIZ: valor_fora_do_dominio
CAMPO: resumo
IMPACTO: O resumo exibido na tela contém caracteres errados, indicando um problema de codificação.
FONTE: [contrato-produto], [entidade-produto]
```

## Rastro

Gerado dos eventos 1387 a 1412 da trilha; hash dos eventos deste caso: `96654751dc17f0d0` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-18@fixture.md`.
