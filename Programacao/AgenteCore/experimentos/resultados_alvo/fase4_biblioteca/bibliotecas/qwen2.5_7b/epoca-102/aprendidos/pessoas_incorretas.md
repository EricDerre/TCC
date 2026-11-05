---
# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 101 a partir do caso tra-5 (Fase 3).
# ! Motivo: O caso demonstrou a necessidade de validação adicional para garantir que a quantidade de pessoas seja correta.
id: pessoas_incorretas
titulo: Inconsistência na quantidade de pessoas reservadas
sistema: CobaiaAPI
entidade_principal: Pedido
tipo: aprendido
status: ativo
sintomas: [pessoas menor que 1, reserva nem ativa nem cancelada na tela]
palavras_chave: [conversao, arredondamento, quantidade]
causas_relacionadas: [escala_ou_unidade_errada, valor_fora_do_dominio]
---
## Resumo
Adicionar validação no número de pessoas no pedido para evitar valores incorretos.

## Sinais
- pessoas menor que 1
- reserva nem ativa nem cancelada na tela
