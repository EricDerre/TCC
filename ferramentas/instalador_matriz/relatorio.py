#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (25/11/2026, pacote I7 do instalador único, decisões 143 e 153): lê todas as pastas de rodada de
# `Documentacao/memorial/5-metodo-e-ferramental/dados/instalador/celulas/<id>/<data-hora>/` (o `celula.json` e, quando existe, o
# `registro.json`), grava `dados/instalador/matriz.json` (uma linha por rodada) e cola quatro tabelas (`resumo`, `matriz`, `rodadas`,
# `nao_testadas`) entre as marcas do relatório do instalador, do README e do DETALHES-TECNICOS.
# ! Motivo: o README prometia Windows, Linux e macOS, e a prova gravada cobria só o Windows da máquina-alvo e o Linux pelo WSL. Quem escreve "passou
# até o N3" à mão erra o nível ou esquece uma rodada nova (as do GitHub Actions chegam depois, por `importar_actions.py`); com este roteiro o nível
# de cada célula, a primeira falha e a lista do que não foi testado saem dos arquivos de evidência, e `--check` (e a bateria) acusam quando
# o texto ficou para trás.
"""Uso, na raiz do repositório:
  python ferramentas/instalador_matriz/relatorio.py --colar    grava matriz.json e cola os blocos nos arquivos de DESTINOS
  python ferramentas/instalador_matriz/relatorio.py --check    não grava nada; sai com 1 se algum bloco ou o matriz.json difere
Todo arquivo de DESTINOS tem de existir e ter as marcas de todos os seus blocos: faltando uma marca, o `--check` acusa e o `--colar`
não grava nada naquele arquivo e sai com 1. Só biblioteca padrão."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CELULAS_RELATIVO = Path("Documentacao/memorial/5-metodo-e-ferramental/dados/instalador/celulas")
MATRIZ_RELATIVO = Path("Documentacao/memorial/5-metodo-e-ferramental/dados/instalador/matriz.json")
RELATORIO_RELATIVO = Path("Documentacao/memorial/5-metodo-e-ferramental/relatorio-instalador-maquina-limpa.md")
NIVEIS = ("N1", "N2", "N3", "N4")
LIMITE_DA_FALHA = 200

# Cada arquivo e os blocos que ele recebe. As marcas são `<!-- tb_inst_<bloco>:inicio -->` e `<!-- tb_inst_<bloco>:fim -->`.
DESTINOS = {
    # ! Alteração de IA - Revisar: (26/11/2026, decisão 180) o relatório e o DETALHES passam a receber os blocos `limites` e `futuro`, e o README o bloco `limites_curto`.
    # ! Motivo: o dono do projeto pediu que os sistemas em que o instalador não foi provado até o fim fiquem declarados como limitação e como trabalho futuro, e a tabela do resumo não dizia que uma célula que alcançou o N3 pedindo N3 também é um limite, nem que no Mac Intel a prova passou com o instalador interrompido; gerados das pastas de rodada, os blocos não ficam para trás.
    RELATORIO_RELATIVO: ("resumo", "matriz", "rodadas", "nao_testadas", "limites", "futuro"),
    Path("README.md"): ("resumo", "limites_curto"),
    Path("DETALHES-TECNICOS.md"): ("resumo", "nao_testadas", "limites", "futuro"),
}

# ! Alteração de IA - Revisar: tabela fixa das células da matriz do plano (seções 4.1 e 4.2), com o sistema e como a máquina nasce.
# ! Motivo: o relatório precisa mostrar também a célula que ainda não rodou (as quatro do GitHub Actions antes do primeiro push) e dar a cada id um
# nome que uma pessoa entende; o `registro.json` só traz o sistema depois de a prova rodar, e as rodadas do Arch e do openSUSE no modo `como-esta` nem têm registro.
# ! Alteração de IA - Revisar: o texto da célula `ALVO` passa a dizer que o instalador não rodou nela, só a prova.
# ! Motivo: a tabela do README listava a `ALVO` ao lado das máquinas novas e a leitura natural era que o instalador também rodou nela; na `ALVO` só a prova da instalação rodou, sobre a instalação que já existia na máquina do projeto.
CELULAS = {
    "ALVO": ("Windows 11 da máquina-alvo",
             "a máquina do projeto como está: o instalador não rodou nesta célula, só a prova, sobre a instalação que já existia"),
    "L-U2404": ("Ubuntu 24.04", "WSL: imagem oficial importada e apagada no fim"),
    "L-U2404-SS": ("Ubuntu 24.04 sem systemd", "WSL: imagem oficial, com o systemd desligado na instância"),
    "L-U2204": ("Ubuntu 22.04", "WSL: imagem oficial importada e apagada no fim"),
    "L-U2604": ("Ubuntu 26.04", "WSL: imagem oficial importada e apagada no fim"),
    "L-D12": ("Debian 12", "WSL: imagem oficial importada e apagada no fim"),
    "L-D13": ("Debian 13", "WSL: imagem oficial importada e apagada no fim"),
    "L-F45": ("Fedora 45 (melhor esforço)", "WSL: imagem oficial importada e apagada no fim"),
    "L-ARCH": ("Arch Linux (sem suporte)", "WSL: imagem oficial importada e apagada no fim"),
    "L-SUSE": ("openSUSE (sem suporte)", "WSL: imagem oficial importada e apagada no fim"),
    # ! Alteração de IA - Revisar: (25/11/2026, consertos da primeira execução do Actions) o texto da `CI-UBU` passa a dizer que o executor vem com o MySQL 8.0 e que a célula o remove antes do instalador.
    # ! Motivo: na execução 45650086543 o `apt-get install --no-remove ... mariadb-server` parou com "Packages need to be removed but remove is disabled" por causa do MySQL 8.0 do executor; a decisão do dono do projeto foi a célula tirá-lo antes (preparo `remover-mysql`), e a tabela do README tem de dizer que esta máquina é alterada antes da instalação.
    "CI-UBU": ("Ubuntu 24.04 do GitHub Actions",
               "executor do GitHub; já traz Python, PHP e o MySQL 8.0, e a célula remove o MySQL antes do instalador; não é limpo"),
    "CI-WIN": ("Windows Server 2025 do GitHub Actions", "executor do GitHub; já traz Python, PHP e banco, não é limpo"),
    "M-15": ("macOS 15, Apple Silicon", "executor do GitHub; já traz o Homebrew e o Python, não é limpo"),
    # ! Alteração de IA - Revisar: (25/11/2026, consertos da primeira execução do Actions, tarefa E) o sistema da `M-15I` passa a dizer "macOS 15, Intel (melhor esforço)", como o Fedora.
    # ! Motivo: decisão do dono do projeto de 25/11/2026 ("Melhor esforço, célula fica"): nos arquivos públicos do Homebrew (`Formula/p/php.rb`, `Formula/m/mariadb.rb`, `Formula/m/mariadb@11.8.rb`) o bloco `bottle` só traz pacote pronto de macOS para Apple Silicon; num Mac Intel o `brew install` compila do código-fonte e pode levar mais de uma hora. A tabela do README tem de dizer que esta célula não é garantida. Nada disso foi observado em execução ainda.
    "M-15I": ("macOS 15, Intel (melhor esforço)", "executor do GitHub; já traz o Homebrew e o Python, não é limpo"),
}

# ! Alteração de IA - Revisar: lista fixa do que a decisão 153 deixou sem teste, com o motivo de cada uma.
# ! Motivo: o README e o DETALHES precisam dizer o que NÃO foi provado, e essa lista tem de vir do mesmo lugar do resumo, para as duas não se contradizerem.
_MOTIVO_153 = "decisão 153 (25/11/2026): a prova em máquina nova antes da entrega é a do GitHub Actions"
NAO_TESTADAS = [
    ("W11-SB", "Windows 11 no Windows Sandbox",
     f"{_MOTIVO_153}; esta pedia ligar um recurso do Windows e reiniciar a máquina do projeto"),
    ("W11-VM-D1", "Windows 11 Enterprise de avaliação em máquina virtual, com o Defender ligado",
     f"{_MOTIVO_153}; esta pedia baixar a imagem de avaliação e criar uma máquina virtual no Hyper-V"),
    ("W11-VM-D0", "Windows 11 Enterprise de avaliação em máquina virtual, com o Defender desligado",
     f"{_MOTIVO_153}; esta pedia baixar a imagem de avaliação e criar uma máquina virtual no Hyper-V"),
    ("WS22-VM", "Windows Server 2022 de avaliação em máquina virtual",
     f"{_MOTIVO_153}; esta pedia baixar a imagem de avaliação e criar uma máquina virtual no Hyper-V"),
    ("L-U2404-VM", "Ubuntu 24.04 de mesa em máquina virtual",
     f"{_MOTIVO_153}; esta pedia baixar a imagem do Ubuntu de mesa e criar uma máquina virtual no Hyper-V"),
    ("W10-USADO", "Windows 10 de um integrante",
     f"{_MOTIVO_153}; esta pedia o computador de um integrante"),
]

# ! Alteração de IA - Revisar: (26/11/2026, decisão 180) lista fixa de situações que nenhuma célula da matriz exercita, com o motivo de cada uma, para o bloco de trabalho futuro.
# ! Motivo: o dono do projeto pediu que o que falta provar fique declarado; estas quatro situações não têm célula nem entram em `NAO_TESTADAS` (que é só o que a decisão 153 cortou), e são texto descritivo, sem número de resultado, para não envelhecer.
SEM_CELULA = [
    ("O MariaDB instalado pelo MSI do `winget`, no Windows com administrador e sem MySQL",
     "a célula do Windows usa o zip portátil do MariaDB; o outro caminho não foi exercitado em máquina nova"),
    ("O Python e o PHP trazidos pelo `winget`, no Windows", "a máquina do GitHub já traz os dois"),
    ("Um Mac sem o Homebrew", "a máquina do GitHub já traz o Homebrew"),
    ("Windows e Linux em processador ARM", "nenhuma célula da matriz roda nesses processadores"),
]


# ! Alteração de IA - Revisar: bloco de funções de leitura (`_limpo`, `_ler_json`, `origem_do_id`, `_primeira_falha`): `_limpo` põe o texto numa linha sem travessão, seta nem `|` solto; `_ler_json` lê um JSON ou devolve None; `origem_do_id` diz onde a célula rodou (GitHub Actions, WSL ou máquina-alvo); `_primeira_falha` acha o primeiro nível que falhou e a primeira linha do detalhe.
# ! Motivo: o texto de uma falha vem do log da máquina e pode trazer quebra de linha, travessão (regra do projeto: não entra em documento) ou `|` (que quebraria a tabela em Markdown); e um `celula.json` ou `registro.json` ilegível não pode derrubar o relatório inteiro.
def _limpo(texto: object) -> str:
    """O texto numa linha só, sem travessão nem seta (regra do projeto para os documentos) e sem `|` solto, que quebraria a tabela."""
    t = " ".join(str(texto).split())
    t = t.replace("—", "-").replace("–", "-").replace("→", "para").replace("->", "para")
    return t.replace("|", "\\|")


def _ler_json(caminho: Path) -> dict | None:
    """O JSON do arquivo, ou None se o arquivo não existe ou não é JSON válido."""
    if not caminho.exists():
        return None
    try:
        return json.loads(caminho.read_text(encoding="utf-8-sig"))
    except ValueError:
        return None


def origem_do_id(ident: str, celula: dict | None = None) -> str:
    """Onde a célula rodou: `GitHub Actions` se o `celula.json` tem a chave `actions` (ou o id é de uma célula do GitHub), `WSL` para os ids `L-...`, `máquina-alvo` para `ALVO`."""
    if celula is not None and "actions" in celula:
        return "GitHub Actions"
    if ident.startswith("L-"):
        return "WSL"
    if ident == "ALVO":
        return "máquina-alvo"
    if ident.startswith(("CI-", "M-")):
        return "GitHub Actions"
    return ""


def _primeira_falha(niveis: dict) -> str:
    """O primeiro nível que falhou e a primeira linha do seu detalhe (cortada em LIMITE_DA_FALHA caracteres); vazio se nenhum falhou."""
    for nivel in NIVEIS:
        dados = niveis.get(nivel) or {}
        if dados.get("estado") == "falhou":
            linhas = str(dados.get("detalhe", "")).strip().splitlines()
            return f"{nivel}: {linhas[0].strip()[:LIMITE_DA_FALHA] if linhas else ''}"
    return ""


# ! Alteração de IA - Revisar: `coletar` passa a guardar `terminou` de cada rodada e a pôr "não terminou" no lugar do nível quando o `celula.json` diz `"terminou": false`.
# ! Motivo: a célula do GitHub grava o `celula.json` no começo, com `terminou` falso, e regrava no fim; uma tarefa cortada pelo GitHub fica só com a primeira versão, e o relatório não pode apresentá-la como "sem prova" comum nem como nível alcançado. Rodada antiga, sem a chave, vale como terminada.
# ! Alteração de IA - Revisar: (26/11/2026, decisão 180) `_estado_do_instalador` diz, do `celula.json`, se o instalador `concluído`, `interrompido` ou `não rodou` naquela rodada; `coletar` guarda o resultado no campo `instalador`.
# ! Motivo: a tabela do resumo só mostrava o nível da prova, e no Mac Intel (`M-15I`) a prova passou com o instalador interrompido (código de saída 1 em `saidas.instalador`); sem este campo, "provado até o fim" não distingue isso. A célula `ALVO` só roda a prova e não grava código do instalador: é `não rodou`.
def _estado_do_instalador(celula: dict) -> str:
    """`concluído`, `interrompido` ou `não rodou`, lido do `celula.json`: `resultado_do_instalador` (células do GitHub Actions: `concluida` ou outro valor) ou, sem ele, os códigos de saída `saidas.instalador` e `saidas.install*`."""
    resultado = celula.get("resultado_do_instalador")
    if resultado:
        return "concluído" if resultado == "concluida" else "interrompido"
    saidas = celula.get("saidas") or {}
    codigos = [str(v).strip() for k, v in saidas.items() if k == "instalador" or k.startswith("install")]
    if not codigos:
        return "não rodou"
    return "concluído" if all(c == "0" for c in codigos) else "interrompido"


def coletar(celulas: Path) -> list[dict]:
    """Uma entrada por pasta de rodada que tem `celula.json`, em ordem de id e de data."""
    caminhos = sorted(celulas.glob("*/*/celula.json"), key=lambda p: (p.parent.parent.name, p.parent.name)) if celulas.is_dir() else []
    rodadas = []
    for caminho in caminhos:
        pasta = caminho.parent
        celula = _ler_json(caminho) or {}
        registro = _ler_json(pasta / "registro.json")
        ident = pasta.parent.name
        niveis = {n: d.get("estado", "") for n, d in (registro or {}).get("niveis", {}).items()}
        terminou = celula.get("terminou", True) is not False
        if not terminou:
            alcancado = "não terminou"
        else:
            alcancado = (registro.get("alcancado") or "N0") if registro else "sem prova"
        rodadas.append({
            "id": ident, "rodada": pasta.name, "modo": celula.get("modo", ""), "origem": origem_do_id(ident, celula),
            "imagem": celula.get("imagem", ""), "ate": celula.get("ate", ""), "terminou": terminou,
            "alcancado": alcancado,
            "falhou": registro.get("falhou") if registro else None,
            "niveis": niveis, "primeira_falha": _primeira_falha((registro or {}).get("niveis", {})),
            "impedida_por_versao": list((registro or {}).get("impedida_por_versao", [])),
            "sistema": ((registro or {}).get("sistema") or {}).get("nome", ""),
            "commit": str((celula.get("actions") or {}).get("commit", ""))[:8],
            # ! Alteração de IA - Revisar: (25/11/2026, consertos da primeira execução do Actions) cada rodada guarda o nome do `preparo` do `celula.json` (`nenhum` se a chave não existe).
            # ! Motivo: a `CI-UBU` passa a remover o MySQL do executor antes do instalador; a linha da rodada precisa dizer isso, e as rodadas gravadas antes da chave continuam valendo, sem preparo.
            "preparo": str((celula.get("preparo") or {}).get("nome", "nenhum")) if isinstance(celula.get("preparo"), dict) else "nenhum",
            "instalador": _estado_do_instalador(celula),   # ! Alteração de IA - Revisar: campo novo (decisão 180). ! Motivo: ver `_estado_do_instalador`.
        })
    return rodadas


# ! Alteração de IA - Revisar: bloco de funções de resumo por célula (`_da_rodada`, `por_celula`, `_peso_do_nivel`, `_melhor_nivel`): `_da_rodada` guarda os campos de uma rodada que o resumo mostra; `por_celula` junta as rodadas de cada id (primeira, última e maior nível das rodadas `novo`); `_peso_do_nivel` e `_melhor_nivel` dão o maior nível entre N1 e N4.
# ! Motivo: a última rodada de uma célula pode ter pedido menos níveis que uma anterior (por exemplo, `--ate N1` depois de um `--ate N3`), e mostrar só a última esconderia o que já foi provado; "sem prova" e "não terminou" valem menos que N0.
def _da_rodada(r: dict) -> dict:
    """Os campos de uma rodada que a tabela por célula mostra."""
    return {"rodada": r["rodada"], "modo": r["modo"], "alcancado": r["alcancado"], "ate": r["ate"], "primeira_falha": r["primeira_falha"],
            "preparo": r.get("preparo", "nenhum")}   # ! Alteração de IA - Revisar: entra `preparo` (ver `coletar`). ! Motivo: `_texto_da_rodada` o mostra.


def por_celula(rodadas: list[dict]) -> list[dict]:
    """Uma entrada por id, com a primeira e a última rodada."""
    grupos: dict[str, list[dict]] = {}
    for r in rodadas:
        grupos.setdefault(r["id"], []).append(r)
    saida = []
    for ident in sorted(grupos):
        lista = sorted(grupos[ident], key=lambda r: r["rodada"])
        ultima = lista[-1]
        saida.append({"id": ident, "origem": ultima["origem"], "sistema": CELULAS[ident][0] if ident in CELULAS else ultima["sistema"],
                      "rodadas": len(lista), "primeira": _da_rodada(lista[0]), "ultima": _da_rodada(ultima),
                      "melhor_novo": _melhor_nivel([r["alcancado"] for r in lista if r["modo"] == "novo"]),
                      # ! Alteração de IA - Revisar: (26/11/2026, decisão 180) a célula ganha `pedido_novo` (o maior `ate` entre as rodadas `novo`, `-` se não há) e `instalador_ultima` (o campo `instalador` da última rodada).
                      # ! Motivo: `classificar` compara o que a prova alcançou com o que foi pedido e olha se o instalador foi até o fim na última rodada; o `melhor_novo` sozinho não diz se N3 era o teto pedido ou um tropeço.
                      "pedido_novo": _melhor_nivel([r["ate"] for r in lista if r["modo"] == "novo" and _peso_do_nivel(r["ate"]) >= 0]),
                      "instalador_ultima": ultima["instalador"]})
    return saida


def _peso_do_nivel(nivel: str) -> int:
    """O número do nível (N3 vale 3); qualquer outro texto (`sem prova`, `não terminou`) vale -1."""
    return int(nivel[1:]) if len(nivel) == 2 and nivel[0] == "N" and nivel[1].isdigit() else -1


def _melhor_nivel(niveis: list[str]) -> str:
    """O maior nível entre os dados (`sem prova` vale menos que `N0`); `-` se não há nenhum."""
    return max(niveis, key=_peso_do_nivel) if niveis else "-"


# ! Alteração de IA - Revisar: bloco de funções que montam as tabelas (`_tabela`, `_ordem_das_celulas`, `bloco_resumo`, `_texto_da_rodada`, `bloco_matriz`, `bloco_rodadas`, `bloco_nao_testadas`): `_tabela` monta a tabela em Markdown; `_ordem_das_celulas` põe as células da matriz primeiro e as de fora dela depois; `bloco_resumo` é a tabela curta do README (agora com a coluna "Como a máquina nasce"); `_texto_da_rodada` e `bloco_matriz` mostram a primeira e a última rodada de cada célula; `bloco_rodadas` é o dado cru, uma linha por rodada; `bloco_nao_testadas` lista o que a decisão 153 deixou sem teste.
# ! Motivo: a tabela do README trazia a `ALVO` ao lado das máquinas novas sem dizer que nela o instalador não rodou, e uma pessoa lia "passou até o N3" como "instalou numa máquina limpa"; a coluna nova diz como cada máquina nasce. Uma rodada cortada pelo GitHub aparece como "não terminou", e não como nível.
def _tabela(cabecalho: list[str], linhas: list[list[str]]) -> str:
    """Uma tabela em Markdown; cada célula passa por `_limpo`."""
    saida = ["| " + " | ".join(cabecalho) + " |", "|" + "---|" * len(cabecalho)]
    saida += ["| " + " | ".join(_limpo(c) for c in linha) + " |" for linha in linhas]
    return "\n".join(saida)


def _ordem_das_celulas(celulas: list[dict]) -> list[str]:
    """As células da matriz do plano, na ordem de CELULAS, e depois as que aparecem nas rodadas e não estão lá."""
    ids = list(CELULAS) + sorted(c["id"] for c in celulas if c["id"] not in CELULAS)
    return ids


def bloco_resumo(celulas: list[dict]) -> str:
    """A tabela curta do README: uma linha por célula da matriz, com a última rodada e como a máquina nasce."""
    por_id = {c["id"]: c for c in celulas}
    linhas = []
    for ident in _ordem_das_celulas(celulas):
        c = por_id.get(ident)
        sistema = CELULAS[ident][0] if ident in CELULAS else (c["sistema"] if c else "")
        nasce = CELULAS[ident][1] if ident in CELULAS else ""
        if c is None:
            previsto = origem_do_id(ident)
            linhas.append([ident, sistema, nasce, f"{previsto} (previsto)" if previsto else "", "ainda sem rodada", "-", "-"])
        else:
            linhas.append([ident, sistema, nasce, c["origem"], c["ultima"]["alcancado"], c["ultima"]["ate"], c["melhor_novo"]])
    tabela = _tabela(["Célula", "Sistema", "Como a máquina nasce", "Onde rodou", "Nível alcançado na última rodada", "Prova pedida até",
                      "Maior nível em rodada novo"], linhas)
    legenda = ("Cada linha é uma célula de teste, e a coluna \"Como a máquina nasce\" diz o que ela é: na `ALVO` só a prova rodou. "
               "Nível alcançado é o maior nível da prova que passou sem nenhum nível abaixo dele ter falhado; N0 quer dizer que nenhum nível "
               "passou, \"sem prova\" quer dizer que a rodada parou antes de gravar o `registro.json`, e \"não terminou\" quer dizer que "
               "o GitHub cortou a tarefa antes do fim. Rodada `novo` é a que roda o "
               "instalador já com os consertos; `como-esta` é a que roda o instalador antes deles, para gravar a falha. A última coluna "
               "olha todas as rodadas `novo` da célula, porque a última rodada pode ter pedido menos níveis que uma anterior.")
    return tabela + "\n\n" + legenda


def _texto_da_rodada(r: dict) -> str:
    """A rodada numa frase: nome, modo, até onde foi pedido, o que alcançou e a primeira falha."""
    if r["alcancado"] == "sem prova":
        alcancou = "sem prova (a rodada parou antes de gravar o registro.json)"
    elif r["alcancado"] == "não terminou":
        alcancou = "não terminou (o GitHub cortou a tarefa antes do fim)"
    else:
        alcancou = f"alcançou {r['alcancado']}"
    # ! Alteração de IA - Revisar: (25/11/2026, consertos da primeira execução do Actions) a frase da rodada passa a dizer "preparo <nome>" quando o `celula.json` traz um preparo diferente de `nenhum`.
    # ! Motivo: a `CI-UBU` remove o MySQL do executor antes do instalador (execução 45650086543: o `apt-get --no-remove` recusou a troca); quem lê o relatório precisa ver que aquela rodada não foi numa máquina como veio.
    preparo = f", preparo {r['preparo']}" if r.get("preparo", "nenhum") != "nenhum" else ""
    texto = f"{r['rodada']}, {r['modo'] or 'modo não gravado'}{preparo}, até {r['ate'] or '?'}: {alcancou}"
    return texto + (f". {r['primeira_falha']}" if r["primeira_falha"] else "")


def bloco_matriz(celulas: list[dict]) -> str:
    """A tabela completa: primeira e última rodada de cada célula, com o modo, o nível e a primeira falha."""
    linhas = []
    for c in celulas:
        ultima = "a mesma rodada" if c["rodadas"] == 1 else _texto_da_rodada(c["ultima"])
        linhas.append([c["id"], str(c["rodadas"]), _texto_da_rodada(c["primeira"]), ultima])
    return _tabela(["Célula", "Rodadas", "Primeira rodada", "Última rodada"], linhas)


def bloco_rodadas(rodadas: list[dict]) -> str:
    """Uma linha por rodada (o dado cru)."""
    linhas = []
    for r in rodadas:
        linhas.append([r["id"], r["rodada"], r["origem"], r["modo"] or "-", r["ate"] or "-", r["alcancado"]]
                      + [r["niveis"].get(n, "-") for n in NIVEIS]
                      + [r["commit"] or "-", ", ".join(r["impedida_por_versao"]) or "-"])
    return _tabela(["Célula", "Rodada", "Onde", "Modo", "Até", "Alcançou", "N1", "N2", "N3", "N4", "Commit", "Versão impede"], linhas)


def bloco_nao_testadas() -> str:
    """A tabela das células que a decisão 153 deixou sem teste, com o motivo de cada uma."""
    return _tabela(["Célula", "Sistema", "Por que não foi testada"], [[c, s, m] for c, s, m in NAO_TESTADAS])


# ! Alteração de IA - Revisar: (26/11/2026, decisão 180) bloco de funções da limitação e do trabalho futuro (`classificar`, `_sistema_e_id`, `_nivel_alcancado`, `bloco_limites`, `_linhas_do_futuro`, `bloco_futuro`, `bloco_limites_curto`): `classificar` põe cada célula numa de seis classes (`so_prova`, `sem_suporte`, `abaixo_do_pedido`, `instalador_parou`, `sem_n4`, `ate_o_fim`) com a frase da limitação; `bloco_limites` e `bloco_limites_curto` dizem até onde a prova chegou em cada sistema; `bloco_futuro` lista o que falta provar.
# ! Motivo: o dono do projeto pediu que os sistemas em que o instalador não foi provado até o fim fiquem declarados como limitação e como trabalho futuro, e a tabela do resumo não dizia que uma célula que alcançou o N3 pedindo N3 também é um limite, nem que no Mac Intel a prova passou com o instalador interrompido; gerados das pastas de rodada, os blocos não ficam para trás. "Provado até o fim" é a instalação concluída e a prova até o N4 numa máquina em que o instalador rodou.
def classificar(celula: dict) -> tuple[str, str]:
    """A classe da célula e a frase da limitação (vazia em `ate_o_fim`); a primeira regra que vale decide."""
    melhor_esforco = " (melhor esforço)" if "(melhor esforço)" in celula["sistema"] else ""
    if celula["instalador_ultima"] == "não rodou":
        return "so_prova", "só a prova rodou, sobre a instalação que já existia; o instalador não rodou nesta máquina"
    if "(sem suporte)" in celula["sistema"]:
        return "sem_suporte", "sem suporte, de propósito: o instalador para e diz o que instalar à mão"
    if _peso_do_nivel(celula["melhor_novo"]) < _peso_do_nivel(celula["pedido_novo"]):
        return "abaixo_do_pedido", "a prova ficou abaixo do nível pedido" + melhor_esforco
    if celula["instalador_ultima"] == "interrompido":
        return "instalador_parou", "a prova passou, mas o instalador não foi até o fim" + melhor_esforco
    if _peso_do_nivel(celula["melhor_novo"]) < _peso_do_nivel("N4"):
        return "sem_n4", "o N4, com o modelo do projeto respondendo, não foi pedido nesta célula"
    return "ate_o_fim", ""


def _sistema_e_id(c: dict) -> str:
    return f"{c['sistema']} (`{c['id']}`)"


def _nivel_alcancado(c: dict) -> str:
    """Até onde a prova chegou: o melhor nível das rodadas `novo`; na `so_prova`, o nível da última rodada."""
    return c["ultima"]["alcancado"] if classificar(c)[0] == "so_prova" else c["melhor_novo"]


def _nivel_pedido(c: dict) -> str:
    return c["ultima"]["ate"] if classificar(c)[0] == "so_prova" else c["pedido_novo"]


def _ordenadas(celulas: list[dict]) -> list[dict]:
    por_id = {c["id"]: c for c in celulas}
    return [por_id[i] for i in _ordem_das_celulas(celulas) if i in por_id]


def bloco_limites(celulas: list[dict]) -> str:
    """A frase do que foi provado até o fim, a tabela das outras células com rodada e a legenda."""
    ordem = _ordenadas(celulas)
    inteiras = [c for c in ordem if classificar(c)[0] == "ate_o_fim"]
    frase = "**Provado até o fim** (instalação concluída e prova até o N4): " + (
        "; ".join(f"{c['sistema']} (`{c['id']}`, {c['origem']})" for c in inteiras) + "." if inteiras else "nenhuma célula.")
    linhas = [[c["id"], c["sistema"], c["origem"], _nivel_alcancado(c), _nivel_pedido(c), c["instalador_ultima"], classificar(c)[1]]
              for c in ordem if classificar(c)[0] != "ate_o_fim"]
    tabela = _tabela(["Célula", "Sistema", "Onde rodou", "Até onde a prova chegou", "Maior nível pedido", "Instalador na última rodada",
                      "Limitação"], linhas)
    legenda = ("\"Até onde a prova chegou\" é o maior nível alcançado numa rodada `novo`, que é a do instalador depois dos consertos "
               "(na célula em que só a prova rodou, é o nível da última rodada). \"Maior nível pedido\" existe porque nem toda célula pede o N4. "
               "\"Instalador na última rodada\" diz se o instalador terminou, parou no meio ou nem rodou.")
    return frase + "\n\n" + tabela + "\n\n" + legenda


def _linhas_do_futuro(celulas: list[dict]) -> list[tuple[str, str]]:
    """As linhas do trabalho futuro (o que falta provar, por que ficou de fora), na ordem do bloco."""
    ordem = _ordenadas(celulas)
    por_classe: dict[str, list[dict]] = {}
    for c in ordem:
        por_classe.setdefault(classificar(c)[0], []).append(c)
    linhas: list[tuple[str, str]] = []
    pedidos = sorted({c["pedido_novo"] for c in por_classe.get("sem_n4", [])}, key=_peso_do_nivel)
    for pedido in pedidos:
        grupo = [c for c in por_classe["sem_n4"] if c["pedido_novo"] == pedido]
        linhas.append(("A prova até o N4, com o modelo do projeto respondendo, em: " + ", ".join(_sistema_e_id(c) for c in grupo),
                       f"essas células pediram a prova só até o {pedido}"))
    if "instalador_parou" in por_classe:
        linhas.append(("O instalador até o fim em: " + ", ".join(_sistema_e_id(c) for c in por_classe["instalador_parou"]),
                       "na última rodada a prova passou e o instalador foi interrompido (seção 5 do relatório do instalador)"))
    if "abaixo_do_pedido" in por_classe:
        grupo = por_classe["abaixo_do_pedido"]
        todas = all("(melhor esforço)" in c["sistema"] for c in grupo)
        linhas.append(("O nível pedido em: " + ", ".join(f"{_sistema_e_id(c)} (ficou no {c['melhor_novo']} de {c['pedido_novo']})" for c in grupo),
                       "melhor esforço: o instalador não instala tudo de que esse sistema precisa" if todas
                       else "a prova ficou abaixo do nível pedido"))
    linhas += [(f"{sistema} (`{cod}`)", motivo) for cod, sistema, motivo in NAO_TESTADAS]
    linhas += list(SEM_CELULA)
    return linhas


def bloco_futuro(celulas: list[dict]) -> str:
    """A tabela do que falta provar e por que ficou de fora."""
    return _tabela(["O que falta provar", "Por que ficou de fora"], [list(l) for l in _linhas_do_futuro(celulas)])


def bloco_limites_curto(celulas: list[dict]) -> str:
    """Os dois parágrafos do README: a limitação e o trabalho futuro."""
    # ! Alteração de IA - Revisar: (26/11/2026, decisão 180, ajuste do controlador) os dois parágrafos do README passam a agrupar os sistemas por tipo de limite, sem o código de cada célula; o motivo de cada item fica nas tabelas do relatório.
    # ! Motivo: a primeira forma repetia a mesma frase a cada célula e listava cada linha do trabalho futuro por extenso; o parágrafo ficava maior que a tabela que ele resume, num README que estava sendo enxugado a pedido do Eric.
    ordem = _ordenadas(celulas)
    por_classe: dict[str, list[dict]] = {}
    for c in ordem:
        por_classe.setdefault(classificar(c)[0], []).append(c)

    def nomes(grupo: list[dict]) -> str:
        return "; ".join(c["sistema"] for c in grupo)

    inteiras = por_classe.get("ate_o_fim", [])
    onde = "; ".join(f"{c['sistema']} ({c['origem']})" for c in inteiras) if inteiras else "nenhuma célula"
    frases = []
    sem_n4 = por_classe.get("sem_n4", [])
    for pedido in sorted({c["pedido_novo"] for c in sem_n4}, key=_peso_do_nivel):
        frases.append(f"A prova foi até o {pedido}, o nível pedido, sem chegar ao N4: {nomes([c for c in sem_n4 if c['pedido_novo'] == pedido])}.")
    if "instalador_parou" in por_classe:
        frases.append(f"A prova passou, mas o instalador não foi até o fim: {nomes(por_classe['instalador_parou'])}.")
    if "abaixo_do_pedido" in por_classe:
        frases.append("A prova ficou abaixo do nível pedido: "
                      + "; ".join(f"{c['sistema']}, no {c['melhor_novo']} de {c['pedido_novo']}" for c in por_classe["abaixo_do_pedido"]) + ".")
    if "sem_suporte" in por_classe:
        frases.append(f"Sem suporte, de propósito: {nomes(por_classe['sem_suporte'])}.")
    if "so_prova" in por_classe:
        frases.append(f"Só a prova rodou, sem o instalador: {nomes(por_classe['so_prova'])}.")
    limitacao = ("**Limitação (o que o projeto entrega hoje).** O instalador foi provado até o fim, com a instalação concluída e a prova "
                 f"até o N4, em: {onde}." + (" Nos outros sistemas com rodada: " + " ".join(frases) if frases else ""))
    falta = []
    if sem_n4:
        falta.append(f"A prova até o N4, com o modelo do projeto respondendo, em: {nomes(sem_n4)}.")
    if "instalador_parou" in por_classe:
        falta.append(f"O instalador até o fim em: {nomes(por_classe['instalador_parou'])}.")
    if "abaixo_do_pedido" in por_classe:
        falta.append(f"O nível pedido em: {nomes(por_classe['abaixo_do_pedido'])}.")
    falta.append("As células da matriz que não rodaram: " + "; ".join(sistema for _, sistema, _ in NAO_TESTADAS) + ".")
    falta.append("E o que nenhuma célula exercita: "
                 + "; ".join((item[0].lower() + item[1:]) if item.startswith(("O ", "Um ")) else item for item, _ in SEM_CELULA) + ".")
    falta.append("O motivo de cada item está na seção 6 do relatório do instalador.")
    futuro = "**Trabalho futuro (o que falta provar).** " + " ".join(falta)
    return _limpo_paragrafo(limitacao) + "\n\n" + _limpo_paragrafo(futuro)


def _limpo_paragrafo(texto: str) -> str:
    """O parágrafo numa linha, sem travessão nem seta (diferente de `_limpo`, não escapa o `|`: não está numa tabela)."""
    return " ".join(texto.split()).replace("—", "-").replace("–", "-").replace("→", "para").replace("->", "para")


# ! Alteração de IA - Revisar: bloco de funções que colam e gravam (`_marcas`, `colar`, `matriz_json`, `_blocos`, `_ler`, `_gravar`, `sincronizar`, `main`): `_marcas` dá as duas marcas HTML de um bloco; `colar` troca o texto entre elas; `matriz_json` monta o `matriz.json`; `_blocos` monta os quatro blocos; `_ler` e `_gravar` leem e gravam sem mexer no fim de linha; `sincronizar` compara (e, com `gravar`, grava) o `matriz.json` e os destinos; `main` é a linha de comando (`--colar` e `--check`). Em `sincronizar`, destino que não existe ou sem as marcas de um bloco passa a ser diferença (antes era só aviso) e nenhum destino com erro de marca é gravado.
# ! Motivo: se alguém apagasse uma marca do README, o `--check` só avisava, sai com 0 e o resumo do README ficava velho sem ninguém ver; e o `--colar` gravava o que dava e deixava o arquivo com uns blocos novos e outros velhos. Agora a marca que sumiu derruba o `--check` e o `--colar` (código 1) e o arquivo com problema fica como estava.
def _marcas(nome: str) -> tuple[str, str]:
    """As marcas de início e de fim do bloco `nome`."""
    return f"<!-- tb_inst_{nome}:inicio -->", f"<!-- tb_inst_{nome}:fim -->"


def colar(texto: str, nome: str, conteudo: str) -> str:
    """Troca o que está entre as marcas do bloco `nome`. O resto do texto não muda. `ValueError` se faltam marcas ou se estão repetidas."""
    inicio, fim = _marcas(nome)
    n_inicio, n_fim = texto.count(inicio), texto.count(fim)
    if n_inicio == 0 and n_fim == 0:
        raise ValueError(f"as marcas do bloco {nome} não existem")
    if n_inicio > 1 or n_fim > 1:
        raise ValueError(f"as marcas do bloco {nome} aparecem mais de uma vez")
    if n_inicio == 0:
        raise ValueError(f"falta a marca de início do bloco {nome}")
    if n_fim == 0:
        raise ValueError(f"falta a marca de fim do bloco {nome}")
    fim_do_inicio = texto.index(inicio) + len(inicio)
    comeco_do_fim = texto.index(fim)
    if comeco_do_fim < fim_do_inicio:
        raise ValueError(f"a marca de fim do bloco {nome} vem antes da de início")
    quebra = "\r\n" if "\r\n" in texto else "\n"
    corpo = conteudo.replace("\r\n", "\n").strip("\n").replace("\n", quebra)
    return texto[:fim_do_inicio] + quebra + corpo + quebra + texto[comeco_do_fim:]


def matriz_json(rodadas: list[dict]) -> str:
    """O texto do `matriz.json`: a tag e uma linha por rodada."""
    dados = {
        "tag_ia": {
            "alteracao": "! Alteração de IA - Revisar: arquivo gerado por ferramentas/instalador_matriz/relatorio.py: uma linha por rodada de "
                         "célula de teste do instalador, lida dos `celula.json` e `registro.json` de `celulas/`.",
            "motivo": "! Motivo: o relatório do instalador e os blocos do README e do DETALHES-TECNICOS saem destas linhas; escrever o nível "
                      "à mão faria o texto divergir da evidência (rode `relatorio.py --colar` depois de importar uma rodada nova).",
        },
        "rodadas": rodadas,
    }
    return json.dumps(dados, ensure_ascii=False, indent=1) + "\n"


def _blocos(rodadas: list[dict]) -> dict:
    """Os sete blocos de texto, por nome."""   # ! Alteração de IA - Revisar: entram `limites`, `futuro` e `limites_curto` (decisão 180). ! Motivo: ver `DESTINOS`.
    celulas = por_celula(rodadas)
    return {"resumo": bloco_resumo(celulas), "matriz": bloco_matriz(celulas), "rodadas": bloco_rodadas(rodadas),
            "nao_testadas": bloco_nao_testadas(), "limites": bloco_limites(celulas), "futuro": bloco_futuro(celulas),
            "limites_curto": bloco_limites_curto(celulas)}


def _ler(caminho: Path) -> str:
    """O texto do arquivo em UTF-8, sem trocar o fim de linha."""
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        return arquivo.read()


def _gravar(caminho: Path, texto: str) -> None:
    """Grava em UTF-8 sem trocar o fim de linha, criando a pasta se faltar."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        arquivo.write(texto)


def sincronizar(raiz: Path, gravar: bool) -> tuple[list[str], list[str]]:
    """Compara (e, com `gravar`, grava) o `matriz.json` e os blocos dos destinos com o que as evidências dão.
    Devolve (diferenças, avisos). Destino que não existe, ou que não tem as marcas de um bloco, é diferença; nesse caso nada é
    gravado naquele arquivo. A lista de avisos fica vazia (todo problema é diferença); o retorno em par é mantido."""
    rodadas = coletar(raiz / CELULAS_RELATIVO)
    blocos = _blocos(rodadas)
    diferencas: list[str] = []
    avisos: list[str] = []
    esperado = matriz_json(rodadas)
    atual = _ler(raiz / MATRIZ_RELATIVO) if (raiz / MATRIZ_RELATIVO).exists() else None
    if atual != esperado:
        diferencas.append(f"{MATRIZ_RELATIVO.as_posix()}: não existe ou difere das rodadas lidas")
        if gravar:
            _gravar(raiz / MATRIZ_RELATIVO, esperado)
    for destino, nomes in DESTINOS.items():
        caminho = raiz / destino
        if not caminho.exists():
            diferencas.append(f"{destino.as_posix()}: o arquivo não existe")
            continue
        texto = _ler(caminho)
        novo, mudados, com_problema = texto, [], False
        for nome in nomes:
            inicio, fim = _marcas(nome)
            if inicio not in novo and fim not in novo:
                diferencas.append(f"{destino.as_posix()}: sem as marcas do bloco {nome}")
                com_problema = True
                continue
            try:
                depois = colar(novo, nome, blocos[nome])
            except ValueError as e:
                diferencas.append(f"{destino.as_posix()}: marcas com problema: {e}")
                com_problema = True
                continue
            if depois != novo:
                mudados.append(nome)
            novo = depois
        if mudados:
            diferencas.append(f"{destino.as_posix()}: o bloco {', '.join(mudados)} difere do que as evidências dão")
            if gravar and not com_problema:
                _gravar(caminho, novo)
    return diferencas, avisos


def main(argv: list[str] | None = None) -> int:
    """A linha de comando: `--colar` grava e `--check` só confere; sai com 1 se sobrar diferença."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--colar", action="store_true", help="grava o matriz.json e cola os blocos")
    grupo.add_argument("--check", action="store_true", help="não grava; sai com 1 se algo difere")
    args = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    diferencas, avisos = sincronizar(RAIZ, gravar=args.colar)
    for aviso in avisos:
        print(f"aviso: {aviso}")
    if args.colar:
        for d in diferencas:
            print(f"atualizado: {d}")
        restantes, _ = sincronizar(RAIZ, gravar=False)
        for d in restantes:
            print(f"erro: {d}")
        print(f"relatorio.py --colar: {len(diferencas)} arquivo(s) atualizado(s)")
        return 1 if restantes else 0
    for d in diferencas:
        print(f"diferença: {d}")
    print("relatorio.py --check: " + ("sem diferença" if not diferencas else f"{len(diferencas)} diferença(s)"))
    return 1 if diferencas else 0


if __name__ == "__main__":
    sys.exit(main())
