#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/10/2026, Fase 4, pacote P2): recria o banco `ti93phpdb01` a partir dos
# três .sql do CobaiaFront (`DROP DATABASE IF EXISTS` e depois `install.apply_sql_files`, os mesmos passos do
# instalador), subindo o MariaDB pelo mesmo caminho de `run.py` (`_env_common.ensure_mariadb_running`) e conferindo
# as contagens do seed no fim (4 tipos, 14 produtos, 2 usuários, 0 reservas).
# ! Motivo: a Fase 4 e a Fase 5 rodam cenários que mexem no banco (reserva do cliente; `*_excluir.php` e
# `cliente_cancelar.php` são GET destrutivos sem sessão) e o protocolo do projeto ABNT (§3.4) exige o banco restaurado
# entre execuções; até aqui só havia o `install.py`, que reaplica os .sql por cima do que sobrou, sem apagar.
"""Uso (de qualquer pasta): python restaurar_banco.py [--manter-servidor]
Sobe o MariaDB se preciso, apaga e recria `ti93phpdb01` com schema e seed, imprime as contagens e, salvo
--manter-servidor, desliga o servidor que este processo subiu. Código de saída 1 se as contagens não forem as do seed."""
import argparse
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

import _env_common as env  # noqa: E402
import install  # noqa: E402

BANCO = "ti93phpdb01"
TABELAS = ("tbtipos", "tbprodutos", "tbusuarios", "tbpedido_reserva")
CONTAGENS_DO_SEED = {"tbtipos": 4, "tbprodutos": 14, "tbusuarios": 2, "tbpedido_reserva": 0}


def executar_sql(cli: str, sql: str) -> str:
    """Roda um comando SQL como root pelo cliente de linha de comando e devolve a saída sem cabeçalho."""
    r = subprocess.run([cli, "-u", "root", "--batch", "--skip-column-names", "-e", sql],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"SQL falhou (código {r.returncode}): {r.stderr.strip()[:300]}")
    return r.stdout


def contar(cli: str, banco: str = BANCO) -> dict[str, int]:
    """Quantas linhas há em cada tabela do seed."""
    sql = "SELECT " + ", ".join(f"(SELECT COUNT(*) FROM `{banco}`.`{t}`)" for t in TABELAS) + ";"
    valores = executar_sql(cli, sql).split()
    return dict(zip(TABELAS, (int(v) for v in valores)))


def restaurar(cli: str | None = None) -> dict[str, int]:
    """Apaga e recria o banco com os três .sql do CobaiaFront; devolve as contagens depois."""
    cli = cli or env.find_mysql_cli()
    if not cli:
        raise RuntimeError("cliente do MariaDB não encontrado; rode install.py (ou install.ps1) primeiro")
    if not env.ensure_mariadb_running(cli):
        raise RuntimeError("o MariaDB não respondeu; veja as mensagens acima")
    executar_sql(cli, f"DROP DATABASE IF EXISTS `{BANCO}`;")
    install.apply_sql_files(cli)
    return contar(cli)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manter-servidor", action="store_true", dest="manter_servidor",
                    help="não desliga o MariaDB no fim, mesmo que este processo o tenha subido")
    args = ap.parse_args()
    try:
        contagens = restaurar()
    finally:
        if not args.manter_servidor:
            env.stop_managed_mariadbd()
    for tabela in TABELAS:
        print(f"{tabela}: {contagens[tabela]}")
    if contagens != CONTAGENS_DO_SEED:
        print(f"ATENÇÃO: as contagens não são as do seed esperado {CONTAGENS_DO_SEED}")
        return 1
    print(f"banco {BANCO} restaurado ao seed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
