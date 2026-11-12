<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 15 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos/9`, campo `id`

Caso `relatorio-15` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-15`: o caso `relatorio-15` na corrida `fase4_ineditos`; eventos 833 a 858 da trilha `trilha_ineditos.jsonl`, hash dos eventos `93af00621c521043` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos/9`, campo `id`

## 3. Data, organização e autor

Observado em 06/11/2026 14:33:09 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/9` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-15`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/9`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}
```

Árvore de acessibilidade da página, como o caso a trouxe:

```text
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Fraldinha" level=3
      text "Carnes"
      button "R$ 69,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    group
      heading "Balde de Cerveja" level=3
      text "Bebidas"
      button "R$ 45,00"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="9"
  dialog
    button "×" class="close"
    heading "Fraldinha" level=4 id="modalDetalheTitulo"
    text "Corte grelhado na brasa, fatiado na hora" id="modalDetalheCorpo"
```

4. Sintoma observado (texto do caso):

> O roteiro clica em 'Saiba Mais...' da Fraldinha e, logo em seguida, no do Balde de Cerveja. As duas requisicoes (GET /api/produtos/3 e GET /api/produtos/9) respondem 200 com o corpo certo, mas a de id 3 chega cerca de 2 segundos depois da de id 9. O modal fica com o titulo e a descricao da Fraldinha; a verificacao esperava o Balde de Cerveja.

5. Observação adicional (texto do caso):

> O corpo mostrado e o da ultima requisicao disparada (id 9); a resposta do id 3 tambem tinha o corpo certo.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/9` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O roteiro clica em 'Saiba Mais...' da Fraldinha e, logo em seguida, no do Balde de Cerveja. As duas requisicoes (GET /api/produtos/3 e GET /api/produtos/9) respondem 200 com o corpo certo, mas a de id 3 chega cerca de 2 segundos depois da de id 9. O modal fica com o titulo e a descricao da Fraldinha; a verificacao esperava o Balde de Cerveja. |

Corpo recebido, como veio no caso:

```text
{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/colecao_no_lugar_de_objeto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/colecao_no_lugar_de_objeto.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `relatorio-15` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-15` em `trilha_ineditos.jsonl`, eventos 833 a 858, hash dos eventos `93af00621c521043`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)). Campo: `id`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,91 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê o título e a descrição da Fraldinha no modal, mesmo após clicar no botão do Balde de Cerveja.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu colecao_no_lugar_de_objeto no campo id porque os verbetes entidade-produto, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,04 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/9

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}

ÁRVORE DE ACESSIBILIDADE DA PÁGINA:
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Fraldinha" level=3
      text "Carnes"
      button "R$ 69,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    group
      heading "Balde de Cerveja" level=3
      text "Bebidas"
      button "R$ 45,00"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="9"
  dialog
    button "×" class="close"
    heading "Fraldinha" level=4 id="modalDetalheTitulo"
    text "Corte grelhado na brasa, fatiado na hora" id="modalDetalheCorpo"


SINTOMA OBSERVADO: O roteiro clica em 'Saiba Mais...' da Fraldinha e, logo em seguida, no do Balde de Cerveja. As duas requisicoes (GET /api/produtos/3 e GET /api/produtos/9) respondem 200 com o corpo certo, mas a de id 3 chega cerca de 2 segundos depois da de id 9. O modal fica com o titulo e a descricao da Fraldinha; a verificacao esperava o Balde de Cerveja.

OBSERVAÇÃO ADICIONAL: O corpo mostrado e o da ultima requisicao disparada (id 9); a resposta do id 3 tambem tinha o corpo certo.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> colecao_no_lugar_de_objeto e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,91 contra 0,04; verbete(s) na evidência: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,91 | sim |
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 0,04 |  |
| `tipo_divergente` (Tipo divergente) | 0,03 |  |
| `campo_ausente` (Campo ausente) | 0,01 |  |
| `campo_renomeado` (Campo renomeado) | 0,01 |  |
| `resposta_truncada` (Resposta truncada) | 0,01 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,01 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [colecao_no_lugar_de_objeto]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/colecao_no_lugar_de_objeto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/colecao_no_lugar_de_objeto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto`, `colecao_no_lugar_de_objeto` |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto], [colecao_no_lugar_de_objeto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "colecao_no_lugar_de_objeto"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "colecao_no_lugar_de_objeto"} |
| O verbete citado fala da causa respondida | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 833 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:33:09 | caso relatorio-15 |
| 834 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:33:09 | 3 de 39 verbetes entregues |
| 836 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:33:09 | diagnostico: 4893 caracteres; verbetes entidade-produto, contrato-produto, colecao_no_lugar_de_objeto |
| 838 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:33:09 | diagnostico: 82,3 s |
| 839 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:33:09 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 840 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:33:09 | campo: `id` |
| 841 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:33:09 | impacto: `O usuário vê o título e a descrição da Fraldinha no modal, mesmo após clicar no botão do Balde de Cerveja.` |
| 842 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:33:09 | fonte: `[contrato-produto], [colecao_no_lugar_de_objeto]` |
| 843 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:33:09 | fonte_citada: `contrato-produto` |
| 844 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T14:33:09 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 845 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | quatro_linhas_presentes: confere |
| 846 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | rotulo_no_conjunto: confere |
| 847 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | fonte_existe_na_biblioteca: confere |
| 848 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | fonte_existe_na_biblioteca: confere |
| 849 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | fonte_estava_no_contexto: confere |
| 850 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | fonte_estava_no_contexto: confere |
| 851 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | campo_existe_no_caso: confere |
| 852 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 853 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | notas_nos_verbetes_citados: informativo |
| 854 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | impacto: nao_verificavel |
| 855 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | fonte_formato_valido: confere |
| 856 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | fonte_contem_termo_da_causa: nao_confere |
| 857 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T14:33:09 | fonte_contem_termo_da_causa: confere |
| 858 | 24 | decisao | programa | ao_vivo | 2026-11-06T14:33:09 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 858, decisão `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido.
  - Evidência: evento 834 (verbete_entregue: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto`); evento 838 (resposta); evento 843 (verbete_citado: `contrato-produto`); evento 844 (verbete_citado: `colecao_no_lugar_de_objeto`).
  - Usou: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 833 a 858 da trilha; hash dos eventos deste caso: `93af00621c521043`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-15`

Caso `relatorio-15` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-15`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 24 afirmações (15 observado, 6 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1579 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1579 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4893 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (48,48), `contrato-produto` (35,88) e `colecao_no_lugar_de_objeto` (32,02) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto`, `contrato-produto` e `colecao_no_lugar_de_objeto`; o da entidade, em `entidade-produto`, `contrato-produto` e `colecao_no_lugar_de_objeto` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (30,76), `estado_da_tela_divergente` (29,63), `ancora-saiba-mais` (28,67), `tempo_de_resposta_excedido` (27,29) e `corpo_nao_e_json` (24,08) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 86 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `colecao_no_lugar_de_objeto`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (29,02 contra 28,76), e os reforços em código levaram a diferença a 1,26 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 48,48: 45,48 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 35,88: 32,88 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `colecao_no_lugar_de_objeto` | posição 3, pontuação 32,02: 29,02 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `pagina-produtos-api` | posição 4, pontuação 30,76: 28,76 pelas palavras do caso, mais 2,0 por rota |  |
| `estado_da_tela_divergente` | posição 5, pontuação 29,63: 29,63 pelas palavras do caso, sem reforço |  |
| `ancora-saiba-mais` | posição 6, pontuação 28,67: 28,67 pelas palavras do caso, sem reforço |  |
| `tempo_de_resposta_excedido` | posição 7, pontuação 27,29: 26,29 pelas palavras do caso, mais 1,0 por status |  |
| `corpo_nao_e_json` | posição 8, pontuação 24,08: 23,08 pelas palavras do caso, mais 1,0 por status |  |

## Decisão 3: a causa

Escolha: `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)); segunda: `tempo_de_resposta_excedido`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `colecao_no_lugar_de_objeto` (declarado).
- O modelo apontou o campo `id` (declarado).
- `id` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `tempo_de_resposta_excedido` (Tempo de resposta excedido), ficou com probabilidade 0,044 contra 0,906 da escolhida; nenhum verbete entregue a sustenta (observado).
- As outras 8 alternativas lidas na resposta somam probabilidade 0,056; as maiores: `tipo_divergente` (0,025), `campo_ausente` (0,009) e `campo_renomeado` (0,009) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,906, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/9`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `colecao_no_lugar_de_objeto` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `colecao_no_lugar_de_objeto`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), traz o termo da causa no texto: `contrato-produto` não confere; `colecao_no_lugar_de_objeto` confere (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `contrato-produto` e `colecao_no_lugar_de_objeto` (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/colecao_no_lugar_de_objeto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/colecao_no_lugar_de_objeto.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 10 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `colecao_no_lugar_de_objeto` | 0,906 | `contrato-produto` e `colecao_no_lugar_de_objeto` | sim |
| `tempo_de_resposta_excedido` | 0,044 | nenhum |  |
| `tipo_divergente` | 0,025 | `entidade-produto` e `contrato-produto` |  |
| `campo_ausente` | 0,009 | `contrato-produto` e `colecao_no_lugar_de_objeto` |  |
| `campo_renomeado` | 0,009 | `contrato-produto` |  |
| `resposta_truncada` | 0,007 | nenhum |  |
| `estrutura_aninhada_divergente` | 0,005 | `colecao_no_lugar_de_objeto` |  |
| `formato_de_data_divergente` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê o título e a descrição da Fraldinha no modal, mesmo após clicar no botão do Balde de Cerveja.
> FONTE: [contrato-produto], [colecao_no_lugar_de_objeto]

Resposta inteira:

```text
CAUSA_RAIZ: colecao_no_lugar_de_objeto
CAMPO: id
IMPACTO: O usuário vê o título e a descrição da Fraldinha no modal, mesmo após clicar no botão do Balde de Cerveja.
FONTE: [contrato-produto], [colecao_no_lugar_de_objeto]
```

## Rastro

Gerado dos eventos 833 a 858 da trilha; hash dos eventos deste caso: `93af00621c521043` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-15.md`.
