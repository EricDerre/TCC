# ! Alteração de IA - Revisar: script novo (21/09/2026) que transforma o JSON da pesquisa (`r2-entrada.json` ou
# `r2-final.json`) nas subseções §6.9.N do levantamento, no bloco de afirmações rejeitadas (§6.9.17) e nos blocos
# novos de `referencias.md`, com dedup contra as referências já existentes; `--check` regera as subseções da rodada 1
# (§6.9.1–6.9.8) e compara com o que está no Memorial, para provar que o formato é o mesmo.
# ! Motivo: a rodada 1 foi colada à mão em 11/09 e ficou com duas linhas de depuração no meio do arquivo; a rodada 2
# entra por script (processamento local, sem tokens), no formato exato das oito subseções existentes, e o que foi
# rejeitado na verificação fica registrado com o motivo — o Eric pediu que o descartado também seja documentado.
"""Uso:
  python ferramentas/render_levantamento.py --check                    # regera §6.9.1–6.9.8 e compara com o Memorial
  python ferramentas/render_levantamento.py --entrada r2-final.json --saida pasta/   # grava r2-secoes.md, r2-rejeitadas.md, r2-referencias.md
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parents[1]
SDD = RAIZ / ".superpowers" / "sdd" / "fase3b-e-fechamento"
LEVANTAMENTO = RAIZ / "Documentacao" / "memorial" / "2-pesquisa-e-literatura" / "levantamento-2026-09-11-fase-3.md"
REFERENCIAS = RAIZ / "Documentacao" / "memorial" / "2-pesquisa-e-literatura" / "referencias.md"

# Título curto de cada subseção (o do cabeçalho `#### 6.9.N`), na ordem em que entram no arquivo.
TITULOS_CURTOS = {
    "faceli": "Fontes brasileiras e o livro-texto (Faceli et al., 3. ed., 2025)",
    "tokenizacao": "Tokenização",
    "arquitetura": "Arquitetura de inferência em CPU",
    "otimizacao": "Otimização de recursos e de tokens em CPU",
    "rag": "RAG, perda de contexto e recuperação",
    "memoria": "Memória gerida pelo próprio modelo",
    "selfhealing": "Self-healing, árvore de acessibilidade e contrato",
    "metricas": "Métricas e desenho experimental",
    "r2-conflito-contexto-conhecimento-e-sicofancia-documental": "Conflito entre contexto recuperado e conhecimento paramétrico (sicofância documental)",
    "r2-validacao-de-artefatos-gerados-e-limites-da-autocorrecao": "Validação em código de artefatos escritos por LLM e limites da autocorreção",
    "r2-metricas-de-qualidade-de-documentacao-e-inconsistencia-doc-codigo": "Qualidade de documentação técnica e inconsistência documento–código",
    "r2-recuperacao-em-corpus-pequeno-curado-e-crescente": "O recuperador como teto: BM25 em corpus pequeno, curado e crescente",
    "r2-aprendizado-sem-atualizacao-de-pesos-e-ancoragem-em-faceli": "Aprender sem atualizar pesos e a ancoragem no livro-guia",
    "r2-prompting-em-estagios-e-cot-em-modelos-pequenos": "Decomposição em estágios e cadeia de pensamento em modelos pequenos",
    "r2-taxonomia-rotulos-ouro-e-rca-com-llm": "Taxonomia de causa raiz, rótulos-ouro e RCA com LLM",
    "r2-agente-autonomo-de-qa-autonomia-e-supervisao": "Arquitetura de agentes autônomos de QA: autonomia, guardrails e supervisão",
}
ORDEM_R1 = ("faceli", "tokenizacao", "arquitetura", "otimizacao", "rag", "memoria", "selfhealing", "metricas")
ORDEM_R2 = tuple(k for k in TITULOS_CURTOS if k.startswith("r2-"))


def _texto_rebaixado(texto: str) -> str:
    """Títulos internos da síntese (`### …`) viram negrito, como na rodada 1."""
    linhas = []
    for l in (texto or "").replace("\r\n", "\n").split("\n"):
        m = re.match(r"^#{1,6}\s+(.*\S)\s*$", l)
        linhas.append(f"**{m.group(1)}**" if m else l)
    return "\n".join(linhas).strip("\n")


def eh_alem_do_teto(r: dict) -> bool:
    return "além do teto" in (r.get("motivo") or "")


def contagem(item: dict) -> tuple[int, int, int]:
    """(aprovadas, rejeitadas por veredito, não verificadas por exceder o teto de 20)."""
    rej = item.get("rejeitadas") or []
    teto = sum(1 for r in rej if eh_alem_do_teto(r))
    return len(item.get("verified") or []), len(rej) - teto, teto


def secao(numero: int, key: str, item: dict) -> str:
    s = item.get("synthesis") or {}
    n_ok, n_rej, n_teto = contagem(item)
    plural = lambda n, um, muitos: um if n == 1 else muitos
    # "não verificada" (além do teto de 20 por tópico) não é rejeição: o verificador nunca a avaliou
    sufixo = f", {n_teto} não {plural(n_teto, 'verificada', 'verificadas')}" if n_teto else ""
    partes = [
        f"#### 6.9.{numero} {TITULOS_CURTOS.get(key, item.get('titulo', key))} (`{key}` — {n_ok} {plural(n_ok, 'aprovada', 'aprovadas')}, {n_rej} {plural(n_rej, 'rejeitada', 'rejeitadas')}{sufixo})",
        "",
        # alguns sintetizadores prefixam o título com o número da seção ("6.10 …", "6.9.9 …"); o número é do Memorial, não do título
        f"*Título da síntese:* {re.sub(r'^\s*\d+(\.\d+)+\s+', '', s.get('titulo', '(sem síntese)'))}",
        "",
        "##### Texto",
        "",
        _texto_rebaixado(s.get("texto_memorial_pt", "*(síntese ausente: a lacuna não chegou a ser fechada)*")),
        "",
        "##### Implicações para a Fase 3",
        "",
        *[f"* {x}" for x in s.get("implicacoes_fase3_pt", [])],
        "",
        "##### Lacunas",
        "",
        *[f"* {x}" for x in s.get("lacunas_pt", [])],
        "",
        "##### Referências ABNT do tópico",
        "",
        *[f"- {x}" for x in s.get("referencias_abnt", [])],
        "",
    ]
    return "\n".join(partes)


def bloco_rejeitadas(numero: int, dados: dict) -> str:
    partes = [f"#### 6.9.{numero} Afirmações rejeitadas ou de suporte parcial nas rodadas 1 e 2 (com o motivo)", "",
              "Cada linha é uma afirmação que um pesquisador trouxe e o verificador cético não confirmou (fonte inexistente, ano anterior a 2024 sem ser clássico, número ou condição que a fonte não sustenta, ou fonte que não abriu). Ficam aqui para que o descarte seja rastreável; nenhuma delas foi usada nas sínteses.", ""]
    for rodada, chaves in (("Rodada 1", ORDEM_R1), ("Rodada 2", ORDEM_R2)):
        partes.append(f"**{rodada}**"); partes.append("")
        for k in chaves:
            it = dados.get(k) or {}
            rej = [r for r in (it.get("rejeitadas") or []) if not eh_alem_do_teto(r)]
            teto = [r for r in (it.get("rejeitadas") or []) if eh_alem_do_teto(r)]
            parciais = [v for v in (it.get("verified") or []) if v.get("support") == "partial"]
            if not rej and not parciais and not teto:
                continue
            partes.append(f"*`{k}`* — {len(rej)} rejeitada(s), {len(parciais)} parcial(is), {len(teto)} não verificada(s)")
            for r in rej:
                partes.append(f"- Rejeitada: {r.get('claim', '')} — *fonte declarada:* {r.get('fonte', '')} — *motivo:* {r.get('motivo', '')}")
            for r in teto:
                partes.append(f"- Não verificada: {r.get('claim', '')} — *fonte declarada:* {r.get('fonte', '')} — *motivo:* {r.get('motivo', '')}")
            for v in parciais:
                partes.append(f"- Parcial: {v.get('claim_pt', '')} — *número que a fonte sustenta:* {v.get('number', '')} — *ref.:* {v.get('ref', '')}")
            partes.append("")
    return "\n".join(partes)


def _titulo_de(ref: str) -> str:
    """Título da referência: o trecho em negrito (blocos antigos) ou o primeiro segmento entre pontos que
    lê como título (três ou mais palavras de três letras ou mais, sem ponto e vírgula de lista de autores)."""
    m = re.search(r"\*\*(.+?)\*\*", ref)
    if m:
        return m.group(1)
    # o primeiro segmento é sempre a lista de autores (com autor único e nome por extenso ele também
    # "lê como título"; foi o que duplicou STEKEL/MTEB-BR em 21/09) — a busca começa no segundo
    for seg in re.split(r"\.\s+", ref)[1:]:
        if ";" in seg:
            continue
        palavras = re.findall(r"[^\W\d_]{3,}", seg)
        if len(palavras) >= 3 and any(w.islower() or w[1:].islower() for w in palavras):
            return seg
    return ""


def _chave_ref(ref: str) -> str:
    """sobrenome + ano + 3 primeiras palavras do título, sem acento/caixa — chave de dedup."""
    t = unicodedata.normalize("NFKD", ref).encode("ascii", "ignore").decode().lower()
    titulo = unicodedata.normalize("NFKD", _titulo_de(ref)).encode("ascii", "ignore").decode().lower()
    sobrenome = re.match(r"\s*([a-z' -]+?),", t)
    ano = re.search(r"\b(19|20)\d{2}\b", t)
    palavras = re.findall(r"[a-z0-9]+", titulo)[:3]
    return f"{(sobrenome.group(1).strip() if sobrenome else '?')}|{ano.group(0) if ano else '?'}|{' '.join(palavras)}"


def referencias_existentes() -> dict[str, str]:
    chaves = {}
    for l in REFERENCIAS.read_text(encoding="utf-8").splitlines():
        if l.startswith("- "):
            chaves[_chave_ref(l[2:])] = l[2:]
    return chaves


def bloco_referencias(dados: dict, chaves: tuple[str, ...], rotulo: str) -> tuple[str, list[str]]:
    existentes = referencias_existentes()
    novas: dict[str, str] = {}
    quase: list[str] = []
    for k in chaves:
        for ref in ((dados.get(k) or {}).get("synthesis") or {}).get("referencias_abnt", []):
            ch = _chave_ref(ref)
            if ch in existentes:
                continue
            sob_ano = ch.rsplit("|", 1)[0]
            if any(e.startswith(sob_ano + "|") for e in existentes) and ch not in novas:
                quase.append(f"{ref[:90]}  ~  {next(e for e in existentes.values() if _chave_ref(e).startswith(sob_ano + '|'))[:90]}")
            novas.setdefault(ch, ref)
    linhas = [f"### Rodada 2 do levantamento ({rotulo})", "",
              "<!-- ! Alteração de IA - Revisar: bloco gerado por ferramentas/render_levantamento.py a partir das sínteses da rodada 2; referências já presentes acima foram omitidas (dedup por sobrenome + ano + título).",
              "     ! Motivo: cada síntese traz a sua lista ABNT; sem dedup as mesmas fontes entrariam duas vezes e o total do arquivo ficaria errado. -->", ""]
    linhas += [f"- {r}" for r in sorted(novas.values(), key=lambda x: unicodedata.normalize('NFKD', x).lower())]
    return "\n".join(linhas) + "\n", quase


def secoes_atuais() -> dict[str, str]:
    """Subseções `#### 6.9.N …` do Memorial, por key (entre crases no cabeçalho)."""
    texto = LEVANTAMENTO.read_text(encoding="utf-8").replace("\r\n", "\n")
    partes = re.split(r"(?m)^(?=#### 6\.9\.)", texto)
    saida = {}
    for p in partes:
        m = re.match(r"#### 6\.9\.\d+ .*?\(`([a-z0-9-]+)`", p)
        if m:
            saida[m.group(1)] = p
    return saida


def _normalizar(s: str) -> list[str]:
    s = s.replace("\r\n", "\n")
    s = re.sub(r"^(TOTAL sinteses:.*|VERIFICACOES:.*)$", "", s, flags=re.M)  # linhas de depuração do arquivo atual
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)  # tags de IA entre as subseções não fazem parte do texto gerado
    return [l.rstrip() for l in s.strip("\n").split("\n") if l.strip()]


def check(entrada: dict) -> int:
    atuais = secoes_atuais()
    falhas = 0
    dados = {**entrada["r1"], **entrada.get("r2", {})}
    presentes = [k for k in ORDEM_R1 + ORDEM_R2 if k in atuais and (dados.get(k) or {}).get("synthesis")]
    for i, k in enumerate(presentes, start=1):
        gerado = _normalizar(secao(i, k, dados[k]))
        atual = _normalizar(atuais.get(k, ""))
        if gerado == atual:
            print(f"6.9.{i} {k}: idêntico")
            continue
        falhas += 1
        diff = list(difflib.unified_diff(atual, gerado, "memorial", "gerado", lineterm="", n=0))
        print(f"6.9.{i} {k}: DIFERE ({len([d for d in diff if d.startswith(('+', '-')) and not d.startswith(('+++', '---'))])} linhas)")
        for d in diff[:12]:
            print("   ", d[:160])
    return 1 if falhas else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", default=str(SDD / "pesquisa" / "r2-entrada.json"))
    ap.add_argument("--saida", default=str(SDD / "pesquisa"))
    ap.add_argument("--check", action="store_true", help="regera §6.9.1–6.9.8 e compara com o Memorial")
    ap.add_argument("--primeiro-numero", type=int, default=9, help="número da primeira subseção da rodada 2")
    ap.add_argument("--rotulo", default="levantamento de 21/09/2026")
    args = ap.parse_args()
    entrada = json.loads(Path(args.entrada).read_text(encoding="utf-8"))
    if args.check:
        return check(entrada)
    dados = {**entrada["r1"], **entrada["r2"]}
    saida = Path(args.saida); saida.mkdir(parents=True, exist_ok=True)
    secoes = [secao(args.primeiro_numero + i, k, entrada["r2"][k]) for i, k in enumerate(ORDEM_R2)]
    (saida / "r2-secoes.md").write_text("\n".join(secoes), encoding="utf-8", newline="\n")
    (saida / "r2-rejeitadas.md").write_text(bloco_rejeitadas(args.primeiro_numero + len(ORDEM_R2), dados), encoding="utf-8", newline="\n")
    refs, quase = bloco_referencias(dados, ORDEM_R2, args.rotulo)
    (saida / "r2-referencias.md").write_text(refs, encoding="utf-8", newline="\n")
    n_ref = refs.count("\n- ")
    print(f"gravados em {saida}: r2-secoes.md ({len(secoes)} subseções), r2-rejeitadas.md, r2-referencias.md ({n_ref} referências novas)")
    if quase:
        print("quase-duplicatas para conferir (mesmo sobrenome e ano, título diferente):")
        for q in quase:
            print("  ", q)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
