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
# ! Alteração de IA - Revisar: acrescenta o tipo "aprendido" — verbete NOVO, escrito pelo
# modelo durante a Fase 3, que mora na pasta aprendidos/.
# ! Motivo: sem esse tipo, todo verbete criado pelo modelo cairia na checagem
# "tipo='aprendido' fora de [...]" de validar() e a cópia dele da biblioteca ficaria
# inválida. Ele é separado de "erro" de propósito: por_causa() só olha tipo 'erro', então
# um verbete aprendido nunca pode virar o verbete de ouro de uma causa raiz.
TIPOS = {"funcionamento", "regra", "contrato", "erro", "defeito_conhecido", "limite",
         "aprendido"}
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
# ! Alteração de IA - Revisar: SECOES ganha "Notas do modelo" e, com ela, os tetos e o
# formato de linha das notas que o modelo escreve na Fase 3.
# ! Motivo: até a Fase 2-B qualquer seção fora das quatro originais era acusada por
# validar() como "seção desconhecida". Na Fase 3 o modelo edita a SUA cópia da biblioteca só
# por acréscimo, e todo acréscimo em verbete existente vai para essa seção — sem ela, a
# cópia editada ficaria inválida. Os tetos existem porque essas notas entram no prompt: 800
# caracteres renderizados por verbete ≈ 308 tokens (2,6 chars/token, o pior caso medido na
# Fase 2-A), então os 3 verbetes recuperados somam no máximo ~1.700 tokens de notas dentro
# do num_ctx de 8192; 6 notas por verbete evita que um verbete vire um diário.
SECOES = ("Resumo", "Sinais", "Causa", "Como confirmar", "Notas do modelo")
TETO_CHARS_NOTAS_VERBETE = 800
TETO_NOTAS_POR_VERBETE = 6
# Uma nota por linha, no formato que aplicar_edicao grava:
#   - [E1 · sin-4 · nota] <TEXTO> — Motivo: <MOTIVO>
#   - [E2 · tra-9 · retificação de "<TRECHO>"] <TEXTO> — Motivo: <MOTIVO>
# A época (E<n>) e o id do caso ficam na linha para a revisão saber de onde veio cada nota;
# nenhum dos dois vai ao prompt (ver render_notas).
NOTA_RE = re.compile(r'^- \[E(\d+) · ([a-z]+-\d+) · (nota|retificação(?: de "(.+?)")?)\] '
                     r'(.+?) — Motivo: (.+)$')

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


# ! Alteração de IA - Revisar: lê a seção "## Notas do modelo" de um verbete e devolve uma
# nota por linha, já separada em época, caso, operação, trecho retificado, texto e motivo.
# ! Motivo: as notas são gravadas como texto no próprio .md (o modelo edita a cópia dele da
# biblioteca), então quem precisa delas — render_notas, validar e o índice do BM25 — teria
# de reparsear a linha em cada lugar, cada um com uma regra diferente. Linha que não casa
# com NOTA_RE é ignorada AQUI de propósito: quem acusa a linha malformada é validar(), para
# que uma nota mal escrita não derrube a bateria no meio da corrida.
def notas(v: dict) -> list[dict]:
    saida = []
    for linha in v["secoes"].get("Notas do modelo", "").splitlines():
        m = NOTA_RE.match(linha.strip())
        if not m:
            continue
        saida.append({"epoca": int(m.group(1)), "caso": m.group(2),
                      "operacao": "nota" if m.group(3) == "nota" else "retificacao",
                      "trecho": m.group(4), "texto": m.group(5), "motivo": m.group(6)})
    return saida


def notas_malformadas(v: dict) -> list[int]:
    """! Alteração de IA - Revisar: número de cada linha da seção "## Notas do modelo" que
    não casa com NOTA_RE — contando só as linhas não vazias, a partir de 1.
    ! Motivo: validar() acusava a linha malformada com um laço próprio, igual ao de notas()
    mas com a contagem de linhas; dois laços sobre a mesma seção com a mesma regra
    divergiriam na primeira mudança de NOTA_RE. A contagem fica aqui para a mensagem
    "nota malformada na linha N" de validar() continuar apontando a mesma linha que a
    revisão vê ao abrir o .md (linhas em branco não contam, como antes)."""
    saida = []
    n_linha = 0
    for linha in v["secoes"].get("Notas do modelo", "").splitlines():
        if not linha.strip():
            continue
        n_linha += 1
        if not NOTA_RE.match(linha.strip()):
            saida.append(n_linha)
    return saida


# ----------------------------------------------------------------- renderização

def _sinais(v: dict) -> str:
    itens = [re.sub(r"^[-*]\s*", "", ln).strip()
             for ln in v["secoes"].get("Sinais", "").splitlines() if ln.strip()]
    return "; ".join(itens)


# ! Alteração de IA - Revisar: o que era render() virou render_base() (corpo idêntico, byte
# a byte na saída) e render() passou a ser render_base() + render_notas().
# ! Motivo: na Fase 3 o verbete cresce com as notas do modelo, mas a parte original tem de
# continuar medível sozinha — é o render_base que responde pelo teto de 550 caracteres em
# validar() e é ele que precisa sair igual ao da Fase 2-B para o braço A1 ("biblioteca
# inteira") e o cache de prefixo continuarem comparáveis entre as fases.
def render_base(v: dict) -> str:
    """Forma compacta que vai ao prompt — a MESMA em todos os braços, para que a única
    diferença entre 'biblioteca inteira' e 'recuperada' seja a seleção, não a
    profundidade. Uma linha de título com o id (é o que o modelo cita em FONTE) e um
    parágrafo com resumo, sinais, causa e como confirmar. É a parte ORIGINAL do verbete,
    escrita à mão antes da Fase 3: nunca cresce, aconteça o que acontecer nas épocas."""
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


def _frase(texto: str) -> str:
    """! Alteração de IA - Revisar: fecha a frase da nota com ponto, se ela já não terminar
    em pontuação.
    ! Motivo: as notas entram no prompt uma atrás da outra ("Notas: texto1 texto2"); sem o
    ponto entre elas, duas notas escritas sem pontuação final pelo modelo viravam uma frase
    só e o verbete lido pelo modelo seguinte misturava as duas observações."""
    return texto if texto.endswith((".", "!", "?")) else texto + "."


def render_notas(v: dict) -> str:
    """! Alteração de IA - Revisar: trecho que as notas do modelo acrescentam ao verbete no
    prompt: só o TEXTO de cada nota e, nas retificações, o trecho corrigido. Época, id do
    caso e motivo ficam de fora — são metadados de revisão que só gastariam tokens do
    num_ctx e, no caso do motivo, ainda citariam o caso que originou a nota.
    ! Motivo: é a única parte do verbete que cresce na Fase 3 (render_base nunca muda), e é
    medida sozinha por validar() contra o teto de 800 caracteres — se o motivo entrasse
    aqui, o verbete estouraria o teto com metade das notas e, pior, o prompt de diagnóstico
    passaria a citar o caso de origem ("o caso mostrou o botão com undefined"), o que
    transformaria a medição em busca de par."""
    partes = []
    for n in notas(v):
        if n["operacao"] == "retificacao":
            # Sem o trecho (a parte ` de "..."` é opcional em NOTA_RE) a retificação vira
            # uma correção sem alvo: fica só o rótulo, nunca a palavra None no prompt.
            onde = f'onde diz "{n["trecho"]}", leia: ' if n["trecho"] else ""
            partes.append(_frase(f"Retificação: {onde}{n['texto']}"))
        else:
            partes.append(_frase(n["texto"]))
    return " Notas: " + " ".join(partes) if partes else ""


def render(v: dict) -> str:
    """Verbete inteiro que vai ao prompt: a parte original mais as notas do modelo. Para
    a biblioteca original (base_conhecimento/), que não tem notas, é igual a
    render_base(v)."""
    return render_base(v) + render_notas(v)


CABECALHO = ("DOCUMENTAÇÃO DO SISTEMA (fonte da verdade — consulte antes de concluir; "
             "cada verbete tem um identificador entre colchetes)")

# ! Alteração de IA - Revisar: "aprendidos" entra no FIM da ordem das pastas.
# ! Motivo: é a pasta dos verbetes que o modelo escreve na Fase 3; no fim porque a ordem
# aqui é a ordem em que os verbetes aparecem no prompt do braço "biblioteca inteira", e a
# documentação escrita à mão continua vindo primeiro. Pasta fora desta lista ia para o
# índice 99 (junto com qualquer outra), o que misturaria aprendidos com pastas inesperadas.
_ORDEM_PASTAS = ("negocio", "contratos", "falhas_injetadas", "defeitos_conhecidos", "erros",
                 "aprendidos")


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


# ! Alteração de IA - Revisar: validar() ganha o parâmetro teto_global (None desliga a
# checagem do tamanho da biblioteca inteira) e passa a checar as notas do modelo e os
# verbetes de tipo 'aprendido'.
# ! Motivo: na Fase 3 cada modelo valida a SUA cópia da biblioteca, que cresce a cada época;
# o braço "biblioteca inteira" (A1) não roda lá, então acusar "biblioteca inteira estimada
# em N tokens (teto 6700)" pararia a corrida por um orçamento que ninguém gasta — o que
# importa é o teto por verbete, que é o que entra no prompt dos 3 recuperados. A Fase 2-B
# continua chamando sem o parâmetro e mantém o teto de 6.700.
def validar(verbetes: list[dict], casos: list[dict], limiar_sobreposicao: float = 0.3,
            teto_global: int | None = TETO_TOKENS_BIBLIOTECA) -> list[str]:
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
        # ! Alteração de IA - Revisar: o teto de 550 caracteres passa a medir render_base(v),
        # e as notas do modelo ganham tetos próprios (800 caracteres renderizados e 6 notas),
        # mais a checagem de formato de cada linha da seção "## Notas do modelo".
        # ! Motivo: medir render(v) misturaria a parte original com o que o modelo
        # acrescentou — na segunda época qualquer verbete anotado estouraria os 550 e a
        # biblioteca do modelo ficaria inválida por ter aprendido. Separando, a parte escrita
        # à mão continua presa aos 550 (é o que a Fase 2-B mediu) e o que cresce tem o seu
        # próprio limite. A linha malformada é acusada aqui, e não em notas(), para a
        # revisão ver o número da linha e o arquivo.
        tam = len(render_base(v))
        if tam > TETO_CHARS_VERBETE:
            problemas.append(f"{rot}: verbete renderizado com {tam} caracteres "
                             f"(teto {TETO_CHARS_VERBETE}) — encurtar")
        # ! Alteração de IA - Revisar: a varredura das linhas malformadas passou para
        # notas_malformadas(v); aqui só sobra montar a mensagem.
        # ! Motivo: o laço era uma cópia do de notas() com contagem de linha — ver o
        # docstring de notas_malformadas.
        for n_linha in notas_malformadas(v):
            problemas.append(f"{rot}: nota malformada na linha {n_linha} da seção "
                             "'Notas do modelo'")
        tam_notas = len(render_notas(v))
        if tam_notas > TETO_CHARS_NOTAS_VERBETE:
            problemas.append(f"{rot}: notas renderizadas com {tam_notas} caracteres "
                             f"(teto {TETO_CHARS_NOTAS_VERBETE})")
        n_notas = len(notas(v))
        if n_notas > TETO_NOTAS_POR_VERBETE:
            problemas.append(f"{rot}: {n_notas} notas do modelo "
                             f"(teto {TETO_NOTAS_POR_VERBETE})")
        # ! Alteração de IA - Revisar: verbete de tipo 'aprendido' (escrito pelo modelo na
        # Fase 3) tem de estar em aprendidos/ e apontar as causas raiz de que fala.
        # ! Motivo: sem a pasta, um verbete aprendido ficaria misturado com a documentação
        # escrita à mão e não daria para separar, na análise, o que veio de cada origem; sem
        # causas_relacionadas, ele não entra em causas_com_defeito_documentado() nem no
        # índice, virando texto solto que só ocupa espaço no prompt.
        if m.get("tipo") == "aprendido":
            if v["pasta"] != "aprendidos":
                problemas.append(f"{rot}: verbete 'aprendido' fora da pasta aprendidos/")
            if not m.get("causas_relacionadas"):
                problemas.append(f"{rot}: verbete 'aprendido' sem causas_relacionadas")

    faltam = set(CAUSAS_RAIZ) - set(causas_dedicadas)
    if faltam:
        problemas.append(f"causas raiz sem verbete dedicado: {sorted(faltam)}")

    if teto_global is not None:
        total = estimar_tokens(render_biblioteca(verbetes))
        if total > teto_global:
            problemas.append(f"biblioteca inteira estimada em {total} tokens "
                             f"(teto {teto_global})")

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
