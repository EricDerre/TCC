#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/10/2026, Fase 4, pacote P2): o interceptador do plano aprovado (seção
# 3.2). Escuta pelo Playwright toda requisição e resposta da página à CobaiaAPI (método, caminho, consulta, status,
# tipo de conteúdo, tempo, hash SHA-256 do corpo, com o corpo guardado uma vez), monta em código a aresta "chamada
# HTTP" entre a página PHP e a rota FastAPI, captura a árvore de acessibilidade com os atributos do DOM dos elementos
# interativos (id, name, class, data-id, data-testid, href, na ordem do documento), aplica a lista de hosts permitidos
# (só as cobaias; CDNs servidas do HAR gravado em `fixtures_fase4/cdn.har`; qualquer outro host é bloqueado e
# registrado como incidente) e grava o HAR das CDNs (`--gravar-har`). O Playwright só é importado quando o navegador
# abre, para as funções puras (hosts, aresta, registro) rodarem com o Python do sistema.
# ! Motivo: a Fase 4 é a do agente na tela e o sinal que ele precisa observar é a resposta JSON por HTTP (é por isso
# que só `produtos_api.php` chama a CobaiaAPI); a medição não pode depender da rede (as páginas carregam jQuery,
# AngularJS, Bootstrap e mapa de CDNs) e nenhum roteiro pode chegar a um host externo (o formulário de contato manda
# e-mail de verdade). O corpo inteiro vai para o blob da trilha; aqui fica só o registro com o hash.
"""Interceptador da Fase 4 (pacote P2): tráfego da CobaiaAPI, árvore com atributos do DOM, hosts permitidos, HAR.
Uso: python interceptador.py --gravar-har [--url http://localhost:8080/produtos_api.php] [--saida fixtures_fase4/cdn.har]"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlsplit

import navegador
import trilha as tr

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

HOST_DA_API = "localhost:8000"
HOSTS_PERMITIDOS = ("localhost:8080", "127.0.0.1:8080", "[::1]:8080", "localhost:8000", "127.0.0.1:8000", "[::1]:8000")
# Hosts das dependências externas das páginas (menu, rodapé e mapa); conferidos ao gravar o HAR em 26/10/2026.
CDN_PADRAO = ("code.jquery.com", "ajax.googleapis.com", "cdnjs.cloudflare.com", "maxcdn.bootstrapcdn.com",
              "stackpath.bootstrapcdn.com", "cdn.jsdelivr.net", "unpkg.com", "fonts.googleapis.com", "fonts.gstatic.com",
              "use.fontawesome.com", "kit.fontawesome.com", "ka-f.fontawesome.com")
# As páginas que os roteiros abrem e que carregam dependência externa (jQuery e AngularJS do Google, slick do jsDelivr,
# kit do FontAwesome): o HAR é gravado visitando todas.
PAGINAS_DO_HAR = ("index.php", "produtos_api.php", "admin/login.php")
# Hosts do mapa embutido no rodapé: bloqueados sem virar incidente e fora do HAR (o mapa não entra no diagnóstico e
# pesaria cerca de 2 MB de scripts no HAR gravado em 26/10/2026).
HOSTS_SILENCIOSOS = ("maps.googleapis.com", "maps.gstatic.com", "www.google.com", "maps.google.com")
FIXTURES = Path(__file__).resolve().parent / "fixtures_fase4"
HAR_PADRAO = FIXTURES / "cdn.har"
ATRIBUTOS_DO_DOM = ("id", "name", "class", "data-id", "data-testid", "href")

JS_INTERATIVOS = r"""
() => {
  const papel = (el) => {
    const r = el.getAttribute('role');
    if (r) return r;
    const t = el.tagName.toLowerCase();
    if (t === 'a') return el.hasAttribute('href') ? 'link' : null;
    if (t === 'button') return 'button';
    if (t === 'select') return 'combobox';
    if (t === 'textarea') return 'textbox';
    if (t === 'input') {
      const ty = (el.getAttribute('type') || 'text').toLowerCase();
      if (ty === 'search') return 'searchbox';
      if (ty === 'checkbox') return 'checkbox';
      if (ty === 'radio') return 'radio';
      if (['submit', 'button', 'reset', 'image'].includes(ty)) return 'button';
      if (ty === 'hidden') return null;
      return 'textbox';
    }
    return null;
  };
  const nome = (el) => {
    const al = el.getAttribute('aria-label');
    if (al && al.trim()) return al.trim();
    const t = el.tagName.toLowerCase();
    if (t === 'input' && ['submit', 'button', 'reset'].includes((el.getAttribute('type') || '').toLowerCase())) return (el.value || '').trim();
    if (t === 'input' || t === 'textarea' || t === 'select') {
      if (el.id) {
        const lab = document.querySelector('label[for="' + CSS.escape(el.id) + '"]');
        if (lab && lab.textContent.trim()) return lab.textContent.replace(/\s+/g, ' ').trim();
      }
      return (el.getAttribute('placeholder') || el.getAttribute('title') || el.getAttribute('name') || '').trim();
    }
    return (el.textContent || '').replace(/\s+/g, ' ').trim();
  };
  const saida = [];
  document.querySelectorAll('a, button, input, select, textarea, [role]').forEach((el) => {
    const p = papel(el);
    if (!p) return;
    const item = {papel: p, nome: nome(el), tag: el.tagName.toLowerCase()};
    for (const a of ['id', 'name', 'class', 'data-id', 'data-testid', 'href']) {
      const v = el.getAttribute(a);
      if (v) item[a] = v;
    }
    saida.push(item);
  });
  return saida;
}
"""


# ------------------------------------------------------------------ funções puras

def host_de(url: str) -> str:
    return (urlsplit(url).netloc or "").lower()


def permitido(url: str, hosts_permitidos=HOSTS_PERMITIDOS, hosts_har=(), hosts_silenciosos=HOSTS_SILENCIOSOS) -> str:
    """`permitido` (cobaias), `har` (dependência externa servida do HAR gravado), `silencioso` (mapa do rodapé,
    bloqueado sem incidente) ou `bloqueado` (qualquer outro host, registrado como incidente)."""
    h = host_de(url)
    if h in hosts_permitidos:
        return "permitido"
    if h in hosts_silenciosos:
        return "silencioso"
    if h in hosts_har:
        return "har"
    return "bloqueado"


def _nome_da_pagina(url: str) -> str:
    nome = urlsplit(url).path.rsplit("/", 1)[-1]
    return nome or "index"


def aresta_http(url_da_pagina: str, metodo: str, url_requisicao: str) -> dict:
    """A aresta "chamada HTTP" entre a página (nome do arquivo PHP) e a rota (método e caminho), montada em código."""
    return {"tipo": "chamada_http", "de": _nome_da_pagina(url_da_pagina), "para": f"{metodo.upper()} {urlsplit(url_requisicao).path}",
            "host": host_de(url_requisicao)}


def registro_http(metodo: str, url: str, status: int | None, cabecalhos: dict | None, corpo: str | None,
                  inicio_ms: float | None = None, fim_ms: float | None = None, tipo_recurso: str | None = None) -> dict:
    """O registro de uma troca HTTP sem o corpo: caminho, consulta, status, tipo e tamanho do conteúdo, tempo e o hash
    do corpo (o corpo em si vai para o blob da trilha, uma vez só)."""
    p = urlsplit(url)
    cab = {str(k).lower(): v for k, v in (cabecalhos or {}).items()}
    tamanho = cab.get("content-length")
    return {"metodo": metodo.upper(), "url": url, "host": host_de(url), "caminho": p.path, "consulta": p.query, "status": status,
            "content_type": cab.get("content-type"),
            "content_length": int(tamanho) if isinstance(tamanho, str) and tamanho.isdigit() else None,
            "tempo_ms": round(fim_ms - inicio_ms, 1) if inicio_ms is not None and fim_ms is not None else None,
            "tipo_recurso": tipo_recurso,
            "corpo_sha": tr.sha(corpo) if corpo is not None else None, "corpo_chars": len(corpo) if corpo is not None else None}


# ------------------------------------------------------------------ ao vivo, com o Playwright

class Interceptador:
    """Liga-se a uma página do Playwright: bloqueia hosts fora da lista (ou os serve do HAR), guarda as respostas da
    CobaiaAPI com corpo e tempo, e captura a árvore de acessibilidade com os atributos do DOM dos interativos."""

    def __init__(self, pagina, hosts_permitidos=HOSTS_PERMITIDOS, hosts_har=None, host_da_api: str = HOST_DA_API,
                 har: Path | str | None = "auto") -> None:
        # "auto": o HAR gravado em fixtures_fase4/cdn.har, quando existe (o jQuery das páginas vem dele; sem ele o modal
        # de produtos_api.php não abre, porque o Bootstrap chama $(...).modal)
        if har == "auto":
            har = HAR_PADRAO if HAR_PADRAO.exists() else None
        self.pagina = pagina
        self.hosts = tuple(hosts_permitidos)
        self.hosts_har = tuple(CDN_PADRAO if hosts_har is None else hosts_har) if har else ()
        self.host_da_api = host_da_api
        self.bloqueados: list[dict] = []
        self.incidentes: list[dict] = []
        self._inicio: dict = {}
        self._pendentes: list[tuple] = []
        self._registros: list[dict] = []
        self._corpos: dict[str, str] = {}
        contexto = pagina.context
        contexto.route("**/*", self._rota)
        if har:
            padrao = re.compile(r"^https?://(" + "|".join(re.escape(h) for h in self.hosts_har) + r")/")
            contexto.route_from_har(str(har), url=padrao, not_found="fallback")
        pagina.on("request", self._ao_pedir)
        pagina.on("response", self._ao_responder)
        pagina.on("requestfailed", self._ao_falhar)

    def _rota(self, rota) -> None:
        url = rota.request.url
        decisao = permitido(url, self.hosts, self.hosts_har)
        if decisao == "permitido":
            rota.continue_()
            return
        registro = {"url": url, "host": host_de(url), "decisao": decisao, "tipo_recurso": rota.request.resource_type,
                    "quando": time.strftime("%Y-%m-%dT%H:%M:%S")}
        self.bloqueados.append(registro)
        if decisao == "bloqueado":
            self.incidentes.append({"tipo": "host_fora_da_lista", **registro})
        elif decisao == "har":
            self.incidentes.append({"tipo": "cdn_fora_do_har", **registro})
        rota.abort()

    def _ao_pedir(self, requisicao) -> None:
        self._inicio[requisicao] = time.monotonic() * 1000

    def _ao_responder(self, resposta) -> None:
        if host_de(resposta.url) != self.host_da_api:
            return
        fim = time.monotonic() * 1000
        corpo = None
        try:
            corpo = resposta.text()
        except Exception:  # noqa: BLE001 - o corpo pode não estar mais disponível; fica None e o registro diz
            corpo = None
        self._pendentes.append((resposta, self._inicio.get(resposta.request), fim, corpo))

    def _ao_falhar(self, requisicao) -> None:
        if host_de(requisicao.url) == self.host_da_api:
            self.incidentes.append({"tipo": "requisicao_falhou", "url": requisicao.url, "erro": requisicao.failure,
                                    "quando": time.strftime("%Y-%m-%dT%H:%M:%S")})

    def registros(self) -> list[dict]:
        """As trocas com a CobaiaAPI até agora, na ordem; o corpo de cada uma fica em `corpo(sha)`."""
        for resposta, inicio, fim, corpo in self._pendentes:
            req = resposta.request
            try:
                url_da_pagina = req.frame.url
            except Exception:  # noqa: BLE001
                url_da_pagina = self.pagina.url
            reg = registro_http(req.method, resposta.url, resposta.status, resposta.headers, corpo, inicio, fim, req.resource_type)
            reg["aresta"] = aresta_http(url_da_pagina, req.method, resposta.url)
            if corpo is not None:
                self._corpos[reg["corpo_sha"]] = corpo
            self._registros.append(reg)
        self._pendentes = []
        return list(self._registros)

    def corpo(self, sha: str) -> str | None:
        return self._corpos.get(sha)

    def zerar(self) -> None:
        """Esquece as trocas registradas (entre um passo e outro do roteiro), sem esquecer os corpos."""
        self.registros()
        self._registros = []

    def capturar(self, seletor: str = "body") -> dict:
        """A árvore de acessibilidade (texto e nós) mais os elementos interativos do DOM com os atributos deles."""
        captura = navegador.capturar_arvore(self.pagina, seletor)
        captura["interativos"] = self.pagina.evaluate(JS_INTERATIVOS)
        return captura


def gravar_har(url: str | list[str], destino: Path = HAR_PADRAO, canal: str = "chromium", esperar: str | None = None,
               excluir=HOSTS_SILENCIOSOS) -> dict:
    """Abre a página (ou cada página da lista) numa sessão nova gravando no HAR só os hosts externos (tudo que não é
    cobaia nem host silencioso), com os corpos embutidos, e devolve os hosts gravados. Precisa de rede e das cobaias
    no ar. `esperar` vale só para a primeira página."""
    from playwright.sync_api import sync_playwright
    destino.parent.mkdir(parents=True, exist_ok=True)
    fora = "|".join(re.escape(h) for h in ("localhost", "127.0.0.1", "[::1]", *excluir))
    externos = re.compile(rf"^https?://(?!(?:{fora})(?:[:/]|$))")
    urls = [url] if isinstance(url, str) else list(url)
    with sync_playwright() as p:
        opcoes = {"headless": True}
        if canal != "chromium":
            opcoes["channel"] = canal
        navegador_ = p.chromium.launch(**opcoes)
        contexto = navegador_.new_context(record_har_path=str(destino), record_har_url_filter=externos, record_har_content="embed")
        pagina = contexto.new_page()
        for i, u in enumerate(urls):
            pagina.goto(u, wait_until="load", timeout=60000)
            if esperar and i == 0:
                pagina.wait_for_selector(esperar, state="visible", timeout=30000)
            try:
                pagina.wait_for_load_state("networkidle", timeout=30000)
            except Exception:  # noqa: BLE001 - mapa e fontes podem continuar pingando; o que carregou já está no HAR
                pass
        contexto.close()
        navegador_.close()
    dados = json.loads(destino.read_text(encoding="utf-8"))
    # ! Alteração de IA - Revisar: entradas sem resposta (status -1: o recurso não respondeu na gravação, como o
    # `jquery-2.2.0.min-js` com nome errado em index.php) saem do HAR antes de gravar.
    # ! Motivo: conferido em 26/10/2026: `route_from_har` encontra a entrada sem resposta e não a cumpre nem a repassa,
    # e a página fica esperando o load para sempre (index.php travou 60 s). Sem a entrada, a requisição cai no
    # bloqueio normal e é abortada, como acontece sem o HAR.
    entradas = dados["log"]["entries"]
    sem_resposta = [e["request"]["url"] for e in entradas if int(e.get("response", {}).get("status", -1) or -1) <= 0]
    dados["log"]["entries"] = [e for e in entradas if int(e.get("response", {}).get("status", -1) or -1) > 0]
    destino.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    hosts = sorted({host_de(e["request"]["url"]) for e in dados["log"]["entries"]})
    return {"arquivo": str(destino), "entradas": len(dados["log"]["entries"]), "hosts": hosts, "sem_resposta": sem_resposta}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gravar-har", action="store_true", dest="gravar_har", help="grava o HAR das dependências externas da página")
    ap.add_argument("--base", default="http://localhost:8080/")
    ap.add_argument("--paginas", nargs="+", default=list(PAGINAS_DO_HAR), help="páginas (relativas à base) a visitar")
    ap.add_argument("--saida", default=str(HAR_PADRAO))
    ap.add_argument("--canal", choices=navegador.CANAIS, default="chromium")
    args = ap.parse_args()
    if not args.gravar_har:
        ap.error("informe --gravar-har")
    resultado = gravar_har([args.base + p for p in args.paginas], Path(args.saida), canal=args.canal)
    print(f"gravado: {resultado['arquivo']} ({resultado['entradas']} entradas; hosts: {', '.join(resultado['hosts'])})")
    fora = [h for h in resultado["hosts"] if h not in CDN_PADRAO]
    if fora:
        print(f"ATENÇÃO: hosts fora de CDN_PADRAO: {fora}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
