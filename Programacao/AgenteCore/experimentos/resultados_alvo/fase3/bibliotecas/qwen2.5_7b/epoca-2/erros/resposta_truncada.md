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
sintomas: [fim inesperado da entrada, json cortado, content-length menor que o corpo, lista incompleta, ultimo item cortado, corpo cortado]
palavras_chave: [truncad, cortad, incomplet, unexpected end, content-length, tamanho, parcial, malformed_json, truncamento, conexao, proxy]
causas_relacionadas: [corpo_nao_e_json, corpo_vazio, tempo_de_resposta_excedido]
# ! Alteração por modelo qwen2.5:7b (E1, caso lex-5) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5:7b (E1, caso lex-14) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E2, caso lex-14) - Revisar: retificação acrescentada.
---
## Resumo
O corpo começa como JSON válido e termina no meio de um valor ou chave — faltam bytes; o parse falha com "Unexpected end of JSON input".

## Sinais
- primeiros itens íntegros, o último cortado ou sem o colchete final
- Content-Length menor que o esperado

## Causa
O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio.

## Notas do modelo
- [E1 · lex-5 · retificação de "Fora dele: limite num proxy, conexão encerrada durante o envio."] Corrigir a descrição para incluir que o truncamento pode ser causado por limites de proxy ou interrupção de conexão. — Motivo: Esclarecer que limites de proxy ou interrupção de conexão podem causar truncamento, ajudando a diagnosticar casos futuros.
- [E1 · lex-14 · nota] Adicione um exemplo de como verificar o Content-Length na documentação para evitar esse problema. — Motivo: Este caso mostrou que a verificação do Content-Length é crucial para detectar respostas truncadas, e a documentação não aborda isso explicitamente.
- [E2 · lex-14 · retificação de "Fora dele: limite num proxy, conexão encerrada durante o envio."] Corrigir a descrição para incluir que o truncamento pode ser causado por limites de proxy ou interrupção de conexão. Adicione um exemplo de como verificar o Content-Length na documentação para evitar esse problema. — Motivo: Este caso mostrou que a documentação não abrangia todas as possíveis causas de truncamento da resposta, especificamente relacionadas a limites de proxy ou interrupção de conexão.
