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
sintomas: [status com texto desconhecido, reserva de outro cliente, linha de reserva vazia, reserva_incompleta, reserva_normal, reserva_nao_ativa_nem_cancelada, status_inesperado, reserva_vazia, cliente_sem_reserva]
palavras_chave: [reserva, pedido, status, em analise, cancelado, pessoas, data_pedido, id_clientes, view, campos_nulos, renderizacao_incorreta, enum, validacao, left_join, nulo, renderizacao]
causas_relacionadas: [valor_fora_do_dominio, nulo_inesperado, chave_de_juncao_errada]
# ! Alteração por modelo qwen2.5:7b (E1, caso sin-12) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5:7b (E1, caso semt-15) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5:7b (E1, caso semt-15) - Revisar: retificação acrescentada.
---
## Resumo
Reserva em tbpedido_reserva: id_pedido, id_clientes (chave para tbusuarios), pessoas, data_pedido, status. Status só admite 'Em Análise' (inicial) e 'Cancelado'.

## Sinais
- status com outro texto: fora do domínio
- linha de reserva toda vazia: cliente que ainda não reservou

## Causa
A leitura usa vw_tbpedidos, LEFT JOIN de tbusuarios (schema_completo.sql:57): cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza.

## Notas do modelo
- [E1 · sin-12 · retificação de "cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza."] Corrigir a renderização para não exibir linhas com campos nulos quando o cliente não reservou. — Motivo: Este caso mostrou que a interface web exibe linhas incompletas, indicando uma falha na lógica de renderização quando os campos ausentes não são tratados adequadamente.
- [E1 · semt-15 · retificação de "Status só admite 'Em Análise' (inicial) e 'Cancelado'."] Adicionar validação no backend para verificar se o status está dentro do domínio permitido. — Motivo: O caso mostrou que a API retorna um status inesperado, que não é tratado pelo frontend, causando o problema de reserva sem pessoas.
- [E1 · semt-15 · retificação de "A leitura usa vw_tbpedidos, LEFT JOIN de tbusuarios (schema_completo.sql:57): cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza."] Corrigir a lógica do LEFT JOIN para evitar linhas nulas quando o cliente não tem reserva. — Motivo: O caso mostrou que a API retorna linhas nulas para clientes sem reserva, que são renderizadas pelo frontend, causando o problema de reserva não alocada.
