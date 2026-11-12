<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Valor fora do domínio em `GET /api/produtos`, campo `resumo`

Caso `lex-18` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/lex-18@fixture`: o caso `lex-18` na corrida `fase4_tela_v4`; eventos 1387 a 1412 da trilha `trilha_tela.jsonl`, hash dos eventos `96654751dc17f0d0` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Valor fora do domínio em `GET /api/produtos`, campo `resumo`

## 3. Data, organização e autor

Observado em 06/11/2026 10:46:32 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `lex-18`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 1 (léxica: o corpo da resposta nem dá para ler); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gÃ¡s", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}]
```

4. Sintoma observado (texto do caso):

> O card da Agua Mineral mostra o resumo como 'Garrafa 500ml, com ou sem gÃ¡s'; o nome do produto, logo acima no mesmo card, aparece com o acento certo ('Água').

5. Observação adicional (texto do caso):

> So o campo resumo veio com os bytes trocados; nome, no mesmo item, chegou certo: nao e um problema de charset da resposta inteira.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids lex-18 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O card da Agua Mineral mostra o resumo como 'Garrafa 500ml, com ou sem gÃ¡s'; o nome do produto, logo acima no mesmo card, aparece com o acento certo ('Água'). |

Corpo recebido, como veio no caso:

```text
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gÃ¡s", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 1 (léxica: o corpo da resposta nem dá para ler); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 1 (léxica); nível 2 (médio). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Verbetes entregues pela busca e não citados: `estado_da_tela_divergente` (Estado da tela divergente da resposta; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estado_da_tela_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estado_da_tela_divergente.md`).
- Caso escrito: `lex-18` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/lex-18@fixture` em `trilha_tela.jsonl`, eventos 1387 a 1412, hash dos eventos `96654751dc17f0d0`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/lex-18@fixture.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids lex-18 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `valor_fora_do_dominio` (Valor fora do domínio). Campo: `resumo`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,42 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O resumo exibido na tela contém caracteres errados, indicando um problema de codificação.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu valor_fora_do_dominio no campo resumo porque os verbetes contrato-produto, entidade-produto, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,22. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida valor_fora_do_dominio. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,42); trate como hipótese e confira o campo resumo antes de agir.

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida valor_fora_do_dominio.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gÃ¡s", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}]

SINTOMA OBSERVADO: O card da Agua Mineral mostra o resumo como 'Garrafa 500ml, com ou sem gÃ¡s'; o nome do produto, logo acima no mesmo card, aparece com o acento certo ('Água').

OBSERVAÇÃO ADICIONAL: So o campo resumo veio com os bytes trocados; nome, no mesmo item, chegou certo — nao e um problema de charset da resposta inteira.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> valor_fora_do_dominio e não campo_ausente: a escolha tem probabilidade 0,42 contra 0,22; verbete(s) na evidência: contrato-produto, entidade-produto, estado_da_tela_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,42 | sim |
| `campo_ausente` (Campo ausente) | 0,22 |  |
| `campo_renomeado` (Campo renomeado) | 0,22 |  |
| `codificacao_incorreta` (Codificação de caracteres incorreta) | 0,13 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,09 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,07 |  |
| `tipo_divergente` (Tipo divergente) | 0,05 |  |
| `nulo_inesperado` (Nulo inesperado) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [entidade-produto]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `estado_da_tela_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto], [entidade-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "entidade-produto"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "valor_fora_do_dominio"} |
| O verbete citado fala da causa respondida | `entidade-produto` | não confere | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `resumo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids lex-18 --k 3`

## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1387 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:46:32 | caso lex-18 |
| 1388 | 2 | candidatos | programa | ao_vivo | 2026-11-06T10:46:32 | 3 de 39 verbetes entregues |
| 1390 | 3 | prompt | programa | ao_vivo | 2026-11-06T10:46:32 | diagnostico: 3744 caracteres; verbetes contrato-produto, entidade-produto, estado_da_tela_divergente |
| 1392 | 4 | inferencia | programa | ao_vivo | 2026-11-06T10:46:32 | diagnostico: 58,0 s |
| 1393 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T10:46:32 | causa_raiz: `valor_fora_do_dominio` |
| 1394 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T10:46:32 | campo: `resumo` |
| 1395 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T10:46:32 | impacto: `O resumo exibido na tela contém caracteres errados, indicando um problema de codificação.` |
| 1396 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T10:46:32 | fonte: `[contrato-produto], [entidade-produto]` |
| 1397 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T10:46:32 | fonte_citada: `contrato-produto` |
| 1398 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T10:46:32 | fonte_citada: `entidade-produto` |
| 1399 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | quatro_linhas_presentes: confere |
| 1400 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | rotulo_no_conjunto: confere |
| 1401 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | fonte_existe_na_biblioteca: confere |
| 1402 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | fonte_existe_na_biblioteca: confere |
| 1403 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | fonte_estava_no_contexto: confere |
| 1404 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | fonte_estava_no_contexto: confere |
| 1405 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | campo_existe_no_caso: confere |
| 1406 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1407 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | notas_nos_verbetes_citados: informativo |
| 1408 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | impacto: nao_verificavel |
| 1409 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | fonte_formato_valido: confere |
| 1410 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | fonte_contem_termo_da_causa: nao_confere |
| 1411 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:46:32 | fonte_contem_termo_da_causa: nao_confere |
| 1412 | 24 | decisao | programa | ao_vivo | 2026-11-06T10:46:32 | diagnostico: escolha valor_fora_do_dominio; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 1412, decisão `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido.
  - Evidência: evento 1388 (verbete_entregue: `contrato-produto`, `entidade-produto`, `estado_da_tela_divergente`); evento 1392 (resposta); evento 1397 (verbete_citado: `contrato-produto`); evento 1398 (verbete_citado: `entidade-produto`).
  - Usou: `contrato-produto`, `entidade-produto`, `estado_da_tela_divergente`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1387 a 1412 da trilha; hash dos eventos deste caso: `96654751dc17f0d0`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
