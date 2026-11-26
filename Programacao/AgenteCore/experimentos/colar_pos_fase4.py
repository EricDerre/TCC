#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria colar_pos_fase4.py, que cola no relatório da Pós-Fase 4 (Documentacao/memorial/3-resultados-e-analises/pos-fase-4-relatorio.md) as tabelas das leituras de resultados_alvo/fase4/, e que com `--check` confere, sem gravar, se algum bloco do relatório difere da leitura de origem.
# ! Motivo: o relatório junta tabelas de 12 leituras de pacotes diferentes (filtros de texto, revisão humana, barra de progresso, seleção pelo Git, corridas 25 a 27, hub); cada leitura tem o seu script e o seu `--check`, mas nenhuma cola no relatório da fase inteira. Sem uma lista fixa de (leitura, prefixo dos blocos), o relatório teria número copiado à mão ou ficaria com tabela velha depois de uma leitura ser regerada. Os blocos colados são os que o texto do relatório discute; os outros ficam só na leitura de origem (a rastreabilidade do relatório diz onde).
"""Cola e confere as tabelas do relatório da Pós-Fase 4.

Uso (na raiz do repositório):
  python -I Programacao/AgenteCore/experimentos/colar_pos_fase4.py            # cola os blocos cujo marcador já está no relatório
  python -I Programacao/AgenteCore/experimentos/colar_pos_fase4.py --check    # não grava; sai com 1 se algum bloco difere da leitura
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # com `python -I` a pasta do script não entra sozinha no caminho

import analisar_fase3b as a3b  # noqa: E402
import pre_fase4  # noqa: E402

EXP = Path(__file__).resolve().parent
# ! Alteração de IA - Revisar: a pasta das leituras é fixa em resultados_alvo/ (o registro oficial, só lido aqui), e não `caminhos.RESULTADOS`.
# ! Motivo: `caminhos.RESULTADOS` aponta para `resultados/` quando a variável RESULTADOS_DIR não está definida, e as leituras da Pós-Fase 4 só existem em `resultados_alvo/`; sem isso o script dizia que `fase4/texto.md` não existia.
RESULTADOS_ALVO = EXP / "resultados_alvo"
RELATORIO = EXP.parent.parent.parent / "Documentacao" / "memorial" / "3-resultados-e-analises" / "pos-fase-4-relatorio.md"

# ! Alteração de IA - Revisar: lista fixa dos pares (arquivo da leitura relativo a resultados_alvo, prefixo dos blocos que ele gera).
# ! Motivo: três leituras da barra de progresso e duas da seleção pelo Git compartilham o começo do nome dos blocos (`tb_f4_progresso_`, `tb_f4_conferencia_`); por isso o prefixo é o mais longo que ainda separa uma leitura da outra, e um marcador que não casa com nenhum par é acusado pelo teste do relatório.
PARES: list[tuple[str, str]] = [
    ("fase4/texto.md", "tb_f4_texto_"),
    ("fase4/leitura_revisao_v3.md", "tb_f4_revisao_v3_"),
    ("fase4/taxas_progresso.md", "tb_f4_progresso_taxas"),
    ("fase4/erro_progresso.md", "tb_f4_progresso_erro"),
    ("fase4/fumaca_progresso.md", "tb_f4_progresso_fumaca"),
    ("fase4/impacto_git.md", "tb_f4_impacto_"),
    ("fase4/conferencia_git.md", "tb_f4_conferencia_pares"),
    ("fase4/sem_notas.md", "tb_f4_semnotas_"),
    ("fase4/segundo_passe.md", "tb_f4_segpasse_"),
    ("fase4/portoes_m1.md", "tb_f4_portoes_"),
    ("fase4/analista.md", "tb_f4_analista_"),
    ("fase4/hub.md", "tb_f4_hub_"),
]


def _marcadores(texto: str) -> list[str]:
    return a3b.BLOCO_ALVO_RE.findall(texto)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="não grava; sai com 1 se algum bloco do relatório difere da leitura")
    ap.add_argument("--raiz", type=Path, default=None, help="pasta das leituras (padrão: resultados_alvo; só os testes mudam)")
    ap.add_argument("--relatorio", type=Path, default=None, help="relatório a colar (padrão: o da Pós-Fase 4; só os testes mudam)")
    a = ap.parse_args(argv)
    raiz = a.raiz or RESULTADOS_ALVO
    doc = a.relatorio or RELATORIO
    texto = doc.read_text(encoding="utf-8")
    marcadores = _marcadores(texto)

    sem_par = [n for n in marcadores if not any(n.startswith(p) for _, p in PARES)]
    if sem_par:
        print(f"{doc.name}: marcador(es) sem leitura de origem na lista de pares: {sem_par}")
        return 1

    divergentes: list[str] = []
    colados = 0
    for arquivo, prefixo in PARES:
        meus = [n for n in marcadores if n.startswith(prefixo)]
        if not meus:
            continue
        origem = raiz / arquivo
        if not origem.exists():
            print(f"{doc.name}: a leitura {arquivo} não existe, e o relatório tem os blocos {meus}")
            return 1
        md = origem.read_text(encoding="utf-8")
        if a.check:
            divergentes += [f"{n} (leitura {arquivo})" for n in pre_fase4.blocos_divergentes(doc, md, prefixo)]
        else:
            n_colados, _mudou = pre_fase4.colar_blocos(doc, md, prefixo)
            colados += n_colados
    if a.check:
        if divergentes:
            print(f"--check: {len(divergentes)} bloco(s) de {doc.name} diferem da leitura de origem:")
            for d in divergentes:
                print(f"  {d}")
            return 1
        print(f"--check: os {len(marcadores)} blocos de {doc.name} batem com as leituras de origem")
        return 0
    print(f"{doc.name}: {colados} bloco(s) colado(s), de {len({p for _, p in PARES if any(n.startswith(p) for n in marcadores)})} leitura(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
