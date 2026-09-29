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
palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora, falha_interna, injetor, excecao_nao_tratada, injecao de falha, excecao nao tratada]
causas_relacionadas: [corpo_nao_e_json, tempo_de_resposta_excedido, limite_de_requisicoes]
# ! Alteração por modelo qwen2.5:7b (E1, caso run-6) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E1, caso run-12) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E2, caso run-12) - Revisar: retificação acrescentada.
---
## Resumo
500 com {"detail": ...}: falha própria da API. detail "fault injection: error_500 em produto" é o injetor; "Internal Server Error" é exceção não tratada.

## Sinais
- intermitente sem padrão: injetor com probability < 1
- em toda requisição: banco inacessível ou defeito na rota

## Causa
Rotas convertem ErrorFault em 500 (produtos.py:42). No site PHP, banco fora NÃO dá 500: imprime "Atenção ERRO" em HTML (connect.php:16).

## Notas do modelo
- [E1 · run-6 · nota] Adicionar que este erro pode ocorrer devido a falhas no banco de dados ou em rotas, e que a mensagem genérica pode esconder problemas específicos. — Motivo: Este caso mostrou que a mensagem de erro genérica pode esconder problemas específicos, como falhas no banco de dados, que não são explicitamente mencionados na documentação.
- [E1 · run-12 · nota] Adicionar que este erro pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota. — Motivo: Este caso mostrou que o erro interno do servidor pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota, evidenciando a necessidade de uma nota sobre esse comportamento.
- [E2 · run-12 · retificação de "500 com {'detail': ...}: falha própria da API. detail 'fault injection: error_500 em produto' é o injetor; 'Internal Server Error' é exceção não tratada."] Corrigir a estrutura da resposta da API para ser consistente, evitando envelopes ou campos simples aninhados, para padronizar o desenpacotamento dos dados. — Motivo: Este caso mostrou que a documentação não abrangia a necessidade de padronização na estrutura da resposta, o que pode levar a diagnósticos incorretos em casos futuros.
