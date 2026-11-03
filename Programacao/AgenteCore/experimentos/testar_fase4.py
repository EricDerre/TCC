#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria testar_fase4.py, o runner de testes da Fase 4 (pacote P0: ambiente_fase4.py e
# navegador.py; os pacotes seguintes acrescentam os seus testes aqui), no mesmo formato sem pytest de
# testar_pre_fase4.py: funções teste_<nome>(), main() roda todas em ordem de definição e termina em "N testes ok".
# A tag deste cabeçalho cobre as funções de teste e os ajudantes de teste. Com `--gravar-hashes`, grava em
# fixtures_fase4/hashes_areas_so_leitura.json o hash de conteúdo das áreas que a Fase 4 não pode alterar.
# ! Motivo: o plano aprovado da Fase 4 (seção 5, P0) pede os testes escritos antes do código: que o ambiente.json
# tenha as quatro versões (Python, Playwright, navegador, Ollama), que a fixture da árvore de acessibilidade tenha
# papel e nome em cada nó, e o hash das áreas só de leitura antes e depois de cada pacote. Os testes são escritos
# ANTES dos módulos: a primeira rodada falha por ModuleNotFoundError nos imports abaixo, que é o RED aceito para
# módulo novo. O hash é de conteúdo (não de mtime, como em testar_fase3b._hash_arvore), com CRLF lido como LF, para
# a mesma gravação dar o mesmo hash em outra máquina depois de um clone; as áreas somam cerca de 36 MB em 26/10/2026.
"""Testes da Fase 4, sem pytest (asserts em Python puro)."""
import argparse
import datetime as dt
import hashlib
import inspect
import json
import sys
import traceback
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

EXP = Path(__file__).resolve().parent
AGENTE = EXP.parent
RAIZ = AGENTE.parent.parent
RA = EXP / "resultados_alvo"
FIX = EXP / "fixtures_fase4"
ARQUIVO_HASHES = FIX / "hashes_areas_so_leitura.json"

import ambiente_fase4
import navegador

# ! Alteração de IA - Revisar: imports do pacote P1 (26/10/2026): trilha v2 e relatório v2, mais o avaliador para as
# respostas sintéticas. Os testes do P1 ficam na seção "P1" abaixo e seguem a mesma regra: escritos antes do código.
# ! Motivo: o plano aprovado (seção 5, P1) pede os testes antes: leitor v2 lendo v1 sem perda, nó sem divergência
# rejeitado, molde que nunca cita verbete fora da evidência, diff que acha o primeiro nó divergente e tolera a
# variação declarada, valores declarados como trecho literal, seções do relatório em ordem fixa.
import gerar_relatorio_raciocinio as grr
import trilha


def _areas_so_leitura() -> dict[str, Path]:
    """As pastas que a Fase 4 só lê (plano aprovado, seção 2, princípio 7): base_conhecimento, biblioteca_producao,
    resultados_alvo/fase3, resultados_alvo/fase3b_* e resultados_alvo/pre_fase4_confianca."""
    areas = {"base_conhecimento": AGENTE / "base_conhecimento",
             "biblioteca_producao": AGENTE / "biblioteca_producao",
             "fase3": RA / "fase3",
             "pre_fase4_confianca": RA / "pre_fase4_confianca"}
    for pasta in sorted(RA.glob("fase3b_*")):
        if pasta.is_dir():
            areas[pasta.name] = pasta
    return areas


def _hash_conteudo(raiz: Path) -> str | None:
    """sha256 de (caminho relativo, conteúdo com CRLF trocado por LF) de cada arquivo sob raiz, em ordem; None se a
    pasta não existir."""
    if not raiz.exists():
        return None
    h = hashlib.sha256()
    for p in sorted(raiz.rglob("*")):
        if p.is_file():
            h.update(p.relative_to(raiz).as_posix().encode("utf-8") + b"\0")
            h.update(p.read_bytes().replace(b"\r\n", b"\n") + b"\0")
    return h.hexdigest()[:16]


def gravar_hashes() -> dict[str, str | None]:
    FIX.mkdir(parents=True, exist_ok=True)
    areas = {nome: _hash_conteudo(p) for nome, p in _areas_so_leitura().items()}
    dados = {"gravado_em": dt.datetime.now().isoformat(timespec="seconds"), "areas": areas,
             # a tag vai num campo porque JSON não aceita comentário; conferir_docs.py procura o texto dela no arquivo
             "tag_ia": {"alteracao": "! Alteração de IA - Revisar: gravado por `testar_fase4.py --gravar-hashes` (Fase 4, "
                                     "pacote P0): hash de conteúdo de cada área só de leitura, para o teste comparar a cada rodada.",
                        "motivo": "! Motivo: o plano aprovado exige o hash antes e depois de cada pacote; o hash é de conteúdo "
                                  "com CRLF lido como LF, para valer depois de um clone em outra máquina."}}
    ARQUIVO_HASHES.write_text(json.dumps(dados, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return areas


# ----------------------------------------------------------------------------- P0: ambiente

def teste_ambiente_montar_exige_as_quatro_versoes():
    dados = ambiente_fase4.montar(python="3.14.7", playwright="1.64.1", navegador="156.0.8078.4", ollama="0.40.2",
                                  canal="chromium", executavel="x.exe", maquina={"so": "w"}, cobaias={"php": None})
    assert tuple(sorted(dados["versoes"])) == ambiente_fase4.CHAVES_VERSAO, dados["versoes"]
    assert dados["navegador"] == {"canal": "chromium", "executavel": "x.exe", "modo": "headless"}, dados["navegador"]
    for faltando in ("python", "playwright", "navegador", "ollama"):
        kw = dict(python="3.14.7", playwright="1.64.1", navegador="156", ollama="0.40.2", canal="chromium",
                  executavel="x.exe", maquina={}, cobaias={})
        kw[faltando] = ""
        try:
            ambiente_fase4.montar(**kw)
        except ValueError as e:
            assert faltando in str(e), (faltando, e)
        else:
            raise AssertionError(f"montar aceitou {faltando} vazio")
    try:
        ambiente_fase4.montar(python="3", playwright="1", navegador="1", ollama="1", canal="firefox",
                              executavel="x", maquina={}, cobaias={})
    except ValueError as e:
        assert "canal" in str(e), e
    else:
        raise AssertionError("montar aceitou canal fora de chromium/msedge")


def teste_ambiente_json_tem_as_quatro_versoes():
    caminho = RA / "fase4" / "ambiente.json"
    assert caminho.exists(), f"{caminho} não existe: rode `RESULTADOS_DIR=resultados_alvo python ambiente_fase4.py`"
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    versoes = dados["versoes"]
    assert tuple(sorted(versoes)) == ambiente_fase4.CHAVES_VERSAO, versoes
    for chave, valor in versoes.items():
        assert isinstance(valor, str) and valor.strip() and valor[0].isdigit(), (chave, valor)
    assert dados["navegador"]["canal"] in navegador.CANAIS, dados["navegador"]
    assert dados["navegador"]["modo"] == "headless", dados["navegador"]
    assert "cobaias" in dados and "gravado_em" in dados, sorted(dados)


# ----------------------------------------------------------------------------- P0: árvore de acessibilidade

ARIA_EXEMPLO = """- navigation:
  - link "PRODUTOS":
    - /url: produtos.php
  - link "PRODUTOS (API)"
- main:
  - heading "Produtos via API" [level=2]
  - text: Carregando produtos da CobaiaAPI...
  - group:
    - heading "Picanha ao Alho" [level=3]
    - button "R$ 89,90" [disabled]
    - button "Saiba Mais..."
"""


def teste_parse_aria_le_papel_nome_e_profundidade():
    nos = navegador.parse_aria(ARIA_EXEMPLO)
    assert [n["papel"] for n in nos][:3] == ["navigation", "link", "link"], nos[:3]
    # a linha de propriedade (/url) não vira nó: é atributo do link acima dela
    assert nos[1] == {"papel": "link", "nome": "PRODUTOS", "profundidade": 1, "atributos": {"url": "produtos.php"}}, nos[1]
    assert nos[2] == {"papel": "link", "nome": "PRODUTOS (API)", "profundidade": 1, "atributos": {}}, nos[2]
    titulo = [n for n in nos if n["papel"] == "heading" and n["nome"] == "Produtos via API"][0]
    assert titulo["atributos"] == {"level": "2"} and titulo["profundidade"] == 1, titulo
    texto = [n for n in nos if n["papel"] == "text"][0]
    assert texto["nome"] == "Carregando produtos da CobaiaAPI...", texto
    preco = [n for n in nos if n["nome"] == "R$ 89,90"][0]
    assert preco["papel"] == "button" and preco["atributos"] == {"disabled": "true"} and preco["profundidade"] == 2, preco
    assert all(set(n) == {"papel", "nome", "profundidade", "atributos"} for n in nos), nos
    assert not any(n["papel"].startswith("/") for n in nos), nos
    # o formato real da versão instalada: filho `strong: texto` sob o heading e parágrafo com texto entre aspas
    real = navegador.parse_aria('- heading "Produtos via API" [level=2]:\n  - strong: Produtos via API\n'
                                '- paragraph: "Resumo: carne"\n- img\n')
    assert real[1] == {"papel": "strong", "nome": "Produtos via API", "profundidade": 1, "atributos": {}}, real[1]
    assert real[2] == {"papel": "paragraph", "nome": "Resumo: carne", "profundidade": 0, "atributos": {}}, real[2]
    assert real[3] == {"papel": "img", "nome": "", "profundidade": 0, "atributos": {}}, real[3]


def _conferir_fixture_arvore(caminho: Path) -> dict:
    assert caminho.exists(), f"{caminho} não existe: rode `python navegador.py --fixture ...`"
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    for chave in ("origem", "gravado_em", "playwright", "navegador", "canal", "aria", "nos", "contagem"):
        assert chave in dados, (chave, sorted(dados))
    assert dados["contagem"] == len(dados["nos"]) > 0, dados["contagem"]
    for no in dados["nos"]:
        assert isinstance(no["papel"], str) and no["papel"], no
        assert isinstance(no["nome"], str), no
        assert isinstance(no["profundidade"], int) and no["profundidade"] >= 0, no
    assert dados["nos"] == navegador.parse_aria(dados["aria"]), "nos não bate com o texto aria gravado"
    papeis_nomes = {(n["papel"], n["nome"]) for n in dados["nos"]}
    assert ("heading", "Produtos via API") in papeis_nomes, sorted(papeis_nomes)[:20]
    assert ("button", "Saiba Mais...") in papeis_nomes, sorted(papeis_nomes)[:20]
    return dados


def teste_fixture_estatica_da_arvore_tem_papel_e_nome():
    """A amostra provisória, capturada da cópia estática da página (sem PHP nem MariaDB na máquina)."""
    dados = _conferir_fixture_arvore(FIX / "arvore_pagina_estatica_produtos_api.json")
    assert dados["origem"].startswith("file:///"), dados["origem"]
    assert dados.get("provisoria") is True and dados.get("motivo"), dados.get("motivo")


# ----------------------------------------------------------------------------- áreas só de leitura

def teste_areas_so_leitura_intocadas():
    assert ARQUIVO_HASHES.exists(), f"{ARQUIVO_HASHES} não existe: rode `python testar_fase4.py --gravar-hashes`"
    gravado = json.loads(ARQUIVO_HASHES.read_text(encoding="utf-8"))["areas"]
    agora = {nome: _hash_conteudo(p) for nome, p in _areas_so_leitura().items()}
    assert set(agora) == set(gravado), (sorted(set(agora) ^ set(gravado)))
    diferentes = sorted(nome for nome in agora if agora[nome] != gravado[nome])
    assert not diferentes, f"áreas só de leitura alteradas desde a gravação: {diferentes}"


# ----------------------------------------------------------------------------- P1: trilha v2

import tempfile
import shutil

_TEMPORARIOS: list[Path] = []
TS = "2026-10-26T20:00:00"
RESPOSTA_V2 = ("CAUSA_RAIZ: campo_renomeado\nCAMPO: preco\nIMPACTO: o cartão mostra o preço vazio.\n"
               "FONTE: [contrato-produto]")


def _temp() -> Path:
    p = Path(tempfile.mkdtemp(prefix="fase4_teste_"))
    _TEMPORARIOS.append(p)
    return p


def _cabecalho() -> dict:
    return trilha.cabecalho_de_corrida(modelo="qwen2.5:7b", versao_ollama="0.40.2", inicio=TS, hash_biblioteca="1fca10f1a6f6",
                                       hash_prompt_fixo="abc", hash_indice="def", playwright="1.64.1", navegador="156.0.8078.4")


def _no(**mudancas) -> dict:
    base = dict(decisao="diagnostico", escolha="campo_renomeado",
                alternativas=[{"opcao": "campo_renomeado", "escore": 0.63}, {"opcao": "tipo_incompativel", "escore": 0.21}],
                evidencia=[{"seq": 2, "papel": "sinal_em_codigo"}, {"seq": 3, "papel": "verbete_entregue", "id": "contrato-produto"}],
                resultado="rotulo_emitido", divergencia={"ha": False, "entre": [], "detalhe": None},
                confianca={"logprob_rotulo": -0.46, "p_rotulo": 0.63, "alternativas_top": 2, "selo": "medio"},
                prov={"used": ["contrato-produto", "entidade-produto"], "wasDerivedFrom": [], "wasGeneratedBy": None})
    base.update(mudancas)
    return trilha.no_de_decisao(**base)


def _trilha_v2(tid: str = "fase4/qwen2.5_7b/lex-1@ao_vivo", resposta: str = RESPOSTA_V2, selo: str = "medio",
               com_gabarito: bool = False) -> "trilha.Trilha":
    """Uma trilha v2 mínima de um diagnóstico ao vivo, com os eventos que o P3 vai emitir."""
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(), ts=TS)
    s_ent = t.evento("entrada", tid, {"caso": "lex-1", "classe": 1, "nivel": 1, "texto": t.blob("REQUISIÇÃO: GET /api/produtos", "caso")},
                     "ao_vivo", ts=TS)
    s_int = t.evento("interceptacao", tid, {"metodo": "GET", "caminho": "/api/produtos", "status": 200,
                                            "corpo": t.blob('[{"id": 1, "preco_v2": 89.9}]', "corpo_http"), "arvore": t.blob("- main", "arvore")},
                     "ao_vivo", pai=s_ent, ts=TS)
    s_poda = t.evento("poda", tid, {"alvo": "corpo_http", "antes": {"chars": 30}, "depois": {"chars": 12}, "regras": ["diff_contra_contrato"],
                                    "sha": t.blob('{"preco_v2": 89.9}', "corpo_podado"),
                                    "diff": [{"campo": "preco", "esperado": "preco: numero", "recebido": "preco_v2"}]}, "ao_vivo", pai=s_int, ts=TS)
    s_cand = t.evento("candidatos", tid, {"k": 3, "itens": [{"id": "contrato-produto", "posicao": 1, "pontuacao": 21.9, "escolhido": True},
                                                            {"id": "entidade-produto", "posicao": 2, "pontuacao": 20.1, "escolhido": True}]},
                      "ao_vivo", pai=s_poda, ts=TS)
    s_prompt = t.evento("prompt", tid, {"etapa": "diagnostico", "sha": trilha.sha("prompt"), "chars": 6}, "ao_vivo", pai=s_cand, ts=TS)
    s_inf = t.evento("inferencia", tid, {"etapa": "diagnostico", "resposta": t.blob(resposta, "resposta"), "segundos": 61.1},
                     "ao_vivo", pai=s_prompt, ts=TS)
    decl = trilha.localizar_declaracoes(resposta)
    for chave, _ in trilha._CAMPOS:
        item = decl["campos"][chave]
        lido = decl["lido"]["fonte_ids"] if chave == "fonte" else decl["lido"][chave]
        dados = {"campo": chave, "ausente": True, "valor": None, "lido": lido} if item is None else {"campo": chave, "lido": lido, **item}
        t.evento("declaracao", tid, dados, "ao_vivo", pai=s_inf, ts=TS)
    for f in decl["fontes"]:
        t.evento("declaracao", tid, {"campo": "fonte_citada", **f}, "ao_vivo", pai=s_inf, ts=TS)
    verificacoes = [trilha._v("quatro_linhas_presentes", "resposta", "confere", {"ausentes": []}),
                    trilha._v("fonte_estava_no_contexto", "contrato-produto", "confere", {"contexto": ["contrato-produto", "entidade-produto"]}),
                    trilha._v("impacto", decl["lido"]["impacto"], "nao_verificavel", "sem contraparte no caso")]
    if com_gabarito:
        verificacoes.append(trilha._v("causa_correta", decl["lido"]["causa_raiz"], "confere", {"gabarito": "campo_renomeado"}, usa_gabarito=True))
    for v in verificacoes:
        t.evento("verificacao", tid, v, "ao_vivo", pai=s_inf, ts=TS)
    intervencao = {"tipo": "remocao", "verbete": "contrato-produto", "rotulo_antes": "campo_renomeado", "rotulo_depois": "tipo_incompativel",
                   "p_antes": 0.63, "p_depois": 0.31, "mudou_rotulo": True, "limite_inferior": False}
    no = _no(evidencia=[{"seq": s_poda, "papel": "sinal_em_codigo"}, {"seq": s_cand, "papel": "verbete_entregue", "id": "contrato-produto"}],
             confianca={"logprob_rotulo": -0.46, "p_rotulo": 0.63, "alternativas_top": 2, "selo": selo})
    no["justificativa"] = grr.justificativa_por_molde(no, eventos=t.eventos, verificacoes=verificacoes, intervencoes=[intervencao])
    no["contraste"] = grr.contraste_por_molde(no)
    t.decisao(tid, no, pai=s_inf, ts=TS)
    t.evento("intervencao", tid, intervencao, "ao_vivo", pai=s_inf, ts=TS)
    t.fechar(fim="2026-10-26T20:01:01")
    return t


def teste_trilha_v1_lida_pelo_leitor_v2_sem_perda():
    arq = RA / "pre_fase4" / "trilhas" / "fase3b_cruzada_qwen__qwen2.5-coder_3b__L1.jsonl"
    assert arq.exists(), f"{arq} não existe (vitrine da Pré-Fase 4)"
    linhas = [l for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()]
    t = trilha.Trilha.carregar(arq)
    assert t.versao == 1 and trilha.versao_do_arquivo(t.eventos) == 1
    assert t.linhas() == linhas, "um arquivo v1 lido pelo leitor v2 sai igual byte a byte"
    assert trilha.CAMADA_DO_TIPO_V2["decisao"] == "programa" and set(trilha.CAMADA_DO_TIPO) <= set(trilha.CAMADA_DO_TIPO_V2)
    # o escritor carregado continua numerando de onde o arquivo parou, por trilha e por arquivo
    tid = next(k for k in trilha.por_trilha(t.eventos) if "@" in k)
    passo_antes = max(e["passo"] for e in t.eventos if e["trilha"] == tid)
    s = t.evento("acao", tid, {"acao": "teste"}, "recalculado")
    assert s == len(linhas) + 1 and t.eventos[-1]["passo"] == passo_antes + 1 and t.eventos[-1]["v"] == 1
    # o escritor v1 continua recusando os tipos novos: a vitrine não muda de forma sem querer
    try:
        t.evento("decisao", tid, {}, "recalculado")
    except ValueError:
        pass
    else:
        raise AssertionError("o escritor v1 aceitou um tipo da versão 2")


def teste_trilha_v2_exige_ts_no_ao_vivo_e_cabecalho_primeiro():
    t = trilha.Trilha(versao=trilha.V2)
    assert t.versao == 2
    for ruim in (lambda: t.evento("entrada", "x", {"caso": "x"}, "ao_vivo", ts=TS),
                 lambda: t.evento("corrida", "x", {"modelo": "m"}, "registro")):
        try:
            ruim()
        except ValueError as e:
            assert "cabe" in str(e).lower() or "corrida" in str(e).lower(), e
        else:
            raise AssertionError("a trilha v2 aceitou um evento antes do cabeçalho de corrida")
    cab = _cabecalho()
    assert cab["versao_do_esquema"] == 2 and cab["limites"] == trilha.LIMITES_PADRAO and cab["fim"] is None, cab
    assert cab["num_ctx"] == 8192 and cab["temperatura"] == 0.1 and cab["modelo"] == "qwen2.5:7b", cab
    for faltando in ("modelo", "versao_ollama", "inicio"):
        try:
            trilha.cabecalho_de_corrida(**{**dict(modelo="m", versao_ollama="0.40.2", inicio=TS), faltando: ""})
        except ValueError as e:
            assert faltando in str(e), e
        else:
            raise AssertionError(f"cabeçalho aceitou {faltando} vazio")
    s0 = t.corrida(cab, ts=TS)
    assert s0 == 1 and t.eventos[0]["tipo"] == "corrida" and t.eventos[0]["origem"] == "ao_vivo" and t.eventos[0]["v"] == 2
    try:
        t.evento("entrada", "x@ao_vivo", {"caso": "x"}, "ao_vivo")
    except ValueError as e:
        assert "ts" in str(e), e
    else:
        raise AssertionError("evento ao_vivo sem ts foi aceito")
    s1 = t.evento("entrada", "x@ao_vivo", {"caso": "x"}, "ao_vivo", ts=TS)
    s2 = t.evento("interceptacao", "x@ao_vivo", {"metodo": "GET"}, "ao_vivo", pai=s1, ts=TS)
    s3 = t.evento("revisao", "x@ao_vivo", {"veredito": "certo"}, "humano", pai=s2, ts=TS)
    e = {ev["seq"]: ev for ev in t.eventos}
    assert e[s2]["camada"] == "programa" and e[s3]["camada"] == "humano" and e[s2]["ts"] == TS
    assert all(ev["v"] == 2 for ev in t.eventos)
    t.fechar(fim="2026-10-26T20:30:00")
    cab_gravado = json.loads(t.linhas()[0])["dados"]
    assert cab_gravado["fim"] == "2026-10-26T20:30:00" and cab_gravado["tamanho"]["eventos"] == len(t.eventos), cab_gravado["tamanho"]
    assert cab_gravado["tamanho"]["chars"] == sum(len(l) + 1 for l in t.linhas()), "o tamanho é o do arquivo gravado"


def teste_trilha_v2_limites_de_nos_e_blob_fora_da_linha():
    pasta = _temp()
    limites = {**trilha.LIMITES_PADRAO, "nos_por_diagnostico": 2, "nos_por_cura": 1, "blob_inline_max_chars": 20}
    t = trilha.Trilha(versao=trilha.V2, limites=limites, pasta_blobs=pasta)
    t.corrida(trilha.cabecalho_de_corrida(modelo="m", versao_ollama="0.40.2", inicio=TS, limites=limites), ts=TS)
    assert json.loads(t.linhas()[0])["dados"]["limites"]["nos_por_diagnostico"] == 2
    curto = t.blob("curto", "caso")
    longo = t.blob("x" * 50, "resposta")
    e = {ev["dados"].get("sha"): ev["dados"] for ev in t.eventos if ev["tipo"] == "blob"}
    assert e[curto]["texto"] == "curto" and "arquivo" not in e[curto]
    assert e[longo]["texto"] is None and e[longo]["chars"] == 50 and e[longo]["arquivo"].endswith(f"{longo}.txt"), e[longo]
    assert (pasta / f"{longo}.txt").read_text(encoding="utf-8") == "x" * 50
    assert trilha.blobs_de(t.eventos)[longo] is None and trilha.blobs_de(t.eventos, pasta=pasta)[longo] == "x" * 50
    try:
        trilha.Trilha(versao=trilha.V2, limites=limites).blob("y" * 50, "resposta")
    except ValueError as e:
        assert "pasta" in str(e), e
    else:
        raise AssertionError("blob acima do limite sem pasta de destino foi aceito")
    tid = "x@ao_vivo"
    t.decisao(tid, _no(decisao="recuperacao", escolha="contrato-produto", alternativas=[{"opcao": "contrato-produto", "escore": 1.0}]), ts=TS)
    t.decisao(tid, _no(), ts=TS)
    try:
        t.decisao(tid, _no(), ts=TS)
    except ValueError as e:
        assert "nos_por_diagnostico" in str(e), e
    else:
        raise AssertionError("terceiro nó de diagnóstico acima do limite foi aceito")
    t.decisao(tid, _no(decisao="cura", escolha="role+name", alternativas=[{"opcao": "role+name", "escore": 1}]), ts=TS)
    try:
        t.decisao(tid, _no(decisao="reexecucao", escolha="passou", alternativas=[{"opcao": "passou", "escore": 1}]), ts=TS)
    except ValueError as e:
        assert "nos_por_cura" in str(e), e
    else:
        raise AssertionError("nó de cura acima do limite foi aceito")


def teste_no_de_decisao_valida_campos_e_rejeita_sem_divergencia():
    no = _no()
    assert set(no) >= {"decisao", "alternativas", "escolha", "evidencia", "resultado", "contraste", "divergencia", "confianca",
                       "justificativa", "falha", "prov"}, sorted(no)
    assert no["falha"] is None and no["contraste"] is None and no["justificativa"] is None
    erros = {
        "divergencia": dict(divergencia=None),
        "decisao": dict(decisao="adivinhacao"),
        "escolha": dict(escolha="fora_das_alternativas"),
        "evidencia": dict(evidencia=[{"seq": 2, "papel": "sinal_em_codigo", "texto": "copiado"}]),
        "falha": dict(falha="falha_que_nao_existe"),
        "selo": dict(confianca={"p_rotulo": 0.5, "selo": "altissimo"}),
        "entre": dict(divergencia={"ha": True, "entre": ["modelo", "oraculo"], "detalhe": "x"}),
    }
    for palavra, mudanca in erros.items():
        try:
            _no(**mudanca)
        except ValueError as e:
            assert palavra in str(e), (palavra, e)
        else:
            raise AssertionError(f"nó com {palavra} inválido foi aceito")
    assert _no(falha="rotulo_errado")["falha"] == "rotulo_errado" and trilha.origem_da_falha("rotulo_errado") == "modelo"
    assert trilha.origem_da_falha("incidente") == "harness" and trilha.origem_da_falha("candidato_ambiguo") == "cura"
    assert _no(alternativas=[], escolha="sem_alternativas")["escolha"] == "sem_alternativas", "sem alternativas, qualquer escolha vale"
    assert _no(divergencia={"ha": True, "entre": ["modelo", "verificacao"], "detalhe": "a FONTE cita verbete fora do contexto"})["divergencia"]["ha"] is True
    assert trilha.exportar_nome_gen_ai("diagnostico") == "chat" and trilha.exportar_nome_gen_ai("cura") == "execute_tool"
    assert trilha.exportar_nome_gen_ai("poda") == "plan" and trilha.exportar_nome_gen_ai("recuperacao") == "retrieval"
    assert trilha.exportar_nome_gen_ai("reexecucao") is None, "a tabela só exporta nomes; o que não tem par fica sem"


def teste_diff_acha_o_primeiro_no_divergente_e_tolera_o_ruido():
    def corrida(escolhas: dict[str, list[tuple[str, str]]]) -> list[dict]:
        t = trilha.Trilha(versao=trilha.V2)
        t.corrida(_cabecalho(), ts=TS)
        for tid, nos in escolhas.items():
            for decisao, escolha in nos:
                t.decisao(tid, _no(decisao=decisao, escolha=escolha, alternativas=[{"opcao": escolha, "escore": 1.0}]), ts=TS)
        return t.eventos

    ref = corrida({"a": [("recuperacao", "v1"), ("diagnostico", "campo_renomeado")], "b": [("recuperacao", "v2"), ("diagnostico", "campo_ausente")]})
    igual = corrida({"a": [("recuperacao", "v1"), ("diagnostico", "campo_renomeado")], "b": [("recuperacao", "v2"), ("diagnostico", "campo_ausente")]})
    nova = corrida({"a": [("recuperacao", "v1"), ("diagnostico", "campo_renomeado")], "b": [("recuperacao", "v2"), ("diagnostico", "tipo_incompativel")],
                    "c": [("diagnostico", "x")]})
    d0 = trilha.diff_contra_referencia(igual, ref)
    assert d0["divergencias"] == [] and d0["trilhas_comparadas"] == 2 and d0["so_na_nova"] == [] and d0["so_na_referencia"] == []
    d1 = trilha.diff_contra_referencia(nova, ref)
    assert len(d1["divergencias"]) == 1 and d1["so_na_nova"] == ["c"], d1
    div = d1["divergencias"][0]
    assert div["trilha"] == "b" and div["posicao"] == 2, div
    assert div["esperado"] == {"decisao": "diagnostico", "escolha": "campo_ausente"} and div["obtido"] == {"decisao": "diagnostico", "escolha": "tipo_incompativel"}
    # a trilha mais curta diverge no primeiro nó que falta
    curta = corrida({"a": [("recuperacao", "v1")], "b": [("recuperacao", "v2"), ("diagnostico", "campo_ausente")]})
    d2 = trilha.diff_contra_referencia(curta, ref)
    assert d2["divergencias"][0]["trilha"] == "a" and d2["divergencias"][0]["posicao"] == 2 and d2["divergencias"][0]["obtido"] is None
    # uma divergência numa corrida só fica dentro do ruído declarado; repetida em duas corridas vira regressão
    r1 = trilha.regressoes(d1, anterior=None, limiar_ruido=3)
    assert r1["dentro_do_ruido"] is True and r1["regressoes"] == [] and r1["divergentes"] == 1, r1
    r2 = trilha.regressoes(d1, anterior=d1, limiar_ruido=3)
    assert [r["trilha"] for r in r2["regressoes"]] == ["b"], r2
    muitas = corrida({k: [("diagnostico", "x")] for k in "abcd"})
    ref4 = corrida({k: [("diagnostico", "y")] for k in "abcd"})
    r3 = trilha.regressoes(trilha.diff_contra_referencia(muitas, ref4), anterior=None, limiar_ruido=3)
    assert r3["dentro_do_ruido"] is False and len(r3["regressoes"]) == 4, r3


def teste_verificar_sem_gabarito_e_conferencias_da_fase4():
    import biblioteca as bib
    verbetes = bib.carregar()
    caso = {"id": "x", "classe": 1, "nivel": 1, "entrada": {"requisicao": "GET /api/produtos", "status": 200, "contrato": "preco: numero",
                                                           "corpo": '{"preco_v2": 89.9}', "sintoma": "preço vazio"}}
    ids = [v["id"] for v in verbetes[:3]]
    resposta = f"CAUSA_RAIZ: campo_renomeado\nCAMPO: preco\nIMPACTO: nada.\nFONTE: [{ids[0]}]"
    decl = trilha.localizar_declaracoes(resposta)
    registro = {"caso": "x", "resposta": resposta, "verbetes_ids": ids, "modelo": "m", "classe": 1, "nivel": 1, "estrategia": "linear",
                "segundos": 1.0, "tokens_saida": 10, "somente_cpu": True, "condicao": "A2"}
    sem = trilha.verificar(registro, caso, verbetes, decl, com_gabarito=False)
    assert sem and not any(v["usa_gabarito"] for v in sem), [v["regra"] for v in sem if v["usa_gabarito"]]
    assert [v["regra"] for v in sem][:2] == ["quatro_linhas_presentes", "rotulo_no_conjunto"]
    com = trilha.verificar({**registro, "gabarito": {"causa_raiz": "campo_renomeado", "campo_afetado": "preco"}, "verbete_ouro": ids[0]},
                           caso, verbetes, decl)
    assert [v["regra"] for v in com if v["usa_gabarito"]] == ["causa_correta", "campo_correto", "verbete_de_ouro_no_contexto"]
    assert [v for v in com if not v["usa_gabarito"]] == sem, "sem o gabarito, as outras conferências são as mesmas"
    textos = {"v-a": "O campo foi renomeado (campo_renomeado): a chave sumiu da resposta.", "v-b": "Nada a ver com a causa."}
    ok = trilha.localizar_declaracoes("CAUSA_RAIZ: campo_renomeado\nCAMPO: preco\nIMPACTO: x.\nFONTE: [v-a], [v-b]")
    extras = {v["regra"] + ":" + str(v["alvo"]): v for v in trilha.conferencias_fase4(ok, textos)}
    assert extras["fonte_formato_valido:[v-a], [v-b]"]["resultado"] == "confere", extras
    assert extras["fonte_contem_termo_da_causa:v-a"]["resultado"] == "confere" and extras["fonte_contem_termo_da_causa:v-b"]["resultado"] == "nao_confere"
    livre = trilha.localizar_declaracoes("CAUSA_RAIZ: campo_renomeado\nCAMPO: preco\nIMPACTO: x.\nFONTE: [v-a] e o manual do sistema")
    extras2 = {v["regra"]: v for v in trilha.conferencias_fase4(livre, textos)}
    assert extras2["fonte_formato_valido"]["resultado"] == "nao_confere", extras2["fonte_formato_valido"]
    nenhum = trilha.localizar_declaracoes("CAUSA_RAIZ: campo_renomeado\nCAMPO: preco\nIMPACTO: x.\nFONTE: nenhum")
    extras3 = {v["regra"]: v for v in trilha.conferencias_fase4(nenhum, textos)}
    assert extras3["fonte_formato_valido"]["resultado"] == "nao_se_aplica" and extras3["fonte_contem_termo_da_causa"]["resultado"] == "nao_se_aplica"
    assert all(v["usa_gabarito"] is False for v in trilha.conferencias_fase4(ok, textos))


# ----------------------------------------------------------------------------- P1: relatório v2 e molde

def teste_molde_nunca_cita_verbete_fora_da_evidencia_e_marca_incerteza():
    t = _trilha_v2(selo="medio")
    no = next(e["dados"] for e in t.eventos if e["tipo"] == "decisao")
    texto = no["justificativa"]
    assert "campo_renomeado" in texto and "preco" in texto and "contrato-produto" in texto, texto
    assert "entidade-produto" not in texto, "o molde só cita verbetes que estão na evidência do nó, não os de prov.used"
    assert "tipo_incompativel" in texto and "0,21" in texto, "a segunda causa e a probabilidade dela entram no contraste"
    assert "mudou a resposta" in texto and "não dá para conferir por código" in texto, texto
    assert "não está seguro" not in texto, "com selo médio a frase de incerteza não entra"
    baixo = _trilha_v2(selo="baixo")
    jb = next(e["dados"] for e in baixo.eventos if e["tipo"] == "decisao")["justificativa"]
    assert "não está seguro desta causa" in jb and "0,63" in jb and "confira o campo preco" in jb, jb
    assert grr.MARCA_DO_MOLDE == "gerada por molde"
    contraste = no["contraste"]
    assert contraste.startswith("campo_renomeado e não tipo_incompativel"), contraste
    # sem eventos, o molde ainda funciona e continua sem inventar: cita só os ids que a evidência traz
    solto = grr.justificativa_por_molde(_no())
    assert "contrato-produto" in solto and "entidade-produto" not in solto and "—" not in solto and "→" not in solto
    # um nó marcado com falha diz a falha, sem esconder
    com_falha = grr.justificativa_por_molde(_no(falha="citacao_fora_do_contexto", divergencia={"ha": True, "entre": ["modelo", "verificacao"], "detalhe": "x"}))
    assert "citacao_fora_do_contexto" in com_falha and "diverge" in com_falha, com_falha


SECOES_V2 = ["## 1. Veredito", "## 2. Evidência", "## 3. Contraste", "## 4. FONTE", "## 5. Linha de ação", "## 6. Árvore"]


def teste_relatorio_v2_secoes_na_ordem_fixa_e_valores_literais():
    t = _trilha_v2(com_gabarito=True)
    tid = next(k for k in trilha.por_trilha(t.eventos) if "@" in k)
    md = grr.relatorio_do_caso_v2(t.eventos, tid, comando_reexecucao="python executar_fase4.py --modo reproducao --caso lex-1")
    posicoes = [md.index(s) for s in SECOES_V2]
    assert posicoes == sorted(posicoes), "as seis seções vêm na ordem fixa da especificação (seção 11)"
    assert grr.MARCA_DO_MOLDE in md and "python executar_fase4.py --modo reproducao --caso lex-1" in md
    aval = md.index("### Avaliação contra o gabarito")
    assert aval > posicoes[-1], "a avaliação com gabarito vem por último, dentro da árvore"
    assert "gabarito" not in md[:aval].lower(), "o gabarito só aparece na seção de avaliação"
    assert "`campo_renomeado`" in md[:posicoes[1]] and "`preco`" in md[:posicoes[1]] and "medio" in md[:posicoes[1]].lower()
    assert "preco_v2" in md[posicoes[1]:posicoes[2]], "a evidência mostra o campo divergente do contrato ao lado do trecho podado"
    assert "tipo_incompativel" in md[posicoes[2]:posicoes[3]]
    assert "mudou a resposta" in md[posicoes[3]:posicoes[4]] or "remo" in md[posicoes[3]:posicoes[4]].lower()
    # todo valor declarado continua sendo trecho literal da resposta (o invariante da v1 vale na v2)
    blobs = trilha.blobs_de(t.eventos)
    resposta = blobs[next(e["dados"]["resposta"] for e in t.eventos if e["tipo"] == "inferencia")]
    for e in t.eventos:
        if e["tipo"] == "declaracao" and e["dados"].get("ini") is not None:
            assert resposta[e["dados"]["ini"]:e["dados"]["fim"]] == e["dados"]["valor"], e["dados"]
            assert f"`{e['dados']['valor']}`" in md, e["dados"]["valor"]
    import re as _re
    prosa = _re.sub(r"(?s)`{3,4}text\n.*?\n`{3,4}", "", md)
    assert "—" not in prosa and "→" not in prosa
    assert grr.relatorio_do_caso_v2(t.eventos, tid, comando_reexecucao="x") == grr.relatorio_do_caso_v2(t.eventos, tid, comando_reexecucao="x")
    # sem gabarito, a subseção de avaliação não existe e o relatório diz que não houve gabarito
    sem = grr.relatorio_do_caso_v2(_trilha_v2().eventos, tid)
    assert "### Avaliação contra o gabarito" not in sem and "sem gabarito" in sem.lower()
    # o carimbo de conflito aparece quando a divergência é marcada
    tc = _trilha_v2()
    no = next(e for e in tc.eventos if e["tipo"] == "decisao")
    no["dados"]["divergencia"] = {"ha": True, "entre": ["modelo", "verificacao"], "detalhe": "a FONTE cita verbete fora do contexto"}
    assert "CONFLITO" in grr.relatorio_do_caso_v2(tc.eventos, tid)[:grr.relatorio_do_caso_v2(tc.eventos, tid).index("## 2. Evidência")]


# ----------------------------------------------------------------------------- P2: restauração do banco e poda em código

# ! Alteração de IA - Revisar: testes do pacote P2 (26/10/2026), escritos antes de `restaurar_banco.py` e `poda.py`.
# ! Motivo: o plano aprovado (seção 5, P2) pede, sobre fixtures congelados e sem navegador: a poda da árvore preserva o
# alvo do passo e os papéis interativos e remove o resto, com as contagens certas; o diff do corpo contra o contrato
# acha campo ausente, renomeado, tipo diferente, corpo não JSON e truncado; `restaurar_banco.py` deixa o seed a partir
# de um banco sujo (teste de integração, pulado com aviso quando o MariaDB não responde).

def teste_restaurar_banco_deixa_o_seed_a_partir_de_um_banco_sujo():
    sys.path.insert(0, str(RAIZ))
    import _env_common as env
    import restaurar_banco as rb
    assert rb.CONTAGENS_DO_SEED == {"tbtipos": 4, "tbprodutos": 14, "tbusuarios": 2, "tbpedido_reserva": 0}
    cli = env.find_mysql_cli()
    if not cli or not env.ensure_mariadb_running(cli):
        print("  (pulado com aviso: MariaDB não disponível nesta máquina; o teste precisa do servidor portátil ou instalado)")
        return
    try:
        rb.executar_sql(cli, f"DELETE FROM {rb.BANCO}.tbprodutos;")
        assert rb.contar(cli)["tbprodutos"] == 0, "o banco sujo precisa estar sem produtos antes de restaurar"
        contagens = rb.restaurar(cli)
        assert contagens == rb.CONTAGENS_DO_SEED, contagens
        assert rb.restaurar(cli) == rb.CONTAGENS_DO_SEED, "restaurar de novo dá o mesmo seed"
    finally:
        env.stop_managed_mariadbd()


def _nos_da_pagina() -> tuple[list[dict], str]:
    d = json.loads((FIX / "arvore_produtos_api.json").read_text(encoding="utf-8"))
    return d["nos"], d["titulo"]


def _cartao_do_botao(nos: list[dict], ocorrencia: int) -> str:
    """O nome do heading de nível 3 que antecede a n-ésima ocorrência do botão "Saiba Mais..." na árvore real."""
    vistos, ultimo = 0, None
    for n in nos:
        if n["papel"] == "heading" and n["atributos"].get("level") == "3":
            ultimo = n["nome"]
        if n["papel"] == "button" and n["nome"] == "Saiba Mais...":
            vistos += 1
            if vistos == ocorrencia:
                return ultimo
    raise AssertionError(f"a árvore não tem {ocorrencia} botões 'Saiba Mais...'")


def teste_poda_arvore_preserva_alvo_e_interativos_com_contagens():
    import poda
    nos, titulo = _nos_da_pagina()
    interativos = [{"papel": "button", "nome": "Saiba Mais...", "class": "btn btn-info btn-xs saiba-mais", "data-id": str(i)} for i in range(1, 15)]
    alvo = {"papel": "button", "nome": "Saiba Mais...", "ocorrencia": 6}
    r = poda.podar_arvore(nos, titulo=titulo, alvo=alvo, interativos=interativos)
    linhas = r["texto"].splitlines()
    assert linhas[0] == f'document "{titulo}"' and r["antes"] == len(nos) == 193, (linhas[0], r["antes"])
    assert r["depois"] == len(linhas) < 70, (r["depois"], len(linhas))
    assert "  navigation" in linhas and '    link "PRODUTOS (API)"' in linhas and "  main" in linhas, linhas[:12]
    assert '    heading "Produtos via API" level=2' in linhas
    assert linhas.count("    group") == 4, "três primeiros cartões mais o cartão do alvo"
    assert f'      heading "{_cartao_do_botao(nos, 1)}" level=3' in linhas and f'      heading "{_cartao_do_botao(nos, 6)}" level=3' in linhas
    assert f'      heading "{_cartao_do_botao(nos, 5)}" level=3' not in linhas, "o quinto cartão não é dos três primeiros nem o do alvo"
    assert '      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"' in linhas, linhas
    assert '      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="6"' in linhas, linhas
    assert '      text "Carnes"' in linhas and any(l.startswith('      button "R$') for l in linhas), linhas
    assert any("cartões omitidos" in l and "10" in l for l in linhas), "a contagem dos cartões omitidos fica na árvore"
    proibidos = ("img", "iframe", "listitem", "list", "strong", "paragraph")
    assert not any(l.strip().split(" ")[0] in proibidos for l in linhas), [l for l in linhas if l.strip().split(" ")[0] in proibidos]
    assert '    textbox "Digite seu nome"' in linhas and any(l.strip().startswith('button "enviar"') for l in linhas), linhas[-12:]
    assert r["regras"]["cartoes_omitidos"] == 10 and r["regras"]["imagens_removidas"] == 16, r["regras"]
    assert poda.podar_arvore(nos, titulo=titulo, alvo=alvo, interativos=interativos)["texto"] == r["texto"], "determinística"
    r2 = poda.podar_arvore(nos, titulo=titulo)
    assert r2["texto"].count("    group") == 3 and r2["regras"]["cartoes_omitidos"] == 11, r2["regras"]
    assert poda.tokens_estimados(r["texto"]) == round(len(r["texto"]) / 2.6) and poda.cabe(r["texto"], 8192)
    assert not poda.cabe("x" * 30000, 8192)


def teste_diff_contrato_acha_ausente_renomeado_tipo_nao_json_e_truncado():
    import poda
    from banco_casos import CONTRATO_PEDIDO, CONTRATO_PRODUTO, PRODUTO_OK
    ok = poda.diff_contrato(CONTRATO_PRODUTO, f"[{PRODUTO_OK}]")
    assert ok["corpo"] == "json" and ok["forma"] == "lista" and ok["itens"] == 1 and ok["diferencas"] == [], ok
    campos = {c["campo"]: c for c in poda.campos_do_contrato(CONTRATO_PRODUTO)}
    assert campos["preco"]["tipos"] == ["numero"] and campos["resumo"]["tipos"] == ["texto", "nulo"], campos
    renomeado = poda.diff_contrato(CONTRATO_PRODUTO, PRODUTO_OK.replace('"preco"', '"preco_v2"'))
    d = {x["campo"]: x for x in renomeado["diferencas"]}
    assert d["preco"]["tipo"] == "renomeado" and d["preco"]["recebido"] == "preco_v2" and renomeado["forma"] == "objeto", renomeado
    assert "preco_v2" in renomeado["trecho"] and len(renomeado["diferencas"]) == 1, renomeado
    ausente = poda.diff_contrato(CONTRATO_PRODUTO, PRODUTO_OK.replace(', "imagem": "picanha_alho.jpg"', ""))
    assert [x["tipo"] for x in ausente["diferencas"]] == ["ausente"] and ausente["diferencas"][0]["campo"] == "imagem", ausente
    tipo = poda.diff_contrato(CONTRATO_PRODUTO, PRODUTO_OK.replace('"preco": 89.9', '"preco": "89,90"').replace('"destaque": true', '"destaque": "sim"'))
    d = {x["campo"]: x for x in tipo["diferencas"]}
    assert d["preco"]["tipo"] == "tipo_diferente" and d["preco"]["esperado"] == "numero" and d["preco"]["recebido"] == "texto", d
    assert d["destaque"]["tipo"] == "tipo_diferente" and d["destaque"]["recebido"] == "texto", d
    nulo = poda.diff_contrato(CONTRATO_PRODUTO, PRODUTO_OK.replace('"tipo": "Carnes"', '"tipo": null'))
    assert [x["tipo"] for x in nulo["diferencas"]] == ["nulo_inesperado"], nulo
    assert poda.diff_contrato(CONTRATO_PRODUTO, PRODUTO_OK.replace('"resumo": "Picanha grelhada"', '"resumo": null'))["diferencas"] == [], "resumo aceita nulo"
    extra = poda.diff_contrato(CONTRATO_PRODUTO, PRODUTO_OK.replace('"destaque": true', '"destaque": true, "preco_centavos": 8990'))
    assert [x["tipo"] for x in extra["diferencas"]] == ["inesperado"] and extra["diferencas"][0]["campo"] == "preco_centavos", extra
    pedido_ok = '{"id_pedido": 1, "pessoas": 4, "data_pedido": "2026-10-26", "status": "Em Analise", "nome": "Ana", "cpf": "123"}'
    assert poda.diff_contrato(CONTRATO_PEDIDO, pedido_ok)["diferencas"] == []
    dominio = poda.diff_contrato(CONTRATO_PEDIDO, pedido_ok.replace("Em Analise", "Pendente").replace("2026-10-26", "26/10/2026"))
    d = {x["campo"]: x for x in dominio["diferencas"]}
    assert d["status"]["tipo"] == "fora_do_dominio" and d["data_pedido"]["tipo"] == "formato_divergente", d
    for corpo, esperado in (("", "vazio"), ("<html><body>Erro</body></html>", "nao_json"), ('[{"id": 1, "nome": "Picanha ao Alho", "tipo": "Carnes", "preco": 89.9', "truncado")):
        r = poda.diff_contrato(CONTRATO_PRODUTO, corpo)
        assert r["corpo"] == esperado and r["diferencas"] == [] and r["forma"] is None, (corpo[:20], r)
    assert "html" in poda.diff_contrato(CONTRATO_PRODUTO, "<html><body>Erro</body></html>")["trecho"]
    objeto = poda.diff_contrato(CONTRATO_PRODUTO, f"[{PRODUTO_OK}]", forma_esperada="objeto")
    assert [x["tipo"] for x in objeto["diferencas"]] == ["forma_diferente"] and objeto["diferencas"][0]["recebido"] == "lista", objeto
    assert poda.diff_contrato(CONTRATO_PRODUTO, "[]")["itens"] == 0


# ----------------------------------------------------------------------------- P2: interceptador, HAR e caso ao vivo

MODOS_DE_FALHA = ("error_500", "latency", "type_drift", "field_missing", "field_renamed", "malformed_json")


def teste_interceptador_decide_hosts_e_monta_a_aresta_http():
    import interceptador as ic
    assert ic.host_de("http://localhost:8000/api/produtos?x=1") == "localhost:8000"
    assert ic.host_de("https://code.jquery.com/jquery.min.js") == "code.jquery.com"
    assert ic.permitido("http://localhost:8000/api/produtos") == "permitido"
    assert ic.permitido("http://127.0.0.1:8080/produtos_api.php") == "permitido"
    assert ic.permitido("https://code.jquery.com/jquery.min.js", hosts_har=("code.jquery.com",)) == "har"
    assert ic.permitido("https://code.jquery.com/jquery.min.js") == "bloqueado"
    assert ic.permitido("https://smtp.exemplo.com/enviar") == "bloqueado"
    assert ic.permitido("https://maps.googleapis.com/maps/api/js") == "silencioso", "o mapa do rodapé é bloqueado sem incidente"
    assert ic.permitido("https://www.google.com/maps/embed", hosts_har=("www.google.com",)) == "silencioso", "silencioso vence o HAR"
    aresta = ic.aresta_http("http://localhost:8080/produtos_api.php", "GET", "http://localhost:8000/api/produtos")
    assert aresta == {"tipo": "chamada_http", "de": "produtos_api.php", "para": "GET /api/produtos", "host": "localhost:8000"}, aresta
    assert ic.aresta_http("http://localhost:8080/produtos_api.php?x=1", "GET", "http://localhost:8000/api/produtos/3")["para"] == "GET /api/produtos/3"
    assert ic.aresta_http("http://localhost:8080/", "POST", "http://localhost:8000/api/pedidos")["de"] == "index"
    registro = ic.registro_http("GET", "http://localhost:8000/api/produtos?pagina=2", 200, {"content-type": "application/json", "content-length": "17"},
                                '[{"id": 1}]', inicio_ms=100.0, fim_ms=161.5, tipo_recurso="fetch")
    assert registro["caminho"] == "/api/produtos" and registro["consulta"] == "pagina=2" and registro["host"] == "localhost:8000", registro
    assert registro["status"] == 200 and registro["content_type"] == "application/json" and registro["tempo_ms"] == 61.5, registro
    assert registro["corpo_sha"] == trilha.sha('[{"id": 1}]') and registro["corpo_chars"] == 11 and registro["tipo_recurso"] == "fetch", registro
    assert "corpo" not in registro, "o corpo inteiro vai para o blob da trilha, não para o registro"
    assert ic.CDN_PADRAO and all("." in h for h in ic.CDN_PADRAO)


def _cobaias_no_ar() -> bool:
    import socket
    for porta in (8080, 8000):
        try:
            with socket.create_connection(("localhost", porta), timeout=1):
                pass
        except OSError:
            return False
    return True


def teste_interceptador_ao_vivo_captura_a_chamada_do_catalogo():
    """Integração: precisa das cobaias no ar (python run.py em outro terminal). Pulado com aviso quando não respondem."""
    if not _cobaias_no_ar():
        print("  (pulado com aviso: as cobaias não estão no ar nas portas 8080 e 8000; suba com `python run.py` para rodar este teste)")
        return
    import interceptador as ic
    with navegador.Navegador() as nav:
        pagina = nav.nova_pagina()
        inter = ic.Interceptador(pagina)
        pagina.goto("http://localhost:8080/produtos_api.php", wait_until="load")
        pagina.wait_for_selector("#produtos-api-grid .saiba-mais", state="visible", timeout=30000)
        captura = inter.capturar()
        chamadas = inter.registros()
    catalogo = [r for r in chamadas if r["caminho"] == "/api/produtos" and r["metodo"] == "GET"]
    assert len(catalogo) == 1 and catalogo[0]["status"] == 200, chamadas
    assert catalogo[0]["aresta"] == {"tipo": "chamada_http", "de": "produtos_api.php", "para": "GET /api/produtos", "host": "localhost:8000"}
    corpo = inter.corpo(catalogo[0]["corpo_sha"])
    assert corpo and trilha.sha(corpo) == catalogo[0]["corpo_sha"] and json.loads(corpo)[0]["id"] == 1, corpo[:80]
    assert captura["contagem"] > 100 and any(n["papel"] == "button" and n["nome"] == "Saiba Mais..." for n in captura["nos"])
    botoes = [i for i in captura["interativos"] if i["papel"] == "button" and i["nome"] == "Saiba Mais..."]
    assert len(botoes) == 14 and botoes[0]["data-id"] and "saiba-mais" in botoes[0]["class"], botoes[:2]
    assert all(ic.host_de(b["url"]) not in ("localhost:8080", "localhost:8000") for b in inter.bloqueados), inter.bloqueados[:3]


def teste_har_das_cdns_existe_e_cobre_os_hosts():
    import interceptador as ic
    har = FIX / "cdn.har"
    if not har.exists():
        print("  (pulado com aviso: fixtures_fase4/cdn.har ainda não foi gravado; rode `python interceptador.py --gravar-har`)")
        return
    dados = json.loads(har.read_text(encoding="utf-8"))
    hosts = {ic.host_de(e["request"]["url"]) for e in dados["log"]["entries"]}
    assert hosts and hosts <= set(ic.CDN_PADRAO), sorted(hosts - set(ic.CDN_PADRAO))
    assert all(ic.host_de(e["request"]["url"]) not in ("localhost:8080", "localhost:8000") for e in dados["log"]["entries"])


OPENAPI_DE_TESTE = {"components": {"schemas": {"ProdutoOut": {
    "properties": {"id": {"type": "integer", "title": "Id"}, "nome": {"type": "string", "title": "Nome"},
                   "resumo": {"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Resumo"},
                   "tipo": {"type": "string", "title": "Tipo"}, "preco": {"type": "number", "title": "Preco"},
                   "imagem": {"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Imagem"},
                   "destaque": {"type": "boolean", "title": "Destaque"}},
    "required": ["id", "nome", "tipo", "preco", "destaque"], "title": "ProdutoOut", "type": "object"}}}}


# ! Alteração de IA - Revisar: (01/11/2026, ficha 37 opção a) o caso ao vivo passa a comparar o corpo com a referência em
# modo normal: itens a menos ou a mais, repetidos, valores diferentes item a item e o tempo da chamada; quando a poda não
# acha diferença de campo contra o contrato, o CORPO deixa de ser o primeiro item normal e diz a forma, a contagem e o
# que mudou; o SINTOMA recebe as mesmas frases.
# ! Motivo: na corrida 18 (roadmap §2.10) 22 casos foram ao modelo com o primeiro produto normal no CORPO e 11 viraram
# colecao_no_lugar_de_objeto; nas falhas de lista e de latência o caso ao vivo dizia "Nenhuma diferença medida".
def teste_caso_ao_vivo_diff_contra_referencia_no_corpo_e_no_sintoma():
    import caso_ao_vivo as cv
    import poda
    ref = [{"id": i, "nome": f"Produto {i}", "preco": 10.0 + i, "tipo": "Carnes"} for i in range(1, 15)]
    ref[12]["nome"] = "Hamburguer Artesanal"
    contrato = "id: inteiro | nome: texto | preco: numero | tipo: texto"

    def js(x):
        return json.dumps(x, ensure_ascii=False)

    # 13 itens: falta o id 13
    menos = [x for x in ref if x["id"] != 13]
    d = cv.diff_referencia(js(ref), js(menos), 20.0, 25.0, orcamento_ms=1000)
    assert d["forma"] == "lista" and d["itens"] == 13 and d["itens_ref"] == 14 and d["faltam"] == [13] and d["sobram"] == [], d
    assert d["duplicados"] == [] and d["valores"] == [] and d["lento"] is False and d["igual"] is False
    frases = cv.frases_da_referencia(d)
    assert frases == ['A lista veio com 13 itens; a referência em modo normal tem 14: falta o id 13 ("Hamburguer Artesanal").'], frases
    diff = poda.diff_contrato(contrato, js(menos), forma_esperada="lista")
    assert diff["diferencas"] == []
    corpo = cv.corpo_do_caso(diff, d)
    assert corpo.startswith('lista com 13 itens (referência em modo normal: 14); falta o id 13 ("Hamburguer Artesanal")') and '"id": 1,' in corpo, corpo
    sint = cv.sintoma_por_molde(None, diff, None, status=200, diff_ref=d)
    assert "falta o id 13" in sint and "Nenhuma diferença" not in sint, sint
    # repetido: o id 5 duas vezes
    dup = ref[:5] + [ref[4]] + ref[5:]
    d2 = cv.diff_referencia(js(ref), js(dup), 20.0, 30.0)
    assert d2["itens"] == 15 and d2["duplicados"] == [{"id": 5, "vezes": 2}] and d2["faltam"] == [] and d2["sobram"] == [], d2
    assert cv.frases_da_referencia(d2) == ['A lista veio com 15 itens; a referência em modo normal tem 14: o id 5 ("Produto 5") aparece 2 vezes.']
    assert "aparece 2 vezes" in cv.corpo_do_caso(poda.diff_contrato(contrato, js(dup), forma_esperada="lista"), d2)
    # valores: nome com acento estragado em 2 itens e preco em centavos em todos
    val = [dict(x) for x in ref]
    val[0]["nome"], val[1]["nome"] = "PÃ£o", "Ã\u0081gua"
    for x in val:
        x["preco"] = x["preco"] * 100
    d3 = cv.diff_referencia(js(ref), js(val), 20.0, 30.0)
    assert {v["campo"] for v in d3["valores"]} == {"nome", "preco"} and sum(1 for v in d3["valores"] if v["campo"] == "preco") == 14
    assert d3["valores"][0] == {"id": 1, "campo": "nome", "referencia": '"Produto 1"', "recebido": '"PÃ£o"'}, d3["valores"][0]
    f3 = cv.frases_da_referencia(d3)
    assert f3 == ['O campo nome veio diferente da referência em modo normal em 2 itens, por exemplo no id 1: "PÃ£o" em vez de "Produto 1".',
                  "O campo preco veio diferente da referência em modo normal em 14 itens, por exemplo no id 1: 1100.0 em vez de 11.0."], f3
    corpo3 = cv.corpo_do_caso(poda.diff_contrato(contrato, js(val), forma_esperada="lista"), d3)
    assert corpo3.startswith("lista com 14 itens (referência em modo normal: 14); nome diferente em 2 itens; preco diferente em 14 itens") and "PÃ£o" in corpo3, corpo3
    # latência: corpo igual, chamada lenta
    d4 = cv.diff_referencia(js(ref), js(ref), 20.0, 28000.0, orcamento_ms=1000)
    assert d4["igual"] is True and d4["lento"] is True and d4["tempo_ms"] == 28000.0 and d4["tempo_ref_ms"] == 20.0
    assert cv.frases_da_referencia(d4) == ["A chamada levou 28,0 s; na referência em modo normal, 20 ms."]
    corpo4 = cv.corpo_do_caso(poda.diff_contrato(contrato, js(ref), forma_esperada="lista"), d4)
    assert corpo4.startswith("lista com 14 itens, igual à referência em modo normal; primeiro item: {") and '"Produto 1"' in corpo4, corpo4
    assert cv.sintoma_por_molde(None, poda.diff_contrato(contrato, js(ref), forma_esperada="lista"), None, status=200, diff_ref=d4).startswith("A chamada levou 28,0 s")
    # sem referência, corpo que não é JSON, ou diferença de campo contra o contrato: o CORPO fica como era
    assert cv.diff_referencia(None, js(ref), None, 10.0) is None and cv.diff_referencia(js(ref), "...[{", 20.0, 10.0) is None
    diff_campo = poda.diff_contrato(contrato, js([{**ref[0], "preco": "89.9"}]), forma_esperada="lista")
    d_campo = cv.diff_referencia(js(ref[:1]), js([{**ref[0], "preco": "89.9"}]), 20.0, 30.0)
    assert cv.corpo_do_caso(diff_campo, d_campo) == diff_campo["trecho"]
    sint_campo = cv.sintoma_por_molde(None, diff_campo, None, status=200, diff_ref=d_campo)
    assert "veio como texto em vez de numero" in sint_campo and "diferente da referência" not in sint_campo, sint_campo
    assert cv.corpo_do_caso(diff, None) == diff["trecho"]
    truncado = poda.diff_contrato(contrato, "[{\"id\": 1", forma_esperada="lista")
    assert cv.corpo_do_caso(truncado, None) == truncado["trecho"]
    # objeto (detalhe): campo a campo
    d5 = cv.diff_referencia(js(ref[0]), js({**ref[0], "preco": 1100.0}), 20.0, 30.0)
    assert d5["forma"] == "objeto" and d5["valores"] == [{"id": None, "campo": "preco", "referencia": "11.0", "recebido": "1100.0"}], d5
    assert cv.frases_da_referencia(d5) == ["O campo preco veio 1100.0; na referência em modo normal, 11.0."]
    corpo5 = cv.corpo_do_caso(poda.diff_contrato(contrato, js({**ref[0], "preco": 1100.0}), forma_esperada="objeto"), d5)
    assert corpo5.endswith("(contra a referência em modo normal: preco 1100.0 em vez de 11.0)"), corpo5
    # as linhas do evento de poda: um sinal em código por diferença, com esperado e recebido
    linhas = cv.linhas_diff_da_referencia(d)
    assert linhas == [{"campo": "itens", "tipo": "itens_a_menos", "esperado": "14 itens (referência em modo normal)", "recebido": 'falta o id 13 ("Hamburguer Artesanal")'}], linhas
    assert [l["tipo"] for l in cv.linhas_diff_da_referencia(d3)] == ["valor_diferente_da_referencia", "valor_diferente_da_referencia"]
    assert cv.linhas_diff_da_referencia(d4) == [{"campo": "tempo_ms", "tipo": "tempo_acima_do_orcamento", "esperado": "20 ms (referência em modo normal)", "recebido": "28000 ms"}]
    assert cv.linhas_diff_da_referencia(None) == []


def teste_caso_ao_vivo_contrato_sintoma_e_chaves():
    import caso_ao_vivo as cv
    import poda
    import taxonomia
    from banco_casos import CASOS, CONTRATO_PRODUTO, PRODUTO_OK
    assert cv.contrato_do_openapi(OPENAPI_DE_TESTE, "ProdutoOut") == CONTRATO_PRODUTO
    pedido = {"components": {"schemas": {"PedidoOut": {"properties": {
        "data_pedido": {"type": "string", "format": "date", "title": "Data"},
        "status": {"type": "string", "enum": ["Em Analise", "Cancelado"], "title": "Status"}}, "required": ["data_pedido", "status"]}}}}
    assert cv.contrato_do_openapi(pedido, "PedidoOut") == "data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado')"
    real = FIX / "openapi.json"
    if real.exists():
        openapi_real = json.loads(real.read_text(encoding="utf-8"))
        assert openapi_real["components"]["schemas"]["ProdutoOut"]["properties"]["preco"].get("type") == "string", "o OpenAPI declara o Decimal como texto"
        assert cv.contrato_do_openapi(openapi_real, "ProdutoOut", cv.AJUSTES_PRODUTO) == CONTRATO_PRODUTO
        assert "preco: texto" in cv.contrato_do_openapi(openapi_real, "ProdutoOut")
        assert "x-alteracao-de-ia" in openapi_real and "x-motivo" in openapi_real, "a fixture leva a tag de IA nas chaves x-"
        assert cv.anotar_openapi({"openapi": "3.1.0"})["x-motivo"].startswith("! Motivo")
    else:
        print("  (aviso: fixtures_fase4/openapi.json ainda não foi gravado; a conferência contra o OpenAPI real fica para a próxima rodada)")
    diff = poda.diff_contrato(CONTRATO_PRODUTO, PRODUTO_OK.replace('"preco"', '"preco_v2"'))
    conferencia = {"nome": "grid com 14 cartões", "esperado": "14 cartões com preço", "observado": "14 cartões com preço vazio"}
    arvore = cv.diff_arvore('document "x"\n  main\n    group\n      text "R$ 89,90"\n', 'document "x"\n  main\n    group\n      text "undefined"\n')
    assert arvore["a_menos"] == 1 and arvore["a_mais"] == 1 and arvore["faltam"] == ['text "R$ 89,90"'] and arvore["sobram"] == ['text "undefined"'], arvore
    sintoma = cv.sintoma_por_molde(conferencia, diff, arvore, status=200)
    assert sintoma == cv.sintoma_por_molde(conferencia, diff, arvore, status=200), "determinístico"
    assert "preco_v2" in sintoma and "14 cartões" in sintoma and "R$ 89,90" in sintoma, sintoma
    texto = sintoma.lower()
    for proibido in list(taxonomia.CAUSAS_RAIZ) + list(MODOS_DE_FALHA):
        assert proibido not in texto, (proibido, sintoma)
    assert "—" not in sintoma and "→" not in sintoma
    assert "HTTP 500" in cv.sintoma_por_molde(None, poda.diff_contrato(CONTRATO_PRODUTO, "Internal Server Error"), None, status=500)
    assert "vazia" in cv.sintoma_por_molde(None, poda.diff_contrato(CONTRATO_PRODUTO, ""), None, status=200)
    assert "cortada" in cv.sintoma_por_molde(None, poda.diff_contrato(CONTRATO_PRODUTO, '[{"id": 1, "nome": "P'), None, status=200)
    caso = cv.montar_caso("ao-vivo-1", "GET /api/produtos", 200, CONTRATO_PRODUTO, diff["trecho"], sintoma,
                          arvore='document "x"\n  main\n', observacao="poda: 193 nós antes, 40 depois")
    assert set(caso) == {"id", "entrada", "origem"} and caso["id"] == "ao-vivo-1" and caso["origem"] == "ao_vivo"
    chaves_gravadas = set().union(*(c["entrada"].keys() for c in CASOS))
    assert set(caso["entrada"]) <= chaves_gravadas and set(cv.OBRIGATORIAS) <= set(caso["entrada"]), (sorted(caso["entrada"]), sorted(chaves_gravadas))
    assert "gabarito" not in caso and caso["entrada"]["corpo"] == diff["trecho"] and caso["entrada"]["sintoma"] == sintoma
    import estrategias
    prompt = estrategias.linear_com_biblioteca(caso, "") if hasattr(estrategias, "linear_com_biblioteca") else estrategias._dados_do_caso(caso)
    assert "REQUISIÇÃO: GET /api/produtos" in prompt and "SINTOMA OBSERVADO" in prompt and "ÁRVORE DE ACESSIBILIDADE" in prompt
    try:
        cv.montar_caso("x", "GET /x", 200, CONTRATO_PRODUTO, "{}", "")
    except ValueError as e:
        assert "sintoma" in str(e), e
    else:
        raise AssertionError("caso sem sintoma foi aceito")


# ----------------------------------------------------------------------------- P2: cenários, cronômetro e critério

def teste_catalogo_de_cenarios_e_conferencias_puras():
    import cenarios_fase4 as cen
    assert cen.validar_catalogo(cen.CENARIOS) == [], cen.validar_catalogo(cen.CENARIOS)
    ids = [c["id"] for c in cen.CENARIOS]
    assert len(ids) == len(set(ids)) and "api-catalogo" in ids and "api-detalhe" in ids, ids
    assert {"front-busca", "front-admin-login", "front-admin-produtos", "front-cliente-reserva"} <= set(ids), ids
    assert all(cen.cenario(i)["cobaia"] == "front" for i in ids if i.startswith("front-"))
    assert cen.cenario("front-cliente-reserva").get("restaura_banco") is True, "a reserva grava no banco: o executor restaura antes"
    import datetime as _dt
    assert cen.valor_do_passo({"valor": "{hoje+3}"}, hoje=_dt.date(2026, 10, 26)) == "2026-10-29"
    assert cen.valor_do_passo({"valor": "Picanha"}) == "Picanha"
    catalogo = cen.cenario("api-catalogo")
    assert catalogo["cobaia"] == "api" and catalogo["requisicao"] == "GET /api/produtos" and catalogo["esquema"] == "ProdutoOut"
    assert [p["acao"] for p in catalogo["passos"]][0] == "abrir" and any(p["acao"] == "conferir" for p in catalogo["passos"])
    assert cen.cenario("api-detalhe")["requisicao"] == "GET /api/produtos/{id}"
    ruim = [{"id": "x", "cobaia": "nave", "pagina": "x.php", "passos": [{"acao": "voar"}]}, {"id": "x", "cobaia": "api", "pagina": "y.php", "passos": []}]
    erros = cen.validar_catalogo(ruim)
    assert any("cobaia" in e for e in erros) and any("voar" in e for e in erros) and any("repetido" in e for e in erros) and any("conferir" in e for e in erros), erros
    c = cen.conferir({"acao": "conferir", "nome": "grid com 14 cartões", "tipo": "contagem", "esperado": 14}, 13)
    assert c == {"nome": "grid com 14 cartões", "passou": False, "esperado": "14 elementos", "observado": "13 elementos"}, c
    assert cen.conferir({"acao": "conferir", "nome": "n", "tipo": "contagem", "esperado": 14}, 14)["passou"] is True
    t = cen.conferir({"acao": "conferir", "nome": "preço", "tipo": "texto", "padrao": r"^R\$ \d+,\d{2}$"}, "R$ 89,90")
    assert t["passou"] is True and t["observado"] == "R$ 89,90", t
    t2 = cen.conferir({"acao": "conferir", "nome": "preço", "tipo": "texto", "padrao": r"^R\$ \d+,\d{2}$"}, "R$ undefined")
    assert t2["passou"] is False and "R$ undefined" in t2["observado"] and "R\\$" in t2["esperado"], t2
    assert cen.conferir({"acao": "conferir", "nome": "v", "tipo": "visivel"}, True)["passou"] and not cen.conferir({"acao": "conferir", "nome": "v", "tipo": "visivel"}, False)["passou"]
    assert cen.mttr_segundos("2026-10-26T20:00:00", "2026-10-26T20:02:30") == 150.0
    assert cen.task_success({"passou": True, "conferencias": [{"passou": True}]}) is True
    assert cen.task_success({"passou": False, "conferencias": [{"passou": False}]}) is False
    assert cen.CENARIOS_DA_FASE_5 and all(cen.cenario(i) for i in cen.CENARIOS_DA_FASE_5)
    import taxonomia
    cobertas = set(cen.MODO_POR_CAUSA) | set(cen.CAUSAS_PELO_HARNESS) | set(cen.CAUSAS_SEM_MODO)
    assert cobertas == set(taxonomia.CAUSAS_RAIZ), sorted(set(taxonomia.CAUSAS_RAIZ) ^ cobertas)
    assert len(cen.MODO_POR_CAUSA) == 20 and len(set(cen.MODO_POR_CAUSA.values())) == 20
    assert set(cen.MODOS_COM_CAMPO) <= set(cen.MODO_POR_CAUSA.values())


def teste_cenarios_da_api_rodam_com_as_cobaias_no_ar():
    """Integração: catálogo e detalhe em produtos_api.php, sem modelo. Pulado com aviso quando as cobaias não respondem."""
    if not _cobaias_no_ar():
        print("  (pulado com aviso: as cobaias não estão no ar nas portas 8080 e 8000)")
        return
    import cenarios_fase4 as cen
    import interceptador as ic
    with navegador.Navegador() as nav:
        for id_ in ("api-catalogo", "api-detalhe"):
            pagina = nav.nova_pagina()
            inter = ic.Interceptador(pagina)
            r = cen.rodar_cenario(cen.cenario(id_), pagina, inter)
            pagina.close()
            assert r["passou"] is True and r["passo_falho"] is None and r["conferencia_falha"] is None, (id_, r.get("conferencia_falha"), r.get("erro"))
            assert len(r["capturas"]) == len(cen.cenario(id_)["passos"]) and all(c["contagem"] > 50 for c in r["capturas"]), id_
            assert r["segundos"] > 0 and len(r["tempos_ms"]) == len(cen.cenario(id_)["passos"]), r["tempos_ms"]
            caminhos_http = [c["caminho"] for c in r["chamadas"]]
            assert "/api/produtos" in caminhos_http, (id_, caminhos_http)
            if id_ == "api-detalhe":
                assert any(c.startswith("/api/produtos/") and c != "/api/produtos" for c in caminhos_http), caminhos_http
                assert r["chamadas"][-1]["aresta"]["de"] == "produtos_api.php"
            assert all(c["passou"] for c in r["conferencias"]), r["conferencias"]


def teste_cenarios_do_front_rodam_com_as_cobaias_no_ar():
    """Integração: busca, login do administrador, lista de produtos e reserva do cliente no front legado. Restaura o
    banco antes da reserva e no fim. Pulado com aviso quando as cobaias não respondem."""
    if not _cobaias_no_ar():
        print("  (pulado com aviso: as cobaias não estão no ar nas portas 8080 e 8000)")
        return
    sys.path.insert(0, str(RAIZ))
    import cenarios_fase4 as cen
    import interceptador as ic
    import restaurar_banco as rb
    cli = rb.env.find_mysql_cli()
    assert cli and rb.restaurar(cli) == rb.CONTAGENS_DO_SEED, "o banco precisa estar no seed antes da reserva"
    try:
        with navegador.Navegador() as nav:
            for id_ in ("front-busca", "front-admin-login", "front-admin-produtos", "front-cliente-reserva"):
                pagina = nav.nova_pagina()
                inter = ic.Interceptador(pagina)
                r = cen.rodar_cenario(cen.cenario(id_), pagina, inter)
                pagina.close()
                assert r["passou"] is True, (id_, r.get("conferencia_falha"), r.get("erro"), [c for c in r["conferencias"] if not c["passou"]])
                assert len(r["capturas"]) == len(cen.cenario(id_)["passos"]) and r["segundos"] > 0, id_
                assert not [b for b in inter.bloqueados if b["decisao"] == "bloqueado"], (id_, inter.incidentes[:3])
        assert rb.contar(cli)["tbpedido_reserva"] == 1, "a reserva do cliente gravou uma linha"
    finally:
        rb.restaurar(cli)
    assert rb.contar(cli)["tbpedido_reserva"] == 0


# ----------------------------------------------------------------------------- P2: corrida 17 (reprodução na tela, sem modelo)

def _casos_sinteticos() -> list[dict]:
    def caso(i, classe, nivel, requisicao, status, causa, campo):
        return {"id": i, "classe": classe, "nivel": nivel, "entrada": {"requisicao": requisicao, "status": status, "contrato": "x", "corpo": "", "sintoma": "s"},
                "gabarito": {"causa_raiz": causa, "campo_afetado": campo, "termos_esperados": [], "termos_proibidos": []}}
    return [caso("a", 2, 1, "GET /api/produtos", 200, "campo_renomeado", "preco"),
            caso("b", 5, 1, "GET /api/pedidos?login=11122233344", 500, "erro_interno_do_servidor", None),
            caso("c", 5, 3, "GET /api/produtos/3", 200, "dado_desatualizado", "preco"),
            caso("d", 6, 1, "GET /api/produtos", 200, "localizador_quebrado", None),
            caso("e", 1, 1, "GET /api/produtos/7", 200, "resposta_truncada", None),
            caso("f", 3, 2, "POST /api/pedidos", 201, "tipo_divergente", "pessoas")]


def teste_executar_fase4_seleciona_os_casos_e_monta_o_modo():
    import executar_fase4 as ex
    sel = ex.selecionar_casos(_casos_sinteticos())
    assert [s["id"] for s in sel["reproduziveis"]] == ["a", "e"], sel
    a, e = sel["reproduziveis"]
    assert a["modo"] == "field_renamed" and a["campo"] == "preco" and a["cenario"] == "api-catalogo" and a["produto_id"] is None, a
    assert e["modo"] == "malformed_json" and e["campo"] is None and e["cenario"] == "api-detalhe" and e["produto_id"] == 7, e
    motivos = {s["id"]: s["motivo"] for s in sel["fora"]}
    assert set(motivos) == {"b", "c", "d", "f"}, motivos
    assert "sem tela" in motivos["b"] and "sem tela" in motivos["f"], motivos
    assert "sem modo" in motivos["c"] and "harness" in motivos["d"], motivos
    assert ex.corpo_admin("field_renamed", "preco") == {"mode": "field_renamed", "target_field": "preco", "probability": 1.0}
    assert ex.corpo_admin("corpo_vazio", None) == {"mode": "corpo_vazio", "target_field": None, "probability": 1.0}
    assert ex.corpo_admin("normal", "preco")["target_field"] is None, "voltar ao normal não leva campo"
    ok = {"passou": True, "conferencia_falha": None}
    sem = {"corpo": "json", "diferencas": [], "forma": "lista"}
    igual = {"corpo_igual": True, "arvore": {"a_menos": 0, "a_mais": 0, "faltam": [], "sobram": []}}
    assert ex.reproduz(ok, sem, {"status": 200, "tempo_ms": 120.0}, igual)["reproduz"] is False
    r = ex.reproduz({"passou": False, "conferencia_falha": {"nome": "grid com 14 cartões"}}, sem, {"status": 200, "tempo_ms": 120.0}, igual)
    assert r["reproduz"] is True and "confer" in r["motivo"], r
    r = ex.reproduz(ok, {"corpo": "json", "diferencas": [{"campo": "preco", "tipo": "renomeado"}], "forma": "lista"}, {"status": 200, "tempo_ms": 10.0}, igual)
    assert r["reproduz"] is True and "contrato" in r["motivo"], r
    assert ex.reproduz(ok, sem, {"status": 429, "tempo_ms": 10.0}, igual)["reproduz"] is True
    r = ex.reproduz(ok, sem, {"status": 200, "tempo_ms": 2100.0}, igual)
    assert r["reproduz"] is True and "tempo" in r["motivo"], r
    assert ex.reproduz(ok, {"corpo": "vazio", "diferencas": [], "forma": None}, {"status": 200, "tempo_ms": 10.0}, igual)["reproduz"] is True
    r = ex.reproduz(ok, sem, None, igual)
    assert r["reproduz"] is False and "nenhuma chamada" in r["motivo"], r
    # mutação que o contrato não vê (acento estragado, preço em centavos, tipo girado): o corpo difere da referência
    r = ex.reproduz(ok, sem, {"status": 200, "tempo_ms": 10.0}, {**igual, "corpo_igual": False})
    assert r["reproduz"] is True and "referência" in r["motivo"], r
    r = ex.reproduz(ok, sem, {"status": 200, "tempo_ms": 10.0}, {"corpo_igual": True, "arvore": {"a_menos": 1, "a_mais": 1, "faltam": ["x"], "sobram": ["y"]}})
    assert r["reproduz"] is True and "árvore" in r["motivo"], r
    assert ex.reproduz(ok, sem, {"status": 200, "tempo_ms": 10.0}, None)["reproduz"] is False, "sem referência, só o contrato e o roteiro decidem"
    assert ex.ORCAMENTO_DE_TEMPO_MS == 1000
    chamadas = [{"metodo": "GET", "caminho": "/api/produtos", "status": 200}, {"metodo": "GET", "caminho": "/api/produtos/7", "status": 200}]
    assert ex.chamada_do_caso(chamadas, "api-detalhe", 7) == (chamadas[1], True)
    assert ex.chamada_do_caso(chamadas, "api-catalogo", None) == (chamadas[0], True)
    assert ex.chamada_do_caso(chamadas[:1], "api-detalhe", 7) == (chamadas[0], False), "sem a chamada do detalhe, vale a última do roteiro"
    assert ex.chamada_do_caso([], "api-catalogo", None) == (None, False)


# ! Alteração de IA - Revisar: teste novo (27/10/2026) da opção `--banco` do executor: `casos_de_avaliacao` lê os 72
# de avaliação (padrão), só os 36 inéditos da ficha 27 ou os 108; a seleção dos inéditos deixa 25 na tela e 11 fora
# (os quatro de pedidos sem página, o `dado_desatualizado` sem modo e os seis de efeito, armados pelo harness).
# ! Motivo: a corrida 17 só leu os 72 casos; para medir na tela os 36 inéditos antes da conferência do Eric, o
# executor precisa escolher o banco pela linha de comando sem mudar o padrão das corridas já feitas.
def teste_executar_fase4_le_o_banco_pedido():
    import executar_fase4 as ex
    assert ex.BANCOS == ("avaliacao", "ineditos_fase4", "todos")
    avaliacao = ex.casos_de_avaliacao()
    assert len(avaliacao) == 72 and ex.casos_de_avaliacao("avaliacao") == avaliacao
    ineditos = ex.casos_de_avaliacao("ineditos_fase4")
    assert len(ineditos) == 36, len(ineditos)
    assert all(22 <= int(c["id"].split("-")[1]) <= 27 for c in ineditos), [c["id"] for c in ineditos]
    todos = ex.casos_de_avaliacao("todos")
    assert len(todos) == 108 and len({c["id"] for c in todos}) == 108
    try:
        ex.casos_de_avaliacao("outro")
        raise AssertionError("banco desconhecido devia ser recusado")
    except ValueError:
        pass
    sel = ex.selecionar_casos(ineditos)
    assert len(sel["reproduziveis"]) == 25, [s["id"] for s in sel["reproduziveis"]]
    fora = {s["id"]: s["motivo"] for s in sel["fora"]}
    assert set(fora) == {"lex-27", "semt-25", "tra-23", "run-26", "run-27",
                         "efe-22", "efe-23", "efe-24", "efe-25", "efe-26", "efe-27"}, fora
    assert "sem tela" in fora["lex-27"] and "sem modo" in fora["run-26"] and "harness" in fora["efe-26"], fora
    ap = ex.montar_parser()
    assert ap.parse_args(["--modo", "reproducao", "--saida", "x"]).banco == "avaliacao"
    assert ap.parse_args(["--modo", "reproducao", "--saida", "x", "--banco", "ineditos_fase4"]).banco == "ineditos_fase4"


def teste_avaliar_fase4_resume_a_reproducao_e_renderiza_com_check():
    import avaliar_fase4 as av
    import pre_fase4 as pf
    base = {"cenario": "api-catalogo", "segundos": 3.2, "arvore_antes": 193, "arvore_depois": 40, "corpo_chars": 2000, "caso_chars": 800,
            "status": 200, "tempo_ms": 120.0, "sintoma": "x", "erro": None}
    registros = [{**base, "id": "a", "classe": 2, "nivel": 1, "causa": "campo_renomeado", "modo": "field_renamed", "campo": "preco", "reproduz": True, "motivo": "diff do contrato: renomeado"},
                 {**base, "id": "b", "classe": 2, "nivel": 1, "causa": "campo_ausente", "modo": "field_missing", "campo": None, "reproduz": False, "motivo": "nenhuma diferença medida"},
                 {**base, "id": "e", "classe": 1, "nivel": 1, "causa": "resposta_truncada", "modo": "malformed_json", "campo": None, "reproduz": True, "motivo": "corpo truncado"}]
    fora = [{"id": "c", "classe": 5, "nivel": 3, "causa": "dado_desatualizado", "motivo": "sem modo para a causa"},
            {"id": "d", "classe": 6, "nivel": 1, "causa": "localizador_quebrado", "motivo": "armada pelo harness (ficha 29)"}]
    dado = av.resumir(registros, fora, gerado_em="2026-10-26T22:00:00", corrida="fase4_reproducao")
    r = dado["resumo"]
    assert r["casos"] == 5 and r["na_tela"] == 3 and r["reproduzem"] == 2 and r["fora"] == 2, r
    assert r["reproduzem_pct"] == 40.0 and r["reproduzem_dos_na_tela_pct"] == 66.7, r
    assert dado["por_classe"][0]["classe"] == 1 and dado["por_classe"][0]["reproduzem"] == 1, dado["por_classe"]
    por_modo = {m["modo"]: m for m in dado["por_modo"]}
    assert por_modo["field_renamed"]["reproduzem"] == 1 and por_modo["field_missing"]["reproduzem"] == 0, por_modo
    assert dado["tempo"]["mediana_s"] == 3.2 and dado["tamanhos"]["arvore_depois_mediana"] == 40, dado
    md = av.render(dado)
    for bloco in ("tb_f4_reproducao_resumo", "tb_f4_reproducao_por_classe", "tb_f4_reproducao_por_modo", "tb_f4_reproducao_casos", "tb_f4_reproducao_fora"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    assert "—" not in md and "→" not in md
    pasta = _temp()
    assert pf.fechar(av.NOME, dado, md, av.PREFIXO, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert pf.fechar(av.NOME, dado, md, av.PREFIXO, check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert av.NOME == "reproducibilidade" and av.PREFIXO == "tb_f4_reproducao_"
    # ! Alteração de IA - Revisar: (27/10/2026) o avaliador aceita `--nome` e `--titulo`, para a corrida sobre os 36
    # inéditos da ficha 27 sair em `reproducibilidade_ineditos.{json,md}` sem regravar a leitura da corrida 17.
    # ! Motivo: `pf.fechar` grava pelo nome; com o nome fixo, avaliar a segunda corrida apagaria os números da primeira.
    assert av.TITULO == "Reprodução dos casos na tela (corrida 17)"
    assert "corrida 17 sobre os 36 inéditos" in av.render(dado, titulo="Reprodução na tela (corrida 17 sobre os 36 inéditos da ficha 27)")
    ap = av.montar_parser()
    assert ap.parse_args(["--reproducao"]).nome is None and av.nome_dos_arquivos(None, "reproducao") == av.NOME
    args = ap.parse_args(["--reproducao", "--saida", "fase4_reproducao_ineditos", "--nome", "reproducibilidade_ineditos"])
    assert args.nome == "reproducibilidade_ineditos" and args.titulo == av.TITULO


# ----------------------------------------------------------------------------- P3: diagnóstico ao vivo

# ! Alteração de IA - Revisar: testes do pacote P3 (27/10/2026), escritos antes de `diagnostico_ao_vivo.py`, dos modos
# `calibracao` e `tela` de `executar_fase4.py`, das leituras `--calibracao` e `--tela` de `avaliar_fase4.py` e dos modos
# novos de `rodar_fase4.ps1`. O Ollama é de mentira (troca de `cliente_ollama._post` e `_get`, como em testar_fase3), e
# as probabilidades por token vêm de fluxos sintéticos no formato que o Ollama devolve.
# ! Motivo: o plano aprovado (seção 5, P3) pede os testes antes: o registro do diagnóstico ao vivo tem as 37 chaves
# oficiais e mais nada; o prompt montado da tela é igual, byte a byte, ao do fixture quando a entrada é igual; a
# probabilidade é lida no token certo (acento partido, negrito, rótulo e quebra de linha no mesmo token); o selo segue
# `limiares.json`; os gatilhos disparam só nos casos previstos; a regra R2 é calculada contra um par sintético com
# b + c conhecido. A primeira rodada falha por ModuleNotFoundError em `diagnostico_ao_vivo`, que é o RED aceito.

import contextlib
import math


def _tok(texto: str, p: float, alternativas=None, dados: bytes | None = None) -> dict:
    """Um token na forma do Ollama (texto, log-probabilidade, bytes e as alternativas da posição, a própria primeiro)."""
    b = dados if dados is not None else texto.encode("utf-8")
    return {"token": texto, "logprob": math.log(p), "bytes": list(b),
            "top_logprobs": [{"token": texto, "logprob": math.log(p)}] + [{"token": t, "logprob": math.log(q)} for t, q in (alternativas or [])]}


def _tokens_da_resposta(texto: str, p_rotulo: float = 0.8, alternativas=(), p_outros: float = 0.97) -> list[dict]:
    """A resposta inteira repartida em tokens que, juntos pelos bytes, a remontam: o rótulo da CAUSA_RAIZ sai num token
    só, com a probabilidade e as alternativas pedidas; o resto vale `p_outros`."""
    tokens = []
    for i, linha in enumerate(texto.split("\n")):
        if i:
            tokens.append(_tok("\n", p_outros))
        if linha.startswith("CAUSA_RAIZ:"):
            tokens += [_tok("CAUSA_RAIZ", p_outros), _tok(":", p_outros), _tok(linha[len("CAUSA_RAIZ:"):], p_rotulo, list(alternativas))]
        elif ":" in linha and linha.split(":", 1)[0] in ("CAMPO", "IMPACTO", "FONTE"):
            nome, resto = linha.split(":", 1)
            tokens += [_tok(nome, p_outros), _tok(":", p_outros), _tok(resto, p_outros)]
        elif linha:
            tokens.append(_tok(linha, p_outros))
    return tokens


@contextlib.contextmanager
def _ollama_de_mentira_v2(responder, chamadas: list, versao: str = "0.40.2"):
    """Troca `cliente_ollama._post` e `_get` pelo tempo do bloco. `responder(prompt, corpo)` devolve (texto da resposta,
    probabilidade do rótulo, alternativas do rótulo); `chamadas` acumula os corpos enviados a /api/generate."""
    import cliente_ollama as oll
    original_post, original_get = oll._post, oll._get

    def post(caminho: str, corpo: dict, timeout: int = 900) -> dict:
        if caminho != "/api/generate" or not corpo.get("prompt"):
            return {}
        chamadas.append(corpo)
        texto, p, alternativas = responder(corpo["prompt"], corpo)
        tokens = _tokens_da_resposta(texto, p, alternativas)
        return {"response": texto, "logprobs": tokens if corpo.get("logprobs") else None, "done_reason": "stop",
                "prompt_eval_count": 1000, "prompt_eval_cached_count": 900, "eval_count": len(tokens),
                "load_duration": 0, "prompt_eval_duration": 1_000_000_000, "eval_duration": 500_000_000, "total_duration": 1_500_000_000}

    def get(caminho: str, timeout: int = 30) -> dict:
        if caminho == "/api/version":
            return {"version": versao}
        if caminho == "/api/ps":
            return {"models": [{"name": "qwen2.5:7b", "size": 5203 * 1024 * 1024, "size_vram": 0}]}
        if caminho == "/api/tags":
            return {"models": [{"name": "qwen2.5:7b", "digest": "845dbda0ea48000000"}]}
        return {}

    oll._post, oll._get = post, get
    try:
        yield
    finally:
        oll._post, oll._get = original_post, original_get


_BIBLIOTECA_CURADA: dict = {}


def _curada():
    """A L1 curada (biblioteca_producao) e o índice BM25 dela, carregados uma vez por rodada de testes."""
    if not _BIBLIOTECA_CURADA:
        import biblioteca as bib
        import diagnostico_ao_vivo as dv
        import recuperacao as rec
        verbetes = bib.carregar(dv.PASTA_CURADA)
        _BIBLIOTECA_CURADA.update({"verbetes": verbetes, "indice": rec.Indice(verbetes)})
    return _BIBLIOTECA_CURADA["verbetes"], _BIBLIOTECA_CURADA["indice"]


def _comum_de_teste(k: int = 3) -> dict:
    return {"digest": "845dbda0ea48", "versao_ollama": "0.40.2", "maquina": "maquina-de-teste", "epoca": 101, "biblioteca_epoca": 100,
            "biblioteca_versao": "1fca10f1a6f6", "particao": None, "k": k}


def teste_diagnostico_ao_vivo_prompt_igual_ao_do_fixture_e_registro_com_as_37_chaves():
    import diagnostico_ao_vivo as dv
    import executar_fase3
    from banco_casos import CASOS
    verbetes, indice = _curada()
    fixture = CASOS[0]
    vivo = {"id": f"{fixture['id']}@tela", "origem": "ao_vivo", "entrada": dict(fixture["entrada"])}
    ctx_f, prompt_f = executar_fase3.contexto_e_prompt(verbetes, indice, fixture, 3)
    ctx_v, prompt_v = dv.montar_prompt(verbetes, indice, vivo, 3)
    assert prompt_v == prompt_f, "o prompt da tela tem de ser, byte a byte, o do fixture quando a entrada é igual"
    assert ctx_v["verbetes_ids"] == ctx_f["verbetes_ids"] and ctx_v["texto"] == ctx_f["texto"]
    assert ctx_v["verbete_ouro"] is None and ctx_v["causa_plantada"] is None, "o gabarito não entra no agente"
    assert len(dv.montar_prompt(verbetes, indice, vivo, 5)[0]["verbetes_ids"]) == 5
    assert dv.hash_prompt_fixo(verbetes, ctx_v, vivo, prompt_v) == dv.hash_prompt_fixo(verbetes, ctx_f, fixture, prompt_f)
    assert len(dv.hash_indice(indice)) == 16 and dv.hash_indice(indice) == dv.hash_indice(indice)
    # o registro tem exatamente as 37 chaves do executor congelado, na mesma ordem
    r8 = {"segundos": 61.1, "tokens_entrada": 1118, "tokens_saida": 56, "carga_ms": 27, "prefill_ms": 63476, "geracao_ms": 12754, "total_ms": 76343,
          "resposta": "CAUSA_RAIZ: resposta_truncada\nCAMPO: nenhum\nIMPACTO: x.\nFONTE: nenhum"}
    ambiente = {"somente_cpu": True, "modelos_residentes": 1, "memoria_mb": 5203}
    particao = {"casos": {fixture["id"]: {"particao": "avaliacao"}}}
    comum = {**_comum_de_teste(), "particao": particao}
    original = executar_fase3.inferir_com_repeticao, executar_fase3.ambiente_residente
    executar_fase3.inferir_com_repeticao = lambda *a, **kw: dict(r8)
    executar_fase3.ambiente_residente = lambda: dict(ambiente)
    try:
        oficial = executar_fase3.diagnosticar("qwen2.5:7b", fixture, verbetes, ctx_f, prompt_f, 600, comum)
    finally:
        executar_fase3.inferir_com_repeticao, executar_fase3.ambiente_residente = original
    registro = dv.registro_oficial("qwen2.5:7b", vivo, verbetes, ctx_v, prompt_v, r8, _comum_de_teste(), ambiente)
    assert list(registro) == list(oficial), (list(registro), list(oficial))
    assert len(registro) == 37 and tuple(registro) == dv.CHAVES_OFICIAIS
    assert registro["gabarito"] is None and registro["verbete_ouro"] is None and registro["causa_plantada"] is None
    assert registro["caso"] == f"{fixture['id']}@tela" and registro["fase"] == "4" and registro["particao"] == "avaliacao"
    assert registro["contexto_sha256"] == oficial["contexto_sha256"] and registro["chars_contexto"] == oficial["chars_contexto"]
    assert registro["biblioteca_epoca"] == dv.VERSAO_CURADA and registro["k"] == 3 and registro["teto_tokens"] == 600


def teste_diagnostico_ao_vivo_le_a_probabilidade_no_token_certo():
    import analisar_confianca as conf
    import diagnostico_ao_vivo as dv
    simples = [_tok("CAUSA", .99), _tok("_RAIZ", .99), _tok(":", .99), _tok(" campo", .6, [(" tipo", .3), (" corpo", .05)]),
               _tok("_aus", .9, [("_renomeado", .08)]), _tok("ente", .95), _tok("\n", .99), _tok("CAMPO", .99), _tok(": preco", .5)]
    c = dv.confianca_do_rotulo(simples)
    assert c["rotulo"] == "campo_ausente" and math.isclose(c["p_rotulo"], .6) and math.isclose(c["logprob_rotulo"], math.log(.6))
    assert math.isclose(c["p_conjunta"], .6 * .9 * .95) and c["tokens_do_rotulo"] == 3
    alts = {a["opcao"]: a["escore"] for a in c["alternativas"]}
    assert math.isclose(alts["campo_ausente"], .6) and math.isclose(alts["tipo_divergente"], .3) and math.isclose(alts["campo_renomeado"], .6 * .08), alts
    assert math.isclose(alts["corpo_vazio"], .05) and math.isclose(alts["corpo_nao_e_json"], .05), "um prefixo comum a duas causas conta para as duas"
    assert c["segunda"]["opcao"] == "tipo_divergente" and math.isclose(c["margem"], .6 - .3)
    assert math.isclose(c["massa_divergente"], .3 + .05 + .6 * .08) and 0 < c["entropia_normalizada"] <= 1
    assert c["alternativas_top"] == 3, "quantas alternativas o Ollama devolveu na posição do rótulo"
    negrito = [_tok("**", .9), _tok("CAUSA_RAIZ", .9), _tok(":**", .9), _tok(" campo_ausente", .7), _tok("\n", .9)]
    c = dv.confianca_do_rotulo(negrito)
    assert c["rotulo"] == "campo_ausente" and math.isclose(c["p_rotulo"], .7) and c["segunda"] is None and math.isclose(c["margem"], .7)
    junto = [_tok("CAUSA_RAIZ", .9), _tok(":", .9), _tok(" tipo", .8), _tok("_divergente\nCAMPO", .5), _tok(": x", .9)]
    c = dv.confianca_do_rotulo(junto)
    assert c["rotulo"] == "tipo_divergente" and math.isclose(c["p_rotulo"], .8) and math.isclose(c["p_conjunta"], .4)
    o_agudo = "ó".encode("utf-8")
    partido = [_tok("Diagn", .9), _tok("�", .9, dados=o_agudo[:1]), _tok("�", .9, dados=o_agudo[1:]), _tok("stico\n", .9),
               _tok("CAUSA_RAIZ", .9), _tok(":", .9), _tok(" corpo", .7), _tok("_vazio", .6), _tok("\n", .9)]
    c = dv.confianca_do_rotulo(partido)
    assert c["rotulo"] == "corpo_vazio" and math.isclose(c["p_rotulo"], .7) and math.isclose(c["p_conjunta"], .42)
    assert dv.confianca_do_rotulo([_tok("não", .9), _tok(" sei", .9)]) is None, "sem a linha CAUSA_RAIZ não há probabilidade"
    # a probabilidade do rótulo ORIGINAL depois de uma intervenção: lida nas alternativas da posição do rótulo novo;
    # quando o rótulo original não está entre as alternativas devolvidas, fica só um limite inferior, marcado
    depois = [_tok("CAUSA_RAIZ", .9), _tok(":", .9), _tok(" tipo", .7, [(" campo", .2), (" corpo", .05)]), _tok("_divergente", .9), _tok("\n", .9)]
    t = conf.trecho_do_rotulo(depois)
    assert dv.probabilidade_do_rotulo_original(depois, t, "tipo_divergente") == (math.exp(math.log(.7)), False)
    p, limite = dv.probabilidade_do_rotulo_original(depois, t, "campo_ausente")
    assert math.isclose(p, .2) and limite is False
    p, limite = dv.probabilidade_do_rotulo_original(depois, t, "nulo_inesperado")
    assert math.isclose(p, .05) and limite is True, "abaixo da última alternativa devolvida"
    assert dv.probabilidade_do_rotulo_original(depois, None, "x") == (None, True)
    # o rótulo novo divide o primeiro token com o original (" campo" em campo_ausente e campo_renomeado, como na corrida 12):
    # a probabilidade do original é a desse token, sem limite inferior
    compartilha = [_tok("CAUSA_RAIZ", .9), _tok(":", .9), _tok(" campo", .6, [(" tipo", .3)]), _tok("_renomeado", .9, [("_ausente", .05)]), _tok("\n", .9)]
    p, limite = dv.probabilidade_do_rotulo_original(compartilha, conf.trecho_do_rotulo(compartilha), "campo_ausente")
    assert math.isclose(p, .6) and limite is False, (p, limite)


def teste_diagnostico_ao_vivo_limiares_e_selo():
    import diagnostico_ao_vivo as dv
    pares = [(.99, True), (.95, True), (.9, True), (.85, True), (.8, False), (.7, True), (.6, True), (.5, False), (.3, False), (.2, True)]
    linhas = [{"caso": f"c{i}", "p": p, "acerto": a} for i, (p, a) in enumerate(pares)]
    lim = dv.calcular_limiares(linhas, parcela=.3, k=3, origem="teste")
    # ficha 31 (a): baixo = os 30% de menor probabilidade (3 de 10: 0,2, 0,3 e 0,5), alto = acima da mediana dos acertos
    assert lim["baixo_ate"] == .5 and lim["revisados"] == 3 and lim["erros_pegos"] == 2 and lim["erros"] == 3 and lim["acertos_revisados"] == 1, lim
    assert lim["alto_a_partir_de"] == .85 and lim["parcela_baixa"] == .3 and lim["medida"] == "p_rotulo" and lim["k"] == 3 and lim["n"] == 10
    assert lim["leitura"] == dv.LEITURA_DA_PROBABILIDADE and lim["origem"] == "teste" and abs(lim["risco_no_que_sobra"] - 1 / 7) < 1e-3
    assert dv.selo(.3, lim) == "baixo" and dv.selo(.5, lim) == "baixo" and dv.selo(.6, lim) == "medio"
    assert dv.selo(.85, lim) == "alto" and dv.selo(.99, lim) == "alto"
    assert dv.selo(.3, None) is None and dv.selo(None, lim) is None, "sem limiares (antes da corrida 16) ou sem rótulo não há selo"
    lim2 = dv.calcular_limiares(linhas + [{"caso": "x", "p": None, "acerto": False}], parcela=.3)
    assert lim2["sem_rotulo"] == 1 and lim2["n"] == 10, "linha sem probabilidade fica fora da curva e é contada"
    pasta = _temp()
    dv.gravar_limiares(lim, pasta / "limiares.json")
    lido = dv.carregar_limiares(pasta / "limiares.json")
    assert lido["baixo_ate"] == .5 and lido["alto_a_partir_de"] == .85 and lido["gravado_em"]
    assert dv.carregar_limiares(pasta / "nao_existe.json") is None


def teste_diagnostico_ao_vivo_gatilhos_e_divergencia():
    import diagnostico_ao_vivo as dv
    lim = {"baixo_ate": .5, "alto_a_partir_de": .85, "medida": "p_rotulo", "parcela_baixa": .3}
    v_ok = [trilha._v("quatro_linhas_presentes", "resposta", "confere", {"ausentes": []}),
            trilha._v("rotulo_no_conjunto", "campo_ausente", "confere"),
            trilha._v("fonte_existe_na_biblioteca", "contrato-produto", "confere"),
            trilha._v("fonte_estava_no_contexto", "contrato-produto", "confere", {"contexto": ["contrato-produto"]}),
            trilha._v("campo_existe_no_caso", "preco", "confere"),
            trilha._v("rotulo_sustentado_por_verbete_do_contexto", "campo_ausente", "confere", {"verbetes": ["contrato-produto"]})]
    g = dv.gatilhos({"p_rotulo": .9}, v_ok, lim, caso_id="lex-1", amostra=())
    assert g == {"probabilidade": False, "fonte_divergente": False, "amostra": False, "algum": False}, g
    assert dv.gatilhos({"p_rotulo": .5}, v_ok, lim)["probabilidade"] is True, "no limiar, dispara"
    assert dv.gatilhos({"p_rotulo": .5}, v_ok, None)["probabilidade"] is False, "sem limiares o gatilho por probabilidade fica desligado"
    assert dv.gatilhos(None, v_ok, lim)["probabilidade"] is True, "sem rótulo lido não há probabilidade: o caso vai para intervenção"
    v_fora = [trilha._v("fonte_estava_no_contexto", "v-x", "nao_confere", {"contexto": []})]
    assert dv.gatilhos({"p_rotulo": .9}, v_fora, lim)["fonte_divergente"] is True
    v_sem = [trilha._v("rotulo_sustentado_por_verbete_do_contexto", "campo_ausente", "nao_confere", {"verbetes": []})]
    assert dv.gatilhos({"p_rotulo": .9}, v_sem, lim)["fonte_divergente"] is True
    g = dv.gatilhos({"p_rotulo": .9}, v_ok, lim, caso_id="lex-1", amostra=("lex-1",))
    assert g["amostra"] is True and g["algum"] is True
    assert dv.gatilhos({"p_rotulo": .9}, v_ok, lim, caso_id="lex-1@tela", amostra=("lex-1",))["amostra"] is True, "o caso ao vivo se chama <id>@tela"
    assert dv.gatilhos({"p_rotulo": .9}, v_ok, lim, caso_id="lex-2", amostra=("lex-1",))["amostra"] is False
    d, falha = dv.divergencia_e_falha(v_ok)
    assert d == {"ha": False, "entre": [], "detalhe": None} and falha is None
    d, falha = dv.divergencia_e_falha(v_fora)
    assert d["ha"] is True and d["entre"] == ["modelo", "verificacao"] and "fora do contexto" in d["detalhe"] and "v-x" in d["detalhe"]
    assert falha == "citacao_fora_do_contexto" and trilha.origem_da_falha(falha) == "modelo"
    d, falha = dv.divergencia_e_falha([trilha._v("quatro_linhas_presentes", "resposta", "nao_confere", {"ausentes": ["CAUSA_RAIZ"]}),
                                       trilha._v("rotulo_no_conjunto", None, "nao_se_aplica", "a resposta não tem a linha CAUSA_RAIZ")])
    assert falha == "formato_das_quatro_linhas" and d["ha"] is True and "CAUSA_RAIZ" in d["detalhe"]
    assert dv.divergencia_e_falha([trilha._v("rotulo_no_conjunto", "causa_inventada", "nao_confere")])[1] == "rotulo_fora_da_taxonomia"
    assert dv.divergencia_e_falha(v_sem)[1] == "causa_sem_verbete_que_a_trate"
    assert dv.divergencia_e_falha([trilha._v("campo_existe_no_caso", "precinho", "nao_confere")])[1] == "campo_errado"
    assert dv.divergencia_e_falha([trilha._v("fonte_existe_na_biblioteca", "v-inventado", "nao_confere")])[1] == "citacao_inexistente"
    d, falha = dv.divergencia_e_falha(v_ok, intervencoes=[{"tipo": "remocao", "verbete": "contrato-produto", "mudou_rotulo": True,
                                                            "rotulo_antes": "campo_ausente", "rotulo_depois": "tipo_divergente"}])
    assert d["ha"] is True and "contrato-produto" in d["detalhe"] and falha is None, "a intervenção marca divergência, não falha do modelo"
    assert all(trilha.origem_da_falha(f) is not None for f in dv.FALHA_POR_REGRA.values())


def teste_diagnostico_ao_vivo_emite_no_intervencoes_e_justificativa():
    import caso_ao_vivo as cv
    import diagnostico_ao_vivo as dv
    verbetes, indice = _curada()
    caso = cv.montar_caso("lex-1@tela", "GET /api/produtos", 200, "id: inteiro | nome: texto | preco: numero",
                          '[{"id": 1, "nome": "Picanha ao Alho", "preco_v2": 89.9}]', "O campo preco não veio na resposta.",
                          arvore='- main\n  - button "Saiba Mais..."', observacao="poda: árvore com 193 nós e 40 linhas depois")
    caso["classe"], caso["nivel"] = 1, 1    # metadados do caso, como Tela.rodar_caso os põe (não é o gabarito)
    ctx, _ = dv.montar_prompt(verbetes, indice, caso, 3)
    citado = ctx["verbetes_ids"][0]
    base = (f"O campo preco veio como preco_v2.\nCAUSA_RAIZ: campo_renomeado\nCAMPO: preco\nIMPACTO: o cartão mostra o preço vazio.\nFONTE: [{citado}]",
            .45, [(" tipo_divergente", .25), (" campo_ausente", .1)])

    def responder(prompt: str, corpo: dict):
        if prompt.startswith("\n\n====="):          # sem documentação: o contexto é vazio e o prompt começa pelo separador
            return ("Sem documentação.\nCAUSA_RAIZ: tipo_divergente\nCAMPO: preco\nIMPACTO: x.\nFONTE: nenhum", .55, [(" nulo", .2)])
        if dv.MARCADOR_NEUTRO.splitlines()[0] in prompt:   # o verbete citado foi trocado pelo marcador neutro
            return ("Faltou o verbete.\nCAUSA_RAIZ: campo_ausente\nCAMPO: preco\nIMPACTO: x.\nFONTE: nenhum", .5, [(" campo_renomeado", .3)])
        return base

    lim = {"baixo_ate": .5, "alto_a_partir_de": .85, "medida": "p_rotulo", "parcela_baixa": .3}
    tid = "fase4_tela/qwen2.5_7b/lex-1@tela"

    def trilha_com_poda():
        t = trilha.Trilha(versao=trilha.V2)
        t.corrida(_cabecalho(), ts=TS)
        s_ent = t.evento("entrada", tid, {"caso": "lex-1", "classe": 1, "nivel": 1, "caso_ao_vivo": t.blob(json.dumps(caso, ensure_ascii=False), "caso_ao_vivo")},
                         "ao_vivo", ts=TS)
        s_poda = t.evento("poda", tid, {"alvo": "corpo_http", "antes": {"chars": 60}, "depois": {"chars": 20}, "regras": ["diff_contra_contrato"],
                                        "sha": t.blob('{"preco_v2": 89.9}', "corpo_podado"),
                                        "diff": [{"campo": "preco", "esperado": "preco: numero", "recebido": "preco_v2", "tipo": "renomeado"}]},
                          "ao_vivo", pai=s_ent, ts=TS)
        return t, s_poda

    chamadas: list = []
    t, s_poda = trilha_com_poda()
    with _ollama_de_mentira_v2(responder, chamadas):
        saida = dv.diagnosticar(t, tid, caso, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=_comum_de_teste(), limiares=lim,
                                intervencoes="por_gatilho", evidencia=[{"seq": s_poda, "papel": "sinal_em_codigo"}], ts=TS)
    assert len(chamadas) == 5, "base, remoção, troca, sem documentação e a repetição da base: cinco inferências"
    assert all(c.get("logprobs") is True and c.get("top_logprobs") == dv.TOP_LOGPROBS for c in chamadas)
    assert all(c["options"]["num_gpu"] == 0 and c["options"]["num_ctx"] == 8192 and c["options"]["temperature"] == 0.1 for c in chamadas)
    reg = saida["registro"]
    assert tuple(reg) == dv.CHAVES_OFICIAIS and reg["gabarito"] is None and reg["resposta"] == base[0] and reg["caso"] == "lex-1@tela"
    assert reg["classe"] == 1 and reg["nivel"] == 1, "classe e nível do caso entram no registro ao vivo"
    lat = saida["lateral"]
    assert lat["caso"] == "lex-1@tela" and lat["top_logprobs"] == dv.TOP_LOGPROBS and lat["logprobs"] and lat["prompt_sha256"]
    no = saida["no"]
    assert no["decisao"] == "diagnostico" and no["escolha"] == "campo_renomeado" and no["resultado"] == "rotulo_emitido"
    assert no["confianca"]["selo"] == "baixo" and math.isclose(no["confianca"]["p_rotulo"], .45) and no["confianca"]["alternativas_top"] == 3
    assert no["confianca"]["leitura"] == dv.LEITURA_DA_PROBABILIDADE and math.isclose(no["confianca"]["margem"], .45 - .25)
    alts = {a["opcao"]: a["escore"] for a in no["alternativas"]}
    assert math.isclose(alts["tipo_divergente"], .25) and math.isclose(alts["campo_renomeado"], .45) and math.isclose(alts["campo_ausente"], .1)
    assert no["contraste"].startswith("campo_renomeado e não tipo_divergente"), no["contraste"]
    assert no["campo"] == "preco" and no["k"] == 3
    assert no["gatilhos"] == {"probabilidade": True, "fonte_divergente": False, "amostra": False, "algum": True}, no["gatilhos"]
    assert no["divergencia"]["ha"] is True and no["divergencia"]["entre"] == ["modelo", "verificacao"], "a remoção mudou o rótulo"
    assert no["falha"] is None and no["prov"]["wasGeneratedBy"] == saida["seq_inferencia"] and citado in no["prov"]["used"]
    por_tipo = {i["tipo"]: i for i in saida["intervencoes"]}
    assert list(por_tipo) == list(dv.INTERVENCOES), list(por_tipo)
    rem = por_tipo["remocao"]
    assert rem["verbete"] == citado and rem["alvo"] == "citado" and rem["mudou_rotulo"] is True and rem["rotulo_depois"] == "campo_ausente"
    assert math.isclose(rem["p_antes"], .45) and math.isclose(rem["p_depois"], .3) and rem["limite_inferior"] is False
    sem = por_tipo["sem_documentacao"]
    assert sem["rotulo_depois"] == "tipo_divergente" and sem["limite_inferior"] is True and math.isclose(sem["p_depois"], .2)
    assert por_tipo["troca"]["verbete"] == citado and por_tipo["troca"]["verbete_errado"] and por_tipo["troca"]["verbete_errado"] not in ctx["verbetes_ids"]
    assert por_tipo["troca"]["mudou_rotulo"] is False and por_tipo["repeticao_da_base"]["mudou_rotulo"] is False
    assert all(i["seq_inferencia"] for i in saida["intervencoes"])
    # eventos: cada intervenção é um evento próprio ligado à inferência que a pediu; o nó vem por último
    ev = [e for e in t.eventos if e["trilha"] == tid]
    s_inf = saida["seq_inferencia"]
    intervs = [e for e in ev if e["tipo"] == "intervencao"]
    assert len(intervs) == 4 and all(e["pai"] == s_inf for e in intervs) and [e["dados"]["tipo"] for e in intervs] == list(dv.INTERVENCOES)
    infs = [e for e in ev if e["tipo"] == "inferencia"]
    assert len(infs) == 5 and infs[0]["seq"] == s_inf and all(e["pai"] == s_inf for e in infs[1:])
    assert [e["dados"]["etapa"] for e in infs] == ["diagnostico"] + [f"intervencao:{i}" for i in dv.INTERVENCOES]
    nos = [e for e in ev if e["tipo"] == "decisao"]
    assert len(nos) == 1 and nos[0]["pai"] == s_inf and nos[0]["seq"] > intervs[-1]["seq"] and nos[0]["seq"] == saida["seq_decisao"]
    tipos = [e["tipo"] for e in ev]
    assert tipos.index("candidatos") < tipos.index("prompt") < tipos.index("inferencia") < tipos.index("declaracao") < tipos.index("verificacao")
    assert all(e["origem"] == "ao_vivo" and e["ts"] == TS for e in ev)
    papeis = {(e["papel"], e.get("id")) for e in no["evidencia"]}
    assert ("sinal_em_codigo", None) in papeis and ("verbete_entregue", citado) in papeis and ("verbete_citado", citado) in papeis and ("resposta", None) in papeis
    assert all("texto" not in e and "valor" not in e for e in no["evidencia"]), "a evidência aponta eventos, nunca copia texto"
    regras = [e["dados"]["regra"] for e in ev if e["tipo"] == "verificacao"]
    assert "fonte_formato_valido" in regras and "fonte_contem_termo_da_causa" in regras and "quatro_linhas_presentes" in regras
    assert not any(e["dados"]["usa_gabarito"] for e in ev if e["tipo"] == "verificacao"), "sem gabarito, nenhuma conferência o usa"
    decl = [e["dados"] for e in ev if e["tipo"] == "declaracao" and e["dados"].get("campo") == "causa_raiz"]
    assert decl and decl[0]["valor"] == "campo_renomeado" and base[0][decl[0]["ini"]:decl[0]["fim"]] == "campo_renomeado"
    j = no["justificativa"]
    assert j == grr.justificativa_por_molde(no, eventos=t.eventos, verificacoes=saida["verificacoes"], intervencoes=saida["intervencoes"])
    assert "não está seguro" in j and "campo preco" in j and citado in j and "mudou a resposta" in j and "—" not in j and "→" not in j, j
    assert "sem documentação" in j.lower() and "repetição" in j.lower(), "o molde diz o que cada intervenção fez, pelo tipo"
    t.fechar(fim="2026-10-27T20:05:00")
    md = grr.relatorio_do_caso_v2(t.eventos, tid, comando_reexecucao="python executar_fase4.py --modo tela --casos 1")
    assert "CONFLITO" in md and "**baixo**" in md and "sem_documentacao" in md and grr.MARCA_DO_MOLDE in md
    # com as intervenções desligadas (corrida 18) só a inferência de base roda; o gatilho fica registrado no nó
    chamadas2: list = []
    t2, s_poda2 = trilha_com_poda()
    with _ollama_de_mentira_v2(responder, chamadas2):
        s2 = dv.diagnosticar(t2, tid, caso, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=_comum_de_teste(), limiares=lim,
                             intervencoes="desligadas", evidencia=[{"seq": s_poda2, "papel": "sinal_em_codigo"}], ts=TS)
    assert len(chamadas2) == 1 and s2["intervencoes"] == [] and s2["gatilhos"]["algum"] is True and s2["no"]["divergencia"]["ha"] is False
    assert s2["no"]["confianca"]["selo"] == "baixo" and "não está seguro" in s2["no"]["justificativa"]
    # probabilidade alta e FONTE no contexto: por_gatilho não dispara nada; sem limiares não há selo nem gatilho por probabilidade
    chamadas3: list = []
    t3, s_poda3 = trilha_com_poda()
    sem_campo = base[0].replace("CAMPO: preco", "CAMPO: nenhum")
    with _ollama_de_mentira_v2(lambda p, c: (sem_campo, .95, [(" tipo_divergente", .02)]), chamadas3):
        s3 = dv.diagnosticar(t3, tid, caso, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=_comum_de_teste(), limiares=lim,
                             intervencoes="por_gatilho", evidencia=[{"seq": s_poda3, "papel": "sinal_em_codigo"}], ts=TS)
        s4 = dv.diagnosticar(t3, tid + "/2", caso, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=_comum_de_teste(), limiares=None,
                             intervencoes="por_gatilho", ts=TS)
    assert len(chamadas3) == 2 and s3["no"]["confianca"]["selo"] == "alto" and s3["gatilhos"]["algum"] is False and s3["no"]["divergencia"]["ha"] is False
    assert s3["no"]["campo"] is None and "campo nenhum" not in s3["no"]["justificativa"], "CAMPO: nenhum não vira 'no campo nenhum'"
    assert s4["no"]["confianca"]["selo"] is None and s4["gatilhos"]["probabilidade"] is False and s4["no"]["justificativa"]
    assert "campo nenhum" not in s4["no"]["justificativa"], "sem evento de poda o molde cai na declaração CAMPO, que também é 'nenhum'"
    # resposta sem a linha CAUSA_RAIZ: nó sem escolha, falha de formato e divergência marcada
    chamadas5: list = []
    t5, _ = trilha_com_poda()
    with _ollama_de_mentira_v2(lambda p, c: ("Não sei dizer.", .5, []), chamadas5):
        s5 = dv.diagnosticar(t5, tid, caso, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=_comum_de_teste(), limiares=lim,
                             intervencoes="desligadas", ts=TS)
    assert s5["no"]["escolha"] is None and s5["no"]["falha"] == "formato_das_quatro_linhas" and s5["no"]["divergencia"]["ha"] is True
    assert s5["no"]["confianca"]["p_rotulo"] is None and s5["no"]["confianca"]["selo"] is None and s5["gatilhos"]["probabilidade"] is True
    assert "None" not in s5["no"]["justificativa"] and "CAUSA_RAIZ" in s5["no"]["justificativa"] and s5["no"]["contraste"].startswith("sem rótulo")
    # sem rótulo de base, o gatilho dispara mas as intervenções não rodam (não há o que comparar) e o nó diz por quê
    chamadas6: list = []
    t6, _ = trilha_com_poda()
    with _ollama_de_mentira_v2(lambda p, c: ("Não sei dizer.", .5, []), chamadas6):
        s6 = dv.diagnosticar(t6, tid, caso, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=_comum_de_teste(), limiares=lim,
                             intervencoes="por_gatilho", ts=TS)
    assert len(chamadas6) == 1 and s6["intervencoes"] == [] and s6["no"]["intervencoes_puladas"] and "não rodaram" in s6["no"]["justificativa"]
    # a frase dos verbetes entregues cita só o que a busca entregou; o citado fora do contexto fica para a frase da FONTE
    solto = grr.justificativa_por_molde(_no(evidencia=[{"seq": 3, "papel": "verbete_entregue", "id": "contrato-produto"},
                                                        {"seq": 4, "papel": "verbete_citado", "id": "atualizacao_imediata"}]))
    assert "contrato-produto" in solto and "atualizacao_imediata" not in solto, solto


def teste_executar_fase4_calibracao_e_tela_partes_puras():
    import executar_fase4 as ex
    assert ex.MODOS == ("reproducao", "calibracao", "tela", "cura", "biblioteca")   # (01/11, P4) cura e (03/11, P5) biblioteca entraram na tupla

    def reg(caso: str, causa: str, resposta: str) -> dict:
        return {"caso": caso, "gabarito": {"causa_raiz": causa, "campo_afetado": None},
                "resposta": f"CAUSA_RAIZ: {resposta}\nCAMPO: nenhum\nIMPACTO: x.\nFONTE: nenhum"}

    # ponte contra a Fase 3 (regra R6, decisão 47): b = casos que só a corrida nova acertou, c = só a Fase 3; os dois casos de
    # texto corrigido em 28/09 ficam fora, como em analisar_fase3b.mesma_entrada
    base = [reg("a", "x", "x"), reg("b", "y", "z"), reg("c", "w", "w"), reg("d", "u", "u"), reg("efe-3", "q", "q"), reg("efe-10", "q", "r")]
    novos = [reg("a", "x", "x"), reg("b", "y", "y"), reg("c", "w", "v"), reg("efe-3", "q", "r"), reg("efe-10", "q", "q")]
    p = ex.ponte_contra_fase3(novos, base)
    assert (p["n"], p["b"], p["c"]) == (3, 1, 1) and p["ganhos"] == ["b"] and p["perdas"] == ["c"], p
    assert p["pareavel"] is True and p["limite"] == 2 and p["casos_de_texto_alterado"] == ["efe-10", "efe-3"] and p["discordantes"] == 2
    assert ex.ponte_contra_fase3(novos, base, alterados=frozenset())["n"] == 5
    # até 2 discordantes ainda é pareável (decisão 47); com 4 (b = 1, c = 3) não é
    assert ex.ponte_contra_fase3([reg("a", "x", "y"), reg("b", "y", "z"), reg("c", "w", "v")], base)["pareavel"] is True
    fora = ex.ponte_contra_fase3([reg("a", "x", "y"), reg("b", "y", "y"), reg("c", "w", "v"), reg("d", "u", "t")], base)
    assert fora["pareavel"] is False and (fora["b"], fora["c"]) == (1, 3), fora
    pontes = {"pontes": [{"versao": "0.34.4", "corrida": "fase3b_ponte_0344", "pareavel": True}, {"versao": "0.40.2", "corrida": "fase3b_ponte_0402", "pareavel": True}]}
    assert ex.versao_precisa_de_ponte("0.40.2", pontes) is False and ex.versao_precisa_de_ponte("0.41.0", pontes) is True
    assert ex.versao_precisa_de_ponte("0.40.2", None) is True and ex.versao_precisa_de_ponte(None, pontes) is True
    # regra R8: k = 5 só com acurácia balanceada maior E b + c acima de 3; empate ou k = 5 não medido ficam com k = 3
    assert ex.regra_r8({"acuracia_balanceada_pct": 70.0}, {"acuracia_balanceada_pct": 75.0}, {"b": 5, "c": 1})["k"] == 5
    assert ex.regra_r8({"acuracia_balanceada_pct": 70.0}, {"acuracia_balanceada_pct": 75.0}, {"b": 2, "c": 1})["k"] == 3
    assert ex.regra_r8({"acuracia_balanceada_pct": 75.0}, {"acuracia_balanceada_pct": 75.0}, {"b": 4, "c": 4})["k"] == 3
    assert ex.regra_r8({"acuracia_balanceada_pct": 75.0}, {"acuracia_balanceada_pct": 70.0}, {"b": 1, "c": 5})["k"] == 3
    r8 = ex.regra_r8({"acuracia_balanceada_pct": 70.0}, None, None)
    assert r8["k"] == 3 and "não" in r8["motivo"]
    assert ex.regra_r8(None, {"acuracia_balanceada_pct": 70.0}, None)["k"] == 5, "só k = 5 medido: os limiares vêm dele"
    # uma ponte só vale completa: os 36 casos e corrida não parcial
    trinta_e_seis = [reg(f"c{i}", "x", "x") for i in range(36)]
    assert ex.ponte_completa(trinta_e_seis, {}) is True and ex.ponte_completa(trinta_e_seis[:2], {}) is False
    assert ex.ponte_completa(trinta_e_seis, {"parcial": True}) is False
    assert ex.versao_precisa_de_ponte("0.40.2", {"pontes": [{"versao": "0.40.2", "completa": False}]}) is True
    assert ex.ler_ids("lex-1, lex-4") == ["lex-1", "lex-4"] and ex.ler_ids(None) == [] and ex.ler_ids("") == []
    for vazio in ("", " , "):
        try:
            ex.ler_ks(vazio)
        except ValueError:
            pass
        else:
            raise AssertionError("lista de k vazia aceita")
    rep = {"casos": [{"id": "lex-1", "reproduz": True}, {"id": "lex-4", "reproduz": False}, {"id": "sin-4", "reproduz": True}]}
    assert ex.casos_que_reproduzem(rep) == ["lex-1", "sin-4"]
    f = ex.fixture_sem_gabarito({"id": "lex-1", "classe": 1, "nivel": 1, "entrada": {"requisicao": "GET /x"}, "gabarito": {"causa_raiz": "x"}})
    assert "gabarito" not in f and f["origem"] == "fixture" and f["entrada"] == {"requisicao": "GET /x"} and f["id"] == "lex-1" and f["classe"] == 1
    assert ex.ler_ks("3,5") == (3, 5) and ex.ler_ks("3") == (3,) and ex.ler_ks(" 5 , 3 ") == (5, 3)
    try:
        ex.ler_ks("3,x")
    except ValueError:
        pass
    else:
        raise AssertionError("k inválido aceito")
    assert ex.RAM_MINIMA_GB["qwen2.5:7b"] == 6.5


def _registro_de_mentira(caso: str, classe: int, causa: str, resposta: str, p: float, segundos: float = 60.0, particao: str = "avaliacao",
                         k: int = 3) -> tuple[dict, dict]:
    """Um registro de diagnóstico (só as chaves que a avaliação lê) e a linha lateral dele com as probabilidades."""
    texto = f"CAUSA_RAIZ: {resposta}\nCAMPO: nenhum\nIMPACTO: x.\nFONTE: nenhum"
    import sonda_confianca as sc
    registro = {"caso": caso, "classe": classe, "nivel": 1, "modelo": "qwen2.5:7b", "versao_ollama": "0.40.2", "biblioteca_epoca": 100,
                "biblioteca_versao": "1fca10f1a6f6", "particao": particao, "k": k, "segundos": segundos, "tokens_entrada": 1100,
                "tokens_saida": 20, "gabarito": {"causa_raiz": causa, "campo_afetado": None}, "resposta": texto, "verbetes_ids": []}
    lateral = {"caso": caso, "biblioteca_epoca": 100, "top_logprobs": 20, "logprobs": sc.compactar(_tokens_da_resposta(texto, p, [(" nulo", .01)]))}
    return registro, lateral


def teste_avaliar_fase4_calibracao_e_tela_com_check():
    import avaliar_fase4 as av
    import pre_fase4 as pf
    pares = [("a", 1, "x", "x", .99, "aprendizado"), ("b", 1, "y", "y", .9, "avaliacao"), ("c", 2, "z", "q", .8, "avaliacao"),
             ("d", 2, "w", "w", .6, "avaliacao"), ("e", 3, "v", "r", .3, "aprendizado"), ("f", 3, "u", "u", .2, "avaliacao")]
    k3 = [_registro_de_mentira(c, cl, g, r, p, particao=pt) for c, cl, g, r, p, pt in pares]
    k5 = [_registro_de_mentira(c, cl, g, g if c != "a" else "q", p, segundos=72.0, particao=pt, k=5) for c, cl, g, r, p, pt in pares]
    bruto = {"k": {3: {"registros": [r for r, _ in k3], "laterais": [l for _, l in k3]}, 5: {"registros": [r for r, _ in k5], "laterais": [l for _, l in k5]}},
             "sondagem": {"metadados": {"versao_ollama": "0.40.2", "modelo": "qwen2.5:7b"},
                          "conferencias": {"a": {"tokens_com_logprob": 60, "top_por_posicao_max": 20, "tem_bytes": True, "texto_bate": True, "tokens_que_partem_caractere": 0},
                                           "temperatura": {"veredito": "antes", "razao": 0.98}, "resposta_igual_sem_logprobs": True}},
             "ponte": {"versao": "0.40.2", "feita_nesta_corrida": False, "corrida": "fase3b_ponte_0402", "b": 1, "c": 0, "n": 35, "pareavel": True},
             "condicoes": {"versao_ollama": "0.40.2", "k": [3, 5], "casos": 6}}
    dado = av.resumir_calibracao(bruto, gerado_em="2026-10-27T23:00:00", corrida="fase4_calibracao")
    por_k = {x["k"]: x for x in dado["por_k"]}
    assert por_k[3]["n"] == 6 and por_k[3]["acertos"] == 4 and por_k[5]["acertos"] == 5, por_k
    assert por_k[3]["acuracia_balanceada_pct"] == round(100 * 4 / 6, 1) and por_k[3]["segundos_mediana"] == 60.0 and por_k[5]["segundos_mediana"] == 72.0
    assert por_k[3]["sinais"]["p_rotulo"]["auroc"] is not None and por_k[3]["sinais"]["p_conjunta"]["auroc"] is not None
    assert por_k[3]["por_particao"]["avaliacao"]["n"] == 4 and por_k[3]["por_particao"]["aprendizado"]["n"] == 2
    assert [x["fracao"] for x in por_k[3]["revisao"]] == [0.1, 0.2, 0.3] and len(por_k[3]["curva"]) == 6
    assert dado["r8"]["par"]["b"] == 2 and dado["r8"]["par"]["c"] == 1 and dado["r8"]["k"] == 3, "b + c = 3 não passa de 3: fica o k = 3"
    # a linha lateral guarda a log-probabilidade com 5 casas (sonda_confianca.CASAS): a probabilidade volta com erro de 1e-5
    assert dado["limiares"]["k"] == 3 and dado["limiares"]["n"] == 6 and abs(dado["limiares"]["baixo_ate"] - .3) < 1e-4, dado["limiares"]
    assert dado["ponte"]["pareavel"] is True and dado["sondagem"]["ok"] is True and dado["sondagem"]["temperatura"] == "antes"
    assert por_k[3]["completo"] is True and por_k[5]["completo"] is True and dado["k_escolhido"] == 3
    # ! Alteração de IA - Revisar: (28/10/2026) os casos e os erros por selo com os limiares do k escolhido: baixo pega f e e
    # (os 30% de menor probabilidade, 2 de 6), alto começa na mediana dos acertos (0,75: a, b e c), d fica no médio.
    # ! Motivo: o bloco `tb_f4_calibracao_selos` é a origem dos "erros com selo alto" citados no roadmap e no painel.
    assert [(x["selo"], x["casos"], x["errados"]) for x in dado["por_selo"]] == [("baixo", 2, 1), ("medio", 1, 0), ("alto", 3, 1)], dado["por_selo"]
    assert dado["por_selo"][0]["casos_errados"] == ["e"] and dado["por_selo"][2]["casos_errados"] == ["c"] and dado["por_selo"][2]["erro_pct"] == round(100 / 3, 1)
    # k = 5 interrompido (4 de 6 casos) não entra na regra R8 nem nos limiares; só k = 5 medido: os limiares vêm dele
    interrompido = {**bruto, "k": {3: bruto["k"][3], 5: {"registros": bruto["k"][5]["registros"][:4], "laterais": bruto["k"][5]["laterais"][:4]}}}
    d2 = av.resumir_calibracao(interrompido, gerado_em="2026-10-27T23:00:00", corrida="fase4_calibracao")
    k5 = next(x for x in d2["por_k"] if x["k"] == 5)
    assert k5["completo"] is False and k5["n"] == 4 and d2["r8"]["k"] == 3 and d2["r8"]["par"] is None and d2["limiares"]["k"] == 3, d2["r8"]
    so5 = {**bruto, "k": {5: bruto["k"][5]}}
    d3 = av.resumir_calibracao(so5, gerado_em="2026-10-27T23:00:00", corrida="fase4_calibracao")
    assert d3["k_escolhido"] == 5 and d3["limiares"]["k"] == 5 and d3["r8"]["k"] == 5, (d3["k_escolhido"], d3["r8"])
    md = av.render_calibracao(dado)
    for bloco in ("tb_f4_calibracao_resumo", "tb_f4_calibracao_por_k", "tb_f4_calibracao_revisao", "tb_f4_calibracao_selos", "tb_f4_calibracao_r8",
                  "tb_f4_calibracao_ponte", "tb_f4_calibracao_sondagem", "tb_f4_calibracao_casos"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    assert "—" not in md and "→" not in md
    pasta = _temp()
    assert pf.fechar(av.NOME_CALIBRACAO, dado, md, av.PREFIXO_CALIBRACAO, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert pf.fechar(av.NOME_CALIBRACAO, dado, md, av.PREFIXO_CALIBRACAO, check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    # tela: regra R2 contra um par sintético com b + c conhecido (a e d concordam; b só a tela acerta; c só o fixture)
    casos = [{"id": i, "classe": cl, "nivel": 1, "gabarito": {"causa_raiz": g, "campo_afetado": None}} for i, cl, g in
             [("a", 1, "x"), ("b", 1, "y"), ("c", 2, "z"), ("d", 2, "w")]]
    tela = [_registro_de_mentira(f"{c}@tela", cl, g, r, p)[0] for c, cl, g, r, p in [("a", 1, "x", "x", .9), ("b", 1, "y", "y", .6), ("c", 2, "z", "q", .4), ("d", 2, "w", "q", .3)]]
    fixture = [_registro_de_mentira(c, cl, g, r, p)[0] for c, cl, g, r, p in [("a", 1, "x", "x", .95), ("b", 1, "y", "q", .5), ("c", 2, "z", "z", .7), ("d", 2, "w", "q", .2)]]
    por_caso = [{"caso": c, "reproduz": True, "p_tela": pt, "p_fixture": pf_, "selo_tela": st, "selo_fixture": sf, "segundos_tela": 80.0, "segundos_fixture": 60.0,
                 "gatilhos_tela": {"algum": g}, "intervencoes_tela": 0, "divergencia_tela": d}
                for c, pt, pf_, st, sf, g, d in [("a", .9, .95, "alto", "alto", False, False), ("b", .6, .5, "medio", "baixo", False, False),
                                                 ("c", .4, .7, "baixo", "medio", True, True), ("d", .3, .2, "baixo", "baixo", True, False)]]
    # (01/11/2026) a entrada do caso ao vivo (blobs da trilha): a tem diferença de campo contra o contrato, c não tem e a
    # poda mostrou o primeiro item da lista; o bloco `corpo` conta os dois lados e `rotulos` soma os casos
    vivos = {"a@tela": {"corpo": '{"preco": "89.9"}', "observacao": "poda: árvore com 193 nós e 39 linhas depois; corpo json, forma lista, 1 diferença(s) contra o contrato",
                        "sintoma": "O campo preco veio como texto em vez de numero."},
             "c@tela": {"corpo": '{"id": 1, "nome": "Picanha ao Alho"}', "observacao": "poda: árvore com 193 nós e 39 linhas depois; corpo json, forma lista, 0 diferença(s) contra o contrato",
                        "sintoma": "Nenhuma diferença medida contra a referência."}}
    dado_t = av.resumir_tela(tela, fixture, casos, por_caso, trilha_info={"bytes": 123456, "eventos": 400, "blobs_externos": 0},
                             gerado_em="2026-10-27T23:00:00", corrida="fase4_tela", vivos=vivos)
    r = dado_t["resumo"]
    cp = dado_t["corpo"]
    assert cp["casos_lidos"] == 2 and cp["sem_diferenca_contra_contrato"] == 1 and cp["sem_diferenca_casos"] == ["c"] and cp["sem_diferenca_concordam"] == 0, cp
    assert cp["com_diferenca_contra_contrato"] == 1 and cp["com_diferenca_concordam"] == 1 and cp["sintoma_sem_medida"] == 1 and cp["sintoma_sem_medida_casos"] == ["c"]
    linha_c = next(l for l in dado_t["casos"] if l["caso"] == "c")
    assert linha_c["diferencas_contra_contrato"] == 0 and linha_c["forma_do_corpo"] == "lista" and linha_c["corpo_tela"].startswith('{"id": 1')
    assert next(l for l in dado_t["casos"] if l["caso"] == "b")["diferencas_contra_contrato"] is None
    assert sum(x["tela"] for x in dado_t["rotulos"]) == 4 and sum(x["gabarito"] for x in dado_t["rotulos"]) == 4
    assert next(x for x in dado_t["rotulos"] if x["rotulo"] == "q") == {"rotulo": "q", "tela": 2, "fixture": 2, "gabarito": 0}, dado_t["rotulos"]
    assert r["casos"] == 4 and r["acerto_tela"] == 2 and r["acerto_fixture"] == 2 and r["concordam"] == 2, r
    assert r["b"] == 1 and r["c"] == 1 and r["discordantes"] == 2 and r["dentro_do_limite_r2"] is True and r["limite_r2"] == 3
    assert r["casos_que_mudaram"] == ["b", "c"] and r["selos_tela"] == {"alto": 1, "medio": 1, "baixo": 2} and r["gatilhos_tela"] == 2
    assert r["segundos_tela_mediana"] == 80.0 and r["segundos_fixture_mediana"] == 60.0 and r["trilha_bytes"] == 123456 and r["divergencias_tela"] == 1
    assert dado_t["por_classe"][0] == {"classe": 1, "casos": 2, "acerto_tela": 2, "acerto_fixture": 1, "concordam": 1}, dado_t["por_classe"]
    md_t = av.render_tela(dado_t)
    for bloco in ("tb_f4_tela_resumo", "tb_f4_tela_por_classe", "tb_f4_tela_rotulos", "tb_f4_tela_corpo", "tb_f4_tela_casos"):
        assert f"<!-- tabela:{bloco} -->" in md_t, bloco
    assert "—" not in md_t and "→" not in md_t
    assert pf.fechar(av.NOME_TELA, dado_t, md_t, av.PREFIXO_TELA, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert pf.fechar(av.NOME_TELA, dado_t, md_t, av.PREFIXO_TELA, check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    # (01/11/2026, ficha 37) --nome vale para a tela: a repetição da corrida 18 grava tela_v2.{json,md} sem tocar em tela.*
    assert av.nome_dos_arquivos(None, "tela") == "tela" and av.nome_dos_arquivos("tela_v2", "tela") == "tela_v2"
    assert av.nome_dos_arquivos(None, "reproducao") == "reproducibilidade" and av.nome_dos_arquivos("reproducibilidade_ineditos", "reproducao") == "reproducibilidade_ineditos"
    assert pf.fechar("tela_v2", dado_t, md_t, av.PREFIXO_TELA, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert (pasta / "tela_v2.json").exists() and (pasta / "tela.json").exists()
    assert av.NOME_CALIBRACAO == "calibracao" and av.NOME_TELA == "tela" and av.LIMITE_R2 == 3


def teste_rodar_fase4_ps1_com_bom_sem_travessao_e_modos_novos():
    arq = EXP / "rodar_fase4.ps1"
    dados = arq.read_bytes()
    assert dados[:3] == b"\xef\xbb\xbf", "sem BOM"
    texto = dados[3:].decode("utf-8")
    assert "—" not in texto and "–" not in texto and "→" not in texto
    # ! Alteração de IA - Revisar: (01/11/2026, P4) o modo `cura`, `-Repeticoes` e `-Formas` entram no `.ps1`.
    # ! Motivo: a corrida 19 é `rodar_fase4.ps1 -Modo cura -Saida fase4_cura -Repeticoes 5` (plano aprovado, seção 6).
    # ! Alteração de IA - Revisar: (03/11/2026, P5) o modo `biblioteca` e `-BaseIneditos` entram no `.ps1`.
    # ! Motivo: a corrida 20 é `rodar_fase4.ps1 -Modo biblioteca -Saida fase4_biblioteca` (plano aprovado, seção 6).
    assert 'ValidateSet("reproducao", "calibracao", "tela", "cura", "biblioteca")' in texto, "os modos novos entram no ValidateSet"
    assert "[int]$Repeticoes = 5" in texto and "[string]$Formas" in texto and "--repeticoes" in texto and "--formas" in texto
    assert '[string]$BaseIneditos = "corrida12"' in texto and "--base-ineditos" in texto and '($Modo -eq "biblioteca")' in texto
    for trecho in ("[string]$K", "[switch]$Intervencoes", "RamLivreGB", "api/version", "--pasta", "[int][math]::Floor($duracao.TotalHours)",
                   "testar_fase4.py", "executar_fase4.py", "avaliar_fase4.py"):
        assert trecho in texto, trecho
    assert "de IA - Revisar" in texto and "! Motivo:" in texto
    # ! Alteração de IA - Revisar: confere que o Marco grava com System.IO.FileStream em FileShare.ReadWrite (sem Add-Content) e que
    # espera ao menos 60 tentativas de 500 ms.
    # ! Motivo: o Add-Content falha com qualquer outro processo que tenha o fase4.log aberto (corrida 16, 27/10/2026: a chamada de
    # avaliar_fase4.py e a linha FIM ficaram fora do log); se alguém voltar ao Add-Content ou encurtar a espera, este teste acusa.
    import re
    codigo = "\n".join(linha for linha in texto.splitlines() if not linha.lstrip().startswith("#"))
    assert "System.IO.FileStream" in codigo and "[System.IO.FileShare]::ReadWrite" in codigo, "o Marco grava com FileShare.ReadWrite"
    assert "Add-Content" not in codigo, "o Add-Content não aceita nenhum leitor no arquivo; o Marco usa FileStream"
    tentativas = re.search(r"\$tentativa -le (\d+)", codigo)
    assert tentativas and int(tentativas.group(1)) >= 60, "o Marco espera ao menos 60 tentativas de 500 ms"
    import shutil
    import subprocess
    if shutil.which("powershell"):
        r = subprocess.run(["powershell", "-NoProfile", "-Command", f"[scriptblock]::Create((Get-Content -Raw '{arq}')) | Out-Null; 'parse ok'"],
                           capture_output=True, text=True, timeout=60)
        assert "parse ok" in r.stdout, r.stderr
    else:
        print("  (pulado com aviso: powershell não está no PATH; o parse do .ps1 não foi conferido)")


# ! Alteração de IA - Revisar: teste novo (01/11/2026) que chama de verdade o `Marco` do rodar_fase4.ps1, tirado do arquivo pela
# árvore sintática do PowerShell (o script em si não roda), com o fase4.log aberto por outro leitor (acesso de leitura, que aceita
# escrita de outros processos), e confere que as três linhas chegam ao arquivo, na ordem, com um só BOM no começo.
# ! Motivo: na corrida 16 as duas últimas linhas do .ps1 (a chamada de avaliar_fase4.py e a linha FIM) ficaram fora do fase4.log
# porque o Add-Content falha com qualquer outro processo que tenha o arquivo aberto, até com um leitor que aceita escrita; conferir
# só o texto do .ps1 não pegaria uma volta ao Add-Content. Com o Marco antigo este teste falha: a linha 2 não entra, depois de 5 s.
def teste_marco_do_rodar_fase4_grava_com_o_log_aberto_por_outro_leitor():
    import base64
    import re
    import subprocess
    if not shutil.which("powershell"):
        print("  (pulado com aviso: powershell não está no PATH; o Marco não foi exercitado)")
        return
    arq = EXP / "rodar_fase4.ps1"
    log = _temp() / "saida" / "fase4.log"

    def literal(caminho: Path) -> str:
        return "'" + str(caminho).replace("'", "''") + "'"

    roteiro = "\n".join([
        "$ErrorActionPreference = 'Stop'",
        "$tokens = $null; $erros = $null",
        f"$ast = [System.Management.Automation.Language.Parser]::ParseFile({literal(arq)}, [ref]$tokens, [ref]$erros)",
        "$def = $ast.Find({ param($n) ($n -is [System.Management.Automation.Language.FunctionDefinitionAst]) -and ($n.Name -eq 'Marco') }, $true)",
        "if (-not $def) { throw 'funcao Marco nao encontrada no rodar_fase4.ps1' }",
        "Invoke-Expression $def.Extent.Text",
        f"$Log = {literal(log)}",
        "Marco 'linha 1'",
        "$leitor = [System.IO.File]::Open($Log, 'Open', 'Read', 'ReadWrite')",
        "try { Marco 'linha 2' } finally { $leitor.Dispose() }",
        "Marco 'linha 3'",
    ])
    r = subprocess.run(["powershell", "-NoProfile", "-EncodedCommand", base64.b64encode(roteiro.encode("utf-16-le")).decode("ascii")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
    assert r.returncode == 0, (r.stdout, r.stderr)
    assert "nao consegui" not in r.stdout, r.stdout
    dados = log.read_bytes()
    assert dados[:3] == b"\xef\xbb\xbf" and dados.count(b"\xef\xbb\xbf") == 1, "um só BOM, no começo do arquivo criado pelo Marco"
    linhas = dados[3:].decode("utf-8").split("\r\n")
    assert len(linhas) == 4 and linhas[-1] == "", linhas
    for numero, linha in enumerate(linhas[:3], start=1):
        assert re.fullmatch(r"\[\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\] linha " + str(numero), linha), linha


# ----------------------------------------------------------------------------- P4: cura de seletor e reexecução

# ! Alteração de IA - Revisar: testes do pacote P4 (01/11/2026), escritos antes de `cura_seletor.py`, dos modos de quebra
# de localizador em `cenarios_fase4.py` (armados pelo harness por `add_init_script` e pela variante do front PHP ligada
# só por parâmetro de URL ou cookie, ficha 29 opção c, decisão 80), do modo `cura` de `executar_fase4.py`, da leitura
# `--cura` de `avaliar_fase4.py`, do relatório v2 com a cura e do `rodar_fase4.ps1`. Tudo sem modelo e, salvo a quebra
# armada no navegador (pulada com aviso quando o Playwright não está neste Python), sem navegador e sem cobaias: a
# árvore vem da fixture congelada de produtos_api.php e os resolvedores são de mentira.
# ! Motivo: o plano aprovado (seção 5, P4) pede os testes antes: cada estratégia de candidato gera o esperado numa
# árvore de exemplo; a verificação recusa candidato que resolve para dois elementos, para elemento invisível ou para
# outro papel; a ordem de aplicação é a fixa; o relatório lista todos os candidatos com o resultado; a quebra armada é
# determinística (o mesmo HTML, duas vezes, dá a mesma árvore). A primeira rodada falha por ModuleNotFoundError em
# `cura_seletor`, que é o RED aceito para módulo novo.

import shutil as _shutil
import subprocess as _subprocess


def _alvo_saiba_mais(ocorrencia: int = 6) -> dict:
    """O alvo registrado na corrida de referência: o botão "Saiba Mais..." do sexto cartão de produtos_api.php, na forma
    que cura_seletor.descrever_elemento devolve (papel e nome pela árvore de acessibilidade; o resto pelo DOM)."""
    return {"seletor": f"#produtos-api-grid .saiba-mais[data-id='{ocorrencia}']", "tag": "button", "papel": "button", "nome": "Saiba Mais...",
            "texto": "Saiba Mais...", "ocorrencia": ocorrencia,
            "atributos": {"id": None, "class": "btn btn-info btn-xs saiba-mais", "data-id": str(ocorrencia), "name": None, "type": "button",
                          "value": None, "placeholder": None, "aria-label": None, "href": None},
            "ancestral_com_id": "produtos-api-grid",
            "caminho": f"#produtos-api-grid > div:nth-of-type({ocorrencia}) > div > div > p:nth-of-type(4) > button:nth-of-type(2)",
            "pai": f"#produtos-api-grid > div:nth-of-type({ocorrencia}) > div > div > p:nth-of-type(4)", "posicao_entre_irmaos": 2,
            "impressao": {"tag": "button", "type": "button", "name": None, "form_action": None, "data_nome": None, "href": None}}


def teste_cura_gera_os_candidatos_na_ordem_fixa_a_partir_da_arvore_podada():
    import cura_seletor as cs
    import poda
    assert cs.ESTRATEGIAS == ("papel_e_nome", "papel_e_nome_parecido", "texto_contido", "data_id", "caminho_do_ancestral_com_id", "posicao_entre_irmaos")
    assert cs.LIMIAR_NOME == 0.6
    nos, titulo = _nos_da_pagina()
    interativos = [{"papel": "button", "nome": "Saiba Mais...", "class": "btn btn-info btn-xs saiba-mais", "data-id": str(i)} for i in range(1, 15)]
    alvo = _alvo_saiba_mais(6)
    podada = poda.podar_arvore(nos, titulo=titulo, alvo={"papel": "button", "nome": "Saiba Mais...", "ocorrencia": 6}, interativos=interativos)
    cands = cs.gerar_candidatos(alvo, podada["texto"])
    assert [c["estrategia"] for c in cands] == list(cs.ESTRATEGIAS), [c["estrategia"] for c in cands]
    por = {c["estrategia"]: c for c in cands}
    # (1) papel e nome iguais: a árvore mostra quatro botões com esse nome, então o candidato leva a ocorrência da referência
    assert por["papel_e_nome"]["gerado"] is True and por["papel_e_nome"]["seletor"] == 'role=button[name="Saiba Mais..."] >> nth=5', por["papel_e_nome"]
    assert por["papel_e_nome"]["cadeia"] == ['role=button[name="Saiba Mais..."]'] and por["papel_e_nome"]["nth"] == 5
    # (2) nome parecido: nenhum outro botão da árvore se parece com "Saiba Mais..."
    assert por["papel_e_nome_parecido"]["gerado"] is False and "parecido" in por["papel_e_nome_parecido"]["motivo"], por["papel_e_nome_parecido"]
    # (3) texto contido
    assert por["texto_contido"]["gerado"] is True and por["texto_contido"]["seletor"] == "text=Saiba Mais... >> nth=5", por["texto_contido"]
    # (4) data-id igual
    assert por["data_id"]["gerado"] is True and por["data_id"]["seletor"] == 'button[data-id="6"]', por["data_id"]
    # (5) caminho a partir do ancestral com id
    assert por["caminho_do_ancestral_com_id"]["gerado"] is True and por["caminho_do_ancestral_com_id"]["seletor"] == alvo["caminho"]
    # (6) posição entre os irmãos do mesmo papel
    assert por["posicao_entre_irmaos"]["cadeia"] == [alvo["pai"], "role=button"] and por["posicao_entre_irmaos"]["nth"] == 1
    assert por["posicao_entre_irmaos"]["seletor"] == alvo["pai"] + " >> role=button >> nth=1"
    assert all(cs.seletor_de(c) == c["seletor"] for c in cands if c["gerado"])
    # a árvore em que o botão foi renomeado: (1) não gera, (2) acha o nome parecido acima do limiar e (3) acha o texto contido
    texto2 = podada["texto"].replace('button "Saiba Mais..."', 'button "Saiba Mais... agora"')
    por2 = {c["estrategia"]: c for c in cs.gerar_candidatos(alvo, texto2)}
    assert por2["papel_e_nome"]["gerado"] is False and "não tem" in por2["papel_e_nome"]["motivo"], por2["papel_e_nome"]
    assert por2["papel_e_nome_parecido"]["gerado"] is True and por2["papel_e_nome_parecido"]["seletor"] == 'role=button[name="Saiba Mais... agora"] >> nth=5'
    assert por2["papel_e_nome_parecido"]["similaridade"] >= cs.LIMIAR_NOME
    assert por2["texto_contido"]["gerado"] is True, "o nome novo contém o texto do alvo"
    # alvo sem data-id e sem texto visível: as estratégias que dependem deles não geram candidato e dizem por quê
    alvo3 = {**alvo, "texto": "", "atributos": {**alvo["atributos"], "data-id": None}}
    por3 = {c["estrategia"]: c for c in cs.gerar_candidatos(alvo3, podada["texto"])}
    assert por3["data_id"]["gerado"] is False and "data-id" in por3["data_id"]["motivo"]
    assert por3["texto_contido"]["gerado"] is False and "texto" in por3["texto_contido"]["motivo"]
    # um nó único na árvore não precisa de nth
    alvo4 = {**alvo, "papel": "link", "nome": "PRODUTOS (API)", "texto": "PRODUTOS (API)", "ocorrencia": 1}
    por4 = {c["estrategia"]: c for c in cs.gerar_candidatos(alvo4, podada["texto"])}
    assert por4["papel_e_nome"]["seletor"] == 'role=link[name="PRODUTOS (API)"]' and por4["papel_e_nome"]["nth"] is None
    assert por4["texto_contido"]["seletor"] == "text=PRODUTOS (API)"
    # sem ancestral com id, o caminho parte do body e a estratégia diz isso
    alvo5 = {**alvo, "ancestral_com_id": None, "caminho": "body > div:nth-of-type(2) > button:nth-of-type(1)", "pai": "body > div:nth-of-type(2)"}
    por5 = {c["estrategia"]: c for c in cs.gerar_candidatos(alvo5, podada["texto"])}
    assert por5["caminho_do_ancestral_com_id"]["gerado"] is True and "body" in por5["caminho_do_ancestral_com_id"]["motivo"]
    # texto normalizado e similaridade
    assert cs.normalizar("  Reservar   MESA ") == "reservar mesa" and cs.normalizar("Análise") == "analise"
    assert cs.similaridade("Entrar", "Entrar agora") >= cs.LIMIAR_NOME and cs.similaridade("Entrar", "Acessar") < cs.LIMIAR_NOME
    assert cs.similaridade("EXCLUIR", "EXCLUIR ITEM") >= cs.LIMIAR_NOME and cs.similaridade("Reservar", "Reservar mesa") >= cs.LIMIAR_NOME
    assert cs.similaridade("Saiba Mais...", "Saiba Mais...") == 1.0
    assert cs.gerar_candidatos(alvo, podada["texto"]) == cands, "a geração é determinística"
    nos_podados = cs.nos_da_arvore_podada(podada["texto"])
    assert any(n["papel"] == "button" and n["nome"] == "Saiba Mais..." and n["atributos"].get("data-id") == "6" for n in nos_podados), nos_podados[:5]


def teste_cura_verificacao_recusa_dois_elementos_invisivel_e_outro_papel():
    import cura_seletor as cs
    assert cs.VERIFICACOES == ("resolve_um_elemento", "visivel_e_habilitado", "mesmo_papel", "nome_parecido", "efeito_na_reexecucao")
    alvo = _alvo_saiba_mais(6)
    base = {"contagem": 1, "visivel": True, "habilitado": True, "papel": "button", "nome": "Saiba Mais..."}
    ok = cs.verificar_candidato(base, alvo)
    assert ok["passou_estaticas"] is True and all(ok[v]["resultado"] == "confere" for v in cs.VERIFICACOES[:4]), ok
    assert ok["nome_parecido"]["similaridade"] == 1.0 and ok["falha"] is None
    assert ok["efeito_na_reexecucao"]["resultado"] == "nao_tentado", "o efeito só é medido na reexecução"
    dois = cs.verificar_candidato({**base, "contagem": 2}, alvo)
    assert dois["passou_estaticas"] is False and dois["resolve_um_elemento"]["resultado"] == "nao_confere" and "2" in dois["resolve_um_elemento"]["detalhe"], dois
    assert dois["mesmo_papel"]["resultado"] == "nao_se_aplica", "sem um elemento só, as outras verificações não se aplicam"
    assert dois["falha"] == "candidato_ambiguo"
    zero = cs.verificar_candidato({**base, "contagem": 0}, alvo)
    assert zero["passou_estaticas"] is False and zero["falha"] == "candidato_invalido" and zero["visivel_e_habilitado"]["resultado"] == "nao_se_aplica"
    invisivel = cs.verificar_candidato({**base, "visivel": False}, alvo)
    assert invisivel["passou_estaticas"] is False and invisivel["visivel_e_habilitado"]["resultado"] == "nao_confere" and invisivel["falha"] == "candidato_invalido"
    assert invisivel["mesmo_papel"]["resultado"] == "confere", "as verificações seguintes continuam medidas, para o relatório mostrar todas"
    desabilitado = cs.verificar_candidato({**base, "habilitado": False}, alvo)
    assert desabilitado["passou_estaticas"] is False and "habilitado" in desabilitado["visivel_e_habilitado"]["detalhe"]
    outro = cs.verificar_candidato({**base, "papel": "link"}, alvo)
    assert outro["passou_estaticas"] is False and outro["mesmo_papel"]["resultado"] == "nao_confere" and "link" in outro["mesmo_papel"]["detalhe"]
    longe = cs.verificar_candidato({**base, "nome": "Ver detalhes"}, alvo)
    assert longe["passou_estaticas"] is False and longe["nome_parecido"]["resultado"] == "nao_confere" and longe["nome_parecido"]["similaridade"] < cs.LIMIAR_NOME
    perto = cs.verificar_candidato({**base, "nome": "Saiba Mais... agora"}, alvo)
    assert perto["passou_estaticas"] is True and perto["nome_parecido"]["similaridade"] >= cs.LIMIAR_NOME
    assert cs.verificar_candidato({**base, "nome": "Ver detalhes"}, alvo, limiar=0.1)["passou_estaticas"] is True, "o limiar é parâmetro e fica registrado na corrida"
    # a impressão do elemento (o que nenhum modo de quebra muda) decide "mesmo elemento" e "outro elemento" (regra R3)
    a = {"tag": "button", "type": "submit", "name": None, "form_action": "login.php", "data_nome": None, "href": None}
    assert cs.mesmo_elemento(a, dict(a)) is True and cs.mesmo_elemento(a, {**a, "data_nome": "x"}) is False and cs.mesmo_elemento(a, None) is None


def _candidatos_de_mentira(cs) -> list[dict]:
    return [{"estrategia": e, "gerado": e != "papel_e_nome_parecido", "motivo": None if e != "papel_e_nome_parecido" else "nenhum button com nome parecido",
             "seletor": f"sel:{e}", "cadeia": [f"sel:{e}"], "nth": None, "nome_encontrado": None, "similaridade": None} for e in cs.ESTRATEGIAS]


def _resolucoes_de_mentira() -> dict:
    um = {"contagem": 1, "visivel": True, "habilitado": True, "papel": "button", "nome": "Saiba Mais..."}
    return {"papel_e_nome": {**um, "contagem": 2}, "texto_contido": {**um, "visivel": False}, "data_id": {**um, "papel": "link"},
            "caminho_do_ancestral_com_id": dict(um), "posicao_entre_irmaos": dict(um)}


def teste_cura_aplica_so_o_primeiro_que_passa_e_registra_todos():
    import cura_seletor as cs
    alvo = _alvo_saiba_mais(6)
    cands = _candidatos_de_mentira(cs)
    resolucoes = _resolucoes_de_mentira()
    reexecucoes: list[str] = []

    def resolver(c: dict) -> dict:
        return resolucoes[c["estrategia"]]

    def reexecutar(c: dict) -> dict:
        reexecucoes.append(c["estrategia"])
        passou = c["estrategia"] == "posicao_entre_irmaos"
        return {"passou": passou, "detalhe": "o roteiro chegou ao fim" if passou else "falhou no passo 6", "mesmo_elemento": True if passou else None,
                "segundos": 1.5, "impressao": dict(alvo["impressao"])}

    r = cs.escolher(cands, resolver, reexecutar, alvo)
    assert r["curado"] is True and r["aplicado"]["estrategia"] == "posicao_entre_irmaos", r["aplicado"]
    assert reexecucoes == ["caminho_do_ancestral_com_id", "posicao_entre_irmaos"], "só quem passa as quatro verificações estáticas é reexecutado, na ordem fixa"
    assert r["reexecucoes"] == 2 and r["falha"] is None and r["mesmo_elemento"] is True
    assert len(r["candidatos"]) == 6 and [c["estrategia"] for c in r["candidatos"]] == list(cs.ESTRATEGIAS)
    por = {c["estrategia"]: c for c in r["candidatos"]}
    assert por["papel_e_nome_parecido"]["gerado"] is False and por["papel_e_nome_parecido"]["verificacoes"] is None and por["papel_e_nome_parecido"]["reexecutado"] is False
    assert por["papel_e_nome"]["verificacoes"]["resolve_um_elemento"]["resultado"] == "nao_confere" and por["papel_e_nome"]["reexecutado"] is False
    assert por["papel_e_nome"]["efeito"]["resultado"] == "nao_tentado" and por["papel_e_nome"]["aplicado"] is False
    assert por["caminho_do_ancestral_com_id"]["reexecutado"] is True and por["caminho_do_ancestral_com_id"]["efeito"]["resultado"] == "nao_confere"
    assert por["caminho_do_ancestral_com_id"]["aplicado"] is False and "passo 6" in por["caminho_do_ancestral_com_id"]["efeito"]["detalhe"]
    assert por["posicao_entre_irmaos"]["aplicado"] is True and por["posicao_entre_irmaos"]["efeito"]["resultado"] == "confere"
    assert r["segundo"]["estrategia"] == "caminho_do_ancestral_com_id", "o segundo candidato é o anterior que passou as estáticas e foi recusado na reexecução"
    # nenhuma reexecução passa: a falha é da reexecução
    r2 = cs.escolher(cands, resolver, lambda c: {"passou": False, "detalhe": "falhou no passo 6", "mesmo_elemento": None}, alvo)
    assert r2["curado"] is False and r2["aplicado"] is None and r2["falha"] == "reexecucao_falhou" and r2["reexecucoes"] == 2
    # nenhum candidato passa as estáticas: nada é reexecutado e a falha é a do melhor candidato (ambíguo antes de inválido)
    r3 = cs.escolher(cands[:4], resolver, reexecutar, alvo)
    assert r3["curado"] is False and r3["falha"] == "candidato_ambiguo" and r3["reexecucoes"] == 0 and r3["segundo"] is None
    r4 = cs.escolher(cands[2:4], resolver, reexecutar, alvo)
    assert r4["falha"] == "candidato_invalido"
    # a escolha ganha os campos do relatório: resultado e o contraste entre o aplicado e o segundo
    assert r["resultado"] == "cura_aplicada" and r2["resultado"] == "sem_cura"
    assert "posicao_entre_irmaos" in cs.contraste_da_cura(r) and "e não" in cs.contraste_da_cura(r) and "caminho_do_ancestral_com_id" in cs.contraste_da_cura(r)


def _trilha_de_cura(curado: bool = True, mesmo: bool = True) -> tuple:
    """Uma trilha v2 de uma execução da cura, com os eventos que o modo `cura` emite: entrada, as ações do roteiro que
    quebrou, a poda da árvore, o evento `cura`, o nó `cura`, as ações da reexecução e o nó `reexecucao`."""
    import cura_seletor as cs
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(), ts=TS)
    tid = "fase4_cura/front-admin-login/texto_alterado/harness/r1"
    alvo = {**_alvo_saiba_mais(1), "papel": "button", "nome": "Entrar", "texto": "Entrar", "seletor": 'role=button[name="Entrar"]',
            "atributos": {"id": None, "class": " btn btn-primary", "data-id": None, "name": None, "type": "submit", "value": None, "placeholder": None, "aria-label": None, "href": None},
            "ancestral_com_id": None, "caminho": "body > div > div > form > button:nth-of-type(1)", "pai": "body > div > div > form", "posicao_entre_irmaos": 1,
            "impressao": {"tag": "button", "type": "submit", "name": None, "form_action": "login.php", "data_nome": None, "href": None}}
    s_ent = t.evento("entrada", tid, {"roteiro": "front-admin-login", "modo": "texto_alterado", "forma": "harness", "repeticao": 1, "passo": 5,
                                      "localizador": alvo["seletor"], "alvo": alvo}, "ao_vivo", ts=TS)
    for i, sel in enumerate(["admin/login.php", "#login_usuario", "#login_usuario", "#senha_usuario", alvo["seletor"]]):
        t.evento("acao", tid, {"passo": i + 1, "acao": "clicar" if i == 4 else "preencher", "seletor": sel, "tempo_ms": 10.0, "falhou": i == 4}, "ao_vivo", pai=s_ent, ts=TS)
    s_poda = t.evento("poda", tid, {"alvo": "arvore", "antes": {"nos": 12}, "depois": {"linhas": 6}, "regras": {}, "diff": [],
                                    "sha": t.blob('document "Chuleta Quente - Login"\n  textbox "Login"\n  textbox "Senha"\n  button "Entrar agora"\n', "arvore_podada")},
                     "ao_vivo", pai=s_ent, ts=TS)
    cands = _candidatos_de_mentira(cs)
    resolucoes = _resolucoes_de_mentira()
    resolucoes["papel_e_nome"] = {"contagem": 0, "visivel": None, "habilitado": None, "papel": None, "nome": None}
    resolucoes["caminho_do_ancestral_com_id"]["nome"] = "Entrar agora"
    resolucoes["posicao_entre_irmaos"]["nome"] = "Entrar agora"

    def reexecutar(c: dict) -> dict:
        passou = curado and c["estrategia"] == "posicao_entre_irmaos"
        return {"passou": passou, "detalhe": "o roteiro chegou ao fim: as 2 conferências passaram" if passou else "falhou no passo 6 (esperar h1.breadcrumb visível)",
                "mesmo_elemento": (mesmo if passou else None), "segundos": 1.2, "impressao": alvo["impressao"] if mesmo else {**alvo["impressao"], "data_nome": "x"}}

    r = cs.escolher(cands, lambda c: resolucoes[c["estrategia"]], reexecutar, {**alvo, "nome": "Entrar"})
    dados_cura = cs.evento_de_cura(r, alvo, localizador=alvo["seletor"], passo=5, erro="TimeoutError: waiting for locator", deteccao=TS, validacao="2026-10-26T20:00:04",
                                   mttr_s=3.8 if r["curado"] else None)
    s_cura = t.evento("cura", tid, dados_cura, "ao_vivo", pai=s_poda, ts=TS)
    no = cs.no_de_cura(r, seq_cura=s_cura, seq_poda=s_poda, justificativa=grr.justificativa_da_cura(dados_cura))
    t.decisao(tid, no, pai=s_cura, ts=TS)
    seqs = []
    if r["reexecucoes"]:
        for i, sel in enumerate(["admin/login.php", "#login_usuario", "#login_usuario", "#senha_usuario", r["aplicado"]["seletor"] if r["aplicado"] else "x", "h1.breadcrumb"]):
            t.evento("acao", tid, {"passo": i + 1, "acao": "esperar" if i == 5 else "clicar", "seletor": sel, "tempo_ms": 10.0, "falhou": False, "reexecucao": True, "curado": i == 4},
                     "ao_vivo", pai=s_cura, ts=TS)
        seqs.append(t.evento("verificacao", tid, trilha._v("conferencia_do_roteiro", "área administrativa aberta", "confere" if curado else "nao_confere",
                                                        {"esperado": "texto", "observado": "Área Administrativa"}), "ao_vivo", pai=s_cura, ts=TS))
    t.decisao(tid, cs.no_de_reexecucao(r, seq_cura=s_cura, seqs_verificacoes=seqs), pai=s_cura, ts=TS)
    t.fechar(fim="2026-10-26T20:00:05")
    return t, tid, r


def teste_cura_na_trilha_v2_e_no_relatorio_lista_todos_os_candidatos():
    import cura_seletor as cs
    t, tid, r = _trilha_de_cura()
    nos = [e["dados"] for e in t.eventos if e["tipo"] == "decisao"]
    assert [n["decisao"] for n in nos] == ["cura", "reexecucao"], [n["decisao"] for n in nos]
    cura_, reex = nos
    assert cura_["escolha"] == "posicao_entre_irmaos" and [a["opcao"] for a in cura_["alternativas"]] == [c["estrategia"] for c in r["candidatos"] if c["gerado"]]
    assert cura_["divergencia"]["ha"] is True and "caminho_do_ancestral_com_id" in cura_["divergencia"]["detalhe"], cura_["divergencia"]
    assert cura_["contraste"] and "e não" in cura_["contraste"] and cura_["justificativa"] and grr.MARCA_DO_MOLDE not in cura_["justificativa"]
    assert cura_["resultado"] == "cura_aplicada" and cura_["falha"] is None and {e["papel"] for e in cura_["evidencia"]} == {"candidato_de_seletor", "arvore_podada"}
    assert cura_["prov"]["used"] == [c["estrategia"] for c in r["candidatos"] if c["gerado"]]
    assert trilha.exportar_nome_gen_ai("cura") == "execute_tool"
    assert reex["escolha"] == "validada" and reex["divergencia"]["ha"] is False and reex["resultado"] == "roteiro_concluido" and reex["falha"] is None
    ev = next(e["dados"] for e in t.eventos if e["tipo"] == "cura")
    assert ev["curado"] is True and ev["aplicado"]["seletor"] == r["aplicado"]["seletor"] and ev["mttr_s"] == 3.8 and len(ev["candidatos"]) == 6
    assert ev["limiar_nome"] == cs.LIMIAR_NOME and ev["mesmo_elemento"] is True
    md = grr.relatorio_do_caso_v2(t.eventos, tid, comando_reexecucao="python executar_fase4.py --modo cura --roteiros front-admin-login --modos texto_alterado")
    assert "Cura de seletor" in md and "## 1. Veredito" in md
    for e in cs.ESTRATEGIAS:
        assert f"`{e}`" in md, e
    assert r["aplicado"]["seletor"] in md and "mesmo elemento" in md.lower() and "não confere" in md and "não gerado" in md
    assert "Sugestão" in md and "o agente não altera a aplicação" in md
    assert "--modos texto_alterado" in md and "gerada por molde" in md
    assert md.index("## 1. Veredito") < md.index("## 2. Evidência") < md.index("## 3. Contraste") < md.index("## 5. Linha de ação")
    # outro elemento fez o roteiro passar: a reexecução registra a divergência (regra R3)
    t2, tid2, r2 = _trilha_de_cura(curado=True, mesmo=False)
    reex2 = [e["dados"] for e in t2.eventos if e["tipo"] == "decisao"][1]
    assert reex2["divergencia"]["ha"] is True and "outro elemento" in reex2["divergencia"]["detalhe"]
    assert "outro elemento" in grr.relatorio_do_caso_v2(t2.eventos, tid2)
    # sem cura: o nó diz a falha da taxonomia e o relatório diz que não houve cura
    t3, tid3, r3 = _trilha_de_cura(curado=False)
    cura3, reex3 = [e["dados"] for e in t3.eventos if e["tipo"] == "decisao"]
    assert cura3["escolha"] == "nenhuma" and cura3["falha"] == "reexecucao_falhou" and reex3["escolha"] == "falhou" and reex3["falha"] == "reexecucao_falhou"
    md3 = grr.relatorio_do_caso_v2(t3.eventos, tid3)
    assert "não curado" in md3.lower() or "sem cura" in md3.lower()
    assert grr.justificativa_da_cura(next(e["dados"] for e in t3.eventos if e["tipo"] == "cura")).startswith("O passo 5")


HTML_LOGIN_DE_TESTE = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Chuleta Quente - Login</title></head>
<body class="fundofixo"><div class="login-container"><div class="login-form">
<form action="login.php" method="POST">
<div class="input-group"><label for="login_usuario">Login</label><input type="text" name="login_usuario" id="login_usuario" required placeholder="Digite seu login."></div>
<div class="input-group"><label for="senha_usuario">Senha</label><input type="password" name="senha_usuario" id="senha_usuario" required placeholder="Digite sua senha."></div>
<button type="submit" class=" btn btn-primary">Entrar</button>
</form></div></div></body></html>"""


def _url_de_teste(html: str) -> str:
    """A página de teste como URL data: (o init script só roda numa navegação; set_content não serve)."""
    import urllib.parse
    return "data:text/html;charset=utf-8," + urllib.parse.quote(html)


def teste_catalogo_de_quebras_cobre_quatro_roteiros_e_quatro_modos_nas_duas_formas():
    import cenarios_fase4 as cen
    assert cen.MODOS_DE_QUEBRA == ("id_renomeado", "classe_trocada", "texto_alterado", "estrutura_alterada")
    assert cen.FORMAS_DE_QUEBRA == ("harness", "php") and cen.COOKIE_DA_QUEBRA == "quebra"
    assert cen.ROTEIROS_DA_CURA == ("front-busca", "front-admin-login", "front-admin-produtos", "front-cliente-reserva")
    assert cen.TEMPO_LIMITE_QUEBRA_MS == 5000
    assert len(cen.QUEBRAS) == 16 and {(q["cenario"], q["modo"]) for q in cen.QUEBRAS} == {(r, m) for r in cen.ROTEIROS_DA_CURA for m in cen.MODOS_DE_QUEBRA}
    assert cen.validar_quebras(cen.QUEBRAS, cen.CENARIOS) == [], cen.validar_quebras(cen.QUEBRAS, cen.CENARIOS)
    assert cen.validar_catalogo(cen.CENARIOS) == []
    for q in cen.QUEBRAS:
        c = cen.cenario(q["cenario"])
        assert any(p.get("seletor") == q["seletor_original"] for p in c["passos"]), q
        assert q["localizador"] and q["alvo"]["papel"] and q["alvo"]["nome"] and q["mutacoes"] and q["descricao"], q
        # a variante do PHP só altera a página da célula (o cookie `quebra_pagina`): o login do administrador, que os
        # roteiros de produtos e de reserva atravessam, não pode quebrar junto
        assert q["pagina"].endswith(".php") and "/" not in q["pagina"].strip("/")[:0] and not q["pagina"].startswith("/"), q["pagina"]
        assert all(m["op"] in cen.OPERACOES_DE_QUEBRA and m.get("seletor") for m in q["mutacoes"]), q["mutacoes"]
        novo = cen.cenario_com_localizador(c, q)
        trocados = [i for i, p in enumerate(novo["passos"]) if p.get("seletor") == q["localizador"]]
        assert trocados and all(novo["passos"][i].get("ate_ms") == cen.TEMPO_LIMITE_QUEBRA_MS for i in trocados), (q["cenario"], q["modo"], trocados)
        assert q["passo_alvo"] == trocados[0] and novo["passos"][q["passo_alvo"]]["seletor"] == q["localizador"]
        assert c["passos"][q["passo_alvo"]]["seletor"] == q["seletor_original"], "o passo do alvo é o primeiro que usa o seletor original"
        assert novo is not c and c["passos"][q["passo_alvo"]]["seletor"] == q["seletor_original"], "o catálogo não muda"
        js = cen.script_de_quebra(q["mutacoes"], q["modo"])
        assert "DOMContentLoaded" in js and all(m["seletor"] in js for m in q["mutacoes"]) and q["modo"] in js, q["modo"]
    assert cen.quebra("front-busca", "id_renomeado")["cenario"] == "front-busca"
    try:
        cen.quebra("front-busca", "x")
    except KeyError:
        pass
    else:
        raise AssertionError("modo desconhecido aceito")
    # cada modo quebra o localizador pelo lado que ele ataca: id, classe, texto, estrutura
    for q in cen.QUEBRAS:
        ops = {m["op"] for m in q["mutacoes"]}
        esperado = {"id_renomeado": {"renomear_id", "renomear_atributo"}, "classe_trocada": {"trocar_classe"}, "texto_alterado": {"trocar_texto", "trocar_atributo"},
                    "estrutura_alterada": {"envolver_e_mover"}}[q["modo"]]
        assert ops <= esperado and ops, (q["cenario"], q["modo"], ops)
    # o roteiro da lista de produtos abre o modal de exclusão e nunca confirma
    prod = cen.cenario("front-admin-produtos")
    assert any(p.get("acao") == "esperar" and p.get("seletor") == "#modalEdit" for p in prod["passos"]), prod["passos"]
    assert any(p.get("acao") == "clicar" and "data-id" in str(p.get("seletor")) for p in prod["passos"])
    assert not any("delete-yes" in str(p.get("seletor")) for p in prod["passos"]), "nunca confirma a exclusão"
    assert cen.cenario("front-admin-produtos")["alvo"]["nome"] == "EXCLUIR"
    # a variante do front PHP: mesma quebra, ligada só por parâmetro de URL ou cookie, desligada por padrão
    front = RAIZ / "Programacao" / "CobaiaFront"
    quebra_php = front / "quebra.php"
    assert quebra_php.exists(), "a variante de quebra do front (ficha 29 c) vive em quebra.php"
    texto = quebra_php.read_text(encoding="utf-8")
    assert "$_GET['quebra']" in texto and "$_COOKIE['quebra']" in texto and all(m in texto for m in cen.MODOS_DE_QUEBRA), "modos e gatilhos"
    assert "quebra_pagina" in texto and "SCRIPT_NAME" in texto, "o modo vale só na página da célula quando quebra_pagina vem junto"
    assert cen.COOKIE_DA_PAGINA == "quebra_pagina"
    assert {q["pagina"] for q in cen.QUEBRAS} == {"index.php", "admin/login.php", "admin/produtos_lista.php", "cliente/index.php"}
    assert "de IA - Revisar" in texto and "! Motivo:" in texto and "return ''" in texto, "desligada por padrão"
    paginas = ("menu_publico.php", "admin/login.php", "admin/produtos_lista.php", "cliente/registrar_reserva.php")
    for pagina in paginas:
        t = (front / pagina).read_text(encoding="utf-8")
        assert "quebra.php" in t and "quebra_" in t and "de IA - Revisar" in t, pagina
    if _shutil.which("php"):
        for arq in [quebra_php] + [front / p for p in paginas]:
            r = _subprocess.run(["php", "-l", str(arq)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
            assert "No syntax errors" in r.stdout, (arq, r.stdout, r.stderr)
    else:
        print("  (pulado com aviso: php não está no PATH; a sintaxe da variante do front não foi conferida)")


def teste_quebra_armada_pelo_harness_e_deterministica():
    """A mesma página, com a mesma quebra armada duas vezes, dá a mesma árvore de acessibilidade; cada modo muda (ou não)
    a árvore do jeito esperado. Precisa do Playwright (pulado com aviso fora da venv do AgenteCore); não precisa das cobaias."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  (pulado com aviso: o Playwright não está neste Python; rode com Programacao/AgenteCore/.venv/Scripts/python.exe)")
        return
    import cenarios_fase4 as cen
    arvores: dict[str, str] = {}
    aplicadas: dict[str, str] = {}
    with sync_playwright() as p:
        nav = p.chromium.launch(headless=True)
        try:
            for modo in cen.MODOS_DE_QUEBRA:
                q = cen.quebra("front-admin-login", modo)
                textos = []
                for _ in range(2):
                    pagina = nav.new_page()
                    cen.armar_quebra(pagina, q, "harness")
                    pagina.goto(_url_de_teste(HTML_LOGIN_DE_TESTE))
                    textos.append(pagina.locator("body").aria_snapshot())
                    aplicadas[modo] = pagina.evaluate("document.documentElement.dataset.quebraAplicada")
                    pagina.close()
                assert textos[0] == textos[1], (modo, textos)
                arvores[modo] = textos[0]
            pagina = nav.new_page()
            pagina.goto(_url_de_teste(HTML_LOGIN_DE_TESTE))
            normal = pagina.locator("body").aria_snapshot()
            assert pagina.evaluate("document.documentElement.dataset.quebraAplicada") is None, "sem quebra armada nada muda"
            pagina.close()
        finally:
            nav.close()
    assert all(aplicadas[m] == str(len(cen.quebra("front-admin-login", m)["mutacoes"])) for m in cen.MODOS_DE_QUEBRA), aplicadas
    assert 'button "Entrar"' in normal, normal
    assert 'button "Entrar agora"' in arvores["texto_alterado"] and 'button "Entrar"\n' not in arvores["texto_alterado"], arvores["texto_alterado"]
    assert arvores["id_renomeado"] == normal, "renomear o id (e o for do rótulo) não muda a árvore de acessibilidade"
    assert arvores["classe_trocada"] == normal, "trocar a classe não muda a árvore de acessibilidade"
    assert arvores["estrutura_alterada"] != normal and arvores["estrutura_alterada"].index('button "Entrar"') < arvores["estrutura_alterada"].index('textbox "Login"'), \
        "o botão envolvido foi movido para antes dos campos"


def teste_executar_fase4_modo_cura_partes_puras():
    import cenarios_fase4 as cen
    import executar_fase4 as ex
    assert ex.MODOS == ("reproducao", "calibracao", "tela", "cura", "biblioteca")
    ap = ex.montar_parser()
    a = ap.parse_args(["--modo", "cura", "--saida", "x"])
    assert a.repeticoes == 5 and a.formas == "harness,php" and a.roteiros is None and a.modos is None
    assert ex.ler_lista("harness, php") == ["harness", "php"] and ex.ler_lista(None) == [] and ex.ler_lista("") == []
    celulas = ex.celulas_da_cura([], [], ["harness", "php"], 2)
    assert len(celulas) == 16 * 2 * 2 and celulas[0] == {"cenario": "front-busca", "modo": "id_renomeado", "forma": "harness", "repeticao": 1}
    assert celulas[1]["repeticao"] == 2 and celulas[2]["forma"] == "php", celulas[:4]
    assert [c["cenario"] for c in celulas][::16] == list(cen.ROTEIROS_DA_CURA)
    assert ex.celulas_da_cura(["front-busca"], ["texto_alterado"], ["php"], 1) == [{"cenario": "front-busca", "modo": "texto_alterado", "forma": "php", "repeticao": 1}]
    for ruim in (["x"], None):
        try:
            if ruim is None:
                ex.celulas_da_cura([], [], ["navegador"], 1)
            else:
                ex.celulas_da_cura(ruim, [], ["harness"], 1)
        except ValueError:
            pass
        else:
            raise AssertionError("roteiro ou forma desconhecidos aceitos")
    try:
        ex.celulas_da_cura([], [], ["harness"], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero repetições aceito")
    assert ex.mttr_da_cura(10.0, 13.5, descontar_s=1.0) == 2.5 and ex.mttr_da_cura(10.0, None) is None
    # a cura só roda quando o passo que falhou é um dos que usam o localizador da célula; falha em outro passo fica registrada
    q = cen.quebra("front-busca", "id_renomeado")
    roteiro = cen.cenario_com_localizador(cen.cenario("front-busca"), q)
    assert ex.falha_no_passo_do_alvo({"passou": False, "passo_falho": 1}, roteiro, q) is True
    assert ex.falha_no_passo_do_alvo({"passou": False, "passo_falho": 2}, roteiro, q) is True, "o segundo passo também usa #buscar"
    assert ex.falha_no_passo_do_alvo({"passou": False, "passo_falho": 0}, roteiro, q) is False, "abrir a página falhou: não é quebra de localizador"
    assert ex.falha_no_passo_do_alvo({"passou": True, "passo_falho": None}, roteiro, q) is False
    d = {"celula": {"cenario": "front-busca", "modo": "id_renomeado", "forma": "harness", "repeticao": 1}, "quebra": cen.quebra("front-busca", "id_renomeado"),
         "quebrou": True, "passo_falho": 1, "erro": "TimeoutError: x", "deteccao": "2026-11-01T10:00:00", "validacao": "2026-11-01T10:00:03",
         "escolha": {"curado": True, "aplicado": {"estrategia": "papel_e_nome", "seletor": 'role=searchbox[name="search"]'}, "reexecucoes": 1,
                     "mesmo_elemento": True, "falha": None, "resultado": "cura_aplicada", "segundo": None,
                     "candidatos": [{"estrategia": "papel_e_nome", "gerado": True, "seletor": "s", "passou_estaticas": True, "reexecutado": True, "aplicado": True,
                                     "efeito": {"resultado": "confere", "detalhe": "fim"}, "verificacoes": {"resolve_um_elemento": {"resultado": "confere"}}}]},
         "mttr_s": 2.5, "segundos_quebra": 5.4, "segundos_referencia": 1.1, "segundos_cura": 3.1, "arvore_sha": "abc", "arvore_podada_sha": "def", "incidentes": 0,
         "alvo": {"papel": "searchbox", "nome": "search", "impressao": {"tag": "input"}}, "segundos_restauracao": 0.0}
    reg = ex.registro_da_cura(d)
    assert reg["roteiro"] == "front-busca" and reg["modo"] == "id_renomeado" and reg["forma"] == "harness" and reg["repeticao"] == 1
    assert reg["curado"] is True and reg["aplicado"] == "papel_e_nome" and reg["seletor_curado"] == 'role=searchbox[name="search"]'
    assert reg["mesmo_elemento"] is True and reg["mttr_s"] == 2.5 and reg["quebrou"] is True and reg["localizador"] == "#buscar"
    assert reg["id"] == "front-busca/id_renomeado/harness/r1" and len(reg["candidatos"]) == 1 and reg["arvore_sha"] == "abc"


def _registros_de_cura_de_mentira() -> list[dict]:
    import cura_seletor as cs
    regs = []
    cenas = ("front-busca", "front-admin-login")
    modos = ("id_renomeado", "texto_alterado")
    for cena in cenas:
        for modo in modos:
            for forma in ("harness", "php"):
                for rep in (1, 2):
                    quebrou, aplicado, curado, mesmo = True, "papel_e_nome", True, True
                    if cena == "front-busca" and modo == "texto_alterado":
                        quebrou, aplicado, curado, mesmo = False, None, False, None     # o localizador sobreviveu à mutação
                    if cena == "front-admin-login" and modo == "texto_alterado":
                        aplicado = "papel_e_nome_parecido"
                        if forma == "php":
                            curado, mesmo = False, None                                   # ninguém levou o roteiro ao fim
                        elif rep == 2:
                            mesmo = False                                                 # outro elemento fez o roteiro passar
                    cands = [{"estrategia": e, "gerado": e != "data_id", "seletor": f"s:{e}", "passou_estaticas": e in (aplicado, "posicao_entre_irmaos"),
                              "reexecutado": e == aplicado or (e == "posicao_entre_irmaos" and aplicado is not None and not curado),
                              "efeito": {"resultado": "confere" if (e == aplicado and curado) else ("nao_confere" if e in (aplicado, "posicao_entre_irmaos") and aplicado and not curado else "nao_tentado")},
                              "aplicado": bool(e == aplicado and curado),
                              "verificacoes": None if e == "data_id" else {v: {"resultado": "confere" if e in (aplicado, "posicao_entre_irmaos") else "nao_confere"} for v in cs.VERIFICACOES[:4]}}
                             for e in cs.ESTRATEGIAS] if quebrou else []
                    regs.append({"id": f"{cena}/{modo}/{forma}/r{rep}", "roteiro": cena, "modo": modo, "forma": forma, "repeticao": rep, "localizador": "#x",
                                 "passo_alvo": 1, "quebrou": quebrou, "passo_falho": 1 if quebrou else None, "erro": "TimeoutError" if quebrou else None,
                                 "candidatos": cands, "aplicado": aplicado if curado else None, "seletor_curado": f"s:{aplicado}" if curado else None,
                                 "curado": curado, "mesmo_elemento": mesmo, "falha": None if curado or not quebrou else "reexecucao_falhou",
                                 "mttr_s": (2.0 + rep + (1.0 if forma == "php" else 0.0)) if curado else None, "reexecucoes": (2 if aplicado and not curado else 1) if quebrou else 0,
                                 "segundos_quebra": 6.0, "segundos_referencia": 1.0, "segundos_cura": 3.0, "arvore_sha": f"{cena}-{modo}" + ("-php" if forma == "php" and modo == "id_renomeado" and cena == "front-busca" else ""),
                                 "arvore_podada_sha": "p", "incidentes": 0, "alvo": {"papel": "button", "nome": "x"}})
    return regs


def teste_avaliar_fase4_cura_aplica_a_regra_r3_com_check():
    import avaliar_fase4 as av
    import pre_fase4 as pf
    regs = _registros_de_cura_de_mentira()
    condicoes = {"modo": "cura", "repeticoes": 2, "formas": ["harness", "php"], "limiar_nome": 0.6, "tempo_limite_ms": 5000}
    dado = av.resumir_cura(regs, condicoes, gerado_em="2026-11-01T18:00:00", corrida="fase4_cura")
    r = dado["resumo"]
    assert r["execucoes"] == 16 and r["quebras_detectadas"] == 12 and r["nao_quebrou"] == 4, r
    assert r["curadas"] == 10 and r["nao_curadas"] == 2 and r["taxa_de_cura_pct"] == 83.3, r
    assert r["mesmo_elemento"] == 9 and r["outro_elemento"] == 1, r
    assert r["mttr_mediana_s"] == 4.0 and r["mttr_min_s"] == 3.0 and r["mttr_max_s"] == 5.0, r
    assert r["reexecucoes_mediana"] == 1 and r["repeticoes"] == 2 and r["limiar_nome"] == 0.6
    por_modo = {x["modo"]: x for x in dado["por_modo"]}
    assert por_modo["id_renomeado"] == {"modo": "id_renomeado", "execucoes": 8, "quebrou": 8, "curadas": 8, "taxa_de_cura_pct": 100.0, "mesmo_elemento": 8, "outro_elemento": 0,
                                        "nao_curadas": 0, "nao_quebrou": 0, "mttr_mediana_s": 4.0, "mttr_max_s": 5.0, "estrategias_aplicadas": {"papel_e_nome": 8}}, por_modo["id_renomeado"]
    assert por_modo["texto_alterado"]["quebrou"] == 4 and por_modo["texto_alterado"]["curadas"] == 2 and por_modo["texto_alterado"]["outro_elemento"] == 1
    por_rot = {x["roteiro"]: x for x in dado["por_roteiro"]}
    assert por_rot["front-busca"]["nao_quebrou"] == 4 and por_rot["front-admin-login"]["nao_curadas"] == 2 and por_rot["front-admin-login"]["taxa_de_cura_pct"] == 75.0
    por_forma = {x["forma"]: x for x in dado["por_forma"]}
    assert por_forma["harness"]["curadas"] == 6 and por_forma["php"]["curadas"] == 4 and por_forma["php"]["mttr_mediana_s"] == 4.5, por_forma
    # as duas formas dão a mesma árvore quando o sha da página quebrada coincide célula a célula
    assert dado["formas"]["celulas_comparadas"] == 4 and dado["formas"]["arvore_igual"] == 3 and dado["formas"]["arvore_diferente"] == ["front-busca/id_renomeado"], dado["formas"]
    assert dado["formas"]["mesmo_resultado"] == 3, "em uma célula a forma php não curou e a harness curou"
    estr = {x["estrategia"]: x for x in dado["por_estrategia"]}
    assert estr["papel_e_nome"]["gerada"] == 12 and estr["papel_e_nome"]["passou_estaticas"] == 8 and estr["papel_e_nome"]["aplicada"] == 8
    assert estr["data_id"]["gerada"] == 0 and estr["posicao_entre_irmaos"]["reexecutada"] == 2 and estr["posicao_entre_irmaos"]["aplicada"] == 0
    assert estr["papel_e_nome_parecido"]["aplicada"] == 2 and estr["texto_contido"]["recusada_em"]["resolve_um_elemento"] == 12
    assert [x["id"] for x in dado["outro_elemento"]] == ["front-admin-login/texto_alterado/harness/r2"]
    assert [x["id"] for x in dado["nao_curadas"]] == ["front-admin-login/texto_alterado/php/r1", "front-admin-login/texto_alterado/php/r2"]
    assert len(dado["execucoes"]) == 16 and dado["execucoes"][0]["id"] == regs[0]["id"]
    assert dado["regra_r3"]["cumprida"] is True and "reexecução" in dado["regra_r3"]["texto"]
    md = av.render_cura(dado)
    for bloco in ("tb_f4_cura_resumo", "tb_f4_cura_por_modo", "tb_f4_cura_por_roteiro", "tb_f4_cura_por_forma", "tb_f4_cura_estrategias", "tb_f4_cura_outro_elemento",
                  "tb_f4_cura_nao_curadas", "tb_f4_cura_execucoes"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    assert "—" not in md and "→" not in md and "83,3" in md
    pasta = _temp()
    assert pf.fechar(av.NOME_CURA, dado, md, av.PREFIXO_CURA, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert pf.fechar(av.NOME_CURA, dado, md, av.PREFIXO_CURA, check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert av.NOME_CURA == "cura" and av.PREFIXO_CURA == "tb_f4_cura_" and av.TITULO_CURA == "Cura de seletor (corrida 19)"
    assert av.nome_dos_arquivos(None, "cura") == "cura" and av.nome_dos_arquivos("cura_fumaca", "cura") == "cura_fumaca"
    ap = av.montar_parser()
    assert ap.parse_args(["--cura", "--saida", "fase4_cura"]).cura is True
    vazio = av.resumir_cura([], condicoes, gerado_em="2026-11-01T18:00:00", corrida="x")
    assert vazio["resumo"]["execucoes"] == 0 and vazio["resumo"]["taxa_de_cura_pct"] is None and av.render_cura(vazio)


# ----------------------------------------------------------------------------- P5: biblioteca em produção e ciclo de correção

# ! Alteração de IA - Revisar: testes do pacote P5 (03/11/2026): biblioteca em produção e ciclo de correção, escritos antes do
# módulo `biblioteca_fase4.py`, do modo `biblioteca` de `executar_fase4.py`, de `avaliar_fase4.py --biblioteca`, da recuperação
# por id em `diagnostico_ao_vivo.py` e `sonda_correcao.py`, e das seções "Solução sugerida" e "Solução aplicada" em `biblioteca.py`.
# A primeira rodada falha por ModuleNotFoundError em `biblioteca_fase4` (o RED aceito para módulo novo) e por AssertionError nos
# módulos que já existem.
# ! Motivo: o plano aprovado (seção 5, P5) pede os testes antes: cada filtro em código recusa o exemplo mínimo que o motiva e
# aceita o contraexemplo; a operação "correção" nunca remove bytes e só avança o estado; o gatilho marca `corrigido` só com a
# evidência dos dois diffs; a recuperação por id traz as notas do caso e nada mais; a regra dos 40% manda para revisão a nota do
# verbete mais recuperado da calibração; um lote com c > b fica em espera; nenhum texto de corpo HTTP entra em proposta sem
# validação. Os números da calibração vêm dos registros oficiais da corrida 16 (`fase4_calibracao/k3`), nunca digitados à mão.

CASO_DE_TESTE_P5 = {"id": "sin-1", "classe": 2, "nivel": 1, "entrada": {"requisicao": "GET /api/produtos", "status": 200,
                                                                       "contrato": "id: inteiro | nome: texto | preco: numero",
                                                                       "corpo": '[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes"}]',
                                                                       "sintoma": "O botão do cartão mostra undefined no lugar do preço.",
                                                                       "observacao": "O campo preco não veio na resposta."},
                    "gabarito": {"causa_raiz": "campo_ausente", "campo_afetado": "preco", "termos_esperados": [], "termos_proibidos": []}}


def _copia_da_curada(pasta_bib: Path) -> Path:
    """`<pasta_bib>/epoca-100` = cópia fechada da L1 curada (hash conferido por executar_fase3b._preparar_copia)."""
    import diagnostico_ao_vivo as dv
    import executar_fase3b as e3b
    destino = pasta_bib / "epoca-100"
    e3b._preparar_copia(dv.PASTA_CURADA, destino)
    return destino


def teste_biblioteca_fase4_origem_estado_e_recuperacao_por_id():
    import biblioteca as bib
    import biblioteca_fase4 as bf
    import diagnostico_ao_vivo as dv
    import trilha as tr
    verbetes, indice = _curada()
    por_id = {v["id"]: v for v in verbetes}
    assert bf.ORIGENS == ("humano", "modelo", "sistema_sob_teste") and bf.ESTADOS == ("nao_corrigido", "corrigido")
    assert bf.origem_do_verbete(por_id["campo_ausente"]) == "humano" and bf.origem_do_verbete(por_id["atualizacao_imediata"]) == "modelo"
    # o estado é lido do `status`: 'ativo' de um verbete com defeito documentado vale como não corrigido; 'corrigido' só depois da correção
    assert bf.estado_do_verbete(por_id["campo_ausente"]) == "nao_corrigido"
    assert bf.estado_do_verbete({"meta": {"status": "corrigido"}, "secoes": {}}) == "corrigido"
    # os casos ligados a um verbete: pelas notas `[E1 · caso · …]` e, nos verbetes escritos pelo modelo, pelo caso de origem do comentário
    assert bf.casos_do_verbete(por_id["campo_ausente"]) == ["sin-1"]
    assert bf.casos_do_verbete(por_id["interface-frontend"]) == ["efe-10"], bf.casos_do_verbete(por_id["interface-frontend"])
    assert bf.casos_do_verbete(por_id["corpo_vazio"]) == ["lex-13"], "o mesmo caso duas vezes conta uma vez"
    assert bf.casos_do_verbete(por_id["contrato-pedido"]) == []
    # a recuperação por id traz as notas do caso e nada mais
    assert [v["id"] for v in bf.verbetes_do_caso(verbetes, "sin-1")] == ["campo_ausente"]
    assert sorted(v["id"] for v in bf.verbetes_do_caso(verbetes, "lex-5")) == ["contrato-produto", "resposta_truncada"]
    assert [v["id"] for v in bf.verbetes_do_caso(verbetes, "efe-10")] == ["interface-frontend"]
    assert bf.verbetes_do_caso(verbetes, "efe-3") == [] and bf.verbetes_do_caso(verbetes, "lex-1") == []
    notas = bf.notas_do_caso(verbetes, "lex-5")
    assert len(notas) == 2 and {n["verbete"] for n in notas} == {"contrato-produto", "resposta_truncada"} and all(n["caso"] == "lex-5" for n in notas)
    assert all(n["caso"] == "sin-1" for n in bf.notas_do_caso(verbetes, "sin-1")) and len(bf.notas_do_caso(verbetes, "sin-1")) == 1
    assert bf.sugestao_do_modelo(por_id["campo_ausente"], "sin-1").startswith("Adicionar nota sobre a remoção de campos")
    assert bf.sugestao_do_modelo(por_id["interface-frontend"], "efe-10") == por_id["interface-frontend"]["secoes"]["Resumo"].replace("\n", " ")
    assert bf.sugestao_do_modelo(por_id["campo_ausente"], "lex-1") == ""
    # o contexto com id: os k da busca na frente, os do id depois, sem repetição; o prompt continua repartível (prompt fixo intacto)
    caso = dict(CASO_DE_TESTE_P5)
    ctx = bf.contexto_com_id(verbetes, indice, caso, 3)
    base = dv.contexto_ao_vivo(verbetes, indice, caso, 3)
    assert ctx["verbetes_ids"][:3] == base["verbetes_ids"] and ctx["verbete_ouro"] is None and ctx["causa_plantada"] is None
    assert "campo_ausente" in ctx["verbetes_ids"] and ctx["por_id"] == [i for i in ["campo_ausente"] if i not in base["verbetes_ids"]]
    assert len(ctx["verbetes_ids"]) == len(set(ctx["verbetes_ids"]))
    ctx2, prompt2 = dv.montar_prompt(verbetes, indice, caso, 3, extras=bf.verbetes_do_caso(verbetes, "sin-1"))
    assert ctx2["verbetes_ids"] == ctx["verbetes_ids"] and ctx2["texto"] == ctx["texto"]
    partes = tr.partes_do_prompt(verbetes, ctx2, caso, prompt2)
    assert [p["id"] for p in partes if p["papel"] == "verbete"] == ctx2["verbetes_ids"]
    assert dv.hash_prompt_fixo(verbetes, ctx2, caso, prompt2) == dv.hash_prompt_fixo(verbetes, base, caso, dv.montar_prompt(verbetes, indice, caso, 3)[1])
    sem = bf.contexto_com_id(verbetes, indice, {**caso, "id": "lex-1"}, 3)
    assert sem["por_id"] == [] and sem["verbetes_ids"] == dv.contexto_ao_vivo(verbetes, indice, {**caso, "id": "lex-1"}, 3)["verbetes_ids"]
    # as seções da correção são aceitas pelo validador da biblioteca e renderizadas só quando existem
    assert "Solução sugerida" in bib.SECOES and "Solução aplicada" in bib.SECOES
    assert bib.render_correcoes(por_id["campo_ausente"]) == "" and bib.render(por_id["campo_ausente"]) == bib.render_base(por_id["campo_ausente"]) + bib.render_notas(por_id["campo_ausente"])


def teste_biblioteca_fase4_cada_filtro_recusa_o_exemplo_minimo_e_aceita_o_contraexemplo():
    import biblioteca as bib
    import biblioteca_fase4 as bf
    verbetes, _ = _curada()
    por_id = {v["id"]: v for v in verbetes}
    assert bf.FILTROS == ("evidencia_obrigatoria", "atomicidade", "abstencao_valida", "fonte_confiavel", "granularidade", "peso_por_tipo",
                          "redundancia", "proveniencia", "auditoria_por_etapa", "conflito_deterministico", "metricas_por_rodada",
                          "revisao_humana_amostral", "regra_dos_40"), "os 13 filtros em código da decisão 65, na ordem do plano"
    caso = dict(CASO_DE_TESTE_P5)
    termos = bf.termos_de_evidencia(caso)
    assert {"preco", "200", "undefined"} <= termos and "api" not in termos, termos
    # 1. evidência obrigatória: o MOTIVO cita a evidência do caso
    assert bf.filtro_evidencia_obrigatoria({"OPERACAO": "nota", "MOTIVO": "Para enriquecer a documentação do sistema."}, caso)["codigo"] == "sem_evidencia_do_caso"
    assert bf.filtro_evidencia_obrigatoria({"OPERACAO": "nota", "MOTIVO": "O corpo veio sem a chave preco e o botão mostrou undefined."}, caso) is None
    assert bf.filtro_evidencia_obrigatoria({"OPERACAO": "retificacao", "TRECHO": "curto", "MOTIVO": "o campo preco sumiu"}, caso)["codigo"] == "sem_evidencia_do_caso"
    # 2. atomicidade: uma alegação curta, sem lista
    assert bf.filtro_atomicidade({"TEXTO": "O campo some. O botão quebra. A tela fica em branco e o log cresce."})["codigo"] == "texto_nao_atomico"
    assert bf.filtro_atomicidade({"TEXTO": "Primeiro: a; segundo: b; terceiro: c, tudo junto numa frase só de enumeração."})["codigo"] == "texto_nao_atomico"
    assert bf.filtro_atomicidade({"TEXTO": "Quando o campo preco falta, o botão imprime undefined. Conferir o modo field_missing."}) is None
    # 3. abstenção válida: NENHUMA é saída válida e contada à parte; resposta sem bloco e sem NENHUMA continua sem_bloco
    import evolucao_biblioteca as evo
    assert bf.classificar_resposta(evo.parsear_propostas("NENHUMA")) == "abstencao"
    assert bf.classificar_resposta(evo.parsear_propostas("não sei")) == "sem_bloco"
    assert bf.classificar_resposta(evo.parsear_propostas("PROPOSTA 1\nOPERACAO: nota\nVERBETE: [x]\nTEXTO: t\nMOTIVO: m\nFIM")) == "propostas"
    # 4. fonte confiável: mensagem de erro entre aspas e endpoint conferidos contra o código das cobaias e o openapi.json
    fontes = bf.fontes_das_cobaias()
    rotas = bf.rotas_do_openapi()
    assert "GET /api/produtos/{id}" in rotas and "GET /api/produtos" in rotas, rotas
    assert bf.filtro_fonte_confiavel({"TEXTO": 'A API responde "Produto nao localizado na base" quando o id não existe.'}, fontes, rotas)["codigo"] == "mensagem_nao_encontrada_no_codigo"
    assert bf.filtro_fonte_confiavel({"TEXTO": 'A API responde "Produto não encontrado" quando o id não existe.'}, fontes, rotas) is None
    assert bf.filtro_fonte_confiavel({"TEXTO": "A rota GET /api/produtos/99/detalhe não existe no serviço."}, fontes, rotas)["codigo"] == "endpoint_fora_do_openapi"
    assert bf.filtro_fonte_confiavel({"TEXTO": "A rota GET /api/produtos/99 devolve 404 quando o id não existe."}, fontes, rotas) is None
    # 5. granularidade: retificar (propõe texto) ou sinalizar (só aponta); sinalização sem trecho específico é recusada
    alvo = por_id["campo_ausente"]
    resumo = alvo["secoes"]["Resumo"]
    assert bf.granularidade({"OPERACAO": "retificacao", "TEXTO": "Este trecho pode estar desatualizado; verificar se ainda vale."}) == "sinalizar"
    assert bf.granularidade({"OPERACAO": "retificacao", "TEXTO": "O modo field_missing remove o campo-alvo e nenhuma chave nova aparece."}) == "retificar"
    assert bf.granularidade({"OPERACAO": "nota", "TEXTO": "x"}) is None
    assert bf.filtro_granularidade({"OPERACAO": "retificacao", "TRECHO": resumo, "TEXTO": "Este trecho pode estar desatualizado; verificar."}, alvo)["codigo"] == "sinalizacao_sem_trecho"
    assert bf.filtro_granularidade({"OPERACAO": "retificacao", "TRECHO": "nem com nulo", "TEXTO": "Este trecho pode estar desatualizado; verificar."}, alvo) is None
    # 6. peso por tipo de edição: nota 1, sinalização 1, retificação 2, verbete novo 3; orçamento por verbete e rodada
    assert bf.PESO_POR_TIPO == {"nota": 1, "sinalizacao": 1, "retificacao": 2, "novo_verbete": 3} and bf.ORCAMENTO_DE_PESO_POR_VERBETE == 4
    assert bf.peso_da_edicao("retificacao", "sinalizar") == 1 and bf.peso_da_edicao("retificacao", "retificar") == 2 and bf.peso_da_edicao("novo_verbete", None) == 3
    assert bf.filtro_peso_por_tipo("retificacao", "retificar", "campo_ausente", {"campo_ausente": 3})["codigo"] == "peso_acima_do_orcamento"
    assert bf.filtro_peso_por_tipo("nota", None, "campo_ausente", {"campo_ausente": 3}) is None
    # 7. redundância por n-gramas: paráfrase de uma nota existente é recusada; texto novo entra
    nota_existente = bib.notas(alvo)[0]["texto"]
    assert bf.similaridade_ngramas(nota_existente, bib.render(alvo)) == 1.0 and bf.similaridade_ngramas("nada a ver com isso aqui", bib.render(alvo)) == 0.0
    assert bf.filtro_redundancia({"TEXTO": nota_existente.replace("Adicionar", "Incluir")}, alvo)["codigo"] == "redundante"
    assert bf.filtro_redundancia({"TEXTO": "Quando o campo preco falta, o botão imprime undefined. Conferir o modo field_missing."}, alvo) is None
    # 8. proveniência por edição: caso de origem, modelo e época; sem caso, recusada
    edicao = {"caso": "sin-1", "modelo": "qwen2.5:7b", "epoca": 101, "operacao": "nota", "verbete": "campo_ausente"}
    assert bf.filtro_proveniencia({**edicao, "caso": None}, {"sin-1"})["codigo"] == "sem_proveniencia"
    assert bf.filtro_proveniencia({**edicao, "caso": "lex-9"}, {"sin-1"})["codigo"] == "sem_proveniencia"
    assert bf.filtro_proveniencia(edicao, {"sin-1"}) is None
    prov = bf.proveniencia(edicao, "2026-11-03")
    assert prov == {"origem": "modelo", "caso": "sin-1", "modelo": "qwen2.5:7b", "epoca": 101, "data": "2026-11-03"}
    # 9. auditoria por etapa: admissão e atualização separadas; proposta sobre caso já corrigido no verbete é recusada
    assert bf.filtro_auditoria_por_etapa("campo_ausente", "sin-1", {"campo_ausente": ["sin-1"]})["codigo"] == "proposta_sobre_caso_corrigido"
    assert bf.filtro_auditoria_por_etapa("campo_ausente", "sin-1", {"campo_renomeado": ["sin-9"]}) is None
    aud = bf.auditoria(verbetes, {"campo_ausente": ["sin-1"]}, [{"verbete": "corpo_vazio", "caso": "lex-13"}])
    assert aud["admissao"] == [{"verbete": "corpo_vazio", "caso": "lex-13"}] and [a["verbete"] for a in aud["atualizacao"]] == ["campo_ausente"]
    assert aud["atualizacao"][0]["casos_corrigidos"] == ["sin-1"] and aud["atualizacao"][0]["notas_do_caso"] == 1
    # 10. resolução determinística de conflito: duas retificações do mesmo trecho que se contradizem; a de correção vence, depois a mais recente
    a = {"verbete": "campo_ausente", "operacao": "retificacao", "trecho": "nem com nulo", "texto": "vem com nulo", "data": "2026-11-01", "ordem": 1, "evidencia": "retificacao"}
    b = {"verbete": "campo_ausente", "operacao": "retificacao", "trecho": "Nem com nulo", "texto": "vem vazio", "data": "2026-11-03", "ordem": 2, "evidencia": "retificacao"}
    c = {"verbete": "campo_ausente", "operacao": "retificacao", "trecho": "nem com nulo", "texto": "vem com nulo", "data": "2026-11-02", "ordem": 3, "evidencia": "correcao"}
    d = {"verbete": "corpo_vazio", "operacao": "nota", "trecho": None, "texto": "outra", "data": "2026-11-03", "ordem": 4, "evidencia": "nota"}
    res = bf.resolver_conflito([a, b, c, d])
    assert [r["ordem"] for r in res if r["prevalece"]] == [3, 4] and [r["ordem"] for r in res if r.get("codigo") == "superada_por_conflito"] == [1, 2]
    assert bf.resolver_conflito([a, b])[1]["prevalece"] is True, "sem evidência de correção vence a mais recente"
    assert all(r["prevalece"] for r in bf.resolver_conflito([a, d]))
    # 11. métricas por rodada, sem intervenção humana
    regs = [{"caso": "sin-1", "abstencao": False, "decisoes": [{"aceita": True, "motivo": None, "edicao": {"operacao": "nota"}, "filtro": None, "peso": 1},
                                                              {"aceita": False, "motivo": "para_revisao_humana", "edicao": {"operacao": "nota"}, "filtro": "regra_dos_40", "peso": 1}]},
            {"caso": "lex-2", "abstencao": True, "decisoes": []},
            {"caso": "lex-9", "abstencao": False, "decisoes": [{"aceita": False, "motivo": "redundante", "edicao": None, "filtro": "redundancia", "peso": None},
                                                              {"aceita": False, "motivo": "texto_curto", "edicao": None, "filtro": None, "peso": None}]}]
    m = bf.metricas_da_rodada(regs)
    assert m["casos"] == 3 and m["abstencoes"] == 1 and m["propostas"] == 4 and m["aceitas"] == 1 and m["para_revisao"] == 1
    assert m["recusadas_fase3"] == {"texto_curto": 1} and m["recusadas_p5"] == {"redundante": 1} and m["por_filtro"]["redundancia"] == 1 and m["por_filtro"]["regra_dos_40"] == 1
    assert m["aceitas_por_tipo"] == {"nota": 1} and m["peso_aceito"] == 1 and m["taxa_de_rejeicao_pct"] == 50.0
    # 12. revisão humana amostral dirigida: primeiro o que a regra dos 40% segurou, depois o maior peso, depois o verbete mais recuperado
    edicoes = [{"verbete": "corpo_vazio", "operacao": "nota", "peso": 1, "para_revisao": False}, {"verbete": "entidade-produto", "operacao": "nota", "peso": 1, "para_revisao": True},
               {"verbete": "campo_ausente", "operacao": "retificacao", "peso": 2, "para_revisao": False}, {"verbete": "contrato-pedido", "operacao": "nota", "peso": 1, "para_revisao": False}]
    amostra = bf.amostra_para_revisao(edicoes, {"entidade-produto": .47, "contrato-pedido": .26, "corpo_vazio": .02}, n=3)
    assert [e["verbete"] for e in amostra] == ["entidade-produto", "campo_ausente", "contrato-pedido"], [e["verbete"] for e in amostra]
    planilha = bf.planilha_de_revisao(edicoes, {"entidade-produto": .47}, "fase4_biblioteca")
    assert "| # |" in planilha and "entidade-produto" in planilha and "—" not in planilha and "→" not in planilha
    assert bf.revisao_preenchida(planilha) is False and bf.revisao_preenchida(planilha.replace("| (em branco) |", "| Correta |")) is True
    # 13. regra dos 40%: verbete em 40% ou mais dos contextos da calibração manda a nota para revisão humana antes de entrar
    assert bf.filtro_regra_dos_40("entidade-produto", {"entidade-produto": .467, "corpo_vazio": .02})["codigo"] == "para_revisao_humana"
    assert bf.filtro_regra_dos_40("corpo_vazio", {"entidade-produto": .467, "corpo_vazio": .02}) is None
    assert bf.filtro_regra_dos_40("verbete-novo", {}) is None
    # nenhum texto vindo de resposta HTTP entra sem validação: um trecho literal do corpo com 20 caracteres ou mais é barrado
    corpo = caso["entrada"]["corpo"]
    assert bf.filtro_texto_de_origem_proibida({"TEXTO": 'O catálogo devolve "nome": "Picanha ao Alho", "resumo": "Picanha grelhada" e por isso o cartão quebra.'}, corpo)["codigo"] == "texto_de_origem_proibida"
    assert bf.filtro_texto_de_origem_proibida({"TEXTO": "O catálogo devolve o nome e o resumo do produto, mas sem o preço, e por isso o cartão quebra."}, corpo) is None
    assert bf.filtro_texto_de_origem_proibida({"TEXTO": "qualquer coisa"}, None) is None
    # o aplicador dos filtros na ordem fixa: a primeira recusa decide; o que passa leva granularidade, peso e a marca de revisão
    campos_ok = {"OPERACAO": "nota", "VERBETE": "campo_ausente", "TEXTO": "Quando o campo preco falta, o botão imprime undefined. Conferir o modo field_missing.",
                 "MOTIVO": "O corpo veio sem a chave preco e o botão mostrou undefined."}
    ctx_f = {"parcelas": {"entidade-produto": .467}, "corpo_http": corpo, "corrigidos": {}, "pesos_usados": {}, "casos_da_rodada": {"sin-1"},
             "fontes": fontes, "rotas": rotas}
    v = bf.filtrar_proposta(campos_ok, {**edicao, "texto": campos_ok["TEXTO"]}, caso, alvo, ctx_f)
    assert v == {"aceita": True, "codigo": None, "filtro": None, "detalhe": None, "granularidade": None, "peso": 1, "para_revisao": False}, v
    v2 = bf.filtrar_proposta({**campos_ok, "VERBETE": "entidade-produto"}, {**edicao, "verbete": "entidade-produto", "texto": campos_ok["TEXTO"]}, caso, por_id["entidade-produto"], ctx_f)
    assert v2["aceita"] is True and v2["para_revisao"] is True and v2["filtro"] == "regra_dos_40" and v2["codigo"] == "para_revisao_humana"
    v3 = bf.filtrar_proposta({**campos_ok, "MOTIVO": "para melhorar"}, {**edicao, "texto": campos_ok["TEXTO"]}, caso, alvo, ctx_f)
    assert v3["aceita"] is False and v3["filtro"] == "evidencia_obrigatoria" and v3["codigo"] == "sem_evidencia_do_caso"
    assert set(bf.CODIGOS_P5) >= {"sem_evidencia_do_caso", "texto_nao_atomico", "mensagem_nao_encontrada_no_codigo", "endpoint_fora_do_openapi", "sinalizacao_sem_trecho",
                                  "peso_acima_do_orcamento", "redundante", "sem_proveniencia", "proposta_sobre_caso_corrigido", "superada_por_conflito",
                                  "texto_de_origem_proibida", "para_revisao_humana"}


def teste_biblioteca_fase4_regra_dos_40_manda_para_revisao_o_verbete_mais_recuperado_da_calibracao():
    """Os contextos reais da corrida 16 (k = 3, o k escolhido pela regra R8): a parcela de contextos em que cada verbete entrou."""
    import biblioteca_fase4 as bf
    import executar_bateria
    arq = RA / "fase4_calibracao" / "k3" / "qwen2.5_7b" / "diagnosticos__L100.jsonl"
    if not arq.exists():
        print("  (pulado com aviso: sem os registros da corrida 16 nesta máquina)")
        return
    regs = executar_bateria.ler_jsonl(arq)
    parcelas = bf.parcela_nos_contextos(regs)
    assert len(regs) == 90 and abs(sum(parcelas.values()) - 3.0) < 1e-9, "k = 3 verbetes por contexto"
    mais = max(parcelas, key=parcelas.get)
    assert parcelas[mais] >= bf.PARCELA_PARA_REVISAO
    revisao = bf.verbetes_para_revisao(parcelas)
    assert revisao[0] == mais and all(parcelas[v] >= 0.4 for v in revisao) and all(parcelas[v] < 0.4 for v in parcelas if v not in revisao)
    assert bf.filtro_regra_dos_40(mais, parcelas)["codigo"] == "para_revisao_humana"
    raro = min(parcelas, key=parcelas.get)
    assert bf.filtro_regra_dos_40(raro, parcelas) is None
    # os quatro verbetes aprendidos nunca entraram num contexto da calibração com k = 3 (ficha 32): a medida que decide a pasta de espera
    import biblioteca as bib
    import diagnostico_ao_vivo as dv
    aprendidos = [v["id"] for v in bib.carregar(dv.PASTA_CURADA) if v["pasta"] == "aprendidos"]
    rec = bf.recuperacao_dos_aprendidos(regs, aprendidos)
    assert set(rec) == set(aprendidos) and all(isinstance(n, int) for n in rec.values())
    assert bf.aprendidos_sem_recuperacao(rec) == sorted(a for a in aprendidos if rec[a] == 0)


def _biblioteca_de_teste() -> tuple[Path, Path]:
    """Uma cópia da L1 curada numa pasta temporária (epoca-100 fechada) e a pasta pai."""
    pasta_bib = _temp() / "bibliotecas" / "qwen2.5_7b"
    pasta_bib.mkdir(parents=True)
    return pasta_bib, _copia_da_curada(pasta_bib)


def teste_biblioteca_fase4_correcao_nunca_remove_bytes_e_so_avanca_o_estado():
    import biblioteca as bib
    import biblioteca_fase4 as bf
    import evolucao_biblioteca as evo
    import executar_fase3b as e3b
    pasta_bib, antes = _biblioteca_de_teste()
    depois = pasta_bib / "epoca-102"
    evo.copiar_biblioteca(antes, depois)
    evo._limpar_gerados(depois)
    arq = depois / "erros" / "campo_ausente.md"
    texto_antes = arq.read_text(encoding="utf-8")
    sugerida = bf.sugestao_do_modelo(next(v for v in bib.carregar(antes) if v["id"] == "campo_ausente"), "sin-1")
    aplicada = "Em 03/11/2026 o cenário api-catalogo voltou a passar com o modo field_missing desligado: o corpo de GET /api/produtos voltou a trazer o campo preco."
    caminho = bf.corrigir(depois, "campo_ausente", "sin-1", sugerida, aplicada, "2026-11-03")
    assert caminho == arq
    texto_depois = arq.read_text(encoding="utf-8")
    corpo_antes = bib._parse_frontmatter(texto_antes)[1].rstrip("\n")
    meta_depois, corpo_depois = bib._parse_frontmatter(texto_depois)
    assert corpo_depois.startswith(corpo_antes), "o corpo antigo é prefixo do novo: nada foi removido"
    assert meta_depois["status"] == "corrigido" and "## Solução sugerida" in corpo_depois and "## Solução aplicada" in corpo_depois
    assert f"- [sin-1 · 2026-11-03] {sugerida}" in corpo_depois and f"- [sin-1 · 2026-11-03] {aplicada}" in corpo_depois
    assert "status avançou de ativo para corrigido" in texto_depois and "de IA - Revisar" in texto_depois
    # todas as linhas do arquivo antigo continuam no novo, na ordem (só a linha do status mudou de valor)
    linhas_antes = [l for l in texto_antes.splitlines() if not l.startswith("status:")]
    linhas_depois = texto_depois.splitlines()
    pos = -1
    for l in linhas_antes:
        pos = linhas_depois.index(l, pos + 1)
    v = next(x for x in bib.carregar(depois) if x["id"] == "campo_ausente")
    assert bf.estado_do_verbete(v) == "corrigido" and bf.casos_corrigidos(v) == ["sin-1"]
    r = bib.render_correcoes(v)
    assert r.startswith(" Correção") and sugerida[:30] in r and aplicada[:30] in r and "—" not in r and "→" not in r
    assert bib.render(v) == bib.render_base(v) + bib.render_notas(v) + r
    assert bib.validar(bib.carregar(depois), e3b.TODOS_OS_CASOS, teto_global=None) == [], "as seções novas são aceitas pelo validador"
    assert bf.conferir_correcao(antes, depois, {"campo_ausente": ["sin-1"]}) == []
    # o invariante de só acréscimo da Fase 3 continua valendo: tudo o que ele acusa, fora o avanço permitido do status, é violação
    assert any("'status' mudou" in x for x in evo.conferir_somente_acrescimo(antes, depois))
    # uma segunda correção no mesmo verbete (outro caso) acrescenta linhas e não repete o avanço do estado
    bf.corrigir(depois, "campo_ausente", "sin-2", "", "Em 03/11/2026 o cenário api-detalhe voltou a passar.", "2026-11-03")
    t2 = arq.read_text(encoding="utf-8")
    assert t2.count("## Solução aplicada") == 1 and "- [sin-2 · 2026-11-03] (sem nota do modelo para este caso)" in t2 and t2.count("status avançou") == 1
    assert bf.conferir_correcao(antes, depois, {"campo_ausente": ["sin-1", "sin-2"]}) == []
    # o estado só avança: voltar para 'ativo' é acusado; remover a nota apontada é acusado; corrigir um verbete obsoleto é recusado
    recuado = pasta_bib / "epoca-recuada"
    evo.copiar_biblioteca(depois, recuado)
    arq_r = recuado / "erros" / "campo_ausente.md"
    arq_r.write_text(arq_r.read_text(encoding="utf-8").replace("status: corrigido", "status: ativo"), encoding="utf-8")
    assert any("recuou" in x for x in bf.conferir_correcao(depois, recuado, {})), bf.conferir_correcao(depois, recuado, {})
    sem_nota = pasta_bib / "epoca-sem-nota"
    evo.copiar_biblioteca(depois, sem_nota)
    arq_s = sem_nota / "erros" / "campo_ausente.md"
    arq_s.write_text("\n".join(l for l in arq_s.read_text(encoding="utf-8").splitlines() if "[E1 · sin-1 · nota]" not in l) + "\n", encoding="utf-8")
    assert any("sumiu" in x or "removid" in x or "acréscimo" in x for x in bf.conferir_correcao(antes, sem_nota, {"campo_ausente": ["sin-1", "sin-2"]}))
    obsoleto = depois / "erros" / "corpo_vazio.md"
    texto_original = obsoleto.read_text(encoding="utf-8")
    obsoleto.write_text(texto_original.replace("status: ativo", "status: obsoleto"), encoding="utf-8")
    try:
        bf.corrigir(depois, "corpo_vazio", "lex-13", "x", "y", "2026-11-03")
    except ValueError:
        pass
    else:
        raise AssertionError("correção de verbete obsoleto aceita")
    obsoleto.write_text(texto_original, encoding="utf-8")     # a cópia volta ao que era: o fechamento abaixo confere só as correções
    # o teto das correções renderizadas vale no validador da biblioteca
    longa = "x" * (bf.TETO_CHARS_CORRECOES + 10)
    bf.corrigir(depois, "campo_renomeado", "sin-9", "", longa, "2026-11-03")
    problemas = bib.validar(bib.carregar(depois), e3b.TODOS_OS_CASOS, teto_global=None)
    assert any("campo_renomeado" in p and "correç" in p.lower() for p in problemas), problemas
    # fechar a época de correções: validação, invariante com o avanço permitido, índice, diff e fechamento.json
    arq_c = depois / "erros" / "campo_renomeado.md"
    arq_c.write_text(arq_c.read_text(encoding="utf-8").replace(longa, "curta"), encoding="utf-8")
    fechamento = bf.fechar_correcoes(pasta_bib, 102, "qwen2.5:7b", e3b.TODOS_OS_CASOS, {"campo_ausente": ["sin-1", "sin-2"], "campo_renomeado": ["sin-9"]},
                                      versao_ollama="0.40.2", anterior=100)
    assert fechamento["hash"] == evo.hash_biblioteca(depois) and evo.snapshot_fechado(depois) and (pasta_bib / "diff__E102.md").exists()
    assert fechamento["n_verbetes"] == 40 and fechamento["correcoes"] == 3 and (depois / "INDICE.md").exists()


def teste_biblioteca_fase4_gatilho_marca_corrigido_so_com_os_dois_diffs():
    import biblioteca_fase4 as bf
    contrato = "id: inteiro | nome: texto | preco: numero"
    arvore_quebrada = 'document "Catálogo"\n  main\n    button "Saiba Mais..." data-id="1"\n'
    arvore_boa = 'document "Catálogo"\n  main\n    button "Saiba Mais..." data-id="1"\n    button "Saiba Mais..." data-id="2"\n    text "R$ 89,90"\n'
    corpo_quebrado = '[{"id": 1, "nome": "Picanha ao Alho"}, {"id": 2, "nome": "Costela"}]'
    corpo_bom = '[{"id": 1, "nome": "Picanha ao Alho", "preco": 89.9}, {"id": 2, "nome": "Costela", "preco": 59.9}]'
    antes = {"passou": False, "corpo": corpo_quebrado, "tempo_ms": 12.0, "arvore": arvore_quebrada,
             "conferencia_falha": {"nome": "preço no botão", "passou": False, "esperado": "R$", "observado": "undefined"}}
    depois = {"passou": True, "corpo": corpo_bom, "tempo_ms": 11.0, "arvore": arvore_boa, "conferencia_falha": None}
    ev = bf.evidencia_de_correcao(antes, depois, contrato)
    assert ev["passou_depois"] is True and ev["ha_diff_http"] is True and ev["ha_diff_arvore"] is True and ev["sintoma_sumiu"] is True
    assert ev["diff_http"]["diferencas_contrato_antes"] == 1 and ev["diff_http"]["diferencas_contrato_depois"] == 0 and ev["diff_http"]["campos_que_voltaram"] == ["preco"]
    assert ev["diff_arvore"]["a_mais"] == 2 and ev["diff_arvore"]["a_menos"] == 0
    d = bf.detectar_correcao(ev)
    assert d["corrigido"] is True and d["motivo"]
    # passou, mas nada mudou no fio: não marca
    ev2 = bf.evidencia_de_correcao({**antes, "corpo": corpo_bom}, depois, contrato)
    assert ev2["ha_diff_http"] is False and bf.detectar_correcao(ev2)["corrigido"] is False and "fio" in bf.detectar_correcao(ev2)["motivo"]
    # passou e o fio mudou, mas a árvore é a mesma: não marca
    ev3 = bf.evidencia_de_correcao({**antes, "arvore": arvore_boa}, depois, contrato)
    assert ev3["ha_diff_arvore"] is False and bf.detectar_correcao(ev3)["corrigido"] is False and "árvore" in bf.detectar_correcao(ev3)["motivo"]
    # o modo continua ligado: a reexecução ainda falha, nada a marcar
    ev4 = bf.evidencia_de_correcao(antes, {**antes, "tempo_ms": 13.0}, contrato)
    assert ev4["passou_depois"] is False and bf.detectar_correcao(ev4)["corrigido"] is False
    # a latência: o corpo é o mesmo, mas o tempo da chamada contra o orçamento conta como diferença no fio
    ev5 = bf.evidencia_de_correcao({**antes, "corpo": corpo_bom, "tempo_ms": 2100.0}, {**depois, "tempo_ms": 15.0}, contrato)
    assert ev5["ha_diff_http"] is True and ev5["diff_http"]["lento_antes"] is True and ev5["diff_http"]["lento_depois"] is False
    # a solução aplicada sai do molde: determinística, sem o nome da causa, sem travessão
    frase = bf.solucao_aplicada_por_molde("sin-1", "api-catalogo", "field_missing", ev, "2026-11-03")
    assert frase == bf.solucao_aplicada_por_molde("sin-1", "api-catalogo", "field_missing", ev, "2026-11-03")
    assert "2026-11-03" in frase and "api-catalogo" in frase and "field_missing" in frase and "preco" in frase and "campo_ausente" not in frase
    assert "—" not in frase and "→" not in frase and len(frase) <= bf.TETO_CHARS_CORRECOES
    # regra R4 sobre registros sintéticos: precisão e revocação da marca contra o conjunto desligado
    regs = [{"caso": "a", "desligado": True, "reproduziu_antes": True, "marcado": True}, {"caso": "b", "desligado": True, "reproduziu_antes": True, "marcado": False},
            {"caso": "c", "desligado": False, "reproduziu_antes": True, "marcado": False}, {"caso": "d", "desligado": False, "reproduziu_antes": True, "marcado": True},
            {"caso": "e", "desligado": True, "reproduziu_antes": False, "marcado": False}]
    r4 = bf.regra_r4(regs)
    assert r4 == {"universo": 4, "desligados": 2, "mantidos": 2, "marcados": 2, "acertos": 1, "falsos_positivos": 1, "perdidos": 1, "precisao_pct": 50.0,
                  "revocacao_pct": 50.0, "sem_sintoma_antes": ["e"], "kappa": 0.0}, r4


def teste_biblioteca_fase4_lote_com_c_maior_que_b_fica_em_espera():
    import biblioteca_fase4 as bf

    def reg(caso: str, causa: str, resposta: str) -> dict:
        return {"caso": caso, "gabarito": {"causa_raiz": causa, "campo_afetado": None}, "resposta": f"CAUSA_RAIZ: {resposta}\nCAMPO: nenhum\nIMPACTO: x.\nFONTE: nenhum"}

    base = [reg("a", "x", "x"), reg("b", "y", "z"), reg("c", "w", "w"), reg("d", "u", "u")]
    melhor = [reg("a", "x", "x"), reg("b", "y", "y"), reg("c", "w", "w"), reg("d", "u", "t")]      # b = 1 (b), c = 1 (d)
    pior = [reg("a", "x", "y"), reg("b", "y", "z"), reg("c", "w", "v"), reg("d", "u", "u")]        # b = 0, c = 2
    empate = bf.avaliar_lote(base, melhor)
    assert (empate["n"], empate["b"], empate["c"]) == (4, 1, 1) and empate["veredito"] == "aceito" and empate["ganhos"] == ["b"] and empate["perdas"] == ["d"]
    assert empate["acerto_base"] == 3 and empate["acerto_novo"] == 3 and 0 <= empate["p_mcnemar"] <= 1
    esp = bf.avaliar_lote(base, pior)
    assert esp["veredito"] == "em_espera" and (esp["b"], esp["c"]) == (0, 2) and "c = 2" in esp["motivo"] and "b = 0" in esp["motivo"]
    assert bf.avaliar_lote(base, base)["veredito"] == "aceito"
    assert bf.avaliar_lote(base, [reg("a", "x", "x")])["n"] == 1, "só os casos pareados contam"
    assert bf.REGRA_R5.startswith("um lote de acréscimos entra se")


def _proposta(numero: int, operacao: str, verbete: str, texto: str, motivo: str, trecho: str = "") -> str:
    campos = [f"PROPOSTA {numero}", f"OPERACAO: {operacao}", f"VERBETE: [{verbete}]"]
    if trecho:
        campos.append(f"TRECHO: {trecho}")
    campos += [f"TEXTO: {texto}", f"MOTIVO: {motivo}", "FIM"]
    return "\n".join(campos)


def teste_biblioteca_fase4_propor_p5_com_ollama_de_mentira_e_trilha_v2():
    import biblioteca as bib
    import biblioteca_fase4 as bf
    import diagnostico_ao_vivo as dv
    import evolucao_biblioteca as evo
    import executar_fase3
    import executar_fase3b as e3b
    import recuperacao as rec
    pasta_bib, leitura = _biblioteca_de_teste()
    raiz = evo.abrir_epoca(pasta_bib, 101, [])
    verbetes = bib.carregar(leitura)
    indice = rec.Indice(verbetes)
    por_id = {v["id"]: v for v in verbetes}
    caso = {**CASO_DE_TESTE_P5}
    extras = bf.verbetes_do_caso(verbetes, caso["id"])
    ctx, prompt_diag = dv.montar_prompt(verbetes, indice, caso, 3, extras=extras)
    resposta_diag = "O preço não veio.\nCAUSA_RAIZ: campo_ausente\nCAMPO: preco\nIMPACTO: o botão mostra undefined.\nFONTE: [campo_ausente]"
    registro_diag = {"caso": caso["id"], "resposta": resposta_diag, "verbetes_ids": ctx["verbetes_ids"]}
    texto_ok = "Quando o campo preco falta no catálogo, o botão do cartão imprime undefined; conferir o modo field_missing."
    motivo_ok = "O corpo veio sem a chave preco e o botão mostrou undefined."
    respostas = {
        "sin-1": _proposta(1, "nota", "campo_ausente", texto_ok, motivo_ok) + "\n\n" + _proposta(2, "nota", "entidade-produto", texto_ok.replace("catálogo", "grid"), motivo_ok),
        "lex-9": _proposta(1, "nota", "corpo_nao_e_json", 'O catálogo devolve "nome": "Picanha ao Alho", "resumo": "Picanha grelhada" quando o corpo vem cortado pela metade.',
                           "O corpo veio sem a chave preco e com status 200."),
        "lex-2": "NENHUMA",
    }
    chamadas: list = []
    fila = [respostas["sin-1"], respostas["lex-9"], respostas["lex-2"]]     # as três chamadas, na ordem em que o teste as faz

    def responder(prompt: str, corpo: dict):
        assert "CORREÇÃO DESTE CASO" in prompt, "só a proposta passa por aqui"
        return fila.pop(0), .9, []

    comum = {**_comum_de_teste(), "epoca": 101, "biblioteca_epoca": 100}
    # entidade-produto entra nos visíveis como se a busca o tivesse entregue (está em 46,7% dos contextos da calibração)
    ctx_validacao = {"raiz": raiz, "verbetes": bib.carregar(raiz), "casos": e3b.TODOS_OS_CASOS, "ids_visiveis": set(ctx["verbetes_ids"]) | {"campo_ausente", "entidade-produto"},
                     "epoca": 101, "caso_id": caso["id"], "modelo": "qwen2.5:7b", "novos_nesta_epoca": 0, "aceitas_no_caso": 0, "k": 3}
    filtros_ctx = {"parcelas": {"entidade-produto": .467, "contrato-produto": .422}, "corpo_http": caso["entrada"]["corpo"], "corrigidos": {}, "pesos_usados": {},
                   "casos_da_rodada": {"sin-1", "lex-9", "lex-2"}, "fontes": bf.fontes_das_cobaias(), "rotas": bf.rotas_do_openapi(), "data": "2026-11-03"}
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(), ts=TS)
    tid = "fase4_biblioteca/qwen2.5_7b/sin-1"
    s_ent = t.evento("entrada", tid, {"caso": "sin-1", "classe": 2, "nivel": 1, "origem": "fixture"}, "ao_vivo", ts=TS)
    with _ollama_de_mentira_v2(responder, chamadas):
        r1 = bf.propor_p5("qwen2.5:7b", caso, registro_diag, ctx, prompt_diag, verbetes, 700, comum, ctx_validacao, pasta_bib, 0, filtros_ctx,
                          trilha=t, tid=tid, evidencia=[{"seq": s_ent, "papel": "sinal_em_codigo"}], ts=TS)
    assert len(chamadas) == 1 and chamadas[0]["prompt"].startswith(prompt_diag + "\n\n" + resposta_diag + "\n\n"), "a proposta continua o prompt do diagnóstico byte a byte"
    assert r1["caso"] == "sin-1" and r1["tipo"] == "proposta" and r1["fase"] == "4" and r1["epoca"] == 101 and r1["n_propostas"] == 2 and r1["n_aceitas"] == 1
    # a busca já entregou campo_ausente a este caso: nada veio só pelo id, mas o verbete ligado fica registrado
    assert r1["abstencao"] is False and r1["recuperacao_por_id"] == ctx["por_id"] and r1["verbetes_ligados"] == [v["id"] for v in extras]
    assert r1["hash_biblioteca_apos"] == evo.hash_biblioteca(raiz)
    d1, d2 = r1["decisoes"]
    assert d1["aceita"] is True and d1["motivo"] is None and d1["edicao"]["verbete"] == "campo_ausente" and d1["filtro"] is None and d1["peso"] == 1
    assert d2["aceita"] is False and d2["motivo"] == "para_revisao_humana" and d2["filtro"] == "regra_dos_40" and d2["edicao"]["verbete"] == "entidade-produto"
    assert r1["para_revisao"] == [d2["edicao"]] and r1["filtros"][0]["fase3"]["aceita"] is True and r1["filtros"][1]["p5"]["codigo"] == "para_revisao_humana"
    assert d1["proveniencia"] == {"origem": "modelo", "caso": "sin-1", "modelo": "qwen2.5:7b", "epoca": 101, "data": "2026-11-03"}
    notas = bib.notas(next(v for v in bib.carregar(raiz) if v["id"] == "campo_ausente"))
    assert [n["caso"] for n in notas] == ["sin-1", "sin-1"] and notas[-1]["epoca"] == 101 and notas[-1]["texto"] == texto_ok
    assert not any(n["epoca"] == 101 for n in bib.notas(next(v for v in bib.carregar(raiz) if v["id"] == "entidade-produto"))), "a nota segurada não entra na cópia"
    assert filtros_ctx["pesos_usados"] == {"campo_ausente": 1}
    # a trilha: inferência da proposta, um evento edicao_biblioteca por bloco e o nó de decisão por último
    ev = [e for e in t.eventos if e["trilha"] == tid]
    inf = [e for e in ev if e["tipo"] == "inferencia"]
    eds = [e for e in ev if e["tipo"] == "edicao_biblioteca"]
    nos = [e for e in ev if e["tipo"] == "decisao"]
    assert len(inf) == 1 and inf[0]["dados"]["etapa"] == "proposta" and len(eds) == 2 and len(nos) == 1 and nos[0]["seq"] > eds[-1]["seq"]
    assert eds[0]["dados"]["aplicada"] is True and eds[0]["dados"]["origem"] == "modelo" and eds[0]["dados"]["proveniencia"]["caso"] == "sin-1"
    assert eds[1]["dados"]["aplicada"] is False and eds[1]["dados"]["para_revisao"] is True and eds[1]["dados"]["filtro"] == "regra_dos_40"
    no = nos[0]["dados"]
    assert no["decisao"] == "edicao_biblioteca" and no["escolha"] == "proposta_1" and no["resultado"] == "lote" and no["falha"] is None
    assert [a["opcao"] for a in no["alternativas"]] == ["proposta_1", "proposta_2", "nenhuma"] and no["divergencia"]["ha"] is False
    assert no["prov"]["wasDerivedFrom"] == ["sin-1"] and no["prov"]["wasGeneratedBy"] == inf[0]["seq"] and "campo_ausente" in no["prov"]["used"]
    assert any(e["papel"] == "sinal_em_codigo" for e in no["evidencia"]) and any(e["papel"] == "resposta" for e in no["evidencia"])
    assert no["justificativa"] and "—" not in no["justificativa"] and no["contraste"]
    assert r1["no"] == no and r1["seq_decisao"] == nos[0]["seq"]
    # segundo caso: texto de corpo HTTP na proposta é barrado antes de qualquer gravação; o nó aponta a falha da taxonomia
    caso2 = {**caso, "id": "lex-9", "entrada": {**caso["entrada"], "requisicao": "GET /api/produtos", "sintoma": "O catálogo fica vazio.", "status": 200,
                                                "corpo": caso["entrada"]["corpo"][:40]},
             "gabarito": {"causa_raiz": "corpo_nao_e_json", "campo_afetado": None, "termos_esperados": [], "termos_proibidos": []}}
    ctx_b, prompt_b = dv.montar_prompt(verbetes, indice, caso2, 3, extras=bf.verbetes_do_caso(verbetes, "lex-9"))
    ctx_validacao.update({"caso_id": "lex-9", "aceitas_no_caso": 0, "ids_visiveis": set(ctx_b["verbetes_ids"]) | {"corpo_nao_e_json"}})
    filtros_ctx["corpo_http"] = caso["entrada"]["corpo"]
    tid2 = "fase4_biblioteca/qwen2.5_7b/lex-9"
    t.evento("entrada", tid2, {"caso": "lex-9", "origem": "fixture"}, "ao_vivo", ts=TS)
    hash_antes = evo.hash_biblioteca(raiz)
    with _ollama_de_mentira_v2(responder, chamadas):
        r2 = bf.propor_p5("qwen2.5:7b", caso2, {"caso": "lex-9", "resposta": "CAUSA_RAIZ: corpo_nao_e_json\nCAMPO: nenhum\nIMPACTO: x.\nFONTE: [corpo_nao_e_json]",
                                                "verbetes_ids": ctx_b["verbetes_ids"]}, ctx_b, prompt_b, verbetes, 700, comum, ctx_validacao, pasta_bib, 1, filtros_ctx,
                          trilha=t, tid=tid2, ts=TS)
    assert r2["n_aceitas"] == 0 and r2["decisoes"][0]["motivo"] == "texto_de_origem_proibida" and r2["decisoes"][0]["edicao"] is None
    assert evo.hash_biblioteca(raiz) == hash_antes
    no2 = r2["no"]
    assert no2["escolha"] == "nenhuma" and no2["resultado"] == "recusada" and no2["falha"] == "texto_de_origem_proibida" and no2["divergencia"]["ha"] is True
    # terceiro caso: NENHUMA é abstenção válida, sem gravação e sem falha
    caso3 = {**caso2, "id": "lex-2"}
    ctx_c, prompt_c = dv.montar_prompt(verbetes, indice, caso3, 3)
    ctx_validacao.update({"caso_id": "lex-2", "aceitas_no_caso": 0, "ids_visiveis": set(ctx_c["verbetes_ids"]) | {"corpo_nao_e_json"}})
    tid3 = "fase4_biblioteca/qwen2.5_7b/lex-2"
    t.evento("entrada", tid3, {"caso": "lex-2", "origem": "fixture"}, "ao_vivo", ts=TS)
    with _ollama_de_mentira_v2(responder, chamadas):
        r3 = bf.propor_p5("qwen2.5:7b", caso3, {"caso": "lex-2", "resposta": "CAUSA_RAIZ: corpo_nao_e_json\nCAMPO: nenhum\nIMPACTO: x.\nFONTE: nenhum",
                                                "verbetes_ids": ctx_c["verbetes_ids"]}, ctx_c, prompt_c, verbetes, 700, comum, ctx_validacao, pasta_bib, 1, filtros_ctx,
                          trilha=t, tid=tid3, ts=TS)
    assert r3["abstencao"] is True and r3["n_propostas"] == 0 and r3["decisoes"] == [] and r3["no"]["resultado"] == "abstencao" and r3["no"]["escolha"] == "nenhuma"
    assert r3["no"]["falha"] is None and r3["no"]["divergencia"]["ha"] is False
    # a época reconstruída do JSONL tem o mesmo hash (retomada da corrida), e fecha pelo fechamento da Fase 3
    import shutil as sh
    sh.rmtree(raiz)
    raiz2 = evo.abrir_epoca(pasta_bib, 101, [r1, r2, r3])
    assert evo.hash_biblioteca(raiz2) == r1["hash_biblioteca_apos"]
    fechamento = evo.fechar_epoca(pasta_bib, 101, "qwen2.5:7b", e3b.TODOS_OS_CASOS, 1, versao_ollama="0.40.2")
    assert fechamento["aceitas_na_epoca"] == 1 and fechamento["n_notas"] == 13
    # o relatório v2 do caso mostra a decisão da biblioteca
    t.fechar(fim="2026-11-03T22:00:00")
    md = grr.relatorio_do_caso_v2(t.eventos, tid, comando_reexecucao="python executar_fase4.py --modo biblioteca --casos 1")
    assert "Biblioteca" in md and "entidade-produto" in md and "revisão humana" in md and "—" not in md
    md2 = grr.relatorio_do_caso_v2(t.eventos, tid2)
    assert "texto_de_origem_proibida" in md2
    # a sonda com recuperação por id: o contexto do executor congelado ganha os verbetes ligados ao caso pelo id, só para esses casos
    with bf.com_recuperacao_por_id(verbetes):
        ctx_e10, prompt_e10 = executar_fase3.contexto_e_prompt(verbetes, indice, next(c for c in e3b.TODOS_OS_CASOS if c["id"] == "efe-10"), 3)
        ctx_e3, _ = executar_fase3.contexto_e_prompt(verbetes, indice, next(c for c in e3b.TODOS_OS_CASOS if c["id"] == "efe-3"), 3)
    assert "interface-frontend" in ctx_e10["verbetes_ids"] and ctx_e10["texto"].endswith(bib.render(por_id["interface-frontend"])) and ctx_e10["verbete_ouro"]
    assert prompt_e10 == executar_fase3.linear_com_biblioteca(next(c for c in e3b.TODOS_OS_CASOS if c["id"] == "efe-10"), ctx_e10["texto"])
    assert ctx_e3["verbetes_ids"] == rec.contexto(verbetes, indice, next(c for c in e3b.TODOS_OS_CASOS if c["id"] == "efe-3"), "A2", 3)["verbetes_ids"]
    assert executar_fase3.contexto_e_prompt(verbetes, indice, next(c for c in e3b.TODOS_OS_CASOS if c["id"] == "efe-10"), 3)[0]["verbetes_ids"] == \
        rec.contexto(verbetes, indice, next(c for c in e3b.TODOS_OS_CASOS if c["id"] == "efe-10"), "A2", 3)["verbetes_ids"], "fora do bloco, o executor volta ao normal"
    import sonda_correcao
    ap = sonda_correcao.montar_parser()
    a = ap.parse_args(["--saida", "x", "--modelo", "qwen2.5:7b", "--casos", "efe-3", "--recuperacao-por-id", "--origem", str(leitura)])
    assert a.recuperacao_por_id is True and a.origem == str(leitura) and ap.parse_args(["--saida", "x", "--modelo", "m", "--casos", "efe-3"]).recuperacao_por_id is False
    assert sonda_correcao.menciona_correcao("A documentação já registra a solução aplicada: o campo voltou.") is True
    assert sonda_correcao.menciona_correcao("Adicionar nota sobre a remoção de campos.") is False


def teste_executar_fase4_modo_biblioteca_partes_puras():
    import executar_fase4 as ex
    assert ex.MODOS == ("reproducao", "calibracao", "tela", "cura", "biblioteca")
    ap = ex.montar_parser()
    a = ap.parse_args(["--modo", "biblioteca", "--saida", "x"])
    assert a.base_ineditos == "corrida12" and a.sem_sonda is False and a.sem_correcao is False and a.teto_proposta == 700
    assert ap.parse_args(["--modo", "biblioteca", "--saida", "x", "--base-ineditos", "propria"]).base_ineditos == "propria"
    # o conjunto de correção: metade dos casos ligados a notas e com tela fica com o modo desligado, metade mantido; a partilha é determinística
    ids = ["lex-2", "lex-9", "run-7", "semt-13", "sin-1", "sin-13", "sin-15", "sin-9", "tra-12", "tra-3"]
    conj = ex.conjunto_de_correcao(ids)
    assert sorted(conj["desligados"] + conj["mantidos"]) == sorted(ids) and len(conj["desligados"]) == 5 and len(conj["mantidos"]) == 5
    assert conj == ex.conjunto_de_correcao(list(reversed(ids))) and conj["regra"].startswith("sha256")
    assert ex.conjunto_de_correcao(["a"]) == {"desligados": ["a"], "mantidos": [], "regra": conj["regra"]}
    assert ex.conjunto_de_correcao([])["desligados"] == []
    # os casos de aprendizado ligados a notas da L1 curada e com tela: os dez conhecidos
    lig = ex.casos_ligados_com_tela()
    assert [c["id"] for c in lig] == ids, [c["id"] for c in lig]
    assert all(c["modo"] and c["cenario"] and c["verbetes"] for c in lig) and lig[4]["verbetes"] == ["campo_ausente"]
    # os registros compactos da corrida
    d = {"caso": "sin-1", "classe": 2, "nivel": 1, "origem": "tela", "reproduz": True, "modo": "field_missing", "campo": "preco", "cenario": "api-catalogo",
         "diagnostico": {"no": {"escolha": "campo_ausente", "confianca": {"p_rotulo": .9, "selo": "alto"}, "divergencia": {"ha": False}, "falha": None},
                         "registro": {"segundos": 60.0, "tokens_entrada": 1100}, "gatilhos": {"algum": False}},
         "acertou": True, "proposta": {"n_propostas": 2, "n_aceitas": 1, "abstencao": False, "segundos": 50.0, "tokens_entrada": 1800, "recuperacao_por_id": ["campo_ausente"],
                                       "decisoes": [{"aceita": True, "motivo": None, "filtro": None, "operacao": "nota", "verbete": "campo_ausente", "peso": 1},
                                                    {"aceita": False, "motivo": "para_revisao_humana", "filtro": "regra_dos_40", "operacao": "nota", "verbete": "entidade-produto", "peso": 1}],
                                       "para_revisao": [{"verbete": "entidade-produto"}]},
         "segundos_cenario": 3.2}
    reg = ex.registro_da_biblioteca(d)
    assert reg["caso"] == "sin-1" and reg["origem"] == "tela" and reg["rotulo"] == "campo_ausente" and reg["acertou"] is True and reg["p_rotulo"] == .9
    assert reg["n_propostas"] == 2 and reg["n_aceitas"] == 1 and reg["para_revisao"] == 1 and reg["recusadas"] == [] and reg["abstencao"] is False
    assert reg["recuperacao_por_id"] == ["campo_ausente"] and reg["segundos_diagnostico"] == 60.0 and reg["segundos_proposta"] == 50.0 and reg["verbetes_editados"] == ["campo_ausente"]
    c = {"caso": "sin-1", "cenario": "api-catalogo", "modo": "field_missing", "campo": "preco", "verbetes": ["campo_ausente"], "desligado": True,
         "antes": {"passou": False, "reproduz": True}, "depois": {"passou": True}, "evidencia": {"ha_diff_http": True, "ha_diff_arvore": True, "sintoma_sumiu": True},
         "deteccao": {"corrigido": True, "motivo": "ok"}, "estados": {"campo_ausente": ("nao_corrigido", "corrigido")}, "segundos": 4.5}
    rc = ex.registro_da_correcao(c)
    assert rc["caso"] == "sin-1" and rc["desligado"] is True and rc["reproduziu_antes"] is True and rc["passou_depois"] is True and rc["marcado"] is True
    assert rc["ha_diff_http"] is True and rc["ha_diff_arvore"] is True and rc["verbetes"] == ["campo_ausente"] and rc["estados"]["campo_ausente"] == ["nao_corrigido", "corrigido"]


def _bruto_da_biblioteca_de_mentira() -> dict:
    def diag(caso: str, causa: str, resposta: str, origem: str = "fixture") -> dict:
        return {"caso": caso, "classe": 1, "nivel": 1, "origem": origem, "reproduz": origem == "tela", "modo": "field_missing", "cenario": "api-catalogo", "rotulo": resposta,
                "acertou": resposta == causa, "p_rotulo": .9, "selo": "alto", "segundos_diagnostico": 60.0, "segundos_proposta": 50.0, "tokens_entrada": 1100,
                "n_propostas": 1, "n_aceitas": 1 if caso != "lex-9" else 0, "para_revisao": 1 if caso == "sin-1" else 0, "abstencao": caso == "lex-2",
                "recusadas": ["redundante"] if caso == "lex-9" else [], "recuperacao_por_id": ["campo_ausente"] if caso == "sin-1" else [],
                "verbetes_editados": ["campo_ausente"] if caso == "sin-1" else (["corpo_nao_e_json"] if caso == "lex-2" else [])}

    def reg(caso: str, causa: str, resposta: str) -> dict:
        return {"caso": caso, "gabarito": {"causa_raiz": causa, "campo_afetado": None}, "resposta": f"CAUSA_RAIZ: {resposta}\nCAMPO: nenhum\nIMPACTO: x.\nFONTE: nenhum"}

    propostas = [{"caso": "sin-1", "abstencao": False, "n_propostas": 2, "n_aceitas": 1, "segundos": 50.0,
                  "decisoes": [{"aceita": True, "motivo": None, "filtro": None, "operacao": "nota", "verbete": "campo_ausente", "peso": 1, "edicao": {"operacao": "nota", "verbete": "campo_ausente", "caso": "sin-1", "texto": "t"}},
                               {"aceita": False, "motivo": "para_revisao_humana", "filtro": "regra_dos_40", "operacao": "nota", "verbete": "entidade-produto", "peso": 1,
                                "edicao": {"operacao": "nota", "verbete": "entidade-produto", "caso": "sin-1", "texto": "t2"}}]},
                 {"caso": "lex-9", "abstencao": False, "n_propostas": 1, "n_aceitas": 0, "segundos": 40.0,
                  "decisoes": [{"aceita": False, "motivo": "redundante", "filtro": "redundancia", "operacao": "nota", "verbete": "corpo_nao_e_json", "peso": None, "edicao": None}]},
                 {"caso": "lex-2", "abstencao": True, "n_propostas": 0, "n_aceitas": 0, "segundos": 30.0, "decisoes": []}]
    base = [reg("lex-16", "x", "x"), reg("lex-17", "y", "z"), reg("sin-16", "w", "w"), reg("efe-21", "u", "u")]
    novo = [reg("lex-16", "x", "x"), reg("lex-17", "y", "y"), reg("sin-16", "w", "w"), reg("efe-21", "u", "u")]
    correcoes = [{"caso": "sin-1", "cenario": "api-catalogo", "modo": "field_missing", "verbetes": ["campo_ausente"], "desligado": True, "reproduziu_antes": True, "passou_depois": True,
                  "ha_diff_http": True, "ha_diff_arvore": True, "marcado": True, "motivo": "ok", "estados": {"campo_ausente": ["nao_corrigido", "corrigido"]}, "segundos": 4.0},
                 {"caso": "lex-9", "cenario": "api-catalogo", "modo": "corpo_nao_e_json", "verbetes": ["corpo_nao_e_json"], "desligado": False, "reproduziu_antes": True, "passou_depois": False,
                  "ha_diff_http": False, "ha_diff_arvore": False, "marcado": False, "motivo": "ainda falha", "estados": {}, "segundos": 3.0},
                 {"caso": "tra-3", "cenario": "api-catalogo", "modo": "chave_de_juncao_errada", "verbetes": ["chave_de_juncao_errada"], "desligado": True, "reproduziu_antes": True, "passou_depois": True,
                  "ha_diff_http": True, "ha_diff_arvore": False, "marcado": False, "motivo": "árvore igual", "estados": {}, "segundos": 3.5}]
    sonda = {"casos": [{"caso": "efe-10", "rotulo": "estado_da_tela_divergente", "acertou": True, "n_propostas": 1, "n_aceitas": 0, "abstencao": False, "motivos": ["duplicada"],
                        "menciona_correcao": True, "por_id": ["interface-frontend"], "segundos": 120.0},
                       {"caso": "efe-3", "rotulo": "campo_ausente", "acertou": True, "n_propostas": 2, "n_aceitas": 0, "abstencao": False, "motivos": ["teto_notas_verbete", "duplicada"],
                        "menciona_correcao": False, "por_id": [], "segundos": 110.0},
                       {"caso": "sin-1", "rotulo": "campo_ausente", "acertou": True, "n_propostas": 0, "n_aceitas": 0, "abstencao": True, "motivos": [],
                        "menciona_correcao": False, "por_id": ["campo_ausente"], "segundos": 90.0}],
             "anterior": {"efe-10": {"rotulo": "dado_desatualizado", "acertou": False, "n_propostas": 2, "n_aceitas": 1, "motivos": ["teto_notas_verbete"]},
                          "efe-3": {"rotulo": "campo_ausente", "acertou": True, "n_propostas": 2, "n_aceitas": 0, "motivos": ["teto_notas_verbete", "duplicada"]}}}
    return {"condicoes": {"modo": "biblioteca", "k": 3, "casos": 3, "parcial": False, "base_ineditos": "corrida12", "conjunto_de_correcao": {"desligados": ["sin-1", "tra-3"], "mantidos": ["lex-9"]},
                          "parcelas_para_revisao": {"entidade-produto": .467, "contrato-produto": .422}, "biblioteca": {"hash": "1fca10f1a6f6"}},
            "registros": [diag("sin-1", "campo_ausente", "campo_ausente", "tela"), diag("lex-9", "corpo_nao_e_json", "corpo_vazio"), diag("lex-2", "corpo_nao_e_json", "corpo_nao_e_json")],
            "propostas": propostas, "lote": {"edicoes": [{"verbete": "campo_ausente", "operacao": "nota", "caso": "sin-1", "peso": 1}], "para_revisao": [{"verbete": "entidade-produto", "operacao": "nota", "caso": "sin-1", "peso": 1}],
                                             "fechamento": {"hash": "abc123", "n_notas": 13, "n_verbetes": 40, "n_verbetes_novos": 4}},
            "reavaliacao": {"base": base, "novo": novo, "origem_da_base": "pre_fase4_confianca (corrida 12, Ollama 0.34.4)"},
            "correcoes": correcoes, "sonda": sonda, "recuperacao": {"aprendidos_na_calibracao": {"atualizacao_imediata": 0, "interface-estados": 0, "interface-frontend": 0, "rotas-inexistentes": 0},
                                                                   "por_id_nesta_corrida": {"casos_com_verbete_por_id": 1, "verbetes": {"campo_ausente": 1}}},
            "trilha_info": {"bytes": 1000, "eventos": 50}, "inferencias": 11, "segundos": 900.0}


def teste_avaliar_fase4_biblioteca_aplica_r4_e_r5_com_check():
    import avaliar_fase4 as av
    import pre_fase4 as pf
    bruto = _bruto_da_biblioteca_de_mentira()
    dado = av.resumir_biblioteca(bruto, gerado_em="2026-11-03T23:00:00", corrida="fase4_biblioteca")
    r = dado["resumo"]
    assert r["casos"] == 3 and r["da_tela"] == 1 and r["do_fixture"] == 2 and r["acertos_diagnostico"] == 2 and r["propostas"] == 3 and r["aceitas"] == 1
    assert r["abstencoes"] == 1 and r["para_revisao"] == 1 and r["recusadas_p5"] == 1 and r["recusadas_fase3"] == 0 and r["casos_com_verbete_por_id"] == 1
    f = {x["filtro"]: x for x in dado["filtros"]}
    assert f["redundancia"]["recusas"] == 1 and f["regra_dos_40"]["recusas"] == 1 and f["evidencia_obrigatoria"]["recusas"] == 0 and len(dado["filtros"]) == 13
    assert dado["lote"]["edicoes"] == 1 and dado["lote"]["para_revisao"] == 1 and dado["lote"]["hash"] == "abc123"
    r5 = dado["reavaliacao"]
    assert (r5["n"], r5["b"], r5["c"]) == (4, 1, 0) and r5["veredito"] == "aceito" and r5["acerto_base_pct"] == 75.0 and r5["acerto_novo_pct"] == 100.0
    r4 = dado["correcao"]
    assert r4["universo"] == 3 and r4["desligados"] == 2 and r4["marcados"] == 1 and r4["precisao_pct"] == 100.0 and r4["revocacao_pct"] == 50.0
    assert [x["caso"] for x in r4["por_caso"]] == ["sin-1", "lex-9", "tra-3"] and r4["por_caso"][2]["motivo"] == "árvore igual"
    s = dado["sonda"]
    assert s["casos"] == 3 and s["mudaram_proposta"] == 1 and s["sem_sonda_anterior"] == 1 and s["mencionam_correcao"] == 1 and s["abstencoes"] == 1
    assert [x["caso"] for x in s["por_caso"]] == ["efe-10", "efe-3", "sin-1"] and s["por_caso"][0]["rotulo_anterior"] == "dado_desatualizado" and s["por_caso"][2]["rotulo_anterior"] is None
    assert dado["recuperacao"]["aprendidos_sem_recuperacao"] == ["atualizacao_imediata", "interface-estados", "interface-frontend", "rotas-inexistentes"]
    assert dado["regra_r4"]["cumprida"] is None or isinstance(dado["regra_r4"]["cumprida"], bool)
    assert dado["regra_r5"]["veredito"] == "aceito"
    md = av.render_biblioteca(dado)
    for bloco in ("tb_f4_biblioteca_resumo", "tb_f4_biblioteca_filtros", "tb_f4_biblioteca_rejeicoes", "tb_f4_biblioteca_lote", "tb_f4_biblioteca_reavaliacao",
                  "tb_f4_biblioteca_correcao", "tb_f4_biblioteca_sonda", "tb_f4_biblioteca_revisao", "tb_f4_biblioteca_recuperacao", "tb_f4_biblioteca_casos"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    assert "—" not in md and "→" not in md and "75,0" in md and "100,0" in md
    pasta = _temp()
    assert pf.fechar(av.NOME_BIBLIOTECA, dado, md, av.PREFIXO_BIBLIOTECA, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert pf.fechar(av.NOME_BIBLIOTECA, dado, md, av.PREFIXO_BIBLIOTECA, check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert av.NOME_BIBLIOTECA == "biblioteca" and av.PREFIXO_BIBLIOTECA == "tb_f4_biblioteca_" and av.TITULO_BIBLIOTECA == "Biblioteca em produção e ciclo de correção (corrida 20)"
    assert av.nome_dos_arquivos(None, "biblioteca") == "biblioteca"
    assert av.montar_parser().parse_args(["--biblioteca", "--saida", "fase4_biblioteca"]).biblioteca is True
    vazio = av.resumir_biblioteca({"condicoes": {}, "registros": [], "propostas": [], "lote": None, "reavaliacao": None, "correcoes": [], "sonda": None, "recuperacao": None,
                                   "trilha_info": None, "inferencias": 0, "segundos": 0.0}, gerado_em="2026-11-03T23:00:00", corrida="x")
    assert vazio["resumo"]["casos"] == 0 and vazio["reavaliacao"] is None and av.render_biblioteca(vazio)


# ----------------------------------------------------------------------------- P0: a amostra real (fica por último)

def teste_fixture_da_arvore_tem_papel_e_nome():
    """A amostra real de produtos_api.php, com as cobaias no ar (P0, item 3 do plano aprovado). Fica por último porque
    o runner para na primeira falha: enquanto PHP e MariaDB não existirem na máquina, este é o único teste vermelho."""
    dados = _conferir_fixture_arvore(FIX / "arvore_produtos_api.json")
    assert dados["origem"].startswith("http://localhost:8080/"), dados["origem"]
    assert not dados.get("provisoria"), "a amostra real não pode ser marcada como provisória"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gravar-hashes", action="store_true",
                    help="grava o hash de conteúdo das áreas só de leitura em fixtures_fase4/ e sai")
    args = ap.parse_args()
    if args.gravar_hashes:
        for nome, h in gravar_hashes().items():
            print(f"{nome}: {h}")
        print(f"gravado em {ARQUIVO_HASHES}")
        return
    modulo = sys.modules[__name__]
    testes = [(nome, obj) for nome, obj in vars(modulo).items()
              if nome.startswith("teste_") and inspect.isfunction(obj) and obj.__module__ == modulo.__name__]
    try:
        for nome, funcao in testes:
            try:
                funcao()
            except Exception:
                print(nome)
                traceback.print_exc()
                sys.exit(1)
            print(f"{nome} ok")
        print(f"{len(testes)} testes ok")
    finally:
        for caminho in _TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)


if __name__ == "__main__":
    main()
