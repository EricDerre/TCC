#!/usr/bin/env python3
# ! Alteração de IA - Revisar: módulo novo (08/11/2026, Pós-Fase 4, pacote Q5): a sessão de revisão com revisor humano dos relatórios v3 e das árvores de decisão da
# corrida 24 (`fase4_ineditos`), conduzida pela página da sessão (`ferramentas/sessao_revisao.py --perfil v3`: um relatório por vez, com cronômetro, respostas no banco
# da página e passadas à planilha por `--gravar`) ou, sem a página, por cartões na sessão do Claude. `--gerar` sorteia a ordem dos 36 casos com semente fixa, grava a planilha `revisao_v3.md`
# (as mesmas colunas da planilha da sessão de 05/11/2026, `revisao_trilha.md`) e uma cópia por relatório em `sessao_revisao_v3/relatorio-N.md`, com o relatório v3 e a
# árvore do caso sem o nome do caso, a classe, o nível e o comando de reexecução; pelo caminho dos cartões, `--inicio N` marca a hora em que o cartão N foi apresentado e
# `--responder N` grava na planilha a decisão, a avaliação, o erro localizado, a utilidade e o comentário, com o tempo contado do cartão à resposta; `--proximo` diz o próximo
# relatório em branco. A leitura sai por `avaliar_fase4.py --revisao_v3`, contra o acerto de cada caso em `ineditos.json`, e só com a planilha inteira.
# ! Motivo: a ficha 40 ficou aberta desde 05/11/2026 porque a sessão da corrida 22 teve uma resposta do Eric e dez pareceres do Claude aprovados (decisões 85 a 87 e 95);
# em 08/11/2026 o Eric escolheu fazer a sessão com os relatórios no formato novo (v3 mais árvore) de casos que não leu com o agente, a corrida 24 inteira, numa página
# com cronômetro ("uma interfacezinha"), no lugar dos cartões. O nome, a classe e o nível saem porque reduzem as 23 causas possíveis a poucas (o mesmo motivo que tirou
# o nome na página de 05/11); nos cartões, sem cronômetro próprio, o tempo é medido pelo relógio deste módulo.
# ! Alteração de IA - Revisar: (10/11/2026) o parágrafo "Como foi preenchida" que `texto_da_planilha` escreve deixou de dizer que o revisor leu na página: diz que a
# resposta dada fora da página por um analista e digitada ou colada pelo Eric entra com o tempo "não medido" (a palavra "digitada" entrou com a decisão 117: uma
# das 36 respostas do analista foi digitada na página pelo Eric, e não colada).
# ! Motivo: a sessão de 09 e 10/11/2026 foi registrada como feita pelo Eric; no dia 10 ele declarou que passou os relatórios a um analista e colou o que ele respondeu
# (decisão 114), e o tempo que a página mediu nesses relatórios era o da troca entre os dois.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python revisao_v3.py --gerar [--check]
  RESULTADOS_DIR=resultados_alvo python revisao_v3.py --proximo
  RESULTADOS_DIR=resultados_alvo python revisao_v3.py --inicio 1
  RESULTADOS_DIR=resultados_alvo python revisao_v3.py --responder 1 --decisao aceitar --avaliacao certo --erro n.a. --utilidade 4 [--comentario "..."]
"""
from __future__ import annotations

import argparse
import contextlib
import json
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import caminhos

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    with contextlib.suppress(OSError, ValueError, AttributeError):
        sys.stdout.reconfigure(encoding="utf-8")

SEMENTE = 20261108                 # a data da sessão, como nas outras sementes do projeto
CORRIDA = "fase4_ineditos"         # a corrida 24: os 36 inéditos da ficha 27, que o Eric nunca leu com o agente
FONTE = "ineditos.json"            # a leitura vigente da corrida 24 (avaliar_fase4.py --ineditos): caso, classe, gabarito, rótulo, acerto, selo
NOME_PLANILHA = "revisao_v3.md"
PASTA_SESSAO = "sessao_revisao_v3"
NOME_RESPOSTAS = "respostas.json"
NOME_TEMPOS = "tempos.json"
CELULA_EM_BRANCO = "(em branco)"   # a mesma marca de biblioteca_fase4.CELULA_EM_BRANCO, que avaliar_fase4.ler_planilha_de_revisao procura
CLASSE_OMITIDA = "classe e nível omitidos nesta sessão (dizem a família do defeito)"
VALORES = {"decisao": ("aceitar", "recusar"), "avaliacao": ("certo", "errado"), "erro_localizado": ("sim", "não", "n.a.")}
RE_LINHA = re.compile(r"^\| \d+ \|")
# Os nomes dos casos do banco e dos inéditos; qualquer um que sobre na cópia diria a família do defeito.
RE_NOME_DE_CASO = re.compile(r"(?<![\w-])(?:efe|lex|run|semt|sin|tra)-\d+(?![\w-])")
# Os campos com a resposta certa e as frases que diriam o resultado do caso: se a cópia os trouxer, a sessão deixa de ser às cegas.
RE_RESULTADO = re.compile(r"causa_correta|campo_correto|verbete_de_ouro|causa[ _]esperada|r[oó]tulo[ _]esperado|\bacertou\b|\berrou\b", re.IGNORECASE)
# A taxa de acerto da faixa de confiança na corrida de calibração fica na árvore por decisão (ficha 58, decisão 110): não é o resultado deste caso.
RE_TAXA_DA_FAIXA = re.compile(r"acertou a causa em \d+ de \d+")
RE_CLASSE_E_NIVEL = re.compile(r"classe \d+ \([^)]*\)(?:; n[íi]vel \d+ \([^)]*\))?")
RE_NIVEL = re.compile(r"n[íi]vel \d+ \([^)]*\)")
RE_COMANDO = re.compile(r"^.*Comando (?:para reexecutar o caso|de reexecução).*\n?", re.MULTILINE)


def casos_da_fonte(pasta_fase4: Path) -> tuple[dict, list[dict]]:
    dado = json.loads((pasta_fase4 / FONTE).read_text(encoding="utf-8"))
    return dado, dado["casos"]


def amostra(casos: list[dict], semente: int = SEMENTE) -> list[dict]:
    """Todos os casos, embaralhados com a semente fixa (o Eric escolheu a corrida inteira em 08/11/2026), com a posição de 1 a N
    e o caminho da cópia da sessão; a ordem não diz o acerto."""
    rng = random.Random(semente)
    ordem = sorted(casos, key=lambda c: c["caso"])
    rng.shuffle(ordem)
    return [{"posicao": i, "caso": c["caso"], "classe": c.get("classe"), "acerto": bool(c["acerto"]), "relatorio": f"{PASTA_SESSAO}/relatorio-{i}.md"}
            for i, c in enumerate(ordem, 1)]


def _esconder(texto: str, caso: str, apelido: str) -> str:
    texto = RE_COMANDO.sub("", texto)
    texto = re.sub(rf"(?<![\w-]){re.escape(caso)}(?![\w-])", apelido, texto)
    texto = RE_CLASSE_E_NIVEL.sub(CLASSE_OMITIDA, texto)
    return RE_NIVEL.sub(CLASSE_OMITIDA, texto)


def _conferir_as_cegas(texto: str, caso: str, nome: str) -> None:
    achado = RE_RESULTADO.search(RE_TAXA_DA_FAIXA.sub("", texto))
    if achado:
        raise ValueError(f"o {nome} de {caso} traz o resultado do caso ({achado.group(0)}); a sessão deixaria de ser às cegas")
    outro = RE_NOME_DE_CASO.search(texto)
    if outro:
        raise ValueError(f"o {nome} de {caso} cita o nome de outro caso ({outro.group(0)}); a sessão deixaria de ser às cegas")


def copia_da_sessao(v3: str, arvore: str, caso: str, posicao: int, total: int) -> str:
    """O texto que o revisor lê no cartão: o relatório v3 e, depois dele, a árvore de decisão, com o nome do caso trocado por relatorio-N,
    a classe e o nível omitidos e o comando de reexecução (que traz o nome) retirado; recusa texto que diga o resultado ou cite outro caso."""
    apelido = f"relatorio-{posicao}"
    partes = []
    for nome, texto in (("relatório v3", v3), ("árvore", arvore)):
        escondido = _esconder(texto, caso, apelido)
        _conferir_as_cegas(escondido, caso, nome)
        partes.append(escondido.rstrip("\n"))
    cab = [("<!-- ! Alteração de IA - Revisar: cópia DERIVADA para a sessão de revisão com revisor humano (Pós-Fase 4, pacote Q5), gerada por revisao_v3.py --gerar a partir do "
           "relatório v3 e da árvore de decisão do caso, com o nome do caso trocado por relatorio-N e a classe, o nível e o comando de reexecução omitidos; não editar à mão "
           "(--check regera e compara)."),
           ("     ! Motivo: a sessão é às cegas (ficha 40, opção b): o nome do caso e a classe dizem a família do defeito e reduziriam as 23 causas possíveis a poucas, como a "
           "página da sessão de 05/11/2026 já escondia o nome. -->"),
           f"# Relatório {posicao} de {total} (sessão de revisão)", "",
           ("Leia o relatório de defeito e, depois dele, a árvore de decisão do caso, e responda na ficha: decisão (aceitar ou recusar o diagnóstico), avaliação (o diagnóstico "
            "está certo ou errado), erro localizado (sim, não ou n.a.) e utilidade do relatório (1 a 5). O nome do caso foi trocado e a classe e o nível foram omitidos; "
            "nada aqui diz o resultado do caso."), "", "---", ""]
    return "\n".join(cab) + partes[0] + "\n\n---\n\n" + partes[1] + "\n"


def texto_da_planilha(amostra_: list[dict], corrida: str) -> str:
    cab = [("<!-- ! Alteração de IA - Revisar: planilha DERIVADA da sessão de revisão com revisor humano dos relatórios v3 e das árvores de decisão (Pós-Fase 4, pacote Q5), "
           "gerada por revisao_v3.py --gerar a partir de ineditos.json; só as células do revisor são preenchidas (por revisao_v3.py --responder, a cada cartão), e o script "
           "não a regrava depois de começada."),
           ("     ! Motivo: a especificação da trilha (seção 12 c) mede, com um revisor humano, o acerto da localização do erro, o tempo até a decisão e a adesão apropriada "
           "(aceitar o diagnóstico certo e recusar o errado), com a utilidade percebida como medida secundária; a ficha 40 foi fechada em 08/11/2026 pela opção (b), e esta "
           "planilha é o registro conferível da sessão, no mesmo formato da de 05/11 (revisao_trilha.md). -->"),
           f"# Sessão de revisão dos relatórios v3 e das árvores de decisão (corrida {corrida}, Pós-Fase 4)", "",
           ("Como foi preenchida, um relatório por vez, na ordem da tabela: cada linha traz a resposta dada à cópia da sessão indicada em \"Relatório\" (o relatório v3 e a árvore "
            "de decisão do caso, com o nome do caso trocado por relatorio-N e a classe e o nível omitidos): a decisão (aceitar ou recusar), a avaliação (certo ou errado), se quem "
            "leu achou no relatório onde está o erro (sim, não ou n.a. quando não vê erro) e a utilidade de 1 (nenhuma) a 5 (decidiu sozinho). A resposta entrou pela página da "
            "sessão (ferramentas/sessao_revisao.py --perfil v3, um relatório por vez). Quando quem leu respondeu na própria página, o tempo até a decisão é o que ela mediu, do "
            "relatório aberto à decisão, descontadas as pausas, em segundos; quando a resposta foi dada fora da página por um analista e digitada ou colada pelo Eric, o tempo fica "
            "\"não "
            "medido\", porque o que a página mediu foi a troca entre os dois (sessao_revisao_v3/respostas.json guarda o registro da página, e respostas_planilha.json o que veio "
            "para esta planilha). Esta planilha, ineditos.json, a trilha e os arquivos da corrida dizem o resultado de cada caso, e a adesão apropriada só vale para quem "
            "respondeu sem abri-los."), "",
           ("| # | Caso | Classe | Relatório | Tempo até a decisão (s) | Erro localizado (sim, não, n.a.) | Decisão (aceitar, recusar) | Utilidade (1 a 5) | "
           "Avaliação (certo, errado) | Comentário |"),
           "|---|---|---|---|---|---|---|---|---|---|"]
    linhas = [f"| {x['posicao']} | `{x['caso']}` | {x['classe']} | `{x['relatorio']}` | {CELULA_EM_BRANCO} | {CELULA_EM_BRANCO} | {CELULA_EM_BRANCO} | "
              f"{CELULA_EM_BRANCO} | {CELULA_EM_BRANCO} |  |" for x in amostra_]
    return "\n".join(cab + linhas) + "\n"


def _celulas(linha: str) -> list[str]:
    return [x.strip() for x in linha.strip().strip("|").split("|")]


def ler_planilha(pasta_fase4: Path) -> list[dict]:
    """As linhas de relatório da planilha, na ordem dela: posição, caso, classe e caminho da cópia, as células cruas e se ainda está em branco."""
    linhas = []
    for linha in (pasta_fase4 / NOME_PLANILHA).read_text(encoding="utf-8").splitlines():
        if RE_LINHA.match(linha):
            c = _celulas(linha)
            linhas.append({"posicao": int(c[0]), "caso": c[1].strip("`"), "classe": c[2], "relatorio": c[3].strip("`"), "celulas": c,
                           "em_branco": CELULA_EM_BRANCO in c[4:9]})
    return linhas


def _comecada(pasta_fase4: Path) -> bool:
    return (pasta_fase4 / NOME_PLANILHA).exists() and any(not x["em_branco"] for x in ler_planilha(pasta_fase4))


def _estrutura(texto: str) -> list[list[str]]:
    return [_celulas(linha)[:4] for linha in texto.splitlines() if RE_LINHA.match(linha)]


def gerar(pasta_fase4: Path, raiz_corrida: Path, check: bool = False) -> dict:
    """Grava a planilha (só enquanto nenhuma linha foi respondida) e as cópias da sessão; com check, regera e compara sem gravar
    (a planilha só pelas quatro primeiras colunas, porque as outras são do revisor)."""
    dado, casos = casos_da_fonte(pasta_fase4)
    am = amostra(casos)
    corrida = (dado.get("metadados") or {}).get("corrida") or CORRIDA
    copias = {}
    for x in am:
        v3 = (raiz_corrida / "relatorios_v3" / f"{x['caso']}.md").read_text(encoding="utf-8")
        arv = (raiz_corrida / "arvores" / f"{x['caso']}.md").read_text(encoding="utf-8")
        copias[x["relatorio"]] = copia_da_sessao(v3, arv, x["caso"], x["posicao"], len(am))
    texto = texto_da_planilha(am, corrida)
    planilha = pasta_fase4 / NOME_PLANILHA
    if check:
        diferentes = []
        if not planilha.exists() or _estrutura(planilha.read_text(encoding="utf-8")) != _estrutura(texto):
            diferentes.append(NOME_PLANILHA)
        diferentes += [rel for rel, t in copias.items() if not (pasta_fase4 / rel).exists() or (pasta_fase4 / rel).read_text(encoding="utf-8") != t]
        return {"diferentes": diferentes, "amostra": am, "copias": len(copias), "planilha": "conferida"}
    (pasta_fase4 / PASTA_SESSAO).mkdir(parents=True, exist_ok=True)
    for rel, t in copias.items():
        (pasta_fase4 / rel).write_text(t, encoding="utf-8", newline="\n")
    if _comecada(pasta_fase4):
        estado = "mantida"
    else:
        planilha.write_text(texto, encoding="utf-8", newline="\n")
        estado = "gravada"
    return {"planilha": estado, "copias": len(copias), "amostra": am, "diferentes": []}


def proximo_em_branco(pasta_fase4: Path) -> dict | None:
    linhas = ler_planilha(pasta_fase4)
    em_branco = [x for x in linhas if x["em_branco"]]
    if not em_branco:
        return None
    x = em_branco[0]
    return {"posicao": x["posicao"], "relatorio": x["relatorio"], "faltam": len(em_branco), "total": len(linhas)}


def _tempos(pasta_fase4: Path) -> dict:
    arq = pasta_fase4 / PASTA_SESSAO / NOME_TEMPOS
    return json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else {}


def marcar_inicio(pasta_fase4: Path, posicao: int, agora: float | None = None) -> dict:
    """Guarda a hora em que o cartão do relatório foi apresentado ao revisor; marcar de novo recomeça a contagem."""
    if posicao not in {x["posicao"] for x in ler_planilha(pasta_fase4)}:
        raise ValueError(f"relatório {posicao} fora da planilha")
    agora = time.time() if agora is None else agora
    tempos = _tempos(pasta_fase4)
    tempos[str(posicao)] = {"inicio_s": agora, "inicio": datetime.fromtimestamp(agora).isoformat(timespec="seconds")}
    (pasta_fase4 / PASTA_SESSAO).mkdir(parents=True, exist_ok=True)
    (pasta_fase4 / PASTA_SESSAO / NOME_TEMPOS).write_text(json.dumps(tempos, ensure_ascii=False, indent=2), encoding="utf-8")
    return tempos[str(posicao)]


def _comentario(texto) -> str:
    return " ".join(str(texto or "").replace("|", "/").split())


def responder(pasta_fase4: Path, posicao: int, decisao: str, avaliacao: str, erro: str, utilidade: int, comentario: str = "",
              agora: float | None = None, corrigir: bool = False) -> dict:
    """Grava a resposta do cartão na linha do relatório: o tempo até a decisão (do início marcado a agora), o erro localizado, a decisão,
    a utilidade, a avaliação e o comentário; recusa valor fora do que a planilha aceita, linha já preenchida (sem `corrigir`) e cartão
    sem início marcado. Cada resposta também vai para sessao_revisao_v3/respostas.json, com a hora do cartão e a da resposta."""
    erros = [f"{campo} = {valor!r}" for campo, valor in (("decisao", decisao), ("avaliacao", avaliacao), ("erro_localizado", erro)) if valor not in VALORES[campo]]
    if type(utilidade) is not int or not 1 <= utilidade <= 5:
        erros.append(f"utilidade = {utilidade!r}")
    if erros:
        raise ValueError(f"resposta inválida no relatório {posicao}: {', '.join(erros)}")
    inicio = _tempos(pasta_fase4).get(str(posicao))
    if not inicio:
        raise ValueError(f"cartão do relatório {posicao} sem início marcado (revisao_v3.py --inicio {posicao})")
    agora = time.time() if agora is None else agora
    segundos = max(0, round(agora - inicio["inicio_s"]))
    caminho = pasta_fase4 / NOME_PLANILHA
    saida, gravada = [], None
    for linha in caminho.read_text(encoding="utf-8").split("\n"):
        if not RE_LINHA.match(linha) or int(_celulas(linha)[0]) != posicao:
            saida.append(linha)
            continue
        c = _celulas(linha)
        if CELULA_EM_BRANCO not in c[4:9] and not corrigir:
            raise ValueError(f"a linha do relatório {posicao} já está preenchida: {c[4:10]}; use corrigir para trocar")
        novas = [str(segundos), erro, decisao, str(utilidade), avaliacao, _comentario(comentario)]
        saida.append("| " + " | ".join(c[:4] + novas) + " |")
        gravada = {"posicao": posicao, "caso": f"relatorio-{posicao}", "segundos": segundos, "erro_localizado": erro, "decisao": decisao,
                   "utilidade": utilidade, "avaliacao": avaliacao, "comentario": _comentario(comentario), "inicio": inicio["inicio"],
                   "fim": datetime.fromtimestamp(agora).isoformat(timespec="seconds"), "corrigida": corrigir}
    if gravada is None:
        raise ValueError(f"relatório {posicao} fora da planilha")
    caminho.write_text("\n".join(saida), encoding="utf-8", newline="\n")
    arq = pasta_fase4 / PASTA_SESSAO / NOME_RESPOSTAS
    respostas = json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else []
    respostas.append(gravada)
    arq.write_text(json.dumps(respostas, ensure_ascii=False, indent=2), encoding="utf-8")
    return gravada


def _frase_do_proximo(pasta_fase4: Path) -> str:
    p = proximo_em_branco(pasta_fase4)
    if p is None:
        return "planilha inteira: a leitura pode sair (avaliar_fase4.py --revisao_v3)"
    return f"faltam {p['faltam']} de {p['total']}; próximo: relatório {p['posicao']} ({p['relatorio']})"


# ------------------------------------------------------------------ linha de comando

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gerar", action="store_true", help=f"sorteia a ordem, grava a planilha {NOME_PLANILHA} e as cópias da sessão em {PASTA_SESSAO}/")
    ap.add_argument("--check", action="store_true", help="com --gerar: regera e compara, sem gravar")
    ap.add_argument("--proximo", action="store_true", help="diz o próximo relatório em branco")
    ap.add_argument("--inicio", type=int, metavar="N", help="marca a hora em que o cartão do relatório N foi apresentado")
    ap.add_argument("--responder", type=int, metavar="N", help="grava a resposta do cartão do relatório N (com --decisao, --avaliacao, --erro, --utilidade e --comentario)")
    ap.add_argument("--decisao", choices=VALORES["decisao"])
    ap.add_argument("--avaliacao", choices=VALORES["avaliacao"])
    ap.add_argument("--erro", choices=VALORES["erro_localizado"] + ("nao",), help="erro localizado: sim, não (ou nao) ou n.a.")
    ap.add_argument("--utilidade", type=int)
    ap.add_argument("--comentario", default="")
    ap.add_argument("--corrigir", action="store_true", help="com --responder: troca uma linha já preenchida")
    ap.add_argument("--corrida", default=CORRIDA, help="a pasta da corrida em RESULTADOS_DIR com relatorios_v3/ e arvores/")
    ap.add_argument("--pasta", default=None, help="a pasta dos derivados (padrão: RESULTADOS_DIR/fase4)")
    args = ap.parse_args(argv)
    pasta = Path(args.pasta) if args.pasta else caminhos.RESULTADOS / "fase4"
    if argv is None:
        print(caminhos.descricao())
    if args.gerar:
        r = gerar(pasta, caminhos.fase3(args.corrida)["raiz"], check=args.check)
        if args.check:
            if r["diferentes"]:
                print(f"--check: DIFERE ({len(r['diferentes'])} arquivo(s): {r['diferentes'][:5]})")
                return 1
            print(f"--check: {r['copias']} cópias da sessão e a planilha {NOME_PLANILHA} batem com {FONTE} e com a corrida {args.corrida}")
            return 0
        print(f"planilha {NOME_PLANILHA} {r['planilha']}; {r['copias']} cópias da sessão em {pasta / PASTA_SESSAO}")
        return 0
    if args.inicio is not None:
        t = marcar_inicio(pasta, args.inicio)
        print(f"relatório {args.inicio}: cartão apresentado em {t['inicio']}")
        return 0
    if args.responder is not None:
        if None in (args.decisao, args.avaliacao, args.erro, args.utilidade):
            ap.error("--responder pede --decisao, --avaliacao, --erro e --utilidade")
        erro = "não" if args.erro == "nao" else args.erro
        r = responder(pasta, args.responder, args.decisao, args.avaliacao, erro, args.utilidade, args.comentario, corrigir=args.corrigir)
        extra = f"; comentário: {r['comentario']}" if r["comentario"] else ""
        print(f"relatório {r['posicao']}: {r['segundos']} s, erro localizado {r['erro_localizado']}, {r['decisao']}, utilidade {r['utilidade']}, {r['avaliacao']}{extra}")
        print(_frase_do_proximo(pasta))
        return 0
    if args.proximo:
        print(_frase_do_proximo(pasta))
        return 0
    ap.error("informe --gerar, --proximo, --inicio N ou --responder N")
    return 2


if __name__ == "__main__":
    sys.exit(main())
