<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Chave de junção errada em `GET /api/produtos`, campo `tipo`

Caso `tra-20` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/tra-20@fixture`: o caso `tra-20` na corrida `fase4_tela_v4`; eventos 2003 a 2024 da trilha `trilha_tela.jsonl`, hash dos eventos `b38bacc68d54d8f3` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Chave de junção errada em `GET /api/produtos`, campo `tipo`

## 3. Data, organização e autor

Observado em 06/11/2026 11:04:42 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `tra-20`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 4 (tradução: o mapeamento entre as camadas está errado); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Sobremesas", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Sobremesas", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]
```

4. Sintoma observado (texto do caso):

> Fraldinha e Costelona (os dois cortes de carne) aparecem na categoria Sobremesas; os demais produtos de carne da listagem continuam certos em Carnes.

5. Observação adicional (texto do caso):

> tbprodutos.id_tipo_produto de id 3 e id 4 aponta pra 1 (Carnes) no banco; so esses dois produtos vem errados na resposta, o que sugere troca pontual de id_tipo_produto pra 4 (Sobremesas) nesses dois registros, nao um bug geral de juncao.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-20 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Fraldinha e Costelona (os dois cortes de carne) aparecem na categoria Sobremesas; os demais produtos de carne da listagem continuam certos em Carnes. |

Corpo recebido, como veio no caso:

```text
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Sobremesas", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Sobremesas", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 4 (tradução: o mapeamento entre as camadas está errado); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 4 (tradução); nível 3 (difícil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `chave_de_juncao_errada` (Chave de junção errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/chave_de_juncao_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/chave_de_juncao_errada.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `tra-20` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/tra-20@fixture` em `trilha_tela.jsonl`, eventos 2003 a 2024, hash dos eventos `b38bacc68d54d8f3`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/tra-20@fixture.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-20 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `chave_de_juncao_errada` (Chave de junção errada). Campo: `tipo`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `Os produtos Fraldinha e Costelona, que são cortes de carne, aparecem incorretamente na categoria Sobremesas na interface web.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu chave_de_juncao_errada no campo tipo porque os verbetes entidade-produto, contrato-produto, chave_de_juncao_errada estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Sobremesas", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Sobremesas", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]

SINTOMA OBSERVADO: Fraldinha e Costelona (os dois cortes de carne) aparecem na categoria Sobremesas; os demais produtos de carne da listagem continuam certos em Carnes.

OBSERVAÇÃO ADICIONAL: tbprodutos.id_tipo_produto de id 3 e id 4 aponta pra 1 (Carnes) no banco; so esses dois produtos vem errados na resposta, o que sugere troca pontual de id_tipo_produto pra 4 (Sobremesas) nesses dois registros, nao um bug geral de juncao.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> chave_de_juncao_errada e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, chave_de_juncao_errada

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `chave_de_juncao_errada` (Chave de junção errada) | 1,00 | sim |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `registro_duplicado` (Registro duplicado) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[chave_de_juncao_errada]`; verbetes citados: `chave_de_juncao_errada` (Chave de junção errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/chave_de_juncao_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/chave_de_juncao_errada.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `chave_de_juncao_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `chave_de_juncao_errada` | confere | contexto: `entidade-produto`, `contrato-produto`, `chave_de_juncao_errada` |
| Algum verbete do contexto trata da causa respondida | `chave_de_juncao_errada` | confere | verbetes: `entidade-produto`, `chave_de_juncao_errada` |
| A linha FONTE só tem identificadores, no formato pedido | `[chave_de_juncao_errada]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["chave_de_juncao_errada"]} |
| O verbete citado fala da causa respondida | `chave_de_juncao_errada` | confere | {"termo": "chave_de_juncao_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-20 --k 3`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2003 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:04:42 | caso tra-20 |
| 2004 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:04:42 | 3 de 39 verbetes entregues |
| 2006 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:04:42 | diagnostico: 4504 caracteres; verbetes entidade-produto, contrato-produto, chave_de_juncao_errada |
| 2008 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:04:42 | diagnostico: 71,2 s |
| 2009 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:42 | causa_raiz: `chave_de_juncao_errada` |
| 2010 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:42 | campo: `tipo` |
| 2011 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:42 | impacto: `Os produtos Fraldinha e Costelona, que são cortes de carne, aparecem incorretamente na categoria Sobremesas na interface web.` |
| 2012 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:42 | fonte: `[chave_de_juncao_errada]` |
| 2013 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:42 | fonte_citada: `chave_de_juncao_errada` |
| 2014 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | quatro_linhas_presentes: confere |
| 2015 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | rotulo_no_conjunto: confere |
| 2016 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | fonte_existe_na_biblioteca: confere |
| 2017 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | fonte_estava_no_contexto: confere |
| 2018 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | campo_existe_no_caso: confere |
| 2019 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2020 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | notas_nos_verbetes_citados: informativo |
| 2021 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | impacto: nao_verificavel |
| 2022 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | fonte_formato_valido: confere |
| 2023 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | fonte_contem_termo_da_causa: confere |
| 2024 | 20 | decisao | programa | ao_vivo | 2026-11-06T11:04:42 | diagnostico: escolha chave_de_juncao_errada; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 2024, decisão `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido.
  - Evidência: evento 2004 (verbete_entregue: `entidade-produto`, `contrato-produto`, `chave_de_juncao_errada`); evento 2008 (resposta); evento 2013 (verbete_citado: `chave_de_juncao_errada`).
  - Usou: `entidade-produto`, `contrato-produto`, `chave_de_juncao_errada`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2003 a 2024 da trilha; hash dos eventos deste caso: `b38bacc68d54d8f3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
