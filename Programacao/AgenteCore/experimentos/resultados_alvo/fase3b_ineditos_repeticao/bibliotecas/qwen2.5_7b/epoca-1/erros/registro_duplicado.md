---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: nem a API nem o formulário PHP têm chave de idempotência — reenvio grava de
# novo. Conferido em pedidos.py e registrar_reserva.php.
id: registro_duplicado
titulo: Registro duplicado
sistema: Ambos
entidade_principal: Pedido
tipo: erro
status: ativo
causa_raiz: registro_duplicado
arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaFront/cliente/registrar_reserva.php]
endpoints: [POST /api/pedidos, GET /api/pedidos]
tabelas: [tbpedido_reserva]
sintomas: [duas reservas identicas, dois 201 seguidos, cobranca em duplicidade]
palavras_chave: [duplicad, duplicat, repetid, reenvio, clique duplo, F5, idempot, dois registros, ids consecutivos]
causas_relacionadas: [dado_desatualizado, contagem_inconsistente]
---
## Resumo
A mesma escrita gravada mais de uma vez: reservas iguais com ids consecutivos, duas respostas 201 para um único gesto.

## Sinais
- registros idênticos exceto pelo id
- dois POST com o mesmo corpo na sequência

## Causa
POST /api/pedidos insere sem chave de idempotência (pedidos.py:46-66): clique duplo vira duas linhas. registrar_reserva.php insere a cada POST — recarregar após reservar reenvia o formulário.
