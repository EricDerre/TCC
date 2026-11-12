<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos`, campo `imagem_url`

Caso `sin-14` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/sin-14@fixture`: o caso `sin-14` na corrida `fase4_tela_v4`; eventos 932 a 953 da trilha `trilha_tela.jsonl`, hash dos eventos `ad4d093cb10bd1af` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos`, campo `imagem_url`

## 3. Data, organização e autor

Observado em 06/11/2026 10:30:16 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `sin-14`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 2 (sintática: a forma da resposta não é a esperada); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem_url": "picanha_alho.jpg", "destaque": true}]
```

4. Sintoma observado (texto do caso):

> Todos os cartoes mostram icone de imagem quebrada; o resto do dado esta certo.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-14 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Todos os cartoes mostram icone de imagem quebrada; o resto do dado esta certo. |

Corpo recebido, como veio no caso:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem_url": "picanha_alho.jpg", "destaque": true}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 2 (sintática: a forma da resposta não é a esperada); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 2 (sintática); nível 3 (difícil). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`).
- Caso escrito: `sin-14` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/sin-14@fixture` em `trilha_tela.jsonl`, eventos 932 a 953, hash dos eventos `ad4d093cb10bd1af`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/sin-14@fixture.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-14 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)). Campo: `imagem_url`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,31 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O ícone de imagem quebrado indica que a URL da imagem está sendo tratada como uma coleção, resultando em erros de exibição.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu colecao_no_lugar_de_objeto no campo imagem_url porque os verbetes entidade-produto, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,17. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,31); trate como hipótese e confira o campo imagem_url antes de agir.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem_url": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: Todos os cartoes mostram icone de imagem quebrada; o resto do dado esta certo.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> colecao_no_lugar_de_objeto e não tipo_divergente: a escolha tem probabilidade 0,31 contra 0,17; verbete(s) na evidência: entidade-produto, contrato-produto, campo_renomeado

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,31 | sim |
| `tipo_divergente` (Tipo divergente) | 0,17 |  |
| `resposta_truncada` (Resposta truncada) | 0,16 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,14 |  |
| `campo_ausente` (Campo ausente) | 0,09 |  |
| `campo_renomeado` (Campo renomeado) | 0,09 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,03 |  |
| `corpo_vazio` (Corpo vazio) | 0,03 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `imagem_url` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-14 --k 3`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 932 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:30:16 | caso sin-14 |
| 933 | 2 | candidatos | programa | ao_vivo | 2026-11-06T10:30:16 | 3 de 39 verbetes entregues |
| 935 | 3 | prompt | programa | ao_vivo | 2026-11-06T10:30:16 | diagnostico: 3588 caracteres; verbetes entidade-produto, contrato-produto, campo_renomeado |
| 937 | 4 | inferencia | programa | ao_vivo | 2026-11-06T10:30:16 | diagnostico: 55,6 s |
| 938 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T10:30:16 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 939 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T10:30:16 | campo: `imagem_url` |
| 940 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T10:30:16 | impacto: `O ícone de imagem quebrado indica que a URL da imagem está sendo tratada como uma coleção, resultando em erros de exibição.` |
| 941 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T10:30:16 | fonte: `[contrato-produto]` |
| 942 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T10:30:16 | fonte_citada: `contrato-produto` |
| 943 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:30:16 | quatro_linhas_presentes: confere |
| 944 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:30:16 | rotulo_no_conjunto: confere |
| 945 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:30:16 | fonte_existe_na_biblioteca: confere |
| 946 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:30:16 | fonte_estava_no_contexto: confere |
| 947 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T10:30:16 | campo_existe_no_caso: confere |
| 948 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T10:30:16 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 949 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T10:30:16 | notas_nos_verbetes_citados: informativo |
| 950 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:30:16 | impacto: nao_verificavel |
| 951 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:30:16 | fonte_formato_valido: confere |
| 952 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:30:16 | fonte_contem_termo_da_causa: nao_confere |
| 953 | 20 | decisao | programa | ao_vivo | 2026-11-06T10:30:16 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 953, decisão `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido.
  - Evidência: evento 933 (verbete_entregue: `entidade-produto`, `contrato-produto`, `campo_renomeado`); evento 937 (resposta); evento 942 (verbete_citado: `contrato-produto`).
  - Usou: `entidade-produto`, `contrato-produto`, `campo_renomeado`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 932 a 953 da trilha; hash dos eventos deste caso: `ad4d093cb10bd1af`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
