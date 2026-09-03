---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (defeito conhecido).
# ! Motivo: inconsistência real entre cadastro, edição e login, mantida de propósito;
# explica por que uma conta editada pelo painel deixa de entrar. Conferido nos três php.
id: senha-sem-hash
titulo: Senha em texto puro, MD5 na edição, sem hash no login
sistema: CobaiaFront
entidade_principal: Usuario
tipo: defeito_conhecido
status: nao_corrigido
arquivos: [Programacao/CobaiaFront/admin/usuario_insere.php, Programacao/CobaiaFront/admin/usuario_atualiza.php, Programacao/CobaiaFront/admin/login.php]
tabelas: [tbusuarios]
sintomas: [usuario nao consegue entrar apos edicao, redirecionado para invasor]
palavras_chave: [senha, md5, hash, texto puro, login, invasor, usuario_insere, usuario_atualiza]
causas_relacionadas: [estado_da_tela_divergente, valor_fora_do_dominio]
---
## Resumo
Cadastro grava senha em texto puro (usuario_insere.php), edição grava MD5 (usuario_atualiza.php), login compara sem hash (login.php:7). Mantido de propósito.

## Sinais
- usuário deixa de entrar depois de editado no painel

## Causa
Após edição a senha guardada é MD5 e o login compara com o texto digitado — nunca bate; cai em invasor.php. As contas do seed estão em texto puro e funcionam.
