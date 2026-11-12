<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos`, campo `id`

Caso `tra-26` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/tra-26`: o caso `tra-26` na corrida `fase4_ineditos`; eventos 545 a 566 da trilha `trilha_ineditos.jsonl`, hash dos eventos `322098fc80ac1989` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos`, campo `id`

## 3. Data, organização e autor

Observado em 06/11/2026 14:18:30 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `tra-26`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 4 (tradução: o mapeamento entre as camadas está errado); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 4, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 5, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}, {"id": 6, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}]
```

4. Sintoma observado (texto do caso):

> A grade aparece normal, mas cada 'Saiba Mais...' abre o produto vizinho: o botao do cartao da Fraldinha abre o modal da Costelona, o da Costelona abre o da Alcatra na Pedra e o da Alcatra na Pedra abre o da Maminha. O clique no cartao da Fraldinha disparou GET /api/produtos/4, que respondeu 200 com os dados da Costelona.

5. Observação adicional (texto do caso):

> O corpo mostra so os cartoes da Fraldinha, da Costelona e da Alcatra na Pedra; a lista completa tem 14.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-26`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A grade aparece normal, mas cada 'Saiba Mais...' abre o produto vizinho: o botao do cartao da Fraldinha abre o modal da Costelona, o da Costelona abre o da Alcatra na Pedra e o da Alcatra na Pedra abre o da Maminha. O clique no cartao da Fraldinha disparou GET /api/produtos/4, que respondeu 200 com os dados da Costelona. |

Corpo recebido, como veio no caso:

```text
[{"id": 4, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 5, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}, {"id": 6, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 4 (tradução: o mapeamento entre as camadas está errado); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 4 (tradução); nível 3 (difícil). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `ancora-saiba-mais` (Link "Saiba Mais..." abre produto vazio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/defeitos_conhecidos/ancora-saiba-mais.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/defeitos_conhecidos/ancora-saiba-mais.md`).
- Caso escrito: `tra-26` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/tra-26` em `trilha_ineditos.jsonl`, eventos 545 a 566, hash dos eventos `322098fc80ac1989`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-26`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)). Campo: `id`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,92 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê o conteúdo do produto vizinho ao clicar no "Saiba Mais...".`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu colecao_no_lugar_de_objeto no campo id porque os verbetes entidade-produto, contrato-produto, ancora-saiba-mais estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,03. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 4, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 5, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}, {"id": 6, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}]

SINTOMA OBSERVADO: A grade aparece normal, mas cada 'Saiba Mais...' abre o produto vizinho: o botao do cartao da Fraldinha abre o modal da Costelona, o da Costelona abre o da Alcatra na Pedra e o da Alcatra na Pedra abre o da Maminha. O clique no cartao da Fraldinha disparou GET /api/produtos/4, que respondeu 200 com os dados da Costelona.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os cartoes da Fraldinha, da Costelona e da Alcatra na Pedra; a lista completa tem 14.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> colecao_no_lugar_de_objeto e não campo_ausente: a escolha tem probabilidade 0,92 contra 0,03; verbete(s) na evidência: entidade-produto, contrato-produto, ancora-saiba-mais

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,92 | sim |
| `campo_ausente` (Campo ausente) | 0,03 |  |
| `campo_renomeado` (Campo renomeado) | 0,03 |  |
| `resposta_truncada` (Resposta truncada) | 0,03 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,01 |  |
| `tipo_divergente` (Tipo divergente) | 0,01 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `ancora-saiba-mais` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids tra-26`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 545 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:18:30 | caso tra-26 |
| 546 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:18:30 | 3 de 39 verbetes entregues |
| 548 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:18:30 | diagnostico: 4117 caracteres; verbetes entidade-produto, contrato-produto, ancora-saiba-mais |
| 550 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:18:30 | diagnostico: 63,2 s |
| 551 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:18:30 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 552 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:18:30 | campo: `id` |
| 553 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:18:30 | impacto: `O usuário vê o conteúdo do produto vizinho ao clicar no "Saiba Mais...".` |
| 554 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:18:30 | fonte: `[contrato-produto]` |
| 555 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:18:30 | fonte_citada: `contrato-produto` |
| 556 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:18:30 | quatro_linhas_presentes: confere |
| 557 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:18:30 | rotulo_no_conjunto: confere |
| 558 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:18:30 | fonte_existe_na_biblioteca: confere |
| 559 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:18:30 | fonte_estava_no_contexto: confere |
| 560 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:18:30 | campo_existe_no_caso: confere |
| 561 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:18:30 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 562 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:18:30 | notas_nos_verbetes_citados: informativo |
| 563 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:18:30 | impacto: nao_verificavel |
| 564 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:18:30 | fonte_formato_valido: confere |
| 565 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:18:30 | fonte_contem_termo_da_causa: nao_confere |
| 566 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:18:30 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 566, decisão `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido.
  - Evidência: evento 546 (verbete_entregue: `entidade-produto`, `contrato-produto`, `ancora-saiba-mais`); evento 550 (resposta); evento 555 (verbete_citado: `contrato-produto`).
  - Usou: `entidade-produto`, `contrato-produto`, `ancora-saiba-mais`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 545 a 566 da trilha; hash dos eventos deste caso: `322098fc80ac1989`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
