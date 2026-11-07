#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (07/11/2026) que integra ao Memorial a rodada 6 da pesquisa, a da Pós-Fase 4: treze
# leituras em Markdown feitas por subagentes no mesmo dia (cinco bases da parte 1 e oito repositórios da parte 3) e a leitura
# do syllabus CTFL 4.0 (parte 2), guardadas em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`. Grava
# `levantamento-2026-11-07-pos-fase-4.md` (§6.15.1 a §6.15.14, uma subseção por leitura, na ordem fixa das três partes do
# pedido; §6.15.15 o mapa adotado, ideia, adiado, descartado), o bloco de referências novas em `referencias.md` (antes do
# bloco da Pré-Fase 4, sem repetir as que já constam, com o total recontado) e a linha no índice do Memorial; `--check`
# regera os três e compara.
# ! Motivo: pedido do Eric em 07/11/2026 (Pós-Fase 4 em três partes; decisões 101 a 104): o plano precisa apontar a fonte de
# cada ponto, e a regra do Memorial é que a pesquisa entre por script, nunca colada à mão. Diferente das rodadas 1 a 5, esta
# não passou por Workflow com verificação cética: cada leitura marca, fonte a fonte, o que abriu e leu, e o cabeçalho declara
# isso. O bloco de referências entra antes do bloco da Pré-Fase 4 porque integrar_pesquisa_pre_fase4.py trata o bloco dele
# como o último do arquivo e regrava tudo o que vem depois do título dele; a frase do total é escrita pelos dois scripts com
# a mesma constante (DATAS_DOS_LEVANTAMENTOS).
"""Uso:
    python ferramentas/integrar_pesquisa_pos_fase4.py [--simular]
    python ferramentas/integrar_pesquisa_pos_fase4.py --check
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import integrar_pesquisa_pre_fase4 as ip
import render_levantamento as rl

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = rl.RAIZ
DOC_DIR = RAIZ / "Documentacao" / "memorial"
DADOS = DOC_DIR / "5-metodo-e-ferramental" / "dados" / "pesquisa-pos-fase-4"
LEVANTAMENTO = DOC_DIR / "2-pesquisa-e-literatura" / "levantamento-2026-11-07-pos-fase-4.md"
MEMORIAL = ip.MEMORIAL
DATA = "07/11/2026"
SECAO = "6.15"
ROTULO = f"levantamento de {DATA}"
TITULO_REFS = f"### Levantamento da Pós-Fase 4 ({ROTULO})"
MARCA_DO_INDICE = f"- [Levantamento: Pós-Fase 4 ({DATA})]"
TAG_DO_INDICE = "<!-- ! Alteração de IA - Revisar: linha do índice para o levantamento da Pós-Fase 4"

# Chave, arquivo da leitura, parte do pedido do Eric, título da subseção e quem leu, na ordem fixa das subseções §6.15.1 a
# §6.15.14: as cinco bases da parte 1, o syllabus (parte 2) e os oito repositórios na ordem em que o Eric os listou.
TOPICOS = [
    ("pos4-revisao-estilo-pr", "base-A-revisao-estilo-pr.md", "1", "O hub central à imagem de uma pull request: o modelo de revisão do GitHub e do Azure DevOps", "subagente"),
    ("pos4-indicador-de-progresso", "base-B-indicador-de-progresso.md", "1", "A barra de progresso para a espera da inferência local", "subagente"),
    ("pos4-arvore-de-decisao", "base-C-arvore-de-decisao.md", "1", "A árvore de decisão legível para o analista", "subagente"),
    ("pos4-metricas-de-prolixidade", "base-D-metricas-de-prolixidade.md", "1", "Métricas de prolixidade e objetividade para os filtros determinísticos", "subagente"),
    ("pos4-impacto-git-e-vm", "base-E-impacto-git-e-vm.md", "1", "Seleção de testes pelo diff do Git e a máquina virtual sugerida pelo orientador", "subagente"),
    ("pos4-syllabus-ctfl", "istqb-ctfl-4.0-validacao.md", "2", "O projeto contra o syllabus CTFL 4.0 do ISTQB, na tradução do BSTQB", "Claude, na sessão principal"),
    ("pos4-repo-dimensional-drawing", "repo-01-dimensional-drawing.md", "3", "Repositório enesozturk/dimensional-drawing", "subagente"),
    ("pos4-repo-rag-anything", "repo-02-rag-anything.md", "3", "Repositório HKUDS/RAG-Anything", "subagente"),
    ("pos4-repo-mcptoon", "repo-03-mcptoon.md", "3", "Repositório activeing123/mcptoon", "subagente"),
    ("pos4-repo-understand-anything", "repo-04-understand-anything.md", "3", "Repositório Egonex-AI/Understand-Anything", "subagente"),
    ("pos4-repo-agenttrail", "repo-05-agenttrail.md", "3", "Repositório sodiumsun/agenttrail", "subagente"),
    ("pos4-repo-eagle-4", "repo-06-eagle-4.md", "3", "Repositório eagle-hq/EAGLE-4", "subagente"),
    ("pos4-repo-gepa", "repo-07-gepa.md", "3", "Repositório gepa-ai/gepa", "subagente"),
    ("pos4-repo-claude-obsidian", "repo-08-claude-obsidian.md", "3", "Repositório AgriciDaniel/claude-obsidian", "subagente"),
]
N_MAPA = len(TOPICOS) + 1
PARTES = {"1": "o visual e a usabilidade do agente", "2": "o projeto contra o syllabus CTFL 4.0", "3": "os oito repositórios do GitHub"}
INTERESSE_DO_ERIC = {"pos4-repo-dimensional-drawing": "alto", "pos4-repo-rag-anything": "médio", "pos4-repo-mcptoon": "alto", "pos4-repo-understand-anything": "muito alto",
                     "pos4-repo-agenttrail": "alto", "pos4-repo-eagle-4": "médio", "pos4-repo-gepa": "muito alto", "pos4-repo-claude-obsidian": "médio"}
# O mapa (§6.15.15): chave, o que vale para o Claude Code, o que vale para o agente, o que fica no projeto e o veredito.
# São dados, não código: o texto sai como está na tabela do levantamento e na aba do painel.
MAPA = [
    ("pos4-revisao-estilo-pr", "o próprio fluxo de revisão de PR do GitHub e do Azure DevOps que o Eric já usa", "base do hub central (pacote Q6): três desfechos da revisão, comentário ancorado com rascunho, threads com estado, iterações numeradas, veredito de cinco valores e a regra de que a IA só comenta", "o desenho do hub, com as fontes", "adotado"),
    ("pos4-indicador-de-progresso", "n/a", "base da barra de progresso (pacote Q4): os limites de 0,1, 1 e 10 s, o indicador de porcentagem, as pausas perto do fim que parecem mais lentas, a barra determinada quando a duração é estimável e os campos de contagem do Ollama", "a estimativa em duas fases, com as fontes", "adotado"),
    ("pos4-arvore-de-decisao", "n/a", "base da árvore de decisão (pacote Q3): explicação contrastiva com o por que não, o raciocínio escrito rotulado como texto sem garantia, as diretrizes G2 e G11 e os formatos de trilha das ferramentas de observabilidade", "um nó por decisão, com a escolhida contra as descartadas e o rótulo de origem de cada afirmação", "adotado"),
    ("pos4-metricas-de-prolixidade", "as mesmas métricas valem para o texto que o Claude escreve nos documentos", "base dos filtros determinísticos (pacote Q2): o Flesch adaptado ao português, palavras por frase, preenchimento por lista fechada, repetição interna, taxa de compressão, jargão sem expansão, densidade e o tamanho só como covariável", "oito métricas em Python puro, com o limiar e a fonte de cada uma", "adotado"),
    ("pos4-impacto-git-e-vm", "n/a", "base da integração com o Git (pacote Q7): seleção segura por arquivo, mapa escrito à mão como o do Azure DevOps, arquivo fora do mapa roda tudo, rodada completa periódica e conferência contra ela; a VM fica registrada como viável só num servidor (decisão 102)", "o mapa por frontmatter dos verbetes e as três regras; a resposta ao orientador sobre a VM", "adotado"),
    ("pos4-syllabus-ctfl", "n/a", "base do relatório por caso no molde do relatório de defeitos (seção 5.5; decisão 104), da terminologia erro, defeito, falha e causa-raiz no TCC e do enquadramento do agente como teste funcional, caixa-preta e automatizado, nos níveis de sistema e de integração de sistema", "a referência na bibliografia do TCC e os campos do relatório v3", "adotado"),
    ("pos4-repo-dimensional-drawing", "não adotar; no máximo uma figura pontual de um componente, por pedido", "não serve: são instruções de desenho de interface, sem relação com o diagnóstico", "nada", "descartado"),
    ("pos4-repo-rag-anything", "não adotar", "não: exige embedding (descartado por medição, decisão 61), três modelos e serviços na nuvem por padrão", "nada", "descartado"),
    ("pos4-repo-mcptoon", "só se o número de servidores MCP crescer (`mcptoon bench` mede o custo fixo por turno)", "não: recodificar o contexto do agente reabriria o prompt congelado", "trabalho futuro, se os servidores MCP crescerem", "adiado"),
    ("pos4-repo-understand-anything", "opcional e de baixo valor: testar uma vez nas cobaias, sem adotar (ficha 53: não testado, decisão 106)", "não: depende de um modelo na nuvem e de Node; a ideia do impacto das mudanças por diff vale, feita em Python local, sem modelo", "a ideia da seleção por diff do pacote Q7", "ideia"),
    ("pos4-repo-agenttrail", "opcional: só passivo, com Node 20 portátil, sem `init` (ficha 53: não testado, decisão 106)", "não como base nem como formato: não registra alternativas nem o pai de cada passo, que a trilha v2 já tem", "os rótulos de evidência (reportado, observado, inferido, desconhecido) e o registro datado de decisões, no pacote Q3", "ideia"),
    ("pos4-repo-eagle-4", "não serve", "não: exige GPU, SGLang ou vLLM e um segundo modelo residente; nenhuma medida em CPU ou com modelo de 7B", "citação de trabalho relacionado no TCC", "descartado"),
    ("pos4-repo-gepa", "opcional e adiável: só para um subagente com métrica automática", "não é filtro de respostas: é um otimizador offline de prompt por evolução com reflexão em texto; no máximo um experimento no prompt de cura, no lugar do DSPy adiado, nunca no prompt congelado", "candidato futuro para o prompt de cura", "adiado"),
    ("pos4-repo-claude-obsidian", "não instalar: a escrita só roda em WSL, Linux ou macOS", "não serve: é um segundo cérebro em Markdown para o Claude Code, sem relação com o diagnóstico", "o lint de notas órfãs, por script", "ideia"),
]

# Uma referência começa por autor ou entidade em caixa alta (sobrenome ou sigla, seguido de vírgula ou ponto) e vai até o
# "Acesso em: d mês. ano." Pode vir em negrito, numerada ("**1. ") ou depois de dois-pontos dentro de um item de lista
# ("Fonte complementar (página aberta): LIM, B. Y.; ..."). Linha que só cita um endereço, sem autor, não é referência.
_REFERENCIA = re.compile(r"(?:^|(?<=: ))\*{0,2}\s*(?:\d+\.\s+)?(?P<ref>[A-ZÀ-Ü][A-ZÀ-Ü0-9\-' ]{1,60}[,.].*?Acesso em: \d{1,2} [a-z]{3}\. \d{4}\.)")


def rebaixar(texto: str) -> str:
    """O texto de uma leitura sem o título de nível 1 (a subseção do levantamento ganha o seu) e com os demais títulos
    rebaixados: `##` vira `#####`; `###` e `####` viram `######`, o último nível do Markdown."""
    linhas = []
    for l in texto.splitlines():
        if l.startswith("# "):
            continue
        m = re.match(r"^(#{2,6}) (.*)$", l)
        if m:
            l = "#" * min(len(m.group(1)) + 3, 6) + " " + m.group(2)
        linhas.append(l)
    return "\n".join(linhas).strip("\n")


def extrair_referencias(texto: str) -> list[str]:
    """As referências de uma leitura, uma por linha em que aparecem, sem negrito, sem numeração e sem a marca de confiança
    que o leitor escreveu depois do ponto final."""
    refs = []
    for l in texto.splitlines():
        s = l.strip()
        if s.startswith(("- ", "* ")):
            s = s[2:]
        if "Acesso em:" not in s:
            continue
        m = _REFERENCIA.search(s)
        if not m:
            continue
        refs.append(re.sub(r"\s+", " ", m.group("ref").replace("**", "")).strip())
    return refs


def carregar(pasta: Path = DADOS, topicos: list[tuple] | None = None) -> dict:
    """{chave: leitura} na ordem fixa; leitura ausente interrompe, porque a numeração das subseções é fixa."""
    dados = {}
    for chave, arquivo, parte, titulo, leitor in topicos or TOPICOS:
        p = pasta / arquivo
        if not p.exists():
            raise SystemExit(f"leitura ausente: {p}")
        texto = p.read_text(encoding="utf-8").replace("\r\n", "\n")
        # a tag de IA no topo da leitura (exigida por conferir_docs.py) é metadado do arquivo e não entra no levantamento
        texto = re.sub(r"\A\s*(?:<!--.*?-->\s*)+", "", texto, flags=re.DOTALL)
        fontes = extrair_referencias(texto)
        dados[chave] = {"titulo": titulo, "parte": parte, "leitor": leitor, "arquivo": arquivo, "texto": rebaixar(texto), "fontes": fontes, "n_fontes": len(fontes)}
    return dados


# ------------------------------------------------------------------ render

def _fontes(n: int) -> str:
    return f"{n} fonte com endereço" if n == 1 else f"{n} fontes com endereço"


def secao(numero: int, chave: str, item: dict) -> str:
    interesse = f" Interesse declarado pelo Eric: {INTERESSE_DO_ERIC[chave]}." if chave in INTERESSE_DO_ERIC else ""
    return "\n".join([f"#### {SECAO}.{numero} {item['titulo']} (`{chave}`; {_fontes(item['n_fontes'])})", "",
                      f"*Leitura de:* {item['leitor']}, em {DATA}; arquivo `{item['arquivo']}` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`.{interesse}", "",
                      item["texto"], ""])


def bloco_mapa(numero: int = N_MAPA) -> str:
    titulos = {t[0]: t[3] for t in TOPICOS}
    partes = [f"#### {SECAO}.{numero} Mapa adotado, ideia, adiado, descartado", "",
              ("Um veredito por leitura, escrito pelo Claude a partir das leituras e dos critérios do projeto (máquina sem GPU e sem administrador, prompt congelado, "
               "biblioteca medida, nenhuma segunda chamada ao modelo). *Adotado* = serve de base a um pacote do plano da Pós-Fase 4; *ideia* = a ferramenta não entra, "
               "mas uma ideia dela entra, em código próprio; *adiado* = só com outra máquina ou depois da Fase 5; *descartado* = não serve, com o motivo. Os vereditos "
               "foram escritos pelo Claude; o Eric aprovou o plano que os incorpora (ficha 54, decisão 105) e decidiu não testar os dois repositórios marcados como opcionais "
               "para o Claude Code (ficha 53, decisão 106)."), "",
              "| Leitura | Para o Claude Code | Para o agente | O que fica | Veredito |", "|---|---|---|---|---|"]
    partes += [f"| {titulos[chave]} (`{chave}`) | {claude} | {agente} | {fica} | **{veredito}** |" for chave, claude, agente, fica, veredito in MAPA]
    return "\n".join(partes) + "\n"


def cabecalho(dados: dict, topicos: list[tuple]) -> str:
    n, n_mapa = len(topicos), len(topicos) + 1
    por_parte = Counter(t[2] for t in topicos)
    total = sum(d["n_fontes"] for d in dados.values())
    linhas = [
        ("<!-- ! Alteração de IA - Revisar: arquivo gerado por ferramentas/integrar_pesquisa_pos_fase4.py a partir das leituras guardadas em "
         "5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/ (rodada 6 da pesquisa, 07/11/2026). NÃO editar as subseções à mão (o --check compara com o regerado)."),
        (f"     ! Motivo: a Pós-Fase 4 foi especificada pelo Eric em 07/11/2026 em três partes, e o plano dela precisa apontar a fonte de cada ponto; a pesquisa "
         f"entra por script, nunca colada à mão, e o que não serve fica registrado com o motivo (§{SECAO}.{n_mapa}). -->"),
        "", f"# Levantamento bibliográfico: Pós-Fase 4 ({DATA})", "",
        ("Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Continua o [levantamento da Pré-Fase 4](levantamento-2026-10-01-pre-fase-4.md) "
         "(§6.14). O que motivou: o Eric especificou a Pós-Fase 4 em três partes: (1) o visual e a usabilidade do agente, com um hub central à imagem de uma pull request, "
         "a integração com o Git, a barra de progresso, a árvore de decisão e a normalização das respostas por filtros determinísticos; (2) o projeto contra o syllabus "
         "CTFL 4.0 do ISTQB, na tradução do BSTQB; (3) oito repositórios do GitHub, com a viabilidade para o Claude Code e para o agente ([roadmap](../roadmap.md), §4.8; "
         "plano aprovado em `claude-memoria/plano-aprovado-pos-fase-4.md`). Referências completas em [referencias.md](referencias.md)."),
        "", f"### {SECAO} Levantamento da Pós-Fase 4", "",
        (f"{n} leituras em {DATA}: {por_parte.get('1', 0)} bases da parte 1 ({PARTES['1']}), {por_parte.get('2', 0)} da parte 2 ({PARTES['2']}) e "
         f"{por_parte.get('3', 0)} da parte 3 ({PARTES['3']}), com {total} fontes com endereço no total. Diferente das rodadas 1 a 5, esta rodada não passou por um "
         "Workflow com pesquisador, verificadores céticos e síntese: cada leitura foi feita por um subagente (as bases e os repositórios) ou pelo Claude na sessão "
         "principal (o syllabus), que abriu as páginas, os README e os PDF que conseguiu e marcou, fonte a fonte, o que leu por inteiro, o que só viu em resumo de "
         "busca e o que veio de memória. Um número citado vale com a marca da fonte de onde veio; nenhuma afirmação foi conferida por um segundo agente. Os textos "
         "entram como os leitores os escreveram, com os títulos rebaixados para caber na numeração; o mapa final é do Claude."),
        "", "| Subseção | Parte | Leitura | Fontes com endereço |", "|---|---|---|---|",
    ]
    linhas += [f"| §{SECAO}.{i} | {parte} | `{chave}` | {dados[chave]['n_fontes']} |" for i, (chave, _, parte, _, _) in enumerate(topicos, 1)]
    avisos = [
        ("**Sem verificação cética.** As rodadas 1 a 5 passaram cada afirmação por um verificador; esta não. O que cada leitura afirma vale com a marca de confiança "
         "que o leitor pôs na fonte (aberta e lida; só o resumo de busca; de memória), e as leituras dizem o que não conseguiram abrir."),
        ("**Fontes sem revisão por pares.** Os repositórios, a documentação do GitHub, do Azure DevOps, da Apple, do Material e do Ollama e os blogs citados não têm "
         "revisão por pares; os artigos citados trazem o veículo e o ano. Os números de desempenho dos repositórios são medições dos próprios autores, lidas nos README."),
        ("**Grafia.** O texto das leituras entra como foi escrito, sem travessão nem seta, como manda a regra de documentação; títulos e citações literais das fontes "
         "ficam como na fonte."),
        ("**O que já foi decidido.** As decisões 101 a 106 (fichas 49 a 54) foram tomadas pelo Eric no quadro da sessão de 07/11/2026 lendo estas leituras; o mapa do "
         f"§{SECAO}.{n_mapa} foi escrito pelo Claude, e o plano que o incorpora foi aprovado como está (ficha 54, decisão 105), sem sessão de teste para os repositórios "
         "marcados como opcionais (ficha 53, decisão 106)."),
    ]
    linhas += ["", f"{ip._POR_EXTENSO[len(avisos)]} avisos sobre o texto abaixo:", ""] + [f"{i}. {a}" for i, a in enumerate(avisos, 1)] + [""]
    return "\n".join(linhas) + "\n"


def render(dados: dict, topicos: list[tuple] | None = None) -> str:
    topicos = topicos or TOPICOS
    secoes = [secao(i, chave, dados[chave]) for i, (chave, *_) in enumerate(topicos, 1)]
    return cabecalho(dados, topicos) + "\n" + "\n".join(secoes) + "\n" + bloco_mapa(len(topicos) + 1)


# ------------------------------------------------------------------ referências e índice (texto entra, texto sai)

def _sem_o_bloco(atual: str) -> str:
    """O arquivo sem o bloco desta rodada: o que vem antes do título dele e o que vem do título seguinte de nível 3 em diante."""
    if TITULO_REFS not in atual:
        return atual
    ini = atual.index(TITULO_REFS)
    m = re.search(r"^### ", atual[ini + len(TITULO_REFS):], re.MULTILINE)
    antes = atual[:ini].rstrip("\n")
    return antes + "\n\n" + atual[ini + len(TITULO_REFS) + m.start():] if m else antes + "\n"


def _selecionar(resto: str, dados: dict) -> tuple[list[str], list[str]]:
    """Das fontes das leituras, na ordem dos tópicos: as que entram no bloco e as omitidas por já constarem no arquivo (mesma
    chave das outras rodadas, ou o mesmo endereço) ou por repetirem outra leitura desta rodada."""
    linhas = [l[2:] for l in resto.splitlines() if l.startswith("- ")]
    chaves, urls = {ip._chave(l) for l in linhas}, {ip._url(l) for l in linhas} - {""}
    novas, omitidas = [], []
    for chave in dados:
        for ref in dados[chave]["fontes"]:
            ch, u = ip._chave(ref), ip._url(ref)
            if ch in chaves or (u and u in urls):
                omitidas.append(ref)
                continue
            chaves.add(ch)
            if u:
                urls.add(u)
            novas.append(ref)
    return novas, omitidas


def omitidas(atual: str, dados: dict) -> list[str]:
    return _selecionar(_sem_o_bloco(atual), dados)[1]


def referencias_com_bloco(atual: str, dados: dict) -> tuple[str, int, int]:
    """O texto de referencias.md com o bloco desta rodada regravado logo antes do bloco da Pré-Fase 4 (ou no fim, se ele não
    existir), sem repetir referência que já conste, e com o total da frase de abertura recontado. Devolve também quantas
    referências novas a rodada trouxe e o total do arquivo."""
    resto = _sem_o_bloco(atual)
    novas, _ = _selecionar(resto, dados)
    bloco = "\n".join([TITULO_REFS, "",
                       ("<!-- ! Alteração de IA - Revisar: bloco gerado por ferramentas/integrar_pesquisa_pos_fase4.py a partir das leituras da rodada 6 (Pós-Fase 4); "
                        "referências já presentes no arquivo foram omitidas (mesma chave das outras rodadas, sobrenome, ano e início do título, ou o mesmo endereço). "
                        "O bloco fica antes do bloco da Pré-Fase 4, que o integrador dela trata como o último do arquivo."),
                       "     ! Motivo: cada leitura traz as suas fontes na norma; sem a conferência as mesmas fontes entrariam duas vezes e o total do arquivo ficaria errado. -->",
                       ""] + [f"- {r}" for r in sorted(novas, key=ip._ordem)]) + "\n"
    if ip.TITULO_REFS in resto:
        i = resto.index(ip.TITULO_REFS)
        novo = resto[:i].rstrip("\n") + "\n\n" + bloco + "\n" + resto[i:]
    else:
        novo = resto.rstrip("\n") + "\n\n" + bloco
    total = sum(1 for l in novo[novo.index("## 9. Referências levantadas"):].splitlines() if l.startswith("- "))
    m = re.search(r"os levantamentos de [^*\n]*? produziram as \*\*(\d+)\*\* referências abaixo", novo)
    assert m, "frase do total de referências não encontrada"
    novo = novo[:m.start()] + f"os levantamentos de {ip.DATAS_DOS_LEVANTAMENTOS} produziram as **{total}** referências abaixo" + novo[m.end():]
    return novo, len(novas), total


def memorial_com_linha(s: str, dados: dict) -> str:
    """O texto do Memorial com a linha do índice deste levantamento gravada (ou regravada) logo depois da linha da Pré-Fase 4."""
    n = len(dados)
    linha = (TAG_DO_INDICE + f" (§{SECAO}), gravada por integrar_pesquisa_pos_fase4.py. ! Motivo: sem a linha o índice não leva ao levantamento nem ao mapa; ela é regravada a cada integração. -->\n"
             + MARCA_DO_INDICE + f"(memorial/2-pesquisa-e-literatura/levantamento-2026-11-07-pos-fase-4.md): §{SECAO}, {n} tópicos lidos em {DATA} (o hub à imagem de uma pull request, "
             "o indicador de progresso, a árvore de decisão, as métricas de prolixidade, o impacto pelo Git e a VM, o projeto contra o syllabus CTFL 4.0 e os oito repositórios do GitHub); "
             f"§{SECAO}.{n + 1} mapa adotado, ideia, adiado, descartado.\n")
    if MARCA_DO_INDICE in s:
        ini = s.rfind(TAG_DO_INDICE, 0, s.index(MARCA_DO_INDICE))
        assert ini >= 0, "linha do índice sem a tag que a acompanha"
        fim = s.index("\n", s.index(MARCA_DO_INDICE)) + 1
        return s[:ini] + linha + s[fim:]
    assert ip.MARCA_DO_INDICE in s, "linha do levantamento da Pré-Fase 4 no índice do Memorial não encontrada"
    fim = s.index("\n", s.index(ip.MARCA_DO_INDICE)) + 1
    return s[:fim] + linha + s[fim:]


def integrar_referencias(dados: dict, simular: bool) -> None:
    atual, crlf = ip._ler(rl.REFERENCIAS)
    novo, novas, total = referencias_com_bloco(atual, dados)
    print(f"referências: {novas} novas desta rodada; total do arquivo {total}" + (" (simulado)" if simular else ("" if novo != atual else " (já estava em dia)")))
    for ref in omitidas(atual, dados):
        print("  omitida (já consta no arquivo ou em outra leitura):", ref[:110])
    if not simular and novo != atual:
        ip._gravar(rl.REFERENCIAS, novo, crlf)


def integrar_memorial(dados: dict, simular: bool) -> None:
    atual, crlf = ip._ler(MEMORIAL)
    novo = memorial_com_linha(atual, dados)
    if not simular and novo != atual:
        ip._gravar(MEMORIAL, novo, crlf)
    print("Memorial: linha do índice " + ("simulada" if simular else ("gravada" if novo != atual else "já estava em dia")))


def check() -> int:
    if not LEVANTAMENTO.exists():
        print("--check: nada integrado ainda")
        return 1
    dados = carregar()
    falhas = 0
    e, a = rl._normalizar(render(dados)), rl._normalizar(LEVANTAMENTO.read_text(encoding="utf-8"))
    if e == a:
        print(f"--check: levantamento da Pós-Fase 4 idêntico ao regerado ({len(dados)} leituras)")
    else:
        falhas += 1
        print("--check: o levantamento DIFERE do regerado")
        print("\n".join(list(difflib.unified_diff(a, e, lineterm=""))[:30]))
    refs = ip._ler(rl.REFERENCIAS)[0]
    if referencias_com_bloco(refs, dados)[0] == refs:
        print("--check: bloco de referências e total em dia")
    else:
        falhas += 1
        print("--check: o bloco de referências (ou o total) DIFERE do regerado")
    indice = ip._ler(MEMORIAL)[0]
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
    dados = carregar()
    for chave, item in dados.items():
        print(f"  {chave}: {_fontes(item['n_fontes'])}")
    texto = render(dados)
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
