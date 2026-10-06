#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (01/10/2026) que integra ao Memorial a rodada 5 da pesquisa, a da Pré-Fase 4,
# feita em duas partes por Workflow (A: o repositório colibri, as pesquisas que ele cita, inferência com os pesos fora
# da RAM, MoE pequenos em CPU e atlas de especialistas; B: raciocínio aberto). Grava
# `levantamento-2026-10-01-pre-fase-4.md` (§6.14.1 a §6.14.11, uma subseção por tópico já pesquisado; §6.14.12
# rejeitadas com o motivo; §6.14.13 mapas adotado, adiado, descartado), o bloco de referências novas em
# `referencias.md` (sem repetir as que já constam, com o total recontado) e a linha no índice do Memorial; `--check`
# regera os três e compara.
# ! Motivo: pedido do Eric em 01/10/2026 (decisão 70): análise densa do colibri e das pesquisas em que ele se baseia, a
# validação do "expert atlas" e a pesquisa sobre o raciocínio aberto. Mesmo desenho das rodadas 3 e 4
# (integrar_pesquisa_llms.py e integrar_pesquisa_documentacao.py): o texto das sínteses entra por script, nunca colado
# à mão, e o que foi rejeitado fica com o motivo. Quatro coisas são próprias desta rodada: (1) a numeração é fixa para
# os onze tópicos, de modo que integrar a parte B depois não muda o número de nenhuma subseção já citada; (2) o
# contexto que dei aos agentes da parte A dizia que o prompt do agente tem "alguns milhares de tokens", e o valor
# medido é outro: o script troca a expressão pelo número lido de viabilidade_modelos_grandes.json e declara a troca no
# cabeçalho do arquivo gerado; (3) o bloco de referências e a linha do índice são regravados inteiros a cada
# integração, em vez de "já existe, não regravo", porque a parte B acrescenta referências ao mesmo bloco; (4) o texto
# que o script escreve não usa travessão nem seta (o cabeçalho de cada subseção mantém o formato fixo da regra de
# documentação, que o painel lê, e os títulos e citações literais das fontes ficam como na fonte).
"""Uso:
    python ferramentas/integrar_pesquisa_pre_fase4.py [--simular]     (integra ao Memorial as partes que já rodaram)
    python ferramentas/integrar_pesquisa_pre_fase4.py --check
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import integrar_pesquisa_llms as ipl  # noqa: E402
import render_levantamento as rl  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = rl.RAIZ
DOC_DIR = RAIZ / "Documentacao" / "memorial"
LEVANTAMENTO = DOC_DIR / "2-pesquisa-e-literatura" / "levantamento-2026-10-01-pre-fase-4.md"
MEMORIAL = RAIZ / "Documentacao" / "Memorial de Desenvolvimento.md"
SDD = RAIZ / ".superpowers" / "sdd" / "pre-fase-4"
PARTES = [("A", SDD / "pesquisa" / "r5a-final.json"), ("B", SDD / "pesquisa" / "r5b-final.json")]
VIABILIDADE = RAIZ / "Programacao" / "AgenteCore" / "experimentos" / "resultados_alvo" / "pre_fase4" / "viabilidade_modelos_grandes.json"
ROTULO = "levantamento de 01/10/2026"
TITULO_REFS = f"### Levantamento da Pré-Fase 4 ({ROTULO})"
MARCA_DO_INDICE = "- [Levantamento: Pré-Fase 4 (01/10/2026)]"
TAG_DO_INDICE = "<!-- ! Alteração de IA - Revisar: linha do índice para o levantamento da Pré-Fase 4"
TETO = 16

# Parte da rodada e título curto de cada tópico, na ordem (fixa) das subseções §6.14.1 a §6.14.11.
TITULOS_R5 = {
    "r5-colibri-leitura-integral": ("A", "O repositório colibri: o que roda, em que máquina e a que velocidade"),
    "r5-base-de-pesquisa-do-colibri": ("A", "As pesquisas em que o colibri se apoia"),
    "r5-pesos-em-disco": ("A", "Inferência com os pesos fora da RAM"),
    "r5-moe-pequenos-em-cpu": ("A", "Modelos MoE que cabem em 16 GB e rodam em CPU"),
    "r5-atlas-e-especializacao": ("A", "Atlas de especialistas, análise de roteamento e visualização de competências"),
    "r5-fidelidade-do-raciocinio": ("B", "O raciocínio escrito é o que decidiu a resposta?"),
    "r5-trilha-e-observabilidade": ("B", "Formatos de trilha e exigências de registro"),
    "r5-relatorio-para-humanos": ("B", "Relatório de raciocínio para quem desenvolve"),
    "r5-atribuicao-ao-contexto": ("B", "Que trecho do contexto causou a resposta"),
    "r5-confianca-por-probabilidade": ("B", "A probabilidade do rótulo como sinal de incerteza"),
    "r5-uso-das-trilhas": ("B", "Usar as trilhas para melhorar o sistema"),
}
ORDEM_R5 = tuple(TITULOS_R5)
N_REJ = len(ORDEM_R5) + 1
N_MAPA = len(ORDEM_R5) + 2
NOME_DO_MAPA = {"A": "Parte A: viabilidade nesta máquina (modelos grandes pelo disco e atlas)",
                "B": "Parte B: raciocínio aberto (trilha, relatório, confiança)"}
# "alguns milhares de tokens" e "milhares de tokens" quando falam do prompt do agente; "dezenas de milhares" e
# "centenas de milhares" são medidas de fontes e ficam como estão.
_EXPRESSAO_DO_CONTEXTO = re.compile(r"(?<!dezenas de )(?<!centenas de )(?:alguns )?milhares de tokens")
# Correções feitas depois da revisão das sínteses e do mapa contra as afirmações verificadas (um revisor por tópico e um
# para o mapa, em 01/10/2026). Cada item: `onde` (a chave do tópico, ou `mapa:A`), `de` (o trecho como o agente
# escreveu, que tem de aparecer exatamente uma vez), `para` (o trecho corrigido) e `motivo` (o que a afirmação
# verificada sustenta). A lista vive em correcoes_pesquisa_pre_fase4.py (são dados, não código) e sai declarada no
# cabeçalho e no fim do §6.14.12 do levantamento.
# ! Alteração de IA - Revisar: (05/10/2026) a lista de correções passou a vir de um módulo próprio, e o cabeçalho ganhou
# o aviso sobre a memória da máquina (instalada contra visível) e a medida do prefill, lidos do JSON de viabilidade.
# ! Motivo: a revisão de 01/10 apontou 104 trechos; 156 correções declaradas não cabem neste arquivo sem esconder o
# código. O aviso da memória existe porque o contexto dado aos agentes dizia "15,69 GB de RAM" (o que o Windows
# enxerga) e várias frases comparavam a RAM livre com o mínimo de 16 GB do colibri; a máquina tem 16 GB instalados, e
# é com a instalada que o mínimo se compara. A medida do prefill existe porque as sínteses diziam que "o prefill
# domina o custo" como se fosse das fontes: é fato dos registros da Fase 3, e passa a ser declarado com o número.
from correcoes_pesquisa_pre_fase4 import CORRECOES_DA_REVISAO, DATA_DAS_CORRECOES  # noqa: E402


def _plural(n: int, um: str, muitos: str) -> str:
    return f"{n} {um if n == 1 else muitos}"


_POR_EXTENSO = {4: "Quatro", 5: "Cinco", 6: "Seis"}


def _br(v: float, casas: int = 1) -> str:
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ------------------------------------------------------------------ carga e correções declaradas

def forma_do_tamanho(mediana: float) -> str:
    """A forma em que o tamanho medido do prompt entra no texto: arredondado para a centena."""
    return f"cerca de {int(round(mediana, -2)):,} tokens".replace(",", ".")


def medidas_do_projeto() -> dict:
    """As medidas do projeto que o cabeçalho declara, lidas de viabilidade_modelos_grandes.json: as medianas do agente
    (360 diagnósticos da Fase 3: tokens do prompt e da resposta, segundos de prefill e de geração), a forma em que o
    tamanho do prompt entra no texto, e a memória da máquina (instalada, visível ao sistema e livre no início de uma
    corrida)."""
    v = json.loads(VIABILIDADE.read_text(encoding="utf-8"))
    m, maq = v["medianas_do_agente"], v["maquina"]
    return {"mediana": m["tokens_entrada"], "saida": m["tokens_saida"], "n": m["n"], "texto": forma_do_tamanho(m["tokens_entrada"]),
            "prefill_s": m["prefill_ms"] / 1000, "geracao_s": m["geracao_ms"] / 1000,
            "ram_instalada_gb": maq["ram_instalada_gb"], "ram_visivel_gb": maq["ram_gb"], "ram_livre_gb": maq["ram_livre_no_inicio_de_corrida_gb"]}


def corrigir(texto: str, novo: str) -> tuple[str, int]:
    """Troca a expressão do contexto dado aos agentes pelo tamanho medido; devolve o texto e quantas trocas fez."""
    return _EXPRESSAO_DO_CONTEXTO.subn(novo, texto or "")


def _sem_seta(texto: str) -> str:
    """Faixa de números escrita pelo verificador com seta ("3,69→4,18") passa a "3,69 para 4,18"."""
    return re.sub(r"\s*→\s*", " para ", texto or "")


def carregar(partes: list[tuple[str, Path]] | None = None, medida: dict | None = None) -> tuple[dict, dict, int]:
    """Lê as partes da rodada que já rodaram. Devolve {key: tópico}, {parte: mapa} e quantas vezes a expressão do
    contexto foi trocada pelo número medido nos textos que entram no documento."""
    novo = (medida or medidas_do_projeto())["texto"]
    trocas = 0

    def troca(texto: str) -> str:
        nonlocal trocas
        corrigido, n = corrigir(texto, novo)
        trocas += n
        return corrigido

    topicos, mapas = {}, {}
    for parte, arq in partes or PARTES:
        if not arq.exists():
            continue
        dado = json.loads(arq.read_text(encoding="utf-8"))
        dado = dado.get("result", dado)
        for t in dado.get("topicos") or []:
            if not t:
                continue
            # o Workflow separa em lista própria o que passou do teto; o renderizador reconhece a frase dentro de `rejeitadas`
            for r in t.pop("alem_do_teto", []) or []:
                t.setdefault("rejeitadas", []).append({**r, "motivo": f"além do teto de {TETO} verificações: não verificada"})
            s = t.get("synthesis") or {}
            if s.get("texto_memorial_pt"):
                s["texto_memorial_pt"] = troca(s["texto_memorial_pt"])
            for campo in ("implicacoes_fase3_pt", "lacunas_pt"):
                if s.get(campo):
                    s[campo] = [troca(x) for x in s[campo]]
            for v in t.get("verified") or []:
                if v.get("support") == "partial":  # só as parciais aparecem no documento (§6.14.12)
                    v["claim_pt"], v["number"] = _sem_seta(troca(v.get("claim_pt", ""))), _sem_seta(str(v.get("number", "")))
            for r in t.get("rejeitadas") or []:
                r["claim"] = _sem_seta(troca(r.get("claim", "")))
            topicos[t["key"]] = t
        m = dado.get("mapa") or {}
        if m:
            for linha in m.get("linhas") or []:
                linha["motivo_pt"] = troca(linha["motivo_pt"])
            for r in m.get("riscos") or []:
                r["risco"], r["mitigacao"] = troca(r["risco"]), troca(r["mitigacao"])
            m["leitura_pt"] = troca(m.get("leitura_pt") or "")
            mapas[parte] = m
    desconhecidos = sorted(set(topicos) - set(ORDEM_R5))
    if desconhecidos:
        raise SystemExit(f"tópico(s) fora da lista da rodada 5: {desconhecidos}")
    aplicar_correcoes(topicos, mapas, CORRECOES_DA_REVISAO)
    return topicos, mapas, trocas


def _campos_de_texto(dados: dict, mapas: dict, onde: str) -> list[tuple]:
    """Os lugares em que o texto de um tópico (ou de um mapa, `mapa:A`) entra no documento, como pares (objeto, chave)."""
    if onde.startswith("mapa:"):
        m = mapas.get(onde.split(":", 1)[1])
        if not m:
            return []
        return ([(l, "motivo_pt") for l in m.get("linhas") or []] + [(r, k) for r in m.get("riscos") or [] for k in ("risco", "mitigacao")] + [(m, "leitura_pt")])
    s = (dados.get(onde) or {}).get("synthesis") or {}
    campos = [(s, "texto_memorial_pt")] if s.get("texto_memorial_pt") else []
    for nome in ("implicacoes_fase3_pt", "lacunas_pt"):
        campos += [(s[nome], i) for i in range(len(s.get(nome) or []))]
    return campos


def aplicar_correcoes(dados: dict, mapas: dict, correcoes: list[dict]) -> int:
    """Aplica as correções da revisão: cada uma troca um trecho que aparece exatamente uma vez no texto do tópico (ou
    do mapa) indicado. Trecho ausente ou repetido interrompe, para uma correção velha não passar calada depois de o
    texto de origem mudar."""
    for c in correcoes:
        campos = _campos_de_texto(dados, mapas, c["onde"])
        vezes = sum(obj[k].count(c["de"]) for obj, k in campos)
        if vezes != 1:
            raise SystemExit(f"correção em {c['onde']}: o trecho \"{c['de'][:70]}\" aparece {vezes} vez(es) no texto; tem de aparecer exatamente uma")
        for obj, k in campos:
            if c["de"] in obj[k]:
                obj[k] = obj[k].replace(c["de"], c["para"])
                break
    return len(correcoes)


# ------------------------------------------------------------------ render

def secao_r5(key: str, item: dict) -> str:
    rl.TITULOS_CURTOS.setdefault(key, TITULOS_R5[key][1])
    texto = rl.secao(ORDEM_R5.index(key) + 1, key, item)
    texto = texto.replace("#### 6.9.", "#### 6.14.", 1)
    return texto.replace("##### Implicações para a Fase 3", "##### Implicações para o agente local e a Fase 4", 1)


def bloco_rejeitadas(dados: dict, correcoes: list[dict] | None = None) -> str:
    partes = [f"#### 6.14.{N_REJ} Afirmações rejeitadas, não verificadas ou de suporte parcial (com o motivo)", "",
              "Cada linha é uma afirmação que um pesquisador trouxe e o verificador cético não confirmou (fonte inexistente, ano anterior a 2024 sem ser clássica, número ou "
              f"condição que a fonte não sustenta, fonte que não abriu) ou que ficou além do teto de {TETO} verificações por tópico. Nenhuma delas entrou nas sínteses. As de "
              "suporte parcial entraram com o número que a fonte de fato sustenta, e aparecem aqui para a correção ser rastreável.", ""]
    for k in ORDEM_R5:
        it = dados.get(k)
        if not it:
            continue
        rej = [r for r in (it.get("rejeitadas") or []) if not rl.eh_alem_do_teto(r)]
        teto = [r for r in (it.get("rejeitadas") or []) if rl.eh_alem_do_teto(r)]
        parciais = [v for v in (it.get("verified") or []) if v.get("support") == "partial"]
        if not rej and not parciais and not teto:
            continue
        partes.append(f"*`{k}`*: {_plural(len(rej), 'rejeitada', 'rejeitadas')}, {_plural(len(parciais), 'parcial', 'parciais')}, "
                      f"{_plural(len(teto), 'não verificada', 'não verificadas')}")
        for r in rej:
            partes.append(f"- Rejeitada: {r.get('claim', '')} *Fonte declarada:* {r.get('fonte', '')} *Motivo:* {r.get('motivo', '')}")
        for r in teto:
            partes.append(f"- Não verificada: {r.get('claim', '')} *Fonte declarada:* {r.get('fonte', '')} *Motivo:* {r.get('motivo', '')}")
        for v in parciais:
            partes.append(f"- Parcial: {v.get('claim_pt', '')} *Número que a fonte sustenta:* {v.get('number', '')} *Ref.:* {v.get('ref', '')}")
        partes.append("")
    correcoes = CORRECOES_DA_REVISAO if correcoes is None else correcoes
    if correcoes:
        partes += ["**Correções feitas depois da revisão**", "",
                   "Depois de integradas, as sínteses e o mapa foram conferidos contra as afirmações verificadas, um revisor por tópico e um para o mapa. Cada linha é um trecho "
                   f"corrigido por script em {DATA_DAS_CORRECOES}: onde estava, como ficou e o motivo. O texto das subseções já traz a forma corrigida.", ""]
        for c in correcoes:
            lugar = NOME_DO_MAPA.get(c["onde"].split(":", 1)[1], c["onde"]) if c["onde"].startswith("mapa:") else f"`{c['onde']}`"
            partes.append(f"- {lugar}: onde estava \"{c['de']}\", passou a \"{c['para']}\". *Motivo:* {c['motivo']}")
        partes.append("")
    return "\n".join(partes)


def bloco_mapas(mapas: dict) -> str:
    partes = [f"#### 6.14.{N_MAPA} Mapas adotado / adiado / descartado", "",
              "Um mapa por parte da rodada, escrito por um agente a partir das sínteses e das afirmações verificadas. *Adotado* = serve agora, nesta máquina, sem trocar o modelo "
              "decidido; *adiado* = só serviria com outra máquina, outro motor ou depois da Fase 4; *descartado* = não serve, com o motivo.", ""]
    for parte, _ in PARTES:
        m = mapas.get(parte)
        partes += [f"**{NOME_DO_MAPA[parte]}**", ""]
        if not m:
            partes += ["Esta parte da rodada ainda não rodou.", ""]
            continue
        partes += [ipl.tabela_mapa(m), "", "**Riscos**", "", "| Risco | Mitigação | Fonte |", "|---|---|---|"]
        partes += [f"| {ipl._cel(r['risco'])} | {ipl._cel(r['mitigacao'])} | {ipl._cel(r['fonte'])} |" for r in m.get("riscos", [])]
        partes += ["", "**Leitura**", "", (m.get("leitura_pt") or "").strip(), ""]
    return "\n".join(partes)


def cabecalho(dados: dict, trocas: int, medida: dict, correcoes: list[dict] | None = None) -> str:
    correcoes = CORRECOES_DA_REVISAO if correcoes is None else correcoes
    cont = [(k, *rl.contagem(dados[k])) if k in dados else (k, None, None, None) for k in ORDEM_R5]
    feitos = [c for c in cont if c[1] is not None]
    tot = [sum(c[i] for c in feitos) for i in (1, 2, 3)]
    saida = medida.get("saida")
    razao = f" Com o número medido as conclusões que dependiam da ordem de grandeza continuam valendo: a entrada é cerca de {round(medida['mediana'] / saida)} vezes os {_br(saida, 0)} tokens da resposta mediana." if saida else ""
    linhas = [
        "<!-- ! Alteração de IA - Revisar: arquivo gerado por ferramentas/integrar_pesquisa_pre_fase4.py a partir dos resultados dos Workflows da rodada 5 de pesquisa (01/10/2026). NÃO editar as subseções à mão (o --check compara com o regerado).",
        "     ! Motivo: levantamento pedido pelo Eric em 01/10/2026 (decisão 70, Pré-Fase 4): a viabilidade do repositório colibri e das pesquisas em que ele se apoia, o que é o \"expert atlas\" e como abrir o raciocínio do agente. Cada afirmação passou por verificação cética, e o que foi rejeitado ou descartado fica registrado com o motivo (§6.14.12 e §6.14.13). -->",
        "", "# Levantamento bibliográfico: Pré-Fase 4 (01/10/2026)", "",
        "Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Continua o [levantamento da Fase 3](levantamento-2026-09-11-fase-3.md) (§6.9), o "
        "[mapa de decisões](mapa-de-decisoes-fase-3.md) (§6.10), o [levantamento das LLMs locais](levantamento-2026-09-22-llms-locais.md) (§6.12) e o "
        "[da documentação autogerida](levantamento-2026-09-29-documentacao-autogerida.md) (§6.13). O que motivou: o Eric abriu uma fase de pesquisa antes da Fase 4 com três "
        "frentes: rodar modelo grande lendo os pesos do disco (repositório `github.com/JustVugg/colibri`), o atlas visual de especialistas e o raciocínio aberto do agente "
        "([roadmap](../roadmap.md), §3.1). Referências completas em [referencias.md](referencias.md).",
        "", "### 6.14 Levantamento da Pré-Fase 4", "",
        f"Onze tópicos em duas partes, cada parte num Workflow: um pesquisador por tópico (10 a 16 afirmações com número e condição), verificadores céticos em lotes de quatro "
        f"afirmações, até {TETO} por tópico (a fonte existe? o ano vale? o número e a condição batem?), e uma síntese só com o que sobreviveu. "
        f"Totais do que já rodou: **{_plural(tot[0], 'aprovada', 'aprovadas')}, {_plural(tot[1], 'rejeitada', 'rejeitadas')}, {_plural(tot[2], 'não verificada', 'não verificadas')}**.",
        "", "| Subseção | Parte | Tópico | Aprovadas | Rejeitadas | Não verificadas |", "|---|---|---|---|---|---|",
    ]
    for i, (k, a, r, t) in enumerate(cont, 1):
        parte = TITULOS_R5[k][0]
        linhas.append(f"| §6.14.{i} | {parte} | `{k}` | {a} | {r} | {t} |" if a is not None else f"| §6.14.{i} | {parte} | `{k}` | ainda não rodou | | |")
    # o prefill e a memória só entram quando a medida os traz (o JSON de viabilidade os tem; os testes podem omitir)
    prefill = (f" Nos mesmos registros, a mediana do prefill é de {_br(medida['prefill_s'])} s e a da geração, de {_br(medida['geracao_s'])} s (campos `prefill_ms` e "
               "`geracao_ms`): o prefill toma a maior parte do tempo de cada diagnóstico, e é a esse fato do projeto, não a uma fonte, que as sínteses e o mapa se referem quando "
               "dizem que o prefill domina o custo." if medida.get("prefill_s") and medida.get("geracao_s") else "")
    memoria = medida.get("ram_instalada_gb") is not None and medida.get("ram_visivel_gb") is not None
    n_corr = 5 + (1 if memoria else 0)
    avisos = [
        f"**Correção declarada.** O contexto dado aos agentes da parte A dizia que o prompt do agente tem \"alguns milhares de tokens\". O valor medido nos registros da Fase 3 é a "
        f"mediana de {_br(medida['mediana'])} tokens (`resultados_alvo/pre_fase4/viabilidade_modelos_grandes.json`, campo `medianas_do_agente.tokens_entrada`). O script trocou a expressão por "
        f"\"{medida['texto']}\" nas {trocas} ocorrências das sínteses e dos mapas.{razao}{prefill}",
        "**Ajuste de grafia.** Nas afirmações de suporte parcial (§6.14.12), a seta que os verificadores usaram em faixas de números virou \"para\". Títulos de issue e citações "
        "literais das fontes ficam como na fonte, inclusive com travessão e seta. "
        + (f"Fora isto, a troca do aviso 1 e as correções do aviso {n_corr}, nada do texto dos agentes foi alterado." if correcoes else "Nada mais do texto dos agentes foi alterado."),
        "**O que mudou depois de a parte A ser escrita.** A linha do mapa sobre a escolha fechada por probabilidade diz que a disponibilidade no Ollama 0.34.4 não tinha sido "
        "verificada: a sonda `sondar_logprobs.py` verificou em 01/10 (o Ollama devolve a probabilidade de cada token, de antes da temperatura), e a corrida 12 do roadmap mede se "
        "ela serve de sinal. A linha sobre a telemetria de roteamento medida nesta máquina aparece como adiada: o Eric escolheu fazê-la nesta fase, como estudo lateral com o OLMoE "
        "(corrida 13). O descarte do OLMoE como modelo do agente continua valendo; a corrida 13 mede, não adota.",
        "**Fontes sem revisão por pares.** O colibri é um repositório, e parte das medidas citadas vem de issues e de discussões da comunidade; as sínteses dizem quando é o caso.",
    ]
    if memoria:
        livre = f" ({_br(medida['ram_livre_gb'])} GB)" if medida.get("ram_livre_gb") is not None else ""
        avisos.append(f"**Memória da máquina.** O contexto dado aos agentes dizia que a máquina tem {_br(medida['ram_visivel_gb'], 2)} GB de RAM: é a memória que o Windows enxerga. "
                      f"A máquina tem {_br(medida['ram_instalada_gb'])} GB instalados (`viabilidade_modelos_grandes.json`, campo `maquina.ram_instalada_gb`), e é com a memória instalada "
                      f"que se compara o mínimo de RAM que um repositório declara. Onde as sínteses e o mapa comparavam a RAM livre no início de uma corrida{livre} com o mínimo do "
                      f"colibri, ou diziam que a máquina fica abaixo desse mínimo, o texto foi corrigido (aviso {n_corr}); onde só descrevem a máquina com "
                      f"{_br(medida['ram_visivel_gb'], 2)} GB, o número ficou, com este aviso valendo.")
    if correcoes:
        avisos.append(f"**Correções da revisão.** Depois de integradas, as sínteses e o mapa foram conferidos contra as afirmações verificadas (um revisor por tópico e um para o mapa). "
                      f"{_plural(len(correcoes), 'trecho foi corrigido', 'trechos foram corrigidos')} por script em {DATA_DAS_CORRECOES}; a lista, com o que mudou e o motivo de cada "
                      f"correção, está no fim do §6.14.{N_REJ}.")
    linhas += ["", f"{_POR_EXTENSO[len(avisos)]} avisos sobre o texto abaixo:", ""] + [f"{i}. {a}" for i, a in enumerate(avisos, 1)] + [""]
    return "\n".join(linhas) + "\n"


def render(dados: dict, mapas: dict, trocas: int, medida: dict, correcoes: list[dict] | None = None) -> str:
    secoes = [secao_r5(k, dados[k]) for k in ORDEM_R5 if k in dados]
    return cabecalho(dados, trocas, medida, correcoes) + "\n" + "\n".join(secoes) + "\n" + bloco_rejeitadas(dados, correcoes) + "\n" + bloco_mapas(mapas)


# ------------------------------------------------------------------ referências e índice (texto entra, texto sai)

def _ordem(ref: str) -> str:
    return unicodedata.normalize("NFKD", ref).lower()


def _url(ref: str) -> str:
    """Endereço da referência numa forma comparável: sem caixa, sem ponto ou barra no fim, e com o PDF e as versões
    de um preprint do arXiv levados ao endereço do resumo."""
    m = re.search(r"https?://[^\s<>\]]+", ref)
    if not m:
        return ""
    u = re.sub(r"^https?://(www\.)?", "", m.group(0).lower()).rstrip(".,;/)")
    m = re.match(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", u)
    return f"arxiv.org/abs/{m.group(1)}" if m else u


def _chave(ref: str) -> str:
    """A chave das outras rodadas (sobrenome, ano e início do título). Quando o título tem uma ou duas palavras, ela
    cai no trecho "Disponível em: https" e fica igual para fontes diferentes do mesmo ano; nesse caso o endereço
    entra no lugar do título."""
    ch = rl._chave_ref(ref)
    base, _, titulo = ch.rpartition("|")
    return f"{base}|{_url(ref) or ref.lower()[:60]}" if titulo in ("", "disponivel em https") else ch


def _sem_o_bloco(atual: str) -> str:
    return (atual[:atual.index(TITULO_REFS)] if TITULO_REFS in atual else atual).rstrip("\n")


def _selecionar(antes: str, dados: dict) -> tuple[list[str], list[str]]:
    """Das referências das sínteses, na ordem dos tópicos: as que entram no bloco e as omitidas por terem o mesmo
    endereço de outra que já entrou ou que já consta no arquivo (a mesma fonte citada em duas formas)."""
    linhas = [l[2:] for l in antes.splitlines() if l.startswith("- ")]
    chaves, urls = {_chave(l) for l in linhas}, {_url(l) for l in linhas} - {""}
    novas, pela_url = [], []
    for k in ORDEM_R5:
        for ref in ((dados.get(k) or {}).get("synthesis") or {}).get("referencias_abnt", []):
            ch, u = _chave(ref), _url(ref)
            if ch in chaves:
                continue
            if u and u in urls:
                pela_url.append(ref)
                continue
            chaves.add(ch)
            if u:
                urls.add(u)
            novas.append(ref)
    return novas, pela_url


def omitidas_pela_url(atual: str, dados: dict) -> list[str]:
    """As referências das sínteses que ficaram fora do bloco por repetirem o endereço de outra já listada."""
    return _selecionar(_sem_o_bloco(atual), dados)[1]


def referencias_com_bloco(atual: str, dados: dict) -> tuple[str, int, int]:
    """O texto de referencias.md com o bloco desta rodada regravado no fim (é sempre o último bloco), sem repetir
    referência que conste nos blocos anteriores, e com o total da frase de abertura recontado. Devolve também quantas
    referências novas a rodada trouxe e o total do arquivo."""
    antes = _sem_o_bloco(atual)
    novas, _ = _selecionar(antes, dados)
    bloco = "\n".join([TITULO_REFS, "",
                       "<!-- ! Alteração de IA - Revisar: bloco gerado por ferramentas/integrar_pesquisa_pre_fase4.py a partir das sínteses da rodada 5; referências já presentes acima foram omitidas (mesma chave das outras rodadas, sobrenome, ano e início do título, e também o mesmo endereço).",
                       "     ! Motivo: cada síntese traz a sua lista ABNT; sem a conferência as mesmas fontes entrariam duas vezes e o total do arquivo ficaria errado. O bloco é regravado inteiro quando a parte B da rodada for integrada. -->",
                       ""] + [f"- {r}" for r in sorted(novas, key=_ordem)]) + "\n"
    novo = antes + "\n\n" + bloco
    total = sum(1 for l in novo[novo.index("## 9. Referências levantadas"):].splitlines() if l.startswith("- "))
    m = re.search(r"os levantamentos de [^*\n]*? produziram as \*\*(\d+)\*\* referências abaixo", novo)
    assert m, "frase do total de referências não encontrada"
    novo = novo[:m.start()] + f"os levantamentos de 11/09, 21/09, 22/09, 29/09 e 01/10/2026 produziram as **{total}** referências abaixo" + novo[m.end():]
    return novo, len(novas), total  # `novas` já vem sem as repetidas pela chave e pelo endereço


def memorial_com_linha(s: str, dados: dict) -> str:
    """O texto do Memorial com a linha do índice deste levantamento gravada (ou regravada) logo depois da linha do
    levantamento da documentação autogerida."""
    feitos = [k for k in ORDEM_R5 if k in dados]
    falta_b = any(TITULOS_R5[k][0] == "B" and k not in dados for k in ORDEM_R5)
    linha = (TAG_DO_INDICE + " (§6.14), gravada por integrar_pesquisa_pre_fase4.py. ! Motivo: sem a linha o índice não leva ao levantamento nem aos mapas; ela é regravada quando a parte B da rodada for integrada. -->\n"
             + MARCA_DO_INDICE + "(memorial/2-pesquisa-e-literatura/levantamento-2026-10-01-pre-fase-4.md): §6.14, "
             + f"{len(feitos)} de {len(ORDEM_R5)} tópicos integrados (o repositório colibri, as pesquisas que ele cita, inferência com os pesos fora da RAM, modelos MoE pequenos em CPU e atlas de especialistas"
             + ("; os seis tópicos do raciocínio aberto entram com a parte B" if falta_b else "; fidelidade do raciocínio, formatos de trilha, relatório para humanos, atribuição ao contexto, confiança por probabilidade e uso das trilhas")
             + "); §6.14.12 rejeitadas com o motivo; §6.14.13 mapas adotado, adiado, descartado.\n")
    if MARCA_DO_INDICE in s:
        ini = s.rfind(TAG_DO_INDICE, 0, s.index(MARCA_DO_INDICE))
        assert ini >= 0, "linha do índice sem a tag que a acompanha"
        fim = s.index("\n", s.index(MARCA_DO_INDICE)) + 1
        return s[:ini] + linha + s[fim:]
    m = re.search(r"^- \[Levantamento — qualidade da documentação autogerida[^\n]*\n", s, re.M)
    assert m, "linha do levantamento da documentação autogerida no índice do Memorial não encontrada"
    return s[:m.end()] + linha + s[m.end():]


def _ler(p: Path) -> tuple[str, bool]:
    b = p.read_bytes()
    return b.decode("utf-8").replace("\r\n", "\n"), b"\r\n" in b


def _gravar(p: Path, texto: str, crlf: bool) -> None:
    p.write_bytes((texto.replace("\n", "\r\n") if crlf else texto).encode("utf-8"))


def integrar_referencias(dados: dict, simular: bool) -> None:
    atual, crlf = _ler(rl.REFERENCIAS)
    novo, novas, total = referencias_com_bloco(atual, dados)
    print(f"referências: {novas} novas desta rodada; total do arquivo {total}" + (" (simulado)" if simular else ("" if novo != atual else " (já estava em dia)")))
    for ref in omitidas_pela_url(atual, dados):
        print("  omitida (mesmo endereço de outra já listada):", ref[:110])
    if not simular and novo != atual:
        _gravar(rl.REFERENCIAS, novo, crlf)


def integrar_memorial(dados: dict, simular: bool) -> None:
    atual, crlf = _ler(MEMORIAL)
    novo = memorial_com_linha(atual, dados)
    if not simular and novo != atual:
        _gravar(MEMORIAL, novo, crlf)
    print("Memorial: linha do índice " + ("simulada" if simular else ("gravada" if novo != atual else "já estava em dia")))


def check() -> int:
    if not LEVANTAMENTO.exists():
        print("--check: nada integrado ainda")
        return 1
    medida = medidas_do_projeto()
    dados, mapas, trocas = carregar(medida=medida)
    falhas = 0
    e, a = rl._normalizar(render(dados, mapas, trocas, medida)), rl._normalizar(LEVANTAMENTO.read_text(encoding="utf-8"))
    if e == a:
        print(f"--check: levantamento da Pré-Fase 4 idêntico ao regerado ({len(dados)} de {len(ORDEM_R5)} tópicos)")
    else:
        falhas += 1
        print("--check: o levantamento DIFERE do regerado")
        print("\n".join(list(difflib.unified_diff(a, e, lineterm=""))[:30]))
    refs = _ler(rl.REFERENCIAS)[0]
    if referencias_com_bloco(refs, dados)[0] == refs:
        print("--check: bloco de referências e total em dia")
    else:
        falhas += 1
        print("--check: o bloco de referências (ou o total) DIFERE do regerado")
    indice = _ler(MEMORIAL)[0]
    if memorial_com_linha(indice, dados) == indice:
        print("--check: linha do índice do Memorial em dia")
    else:
        falhas += 1
        print("--check: a linha do índice do Memorial DIFERE da regerada")
    return 1 if falhas else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--simular", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        return check()
    medida = medidas_do_projeto()
    dados, mapas, trocas = carregar(medida=medida)
    if not dados:
        raise SystemExit("nenhuma parte da rodada 5 encontrada em .superpowers/sdd/pre-fase-4/pesquisa/")
    sem_sintese = [k for k in dados if not dados[k].get("synthesis")]
    if sem_sintese:
        raise SystemExit(f"tópico(s) sem síntese: {sem_sintese}")
    for k in ORDEM_R5:
        if k in dados:
            a, r, t = rl.contagem(dados[k])
            print(f"  {k}: {a} aprovadas, {r} rejeitadas, {t} não verificadas")
    for parte, m in mapas.items():
        print(f"mapa da parte {parte}: {len(m.get('linhas', []))} linhas, {len(m.get('riscos', []))} riscos")
    print(f"expressão do contexto trocada por \"{medida['texto']}\" em {trocas} ocorrência(s)")
    texto = render(dados, mapas, trocas, medida)
    if args.simular:
        print(f"levantamento: {len(texto)} caracteres (simulado)")
    else:
        LEVANTAMENTO.write_text(texto, encoding="utf-8", newline="\n")
        print(f"levantamento gravado: {LEVANTAMENTO.name} ({len(texto)} caracteres)")
    integrar_referencias(dados, args.simular)
    integrar_memorial(dados, args.simular)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
