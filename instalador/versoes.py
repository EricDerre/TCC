# ! Alteração de IA - Revisar: arquivo novo (pacote I1 do instalador único, decisão 139): lê o `versoes.json` da raiz e compara
# a versão encontrada de cada ferramenta com a versão que o projeto testou e com a faixa que ele aceita.
# ! Motivo: o instalador só escolhia a versão do Playwright e a série do MariaDB no Windows; o Ollama se atualiza sozinho (17
# versões estáveis entre 25/09 e 09/11/2026) e o PHP e o MariaDB mudam conforme a distribuição. Sem um registro só, quem instala
# meses depois recebe uma combinação que ninguém testou e o instalador não avisa.
"""Versões testadas e faixas aceitas (decisão 139). Só biblioteca padrão; não instala nada."""
import json
import re
import sys
from pathlib import Path


# ! Alteração de IA - Revisar: (25/11/2026, consertos da revisão depois da primeira execução do Actions) função nova `raiz_do_projeto`: a pasta do executável quando o programa está compilado pelo PyInstaller (`Cobaia.exe`, que fica na raiz do projeto, ao lado do `versoes.json`) e a pasta de cima de `instalador/` nos outros casos; `RAIZ` passa a vir dela.
# ! Motivo: o `Cobaia.py` chama `install.main()` de dentro do executável, e lá `__file__` aponta para a pasta temporária de extração (`%TEMP%\_MEIxxxx`), onde não há `versoes.json`: `versoes.carregar()` no passo do Ollama (`install.setup_agente_core`) levantaria `FileNotFoundError`, que o `install.main` não trata, e a instalação pelo executável pararia com um erro do Python depois de já ter instalado PHP, MariaDB e as venvs. Mesma regra que o `_env_common.REPO_ROOT` já usa. Não rodei nem compilei o `Cobaia.exe`.
def raiz_do_projeto(congelado: bool | None = None, executavel: str | None = None, arquivo: str | None = None) -> Path:
    """A raiz do projeto: a pasta do executável quando o programa está compilado (`sys.frozen`), senão a pasta de cima de
    `instalador/`. Os três parâmetros só existem para o teste trocar o que `sys` e `__file__` diriam."""
    if congelado is None:
        congelado = bool(getattr(sys, "frozen", False))
    if congelado:
        return Path(executavel or sys.executable).resolve().parent
    return Path(arquivo or __file__).resolve().parent.parent


RAIZ = raiz_do_projeto()
ARQUIVO = RAIZ / "versoes.json"
ALVOS_UV = ("windows-x86_64", "linux-x86_64", "linux-aarch64", "macos-aarch64", "macos-x86_64")


def versao_tupla(versao: str) -> tuple[int, ...]:
    """A primeira sequência de números com ponto do texto: 'PHP 8.2.35 (cli)' vira (8, 2, 35); texto sem número vira ()."""
    achado = re.search(r"\d+(?:\.\d+)*", versao or "")
    return tuple(int(p) for p in achado.group().split(".")) if achado else ()


def _dentro(tupla: tuple[int, ...], limite: str, piso: bool) -> bool:
    """Compara só os componentes que o limite traz: o teto '8.5' aceita 8.5.12; limite vazio não limita."""
    if not limite:
        return True
    lim = versao_tupla(limite)
    corte = tupla[:len(lim)]
    return corte >= lim if piso else corte <= lim


def comparar(encontrada: str, registro: dict) -> str:
    """'igual' à testada, 'na_faixa' aceita, 'fora_da_faixa', ou 'desconhecida' quando não há número para ler."""
    tupla = versao_tupla(encontrada)
    if not tupla:
        return "desconhecida"
    if tupla == versao_tupla(registro.get("testada", "")):
        return "igual"
    if _dentro(tupla, registro.get("aceita_de", ""), piso=True) and _dentro(tupla, registro.get("aceita_ate", ""), piso=False):
        return "na_faixa"
    return "fora_da_faixa"


def comparar_identificador(encontrado: str, registro: dict) -> str:
    """Para o modelo: o identificador é o começo do SHA-256 do manifesto (o que `ollama list` mostra); vale o prefixo."""
    if not encontrado:
        return "desconhecida"
    curto, longo = sorted((encontrado.lower(), registro.get("testada", "").lower()), key=len)
    return "igual" if curto and longo.startswith(curto) else "fora_da_faixa"


def julgar(encontradas: dict[str, str], ferramentas: dict, reproduzir: bool = False) -> dict:
    """O estado de cada ferramenta encontrada e se ele impede seguir. Modo normal: só 'fora_da_faixa' impede.
    Com reproduzir=True (quem repete as medidas do TCC), nas ferramentas com `afeta_medida` só 'igual' passa."""
    saida = {}
    for nome, reg in ferramentas.items():
        if nome not in encontradas:
            continue
        achada = encontradas[nome]
        estado = comparar_identificador(achada, reg) if reg.get("identificador") else comparar(achada, reg)
        exata = reproduzir and reg.get("afeta_medida", False)
        saida[nome] = {"encontrada": achada, "testada": reg.get("testada", ""), "estado": estado,
                       "impede": estado == "fora_da_faixa" or (exata and estado != "igual")}
    return saida


def carregar(caminho: Path = ARQUIVO) -> dict:
    """O bloco `ferramentas` do versoes.json."""
    return json.loads(Path(caminho).read_text(encoding="utf-8"))["ferramentas"]


def gerar_uv_fixado(ferramentas: dict) -> str:
    """O texto de `instalador/uv_fixado.txt`: linhas CHAVE=valor, só ASCII, fim de linha do Linux."""
    uv, py = ferramentas["uv"], ferramentas["python"]
    linhas = [
        "# ! Alteracao de IA - Revisar: arquivo gerado por ferramentas/instalador_matriz/atualizar_versoes.py a partir do versoes.json; nao editar a mao.",
        "# ! Motivo: os lancadores install.ps1 e install.sh precisam da versao do uv e do SHA-256 de cada sistema antes de existir um Python para ler o versoes.json. Sem acento de proposito: o arquivo e lido pelo PowerShell 5.1 e pelo shell.",
        f"UV_VERSAO={uv['testada']}",
        f"PYTHON_VERSAO={'.'.join(py['testada'].split('.')[:2])}",
        f"PYTHON_MINIMO={py['aceita_de']}",
    ]
    for alvo in ALVOS_UV:
        chave = alvo.upper().replace("-", "_")
        linhas.append(f"UV_{chave}_URL={uv['downloads'][alvo]['url']}")
        linhas.append(f"UV_{chave}_SHA256={uv['downloads'][alvo]['sha256']}")
    return "\n".join(linhas) + "\n"
