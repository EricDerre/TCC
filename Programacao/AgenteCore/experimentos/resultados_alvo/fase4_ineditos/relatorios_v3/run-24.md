<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Registro duplicado em `GET /api/produtos`, campo `id`

Caso `run-24` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/run-24`: o caso `run-24` na corrida `fase4_ineditos`; eventos 641 a 666 da trilha `trilha_ineditos.jsonl`, hash dos eventos `c208aaf87e9d9507` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Registro duplicado em `GET /api/produtos`, campo `id`

## 3. Data, organização e autor

Observado em 06/11/2026 14:23:18 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `run-24`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": false}]
```

4. Sintoma observado (texto do caso):

> A grade mostra o cartao da Picanha ao Alho duas vezes seguidas, identicos, e os outros produtos uma vez cada. A grade tem 15 cartoes; a tabela tbprodutos tem 14 linhas.

5. Observação adicional (texto do caso):

> O corpo mostra so os 3 primeiros itens da lista recebida (15 itens no total).

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids run-24`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A grade mostra o cartao da Picanha ao Alho duas vezes seguidas, identicos, e os outros produtos uma vez cada. A grade tem 15 cartoes; a tabela tbprodutos tem 14 linhas. |

Corpo recebido, como veio no caso:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 5 (tempo e estado); nível 2 (médio). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `run-24` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/run-24` em `trilha_ineditos.jsonl`, eventos 641 a 666, hash dos eventos `c208aaf87e9d9507`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids run-24`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `registro_duplicado` (Registro duplicado). Campo: `id`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,97 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê a Picanha ao Alho duplicada na grade, enquanto os outros produtos aparecem uma única vez.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu registro_duplicado no campo id porque os verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,01 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": false}]

SINTOMA OBSERVADO: A grade mostra o cartao da Picanha ao Alho duas vezes seguidas, identicos, e os outros produtos uma vez cada. A grade tem 15 cartoes; a tabela tbprodutos tem 14 linhas.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os 3 primeiros itens da lista recebida (15 itens no total).
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> registro_duplicado e não resposta_truncada: a escolha tem probabilidade 0,97 contra 0,01; verbete(s) na evidência: entidade-produto, contrato-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `registro_duplicado` (Registro duplicado) | 0,97 | sim |
| `resposta_truncada` (Resposta truncada) | 0,01 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,01 |  |
| `corpo_vazio` (Corpo vazio) | 0,01 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `recurso_inexistente` (Recurso inexistente (404 e vizinhos)) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [estrutura_aninhada_divergente]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto] [estrutura_aninhada_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "estrutura_aninhada_divergente"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "registro_duplicado"} |
| O verbete citado fala da causa respondida | `estrutura_aninhada_divergente` | não confere | {"termo": "registro_duplicado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids run-24`

## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 641 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:23:18 | caso run-24 |
| 642 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:23:18 | 3 de 39 verbetes entregues |
| 644 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:23:18 | diagnostico: 4201 caracteres; verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente |
| 646 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:23:18 | diagnostico: 67,4 s |
| 647 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:23:18 | causa_raiz: `registro_duplicado` |
| 648 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:23:18 | campo: `id` |
| 649 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:23:18 | impacto: `O usuário vê a Picanha ao Alho duplicada na grade, enquanto os outros produtos aparecem uma única vez.` |
| 650 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:23:18 | fonte: `[contrato-produto] [estrutura_aninhada_divergente]` |
| 651 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:23:18 | fonte_citada: `contrato-produto` |
| 652 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T14:23:18 | fonte_citada: `estrutura_aninhada_divergente` |
| 653 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | quatro_linhas_presentes: confere |
| 654 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | rotulo_no_conjunto: confere |
| 655 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | fonte_existe_na_biblioteca: confere |
| 656 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | fonte_existe_na_biblioteca: confere |
| 657 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | fonte_estava_no_contexto: confere |
| 658 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | fonte_estava_no_contexto: confere |
| 659 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | campo_existe_no_caso: confere |
| 660 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 661 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | notas_nos_verbetes_citados: informativo |
| 662 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | impacto: nao_verificavel |
| 663 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | fonte_formato_valido: confere |
| 664 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | fonte_contem_termo_da_causa: nao_confere |
| 665 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T14:23:18 | fonte_contem_termo_da_causa: nao_confere |
| 666 | 24 | decisao | programa | ao_vivo | 2026-11-06T14:23:18 | diagnostico: escolha registro_duplicado; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 666, decisão `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido.
  - Evidência: evento 642 (verbete_entregue: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente`); evento 646 (resposta); evento 651 (verbete_citado: `contrato-produto`); evento 652 (verbete_citado: `estrutura_aninhada_divergente`).
  - Usou: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 641 a 666 da trilha; hash dos eventos deste caso: `c208aaf87e9d9507`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
