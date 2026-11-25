# ! Alteração de IA - Revisar: arquivo novo (pacote I1 do instalador único): monta e grava o `registro.json`, a evidência de uma
# instalação: o sistema, a máquina, o estado de cada um dos quatro níveis da prova e a versão encontrada de cada ferramenta.
# ! Motivo: o plano aprovado (decisão 143) pede a evidência de cada célula em arquivo e o relatório gerado por script; até aqui
# a única prova de uma instalação era o texto que o `install.py` imprime, que termina em "Instalação concluída" mesmo quando o
# Ollama não foi instalado.
"""O registro da prova de uma instalação (seção 3.3 do plano). Só biblioteca padrão."""
import json
from datetime import datetime
from pathlib import Path

from instalador import versoes

NIVEIS = ("N1", "N2", "N3", "N4")
ESTADOS = ("passou", "falhou", "nao_coube", "nao_rodou")
TAG = {
    "alteracao": "! Alteração de IA - Revisar: arquivo gerado por instalador/conferir.py: a prova de uma instalação, nível a nível.",
    "motivo": "! Motivo: o plano do instalador único (decisão 143) pede a evidência de cada célula de teste em arquivo, com o erro literal "
              "de cada falha, para o relatório sair de script e não de memória.",
}


def novo(celula: str, sistema: dict, maquina: dict) -> dict:
    """Um registro em branco: os quatro níveis como 'nao_rodou'."""
    return {"tag_ia": TAG, "celula": celula, "gravado_em": datetime.now().isoformat(timespec="seconds"),
            "sistema": sistema, "maquina": maquina,
            "niveis": {n: {"estado": "nao_rodou", "detalhe": "", "segundos": None} for n in NIVEIS}, "versoes": {}}


def anotar_nivel(reg: dict, nivel: str, estado: str, detalhe: str = "", segundos: float | None = None) -> None:
    """Grava o estado de um nível; o detalhe leva o erro literal quando falha."""
    if nivel not in NIVEIS or estado not in ESTADOS:
        raise ValueError(f"nível ou estado desconhecido: {nivel!r}, {estado!r}")
    reg["niveis"][nivel] = {"estado": estado, "detalhe": detalhe, "segundos": segundos}


def anotar_versoes(reg: dict, encontradas: dict[str, str], ferramentas: dict, reproduzir: bool = False) -> None:
    """A versão encontrada de cada ferramenta contra o versoes.json."""
    reg["versoes"] = versoes.julgar(encontradas, ferramentas, reproduzir=reproduzir)


def alcancado(reg: dict) -> str:
    """O último nível de uma sequência sem falha desde o N1: 'N0' se nem o N1 passou."""
    ultimo = "N0"
    for nivel in NIVEIS:
        if reg["niveis"][nivel]["estado"] != "passou":
            break
        ultimo = nivel
    return ultimo


def falhou(reg: dict) -> bool:
    """Verdadeiro se algum nível falhou. 'nao_coube' (memória) e 'nao_rodou' não contam como falha do instalador."""
    return any(n["estado"] == "falhou" for n in reg["niveis"].values())


# ! Alteração de IA - Revisar: função nova `impedida_por_versao`, e o `gravar` passa a gravar `impedida_por_versao` no registro.json.
# ! Motivo: o registro só dizia se um nível falhou; uma ferramenta fora da faixa do versoes.json (ou, com --reproduzir, diferente
# da testada) ficava escondida dentro de `versoes` e a prova saía com código 0 mesmo assim.
def impedida_por_versao(reg: dict) -> list[str]:
    """As ferramentas cuja versão impede seguir, em ordem alfabética."""
    return sorted(nome for nome, dados in reg["versoes"].items() if dados.get("impede"))


def gravar(reg: dict, pasta: Path) -> Path:
    """Grava `registro.json` na pasta, com o nível alcançado e a falha já calculados, e devolve o caminho."""
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = pasta / "registro.json"
    extra = {"alcancado": alcancado(reg), "falhou": falhou(reg), "impedida_por_versao": impedida_por_versao(reg)}
    caminho.write_text(json.dumps({**reg, **extra}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    return caminho
