#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (pacote I1 do instalador único, decisão 139): preenche e confere o `versoes.json`
# da raiz e o `instalador/uv_fixado.txt`, copiando cada versão testada do arquivo em que o projeto a registrou.
# ! Motivo: a regra do projeto é não digitar número. A versão do Ollama vem das pontes (`pontes.json`), a do Playwright do
# `requirements.txt`, a do MariaDB e a do Chromium do `ambiente.json`, o identificador do modelo do manifesto que o Ollama
# grava no disco; sem o script, o `versoes.json` seria escrito à mão e envelheceria sem ninguém perceber.
"""Uso: python ferramentas/instalador_matriz/atualizar_versoes.py --local | --hashes | --check
--local   regrava versoes.json e uv_fixado.txt com as fontes desta máquina (não usa a rede; mantém os SHA-256 já gravados)
--hashes  busca na release do uv o SHA-256 de cada sistema (usa a rede) e regrava os dois arquivos
--check   não grava nada: sai com código 1 se algum dos dois arquivos difere do que as fontes do repositório dizem"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from instalador import versoes

EXP = RAIZ / "Programacao" / "AgenteCore" / "experimentos"
# A versão do uv é escolha do projeto, não medida: era a release mais recente em 18/11/2026
# (Documentacao/memorial/5-metodo-e-ferramental/dados/instalador/pesquisa-versoes-linux.md, seção 8).
UV_VERSAO = "0.13.9"
ARQUIVOS_UV = {
    "windows-x86_64": "uv-x86_64-pc-windows-msvc.zip",
    "linux-x86_64": "uv-x86_64-unknown-linux-gnu.tar.gz",
    "linux-aarch64": "uv-aarch64-unknown-linux-gnu.tar.gz",
    "macos-aarch64": "uv-aarch64-apple-darwin.tar.gz",
    "macos-x86_64": "uv-x86_64-apple-darwin.tar.gz",
}
# A política da decisão 139. As faixas são o que a matriz de testes vai conferir, não uma promessa:
# quando uma célula mostrar que uma versão não serve, a faixa é estreitada aqui.
POLITICA = {
    "python": {"aceita_de": "3.12", "aceita_ate": "", "afeta_medida": False},
    "php": {"aceita_de": "8.1", "aceita_ate": "8.5", "afeta_medida": False},
    "mariadb": {"aceita_de": "10.6", "aceita_ate": "13.0", "afeta_medida": False},
    "playwright": {"exata": True, "afeta_medida": True},
    "chromium": {"exata": True, "afeta_medida": True},
    "ollama": {"aceita_ate": "", "afeta_medida": True},
    "modelo": {"identificador": True, "afeta_medida": True, "nome": "qwen2.5:7b"},
}
TAG = {
    "alteracao": "! Alteração de IA - Revisar: arquivo novo (pacote I1 do instalador único, decisão 139): a versão que o projeto testou e a faixa que ele "
                 "aceita de cada ferramenta, gerado por ferramentas/instalador_matriz/atualizar_versoes.py; não editar à mão.",
    "motivo": "! Motivo: o instalador só escolhia a versão do Playwright e a série do MariaDB no Windows; o Ollama se atualiza sozinho e o "
              "PHP e o MariaDB mudam conforme o sistema. Com o registro, o instalador instala a versão testada quando a "
              "ferramenta falta, avisa quando a encontrada é outra e, no modo --reproduzir, exige a exata.",
}


def ollama_das_pontes(pontes: dict) -> dict:
    """A ponte pareável mais recente é a versão testada; o piso é a menor versão pareável da mesma série (os dois primeiros números)."""
    boas = [p for p in pontes.get("pontes", []) if p.get("pareavel")]
    ultima = max(boas, key=lambda p: (p.get("data", ""), versoes.versao_tupla(p["versao"])))
    serie = versoes.versao_tupla(ultima["versao"])[:2]
    da_serie = [p["versao"] for p in boas if versoes.versao_tupla(p["versao"])[:2] == serie]
    return {"testada": ultima["versao"], "aceita_de": min(da_serie, key=versoes.versao_tupla)}


def playwright_do_requirements(texto: str) -> str:
    return re.search(r"^playwright==([\w.]+)\s*$", texto, flags=re.MULTILINE).group(1)


def python_da_venv(cfg: str) -> str:
    return re.search(r"^version\s*=\s*([\d.]+)", cfg, flags=re.MULTILINE).group(1)


def mariadb_do_ambiente(ambiente: dict) -> str:
    return re.search(r"mariadb-(\d+\.\d+\.\d+)-winx64", ambiente["cobaias"]["mariadbd"]).group(1)


def chromium_do_ambiente(ambiente: dict) -> str:
    return ambiente["versoes"]["navegador"]


def php_da_saida(saida: str) -> str:
    return re.match(r"PHP (\d+\.\d+\.\d+)", saida).group(1)


def modelo_do_manifesto(bruto: bytes) -> dict:
    """O identificador que `ollama list` mostra é o começo do SHA-256 do arquivo de manifesto; os pesos são a camada `model`."""
    pesos = next(c for c in json.loads(bruto)["layers"] if c["mediaType"] == "application/vnd.ollama.image.model")
    return {"testada": hashlib.sha256(bruto).hexdigest()[:12],
            "pesos_sha256": pesos["digest"].removeprefix("sha256:"), "pesos_bytes": pesos["size"]}


def coletar_do_repositorio(raiz: Path) -> dict:
    """As versões cuja fonte está no git: Ollama, Playwright, MariaDB e Chromium."""
    exp = raiz / "Programacao" / "AgenteCore" / "experimentos"
    ambiente = json.loads((exp / "resultados_alvo" / "fase4" / "ambiente.json").read_text(encoding="utf-8"))
    pontes = json.loads((exp / "resultados_alvo" / "fase4" / "pontes.json").read_text(encoding="utf-8"))
    return {
        "ollama": {**ollama_das_pontes(pontes), "origem": "resultados_alvo/fase4/pontes.json (última ponte pareável)"},
        "playwright": {"testada": playwright_do_requirements((exp.parent / "requirements.txt").read_text(encoding="utf-8")),
                       "origem": "Programacao/AgenteCore/requirements.txt"},
        "mariadb": {"testada": mariadb_do_ambiente(ambiente), "origem": "resultados_alvo/fase4/ambiente.json (cobaias.mariadbd)"},
        "chromium": {"testada": chromium_do_ambiente(ambiente), "origem": "resultados_alvo/fase4/ambiente.json (versoes.navegador)"},
    }


def coletar_da_maquina(raiz: Path) -> dict:
    """As versões cuja fonte só existe na máquina-alvo: Python da venv, PHP em uso e o manifesto do modelo. O que faltar fica de fora."""
    saida = {}
    cfg = raiz / "Programacao" / "AgenteCore" / ".venv" / "pyvenv.cfg"
    if cfg.exists():
        saida["python"] = {"testada": python_da_venv(cfg.read_text(encoding="utf-8")),
                           "origem": "Programacao/AgenteCore/.venv/pyvenv.cfg (version), na máquina-alvo"}
    import _env_common as env
    php = env.find_php()
    if php:
        r = subprocess.run([php, "-v"], capture_output=True, text=True, check=False)
        if r.returncode == 0:
            saida["php"] = {"testada": php_da_saida(r.stdout), "origem": "php -v do executável em uso na máquina-alvo"}
    manifesto = Path.home() / ".ollama" / "models" / "manifests" / "registry.ollama.ai" / "library" / "qwen2.5" / "7b"
    if manifesto.exists():
        saida["modelo"] = {**modelo_do_manifesto(manifesto.read_bytes()),
                           "origem": "manifesto do qwen2.5:7b gravado pelo Ollama no disco da máquina-alvo"}
    return saida


def montar(locais: dict, anterior: dict | None) -> dict:
    """Junta as fontes com a política; o que não tem fonte nesta máquina e o que veio da rede (uv) ficam como estavam."""
    antes = (anterior or {}).get("ferramentas", {})
    ferramentas = {}
    for nome, politica in POLITICA.items():
        local = locais.get(nome)
        if local is None:
            if nome in antes:
                ferramentas[nome] = antes[nome]
            continue
        reg = {"testada": local["testada"]}
        if politica.get("identificador"):
            reg.update({"identificador": True, "nome": politica["nome"],
                        "pesos_sha256": local["pesos_sha256"], "pesos_bytes": local["pesos_bytes"]})
        elif politica.get("exata"):
            reg.update({"aceita_de": local["testada"], "aceita_ate": local["testada"]})
        else:
            reg.update({"aceita_de": local.get("aceita_de", politica.get("aceita_de", "")), "aceita_ate": politica["aceita_ate"]})
        reg.update({"afeta_medida": politica["afeta_medida"], "origem": local["origem"]})
        ferramentas[nome] = reg
    uv = dict(antes.get("uv", {}))
    uv.update({"testada": UV_VERSAO, "afeta_medida": False, "origem": "release do uv no GitHub (astral-sh/uv)"})
    uv.setdefault("downloads", {})
    ferramentas["uv"] = uv
    return {"tag_ia": TAG, "gravado_em": datetime.now().isoformat(timespec="seconds"), "ferramentas": ferramentas}


def baixar_hashes_uv(versao: str = UV_VERSAO) -> dict:
    """Busca o arquivo `.sha256` que a release do uv publica para cada sistema. Usa a rede."""
    base = f"https://github.com/astral-sh/uv/releases/download/{versao}/"
    saida = {}
    for alvo, arquivo in ARQUIVOS_UV.items():
        pedido = urllib.request.Request(base + arquivo + ".sha256", headers={"User-Agent": "cobaia-install"})
        with urllib.request.urlopen(pedido, timeout=60) as resposta:
            sha = resposta.read().decode("ascii").split()[0].lower()
        if not re.fullmatch(r"[0-9a-f]{64}", sha):
            raise ValueError(f"SHA-256 inesperado para {arquivo}: {sha!r}")
        saida[alvo] = {"url": base + arquivo, "sha256": sha}
    return saida


def _gravar(dados: dict) -> None:
    versoes.ARQUIVO.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    faltam = [a for a in versoes.ALVOS_UV if a not in dados["ferramentas"]["uv"]["downloads"]]
    if faltam:
        print(f"uv_fixado.txt não gravado: faltam os SHA-256 de {faltam}; rode com --hashes")
        return
    (RAIZ / "instalador" / "uv_fixado.txt").write_text(versoes.gerar_uv_fixado(dados["ferramentas"]), encoding="ascii", newline="\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--local", action="store_true")
    grupo.add_argument("--hashes", action="store_true")
    grupo.add_argument("--check", action="store_true")
    args = ap.parse_args()
    anterior = json.loads(versoes.ARQUIVO.read_text(encoding="utf-8")) if versoes.ARQUIVO.exists() else None
    if args.check:
        erros = []
        gravadas = (anterior or {}).get("ferramentas", {})
        for nome, local in coletar_do_repositorio(RAIZ).items():
            if gravadas.get(nome, {}).get("testada") != local["testada"]:
                erros.append(f"{nome}: versoes.json diz {gravadas.get(nome, {}).get('testada')!r}, a fonte diz {local['testada']!r}")
        fixado = RAIZ / "instalador" / "uv_fixado.txt"
        completo = "uv" in gravadas and "python" in gravadas and all(a in gravadas["uv"].get("downloads", {}) for a in versoes.ALVOS_UV)
        if not completo:
            erros.append("versoes.json não existe ou não tem o uv com os SHA-256 de todos os sistemas; rode com --hashes")
        elif not fixado.exists() or fixado.read_text(encoding="ascii") != versoes.gerar_uv_fixado(gravadas):
            erros.append("instalador/uv_fixado.txt difere do versoes.json")
        for erro in erros:
            print("DIFERENÇA:", erro)
        print("--check:", "ok" if not erros else f"{len(erros)} diferença(s)")
        return 1 if erros else 0
    locais = {**coletar_do_repositorio(RAIZ), **coletar_da_maquina(RAIZ)}
    dados = montar(locais, anterior)
    if args.hashes:
        dados["ferramentas"]["uv"]["downloads"] = baixar_hashes_uv()
    _gravar(dados)
    for nome, reg in dados["ferramentas"].items():
        print(f"{nome}: testada {reg['testada']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
