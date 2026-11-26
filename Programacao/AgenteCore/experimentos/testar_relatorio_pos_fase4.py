#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria testar_relatorio_pos_fase4.py, o runner (sem pytest, como os outros testar_*.py desta pasta) dos testes do relatório da Pós-Fase 4 e do script que cola as tabelas nele (colar_pos_fase4.py). Os testes foram escritos ANTES do script: a primeira rodada falha por ModuleNotFoundError em `colar_pos_fase4`.
# ! Motivo: o relatório da Pós-Fase 4 (Documentacao/memorial/3-resultados-e-analises/pos-fase-4-relatorio.md) não pode ter número de resultado digitado à mão: as tabelas vêm das leituras em resultados_alvo/fase4/ e o `--check` tem de acusar quando um número do relatório for trocado ou a leitura mudar. Aqui ficam fixados: a colagem num relatório de mentira, o `--check` que acusa um número trocado à mão, a ligação de cada marcador do relatório de verdade a uma leitura de origem, e as regras de escrita do texto corrido (sem travessão, sem seta, sem o marcador de pendência de conferência).
"""Testes do relatório da Pós-Fase 4 e do colar_pos_fase4.py, sem pytest. Uso (na raiz do repositório):
  python -I Programacao/AgenteCore/experimentos/testar_relatorio_pos_fase4.py
"""
from __future__ import annotations

import inspect
import io
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
from contextlib import redirect_stdout
from pathlib import Path

EXP = Path(__file__).resolve().parent
sys.path.insert(0, str(EXP))  # com `python -I` a pasta do script não entra sozinha no caminho de módulos

RAIZ_REPO = EXP.parent.parent.parent
RELATORIO = RAIZ_REPO / "Documentacao" / "memorial" / "3-resultados-e-analises" / "pos-fase-4-relatorio.md"
SCRIPT = EXP / "colar_pos_fase4.py"
_TEMPORARIOS: list[Path] = []

BLOCO = (
    "<!-- tabela:tb_f4_texto_resumo -->\n"
    "| Grupo | Textos |\n|---|---|\n| corrida de mentira | 74 |\n"
    "<!-- /tabela:tb_f4_texto_resumo -->"
)
LEITURA_DE_MENTIRA = (
    "<!-- ! Alteração de IA - Revisar: leitura de mentira dos testes.\n"
    "     ! Motivo: só existe dentro da pasta temporária do teste. -->\n"
    "# Leitura de mentira, gerada em 2026-01-01\n\ntexto solto\n\n" + BLOCO + "\n"
)
RELATORIO_DE_MENTIRA = (
    "# Relatório de mentira\n\nUma frase.\n\n"
    "<!-- tabela:tb_f4_texto_resumo -->\n<!-- /tabela:tb_f4_texto_resumo -->\n\nOutra frase.\n"
)


def _pasta() -> Path:
    p = Path(tempfile.mkdtemp(prefix="relatorio_pos_fase4_"))
    _TEMPORARIOS.append(p)
    return p


def _montar_mentira() -> tuple[Path, Path]:
    raiz = _pasta()
    (raiz / "fase4").mkdir()
    (raiz / "fase4" / "texto.md").write_text(LEITURA_DE_MENTIRA, encoding="utf-8", newline="\n")
    rel = raiz / "relatorio.md"
    rel.write_text(RELATORIO_DE_MENTIRA, encoding="utf-8", newline="\n")
    return raiz, rel


def _rodar(args: list[str]) -> tuple[int, str]:
    import colar_pos_fase4 as c
    saida = io.StringIO()
    with redirect_stdout(saida):
        try:
            codigo = c.main(args)
        except SystemExit as e:
            codigo = e.code if isinstance(e.code, int) else 1
            if isinstance(e.code, str):
                saida.write(e.code)
    return int(codigo or 0), saida.getvalue()


def _sem_blocos_e_codigo(texto: str) -> str:
    """O texto corrido do relatório: sem as tabelas coladas e sem os blocos de código."""
    texto = re.sub(r"<!-- tabela:(tb_[a-z0-9_]+) -->.*?<!-- /tabela:\1 -->", "", texto, flags=re.S)
    texto = re.sub(r"```.*?```", "", texto, flags=re.S)
    return texto


def teste_script_cola_o_bloco_num_relatorio_de_mentira_e_o_check_passa() -> None:
    raiz, rel = _montar_mentira()
    codigo, saida = _rodar(["--raiz", str(raiz), "--relatorio", str(rel)])
    assert codigo == 0, saida
    texto = rel.read_text(encoding="utf-8")
    assert "| corrida de mentira | 74 |" in texto, texto
    assert "Uma frase." in texto and "Outra frase." in texto
    codigo, saida = _rodar(["--check", "--raiz", str(raiz), "--relatorio", str(rel)])
    assert codigo == 0, saida


def teste_check_nao_grava_nada() -> None:
    raiz, rel = _montar_mentira()
    antes = rel.read_text(encoding="utf-8")
    codigo, saida = _rodar(["--check", "--raiz", str(raiz), "--relatorio", str(rel)])
    assert codigo == 1, (codigo, saida)  # o marcador está vazio: difere da leitura
    assert "tb_f4_texto_resumo" in saida, saida
    assert rel.read_text(encoding="utf-8") == antes


def teste_check_acusa_numero_trocado_a_mao() -> None:
    raiz, rel = _montar_mentira()
    assert _rodar(["--raiz", str(raiz), "--relatorio", str(rel)])[0] == 0
    rel.write_text(rel.read_text(encoding="utf-8").replace("| 74 |", "| 75 |"), encoding="utf-8", newline="\n")
    codigo, saida = _rodar(["--check", "--raiz", str(raiz), "--relatorio", str(rel)])
    assert codigo == 1, saida
    assert "tb_f4_texto_resumo" in saida, saida


def teste_marcador_sem_leitura_de_origem_interrompe() -> None:
    raiz, rel = _montar_mentira()
    rel.write_text(rel.read_text(encoding="utf-8") + "\n<!-- tabela:tb_f4_inventado_x -->\n<!-- /tabela:tb_f4_inventado_x -->\n",
                   encoding="utf-8", newline="\n")
    codigo, saida = _rodar(["--raiz", str(raiz), "--relatorio", str(rel)])
    assert codigo != 0 and "tb_f4_inventado_x" in saida, (codigo, saida)


def teste_leitura_que_sumiu_com_marcador_no_relatorio_interrompe() -> None:
    raiz, rel = _montar_mentira()
    (raiz / "fase4" / "texto.md").unlink()
    codigo, saida = _rodar(["--raiz", str(raiz), "--relatorio", str(rel)])
    assert codigo != 0 and "texto.md" in saida, (codigo, saida)


def teste_relatorio_de_verdade_existe_e_todo_marcador_tem_leitura_de_origem() -> None:
    import colar_pos_fase4 as c
    assert RELATORIO.exists(), RELATORIO
    texto = RELATORIO.read_text(encoding="utf-8")
    nomes = re.findall(r"<!-- tabela:(tb_[a-z0-9_]+) -->", texto)
    assert len(nomes) >= 15, len(nomes)
    sem_origem = [n for n in nomes if not any(n.startswith(prefixo) for _, prefixo in c.PARES)]
    assert not sem_origem, sem_origem
    fechamentos = re.findall(r"<!-- /tabela:(tb_[a-z0-9_]+) -->", texto)
    assert sorted(nomes) == sorted(fechamentos), "marcador aberto sem o de fechamento"
    assert len(set(nomes)) == len(nomes), "marcador repetido"


def teste_check_passa_no_relatorio_de_verdade() -> None:
    r = subprocess.run([sys.executable, "-I", str(SCRIPT), "--check"], capture_output=True, text=True,
                       encoding="utf-8", cwd=str(RAIZ_REPO), check=False)
    assert r.returncode == 0, (r.stdout, r.stderr)


def teste_relatorio_sem_travessao_seta_e_marcador_de_conferir() -> None:
    texto = _sem_blocos_e_codigo(RELATORIO.read_text(encoding="utf-8"))
    for simbolo in ("—", "→", "↔", "⇒"):
        achados = [l.strip()[:90] for l in texto.splitlines() if simbolo in l]
        assert not achados, (simbolo, achados[:3])
    assert "[conferir]" not in RELATORIO.read_text(encoding="utf-8")


# ! Alteração de IA - Revisar: (26/11/2026, Pós-Fase 4, pacote Q8) o teste deixa de exigir a marca de espera da ficha 99 e passa a exigir
# o parágrafo da corrida curta já lida: sem marca de espera no arquivo, com a pasta `fase4_fumaca_q7` citada e dizendo que a seleção
# parcial continua sem prova; e a seção do hub tem de contar a central aberta pelo `Cobaia.exe` com o limite do botão.
# ! Motivo: a ficha 99 foi fechada em 25/11/2026 com a corrida curta rodada e o hub virou a central (ficha 109, decisão 170); o teste
# antigo exigia a marca `A_PREENCHER` e falharia no relatório atualizado, e nada conferia que o relatório não dá como provado o que não
# foi visto rodando (uma seleção parcial e o botão do hub lançando uma corrida com o modelo).
def teste_relatorio_tem_a_tag_e_a_corrida_curta_da_ficha_99_lida() -> None:
    texto = RELATORIO.read_text(encoding="utf-8")
    assert "Alteração de IA - Revisar" in texto.split("\n\n", 1)[0] and "! Motivo:" in texto.split("\n\n", 1)[0]
    assert "A_PREENCHER" not in texto, "sobrou marca de espera no relatório"
    paragrafos = texto.split("\n\n")
    curta = [p for p in paragrafos if "**A corrida curta da ficha 99.**" in p]
    assert len(curta) == 1, len(curta)
    assert "fase4_fumaca_q7" in curta[0] and "seleção parcial" in curta[0] and "não tinha rodado" not in curta[0]
    assert "a corrida com as cobaias está pendente" not in texto and "a corrida com o modelo ainda não rodou" not in texto
    central = [p for p in paragrafos if "**O hub como central.**" in p]
    assert len(central) == 1, len(central)
    assert "Cobaia.exe" in central[0] and "decisão 170" in central[0] and "não foi visto lançando uma corrida com o modelo" in central[0]


def teste_relatorio_nao_cita_integrante_nem_atribui_a_revisao_ao_eric() -> None:
    texto = RELATORIO.read_text(encoding="utf-8")
    for nome in ("Pedro", "Gonçalves", "Goncalves", "pedrohtgoncalvesgit"):
        assert nome not in texto, nome
    assert "analista de QA" in texto
    # a revisão humana nunca é dita do Eric (a frase negada, "não foi feita pelo Eric", pode)
    assert not re.search(r"(?i)revis[aã]o[^.\n]{0,60}(?<!não foi )(?<!não )(feita|realizada) pelo Eric", texto)


def teste_toda_fonte_de_comentario_nomeia_um_arquivo_que_existe() -> None:
    texto = RELATORIO.read_text(encoding="utf-8")
    fontes = re.findall(r"<!-- fonte: ([^>]*?) -->", texto)
    assert len(fontes) >= 20, len(fontes)
    pastas = [EXP / "resultados_alvo", RAIZ_REPO / "Documentacao" / "memorial", RAIZ_REPO / "claude-memoria"]
    faltando = []
    for f in fontes:
        for parte in f.split(";"):
            m = re.match(r"\s*([\w.\-]+\.(?:md|json|jsonl))\b", parte)
            if not m:
                faltando.append(parte.strip()[:60])
                continue
            if not any(next(p.rglob(m.group(1)), None) for p in pastas):
                faltando.append(m.group(1))
    assert not faltando, sorted(set(faltando))


def main() -> None:
    modulo = sys.modules[__name__]
    testes = [(n, o) for n, o in vars(modulo).items()
              if n.startswith("teste_") and inspect.isfunction(o) and o.__module__ == modulo.__name__]
    try:
        for nome, funcao in testes:
            try:
                funcao()
            except Exception:  # noqa: BLE001 - o runner pega qualquer falha do teste para imprimir o rastro e parar com código 1
                print(nome)
                traceback.print_exc()
                sys.exit(1)
            print(f"{nome} ok")
        print(f"{len(testes)} testes ok")
    finally:
        for p in _TEMPORARIOS:
            shutil.rmtree(p, ignore_errors=True)


if __name__ == "__main__":
    main()
