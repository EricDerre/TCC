<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Escala ou unidade errada em `GET /api/produtos`, campo `preco`

Caso `tra-19` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/tra-19@fixture`: o caso `tra-19` na corrida `fase4_tela_v4`; eventos 1944 a 1969 da trilha `trilha_tela.jsonl`, hash dos eventos `1399badeeb895964` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Escala ou unidade errada em `GET /api/produtos`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 11:03:33 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `tra-19`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 4 (tradução: o mapeamento entre as camadas está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 4.5, "imagem": "balde_cerveja.png", "destaque": true}]
```

4. Sintoma observado (texto do caso):

> O Balde de Cerveja aparece por 'R$ 4,50'; no cadastro custa R$ 45,00: dez vezes mais.

5. Observação adicional (texto do caso):

> tbprodutos.valor_produto do id 9 vale 45.00.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-19 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O Balde de Cerveja aparece por 'R$ 4,50'; no cadastro custa R$ 45,00: dez vezes mais. |

Corpo recebido, como veio no caso:

```text
[{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 4.5, "imagem": "balde_cerveja.png", "destaque": true}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 4 (tradução: o mapeamento entre as camadas está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 4 (tradução); nível 2 (médio). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`).
- Caso escrito: `tra-19` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/tra-19@fixture` em `trilha_tela.jsonl`, eventos 1944 a 1969, hash dos eventos `1399badeeb895964`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/tra-19@fixture.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-19 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `escala_ou_unidade_errada` (Escala ou unidade errada). Campo: `preco`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,61 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê o preço do Balde de Cerveja como R$ 4,50, quando na verdade é R$ 45,00.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu escala_ou_unidade_errada no campo preco porque os verbetes entidade-produto, contrato-produto, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,17. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,61); trate como hipótese e confira o campo preco antes de agir.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 4.5, "imagem": "balde_cerveja.png", "destaque": true}]

SINTOMA OBSERVADO: O Balde de Cerveja aparece por 'R$ 4,50'; no cadastro custa R$ 45,00 — dez vezes mais.

OBSERVAÇÃO ADICIONAL: tbprodutos.valor_produto do id 9 vale 45.00.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> escala_ou_unidade_errada e não valor_fora_do_dominio: a escolha tem probabilidade 0,61 contra 0,17; verbete(s) na evidência: entidade-produto, contrato-produto, nulo_inesperado

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,61 | sim |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,17 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,13 |  |
| `tipo_divergente` (Tipo divergente) | 0,09 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `nulo_inesperado` (Nulo inesperado) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto] [contrato-produto]`; verbetes citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto` |
| A linha FONTE só tem identificadores, no formato pedido | `[entidade-produto] [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["entidade-produto", "contrato-produto"]} |
| O verbete citado fala da causa respondida | `entidade-produto` | não confere | {"termo": "escala_ou_unidade_errada"} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-19 --k 3`

## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1944 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:03:33 | caso tra-19 |
| 1945 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:03:33 | 3 de 39 verbetes entregues |
| 1947 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:03:33 | diagnostico: 3453 caracteres; verbetes entidade-produto, contrato-produto, nulo_inesperado |
| 1949 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:03:33 | diagnostico: 43,1 s |
| 1950 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:03:33 | causa_raiz: `escala_ou_unidade_errada` |
| 1951 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:03:33 | campo: `preco` |
| 1952 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:03:33 | impacto: `O usuário vê o preço do Balde de Cerveja como R$ 4,50, quando na verdade é R$ 45,00.` |
| 1953 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:03:33 | fonte: `[entidade-produto] [contrato-produto]` |
| 1954 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:03:33 | fonte_citada: `entidade-produto` |
| 1955 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T11:03:33 | fonte_citada: `contrato-produto` |
| 1956 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | quatro_linhas_presentes: confere |
| 1957 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | rotulo_no_conjunto: confere |
| 1958 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | fonte_existe_na_biblioteca: confere |
| 1959 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | fonte_existe_na_biblioteca: confere |
| 1960 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | fonte_estava_no_contexto: confere |
| 1961 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | fonte_estava_no_contexto: confere |
| 1962 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | campo_existe_no_caso: confere |
| 1963 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1964 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | notas_nos_verbetes_citados: informativo |
| 1965 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | impacto: nao_verificavel |
| 1966 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | fonte_formato_valido: confere |
| 1967 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | fonte_contem_termo_da_causa: nao_confere |
| 1968 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:03:33 | fonte_contem_termo_da_causa: nao_confere |
| 1969 | 24 | decisao | programa | ao_vivo | 2026-11-06T11:03:33 | diagnostico: escolha escala_ou_unidade_errada; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 1969, decisão `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido.
  - Evidência: evento 1945 (verbete_entregue: `entidade-produto`, `contrato-produto`, `nulo_inesperado`); evento 1949 (resposta); evento 1954 (verbete_citado: `entidade-produto`); evento 1955 (verbete_citado: `contrato-produto`).
  - Usou: `entidade-produto`, `contrato-produto`, `nulo_inesperado`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1944 a 1969 da trilha; hash dos eventos deste caso: `1399badeeb895964`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
