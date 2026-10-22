#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes de sincronizar_orientador.py (22/10/2026): um repositório de origem e um clone de
# destino criados em pasta temporária com `git init`; conferem que a cópia leva só os arquivos rastreados do commit HEAD
# para `projeto/` (não o que está na pasta de trabalho sem commit), que a `.venv` da CobaiaAPI e a `.claude/` ficam de fora,
# que o que saiu do principal é apagado da cópia, que nada fora de `projeto/` é tocado, que o bloco SINCRONIZACAO do README
# do clone recebe o commit e a contagem (mantendo CRLF se o README tiver CRLF), que `--check` devolve 1 fora de sincronia
# e 0 em sincronia, e que arquivo copiado que o `.gitignore` do clone ignoraria é avisado.
# ! Motivo: o Eric commita a cópia no repositório do orientador sem reler os milhares de arquivos; se o script copiasse
# um arquivo editado sem commit, esquecesse de apagar o que saiu ou gravasse fora de `projeto/`, ninguém perceberia antes
# do push. Uso: python ferramentas/testar_sincronizar_orientador.py
"""Testes de sincronizar_orientador.py: python ferramentas/testar_sincronizar_orientador.py"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sincronizar_orientador as so  # noqa: E402

MARCADORES = f"{so.INICIO}\nUltima sincronizacao: (ainda nao executada)\n{so.FIM}\n"
ARQUIVOS = {
    "README.md": "# Principal\n",
    ".gitignore": "*.log\n.venv/\n",
    "Documentacao/Projeto de Pesquisa - ABNT 15287_2025 - V3.md": "# Projeto\n\nTexto com acentuação: ção, ã, é.\n",
    "ferramentas/a.py": "print('a')\n",
    "Programacao/AgenteCore/dados.jsonl": b'{"x": 1}\n{"y": 2}\n',
    "Programacao/AgenteCore/bateria.log": "linha 1\n",
}
EXCLUIDOS = {
    "Programacao/CobaiaAPI/.venv/Scripts/ruff.exe": b"\x00\x01\x02binario",
    ".claude/settings.json": "{}\n",
}


def git(pasta: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(pasta), *args], check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout


def novo_repo(pasta: Path) -> None:
    pasta.mkdir(parents=True, exist_ok=True)
    git(pasta, "init", "-q", "-b", "main")
    git(pasta, "config", "user.email", "teste@exemplo.org")
    git(pasta, "config", "user.name", "Teste")
    git(pasta, "config", "core.autocrlf", "false")


def gravar(pasta: Path, rel: str, conteudo: str | bytes) -> Path:
    p = pasta / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(conteudo, bytes):
        p.write_bytes(conteudo)
    else:
        p.write_bytes(conteudo.encode("utf-8"))
    return p


def commit(pasta: Path, mensagem: str) -> str:
    git(pasta, "add", "-A", "-f")  # -f: a .venv e o .log entram de propósito, como no repositório real
    git(pasta, "commit", "-q", "-m", mensagem)
    return git(pasta, "rev-parse", "--short", "HEAD").strip()


class Base(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        raiz = Path(self.tmp.name)
        self.origem = raiz / "TCC"
        self.destino = raiz / "squad-24-projeto"
        self.alvo = self.destino / so.SUBPASTA
        novo_repo(self.origem)
        for rel, conteudo in {**ARQUIVOS, **EXCLUIDOS}.items():
            gravar(self.origem, rel, conteudo)
        self.commit1 = commit(self.origem, "inicial")
        novo_repo(self.destino)
        gravar(self.destino, "README.md", "# Squad 24\n\n## Projeto\n\n" + MARCADORES + "\n## Entregas\n")
        gravar(self.destino, "docs/README.md", "# Docs\n")
        gravar(self.destino, "projeto/velho.txt", "sai\n")
        gravar(self.destino, "projeto/sub/pasta/antiga.txt", "sai\n")
        commit(self.destino, "esqueleto")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def conferir_copia(self) -> None:
        for rel, conteudo in ARQUIVOS.items():
            esperado = conteudo if isinstance(conteudo, bytes) else conteudo.encode("utf-8")
            self.assertEqual((self.alvo / rel).read_bytes(), esperado, rel)
        for rel in EXCLUIDOS:
            self.assertFalse((self.alvo / rel).exists(), rel)


class TesteEnsaio(Base):
    def teste_ensaio_lista_e_nao_grava(self) -> None:
        rel = so.sincronizar(self.origem, self.destino, aplicar=False)
        self.assertEqual(sorted(rel.novos), sorted(ARQUIVOS))
        self.assertEqual(rel.alterados, [])
        self.assertEqual(sorted(rel.removidos), ["sub/pasta/antiga.txt", "velho.txt"])
        self.assertEqual(sorted(rel.excluidos), sorted(EXCLUIDOS))
        self.assertEqual(rel.commit, self.commit1)
        self.assertFalse(rel.aplicado)
        self.assertFalse(rel.em_sincronia)
        self.assertFalse((self.alvo / "README.md").exists())
        self.assertTrue((self.alvo / "velho.txt").exists())
        self.assertIn("(ainda nao executada)", (self.destino / "README.md").read_text(encoding="utf-8"))

    def teste_hash_blob_igual_ao_git(self) -> None:
        dados = "conteúdo com acento\n".encode("utf-8")
        arquivo = gravar(self.origem, "hash.bin", dados)
        esperado = git(self.origem, "hash-object", "--no-filters", str(arquivo)).strip()
        self.assertEqual(so.hash_blob(dados), esperado)


class TesteAplicar(Base):
    def teste_copia_remove_e_atualiza_readme(self) -> None:
        rel = so.sincronizar(self.origem, self.destino, aplicar=True)
        self.assertTrue(rel.aplicado)
        self.conferir_copia()
        self.assertFalse((self.alvo / "velho.txt").exists())
        self.assertFalse((self.alvo / "sub").exists())
        readme = (self.destino / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"commit `{self.commit1}`", readme)
        self.assertIn(f"{len(ARQUIVOS)} arquivos", readme)
        self.assertNotIn("(ainda nao executada)", readme)
        self.assertTrue(readme.startswith("# Squad 24\n\n## Projeto\n\n" + so.INICIO + "\n"))
        self.assertTrue(readme.endswith(so.FIM + "\n\n## Entregas\n"))
        self.assertEqual((self.destino / "docs" / "README.md").read_text(encoding="utf-8"), "# Docs\n")
        self.assertTrue((self.destino / ".git").is_dir())
        self.assertEqual(rel.ignorados_no_destino, ["Programacao/AgenteCore/bateria.log"])

    def teste_segunda_vez_nada_muda(self) -> None:
        so.sincronizar(self.origem, self.destino, aplicar=True)
        rel = so.sincronizar(self.origem, self.destino, aplicar=True)
        self.assertEqual((rel.novos, rel.alterados, rel.removidos), ([], [], []))
        self.assertEqual(rel.iguais, len(ARQUIVOS))
        self.assertTrue(rel.em_sincronia)

    def teste_propaga_alteracao_novo_e_remocao(self) -> None:
        so.sincronizar(self.origem, self.destino, aplicar=True)
        gravar(self.origem, "ferramentas/a.py", "print('b')\n")
        gravar(self.origem, "novo.md", "# Novo\n")
        (self.origem / "Documentacao" / "Projeto de Pesquisa - ABNT 15287_2025 - V3.md").unlink()
        commit2 = commit(self.origem, "segundo")
        rel = so.sincronizar(self.origem, self.destino, aplicar=False)
        self.assertEqual(rel.alterados, ["ferramentas/a.py"])
        self.assertEqual(rel.novos, ["novo.md"])
        self.assertEqual(rel.removidos, ["Documentacao/Projeto de Pesquisa - ABNT 15287_2025 - V3.md"])
        rel = so.sincronizar(self.origem, self.destino, aplicar=True)
        self.assertEqual(rel.commit, commit2)
        self.assertEqual((self.alvo / "ferramentas" / "a.py").read_text(encoding="utf-8"), "print('b')\n")
        self.assertEqual((self.alvo / "novo.md").read_text(encoding="utf-8"), "# Novo\n")
        self.assertFalse((self.alvo / "Documentacao").exists())
        self.assertIn(f"commit `{commit2}`", (self.destino / "README.md").read_text(encoding="utf-8"))
        self.assertTrue(so.sincronizar(self.origem, self.destino, aplicar=False).em_sincronia)

    def teste_copia_o_commit_e_nao_a_pasta_de_trabalho(self) -> None:
        so.sincronizar(self.origem, self.destino, aplicar=True)
        gravar(self.origem, "ferramentas/a.py", "print('sem commit')\n")
        gravar(self.origem, "solto.txt", "fora do git\n")
        rel = so.sincronizar(self.origem, self.destino, aplicar=True)
        self.assertTrue(rel.sujo)
        self.assertTrue(rel.em_sincronia)
        self.assertEqual((self.alvo / "ferramentas" / "a.py").read_text(encoding="utf-8"), "print('a')\n")
        self.assertFalse((self.alvo / "solto.txt").exists())

    def teste_readme_sem_marcadores_avisa_e_nao_mexe(self) -> None:
        gravar(self.destino, "README.md", "# Sem bloco\n")
        rel = so.sincronizar(self.origem, self.destino, aplicar=True)
        self.assertTrue(any("SINCRONIZACAO" in aviso for aviso in rel.avisos), rel.avisos)
        self.assertEqual((self.destino / "README.md").read_text(encoding="utf-8"), "# Sem bloco\n")
        self.conferir_copia()

    def teste_readme_com_crlf_mantem_crlf(self) -> None:
        texto = ("# Squad 24\n\n" + MARCADORES + "\nfim\n").replace("\n", "\r\n")
        gravar(self.destino, "README.md", texto.encode("utf-8"))
        so.sincronizar(self.origem, self.destino, aplicar=True)
        dados = (self.destino / "README.md").read_bytes().decode("utf-8")
        self.assertIn(f"commit `{self.commit1}`", dados)
        self.assertNotRegex(dados, r"(?<!\r)\n", "quebra de linha sem CR apareceu num README em CRLF")
        self.assertTrue(dados.endswith("\r\nfim\r\n"))


class TesteCli(Base):
    def rodar(self, *args: str, destino: Path | None = None) -> subprocess.CompletedProcess[str]:
        ambiente = dict(os.environ, PYTHONIOENCODING="utf-8")
        return subprocess.run([sys.executable, so.__file__, "--origem", str(self.origem),
                               "--destino", str(destino or self.destino), *args],
                              capture_output=True, text=True, encoding="utf-8", env=ambiente)

    def teste_check_e_aplicar(self) -> None:
        r = self.rodar("--check")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(f"Novos: {len(ARQUIVOS)}", r.stdout)
        r = self.rodar("--aplicar")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.conferir_copia()
        r = self.rodar("--check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Em sincronia", r.stdout)

    def teste_destino_sem_git_falha(self) -> None:
        r = self.rodar("--check", destino=self.destino / "nada")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=1)
