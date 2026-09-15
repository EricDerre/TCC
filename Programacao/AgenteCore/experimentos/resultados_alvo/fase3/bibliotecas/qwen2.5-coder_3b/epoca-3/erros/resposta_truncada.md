---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: o modo malformed_json produz exatamente isso; conferido em produtos.py:19.
id: resposta_truncada
titulo: Resposta truncada
sistema: CobaiaAPI
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: resposta_truncada
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py]
sintomas: [fim inesperado da entrada, json cortado, content-length menor que o corpo, parse falha, json invalido]
palavras_chave: [truncad, cortad, incomplet, unexpected end, content-length, tamanho, parcial, malformed_json, json parsing, api falha]
causas_relacionadas: [corpo_nao_e_json, corpo_vazio, tempo_de_resposta_excedido]
# ! Alteração por modelo qwen2.5-coder:3b (E2, caso lex-14) - Revisar: retificação acrescentada.
---
## Resumo
O corpo começa como JSON válido e termina no meio de um valor ou chave — faltam bytes; o parse falha com "Unexpected end of JSON input".

## Sinais
- primeiros itens íntegros, o último cortado ou sem o colchete final
- Content-Length menor que o esperado

## Causa
O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio.

## Notas do modelo
- [E2 · lex-14 · retificação de "o parse falha com 'Unexpected end of JSON input'."] Corrigir o parsing JSON para lidar com erros de truncamento. — Motivo: O erro de truncamento pode ser causado por problemas de comunicação, então melhorar o parsing JSON ajuda a evitar erros futuros.
