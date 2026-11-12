<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 22 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Localizador (seletor) quebrado em `GET /api/produtos/3`

Caso `relatorio-22` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-22`: o caso `relatorio-22` na corrida `fase4_ineditos`; eventos 810 a 831 da trilha `trilha_ineditos.jsonl`, hash dos eventos `26088ac9bd4c3c76` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Localizador (seletor) quebrado em `GET /api/produtos/3`

## 3. Data, organização e autor

Observado em 06/11/2026 14:32:06 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/3` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-22`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/3`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}
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
      heading "Costelona" level=3
      text "Carnes"
      button "R$ 79,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="4"
  dialog
    button "×" class="close"
    heading "Fraldinha" level=4 id="modalDetalheTitulo"
    text "Corte grelhado na brasa, fatiado na hora" id="modalDetalheCorpo"
```

Seletor que falhou: `#modalDetalhe .modal-title`.
4. Sintoma observado (texto do caso):

> Depois do clique em 'Saiba Mais...' da Fraldinha, o modal aparece na tela com o titulo 'Fraldinha', mas a verificacao do roteiro, que le o texto de '#modalDetalhe.modal-title', esgota o tempo sem encontrar o elemento. GET /api/produtos/3 respondeu 200 com os dados certos.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/3` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Depois do clique em 'Saiba Mais...' da Fraldinha, o modal aparece na tela com o titulo 'Fraldinha', mas a verificacao do roteiro, que le o texto de '#modalDetalhe.modal-title', esgota o tempo sem encontrar o elemento. GET /api/produtos/3 respondeu 200 com os dados certos. |

Corpo recebido, como veio no caso:

```text
{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).
- Verbetes entregues pela busca e não citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `relatorio-22` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-22` em `trilha_ineditos.jsonl`, eventos 810 a 831, hash dos eventos `26088ac9bd4c3c76`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `localizador_quebrado` (Localizador (seletor) quebrado). Campo: nenhum apontado. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,96 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário não consegue visualizar o detalhe do produto corretamente, pois o modal não carrega o título esperado.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, estado_da_tela_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/3

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}

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
      heading "Costelona" level=3
      text "Carnes"
      button "R$ 79,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="4"
  dialog
    button "×" class="close"
    heading "Fraldinha" level=4 id="modalDetalheTitulo"
    text "Corte grelhado na brasa, fatiado na hora" id="modalDetalheCorpo"


SELETOR QUE FALHOU: #modalDetalhe .modal-title

SINTOMA OBSERVADO: Depois do clique em 'Saiba Mais...' da Fraldinha, o modal aparece na tela com o titulo 'Fraldinha', mas a verificacao do roteiro, que le o texto de '#modalDetalhe .modal-title', esgota o tempo sem encontrar o elemento. GET /api/produtos/3 respondeu 200 com os dados certos.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> localizador_quebrado e não estado_da_tela_divergente: a escolha tem probabilidade 0,96 contra 0,00; verbete(s) na evidência: localizador_quebrado, contrato-produto, entidade-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `localizador_quebrado` (Localizador (seletor) quebrado) | 0,96 | sim |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| A linha FONTE só tem identificadores, no formato pedido | `[localizador_quebrado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["localizador_quebrado"]} |
| O verbete citado fala da causa respondida | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 810 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:32:06 | caso relatorio-22 |
| 811 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:32:06 | 3 de 39 verbetes entregues |
| 813 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:32:06 | diagnostico: 4610 caracteres; verbetes localizador_quebrado, contrato-produto, entidade-produto |
| 815 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:32:06 | diagnostico: 58,7 s |
| 816 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:32:06 | causa_raiz: `localizador_quebrado` |
| 817 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:32:06 | campo: `nenhum` |
| 818 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:32:06 | impacto: `O usuário não consegue visualizar o detalhe do produto corretamente, pois o modal não carrega o título esperado.` |
| 819 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:32:06 | fonte: `[localizador_quebrado]` |
| 820 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:32:06 | fonte_citada: `localizador_quebrado` |
| 821 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:32:06 | quatro_linhas_presentes: confere |
| 822 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:32:06 | rotulo_no_conjunto: confere |
| 823 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:32:06 | fonte_existe_na_biblioteca: confere |
| 824 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:32:06 | fonte_estava_no_contexto: confere |
| 825 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:32:06 | campo_existe_no_caso: nao_se_aplica |
| 826 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:32:06 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 827 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:32:06 | notas_nos_verbetes_citados: informativo |
| 828 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:32:06 | impacto: nao_verificavel |
| 829 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:32:06 | fonte_formato_valido: confere |
| 830 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:32:06 | fonte_contem_termo_da_causa: confere |
| 831 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:32:06 | diagnostico: escolha localizador_quebrado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 831, decisão `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido.
  - Evidência: evento 811 (verbete_entregue: `localizador_quebrado`, `contrato-produto`, `entidade-produto`); evento 815 (resposta); evento 820 (verbete_citado: `localizador_quebrado`).
  - Usou: `localizador_quebrado`, `contrato-produto`, `entidade-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 810 a 831 da trilha; hash dos eventos deste caso: `26088ac9bd4c3c76`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-22`

Caso `relatorio-22` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-22`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 23 afirmações (15 observado, 5 conferido, 3 declarado); nenhuma divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1427 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1427 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4610 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `localizador_quebrado` (43,18), `contrato-produto` (27,62) e `entidade-produto` (27,19) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `contrato-produto` e `entidade-produto`; o da entidade, em `localizador_quebrado` (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `estado_da_tela_divergente` (26,90), `ancora-saiba-mais` (25,99), `pagina-produtos-api` (21,85), `campo_ausente` (19,83) e `dado_desatualizado` (18,06) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Interface`, status 200 e 67 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `entidade-produto`, e o primeiro de fora, `estado_da_tela_divergente`, só pelo texto do caso o segundo estaria à frente (25,90 contra 25,19); os reforços em código viraram a ordem, com diferença final de 0,29 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `localizador_quebrado` | posição 1, pontuação 43,18: 42,18 pelas palavras do caso, mais 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 27,62: 25,62 pelas palavras do caso, mais 2,0 por rota | sim |
| `entidade-produto` | posição 3, pontuação 27,19: 25,19 pelas palavras do caso, mais 2,0 por rota | sim |
| `estado_da_tela_divergente` | posição 4, pontuação 26,90: 25,90 pelas palavras do caso, mais 1,0 por entidade |  |
| `ancora-saiba-mais` | posição 5, pontuação 25,99: 24,99 pelas palavras do caso, mais 1,0 por entidade |  |
| `pagina-produtos-api` | posição 6, pontuação 21,85: 18,85 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade |  |
| `campo_ausente` | posição 7, pontuação 19,83: 19,83 pelas palavras do caso, sem reforço |  |
| `dado_desatualizado` | posição 8, pontuação 18,06: 17,06 pelas palavras do caso, mais 1,0 por status |  |

## Decisão 3: a causa

Escolha: `localizador_quebrado` (Localizador (seletor) quebrado); segunda: `estado_da_tela_divergente`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `localizador_quebrado` (declarado).
- O modelo não apontou campo (linha CAMPO: nenhum) (declarado).
- A segunda causa, `estado_da_tela_divergente` (Estado da tela divergente da resposta), ficou com probabilidade 0,000 contra 0,959 da escolhida; verbetes entregues que a sustentam: `localizador_quebrado` (observado).
- As outras 2 alternativas lidas na resposta somam probabilidade 0,000; as maiores: `campo_ausente` (0,000) e `campo_renomeado` (0,000) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,959, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente não disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/3`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `localizador_quebrado` (declarado).
- Verbete citado `localizador_quebrado`: existe na biblioteca (confere), estava entre os entregues ao modelo (confere), traz o termo da causa no texto (confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Há verbete entregue sobre essa causa: `localizador_quebrado` (conferido).
- Leitura do verbete `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`) (observado).
- Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código (conferido).
- Conferências em código com veredito: 7 de 7 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `localizador_quebrado` | 0,959 | `localizador_quebrado` | sim |
| `estado_da_tela_divergente` | 0,000 | `localizador_quebrado` |  |
| `campo_ausente` | 0,000 | `contrato-produto` |  |
| `campo_renomeado` | 0,000 | `contrato-produto` |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário não consegue visualizar o detalhe do produto corretamente, pois o modal não carrega o título esperado.
> FONTE: [localizador_quebrado]

Resposta inteira:

```text
CAUSA_RAIZ: localizador_quebrado
CAMPO: nenhum
IMPACTO: O usuário não consegue visualizar o detalhe do produto corretamente, pois o modal não carrega o título esperado.
FONTE: [localizador_quebrado]
```

## Rastro

Gerado dos eventos 810 a 831 da trilha; hash dos eventos deste caso: `26088ac9bd4c3c76` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-22.md`.
