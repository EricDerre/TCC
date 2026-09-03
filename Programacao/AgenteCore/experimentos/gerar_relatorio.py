#!/usr/bin/env python3
# ! Alteração de IA - Revisar: gera relatorio.html — um arquivo único, sem dependência de
# rede, com a tabela por modelo × condição e as 90 respostas cruas filtráveis por modelo,
# condição, classe, nível e acerto.
# ! Motivo: os gráficos respondem "quanto"; para responder "por quê" é preciso ler o que o
# modelo escreveu em cada caso, lado a lado com o gabarito e com os verbetes que recebeu.
# Isso era feito abrindo o JSONL à mão. O HTML embute os dados (não faz fetch) para abrir
# por duplo clique em qualquer máquina dos integrantes.
import html
import json
import sys
from pathlib import Path

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, igual ao _env_common.py.
# ! Motivo: no Windows o console pode estar em cp1252; os nomes de gráfico e as mensagens
# têm acentos e o script abortava ou imprimia lixo ao exibi-los.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "resultados"

CAMPOS_TABELA = [("modelo", "modelo"), ("condicao", "cond."), ("n", "n"),
                 ("causa_correta_pct", "causa %"), ("causa_correta_ic95", "IC 95%"),
                 ("campo_correto_pct", "campo %"), ("fora_do_conjunto_pct", "fora %"),
                 ("citou_verbete_pct", "citou %"), ("ouro_no_contexto_pct", "ouro %"),
                 ("seguiu_causa_plantada_pct", "seguiu falso %"),
                 ("tokens_entrada_mediana", "tok. entrada"), ("prefill_ms_mediana", "prefill ms"),
                 ("segundos_mediana", "seg")]

_MODELO = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Fase 2-B — respostas</title>
<style>
body{font:14px/1.45 system-ui,sans-serif;margin:0;padding:24px;color:#0b0b0b;background:#fcfcfb}
h1{font-size:20px;margin:0 0 4px}h2{font-size:16px;margin:28px 0 8px}
table{border-collapse:collapse;font-size:12.5px}th,td{border-bottom:1px solid #e5e4e0;padding:4px 8px;text-align:left}
th{color:#52514e;font-weight:600}td.num{text-align:right;font-variant-numeric:tabular-nums}
.filtros{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}.filtros label{font-size:12px;color:#52514e}
select{font:inherit}#lista{display:grid;gap:10px}
.caso{border:1px solid #e5e4e0;border-radius:6px;padding:10px 12px;background:#fff}
.caso header{display:flex;gap:10px;flex-wrap:wrap;font-size:12px;color:#52514e;margin-bottom:6px}
.ok{color:#1baf7a;font-weight:600}.erro{color:#eb6834;font-weight:600}
pre{white-space:pre-wrap;font-size:12px;background:#f5f4f1;padding:8px;border-radius:4px;margin:6px 0 0}
details summary{cursor:pointer;font-size:12px;color:#52514e}
</style></head><body>
<h1>Fase 2-B — resultados por modelo e condição</h1>
<p style="color:#52514e;margin:0">Gerado por gerar_relatorio.py a partir de avaliacao.json e dos JSONL em resultados/. Nenhum número digitado à mão.</p>
<h2>Resumo (braço linear)</h2>
__TABELA__
<h2>Respostas caso a caso</h2>
<div class="filtros">
<label>modelo <select id="f-modelo"><option value="">todos</option></select></label>
<label>condição <select id="f-condicao"><option value="">todas</option></select></label>
<label>classe <select id="f-classe"><option value="">todas</option></select></label>
<label>nível <select id="f-nivel"><option value="">todos</option></select></label>
<label>acerto <select id="f-acerto"><option value="">todos</option><option value="1">só acertos</option><option value="0">só erros</option></select></label>
<span id="contagem" style="font-size:12px;color:#52514e"></span>
</div>
<div id="lista"></div>
<script>
var DADOS = __DADOS__;
var CLASSES = {1:"Léxica",2:"Sintática",3:"Semântica",4:"Tradução",5:"Runtime",6:"Efeito"};
function opcoes(id, valores){var s=document.getElementById(id);valores.forEach(function(v){var o=document.createElement("option");o.value=v;o.textContent=v;s.appendChild(o);});}
function unicos(campo){return Array.from(new Set(DADOS.map(function(d){return d[campo];}))).sort();}
opcoes("f-modelo", unicos("modelo")); opcoes("f-condicao", unicos("condicao")); opcoes("f-classe", unicos("classe")); opcoes("f-nivel", unicos("nivel"));
function esc(s){return String(s==null?"":s).replace(/[&<>]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;"}[c];});}
function render(){
  var f = {modelo:document.getElementById("f-modelo").value, condicao:document.getElementById("f-condicao").value,
           classe:document.getElementById("f-classe").value, nivel:document.getElementById("f-nivel").value,
           acerto:document.getElementById("f-acerto").value};
  var sel = DADOS.filter(function(d){
    return (!f.modelo||d.modelo===f.modelo)&&(!f.condicao||d.condicao===f.condicao)&&(!f.classe||String(d.classe)===f.classe)
        &&(!f.nivel||String(d.nivel)===f.nivel)&&(!f.acerto||String(d.causa_correta?1:0)===f.acerto);
  });
  document.getElementById("contagem").textContent = sel.length + " de " + DADOS.length + " registros";
  document.getElementById("lista").innerHTML = sel.slice(0,400).map(function(d){
    return '<div class="caso"><header><b>'+esc(d.caso)+'</b><span>'+esc(d.modelo)+'</span><span>'+esc(d.condicao)+' / '+esc(d.estrategia)+'</span>'
      +'<span>'+CLASSES[d.classe]+' · nível '+d.nivel+'</span><span class="'+(d.causa_correta?"ok":"erro")+'">'+(d.causa_correta?"acertou":"errou")+'</span>'
      +'<span>esperado: <code>'+esc(d.causa_esperada)+'</code> · respondeu: <code>'+esc(d.causa_respondida)+'</code></span>'
      +(d.causa_plantada?'<span>plantada: <code>'+esc(d.causa_plantada)+'</code>'+(d.seguiu_causa_plantada?' <b class="erro">seguiu</b>':'')+'</span>':'')
      +'<span>'+(d.segundos==null?"—":d.segundos+" s")+(d.prefill_ms?" · prefill "+d.prefill_ms+" ms":"")+'</span></header>'
      +(d.verbetes_ids&&d.verbetes_ids.length?'<div style="font-size:12px;color:#52514e">verbetes: '+esc(d.verbetes_ids.join(", "))+(d.verbete_ouro?' · ouro: '+esc(d.verbete_ouro):'')+'</div>':'')
      +'<pre>'+esc(d.resposta)+'</pre>'
      +'<details><summary>sintoma do caso</summary><pre>'+esc(d.sintoma)+'</pre></details></div>';
  }).join("") + (sel.length>400?'<p style="color:#52514e">mostrando os 400 primeiros — refine os filtros</p>':'');
}
["f-modelo","f-condicao","f-classe","f-nivel","f-acerto"].forEach(function(id){document.getElementById(id).addEventListener("change",render);});
render();
</script></body></html>
"""


def _tabela(resumo: dict) -> str:
    linhas = resumo.get("por_modelo_condicao", [])
    cab = "".join(f"<th>{html.escape(r)}</th>" for _, r in CAMPOS_TABELA)
    corpo = []
    for r in sorted(linhas, key=lambda r: (r["modelo"], r["condicao"])):
        celulas = []
        for campo, _ in CAMPOS_TABELA:
            v = r.get(campo)
            if isinstance(v, list):
                v = f"{v[0]}–{v[1]}"
            celulas.append(f'<td class="num">{html.escape(str(v if v is not None else "—"))}</td>')
        corpo.append("<tr>" + "".join(celulas) + "</tr>")
    return f"<table><thead><tr>{cab}</tr></thead><tbody>{''.join(corpo)}</tbody></table>"


def main() -> None:
    avaliacao = json.loads((AQUI / "avaliacao.json").read_text(encoding="utf-8"))
    resumo = json.loads((AQUI / "resumo_metricas.json").read_text(encoding="utf-8"))

    # As respostas cruas e o sintoma ficam só no JSONL; junta pela chave do registro.
    brutos = {}
    for arq in sorted(SAIDA.glob("*.jsonl")):
        with open(arq, encoding="utf-8") as f:
            for linha in f:
                try:
                    r = json.loads(linha)
                except json.JSONDecodeError:
                    continue
                brutos[(r["modelo"], r.get("condicao", "A0"), r["estrategia"], r["caso"])] = r
    from banco_casos import CASOS
    from banco_casos_extra import CASOS_EXTRA
    sintomas = {c["id"]: c["entrada"].get("sintoma", "") for c in CASOS + CASOS_EXTRA}

    dados = []
    for a in avaliacao:
        b = brutos.get((a["modelo"], a["condicao"], a["estrategia"], a["caso"]), {})
        dados.append({**a, "resposta": b.get("resposta", ""),
                      "verbetes_ids": b.get("verbetes_ids", []),
                      "verbete_ouro": b.get("verbete_ouro"),
                      "sintoma": sintomas.get(a["caso"], "")})

    pagina = (_MODELO.replace("__TABELA__", _tabela(resumo))
              .replace("__DADOS__", json.dumps(dados, ensure_ascii=False)))
    destino = AQUI / "relatorio.html"
    destino.write_text(pagina, encoding="utf-8")
    print(f"{destino} ({len(dados)} registros, {round(destino.stat().st_size / 1024)} KB)")


if __name__ == "__main__":
    main()
