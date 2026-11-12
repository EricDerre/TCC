<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Limite de requisições (429) em `GET /api/produtos`

Caso `run-22` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/run-22`: o caso `run-22` na corrida `fase4_ineditos`; eventos 595 a 616 da trilha `trilha_ineditos.jsonl`, hash dos eventos `3a4fd6a256130d34` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Limite de requisições (429) em `GET /api/produtos`

## 3. Data, organização e autor

Observado em 06/11/2026 14:20:38 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `run-22`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 429 (a API barrou por excesso de requisições).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"detail": "limite de requisições excedido"}
```

4. Sintoma observado (texto do caso):

> A pagina Produtos (API) abre sem nenhum cartao; a linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI: HTTP 429'.

5. Observação adicional (texto do caso):

> A resposta traz o cabecalho Retry-After: 60.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids run-22`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A pagina Produtos (API) abre sem nenhum cartao; a linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI: HTTP 429'. |

Corpo recebido, como veio no caso:

```text
{"detail": "limite de requisições excedido"}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 5 (tempo e estado); nível 1 (fácil). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `limite_de_requisicoes` (Limite de requisições (429); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/limite_de_requisicoes.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/limite_de_requisicoes.md`).
- Verbetes entregues pela busca e não citados: `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`); `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`).
- Caso escrito: `run-22` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/run-22` em `trilha_ineditos.jsonl`, eventos 595 a 616, hash dos eventos `3a4fd6a256130d34`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids run-22`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `limite_de_requisicoes` (Limite de requisições (429)). Campo: nenhum apontado. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,64 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `A página Produtos fica vazia, e a linha de status indica um erro de carregamento devido ao excesso de requisições.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu limite_de_requisicoes porque os verbetes limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,64); trate como hipótese e confira o caso antes de agir.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 429

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "limite de requisições excedido"}

SINTOMA OBSERVADO: A pagina Produtos (API) abre sem nenhum cartao; a linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI: HTTP 429'.

OBSERVAÇÃO ADICIONAL: A resposta traz o cabecalho Retry-After: 60.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> limite_de_requisicoes e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,64 contra 0,00; verbete(s) na evidência: limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `limite_de_requisicoes` (Limite de requisições (429)) | 0,64 | sim |
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[limite_de_requisicoes]`; verbetes citados: `limite_de_requisicoes` (Limite de requisições (429); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/limite_de_requisicoes.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/limite_de_requisicoes.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `limite_de_requisicoes` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `limite_de_requisicoes` | confere | contexto: `limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `limite_de_requisicoes` | confere | verbetes: `limite_de_requisicoes` |
| A linha FONTE só tem identificadores, no formato pedido | `[limite_de_requisicoes]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["limite_de_requisicoes"]} |
| O verbete citado fala da causa respondida | `limite_de_requisicoes` | confere | {"termo": "limite_de_requisicoes"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids run-22`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 595 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:20:38 | caso run-22 |
| 596 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:20:38 | 3 de 39 verbetes entregues |
| 598 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:20:38 | diagnostico: 3888 caracteres; verbetes limite_de_requisicoes, contagem_inconsistente, estrutura_aninhada_divergente |
| 600 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:20:38 | diagnostico: 76,9 s |
| 601 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:20:38 | causa_raiz: `limite_de_requisicoes` |
| 602 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:20:38 | campo: `nenhum` |
| 603 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:20:38 | impacto: `A página Produtos fica vazia, e a linha de status indica um erro de carregamento devido ao excesso de requisições.` |
| 604 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:20:38 | fonte: `[limite_de_requisicoes]` |
| 605 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:20:38 | fonte_citada: `limite_de_requisicoes` |
| 606 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | quatro_linhas_presentes: confere |
| 607 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | rotulo_no_conjunto: confere |
| 608 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | fonte_existe_na_biblioteca: confere |
| 609 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | fonte_estava_no_contexto: confere |
| 610 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | campo_existe_no_caso: nao_se_aplica |
| 611 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 612 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | notas_nos_verbetes_citados: informativo |
| 613 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | impacto: nao_verificavel |
| 614 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | fonte_formato_valido: confere |
| 615 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:20:38 | fonte_contem_termo_da_causa: confere |
| 616 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:20:38 | diagnostico: escolha limite_de_requisicoes; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 616, decisão `diagnostico`: escolha `limite_de_requisicoes`; resultado rotulo_emitido.
  - Evidência: evento 596 (verbete_entregue: `limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente`); evento 600 (resposta); evento 605 (verbete_citado: `limite_de_requisicoes`).
  - Usou: `limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 595 a 616 da trilha; hash dos eventos deste caso: `3a4fd6a256130d34`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
