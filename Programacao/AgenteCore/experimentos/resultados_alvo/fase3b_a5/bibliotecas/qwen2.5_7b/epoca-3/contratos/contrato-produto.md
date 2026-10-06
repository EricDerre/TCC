---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (contrato).
# ! Motivo: campo a campo, com a diferença declarado × real (Decimal no schema, número
# em ponto flutuante no fio). Conferido em schemas.py e produtos.py.
id: contrato-produto
titulo: Contrato de /api/produtos
sistema: CobaiaAPI
entidade_principal: Produto
tipo: contrato
status: ativo
arquivos: [Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaAPI/app/routers/produtos.py]
endpoints: [GET /api/produtos, GET /api/produtos/{id}]
tabelas: [tbprodutos, tbtipos]
sintomas: [chave a mais ou a menos, lista no lugar de objeto, preco como texto, lista incompleta, ultimo item cortado, lista onde se espera objeto, ou o inverso, nulo_inesperado, valor_fora_do_dominio]
palavras_chave: [contrato, produtos, id, nome, resumo, tipo, preco, imagem, destaque, lista, objeto, 404, produto nao encontrado, schema, json, campos, divergencia, convercao]
causas_relacionadas: [campo_ausente, campo_renomeado, colecao_no_lugar_de_objeto, tipo_divergente, recurso_inexistente]
# ! Alteração por modelo qwen2.5:7b (E1, caso lex-5) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E1, caso sin-6) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5:7b (E1, caso sin-13) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5:7b (E2, caso semt-6) - Revisar: nota acrescentada.
---
## Resumo
GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.

## Sinais
- chave a mais ou a menos: campo ausente ou renomeado
- lista onde se espera objeto, ou o inverso

## Causa
Origem tbprodutos + rótulo de tbtipos (produtos.py _to_dict). preco sai 89.9 (número), embora o schema declare Decimal.

## Notas do modelo
- [E1 · lex-5 · nota] Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta. — Motivo: Destacar a necessidade de incluir o risco de truncamento de resposta no contrato, pois é uma causa comum de problemas de integração.
- [E1 · sin-6 · retificação de "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano."] Corrigir "preco número" para "preco Decimal" para refletir o tipo correto em valor_produto. — Motivo: Este trecho mostra a divergência entre o tipo declarado no contrato e o tipo real na resposta, evidenciando a necessidade de manter a consistência entre ambos.
- [E1 · sin-13 · retificação de "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano."] Adicionar observação sobre possíveis nomes diferentes para o campo tipo no verbete. — Motivo: O caso mostrou que o campo tipo pode ser renomeado ou ter seu tipo divergente, necessitando de uma observação explícita no verbete.
- [E2 · semt-6 · nota] Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda a necessidade de converção correta do tipo de dados no front-end. — Motivo: Este caso mostrou que a documentação do contrato não aborda a necessidade de converção correta do tipo de dados no front-end, o que pode levar a erros como o ID vindo como uma string.
