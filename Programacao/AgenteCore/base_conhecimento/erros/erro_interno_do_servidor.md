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
sintomas: [HTTP 500, Internal Server Error, fault injection error_500, falha intermitente]
palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora]
causas_relacionadas: [corpo_nao_e_json, tempo_de_resposta_excedido, limite_de_requisicoes]
---
## Resumo
500 com {"detail": ...}: falha própria da API. detail "fault injection: error_500 em produto" é o injetor; "Internal Server Error" é exceção não tratada.

## Sinais
- intermitente sem padrão: injetor com probability < 1
- em toda requisição: banco inacessível ou defeito na rota

## Causa
Rotas convertem ErrorFault em 500 (produtos.py:42). No site PHP, banco fora NÃO dá 500: imprime "Atenção ERRO" em HTML (connect.php:16).
