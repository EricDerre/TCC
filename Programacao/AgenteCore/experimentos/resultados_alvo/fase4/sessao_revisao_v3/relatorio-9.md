<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 9 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Codificação de caracteres incorreta em `GET /api/produtos/11`, campo `nome`

Caso `relatorio-9` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-9`: o caso `relatorio-9` na corrida `fase4_ineditos`; eventos 103 a 128 da trilha `trilha_ineditos.jsonl`, hash dos eventos `3db8657b1dba4adb` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Codificação de caracteres incorreta em `GET /api/produtos/11`, campo `nome`

## 3. Data, organização e autor

Observado em 06/11/2026 13:57:05 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/11` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-9`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/11`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}
```

4. Sintoma observado (texto do caso):

> Na mesma tela, o cartao do Pão de Alho mostra o titulo 'Pão de Alho', mas o modal aberto pelo 'Saiba Mais...' desse mesmo cartao mostra o titulo 'PÃ£o de Alho'. A grade foi carregada antes do clique e as duas respostas chegaram com status 200.

5. Observação adicional (texto do caso):

> A listagem GET /api/produtos, feita antes do clique, trouxe este produto (id 11) com o nome 'Pão de Alho'; so a resposta do detalhe veio com os simbolos estranhos.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/11` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Na mesma tela, o cartao do Pão de Alho mostra o titulo 'Pão de Alho', mas o modal aberto pelo 'Saiba Mais...' desse mesmo cartao mostra o titulo 'PÃ£o de Alho'. A grade foi carregada antes do clique e as duas respostas chegaram com status 200. |

Corpo recebido, como veio no caso:

```text
{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Verbetes entregues pela busca e não citados: `pagina-produtos-api` (Aba "Produtos (API)", a fronteira JSON; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/pagina-produtos-api.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/pagina-produtos-api.md`).
- Caso escrito: `relatorio-9` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-9` em `trilha_ineditos.jsonl`, eventos 103 a 128, hash dos eventos `3db8657b1dba4adb`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `codificacao_incorreta` (Codificação de caracteres incorreta). Campo: `nome`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê o título do cartão corretamente, mas o modal exibe o título com caracteres estranhos.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu codificacao_incorreta no campo nome porque os verbetes entidade-produto, campo_ausente, pagina-produtos-api estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/11

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}

SINTOMA OBSERVADO: Na mesma tela, o cartao do Pão de Alho mostra o titulo 'Pão de Alho', mas o modal aberto pelo 'Saiba Mais...' desse mesmo cartao mostra o titulo 'PÃ£o de Alho'. A grade foi carregada antes do clique e as duas respostas chegaram com status 200.

OBSERVAÇÃO ADICIONAL: A listagem GET /api/produtos, feita antes do clique, trouxe este produto (id 11) com o nome 'Pão de Alho'; so a resposta do detalhe veio com os simbolos estranhos.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> codificacao_incorreta e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, campo_ausente, pagina-produtos-api

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `codificacao_incorreta` (Codificação de caracteres incorreta) | 1,00 | sim |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente] [entidade-produto]`; verbetes citados: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `campo_ausente`, `pagina-produtos-api` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `campo_ausente`, `pagina-produtos-api` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[campo_ausente] [entidade-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_ausente", "entidade-produto"]} |
| O verbete citado fala da causa respondida | `campo_ausente` | não confere | {"termo": "codificacao_incorreta"} |
| O verbete citado fala da causa respondida | `entidade-produto` | não confere | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 103 | 1 | entrada | programa | ao_vivo | 2026-11-06T13:57:05 | caso relatorio-9 |
| 104 | 2 | candidatos | programa | ao_vivo | 2026-11-06T13:57:05 | 3 de 39 verbetes entregues |
| 106 | 3 | prompt | programa | ao_vivo | 2026-11-06T13:57:05 | diagnostico: 3654 caracteres; verbetes entidade-produto, campo_ausente, pagina-produtos-api |
| 108 | 4 | inferencia | programa | ao_vivo | 2026-11-06T13:57:05 | diagnostico: 59,1 s |
| 109 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T13:57:05 | causa_raiz: `codificacao_incorreta` |
| 110 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T13:57:05 | campo: `nome` |
| 111 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T13:57:05 | impacto: `O usuário vê o título do cartão corretamente, mas o modal exibe o título com caracteres estranhos.` |
| 112 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T13:57:05 | fonte: `[campo_ausente] [entidade-produto]` |
| 113 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T13:57:05 | fonte_citada: `campo_ausente` |
| 114 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T13:57:05 | fonte_citada: `entidade-produto` |
| 115 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | quatro_linhas_presentes: confere |
| 116 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | rotulo_no_conjunto: confere |
| 117 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | fonte_existe_na_biblioteca: confere |
| 118 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | fonte_existe_na_biblioteca: confere |
| 119 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | fonte_estava_no_contexto: confere |
| 120 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | fonte_estava_no_contexto: confere |
| 121 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | campo_existe_no_caso: confere |
| 122 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 123 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | notas_nos_verbetes_citados: informativo |
| 124 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | impacto: nao_verificavel |
| 125 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | fonte_formato_valido: confere |
| 126 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | fonte_contem_termo_da_causa: nao_confere |
| 127 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T13:57:05 | fonte_contem_termo_da_causa: nao_confere |
| 128 | 24 | decisao | programa | ao_vivo | 2026-11-06T13:57:05 | diagnostico: escolha codificacao_incorreta; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 128, decisão `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido.
  - Evidência: evento 104 (verbete_entregue: `entidade-produto`, `campo_ausente`, `pagina-produtos-api`); evento 108 (resposta); evento 113 (verbete_citado: `campo_ausente`); evento 114 (verbete_citado: `entidade-produto`).
  - Usou: `entidade-produto`, `campo_ausente`, `pagina-produtos-api`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 103 a 128 da trilha; hash dos eventos deste caso: `3db8657b1dba4adb`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-9`

Caso `relatorio-9` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-9`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 25 afirmações (15 observado, 7 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (841 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (841 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3654 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (59,44), `campo_ausente` (37,02) e `pagina-produtos-api` (31,67) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `pagina-produtos-api`; o da entidade, em `entidade-produto` e `campo_ausente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `contrato-produto` (31,57), `codificacao_incorreta` (29,36), `colecao_no_lugar_de_objeto` (27,63), `registro_duplicado` (27,50) e `estado_da_tela_divergente` (27,44) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 81 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `pagina-produtos-api`, e o primeiro de fora, `contrato-produto`, só o texto do caso já punha o primeiro à frente (29,67 contra 28,57), e os reforços em código levaram a diferença a 0,09 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 59,44: 56,44 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_ausente` | posição 2, pontuação 37,02: 36,02 pelas palavras do caso, mais 1,0 por entidade | sim |
| `pagina-produtos-api` | posição 3, pontuação 31,67: 29,67 pelas palavras do caso, mais 2,0 por rota | sim |
| `contrato-produto` | posição 4, pontuação 31,57: 28,57 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `codificacao_incorreta` | posição 5, pontuação 29,36: 29,36 pelas palavras do caso, sem reforço |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 27,63: 24,63 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `registro_duplicado` | posição 7, pontuação 27,50: 27,50 pelas palavras do caso, sem reforço |  |
| `estado_da_tela_divergente` | posição 8, pontuação 27,44: 27,44 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `codificacao_incorreta` (Codificação de caracteres incorreta); segunda: `campo_ausente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `codificacao_incorreta` (declarado).
- O modelo apontou o campo `nome` (declarado).
- `nome` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,000 contra 1,000 da escolhida; verbetes entregues que a sustentam: `campo_ausente` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_renomeado` (0,000), `formato_de_data_divergente` (0,000) e `chave_de_juncao_errada` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 1,000, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/11`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `campo_ausente` e `entidade-produto` (declarado).
- Os 2 verbetes citados (`campo_ausente` e `entidade-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Camada de leitura de cada verbete citado: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 8 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `codificacao_incorreta` | 1,000 | nenhum | sim |
| `campo_ausente` | 0,000 | `campo_ausente` |  |
| `campo_renomeado` | 0,000 | `campo_ausente` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` |  |
| `tipo_divergente` | 0,000 | `entidade-produto` e `pagina-produtos-api` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | `pagina-produtos-api` |  |
| `estrutura_aninhada_divergente` | 0,000 | `campo_ausente` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê o título do cartão corretamente, mas o modal exibe o título com caracteres estranhos.
> FONTE: [campo_ausente] [entidade-produto]

Resposta inteira:

```text
CAUSA_RAIZ: codificacao_incorreta
CAMPO: nome
IMPACTO: O usuário vê o título do cartão corretamente, mas o modal exibe o título com caracteres estranhos.
FONTE: [campo_ausente] [entidade-produto]
```

## Rastro

Gerado dos eventos 103 a 128 da trilha; hash dos eventos deste caso: `3db8657b1dba4adb` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-9.md`.
