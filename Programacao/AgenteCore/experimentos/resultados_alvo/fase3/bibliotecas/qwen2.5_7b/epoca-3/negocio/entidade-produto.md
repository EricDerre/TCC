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
sintomas: [nome da categoria no titulo do cartao, preco com grandeza estranha, nulo_inesperado, escala_ou_unidade_errada, preco cru, separador decimal como virgula, incorreto, tipo errado]
palavras_chave: [produto, categoria, tipo, preco, destaque, imagem, resumo, cardapio, picanha, convercao, valor, formatacao, decimal, separador]
causas_relacionadas: [chave_de_juncao_errada, escala_ou_unidade_errada, tipo_divergente]
# ! Alteração por modelo qwen2.5:7b (E1, caso sin-1) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5:7b (E1, caso semt-13) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E2, caso tra-3) - Revisar: retificação acrescentada.
---
## Resumo
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90.

## Sinais
- título com nome de categoria: junção trocada
- preço com grandeza estranha: conversão de valor_produto

## Causa
valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.

## Notas do modelo
- [E1 · sin-1 · retificação de "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano."] Corrigir a conversão do preço e destaque no _to_dict de produtos.py. — Motivo: O caso mostrou que a conversão incorreta de tipos pode levar a sintomas como 'undefined' e '89.9', indicando uma necessidade de revisão na conversão de tipos.
- [E1 · semt-13 · nota] Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. — Motivo: O caso demonstra a importância de uma formatação correta do preço, independentemente da conversão do backend.
- [E2 · tra-3 · retificação de "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano."] Corrigir a conversão do preço e destaque no _to_dict de produtos.py, garantindo que o preço seja convertido corretamente para Decimal. — Motivo: O caso mostrou que a conversão incorreta do tipo de dado no backend afeta a apresentação do produto no frontend, evidenciando a necessidade de manter a consistência dos tipos de dados.
