<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Resposta truncada em `GET /api/produtos`, campo `preco`

Caso `sin-26` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/sin-26`: o caso `sin-26` na corrida `fase4_ineditos`; eventos 249 a 274 da trilha `trilha_ineditos.jsonl`, hash dos eventos `43855b1f6738e30c` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Resposta truncada em `GET /api/produtos`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 14:04:08 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `sin-26`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 2 (sintática: a forma da resposta não é a esperada); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Bebidas", "imagem": "refrigerante.png", "destaque": false}]
```

4. Sintoma observado (texto do caso):

> Na grade de bebidas, o botao de preco da Agua Mineral e o do Refrigerante mostram 'undefined', e o do Balde de Cerveja mostra 'R$ 45,00'. Ao recarregar a pagina, os produtos afetados mudam.

5. Observação adicional (texto do caso):

> O corpo mostra so os itens de id 8 a 10; a lista completa tem 14.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-26`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Na grade de bebidas, o botao de preco da Agua Mineral e o do Refrigerante mostram 'undefined', e o do Balde de Cerveja mostra 'R$ 45,00'. Ao recarregar a pagina, os produtos afetados mudam. |

Corpo recebido, como veio no caso:

```text
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Bebidas", "imagem": "refrigerante.png", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 2 (sintática: a forma da resposta não é a esperada); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 2 (sintática); nível 3 (difícil). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `sin-26` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/sin-26` em `trilha_ineditos.jsonl`, eventos 249 a 274, hash dos eventos `43855b1f6738e30c`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-26`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `resposta_truncada` (Resposta truncada). Campo: `preco`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,95 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê preços incorretos ou 'undefined' para alguns produtos, devido à lista truncada.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu resposta_truncada no campo preco porque os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,02. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Bebidas", "imagem": "refrigerante.png", "destaque": false}]

SINTOMA OBSERVADO: Na grade de bebidas, o botao de preco da Agua Mineral e o do Refrigerante mostram 'undefined', e o do Balde de Cerveja mostra 'R$ 45,00'. Ao recarregar a pagina, os produtos afetados mudam.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os itens de id 8 a 10; a lista completa tem 14.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> resposta_truncada e não campo_ausente: a escolha tem probabilidade 0,95 contra 0,02; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `resposta_truncada` (Resposta truncada) | 0,95 | sim |
| `campo_ausente` (Campo ausente) | 0,02 |  |
| `campo_renomeado` (Campo renomeado) | 0,02 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,01 |  |
| `corpo_vazio` (Corpo vazio) | 0,01 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,01 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `contagem_inconsistente` (Contagem inconsistente) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [campo_ausente]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto], [campo_ausente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "campo_ausente"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "resposta_truncada"} |
| O verbete citado fala da causa respondida | `campo_ausente` | não confere | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-26`

## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 249 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:04:08 | caso sin-26 |
| 250 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:04:08 | 3 de 39 verbetes entregues |
| 252 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:04:08 | diagnostico: 3917 caracteres; verbetes entidade-produto, contrato-produto, campo_ausente |
| 254 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:04:08 | diagnostico: 46,5 s |
| 255 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:08 | causa_raiz: `resposta_truncada` |
| 256 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:08 | campo: `preco` |
| 257 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:08 | impacto: `O usuário vê preços incorretos ou 'undefined' para alguns produtos, devido à lista truncada.` |
| 258 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:08 | fonte: `[contrato-produto], [campo_ausente]` |
| 259 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:08 | fonte_citada: `contrato-produto` |
| 260 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:08 | fonte_citada: `campo_ausente` |
| 261 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | quatro_linhas_presentes: confere |
| 262 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | rotulo_no_conjunto: confere |
| 263 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_existe_na_biblioteca: confere |
| 264 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_existe_na_biblioteca: confere |
| 265 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_estava_no_contexto: confere |
| 266 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_estava_no_contexto: confere |
| 267 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | campo_existe_no_caso: confere |
| 268 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 269 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | notas_nos_verbetes_citados: informativo |
| 270 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | impacto: nao_verificavel |
| 271 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_formato_valido: confere |
| 272 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_contem_termo_da_causa: nao_confere |
| 273 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:08 | fonte_contem_termo_da_causa: nao_confere |
| 274 | 24 | decisao | programa | ao_vivo | 2026-11-06T14:04:08 | diagnostico: escolha resposta_truncada; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 274, decisão `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido.
  - Evidência: evento 250 (verbete_entregue: `entidade-produto`, `contrato-produto`, `campo_ausente`); evento 254 (resposta); evento 259 (verbete_citado: `contrato-produto`); evento 260 (verbete_citado: `campo_ausente`).
  - Usou: `entidade-produto`, `contrato-produto`, `campo_ausente`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 249 a 274 da trilha; hash dos eventos deste caso: `43855b1f6738e30c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
