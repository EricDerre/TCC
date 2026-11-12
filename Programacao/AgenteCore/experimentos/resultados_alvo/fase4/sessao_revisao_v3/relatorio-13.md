<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão (--check regera e compara).
     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a página da sessão de 05/11/2026 já escondia o nome. -->
# Relatório 13 de 36 (sessão de revisão)

Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; nada aqui diz o resultado do caso.

---
<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Dado desatualizado (cache) em `GET /api/produtos/2`, campo `preco`

Caso `relatorio-13` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/relatorio-13`: o caso `relatorio-13` na corrida `fase4_ineditos`; eventos 860 a 885 da trilha `trilha_ineditos.jsonl`, hash dos eventos `624dd17b154dd46a` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Dado desatualizado (cache) em `GET /api/produtos/2`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 14:34:36 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/2` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `relatorio-13`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe e nível omitidos nesta sessão (dizem a família do defeito). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/2`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 94.9, "imagem": "picanha_sem.jpg", "destaque": false}
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
      heading "Picanha ao Alho" level=3
      text "Carnes"
      button "R$ 89,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      button "R$ 84,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
```

4. Sintoma observado (texto do caso):

> A pagina foi aberta as 10:00 e mostrou a Picanha Simples por 'R$ 84,90'. As 10:05 o preco desse produto foi alterado no banco para 94,90. As 10:07 o roteiro consultou GET /api/produtos/2, que respondeu 200 com preco 94.9, e comparou com o cartao, que continua mostrando 'R$ 84,90'.

5. Observação adicional (texto do caso):

> A pagina nao foi recarregada entre as 10:00 e as 10:07.


## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/2` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A pagina foi aberta as 10:00 e mostrou a Picanha Simples por 'R$ 84,90'. As 10:05 o preco desse produto foi alterado no banco para 94,90. As 10:07 o roteiro consultou GET /api/produtos/2, que respondeu 200 com preco 94.9, e comparou com o cartao, que continua mostrando 'R$ 84,90'. |

Corpo recebido, como veio no caso:

```text
{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 94.9, "imagem": "picanha_sem.jpg", "destaque": false}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe e nível omitidos nesta sessão (dizem a família do defeito).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe e nível omitidos nesta sessão (dizem a família do defeito). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `relatorio-13` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/relatorio-13` em `trilha_ineditos.jsonl`, eventos 860 a 885, hash dos eventos `624dd17b154dd46a`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `dado_desatualizado` (Dado desatualizado (cache)). Campo: `preco`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,87 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê um preço antigo no cartão, enquanto a página exibe o preço atualizado.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu dado_desatualizado no campo preco porque os verbetes entidade-produto, contrato-produto, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,08. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida dado_desatualizado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida dado_desatualizado.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/2

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 94.9, "imagem": "picanha_sem.jpg", "destaque": false}

ÁRVORE DE ACESSIBILIDADE DA PÁGINA:
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Picanha ao Alho" level=3
      text "Carnes"
      button "R$ 89,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      button "R$ 84,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"


SINTOMA OBSERVADO: A pagina foi aberta as 10:00 e mostrou a Picanha Simples por 'R$ 84,90'. As 10:05 o preco desse produto foi alterado no banco para 94,90. As 10:07 o roteiro consultou GET /api/produtos/2, que respondeu 200 com preco 94.9, e comparou com o cartao, que continua mostrando 'R$ 84,90'.

OBSERVAÇÃO ADICIONAL: A pagina nao foi recarregada entre as 10:00 e as 10:07.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> dado_desatualizado e não valor_fora_do_dominio: a escolha tem probabilidade 0,87 contra 0,08; verbete(s) na evidência: entidade-produto, contrato-produto, nulo_inesperado

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `dado_desatualizado` (Dado desatualizado (cache)) | 0,87 | sim |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,08 |  |
| `nulo_inesperado` (Nulo inesperado) | 0,02 |  |
| `campo_ausente` (Campo ausente) | 0,01 |  |
| `campo_renomeado` (Campo renomeado) | 0,01 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `registro_duplicado` (Registro duplicado) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [nulo_inesperado]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `dado_desatualizado` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto], [nulo_inesperado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "nulo_inesperado"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "dado_desatualizado"} |
| O verbete citado fala da causa respondida | `nulo_inesperado` | não confere | {"termo": "dado_desatualizado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.


## 17. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 860 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:34:36 | caso relatorio-13 |
| 861 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:34:36 | 3 de 39 verbetes entregues |
| 863 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:34:36 | diagnostico: 4207 caracteres; verbetes entidade-produto, contrato-produto, nulo_inesperado |
| 865 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:34:36 | diagnostico: 67,6 s |
| 866 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:34:36 | causa_raiz: `dado_desatualizado` |
| 867 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:34:36 | campo: `preco` |
| 868 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:34:36 | impacto: `O usuário vê um preço antigo no cartão, enquanto a página exibe o preço atualizado.` |
| 869 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:34:36 | fonte: `[contrato-produto], [nulo_inesperado]` |
| 870 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:34:36 | fonte_citada: `contrato-produto` |
| 871 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T14:34:36 | fonte_citada: `nulo_inesperado` |
| 872 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | quatro_linhas_presentes: confere |
| 873 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | rotulo_no_conjunto: confere |
| 874 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | fonte_existe_na_biblioteca: confere |
| 875 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | fonte_existe_na_biblioteca: confere |
| 876 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | fonte_estava_no_contexto: confere |
| 877 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | fonte_estava_no_contexto: confere |
| 878 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | campo_existe_no_caso: confere |
| 879 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 880 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | notas_nos_verbetes_citados: informativo |
| 881 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | impacto: nao_verificavel |
| 882 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | fonte_formato_valido: confere |
| 883 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | fonte_contem_termo_da_causa: nao_confere |
| 884 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T14:34:36 | fonte_contem_termo_da_causa: nao_confere |
| 885 | 24 | decisao | programa | ao_vivo | 2026-11-06T14:34:36 | diagnostico: escolha dado_desatualizado; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 885, decisão `diagnostico`: escolha `dado_desatualizado`; resultado rotulo_emitido.
  - Evidência: evento 861 (verbete_entregue: `entidade-produto`, `contrato-produto`, `nulo_inesperado`); evento 865 (resposta); evento 870 (verbete_citado: `contrato-produto`); evento 871 (verbete_citado: `nulo_inesperado`).
  - Usou: `entidade-produto`, `contrato-produto`, `nulo_inesperado`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 860 a 885 da trilha; hash dos eventos deste caso: `624dd17b154dd46a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.

---

<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que eventos ela saiu. -->
# Árvore de decisão do caso `relatorio-13`

Caso `relatorio-13` da corrida `fase4_ineditos`, trilha `fase4_ineditos/qwen2.5_7b/relatorio-13`, modelo `qwen2.5:7b`. Um bloco por decisão do agente, na ordem em que aconteceram. Cada frase termina com a origem entre parênteses: observado (o código mediu); conferido (o código checou o que o modelo disse); declarado (o modelo escreveu, sem garantia); desconhecido (faltou dado; nunca vira percentual). As linhas escritas pelo modelo ficam no bloco "Texto do modelo", no fim.

Resumo: 3 decisões e 25 afirmações (15 observado, 7 conferido, 3 declarado); há divergência entre o declarado e o conferido; confiança média.

## Decisão 1: o que o modelo lê

Escolha: ler o caso escrito inteiro, como veio (1306 caracteres).

- O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito (1306 caracteres) (observado).
- O texto entregue ao modelo, com os verbetes da decisão 2, tem 4207 caracteres (observado).

## Decisão 2: que verbetes entram

Escolha: entregar ao modelo os 3 verbetes mais bem pontuados pela busca.

- A busca pontuou 39 verbetes da biblioteca e entregou os 3 primeiros: `entidade-produto` (52,85), `contrato-produto` (33,22) e `nulo_inesperado` (32,80) (observado).
- A pontuação soma a busca por palavras no texto do caso e os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status): o reforço da rota entrou em `entidade-produto` e `contrato-produto`; o da entidade, em `entidade-produto` e `contrato-produto`; `nulo_inesperado` pontuou só pelas palavras (observado).
- Ficaram de fora 36 verbetes; os mais perto de entrar: `pagina-produtos-api` (28,94), `estado_da_tela_divergente` (26,25), `tipo_divergente` (25,02), `estrutura_aninhada_divergente` (24,89) e `tempo_de_resposta_excedido` (23,85) (observado).
- Sinais da consulta, tirados do caso em código: rota `GET /api/produtos/{id}`, entidade `Produto`, status 200 e 77 termos de busca, vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato (observado).
- Entre o último entregue, `nulo_inesperado`, e o primeiro de fora, `pagina-produtos-api`, só o texto do caso já punha o primeiro à frente (32,80 contra 26,94); a diferença final foi 3,86 (observado).

| Alternativa | Detalhe | Escolhida |
|---|---|---|
| `entidade-produto` | posição 1, pontuação 52,85: 49,85 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `contrato-produto` | posição 2, pontuação 33,22: 30,22 pelas palavras do caso, mais 2,0 por rota e 1,0 por entidade | sim |
| `nulo_inesperado` | posição 3, pontuação 32,80: 32,80 pelas palavras do caso, sem reforço | sim |
| `pagina-produtos-api` | posição 4, pontuação 28,94: 26,94 pelas palavras do caso, mais 2,0 por rota |  |
| `estado_da_tela_divergente` | posição 5, pontuação 26,25: 26,25 pelas palavras do caso, sem reforço |  |
| `tipo_divergente` | posição 6, pontuação 25,02: 24,02 pelas palavras do caso, mais 1,0 por entidade |  |
| `estrutura_aninhada_divergente` | posição 7, pontuação 24,89: 23,89 pelas palavras do caso, mais 1,0 por entidade |  |
| `tempo_de_resposta_excedido` | posição 8, pontuação 23,85: 22,85 pelas palavras do caso, mais 1,0 por status |  |

## Decisão 3: a causa

Escolha: `dado_desatualizado` (Dado desatualizado (cache)); segunda: `valor_fora_do_dominio`; confiança média.

- A linha CAUSA_RAIZ da resposta diz `dado_desatualizado` (declarado).
- O modelo apontou o campo `preco` (declarado).
- `preco` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): confere (conferido).
- A segunda causa, `valor_fora_do_dominio` (Valor fora do domínio), ficou com probabilidade 0,075 contra 0,875 da escolhida; verbetes entregues que a sustentam: `nulo_inesperado` (observado).
- As outras 12 alternativas lidas na resposta somam probabilidade 0,052; as maiores: `nulo_inesperado` (0,024), `campo_ausente` (0,009) e `campo_renomeado` (0,009) (observado).
- Confiança média: a probabilidade lida na causa respondida foi 0,875, e a faixa média vai de 0,832 a 0,990 (cortes fixados na calibração) (observado).
- Na corrida de calibração (`fase4_calibracao`), dos 26 casos que caíram na faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).
- Gatilhos de revisão humana: probabilidade baixa não disparou; FONTE divergente disparou; amostra fixa não disparou (observado).
- Nenhuma intervenção rodou neste caso (modo `desligadas`) (observado).
- Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `GET /api/produtos/2`, o status 200 (a API respondeu sem código de erro) e o corpo como estavam no caso escrito (observado).
- A linha FONTE cita `contrato-produto` e `nulo_inesperado` (declarado).
- Os 2 verbetes citados (`contrato-produto` e `nulo_inesperado`): existem na biblioteca (confere), estavam entre os entregues ao modelo (confere), nenhum traz o termo da causa no texto (não confere) (conferido).
- A FONTE veio no formato pedido, só identificadores entre colchetes (conferido).
- Nenhum dos verbetes entregues é sobre essa causa (conferido).
- Camada de leitura de cada verbete citado: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `nulo_inesperado` (Nulo inesperado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/nulo_inesperado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/nulo_inesperado.md`) (observado).
- O declarado pelo modelo diverge do conferido pelo código (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida dado_desatualizado (conferido).
- Falha registrada no nó: `causa_sem_verbete_que_a_trate` (a causa respondida não é tratada por nenhum dos verbetes entregues; origem na taxonomia da trilha: modelo) (conferido).
- Conferências em código com veredito: 8 de 11 conferem; a frase de impacto não tem como ser conferida por código (conferido).

| Alternativa | Probabilidade lida na causa | Verbetes entregues que a tratam | Escolhida |
|---|---|---|---|
| `dado_desatualizado` | 0,875 | nenhum | sim |
| `valor_fora_do_dominio` | 0,075 | `nulo_inesperado` |  |
| `nulo_inesperado` | 0,024 | `nulo_inesperado` |  |
| `campo_ausente` | 0,009 | `contrato-produto` e `nulo_inesperado` |  |
| `campo_renomeado` | 0,009 | `contrato-produto` |  |
| `formato_de_data_divergente` | 0,004 | nenhum |  |
| `tipo_divergente` | 0,002 | `entidade-produto` e `contrato-produto` |  |
| `tempo_de_resposta_excedido` | 0,002 | nenhum |  |
| `resposta_truncada` | 0,001 | nenhum |  |
| `registro_duplicado` | 0,001 | nenhum |  |
| `escala_ou_unidade_errada` | 0,000 | `entidade-produto` |  |
| `estado_da_tela_divergente` | 0,000 | nenhum |  |
| `corpo_nao_e_json` | 0,000 | nenhum |  |
| `corpo_vazio` | 0,000 | nenhum |  |

## Texto do modelo

As linhas escritas pelo modelo, como vieram e sem garantia (texto do modelo):

> IMPACTO: O usuário vê um preço antigo no cartão, enquanto a página exibe o preço atualizado.
> FONTE: [contrato-produto], [nulo_inesperado]

Resposta inteira:

```text
CAUSA_RAIZ: dado_desatualizado
CAMPO: preco
IMPACTO: O usuário vê um preço antigo no cartão, enquanto a página exibe o preço atualizado.
FONTE: [contrato-produto], [nulo_inesperado]
```

## Rastro

Gerado dos eventos 860 a 885 da trilha; hash dos eventos deste caso: `624dd17b154dd46a` (a impressão digital destes eventos: muda se um byte deles mudar). Relatório de defeito do mesmo caso: `../relatorios_v3/relatorio-13.md`.
