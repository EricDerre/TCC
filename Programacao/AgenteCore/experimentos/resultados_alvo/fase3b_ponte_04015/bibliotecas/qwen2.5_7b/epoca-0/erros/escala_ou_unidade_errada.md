---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: a API não aplica escala nenhuma (float direto do DECIMAL, DATE sem fuso), o
# que faz qualquer fator ou deslocamento ser sinal de tradução errada. Conferido.
id: escala_ou_unidade_errada
titulo: Escala ou unidade errada
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: escala_ou_unidade_errada
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/models.py]
endpoints: [GET /api/produtos, GET /api/pedidos]
tabelas: [tbprodutos, tbpedido_reserva]
sintomas: [precos cem vezes maiores, precos cem vezes menores, preco arredondado, data um dia antes, dobro de pessoas]
palavras_chave: [escala, unidade, centavos, reais, fator, cem, arredond, fuso, dia, dobro, multiplic, divid]
causas_relacionadas: [tipo_divergente, formato_de_data_divergente, chave_de_juncao_errada]
---
## Resumo
Tipo e formato certos, mas o número está noutra escala ou unidade: centavos por reais (8990), fração (0.899), arredondado (90), data deslocada um dia, quantidade dobrada.

## Sinais
- todos os valores errados pelo mesmo fator: conversão de unidade
- só o arredondamento errado

## Causa
A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela.
