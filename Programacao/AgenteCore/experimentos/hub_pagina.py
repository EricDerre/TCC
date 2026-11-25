#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (25/11/2026, Pós-Fase 4, pacote Q6): a apresentação do hub central. Nesta etapa, o conversor de
# Markdown para HTML que monta os blocos do relatório v3 e a árvore de decisão na página (`md_para_html`): títulos, parágrafos, tabelas,
# listas com um nível de sublista, listas numeradas, citações, blocos de código e, dentro da linha, código, negrito, itálico e link.
# ! Motivo: plano aprovado da Pós-Fase 4, seção 3.6 ("a página no padrão do painel, HTML e JS gerados por Python"), e ficha 97 (decisão 157).
# O relatório v3 e a árvore carregam texto que veio de fora do projeto (o corpo da resposta das cobaias, a mensagem de erro do navegador, o
# que o modelo escreveu); por isso todo texto é escapado antes de qualquer marcação, e só endereço http ou https vira link: um
# `<script>` dentro de um corpo de resposta aparece como texto na página e nunca é executado. O conversor do painel
# (`ferramentas/painel_textos.md_doc_para_html`) não trata citação nem bloco de código, que os relatórios usam, e o hub não depende da pasta
# `ferramentas/`, que é da documentação.
"""A apresentação do hub central (Pós-Fase 4, pacote Q6): o conversor de Markdown e a página."""
from __future__ import annotations

import html
import re
import unicodedata

_COMENTARIO = re.compile(r"<!--.*?-->", re.DOTALL)
_TITULO = re.compile(r"^(#{1,6})\s+(.*)$")
_ITEM = re.compile(r"^(\s*)- (.*)$")
_NUMERADO = re.compile(r"^\d+\. (.*)$")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_PIPE = re.compile(r"(?<!\\)\|")


def esc(texto) -> str:
    return html.escape("" if texto is None else str(texto), quote=True)


def slug(texto: str) -> str:
    """O texto em minúsculas, sem acento, com hífen no lugar do que não é letra nem número (para o id de um bloco)."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", sem_acento).strip("-")


def inline(texto: str) -> str:
    """Código, negrito, itálico e link de um trecho de linha, sobre o texto já escapado. Link só para endereço http ou https; qualquer outro
    destino (arquivo do repositório, `javascript:`) fica como texto, com o destino na dica."""
    s = html.escape(texto, quote=False)
    codigos: list[str] = []

    def guardar(m: re.Match) -> str:
        codigos.append(m.group(1))
        return f"\x00{len(codigos) - 1}\x00"

    s = re.sub(r"`([^`]+)`", guardar, s)

    def link(m: re.Match) -> str:
        rotulo, destino = m.group(1), m.group(2)
        if re.match(r"^https?://", destino):
            return f'<a href="{html.escape(destino, quote=True)}" target="_blank" rel="noopener noreferrer">{rotulo}</a>'
        return f'<span class="ref">{rotulo}</span>'

    s = _LINK.sub(link, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*\n]+?)\*(?![*\w])", r"<em>\1</em>", s)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codigos[int(m.group(1))]}</code>", s)


def _celulas(linha: str) -> list[str]:
    s = linha.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in _PIPE.split(s)]


def _tabela(linhas: list[str]) -> str:
    cab = _celulas(linhas[0])
    corpo = [_celulas(l) for l in linhas[1:] if not re.match(r"^\|\s*:?-", l)]
    th = "".join(f"<th>{inline(c)}</th>" for c in cab)
    trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in corpo)
    return f'<div class="tabela"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def _lista(linhas: list[str], i: int) -> tuple[str, int]:
    itens: list[list] = []
    while i < len(linhas) and _ITEM.match(linhas[i]):
        m = _ITEM.match(linhas[i])
        if len(m.group(1)) == 0 or not itens:
            itens.append([m.group(2), []])
        else:
            itens[-1][1].append(m.group(2))
        i += 1
    saida = []
    for texto, subs in itens:
        sub = ("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in subs) + "</ul>") if subs else ""
        saida.append(f"<li>{inline(texto)}{sub}</li>")
    return "<ul>" + "".join(saida) + "</ul>", i


def md_para_html(md: str) -> str:
    """O Markdown dos relatórios e das árvores em HTML. Os comentários (`<!-- -->`) saem; todo o resto do texto é escapado."""
    linhas = _COMENTARIO.sub("", md).split("\n")
    out: list[str] = []
    par: list[str] = []
    i = 0

    def fecha_par() -> None:
        if par:
            out.append(f"<p>{inline(' '.join(par))}</p>")
            par.clear()

    while i < len(linhas):
        l = linhas[i]
        if not l.strip():
            fecha_par()
            i += 1
            continue
        if l.startswith("```"):
            fecha_par()
            i += 1
            codigo = []
            while i < len(linhas) and not linhas[i].startswith("```"):
                codigo.append(linhas[i])
                i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(codigo), quote=False) + "</code></pre>")
            continue
        if l.startswith("|"):
            fecha_par()
            tab = []
            while i < len(linhas) and linhas[i].startswith("|"):
                tab.append(linhas[i])
                i += 1
            out.append(_tabela(tab))
            continue
        if l.startswith(">"):
            fecha_par()
            cit = []
            while i < len(linhas) and linhas[i].startswith(">"):
                cit.append(inline(linhas[i][1:].lstrip()))
                i += 1
            out.append("<blockquote>" + "<br>".join(cit) + "</blockquote>")
            continue
        m = _TITULO.match(l)
        if m:
            fecha_par()
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
            continue
        if _ITEM.match(l):
            fecha_par()
            bloco, i = _lista(linhas, i)
            out.append(bloco)
            continue
        if _NUMERADO.match(l):
            fecha_par()
            itens = []
            while i < len(linhas) and _NUMERADO.match(linhas[i]):
                itens.append(f"<li>{inline(_NUMERADO.match(linhas[i]).group(1))}</li>")
                i += 1
            out.append("<ol>" + "".join(itens) + "</ol>")
            continue
        par.append(l.strip())
        i += 1
    fecha_par()
    return "\n".join(out)


def texto_puro(marcado: str) -> str:
    """O texto de um HTML gerado por `md_para_html`, sem as marcas (para a busca na lista de casos)."""
    return html.unescape(re.sub(r"<[^>]+>", " ", marcado)).strip()


# ! Alteração de IA - Revisar: (25/11/2026, pacote Q6, etapa 2) `arvore_para_html` monta a aba "Árvore de decisão" a partir do JSON de
# `arvore_de_decisao.arvore_do_caso`: um cartão por decisão do agente, com a escolha, cada afirmação precedida da origem (observado, conferido,
# declarado, desconhecido) e a tabela das alternativas; o que o modelo escreveu fica num cartão à parte, com o rótulo "texto do modelo".
# ! Motivo: o plano (seções 3.4 e 3.6) diz que a árvore sai em JSON "para o hub"; o Markdown da árvore traz a origem no fim de cada frase,
# entre parênteses, e na página a origem precisa aparecer antes do texto, como etiqueta de cor, para o analista separar de relance o que o
# código mediu do que o modelo só declarou (plano, princípio 3). A tabela das alternativas é a mesma do Markdown, sem regra copiada.
def arvore_para_html(arvore: dict) -> str:
    import arvore_de_decisao as ad

    r = arvore["resumo"]
    legenda = " ".join(f'<span class="legenda-origem origem-{rot}">{esc(rot)}</span> {esc(sig)};' for rot, sig in arvore["rotulos"].items())
    partes = [f'<p class="legenda">Cada frase começa com a origem dela: {legenda} o que o modelo escreveu fica no último cartão.</p>',
              (f'<p class="resumo-da-arvore">{r["decisoes"]} decisões e {r["afirmacoes"]} afirmações; '
               + ("há divergência entre o declarado e o conferido" if r["divergencia"] else "nenhuma divergência entre o declarado e o conferido")
               + ("; houve cura de localizador" if r["cura"] else "") + (f'; confiança {esc(r["confianca"])}' if r.get("confianca") else "") + ".</p>")]
    for d in arvore["decisoes"]:
        escolha = d.get("escolha")
        if d["chave"] == "causa":
            linha = ("Escolha: " + (f"`{escolha}` ({d.get('causa_em_palavras')})" if escolha is not None else "nenhuma causa respondida")
                     + (f"; segunda: `{d['segunda']}`" if d.get("segunda") else "")
                     + (f"; confiança {d['confianca']['palavra']}" if (d.get("confianca") or {}).get("palavra") else "") + ".")
        elif d["chave"] == "cura":
            linha = "Escolha: " + (f"`{escolha}` (`{d.get('seletor')}`)" if d.get("curado") else "nenhum candidato aplicado") + "."
        else:
            linha = f"Escolha: {escolha}." if escolha else "Escolha: nada registrado."
        partes += [f'<section class="decisao" data-decisao="{esc(d["chave"])}">', f'<h3>Decisão {d["numero"]}: {esc(d["titulo"])}</h3>',
                   f'<p class="escolha">{inline(linha)}</p>', '<ul class="afirmacoes">']
        partes += [f'<li><span class="origem origem-{esc(a["origem"])}">{esc(a["origem"])}</span> {inline(a["texto"])}</li>' for a in d["afirmacoes"]]
        partes.append("</ul>")
        if d.get("diferencas"):
            linhas = "".join(f"<tr><td>{inline(str(x['onde']))}</td><td>{inline(str(x['esperado']))}</td><td>{inline(str(x['recebido']))}</td></tr>" for x in d["diferencas"])
            partes.append(f'<div class="tabela"><table><thead><tr><th>Onde</th><th>Esperado</th><th>Recebido</th></tr></thead><tbody>{linhas}</tbody></table></div>')
        if d["chave"] == "cura" and d.get("erro"):
            partes.append(f'<p class="nota">Mensagem do navegador, como veio:</p><pre><code>{esc(d["erro"])}</code></pre>')
        tabela = ad._tabela_de_alternativas(d)
        if tabela:
            partes.append(md_para_html(tabela))
        partes.append("</section>")
    tm = arvore.get("texto_do_modelo") or {}
    partes += ['<section class="texto-do-modelo">', "<h3>Texto do modelo</h3>",
               f'<p class="nota"><span class="selo-modelo">{esc(ad.TEXTO_DO_MODELO)}</span> As linhas escritas pelo modelo, como vieram e sem garantia.</p>']
    for nome in ("impacto", "fonte"):
        partes.append(f"<blockquote>{esc(nome.upper())}: {esc(tm[nome])}</blockquote>" if tm.get(nome) else f'<p class="nota">A linha {nome.upper()} não veio na resposta.</p>')
    if tm.get("raciocinio"):
        partes.append(f'<p class="nota">Texto escrito antes das quatro linhas:</p><pre><code>{esc(tm["raciocinio"])}</code></pre>')
    if tm.get("resposta"):
        partes.append(f'<p class="nota">Resposta inteira:</p><pre><code>{esc(tm["resposta"])}</code></pre>')
    partes.append("</section>")
    return "\n".join(partes)


# ! Alteração de IA - Revisar: (25/11/2026, pacote Q6, etapa 2) a página do hub: `pagina()` devolve só a estrutura (cabeçalho com o nome de
# quem revisa e os filtros, a lista de casos, o caso com as abas Relatório, Árvore de decisão e Trilha, a evidência ao lado e a caixa da
# revisão); o estilo (`CSS`) e o programa (`JS`) são servidos em endereços próprios, `/hub.css` e `/hub.js`.
# ! Motivo: plano, seção 3.6 (itens 1 a 6), e ficha 97. O programa fica fora do HTML para o servidor poder mandar ao navegador a regra de que
# só roda script vindo do próprio hub (cabeçalho Content-Security-Policy sem `unsafe-inline`): se algum texto de cobaia ou de modelo escapasse
# do conversor com uma marcação de script, o navegador se recusaria a executá-la. O texto que o analista digita e o que vem da evidência entram
# na página por `textContent`, nunca como marcação. As cores e as fontes são as do painel do projeto, com tema escuro pelo sistema.
def pagina() -> str:
    def opcao_vazia(rotulo: str) -> str:
        return f'<option value="">{esc(rotulo)}</option>'

    return "\n".join([
        "<!doctype html>", '<html lang="pt-BR">', "<head>", '<meta charset="utf-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Hub de revisão do agente de QA</title>", '<link rel="stylesheet" href="/hub.css">', "</head>", "<body>",
        '<header class="topo">',
        '<div class="marca"><strong>Hub de revisão</strong><span>o agente comenta; o veredito é do analista</span></div>',
        '<label class="campo">Quem está revisando <input id="nome-do-revisor" type="text" maxlength="80" autocomplete="off" placeholder="seu nome"></label>',
        f'<label class="campo">Corrida <select id="filtro-corrida">{opcao_vazia("todas")}</select></label>',
        '<label class="campo">Procurar <input id="filtro-texto" type="search" placeholder="caso, causa, título"></label>',
        '<label class="campo marcar"><input id="filtro-sem-veredito" type="checkbox"> só sem veredito</label>',
        '<span id="contagem-de-casos" class="contagem"></span>',
        '<p id="erro" role="alert" aria-live="assertive"></p>',
        "</header>",
        '<div class="corpo">',
        '<aside class="lateral" aria-label="Casos"><ul id="lista-de-casos"></ul></aside>',
        '<main id="caso" hidden>',
        '<div id="cabecalho-do-caso">',
        '<h1 id="titulo-do-caso"></h1>',
        '<p id="meta-do-caso" class="meta"></p>',
        '<div class="linha-da-iteracao">',
        '<label class="campo">Iteração <select id="seletor-de-iteracao"></select></label>',
        '<label class="campo marcar"><input id="marca-lido" type="checkbox"> li esta iteração</label>',
        '<span id="aviso-lido" class="aviso"></span>',
        '<span id="aviso-de-iteracao" class="aviso"></span>',
        "</div>",
        '<div id="mudancas"></div>',
        "</div>",
        '<nav class="abas" aria-label="Partes do caso">',
        '<button type="button" data-aba="relatorio">Relatório</button>',
        '<button type="button" data-aba="arvore">Árvore de decisão</button>',
        '<button type="button" data-aba="trilha">Trilha</button>',
        "</nav>",
        '<section id="aba-relatorio" class="aba">',
        '<div class="duas-colunas">',
        '<div class="relatorio">',
        '<div id="comentario-do-agente" class="cartao"></div>',
        '<div id="preambulo" class="nota"></div>',
        '<div id="blocos"></div>',
        '<div id="rastro" class="nota"></div>',
        "</div>",
        '<div id="evidencia" class="cartao"><h2>Evidência</h2><div id="evidencia-abas" class="abas-menores"></div><div id="evidencia-conteudo"></div></div>',
        "</div>",
        '<section id="revisao" class="cartao">',
        "<h2>Revisão do analista</h2>",
        '<p id="veredito-atual"></p>',
        '<p id="causa-atual"></p>',
        '<h3>Comentários gerais</h3>',
        '<div id="conversas-gerais"></div>',
        '<button type="button" id="comentar-geral">Comentar a revisão</button>',
        '<h3>Severidade, prioridade e estado (seção 5.5 do syllabus)</h3>',
        '<div class="linha-de-campos">',
        f'<label class="campo">Severidade <select id="severidade">{opcao_vazia("em branco")}</select></label>',
        f'<label class="campo">Prioridade <select id="prioridade">{opcao_vazia("em branco")}</select></label>',
        '<label class="campo">Estado <select id="estado-55"></select></label>',
        '<button type="button" id="gravar-55">Gravar os três campos</button>',
        '<span id="aviso-55" class="aviso"></span>',
        "</div>",
        "<h3>A causa é outra</h3>",
        '<div class="linha-de-campos">',
        f'<label class="campo">Causa corrigida <select id="causa-sugerida">{opcao_vazia("não sugerir")}</select></label>',
        '<label class="campo">Campo <input id="campo-sugerido" type="text" maxlength="120" placeholder="opcional"></label>',
        "</div>",
        "<h3>Veredito</h3>",
        '<div class="linha-de-campos">',
        '<label class="campo">Veredito <select id="veredito"></select></label>',
        f'<label class="campo">Desfecho <select id="desfecho">{opcao_vazia("sem desfecho")}</select></label>',
        "</div>",
        '<label class="campo largo">Resumo da revisão <textarea id="resumo-da-revisao" rows="3" maxlength="4000"></textarea></label>',
        '<h3>Rascunhos <span id="contagem-de-rascunhos" class="contagem"></span></h3>',
        '<div id="rascunhos"></div>',
        '<button type="button" id="enviar-revisao" class="principal">Enviar revisão</button>',
        "</section>",
        "</section>",
        '<section id="aba-arvore" class="aba" hidden></section>',
        '<section id="aba-trilha" class="aba" hidden></section>',
        "</main>",
        '<p id="vazio" class="nota">Escolha um caso na lista.</p>',
        "</div>",
        '<button type="button" id="comentar-trecho" hidden>Comentar o trecho</button>',
        '<div id="form-comentario" class="cartao" hidden>',
        '<blockquote class="trecho-citado" hidden></blockquote>',
        '<label class="campo largo">Comentário <textarea id="texto-do-comentario" rows="3" maxlength="4000"></textarea></label>',
        '<div class="linha-de-campos">',
        f'<label class="campo">Rótulo <select id="rotulo-do-comentario">{opcao_vazia("sem rótulo")}</select></label>',
        '<label class="campo marcar"><input id="bloqueante" type="checkbox"> bloqueante</label>',
        '<button type="button" id="comentar-agora" class="principal">Comentar agora</button>',
        '<button type="button" id="guardar-rascunho">Guardar rascunho</button>',
        '<button type="button" id="cancelar-comentario">Cancelar</button>',
        "</div>",
        "</div>",
        '<script src="/hub.js" defer></script>',
        "</body>", "</html>", ""])


# ! Alteração de IA - Revisar: (25/11/2026, pacote Q6, etapa 2) o estilo da página do hub, servido em `/hub.css`: as cores e as fontes do painel
# do projeto (`ferramentas/gerar_dashboard.py`), com tema escuro pelo sistema; cabeçalho fixo, lista de casos à esquerda, o caso à direita com
# o relatório e a evidência lado a lado; etiquetas de cor para a origem de cada afirmação da árvore e para o estado de cada conversa.
# ! Motivo: plano, seção 3.6 ("a página no padrão do painel"); a evidência fica presa ao lado do relatório enquanto ele rola, porque a pesquisa
# (Bacchelli e Bird, 2013, levantamento §6.15.1) diz que entender a mudança é o centro da revisão, e o analista compara os dois o tempo todo.
CSS = r"""
:root{--bg:#f6f4ee;--bg2:#fdfcf9;--ink:#1f2328;--ink2:#4c545c;--linha:#d8d3c7;--acento:#2f5d8a;--acento2:#dbe7f3;--bom:#2e7d4f;--meio:#96610f;--ruim:#b3392b;
--marca:#fff1b8;--sombra:0 1px 2px rgba(20,25,30,.06),0 8px 24px rgba(20,25,30,.06);
--fd:"Source Serif 4",Georgia,"Times New Roman",serif;--fb:"IBM Plex Sans","Segoe UI",Roboto,Arial,sans-serif;--fm:"IBM Plex Mono",Consolas,monospace}
@media (prefers-color-scheme:dark){:root{color-scheme:dark;--bg:#15181c;--bg2:#1d2126;--ink:#e8e6df;--ink2:#a8adb4;--linha:#333a42;--acento:#7fb0e0;--acento2:#243342;
--bom:#5cc48a;--meio:#e0a84a;--ruim:#e46b5c;--marca:#5a4a12;--sombra:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.35)}}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 var(--fb);display:flex;flex-direction:column}
[hidden]{display:none!important}
h1,h2,h3,h4{font-family:var(--fd);line-height:1.25;margin:0 0 8px}
h1{font-size:22px}h2{font-size:18px}h3{font-size:15px;margin-top:16px}h4{font-size:14px;margin-top:12px}
code,pre{font-family:var(--fm);font-size:13px}
code{background:var(--acento2);border-radius:4px;padding:0 4px;overflow-wrap:anywhere}
pre{background:var(--bg);border:1px solid var(--linha);border-radius:8px;padding:10px 12px;overflow:auto;max-height:420px;white-space:pre-wrap;overflow-wrap:anywhere;margin:8px 0}
pre code{background:none;padding:0}
blockquote{margin:8px 0;padding:6px 12px;border-left:3px solid var(--linha);color:var(--ink2);overflow-wrap:anywhere}
a{color:var(--acento)}
button,select,input,textarea{font:14px var(--fb);color:var(--ink);background:var(--bg2);border:1px solid var(--linha);border-radius:6px;padding:5px 9px}
select,input{max-width:100%}
button{cursor:pointer}button:hover{border-color:var(--acento)}
button.principal{background:var(--acento);color:var(--bg2);border-color:var(--acento);font-weight:600}
:focus-visible{outline:2px solid var(--acento);outline-offset:2px}
textarea{width:100%;resize:vertical}
.topo{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;padding:10px 16px;background:var(--bg2);border-bottom:1px solid var(--linha);box-shadow:var(--sombra)}
.marca{display:flex;flex-direction:column;line-height:1.2;margin-right:8px}.marca strong{font-family:var(--fd);font-size:18px}.marca span{font-size:12px;color:var(--ink2)}
.campo{display:flex;flex-direction:column;font-size:12px;color:var(--ink2);gap:2px}
.campo.marcar{flex-direction:row;align-items:center;gap:6px;font-size:13px;color:var(--ink)}
.campo.largo{width:100%;margin:8px 0}
.contagem{font-size:13px;color:var(--ink2)}
#erro{margin:0;color:var(--ruim);font-weight:600;flex-basis:100%}#erro:empty{display:none}
.corpo{flex:1;min-height:0;display:grid;grid-template-columns:330px minmax(0,1fr)}
.lateral{overflow-y:auto;border-right:1px solid var(--linha);background:var(--bg2)}
#lista-de-casos{list-style:none;margin:0;padding:0}
.item-caso{display:flex;flex-direction:column;gap:3px;padding:10px 14px;border-bottom:1px solid var(--linha);cursor:pointer}
.item-caso:hover{background:var(--acento2)}.item-caso.aberto{background:var(--acento2);box-shadow:inset 3px 0 0 var(--acento)}
.titulo-do-item{font-weight:600;font-size:14px;line-height:1.3}
.meta{font-size:12px;color:var(--ink2);margin:0}
.etiquetas{display:flex;flex-wrap:wrap;gap:4px}
.etiqueta,.origem,.legenda-origem,.estado-da-conversa,.tipo,.rotulo,.bloqueante,.selo-modelo{display:inline-block;font:500 11px/1.5 var(--fm);border:1px solid var(--linha);border-radius:999px;padding:0 7px;white-space:nowrap}
.conf-alto{color:var(--bom);border-color:var(--bom)}.conf-medio{color:var(--meio);border-color:var(--meio)}.conf-baixo,.alerta,.bloqueante{color:var(--ruim);border-color:var(--ruim)}
.veredito{background:var(--acento);color:var(--bg2);border-color:var(--acento)}.conversa-ativa{color:var(--acento);border-color:var(--acento)}
main{overflow-y:auto;padding:16px 20px 60px}
#vazio{padding:24px}
.nota{color:var(--ink2);font-size:13px}
.aviso{font-size:13px;color:var(--meio)}
.linha-da-iteracao,.linha-de-campos{display:flex;flex-wrap:wrap;align-items:flex-end;gap:10px 16px;margin:8px 0}
#mudancas table,.tabela table{border-collapse:collapse;width:100%;font-size:13px}
th,td{border-bottom:1px solid var(--linha);padding:5px 8px;text-align:left;vertical-align:top;overflow-wrap:break-word}
th{background:var(--acento2);font-weight:600;overflow-wrap:normal}
td code{overflow-wrap:anywhere}
.tabela{overflow-x:auto;margin:8px 0;border:1px solid var(--linha);border-radius:8px;background:var(--bg2)}
.abas,.abas-menores,.filtros-de-tipo{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
.abas button{font-weight:600;padding:7px 14px}.abas button.ativa,.abas-menores button.ativa,.filtros-de-tipo button.ativa{background:var(--acento);color:var(--bg2);border-color:var(--acento)}
.abas-menores button,.filtros-de-tipo button{font-size:12px;padding:3px 9px;border-radius:999px}
.duas-colunas{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:18px;align-items:start}
.cartao{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:14px 16px;box-shadow:var(--sombra);margin:0 0 14px}
#evidencia{position:sticky;top:0;max-height:calc(100vh - 150px);overflow:auto}
.grupo-de-blocos{font:600 12px var(--fb);letter-spacing:.04em;text-transform:uppercase;color:var(--ink2);margin:18px 0 6px}
.bloco{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:12px 16px;margin:0 0 10px}
.bloco h3{margin-top:0}.bloco .conteudo p{margin:6px 0}.bloco .conteudo ul,.bloco .conteudo ol{margin:6px 0;padding-left:22px}
.valor-do-analista{font-size:13px;color:var(--acento);font-weight:600;margin:6px 0 0}
mark.trecho-comentado{background:var(--marca);color:inherit;border-radius:3px;padding:0 1px}
mark.trecho-rascunho{background:none;color:inherit;border-bottom:2px dashed var(--meio)}
.conversa{border:1px solid var(--linha);border-left:3px solid var(--acento);border-radius:8px;padding:8px 12px;margin:10px 0;background:var(--bg)}
.conversa[data-estado=resolvida]{border-left-color:var(--bom)}.conversa[data-estado=nao_sera_tratada]{border-left-color:var(--ink2)}
.cab-conversa{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:12px;color:var(--ink2)}
.cab-conversa q{font-style:italic}
.comentario{margin:8px 0;padding-top:6px;border-top:1px dashed var(--linha)}.comentario:first-of-type{border-top:0}
.comentario .autor{font-weight:600}.comentario .quando{font-size:12px;color:var(--ink2);margin:0 6px}
.comentario .texto{margin:4px 0;white-space:pre-wrap;overflow-wrap:anywhere}
.acoes-da-conversa{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.rascunho{border:1px dashed var(--meio);border-radius:8px;padding:8px 12px;margin:8px 0}
.rascunho .texto{white-space:pre-wrap;margin:4px 0}
#comentar-trecho{position:fixed;z-index:20;background:var(--acento);color:var(--bg2);border-color:var(--acento);font-weight:600;box-shadow:var(--sombra)}
#form-comentario{margin:10px 0}
#comentario-do-agente .autor{font-weight:600}
.decisao,.texto-do-modelo{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:12px 16px;margin:0 0 12px}
.decisao h3,.texto-do-modelo h3{margin-top:0}
.afirmacoes{list-style:none;padding:0;margin:8px 0}.afirmacoes li{margin:6px 0;padding-left:0}
.origem-observado{color:var(--bom);border-color:var(--bom)}.origem-conferido{color:var(--acento);border-color:var(--acento)}
.origem-declarado{color:var(--meio);border-color:var(--meio)}.origem-desconhecido{color:var(--ink2);border-style:dashed}
.selo-modelo{color:var(--meio);border-color:var(--meio)}
#aba-trilha table{border-collapse:collapse;width:100%;font-size:13px;background:var(--bg2);border:1px solid var(--linha)}
tr.evento{cursor:pointer}tr.evento:hover{background:var(--acento2)}
tr.evento td:first-child{font-family:var(--fm)}
.tipo-decisao{color:var(--acento);border-color:var(--acento)}.tipo-verificacao{color:var(--bom);border-color:var(--bom)}.tipo-declaracao{color:var(--meio);border-color:var(--meio)}
details{border:1px solid var(--linha);border-radius:8px;padding:6px 10px;margin:8px 0;background:var(--bg2)}summary{cursor:pointer;font-weight:600}
@media (max-width:1100px){.corpo{grid-template-columns:240px minmax(0,1fr)}.duas-colunas{grid-template-columns:minmax(0,1fr)}#evidencia{position:static;max-height:none}}
@media (max-width:720px){body{height:auto}.corpo{display:block}.lateral{max-height:40vh}main{overflow:visible}}
@media (prefers-reduced-motion:no-preference){.item-caso,button{transition:background-color .12s,border-color .12s,color .12s}}
"""


# ! Alteração de IA - Revisar: (25/11/2026, pacote Q6, etapa 2) o programa da página do hub, servido em `/hub.js`, sem biblioteca de fora: busca
# a lista e o caso no servidor, desenha o relatório em blocos com as conversas presas aos trechos, a evidência, a árvore e a trilha, e manda
# ao servidor cada ação do analista (comentar, responder, mudar o estado de uma conversa, marcar como lido, gravar os campos da 5.5 e enviar a
# revisão com os rascunhos, a causa corrigida e o veredito). O rascunho e o nome de quem revisa ficam no armazenamento do navegador; o caso e
# a aba abertos ficam no endereço, para recarregar voltar ao mesmo lugar.
# ! Motivo: plano, seção 3.6 (itens 1 a 6), e ficha 97. O trecho comentado é guardado pela posição dele no texto do bloco e pelo próprio
# trecho: se a posição não bate mais (o relatório de outra iteração tem outro texto), a página procura o trecho e, se não acha, avisa na
# conversa em vez de marcar o lugar errado. O rascunho só vai ao servidor junto com o veredito, como a revisão pendente do GitHub
# (levantamento §6.15.1). Todo texto digitado ou vindo da evidência entra por `textContent`; só o HTML que o servidor já escapou entra como marcação.
JS = r"""'use strict';
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const E = {indice: null, caso: null, aba: 'relatorio', evidencia: null, ancora: null, selecao: null};
const ABAS = ['relatorio', 'arvore', 'trilha'];

function el(tag, props = {}, ...filhos) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (v === null || v === undefined || v === false) continue;
    if (k === 'class') e.className = v;
    else if (k === 'text') e.textContent = v;
    else if (k === 'data') Object.assign(e.dataset, v);
    else if (k === 'hidden') e.hidden = true;
    else e.setAttribute(k, v === true ? '' : v);
  }
  for (const f of filhos.flat()) if (f !== null && f !== undefined && f !== false) e.append(f);
  return e;
}

function comCodigo(texto) {
  return String(texto || '').split('`').map((parte, i) => (i % 2 ? el('code', {text: parte}) : parte));
}

function mostrarErro(msg) { $('#erro').textContent = msg || ''; }
function revisor() { return $('#nome-do-revisor').value.trim(); }
function quando(ts) { return ts ? ts.replace('T', ' ').slice(0, 16) : ''; }
function rotuloDe(lista, chave) { const par = (lista || []).find(p => p[0] === chave); return par ? par[1] : chave; }

async function api(caminho, corpo) {
  const opcoes = corpo === undefined ? {} : {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(corpo)};
  let r;
  try { r = await fetch(caminho, opcoes); } catch (e) { throw new Error('O hub não respondeu. Ele continua aberto no terminal?'); }
  let dado = null;
  try { dado = await r.json(); } catch (e) { dado = null; }
  if (!r.ok) throw new Error((dado && dado.erro) || ('O hub recusou o pedido (' + r.status + ').'));
  return dado;
}

async function gravar(acao, extras) {
  if (!revisor()) {
    mostrarErro('Diga quem está revisando (o campo do nome, no alto da página) antes de gravar.');
    $('#nome-do-revisor').focus();
    return null;
  }
  try {
    const r = await api('/api/revisao', {tid: E.caso.tid, acao, autor: {nome: revisor()}, ...extras});
    E.caso.revisao = r.revisao;
    E.caso.revisao_desta_iteracao = r.revisao_desta_iteracao;
    atualizarItens(E.caso.caso, r.resumo);
    mostrarErro('');
    return r;
  } catch (e) { mostrarErro(e.message); return null; }
}

// ---------------------------------------------------------------- a lista de casos

function etiquetas(c) {
  const r = c.revisao || {};
  const itens = [el('span', {class: 'etiqueta conf-' + (c.selo || 'sem'), text: 'confiança ' + c.confianca})];
  if (c.divergencia) itens.push(el('span', {class: 'etiqueta alerta', text: 'divergência'}));
  if (c.cura) itens.push(el('span', {class: 'etiqueta', text: 'cura'}));
  if (r.veredito) itens.push(el('span', {class: 'etiqueta veredito', text: r.veredito_rotulo}));
  if (r.ativas) itens.push(el('span', {class: 'etiqueta conversa-ativa', text: r.ativas === 1 ? '1 conversa ativa' : r.ativas + ' conversas ativas'}));
  return itens;
}

function itemDaLista(c) {
  const li = el('li', {class: 'item-caso', data: {tid: c.tid, caso: c.caso, corrida: c.corrida}, tabindex: '0', role: 'button'},
    el('span', {class: 'titulo-do-item'}, comCodigo(c.titulo)),
    el('span', {class: 'meta', text: c.rotulo_da_corrida + ' · ' + c.nome + ' · iteração ' + c.iteracao + ' de ' + c.iteracoes}),
    el('span', {class: 'etiquetas'}, etiquetas(c)));
  li.addEventListener('click', () => abrirCaso(c.tid));
  li.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); abrirCaso(c.tid); } });
  return li;
}

function desenharLista() {
  const ul = $('#lista-de-casos');
  ul.replaceChildren(...E.indice.casos.map(itemDaLista));
  filtrar();
}

function filtrar() {
  const corrida = $('#filtro-corrida').value, texto = $('#filtro-texto').value.trim().toLowerCase(), semVeredito = $('#filtro-sem-veredito').checked;
  let visiveis = 0;
  for (const c of E.indice.casos) {
    const li = $('#lista-de-casos').querySelector('.item-caso[data-tid="' + CSS.escape(c.tid) + '"]');
    const alvo = [c.tid, c.titulo, c.escolha, c.causa_em_palavras, c.campo].join(' ').toLowerCase();
    const mostra = (!corrida || c.corrida === corrida) && (!texto || alvo.includes(texto)) && (!semVeredito || !(c.revisao && c.revisao.veredito));
    li.hidden = !mostra;
    if (mostra) visiveis += 1;
  }
  $('#contagem-de-casos').textContent = visiveis + ' de ' + E.indice.casos.length + ' casos';
}

function atualizarItens(caso, resumo) {
  for (const c of E.indice.casos) {
    if (c.caso !== caso) continue;
    c.revisao = resumo;
    const li = $('#lista-de-casos').querySelector('.item-caso[data-tid="' + CSS.escape(c.tid) + '"]');
    if (li) $('.etiquetas', li).replaceChildren(...etiquetas(c));
  }
  filtrar();
}

// ---------------------------------------------------------------- o caso

function lerEndereco() {
  const p = new URLSearchParams(location.hash.slice(1));
  return {tid: p.get('caso'), aba: ABAS.includes(p.get('aba')) ? p.get('aba') : 'relatorio'};
}

function gravarEndereco() {
  const p = new URLSearchParams();
  if (E.caso) p.set('caso', E.caso.tid);
  p.set('aba', E.aba);
  history.replaceState(null, '', '#' + p.toString());
}

async function abrirCaso(tid, aba) {
  let caso;
  try { caso = await api('/api/caso?tid=' + encodeURIComponent(tid)); } catch (e) { mostrarErro(e.message); return; }
  mostrarErro('');
  fecharFormulario();
  E.caso = caso;
  if (aba) E.aba = aba;
  if (!E.evidencia || !caso.evidencia.some(x => x.id === E.evidencia)) E.evidencia = caso.evidencia.length ? caso.evidencia[0].id : null;
  desenharCaso();
}

function desenharCaso() {
  const c = E.caso, main = $('#caso');
  $('#vazio').hidden = true;
  main.hidden = false;
  $('#titulo-do-caso').replaceChildren(...comCodigo(c.titulo));
  $('#meta-do-caso').textContent = c.corrida.rotulo + (c.corrida.descricao ? ' (' + c.corrida.descricao + ')' : '') + ' · ' + c.nome + ' · iteração ' + c.iteracao + ' de '
    + c.iteracoes.length + ' · modelo ' + c.corrida.modelo;
  $('#seletor-de-iteracao').replaceChildren(...c.iteracoes.map(i => el('option', {value: i.tid, text: 'iteração ' + i.numero + ' · ' + i.rotulo_da_corrida + ' · ' + i.nome + ' · ' + quando(i.ts),
    selected: i.tid === c.tid})));
  $('#seletor-de-iteracao').value = c.tid;
  $('#aviso-de-iteracao').textContent = c.iteracao < c.iteracoes.length ? 'Há iteração mais nova: a ' + c.iteracoes.length + ' é a última.' : '';
  desenharMudancas();
  const ag = c.comentario_do_agente;
  $('#comentario-do-agente').replaceChildren(
    el('p', {class: 'meta'}, el('span', {class: 'autor', text: ag.autor.nome}), ' · ' + quando(ag.ts) + ' · o agente só comenta: o veredito é do analista'),
    el('p', {}, comCodigo(ag.texto)));
  $('#preambulo').innerHTML = c.relatorio.preambulo_html;
  $('#rastro').innerHTML = c.relatorio.rastro_html;
  desenharEvidencia();
  $('#aba-arvore').innerHTML = c.arvore_html;
  desenharTrilha();
  desenharRevisao();
  mostrarAba(ABAS.includes(E.aba) ? E.aba : 'relatorio');
  for (const li of $$('#lista-de-casos .item-caso')) li.classList.toggle('aberto', li.dataset.tid === c.tid);
  main.scrollTop = 0;
  main.dataset.tid = c.tid;
}

function desenharMudancas() {
  const m = E.caso.mudancas, raiz = $('#mudancas');
  raiz.replaceChildren();
  if (!m || m.de === null) return;
  const titulo = 'O que mudou desde a iteração ' + m.de + ' (' + m.motivo + ')';
  if (!m.itens.length) { raiz.append(el('p', {class: 'nota', text: titulo + ': nada, nos campos que o hub compara.'})); return; }
  raiz.append(el('h3', {text: titulo}), el('div', {class: 'tabela'}, el('table', {},
    el('thead', {}, el('tr', {}, el('th', {text: 'O quê'}), el('th', {text: 'Antes'}), el('th', {text: 'Agora'}))),
    el('tbody', {}, m.itens.map(i => el('tr', {}, el('td', {text: i.campo}), el('td', {text: i.antes}), el('td', {text: i.depois})))))));
}

function mostrarAba(nome) {
  E.aba = nome;
  for (const s of $$('#caso > section.aba')) s.hidden = s.id !== 'aba-' + nome;
  for (const b of $$('nav.abas button')) b.classList.toggle('ativa', b.dataset.aba === nome);
  $('#comentar-trecho').hidden = true;
  gravarEndereco();
}

// ---------------------------------------------------------------- a evidência

function desenharEvidencia() {
  const c = E.caso;
  $('#evidencia-abas').replaceChildren(...c.evidencia.map(x => {
    const b = el('button', {type: 'button', data: {evidencia: x.id}, class: x.id === E.evidencia ? 'ativa' : '', text: x.titulo});
    b.addEventListener('click', () => { E.evidencia = x.id; desenharEvidencia(); });
    return b;
  }));
  const x = c.evidencia.find(y => y.id === E.evidencia), alvo = $('#evidencia-conteudo');
  alvo.replaceChildren();
  if (!x) { alvo.append(el('p', {class: 'nota', text: 'Este caso não guardou evidência para mostrar.'})); return; }
  alvo.append(el('p', {class: 'nota'}, x.rotulo ? el('span', {class: 'selo-modelo', text: x.rotulo}) : null, (x.rotulo ? ' ' : '') + (x.nota || '')));
  if (x.tipo === 'verbetes') {
    for (const v of x.itens) {
      const d = el('details', {}, el('summary', {}, v.titulo + ' ', el('code', {text: v.id}), v.curado ? ' · leitura revisada à mão' : ''));
      if (v.arquivo) d.append(el('p', {class: 'meta', text: v.arquivo}));
      for (const s of v.secoes) { const corpo = el('div', {}); corpo.innerHTML = s.html; d.append(el('h4', {text: s.titulo}), corpo); }
      alvo.append(d);
    }
    return;
  }
  alvo.append(el('pre', {text: x.texto}));
  if (x.texto_podado) alvo.append(el('p', {class: 'nota', text: 'Depois da poda (o que o modelo leu):'}), el('pre', {text: x.texto_podado}));
}

// ---------------------------------------------------------------- a trilha

function detalheDoEvento(e) {
  const partes = [el('pre', {text: JSON.stringify(e.dados, null, 2)})];
  if (e.pai !== null && e.pai !== undefined) partes.unshift(el('p', {class: 'meta', text: 'Veio do evento ' + e.pai + ' · camada ' + (e.camada || 'não registrada')}));
  for (const [chave, valor] of Object.entries(e.dados || {})) {
    if (typeof valor === 'string' && Object.prototype.hasOwnProperty.call(E.caso.blobs, valor)) {
      partes.push(el('details', {}, el('summary', {text: chave + ': o texto guardado (' + valor + ')'}), el('pre', {text: E.caso.blobs[valor]})));
    }
  }
  return partes;
}

function desenharTrilha() {
  const raiz = $('#aba-trilha'), eventos = E.caso.trilha, tipos = {};
  for (const e of eventos) tipos[e.tipo] = (tipos[e.tipo] || 0) + 1;
  const filtros = el('div', {class: 'filtros-de-tipo'},
    el('button', {type: 'button', class: 'ativa', data: {tipo: ''}, text: 'todos (' + eventos.length + ')'}),
    Object.entries(tipos).map(([t, n]) => el('button', {type: 'button', data: {tipo: t}, text: t + ' (' + n + ')'})));
  const corpo = el('tbody');
  for (const e of eventos) {
    const det = el('tr', {class: 'detalhe-do-evento', hidden: true, data: {tipo: e.tipo}}, el('td', {colspan: '5'}, detalheDoEvento(e)));
    const linha = el('tr', {class: 'evento', tabindex: '0', data: {seq: e.seq, tipo: e.tipo}},
      el('td', {text: e.seq}), el('td', {}, el('span', {class: 'tipo tipo-' + e.tipo, text: e.tipo})), el('td', {text: quando(e.ts).slice(11)}),
      el('td', {text: e.origem || ''}), el('td', {text: e.resumo}));
    const alternar = () => { det.hidden = !det.hidden; };
    linha.addEventListener('click', alternar);
    linha.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); alternar(); } });
    corpo.append(linha, det);
  }
  filtros.addEventListener('click', ev => {
    const b = ev.target.closest('button');
    if (!b) return;
    for (const x of $$('button', filtros)) x.classList.toggle('ativa', x === b);
    for (const tr of $$('tr', corpo)) {
      const fora = Boolean(b.dataset.tipo) && tr.dataset.tipo !== b.dataset.tipo;
      if (tr.classList.contains('evento')) tr.hidden = fora; else if (fora) tr.hidden = true;
    }
  });
  raiz.replaceChildren(
    el('p', {class: 'nota', text: 'Os eventos deste caso na trilha, na ordem em que o agente os gravou. Clique numa linha para ver o registro inteiro.'}),
    filtros,
    el('table', {}, el('thead', {}, el('tr', {}, ['nº', 'tipo', 'hora', 'origem', 'o que aconteceu'].map(t => el('th', {text: t})))), corpo));
}

// ---------------------------------------------------------------- os blocos e as conversas

function localizar(raiz, ancora) {
  const texto = raiz.textContent;
  if (texto.slice(ancora.inicio, ancora.fim) === ancora.trecho) return [ancora.inicio, ancora.fim];
  const i = texto.indexOf(ancora.trecho);
  return i < 0 ? null : [i, i + ancora.trecho.length];
}

function marcar(raiz, inicio, fim, classe, conversa) {
  const andador = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT), alvos = [];
  let pos = 0, no;
  while ((no = andador.nextNode())) {
    const a = pos, b = pos + no.data.length;
    if (b > inicio && a < fim) alvos.push([no, Math.max(inicio - a, 0), Math.min(fim - a, no.data.length)]);
    pos = b;
  }
  for (const [n, i, f] of alvos) {
    const r = document.createRange();
    r.setStart(n, i);
    r.setEnd(n, f);
    const m = el('mark', {class: classe, data: conversa ? {conversa} : {}});
    r.surroundContents(m);
  }
}

function cartaoDaConversa(cv, achou) {
  const opcoes = E.indice.opcoes;
  const cab = el('div', {class: 'cab-conversa'}, el('span', {class: 'estado-da-conversa', text: rotuloDe(opcoes.estados_da_conversa, cv.estado)}));
  if (cv.ancora) cab.append(el('q', {text: cv.ancora.trecho}));
  if (cv.de_iteracao_anterior) cab.append(el('span', {class: 'aviso', text: 'aberta na iteração ' + cv.iteracao.numero}));
  if (cv.ancora && !achou) cab.append(el('span', {class: 'aviso', text: 'o trecho comentado não está no texto desta iteração'}));
  const card = el('div', {class: 'conversa', data: {conversa: cv.id, estado: cv.estado}}, cab);
  for (const cm of cv.comentarios) {
    card.append(el('div', {class: 'comentario'},
      el('span', {class: 'autor', text: cm.autor.nome}), el('span', {class: 'quando', text: quando(cm.ts)}),
      cm.rotulo ? el('span', {class: 'rotulo', text: rotuloDe(opcoes.rotulos, cm.rotulo)}) : null,
      cm.bloqueante ? el('span', {class: 'bloqueante', text: 'bloqueante'}) : null,
      el('p', {class: 'texto', text: cm.texto})));
  }
  const resposta = el('textarea', {class: 'resposta', rows: '2', maxlength: '4000', 'aria-label': 'Responder a esta conversa', placeholder: 'Responder'});
  const botao = (classe, rotulo, estado) => {
    const b = el('button', {type: 'button', class: classe, text: rotulo});
    b.addEventListener('click', async () => { if (await gravar('estado_da_conversa', {conversa: cv.id, estado})) desenharRevisao(); });
    return b;
  };
  const responder = el('button', {type: 'button', class: 'responder', text: 'Responder'});
  responder.addEventListener('click', async () => {
    if (!resposta.value.trim()) { mostrarErro('Escreva a resposta antes de enviar.'); return; }
    if (await gravar('comentar', {texto: resposta.value, conversa: cv.id, ancora: null})) desenharRevisao();
  });
  card.append(resposta, el('div', {class: 'acoes-da-conversa'}, responder,
    cv.estado === 'ativa' ? [botao('resolver', 'Resolver', 'resolvida'), botao('nao-tratar', 'Não será tratada', 'nao_sera_tratada')] : botao('reabrir', 'Reabrir', 'ativa')));
  return card;
}

function desenharBlocos() {
  const c = E.caso, raiz = $('#blocos'), campos = c.revisao.campos_55;
  const doAnalista = {8: ['Severidade', campos.severidade], 9: ['Prioridade', campos.prioridade], 10: ['Estado', campos.estado]};
  raiz.replaceChildren();
  let grupo = null;
  for (const b of c.relatorio.blocos) {
    if (b.grupo !== grupo) {
      grupo = b.grupo;
      raiz.append(el('p', {class: 'grupo-de-blocos', text: grupo === '5.5' ? 'Relatório de defeito (seção 5.5 do syllabus)' : 'O que o agente fez, declarou e conferiu'}));
    }
    const conteudo = el('div', {class: 'conteudo'});
    conteudo.innerHTML = b.html;
    const sec = el('section', {class: 'bloco', data: {bloco: b.id, grupo: b.grupo}}, el('h3', {text: b.numero + '. ' + b.titulo}), conteudo);
    if (doAnalista[b.numero] && c.relatorio.blocos.length > 11) {
      sec.append(el('p', {class: 'valor-do-analista', text: doAnalista[b.numero][0] + ' dada pelo analista: ' + (doAnalista[b.numero][1] || 'ainda em branco')}));
    }
    sec.append(el('div', {class: 'conversas-do-bloco'}));
    raiz.append(sec);
  }
  $('#conversas-gerais').replaceChildren();
  for (const cv of c.revisao.conversas) {
    const sec = cv.ancora ? raiz.querySelector('section.bloco[data-bloco="' + CSS.escape(cv.ancora.bloco) + '"]') : null;
    if (!sec) { $('#conversas-gerais').append(cartaoDaConversa(cv, true)); continue; }
    const lugar = localizar($('.conteudo', sec), cv.ancora);
    if (lugar) marcar($('.conteudo', sec), lugar[0], lugar[1], 'trecho-comentado', cv.id);
    $('.conversas-do-bloco', sec).append(cartaoDaConversa(cv, Boolean(lugar)));
  }
  for (const r of rascunhos()) {
    if (!r.ancora) continue;
    const sec = raiz.querySelector('section.bloco[data-bloco="' + CSS.escape(r.ancora.bloco) + '"]');
    const lugar = sec ? localizar($('.conteudo', sec), r.ancora) : null;
    if (lugar) marcar($('.conteudo', sec), lugar[0], lugar[1], 'trecho-rascunho', null);
  }
  if (!c.revisao.conversas.some(cv => !cv.ancora)) $('#conversas-gerais').append(el('p', {class: 'nota', text: 'Nenhum comentário geral.'}));
}

// ---------------------------------------------------------------- a revisão

function chaveDosRascunhos() { return 'hub.rascunhos.' + E.caso.tid; }
function rascunhos() { try { return JSON.parse(localStorage.getItem(chaveDosRascunhos()) || '[]'); } catch (e) { return []; } }
function guardarRascunhos(lista) { if (lista.length) localStorage.setItem(chaveDosRascunhos(), JSON.stringify(lista)); else localStorage.removeItem(chaveDosRascunhos()); }

function desenharRascunhos() {
  const lista = rascunhos(), raiz = $('#rascunhos');
  raiz.replaceChildren();
  lista.forEach((r, i) => {
    const descartar = el('button', {type: 'button', class: 'descartar', text: 'Descartar'});
    descartar.addEventListener('click', () => { const l = rascunhos(); l.splice(i, 1); guardarRascunhos(l); desenharRevisao(); });
    raiz.append(el('div', {class: 'rascunho'},
      el('p', {class: 'meta', text: r.ancora ? 'preso ao trecho "' + r.ancora.trecho + '"' : 'comentário geral'}),
      el('p', {class: 'texto', text: r.texto}), descartar));
  });
  if (!lista.length) raiz.append(el('p', {class: 'nota', text: 'Nenhum rascunho. O rascunho só é gravado quando a revisão é enviada.'}));
  $('#contagem-de-rascunhos').textContent = lista.length ? '(' + lista.length + ')' : '';
  $('#enviar-revisao').textContent = lista.length ? 'Enviar revisão (' + lista.length + ')' : 'Enviar revisão';
}

function desenharLido() {
  const c = E.caso, d = c.revisao_desta_iteracao, lido = c.revisao.lido;
  $('#marca-lido').checked = d.lida;
  let aviso = '';
  if (d.lida) aviso = 'Iteração ' + c.iteracao + ' marcada como lida em ' + quando(lido.ts) + '.';
  else if (lido && lido.numero < c.iteracao) aviso = 'A sua marca de lido é da iteração ' + lido.numero + ': esta é uma iteração nova para você.';
  else if (lido) aviso = 'Você já leu uma iteração mais nova (a ' + lido.numero + ').';
  $('#aviso-lido').textContent = aviso;
}

function desenharRevisao() {
  const c = E.caso, rev = c.revisao, opcoes = E.indice.opcoes;
  fecharFormulario();
  desenharBlocos();
  const v = rev.veredito_atual;
  $('#veredito-atual').textContent = v
    ? 'Veredito: ' + rotuloDe(opcoes.vereditos, v.veredito) + ' · por ' + v.autor.nome + ' em ' + quando(v.ts) + ', na iteração ' + v.iteracao.numero
      + (v.desfecho ? ' · ' + rotuloDe(opcoes.desfechos, v.desfecho) : '') + (v.resumo ? ' · ' + v.resumo : '')
      + (rev.veredito_vale_para_a_iteracao_atual ? '' : ' · dado numa iteração anterior: a última ainda espera veredito')
    : 'Sem veredito do analista.';
  const s = rev.causa_sugerida;
  $('#causa-atual').textContent = s ? 'A causa é outra, segundo ' + s.autor.nome + ' (' + quando(s.ts) + ', iteração ' + s.iteracao.numero + '): ' + s.causa
    + (s.campo ? ', campo ' + s.campo : '') + (s.texto ? ' · ' + s.texto : '') : '';
  $('#severidade').value = rev.campos_55.severidade || '';
  $('#prioridade').value = rev.campos_55.prioridade || '';
  $('#estado-55').value = rev.campos_55.estado;
  $('#aviso-55').textContent = '';
  desenharRascunhos();
  desenharLido();
}

function lerCampos55() { return {severidade: $('#severidade').value || null, prioridade: $('#prioridade').value || null, estado: $('#estado-55').value}; }

async function enviarRevisao() {
  const rev = E.caso.revisao, campos = lerCampos55(), causa = $('#causa-sugerida').value;
  if (!$('#veredito').value) { mostrarErro('Escolha o veredito antes de enviar a revisão.'); $('#veredito').focus(); return; }
  const mudou = ['severidade', 'prioridade', 'estado'].some(k => campos[k] !== rev.campos_55[k]);
  const r = await gravar('enviar_revisao', {
    veredito: $('#veredito').value, resumo: $('#resumo-da-revisao').value, desfecho: $('#desfecho').value || null,
    rascunhos: rascunhos().map(x => ({texto: x.texto, ancora: x.ancora, rotulo: x.rotulo, bloqueante: x.bloqueante})),
    campos_55: mudou ? campos : null,
    causa_sugerida: causa ? {causa, campo: $('#campo-sugerido').value.trim() || null, texto: ''} : null});
  if (!r) return;
  guardarRascunhos([]);
  for (const id of ['#veredito', '#desfecho', '#causa-sugerida', '#campo-sugerido', '#resumo-da-revisao']) $(id).value = '';
  desenharRevisao();
}

// ---------------------------------------------------------------- o formulário de comentário

function fecharFormulario() {
  const f = $('#form-comentario');
  f.hidden = true;
  document.body.append(f);
  $('#texto-do-comentario').value = '';
  $('#rotulo-do-comentario').value = '';
  $('#bloqueante').checked = false;
  E.ancora = null;
}

function abrirFormulario(ancora) {
  const f = $('#form-comentario'), citado = $('.trecho-citado', f);
  E.ancora = ancora;
  citado.hidden = !ancora;
  citado.textContent = ancora ? ancora.trecho : '';
  const sec = ancora ? $('#blocos').querySelector('section.bloco[data-bloco="' + CSS.escape(ancora.bloco) + '"]') : null;
  if (sec) $('.conversas-do-bloco', sec).append(f); else $('#conversas-gerais').after(f);
  f.hidden = false;
  $('#comentar-trecho').hidden = true;
  $('#texto-do-comentario').focus();
}

function lerFormulario() {
  const texto = $('#texto-do-comentario').value;
  if (!texto.trim()) { mostrarErro('Escreva o comentário antes de gravar.'); return null; }
  return {texto, ancora: E.ancora, rotulo: $('#rotulo-do-comentario').value || null, bloqueante: $('#bloqueante').checked};
}

function aoSelecionar() {
  const s = getSelection(), botao = $('#comentar-trecho');
  botao.hidden = true;
  E.selecao = null;
  if (!s || s.isCollapsed || !s.rangeCount) return;
  const r = s.getRangeAt(0);
  const pai = r.commonAncestorContainer.nodeType === 1 ? r.commonAncestorContainer : r.commonAncestorContainer.parentElement;
  const conteudo = pai ? pai.closest('section.bloco .conteudo') : null;
  if (!conteudo) return;
  const bruto = r.toString(), trecho = bruto.trim();
  if (!trecho) return;
  const antes = document.createRange();
  antes.selectNodeContents(conteudo);
  antes.setEnd(r.startContainer, r.startOffset);
  const inicio = antes.toString().length + (bruto.length - bruto.trimStart().length);
  E.selecao = {bloco: conteudo.closest('section.bloco').dataset.bloco, trecho, inicio, fim: inicio + trecho.length};
  const caixa = r.getBoundingClientRect();
  botao.style.top = Math.min(caixa.bottom + 6, innerHeight - 40) + 'px';
  botao.style.left = Math.max(8, Math.min(caixa.left, innerWidth - 190)) + 'px';
  botao.hidden = false;
}

// ---------------------------------------------------------------- a partida

function preencher(seletor, itens) {
  for (const item of itens) {
    const [valor, rotulo] = Array.isArray(item) ? item : [item, item];
    $(seletor).append(el('option', {value: valor, text: rotulo}));
  }
}

async function iniciar() {
  $('#nome-do-revisor').value = localStorage.getItem('hub.revisor') || '';
  $('#nome-do-revisor').addEventListener('input', ev => localStorage.setItem('hub.revisor', ev.target.value));
  try { E.indice = await api('/api/indice'); } catch (e) { mostrarErro(e.message); return; }
  const o = E.indice.opcoes;
  preencher('#filtro-corrida', E.indice.corridas.map(c => [c.pasta, c.rotulo + ' (' + c.casos + ')']));
  preencher('#severidade', o.severidades);
  preencher('#prioridade', o.prioridades);
  preencher('#estado-55', o.estados_55);
  preencher('#causa-sugerida', o.causas);
  $('#veredito').append(el('option', {value: '', text: 'escolha o veredito'}));
  preencher('#veredito', o.vereditos);
  preencher('#desfecho', o.desfechos);
  preencher('#rotulo-do-comentario', o.rotulos);
  desenharLista();
  for (const id of ['#filtro-corrida', '#filtro-texto', '#filtro-sem-veredito']) $(id).addEventListener('input', filtrar);
  for (const b of $$('nav.abas button')) b.addEventListener('click', () => mostrarAba(b.dataset.aba));
  $('#seletor-de-iteracao').addEventListener('change', ev => abrirCaso(ev.target.value));
  $('#marca-lido').addEventListener('change', async ev => { if (ev.target.checked) await gravar('lido', {}); desenharLido(); });
  $('#comentar-geral').addEventListener('click', () => abrirFormulario(null));
  $('#comentar-trecho').addEventListener('mousedown', ev => ev.preventDefault());
  $('#comentar-trecho').addEventListener('click', () => { if (E.selecao) abrirFormulario(E.selecao); });
  $('#cancelar-comentario').addEventListener('click', fecharFormulario);
  $('#comentar-agora').addEventListener('click', async () => {
    const c = lerFormulario();
    if (c && await gravar('comentar', {...c, conversa: null})) desenharRevisao();
  });
  $('#guardar-rascunho').addEventListener('click', () => {
    const c = lerFormulario();
    if (!c) return;
    guardarRascunhos([...rascunhos(), c]);
    mostrarErro('');
    desenharRevisao();
  });
  $('#gravar-55').addEventListener('click', async () => {
    if (await gravar('campos_55', lerCampos55())) { desenharRevisao(); $('#aviso-55').textContent = 'Campos gravados.'; }
  });
  $('#enviar-revisao').addEventListener('click', enviarRevisao);
  document.addEventListener('mouseup', ev => { if (!(ev.target.closest && ev.target.closest('#comentar-trecho'))) setTimeout(aoSelecionar, 0); });
  document.addEventListener('keyup', ev => { if (ev.shiftKey || ev.key === 'Shift') setTimeout(aoSelecionar, 0); });
  $('#caso').addEventListener('scroll', () => { if (!$('#comentar-trecho').hidden) aoSelecionar(); });
  const {tid, aba} = lerEndereco();
  if (tid) await abrirCaso(tid, aba);
}

iniciar();
"""
