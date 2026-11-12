<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `lex-24`

Caso `lex-24` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/lex-24`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 25 afirmações (15 observado, 7 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (572 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (572 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3606 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (31,35), `contrato-produto` (26,07) e `estado_da_tela_divergente` (22,21) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; `estado_da_tela_divergente` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `tipo_divergente` (17,22), `estrutura_aninhada_divergente` (16,69), `colecao_no_lugar_de_objeto` (15,92), `campo_renomeado` (15,88) e `pagina-produtos-api` (15,87) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 49 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `estado_da_tela_divergente`, e o primeiro de fora, `tipo_divergente`, só o texto do caso já punha o primeiro à frente (22,21 contra 16,22); a diferença final foi 4,99 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 31,35: 28,35 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 26,07: 23,07 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estado_da_tela_divergente` | posição 3, pontuação 22,21: 22,21 pelas palavras do caso, sem reforço | sim |
| `tipo_divergente` | posição 4, pontuação 17,22: 16,22 pelas palavras do caso, mais 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 5, pontuação 16,69: 15,69 pelas palavras do caso, mais 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 15,92: 12,92 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_renomeado` | posição 7, pontuação 15,88: 14,88 pelas palavras do caso, mais 1,0 por entidade |  |
| `pagina-produtos-api` | posição 8, pontuação 15,87: 13,87 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `codificacao_incorreta` (Codificação de caracteres incorreta); segunda: `formato_de_data_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `codificacao_incorreta` (declarado).
- O modelo apontou o campo `resumo` (declarado).
- `resumo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `formato_de_data_divergente` (Formato de data divergente), ficou com probabilidade 0,000 contra 0,999 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `tipo_divergente` (0,000), `campo_ausente` (0,000) e `campo_renomeado` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,999, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/14`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `entidade-produto` e `contrato-produto` (declarado).
- Os 2 verbetes citados (`entidade-produto` e `contrato-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Camada de leitura de cada verbete citado: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 8 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `codificacao_incorreta` | 0,999 | nenhum | sim |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `tipo_divergente` | 0,000 | `entidade-produto` e `contrato-produto` |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | `estado_da_tela_divergente` |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O texto de descrição do Abacaxi na Brasa aparece corrompido com símbolos estranhos.
> FONTE: [entidade-produto], [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: codificacao_incorreta
CAMPO: resumo
IMPACTO: O texto de descrição do Abacaxi na Brasa aparece corrompido com símbolos estranhos.
FONTE: [entidade-produto], [contrato-produto]
```

## Rastro

Gerado dos eventos 49 a 74 da trilha; hash dos eventos deste caso: `a8c4e961f75bf6bd` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/lex-24.md`.
