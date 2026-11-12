<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 26 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Recurso inexistente (404 e vizinhos) em `GET /api/produtos/5`, campo `id`

Caso `relatorio-26` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-26`: o caso `relatorio-26` na corrida `fase4_ineditos`; eventos 618 a 639 da trilha `trilha_ineditos.jsonl`, hash dos eventos `43860baed69d86cb` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Recurso inexistente (404 e vizinhos) em `GET /api/produtos/5`, campo `id`

## 3. Data, organização e autor

Observado em 06/11/2026 14:21:59 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/5` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-26`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/5`, status 404 (a API não achou o recurso).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"detail": "produto não encontrado"}
```

4. Sintoma observado (texto do caso):

> A grade foi carregada com os 14 cartoes, entre eles o da Alcatra na Pedra; ao clicar no 'Saiba Mais...' desse cartao, o modal abre com 'Erro' no titulo e 'HTTP 404' no corpo.

5. Observação adicional (texto do caso):

> O id 5 aparece na listagem GET /api/produtos feita antes do clique, e GET /api/produtos/5 respondeu 200 em chamadas anteriores.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/5` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A grade foi carregada com os 14 cartoes, entre eles o da Alcatra na Pedra; ao clicar no 'Saiba Mais...' desse cartao, o modal abre com 'Erro' no titulo e 'HTTP 404' no corpo. |

Corpo recebido, como veio no caso:

```text
{"detail": "produto não encontrado"}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `recurso_inexistente` (Recurso inexistente (404 e vizinhos); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/recurso_inexistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/recurso_inexistente.md`).
- Verbetes entregues pela busca e não citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `mensagens-de-erro-do-codigo` (Índice de mensagens literais do código; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/mensagens-de-erro-do-codigo.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/mensagens-de-erro-do-codigo.md`).
- Caso escrito: `relatorio-26` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-26` em `trilha_ineditos.jsonl`, eventos 618 a 639, hash dos eventos `43860baed69d86cb`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `recurso_inexistente` (Recurso inexistente (404 e vizinhos)). Campo: `id`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê um erro "HTTP 404" ao tentar acessar detalhes do produto, indicando que o recurso não existe.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu recurso_inexistente no campo id porque os verbetes recurso_inexistente, contrato-produto, mensagens-de-erro-do-codigo estavam entre os entregues ao modelo. A segunda causa, registro_duplicado, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/5

STATUS HTTP: 404

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "produto não encontrado"}

SINTOMA OBSERVADO: A grade foi carregada com os 14 cartoes, entre eles o da Alcatra na Pedra; ao clicar no 'Saiba Mais...' desse cartao, o modal abre com 'Erro' no titulo e 'HTTP 404' no corpo.

OBSERVAÇÃO ADICIONAL: O id 5 aparece na listagem GET /api/produtos feita antes do clique, e GET /api/produtos/5 respondeu 200 em chamadas anteriores.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> recurso_inexistente e não registro_duplicado: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: recurso_inexistente, contrato-produto, mensagens-de-erro-do-codigo

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `recurso_inexistente` (Recurso inexistente (404 e vizinhos)) | 1,00 | sim |
| `registro_duplicado` (Registro duplicado) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[recurso_inexistente]`; verbetes citados: `recurso_inexistente` (Recurso inexistente (404 e vizinhos); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/recurso_inexistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/recurso_inexistente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `recurso_inexistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `recurso_inexistente` | confere | contexto: `recurso_inexistente`, `contrato-produto`, `mensagens-de-erro-do-codigo` |
| Algum verbete do contexto trata da causa respondida | `recurso_inexistente` | confere | verbetes: `recurso_inexistente`, `contrato-produto`, `mensagens-de-erro-do-codigo` |
| A linha FONTE só tem identificadores, no formato pedido | `[recurso_inexistente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["recurso_inexistente"]} |
| O verbete citado fala da causa respondida | `recurso_inexistente` | confere | {"termo": "recurso_inexistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 618 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:21:59 | caso relatorio-26 |
| 619 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:21:59 | 3 de 39 verbetes entregues |
| 621 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:21:59 | diagnostico: 3566 caracteres; verbetes recurso_inexistente, contrato-produto, mensagens-de-erro-do-codigo |
| 623 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:21:59 | diagnostico: 75,2 s |
| 624 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:21:59 | causa_raiz: `recurso_inexistente` |
| 625 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:21:59 | campo: `id` |
| 626 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:21:59 | impacto: `O usuário vê um erro "HTTP 404" ao tentar acessar detalhes do produto, indicando que o recurso não existe.` |
| 627 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:21:59 | fonte: `[recurso_inexistente]` |
| 628 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:21:59 | fonte_citada: `recurso_inexistente` |
| 629 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:21:59 | quatro_linhas_presentes: confere |
| 630 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:21:59 | rotulo_no_conjunto: confere |
| 631 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:21:59 | fonte_existe_na_biblioteca: confere |
| 632 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:21:59 | fonte_estava_no_contexto: confere |
| 633 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:21:59 | campo_existe_no_caso: confere |
| 634 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:21:59 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 635 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:21:59 | notas_nos_verbetes_citados: informativo |
| 636 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:21:59 | impacto: nao_verificavel |
| 637 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:21:59 | fonte_formato_valido: confere |
| 638 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:21:59 | fonte_contem_termo_da_causa: confere |
| 639 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:21:59 | diagnostico: escolha recurso_inexistente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 639, decisão `diagnostico`: escolha `recurso_inexistente`; resultado rotulo_emitido.
  - Evidência: evento 619 (verbete_entregue: `recurso_inexistente`, `contrato-produto`, `mensagens-de-erro-do-codigo`); evento 623 (resposta); evento 628 (verbete_citado: `recurso_inexistente`).
  - Usou: `recurso_inexistente`, `contrato-produto`, `mensagens-de-erro-do-codigo`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 618 a 639 da trilha; hash dos eventos deste caso: `43860baed69d86cb`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-26`

Caso `relatorio-26` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-26`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (606 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (606 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3566 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `recurso_inexistente` (50,44), `contrato-produto` (28,80) e `mensagens-de-erro-do-codigo` (25,66) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `recurso_inexistente` e `contrato-produto`; o da entidade, em `contrato-produto`; o do status, em `recurso_inexistente`, `contrato-produto` e `mensagens-de-erro-do-codigo` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `contagem_inconsistente` (25,24), `pagina-produtos-api` (24,78), `ancora-saiba-mais` (24,26), `entidade-produto` (20,22) e `colecao_no_lugar_de_objeto` (19,84) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 404 e 51 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `mensagens-de-erro-do-codigo`, e o primeiro de fora, `contagem_inconsistente`, só o texto do caso já punha o primeiro à frente (24,66 contra 24,24), e os reforços em código levaram a diferença a 0,43 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `recurso_inexistente` | posição 1, pontuação 50,44: 47,44 pelas palavras do caso, mais 2,0 por rota e 1,0 por status | sim |
| `contrato-produto` | posição 2, pontuação 28,80: 24,80 pelas palavras do caso, mais 2,0 por rota, 1,0 por entidade e 1,0 por status | sim |
| `mensagens-de-erro-do-codigo` | posição 3, pontuação 25,66: 24,66 pelas palavras do caso, mais 1,0 por status | sim |
| `contagem_inconsistente` | posição 4, pontuação 25,24: 24,24 pelas palavras do caso, mais 1,0 por entidade |  |
| `pagina-produtos-api` | posição 5, pontuação 24,78: 22,78 pelas palavras do caso, mais 2,0 por rota |  |
| `ancora-saiba-mais` | posição 6, pontuação 24,26: 24,26 pelas palavras do caso, sem reforço |  |
| `entidade-produto` | posição 7, pontuação 20,22: 17,22 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 8, pontuação 19,84: 16,84 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `recurso_inexistente` (Recurso inexistente (404 e vizinhos)); segunda: `registro_duplicado`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `recurso_inexistente` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `registro_duplicado` (Registro duplicado), ficou com probabilidade 0,000 contra 0,996 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 3 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `campo_renomeado` (0,000) e `resposta_truncada` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,996, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/5`, o status 404 (a API não achou o recurso) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `recurso_inexistente` (declarado).
- Verbete citado `recurso_inexistente`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `recurso_inexistente`, `contrato-produto` e `mensagens-de-erro-do-codigo` (conferido).
- Leitura do verbete `recurso_inexistente` (Recurso inexistente (404 e vizinhos); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/recurso_inexistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/recurso_inexistente.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `recurso_inexistente` | 0,996 | `recurso_inexistente`, `contrato-produto` e `mensagens-de-erro-do-codigo` | sim |
| `registro_duplicado` | 0,000 | nenhum |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `resposta_truncada` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um erro "HTTP 404" ao tentar acessar detalhes do produto, indicando que o recurso não existe.
> FONTE: [recurso_inexistente]

Resposta inteira:

```text
CAUSA_RAIZ: recurso_inexistente
CAMPO: id
IMPACTO: O usuário vê um erro "HTTP 404" ao tentar acessar detalhes do produto, indicando que o recurso não existe.
FONTE: [recurso_inexistente]
```

## Rastro

Gerado dos eventos 618 a 639 da trilha; hash dos eventos deste caso: `43860baed69d86cb` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-26.md`.
