---
# ! Alteração de IA - Revisar: camada de leitura do verbete `estrutura_aninhada_divergente`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/estrutura_aninhada_divergente.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê; e a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê.
id: estrutura_aninhada_divergente
titulo: Estrutura aninhada divergente
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: estrutura_aninhada_divergente
arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/schemas.py]
endpoints: [GET /api/produtos]
sintomas: [object Object, envelope data, lista dentro de objeto, campo virou objeto, envelope na raiz, campo como objeto]
palavras_chave: [aninhad, envelope, data, itens, objeto, nivel, profundidade, object Object, stringify, estrutura, aninhamento, divergencia]
causas_relacionadas: [colecao_no_lugar_de_objeto, campo_renomeado, contagem_inconsistente]
verbete: erros/estrutura_aninhada_divergente.md
hash_do_verbete: 7feba362636e1ed6
gerado_em: 2026-11-07
curado: sim
---

# Estrutura aninhada divergente

Camada de leitura do verbete `estrutura_aninhada_divergente` (`biblioteca_producao/erros/estrutura_aninhada_divergente.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Produto. Trata da causa `estrutura_aninhada_divergente` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

Chaves existem, mas noutro nível: lista num envelope ({"data": {"itens": [...]}}) ou campo simples como objeto ({"id": 1, "nome": "Carnes"}).

## Como aparece na tela

- envelope na raiz: Array.isArray falha, "Nenhum produto retornado".
- campo como objeto: cartão imprime [object Object].

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `object Object`, `envelope data`, `lista dentro de objeto`, `campo virou objeto`, `envelope na raiz`, `campo como objeto`.

## O que conferir

Causa, como o verbete a descreve: Contrato real: lista crua na raiz e tipo como texto (produtos.py _to_dict); envelope ou aninhamento veio de outra versão ou intermediário.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)), `campo_renomeado` (Campo renomeado), `contagem_inconsistente` (Contagem inconsistente).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/produtos_api.php`, `Programacao/CobaiaAPI/app/schemas.py`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `aninhad`, `envelope`, `data`, `itens`, `objeto`, `nivel`, `profundidade`, `object Object`, `stringify`, `estrutura`, `aninhamento`, `divergencia`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/estrutura_aninhada_divergente.md`.

## Curadoria

Leitura revisada e aprovada. Descrição conceitual focada nas anomalias geradas por serialização JSON inesperada, como envelopamento (data) e parse defeituoso ([object Object]). A nota do modelo foi retirada desta leitura por repetir o que o texto já diz; continua no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
