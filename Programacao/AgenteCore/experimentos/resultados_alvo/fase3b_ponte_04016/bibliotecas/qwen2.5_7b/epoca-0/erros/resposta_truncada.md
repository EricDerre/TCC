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
sintomas: [fim inesperado da entrada, json cortado, content-length menor que o corpo]
palavras_chave: [truncad, cortad, incomplet, unexpected end, content-length, tamanho, parcial, malformed_json]
causas_relacionadas: [corpo_nao_e_json, corpo_vazio, tempo_de_resposta_excedido]
---
## Resumo
O corpo começa como JSON válido e termina no meio de um valor ou chave — faltam bytes; o parse falha com "Unexpected end of JSON input".

## Sinais
- primeiros itens íntegros, o último cortado ou sem o colchete final
- Content-Length menor que o esperado

## Causa
O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio.
