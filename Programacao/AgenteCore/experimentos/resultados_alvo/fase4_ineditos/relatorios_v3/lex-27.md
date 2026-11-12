<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Codificação de caracteres incorreta em `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 3, "data_pedido": "2026-12-05"})`, campo `status`

Caso `lex-27` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/lex-27`: o caso `lex-27` na corrida `fase4_ineditos`; eventos 130 a 151 da trilha `trilha_ineditos.jsonl`, hash dos eventos `3bfdbee025a159ff` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Codificação de caracteres incorreta em `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 3, "data_pedido": "2026-12-05"})`, campo `status`

## 3. Data, organização e autor

Observado em 06/11/2026 13:58:08 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 3, "data_pedido": "2026-12-05"})` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `lex-27`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 1 (léxica: o corpo da resposta nem dá para ler); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 3, "data_pedido": "2026-12-05"})`, status 201 (a API criou o registro).
2. Contrato da interface: `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`.
3. Corpo da resposta:

```text
{"id_pedido": 10, "pessoas": 3, "data_pedido": "2026-12-05", "status": "Em AnÃ¡lise", "nome": "Cliente Teste", "cpf": "11122233344"}
```

4. Sintoma observado (texto do caso):

> A reserva e criada (status 201), mas o campo status da resposta traz 'Em AnÃ¡lise', com simbolos estranhos no lugar do acento.

5. Observação adicional (texto do caso):

> Consultando o banco direto, tbpedido_reserva guarda a reserva 10 com status 'Em Análise'.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids lex-27`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 3, "data_pedido": "2026-12-05"})` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A reserva e criada (status 201), mas o campo status da resposta traz 'Em AnÃ¡lise', com simbolos estranhos no lugar do acento. |

Corpo recebido, como veio no caso:

```text
{"id_pedido": 10, "pessoas": 3, "data_pedido": "2026-12-05", "status": "Em AnÃ¡lise", "nome": "Cliente Teste", "cpf": "11122233344"}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 1 (léxica: o corpo da resposta nem dá para ler); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 1 (léxica); nível 3 (difícil). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`).
- Verbetes entregues pela busca e não citados: `pedido-reserva` (Reserva de mesa (pedido); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/pedido-reserva.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/pedido-reserva.md`); `formato_de_data_divergente` (Formato de data divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/formato_de_data_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/formato_de_data_divergente.md`).
- Caso escrito: `lex-27` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/lex-27` em `trilha_ineditos.jsonl`, eventos 130 a 151, hash dos eventos `3bfdbee025a159ff`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids lex-27`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `codificacao_incorreta` (Codificação de caracteres incorreta). Campo: `status`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,74 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê um status com caracteres estranhos no lugar do acento, indicando um erro na codificação.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu codificacao_incorreta no campo status porque os verbetes contrato-pedido, pedido-reserva, formato_de_data_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,26. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,74); trate como hipótese e confira o campo status antes de agir.

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 3, "data_pedido": "2026-12-05"})

STATUS HTTP: 201

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
{"id_pedido": 10, "pessoas": 3, "data_pedido": "2026-12-05", "status": "Em AnÃ¡lise", "nome": "Cliente Teste", "cpf": "11122233344"}

SINTOMA OBSERVADO: A reserva e criada (status 201), mas o campo status da resposta traz 'Em AnÃ¡lise', com simbolos estranhos no lugar do acento.

OBSERVAÇÃO ADICIONAL: Consultando o banco direto, tbpedido_reserva guarda a reserva 10 com status 'Em Análise'.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> codificacao_incorreta e não campo_ausente: a escolha tem probabilidade 0,74 contra 0,26; verbete(s) na evidência: contrato-pedido, pedido-reserva, formato_de_data_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `codificacao_incorreta` (Codificação de caracteres incorreta) | 0,74 | sim |
| `campo_ausente` (Campo ausente) | 0,26 |  |
| `campo_renomeado` (Campo renomeado) | 0,26 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido` (Contrato de /api/pedidos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-pedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-pedido.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `formato_de_data_divergente` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-pedido]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-pedido"]} |
| O verbete citado fala da causa respondida | `contrato-pedido` | não confere | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `status` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids lex-27`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 130 | 1 | entrada | programa | ao_vivo | 2026-11-06T13:58:08 | caso lex-27 |
| 131 | 2 | candidatos | programa | ao_vivo | 2026-11-06T13:58:08 | 3 de 39 verbetes entregues |
| 133 | 3 | prompt | programa | ao_vivo | 2026-11-06T13:58:08 | diagnostico: 3605 caracteres; verbetes contrato-pedido, pedido-reserva, formato_de_data_divergente |
| 135 | 4 | inferencia | programa | ao_vivo | 2026-11-06T13:58:08 | diagnostico: 66,5 s |
| 136 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T13:58:08 | causa_raiz: `codificacao_incorreta` |
| 137 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T13:58:08 | campo: `status` |
| 138 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T13:58:08 | impacto: `O usuário vê um status com caracteres estranhos no lugar do acento, indicando um erro na codificação.` |
| 139 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T13:58:08 | fonte: `[contrato-pedido]` |
| 140 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T13:58:08 | fonte_citada: `contrato-pedido` |
| 141 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T13:58:08 | quatro_linhas_presentes: confere |
| 142 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T13:58:08 | rotulo_no_conjunto: confere |
| 143 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T13:58:08 | fonte_existe_na_biblioteca: confere |
| 144 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T13:58:08 | fonte_estava_no_contexto: confere |
| 145 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T13:58:08 | campo_existe_no_caso: confere |
| 146 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T13:58:08 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 147 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T13:58:08 | notas_nos_verbetes_citados: informativo |
| 148 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T13:58:08 | impacto: nao_verificavel |
| 149 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T13:58:08 | fonte_formato_valido: confere |
| 150 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T13:58:08 | fonte_contem_termo_da_causa: nao_confere |
| 151 | 20 | decisao | programa | ao_vivo | 2026-11-06T13:58:08 | diagnostico: escolha codificacao_incorreta; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 151, decisão `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido.
  - Evidência: evento 131 (verbete_entregue: `contrato-pedido`, `pedido-reserva`, `formato_de_data_divergente`); evento 135 (resposta); evento 140 (verbete_citado: `contrato-pedido`).
  - Usou: `contrato-pedido`, `pedido-reserva`, `formato_de_data_divergente`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 130 a 151 da trilha; hash dos eventos deste caso: `3bfdbee025a159ff`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
