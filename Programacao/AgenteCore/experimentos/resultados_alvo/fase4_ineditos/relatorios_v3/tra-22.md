<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Tipo divergente em `GET /api/produtos`, campo `preco`

Caso `tra-22` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/tra-22`: o caso `tra-22` na corrida `fase4_ineditos`; eventos 441 a 466 da trilha `trilha_ineditos.jsonl`, hash dos eventos `bf62c932e59826a9` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Tipo divergente em `GET /api/produtos`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 14:13:53 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `tra-22`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 4 (tradução: o mapeamento entre as camadas está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 600.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 4500.0, "imagem": "balde_cerveja.png", "destaque": true}]
```

4. Sintoma observado (texto do caso):

> Na grade de bebidas, a Agua Mineral aparece por 'R$ 600,00' e o Balde de Cerveja por 'R$ 4500,00'; nomes, categorias e fotos estao certos.

5. Observação adicional (texto do caso):

> Antes da falha, a mesma grade mostrava a Agua Mineral por 'R$ 6,00' e o Balde de Cerveja por 'R$ 45,00'.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-22`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Na grade de bebidas, a Agua Mineral aparece por 'R$ 600,00' e o Balde de Cerveja por 'R$ 4500,00'; nomes, categorias e fotos estao certos. |

Corpo recebido, como veio no caso:

```text
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 600.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 4500.0, "imagem": "balde_cerveja.png", "destaque": true}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 4 (tradução: o mapeamento entre as camadas está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 4 (tradução); nível 1 (fácil). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`).
- Caso escrito: `tra-22` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/tra-22` em `trilha_ineditos.jsonl`, eventos 441 a 466, hash dos eventos `bf62c932e59826a9`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-22`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `tipo_divergente` (Tipo divergente). Campo: `preco`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,81 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `Os preços exibidos na interface são muito altos, sugerindo um erro na formatação ou conversão do valor.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu tipo_divergente no campo preco porque os verbetes entidade-produto, nulo_inesperado, contrato-produto estavam entre os entregues ao modelo. A segunda causa, escala_ou_unidade_errada, ficou com probabilidade 0,09. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,81); trate como hipótese e confira o campo preco antes de agir.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 600.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 4500.0, "imagem": "balde_cerveja.png", "destaque": true}]

SINTOMA OBSERVADO: Na grade de bebidas, a Agua Mineral aparece por 'R$ 600,00' e o Balde de Cerveja por 'R$ 4500,00'; nomes, categorias e fotos estao certos.

OBSERVAÇÃO ADICIONAL: Antes da falha, a mesma grade mostrava a Agua Mineral por 'R$ 6,00' e o Balde de Cerveja por 'R$ 45,00'.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> tipo_divergente e não escala_ou_unidade_errada: a escolha tem probabilidade 0,81 contra 0,09; verbete(s) na evidência: entidade-produto, nulo_inesperado, contrato-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `tipo_divergente` (Tipo divergente) | 0,81 | sim |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,09 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,06 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,04 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `nulo_inesperado`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `nulo_inesperado`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto` |
| A linha FONTE só tem identificadores, no formato pedido | `[entidade-produto], [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["entidade-produto", "contrato-produto"]} |
| O verbete citado fala da causa respondida | `entidade-produto` | não confere | {"termo": "tipo_divergente"} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-22`

## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 441 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:13:53 | caso tra-22 |
| 442 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:13:53 | 3 de 39 verbetes entregues |
| 444 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:13:53 | diagnostico: 3722 caracteres; verbetes entidade-produto, nulo_inesperado, contrato-produto |
| 446 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:13:53 | diagnostico: 69,2 s |
| 447 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:13:53 | causa_raiz: `tipo_divergente` |
| 448 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:13:53 | campo: `preco` |
| 449 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:13:53 | impacto: `Os preços exibidos na interface são muito altos, sugerindo um erro na formatação ou conversão do valor.` |
| 450 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:13:53 | fonte: `[entidade-produto], [contrato-produto]` |
| 451 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:13:53 | fonte_citada: `entidade-produto` |
| 452 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T14:13:53 | fonte_citada: `contrato-produto` |
| 453 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | quatro_linhas_presentes: confere |
| 454 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | rotulo_no_conjunto: confere |
| 455 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | fonte_existe_na_biblioteca: confere |
| 456 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | fonte_existe_na_biblioteca: confere |
| 457 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | fonte_estava_no_contexto: confere |
| 458 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | fonte_estava_no_contexto: confere |
| 459 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | campo_existe_no_caso: confere |
| 460 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 461 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | notas_nos_verbetes_citados: informativo |
| 462 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | impacto: nao_verificavel |
| 463 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | fonte_formato_valido: confere |
| 464 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | fonte_contem_termo_da_causa: nao_confere |
| 465 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T14:13:53 | fonte_contem_termo_da_causa: nao_confere |
| 466 | 24 | decisao | programa | ao_vivo | 2026-11-06T14:13:53 | diagnostico: escolha tipo_divergente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 466, decisão `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido.
  - Evidência: evento 442 (verbete_entregue: `entidade-produto`, `nulo_inesperado`, `contrato-produto`); evento 446 (resposta); evento 451 (verbete_citado: `entidade-produto`); evento 452 (verbete_citado: `contrato-produto`).
  - Usou: `entidade-produto`, `nulo_inesperado`, `contrato-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 441 a 466 da trilha; hash dos eventos deste caso: `bf62c932e59826a9`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
