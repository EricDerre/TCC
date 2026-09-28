---
# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso tra-12 (Fase 3).
# ! Motivo: Este caso demonstrou a necessidade de uma regra específica para a conversão de valores DECIMAL para float, para evitar arredondamentos incorretos.
id: conversao-de-valor
titulo: Conversão de valor DECIMAL para float
sistema: CobaiaAPI
entidade_principal: Produto
tipo: aprendido
status: ativo
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py]
sintomas: [arredondamento incorreto, valor fora do dominio]
palavras_chave: [conversao, arredondamento, decimal, float]
causas_relacionadas: [escala_ou_unidade_errada, valor_fora_do_dominio]
---
## Resumo
Adicionar regra para conversão correta de valor DECIMAL para float no _to_dict.

## Sinais
- arredondamento incorreto
- valor fora do dominio
