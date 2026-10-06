---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: lista as origens reais de 500 (injetor e banco fora) e a diferença crucial:
# no site PHP, banco fora não dá 500, dá HTML. Conferido em produtos.py e connect.php.
id: erro_interno_do_servidor
titulo: Erro interno do servidor (500)
sistema: Ambos
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: erro_interno_do_servidor
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/conn/connect.php]
endpoints: [GET /api/produtos, POST /api/pedidos]
sintomas: [HTTP 500, Internal Server Error, fault injection error_500, falha intermitente, intermitente sem padrao, em toda requisicao, banco inacessivel, erro interno do servidor, banco fora]
palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora, injetor, banco inacessivel, defeito na rota, excecao nao tratada, falhas de banco de dados, injetores de erros]
causas_relacionadas: [corpo_nao_e_json, tempo_de_resposta_excedido, limite_de_requisicoes]
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso run-6) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso run-12) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E3, caso run-6) - Revisar: nota acrescentada.
---
## Resumo
500 com {"detail": ...}: falha própria da API. detail "fault injection: error_500 em produto" é o injetor; "Internal Server Error" é exceção não tratada.

## Sinais
- intermitente sem padrão: injetor com probability < 1
- em toda requisição: banco inacessível ou defeito na rota

## Causa
Rotas convertem ErrorFault em 500 (produtos.py:42). No site PHP, banco fora NÃO dá 500: imprime "Atenção ERRO" em HTML (connect.php:16).

## Notas do modelo
- [E1 · run-6 · nota] Adicionar nota explicando que o erro interno do servidor pode ocorrer devido a falhas no banco de dados ou defeitos na rota, além de ser intermitente. — Motivo: Esta nota ajudará a explicar a causa raiz do erro interno do servidor em rotas de produtos, que é um problema de infraestrutura relacionado ao banco de dados ou rotas.
- [E1 · run-12 · nota] Adicionar nota explicando que o erro interno do servidor pode ser causado por falhas de banco de dados ou injetores de erros. — Motivo: Esta nota ajudará a identificar rapidamente falhas de banco de dados ou injetores de erros como a causa raiz do problema.
- [E3 · run-6 · nota] Adicionar nota explicando que o erro interno do servidor pode ocorrer devido a falhas no banco de dados ou defeitos na rota, além de ser intermitente. Adicionar nota explicando que o erro interno do servidor pode ser causado por falhas de banco de dados ou injetores de erros. — Motivo: Esta nota ajudará a explicar as possíveis causas do erro interno do servidor, incluindo falhas no banco de dados e injetores de erros, o que pode ajudar a diagnosticar o problema corretamente.
