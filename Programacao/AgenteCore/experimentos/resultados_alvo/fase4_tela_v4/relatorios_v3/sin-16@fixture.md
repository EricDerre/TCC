<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Campo ausente em `GET /api/produtos/1 (modo field_missing, campo destaque)`, campo `destaque`

Caso `sin-16` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/sin-16@fixture`: o caso `sin-16` na corrida `fase4_tela_v4`; eventos 1455 a 1476 da trilha `trilha_tela.jsonl`, hash dos eventos `cd7bdd5dd4763a57` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Campo ausente em `GET /api/produtos/1 (modo field_missing, campo destaque)`, campo `destaque`

## 3. Data, organização e autor

Observado em 06/11/2026 10:48:32 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/1 (modo field_missing, campo destaque)` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `sin-16`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 2 (sintática: a forma da resposta não é a esperada); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/1 (modo field_missing, campo destaque)`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg"}
```

4. Sintoma observado (texto do caso):

> A resposta de GET /api/produtos/1 deixa de trazer o campo destaque; o modal 'Saiba Mais...' (que so le nome e resumo) continua abrindo normal, mas o campo e obrigatorio no contrato (ProdutoOut.destaque: bool, sem valor default).

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-16 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/1 (modo field_missing, campo destaque)` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A resposta de GET /api/produtos/1 deixa de trazer o campo destaque; o modal 'Saiba Mais...' (que so le nome e resumo) continua abrindo normal, mas o campo e obrigatorio no contrato (ProdutoOut.destaque: bool, sem valor default). |

Corpo recebido, como veio no caso:

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg"}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 2 (sintática: a forma da resposta não é a esperada); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 2 (sintática); nível 1 (fácil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `sin-16` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/sin-16@fixture` em `trilha_tela.jsonl`, eventos 1455 a 1476, hash dos eventos `cd7bdd5dd4763a57`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/sin-16@fixture.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-16 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `campo_ausente` (Campo ausente). Campo: `destaque`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O campo destaque, obrigatório no contrato, não é retornado na resposta, causando inconsistência na exibição do produto.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu campo_ausente no campo destaque porque os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_renomeado, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/1 (modo field_missing, campo destaque)

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg"}

SINTOMA OBSERVADO: A resposta de GET /api/produtos/1 deixa de trazer o campo destaque; o modal 'Saiba Mais...' (que so le nome e resumo) continua abrindo normal, mas o campo e obrigatorio no contrato (ProdutoOut.destaque: bool, sem valor default).
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> campo_ausente e não campo_renomeado: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `campo_ausente` (Campo ausente) | 1,00 | sim |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente]`; verbetes citados: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto`, `campo_ausente` |
| A linha FONTE só tem identificadores, no formato pedido | `[campo_ausente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_ausente"]} |
| O verbete citado fala da causa respondida | `campo_ausente` | confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `destaque` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-16 --k 3`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1455 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:48:32 | caso sin-16 |
| 1456 | 2 | candidatos | programa | ao_vivo | 2026-11-06T10:48:32 | 3 de 39 verbetes entregues |
| 1458 | 3 | prompt | programa | ao_vivo | 2026-11-06T10:48:32 | diagnostico: 3595 caracteres; verbetes entidade-produto, contrato-produto, campo_ausente |
| 1460 | 4 | inferencia | programa | ao_vivo | 2026-11-06T10:48:32 | diagnostico: 39,0 s |
| 1461 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T10:48:32 | causa_raiz: `campo_ausente` |
| 1462 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T10:48:32 | campo: `destaque` |
| 1463 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T10:48:32 | impacto: `O campo destaque, obrigatório no contrato, não é retornado na resposta, causando inconsistência na exibição do produto.` |
| 1464 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T10:48:32 | fonte: `[campo_ausente]` |
| 1465 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T10:48:32 | fonte_citada: `campo_ausente` |
| 1466 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:48:32 | quatro_linhas_presentes: confere |
| 1467 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:48:32 | rotulo_no_conjunto: confere |
| 1468 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:48:32 | fonte_existe_na_biblioteca: confere |
| 1469 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:48:32 | fonte_estava_no_contexto: confere |
| 1470 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T10:48:32 | campo_existe_no_caso: confere |
| 1471 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T10:48:32 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1472 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T10:48:32 | notas_nos_verbetes_citados: informativo |
| 1473 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:48:32 | impacto: nao_verificavel |
| 1474 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:48:32 | fonte_formato_valido: confere |
| 1475 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:48:32 | fonte_contem_termo_da_causa: confere |
| 1476 | 20 | decisao | programa | ao_vivo | 2026-11-06T10:48:32 | diagnostico: escolha campo_ausente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 1476, decisão `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido.
  - Evidência: evento 1456 (verbete_entregue: `entidade-produto`, `contrato-produto`, `campo_ausente`); evento 1460 (resposta); evento 1465 (verbete_citado: `campo_ausente`).
  - Usou: `entidade-produto`, `contrato-produto`, `campo_ausente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1455 a 1476 da trilha; hash dos eventos deste caso: `cd7bdd5dd4763a57`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
