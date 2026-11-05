---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: o modo field_renamed acrescenta o sufixo _v2; a distinção para campo_ausente é
# a chave nova com o mesmo valor. Conferido em fault_injection.py.
id: campo_renomeado
titulo: Campo renomeado
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: corrigido
causa_raiz: campo_renomeado
arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaAPI/app/schemas.py]
endpoints: [GET /api/produtos, GET /api/pedidos]
sintomas: [chave desconhecida no lugar da esperada, _v2, campo com outro nome, titulo vazio, nome correto, categoria e preco corretos]
palavras_chave: [renomead, outro nome, _v2, descricao, situacao, imagem_url, field_renamed, chave inesperada, campo-renomeado, contrato, cliente]
causas_relacionadas: [campo_ausente, estrutura_aninhada_divergente]
# ! Alteração por modelo qwen2.5:7b (E1, caso sin-9) - Revisar: retificação acrescentada.
# ! Alteração pelo harness da Fase 4 (correção, caso sin-9, 2026-11-04) - Revisar: status avançou de ativo para corrigido.
---
## Resumo
O valor existe sob outra chave: falta a esperada e aparece uma desconhecida com o mesmo tipo e conteúdo (preco → preco_v2, nome → descricao, status → situacao).

## Sinais
- o resto do objeto confere; uma chave sumiu e outra sobrou
- vazio ou undefined só naquele campo

## Causa
O modo field_renamed troca o campo-alvo por <campo>_v2 (fault_injection.py). Fora dele: contrato mudou no servidor sem atualizar o cliente.

## Solução sugerida
- [sin-9 · 2026-11-04] Corrigir a afirmação para "Contrato mudou no servidor sem atualizar o cliente e API não reflete as mudanças."

## Solução aplicada
- [sin-9 · 2026-11-04] Em 2026-11-04, o cenário api-catalogo do caso sin-9 voltou a passar com o modo field_renamed desligado: no fio, o campo nome voltou ao corpo; 1 diferença contra o contrato antes e 0 depois; na tela, 3 linhas da árvore voltaram e 3 sumiram.

## Notas do modelo
- [E1 · sin-9 · retificação de "Fora dele: contrato mudou no servidor sem atualizar o cliente."] Corrigir a afirmação para "Contrato mudou no servidor sem atualizar o cliente e API não reflete as mudanças." — Motivo: O caso mostrou que a documentação não refletiu a necessidade de atualizar o cliente quando o contrato muda, causando a renomeação do campo sem que o cliente o refletisse.
