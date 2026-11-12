<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Recurso inexistente (404 e vizinhos) em `GET /api/produtos/5`, campo `id`

Caso `run-23` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/run-23`: o caso `run-23` na corrida `fase4_ineditos`; eventos 618 a 639 da trilha `trilha_ineditos.jsonl`, hash dos eventos `43860baed69d86cb` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Recurso inexistente (404 e vizinhos) em `GET /api/produtos/5`, campo `id`

## 3. Data, organização e autor

Observado em 06/11/2026 14:21:59 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/5` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `run-23`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids run-23`

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

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 5 (tempo e estado); nível 1 (fácil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `recurso_inexistente` (Recurso inexistente (404 e vizinhos); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/recurso_inexistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/recurso_inexistente.md`).
- Verbetes entregues pela busca e não citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `mensagens-de-erro-do-codigo` (Índice de mensagens literais do código; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/mensagens-de-erro-do-codigo.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/mensagens-de-erro-do-codigo.md`).
- Caso escrito: `run-23` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/run-23` em `trilha_ineditos.jsonl`, eventos 618 a 639, hash dos eventos `43860baed69d86cb`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids run-23`.
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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids run-23`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 618 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:21:59 | caso run-23 |
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
