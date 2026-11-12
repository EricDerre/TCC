---
# ! Alteração de IA - Revisar: camada de leitura do verbete `usuario-e-login`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/negocio/usuario-e-login.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
id: usuario-e-login
titulo: Usuário, níveis e login
sistema: Ambos
entidade_principal: Usuario
tipo: funcionamento
status: ativo
arquivos: [Programacao/CobaiaFront/admin/login.php, Programacao/CobaiaFront/admin/acesso_com.php, Programacao/CobaiaAPI/app/models.py]
tabelas: [tbusuarios]
sintomas: [reserva com nome de outro usuario, saudacao vazia]
palavras_chave: [usuario, login, cpf, senha, nivel, sup, cli, administrador, cliente, sessao]
causas_relacionadas: [chave_de_juncao_errada, nulo_inesperado]
verbete: negocio/usuario-e-login.md
hash_do_verbete: 025768294ef1cbfd
gerado_em: 2026-11-07
curado: sim
---

# Usuário, níveis e login

Camada de leitura do verbete `usuario-e-login` (`biblioteca_producao/negocio/usuario-e-login.md`). Tipo: funcionamento (descreve como uma parte do sistema funciona); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Usuario.

## O que é

Conta em tbusuarios: login_usuario, senha_usuario, nivel_usuario ('sup' admin, 'cli' cliente). Para o cliente o login é o CPF, que vira o campo cpf da API.

## Como aparece na tela

- nome ou cpf de outra pessoa na reserva: junção por id trocada.
- saudação "Olá, !" sem nome: nome nulo vindo da view.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `reserva com nome de outro usuario`, `saudacao vazia`.

## O que conferir

Causa, como o verbete a descreve: login.php:7 compara a senha em texto puro; 'sup' abre o painel, 'cli' abre cliente/index.php?cliente=<login>, falha vai a invasor.php.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `chave_de_juncao_errada` (Chave de junção errada), `nulo_inesperado` (Nulo inesperado).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/admin/login.php`, `Programacao/CobaiaFront/admin/acesso_com.php`, `Programacao/CobaiaAPI/app/models.py`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: `tbusuarios`.
- Palavras que a busca usa para achar este verbete: `usuario`, `login`, `cpf`, `senha`, `nivel`, `sup`, `cli`, `administrador`, `cliente`, `sessao`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
