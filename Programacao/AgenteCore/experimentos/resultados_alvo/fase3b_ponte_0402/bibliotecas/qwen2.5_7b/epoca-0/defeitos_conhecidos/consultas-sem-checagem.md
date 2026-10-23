---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (defeito conhecido).
# ! Motivo: nenhuma página confere o retorno de query(), e o cancelamento aceita qualquer
# id pela URL — duas ausências reais que produzem "gravou mas não aparece".
id: consultas-sem-checagem
titulo: Consultas sem checagem e cancelamento sem dono
sistema: CobaiaFront
entidade_principal: Pedido
tipo: defeito_conhecido
status: nao_corrigido
arquivos: [Programacao/CobaiaFront/cliente/registrar_reserva.php, Programacao/CobaiaFront/cliente/cliente_cancelar.php, Programacao/CobaiaFront/conn/connect.php]
tabelas: [tbpedido_reserva]
sintomas: [reserva confirmada que nao aparece, reserva de outro cliente cancelada, redireciona sem gravar]
palavras_chave: [query, mysqli, retorno, checagem, silencioso, cancelar, id_pedido, url, dono, redirect]
causas_relacionadas: [dado_desatualizado, estado_da_tela_divergente, registro_duplicado]
---
## Resumo
Nenhuma página PHP confere o retorno de $conn->query(): INSERT/UPDATE que falha segue em silêncio e a página redireciona como se tivesse gravado. cliente_cancelar.php:6 aceita qualquer id_pedido pela URL, sem checar o dono.

## Sinais
- reserva "confirmada" que não aparece depois
- reserva de outra pessoa cancelada

## Causa
mysqli não lança exceção por padrão; a falha só aparece como dado ausente ou tela que não muda.
