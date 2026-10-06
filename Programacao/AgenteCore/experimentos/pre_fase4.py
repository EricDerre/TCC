#!/usr/bin/env python3
# ! Alteração de IA - Revisar: módulo novo (01/10/2026) com o que os scripts da Pré-Fase 4 têm em comum: a pasta dos
# documentos derivados (resultados_alvo/pre_fase4/), o relatório do Memorial em que os blocos de tabela são colados, o
# cabeçalho padrão dos .md derivados e a rotina que grava o par .json/.md, confere com --check e cola com --colar.
# ! Motivo: a fase tem vários scripts de análise (viabilidade dos modelos grandes, relatório de raciocínio, confiança,
# atlas) e todos seguem a regra do projeto de não digitar número à mão: gravam um JSON e um Markdown com blocos
# `<!-- tabela:tb_… -->` e um modo --check que regera e compara. A colagem de analisar_fase3b.colar interrompe quando
# o documento tem um bloco que o script não gerou; como aqui o mesmo relatório recebe blocos de vários scripts, cada
# script cuida só dos blocos do próprio prefixo (tb_viab_, tb_conf_, …) e deixa os dos outros como estão.
"""Caminhos e rotina de gravação/conferência dos derivados da Pré-Fase 4."""
from __future__ import annotations

import json
from pathlib import Path

import analisar_fase3b as a3b
import caminhos

EXP = Path(__file__).resolve().parent
PASTA = caminhos.RESULTADOS / "pre_fase4"
DOC_ALVO = EXP.parent.parent.parent / "Documentacao" / "memorial" / "3-resultados-e-analises" / "pre-fase-4-relatorio.md"


def cabecalho(titulo: str, script: str, origem: str, data: str) -> list[str]:
    """As três primeiras linhas de todo .md derivado da fase: a tag (duas linhas) e o título com a data, que é a única
    parte que muda de um dia para o outro e por isso fica fora da comparação do --check."""
    return [f"<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por {script} a partir de {origem} (--check regera e compara); não editar à mão.",
            "     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->",
            f"# {titulo}, gerada em {data}"]


def sem_data(dado: dict) -> dict:
    """O dado sem `metadados.gerado_em`, para comparar o conteúdo de duas gerações em dias diferentes."""
    return {k: ({kk: vv for kk, vv in v.items() if kk != "gerado_em"} if k == "metadados" and isinstance(v, dict) else v)
            for k, v in dado.items()}


def colar_blocos(doc: Path, md: str, prefixo: str) -> tuple[int, bool]:
    """Troca no documento os blocos `<!-- tabela:<prefixo>… -->` pelos gerados em `md`. Bloco desse prefixo que o
    documento tem e o script não gerou interrompe; blocos de outros prefixos não são tocados."""
    gerados = {n: b for n, b in a3b.blocos_de(md).items() if n.startswith(prefixo)}
    texto = doc.read_text(encoding="utf-8")
    faltando = [n for n in a3b.BLOCO_ALVO_RE.findall(texto) if n.startswith(prefixo) and n not in gerados]
    if faltando:
        raise SystemExit(f"{doc.name}: bloco(s) sem tabela gerada: {faltando}")
    colados = 0

    def troca(m) -> str:
        nonlocal colados
        if m.group(1) in gerados:
            colados += 1
            return gerados[m.group(1)]
        return m.group(0)

    novo = a3b.BLOCO_ALVO_RE.sub(troca, texto)
    if novo != texto:
        doc.write_text(novo, encoding="utf-8", newline="\n")
    return colados, novo != texto


def blocos_divergentes(doc: Path, md: str, prefixo: str) -> list[str]:
    """Nomes dos blocos do prefixo que estão no documento com conteúdo diferente do gerado (vazio conta como diferente)."""
    gerados = a3b.blocos_de(md)
    texto = doc.read_text(encoding="utf-8")
    cheios = a3b.blocos_de(texto)
    return [n for n in a3b.BLOCO_ALVO_RE.findall(texto) if n.startswith(prefixo) and cheios.get(n) != gerados.get(n)]


def fechar(nome: str, dado: dict, md: str, prefixo: str, check: bool = False, colar: bool = False,
           pasta: Path | None = None, doc: Path | None = None) -> int:
    """Grava `<nome>.json` e `<nome>.md` na pasta dos derivados. Com check=True não grava: regera e compara com o que
    está em disco (o JSON sem a data de geração, o Markdown sem as três linhas do cabeçalho) e com os blocos já colados
    no relatório; devolve 1 se algo difere. Com colar=True cola os blocos do prefixo no relatório."""
    pasta = pasta or PASTA
    doc = doc or DOC_ALVO
    arq_json, arq_md = pasta / f"{nome}.json", pasta / f"{nome}.md"
    if check:
        antigo = json.loads(arq_json.read_text(encoding="utf-8")) if arq_json.exists() else {}
        atual = arq_md.read_text(encoding="utf-8") if arq_md.exists() else ""
        ok_json = sem_data(antigo) == sem_data(json.loads(json.dumps(dado, ensure_ascii=False)))
        ok_md = bool(atual) and atual.split("\n", 3)[-1] == md.split("\n", 3)[-1]
        divergentes = blocos_divergentes(doc, md, prefixo) if doc.exists() else []
        if ok_json and ok_md and not divergentes:
            print(f"--check: {arq_json.name} e {arq_md.name} batem com os dados atuais"
                  + (f", e os blocos {prefixo}* de {doc.name} também" if doc.exists() else f" ({doc.name} ainda não existe)"))
            return 0
        print(f"--check: DIFERE (json {'ok' if ok_json else 'difere'}; md {'ok' if ok_md else 'difere'}; "
              f"blocos divergentes em {doc.name}: {divergentes})")
        return 1
    if colar:
        n, mudou = colar_blocos(doc, md, prefixo)
        print(f"{doc.name}: {n} bloco(s) {prefixo}* colado(s); mudou: {mudou}")
        return 0
    pasta.mkdir(parents=True, exist_ok=True)
    arq_json.write_text(json.dumps(dado, ensure_ascii=False, indent=2), encoding="utf-8")
    arq_md.write_text(md, encoding="utf-8", newline="\n")
    print(f"gravado: {arq_json.name} e {arq_md.name} em {pasta}")
    return 0
