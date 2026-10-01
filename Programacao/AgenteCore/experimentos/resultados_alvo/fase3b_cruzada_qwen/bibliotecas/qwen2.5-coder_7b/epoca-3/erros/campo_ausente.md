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
sintomas: [cartao sem titulo, sem nome, undefined na tela, botao que nao faz nada, nulo_inesperado, undefined no botao de preco]
palavras_chave: [ausente, falta, faltando, sem o campo, undefined, field_missing, chave, front-end, json, campo ausente, formatacao]
causas_relacionadas: [campo_renomeado, nulo_inesperado, estrutura_aninhada_divergente]
# ! Alteração por modelo qwen2.5:7b (E1, caso sin-1) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E3, caso sin-1) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E3, caso sin-6) - Revisar: nota acrescentada.
---
## Resumo
Uma chave do contrato não vem no objeto — nem com nulo. No JavaScript a leitura vira undefined.

## Sinais
- nome ausente: cartão "(sem nome)"; preço ausente: botão imprime "undefined"
- id ausente: botão de detalhe ou cancelar sem identificador, clique sem efeito

## Causa
O modo field_missing remove o campo-alvo (fault_injection.py). Diferença para campo_renomeado: nenhuma chave nova aparece no lugar.

## Notas do modelo
- [E1 · sin-1 · nota] Adicionar nota sobre a remoção de campos no fault_injection.py. — Motivo: O caso demonstrou que a remoção de campos pode causar sintomas como 'undefined', indicando a necessidade de documentar melhor esse cenário.
- [E3 · sin-1 · nota] Adicionar nota sobre a remoção de campos no fault_injection.py e a necessidade de formatação correta do preço no front-end. — Motivo: O sintoma mostrou que o campo preco estava ausente, indicando a necessidade de notas adicionais na documentação.
- [E3 · sin-6 · nota] Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. — Motivo: O sintoma mostrou que a falta do campo "nome" causou o problema, e a nota ajudaria a prevenir futuros diagnósticos semelhantes.
