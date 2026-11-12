<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 3 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Tempo de resposta excedido em `GET /api/produtos/7`

Caso `relatorio-3` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-3`: o caso `relatorio-3` na corrida `fase4_ineditos`; eventos 668 a 689 da trilha `trilha_ineditos.jsonl`, hash dos eventos `08fa9d48a150a287` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Tempo de resposta excedido em `GET /api/produtos/7`

## 3. Data, organização e autor

Observado em 06/11/2026 14:24:29 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/7` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-3`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/7`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}
```

4. Sintoma observado (texto do caso):

> Ao clicar em 'Saiba Mais...' do Cupim, nada acontece por cerca de 2 segundos e so entao o modal abre, com os dados certos. O roteiro espera o modal por 1 segundo e reprova por tempo.

5. Observação adicional (texto do caso):

> As outras requisicoes da mesma sessao responderam em menos de 100 ms.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/7` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Ao clicar em 'Saiba Mais...' do Cupim, nada acontece por cerca de 2 segundos e so entao o modal abre, com os dados certos. O roteiro espera o modal por 1 segundo e reprova por tempo. |

Corpo recebido, como veio no caso:

```text
{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `ancora-saiba-mais` (Link "Saiba Mais..." abre produto vazio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/defeitos_conhecidos/ancora-saiba-mais.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/defeitos_conhecidos/ancora-saiba-mais.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `relatorio-3` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-3` em `trilha_ineditos.jsonl`, eventos 668 a 689, hash dos eventos `08fa9d48a150a287`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `tempo_de_resposta_excedido` (Tempo de resposta excedido). Campo: nenhum apontado. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,83 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê um modal demorado a abrir, com dados corretos, após um breve tempo de espera.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu tempo_de_resposta_excedido porque os verbetes entidade-produto, ancora-saiba-mais, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,12. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida tempo_de_resposta_excedido. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida tempo_de_resposta_excedido.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/7

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}

SINTOMA OBSERVADO: Ao clicar em 'Saiba Mais...' do Cupim, nada acontece por cerca de 2 segundos e so entao o modal abre, com os dados certos. O roteiro espera o modal por 1 segundo e reprova por tempo.

OBSERVAÇÃO ADICIONAL: As outras requisicoes da mesma sessao responderam em menos de 100 ms.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> tempo_de_resposta_excedido e não tipo_divergente: a escolha tem probabilidade 0,83 contra 0,12; verbete(s) na evidência: entidade-produto, ancora-saiba-mais, contrato-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 0,83 | sim |
| `tipo_divergente` (Tipo divergente) | 0,12 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,02 |  |
| `resposta_truncada` (Resposta truncada) | 0,01 |  |
| `campo_ausente` (Campo ausente) | 0,01 |  |
| `campo_renomeado` (Campo renomeado) | 0,01 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,01 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[ancora-saiba-mais]`; verbetes citados: `ancora-saiba-mais` (Link "Saiba Mais..." abre produto vazio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/defeitos_conhecidos/ancora-saiba-mais.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/defeitos_conhecidos/ancora-saiba-mais.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `ancora-saiba-mais` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `ancora-saiba-mais` | confere | contexto: `entidade-produto`, `ancora-saiba-mais`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[ancora-saiba-mais]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["ancora-saiba-mais"]} |
| O verbete citado fala da causa respondida | `ancora-saiba-mais` | não confere | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 668 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:24:29 | caso relatorio-3 |
| 669 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:24:29 | 3 de 39 verbetes entregues |
| 671 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:24:29 | diagnostico: 3593 caracteres; verbetes entidade-produto, ancora-saiba-mais, contrato-produto |
| 673 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:24:29 | diagnostico: 63,6 s |
| 674 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:24:29 | causa_raiz: `tempo_de_resposta_excedido` |
| 675 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:24:29 | campo: `nenhum` |
| 676 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:24:29 | impacto: `O usuário vê um modal demorado a abrir, com dados corretos, após um breve tempo de espera.` |
| 677 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:24:29 | fonte: `[ancora-saiba-mais]` |
| 678 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:24:29 | fonte_citada: `ancora-saiba-mais` |
| 679 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:24:29 | quatro_linhas_presentes: confere |
| 680 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:24:29 | rotulo_no_conjunto: confere |
| 681 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:24:29 | fonte_existe_na_biblioteca: confere |
| 682 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:24:29 | fonte_estava_no_contexto: confere |
| 683 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:24:29 | campo_existe_no_caso: nao_se_aplica |
| 684 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:24:29 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 685 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:24:29 | notas_nos_verbetes_citados: informativo |
| 686 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:24:29 | impacto: nao_verificavel |
| 687 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:24:29 | fonte_formato_valido: confere |
| 688 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:24:29 | fonte_contem_termo_da_causa: nao_confere |
| 689 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:24:29 | diagnostico: escolha tempo_de_resposta_excedido; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 689, decisão `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido.
  - Evidência: evento 669 (verbete_entregue: `entidade-produto`, `ancora-saiba-mais`, `contrato-produto`); evento 673 (resposta); evento 678 (verbete_citado: `ancora-saiba-mais`).
  - Usou: `entidade-produto`, `ancora-saiba-mais`, `contrato-produto`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 668 a 689 da trilha; hash dos eventos deste caso: `08fa9d48a150a287`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-3`

Caso `relatorio-3` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-3`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (668 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (668 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3593 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (25,86), `ancora-saiba-mais` (25,37) e `contrato-produto` (24,97) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; `ancora-saiba-mais` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estado_da_tela_divergente` (21,66), `pagina-produtos-api` (20,97), `colecao_no_lugar_de_objeto` (20,82), `tempo_de_resposta_excedido` (16,07) e `usuario-e-login` (15,52) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 58 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `contrato-produto`, e o primeiro de fora, `estado_da_tela_divergente`, só o texto do caso já punha o primeiro à frente (21,97 contra 21,66), e os reforços em código levaram a diferença a 3,31 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 25,86: 22,86 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `ancora-saiba-mais` | posição 2, pontuação 25,37: 25,37 pelas palavras do caso, sem reforço | sim |
| `contrato-produto` | posição 3, pontuação 24,97: 21,97 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estado_da_tela_divergente` | posição 4, pontuação 21,66: 21,66 pelas palavras do caso, sem reforço |  |
| `pagina-produtos-api` | posição 5, pontuação 20,97: 18,97 pelas palavras do caso, mais 2,0 por rota |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 20,82: 17,82 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tempo_de_resposta_excedido` | posição 7, pontuação 16,07: 15,07 pelas palavras do caso, mais 1,0 por status |  |
| `usuario-e-login` | posição 8, pontuação 15,52: 15,52 pelas palavras do caso, sem reforço |  |

## Decisão 3: a causa

Escolha: `tempo_de_resposta_excedido` (Tempo de resposta excedido); segunda: `tipo_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `tempo_de_resposta_excedido` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,115 contra 0,832 da escolhida; verbetes entregues que a sustentam: `entidade-produto` e `contrato-produto` (observado).
- As outras 11 alternativas lidas na resposta somam probabilidade 0,055; as maiores: `colecao_no_lugar_de_objeto` (0,015), `resposta_truncada` (0,015) e `campo_ausente` (0,008) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,832, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/7`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `ancora-saiba-mais` (declarado).
- Verbete citado `ancora-saiba-mais`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), não traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Leitura do verbete `ancora-saiba-mais` (Link "Saiba Mais..." abre produto vazio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/defeitos_conhecidos/ancora-saiba-mais.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/defeitos_conhecidos/ancora-saiba-mais.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida tempo_de_resposta_excedido (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 5 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `tempo_de_resposta_excedido` | 0,832 | nenhum | sim |
| `tipo_divergente` | 0,115 | `entidade-produto` e `contrato-produto` |  |
| `colecao_no_lugar_de_objeto` | 0,015 | `contrato-produto` |  |
| `resposta_truncada` | 0,015 | nenhum |  |
| `campo_ausente` | 0,008 | `contrato-produto` |  |
| `campo_renomeado` | 0,008 | `contrato-produto` |  |
| `formato_de_data_divergente` | 0,005 | nenhum |  |
| `valor_fora_do_dominio` | 0,002 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |
| `estado_da_tela_divergente` | 0,000 | `ancora-saiba-mais` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um modal demorado a abrir, com dados corretos, após um breve tempo de espera.
> FONTE: [ancora-saiba-mais]

Resposta inteira:

```text
CAUSA_RAIZ: tempo_de_resposta_excedido
CAMPO: nenhum
IMPACTO: O usuário vê um modal demorado a abrir, com dados corretos, após um breve tempo de espera.
FONTE: [ancora-saiba-mais]
```

## Rastro

Gerado dos eventos 668 a 689 da trilha; hash dos eventos deste caso: `08fa9d48a150a287` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-3.md`.
