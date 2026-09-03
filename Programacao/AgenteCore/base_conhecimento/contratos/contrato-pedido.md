---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (contrato).
# ! Motivo: reúne os três endpoints de pedido, os códigos de erro reais e a divergência
# de busca (exata na API, substring no PHP). Conferido em pedidos.py e cliente/index.php.
id: contrato-pedido
titulo: Contrato de /api/pedidos
sistema: CobaiaAPI
entidade_principal: Pedido
tipo: contrato
status: ativo
arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaFront/cliente/index.php]
endpoints: [GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
tabelas: [tbpedido_reserva, tbusuarios]
sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado]
palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar]
causas_relacionadas: [formato_de_data_divergente, valor_fora_do_dominio, recurso_inexistente, campo_ausente]
---
## Resumo
GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf.

## Sinais
- data noutro formato ou como número
- status fora dos dois valores

## Causa
cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
