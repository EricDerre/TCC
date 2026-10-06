#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (01/10/2026, Pré-Fase 4) da sonda de confiança: roda o modelo decidido
# com a biblioteca que ele mesmo escreveu nos 36 casos oficiais de avaliação e nos 36 inéditos, com o mesmo prompt,
# o mesmo executor (executar_fase3.rodar_epoca em passada final, via executar_fase3b) e os mesmos parâmetros da
# Fase 3, pedindo ao Ollama a probabilidade de cada token. O registro de diagnóstico sai com as mesmas 37 chaves do
# formato oficial; as probabilidades vão para um arquivo lateral, logprobs__L<n>.jsonl, na pasta do modelo.
# ! Motivo: o levantamento de 22/09 (§6.12.8) e o de 11/09 (§6.9.9) apontaram a probabilidade do rótulo como sinal
# barato de incerteza e deixaram duas lacunas: se o /api/generate a devolve (conferido em 01/10 por
# sondar_logprobs.py) e se ela separa acerto de erro numa taxonomia de 23 causas (é o que esta corrida mede). Nenhum
# arquivo congelado é alterado: as duas trocas são feitas em tempo de execução e desfeitas no finally, como a Fase
# 3-B fez com CONDICAO e TEXTO_MAX. A primeira (sondar_logprobs.com_logprobs) acrescenta os dois campos à chamada
# que cliente_ollama.gerar já faz; a segunda embrulha executar_fase3.diagnosticar para gravar a linha lateral ANTES
# de o executor gravar o registro, de modo que nunca exista registro sem a probabilidade correspondente.
"""Uso (em Programacao/AgenteCore/experimentos, com o Ollama no ar e nenhum modelo residente):
  RESULTADOS_DIR=resultados_alvo python sonda_confianca.py [--saida pre_fase4_confianca] [--modelo qwen2.5:7b]
                                                           [--versoes 1] [--top 20] [--casos N]
"""
from __future__ import annotations

import argparse
import contextlib
import json
import sys
from pathlib import Path

import caminhos
import executar_fase3
import executar_fase3b as e3b
import sondar_logprobs as sl

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

MODO = "confianca"
SAIDA_PADRAO = "pre_fase4_confianca"
CASAS = 5   # casas decimais guardadas de cada log-probabilidade


def compactar(logprobs: list[dict]) -> list[dict]:
    """Forma enxuta do `logprobs` do Ollama para o arquivo lateral: do token gerado ficam texto, log-probabilidade e
    bytes (o texto exato da resposta se remonta por eles); de cada alternativa ficam só texto e log-probabilidade.
    Corta o arquivo a cerca de metade sem perder o que a análise usa."""
    return [{"t": p.get("token", ""), "l": round(p["logprob"], CASAS), "b": p.get("bytes"),
             "a": [[a.get("token", ""), round(a["logprob"], CASAS)] for a in p.get("top_logprobs") or []]}
            for p in logprobs]


def expandir(compacto: list[dict]) -> list[dict]:
    """Volta da forma enxuta para a forma do Ollama (as alternativas ficam sem os bytes)."""
    return [{"token": p["t"], "logprob": p["l"], "bytes": p.get("b"),
             "top_logprobs": [{"token": t, "logprob": l} for t, l in p.get("a") or []]} for p in compacto]


def casos_da_sonda(particao_oficial: dict) -> list[dict]:
    """Os 36 casos oficiais de avaliação, na ordem do banco, seguidos dos 36 inéditos: os 72 casos que nenhuma
    biblioteca viu."""
    return e3b._casos_avaliacao(particao_oficial) + list(e3b._casos_ineditos())


def particao_da_sonda(casos: list[dict]) -> dict:
    """Partição da pasta da sonda: todo caso em 'avaliacao' (ninguém aprende nada aqui), sem data nem valor que mude
    de uma execução para a outra, para o relance conferir a partição em vez de recusá-la."""
    p = e3b._particao_tudo_avaliacao(casos)
    p["regra"] = ("Pré-Fase 4 (sonda de confiança): os 36 casos oficiais de avaliação da Fase 3 e os 36 inéditos da "
                  "Fase 3-B; todos em 'avaliacao', porque a corrida só diagnostica.")
    return p


def linha_lateral(registro: dict, captura: dict, top: int) -> dict:
    """A linha de logprobs__L<n>.jsonl de um diagnóstico. Confere antes que os tokens, juntos, são a resposta que foi
    para o registro: se não forem, a probabilidade guardada seria de outro texto."""
    r = captura["resposta"]
    lp = r.get("logprobs") or []
    if sl.texto_dos_tokens(lp).strip() != registro["resposta"]:
        raise RuntimeError(f"caso {registro['caso']}: os tokens devolvidos não remontam a resposta gravada")
    return {"caso": registro["caso"], "modelo": registro["modelo"], "biblioteca_epoca": registro["biblioteca_epoca"],
            "biblioteca_versao": registro["biblioteca_versao"], "versao_ollama": registro["versao_ollama"],
            "prompt_sha256": captura["prompt_sha256"], "top_logprobs": top, "done_reason": r.get("done_reason"),
            "prompt_eval_count": r.get("prompt_eval_count"), "prompt_eval_cached_count": r.get("prompt_eval_cached_count"),
            "eval_count": r.get("eval_count"), "logprobs": compactar(lp)}


@contextlib.contextmanager
def diagnostico_com_lateral(pasta: Path, capturas: list, top: int):
    """Durante o bloco, cada chamada de executar_fase3.diagnosticar grava, logo depois da inferência e antes de o
    executor gravar o registro, a linha lateral com as probabilidades da tentativa que deu certo (tentativa que
    falha por rede não chega a ser capturada). A função original é restaurada na saída."""
    original = executar_fase3.diagnosticar

    def trocado(modelo, caso, verbetes, ctx, prompt, max_tokens, comum):
        del capturas[:]
        registro = original(modelo, caso, verbetes, ctx, prompt, max_tokens, comum)
        if not capturas:
            raise RuntimeError(f"caso {caso['id']}: diagnóstico sem captura das probabilidades")
        linha = linha_lateral(registro, capturas[-1], top)
        arq = pasta / f"logprobs__L{registro['biblioteca_epoca']}.jsonl"
        arq.parent.mkdir(parents=True, exist_ok=True)
        with arq.open("a", encoding="utf-8") as f:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")
            f.flush()
        return registro

    executar_fase3.diagnosticar = trocado
    try:
        yield
    finally:
        executar_fase3.diagnosticar = original


def _completar_condicoes(c3b: dict, top: int, casos: list[dict], n_oficiais: int) -> None:
    """Acrescenta ao condicoes_3b.json o que é próprio desta corrida (quantas alternativas por posição foram pedidas
    e de que conjuntos vêm os casos); `_gravar_condicoes` regrava o arquivo a cada chamada, então isto roda depois."""
    caminho = c3b["raiz"] / "condicoes_3b.json"
    dado = json.loads(caminho.read_text(encoding="utf-8"))
    dado["top_logprobs"] = top
    dado["conjuntos"] = {"oficiais_de_avaliacao": n_oficiais, "ineditos": len(casos) - n_oficiais}
    caminho.write_text(json.dumps(dado, ensure_ascii=False, indent=2), encoding="utf-8")


def rodar(args: argparse.Namespace) -> list[str]:
    """Roda a sonda para args.modelo nas args.versoes da biblioteca dele. Devolve a lista de modelos que pararam
    antes do fim (vazia = tudo certo), como os modos de executar_fase3b."""
    c3_of = e3b._oficial()
    particao_oficial = e3b._particao_oficial(c3_of)
    casos = casos_da_sonda(particao_oficial)
    n_oficiais = len(e3b._casos_avaliacao(particao_oficial))
    particao = particao_da_sonda(casos)
    if args.casos:
        casos = casos[:args.casos]
    c3b = e3b.preparar_saida(args.saida, particao)
    e3b._gravar_condicoes(c3b, modo=MODO, doador=None, versoes=list(args.versoes), texto_max=None,
                          condicao=executar_fase3.CONDICAO, modelos=[args.modelo],
                          versao_ollama=executar_fase3._versao_ollama())
    _completar_condicoes(c3b, args.top, casos_da_sonda(particao_oficial), n_oficiais)

    modelo = args.modelo
    slug = executar_fase3._slug(modelo)
    pasta, pasta_bib = c3b["raiz"] / slug, c3b["bibliotecas"] / slug
    capturas: list = []
    try:
        digest, versao_ollama = e3b._preparar_modelo(modelo)

        def _rodar() -> None:
            for versao in args.versoes:
                origem = c3_of["bibliotecas"] / slug / f"epoca-{versao}"
                if not origem.exists():
                    raise SystemExit(f"sem epoca-{versao} oficial de {modelo} em {origem}")
                e3b._preparar_copia(origem, pasta_bib / f"epoca-{versao}")
                with sl.com_logprobs(args.top, capturas, exigir=True), diagnostico_com_lateral(pasta, capturas, args.top):
                    e3b._diagnosticar_versao(modelo, versao, casos, particao, pasta, pasta_bib, args.k,
                                             args.max_tokens_diagnostico, args.max_tokens_proposta, digest, versao_ollama)

        e3b._com_modelo_descarregado(modelo, _rodar)
    except SystemExit as e:
        print(f"\n!! {modelo} parou: {e}")
        return [modelo]
    return []


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--saida", default=SAIDA_PADRAO, help="subpasta nova dos resultados (padrão: pre_fase4_confianca)")
    ap.add_argument("--modelo", default="qwen2.5:7b")
    ap.add_argument("--versoes", type=int, nargs="+", default=[1], help="versões da biblioteca do próprio modelo (padrão: 1)")
    ap.add_argument("--top", type=int, default=20, help="alternativas por posição pedidas ao Ollama (top_logprobs)")
    ap.add_argument("--k", type=int, default=3, help="verbetes recuperados (condição A2)")
    ap.add_argument("--max-tokens-diagnostico", type=int, default=600)
    ap.add_argument("--max-tokens-proposta", type=int, default=700)
    ap.add_argument("--casos", type=int, default=0, help="recorta para os N primeiros casos (0 = todos); só para teste de fumaça")
    args = ap.parse_args()
    print(caminhos.descricao())
    falhas = rodar(args)
    c3b = caminhos.fase3(args.saida)
    print(f"\nResultados em {c3b['raiz']}")
    problemas = []
    if falhas:
        problemas.append(f"{len(falhas)} modelo(s) pararam antes do fim: {', '.join(falhas)}; veja as mensagens acima")
    aviso = e3b._conferir_versao_ollama_uniforme(c3b)
    if aviso:
        print(f"!! {aviso}")
        problemas.append(aviso)
    if problemas:
        raise SystemExit(" | ".join(problemas))


if __name__ == "__main__":
    main()
