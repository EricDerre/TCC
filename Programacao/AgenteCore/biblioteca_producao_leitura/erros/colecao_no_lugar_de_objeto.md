---
# ! Alteração de IA - Revisar: camada de leitura do verbete `colecao_no_lugar_de_objeto`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/colecao_no_lugar_de_objeto.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê; e a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê.
id: colecao_no_lugar_de_objeto
titulo: Coleção no lugar de objeto (ou o inverso)
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: colecao_no_lugar_de_objeto
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_api.php]
endpoints: [GET /api/produtos, GET /api/produtos/{id}]
sintomas: [detalhe sem preencher campos, colchetes ao redor do valor, nenhum produto retornado]
palavras_chave: [lista, array, colecao, objeto, unico, recurso, colchetes, detalhe, modal, formato_de_resposta, estrutura_json]
causas_relacionadas: [estrutura_aninhada_divergente, campo_ausente]
verbete: erros/colecao_no_lugar_de_objeto.md
hash_do_verbete: 3e7b1dd07feb6a78
gerado_em: 2026-11-07
curado: sim
---

# Coleção no lugar de objeto (ou o inverso)

Camada de leitura do verbete `colecao_no_lugar_de_objeto` (`biblioteca_producao/erros/colecao_no_lugar_de_objeto.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Produto. Trata da causa `colecao_no_lugar_de_objeto` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (["Carnes"]).

## Como aparece na tela

- modal "Produto #1"/"(sem descrição)": p é lista.
- categoria com colchetes: campo veio como lista.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `detalhe sem preencher campos`, `colchetes ao redor do valor`, `nenhum produto retornado`.

## O que conferir

Causa, como o verbete a descreve: GET /api/produtos devolve lista, GET /api/produtos/{id} objeto (produtos.py); a página não confere a forma antes de ler os campos.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `estrutura_aninhada_divergente` (Estrutura aninhada divergente), `campo_ausente` (Campo ausente).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/routers/produtos.py`, `Programacao/CobaiaFront/produtos_api.php`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`, `GET /api/produtos/{id}`.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `lista`, `array`, `colecao`, `objeto`, `unico`, `recurso`, `colchetes`, `detalhe`, `modal`, `formato_de_resposta`, `estrutura_json`.

## Notas do modelo

O verbete que o modelo lê traz 2 notas do modelo. A curadoria de 10/11/2026 as retirou desta leitura; elas continuam em `biblioteca_producao/erros/colecao_no_lugar_de_objeto.md`.

## Curadoria

Leitura revisada e aprovada. Descrições estruturais mantidas. As duas notas do modelo (épocas 1 e 101) sobre o tratamento do campo `tipo` foram retiradas desta leitura; continuam no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
