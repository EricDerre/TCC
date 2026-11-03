---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: a API serializa a data com isoformat(); qualquer outro formato é divergência.
# Conferido em pedidos.py:23.
id: formato_de_data_divergente
titulo: Formato de data divergente
sistema: CobaiaAPI
entidade_principal: Pedido
tipo: erro
status: ativo
causa_raiz: formato_de_data_divergente
arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py]
endpoints: [GET /api/pedidos, POST /api/pedidos]
tabelas: [tbpedido_reserva]
sintomas: [Invalid Date, data como numero, data em formato brasileiro]
palavras_chave: [data, formato, iso, AAAA-MM-DD, dd/mm/aaaa, timestamp, epoch, Invalid Date, data_pedido]
causas_relacionadas: [escala_ou_unidade_errada, tipo_divergente]
---
## Resumo
data_pedido deve ser texto AAAA-MM-DD. Chega noutro formato (10/09/2026), como segundos (1789084800) ou com hora e fuso — e o cliente não interpreta.

## Sinais
- "Invalid Date" na listagem: formato brasileiro ou texto não reconhecido
- número grande no lugar da data: timestamp

## Causa
A API devolve data_pedido.isoformat() (pedidos.py:23), sempre AAAA-MM-DD. Em escala_ou_unidade_errada a data é legível mas deslocada; aqui é ilegível.
