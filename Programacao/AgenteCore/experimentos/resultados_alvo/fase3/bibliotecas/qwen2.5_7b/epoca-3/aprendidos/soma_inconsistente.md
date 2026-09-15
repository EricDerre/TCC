---
# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 3 a partir do caso semt-7 (Fase 3).
# ! Motivo: O caso mostrou que a soma total de lugares reservados estava incorreta devido ao campo pessoas vindo como uma string, e a junção incorreta pode levar a linhas nulas.
id: soma_inconsistente
titulo: Soma inconsistente
sistema: Ambos
entidade_principal: Pedido
tipo: aprendido
status: ativo
sintomas: [soma_total_incorreta, campos_nulos, juncao_incorreta]
palavras_chave: [soma, tipo, juncao]
causas_relacionadas: [tipo_divergente, chave_de_juncao_errada]
---
## Resumo
Adicionar validação no backend para verificar se a soma de pessoas está correta e corrigir a lógica do LEFT JOIN para evitar linhas nulas.

## Sinais
- soma_total_incorreta
- campos_nulos
- juncao_incorreta
