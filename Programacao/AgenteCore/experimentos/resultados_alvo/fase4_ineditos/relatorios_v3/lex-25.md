<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Codificação de caracteres incorreta em `GET /api/produtos`, campo `nome`

Caso `lex-25` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/lex-25`: o caso `lex-25` na corrida `fase4_ineditos`; eventos 76 a 101 da trilha `trilha_ineditos.jsonl`, hash dos eventos `77cf48f787396495` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Codificação de caracteres incorreta em `GET /api/produtos`, campo `nome`

## 3. Data, organização e autor

Observado em 06/11/2026 13:56:02 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `lex-25`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 1 (léxica: o corpo da resposta nem dá para ler); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}, {"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}, {"id": 13, "nome": "HambÃºrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}]
```

4. Sintoma observado (texto do caso):

> Na grade de acompanhamentos, os titulos 'PÃ£o de Alho' e 'HambÃºrguer Artesanal' aparecem com simbolos estranhos no lugar das letras acentuadas, enquanto 'Queijo Coalho' (sem acento no nome) aparece normal. A descricao de cada cartao, logo abaixo do titulo, esta com os acentos certos.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids lex-25`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Na grade de acompanhamentos, os titulos 'PÃ£o de Alho' e 'HambÃºrguer Artesanal' aparecem com simbolos estranhos no lugar das letras acentuadas, enquanto 'Queijo Coalho' (sem acento no nome) aparece normal. A descricao de cada cartao, logo abaixo do titulo, esta com os acentos certos. |

Corpo recebido, como veio no caso:

```text
[{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}, {"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}, {"id": 13, "nome": "HambÃºrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 1 (léxica: o corpo da resposta nem dá para ler); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 1 (léxica); nível 2 (médio). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`).
- Caso escrito: `lex-25` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/lex-25` em `trilha_ineditos.jsonl`, eventos 76 a 101, hash dos eventos `77cf48f787396495`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids lex-25`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `codificacao_incorreta` (Codificação de caracteres incorreta). Campo: `nome`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `Os títulos dos produtos exibidos na interface apresentam caracteres inválidos, prejudicando a leitura e compreensão dos nomes.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu codificacao_incorreta no campo nome porque os verbetes entidade-produto, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}, {"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}, {"id": 13, "nome": "HambÃºrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}]

SINTOMA OBSERVADO: Na grade de acompanhamentos, os titulos 'PÃ£o de Alho' e 'HambÃºrguer Artesanal' aparecem com simbolos estranhos no lugar das letras acentuadas, enquanto 'Queijo Coalho' (sem acento no nome) aparece normal. A descricao de cada cartao, logo abaixo do titulo, esta com os acentos certos.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> codificacao_incorreta e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, campo_renomeado

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `codificacao_incorreta` (Codificação de caracteres incorreta) | 1,00 | sim |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[entidade-produto], [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["entidade-produto", "contrato-produto"]} |
| O verbete citado fala da causa respondida | `entidade-produto` | não confere | {"termo": "codificacao_incorreta"} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids lex-25`

## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 76 | 1 | entrada | programa | ao_vivo | 2026-11-06T13:56:02 | caso lex-25 |
| 77 | 2 | candidatos | programa | ao_vivo | 2026-11-06T13:56:02 | 3 de 39 verbetes entregues |
| 79 | 3 | prompt | programa | ao_vivo | 2026-11-06T13:56:02 | diagnostico: 4147 caracteres; verbetes entidade-produto, contrato-produto, campo_renomeado |
| 81 | 4 | inferencia | programa | ao_vivo | 2026-11-06T13:56:02 | diagnostico: 58,8 s |
| 82 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T13:56:02 | causa_raiz: `codificacao_incorreta` |
| 83 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T13:56:02 | campo: `nome` |
| 84 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T13:56:02 | impacto: `Os títulos dos produtos exibidos na interface apresentam caracteres inválidos, prejudicando a leitura e compreensão dos nomes.` |
| 85 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T13:56:02 | fonte: `[entidade-produto], [contrato-produto]` |
| 86 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T13:56:02 | fonte_citada: `entidade-produto` |
| 87 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T13:56:02 | fonte_citada: `contrato-produto` |
| 88 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | quatro_linhas_presentes: confere |
| 89 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | rotulo_no_conjunto: confere |
| 90 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | fonte_existe_na_biblioteca: confere |
| 91 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | fonte_existe_na_biblioteca: confere |
| 92 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | fonte_estava_no_contexto: confere |
| 93 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | fonte_estava_no_contexto: confere |
| 94 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | campo_existe_no_caso: confere |
| 95 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 96 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | notas_nos_verbetes_citados: informativo |
| 97 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | impacto: nao_verificavel |
| 98 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | fonte_formato_valido: confere |
| 99 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | fonte_contem_termo_da_causa: nao_confere |
| 100 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T13:56:02 | fonte_contem_termo_da_causa: nao_confere |
| 101 | 24 | decisao | programa | ao_vivo | 2026-11-06T13:56:02 | diagnostico: escolha codificacao_incorreta; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 101, decisão `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido.
  - Evidência: evento 77 (verbete_entregue: `entidade-produto`, `contrato-produto`, `campo_renomeado`); evento 81 (resposta); evento 86 (verbete_citado: `entidade-produto`); evento 87 (verbete_citado: `contrato-produto`).
  - Usou: `entidade-produto`, `contrato-produto`, `campo_renomeado`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 76 a 101 da trilha; hash dos eventos deste caso: `77cf48f787396495`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
