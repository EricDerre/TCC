<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 31 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Registro duplicado em `GET /api/pedidos?login=11122233344`

Caso `relatorio-31` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-31`: o caso `relatorio-31` na corrida `fase4_ineditos`; eventos 714 a 739 da trilha `trilha_ineditos.jsonl`, hash dos eventos `efd2daf899ced71f` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Registro duplicado em `GET /api/pedidos?login=11122233344`

## 3. Data, organização e autor

Observado em 06/11/2026 14:26:30 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/pedidos?login=11122233344` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-31`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/pedidos?login=11122233344`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`.
3. Corpo da resposta:

```text
[{"id_pedido": 18, "pessoas": 4, "data_pedido": "2026-12-19", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 19, "pessoas": 4, "data_pedido": "2026-12-19", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

4. Sintoma observado (texto do caso):

> O roteiro envia POST /api/pedidos para uma reserva de 4 pessoas em 2026-12-19: a primeira tentativa respondeu 500, o roteiro tentou de novo e a segunda respondeu 201. A consulta GET /api/pedidos seguinte lista duas reservas identicas (ids 18 e 19, mesma data e mesmo numero de pessoas), embora so uma tenha sido pedida.

5. Observação adicional (texto do caso):

> O corpo mostra so as duas ultimas reservas do cliente. A resposta 500 da primeira tentativa nao trouxe nenhuma reserva, so uma mensagem de erro.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/pedidos?login=11122233344` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O roteiro envia POST /api/pedidos para uma reserva de 4 pessoas em 2026-12-19: a primeira tentativa respondeu 500, o roteiro tentou de novo e a segunda respondeu 201. A consulta GET /api/pedidos seguinte lista duas reservas identicas (ids 18 e 19, mesma data e mesmo numero de pessoas), embora so uma tenha sido pedida. |

Corpo recebido, como veio no caso:

```text
[{"id_pedido": 18, "pessoas": 4, "data_pedido": "2026-12-19", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 19, "pessoas": 4, "data_pedido": "2026-12-19", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`); `registro_duplicado` (Registro duplicado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/registro_duplicado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/registro_duplicado.md`).
- Verbetes entregues pela busca e não citados: `pedido-reserva` (Reserva de mesa (pedido); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/pedido-reserva.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/pedido-reserva.md`).
- Caso escrito: `relatorio-31` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-31` em `trilha_ineditos.jsonl`, eventos 714 a 739, hash dos eventos `efd2daf899ced71f`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `registro_duplicado` (Registro duplicado). Campo: nenhum apontado. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê duas reservas iguais na lista, embora tenha solicitado apenas uma.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu registro_duplicado porque os verbetes contrato-pedido, pedido-reserva, registro_duplicado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 18, "pessoas": 4, "data_pedido": "2026-12-19", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 19, "pessoas": 4, "data_pedido": "2026-12-19", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: O roteiro envia POST /api/pedidos para uma reserva de 4 pessoas em 2026-12-19: a primeira tentativa respondeu 500, o roteiro tentou de novo e a segunda respondeu 201. A consulta GET /api/pedidos seguinte lista duas reservas identicas (ids 18 e 19, mesma data e mesmo numero de pessoas), embora so uma tenha sido pedida.

OBSERVAÇÃO ADICIONAL: O corpo mostra so as duas ultimas reservas do cliente. A resposta 500 da primeira tentativa nao trouxe nenhuma reserva, so uma mensagem de erro.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> registro_duplicado e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-pedido, pedido-reserva, registro_duplicado

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `registro_duplicado` (Registro duplicado) | 1,00 | sim |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `erro_interno_do_servidor` (Erro interno do servidor (500)) | 0,00 |  |
| `recurso_inexistente` (Recurso inexistente (404 e vizinhos)) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido] [registro_duplicado]`; verbetes citados: `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`); `registro_duplicado` (Registro duplicado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/registro_duplicado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/registro_duplicado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado existe na biblioteca | `registro_duplicado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `registro_duplicado` |
| O verbete citado estava no contexto entregue ao modelo | `registro_duplicado` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `registro_duplicado` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | confere | verbetes: `registro_duplicado` |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-pedido] [registro_duplicado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-pedido", "registro_duplicado"]} |
| O verbete citado fala da causa respondida | `contrato-pedido` | não confere | {"termo": "registro_duplicado"} |
| O verbete citado fala da causa respondida | `registro_duplicado` | confere | {"termo": "registro_duplicado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 714 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:26:30 | caso relatorio-31 |
| 715 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:26:30 | 3 de 39 verbetes entregues |
| 717 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:26:30 | diagnostico: 3887 caracteres; verbetes contrato-pedido, pedido-reserva, registro_duplicado |
| 719 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:26:30 | diagnostico: 61,3 s |
| 720 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:26:30 | causa_raiz: `registro_duplicado` |
| 721 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:26:30 | campo: `nenhum` |
| 722 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:26:30 | impacto: `O usuário vê duas reservas iguais na lista, embora tenha solicitado apenas uma.` |
| 723 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:26:30 | fonte: `[contrato-pedido] [registro_duplicado]` |
| 724 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:26:30 | fonte_citada: `contrato-pedido` |
| 725 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T14:26:30 | fonte_citada: `registro_duplicado` |
| 726 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | quatro_linhas_presentes: confere |
| 727 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | rotulo_no_conjunto: confere |
| 728 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | fonte_existe_na_biblioteca: confere |
| 729 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | fonte_existe_na_biblioteca: confere |
| 730 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | fonte_estava_no_contexto: confere |
| 731 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | fonte_estava_no_contexto: confere |
| 732 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | campo_existe_no_caso: nao_se_aplica |
| 733 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 734 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | notas_nos_verbetes_citados: informativo |
| 735 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | impacto: nao_verificavel |
| 736 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | fonte_formato_valido: confere |
| 737 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | fonte_contem_termo_da_causa: nao_confere |
| 738 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T14:26:30 | fonte_contem_termo_da_causa: confere |
| 739 | 24 | decisao | programa | ao_vivo | 2026-11-06T14:26:30 | diagnostico: escolha registro_duplicado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 739, decisão `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido.
  - Evidência: evento 715 (verbete_entregue: `contrato-pedido`, `pedido-reserva`, `registro_duplicado`); evento 719 (resposta); evento 724 (verbete_citado: `contrato-pedido`); evento 725 (verbete_citado: `registro_duplicado`).
  - Usou: `contrato-pedido`, `pedido-reserva`, `registro_duplicado`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 714 a 739 da trilha; hash dos eventos deste caso: `efd2daf899ced71f`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-31`

Caso `relatorio-31` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-31`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1042 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1042 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3887 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-pedido` (86,29), `pedido-reserva` (55,12) e `registro_duplicado` (44,82) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-pedido`, `pedido-reserva` e `registro_duplicado`; o da entidade, em `contrato-pedido`, `pedido-reserva` e `registro_duplicado` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `valor_fora_do_dominio` (38,97), `formato_de_data_divergente` (38,89), `chave_de_juncao_errada` (38,22), `estado_da_tela_divergente` (37,16) e `fluxo-reserva-e-cancelamento` (33,15) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/pedidos`, entidade `Pedido`, status 200 e 101 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `registro_duplicado`, e o primeiro de fora, `valor_fora_do_dominio`, só o texto do caso já punha o primeiro à frente (41,82 contra 35,97), e os reforços em código levaram a diferença a 5,85 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-pedido` | posição 1, pontuação 86,29: 83,29 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pedido-reserva` | posição 2, pontuação 55,12: 52,12 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `registro_duplicado` | posição 3, pontuação 44,82: 41,82 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `valor_fora_do_dominio` | posição 4, pontuação 38,97: 35,97 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `formato_de_data_divergente` | posição 5, pontuação 38,89: 35,89 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 6, pontuação 38,22: 35,22 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estado_da_tela_divergente` | posição 7, pontuação 37,16: 37,16 pelas palavras do caso, sem reforço |  |
| `fluxo-reserva-e-cancelamento` | posição 8, pontuação 33,15: 32,15 pelas palavras do caso, mais 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `registro_duplicado` (Registro duplicado); segunda: `tipo_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `registro_duplicado` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 1,000 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 2 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `erro_interno_do_servidor` (0,000) e `recurso_inexistente` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 1,000, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/pedidos?login=11122233344`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-pedido` e `registro_duplicado` (declarado).
- Os 2 verbetes citados (`contrato-pedido` e `registro_duplicado`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `contrato-pedido` não confere; `registro_duplicado` confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `registro_duplicado` (conferido).
- Camada de leitura de cada verbete citado: `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`); `registro_duplicado` (Registro duplicado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/registro_duplicado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/registro_duplicado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 9 de 10 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `registro_duplicado` | 1,000 | `registro_duplicado` | sim |
| `tipo_divergente` | 0,000 | nenhum |  |
| `erro_interno_do_servidor` | 0,000 | nenhum |  |
| `recurso_inexistente` | 0,000 | `contrato-pedido` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê duas reservas iguais na lista, embora tenha solicitado apenas uma.
> FONTE: [contrato-pedido] [registro_duplicado]

Resposta inteira:

```text
CAUSA_RAIZ: registro_duplicado
CAMPO: nenhum
IMPACTO: O usuário vê duas reservas iguais na lista, embora tenha solicitado apenas uma.
FONTE: [contrato-pedido] [registro_duplicado]
```

## Rastro

Gerado dos eventos 714 a 739 da trilha; hash dos eventos deste caso: `efd2daf899ced71f` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-31.md`.
