---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: a página checa Array.isArray e imprime objetos com JSON.stringify — é o que
# torna cada forma de aninhamento visível de um jeito. Conferido em produtos_api.php.
id: estrutura_aninhada_divergente
titulo: Estrutura aninhada divergente
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: corrigido
causa_raiz: estrutura_aninhada_divergente
arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/schemas.py]
endpoints: [GET /api/produtos]
sintomas: [object Object, envelope data, lista dentro de objeto, campo virou objeto, envelope na raiz, campo como objeto]
palavras_chave: [aninhad, envelope, data, itens, objeto, nivel, profundidade, object Object, stringify, estrutura, aninhamento, divergencia]
causas_relacionadas: [colecao_no_lugar_de_objeto, campo_renomeado, contagem_inconsistente]
# ! Alteração por modelo qwen2.5:7b (E1, caso sin-13) - Revisar: retificação acrescentada.
# ! Alteração pelo harness da Fase 4 (correção, caso sin-13, 2026-11-04) - Revisar: status avançou de ativo para corrigido.
---
## Resumo
Chaves existem, mas noutro nível: lista num envelope ({"data": {"itens": [...]}}) ou campo simples como objeto ({"id": 1, "nome": "Carnes"}).

## Sinais
- envelope na raiz: Array.isArray falha, "Nenhum produto retornado"
- campo como objeto: cartão imprime [object Object]

## Causa
Contrato real: lista crua na raiz e tipo como texto (produtos.py _to_dict); envelope ou aninhamento veio de outra versão ou intermediário.

## Solução sugerida
- [sin-13 · 2026-11-04] Adicionar exemplo de estrutura aninhada divergente no verbete.

## Solução aplicada
- [sin-13 · 2026-11-04] Em 2026-11-04, o cenário api-catalogo do caso sin-13 voltou a passar com o modo estrutura_aninhada_divergente desligado: no fio, o campo tipo voltou ao corpo; 1 diferença contra o contrato antes e 0 depois; 14 valores voltaram ao da referência; na tela, 3 linhas da árvore voltaram e 3 sumiram.

## Notas do modelo
- [E1 · sin-13 · retificação de "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'})."] Adicionar exemplo de estrutura aninhada divergente no verbete. — Motivo: O exemplo de sintoma observado mostrou que a estrutura pode variar entre um envelope e um campo simples, necessitando de um exemplo explícito no verbete.
