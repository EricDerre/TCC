<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Contagem inconsistente em `GET /api/produtos?pagina=1`, campo `total`

Caso `tra-4` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/tra-4@fixture`: o caso `tra-4` na corrida `fase4_tela_v4`; eventos 410 a 431 da trilha `trilha_tela.jsonl`, hash dos eventos `02310be04b96a43e` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Contagem inconsistente em `GET /api/produtos?pagina=1`, campo `total`

## 3. Data, organização e autor

Observado em 06/11/2026 10:10:02 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos?pagina=1` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `tra-4`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 4 (tradução: o mapeamento entre as camadas está errado); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos?pagina=1`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano | envelope: {total: inteiro, itens: lista}`.
3. Corpo da resposta:

```text
{"total": 14, "itens": [{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]}
```

4. Sintoma observado (texto do caso):

> A tela informa '14 produtos encontrados' mas exibe apenas 1 cartao.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-4 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano | envelope: {total: inteiro, itens: lista}`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos?pagina=1` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A tela informa '14 produtos encontrados' mas exibe apenas 1 cartao. |

Corpo recebido, como veio no caso:

```text
{"total": 14, "itens": [{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 4 (tradução: o mapeamento entre as camadas está errado); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 4 (tradução); nível 3 (difícil). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`).
- Caso escrito: `tra-4` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/tra-4@fixture` em `trilha_tela.jsonl`, eventos 410 a 431, hash dos eventos `02310be04b96a43e`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/tra-4@fixture.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-4 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `contagem_inconsistente` (Contagem inconsistente). Campo: `total`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,97 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `A tela informa '14 produtos encontrados' mas exibe apenas 1 cartão, devido à contagem inconsistente entre o total informado e o número de itens retornados.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu contagem_inconsistente no campo total porque os verbetes contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos?pagina=1

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano | envelope: {total: inteiro, itens: lista}

CORPO DA RESPOSTA:
{"total": 14, "itens": [{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]}

SINTOMA OBSERVADO: A tela informa '14 produtos encontrados' mas exibe apenas 1 cartao.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> contagem_inconsistente e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,97 contra 0,00; verbete(s) na evidência: contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `contagem_inconsistente` (Contagem inconsistente) | 0,97 | sim |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `entidade-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| A linha FONTE só tem identificadores, no formato pedido | `[contagem_inconsistente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contagem_inconsistente"]} |
| O verbete citado fala da causa respondida | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `total` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-4 --k 3`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 410 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:10:02 | caso tra-4 |
| 411 | 2 | candidatos | programa | ao_vivo | 2026-11-06T10:10:02 | 3 de 39 verbetes entregues |
| 413 | 3 | prompt | programa | ao_vivo | 2026-11-06T10:10:02 | diagnostico: 3720 caracteres; verbetes contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente |
| 415 | 4 | inferencia | programa | ao_vivo | 2026-11-06T10:10:02 | diagnostico: 77,7 s |
| 416 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T10:10:02 | causa_raiz: `contagem_inconsistente` |
| 417 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T10:10:02 | campo: `total` |
| 418 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T10:10:02 | impacto: `A tela informa '14 produtos encontrados' mas exibe apenas 1 cartão, devido à contagem inconsistente entre o total informado e o número de itens retornados.` |
| 419 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T10:10:02 | fonte: `[contagem_inconsistente]` |
| 420 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T10:10:02 | fonte_citada: `contagem_inconsistente` |
| 421 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:10:02 | quatro_linhas_presentes: confere |
| 422 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:10:02 | rotulo_no_conjunto: confere |
| 423 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:10:02 | fonte_existe_na_biblioteca: confere |
| 424 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:10:02 | fonte_estava_no_contexto: confere |
| 425 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T10:10:02 | campo_existe_no_caso: confere |
| 426 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T10:10:02 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 427 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T10:10:02 | notas_nos_verbetes_citados: informativo |
| 428 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:10:02 | impacto: nao_verificavel |
| 429 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:10:02 | fonte_formato_valido: confere |
| 430 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:10:02 | fonte_contem_termo_da_causa: confere |
| 431 | 20 | decisao | programa | ao_vivo | 2026-11-06T10:10:02 | diagnostico: escolha contagem_inconsistente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 431, decisão `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido.
  - Evidência: evento 411 (verbete_entregue: `contagem_inconsistente`, `entidade-produto`, `estrutura_aninhada_divergente`); evento 415 (resposta); evento 420 (verbete_citado: `contagem_inconsistente`).
  - Usou: `contagem_inconsistente`, `entidade-produto`, `estrutura_aninhada_divergente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 410 a 431 da trilha; hash dos eventos deste caso: `02310be04b96a43e`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
