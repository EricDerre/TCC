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
import json
# ! Alteração de IA - Revisar: entra o import de `os` (usado só por `teste_fixa_windows_onde_o_env_common_procura` e `teste_fixa_windows_setup_agente_core`).
# ! Motivo: o primeiro monta os padrões esperados com `os.path.expandvars`, igual a `_env_common.py`, e o segundo tira e repõe `COBAIA_MODELO_LLM` de `os.environ`; sem o import os dois dão NameError.
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import traceback
import zipfile
from datetime import datetime
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

import _env_common as env
import install
import run

# ! Alteração de IA - Revisar: entram os imports do pacote I1 (`atualizar_versoes`, `empacotar`, `instalador.*`) e os `zipfile`,
# `tarfile`, `subprocess` e `shutil` que os testes do empacotador e da prova usam.
# ! Motivo: sem esses módulos os testes novos (versoes.json, uv_fixado.txt, empacotador, registro.json, conferir.py) não rodam.
sys.path.insert(0, str(RAIZ / "ferramentas" / "instalador_matriz"))
import atualizar_versoes
import empacotar
# ! Alteração de IA - Revisar: (25/11/2026, pacote I5) entra o import de `celula_actions` (roteiro da célula no GitHub Actions); `from datetime import datetime` entra junto dos imports padrão.
# ! Motivo: os testes novos do roteiro do GitHub Actions chamam as funções dele e montam datas fixas; sem o import dão NameError.
import celula_actions
# ! Alteração de IA - Revisar: (25/11/2026, pacote I7) entram os imports de `importar_actions` e `ler_celula` (traz a evidência do GitHub para `celulas/` e lê o resumo dela).
# ! Motivo: os testes novos do importador chamam as funções dele e conferem o que `ler_celula.resumir` lê da rodada gravada.
import importar_actions
import ler_celula
# ! Alteração de IA - Revisar: (25/11/2026, pacote I7) entra o import de `relatorio` (lê todas as rodadas de `celulas/` e cola os blocos gerados no relatório do instalador, no README e no DETALHES-TECNICOS).
# ! Motivo: os testes novos do relatório chamam `coletar`, `por_celula`, os blocos e `colar`; sem o import dão NameError.
import relatorio

# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) o import deixa de trazer `nucleo` e `servicos`; fica `conferir, ferramentas, registro, sistema, versoes`.
# ! Motivo: `instalador/nucleo.py` e `instalador/servicos.py` (pontos de entrada provisórios do pacote I2) deixaram de existir; os testes chamam os passos de `instalador/ferramentas.py` direto e o resto pelo `install.py` e pelo `_env_common.py`.
from instalador import conferir, ferramentas, registro, sistema, versoes

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
    # ! Alteração de IA - Revisar: (07/11/2026, ficha 55) a pasta de dados fica dentro do projeto (`.mariadb/data`), não mais em
    # `%LOCALAPPDATA%\MariaDB\data`; `dados=` troca o lugar só nos testes. Os binários continuam em `%LOCALAPPDATA%\MariaDB`.
    # ! Motivo: o app Claude é um pacote MSIX e o que ele grava em AppData\Local vai para uma pasta privada; o servidor subido de
    # dentro do app misturava o dicionário do InnoDB privado com as tabelas da cópia real (erro 1932 em todas as tabelas) e, numa
    # partida, apagou os .ibd da cópia real. A pasta do projeto não é virtualizada: as duas janelas enxergam a mesma pasta.
    assert c["dados"] == install.DATADIR_DO_PROJETO == env.REPO_ROOT / ".mariadb" / "data", c["dados"]
    assert c["my_ini"] == install.DATADIR_DO_PROJETO / "my.ini", c["my_ini"]
    outra = install.caminhos_mariadb_portatil("11.8.9", base=base, dados=Path(r"C:\y\dados"))
    assert outra["dados"] == Path(r"C:\y\dados") and outra["my_ini"] == Path(r"C:\y\dados") / "my.ini", outra
    # sem base, os binários continuam em %LOCALAPPDATA%\MariaDB
    padrao = install.caminhos_mariadb_portatil("11.8.9")
    assert padrao["base"].name == "MariaDB" and padrao["base"].parent.name == "Local", padrao["base"]


def teste_my_ini_do_projeto_vem_antes_do_de_appdata():
    # ! Alteração de IA - Revisar: (07/11/2026, ficha 55) find_mariadb_datadir_config prefere o my.ini de `.mariadb/data` na raiz do repositório.
    # ! Motivo: é o que faz as duas janelas (a do Eric e a do app) subirem o servidor com a mesma pasta de dados; o caminho de
    # AppData continua valendo numa máquina que só tem a instalação antiga.
    raiz = Path(tempfile.mkdtemp(prefix="cobaia_raiz_"))
    try:
        assert env.find_mariadb_datadir_config(raiz=raiz) != str(raiz / ".mariadb" / "data" / "my.ini")
        (raiz / ".mariadb" / "data").mkdir(parents=True)
        (raiz / ".mariadb" / "data" / "my.ini").write_text("[mysqld]\n", encoding="utf-8")
        assert env.find_mariadb_datadir_config(raiz=raiz) == str(raiz / ".mariadb" / "data" / "my.ini")
    finally:
        shutil.rmtree(raiz, ignore_errors=True)


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


# ! Alteração de IA - Revisar: a partir daqui entram os testes do pacote I1 do instalador único (registro de versões, sistema,
# registro da prova, conferência em quatro níveis, empacotador do repositório e formato do roteiro da célula de WSL), todos sem rede
# e sem subir serviço.
# ! Motivo: o instalador nunca rodou em máquina limpa; as peças novas (instalador/ e ferramentas/instalador_matriz/) precisam de
# teste antes de qualquer célula de WSL ou de máquina virtual usá-las.
def teste_versao_tupla_acha_a_primeira_sequencia_de_numeros():
    assert versoes.versao_tupla("8.2.35") == (8, 2, 35)
    assert versoes.versao_tupla("v0.40.16") == (0, 40, 16)
    assert versoes.versao_tupla("PHP 8.2.35 (cli) (built: Oct 20 2026)") == (8, 2, 35)
    assert versoes.versao_tupla("10.11.7-MariaDB-1ubuntu0.24.04") == (10, 11, 7)
    assert versoes.versao_tupla("sem numero") == ()
    assert versoes.versao_tupla("") == ()


def teste_comparar_versao_igual_na_faixa_e_fora():
    php = {"testada": "8.2.35", "aceita_de": "8.1", "aceita_ate": "8.5"}
    assert versoes.comparar("8.2.35", php) == "igual"
    assert versoes.comparar("8.3.6", php) == "na_faixa"
    assert versoes.comparar("8.5.12", php) == "na_faixa"  # o teto "8.5" aceita qualquer 8.5.x
    assert versoes.comparar("8.1.2", php) == "na_faixa"
    assert versoes.comparar("8.0.30", php) == "fora_da_faixa"
    assert versoes.comparar("8.6.0", php) == "fora_da_faixa"
    assert versoes.comparar("", php) == "desconhecida"
    assert versoes.comparar("nao sei", php) == "desconhecida"
    sem_teto = {"testada": "0.40.16", "aceita_de": "0.40.2", "aceita_ate": ""}
    assert versoes.comparar("0.41.0", sem_teto) == "na_faixa"
    assert versoes.comparar("0.40.1", sem_teto) == "fora_da_faixa"


def teste_comparar_identificador_do_modelo():
    modelo = {"testada": "845dbda0ea48", "identificador": True}
    assert versoes.comparar_identificador("845dbda0ea48", modelo) == "igual"
    assert versoes.comparar_identificador("845dbda0ea48ed749caafd9e6037047aa19acfcfd82e704d7ca97d631a0b697e", modelo) == "igual"
    assert versoes.comparar_identificador("deadbeef0000", modelo) == "fora_da_faixa"
    assert versoes.comparar_identificador("", modelo) == "desconhecida"


def teste_julgar_modo_normal_e_reproduzir():
    ferramentas = {
        "ollama": {"testada": "0.40.16", "aceita_de": "0.40.2", "aceita_ate": "", "afeta_medida": True},
        "php": {"testada": "8.2.35", "aceita_de": "8.1", "aceita_ate": "8.5", "afeta_medida": False},
        "modelo": {"testada": "845dbda0ea48", "identificador": True, "afeta_medida": True},
    }
    achadas = {"ollama": "0.40.17", "php": "8.3.6", "modelo": "845dbda0ea48"}
    normal = versoes.julgar(achadas, ferramentas)
    assert normal["ollama"] == {"encontrada": "0.40.17", "testada": "0.40.16", "estado": "na_faixa", "impede": False}, normal
    assert normal["php"]["impede"] is False and normal["modelo"]["estado"] == "igual"
    exato = versoes.julgar(achadas, ferramentas, reproduzir=True)
    assert exato["ollama"]["impede"] is True   # afeta a medida e não é a versão exata
    assert exato["php"]["impede"] is False     # não afeta a medida: a faixa basta
    assert exato["modelo"]["impede"] is False
    fora = versoes.julgar({"php": "7.4.33"}, ferramentas)
    assert fora == {"php": {"encontrada": "7.4.33", "testada": "8.2.35", "estado": "fora_da_faixa", "impede": True}}, fora


def teste_gerar_uv_fixado_tem_uma_linha_por_chave():
    downloads = {alvo: {"url": f"https://x/{alvo}", "sha256": "a" * 64} for alvo in versoes.ALVOS_UV}
    ferramentas = {"uv": {"testada": "0.13.9", "downloads": downloads},
                   "python": {"testada": "3.14.7", "aceita_de": "3.12"}}
    texto = versoes.gerar_uv_fixado(ferramentas)
    linhas = [l for l in texto.splitlines() if l and not l.startswith("#")]
    assert linhas[:3] == ["UV_VERSAO=0.13.9", "PYTHON_VERSAO=3.14", "PYTHON_MINIMO=3.12"], linhas[:3]
    assert "UV_WINDOWS_X86_64_URL=https://x/windows-x86_64" in linhas
    assert "UV_LINUX_X86_64_SHA256=" + "a" * 64 in linhas
    assert len(linhas) == 3 + 2 * len(versoes.ALVOS_UV)
    assert texto.endswith("\n") and "\r" not in texto
    assert all(ord(c) < 128 for c in texto), "o arquivo é lido pelo PowerShell 5.1 e pelo shell: só ASCII"


def teste_ollama_das_pontes_pega_a_ultima_pareavel_e_o_piso_da_serie():
    pontes = {"pontes": [
        {"versao": "0.34.4", "data": "2026-09-30", "pareavel": True},
        {"versao": "0.40.2", "data": "2026-10-23", "pareavel": True},
        {"versao": "0.40.16", "data": "2026-11-16", "pareavel": True},
        {"versao": "0.40.15", "data": "2026-11-11", "pareavel": True},
        {"versao": "0.40.17", "data": "2026-11-17", "pareavel": False},
    ]}
    assert atualizar_versoes.ollama_das_pontes(pontes) == {"testada": "0.40.16", "aceita_de": "0.40.2"}


def teste_leitores_das_fontes_locais():
    assert atualizar_versoes.playwright_do_requirements("matplotlib>=3.9\n# nota\nplaywright==1.64.1\n") == "1.64.1"
    assert atualizar_versoes.python_da_venv("home = C:\\Python314\nversion = 3.14.7\n") == "3.14.7"
    ambiente = {"cobaias": {"mariadbd": r"C:\x\MariaDB\mariadb-11.8.9-winx64\bin\mariadbd.exe"},
                "versoes": {"navegador": "156.0.8078.4"}}
    assert atualizar_versoes.mariadb_do_ambiente(ambiente) == "11.8.9"
    assert atualizar_versoes.chromium_do_ambiente(ambiente) == "156.0.8078.4"
    assert atualizar_versoes.php_da_saida("PHP 8.2.35 (cli) (built: Oct 20 2026 04:17:59) (ZTS Visual C++ 2019 x64)\n") == "8.2.35"


def teste_modelo_do_manifesto():
    bruto = (b'{"schemaVersion":2,"config":{"digest":"sha256:cfg"},"layers":['
             b'{"mediaType":"application/vnd.ollama.image.model","digest":"sha256:' + b"b" * 64 + b'","size":123},'
             b'{"mediaType":"application/vnd.ollama.image.license","digest":"sha256:lic","size":9}]}')
    m = atualizar_versoes.modelo_do_manifesto(bruto)
    assert m == {"testada": hashlib.sha256(bruto).hexdigest()[:12], "pesos_sha256": "b" * 64, "pesos_bytes": 123}, m


def teste_montar_junta_fontes_faixas_e_mantem_os_downloads_do_uv():
    locais = {"ollama": {"testada": "0.40.16", "aceita_de": "0.40.2", "origem": "pontes"},
              "playwright": {"testada": "1.64.1", "origem": "requirements"},
              "php": {"testada": "8.2.35", "origem": "php -v"}}
    anterior = {"ferramentas": {"uv": {"testada": atualizar_versoes.UV_VERSAO, "downloads": {"linux-x86_64": {"url": "u", "sha256": "s"}}},
                                "python": {"testada": "3.14.7", "aceita_de": "3.12", "aceita_ate": "", "afeta_medida": False, "origem": "venv"}}}
    dados = atualizar_versoes.montar(locais, anterior)
    f = dados["ferramentas"]
    assert set(dados["tag_ia"]) == {"alteracao", "motivo"}
    assert f["ollama"] == {"testada": "0.40.16", "aceita_de": "0.40.2", "aceita_ate": "", "afeta_medida": True, "origem": "pontes"}, f["ollama"]
    assert f["playwright"]["aceita_de"] == f["playwright"]["aceita_ate"] == "1.64.1" and f["playwright"]["afeta_medida"] is True
    assert (f["php"]["aceita_de"], f["php"]["aceita_ate"], f["php"]["afeta_medida"]) == ("8.1", "8.5", False)
    assert f["uv"]["downloads"] == {"linux-x86_64": {"url": "u", "sha256": "s"}}   # o que veio da rede fica
    assert f["python"]["testada"] == "3.14.7"   # fonte que faltou nesta máquina mantém o valor anterior


def teste_versoes_json_bate_com_as_fontes_do_repositorio():
    dados = versoes.carregar()
    for nome, local in atualizar_versoes.coletar_do_repositorio(RAIZ).items():
        assert dados[nome]["testada"] == local["testada"], (nome, dados[nome]["testada"], local["testada"])


def teste_uv_fixado_bate_com_o_versoes_json():
    gravado = (RAIZ / "instalador" / "uv_fixado.txt").read_text(encoding="ascii")
    assert gravado == versoes.gerar_uv_fixado(versoes.carregar())


OS_UBUNTU = 'PRETTY_NAME="Ubuntu 24.04.5 LTS"\nNAME="Ubuntu"\nVERSION_ID="24.04"\nID=ubuntu\nID_LIKE=debian\n'
OS_UBUNTU_ANTIGO = 'PRETTY_NAME="Ubuntu 20.04.6 LTS"\nVERSION_ID="20.04"\nID=ubuntu\nID_LIKE=debian\n'
OS_DEBIAN = 'PRETTY_NAME="Debian GNU/Linux 13 (trixie)"\nVERSION_ID="13"\nID=debian\n'
OS_MINT = 'NAME="Linux Mint"\nVERSION_ID="22.3"\nID=linuxmint\nID_LIKE="ubuntu debian"\n'
OS_FEDORA = 'NAME="Fedora Linux"\nVERSION_ID=45\nID=fedora\n'
OS_ARCH = '# comentario\nNAME="Arch Linux"\nID=arch\n\n'
OS_SUSE = 'NAME="openSUSE Tumbleweed"\nID="opensuse-tumbleweed"\nID_LIKE="opensuse suse"\n'


def teste_ler_os_release_tira_aspas_comentario_e_linha_vazia():
    assert sistema.ler_os_release(OS_ARCH) == {"NAME": "Arch Linux", "ID": "arch"}
    assert sistema.ler_os_release(OS_MINT)["ID_LIKE"] == "ubuntu debian"


def _resumo(info: dict) -> tuple:
    return info["familia"], info["id"], info["versao"], info["suporte"]


def teste_familia_por_sistema():
    f, ler = sistema.familia, sistema.ler_os_release
    assert _resumo(f("Windows")) == ("windows", "windows", "", "suportado")
    assert _resumo(f("Linux", ler(OS_UBUNTU))) == ("apt", "ubuntu", "24.04", "suportado")
    assert f("Linux", ler(OS_UBUNTU))["nome"] == "Ubuntu 24.04.5 LTS"
    assert _resumo(f("Linux", ler(OS_DEBIAN))) == ("apt", "debian", "13", "suportado")
    assert _resumo(f("Linux", ler(OS_UBUNTU_ANTIGO))) == ("apt", "ubuntu", "20.04", "melhor_esforco")
    assert _resumo(f("Linux", ler(OS_MINT))) == ("apt", "linuxmint", "22.3", "melhor_esforco")
    assert _resumo(f("Linux", ler(OS_FEDORA))) == ("dnf", "fedora", "45", "melhor_esforco")
    assert _resumo(f("Linux", ler(OS_ARCH))) == ("nao_suportado", "arch", "", "nao_suportado")
    assert _resumo(f("Linux", ler(OS_SUSE))) == ("nao_suportado", "opensuse-tumbleweed", "", "nao_suportado")
    assert _resumo(f("Linux", {})) == ("nao_suportado", "", "", "nao_suportado")
    assert _resumo(f("Darwin", tem_brew=True)) == ("brew", "macos", "", "suportado")
    assert _resumo(f("Darwin", tem_brew=False)) == ("brew", "macos", "", "falta_homebrew")
    assert _resumo(f("FreeBSD")) == ("nao_suportado", "freebsd", "", "nao_suportado")


def teste_pacotes_por_familia():
    apt = sistema.pacotes("apt")
    assert {"php-cli", "php-mysql", "php-mbstring"} <= set(apt["php"]), apt["php"]
    assert apt["mariadb"] == ["mariadb-server"] and apt["venv"] == ["python3-venv"]
    assert {"curl", "ca-certificates", "zstd"} <= set(apt["base"])
    dnf = sistema.pacotes("dnf")
    assert {"php-cli", "php-mysqlnd", "php-mbstring"} <= set(dnf["php"]) and dnf["mariadb"] == ["mariadb-server"]
    # ! Alteração de IA - Revisar: (19/11/2026, célula L-F45 em modo `novo`) a tabela do `dnf` tem de trazer o `gawk`.
    # ! Motivo: na rodada 20261119-134801 o script oficial do Ollama parou com "The following tools are required but missing:
    # - awk": a imagem do Fedora 45 para o WSL não traz o `awk`, e o instalador saiu com erro depois de o site já estar pronto.
    assert {"curl", "zstd", "gawk"} <= set(dnf["base"]), dnf["base"]
    for sem_tabela in ("nao_suportado", "windows", "brew"):
        try:
            sistema.pacotes(sem_tabela)
        except ValueError as e:
            assert sem_tabela in str(e), e
        else:
            raise AssertionError(f"pacotes({sem_tabela!r}) devia recusar")


def teste_mensagem_nao_suportado_diz_o_sistema_e_o_que_instalar():
    ferramentas = {"php": {"aceita_de": "8.1", "aceita_ate": "8.5"}, "mariadb": {"aceita_de": "10.6"}, "python": {"aceita_de": "3.12"}}
    texto = sistema.mensagem_nao_suportado(sistema.familia("Linux", sistema.ler_os_release(OS_ARCH)), ferramentas)
    for pedaco in ("Arch Linux", "PHP 8.1 a 8.5", "mysqli", "mbstring", "MariaDB 10.6", "Python 3.12", "Ollama",
                   "Ubuntu 22.04, 24.04 e 26.04", "Debian 12 e 13"):
        assert pedaco in texto, (pedaco, texto)
    assert "—" not in texto and "→" not in texto


def teste_registro_novo_tem_os_quatro_niveis_sem_rodar():
    reg = registro.novo("L-U2404", {"familia": "apt", "nome": "Ubuntu 24.04.5 LTS"}, {"memoria_gb": 7.6})
    assert reg["celula"] == "L-U2404" and reg["sistema"]["familia"] == "apt" and reg["maquina"] == {"memoria_gb": 7.6}
    assert list(reg["niveis"]) == ["N1", "N2", "N3", "N4"]
    assert all(n == {"estado": "nao_rodou", "detalhe": "", "segundos": None} for n in reg["niveis"].values())
    assert set(reg["tag_ia"]) == {"alteracao", "motivo"} and reg["versoes"] == {}


def teste_registro_nivel_alcancado_e_falha():
    reg = registro.novo("x", {}, {})
    assert registro.alcancado(reg) == "N0" and registro.falhou(reg) is False
    registro.anotar_nivel(reg, "N1", "passou", "14 produtos", 12.5)
    registro.anotar_nivel(reg, "N2", "passou")
    registro.anotar_nivel(reg, "N3", "passou")
    registro.anotar_nivel(reg, "N4", "nao_coube", "3,1 GB livres")
    assert registro.alcancado(reg) == "N3"
    assert registro.falhou(reg) is False          # não caber na memória não é falha do instalador
    assert reg["niveis"]["N1"] == {"estado": "passou", "detalhe": "14 produtos", "segundos": 12.5}
    registro.anotar_nivel(reg, "N2", "falhou", "chromium: error while loading shared libraries: libnss3.so")
    assert registro.alcancado(reg) == "N1" and registro.falhou(reg) is True
    for ruim in (("N5", "passou"), ("N1", "talvez")):
        try:
            registro.anotar_nivel(reg, *ruim)
        except ValueError:
            pass
        else:
            raise AssertionError(f"anotar_nivel aceitou {ruim}")


def teste_registro_anota_versoes_e_grava():
    ferramentas = {"php": {"testada": "8.2.35", "aceita_de": "8.1", "aceita_ate": "8.5", "afeta_medida": False}}
    reg = registro.novo("x", {}, {})
    registro.anotar_versoes(reg, {"php": "8.3.6"}, ferramentas)
    assert reg["versoes"] == {"php": {"encontrada": "8.3.6", "testada": "8.2.35", "estado": "na_faixa", "impede": False}}
    pasta = _pasta_temporaria()
    caminho = registro.gravar(reg, pasta / "evidencia")
    assert caminho == pasta / "evidencia" / "registro.json"
    lido = json.loads(caminho.read_text(encoding="utf-8"))
    assert lido["versoes"]["php"]["estado"] == "na_faixa" and lido["alcancado"] == "N0" and lido["falhou"] is False
    assert lido["impedida_por_versao"] == []


def _sonda_de_mentira(chamadas: list, nome: str, estado: str, detalhe: str = ""):
    def sonda():
        chamadas.append(nome)
        return estado, detalhe
    return sonda


def teste_conferir_roda_os_niveis_e_respeita_os_requisitos():
    chamadas = []
    sondas = {"N1": _sonda_de_mentira(chamadas, "N1", "falhou", "a porta 8080 não respondeu"),
              "N2": _sonda_de_mentira(chamadas, "N2", "passou"),
              "N3": _sonda_de_mentira(chamadas, "N3", "passou", "qwen2.5:0.5b respondeu"),
              "N4": _sonda_de_mentira(chamadas, "N4", "nao_coube", "3,1 GB livres")}
    reg = conferir.rodar(registro.novo("L-U2404", {}, {}), sondas)
    assert chamadas == ["N1", "N3", "N4"], chamadas            # o N2 precisa do N1, que falhou
    assert reg["niveis"]["N1"]["estado"] == "falhou" and reg["niveis"]["N1"]["detalhe"] == "a porta 8080 não respondeu"
    assert reg["niveis"]["N2"] == {"estado": "nao_rodou", "detalhe": "depende do N1, que não passou", "segundos": None}
    assert reg["niveis"]["N3"]["estado"] == "passou" and isinstance(reg["niveis"]["N3"]["segundos"], float)
    assert reg["niveis"]["N4"]["estado"] == "nao_coube"
    assert registro.alcancado(reg) == "N0" and registro.falhou(reg) is True


def teste_conferir_para_no_nivel_pedido():
    chamadas = []
    sondas = {n: _sonda_de_mentira(chamadas, n, "passou") for n in registro.NIVEIS}
    reg = conferir.rodar(registro.novo("x", {}, {}), sondas, ate="N2")
    assert chamadas == ["N1", "N2"], chamadas
    assert reg["niveis"]["N3"]["estado"] == "nao_rodou" and registro.alcancado(reg) == "N2"


def teste_conferir_sonda_que_estoura_vira_falha_com_o_erro_literal():
    def estoura():
        raise RuntimeError("SQL falhou (código 1): ERROR 1698 (28000): Access denied for user 'root'@'localhost'")
    sondas = {"N1": estoura, "N2": lambda: ("passou", ""), "N3": lambda: ("passou", ""), "N4": lambda: ("passou", "")}
    reg = conferir.rodar(registro.novo("x", {}, {}), sondas)
    assert reg["niveis"]["N1"]["estado"] == "falhou"
    assert "RuntimeError" in reg["niveis"]["N1"]["detalhe"] and "ERROR 1698" in reg["niveis"]["N1"]["detalhe"]
    assert reg["niveis"]["N2"]["estado"] == "nao_rodou" and reg["niveis"]["N3"]["estado"] == "passou"


def teste_conferir_erro_http_guarda_o_corpo_e_classifica_falta_de_memoria():
    erro = conferir.ErroHttp(500, "http://127.0.0.1:11434/api/generate",
                             '{"error":"model requires more system memory (5.5 GiB) than is available (3.1 GiB)"}')
    assert isinstance(erro, OSError) and erro.status == 500
    assert "HTTP 500" in str(erro) and "more system memory" in str(erro)
    assert conferir.classificar_erro_do_ollama(erro.corpo) == "nao_coube"
    assert conferir.classificar_erro_do_ollama('{"error":"model not found"}') == "falhou"
    assert conferir.classificar_erro_do_ollama("") == "falhou"


def teste_conferir_identificador_do_modelo_nas_tags_do_ollama():
    tags = {"models": [
        {"name": "qwen2.5:0.5b", "model": "qwen2.5:0.5b", "digest": "a8b0c5157701" + "0" * 52},
        {"name": "qwen2.5:7b", "model": "qwen2.5:7b", "digest": "sha256:845dbda0ea48" + "f" * 52},
    ]}
    assert conferir.identificador_nas_tags(tags, "qwen2.5:7b") == "845dbda0ea48" + "f" * 52
    assert conferir.identificador_nas_tags(tags, "qwen2.5:0.5b").startswith("a8b0c5157701")
    assert conferir.identificador_nas_tags(tags, "outro:1b") == ""
    assert conferir.identificador_nas_tags({}, "qwen2.5:7b") == ""


def teste_conferir_extrair_versao_de_cada_ferramenta():
    e = conferir.extrair_versao
    assert e("ollama", "ollama version is 0.40.16\n") == "0.40.16"
    assert e("ollama", "Warning: could not connect to a running Ollama instance\nWarning: client version is 0.40.16\n") == "0.40.16"
    assert e("mariadb", r"C:\Users\aluno2\AppData\Local\MariaDB\mariadb-11.8.9-winx64\bin\mariadbd.exe  Ver 11.8.9-MariaDB for Win64 on AMD64") == "11.8.9"
    assert e("mariadb", "mariadbd  Ver 10.11.7-MariaDB-1ubuntu0.24.04.1 for debian-linux-gnu on x86_64 (Ubuntu 24.04)") == "10.11.7"
    assert e("php", "PHP 8.3.6 (cli) (built: Jul 14 2025 18:30:55) (NTS)\nCopyright (c) The PHP Group\n") == "8.3.6"
    assert e("ollama", "Warning: could not connect to a running Ollama instance\n") == ""
    assert e("outra", "1.2.3") == ""


def teste_conferir_memoria_do_meminfo():
    texto = "MemTotal:        8040116 kB\nMemFree:          812340 kB\nMemAvailable:    6291456 kB\nBuffers:           1234 kB\n"
    assert conferir.memoria_do_meminfo(texto) == {"memoria_total_gb": 7.7, "memoria_livre_gb": 6.0}
    assert conferir.memoria_do_meminfo("MemTotal: 1048576 kB\n") == {"memoria_total_gb": 1.0}
    assert conferir.memoria_do_meminfo("") == {}


def teste_registro_impedida_por_versao():
    ferramentas = {"php": {"testada": "8.2.35", "aceita_de": "8.1", "aceita_ate": "8.5", "afeta_medida": False},
                   "ollama": {"testada": "0.40.16", "aceita_de": "0.40.2", "aceita_ate": "", "afeta_medida": True}}
    reg = registro.novo("x", {}, {})
    registro.anotar_versoes(reg, {"php": "7.4.33", "ollama": "0.40.17"}, ferramentas)
    assert registro.impedida_por_versao(reg) == ["php"]                    # modo normal: só a que saiu da faixa
    registro.anotar_versoes(reg, {"php": "7.4.33", "ollama": "0.40.17"}, ferramentas, reproduzir=True)
    assert registro.impedida_por_versao(reg) == ["ollama", "php"]          # reproduzir: a que afeta a medida tem de ser exata


def _git(pasta: Path, *argumentos: str) -> None:
    subprocess.run(["git", "-C", str(pasta), *argumentos], check=True, capture_output=True)


def _repositorio_de_teste() -> Path:
    raiz = _pasta_temporaria() / "repo"
    raiz.mkdir()
    _git(raiz, "init", "-q")
    for chave, valor in (("user.name", "teste"), ("user.email", "teste@exemplo.invalid"), ("core.autocrlf", "true")):
        _git(raiz, "config", chave, valor)
    (raiz / "install.sh").write_bytes(b"#!/usr/bin/env bash\r\necho oi\r\n")     # CRLF no working tree, como no Windows
    (raiz / "LEIAME.md").write_bytes(b"linha\n")
    (raiz / "bin.dat").write_bytes(b"\x00\x01\r\n\x02")                          # binário: não muda
    (raiz / "apagado.txt").write_bytes(b"x\n")
    _git(raiz, "add", "-A")
    _git(raiz, "commit", "-q", "-m", "inicial")
    (raiz / "apagado.txt").unlink()                                              # rastreado e apagado: fica de fora
    (raiz / "LEIAME.md").write_bytes(b"linha alterada\r\n")                      # alterado sem add: entra como está, com LF
    (raiz / "instalador").mkdir()
    (raiz / "instalador" / "novo.py").write_bytes(b"x = 1\r\n")                  # novo, sem add: entra (está em EXTRAS)
    (raiz / "instalador" / "__pycache__").mkdir()
    (raiz / "instalador" / "__pycache__" / "novo.pyc").write_bytes(b"\x00")
    (raiz / "rascunho.txt").write_bytes(b"fora\n")                               # novo fora de EXTRAS: fica de fora
    (raiz / ".gitignore").write_bytes(b"__pycache__/\n")
    return raiz


def teste_empacotar_lista_rastreados_e_extras():
    raiz = _repositorio_de_teste()
    nomes = sorted(item["caminho"] for item in empacotar.listar(raiz))
    assert nomes == ["LEIAME.md", "bin.dat", "instalador/novo.py", "install.sh"], nomes


def teste_empacotar_fim_de_linha_e_modo_como_o_git_entrega():
    raiz = _repositorio_de_teste()
    destino = _pasta_temporaria() / "pacote"
    resumo = empacotar.montar(raiz, destino)
    assert resumo["arquivos"] == 4
    with zipfile.ZipFile(str(destino) + ".zip") as z:
        assert sorted(z.namelist()) == ["TCC-main/LEIAME.md", "TCC-main/bin.dat", "TCC-main/instalador/novo.py", "TCC-main/install.sh"]
        assert z.read("TCC-main/install.sh") == b"#!/usr/bin/env bash\necho oi\n"
        assert z.read("TCC-main/LEIAME.md") == b"linha alterada\n"
        assert z.read("TCC-main/instalador/novo.py") == b"x = 1\n"
        assert z.read("TCC-main/bin.dat") == b"\x00\x01\r\n\x02"
        assert (z.getinfo("TCC-main/install.sh").external_attr >> 16) & 0o777 == 0o644   # sem permissão de execução, como no git
    with tarfile.open(str(destino) + ".tar.gz") as t:
        membro = t.getmember("TCC-main/install.sh")
        assert membro.mode == 0o644 and membro.mtime == 0 and membro.uname == "" and membro.uid == 0
        assert t.extractfile(membro).read() == b"#!/usr/bin/env bash\necho oi\n"


def teste_empacotar_duas_vezes_da_o_mesmo_arquivo():
    raiz = _repositorio_de_teste()
    um = empacotar.montar(raiz, _pasta_temporaria() / "a")
    dois = empacotar.montar(raiz, _pasta_temporaria() / "b")
    assert um == dois, (um, dois)
    assert len(um["zip_sha256"]) == 64 and len(um["tar_sha256"]) == 64


def teste_celula_wsl_ps1_tem_bom_tag_e_nao_tem_travessao():
    caminho = RAIZ / "ferramentas" / "instalador_matriz" / "celula_wsl.ps1"
    bruto = caminho.read_bytes()
    assert bruto[:3] == b"\xef\xbb\xbf", "o .ps1 precisa de UTF-8 com BOM (Windows PowerShell 5.1)"
    texto = bruto.decode("utf-8-sig")
    assert "—" not in texto and "→" not in texto
    assert "! Alteração de IA - Revisar:" in texto and "! Motivo:" in texto
    # ! Alteração de IA - Revisar: (pacote I2) o texto conferido passa de `timeout 7200` para `timeout -s INT 7200`, e o teste
    # recusa a forma antiga.
    # ! Motivo: o `timeout` sem `-s` manda SIGTERM, que mata o Python da prova sem passar pelo `finally` do `main` de
    # `instalador/conferir.py`; numa prova que travasse por duas horas a célula ficava sem `registro.json`. Com `-s INT` o
    # Python recebe a interrupção do teclado, o `finally` grava o registro e desliga os serviços.
    for pedaco in ("[switch]$Simular", "wsl --import", "wsl --unregister", "executar_fase", "celula.json", "instalador.conferir",
                   "rodar_fase", "timeout -s INT 7200"):
        assert pedaco in texto, pedaco
    assert "timeout 7200" not in texto, "a prova precisa ser interrompida com -s INT, para o registro.json sair"


# ! Alteração de IA - Revisar: (pacote I2) testes das sondas das suspeitas (`sondas_suspeitas.sh`), da parte `suspeitas` do
# roteiro embutido no `celula_wsl.ps1` e do leitor da evidência (`ler_celula.py`).
# ! Motivo: o `install.py` para no primeiro erro (no Ubuntu, o root do MariaDB), e a célula `como-esta` só mostraria essa falha;
# as outras suspeitas (venv, extensões do PHP, bibliotecas do Chromium, Ollama) ficariam escondidas e cada uma custaria uma
# rodada a mais na janela do Eric. As sondas testam cada suspeita em separado, depois do instalador e da prova, e o leitor
# resume a pasta de evidência para a sessão não ler os logs inteiros. Os dois precisam de teste sem WSL: a sintaxe do shell
# é conferida pelo `bash -n` do Git, e o leitor, sobre uma pasta de evidência de mentira.
def _bash_para_sintaxe() -> str | None:
    """O bash que confere a sintaxe. No Windows só o do Git: o `bash.exe` de System32 é o lançador do WSL."""
    if sys.platform == "win32":
        for candidato in (r"C:\Program Files\Git\bin\bash.exe", r"C:\Program Files\Git\usr\bin\bash.exe"):
            if Path(candidato).exists():
                return candidato
        return None
    return shutil.which("bash")


def _conferir_sintaxe_do_shell(texto: str) -> None:
    bash = _bash_para_sintaxe()
    if not bash:
        return
    arquivo = _pasta_temporaria() / "roteiro.sh"
    arquivo.write_bytes(texto.replace("\r\n", "\n").encode("utf-8"))
    r = subprocess.run([bash, "-n", str(arquivo)], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    assert r.returncode == 0, r.stderr


def teste_sondas_das_suspeitas_cobrem_hl1_a_hl11():
    import re
    texto = (RAIZ / "ferramentas" / "instalador_matriz" / "sondas_suspeitas.sh").read_text(encoding="utf-8")
    assert "! Alteração de IA - Revisar:" in texto and "! Motivo:" in texto
    assert "—" not in texto and "→" not in texto
    cobertas = set(re.findall(r"^\s*(?:sonda|nota) (HL\d+) ", texto, re.MULTILINE))
    assert cobertas == {f"HL{n}" for n in range(1, 12)}, sorted(cobertas)
    # o install.sh do clone do Windows só é lido (od), nunca executado: ele chamaria o install.py do repositório real
    assert "/mnt/c" not in texto, "o caminho do clone do Windows vem por argumento, não fixo no roteiro"
    for linha in texto.splitlines():
        if "CLONE_SH" in linha and not linha.lstrip().startswith("#"):
            assert linha.startswith("REPO=") or "od -c" in linha or linha.lstrip().startswith("if ["), linha
    _conferir_sintaxe_do_shell(texto)


def teste_celula_sh_embutido_chama_as_sondas_e_passa_no_bash_n():
    texto = (RAIZ / "ferramentas" / "instalador_matriz" / "celula_wsl.ps1").read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
    roteiro = texto.split("@'\n", 1)[1].split("\n'@", 1)[0]
    assert roteiro.startswith("#!/usr/bin/env bash")
    for pedaco in ("suspeitas)", "ferramentas/instalador_matriz/sondas_suspeitas.sh", "saida_sondas.txt"):
        assert pedaco in roteiro, pedaco
    assert '"suspeitas"' in texto and "[switch]$SemSondas" in texto
    # ! Alteração de IA - Revisar: (pacote I2, tarefa 5) o teste passa a exigir as duas variáveis que o roteiro exporta antes do
    # `./install.sh`, a procura das sondas ao lado do `celula.sh` e a gravação das sondas na pasta de evidência.
    # ! Motivo: célula L-U2404 de 18/11/2026: sem terminal o instalador novo não pergunta se troca o root do MariaDB e para; e sem
    # `COBAIA_MODELO_LLM` ele baixa o `qwen2.5:7b` (4,7 GB) mesmo numa célula que só vai até o N3. As rodadas `como-esta` das outras
    # distribuições usam o pacote guardado de 18/11, que traz as sondas daquele dia; a cópia na evidência faz valer a sonda nova.
    for pedaco in ("export COBAIA_ROOT_SEM_SENHA=1", 'export COBAIA_MODELO_LLM="$MODELO"', '$(dirname "$0")/sondas_suspeitas.sh'):
        assert pedaco in roteiro, pedaco
    assert any("sondas_suspeitas.sh" in linha and "WriteAllText" in linha for linha in texto.splitlines()), \
        "o .ps1 precisa gravar sondas_suspeitas.sh na pasta de evidência (linha com WriteAllText)"
    _conferir_sintaxe_do_shell(roteiro)


def _evidencia_de_mentira() -> Path:
    pasta = _pasta_temporaria() / "celulas" / "L-TESTE" / "20261118-120000"
    (pasta / "suspeitas").mkdir(parents=True)
    celula = {"id": "L-TESTE", "modo": "como-esta", "ate": "N3", "imagem": "x.wsl", "inicio": "2026-11-18T12:00:00",
              "fim": "2026-11-18T12:10:30", "saidas": {"install_direto": "126", "install_bash": "1", "conferir": "1"}}
    (pasta / "celula.json").write_text(json.dumps(celula), encoding="utf-8")
    reg = registro.novo("L-TESTE", {"nome": "Ubuntu 24.04.5 LTS", "familia": "apt", "suporte": "suportado"}, {"python": "3.12.3"})
    registro.anotar_nivel(reg, "N1", "falhou", "o MariaDB não respondeu (ensure_mariadb_running)", 76.2)
    registro.anotar_versoes(reg, {"php": "8.3.6"}, {"php": {"testada": "8.2.35", "aceita_de": "8.1", "aceita_ate": "8.5"}})
    # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) o registro de mentira ganha a chave `instalacao` e a pasta ganha um `restaurar_banco.log`.
    # ! Motivo: o leitor da evidência passa a mostrar os tempos dos passos da instalação (que o `conferir.py` copia do `passos.json`) e o log da restauração do banco da célula ALVO; o teste precisa de uma pasta que tenha os dois.
    reg["instalacao"] = {"resultado": "concluida", "passos": [{"passo": "pacotes do sistema", "segundos": 12.5}]}
    registro.gravar(reg, pasta)
    (pasta / "restaurar_banco.log").write_text("banco restaurado ao seed\n", encoding="utf-8")
    (pasta / "os-release.txt").write_text('PRETTY_NAME="Ubuntu 24.04.5 LTS"\nID=ubuntu\n', encoding="utf-8")
    (pasta / "systemd.txt").write_text("running\n", encoding="utf-8")
    (pasta / "instalacao_direto.log").write_text("timeout: failed to run command './install.sh': Permission denied\n", encoding="utf-8")
    linhas = [f"linha {i}" for i in range(100)] + ["[cobaia] Não foi possível subir o MariaDB."]
    (pasta / "instalacao.log").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    (pasta / "suspeitas" / "HL2.txt").write_text(
        "### criar a venv como o install.py faz\n$ python3 -m venv x\nensurepip is not available\n[codigo de saida: 1]\n\n"
        "### criar a venv depois do contorno\n$ python3 -m venv x\n[codigo de saida: 0]\n\n", encoding="utf-8")
    (pasta / "suspeitas" / "HL10.txt").write_text("### root sem senha\n$ mariadb -u root\nERROR 1698 (28000): Access denied\n"
                                                  "[codigo de saida: 1]\n\n", encoding="utf-8")
    return pasta


def teste_ler_celula_resume_a_evidencia():
    sys.path.insert(0, str(RAIZ / "ferramentas" / "instalador_matriz"))
    import ler_celula
    pasta = _evidencia_de_mentira()
    resumo = ler_celula.resumir(pasta, linhas_do_log=5)
    assert resumo["celula"]["id"] == "L-TESTE" and resumo["celula"]["modo"] == "como-esta"
    assert resumo["duracao_s"] == 630, resumo["duracao_s"]
    assert resumo["saidas"] == {"install_direto": "126", "install_bash": "1", "conferir": "1"}
    assert resumo["niveis"]["N1"]["estado"] == "falhou" and resumo["alcancado"] == "N0"
    assert resumo["versoes"]["php"]["estado"] == "na_faixa"
    assert resumo["ambiente"]["os-release"] == "Ubuntu 24.04.5 LTS" and resumo["ambiente"]["systemd"] == "running"
    assert resumo["logs"]["instalacao_direto.log"] == ["timeout: failed to run command './install.sh': Permission denied"]
    assert len(resumo["logs"]["instalacao.log"]) == 5 and resumo["logs"]["instalacao.log"][-1].endswith("subir o MariaDB.")
    # as suspeitas saem na ordem do número, com o código de saída de cada sonda
    assert list(resumo["suspeitas"]) == ["HL2", "HL10"], list(resumo["suspeitas"])
    assert resumo["suspeitas"]["HL2"]["codigos"] == [1, 0] and resumo["suspeitas"]["HL10"]["codigos"] == [1]
    texto = ler_celula.em_texto(resumo)
    for pedaco in ("L-TESTE", "Permission denied", "N1: falhou", "HL2", "ensurepip is not available", "ERROR 1698", "subir o MariaDB"):
        assert pedaco in texto, pedaco
    # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) o teste também exige a linha dos tempos dos passos e o `restaurar_banco.log`.
    # ! Motivo: a seção 3.3 do plano pede o tempo de cada passo no registro; sem o leitor mostrá-lo, o número ficaria só no JSON.
    assert "Instalação (concluida): pacotes do sistema 12.5 s" in texto, texto
    assert "banco restaurado ao seed" in texto and "restaurar_banco.log" in texto


def teste_ler_celula_acha_a_rodada_mais_recente_e_corta_sonda_longa():
    sys.path.insert(0, str(RAIZ / "ferramentas" / "instalador_matriz"))
    import ler_celula
    pasta = _evidencia_de_mentira()
    celulas = pasta.parent.parent
    (celulas / "L-TESTE" / "20261117-090000").mkdir()
    assert ler_celula.pasta_mais_recente(celulas, "L-TESTE") == pasta
    try:
        ler_celula.pasta_mais_recente(celulas, "L-NAO-EXISTE")
        raise AssertionError("célula sem rodada tinha de levantar FileNotFoundError")
    except FileNotFoundError:
        pass
    (pasta / "suspeitas" / "HL6.txt").write_text("### baixar\n$ playwright install\n" + "\n".join(f"progresso {i}" for i in range(400))
                                                 + "\nBEWARE: faltam bibliotecas\n[codigo de saida: 0]\n\n", encoding="utf-8")
    resumo = ler_celula.resumir(pasta, linhas_da_sonda=12)
    linhas = resumo["suspeitas"]["HL6"]["linhas"]
    assert len(linhas) <= 14 and linhas[0] == "### baixar" and "BEWARE: faltam bibliotecas" in linhas, linhas
    assert any("linhas cortadas" in linha for linha in linhas)
    # com a suspeita pedida por nome, o texto dela sai inteiro
    inteiro = ler_celula.resumir(pasta, linhas_da_sonda=12, inteiras=("HL6",))
    assert len(inteiro["suspeitas"]["HL6"]["linhas"]) > 400


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) testes novos da prova (`conferir.py`) e do roteiro da célula ALVO (`celula_alvo.ps1`).
# ! Motivo: a prova rodava `ollama pull` sempre, e na máquina das corridas o `qwen2.5:7b` medido já está no disco (a etiqueta trocada no registro de modelos faria o `pull` trocar o modelo sem ninguém pedir); o registro não levava os tempos dos passos da instalação; e a célula ALVO (prova na máquina-alvo) não existia.
def teste_conferir_so_baixa_o_modelo_que_falta():
    originais = (env.find_ollama, conferir._baixar, conferir.subprocess.run, dict(conferir._achadas))
    comandos: list = []

    def baixar(url, dados=None, espera=30):
        if url.endswith("/api/version"):
            return 200, '{"version": "0.40.16"}'
        if url.endswith("/api/tags"):
            return 200, json.dumps({"models": [{"name": "x:1", "digest": "sha256:abc"}]})
        if url.endswith("/api/generate"):
            return 200, '{"response": "pronto"}'
        raise AssertionError(url)

    def rodar(comando, *args, **kwargs):
        comandos.append(list(comando))
        return _Resultado(0)

    try:
        env.find_ollama = lambda: "ollama"
        conferir._baixar = baixar
        conferir.subprocess.run = rodar
        estado, _ = conferir._ollama_responde("x:1")
        assert estado == "passou", estado
        assert not any("pull" in c for c in comandos), comandos
        estado, _ = conferir._ollama_responde("y:2")
        assert estado == "passou", estado
        assert ["ollama", "pull", "y:2"] in comandos, comandos
        # ! Alteração de IA - Revisar: (19/11/2026, revisão do pacote I3, achado 3) terceira parte: sem conseguir ler `/api/tags`, a prova falha e não baixa nada.
        # ! Motivo: uma falha passageira na leitura da lista de modelos levava ao `ollama pull`, inclusive do `qwen2.5:7b` na máquina das medidas.
        comandos.clear()

        def baixar_sem_tags(url, dados=None, espera=30):
            if url.endswith("/api/tags"):
                raise OSError("x")
            return baixar(url, dados, espera)

        conferir._baixar = baixar_sem_tags
        estado, detalhe = conferir._ollama_responde("x:1")
        assert estado == "falhou" and "/api/tags" in detalhe, (estado, detalhe)
        assert not any("pull" in c for c in comandos), comandos
    finally:
        env.find_ollama, conferir._baixar, conferir.subprocess.run = originais[:3]
        conferir._achadas.clear()
        conferir._achadas.update(originais[3])


# ! Alteração de IA - Revisar: (19/11/2026, revisão do pacote I3, achado 1) teste novo: a sonda N1 recusa serviço que já estava no ar e processo que saiu logo depois de subir.
# ! Motivo: `run.start_services` não confere se as portas estão livres; com um run.cmd ou um Cobaia.exe aberto, o `php -S` e o `uvicorn` novos saíam por porta ocupada e a prova passava olhando o site e a API antigos.
def teste_conferir_n1_recusa_servico_que_ja_estava_no_ar():
    import restaurar_banco
    chamadas: list = []
    site, api = _Processo(poll=None), _Processo(poll=None)

    def baixar(url, dados=None, espera=30):
        if url.endswith("/api/produtos"):
            return 200, json.dumps([{"nome": f"Produto {i}"} for i in range(14)])
        if url.endswith("/produtos_geral.php"):
            return 200, "<html>Produto 3</html>"
        raise AssertionError(url)

    def start_services():
        chamadas.append(1)
        return site, api

    original = _trocar([(env, "find_mysql_cli", lambda: "cli"), (env, "ensure_mariadb_running", lambda cli: True),
                        (restaurar_banco, "contar", lambda cli: dict(restaurar_banco.CONTAGENS_DO_SEED)),
                        (run, "wait_until_ready", lambda *a, **k: True), (run, "start_services", start_services),
                        (run, "_port_responds", lambda porta: porta == 8080), (conferir, "_baixar", baixar)])
    servicos = conferir._servicos[:]
    try:
        estado, detalhe = conferir.sonda_n1()
        assert estado == "falhou" and "8080" in detalhe and "Cobaia.exe" in detalhe, (estado, detalhe)
        assert chamadas == [], "a sonda não podia subir os serviços com a 8080 ocupada"
        run._port_responds = lambda porta: False
        site._poll = 1
        estado, detalhe = conferir.sonda_n1()
        assert estado == "falhou" and "site" in detalhe, (estado, detalhe)
        site._poll = None
        estado, detalhe = conferir.sonda_n1()
        assert estado == "passou" and "14 produtos" in detalhe, (estado, detalhe)
    finally:
        _destrocar(original)
        conferir._servicos[:] = servicos


def teste_conferir_le_os_passos_da_instalacao():
    original = install._PASSOS[:]
    try:
        install._PASSOS[:] = [{"passo": "pacotes do sistema", "segundos": 12.5}]
        pasta = _pasta_temporaria()
        arquivo = install.gravar_passos("concluida", pasta=pasta)
        dados = conferir.ler_passos_da_instalacao(arquivo)
        assert dados["resultado"] == "concluida" and dados["passos"] == [{"passo": "pacotes do sistema", "segundos": 12.5}], dados
        assert "tag_ia" not in dados
        assert conferir.ler_passos_da_instalacao(pasta / "nao_existe.json") == {}
        estragado = pasta / "estragado.json"
        estragado.write_text("isto não é JSON", encoding="utf-8")
        assert conferir.ler_passos_da_instalacao(estragado) == {}
    finally:
        install._PASSOS[:] = original


def teste_celula_alvo_ps1_tem_bom_tag_e_nao_instala_nada():
    caminho = RAIZ / "ferramentas" / "instalador_matriz" / "celula_alvo.ps1"
    bruto = caminho.read_bytes()
    assert bruto[:3] == b"\xef\xbb\xbf", "o .ps1 precisa de UTF-8 com BOM (Windows PowerShell 5.1)"
    texto = bruto.decode("utf-8-sig")
    assert "—" not in texto and "→" not in texto
    assert "! Alteração de IA - Revisar:" in texto and "! Motivo:" in texto
    for pedaco in ("[switch]$Simular", "restaurar_banco.py", "instalador.conferir", "celula.json", "executar_fase", "rodar_fase",
                   "CLAUDECODE", "qwen2.5:0.5b-instruct", "Get-NetTCPConnection"):
        assert pedaco in texto, pedaco
    for linha in texto.splitlines():
        if not linha.lstrip().startswith("#"):
            for proibido in ("install.py", "winget", "wsl "):
                assert proibido not in linha, (proibido, linha)


# ! Alteração de IA - Revisar: teste do `build_exe.ps1`: ele só diz "Cobaia.exe atualizado" depois de conferir o código de saída do PyInstaller e a data do arquivo, e roda o PyInstaller de dentro da pasta do projeto.
# ! Motivo: em 19/11/2026 o roteiro rodou 4 segundos na janela do Eric, não gravou o `Cobaia.spec` nem o `Cobaia.exe` (que ficou com a data de 07/11/2026) e terminou em "Cobaia.exe atualizado";
# chamado de uma janela aberta em C:/Windows/System32, o PyInstaller para em "Do not run pyinstaller from" antes de gravar qualquer arquivo (reproduzido no mesmo dia).
def teste_build_exe_ps1_confere_o_resultado_e_entra_na_pasta_do_projeto():
    bruto = (RAIZ / "build_exe.ps1").read_bytes()
    assert bruto[:3] == b"\xef\xbb\xbf", "o .ps1 precisa de UTF-8 com BOM (Windows PowerShell 5.1)"
    texto = bruto.decode("utf-8-sig")
    assert "—" not in texto and "→" not in texto
    assert "! Alteração de IA - Revisar:" in texto and "! Motivo:" in texto
    codigo = "\n".join(linha for linha in texto.splitlines() if not linha.lstrip().startswith("#"))
    for pedaco in ("[string]$Saida = $PSScriptRoot", "Push-Location $PSScriptRoot", "Pop-Location", "$LASTEXITCODE", "LastWriteTime",
                   "exit 1", "cmd /c", "2>&1", "--distpath", "--specpath", "Cobaia.py"):
        assert pedaco in codigo, pedaco
    assert codigo.index("exit 1") < codigo.index("Cobaia.exe atualizado"), "a mensagem de sucesso só sai depois da conferência"
    assert codigo.count("Cobaia.exe atualizado") == 1


# ! Alteração de IA - Revisar: testes do pacote I2 (instalador/servicos.py, instalador/ferramentas.py, instalador/nucleo.py), sem rede,
# sem banco e sem tocar fora de pasta temporária; os testes que trocam atributo de módulo devolvem o original num `finally`.
# ! Motivo: na célula L-U2404 de 18/11/2026 o `php -S` subiu com `mysqli: NAO carregada` (`Class "mysqli" not found`), o instalador
# parou em "Não foi possível subir o MariaDB" com o serviço no ar (`ERROR 1698 (28000): Access denied for user 'root'@'localhost'`)
# e faltaram `python3-venv`, `php-mbstring` e as bibliotecas do Chromium; cada conserto precisa de teste antes do código.
# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) `teste_servicos_opcoes_do_php_por_sistema` vira `teste_env_php_extension_flags_por_sistema`, que chama a função de `_env_common.py` (parâmetro `so=`).
# ! Motivo: as opções do PHP por sistema passaram de `instalador/servicos.py` para `_env_common.php_extension_flags`; no Linux só o `output_buffering` (célula L-U2404, `Class "mysqli" not found` com `extension_dir=/usr/bin/ext`), e no Windows e no macOS a lista de sempre.
def teste_env_php_extension_flags_por_sistema():
    assert env.php_extension_flags("/usr/bin/php", "Linux") == ["-d", "output_buffering=4096"]
    for so in ("Windows", "Darwin"):
        opcoes = env.php_extension_flags("/usr/bin/php", so)
        assert "extension=mysqli" in opcoes, so
        assert "extension=mbstring" in opcoes, so
        assert any(item.startswith("extension_dir=") for item in opcoes), so


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) `teste_conferir_n1_ajusta_o_run_antes_de_subir` vira `teste_conferir_n1_nao_troca_as_opcoes_na_memoria`: o N1 não troca mais nada no `run.py` antes de subir os serviços.
# ! Motivo: `run.start_services` agora recebe as opções do PHP certas para o sistema direto de `_env_common.php_extension_flags`; a troca na memória (`servicos.ajustar_run`) deixou de existir junto com `instalador/servicos.py`.
def teste_conferir_n1_nao_troca_as_opcoes_na_memoria():
    assert "ajustar_run" not in inspect.getsource(conferir.sonda_n1)
    assert not hasattr(conferir, "servicos")


# ! Alteração de IA - Revisar: testes de `instalador/ferramentas.py` (Tarefa 2 do pacote I2), todos sem rede, sem `apt`, sem MariaDB e sem Ollama.
# ! Motivo: HL2, HL5, HL6, HL10 a HL13 da célula L-U2404 (`ensurepip is not available`, `ERROR 1698 (28000)`, `libnspr4.so`,
# `mb_strimwidth()` indefinida, pacote `php` trazendo o Apache): cada decisão do módulo é função pura ou recebe o que troca por parâmetro.
class _Resultado:
    def __init__(self, returncode: int = 0, stdout: str = ""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = ""


def teste_ferramentas_pacotes_desejados():
    from instalador import ferramentas
    com = ferramentas.pacotes_desejados("apt", True)
    for pacote in ("python3-venv", "php-cli", "php-mysql", "php-mbstring", "mariadb-server", "curl", "zstd"):
        assert pacote in com, pacote
    assert "php" not in com
    assert "python3-venv" not in ferramentas.pacotes_desejados("apt", False)


def teste_ferramentas_pacotes_que_faltam_e_comando_apt():
    from instalador import ferramentas
    assert ferramentas.pacotes_que_faltam(["a", "b", "c"], lambda p: p == "b") == ["a", "c"]
    # ! Alteração de IA - Revisar: o comando esperado ganha `--no-remove` antes dos pacotes (consertos do I2, C2).
    # ! Motivo: numa máquina com o `mysql-server`, `apt-get install -y mariadb-server` resolvia o conflito removendo o MySQL sem perguntar.
    assert ferramentas.comando_apt(["a", "b"], ["sudo"]) == ["sudo", "env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "install", "-y",
                                                              "--no-remove", "a", "b"]
    assert ferramentas.comando_apt(["a"], [])[0] == "env"


# ! Alteração de IA - Revisar: testes novos dos consertos da revisão do I2 (C2, C3, C5): o `apt` sem remover pacotes, a `.venv` que existe sem `python` e `pip`, e a versão que o script do Ollama instalou.
# ! Motivo: a revisão do pacote I2 achou que o `apt-get install -y mariadb-server` removia o `mysql-server` sem perguntar, que uma `.venv` vinda do Windows (ou de uma instalação que parou no `ensurepip is not available`) derrubava o instalador com `FileNotFoundError`, e que o instalador não conferia a versão do Ollama depois do script oficial.
def teste_ferramentas_instalar_pacotes_nao_remove_e_explica():
    from instalador import ferramentas
    original = (ferramentas.pacotes_que_faltam, ferramentas.como_root, env.run)
    comandos: list = []
    codigos = {"update": 100, "install": 100}

    def gravar(comando, **kw):
        comandos.append(comando)
        return _Resultado(codigos["update" if "update" in comando else "install"])

    try:
        ferramentas.pacotes_que_faltam = lambda pacotes, *a, **k: ["mariadb-server"]
        ferramentas.como_root = lambda *a, **k: ["sudo"]
        env.run = gravar
        try:
            ferramentas.instalar_pacotes_do_sistema({"familia": "apt"})
            raise AssertionError("o install com código 100 tinha de levantar Falha")
        except ferramentas.Falha as e:
            assert "mysql-server" in str(e), str(e)
        assert "--no-remove" in comandos[1], comandos
        comandos.clear()
        codigos["install"] = 0
        assert ferramentas.instalar_pacotes_do_sistema({"familia": "apt"}) == ["mariadb-server"]
    finally:
        ferramentas.pacotes_que_faltam, ferramentas.como_root, env.run = original


def teste_ferramentas_conferir_pasta_da_venv():
    from instalador import ferramentas
    base = _pasta_temporaria()
    ferramentas.conferir_pasta_da_venv(base / "nao-existe")
    vazia = base / "vazia"
    vazia.mkdir()
    try:
        ferramentas.conferir_pasta_da_venv(vazia)
        raise AssertionError("pasta sem python e pip tinha de levantar Falha")
    except ferramentas.Falha as e:
        assert "Apague" in str(e), str(e)
    completa = base / "completa"
    python_venv = ferramentas.python_da_venv(completa)
    pip = python_venv.with_name("pip.exe" if env.OS_NAME == "Windows" else "pip")
    for arquivo in (python_venv, pip):
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_text("x", encoding="utf-8")
    ferramentas.conferir_pasta_da_venv(completa)


def teste_ferramentas_como_root():
    from instalador import ferramentas
    assert ferramentas.como_root(uid=0, tem_sudo=False) == []
    assert ferramentas.como_root(uid=1000, tem_sudo=True) == ["sudo"]
    try:
        ferramentas.como_root(uid=1000, tem_sudo=False)
        raise AssertionError("sem sudo e sem root tinha de levantar Falha")
    except ferramentas.Falha as e:
        assert "sudo" in str(e)


def teste_ferramentas_ler_extensoes():
    from instalador import ferramentas
    assert ferramentas.ler_extensoes("PHP Warning: x\nmysqli=1\npdo_mysql=1\nmbstring=0\n") == {"mysqli": True, "pdo_mysql": True, "mbstring": False}
    assert ferramentas.ler_extensoes("") == {"mysqli": False, "pdo_mysql": False, "mbstring": False}


def teste_ferramentas_confirmar_root_sem_senha():
    from instalador import ferramentas

    def nao_perguntar(_texto):
        raise AssertionError("não devia perguntar")

    assert ferramentas.confirmar_root_sem_senha({"COBAIA_ROOT_SEM_SENHA": "1"}, True, nao_perguntar) is True
    assert ferramentas.confirmar_root_sem_senha({"COBAIA_ROOT_SEM_SENHA": "0"}, True, nao_perguntar) is False
    assert ferramentas.confirmar_root_sem_senha({}, False, nao_perguntar) is False
    assert ferramentas.confirmar_root_sem_senha({}, True, lambda _t: " S ") is True
    assert ferramentas.confirmar_root_sem_senha({}, True, lambda _t: "") is False


def teste_ferramentas_garantir_root_sem_senha():
    from instalador import ferramentas
    original_conectar, original_conserto = env._can_connect, env.ensure_root_no_password
    chamadas: list[str] = []
    try:
        env.ensure_root_no_password = lambda cli: chamadas.append(cli) or True
        env._can_connect = lambda cli: True
        ferramentas.garantir_root_sem_senha("mariadb", {}, False)
        assert chamadas == []
        env._can_connect = lambda cli: False
        try:
            ferramentas.garantir_root_sem_senha("mariadb", {"COBAIA_ROOT_SEM_SENHA": "0"}, False)
            raise AssertionError("recusa tinha de levantar Falha")
        except ferramentas.Falha as e:
            assert "COBAIA_ROOT_SEM_SENHA=1" in str(e)
        assert chamadas == []
        ferramentas.garantir_root_sem_senha("mariadb", {"COBAIA_ROOT_SEM_SENHA": "1"}, False)
        assert chamadas == ["mariadb"]
        env.ensure_root_no_password = lambda cli: False
        try:
            ferramentas.garantir_root_sem_senha("mariadb", {"COBAIA_ROOT_SEM_SENHA": "1"}, False)
            raise AssertionError("conserto que falha tinha de levantar Falha")
        except ferramentas.Falha:
            pass
    finally:
        env._can_connect, env.ensure_root_no_password = original_conectar, original_conserto


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) `teste_ferramentas_banco_no_ar` vira `teste_env_banco_no_ar`: o mesmo roteiro, chamando `env.banco_no_ar` e trocando `env.subprocess.run`.
# ! Motivo: `banco_no_ar` passou de `instalador/ferramentas.py` para `_env_common.py` (suspeita HL12: entrar como root sem senha não prova que o banco está desligado; no Ubuntu `ERROR 1698 (28000): Access denied for user 'root'@'localhost'` com o serviço no ar).
def teste_env_banco_no_ar():
    original = (env._can_connect, env.find_mariadb_admin, env.subprocess.run)
    comandos: list = []
    try:
        env.subprocess.run = lambda comando, **kw: comandos.append(comando) or _Resultado(0)
        env._can_connect = lambda cli: True
        assert env.banco_no_ar("mariadb") is True
        assert comandos == []
        env._can_connect = lambda cli: False
        env.find_mariadb_admin = lambda: None
        assert env.banco_no_ar("mariadb") is False
        env.find_mariadb_admin = lambda: "/usr/bin/mariadb-admin"
        assert env.banco_no_ar("mariadb") is True
        assert comandos == [["/usr/bin/mariadb-admin", "ping"]]
        env.subprocess.run = lambda comando, **kw: _Resultado(1)
        assert env.banco_no_ar("mariadb") is False
    finally:
        env._can_connect, env.find_mariadb_admin, env.subprocess.run = original


# ! Alteração de IA - Revisar: (19/11/2026, I2b, B2; pacote I3) testes do serviço do banco: o comando de subir (com e sem systemd), o prefixo de root, `ensure_mariadb_running` no Linux ligando o serviço, e `ferramentas.subir_banco` virando `Falha`.
# ! Motivo: célula L-U2404-SS de 19/11/2026 (HL7): com o systemd desligado, `sudo systemctl enable --now mariadb` responde "System has not been booted with systemd as init system (PID 1). Can't operate."; o servidor direto como usuário comum dá `Can't create/write to file './ddl_recovery.log' (Errcode: 13 "Permission denied")`; `sudo service mariadb start` sobe. No pacote I3 o conserto passou para `_env_common.py`, que o `run.py` e o `restaurar_banco.py` também chamam.
def teste_env_comando_de_subir_o_banco():
    assert env.comando_de_subir_o_banco(True, ["sudo"]) == ["sudo", "systemctl", "enable", "--now", "mariadb"]
    assert env.comando_de_subir_o_banco(False, ["sudo"]) == ["sudo", "service", "mariadb", "start"]


def teste_env_prefixo_de_root():
    assert env.prefixo_de_root(uid=0, tem_sudo=False) == []
    assert env.prefixo_de_root(uid=1000, tem_sudo=True) == ["sudo"]
    assert env.prefixo_de_root(uid=1000, tem_sudo=False) is None


def teste_env_ensure_mariadb_running_no_linux_liga_o_servico():
    comandos: list = []
    mensagens: list = []
    respostas = iter([False, True])
    original = _trocar([(env, "OS_NAME", "Linux"), (env, "_can_connect", lambda cli: False),
                        (env, "banco_no_ar", lambda cli: next(respostas)),
                        (env, "prefixo_de_root", lambda *a, **k: ["sudo"]),
                        (env, "systemd_no_ar", lambda: False),
                        (env, "run", lambda comando, **kw: comandos.append(comando) or _Resultado(0)),
                        (env.subprocess, "Popen", lambda *a, **k: (_ for _ in ()).throw(
                            AssertionError("no Linux o servidor não sobe como processo direto"))),
                        (env, "log", mensagens.append)])
    try:
        env.systemd_no_ar = lambda: False
        assert env.ensure_mariadb_running("mariadb") is True
        assert comandos == [["sudo", "service", "mariadb", "start"]], comandos
        comandos.clear()
        respostas = iter([False, True])
        env.systemd_no_ar = lambda: True
        assert env.ensure_mariadb_running("mariadb") is True
        assert comandos == [["sudo", "systemctl", "enable", "--now", "mariadb"]], comandos
        # O serviço não responde: devolve False, com o comando rodado uma vez e a mensagem dizendo qual foi.
        comandos.clear()
        mensagens.clear()
        env.systemd_no_ar = lambda: False
        env.banco_no_ar = lambda cli: False
        assert env.subir_servico_no_linux("mariadb", espera_s=0) is False
        assert comandos == [["sudo", "service", "mariadb", "start"]], comandos
        assert any("service mariadb start" in m for m in mensagens), mensagens
        # Sem sudo (e sem ser root): não roda nada e diz o que falta.
        comandos.clear()
        mensagens.clear()
        env.prefixo_de_root = lambda *a, **k: None
        assert env.subir_servico_no_linux("mariadb", espera_s=0) is False
        assert comandos == []
        assert any("sudo" in m for m in mensagens), mensagens
        # HL12: acesso recusado com o servidor no ar não é banco desligado; nenhum comando roda.
        env.prefixo_de_root = lambda *a, **k: ["sudo"]
        env.banco_no_ar = lambda cli: True
        assert env.ensure_mariadb_running("mariadb") is True
        assert comandos == []
    finally:
        _destrocar(original)


def teste_ferramentas_subir_banco_vira_falha():
    from instalador import ferramentas
    original = env.ensure_mariadb_running
    try:
        env.ensure_mariadb_running = lambda cli: False
        try:
            ferramentas.subir_banco("mariadb")
            raise AssertionError("banco que não sobe tinha de levantar Falha")
        except ferramentas.Falha:
            pass
        env.ensure_mariadb_running = lambda cli: True
        ferramentas.subir_banco("mariadb")
    finally:
        env.ensure_mariadb_running = original


def teste_ferramentas_conferir_php_usa_as_opcoes_do_env_common():
    from instalador import ferramentas
    comandos: list = []
    original = _trocar([(env, "find_php", lambda: "/usr/bin/php"),
                        (env, "php_extension_flags", lambda php, so=None: ["-d", "x=1"]),
                        (ferramentas.subprocess, "run",
                         lambda comando, **kw: comandos.append(comando) or _Resultado(0, "mysqli=1\npdo_mysql=1\nmbstring=1\n")),
                        (env, "log", lambda msg: None)])
    try:
        assert ferramentas.conferir_php() == "/usr/bin/php"
        assert comandos[0][:4] == ["/usr/bin/php", "-d", "x=1", "-r"], comandos
    finally:
        _destrocar(original)


# ! Alteração de IA - Revisar: (19/11/2026, I2b, B3) testes novos do `dnf`: consulta de pacote instalado, comando de instalar, pacotes desejados, instalação sem `apt-get` e Chromium sem bibliotecas como aviso no melhor esforço.
# ! Motivo: célula L-F45 de 19/11/2026 (HL3): no Fedora o instalador rodava `sudo apt-get update` ("sudo: apt-get: command not found") e parava em "PHP foi instalado mas não foi encontrado automaticamente. Feche e reabra o terminal"; o Playwright avisa "your OS is not officially supported" e o Chromium não abre (`libnspr4.so: cannot open shared object file`).
def teste_ferramentas_pacote_instalado_por_familia():
    from instalador import ferramentas
    original = ferramentas.subprocess.run
    comandos: list = []
    codigo = {"valor": 0}

    def gravar(comando, **kw):
        comandos.append(comando)
        return _Resultado(codigo["valor"], "installed")

    try:
        ferramentas.subprocess.run = gravar
        assert ferramentas.pacote_instalado("php-cli", "apt") is True
        assert comandos[-1][0] == "dpkg-query", comandos
        assert ferramentas.pacote_instalado("php-cli", "dnf") is True
        # ! Alteração de IA - Revisar: (19/11/2026, revisão da segunda rodada, M-1) o `rpm` é perguntado por `--whatprovides`.
        # ! Motivo: no Fedora o `curl` pode vir do pacote `curl-minimal`, que provê `curl`; `rpm -q curl` diria que falta, e o
        # `dnf install curl` entraria em conflito com o `curl-minimal` já instalado.
        assert comandos[-1] == ["rpm", "-q", "--whatprovides", "php-cli"], comandos
        codigo["valor"] = 1
        assert ferramentas.pacote_instalado("php-cli", "apt") is False
        assert ferramentas.pacote_instalado("php-cli", "dnf") is False
    finally:
        ferramentas.subprocess.run = original


def teste_ferramentas_comando_de_instalar_por_familia():
    from instalador import ferramentas
    assert ferramentas.comando_de_instalar(["a"], ["sudo"], "apt") == ferramentas.comando_apt(["a"], ["sudo"])
    assert ferramentas.comando_de_instalar(["a", "b"], ["sudo"], "dnf") == ["sudo", "dnf", "install", "-y", "a", "b"]


def teste_ferramentas_pacotes_desejados_do_dnf():
    from instalador import ferramentas
    pacotes = ferramentas.pacotes_desejados("dnf", True)
    # ! Alteração de IA - Revisar: (19/11/2026, célula L-F45 em modo `novo`) o `gawk` entra na lista conferida.
    # ! Motivo: sem o `awk` o script oficial do Ollama para logo no começo (rodada 20261119-134801 do Fedora 45).
    for pacote in ("php-cli", "php-mysqlnd", "php-mbstring", "mariadb-server", "curl", "zstd", "gawk"):
        assert pacote in pacotes, pacote
    assert "python3-venv" not in pacotes


def teste_ferramentas_instalar_pacotes_pelo_dnf_nao_roda_apt():
    from instalador import ferramentas
    original = (ferramentas.pacotes_que_faltam, ferramentas.como_root, env.run)
    comandos: list = []
    try:
        ferramentas.pacotes_que_faltam = lambda pacotes, *a, **k: ["mariadb-server"]
        ferramentas.como_root = lambda *a, **k: ["sudo"]
        env.run = lambda comando, **kw: comandos.append(comando) or _Resultado(0)
        assert ferramentas.instalar_pacotes_do_sistema({"familia": "dnf"}) == ["mariadb-server"]
        assert comandos == [["sudo", "dnf", "install", "-y", "mariadb-server"]], comandos
        # ! Alteração de IA - Revisar: (19/11/2026, revisão da segunda rodada, M-6) o caso em que o `dnf` sai com erro.
        # ! Motivo: só o caminho de sucesso tinha teste; a mensagem de falha do `dnf` podia mudar ou sumir sem a bateria acusar.
        env.run = lambda comando, **kw: _Resultado(1)
        try:
            ferramentas.instalar_pacotes_do_sistema({"familia": "dnf"})
            raise AssertionError("o dnf saindo com erro tinha de levantar Falha")
        except ferramentas.Falha as e:
            assert "dnf" in str(e) and "mariadb-server" in str(e) and "apt" not in str(e), str(e)
    finally:
        ferramentas.pacotes_que_faltam, ferramentas.como_root, env.run = original


def teste_ferramentas_chromium_sem_bibliotecas_no_melhor_esforco_so_avisa():
    from instalador import ferramentas
    original = (env.playwright_chromium_instalado, ferramentas.binarios_do_chromium, ferramentas.subprocess.run, env.log)
    mensagens: list[str] = []
    try:
        env.playwright_chromium_instalado = lambda: True
        ferramentas.binarios_do_chromium = lambda *a, **k: [Path("x")]
        ferramentas.subprocess.run = lambda comando, **kw: _Resultado(0, "\tlibnss3.so => not found\n")
        env.log = lambda texto="": mensagens.append(texto)
        ferramentas.instalar_chromium(Path("/v/bin/python"), {"familia": "dnf", "suporte": "melhor_esforco"})
        assert any("libnss3.so" in m for m in mensagens), mensagens
        try:
            ferramentas.instalar_chromium(Path("/v/bin/python"), {"familia": "dnf", "suporte": "suportado"})
            raise AssertionError("sem o melhor esforço, a falta das bibliotecas tinha de levantar Falha")
        except ferramentas.Falha as e:
            assert "libnss3.so" in str(e), str(e)
    finally:
        env.playwright_chromium_instalado, ferramentas.binarios_do_chromium, ferramentas.subprocess.run, env.log = original


def teste_ferramentas_bibliotecas_que_faltam():
    from instalador import ferramentas
    saida = "\tlibnspr4.so => not found\n\tlibnss3.so => not found\n\tlibc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x1)\n\tlibnss3.so => not found\n"
    assert ferramentas.bibliotecas_que_faltam(saida) == ["libnspr4.so", "libnss3.so"]


def teste_ferramentas_binarios_do_chromium():
    from instalador import ferramentas
    base = _pasta_temporaria()
    arquivos = ["chromium-1248/chrome-linux64/chrome",
                "chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell",
                "ffmpeg-1013/ffmpeg-linux", "chromium-1248/chrome-linux64/LICENSE"]
    for arquivo in arquivos:
        caminho = base / arquivo
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text("x", encoding="utf-8")
    achados = ferramentas.binarios_do_chromium(base)
    assert sorted(p.name for p in achados) == ["chrome", "chrome-headless-shell"], achados


def teste_ferramentas_comando_do_chromium():
    from instalador import ferramentas
    assert ferramentas.comando_do_chromium("/v/bin/python", True) == ["/v/bin/python", "-m", "playwright", "install", "--with-deps", "chromium"]
    assert ferramentas.comando_do_chromium("/v/bin/python", False) == ["/v/bin/python", "-m", "playwright", "install", "chromium"]


def teste_ferramentas_decidir_ollama():
    from instalador import ferramentas
    registro_ollama = versoes.carregar()["ollama"]
    assert ferramentas.decidir_ollama(None, registro_ollama) == "instalar"
    assert ferramentas.decidir_ollama(registro_ollama["testada"], registro_ollama) == "usar"
    partes = registro_ollama["testada"].split(".")
    partes[-1] = str(int(partes[-1]) + 1)
    assert ferramentas.decidir_ollama(".".join(partes), registro_ollama) == "avisar"
    assert ferramentas.decidir_ollama("0.1.0", registro_ollama) == "parar"
    assert ferramentas.decidir_ollama("", registro_ollama) == "avisar"


def teste_ferramentas_preparar_ollama_instala_e_baixa_o_modelo():
    from instalador import ferramentas
    ferr = versoes.carregar()
    original = (env.find_ollama, ferramentas.instalar_ollama, ferramentas.garantir_ollama_no_ar, env.modelo_llm_ja_baixado, env.run,
                ferramentas.versao_do_ollama)
    achados = iter([None, "/usr/local/bin/ollama"])
    instalada: list[str] = []
    comandos: list = []
    try:
        # ! Alteração de IA - Revisar: `versao_do_ollama` passa a ser trocada neste teste (devolve a versão testada).
        # ! Motivo: `preparar_ollama` agora lê a versão do executável recém-instalado (conserto C5); sem a troca o teste rodaria o `ollama` de verdade.
        ferramentas.versao_do_ollama = lambda ollama: ferr["ollama"]["testada"]
        env.find_ollama = lambda: next(achados)
        ferramentas.instalar_ollama = lambda versao: instalada.append(versao)
        ferramentas.garantir_ollama_no_ar = lambda ollama: None
        env.modelo_llm_ja_baixado = lambda ollama, modelo: False
        env.run = lambda comando, **kw: comandos.append(comando) or _Resultado(0)
        ferramentas.preparar_ollama(ferr, {"COBAIA_MODELO_LLM": "qwen2.5:0.5b"})
        assert instalada == [ferr["ollama"]["testada"]]
        assert comandos == [["/usr/local/bin/ollama", "pull", "qwen2.5:0.5b"]]
        achados = iter([None, "/usr/local/bin/ollama"])
        comandos.clear()
        ferramentas.preparar_ollama(ferr, {})
        assert comandos == [["/usr/local/bin/ollama", "pull", ferr["modelo"]["nome"]]]
    finally:
        (env.find_ollama, ferramentas.instalar_ollama, ferramentas.garantir_ollama_no_ar, env.modelo_llm_ja_baixado, env.run,
         ferramentas.versao_do_ollama) = original


def teste_ferramentas_preparar_ollama_confere_a_versao_instalada():
    from instalador import ferramentas
    ferr = versoes.carregar()
    original = (env.find_ollama, ferramentas.instalar_ollama, ferramentas.garantir_ollama_no_ar, env.modelo_llm_ja_baixado, env.run,
                ferramentas.versao_do_ollama)
    achados = iter([None, "/usr/local/bin/ollama"])
    comandos: list = []
    try:
        ferramentas.versao_do_ollama = lambda ollama: "0.1.0"
        env.find_ollama = lambda: next(achados)
        ferramentas.instalar_ollama = lambda versao: None
        ferramentas.garantir_ollama_no_ar = lambda ollama: None
        env.modelo_llm_ja_baixado = lambda ollama, modelo: False
        env.run = lambda comando, **kw: comandos.append(comando) or _Resultado(0)
        try:
            ferramentas.preparar_ollama(ferr, {})
            raise AssertionError("o script instalar outra versão tinha de levantar Falha")
        except ferramentas.Falha as e:
            assert "0.1.0" in str(e), str(e)
        assert comandos == [], comandos
    finally:
        (env.find_ollama, ferramentas.instalar_ollama, ferramentas.garantir_ollama_no_ar, env.modelo_llm_ja_baixado, env.run,
         ferramentas.versao_do_ollama) = original


def teste_ferramentas_preparar_ollama_fora_da_faixa_para():
    from instalador import ferramentas
    ferr = versoes.carregar()
    original = (env.find_ollama, ferramentas.versao_do_ollama, ferramentas.instalar_ollama)
    instalada: list[str] = []
    try:
        env.find_ollama = lambda: "/usr/local/bin/ollama"
        ferramentas.versao_do_ollama = lambda ollama: "0.1.0"
        ferramentas.instalar_ollama = lambda versao: instalada.append(versao)
        try:
            ferramentas.preparar_ollama(ferr, {})
            raise AssertionError("Ollama fora da faixa tinha de levantar Falha")
        except ferramentas.Falha:
            pass
        assert instalada == []
    finally:
        env.find_ollama, ferramentas.versao_do_ollama, ferramentas.instalar_ollama = original


# ! Alteração de IA - Revisar: testes dos passos do Linux e do `main` (Tarefa 3 do pacote I2): a ordem dos passos no `apt`, a falha sem cliente do banco e as saídas de `main`.
# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) estes testes passaram do `instalador/nucleo.py` para o `install.py`: `_gravadores_do_nucleo` vira `_gravadores_do_instalador` e os `teste_nucleo_*` viram `teste_install_*`; todo teste que chama `install.main` troca `install.gravar_passos` por uma função vazia.
# ! Motivo: HL12 da célula L-U2404 de 18/11/2026: o `install.py` rodava os `.sql` antes de o serviço e o root do MariaDB estarem
# prontos e parava em "Não foi possível subir o MariaDB" com o serviço no ar; a ordem dos passos precisa de teste que a trave. No pacote I3 os passos moram no `install.py`, e sem a troca de `gravar_passos` o teste gravaria `.ferramentas/instalacao/passos.json` dentro do repositório.
def _gravadores_do_instalador(chamadas: list[str]) -> dict:
    """Troca os passos do `instalar_no_linux` por gravadores e devolve o que precisa ser desfeito."""
    from instalador import ferramentas
    alvos = [(ferramentas, "instalar_pacotes_do_sistema"), (ferramentas, "conferir_php"), (ferramentas, "subir_banco"),
             (ferramentas, "garantir_root_sem_senha"), (install, "apply_sql_files"), (install, "setup_cobaia_api"),
             (ferramentas, "conferir_pasta_da_venv"), (ferramentas, "conferir_venv"), (ferramentas, "preparar_agente"),
             (install, "find_mysql_cli")]
    originais = {(modulo, nome): getattr(modulo, nome) for modulo, nome in alvos}
    for modulo, nome in alvos[:-1]:
        setattr(modulo, nome, lambda *a, _nome=nome, **k: chamadas.append(_nome))
    install.find_mysql_cli = lambda: "mariadb"
    return originais


def _desfazer(originais: dict) -> None:
    for (modulo, nome), valor in originais.items():
        setattr(modulo, nome, valor)


def _sem_gravar_passos(*args, **kwargs):
    return None


def teste_install_caminho_por_familia():
    # ! Alteração de IA - Revisar: (19/11/2026, I2b, B3) o esperado passa a ser: `dnf` tem caminho próprio e `nao_suportado` recebe a mensagem de "sem suporte".
    # ! Motivo: célula L-F45 (HL3): o Fedora caía no `install.py`, que rodava `sudo apt-get` ("command not found"); só Windows e macOS seguem como estavam.
    assert install.caminho_para({"familia": "apt"}) == "apt"
    assert install.caminho_para({"familia": "dnf"}) == "dnf"
    assert install.caminho_para({"familia": "nao_suportado"}) == "nao_suportado"
    for familia in ("windows", "brew"):
        assert install.caminho_para({"familia": familia}) == "como_estava", familia


def teste_install_ordem_dos_passos_no_linux():
    chamadas: list[str] = []
    originais = _gravadores_do_instalador(chamadas)
    try:
        install.instalar_no_linux({"familia": "apt"}, {})
    finally:
        _desfazer(originais)
    assert chamadas == ["instalar_pacotes_do_sistema", "conferir_php", "subir_banco", "garantir_root_sem_senha",
                        "apply_sql_files", "conferir_pasta_da_venv", "setup_cobaia_api", "conferir_venv",
                        "preparar_agente"], chamadas


def teste_install_sem_cliente_do_banco_e_falha():
    from instalador import ferramentas
    chamadas: list[str] = []
    originais = _gravadores_do_instalador(chamadas)
    try:
        install.find_mysql_cli = lambda: None
        try:
            install.instalar_no_linux({"familia": "apt"}, {})
            raise AssertionError("sem cliente do banco tinha de levantar Falha")
        except ferramentas.Falha:
            pass
    finally:
        _desfazer(originais)


def teste_install_main_no_windows_roda_os_passos_do_windows():
    chamadas: list[int] = []
    original = _trocar([(sistema, "detectar", lambda: sistema.familia("Windows")),
                        (install, "instalar_no_windows_ou_mac", lambda: chamadas.append(1)),
                        (install, "log", lambda texto="": None), (install, "gravar_passos", _sem_gravar_passos)])
    try:
        assert install.main([]) == 0
        assert len(chamadas) == 1
    finally:
        _destrocar(original)


# ! Alteração de IA - Revisar: (19/11/2026, revisão do pacote I3, achado 4) teste novo: `--reproduzir` no Windows avisa que só vale na prova.
# ! Motivo: o argumento era aceito em silêncio e a instalação terminava em "Instalação concluída" sem conferir versão nenhuma.
def teste_install_main_reproduzir_no_windows_avisa():
    mensagens: list[str] = []
    original = _trocar([(sistema, "detectar", lambda: sistema.familia("Windows")),
                        (install, "instalar_no_windows_ou_mac", lambda: None),
                        (install, "log", lambda texto="": mensagens.append(texto)), (install, "gravar_passos", _sem_gravar_passos)])
    try:
        assert install.main(["--reproduzir"]) == 0
        assert any("--conferir --reproduzir" in m for m in mensagens), mensagens
        mensagens.clear()
        assert install.main([]) == 0
        assert not any("--reproduzir" in m for m in mensagens), mensagens
    finally:
        _destrocar(original)


def teste_install_main_devolve_1_quando_um_passo_falha():
    from instalador import ferramentas

    def falhar(info, ferr):
        raise ferramentas.Falha("x")

    original = _trocar([(sistema, "detectar", lambda: sistema.familia("Linux", UBUNTU_2404)),
                        (install, "instalar_no_linux", falhar), (install, "eh_root", lambda: False),
                        (install, "log", lambda texto="": None), (install, "gravar_passos", _sem_gravar_passos)])
    try:
        assert install.main([]) == 1
    finally:
        _destrocar(original)


# ! Alteração de IA - Revisar: testes novos de `install.main` (consertos do I2, C1, C4 e C7): recusa de root no `apt`, macOS sem Homebrew e `sys.exit` de dentro do `install.py`.
# ! Motivo: como root, as venvs e o navegador ficam na pasta do root e a entrada do root do MariaDB passa no teste pelo unix_socket sem ser trocada; no macOS sem Homebrew o `install.main()` morria em `FileNotFoundError` no `brew`; e o `install.py` chama `sys.exit` quando um passo dele falha, o que escapava do `main` com traceback.
UBUNTU_2404 = {"ID": "ubuntu", "VERSION_ID": "24.04", "PRETTY_NAME": "Ubuntu 24.04.5 LTS"}


def teste_install_main_recusa_root_no_apt():
    chamadas: list[int] = []
    original = _trocar([(sistema, "detectar", lambda: sistema.familia("Linux", UBUNTU_2404)),
                        (install, "instalar_no_linux", lambda info, ferr: chamadas.append(1)),
                        (install, "eh_root", lambda: True), (install, "log", lambda texto="": None),
                        (install, "gravar_passos", _sem_gravar_passos)])
    try:
        assert install.main([]) == 1
        assert chamadas == []
    finally:
        _destrocar(original)


def teste_install_main_no_mac_sem_homebrew_avisa_e_para():
    chamadas: list[int] = []
    original = _trocar([(sistema, "detectar", lambda: sistema.familia("Darwin", tem_brew=False)),
                        (install, "instalar_no_windows_ou_mac", lambda: chamadas.append(1)),
                        (install, "log", lambda texto="": None), (install, "gravar_passos", _sem_gravar_passos)])
    try:
        assert install.main([]) == 1
        assert chamadas == []
    finally:
        _destrocar(original)


def teste_install_main_devolve_1_quando_o_install_py_sai():
    def sair(info, ferr):
        raise SystemExit(1)

    original = _trocar([(sistema, "detectar", lambda: sistema.familia("Linux", UBUNTU_2404)),
                        (install, "instalar_no_linux", sair), (install, "eh_root", lambda: False),
                        (install, "log", lambda texto="": None), (install, "gravar_passos", _sem_gravar_passos)])
    try:
        assert install.main([]) == 1
    finally:
        _destrocar(original)


# ! Alteração de IA - Revisar: (19/11/2026, I2b, B3) testes novos de `install.main`: sistema sem suporte imprime a lista do que instalar e devolve 1; Fedora instala pelo mesmo caminho do `apt`.
# ! Motivo: célula L-F45 (HL3): no Fedora o instalador rodava `sudo: apt-get: command not found` e parava em "Feche e reabra o terminal"; a decisão 141 pede, para Arch e openSUSE, só a mensagem com a lista.
def teste_install_main_sem_suporte_imprime_a_lista_e_devolve_1():
    chamadas: list[str] = []
    mensagens: list[str] = []
    original = _trocar([(sistema, "detectar", lambda: sistema.familia("Linux", {"ID": "arch", "PRETTY_NAME": "Arch Linux"})),
                        (install, "instalar_no_windows_ou_mac", lambda: chamadas.append("instalar_no_windows_ou_mac")),
                        (install, "instalar_no_linux", lambda info, ferr: chamadas.append("instalar_no_linux")),
                        (install, "log", lambda texto="": mensagens.append(texto)),
                        (install, "gravar_passos", _sem_gravar_passos)])
    try:
        assert install.main([]) == 1
    finally:
        _destrocar(original)
    assert chamadas == [], chamadas
    texto = "\n".join(mensagens)
    assert "Arch Linux" in texto and "mbstring" in texto, texto


def teste_install_main_no_fedora_instala_pelo_dnf():
    recebidas: list = []
    info_fedora = sistema.familia("Linux", {"ID": "fedora", "VERSION_ID": "45", "PRETTY_NAME": "Fedora Linux 45"})
    original = _trocar([(sistema, "detectar", lambda: info_fedora), (install, "eh_root", lambda: False),
                        (install, "instalar_no_linux", lambda info, ferr: recebidas.append(info)),
                        (install, "relatar_versoes", lambda ferr, reproduzir: []),
                        (install, "log", lambda texto="": None), (install, "gravar_passos", _sem_gravar_passos)])
    try:
        assert install.main([]) == 0
    finally:
        _destrocar(original)
    assert recebidas == [info_fedora], recebidas


def teste_install_main_conferir_chama_a_prova():
    original = conferir.main
    recebidos: list = []
    try:
        conferir.main = lambda argumentos: recebidos.extend(argumentos) or 0
        assert install.main(["--conferir", "--ate", "N2", "--reproduzir"]) == 0
    finally:
        conferir.main = original
    for pedaco in ("--ate", "N2", "--reproduzir", "--celula", "--saida"):
        assert pedaco in recebidos, (pedaco, recebidos)


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) testes novos do `install.py`: código de saída de um `sys.exit` de dentro de um passo, tempos dos passos (`cronometrar` e `gravar_passos`), `main` sem argumentos, ajuda, chamada direta do arquivo, passos do Windows sem ramo do Linux, progresso de download pequeno, conferência da `.venv` do AgenteCore e o `Cobaia.py` parando quando a instalação falha.
# ! Motivo: o ponto de entrada provisório devolvia 1 para qualquer `SystemExit`, inclusive `sys.exit(0)`, e a seção 3.3 do plano pede no registro o tempo de cada passo; célula L-F45 de 19/11/2026: ao baixar o script do Ollama o progresso mostrava `0 MB de 0 MB`; sem a conferência no `Cobaia.py`, uma instalação interrompida no Linux subiria o site e a API pela metade.
def teste_install_codigo_de_saida():
    assert install.codigo_de_saida(SystemExit()) == 0
    assert install.codigo_de_saida(SystemExit(0)) == 0
    assert install.codigo_de_saida(SystemExit(3)) == 3
    assert install.codigo_de_saida(SystemExit("texto")) == 1


def teste_install_main_sair_sem_erro_devolve_zero():
    mensagens: list[str] = []
    saida = {"erro": SystemExit(0)}

    def sair(info, ferr):
        raise saida["erro"]

    original = _trocar([(sistema, "detectar", lambda: sistema.familia("Linux", UBUNTU_2404)),
                        (install, "instalar_no_linux", sair), (install, "eh_root", lambda: False),
                        (install, "log", lambda texto="": mensagens.append(texto)),
                        (install, "gravar_passos", _sem_gravar_passos)])
    try:
        assert install.main([]) == 0
        assert not any("interrompida" in m for m in mensagens), mensagens
        mensagens.clear()
        saida["erro"] = SystemExit(3)
        assert install.main([]) == 3
        assert any("Instalação interrompida" in m for m in mensagens), mensagens
    finally:
        _destrocar(original)


def teste_install_cronometrar_anota_o_passo_mesmo_quando_ele_falha():
    guardados = install._PASSOS[:]
    try:
        install._PASSOS.clear()
        assert install.cronometrar("a", lambda x: x + 1, 1) == 2

        def quebrar():
            raise ValueError("x")

        try:
            install.cronometrar("b", quebrar)
            raise AssertionError("o erro do passo tinha de passar adiante")
        except ValueError:
            pass
        assert [p["passo"] for p in install._PASSOS] == ["a", "b"], install._PASSOS
        assert all(isinstance(p["segundos"], float) and p["segundos"] >= 0 for p in install._PASSOS), install._PASSOS
    finally:
        install._PASSOS[:] = guardados


def teste_install_gravar_passos():
    guardados = install._PASSOS[:]
    pasta = _pasta_temporaria()
    original = _trocar([(install, "log", lambda texto="": None)])
    try:
        install._PASSOS[:] = [{"passo": "PHP", "segundos": 1.5}]
        caminho = install.gravar_passos("concluida", pasta=pasta)
        assert caminho == pasta / "passos.json", caminho
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        assert dados["resultado"] == "concluida"
        assert dados["passos"] == [{"passo": "PHP", "segundos": 1.5}]
        assert dados["gravado_em"]
        assert "! Alteração de IA - Revisar:" in dados["tag_ia"]["alteracao"]
        assert "! Motivo:" in dados["tag_ia"]["motivo"]
        # Uma pasta que é um arquivo não dá para criar: devolve None, sem erro.
        arquivo = pasta / "arquivo.txt"
        arquivo.write_text("x", encoding="utf-8")
        assert install.gravar_passos("interrompida", pasta=arquivo) is None
    finally:
        install._PASSOS[:] = guardados
        _destrocar(original)


def teste_install_main_grava_os_passos_com_o_resultado():
    gravados: list = []
    estado = {"linux": None, "windows": None}

    def linux(info, ferr):
        if estado["linux"]:
            raise estado["linux"]

    def windows():
        if estado["windows"]:
            raise estado["windows"]

    from instalador import ferramentas
    original = _trocar([(sistema, "detectar", lambda: sistema.familia("Linux", UBUNTU_2404)),
                        (install, "instalar_no_linux", linux), (install, "instalar_no_windows_ou_mac", windows),
                        (install, "relatar_versoes", lambda ferr, reproduzir: []), (install, "eh_root", lambda: False),
                        (install, "log", lambda texto="": None),
                        (install, "gravar_passos", lambda resultado, pasta=None: gravados.append(resultado))])
    try:
        assert install.main([]) == 0
        assert gravados == ["concluida"], gravados
        gravados.clear()
        estado["linux"] = ferramentas.Falha("x")
        assert install.main([]) == 1
        assert gravados == ["interrompida"], gravados
        gravados.clear()
        sistema.detectar = lambda: sistema.familia("Windows")
        assert install.main([]) == 0
        assert gravados == ["concluida"], gravados
        gravados.clear()
        estado["windows"] = SystemExit(1)
        _sai_com_1(lambda: install.main([]))
        assert gravados == ["interrompida"], gravados
        gravados.clear()
        sistema.detectar = lambda: sistema.familia("Linux", {"ID": "arch", "PRETTY_NAME": "Arch Linux"})
        assert install.main([]) == 1
        assert gravados == [], gravados
    finally:
        _destrocar(original)


def teste_install_main_sem_argumentos_nao_le_a_linha_de_comando():
    gravados: list = []

    def nao_chamar(argumentos):
        raise AssertionError("o main sem argumentos não pode ler a linha de comando")

    argv_original = sys.argv
    original = _trocar([(sistema, "detectar", lambda: sistema.familia("Windows")), (conferir, "main", nao_chamar),
                        (install, "instalar_no_windows_ou_mac", lambda: None), (install, "log", lambda texto="": None),
                        (install, "gravar_passos", lambda resultado, pasta=None: gravados.append(resultado))])
    try:
        sys.argv = ["Cobaia.exe", "--conferir"]
        assert install.main() == 0
        assert gravados == ["concluida"], gravados
    finally:
        sys.argv = argv_original
        _destrocar(original)


def teste_install_ajuda_e_argumento_desconhecido():
    import io
    saida_original, erro_original = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
        for argumentos, codigo in ((["--help"], 0), (["--nao-existe"], 2)):
            try:
                install.main(argumentos)
                raise AssertionError(f"{argumentos} tinha de levantar SystemExit")
            except SystemExit as e:
                assert e.code == codigo, (argumentos, e.code)
    finally:
        sys.stdout, sys.stderr = saida_original, erro_original


def teste_install_py_direto_roda_pelo_modulo_install():
    texto = (RAIZ / "install.py").read_text(encoding="utf-8")
    depois = texto.split('if __name__ == "__main__":', 1)[1]
    assert "import install" in depois and "sys.exit(install.main(sys.argv[1:]))" in depois, depois


def teste_install_passos_do_windows_e_do_mac_sem_ramo_do_linux():
    # Só as linhas de código contam: a tag de histórico pode citar o comando que saiu.
    for funcao in (install.ensure_php, install.ensure_mariadb_installed, install.ensure_ollama):
        codigo = [linha for linha in inspect.getsource(funcao).splitlines() if not linha.lstrip().startswith("#")]
        texto = "\n".join(codigo)
        for proibido in ("apt-get", "systemctl", "curl -fsSL"):
            assert proibido not in texto, (funcao.__name__, proibido)


def teste_baixar_arquivo_pequeno_mostra_kb():
    mensagens: list = []
    destino = _pasta_temporaria() / "pequeno.sh"
    com_cabecalho = {"sim": True}

    def abrir(pedido, timeout=None):
        resposta = _RespostaHttp(1, 21000)
        if not com_cabecalho["sim"]:
            resposta.headers = {}
        return resposta

    original = _trocar([(install.urllib.request, "urlopen", abrir), (install, "log", mensagens.append)])
    try:
        assert install.baixar_arquivo("http://exemplo.invalido/pequeno.sh", destino) == 21000
        assert mensagens == ["  21 kB de 21 kB"], mensagens
        mensagens.clear()
        com_cabecalho["sim"] = False
        install.baixar_arquivo("http://exemplo.invalido/pequeno.sh", destino)
        assert mensagens == ["  21 kB"], mensagens
    finally:
        _destrocar(original)
    assert install.tamanho_legivel(1) == "1 kB"
    assert install.tamanho_legivel(1 << 20) == "1 MB"
    assert install.tamanho_legivel(25 << 20) == "25 MB"


def teste_ferramentas_preparar_agente_confere_a_pasta_da_venv():
    from instalador import ferramentas

    def pasta_de_mentira(pasta):
        raise ferramentas.Falha("pasta de mentira")

    original = _trocar([(ferramentas, "conferir_pasta_da_venv", pasta_de_mentira), (env, "run", _levanta)])
    try:
        try:
            ferramentas.preparar_agente({"familia": "apt"}, {})
            raise AssertionError("a pasta da venv com defeito tinha de levantar Falha")
        except ferramentas.Falha as e:
            assert "pasta de mentira" in str(e), str(e)
    finally:
        _destrocar(original)


def teste_cobaia_py_para_quando_a_instalacao_falha():
    import Cobaia
    original = _trocar([(install, "main", lambda *a, **k: 1), (run, "start_services", _levanta)])
    try:
        try:
            Cobaia.main()
            raise AssertionError("instalação com código 1 tinha de parar o Cobaia.main")
        except SystemExit as e:
            assert e.code == 1, e.code
    finally:
        _destrocar(original)


# ! Alteração de IA - Revisar: (pacote I2, tarefa 4) testes do `.gitattributes` e dos lançadores `install.sh` e `run.sh`: fim de linha,
# tag, sintaxe e, com o bash do Git, o comportamento deles numa pasta de projeto de mentira (Python, `curl` e `uv` de mentira no PATH).
# ! Motivo: célula L-U2404 de 18/11/2026, HL9: num clone feito no Windows o `install.sh` saía com CRLF e `./install.sh` dava
# "/usr/bin/env: 'bash\r': No such file or directory". E o lançador novo (decisão 140) escolhe o Python, baixa o `uv`, confere o
# SHA-256 e instala o Python em `.ferramentas/python`: tudo isso precisa de teste sem rede, sem instalar nada e sem rodar o
# `install.sh` de verdade (que chamaria o instalador do repositório). Aqui só rodam cópias numa pasta temporária.
def _pasta_usr_bin_do_bash(bash: str) -> str:
    """A pasta dos utilitários (tar, find, sha256sum...) do bash em uso. No Git para Windows ela fica em `usr\\bin`, ao lado ou
    acima do bash; em Linux e macOS são as pastas de sempre."""
    import os
    if sys.platform != "win32":
        return "/usr/bin" + os.pathsep + "/bin"
    pasta = Path(bash).parent
    return str(pasta if pasta.parent.name == "usr" else pasta.parent / "usr" / "bin")


def _bash_do_lancador() -> str:
    """O bash que roda os lançadores. No Windows, o `bin\\bash.exe` do Git é um lançador que acrescenta `/mingw64/bin` na frente
    do PATH (e aí acha o `curl` de verdade antes do de mentira); o `usr\\bin\\bash.exe` respeita o PATH que o teste monta."""
    bash = _bash_para_sintaxe()
    if sys.platform == "win32":
        direto = Path(_pasta_usr_bin_do_bash(bash)) / "bash.exe"
        if direto.exists():
            return str(direto)
    return bash


# ! Alteração de IA - Revisar: (consertos do I2, C8) `_sem_bash()` avisa `  pulado: sem bash` quando não há bash; os testes do lançador deixam de passar em silêncio.
# ! Motivo: sem bash, o teste do lançador voltava sem rodar nada e a bateria dizia `ok` como se tivesse provado o `install.sh`.
def _sem_bash() -> bool:
    if _bash_para_sintaxe():
        return False
    print("  pulado: sem bash")
    return True


def _gravar_roteiro(caminho: Path, texto: str) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(texto.replace("\r\n", "\n").encode("utf-8"))
    if sys.platform != "win32":
        caminho.chmod(0o755)


PYTHON_DE_MENTIRA = """#!/usr/bin/env bash
case "${1:-}" in
    -c) exit "${FALSO_PYTHON_SERVE:-0}" ;;
    --version) echo "Python 3.99.0" ;;
    *) echo "NUCLEO: $*" ;;
esac
"""

CURL_DE_MENTIRA = """#!/usr/bin/env bash
destino=""
while [ $# -gt 0 ]; do
    if [ "$1" = "-o" ]; then destino="$2"; shift; fi
    shift
done
cp "$PACOTE_DE_MENTIRA" "$destino"
"""

# ! Alteração de IA - Revisar: (consertos do I2, C8) o `uv` de mentira sai com código 3 e diz qual variável está errada quando o lançador não o chama com `UV_PYTHON_INSTALL_BIN=0`, `UV_NO_CONFIG=1` e `UV_PYTHON_INSTALL_DIR` e `UV_CACHE_DIR` dentro de `.ferramentas/`.
# ! Motivo: o princípio 8 do plano (o instalador não escreve fora de `.ferramentas`) só estava provado por leitura do `install.sh`; sem essas variáveis o `uv` de verdade põe um atalho em `~/.local/bin` e lê configuração do usuário.
UV_DE_MENTIRA = """#!/usr/bin/env bash
if [ "${UV_PYTHON_INSTALL_BIN:-}" != "0" ]; then echo "uv de mentira: UV_PYTHON_INSTALL_BIN devia ser 0" >&2; exit 3; fi
if [ "${UV_NO_CONFIG:-}" != "1" ]; then echo "uv de mentira: UV_NO_CONFIG devia ser 1" >&2; exit 3; fi
case "${UV_PYTHON_INSTALL_DIR:-}" in */.ferramentas/*) ;; *) echo "uv de mentira: UV_PYTHON_INSTALL_DIR devia estar em .ferramentas" >&2; exit 3 ;; esac
case "${UV_CACHE_DIR:-}" in */.ferramentas/*) ;; *) echo "uv de mentira: UV_CACHE_DIR devia estar em .ferramentas" >&2; exit 3 ;; esac
if [ "${1:-}" = "python" ] && [ "${2:-}" = "install" ]; then
    mkdir -p "$UV_PYTHON_INSTALL_DIR/cpython-$3-mentira/bin"
    cat > "$UV_PYTHON_INSTALL_DIR/cpython-$3-mentira/bin/python3" <<'FIM'
#!/usr/bin/env bash
case "${1:-}" in
    -c) exit 0 ;;
    --version) echo "Python 3.99.1" ;;
    *) echo "NUCLEO-UV: $*" ;;
esac
FIM
    chmod +x "$UV_PYTHON_INSTALL_DIR/cpython-$3-mentira/bin/python3"
fi
"""


def _projeto_de_mentira(com_uv: bool = False, sha_certo: bool = True) -> tuple[Path, dict]:
    """Uma pasta com cópias do `install.sh` e do `run.sh`, o `uv_fixado.txt` (com CRLF, como num clone do Windows) e uma
    `bin/` de mentira. Devolve a pasta e o ambiente com que o bash deve rodar."""
    import os
    bash = _bash_para_sintaxe()
    pasta = _pasta_temporaria()
    for nome in ("install.sh", "run.sh"):
        _gravar_roteiro(pasta / nome, (RAIZ / nome).read_bytes().decode("utf-8"))
    bin_falso = pasta / "bin"
    # ! Alteração de IA - Revisar: (consertos do I2, C8) grava também um `python` de mentira, igual ao `python3`.
    # ! Motivo: em Linux, um `python` de verdade em `/usr/bin` seria achado pelo lançador antes de o teste mostrar o que ele faz com o de mentira.
    _gravar_roteiro(bin_falso / "python3", PYTHON_DE_MENTIRA)
    _gravar_roteiro(bin_falso / "python", PYTHON_DE_MENTIRA)
    ambiente = {**os.environ, "PATH": str(bin_falso) + os.pathsep + _pasta_usr_bin_do_bash(bash),
                "COBAIA_FORCAR_UV": "0", "FALSO_PYTHON_SERVE": "0"}
    for nome in ("COBAIA_UV_ALVO", "PACOTE_DE_MENTIRA"):
        ambiente.pop(nome, None)
    sha = "0" * 64
    if com_uv:
        _gravar_roteiro(bin_falso / "curl", CURL_DE_MENTIRA)
        pacote = pasta / "uv-de-mentira.tar.gz"
        conteudo = UV_DE_MENTIRA.encode("utf-8")
        with tarfile.open(pacote, "w:gz") as tar:
            membro = tarfile.TarInfo("uv-de-mentira/uv")
            membro.size = len(conteudo)
            membro.mode = 0o755
            import io
            tar.addfile(membro, io.BytesIO(conteudo))
        sha = hashlib.sha256(pacote.read_bytes()).hexdigest() if sha_certo else "f" * 64
        ambiente["PACOTE_DE_MENTIRA"] = pacote.as_posix()
        ambiente["COBAIA_UV_ALVO"] = "LINUX_X86_64"
    fixado = (f"PYTHON_MINIMO=3.12\nPYTHON_VERSAO=3.14\nUV_VERSAO=0.0.1\n"
              f"UV_LINUX_X86_64_URL=http://exemplo.invalido/uv.tar.gz\nUV_LINUX_X86_64_SHA256={sha}\n").replace("\n", "\r\n")
    (pasta / "instalador").mkdir()
    (pasta / "instalador" / "uv_fixado.txt").write_bytes(fixado.encode("utf-8"))
    return pasta, ambiente


def _rodar_lancador(pasta: Path, ambiente: dict, *argumentos: str) -> tuple[int, str]:
    r = subprocess.run([_bash_do_lancador(), *argumentos], cwd=str(pasta), env=ambiente, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", timeout=120, check=False)
    return r.returncode, r.stdout


def teste_gitattributes_fixa_o_fim_de_linha():
    bruto = (RAIZ / ".gitattributes").read_bytes()
    assert b"\r" not in bruto, ".gitattributes precisa de fim de linha LF"
    texto = bruto.decode("utf-8")
    assert "! Alteração de IA - Revisar:" in texto and "! Motivo:" in texto
    linhas = texto.splitlines()
    for regra in ("*.sh text eol=lf", "*.cmd text eol=crlf", "*.bat text eol=crlf", "*.ps1 text eol=crlf",
                  "instalador/uv_fixado.txt text eol=lf"):
        assert regra in linhas, regra


def teste_lancadores_do_linux_tem_lf_tag_e_sintaxe():
    for nome in ("install.sh", "run.sh"):
        bruto = (RAIZ / nome).read_bytes()
        assert b"\r" not in bruto, f"{nome} precisa de fim de linha LF (o `bash\\r` da célula L-U2404)"
        texto = bruto.decode("utf-8")
        assert texto.startswith("#!/usr/bin/env bash\n"), nome
        assert "! Alteração de IA - Revisar:" in texto and "! Motivo:" in texto, nome
        assert "—" not in texto and "→" not in texto, nome
        _conferir_sintaxe_do_shell(texto)
    instalar = (RAIZ / "install.sh").read_text(encoding="utf-8")
    # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) o `install.sh` chama `install.py` (e não mais `instalador.nucleo`), e o `run.sh` chama `run.py` (e não mais `instalador.servicos`).
    # ! Motivo: os consertos de Linux que moravam nos pontos de entrada provisórios entraram no `install.py` e no `_env_common.py`; os módulos provisórios foram apagados. Só as linhas que não são comentário contam nas duas proibições, porque a tag de histórico pode citar o nome antigo.
    for pedaco in ("install.py", "sha256", "uv_fixado.txt"):
        assert pedaco in instalar, pedaco
    # ! Alteração de IA - Revisar: (19/11/2026, I2b, B1) a conferência deixa de proibir o `apt-get` no `install.sh`: agora ele só pode aparecer para instalar o `curl`.
    # ! Motivo: célula L-D13: o Debian 13 do WSL vem sem `curl` e `wget`, e o lançador passa a instalar o `curl` pelo `apt-get`; o que continua proibido é o `brew` e a instalação do Python pelo apt (`python3-venv`, `python3-pip`), que o lançador antigo fazia.
    # O que o lançador faz é conferido fora dos comentários e das mensagens ao usuário (`aviso`).
    codigo = [linha for linha in instalar.splitlines() if not linha.lstrip().startswith("#") and "aviso " not in linha]
    assert not any("brew" in linha or "python3-venv" in linha or "python3-pip" in linha for linha in codigo), codigo
    texto_do_run = (RAIZ / "run.sh").read_text(encoding="utf-8")
    codigo_do_run = [linha for linha in texto_do_run.splitlines() if not linha.lstrip().startswith("#")]
    assert any("run.py" in linha for linha in codigo_do_run), codigo_do_run
    assert not any("instalador.servicos" in linha for linha in codigo_do_run), codigo_do_run
    assert not any("instalador.nucleo" in linha for linha in codigo)


def teste_lancador_usa_o_python_do_sistema_que_serve():
    if _sem_bash():
        return
    pasta, ambiente = _projeto_de_mentira()
    codigo, saida = _rodar_lancador(pasta, ambiente, "install.sh", "--reproduzir")
    assert codigo == 0, saida
    assert any(linha.startswith("NUCLEO: ") and linha.endswith("/install.py --reproduzir") for linha in saida.splitlines()), saida
    assert not (pasta / ".ferramentas").exists(), saida


def teste_lancador_traz_o_python_pelo_uv_e_confere_o_sha():
    if _sem_bash():
        return
    pasta, ambiente = _projeto_de_mentira(com_uv=True)
    ambiente["FALSO_PYTHON_SERVE"] = "1"
    codigo, saida = _rodar_lancador(pasta, ambiente, "install.sh")
    assert codigo == 0, saida
    assert any(linha.startswith("NUCLEO-UV: ") and linha.endswith("/install.py") for linha in saida.splitlines()), saida
    assert list((pasta / ".ferramentas" / "python").glob("*/bin/python3")), saida
    assert not list((pasta / ".ferramentas" / "uv").glob("*.tar.gz")), saida


def teste_lancador_recusa_o_uv_com_sha_errado():
    if _sem_bash():
        return
    pasta, ambiente = _projeto_de_mentira(com_uv=True, sha_certo=False)
    ambiente["FALSO_PYTHON_SERVE"] = "1"
    codigo, saida = _rodar_lancador(pasta, ambiente, "install.sh")
    assert codigo != 0, saida
    assert "SHA-256" in saida, saida
    assert not (pasta / ".ferramentas" / "python").exists(), saida
    assert not list((pasta / ".ferramentas" / "uv").glob("*.tar.gz")), saida


def teste_lancador_com_forcar_uv_ignora_o_python_do_sistema():
    if _sem_bash():
        return
    pasta, ambiente = _projeto_de_mentira(com_uv=True)
    ambiente["COBAIA_FORCAR_UV"] = "1"
    codigo, saida = _rodar_lancador(pasta, ambiente, "install.sh")
    assert codigo == 0, saida
    assert "NUCLEO-UV" in saida, saida


# ! Alteração de IA - Revisar: (19/11/2026, I2b, B1) testes novos do lançador sem `curl` nem `wget`: com `apt-get` ele instala o `curl` e segue; sem `apt-get` ele para dizendo o que instalar.
# ! Motivo: célula L-D13 de 19/11/2026: a imagem do Debian 13 para o WSL vem sem `python3`, `curl` e `wget`; o lançador novo precisa de um dos dois para baixar o `uv` e pararia pedindo um passo manual que o lançador antigo não pedia.
def _projeto_sem_curl_nem_wget() -> tuple[Path, dict] | None:
    """O projeto de mentira com o Python de mentira sem servir (cai no `uv`) e sem `curl` na `bin/`; o `curl` de mentira fica
    guardado fora da `bin/` (variável `CURL_DE_MENTIRA`). Devolve None, com o aviso de pulado, se o PATH do teste tiver `curl`
    ou `wget` de verdade."""
    bash = _bash_para_sintaxe()
    pasta_usr = _pasta_usr_bin_do_bash(bash)
    if shutil.which("curl", path=pasta_usr) or shutil.which("wget", path=pasta_usr):
        print("  pulado: o PATH do teste tem curl ou wget de verdade")
        return None
    pasta, ambiente = _projeto_de_mentira(com_uv=True)
    ambiente["FALSO_PYTHON_SERVE"] = "1"
    guardado = pasta / "curl_guardado"
    shutil.move(str(pasta / "bin" / "curl"), str(guardado))
    ambiente["CURL_DE_MENTIRA"] = guardado.as_posix()
    ambiente["REGISTRO_DO_APT"] = (pasta / "registro_do_apt.txt").as_posix()
    return pasta, ambiente


APT_GET_DE_MENTIRA = """#!/usr/bin/env bash
echo "$*" >> "$REGISTRO_DO_APT"
case " $* " in
    *" install "*" curl "*) cp "$CURL_DE_MENTIRA" "$(dirname "$0")/curl"; chmod +x "$(dirname "$0")/curl" ;;
esac
exit 0
"""

SUDO_DE_MENTIRA = """#!/usr/bin/env bash
exec "$@"
"""


def teste_lancador_instala_o_curl_pelo_apt_quando_falta():
    if _sem_bash():
        return
    montado = _projeto_sem_curl_nem_wget()
    if montado is None:
        return
    pasta, ambiente = montado
    _gravar_roteiro(pasta / "bin" / "sudo", SUDO_DE_MENTIRA)
    _gravar_roteiro(pasta / "bin" / "apt-get", APT_GET_DE_MENTIRA)
    codigo, saida = _rodar_lancador(pasta, ambiente, "install.sh")
    assert codigo == 0, saida
    assert any(linha.startswith("NUCLEO-UV: ") and linha.endswith("/install.py") for linha in saida.splitlines()), saida
    linhas = (pasta / "registro_do_apt.txt").read_text(encoding="utf-8").splitlines()
    assert any("update" in linha for linha in linhas), linhas
    instalou = [linha for linha in linhas if "install" in linha]
    assert len(instalou) == 1, linhas
    for pedaco in ("-y", "curl", "ca-certificates"):
        assert pedaco in instalou[0].split(), instalou


def teste_lancador_sem_curl_e_sem_apt_diz_o_que_instalar():
    if _sem_bash():
        return
    # ! Alteração de IA - Revisar: (19/11/2026, revisão da segunda rodada, achado I-1) o teste é pulado quando o PATH do teste
    # tem um `apt-get` de verdade.
    # ! Motivo: num Linux de `apt` sem `curl` nem `wget` (a própria imagem do Debian 13 da célula L-D13), o lançador acharia o
    # `apt-get` e o `sudo` de verdade e instalaria pacotes na máquina que roda a bateria; o teste é do caminho "sem `apt-get`".
    if shutil.which("apt-get", path=_pasta_usr_bin_do_bash(_bash_para_sintaxe())):
        print("  pulado: o PATH do teste tem apt-get de verdade")
        return
    montado = _projeto_sem_curl_nem_wget()
    if montado is None:
        return
    pasta, ambiente = montado
    codigo, saida = _rodar_lancador(pasta, ambiente, "install.sh")
    assert codigo != 0, saida
    assert "curl" in saida, saida
    assert not (pasta / ".ferramentas" / "python").exists(), saida


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) `teste_run_sh_chama_os_servicos` vira `teste_run_sh_chama_o_run_py`; entram `teste_run_start_services_no_linux_passa_so_o_output_buffering` e `teste_ponto_de_entrada_provisorio_sumiu`.
# ! Motivo: o `run.sh` volta a chamar o `run.py`, que passa ao `php -S` as opções de `_env_common.php_extension_flags` (no Linux só o `output_buffering`; com `-d extension_dir=/usr/bin/ext` o site respondia `Class "mysqli" not found`, célula L-U2404); e os dois módulos provisórios do pacote I2 não podem voltar a ser chamados por nenhum roteiro.
def teste_run_sh_chama_o_run_py():
    if _sem_bash():
        return
    pasta, ambiente = _projeto_de_mentira()
    codigo, saida = _rodar_lancador(pasta, ambiente, "run.sh")
    assert codigo == 0, saida
    assert any(linha.startswith("NUCLEO: ") and linha.endswith("/run.py") for linha in saida.splitlines()), saida


def teste_run_start_services_no_linux_passa_so_o_output_buffering():
    popens: list = []
    php = "/usr/bin/php"
    pasta = _pasta_temporaria()
    python_venv = Path(run.comando_api(pasta / ".venv")[0])
    python_venv.parent.mkdir(parents=True)
    python_venv.write_text("", encoding="utf-8")

    def popen(comando, **kwargs):
        popens.append((comando, kwargs))
        return _Processo()

    original = _trocar([(env, "OS_NAME", "Linux"), (run, "find_php", lambda: php), (run, "find_mysql_cli", lambda: "cli"),
                        (run, "ensure_mariadb_running", lambda cli: True), (run, "COBAIA_API", pasta),
                        (run, "log", lambda msg: None), (run.subprocess, "Popen", popen)])
    try:
        run.start_services()
        assert popens[0][0] == [php, "-S", "localhost:8080", "-t", str(run.COBAIA_FRONT), "-d", "output_buffering=4096"], popens
    finally:
        _destrocar(original)


def teste_ponto_de_entrada_provisorio_sumiu():
    assert not (RAIZ / "instalador" / "nucleo.py").exists()
    assert not (RAIZ / "instalador" / "servicos.py").exists()
    roteiros = [RAIZ / "install.sh", RAIZ / "run.sh", RAIZ / "ferramentas" / "instalador_matriz" / "celula_wsl.ps1",
                RAIZ / "ferramentas" / "instalador_matriz" / "sondas_suspeitas.sh"]
    for roteiro in roteiros:
        for linha in roteiro.read_text(encoding="utf-8").splitlines():
            if linha.lstrip().startswith(("#", "rem ")):
                continue
            assert "instalador.nucleo" not in linha and "instalador.servicos" not in linha, (roteiro.name, linha)
    for arquivo in (RAIZ / "instalador").glob("*.py"):
        for linha in arquivo.read_text(encoding="utf-8").splitlines():
            if linha.lstrip().startswith(("import ", "from ")):
                for nome in ("nucleo", "servicos"):
                    assert nome not in linha.replace("_servicos", ""), (arquivo.name, linha)


# ! Alteração de IA - Revisar: (19/11/2026) teste do roteiro do navegador da prova (N2): a versão do Playwright sai por
# `importlib.metadata`, e não por `playwright.__version__`.
# ! Motivo: célula L-U2404 `novo` de 19/11/2026 (rodada `20261119-094340`): o instalador terminou em "Instalação concluída", o
# Chromium abriu e a página carregou, e o N2 falhou na linha do `print` do roteiro com `AttributeError: module 'playwright'
# has no attribute '__version__'`; o pacote 1.64.1 não tem esse atributo. O defeito era da prova, não do instalador.
def teste_conferir_roteiro_do_navegador_le_a_versao_pelo_metadata():
    roteiro = conferir.ROTEIRO_DO_NAVEGADOR
    compile(roteiro, "<roteiro do navegador>", "exec")
    assert "__version__" not in roteiro, "o pacote playwright não tem __version__"
    assert 'version("playwright")' in roteiro and "importlib.metadata" in roteiro
    # onde a venv do AgenteCore existe (a máquina-alvo), a leitura da versão roda de verdade, sem abrir o navegador
    python_venv = ferramentas.python_da_venv(env.AGENTE_CORE / ".venv")
    if not python_venv.exists():
        print("  pulado: sem a venv do AgenteCore para ler a versão de verdade")
        return
    importacao = [linha for linha in roteiro.splitlines() if "importlib.metadata" in linha][0]
    r = subprocess.run([str(python_venv), "-c", importacao + '\nprint(version("playwright"))'],
                       capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == versoes.carregar()["playwright"]["testada"], r.stdout


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3, tarefa 1) 17 testes que fixam o que `_env_common.py`, `install.py`, `run.py` e `Cobaia.py` fazem hoje no Windows, função por função, sem chamar winget, MariaDB, PHP, Ollama nem rede.
# ! Motivo: o pacote I3 vai mexer nos três primeiros arquivos (e `executar_fase4.py`, `linha_de_base_manual.py`, `restaurar_banco.py` e o `Cobaia.exe` importam todos eles); até aqui só o lado Linux tinha teste, e uma troca que estragasse `winget install --id PHP.PHP.8.2`, os padrões de busca do MariaDB portátil ou a ordem dos passos de `install.main()` só apareceria numa célula de Windows. Cada teste força `OS_NAME = "Windows"` no módulo certo (`env`, `install`), então o resultado não depende do sistema em que a bateria roda; o que é trocado em módulo volta no `finally`.
def _trocar(alvos: list) -> list:
    """Troca atributos de módulo ou objeto e devolve o que havia antes, para `_destrocar`."""
    originais = [(objeto, nome, getattr(objeto, nome)) for objeto, nome, _ in alvos]
    for objeto, nome, novo in alvos:
        setattr(objeto, nome, novo)
    return originais


def _destrocar(originais: list) -> None:
    for objeto, nome, valor in reversed(originais):
        setattr(objeto, nome, valor)


def _levanta(*args, **kwargs):
    raise AssertionError(f"não devia ser chamado: {args} {kwargs}")


class _Processo:
    """Processo de mentira: `poll` devolve o valor dado, `wait` pode levantar o erro dado."""

    def __init__(self, poll=None, erro_no_wait=None):
        self._poll = poll
        self._erro_no_wait = erro_no_wait
        self.chamadas: list = []

    def poll(self):
        return self._poll

    def wait(self, timeout=None):
        self.chamadas.append(("wait", timeout))
        if self._erro_no_wait:
            raise self._erro_no_wait

    def terminate(self):
        self.chamadas.append(("terminate",))


def _respostas(*valores):
    """Função sem argumentos que devolve um valor por chamada, na ordem dada."""
    fila = iter(valores)
    return lambda: next(fila)


def _sai_com_1(funcao) -> None:
    try:
        funcao()
    except SystemExit as erro:
        assert erro.code == 1, erro.code
        return
    raise AssertionError("esperava SystemExit(1)")


def teste_fixa_windows_php_extension_flags():
    original = _trocar([(env, "OS_NAME", "Windows")])
    try:
        php = r"C:\php\php.exe"
        assert env.php_extension_flags(php) == [
            "-d", f"extension_dir={Path(php).parent / 'ext'}",
            "-d", "extension=mysqli",
            "-d", "extension=pdo_mysql",
            "-d", "extension=mbstring",
            "-d", "output_buffering=4096",
        ]
    finally:
        _destrocar(original)


def teste_fixa_windows_ensure_mariadb_running_ja_no_ar():
    original = _trocar([(env, "OS_NAME", "Windows"), (env, "_can_connect", lambda cli: True),
                        (env, "run", _levanta), (env.subprocess, "Popen", _levanta)])
    try:
        assert env.ensure_mariadb_running("cli") is True
    finally:
        _destrocar(original)


def teste_fixa_windows_ensure_mariadb_running_sobe_o_servidor_como_processo():
    popens: list = []
    esperas: list = []
    processo = _Processo()

    def popen(comando, **kwargs):
        popens.append((comando, kwargs))
        return processo

    def espera(*args, **kwargs):
        esperas.append((args, kwargs))
        return True

    original = _trocar([(env, "OS_NAME", "Windows"), (env, "_can_connect", lambda cli: False),
                        (env, "find_mariadbd_server", lambda: r"C:\m\bin\mariadbd.exe"),
                        (env, "find_mariadb_datadir_config", lambda: r"C:\p\.mariadb\data\my.ini"),
                        (env.subprocess, "Popen", popen), (env, "wait_for_mariadb", espera),
                        (env, "run", _levanta), (env, "log", lambda msg: None), (env, "_mariadbd_proc", None)])
    try:
        assert env.ensure_mariadb_running("cli") is True
        assert popens == [([r"C:\m\bin\mariadbd.exe", r"--defaults-file=C:\p\.mariadb\data\my.ini"],
                           {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL})]
        assert esperas == [(("cli",), {"timeout_s": 45})]
        assert env._mariadbd_proc is processo
        # Sem my.ini achado, o comando é só o binário.
        popens.clear()
        env.find_mariadb_datadir_config = lambda: None
        assert env.ensure_mariadb_running("cli") is True
        assert popens == [([r"C:\m\bin\mariadbd.exe"], {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL})]
        # Sem o binário do servidor, devolve False e não sobe nada.
        popens.clear()
        env.find_mariadbd_server = lambda: None
        assert env.ensure_mariadb_running("cli") is False
        assert popens == []
    finally:
        _destrocar(original)


def teste_fixa_windows_stop_managed_mariadbd():
    runs: list = []
    original = _trocar([(env, "find_mariadb_admin", lambda: r"C:\m\bin\mariadb-admin.exe"),
                        (env.subprocess, "run", lambda comando, **kw: runs.append((comando, kw))),
                        (env, "log", lambda msg: None), (env, "_mariadbd_proc", None)])
    try:
        vivo = _Processo(poll=None)
        env._mariadbd_proc = vivo
        env.stop_managed_mariadbd()
        assert runs == [([r"C:\m\bin\mariadb-admin.exe", "-u", "root", "shutdown"], {"capture_output": True, "timeout": 30})]
        assert vivo.chamadas == [("wait", 15)]
        # Se o servidor não encerra em 15 s, terminate().
        runs.clear()
        teimoso = _Processo(poll=None, erro_no_wait=subprocess.TimeoutExpired("x", 15))
        env._mariadbd_proc = teimoso
        env.stop_managed_mariadbd()
        assert teimoso.chamadas == [("wait", 15), ("terminate",)]
        # Sem processo gerenciado, nada é chamado.
        runs.clear()
        env._mariadbd_proc = None
        env.stop_managed_mariadbd()
        assert runs == []
    finally:
        _destrocar(original)


def teste_fixa_windows_ensure_root_no_password():
    mensagens: list = []
    original = _trocar([(env, "OS_NAME", "Windows"), (env.subprocess, "run", _levanta),
                        (env, "log", mensagens.append), (env, "_can_connect", lambda cli: True)])
    try:
        assert env.ensure_root_no_password("cli") is True
        assert mensagens == []
        env._can_connect = lambda cli: False
        assert env.ensure_root_no_password("cli") is False
        assert len(mensagens) == 3 and all(m.startswith("!!") for m in mensagens), mensagens
    finally:
        _destrocar(original)


def teste_fixa_windows_onde_o_env_common_procura():
    padroes: list = []
    original = _trocar([(env, "OS_NAME", "Windows"), (env, "which_any", lambda *nomes: None),
                        (env, "find_by_glob", lambda *p: padroes.append(p))])
    try:
        esperados = {
            "find_php": (
                os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\PHP.PHP*\php.exe"),
                r"C:\tools\php*\php.exe",
                r"C:\Program Files\PHP\*\php.exe",
                r"C:\PHP*\php.exe"),
            "find_mysql_cli": (
                r"C:\Program Files\MariaDB*\bin\mariadb.exe",
                r"C:\Program Files\MariaDB*\bin\mysql.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\MariaDB\mariadb-*-winx64\bin\mariadb.exe")),
            "find_mariadbd_server": (
                r"C:\Program Files\MariaDB*\bin\mariadbd.exe",
                r"C:\Program Files\MariaDB*\bin\mysqld.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\MariaDB\mariadb-*-winx64\bin\mariadbd.exe")),
            "find_mariadb_admin": (
                r"C:\Program Files\MariaDB*\bin\mariadb-admin.exe",
                r"C:\Program Files\MariaDB*\bin\mysqladmin.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\MariaDB\mariadb-*-winx64\bin\mariadb-admin.exe")),
            "find_ollama": (
                os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe"),
                os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Ollama.Ollama*\ollama.exe"),
                r"C:\Program Files\Ollama\ollama.exe"),
        }
        for nome, esperado in esperados.items():
            padroes.clear()
            assert getattr(env, nome)() is None, nome
            assert padroes == [esperado], (nome, padroes)
        # Achado no PATH: devolve o achado sem olhar as pastas conhecidas.
        env.which_any = lambda *nomes: "x"
        env.find_by_glob = _levanta
        for nome in esperados:
            assert getattr(env, nome)() == "x", nome
    finally:
        _destrocar(original)


def _gravador_de_passos(chamadas: list, nome: str, devolve=None):
    def passo(*args):
        chamadas.append((nome, args))
        return devolve
    return passo


def teste_fixa_windows_install_main_ordem_dos_passos():
    chamadas: list = []
    mensagens: list = []
    troca = [(install, "OS_NAME", "Windows"), (sistema, "detectar", lambda: sistema.familia("Windows")),
             (install, "ensure_php", _gravador_de_passos(chamadas, "ensure_php")),
             (install, "ensure_mariadb_installed", _gravador_de_passos(chamadas, "ensure_mariadb_installed", "cli")),
             (install, "ensure_mariadb_running", _gravador_de_passos(chamadas, "ensure_mariadb_running", True)),
             (install, "ensure_root_no_password", _gravador_de_passos(chamadas, "ensure_root_no_password")),
             (install, "apply_sql_files", _gravador_de_passos(chamadas, "apply_sql_files")),
             (install, "setup_cobaia_api", _gravador_de_passos(chamadas, "setup_cobaia_api")),
             (install, "setup_agente_core", _gravador_de_passos(chamadas, "setup_agente_core")),
             (install, "log", mensagens.append)]
    # `gravar_passos` só passa a existir na tarefa 3 do I3 e gravaria um arquivo em `.ferramentas/`; aqui ela não faz nada.
    if hasattr(install, "gravar_passos"):
        troca.append((install, "gravar_passos", lambda *args, **kwargs: None))
    original = _trocar(troca)
    try:
        assert install.main() in (None, 0)
        assert chamadas == [("ensure_php", ()), ("ensure_mariadb_installed", ()), ("ensure_mariadb_running", ("cli",)),
                            ("ensure_root_no_password", ("cli",)), ("apply_sql_files", ("cli",)),
                            ("setup_cobaia_api", ()), ("setup_agente_core", ())], chamadas
        assert any("Instalação concluída" in m for m in mensagens)
        assert any("run.cmd" in m for m in mensagens)
        # O banco não sobe: sai com código 1 e nenhum passo depois dele roda.
        chamadas.clear()
        mensagens.clear()
        install.ensure_mariadb_running = _gravador_de_passos(chamadas, "ensure_mariadb_running", False)
        _sai_com_1(install.main)
        assert [c[0] for c in chamadas] == ["ensure_php", "ensure_mariadb_installed", "ensure_mariadb_running"], chamadas
        assert any("Não foi possível subir o MariaDB" in m for m in mensagens)
    finally:
        _destrocar(original)


def teste_fixa_windows_ensure_php():
    comandos: list = []
    winget = ["winget", "install", "--id", "PHP.PHP.8.2", "-e", "--accept-package-agreements", "--accept-source-agreements"]
    original = _trocar([(install, "OS_NAME", "Windows"), (install, "log", lambda msg: None),
                        (install, "run", lambda cmd, **kw: comandos.append(cmd) or _Resultado(0)),
                        (install, "find_php", lambda: r"C:\php\php.exe")])
    try:
        assert install.ensure_php() == r"C:\php\php.exe"
        assert comandos == []
        install.find_php = _respostas(None, r"C:\php\php.exe")
        assert install.ensure_php() == r"C:\php\php.exe"
        assert comandos == [winget]
        install.find_php = lambda: None
        _sai_com_1(install.ensure_php)
    finally:
        _destrocar(original)


def teste_fixa_windows_ensure_mariadb_installed():
    comandos: list = []
    portateis: list = []
    codigo = [0]
    winget = ["winget", "install", "--id", "MariaDB.Server", "-e", "--accept-package-agreements", "--accept-source-agreements"]
    original = _trocar([(install, "OS_NAME", "Windows"), (install, "log", lambda msg: None),
                        (install, "find_mysql_cli", lambda: "cli"),
                        (install, "usar_mariadb_portatil", lambda *a, **k: True),
                        (install, "instalar_mariadb_portatil", lambda *a, **k: portateis.append(comandos[:])),
                        (install, "run", lambda cmd, **kw: comandos.append(cmd) or _Resultado(codigo[0]))])
    try:
        # (a) cliente achado: nada roda.
        assert install.ensure_mariadb_installed() == "cli"
        assert comandos == [] and portateis == []
        # (b) não achado, portátil: instala o portátil e não chama o winget.
        install.find_mysql_cli = _respostas(None, "cli")
        assert install.ensure_mariadb_installed() == "cli"
        assert comandos == [] and len(portateis) == 1
        # (c) winget com código 0: o portátil não é chamado.
        portateis.clear()
        install.usar_mariadb_portatil = lambda *a, **k: False
        install.find_mysql_cli = _respostas(None, "cli")
        assert install.ensure_mariadb_installed() == "cli"
        assert comandos == [winget] and portateis == []
        # (d) winget com código 1: o portátil é chamado depois do winget.
        comandos.clear()
        codigo[0] = 1
        install.find_mysql_cli = _respostas(None, "cli")
        assert install.ensure_mariadb_installed() == "cli"
        assert comandos == [winget] and portateis == [[winget]]
        # (e) cliente nunca achado: SystemExit(1).
        install.find_mysql_cli = lambda: None
        _sai_com_1(install.ensure_mariadb_installed)
    finally:
        _destrocar(original)


def teste_fixa_windows_ensure_ollama():
    comandos: list = []
    winget = ["winget", "install", "--id", "Ollama.Ollama", "-e", "--accept-package-agreements", "--accept-source-agreements"]
    original = _trocar([(install, "OS_NAME", "Windows"), (install, "log", lambda msg: None),
                        (install, "find_ollama", lambda: "ollama.exe"),
                        (install, "run", lambda cmd, **kw: comandos.append(cmd) or _Resultado(0))])
    try:
        assert install.ensure_ollama() == "ollama.exe"
        assert comandos == []
        install.find_ollama = _respostas(None, "ollama.exe")
        assert install.ensure_ollama() == "ollama.exe"
        assert comandos == [winget]
        comandos.clear()
        install.find_ollama = lambda: None
        assert install.ensure_ollama() is None
        assert comandos == [winget]
    finally:
        _destrocar(original)


def teste_fixa_windows_setup_cobaia_api():
    comandos: list = []
    mensagens: list = []
    pasta = _pasta_temporaria()
    original = _trocar([(install, "OS_NAME", "Windows"), (install, "IS_FROZEN", False), (install, "COBAIA_API", pasta),
                        (install, "log", mensagens.append),
                        (install, "run", lambda cmd, **kw: comandos.append(cmd) or _Resultado(0))])
    try:
        venv = pasta / ".venv"
        req = pasta / "requirements-dev.txt"
        pip = str(venv / "Scripts/pip.exe")
        req.write_text("fastapi\n", encoding="utf-8")
        install.setup_cobaia_api()
        assert comandos == [[sys.executable, "-m", "venv", str(venv)], [pip, "install", "-r", str(req)]], comandos
        # Com a .venv criada, só o pip.
        comandos.clear()
        venv.mkdir()
        install.setup_cobaia_api()
        assert comandos == [[pip, "install", "-r", str(req)]], comandos
        # Sem requirements-dev.txt: nenhum pip e um aviso.
        comandos.clear()
        mensagens.clear()
        vazia = _pasta_temporaria()
        install.COBAIA_API = vazia
        install.setup_cobaia_api()
        assert comandos == [[sys.executable, "-m", "venv", str(vazia / ".venv")]], comandos
        assert any("requirements-dev.txt" in m for m in mensagens)
    finally:
        _destrocar(original)


def teste_fixa_windows_setup_agente_core():
    comandos: list = []
    mensagens: list = []
    pasta = _pasta_temporaria()
    (pasta / "requirements.txt").write_text("playwright\n", encoding="utf-8")
    (pasta / ".venv").mkdir()
    venv = pasta / ".venv"
    req = pasta / "requirements.txt"
    pip = str(venv / "Scripts" / "pip.exe")
    python_venv = str(venv / "Scripts" / "python.exe")
    estado = {"chromium": False, "ollama": "ollama.exe", "modelo": False}
    modelo_anterior = os.environ.pop("COBAIA_MODELO_LLM", None)
    original = _trocar([(install, "OS_NAME", "Windows"), (install, "IS_FROZEN", False), (install, "AGENTE_CORE", pasta),
                        (install, "log", mensagens.append),
                        (install, "run", lambda cmd, **kw: comandos.append(cmd) or _Resultado(0)),
                        (install, "playwright_chromium_instalado", lambda: estado["chromium"]),
                        (install, "ensure_ollama", lambda: estado["ollama"]),
                        (install, "modelo_llm_ja_baixado", lambda ollama, modelo: estado["modelo"])])
    try:
        install.setup_agente_core()
        assert comandos == [[pip, "install", "-r", str(req)], [python_venv, "-m", "playwright", "install", "chromium"],
                            ["ollama.exe", "pull", "qwen2.5:7b"]], comandos
        # COBAIA_MODELO_LLM manda no nome do modelo.
        comandos.clear()
        os.environ["COBAIA_MODELO_LLM"] = "x:1"
        install.setup_agente_core()
        assert comandos[-1] == ["ollama.exe", "pull", "x:1"], comandos
        os.environ.pop("COBAIA_MODELO_LLM")
        # Chromium e modelo já na máquina: só o pip.
        comandos.clear()
        estado["chromium"] = True
        estado["modelo"] = True
        install.setup_agente_core()
        assert comandos == [[pip, "install", "-r", str(req)]], comandos
        # Sem Ollama não há pull.
        comandos.clear()
        estado["ollama"] = None
        estado["modelo"] = False
        install.modelo_llm_ja_baixado = _levanta
        install.setup_agente_core()
        assert comandos == [[pip, "install", "-r", str(req)]], comandos
        # Sem requirements.txt nada roda.
        comandos.clear()
        mensagens.clear()
        install.AGENTE_CORE = _pasta_temporaria()
        install.setup_agente_core()
        assert comandos == []
        assert any("AgenteCore ainda não implementado" in m for m in mensagens)
    finally:
        _destrocar(original)
        os.environ.pop("COBAIA_MODELO_LLM", None)
        if modelo_anterior is not None:
            os.environ["COBAIA_MODELO_LLM"] = modelo_anterior


class _RespostaSql:
    def __init__(self, returncode: int = 0):
        self.returncode = returncode
        self.stderr = b""


def teste_fixa_apply_sql_files():
    chamadas: list = []
    mensagens: list = []
    codigo = [0]
    pasta = _pasta_temporaria()
    (pasta / "banco").mkdir()
    for nome in ("bancoatualizado.sql", "schema_completo.sql", "seed.sql"):
        (pasta / "banco" / nome).write_text("SELECT 1;\n", encoding="utf-8")

    def executar(comando, **kwargs):
        chamadas.append((comando, Path(kwargs["stdin"].name).name))
        return _RespostaSql(codigo[0])

    original = _trocar([(install, "COBAIA_FRONT", pasta), (install, "log", mensagens.append),
                        (install.subprocess, "run", executar)])
    try:
        install.apply_sql_files("cli")
        assert chamadas == [(["cli", "-u", "root"], "bancoatualizado.sql"), (["cli", "-u", "root"], "schema_completo.sql"),
                            (["cli", "-u", "root"], "seed.sql")], chamadas
        # Arquivo faltando é pulado, com aviso.
        chamadas.clear()
        mensagens.clear()
        (pasta / "banco" / "schema_completo.sql").unlink()
        install.apply_sql_files("cli")
        assert [c[1] for c in chamadas] == ["bancoatualizado.sql", "seed.sql"]
        assert any("Aviso" in m for m in mensagens)
        # Erro do cliente: SystemExit(1).
        codigo[0] = 1
        _sai_com_1(lambda: install.apply_sql_files("cli"))
    finally:
        _destrocar(original)


class _RespostaHttp:
    def __init__(self, blocos: int, tamanho: int):
        self.headers = {"Content-Length": str(blocos * tamanho)}
        self._restantes = blocos
        self._tamanho = tamanho

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, n):
        if self._restantes <= 0:
            return b""
        self._restantes -= 1
        return b"x" * self._tamanho


def teste_fixa_baixar_arquivo_progresso_de_arquivo_grande():
    mensagens: list = []
    destino = _pasta_temporaria() / "x.zip"
    original = _trocar([(install.urllib.request, "urlopen", lambda pedido, timeout=None: _RespostaHttp(25, 1 << 20)),
                        (install, "log", mensagens.append)])
    try:
        assert install.baixar_arquivo("http://exemplo.invalido/x.zip", destino) == 25 << 20
        assert destino.stat().st_size == 25 << 20
        assert mensagens == ["  1 MB de 25 MB", "  10 MB de 25 MB", "  20 MB de 25 MB"], mensagens
    finally:
        _destrocar(original)


def teste_fixa_windows_run_start_services():
    popens: list = []
    php = r"C:\php\php.exe"
    pasta = _pasta_temporaria()
    python_venv = Path(run.comando_api(pasta / ".venv")[0])
    python_venv.parent.mkdir(parents=True)
    python_venv.write_text("", encoding="utf-8")

    def popen(comando, **kwargs):
        popens.append((comando, kwargs))
        return _Processo()

    original = _trocar([(env, "OS_NAME", "Windows"), (run, "find_php", lambda: php), (run, "find_mysql_cli", lambda: "cli"),
                        (run, "ensure_mariadb_running", lambda cli: True), (run, "COBAIA_API", pasta),
                        (run, "log", lambda msg: None), (run.subprocess, "Popen", popen)])
    try:
        front, api = run.start_services()
        assert len(popens) == 2
        assert popens[0][0] == [php, "-S", "localhost:8080", "-t", str(run.COBAIA_FRONT),
                                "-d", f"extension_dir={Path(php).parent / 'ext'}",
                                "-d", "extension=mysqli", "-d", "extension=pdo_mysql",
                                "-d", "extension=mbstring", "-d", "output_buffering=4096"]
        assert popens[1][0] == run.comando_api(pasta / ".venv")
        assert popens[1][1] == {"cwd": str(pasta)}
        # Quatro saídas com código 1.
        popens.clear()
        run.find_php = lambda: None
        _sai_com_1(run.start_services)
        run.find_php = lambda: php
        run.find_mysql_cli = lambda: None
        _sai_com_1(run.start_services)
        run.find_mysql_cli = lambda: "cli"
        run.ensure_mariadb_running = lambda cli: False
        _sai_com_1(run.start_services)
        run.ensure_mariadb_running = lambda cli: True
        run.COBAIA_API = _pasta_temporaria()
        _sai_com_1(run.start_services)
        assert popens == []
    finally:
        _destrocar(original)


def teste_fixa_run_wait_and_cleanup():
    paradas: list = []
    site = _Processo(poll=0)
    api = _Processo(poll=None)
    original = _trocar([(run.time, "sleep", lambda s: None), (run, "stop_managed_mariadbd", lambda: paradas.append(1))])
    try:
        run.wait_and_cleanup(site, api)
        assert site.chamadas == []
        assert api.chamadas == [("terminate",)]
        assert paradas == [1]
    finally:
        _destrocar(original)


def teste_fixa_cobaia_py_instala_sobe_e_abre():
    import Cobaia
    chamadas: list = []
    original = _trocar([(install, "main", lambda: chamadas.append(("install.main",))),
                        (run, "start_services", lambda: chamadas.append(("start_services",)) or ("site", "api")),
                        (run, "wait_until_ready", lambda *a, **k: chamadas.append(("wait_until_ready",)) or True),
                        (Cobaia.webbrowser, "open", lambda url, *a, **k: chamadas.append(("open", url))),
                        (run, "wait_and_cleanup", lambda f, a: chamadas.append(("wait_and_cleanup", f, a)))])
    try:
        Cobaia.main()
        assert chamadas == [("install.main",), ("start_services",), ("wait_until_ready",),
                            ("open", "http://localhost:8080"), ("open", "http://localhost:8000/docs"),
                            ("wait_and_cleanup", "site", "api")], chamadas
    finally:
        _destrocar(original)


# ! Alteração de IA - Revisar: (25/11/2026, pacote I5, decisão 153) testes novos do roteiro `celula_actions.py` e do fluxo `.github/workflows/instalador.yml`: comando e ambiente por sistema, escolha do Python da prova, `celula.json` com a tag, veredito e resumo, e as quatro células do fluxo.
# ! Motivo: cada execução de verdade do fluxo custa um commit e um push do dono do repositório; o que dá para conferir sem rede (que variável responde a que pergunta do instalador, que comando a prova roda, se o `celula.json` leva a tag exigida pela decisão 147) fica coberto aqui, para o erro aparecer antes do push e não na página do GitHub.
def teste_celula_actions_comando_e_ambiente_por_sistema():
    ca = celula_actions
    assert ca.comando_do_instalador("Linux") == ["./install.sh"]
    assert ca.comando_do_instalador("Darwin") == ["./install.sh"]
    assert ca.comando_do_instalador("Windows") == ["cmd", "/c", "install.cmd"]
    base = {"PATH": "x"}
    linux = ca.ambiente_do_instalador("Linux", True, base)
    assert linux["COBAIA_ROOT_SEM_SENHA"] == "1" and linux["COBAIA_FORCAR_UV"] == "1" and linux["PATH"] == "x"
    assert "COBAIA_FORCAR_UV" not in ca.ambiente_do_instalador("Darwin", False, base)
    windows = ca.ambiente_do_instalador("Windows", True, base)
    assert windows["COBAIA_MARIADB_PORTATIL"] == "1" and "COBAIA_ROOT_SEM_SENHA" not in windows
    assert base == {"PATH": "x"}, "o ambiente de entrada não pode ser alterado"
    # C2: nos três sistemas a saída sai em UTF-8 e sem atraso (o executor do Windows usa a codepage e junta a saída em buffer)
    for sistema in ("Linux", "Darwin", "Windows"):
        amb = ca.ambiente_do_instalador(sistema, False, base)
        assert (amb["PYTHONIOENCODING"], amb["PYTHONUTF8"], amb["PYTHONUNBUFFERED"]) == ("utf-8", "1", "1"), sistema
    prova = ca.ambiente_da_prova(base)
    assert (prova["PYTHONIOENCODING"], prova["PYTHONUTF8"], prova["PYTHONUNBUFFERED"], prova["PATH"]) == ("utf-8", "1", "1", "x")
    assert "COBAIA_ROOT_SEM_SENHA" not in prova and base == {"PATH": "x"}


def teste_celula_actions_limites_somam_menos_que_o_do_github():
    assert celula_actions.LIMITE_DO_INSTALADOR_S == 3600 and celula_actions.LIMITE_DA_PROVA_S == 3600
    assert celula_actions.CELULAS_DO_ACTIONS == ("CI-UBU", "CI-WIN", "M-15", "M-15I")


def teste_celula_actions_python_da_prova_prefere_o_que_o_lancador_trouxe():
    raiz = _pasta_temporaria()
    assert celula_actions.python_da_prova(raiz, "Linux") == "python3"
    assert celula_actions.python_da_prova(raiz, "Windows") == "python"
    trazido = raiz / ".ferramentas" / "python" / "cpython-3.14.7-linux-x86_64-gnu" / "bin"
    trazido.mkdir(parents=True)
    (trazido / "python3").write_text("", encoding="utf-8")
    assert celula_actions.python_da_prova(raiz, "Linux") == str(trazido / "python3")
    assert celula_actions.python_da_prova(raiz, "Windows") == "python"
    comando = celula_actions.comando_da_prova("python3", "M-15", Path("/tmp/e"), "N3", "qwen2.5:0.5b-instruct")
    assert comando == ["python3", "-m", "instalador.conferir", "--celula", "M-15", "--saida", str(Path("/tmp/e")),
                       "--ate", "N3", "--modelo-pequeno", "qwen2.5:0.5b-instruct"], comando


def teste_celula_actions_celula_json_tem_tag_e_origem():
    ambiente = {"RUNNER_OS": "macOS", "RUNNER_ARCH": "ARM64", "ImageOS": "macos15", "ImageVersion": "20261104.0514.1",
                "GITHUB_REPOSITORY": "dono/repo", "GITHUB_SHA": "a" * 40, "GITHUB_RUN_ID": "123", "GITHUB_RUN_ATTEMPT": "2",
                "GITHUB_EVENT_NAME": "push"}
    inicio = datetime(2026, 11, 26, 12, 0, 0)
    celula = celula_actions.montar_celula("M-15", "N3", "qwen2.5:0.5b-instruct", True, inicio, datetime(2026, 11, 26, 12, 30, 0),
                                          {"instalador": 0, "conferir": 1}, ambiente, modo="como-esta", terminou=True,
                                          resultado_do_instalador="ok")
    assert celula["tag_ia"]["alteracao"].startswith("! Alteração de IA - Revisar: ")
    assert celula["tag_ia"]["motivo"].startswith("! Motivo: ")
    assert (celula["id"], celula["modo"], celula["ate"], celula["forcar_uv"]) == ("M-15", "como-esta", "N3", True)
    assert (celula["terminou"], celula["fuso"], celula["resultado_do_instalador"]) == (True, "UTC", "ok")
    parcial = celula_actions.montar_celula("M-15", "N3", "m", False, inicio, inicio, {}, {}, modo="novo", terminou=False)
    assert parcial["terminou"] is False and parcial["modo"] == "novo" and parcial["saidas"] == {} and parcial["resultado_do_instalador"] == ""
    assert celula["imagem"] == "GitHub Actions: macOS ARM64, imagem macos15 20261104.0514.1"
    assert celula["actions"] == {"repositorio": "dono/repo", "commit": "a" * 40, "execucao": "123", "tentativa": "2", "evento": "push"}
    assert celula["inicio"] == "2026-11-26T12:00:00" and celula["fim"] == "2026-11-26T12:30:00"
    assert celula["saidas"] == {"instalador": "0", "conferir": "1"}      # texto, como nas outras células
    assert celula_actions.carimbo(inicio) == "20261126-120000"
    sem_actions = celula_actions.montar_celula("X", "N1", "m", False, inicio, inicio, {}, {}, modo="novo", terminou=True)
    assert sem_actions["imagem"] == "GitHub Actions: sistema e imagem não informados" and sem_actions["actions"]["commit"] == ""


def teste_celula_actions_veredito_e_resumo():
    ca = celula_actions
    assert ca.veredito(None) == 1
    bom = {"falhou": False, "impedida_por_versao": [], "alcancado": "N3",
           "niveis": {"N1": {"estado": "passou", "detalhe": "14 produtos", "segundos": 12.0},
                      "N2": {"estado": "passou", "detalhe": "", "segundos": 3.0},
                      "N3": {"estado": "passou", "detalhe": "", "segundos": 5.0},
                      "N4": {"estado": "nao_coube", "detalhe": "3,1 GB livres", "segundos": 2.0}},
           "versoes": {"php": {"encontrada": "8.4.1", "testada": "8.2.35", "estado": "na_faixa", "impede": False}}}
    assert ca.veredito(bom) == 0                                          # não caber na memória não é falha
    assert ca.veredito({**bom, "falhou": True}) == 1
    assert ca.veredito({**bom, "impedida_por_versao": ["php"]}) == 1
    celula = {"id": "M-15", "ate": "N3", "imagem": "GitHub Actions: macOS ARM64, imagem macos15 1", "saidas": {"instalador": "0", "conferir": "0"},
              "resultado_do_instalador": "falhou_no_passo_x"}
    texto = ca.resumo_em_markdown(celula, bom, "fim do log do instalador", "fim do log da prova")
    for pedaco in ("M-15", "N3", "| N1 | passou |", "| N4 | nao_coube |", "14 produtos", "php", "8.4.1", "na_faixa",
                   "fim do log do instalador", "fim do log da prova", "Resultado gravado pelo instalador: falhou_no_passo_x"):
        assert pedaco in texto, pedaco
    sem_prova = ca.resumo_em_markdown(celula, None, "x", "y")
    assert "a prova não gravou o registro" in sem_prova
    assert "—" not in texto and "→" not in texto


def teste_instalador_yml_tem_as_quatro_celulas_e_guarda_a_evidencia():
    texto = (RAIZ / ".github" / "workflows" / "instalador.yml").read_text(encoding="utf-8")
    assert "\t" not in texto, "YAML não aceita tabulação"
    assert "! Alteração de IA - Revisar:" in texto and "! Motivo:" in texto
    for pedaco in ("workflow_dispatch:", "schedule:", "contents: read", "fail-fast: false",
                   "id: CI-UBU", "id: CI-WIN", "id: M-15", "id: M-15I",
                   "runner: ubuntu-24.04", "runner: windows-2025", "runner: macos-15", "runner: macos-15-intel",
                   "ferramentas/instalador_matriz/celula_actions.py", "actions/upload-artifact@", "if: always()", "celula-${{ matrix.id }}",
                   "modo: como-esta", "modo: novo", '--modo "${{ matrix.modo }}"', "cancel-in-progress: false", "repositório é público"):
        assert pedaco in texto, pedaco
    assert "cancel-in-progress: true" not in texto


# ! Alteração de IA - Revisar: (25/11/2026, pacote I7) testes novos do `importar_actions.py`: traz uma rodada de um zip para a pasta `celulas/`, e recusa o que não é evidência (sem `celula.json`, sem tag, `id` diferente da pasta, nome de pasta fora do formato, regravação, caminho que sai da pasta).
# ! Motivo: o zip que o GitHub entrega é arquivo baixado; se o importador aceitasse pasta sem tag ou com `id` trocado, uma evidência errada entraria no repositório e no relatório sem ninguém perceber, e regravar uma rodada apagaria evidência que já foi lida.
def _zip_de_rodada(destino: Path, arquivos: dict) -> Path:
    caminho = destino / "celula-X.zip"
    with zipfile.ZipFile(caminho, "w") as z:
        for nome, conteudo in arquivos.items():
            z.writestr(nome, conteudo)
    return caminho


_CELULA_JSON_CERTO = json.dumps({"tag_ia": {"alteracao": "! Alteração de IA - Revisar: x", "motivo": "! Motivo: y"},
                                 "id": "CI-UBU", "modo": "novo", "ate": "N3", "actions": {"commit": "a" * 40},
                                 "inicio": "2026-11-26T12:00:00",
                                 "fim": "2026-11-26T12:30:00", "saidas": {"instalador": "0", "conferir": "0"}})


def teste_importar_actions_traz_a_rodada():
    base = _pasta_temporaria()
    arquivos = {"CI-UBU/20261126-120000/celula.json": _CELULA_JSON_CERTO,
                "CI-UBU/20261126-120000/instalacao.log": "linha 1\nlinha 2\n",
                "CI-UBU/20261126-120000/registro.json": json.dumps({"alcancado": "N3", "niveis": {}})}
    pacote = _zip_de_rodada(base, arquivos)
    celulas = base / "celulas"
    gravadas = importar_actions.importar(pacote, celulas)
    assert gravadas == [celulas / "CI-UBU" / "20261126-120000"], gravadas
    for nome, conteudo in arquivos.items():
        assert (celulas / nome).read_text(encoding="utf-8") == conteudo, nome
    # uma pasta já extraída também serve, e o resumo de ler_celula lê o que foi gravado
    assert importar_actions.rodadas_do_pacote(celulas) == gravadas
    assert ler_celula.resumir(gravadas[0])["alcancado"] == "N3"
    assert importar_actions.conferir_rodada(gravadas[0]) == []


def teste_importar_actions_recusa_o_que_nao_e_evidencia():
    base = _pasta_temporaria()
    celulas = base / "celulas"

    def recusa(nome_do_zip: str, arquivos: dict, trecho: str) -> None:
        pasta = base / nome_do_zip
        pasta.mkdir()
        try:
            importar_actions.importar(_zip_de_rodada(pasta, arquivos), celulas)
        except ValueError as e:
            assert trecho in str(e), (trecho, str(e))
        else:
            raise AssertionError(f"devia recusar: {nome_do_zip}")
        assert not celulas.exists() or not any(celulas.rglob("*.json")), "recusou mas gravou"

    recusa("sem_celula_json", {"CI-UBU/20261126-120000/instalacao.log": "x"}, "celula.json")
    sem_tag = json.dumps({"id": "CI-UBU", "modo": "novo"})
    recusa("sem_tag", {"CI-UBU/20261126-120000/celula.json": sem_tag}, "tag")
    recusa("id_trocado", {"CI-WIN/20261126-120000/celula.json": _CELULA_JSON_CERTO}, "id")
    recusa("nome_ruim", {"CI-UBU/ontem/celula.json": _CELULA_JSON_CERTO}, "AAAAMMDD-HHMMSS")
    recusa("fora_da_pasta", {"CI-UBU/20261126-120000/celula.json": _CELULA_JSON_CERTO, "../fora.txt": "x"}, "fora da pasta")
    assert not (base / "fora.txt").exists()
    # regravar a mesma rodada é recusado e não muda o que já está lá
    pasta = base / "repete"
    pasta.mkdir()
    pacote = _zip_de_rodada(pasta, {"CI-UBU/20261126-120000/celula.json": _CELULA_JSON_CERTO})
    importar_actions.importar(pacote, celulas)
    antes = (celulas / "CI-UBU" / "20261126-120000" / "celula.json").read_bytes()
    try:
        importar_actions.importar(pacote, celulas)
    except ValueError as e:
        assert "já existe" in str(e), str(e)
    else:
        raise AssertionError("devia recusar a regravação")
    assert (celulas / "CI-UBU" / "20261126-120000" / "celula.json").read_bytes() == antes


def teste_importar_actions_so_aceita_celula_do_actions_e_nao_estoura():
    base = _pasta_temporaria()
    celulas = base / "celulas"

    def recusa(nome_do_zip: str, arquivos: dict, trecho: str, **extra) -> None:
        pasta = base / nome_do_zip
        pasta.mkdir()
        try:
            importar_actions.importar(_zip_de_rodada(pasta, arquivos), celulas, **extra)
        except ValueError as e:
            assert trecho in str(e), (trecho, str(e))
        else:
            raise AssertionError(f"devia recusar: {nome_do_zip}")
        assert not celulas.exists() or not any(celulas.rglob("*.json")), "recusou mas gravou"

    recusa("json_lista", {"CI-UBU/20261126-120000/celula.json": "[1, 2]"}, "objeto")
    recusa("json_quebrado", {"CI-UBU/20261126-120000/celula.json": "{ nao e json"}, "JSON")
    sem_actions = json.loads(_CELULA_JSON_CERTO)
    del sem_actions["actions"]
    recusa("sem_actions", {"CI-UBU/20261126-120000/celula.json": json.dumps(sem_actions)}, "actions")
    de_wsl = {**json.loads(_CELULA_JSON_CERTO), "id": "L-U2404"}
    recusa("id_fora_da_lista", {"L-U2404/20261126-120000/celula.json": json.dumps(de_wsl)}, "L-U2404")
    recusa("grande_demais", {"CI-UBU/20261126-120000/celula.json": _CELULA_JSON_CERTO,
                             "CI-UBU/20261126-120000/instalacao.log": "x" * 500}, "grande", limite_descompactado=100)
    # arquivo que não é zip
    ruim = base / "nao_e_zip.zip"
    ruim.write_bytes(b"isto nao e um zip")
    try:
        importar_actions.importar(ruim, celulas)
    except ValueError as e:
        assert "zip" in str(e), str(e)
    else:
        raise AssertionError("devia recusar o arquivo que não é zip")


# ! Alteração de IA - Revisar: (25/11/2026, pacote I7) testes do `relatorio.py`: `_celulas_de_mentira` monta uma pasta `celulas/` com quatro células (uma com duas rodadas, uma rodada sem `registro.json`, uma do GitHub Actions e uma com `celula.json` gravado com BOM), e cinco testes conferem a coleta, o resumo por célula, os blocos em Markdown, a troca do bloco marcado e a concordância do repositório real com as evidências.
# ! Motivo: o relatório do instalador (`relatorio-instalador-maquina-limpa.md`) e os blocos do README e do DETALHES-TECNICOS saem de script e não de digitação; sem teste, uma rodada sem `registro.json` (a do Arch e a do openSUSE no modo `como-esta`, que param antes da prova), uma rodada do Actions ou um `|` dentro do erro literal de um nível quebrariam a tabela sem ninguém ver. O último teste é o `--check` rodado no repositório: se alguém trouxer uma rodada nova (`importar_actions.py`) e esquecer o `relatorio.py --colar`, a bateria acusa.
def _celulas_de_mentira() -> Path:
    celulas = _pasta_temporaria() / "celulas"

    def rodada(ident: str, nome: str, celula: dict, registro: dict | None = None, bom: bool = False) -> None:
        pasta = celulas / ident / nome
        pasta.mkdir(parents=True)
        texto = json.dumps({"id": ident, **celula}, ensure_ascii=False, indent=1)
        (pasta / "celula.json").write_text(texto, encoding="utf-8-sig" if bom else "utf-8")
        if registro is not None:
            (pasta / "registro.json").write_text(json.dumps(registro, ensure_ascii=False), encoding="utf-8")

    nao_rodou = {"estado": "nao_rodou", "detalhe": "", "segundos": None}
    rodada("L-U2404", "20261119-094340",
           {"modo": "novo", "ate": "N3", "imagem": "ubuntu.wsl"},
           {"alcancado": "N3", "falhou": False, "impedida_por_versao": [], "sistema": {"nome": "Ubuntu 24.04.5 LTS"},
            "niveis": {"N1": {"estado": "passou", "detalhe": "14 produtos", "segundos": 1.0},
                       "N2": {"estado": "passou", "detalhe": "", "segundos": 1.0},
                       "N3": {"estado": "passou", "detalhe": "", "segundos": 1.0}, "N4": nao_rodou}})
    rodada("L-U2404", "20261118-193340",
           {"modo": "como-esta", "ate": "N3", "imagem": "ubuntu.wsl"},
           {"alcancado": "N0", "falhou": True, "impedida_por_versao": [], "sistema": {"nome": "Ubuntu 24.04.5 LTS"},
            "niveis": {"N1": {"estado": "falhou", "detalhe": "o MariaDB não respondeu | sem resposta — de novo\nsegunda linha", "segundos": 76.3},
                       "N2": nao_rodou, "N3": nao_rodou, "N4": nao_rodou}}, bom=True)
    rodada("L-ARCH", "20261119-162745", {"modo": "como-esta", "ate": "N1", "imagem": "arch.wsl"})
    rodada("M-15", "20261126-120000",
           {"modo": "novo", "ate": "N3", "imagem": "GitHub Actions: macOS ARM64",
            "actions": {"repositorio": "dono/repo", "commit": "a1b2c3d4e5f6" + "0" * 28, "execucao": "1", "tentativa": "1", "evento": "push"}},
           {"alcancado": "N2", "falhou": True, "impedida_por_versao": ["php"], "sistema": {"nome": "macOS"},
            "niveis": {"N1": {"estado": "passou", "detalhe": "", "segundos": 1.0},
                       "N2": {"estado": "falhou", "detalhe": "x" * 300, "segundos": 2.0},
                       "N3": nao_rodou, "N4": nao_rodou}})
    return celulas


def teste_relatorio_coleta_as_rodadas():
    rodadas = relatorio.coletar(_celulas_de_mentira())
    assert [(r["id"], r["rodada"]) for r in rodadas] == [
        ("L-ARCH", "20261119-162745"), ("L-U2404", "20261118-193340"), ("L-U2404", "20261119-094340"),
        ("M-15", "20261126-120000")], "ordem de id e de data"
    arch, velha, nova, mac = rodadas
    assert (arch["alcancado"], arch["falhou"], arch["niveis"], arch["primeira_falha"], arch["sistema"]) == ("sem prova", None, {}, "", "")
    assert (arch["origem"], arch["modo"], arch["ate"], arch["commit"]) == ("WSL", "como-esta", "N1", "")
    assert (velha["alcancado"], velha["falhou"], velha["sistema"]) == ("N0", True, "Ubuntu 24.04.5 LTS")
    assert velha["niveis"] == {"N1": "falhou", "N2": "nao_rodou", "N3": "nao_rodou", "N4": "nao_rodou"}
    assert velha["primeira_falha"] == "N1: o MariaDB não respondeu | sem resposta — de novo", velha["primeira_falha"]
    assert (nova["alcancado"], nova["falhou"], nova["primeira_falha"], nova["impedida_por_versao"]) == ("N3", False, "", [])
    assert (mac["origem"], mac["commit"], mac["impedida_por_versao"], mac["imagem"]) == ("GitHub Actions", "a1b2c3d4", ["php"], "GitHub Actions: macOS ARM64")
    assert mac["primeira_falha"] == "N2: " + "x" * 200, "o detalhe é cortado em 200 caracteres"
    assert relatorio.coletar(_pasta_temporaria() / "nao_existe") == []


def teste_relatorio_resume_por_celula():
    celulas = relatorio.por_celula(relatorio.coletar(_celulas_de_mentira()))
    assert [c["id"] for c in celulas] == ["L-ARCH", "L-U2404", "M-15"]
    u2404 = celulas[1]
    assert (u2404["rodadas"], u2404["origem"], u2404["sistema"]) == (2, "WSL", relatorio.CELULAS["L-U2404"][0])
    assert (u2404["primeira"]["rodada"], u2404["primeira"]["modo"], u2404["primeira"]["alcancado"]) == ("20261118-193340", "como-esta", "N0")
    assert u2404["primeira"]["primeira_falha"].startswith("N1: ")
    assert (u2404["ultima"]["rodada"], u2404["ultima"]["modo"], u2404["ultima"]["alcancado"], u2404["ultima"]["ate"]) == ("20261119-094340", "novo", "N3", "N3")
    assert celulas[0]["rodadas"] == 1 and celulas[0]["primeira"] == celulas[0]["ultima"]
    assert celulas[2]["origem"] == "GitHub Actions"
    for fixa in ("ALVO", "L-U2404", "L-U2404-SS", "L-U2204", "L-U2604", "L-D12", "L-D13", "L-F45", "L-ARCH", "L-SUSE",
                 "CI-UBU", "CI-WIN", "M-15", "M-15I"):
        assert fixa in relatorio.CELULAS and len(relatorio.CELULAS[fixa]) == 2, fixa
    assert relatorio.CELULAS["L-U2404-SS"][0] == "Ubuntu 24.04 sem systemd"
    assert [n[0] for n in relatorio.NAO_TESTADAS] == ["W11-SB", "W11-VM-D1", "W11-VM-D0", "WS22-VM", "L-U2404-VM", "W10-USADO"]


def teste_relatorio_blocos_em_markdown():
    rodadas = relatorio.coletar(_celulas_de_mentira())
    celulas = relatorio.por_celula(rodadas)
    resumo, matriz, cru, nao = (relatorio.bloco_resumo(celulas), relatorio.bloco_matriz(celulas),
                                relatorio.bloco_rodadas(rodadas), relatorio.bloco_nao_testadas())
    assert ("| Célula | Sistema | Como a máquina nasce | Onde rodou | Nível alcançado na última rodada | Prova pedida até | "
            "Maior nível em rodada novo |") in resumo
    assert "| L-U2404 | " in resumo and "| N3 | N3 | N3 |" in resumo
    assert f"| M-15 | macOS 15, Apple Silicon | {relatorio.CELULAS['M-15'][1]} | GitHub Actions | N2 | N3 | N2 |" in resumo
    assert "só a prova, sobre a instalação que já existia" in relatorio.CELULAS["ALVO"][1]
    assert "o instalador não rodou nesta célula" in relatorio.CELULAS["ALVO"][1]
    assert "| L-ARCH | " in resumo and "| sem prova | N1 | - |" in resumo, "sem rodada novo, a última coluna fica em -"
    assert "sem prova" in resumo, "a rodada sem registro.json"
    assert "ainda sem rodada" in resumo and "| CI-UBU |" in resumo, "célula da matriz que ainda não rodou"
    assert "GitHub Actions" in resumo and "WSL" in resumo
    assert "| Célula | Rodadas | Primeira rodada | Última rodada |" in matriz
    assert "20261118-193340" in matriz and "20261119-094340" in matriz
    assert "\\|" in matriz, "o `|` do erro literal não pode quebrar a tabela"
    assert "| Célula | Rodada | Onde | Modo | Até |" in cru and cru.count("\n| ") == 4, "uma linha por rodada"
    assert "a1b2c3d4" in cru and "php" in cru
    for nome in ("W11-SB", "W11-VM-D1", "W11-VM-D0", "WS22-VM", "L-U2404-VM", "W10-USADO", "decisão 153"):
        assert nome in nao, nome
    for texto in (resumo, matriz, cru, nao):
        assert "—" not in texto and "→" not in texto
        linhas = [linha for linha in texto.splitlines() if linha.startswith("|")]
        colunas = {linha.replace("\\|", "").count("|") for linha in linhas[:1]}
        assert all(linha.replace("\\|", "").count("|") in colunas for linha in linhas), "colunas diferentes na tabela"


def teste_relatorio_colar_troca_so_o_bloco():
    texto = "antes\n<!-- tb_inst_resumo:inicio -->\nvelho\n<!-- tb_inst_resumo:fim -->\ndepois\n<!-- tb_inst_outro:inicio -->\nx\n<!-- tb_inst_outro:fim -->\n"
    novo = relatorio.colar(texto, "resumo", "linha 1\nlinha 2")
    assert novo == ("antes\n<!-- tb_inst_resumo:inicio -->\nlinha 1\nlinha 2\n<!-- tb_inst_resumo:fim -->\ndepois\n"
                    "<!-- tb_inst_outro:inicio -->\nx\n<!-- tb_inst_outro:fim -->\n"), novo
    assert relatorio.colar(novo, "resumo", "linha 1\nlinha 2") == novo, "colar duas vezes dá o mesmo texto"
    assert relatorio.colar(texto.replace("\n", "\r\n"), "resumo", "a\nb") == texto.replace("\n", "\r\n").replace("velho", "a\r\nb")
    for ruim, pedaco in ((texto.replace("<!-- tb_inst_resumo:fim -->", ""), "fim"),
                         (texto.replace("<!-- tb_inst_resumo:inicio -->", ""), "início"),
                         (texto + texto, "mais de uma vez"),
                         ("sem marcas\n", "marcas")):
        try:
            relatorio.colar(ruim, "resumo", "x")
        except ValueError as e:
            assert pedaco in str(e), str(e)
        else:
            raise AssertionError(f"devia recusar: {pedaco}")
    # a marca de outro bloco não vale para este: `resumo` não encontra `nao_testadas`
    try:
        relatorio.colar(texto, "nao_testadas", "x")
    except ValueError:
        pass
    else:
        raise AssertionError("bloco sem marca devia ser recusado")


def teste_relatorio_rodada_que_nao_terminou_aparece_como_tal():
    celulas = _pasta_temporaria() / "celulas"
    pasta = celulas / "CI-WIN" / "20261126-120000"
    pasta.mkdir(parents=True)
    (pasta / "celula.json").write_text(json.dumps({"id": "CI-WIN", "modo": "como-esta", "ate": "N4", "terminou": False,
                                                   "actions": {"commit": "b" * 40}}), encoding="utf-8")
    antiga = celulas / "CI-UBU" / "20261126-120000"
    antiga.mkdir(parents=True)
    (antiga / "celula.json").write_text(json.dumps({"id": "CI-UBU", "modo": "novo", "ate": "N3", "actions": {}}), encoding="utf-8")
    rodadas = relatorio.coletar(celulas)
    win = [r for r in rodadas if r["id"] == "CI-WIN"][0]
    ubu = [r for r in rodadas if r["id"] == "CI-UBU"][0]
    assert win["alcancado"] == "não terminou" and ubu["alcancado"] == "sem prova", "rodada antiga sem a chave vale como terminada"
    resumo = relatorio.bloco_resumo(relatorio.por_celula(rodadas))
    assert "| não terminou |" in resumo
    assert "não terminou" in relatorio.bloco_matriz(relatorio.por_celula(rodadas))


def teste_relatorio_sincronizar_acusa_destino_sem_marca_e_o_check_acusa_diferenca():
    raiz = _pasta_temporaria()
    celulas = raiz / relatorio.CELULAS_RELATIVO
    celulas.parent.mkdir(parents=True)
    shutil.copytree(_celulas_de_mentira(), celulas)
    caminho_relatorio = raiz / relatorio.RELATORIO_RELATIVO
    caminho_relatorio.parent.mkdir(parents=True, exist_ok=True)
    marcas = "".join(f"<!-- tb_inst_{n}:inicio -->\nvelho\n<!-- tb_inst_{n}:fim -->\n" for n in ("resumo", "matriz", "rodadas", "nao_testadas"))
    caminho_relatorio.write_text("texto\n" + marcas + "fim\n", encoding="utf-8")
    (raiz / "README.md").write_text("README sem marcas\n", encoding="utf-8")
    (raiz / "DETALHES-TECNICOS.md").write_text("DETALHES com so uma marca\n<!-- tb_inst_resumo:inicio -->\nvelho\n<!-- tb_inst_resumo:fim -->\n", encoding="utf-8")
    diferencas, avisos = relatorio.sincronizar(raiz, gravar=False)
    assert any("matriz.json" in d for d in diferencas) and any("relatorio-instalador" in d and "resumo" in d for d in diferencas), diferencas
    assert not (raiz / relatorio.MATRIZ_RELATIVO).exists(), "--check não grava"
    assert any("README.md" in d and "resumo" in d and "marca" in d for d in diferencas), "destino sem marcas é diferença"
    assert any("DETALHES-TECNICOS.md" in d and "nao_testadas" in d and "marca" in d for d in diferencas)
    diferencas, avisos = relatorio.sincronizar(raiz, gravar=True)
    assert (raiz / relatorio.MATRIZ_RELATIVO).exists()
    matriz = json.loads((raiz / relatorio.MATRIZ_RELATIVO).read_text(encoding="utf-8"))
    assert matriz["tag_ia"]["alteracao"].startswith("! Alteração de IA - Revisar: ") and matriz["tag_ia"]["motivo"].startswith("! Motivo: ")
    assert len(matriz["rodadas"]) == 4 and matriz["rodadas"][0]["id"] == "L-ARCH"
    assert (raiz / "README.md").read_text(encoding="utf-8") == "README sem marcas\n", "sem marcas, o arquivo fica como está"
    detalhes = (raiz / "DETALHES-TECNICOS.md").read_text(encoding="utf-8")
    assert "velho" in detalhes and "L-U2404" not in detalhes, "faltou marca de um bloco: nada é gravado naquele arquivo"
    assert any("DETALHES-TECNICOS.md" in d and "nao_testadas" in d for d in diferencas), "o bloco sem marca continua acusado depois de colar"
    # o que falta de marca continua falta: o check segue acusando só os dois arquivos incompletos
    restantes, _ = relatorio.sincronizar(raiz, gravar=False)
    assert len([d for d in restantes if "sem as marcas" in d]) == 2, restantes
    # arquivo de destino que não existe também é diferença
    (raiz / "README.md").unlink()
    restantes, _ = relatorio.sincronizar(raiz, gravar=False)
    assert any("README.md" in d and "não existe" in d for d in restantes), restantes
    # com todas as marcas, depois de colar o check não acusa nada, e uma edição à mão no bloco é acusada
    (raiz / "README.md").write_text("README\n<!-- tb_inst_resumo:inicio -->\nvelho\n<!-- tb_inst_resumo:fim -->\n", encoding="utf-8")
    (raiz / "DETALHES-TECNICOS.md").write_text("D\n" + "".join(f"<!-- tb_inst_{n}:inicio -->\nv\n<!-- tb_inst_{n}:fim -->\n"
                                                              for n in ("resumo", "nao_testadas")), encoding="utf-8")
    relatorio.sincronizar(raiz, gravar=True)
    assert relatorio.sincronizar(raiz, gravar=False) == ([], []), "depois de colar, o check não acusa nada"
    caminho_relatorio.write_text(caminho_relatorio.read_text(encoding="utf-8").replace("L-ARCH", "L-OUTRA", 1), encoding="utf-8")
    diferencas, _ = relatorio.sincronizar(raiz, gravar=False)
    assert len(diferencas) == 1 and "relatorio-instalador" in diferencas[0], diferencas


def teste_relatorio_do_repositorio_bate_com_as_evidencias():
    diferencas, avisos = relatorio.sincronizar(RAIZ, gravar=False)
    assert diferencas == [] and avisos == [], "rode `python ferramentas/instalador_matriz/relatorio.py --colar`: " + "; ".join(diferencas + avisos)
    rodadas = relatorio.coletar(RAIZ / relatorio.CELULAS_RELATIVO)
    assert rodadas, "nenhuma rodada encontrada no repositório"
    for fixa in relatorio.CELULAS:
        if fixa.startswith(("L-", "ALVO")):
            assert any(r["id"] == fixa for r in rodadas), f"{fixa} devia ter rodada"


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
