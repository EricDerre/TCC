<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Nulo inesperado em `GET /api/produtos/12`, campo `resumo`

Caso `semt-26` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/semt-26`: o caso `semt-26` na corrida `fase4_ineditos`; eventos 395 a 416 da trilha `trilha_ineditos.jsonl`, hash dos eventos `d4c192c507f326d8` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Nulo inesperado em `GET /api/produtos/12`, campo `resumo`

## 3. Data, organização e autor

Observado em 06/11/2026 14:11:23 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/12` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `semt-26`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/12`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"id": 12, "nome": "Queijo Coalho", "resumo": null, "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}
```

4. Sintoma observado (texto do caso):

> O cartao do Queijo Coalho na grade mostra a descricao 'Queijo coalho grelhado com mel', mas o modal aberto pelo 'Saiba Mais...' desse mesmo produto mostra '(sem descrição)'. As duas respostas chegaram com status 200.

5. Observação adicional (texto do caso):

> A listagem GET /api/produtos, feita antes do clique, trouxe este produto (id 12) com o resumo preenchido. O contrato permite resumo nulo (texto|nulo).

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids semt-26`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/12` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O cartao do Queijo Coalho na grade mostra a descricao 'Queijo coalho grelhado com mel', mas o modal aberto pelo 'Saiba Mais...' desse mesmo produto mostra '(sem descrição)'. As duas respostas chegaram com status 200. |

Corpo recebido, como veio no caso:

```text
{"id": 12, "nome": "Queijo Coalho", "resumo": null, "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 3 (semântica); nível 3 (difícil). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`).
- Verbetes entregues pela busca e não citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `semt-26` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/semt-26` em `trilha_ineditos.jsonl`, eventos 395 a 416, hash dos eventos `d4c192c507f326d8`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids semt-26`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `nulo_inesperado` (Nulo inesperado). Campo: `resumo`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,89 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê uma descrição no cardápio, mas no modal, o campo 'Saiba Mais...' está vazio.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu nulo_inesperado no campo resumo porque os verbetes contrato-produto, nulo_inesperado, entidade-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,04. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/12

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 12, "nome": "Queijo Coalho", "resumo": null, "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}

SINTOMA OBSERVADO: O cartao do Queijo Coalho na grade mostra a descricao 'Queijo coalho grelhado com mel', mas o modal aberto pelo 'Saiba Mais...' desse mesmo produto mostra '(sem descrição)'. As duas respostas chegaram com status 200.

OBSERVAÇÃO ADICIONAL: A listagem GET /api/produtos, feita antes do clique, trouxe este produto (id 12) com o resumo preenchido. O contrato permite resumo nulo (texto|nulo).
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> nulo_inesperado e não campo_ausente: a escolha tem probabilidade 0,89 contra 0,04; verbete(s) na evidência: contrato-produto, nulo_inesperado, entidade-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `nulo_inesperado` (Nulo inesperado) | 0,89 | sim |
| `campo_ausente` (Campo ausente) | 0,04 |  |
| `campo_renomeado` (Campo renomeado) | 0,04 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,04 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,01 |  |
| `tipo_divergente` (Tipo divergente) | 0,01 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `contrato-produto`, `nulo_inesperado`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| A linha FONTE só tem identificadores, no formato pedido | `[nulo_inesperado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["nulo_inesperado"]} |
| O verbete citado fala da causa respondida | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `resumo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids semt-26`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 395 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:11:23 | caso semt-26 |
| 396 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:11:23 | 3 de 39 verbetes entregues |
| 398 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:11:23 | diagnostico: 3672 caracteres; verbetes contrato-produto, nulo_inesperado, entidade-produto |
| 400 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:11:23 | diagnostico: 72,7 s |
| 401 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:11:23 | causa_raiz: `nulo_inesperado` |
| 402 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:11:23 | campo: `resumo` |
| 403 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:11:23 | impacto: `O usuário vê uma descrição no cardápio, mas no modal, o campo 'Saiba Mais...' está vazio.` |
| 404 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:11:23 | fonte: `[nulo_inesperado]` |
| 405 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:11:23 | fonte_citada: `nulo_inesperado` |
| 406 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | quatro_linhas_presentes: confere |
| 407 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | rotulo_no_conjunto: confere |
| 408 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | fonte_existe_na_biblioteca: confere |
| 409 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | fonte_estava_no_contexto: confere |
| 410 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | campo_existe_no_caso: confere |
| 411 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 412 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | notas_nos_verbetes_citados: informativo |
| 413 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | impacto: nao_verificavel |
| 414 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | fonte_formato_valido: confere |
| 415 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:11:23 | fonte_contem_termo_da_causa: confere |
| 416 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:11:23 | diagnostico: escolha nulo_inesperado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 416, decisão `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido.
  - Evidência: evento 396 (verbete_entregue: `contrato-produto`, `nulo_inesperado`, `entidade-produto`); evento 400 (resposta); evento 405 (verbete_citado: `nulo_inesperado`).
  - Usou: `contrato-produto`, `nulo_inesperado`, `entidade-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 395 a 416 da trilha; hash dos eventos deste caso: `d4c192c507f326d8`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
