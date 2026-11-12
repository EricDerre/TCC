<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 1 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Codificação de caracteres incorreta em `GET /api/produtos/14`, campo `resumo`

Caso `relatorio-1` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-1`: o caso `relatorio-1` na corrida `fase4_ineditos`; eventos 49 a 74 da trilha `trilha_ineditos.jsonl`, hash dos eventos `a8c4e961f75bf6bd` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Codificação de caracteres incorreta em `GET /api/produtos/14`, campo `resumo`

## 3. Data, organização e autor

Observado em 06/11/2026 13:54:54 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/14` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-1`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/14`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e aÃ§Ãºcar", "tipo": "Sobremesas", "preco": 14.9, "imagem": "abacaxi.jpg", "destaque": false}
```

4. Sintoma observado (texto do caso):

> O modal do Abacaxi na Brasa abre com o titulo certo, mas o texto de descricao aparece como 'Com canela e aÃ§Ãºcar': cada letra acentuada virou um par de simbolos estranhos.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/14` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O modal do Abacaxi na Brasa abre com o titulo certo, mas o texto de descricao aparece como 'Com canela e aÃ§Ãºcar': cada letra acentuada virou um par de simbolos estranhos. |

Corpo recebido, como veio no caso:

```text
{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e aÃ§Ãºcar", "tipo": "Sobremesas", "preco": 14.9, "imagem": "abacaxi.jpg", "destaque": false}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `estado_da_tela_divergente` (Estado da tela divergente da resposta; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estado_da_tela_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estado_da_tela_divergente.md`).
- Caso escrito: `relatorio-1` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-1` em `trilha_ineditos.jsonl`, eventos 49 a 74, hash dos eventos `a8c4e961f75bf6bd`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `codificacao_incorreta` (Codificação de caracteres incorreta). Campo: `resumo`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O texto de descrição do Abacaxi na Brasa aparece corrompido com símbolos estranhos.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu codificacao_incorreta no campo resumo porque os verbetes entidade-produto, contrato-produto, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/14

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e aÃ§Ãºcar", "tipo": "Sobremesas", "preco": 14.9, "imagem": "abacaxi.jpg", "destaque": false}

SINTOMA OBSERVADO: O modal do Abacaxi na Brasa abre com o titulo certo, mas o texto de descricao aparece como 'Com canela e aÃ§Ãºcar': cada letra acentuada virou um par de simbolos estranhos.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> codificacao_incorreta e não formato_de_data_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, estado_da_tela_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `codificacao_incorreta` (Codificação de caracteres incorreta) | 1,00 | sim |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[entidade-produto], [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["entidade-produto", "contrato-produto"]} |
| O verbete citado fala da causa respondida | `entidade-produto` | não confere | {"termo": "codificacao_incorreta"} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `resumo` no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 49 | 1 | entrada | programa | ao_vivo | 2026-11-06T13:54:54 | caso relatorio-1 |
| 50 | 2 | candidatos | programa | ao_vivo | 2026-11-06T13:54:54 | 3 de 39 verbetes entregues |
| 52 | 3 | prompt | programa | ao_vivo | 2026-11-06T13:54:54 | diagnostico: 3606 caracteres; verbetes entidade-produto, contrato-produto, estado_da_tela_divergente |
| 54 | 4 | inferencia | programa | ao_vivo | 2026-11-06T13:54:54 | diagnostico: 63,7 s |
| 55 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T13:54:54 | causa_raiz: `codificacao_incorreta` |
| 56 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T13:54:54 | campo: `resumo` |
| 57 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T13:54:54 | impacto: `O texto de descrição do Abacaxi na Brasa aparece corrompido com símbolos estranhos.` |
| 58 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T13:54:54 | fonte: `[entidade-produto], [contrato-produto]` |
| 59 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T13:54:54 | fonte_citada: `entidade-produto` |
| 60 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T13:54:54 | fonte_citada: `contrato-produto` |
| 61 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | quatro_linhas_presentes: confere |
| 62 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | rotulo_no_conjunto: confere |
| 63 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | fonte_existe_na_biblioteca: confere |
| 64 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | fonte_existe_na_biblioteca: confere |
| 65 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | fonte_estava_no_contexto: confere |
| 66 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | fonte_estava_no_contexto: confere |
| 67 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | campo_existe_no_caso: confere |
| 68 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 69 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | notas_nos_verbetes_citados: informativo |
| 70 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | impacto: nao_verificavel |
| 71 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | fonte_formato_valido: confere |
| 72 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | fonte_contem_termo_da_causa: nao_confere |
| 73 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T13:54:54 | fonte_contem_termo_da_causa: nao_confere |
| 74 | 24 | decisao | programa | ao_vivo | 2026-11-06T13:54:54 | diagnostico: escolha codificacao_incorreta; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 74, decisão `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido.
  - Evidência: evento 50 (verbete_entregue: `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente`); evento 54 (resposta); evento 59 (verbete_citado: `entidade-produto`); evento 60 (verbete_citado: `contrato-produto`).
  - Usou: `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 49 a 74 da trilha; hash dos eventos deste caso: `a8c4e961f75bf6bd`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-1`

Caso `relatorio-1` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-1`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 25 afirmações (15 observado, 7 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (572 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (572 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3606 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (31,35), `contrato-produto` (26,07) e `estado_da_tela_divergente` (22,21) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; `estado_da_tela_divergente` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `tipo_divergente` (17,22), `estrutura_aninhada_divergente` (16,69), `colecao_no_lugar_de_objeto` (15,92), `campo_renomeado` (15,88) e `pagina-produtos-api` (15,87) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 49 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `estado_da_tela_divergente`, e o primeiro de fora, `tipo_divergente`, só o texto do caso já punha o primeiro à frente (22,21 contra 16,22); a diferença final foi 4,99 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 31,35: 28,35 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 26,07: 23,07 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estado_da_tela_divergente` | posição 3, pontuação 22,21: 22,21 pelas palavras do caso, sem reforço | sim |
| `tipo_divergente` | posição 4, pontuação 17,22: 16,22 pelas palavras do caso, mais 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 5, pontuação 16,69: 15,69 pelas palavras do caso, mais 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 15,92: 12,92 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_renomeado` | posição 7, pontuação 15,88: 14,88 pelas palavras do caso, mais 1,0 por entidade |  |
| `pagina-produtos-api` | posição 8, pontuação 15,87: 13,87 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `codificacao_incorreta` (Codificação de caracteres incorreta); segunda: `formato_de_data_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `codificacao_incorreta` (declarado).
- O modelo apontou o campo `resumo` (declarado).
- `resumo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `formato_de_data_divergente` (Formato de data divergente), ficou com probabilidade 0,000 contra 0,999 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `tipo_divergente` (0,000), `campo_ausente` (0,000) e `campo_renomeado` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,999, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/14`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `entidade-produto` e `contrato-produto` (declarado).
- Os 2 verbetes citados (`entidade-produto` e `contrato-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Camada de leitura de cada verbete citado: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 8 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `codificacao_incorreta` | 0,999 | nenhum | sim |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `tipo_divergente` | 0,000 | `entidade-produto` e `contrato-produto` |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | `estado_da_tela_divergente` |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O texto de descrição do Abacaxi na Brasa aparece corrompido com símbolos estranhos.
> FONTE: [entidade-produto], [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: codificacao_incorreta
CAMPO: resumo
IMPACTO: O texto de descrição do Abacaxi na Brasa aparece corrompido com símbolos estranhos.
FONTE: [entidade-produto], [contrato-produto]
```

## Rastro

Gerado dos eventos 49 a 74 da trilha; hash dos eventos deste caso: `a8c4e961f75bf6bd` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-1.md`.
