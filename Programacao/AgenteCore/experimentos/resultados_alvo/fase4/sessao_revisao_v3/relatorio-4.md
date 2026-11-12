<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 4 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Registro duplicado em `GET /api/pedidos?login=11122233344`

Caso `relatorio-4` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-4`: o caso `relatorio-4` na corrida `fase4_ineditos`; eventos 691 a 712 da trilha `trilha_ineditos.jsonl`, hash dos eventos `8211e6707f45b278` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Registro duplicado em `GET /api/pedidos?login=11122233344`

## 3. Data, organização e autor

Observado em 06/11/2026 14:25:37 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/pedidos?login=11122233344` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-4`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/pedidos?login=11122233344`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`.
3. Corpo da resposta:

```text
[{"id_pedido": 8, "pessoas": 2, "data_pedido": "2026-11-20", "status": "Cancelado", "nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 9, "pessoas": 4, "data_pedido": "2026-12-05", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

4. Sintoma observado (texto do caso):

> Logo depois de POST /api/pedidos/9/cancelar responder 200 com status 'Cancelado', a consulta GET /api/pedidos?login=11122233344 ainda lista a reserva 9 como 'Em Analise'. A reserva 8, cancelada ontem, ja aparece como 'Cancelado'.

5. Observação adicional (texto do caso):

> Uma consulta direta ao banco (tbpedido_reserva) ja mostra a reserva 9 como 'Cancelado'. A mesma consulta GET /api/pedidos repetida cerca de 5 minutos depois traz o status novo.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/pedidos?login=11122233344` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Logo depois de POST /api/pedidos/9/cancelar responder 200 com status 'Cancelado', a consulta GET /api/pedidos?login=11122233344 ainda lista a reserva 9 como 'Em Analise'. A reserva 8, cancelada ontem, ja aparece como 'Cancelado'. |

Corpo recebido, como veio no caso:

```text
[{"id_pedido": 8, "pessoas": 2, "data_pedido": "2026-11-20", "status": "Cancelado", "nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 9, "pessoas": 4, "data_pedido": "2026-12-05", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`).
- Verbetes entregues pela busca e não citados: `pedido-reserva` (Reserva de mesa (pedido); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/pedido-reserva.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/pedido-reserva.md`); `valor_fora_do_dominio` (Valor fora do domínio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/valor_fora_do_dominio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/valor_fora_do_dominio.md`).
- Caso escrito: `relatorio-4` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-4` em `trilha_ineditos.jsonl`, eventos 691 a 712, hash dos eventos `8211e6707f45b278`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `registro_duplicado` (Registro duplicado). Campo: nenhum apontado. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,76 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê reservas com status inconsistente, onde algumas reservas não refletem o status atualizado.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu registro_duplicado porque os verbetes contrato-pedido, pedido-reserva, valor_fora_do_dominio estavam entre os entregues ao modelo. A segunda causa, dado_desatualizado, ficou com probabilidade 0,22 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,76); trate como hipótese e confira o caso antes de agir.

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 8, "pessoas": 2, "data_pedido": "2026-11-20", "status": "Cancelado", "nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 9, "pessoas": 4, "data_pedido": "2026-12-05", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: Logo depois de POST /api/pedidos/9/cancelar responder 200 com status 'Cancelado', a consulta GET /api/pedidos?login=11122233344 ainda lista a reserva 9 como 'Em Analise'. A reserva 8, cancelada ontem, ja aparece como 'Cancelado'.

OBSERVAÇÃO ADICIONAL: Uma consulta direta ao banco (tbpedido_reserva) ja mostra a reserva 9 como 'Cancelado'. A mesma consulta GET /api/pedidos repetida cerca de 5 minutos depois traz o status novo.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> registro_duplicado e não dado_desatualizado: a escolha tem probabilidade 0,76 contra 0,22; verbete(s) na evidência: contrato-pedido, pedido-reserva, valor_fora_do_dominio

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `registro_duplicado` (Registro duplicado) | 0,76 | sim |
| `dado_desatualizado` (Dado desatualizado (cache)) | 0,22 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,01 |  |
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `nulo_inesperado` (Nulo inesperado) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `contagem_inconsistente` (Contagem inconsistente) | 0,00 |  |
| `recurso_inexistente` (Recurso inexistente (404 e vizinhos)) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-pedido]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-pedido"]} |
| O verbete citado fala da causa respondida | `contrato-pedido` | não confere | {"termo": "registro_duplicado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 691 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:25:37 | caso relatorio-4 |
| 692 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:25:37 | 3 de 39 verbetes entregues |
| 694 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:25:37 | diagnostico: 4000 caracteres; verbetes contrato-pedido, pedido-reserva, valor_fora_do_dominio |
| 696 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:25:37 | diagnostico: 49,3 s |
| 697 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:25:37 | causa_raiz: `registro_duplicado` |
| 698 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:25:37 | campo: `nenhum` |
| 699 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:25:37 | impacto: `O usuário vê reservas com status inconsistente, onde algumas reservas não refletem o status atualizado.` |
| 700 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:25:37 | fonte: `[contrato-pedido]` |
| 701 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:25:37 | fonte_citada: `contrato-pedido` |
| 702 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:25:37 | quatro_linhas_presentes: confere |
| 703 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:25:37 | rotulo_no_conjunto: confere |
| 704 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:25:37 | fonte_existe_na_biblioteca: confere |
| 705 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:25:37 | fonte_estava_no_contexto: confere |
| 706 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:25:37 | campo_existe_no_caso: nao_se_aplica |
| 707 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:25:37 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 708 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:25:37 | notas_nos_verbetes_citados: informativo |
| 709 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:25:37 | impacto: nao_verificavel |
| 710 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:25:37 | fonte_formato_valido: confere |
| 711 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:25:37 | fonte_contem_termo_da_causa: nao_confere |
| 712 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:25:37 | diagnostico: escolha registro_duplicado; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 712, decisão `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido.
  - Evidência: evento 692 (verbete_entregue: `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio`); evento 696 (resposta); evento 701 (verbete_citado: `contrato-pedido`).
  - Usou: `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 691 a 712 da trilha; hash dos eventos deste caso: `8211e6707f45b278`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-4`

Caso `relatorio-4` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-4`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (981 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (981 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4000 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-pedido` (83,59), `pedido-reserva` (81,08) e `valor_fora_do_dominio` (57,97) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-pedido`, `pedido-reserva` e `valor_fora_do_dominio`; o da entidade, em `contrato-pedido`, `pedido-reserva` e `valor_fora_do_dominio` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `fluxo-reserva-e-cancelamento` (47,92), `dado_desatualizado` (45,98), `chave_de_juncao_errada` (39,19), `usuario-e-login` (34,88) e `estado_da_tela_divergente` (34,61) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/pedidos`, entidade `Pedido`, status 200 e 95 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `valor_fora_do_dominio`, e o primeiro de fora, `fluxo-reserva-e-cancelamento`, só o texto do caso já punha o primeiro à frente (54,97 contra 46,92), e os reforços em código levaram a diferença a 10,05 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-pedido` | posição 1, pontuação 83,59: 80,59 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pedido-reserva` | posição 2, pontuação 81,08: 78,08 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `valor_fora_do_dominio` | posição 3, pontuação 57,97: 54,97 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `fluxo-reserva-e-cancelamento` | posição 4, pontuação 47,92: 46,92 pelas palavras do caso, mais 1,0 por entidade |  |
| `dado_desatualizado` | posição 5, pontuação 45,98: 42,98 pelas palavras do caso, mais 2,0 por rota e 1,0 por status |  |
| `chave_de_juncao_errada` | posição 6, pontuação 39,19: 36,19 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `usuario-e-login` | posição 7, pontuação 34,88: 34,88 pelas palavras do caso, sem reforço |  |
| `estado_da_tela_divergente` | posição 8, pontuação 34,61: 34,61 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `registro_duplicado` (Registro duplicado); segunda: `dado_desatualizado`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `registro_duplicado` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `dado_desatualizado` (Dado desatualizado (cache)), ficou com probabilidade 0,216 contra 0,757 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 10 alternativas lidas na resposta somam probabilidade 0,017; as maiores: `estado_da_tela_divergente` (0,010), `tempo_de_resposta_excedido` (0,002) e `resposta_truncada` (0,001) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,757, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/pedidos?login=11122233344`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-pedido` (declarado).
- Verbete citado `contrato-pedido`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), não traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Leitura do verbete `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 5 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `registro_duplicado` | 0,757 | nenhum | sim |
| `dado_desatualizado` | 0,216 | nenhum |  |
| `estado_da_tela_divergente` | 0,010 | nenhum |  |
| `tempo_de_resposta_excedido` | 0,002 | nenhum |  |
| `resposta_truncada` | 0,001 | nenhum |  |
| `nulo_inesperado` | 0,001 | `pedido-reserva` e `valor_fora_do_dominio` |  |
| `valor_fora_do_dominio` | 0,001 | `contrato-pedido`, `pedido-reserva` e `valor_fora_do_dominio` |  |
| `campo_ausente` | 0,001 | `contrato-pedido` |  |
| `campo_renomeado` | 0,001 | nenhum |  |
| `contagem_inconsistente` | 0,000 | nenhum |  |
| `recurso_inexistente` | 0,000 | `contrato-pedido` |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê reservas com status inconsistente, onde algumas reservas não refletem o status atualizado.
> FONTE: [contrato-pedido]

Resposta inteira:

```text
CAUSA_RAIZ: registro_duplicado
CAMPO: nenhum
IMPACTO: O usuário vê reservas com status inconsistente, onde algumas reservas não refletem o status atualizado.
FONTE: [contrato-pedido]
```

## Rastro

Gerado dos eventos 691 a 712 da trilha; hash dos eventos deste caso: `8211e6707f45b278` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-4.md`.
