<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Registro duplicado em `GET /api/pedidos?login=11122233344`

Caso `run-26` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/run-26`: o caso `run-26` na corrida `fase4_ineditos`; eventos 691 a 712 da trilha `trilha_ineditos.jsonl`, hash dos eventos `8211e6707f45b278` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Registro duplicado em `GET /api/pedidos?login=11122233344`

## 3. Data, organização e autor

Observado em 06/11/2026 14:25:37 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/pedidos?login=11122233344` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `run-26`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids run-26`

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

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 5 (tempo e estado); nível 3 (difícil). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`).
- Verbetes entregues pela busca e não citados: `pedido-reserva` (Reserva de mesa (pedido); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/pedido-reserva.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/pedido-reserva.md`); `valor_fora_do_dominio` (Valor fora do domínio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/valor_fora_do_dominio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/valor_fora_do_dominio.md`).
- Caso escrito: `run-26` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/run-26` em `trilha_ineditos.jsonl`, eventos 691 a 712, hash dos eventos `8211e6707f45b278`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids run-26`.
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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids run-26`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 691 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:25:37 | caso run-26 |
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
