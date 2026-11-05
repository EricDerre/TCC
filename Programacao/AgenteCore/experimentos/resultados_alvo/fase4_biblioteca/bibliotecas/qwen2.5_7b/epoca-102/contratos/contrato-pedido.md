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
sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado, duas reservas iguais apos um unico post, registros com id consecutivo]
palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar, post duplo, registros duplicados]
causas_relacionadas: [formato_de_data_divergente, valor_fora_do_dominio, recurso_inexistente, campo_ausente]
# ! Alteração por modelo qwen2.5:7b (E101, caso run-5) - Revisar: nota acrescentada.
---
## Resumo
GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf.

## Sinais
- data noutro formato ou como número
- status fora dos dois valores

## Causa
cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).

## Notas do modelo
- [E101 · run-5 · nota] Adicionar nota sobre a possibilidade de POST /api/pedidos inserir registros duplicados sem idempotência, causando registros com id consecutivo e duas respostas 201 para um único POST. — Motivo: Este caso mostrou que a falta de mecanismo de idempotência no POST /api/pedidos pode resultar em registros duplicados, algo não coberto nos verbetes existentes.
