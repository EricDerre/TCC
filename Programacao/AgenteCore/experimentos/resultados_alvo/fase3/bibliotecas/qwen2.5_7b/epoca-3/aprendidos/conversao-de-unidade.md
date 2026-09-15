---
# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso tra-6 (Fase 3).
# ! Motivo: Este caso demonstra a importância de explicitar a necessidade de aplicar o fator correto na conversão de unidades monetárias, evitando erros de escala.
id: conversao-de-unidade
titulo: Conversão de unidade
sistema: CobaiaAPI
entidade_principal: Produto
tipo: aprendido
status: ativo
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py]
sintomas: [precos cem vezes menores]
palavras_chave: [fator, decimal, unidade]
causas_relacionadas: [escala_ou_unidade_errada]
---
## Resumo
Adicionar instruções sobre a necessidade de aplicar o fator correto na conversão do valor_produto.

## Sinais
- precos cem vezes menores
