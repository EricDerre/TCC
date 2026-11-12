<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Valor fora do domínio em `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 4, "data_pedido": "2026-12-19"})`, campo `pessoas`

Caso `tra-23` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/tra-23`: o caso `tra-23` na corrida `fase4_ineditos`; eventos 468 a 493 da trilha `trilha_ineditos.jsonl`, hash dos eventos `b62b751f29151d15` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Valor fora do domínio em `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 4, "data_pedido": "2026-12-19"})`, campo `pessoas`

## 3. Data, organização e autor

Observado em 06/11/2026 14:15:06 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 4, "data_pedido": "2026-12-19"})` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `tra-23`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 4 (tradução: o mapeamento entre as camadas está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 4, "data_pedido": "2026-12-19"})`, status 201 (a API criou o registro).
2. Contrato da interface: `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`.
3. Corpo da resposta:

```text
{"id_pedido": 12, "pessoas": 400, "data_pedido": "2026-12-19", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}
```

4. Sintoma observado (texto do caso):

> A reserva e criada (status 201), mas a resposta mostra 400 pessoas para uma reserva pedida para 4.

5. Observação adicional (texto do caso):

> Consultando o banco direto, tbpedido_reserva guarda a reserva 12 com 4 pessoas.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-23`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 4, "data_pedido": "2026-12-19"})` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A reserva e criada (status 201), mas a resposta mostra 400 pessoas para uma reserva pedida para 4. |

Corpo recebido, como veio no caso:

```text
{"id_pedido": 12, "pessoas": 400, "data_pedido": "2026-12-19", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 4 (tradução: o mapeamento entre as camadas está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 4 (tradução); nível 1 (fácil). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `pedido-reserva` (Reserva de mesa (pedido); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/pedido-reserva.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/pedido-reserva.md`); `valor_fora_do_dominio` (Valor fora do domínio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/valor_fora_do_dominio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/valor_fora_do_dominio.md`).
- Verbetes entregues pela busca e não citados: `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`).
- Caso escrito: `tra-23` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/tra-23` em `trilha_ineditos.jsonl`, eventos 468 a 493, hash dos eventos `b62b751f29151d15`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-23`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `valor_fora_do_dominio` (Valor fora do domínio). Campo: `pessoas`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,65 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê 400 pessoas reservadas em vez das 4 solicitadas.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu valor_fora_do_dominio no campo pessoas porque os verbetes contrato-pedido, pedido-reserva, valor_fora_do_dominio estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,35. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,65); trate como hipótese e confira o campo pessoas antes de agir.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 4, "data_pedido": "2026-12-19"})

STATUS HTTP: 201

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
{"id_pedido": 12, "pessoas": 400, "data_pedido": "2026-12-19", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}

SINTOMA OBSERVADO: A reserva e criada (status 201), mas a resposta mostra 400 pessoas para uma reserva pedida para 4.

OBSERVAÇÃO ADICIONAL: Consultando o banco direto, tbpedido_reserva guarda a reserva 12 com 4 pessoas.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> valor_fora_do_dominio e não tipo_divergente: a escolha tem probabilidade 0,65 contra 0,35; verbete(s) na evidência: contrato-pedido, pedido-reserva, valor_fora_do_dominio

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,65 | sim |
| `tipo_divergente` (Tipo divergente) | 0,35 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `registro_duplicado` (Registro duplicado) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[pedido-reserva] [valor_fora_do_dominio]`; verbetes citados: `pedido-reserva` (Reserva de mesa (pedido); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/pedido-reserva.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/pedido-reserva.md`); `valor_fora_do_dominio` (Valor fora do domínio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/valor_fora_do_dominio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/valor_fora_do_dominio.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `pedido-reserva` | confere |  |
| O verbete citado existe na biblioteca | `valor_fora_do_dominio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `pedido-reserva` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio` |
| O verbete citado estava no contexto entregue ao modelo | `valor_fora_do_dominio` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio` |
| A linha FONTE só tem identificadores, no formato pedido | `[pedido-reserva] [valor_fora_do_dominio]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["pedido-reserva", "valor_fora_do_dominio"]} |
| O verbete citado fala da causa respondida | `pedido-reserva` | não confere | {"termo": "valor_fora_do_dominio"} |
| O verbete citado fala da causa respondida | `valor_fora_do_dominio` | confere | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `pessoas` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-23`

## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 468 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:15:06 | caso tra-23 |
| 469 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:15:06 | 3 de 39 verbetes entregues |
| 471 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:15:06 | diagnostico: 3698 caracteres; verbetes contrato-pedido, pedido-reserva, valor_fora_do_dominio |
| 473 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:15:06 | diagnostico: 57,2 s |
| 474 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:15:06 | causa_raiz: `valor_fora_do_dominio` |
| 475 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:15:06 | campo: `pessoas` |
| 476 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:15:06 | impacto: `O usuário vê 400 pessoas reservadas em vez das 4 solicitadas.` |
| 477 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:15:06 | fonte: `[pedido-reserva] [valor_fora_do_dominio]` |
| 478 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:15:06 | fonte_citada: `pedido-reserva` |
| 479 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T14:15:06 | fonte_citada: `valor_fora_do_dominio` |
| 480 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | quatro_linhas_presentes: confere |
| 481 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | rotulo_no_conjunto: confere |
| 482 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | fonte_existe_na_biblioteca: confere |
| 483 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | fonte_existe_na_biblioteca: confere |
| 484 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | fonte_estava_no_contexto: confere |
| 485 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | fonte_estava_no_contexto: confere |
| 486 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | campo_existe_no_caso: confere |
| 487 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 488 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | notas_nos_verbetes_citados: informativo |
| 489 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | impacto: nao_verificavel |
| 490 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | fonte_formato_valido: confere |
| 491 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | fonte_contem_termo_da_causa: nao_confere |
| 492 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T14:15:06 | fonte_contem_termo_da_causa: confere |
| 493 | 24 | decisao | programa | ao_vivo | 2026-11-06T14:15:06 | diagnostico: escolha valor_fora_do_dominio; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 493, decisão `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido.
  - Evidência: evento 469 (verbete_entregue: `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio`); evento 473 (resposta); evento 478 (verbete_citado: `pedido-reserva`); evento 479 (verbete_citado: `valor_fora_do_dominio`).
  - Usou: `contrato-pedido`, `pedido-reserva`, `valor_fora_do_dominio`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 468 a 493 da trilha; hash dos eventos deste caso: `b62b751f29151d15`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
