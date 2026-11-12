<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `localizador-front-cliente-reserva#1`

Caso `localizador-front-cliente-reserva#1` da corrida `fase4_ensaio_v4`, trilha `fase4_ensaio_v4/qwen2.5_7b/localizador-front-cliente-reserva#1`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 4 decisões e 33 afirmações (24 observado, 5 conferido, 3 declarado, 1 desconhecido); há divergência entre o declarado e o conferido; houve cura de localizador; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: mandar ao modelo a árvore de acessibilidade podada (14 linhas), não a página inteira.

- A poda da árvore de acessibilidade da tela levou 36 nós a 14 linhas (observado).
- O que saiu, pelas regras em código: 1 elemento de decoração removido (separador, moldura ou figura) e 13 listas e grupos achatados (fica só o conteúdo) (observado).
- O que ficou: os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos da página, na forma textual dos casos escritos (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4116 caracteres (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| a árvore de acessibilidade inteira | 36 nós |  |
| a árvore podada | 14 linhas | sim |

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `localizador_quebrado` (31,60), `corpo_nao_e_json` (26,05) e `resposta_truncada` (13,07) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da entidade entrou em `localizador_quebrado`; o do status, em `corpo_nao_e_json`; `resposta_truncada` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `tempo_de_resposta_excedido` (12,10), `limites-do-sistema` (10,90), `colecao_no_lugar_de_objeto` (7,80), `dado_desatualizado` (6,29) e `consultas-sem-checagem` (5,57) (observado).
- Sinais da consulta, tirados do caso em código: rota nenhuma, entidade `Interface`, status 200 e 49 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `resposta_truncada`, e o primeiro de fora, `tempo_de_resposta_excedido`, só o texto do caso já punha o primeiro à frente (13,07 contra 11,10); a diferença final foi 0,97 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `localizador_quebrado` | posição 1, pontuação 31,60: 30,60 pelas palavras do caso, mais 1,0 por entidade | sim |
| `corpo_nao_e_json` | posição 2, pontuação 26,05: 25,05 pelas palavras do caso, mais 1,0 por status | sim |
| `resposta_truncada` | posição 3, pontuação 13,07: 13,07 pelas palavras do caso, sem reforço | sim |
| `tempo_de_resposta_excedido` | posição 4, pontuação 12,10: 11,10 pelas palavras do caso, mais 1,0 por status |  |
| `limites-do-sistema` | posição 5, pontuação 10,90: 10,90 pelas palavras do caso, sem reforço |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 7,80: 7,80 pelas palavras do caso, sem reforço |  |
| `dado_desatualizado` | posição 7, pontuação 6,29: 5,29 pelas palavras do caso, mais 1,0 por status |  |
| `consultas-sem-checagem` | posição 8, pontuação 5,57: 5,57 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `localizador_quebrado` (Localizador (seletor) quebrado); segunda: `tempo_de_resposta_excedido`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `localizador_quebrado` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `tempo_de_resposta_excedido` (Tempo de resposta excedido), ficou com probabilidade 0,000 contra 0,998 da escolhida; verbetes entregues que a sustentam: `resposta_truncada` (observado).
- As outras 2 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `estado_da_tela_divergente` (0,000) e `nulo_inesperado` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,998, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
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
- Conferências em código com veredito: 9 de 9 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `localizador_quebrado` | 0,998 | `localizador_quebrado` | sim |
| `tempo_de_resposta_excedido` | 0,000 | `resposta_truncada` |  |
| `estado_da_tela_divergente` | 0,000 | `localizador_quebrado` |  |
| `nulo_inesperado` | 0,000 | nenhum |  |

## Decisão 4: a cura

Escolha: `papel_e_nome` (`role=button[name="Reservar"]`).

- O passo 11 do roteiro, localizador `#reserva_login > input[type=submit]`, falhou: o navegador não achou o elemento (a mensagem dele está em citação abaixo) (observado).
- Dos 6 candidatos previstos, 4 foram gerados da árvore podada e do alvo da referência, e 3 passaram nas quatro checagens em código (um elemento só, visível e habilitado, mesmo papel e nome parecido acima de 0,6) (observado).
- Aplicado `papel_e_nome` (`role=button[name="Reservar"]`): o elemento é achado pelo papel e pelo nome acessíveis, iguais aos do alvo; passou as 5 verificações em código: um elemento só, visível e habilitado, mesmo papel, nome parecido e efeito na reexecução (observado).
- A reexecução foi validada: o roteiro chegou ao fim com o localizador novo, e é o mesmo elemento da referência (observado).
- Outros 2 candidatos, `texto_contido` e `posicao_entre_irmaos`, também passaram nas quatro checagens e não foram tentados, porque o primeiro já tinha fechado o roteiro (observado).
- Não foram gerados: `papel_e_nome_parecido` (nenhum button da árvore podada tem nome parecido com "Reservar" acima do limiar 0.6 (o mais próximo, " CANCELAR", fica em 0.33)); `data_id` (o alvo da referência não tem data-id) (observado).
- Da detecção à reexecução validada: 68,8 s (observado).
- Divergência registrada no nó da cura: o aplicado foi `papel_e_nome` (role=button[name="Reservar"]); o segundo candidato, `texto_contido` (text=Reservar), também passou as verificações estáticas e não foi tentado: a ordem fixa decidiu, não a verificação (observado).

Mensagem do navegador, como veio:

> TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("#reserva_login > input[type=submit]")

| Candidato | Seletor | Verificações que passou | O que aconteceu | Aplicado |
|---|---|---|---|---|
| `papel_e_nome` | `role=button[name="Reservar"]` | 5 | gerado; passou as verificações estáticas; aplicado: levou o roteiro ao fim na reexecução | sim |
| `papel_e_nome_parecido` | não gerado | 0 | não gerado: nenhum button da árvore podada tem nome parecido com "Reservar" acima do limiar 0.6 (o mais próximo, " CANCELAR", fica em 0.33) |  |
| `texto_contido` | `text=Reservar` | 4 | gerado; passou as verificações estáticas; não foi tentado: passou as verificações estáticas, mas um candidato anterior já tinha levado o roteiro ao fim |  |
| `data_id` | não gerado | 0 | não gerado: o alvo da referência não tem data-id |  |
| `caminho_do_ancestral_com_id` | `#reserva_login > input:nth-of-type(1)` | 0 | gerado; não passou as verificações estáticas |  |
| `posicao_entre_irmaos` | `#reserva_login >> role=button >> nth=0` | 4 | gerado; passou as verificações estáticas; não foi tentado: passou as verificações estáticas, mas um candidato anterior já tinha levado o roteiro ao fim |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário não consegue clicar no botão de login de reserva devido ao seletor quebrado, resultando em um TimeoutError.
> FONTE: [localizador_quebrado]

Resposta inteira:

```text
CAUSA_RAIZ: localizador_quebrado
CAMPO: nenhum
IMPACTO: O usuário não consegue clicar no botão de login de reserva devido ao seletor quebrado, resultando em um TimeoutError.
FONTE: [localizador_quebrado]
```

## Rastro

Gerado dos eventos 372 a 426 da trilha; hash dos eventos deste caso: `488b6fcc4671f9b1` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/localizador-front-cliente-reserva__r1.md`.
