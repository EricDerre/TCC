<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 24 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Campo renomeado em `GET /api/produtos/10`, campo `resumo`

Caso `relatorio-24` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-24`: o caso `relatorio-24` na corrida `fase4_ineditos`; eventos 176 a 197 da trilha `trilha_ineditos.jsonl`, hash dos eventos `0354be1bfb1f8a66` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Campo renomeado em `GET /api/produtos/10`, campo `resumo`

## 3. Data, organização e autor

Observado em 06/11/2026 14:00:14 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/10` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-24`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/10`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"id": 10, "nome": "Refrigerante", "tipo": "Bebidas", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false, "resumo_v2": "Lata 350ml, diversos sabores"}
```

4. Sintoma observado (texto do caso):

> O modal do Refrigerante abre com o titulo certo, mas o texto de descricao aparece como '(sem descrição)'.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/10` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O modal do Refrigerante abre com o titulo certo, mas o texto de descricao aparece como '(sem descrição)'. |

Corpo recebido, como veio no caso:

```text
{"id": 10, "nome": "Refrigerante", "tipo": "Bebidas", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false, "resumo_v2": "Lata 350ml, diversos sabores"}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`).
- Verbetes entregues pela busca e não citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `relatorio-24` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-24` em `trilha_ineditos.jsonl`, eventos 176 a 197, hash dos eventos `0354be1bfb1f8a66`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `campo_renomeado` (Campo renomeado). Campo: `resumo`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O campo resumo foi renomeado para resumo_v2, mas a interface espera resumo, resultando em uma descrição não exibida corretamente.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu campo_renomeado no campo resumo porque os verbetes contrato-produto, campo_renomeado, entidade-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/10

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 10, "nome": "Refrigerante", "tipo": "Bebidas", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false, "resumo_v2": "Lata 350ml, diversos sabores"}

SINTOMA OBSERVADO: O modal do Refrigerante abre com o titulo certo, mas o texto de descricao aparece como '(sem descrição)'.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> campo_renomeado e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, campo_renomeado, entidade-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `campo_renomeado` (Campo renomeado) | 1,00 | sim |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `dado_desatualizado` (Dado desatualizado (cache)) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado]`; verbetes citados: `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `contrato-produto`, `campo_renomeado`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `contrato-produto`, `campo_renomeado` |
| A linha FONTE só tem identificadores, no formato pedido | `[campo_renomeado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_renomeado"]} |
| O verbete citado fala da causa respondida | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `resumo` no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 176 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:00:14 | caso relatorio-24 |
| 177 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:00:14 | 3 de 39 verbetes entregues |
| 179 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:00:14 | diagnostico: 3626 caracteres; verbetes contrato-produto, campo_renomeado, entidade-produto |
| 181 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:00:14 | diagnostico: 70,6 s |
| 182 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:00:14 | causa_raiz: `campo_renomeado` |
| 183 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:00:14 | campo: `resumo` |
| 184 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:00:14 | impacto: `O campo resumo foi renomeado para resumo_v2, mas a interface espera resumo, resultando em uma descrição não exibida corretamente.` |
| 185 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:00:14 | fonte: `[campo_renomeado]` |
| 186 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:00:14 | fonte_citada: `campo_renomeado` |
| 187 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | quatro_linhas_presentes: confere |
| 188 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | rotulo_no_conjunto: confere |
| 189 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | fonte_existe_na_biblioteca: confere |
| 190 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | fonte_estava_no_contexto: confere |
| 191 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | campo_existe_no_caso: confere |
| 192 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 193 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | notas_nos_verbetes_citados: informativo |
| 194 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | impacto: nao_verificavel |
| 195 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | fonte_formato_valido: confere |
| 196 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | fonte_contem_termo_da_causa: confere |
| 197 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:00:14 | diagnostico: escolha campo_renomeado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 197, decisão `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido.
  - Evidência: evento 177 (verbete_entregue: `contrato-produto`, `campo_renomeado`, `entidade-produto`); evento 181 (resposta); evento 186 (verbete_citado: `campo_renomeado`).
  - Usou: `contrato-produto`, `campo_renomeado`, `entidade-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 176 a 197 da trilha; hash dos eventos deste caso: `0354be1bfb1f8a66`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-24`

Caso `relatorio-24` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-24`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança alta.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (512 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (512 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 3626 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `contrato-produto` (30,62), `campo_renomeado` (27,94) e `entidade-produto` (26,39) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto` e `entidade-produto`; o da entidade, em `contrato-produto`, `campo_renomeado` e `entidade-produto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `campo_ausente` (22,44), `tipo_divergente` (17,37), `colecao_no_lugar_de_objeto` (17,12), `chave_de_juncao_errada` (16,15) e `pagina-produtos-api` (12,62) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 40 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `campo_ausente`, só o texto do caso já punha o primeiro à frente (23,39 contra 21,44), e os reforços em código levaram a diferença a 3,95 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `contrato-produto` | posição 1, pontuação 30,62: 27,62 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_renomeado` | posição 2, pontuação 27,94: 26,94 pelas palavras do caso, mais 1,0 por entidade | sim |
| `entidade-produto` | posição 3, pontuação 26,39: 23,39 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `campo_ausente` | posição 4, pontuação 22,44: 21,44 pelas palavras do caso, mais 1,0 por entidade |  |
| `tipo_divergente` | posição 5, pontuação 17,37: 16,37 pelas palavras do caso, mais 1,0 por entidade |  |
| `colecao_no_lugar_de_objeto` | posição 6, pontuação 17,12: 14,12 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `chave_de_juncao_errada` | posição 7, pontuação 16,15: 16,15 pelas palavras do caso, sem reforço |  |
| `pagina-produtos-api` | posição 8, pontuação 12,62: 10,62 pelas palavras do caso, mais 2,0 por rota |  |

## Decisão 3: a causa

Escolha: `campo_renomeado` (Campo renomeado); segunda: `tipo_divergente`; confiança alta.

- A linha CAUSA_RAIZ da resposta diz `campo_renomeado` (declarado).
- O modelo apontou o campo `resumo` (declarado).
- `resumo` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tipo_divergente` (Tipo divergente), ficou com probabilidade 0,000 contra 0,999 da escolhida; verbetes entregues que a sustentam: `contrato-produto` e `entidade-produto` (observado).
- As outras 7 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000), `chave_de_juncao_errada` (0,000) e `resposta_truncada` (0,000) (observado).
- Confiança alta: a probabilidade lida na causa respondida foi 0,999, e a faixa alta começa em 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 37 casos que caíram na faixa alta, o agente acertou a causa em 34 de 37: 91,9% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/10`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `campo_renomeado` (declarado).
- Verbete citado `campo_renomeado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-produto` e `campo_renomeado` (conferido).
- Leitura do verbete `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 8 de 8 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `campo_renomeado` | 0,999 | `contrato-produto` e `campo_renomeado` | sim |
| `tipo_divergente` | 0,000 | `contrato-produto` e `entidade-produto` |  |
| `campo_ausente` | 0,000 | `contrato-produto` e `campo_renomeado` |  |
| `chave_de_juncao_errada` | 0,000 | `entidade-produto` |  |
| `resposta_truncada` | 0,000 | nenhum |  |
| `valor_fora_do_dominio` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |
| `dado_desatualizado` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O campo resumo foi renomeado para resumo_v2, mas a interface espera resumo, resultando em uma descrição não exibida corretamente.
> FONTE: [campo_renomeado]

Resposta inteira:

```text
CAUSA_RAIZ: campo_renomeado
CAMPO: resumo
IMPACTO: O campo resumo foi renomeado para resumo_v2, mas a interface espera resumo, resultando em uma descrição não exibida corretamente.
FONTE: [campo_renomeado]
```

## Rastro

Gerado dos eventos 176 a 197 da trilha; hash dos eventos deste caso: `0354be1bfb1f8a66` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-24.md`.
