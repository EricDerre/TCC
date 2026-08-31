-- ! Alteração de IA - Revisar
-- Completa o schema de bancoatualizado.sql: tbusuarios.nome/cpf/nivel 'cli',
-- tabela tbpedido_reserva e view vw_tbpedidos, usadas por cliente/*.php e
-- admin/login.php mas ausentes do dump original. Colunas conferidas
-- diretamente no código-fonte (cliente/registrar_reserva.php, reserva_cli.php,
-- cliente_cancelar.php, cliente/index.php, admin/login.php).
--
-- Idempotente: seguro rodar mais de uma vez.

USE `ti93phpdb01`;

-- tbusuarios só tinha login_usuario/senha_usuario/nivel_usuario ('sup' único
-- valor possível) — sem isso, uma conta de cliente é fisicamente impossível,
-- e vw_tbpedidos (abaixo) não tem de onde tirar nome/cpf.
SET @col_exists := (
  SELECT COUNT(*) FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = 'ti93phpdb01' AND TABLE_NAME = 'tbusuarios' AND COLUMN_NAME = 'nome'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `tbusuarios` ADD COLUMN `nome` VARCHAR(100) NOT NULL DEFAULT '''' AFTER `login_usuario`',
  'SELECT ''tbusuarios.nome ja existe'''
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

ALTER TABLE `tbusuarios`
  MODIFY COLUMN `nivel_usuario` ENUM('sup','cli') NOT NULL;

-- tbpedido_reserva: INSERT em cliente/registrar_reserva.php, SELECT em
-- cliente/reserva_cli.php, UPDATE em cliente/cliente_cancelar.php.
CREATE TABLE IF NOT EXISTS `tbpedido_reserva` (
  `id_pedido`    INT(11) NOT NULL AUTO_INCREMENT,
  `id_clientes`  INT(11) NOT NULL,
  `pessoas`      INT(11) NOT NULL,
  `data_pedido`  DATE NOT NULL,
  `status`       ENUM('Em Análise','Cancelado') NOT NULL DEFAULT 'Em Análise',
  PRIMARY KEY (`id_pedido`),
  INDEX `id_clientes_fk` (`id_clientes` ASC),
  CONSTRAINT `id_clientes_fk` FOREIGN KEY (`id_clientes`)
    REFERENCES `tbusuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
-- utf8 (nao utf8mb4): precisa casar collation com tbusuarios pro JOIN da view abaixo.

-- vw_tbpedidos: usada por cliente/index.php e cliente/registrar_reserva.php
-- (filtro "where cpf like '%login%'", e leitura de nome/id_clientes).
--
-- LEFT JOIN a partir de tbusuarios (não JOIN normal a partir de
-- tbpedido_reserva): testado ao vivo — com INNER JOIN, um cliente recém
-- criado sem nenhuma reserva some inteiramente da view, e cliente/index.php
-- quebra com "Trying to access array offset on value of type null" ao tentar
-- ler $row['nome'] pra saudação (fetch_assoc retorna null com 0 linhas).
-- Também usa u.id_usuario (não pr.id_clientes) como id_clientes, pra esse
-- campo continuar correto mesmo sem reserva — senão a primeira reserva de um
-- cliente novo tentaria gravar id_clientes vazio (viola a FK, falha
-- silenciosamente já que mysqli não lança exceção por padrão).
CREATE OR REPLACE VIEW `vw_tbpedidos` AS
SELECT pr.id_pedido, u.id_usuario AS id_clientes, pr.pessoas, pr.data_pedido, pr.status,
       u.nome, u.login_usuario AS cpf
FROM `tbusuarios` u
LEFT JOIN `tbpedido_reserva` pr ON pr.id_clientes = u.id_usuario;
