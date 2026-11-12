<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Chave de junção errada em `GET /api/produtos`, campo `tipo`

Caso `tra-24` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/tra-24`: o caso `tra-24` na corrida `fase4_ineditos`; eventos 495 a 516 da trilha `trilha_ineditos.jsonl`, hash dos eventos `f27bc1e9d1758c80` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Chave de junção errada em `GET /api/produtos`, campo `tipo`

## 3. Data, organização e autor

Observado em 06/11/2026 14:16:08 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `tra-24`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 4 (tradução: o mapeamento entre as camadas está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}, {"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Acompanhamentos", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false}]
```

4. Sintoma observado (texto do caso):

> Na grade, o Cupim aparece com a categoria 'Bebidas' e o Refrigerante com 'Acompanhamentos'; a Agua Mineral e o Balde de Cerveja aparecem com 'Bebidas'. Os nomes, os precos e as fotos estao certos.

5. Observação adicional (texto do caso):

> O corpo mostra so os itens de id 7 a 10; a lista completa tem 14.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-24`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Na grade, o Cupim aparece com a categoria 'Bebidas' e o Refrigerante com 'Acompanhamentos'; a Agua Mineral e o Balde de Cerveja aparecem com 'Bebidas'. Os nomes, os precos e as fotos estao certos. |

Corpo recebido, como veio no caso:

```text
[{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}, {"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Acompanhamentos", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 4 (tradução: o mapeamento entre as camadas está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 4 (tradução); nível 2 (médio). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `chave_de_juncao_errada` (Chave de junção errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/chave_de_juncao_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/chave_de_juncao_errada.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `tra-24` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/tra-24` em `trilha_ineditos.jsonl`, eventos 495 a 516, hash dos eventos `f27bc1e9d1758c80`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-24`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `chave_de_juncao_errada` (Chave de junção errada). Campo: `tipo`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,92 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `Os produtos são exibidos com categorias incorretas, misturando itens de diferentes tipos.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu chave_de_juncao_errada no campo tipo porque os verbetes entidade-produto, contrato-produto, chave_de_juncao_errada estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,04. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}, {"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Acompanhamentos", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false}]

SINTOMA OBSERVADO: Na grade, o Cupim aparece com a categoria 'Bebidas' e o Refrigerante com 'Acompanhamentos'; a Agua Mineral e o Balde de Cerveja aparecem com 'Bebidas'. Os nomes, os precos e as fotos estao certos.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os itens de id 7 a 10; a lista completa tem 14.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> chave_de_juncao_errada e não tipo_divergente: a escolha tem probabilidade 0,92 contra 0,04; verbete(s) na evidência: entidade-produto, contrato-produto, chave_de_juncao_errada

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `chave_de_juncao_errada` (Chave de junção errada) | 0,92 | sim |
| `tipo_divergente` (Tipo divergente) | 0,04 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,02 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-24`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 495 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:16:08 | caso tra-24 |
| 496 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:16:08 | 3 de 39 verbetes entregues |
| 498 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:16:08 | diagnostico: 4674 caracteres; verbetes entidade-produto, contrato-produto, chave_de_juncao_errada |
| 500 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:16:08 | diagnostico: 73,7 s |
| 501 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:16:08 | causa_raiz: `chave_de_juncao_errada` |
| 502 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:16:08 | campo: `tipo` |
| 503 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:16:08 | impacto: `Os produtos são exibidos com categorias incorretas, misturando itens de diferentes tipos.` |
| 504 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:16:08 | fonte: `[chave_de_juncao_errada]` |
| 505 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:16:08 | fonte_citada: `chave_de_juncao_errada` |
| 506 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | quatro_linhas_presentes: confere |
| 507 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | rotulo_no_conjunto: confere |
| 508 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | fonte_existe_na_biblioteca: confere |
| 509 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | fonte_estava_no_contexto: confere |
| 510 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | campo_existe_no_caso: confere |
| 511 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 512 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | notas_nos_verbetes_citados: informativo |
| 513 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | impacto: nao_verificavel |
| 514 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | fonte_formato_valido: confere |
| 515 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:16:08 | fonte_contem_termo_da_causa: confere |
| 516 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:16:08 | diagnostico: escolha chave_de_juncao_errada; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 516, decisão `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido.
  - Evidência: evento 496 (verbete_entregue: `entidade-produto`, `contrato-produto`, `chave_de_juncao_errada`); evento 500 (resposta); evento 505 (verbete_citado: `chave_de_juncao_errada`).
  - Usou: `entidade-produto`, `contrato-produto`, `chave_de_juncao_errada`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 495 a 516 da trilha; hash dos eventos deste caso: `f27bc1e9d1758c80`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
