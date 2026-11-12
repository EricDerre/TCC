<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `tra-19`

Caso `tra-19` da corrida `fase4_tela_v4`, trilha `fase4_tela_v4/qwen2.5_7b/tra-19@fixture`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (552 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (552 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3453 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (29,69), `contrato-produto` (24,24) e `nulo_inesperado` (20,77) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `nulo_inesperado`; o da entidade, em `entidade-produto` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (20,41), `tipo_divergente` (19,06), `estado_da_tela_divergente` (18,20), `escala_ou_unidade_errada` (16,75) e `chave_de_juncao_errada` (15,54) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 48 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `nulo_inesperado`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (18,77 contra 18,41), e os reforços em código levaram a diferença a 0,36 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 29,69: 26,69 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 24,24: 21,24 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `nulo_inesperado` | posição 3, pontuação 20,77: 18,77 pelas palavras do caso, mais 2,0 por rota | sim |
| `pagina-produtos-api` | posição 4, pontuação 20,41: 18,41 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 5, pontuação 19,06: 16,06 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estado_da_tela_divergente` | posição 6, pontuação 18,20: 18,20 pelas palavras do caso, sem reforço |  |
| `escala_ou_unidade_errada` | posição 7, pontuação 16,75: 13,75 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 8, pontuação 15,54: 13,54 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `escala_ou_unidade_errada` (Escala ou unidade errada); segunda: `valor_fora_do_dominio`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `escala_ou_unidade_errada` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `valor_fora_do_dominio` (Valor fora do domínio), ficou com probabilidade 0,167 contra 0,612 da escolhida; verbetes entregues que a sustentam: `nulo_inesperado` (observado).
- As outras 6 alternativas lidas na resposta somam probabilidade 0,219; as maiores: `formato_de_data_divergente` (0,132), `tipo_divergente` (0,087) e `campo_ausente` (0,000) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,612, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `entidade-produto` e `contrato-produto` (declarado).
- Os 2 verbetes citados (`entidade-produto` e `contrato-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `entidade-produto` (conferido).
- Camada de leitura de cada verbete citado: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 9 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `escala_ou_unidade_errada` | 0,612 | `entidade-produto` | sim |
| `valor_fora_do_dominio` | 0,167 | `nulo_inesperado` |  |
| `formato_de_data_divergente` | 0,132 | nenhum |  |
| `tipo_divergente` | 0,087 | `entidade-produto` e `contrato-produto` |  |
| `campo_ausente` | 0,000 | `contrato-produto` e `nulo_inesperado` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |
| `nulo_inesperado` | 0,000 | `nulo_inesperado` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê o preço do Balde de Cerveja como R$ 4,50, quando na verdade é R$ 45,00.
> FONTE: [entidade-produto] [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: escala_ou_unidade_errada
CAMPO: preco
IMPACTO: O usuário vê o preço do Balde de Cerveja como R$ 4,50, quando na verdade é R$ 45,00.
FONTE: [entidade-produto] [contrato-produto]
```

## Rastro

Gerado dos eventos 1944 a 1969 da trilha; hash dos eventos deste caso: `1399badeeb895964` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/tra-19@fixture.md`.
