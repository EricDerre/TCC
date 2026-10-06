#!/usr/bin/env python3
# ! Alteração de IA - Revisar: módulo novo (01/10/2026, Pré-Fase 4) com o explorador de casos da aba "Raciocínio aberto"
# do painel: de cada trilha versionada sai um recorte por caso, e a página mostra, para o caso escolhido, as três
# camadas em cartões separados (o que o programa fez, o que o modelo declarou, o que o código conferiu) e, num bloco à
# parte e recolhido, a avaliação contra o gabarito.
# ! Motivo: o Eric pediu (01/10/2026) que o analista tenha "acesso claro à linha de raciocínio da IA", com um relatório
# para humanos gerado do arquivo bruto. Os relatórios por caso existem como arquivos .md (108 na vitrine), mas é pelo
# painel que ele lê; antes a aba só mostrava um relatório de exemplo. O explorador não copia os relatórios inteiros
# (o painel cresceria mais de 1 MB): leva de cada caso só os dados das três camadas, lidos da trilha. A resposta certa
# aparece num lugar só, como no relatório. Fica num arquivo à parte porque painel_topicos.py já é grande.
"""Explorador de casos da aba "Raciocínio aberto". Uso: importado por painel_topicos.py."""
from __future__ import annotations

import html

CANDIDATOS_MOSTRADOS = 5


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def _texto_do_alvo(alvo) -> str:
    if alvo is None:
        return ""
    return ", ".join(str(x) for x in alvo) if isinstance(alvo, list) else str(alvo)


def casos_da_trilha(eventos: list[dict]) -> list[dict]:
    """De uma trilha (lista de eventos), o recorte de cada diagnóstico para o explorador."""
    blobs = {e["dados"]["sha"]: e["dados"]["texto"] for e in eventos if e["tipo"] == "blob"}
    por_trilha: dict[str, list[dict]] = {}
    for e in eventos:
        if e["trilha"] is not None and "@" in e["trilha"]:
            por_trilha.setdefault(e["trilha"], []).append(e)
    casos = []
    for tid, seq in por_trilha.items():
        def um(tipo: str, **filtro) -> dict | None:
            return next((e["dados"] for e in seq if e["tipo"] == tipo and all(e["dados"].get(k) == v for k, v in filtro.items())), None)

        entrada, cand = um("entrada"), um("candidatos")
        prompt, inf = um("prompt", etapa="diagnostico"), um("inferencia", etapa="diagnostico")
        decl = {e["dados"]["campo"]: e["dados"] for e in seq if e["tipo"] == "declaracao" and e["dados"]["campo"] not in ("fonte_citada", "proposta")}
        fontes = [e["dados"]["valor"] for e in seq if e["tipo"] == "declaracao" and e["dados"]["campo"] == "fonte_citada"]
        ver = [e["dados"] for e in seq if e["tipo"] == "verificacao" and e["dados"]["regra"] not in ("validador_da_biblioteca", "revisao_humana_da_edicao")]
        avaliacao = [{"regra": v["regra"], "alvo": _texto_do_alvo(v["alvo"]), "resultado": v["resultado"],
                      "gabarito": (v.get("evidencia") or {}).get("gabarito") if isinstance(v.get("evidencia"), dict) else None}
                     for v in ver if v.get("usa_gabarito")]
        propostas = []
        for e in seq:
            if e["tipo"] == "declaracao" and e["dados"]["campo"] == "proposta":
                d = e["dados"]
                validador = next((x["dados"] for x in seq if x["tipo"] == "verificacao" and x["pai"] == e["seq"] and x["dados"]["regra"] == "validador_da_biblioteca"), None)
                acao = next((x for x in seq if x["tipo"] == "acao" and x["pai"] == e["seq"]), None)
                humano = next((x["dados"]["resultado"] for x in seq if acao and x["tipo"] == "verificacao" and x["pai"] == acao["seq"]
                               and x["dados"]["regra"] == "revisao_humana_da_edicao"), None)
                propostas.append({"operacao": d.get("operacao"), "verbete": d.get("verbete"), "resultado": validador["resultado"] if validador else None,
                                  "codigo": (validador.get("evidencia") or {}).get("codigo") if validador else None, "humano": humano})
        itens = cand["itens"] if cand else []
        caso = {
            "trilha": tid, "caso": entrada["caso"], "classe": entrada["classe"], "nivel": entrada["nivel"],
            "ok": next((v["resultado"] == "confere" for v in ver if v["regra"] == "causa_correta"), False),
            "programa": {"candidatos": [{"id": x["id"], "pos": x["posicao"], "pontos": x["pontuacao"], "bm25": x["bm25"],
                                         "reforcos": round(x["reforco_endpoint"] + x["reforco_entidade"] + x["reforco_status"], 2), "entregue": x["escolhido"]}
                                        for x in itens[:max(CANDIDATOS_MOSTRADOS, sum(1 for x in itens if x["escolhido"]))]],
                         "pontuados": len(itens), "prompt_chars": prompt["chars"], "prova": prompt["nivel"],
                         "tokens_entrada": inf.get("tokens_entrada"), "tokens_saida": inf.get("tokens_saida"), "segundos": inf.get("segundos"),
                         "resposta": blobs.get(inf["resposta"], "")},
            "modelo": {"raciocinio": (decl.get("raciocinio") or {}).get("valor") or "", "causa": (decl.get("causa_raiz") or {}).get("lido"),
                       "campo": (decl.get("campo") or {}).get("lido"), "impacto": (decl.get("impacto") or {}).get("lido"), "fontes": fontes},
            "conferencias": [{"regra": v["regra"], "alvo": _texto_do_alvo(v["alvo"]), "resultado": v["resultado"]} for v in ver if not v.get("usa_gabarito")],
            "avaliacao": avaliacao,
        }
        if propostas:
            caso["propostas"] = propostas
        casos.append(caso)
    return casos


def dados_do_explorador(trilhas: dict[str, list[dict]] | None, nomes: dict[str, str], rotulos: dict[str, str], classes: dict[int, str],
                        padrao: tuple[str, str] | None = None) -> dict:
    """`trilhas`: {nome do arquivo sem extensão: eventos}; `nomes`: o nome legível de cada trilha; `padrao`: o arquivo
    e o caso que abrem escolhidos."""
    saida = []
    for arquivo in sorted(trilhas or {}):
        saida.append({"arquivo": arquivo, "nome": nomes.get(arquivo, arquivo), "casos": casos_da_trilha(trilhas[arquivo])})
    indice = next((k for k, t in enumerate(saida) if padrao and t["arquivo"] == padrao[0]), 0)
    return {"trilhas": saida, "rotulos": rotulos, "classes": {str(k): v for k, v in classes.items()},
            "padrao": {"trilha": indice, "caso": padrao[1] if padrao else None}}


def bloco_html(dados: dict) -> str:
    if not dados["trilhas"]:
        return ""
    total = sum(len(t["casos"]) for t in dados["trilhas"])
    opcoes = "".join(f'<option value="{k}"{" selected" if k == dados["padrao"]["trilha"] else ""}>{esc(t["nome"])} ({len(t["casos"])} casos)</option>'
                     for k, t in enumerate(dados["trilhas"]))
    return f'''<h2>Explorar um caso</h2>
<p>Os {total} diagnósticos das trilhas versionadas, um por vez. Cada cartão é uma camada: o que o programa fez é fato, o que o modelo declarou é alegação, e o que o código conferiu é a checagem da alegação sem saber a resposta certa. A resposta certa fica num bloco à parte, fechado.</p>
<div class="ra-explorador">
<div class="ra-controles"><label>Corrida <select class="ra-sel-trilha">{opcoes}</select></label><label>Caso <select class="ra-sel-caso"></select></label></div>
<div class="ra-camadas"><p class="nota">Escolha a corrida e o caso. Sem o script da página, os mesmos dados estão nos relatórios por caso em <code>resultados_alvo/pre_fase4/relatorios/</code>.</p></div>
</div>'''


CSS_EXPLORADOR = r"""
.ra-controles{display:flex;flex-wrap:wrap;gap:10px 18px;font-size:13px;color:var(--ink2);margin:10px 0}.ra-controles select{max-width:100%;margin-left:4px}
.ra-camadas{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(330px,100%),1fr));gap:14px;align-items:start}
.ra-camada{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:14px 16px;min-width:0}
.ra-camada h4{margin:0 0 4px}.ra-camada > p{margin:4px 0 8px;font-size:13px}
.ra-camada dl{display:grid;grid-template-columns:minmax(90px,auto) minmax(0,1fr);gap:4px 12px;margin:8px 0;font-size:13px}.ra-camada dt{color:var(--ink2)}.ra-camada dd{margin:0;overflow-wrap:anywhere}
.ra-camada .tabela{margin:8px 0}.ra-camada table{font-size:12px}.ra-camada td,.ra-camada th{padding:4px 7px}
.ra-camada ul{list-style:none;padding:0;margin:6px 0;font-size:13px}.ra-camada li{margin:7px 0;display:flex;flex-wrap:wrap;gap:3px 8px;align-items:baseline}
.ra-camada li span.alvo{font-family:var(--fm);font-size:12px;color:var(--ink2);overflow-wrap:anywhere}
.ra-camada details{margin:8px 0 0}.ra-camada td.verbete{overflow-wrap:anywhere}.ra-camada td.verbete small{color:var(--ink2)}
.ra-gabarito{grid-column:1/-1;margin:0}.ra-gabarito ul{list-style:none;padding:0;margin:8px 0;font-size:13px}.ra-gabarito li{margin:7px 0;display:flex;flex-wrap:wrap;gap:3px 8px;align-items:baseline}
.ra-gabarito span.alvo{font-family:var(--fm);font-size:12px;color:var(--ink2);overflow-wrap:anywhere}
"""

JS_EXPLORADOR = r"""
function raExplorar(){
  const E = (T.raciocinio || {}).explorador, raiz = document.querySelector('#raciocinio .ra-explorador');
  if(!E || !E.trilhas || !E.trilhas.length || !raiz || raiz.dataset.pronto) return; raiz.dataset.pronto = '1';
  const selT = raiz.querySelector('.ra-sel-trilha'), selC = raiz.querySelector('.ra-sel-caso'), alvo = raiz.querySelector('.ra-camadas');
  const el = (tag, attrs, texto) => { const e = document.createElement(tag); Object.entries(attrs || {}).forEach(([k, v]) => e.setAttribute(k, v)); if(texto != null) e.textContent = texto; return e; };
  const br = (v, c) => v == null ? 'n/d' : Number(v).toLocaleString('pt-BR', {minimumFractionDigits: c == null ? 1 : c, maximumFractionDigits: c == null ? 1 : c});
  const nomeResultado = {confere: 'confere', nao_confere: 'não confere', nao_se_aplica: 'não se aplica', nao_verificavel: 'não dá para conferir por código', informativo: 'informativo', aceita: 'aceita', rejeitada: 'rejeitada'};
  const classeResultado = {confere: 'adotado', nao_confere: 'descartado', aceita: 'adotado', rejeitada: 'descartado'};
  const chip = r => el('span', {class: 'chip ' + (classeResultado[r] || 'pendente')}, nomeResultado[r] || r);
  const prova = {prompt_inteiro: 'o prompt inteiro está provado', contexto: 'só a documentação entregue tem prova gravada', nao_comprovado: 'não comprovado'};
  const dl = pares => { const d = el('dl'); pares.forEach(([k, v]) => { d.append(el('dt', {}, k), el('dd', {}, v)); }); return d; };
  const cartao = (titulo, sub, larga) => { const c = el('div', {class: 'ra-camada' + (larga ? ' larga' : '')}); c.append(el('h4', {}, titulo)); if(sub) c.append(el('p', {class: 'nota'}, sub)); return c; };

  function doPrograma(c){
    const p = c.programa, k = cartao('1 · O que o programa fez', 'Fato: gravado na corrida ou refeito agora a partir dos mesmos insumos.');
    k.append(el('p', {}, `Caso ${c.caso}, classe ${E.classes[c.classe] || c.classe}, nível ${c.nivel}. A busca pontuou ${p.pontuados} verbetes e entregou ${p.candidatos.filter(x => x.entregue).length}.`));
    const caixa = el('div', {class: 'tabela'}), tab = el('table'), cab = el('tr');
    ['#', 'Verbete', 'Pontos', 'BM25 + reforços'].forEach(h => cab.append(el('th', {}, h)));
    const corpo = el('tbody');
    p.candidatos.forEach(x => { const tr = el('tr'), nome = el('td', {class: 'verbete'});
      nome.append(el(x.entregue ? 'strong' : 'span', {}, x.id)); if(x.entregue) nome.append(el('small', {}, ' entregue'));
      tr.append(el('td', {class: 'num'}, String(x.pos)), nome, el('td', {class: 'num'}, br(x.pontos, 2)), el('td', {class: 'num'}, br(x.bm25, 2) + ' + ' + br(x.reforcos, 1))); corpo.append(tr); });
    const thead = el('thead'); thead.append(cab); tab.append(thead, corpo); caixa.append(tab); k.append(caixa);
    k.append(dl([['Prompt', br(p.prompt_chars, 0) + ' caracteres; ' + (prova[p.prova] || p.prova)], ['Entrada e saída', br(p.tokens_entrada, 0) + ' e ' + br(p.tokens_saida, 0) + ' tokens'], ['Tempo', br(p.segundos) + ' s']]));
    const d = el('details'); d.append(el('summary', {}, 'Resposta crua do modelo')); const pre = el('pre', {class: 'bruto'}); pre.append(el('code', {}, p.resposta)); d.append(pre); k.append(d);
    return k;
  }
  function doModelo(c){
    const m = c.modelo, k = cartao('2 · O que o modelo declarou', 'Alegação: sempre um trecho literal da resposta.');
    k.append(dl([['Raciocínio antes das linhas', m.raciocinio || 'nenhum: o modelo foi direto às quatro linhas'], ['Causa', m.causa || 'sem a linha CAUSA_RAIZ'], ['Campo', m.campo || 'sem a linha CAMPO'],
      ['Impacto', m.impacto || 'sem a linha IMPACTO'], ['Verbetes citados', m.fontes.length ? m.fontes.join(', ') : 'nenhum']]));
    return k;
  }
  function lista(itens, comGabarito){
    const ul = el('ul');
    itens.forEach(x => { const li = el('li'); li.append(el('span', {}, E.rotulos[x.regra] || x.regra.replace(/_/g, ' ')));
      if(x.alvo) li.append(el('span', {class: 'alvo'}, x.alvo)); li.append(chip(x.resultado));
      if(comGabarito && x.gabarito != null) li.append(el('span', {class: 'alvo'}, 'gabarito: ' + x.gabarito)); ul.append(li); });
    return ul;
  }
  function doCodigo(c){ const k = cartao('3 · O que o código conferiu', 'Sem usar a resposta certa: é o que o agente pode checar sozinho.'); k.append(lista(c.conferencias, false)); return k; }
  function doGabarito(c){
    const d = el('details', {class: 'ra-gabarito'}), k = d;
    d.append(el('summary', {}, 'Avaliação contra o gabarito (a resposta certa aparece só aqui)')); d.append(lista(c.avaliacao, true));
    if(c.propostas && c.propostas.length){ d.append(el('h4', {}, 'Proposta de edição da biblioteca (caso de aprendizado)')); const ul = el('ul');
      c.propostas.forEach(x => { const li = el('li'); li.append(el('span', {}, (x.operacao || 'proposta') + ' em'), el('span', {class: 'alvo'}, x.verbete || 'verbete não informado'));
        if(x.resultado) li.append(chip(x.resultado)); if(x.codigo) li.append(el('span', {class: 'alvo'}, 'motivo do validador: ' + x.codigo));
        if(x.humano) li.append(el('span', {class: 'alvo'}, 'revisão humana: ' + x.humano)); ul.append(li); }); d.append(ul); }
    return k;
  }
  function casos(){
    const t = E.trilhas[Number(selT.value)]; selC.replaceChildren();
    [['errados', c => !c.ok], ['certos', c => c.ok]].forEach(([nome, f]) => { const itens = t.casos.filter(f); if(!itens.length) return;
      const g = el('optgroup', {label: `${nome} (${itens.length})`}); itens.forEach(c => g.append(el('option', {value: c.caso}, c.caso))); selC.append(g); });
  }
  function mostrar(){
    const t = E.trilhas[Number(selT.value)], c = t.casos.find(x => x.caso === selC.value) || t.casos[0]; if(!c) return;
    alvo.replaceChildren(doPrograma(c), doModelo(c), doCodigo(c), doGabarito(c));
  }
  selT.addEventListener('change', () => { casos(); mostrar(); });
  selC.addEventListener('change', mostrar);
  selT.value = String(E.padrao.trilha); casos();
  if(E.padrao.caso && E.trilhas[E.padrao.trilha].casos.some(c => c.caso === E.padrao.caso)) selC.value = E.padrao.caso;
  mostrar();
}
"""
