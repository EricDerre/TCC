<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Resposta truncada em `GET /api/produtos`

Caso `lex-10` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/lex-10@fixture`: o caso `lex-10` na corrida `fase4_tela_v4`; eventos 752 a 777 da trilha `trilha_tela.jsonl`, hash dos eventos `8e4cee2e8947d393` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Resposta truncada em `GET /api/produtos`

## 3. Data, organização e autor

Observado em 06/11/2026 10:22:56 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `lex-10`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 1 (léxica: o corpo da resposta nem dá para ler); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre
```

4. Sintoma observado (texto do caso):

> A lista carrega parcialmente. So acontece quando ha mais de 10 produtos.

5. Observação adicional (texto do caso):

> Content-Length declara 4096; o corpo recebido tem 4096 bytes exatos.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids lex-10 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A lista carrega parcialmente. So acontece quando ha mais de 10 produtos. |

Corpo recebido, como veio no caso:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 1 (léxica: o corpo da resposta nem dá para ler); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 1 (léxica); nível 3 (difícil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `resposta_truncada` (Resposta truncada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/resposta_truncada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/resposta_truncada.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `lex-10` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/lex-10@fixture` em `trilha_tela.jsonl`, eventos 752 a 777, hash dos eventos `8e4cee2e8947d393`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/lex-10@fixture.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids lex-10 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `resposta_truncada` (Resposta truncada). Campo: nenhum apontado. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê uma lista incompleta de produtos, com apenas os dois primeiros itens exibidos.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu resposta_truncada porque os verbetes entidade-produto, resposta_truncada, contrato-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre

SINTOMA OBSERVADO: A lista carrega parcialmente. So acontece quando ha mais de 10 produtos.

OBSERVAÇÃO ADICIONAL: Content-Length declara 4096; o corpo recebido tem 4096 bytes exatos.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> resposta_truncada e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, resposta_truncada, contrato-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `resposta_truncada` (Resposta truncada) | 1,00 | sim |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `limite_de_requisicoes` (Limite de requisições (429)) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[resposta_truncada] [contrato-produto]`; verbetes citados: `resposta_truncada` (Resposta truncada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/resposta_truncada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/resposta_truncada.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `entidade-produto`, `resposta_truncada`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `resposta_truncada`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | confere | verbetes: `resposta_truncada` |
| A linha FONTE só tem identificadores, no formato pedido | `[resposta_truncada] [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["resposta_truncada", "contrato-produto"]} |
| O verbete citado fala da causa respondida | `resposta_truncada` | confere | {"termo": "resposta_truncada"} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids lex-10 --k 3`

## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 752 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:22:56 | caso lex-10 |
| 753 | 2 | candidatos | programa | ao_vivo | 2026-11-06T10:22:56 | 3 de 39 verbetes entregues |
| 755 | 3 | prompt | programa | ao_vivo | 2026-11-06T10:22:56 | diagnostico: 3823 caracteres; verbetes entidade-produto, resposta_truncada, contrato-produto |
| 757 | 4 | inferencia | programa | ao_vivo | 2026-11-06T10:22:56 | diagnostico: 75,5 s |
| 758 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T10:22:56 | causa_raiz: `resposta_truncada` |
| 759 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T10:22:56 | campo: `nenhum` |
| 760 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T10:22:56 | impacto: `O usuário vê uma lista incompleta de produtos, com apenas os dois primeiros itens exibidos.` |
| 761 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T10:22:56 | fonte: `[resposta_truncada] [contrato-produto]` |
| 762 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T10:22:56 | fonte_citada: `resposta_truncada` |
| 763 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T10:22:56 | fonte_citada: `contrato-produto` |
| 764 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | quatro_linhas_presentes: confere |
| 765 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | rotulo_no_conjunto: confere |
| 766 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_existe_na_biblioteca: confere |
| 767 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_existe_na_biblioteca: confere |
| 768 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_estava_no_contexto: confere |
| 769 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_estava_no_contexto: confere |
| 770 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | campo_existe_no_caso: nao_se_aplica |
| 771 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 772 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | notas_nos_verbetes_citados: informativo |
| 773 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | impacto: nao_verificavel |
| 774 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_formato_valido: confere |
| 775 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_contem_termo_da_causa: confere |
| 776 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_contem_termo_da_causa: nao_confere |
| 777 | 24 | decisao | programa | ao_vivo | 2026-11-06T10:22:56 | diagnostico: escolha resposta_truncada; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 777, decisão `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido.
  - Evidência: evento 753 (verbete_entregue: `entidade-produto`, `resposta_truncada`, `contrato-produto`); evento 757 (resposta); evento 762 (verbete_citado: `resposta_truncada`); evento 763 (verbete_citado: `contrato-produto`).
  - Usou: `entidade-produto`, `resposta_truncada`, `contrato-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 752 a 777 da trilha; hash dos eventos deste caso: `8e4cee2e8947d393`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
