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
         # ! Alteração de IA - Revisar: (01/11/2026, P4) a contagem passa a ser das linhas da tabela, e o roteiro ganha o
         # clique no botão EXCLUIR do produto 1, a espera do modal de confirmação e a conferência do nome do produto no
         # modal; o roteiro nunca clica em "Confirmar", então produtos_excluir.php não roda.
         # ! Motivo: a cura de seletor (plano, seção 3.6) precisa de um passo que resolva um elemento só e cujo efeito a
         # reexecução confira ("o modal abre"); contar `button.delete[data-id]` resolveria 14 elementos e, no modo de
         # quebra por classe, a contagem falharia antes do passo do alvo.
         {"acao": "conferir", "nome": "14 produtos na tabela", "tipo": "contagem", "seletor": "table.table tbody tr", "esperado": 14},
         {"acao": "conferir", "nome": "título da lista", "tipo": "texto", "seletor": "h2.breadcrumb", "padrao": "Lista de Produtos"},
         {"acao": "clicar", "seletor": "button.delete[data-id='1']"},
         {"acao": "esperar", "seletor": "#modalEdit", "ate_ms": 10000},
         {"acao": "conferir", "nome": "modal de exclusão com o nome do produto", "tipo": "texto", "seletor": "#modalEdit span.nome", "padrao": r"\S"},
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

def rodar_cenario(cenario_: dict, pagina, inter=None, base: str = BASE_PADRAO, capturar: bool = True, tempo_limite_ms: int = 60000,
                  antes_do_passo=None) -> dict:
    """Roda os passos no Playwright, capturando a árvore depois de cada passo (com os atributos do DOM quando há
    interceptador) e parando na primeira conferência que falha ou no primeiro passo que estoura o tempo: esse é o
    momento da detecção. Devolve passou, passo_falho, conferencia_falha, erro, conferencias, tempos_ms, capturas, chamadas.
    ! Alteração de IA - Revisar: (01/11/2026, P4) `antes_do_passo(i, passo, pagina)` é chamado antes de cada passo, e a
    detecção também fica em `t_deteccao` (relógio monotônico, em segundos).
    ! Motivo: a corrida de referência da cura descreve o alvo do passo antes de executá-lo, e o MTTR (da detecção à
    reexecução validada) precisa de um relógio com fração de segundo; `deteccao` em ISO só tem segundos inteiros."""
    inicio = agora()
    t0 = time.monotonic()
    r: dict = {"id": cenario_["id"], "inicio": inicio, "fim": None, "segundos": None, "passou": True, "passo_falho": None,
               "conferencia_falha": None, "erro": None, "conferencias": [], "tempos_ms": [], "capturas": [], "chamadas": [], "deteccao": None,
               "t_deteccao": None}
    for i, passo in enumerate(cenario_["passos"]):
        if antes_do_passo is not None:
            antes_do_passo(i, passo, pagina)
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
            r["t_deteccao"] = time.monotonic()
            break
    r["fim"] = agora()
    r["segundos"] = round(time.monotonic() - t0, 3)
    if inter is not None:
        r["chamadas"] = inter.registros()
    return r


# ------------------------------------------------------------------ P4: quebra de localizador (ficha 29, opção c)

# ! Alteração de IA - Revisar: (01/11/2026, Fase 4, pacote P4) o catálogo das quebras de localizador (decisão 80): quatro
# modos (renomear o id, trocar a classe, alterar o texto e alterar a estrutura, que envolve o elemento num contêiner novo
# e o troca de posição entre os irmãos) sobre os quatro roteiros do front legado (ficha 36), armados de duas formas: pelo
# harness, no navegador (`armar_quebra` injeta por `add_init_script` um script determinístico que aplica as mutações no
# DOMContentLoaded, depois dos scripts embutidos da página e antes de o roteiro agir), e pela variante do front PHP
# (`Programacao/CobaiaFront/quebra.php`, ligada pelo cookie `quebra=<modo>` ou pelo parâmetro de URL de mesmo nome,
# desligada por padrão). Cada célula (roteiro, modo) declara o passo do alvo, o localizador que esse passo usa na célula
# (o estilo de localizador que o modo quebra: por id, por classe, por texto ou por caminho na estrutura), o alvo (papel e
# nome na árvore de acessibilidade) e as mutações, as mesmas nas duas formas; `cenario_com_localizador` monta o roteiro
# da célula sem mudar o catálogo, e `script_de_quebra` gera o script a partir das mutações, em dados.
# ! Motivo: os roteiros da ficha 36 localizam por id e classe (`#buscar`, `button.delete[data-id]`), e uma mutação de
# texto ou de estrutura não quebraria esses localizadores: das 16 células só 3 quebrariam. Com cada modo atacando o
# estilo de localizador que ele quebra, as 16 células da corrida 19 medem a cura (plano, P4: 4 roteiros x 4 modos x 5
# repetições) e a limitação (quebra armada, não ocorrida; o estilo do localizador escolhido por célula) fica declarada no
# roadmap. O texto muda por acréscimo de uma palavra ("Entrar agora"), porque a estratégia "papel igual e nome parecido"
# do plano (seção 3.6) é a que cobre mudança de texto; um sinônimo ("Acessar") ficaria abaixo do limiar do nome e é
# limitação declarada. Na lista de produtos, que não tem id em elemento nenhum, o modo do id renomeia o atributo
# identificador `data-id`; no login, o botão não tem id, então o modo do id renomeia o campo de login (o passo que quebra
# é o do campo, e o alvo da célula é o campo).
MODOS_DE_QUEBRA = ("id_renomeado", "classe_trocada", "texto_alterado", "estrutura_alterada")
DESCRICAO_DO_MODO = {
    "id_renomeado": "o id (ou o atributo identificador) do alvo é renomeado",
    "classe_trocada": "a classe que o localizador usa é trocada por outra",
    "texto_alterado": "o texto do alvo (ou o seu valor ou placeholder) ganha uma palavra",
    "estrutura_alterada": "o alvo é envolvido num contêiner novo e trocado de posição entre os irmãos",
}
FORMAS_DE_QUEBRA = ("harness", "php")
COOKIE_DA_QUEBRA = "quebra"
# ! Alteração de IA - Revisar: (01/11/2026, fumaça do P4) a variante do PHP ganha o cookie `quebra_pagina`, com a página da
# célula (o SCRIPT_NAME servido pelo PHP, sem a barra inicial): o modo só vale nessa página.
# ! Motivo: na fumaça, com o cookie `quebra` valendo em toda página, o modo id_renomeado da lista de produtos renomeou
# também o campo de login (admin/login.php), e o roteiro quebrou no login, antes do passo do alvo; a mutação do harness
# é por seletor e só alcança a página do alvo, então as duas formas não eram comparáveis.
COOKIE_DA_PAGINA = "quebra_pagina"
ROTEIROS_DA_CURA = ("front-busca", "front-admin-login", "front-admin-produtos", "front-cliente-reserva")
OPERACOES_DE_QUEBRA = ("renomear_id", "renomear_atributo", "trocar_classe", "trocar_atributo", "trocar_texto", "envolver_e_mover")
TEMPO_LIMITE_QUEBRA_MS = 5000     # o passo do alvo espera 5 s antes de contar como quebrado (na referência ele resolve em menos de 1 s)


def _primeiro_passo_com(cenario_id: str, seletor: str) -> int:
    for i, p in enumerate(cenario(cenario_id)["passos"]):
        if p.get("seletor") == seletor:
            return i
    raise KeyError(f"{cenario_id}: nenhum passo usa o seletor {seletor!r}")


# a página (SCRIPT_NAME sem a barra inicial) em que a variante do PHP aplica a quebra de cada roteiro
PAGINA_DA_QUEBRA = {"front-busca": "index.php", "front-admin-login": "admin/login.php", "front-admin-produtos": "admin/produtos_lista.php",
                    "front-cliente-reserva": "cliente/index.php"}


def _q(cenario_id: str, modo: str, seletor_original: str, localizador: str, alvo: dict, mutacoes: list[dict], descricao: str) -> dict:
    return {"cenario": cenario_id, "modo": modo, "seletor_original": seletor_original, "localizador": localizador, "alvo": alvo,
            "mutacoes": mutacoes, "descricao": descricao, "passo_alvo": _primeiro_passo_com(cenario_id, seletor_original),
            "pagina": PAGINA_DA_QUEBRA[cenario_id]}


_BUSCA = {"papel": "searchbox", "nome": "search", "ocorrencia": 1}
_ENTRAR = {"papel": "button", "nome": "Entrar", "ocorrencia": 1}
_LOGIN = {"papel": "textbox", "nome": "Login", "ocorrencia": 1}
_EXCLUIR = {"papel": "button", "nome": "EXCLUIR", "ocorrencia": 1}
_RESERVAR = {"papel": "button", "nome": "Reservar", "ocorrencia": 1}
_BOTAO_LOGIN = "form button[type=submit]"
QUEBRAS: list[dict] = [
    _q("front-busca", "id_renomeado", "#buscar", "#buscar", _BUSCA,
       [{"op": "renomear_id", "seletor": "#buscar", "para": "buscar_v2"}],
       "o campo de busca perde o id `buscar` (vira `buscar_v2`); o roteiro localiza por `#buscar`"),
    _q("front-busca", "classe_trocada", "#buscar", "#form-busca input.form-control", _BUSCA,
       [{"op": "trocar_classe", "seletor": "#buscar", "de": "form-control", "para": "campo-busca"}],
       "a classe `form-control` do campo vira `campo-busca`; o roteiro localiza por `#form-busca input.form-control`"),
    _q("front-busca", "texto_alterado", "#buscar", 'input[placeholder="Buscar produto"]', _BUSCA,
       [{"op": "trocar_atributo", "seletor": "#buscar", "atributo": "placeholder", "para": "Buscar produtos"}],
       "o placeholder passa de \"Buscar produto\" a \"Buscar produtos\"; o roteiro localiza pelo placeholder"),
    _q("front-busca", "estrutura_alterada", "#buscar", "#form-busca > div > input", _BUSCA,
       [{"op": "envolver_e_mover", "seletor": "#buscar", "tag": "span", "classe": "envoltorio", "mover": "fim"}],
       "o campo é envolvido num `span.envoltorio` e passa para depois do botão; o roteiro localiza por `#form-busca > div > input`"),
    _q("front-admin-login", "id_renomeado", "#login_usuario", "#login_usuario", _LOGIN,
       [{"op": "renomear_id", "seletor": "#login_usuario", "para": "usuario"}],
       "o campo de login perde o id `login_usuario` (vira `usuario`, com o `for` do rótulo); o roteiro localiza por `#login_usuario`"),
    _q("front-admin-login", "classe_trocada", "button[type=submit]", "button.btn-primary", _ENTRAR,
       [{"op": "trocar_classe", "seletor": _BOTAO_LOGIN, "de": "btn-primary", "para": "btn-entrar"}],
       "a classe `btn-primary` do botão Entrar vira `btn-entrar`; o roteiro localiza por `button.btn-primary`"),
    _q("front-admin-login", "texto_alterado", "button[type=submit]", 'role=button[name="Entrar"]', _ENTRAR,
       [{"op": "trocar_texto", "seletor": _BOTAO_LOGIN, "de": "Entrar", "para": "Entrar agora"}],
       "o botão passa de \"Entrar\" a \"Entrar agora\"; o roteiro localiza pelo papel e pelo nome \"Entrar\""),
    _q("front-admin-login", "estrutura_alterada", "button[type=submit]", ".login-form form > button", _ENTRAR,
       [{"op": "envolver_e_mover", "seletor": _BOTAO_LOGIN, "tag": "div", "classe": "acoes", "mover": "inicio"}],
       "o botão é envolvido num `div.acoes` e passa para antes dos campos; o roteiro localiza por `.login-form form > button`"),
    _q("front-admin-produtos", "id_renomeado", "button.delete[data-id='1']", "button[data-id='1']", _EXCLUIR,
       [{"op": "renomear_atributo", "seletor": "button.delete", "atributo": "data-id", "para": "data-produto", "todos": True}],
       "o atributo `data-id` dos botões EXCLUIR vira `data-produto` (a página não tem id em elemento nenhum); o roteiro localiza por `button[data-id='1']`"),
    _q("front-admin-produtos", "classe_trocada", "button.delete[data-id='1']", "button.delete[data-id='1']", _EXCLUIR,
       [{"op": "trocar_classe", "seletor": "button.delete", "de": "delete", "para": "remover", "todos": True}],
       "a classe `delete` dos botões EXCLUIR vira `remover`; o roteiro localiza por `button.delete[data-id='1']`"),
    # o nome acessível do botão é "<ícone> EXCLUIR" (o glyphicon entra no nome pelo conteúdo do CSS), por isso o localizador
    # casa o nome terminado em EXCLUIR; com " ITEM" acrescentado ele deixa de casar
    _q("front-admin-produtos", "texto_alterado", "button.delete[data-id='1']", "role=button[name=/EXCLUIR$/] >> nth=0", _EXCLUIR,
       [{"op": "trocar_texto", "seletor": "button.delete", "de": "EXCLUIR", "para": "EXCLUIR ITEM", "todos": True}],
       "os botões passam de \"EXCLUIR\" a \"EXCLUIR ITEM\"; o roteiro localiza pelo papel e pelo nome terminado em \"EXCLUIR\", primeira ocorrência"),
    _q("front-admin-produtos", "estrutura_alterada", "button.delete[data-id='1']", "table.table tbody tr:first-child td:last-child > button", _EXCLUIR,
       [{"op": "envolver_e_mover", "seletor": "button.delete", "tag": "div", "classe": "acoes", "mover": "inicio", "todos": True}],
       "cada botão EXCLUIR é envolvido num `div.acoes` e passa para antes do link ALTERAR; o roteiro localiza pelo caminho na primeira linha da tabela"),
    _q("front-cliente-reserva", "id_renomeado", "#enviar", "#enviar", _RESERVAR,
       [{"op": "renomear_id", "seletor": "#enviar", "para": "enviar_reserva"}],
       "o botão Reservar perde o id `enviar` (vira `enviar_reserva`); o roteiro localiza por `#enviar`"),
    _q("front-cliente-reserva", "classe_trocada", "#enviar", "#reserva_login input.btn-danger", _RESERVAR,
       [{"op": "trocar_classe", "seletor": "#enviar", "de": "btn-danger", "para": "btn-reservar"}],
       "a classe `btn-danger` do botão Reservar vira `btn-reservar`; o roteiro localiza por `#reserva_login input.btn-danger`"),
    _q("front-cliente-reserva", "texto_alterado", "#enviar", 'input[value="Reservar"]', _RESERVAR,
       [{"op": "trocar_atributo", "seletor": "#enviar", "atributo": "value", "para": "Reservar mesa"}],
       "o botão passa de \"Reservar\" a \"Reservar mesa\"; o roteiro localiza pelo valor \"Reservar\""),
    _q("front-cliente-reserva", "estrutura_alterada", "#enviar", "#reserva_login > input[type=submit]", _RESERVAR,
       [{"op": "envolver_e_mover", "seletor": "#enviar", "tag": "div", "classe": "acoes", "mover": "inicio"}],
       "o botão é envolvido num `div.acoes` e passa para o começo do formulário; o roteiro localiza por `#reserva_login > input[type=submit]`"),
]


def quebra(cenario_id: str, modo: str) -> dict:
    for q in QUEBRAS:
        if q["cenario"] == cenario_id and q["modo"] == modo:
            return q
    raise KeyError(f"quebra desconhecida: {cenario_id!r} em modo {modo!r}")


def validar_quebras(quebras: list[dict], cenarios: list[dict]) -> list[str]:
    """Os erros do catálogo de quebras (vazio quando está certo): célula repetida, roteiro fora da cura, modo desconhecido,
    seletor original que nenhum passo do roteiro usa, passo do alvo que não é o primeiro com esse seletor, campo em
    branco, operação desconhecida ou mutação sem seletor."""
    erros, vistos = [], set()
    ids = {c["id"] for c in cenarios}
    for q in quebras:
        chave = (q.get("cenario"), q.get("modo"))
        if chave in vistos:
            erros.append(f"{chave}: célula repetida")
        vistos.add(chave)
        if q.get("cenario") not in ROTEIROS_DA_CURA or q.get("cenario") not in ids:
            erros.append(f"{chave}: roteiro fora de ROTEIROS_DA_CURA ou do catálogo")
            continue
        if q.get("modo") not in MODOS_DE_QUEBRA:
            erros.append(f"{chave}: modo desconhecido")
        passos = cenario(q["cenario"])["passos"]
        usados = [i for i, p in enumerate(passos) if p.get("seletor") == q.get("seletor_original")]
        if not usados:
            erros.append(f"{chave}: nenhum passo usa o seletor original {q.get('seletor_original')!r}")
        elif q.get("passo_alvo") != usados[0]:
            erros.append(f"{chave}: passo_alvo {q.get('passo_alvo')} não é o primeiro passo com o seletor original ({usados[0]})")
        for campo in ("localizador", "descricao", "pagina"):
            if not q.get(campo):
                erros.append(f"{chave}: sem {campo}")
        alvo = q.get("alvo") or {}
        if not (alvo.get("papel") and alvo.get("nome")):
            erros.append(f"{chave}: alvo sem papel ou nome")
        if not q.get("mutacoes"):
            erros.append(f"{chave}: sem mutações")
        for m in q.get("mutacoes") or []:
            if m.get("op") not in OPERACOES_DE_QUEBRA:
                erros.append(f"{chave}: operação {m.get('op')!r} desconhecida")
            if not m.get("seletor"):
                erros.append(f"{chave}: mutação sem seletor")
    return erros


def cenario_com_localizador(cenario_: dict, quebra_: dict) -> dict:
    """Uma cópia do roteiro em que todo passo que usa o seletor original do alvo passa a usar o localizador da célula, com
    o tempo limite da quebra; o catálogo não muda."""
    import copy
    novo = copy.deepcopy(cenario_)
    for p in novo["passos"]:
        if p.get("seletor") == quebra_["seletor_original"]:
            p["seletor"] = quebra_["localizador"]
            p["ate_ms"] = TEMPO_LIMITE_QUEBRA_MS
    novo["quebra"] = {"modo": quebra_["modo"], "localizador": quebra_["localizador"], "seletor_original": quebra_["seletor_original"],
                      "passo_alvo": quebra_["passo_alvo"]}
    return novo


def script_de_quebra(mutacoes: list[dict], modo: str = "") -> str:
    """O script que o harness injeta antes de a página carregar: no DOMContentLoaded aplica as mutações, em ordem, sobre o
    DOM já montado (os scripts embutidos da página já rodaram e os manipuladores de evento ficam nos mesmos elementos),
    e anota em `<html data-quebra data-quebra-aplicada>` o modo e quantas mutações encontraram o seletor."""
    import json as _json
    return r"""(() => {
  const modo = %s;
  const mutacoes = %s;
  const aplicar = () => {
    let feitas = 0;
    for (const m of mutacoes) {
      try {
        const alvos = m.todos ? Array.from(document.querySelectorAll(m.seletor)) : [document.querySelector(m.seletor)].filter(Boolean);
        if (!alvos.length) continue;
        for (const el of alvos) {
          if (m.op === 'renomear_id') {
            const de = el.id;
            el.id = m.para;
            if (de) document.querySelectorAll('label[for="' + CSS.escape(de) + '"]').forEach((l) => l.setAttribute('for', m.para));
          } else if (m.op === 'renomear_atributo') {
            const v = el.getAttribute(m.atributo);
            if (v !== null) { el.removeAttribute(m.atributo); el.setAttribute(m.para, v); }
          } else if (m.op === 'trocar_classe') {
            el.classList.replace(m.de, m.para);
          } else if (m.op === 'trocar_atributo') {
            el.setAttribute(m.atributo, m.para);
          } else if (m.op === 'trocar_texto') {
            const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
            let n;
            while ((n = w.nextNode())) { if (n.nodeValue.includes(m.de)) n.nodeValue = n.nodeValue.replace(m.de, m.para); }
          } else if (m.op === 'envolver_e_mover') {
            const pai = el.parentNode;
            const w = document.createElement(m.tag || 'div');
            w.className = m.classe || '';
            pai.insertBefore(w, el);
            w.appendChild(el);
            if (m.mover === 'fim') pai.appendChild(w);
            else if (m.mover === 'inicio') pai.insertBefore(w, pai.firstChild);
            else if (m.mover && m.mover.startsWith('antes_de:')) { const ref = pai.querySelector(m.mover.slice(9)); if (ref) pai.insertBefore(w, ref); }
          }
        }
        feitas++;
      } catch (e) { console.error('quebra ' + modo + ': ' + e); }
    }
    document.documentElement.dataset.quebra = modo;
    document.documentElement.dataset.quebraAplicada = String(feitas);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', aplicar); else aplicar();
})();
""" % (_json.dumps(modo, ensure_ascii=False), _json.dumps(mutacoes, ensure_ascii=False))


def armar_quebra(pagina, quebra_: dict, forma: str, base: str = BASE_PADRAO) -> dict:
    """Arma a quebra da célula na página antes de navegar: `harness` injeta o script por `add_init_script`; `php` grava o
    cookie `quebra=<modo>` no contexto, que a variante do front lê em toda página. Devolve o que foi armado."""
    if forma not in FORMAS_DE_QUEBRA:
        raise ValueError(f"forma {forma!r} fora de {FORMAS_DE_QUEBRA}")
    if forma == "harness":
        pagina.add_init_script(script_de_quebra(quebra_["mutacoes"], quebra_["modo"]))
        return {"forma": forma, "modo": quebra_["modo"], "mutacoes": len(quebra_["mutacoes"]), "como": "add_init_script no DOMContentLoaded"}
    pagina.context.add_cookies([{"name": COOKIE_DA_QUEBRA, "value": quebra_["modo"], "url": base},
                                {"name": COOKIE_DA_PAGINA, "value": quebra_["pagina"], "url": base}])
    return {"forma": forma, "modo": quebra_["modo"], "mutacoes": len(quebra_["mutacoes"]),
            "como": f"cookies {COOKIE_DA_QUEBRA}={quebra_['modo']} e {COOKIE_DA_PAGINA}={quebra_['pagina']} lidos por quebra.php"}


# ! Alteração de IA - Revisar: (04/11/2026, P6) roteiro_com_seletor: o roteiro com um seletor no lugar do localizador quebrado
# (marcando o passo como curado); a reexecução da cura (executar_fase4.Cura._roteiro_curado) e a conferência da linha de base
# manual (conferir_localizador_manual.py) usam a mesma troca.
# ! Motivo: o Task Success do cenário de localizador do agente e o do integrante têm de ser conferidos do mesmo jeito para a Fase 5
# comparar os dois; com a troca num lugar só, uma mudança nela vale para os dois lados.
def roteiro_com_seletor(cenario_: dict, quebra_: dict, seletor: str) -> dict:
    """O cenário com `seletor` em todo passo que usava o localizador quebrado, marcado como curado; o original não muda."""
    import copy
    novo = copy.deepcopy(cenario_)
    for p in novo["passos"]:
        if p.get("seletor") == quebra_["localizador"]:
            p["seletor"] = seletor
            p["curado"] = True
    return novo


# ! Alteração de IA - Revisar: (04/11/2026, P6) motivo_do_roteiro: a ficha da falha de um roteiro que parou, numa linha: o passo,
# o que ele fazia e o erro (cortado em 200 caracteres), ou a conferência que falhou com o esperado e o observado.
# ! Motivo: o ensaio da Fase 5 (executar_fase4.rodar_cenarios) grava esta ficha em cenarios.jsonl (campo motivo_deteccao) e o
# ajudante da linha de base manual (linha_de_base_manual.py) a mostra ao integrante; com o texto montado num lugar só, o
# integrante recebe a mesma falha que a detecção do agente acusou.
def _uma_linha(texto, limite: int) -> str:
    return " ".join(str(texto).split())[:limite]


def motivo_do_roteiro(resultado: dict) -> str | None:
    """A ficha da falha do roteiro em uma linha; None quando o roteiro passou."""
    if resultado.get("passou"):
        return None
    cf = resultado.get("conferencia_falha") or {}
    n = (resultado.get("passo_falho") or 0) + 1
    if resultado.get("erro"):
        nome = cf.get("nome") or f"passo {n}"
        return f"o {nome} não terminou: {_uma_linha(resultado['erro'], 200)}"
    return (f'a conferência "{cf.get("nome")}" (passo {n}) falhou: esperado {_uma_linha(cf.get("esperado"), 80)}, '
            f'observado {_uma_linha(cf.get("observado"), 120)}')


# ------------------------------------------------------------------ cronômetro e critério da Fase 5

def mttr_segundos(deteccao: str, validacao: str) -> float:
    """Da detecção (primeira conferência que falhou) até a correção validada na reexecução, em segundos."""
    a, b = dt.datetime.fromisoformat(deteccao), dt.datetime.fromisoformat(validacao)
    return round((b - a).total_seconds(), 3)


def task_success(resultado: dict) -> bool:
    """Fluxo restaurado e roteiro concluído sem erro: o cenário passou e nenhuma conferência falhou."""
    return bool(resultado.get("passou")) and all(c.get("passou") for c in resultado.get("conferencias") or [])


# ------------------------------------------------------------------ os dez cenários do ensaio da Fase 5 (pacote P6)

# ! Alteração de IA - Revisar: (04/11/2026, P6) o catálogo dos dez cenários da ficha 36 (decisão 79): seis de contrato em
# produtos_api.php (roteiro api-catalogo), um por modo, e quatro de localizador, um por roteiro do front legado, cada um com um
# modo de quebra fixo, armado pelo harness. A lista da opção (a) trocou latency por escala_ou_unidade_errada (TROCA_DA_FICHA_36).
# ! Motivo: a decisão 79 fixou 6 de contrato e 4 de localizador e pediu trocar cenários de contrato por modos novos da ficha 28 que
# cobrissem mais classes; os seis da opção (a) cobriam as classes 1, 2, 3 e 5, e com uma troca os seis cobrem as cinco classes de
# contrato (a 6, efeito, vem dos quatro de localizador). Os quatro modos de quebra entram um em cada roteiro, para o ensaio passar
# pelos quatro; a forma "harness" deixa o front intocado (ficha 29).
TROCA_DA_FICHA_36 = {
    "sai": "latency", "entra": "escala_ou_unidade_errada",
    "motivo": ("os seis modos da opção (a) cobriam as classes 1, 2, 3 e 5; a decisão 79 pede trocar cenários de contrato por modos "
               "novos da ficha 28 que cubram mais classes. Sai latency, que repete a classe 5 de error_500 e tem o MTTR dominado pela "
               "espera do tempo limite; entra escala_ou_unidade_errada em preco, da classe 4 (tradução), que nenhum dos seis cobria."),
}
CENARIOS_DE_CONTRATO = tuple(
    {"id": f"contrato-{modo}", "tipo": "contrato", "cenario": "api-catalogo", "modo": modo, "campo": campo, "causa": causa, "classe": classe,
     "nivel": nivel}
    for modo, campo, causa, classe, nivel in (
        ("malformed_json", None, "resposta_truncada", 1, 1),
        ("field_missing", "preco", "campo_ausente", 2, 1),
        ("field_renamed", "preco", "campo_renomeado", 2, 2),
        ("type_drift", "preco", "tipo_divergente", 3, 2),
        ("escala_ou_unidade_errada", "preco", "escala_ou_unidade_errada", 4, 2),
        ("error_500", None, "erro_interno_do_servidor", 5, 1),
    ))
CENARIOS_DE_LOCALIZADOR = tuple(
    {"id": f"localizador-{roteiro}", "tipo": "localizador", "cenario": roteiro, "modo": modo, "forma": "harness", "campo": None,
     "causa": "localizador_quebrado", "classe": 6, "nivel": 2}
    for roteiro, modo in (("front-busca", "id_renomeado"), ("front-admin-login", "classe_trocada"),
                          ("front-admin-produtos", "texto_alterado"), ("front-cliente-reserva", "estrutura_alterada")))
CENARIOS_DO_ENSAIO = CENARIOS_DE_CONTRATO + CENARIOS_DE_LOCALIZADOR
LINHAS_DO_DIAGNOSTICO = ("CAUSA_RAIZ", "CAMPO", "IMPACTO", "FONTE")


# ! Alteração de IA - Revisar: (04/11/2026, P6) o cronômetro em relógio monotônico (mttr_monotonico), a conferência do
# diagnóstico em código da ficha 35 (diagnostico_conferido) e o Task Success do cenário de contrato (task_success_contrato).
# ! Motivo: ficha 35 (a), decisão 79: na quebra de contrato o agente não corrige a API, ele diagnostica; o resultado é o
# diagnóstico conferido em código (quatro linhas válidas, causa dentro das 23, campo existente no caso), o MTTR para nele e o Task
# Success é a causa e o campo certos. mttr_segundos (ISO, segundos inteiros) não serve para tempos de fração de segundo.
def mttr_monotonico(t_deteccao: float | None, t_fim: float | None, descontar: float = 0.0) -> float | None:
    """Da detecção ao fim do cronômetro (diagnóstico conferido ou reexecução validada), em segundos, descontando o tempo de
    restaurar o banco entre os dois; None sem detecção, sem fim ou com o fim antes da detecção."""
    if t_deteccao is None or t_fim is None or t_fim < t_deteccao:
        return None
    return round(max(0.0, t_fim - t_deteccao - (descontar or 0.0)), 3)


def diagnostico_conferido(resposta: str | None, caso: dict) -> dict:
    """Ficha 35: as quatro linhas presentes, a causa dentro das 23 (sem acento, como avaliar.py) e o campo citado existente no
    contrato ou no corpo do caso (ou "nenhum")."""
    import avaliar
    texto = (resposta or "").replace("*", "").replace("`", "")
    linhas = {n: re.search(rf"^\s*{n}\s*:\s*\S", texto, re.IGNORECASE | re.MULTILINE) is not None for n in LINHAS_DO_DIAGNOSTICO}
    lido = avaliar.extrair(texto)
    causa = lido["causa_raiz"]
    causa_ok = causa is not None and avaliar._normalizar(causa) in avaliar._PERMITIDAS
    campo = (lido["campo"] or "").strip()
    if not campo or "nenhum" in avaliar._normalizar(campo):
        campo_ok, campo_lido = True, None
    else:
        token = re.split(r"[\s,;()]+", campo.strip("'\". "))[0]
        e = caso.get("entrada") or {}
        onde = f"{e.get('contrato') or ''}\n{e.get('corpo') or ''}"
        campo_ok = bool(token) and re.search(rf"(?<!\w){re.escape(token)}(?!\w)", onde) is not None
        campo_lido = token
    return {"conferido": all(linhas.values()) and causa_ok and campo_ok, "linhas": linhas, "causa_no_conjunto": causa_ok,
            "campo_no_caso": campo_ok, "causa": causa, "campo": campo_lido}


def task_success_contrato(conferencia: dict | None, causa_esperada: str, campo_esperado: str | None) -> bool:
    """Ficha 35: no cenário de contrato, Task Success é o diagnóstico conferido com a causa e o campo certos."""
    import avaliar
    if not conferencia or not conferencia.get("conferido"):
        return False
    if avaliar._normalizar(conferencia.get("causa") or "") != avaliar._normalizar(causa_esperada):
        return False
    if campo_esperado is None:
        return conferencia.get("campo") is None
    return conferencia.get("campo") is not None and avaliar._normalizar(campo_esperado) in avaliar._normalizar(conferencia["campo"])
