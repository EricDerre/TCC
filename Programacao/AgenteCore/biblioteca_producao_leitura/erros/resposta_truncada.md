---
# ! Alteração de IA - Revisar: camada de leitura do verbete `resposta_truncada`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/resposta_truncada.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê.
id: resposta_truncada
titulo: Resposta truncada
sistema: CobaiaAPI
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: resposta_truncada
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py]
sintomas: [fim inesperado da entrada, json cortado, content-length menor que o corpo, lista incompleta, ultimo item cortado, corpo cortado]
palavras_chave: [truncad, cortad, incomplet, unexpected end, content-length, tamanho, parcial, malformed_json, truncamento, conexao, proxy]
causas_relacionadas: [corpo_nao_e_json, corpo_vazio, tempo_de_resposta_excedido]
verbete: erros/resposta_truncada.md
hash_do_verbete: 85859fec6984cdb1
gerado_em: 2026-11-07
curado: sim
---

# Resposta truncada

Camada de leitura do verbete `resposta_truncada` (`biblioteca_producao/erros/resposta_truncada.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Infraestrutura. Trata da causa `resposta_truncada` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

O corpo começa como JSON válido e termina no meio de um valor ou chave: faltam bytes; o parse falha com "Unexpected end of JSON input".

## Como aparece na tela

- primeiros itens íntegros, o último cortado ou sem o colchete final.
- Content-Length menor que o esperado.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `fim inesperado da entrada`, `json cortado`, `content-length menor que o corpo`, `lista incompleta`, `ultimo item cortado`, `corpo cortado`.

## O que conferir

Causa, como o verbete a descreve: O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `corpo_nao_e_json` (Corpo não é JSON), `corpo_vazio` (Corpo vazio), `tempo_de_resposta_excedido` (Tempo de resposta excedido).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/routers/produtos.py`, `Programacao/CobaiaAPI/app/fault_injection.py`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `truncad`, `cortad`, `incomplet`, `unexpected end`, `content-length`, `tamanho`, `parcial`, `malformed_json`, `truncamento`, `conexao`, `proxy`.

## Notas do modelo

O verbete que o modelo lê traz 2 notas do modelo. A curadoria de 10/11/2026 as retirou desta leitura; elas continuam em `biblioteca_producao/erros/resposta_truncada.md`.

## Curadoria

Leitura revisada e aprovada. Descrição conceitual precisa sobre truncamento de JSON na camada de rede/proxy e no injetor malformed_json. As duas notas do modelo (época 1) foram retiradas desta leitura para ela ficar curta; continuam no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
