<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 12 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Chave de junção errada em `GET /api/produtos`, campo `tipo`

Caso `relatorio-12` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-12`: o caso `relatorio-12` na corrida `fase4_ineditos`; eventos 495 a 516 da trilha `trilha_ineditos.jsonl`, hash dos eventos `f27bc1e9d1758c80` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Chave de junção errada em `GET /api/produtos`, campo `tipo`

## 3. Data, organização e autor

Observado em 06/11/2026 14:16:08 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-12`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}, {"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Acompanhamentos", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false}]
```

4. Sintoma observado (texto do caso):

> Na grade, o Cupim aparece com a categoria 'Bebidas' e o Refrigerante com 'Acompanhamentos'; a Agua Mineral e o Balde de Cerveja aparecem com 'Bebidas'. Os nomes, os precos e as fotos estao certos.

5. Observação adicional (texto do caso):

> O corpo mostra so os itens de id 7 a 10; a lista completa tem 14.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Na grade, o Cupim aparece com a categoria 'Bebidas' e o Refrigerante com 'Acompanhamentos'; a Agua Mineral e o Balde de Cerveja aparecem com 'Bebidas'. Os nomes, os precos e as fotos estao certos. |

Corpo recebido, como veio no caso:

```text
[{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}, {"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Acompanhamentos", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `chave_de_juncao_errada` (Chave de junção errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/chave_de_juncao_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/chave_de_juncao_errada.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `relatorio-12` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-12` em `trilha_ineditos.jsonl`, eventos 495 a 516, hash dos eventos `f27bc1e9d1758c80`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `chave_de_juncao_errada` (Chave de junção errada). Campo: `tipo`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,92 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `Os produtos são exibidos com categorias incorretas, misturando itens de diferentes tipos.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu chave_de_juncao_errada no campo tipo porque os verbetes entidade-produto, contrato-produto, chave_de_juncao_errada estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,04. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}, {"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Acompanhamentos", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false}]

SINTOMA OBSERVADO: Na grade, o Cupim aparece com a categoria 'Bebidas' e o Refrigerante com 'Acompanhamentos'; a Agua Mineral e o Balde de Cerveja aparecem com 'Bebidas'. Os nomes, os precos e as fotos estao certos.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os itens de id 7 a 10; a lista completa tem 14.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> chave_de_juncao_errada e não tipo_divergente: a escolha tem probabilidade 0,92 contra 0,04; verbete(s) na evidência: entidade-produto, contrato-produto, chave_de_juncao_errada

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `chave_de_juncao_errada` (Chave de junção errada) | 0,92 | sim |
| `tipo_divergente` (Tipo divergente) | 0,04 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,02 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[chave_de_juncao_errada]`; verbetes citados: `chave_de_juncao_errada` (Chave de junção errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/chave_de_juncao_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/chave_de_juncao_errada.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `chave_de_juncao_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `chave_de_juncao_errada` | confere | contexto: `entidade-produto`, `contrato-produto`, `chave_de_juncao_errada` |
| Algum verbete do contexto trata da causa respondida | `chave_de_juncao_errada` | confere | verbetes: `entidade-produto`, `chave_de_juncao_errada` |
| A linha FONTE só tem identificadores, no formato pedido | `[chave_de_juncao_errada]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["chave_de_juncao_errada"]} |
| O verbete citado fala da causa respondida | `chave_de_juncao_errada` | confere | {"termo": "chave_de_juncao_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 495 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:16:08 | caso relatorio-12 |
| 496 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:16:08 | 3 de 39 verbetes entregues |
| 498 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:16:08 | diagnostico: 4674 caracteres; verbetes entidade-produto, contrato-produto, chave_de_juncao_errada |
| 500 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:16:08 | diagnostico: 73,7 s |
| 501 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:16:08 | causa_raiz: `chave_de_juncao_errada` |
| 502 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:16:08 | campo: `tipo` |
| 503 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:16:08 | impacto: `Os produtos são exibidos com categorias incorretas, misturando itens de diferentes tipos.` |
| 504 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:16:08 | fonte: `[chave_de_juncao_errada]` |
| 505 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:16:08 | fonte_citada: `chave_de_juncao_errada` |
| 506 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | quatro_linhas_presentes: confere |
| 507 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | rotulo_no_conjunto: confere |
| 508 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | fonte_existe_na_biblioteca: confere |
| 509 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | fonte_estava_no_contexto: confere |
| 510 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | campo_existe_no_caso: confere |
| 511 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 512 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | notas_nos_verbetes_citados: informativo |
| 513 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | impacto: nao_verificavel |
| 514 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | fonte_formato_valido: confere |
| 515 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | fonte_contem_termo_da_causa: confere |
| 516 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:16:08 | diagnostico: escolha chave_de_juncao_errada; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 516, decisão `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido.
  - Evidência: evento 496 (verbete_entregue: `entidade-produto`, `contrato-produto`, `chave_de_juncao_errada`); evento 500 (resposta); evento 505 (verbete_citado: `chave_de_juncao_errada`).
  - Usou: `entidade-produto`, `contrato-produto`, `chave_de_juncao_errada`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 495 a 516 da trilha; hash dos eventos deste caso: `f27bc1e9d1758c80`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-12`

Caso `relatorio-12` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-12`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1155 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1155 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4674 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (69,03), `contrato-produto` (52,67) e `chave_de_juncao_errada` (31,12) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `chave_de_juncao_errada`; o da entidade, em `entidade-produto` e `contrato-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `nulo_inesperado` (28,10), `tipo_divergente` (27,76), `estrutura_aninhada_divergente` (27,15), `estado_da_tela_divergente` (25,79) e `campo_renomeado` (24,67) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 88 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `chave_de_juncao_errada`, e o primeiro de fora, `nulo_inesperado`, só o texto do caso já punha o primeiro à frente (29,12 contra 26,10), e os reforços em código levaram a diferença a 3,02 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 69,03: 66,03 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 52,67: 49,67 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `chave_de_juncao_errada` | posição 3, pontuação 31,12: 29,12 pelas palavras do caso, mais 2,0 por rota | sim |
| `nulo_inesperado` | posição 4, pontuação 28,10: 26,10 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 5, pontuação 27,76: 24,76 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 6, pontuação 27,15: 24,15 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `estado_da_tela_divergente` | posição 7, pontuação 25,79: 25,79 pelas palavras do caso, sem reforço |  |
| `campo_renomeado` | posição 8, pontuação 24,67: 21,67 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `chave_de_juncao_errada` (Chave de junção errada); segunda: `tipo_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `chave_de_juncao_errada` (declarado).
- O modelo apontou o campo `tipo` (declarado).
- `tipo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,036 contra 0,915 da escolhida; verbetes entregues que a sustentam: `entidade-produto` e `contrato-produto` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,029; as maiores: `colecao_no_lugar_de_objeto` (0,019), `campo_ausente` (0,004) e `campo_renomeado` (0,004) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,915, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `chave_de_juncao_errada` (declarado).
- Verbete citado `chave_de_juncao_errada`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `entidade-produto` e `chave_de_juncao_errada` (conferido).
- Leitura do verbete `chave_de_juncao_errada` (Chave de junção errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/chave_de_juncao_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/chave_de_juncao_errada.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `chave_de_juncao_errada` | 0,915 | `entidade-produto` e `chave_de_juncao_errada` | sim |
| `tipo_divergente` | 0,036 | `entidade-produto` e `contrato-produto` |  |
| `colecao_no_lugar_de_objeto` | 0,019 | `contrato-produto` |  |
| `campo_ausente` | 0,004 | `contrato-produto` |  |
| `campo_renomeado` | 0,004 | `contrato-produto` |  |
| `estrutura_aninhada_divergente` | 0,002 | nenhum |  |
| `resposta_truncada` | 0,001 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `valor_fora_do_dominio` | 0,000 | `chave_de_juncao_errada` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: Os produtos são exibidos com categorias incorretas, misturando itens de diferentes tipos.
> FONTE: [chave_de_juncao_errada]

Resposta inteira:

```text
CAUSA_RAIZ: chave_de_juncao_errada
CAMPO: tipo
IMPACTO: Os produtos são exibidos com categorias incorretas, misturando itens de diferentes tipos.
FONTE: [chave_de_juncao_errada]
```

## Rastro

Gerado dos eventos 495 a 516 da trilha; hash dos eventos deste caso: `f27bc1e9d1758c80` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-12.md`.
