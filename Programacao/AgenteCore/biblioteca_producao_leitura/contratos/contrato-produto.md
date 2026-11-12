---
# ! Alteração de IA - Revisar: camada de leitura do verbete `contrato-produto`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/contratos/contrato-produto.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota não dizia que o texto do modelo saiu só desta leitura e continua no verbete que o modelo lê.
id: contrato-produto
titulo: Contrato de /api/produtos
sistema: CobaiaAPI
entidade_principal: Produto
tipo: contrato
status: ativo
arquivos: [Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaAPI/app/routers/produtos.py]
endpoints: [GET /api/produtos, GET /api/produtos/{id}]
tabelas: [tbprodutos, tbtipos]
sintomas: [chave a mais ou a menos, lista no lugar de objeto, preco como texto, lista incompleta, ultimo item cortado]
palavras_chave: [contrato, produtos, id, nome, resumo, tipo, preco, imagem, destaque, lista, objeto, 404, produto nao encontrado, schema, json]
causas_relacionadas: [campo_ausente, campo_renomeado, colecao_no_lugar_de_objeto, tipo_divergente, recurso_inexistente]
verbete: contratos/contrato-produto.md
hash_do_verbete: b5555a711e214495
gerado_em: 2026-11-07
curado: sim
---

# Contrato de /api/produtos

Camada de leitura do verbete `contrato-produto` (`biblioteca_producao/contratos/contrato-produto.md`). Tipo: contrato (o contrato de uma rota da API, campo a campo); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Produto.

## O que é

GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.

## Como aparece na tela

- chave a mais ou a menos: campo ausente ou renomeado.
- lista onde se espera objeto, ou o inverso.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `chave a mais ou a menos`, `lista no lugar de objeto`, `preco como texto`, `lista incompleta`, `ultimo item cortado`.

## O que conferir

Causa, como o verbete a descreve: Origem tbprodutos + rótulo de tbtipos (produtos.py _to_dict). preco sai 89.9 (número), embora o esquema de validação do código (schema Pydantic) declare Decimal.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `campo_ausente` (Campo ausente), `campo_renomeado` (Campo renomeado), `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)), `tipo_divergente` (Tipo divergente), `recurso_inexistente` (Recurso inexistente (404 e vizinhos)).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/schemas.py`, `Programacao/CobaiaAPI/app/routers/produtos.py`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`, `GET /api/produtos/{id}`.
- Tabelas do banco: `tbprodutos`, `tbtipos`.
- Palavras que a busca usa para achar este verbete: `contrato`, `produtos`, `id`, `nome`, `resumo`, `tipo`, `preco`, `imagem`, `destaque`, `lista`, `objeto`, `404`, `produto nao encontrado`, `schema`, `json`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/contratos/contrato-produto.md`.

## Curadoria

Leitura revisada e aprovada. O termo "schema" foi contextualizado na primeira menção para satisfazer os critérios do filtro Q2. A nota do modelo sobre o truncamento de resposta foi retirada desta leitura, para ela ficar só com as regras do contrato; continua no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
