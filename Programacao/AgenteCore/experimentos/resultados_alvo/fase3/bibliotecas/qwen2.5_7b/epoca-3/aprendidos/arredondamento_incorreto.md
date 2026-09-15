---
# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 3 a partir do caso tra-5 (Fase 3).
# ! Motivo: O caso mostrou que a conversão direta do valor_produto pode levar a arredondamento errado, necessitando de uma correção no processo.
id: arredondamento_incorreto
titulo: Arredondamento incorreto
sistema: CobaiaAPI
entidade_principal: Pedido
tipo: aprendido
status: ativo
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py]
sintomas: [arredondamento errado, valor_fora_do_dominio]
palavras_chave: [arredondamento, fator, conversao]
causas_relacionadas: [escala_ou_unidade_errada]
---
## Resumo
Adicionar exemplo de conversão incorreta de valor_produto DECIMAL(9,2) para float, causando arredondamento.

## Sinais
- arredondamento errado
- valor_fora_do_dominio
