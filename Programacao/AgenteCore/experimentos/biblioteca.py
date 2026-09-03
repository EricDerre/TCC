#!/usr/bin/env python3
# ! Alteração de IA - Revisar: carrega, valida e renderiza a biblioteca de documentação
# (Programacao/AgenteCore/base_conhecimento/) que a Fase 2-B entrega aos modelos como
# fonte da verdade sobre o cobaia.
# ! Motivo: na Fase 2-A os modelos recebiam só o par requisição/resposta e o contrato de
# campos; o melhor acerto ficou em 67,8%. Esta fase mede se documentação do sistema
# (regras de negócio + catálogo de erros com o ponto do código) fecha a lacuna até os
# 70–80% da meta. Para a medição valer, a biblioteca precisa ser validada por código:
# frontmatter completo, referências a arquivos/tabelas/endpoints que existem de fato
# (alucinação acumulada é o risco de uma base escrita à mão), cobertura das 23 causas raiz
# e — o mais importante — nenhum verbete que copie um caso do banco de testes, senão a
# medição vira busca de par e não diagnóstico.
#
# Formato dos verbetes: Markdown com frontmatter num SUBCONJUNTO PLANO de YAML
# (`chave: valor` e `chave: [a, b]`), parseado aqui mesmo com biblioteca padrão. Não usa
# pyyaml de propósito: o AgenteCore só depende de matplotlib, e o subconjunto plano evita
# as conversões implícitas do YAML (ex.: `id: 001` virar inteiro).
import re
import sys
import unicodedata
from pathlib import Path

from taxonomia import CAUSAS_RAIZ

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, igual ao _env_common.py.
# ! Motivo: no Windows o console pode estar em cp1252, que não representa símbolos usados
# nos relatórios (≈, Δ, →) — o script inteiro abortava com UnicodeEncodeError ao imprimir.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

AQUI = Path(__file__).resolve().parent
RAIZ_REPO = AQUI.parents[2]
BASE = AQUI.parent / "base_conhecimento"

# Medido nos 90 prompts lineares da Fase 2-A (caracteres do prompt / prompt_eval_count):
# Granite 2,62 · Qwen2.5 2,83 · phi4-mini 3,19 chars por token. Usa-se o pior caso para
# o validador acusar biblioteca grande demais antes de rodar; o número real de tokens
# entra no registro da bateria via prompt_eval_count.
CHARS_POR_TOKEN = 2.6
# Orçamento no num_ctx de 8192: maior caso linear ~1.250 tokens + resposta ≤ 900 + margem.
# Fica ACIMA dos ~2.500 tokens em que a literatura mede degradação (Context Rot) — de
# propósito: o braço "biblioteca inteira" existe para medir exatamente esse custo.
TETO_TOKENS_BIBLIOTECA = 6700
TETO_CHARS_VERBETE = 550  # renderizado; 36 verbetes × ~470 chars ≈ 17k chars ≈ 6,5k tokens

SISTEMAS = {"CobaiaFront", "CobaiaAPI", "Infraestrutura", "Ambos"}
ENTIDADES = {"Produto", "Tipo", "Usuario", "Pedido", "Interface", "Infraestrutura"}
TIPOS = {"funcionamento", "regra", "contrato", "erro", "defeito_conhecido", "limite"}
STATUS = {"ativo", "corrigido", "nao_corrigido", "obsoleto"}
# Nomes reais, conferidos em CobaiaFront/banco/bancoatualizado.sql e schema_completo.sql.
TABELAS = {"tbtipos", "tbprodutos", "tbusuarios", "tbpedido_reserva",
           "vw_tbpedidos", "vw_tbprodutos"}
# Rotas reais, conferidas em CobaiaAPI/app/routers/*.py.
ENDPOINTS = {"GET /api/produtos", "GET /api/produtos/{id}", "GET /api/pedidos",
             "POST /api/pedidos", "POST /api/pedidos/{id}/cancelar",
             "GET /api/admin/fault-mode", "POST /api/admin/fault-mode"}
OBRIGATORIOS = ("id", "titulo", "sistema", "entidade_principal", "tipo", "status",
                "palavras_chave")
SECOES = ("Resumo", "Sinais", "Causa", "Como confirmar")

_STOP = set("""a o os as um uma uns umas de do da dos das em no na nos nas por para com sem
sobre entre e ou que se ao aos à às é são foi ser está estão como mais menos muito não sim
ele ela eles elas isso isto esse essa este esta seu sua seus suas ja já so só ate até""".split())


def normalizar(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto)
    limpo = "".join(c for c in sem_acento if not unicodedata.combining(c)).lower()
    return re.sub(r"\s+", " ", limpo).strip()


def tokens(texto: str) -> list[str]:
    """Palavras normalizadas, sem stopwords — a mesma tokenização para BM25 e para a
    checagem de sobreposição com os casos."""
    return [t for t in re.findall(r"[a-z0-9_$\.]+", normalizar(texto)) if t not in _STOP]


def _shingles(palavras: list[str], n: int = 5) -> set[tuple[str, ...]]:
    return {tuple(palavras[i:i + n]) for i in range(len(palavras) - n + 1)}


def _parse_frontmatter(texto: str) -> tuple[dict, str]:
    if not texto.startswith("---"):
        raise ValueError("arquivo não começa com '---'")
    fim = texto.find("\n---", 3)
    if fim < 0:
        raise ValueError("frontmatter sem '---' de fechamento")
    meta = {}
    for linha in texto[3:fim].strip().splitlines():
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        if ":" not in linha:
            raise ValueError(f"linha de frontmatter sem ':' — {linha!r}")
        chave, valor = linha.split(":", 1)
        chave, valor = chave.strip(), valor.strip()
        if valor.startswith("[") and valor.endswith("]"):
            meta[chave] = [v.strip() for v in valor[1:-1].split(",") if v.strip()]
        else:
            meta[chave] = valor
    return meta, texto[fim + 4:]


def _parse_secoes(corpo: str) -> dict[str, str]:
    secoes, atual = {}, None
    for linha in corpo.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", linha)
        if m:
            atual = m.group(1)
            secoes[atual] = ""
        elif atual is not None:
            secoes[atual] += linha + "\n"
    return {k: v.strip() for k, v in secoes.items()}


def carregar(raiz: Path = BASE) -> list[dict]:
    """Lê todos os verbetes. Cada um vira {id, pasta, caminho, meta, secoes}."""
    verbetes = []
    for arq in sorted(raiz.rglob("*.md")):
        if arq.name.upper() == "INDICE.MD":
            continue
        texto = arq.read_text(encoding="utf-8")
        try:
            meta, corpo = _parse_frontmatter(texto)
        except ValueError as e:
            meta, corpo = {"_erro": str(e)}, texto
        verbetes.append({
            "id": meta.get("id", arq.stem),
            "pasta": arq.parent.name,
            "caminho": arq,
            "meta": meta,
            "secoes": _parse_secoes(corpo),
        })
    return verbetes


def por_causa(verbetes: list[dict]) -> dict[str, dict]:
    """Causa raiz -> verbete dedicado (tipo 'erro' com campo causa_raiz)."""
    return {v["meta"]["causa_raiz"]: v for v in verbetes
            if v["meta"].get("tipo") == "erro" and v["meta"].get("causa_raiz")}


def causas_com_defeito_documentado(verbetes: list[dict]) -> set[str]:
    """Causas que algum verbete de defeito conhecido lista em causas_relacionadas — é o
    corte 'com × sem defeito documentado' pedido para os resultados."""
    saida = set()
    for v in verbetes:
        if v["meta"].get("tipo") == "defeito_conhecido":
            saida.update(v["meta"].get("causas_relacionadas", []))
    return saida


# ----------------------------------------------------------------- renderização

def _sinais(v: dict) -> str:
    itens = [re.sub(r"^[-*]\s*", "", ln).strip()
             for ln in v["secoes"].get("Sinais", "").splitlines() if ln.strip()]
    return "; ".join(itens)


def render(v: dict) -> str:
    """Forma compacta que vai ao prompt — a MESMA em todos os braços, para que a única
    diferença entre 'biblioteca inteira' e 'recuperada' seja a seleção, não a
    profundidade. Uma linha de título com o id (é o que o modelo cita em FONTE) e um
    parágrafo com resumo, sinais, causa e como confirmar."""
    s = v["secoes"]
    partes = [s.get("Resumo", "").replace("\n", " ")]
    sinais = _sinais(v)
    if sinais:
        partes.append(f"Sinais: {sinais}.")
    if s.get("Causa"):
        partes.append(f"Causa: {s['Causa'].replace(chr(10), ' ')}")
    if s.get("Como confirmar"):
        partes.append(f"Confirmar: {s['Como confirmar'].replace(chr(10), ' ')}")
    return f"[{v['id']}] {v['meta'].get('titulo', '')}\n" + " ".join(p for p in partes if p)


CABECALHO = ("DOCUMENTAÇÃO DO SISTEMA (fonte da verdade — consulte antes de concluir; "
             "cada verbete tem um identificador entre colchetes)")

_ORDEM_PASTAS = ("negocio", "contratos", "falhas_injetadas", "defeitos_conhecidos", "erros")


def render_biblioteca(verbetes: list[dict]) -> str:
    ordenados = sorted(verbetes, key=lambda v: (_ORDEM_PASTAS.index(v["pasta"])
                                                if v["pasta"] in _ORDEM_PASTAS else 99,
                                                v["id"]))
    return CABECALHO + "\n\n" + "\n\n".join(render(v) for v in ordenados)


def estimar_tokens(texto: str) -> int:
    return round(len(texto) / CHARS_POR_TOKEN)


# --------------------------------------------------------------------- validação

def _texto_completo(v: dict) -> str:
    return " ".join([v["meta"].get("titulo", ""), *v["secoes"].values()])


def validar(verbetes: list[dict], casos: list[dict], limiar_sobreposicao: float = 0.3
            ) -> list[str]:
    """Devolve a lista de problemas — vazia significa biblioteca válida."""
    problemas = []
    ids = [v["id"] for v in verbetes]
    for dup in {i for i in ids if ids.count(i) > 1}:
        problemas.append(f"id repetido: {dup}")

    causas_dedicadas = {}
    for v in verbetes:
        m, rot = v["meta"], f"{v['pasta']}/{v['caminho'].name}"
        if "_erro" in m:
            problemas.append(f"{rot}: frontmatter ilegível — {m['_erro']}")
            continue
        for k in OBRIGATORIOS:
            if not m.get(k):
                problemas.append(f"{rot}: falta '{k}' no frontmatter")
        if m.get("id") != v["caminho"].stem:
            problemas.append(f"{rot}: id '{m.get('id')}' diferente do nome do arquivo")
        for campo, permitidos in (("sistema", SISTEMAS), ("entidade_principal", ENTIDADES),
                                  ("tipo", TIPOS), ("status", STATUS)):
            if m.get(campo) and m[campo] not in permitidos:
                problemas.append(f"{rot}: {campo}='{m[campo]}' fora de {sorted(permitidos)}")
        for caminho in m.get("arquivos", []):
            if not (RAIZ_REPO / caminho).exists():
                problemas.append(f"{rot}: arquivo inexistente '{caminho}'")
        for t in m.get("tabelas", []):
            if t not in TABELAS:
                problemas.append(f"{rot}: tabela inexistente '{t}'")
        for e in m.get("endpoints", []):
            if e not in ENDPOINTS:
                problemas.append(f"{rot}: endpoint inexistente '{e}'")
        for c in m.get("causas_relacionadas", []):
            if c not in CAUSAS_RAIZ:
                problemas.append(f"{rot}: causa_relacionada '{c}' fora do conjunto fechado")
        if m.get("tipo") == "erro":
            causa = m.get("causa_raiz")
            if causa not in CAUSAS_RAIZ:
                problemas.append(f"{rot}: verbete de erro sem causa_raiz válida ('{causa}')")
            elif causa in causas_dedicadas:
                problemas.append(f"{rot}: causa '{causa}' já tem verbete ({causas_dedicadas[causa]})")
            else:
                causas_dedicadas[causa] = v["id"]
        if not v["secoes"].get("Resumo"):
            problemas.append(f"{rot}: sem seção '## Resumo'")
        for sec in v["secoes"]:
            if sec not in SECOES:
                problemas.append(f"{rot}: seção desconhecida '## {sec}' (use {SECOES})")
        tam = len(render(v))
        if tam > TETO_CHARS_VERBETE:
            problemas.append(f"{rot}: verbete renderizado com {tam} caracteres "
                             f"(teto {TETO_CHARS_VERBETE}) — encurtar")

    faltam = set(CAUSAS_RAIZ) - set(causas_dedicadas)
    if faltam:
        problemas.append(f"causas raiz sem verbete dedicado: {sorted(faltam)}")

    total = estimar_tokens(render_biblioteca(verbetes))
    if total > TETO_TOKENS_BIBLIOTECA:
        problemas.append(f"biblioteca inteira estimada em {total} tokens "
                         f"(teto {TETO_TOKENS_BIBLIOTECA})")

    # Sobreposição com o banco de casos: compara 5-gramas de palavras do texto de cada
    # caso (sintoma, observação, corpo) com o texto do verbete. Copiar um caso para a
    # documentação faria a medição virar busca de par.
    for caso in casos:
        e = caso["entrada"]
        texto_caso = " ".join(str(e.get(k, "")) for k in ("sintoma", "observacao", "corpo"))
        sh_caso = _shingles(tokens(texto_caso))
        if len(sh_caso) < 5:
            continue
        for v in verbetes:
            sh_v = _shingles(tokens(_texto_completo(v)))
            razao = len(sh_caso & sh_v) / len(sh_caso)
            if razao >= limiar_sobreposicao:
                problemas.append(f"{v['pasta']}/{v['caminho'].name}: {razao:.0%} dos 5-gramas "
                                 f"do caso {caso['id']} aparecem no verbete — reescrever")
    return problemas


def resumo(verbetes: list[dict]) -> str:
    inteira = render_biblioteca(verbetes)
    por_pasta = {}
    for v in verbetes:
        por_pasta[v["pasta"]] = por_pasta.get(v["pasta"], 0) + 1
    return (f"{len(verbetes)} verbetes {dict(sorted(por_pasta.items()))}; "
            f"biblioteca inteira: {len(inteira)} caracteres ≈ {estimar_tokens(inteira)} tokens")


if __name__ == "__main__":
    from banco_casos import CASOS
    from banco_casos_extra import CASOS_EXTRA

    vs = carregar()
    print(resumo(vs))
    probs = validar(vs, CASOS + CASOS_EXTRA)
    if probs:
        print(f"\n{len(probs)} problema(s):")
        for p in probs:
            print("  -", p)
    else:
        print("biblioteca válida")
