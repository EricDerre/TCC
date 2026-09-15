---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (regra de negócio).
# ! Motivo: o login do cliente É o CPF — sem isso o modelo não entende por que o campo
# cpf da API vem de login_usuario nem por que nome/cpf trocados indicam junção errada.
id: usuario-e-login
titulo: Usuário, níveis e login
sistema: Ambos
entidade_principal: Usuario
tipo: funcionamento
status: ativo
arquivos: [Programacao/CobaiaFront/admin/login.php, Programacao/CobaiaFront/admin/acesso_com.php, Programacao/CobaiaAPI/app/models.py]
tabelas: [tbusuarios]
sintomas: [reserva com nome de outro usuario, saudacao vazia, nome incorreto em reservas]
palavras_chave: [usuario, login, cpf, senha, nivel, sup, cli, administrador, cliente, sessao, juncao de usuarios, chave de juncao]
causas_relacionadas: [chave_de_juncao_errada, nulo_inesperado]
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso tra-2) - Revisar: retificação acrescentada.
---
## Resumo
Conta em tbusuarios: login_usuario, senha_usuario, nivel_usuario ('sup' admin, 'cli' cliente). Para o cliente o login é o CPF, que vira o campo cpf da API.

## Sinais
- nome ou cpf de outra pessoa na reserva: junção por id trocada
- saudação "Olá, !" sem nome: nome nulo vindo da view

## Causa
login.php:7 compara a senha em texto puro; 'sup' abre o painel, 'cli' abre cliente/index.php?cliente=<login>, falha vai a invasor.php.

## Notas do modelo
- [E1 · tra-2 · retificação de "nome ou cpf de outra pessoa na reserva: junção por id trocada"] Corrigir a junção entre tbusuarios e tbpedido_reserva para garantir que o nome do usuário correto seja exibido. — Motivo: A evidência deste caso mostrou que o nome incorreto estava sendo exibido devido a uma junção incorreta entre os registros de usuários e reservas. A correção desta junção resolve o problema.
