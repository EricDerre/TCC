---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: o modo field_renamed acrescenta o sufixo _v2; a distinção para campo_ausente é
# a chave nova com o mesmo valor. Conferido em fault_injection.py.
id: campo_renomeado
titulo: Campo renomeado
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: campo_renomeado
arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaAPI/app/schemas.py]
endpoints: [GET /api/produtos, GET /api/pedidos]
sintomas: [chave desconhecida no lugar da esperada, _v2, campo com outro nome, titulo vazio, preco e categoria corretos]
palavras_chave: [renomead, outro nome, _v2, descricao, situacao, imagem_url, field_renamed, chave inesperada, renomeacao, campo-alvo, injeccao de falha]
causas_relacionadas: [campo_ausente, estrutura_aninhada_divergente]
# ! Alteração por modelo qwen2.5-coder:7b (E3, caso sin-9) - Revisar: nota acrescentada.
---
## Resumo
O valor existe sob outra chave: falta a esperada e aparece uma desconhecida com o mesmo tipo e conteúdo (preco → preco_v2, nome → descricao, status → situacao).

## Sinais
- o resto do objeto confere; uma chave sumiu e outra sobrou
- vazio ou undefined só naquele campo

## Causa
O modo field_renamed troca o campo-alvo por <campo>_v2 (fault_injection.py). Fora dele: contrato mudou no servidor sem atualizar o cliente.

## Notas do modelo
- [E3 · sin-9 · nota] Adicionar nota explicando que o campo "nome" foi renomeado para "descricao" em versões mais recentes do sistema. — Motivo: Esta nota ajudará a explicar a renomeação do campo, permitindo que os desenvolvedores futuros entendam a mudança e evitem diagnósticos incorretos.
