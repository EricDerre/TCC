#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes de painel_textos.py (28/09/2026) — fichas e roadmap sintéticos
# (formato exato que o painel espera) e os dois arquivos reais do Memorial (toda ficha com Estado, O que é,
# Recomendação e Decisão; números únicos por bloco; toda fase e toda corrida com estado reconhecido).
# ! Motivo: as pendências futuras serão escritas nesse formato por quem estiver na sessão; se um campo
# sair com o nome errado ou uma corrida sem a palavra de estado, o painel mostraria um cartão vazio ou
# sem cor — o teste acusa antes de o painel ser gerado. Uso: python ferramentas/testar_painel_textos.py
"""Testes de painel_textos.py — python ferramentas/testar_painel_textos.py"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import painel_textos as pt  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
MEMORIAL = RAIZ / "Documentacao" / "memorial"

EXEMPLO_PENDENCIAS = """<!-- ! Alteração de IA - Revisar: exemplo. ! Motivo: teste. -->
# Pendências

Intro do arquivo.

## Abertas em 01/01/2026

Contexto do bloco.

### 1. Primeira pergunta
- **Estado:** aberta
- **Quem decide:** Eric
- **Aberta em:** 01/01/2026
- **O que é:** Texto com `codigo` e [link](arquivo.md) e [site](https://exemplo.org/x).
- **Por que importa:** Importa.
- **Opções:**
  - (a) Uma.
  - (b) Outra.
- **Recomendação:** (a).
- **Decisão:** em aberto.

### 2. Segunda, fechada
- **Estado:** fechada em 02/01/2026
- **Quem decide:** Claude
- **O que é:** Feita.
- **Decisão:** (b) — feita.

### Subseção sem ficha
- item solto

## Histórico
- coisa antiga
"""

EXEMPLO_ROADMAP = """<!-- tag -->
# Roadmap — 05/01/2026

Parte do Memorial.

## 1. Onde estamos, por fase

| Fase | O que é | Estado |
|---|---|---|
| 1 — Ambiente | Instalador | Concluída — tudo |
| 2 — Testes | Bateria | Em andamento — rodando |
| 3 — Agente | Tela | Não iniciada |

Posição: fim do **Mês 2**.

## 2. O que precisamos rodar

| # | Corrida | Comando (em `pasta`) | Inferências / tempo | Pré-requisito | O que fecha | Estado |
|---|---|---|---|---|---|---|
| 1 | **Cruzada** — x | `powershell -File r.ps1 -Modo cruzada -Saida saida_a -Modelos a,b` | 144 / ~2 h | nada | Limitação 7 | pendente — noite |
| 2 | **Inéditos** | `python x.py --saida saida_b` | 216 | nada | Limitação 2 | rodando desde ontem |
| 3 | **Sonda** | `python s.py` | 4 | nada | Requisito | feita em 04/01 |

Fora da máquina: nada.

## 3. Texto livre

Parágrafo com **negrito**.
1. um
2. dois
"""


def _grava(pasta: str, nome: str, texto: str) -> Path:
    p = Path(pasta) / nome
    p.write_text(texto, encoding="utf-8")
    return p


class TestePendenciasSinteticas(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.blocos = pt.ler_pendencias(_grava(self.tmp.name, "p.md", EXEMPLO_PENDENCIAS))

    def tearDown(self):
        self.tmp.cleanup()

    def teste_blocos_e_fichas(self):
        self.assertEqual([b.titulo for b in self.blocos], ["Abertas em 01/01/2026", "Histórico"])
        b = self.blocos[0]
        self.assertEqual(len(b.fichas), 2)
        self.assertIn("Contexto do bloco", b.intro)
        self.assertIn("### Subseção sem ficha", b.resto)
        self.assertEqual(self.blocos[1].fichas, [])
        self.assertIn("coisa antiga", self.blocos[1].intro)

    def teste_campos_da_ficha_aberta(self):
        f = self.blocos[0].fichas[0]
        self.assertEqual((f.numero, f.titulo), (1, "Primeira pergunta"))
        self.assertTrue(f.aberta)
        self.assertTrue(f.depende_do_eric)
        self.assertTrue(f.decisao_em_aberto)
        self.assertIsNone(f.fechada_em)
        self.assertEqual(f.listas["Opções"], ["(a) Uma.", "(b) Outra."])
        self.assertEqual(f.campos["Recomendação"], "(a).")
        self.assertEqual(f.id_html, "p0-1")

    def teste_ficha_fechada(self):
        f = self.blocos[0].fichas[1]
        self.assertFalse(f.aberta)
        self.assertEqual(f.fechada_em, "02/01/2026")
        self.assertFalse(f.depende_do_eric)
        self.assertFalse(f.decisao_em_aberto)

    def teste_html_da_ficha(self):
        h = pt.html_ficha(self.blocos[0].fichas[0])
        self.assertIn('id="p0-1"', h)
        self.assertIn('data-estado="aberta"', h)
        self.assertIn('data-quem="eric"', h)
        self.assertIn("<code>codigo</code>", h)
        self.assertIn('<span class="ref">link</span>', h)
        self.assertIn('href="https://exemplo.org/x"', h)
        self.assertIn('<ul class="opcoes"><li>(a) Uma.</li><li>(b) Outra.</li></ul>', h)
        self.assertIn('class="fc decisao pendente"', h)
        h2 = pt.html_ficha(self.blocos[0].fichas[1])
        self.assertIn("Fechada em 02/01/2026", h2)
        self.assertIn('class="fc decisao tomada"', h2)


class TesteRoadmapSintetico(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.road = pt.ler_roadmap(_grava(self.tmp.name, "r.md", EXEMPLO_ROADMAP))

    def tearDown(self):
        self.tmp.cleanup()

    def teste_fases(self):
        self.assertEqual(self.road["data"], "05/01/2026")
        self.assertEqual([f.classe for f in self.road["fases"]], ["concluida", "andamento", "nao_iniciada"])
        self.assertEqual(self.road["fases"][0].nome, "1 — Ambiente")
        self.assertIn("fim do **Mês 2**", self.road["posicao"])

    def teste_corridas(self):
        c = self.road["corridas"]
        self.assertEqual([x.classe for x in c], ["pendente", "rodando", "feita"])
        self.assertEqual(c[0].comando, "powershell -File r.ps1 -Modo cruzada -Saida saida_a -Modelos a,b")
        self.assertEqual(c[0].saida, "saida_a")
        self.assertEqual(c[1].saida, "saida_b")
        self.assertIsNone(c[2].saida)
        self.assertEqual(c[0].prerequisito, "nada")
        self.assertEqual(c[0].fecha, "Limitação 7")
        self.assertEqual(c[0].tempo, "144 / ~2 h")
        self.assertIn("Fora da máquina", self.road["fora_da_maquina"])

    def teste_secoes_restantes(self):
        self.assertEqual([t for t, _ in self.road["secoes"]], ["3. Texto livre"])
        h = pt.md_doc_para_html(self.road["secoes"][0][1])
        self.assertIn("<strong>negrito</strong>", h)
        self.assertIn("<ol><li>um</li><li>dois</li></ol>", h)


class TesteMarkdown(unittest.TestCase):
    def teste_tabela_com_barra_em_codigo(self):
        self.assertEqual(pt.celulas("| a | `x | y` | c |"), ["a", "`x | y`", "c"])

    def teste_documento(self):
        h = pt.md_doc_para_html("# Título\n\n## Seção\n\ntexto\ncontinua\n\n- um\n  - sub\n- dois\n\n| a | b |\n|---|---|\n| 1 | 2 |\n")
        self.assertNotIn("Título", h)
        self.assertIn("<h2>Seção</h2>", h)
        self.assertIn("<p>texto continua</p>", h)
        self.assertIn("<li>um<ul><li>sub</li></ul></li><li>dois</li>", h)
        self.assertIn("<th>a</th>", h)
        self.assertIn("<td>2</td>", h)

    def teste_inline(self):
        self.assertEqual(pt.inline("a **b** `c<d>` *e*"), "a <strong>b</strong> <code>c&lt;d&gt;</code> <em>e</em>")
        self.assertEqual(pt.inline("[`x.md`](../x.md)"), '<span class="ref"><code>x.md</code></span>')


class TesteArquivosReais(unittest.TestCase):
    def teste_pendencias_reais(self):
        blocos = pt.ler_pendencias(MEMORIAL / "pendencias.md")
        fichas = [f for b in blocos for f in b.fichas]
        self.assertGreaterEqual(len(fichas), 14)
        self.assertTrue(any(f.aberta for f in fichas))
        for f in fichas:
            for campo in ("Estado", "Quem decide", "O que é", "Recomendação", "Decisão"):
                self.assertIn(campo, f.campos, f"ficha {f.numero} ({f.titulo}) sem o campo {campo}")
            self.assertIn(f.estado.lower().split(" ")[0], ("aberta", "fechada"), f"ficha {f.numero}: estado {f.estado!r}")
            if not f.aberta:
                self.assertIsNotNone(f.fechada_em, f"ficha {f.numero} fechada sem data")
        for b in blocos:
            numeros = [f.numero for f in b.fichas]
            self.assertEqual(len(numeros), len(set(numeros)), f"bloco {b.titulo!r} com número repetido")
        self.assertTrue(any(b.titulo.startswith("Histórico") for b in blocos))

    def teste_roadmap_real(self):
        road = pt.ler_roadmap(MEMORIAL / "roadmap.md")
        self.assertRegex(road["data"], r"\d{2}/\d{2}/\d{4}")
        self.assertGreaterEqual(len(road["fases"]), 8)
        for f in road["fases"]:
            self.assertNotEqual(f.classe, "outro", f"fase {f.nome!r}: estado sem palavra fixa: {f.estado[:40]!r}")
        self.assertGreaterEqual(len(road["corridas"]), 6)
        for c in road["corridas"]:
            self.assertNotEqual(c.classe, "outro", f"corrida {c.numero}: estado sem palavra fixa: {c.estado[:40]!r}")
            if "-Modo" in c.comando:
                self.assertIsNotNone(c.saida, f"corrida {c.numero} sem -Saida no comando")
        self.assertTrue(any(c.classe == "rodando" or c.classe == "pendente" for c in road["corridas"]))


if __name__ == "__main__":
    unittest.main(verbosity=1)
