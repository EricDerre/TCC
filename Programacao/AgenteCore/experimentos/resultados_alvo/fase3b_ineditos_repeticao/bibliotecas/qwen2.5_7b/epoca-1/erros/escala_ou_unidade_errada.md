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
palavras_chave: [escala, unidade, centavos, reais, fator, cem, arredond, fuso, dia, dobro, multiplic, divid, conversao]
causas_relacionadas: [tipo_divergente, formato_de_data_divergente, chave_de_juncao_errada]
# ! Alteração por modelo qwen2.5:7b (E1, caso tra-6) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5:7b (E1, caso tra-12) - Revisar: retificação acrescentada.
---
## Resumo
Tipo e formato certos, mas o número está noutra escala ou unidade: centavos por reais (8990), fração (0.899), arredondado (90), data deslocada um dia, quantidade dobrada.

## Sinais
- todos os valores errados pelo mesmo fator: conversão de unidade
- só o arredondamento errado

## Causa
A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela.

## Notas do modelo
- [E1 · tra-6 · retificação de "A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela."] Corrigir a conversão do valor_produto para float, aplicando o fator correto. — Motivo: Este caso mostrou que a conversão direta do DECIMAL para float sem aplicar o fator correto resulta em preços errados, evidenciando a necessidade de uma correção na documentação.
- [E1 · tra-12 · retificação de "Sinais: todos os valores errados pelo mesmo fator: conversão de unidade; só o arredondamento errado. Causa: A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela."] Adicionar exemplo de conversão incorreta de valor_produto DECIMAL(9,2) para float, causando arredondamento. — Motivo: Este caso mostrou que a documentação não era suficiente para alertar sobre a necessidade de conversão correta do valor DECIMAL para float, o que resultou em arredondamento.
