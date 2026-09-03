---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (regra de negócio).
# ! Motivo: o domínio fechado do status e o LEFT JOIN da view são as duas fontes reais de
# valor_fora_do_dominio e nulo_inesperado em reservas; conferido em schema_completo.sql.
id: pedido-reserva
titulo: Reserva de mesa (pedido)
sistema: Ambos
entidade_principal: Pedido
tipo: funcionamento
status: ativo
arquivos: [Programacao/CobaiaFront/banco/schema_completo.sql, Programacao/CobaiaFront/cliente/reserva_cli.php, Programacao/CobaiaAPI/app/routers/pedidos.py]
endpoints: [GET /api/pedidos]
tabelas: [tbpedido_reserva, vw_tbpedidos, tbusuarios]
sintomas: [status com texto desconhecido, reserva de outro cliente, linha de reserva vazia]
palavras_chave: [reserva, pedido, status, em analise, cancelado, pessoas, data_pedido, id_clientes, view]
causas_relacionadas: [valor_fora_do_dominio, nulo_inesperado, chave_de_juncao_errada]
---
## Resumo
Reserva em tbpedido_reserva: id_pedido, id_clientes (chave para tbusuarios), pessoas, data_pedido, status. Status só admite 'Em Análise' (inicial) e 'Cancelado'.

## Sinais
- status com outro texto: fora do domínio
- linha de reserva toda vazia: cliente que ainda não reservou

## Causa
A leitura usa vw_tbpedidos, LEFT JOIN de tbusuarios (schema_completo.sql:57): cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza.
