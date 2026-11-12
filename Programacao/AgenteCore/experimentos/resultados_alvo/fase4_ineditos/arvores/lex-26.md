<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-26`

Caso `lex-26` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/lex-26`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 25 afirmações (15 observado, 7 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (841 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (841 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3654 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (59,44), `campo_ausente` (37,02) e `pagina-produtos-api` (31,67) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `pagina-produtos-api`; o da entidade, em `entidade-produto` e `campo_ausente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `contrato-produto` (31,57), `codificacao_incorreta` (29,36), `colecao_no_lugar_de_objeto` (27,63), `registro_duplicado` (27,50) e `estado_da_tela_divergente` (27,44) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 81 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `pagina-produtos-api`, e o primeiro de fora, `contrato-produto`, só o texto do caso já punha o primeiro à frente (29,67 contra 28,57), e os reforços em código levaram a diferença a 0,09 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 59,44: 56,44 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_ausente` | posição 2, pontuação 37,02: 36,02 pelas palavras do caso, mais 1,0 por entidade | sim |
| `pagina-produtos-api` | posição 3, pontuação 31,67: 29,67 pelas palavras do caso, mais 2,0 por rota | sim |
| `contrato-produto` | posição 4, pontuação 31,57: 28,57 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `codificacao_incorreta` | posição 5, pontuação 29,36: 29,36 pelas palavras do caso, sem reforço |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 27,63: 24,63 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `registro_duplicado` | posição 7, pontuação 27,50: 27,50 pelas palavras do caso, sem reforço |  |
| `estado_da_tela_divergente` | posição 8, pontuação 27,44: 27,44 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `codificacao_incorreta` (Codificação de caracteres incorreta); segunda: `campo_ausente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `codificacao_incorreta` (declarado).
- O modelo apontou o campo `nome` (declarado).
- `nome` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,000 contra 1,000 da escolhida; verbetes entregues que a sustentam: `campo_ausente` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_renomeado` (0,000), `formato_de_data_divergente` (0,000) e `chave_de_juncao_errada` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 1,000, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/11`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `campo_ausente` e `entidade-produto` (declarado).
- Os 2 verbetes citados (`campo_ausente` e `entidade-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Camada de leitura de cada verbete citado: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 8 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `codificacao_incorreta` | 1,000 | nenhum | sim |
| `campo_ausente` | 0,000 | `campo_ausente` |  |
| `campo_renomeado` | 0,000 | `campo_ausente` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` |  |
| `tipo_divergente` | 0,000 | `entidade-produto` e `pagina-produtos-api` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | `pagina-produtos-api` |  |
| `estrutura_aninhada_divergente` | 0,000 | `campo_ausente` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê o título do cartão corretamente, mas o modal exibe o título com caracteres estranhos.
> FONTE: [campo_ausente] [entidade-produto]

Resposta inteira:

```text
CAUSA_RAIZ: codificacao_incorreta
CAMPO: nome
IMPACTO: O usuário vê o título do cartão corretamente, mas o modal exibe o título com caracteres estranhos.
FONTE: [campo_ausente] [entidade-produto]
```

## Rastro

Gerado dos eventos 103 a 128 da trilha; hash dos eventos deste caso: `3db8657b1dba4adb` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-26.md`.
