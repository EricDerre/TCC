#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (05/11/2026, ficha 42): mede, sem modelo, de onde vêm os tokens do prompt na
# tela nas corridas 18b e 21b e quanto cada corte tiraria, lendo os prompts guardados nas trilhas e os tokens de entrada
# medidos pelo Ollama. Grava `resultados_alvo/fase4/prompt_tela_blocos.json`; `--check` confere sem gravar.
# ! Motivo: o plano aprovado (seção 3.3) limita o prompt ao vivo ao maior da calibração mais 10%, e na corrida 18b os 37
# prompts passaram disso. O Eric decidiu apertar e repetir (decisão 90), mas a ficha 42 falava só da poda da árvore, e o
# corte precisa ser dimensionado antes de ocupar a máquina. Os tokens depois de cada corte são uma estimativa: desconta os
# caracteres cortados pela razão de tokens por caractere do próprio prompt. Nas corridas 18b e 21b o que o caso ao vivo
# acrescenta tem menos caracteres por token que o prompt inteiro, então a estimativa erra para mais, não para menos.
"""Quanto cada bloco pesa no prompt da tela (corridas 18b e 21b) e quanto cada corte tiraria, sem modelo (ficha 42)."""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

import caminhos

SEPARADOR = "\n\n=====\n\n"
CABECALHOS = (("requisicao", "REQUISIÇÃO: "), ("status", "STATUS HTTP: "), ("contrato", "CONTRATO ESPERADO PELA INTERFACE: "), ("corpo", "CORPO DA RESPOSTA:\n"),
              ("arvore", "ÁRVORE DE ACESSIBILIDADE DA PÁGINA:\n"), ("seletor", "SELETOR QUE FALHOU: "), ("sintoma", "SINTOMA OBSERVADO: "),
              ("observacao", "OBSERVAÇÃO ADICIONAL: "), ("formato", "Depois do raciocínio"))
ORDEM = ("instrucao", *(nome for nome, _ in CABECALHOS))
DESCRICAO_DOS_CENARIOS = {
    "hoje": "o prompt como rodou",
    "arvore": "a árvore só com o título e o que difere da referência em modo normal",
    "arvore_observacao": "o corte da árvore e sem a linha OBSERVAÇÃO ADICIONAL",
    "arvore_observacao_sintoma": "os dois cortes e o SINTOMA só com as contagens de linhas, sem as listas faltam e sobram",
    "sem_arvore": "para comparar: sem nenhuma árvore e com o resto como rodou",
}
CORRIDAS = {"18b": ("fase4_tela_v2", "trilha_tela.jsonl", "diagnosticos__tela.jsonl"), "21b": ("fase4_ensaio_v2", "trilha_cenarios.jsonl", "diagnosticos__cenarios.jsonl")}
MODELO = "qwen2.5_7b"
CALIBRACAO = Path("fase4_calibracao") / "k3" / MODELO / "diagnosticos__L100.jsonl"
ARQUIVO = "prompt_tela_blocos.json"
_LISTA_DO_SINTOMA = re.compile(r"; (?:faltam|sobram): .*?(?=\. A tela mostra \d|\.\s*\Z)", re.S)


def blocos_do_prompt(prompt: str) -> dict[str, str]:
    """O prompt repartido nos blocos de `estrategias.linear_com_biblioteca`, sem perder nem repetir texto."""
    verbetes, _, resto = prompt.partition(SEPARADOR)
    posicoes = sorted((resto.find(h), nome) for nome, h in CABECALHOS if h in resto)
    fora = {"verbetes": verbetes, "instrucao": resto[: posicoes[0][0]]}
    for i, (inicio, nome) in enumerate(posicoes):
        fora[nome] = resto[inicio: posicoes[i + 1][0] if i + 1 < len(posicoes) else len(resto)]
    return fora


def _montar(blocos: dict[str, str]) -> str:
    return blocos["verbetes"] + SEPARADOR + "".join(blocos.get(nome, "") for nome in ORDEM)


def _sem_cartoes(linhas: list[str]) -> list[str]:
    fica, recuo = [], None
    for linha in linhas:
        atual = len(linha) - len(linha.lstrip())
        if recuo is not None and atual > recuo:
            continue
        recuo = None
        if linha.strip() == "group":
            recuo = atual
            continue
        fica.append(linha)
    return fica


def arvore_contra_referencia(arvore: str, referencias: dict[str, str]) -> str:
    """O título e as linhas que a referência em modo normal da mesma página não tem. Página sem referência guardada (as do
    front nos cenários de localizador): tira o que é comum com as referências que existem (navegação e rodapé) e os cartões."""
    linhas = arvore.strip("\n").splitlines()
    if not linhas:
        return ""
    titulo, corpo = linhas[0], linhas[1:]
    mesma_pagina = [t for t in referencias.values() if t.splitlines()[:1] == [titulo]]
    if mesma_pagina:
        iguais = set(max(mesma_pagina, key=lambda t: len(set(t.splitlines()) & set(corpo))).splitlines())
    else:
        iguais = {linha for t in referencias.values() for linha in t.splitlines()[1:]}
        corpo = _sem_cartoes(corpo)
    return "\n".join([titulo, *(linha for linha in corpo if linha not in iguais)])


def sintoma_sem_listas(sintoma: str) -> str:
    """Guarda as contagens de linhas a menos e a mais e tira as listas `faltam` e `sobram`, que chegavam a repetir `- img`."""
    return _LISTA_DO_SINTOMA.sub("", sintoma)


def cortes(prompt: str, referencias: dict[str, str]) -> dict[str, str]:
    """O prompt em cada cenário de `DESCRICAO_DOS_CENARIOS`, na ordem dela."""
    b = blocos_do_prompt(prompt)
    cabecalho = dict(CABECALHOS)["arvore"]
    arvore = cabecalho + arvore_contra_referencia(b["arvore"][len(cabecalho):], referencias) + "\n\n" if "arvore" in b else ""
    return {"hoje": prompt,
            "arvore": _montar({**b, "arvore": arvore}),
            "arvore_observacao": _montar({**b, "arvore": arvore, "observacao": ""}),
            "arvore_observacao_sintoma": _montar({**b, "arvore": arvore, "observacao": "", "sintoma": sintoma_sem_listas(b.get("sintoma", ""))}),
            "sem_arvore": _montar({**b, "arvore": ""})}


def tokens_apos_corte(tokens: int, chars: int, cortados: int) -> int:
    return round(tokens - cortados * tokens / chars)


def limite_do_plano(maior_da_calibracao: int) -> int:
    """Plano, seção 3.3: o maior prompt da calibração mais 10%, arredondado para baixo."""
    return maior_da_calibracao * 11 // 10


def resumo(valores: list) -> dict:
    return {"min": min(valores), "mediana": statistics.median(valores), "max": max(valores)}


def _jsonl(arq: Path) -> list[dict]:
    return [json.loads(linha) for linha in arq.read_text(encoding="utf-8").splitlines() if linha.strip()]


def _ler_corrida(raiz: Path, pasta: str, arq_trilha: str, arq_diag: str) -> tuple[list[tuple[str, int, str]], dict[str, str]]:
    trilha = _jsonl(raiz / pasta / arq_trilha)
    textos = {r["dados"]["sha"]: r["dados"]["texto"] for r in trilha if r["tipo"] == "blob"}
    prompts = {r["trilha"].split("/")[-1]: textos[r["dados"]["sha"]] for r in trilha if r["tipo"] == "prompt" and r["dados"].get("etapa") == "diagnostico"}
    referencias = {r["trilha"].split("/")[-1]: textos[r["dados"]["sha"]] for r in trilha
                   if r["tipo"] == "poda" and r["dados"].get("alvo") == "arvore" and "/referencia/" in r["trilha"] and r["dados"].get("sha") in textos}
    registros = []
    for d in _jsonl(raiz / pasta / MODELO / arq_diag):
        base = d["caso"].split("@")[0]
        prompt = prompts.get(d["caso"]) or prompts.get(base) or next((v for nome, v in prompts.items() if nome.startswith(base)), None)
        if prompt is None:
            raise SystemExit(f"{pasta}: sem prompt guardado para {d['caso']}")
        registros.append((d["caso"], d["tokens_entrada"], prompt))
    return registros, referencias


def _ler_corrida_resumida(raiz: Path, pasta: str, arq_trilha: str, arq_diag: str, limite: int) -> dict:
    registros, referencias = _ler_corrida(raiz, pasta, arq_trilha, arq_diag)
    por_cenario: dict[str, list[tuple[str, int]]] = {nome: [] for nome in DESCRICAO_DOS_CENARIOS}
    blocos: dict[str, list[int]] = {}
    for caso, tokens, prompt in registros:
        for nome, texto in blocos_do_prompt(prompt).items():
            blocos.setdefault(nome, []).append(len(texto))
        for nome, texto in cortes(prompt, referencias).items():
            por_cenario[nome].append((caso, tokens_apos_corte(tokens, len(prompt), len(prompt) - len(texto))))
    return {"pasta": pasta, "prompts": len(registros), "referencias": sorted(referencias),
            "chars_por_token": {k: round(v, 2) for k, v in resumo([len(p) / t for _, t, p in registros]).items()},
            "blocos_chars": {nome: resumo(valores + [0] * (len(registros) - len(valores))) for nome, valores in sorted(blocos.items())},
            "cenarios": {nome: {"descricao": DESCRICAO_DOS_CENARIOS[nome], **resumo([t for _, t in itens]), "acima_do_limite": sum(t > limite for _, t in itens),
                                "casos_acima": sorted(c for c, t in itens if t > limite)} for nome, itens in por_cenario.items()}}


def medir(raiz: Path) -> dict:
    maior = max(r["tokens_entrada"] for r in _jsonl(raiz / CALIBRACAO))
    limite = limite_do_plano(maior)
    return {"o_que_e": "de onde vêm os tokens do prompt na tela nas corridas 18b e 21b e quanto cada corte tiraria, sem modelo; os tokens depois de cada corte são estimados pela razão de tokens por caractere do próprio prompt",
            "limite": {"tokens": limite, "maior_da_calibracao": maior, "origem": f"maior tokens_entrada de {CALIBRACAO.as_posix()} mais 10% (plano, seção 3.3)"},
            "corridas": {nome: _ler_corrida_resumida(raiz, *arquivos, limite) for nome, arquivos in CORRIDAS.items()}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="confere o arquivo gravado contra os dados, sem gravar")
    args = ap.parse_args()
    dado = medir(caminhos.RESULTADOS)
    texto = json.dumps(dado, ensure_ascii=False, indent=2) + "\n"
    arq = caminhos.RESULTADOS / "fase4" / ARQUIVO
    if args.check:
        if not arq.exists() or arq.read_text(encoding="utf-8") != texto:
            print(f"--check: {arq.name} DIFERE dos dados atuais")
            return 1
        print(f"--check: {arq.name} bate com os dados atuais")
        return 0
    arq.write_text(texto, encoding="utf-8")
    print(f"gravado em {arq}")
    for nome, c in dado["corridas"].items():
        for cenario, v in c["cenarios"].items():
            print(f"{nome} {cenario}: min {v['min']}, mediana {v['mediana']}, max {v['max']}, acima de {dado['limite']['tokens']}: {v['acima_do_limite']} de {c['prompts']} {v['casos_acima'] if v['acima_do_limite'] <= 5 else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
