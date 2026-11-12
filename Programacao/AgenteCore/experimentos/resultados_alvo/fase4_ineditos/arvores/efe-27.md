<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `efe-27`

Caso `efe-27` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/efe-27`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 25 afirmações (15 observado, 7 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1306 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1306 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4207 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (52,85), `contrato-produto` (33,22) e `nulo_inesperado` (32,80) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; `nulo_inesperado` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (28,94), `estado_da_tela_divergente` (26,25), `tipo_divergente` (25,02), `estrutura_aninhada_divergente` (24,89) e `tempo_de_resposta_excedido` (23,85) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 77 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `nulo_inesperado`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (32,80 contra 26,94); a diferença final foi 3,86 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 52,85: 49,85 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 33,22: 30,22 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `nulo_inesperado` | posição 3, pontuação 32,80: 32,80 pelas palavras do caso, sem reforço | sim |
| `pagina-produtos-api` | posição 4, pontuação 28,94: 26,94 pelas palavras do caso, mais 2,0 por rota |  |
| `estado_da_tela_divergente` | posição 5, pontuação 26,25: 26,25 pelas palavras do caso, sem reforço |  |
| `tipo_divergente` | posição 6, pontuação 25,02: 24,02 pelas palavras do caso, mais 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 7, pontuação 24,89: 23,89 pelas palavras do caso, mais 1,0 por entidade |  |
| `tempo_de_resposta_excedido` | posição 8, pontuação 23,85: 22,85 pelas palavras do caso, mais 1,0 por status |  |

## Decisão 3: a causa

Escolha: `dado_desatualizado` (Dado desatualizado (cache)); segunda: `valor_fora_do_dominio`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `dado_desatualizado` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `valor_fora_do_dominio` (Valor fora do domínio), ficou com probabilidade 0,075 contra 0,875 da escolhida; verbetes entregues que a sustentam: `nulo_inesperado` (observado).
- As outras 12 alternativas lidas na resposta somam probabilidade 0,052; as maiores: `nulo_inesperado` (0,024), `campo_ausente` (0,009) e `campo_renomeado` (0,009) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,875, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/2`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `nulo_inesperado` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `nulo_inesperado`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida dado_desatualizado (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 8 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `dado_desatualizado` | 0,875 | nenhum | sim |
| `valor_fora_do_dominio` | 0,075 | `nulo_inesperado` |  |
| `nulo_inesperado` | 0,024 | `nulo_inesperado` |  |
| `campo_ausente` | 0,009 | `contrato-produto` e `nulo_inesperado` |  |
| `campo_renomeado` | 0,009 | `contrato-produto` |  |
| `formato_de_data_divergente` | 0,004 | nenhum |  |
| `tipo_divergente` | 0,002 | `entidade-produto` e `contrato-produto` |  |
| `tempo_de_resposta_excedido` | 0,002 | nenhum |  |
| `resposta_truncada` | 0,001 | nenhum |  |
| `registro_duplicado` | 0,001 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |
| `estado_da_tela_divergente` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um preço antigo no cartão, enquanto a página exibe o preço atualizado.
> FONTE: [contrato-produto], [nulo_inesperado]

Resposta inteira:

```text
CAUSA_RAIZ: dado_desatualizado
CAMPO: preco
IMPACTO: O usuário vê um preço antigo no cartão, enquanto a página exibe o preço atualizado.
FONTE: [contrato-produto], [nulo_inesperado]
```

## Rastro

Gerado dos eventos 860 a 885 da trilha; hash dos eventos deste caso: `624dd17b154dd46a` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/efe-27.md`.
