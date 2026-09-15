---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: a API real não tem total nem paginação — qualquer envelope com contagem já
# é sinal de outra origem; conferido em produtos.py.
id: contagem_inconsistente
titulo: Contagem inconsistente
sistema: Ambos
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: contagem_inconsistente
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_destaque.php]
endpoints: [GET /api/produtos]
tabelas: [tbprodutos]
sintomas: [total diferente dos itens, pagina vazia com total positivo, quatro destaques mas cinco cartoes, contagem de destaques incorreta, renderizacao de cartoes]
palavras_chave: [contagem, total, itens, pagina, paginacao, quantidade, destaques, inconsistente, zero, renderizacao, home]
causas_relacionadas: [estrutura_aninhada_divergente, dado_desatualizado, estado_da_tela_divergente]
# ! Alteração por modelo qwen2.5:7b (E2, caso tra-14) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E2, caso tra-14) - Revisar: retificação acrescentada.
---
## Resumo
Dois números que deveriam bater não batem: total 14 e lista com 1; total 0 com itens; página 2 vazia com total 14; contador de destaques diferente dos cartões.

## Sinais
- total e lista vêm de consultas diferentes
- rótulo numérico que não corresponde ao renderizado

## Causa
GET /api/produtos devolve a lista crua, sem total nem paginação (produtos.py:34-43); o seed tem 14 produtos, 5 em destaque. Envelope com total indica outra versão.

## Notas do modelo
- [E2 · tra-14 · nota] Adicionar nota sobre a necessidade de verificar a consistência entre a contagem de itens na resposta e a renderização na interface, especialmente em endpoints que retornam listas paginadas. — Motivo: Este caso mostrou que a inconsistência entre a contagem de itens na resposta e a renderização na interface é um problema comum, mas a documentação não destaca a importância de verificar essa consistência em endpoints paginados.
- [E2 · tra-14 · retificação de "contador de destaques diferente dos cartões. Sinais: total e lista vêm de consultas diferentes; rótulo numérico que não corresponde ao renderizado."] Corrigir que destaque booleano saia literal, garantindo que seja convertido corretamente para True ou False. — Motivo: Esta retificação corrigirá a conversão do destaque booleano, mas também destaca a importância de verificar a consistência entre a contagem de itens na resposta e a renderização na interface, especialmente em endpoints paginados.
