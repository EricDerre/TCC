#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (01/10/2026, Pré-Fase 4) que faz a conta de viabilidade do repositório
# colibri nesta máquina: para cada família de modelo que ele roda, se o arquivo cabe no disco e se a RAM mínima
# declarada cabe na nossa; quanto tempo o disco levaria para entregar um token "frio" (o repositório diz quantos GB
# são lidos por token) no NVMe medido por ferramentas/medir_disco.py e em dois discos mais lentos, postos como
# premissa declarada; e quanto tempo levaria a resposta mediana do nosso diagnóstico nas velocidades que terceiros
# mediram em máquinas parecidas. Grava viabilidade_modelos_grandes.json e .md em resultados_alvo/pre_fase4/, com
# --check e --colar.
# ! Motivo: o Eric pediu a viabilidade da ideia do colibri com CPU e SSD ou HD, com ganhos e custos. Os números do
# repositório estão em tokens por segundo e em GB; o que importa para o agente é o tempo de UM diagnóstico, e esse
# sai da mediana de tokens que o nosso modelo de fato escreve (lida dos registros oficiais da Fase 3). As constantes
# do repositório ficam aqui com a URL do arquivo de onde saíram e a data de acesso, para o texto formal poder citá-las;
# a rodada 5 da pesquisa (tópico r5-colibri-leitura-integral) confere cada uma, e a chave `conferido_pela_rodada_5`
# diz se isso já foi feito.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python viabilidade_modelos_grandes.py [--check] [--colar]
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import datetime
from pathlib import Path

import analisar_fase3b as a3b
import caminhos
import pre_fase4 as pf

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

NOME = "viabilidade_modelos_grandes"
PREFIXO = "tb_viab_"
MODELO = "qwen2.5:7b"
REPO = "https://github.com/JustVugg/colibri"
ACESSO = "2026-10-01"
# Rodada A da pesquisa (01/10/2026, tópico r5-colibri-leitura-integral, 16 afirmações verificadas): requisitos por
# modelo, leitura por token frio e as medidas de terceiros abaixo conferem com o repositório. Única ressalva: o
# verificador não confirmou os 419 GB do GLM-5.3 (a linha "GLM-5.2/5.3" da tabela do README foi lida aqui duas vezes
# com "~372 GB (5.2) / ~419 GB (5.3)").
CONFERIDO_PELA_RODADA_5 = True
RESSALVA_DA_CONFERENCIA = "o verificador não confirmou o tamanho em disco do GLM-5.3 (419 GB)"
FONTE_TABELA = f"{REPO}/blob/main/README.md"
FONTE_MEDIDAS = f"{REPO}/blob/main/docs/benchmarks.md"
FONTE_SITE = "https://justvugg.github.io/colibri"

# Tabela "What each one needs" do README (disco e RAM) e parâmetros totais e ativos da página do projeto.
# disco_gb e ram_min_gb são os valores com que a conta é feita; `ram_texto` guarda a redação do repositório.
FAMILIAS = [
    {"nome": "OLMoE", "parametros_bi": 7, "ativos_bi": 1, "disco_gb": 7, "ram_min_gb": 8, "ram_texto": "8 GB", "gpu": "não precisa"},
    {"nome": "Qwen3.6-35B-A3B", "parametros_bi": 35, "ativos_bi": 3, "disco_gb": 20, "ram_min_gb": 24,
     "ram_texto": "24 GB (needs full RAM residency)", "gpu": "opcional"},
    {"nome": "DeepSeek V4 Flash", "parametros_bi": 284, "ativos_bi": 13, "disco_gb": 167, "ram_min_gb": 16,
     "ram_texto": "16 GB min, 32 GB comfortable", "gpu": "opcional"},
    {"nome": "Qwen3.8-Flash-Next", "parametros_bi": 180, "ativos_bi": 6, "disco_gb": 185.5, "ram_min_gb": 16,
     "ram_texto": "16 GB min, 24 GB comfortable at the default context", "gpu": "opcional"},
    {"nome": "GLM-5.3-Flash", "parametros_bi": 320, "ativos_bi": 18, "disco_gb": 195, "ram_min_gb": 25,
     "ram_texto": "25 GB (12 GB weights at int4 + expert cache)", "gpu": "não precisa"},
    {"nome": "GLM-5.2", "parametros_bi": 744, "ativos_bi": 40, "disco_gb": 372, "ram_min_gb": 16,
     "ram_texto": "16 GB min, 24 GB comfortable", "gpu": "não precisa"},
    {"nome": "GLM-5.3", "parametros_bi": None, "ativos_bi": None, "disco_gb": 419, "ram_min_gb": 16,
     "ram_texto": "16 GB min, 24 GB comfortable", "gpu": "não precisa"},
    {"nome": "Inkling", "parametros_bi": 975, "ativos_bi": 41, "disco_gb": 469, "ram_min_gb": 25,
     "ram_texto": "25 GB with the int4 dense container, ~120 GB without", "gpu": "não precisa"},
    {"nome": "Kimi K3", "parametros_bi": 2800, "ativos_bi": 104, "disco_gb": 1600, "ram_min_gb": 32, "ram_texto": "32 GB+", "gpu": "não precisa"},
]
for _f in FAMILIAS:
    _f["fonte"] = FONTE_TABELA

# "a cold token costs ~11.4 GB of expert reads" (docs/benchmarks.md), para o GLM-5.2.
GB_POR_TOKEN_FRIO = 11.4

# Linhas de docs/benchmarks.md com máquina pequena ou só CPU (a issue de cada uma está na própria tabela).
MEDIDAS_DE_TERCEIROS = [
    {"maquina": "Intel Core Ultra 7 270K Plus, 24 GB, WSL2, NVMe", "modelo": "GLM-5.2", "tok_por_s": 0.07, "nota": "padrão; cache de especialistas com acerto de 3 a 4%", "issue": 2},
    {"maquina": "Intel Core Ultra 7 270K Plus, 24 GB, WSL2, NVMe", "modelo": "GLM-5.2", "tok_por_s": 0.11, "nota": "com --topp 0.7, que o repositório marca como opção com perda", "issue": 2},
    {"maquina": "Intel i5-12600K, 32 GB, Windows 11 nativo, só CPU", "modelo": "GLM-5.2", "tok_por_s": 0.08, "nota": "frio, cache limitado pela RAM a cerca de 2 especialistas por camada", "issue": 113},
    {"maquina": "Intel Core Ultra 9 185H, 32 GB, Windows 11 nativo", "modelo": "GLM-5.2", "tok_por_s": 0.03, "nota": "frio, só CPU; a mesma máquina chega a 0,5 com o cache quente", "issue": 128},
    {"maquina": "Apple M3 básico, 16 GB, só CPU", "modelo": "OLMoE", "tok_por_s": 3.69, "nota": "frio; 4,18 com o cache quente", "issue": 949},
]
for _m in MEDIDAS_DE_TERCEIROS:
    _m["fonte"] = FONTE_MEDIDAS

# Discos que não medimos entram como premissa declarada, para responder à pergunta do Eric sobre SSD comum e HD.
DISCOS_DE_PREMISSA = [
    {"disco": "SSD SATA (premissa: 0,55 GB/s, teto prático da interface)", "gb_por_s": 0.55},
    {"disco": "disco rígido de 7.200 rpm (premissa: 0,15 GB/s em leitura sequencial)", "gb_por_s": 0.15},
]


# ! Alteração de IA - Revisar: (01/10/2026, tarde) a RAM mínima que o repositório declara passa a ser comparada com a
# memória INSTALADA na máquina, em três estados (sim, no_minimo, nao), e o veredito ganha o estado "no_limite".
# ! Motivo: a primeira versão comparava o "16 GB min" do repositório com os 15,69 GB que o Windows enxerga e dava a
# máquina como abaixo do mínimo; ela tem 16 GB instalados (parte reservada ao vídeo integrado), que é a classe de
# máquina de que o repositório fala. Com a conta certa, dois modelos grandes cabem no disco livre e ficam exatamente no
# mínimo de RAM declarado: "só o OLMoE roda" passa a ser "só o OLMoE roda com folga". Achado na revisão do levantamento.
def cabe(familia: dict, maquina: dict) -> dict:
    """O modelo cabe nesta máquina? No disco livre, no disco inteiro (se fosse esvaziado) e na RAM. A RAM mínima que o
    repositório declara é comparada com a memória instalada: `sim` se ele pede menos, `no_minimo` se pede exatamente a
    instalada, `nao` se pede mais. Roda (`sim`) o que cabe no disco livre com folga de RAM; fica `no_limite` o que
    cabe no disco livre e está no mínimo de RAM declarado; o resto não roda (`nao`)."""
    instalada = maquina.get("ram_instalada_gb")
    if instalada is None:
        raise SystemExit("falta maquina.ram_instalada_gb: rode `python ferramentas/medir_disco.py --completar-maquina` na raiz do repositório")
    disco_livre = familia["disco_gb"] <= maquina["disco_livre_gb"]
    disco_total = familia["disco_gb"] <= maquina["disco_total_gb"]
    ram = "sim" if familia["ram_min_gb"] < instalada else ("no_minimo" if familia["ram_min_gb"] == instalada else "nao")
    roda = "nao" if (not disco_livre or ram == "nao") else ("sim" if ram == "sim" else "no_limite")
    return {"disco_livre": disco_livre, "disco_total": disco_total, "ram": ram, "roda": roda}


def segundos_por_token_frio(gb_por_token: float, gb_por_s: float | None) -> float | None:
    """Tempo só de disco para entregar um token sem nada em cache; piso do tempo real, que ainda soma a conta na CPU."""
    return gb_por_token / gb_por_s if gb_por_s else None


def segundos_de_geracao(tokens: float, tok_por_s: float | None) -> float | None:
    return tokens / tok_por_s if tok_por_s else None


def medianas_dos_registros(pasta_do_modelo: Path) -> dict:
    """Medianas de tokens e de tempo dos diagnósticos gravados de um modelo (todos os diagnosticos__L*.jsonl da pasta)."""
    regs = []
    for arq in sorted(pasta_do_modelo.glob("diagnosticos__L*.jsonl")):
        regs += [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()]
    campos = ("tokens_entrada", "tokens_saida", "segundos", "prefill_ms", "geracao_ms")
    return {"n": len(regs), **{c: statistics.median(r[c] for r in regs) for c in campos}}


def carregar() -> dict:
    """Lê a medição do disco (medir_disco.py), a RAM livre no início de uma corrida (maquina.json da Fase 2-B) e as
    medianas dos registros oficiais do modelo decidido."""
    arq_disco = pf.PASTA / "disco.json"
    if not arq_disco.exists():
        raise SystemExit(f"falta {arq_disco}: rode `python ferramentas/medir_disco.py` na raiz do repositório")
    disco = json.loads(arq_disco.read_text(encoding="utf-8"))
    maq = disco["maquina"]
    antiga = json.loads((caminhos.RESULTADOS / "maquina.json").read_text(encoding="utf-8-sig"))
    c3 = caminhos.fase3("fase3")
    maq3 = json.loads(c3["maquina"].read_text(encoding="utf-8-sig"))
    maquina = {"cpu": maq.get("cpu"), "nucleos": antiga.get("nucleos"), "threads": maq.get("threads"), "ram_gb": maq.get("ram_gb"), "ram_instalada_gb": maq.get("ram_instalada_gb"),
               "ram_livre_no_inicio_de_corrida_gb": antiga.get("ram_livre_no_inicio_gb"),
               "disco_modelo": maq["disco"].get("modelo"), "disco_barramento": maq["disco"].get("barramento"),
               "disco_total_gb": maq["disco"].get("total_gb"), "disco_livre_gb": maq["disco"].get("livre_gb"),
               "sistema": antiga.get("sistema"), "ollama_da_fase_3": maq3.get("ollama")}
    slug = a3b.slug(MODELO)
    return {"maquina": maquina, "medianas": medianas_dos_registros(c3["raiz"] / slug), "disco": disco}


def montar(maquina: dict, medianas: dict, disco: dict, modelo: str = MODELO, gerado_em: str | None = None) -> dict:
    familias = [{**f, **cabe(f, maquina)} for f in FAMILIAS]
    tokens = medianas["tokens_saida"]

    def cenario(nome: str, gb_s: float | None, premissa: bool) -> dict:
        s = segundos_por_token_frio(GB_POR_TOKEN_FRIO, gb_s)
        return {"disco": nome, "gb_por_s": gb_s, "premissa": premissa, "segundos_por_token_frio": s,
                "tokens_por_s_teto": (1 / s) if s else None,
                "minutos_de_leitura_por_resposta": (s * tokens / 60) if s else None}

    cenarios = [cenario("NVMe desta máquina, leitura por fora do cache (medido)", (disco.get("direto") or {}).get("gb_por_s_mediana"), False)]
    cenarios += [cenario(d["disco"], d["gb_por_s"], True) for d in DISCOS_DE_PREMISSA]
    medidas = []
    for m in MEDIDAS_DE_TERCEIROS:
        s = segundos_de_geracao(tokens, m["tok_por_s"])
        medidas.append({**m, "segundos_por_resposta": s, "minutos_por_resposta": s / 60 if s else None,
                        "vezes_o_tempo_de_hoje": (s / medianas["segundos"]) if s and medianas.get("segundos") else None})
    return {
        "metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "repositorio": REPO, "acesso": ACESSO,
                      "conferido_pela_rodada_5": CONFERIDO_PELA_RODADA_5, "ressalva_da_conferencia": RESSALVA_DA_CONFERENCIA,
                      "modelo_do_agente": modelo,
                      "gb_por_token_frio": GB_POR_TOKEN_FRIO,
                      "fontes": {"tabela_de_requisitos": FONTE_TABELA, "medidas": FONTE_MEDIDAS, "parametros": FONTE_SITE,
                                 "disco": "resultados_alvo/pre_fase4/disco.json", "medianas": "resultados_alvo/fase3/<modelo>/diagnosticos__L*.jsonl",
                                 "ram_livre": "resultados_alvo/maquina.json (ram_livre_no_inicio_gb)"}},
        "maquina": maquina, "medianas_do_agente": medianas,
        "disco_medido": {k: disco.get(k) for k in ("bloco_bytes", "blocos", "threads")}
                        | {"direto": {k: v for k, v in (disco.get("direto") or {}).items() if k != "medidas"},
                           "pelo_cache": {k: v for k, v in (disco.get("pelo_cache") or {}).items() if k != "medidas"}},
        "familias": familias, "cenarios_de_disco": cenarios, "medidas_de_terceiros": medidas,
    }


def render(dado: dict) -> str:
    f = a3b.f
    m, maq, med = dado["metadados"], dado["maquina"], dado["medianas_do_agente"]
    sim = lambda v: "sim" if v else "**não**"  # noqa: E731
    texto_da_ram = {"sim": "sim", "no_minimo": "no mínimo declarado", "nao": "**não**"}
    texto_do_veredito = {"sim": "sim", "no_limite": "no limite", "nao": "**não**"}
    blocos = [
        a3b.tab("tb_viab_maquina", ["Item", "Valor", "Origem"], [
            ["Processador", f(maq["cpu"]), "`disco.json` (`maquina.cpu`)"],
            ["RAM instalada", f(maq["ram_instalada_gb"]) + " GB", "`disco.json` (`maquina.ram_instalada_gb`)"],
            ["RAM que o sistema enxerga", f(maq["ram_gb"], 2) + " GB", "`disco.json` (`maquina.ram_gb`)"],
            ["RAM livre no início de uma corrida", f(maq["ram_livre_no_inicio_de_corrida_gb"]) + " GB", "`resultados_alvo/maquina.json` (`ram_livre_no_inicio_gb`, Fase 2-B)"],
            ["Disco", f"{f(maq['disco_modelo'])} ({f(maq['disco_barramento'])})", "`disco.json` (`maquina.disco`)"],
            ["Disco: tamanho e espaço livre", f"{f(maq['disco_total_gb'])} GB, {f(maq['disco_livre_gb'])} GB livres", "`disco.json` (`maquina.disco`)"],
            ["Leitura do disco por fora do cache (mediana)", f((dado["disco_medido"]["direto"] or {}).get("gb_por_s_mediana"), 2) + " GB/s", "`disco.json` (`direto.gb_por_s_mediana`)"],
            ["Leitura passando pelo cache (mediana)", f((dado["disco_medido"]["pelo_cache"] or {}).get("gb_por_s_mediana"), 2) + " GB/s", "`disco.json` (`pelo_cache.gb_por_s_mediana`)"],
            [f"Resposta mediana do `{m['modelo_do_agente']}`", f"{f(med['tokens_saida'])} tokens em {f(float(med['segundos']))} s ({f(med['n'])} diagnósticos)", "registros oficiais da Fase 3"],
            ["Prompt mediano", f"{f(med['tokens_entrada'])} tokens", "registros oficiais da Fase 3"],
        ]),
        a3b.tab("tb_viab_familias", ["Modelo", "Parâmetros (bilhões)", "Ativos por token (bilhões)", "Disco pedido (GB)", "RAM pedida (texto do repositório)",
                                     "Cabe no disco livre", "Caberia no disco vazio", "RAM pedida contra a instalada", "Roda nesta máquina"],
                [[x["nome"], f(x["parametros_bi"]), f(x["ativos_bi"]), f(float(x["disco_gb"])), x["ram_texto"], sim(x["disco_livre"]), sim(x["disco_total"]),
                  texto_da_ram[x["ram"]], texto_do_veredito[x["roda"]]] for x in dado["familias"]]),
        a3b.tab("tb_viab_disco", ["Disco", "Leitura (GB/s)", "Medido ou premissa", "Segundos de disco por token frio", "Teto de tokens por segundo",
                                  "Minutos só de leitura para a resposta mediana"],
                [[c["disco"], f(c["gb_por_s"], 2), "premissa" if c["premissa"] else "medido", f(c["segundos_por_token_frio"]),
                  f(c["tokens_por_s_teto"], 3), f(c["minutos_de_leitura_por_resposta"])] for c in dado["cenarios_de_disco"]]),
        a3b.tab("tb_viab_terceiros", ["Máquina (medida publicada no repositório)", "Modelo", "Tokens por segundo", "Condição", "Minutos só de geração para a nossa resposta mediana",
                                      "Vezes o tempo total de um diagnóstico de hoje", "Issue"],
                [[x["maquina"], x["modelo"], f(x["tok_por_s"], 2), x["nota"], f(x["minutos_por_resposta"]), f(x["vezes_o_tempo_de_hoje"]), f"#{x['issue']}"]
                 for x in dado["medidas_de_terceiros"]]),
    ]
    cab = pf.cabecalho("Viabilidade dos modelos grandes do colibri nesta máquina", "viabilidade_modelos_grandes.py",
                       "disco.json, dos registros oficiais da Fase 3 e das constantes citadas do repositório", m["gerado_em"][:10])
    conferido = (f"já foram conferidas (ressalva: {m['ressalva_da_conferencia']})" if m["conferido_pela_rodada_5"]
                 else "ainda não foram conferidas")
    cab += ["", f"Repositório: {m['repositorio']} (acesso em {m['acesso']}). As constantes do repositório (requisitos por modelo, GB lidos por token e medidas de "
                f"terceiros) {conferido} pela rodada 5 da pesquisa. Um token frio do GLM-5.2 lê cerca de {f(m['gb_por_token_frio'])} GB do disco "
                "(`docs/benchmarks.md`). Os tempos de disco são piso: ainda falta a conta na CPU e a leitura do prompt, que o repositório não mede em máquina pequena.", "",
            "Como ler a última coluna da tabela dos modelos: roda (sim) o que cabe no disco livre e pede menos RAM do que a instalada; fica no limite o que cabe no disco livre e pede "
            "exatamente a RAM instalada, que é o mínimo declarado pelo repositório (não há medida publicada de nenhum deles numa máquina dessa classe); o resto não roda.", ""]
    return "\n".join(cab) + "\n\n" + "\n\n".join(blocos) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="regera e compara com os arquivos gravados e com os blocos do relatório")
    ap.add_argument("--colar", action="store_true", help="cola os blocos tb_viab_* no relatório da Pré-Fase 4")
    args = ap.parse_args()
    print(caminhos.descricao())
    dado = montar(**carregar())
    return pf.fechar(NOME, dado, render(dado), PREFIXO, check=args.check, colar=args.colar)


if __name__ == "__main__":
    sys.exit(main())
