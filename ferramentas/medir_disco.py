#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (01/10/2026, Pré-Fase 4) que mede a vazão de leitura do disco da
# máquina-alvo do jeito que o repositório colibri mede a dele (ferramenta `iobench`: blocos de 19 MB, 64
# leituras, 8 threads, em posições sorteadas de um arquivo grande), com a leitura passando pelo cache do
# sistema e por fora dele, e grava o resultado com a descrição da máquina (CPU, RAM, modelo e espaço do
# disco) em resultados_alvo/pre_fase4/disco.json.
# ! Motivo: a viabilidade do colibri nesta máquina depende de quantos GB por segundo o NVMe entrega, porque
# o motor lê do disco, a cada token, os especialistas que o modelo aciona; a tabela de medidas dele traz essa
# vazão para cada máquina e, sem medir a nossa do mesmo jeito, a comparação seria com número de catálogo.
# Nenhum maquina.json do projeto tem campo de disco. O arquivo lido é um blob de modelo do Ollama que já
# está no disco (só leitura); a leitura por fora do cache usa FILE_FLAG_NO_BUFFERING do Windows por ctypes,
# para medir o disco e não a RAM. Só biblioteca padrão.
"""Uso (na raiz do repositório):
    python ferramentas/medir_disco.py [--arquivo CAMINHO] [--blocos 64] [--bloco-mb 19] [--threads 8]
                                      [--repeticoes 3] [--saida CAMINHO]
"""
from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import statistics
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "Programacao" / "AgenteCore" / "experimentos" / "resultados_alvo" / "pre_fase4" / "disco.json"
MB = 1024 * 1024
NO_WINDOWS = os.name == "nt"
TEM_LEITURA_DIRETA = NO_WINDOWS or hasattr(os, "O_DIRECT")


def deslocamentos(tamanho: int, bloco: int, n: int, semente: int) -> list[int]:
    """n posições de leitura, múltiplas do tamanho do bloco e que cabem no arquivo. Sem repetição enquanto o
    arquivo tiver blocos inteiros suficientes; com menos blocos do que o pedido, repete."""
    inteiros = tamanho // bloco
    if inteiros < 1:
        raise ValueError(f"arquivo de {tamanho} bytes é menor que um bloco de {bloco}")
    sorteio = random.Random(semente)
    if inteiros >= n:
        indices = sorteio.sample(range(inteiros), n)
    else:
        indices = [sorteio.randrange(inteiros) for _ in range(n)]
    return [i * bloco for i in indices]


def _ler_pelo_cache(arquivo: Path, offs: list[int], bloco: int, guardar: bool):
    total, blocos = 0, []
    alvo = bytearray(bloco)
    with open(arquivo, "rb", buffering=0) as f:
        for off in offs:
            f.seek(off)
            lido = f.readinto(alvo)
            total += lido
            if guardar:
                blocos.append(bytes(alvo[:lido]))
    return blocos if guardar else total


def _ler_direto_windows(arquivo: Path, offs: list[int], bloco: int, guardar: bool):
    """Leitura com FILE_FLAG_NO_BUFFERING: o Windows não usa o cache de arquivos, então o que se mede é o disco.
    Essa forma de abrir exige posição, tamanho e memória alinhados ao setor; o bloco é múltiplo de 1 MB e a
    memória vem de VirtualAlloc, que já entrega página alinhada."""
    import ctypes
    from ctypes import wintypes
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.CreateFileW.restype = wintypes.HANDLE
    k32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD,
                                wintypes.DWORD, wintypes.HANDLE]
    k32.VirtualAlloc.restype = wintypes.LPVOID
    k32.VirtualAlloc.argtypes = [wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD, wintypes.DWORD]
    k32.VirtualFree.argtypes = [wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD]
    k32.SetFilePointerEx.argtypes = [wintypes.HANDLE, ctypes.c_longlong, ctypes.POINTER(ctypes.c_longlong), wintypes.DWORD]
    k32.ReadFile.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID]
    k32.CloseHandle.argtypes = [wintypes.HANDLE]
    leitura, compartilhar, abrir_existente, sem_cache = 0x80000000, 0x1 | 0x2 | 0x4, 3, 0x20000000
    h = k32.CreateFileW(str(arquivo), leitura, compartilhar, None, abrir_existente, sem_cache, None)
    if h is None or h == wintypes.HANDLE(-1).value:
        raise OSError(ctypes.get_last_error(), f"não abriu {arquivo} para leitura direta")
    memoria = k32.VirtualAlloc(None, bloco, 0x1000 | 0x2000, 0x04)  # reservar e confirmar, leitura e escrita
    if not memoria:
        k32.CloseHandle(h)
        raise MemoryError(f"sem memória para um bloco de {bloco} bytes")
    total, blocos = 0, []
    lidos = wintypes.DWORD(0)
    try:
        for off in offs:
            if not k32.SetFilePointerEx(h, off, None, 0):
                raise OSError(ctypes.get_last_error(), f"não posicionou em {off}")
            if not k32.ReadFile(h, memoria, bloco, ctypes.byref(lidos), None):
                raise OSError(ctypes.get_last_error(), f"falhou a leitura direta em {off}")
            total += lidos.value
            if guardar:
                blocos.append(ctypes.string_at(memoria, lidos.value))
    finally:
        k32.VirtualFree(memoria, 0, 0x8000)
        k32.CloseHandle(h)
    return blocos if guardar else total


def _ler_direto_posix(arquivo: Path, offs: list[int], bloco: int, guardar: bool):
    import mmap
    fd = os.open(str(arquivo), os.O_RDONLY | os.O_DIRECT)
    memoria = mmap.mmap(-1, bloco)  # memória anônima já vem alinhada à página
    total, blocos = 0, []
    try:
        for off in offs:
            lido = os.preadv(fd, [memoria], off)
            total += lido
            if guardar:
                blocos.append(bytes(memoria[:lido]))
    finally:
        memoria.close()
        os.close(fd)
    return blocos if guardar else total


def ler_blocos(arquivo: Path, offs: list[int], bloco: int, direto: bool, guardar: bool = False):
    """Lê um bloco em cada posição. Devolve o total de bytes lidos ou, com guardar=True (só nos testes), a lista
    dos blocos lidos."""
    if not direto:
        return _ler_pelo_cache(arquivo, offs, bloco, guardar)
    if NO_WINDOWS:
        return _ler_direto_windows(arquivo, offs, bloco, guardar)
    if hasattr(os, "O_DIRECT"):
        return _ler_direto_posix(arquivo, offs, bloco, guardar)
    raise OSError("este sistema não tem leitura direta (sem cache)")


def medir(arquivo: Path, bloco: int, n: int, threads: int, direto: bool, semente: int) -> dict:
    """n leituras de `bloco` bytes em posições sorteadas, repartidas entre `threads` threads (cada uma com o seu
    descritor e a sua memória). As leituras soltam a trava do interpretador, então correm de fato em paralelo."""
    offs = deslocamentos(arquivo.stat().st_size, bloco, n, semente)
    partes = [offs[i::threads] for i in range(threads)]
    partes = [p for p in partes if p]
    totais = [0] * len(partes)
    erros: list[BaseException] = []

    def trabalho(i: int) -> None:
        try:
            totais[i] = ler_blocos(arquivo, partes[i], bloco, direto)
        except BaseException as e:  # noqa: BLE001
            erros.append(e)

    fios = [threading.Thread(target=trabalho, args=(i,)) for i in range(len(partes))]
    inicio = time.perf_counter()
    for t in fios:
        t.start()
    for t in fios:
        t.join()
    segundos = time.perf_counter() - inicio
    if erros:
        raise erros[0]
    lidos = sum(totais)
    return {"modo": "direto" if direto else "pelo_cache", "blocos": n, "bloco_bytes": bloco, "threads": len(partes),
            "bytes": lidos, "segundos": round(segundos, 4), "gb_por_s": round(lidos / 1e9 / segundos, 3),
            "gib_por_s": round(lidos / 2**30 / segundos, 3)}


def resumir(medidas: list[dict]) -> dict:
    v = [m["gb_por_s"] for m in medidas]
    if not v:
        return {"repeticoes": 0, "gb_por_s_mediana": None, "gb_por_s_min": None, "gb_por_s_max": None}
    return {"repeticoes": len(v), "gb_por_s_mediana": statistics.median(v), "gb_por_s_min": min(v), "gb_por_s_max": max(v)}


def maior_blob_do_ollama() -> Path | None:
    """O maior arquivo de pesos que o Ollama guarda (OLLAMA_MODELS ou ~/.ollama/models/blobs)."""
    base = Path(os.environ.get("OLLAMA_MODELS") or Path.home() / ".ollama" / "models") / "blobs"
    if not base.is_dir():
        return None
    arquivos = [p for p in base.iterdir() if p.is_file()]
    return max(arquivos, key=lambda p: p.stat().st_size) if arquivos else None


def _ram_total_gb() -> float | None:
    try:
        if NO_WINDOWS:
            import ctypes

            class Estado(ctypes.Structure):
                _fields_ = [("tamanho", ctypes.c_ulong), ("carga", ctypes.c_ulong), ("total", ctypes.c_ulonglong),
                            ("livre", ctypes.c_ulonglong), ("pag_total", ctypes.c_ulonglong), ("pag_livre", ctypes.c_ulonglong),
                            ("virt_total", ctypes.c_ulonglong), ("virt_livre", ctypes.c_ulonglong), ("ext", ctypes.c_ulonglong)]

            e = Estado()
            e.tamanho = ctypes.sizeof(Estado)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(e))
            return round(e.total / 2**30, 2)
        return round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2**30, 2)
    except Exception:  # noqa: BLE001
        return None


def _cpu() -> str | None:
    try:
        if NO_WINDOWS:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as k:
                return str(winreg.QueryValueEx(k, "ProcessorNameString")[0]).strip()
        import platform
        return platform.processor() or None
    except Exception:  # noqa: BLE001
        return None


def _disco_fisico() -> dict:
    """Modelo, tipo e barramento do disco, pelo Get-PhysicalDisk do Windows; vazio se o comando não existir."""
    if not NO_WINDOWS:
        return {}
    try:
        cmd = ("Get-PhysicalDisk | Select-Object FriendlyName, MediaType, BusType, Size | ConvertTo-Json -Compress")
        saida = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True, timeout=60).stdout.strip()
        dado = json.loads(saida) if saida else []
        discos = dado if isinstance(dado, list) else [dado]
        if not discos:
            return {}
        d = discos[0]
        return {"modelo": d.get("FriendlyName"), "tipo": d.get("MediaType"), "barramento": d.get("BusType"),
                "tamanho_fisico_gb": round(int(d.get("Size") or 0) / 2**30, 1), "discos_fisicos": len(discos)}
    except Exception:  # noqa: BLE001
        return {}


# ! Alteração de IA - Revisar: (01/10/2026, tarde) a descrição da máquina passa a guardar também a memória fisicamente
# instalada (`ram_instalada_gb`), e `completar_maquina` acrescenta esse campo a um disco.json já gravado sem refazer a
# medição do disco.
# ! Motivo: a conta de viabilidade do colibri comparava o "16 GB min" do repositório com os 15,69 GB que o Windows
# enxerga e concluía que a máquina ficava abaixo do mínimo de RAM. Ela tem 16 GB instalados (parte fica reservada para
# o vídeo integrado), ou seja, está exatamente no mínimo declarado. O defeito foi achado na revisão do levantamento.
def memoria_instalada_gb() -> float | None:
    """A memória fisicamente instalada, em GiB (no Windows, GetPhysicallyInstalledSystemMemory; fora dele, None)."""
    try:
        if NO_WINDOWS:
            import ctypes

            kb = ctypes.c_ulonglong(0)
            if ctypes.windll.kernel32.GetPhysicallyInstalledSystemMemory(ctypes.byref(kb)):
                return round(kb.value / 2**20, 2)
    except Exception:  # noqa: BLE001
        pass
    return None


def completar_maquina(arquivo_json: Path, instalada_gb: float | None = None) -> bool:
    """Acrescenta `maquina.ram_instalada_gb` a um disco.json já gravado, se faltar. Não refaz a medição do disco nem
    toca nos outros campos. Devolve True se gravou."""
    dado = json.loads(arquivo_json.read_text(encoding="utf-8"))
    if dado.get("maquina", {}).get("ram_instalada_gb") is not None:
        return False
    valor = instalada_gb if instalada_gb is not None else memoria_instalada_gb()
    if valor is None:
        return False
    dado["maquina"]["ram_instalada_gb"] = valor
    arquivo_json.write_text(json.dumps(dado, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


def descrever_maquina(arquivo: Path) -> dict:
    uso = shutil.disk_usage(arquivo.anchor or "/")
    return {"cpu": _cpu(), "threads": os.cpu_count(), "ram_gb": _ram_total_gb(), "ram_instalada_gb": memoria_instalada_gb(),
            "disco": {**_disco_fisico(), "unidade": arquivo.anchor, "total_gb": round(uso.total / 2**30, 1),
                      "livre_gb": round(uso.free / 2**30, 1)}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--arquivo", help="arquivo grande a ler (padrão: o maior blob do Ollama)")
    ap.add_argument("--blocos", type=int, default=64)
    ap.add_argument("--bloco-mb", type=int, default=19)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--repeticoes", type=int, default=3)
    ap.add_argument("--saida", default=str(SAIDA))
    ap.add_argument("--completar-maquina", action="store_true",
                    help="só acrescenta à saída já gravada os campos da máquina que faltarem (memória instalada), sem medir o disco de novo")
    args = ap.parse_args()
    if args.completar_maquina:
        mudou = completar_maquina(Path(args.saida))
        print(f"{Path(args.saida).name}: memória instalada " + ("gravada" if mudou else "já estava gravada (ou não pôde ser lida)"))
        return 0
    arquivo = Path(args.arquivo) if args.arquivo else maior_blob_do_ollama()
    if arquivo is None or not arquivo.is_file():
        print("nenhum arquivo para ler: passe --arquivo ou instale um modelo no Ollama")
        return 2
    bloco = args.bloco_mb * MB
    print(f"arquivo: {arquivo.name[:24]}… ({arquivo.stat().st_size / 2**30:.2f} GiB); {args.blocos} leituras de {args.bloco_mb} MB, "
          f"{args.threads} threads, {args.repeticoes} repetições por modo")
    diretas, pelo_cache = [], []
    if TEM_LEITURA_DIRETA:
        for i in range(args.repeticoes):
            m = medir(arquivo, bloco, args.blocos, args.threads, direto=True, semente=20261001 + i)
            diretas.append(m)
            print(f"  direto      #{i + 1}: {m['gb_por_s']:.2f} GB/s em {m['segundos']:.2f} s")
    for i in range(args.repeticoes):
        m = medir(arquivo, bloco, args.blocos, args.threads, direto=False, semente=20261101 + i)
        pelo_cache.append(m)
        print(f"  pelo cache  #{i + 1}: {m['gb_por_s']:.2f} GB/s em {m['segundos']:.2f} s")
    registro = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "metodo": "leituras de blocos inteiros em posições sorteadas de um arquivo grande, repartidas entre threads; desenho do "
                  "iobench do colibri (19 MB x 64, 8 threads). 'direto' abre o arquivo sem o cache do sistema; 'pelo_cache' passa "
                  "pelo cache, e a partir da segunda repetição pode vir da RAM.",
        "arquivo": {"nome": arquivo.name, "gb": round(arquivo.stat().st_size / 2**30, 2), "origem": "blob de modelo do Ollama, só leitura"},
        "bloco_bytes": bloco, "blocos": args.blocos, "threads": args.threads,
        "direto": {**resumir(diretas), "medidas": diretas},
        "pelo_cache": {**resumir(pelo_cache), "medidas": pelo_cache},
        "maquina": descrever_maquina(arquivo),
    }
    saida = Path(args.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"gravado: {saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
