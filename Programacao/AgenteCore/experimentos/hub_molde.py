#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/11/2026, molde visual do hub, ficha 113): o estilo e o programa dos diagramas da página do hub,
# desenhados em SVG pelo próprio navegador, sem biblioteca de fora: a linha de produção de um caso (as seis etapas da figura "Como o agente
# trabalha", as três saídas e a trilha, com o estado e o tempo gravado de cada uma, e o cartão que amplia ao clicar), a rede que liga os sinais
# do caso, os verbetes pontuados, as causas possíveis e o resultado (no lugar da árvore de decisão em texto corrido), o diagrama dos espaços de
# trabalho na tela "Início" (quem usa, o hub, o agente, o navegador, o site, a API, o banco, o modelo local e a biblioteca, com o que está no
# ar aceso) e os gráficos de barras das métricas. `hub_pagina.py` junta `CSS` e `JS` daqui ao estilo e ao programa que ele já servia.
# ! Motivo: o Eric testou o hub em 26/11/2026 e pediu um molde visual: menos texto na tela, cada campo explicado e diagramas gerados por
# código na máquina, com o processo, o tempo de cada etapa e o resultado ao abrir cada cartão. Ficou em arquivo próprio para o desenho não se
# misturar com a revisão (comentários, veredito), que `hub_pagina.py` já fazia. Todo número desenhado vem do que o servidor entrega
# (`hub_dados.processo_do_caso`, `hub_dados.metricas`, `/api/central`): o programa não calcula resultado nenhum, só posiciona. A etapa sem
# tempo gravado aparece como "sem tempo gravado", nunca com tempo estimado. As cores vêm das variáveis do estilo, para o tema escuro valer
# também nos diagramas, e o desenho é refeito quando a largura da janela muda, para a tela estreita empilhar as etapas em vez de encolher a letra.
"""O molde visual do hub (ficha 113): o estilo e o programa dos diagramas em SVG, juntados à página por `hub_pagina.py`."""

CSS = r"""
:root{--et-codigo:#2f5d8a;--et-codigo-bg:#e9f1fa;--et-modelo:#c2571f;--et-modelo-bg:#fdeee4;--et-saida:#6b6f73;--et-saida-bg:#f1efe9}
@media (prefers-color-scheme:dark){:root{--et-codigo:#7fb0e0;--et-codigo-bg:#1f2a36;--et-modelo:#f0a070;--et-modelo-bg:#33251c;--et-saida:#a8adb4;--et-saida-bg:#23272c}}
.diagrama{margin:8px 0}.diagrama svg{display:block;max-width:100%;height:auto}
.diagrama.rolavel{overflow-x:auto}.diagrama.rolavel svg{min-width:720px}
svg text{font-family:var(--fb);fill:var(--ink)}
svg .etapa,svg .saida,svg .no-clicavel,svg .barra-da-corrida{cursor:pointer}
svg .etapa rect.cartao-da-etapa,svg .saida rect.cartao-da-etapa{stroke-width:1.5}
svg .etapa.por-codigo rect.cartao-da-etapa{fill:var(--et-codigo-bg);stroke:var(--et-codigo)}
svg .etapa.por-modelo rect.cartao-da-etapa{fill:var(--et-modelo-bg);stroke:var(--et-modelo)}
svg .saida rect.cartao-da-etapa,svg .trilha rect.cartao-da-etapa{fill:var(--et-saida-bg);stroke:var(--et-saida)}
svg .trilha{cursor:pointer}svg .trilha:hover rect.cartao-da-etapa,svg .trilha:focus rect.cartao-da-etapa{stroke-width:3}svg .trilha:focus{outline:none}
svg .saida.saiu rect.cartao-da-etapa{stroke:var(--bom);stroke-width:2}
svg .nao-se-aplica rect.cartao-da-etapa,svg .pendente rect.cartao-da-etapa{stroke-dasharray:5 4;fill:var(--bg2)}
svg .nao-se-aplica text,svg .pendente text{fill:var(--ink2)}
svg .etapa:hover rect.cartao-da-etapa,svg .saida:hover rect.cartao-da-etapa,svg .etapa:focus rect.cartao-da-etapa,svg .saida:focus rect.cartao-da-etapa{stroke-width:3}
svg .etapa:focus,svg .saida:focus,svg .barra-da-corrida:focus{outline:none}
svg .titulo{font-size:13px;font-weight:600}
svg .tempo{font-size:15px;font-weight:700;font-variant-numeric:tabular-nums}
svg .nao-se-aplica .tempo,svg .pendente .tempo,svg .sem-tempo .tempo{font-size:12px;font-weight:500;fill:var(--ink2)}
svg .resumo{font-size:11.5px;fill:var(--ink2)}
svg .seta{stroke:var(--ink2);stroke-width:1.4;fill:none}svg .ponta{fill:var(--ink2)}
svg .em-andamento rect.cartao-da-etapa{stroke-width:3}
svg .andamento-trilho{fill:var(--bg2);stroke:var(--linha)}svg .andamento-cheio{fill:var(--et-modelo)}
@media (prefers-reduced-motion:no-preference){svg .em-andamento rect.cartao-da-etapa{animation:pulso 1.2s ease-in-out infinite alternate}}
@keyframes pulso{from{stroke-opacity:.35}to{stroke-opacity:1}}
.legenda-do-diagrama{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:12px;color:var(--ink2);margin:6px 0}
.legenda-do-diagrama span::before{content:"";display:inline-block;width:12px;height:12px;border-radius:3px;border:1.5px solid var(--et-saida);background:var(--et-saida-bg);margin-right:6px;vertical-align:-2px}
.legenda-do-diagrama .l-codigo::before{border-color:var(--et-codigo);background:var(--et-codigo-bg)}.legenda-do-diagrama .l-modelo::before{border-color:var(--et-modelo);background:var(--et-modelo-bg)}
.fichas{display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px;margin:6px 0}
.ficha{display:inline-flex;gap:6px;align-items:baseline;border:1px solid var(--linha);border-radius:999px;padding:2px 10px;font-size:12.5px;background:var(--bg2)}
.ficha b{font-variant-numeric:tabular-nums}.ficha.bom{border-color:var(--bom);color:var(--bom)}.ficha.ruim{border-color:var(--ruim);color:var(--ruim)}
details.nota-do-tempo,details.por-escrito,details.tabela-recolhida,details.por-extenso{font-size:13px}
.zoom{position:fixed;inset:0;z-index:40;background:rgba(15,18,22,.55);display:flex;align-items:flex-start;justify-content:center;padding:6vh 16px;overflow-y:auto}
.zoom-caixa{background:var(--bg2);border:1px solid var(--linha);border-radius:12px;box-shadow:var(--sombra);padding:18px 22px;width:min(720px,100%);position:relative}
.zoom-caixa h2{margin-right:90px}#fechar-zoom{position:absolute;top:14px;right:16px}
.zoom-caixa .o-que-e{color:var(--ink2);margin:2px 0 10px}
.barra-h{display:grid;grid-template-columns:minmax(110px,38%) minmax(60px,1fr) minmax(70px,auto);gap:10px;align-items:center;margin:5px 0;font-size:13px}
.barra-h .rotulo-da-barra{overflow-wrap:anywhere}.barra-h .valor{font:13px var(--fm);color:var(--ink2);text-align:right;white-space:nowrap}
.barra-h.destaque .trilho div{background:var(--acento)}.barra-h.destaque .rotulo-da-barra{font-weight:600}.barra-h.alerta .trilho div{background:var(--ruim)}
.duas-partes{display:flex;height:16px;border:1px solid var(--linha);border-radius:999px;overflow:hidden;margin:6px 0}
.duas-partes div{height:100%}.duas-partes .p1{background:var(--et-codigo)}.duas-partes .p2{background:var(--et-modelo)}
.conferencia{display:flex;gap:8px;align-items:baseline;font-size:13px;margin:3px 0}.conferencia::before{content:"";flex:none;width:9px;height:9px;border-radius:50%;background:var(--bom)}
.conferencia.nao::before{background:var(--ruim)}.conferencia .regra{color:var(--ink2);font-size:12px}
svg .titulo-da-camada{font-size:12px;font-weight:600;fill:var(--ink2);text-anchor:middle;letter-spacing:.03em;text-transform:uppercase}
svg .no rect{fill:var(--bg2);stroke:var(--linha);stroke-width:1.2}svg .no.destaque rect{stroke:var(--acento);stroke-width:2.2;fill:var(--acento2)}
svg .no .rotulo-do-no{font-size:12px}svg .no.destaque .rotulo-do-no{font-weight:600}
svg .no .valor-do-no{font-size:11px;fill:var(--ink2);font-variant-numeric:tabular-nums}
svg .no .medida-trilho{fill:var(--bg);stroke:none}svg .no .medida-cheia{fill:var(--ink2)}svg .no.destaque .medida-cheia{fill:var(--acento)}
svg .aresta{fill:none;stroke:var(--ink2);stroke-opacity:.28}svg .aresta.destaque{stroke:var(--acento);stroke-opacity:.8}
svg .vazio-da-camada{font-size:12px;fill:var(--ink2);text-anchor:middle}
svg .ligacao{fill:none;stroke:var(--ink2);stroke-width:1.3}svg .rotulo-da-ligacao{font-size:10.5px;fill:var(--ink2);stroke:var(--bg2);stroke-width:4px;paint-order:stroke;stroke-linejoin:round}
svg .ws rect{fill:var(--bg2);stroke:var(--linha);stroke-width:1.4}svg .ws .nome-do-no{font-size:12.5px;font-weight:600}svg .ws .sub-do-no{font-size:11px;fill:var(--ink2)}
svg .ws.no-ar rect{stroke:var(--bom);stroke-width:2}svg .ws.fora-do-ar rect{stroke:var(--ruim);stroke-width:2;stroke-dasharray:5 4}
svg .ws .estado-do-no{font:600 11px var(--fm)}svg .ws.no-ar .estado-do-no{fill:var(--bom)}svg .ws.fora-do-ar .estado-do-no{fill:var(--ruim)}
svg .ws.centro rect{fill:var(--et-codigo-bg);stroke:var(--et-codigo);stroke-width:2}svg .ws.do-modelo rect{fill:var(--et-modelo-bg)}
svg .rotulo-do-grafico{font-size:12.5px}svg .valor-do-grafico{font-size:12.5px;font-variant-numeric:tabular-nums}
svg .trilho-do-grafico{fill:var(--bg);stroke:var(--linha)}svg .cheio-do-grafico{fill:var(--acento)}
svg .barra-da-corrida.destaque .cheio-do-grafico,svg .barra-da-corrida:hover .cheio-do-grafico{fill:var(--et-modelo)}
svg .barra-do-lado.agente .cheio-do-grafico{fill:var(--bom)}svg .barra-do-lado.pessoas .cheio-do-grafico{fill:var(--ink2)}
svg .seg-alta{fill:var(--bom)}svg .seg-media{fill:var(--meio)}svg .seg-baixa{fill:var(--ruim)}svg .seg-outra{fill:var(--ink2)}
.topo-da-lista{display:flex;flex-wrap:wrap;gap:8px 10px;align-items:flex-end;padding:10px 12px;border-bottom:1px solid var(--linha)}
.topo-da-lista .campo{flex:1 1 120px;min-width:0}.topo-da-lista .campo.marcar{flex:1 1 auto}.topo-da-lista select,.topo-da-lista input[type=search]{width:100%;min-width:0}
#abrir-legenda{font-size:12px;padding:2px 9px;border-radius:999px}
.legenda-da-lista{padding:10px 14px;border-bottom:1px solid var(--linha);font-size:12.5px;background:var(--bg)}
.legenda-da-lista dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:4px 10px}.legenda-da-lista dt{font-weight:600}.legenda-da-lista dd{margin:0;color:var(--ink2)}
.grupo-de-casos{border-bottom:1px solid var(--linha)}
.cabeca-do-grupo{display:flex;justify-content:space-between;align-items:baseline;gap:8px;width:100%;border:0;border-radius:0;background:var(--bg);padding:9px 14px;text-align:left;font-weight:600}
.cabeca-do-grupo::before{content:"▸";margin-right:6px;color:var(--ink2)}.cabeca-do-grupo[aria-expanded=true]::before{content:"▾"}
.cabeca-do-grupo .nome-do-grupo{flex:1}.cabeca-do-grupo .contagem{font-weight:400;font-size:12px}
.casos-do-grupo{list-style:none;margin:0;padding:0}.casos-do-grupo .item-caso{border-bottom:0;border-top:1px solid var(--linha);padding:8px 14px}
.titulo-do-item{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.mostrar-mais{display:block;width:calc(100% - 28px);margin:6px 14px 10px;font-size:12.5px}
#servicos.servicos{grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:8px}#servicos .servico{padding:6px 10px;gap:2px;font-size:13px}
#grafico-da-fase-5,#grafico-do-reparo,#grafico-da-confianca,#grafico-dos-cenarios{margin:6px 0 10px}
"""

JS = r"""
// ---------------------------------------------------------------- o molde visual: desenho em SVG, sem biblioteca de fora

const NS = 'http://www.w3.org/2000/svg';
const O_QUE_E = {
  roteiro: 'Abre a página no navegador e segue os passos, olhando a tela e as chamadas à API.',
  deteccao: 'Uma conferência do roteiro não passa, ou a resposta da API mudou.',
  poda: 'Fica só o que mudou contra a tela normal. É a poda, feita em código.',
  busca: 'Separa os verbetes de documentação mais parecidos com o caso.',
  modelo: 'O modelo local, só com CPU, escolhe a causa numa lista fechada.',
  selo: 'O código confere a resposta do modelo e dá um selo de confiança: alta, média ou baixa.',
  contrato: 'A API mudou: sai um relatório para o analista, com a causa e o selo.',
  localizador: 'A tela mudou: o código acha outro seletor e testa de novo, sem o modelo.',
  aprendizado: 'O modelo propõe um acréscimo à biblioteca, e filtros em código decidem se entra.',
  trilha: 'Cada passo fica gravado: o que o agente viu, o que o modelo respondeu e o que o código conferiu.'};
const O_QUE_O_TEMPO_COBRE = {
  roteiro: 'do começo do caso até a página do roteiro fechar',
  deteccao: 'do fim do roteiro até o começo da poda, com a comparação da resposta com o contrato ou a captura da tela',
  poda: 'da redução da tela até o caso ficar montado para o diagnóstico',
  busca: 'a busca dos verbetes e a montagem do pedido ao modelo',
  modelo: 'a chamada ao modelo, do envio do pedido até a resposta',
  selo: 'da resposta do modelo até a decisão ficar gravada: o registro da resposta, a consulta ao Ollama sobre o modelo carregado, as conferências e o selo'};
const ETAPAS_EM_BRANCO = [['roteiro', 'Roda o roteiro', 'codigo'], ['deteccao', 'Detecta a falha', 'codigo'], ['poda', 'Reduz o que viu', 'codigo'],
  ['busca', 'Busca na biblioteca', 'codigo'], ['modelo', 'O modelo diagnostica', 'modelo'], ['selo', 'Confere e dá um selo', 'codigo']];
const SAIDAS_EM_BRANCO = [['contrato', 'Falha de contrato'], ['localizador', 'Localizador quebrado'], ['aprendizado', 'Aprendizado']];

function sv(tag, attrs = {}, ...filhos) {
  const e = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === null || v === undefined || v === false) continue;
    if (k === 'text') e.textContent = v;
    else if (k === 'data') for (const [d, x] of Object.entries(v)) e.setAttribute('data-' + d, x);
    else e.setAttribute(k, v);
  }
  for (const f of filhos.flat()) if (f !== null && f !== undefined && f !== false) e.append(f);
  return e;
}

function quebrar(texto, porLinha, maxLinhas) {
  const linhas = [];
  let atual = '';
  for (let p of String(texto || '').split(/\s+/).filter(Boolean)) {
    if (p.length > porLinha) p = p.slice(0, Math.max(1, porLinha - 1)) + '…';
    if (atual && (atual + ' ' + p).length > porLinha) { linhas.push(atual); atual = p; } else atual = atual ? atual + ' ' + p : p;
  }
  if (atual) linhas.push(atual);
  if (linhas.length > maxLinhas) { linhas.length = maxLinhas; linhas[maxLinhas - 1] = linhas[maxLinhas - 1].slice(0, Math.max(1, porLinha - 1)) + '…'; }
  return linhas;
}

function emLinhas(classe, x, y, linhas, alturaDaLinha) {
  return sv('text', {class: classe, x, y}, linhas.map((l, i) => sv('tspan', {x, dy: i ? alturaDaLinha : 0, text: l})));
}

function curto(texto, max) { texto = String(texto === null || texto === undefined ? '' : texto); return texto.length > max ? texto.slice(0, Math.max(1, max - 1)) + '…' : texto; }

function tempoEmPalavras(s) {
  if (typeof s !== 'number') return '';
  if (s < 1) return Math.round(s * 1000) + ' ms';
  return s < 90 ? comVirgula(s, 1) + ' s' : Math.floor(s / 60) + ' min ' + Math.round(s % 60) + ' s';
}

function porcento(p) { return typeof p === 'number' ? (p * 100).toFixed(1).replace('.', ',') + '%' : 'sem probabilidade lida'; }

function seta(x1, y1, x2, y2) {
  const a = Math.atan2(y2 - y1, x2 - x1), t = 7, l = 3.5;
  const bx = x2 - t * Math.cos(a), by = y2 - t * Math.sin(a);
  return [sv('line', {class: 'seta', x1, y1, x2: bx, y2: by}),
    sv('polygon', {class: 'ponta', points: [x2, y2, bx - l * Math.sin(a), by + l * Math.cos(a), bx + l * Math.sin(a), by - l * Math.cos(a)].map(n => n.toFixed(1)).join(' ')})];
}

function clicavel(no, acao) {
  no.setAttribute('tabindex', '0');
  no.setAttribute('role', 'button');
  no.addEventListener('click', acao);
  no.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); acao(); } });
  return no;
}

// ---------------------------------------------------------------- a linha de produção de um caso

function classeDoEstado(estado) { return String(estado || 'pendente').replace(/_/g, '-'); }

function tempoDaEtapa(e) {
  if (e.sem_detalhe) return 'concluída';
  if (e.estado === 'em_andamento') return 'rodando agora';
  if (e.estado === 'pendente') return 'aguardando';
  if (e.estado === 'nao_se_aplica') return 'não se aplica';
  return typeof e.tempo_s === 'number' ? tempoEmPalavras(e.tempo_s) : 'sem tempo gravado';
}

function processoEmBranco() {
  return {tipo: null, cenario: null, trilha: null, tempo_nao_gravado: null, rede: null,
    etapas: ETAPAS_EM_BRANCO.map(([id, titulo, feito_por], i) => ({id, numero: i + 1, titulo, feito_por, estado: 'pendente', tempo_s: null, resumo: '', detalhe: null})),
    saidas: SAIDAS_EM_BRANCO.map(([id, titulo]) => ({id, titulo, estado: 'pendente', resumo: '', tempo_s: null, detalhe: null}))};
}

function cartaoDoProcesso(item, tipo, x, y, w, h, vivo) {
  const emAndamento = item.estado === 'em_andamento';
  const classe = tipo + ' ' + classeDoEstado(item.estado) + (tipo === 'etapa' ? ' por-' + item.feito_por : '')
    + (item.estado === 'feita' && typeof item.tempo_s !== 'number' ? ' sem-tempo' : '');
  const porLinha = Math.max(10, Math.floor((w - 20) / 6.6));
  const titulo = quebrar((item.numero ? item.numero + '. ' : '') + item.titulo, Math.max(8, Math.floor((w - 20) / 7.4)), 2);
  const yTempo = y + 20 + titulo.length * 16 + 4;
  const tempo = tipo === 'etapa' ? tempoDaEtapa(item)
    : item.estado === 'saiu' ? (typeof item.tempo_s === 'number' ? 'reparo em ' + tempoEmPalavras(item.tempo_s) : 'saiu')
      : item.estado === 'pendente' ? 'aguardando' : item.estado === 'registrada' ? item.contagem : 'não se aplica';
  const sobra = Math.max(0, Math.floor((y + h - (emAndamento ? 22 : 8) - yTempo - 8) / 14));
  const g = sv('g', {class: classe, data: tipo === 'etapa' ? {etapa: item.id} : {saida: item.id}, 'aria-label': item.titulo + ': ' + tempo + (item.resumo ? '. ' + item.resumo : '')},
    sv('rect', {class: 'cartao-da-etapa', x, y, width: w, height: h, rx: 10}),
    emLinhas('titulo', x + 10, y + 20, titulo, 16),
    sv('text', {class: 'tempo', x: x + 10, y: yTempo, text: tempo}),
    sobra ? emLinhas('resumo', x + 10, yTempo + 17, quebrar(item.resumo, porLinha, sobra), 14) : null);
  if (emAndamento) {
    const fracao = vivo && typeof vivo.fracao === 'number' ? Math.max(0.03, Math.min(1, vivo.fracao)) : 0.3;
    g.append(sv('rect', {class: 'andamento-trilho', x: x + 10, y: y + h - 16, width: w - 20, height: 7, rx: 3.5}),
      sv('rect', {class: 'andamento-cheio', x: x + 10, y: y + h - 16, width: (w - 20) * fracao, height: 7, rx: 3.5}));
  }
  return g;
}

function desenharProcesso(alvo, p, vivo) {
  alvo.replaceChildren();
  if (!p) return;
  const etapas = p.etapas.map(e => (vivo && vivo.etapa === e.id ? {...e, estado: 'em_andamento', resumo: vivo.resumo || e.resumo} : e));
  const trilha = {id: 'trilha', titulo: 'Trilha aberta', estado: p.trilha ? 'registrada' : 'pendente', contagem: p.trilha ? p.trilha.eventos + ' eventos gravados' : '',
    resumo: p.trilha ? 'tudo o que o agente viu, respondeu e conferiu neste caso' : '', tempo_s: null};
  const W = Math.max(300, Math.floor(alvo.clientWidth || 1000)), estreito = W < 760, svg = sv('svg', {role: 'group', 'aria-label': 'Linha de produção do caso'});
  const abrir = (item, tipo) => () => abrirZoom(item, tipo, p);
  let H;
  if (!estreito) {
    const vao = 18, cw = (W - 5 * vao) / 6, ch = 128, yB = ch + 44, hB = 104;
    etapas.forEach((e, i) => {
      const x = i * (cw + vao);
      svg.append(clicavel(cartaoDoProcesso(e, 'etapa', x, 1, cw, ch, vivo), abrir(e, 'etapa')));
      if (i) svg.append(...seta(x - vao + 1, 1 + ch / 2, x - 1, 1 + ch / 2));
    });
    const larguraDasSaidas = 4 * cw + 3 * vao, sw = (larguraDasSaidas - 2 * vao) / 3, xDoSelo = 5 * (cw + vao) + cw / 2, yBarra = ch + 22;
    svg.append(sv('path', {class: 'seta', d: `M ${xDoSelo} ${ch + 1} V ${yBarra} H ${sw / 2}`}));
    p.saidas.forEach((s, i) => {
      const x = i * (sw + vao);
      svg.append(...seta(x + sw / 2, yBarra, x + sw / 2, yB - 1), clicavel(cartaoDoProcesso(s, 'saida', x, yB, sw, hB, null), abrir(s, 'saida')));
    });
    const xT = 4 * (cw + vao), wT = 2 * cw + vao;
    svg.append(...seta(xDoSelo, yBarra, xDoSelo, yB - 1), clicavel(cartaoDoProcesso(trilha, 'trilha', xT, yB, wT, hB, null), abrir(trilha, 'trilha')));
    H = yB + hB + 2;
  } else {
    const ch = 96, vao = 16;
    let y = 1;
    etapas.forEach((e, i) => {
      if (i) svg.append(...seta(W / 2, y - vao + 1, W / 2, y - 1));
      svg.append(clicavel(cartaoDoProcesso(e, 'etapa', 1, y, W - 2, ch, vivo), abrir(e, 'etapa')));
      y += ch + vao;
    });
    for (const s of [...p.saidas, trilha]) {
      svg.append(...seta(W / 2, y - vao + 1, W / 2, y - 1), clicavel(cartaoDoProcesso(s, s.id === 'trilha' ? 'trilha' : 'saida', 1, y, W - 2, 78, null), abrir(s, s.id === 'trilha' ? 'trilha' : 'saida')));
      y += 78 + vao;
    }
    H = y - vao + 2;
  }
  svg.setAttribute('width', W);
  svg.setAttribute('height', H);
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  alvo.append(svg, el('div', {class: 'legenda-do-diagrama'}, el('span', {class: 'l-codigo', text: 'feito em código'}), el('span', {class: 'l-modelo', text: 'feito pelo modelo de linguagem'}),
    el('span', {text: 'o que sai no fim'}), el('span', {text: 'clique num cartão para ampliar'})));
}

function fichasDoCenario(p) {
  const c = p && p.cenario, itens = [];
  if (c) {
    if (typeof c.segundos === 'number') itens.push(el('span', {class: 'ficha', title: 'do começo do roteiro ao fim da execução deste cenário'}, 'tempo total do cenário ', el('b', {text: tempoEmPalavras(c.segundos)})));
    if (typeof c.mttr_s === 'number') itens.push(el('span', {class: 'ficha', title: 'da detecção da falha ao diagnóstico conferido ou à reexecução validada'}, 'tempo de reparo ', el('b', {text: tempoEmPalavras(c.mttr_s)})));
    itens.push(el('span', {class: 'ficha ' + (c.task_success ? 'bom' : 'ruim'), title: 'Task Success: o agente chegou ao resultado certo nesta execução'}, c.task_success ? 'chegou ao resultado' : 'não chegou ao resultado'));
  }
  if (p && p.tempo_nao_gravado) itens.push(el('details', {class: 'nota-do-tempo'}, el('summary', {text: 'Por que algumas etapas estão sem tempo?'}), el('p', {class: 'nota', text: p.tempo_nao_gravado})));
  return itens;
}

// ---------------------------------------------------------------- o cartão ampliado

function barraH(rotulo, fracao, valor, destaque, alerta) {
  const cheio = el('div');
  cheio.style.width = (typeof fracao === 'number' ? Math.max(1, Math.round(Math.max(0, Math.min(1, fracao)) * 100)) : 0) + '%';
  return el('div', {class: 'barra-h' + (destaque ? ' destaque' : '') + (alerta ? ' alerta' : '')}, el('span', {class: 'rotulo-da-barra'}, rotulo), el('div', {class: 'trilho'}, cheio),
    el('span', {class: 'valor', text: valor}));
}

function linhaDaConferencia(x) {
  const passou = x.resultado === 'confere';
  return el('div', {class: 'conferencia' + (passou ? '' : ' nao')}, el('span', {}, x.alvo || 'conferência', passou ? '' : ' (não confere)'),
    x.esperado !== undefined && x.esperado !== null ? el('span', {class: 'regra', text: 'esperado ' + x.esperado + '; observado ' + x.observado}) : el('span', {class: 'regra', text: x.regra || ''}));
}

function corpoDoZoom(item, tipo, p) {
  const d = item.detalhe || {}, nos = [];
  const titulo = t => el('h3', {text: t});
  if (item.estado === 'pendente' || item.estado === 'em_andamento' || (tipo !== 'trilha' && item.estado !== 'nao_se_aplica' && !item.detalhe)) {
    nos.push(el('p', {class: 'nota', text: 'O detalhe desta etapa aparece quando o caso terminar e a corrida regravar a trilha.'}));
    return nos;
  }
  if (tipo === 'etapa' && item.tempo_de === 'marcas') {       // a corrida gravou a hora de cada etapa (decisão 176): o cartão diz o que o tempo cobre
    nos.push(el('p', {class: 'nota'}, 'Tempo pelo relógio da corrida: ' + (O_QUE_O_TEMPO_COBRE[item.id] || 'do começo ao fim da etapa') + '.'
      + (typeof item.tempo_pela_trilha_s === 'number' ? (item.id === 'roteiro' ? ' A soma dos passos, pela trilha, é ' : ' A inferência sozinha, pela trilha, é ')
        + tempoEmPalavras(item.tempo_pela_trilha_s) + '.' : '')));
  }
  if (tipo === 'trilha') {
    const abrir = el('button', {type: 'button', text: 'Abrir a trilha deste caso'});
    abrir.addEventListener('click', () => { fecharZoom(); if (E.caso) mostrarAba('trilha'); });
    nos.push(el('p', {}, p.trilha ? p.trilha.eventos + ' eventos gravados, um por passo. O código de conferência do conjunto é ' : '', p.trilha ? el('code', {text: p.trilha.hash}) : '', '.'), E.caso ? abrir : null);
    return nos;
  }
  if (item.estado === 'nao_se_aplica') return nos;
  if (item.id === 'roteiro') {
    const max = Math.max(1, ...d.passos.map(x => x.tempo_ms || 0));
    nos.push(titulo('Os passos e o tempo de cada um'), ...d.passos.map(x => barraH([String(x.passo || '') + ' ', el('code', {text: [x.acao, x.seletor].filter(Boolean).join(' ')})],
      (x.tempo_ms || 0) / max, typeof x.tempo_ms === 'number' ? tempoEmPalavras(x.tempo_ms / 1000) : 'sem tempo', false, x.falhou)));
    if (d.chamadas.length) nos.push(titulo('O que a página pediu à API'), el('div', {class: 'fichas'}, d.chamadas.map(x => el('span', {class: 'ficha'}, el('code', {text: x.metodo + ' ' + x.caminho}),
      ' status ' + x.status, typeof x.tempo_ms === 'number' ? el('b', {text: tempoEmPalavras(x.tempo_ms / 1000)}) : null))));
  } else if (item.id === 'deteccao') {
    if (d.erro) nos.push(titulo('O que o navegador disse'), el('pre', {}, el('code', {text: d.erro})));
    if (d.conferencias.length) nos.push(titulo('As conferências do roteiro'), ...d.conferencias.map(linhaDaConferencia));
  } else if (item.id === 'poda') {
    for (const x of d.itens) {
      nos.push(titulo('O que foi reduzido: ' + x.alvo), el('div', {class: 'fichas'}, el('span', {class: 'ficha'}, 'antes ', el('b', {text: x.antes_em_palavras})), el('span', {class: 'ficha bom'}, 'depois ', el('b', {text: x.depois_em_palavras}))));
      const regras = Object.entries(x.regras || {}).filter(([, n]) => typeof n === 'number'), max = Math.max(1, ...regras.map(([, n]) => n));
      nos.push(...regras.map(([nome, n]) => barraH(nome.replace(/_/g, ' '), n / max, String(n))));
    }
  } else if (item.id === 'busca') {
    const max = Math.max(1e-9, ...d.verbetes.map(v => v.pontuacao || 0)), sinais = Object.entries(d.sinais || {}).filter(([, v]) => v !== null && v !== undefined);
    if (sinais.length) nos.push(titulo('Os sinais do caso usados na busca'), el('div', {class: 'fichas'}, sinais.map(([k, v]) => el('span', {class: 'ficha'}, k + ' ', el('b', {text: String(v)})))));
    nos.push(titulo('Os verbetes mais bem pontuados (' + d.pontuados + ' pontuados, ' + d.k + ' entregues)'),
      ...d.verbetes.map(v => barraH(el('code', {text: v.id}), (v.pontuacao || 0) / max, comVirgula(v.pontuacao, 2) + (v.entregue ? ' · entregue' : ''), v.entregue)));
  } else if (item.id === 'modelo') {
    nos.push(titulo('As causas da lista e a probabilidade lida'),
      ...(d.alternativas.length ? d.alternativas.map(a => barraH(el('code', {text: a.opcao}), a.probabilidade, porcento(a.probabilidade), a.escolhida)) : [el('p', {class: 'nota', text: 'A resposta não trouxe alternativas.'})]));
    if (typeof d.prefill_s === 'number' && typeof d.geracao_s === 'number') {
      const p1 = el('div', {class: 'p1'}), p2 = el('div', {class: 'p2'}), total = d.prefill_s + d.geracao_s || 1;
      p1.style.width = (100 * d.prefill_s / total) + '%';
      p2.style.width = (100 * d.geracao_s / total) + '%';
      nos.push(titulo('Para onde foi o tempo'), el('div', {class: 'duas-partes'}, p1, p2), el('div', {class: 'fichas'},
        el('span', {class: 'ficha'}, 'lendo o caso ', el('b', {text: tempoEmPalavras(d.prefill_s)})), el('span', {class: 'ficha'}, 'escrevendo a resposta ', el('b', {text: tempoEmPalavras(d.geracao_s)})),
        el('span', {class: 'ficha'}, 'tokens lidos ', el('b', {text: String(d.tokens_entrada)})), el('span', {class: 'ficha'}, 'tokens escritos ', el('b', {text: String(d.tokens_saida)}))));
    }
    if (d.modelo) nos.push(el('p', {class: 'nota'}, 'Modelo: ', el('code', {text: d.modelo}), d.campo ? [' · campo apontado: ', el('code', {text: d.campo})] : ''));
  } else if (item.id === 'selo') {
    const c = d.conferencias;
    nos.push(el('div', {class: 'fichas'}, el('span', {class: 'ficha ' + (d.selo === 'alto' ? 'bom' : d.selo === 'baixo' ? 'ruim' : '')}, 'confiança ', el('b', {text: d.confianca || 'sem selo'})),
      typeof d.probabilidade === 'number' ? el('span', {class: 'ficha'}, 'probabilidade da causa ', el('b', {text: porcento(d.probabilidade)})) : null,
      d.divergencia ? el('span', {class: 'ficha ruim', text: 'o que o modelo declarou não bate com o que o código conferiu'}) : null,
      d.gatilhos.map(g => el('span', {class: 'ficha ruim', text: 'gatilho: ' + g.replace(/_/g, ' ')}))));
    if (c.total) nos.push(titulo('O que o código conferiu da resposta'), barraH('conferências que passaram', c.conferem / c.total, c.conferem + ' de ' + c.total, c.conferem === c.total, c.conferem !== c.total),
      ...c.itens.map(linhaDaConferencia));
    if (d.detalhe_da_divergencia) nos.push(el('p', {class: 'nota'}, comCodigo(d.detalhe_da_divergencia)));
  } else if (item.id === 'contrato') {
    const abrir = el('button', {type: 'button', text: 'Abrir o relatório'});
    abrir.addEventListener('click', () => { fecharZoom(); if (E.caso) mostrarAba('relatorio'); });
    nos.push(el('div', {class: 'fichas'}, el('span', {class: 'ficha'}, 'causa ', el('b', {text: d.causa_em_palavras || d.causa})), d.campo ? el('span', {class: 'ficha'}, 'campo ', el('b', {text: d.campo})) : null,
      d.confianca ? el('span', {class: 'ficha'}, 'confiança ', el('b', {text: d.confianca})) : null), E.caso ? abrir : null);
  } else if (item.id === 'localizador') {
    nos.push(el('div', {class: 'fichas'}, el('span', {class: 'ficha ' + (d.curado ? 'bom' : 'ruim'), text: d.curado ? 'localizador curado' : 'localizador não curado'}),
      d.estrategia ? el('span', {class: 'ficha'}, 'estratégia ', el('b', {text: d.estrategia})) : null, el('span', {class: 'ficha'}, 'candidatos testados ', el('b', {text: String(d.candidatos)})),
      typeof d.mttr_s === 'number' ? el('span', {class: 'ficha'}, 'tempo de reparo ', el('b', {text: tempoEmPalavras(d.mttr_s)})) : null,
      d.reexecucao ? el('span', {class: 'ficha'}, 'reexecução ', el('b', {text: d.reexecucao})) : null),
      el('p', {}, 'Antes: ', el('code', {text: d.localizador || ''}), d.seletor ? [' · depois: ', el('code', {text: d.seletor})] : ''));
  }
  return nos;
}

function abrirZoom(item, tipo, p) {
  $('#titulo-do-zoom').textContent = (item.numero ? item.numero + '. ' : '') + item.titulo;
  const tempo = tipo === 'etapa' ? tempoDaEtapa(item) : typeof item.tempo_s === 'number' ? 'reparo em ' + tempoEmPalavras(item.tempo_s) : '';
  $('#o-que-e-do-zoom').textContent = O_QUE_E[item.id] || '';
  $('#resumo-do-zoom').replaceChildren(tempo ? el('span', {class: 'ficha'}, el('b', {text: tempo})) : '', item.resumo ? ' ' + item.resumo : '');
  $('#corpo-do-zoom').replaceChildren(...corpoDoZoom(item, tipo, p).flat().filter(Boolean));
  $('#zoom-da-etapa').hidden = false;
  $('#fechar-zoom').focus();
}

function fecharZoom() { $('#zoom-da-etapa').hidden = true; }

// ---------------------------------------------------------------- a rede da decisão

function desenharRede(alvo, rede) {
  alvo.replaceChildren();
  if (!rede) return;
  const camadas = rede.camadas, W = Math.max(760, Math.floor(alvo.clientWidth || 900)), col = W / camadas.length, nw = Math.min(236, col - 44), nh = 46, passo = 58, topo = 34;
  const maior = Math.max(1, ...camadas.map(c => c.nos.length)), H = topo + maior * passo + 6, pos = {};
  camadas.forEach((c, i) => c.nos.forEach((n, j) => { pos[n.id] = {x: i * col + (col - nw) / 2, y: topo + (maior - c.nos.length) * passo / 2 + j * passo, n, camada: c.id}; }));
  const svg = sv('svg', {width: W, height: H, viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Rede da decisão: dos sinais do caso aos verbetes, às causas possíveis e ao resultado'});
  camadas.forEach((c, i) => {
    svg.append(sv('text', {class: 'titulo-da-camada', x: i * col + col / 2, y: 16, text: c.titulo}));
    if (!c.nos.length) svg.append(sv('text', {class: 'vazio-da-camada', x: i * col + col / 2, y: topo + maior * passo / 2, text: 'nada registrado'}));
  });
  for (const a of rede.arestas) {
    const de = pos[a.de], para = pos[a.para];
    if (!de || !para) continue;
    const x1 = de.x + nw, y1 = de.y + nh / 2, x2 = para.x, y2 = para.y + nh / 2, m = (x1 + x2) / 2;
    svg.append(sv('path', {class: 'aresta' + (de.n.destaque && para.n.destaque ? ' destaque' : ''), d: `M ${x1} ${y1} C ${m} ${y1}, ${m} ${y2}, ${x2} ${y2}`, 'stroke-width': (1 + 5 * a.peso).toFixed(1)}));
  }
  const caracteres = Math.max(8, Math.floor((nw - 16) / 6.7));
  for (const {x, y, n, camada} of Object.values(pos)) {
    const teto = Math.max(1e-9, ...camadas.find(c => c.id === camada).nos.map(o => o.valor || 0));
    const valor = typeof n.valor !== 'number' ? (n.nota || '') : camada === 'verbetes' ? 'pontuação ' + comVirgula(n.valor, 2) : porcento(n.valor) + (n.nota ? ' · ' + n.nota : '');
    const fracao = typeof n.valor !== 'number' ? null : camada === 'verbetes' ? n.valor / teto : n.valor;
    svg.append(sv('g', {class: 'no' + (n.destaque ? ' destaque' : ''), data: {no: n.id}},
      sv('title', {text: n.rotulo + (valor ? ' (' + valor + ')' : '')}), sv('rect', {x, y, width: nw, height: nh, rx: 8}),
      sv('text', {class: 'rotulo-do-no', x: x + 8, y: y + (valor ? 18 : 27), text: curto(n.rotulo, caracteres)}),
      valor ? sv('text', {class: 'valor-do-no', x: x + 8, y: y + 33, text: curto(valor, caracteres + 4)}) : null,
      fracao !== null ? [sv('rect', {class: 'medida-trilho', x: x + 8, y: y + nh - 8, width: nw - 16, height: 3, rx: 1.5}),
        sv('rect', {class: 'medida-cheia', x: x + 8, y: y + nh - 8, width: Math.max(2, (nw - 16) * Math.max(0, Math.min(1, fracao))), height: 3, rx: 1.5})] : null));
  }
  alvo.append(svg, el('p', {class: 'nota', text: 'Em destaque, o caminho que o agente seguiu. A espessura da linha acompanha a pontuação do verbete ou a probabilidade da causa.'}));
}

// ---------------------------------------------------------------- os espaços de trabalho

const NOS_DO_WORKSPACE = [
  {id: 'analista', nome: 'Analista de QA', sub: 'revisa e dá o veredito', x: 1, y: 118},
  {id: 'hub', nome: 'Hub central', sub: 'esta página', x: 233, y: 118, servico: 'hub'},
  {id: 'agente', nome: 'Agente', sub: 'executor em Python', x: 465, y: 118, classe: 'centro'},
  {id: 'navegador', nome: 'Navegador', sub: 'Chromium do Playwright', x: 697, y: 14},
  {id: 'site', nome: 'Site de demonstração', sub: 'porta 8080', x: 929, y: 14, servico: 'site'},
  {id: 'api', nome: 'API do site', sub: 'porta 8000', x: 929, y: 118, servico: 'api'},
  {id: 'banco', nome: 'Banco de dados', sub: 'MariaDB', x: 929, y: 222},
  {id: 'ollama', nome: 'Modelo local', sub: 'Ollama, só com CPU', x: 697, y: 118, servico: 'ollama', classe: 'do-modelo'},
  {id: 'biblioteca', nome: 'Biblioteca', sub: 'verbetes de documentação', x: 697, y: 222},
  {id: 'registros', nome: 'Trilha e relatórios', sub: 'o que cada corrida grava', x: 465, y: 222}];
const LIGACOES_DO_WORKSPACE = [['analista', 'hub', 'abre'], ['hub', 'agente', 'manda rodar'], ['agente', 'navegador', 'roteiro'], ['navegador', 'site', 'abre a tela'],
  ['site', 'api', 'chama'], ['api', 'banco', 'lê e grava'], ['agente', 'ollama', 'diagnóstico'], ['agente', 'biblioteca', 'verbetes'], ['agente', 'registros', 'grava'],
  ['registros', 'hub', 'lê']];

function desenharWorkspaces(alvo, central) {
  const W = 1090, H = 296, nw = 160, nh = 60, porId = {}, servicos = {};
  for (const s of central.servicos) servicos[s.id] = s;
  for (const n of NOS_DO_WORKSPACE) porId[n.id] = n;
  const svg = sv('svg', {viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: 'img', 'aria-label': 'Como as peças se ligam: quem usa, o hub, o agente, o navegador, o site, a API, o banco, o modelo local e a biblioteca'});
  for (const [de, para, rotulo] of LIGACOES_DO_WORKSPACE) {
    const a = porId[de], b = porId[para];
    let x1, y1, x2, y2;
    if (a.y === b.y) { x1 = a.x < b.x ? a.x + nw : a.x; x2 = a.x < b.x ? b.x : b.x + nw; y1 = y2 = a.y + nh / 2; }
    else if (a.x === b.x) { x1 = x2 = a.x + nw / 2; y1 = a.y < b.y ? a.y + nh : a.y; y2 = a.y < b.y ? b.y : b.y + nh; }
    else { x1 = a.x < b.x ? a.x + nw : a.x; y1 = a.y + nh / 2 + (b.y < a.y ? -14 : 14); x2 = a.x < b.x ? b.x : b.x + nw; y2 = b.y + nh / 2; }
    const emPe = x1 === x2;       // na ligação em pé o rótulo vai ao lado da linha; nas outras, acima do meio dela
    svg.append(sv('g', {class: 'ligacao', data: {de, para}}, ...seta(x1, y1, x2, y2)),
      sv('text', {class: 'rotulo-da-ligacao', x: emPe ? x1 + 7 : (x1 + x2) / 2, y: (y1 + y2) / 2 + (emPe ? 4 : -6), 'text-anchor': emPe ? 'start' : 'middle', text: rotulo}));
  }
  for (const n of NOS_DO_WORKSPACE) {
    const s = n.servico ? servicos[n.servico] : null, estado = s ? (s.no_ar ? 'no ar' : 'fora do ar') : '';
    const g = sv('g', {class: 'no ws' + (n.classe ? ' ' + n.classe : '') + (s ? (s.no_ar ? ' no-ar' : ' fora-do-ar') : ''), data: {no: n.id}},
      sv('title', {text: n.nome + (estado ? ': ' + estado : '') + (s && s.url ? ' (' + s.url + ')' : '')}), sv('rect', {x: n.x, y: n.y, width: nw, height: nh, rx: 10}),
      sv('text', {class: 'nome-do-no', x: n.x + 10, y: n.y + 22, text: n.nome}), sv('text', {class: 'sub-do-no', x: n.x + 10, y: n.y + 39, text: n.sub}),
      estado ? sv('text', {class: 'estado-do-no', x: n.x + 10, y: n.y + 54, text: estado}) : null);
    svg.append(s && s.url ? sv('a', {href: s.url, target: '_blank', rel: 'noopener noreferrer'}, g) : g);
  }
  alvo.replaceChildren(svg);
}

// ---------------------------------------------------------------- os gráficos de barras

function graficoDeBarras(alvo, itens, classe, rotuloDoGrafico) {
  alvo.replaceChildren();
  if (!itens.length) return;
  const W = Math.max(280, Math.floor(alvo.clientWidth || 700)), estreito = W < 560, rw = estreito ? 0 : Math.min(250, Math.round(W * 0.3)), vw = estreito ? 120 : 170;
  const bx = estreito ? 0 : rw + 10, bw = Math.max(40, W - bx - vw), alt = estreito ? 48 : 30, max = Math.max(1e-9, ...itens.map(i => i.valor || 0));
  const svg = sv('svg', {width: W, height: itens.length * alt + 2, viewBox: `0 0 ${W} ${itens.length * alt + 2}`, role: 'group', 'aria-label': rotuloDoGrafico});
  itens.forEach((it, k) => {
    const y = k * alt + 1, by = estreito ? y + 22 : y + 5, bh = 18;
    const g = sv('g', {class: classe + (it.classe ? ' ' + it.classe : '') + (it.destaque ? ' destaque' : ''), data: it.data || {}, 'aria-label': it.rotulo + ': ' + it.texto},
      sv('title', {text: it.dica || (it.rotulo + ': ' + it.texto)}),
      sv('text', {class: 'rotulo-do-grafico', x: estreito ? 0 : rw, y: estreito ? y + 15 : by + 13, 'text-anchor': estreito ? 'start' : 'end', text: curto(it.rotulo, estreito ? 44 : Math.floor(rw / 6.6))}),
      sv('rect', {class: 'trilho-do-grafico', x: bx, y: by, width: bw, height: bh, rx: 4}));
    if (it.partes) {
      let x = bx;
      const total = it.partes.reduce((s, p) => s + p.n, 0) || 1;
      for (const p of it.partes) { const w = bw * p.n / total; g.append(sv('rect', {class: p.classe, x, y: by, width: w, height: bh})); x += w; }
    } else if (typeof it.valor === 'number') g.append(sv('rect', {class: 'cheio-do-grafico', x: bx, y: by, width: Math.max(2, bw * it.valor / max), height: bh, rx: 4}));
    g.append(sv('text', {class: 'valor-do-grafico', x: bx + bw + 8, y: by + 13, text: it.texto}));
    svg.append(it.aoClicar ? clicavel(g, it.aoClicar) : g);
  });
  alvo.append(svg);
}

// ---------------------------------------------------------------- a ligação dos diagramas com as vistas da página

function desenharProcessoDoCaso() {
  if (!E.caso) return;
  desenharProcesso($('#processo-do-caso'), E.caso.processo, null);
  $('#resumo-do-processo').replaceChildren(...fichasDoCenario(E.caso.processo));
}

// ! Alteração de IA - Revisar: (26/11/2026, ficha 114, decisão 176) a linha de produção ao vivo acende a etapa que o servidor diz estar rodando, qualquer
// das seis, e mostra o tempo das que o caso em andamento já passou (`tempos_agora`), quando a corrida grava a hora de cada etapa.
// ! Motivo: até aqui só a etapa do modelo podia aparecer acesa, porque era a única que a corrida avisava. Numa corrida sem as marcas, o desenho
// continua como era: a etapa do modelo acesa durante a inferência e as de antes dela dadas como concluídas, sem tempo.
function desenharLinhaAoVivo(v) {
  const alvo = $('#linha-de-producao'), frase = $('#caso-ao-vivo');
  if (!v.ha_corrida) {
    alvo.replaceChildren();
    frase.textContent = 'Nenhuma corrida gravou o estado dela nesta pasta de resultados.';
    E.linhaAoVivo = null;
    return;
  }
  const u = v.ultimo_diagnostico, pg = v.progresso || {}, agora = v.etapa_agora, ordem = ETAPAS_EM_BRANCO.map(x => x[0]), numero = ordem.indexOf(agora) + 1;
  let p, vivo = null;
  if (agora) {
    const noModelo = agora === 'modelo';
    if (numero) {
      vivo = {etapa: agora, fracao: noModelo && typeof pg.fracao === 'number' ? pg.fracao : null,
        resumo: noModelo ? (pg.fase === 'prefill' ? 'lendo o caso' : 'escrevendo a resposta') + (typeof pg.decorrido_s === 'number' ? ', há ' + segundos(pg.decorrido_s) : '') : ''};
    }
    if (u && u.processo && v.caso_agora && u.tid.endsWith('/' + v.caso_agora)) p = u.processo;
    else {        // o caso em andamento ainda não está na trilha: as etapas que já passaram entram com o tempo das marcas, e o detalhe vem quando ele terminar
      p = processoEmBranco();
      const tempos = v.tempos_agora || {};
      for (const e of p.etapas) {
        if (numero && e.numero >= numero) continue;
        e.estado = 'feita';
        e.resumo = 'o detalhe aparece quando o caso terminar';
        if (typeof tempos[e.id] === 'number') e.tempo_s = tempos[e.id]; else e.sem_detalhe = true;
      }
    }
    frase.textContent = 'Agora, no caso ' + (v.caso_agora || 'em andamento') + ': '
      + (numero ? ETAPAS_EM_BRANCO[numero - 1][1].toLowerCase() : 'fechando o caso, com o relatório ou a cura')
      + (noModelo && typeof pg.fracao === 'number' ? ' (' + Math.round(pg.fracao * 100) + '% do tempo estimado)' : '') + '.';
  } else {
    p = u && u.processo ? u.processo : processoEmBranco();
    frase.textContent = u ? 'Último caso diagnosticado: ' + u.nome + '. Nenhuma etapa está rodando agora, ou a corrida não grava em que etapa está fora da inferência do modelo.'
      : 'A corrida ainda não gravou nenhum diagnóstico.';
  }
  const assinatura = JSON.stringify([v.pasta, agora, v.caso_agora, pg.fracao, pg.fase, v.tempos_agora, u && u.tid, v.diagnosticos, alvo.clientWidth]);
  if (E.linhaAoVivo && E.linhaAoVivo.assinatura === assinatura) return;     // nada mudou desde a última leitura: o desenho fica como está
  E.linhaAoVivo = {p, vivo, assinatura};
  desenharProcesso(alvo, p, vivo);
}

function abrirGrupoDoCaso(tid) {
  const c = E.porTid[tid];
  if (!c) return;
  const g = estadoDoGrupo(c.corrida), posicao = E.indice.casos.filter(x => x.corrida === c.corrida).findIndex(x => x.tid === tid);
  if (g.aberto && posicao < g.limite) return;
  g.aberto = true;
  g.limite = Math.max(g.limite, posicao + 1);
  filtrar();
}

function redesenharDiagramas() {
  if (E.vista === 'casos' && E.caso) {
    desenharProcessoDoCaso();
    if (E.aba === 'arvore') desenharRede($('#rede-da-decisao'), E.caso.processo.rede);
  }
  if (E.vista === 'ao-vivo' && E.linhaAoVivo) desenharProcesso($('#linha-de-producao'), E.linhaAoVivo.p, E.linhaAoVivo.vivo);
  if (E.vista === 'metricas' && E.metricas) desenharMetricas();
}
"""
