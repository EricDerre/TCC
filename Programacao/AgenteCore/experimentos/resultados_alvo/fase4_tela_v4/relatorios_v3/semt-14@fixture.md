<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Nulo inesperado em `GET /api/produtos`, campo `tipo`

Caso `semt-14` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/semt-14@fixture`: o caso `semt-14` na corrida `fase4_tela_v4`; eventos 1112 a 1137 da trilha `trilha_tela.jsonl`, hash dos eventos `3f5602e433b7efb2` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Nulo inesperado em `GET /api/produtos`, campo `tipo`

## 3. Data, organização e autor

Observado em 06/11/2026 10:36:40 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `semt-14`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 8, "nome": "Agua Mineral", "resumo": "500ml", "tipo": null, "preco": 6.0, "imagem": "agua.png", "destaque": false}]
```

4. Sintoma observado (texto do caso):

> O filtro por categoria deixa de listar alguns produtos que existem no cadastro.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-14 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O filtro por categoria deixa de listar alguns produtos que existem no cadastro. |

Corpo recebido, como veio no caso:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 8, "nome": "Agua Mineral", "resumo": "500ml", "tipo": null, "preco": 6.0, "imagem": "agua.png", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 3 (semântica); nível 3 (difícil). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `semt-14` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/semt-14@fixture` em `trilha_tela.jsonl`, eventos 1112 a 1137, hash dos eventos `3f5602e433b7efb2`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/semt-14@fixture.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-14 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `nulo_inesperado` (Nulo inesperado). Campo: `tipo`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,74 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O filtro por categoria não exibe corretamente os produtos, pois alguns tipos estão ausentes na resposta.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu nulo_inesperado no campo tipo porque os verbetes entidade-produto, contrato-produto, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,25. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,74); trate como hipótese e confira o campo tipo antes de agir.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 8, "nome": "Agua Mineral", "resumo": "500ml", "tipo": null, "preco": 6.0, "imagem": "agua.png", "destaque": false}]

SINTOMA OBSERVADO: O filtro por categoria deixa de listar alguns produtos que existem no cadastro.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 0,74 contra 0,25; verbete(s) na evidência: entidade-produto, contrato-produto, nulo_inesperado

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `nulo_inesperado` (Nulo inesperado) | 0,74 | sim |
| `tipo_divergente` (Tipo divergente) | 0,25 |  |
| `campo_ausente` (Campo ausente) | 0,01 |  |
| `campo_renomeado` (Campo renomeado) | 0,01 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [nulo_inesperado]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto], [nulo_inesperado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "nulo_inesperado"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "nulo_inesperado"} |
| O verbete citado fala da causa respondida | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-14 --k 3`

## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1112 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:36:40 | caso semt-14 |
| 1113 | 2 | candidatos | programa | ao_vivo | 2026-11-06T10:36:40 | 3 de 39 verbetes entregues |
| 1115 | 3 | prompt | programa | ao_vivo | 2026-11-06T10:36:40 | diagnostico: 3495 caracteres; verbetes entidade-produto, contrato-produto, nulo_inesperado |
| 1117 | 4 | inferencia | programa | ao_vivo | 2026-11-06T10:36:40 | diagnostico: 54,2 s |
| 1118 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T10:36:40 | causa_raiz: `nulo_inesperado` |
| 1119 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T10:36:40 | campo: `tipo` |
| 1120 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T10:36:40 | impacto: `O filtro por categoria não exibe corretamente os produtos, pois alguns tipos estão ausentes na resposta.` |
| 1121 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T10:36:40 | fonte: `[contrato-produto], [nulo_inesperado]` |
| 1122 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T10:36:40 | fonte_citada: `contrato-produto` |
| 1123 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T10:36:40 | fonte_citada: `nulo_inesperado` |
| 1124 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | quatro_linhas_presentes: confere |
| 1125 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | rotulo_no_conjunto: confere |
| 1126 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | fonte_existe_na_biblioteca: confere |
| 1127 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | fonte_existe_na_biblioteca: confere |
| 1128 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | fonte_estava_no_contexto: confere |
| 1129 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | fonte_estava_no_contexto: confere |
| 1130 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | campo_existe_no_caso: confere |
| 1131 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1132 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | notas_nos_verbetes_citados: informativo |
| 1133 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | impacto: nao_verificavel |
| 1134 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | fonte_formato_valido: confere |
| 1135 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | fonte_contem_termo_da_causa: nao_confere |
| 1136 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:36:40 | fonte_contem_termo_da_causa: confere |
| 1137 | 24 | decisao | programa | ao_vivo | 2026-11-06T10:36:40 | diagnostico: escolha nulo_inesperado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 1137, decisão `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido.
  - Evidência: evento 1113 (verbete_entregue: `entidade-produto`, `contrato-produto`, `nulo_inesperado`); evento 1117 (resposta); evento 1122 (verbete_citado: `contrato-produto`); evento 1123 (verbete_citado: `nulo_inesperado`).
  - Usou: `entidade-produto`, `contrato-produto`, `nulo_inesperado`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1112 a 1137 da trilha; hash dos eventos deste caso: `3f5602e433b7efb2`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
