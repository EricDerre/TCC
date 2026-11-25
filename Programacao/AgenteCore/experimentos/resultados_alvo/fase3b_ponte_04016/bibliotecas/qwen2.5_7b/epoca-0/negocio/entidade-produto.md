---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (regra de negócio).
# ! Motivo: dá ao modelo o que o contrato de campos não diz — de onde cada campo vem e
# como é traduzido entre banco e API. Conferido em models.py, produtos.py e seed.sql.
id: entidade-produto
titulo: Produto e sua categoria
sistema: Ambos
entidade_principal: Produto
tipo: funcionamento
status: ativo
arquivos: [Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/banco/seed.sql]
endpoints: [GET /api/produtos, GET /api/produtos/{id}]
tabelas: [tbprodutos, tbtipos]
sintomas: [nome da categoria no titulo do cartao, preco com grandeza estranha]
palavras_chave: [produto, categoria, tipo, preco, destaque, imagem, resumo, cardapio, picanha]
causas_relacionadas: [chave_de_juncao_errada, escala_ou_unidade_errada, tipo_divergente]
---
## Resumo
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90.

## Sinais
- título com nome de categoria: junção trocada
- preço com grandeza estranha: conversão de valor_produto

## Causa
valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.
