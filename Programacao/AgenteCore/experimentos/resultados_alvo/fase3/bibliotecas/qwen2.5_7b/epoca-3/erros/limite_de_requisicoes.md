---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: a CobaiaAPI não implementa limite de requisições — um 429 só pode vir de
# fora dela, e isso é o que o modelo precisa saber. Conferido em main.py e nos routers.
id: limite_de_requisicoes
titulo: Limite de requisições (429)
sistema: Infraestrutura
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: limite_de_requisicoes
arquivos: [Programacao/CobaiaAPI/app/main.py, Programacao/CobaiaFront/produtos_api.php]
endpoints: [GET /api/produtos]
sintomas: [HTTP 429, too many requests, rate limit, para de funcionar apos varias tentativas]
palavras_chave: [429, limite, rate limit, too many requests, retry_after, cota, excesso, recarregar, limitador, excesso_de_requisicoes]
causas_relacionadas: [tempo_de_resposta_excedido, erro_interno_do_servidor]
# ! Alteração por modelo qwen2.5:7b (E3, caso run-3) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5:7b (E3, caso run-3) - Revisar: nota acrescentada.
---
## Resumo
Status 429: o servidor ou um intermediário recusou por excesso de requisições num intervalo. Resposta rápida e com corpo — não é lentidão nem erro interno.

## Sinais
- funciona, depois falha após recarregar muitas vezes
- "Erro ao carregar produtos da CobaiaAPI: HTTP 429"; pode vir retry_after

## Causa
A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado.

## Notas do modelo
- [E3 · run-3 · retificação de "Causa: A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado."] Corrigir que destaque booleano saia literal, garantindo que seja convertido corretamente para True ou False. — Motivo: Este trecho não aborda a questão do destaque booleano, que é relevante para diagnósticos futuros de inconsistências na interface.
- [E3 · run-3 · nota] Adicionar nota sobre a necessidade de verificar a consistência entre a contagem de itens na resposta e a renderização na interface, especialmente em endpoints que retornam listas paginadas. — Motivo: Este trecho destaca a importância de verificar a consistência entre contagens e renderizações, que é crucial para diagnósticos futuros de inconsistências na interface.
