#!/usr/bin/env python3
# ! Alteração de IA - Revisar: módulo novo (07/11/2026, Pós-Fase 4, pacote Q1): a camada de leitura dos verbetes. Gera, a
# partir do frontmatter e das seções de cada verbete de `Programacao/AgenteCore/biblioteca_producao/`, um arquivo por
# verbete em `Programacao/AgenteCore/biblioteca_producao_leitura/` (mesmo caminho relativo, mesmo id, os mesmos campos do
# cabeçalho e quatro blocos para quem lê: o que é, como aparece na tela, o que conferir, onde está no código), com um
# índice; confere que cada verbete tem a sua leitura e que nenhuma leitura diverge do cabeçalho do verbete; e respeita a
# curadoria à mão (um arquivo com `curado: sim` no cabeçalho nunca é regravado). A biblioteca de produção não é lida por
# nada além de `biblioteca.carregar`, e nenhum arquivo dela muda.
# ! Motivo: decisão 103 (ficha 51, 07/11/2026): normalizar os verbetes mudaria o que o modelo lê e obrigaria a medir de
# novo (decisões 69 e 95); o que chega ao analista sai de uma camada fora da biblioteca, gerada por código e curada à mão,
# que o relatório v3, a árvore de decisão e o hub citam. A busca (`recuperacao.py`) e o prompt continuam lendo só a
# biblioteca (hash `95af35290860`); o teste `testar_pos_fase4.py` confere que a leitura não entra no prompt.
"""Uso (em Programacao/AgenteCore/experimentos):
  PYTHONIOENCODING=utf-8 python biblioteca_leitura.py --gerar
  PYTHONIOENCODING=utf-8 python biblioteca_leitura.py --check
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import sys
from pathlib import Path

import biblioteca as bib
import caminhos

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    with contextlib.suppress(OSError, ValueError, AttributeError):
        sys.stdout.reconfigure(encoding="utf-8")

PASTA_BIBLIOTECA = caminhos.AQUI.parent / "biblioteca_producao"
PASTA_LEITURA = caminhos.AQUI.parent / "biblioteca_producao_leitura"
RAIZ_DO_REPOSITORIO = caminhos.AQUI.parent.parent.parent
# A frase que abre toda leitura: é o que o teste procura no prompt para provar que a camada não entra nele.
MARCA_DA_LEITURA = "Camada de leitura do verbete"
# Os campos que a leitura acrescenta ao cabeçalho copiado do verbete.
CAMPOS_PROPRIOS = ("verbete", "hash_do_verbete", "gerado_em", "curado")
SECOES_DA_LEITURA = ("O que é", "Como aparece na tela", "O que conferir", "Onde está no código", "Notas do modelo", "Curadoria")
# Código de situação sempre com o significado junto (regra de escrita dos comentários deste repositório).
TIPO_EM_PALAVRAS = {
    "funcionamento": "descreve como uma parte do sistema funciona",
    "regra": "regra de negócio do sistema",
    "contrato": "o contrato de uma rota da API, campo a campo",
    "erro": "uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta",
    "defeito_conhecido": "um defeito real do código cedido, mantido de propósito",
    "limite": "o que o sistema não faz",
    "aprendido": "escrito pelo modelo a partir de um caso, nas Fases 3 e 4, e aceito pela validação em código e pela revisão",
}
STATUS_EM_PALAVRAS = {"ativo": "em vigor", "corrigido": "defeito corrigido no sistema", "nao_corrigido": "defeito sem correção no código cedido",
                      "obsoleto": "fora de uso"}
SISTEMA_EM_PALAVRAS = {"CobaiaFront": "o site PHP", "CobaiaAPI": "a API", "Ambos": "o site PHP e a API", "Infraestrutura": "servidor, banco e rede"}
TEXTO_DA_CURADORIA = ("Nada ainda. Escreva aqui o que corrigir ou acrescentar e troque `curado: nao` por `curado: sim` no cabeçalho: "
                      "a partir daí o gerador deixa de regravar este arquivo, e `--check` só avisa se o verbete de origem mudar.")


def hash_do_verbete(caminho: Path) -> str:
    """Os 16 primeiros caracteres do sha256 dos bytes do verbete: muda com qualquer byte, e é o que a leitura guarda."""
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()[:16]


def _sem_travessao(texto: str) -> str:
    """Troca travessão e seta por pontuação e palavras (regra dos documentos); o verbete de origem fica como está."""
    return (texto.replace(" — ", ": ").replace("—", ":").replace(" → ", " leva a ").replace("→", " leva a ")
            .replace(" ↔ ", " e ").replace("↔", " e "))


def _lista(valores) -> str:
    return ", ".join(f"`{v}`" for v in valores)


def _frase(texto: str) -> str:
    texto = texto.strip()
    return texto if not texto or texto.endswith((".", "!", "?", ":")) else texto + "."


def _valor_do_cabecalho(valor) -> str:
    """O valor no mesmo subconjunto plano de YAML que `biblioteca._parse_frontmatter` lê (lista entre colchetes, separada por vírgula)."""
    return "[" + ", ".join(valor) + "]" if isinstance(valor, list) else str(valor)


def caminho_relativo(v: dict, raiz_bib: Path) -> str:
    return Path(v["caminho"]).relative_to(raiz_bib).as_posix()


def _titulos_por_causa(verbetes: list[dict]) -> dict[str, str]:
    return {x["meta"]["causa_raiz"]: x["meta"]["titulo"] for x in verbetes if x["meta"].get("tipo") == "erro" and x["meta"].get("causa_raiz")}


def _itens(secao: str) -> list[str]:
    return [ln.lstrip("-* ").strip() for ln in secao.splitlines() if ln.strip()]


def leitura_do_verbete(v: dict, verbetes: list[dict], raiz_bib: Path, gerado_em: str) -> str:
    """O texto da leitura de um verbete: o cabeçalho copiado (mesmos campos, mesmos valores) mais os campos próprios, e os blocos
    para quem lê, escritos só com o que o verbete traz (frontmatter e seções); as notas do modelo saem rotuladas como texto do modelo."""
    m, s = v["meta"], v["secoes"]
    rel = caminho_relativo(v, raiz_bib)
    titulos = _titulos_por_causa(verbetes)
    tipo, status, sistema = m.get("tipo", ""), m.get("status", ""), m.get("sistema", "")
    cab = ["---",
           (f"# ! Alteração de IA - Revisar: camada de leitura do verbete `{v['id']}`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de "
            f"biblioteca_producao/{rel} (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão."),
           ("# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, "
            "na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o "
            "gerador deixa de regravar o arquivo.")]
    for chave, valor in m.items():
        cab.append(f"{chave}: {_valor_do_cabecalho(valor)}")
    cab += [f"verbete: {rel}", f"hash_do_verbete: {hash_do_verbete(v['caminho'])}", f"gerado_em: {gerado_em}", "curado: nao", "---"]

    abertura = (f"{MARCA_DA_LEITURA} `{v['id']}` (`biblioteca_producao/{rel}`). Tipo: {tipo} ({TIPO_EM_PALAVRAS.get(tipo, 'tipo não previsto')}); "
                f"estado: {status} ({STATUS_EM_PALAVRAS.get(status, 'estado não previsto')}); sistema: {sistema} ({SISTEMA_EM_PALAVRAS.get(sistema, 'sistema não previsto')}); "
                f"entidade principal: {m.get('entidade_principal', 'não declarada')}.")
    if m.get("causa_raiz"):
        abertura += f" Trata da causa `{m['causa_raiz']}` da taxonomia: é o verbete que o agente cita quando responde essa causa."

    o_que_e = _sem_travessao(s.get("Resumo", "").strip()) or "O verbete não traz resumo."

    sinais = [_sem_travessao(x) for x in _itens(s.get("Sinais", ""))]
    como_aparece = [f"- {_frase(x)}" for x in sinais] if sinais else ["- O verbete não lista sinais; valem os sintomas do cabeçalho, abaixo."]
    # ! Alteração de IA - Revisar: (07/11/2026, Pós-Fase 4, pacote Q2) os sintomas e as palavras-chave do cabeçalho saem entre crases, e cada nota do modelo vira
    # citação do Markdown.
    # ! Motivo: são rótulos da busca e texto do modelo, não escrita desta camada; os filtros de texto (filtros_de_texto.py) contavam neles "timeout", "token", "enum",
    # "hash" e "schema" como jargão sem explicação da leitura, em 7 das 39 leituras, e a citação é a forma que o relatório v3 usa para o que o modelo escreveu.
    if m.get("sintomas"):
        como_aparece += ["", "Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): " + _lista(m["sintomas"]) + "."]

    conferir = []
    if s.get("Causa"):
        conferir.append("Causa, como o verbete a descreve: " + _frase(_sem_travessao(s["Causa"].strip())))
    if s.get("Como confirmar"):
        conferir.append("Como confirmar: " + _frase(_sem_travessao(s["Como confirmar"].strip())))
    if not conferir:
        conferir.append("O verbete não descreve a causa nem como confirmar; confira pelos sinais acima e pelos arquivos abaixo.")
    if m.get("causas_relacionadas"):
        vizinhas = ", ".join(f"`{c}` ({titulos[c]})" if c in titulos else f"`{c}`" for c in m["causas_relacionadas"])
        conferir.append(f"Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): {vizinhas}.")
    correcoes = bib.correcoes(v)
    for c in correcoes:
        conferir.append(f"Correção registrada ({c['data']}, caso {c['caso']}): solução sugerida: {_sem_travessao(c['sugerida']) or 'nenhuma registrada'}; "
                        f"solução aplicada: {_sem_travessao(c['aplicada']) or 'nenhuma registrada'}.")

    onde = [("- Arquivos: " + _lista(m["arquivos"]) + ".") if m.get("arquivos") else "- Arquivos: nenhum declarado no cabeçalho.",
            ("- Rotas da API (campo `endpoints`): " + _lista(m["endpoints"]) + ".") if m.get("endpoints") else "- Rotas da API: nenhuma declarada.",
            ("- Tabelas do banco: " + _lista(m["tabelas"]) + ".") if m.get("tabelas") else "- Tabelas do banco: nenhuma declarada."]
    if m.get("palavras_chave"):
        onde.append("- Palavras que a busca usa para achar este verbete: " + _lista(m["palavras_chave"]) + ".")

    notas = bib.notas(v)
    if notas:
        bloco_notas = ["O que segue é texto do modelo, acrescentado durante as Fases 3 e 4 e aceito na curadoria; não foi conferido por código."]
        for n in notas:
            operacao = "nota" if n["operacao"] == "nota" else ("retificação de \"" + _sem_travessao(n["trecho"]) + "\"" if n["trecho"] else "retificação")
            bloco_notas += ["", f"> [época {n['epoca']}, caso {n['caso']}, {operacao}] {_frase(_sem_travessao(n['texto']))} Motivo: {_frase(_sem_travessao(n['motivo']))}"]
    else:
        bloco_notas = ["Nenhuma nota do modelo neste verbete."]

    partes = cab + ["", f"# {m.get('titulo', v['id'])}", "", abertura, "",
                    "## O que é", "", o_que_e, "",
                    "## Como aparece na tela", "", *como_aparece, "",
                    "## O que conferir", "", "\n\n".join(conferir), "",
                    "## Onde está no código", "", *onde, "",
                    "## Notas do modelo", "", *bloco_notas, "",
                    "## Curadoria", "", TEXTO_DA_CURADORIA, ""]
    return "\n".join(partes)


def _indice(verbetes: list[dict], raiz_bib: Path, raiz_leitura: Path, gerado_em: str) -> str:
    linhas = []
    for v in sorted(verbetes, key=lambda x: (x["pasta"], x["id"])):
        rel = caminho_relativo(v, raiz_bib)
        destino = raiz_leitura / rel
        curado = "não"
        if destino.exists():
            try:
                curado = "sim" if bib._parse_frontmatter(destino.read_text(encoding="utf-8"))[0].get("curado") == "sim" else "não"
            except ValueError:
                curado = "cabeçalho ilegível"
        linhas.append(f"| {v['pasta']} | `{v['id']}` | {v['meta'].get('titulo', '')} | {v['meta'].get('tipo', '')} | {v['meta'].get('causa_raiz') or ''} | "
                      f"{curado} | [{rel}]({rel}) |")
    return "\n".join([
        "<!-- ! Alteração de IA - Revisar: índice da camada de leitura, GERADO por biblioteca_leitura.py --gerar; não editar à mão.",
        "     ! Motivo: quem revisa a camada precisa ver num lugar só quais verbetes têm leitura, de que tipo e quais já foram curados à mão. -->",
        "", "# Camada de leitura da biblioteca de produção", "",
        (f"{len(verbetes)} leituras, uma por verbete de `biblioteca_producao/`, geradas em {gerado_em} por `experimentos/biblioteca_leitura.py`. "
         "A biblioteca que o modelo lê não muda; esta pasta é o que o analista lê (decisão 103). Uma leitura com `curado: sim` no cabeçalho "
         "foi revisada à mão e o gerador não a regrava."), "",
        "| Pasta | Id | Título | Tipo | Causa | Curada à mão | Arquivo |", "|---|---|---|---|---|---|---|", *linhas, ""])


def gerar(raiz_bib: Path = PASTA_BIBLIOTECA, raiz_leitura: Path = PASTA_LEITURA, gerado_em: str | None = None) -> dict:
    """Grava a leitura de cada verbete (e o índice); devolve {gerados: [ids], mantidos: [ids com curado: sim], indice: Path}.
    Um arquivo igual ao que seria gerado não é regravado, e um arquivo curado à mão nunca é tocado."""
    raiz_bib, raiz_leitura = Path(raiz_bib), Path(raiz_leitura)
    gerado_em = gerado_em or dt.date.today().isoformat()
    verbetes = bib.carregar(raiz_bib)
    gerados, mantidos = [], []
    for v in verbetes:
        destino = raiz_leitura / caminho_relativo(v, raiz_bib)
        atual = destino.read_text(encoding="utf-8") if destino.exists() else None
        if atual is not None:
            try:
                if bib._parse_frontmatter(atual)[0].get("curado") == "sim":
                    mantidos.append(v["id"])
                    continue
            except ValueError:
                pass
        texto = leitura_do_verbete(v, verbetes, raiz_bib, gerado_em)
        if atual != texto:
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(texto, encoding="utf-8", newline="\n")
        gerados.append(v["id"])
    indice = raiz_leitura / "INDICE.md"
    texto_indice = _indice(verbetes, raiz_bib, raiz_leitura, gerado_em)
    if not indice.exists() or indice.read_text(encoding="utf-8") != texto_indice:
        indice.parent.mkdir(parents=True, exist_ok=True)
        indice.write_text(texto_indice, encoding="utf-8", newline="\n")
    return {"gerados": gerados, "mantidos": mantidos, "indice": indice}


def carregar(raiz_leitura: Path = PASTA_LEITURA) -> dict[str, dict]:
    """{id do verbete: leitura}, com título, caminho relativo, cabeçalho, seções, se foi curada à mão e a causa (dos verbetes de erro)."""
    saida: dict[str, dict] = {}
    raiz_leitura = Path(raiz_leitura)
    if not raiz_leitura.is_dir():
        return saida
    for v in bib.carregar(raiz_leitura):
        m = v["meta"]
        saida[v["id"]] = {"id": v["id"], "titulo": m.get("titulo", v["id"]), "caminho": Path(v["caminho"]).relative_to(raiz_leitura).as_posix(),
                          "meta": m, "secoes": v["secoes"], "curado": m.get("curado") == "sim", "causa_raiz": m.get("causa_raiz"),
                          "tipo": m.get("tipo"), "verbete": m.get("verbete"), "hash_do_verbete": m.get("hash_do_verbete")}
    return saida


def conferir(raiz_bib: Path = PASTA_BIBLIOTECA, raiz_leitura: Path = PASTA_LEITURA) -> list[str]:
    """As falhas da camada contra a biblioteca: verbete sem leitura, leitura sem verbete, campo do cabeçalho diferente, caminho ou
    `curado` fora do formato, e verbete que mudou depois da leitura (hash gravado diferente do atual). Vazia = tudo bate."""
    raiz_bib, raiz_leitura = Path(raiz_bib), Path(raiz_leitura)
    if not raiz_leitura.is_dir():
        return [f"pasta da camada de leitura não existe: {raiz_leitura}"]
    verbetes = bib.carregar(raiz_bib)
    leituras = carregar(raiz_leitura)
    falhas = []
    for v in verbetes:
        rel = caminho_relativo(v, raiz_bib)
        l = leituras.get(v["id"])
        if l is None:
            falhas.append(f"{v['id']}: sem leitura (esperada em {rel})")
            continue
        if l["caminho"] != rel:
            falhas.append(f"{v['id']}: leitura em {l['caminho']}, esperada em {rel}")
        for chave, valor in v["meta"].items():
            if l["meta"].get(chave) != valor:
                falhas.append(f"{v['id']}: campo {chave} difere do verbete (leitura {l['meta'].get(chave)!r}, verbete {valor!r})")
        if l["meta"].get("verbete") != rel:
            falhas.append(f"{v['id']}: campo verbete aponta {l['meta'].get('verbete')!r}, esperado {rel!r}")
        if l["meta"].get("curado") not in ("sim", "nao"):
            falhas.append(f"{v['id']}: campo curado {l['meta'].get('curado')!r} fora de (sim, nao)")
        atual = hash_do_verbete(v["caminho"])
        if l["meta"].get("hash_do_verbete") != atual:
            falhas.append(f"{v['id']}: o verbete mudou depois da leitura (hash atual {atual}, gravado {l['meta'].get('hash_do_verbete')}); "
                          f"{'revise a leitura curada' if l['curado'] else 'regere com --gerar'}")
    ids = {v["id"] for v in verbetes}
    for i, l in sorted(leituras.items()):
        if i not in ids:
            falhas.append(f"{i}: leitura sem verbete na biblioteca ({l['caminho']})")
    return falhas


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gerar", action="store_true", help="grava a leitura de cada verbete e o índice (não toca em leitura curada à mão)")
    ap.add_argument("--check", action="store_true", help="confere a camada contra a biblioteca; código 1 se algo diverge")
    ap.add_argument("--raiz", default=str(PASTA_BIBLIOTECA), help="pasta da biblioteca (padrão: biblioteca_producao)")
    ap.add_argument("--destino", default=str(PASTA_LEITURA), help="pasta da camada de leitura (padrão: biblioteca_producao_leitura)")
    args = ap.parse_args()
    if not (args.gerar or args.check):
        ap.error("informe --gerar ou --check")
    if args.gerar:
        r = gerar(Path(args.raiz), Path(args.destino))
        print(f"gerados {len(r['gerados'])} e mantidos {len(r['mantidos'])} (curados à mão); índice em {r['indice']}")
    falhas = conferir(Path(args.raiz), Path(args.destino))
    for f in falhas:
        print("  " + f)
    print(f"--check: {'tudo bate' if not falhas else str(len(falhas)) + ' falha(s)'}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
