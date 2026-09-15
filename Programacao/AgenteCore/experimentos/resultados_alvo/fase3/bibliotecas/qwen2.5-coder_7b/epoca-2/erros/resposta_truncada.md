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
sintomas: [fim inesperado da entrada, json cortado, content-length menor que o corpo, resposta incompleta, content-length inconsistente, listagem incompleta]
palavras_chave: [truncad, cortad, incomplet, unexpected end, content-length, tamanho, parcial, malformed_json, resposta truncada, proxy, conexao]
causas_relacionadas: [corpo_nao_e_json, corpo_vazio, tempo_de_resposta_excedido]
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso lex-5) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso lex-14) - Revisar: nota acrescentada.
---
## Resumo
O corpo começa como JSON válido e termina no meio de um valor ou chave — faltam bytes; o parse falha com "Unexpected end of JSON input".

## Sinais
- primeiros itens íntegros, o último cortado ou sem o colchete final
- Content-Length menor que o esperado

## Causa
O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio.

## Notas do modelo
- [E1 · lex-5 · retificação de "Content-Length menor que o esperado."] Adicionar verificação de Content-Length em produtos.py para garantir que a resposta não seja truncada. — Motivo: A verificação de Content-Length ajuda a identificar e corrigir casos de resposta truncada, garantindo que a resposta completa seja enviada ao cliente.
- [E1 · lex-14 · nota] Adicionar nota explicando que a resposta pode ser truncada devido a limites de proxy ou conexões interrompidas. — Motivo: Esta nota ajudará a explicar a causa raiz da falha, que é a resposta truncada, e como ela pode ocorrer, facilitando o diagnóstico futuro.
