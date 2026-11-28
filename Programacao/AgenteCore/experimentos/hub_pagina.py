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
    s = s.removeprefix("|")
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
        "<title>Hub central do agente de QA</title>", '<link rel="stylesheet" href="/hub.css">', "</head>", "<body>",
        '<header class="topo">',
        '<div class="marca"><strong>Hub central</strong><span>o agente comenta; o veredito é do analista</span></div>',
        '<nav class="vistas" aria-label="Vistas do hub">',
        '<button type="button" id="abrir-inicio">Início</button>',
        '<button type="button" id="abrir-metricas">Métricas</button>',
        '<button type="button" id="abrir-ao-vivo">Corrida ao vivo</button>',
        "</nav>",
        ('<label class="campo" title="O seu nome entra em cada comentário e em cada veredito que você gravar">Quem está revisando '
         '<input id="nome-do-revisor" type="text" maxlength="80" autocomplete="off" placeholder="seu nome"></label>'),
        '<p id="erro" role="alert" aria-live="assertive"></p>',
        "</header>",
        '<div class="corpo">',
        '<aside class="lateral" aria-label="Casos">',
        '<div class="topo-da-lista">',
        f'<label class="campo" title="Mostra só os diagnósticos de uma corrida">Corrida <select id="filtro-corrida">{opcao_vazia("todas")}</select></label>',
        ('<label class="campo" title="Procura no nome do caso, na causa respondida, no campo e no título">Procurar '
         '<input id="filtro-texto" type="search" placeholder="caso, causa, título"></label>'),
        ('<label class="campo marcar" title="Esconde os diagnósticos que o analista já julgou"><input id="filtro-sem-veredito" type="checkbox"> só sem veredito</label>'),
        '<span id="contagem-de-casos" class="contagem" title="Quantos diagnósticos passam no filtro, do total que o hub tem"></span>',
        '<button type="button" id="abrir-legenda" aria-controls="legenda-da-lista" aria-expanded="false">O que é cada item?</button>',
        "</div>",
        '<div id="legenda-da-lista" class="legenda-da-lista" hidden><dl>',
        "<dt>Corrida</dt><dd>uma rodada do agente. Cada grupo da lista é uma corrida, e o número ao lado é quantos diagnósticos ela tem</dd>",
        "<dt>Cada linha</dt><dd>um diagnóstico do agente: o título diz a causa que ele respondeu e onde</dd>",
        "<dt>Iteração</dt><dd>o mesmo caso diagnosticado mais de uma vez. Iteração 2 de 3 é a segunda de três</dd>",
        "<dt>Confiança</dt><dd>alta, média ou baixa: o selo que o código dá à resposta do modelo, pela probabilidade lida</dd>",
        "<dt>Divergência</dt><dd>o que o modelo declarou não bate com o que o código conferiu</dd>",
        "<dt>Cura</dt><dd>o agente achou outro seletor para um localizador quebrado e refez o roteiro</dd>",
        "<dt>Veredito</dt><dd>a decisão do analista sobre o diagnóstico. O agente só comenta</dd>",
        "</dl></div>",
        '<ul id="lista-de-casos"></ul>',
        "</aside>",
        '<main id="caso" hidden>',
        '<div id="cabecalho-do-caso">',
        '<h1 id="titulo-do-caso"></h1>',
        '<p id="meta-do-caso" class="meta"></p>',
        '<div id="processo-do-caso" class="diagrama"></div>',
        '<div id="resumo-do-processo" class="fichas"></div>',
        '<div class="linha-da-iteracao">',
        '<label class="campo">Iteração <select id="seletor-de-iteracao"></select></label>',
        '<label class="campo marcar"><input id="marca-lido" type="checkbox"> li esta iteração</label>',
        '<span id="aviso-lido" class="aviso"></span>',
        '<span id="aviso-de-iteracao" class="aviso"></span>',
        "</div>",
        '<div id="mudancas"></div>',
        '<p id="trace-do-caso" class="nota"></p>',
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
        '<section id="ao-vivo" hidden>',
        "<h1>Corrida ao vivo</h1>",
        '<div class="cartao">',
        "<h2>Linha de produção</h2>",
        '<p id="caso-ao-vivo" class="nota" aria-live="polite"></p>',
        '<div id="linha-de-producao" class="diagrama"></div>',
        "</div>",
        # ! Alteração de IA - Revisar: (27/11/2026, coletânea da banca, decisões 194 a 196) o bloco da rodada da coletânea: o resumo da pilha, um cartão
        # por carta (escondido até a resposta), a grade das 64 cartas e, no fim, a lista e o comando que refaz o sorteio.
        # ! Motivo: é onde a banca compara o que foi ligado com o que o agente disse; fica logo abaixo da linha de produção, que mostra o caso rodando.
        '<div id="coletanea" class="cartao" hidden>',
        "<h2>Erros sorteados da coletânea</h2>",
        '<p id="coletanea-resumo" class="nota"></p>',
        '<div id="coletanea-cartas" class="cartas-da-rodada"></div>',
        "<h3>As 64 cartas da coletânea, por grupo</h3>",
        ('<p class="nota">Cada quadrado é uma carta. Azul: revelada nesta rodada (o cartão acima diz se o agente acertou). Cinza: tirada numa rodada anterior '
         'com o mesmo número. Apagado: ainda na pilha, ou escondida até o agente responder; os dois ficam iguais de propósito.</p>'),
        '<div id="coletanea-grade" class="grade-da-coletanea"></div>',
        '<div id="coletanea-fim"></div>',
        "</div>",
        '<div class="cartao">',
        "<h2>Barra de progresso</h2>",
        '<p id="estado-ao-vivo" class="nota"></p>',
        '<p id="etapa-ao-vivo"></p>',
        '<div id="barra" class="barra" role="progressbar" aria-label="Progresso da inferência em andamento" aria-valuemin="0" aria-valuemax="100"><div id="barra-cheia"></div></div>',
        '<p id="tempo-ao-vivo" class="nota"></p>',
        "</div>",
        '<div id="cerebro" class="cartao">',
        "<h2>Cérebro ao vivo: o último diagnóstico</h2>",
        '<div id="cerebro-conteudo"></div>',
        '<button type="button" id="abrir-ultimo" hidden>Abrir este caso</button>',
        "</div>",
        '<div id="execucao" class="cartao">',
        "<h2>Rodar os cenários</h2>",
        '<p id="estado-da-execucao"></p>',
        '<div class="linha-de-campos">',
        # ! Alteração de IA - Revisar: (27/11/2026, coletânea da banca, decisões 193 a 197) "O que rodar" ganha "erros sorteados da coletânea", com
        # os campos "Quantos casos" e "Número da banca" e a nota que explica a pilha; os dois campos só aparecem com a coletânea escolhida.
        # ! Motivo: a banca diz o número e vê de onde vêm os casos; todo campo novo vem com a explicação no lugar onde aparece.
        ('<label class="campo">O que rodar <select id="selecao-da-corrida"><option value="todos">os dez cenários</option>'
         '<option value="git">só os atingidos pelo que mudou no Git</option><option value="coletanea">erros sorteados da coletânea</option></select></label>'),
        '<label class="campo" id="campo-das-quantas" hidden>Quantos casos <select id="quantas-da-corrida"></select></label>',
        ('<label class="campo" id="campo-do-numero" hidden>Número da banca <input id="numero-da-corrida" type="text" inputmode="numeric" maxlength="18" '
         'autocomplete="off" placeholder="vazio: a hora do clique"></label>'),
        ('<label class="campo" id="campo-do-desde" hidden>Desde o commit <input id="desde-da-corrida" type="text" maxlength="40" autocomplete="off" '
         'placeholder="o último testado"></label>'),
        '<label class="campo" id="campo-das-repeticoes">Repetições de cada cenário <select id="repeticoes"></select></label>',
        '<button type="button" id="rodar-cenarios" class="principal" hidden>Ativar o agente e rodar os cenários</button>',
        '<button type="button" id="parar-corrida" hidden>Parar a corrida</button>',
        '<button type="button" id="copiar-comando" hidden>Copiar o comando</button>',
        "</div>",
        ('<p id="nota-da-coletanea" class="nota" hidden>Os erros sorteados saem de uma coletânea de 64 cartas: 58 erros já provados nas corridas '
         '(42 de contrato da API e 16 quebras de localizador do site) e 6 cartas sem erro nenhum. O número dito pela banca, só com algarismos, embaralha a '
         'pilha; cada rodada tira os próximos casos dela, e nenhum se repete até a pilha acabar. Sem número, vale a hora do clique. O sorteio é gravado '
         'antes de o primeiro erro ser ligado, e cada erro só aparece depois de o agente responder. Cada caso leva cerca de um minuto e meio. A rodada é '
         'uso do produto, não medida do TCC.</p>'),
        '<div id="previa-da-selecao"></div>',
        '<pre id="comando-da-corrida" hidden></pre>',
        '<pre id="log-da-execucao" hidden></pre>',
        "</div>",
        "</section>",
        '<section id="inicio" hidden>',
        "<h1>Central do agente de QA</h1>",
        '<p id="resumo-do-inicio" class="nota"></p>',
        '<div class="cartao">',
        "<h2>Como as peças se ligam, e o que está no ar</h2>",
        '<div id="workspaces" class="diagrama rolavel"></div>',
        '<div id="servicos" class="servicos"></div>',
        '<p id="nota-dos-servicos" class="nota"></p>',
        "</div>",
        '<div class="cartao">',
        "<h2>O que dá para fazer daqui</h2>",
        '<div class="atalhos">',
        ('<div class="atalho"><button type="button" id="ir-para-rodar" class="principal">Rodar os cenários</button>'
         '<p class="nota" id="nota-de-rodar"></p></div>'),
        ('<div class="atalho"><button type="button" id="ir-para-metricas">Ver as métricas</button>'
         '<p class="nota">O que cada corrida mediu, lido dos registros gravados, e o resultado da comparação com as pessoas.</p></div>'),
        ('<div class="atalho"><a class="painel" id="abrir-painel" href="/painel" target="_blank" rel="noopener">Abrir o painel do projeto</a>'
         # ! Alteração de IA - Revisar: (26/11/2026, ficha 116, decisão 178) a nota do atalho passou a dizer que o painel funciona sem internet, com os gráficos.
         # ! Motivo: ela dizia que, sem internet, os gráficos do painel não apareciam; a biblioteca que os desenha agora vai embutida no arquivo do painel
         # (`ferramentas/terceiros/chart.umd.js`, posta no HTML por `gerar_dashboard.py`), e a frase antiga deixou de ser verdade.
         '<p class="nota">A leitura de cada resultado, um assunto por aba. Abre o arquivo desta máquina, em outra aba, e funciona sem internet: a '
         'biblioteca que desenha os gráficos vai dentro do próprio arquivo.</p>'
         '<p class="aviso" id="aviso-do-painel" role="status" hidden></p></div>'),
        "</div>",
        '<p class="nota">Para revisar um diagnóstico do agente, escolha um caso na lista ao lado.</p>',
        "</div>",
        "</section>",
        '<section id="metricas" hidden>',
        "<h1>Métricas</h1>",
        '<div id="metricas-da-fase-5" class="cartao" hidden></div>',
        '<div class="cartao">',
        "<h2>Por corrida</h2>",
        "<h3>Tempo médio de reparo das corridas que rodam cenários</h3>",
        '<div id="grafico-do-reparo" class="diagrama"></div>',
        '<p id="nota-do-reparo" class="nota"></p>',
        "<h3>Confiança dos diagnósticos</h3>",
        '<div id="grafico-da-confianca" class="diagrama"></div>',
        ('<div class="legenda-do-diagrama"><span class="l-alta">confiança alta</span><span class="l-media">média</span><span class="l-baixa">baixa</span></div>'),
        '<details class="tabela-recolhida"><summary>Ver a tabela com os números</summary>',
        ('<p class="nota">Cada linha é lida agora dos arquivos da corrida: os casos e a confiança vêm da trilha; as execuções, o Task Success (em quantas o agente '
         'chegou ao resultado) e o tempo de reparo vêm do <code>cenarios.jsonl</code>. O tempo de reparo é a média dos cenários: primeiro a média das execuções de '
         'cada cenário, depois a média entre eles.</p>'),
        ('<div class="tabela"><table><thead><tr><th>Corrida</th><th>Casos com diagnóstico</th><th>Confiança</th><th>Execuções de cenário</th><th>Task Success</th>'
         '<th>Falha detectada</th><th>Tempo médio de reparo</th><th>Medida do TCC</th></tr></thead><tbody id="metricas-por-corrida"></tbody></table></div>'),
        "</details>",
        "</div>",
        '<div id="metricas-por-cenario" class="cartao" hidden></div>',
        "</section>",
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
        '<div id="zoom-da-etapa" class="zoom" role="dialog" aria-modal="true" aria-labelledby="titulo-do-zoom" hidden>',
        '<div class="zoom-caixa">',
        '<button type="button" id="fechar-zoom">Fechar</button>',
        '<h2 id="titulo-do-zoom"></h2>',
        '<p id="o-que-e-do-zoom" class="o-que-e"></p>',
        '<p id="resumo-do-zoom"></p>',
        '<div id="corpo-do-zoom"></div>',
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
main,#ao-vivo,#inicio,#metricas{overflow-y:auto;padding:16px 20px 60px}
.vistas{display:flex;gap:6px}
.vistas button{font-weight:600}.vistas button.ativa{background:var(--acento);color:var(--bg2);border-color:var(--acento)}
.servicos{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;margin:8px 0}
.servico{border:1px solid var(--linha);border-left:4px solid var(--ruim);border-radius:8px;padding:10px 12px;background:var(--bg);display:flex;flex-direction:column;gap:4px}
.servico.no-ar{border-left-color:var(--bom)}
.servico .nome{font-weight:600;line-height:1.3}
.servico .estado{font:600 12px var(--fm);color:var(--ruim)}.servico.no-ar .estado{color:var(--bom)}
.servico a{font-size:13px;overflow-wrap:anywhere}
.atalhos{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:10px 0}
.atalho{display:flex;flex-direction:column;align-items:flex-start;gap:6px}.atalho p{margin:0}
.atalho button,.atalho a.painel{font:600 14px var(--fb);padding:7px 14px;border:1px solid var(--linha);border-radius:6px;background:var(--bg2);color:var(--ink);text-decoration:none}
.atalho button.principal{background:var(--acento);color:var(--bg2);border-color:var(--acento)}
.atalho a.painel:hover{border-color:var(--acento)}
tr.corrida{cursor:pointer}tr.corrida:hover,tr.corrida.aberta{background:var(--acento2)}
tr.corrida td:first-child strong{display:block}
.ressalva{border-left:3px solid var(--meio);padding:4px 12px;margin:8px 0;color:var(--ink)}
.placar{display:flex;flex-wrap:wrap;gap:10px 28px;margin:10px 0}
.placar div{display:flex;flex-direction:column}.placar .numero{font:600 24px var(--fd);font-variant-numeric:tabular-nums}.placar .rotulo-do-numero{font-size:12px;color:var(--ink2)}
.barra,.trilho{height:14px;border:1px solid var(--linha);border-radius:999px;background:var(--bg);overflow:hidden}
#barra-cheia{height:100%;width:0;background:var(--acento)}
.alternativa{display:grid;grid-template-columns:minmax(120px,260px) minmax(60px,1fr) 150px;gap:10px;align-items:center;margin:5px 0}
.trilho{height:10px}.trilho div{height:100%;background:var(--ink2)}.alternativa.escolhida .trilho div{background:var(--acento)}
.alternativa .valor{font:13px var(--fm);color:var(--ink2)}
/* ! Alteração de IA - Revisar: (27/11/2026, coletânea da banca) os cartões das cartas da rodada (escondida, acerto, erro), o lado a lado do que
   foi ligado e do que o agente disse, e a grade das 64 cartas em quadrados por grupo.
   ! Motivo: o bloco da coletânea mostra a rodada em desenho, como o resto do hub; o quadrado apagado e o escondido têm a mesma cor de propósito,
   para a grade não entregar quais cartas estão na rodada antes da resposta. */
.cartas-da-rodada{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:10px;margin:8px 0}
.carta-da-rodada{border:1px solid var(--linha);border-left-width:5px;border-radius:8px;padding:8px 10px;background:var(--bg2)}
.carta-da-rodada p{margin:2px 0}.carta-da-rodada.escondida{border-left-color:var(--linha);color:var(--ink2);border-style:dashed}
.carta-da-rodada.acerto{border-left-color:var(--bom)}.carta-da-rodada.erro{border-left-color:var(--ruim)}
.lado-a-lado{display:grid;grid-template-columns:1fr 1fr;gap:10px}.lado-a-lado h4{margin-top:4px}
.carta-da-rodada .resultado-da-carta{font-weight:600}.carta-da-rodada.acerto .resultado-da-carta{color:var(--bom)}.carta-da-rodada.erro .resultado-da-carta{color:var(--ruim)}
.grade-da-coletanea{display:flex;flex-wrap:wrap;gap:8px 18px;margin:6px 0}
.grupo-da-grade p{margin:0 0 3px}.quadrados{display:flex;flex-wrap:wrap;gap:3px;max-width:180px}
.quadrado{width:16px;height:16px;border-radius:3px;border:1px solid var(--linha);background:var(--bg)}
.quadrado.antes{background:var(--ink2);border-color:var(--ink2)}.quadrado.revelada{background:var(--acento);border-color:var(--acento)}
#comando-da-corrida{user-select:all}
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
mark.trecho-comentado.aceso{outline:2px solid var(--acento);outline-offset:1px}
.conversa.acesa{box-shadow:0 0 0 2px var(--acento)}
td,th,.contagem{font-variant-numeric:tabular-nums}
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
@media (prefers-reduced-motion:no-preference){.item-caso,button{transition:background-color .12s,border-color .12s,color .12s}
.barra.indeterminada #barra-cheia{animation:vai-e-volta 1.4s ease-in-out infinite alternate}}
@keyframes vai-e-volta{from{margin-left:0}to{margin-left:70%}}
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
# ! Alteração de IA - Revisar: (25/11/2026, etapa 3) o programa ganhou a vista "Corrida ao vivo" (a barra de progresso lida de `/api/ao-vivo`, o
# último diagnóstico com as alternativas e os verbetes, e o botão de rodar ou o comando para copiar, por `/api/execucao`), relida sozinha a
# cada dois segundos enquanto está aberta, o botão "Abrir a árvore de decisão" no comentário do agente e o atalho do trace no cabeçalho do caso.
# ! Motivo: decisão 93 (o "Cérebro ao vivo" e o trace na falha) e plano, seção 3.6, item 7 (os botões). A releitura para quando a vista é
# fechada ou a aba do navegador fica escondida, para o hub não ficar lendo o disco à toa durante uma corrida que já disputa a máquina.
JS = r"""'use strict';
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const E = {indice: null, caso: null, aba: 'relatorio', evidencia: null, ancora: null, selecao: null, vista: 'inicio', relogio: null, ultimo: null,
  relogioDoInicio: null, metricas: null, corridaDasMetricas: null, corridaRodando: false, grupos: {}, porTid: {}, linhaAoVivo: null, assinaturaDoWorkspace: null};
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
  const itens = [el('span', {class: 'etiqueta conf-' + (c.selo || 'sem'), text: 'confiança ' + c.confianca, title: 'O selo que o código dá à resposta do modelo, pela probabilidade lida'})];
  if (c.divergencia) itens.push(el('span', {class: 'etiqueta alerta', text: 'divergência', title: 'O que o modelo declarou não bate com o que o código conferiu'}));
  if (c.cura) itens.push(el('span', {class: 'etiqueta', text: 'cura', title: 'O agente achou outro seletor para o localizador quebrado e refez o roteiro'}));
  if (r.veredito) itens.push(el('span', {class: 'etiqueta veredito', text: r.veredito_rotulo, title: 'O veredito do analista sobre este diagnóstico'}));
  if (r.ativas) itens.push(el('span', {class: 'etiqueta conversa-ativa', text: r.ativas === 1 ? '1 conversa ativa' : r.ativas + ' conversas ativas'}));
  return itens;
}

function itemDaLista(c) {
  const li = el('li', {class: 'item-caso', data: {tid: c.tid, caso: c.caso, corrida: c.corrida}, tabindex: '0', role: 'button'},
    el('span', {class: 'titulo-do-item'}, comCodigo(c.titulo)),
    el('span', {class: 'meta', text: c.nome + ' · iteração ' + c.iteracao + ' de ' + c.iteracoes,
      title: 'O nome do caso e qual das vezes em que o agente o diagnosticou é esta'}),
    el('span', {class: 'etiquetas'}, etiquetas(c)));
  li.addEventListener('click', () => abrirCaso(c.tid));
  li.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); abrirCaso(c.tid); } });
  return li;
}

// ! Alteração de IA - Revisar: (26/11/2026, molde visual do hub, ficha 113) a lista de casos passa a ser desenhada em grupos, um por corrida, que abrem
// e fecham; sem filtro, só o primeiro grupo vem aberto (todos, quando o hub tem até doze casos) e cada grupo mostra quinze casos por vez, com o
// botão "Mostrar mais"; com filtro (corrida, busca ou "só sem veredito") aparecem todos os que batem, de todos os grupos.
// ! Motivo: o Eric testou o hub com os 170 diagnósticos numa lista só e pediu o fim da rolagem quase sem fim e a explicação de cada campo. Todos
// os casos continuam na página (escondidos), para a busca e os filtros acharem qualquer um sem pedir nada ao servidor.
const POR_VEZ = 15;

function estadoDoGrupo(pasta) {
  if (!E.grupos[pasta]) E.grupos[pasta] = {aberto: E.indice.casos.length <= 12 || E.indice.corridas.findIndex(c => c.pasta === pasta) === 0, limite: POR_VEZ};
  return E.grupos[pasta];
}

function grupoDaLista(corrida) {
  const cabeca = el('button', {type: 'button', class: 'cabeca-do-grupo', data: {corrida: corrida.pasta}, title: corrida.descricao || 'Os diagnósticos desta corrida'},
    el('span', {class: 'nome-do-grupo', text: corrida.rotulo}), el('span', {class: 'contagem'}));
  cabeca.addEventListener('click', () => { const g = estadoDoGrupo(corrida.pasta); g.aberto = !g.aberto; filtrar(); });
  const mais = el('button', {type: 'button', class: 'mostrar-mais'});
  mais.addEventListener('click', () => { estadoDoGrupo(corrida.pasta).limite += POR_VEZ; filtrar(); });
  return el('li', {class: 'grupo-de-casos', data: {corrida: corrida.pasta}}, cabeca,
    el('ul', {class: 'casos-do-grupo'}, E.indice.casos.filter(c => c.corrida === corrida.pasta).map(itemDaLista)), mais);
}

function desenharLista() {
  E.porTid = Object.fromEntries(E.indice.casos.map(c => [c.tid, c]));
  $('#lista-de-casos').replaceChildren(...E.indice.corridas.map(grupoDaLista));
  filtrar();
}

function filtrar() {
  const corrida = $('#filtro-corrida').value, texto = $('#filtro-texto').value.trim().toLowerCase(), semVeredito = $('#filtro-sem-veredito').checked;
  const comFiltro = Boolean(corrida || texto || semVeredito);
  let batem = 0;
  for (const grupo of $$('#lista-de-casos .grupo-de-casos')) {
    const estado = estadoDoGrupo(grupo.dataset.corrida);
    let noGrupo = 0, total = 0;
    for (const li of $$('.item-caso', grupo)) {
      const c = E.porTid[li.dataset.tid];
      total += 1;
      const alvo = [c.tid, c.titulo, c.escolha, c.causa_em_palavras, c.campo].join(' ').toLowerCase();
      const bate = (!corrida || c.corrida === corrida) && (!texto || alvo.includes(texto)) && (!semVeredito || !(c.revisao && c.revisao.veredito));
      if (bate) noGrupo += 1;
      li.hidden = !(bate && (comFiltro || (estado.aberto && noGrupo <= estado.limite)));
    }
    batem += noGrupo;
    grupo.hidden = comFiltro && noGrupo === 0;
    $('.cabeca-do-grupo', grupo).setAttribute('aria-expanded', String(comFiltro ? noGrupo > 0 : estado.aberto));
    $('.cabeca-do-grupo .contagem', grupo).textContent = comFiltro ? noGrupo + ' de ' + total : total + (total === 1 ? ' caso' : ' casos');
    const resto = noGrupo - estado.limite, mais = $('.mostrar-mais', grupo);
    mais.hidden = comFiltro || !estado.aberto || resto <= 0;
    mais.textContent = 'Mostrar mais ' + Math.min(POR_VEZ, Math.max(0, resto)) + ' (faltam ' + Math.max(0, resto) + ')';
  }
  $('#contagem-de-casos').textContent = batem + ' de ' + E.indice.casos.length + ' casos';
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
  const vista = ['ao-vivo', 'metricas'].includes(p.get('vista')) ? p.get('vista') : (p.get('caso') ? 'casos' : 'inicio');
  return {tid: p.get('caso'), aba: ABAS.includes(p.get('aba')) ? p.get('aba') : 'relatorio', vista};
}

function gravarEndereco() {
  const p = new URLSearchParams();
  if (E.caso && E.vista !== 'inicio') p.set('caso', E.caso.tid);
  p.set('aba', E.aba);
  if (E.vista === 'ao-vivo' || E.vista === 'metricas') p.set('vista', E.vista);
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
  $('#titulo-do-caso').replaceChildren(...comCodigo(c.titulo));
  $('#meta-do-caso').textContent = c.corrida.rotulo + (c.corrida.descricao ? ' (' + c.corrida.descricao + ')' : '') + ' · ' + c.nome + ' · iteração ' + c.iteracao + ' de '
    + c.iteracoes.length + ' · modelo ' + c.corrida.modelo;
  $('#seletor-de-iteracao').replaceChildren(...c.iteracoes.map(i => el('option', {value: i.tid, text: 'iteração ' + i.numero + ' · ' + i.rotulo_da_corrida + ' · ' + i.nome + ' · ' + quando(i.ts),
    selected: i.tid === c.tid})));
  $('#seletor-de-iteracao').value = c.tid;
  $('#aviso-de-iteracao').textContent = c.iteracao < c.iteracoes.length ? 'Há iteração mais nova: a ' + c.iteracoes.length + ' é a última.' : '';
  desenharMudancas();
  const trace = $('#trace-do-caso');
  trace.replaceChildren();
  if (c.trace.existe) {
    trace.append('Trace do Playwright da falha: ', el('a', {href: '/api/trace?tid=' + encodeURIComponent(c.tid), text: 'baixar ' + c.trace.arquivo}),
      ' · para abrir no visualizador: ', el('code', {text: c.trace.comando}));
  } else {
    trace.append('Sem trace gravado: a corrida rodou com o trace desligado (o padrão), ou o roteiro não falhou neste caso.');
  }
  const ag = c.comentario_do_agente;
  const abrirArvore = el('button', {type: 'button', id: 'abrir-arvore', text: 'Abrir a árvore de decisão'});
  abrirArvore.addEventListener('click', () => mostrarAba('arvore'));
  $('#comentario-do-agente').replaceChildren(
    el('p', {class: 'meta'}, el('span', {class: 'autor', text: ag.autor.nome}), ' · ' + quando(ag.ts) + ' · o agente só comenta: o veredito é do analista'),
    el('p', {}, comCodigo(ag.texto)), abrirArvore);
  $('#preambulo').innerHTML = c.relatorio.preambulo_html;
  $('#rastro').innerHTML = c.relatorio.rastro_html;
  desenharEvidencia();
  // a árvore de decisão abre na rede desenhada (molde visual, ficha 113); o texto corrido, com a origem de cada frase, fica recolhido logo abaixo
  const porEscrito = el('div', {class: 'arvore-por-escrito'});
  porEscrito.innerHTML = c.arvore_html;
  $('#aba-arvore').replaceChildren(el('h2', {text: 'Como o agente chegou à causa'}), el('div', {id: 'rede-da-decisao', class: 'diagrama rolavel'}),
    el('details', {class: 'por-escrito'}, el('summary', {text: 'Ver a árvore de decisão por escrito, com a origem de cada frase'}), porEscrito));
  desenharTrilha();
  desenharRevisao();
  mostrarAba(ABAS.includes(E.aba) ? E.aba : 'relatorio');
  for (const li of $$('#lista-de-casos .item-caso')) li.classList.toggle('aberto', li.dataset.tid === c.tid);
  mostrarVista('casos');
  desenharProcessoDoCaso();     // depois de a vista aparecer: o desenho mede a largura do lugar onde entra
  abrirGrupoDoCaso(c.tid);
  main.scrollTop = 0;
  main.dataset.tid = c.tid;
}

// ---------------------------------------------------------------- a corrida ao vivo

// ! Alteração de IA - Revisar: (25/11/2026, ficha 109, decisão 170) a página passou a ter quatro vistas: "Início" (a que abre), o caso, "Corrida
// ao vivo" e "Métricas". `mostrarVista` mostra uma e esconde as outras; sem caso aberto, a vista do caso cai no "Início".
// ! Motivo: o Eric pediu o hub como central de tudo, aberta pelo `.exe`: a primeira tela diz o que está no ar e leva ao site, à API, ao
// painel, a rodar os cenários e às métricas. Antes a página abria numa frase ("Escolha um caso na lista"), que não dizia nada a quem acabou
// de dar dois cliques no `.exe`. O "Início" relê o estado dos serviços a cada cinco segundos só enquanto está à vista.
function mostrarVista(vista) {
  if (vista === 'casos' && !E.caso) vista = 'inicio';
  E.vista = vista;
  const vivo = vista === 'ao-vivo', inicio = vista === 'inicio', metricas = vista === 'metricas';
  $('#ao-vivo').hidden = !vivo;
  $('#inicio').hidden = !inicio;
  $('#metricas').hidden = !metricas;
  $('#caso').hidden = vista !== 'casos';
  $('#abrir-ao-vivo').classList.toggle('ativa', vivo);
  $('#abrir-inicio').classList.toggle('ativa', inicio);
  $('#abrir-metricas').classList.toggle('ativa', metricas);
  $('#comentar-trecho').hidden = true;
  if (vivo) {
    atualizarAoVivo();
    if (!E.relogio) E.relogio = setInterval(atualizarAoVivo, 2000);
  } else if (E.relogio) {
    clearInterval(E.relogio);
    E.relogio = null;
  }
  if (inicio) {
    atualizarInicio();
    if (!E.relogioDoInicio) E.relogioDoInicio = setInterval(atualizarInicio, 5000);
  } else if (E.relogioDoInicio) {
    clearInterval(E.relogioDoInicio);
    E.relogioDoInicio = null;
  }
  if (metricas) atualizarMetricas();
  gravarEndereco();
}

// ---------------------------------------------------------------- o início e as métricas

async function recarregarIndice() {
  let indice;
  try { indice = await api('/api/indice'); } catch (e) { return; }
  E.indice = indice;
  const seletor = $('#filtro-corrida'), escolhida = seletor.value;
  seletor.replaceChildren(el('option', {value: '', text: 'todas'}));
  preencher('#filtro-corrida', indice.corridas.map(c => [c.pasta, c.rotulo + ' (' + c.casos + ')']));
  seletor.value = [...seletor.options].some(o => o.value === escolhida) ? escolhida : '';
  desenharLista();
  if (E.caso) for (const li of $$('#lista-de-casos .item-caso')) li.classList.toggle('aberto', li.dataset.tid === E.caso.tid);
}

async function atualizarInicio() {
  if (document.hidden) return;
  let c;
  try { c = await api('/api/central'); } catch (e) { mostrarErro(e.message); return; }
  desenharInicio(c);
  if (E.indice && c.casos !== E.indice.casos.length) recarregarIndice();     // uma corrida gravou caso novo desde que a lista foi lida
}

function desenharInicio(c) {
  const plural = (n, um, varios) => n + ' ' + (n === 1 ? um : varios);
  $('#resumo-do-inicio').textContent = plural(c.casos, 'caso', 'casos') + ' com diagnóstico do agente em ' + plural(c.corridas, 'corrida', 'corridas') + '. '
    + (c.pelo_exe ? 'Aberta pelo Cobaia.exe: o site e a API de demonstração sobem junto, e fechar a janela dele encerra tudo.'
      : 'Aberta por python hub.py: o site e a API de demonstração só aparecem no ar se alguém os subiu (o Cobaia.exe sobe tudo de uma vez).');
  const quadro = $('#servicos');
  if (quadro.children.length !== c.servicos.length) {
    quadro.replaceChildren(...c.servicos.map(s => el('div', {class: 'servico', data: {servico: s.id}},
      el('span', {class: 'nome', text: s.nome}), el('span', {class: 'estado'}),
      s.url ? el('a', {href: s.url, target: '_blank', rel: 'noopener noreferrer', text: s.url.replace('http://', '')}) : null)));
  }
  for (const s of c.servicos) {       // o cartão é atualizado no lugar: trocá-lo a cada releitura podia engolir um clique no endereço
    const cartao = quadro.querySelector('.servico[data-servico="' + CSS.escape(s.id) + '"]');
    cartao.classList.toggle('no-ar', s.no_ar);
    $('.estado', cartao).textContent = s.no_ar ? 'no ar' : 'fora do ar';
  }
  const fora = id => c.servicos.some(s => s.id === id && !s.no_ar);
  $('#nota-dos-servicos').textContent = [
    (fora('site') || fora('api')) ? 'Para subir o site e a API, abra o Cobaia.exe (ou rode python run.py na raiz do repositório).' : '',
    fora('ollama') ? (c.pelo_exe ? 'O Ollama só precisa estar no ar para rodar os cenários: ao lançar a corrida, o hub tenta iniciá-lo.'
      : 'O Ollama só precisa estar no ar para rodar os cenários.') : ''].filter(Boolean).join(' ');
  $('#ir-para-rodar').textContent = c.execucao_permitida ? 'Rodar os cenários' : 'Ver como rodar os cenários';
  $('#nota-de-rodar').textContent = c.execucao_permitida
    ? 'Ativa o agente nos dez cenários de quebra do site, com o modelo local. Leva cerca de um minuto por cenário, e a corrida aparece na lista de casos.'
    : 'Sem o Cobaia.exe, o hub mostra o comando para copiar e rodar na sua janela do PowerShell.';
  // o painel local (pedido do Eric em 26/11/2026): o botão leva ao arquivo desta máquina, servido pelo hub, e o aviso diz quando ele está atrás das fontes
  const pn = c.painel || {}, aviso = $('#aviso-do-painel');
  $('#abrir-painel').setAttribute('href', pn.url || '/painel');
  aviso.hidden = pn.existe && !pn.atrasado;
  aviso.replaceChildren(...(!pn.existe ? ['O painel ainda não foi gerado nesta máquina. Na raiz do repositório, rode ', el('code', {text: 'python ferramentas/gerar_dashboard.py'}), '.']
    : pn.atrasado ? ['O painel foi gerado antes da última mudança em ', el('code', {text: pn.fonte_mais_nova}), '. Para atualizar, rode ', el('code', {text: 'python ferramentas/gerar_dashboard.py'}),
      ' na raiz do repositório.'] : []));
  const assinatura = c.servicos.map(s => s.id + ':' + s.no_ar).join(' ');     // o diagrama só é refeito quando um serviço sobe ou cai
  if (assinatura !== E.assinaturaDoWorkspace) { E.assinaturaDoWorkspace = assinatura; desenharWorkspaces($('#workspaces'), c); }
}

async function atualizarMetricas() {
  let m;
  try { m = await api('/api/metricas'); } catch (e) { mostrarErro(e.message); return; }
  E.metricas = m;
  desenharMetricas();
}

function comVirgula(v, casas) { return typeof v === 'number' ? v.toFixed(casas).replace('.', ',') : ''; }

// ! Alteração de IA - Revisar: (26/11/2026, molde visual do hub, ficha 113) a vista "Métricas" passa a abrir em gráficos de barras: o tempo médio de
// reparo do agente e das pessoas, o tempo médio de reparo de cada corrida que roda cenários, a confiança dos diagnósticos por corrida e, da corrida
// escolhida, o tempo de cada cenário. A tabela com os números e as frases por extenso ficam recolhidas.
// ! Motivo: o Eric pediu gráficos no lugar do texto, que por escrito fica denso. Os valores são os de `/api/metricas`, sem conta nova aqui, e a
// ressalva do Task Success (decisão 151) continua à vista, ao lado das contagens, e não dentro do texto recolhido.
function desenharMetricas() {
  const m = E.metricas, f = m.fase5, alto = $('#metricas-da-fase-5');
  alto.hidden = !f;
  if (f) {
    const t = f.tempo_medio_s || {}, grafico = el('div', {id: 'grafico-da-fase-5', class: 'diagrama'});
    alto.replaceChildren(
      el('h2', {text: 'O agente contra as pessoas (Fase 5)'}), el('h3', {text: 'Tempo médio de reparo: quanto menor, melhor'}), grafico,
      el('div', {class: 'fichas'},
        el('span', {class: 'ficha', title: 'Task Success: em quantas execuções o agente chegou ao resultado certo'}, 'o agente chegou ao resultado em ', el('b', {text: f.agente.sucessos + ' de ' + f.agente.n})),
        el('span', {class: 'ficha', title: 'Em quantas tentativas as pessoas chegaram ao resultado certo'}, 'as pessoas, em ', el('b', {text: f.pessoas.sucessos + ' de ' + f.pessoas.n}))),
      f.ressalva ? el('p', {class: 'ressalva', text: 'Ressalva do Task Success: ' + f.ressalva}) : null,
      el('details', {class: 'por-extenso'}, el('summary', {text: 'Ler o resultado por extenso'}), el('p', {text: f.tempo}), el('p', {text: f.task_success}),
        el('p', {class: 'nota'}, 'Frases e números copiados de ', el('code', {text: 'resultados_alvo/fase5/medicao.json'}),
          ', a leitura da comparação pelas regras fixadas antes das medidas' + (f.corrida ? ' (corrida do agente: ' + f.corrida + ').' : '.'))));
    if (typeof t.agente === 'number' && typeof t.pessoas === 'number') graficoDeBarras(grafico, [
      {rotulo: 'Agente', valor: t.agente, texto: comVirgula(t.agente, 1) + ' s', classe: 'agente'},
      {rotulo: 'Pessoas', valor: t.pessoas, texto: comVirgula(t.pessoas, 1) + ' s', classe: 'pessoas'}], 'barra-do-lado', 'Tempo médio de reparo do agente e das pessoas');
  }
  const reparo = c => (c.mttr_media_s === null ? 'sem reparo medido' : comVirgula(c.mttr_media_s, 1) + ' s');
  const comCenarios = m.corridas.filter(c => typeof c.execucoes === 'number' && c.execucoes > 0);
  if (!m.corridas.some(c => c.pasta === E.corridaDasMetricas)) E.corridaDasMetricas = comCenarios.length ? comCenarios[comCenarios.length - 1].pasta : null;
  graficoDeBarras($('#grafico-do-reparo'), comCenarios.map(c => ({rotulo: c.rotulo, valor: c.mttr_media_s, texto: reparo(c) + ' · ' + c.task_success + ' de ' + c.execucoes,
    data: {corrida: c.pasta}, destaque: E.corridaDasMetricas === c.pasta, dica: c.rotulo + ': tempo médio de reparo ' + reparo(c) + '; chegou ao resultado em ' + c.task_success + ' de ' + c.execucoes
      + ' execuções. Clique para ver cenário por cenário.', aoClicar: () => { E.corridaDasMetricas = c.pasta; desenharMetricas(); }})), 'barra-da-corrida', 'Tempo médio de reparo por corrida');
  const semCenarios = m.corridas.filter(c => !(typeof c.execucoes === 'number' && c.execucoes > 0)).map(c => c.rotulo);
  $('#nota-do-reparo').textContent = (comCenarios.length ? 'Ao lado do tempo, em quantas execuções o agente chegou ao resultado. Clique numa barra para ver cenário por cenário. ' : '')
    + (semCenarios.length ? 'Sem barra: ' + semCenarios.join(', ') + ', que diagnosticam casos em texto ou na tela e não rodam cenários.' : '');
  const classeDaConfianca = {alta: 'seg-alta', 'média': 'seg-media', baixa: 'seg-baixa'};
  graficoDeBarras($('#grafico-da-confianca'), m.corridas.map(c => ({rotulo: c.rotulo, partes: Object.entries(c.confianca).map(([nome, n]) => ({classe: classeDaConfianca[nome] || 'seg-outra', n})),
    texto: c.casos + (c.casos === 1 ? ' caso' : ' casos'), data: {corrida: c.pasta},
    dica: c.rotulo + ': ' + (Object.entries(c.confianca).map(([nome, n]) => nome + ' ' + n).join(', ') || 'sem casos')})), 'barra-da-confianca', 'Confiança dos diagnósticos por corrida');
  $('#metricas-por-corrida').replaceChildren(...m.corridas.map(c => {
    const confianca = Object.entries(c.confianca).map(([nome, n]) => nome + ' ' + n).join(' · ') || 'sem casos';
    const medida = c.vale_como_medida === true ? 'sim' : c.vale_como_medida === false ? 'não' : 'não declarada';
    const dosCenarios = typeof c.execucoes === 'number'
      ? [el('td', {text: String(c.execucoes)}), el('td', {text: c.task_success + ' de ' + c.execucoes}), el('td', {text: c.detectou + ' de ' + c.execucoes}), el('td', {text: reparo(c)})]
      : [el('td', {colspan: '4', class: 'nota', text: 'não rodou cenários: diagnostica os casos em texto ou na tela'})];
    return el('tr', {class: 'corrida', data: {corrida: c.pasta}}, el('td', {}, el('strong', {text: c.rotulo}), el('code', {text: c.pasta})), el('td', {text: String(c.casos)}),
      el('td', {text: confianca}), ...dosCenarios, el('td', {text: medida}));
  }));
  const aberta = m.corridas.find(c => c.pasta === E.corridaDasMetricas), detalhe = $('#metricas-por-cenario');
  detalhe.hidden = !aberta;
  if (!aberta) return;
  const verCasos = el('button', {type: 'button', id: 'ver-casos-da-corrida', text: 'Mostrar só os casos desta corrida na lista'});
  verCasos.addEventListener('click', () => { $('#filtro-corrida').value = aberta.pasta; filtrar(); });
  const grafico = el('div', {id: 'grafico-dos-cenarios', class: 'diagrama'});
  detalhe.replaceChildren(el('h2', {text: 'Cenário por cenário: ' + aberta.rotulo}), aberta.descricao ? el('p', {class: 'nota', text: aberta.descricao}) : null, grafico,
    aberta.por_cenario.length ? null : el('p', {class: 'nota', text: 'Esta corrida não rodou cenários; os casos dela estão na lista ao lado.'}), verCasos);
  graficoDeBarras(grafico, aberta.por_cenario.map(x => ({rotulo: x.cenario, valor: x.mttr_media_s, texto: reparo(x) + ' · ' + x.task_success + ' de ' + x.execucoes,
    dica: x.cenario + (x.tipo ? ' (' + x.tipo + ')' : '') + ': tempo médio de reparo ' + reparo(x) + '; chegou ao resultado em ' + x.task_success + ' de ' + x.execucoes + '; falha detectada em '
      + x.detectou + ' de ' + x.execucoes, classe: x.task_success === x.execucoes ? '' : 'com-falha'})), 'barra-do-cenario', 'Tempo médio de reparo de cada cenário');
}

function segundos(s) {
  if (typeof s !== 'number') return '';
  return s < 90 ? Math.round(s) + ' s' : Math.floor(s / 60) + ' min ' + Math.round(s % 60) + ' s';
}

// ! Alteração de IA - Revisar: (25/11/2026, Pós-Fase 4, pacote Q7) a escolha "o que rodar" (os dez cenários, ou só os atingidos pelo que mudou no
// Git), o campo do commit de partida e a prévia do que a seleção rodaria e deixaria de fora, com o motivo de cada cenário.
// ! Motivo: plano, seção 3.7: a seleção diz quais cenários rodar e por quê. A prévia é pedida quando a escolha muda, e não a cada releitura
// da vista, para o hub não consultar o Git a cada dois segundos; o commit digitado só vai ao servidor junto com a seleção pelo Git.
// ! Alteração de IA - Revisar: (27/11/2026, coletânea da banca) as opções levam também quantas cartas e o número da banca, só com a coletânea.
// ! Motivo: o servidor recusa o número nas outras escolhas, e com a coletânea as repetições são sempre 1.
function opcoesDaCorrida() {
  const selecao = $('#selecao-da-corrida').value, coletanea = selecao === 'coletanea';
  return {selecao, desde: selecao === 'git' ? ($('#desde-da-corrida').value.trim() || null) : null, repeticoes: coletanea ? 1 : Number($('#repeticoes').value || 1),
          quantas: coletanea ? Number($('#quantas-da-corrida').value || 5) : null, numero: coletanea ? ($('#numero-da-corrida').value.trim() || null) : null};
}

async function atualizarSelecao() {
  const o = opcoesDaCorrida(), alvo = $('#previa-da-selecao');
  $('#campo-do-desde').hidden = o.selecao !== 'git';
  for (const id of ['#campo-das-quantas', '#campo-do-numero', '#nota-da-coletanea']) $(id).hidden = o.selecao !== 'coletanea';   // coletânea da banca
  if (o.selecao !== 'git') { alvo.replaceChildren(); mostrarErro(''); return; }
  let d;
  try { d = await api('/api/selecao' + (o.desde ? '?desde=' + encodeURIComponent(o.desde) : '')); } catch (e) { mostrarErro(e.message); return; }
  mostrarErro('');
  const modo = {completa: 'completa: os ' + d.cenarios.length + ' cenários', selecionada: 'selecionada: ' + d.cenarios.length + ' cenários', nada: 'vazia: nada a rodar'}[d.modo] || d.modo;
  const lista = (itens, porQue) => itens.length
    ? el('ul', {}, itens.map(c => el('li', {}, el('code', {text: c}), porQue && porQue[c] && porQue[c].length ? ' · ' + porQue[c][0] : '')))
    : el('p', {class: 'nota', text: 'nenhum'});
  alvo.replaceChildren(
    el('h3', {text: 'Pelo que mudou no Git, a corrida seria ' + modo}),
    el('p', {text: d.motivo}),
    el('p', {class: 'meta', text: 'Do commit ' + (d.commit_testado ? d.commit_testado.slice(0, 10) : 'nenhum (não há ponto de partida)') + ' até o commit '
      + String(d.commit_atual || '').slice(0, 10) + (d.arvore_suja ? ', mais as alterações ainda não commitadas nas pastas das cobaias' : '') + '.'}),
    el('h4', {text: 'Cenários que rodariam'}), lista(d.cenarios, d.por_que),
    el('h4', {text: 'Deixados de fora, registrados para a conferência contra a rodada completa'}), lista(d.deixados_de_fora, null));
}

async function atualizarAoVivo() {
  if (document.hidden) return;
  const o = opcoesDaCorrida(), consulta = new URLSearchParams({selecao: o.selecao, repeticoes: String(o.repeticoes)});
  if (o.desde) consulta.set('desde', o.desde);
  if (o.quantas) consulta.set('quantas', String(o.quantas));
  if (o.numero && /^\d{1,18}$/.test(o.numero)) consulta.set('numero', o.numero);    // número ainda errado: a recusa vem no clique, e a vista segue viva
  let vivo, exec;
  try { [vivo, exec] = await Promise.all([api('/api/ao-vivo'), api('/api/execucao?' + consulta.toString())]); } catch (e) { mostrarErro(e.message); return; }
  desenharLinhaAoVivo(vivo);
  desenharBarra(vivo);
  desenharCerebro(vivo.ultimo_diagnostico || null);
  desenharColetanea(vivo.coletanea || null);
  desenharExecucao(exec);
}

// ! Alteração de IA - Revisar: (27/11/2026, coletânea da banca, decisões 194 a 196) o bloco da rodada da coletânea: o resumo (número, de onde veio,
// posição na pilha, quantas faltam e a conferência do mesmo agente da medida), um cartão por carta, a grade das 64 cartas e o fim da rodada.
// ! Motivo: a carta escondida chega do servidor só com a posição, e o quadrado apagado sem o nome; esta função não tem como mostrar o erro antes da
// resposta. O cartão revelado põe lado a lado o que foi ligado e o que o agente disse, para a banca comparar sem precisar ler a trilha.
function desenharColetanea(c) {
  $('#coletanea').hidden = !c;
  if (!c) return;
  const m = c.mesmo_agente;
  const agente = !m ? 'a conferência do mesmo agente da medida não pôde ser feita (faltam as condições de uma das corridas)'
    : m.prompt_fixo && m.biblioteca ? 'mesmo agente da medida: o prompt fixo e a biblioteca têm os mesmos códigos da corrida ' + m.referencia
      : 'atenção: o prompt fixo ou a biblioteca não têm os mesmos códigos da corrida ' + m.referencia;
  $('#coletanea-resumo').textContent = 'Número ' + c.numero + (c.origem === 'relógio' ? ' (a hora do clique: ninguém disse um número)' : ' (dito pela banca)')
    + ' · cartas ' + c.de + ' a ' + c.ate + ' de ' + c.total + ' da pilha · faltam ' + c.faltam + ' · ' + agente + '.';
  $('#coletanea-cartas').replaceChildren(...c.cartas_da_rodada.map(cartaDaRodada));
  $('#coletanea-grade').replaceChildren(...c.grade.map(g => el('div', {class: 'grupo-da-grade'},
    el('p', {class: 'meta', text: g.nome + ' (' + g.cartas.length + ')', title: g.pergunta}),
    el('div', {class: 'quadrados'}, g.cartas.map(q => el('span', {class: 'quadrado' + (q.marca ? ' ' + q.marca : ''), role: 'img',
      title: q.marca ? q.descricao : 'apagado: na pilha, ou escondido até a resposta', 'aria-label': q.marca ? q.descricao : 'carta apagada'}))))));
  $('#coletanea-fim').replaceChildren(...(c.lista
    ? [el('h3', {text: 'A rodada inteira, na ordem da pilha'}), el('ol', {start: String(c.de)}, c.lista.map(i => el('li', {}, el('code', {text: i})))),
       el('p', {}, 'Para refazer o sorteio em qualquer máquina, na pasta experimentos: ', el('code', {text: c.comando}))]
    : [el('p', {class: 'nota', text: 'A rodada inteira e o comando que refaz o sorteio aparecem quando a última carta for respondida.'})]));
}

function cartaDaRodada(k) {
  if (!k.revelada) return el('div', {class: 'carta-da-rodada escondida'}, el('p', {class: 'meta', text: k.nome}), el('p', {text: 'escondida até o agente responder'}));
  const a = k.agente;
  const disse = k.tipo === 'sem_erro' ? (a.detectou ? 'acusou uma falha' : 'nada foi acusado, e o modelo nem foi chamado')
    : !a.detectou ? 'a falha não foi detectada'
      : 'causa ' + (a.rotulo || 'nenhuma') + (k.tipo === 'contrato' ? ', campo ' + (a.campo || 'nenhum') : '')
        + (k.tipo === 'localizador' ? (a.curado ? '; a cura fez o roteiro voltar a passar' : '; a cura não fez o roteiro voltar a passar') : '');
  const certo = k.tipo === 'sem_erro' ? 'nenhuma falha' : 'causa ' + k.causa_certa + (k.tipo === 'contrato' ? ', campo ' + (k.campo_certo || 'nenhum') : '');
  const bom = k.veredito === 'acertou' || k.veredito.startsWith('certo');
  return el('div', {class: 'carta-da-rodada revelada ' + (bom ? 'acerto' : 'erro')},
    el('p', {class: 'meta', text: k.nome + ' · ' + (k.grupo || '') + (k.medido_na_fase_5 ? ' · um dos dez da medida da Fase 5' : '')}),
    el('div', {class: 'lado-a-lado'},
      el('div', {}, el('h4', {text: 'O que foi ligado'}), el('p', {}, comCodigo(k.o_que_foi_ligado)), el('p', {class: 'nota', text: 'O certo: ' + certo})),
      el('div', {}, el('h4', {text: 'O que o agente disse'}), el('p', {text: disse}))),
    el('p', {class: 'resultado-da-carta', text: k.veredito}));
}

function desenharBarra(v) {
  const barra = $('#barra'), cheia = $('#barra-cheia');
  if (!v.ha_corrida) {
    $('#estado-ao-vivo').textContent = 'Nenhuma corrida gravou o estado da barra nesta pasta de resultados.';
    $('#etapa-ao-vivo').textContent = '';
    $('#tempo-ao-vivo').textContent = '';
    barra.removeAttribute('aria-valuenow');
    barra.classList.remove('indeterminada');
    cheia.style.width = '0%';
    return;
  }
  const p = v.progresso || {};
  const rodando = {indeterminado: 'o modelo está trabalhando, ainda sem estimativa de tempo', determinado: 'o modelo está trabalhando'};
  const parada = {concluido: 'a última inferência terminou', cancelado: 'a corrida foi cancelada', falhou: 'a última inferência falhou'};
  const situacao = v.em_andamento ? (rodando[p.estado] || 'em andamento')
    : (parada[p.estado] || 'parada: o estado da barra não é regravado há ' + segundos(v.idade_s));
  $('#estado-ao-vivo').textContent = 'Corrida ' + v.pasta + ': ' + situacao + ' · ' + v.diagnosticos + (v.diagnosticos === 1 ? ' diagnóstico gravado' : ' diagnósticos gravados') + ' na trilha.';
  $('#etapa-ao-vivo').textContent = p.etapa ? 'Etapa: ' + p.etapa + (v.em_andamento && p.fase ? ' · ' + (p.fase === 'prefill' ? 'lendo o caso' : 'escrevendo a resposta') : '') : '';
  const pct = typeof p.fracao === 'number' ? Math.round(Math.max(0, Math.min(1, p.fracao)) * 100) : null;
  if (pct === null) {
    barra.removeAttribute('aria-valuenow');
    barra.classList.toggle('indeterminada', v.em_andamento);
    cheia.style.width = v.em_andamento ? '30%' : '0%';
  } else {
    barra.setAttribute('aria-valuenow', String(pct));
    barra.classList.remove('indeterminada');
    cheia.style.width = pct + '%';
  }
  const estimativa = p.estimativa_refeita_s || p.estimativa_s;
  $('#tempo-ao-vivo').textContent = [typeof p.decorrido_s === 'number' ? 'decorrido ' + segundos(p.decorrido_s) : '',
    typeof estimativa === 'number' ? 'estimativa de ' + segundos(estimativa) : '',
    typeof p.inferencias_concluidas === 'number' ? p.inferencias_concluidas + (p.inferencias_concluidas === 1 ? ' inferência concluída' : ' inferências concluídas') : '']
    .filter(Boolean).join(' · ');
}

function desenharCerebro(u) {
  const alvo = $('#cerebro-conteudo');
  E.ultimo = u && u.no_hub ? u.tid : null;
  $('#abrir-ultimo').hidden = !E.ultimo;
  if (!u) { alvo.replaceChildren(el('p', {class: 'nota', text: 'Nenhum diagnóstico gravado ainda nesta corrida.'})); return; }
  const linhas = u.alternativas.map(a => {
    const cheio = el('div');
    cheio.style.width = (typeof a.probabilidade === 'number' ? Math.max(1, Math.round(a.probabilidade * 100)) : 0) + '%';
    return el('div', {class: 'alternativa' + (a.escolhida ? ' escolhida' : '')}, el('code', {text: a.opcao}), el('div', {class: 'trilho'}, cheio),
      el('span', {class: 'valor', text: typeof a.probabilidade === 'number' ? (a.probabilidade * 100).toFixed(1).replace('.', ',') + '%' : 'sem probabilidade lida'}));
  });
  alvo.replaceChildren(
    el('p', {class: 'meta', text: u.nome + ' · ' + quando(u.ts)}),
    el('h3', {}, comCodigo(u.titulo)),
    el('p', {}, 'Causa respondida: ', el('code', {text: u.escolha || 'nenhuma'}), u.causa_em_palavras ? ' (' + u.causa_em_palavras + ')' : '', ' · confiança ' + u.confianca
      + (u.divergencia ? ' · o que o modelo declarou não bate com o que o código conferiu' : '') + (u.cura ? ' · localizador curado' : '')),
    el('h4', {text: 'Alternativas, com a probabilidade lida na causa'}), ...(linhas.length ? linhas : [el('p', {class: 'nota', text: 'A resposta não trouxe alternativas.'})]),
    el('h4', {text: 'Verbetes entregues ao modelo'}), el('ul', {}, u.verbetes.map(v => el('li', {}, v.titulo + ' ', el('code', {text: v.id})))));
}

function desenharExecucao(x) {
  const livre = x.permitida && !x.em_andamento;
  $('#rodar-cenarios').hidden = !livre;
  $('#campo-das-repeticoes').hidden = !livre || $('#selecao-da-corrida').value === 'coletanea';   // coletânea: sempre uma repetição
  $('#parar-corrida').hidden = !(x.permitida && x.em_andamento);
  $('#comando-da-corrida').hidden = x.permitida;
  $('#copiar-comando').hidden = x.permitida;
  $('#comando-da-corrida').textContent = x.comando_sugerido;
  if (!$('#repeticoes').options.length) for (const n of x.repeticoes) $('#repeticoes').append(el('option', {value: String(n), text: String(n)}));
  if (!$('#quantas-da-corrida').options.length) for (const n of x.quantas || []) $('#quantas-da-corrida').append(el('option', {value: String(n), text: String(n), selected: n === 5}));
  $('#estado-da-execucao').textContent = !x.permitida
    ? 'O hub foi aberto sem --permitir-execucao: copie o comando e rode na sua janela do PowerShell, na pasta experimentos, com o aplicativo Claude fechado.'
    : x.em_andamento ? 'Corrida ' + x.saida + ' em andamento desde ' + quando(x.inicio) + '.'
      : x.terminou ? 'A corrida ' + x.saida + ' terminou em ' + quando(x.fim) + ', com código ' + x.codigo + (x.parada_pelo_hub ? ' (parada pelo hub)' : '') + '.'
        : 'Nenhuma corrida lançada pelo hub desde que ele foi aberto. A corrida chama o modelo e leva cerca de um minuto por cenário e repetição.'
          + (x.pelo_exe ? ' Ela usa o site e a API que o Cobaia.exe já subiu, e não vale como medida do TCC.' : '');
  $('#log-da-execucao').hidden = !x.log;
  $('#log-da-execucao').textContent = x.log;
  if (E.corridaRodando && !x.em_andamento) recarregarIndice();      // a corrida lançada daqui acabou: os casos dela entram na lista
  E.corridaRodando = x.em_andamento;
}

async function mandarExecucao(pedido) {
  try { await api('/api/execucao', pedido); mostrarErro(''); } catch (e) { mostrarErro(e.message); }
  await atualizarAoVivo();
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
  if (nome === 'arvore' && E.caso) desenharRede($('#rede-da-decisao'), E.caso.processo.rede);
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
  // o trecho comentado e a conversa dele se acendem juntos (ideia do realce ligado, do estudo do visual-explainer, decisão 126)
  const acender = (ev, ligado) => {
    const alvo = ev.target.closest ? ev.target.closest('[data-conversa]') : null;
    if (!alvo) return;
    const id = CSS.escape(alvo.dataset.conversa);
    for (const m of $$('mark.trecho-comentado[data-conversa="' + id + '"]')) m.classList.toggle('aceso', ligado);
    for (const c of $$('.conversa[data-conversa="' + id + '"]')) c.classList.toggle('acesa', ligado);
  };
  for (const [evento, ligado] of [['mouseover', true], ['focusin', true], ['mouseout', false], ['focusout', false]]) {
    $('#aba-relatorio').addEventListener(evento, ev => acender(ev, ligado));
  }
  $('#abrir-ao-vivo').addEventListener('click', () => mostrarVista(E.vista === 'ao-vivo' ? 'casos' : 'ao-vivo'));
  $('#abrir-inicio').addEventListener('click', () => mostrarVista('inicio'));
  $('#abrir-metricas').addEventListener('click', () => mostrarVista(E.vista === 'metricas' ? 'casos' : 'metricas'));
  $('#ir-para-metricas').addEventListener('click', () => mostrarVista('metricas'));
  $('#ir-para-rodar').addEventListener('click', () => { mostrarVista('ao-vivo'); $('#execucao').scrollIntoView({block: 'start'}); });
  $('#abrir-legenda').addEventListener('click', () => {
    const legenda = $('#legenda-da-lista');
    legenda.hidden = !legenda.hidden;
    $('#abrir-legenda').setAttribute('aria-expanded', String(!legenda.hidden));
  });
  $('#fechar-zoom').addEventListener('click', fecharZoom);
  $('#zoom-da-etapa').addEventListener('click', ev => { if (ev.target === ev.currentTarget) fecharZoom(); });
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && !$('#zoom-da-etapa').hidden) fecharZoom(); });
  let espera = null;
  window.addEventListener('resize', () => { clearTimeout(espera); espera = setTimeout(redesenharDiagramas, 150); });
  $('#abrir-ultimo').addEventListener('click', () => { if (E.ultimo) abrirCaso(E.ultimo); });
  $('#rodar-cenarios').addEventListener('click', () => mandarExecucao({acao: 'rodar', ...opcoesDaCorrida()}));
  for (const id of ['#selecao-da-corrida', '#desde-da-corrida', '#repeticoes', '#quantas-da-corrida', '#numero-da-corrida']) {     // os dois últimos: coletânea da banca
    $(id).addEventListener('change', async () => { if (id !== '#repeticoes') await atualizarSelecao(); atualizarAoVivo(); });
  }
  $('#parar-corrida').addEventListener('click', () => mandarExecucao({acao: 'parar'}));
  $('#copiar-comando').addEventListener('click', async () => {
    try { await navigator.clipboard.writeText($('#comando-da-corrida').textContent); $('#copiar-comando').textContent = 'Comando copiado'; }
    catch (e) { mostrarErro('Não deu para copiar sozinho: selecione o comando e copie.'); }
  });
  const {tid, aba, vista} = lerEndereco();
  if (tid) await abrirCaso(tid, aba);
  mostrarVista(vista);
}

iniciar();
"""


# ! Alteração de IA - Revisar: (26/11/2026, molde visual do hub, ficha 113) o estilo e o programa dos diagramas (`hub_molde.py`) são juntados ao estilo e
# ao programa da página: o estilo vai no fim, e o programa entra antes da chamada `iniciar()`, que continua sendo a última linha.
# ! Motivo: os diagramas ficaram em arquivo próprio para não se misturarem com a revisão; a página continua servindo um estilo e um programa só,
# em `/hub.css` e `/hub.js`, como a regra de segurança do servidor exige (nada de script nem de estilo embutido na página).
import hub_molde  # depois do programa da página, porque o do molde usa as funções definidas acima e é juntado a ele

CSS += hub_molde.CSS + """
.legenda-do-diagrama .l-alta::before{background:var(--bom);border-color:var(--bom)}
.legenda-do-diagrama .l-media::before{background:var(--meio);border-color:var(--meio)}
.legenda-do-diagrama .l-baixa::before{background:var(--ruim);border-color:var(--ruim)}
svg .barra-do-cenario.com-falha .cheio-do-grafico{fill:var(--ruim)}
"""
JS = JS.replace("\niniciar();\n", "\n" + hub_molde.JS + "\niniciar();\n")
