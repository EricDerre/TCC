#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (05/11/2026, decisões 91 e 92) com as duas corridas em texto que faltam antes da Fase 5. A
# corrida 23 mede os itens da decisão 55 nos 90 casos, uma condição por item, contra a calibração com k = 3 da corrida 16 e com a mesma
# biblioteca dela: `exemplar` acrescenta um exemplar resolvido, fixo, antes dos dados do caso, e `rotulos_por_extenso` escreve as 23 causas
# em palavras ("campo ausente"), que é a forma natural dos tokens com espaço inicial. A corrida 24 lê em texto os 36 inéditos da ficha 27
# com a biblioteca de produção, pelo diagnóstico do agente. As leituras gravam `experimento_prompt.{json,md}` e `ineditos.{json,md}` em
# `resultados_alvo/fase4/`, pelo `avaliar_fase4.py`.
# ! Motivo: a ficha 34 (a) e a decisão 79 mandaram medir os dois itens, e o experimento não entrou na tabela de corridas do plano; a
# decisão 91 manda escrevê-lo em código novo, com o prompt do agente congelado, por isso `estrategias.py` não muda: a condição é uma
# transformação de texto do prompt pronto, conferida em teste. Sem gramática (decisão 78), o "espaço inicial do token" de Hamilton e
# Mimno (2025) não se mede direto: o modelo gera livre e escreve o espaço depois de "CAUSA_RAIZ:"; o que muda é o rótulo unido por
# sublinhado, que o tokenizador parte em pedaços, contra palavras comuns, e a literatura diz que formatos semanticamente padrão saem-se
# melhor. O índice numérico e a letra não entram, porque a decisão 91 pagou uma condição por item. A corrida 24 existe porque a
# biblioteca de produção nunca foi medida em casos inéditos (decisão 92), e só o modo `reproducao` lia esse banco.
"""Corridas 23 (itens da decisão 55 em experimento, em texto) e 24 (os 36 inéditos da ficha 27 lidos pelo modelo). Sem navegador."""
from __future__ import annotations

import argparse
import json
import platform
import re
import statistics
import time
from pathlib import Path

import analisar_fase3b as a3b
import avaliar
import avaliar_fase3
import biblioteca as bib
import caminhos
import diagnostico_ao_vivo as dv
import estrategias
import evolucao_biblioteca as evo
import executar_bateria
import executar_fase3
import executar_fase3b as e3b
import pre_fase4 as pf
import recuperacao as rec
import trilha as tr
from taxonomia import CAUSAS_RAIZ

CONDICOES = ("exemplar", "rotulos_por_extenso")
K_DO_EXPERIMENTO = 3  # a regra R8 escolheu k = 3 na corrida 16, e é contra ela que o experimento compara
NOME_EXPERIMENTO, PREFIXO_EXPERIMENTO = "experimento_prompt", "tb_f4_exp_"
NOME_INEDITOS, PREFIXO_INEDITOS = "ineditos", "tb_f4_ineditos_"
CAUSA_DO_EXEMPLAR = "erro_interno_do_servidor"
# O exemplar é de uma rota que a CobaiaAPI não tem, para não ser nenhum dos casos; a causa é a mais fácil de reconhecer, para mostrar a
# forma da resposta sem ensinar nenhuma confusão vizinha. A leitura conta quantas vezes o modelo passou a responder essa causa.
EXEMPLAR = """EXEMPLO RESOLVIDO (de outro sistema, só para mostrar a forma da resposta):
REQUISIÇÃO: GET /api/clientes/7

STATUS HTTP: 500

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto

CORPO DA RESPOSTA:
{"error": "database connection lost"}

SINTOMA OBSERVADO: A tela do cliente mostra uma mensagem de erro no lugar dos dados.

O servidor falhou ao atender a chamada: a resposta 500 traz só a mensagem de erro, sem os campos do contrato.
CAUSA_RAIZ: erro_interno_do_servidor
CAMPO: nenhum
IMPACTO: O usuário não vê os dados do cliente.
FONTE: nenhum

CASO A ANALISAR:
"""
ROTULOS_POR_EXTENSO = {
    "corpo_nao_e_json": "corpo não é JSON", "corpo_vazio": "corpo vazio", "resposta_truncada": "resposta truncada", "codificacao_incorreta": "codificação incorreta",
    "campo_ausente": "campo ausente", "campo_renomeado": "campo renomeado", "estrutura_aninhada_divergente": "estrutura aninhada divergente",
    "colecao_no_lugar_de_objeto": "coleção no lugar de objeto", "tipo_divergente": "tipo divergente", "valor_fora_do_dominio": "valor fora do domínio",
    "formato_de_data_divergente": "formato de data divergente", "nulo_inesperado": "nulo inesperado", "escala_ou_unidade_errada": "escala ou unidade errada",
    "chave_de_juncao_errada": "chave de junção errada", "contagem_inconsistente": "contagem inconsistente", "tempo_de_resposta_excedido": "tempo de resposta excedido",
    "limite_de_requisicoes": "limite de requisições", "dado_desatualizado": "dado desatualizado", "registro_duplicado": "registro duplicado",
    "erro_interno_do_servidor": "erro interno do servidor", "recurso_inexistente": "recurso inexistente", "localizador_quebrado": "localizador quebrado",
    "estado_da_tela_divergente": "estado da tela divergente",
}
_LISTA_POR_EXTENSO = "\n".join(f"  - {ROTULOS_POR_EXTENSO[c]}" for c in CAUSAS_RAIZ)
_LISTA_OFICIAL = "\n".join(f"  - {c}" for c in CAUSAS_RAIZ)


def prompt_da_condicao(condicao: str, caso: dict, contexto: str) -> str:
    """O prompt congelado (`estrategias.linear_com_biblioteca`) com a transformação da condição; `base` é ele byte a byte."""
    base = estrategias.linear_com_biblioteca(caso, contexto)
    if condicao == "base":
        return base
    if condicao == "exemplar":
        posicao = base.index(estrategias._dados_do_caso(caso), len(contexto))
        return base[:posicao] + EXEMPLAR + base[posicao:]
    if condicao == "rotulos_por_extenso":
        if base.count(_LISTA_OFICIAL) != 1:
            raise ValueError("a lista das causas não está no prompt como o experimento espera")
        return base.replace(_LISTA_OFICIAL, _LISTA_POR_EXTENSO)
    raise ValueError(f"condição desconhecida: {condicao!r} (use base ou uma de {CONDICOES})")


def _chave(texto: str) -> str:
    return " ".join(avaliar._normalizar(texto).split()).strip(" .;:,'\"")


_POR_CHAVE = {**{_chave(c): c for c in CAUSAS_RAIZ}, **{_chave(v): c for c, v in ROTULOS_POR_EXTENSO.items()}}
_LINHA_DA_CAUSA = re.compile(r"CAUSA_RAIZ\s*:\s*(.+)", re.IGNORECASE)


# ! Alteração de IA - Revisar: (05/11/2026, decisão 91) lê a linha CAUSA_RAIZ inteira, com a mesma limpeza de negrito e crase do leitor oficial.
# ! Motivo: `avaliar.extrair` guarda só a primeira palavra da linha, o que basta para o rótulo com sublinhado e transforma "campo ausente" em
# "campo"; `avaliar.py` não muda porque lê os registros oficiais, e `teste_corrida23_a_leitura_nova_nao_muda_a_corrida_16` confere a leitura
# nova contra a oficial nos 90 registros da corrida 16.
def _linha_da_causa(resposta: str | None) -> str | None:
    achado = _LINHA_DA_CAUSA.search((resposta or "").replace("*", "").replace("`", ""))
    return achado.group(1).strip() if achado else None


def _rotulo_do_inicio(chave: str) -> str | None:
    """O nome oficial do rótulo com que a linha começa; "campo_ausente_preco" não é "campo_ausente", e "campo ausente, no preco" é."""
    for rotulo, oficial in _POR_CHAVE.items():
        if chave.startswith(rotulo):
            seguinte = chave[len(rotulo):len(rotulo) + 1]
            if not seguinte or not (seguinte.isalnum() or seguinte == "_"):
                return oficial
    return None


def rotulo_lido(resposta: str | None) -> str | None:
    """O rótulo da linha CAUSA_RAIZ com o nome oficial, venha ele com sublinhado ou em palavras; fora do conjunto fica como veio."""
    linha = _linha_da_causa(resposta)
    if not linha:
        return None
    return _rotulo_do_inicio(_chave(linha)) or linha.strip(" .;:,'\"")


def diagnosticar_na_condicao(modelo: str, caso: dict, condicao: str, verbetes: list[dict], indice: rec.Indice, comum: dict, *, teto: int, top: int, k: int = K_DO_EXPERIMENTO) -> dict:
    """Um diagnóstico da condição, sem gabarito, com as mesmas opções do agente (`dv.inferir`, com logprobs como na corrida 16); o registro
    tem as 37 chaves oficiais, e a condição fica no campo `estrategia`."""
    ctx, _ = dv.montar_prompt(verbetes, indice, caso, k)
    prompt = prompt_da_condicao(condicao, caso, ctx["texto"])
    r, _captura = dv.inferir(modelo, prompt, teto, caso["id"], top)
    registro = dv.registro_oficial(modelo, caso, verbetes, ctx, prompt, r, {**comum, "k": k, "teto_tokens": teto}, executar_bateria.ambiente_residente())
    registro["estrategia"] = f"experimento_{condicao}"
    return registro


# ------------------------------------------------------------------ corrida 23: leitura

def _forma(resposta: str | None) -> str:
    chave = _chave(_linha_da_causa(resposta) or "")
    oficial = _rotulo_do_inicio(chave)
    if oficial is None:
        return "outra"
    return "oficial" if chave.startswith(oficial) else "por_extenso"


def _mediana(valores: list) -> float | None:
    numeros = [v for v in valores if isinstance(v, (int, float))]
    # ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 23) a mediana sai em duas casas.
    # ! Motivo: a leitura imprimiu "55,364999999999995" na tabela do relatório, resto da conta em ponto flutuante.
    return round(statistics.median(numeros), 2) if numeros else None


def _pct(parte: int, total: int) -> float | None:
    return round(100 * parte / total, 1) if total else None


def _celulas(registros: list[dict], gabarito: dict[str, str]) -> dict:
    saida = {}
    for r in registros:
        if r["caso"] in gabarito:
            rot = rotulo_lido(r.get("resposta"))
            saida[r["caso"]] = {"causa_correta": rot == gabarito[r["caso"]], "causa_respondida": rot}
    return saida


def _medidas(celulas: dict, gabarito: dict[str, str]) -> dict:
    n = len(celulas)
    acertos = sum(1 for c in celulas.values() if c["causa_correta"])
    pares = [(gabarito[i], c["causa_respondida"] or "") for i, c in celulas.items()]
    lo, hi = avaliar.wilson(acertos, n) if n else (None, None)
    return {"n": n, "acertos": acertos, "acerto_pct": _pct(acertos, n), "wilson_lo_pct": lo, "wilson_hi_pct": hi,
            "acuracia_balanceada_pct": avaliar_fase3.acuracia_balanceada(pares) if pares else None}


def resumir_experimento(base: list[dict], por_condicao: dict[str, list[dict]], condicoes: dict | None, corrida: str | None = None, gerado_em: str | None = None) -> dict:
    """Cada condição contra a corrida 16 com k = 3, caso a caso: acerto, acurácia balanceada, b e c (b: só a condição acerta), trocas de
    rótulo, os 36 de avaliação, formato e custo. O gabarito sai dos registros da corrida 16, e o agente nunca o vê."""
    gabarito = {r["caso"]: r["gabarito"]["causa_raiz"] for r in base}
    avaliacao = {r["caso"] for r in base if r.get("particao") == "avaliacao"}
    celulas_base = _celulas(base, gabarito)
    linhas, mudaram = [], []
    for condicao, registros in por_condicao.items():
        if not registros:
            continue
        cel = _celulas(registros, gabarito)
        base_igual = {i: celulas_base[i] for i in cel}
        par = a3b.parear(cel, base_igual)
        sub = {i: c for i, c in cel.items() if i in avaliacao}
        formas = {"oficial": 0, "por_extenso": 0, "outra": 0}
        for r in registros:
            formas[_forma(r.get("resposta"))] += 1
        par_sub = a3b.parear(sub, {i: celulas_base[i] for i in sub})
        linhas.append({"condicao": condicao, **_medidas(cel, gabarito), "n_base": len(base), "completo": len(cel) == len(base),
                       "b": par["b"], "c": par["c"], "p_mcnemar": par["p_mcnemar"], "ganhos": sorted(par["ganhos"]), "perdas": sorted(par["perdas"]),
                       "acertos_da_base_nos_mesmos": sum(1 for c in base_igual.values() if c["causa_correta"]),
                       "trocas_de_rotulo": sum(1 for i, c in cel.items() if c["causa_respondida"] != celulas_base[i]["causa_respondida"]),
                       "avaliacao": {**_medidas(sub, gabarito), "b": par_sub["b"], "c": par_sub["c"], "p_mcnemar": par_sub["p_mcnemar"]},
                       "fora_do_conjunto": sum(1 for c in cel.values() if c["causa_respondida"] and c["causa_respondida"] not in CAUSAS_RAIZ),
                       "sem_rotulo": sum(1 for c in cel.values() if c["causa_respondida"] is None), "forma": formas,
                       "causa_do_exemplar_respondida": sum(1 for c in cel.values() if c["causa_respondida"] == CAUSA_DO_EXEMPLAR),
                       "causa_do_exemplar_na_base": sum(1 for c in base_igual.values() if c["causa_respondida"] == CAUSA_DO_EXEMPLAR),
                       "tokens_entrada_mediana": _mediana([r.get("tokens_entrada") for r in registros]), "segundos_mediana": _mediana([r.get("segundos") for r in registros])})
        for i in sorted(set(par["ganhos"]) | set(par["perdas"])):
            mudaram.append({"condicao": condicao, "caso": i, "gabarito": gabarito[i], "rotulo_base": celulas_base[i]["causa_respondida"], "rotulo_condicao": cel[i]["causa_respondida"],
                            "efeito": "ganhou" if i in par["ganhos"] else "perdeu"})
    return {"metadados": {"gerado_em": gerado_em or time.strftime("%Y-%m-%dT%H:%M:%S"), "corrida": corrida, "base": "fase4_calibracao/k3 (corrida 16)"},
            "condicoes": condicoes or {}, "base": {**_medidas(celulas_base, gabarito), "tokens_entrada_mediana": _mediana([r.get("tokens_entrada") for r in base]),
                                                   "segundos_mediana": _mediana([r.get("segundos") for r in base]),
                                                   "avaliacao": _medidas({i: c for i, c in celulas_base.items() if i in avaliacao}, gabarito)},
            "por_condicao": linhas, "casos_que_mudaram": mudaram}


def _n(v) -> str:
    if v is None:
        return "n/d"
    return str(v).replace(".", ",") if isinstance(v, float) else str(v)


def _p(v) -> str:
    return "n/d" if v is None else f"{v:.3f}".replace(".", ",")


def render_experimento(dado: dict) -> str:
    b = dado["base"]
    linhas = [["corrida 16 (k = 3)", _n(b["n"]), _n(b["acertos"]), _n(b["acerto_pct"]), _n(b["acuracia_balanceada_pct"]), "", "", "", f"{_n(b['avaliacao']['acertos'])} de {_n(b['avaliacao']['n'])}",
               "", "", _n(b["tokens_entrada_mediana"]), _n(b["segundos_mediana"])]]
    for x in dado["por_condicao"]:
        linhas.append([f"`{x['condicao']}`", _n(x["n"]), _n(x["acertos"]), _n(x["acerto_pct"]), _n(x["acuracia_balanceada_pct"]), _n(x["b"]), _n(x["c"]), _p(x["p_mcnemar"]),
                       f"{_n(x['avaliacao']['acertos'])} de {_n(x['avaliacao']['n'])}", _n(x["trocas_de_rotulo"]), _n(x["fora_do_conjunto"] + x["sem_rotulo"]),
                       _n(x["tokens_entrada_mediana"]), _n(x["segundos_mediana"])])
    blocos = [a3b.tab("tb_f4_exp_resumo", ["Condição", "Casos", "Acertos", "Acerto (%)", "Acurácia balanceada (%)", "b", "c", "p (McNemar)", "Nos 36 de avaliação", "Trocas de rótulo",
                                           "Fora do conjunto ou sem rótulo", "Tokens de entrada (mediana)", "Segundos (mediana)"], linhas),
              a3b.tab("tb_f4_exp_mudaram", ["Condição", "Caso", "Gabarito", "Corrida 16", "Na condição", "Efeito"],
                      [[f"`{x['condicao']}`", f"`{x['caso']}`", f"`{x['gabarito']}`", f"`{x['rotulo_base']}`", f"`{x['rotulo_condicao']}`", x["efeito"]] for x in dado["casos_que_mudaram"]]
                      or [["nenhum"] + [""] * 5])]
    cab = pf.cabecalho("Experimento dos itens da decisão 55 (corrida 23)", "avaliar_fase4.py --experimento_prompt", f"`{dado['metadados'].get('corrida')}` contra `{dado['metadados']['base']}`",
                       dado["metadados"]["gerado_em"][:10])
    texto = ("O prompt do agente não muda em nenhuma condição: este número vai para o TCC e não decide nada na Fase 5 (decisão 91). b é o número de casos que só a condição acerta, e c, os que só a corrida 16 acerta. "
             "A corrida 16 rodou em outra versão do Ollama, e duas corridas iguais já variaram de 0 a 3 casos em 36 (Fase 3-B), então uma diferença de poucos casos não separa a condição do acaso.")
    return "\n".join([*cab, "", texto, "", *blocos]) + "\n"


# ------------------------------------------------------------------ corrida 23: execução e leitura dos arquivos

def _pasta_da_base() -> Path:
    return caminhos.fase3("fase4_calibracao")["raiz"] / "k3"


def ler_experimento(saida: str, modelo: str = "qwen2.5:7b") -> dict:
    raiz = caminhos.fase3(saida)["raiz"]
    slug = executar_fase3._slug(modelo)
    arq_cond = raiz / "condicoes_fase4.json"
    return {"base": executar_bateria.ler_jsonl(_pasta_da_base() / slug / f"diagnosticos__L{dv.VERSAO_CURADA}.jsonl"),
            "por_condicao": {c: executar_bateria.ler_jsonl(raiz / slug / f"diagnosticos__{c}.jsonl") for c in CONDICOES},
            "condicoes": json.loads(arq_cond.read_text(encoding="utf-8")) if arq_cond.exists() else {}}


def _guardas(args: argparse.Namespace, marco) -> tuple[str | None, bool]:
    """A versão do Ollama e a regra R6 (ponte da versão); devolve a versão e se a corrida pode seguir."""
    import executar_fase4 as ex
    parcial = bool(args.casos)
    versao = executar_fase3._versao_ollama()
    if versao is None:
        marco("!! o Ollama não respondeu em /api/version; suba o servidor antes da corrida")
        return None, False
    if ex.versao_precisa_de_ponte(versao, ex.carregar_pontes(gravar=not parcial)):
        if not parcial:
            marco(f"!! a versão {versao} do Ollama não tem ponte completa registrada (regra R6): rode --modo calibracao antes")
            return versao, False
        marco(f"aviso: a versão {versao} do Ollama não tem ponte completa registrada; a corrida parcial segue")
    return versao, True


def rodar_experimento(args: argparse.Namespace) -> int:
    """Corrida 23: cada condição nos 90 casos, com a biblioteca e o k da corrida 16. Relançar retoma de onde parou."""
    import executar_fase4 as ex
    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = ex._marcador(saida / "fase4.log")
    t0 = time.monotonic()
    modelo, slug = args.modelo, executar_fase3._slug(args.modelo)
    versao, segue = _guardas(args, marco)
    if not segue:
        return 2
    condicoes_pedidas = [c.strip() for c in (args.condicoes or ",".join(CONDICOES)).split(",") if c.strip()]
    for c in condicoes_pedidas:
        if c not in CONDICOES:
            marco(f"!! condição desconhecida: {c}")
            return 2
    pasta_bib = _pasta_da_base() / "bibliotecas" / slug / f"epoca-{dv.VERSAO_CURADA}"
    if not pasta_bib.exists():
        marco(f"!! sem a biblioteca da corrida 16 em {pasta_bib}")
        return 2
    hash_bib = evo.hash_biblioteca(pasta_bib)
    verbetes = bib.carregar(pasta_bib)
    indice = rec.Indice(verbetes)
    particao = e3b._particao_oficial(e3b._oficial())
    casos = list(e3b.TODOS_OS_CASOS)[:args.casos] if args.casos else list(e3b.TODOS_OS_CASOS)
    pasta_reg = saida / slug
    pasta_reg.mkdir(parents=True, exist_ok=True)
    condicoes = {"modo": "experimento_prompt", "criado_em": time.strftime("%Y-%m-%dT%H:%M:%S"), "saida": args.saida, "modelo": modelo, "versao_ollama": versao, "k": K_DO_EXPERIMENTO,
                 "condicoes": condicoes_pedidas, "casos": len(casos), "parcial": bool(args.casos), "top_logprobs": args.top, "teto_tokens": args.teto,
                 "biblioteca": {"hash": hash_bib, "origem": str(pasta_bib.relative_to(caminhos.RESULTADOS)).replace("\\", "/")},
                 "exemplar": EXEMPLAR, "causa_do_exemplar": CAUSA_DO_EXEMPLAR, "rotulos_por_extenso": ROTULOS_POR_EXTENSO}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    marco(f"INÍCIO experimento_prompt: Ollama {versao}, {modelo}, biblioteca da corrida 16 ({hash_bib}), k = {K_DO_EXPERIMENTO}; {len(condicoes_pedidas)} condição(ões) x {len(casos)} casos")
    digest, versao_ollama = e3b._preparar_modelo(modelo)
    if versao_ollama != versao:
        marco(f"!! a versão do Ollama mudou antes de começar: {versao} para {versao_ollama}")
        return 2
    comum = {"digest": digest, "versao_ollama": versao_ollama, "maquina": platform.node(), "epoca": dv.VERSAO_CURADA + 1, "biblioteca_epoca": dv.VERSAO_CURADA,
             "biblioteca_versao": hash_bib, "particao": particao}

    def _loop() -> None:
        for condicao in condicoes_pedidas:
            arq = pasta_reg / f"diagnosticos__{condicao}.jsonl"
            ex._conferir_versao_das_linhas([arq], versao)
            feitos = {r["caso"] for r in executar_bateria.ler_jsonl(arq)}
            for n, caso in enumerate(casos, 1):
                if caso["id"] in feitos:
                    continue
                registro = diagnosticar_na_condicao(modelo, ex.fixture_sem_gabarito(caso), condicao, verbetes, indice, comum, teto=args.teto, top=args.top)
                executar_fase3._gravar(arq, registro)
                ex._conferir_versao(versao)
                marco(f"[{condicao} {n}/{len(casos)}] {caso['id']}: {rotulo_lido(registro['resposta'])} ({registro['segundos']} s; {registro['tokens_entrada']} tokens)")

    try:
        e3b._com_modelo_descarregado(modelo, _loop)
    except SystemExit as e:
        marco(f"!! corrida parou: {e}")
        return 1
    marco(f"FIM experimento_prompt: {len(condicoes_pedidas)} condição(ões); duração {time.monotonic() - t0:.0f} s")
    return 0


# ------------------------------------------------------------------ corrida 24: os 36 inéditos da ficha 27

# ! Alteração de IA - Revisar: (06/11/2026) a leitura ganha o acerto com e sem o verbete certo no contexto e a comparação com a corrida 18e, que leu 25 destes casos em texto e na tela.
# ! Motivo: a leitura da corrida 24 mostrou que o verbete certo pesa de novo (18 de 20 com ele, 7 de 16 sem ele) e que o rótulo se repetiu nos 25 casos lidos duas vezes; os dois números precisam sair daqui, com `--check`.
def resumir_ineditos(registros: list[dict], linhas: list[dict], casos: list[dict], condicoes: dict | None, referencia: dict | None = None, corrida: str | None = None, gerado_em: str | None = None,
                     lado_escrito: list[dict] | None = None) -> dict:
    """A biblioteca de produção nos inéditos: acerto, acurácia balanceada, por classe, nível e selo, com e sem o verbete certo, e contra a corrida 18e. O gabarito entra só aqui, pelo id do caso."""
    por_id = {c["id"]: c for c in casos}
    extras = {x["caso"]: x for x in linhas}
    itens = []
    for r in registros:
        c = por_id.get(r["caso"])
        if not c:
            continue
        g, rot = c["gabarito"]["causa_raiz"], rotulo_lido(r.get("resposta"))
        x = extras.get(r["caso"], {})
        itens.append({"caso": r["caso"], "classe": c.get("classe"), "nivel": c.get("nivel"), "gabarito": g, "rotulo": rot, "acerto": rot == g, "p_rotulo": x.get("p_rotulo"), "selo": x.get("selo"),
                      "verbete_certo_no_contexto": g in (x.get("verbetes_ids") or r.get("verbetes_ids") or []), "tokens_entrada": r.get("tokens_entrada"), "segundos": r.get("segundos")})
    n, acertos = len(itens), sum(1 for i in itens if i["acerto"])
    lo, hi = avaliar.wilson(acertos, n) if n else (None, None)

    def grupos(chave: str) -> list[dict]:
        saida = []
        for valor in sorted({i[chave] for i in itens if i[chave] is not None}, key=str):
            sub = [i for i in itens if i[chave] == valor]
            saida.append({chave: valor, "casos": len(sub), "acertos": sum(1 for i in sub if i["acerto"]), "erros": sum(1 for i in sub if not i["acerto"])})
        return saida

    def conta(sub: list[dict]) -> dict:
        return {"casos": len(sub), "acertos": sum(1 for i in sub if i["acerto"])}

    comparacao = None
    if lado_escrito:
        e18 = {x["caso"]: x for x in lado_escrito}
        comuns = [i for i in itens if i["caso"] in e18]
        comparacao = {"casos": len(comuns), "mesmo_rotulo": sum(1 for i in comuns if i["rotulo"] == e18[i["caso"]]["rotulo_fixture"]), "acertos_aqui": sum(1 for i in comuns if i["acerto"]),
                      "acertos_escrito": sum(1 for i in comuns if e18[i["caso"]]["acerto_fixture"]), "acertos_tela": sum(1 for i in comuns if e18[i["caso"]]["acerto_tela"]),
                      "rotulo_diferente": [i["caso"] for i in comuns if i["rotulo"] != e18[i["caso"]]["rotulo_fixture"]]}
    return {"metadados": {"gerado_em": gerado_em or time.strftime("%Y-%m-%dT%H:%M:%S"), "corrida": corrida}, "condicoes": condicoes or {},
            "verbete_certo": {"presente": conta([i for i in itens if i["verbete_certo_no_contexto"]]), "ausente": conta([i for i in itens if not i["verbete_certo_no_contexto"]])}, "lado_escrito_18e": comparacao,
            "resumo": {"casos": n, "acertos": acertos, "acerto_pct": _pct(acertos, n), "wilson_lo_pct": lo, "wilson_hi_pct": hi,
                       "acuracia_balanceada_pct": avaliar_fase3.acuracia_balanceada([(i["gabarito"], i["rotulo"] or "") for i in itens]) if itens else None,
                       "erros": sorted(i["caso"] for i in itens if not i["acerto"]), "verbete_certo_no_contexto": sum(1 for i in itens if i["verbete_certo_no_contexto"]),
                       "fora_do_conjunto": sum(1 for i in itens if i["rotulo"] and i["rotulo"] not in CAUSAS_RAIZ), "sem_rotulo": sum(1 for i in itens if i["rotulo"] is None),
                       "tokens_entrada_mediana": _mediana([i["tokens_entrada"] for i in itens]), "segundos_mediana": _mediana([i["segundos"] for i in itens])},
            "por_classe": grupos("classe"), "por_nivel": grupos("nivel"), "por_selo": grupos("selo"), "referencia": referencia, "casos": itens}


def render_ineditos(dado: dict) -> str:
    r, ref, e = dado["resumo"], dado.get("referencia") or {}, dado.get("lado_escrito_18e")

    def grupo(nome: str, chave: str, rotulo: str, linhas: list[dict]) -> str:
        return a3b.tab(nome, [rotulo, "Casos", "Acertos", "Erros"], [[_n(x[chave]), _n(x["casos"]), _n(x["acertos"]), _n(x["erros"])] for x in linhas] or [["sem casos", "", "", ""]])

    blocos = [a3b.tab("tb_f4_ineditos_resumo", ["Casos", "Acertos", "Acerto (%)", "Wilson 95%", "Acurácia balanceada (%)", "Verbete certo no contexto", "Fora do conjunto ou sem rótulo",
                                                "Tokens de entrada (mediana)", "Segundos (mediana)", "Os 36 oficiais, com a mesma biblioteca (corrida 22)"],
                      [[_n(r["casos"]), _n(r["acertos"]), _n(r["acerto_pct"]), f"{_n(r['wilson_lo_pct'])} a {_n(r['wilson_hi_pct'])}", _n(r["acuracia_balanceada_pct"]), _n(r["verbete_certo_no_contexto"]),
                        _n(r["fora_do_conjunto"] + r["sem_rotulo"]), _n(r["tokens_entrada_mediana"]), _n(r["segundos_mediana"]),
                        f"{_n(ref.get('acertos'))} de {_n(ref.get('casos'))} ({_n(ref.get('acerto_pct'))}%)" if ref else "n/d"]]),
              grupo("tb_f4_ineditos_classe", "classe", "Classe", dado["por_classe"]), grupo("tb_f4_ineditos_nivel", "nivel", "Nível", dado["por_nivel"]),
              grupo("tb_f4_ineditos_selo", "selo", "Selo", dado["por_selo"]),
              a3b.tab("tb_f4_ineditos_verbete", ["Verbete da causa certa entre os entregues", "Casos", "Acertos", "Acerto (%)"],
                      [[rotulo, _n(v["casos"]), _n(v["acertos"]), _n(_pct(v["acertos"], v["casos"]))] for rotulo, v in (("sim", dado["verbete_certo"]["presente"]), ("não", dado["verbete_certo"]["ausente"]))]),
              a3b.tab("tb_f4_ineditos_18e", ["Casos também lidos na corrida 18e", "Mesmo rótulo do caso escrito da 18e", "Acertos aqui", "Acertos no caso escrito da 18e", "Acertos na tela da 18e"],
                      [[_n(e["casos"]), _n(e["mesmo_rotulo"]), _n(e["acertos_aqui"]), _n(e["acertos_escrito"]), _n(e["acertos_tela"])]] if e else [["sem a leitura da corrida 18e", "", "", "", ""]]),
              a3b.tab("tb_f4_ineditos_casos", ["Caso", "Classe", "Nível", "Gabarito", "Rótulo", "Certo", "Probabilidade", "Selo", "Verbete certo no contexto"],
                      [[f"`{i['caso']}`", _n(i["classe"]), _n(i["nivel"]), f"`{i['gabarito']}`", f"`{i['rotulo']}`", "sim" if i["acerto"] else "não", _p(i["p_rotulo"]), _n(i["selo"]),
                        "sim" if i["verbete_certo_no_contexto"] else "não"] for i in dado["casos"]] or [["nenhum"] + [""] * 8])]
    cab = pf.cabecalho("Os 36 inéditos da ficha 27 lidos pelo modelo (corrida 24)", "avaliar_fase4.py --ineditos", f"`{dado['metadados'].get('corrida')}`", dado["metadados"]["gerado_em"][:10])
    texto = ["A biblioteca de produção lê casos que nenhuma biblioteca viu, em texto e sem gabarito no agente: é a única medida da biblioteca final em casos inéditos (decisão 92)."]
    return "\n".join(cab + [""] + texto + [""] + blocos) + "\n"


def ler_ineditos(saida: str, modelo: str = "qwen2.5:7b") -> dict:
    import banco_casos_ineditos_fase4 as bi4
    raiz = caminhos.fase3(saida)["raiz"]
    arq_cond = raiz / "condicoes_fase4.json"
    arq_ref = caminhos.RESULTADOS / "fase4" / "trilha.json"
    resumo_ref = (json.loads(arq_ref.read_text(encoding="utf-8")).get("resumo") or {}) if arq_ref.exists() else {}
    arq_18e = caminhos.RESULTADOS / "fase4" / "tela_ineditos.json"
    lado_escrito = json.loads(arq_18e.read_text(encoding="utf-8")).get("casos") if arq_18e.exists() else None
    return {"registros": executar_bateria.ler_jsonl(raiz / executar_fase3._slug(modelo) / "diagnosticos__ineditos.jsonl"), "linhas": executar_bateria.ler_jsonl(raiz / "ineditos.jsonl"),
            "casos": bi4.CASOS_INEDITOS_FASE4, "condicoes": json.loads(arq_cond.read_text(encoding="utf-8")) if arq_cond.exists() else {},
            "referencia": {k: resumo_ref.get(k) for k in ("casos", "acertos", "acerto_pct")} if resumo_ref else None,
            "lado_escrito": lado_escrito}


def rodar_ineditos(args: argparse.Namespace) -> int:
    """Corrida 24: os 36 inéditos em texto, pelo diagnóstico do agente, com a biblioteca de produção e o k e os limiares da calibração. Relançar retoma."""
    import executar_fase4 as ex
    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = ex._marcador(saida / "fase4.log")
    t0 = time.monotonic()
    inicio = time.strftime("%Y-%m-%dT%H:%M:%S")
    modelo, slug = args.modelo, executar_fase3._slug(args.modelo)
    versao, segue = _guardas(args, marco)
    if not segue:
        return 2
    limiares = dv.carregar_limiares(Path(args.limiares) if args.limiares else None)
    if limiares is None and not args.casos:
        marco("!! sem limiares.json (regra R7): rode --modo calibracao antes")
        return 2
    k = int((limiares or {}).get("k") or K_DO_EXPERIMENTO)
    if not evo.snapshot_fechado(dv.PASTA_CURADA):
        marco(f"!! a biblioteca de produção em {dv.PASTA_CURADA} não existe ou não está fechada (sem fechamento.json)")
        return 2
    pasta_bib = saida / "bibliotecas" / slug / f"epoca-{dv.VERSAO_CURADA}"
    hash_bib = e3b._preparar_copia(dv.PASTA_CURADA, pasta_bib)
    verbetes = bib.carregar(pasta_bib)
    indice = rec.Indice(verbetes)
    casos = ex.casos_de_avaliacao("ineditos_fase4")
    casos = casos[:args.casos] if args.casos else casos
    caso0 = ex.fixture_sem_gabarito(casos[0])
    ctx0, prompt0 = dv.montar_prompt(verbetes, indice, caso0, k)
    hash_fixo = dv.hash_prompt_fixo(verbetes, ctx0, caso0, prompt0)
    pasta_reg = saida / slug
    pasta_reg.mkdir(parents=True, exist_ok=True)
    arq_diag, arq_lat, arq_resumo, arq_trilha = pasta_reg / "diagnosticos__ineditos.jsonl", pasta_reg / "logprobs__ineditos.jsonl", saida / "ineditos.jsonl", saida / "trilha_ineditos.jsonl"
    feitos = {r["caso"] for r in executar_bateria.ler_jsonl(arq_resumo)}
    condicoes = {"modo": "ineditos", "criado_em": inicio, "saida": args.saida, "modelo": modelo, "versao_ollama": versao, "k": k, "limiares": limiares, "casos": len(casos), "parcial": bool(args.casos),
                 "top_logprobs": args.top, "teto_tokens": args.teto, "hash_prompt_fixo": hash_fixo, "hash_indice": dv.hash_indice(indice), "biblioteca": {"hash": hash_bib, "origem": "Programacao/AgenteCore/biblioteca_producao"}}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    marco(f"INÍCIO ineditos: Ollama {versao}, {modelo}, biblioteca de produção ({hash_bib}), k = {k}; {len(casos)} casos; {len(feitos)} já feito(s)")
    digest, versao_ollama = e3b._preparar_modelo(modelo)
    if versao_ollama != versao:
        marco(f"!! a versão do Ollama mudou antes de começar: {versao} para {versao_ollama}")
        return 2
    comum = {"digest": digest, "versao_ollama": versao_ollama, "maquina": platform.node(), "epoca": dv.VERSAO_CURADA + 1, "biblioteca_epoca": dv.VERSAO_CURADA, "biblioteca_versao": hash_bib, "particao": None}
    if arq_trilha.exists() and feitos:
        trilha = tr.Trilha.carregar(arq_trilha)
        trilha.pasta_blobs = saida / "blobs"
    else:
        trilha = tr.Trilha(versao=tr.V2, pasta_blobs=saida / "blobs")
        trilha.corrida(tr.cabecalho_de_corrida(modelo=modelo, versao_ollama=versao, inicio=inicio, quantizacao=dv.quantizacao_do_modelo(modelo), top_logprobs=args.top,
                                               leitura_da_probabilidade=dv.LEITURA_DA_PROBABILIDADE, hash_biblioteca=hash_bib, hash_prompt_fixo=hash_fixo, hash_indice=dv.hash_indice(indice), corrida=args.saida,
                                               etapas_registradas=["recuperacao", "prompt", "diagnostico"], etapas_nao_registradas=["roteiro", "interceptacao", "poda", "cura", "edicao_biblioteca", "intervencao"],
                                               extras={"modo": "ineditos", "k": k, "limiares": limiares}), ts=inicio)

    def _loop() -> None:
        for n, caso in enumerate(casos, 1):
            if caso["id"] in feitos:
                continue
            caso_f = ex.fixture_sem_gabarito(caso)
            tid = f"{args.saida}/{slug}/{caso['id']}"
            ts = time.strftime("%Y-%m-%dT%H:%M:%S")
            trilha.evento("entrada", tid, {"caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"], "origem": "fixture", "texto": trilha.blob(estrategias._dados_do_caso(caso_f), "caso")}, "ao_vivo", ts=ts)
            sv = dv.diagnosticar(trilha, tid, caso_f, verbetes, indice, k=k, modelo=modelo, comum=comum, limiares=limiares, intervencoes="desligadas", top=args.top, teto=args.teto, ts=ts)
            executar_fase3._gravar(arq_diag, sv["registro"])
            executar_fase3._gravar(arq_lat, sv["lateral"])
            confianca = sv["no"]["confianca"]
            executar_fase3._gravar(arq_resumo, {"caso": caso["id"], "p_rotulo": confianca.get("p_rotulo"), "selo": confianca.get("selo"), "verbetes_ids": sv["registro"]["verbetes_ids"], "segundos": sv["registro"]["segundos"]})
            trilha.gravar(arq_trilha)
            ex._conferir_versao(versao)
            marco(f"[{n}/{len(casos)}] {caso['id']}: {sv['no']['escolha']} (p {confianca.get('p_rotulo')}, selo {confianca.get('selo')}; {sv['registro']['segundos']} s)")

    try:
        e3b._com_modelo_descarregado(modelo, _loop)
    except SystemExit as e:
        marco(f"!! corrida parou: {e}")
        return 1
    trilha.fechar(time.strftime("%Y-%m-%dT%H:%M:%S"))
    trilha.gravar(arq_trilha)
    marco(f"FIM ineditos: {len(casos)} casos; duração {time.monotonic() - t0:.0f} s; trilha {arq_trilha.stat().st_size} bytes")
    return 0
