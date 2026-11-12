<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `run-25`

Caso `run-25` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/run-25`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (668 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (668 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3593 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (25,86), `ancora-saiba-mais` (25,37) e `contrato-produto` (24,97) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; `ancora-saiba-mais` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estado_da_tela_divergente` (21,66), `pagina-produtos-api` (20,97), `colecao_no_lugar_de_objeto` (20,82), `tempo_de_resposta_excedido` (16,07) e `usuario-e-login` (15,52) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 58 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `estado_da_tela_divergente`, só o texto do caso já punha o primeiro à frente (21,97 contra 21,66), e os reforços em código levaram a diferença a 3,31 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 25,86: 22,86 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `ancora-saiba-mais` | posição 2, pontuação 25,37: 25,37 pelas palavras do caso, sem reforço | sim |
| `contrato-produto` | posição 3, pontuação 24,97: 21,97 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estado_da_tela_divergente` | posição 4, pontuação 21,66: 21,66 pelas palavras do caso, sem reforço |  |
| `pagina-produtos-api` | posição 5, pontuação 20,97: 18,97 pelas palavras do caso, mais 2,0 por rota |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 20,82: 17,82 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tempo_de_resposta_excedido` | posição 7, pontuação 16,07: 15,07 pelas palavras do caso, mais 1,0 por status |  |
| `usuario-e-login` | posição 8, pontuação 15,52: 15,52 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `tempo_de_resposta_excedido` (Tempo de resposta excedido); segunda: `tipo_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `tempo_de_resposta_excedido` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,115 contra 0,832 da escolhida; verbetes entregues que a sustentam: `entidade-produto` e `contrato-produto` (observado).
- As outras 11 alternativas lidas na resposta somam probabilidade 0,055; as maiores: `colecao_no_lugar_de_objeto` (0,015), `resposta_truncada` (0,015) e `campo_ausente` (0,008) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,832, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/7`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `ancora-saiba-mais` (declarado).
- Verbete citado `ancora-saiba-mais`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), não traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Leitura do verbete `ancora-saiba-mais` (Link "Saiba Mais..." abre produto vazio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/defeitos_conhecidos/ancora-saiba-mais.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/defeitos_conhecidos/ancora-saiba-mais.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida tempo_de_resposta_excedido (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 5 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `tempo_de_resposta_excedido` | 0,832 | nenhum | sim |
| `tipo_divergente` | 0,115 | `entidade-produto` e `contrato-produto` |  |
| `colecao_no_lugar_de_objeto` | 0,015 | `contrato-produto` |  |
| `resposta_truncada` | 0,015 | nenhum |  |
| `campo_ausente` | 0,008 | `contrato-produto` |  |
| `campo_renomeado` | 0,008 | `contrato-produto` |  |
| `formato_de_data_divergente` | 0,005 | nenhum |  |
| `valor_fora_do_dominio` | 0,002 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |
| `estado_da_tela_divergente` | 0,000 | `ancora-saiba-mais` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um modal demorado a abrir, com dados corretos, após um breve tempo de espera.
> FONTE: [ancora-saiba-mais]

Resposta inteira:

```text
CAUSA_RAIZ: tempo_de_resposta_excedido
CAMPO: nenhum
IMPACTO: O usuário vê um modal demorado a abrir, com dados corretos, após um breve tempo de espera.
FONTE: [ancora-saiba-mais]
```

## Rastro

Gerado dos eventos 668 a 689 da trilha; hash dos eventos deste caso: `08fa9d48a150a287` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/run-25.md`.
