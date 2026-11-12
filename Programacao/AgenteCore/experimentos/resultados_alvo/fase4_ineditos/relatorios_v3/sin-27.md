<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Campo renomeado em `GET /api/produtos`, campo `imagem_v2`

Caso `sin-27` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/sin-27`: o caso `sin-27` na corrida `fase4_ineditos`; eventos 276 a 297 da trilha `trilha_ineditos.jsonl`, hash dos eventos `4cdcf8b16eb6767d` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Campo renomeado em `GET /api/produtos`, campo `imagem_v2`

## 3. Data, organização e autor

Observado em 06/11/2026 14:04:59 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `sin-27`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 2 (sintática: a forma da resposta não é a esperada); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "destaque": true, "imagem_v2": "queijo.png"}, {"id": 13, "nome": "Hambúrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}, {"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e açúcar", "tipo": "Sobremesas", "preco": 14.9, "destaque": false, "imagem_v2": "abacaxi.jpg"}]
```

4. Sintoma observado (texto do caso):

> Na grade, o Queijo Coalho e o Abacaxi na Brasa aparecem sem foto, enquanto o Hamburguer Artesanal mostra a foto normalmente. Nome, categoria, preco e botoes estao certos nos tres. Ao recarregar a pagina, os cartoes sem foto mudam.

5. Observação adicional (texto do caso):

> O corpo mostra so os itens de id 12 a 14; a lista completa tem 14.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-27`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Na grade, o Queijo Coalho e o Abacaxi na Brasa aparecem sem foto, enquanto o Hamburguer Artesanal mostra a foto normalmente. Nome, categoria, preco e botoes estao certos nos tres. Ao recarregar a pagina, os cartoes sem foto mudam. |

Corpo recebido, como veio no caso:

```text
[{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "destaque": true, "imagem_v2": "queijo.png"}, {"id": 13, "nome": "Hambúrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}, {"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e açúcar", "tipo": "Sobremesas", "preco": 14.9, "destaque": false, "imagem_v2": "abacaxi.jpg"}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 2 (sintática: a forma da resposta não é a esperada); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 2 (sintática); nível 3 (difícil). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `chave_de_juncao_errada` (Chave de junção errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/chave_de_juncao_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/chave_de_juncao_errada.md`).
- Caso escrito: `sin-27` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/sin-27` em `trilha_ineditos.jsonl`, eventos 276 a 297, hash dos eventos `4cdcf8b16eb6767d`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-27`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `campo_renomeado` (Campo renomeado). Campo: `imagem_v2`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,41 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `Os itens sem foto mostram corretamente os nomes e preços, mas faltam as imagens, pois o campo correto é imagem, não imagem_v2.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu campo_renomeado no campo imagem_v2 porque os verbetes contrato-produto, entidade-produto, chave_de_juncao_errada estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,16. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,41); trate como hipótese e confira o campo imagem_v2 antes de agir.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "destaque": true, "imagem_v2": "queijo.png"}, {"id": 13, "nome": "Hambúrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}, {"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e açúcar", "tipo": "Sobremesas", "preco": 14.9, "destaque": false, "imagem_v2": "abacaxi.jpg"}]

SINTOMA OBSERVADO: Na grade, o Queijo Coalho e o Abacaxi na Brasa aparecem sem foto, enquanto o Hamburguer Artesanal mostra a foto normalmente. Nome, categoria, preco e botoes estao certos nos tres. Ao recarregar a pagina, os cartoes sem foto mudam.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os itens de id 12 a 14; a lista completa tem 14.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> campo_renomeado e não valor_fora_do_dominio: a escolha tem probabilidade 0,41 contra 0,16; verbete(s) na evidência: contrato-produto, entidade-produto, chave_de_juncao_errada

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `campo_renomeado` (Campo renomeado) | 0,41 | sim |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,16 |  |
| `tipo_divergente` (Tipo divergente) | 0,10 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,10 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,07 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,06 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,05 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,01 |  |
| `campo_ausente` (Campo ausente) | 0,01 |  |
| `nulo_inesperado` (Nulo inesperado) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `chave_de_juncao_errada` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `contrato-produto` |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `imagem_v2` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-27`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 276 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:04:59 | caso sin-27 |
| 277 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:04:59 | 3 de 39 verbetes entregues |
| 279 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:04:59 | diagnostico: 4579 caracteres; verbetes contrato-produto, entidade-produto, chave_de_juncao_errada |
| 281 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:04:59 | diagnostico: 73,5 s |
| 282 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:59 | causa_raiz: `campo_renomeado` |
| 283 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:59 | campo: `imagem_v2` |
| 284 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:59 | impacto: `Os itens sem foto mostram corretamente os nomes e preços, mas faltam as imagens, pois o campo correto é imagem, não imagem_v2.` |
| 285 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:59 | fonte: `[contrato-produto]` |
| 286 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:04:59 | fonte_citada: `contrato-produto` |
| 287 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:59 | quatro_linhas_presentes: confere |
| 288 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:59 | rotulo_no_conjunto: confere |
| 289 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:59 | fonte_existe_na_biblioteca: confere |
| 290 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:59 | fonte_estava_no_contexto: confere |
| 291 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:59 | campo_existe_no_caso: confere |
| 292 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:59 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 293 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:59 | notas_nos_verbetes_citados: informativo |
| 294 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:59 | impacto: nao_verificavel |
| 295 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:59 | fonte_formato_valido: confere |
| 296 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:04:59 | fonte_contem_termo_da_causa: nao_confere |
| 297 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:04:59 | diagnostico: escolha campo_renomeado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 297, decisão `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido.
  - Evidência: evento 277 (verbete_entregue: `contrato-produto`, `entidade-produto`, `chave_de_juncao_errada`); evento 281 (resposta); evento 286 (verbete_citado: `contrato-produto`).
  - Usou: `contrato-produto`, `entidade-produto`, `chave_de_juncao_errada`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 276 a 297 da trilha; hash dos eventos deste caso: `4cdcf8b16eb6767d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
