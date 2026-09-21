#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria avaliar_fase3b.py — a avaliação da Fase 3-B. Para os
# modos que rodam sobre os 90 casos oficiais (ponte, cruzada, texto_max, a5), delega inteiro
# para avaliar_fase3.avaliar_saida (sem alterá-la). Para o modo 'ineditos' (casos que nunca
# entraram em banco_casos.py/banco_casos_extra.py, logo fora de avaliar_fase3.TODOS_OS_CASOS),
# monta a agregação própria com as peças de avaliar_fase3 que não dependem do banco oficial de
# casos.
# ! Motivo: avaliar_saida usa TODOS_OS_CASOS (banco_casos.CASOS + banco_casos_extra.
# CASOS_EXTRA) em vários pontos que não fazem sentido para 'ineditos' — casos_da_particao,
# recuperacao_por_epoca e reconstrucao_ok leem/conferem contra os 90 oficiais, e
# conferir_arquivos espera 90 diagnósticos por versão. Chamar avaliar_saida sobre uma saída de
# 'ineditos' mediria os casos errados nesses blocos (quando não quebrasse). As funções que o
# brief pede para o modo 'ineditos' — avaliar_registro_fase3, agregar_fase3, pareado_vs_l0,
# cochran_por_modelo, calcular_flips e rec.avaliar_recuperacao — não têm essa dependência: cada
# uma lê só o que está gravado no PRÓPRIO registro (r['gabarito'], r['caso'], etc., que
# executar_fase3.diagnosticar grava a partir do caso, não de uma tabela global), então
# funcionam sobre qualquer lista de casos, incluindo os inéditos.
"""Avaliação da Fase 3-B: delega a avaliar_fase3.avaliar_saida para ponte/cruzada/texto_max/a5
e monta a agregação própria (avaliar_registro_fase3 + agregar_fase3 + pareado_vs_l0 +
cochran_por_modelo + calcular_flips + recuperacao.avaliar_recuperacao) para o modo ineditos."""
import argparse
import json
import sys
from pathlib import Path

import avaliar_fase3
import biblioteca as bib
import caminhos
import evolucao_biblioteca as evo
import executar_fase3b
import recuperacao as rec

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, copiado de
# avaliar_fase3.py:41-50/biblioteca.py:25-32.
# ! Motivo: no Windows o console pode estar em cp1252, que não representa os símbolos usados
# nas tabelas daqui (Δ, →) — sem isso o avaliador aborta com UnicodeEncodeError depois de já
# ter gravado os JSON, e quem roda vê um traceback no lugar da tabela.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def avaliar_modo_simples(c3b: dict, modelos: list[str] | None = None) -> tuple[list[dict], dict]:
    """! Alteração de IA - Revisar: ponte/cruzada/texto_max/a5 — delega inteiro para
    avaliar_fase3.avaliar_saida(c3b, modelos, gerar_revisao=False) e imprime o mesmo resumo de
    console que avaliar_fase3.py imprimiria (avisos 'N de 90' de conferir_arquivos incluídos;
    são esperados aqui, porque a Fase 3-B roda só 36 casos por versão de biblioteca nesses
    quatro modos, não os 90 da corrida oficial).
    ! Motivo: avaliar_saida já calcula tudo que estes quatro modos precisam (é o mesmo cálculo
    de acerto/campo/formato/citação da Fase 3 oficial, só que sobre os diagnósticos gravados
    na pasta da 3-B) — reimplementar aqui criaria dois números para o mesmo registro."""
    avaliados, resumo = avaliar_fase3.avaliar_saida(c3b, modelos, gerar_revisao=False)
    avaliar_fase3.imprimir_resumo(c3b, avaliados, resumo)
    return avaliados, resumo


def avaliar_modo_ineditos(c3b: dict) -> tuple[list[dict], dict]:
    """! Alteração de IA - Revisar: modo 'ineditos' — monta 'avaliados' com
    avaliar_fase3.avaliar_registro_fase3 por registro (o gabarito de cada caso inédito já vem
    gravado no próprio registro, por executar_fase3.diagnosticar), agrega com
    avaliar_fase3.agregar_fase3/pareado_vs_l0/cochran_por_modelo/calcular_flips e mede a
    recuperação de cada versão de biblioteca com recuperacao.avaliar_recuperacao(verbetes,
    CASOS_INEDITOS) — os mesmos hit@k/MRR que a Fase 3 oficial usa, aqui sobre os casos que
    nunca entraram na biblioteca de jeito nenhum.
    ! Motivo: ver o cabeçalho do módulo — avaliar_saida não serve para esta pasta porque ela
    não tem os 90 casos oficiais. indice_das_versoes (por hash de biblioteca) e
    avaliar_registro_fase3 não dependem do banco de casos e continuam corretas aqui."""
    casos_ineditos = executar_fase3b._casos_ineditos()
    slugs = avaliar_fase3.slugs_da_saida(c3b)
    if not slugs:
        raise SystemExit(f"nenhum diagnóstico em {c3b['raiz']} — rode executar_fase3b.py "
                         "--modo ineditos primeiro")

    try:
        causas_com_defeito = bib.causas_com_defeito_documentado(bib.carregar(bib.BASE))
    except FileNotFoundError:
        causas_com_defeito = set()
    por_versao = avaliar_fase3.indice_das_versoes(c3b, slugs)

    avaliados: list[dict] = []
    nome_por_slug: dict[str, str] = {}
    for slug in slugs:
        diagnosticos, _propostas = avaliar_fase3.carregar_modelo(c3b, slug)
        nome_por_slug[slug] = (diagnosticos[0]["modelo"] if diagnosticos
                               else slug.replace("_", ":"))
        avaliados += [avaliar_fase3.avaliar_registro_fase3(r, causas_com_defeito, por_versao)
                     for r in diagnosticos]

    resumo = {
        "por_modelo_biblioteca_particao": avaliar_fase3.agregar_fase3(
            avaliados, "modelo", "biblioteca_epoca", "particao"),
        "pareado_vs_L0": avaliar_fase3.pareado_vs_l0(avaliados),
        "cochran_q": avaliar_fase3.cochran_por_modelo(avaliados),
        # ! Alteração de IA - Revisar: aviso sobre os flips com versões não consecutivas (21/09/2026, revisão da P3.1).
        # ! Motivo: avaliar_fase3.calcular_flips monta só as transições ADJACENTES de VERSOES=(0,1,2,3); com o
        # padrão do modo inéditos (--versoes 0 1 3, sem a 2) só L0→L1 sai no bloco "flips" e L1→L3 fica de fora
        # sem nada acusar. Como avaliar_fase3.py não muda depois da bateria, o aviso fica no resumo e no console;
        # quem ler o resumo_fase3.json do modo inéditos usa pareado_vs_L0 para L3.
        "flips": avaliar_fase3.calcular_flips(avaliados, "particao"),
        "aviso_flips": "calcular_flips cobre só transições adjacentes (L0→L1, L1→L2, L2→L3); com versões não "
                       "consecutivas (ex.: 0, 1, 3) a transição L1→L3 não aparece — use pareado_vs_L0",
        "recuperacao": [],
    }
    print("!! aviso: o bloco 'flips' cobre só transições adjacentes; com --versoes 0 1 3 a transição L1→L3 fica "
          "fora (use pareado_vs_L0)")
    for slug in slugs:
        modelo = nome_por_slug[slug]
        for epoca, raiz in sorted(avaliar_fase3.snapshots_do_modelo(c3b, slug).items()):
            verbetes = bib.carregar(raiz)
            medida = rec.avaliar_recuperacao(verbetes, casos_ineditos)
            medida.pop("posicao_por_caso", None)
            resumo["recuperacao"].append({"modelo": modelo, "biblioteca_epoca": epoca,
                                          **medida})

    resumo["metadados"] = {
        "saida": c3b["raiz"].name, "modo": "ineditos",
        "modelos": [nome_por_slug[s] for s in slugs],
        "n_casos_ineditos": len(casos_ineditos), "n_diagnosticos": len(avaliados)}

    c3b["raiz"].mkdir(parents=True, exist_ok=True)
    c3b["avaliacao"].write_text(json.dumps(avaliados, ensure_ascii=False, indent=2),
                                encoding="utf-8")
    c3b["resumo"].write_text(json.dumps(resumo, ensure_ascii=False, indent=2),
                             encoding="utf-8")

    print(f"\n{len(avaliados)} diagnósticos de {len(casos_ineditos)} caso(s) inédito(s) "
         f"avaliados — {c3b['raiz']}")
    for linha in resumo["por_modelo_biblioteca_particao"]:
        print(f"  {linha['modelo']:26} L{linha['biblioteca_epoca']} {linha['n']:>4} casos "
             f"{linha['causa_correta_pct']:>6}% de acerto")
    return avaliados, resumo


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Avaliação da Fase 3-B: delega a avaliar_fase3 para ponte/cruzada/"
                    "texto_max/a5 e monta a agregação própria para o modo ineditos.")
    ap.add_argument("--saida", required=True,
                    help="subpasta de resultados gravada por executar_fase3b.py")
    ap.add_argument("--modelos", nargs="+", default=None,
                    help="nomes ou slugs dos modelos (padrão: todos os encontrados; ignorado "
                    "no modo ineditos)")
    args = ap.parse_args()

    print(caminhos.descricao())
    c3b = caminhos.fase3(args.saida)
    caminho_condicoes = c3b["raiz"] / "condicoes_3b.json"
    if not caminho_condicoes.exists():
        raise SystemExit(f"sem condicoes_3b.json em {c3b['raiz']} — rode executar_fase3b.py "
                         "primeiro (ele grava esse arquivo ao preparar a saída)")
    modo = json.loads(caminho_condicoes.read_text(encoding="utf-8")).get("modo")

    if modo == "ineditos":
        avaliados, resumo = avaliar_modo_ineditos(c3b)
    else:
        if not avaliar_fase3.slugs_da_saida(c3b):
            print(f"Nenhum diagnóstico da Fase 3-B em {c3b['raiz']}. Rode executar_fase3b.py "
                 "primeiro.")
            return
        avaliados, resumo = avaliar_modo_simples(c3b, args.modelos)

    print(f"\nAvaliação em {c3b['avaliacao']}\nResumo em {c3b['resumo']}")


if __name__ == "__main__":
    main()
