#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes de replicar_commits_orientador.py (03/11/2026): um repositório de origem com três
# commits e um clone de destino já sincronizado com o primeiro, em pasta temporária; conferem que o ensaio lista só os dois
# commits que faltam sem gravar nada, que `--aplicar` cria no clone um commit por commit de origem (mesma primeira linha,
# rodapé com o hash de origem, data de autoria original) com `projeto/` igual ao commit copiado e o README do clone
# apontando para o último, que um commit que só mexe em arquivo excluído da cópia ainda avança o README, que o script se
# recusa a aplicar com o clone sujo, e que `--desde` substitui a leitura do README.
# ! Motivo: o script roda `git add` e `git commit` no clone do orientador na mão do Eric (decisão 84); se replicasse na
# ordem errada, pulasse um commit ou commitasse com o clone sujo, o histórico do orientador ficaria errado e ninguém veria
# antes do push. Uso: python ferramentas/testar_replicar_commits_orientador.py
"""Testes de replicar_commits_orientador.py: python ferramentas/testar_replicar_commits_orientador.py"""
from __future__ import annotations

import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import replicar_commits_orientador as rc
import sincronizar_orientador as so


def git(pasta: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(pasta), *args], check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout


def novo_repo(pasta: Path) -> None:
    pasta.mkdir(parents=True, exist_ok=True)
    git(pasta, "init", "-q", "-b", "main")
    git(pasta, "config", "user.email", "teste@exemplo.org")
    git(pasta, "config", "user.name", "Teste")
    git(pasta, "config", "core.autocrlf", "false")


def gravar(pasta: Path, rel: str, conteudo: str) -> None:
    p = pasta / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(conteudo.encode("utf-8"))


def commit(pasta: Path, mensagem: str, data: str | None = None) -> str:
    git(pasta, "add", "-A", "-f")
    args = ["commit", "-q", "-m", mensagem]
    if data:
        args += ["--date", data]
    git(pasta, *args)
    return git(pasta, "rev-parse", "HEAD").strip()


class Base(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        raiz = Path(self.tmp.name)
        self.origem, self.destino = raiz / "TCC", raiz / "squad-24-projeto"
        novo_repo(self.origem)
        gravar(self.origem, "README.md", "# Principal v1\n")
        gravar(self.origem, "ferramentas/a.py", "print(1)\n")
        self.c1 = commit(self.origem, "Primeiro commit")
        gravar(self.origem, "ferramentas/a.py", "print(2)\n")
        gravar(self.origem, "Documentacao/novo.md", "novo\n")
        self.c2 = commit(self.origem, "Segundo commit\n\nCorpo com detalhe.", data="2026-10-23T13:20:00-03:00")
        gravar(self.origem, ".claude/settings.json", "{}\n")  # só arquivo excluído da cópia
        self.c3 = commit(self.origem, "Terceiro commit (só .claude)")
        novo_repo(self.destino)
        gravar(self.destino, "README.md", f"# Squad\n\n{so.INICIO}\n(ainda nao)\n{so.FIM}\n")
        commit(self.destino, "esqueleto")
        so.sincronizar(self.origem, self.destino, aplicar=True, commit=self.c1)
        commit(self.destino, "Cópia do primeiro")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def rodar(self, *args: str) -> tuple[int, str]:
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            codigo = rc.main(["--origem", str(self.origem), "--destino", str(self.destino), *args])
        return codigo, saida.getvalue()


class TesteEnsaio(Base):
    def teste_lista_os_que_faltam_sem_gravar(self) -> None:
        codigo, saida = self.rodar()
        self.assertEqual(codigo, 0)
        self.assertIn("2 commit(s) a replicar", saida)
        self.assertIn("Segundo commit", saida)
        self.assertIn("Terceiro commit", saida)
        self.assertNotIn("Primeiro commit", saida)
        self.assertEqual(git(self.destino, "status", "--porcelain").strip(), "")
        self.assertEqual((self.destino / "projeto" / "ferramentas" / "a.py").read_text(encoding="utf-8"), "print(1)\n")
        self.assertEqual(git(self.destino, "rev-list", "--count", "HEAD").strip(), "2")

    def teste_desde_substitui_o_readme(self) -> None:
        codigo, saida = self.rodar("--desde", self.c2)
        self.assertEqual(codigo, 0)
        self.assertIn("1 commit(s) a replicar", saida)
        self.assertIn("Terceiro commit", saida)

    def teste_nada_a_replicar(self) -> None:
        codigo, saida = self.rodar("--desde", self.c3)
        self.assertEqual(codigo, 0)
        self.assertIn("Nada a replicar", saida)


class TesteAplicar(Base):
    def teste_cria_um_commit_por_commit_de_origem(self) -> None:
        codigo, saida = self.rodar("--aplicar")
        self.assertEqual(codigo, 0, saida)
        self.assertEqual(git(self.destino, "rev-list", "--count", "HEAD").strip(), "4")
        assuntos = git(self.destino, "log", "--format=%s", "-2").split("\n")
        self.assertEqual(assuntos[0], "Terceiro commit (só .claude)")
        self.assertEqual(assuntos[1], "Segundo commit")
        corpo2 = git(self.destino, "log", "-1", "--format=%B", "HEAD~1")
        self.assertIn("Corpo com detalhe.", corpo2)
        self.assertIn(f"Réplica do commit {self.c2[:7]}", corpo2)
        self.assertIn("23/10/2026", corpo2)
        self.assertEqual(git(self.destino, "log", "-1", "--format=%ad", "--date=format:%Y-%m-%d %H:%M", "HEAD~1").strip(),
                         "2026-10-23 13:20")
        self.assertEqual((self.destino / "projeto" / "ferramentas" / "a.py").read_text(encoding="utf-8"), "print(2)\n")
        self.assertTrue((self.destino / "projeto" / "Documentacao" / "novo.md").exists())
        self.assertFalse((self.destino / "projeto" / ".claude").exists())
        readme = (self.destino / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"commit `{self.c3[:7]}`", readme)
        self.assertEqual(git(self.destino, "status", "--porcelain").strip(), "")
        codigo, saida = self.rodar()
        self.assertIn("Nada a replicar", saida)

    def teste_recusa_clone_sujo(self) -> None:
        gravar(self.destino, "docs/solto.md", "sem commit\n")
        codigo, _ = self.rodar("--aplicar")
        self.assertEqual(codigo, 2)
        self.assertEqual(git(self.destino, "rev-list", "--count", "HEAD").strip(), "2")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    unittest.main(verbosity=1)
