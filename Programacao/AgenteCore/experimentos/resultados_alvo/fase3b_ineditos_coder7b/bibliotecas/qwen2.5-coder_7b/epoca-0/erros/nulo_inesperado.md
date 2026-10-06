---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: aponta as duas origens legítimas de nulo (colunas nullable e LEFT JOIN da
# view) e o campo que NÃO pode vir nulo pelo código; conferido em models.py e na view.
id: nulo_inesperado
titulo: Nulo inesperado
sistema: Ambos
entidade_principal: Pedido
tipo: erro
status: ativo
causa_raiz: nulo_inesperado
arquivos: [Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaFront/banco/schema_completo.sql, Programacao/CobaiaAPI/app/routers/produtos.py]
endpoints: [GET /api/produtos, GET /api/pedidos]
tabelas: [tbprodutos, vw_tbpedidos]
sintomas: [null onde havia valor, saudacao vazia, R$ 0,00 para produto com preco, produto some do filtro]
palavras_chave: [nulo, null, None, vazio, nullable, saudacao, Ola, left join, view]
causas_relacionadas: [campo_ausente, valor_fora_do_dominio, chave_de_juncao_errada]
---
## Resumo
A chave existe e vem null onde o contrato promete valor. Diferente de campo_ausente: a chave está lá.

## Sinais
- nome nulo: "Olá, !" na área do cliente; preco nulo: cartão sem valor
- tipo nulo: produto some de filtros por categoria

## Causa
Origens legítimas: resumo, valor_produto e imagem_produto são nullable (models.py:33-35) e vw_tbpedidos faz LEFT JOIN. tipo nulo não sai de produtos.py (p.tipo.rotulo_tipo).
