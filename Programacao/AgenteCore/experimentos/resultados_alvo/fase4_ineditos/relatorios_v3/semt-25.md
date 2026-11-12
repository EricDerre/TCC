<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Formato de data divergente em `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 6, "data_pedido": "2026-12-20"})`, campo `data_pedido`

Caso `semt-25` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/semt-25`: o caso `semt-25` na corrida `fase4_ineditos`; eventos 372 a 393 da trilha `trilha_ineditos.jsonl`, hash dos eventos `741ca78bdb34b7ae` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Formato de data divergente em `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 6, "data_pedido": "2026-12-20"})`, campo `data_pedido`

## 3. Data, organização e autor

Observado em 06/11/2026 14:10:00 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 6, "data_pedido": "2026-12-20"})` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `semt-25`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 6, "data_pedido": "2026-12-20"})`, status 201 (a API criou o registro).
2. Contrato da interface: `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`.
3. Corpo da resposta:

```text
{"id_pedido": 11, "pessoas": 6, "data_pedido": "20/12/2026", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}
```

4. Sintoma observado (texto do caso):

> A reserva e criada (status 201), mas a resposta devolve a data como '20/12/2026' para uma reserva pedida com '2026-12-20'; quem le o campo como data ISO (AAAA-MM-DD) nao consegue interpretar o valor.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids semt-25`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 6, "data_pedido": "2026-12-20"})` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A reserva e criada (status 201), mas a resposta devolve a data como '20/12/2026' para uma reserva pedida com '2026-12-20'; quem le o campo como data ISO (AAAA-MM-DD) nao consegue interpretar o valor. |

Corpo recebido, como veio no caso:

```text
{"id_pedido": 11, "pessoas": 6, "data_pedido": "20/12/2026", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 3 (semântica); nível 2 (médio). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `formato_de_data_divergente` (Formato de data divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/formato_de_data_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/formato_de_data_divergente.md`).
- Verbetes entregues pela busca e não citados: `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`); `pedido-reserva` (Reserva de mesa (pedido); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/pedido-reserva.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/pedido-reserva.md`).
- Caso escrito: `semt-25` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/semt-25` em `trilha_ineditos.jsonl`, eventos 372 a 393, hash dos eventos `741ca78bdb34b7ae`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids semt-25`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `formato_de_data_divergente` (Formato de data divergente). Campo: `data_pedido`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,98 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário recebe uma data no formato '20/12/2026' em vez do esperado '2026-12-20', dificultando a interpretação da data ISO (AAAA-MM-DD).`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu formato_de_data_divergente no campo data_pedido porque os verbetes contrato-pedido, formato_de_data_divergente, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,01. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 6, "data_pedido": "2026-12-20"})

STATUS HTTP: 201

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
{"id_pedido": 11, "pessoas": 6, "data_pedido": "20/12/2026", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}

SINTOMA OBSERVADO: A reserva e criada (status 201), mas a resposta devolve a data como '20/12/2026' para uma reserva pedida com '2026-12-20'; quem le o campo como data ISO (AAAA-MM-DD) nao consegue interpretar o valor.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> formato_de_data_divergente e não tipo_divergente: a escolha tem probabilidade 0,98 contra 0,01; verbete(s) na evidência: contrato-pedido, formato_de_data_divergente, pedido-reserva

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `formato_de_data_divergente` (Formato de data divergente) | 0,98 | sim |
| `tipo_divergente` (Tipo divergente) | 0,01 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[formato_de_data_divergente]`; verbetes citados: `formato_de_data_divergente` (Formato de data divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/formato_de_data_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/formato_de_data_divergente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `formato_de_data_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `formato_de_data_divergente` | confere | contexto: `contrato-pedido`, `formato_de_data_divergente`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | confere | verbetes: `contrato-pedido`, `formato_de_data_divergente` |
| A linha FONTE só tem identificadores, no formato pedido | `[formato_de_data_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["formato_de_data_divergente"]} |
| O verbete citado fala da causa respondida | `formato_de_data_divergente` | confere | {"termo": "formato_de_data_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `data_pedido` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids semt-25`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 372 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:10:00 | caso semt-25 |
| 373 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:10:00 | 3 de 39 verbetes entregues |
| 375 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:10:00 | diagnostico: 3564 caracteres; verbetes contrato-pedido, formato_de_data_divergente, pedido-reserva |
| 377 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:10:00 | diagnostico: 79,1 s |
| 378 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:10:00 | causa_raiz: `formato_de_data_divergente` |
| 379 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:10:00 | campo: `data_pedido` |
| 380 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:10:00 | impacto: `O usuário recebe uma data no formato '20/12/2026' em vez do esperado '2026-12-20', dificultando a interpretação da data ISO (AAAA-MM-DD).` |
| 381 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:10:00 | fonte: `[formato_de_data_divergente]` |
| 382 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:10:00 | fonte_citada: `formato_de_data_divergente` |
| 383 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:10:00 | quatro_linhas_presentes: confere |
| 384 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:10:00 | rotulo_no_conjunto: confere |
| 385 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:10:00 | fonte_existe_na_biblioteca: confere |
| 386 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:10:00 | fonte_estava_no_contexto: confere |
| 387 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:10:00 | campo_existe_no_caso: confere |
| 388 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:10:00 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 389 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:10:00 | notas_nos_verbetes_citados: informativo |
| 390 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:10:00 | impacto: nao_verificavel |
| 391 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:10:00 | fonte_formato_valido: confere |
| 392 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:10:00 | fonte_contem_termo_da_causa: confere |
| 393 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:10:00 | diagnostico: escolha formato_de_data_divergente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 393, decisão `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido.
  - Evidência: evento 373 (verbete_entregue: `contrato-pedido`, `formato_de_data_divergente`, `pedido-reserva`); evento 377 (resposta); evento 382 (verbete_citado: `formato_de_data_divergente`).
  - Usou: `contrato-pedido`, `formato_de_data_divergente`, `pedido-reserva`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 372 a 393 da trilha; hash dos eventos deste caso: `741ca78bdb34b7ae`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
