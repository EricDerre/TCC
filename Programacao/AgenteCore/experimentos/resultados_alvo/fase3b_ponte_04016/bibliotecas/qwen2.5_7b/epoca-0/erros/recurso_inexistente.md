---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: os quatro 404 com mensagem própria e o 404 de rota são distinguíveis pelo
# detail — é o que aponta o ponto do código. Conferido em produtos.py, pedidos.py, admin_fault.py.
id: recurso_inexistente
titulo: Recurso inexistente (404 e vizinhos)
sistema: CobaiaAPI
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: recurso_inexistente
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/routers/admin_fault.py]
endpoints: [GET /api/produtos/{id}, GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
sintomas: [HTTP 404, Not Found, produto nao encontrado, cliente nao encontrado, pedido nao encontrado, rota errada]
palavras_chave: [404, not found, nao encontrado, inexistente, rota, endpoint, singular, plural, 403, 422, detail]
causas_relacionadas: [erro_interno_do_servidor, localizador_quebrado]
---
## Resumo
404: id ou rota inexistente. O detail diz qual: "produto não encontrado" (produtos.py:52), "cliente não encontrado" (pedidos.py:37,52), "pedido não encontrado" (pedidos.py:74); "Not Found" genérico é rota inexistente (ex.: /api/produto).

## Sinais
- id válido e ainda 404: campo de busca errado (login × id)
- vizinhos: 403 no admin sem token; 422 sem login

## Causa
Cada 404 com mensagem vem de db.get/filter vazio na rota.
