---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (contrato).
# ! Motivo: campo a campo, com a diferença declarado × real (Decimal no schema, número
# em ponto flutuante no fio). Conferido em schemas.py e produtos.py.
id: contrato-produto
titulo: Contrato de /api/produtos
sistema: CobaiaAPI
entidade_principal: Produto
tipo: contrato
status: ativo
arquivos: [Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaAPI/app/routers/produtos.py]
endpoints: [GET /api/produtos, GET /api/produtos/{id}]
tabelas: [tbprodutos, tbtipos]
sintomas: [chave a mais ou a menos, lista no lugar de objeto, preco como texto]
palavras_chave: [contrato, produtos, id, nome, resumo, tipo, preco, imagem, destaque, lista, objeto, 404, produto nao encontrado]
causas_relacionadas: [campo_ausente, campo_renomeado, colecao_no_lugar_de_objeto, tipo_divergente, recurso_inexistente]
---
## Resumo
GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.

## Sinais
- chave a mais ou a menos: campo ausente ou renomeado
- lista onde se espera objeto, ou o inverso

## Causa
Origem tbprodutos + rótulo de tbtipos (produtos.py _to_dict). preco sai 89.9 (número), embora o schema declare Decimal.
