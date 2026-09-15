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
sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado, pessoas incorreta, data em formato errado, registro duplicado, duas reservas identicas, uma das reservas do cliente some da tela, status inesperado, reserva nem ativa nem cancelada]
palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar, validacao, dados, entrada, idempotencia, unidade de trabalho, contrato pedido cpf ausente]
causas_relacionadas: [formato_de_data_divergente, valor_fora_do_dominio, recurso_inexistente, campo_ausente]
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-5) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso run-5) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso sin-12) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso semt-11) - Revisar: retificação acrescentada.
---
## Resumo
GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf.

## Sinais
- data noutro formato ou como número
- status fora dos dois valores

## Causa
cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).

## Notas do modelo
- [E1 · tra-5 · retificação de "pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado'"] Adicionar validação de dados no endpoint /api/pedidos para garantir que os valores de pessoas estejam no formato correto e que a data esteja no formato AAAA-MM-DD. — Motivo: A falta de validação de dados no endpoint /api/pedidos é a causa raiz do problema. A documentação não menciona a necessidade de validação dos dados de entrada, o que resultou em um erro de integração entre a interface web e a API.
- [E1 · run-5 · retificação de "POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201;"] Adicionar verificação de idempotência para evitar inserções duplicadas. — Motivo: A falta de verificação de idempotência permite que o mesmo pedido seja inserido múltiplas vezes, causando registros duplicados. A adição de uma chave de idempotência garante que cada pedido seja inserido apenas uma vez.
- [E1 · sin-12 · nota] Adicionar 'cpf' como campo obrigatório no contrato de pedido. — Motivo: O campo 'cpf' é crucial para identificar o cliente, e sua ausência causa inconsistência na tela do usuário.
- [E1 · semt-11 · retificação de "status 'Em Análise'|'Cancelado'"] A API deve validar o status dos pedidos para garantir que seja 'Em Análise' ou 'Cancelado'. — Motivo: A falta de validação do status na API é a causa raiz do problema, conforme mostrado no caso atual, onde o status 'Concluido' não é reconhecido.
