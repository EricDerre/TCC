---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (fronteira de integração).
# ! Motivo: é a única página com fetch() JSON do cobaia; as mensagens literais que ela
# imprime e o que faz com cada campo são o elo entre a resposta HTTP e o que o usuário vê.
id: pagina-produtos-api
titulo: Aba "Produtos (API)", a fronteira JSON
sistema: CobaiaFront
entidade_principal: Interface
tipo: funcionamento
status: ativo
arquivos: [Programacao/CobaiaFront/produtos_api.php]
endpoints: [GET /api/produtos, GET /api/produtos/{id}]
sintomas: [carregando produtos parado, nenhum produto retornado, erro ao carregar produtos, R$ NaN, object Object]
palavras_chave: [produtos_api, fetch, cartao, card, modal, saiba mais, formatarPreco, Number, NaN, data-id, status, grid]
causas_relacionadas: [estado_da_tela_divergente, localizador_quebrado, corpo_vazio, tipo_divergente]
---
## Resumo
produtos_api.php monta os cartões com fetch() em localhost:8000/api/produtos — a única fronteira JSON do cobaia; detalhe via GET /api/produtos/{id}.

## Sinais
- "Carregando..." parado: o fetch nunca resolveu
- "Nenhum produto retornado pela API.": não é lista, ou vazia

## Causa
formatarPreco() usa Number(): preço não numérico sai cru; tipo objeto sai via JSON.stringify; botão button.saiba-mais[data-id].
