#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/11/2026, ficha 114, decisão 176): as marcas da hora de cada etapa do agente. Quando a corrida pede
# (`executar_fase4.py --etapas-ao-vivo`, que só o botão do hub passa), `marcar(etapa, caso)` acrescenta uma linha ao arquivo
# `etapas_ao_vivo.jsonl` da pasta da corrida, com o caso, a etapa que está começando e o relógio; `ler` devolve as linhas gravadas e
# `tempos_por_caso` faz a conta do tempo de cada etapa. Desligado (o padrão), `marcar` volta sem fazer nada.
# ! Motivo: o diagrama da linha de produção do hub só tinha tempo para o roteiro, a inferência e a cura, que é o que a trilha grava, e ao vivo
# só acendia a etapa do modelo; o Eric pediu o tempo de cada etapa em tempo real e respondeu a ficha 114 pela opção (a): gravar só nas corridas
# lançadas pelo botão do hub, que são uso do produto e não medida. Por isso o padrão é desligado: nas corridas de medida (18d, 21d, 28b e as
# próximas) nenhuma linha é gravada e nada é cronometrado, e o caminho do agente continua o mesmo. O tempo de uma etapa é a diferença entre a
# marca dela e a marca seguinte do mesmo caso, pelo relógio que só anda para a frente (`time.monotonic`), e só entre marcas do mesmo processo:
# numa corrida retomada o relógio recomeça, e subtrair marcas de dois processos daria um tempo que não existiu. Uma falha ao gravar a marca
# nunca derruba a corrida: a marca serve ao diagrama, não ao diagnóstico.
"""As marcas da hora de cada etapa do agente (ficha 114): desligadas por padrão, gravadas em `etapas_ao_vivo.jsonl` quando a corrida pede."""
from __future__ import annotations

import datetime as dt
import itertools
import json
import os
import time
from pathlib import Path

NOME_DO_ARQUIVO = "etapas_ao_vivo.jsonl"
# as seis etapas da figura "Como o agente trabalha", mais a saída (o relatório ou a cura) e o fim do caso
ETAPAS = ("roteiro", "deteccao", "poda", "busca", "modelo", "selo", "saida", "fim")
_arquivo: Path | None = None


def ligar(pasta: Path) -> Path:
    """Liga as marcas: daqui em diante `marcar` acrescenta linhas ao arquivo da pasta da corrida (que não é apagado: a corrida retomada continua nele)."""
    global _arquivo
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    _arquivo = pasta / NOME_DO_ARQUIVO
    return _arquivo


def desligar() -> None:
    global _arquivo
    _arquivo = None


def ligado() -> bool:
    return _arquivo is not None


def marcar(etapa: str, caso: str | None) -> None:
    """Grava que a etapa começou agora neste caso; sem as marcas ligadas, não faz nada."""
    if _arquivo is None:
        return
    if etapa not in ETAPAS:
        raise ValueError(f"etapa: {etapa!r} não é uma de {ETAPAS}")
    linha = {"caso": caso, "etapa": etapa, "t": round(time.monotonic(), 4), "ts": dt.datetime.now().isoformat(timespec="milliseconds"), "pid": os.getpid()}
    try:
        with _arquivo.open("a", encoding="utf-8") as f:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")
    except OSError:
        pass


def ler(pasta: Path) -> list[dict]:
    """As marcas gravadas na pasta de uma corrida, na ordem; a linha pela metade (a corrida está gravando) e a que não é uma marca são puladas."""
    try:
        linhas = (Path(pasta) / NOME_DO_ARQUIVO).read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    marcas = []
    for linha in linhas:
        try:
            m = json.loads(linha) if linha.strip() else None
        except ValueError:
            continue
        if isinstance(m, dict) and m.get("etapa") in ETAPAS and isinstance(m.get("t"), (int, float)) and not isinstance(m.get("t"), bool):
            marcas.append(m)
    return marcas


def tempos_por_caso(marcas: list[dict]) -> dict[str, dict[str, float]]:
    """O tempo de cada etapa de cada caso, em segundos: da marca da etapa até a marca seguinte do mesmo caso e do mesmo processo.
    A etapa que ainda não terminou (a última marca do caso) fica sem tempo, e a marca `fim` só fecha a anterior."""
    tempos: dict[str, dict[str, float]] = {}
    for atual, seguinte in itertools.pairwise(marcas):
        if atual["etapa"] == "fim" or atual.get("caso") != seguinte.get("caso") or atual.get("pid") != seguinte.get("pid") or seguinte["t"] < atual["t"]:
            continue
        do_caso = tempos.setdefault(str(atual.get("caso")), {})
        do_caso[atual["etapa"]] = do_caso.get(atual["etapa"], 0.0) + (seguinte["t"] - atual["t"])
    return {caso: {etapa: round(s, 3) for etapa, s in do_caso.items()} for caso, do_caso in tempos.items()}
