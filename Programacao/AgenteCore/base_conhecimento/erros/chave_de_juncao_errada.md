---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: registra as junções reais (FK de tipo e de cliente) e o LIKE por substring do
# site, que pode casar mais de um cliente. Conferido em models.py e cliente/index.php.
id: chave_de_juncao_errada
titulo: Chave de junção errada
sistema: Ambos
entidade_principal: Pedido
tipo: erro
status: ativo
causa_raiz: chave_de_juncao_errada
arquivos: [Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaFront/cliente/index.php]
endpoints: [GET /api/produtos, GET /api/pedidos]
tabelas: [tbprodutos, tbtipos, tbusuarios, tbpedido_reserva]
sintomas: [nome de outra pessoa na reserva, categoria errada, imagem de outro produto, nome da categoria no titulo]
palavras_chave: [juncao, join, chave, id, fk, cliente errado, categoria errada, troca, admin, like, substring]
causas_relacionadas: [nulo_inesperado, escala_ou_unidade_errada, valor_fora_do_dominio]
---
## Resumo
Tipo e formato certos, mas o valor é de OUTRO registro: categoria ou imagem alheia no produto, nome ou cpf de outro usuário na reserva.

## Sinais
- afeta campo derivado de junção (tipo, nome, cpf, imagem), não os próprios
- o dado existe no banco, ligado ao registro errado

## Causa
Junções: id_tipo_produto e id_clientes (models.py). No site, cliente/index.php:4 usa LIKE '%login%' — CPF substring de outro casa mais de um cliente.
