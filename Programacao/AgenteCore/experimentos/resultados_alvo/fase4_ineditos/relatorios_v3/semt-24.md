<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Tipo divergente em `GET /api/produtos`, campo `destaque`

Caso `semt-24` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/semt-24`: o caso `semt-24` na corrida `fase4_ineditos`; eventos 349 a 370 da trilha `trilha_ineditos.jsonl`, hash dos eventos `189e3de5ace07d9d` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Tipo divergente em `GET /api/produtos`, campo `destaque`

## 3. Data, organização e autor

Observado em 06/11/2026 14:08:45 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `semt-24`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": "True"}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": "False"}]
```

4. Sintoma observado (texto do caso):

> Nos cartoes da grade, a linha de destaque mostra 'destaque: True' e 'destaque: False' (em ingles, com inicial maiuscula) em vez de 'destaque: Sim' e 'destaque: Não'.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids semt-24`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Nos cartoes da grade, a linha de destaque mostra 'destaque: True' e 'destaque: False' (em ingles, com inicial maiuscula) em vez de 'destaque: Sim' e 'destaque: Não'. |

Corpo recebido, como veio no caso:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": "True"}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": "False"}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 3 (semântica); nível 2 (médio). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `tipo_divergente` (Tipo divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tipo_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tipo_divergente.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `semt-24` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/semt-24` em `trilha_ineditos.jsonl`, eventos 349 a 370, hash dos eventos `189e3de5ace07d9d`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids semt-24`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `tipo_divergente` (Tipo divergente). Campo: `destaque`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê "destaque: True" e "destaque: False" em inglês, em vez de "destaque: Sim" e "destaque: Não".`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu tipo_divergente no campo destaque porque os verbetes entidade-produto, tipo_divergente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": "True"}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": "False"}]

SINTOMA OBSERVADO: Nos cartoes da grade, a linha de destaque mostra 'destaque: True' e 'destaque: False' (em ingles, com inicial maiuscula) em vez de 'destaque: Sim' e 'destaque: Não'.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> tipo_divergente e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, tipo_divergente, contrato-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `tipo_divergente` (Tipo divergente) | 1,00 | sim |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente` (Tipo divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tipo_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tipo_divergente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| A linha FONTE só tem identificadores, no formato pedido | `[tipo_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["tipo_divergente"]} |
| O verbete citado fala da causa respondida | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `destaque` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids semt-24`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 349 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:08:45 | caso semt-24 |
| 350 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:08:45 | 3 de 39 verbetes entregues |
| 352 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:08:45 | diagnostico: 3841 caracteres; verbetes entidade-produto, tipo_divergente, contrato-produto |
| 354 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:08:45 | diagnostico: 70,7 s |
| 355 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:08:45 | causa_raiz: `tipo_divergente` |
| 356 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:08:45 | campo: `destaque` |
| 357 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:08:45 | impacto: `O usuário vê "destaque: True" e "destaque: False" em inglês, em vez de "destaque: Sim" e "destaque: Não".` |
| 358 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:08:45 | fonte: `[tipo_divergente]` |
| 359 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:08:45 | fonte_citada: `tipo_divergente` |
| 360 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:08:45 | quatro_linhas_presentes: confere |
| 361 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:08:45 | rotulo_no_conjunto: confere |
| 362 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:08:45 | fonte_existe_na_biblioteca: confere |
| 363 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:08:45 | fonte_estava_no_contexto: confere |
| 364 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:08:45 | campo_existe_no_caso: confere |
| 365 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:08:45 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 366 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:08:45 | notas_nos_verbetes_citados: informativo |
| 367 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:08:45 | impacto: nao_verificavel |
| 368 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:08:45 | fonte_formato_valido: confere |
| 369 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:08:45 | fonte_contem_termo_da_causa: confere |
| 370 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:08:45 | diagnostico: escolha tipo_divergente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 370, decisão `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido.
  - Evidência: evento 350 (verbete_entregue: `entidade-produto`, `tipo_divergente`, `contrato-produto`); evento 354 (resposta); evento 359 (verbete_citado: `tipo_divergente`).
  - Usou: `entidade-produto`, `tipo_divergente`, `contrato-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 349 a 370 da trilha; hash dos eventos deste caso: `189e3de5ace07d9d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
