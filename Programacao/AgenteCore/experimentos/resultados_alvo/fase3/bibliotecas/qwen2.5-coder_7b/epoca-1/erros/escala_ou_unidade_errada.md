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
sintomas: [precos cem vezes maiores, precos cem vezes menores, preco arredondado, data um dia antes, dobro de pessoas, data deslocada um dia, precos arredondados, precisao financeira comprometida]
palavras_chave: [escala, unidade, centavos, reais, fator, cem, arredond, fuso, dia, dobro, multiplic, divid, conversao, decimal, fuso horario, conversao de data, conversao de unidade, valor_produto]
causas_relacionadas: [tipo_divergente, formato_de_data_divergente, chave_de_juncao_errada]
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-6) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-9) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-12) - Revisar: retificação acrescentada.
---
## Resumo
Tipo e formato certos, mas o número está noutra escala ou unidade: centavos por reais (8990), fração (0.899), arredondado (90), data deslocada um dia, quantidade dobrada.

## Sinais
- todos os valores errados pelo mesmo fator: conversão de unidade
- só o arredondamento errado

## Causa
A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela.

## Notas do modelo
- [E1 · tra-6 · retificação de "float(valor_produto) direto do DECIMAL"] A conversão de valor_produto deve considerar a escala correta, convertendo DECIMAL(9,2) para float sem alteração. — Motivo: A evidência deste caso mostrou que a conversão direta de DECIMAL para float estava causando a escala errada, o que foi confirmado pela documentação do verbete [escala_ou_unidade_errada].
- [E1 · tra-9 · retificação de "DATE em isoformat sem fuso"] A API deve converter a data para o fuso horário do cliente antes de retornar. — Motivo: A falta de conversão de fuso horário é a causa raiz do problema, conforme mostrado no caso atual.
- [E1 · tra-12 · retificação de "float(valor_produto)"] A API deve converter DECIMAL para número considerando a escala correta (100 para centavos). — Motivo: A evidência deste caso mostrou que a API estava simplesmente convertendo DECIMAL para número sem considerar a escala correta, resultando em preços arredondados.
