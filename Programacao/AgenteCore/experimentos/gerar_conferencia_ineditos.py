#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (05/11/2026, decisão 92): monta o documento da conferência dos 36 inéditos da ficha 27 a partir
# do banco (`banco_casos_ineditos_fase4.py`), da corrida 17 (`resultados_alvo/fase4/reproducibilidade_ineditos.json`) e da pré-análise do
# Claude (`resultados_alvo/fase4/conferencia_ineditos_preanalise.json`); grava `conferencia_ineditos.{json,md}` na mesma pasta.
# ! Motivo: a decisão 92 pede a conferência do Eric antes da corrida 24, e nenhuma conferência anterior foi feita sobre esse banco. Quem
# confere precisa ver o corpo, o sintoma e o gabarito juntos; sair de script impede que um trecho de caso ou um número seja digitado à mão,
# e a pré-análise aparece marcada como do Claude, porque ela indica onde olhar e não substitui a conferência.
"""Documento da conferência dos 36 inéditos da ficha 27. Uso: gerar_conferencia_ineditos.py [--check]"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time

import analisar_fase3b as a3b
import banco_casos_ineditos_fase4 as bi4
import caminhos
import pre_fase4 as pf

NOME, PREFIXO = "conferencia_ineditos", "tb_f4_conferencia_"
TITULO = "Conferência dos 36 inéditos da ficha 27"


def _pasta():
    return caminhos.RESULTADOS / "fase4"


def ler() -> dict:
    """A corrida 17 e a pré-análise, como estão gravadas; o que faltar vem como dicionário vazio."""
    def abrir(arquivo: str) -> dict:
        caminho = _pasta() / arquivo
        return json.loads(caminho.read_text(encoding="utf-8")) if caminho.exists() else {}
    return {"reproducao": abrir("reproducibilidade_ineditos.json"), "preanalise": abrir("conferencia_ineditos_preanalise.json")}


def _na_tela(caso_id: str, reproducao: dict) -> str:
    for c in reproducao.get("casos") or []:
        if c["id"] == caso_id:
            return f"{'reproduz' if c.get('reproduz') else 'não reproduz'}: {c.get('motivo')}"
    for c in reproducao.get("fora") or []:
        if c["id"] == caso_id:
            return f"fora: {c.get('motivo')}"
    return ""


def _sem_ponto(nota: str) -> str:
    """A nota sem o "Ponto N:" do começo, que é da lista de verificação do agente e não diz nada a quem lê."""
    limpa = re.sub(r"^Ponto \d+:\s*", "", nota or "")
    return limpa[:1].upper() + limpa[1:]


def resumir(casos: list[dict], reproducao: dict, preanalise: dict, gerado_em: str | None = None) -> dict:
    """Cada caso com o que a corrida 17 viu e a pré-análise; os casos para olhar vêm primeiro, na ordem do banco."""
    pre = {c["caso"]: c for c in preanalise.get("casos") or []}
    ids = {c["id"] for c in casos}
    estranhos = sorted(set(pre) - ids)
    if estranhos:
        raise ValueError(f"pré-análise de caso que não está no banco: {estranhos}")
    itens = []
    for c in casos:
        p = pre.get(c["id"]) or {}
        itens.append({"caso": c["id"], "classe": c["classe"], "nivel": c["nivel"], "veredito": p.get("veredito"), "o_que_olhar": _sem_ponto(p.get("o_que_olhar") or ""),
                      "causa_vizinha": p.get("causa_vizinha"), "evidencia": p.get("evidencia"), "tela": _na_tela(c["id"], reproducao), "entrada": c["entrada"], "gabarito": c["gabarito"]})
    itens.sort(key=lambda x: x["veredito"] != "ver")
    classes = []
    for classe in sorted({x["classe"] for x in itens}):
        sub = [x for x in itens if x["classe"] == classe]
        classes.append({"classe": classe, "casos": len(sub), "ok": sum(1 for x in sub if x["veredito"] == "ok"), "ver": sum(1 for x in sub if x["veredito"] == "ver"),
                        "reproduzem": sum(1 for x in sub if x["tela"].startswith("reproduz"))})
    return {"metadados": {"gerado_em": gerado_em or time.strftime("%Y-%m-%dT%H:%M:%S"), "gerado_por": "gerar_conferencia_ineditos.py", "origem_da_preanalise": preanalise.get("origem")},
            "resumo": {"casos": len(itens), "ok": sum(1 for x in itens if x["veredito"] == "ok"), "ver": sum(1 for x in itens if x["veredito"] == "ver"),
                       "reproduzem": sum(1 for x in itens if x["tela"].startswith("reproduz")), "fora_da_tela": sum(1 for x in itens if x["tela"].startswith("fora")),
                       "sem_preanalise": sum(1 for x in itens if x["veredito"] is None)},
            "por_classe": classes, "casos": itens}


def _termos(lista: list | None) -> str:
    return ", ".join(f"`{t}`" for t in lista or []) or "nenhum"


def _bloco_do_caso(x: dict) -> list[str]:
    e, g = x["entrada"], x["gabarito"]
    marca = " (para olhar)" if x["veredito"] == "ver" else ""
    linhas = [f"### `{x['caso']}`, classe {x['classe']}, nível {x['nivel']}: `{g['causa_raiz']}`{marca}", "",
              f"- **Requisição:** `{e.get('requisicao')}`", f"- **Status:** {e.get('status')}", f"- **Contrato:** `{e.get('contrato')}`", f"- **Corpo:** `{e.get('corpo')}`",
              f"- **Sintoma:** {e.get('sintoma')}"]
    if e.get("observacao"):
        linhas.append(f"- **Observação:** {e['observacao']}")
    if e.get("seletor_quebrado"):
        linhas.append(f"- **Seletor quebrado:** `{e['seletor_quebrado']}`")
    if e.get("arvore"):
        linhas += ["- **Árvore da tela:**", "", "```text", str(e["arvore"]), "```", ""]
    campo = f"`{g['campo_afetado']}`" if g.get("campo_afetado") else "nenhum"
    linhas.append(f"- **Gabarito:** causa `{g['causa_raiz']}`; campo {campo}; termos esperados {_termos(g.get('termos_esperados'))}; termos proibidos {_termos(g.get('termos_proibidos'))}")
    linhas.append(f"- **Na corrida 17:** {x['tela'] or 'não aparece na leitura'}")
    if x["veredito"] == "ver":
        vizinha = f" Outra causa que caberia: `{x['causa_vizinha']}`." if x.get("causa_vizinha") else ""
        linhas.append(f"- **Pré-análise:** {x['o_que_olhar']}{vizinha} (`{x.get('evidencia')}`)")
    elif x["veredito"] == "ok":
        linhas.append(f"- **Pré-análise:** nada a apontar (`{x.get('evidencia')}`)")
    return [*linhas, ""]


def render(dado: dict) -> str:
    r = dado["resumo"]
    cab = pf.cabecalho(TITULO, "gerar_conferencia_ineditos.py", "banco_casos_ineditos_fase4.py, reproducibilidade_ineditos.json e conferencia_ineditos_preanalise.json", dado["metadados"]["gerado_em"][:10])
    texto = ("Os casos que a corrida 24 vai medir (decisão 92). O agente recebe cada caso sem o gabarito e escolhe uma das 23 causas; um caso ruim mede o modelo contra algo que o sistema não produz, "
             "ou contra uma resposta com mais de uma leitura honesta. A pergunta de cada caso: a causa do gabarito é a leitura certa do que o corpo e o sintoma mostram? "
             f"A pré-análise é do Claude, feita só lendo o código, e diz onde olhar com mais cuidado: {r['ver']} casos para olhar e {r['ok']} sem nada a apontar. Ela não é a conferência: quem confere é o Eric. "
             f"\"Na corrida 17\" diz o que a falha injetada fez de verdade: {r['reproduzem']} casos reproduzem na tela e {r['fora_da_tela']} ficam fora dela, porque a rota não tem tela ou o caso é um cenário descrito.")
    blocos = [a3b.tab("tb_f4_conferencia_classes", ["Classe", "Casos", "Reproduzem na tela", "Sem nada a apontar", "Para olhar"],
                      [[str(x["classe"]), str(x["casos"]), str(x["reproduzem"]), str(x["ok"]), str(x["ver"])] for x in dado["por_classe"]]),
              a3b.tab("tb_f4_conferencia_ver", ["Caso", "Causa do gabarito", "Outra causa que caberia", "O que olhar", "Onde"],
                      [[f"`{x['caso']}`", f"`{x['gabarito']['causa_raiz']}`", f"`{x['causa_vizinha']}`" if x.get("causa_vizinha") else "nenhuma", x["o_que_olhar"].replace("|", "\\|"), f"`{x.get('evidencia')}`"]
                       for x in dado["casos"] if x["veredito"] == "ver"] or [["nenhum", "", "", "", ""]])]
    corpo = ["## Os casos, com os para olhar primeiro", ""]
    for x in dado["casos"]:
        corpo += _bloco_do_caso(x)
    return "\n".join([*cab, "", texto, "", *blocos, "", *corpo]).rstrip("\n") + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="regera e compara com o que está em disco")
    args = ap.parse_args()
    bruto = ler()
    if not bruto["reproducao"] or not bruto["preanalise"]:
        print("faltam reproducibilidade_ineditos.json ou conferencia_ineditos_preanalise.json em resultados_alvo/fase4/")
        return 2
    dado = resumir(bi4.CASOS_INEDITOS_FASE4, bruto["reproducao"], bruto["preanalise"])
    return pf.fechar(NOME, dado, render(dado), PREFIXO, check=args.check, pasta=_pasta(), doc=_pasta() / "nao_existe.md")


if __name__ == "__main__":
    sys.exit(main())
