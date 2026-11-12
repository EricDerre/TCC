<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Tipo divergente em `GET /api/produtos/2`, campo `preco`

Caso `tra-27` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/tra-27`: o caso `tra-27` na corrida `fase4_ineditos`; eventos 568 a 593 da trilha `trilha_ineditos.jsonl`, hash dos eventos `fefbdf2f30565248` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Tipo divergente em `GET /api/produtos/2`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 14:19:38 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/2` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `tra-27`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 4 (tradução: o mapeamento entre as camadas está errado); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/2`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 8490.0, "imagem": "picanha_sem.jpg", "destaque": false}
```

4. Sintoma observado (texto do caso):

> O modal da Picanha Simples abre normal (ele so mostra nome e descricao), mas a conferencia de preco do roteiro falha: o preco do detalhe nao bate com o do cartao.

5. Observação adicional (texto do caso):

> A listagem GET /api/produtos, feita antes, trouxe este produto (id 2) com preco 84.9, e o cartao mostra 'R$ 84,90'.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-27`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/2` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O modal da Picanha Simples abre normal (ele so mostra nome e descricao), mas a conferencia de preco do roteiro falha: o preco do detalhe nao bate com o do cartao. |

Corpo recebido, como veio no caso:

```text
{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 8490.0, "imagem": "picanha_sem.jpg", "destaque": false}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 4 (tradução: o mapeamento entre as camadas está errado); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 4 (tradução); nível 3 (difícil). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Verbetes entregues pela busca e não citados: `pagina-produtos-api` (Aba "Produtos (API)", a fronteira JSON; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/pagina-produtos-api.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/pagina-produtos-api.md`).
- Caso escrito: `tra-27` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/tra-27` em `trilha_ineditos.jsonl`, eventos 568 a 593, hash dos eventos `fefbdf2f30565248`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-27`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `tipo_divergente` (Tipo divergente). Campo: `preco`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,96 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O preço exibido no detalhe do produto difere do preço no cartão, causando confusão para o usuário.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu tipo_divergente no campo preco porque os verbetes entidade-produto, contrato-produto, pagina-produtos-api estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,03 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/2

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 8490.0, "imagem": "picanha_sem.jpg", "destaque": false}

SINTOMA OBSERVADO: O modal da Picanha Simples abre normal (ele so mostra nome e descricao), mas a conferencia de preco do roteiro falha: o preco do detalhe nao bate com o do cartao.

OBSERVAÇÃO ADICIONAL: A listagem GET /api/produtos, feita antes, trouxe este produto (id 2) com preco 84.9, e o cartao mostra 'R$ 84,90'.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 0,96 contra 0,03; verbete(s) na evidência: entidade-produto, contrato-produto, pagina-produtos-api

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `tipo_divergente` (Tipo divergente) | 0,96 | sim |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,03 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [entidade-produto]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `pagina-produtos-api` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `pagina-produtos-api` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto`, `pagina-produtos-api` |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto] [entidade-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "entidade-produto"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "tipo_divergente"} |
| O verbete citado fala da causa respondida | `entidade-produto` | não confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-27`

## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 568 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:19:38 | caso tra-27 |
| 569 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:19:38 | 3 de 39 verbetes entregues |
| 571 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:19:38 | diagnostico: 3626 caracteres; verbetes entidade-produto, contrato-produto, pagina-produtos-api |
| 573 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:19:38 | diagnostico: 55,8 s |
| 574 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:19:38 | causa_raiz: `tipo_divergente` |
| 575 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:19:38 | campo: `preco` |
| 576 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:19:38 | impacto: `O preço exibido no detalhe do produto difere do preço no cartão, causando confusão para o usuário.` |
| 577 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:19:38 | fonte: `[contrato-produto] [entidade-produto]` |
| 578 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:19:38 | fonte_citada: `contrato-produto` |
| 579 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T14:19:38 | fonte_citada: `entidade-produto` |
| 580 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | quatro_linhas_presentes: confere |
| 581 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | rotulo_no_conjunto: confere |
| 582 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | fonte_existe_na_biblioteca: confere |
| 583 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | fonte_existe_na_biblioteca: confere |
| 584 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | fonte_estava_no_contexto: confere |
| 585 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | fonte_estava_no_contexto: confere |
| 586 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | campo_existe_no_caso: confere |
| 587 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 588 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | notas_nos_verbetes_citados: informativo |
| 589 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | impacto: nao_verificavel |
| 590 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | fonte_formato_valido: confere |
| 591 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | fonte_contem_termo_da_causa: nao_confere |
| 592 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T14:19:38 | fonte_contem_termo_da_causa: nao_confere |
| 593 | 24 | decisao | programa | ao_vivo | 2026-11-06T14:19:38 | diagnostico: escolha tipo_divergente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 593, decisão `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido.
  - Evidência: evento 569 (verbete_entregue: `entidade-produto`, `contrato-produto`, `pagina-produtos-api`); evento 573 (resposta); evento 578 (verbete_citado: `contrato-produto`); evento 579 (verbete_citado: `entidade-produto`).
  - Usou: `entidade-produto`, `contrato-produto`, `pagina-produtos-api`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 568 a 593 da trilha; hash dos eventos deste caso: `fefbdf2f30565248`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
