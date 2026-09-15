---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: descreve o que o JS faz com um campo que falta (undefined), conferido em
# produtos_api.php, e o modo field_missing que produz o sintoma.
id: campo_ausente
titulo: Campo ausente
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: campo_ausente
arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
endpoints: [GET /api/produtos, GET /api/pedidos]
sintomas: [cartao sem titulo, sem nome, undefined na tela, botao que nao faz nada, cartoes sem titulo]
palavras_chave: [ausente, falta, faltando, sem o campo, undefined, field_missing, chave, campo ausente, nome, contrato api]
causas_relacionadas: [campo_renomeado, nulo_inesperado, estrutura_aninhada_divergente]
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso sin-6) - Revisar: nota acrescentada.
---
## Resumo
Uma chave do contrato não vem no objeto — nem com nulo. No JavaScript a leitura vira undefined.

## Sinais
- nome ausente: cartão "(sem nome)"; preço ausente: botão imprime "undefined"
- id ausente: botão de detalhe ou cancelar sem identificador, clique sem efeito

## Causa
O modo field_missing remove o campo-alvo (fault_injection.py). Diferença para campo_renomeado: nenhuma chave nova aparece no lugar.

## Notas do modelo
- [E1 · sin-6 · nota] Adicionar nota em [campo_ausente] explicando que o campo "nome" pode estar ausente em respostas da API, causando cartões sem título. — Motivo: Esta nota ajuda a identificar rapidamente a causa da falha, pois o campo "nome" é essencial para o título dos cartões.
