---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: lista os domínios reais (ENUM do banco e min do HTML) e onde não há validação;
# conferido em schema_completo.sql, models.py e registrar_reserva.php.
id: valor_fora_do_dominio
titulo: Valor fora do domínio
sistema: Ambos
entidade_principal: Pedido
tipo: erro
status: ativo
causa_raiz: valor_fora_do_dominio
arquivos: [Programacao/CobaiaFront/banco/schema_completo.sql, Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaFront/cliente/registrar_reserva.php]
endpoints: [GET /api/pedidos, GET /api/produtos]
tabelas: [tbpedido_reserva, tbprodutos]
sintomas: [status desconhecido, pessoas zero, destaque 2, reserva sem botao de cancelar, botao de cancelar some, status inesperado]
palavras_chave: [dominio, enum, permitido, conjunto, status, Pendente, Concluido, pessoas, zero, negativo, destaque, validacao]
causas_relacionadas: [tipo_divergente, formato_de_data_divergente, nulo_inesperado]
# ! Alteração por modelo qwen2.5:7b (E1, caso semt-11) - Revisar: retificação acrescentada.
---
## Resumo
Tipo certo, valor fora do conjunto permitido: status diferente de 'Em Análise'/'Cancelado', destaque diferente de true/false, pessoas menor que 1.

## Sinais
- reserva nem ativa nem cancelada na tela: status inesperado
- 0 ou negativo em pessoas: o mínimo só existe no HTML

## Causa
status e destaque são ENUM no banco (schema_completo.sql:37); pessoas ≥ 1 é só min= do HTML (registrar_reserva.php:55); a API não valida o que devolve.

## Notas do modelo
- [E1 · semt-11 · retificação de "Valor fora do domínio"] Adicionar validação no status do pedido na API para evitar valores fora do domínio. — Motivo: Este caso mostrou que a API não valida o status do pedido, permitindo valores inválidos como 'Concluido', o que afeta a exibição de botões na interface.
