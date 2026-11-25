---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (regra de negócio).
# ! Motivo: as regras de data e de pessoas existem só no HTML — o modelo precisa saber
# que o servidor aceita qualquer valor, senão diagnostica "validação" onde não há.
id: fluxo-reserva-e-cancelamento
titulo: Fluxo de reservar e cancelar
sistema: Ambos
entidade_principal: Pedido
tipo: regra
status: ativo
arquivos: [Programacao/CobaiaFront/cliente/registrar_reserva.php, Programacao/CobaiaFront/cliente/cliente_cancelar.php, Programacao/CobaiaAPI/app/routers/pedidos.py]
endpoints: [POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
tabelas: [tbpedido_reserva]
sintomas: [data aceita fora da janela, reserva alheia cancelada, pessoas zero]
palavras_chave: [reservar, cancelar, data, janela, dois dias, noventa dias, pessoas, minimo, validacao, formulario]
causas_relacionadas: [valor_fora_do_dominio, dado_desatualizado, estado_da_tela_divergente]
---
## Resumo
Reserva em cliente/registrar_reserva.php e cancelamento em reserva_cli.php; a API espelha em POST /api/pedidos e POST /api/pedidos/{id}/cancelar.

## Sinais
- regra de data e quantidade só no navegador
- reserva alheia cancelada sem checagem de dono

## Causa
Data hoje+2 a hoje+90 e pessoas ≥ 1 são só min/max do HTML (registrar_reserva.php:28-35,55); cancelar grava 'Cancelado' (pedidos.py:75).
