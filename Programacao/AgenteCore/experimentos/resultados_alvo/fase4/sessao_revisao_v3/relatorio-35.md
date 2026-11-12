<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 35 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Resposta truncada em `GET /api/produtos`, campo `preco`

Caso `relatorio-35` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-35`: o caso `relatorio-35` na corrida `fase4_ineditos`; eventos 249 a 274 da trilha `trilha_ineditos.jsonl`, hash dos eventos `43855b1f6738e30c` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Resposta truncada em `GET /api/produtos`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 14:04:08 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-35`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Bebidas", "imagem": "refrigerante.png", "destaque": false}]
```

4. Sintoma observado (texto do caso):

> Na grade de bebidas, o botao de preco da Agua Mineral e o do Refrigerante mostram 'undefined', e o do Balde de Cerveja mostra 'R$ 45,00'. Ao recarregar a pagina, os produtos afetados mudam.

5. Observação adicional (texto do caso):

> O corpo mostra so os itens de id 8 a 10; a lista completa tem 14.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Na grade de bebidas, o botao de preco da Agua Mineral e o do Refrigerante mostram 'undefined', e o do Balde de Cerveja mostra 'R$ 45,00'. Ao recarregar a pagina, os produtos afetados mudam. |

Corpo recebido, como veio no caso:

```text
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Bebidas", "imagem": "refrigerante.png", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `relatorio-35` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-35` em `trilha_ineditos.jsonl`, eventos 249 a 274, hash dos eventos `43855b1f6738e30c`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `resposta_truncada` (Resposta truncada). Campo: `preco`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,95 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê preços incorretos ou 'undefined' para alguns produtos, devido à lista truncada.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu resposta_truncada no campo preco porque os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,02. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Bebidas", "imagem": "refrigerante.png", "destaque": false}]

SINTOMA OBSERVADO: Na grade de bebidas, o botao de preco da Agua Mineral e o do Refrigerante mostram 'undefined', e o do Balde de Cerveja mostra 'R$ 45,00'. Ao recarregar a pagina, os produtos afetados mudam.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os itens de id 8 a 10; a lista completa tem 14.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> resposta_truncada e não campo_ausente: a escolha tem probabilidade 0,95 contra 0,02; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `resposta_truncada` (Resposta truncada) | 0,95 | sim |
| `campo_ausente` (Campo ausente) | 0,02 |  |
| `campo_renomeado` (Campo renomeado) | 0,02 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,01 |  |
| `corpo_vazio` (Corpo vazio) | 0,01 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,01 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `contagem_inconsistente` (Contagem inconsistente) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [campo_ausente]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto], [campo_ausente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "campo_ausente"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "resposta_truncada"} |
| O verbete citado fala da causa respondida | `campo_ausente` | não confere | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 249 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:04:08 | caso relatorio-35 |
| 250 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:04:08 | 3 de 39 verbetes entregues |
| 252 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:04:08 | diagnostico: 3917 caracteres; verbetes entidade-produto, contrato-produto, campo_ausente |
| 254 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:04:08 | diagnostico: 46,5 s |
| 255 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:08 | causa_raiz: `resposta_truncada` |
| 256 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:08 | campo: `preco` |
| 257 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:08 | impacto: `O usuário vê preços incorretos ou 'undefined' para alguns produtos, devido à lista truncada.` |
| 258 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:08 | fonte: `[contrato-produto], [campo_ausente]` |
| 259 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:08 | fonte_citada: `contrato-produto` |
| 260 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:08 | fonte_citada: `campo_ausente` |
| 261 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | quatro_linhas_presentes: confere |
| 262 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | rotulo_no_conjunto: confere |
| 263 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_existe_na_biblioteca: confere |
| 264 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_existe_na_biblioteca: confere |
| 265 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_estava_no_contexto: confere |
| 266 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_estava_no_contexto: confere |
| 267 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | campo_existe_no_caso: confere |
| 268 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 269 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | notas_nos_verbetes_citados: informativo |
| 270 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | impacto: nao_verificavel |
| 271 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_formato_valido: confere |
| 272 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_contem_termo_da_causa: nao_confere |
| 273 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_contem_termo_da_causa: nao_confere |
| 274 | 24 | decisao | programa | ao_vivo | 2026-11-06T14:04:08 | diagnostico: escolha resposta_truncada; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 274, decisão `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido.
  - Evidência: evento 250 (verbete_entregue: `entidade-produto`, `contrato-produto`, `campo_ausente`); evento 254 (resposta); evento 259 (verbete_citado: `contrato-produto`); evento 260 (verbete_citado: `campo_ausente`).
  - Usou: `entidade-produto`, `contrato-produto`, `campo_ausente`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 249 a 274 da trilha; hash dos eventos deste caso: `43855b1f6738e30c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-35`

Caso `relatorio-35` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-35`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 25 afirmações (15 observado, 7 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (961 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (961 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3917 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (67,86), `contrato-produto` (66,00) e `campo_ausente` (45,13) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `campo_ausente`; o da entidade, em `entidade-produto`, `contrato-produto` e `campo_ausente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `nulo_inesperado` (37,38), `campo_renomeado` (32,69), `chave_de_juncao_errada` (31,71), `campo_preco_ausente` (29,31) e `pagina-produtos-api` (29,10) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 89 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `campo_ausente`, e o primeiro de fora, `nulo_inesperado`, só o texto do caso já punha o primeiro à frente (42,13 contra 35,38), e os reforços em código levaram a diferença a 7,75 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 67,86: 64,86 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 66,00: 63,00 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_ausente` | posição 3, pontuação 45,13: 42,13 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `nulo_inesperado` | posição 4, pontuação 37,38: 35,38 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_renomeado` | posição 5, pontuação 32,69: 29,69 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 6, pontuação 31,71: 29,71 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_preco_ausente` | posição 7, pontuação 29,31: 28,31 pelas palavras do caso, mais 1,0 por entidade |  |
| `pagina-produtos-api` | posição 8, pontuação 29,10: 27,10 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `resposta_truncada` (Resposta truncada); segunda: `campo_ausente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `resposta_truncada` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,020 contra 0,950 da escolhida; verbetes entregues que a sustentam: `contrato-produto` e `campo_ausente` (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,055; as maiores: `campo_renomeado` (0,020), `corpo_nao_e_json` (0,010) e `corpo_vazio` (0,010) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,950, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `campo_ausente` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `campo_ausente`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 8 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `resposta_truncada` | 0,950 | nenhum | sim |
| `campo_ausente` | 0,020 | `contrato-produto` e `campo_ausente` |  |
| `campo_renomeado` | 0,020 | `contrato-produto` e `campo_ausente` |  |
| `corpo_nao_e_json` | 0,010 | nenhum |  |
| `corpo_vazio` | 0,010 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,008 | `contrato-produto` |  |
| `tipo_divergente` | 0,004 | `entidade-produto` e `contrato-produto` |  |
| `contagem_inconsistente` | 0,001 | nenhum |  |
| `formato_de_data_divergente` | 0,001 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,000 | `campo_ausente` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê preços incorretos ou 'undefined' para alguns produtos, devido à lista truncada.
> FONTE: [contrato-produto], [campo_ausente]

Resposta inteira:

```text
CAUSA_RAIZ: resposta_truncada
CAMPO: preco
IMPACTO: O usuário vê preços incorretos ou 'undefined' para alguns produtos, devido à lista truncada.
FONTE: [contrato-produto], [campo_ausente]
```

## Rastro

Gerado dos eventos 249 a 274 da trilha; hash dos eventos deste caso: `43855b1f6738e30c` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-35.md`.
