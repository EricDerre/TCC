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
palavras_chave: [429, limite, rate limit, too many requests, retry_after, cota, excesso, recarregar]
causas_relacionadas: [tempo_de_resposta_excedido, erro_interno_do_servidor]
---
## Resumo
Status 429: o servidor ou um intermediário recusou por excesso de requisições num intervalo. Resposta rápida e com corpo — não é lentidão nem erro interno.

## Sinais
- funciona, depois falha após recarregar muitas vezes
- "Erro ao carregar produtos da CobaiaAPI: HTTP 429"; pode vir retry_after

## Causa
A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado.
