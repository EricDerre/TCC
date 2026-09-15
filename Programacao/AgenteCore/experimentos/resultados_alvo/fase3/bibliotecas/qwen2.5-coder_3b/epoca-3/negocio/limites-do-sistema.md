---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (o que o sistema NÃO faz).
# ! Motivo: pedido explícito do desenho — documentação comum omite as ausências, e é
# justamente a falta de validação e de checagem que explica dado inválido gravado sem erro.
id: limites-do-sistema
titulo: O que o sistema não faz
sistema: Ambos
entidade_principal: Infraestrutura
tipo: limite
status: ativo
arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/schemas.py]
sintomas: [dado invalido gravado, falha silenciosa, contrato do docs diferente da resposta]
palavras_chave: [validacao, servidor, silencioso, checagem, hash, response_model, docs, declarado, real]
causas_relacionadas: [valor_fora_do_dominio, campo_ausente, tipo_divergente, dado_desatualizado]
---
## Resumo
Não valida data nem pessoas no servidor; não confere o retorno de $conn->query() em página nenhuma; não checa se a reserva cancelada é do cliente; não faz hash da senha no login.

## Sinais
- dado inválido gravado sem mensagem
- redireciona como se tivesse gravado e nada mudou: SQL falhou em silêncio

## Causa
A API não revalida a resposta: rotas devolvem JSONResponse cru (produtos.py:1-7); o /docs mostra o esperado, não o que sai pela rede.
