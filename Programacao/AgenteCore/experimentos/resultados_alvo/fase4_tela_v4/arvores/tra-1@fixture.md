<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-1`

Caso `tra-1` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/tra-1@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (537 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (537 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3896 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (39,43), `escala_ou_unidade_errada` (26,27) e `contrato-produto` (24,24) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `escala_ou_unidade_errada` e `contrato-produto`; o da entidade, em `entidade-produto`, `escala_ou_unidade_errada` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estrutura_aninhada_divergente` (18,66), `tipo_divergente` (18,32), `estado_da_tela_divergente` (18,20), `nulo_inesperado` (17,94) e `pagina-produtos-api` (17,70) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 42 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `estrutura_aninhada_divergente`, só o texto do caso já punha o primeiro à frente (21,24 contra 15,66), e os reforços em código levaram a diferença a 5,58 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 39,43: 36,43 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `escala_ou_unidade_errada` | posição 2, pontuação 26,27: 23,27 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 3, pontuação 24,24: 21,24 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 4, pontuação 18,66: 15,66 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tipo_divergente` | posição 5, pontuação 18,32: 15,32 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estado_da_tela_divergente` | posição 6, pontuação 18,20: 18,20 pelas palavras do caso, sem reforço |  |
| `nulo_inesperado` | posição 7, pontuação 17,94: 15,94 pelas palavras do caso, mais 2,0 por rota |  |
| `pagina-produtos-api` | posição 8, pontuação 17,70: 15,70 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `escala_ou_unidade_errada` (Escala ou unidade errada); segunda: `valor_fora_do_dominio`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `escala_ou_unidade_errada` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `valor_fora_do_dominio` (Valor fora do domínio), ficou com probabilidade 0,002 contra 0,996 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 6 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `tipo_divergente` (0,000), `formato_de_data_divergente` (0,000) e `estrutura_aninhada_divergente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,996, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `escala_ou_unidade_errada` (declarado).
- Verbete citado `escala_ou_unidade_errada`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `entidade-produto` e `escala_ou_unidade_errada` (conferido).
- Leitura do verbete `escala_ou_unidade_errada` (Escala ou unidade errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/escala_ou_unidade_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/escala_ou_unidade_errada.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `escala_ou_unidade_errada` | 0,996 | `entidade-produto` e `escala_ou_unidade_errada` | sim |
| `valor_fora_do_dominio` | 0,002 | nenhum |  |
| `tipo_divergente` | 0,000 | `entidade-produto`, `escala_ou_unidade_errada` e `contrato-produto` |  |
| `formato_de_data_divergente` | 0,000 | `escala_ou_unidade_errada` |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `estado_da_tela_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê preços cem vezes maiores do que o esperado, como 'R$ 8.990,00' para a picanha.
> FONTE: [escala_ou_unidade_errada]

Resposta inteira:

```text
CAUSA_RAIZ: escala_ou_unidade_errada
CAMPO: preco
IMPACTO: O usuário vê preços cem vezes maiores do que o esperado, como 'R$ 8.990,00' para a picanha.
FONTE: [escala_ou_unidade_errada]
```

## Rastro

Gerado dos eventos 354 a 375 da trilha; hash dos eventos deste caso: `d1a0cc4fb48146cc` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-1@fixture.md`.
