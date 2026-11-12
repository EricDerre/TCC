<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Estrutura aninhada divergente em `GET /api/produtos`, campo `tipo`

Caso `sin-24` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/sin-24`: o caso `sin-24` na corrida `fase4_ineditos`; eventos 199 a 224 da trilha `trilha_ineditos.jsonl`, hash dos eventos `86021fefb902713d` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Estrutura aninhada divergente em `GET /api/produtos`, campo `tipo`

## 3. Data, organização e autor

Observado em 06/11/2026 14:01:29 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `sin-24`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 2 (sintática: a forma da resposta não é a esperada); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]
```

4. Sintoma observado (texto do caso):

> Sob o nome de cada produto, a linha da categoria mostra o texto {"valor":"Carnes","moeda":"BRL"} em vez de apenas Carnes. O resto de cada cartao esta normal.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-24`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Sob o nome de cada produto, a linha da categoria mostra o texto {"valor":"Carnes","moeda":"BRL"} em vez de apenas Carnes. O resto de cada cartao esta normal. |

Corpo recebido, como veio no caso:

```text
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 2 (sintática: a forma da resposta não é a esperada); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 2 (sintática); nível 2 (médio). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`).
- Caso escrito: `sin-24` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/sin-24` em `trilha_ineditos.jsonl`, eventos 199 a 224, hash dos eventos `86021fefb902713d`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-24`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `estrutura_aninhada_divergente` (Estrutura aninhada divergente). Campo: `tipo`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,80 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê a categoria com o formato completo {"valor":"Carnes","moeda":"BRL"} em vez de apenas "Carnes".`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu estrutura_aninhada_divergente no campo tipo porque os verbetes contrato-produto, entidade-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,09. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,80); trate como hipótese e confira o campo tipo antes de agir.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]

SINTOMA OBSERVADO: Sob o nome de cada produto, a linha da categoria mostra o texto {"valor":"Carnes","moeda":"BRL"} em vez de apenas Carnes. O resto de cada cartao esta normal.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> estrutura_aninhada_divergente e não campo_ausente: a escolha tem probabilidade 0,80 contra 0,09; verbete(s) na evidência: contrato-produto, entidade-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,80 | sim |
| `campo_ausente` (Campo ausente) | 0,09 |  |
| `campo_renomeado` (Campo renomeado) | 0,09 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,08 |  |
| `tipo_divergente` (Tipo divergente) | 0,02 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto] [contrato-produto]`; verbetes citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `estrutura_aninhada_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente` |
| A linha FONTE só tem identificadores, no formato pedido | `[entidade-produto] [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["entidade-produto", "contrato-produto"]} |
| O verbete citado fala da causa respondida | `entidade-produto` | não confere | {"termo": "estrutura_aninhada_divergente"} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "estrutura_aninhada_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-24`

## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 199 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:01:29 | caso sin-24 |
| 200 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:01:29 | 3 de 39 verbetes entregues |
| 202 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:01:29 | diagnostico: 3953 caracteres; verbetes contrato-produto, entidade-produto, estrutura_aninhada_divergente |
| 204 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:01:29 | diagnostico: 72,7 s |
| 205 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:01:29 | causa_raiz: `estrutura_aninhada_divergente` |
| 206 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:01:29 | campo: `tipo` |
| 207 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:01:29 | impacto: `O usuário vê a categoria com o formato completo {"valor":"Carnes","moeda":"BRL"} em vez de apenas "Carnes".` |
| 208 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:01:29 | fonte: `[entidade-produto] [contrato-produto]` |
| 209 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:01:29 | fonte_citada: `entidade-produto` |
| 210 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T14:01:29 | fonte_citada: `contrato-produto` |
| 211 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | quatro_linhas_presentes: confere |
| 212 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | rotulo_no_conjunto: confere |
| 213 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_existe_na_biblioteca: confere |
| 214 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_existe_na_biblioteca: confere |
| 215 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_estava_no_contexto: confere |
| 216 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_estava_no_contexto: confere |
| 217 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | campo_existe_no_caso: confere |
| 218 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 219 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | notas_nos_verbetes_citados: informativo |
| 220 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | impacto: nao_verificavel |
| 221 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_formato_valido: confere |
| 222 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_contem_termo_da_causa: nao_confere |
| 223 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T14:01:29 | fonte_contem_termo_da_causa: nao_confere |
| 224 | 24 | decisao | programa | ao_vivo | 2026-11-06T14:01:29 | diagnostico: escolha estrutura_aninhada_divergente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 224, decisão `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido.
  - Evidência: evento 200 (verbete_entregue: `contrato-produto`, `entidade-produto`, `estrutura_aninhada_divergente`); evento 204 (resposta); evento 209 (verbete_citado: `entidade-produto`); evento 210 (verbete_citado: `contrato-produto`).
  - Usou: `contrato-produto`, `entidade-produto`, `estrutura_aninhada_divergente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 199 a 224 da trilha; hash dos eventos deste caso: `86021fefb902713d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
