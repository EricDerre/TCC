---
# ! Alteração de IA - Revisar: índice mensagem literal → ponto do código → causa (Fase 2-B).
# ! Motivo: é o "caminho pré-definido" pedido para a biblioteca — a mensagem que o usuário
# vê leva direto ao arquivo e à causa. Todas conferidas nos fontes citados.
id: mensagens-de-erro-do-codigo
titulo: Índice de mensagens literais do código
sistema: Ambos
entidade_principal: Infraestrutura
tipo: funcionamento
status: ativo
arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/routers/admin_fault.py, Programacao/CobaiaFront/rodape_contato_envia.php]
sintomas: [mensagem de erro na tela, detail no json de erro]
palavras_chave: [mensagem, literal, detail, erro ao carregar, nenhum produto retornado, atencao erro, token invalido, modo invalido, falha no email, indice]
causas_relacionadas: [recurso_inexistente, erro_interno_do_servidor, corpo_nao_e_json, corpo_vazio, estado_da_tela_divergente]
---
## Resumo
Página: "Carregando produtos da CobaiaAPI..."; "Nenhum produto retornado pela API." (não é lista, ou vazia); "Erro ao carregar produtos da CobaiaAPI: <msg>" ("HTTP <n>" se resp.ok falso). API: "produto/cliente/pedido não encontrado" (404), "token inválido" (403), "modo inválido" (400), "fault injection: error_500 em <ent>" (500). PHP: "Atenção ERRO: ..." (connect.php:16), "falha no email" (rodape_contato_envia.php:33).
