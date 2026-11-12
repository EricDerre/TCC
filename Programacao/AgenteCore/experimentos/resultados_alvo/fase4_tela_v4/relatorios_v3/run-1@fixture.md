<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Erro interno do servidor (500) em `GET /api/produtos`

Caso `run-1` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/run-1@fixture`: o caso `run-1` na corrida `fase4_tela_v4`; eventos 470 a 491 da trilha `trilha_tela.jsonl`, hash dos eventos `3b6c79022d914860` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Erro interno do servidor (500) em `GET /api/produtos`

## 3. Data, organização e autor

Observado em 06/11/2026 10:12:53 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `run-1`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 500 (a API falhou por erro interno).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"detail": "erro interno (fault injection)"}
```

4. Sintoma observado (texto do caso):

> A aba de produtos via API mostra a mensagem de erro ao carregar.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-1 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A aba de produtos via API mostra a mensagem de erro ao carregar. |

Corpo recebido, como veio no caso:

```text
{"detail": "erro interno (fault injection)"}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 5 (tempo e estado); nível 1 (fácil). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `erro_interno_do_servidor` (Erro interno do servidor (500); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/erro_interno_do_servidor.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/erro_interno_do_servidor.md`).
- Verbetes entregues pela busca e não citados: `mensagens-de-erro-do-codigo` (Índice de mensagens literais do código; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/mensagens-de-erro-do-codigo.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/mensagens-de-erro-do-codigo.md`); `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`).
- Caso escrito: `run-1` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/run-1@fixture` em `trilha_tela.jsonl`, eventos 470 a 491, hash dos eventos `3b6c79022d914860`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/run-1@fixture.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-1 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `erro_interno_do_servidor` (Erro interno do servidor (500)). Campo: nenhum apontado. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,98 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `A aba de produtos via API exibe a mensagem "Erro ao carregar produtos da CobaiaAPI: erro interno (fault injection)".`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu erro_interno_do_servidor porque os verbetes erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 500

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "erro interno (fault injection)"}

SINTOMA OBSERVADO: A aba de produtos via API mostra a mensagem de erro ao carregar.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> erro_interno_do_servidor e não corpo_nao_e_json: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `erro_interno_do_servidor` (Erro interno do servidor (500)) | 0,98 | sim |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[erro_interno_do_servidor]`; verbetes citados: `erro_interno_do_servidor` (Erro interno do servidor (500); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/erro_interno_do_servidor.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/erro_interno_do_servidor.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo` |
| A linha FONTE só tem identificadores, no formato pedido | `[erro_interno_do_servidor]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["erro_interno_do_servidor"]} |
| O verbete citado fala da causa respondida | `erro_interno_do_servidor` | confere | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-1 --k 3`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 470 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:12:53 | caso run-1 |
| 471 | 2 | candidatos | programa | ao_vivo | 2026-11-06T10:12:53 | 3 de 39 verbetes entregues |
| 473 | 3 | prompt | programa | ao_vivo | 2026-11-06T10:12:53 | diagnostico: 3503 caracteres; verbetes erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente |
| 475 | 4 | inferencia | programa | ao_vivo | 2026-11-06T10:12:53 | diagnostico: 60,3 s |
| 476 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T10:12:53 | causa_raiz: `erro_interno_do_servidor` |
| 477 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T10:12:53 | campo: `nenhum` |
| 478 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T10:12:53 | impacto: `A aba de produtos via API exibe a mensagem "Erro ao carregar produtos da CobaiaAPI: erro interno (fault injection)".` |
| 479 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T10:12:53 | fonte: `[erro_interno_do_servidor]` |
| 480 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T10:12:53 | fonte_citada: `erro_interno_do_servidor` |
| 481 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | quatro_linhas_presentes: confere |
| 482 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | rotulo_no_conjunto: confere |
| 483 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | fonte_existe_na_biblioteca: confere |
| 484 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | fonte_estava_no_contexto: confere |
| 485 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | campo_existe_no_caso: nao_se_aplica |
| 486 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 487 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | notas_nos_verbetes_citados: informativo |
| 488 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | impacto: nao_verificavel |
| 489 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | fonte_formato_valido: confere |
| 490 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:12:53 | fonte_contem_termo_da_causa: confere |
| 491 | 20 | decisao | programa | ao_vivo | 2026-11-06T10:12:53 | diagnostico: escolha erro_interno_do_servidor; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 491, decisão `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido.
  - Evidência: evento 471 (verbete_entregue: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `contagem_inconsistente`); evento 475 (resposta); evento 480 (verbete_citado: `erro_interno_do_servidor`).
  - Usou: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `contagem_inconsistente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 470 a 491 da trilha; hash dos eventos deste caso: `3b6c79022d914860`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
