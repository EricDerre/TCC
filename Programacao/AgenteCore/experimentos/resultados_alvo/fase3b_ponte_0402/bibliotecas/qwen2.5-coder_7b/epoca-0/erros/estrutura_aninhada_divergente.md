---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: a página checa Array.isArray e imprime objetos com JSON.stringify — é o que
# torna cada forma de aninhamento visível de um jeito. Conferido em produtos_api.php.
id: estrutura_aninhada_divergente
titulo: Estrutura aninhada divergente
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: estrutura_aninhada_divergente
arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/schemas.py]
endpoints: [GET /api/produtos]
sintomas: [object Object, envelope data, lista dentro de objeto, campo virou objeto]
palavras_chave: [aninhad, envelope, data, itens, objeto, nivel, profundidade, object Object, stringify]
causas_relacionadas: [colecao_no_lugar_de_objeto, campo_renomeado, contagem_inconsistente]
---
## Resumo
Chaves existem, mas noutro nível: lista num envelope ({"data": {"itens": [...]}}) ou campo simples como objeto ({"id": 1, "nome": "Carnes"}).

## Sinais
- envelope na raiz: Array.isArray falha, "Nenhum produto retornado"
- campo como objeto: cartão imprime [object Object]

## Causa
Contrato real: lista crua na raiz e tipo como texto (produtos.py _to_dict); envelope ou aninhamento veio de outra versão ou intermediário.
