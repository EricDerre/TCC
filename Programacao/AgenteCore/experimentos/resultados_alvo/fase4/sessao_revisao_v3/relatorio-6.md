<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 6 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Estrutura aninhada divergente em `GET /api/produtos`, campo `tipo`

Caso `relatorio-6` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-6`: o caso `relatorio-6` na corrida `fase4_ineditos`; eventos 199 a 224 da trilha `trilha_ineditos.jsonl`, hash dos eventos `86021fefb902713d` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Estrutura aninhada divergente em `GET /api/produtos`, campo `tipo`

## 3. Data, organização e autor

Observado em 06/11/2026 14:01:29 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-6`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]
```

4. Sintoma observado (texto do caso):

> Sob o nome de cada produto, a linha da categoria mostra o texto {"valor":"Carnes","moeda":"BRL"} em vez de apenas Carnes. O resto de cada cartao esta normal.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Sob o nome de cada produto, a linha da categoria mostra o texto {"valor":"Carnes","moeda":"BRL"} em vez de apenas Carnes. O resto de cada cartao esta normal. |

Corpo recebido, como veio no caso:

```text
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`).
- Caso escrito: `relatorio-6` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-6` em `trilha_ineditos.jsonl`, eventos 199 a 224, hash dos eventos `86021fefb902713d`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `estrutura_aninhada_divergente` (Estrutura aninhada divergente). Campo: `tipo`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,80 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê a categoria com o formato completo {"valor":"Carnes","moeda":"BRL"} em vez de apenas "Carnes".`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu estrutura_aninhada_divergente no campo tipo porque os verbetes contrato-produto, entidade-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,09. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,80); trate como hipótese e confira o campo tipo antes de agir.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]

SINTOMA OBSERVADO: Sob o nome de cada produto, a linha da categoria mostra o texto {"valor":"Carnes","moeda":"BRL"} em vez de apenas Carnes. O resto de cada cartao esta normal.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> estrutura_aninhada_divergente e não campo_ausente: a escolha tem probabilidade 0,80 contra 0,09; verbete(s) na evidência: contrato-produto, entidade-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,80 | sim |
| `campo_ausente` (Campo ausente) | 0,09 |  |
| `campo_renomeado` (Campo renomeado) | 0,09 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,08 |  |
| `tipo_divergente` (Tipo divergente) | 0,02 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto] [contrato-produto]`; verbetes citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `estrutura_aninhada_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente` |
| A linha FONTE só tem identificadores, no formato pedido | `[entidade-produto] [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["entidade-produto", "contrato-produto"]} |
| O verbete citado fala da causa respondida | `entidade-produto` | não confere | {"termo": "estrutura_aninhada_divergente"} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "estrutura_aninhada_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 199 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:01:29 | caso relatorio-6 |
| 200 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:01:29 | 3 de 39 verbetes entregues |
| 202 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:01:29 | diagnostico: 3953 caracteres; verbetes contrato-produto, entidade-produto, estrutura_aninhada_divergente |
| 204 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:01:29 | diagnostico: 72,7 s |
| 205 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:01:29 | causa_raiz: `estrutura_aninhada_divergente` |
| 206 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:01:29 | campo: `tipo` |
| 207 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:01:29 | impacto: `O usuário vê a categoria com o formato completo {"valor":"Carnes","moeda":"BRL"} em vez de apenas "Carnes".` |
| 208 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:01:29 | fonte: `[entidade-produto] [contrato-produto]` |
| 209 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:01:29 | fonte_citada: `entidade-produto` |
| 210 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T14:01:29 | fonte_citada: `contrato-produto` |
| 211 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | quatro_linhas_presentes: confere |
| 212 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | rotulo_no_conjunto: confere |
| 213 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_existe_na_biblioteca: confere |
| 214 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_existe_na_biblioteca: confere |
| 215 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_estava_no_contexto: confere |
| 216 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_estava_no_contexto: confere |
| 217 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | campo_existe_no_caso: confere |
| 218 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 219 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | notas_nos_verbetes_citados: informativo |
| 220 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | impacto: nao_verificavel |
| 221 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_formato_valido: confere |
| 222 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_contem_termo_da_causa: nao_confere |
| 223 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_contem_termo_da_causa: nao_confere |
| 224 | 24 | decisao | programa | ao_vivo | 2026-11-06T14:01:29 | diagnostico: escolha estrutura_aninhada_divergente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 224, decisão `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido.
  - Evidência: evento 200 (verbete_entregue: `contrato-produto`, `entidade-produto`, `estrutura_aninhada_divergente`); evento 204 (resposta); evento 209 (verbete_citado: `entidade-produto`); evento 210 (verbete_citado: `contrato-produto`).
  - Usou: `contrato-produto`, `entidade-produto`, `estrutura_aninhada_divergente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 199 a 224 da trilha; hash dos eventos deste caso: `86021fefb902713d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-6`

Caso `relatorio-6` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-6`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança baixa.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (778 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (778 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3953 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-produto` (58,66), `entidade-produto` (55,50) e `estrutura_aninhada_divergente` (44,68) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto`, `entidade-produto` e `estrutura_aninhada_divergente`; o da entidade, em `contrato-produto`, `entidade-produto` e `estrutura_aninhada_divergente` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `colecao_no_lugar_de_objeto` (40,38), `chave_de_juncao_errada` (38,18), `campo_renomeado` (37,75), `nulo_inesperado` (37,15) e `tipo_divergente` (32,56) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos`, entidade `Produto`, status 200 e 72 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `estrutura_aninhada_divergente`, e o primeiro de fora, `colecao_no_lugar_de_objeto`, só o texto do caso já punha o primeiro à frente (41,68 contra 37,38), e os reforços em código levaram a diferença a 4,30 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-produto` | posição 1, pontuação 58,66: 55,66 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `entidade-produto` | posição 2, pontuação 55,50: 52,50 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `estrutura_aninhada_divergente` | posição 3, pontuação 44,68: 41,68 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `colecao_no_lugar_de_objeto` | posição 4, pontuação 40,38: 37,38 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 5, pontuação 38,18: 36,18 pelas palavras do caso, mais 2,0 por rota |  |
| `campo_renomeado` | posição 6, pontuação 37,75: 34,75 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `nulo_inesperado` | posição 7, pontuação 37,15: 35,15 pelas palavras do caso, mais 2,0 por rota |  |
| `tipo_divergente` | posição 8, pontuação 32,56: 29,56 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |

## Decisão 3: a causa

Escolha: `estrutura_aninhada_divergente` (Estrutura aninhada divergente); segunda: `campo_ausente`; confiança baixa.

- A linha CAUSA_RAIZ da resposta diz `estrutura_aninhada_divergente` (declarado).
- O modelo apontou o campo `tipo` (declarado).
- `tipo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `campo_ausente` (Campo ausente), ficou com probabilidade 0,092 contra 0,797 da escolhida; verbetes entregues que a sustentam: `contrato-produto` (observado).
- As outras 9 alternativas lidas na resposta somam probabilidade 0,199; as maiores: `campo_renomeado` (0,092), `chave_de_juncao_errada` (0,083) e `tipo_divergente` (0,024) (observado).
- Confiança baixa: a probabilidade lida na causa respondida foi 0,797, e a faixa baixa vai até 0,832 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 27 casos que caíram na faixa baixa, o agente acertou a causa em 12 de 27: 44,4% (observado).
- Gatilhos de revisão humana: probabilidade baixa disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `entidade-produto` e `contrato-produto` (declarado).
- Os 2 verbetes citados (`entidade-produto` e `contrato-produto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `estrutura_aninhada_divergente` (conferido).
- Camada de leitura de cada verbete citado: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 9 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `estrutura_aninhada_divergente` | 0,797 | `estrutura_aninhada_divergente` | sim |
| `campo_ausente` | 0,092 | `contrato-produto` |  |
| `campo_renomeado` | 0,092 | `contrato-produto` e `estrutura_aninhada_divergente` |  |
| `chave_de_juncao_errada` | 0,083 | `entidade-produto` |  |
| `tipo_divergente` | 0,024 | `contrato-produto` e `entidade-produto` |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `colecao_no_lugar_de_objeto` | 0,000 | `contrato-produto` e `estrutura_aninhada_divergente` |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê a categoria com o formato completo {"valor":"Carnes","moeda":"BRL"} em vez de apenas "Carnes".
> FONTE: [entidade-produto] [contrato-produto]

Resposta inteira:

```text
CAUSA_RAIZ: estrutura_aninhada_divergente
CAMPO: tipo
IMPACTO: O usuário vê a categoria com o formato completo {"valor":"Carnes","moeda":"BRL"} em vez de apenas "Carnes".
FONTE: [entidade-produto] [contrato-produto]
```

## Rastro

Gerado dos eventos 199 a 224 da trilha; hash dos eventos deste caso: `86021fefb902713d` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-6.md`.
