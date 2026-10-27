#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria testar_instalador.py, o runner de testes dos scripts da raiz (install.py e run.py),
# no mesmo formato sem pytest dos testers de `Programacao/AgenteCore/experimentos/`: funções teste_<nome>(), main()
# roda todas em ordem de definição e termina em "N testes ok". A tag deste cabeçalho cobre as funções de teste.
# ! Motivo: em 26/10/2026 a máquina corporativa (sem administrador) mostrou que o instalador parava no MSI do MariaDB e
# que o `run.py` morria em silêncio quando a venv da CobaiaAPI tinha sido criada em outra pasta (os lançadores `.exe`
# dela saem com código 1 sem mensagem). As partes puras do conserto (escolher o zip e o SHA-256 na resposta da API
# do MariaDB, montar os caminhos do portátil, decidir quando usá-lo, conferir o hash, extrair sem sair da pasta, e o
# comando da API pelo `python -m uvicorn`) precisam de teste sem rede e sem baixar nada; os testes são escritos ANTES
# das funções, e a primeira rodada falha por AttributeError nos nomes novos, que é o RED aceito.
"""Testes dos scripts da raiz (install.py e run.py), sem pytest (asserts em Python puro)."""
import hashlib
import inspect
import shutil
import sys
import tempfile
import traceback
import zipfile
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

import install
import run

_TEMPORARIOS: list[Path] = []


def _pasta_temporaria() -> Path:
    p = Path(tempfile.mkdtemp(prefix="cobaia_teste_"))
    _TEMPORARIOS.append(p)
    return p


RESPOSTA_API = {
    "releases": {
        "11.8.8": {"release_id": "11.8.8", "files": [
            {"file_name": "mariadb-11.8.8-winx64.zip", "file_download_url": "http://x/11.8.8/mariadb-11.8.8-winx64.zip",
             "checksum": {"sha256sum": "a" * 64}}]},
        "11.8.9": {"release_id": "11.8.9", "files": [
            {"file_name": "mariadb-11.8.9-winx64.msi", "file_download_url": "http://x/11.8.9/mariadb-11.8.9-winx64.msi",
             "checksum": {"sha256sum": "b" * 64}},
            {"file_name": "mariadb-11.8.9-winx64-debugsymbols.zip",
             "file_download_url": "http://x/11.8.9/mariadb-11.8.9-winx64-debugsymbols.zip", "checksum": {"sha256sum": "c" * 64}},
            {"file_name": "mariadb-11.8.9-winx64.zip", "file_download_url": "http://x/11.8.9/mariadb-11.8.9-winx64.zip",
             "checksum": {"sha256sum": "d" * 64}}]},
    }
}


def teste_escolher_zip_mariadb_pega_a_versao_mais_nova_e_o_winx64():
    escolha = install.escolher_zip_mariadb(RESPOSTA_API)
    assert escolha == {"versao": "11.8.9", "nome": "mariadb-11.8.9-winx64.zip",
                       "url": "http://x/11.8.9/mariadb-11.8.9-winx64.zip", "sha256": "d" * 64}, escolha
    # a ordem das chaves não manda: 11.8.10 depois de 11.8.9 é a mais nova
    resposta = {"releases": {"11.8.9": RESPOSTA_API["releases"]["11.8.9"],
                             "11.8.10": {"release_id": "11.8.10", "files": [
                                 {"file_name": "mariadb-11.8.10-winx64.zip", "file_download_url": "http://x/10.zip",
                                  "checksum": {"sha256sum": "e" * 64}}]}}}
    assert install.escolher_zip_mariadb(resposta)["versao"] == "11.8.10"


def teste_escolher_zip_mariadb_sem_arquivo_da_erro():
    for resposta in ({"releases": {}}, {"releases": {"11.8.9": {"release_id": "11.8.9", "files": [
            {"file_name": "mariadb-11.8.9-winx64.msi", "file_download_url": "u", "checksum": {"sha256sum": "b" * 64}}]}}}):
        try:
            install.escolher_zip_mariadb(resposta)
        except ValueError as e:
            assert "winx64.zip" in str(e), e
        else:
            raise AssertionError("escolher_zip_mariadb aceitou resposta sem o zip")


def teste_caminhos_mariadb_portatil():
    base = Path(r"C:\x\MariaDB")
    c = install.caminhos_mariadb_portatil("11.8.9", base=base)
    assert c["base"] == base, c
    assert c["zip"] == base / "download" / "mariadb-11.8.9-winx64.zip", c["zip"]
    assert c["pasta"] == base / "mariadb-11.8.9-winx64", c["pasta"]
    assert c["install_db"] == base / "mariadb-11.8.9-winx64" / "bin" / "mariadb-install-db.exe", c["install_db"]
    assert c["dados"] == base / "data" and c["my_ini"] == base / "data" / "my.ini", c
    # sem base, cai em %LOCALAPPDATA%\MariaDB
    padrao = install.caminhos_mariadb_portatil("11.8.9")
    assert padrao["base"].name == "MariaDB" and padrao["base"].parent.name == "Local", padrao["base"]


def teste_usar_mariadb_portatil():
    assert install.usar_mariadb_portatil(so="Windows", admin=False, ambiente={}) is True
    assert install.usar_mariadb_portatil(so="Windows", admin=True, ambiente={}) is False
    assert install.usar_mariadb_portatil(so="Linux", admin=False, ambiente={}) is False
    assert install.usar_mariadb_portatil(so="Windows", admin=True, ambiente={"COBAIA_MARIADB_PORTATIL": "1"}) is True
    assert install.usar_mariadb_portatil(so="Windows", admin=False, ambiente={"COBAIA_MARIADB_PORTATIL": "0"}) is False


def teste_conferir_sha256_e_extrair_zip_seguro():
    tmp = _pasta_temporaria()
    z = tmp / "mariadb-9.9.9-winx64.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("mariadb-9.9.9-winx64/bin/mariadb-install-db.exe", b"nao e um exe")
        zf.writestr("mariadb-9.9.9-winx64/README.md", "ola")
    esperado = hashlib.sha256(z.read_bytes()).hexdigest()
    assert install.conferir_sha256(z, esperado) is True
    assert install.conferir_sha256(z, esperado.upper()) is True
    assert install.conferir_sha256(z, "0" * 64) is False
    destino = tmp / "MariaDB"
    install.extrair_zip_seguro(z, destino)
    assert (destino / "mariadb-9.9.9-winx64" / "bin" / "mariadb-install-db.exe").read_bytes() == b"nao e um exe"
    ruim = tmp / "ruim.zip"
    with zipfile.ZipFile(ruim, "w") as zf:
        zf.writestr("../fora.txt", "x")
    try:
        install.extrair_zip_seguro(ruim, tmp / "destino2")
    except ValueError as e:
        assert "fora" in str(e), e
    else:
        raise AssertionError("extrair_zip_seguro aceitou caminho fora do destino")
    assert not (tmp / "fora.txt").exists()


def teste_comando_api_usa_o_python_da_venv():
    venv = Path(r"C:\x\CobaiaAPI\.venv")
    cmd = run.comando_api(venv, so="Windows")
    assert cmd == [str(venv / "Scripts" / "python.exe"), "-m", "uvicorn", "app.main:app", "--port", str(run.API_PORT)], cmd
    cmd = run.comando_api(venv, so="Linux")
    assert cmd[0] == str(venv / "bin" / "python") and cmd[1:3] == ["-m", "uvicorn"], cmd
    assert "uvicorn.exe" not in " ".join(run.comando_api(venv, so="Windows"))


def main() -> None:
    modulo = sys.modules[__name__]
    testes = [(nome, obj) for nome, obj in vars(modulo).items()
              if nome.startswith("teste_") and inspect.isfunction(obj) and obj.__module__ == modulo.__name__]
    try:
        for nome, funcao in testes:
            try:
                funcao()
            except Exception:
                print(nome)
                traceback.print_exc()
                sys.exit(1)
            print(f"{nome} ok")
        print(f"{len(testes)} testes ok")
    finally:
        for caminho in _TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)


if __name__ == "__main__":
    main()
