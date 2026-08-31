-- ! Alteração de IA - Revisar
-- Dados de demonstração. bancoatualizado.sql não tem nenhum INSERT — sem
-- isso o site sobe vazio e nem dá pra logar (nenhum usuário admin existe).
-- Nomes de arquivo de imagem conferidos em Programacao/CobaiaFront/images/.
--
-- Idempotente: usa INSERT IGNORE / checagem de existência, seguro rodar 2x.

USE `ti93phpdb01`;

INSERT IGNORE INTO tbtipos (id_tipo, sigla_tipo, rotulo_tipo) VALUES
 (1,'CAR','Carnes'),
 (2,'BEB','Bebidas'),
 (3,'ACO','Acompanhamentos'),
 (4,'SOB','Sobremesas');

INSERT IGNORE INTO tbprodutos (id_produto, id_tipo_produto, descri_produto, resumo_produto, valor_produto, imagem_produto, destaque_produto) VALUES
 (1, 1, 'Picanha ao Alho',      'Picanha grelhada com alho laminado na brasa',        89.90, 'picanha_alho.jpg',  'Sim'),
 (2, 1, 'Picanha Simples',      'Corte nobre grelhado no ponto',                       84.90, 'picanha_sem.jpg',   'Não'),
 (3, 1, 'Fraldinha',            'Corte grelhado na brasa, fatiado na hora',            69.90, 'fraldinha.jpg',     'Não'),
 (4, 1, 'Costelona',            'Costela assada lentamente por horas',                 79.90, 'costelona.jpg',     'Sim'),
 (5, 1, 'Alcatra na Pedra',     'Alcatra grelhada servida na pedra quente',            74.90, 'alcatra_pedra.jpg', 'Não'),
 (6, 1, 'Maminha',              'Corte macio grelhado na brasa',                       72.90, 'maminha.jpg',       'Não'),
 (7, 1, 'Cupim',                'Cupim assado lentamente, bem macio',                  76.90, 'cupim.jpg',         'Sim'),
 (8, 2, 'Água Mineral',         'Garrafa 500ml, com ou sem gás',                        6.00, 'agua.png',          'Não'),
 (9, 2, 'Balde de Cerveja',     '5 long necks geladas',                                45.00, 'balde_cerveja.png', 'Sim'),
 (10,2, 'Refrigerante',         'Lata 350ml, diversos sabores',                         7.00, 'refrigerante.png',  'Não'),
 (11,3, 'Pão de Alho',          'Pão de alho grelhado na brasa',                       16.90, 'paodealho.png',     'Não'),
 (12,3, 'Queijo Coalho',        'Queijo coalho grelhado com mel',                      22.90, 'queijo.png',        'Sim'),
 (13,3, 'Hambúrguer Artesanal', 'Blend da casa, pão brioche',                          32.90, 'hamburger.png',     'Não'),
 (14,4, 'Abacaxi na Brasa',     'Com canela e açúcar',                                 14.90, 'abacaxi.jpg',       'Não');

-- Senha em TEXTO PURO de propósito: admin/usuario_insere.php grava assim, e
-- admin/login.php compara sem hash nenhum — usar md5()/hash aqui quebraria o
-- login (ver inconsistência conhecida documentada no plano).
INSERT IGNORE INTO tbusuarios (id_usuario, login_usuario, nome, senha_usuario, nivel_usuario) VALUES
 (1, 'admin', 'Administrador', 'admin123', 'sup'),
 (2, '11122233344', 'Cliente Teste', '123456', 'cli');
