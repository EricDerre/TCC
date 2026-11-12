<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `localizador-front-admin-produtos#1`

Caso `localizador-front-admin-produtos#1` da corrida `fase4_ensaio_v4`, trilha `fase4_ensaio_v4/qwen2.5_7b/localizador-front-admin-produtos#1`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 4 decisões e 33 afirmações (24 observado, 5 conferido, 3 declarado, 1 desconhecido); há divergência entre o declarado e o conferido; houve cura de localizador; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (38 linhas), não a página inteira.

- A poda da árvore de acessibilidade da tela levou 170 nós a 38 linhas (observado).
- O que saiu, pelas regras em código: 14 imagens removidas, 3 botões e campos sem nome acessível removidos e 116 listas e grupos achatados (fica só o conteúdo) (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3766 caracteres (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 170 nós |  |
| a árvore podada | 38 linhas | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `localizador_quebrado` (44,27), `valor_fora_do_dominio` (11,20) e `tempo_de_resposta_excedido` (11,05) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da entidade entrou em `localizador_quebrado`; o do status, em `tempo_de_resposta_excedido`; `valor_fora_do_dominio` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `contagem_inconsistente` (10,37), `limites-do-sistema` (9,83), `nulo_inesperado` (9,12), `corpo_nao_e_json` (9,09) e `colecao_no_lugar_de_objeto` (7,80) (observado).
- Sinais da consulta, tirados do caso em código: rota nenhuma, entidade `Interface`, status 200 e 56 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `tempo_de_resposta_excedido`, e o primeiro de fora, `contagem_inconsistente`, só pelo texto do caso o segundo estaria à frente (10,37 contra 10,05); os reforços em código viraram a ordem, com diferença final de 0,67 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `localizador_quebrado` | posição 1, pontuação 44,27: 43,27 pelas palavras do caso, mais 1,0 por entidade | sim |
| `valor_fora_do_dominio` | posição 2, pontuação 11,20: 11,20 pelas palavras do caso, sem reforço | sim |
| `tempo_de_resposta_excedido` | posição 3, pontuação 11,05: 10,05 pelas palavras do caso, mais 1,0 por status | sim |
| `contagem_inconsistente` | posição 4, pontuação 10,37: 10,37 pelas palavras do caso, sem reforço |  |
| `limites-do-sistema` | posição 5, pontuação 9,83: 9,83 pelas palavras do caso, sem reforço |  |
| `nulo_inesperado` | posição 6, pontuação 9,12: 9,12 pelas palavras do caso, sem reforço |  |
| `corpo_nao_e_json` | posição 7, pontuação 9,09: 8,09 pelas palavras do caso, mais 1,0 por status |  |
| `colecao_no_lugar_de_objeto` | posição 8, pontuação 7,80: 7,80 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `localizador_quebrado` (Localizador (seletor) quebrado); segunda: `tempo_de_resposta_excedido`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `localizador_quebrado` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `tempo_de_resposta_excedido` (Tempo de resposta excedido), ficou com probabilidade 0,000 contra 0,994 da escolhida; verbetes entregues que a sustentam: `tempo_de_resposta_excedido` (observado).
- A outra alternativa lida na resposta, `nulo_inesperado`, tem probabilidade 0,000 (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,994, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- A trilha não aponta um sinal medido em código para esta causa (desconhecido).
- A linha FONTE cita `localizador_quebrado` (declarado).
- Verbete citado `localizador_quebrado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `localizador_quebrado` (conferido).
- Leitura do verbete `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 12 de 12 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `localizador_quebrado` | 0,994 | `localizador_quebrado` | sim |
| `tempo_de_resposta_excedido` | 0,000 | `tempo_de_resposta_excedido` |  |
| `nulo_inesperado` | 0,000 | `valor_fora_do_dominio` |  |

## Decisão 4: a cura

Escolha: `papel_e_nome_parecido` (`role=button[name=" EXCLUIR ITEM"] >> nth=0`).

- O passo 11 do roteiro, localizador `role=button[name=/EXCLUIR$/] >> nth=0`, falhou: o navegador não achou o elemento (a mensagem dele está em citação abaixo) (observado).
- Dos 6 candidatos previstos, 5 foram gerados da árvore podada e do alvo da referência, e 4 passaram nas quatro checagens em código (um elemento só, visível e habilitado, mesmo papel e nome parecido acima de 0,6) (observado).
- Aplicado `papel_e_nome_parecido` (`role=button[name=" EXCLUIR ITEM"] >> nth=0`): o elemento é achado pelo papel igual e pelo nome parecido com o do alvo; passou as 5 verificações em código: um elemento só, visível e habilitado, mesmo papel, nome parecido e efeito na reexecução (observado).
- A reexecução foi validada: o roteiro chegou ao fim com o localizador novo, e é o mesmo elemento da referência (observado).
- Outros 3 candidatos, `data_id`, `caminho_do_ancestral_com_id` e `posicao_entre_irmaos`, também passaram nas quatro checagens e não foram tentados, porque o primeiro já tinha fechado o roteiro (observado).
- Não foi gerado: `papel_e_nome` (a árvore podada não tem button " EXCLUIR") (observado).
- Da detecção à reexecução validada: 66,4 s (observado).
- Divergência registrada no nó da cura: o aplicado foi `papel_e_nome_parecido` (role=button[name=" EXCLUIR ITEM"] >> nth=0); o segundo candidato, `data_id` (button[data-id="1"]), também passou as verificações estáticas e não foi tentado: a ordem fixa decidiu, não a verificação (observado).

Mensagem do navegador, como veio:

> TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("role=button[name=/EXCLUIR$/]").first

| Candidato | Seletor | Verificações que passou | O que aconteceu | Aplicado |
|---|---|---|---|---|
| `papel_e_nome` | não gerado | 0 | não gerado: a árvore podada não tem button " EXCLUIR" |  |
| `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | 5 | gerado; passou as verificações estáticas; aplicado: levou o roteiro ao fim na reexecução | sim |
| `texto_contido` | `text=EXCLUIR >> nth=0` | 3 | gerado; não passou as verificações estáticas |  |
| `data_id` | `button[data-id="1"]` | 4 | gerado; passou as verificações estáticas; não foi tentado: passou as verificações estáticas, mas um candidato anterior já tinha levado o roteiro ao fim |  |
| `caminho_do_ancestral_com_id` | `body > main:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(7) > button:nth-of-type(1)` | 4 | gerado; passou as verificações estáticas; não foi tentado: passou as verificações estáticas, mas um candidato anterior já tinha levado o roteiro ao fim |  |
| `posicao_entre_irmaos` | `body > main:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(7) >> role=button >> nth=1` | 4 | gerado; passou as verificações estáticas; não foi tentado: passou as verificações estáticas, mas um candidato anterior já tinha levado o roteiro ao fim |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário não consegue clicar no botão de exclusão, resultando em uma interação ineficaz com a interface.
> FONTE: [localizador_quebrado]

Resposta inteira:

```text
CAUSA_RAIZ: localizador_quebrado
CAMPO: nenhum
IMPACTO: O usuário não consegue clicar no botão de exclusão, resultando em uma interação ineficaz com a interface.
FONTE: [localizador_quebrado]
```

## Rastro

Gerado dos eventos 313 a 368 da trilha; hash dos eventos deste caso: `f0548bfd6fb24b0e` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/localizador-front-admin-produtos__r1.md`.
