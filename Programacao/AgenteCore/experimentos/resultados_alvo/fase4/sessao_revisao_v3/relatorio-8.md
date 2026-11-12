<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 8 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos`, campo `id`

Caso `relatorio-8` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-8`: o caso `relatorio-8` na corrida `fase4_ineditos`; eventos 418 a 439 da trilha `trilha_ineditos.jsonl`, hash dos eventos `67b8a5451d5833dc` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos`, campo `id`

## 3. Data, organização e autor

Observado em 06/11/2026 14:12:40 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-8`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": -2, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": -3, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": false}]
```

4. Sintoma observado (texto do caso):

> A grade carrega os 14 cartoes sem erro, mas qualquer 'Saiba Mais...' abre o modal com 'Erro' no titulo e 'HTTP 404' no corpo. Ao clicar no botao da Picanha ao Alho, a requisicao disparada foi GET /api/produtos/-2 e a resposta foi 404.

5. Observação adicional (texto do caso):

> O corpo mostra so os itens da Picanha ao Alho e da Picanha Simples; a lista completa tem 14.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A grade carrega os 14 cartoes sem erro, mas qualquer 'Saiba Mais...' abre o modal com 'Erro' no titulo e 'HTTP 404' no corpo. Ao clicar no botao da Picanha ao Alho, a requisicao disparada foi GET /api/produtos/-2 e a resposta foi 404. |

Corpo recebido, como veio no caso:

```text
[{"id": -2, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": -3, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`).
- Caso escrito: `relatorio-8` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-8` em `trilha_ineditos.jsonl`, eventos 418 a 439, hash dos eventos `67b8a5451d5833dc`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)). Campo: `id`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,64 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê um erro ao tentar acessar detalhes de um produto específico, pois a requisição GET está sendo feita com um ID inválido (-2 e -3) em vez do ID correto do produto.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu colecao_no_lugar_de_objeto no campo id porque os verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,18. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,64); trate como hipótese e confira o campo id antes de agir.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": -2, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": -3, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": false}]

SINTOMA OBSERVADO: A grade carrega os 14 cartoes sem erro, mas qualquer 'Saiba Mais...' abre o modal com 'Erro' no titulo e 'HTTP 404' no corpo. Ao clicar no botao da Picanha ao Alho, a requisicao disparada foi GET /api/produtos/-2 e a resposta foi 404.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os itens da Picanha ao Alho e da Picanha Simples; a lista completa tem 14.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> colecao_no_lugar_de_objeto e não campo_ausente: a escolha tem probabilidade 0,64 contra 0,18; verbete(s) na evidência: entidade-produto, contrato-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,64 | sim |
| `campo_ausente` (Campo ausente) | 0,18 |  |
| `campo_renomeado` (Campo renomeado) | 0,18 |  |
| `resposta_truncada` (Resposta truncada) | 0,07 |  |
| `tipo_divergente` (Tipo divergente) | 0,05 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,04 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto`, `estrutura_aninhada_divergente` |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 418 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:12:40 | caso relatorio-8 |
| 419 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:12:40 | 3 de 39 verbetes entregues |
| 421 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:12:40 | diagnostico: 4108 caracteres; verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente |
| 423 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:12:40 | diagnostico: 69,1 s |
| 424 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:12:40 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 425 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:12:40 | campo: `id` |
| 426 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:12:40 | impacto: `O usuário vê um erro ao tentar acessar detalhes de um produto específico, pois a requisição GET está sendo feita com um ID inválido (-2 e -3) em vez do ID correto do produto.` |
| 427 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:12:40 | fonte: `[contrato-produto]` |
| 428 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:12:40 | fonte_citada: `contrato-produto` |
| 429 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:12:40 | quatro_linhas_presentes: confere |
| 430 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:12:40 | rotulo_no_conjunto: confere |
| 431 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:12:40 | fonte_existe_na_biblioteca: confere |
| 432 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:12:40 | fonte_estava_no_contexto: confere |
| 433 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:12:40 | campo_existe_no_caso: confere |
| 434 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:12:40 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 435 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:12:40 | notas_nos_verbetes_citados: informativo |
| 436 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:12:40 | impacto: nao_verificavel |
| 437 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:12:40 | fonte_formato_valido: confere |
| 438 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:12:40 | fonte_contem_termo_da_causa: nao_confere |
| 439 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:12:40 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 439, decisão `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido.
  - Evidência: evento 419 (verbete_entregue: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente`); evento 423 (resposta); evento 428 (verbete_citado: `contrato-produto`).
  - Usou: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 418 a 439 da trilha; hash dos eventos deste caso: `67b8a5451d5833dc`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-8`

Caso `relatorio-8` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-8`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (933 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (933 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4108 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (93,01), `contrato-produto` (51,37) e `estrutura_aninhada_divergente` (36,07) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `estrutura_aninhada_divergente`; o da entidade, em `entidade-produto`, `contrato-produto` e `estrutura_aninhada_divergente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (34,14), `estado_da_tela_divergente` (32,72), `contagem_inconsistente` (28,73), `valor_fora_do_dominio` (27,98) e `tipo_divergente` (27,85) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 87 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `estrutura_aninhada_divergente`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (33,07 contra 32,14), e os reforços em código levaram a diferença a 1,93 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 93,01: 90,01 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 51,37: 48,37 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 3, pontuação 36,07: 33,07 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pagina-produtos-api` | posição 4, pontuação 34,14: 32,14 pelas palavras do caso, mais 2,0 por rota |  |
| `estado_da_tela_divergente` | posição 5, pontuação 32,72: 32,72 pelas palavras do caso, sem reforço |  |
| `contagem_inconsistente` | posição 6, pontuação 28,73: 25,73 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `valor_fora_do_dominio` | posição 7, pontuação 27,98: 25,98 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 8, pontuação 27,85: 24,85 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)); segunda: `campo_ausente`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `colecao_no_lugar_de_objeto` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,177 contra 0,645 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 11 alternativas lidas na resposta somam probabilidade 0,351; as maiores: `campo_renomeado` (0,177), `resposta_truncada` (0,074) e `tipo_divergente` (0,049) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,645, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` (declarado).
- Verbete citado `contrato-produto`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), não traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-produto` e `estrutura_aninhada_divergente` (conferido).
- Leitura do verbete `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `colecao_no_lugar_de_objeto` | 0,645 | `contrato-produto` e `estrutura_aninhada_divergente` | sim |
| `campo_ausente` | 0,177 | `contrato-produto` |  |
| `campo_renomeado` | 0,177 | `contrato-produto` e `estrutura_aninhada_divergente` |  |
| `resposta_truncada` | 0,074 | nenhum |  |
| `tipo_divergente` | 0,049 | `entidade-produto` e `contrato-produto` |  |
| `estrutura_aninhada_divergente` | 0,036 | `estrutura_aninhada_divergente` |  |
| `corpo_nao_e_json` | 0,005 | nenhum |  |
| `corpo_vazio` | 0,005 | nenhum |  |
| `valor_fora_do_dominio` | 0,004 | nenhum |  |
| `chave_de_juncao_errada` | 0,001 | `entidade-produto` |  |
| `estado_da_tela_divergente` | 0,001 | nenhum |  |
| `formato_de_data_divergente` | 0,001 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um erro ao tentar acessar detalhes de um produto específico, pois a requisição GET está sendo feita com um ID inválido (-2 e -3) em vez do ID correto do produto.
> FONTE: [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: colecao_no_lugar_de_objeto
CAMPO: id
IMPACTO: O usuário vê um erro ao tentar acessar detalhes de um produto específico, pois a requisição GET está sendo feita com um ID inválido (-2 e -3) em vez do ID correto do produto.
FONTE: [contrato-produto]
```

## Rastro

Gerado dos eventos 418 a 439 da trilha; hash dos eventos deste caso: `67b8a5451d5833dc` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-8.md`.
