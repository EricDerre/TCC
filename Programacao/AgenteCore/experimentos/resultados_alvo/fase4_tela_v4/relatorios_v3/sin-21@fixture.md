<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Estrutura aninhada divergente em `GET /api/produtos`, campo `tipo`

Caso `sin-21` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/sin-21@fixture`: o caso `sin-21` na corrida `fase4_tela_v4`; eventos 1583 a 1604 da trilha `trilha_tela.jsonl`, hash dos eventos `c662158d6c4e2115` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Estrutura aninhada divergente em `GET /api/produtos`, campo `tipo`

## 3. Data, organização e autor

Observado em 06/11/2026 10:52:32 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `sin-21`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 2 (sintática: a forma da resposta não é a esperada); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "{'id': 1, 'nome': 'Carnes'}", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]
```

4. Sintoma observado (texto do caso):

> A categoria do produto aparece como o texto literal {'id': 1, 'nome': 'Carnes'} no card (aspas simples, no estilo de repr do Python), em vez de 'Carnes': diferente de um objeto de verdade, que apareceria como [object Object].

5. Observação adicional (texto do caso):

> tipo e uma STRING cujo conteudo por acaso parece um dicionario serializado errado (aspas simples); nao e um objeto JSON aninhado de verdade, por isso o card nao mostra [object Object].

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-21 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A categoria do produto aparece como o texto literal {'id': 1, 'nome': 'Carnes'} no card (aspas simples, no estilo de repr do Python), em vez de 'Carnes': diferente de um objeto de verdade, que apareceria como [object Object]. |

Corpo recebido, como veio no caso:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "{'id': 1, 'nome': 'Carnes'}", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 2 (sintática: a forma da resposta não é a esperada); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 2 (sintática); nível 3 (difícil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `pagina-produtos-api` (Aba "Produtos (API)", a fronteira JSON; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/pagina-produtos-api.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/pagina-produtos-api.md`).
- Caso escrito: `sin-21` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/sin-21@fixture` em `trilha_tela.jsonl`, eventos 1583 a 1604, hash dos eventos `c662158d6c4e2115`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/sin-21@fixture.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-21 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `estrutura_aninhada_divergente` (Estrutura aninhada divergente). Campo: `tipo`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê a categoria do produto como o texto literal {'id': 1, 'nome': 'Carnes'} em vez de 'Carnes'.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu estrutura_aninhada_divergente no campo tipo porque os verbetes estrutura_aninhada_divergente, entidade-produto, pagina-produtos-api estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "{'id': 1, 'nome': 'Carnes'}", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: A categoria do produto aparece como o texto literal {'id': 1, 'nome': 'Carnes'} no card (aspas simples, no estilo de repr do Python), em vez de 'Carnes' — diferente de um objeto de verdade, que apareceria como [object Object].

OBSERVAÇÃO ADICIONAL: tipo e uma STRING cujo conteudo por acaso parece um dicionario serializado errado (aspas simples); nao e um objeto JSON aninhado de verdade, por isso o card nao mostra [object Object].
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> estrutura_aninhada_divergente e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: estrutura_aninhada_divergente, entidade-produto, pagina-produtos-api

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 1,00 | sim |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[estrutura_aninhada_divergente]`; verbetes citados: `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `estrutura_aninhada_divergente`, `entidade-produto`, `pagina-produtos-api` |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente` |
| A linha FONTE só tem identificadores, no formato pedido | `[estrutura_aninhada_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["estrutura_aninhada_divergente"]} |
| O verbete citado fala da causa respondida | `estrutura_aninhada_divergente` | confere | {"termo": "estrutura_aninhada_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-21 --k 3`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1583 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:52:32 | caso sin-21 |
| 1584 | 2 | candidatos | programa | ao_vivo | 2026-11-06T10:52:32 | 3 de 39 verbetes entregues |
| 1586 | 3 | prompt | programa | ao_vivo | 2026-11-06T10:52:32 | diagnostico: 3879 caracteres; verbetes estrutura_aninhada_divergente, entidade-produto, pagina-produtos-api |
| 1588 | 4 | inferencia | programa | ao_vivo | 2026-11-06T10:52:32 | diagnostico: 69,2 s |
| 1589 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T10:52:32 | causa_raiz: `estrutura_aninhada_divergente` |
| 1590 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T10:52:32 | campo: `tipo` |
| 1591 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T10:52:32 | impacto: `O usuário vê a categoria do produto como o texto literal {'id': 1, 'nome': 'Carnes'} em vez de 'Carnes'.` |
| 1592 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T10:52:32 | fonte: `[estrutura_aninhada_divergente]` |
| 1593 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T10:52:32 | fonte_citada: `estrutura_aninhada_divergente` |
| 1594 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:52:32 | quatro_linhas_presentes: confere |
| 1595 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:52:32 | rotulo_no_conjunto: confere |
| 1596 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:52:32 | fonte_existe_na_biblioteca: confere |
| 1597 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:52:32 | fonte_estava_no_contexto: confere |
| 1598 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T10:52:32 | campo_existe_no_caso: confere |
| 1599 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T10:52:32 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1600 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T10:52:32 | notas_nos_verbetes_citados: informativo |
| 1601 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:52:32 | impacto: nao_verificavel |
| 1602 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:52:32 | fonte_formato_valido: confere |
| 1603 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:52:32 | fonte_contem_termo_da_causa: confere |
| 1604 | 20 | decisao | programa | ao_vivo | 2026-11-06T10:52:32 | diagnostico: escolha estrutura_aninhada_divergente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 1604, decisão `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido.
  - Evidência: evento 1584 (verbete_entregue: `estrutura_aninhada_divergente`, `entidade-produto`, `pagina-produtos-api`); evento 1588 (resposta); evento 1593 (verbete_citado: `estrutura_aninhada_divergente`).
  - Usou: `estrutura_aninhada_divergente`, `entidade-produto`, `pagina-produtos-api`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1583 a 1604 da trilha; hash dos eventos deste caso: `c662158d6c4e2115`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
