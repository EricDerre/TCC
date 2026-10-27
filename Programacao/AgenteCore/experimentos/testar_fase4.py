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
import avaliar
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
