#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (pacote I2 do instalador único): lê a pasta de evidência de uma célula de teste
# (`Documentacao/memorial/5-metodo-e-ferramental/dados/instalador/celulas/<id>/<data-hora>/`) e imprime um resumo curto: o
# código de saída de cada passo, o estado de cada nível da prova, o fim de cada log e a saída de cada sonda de suspeita.
# ! Motivo: uma rodada grava o log inteiro do `apt-get`, do `pip` e do download do Chromium (milhares de linhas); a regra do
# projeto é a máquina resumir e a sessão ler só o resumo. Sem o leitor, marcar as suspeitas HL1 a HL11 pediria abrir cada
# arquivo à mão, e o que fosse copiado para o livro-razão não teria como ser conferido de novo.
"""Uso: python ferramentas/instalador_matriz/ler_celula.py <id da célula | pasta da rodada> [--log N] [--sonda N]
                                                         [--inteira HLn ...] [--json]
Com o id (por exemplo L-U2404), lê a rodada mais recente da célula. `--log` e `--sonda` dizem quantas linhas de cada log e de
cada sonda aparecem (padrão 25 e 30); `--inteira HL6` mostra as sondas dessa suspeita sem corte."""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from instalador import sistema  # noqa: E402

CELULAS = RAIZ / "Documentacao" / "memorial" / "5-metodo-e-ferramental" / "dados" / "instalador" / "celulas"
# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) `LOGS` ganha `restaurar_banco.log` como primeiro item; `resumir` devolve a chave `instalacao` do registro; `em_texto` imprime os tempos dos passos.
# ! Motivo: a célula ALVO (`celula_alvo.ps1`) grava o log da restauração do banco antes da prova, e o `conferir.py` passou a
# copiar para o `registro.json` o tempo de cada passo da instalação (seção 3.3 do plano); sem isto o leitor não mostraria
# nenhum dos dois e a sessão teria de abrir os arquivos à mão.
LOGS = ("restaurar_banco.log", "instalacao_direto.log", "instalacao.log", "conferir.log", "sondas.log")
AMBIENTE = ("systemd", "python3", "sudo")


def pasta_mais_recente(celulas: Path, ident: str) -> Path:
    """A rodada mais nova de uma célula: a subpasta de nome maior (o nome é a data e a hora)."""
    rodadas = sorted(p for p in (celulas / ident).glob("*") if p.is_dir())
    if not rodadas:
        raise FileNotFoundError(f"nenhuma rodada da célula {ident} em {celulas}")
    return rodadas[-1]


def _linhas(caminho: Path) -> list[str]:
    """As linhas do arquivo, sem as vazias do fim; só o último estado de uma linha de progresso (as que usam `\\r`)."""
    if not caminho.exists():
        return []
    texto = caminho.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    linhas = [linha.split("\r")[-1].rstrip() for linha in texto.split("\n")]
    while linhas and not linhas[-1]:
        linhas.pop()
    return linhas


def _cortar(linhas: list[str], limite: int) -> list[str]:
    """Começo e fim de um bloco comprido, com uma linha no meio dizendo quantas saíram."""
    if limite <= 0 or len(linhas) <= limite:
        return linhas
    cabeca = max(2, limite // 3)
    cauda = limite - cabeca
    return linhas[:cabeca] + [f"... {len(linhas) - limite} linhas cortadas ..."] + linhas[-cauda:]


def _sondas(caminho: Path, limite: int) -> dict:
    """Uma suspeita: o código de saída de cada sonda e as linhas, com cada sonda (bloco que começa em `###`) cortada à parte."""
    blocos: list[list[str]] = []
    for linha in _linhas(caminho):
        if linha.startswith("### ") or not blocos:
            blocos.append([])
        blocos[-1].append(linha)
    codigos = [int(c) for c in re.findall(r"^\[codigo de saida: (-?\d+)\]$", "\n".join(sum(blocos, [])), re.MULTILINE)]
    linhas: list[str] = []
    for bloco in blocos:
        while bloco and not bloco[-1]:
            bloco.pop()
        linhas.extend(_cortar(bloco, limite))
    return {"codigos": codigos, "linhas": linhas}


def resumir(pasta: Path, linhas_do_log: int = 25, linhas_da_sonda: int = 30, inteiras: tuple[str, ...] = ()) -> dict:
    """O resumo de uma rodada, lido dos arquivos que o `celula_wsl.ps1` e o `instalador/conferir.py` gravaram."""
    celula = json.loads((pasta / "celula.json").read_text(encoding="utf-8-sig")) if (pasta / "celula.json").exists() else {}
    celula.pop("tag_ia", None)
    registro = json.loads((pasta / "registro.json").read_text(encoding="utf-8")) if (pasta / "registro.json").exists() else {}
    duracao = None
    if celula.get("inicio") and celula.get("fim"):
        duracao = int((datetime.fromisoformat(celula["fim"]) - datetime.fromisoformat(celula["inicio"])).total_seconds())
    ambiente = {}
    if (pasta / "os-release.txt").exists():
        dados = sistema.ler_os_release((pasta / "os-release.txt").read_text(encoding="utf-8", errors="replace"))
        ambiente["os-release"] = dados.get("PRETTY_NAME") or dados.get("NAME", "")
    for nome in AMBIENTE:
        linhas = _linhas(pasta / f"{nome}.txt")
        if linhas:
            ambiente[nome] = " / ".join(linhas[:3])
    logs = {}
    for nome in LOGS:
        linhas = _linhas(pasta / nome)
        if linhas:
            logs[nome] = linhas[-linhas_do_log:] if linhas_do_log > 0 else linhas
    arquivos = sorted((pasta / "suspeitas").glob("HL*.txt"), key=lambda p: int(re.sub(r"\D", "", p.stem) or 0))
    suspeitas = {p.stem: _sondas(p, 0 if p.stem in inteiras else linhas_da_sonda) for p in arquivos}
    return {"pasta": str(pasta), "celula": celula, "duracao_s": duracao, "saidas": celula.get("saidas", {}),
            "niveis": registro.get("niveis", {}), "alcancado": registro.get("alcancado", ""),
            "versoes": registro.get("versoes", {}), "instalacao": registro.get("instalacao", {}), "impedida_por_versao": registro.get("impedida_por_versao", []),
            "maquina": registro.get("maquina", {}), "ambiente": ambiente, "logs": logs, "suspeitas": suspeitas}


def em_texto(resumo: dict) -> str:
    """O resumo em texto corrido, para ler no terminal."""
    celula = resumo["celula"]
    saida = [f"Célula {celula.get('id', '?')} ({celula.get('modo', '?')}, até {celula.get('ate', '?')}), imagem "
             f"{celula.get('imagem', '?')}, começo {celula.get('inicio', '?')}, {resumo['duracao_s']} s",
             f"Pasta: {resumo['pasta']}"]
    extras = [f"{chave}={celula[chave]}" for chave in ("sondas", "sem_systemd", "modelo_pequeno") if chave in celula]
    if extras:
        saida.append("Opções: " + "; ".join(extras))
    saida.append("Ambiente antes do instalador: " + "; ".join(f"{k}={v}" for k, v in resumo["ambiente"].items()))
    if resumo["maquina"]:
        saida.append("Máquina na prova: " + "; ".join(f"{k}={v}" for k, v in resumo["maquina"].items()))
    saida.append("Códigos de saída: " + ("; ".join(f"{k}={v}" for k, v in resumo["saidas"].items()) or "nenhum gravado"))
    passos = resumo.get("instalacao", {}).get("passos") or []
    if passos:
        saida.append(f"Instalação ({resumo['instalacao'].get('resultado', '?')}): "
                     + "; ".join(f"{p['passo']} {p['segundos']} s" for p in passos))
    if resumo["niveis"]:
        saida.append(f"Prova: alcançado {resumo['alcancado']}")
        for nivel, dados in resumo["niveis"].items():
            tempo = f" ({dados['segundos']} s)" if dados.get("segundos") is not None else ""
            saida.append(f"  {nivel}: {dados['estado']}{tempo} {dados['detalhe'].strip()[:900]}")
    else:
        saida.append("Prova: sem registro.json")
    if resumo["versoes"]:
        saida.append("Versões: " + "; ".join(f"{nome} {d['encontrada'] or '?'} ({d['estado']}; testada {d['testada']})"
                                              for nome, d in resumo["versoes"].items()))
    if resumo["impedida_por_versao"]:
        saida.append("Versão impede: " + ", ".join(resumo["impedida_por_versao"]))
    for nome, linhas in resumo["logs"].items():
        saida.append(f"--- {nome} (últimas {len(linhas)} linhas)")
        saida.extend(linhas)
    for nome, dados in resumo["suspeitas"].items():
        saida.append(f"=== {nome} (códigos de saída das sondas: {', '.join(str(c) for c in dados['codigos']) or 'nenhum'})")
        saida.extend(dados["linhas"])
    return "\n".join(saida) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("alvo", help="id da célula (lê a rodada mais recente) ou a pasta de uma rodada")
    ap.add_argument("--log", type=int, default=25, help="linhas do fim de cada log (0 = todas)")
    ap.add_argument("--sonda", type=int, default=30, help="linhas de cada sonda (0 = todas)")
    ap.add_argument("--inteira", action="append", default=[], help="suspeita cujas sondas saem sem corte (pode repetir)")
    ap.add_argument("--json", action="store_true", help="imprime o resumo em JSON")
    args = ap.parse_args(argv)
    pasta = Path(args.alvo) if Path(args.alvo).is_dir() else pasta_mais_recente(CELULAS, args.alvo)
    resumo = resumir(pasta, linhas_do_log=args.log, linhas_da_sonda=args.sonda, inteiras=tuple(args.inteira))
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(resumo, ensure_ascii=False, indent=1) if args.json else em_texto(resumo), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
