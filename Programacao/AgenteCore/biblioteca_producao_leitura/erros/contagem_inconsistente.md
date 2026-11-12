---
# ! Alteração de IA - Revisar: camada de leitura do verbete `contagem_inconsistente`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/contagem_inconsistente.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê.
id: contagem_inconsistente
titulo: Contagem inconsistente
sistema: Ambos
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: contagem_inconsistente
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_destaque.php]
endpoints: [GET /api/produtos]
tabelas: [tbprodutos]
sintomas: [total diferente dos itens, pagina vazia com total positivo, quatro destaques mas cinco cartoes, menos itens na interface, lista crua sem total]
palavras_chave: [contagem, total, itens, pagina, paginacao, quantidade, destaques, inconsistente, zero, lista]
causas_relacionadas: [estrutura_aninhada_divergente, dado_desatualizado, estado_da_tela_divergente]
verbete: erros/contagem_inconsistente.md
hash_do_verbete: 56cfc121b9ed4873
gerado_em: 2026-11-07
curado: sim
---

# Contagem inconsistente

Camada de leitura do verbete `contagem_inconsistente` (`biblioteca_producao/erros/contagem_inconsistente.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Produto. Trata da causa `contagem_inconsistente` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

Dois números que deveriam bater não batem: total 14 e lista com 1; total 0 com itens; página 2 vazia com total 14; contador de destaques diferente dos cartões.

## Como aparece na tela

- total e lista vêm de consultas diferentes.
- rótulo numérico que não corresponde ao renderizado.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `total diferente dos itens`, `pagina vazia com total positivo`, `quatro destaques mas cinco cartoes`, `menos itens na interface`, `lista crua sem total`.

## O que conferir

Causa, como o verbete a descreve: GET /api/produtos devolve a lista crua, sem total nem paginação (produtos.py:34-43); o seed tem 14 produtos, 5 em destaque. Envelope com total indica outra versão.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `estrutura_aninhada_divergente` (Estrutura aninhada divergente), `dado_desatualizado` (Dado desatualizado (cache)), `estado_da_tela_divergente` (Estado da tela divergente da resposta).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/routers/produtos.py`, `Programacao/CobaiaFront/produtos_destaque.php`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`.
- Tabelas do banco: `tbprodutos`.
- Palavras que a busca usa para achar este verbete: `contagem`, `total`, `itens`, `pagina`, `paginacao`, `quantidade`, `destaques`, `inconsistente`, `zero`, `lista`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/contagem_inconsistente.md`.

## Curadoria

Leitura revisada e aprovada. Descrição base clara e sintomática, diferenciando metadados de listas não envelopadas. A nota do modelo (época 101), que pedia para incluir o total na resposta da API, foi retirada desta leitura; continua no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
