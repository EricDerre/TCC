#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/10/2026, Fase 4, pacote P2): o catálogo de cenários das duas cobaias
# (plano aprovado, seções 3.2 e 3.9; ficha 36), cada um como uma lista de passos em dados (abrir, esperar, clicar,
# preencher, conferir), o executor que roda um cenário no Playwright capturando a árvore depois de cada passo e
# parando na primeira conferência que falha (o momento da detecção, início do cronômetro do MTTR), as conferências em
# código (contagem, texto por padrão, visível, url, título), o cronômetro (`mttr_segundos`) e o critério de Task Success
# (fluxo restaurado e roteiro concluído sem erro). Nada aqui chama modelo.
# ! Motivo: a Fase 5 mede MTTR e Task Success em cerca de dez cenários com cinco repetições (projeto ABNT §3.4), e a
# Fase 4 precisa dos mesmos roteiros para reproduzir os casos na tela (corrida 17) e para a cura de seletor (P4); com
# os passos em dados, o mesmo cenário roda igual nas duas fases e a trilha registra cada passo como evento `acao`.
"""Cenários da Fase 4 e da Fase 5 (pacote P2): catálogo, executor, conferências, cronômetro e critério."""
from __future__ import annotations

import datetime as dt
import re
import time
from urllib.parse import urljoin

import navegador

BASE_PADRAO = "http://localhost:8080/"
COBAIAS = ("api", "front")
ACOES = ("abrir", "esperar", "clicar", "preencher", "conferir")
TIPOS_DE_CONFERENCIA = ("contagem", "texto", "visivel", "url", "titulo")
GRID = "#produtos-api-grid .saiba-mais"
# O passo de espera aceita o grid preenchido OU a mensagem de erro da carga: quando a chamada falha, a conferência
# seguinte falha em segundos em vez de esperar os 60 s do tempo limite (medido na corrida 17 de 26/10/2026).
GRID_OU_ERRO = f"{GRID}, #produtos-api-status.text-danger"

CENARIOS: list[dict] = [
    {"id": "api-catalogo", "cobaia": "api", "titulo": "Catálogo de produtos pela API", "pagina": "produtos_api.php",
     "requisicao": "GET /api/produtos", "esquema": "ProdutoOut", "forma": "lista",
     "alvo": {"papel": "button", "nome": "Saiba Mais...", "ocorrencia": 1},
     "passos": [
         {"acao": "abrir", "url": "produtos_api.php"},
         {"acao": "esperar", "seletor": GRID_OU_ERRO, "ate_ms": 60000},
         {"acao": "conferir", "nome": "grid com 14 cartões", "tipo": "contagem", "seletor": GRID, "esperado": 14},
         {"acao": "conferir", "nome": "preço do primeiro cartão", "tipo": "texto", "seletor": "#produtos-api-grid .thumbnail .btn-default",
          "padrao": r"^R\$ \d+,\d{2}$"},
         {"acao": "conferir", "nome": "sem mensagem de erro na carga", "tipo": "texto", "seletor": "#produtos-api-status", "padrao": r"^$"},
     ]},
    {"id": "api-detalhe", "cobaia": "api", "titulo": "Detalhe do produto no modal", "pagina": "produtos_api.php",
     "requisicao": "GET /api/produtos/{id}", "esquema": "ProdutoOut", "forma": "objeto",
     "alvo": {"papel": "button", "nome": "Saiba Mais...", "ocorrencia": 1},
     "passos": [
         {"acao": "abrir", "url": "produtos_api.php"},
         {"acao": "esperar", "seletor": GRID_OU_ERRO, "ate_ms": 60000},
         {"acao": "conferir", "nome": "grid carregado antes do detalhe", "tipo": "contagem", "seletor": GRID, "esperado": 14},
         {"acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='1']"},
         {"acao": "esperar", "seletor": "#modalDetalhe", "ate_ms": 15000},
         {"acao": "conferir", "nome": "título do modal com o nome do produto", "tipo": "texto", "seletor": "#modalDetalheTitulo", "padrao": r"\S"},
         {"acao": "conferir", "nome": "corpo do modal com o resumo", "tipo": "texto", "seletor": "#modalDetalheCorpo", "padrao": r"\S"},
     ]},
]
ADMIN = {"login": "admin", "senha": "admin123"}          # seed.sql: tbusuarios (1, 'admin', ..., 'admin123', 'sup')
CLIENTE = {"login": "11122233344", "senha": "123456"}  # seed.sql: tbusuarios (2, '11122233344', 'Cliente Teste', '123456', 'cli')
# ! Alteração de IA - Revisar: os quatro roteiros do front legado (ficha 36; plano, P2): busca, login do administrador,
# lista de produtos do administrador e reserva do cliente. Seletores e fluxos lidos de menu_publico.php (form
# `#form-busca`, campo `#buscar`), admin/login.php (`#login_usuario`, `#senha_usuario`, botão "Entrar"; o pós-login é
# um `window.open` em JavaScript, não um 302), admin/produtos_lista.php (`button.delete[data-id]` "EXCLUIR") e
# cliente/index.php (AngularJS: o span "Faça uma nova reserva" mostra `#reserva_login`; o POST de registrar_reserva.php
# responde um fragmento sem redirecionar, por isso o roteiro reabre a página do cliente para conferir).
# ! Motivo: são os cenários de quebra de localizador da Fase 5 e os roteiros que a cura de seletor (P4) vai reexecutar;
# o front legado não tem data-testid, só ids e classes do Bootstrap, e a reserva grava no banco (o executor da
# corrida restaura o banco antes).
_LOGIN_ADMIN = [
    {"acao": "abrir", "url": "admin/login.php"},
    {"acao": "esperar", "seletor": "#login_usuario"},
    {"acao": "preencher", "seletor": "#login_usuario", "valor": ADMIN["login"]},
    {"acao": "preencher", "seletor": "#senha_usuario", "valor": ADMIN["senha"]},
    {"acao": "clicar", "seletor": "button[type=submit]"},
    {"acao": "esperar", "seletor": "h1.breadcrumb", "ate_ms": 30000},
]
CENARIOS += [
    {"id": "front-busca", "cobaia": "front", "titulo": "Busca de produtos pela barra do site", "pagina": "index.php",
     "alvo": {"papel": "searchbox", "nome": "search", "ocorrencia": 1},
     "passos": [
         {"acao": "abrir", "url": "index.php"},
         {"acao": "esperar", "seletor": "#buscar"},
         {"acao": "preencher", "seletor": "#buscar", "valor": "Picanha"},
         {"acao": "clicar", "seletor": "#form-busca button[type=submit]"},
         {"acao": "esperar", "seletor": ".thumbnail", "ate_ms": 30000},
         {"acao": "conferir", "nome": "dois produtos com Picanha no nome", "tipo": "contagem", "seletor": ".thumbnail", "esperado": 2},
         {"acao": "conferir", "nome": "título da lista de resultados", "tipo": "texto", "seletor": "h2.breadcrumb", "padrao": "Produtos Gerais"},
     ]},
    {"id": "front-admin-login", "cobaia": "front", "titulo": "Login do administrador", "pagina": "admin/login.php",
     "alvo": {"papel": "button", "nome": "Entrar", "ocorrencia": 1},
     "passos": _LOGIN_ADMIN + [
         {"acao": "conferir", "nome": "área administrativa aberta", "tipo": "texto", "seletor": "h1.breadcrumb", "padrao": "Área Administrativa"},
         {"acao": "conferir", "nome": "url da área administrativa", "tipo": "url", "contem": "admin/index.php"},
     ]},
    {"id": "front-admin-produtos", "cobaia": "front", "titulo": "Lista de produtos do administrador", "pagina": "admin/produtos_lista.php",
     "alvo": {"papel": "button", "nome": "EXCLUIR", "ocorrencia": 1},
     "passos": _LOGIN_ADMIN + [
         {"acao": "abrir", "url": "admin/produtos_lista.php"},
         {"acao": "esperar", "seletor": "table.table tbody tr"},
         {"acao": "conferir", "nome": "14 produtos com botão de excluir", "tipo": "contagem", "seletor": "button.delete[data-id]", "esperado": 14},
         {"acao": "conferir", "nome": "título da lista", "tipo": "texto", "seletor": "h2.breadcrumb", "padrao": "Lista de Produtos"},
     ]},
    {"id": "front-cliente-reserva", "cobaia": "front", "titulo": "Reserva do cliente", "pagina": "cliente/index.php",
     "alvo": {"papel": "button", "nome": "Reservar", "ocorrencia": 1}, "restaura_banco": True,
     "passos": [
         {"acao": "abrir", "url": "admin/login.php"},
         {"acao": "esperar", "seletor": "#login_usuario"},
         {"acao": "preencher", "seletor": "#login_usuario", "valor": CLIENTE["login"]},
         {"acao": "preencher", "seletor": "#senha_usuario", "valor": CLIENTE["senha"]},
         {"acao": "clicar", "seletor": "button[type=submit]"},
         {"acao": "esperar", "seletor": "span.btn-info", "ate_ms": 30000},
         {"acao": "clicar", "seletor": "span.btn-info"},
         {"acao": "esperar", "seletor": "#reserva_login", "ate_ms": 15000},
         {"acao": "preencher", "seletor": "#pessoas", "valor": "4"},
         {"acao": "preencher", "seletor": "#data_pedido", "valor": "{hoje+3}"},
         {"acao": "clicar", "seletor": "#enviar"},
         {"acao": "abrir", "url": f"cliente/index.php?cliente={CLIENTE['login']}"},
         {"acao": "esperar", "seletor": "table.table tbody tr", "ate_ms": 30000},
         {"acao": "conferir", "nome": "uma reserva em análise na tabela", "tipo": "contagem", "seletor": "button.cancela[data-id]:not([data-id=''])", "esperado": 1},
         {"acao": "conferir", "nome": "status da reserva", "tipo": "texto", "seletor": "table.table tbody", "padrao": "Em Análise"},
     ]},
]
# Os cenários do ensaio da Fase 5 (ficha 36): os de contrato em produtos_api.php (um por modo, ligados pelo executor da
# corrida) e os quatro de localizador no front legado.
CENARIOS_DA_FASE_5 = ["api-catalogo", "api-detalhe", "front-busca", "front-admin-login", "front-admin-produtos", "front-cliente-reserva"]


# ! Alteração de IA - Revisar: a tabela causa da taxonomia -> modo de injeção da CobaiaAPI (os seis modos antigos, em
# inglês, mais os quatorze da ficha 28, que levam o nome da causa); as duas causas de efeito são armadas pelo harness
# (ficha 29) e `dado_desatualizado` não tem modo. É o que a corrida 17 usa para ligar o modo de cada caso.
# ! Motivo: a reprodução na tela precisa saber qual modo produz a causa de cada caso gravado; sem a tabela o
# executor teria de adivinhar, e a contagem de "quantos casos a tela reproduz" (regra R1) não seria auditável.
MODO_POR_CAUSA = {
    "erro_interno_do_servidor": "error_500", "tempo_de_resposta_excedido": "latency", "tipo_divergente": "type_drift",
    "campo_ausente": "field_missing", "campo_renomeado": "field_renamed", "resposta_truncada": "malformed_json",
    "escala_ou_unidade_errada": "escala_ou_unidade_errada", "formato_de_data_divergente": "formato_de_data_divergente",
    "chave_de_juncao_errada": "chave_de_juncao_errada", "contagem_inconsistente": "contagem_inconsistente",
    "nulo_inesperado": "nulo_inesperado", "valor_fora_do_dominio": "valor_fora_do_dominio", "corpo_vazio": "corpo_vazio",
    "corpo_nao_e_json": "corpo_nao_e_json", "codificacao_incorreta": "codificacao_incorreta",
    "limite_de_requisicoes": "limite_de_requisicoes", "recurso_inexistente": "recurso_inexistente",
    "registro_duplicado": "registro_duplicado", "estrutura_aninhada_divergente": "estrutura_aninhada_divergente",
    "colecao_no_lugar_de_objeto": "colecao_no_lugar_de_objeto",
}
CAUSAS_PELO_HARNESS = ("localizador_quebrado", "estado_da_tela_divergente")
CAUSAS_SEM_MODO = ("dado_desatualizado",)
# Modos que precisam de um campo alvo: o executor passa o `campo_afetado` do caso (ou deixa o padrão da API).
MODOS_COM_CAMPO = ("type_drift", "field_missing", "field_renamed", "escala_ou_unidade_errada", "formato_de_data_divergente",
                   "chave_de_juncao_errada", "nulo_inesperado", "valor_fora_do_dominio", "codificacao_incorreta",
                   "estrutura_aninhada_divergente")


def agora() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def cenario(id_: str) -> dict:
    for c in CENARIOS:
        if c["id"] == id_:
            return c
    raise KeyError(f"cenário desconhecido: {id_!r}")


def validar_catalogo(cenarios: list[dict]) -> list[str]:
    """Os erros do catálogo (vazio quando está certo): id repetido, cobaia fora de COBAIAS, ação ou tipo de conferência
    desconhecidos, cenário sem conferência, cenário da API sem requisição ou esquema."""
    erros, vistos = [], set()
    for c in cenarios:
        id_ = c.get("id")
        if id_ in vistos:
            erros.append(f"{id_}: id repetido")
        vistos.add(id_)
        if c.get("cobaia") not in COBAIAS:
            erros.append(f"{id_}: cobaia {c.get('cobaia')!r} fora de {COBAIAS}")
        passos = c.get("passos") or []
        for p in passos:
            if p.get("acao") not in ACOES:
                erros.append(f"{id_}: ação {p.get('acao')!r} desconhecida")
            if p.get("acao") == "conferir" and p.get("tipo") not in TIPOS_DE_CONFERENCIA:
                erros.append(f"{id_}: tipo de conferência {p.get('tipo')!r} desconhecido")
        if not any(p.get("acao") == "conferir" for p in passos):
            erros.append(f"{id_}: sem passo conferir")
        if c.get("cobaia") == "api" and not (c.get("requisicao") and c.get("esquema")):
            erros.append(f"{id_}: cenário da API sem requisicao ou esquema")
    return erros


# ------------------------------------------------------------------ conferências em código

def conferir(passo: dict, observado) -> dict:
    """Compara o que a página mostrou com o que o passo esperava; devolve nome, passou, esperado e observado em texto."""
    tipo = passo.get("tipo")
    nome = passo.get("nome")
    if tipo == "contagem":
        esperado = int(passo["esperado"])
        return {"nome": nome, "passou": observado == esperado, "esperado": f"{esperado} elementos", "observado": f"{observado} elementos"}
    if tipo == "texto":
        texto = "" if observado is None else str(observado).strip()
        if "padrao" in passo:
            passou = re.search(passo["padrao"], texto) is not None
            return {"nome": nome, "passou": passou, "esperado": f"texto no padrão {passo['padrao']}", "observado": texto}
        return {"nome": nome, "passou": texto == passo.get("igual", ""), "esperado": str(passo.get("igual", "")), "observado": texto}
    if tipo == "visivel":
        return {"nome": nome, "passou": bool(observado), "esperado": "elemento visível", "observado": "visível" if observado else "não visível"}
    if tipo == "url":
        return {"nome": nome, "passou": passo.get("contem", "") in str(observado), "esperado": f"url contendo {passo.get('contem')}", "observado": str(observado)}
    if tipo == "titulo":
        return {"nome": nome, "passou": passo.get("contem", "") in str(observado), "esperado": f"título contendo {passo.get('contem')}", "observado": str(observado)}
    raise ValueError(f"tipo de conferência desconhecido: {tipo!r}")


def _observar(pagina, passo: dict):
    tipo = passo.get("tipo")
    if tipo == "contagem":
        return pagina.locator(passo["seletor"]).count()
    if tipo == "texto":
        alvo = pagina.locator(passo["seletor"]).first
        return alvo.inner_text(timeout=passo.get("ate_ms", 10000)) if alvo.count() else None
    if tipo == "visivel":
        alvo = pagina.locator(passo["seletor"]).first
        return alvo.is_visible() if alvo.count() else False
    if tipo == "url":
        return pagina.url
    if tipo == "titulo":
        return pagina.title()
    raise ValueError(f"tipo de conferência desconhecido: {tipo!r}")


def valor_do_passo(passo: dict, hoje: dt.date | None = None) -> str:
    """O valor a preencher; `{hoje+N}` vira a data de hoje mais N dias em ISO (o campo de data da reserva só aceita de
    hoje+2 a hoje+90 dias, calculados pelo servidor PHP)."""
    valor = str(passo.get("valor", ""))
    m = re.fullmatch(r"\{hoje\+(\d+)\}", valor)
    if m:
        return ((hoje or dt.date.today()) + dt.timedelta(days=int(m.group(1)))).isoformat()
    return valor


def _descrever(passo: dict) -> str:
    acao = passo.get("acao")
    if acao == "abrir":
        return f"abrir {passo.get('url')}"
    if acao == "esperar":
        return f"esperar {passo.get('seletor')} visível"
    if acao == "clicar":
        return f"clicar em {passo.get('seletor')}"
    if acao == "preencher":
        return f"preencher {passo.get('seletor')}"
    return f"conferir {passo.get('nome')}"


# ------------------------------------------------------------------ executor

def rodar_cenario(cenario_: dict, pagina, inter=None, base: str = BASE_PADRAO, capturar: bool = True, tempo_limite_ms: int = 60000) -> dict:
    """Roda os passos no Playwright, capturando a árvore depois de cada passo (com os atributos do DOM quando há
    interceptador) e parando na primeira conferência que falha ou no primeiro passo que estoura o tempo: esse é o
    momento da detecção. Devolve passou, passo_falho, conferencia_falha, erro, conferencias, tempos_ms, capturas, chamadas."""
    inicio = agora()
    t0 = time.monotonic()
    r: dict = {"id": cenario_["id"], "inicio": inicio, "fim": None, "segundos": None, "passou": True, "passo_falho": None,
               "conferencia_falha": None, "erro": None, "conferencias": [], "tempos_ms": [], "capturas": [], "chamadas": [], "deteccao": None}
    for i, passo in enumerate(cenario_["passos"]):
        t_passo = time.monotonic()
        acao = passo.get("acao")
        try:
            if acao == "abrir":
                pagina.goto(urljoin(base, passo["url"]), wait_until="load", timeout=passo.get("ate_ms", tempo_limite_ms))
            elif acao == "esperar":
                pagina.wait_for_selector(passo["seletor"], state=passo.get("estado", "visible"), timeout=passo.get("ate_ms", tempo_limite_ms))
            elif acao == "clicar":
                pagina.click(passo["seletor"], timeout=passo.get("ate_ms", 15000))
            elif acao == "preencher":
                pagina.fill(passo["seletor"], valor_do_passo(passo), timeout=passo.get("ate_ms", 15000))
            elif acao == "conferir":
                c = conferir(passo, _observar(pagina, passo))
                r["conferencias"].append(c)
                if not c["passou"]:
                    r["passou"], r["passo_falho"], r["conferencia_falha"] = False, i, c
            else:
                raise ValueError(f"ação desconhecida: {acao!r}")
        except Exception as e:  # noqa: BLE001 - tempo esgotado ou seletor que não resolve: é a falha do passo
            r["passou"], r["passo_falho"], r["erro"] = False, i, f"{type(e).__name__}: {str(e)[:300]}"
            r["conferencia_falha"] = {"nome": f"passo {i + 1} ({_descrever(passo)})", "passou": False, "esperado": _descrever(passo),
                                      "observado": r["erro"]}
        r["tempos_ms"].append(round((time.monotonic() - t_passo) * 1000, 1))
        if capturar:
            try:
                r["capturas"].append(inter.capturar() if inter is not None else navegador.capturar_arvore(pagina))
            except Exception as e:  # noqa: BLE001 - página fechada ou navegando: a captura falha, o passo fica registrado
                r["capturas"].append({"erro": f"{type(e).__name__}: {str(e)[:200]}", "contagem": 0, "nos": [], "aria": ""})
        if not r["passou"]:
            r["deteccao"] = agora()
            break
    r["fim"] = agora()
    r["segundos"] = round(time.monotonic() - t0, 3)
    if inter is not None:
        r["chamadas"] = inter.registros()
    return r


# ------------------------------------------------------------------ cronômetro e critério da Fase 5

def mttr_segundos(deteccao: str, validacao: str) -> float:
    """Da detecção (primeira conferência que falhou) até a correção validada na reexecução, em segundos."""
    a, b = dt.datetime.fromisoformat(deteccao), dt.datetime.fromisoformat(validacao)
    return round((b - a).total_seconds(), 3)


def task_success(resultado: dict) -> bool:
    """Fluxo restaurado e roteiro concluído sem erro: o cenário passou e nenhuma conferência falhou."""
    return bool(resultado.get("passou")) and all(c.get("passou") for c in resultado.get("conferencias") or [])
