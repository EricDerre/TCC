#!/usr/bin/env python3
# ! Alteração de IA - Revisar: novo (05/11/2026): gera a página da sessão de revisão dos relatórios da trilha (corrida 22, Fase 4) a partir só da
# planilha revisao_trilha.md e dos relatórios dela, e passa as respostas da página para as células do revisor na planilha.
# ! Motivo: preencher a planilha à mão pedia cronômetro externo e abrir arquivo por arquivo; a página mostra um relatório por vez, mede o tempo até a
# decisão só com o relatório à vista e guarda cada resposta na hora. A planilha continua sendo o registro oficial que avaliar_fase4.py lê, e este
# gerador nunca abre trilha.json nem trilha.md, porque a adesão apropriada só vale sem o resultado de cada caso.
"""Sessão de revisão dos relatórios da trilha.

Uso:
  python ferramentas/sessao_revisao.py                          gera Documentacao/dashboard/sessao-revisao-trilha.html
  python ferramentas/sessao_revisao.py --gravar respostas.json  grava na planilha as respostas lidas do banco da página
  python ferramentas/sessao_revisao.py --gravar respostas.json --corrigir   idem, trocando linhas já preenchidas
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import painel_textos as pt  # noqa: E402
import painel_topicos as tp  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
PLANILHA = RAIZ / "Programacao" / "AgenteCore" / "experimentos" / "resultados_alvo" / "fase4" / "revisao_trilha.md"
SAIDA = RAIZ / "Documentacao" / "dashboard" / "sessao-revisao-trilha.html"
# a mesma marca de biblioteca_fase4.CELULA_EM_BRANCO, que gerar_dashboard.py procura para saber se a planilha está preenchida
EM_BRANCO = "(em branco)"
# ! Alteração de IA - Revisar: (05/11/2026, decisão 86) o parecer do Claude aprovado pelo Eric entra na planilha sem tempo, com esta marca no lugar dos segundos, e a origem diz quem decidiu.
# ! Motivo: o Eric aprovou o parecer para os relatórios 2 a 11 sem responder na página; o tempo não existe e não pode virar número, e a marca é o que permite à leitura não somar isso como revisão humana.
TEMPO_NAO_MEDIDO = "não medido"
ORIGEM_PARECER = "parecer_aprovado"
RE_LINHA = re.compile(r"^\| \d+ \|")
# Os nomes dos campos com a resposta certa na trilha e as frases que diriam o resultado: se um relatório os trouxer, a sessão deixa de ser às cegas.
# "esperado" sozinho não entra: os relatórios falam do contrato esperado pela tela e da causa nulo_inesperado, que são texto do próprio caso.
RE_RESULTADO = re.compile(r"causa_correta|campo_correto|verbete_de_ouro|causa[ _]esperada|r[oó]tulo[ _]esperado|\bacertou\b|\berrou\b", re.I)
# ! Alteração de IA - Revisar: (05/11/2026) a página mostra relatorio-N no lugar do nome do caso, em todo lugar, e tira o comando de reexecução, que traz o nome real.
# ! Motivo: conferido no banco de casos, o prefixo do nome diz a família do defeito e reduz as 23 causas possíveis a 3 a 6 (num prefixo, uma causa só responde por 58%); um analista de
# verdade não teria esse nome, e o revisor julgaria com uma pista a mais. A coluna Classe da planilha fica de fora pelo mesmo motivo. O revisor separado que leu os 11 relatórios apontou isso.
RE_NOME_DE_CASO = re.compile(r"(?<![\w-])(?:efe|lex|run|semt|sin|tra)-\d+(?![\w-])")
RE_COMANDO = re.compile(r"^Comando para reexecutar o caso: .*$", re.M)
VALORES = {"erro_localizado": ("sim", "não", "n.a."), "decisao": ("aceitar", "recusar"), "avaliacao": ("certo", "errado")}

CSS = """
/* Layout: coluna larga para ler e ficha estreita que acompanha a rolagem; no celular a ficha vira barra presa embaixo e, depois da decisão, sobe para antes do relatório. */
:root{--bg:#f6f4ee;--bg2:#fdfcf9;--ink:#1f2328;--ink2:#4c545c;--linha:#d8d3c7;--acento:#2f5d8a;--acento2:#dbe7f3;--bom:#2e7d4f;--ruim:#b3392b;--sombra:0 -4px 18px rgba(20,25,30,.12);
--fd:"Source Serif 4",Georgia,"Times New Roman",serif;--fb:"IBM Plex Sans","Segoe UI",Roboto,Arial,sans-serif;--fm:"IBM Plex Mono",Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){color-scheme:dark;--bg:#15181c;--bg2:#1d2126;--ink:#e8e6df;--ink2:#a8adb4;--linha:#333a42;--acento:#7fb0e0;--acento2:#243342;--bom:#5cc48a;--ruim:#e46b5c;--sombra:0 -4px 18px rgba(0,0,0,.45)}}
:root[data-theme=dark]{color-scheme:dark;--bg:#15181c;--bg2:#1d2126;--ink:#e8e6df;--ink2:#a8adb4;--linha:#333a42;--acento:#7fb0e0;--acento2:#243342;--bom:#5cc48a;--ruim:#e46b5c;--sombra:0 -4px 18px rgba(0,0,0,.45)}
[hidden]{display:none!important}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font:15px/1.55 var(--fb);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:18px 28px}
.topo,.aviso,.palco{max-width:80rem;margin-inline:auto}
.olho{margin:0;font:500 .72rem/1.3 var(--fm);letter-spacing:.06em;text-transform:uppercase;color:var(--ink2)}
h1{margin:.2rem 0 0;font:600 1.55rem/1.2 var(--fd);text-wrap:balance}
h2{margin:0 0 .4rem;font:600 1.3rem/1.25 var(--fd);text-wrap:balance}
code{font:.87em var(--fm);background:var(--acento2);padding:1px 4px;border-radius:4px;overflow-wrap:anywhere}
:focus-visible{outline:2px solid var(--acento);outline-offset:2px}
button{font:inherit;color:inherit}
.trilho{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;margin:.7rem 0 1.1rem}
.trilho ol{display:flex;flex-wrap:wrap;gap:5px;list-style:none;margin:0;padding:0}
.pip{width:30px;height:30px;padding:0;border-radius:50%;border:1px solid var(--linha);background:transparent;color:var(--ink2);font:500 .8rem var(--fm);font-variant-numeric:tabular-nums}
.pip:disabled{color:var(--ink2);opacity:1}
.pip.salvo{background:var(--acento2);border-color:var(--acento);color:var(--ink)}
.pip.salvo:not(:disabled){cursor:pointer}
.pip.atual{border:2px solid var(--acento);color:var(--acento);font-weight:600}
.contagem{font-size:.85rem;color:var(--ink2);font-variant-numeric:tabular-nums}
.aviso{margin-bottom:1rem;padding:9px 13px;border:1px solid var(--ruim);border-radius:8px;background:var(--bg2);font-size:.92rem}
.palco{display:flex;flex-direction:column;gap:14px}
.bloco{max-width:46rem}
.abertura{margin:0 0 .8rem;font-size:1.05rem}
.passos{margin:0 0 1rem;padding-left:1.3rem}
.passos li{margin:.45rem 0;max-width:68ch}
.cegas{margin:0 0 1.1rem;padding:10px 14px;border:1px solid var(--linha);border-radius:8px;background:var(--bg2);max-width:68ch}
.nota{margin:.5rem 0 0;font-size:.85rem;color:var(--ink2)}
.primario{padding:10px 18px;border:0;border-radius:8px;background:var(--acento);color:var(--bg2);font-weight:600;cursor:pointer}
.secundario{padding:7px 13px;border:1px solid var(--acento);border-radius:8px;background:transparent;color:var(--acento);font-weight:500;cursor:pointer}
.discreto{padding:2px 0;border:0;background:none;color:var(--acento);text-decoration:underline;cursor:pointer}
.relatorio{min-width:0;width:100%}
.relatorio h3{margin:0 0 .6rem;font:600 1.3rem/1.25 var(--fd);text-wrap:balance}
.relatorio h4{margin:1.5rem 0 .5rem;padding-top:.8rem;border-top:1px solid var(--linha);font-size:1.02rem;font-weight:600}
.relatorio h5{margin:1.1rem 0 .3rem;font-size:.92rem;font-weight:600;color:var(--ink2)}
.relatorio p,.relatorio ul{max-width:74ch}
.relatorio li{margin:.3rem 0}
.tabela{overflow-x:auto;margin:10px 0;border:1px solid var(--linha);border-radius:8px;background:var(--bg2)}
table{border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums}
th,td{padding:6px 10px;border-bottom:1px solid var(--linha);text-align:left;vertical-align:top}
th{background:var(--acento2);font-weight:600;white-space:nowrap}
tbody tr:last-child td{border-bottom:0}
pre.bruto{margin:.6rem 0;padding:10px 12px;border:1px solid var(--linha);border-radius:8px;background:var(--bg2);overflow-x:auto}
pre.bruto code{padding:0;background:none;font-size:12.5px;white-space:pre-wrap;overflow-wrap:anywhere}
details{margin:10px 0;padding:8px 12px;border:1px solid var(--linha);border-radius:8px;background:var(--bg2)}
summary{cursor:pointer;font-weight:600}
.painel{min-width:0;padding:12px 14px;border:1px solid var(--linha);border-radius:10px;background:var(--bg2)}
.painel-topo{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px;margin-bottom:.6rem}
.relogio{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:0 0 .5rem;font-size:.88rem;color:var(--ink2)}
.luz{width:8px;height:8px;border-radius:50%;background:var(--bom);display:inline-block}
.pergunta{margin:.2rem 0 .5rem}
.decisoes{display:flex;gap:8px}
.decisao{flex:1;padding:11px 8px;border:1.5px solid var(--acento);border-radius:8px;background:transparent;color:var(--acento);font-weight:600;cursor:pointer}
.decisao:hover{background:var(--acento2)}
.tempo{margin:0 0 .5rem;font-variant-numeric:tabular-nums}
fieldset{margin:0 0 .75rem;padding:0;border:0;min-width:0}
legend{padding:0;margin-bottom:.3rem;font-size:.92rem;font-weight:600}
.opcoes{display:flex;flex-wrap:wrap;gap:5px}
.opcao{position:relative}
.opcao input{position:absolute;width:1px;height:1px;opacity:0}
.opcao label{display:inline-block;min-width:2.3rem;padding:6px 11px;border:1px solid var(--linha);border-radius:8px;background:var(--bg);text-align:center;cursor:pointer}
.opcao input:checked+label{border-color:var(--acento);background:var(--acento);color:var(--bg2)}
.opcao input:focus-visible+label{outline:2px solid var(--acento);outline-offset:2px}
.dica{margin:.25rem 0 0;font-size:.8rem;color:var(--ink2)}
textarea{display:block;width:100%;padding:7px 9px;border:1px solid var(--linha);border-radius:8px;background:var(--bg);color:var(--ink);font:.92rem/1.45 var(--fb);resize:vertical}
label.campo{display:block;margin-bottom:.3rem;font-size:.92rem;font-weight:600}
.acoes{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;margin-top:.8rem}
.mensagem{margin:.5rem 0 0;font-size:.88rem;color:var(--ruim)}
.mensagem:empty{display:none}
.so-leitor{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
@media (min-width:980px){
  .palco[data-fase=lendo],.palco[data-fase=decidido]{display:grid;grid-template-columns:minmax(0,1fr) 20rem;gap:32px;align-items:start}
  .painel{position:sticky;top:calc(env(safe-area-inset-top,0px) + 12px);max-height:calc(100vh - 24px);overflow:auto}
}
@media (max-width:979.98px){
  .so-largo{display:none!important}
  .painel{position:sticky;bottom:env(safe-area-inset-bottom,0px);z-index:5;box-shadow:var(--sombra)}
  .palco[data-fase=decidido] .painel{position:static;order:-1;box-shadow:none}
}
"""

# ! Alteração de IA - Revisar: (05/11/2026) a pergunta sobre o erro ganhou uma dica, e o cabeçalho e o aviso deixaram de dizer "às cegas".
# ! Motivo: na primeira resposta real, o revisor aceitou o diagnóstico, avaliou como certo e marcou que achou o erro, o que sugere ter lido "erro" como o defeito do sistema; e, a partir do relatório 2, ele lê a pré-análise do Claude antes de decidir (decisão 85), embora o resultado de cada caso continue fechado.
CORPO = """
<header class="topo">
  <p class="olho">Fase 4, corrida 22, sessão de revisão</p>
  <h1>Revisão dos relatórios da trilha</h1>
  <nav class="trilho" aria-label="Relatórios da sessão">
    <ol id="trilho-lista">@@PIPS@@</ol>
    <span id="contagem" class="contagem">0 de @@TOTAL@@ respondidos</span>
  </nav>
</header>
<div id="aviso" class="aviso" role="status" hidden><span id="aviso-texto"></span> <button type="button" id="tentar" class="discreto" hidden>Tentar de novo</button></div>
<main id="palco" class="palco" data-fase="inicio">
  <section id="inicio" class="bloco">
    <p class="abertura">São @@TOTAL@@ relatórios de diagnóstico, um por vez, na ordem sorteada. Em cada um você decide se aceita ou recusa o diagnóstico do agente. Reserve cerca de 1 hora; dá para parar entre um relatório e outro.</p>
    <ol class="passos">
      <li><strong>Abra o relatório.</strong> O cronômetro liga nesse clique e só conta com a página à vista. A tela não mostra a contagem, para não apressar a leitura. Se precisar interromper, use Pausar: o relatório some e o tempo para.</li>
      <li><strong>Decida.</strong> O diagnóstico é a causa na seção 1, Veredito. Aceitar ou Recusar para o cronômetro.</li>
      <li><strong>Complete a ficha.</strong> Diga se achou no relatório onde está o erro do agente, a utilidade do relatório de 1 a 5, a sua avaliação do diagnóstico e, se quiser, um comentário.</li>
      <li><strong>Salve.</strong> A resposta fica guardada nesta página, e o Claude lê daqui quando você terminar.</li>
    </ol>
    <p class="cegas"><strong>Sem ver o resultado.</strong> Até terminar, não abra a planilha <code>revisao_trilha.md</code> nem os arquivos <code>trilha.md</code> e <code>trilha.json</code>: eles trazem o nome, a família ou o resultado de cada caso. Por isso os relatórios aparecem aqui com um nome neutro.</p>
    <button type="button" id="comecar" class="primario">Começar pelo relatório 1</button>
  </section>
  <section id="antes" class="bloco" hidden>
    <h2 id="antes-titulo"></h2>
    <p>O cronômetro liga quando você abrir o relatório.</p>
    <button type="button" id="abrir" class="primario">Abrir o relatório</button>
    <p class="nota">Pode parar aqui. O que está respondido continua guardado.</p>
  </section>
  <section id="pausado" class="bloco" hidden>
    <h2>Leitura pausada</h2>
    <p><span id="pausado-titulo"></span>. O relatório fica escondido e o cronômetro parado até você continuar.</p>
    <button type="button" id="continuar" class="primario">Continuar a leitura</button>
  </section>
  <article id="relatorio" class="relatorio" hidden></article>
  <aside id="painel" class="painel" aria-label="Ficha do relatório" hidden>
    <div class="painel-topo so-largo"><strong id="painel-titulo"></strong></div>
    <div id="decidir">
      <p class="relogio"><span class="luz" aria-hidden="true"></span> Cronômetro ligado <button type="button" id="pausar" class="discreto">Pausar</button></p>
      <p class="pergunta so-largo">Você aceita o diagnóstico da seção 1, Veredito?</p>
      <div class="decisoes"><button type="button" id="aceitar" class="decisao">Aceitar</button><button type="button" id="recusar" class="decisao">Recusar</button></div>
      <p class="nota so-largo">O clique para o cronômetro.</p>
    </div>
    <div id="ficha" hidden>
      <p id="tempo" class="tempo"></p>
      <fieldset><legend>Decisão</legend><div class="opcoes">
        <span class="opcao"><input type="radio" name="decisao" id="dec-aceitar" value="aceitar"><label for="dec-aceitar">Aceitar</label></span>
        <span class="opcao"><input type="radio" name="decisao" id="dec-recusar" value="recusar"><label for="dec-recusar">Recusar</label></span>
      </div></fieldset>
      <fieldset><legend>Achou no relatório onde está o erro do agente?</legend><div class="opcoes">
        <span class="opcao"><input type="radio" name="erro" id="erro-sim" value="sim"><label for="erro-sim">Sim</label></span>
        <span class="opcao"><input type="radio" name="erro" id="erro-nao" value="não"><label for="erro-nao">Não</label></span>
        <span class="opcao"><input type="radio" name="erro" id="erro-na" value="n.a."><label for="erro-na">Não vi erro</label></span>
      </div><p class="dica">Erro do agente é o que fez o diagnóstico sair errado. Se o diagnóstico parece certo, marque Não vi erro.</p></fieldset>
      <fieldset><legend>Utilidade do relatório</legend><div class="opcoes">
        <span class="opcao"><input type="radio" name="utilidade" id="util-1" value="1"><label for="util-1">1</label></span>
        <span class="opcao"><input type="radio" name="utilidade" id="util-2" value="2"><label for="util-2">2</label></span>
        <span class="opcao"><input type="radio" name="utilidade" id="util-3" value="3"><label for="util-3">3</label></span>
        <span class="opcao"><input type="radio" name="utilidade" id="util-4" value="4"><label for="util-4">4</label></span>
        <span class="opcao"><input type="radio" name="utilidade" id="util-5" value="5"><label for="util-5">5</label></span>
      </div><p class="dica">1 é nenhuma; 5 é que decidiu sozinho.</p></fieldset>
      <fieldset><legend>Sua avaliação do diagnóstico</legend><div class="opcoes">
        <span class="opcao"><input type="radio" name="avaliacao" id="aval-certo" value="certo"><label for="aval-certo">Certo</label></span>
        <span class="opcao"><input type="radio" name="avaliacao" id="aval-errado" value="errado"><label for="aval-errado">Errado</label></span>
      </div></fieldset>
      <label class="campo" for="comentario">Comentário, se quiser</label>
      <textarea id="comentario" rows="3" placeholder="Se achou o erro, diga em que parte do relatório ele está."></textarea>
      <p id="mensagem" class="mensagem" role="alert"></p>
      <div class="acoes">
        <button type="button" id="salvar" class="primario">Salvar e ir ao próximo</button>
        <button type="button" id="voltar-a-ler" class="discreto">Voltar a ler</button>
        <button type="button" id="voltar-sem-mudar" class="discreto" hidden>Voltar sem mudar</button>
      </div>
    </div>
  </aside>
  <section id="fim" hidden>
    <h2 id="fim-titulo"></h2>
    <p id="fim-texto"></p>
    <div class="tabela"><table>
      <thead><tr><th>#</th><th>Tempo (s)</th><th>Achou o erro</th><th>Decisão</th><th>Utilidade</th><th>Avaliação</th><th>Comentário</th><th><span class="so-leitor">Corrigir</span></th></tr></thead>
      <tbody id="fim-linhas"></tbody>
    </table></div>
    <details id="copia"><summary>Copiar as respostas</summary>
      <p class="nota">Serve para quando as respostas não chegam ao banco da página: cole o texto na conversa com o Claude.</p>
      <textarea id="respostas-texto" rows="8" readonly></textarea>
      <div class="acoes"><button type="button" id="copiar" class="secundario">Copiar</button> <span id="copia-status" role="status"></span></div>
    </details>
  </section>
</main>
"""

JS = """
(() => {
  "use strict";
  document.documentElement.lang = "pt-BR";
  const CASOS = JSON.parse(document.getElementById("casos").textContent);
  const IDS = new Set(CASOS.map((c) => c.caso));
  const CHAVE = "sessao_revisao_trilha_v1";
  const $ = (id) => document.getElementById(id);
  const vazio = () => ({erro: null, utilidade: null, avaliacao: null, comentario: ""});
  const estado = {fase: "inicio", atual: 0, revisitando: false, documento: null, decisao: null, respostas: vazio(), aberto_em: null, decidido_em: null, segundos: null, segundos_relogio: null, pausas: 0, retomadas: 0};
  const relogio = {acumulado: 0, desde: null};
  const enviando = new Set();
  let salvas = {};
  let pendentes = {};
  let banco = null;
  let semBanco = false;
  let falha = "";
  let cargaAtrasada = false;
  let relatorioMostrado = -1;

  const decorrido = () => relogio.acumulado + (relogio.desde === null ? 0 : performance.now() - relogio.desde);
  function ligar() { if (relogio.desde === null && document.visibilityState === "visible") relogio.desde = performance.now(); }
  function desligar() { if (relogio.desde !== null) { relogio.acumulado += performance.now() - relogio.desde; relogio.desde = null; } }

  function guardar() {
    try {
      localStorage.setItem(CHAVE, JSON.stringify({caso: CASOS[estado.atual].caso, fase: estado.revisitando ? "antes" : estado.fase, decorrido: decorrido(), decisao: estado.decisao,
        respostas: estado.respostas, aberto_em: estado.aberto_em, decidido_em: estado.decidido_em, segundos: estado.segundos, segundos_relogio: estado.segundos_relogio,
        pausas: estado.pausas, retomadas: estado.retomadas, pendentes}));
    } catch (e) { /* sem armazenamento local a sessão continua; só a retomada depois de recarregar se perde */ }
  }

  function restaurar() {
    let r = null;
    try { r = JSON.parse(localStorage.getItem(CHAVE) || "null"); } catch (e) { r = null; }
    if (!r) return;
    pendentes = r.pendentes || {};
    const i = CASOS.findIndex((c) => c.caso === r.caso);
    if (i < 0 || pendentes[r.caso] || !["lendo", "pausado", "decidido"].includes(r.fase)) return;
    estado.atual = i;
    relogio.acumulado = r.decorrido || 0;
    estado.aberto_em = r.aberto_em;
    estado.pausas = r.pausas || 0;
    estado.retomadas = (r.retomadas || 0) + (r.fase === "lendo" ? 1 : 0);
    if (r.fase === "decidido") {
      estado.fase = "decidido";
      estado.decisao = r.decisao;
      estado.decidido_em = r.decidido_em;
      estado.segundos = r.segundos;
      estado.segundos_relogio = r.segundos_relogio;
      estado.respostas = Object.assign(vazio(), r.respostas);
      mostrarRelatorio(i);
    } else {
      estado.fase = "pausado";
    }
  }

  function mostrarRelatorio(i) {
    if (relatorioMostrado === i) return;
    $("relatorio").replaceChildren($("rel-" + i).content.cloneNode(true));
    relatorioMostrado = i;
  }

  function limparCaso() {
    estado.revisitando = false;
    estado.documento = null;
    estado.decisao = null;
    estado.respostas = vazio();
    estado.aberto_em = null;
    estado.decidido_em = null;
    estado.segundos = null;
    estado.segundos_relogio = null;
    estado.pausas = 0;
    estado.retomadas = 0;
    relogio.acumulado = 0;
    relogio.desde = null;
    $("relatorio").replaceChildren();
    relatorioMostrado = -1;
  }

  const respondido = (c) => Boolean(salvas[c.caso] || pendentes[c.caso]);
  const documentoDe = (c) => pendentes[c.caso] || salvas[c.caso];
  const lendo = () => ["lendo", "pausado", "decidido"].includes(estado.fase);

  function reposicionar() {
    if (lendo()) return;
    const i = CASOS.findIndex((c) => !respondido(c));
    if (i < 0) { estado.fase = "fim"; return; }
    estado.atual = i;
    if (estado.fase === "fim" || CASOS.some(respondido)) estado.fase = "antes";
  }

  const rolarAoTopo = () => window.scrollTo(0, 0);

  function comecar() { estado.fase = "antes"; reposicionar(); guardar(); render(); }

  function abrir() {
    limparCaso();
    estado.fase = "lendo";
    estado.aberto_em = Date.now();
    mostrarRelatorio(estado.atual);
    ligar();
    guardar();
    render();
    rolarAoTopo();
  }

  function pausar() { desligar(); estado.pausas += 1; estado.fase = "pausado"; guardar(); render(); rolarAoTopo(); }

  function continuar() { estado.fase = "lendo"; mostrarRelatorio(estado.atual); ligar(); guardar(); render(); }

  function decidir(valor) {
    desligar();
    estado.decisao = valor;
    estado.decidido_em = Date.now();
    estado.segundos = Math.round(relogio.acumulado / 1000);
    estado.segundos_relogio = Math.round((estado.decidido_em - estado.aberto_em) / 1000);
    estado.fase = "decidido";
    guardar();
    render();
    if (window.matchMedia("(max-width:979.98px)").matches) window.scrollTo(0, $("palco").offsetTop);
  }

  function voltarALer() {
    estado.fase = "lendo";
    estado.decisao = null;
    estado.decidido_em = null;
    estado.segundos = null;
    estado.segundos_relogio = null;
    $("mensagem").textContent = "";
    ligar();
    guardar();
    render();
  }

  function corrigir(i) {
    const c = CASOS[i];
    const d = documentoDe(c);
    if (!d || lendo()) return;
    limparCaso();
    estado.atual = i;
    estado.fase = "decidido";
    estado.revisitando = true;
    estado.documento = d;
    estado.decisao = d.decisao;
    estado.segundos = d.segundos;
    estado.respostas = {erro: d.erro_localizado, utilidade: d.utilidade, avaliacao: d.avaliacao, comentario: d.comentario || ""};
    mostrarRelatorio(i);
    render();
    rolarAoTopo();
  }

  function voltarSemMudar() { limparCaso(); estado.fase = "antes"; reposicionar(); guardar(); render(); rolarAoTopo(); }

  function salvar() {
    const r = estado.respostas;
    const faltam = [];
    if (!estado.decisao) faltam.push("a decisão");
    if (!r.erro) faltam.push("se achou o erro");
    if (!r.utilidade) faltam.push("a utilidade");
    if (!r.avaliacao) faltam.push("a sua avaliação");
    if (faltam.length) { $("mensagem").textContent = "Falta responder: " + faltam.join(", ") + "."; return; }
    const c = CASOS[estado.atual];
    const agora = new Date().toISOString();
    const comum = {decisao: estado.decisao, erro_localizado: r.erro, utilidade: r.utilidade, avaliacao: r.avaliacao, comentario: r.comentario.trim()};
    const doc = estado.revisitando
      ? Object.assign({}, estado.documento, comum, {editado_em: agora})
      : Object.assign({posicao: c.posicao, caso: c.caso, segundos: estado.segundos, segundos_relogio: estado.segundos_relogio, pausas: estado.pausas, retomadas: estado.retomadas,
          aberto_em: new Date(estado.aberto_em).toISOString(), decidido_em: new Date(estado.decidido_em).toISOString(), salvo_em: agora}, comum);
    pendentes[c.caso] = doc;
    limparCaso();
    estado.fase = "antes";
    reposicionar();
    guardar();
    Object.keys(pendentes).forEach(enviar);
    render();
    rolarAoTopo();
  }

  async function gravarComUmaRepeticao(id, doc) {
    const ref = banco.collection("respostas").doc(id);
    try {
      await ref.set(doc);
    } catch (e) {
      if (!e || e.code !== "unavailable") throw e;
      await new Promise((pronto) => setTimeout(pronto, 400 + Math.random() * 800));
      await ref.set(doc);
    }
  }

  async function enviar(id) {
    const doc = pendentes[id];
    if (!doc || !banco || enviando.has(id)) return;
    enviando.add(id);
    try {
      await gravarComUmaRepeticao(id, doc);
      salvas[id] = doc;
      if (pendentes[id] === doc) delete pendentes[id];
      falha = "";
    } catch (e) {
      falha = (e && (e.message || e.code)) || "erro desconhecido";
    } finally {
      enviando.delete(id);
      guardar();
      render();
    }
  }

  const naoChegaram = () => Object.keys(pendentes).filter((id) => !enviando.has(id)).length;

  function renderAviso() {
    const n = naoChegaram();
    let texto = "";
    if (semBanco) {
      texto = "Esta janela não alcança o banco da página, então as respostas ficam só neste navegador. No fim, copie as respostas e cole na conversa com o Claude.";
    } else if (n && banco) {
      texto = (falha ? "Não consegui salvar: " + falha + ". " : "") + n + (n === 1 ? " resposta ainda não chegou" : " respostas ainda não chegaram") + " ao banco da página. Elas estão guardadas neste navegador.";
    } else if (cargaAtrasada) {
      texto = "As respostas salvas ainda não chegaram. Se você já respondeu algum relatório, espere um pouco antes de abrir o próximo.";
    }
    $("aviso-texto").textContent = texto;
    $("aviso").hidden = !texto;
    $("tentar").hidden = !(n && banco && !semBanco);
  }

  function renderTrilho() {
    CASOS.forEach((c, i) => {
      const b = $("pip-" + i);
      const feito = respondido(c);
      const atual = i === estado.atual && estado.fase !== "inicio" && estado.fase !== "fim";
      b.className = "pip" + (feito ? " salvo" : "") + (atual ? " atual" : "");
      b.disabled = !feito || lendo();
      b.setAttribute("aria-label", "Relatório " + c.posicao + (feito ? ", respondido" : atual ? ", o próximo" : ", ainda não aberto"));
      if (atual) b.setAttribute("aria-current", "step"); else b.removeAttribute("aria-current");
    });
    $("contagem").textContent = CASOS.filter(respondido).length + " de " + CASOS.length + " respondidos";
  }

  function marcar(nome, valor) {
    document.querySelectorAll('input[name="' + nome + '"]').forEach((x) => { x.checked = x.value === String(valor); });
  }

  function renderPainel() {
    const c = CASOS[estado.atual];
    $("painel-titulo").textContent = "Relatório " + c.posicao + " de " + CASOS.length;
    const decidido = estado.fase === "decidido";
    $("decidir").hidden = decidido;
    $("ficha").hidden = !decidido;
    if (!decidido) return;
    const r = estado.respostas;
    $("tempo").textContent = "Decidiu em " + estado.segundos + " s." + (estado.revisitando ? " Corrigir não muda esse tempo." : "");
    marcar("decisao", estado.decisao);
    marcar("erro", r.erro);
    marcar("utilidade", r.utilidade);
    marcar("avaliacao", r.avaliacao);
    if ($("comentario").value !== r.comentario) $("comentario").value = r.comentario;
    $("voltar-a-ler").hidden = estado.revisitando;
    $("voltar-sem-mudar").hidden = !estado.revisitando;
    const faltaSoEste = CASOS.filter((x) => !respondido(x)).length <= 1;
    $("salvar").textContent = estado.revisitando ? "Salvar a correção" : faltaSoEste ? "Salvar e terminar" : "Salvar e ir ao próximo";
  }

  function renderFim() {
    const docs = CASOS.map(documentoDe).filter(Boolean);
    const soAqui = semBanco || naoChegaram() > 0;
    $("fim-titulo").textContent = "As " + docs.length + " respostas " + (soAqui ? "estão neste navegador" : "estão salvas");
    $("fim-texto").textContent = soAqui
      ? "Elas ainda não estão no banco da página. Copie as respostas abaixo e cole na conversa com o Claude."
      : "Volte à conversa com o Claude e escreva terminei. Ele lê as respostas daqui, preenche a planilha e só então abre o resultado de cada caso.";
    const corpo = $("fim-linhas");
    corpo.replaceChildren();
    CASOS.forEach((c, i) => {
      const d = documentoDe(c);
      if (!d) return;
      const tr = document.createElement("tr");
      [String(d.posicao), String(d.segundos), d.erro_localizado, d.decisao, String(d.utilidade), d.avaliacao, d.comentario || ""].forEach((v) => {
        const td = document.createElement("td");
        td.textContent = v;
        tr.appendChild(td);
      });
      const td = document.createElement("td");
      const b = document.createElement("button");
      b.type = "button";
      b.className = "discreto";
      b.textContent = "Corrigir";
      b.dataset.corrigir = String(i);
      td.appendChild(b);
      tr.appendChild(td);
      corpo.appendChild(tr);
    });
    $("respostas-texto").value = JSON.stringify(docs, null, 2);
    if (soAqui) $("copia").open = true;
  }

  function render() {
    const f = estado.fase;
    const c = CASOS[estado.atual];
    $("palco").dataset.fase = f;
    $("inicio").hidden = f !== "inicio";
    $("antes").hidden = f !== "antes";
    $("pausado").hidden = f !== "pausado";
    $("relatorio").hidden = !(f === "lendo" || f === "decidido");
    $("painel").hidden = !(f === "lendo" || f === "decidido");
    $("fim").hidden = f !== "fim";
    renderTrilho();
    renderAviso();
    if (f === "antes") {
      $("antes-titulo").textContent = "Relatório " + c.posicao + " de " + CASOS.length;
    }
    if (f === "pausado") $("pausado-titulo").textContent = "Relatório " + c.posicao + " de " + CASOS.length;
    if (f === "lendo" || f === "decidido") renderPainel();
    if (f === "fim") renderFim();
  }

  const pronta = () => { $("palco").dataset.pronta = "sim"; };

  $("comecar").addEventListener("click", comecar);
  $("abrir").addEventListener("click", abrir);
  $("pausar").addEventListener("click", pausar);
  $("continuar").addEventListener("click", continuar);
  $("aceitar").addEventListener("click", () => decidir("aceitar"));
  $("recusar").addEventListener("click", () => decidir("recusar"));
  $("voltar-a-ler").addEventListener("click", voltarALer);
  $("voltar-sem-mudar").addEventListener("click", voltarSemMudar);
  $("salvar").addEventListener("click", salvar);
  $("tentar").addEventListener("click", () => { falha = ""; Object.keys(pendentes).forEach(enviar); render(); });
  $("ficha").addEventListener("change", (ev) => {
    const a = ev.target;
    if (a.name === "decisao") estado.decisao = a.value;
    if (a.name === "erro") estado.respostas.erro = a.value;
    if (a.name === "utilidade") estado.respostas.utilidade = Number(a.value);
    if (a.name === "avaliacao") estado.respostas.avaliacao = a.value;
    $("mensagem").textContent = "";
    guardar();
  });
  $("comentario").addEventListener("input", (ev) => { estado.respostas.comentario = ev.target.value; guardar(); });
  $("trilho-lista").addEventListener("click", (ev) => {
    const b = ev.target.closest("button[data-i]");
    if (b && !b.disabled) corrigir(Number(b.dataset.i));
  });
  $("fim").addEventListener("click", (ev) => {
    const b = ev.target.closest("button[data-corrigir]");
    if (b) corrigir(Number(b.dataset.corrigir));
  });
  $("copiar").addEventListener("click", () => {
    const texto = $("respostas-texto");
    const escolher = () => { texto.focus(); texto.select(); $("copia-status").textContent = "Selecionei o texto: use Ctrl+C."; };
    if (!navigator.clipboard) { escolher(); return; }
    navigator.clipboard.writeText(texto.value).then(() => { $("copia-status").textContent = "Copiado."; }, escolher);
  });
  document.addEventListener("visibilitychange", () => {
    if (estado.fase !== "lendo") return;
    if (document.visibilityState === "visible") ligar(); else { desligar(); guardar(); }
  });
  window.addEventListener("pagehide", guardar);
  setInterval(() => { if (estado.fase === "lendo") guardar(); }, 5000);

  function semOBanco(motivo) {
    banco = null;
    semBanco = true;
    falha = motivo || "";
    cargaAtrasada = false;
    reposicionar();
    render();
    pronta();
  }

  async function iniciar() {
    restaurar();
    reposicionar();
    render();
    let db = null;
    try { db = window.claude ? await window.claude.use("db") : null; } catch (e) { db = null; }
    if (!db) { semOBanco(); return; }
    banco = db;
    const limite = setTimeout(() => { cargaAtrasada = true; render(); pronta(); }, 10000);
    banco.collection("respostas").onSnapshot((foto) => {
      if (!foto.metadata.fromCache) { clearTimeout(limite); cargaAtrasada = false; }
      const novas = {};
      foto.docs.forEach((d) => { if (IDS.has(d.id)) novas[d.id] = d.data(); });
      salvas = Object.assign({}, salvas, novas);
      reposicionar();
      render();
      pronta();
    }, (e) => { clearTimeout(limite); semOBanco((e && (e.message || e.code)) || ""); });
  }

  iniciar();
})();
"""


def ler_planilha(caminho: Path) -> list[dict]:
    """As linhas de relatório da planilha, na ordem dela: posição, caso e caminho do relatório, sem as crases, mais as células cruas."""
    linhas = []
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if RE_LINHA.match(linha):
            c = pt.celulas(linha)
            linhas.append({"posicao": int(c[0]), "caso": c[1].strip("`"), "relatorio": c[3].strip("`"), "celulas": c})
    return linhas


def _apelido(x: dict) -> str:
    return f"relatorio-{x['posicao']}"


def pagina(linhas: list[dict], pasta: Path) -> str:
    """A página da sessão. Recebe só as linhas da planilha e a pasta dela; o nome do caso vira relatorio-N e a coluna Classe não entra."""
    moldes = []
    for i, x in enumerate(linhas):
        texto = pt.sem_comentarios((pasta / x["relatorio"]).read_text(encoding="utf-8"))
        achado = RE_RESULTADO.search(texto)
        if achado:
            raise ValueError(f"o relatório de {x['caso']} traz o resultado do caso ({achado.group(0)}); a sessão deixaria de ser às cegas")
        texto = re.sub(rf"(?<![\w-]){re.escape(x['caso'])}(?![\w-])", _apelido(x), RE_COMANDO.sub("", texto))
        outro = RE_NOME_DE_CASO.search(texto)
        if outro:
            raise ValueError(f"o relatório de {x['caso']} cita o nome de outro caso ({outro.group(0)}); a sessão deixaria de ser às cegas")
        moldes.append(f'<template id="rel-{i}">{tp._relatorio_para_html(texto)}</template>')
    casos = json.dumps([{"posicao": x["posicao"], "caso": _apelido(x)} for x in linhas], ensure_ascii=False).replace("<", chr(92) + "u003c")
    pips = "".join(f'<li><button type="button" class="pip" id="pip-{i}" data-i="{i}" disabled>{x["posicao"]}</button></li>' for i, x in enumerate(linhas))
    corpo = CORPO.replace("@@TOTAL@@", str(len(linhas))).replace("@@PIPS@@", pips)
    return ("<title>Revisão dos relatórios da trilha</title>\n"
            '<meta name="claude:viewport-fit-sides" content="cover">\n'
            "<!-- ! Alteração de IA - Revisar: página gerada por ferramentas/sessao_revisao.py para a sessão de revisão dos relatórios da corrida 22 (Fase 4).\n"
            "     ! Motivo: a medida com revisor humano da especificação da trilha (seção 12 c) precisa de um relatório por vez, do tempo até a decisão e de nada sobre o resultado de cada caso; "
            "a página leva só a ordem da planilha e o texto dos relatórios, e as respostas ficam no banco da própria página até irem para revisao_trilha.md. -->\n"
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
            f"<style>{CSS}</style>\n{corpo}\n" + "\n".join(moldes) +
            f'\n<script type="application/json" id="casos">{casos}</script>\n<script>{JS}</script>\n')


def _erros_da_resposta(r: dict) -> list[str]:
    erros = [f"{campo} = {r.get(campo)!r}" for campo, aceitos in VALORES.items() if r.get(campo) not in aceitos]
    parecer_sem_tempo = r.get("segundos") is None and r.get("origem") == ORIGEM_PARECER
    if not parecer_sem_tempo and (type(r.get("segundos")) is not int or r["segundos"] < 0):
        erros.append(f"segundos = {r.get('segundos')!r}")
    if type(r.get("utilidade")) is not int or not 1 <= r["utilidade"] <= 5:
        erros.append(f"utilidade = {r.get('utilidade')!r}")
    return erros


def _comentario(texto) -> str:
    return " ".join(str(texto or "").replace("|", "/").split())


def gravar_respostas(caminho: Path, respostas: list[dict], corrigir: bool = False) -> list[str]:
    """Põe as respostas nas células do revisor, pela posição do relatório na planilha, e devolve os casos ainda em branco. Confere tudo antes de gravar: com um valor que a
    planilha não aceita, ou com uma linha já preenchida de outro jeito (sem `corrigir`), levanta ValueError e o arquivo fica como estava."""
    posicoes = {x["posicao"] for x in ler_planilha(caminho)}
    por_posicao = {}
    for r in respostas:
        p = r.get("posicao")
        if p not in posicoes or r.get("caso") != f"relatorio-{p}":
            raise ValueError(f"resposta fora da planilha: posição {p!r}, relatório {r.get('caso')!r}")
        erros = _erros_da_resposta(r)
        if erros:
            raise ValueError(f"resposta inválida no relatório {p}: {', '.join(erros)}")
        por_posicao[p] = r
    saida, faltam = [], []
    for linha in caminho.read_text(encoding="utf-8").split("\n"):
        if not RE_LINHA.match(linha):
            saida.append(linha)
            continue
        c = pt.celulas(linha)
        r = por_posicao.get(int(c[0]))
        if r is None:
            if EM_BRANCO in c[4:9]:
                faltam.append(c[1].strip("`"))
            saida.append(linha)
            continue
        novas = [TEMPO_NAO_MEDIDO if r["segundos"] is None else str(r["segundos"]), r["erro_localizado"], r["decisao"], str(r["utilidade"]), r["avaliacao"], _comentario(r.get("comentario"))]
        atuais = c[4:10]
        if EM_BRANCO not in atuais[:5] and atuais != novas and not corrigir:
            raise ValueError(f"a linha do relatório {r['posicao']} já está preenchida com outros valores: {atuais}; use corrigir para trocar")
        saida.append("| " + " | ".join(c[:4] + novas) + " |")
    caminho.write_text("\n".join(saida), encoding="utf-8", newline="\n")
    return faltam


def respostas_do_parecer(texto: str, desde: int, comentario: str) -> list[dict]:
    """As linhas da tabela da pré-análise, a partir de uma posição, no formato que gravar_respostas aceita: sem tempo e marcadas como parecer aprovado."""
    respostas = []
    for linha in texto.splitlines():
        if RE_LINHA.match(linha):
            c = pt.celulas(linha)
            if int(c[0]) >= desde:
                respostas.append({"posicao": int(c[0]), "caso": f"relatorio-{int(c[0])}", "segundos": None, "origem": ORIGEM_PARECER, "erro_localizado": c[4], "decisao": c[5],
                                  "utilidade": int(c[6]), "avaliacao": c[7], "comentario": comentario})
    return respostas


def main() -> int:
    ap = argparse.ArgumentParser(description="Página da sessão de revisão dos relatórios da trilha e gravação das respostas na planilha.")
    ap.add_argument("--gravar", type=Path, help="arquivo JSON com a lista de respostas lidas do banco da página")
    ap.add_argument("--corrigir", action="store_true", help="com --gravar, troca linhas já preenchidas")
    args = ap.parse_args()
    if args.gravar:
        faltam = gravar_respostas(PLANILHA, json.loads(args.gravar.read_text(encoding="utf-8")), corrigir=args.corrigir)
        print(f"{PLANILHA.name}: gravada; casos em branco: {len(faltam)}")
        return 0
    linhas = ler_planilha(PLANILHA)
    SAIDA.write_text(pagina(linhas, PLANILHA.parent), encoding="utf-8", newline="\n")
    print(f"{SAIDA.name}: {len(linhas)} relatórios, {SAIDA.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
