#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/10/2026, Fase 4, pacote P0): abre o Chromium fixo do Playwright em modo
# headless (ou o Edge instalado, pelo canal `msedge`, se o download do Chromium tiver sido bloqueado) e captura a
# árvore de acessibilidade de uma página como texto (snapshot ARIA do Playwright) e como lista de nós (papel, nome,
# profundidade, atributos), gravando a amostra em `fixtures_fase4/`. O Playwright só é importado dentro de
# `Navegador`, para `parse_aria` e os testes das fixtures rodarem com o Python do sistema, sem a venv.
# ! Motivo: a Fase 4 é a do agente na tela e o harness não tinha nenhum código de navegador; o P0 do plano aprovado
# manda conferir que a captura da árvore funciona na versão instalada (Playwright 1.64.1, Chromium 156.0.8078.4, em
# 26/10/2026) antes de qualquer outro módulo, com a versão do navegador gravada para o cabeçalho de toda trilha. O
# formato do snapshot foi lido de uma página de amostra na versão instalada: `- papel "nome" [atributo=valor]:`,
# filhos com dois espaços a mais, texto solto como `- text: ...` e propriedades como `- /url: ...` logo abaixo do nó.
# O roteiro passo a passo, o trace só na falha e a interceptação de rede entram nos pacotes P2 e P4, não aqui.
"""Navegador da Fase 4: Playwright headless e captura da árvore de acessibilidade (pacote P0)."""
import argparse
import datetime as dt
import importlib.metadata
import json
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

EXP = Path(__file__).resolve().parent
FIXTURES = EXP / "fixtures_fase4"
CANAIS = ("chromium", "msedge")

_LINHA = re.compile(
    r'^(?P<papel>[A-Za-z][\w-]*)'
    r'(?:\s+"(?P<nome>(?:[^"\\]|\\.)*)")?'
    r'(?P<atributos>(?:\s+\[[^\]]*\])*)'
    r'(?::\s*(?P<texto>.*))?$'
)


def _atributos(trecho: str) -> dict[str, str]:
    """`[level=2] [disabled]` vira {"level": "2", "disabled": "true"}."""
    saida: dict[str, str] = {}
    for item in re.findall(r"\[([^\]]*)\]", trecho):
        for parte in item.split():
            chave, _, valor = parte.partition("=")
            saida[chave] = valor if valor else "true"
    return saida


def _sem_aspas(texto: str) -> str:
    texto = texto.strip()
    if len(texto) >= 2 and texto[0] == texto[-1] and texto[0] in "\"'":
        return texto[1:-1].replace('\\"', '"')
    return texto


def parse_aria(texto: str) -> list[dict]:
    """Lê o snapshot ARIA do Playwright e devolve um nó por linha: papel, nome, profundidade (dois espaços por
    nível) e atributos. Uma linha de propriedade (`- /url: x`) não vira nó: entra nos atributos do nó acima dela.
    Linha que não segue o formato vira papel `desconhecido`, com a linha inteira como nome, para nada se perder."""
    nos: list[dict] = []
    for bruta in texto.splitlines():
        if not bruta.strip():
            continue
        recuo = len(bruta) - len(bruta.lstrip(" "))
        linha = bruta.strip()
        if not linha.startswith("- "):
            continue
        resto = linha[2:].strip()
        profundidade = recuo // 2
        if resto.startswith("/"):
            chave, _, valor = resto[1:].partition(":")
            for no in reversed(nos):
                if no["profundidade"] == profundidade - 1:
                    no["atributos"][chave.strip()] = _sem_aspas(valor)
                    break
            continue
        m = _LINHA.match(resto)
        if not m:
            nos.append({"papel": "desconhecido", "nome": resto, "profundidade": profundidade, "atributos": {}})
            continue
        nome = m.group("nome")
        texto_inline = m.group("texto")
        if nome is None:
            nome = _sem_aspas(texto_inline) if texto_inline else ""
        else:
            nome = nome.replace('\\"', '"')
        nos.append({"papel": m.group("papel"), "nome": nome, "profundidade": profundidade,
                    "atributos": _atributos(m.group("atributos") or "")})
    return nos


class Navegador:
    """Abre o navegador uma vez por corrida (plano aprovado, seção 7): `with Navegador() as nav: pagina = nav.nova_pagina()`.
    `canal` é `chromium` (o Chromium que o próprio Playwright baixa e fixa) ou `msedge` (contingência do P0)."""

    def __init__(self, canal: str = "chromium", headless: bool = True) -> None:
        if canal not in CANAIS:
            raise ValueError(f"canal {canal!r} fora de {CANAIS}")
        self.canal = canal
        self.headless = headless
        self._pw = None
        self.navegador = None

    def __enter__(self) -> "Navegador":
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        opcoes = {"headless": self.headless}
        if self.canal != "chromium":
            opcoes["channel"] = self.canal
        self.navegador = self._pw.chromium.launch(**opcoes)
        return self

    def __exit__(self, *exc) -> None:
        try:
            if self.navegador is not None:
                self.navegador.close()
        finally:
            if self._pw is not None:
                self._pw.stop()

    def nova_pagina(self):
        return self.navegador.new_page()

    def versao(self) -> dict[str, str]:
        """Versões para o cabeçalho da trilha: Playwright (pacote), navegador (`Browser.version`), canal e executável."""
        return {"playwright": importlib.metadata.version("playwright"),
                "navegador": self.navegador.version,
                "canal": self.canal,
                "executavel": str(self.navegador.browser_type.executable_path) if self.canal == "chromium" else self.canal}


def capturar_arvore(pagina, seletor: str = "body") -> dict:
    """Snapshot ARIA do elemento (texto) e a lista de nós lida dele."""
    texto = pagina.locator(seletor).aria_snapshot()
    nos = parse_aria(texto)
    return {"url": pagina.url, "titulo": pagina.title(), "seletor": seletor, "aria": texto, "nos": nos,
            "contagem": len(nos)}


def gravar_fixture_arvore(url: str, destino: Path, esperar: str | None = None, canal: str = "chromium",
                          tempo_limite_ms: int = 15000, provisoria: bool = False, motivo: str = "") -> dict:
    """Abre a página, espera o seletor (o grid preenchido, por exemplo), captura a árvore e grava o JSON da fixture
    com a origem, a data e as versões. `provisoria` marca uma amostra que não veio da página real."""
    with Navegador(canal=canal) as nav:
        pagina = nav.nova_pagina()
        pagina.goto(url, wait_until="load", timeout=tempo_limite_ms)
        if esperar:
            pagina.wait_for_selector(esperar, state="visible", timeout=tempo_limite_ms)
        arvore = capturar_arvore(pagina)
        versoes = nav.versao()
    fixture = {"origem": url, "esperado": esperar, "gravado_em": dt.datetime.now().isoformat(timespec="seconds"),
               **versoes, **arvore,
               # a tag vai num campo porque JSON não aceita comentário; conferir_docs.py procura o texto dela no arquivo
               "tag_ia": {"alteracao": "! Alteração de IA - Revisar: fixture gravada por navegador.gravar_fixture_arvore "
                                       "(Fase 4, pacote P0): árvore de acessibilidade da página em `origem`, como texto "
                                       "(`aria`) e como nós (`nos`: papel, nome, profundidade, atributos).",
                          "motivo": "! Motivo: os testes e a poda (pacote P2) precisam de uma árvore real gravada uma vez e "
                                    "congelada, com a versão do Playwright e do navegador que a produziu."}}
    if provisoria:
        fixture["provisoria"] = True
        fixture["motivo"] = motivo
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(fixture, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return fixture


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fixture", metavar="URL", help="abre a URL e grava a árvore de acessibilidade como fixture")
    ap.add_argument("--esperar", metavar="SELETOR", default=None, help="seletor que precisa ficar visível antes da captura")
    ap.add_argument("--saida", metavar="ARQUIVO", default=None, help="JSON de saída (padrão: fixtures_fase4/arvore.json)")
    ap.add_argument("--canal", choices=CANAIS, default="chromium")
    ap.add_argument("--provisoria", metavar="MOTIVO", default=None,
                    help="marca a fixture como provisória, com o motivo (ex.: página estática, sem as cobaias no ar)")
    ap.add_argument("--versao", action="store_true", help="só imprime as versões do Playwright e do navegador")
    args = ap.parse_args()
    if args.versao:
        with Navegador(canal=args.canal) as nav:
            print(json.dumps(nav.versao(), ensure_ascii=False, indent=1))
        return
    if not args.fixture:
        ap.error("informe --fixture URL ou --versao")
    destino = Path(args.saida) if args.saida else FIXTURES / "arvore.json"
    fixture = gravar_fixture_arvore(args.fixture, destino, esperar=args.esperar, canal=args.canal,
                                    provisoria=args.provisoria is not None, motivo=args.provisoria or "")
    print(f"gravado: {destino} ({fixture['contagem']} nós; {fixture['canal']} {fixture['navegador']}; "
          f"playwright {fixture['playwright']})")


if __name__ == "__main__":
    main()
