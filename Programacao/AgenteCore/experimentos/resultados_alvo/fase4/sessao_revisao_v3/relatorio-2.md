<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 2 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Nulo inesperado em `GET /api/produtos`, campo `preco`

Caso `relatorio-2` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-2`: o caso `relatorio-2` na corrida `fase4_ineditos`; eventos 299 a 320 da trilha `trilha_ineditos.jsonl`, hash dos eventos `66f4ad34b6aaeda1` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Nulo inesperado em `GET /api/produtos`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 14:06:16 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-2`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": null, "imagem": "maminha.jpg", "destaque": false}, {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": null, "imagem": "cupim.jpg", "destaque": true}]
```

4. Sintoma observado (texto do caso):

> Todos os botoes de preco da grade mostram 'R$ 0,00'. Os nomes, as categorias e as fotos estao normais.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Todos os botoes de preco da grade mostram 'R$ 0,00'. Os nomes, as categorias e as fotos estao normais. |

Corpo recebido, como veio no caso:

```text
[{"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": null, "imagem": "maminha.jpg", "destaque": false}, {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": null, "imagem": "cupim.jpg", "destaque": true}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`).
- Verbetes entregues pela busca e não citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `relatorio-2` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-2` em `trilha_ineditos.jsonl`, eventos 299 a 320, hash dos eventos `66f4ad34b6aaeda1`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `nulo_inesperado` (Nulo inesperado). Campo: `preco`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O preço dos produtos não é exibido corretamente na interface, mostrando 'R$ 0,00' para todos os itens, pois os preços retornados da API são nulos.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu nulo_inesperado no campo preco porque os verbetes nulo_inesperado, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": null, "imagem": "maminha.jpg", "destaque": false}, {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": null, "imagem": "cupim.jpg", "destaque": true}]

SINTOMA OBSERVADO: Todos os botoes de preco da grade mostram 'R$ 0,00'. Os nomes, as categorias e as fotos estao normais.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: nulo_inesperado, contrato-produto, entidade-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `nulo_inesperado` (Nulo inesperado) | 1,00 | sim |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `nulo_inesperado`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| A linha FONTE só tem identificadores, no formato pedido | `[nulo_inesperado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["nulo_inesperado"]} |
| O verbete citado fala da causa respondida | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 299 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:06:16 | caso relatorio-2 |
| 300 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:06:16 | 3 de 39 verbetes entregues |
| 302 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:06:16 | diagnostico: 3546 caracteres; verbetes nulo_inesperado, contrato-produto, entidade-produto |
| 304 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:06:16 | diagnostico: 75,6 s |
| 305 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:06:16 | causa_raiz: `nulo_inesperado` |
| 306 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:06:16 | campo: `preco` |
| 307 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:06:16 | impacto: `O preço dos produtos não é exibido corretamente na interface, mostrando 'R$ 0,00' para todos os itens, pois os preços retornados da API são nulos.` |
| 308 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:06:16 | fonte: `[nulo_inesperado]` |
| 309 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:06:16 | fonte_citada: `nulo_inesperado` |
| 310 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:06:16 | quatro_linhas_presentes: confere |
| 311 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:06:16 | rotulo_no_conjunto: confere |
| 312 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:06:16 | fonte_existe_na_biblioteca: confere |
| 313 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:06:16 | fonte_estava_no_contexto: confere |
| 314 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:06:16 | campo_existe_no_caso: confere |
| 315 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:06:16 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 316 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:06:16 | notas_nos_verbetes_citados: informativo |
| 317 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:06:16 | impacto: nao_verificavel |
| 318 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:06:16 | fonte_formato_valido: confere |
| 319 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:06:16 | fonte_contem_termo_da_causa: confere |
| 320 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:06:16 | diagnostico: escolha nulo_inesperado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 320, decisão `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido.
  - Evidência: evento 300 (verbete_entregue: `nulo_inesperado`, `contrato-produto`, `entidade-produto`); evento 304 (resposta); evento 309 (verbete_citado: `nulo_inesperado`).
  - Usou: `nulo_inesperado`, `contrato-produto`, `entidade-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 299 a 320 da trilha; hash dos eventos deste caso: `66f4ad34b6aaeda1`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-2`

Caso `relatorio-2` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-2`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (645 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (645 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3546 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `nulo_inesperado` (67,67), `contrato-produto` (54,56) e `entidade-produto` (50,25) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `nulo_inesperado`, `contrato-produto` e `entidade-produto`; o da entidade, em `contrato-produto` e `entidade-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `campo_renomeado` (23,56), `tipo_divergente` (21,84), `pagina-produtos-api` (21,73), `valor_fora_do_dominio` (21,59) e `chave_de_juncao_errada` (21,50) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 59 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `campo_renomeado`, só o texto do caso já punha o primeiro à frente (47,25 contra 20,56), e os reforços em código levaram a diferença a 26,69 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `nulo_inesperado` | posição 1, pontuação 67,67: 65,67 pelas palavras do caso, mais 2,0 por rota | sim |
| `contrato-produto` | posição 2, pontuação 54,56: 51,56 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 3, pontuação 50,25: 47,25 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_renomeado` | posição 4, pontuação 23,56: 20,56 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `tipo_divergente` | posição 5, pontuação 21,84: 18,84 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `pagina-produtos-api` | posição 6, pontuação 21,73: 19,73 pelas palavras do caso, mais 2,0 por rota |  |
| `valor_fora_do_dominio` | posição 7, pontuação 21,59: 19,59 pelas palavras do caso, mais 2,0 por rota |  |
| `chave_de_juncao_errada` | posição 8, pontuação 21,50: 19,50 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `nulo_inesperado` (Nulo inesperado); segunda: `tipo_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `nulo_inesperado` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 0,999 da escolhida; verbetes entregues que a sustentam: `contrato-produto` e `entidade-produto` (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `campo_renomeado` (0,000) e `valor_fora_do_dominio` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,999, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `nulo_inesperado` (declarado).
- Verbete citado `nulo_inesperado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `nulo_inesperado` (conferido).
- Leitura do verbete `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `nulo_inesperado` | 0,999 | `nulo_inesperado` | sim |
| `tipo_divergente` | 0,000 | `contrato-produto` e `entidade-produto` |  |
| `campo_ausente` | 0,000 | `nulo_inesperado` e `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |
| `valor_fora_do_dominio` | 0,000 | `nulo_inesperado` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O preço dos produtos não é exibido corretamente na interface, mostrando 'R$ 0,00' para todos os itens, pois os preços retornados da API são nulos.
> FONTE: [nulo_inesperado]

Resposta inteira:

```text
CAUSA_RAIZ: nulo_inesperado
CAMPO: preco
IMPACTO: O preço dos produtos não é exibido corretamente na interface, mostrando 'R$ 0,00' para todos os itens, pois os preços retornados da API são nulos.
FONTE: [nulo_inesperado]
```

## Rastro

Gerado dos eventos 299 a 320 da trilha; hash dos eventos deste caso: `66f4ad34b6aaeda1` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-2.md`.
