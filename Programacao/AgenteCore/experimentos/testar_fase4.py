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


# ! Alteração de IA - Revisar: (04/11/2026) teste de Trilha.descartar_desde: cortar a trilha a partir de um evento recalcula
# os passos, os nós e os blobs como Trilha.carregar faria, e a numeração continua sem buraco.
# ! Motivo: refazer a fase C da corrida 20 exige tirar da trilha os eventos da primeira tentativa (ver
# teste_executar_fase4_refazer_a_correcao_descarta_da_trilha_os_eventos_da_fase_c); sem recontar, o passo da trilha do
# caso continuaria do número antigo, o limite de nós contaria os nós descartados e um blob descartado não voltaria a ser
# gravado.
def teste_trilha_descartar_desde_reconta_passos_nos_e_blobs():
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(), ts=TS)
    t.evento("entrada", "s/m/lex-2@tela", {"caso": "lex-2"}, "ao_vivo", ts=TS)
    corte = len(t.eventos)
    h = t.blob("texto que só a fase C usa", "corpo")
    s = t.evento("entrada", "s/m/lex-2@correcao", {"caso": "lex-2"}, "ao_vivo", ts=TS)
    t.decisao("s/m/lex-2@correcao", _no(), ts=TS)
    assert t.eventos[s - 1]["passo"] == 1
    assert t.descartar_desde(corte) == 3
    assert len(t.eventos) == corte and t.eventos[-1]["trilha"] == "s/m/lex-2@tela"
    # a parte refeita volta a gravar o blob, recomeça do passo 1 e conta de novo os nós da trilha do caso
    assert t.blob("texto que só a fase C usa", "corpo") == h and t.eventos[-1]["tipo"] == "blob"
    s2 = t.evento("entrada", "s/m/lex-2@correcao", {"caso": "lex-2"}, "ao_vivo", ts=TS)
    assert s2 == len(t.eventos) and t.eventos[-1]["passo"] == 1
    assert [e["seq"] for e in t.eventos] == list(range(1, len(t.eventos) + 1)), "a numeração continua sem buraco"
    for _ in range(trilha.LIMITES_PADRAO["nos_por_diagnostico"]):
        t.decisao("s/m/lex-2@correcao", _no(), ts=TS)
    try:
        t.decisao("s/m/lex-2@correcao", _no(), ts=TS)
    except ValueError:
        pass
    else:
        raise AssertionError("o limite de nós não foi recontado depois do corte")
    try:
        t.descartar_desde(0)
    except ValueError:
        pass
    else:
        raise AssertionError("descartar_desde(0) apagou o cabeçalho da corrida")


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
    # ! Alteração de IA - Revisar: (05/11/2026, decisão 90) o SINTOMA diz a contagem de linhas, sem a lista: "R$ 89,90" saiu dele.
    # ! Motivo: a lista `faltam` saiu do molde para o prompt caber no limite do plano; a trilha continua com ela, no diff.
    assert "preco_v2" in sintoma and "14 cartões" in sintoma and "1 linha(s) a menos" in sintoma and "R$ 89,90" not in sintoma, sintoma
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
# ! Alteração de IA - Revisar: (04/11/2026) os testes que leem a L1 curada passam a ler a cópia que a calibração leu (corrida 16,
# resultados_alvo/fase4_calibracao/k3/bibliotecas/qwen2.5_7b/epoca-100, hash 1fca10f1a6f6), não biblioteca_producao/ ao vivo; o
# hash é conferido a cada carga e a cada cópia.
# ! Motivo: em 04/11/2026 o fechar_p5.ps1 promoveu o lote da corrida 20 e mandou os quatro aprendidos para a espera, como devia; os
# testes do P5 liam a produção e fixavam números da L1 de antes (40 verbetes, 12 notas, os quatro aprendidos, os dez casos ligados a
# notas), e cinco falharam no fim do fechar_p5 ("KeyError: 'atualizacao_imediata'"). A cópia da corrida 16 é pasta oficial, que
# ninguém regrava, e é a biblioteca de que esses números falam; a produção segue conferida pelo teste das áreas só de leitura.
CURADA_DOS_TESTES = RA / "fase4_calibracao" / "k3" / "bibliotecas" / "qwen2.5_7b" / "epoca-100"
HASH_DA_CURADA_DOS_TESTES = "1fca10f1a6f6"


def _curada():
    """A L1 curada (a cópia que a calibração leu, CURADA_DOS_TESTES) e o índice BM25 dela, carregados uma vez por rodada de testes."""
    if not _BIBLIOTECA_CURADA:
        import biblioteca as bib
        import evolucao_biblioteca as evo
        import recuperacao as rec
        assert evo.hash_biblioteca(CURADA_DOS_TESTES) == HASH_DA_CURADA_DOS_TESTES, "a cópia da L1 curada da corrida 16 mudou"
        verbetes = bib.carregar(CURADA_DOS_TESTES)
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
    # ! Alteração de IA - Revisar: (04/11/2026, P6) o modo `cenarios` entra na tupla.
    # ! Motivo: a corrida 21 é `executar_fase4.py --modo cenarios` (plano aprovado, seção 5, P6).
    # ! Alteração de IA - Revisar: (04/11/2026, P7) o modo `avaliacao_trilha` entra na tupla.
    # ! Motivo: a corrida 22 é `executar_fase4.py --modo avaliacao_trilha` (plano aprovado, seção 5, P7).
    # (05/11, decisões 91 e 92) experimento_prompt e ineditos, as corridas 23 e 24, em corridas_em_texto.py
    assert ex.MODOS == ("reproducao", "calibracao", "tela", "cura", "biblioteca", "cenarios", "avaliacao_trilha", "experimento_prompt", "ineditos")   # (01/11, P4) cura, (03/11, P5) biblioteca, (04/11, P6) cenarios, (04/11, P7) avaliacao_trilha

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
    # ! Alteração de IA - Revisar: (04/11/2026, P6) o modo `cenarios` entra no ValidateSet.
    # ! Motivo: a corrida 21 é `rodar_fase4.ps1 -Modo cenarios -Saida fase4_ensaio -Repeticoes 1` (plano aprovado, seção 6).
    # ! Alteração de IA - Revisar: (04/11/2026, P7) o modo `avaliacao_trilha` entra no ValidateSet, conta como modo com modelo e passa
    # `--sem-seletor` ao executor com `-SemSeletor` (fumaça sem as cobaias); a avaliação do modo é `avaliar_fase4.py --trilha`.
    # ! Motivo: a corrida 22 é `rodar_fase4.ps1 -Modo avaliacao_trilha -Saida fase4_trilha` (plano aprovado, seção 6).
    # ! Alteração de IA - Revisar: (05/11/2026, decisões 91 e 92) os modos `experimento_prompt` e `ineditos` entram no ValidateSet.
    # ! Motivo: a corrida 23 é `rodar_fase4.ps1 -Modo experimento_prompt -Saida fase4_experimento` e a 24, `-Modo ineditos -Saida fase4_ineditos`.
    assert 'ValidateSet("reproducao", "calibracao", "tela", "cura", "biblioteca", "cenarios", "avaliacao_trilha", "experimento_prompt", "ineditos")' in texto, "os modos novos entram no ValidateSet"
    assert '($Modo -eq "cenarios")' in texto, "o modo cenarios passa --repeticoes ao executor"
    assert '($Modo -eq "avaliacao_trilha")' in texto and "[switch]$SemSeletor" in texto and "--sem-seletor" in texto, "o modo avaliacao_trilha e -SemSeletor"
    assert "avaliacao_trilha" in texto.split("$ComModelo = ", 1)[1].split("\n", 1)[0], "o modo avaliacao_trilha é um modo com modelo (Ollama, RAM, ponte)"
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


# ! Alteração de IA - Revisar: (04/11/2026, leitura da corrida 21) dois testes: com um diagnóstico entre a detecção e a cura, os
# candidatos são verificados numa página nova, refeita até o passo que falhou (sem diagnóstico, na própria página, como na corrida 19);
# e o relatório de um caso com diagnóstico e cura traz na linha de ação a sugestão da cura, e nunca "Confira o campo `nenhum`".
# ! Motivo: na corrida 21 o modelo levou 55 s no cenário de login, a tela de login voltou sozinha para a página inicial (meta refresh de
# 30 s em admin/login.php) e todos os candidatos deram "nenhum elemento", embora a mesma célula tenha curado 10 de 10 na corrida 19, sem
# modelo no meio. No relatório, o ramo da cura exigia não haver diagnóstico, e os casos da Fase 5 têm os dois.
def teste_cura_depois_do_diagnostico_verifica_numa_pagina_refeita_ate_o_passo_que_falhou():
    import cenarios_fase4 as cen
    import cura_seletor as cs
    import executar_fase4 as ex
    import interceptador as ic
    import poda

    class Pagina:
        def __init__(self, n: int) -> None:
            self.n, self.fechada, self.navegou_sozinha = n, False, False

        def add_init_script(self, _script: str) -> None:
            pass

        def evaluate(self, _js: str):
            return None

        def close(self) -> None:
            self.fechada = True

    class Nav:
        def __init__(self) -> None:
            self.paginas: list[Pagina] = []

        def nova_pagina(self) -> Pagina:
            self.paginas.append(Pagina(len(self.paginas)))
            return self.paginas[-1]

    class Inter:
        def __init__(self, _pagina) -> None:
            self.incidentes: list = []

        def capturar(self) -> dict:
            return {"nos": [], "aria": "", "titulo": "", "interativos": []}

    q = cen.quebra("front-admin-login", "classe_trocada")
    alvo = {"papel": "button", "nome": "Entrar", "texto": "Entrar", "ocorrencia": 1, "contagem": 1, "seletor": q["localizador"], "tag": "button", "ancestral_com_id": None,
            "atributos": {"id": None, "class": " btn btn-primary", "data-id": None}, "caminho": "body > form > button", "pai": "body > form", "posicao_entre_irmaos": 1,
            "impressao": {"tag": "button", "type": "submit"}}

    def montar(apos) -> tuple:
        nav = Nav()
        cura = ex.Cura(nav, None, "saida", "token", lambda _m: None, None)
        cura.referencias[(q["cenario"], q["modo"])] = {"alvo": alvo, "passou": True, "segundos": .1, "erro": None, "conferencia_falha": None, "erro_descricao": None}
        rodadas: list = []
        resolvidas: list = []

        def rodar(cenario_, pagina, _inter=None, **_kw) -> dict:
            n_passos = len(cenario_["passos"])
            curado = any(p.get("curado") for p in cenario_["passos"])
            rodadas.append({"pagina": pagina.n, "passos": n_passos, "curado": curado})
            base = {"inicio": "2026-11-04T20:00:00", "fim": "2026-11-04T20:00:01", "segundos": .2, "conferencia_falha": None, "erro": None, "conferencias": [], "tempos_ms": [],
                    "capturas": [], "chamadas": [], "deteccao": None, "t_deteccao": None, "passo_falho": None, "passou": True}
            if len(rodadas) == 1:
                return {**base, "passou": False, "passo_falho": q["passo_alvo"], "erro": "TimeoutError", "deteccao": "2026-11-04T20:00:01", "t_deteccao": 100.0}
            return base

        def resolver(pagina, _candidato: dict) -> dict:
            resolvidas.append(pagina.n)
            if pagina.navegou_sozinha:
                return {"contagem": 0, "visivel": None, "habilitado": None, "papel": None, "nome": None}
            return {"contagem": 1, "visivel": True, "habilitado": True, "papel": "button", "nome": "Entrar"}

        originais = (cen.rodar_cenario, ic.Interceptador, cs.resolver_no_navegador, poda.podar_arvore)
        cen.rodar_cenario, ic.Interceptador, cs.resolver_no_navegador = rodar, Inter, resolver
        poda.podar_arvore = lambda *_a, **_k: {"texto": 'document "Login"\n  button "Entrar" class="btn btn-entrar"\n', "antes": 2, "depois": 2, "regras": {}}
        try:
            d = cura.executar({"cenario": q["cenario"], "modo": q["modo"], "forma": "harness", "repeticao": 1}, apos_deteccao=apos(nav) if apos else None)
        finally:
            cen.rodar_cenario, ic.Interceptador, cs.resolver_no_navegador, poda.podar_arvore = originais
        return d, nav, rodadas, resolvidas

    # com o diagnóstico no meio: a página da detecção navega sozinha enquanto o modelo pensa (o que o meta refresh fez na corrida 21)
    def diagnostico_lento(nav: Nav):
        def gancho(_d: dict) -> dict:
            nav.paginas[0].navegou_sozinha = True
            return {"rotulo": "localizador_quebrado"}
        return gancho

    d, nav, rodadas, resolvidas = montar(diagnostico_lento)
    assert d["escolha"]["curado"] is True, d["escolha"]
    assert rodadas[1] == {"pagina": 1, "passos": q["passo_alvo"], "curado": False}, "a página nova refaz o roteiro até antes do passo que falhou"
    assert resolvidas and all(n == 1 for n in resolvidas), f"os candidatos são verificados na página refeita: {resolvidas}"
    assert rodadas[-1]["curado"] is True and rodadas[-1]["pagina"] == 2, "a reexecução continua numa página própria, do começo"
    assert d["pagina_refeita"]["passou"] is True and d["pagina_refeita"]["passos"] == q["passo_alvo"]
    assert all(p.fechada for p in nav.paginas), "nenhuma página fica aberta"
    assert d["t_validacao"] is not None and d["mttr_s"] is not None
    # sem diagnóstico (o modo `cura`): a verificação segue na própria página, como na corrida 19
    d, nav, rodadas, resolvidas = montar(None)
    assert d["escolha"]["curado"] is True and d.get("pagina_refeita") is None
    assert resolvidas and all(n == 0 for n in resolvidas) and len(rodadas) == 2 and len(nav.paginas) == 2, (resolvidas, rodadas)


def teste_relatorio_v2_com_diagnostico_e_cura_a_linha_de_acao_e_a_da_cura():
    import caso_ao_vivo as cv
    import diagnostico_ao_vivo as dv
    verbetes, indice = _curada()
    t, tid, r = _trilha_de_cura()
    caso = cv.montar_caso("localizador-front-admin-login@cenario", "GET admin/login.php", 200, "(página PHP do front legado: sem contrato de API)",
                          "(HTML da página; nenhuma chamada à API falhou)", "o roteiro parou no passo 5", arvore='- button "Entrar"', seletor_quebrado="button.btn-primary")
    resposta = ("O localizador não acha o botão.\nCAUSA_RAIZ: localizador_quebrado\nCAMPO: nenhum\nIMPACTO: o roteiro para no login.\nFONTE: [localizador_quebrado]",
                .9, [(" tempo_de_resposta_excedido", .05)])
    with _ollama_de_mentira_v2(lambda _p, _c: resposta, []):
        dv.diagnosticar(t, tid, caso, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=_comum_de_teste(), limiares=None, intervencoes="desligadas", evidencia=[], ts=TS)
    md = grr.relatorio_do_caso_v2(t.eventos, tid)
    acao = md.split("## 5. Linha de ação")[1].split("## 6.")[0]
    assert "Sugestão" in acao and "o agente não altera a aplicação" in acao and r["aplicado"]["seletor"] in acao, acao
    assert "Confira o campo" not in acao and "contrato esperado" not in acao, acao
    assert "`localizador_quebrado`" in md.split("## 2. Evidência")[0], "o veredito continua o do diagnóstico"
    # num caso de contrato sem campo, a linha de ação não manda conferir o campo "nenhum"
    t2 = trilha.Trilha(versao=trilha.V2)
    t2.corrida(_cabecalho(), ts=TS)
    tid2 = "fase4_ensaio/qwen2.5_7b/contrato-error_500#1"
    caso2 = cv.montar_caso("contrato-error_500@tela", "GET /api/produtos", 500, "id: inteiro", "(corpo de erro)", "a grade não carregou")
    resposta2 = ("A API devolveu 500.\nCAUSA_RAIZ: erro_interno_do_servidor\nCAMPO: nenhum\nIMPACTO: a grade fica vazia.\nFONTE: [erro_interno_do_servidor]", .9, [(" corpo_vazio", .05)])
    t2.evento("entrada", tid2, {"caso": "contrato-error_500"}, "ao_vivo", ts=TS)
    with _ollama_de_mentira_v2(lambda _p, _c: resposta2, []):
        dv.diagnosticar(t2, tid2, caso2, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=_comum_de_teste(), limiares=None, intervencoes="desligadas", evidencia=[], ts=TS)
    acao2 = grr.relatorio_do_caso_v2(t2.eventos, tid2).split("## 5. Linha de ação")[1].split("## 6.")[0]
    assert "Confira o campo" not in acao2 and "Confira a resposta" in acao2, acao2


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
    # ! Alteração de IA - Revisar: (04/11/2026, P6) o modo `cenarios` entra na tupla.
    # ! Motivo: a corrida 21 é `executar_fase4.py --modo cenarios` (plano aprovado, seção 5, P6).
    # ! Alteração de IA - Revisar: (04/11/2026, P7) a tupla ganha `avaliacao_trilha` (a corrida 22).
    # ! Motivo: plano aprovado, seção 5 (P7); o teste fixa a tupla inteira para um modo novo nunca entrar sem o seu teste.
    assert ex.MODOS == ("reproducao", "calibracao", "tela", "cura", "biblioteca", "cenarios", "avaliacao_trilha", "experimento_prompt", "ineditos")
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
    """`<pasta_bib>/epoca-100` = cópia fechada da L1 curada que a calibração leu (CURADA_DOS_TESTES; hash conferido por
    executar_fase3b._preparar_copia e contra HASH_DA_CURADA_DOS_TESTES)."""
    import executar_fase3b as e3b
    destino = pasta_bib / "epoca-100"
    assert e3b._preparar_copia(CURADA_DOS_TESTES, destino) == HASH_DA_CURADA_DOS_TESTES
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
    aprendidos = [v["id"] for v in bib.carregar(CURADA_DOS_TESTES) if v["pasta"] == "aprendidos"]
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
    # ! Alteração de IA - Revisar: (04/11/2026) o corpo antigo deixa de ser prefixo do novo: as seções de correção entram
    # antes de "## Notas do modelo", que continua a última seção; nada removido passa a ser conferido linha a linha
    # (insercao_so_de_correcao, mais o laço das linhas na ordem logo abaixo).
    # ! Motivo: a corrida 20 parou na sonda porque a correção no fim do arquivo fazia a nota seguinte do modelo cair na
    # seção "Solução aplicada" (ver teste_biblioteca_fase4_nota_da_sonda_depois_da_correcao_fica_em_notas_do_modelo).
    assert bf.insercao_so_de_correcao(corpo_antes, corpo_depois, ["sin-1"]) == [], "nada do corpo antigo foi removido nem trocado de lugar"
    assert [l.strip() for l in corpo_depois.splitlines() if l.startswith("## ")][-1] == "## Notas do modelo"
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


# ! Alteração de IA - Revisar: (04/11/2026) teste da nota que a sonda acrescenta num verbete já corrigido: a correção
# deixa "## Notas do modelo" como a última seção do arquivo, e a nota gravada pelo aplicar_edicao congelado cai dentro dela.
# ! Motivo: a corrida 20 parou na sonda (04/11/2026, 01:46) com "erros/corpo_nao_e_json.md: linha 2 da seção 'Solução
# aplicada' fora do formato '- [caso · data] texto'". A fase C pôs "Solução sugerida" e "Solução aplicada" no fim do
# arquivo, depois das notas, e evolucao_biblioteca.aplicar_edicao (Fase 3, congelada) sempre grava a nota no fim do
# arquivo. A conferência congelada de só acréscimo exige que o corpo novo comece pelo antigo, então a nota do modelo só
# pode entrar no fim; quem muda é a correção, que passa a entrar antes das notas.
def teste_biblioteca_fase4_nota_da_sonda_depois_da_correcao_fica_em_notas_do_modelo():
    import biblioteca as bib
    import biblioteca_fase4 as bf
    import evolucao_biblioteca as evo
    import executar_fase3b as e3b
    pasta_bib, antes = _biblioteca_de_teste()
    e102 = pasta_bib / "epoca-102"
    evo.copiar_biblioteca(antes, e102)
    evo._limpar_gerados(e102)
    v_antes = next(v for v in bib.carregar(antes) if v["id"] == "campo_ausente")
    assert v_antes["secoes"].get("Notas do modelo"), "o verbete do teste precisa ter nota do modelo antes da correção"
    bf.corrigir(e102, "campo_ausente", "sin-1", bf.sugestao_do_modelo(v_antes, "sin-1"),
                "Em 2026-11-03 o cenário api-catalogo voltou a passar com o modo field_missing desligado.", "2026-11-03")
    arq = e102 / "erros" / "campo_ausente.md"
    cabecalhos = [l.strip() for l in arq.read_text(encoding="utf-8").splitlines() if l.startswith("## ")]
    assert cabecalhos[-1] == "## Notas do modelo", cabecalhos
    assert cabecalhos.index("## Solução sugerida") < cabecalhos.index("## Solução aplicada") < cabecalhos.index("## Notas do modelo"), cabecalhos
    assert bf.conferir_correcao(antes, e102, {"campo_ausente": ["sin-1"]}) == [], bf.conferir_correcao(antes, e102, {"campo_ausente": ["sin-1"]})
    # a sonda: a época 103 copia a 102 e o modelo acrescenta uma nota pela função congelada da Fase 3
    e103 = pasta_bib / "epoca-103"
    evo.copiar_biblioteca(e102, e103)
    evo._limpar_gerados(e103)
    edicao = {"epoca": 103, "caso": "sin-1", "numero": 1, "operacao": "nota", "verbete": "campo_ausente",
              "arquivo": "erros/campo_ausente.md", "texto": "Conferir também os itens seguintes da lista, não só o primeiro.",
              "motivo": "o caso sin-1 mostrou o campo faltando só depois do primeiro item.", "trecho": None,
              "palavras_chave_novas": [], "sintomas_novos": [], "novo": None, "modelo": "qwen2.5:7b"}
    evo.aplicar_edicao(e103, edicao)
    v = next(x for x in bib.carregar(e103) if x["id"] == "campo_ausente")
    linha = evo._linha_nota(edicao)
    assert linha in v["secoes"]["Notas do modelo"], v["secoes"]["Notas do modelo"]
    assert linha not in v["secoes"].get("Solução aplicada", ""), "a nota do modelo não pode cair na seção da correção"
    assert bib.validar(bib.carregar(e103), e3b.TODOS_OS_CASOS, teto_global=None) == [], bib.validar(bib.carregar(e103), e3b.TODOS_OS_CASOS, teto_global=None)
    assert evo.conferir_somente_acrescimo(e102, e103) == [], "a nota do modelo continua sendo acréscimo no fim do arquivo"
    assert [c["caso"] for c in bib.correcoes(v)] == ["sin-1"] and bf.sugestao_do_modelo(v, "sin-1")
    # uma segunda correção no verbete já anotado continua entrando antes das notas
    bf.corrigir(e103, "campo_ausente", "sin-2", "", "Em 2026-11-04 o cenário api-detalhe voltou a passar.", "2026-11-04")
    cabecalhos = [l.strip() for l in (e103 / "erros" / "campo_ausente.md").read_text(encoding="utf-8").splitlines() if l.startswith("## ")]
    assert cabecalhos[-1] == "## Notas do modelo" and cabecalhos.count("## Solução aplicada") == 1, cabecalhos
    # a correção que apaga ou reordena uma linha antiga é acusada pela conferência própria da correção
    estragada = pasta_bib / "epoca-estragada"
    evo.copiar_biblioteca(e102, estragada)
    arq_e = estragada / "erros" / "campo_ausente.md"
    linhas_e = arq_e.read_text(encoding="utf-8").splitlines()
    resumo = next(i for i, l in enumerate(linhas_e) if l.strip() == "## Resumo")
    del linhas_e[resumo + 1]
    arq_e.write_text("\n".join(linhas_e) + "\n", encoding="utf-8")
    assert any("sumiu" in x or "lugar" in x for x in bf.conferir_correcao(antes, estragada, {"campo_ausente": ["sin-1"]})), bf.conferir_correcao(antes, estragada, {"campo_ausente": ["sin-1"]})


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


# ! Alteração de IA - Revisar: (04/11/2026) teste de biblioteca_fase4.gravar_planilha_de_revisao: a planilha é regravada
# quando não existe ou quando as células de Avaliação e Comentário estão todas como o harness deixou (inclusive a de um
# lote antigo); com alguma célula mexida à mão, ela fica e a versão nova vai para revisao_do_lote.nova.md.
# ! Motivo: a fase B regravava revisao_do_lote.md a cada partida da corrida, inclusive na retomada; se o Eric preenchesse a
# planilha e a corrida fosse relançada (como a corrida 20 em 04/11/2026), a revisão humana sumiria sem aviso, e ela é a
# porta final da promoção (biblioteca_fase4.py --promover).
def teste_biblioteca_fase4_planilha_preenchida_nao_e_regravada_na_retomada():
    import biblioteca_fase4 as bf
    pasta = _temp()
    arq = pasta / "revisao_do_lote.md"
    nova = pasta / "revisao_do_lote.nova.md"
    texto = bf.planilha_de_revisao([{"verbete": "campo_ausente", "operacao": "nota", "caso": "sin-1", "texto": "t", "motivo": "m"}], {}, "fase4_biblioteca")
    assert bf.gravar_planilha_de_revisao(arq, texto) == "gravada" and arq.read_text(encoding="utf-8") == texto
    assert bf.gravar_planilha_de_revisao(arq, texto) == "gravada" and not nova.exists(), "a planilha em branco igual é regravada sem efeito"
    # a planilha em branco de um lote antigo é trocada pela do lote novo (ninguém começou a revisão)
    outra = bf.planilha_de_revisao([{"verbete": "corpo_vazio", "operacao": "nota", "caso": "lex-13", "texto": "u", "motivo": "n"}], {}, "fase4_biblioteca")
    assert bf.gravar_planilha_de_revisao(arq, outra) == "gravada" and arq.read_text(encoding="utf-8") == outra and not nova.exists()
    assert bf.gravar_planilha_de_revisao(arq, texto) == "gravada"
    so_comentario = texto.replace("| (em branco) |  |", "| (em branco) | olhar de novo |")
    arq.write_text(so_comentario, encoding="utf-8", newline="\n")
    assert bf.gravar_planilha_de_revisao(arq, texto) == "mantida" and arq.read_text(encoding="utf-8") == so_comentario, "um comentário já conta como revisão começada"
    nova.unlink()
    preenchida = texto.replace("| (em branco) |", "| Correta |")
    arq.write_text(preenchida, encoding="utf-8", newline="\n")
    assert bf.gravar_planilha_de_revisao(arq, texto) == "mantida"
    assert arq.read_text(encoding="utf-8") == preenchida, "a revisão feita à mão não pode ser apagada"
    assert nova.read_text(encoding="utf-8") == texto, "a versão nova fica ao lado para a comparação"


# ! Alteração de IA - Revisar: (04/11/2026) teste de biblioteca_fase4.promover com os vereditos da planilha: entra na produção
# só o que não é Errada (a política da curadoria da L1, ficha 2), a edição segurada pela regra dos 40% entra quando aprovada,
# uma nota que depende de verbete novo que saiu também sai, e a promoção recusa veredito fora de Correta/Parcial/Errada e
# reconstrução que não reproduz a época do lote, sem tocar na produção.
# ! Motivo: o --promover do P5 copiava a época 101 inteira e só conferia se a planilha estava preenchida; uma edição marcada
# Errada entrava na produção do mesmo jeito, e a segurada nunca entrava, porque não está na época 101. A pré-revisão de
# 04/11/2026 marcou 9 das 20 linhas do lote da corrida 20 como Errada.
def teste_biblioteca_fase4_promover_aplica_so_o_que_nao_e_errada_e_a_segurada_aprovada():
    import re

    import biblioteca as bib
    import biblioteca_fase4 as bf
    import evolucao_biblioteca as evo
    import executar_fase3b as e3b

    def nota(caso: str, verbete: str, arquivo: str, texto: str) -> dict:
        return {"epoca": 101, "caso": caso, "numero": 1, "operacao": "nota", "verbete": verbete, "arquivo": arquivo, "texto": texto,
                "motivo": "o caso mostrou isso no fio.", "trecho": None, "palavras_chave_novas": [], "sintomas_novos": [], "novo": None,
                "modelo": "qwen2.5:7b"}

    def preencher(planilha: str, vereditos: dict) -> str:
        saida = []
        for linha in planilha.splitlines():
            m = re.match(r"^\| \d+ \| `([^`]+)` \| \w+ \| ([a-z]+-\d+) \|", linha)
            if m:
                linha = linha.rstrip()[: -len("| (em branco) |  |")] + f"| {vereditos[(m.group(2), m.group(1))]} | conferido |"
            saida.append(linha)
        return "\n".join(saida) + "\n"

    _, curada = _biblioteca_de_teste()
    e_ok = nota("sin-1", "campo_ausente", "erros/campo_ausente.md", "Conferir também os itens seguintes da lista, não só o primeiro.")
    e_novo = {**nota("tra-6", "verbete_errado", "aprendidos/verbete_errado.md", "Formatar o preço no front no padrão brasileiro."),
              "operacao": "novo_verbete", "palavras_chave_novas": ["formatacao"],
              "novo": {"titulo": "Verbete errado", "sistema": "CobaiaFront", "entidade": "Interface", "causas": ["escala_ou_unidade_errada"], "arquivos": []}}
    e_dep = nota("tra-7", "verbete_errado", "aprendidos/verbete_errado.md", "Nota no verbete novo, que depende dele.")
    e_parcial = nota("lex-13", "corpo_vazio", "erros/corpo_vazio.md", "O corpo vazio aparece também com status 200.")
    segurada = {**nota("efe-4", "contrato-produto", "contratos/contrato-produto.md", "A lista de produtos é lida por produtos.map."), "para_revisao": True}
    edicoes = [e_ok, e_novo, e_dep, e_parcial]

    def montar(nome: str, aplicar: list[dict], vereditos: dict) -> tuple[Path, Path, Path]:
        producao = _temp() / "producao"
        evo.copiar_biblioteca(curada, producao)
        raiz = _temp() / nome
        e101 = raiz / "bibliotecas" / "qwen2.5_7b" / "epoca-101"
        evo.copiar_biblioteca(producao, e101)
        evo._limpar_gerados(e101)
        for e in aplicar:
            evo.aplicar_edicao(e101, e)
        evo.fechar_snapshot(e101, 101, "qwen2.5:7b", len(aplicar))
        (raiz / "lote.json").write_text(json.dumps({"edicoes": edicoes, "para_revisao": [segurada], "r5": {"veredito": "aceito"},
                                                    "versao_ollama": "0.40.14"}, ensure_ascii=False), encoding="utf-8")
        (raiz / "revisao_do_lote.md").write_text(preencher(bf.planilha_de_revisao(edicoes + [segurada], {}, nome), vereditos), encoding="utf-8")
        return producao, raiz, e101

    vereditos = {("sin-1", "campo_ausente"): "Correta", ("tra-6", "verbete_errado"): "Errada", ("tra-7", "verbete_errado"): "Correta",
                 ("lex-13", "corpo_vazio"): "Parcial", ("efe-4", "contrato-produto"): "Correta"}
    producao, raiz, _ = montar("fase4_biblioteca", edicoes, vereditos)
    antes = _temp() / "antes"
    evo.copiar_biblioteca(producao, antes)
    r = bf.promover("fase4_biblioteca", destino=producao, raiz=raiz)
    vs = {v["id"]: v for v in bib.carregar(producao)}
    assert "verbete_errado" not in vs and not (producao / "aprendidos" / "verbete_errado.md").exists(), "a edição Errada não entra"
    assert evo._linha_nota(e_ok) in vs["campo_ausente"]["secoes"]["Notas do modelo"]
    assert evo._linha_nota(e_parcial) in vs["corpo_vazio"]["secoes"]["Notas do modelo"], "Parcial entra"
    assert evo._linha_nota(segurada) in vs["contrato-produto"]["secoes"]["Notas do modelo"], "a segurada aprovada entra"
    assert r["mantidas"] == 3, r
    assert sorted((x["caso"], x["motivo_da_saida"]) for x in r["removidas"]) == [("tra-6", "Errada"), ("tra-7", "depende de verbete que saiu")], r["removidas"]
    assert bib.validar(list(vs.values()), e3b.TODOS_OS_CASOS, teto_global=None) == []
    assert evo.conferir_somente_acrescimo(antes, producao) == [], "a promoção é só acréscimo sobre a produção de antes"
    fech = json.loads((producao / "fechamento.json").read_text(encoding="utf-8"))
    assert fech["origem_do_lote"] == "fase4_biblioteca" and fech["politica"] == {"remover": ["Errada"]} and len(fech["removidas"]) == 2
    assert fech["hash"] == evo.hash_biblioteca(producao) and fech["hash_anterior"] == evo.hash_biblioteca(antes)
    # veredito fora dos três: recusa antes de tocar na produção
    producao2, raiz2, _ = montar("fase4_invalido", edicoes, {**vereditos, ("lex-13", "corpo_vazio"): "Talvez"})
    h0 = evo.hash_biblioteca(producao2)
    try:
        bf.promover("fase4_invalido", destino=producao2, raiz=raiz2)
    except SystemExit as e:
        assert "Talvez" in str(e), e
    else:
        raise AssertionError("a promoção aceitou um veredito fora de Correta/Parcial/Errada")
    assert evo.hash_biblioteca(producao2) == h0
    # a época do lote não é a produção mais as edições do lote.json: recusa, sem tocar na produção
    producao3, raiz3, _ = montar("fase4_infiel", [e_ok, e_parcial], vereditos)
    h0 = evo.hash_biblioteca(producao3)
    try:
        bf.promover("fase4_infiel", destino=producao3, raiz=raiz3)
    except SystemExit as e:
        assert "fiel" in str(e), e
    else:
        raise AssertionError("a promoção aceitou uma época do lote que a reconstrução não reproduz")
    assert evo.hash_biblioteca(producao3) == h0


# ! Alteração de IA - Revisar: (04/11/2026) teste de biblioteca_fase4.mover_para_espera com `avaliados`: só sai da produção o
# aprendido que a calibração leu e nunca recuperou; um aprendido que entrou depois (pela promoção do lote) fica.
# ! Motivo: sem a lista dos avaliados, a espera contava os aprendidos da produção atual; depois da promoção da corrida 20 os
# três verbetes novos, que nem existiam na calibração, teriam zero recuperações e sairiam junto com os quatro da ficha 32.
def teste_biblioteca_fase4_espera_so_move_os_aprendidos_que_a_calibracao_avaliou():
    import biblioteca as bib
    import biblioteca_fase4 as bf
    import evolucao_biblioteca as evo
    _, curada = _biblioteca_de_teste()
    producao = _temp() / "producao"
    evo.copiar_biblioteca(curada, producao)
    avaliados = sorted(v["id"] for v in bib.carregar(producao) if v["pasta"] == evo.PASTA_APRENDIDOS)
    assert len(avaliados) == 4, avaliados
    novo = {"epoca": 101, "caso": "efe-8", "numero": 1, "operacao": "novo_verbete", "verbete": "atualizacao-da-tela",
            "arquivo": "aprendidos/atualizacao-da-tela.md", "texto": "A grade só é montada no then() do fetch.", "motivo": "o caso mostrou isso.",
            "trecho": None, "palavras_chave_novas": ["fetch"], "sintomas_novos": [], "modelo": "qwen2.5:7b",
            "novo": {"titulo": "Atualização da tela", "sistema": "CobaiaFront", "entidade": "Interface", "causas": ["estado_da_tela_divergente"], "arquivos": []}}
    evo.aplicar_edicao(producao, novo)
    espera = _temp() / "espera"
    movidos = bf.mover_para_espera(origem=producao, destino=espera, registros=[], avaliados=avaliados)
    assert sorted(movidos) == avaliados, movidos
    restantes = {v["id"] for v in bib.carregar(producao) if v["pasta"] == evo.PASTA_APRENDIDOS}
    assert restantes == {"atualizacao-da-tela"}, "o aprendido que a calibração não leu fica na produção"
    assert sorted(p.stem for p in espera.glob("*.md")) == avaliados


# ! Alteração de IA - Revisar: (04/11/2026) teste de biblioteca_fase4.mover_para_espera sobre uma produção já promovida: o
# fechamento.json regravado pela espera guarda os campos que a promoção escreveu (o lote, a planilha, a política, o que ficou e o que
# saiu, o hash de antes da promoção) e anota à parte o hash de antes da espera.
# ! Motivo: no fechar_p5.ps1 de 04/11/2026 o --espera rodou logo depois do --promover e regravou o fechamento só com as estatísticas
# novas: a origem do lote sumiu (o lancar_corrida21.ps1 confere esse campo) e o hash_anterior da promoção foi trocado pelo de antes
# da espera.
def teste_biblioteca_fase4_espera_guarda_no_fechamento_o_que_a_promocao_gravou():
    import biblioteca_fase4 as bf
    import evolucao_biblioteca as evo
    _, producao = _biblioteca_de_teste()
    arq = producao / "fechamento.json"
    promocao = {"origem_do_lote": "fase4_biblioteca", "hash_anterior": "1fca10f1a6f6", "hash_do_lote": "9f3154eee72d",
                "planilha": "revisao_do_lote.md", "politica": {"remover": ["Errada"]}, "mantidas": 11,
                "removidas": [{"caso": "tra-5", "verbete": "pessoas_incorretas"}], "promovido_em": "2026-11-04T20:03:06"}
    antes = json.loads(arq.read_text(encoding="utf-8"))
    assert not antes.get("aprendidos_em_espera"), "a cópia da L1 de antes da promoção ainda não tem espera"
    arq.write_text(json.dumps({**antes, **promocao}, ensure_ascii=False), encoding="utf-8")
    aprendidos = sorted(v["id"] for v in evo._carregar_verbetes(producao) if v["pasta"] == evo.PASTA_APRENDIDOS)
    espera = _temp() / "espera"
    movidos = bf.mover_para_espera(origem=producao, destino=espera, ids=aprendidos[:1], avaliados=aprendidos)
    assert movidos == aprendidos[:1], movidos
    depois = json.loads(arq.read_text(encoding="utf-8"))
    for chave, valor in promocao.items():
        assert depois.get(chave) == valor, (chave, depois.get(chave))
    assert depois["aprendidos_em_espera"] == aprendidos[:1], depois["aprendidos_em_espera"]
    assert depois["hash_antes_da_espera"] == antes["hash"] and depois["hash"] != antes["hash"]
    assert depois["n_verbetes"] == antes["n_verbetes"] - 1, "as estatísticas são as da biblioteca depois da espera"
    # uma segunda espera soma à lista e não apaga o que a promoção gravou
    bf.mover_para_espera(origem=producao, destino=espera, ids=aprendidos[1:2], avaliados=aprendidos)
    terceiro = json.loads(arq.read_text(encoding="utf-8"))
    assert terceiro["aprendidos_em_espera"] == aprendidos[:2] and terceiro["hash_antes_da_espera"] == depois["hash"]
    assert all(terceiro.get(chave) == valor for chave, valor in promocao.items())


# ! Alteração de IA - Revisar: (04/11/2026) teste de executar_fase4.descartar_eventos_da_correcao: refazer a fase C tira da
# trilha tudo desde o primeiro evento de um caso '@correcao' (as telas de antes e depois, os blobs, a edição e o nó).
# ! Motivo: a fase C é refeita do zero quando a época 102 ou o correcoes.jsonl faltam; é assim que a corrida 20 vai ser
# retomada em 04/11/2026, depois do conserto da ordem das seções. Sem o corte, os 10 casos apareceriam duas vezes na
# trilha e nos relatórios '@correcao'.
def teste_executar_fase4_refazer_a_correcao_descarta_da_trilha_os_eventos_da_fase_c():
    import executar_fase4 as ex
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(), ts=TS)
    t.evento("entrada", "f/m/lex-2@tela", {"caso": "lex-2"}, "ao_vivo", ts=TS)
    t.evento("entrada", "f/m/lex-16@lote", {"caso": "lex-16"}, "ao_vivo", ts=TS)
    n_antes = len(t.eventos)
    t.evento("entrada", "f/m/lex-2@correcao/antes", {"caso": "lex-2"}, "ao_vivo", ts=TS)
    t.blob("árvore da tela de depois", "arvore")
    t.evento("edicao_biblioteca", "f/m/lex-2@correcao", {"etapa": "correcao"}, "ao_vivo", ts=TS)
    assert ex.descartar_eventos_da_correcao(t) == 3
    assert len(t.eventos) == n_antes and not any("@correcao" in (e["trilha"] or "") for e in t.eventos)
    assert ex.descartar_eventos_da_correcao(t) == 0, "sem eventos da fase C, nada a descartar"


def teste_executar_fase4_modo_biblioteca_partes_puras():
    import executar_fase4 as ex
    # ! Alteração de IA - Revisar: (04/11/2026, P6) o modo `cenarios` entra na tupla.
    # ! Motivo: a corrida 21 é `executar_fase4.py --modo cenarios` (plano aprovado, seção 5, P6).
    # ! Alteração de IA - Revisar: (04/11/2026, P7) a tupla ganha `avaliacao_trilha` (a corrida 22).
    # ! Motivo: plano aprovado, seção 5 (P7); o teste fixa a tupla inteira para um modo novo nunca entrar sem o seu teste.
    assert ex.MODOS == ("reproducao", "calibracao", "tela", "cura", "biblioteca", "cenarios", "avaliacao_trilha", "experimento_prompt", "ineditos")
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
    # os casos de aprendizado ligados a notas da L1 curada e com tela: os dez conhecidos (na cópia que a calibração leu; a produção
    # promovida em 04/11/2026 liga mais casos)
    lig = ex.casos_ligados_com_tela(_curada()[0])
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


# ! Alteração de IA - Revisar: teste da ponte de versão 0.40.14 (03/11/2026): a pasta `fase3b_ponte_04014` entra em
# analisar_fase3b.PONTES antes de a corrida rodar, e uma pasta listada sem diagnosticos__L0.jsonl não vira ponte em
# avaliar_fase4.pontes_conhecidas nem libera a regra R6 (executar_fase4.versao_precisa_de_ponte).
# ! Motivo: o aplicativo Ollama se atualizou sozinho de 0.40.2 para 0.40.14 em 03/11/2026 às 15:34 e as duas partidas da
# corrida 20 (15:38 e 15:41) saíram com código 2 pela R6, "a versão 0.40.14 do Ollama não tem ponte completa
# registrada". A cadeia da noite roda a ponte (rodar_fase3b.ps1 -Modo ponte, o mesmo caminho das pontes 0.34.1,
# 0.34.4 e 0.40.2) e regrava pontes.json com `avaliar_fase4.py --pontes`, que só lê as pastas da lista; listar a pasta
# antes é seguro porque pontes_conhecidas pula o que ainda não existe, e isto fica provado aqui.
def teste_pontes_conhecidas_ignora_ponte_listada_que_ainda_nao_rodou():
    """A ponte 0.40.14 está na lista e a linha de base da cruzada não muda; uma pasta listada que ainda não rodou não
    entra em pontes.json, e sem ela a regra R6 continua exigindo a ponte."""
    import analisar_fase3b as a3b
    import avaliar_fase4 as av
    import executar_fase4 as ex
    assert "fase3b_ponte_04014" in a3b.PONTES, a3b.PONTES
    assert a3b.PONTE_DA_CRUZADA == "fase3b_ponte_0344", "a linha de base da cruzada não muda com a ponte nova (decisão 69)"
    original = a3b.PONTES
    a3b.PONTES = ["fase3b_ponte_0402", "fase3b_ponte_que_nao_rodou"]
    try:
        dado = av.pontes_conhecidas()
    finally:
        a3b.PONTES = original
    corridas = [p["corrida"] for p in dado["pontes"]]
    assert "fase3b_ponte_que_nao_rodou" not in corridas and "fase3b_ponte_0402" in corridas, corridas
    assert ex.versao_precisa_de_ponte("0.40.14", dado) is True and ex.versao_precisa_de_ponte("0.40.2", dado) is False


# ----------------------------------------------------------------------------- P6: cenários da Fase 5, MTTR e Task Success

# ! Alteração de IA - Revisar: (04/11/2026, P6) testes escritos antes do código: o catálogo dos dez cenários da ficha 36, o
# cronômetro (da detecção à reexecução validada, ou ao diagnóstico conferido no contrato), o Task Success (roteiro concluído
# sem erro; no contrato, causa e campo certos), o banco restaurado e conferido por hash no começo de cada repetição, a versão do
# navegador igual em todas as repetições, as partes puras do modo `cenarios` e a leitura com reamostragem e Wilson.
# ! Motivo: plano aprovado, seção 5 (P6), e fichas 35 e 36 (decisão 79); a corrida 21 (ensaio de uma repetição) e a Fase 5 leem
# estes números, e sem os testes o MTTR e o Task Success dependeriam de conta feita no meio da corrida.
_RESPOSTA = "O preço não veio.\nCAUSA_RAIZ: {causa}\nCAMPO: {campo}\nIMPACTO: o botão mostra undefined.\nFONTE: [campo_ausente]"
_CASO_DE_CONTRATO = {"id": "contrato-field_missing@cenario", "origem": "ao_vivo",
                     "entrada": {"requisicao": "GET /api/produtos", "status": 200, "contrato": "id: inteiro | nome: texto | preco: numero",
                                 "corpo": '[{"id": 1, "nome": "Picanha ao Alho"}]', "sintoma": "o botão de preço mostra undefined."}}


def teste_cenarios_fase5_catalogo_dez_cenarios_da_ficha_36():
    import cenarios_fase4 as cen
    c = list(cen.CENARIOS_DO_ENSAIO)
    assert len(c) == 10 and len({x["id"] for x in c}) == 10, [x["id"] for x in c]
    contrato = [x for x in c if x["tipo"] == "contrato"]
    loc = [x for x in c if x["tipo"] == "localizador"]
    assert len(contrato) == 6 and len(loc) == 4
    # seis de contrato em produtos_api.php, um por modo, cobrindo as cinco classes de contrato (a troca da ficha 36)
    assert all(x["cenario"] == "api-catalogo" for x in contrato) and len({x["modo"] for x in contrato}) == 6
    assert {x["classe"] for x in contrato} == {1, 2, 3, 4, 5}, sorted(x["classe"] for x in contrato)
    for x in contrato:
        assert cen.MODO_POR_CAUSA[x["causa"]] == x["modo"], x
        assert x["campo"] == ("preco" if x["modo"] in cen.MODOS_COM_CAMPO else None), x
    assert cen.TROCA_DA_FICHA_36["sai"] == "latency" and cen.TROCA_DA_FICHA_36["entra"] == "escala_ou_unidade_errada"
    assert "latency" not in {x["modo"] for x in contrato} and cen.TROCA_DA_FICHA_36["motivo"]
    # quatro de localizador, um por roteiro do front legado, com os quatro modos de quebra, armados pelo harness
    assert {x["cenario"] for x in loc} == set(cen.ROTEIROS_DA_CURA) and {x["modo"] for x in loc} == set(cen.MODOS_DE_QUEBRA)
    assert all(x["forma"] == "harness" and x["causa"] == "localizador_quebrado" and x["classe"] == 6 and x["campo"] is None for x in loc)
    for x in loc:
        assert cen.quebra(x["cenario"], x["modo"])["cenario"] == x["cenario"]


def teste_cenarios_fase5_cronometro_comeca_na_deteccao_e_termina_na_validacao():
    import cenarios_fase4 as cen
    import executar_fase4 as ex
    assert cen.mttr_monotonico(10.0, 12.5) == 2.5 and cen.mttr_monotonico(10.0, 12.5, descontar=0.5) == 2.0
    assert cen.mttr_monotonico(None, 12.5) is None and cen.mttr_monotonico(10.0, None) is None
    assert cen.mttr_monotonico(12.5, 10.0) is None, "validação antes da detecção não vale"
    item = next(x for x in cen.CENARIOS_DO_ENSAIO if x["modo"] == "field_missing")
    ok = cen.diagnostico_conferido(_RESPOSTA.format(causa="campo_ausente", campo="preco"), _CASO_DE_CONTRATO)
    # contrato: o cronômetro para no diagnóstico conferido (ficha 35)
    r = ex.registro_do_cenario(item, 1, "156.0", "h-seed", deteccao="2026-11-04T10:00:00", t_deteccao=100.0, t_diagnostico=161.25,
                               conferencia=ok, rotulo="campo_ausente", p_rotulo=0.91)
    assert r["mttr_s"] == 61.25 and r["task_success"] is True and r["cenario"] == item["id"] and r["repeticao"] == 1
    # diagnóstico que não passa na conferência (sem a linha FONTE): sem MTTR e sem Task Success
    ruim = cen.diagnostico_conferido("CAUSA_RAIZ: campo_ausente\nCAMPO: preco\nIMPACTO: x.", _CASO_DE_CONTRATO)
    r = ex.registro_do_cenario(item, 1, "156.0", "h-seed", deteccao="2026-11-04T10:00:00", t_deteccao=100.0, t_diagnostico=150.0,
                               conferencia=ruim, rotulo="campo_ausente", p_rotulo=0.9)
    assert ruim["conferido"] is False and r["mttr_s"] is None and r["task_success"] is False
    # localizador: o cronômetro para na reexecução validada, descontando a restauração do banco entre as duas
    loc = next(x for x in cen.CENARIOS_DO_ENSAIO if x["tipo"] == "localizador")
    r = ex.registro_do_cenario(loc, 2, "156.0", "h-seed", deteccao="2026-11-04T10:00:00", t_deteccao=200.0, t_diagnostico=260.0,
                               conferencia=None, rotulo="localizador_quebrado", p_rotulo=0.8, cura={"curado": True, "estrategia": "papel_e_nome"},
                               t_validacao=262.5, restauracoes=0.5)
    assert r["mttr_s"] == 62.0 and r["task_success"] is True and r["cura"]["estrategia"] == "papel_e_nome"
    r = ex.registro_do_cenario(loc, 2, "156.0", "h-seed", deteccao="2026-11-04T10:00:00", t_deteccao=200.0, t_diagnostico=260.0,
                               conferencia=None, rotulo="localizador_quebrado", p_rotulo=0.8, cura={"curado": False}, t_validacao=None)
    assert r["mttr_s"] is None and r["task_success"] is False
    # o cenário que não quebrou não tem detecção: nem MTTR nem Task Success
    r = ex.registro_do_cenario(item, 1, "156.0", "h-seed", deteccao=None, t_deteccao=None, t_diagnostico=None, conferencia=None, rotulo=None, p_rotulo=None)
    assert r["detectou"] is False and r["mttr_s"] is None and r["task_success"] is False


def teste_cenarios_fase5_task_success_so_conta_roteiro_concluido_sem_erro():
    import cenarios_fase4 as cen
    assert cen.task_success({"passou": True, "conferencias": [{"passou": True}]}) is True
    assert cen.task_success({"passou": True, "conferencias": [{"passou": True}, {"passou": False}]}) is False
    assert cen.task_success({"passou": False, "conferencias": []}) is False
    certo = cen.diagnostico_conferido(_RESPOSTA.format(causa="campo_ausente", campo="preco"), _CASO_DE_CONTRATO)
    assert certo["conferido"] and cen.task_success_contrato(certo, "campo_ausente", "preco") is True
    campo_errado = cen.diagnostico_conferido(_RESPOSTA.format(causa="campo_ausente", campo="nome"), _CASO_DE_CONTRATO)
    assert campo_errado["conferido"] and cen.task_success_contrato(campo_errado, "campo_ausente", "preco") is False
    causa_errada = cen.diagnostico_conferido(_RESPOSTA.format(causa="tipo_divergente", campo="preco"), _CASO_DE_CONTRATO)
    assert causa_errada["conferido"] and cen.task_success_contrato(causa_errada, "campo_ausente", "preco") is False
    fora = cen.diagnostico_conferido(_RESPOSTA.format(causa="preco_sumiu", campo="preco"), _CASO_DE_CONTRATO)
    assert fora["conferido"] is False and fora["causa_no_conjunto"] is False and cen.task_success_contrato(fora, "campo_ausente", "preco") is False
    campo_de_fora = cen.diagnostico_conferido(_RESPOSTA.format(causa="campo_ausente", campo="desconto"), _CASO_DE_CONTRATO)
    assert campo_de_fora["conferido"] is False and campo_de_fora["campo_no_caso"] is False, "o campo citado tem de existir no caso"
    sem_campo = cen.diagnostico_conferido(_RESPOSTA.format(causa="erro_interno_do_servidor", campo="nenhum"), _CASO_DE_CONTRATO)
    assert sem_campo["conferido"] and cen.task_success_contrato(sem_campo, "erro_interno_do_servidor", None) is True
    assert cen.task_success_contrato(None, "campo_ausente", "preco") is False


def teste_cenarios_fase5_banco_restaurado_e_conferido_no_comeco_de_cada_repeticao():
    import executar_fase4 as ex
    sys.path.insert(0, str(RAIZ))
    import restaurar_banco as rb
    chamadas = []

    def restaurar() -> dict:
        chamadas.append("restaurar")
        return dict(rb.CONTAGENS_DO_SEED)

    hashes = iter(["h-seed", "h-seed", "h-outro"])
    assert ex.preparar_repeticao(1, restaurar, lambda: next(hashes), "h-seed") == "h-seed"
    assert ex.preparar_repeticao(2, restaurar, lambda: next(hashes), "h-seed") == "h-seed"
    try:
        ex.preparar_repeticao(3, restaurar, lambda: next(hashes), "h-seed")
    except SystemExit as e:
        assert "repetição 3" in str(e), e
    else:
        raise AssertionError("a repetição começou com o banco diferente do seed")
    assert chamadas == ["restaurar"] * 3, "o banco é restaurado antes de cada repetição"
    try:
        ex.preparar_repeticao(1, lambda: {**rb.CONTAGENS_DO_SEED, "tbprodutos": 13}, lambda: "h-seed", "h-seed")
    except SystemExit as e:
        assert "contagens" in str(e), e
    else:
        raise AssertionError("a repetição começou com as contagens erradas")
    # com o MariaDB: o hash das tabelas é o mesmo depois de duas restaurações e muda quando uma tabela muda
    import _env_common as env
    cli = env.find_mysql_cli()
    if not cli or not env.ensure_mariadb_running(cli):
        print("  (pulado com aviso: MariaDB não disponível nesta máquina; o hash das tabelas precisa do servidor)")
        return
    try:
        rb.restaurar(cli)
        h1 = rb.hash_das_tabelas(cli)
        rb.restaurar(cli)
        assert rb.hash_das_tabelas(cli) == h1, "duas restaurações dão o mesmo hash"
        rb.executar_sql(cli, f"UPDATE {rb.BANCO}.tbprodutos SET valor_produto = valor_produto + 1 WHERE id_produto = 1;")
        assert rb.hash_das_tabelas(cli) != h1, "mudar um preço muda o hash"
        rb.restaurar(cli)
        assert rb.hash_das_tabelas(cli) == h1
    finally:
        env.stop_managed_mariadbd()


def teste_cenarios_fase5_versao_do_navegador_igual_em_todas_as_repeticoes():
    import executar_fase4 as ex
    assert ex.conferir_navegador(["156.0.8078.4", "156.0.8078.4"]) == "156.0.8078.4"
    assert ex.conferir_navegador([]) is None
    try:
        ex.conferir_navegador(["156.0.8078.4", "157.0.1"])
    except SystemExit as e:
        assert "157.0.1" in str(e) and "156.0.8078.4" in str(e), e
    else:
        raise AssertionError("repetições com versões de navegador diferentes foram aceitas")


def teste_executar_fase4_modo_cenarios_partes_puras():
    import caso_ao_vivo as cv
    import cenarios_fase4 as cen
    import executar_fase4 as ex
    assert "cenarios" in ex.MODOS
    args = ex.montar_parser().parse_args(["--modo", "cenarios", "--saida", "fase4_ensaio", "--repeticoes", "1"])
    assert args.modo == "cenarios" and args.repeticoes == 1
    celulas = ex.celulas_do_ensaio(2)
    assert len(celulas) == 20 and [c["repeticao"] for c in celulas] == [1] * 10 + [2] * 10
    assert [c["cenario"]["id"] for c in celulas[:10]] == [x["id"] for x in cen.CENARIOS_DO_ENSAIO]
    assert celulas[0]["id"] == f"{cen.CENARIOS_DO_ENSAIO[0]['id']}#1" and len({c["id"] for c in celulas}) == 20
    assert len(ex.celulas_do_ensaio(1, casos=3)) == 3, "--casos limita os cenários (corrida parcial)"
    # o caso ao vivo de uma quebra de localizador: a página, o passo que falhou, o seletor que não resolveu e a árvore podada
    loc = next(x for x in cen.CENARIOS_DO_ENSAIO if x["tipo"] == "localizador")
    q = cen.quebra(loc["cenario"], loc["modo"])
    d = {"quebra": q, "r": {"conferencia_falha": {"nome": "passo 3 (clicar #buscar)", "passou": False, "esperado": "clicar #buscar", "observado": None},
                            "erro": "TimeoutError: locator.click", "chamadas": []},
         "podada": {"texto": '- searchbox "search"\n- button "Buscar"', "antes": 40, "depois": 2}}
    caso = ex.caso_do_localizador(loc, d)
    e = caso["entrada"]
    assert caso["origem"] == "ao_vivo" and set(e) <= set(cv.CHAVES_DA_ENTRADA)
    assert e["seletor_quebrado"] == q["localizador"] and e["arvore"].startswith("- searchbox") and e["status"] == 200
    assert e["requisicao"].startswith("GET ") and cen.PAGINA_DA_QUEBRA[loc["cenario"]] in e["requisicao"] and e["sintoma"]


# ! Alteração de IA - Revisar: (04/11/2026, P6) testes da ficha da falha (cen.motivo_do_roteiro e o campo motivo_deteccao do
# registro do ensaio) e do ajudante da sessão manual (linha_de_base_manual.py: roteiro com o seletor do integrante, ordem
# sorteada com semente fixa, planilha modelo, ficha da corrida 21, endereço inicial e lista de passos).
# ! Motivo: o protocolo da linha de base manual entrega ao integrante a mesma falha que o agente recebeu na detecção e confere o
# "corrigido" pela mesma reexecução; sem estes testes, uma mudança no roteiro ou no registro mudaria o que o integrante vê sem
# ninguém perceber.
def teste_cenarios_fase5_ficha_da_falha_diz_o_passo_e_o_que_falhou():
    """A ficha da falha sai do resultado do roteiro: o passo, o que ele fazia e o erro, ou a conferência que falhou com o
    esperado e o observado; é o texto que o ensaio grava e que o integrante da linha de base manual recebe."""
    import cenarios_fase4 as cen
    assert cen.motivo_do_roteiro({"passou": True, "conferencias": []}) is None
    estourou = {"passou": False, "passo_falho": 2, "erro": "TimeoutError: Timeout 5000ms exceeded.\n" + "x" * 400,
                "conferencia_falha": {"nome": "passo 3 (preencher #buscar)", "passou": False, "esperado": "preencher #buscar", "observado": "..."}}
    m = cen.motivo_do_roteiro(estourou)
    assert m.startswith("o passo 3 (preencher #buscar) não terminou: TimeoutError: Timeout 5000ms exceeded. x"), m
    assert "\n" not in m and len(m) < 300, len(m)
    conf = {"passou": False, "passo_falho": 2, "erro": None,
            "conferencia_falha": {"nome": "grid com 14 cartões", "passou": False, "esperado": "14 elementos", "observado": "0 elementos"}}
    assert cen.motivo_do_roteiro(conf) == 'a conferência "grid com 14 cartões" (passo 3) falhou: esperado 14 elementos, observado 0 elementos'


def teste_cenarios_fase5_registro_guarda_a_ficha_da_falha():
    import cenarios_fase4 as cen
    import executar_fase4 as ex
    item = next(x for x in cen.CENARIOS_DO_ENSAIO if x["modo"] == "type_drift")
    r = ex.registro_do_cenario(item, 1, "156.0", "h-seed", deteccao="2026-11-04T10:00:00", t_deteccao=100.0, t_diagnostico=None, conferencia=None,
                               rotulo=None, p_rotulo=None, origem_deteccao="contrato_no_fio", motivo_deteccao="o fio acusou: diff do contrato")
    assert r["motivo_deteccao"] == "o fio acusou: diff do contrato" and r["origem_deteccao"] == "contrato_no_fio"
    r = ex.registro_do_cenario(item, 1, "156.0", "h-seed", deteccao=None, t_deteccao=None, t_diagnostico=None, conferencia=None, rotulo=None,
                               p_rotulo=None, motivo_deteccao="texto que não vale")
    assert r["motivo_deteccao"] is None, "sem detecção não há ficha da falha"


def teste_linha_de_base_manual_roteiro_com_o_seletor_do_integrante():
    """O ajudante da linha de base manual (linha_de_base_manual.py) roda o roteiro com o seletor escrito pelo integrante
    no lugar do localizador quebrado, pela mesma troca que a reexecução da cura do agente usa."""
    import cenarios_fase4 as cen
    import linha_de_base_manual as lbm
    c = next(x for x in cen.CENARIOS_DE_LOCALIZADOR if x["cenario"] == "front-busca")
    q = cen.quebra(c["cenario"], c["modo"])
    base = cen.cenario_com_localizador(cen.cenario(c["cenario"]), q)
    novo = cen.roteiro_com_seletor(base, q, "input[name=search]")
    trocados = [p for p in novo["passos"] if p.get("curado")]
    assert trocados and all(p["seletor"] == "input[name=search]" for p in trocados)
    assert all(p.get("seletor") != q["localizador"] for p in novo["passos"]), "nenhum passo fica com o localizador quebrado"
    assert len(novo["passos"]) == len(base["passos"]) and base["passos"][q["passo_alvo"]]["seletor"] == q["localizador"], "o roteiro de base não muda"
    r, q2 = lbm.roteiro_do_integrante(c["id"], "input[name=search]")
    assert q2 == q and [p.get("seletor") for p in r["passos"]] == [p.get("seletor") for p in novo["passos"]]
    # sem seletor, o roteiro é o do agente, com o localizador quebrado: a ficha da falha do localizador sai dele
    r, q2 = lbm.roteiro_do_integrante(c["id"])
    assert r["passos"][q["passo_alvo"]]["seletor"] == q["localizador"] and not any(p.get("curado") for p in r["passos"])
    for ruim in ("contrato-field_missing", "nao-existe"):
        try:
            lbm.roteiro_do_integrante(ruim, "x")
        except ValueError:
            pass
        else:
            raise AssertionError(f"{ruim} aceito como cenário de localizador")


def teste_linha_de_base_manual_ordem_sorteada_com_semente_fixa_e_planilha_modelo():
    import csv
    import io

    import cenarios_fase4 as cen
    import linha_de_base_manual as lbm
    ordens = lbm.ordem_dos_integrantes()
    ids = [c["id"] for c in cen.CENARIOS_DO_ENSAIO]
    assert sorted(ordens) == [1, 2, 3] and all(sorted(o) == sorted(ids) for o in ordens.values())
    assert ordens == lbm.ordem_dos_integrantes(), "a mesma semente dá a mesma ordem"
    assert len({tuple(o) for o in ordens.values()}) == 3, "cada integrante tem a sua ordem"
    assert lbm.ordem_dos_integrantes(semente=lbm.SEMENTE_DA_ORDEM + 1) != ordens
    # o facilitador chama o cenário pela vez (integrante e posição): o nome, que diz o modo de falha, não aparece na tela
    assert lbm.cenario_da_vez(1, 1) == ordens[1][0] and lbm.cenario_da_vez(3, 10) == ordens[3][9]
    for n, p in ((0, 1), (1, 0), (1, 11)):
        try:
            lbm.cenario_da_vez(n, p)
        except ValueError:
            pass
        else:
            raise AssertionError(f"vez fora da planilha aceita: {n}, {p}")
    linhas = list(csv.reader(io.StringIO(lbm.planilha_modelo(ordens)), delimiter=lbm.SEPARADOR))
    assert lbm.SEPARADOR == ";", "o Excel em português abre em colunas o CSV separado por ponto e vírgula"
    assert tuple(linhas[0]) == lbm.COLUNAS_DA_PLANILHA and len(linhas) == 1 + 30
    assert [x[2] for x in linhas[1:11]] == ordens[1] and all(x[0] == "1" for x in linhas[1:11])
    assert [x[1] for x in linhas[1:11]] == [str(i) for i in range(1, 11)]
    tipos = {c["id"]: c["tipo"] for c in cen.CENARIOS_DO_ENSAIO}
    assert all(x[3] == tipos[x[2]] for x in linhas[1:]) and all(not any(x[4:]) for x in linhas[1:]), "o resto da linha fica em branco para a sessão"


def teste_linha_de_base_manual_ficha_endereco_e_passos_do_cenario():
    import cenarios_fase4 as cen
    import linha_de_base_manual as lbm
    regs = [{"cenario": "contrato-type_drift", "repeticao": 1, "detectou": True, "motivo_deteccao": "o fio acusou: x"},
            {"cenario": "localizador-front-busca", "repeticao": 1, "detectou": False, "motivo_deteccao": None}]
    assert lbm.ficha_da_falha("contrato-type_drift", regs) == "o fio acusou: x"
    assert lbm.ficha_da_falha("localizador-front-busca", regs) is None and lbm.ficha_da_falha("contrato-error_500", regs) is None
    assert lbm.endereco_inicial("contrato-type_drift") == cen.BASE_PADRAO + "produtos_api.php"
    assert lbm.endereco_inicial("localizador-front-admin-produtos") == cen.BASE_PADRAO + "admin/login.php", "o integrante entra pelo login, como o roteiro"
    q = cen.quebra("front-busca", "id_renomeado")
    linhas = lbm.passos_do_roteiro("localizador-front-busca")
    assert len(linhas) == len(cen.cenario("front-busca")["passos"]) and linhas[0].startswith("1. ")
    assert "quebrou" in linhas[q["passo_alvo"]] and q["localizador"] in linhas[q["passo_alvo"]]
    assert sum("quebrou" in x for x in linhas) == 1 and "Picanha" in linhas[2], "o valor preenchido aparece para o integrante"
    assert not any("quebrou" in x for x in lbm.passos_do_roteiro("contrato-type_drift"))
    try:
        lbm.cenario_do_ensaio("nao-existe")
    except ValueError:
        pass
    else:
        raise AssertionError("cenário fora do ensaio aceito")


# ! Alteração de IA - Revisar: (05/11/2026, decisão 90) a leitura dos cenários mede o prompt contra o limite, como a da tela.
# ! Motivo: a corrida 21c existe para os dez prompts caberem em 1409 tokens (ficha 42), e só a leitura da tela dizia isso; sem este bloco, a
# resposta sairia de abrir o cenarios.jsonl à mão.
def teste_avaliar_fase4_cenarios_medem_o_prompt_contra_o_limite():
    import avaliar_fase4 as av
    import cenarios_fase4 as cen
    c = cen.CENARIOS_DO_ENSAIO[0]

    def reg(rep: int) -> dict:
        return {"cenario": c["id"], "tipo": c["tipo"], "modo": c["modo"], "classe": c["classe"], "causa_esperada": c["causa"], "repeticao": rep, "detectou": True,
                "task_success": True, "mttr_s": 60.0, "segundos": 70.0, "rotulo": c["causa"]}

    cal = {"k_escolhido": 3, "por_k": [{"k": 1, "tokens_entrada_max": 900}, {"k": 3, "tokens_entrada_max": 1281}]}
    # os tokens ficam no registro oficial do diagnóstico, e o localizador repete o mesmo id de caso a cada repetição
    diag = [{"caso": "c#1@tela", "tokens_entrada": 1200}, {"caso": "c#2@tela", "tokens_entrada": 1500}, {"caso": "l@cenario", "tokens_entrada": 1450}, {"caso": "l@cenario", "tokens_entrada": 1300}]
    dado = av.resumir_cenarios({"condicoes": {}, "registros": [reg(1), reg(2)], "calibracao": cal, "diagnosticos": diag}, gerado_em="2026-11-05T20:00:00", corrida="x")
    assert dado["prompt"] == {"maximo_da_calibracao": 1281, "limite_mais_10_pct": 1409, "acima": ["c#2@tela", "l@cenario"], "maximo_da_tela": 1500}, dado["prompt"]
    md = av.render_cenarios(dado)
    assert "limite de 1409" in md and "`c#2@tela`" in md, "a leitura diz quem passou do limite"
    sem_tokens = av.resumir_cenarios({"condicoes": {}, "registros": [reg(1)], "calibracao": cal}, gerado_em="2026-11-05T20:00:00", corrida="x")
    assert sem_tokens["prompt"] is None and "limite de" not in av.render_cenarios(sem_tokens), "sem tokens medidos a leitura não pode dizer que nenhum passou"
    sem_calibracao = av.resumir_cenarios({"condicoes": {}, "registros": [reg(1)], "diagnosticos": diag}, gerado_em="2026-11-05T20:00:00", corrida="x")
    assert sem_calibracao["prompt"] is None, "sem a calibração não há limite a citar"


def teste_avaliar_fase4_cenarios_mttr_com_reamostragem_e_task_success_com_wilson():
    import avaliar
    import avaliar_fase4 as av
    import cenarios_fase4 as cen
    import pre_fase4 as pf
    c = list(cen.CENARIOS_DO_ENSAIO)

    def reg(cenario_: dict, rep: int, ts: bool, mttr, seg: float) -> dict:
        return {"cenario": cenario_["id"], "tipo": cenario_["tipo"], "modo": cenario_["modo"], "classe": cenario_["classe"], "causa_esperada": cenario_["causa"],
                "repeticao": rep, "navegador": "156.0.8078.4", "hash_inicio": "h-seed", "detectou": True, "task_success": ts, "mttr_s": mttr,
                "segundos": seg, "rotulo": cenario_["causa"] if ts else "outro", "p_rotulo": 0.9, "conferido": ts}

    regs = [reg(c[0], 1, True, 60.0, 70.0), reg(c[0], 2, True, 62.0, 71.0), reg(c[1], 1, False, None, 65.0), reg(c[1], 2, True, 58.0, 66.0),
            reg(c[6], 1, True, 64.0, 90.0), reg(c[6], 2, True, 66.0, 92.0)]
    # ! Alteração de IA - Revisar: (04/11/2026, P6) a ficha da falha de cada cenário (o que a detecção acusou) entra na tabela.
    # ! Motivo: é a ficha que o protocolo da linha de base manual entrega ao integrante; as repetições iguais aparecem uma vez.
    regs[0]["motivo_deteccao"] = regs[1]["motivo_deteccao"] = 'a conferência "grid com 14 cartões" (passo 3) falhou'
    regs[2]["motivo_deteccao"] = "o roteiro passou na tela, mas o fio acusou: status 500"
    bruto = {"condicoes": {"repeticoes": 2, "parcial": False, "navegador": "156.0.8078.4", "modelo": "qwen2.5:7b"}, "registros": regs}
    dado = av.resumir_cenarios(bruto, gerado_em="2026-11-04T20:00:00", corrida="fase4_ensaio")
    g = dado["geral"]
    assert (g["n"], g["sucessos"]) == (6, 5) and g["task_success_pct"] == round(100 * 5 / 6, 1)
    assert (g["wilson_lo_pct"], g["wilson_hi_pct"]) == avaliar.wilson(5, 6), "avaliar.wilson já devolve pontos percentuais"
    assert g["mttr_media_s"] == round((60 + 62 + 58 + 64 + 66) / 5, 2) and g["mttr_n"] == 5
    assert g["mttr_ic_lo_s"] <= g["mttr_media_s"] <= g["mttr_ic_hi_s"]
    assert av.bootstrap_media([60.0, 62.0, 58.0], semente=7) == av.bootstrap_media([60.0, 62.0, 58.0], semente=7), "a reamostragem tem semente fixa"
    assert av.bootstrap_media([61.0]) == (61.0, 61.0) and av.bootstrap_media([]) == (None, None)
    por = {x["cenario"]: x for x in dado["por_cenario"]}
    assert por[c[1]["id"]]["sucessos"] == 1 and por[c[1]["id"]]["n"] == 2 and por[c[1]["id"]]["mttr_n"] == 1
    assert por[c[0]["id"]]["fichas_da_falha"] == ['a conferência "grid com 14 cartões" (passo 3) falhou']
    assert por[c[1]["id"]]["fichas_da_falha"] == ["o roteiro passou na tela, mas o fio acusou: status 500"] and por[c[6]["id"]]["fichas_da_falha"] == []
    assert {x["tipo"] for x in dado["por_tipo"]} == {"contrato", "localizador"}
    assert dado["tempo"]["segundos_media"] == round(sum(r["segundos"] for r in regs) / 6, 1)
    assert dado["navegador"] == {"versoes": ["156.0.8078.4"], "unica": True} and dado["banco"]["hashes_de_inicio"] == ["h-seed"]
    md = av.render_cenarios(dado)
    for bloco in ("tb_f4_cenarios_resumo", "tb_f4_cenarios_por_cenario", "tb_f4_cenarios_por_tipo", "tb_f4_cenarios_tempo", "tb_f4_cenarios_sem_sucesso"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    # ! Alteração de IA - Revisar: (04/11/2026, leitura da corrida 21) as execuções sem Task Success, com o rótulo e a falha da cura.
    # ! Motivo: na corrida 21 a tabela por cenário só mostrava o zero do login; quem lê a leitura precisa ver que o diagnóstico acertou e
    # que a cura falhou em candidato_invalido, sem abrir o cenarios.jsonl.
    assert [(x["cenario"], x["repeticao"], x["rotulo"]) for x in dado["sem_task_success"]] == [(c[1]["id"], 1, "outro")]
    sem = av.resumir_cenarios({"condicoes": {}, "registros": [{**reg(c[7], 1, False, None, 63.0), "rotulo": c[7]["causa"], "cura": {"curado": False, "falha": "candidato_invalido"}}]},
                              gerado_em="2026-11-04T20:00:00", corrida="x")
    assert sem["sem_task_success"][0]["falha_da_cura"] == "candidato_invalido" and sem["sem_task_success"][0]["detectou"] is True
    assert "candidato_invalido" in av.render_cenarios(sem)
    # ! Alteração de IA - Revisar: (04/11/2026, corrida 21b) a leitura aceita outro título, como as do modo `reproducao`.
    # ! Motivo: a repetição do ensaio grava em cenarios_v2.md e o título fixo diria "corrida 21" nela.
    assert av.TITULO_CENARIOS in av.render_cenarios(sem) and "Título da repetição" in av.render_cenarios(sem, "Título da repetição")
    assert "—" not in md and "→" not in md and "83,3" in md
    assert "O que a detecção acusou" in md and "o roteiro passou na tela, mas o fio acusou: status 500" in md
    pasta = _temp()
    assert pf.fechar(av.NOME_CENARIOS, dado, md, av.PREFIXO_CENARIOS, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert pf.fechar(av.NOME_CENARIOS, dado, md, av.PREFIXO_CENARIOS, check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert av.nome_dos_arquivos(None, "cenarios") == "cenarios" and av.montar_parser().parse_args(["--cenarios", "--saida", "fase4_ensaio"]).cenarios is True
    vazio = av.resumir_cenarios({"condicoes": {}, "registros": []}, gerado_em="2026-11-04T20:00:00", corrida="x")
    assert vazio["geral"]["n"] == 0 and vazio["geral"]["mttr_media_s"] is None and av.render_cenarios(vazio)


# ----------------------------------------------------------------------------- P7: avaliação da própria trilha

# ! Alteração de IA - Revisar: (04/11/2026, P7) testes escritos antes de `avaliacao_trilha.py`, do modo `avaliacao_trilha` de
# `executar_fase4.py`, da leitura `--trilha` de `avaliar_fase4.py` e do modo no `rodar_fase4.ps1`: TPR e TNR contra um gabarito
# sintético; cada mutação (verbete trocado, contrato alterado, seletor quebrado) altera exatamente o nó previsto numa trilha de
# referência sintética; a inferência de base emite os nós `poda`, `recuperacao` e `diagnostico` e a intervenção registra o limite
# inferior quando o rótulo some do `top_logprobs` (risco 6 da especificação), contado pela leitura; a sonda de pós-racionalização
# planta só num verbete entregue que a FONTE não citou; as mutações ao vivo com o Ollama de mentira; as partes puras do modo; a
# leitura com `--check` e a planilha da sessão de revisão. A primeira rodada falha por ModuleNotFoundError em `avaliacao_trilha`,
# o RED aceito para módulo novo.
# ! Motivo: plano aprovado, seção 5 (P7: "testes escritos antes"), e especificação da trilha, seções 5 (sonda), 6.1 (risco 6), 9
# (diff contra a trilha de referência) e 12 (TPR x TNR, injeção programada de falhas, revisão humana).

def teste_avaliacao_trilha_tpr_tnr_contra_gabarito_sintetico():
    import avaliacao_trilha as at
    # 3 erros (2 sinalizados) e 3 acertos (1 sinalizado): TPR 2/3, TNR 2/3, produto 4/9; o acaso é 0,25
    linhas = [{"acerto": False, "sinal": True}, {"acerto": False, "sinal": True}, {"acerto": False, "sinal": False},
              {"acerto": True, "sinal": True}, {"acerto": True, "sinal": False}, {"acerto": True, "sinal": False}]
    r = at.tpr_tnr(linhas)
    assert (r["erros"], r["acertos"], r["vp"], r["fn"], r["fp"], r["vn"]) == (3, 3, 2, 1, 1, 2), r
    assert math.isclose(r["tpr"], 2 / 3) and math.isclose(r["tnr"], 2 / 3) and math.isclose(r["produto"], 4 / 9) and r["acaso"] == 0.25
    # ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) o intervalo de Wilson do TPR e do TNR, e o sinal por_gatilho.
    # ! Motivo: a corrida 22 teve 5 erros: sem o intervalo, um TPR de 0,8 parece firme; e as quatro intervenções rodaram em todos os casos
    # só pela amostra fixa da avaliação, então a divergência medida não é a que o agente mostra fora dela.
    import avaliar
    assert r["ic_tpr"] == avaliar.wilson(2, 3) and r["ic_tnr"] == avaliar.wilson(2, 3), r
    assert str(at.tpr_tnr([{"acerto": False, "sinal": False}] * 5)["ic_tpr"][0]) == "0.0", "um sinal que nao pega nenhum erro comeca em 0,0, nao em -0,0"
    # sinal em todos: pega todo erro, mas nenhum acerto fica sem sinal; o produto é zero
    tudo = at.tpr_tnr([{**l, "sinal": True} for l in linhas])
    assert tudo["tpr"] == 1.0 and tudo["tnr"] == 0.0 and tudo["produto"] == 0.0
    # sem erro não há TPR nem produto; sem acerto não há TNR
    so_acertos = at.tpr_tnr([l for l in linhas if l["acerto"]])
    assert so_acertos["tpr"] is None and so_acertos["produto"] is None and so_acertos["tnr"] is not None and so_acertos["ic_tpr"] is None
    assert at.tpr_tnr([])["produto"] is None and at.tpr_tnr([])["tnr"] is None
    # os sinais de um caso, lidos do registro da corrida: o principal é a divergência do nó; os decompostos dizem de onde ela veio
    linha = {"divergencia": True, "selo": "baixo", "falha": None,
             "intervencoes": [{"tipo": "remocao", "mudou_rotulo": False}, {"tipo": "troca", "mudou_rotulo": False},
                              {"tipo": "sem_documentacao", "mudou_rotulo": True}, {"tipo": "repeticao_da_base", "mudou_rotulo": False}]}
    s = at.sinais_do_caso(linha)
    assert s["divergencia"] is True and s["remocao_ou_troca"] is False and s["sem_documentacao"] is True and s["repeticao_mudou"] is False
    assert s["selo_baixo"] is True and s["falha"] is False and s["qualquer"] is True
    assert [n for n, _ in at.SINAIS] == ["divergencia", "por_gatilho", "regra_b", "regra_b_por_gatilho", "remocao_ou_troca", "sem_documentacao", "repeticao_mudou", "selo_baixo", "falha", "qualquer"]
    # a divergência como ficaria fora da avaliação: a conferência em código vale sempre; a intervenção só conta quando a probabilidade
    # baixa ou a FONTE divergente a dispararia (a amostra fixa, que é o que fez as quatro rodarem em todos, não conta)
    so_amostra = {"probabilidade": False, "fonte_divergente": False, "amostra": True, "algum": True}
    assert s["por_gatilho"] is False, "sem gatilhos registrados, a intervenção não teria rodado"
    assert at.sinais_do_caso({**linha, "gatilhos": so_amostra})["por_gatilho"] is False, "a intervenção mudou o rótulo, mas só rodou pela amostra"
    assert at.sinais_do_caso({**linha, "gatilhos": {**so_amostra, "probabilidade": True}})["por_gatilho"] is True
    assert at.sinais_do_caso({**linha, "gatilhos": {**so_amostra, "fonte_divergente": True}})["por_gatilho"] is True
    calmas = [{"tipo": "remocao", "mudou_rotulo": False}]
    assert at.sinais_do_caso({"divergencia": False, "selo": "baixo", "falha": None, "intervencoes": calmas, "gatilhos": {**so_amostra, "probabilidade": True}})["por_gatilho"] is False
    assert at.sinais_do_caso({"divergencia": True, "selo": "alto", "falha": "campo_errado", "intervencoes": [], "gatilhos": so_amostra})["por_gatilho"] is True, "a conferência em código não depende de gatilho"
    # ! Alteração de IA - Revisar: (05/11/2026, ficha 39) os sinais da opção (b) da ficha: a inferência sem documentação deixa de contar, com as intervenções em todos os casos e por gatilho.
    # ! Motivo: a ficha compara as opções do carimbo de conflito, e os números dela precisam sair do avaliador, não de um script solto.
    assert s["regra_b"] is False, "só a inferência sem documentação mudou: pela opção (b), não acende"
    assert at.sinais_do_caso({**linha, "gatilhos": {**so_amostra, "probabilidade": True}})["regra_b_por_gatilho"] is False
    troca_mudou = [{"tipo": "troca", "mudou_rotulo": True}]
    com_troca = {"divergencia": True, "selo": "alto", "falha": None, "intervencoes": troca_mudou}
    assert at.sinais_do_caso({**com_troca, "gatilhos": so_amostra})["regra_b"] is True
    assert at.sinais_do_caso({**com_troca, "gatilhos": so_amostra})["regra_b_por_gatilho"] is False, "a troca só rodou pela amostra"
    assert at.sinais_do_caso({**com_troca, "gatilhos": {**so_amostra, "fonte_divergente": True}})["regra_b_por_gatilho"] is True
    com_falha = at.sinais_do_caso({"divergencia": True, "selo": "alto", "falha": "campo_errado", "intervencoes": [], "gatilhos": so_amostra})
    assert com_falha["regra_b"] is True and com_falha["regra_b_por_gatilho"] is True, "a conferência em código conta nas duas"
    nada = at.sinais_do_caso({"divergencia": False, "selo": "alto", "falha": None, "intervencoes": []})
    assert not any(nada.values())
    assert at.sinais_do_caso({"divergencia": False, "selo": "alto", "falha": "campo_errado", "intervencoes": []})["qualquer"] is True


def _trilha_de_nos(t, tid: str, nos: list) -> None:
    """Emite na trilha v2 `t` os nós de decisão (decisão, escolha) da trilha `tid`, na ordem dada."""
    for decisao, escolha in nos:
        t.decisao(tid, _no(decisao=decisao, escolha=escolha, alternativas=[{"opcao": escolha, "escore": 1.0}]), ts=TS)


def teste_avaliacao_trilha_cada_mutacao_altera_so_o_no_previsto():
    import avaliacao_trilha as at
    import cenarios_fase4 as cen
    import poda
    assert at.MUTACOES == ("verbete_trocado", "contrato_alterado", "seletor_quebrado")
    assert at.NO_PREVISTO == {"verbete_trocado": "recuperacao", "contrato_alterado": "poda", "seletor_quebrado": "cura"}
    # o contrato mutado: o primeiro campo cujo valor no corpo concorda com o contrato troca de tipo; o resto fica byte a byte
    contrato = "id: inteiro | nome: texto | resumo: texto|nulo | preco: numero"
    corpo = '[{"id": 1, "nome": "Picanha ao Alho", "resumo": null, "preco": 89.9}]'
    m = at.mutar_contrato(contrato, corpo)
    assert m["aplicavel"] is True and m["campo"] == "id" and m["de"] == "inteiro" and m["para"] == "texto", m
    assert m["contrato"] == "id: texto | nome: texto | resumo: texto|nulo | preco: numero"
    antes, depois = poda.diff_contrato(contrato, corpo), poda.diff_contrato(m["contrato"], corpo)
    assert at.resumo_do_diff(antes) == "json/lista; sem diferença" and at.resumo_do_diff(depois) == "json/lista; id:tipo_diferente"
    # o campo que já diverge não serve de alvo (a mutação tem de criar uma diferença nova); texto vira inteiro
    m2 = at.mutar_contrato("preco: numero | nome: texto", '{"preco": "89.9", "nome": "Picanha"}')
    assert m2["aplicavel"] and m2["campo"] == "nome" and m2["para"] == "inteiro" and m2["contrato"] == "preco: numero | nome: inteiro"
    for contrato_, corpo_, motivo in (("n/a", "(nenhuma requisicao falhou)", "contrato"), (contrato, '[{"id": 1, "nome": "Pic', "JSON"),
                                       (contrato, '[{"id": "x", "nome": 2}]', "concorda")):
        r = at.mutar_contrato(contrato_, corpo_)
        assert r["aplicavel"] is False and motivo in r["motivo"], r
    assert at.resumo_do_diff(poda.diff_contrato("n/a", "(nenhuma requisicao falhou)")) == "nao_json"
    assert at.resumo_do_diff(poda.diff_contrato(contrato, '[{"id": 1, "nome": "Pic')) == "truncado"
    # trilha de referência sintética de um caso de texto (poda, recuperacao, diagnostico): cada mutação muda só o nó previsto
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(), ts=TS)
    ref = [("poda", "json/lista; sem diferença"), ("recuperacao", "entidade-produto,contrato-produto,resposta_truncada"), ("diagnostico", "campo_renomeado")]
    _trilha_de_nos(t, "ref", ref)
    _trilha_de_nos(t, "igual", ref)
    _trilha_de_nos(t, "verbete", [ref[0], ("recuperacao", "campo_ausente,contrato-produto,resposta_truncada"), ("diagnostico", "campo_ausente")])
    _trilha_de_nos(t, "contrato", [("poda", "json/lista; id:tipo_diferente"), ("recuperacao", "tipo_divergente,contrato-produto,resposta_truncada"), ref[2]])
    _trilha_de_nos(t, "curta", ref[:2])
    assert at.nos_da_trilha(t.eventos, "ref") == [{"decisao": d, "escolha": e} for d, e in ref]
    d = at.diff_entre_trilhas(t.eventos, "ref", "igual")
    assert d["primeiro_no_divergente"] is None and d["nos_referencia"] == d["nos_nova"]
    assert at.aponta_o_previsto(d["primeiro_no_divergente"], "verbete_trocado") is None, "sem divergência não há o que apontar"
    d = at.diff_entre_trilhas(t.eventos, "ref", "verbete")
    assert d["primeiro_no_divergente"] == {"posicao": 2, "decisao": "recuperacao", "esperado": {"decisao": "recuperacao", "escolha": ref[1][1]},
                                           "obtido": {"decisao": "recuperacao", "escolha": "campo_ausente,contrato-produto,resposta_truncada"}}, d
    assert at.aponta_o_previsto(d["primeiro_no_divergente"], "verbete_trocado") is True
    assert at.aponta_o_previsto(d["primeiro_no_divergente"], "contrato_alterado") is False, "o verbete trocado divergiu na recuperação, não na poda"
    d = at.diff_entre_trilhas(t.eventos, "ref", "contrato")
    assert d["primeiro_no_divergente"]["posicao"] == 1 and d["primeiro_no_divergente"]["decisao"] == "poda", "a poda vem antes: é ela que diverge primeiro, mesmo com a busca mudando"
    assert at.aponta_o_previsto(d["primeiro_no_divergente"], "contrato_alterado") is True
    d = at.diff_entre_trilhas(t.eventos, "ref", "curta")
    assert d["primeiro_no_divergente"]["posicao"] == 3 and d["primeiro_no_divergente"]["decisao"] == "diagnostico" and d["primeiro_no_divergente"]["obtido"] is None
    # o seletor quebrado, na tela: a dourada tem diagnostico, cura e reexecucao; a mutação troca o nome do alvo e a cura muda de candidato
    _trilha_de_nos(t, "dourada", [("diagnostico", "localizador_quebrado"), ("cura", "papel_e_nome"), ("reexecucao", "validada")])
    _trilha_de_nos(t, "mutada", [("diagnostico", "localizador_quebrado"), ("cura", "papel_e_nome_parecido"), ("reexecucao", "validada")])
    d = at.diff_entre_trilhas(t.eventos, "dourada", "mutada")
    assert d["primeiro_no_divergente"]["decisao"] == "cura" and d["primeiro_no_divergente"]["posicao"] == 2
    assert at.aponta_o_previsto(d["primeiro_no_divergente"], "seletor_quebrado") is True
    # a mesma estratégia com outro seletor aplicado (o caso do roteiro cuja dourada já cura por nome parecido): o diff do bloco do
    # seletor compara o nó `cura` pela estratégia E pelo seletor aplicado; o diff comum, só pela escolha, não vê a diferença
    for tid, sel in (("dourada2", 'role=button[name=" EXCLUIR ITEM"] >> nth=0'), ("mutada2", 'role=button[name=" EXCLUIR LINHA"] >> nth=0')):
        t.decisao(tid, _no(decisao="diagnostico", escolha="localizador_quebrado", alternativas=[{"opcao": "localizador_quebrado", "escore": 1.0}]), ts=TS)
        t.decisao(tid, _no(decisao="cura", escolha="papel_e_nome_parecido",
                           alternativas=[{"opcao": "papel_e_nome_parecido", "escore": 4, "seletor": sel, "aplicado": True}, {"opcao": "data_id", "escore": 3, "seletor": 'button[data-id="1"]', "aplicado": False}]), ts=TS)
    assert at.diff_entre_trilhas(t.eventos, "dourada2", "mutada2")["primeiro_no_divergente"] is None
    d = at.diff_entre_trilhas(t.eventos, "dourada2", "mutada2", cura_pelo_seletor=True)
    assert d["primeiro_no_divergente"]["decisao"] == "cura" and d["primeiro_no_divergente"]["posicao"] == 2, d
    assert d["primeiro_no_divergente"]["obtido"]["escolha"] == 'papel_e_nome_parecido (role=button[name=" EXCLUIR LINHA"] >> nth=0)'
    assert at.diff_entre_trilhas(t.eventos, "dourada", "mutada", cura_pelo_seletor=True)["primeiro_no_divergente"]["decisao"] == "cura"
    # a quebra composta de cada roteiro: a quebra do catálogo do ensaio mais UMA mutação que troca o nome acessível do alvo por um nome
    # parecido (acima do limiar da cura, senão nenhum candidato passa a verificação de nome e a cura fica impossível por desenho),
    # por um seletor que sobrevive à primeira mutação (o id que o catálogo renomeia não serve): o candidato que curou a dourada deixa
    # de resolver e a cura tem de ir a outro candidato ou a outro seletor
    import cura_seletor as cs
    for c in cen.CENARIOS_DE_LOCALIZADOR:
        q = cen.quebra(c["cenario"], c["modo"])
        q2 = at.quebra_do_seletor(c["cenario"])
        assert q2["modo"] == f"{c['modo']}+{at.SUFIXO_DA_MUTACAO}" and q2["mutacoes"][:-1] == q["mutacoes"] and len(q2["mutacoes"]) == len(q["mutacoes"]) + 1
        for chave in ("cenario", "localizador", "seletor_original", "passo_alvo", "alvo", "pagina"):
            assert q2[chave] == q[chave], chave
        extra = q2["mutacoes"][-1]
        assert extra["op"] in ("trocar_atributo", "trocar_texto") and extra.get("seletor") and extra.get("para"), extra
        renomeia = [x for x in q["mutacoes"] if x["op"] == "renomear_id"]
        if renomeia:
            assert extra["seletor"] != renomeia[0]["seletor"], "a mutação extra não pode mirar o id que o catálogo renomeia antes dela"
        sim = cs.similaridade(q["alvo"]["nome"], q2["nome_depois"])
        assert cs.LIMIAR_NOME <= sim < 1.0 and cs.normalizar(q2["nome_depois"]) != cs.normalizar(q["alvo"]["nome"]), (c["cenario"], q2["nome_depois"], sim)
        assert extra["para"] in q2["nome_depois"] and extra["para"] in cen.script_de_quebra(q2["mutacoes"], q2["modo"])
        assert "nome" in q2["descricao"] and q2["nome_depois"] in q2["descricao"]
    assert at.quebra_do_seletor("front-busca")["mutacoes"][-1]["seletor"] == "input[name=buscar]", "o id #buscar vira #buscar_v2 antes da mutação extra"
    assert at.quebra_do_seletor("front-admin-produtos")["mutacoes"][-1]["de"] == "ITEM", "em produtos o catálogo já pôs ITEM no texto; a extra troca só a palavra nova"
    try:
        at.quebra_do_seletor("api-catalogo")
    except KeyError:
        pass
    else:
        raise AssertionError("roteiro sem cenário de localizador aceito")


# ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) os ajudantes e os dois testes abaixo: o relatório v2 de um caso lido em
# texto, com o evento de poda do P7, mostra o caso como foi ao prompt; e leituras_da_trilha tira da trilha o controle da sonda (a FONTE
# da repetição da base) e a comparação da mutação do verbete com a intervenção de troca; relatorios_da_amostra grava e confere os
# relatórios da sessão de revisão.
# ! Motivo: na corrida 22 nenhum dos 11 relatórios da amostra mostrava o sintoma, a requisição nem o contrato, porque o relatório só
# imprimia o texto do caso quando a trilha não tinha poda, e o P7 passou a emitir poda nos casos de texto; sem o caso, o revisor não
# tem como julgar o diagnóstico. A mutação do verbete e a intervenção de troca montam o mesmo prompt, e isso precisa sair de script.
def _base_de_teste_do_p7(amostra=("lex-1",), intervencoes="por_gatilho", sem_doc_muda=False) -> tuple:
    """Uma base e a mutação do verbete de lex-1 na trilha v2, com o Ollama de mentira; devolve a trilha, o id da base, o caso e o citado."""
    import avaliacao_trilha as at
    import diagnostico_ao_vivo as dv
    verbetes, indice = _curada()
    caso = _caso_de_texto_do_p7()
    ctx, _ = dv.montar_prompt(verbetes, indice, caso, 3)
    citado = ctx["verbetes_ids"][0]
    resposta = (f"O campo preco veio como preco_v2.\nCAUSA_RAIZ: campo_renomeado\nCAMPO: preco\nIMPACTO: o cartão mostra o preço vazio.\nFONTE: [{citado}]",
                .95, [(" tipo_divergente", .02)])
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(), ts=TS)
    saida = "fase4_trilha_teste/qwen2.5_7b/lex-1"
    lim = {"baixo_ate": .5, "alto_a_partir_de": .85, "medida": "p_rotulo", "parcela_baixa": .3}
    chamadas: list = []

    def responder(prompt: str, corpo: dict):
        if sem_doc_muda and prompt.startswith("\n\n====="):     # sem documentação: o contexto é vazio e o prompt começa pelo separador
            return ("Sem documentação.\nCAUSA_RAIZ: tipo_divergente\nCAMPO: preco\nIMPACTO: x.\nFONTE: nenhum", .55, [(" nulo", .2)])
        return resposta

    with _ollama_de_mentira_v2(responder, chamadas):
        b = at.rodar_base(t, f"{saida}@base", caso, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=_comum_de_teste(), limiares=lim, top=20, teto=600, amostra=amostra,
                          ts=TS, intervencoes=intervencoes)
        at.rodar_mutacao(t, f"{saida}@verbete_trocado", "verbete_trocado", caso, verbetes, indice, b, k=3, modelo="qwen2.5:7b", comum=_comum_de_teste(), limiares=lim,
                         top=20, teto=600, ts=TS)
    return t, f"{saida}@base", caso, citado


def teste_relatorio_v2_de_caso_de_texto_com_poda_mostra_o_caso_como_foi_ao_prompt():
    t, tid, caso, _ = _base_de_teste_do_p7()
    md = grr.relatorio_do_caso_v2(t.eventos, tid)
    secao = md.split("## 2. Evidência")[1].split("## 3. ")[0]
    assert "SINTOMA OBSERVADO: " + caso["entrada"]["sintoma"] in secao, secao[:400]
    assert "REQUISIÇÃO: GET /api/produtos" in secao and "CONTRATO ESPERADO PELA INTERFACE: id: inteiro" in secao
    assert secao.index("SINTOMA OBSERVADO") < secao.index("Poda de `corpo_http`"), "o caso vem antes da poda: é o que o revisor lê primeiro"
    assert "preco_v2" in secao and "Avaliação contra o gabarito" not in md and "campo_renomeado" not in secao.split("Poda de")[0], "o texto do caso não traz o gabarito"
    # um caso em texto sem poda (corrida 18) continua com a frase de antes, sem repetir o caso
    t2 = trilha.Trilha(versao=trilha.V2)
    t2.corrida(_cabecalho(), ts=TS)
    t2.evento("entrada", "x@fixture", {"caso": "x", "origem": "fixture", "texto": t2.blob("SINTOMA OBSERVADO: y", "caso")}, "ao_vivo", ts=TS)
    t2.decisao("x@fixture", _no(), ts=TS)
    md2 = grr.relatorio_do_caso_v2(t2.eventos, "x@fixture")
    assert "Não houve interceptação nem poda" in md2 and md2.count("SINTOMA OBSERVADO: y") == 1, md2
    # ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) a coluna Efeito da tabela das intervenções fala de cada tipo pelo que ele é.
    # ! Motivo: ela dizia "o verbete pesou na decisão" na inferência sem documentação, que não tem verbete, e "sem efeito medido do contexto" na
    # repetição da base; o molde promete não afirmar mais do que foi medido (especificação, seção 7), e a célula do verbete saía vazia.

    def efeito(texto: str, tipo: str) -> str:
        return next(l for l in texto.split("## 4. FONTE")[1].splitlines() if l.startswith(f"| {tipo} |"))

    assert "`" not in efeito(md, "sem_documentacao").split("|")[2] and "não se aplica" in efeito(md, "sem_documentacao").split("|")[2], efeito(md, "sem_documentacao")
    assert "sem documentação a resposta fica a mesma" in efeito(md, "sem_documentacao") and "o mesmo prompt manteve o rótulo" in efeito(md, "repeticao_da_base")
    assert "sem efeito medido do contexto" in efeito(md, "remocao") and "sem efeito medido do contexto" in efeito(md, "troca")
    t4, tid4, _, _ = _base_de_teste_do_p7(sem_doc_muda=True)
    linha = efeito(grr.relatorio_do_caso_v2(t4.eventos, tid4), "sem_documentacao")
    assert "a documentação pesou na decisão" in linha and "o verbete pesou" not in linha, linha


# ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) teste novo: um corpo em texto corrido fica registrado no nó da poda, mas não entra como
# sinal em código na evidência do diagnóstico; corpo truncado e corpo vazio continuam entrando.
# ! Motivo: nos 5 casos de avaliação com contrato e corpo escrito em texto corrido ("POST devolveu ..."), a justificativa gravada disse que o agente
# respondeu "porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente": o sinal vem de como o fixture foi escrito, não da
# falha, e a frase atribui a resposta a ele.
def teste_avaliacao_trilha_corpo_em_texto_corrido_nao_vira_sinal_na_justificativa():
    import avaliacao_trilha as at
    verbetes, indice = _curada()
    base = _caso_de_texto_do_p7()
    resposta = ("Algo saiu errado.\nCAUSA_RAIZ: dado_desatualizado\nCAMPO: nenhum\nIMPACTO: x.\nFONTE: nenhum", .95, [(" nulo", .02)])
    lim = {"baixo_ate": .5, "alto_a_partir_de": .85, "medida": "p_rotulo", "parcela_baixa": .3}

    def rodar(corpo: str) -> tuple:
        caso = {**base, "entrada": {**base["entrada"], "corpo": corpo}}
        t = trilha.Trilha(versao=trilha.V2)
        t.corrida(_cabecalho(), ts=TS)
        with _ollama_de_mentira_v2(lambda p, c: resposta, []):
            b = at.rodar_base(t, "x/q/lex-1@base", caso, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=_comum_de_teste(), limiares=lim, top=20, teto=600, ts=TS, intervencoes="desligadas")
        return t, b

    t, b = rodar('POST devolveu {"id": 8}. GET seguinte devolveu [{"id": 7}]')
    assert at.nos_da_trilha(t.eventos, "x/q/lex-1@base")[0]["escolha"] == "nao_json", "o nó da poda registra o que o código leu"
    assert "nao_json" not in b["no"]["justificativa"] and not any(e["papel"] == "sinal_em_codigo" for e in b["no"]["evidencia"]), b["no"]["justificativa"]
    for corpo, frase in (('[{"id": 1, "nome": "Pic', "corpo truncado"), ("", "corpo vazio")):
        _, b2 = rodar(corpo)
        assert frase in b2["no"]["justificativa"] and any(e["papel"] == "sinal_em_codigo" for e in b2["no"]["evidencia"]), (corpo, b2["no"]["justificativa"])


def teste_avaliacao_trilha_leituras_da_trilha_e_relatorios_da_sessao_de_revisao():
    import avaliacao_trilha as at
    import avaliar_fase4 as av
    t, tid, caso, citado = _base_de_teste_do_p7()
    blobs = trilha.blobs_de(t.eventos)
    da = at.leituras_da_trilha(t.eventos, blobs)
    assert set(da) == {"lex-1"}, da
    d = da["lex-1"]
    assert d["fonte_na_repeticao"] == [citado] and d["repeticao_mesma_resposta"] is True and d["repeticao_mesma_fonte"] is True, d
    assert d["troca_mesmo_prompt"] is True and d["troca_mesma_resposta"] is True and d["troca_mesma_fonte"] is True, "a troca e a mutação do verbete montam o mesmo prompt"
    # sem a mutação na trilha, a comparação fica sem valor em vez de virar falso
    so_base = [e for e in t.eventos if not str(e.get("trilha") or "").endswith("@verbete_trocado")]
    d2 = at.leituras_da_trilha(so_base, blobs)["lex-1"]
    assert d2["troca_mesmo_prompt"] is None and d2["troca_mesma_resposta"] is None and d2["fonte_na_repeticao"] == [citado]
    # fora da amostra as intervenções não rodam: não há repetição para servir de controle
    t3, _, _, _ = _base_de_teste_do_p7(amostra=())
    assert at.leituras_da_trilha(t3.eventos, trilha.blobs_de(t3.eventos))["lex-1"]["fonte_na_repeticao"] is None
    # os relatórios da sessão: gravados ao lado da planilha, com o caso, e conferidos por --check
    pasta = _temp()
    dado = {"condicoes": {"modelo": "qwen2.5:7b"}, "amostra_revisao": [{"posicao": 1, "caso": "lex-1", "classe": 1, "relatorio": f"{av.PASTA_RELATORIOS_REVISAO}/lex-1@base.md"}]}
    assert av.relatorios_da_amostra(dado, t.eventos, "fase4_trilha_teste", pasta) == 0
    arq = pasta / av.PASTA_RELATORIOS_REVISAO / "lex-1@base.md"
    texto = arq.read_text(encoding="utf-8")
    assert "SINTOMA OBSERVADO" in texto and "--ids lex-1" in texto and "fase4_trilha_teste" in texto
    assert av.relatorios_da_amostra(dado, t.eventos, "fase4_trilha_teste", pasta, check=True) == 0
    arq.write_text(texto + "mudou", encoding="utf-8")
    assert av.relatorios_da_amostra(dado, t.eventos, "fase4_trilha_teste", pasta, check=True) == 1, "o --check acusa o relatório que difere"


def _caso_de_texto_do_p7() -> dict:
    """Um caso de texto como os 36 de avaliação, sem gabarito (fixture_sem_gabarito), com contrato e corpo JSON."""
    import executar_fase4 as ex
    return ex.fixture_sem_gabarito({"id": "lex-1", "classe": 1, "nivel": 1, "gabarito": {"causa_raiz": "campo_renomeado"},
                                    "entrada": {"requisicao": "GET /api/produtos", "status": 200, "contrato": "id: inteiro | nome: texto | preco: numero",
                                                "corpo": '[{"id": 1, "nome": "Picanha ao Alho", "preco_v2": 89.9}]',
                                                "sintoma": "O campo preco não veio na resposta e o cartão mostra o preço vazio."}})


def teste_avaliacao_trilha_base_emite_poda_recuperacao_e_diagnostico_e_registra_o_limite_inferior():
    import avaliacao_trilha as at
    import avaliar_fase4 as av
    import diagnostico_ao_vivo as dv
    verbetes, indice = _curada()
    caso = _caso_de_texto_do_p7()
    ctx, _ = dv.montar_prompt(verbetes, indice, caso, 3)
    citado = ctx["verbetes_ids"][0]
    base = (f"O campo preco veio como preco_v2.\nCAUSA_RAIZ: campo_renomeado\nCAMPO: preco\nIMPACTO: o cartão mostra o preço vazio.\nFONTE: [{citado}]",
            .45, [(" tipo_divergente", .25), (" campo_ausente", .1)])

    def responder(prompt: str, corpo: dict):
        if prompt.startswith("\n\n====="):          # sem documentação: o contexto é vazio e o prompt começa pelo separador
            return ("Sem documentação.\nCAUSA_RAIZ: tipo_divergente\nCAMPO: preco\nIMPACTO: x.\nFONTE: nenhum", .55, [(" nulo", .2)])
        if dv.MARCADOR_NEUTRO.splitlines()[0] in prompt:
            # o rótulo original (campo_renomeado) não está entre as alternativas devolvidas: fica só um limite inferior (risco 6)
            return ("Faltou o verbete.\nCAUSA_RAIZ: campo_ausente\nCAMPO: preco\nIMPACTO: x.\nFONTE: nenhum", .5, [(" nulo", .2)])
        return base

    lim = {"baixo_ate": .5, "alto_a_partir_de": .85, "medida": "p_rotulo", "parcela_baixa": .3}
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(), ts=TS)
    tid = "fase4_trilha/qwen2.5_7b/lex-1@base"
    chamadas: list = []
    with _ollama_de_mentira_v2(responder, chamadas):
        b = at.rodar_base(t, tid, caso, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=_comum_de_teste(), limiares=lim, top=20, teto=600,
                          amostra=("lex-1",), ts=TS)
    assert len(chamadas) == 5, "a base e as quatro intervenções (o caso está na amostra fixa)"
    assert tuple(b["registro"]) == dv.CHAVES_OFICIAIS and b["registro"]["caso"] == "lex-1" and b["registro"]["gabarito"] is None
    nos = at.nos_da_trilha(t.eventos, tid)
    assert [n["decisao"] for n in nos] == ["poda", "recuperacao", "diagnostico"], nos
    assert nos[0]["escolha"] == "json/lista; preco:renomeado" and nos[1]["escolha"] == ",".join(ctx["verbetes_ids"]) and nos[2]["escolha"] == "campo_renomeado"
    ev = [e for e in t.eventos if e["trilha"] == tid]
    s_cand = next(e["seq"] for e in ev if e["tipo"] == "candidatos")
    no_rec = next(e["dados"] for e in ev if e["tipo"] == "decisao" and e["dados"]["decisao"] == "recuperacao")
    assert all(x["seq"] == s_cand and x["papel"] == "verbete_entregue" for x in no_rec["evidencia"]) and [x["id"] for x in no_rec["evidencia"]] == ctx["verbetes_ids"]
    assert no_rec["prov"]["wasGeneratedBy"] == s_cand and no_rec["divergencia"]["ha"] is False and no_rec["k"] == 3 and no_rec["mutacao"] is None
    tipos = [e["tipo"] for e in ev]
    i_rec = next(i for i, e in enumerate(ev) if e["tipo"] == "decisao" and e["dados"]["decisao"] == "recuperacao")
    assert tipos.index("candidatos") < i_rec < tipos.index("prompt"), "o nó da recuperação fica entre os candidatos e o prompt"
    assert tipos.index("decisao") < tipos.index("candidatos"), "o nó da poda vem antes da busca"
    no_poda = next(e["dados"] for e in ev if e["tipo"] == "decisao" and e["dados"]["decisao"] == "poda")
    s_poda = next(e["seq"] for e in ev if e["tipo"] == "poda")
    assert no_poda["evidencia"] == [{"seq": s_poda, "papel": "sinal_em_codigo"}] and no_poda["diferencas"] == [{"campo": "preco", "tipo": "renomeado"}]
    assert {"seq": s_poda, "papel": "sinal_em_codigo"} in b["no"]["evidencia"], "o nó de diagnóstico aponta o sinal em código da poda"
    assert "preco_v2" in b["no"]["justificativa"], "o molde cita o sinal em código que a poda achou"
    entrada = next(e["dados"] for e in ev if e["tipo"] == "entrada")
    assert entrada["origem"] == "fixture" and entrada["etapa"] == "base" and entrada["caso"] == "lex-1"
    l = b["linha"]
    assert l["caso"] == "lex-1" and l["rotulo"] == "campo_renomeado" and l["selo"] == "baixo" and l["divergencia"] is True and l["falha"] == b["no"]["falha"]
    por_tipo = {i["tipo"]: i for i in l["intervencoes"]}
    assert list(por_tipo) == list(dv.INTERVENCOES)
    assert por_tipo["remocao"]["mudou_rotulo"] is True and por_tipo["remocao"]["limite_inferior"] is True and math.isclose(por_tipo["remocao"]["p_depois"], .2)
    assert por_tipo["sem_documentacao"]["limite_inferior"] is True and por_tipo["troca"]["limite_inferior"] is False and por_tipo["repeticao_da_base"]["mudou_rotulo"] is False
    assert l["repeticao_manteve"] is True and l["nos_base"] == [[n["decisao"], n["escolha"]] for n in nos] and l["segundos_base"] == b["registro"]["segundos"]
    assert b["fontes"] == [citado] and b["ctx"]["verbetes_ids"] == ctx["verbetes_ids"] and b["rotulo"] == "campo_renomeado"
    # a leitura conta o limite inferior por tipo de intervenção e a repetição que manteve o rótulo
    casos = [{"id": "lex-1", "classe": 1, "nivel": 1, "gabarito": {"causa_raiz": "campo_renomeado", "campo_afetado": "preco"}}]
    dado = av.resumir_trilha({"condicoes": {}, "avaliacao": [l], "seletor": [], "casos": casos}, gerado_em="2026-11-04T23:00:00", corrida="fase4_trilha")
    inter = {x["tipo"]: x for x in dado["intervencoes"]}
    assert inter["remocao"]["n"] == 1 and inter["remocao"]["mudou_rotulo"] == 1 and inter["remocao"]["limite_inferior"] == 1
    assert inter["troca"]["limite_inferior"] == 0 and inter["sem_documentacao"]["limite_inferior"] == 1
    assert dado["casos"][0]["acerto"] is True and dado["repeticao"]["manteve"] == 1
    md = av.render_trilha(dado)
    assert "<!-- tabela:tb_f4_trilha_intervencoes -->" in md and "Limite inferior" in md


def teste_avaliacao_trilha_sonda_e_mutacoes_ao_vivo_com_ollama_de_mentira():
    import avaliacao_trilha as at
    import diagnostico_ao_vivo as dv
    verbetes, indice = _curada()
    caso = _caso_de_texto_do_p7()
    ctx, _ = dv.montar_prompt(verbetes, indice, caso, 3)
    citado, nao_citado = ctx["verbetes_ids"][0], ctx["verbetes_ids"][1]
    errado = dv.verbete_errado(indice, caso, "campo_renomeado", excluir=ctx["verbetes_ids"])
    plantado = at.texto_plantado("campo_renomeado")
    assert "campo_renomeado" in plantado and "\n" not in plantado and len(plantado) < 160
    m = at.mutar_contrato(caso["entrada"]["contrato"], caso["entrada"]["corpo"])
    resposta = "O campo preco veio como preco_v2.\nCAUSA_RAIZ: {causa}\nCAMPO: preco\nIMPACTO: o cartão mostra o preço vazio.\nFONTE: [{fonte}]"

    def responder(prompt: str, corpo: dict):
        if plantado in prompt:   # a FONTE passa a citar o verbete plantado; o rótulo não muda
            return (resposta.format(causa="campo_renomeado", fonte=nao_citado), .6, [(" tipo_divergente", .2)])
        if f"CONTRATO ESPERADO PELA INTERFACE: {m['contrato']}" in prompt:
            return (resposta.format(causa="tipo_divergente", fonte=citado), .7, [(" campo_renomeado", .2)])
        if f"[{errado['id']}]" in prompt and f"[{citado}]" not in prompt:
            return (resposta.format(causa="campo_ausente", fonte=errado["id"]), .5, [(" campo_renomeado", .3)])
        return (resposta.format(causa="campo_renomeado", fonte=citado), .95, [(" tipo_divergente", .02)])

    lim = {"baixo_ate": .5, "alto_a_partir_de": .85, "medida": "p_rotulo", "parcela_baixa": .3}
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(), ts=TS)
    raiz = "fase4_trilha/qwen2.5_7b/lex-1"
    chamadas: list = []
    comum = _comum_de_teste()
    with _ollama_de_mentira_v2(responder, chamadas):
        b = at.rodar_base(t, f"{raiz}@base", caso, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=comum, limiares=lim, top=20, teto=600, amostra=(), ts=TS)
        assert len(chamadas) == 1 and b["linha"]["intervencoes"] == [], "fora da amostra e com probabilidade alta, só a inferência de base"
        s = at.rodar_sonda(t, f"{raiz}@sonda", caso, verbetes, indice, b, k=3, modelo="qwen2.5:7b", comum=comum, limiares=lim, top=20, teto=600, ts=TS)
        assert len(chamadas) == 2
        prompt_s = chamadas[-1]["prompt"]
        assert prompt_s.count(plantado) == 1, "o trecho plantado entra uma vez"
        bloco = prompt_s.split(f"[{nao_citado}]", 1)[1].split("\n\n[", 1)[0]
        assert plantado in bloco, "o trecho entra no verbete entregue que a FONTE da base não citou"
        assert not any(plantado in json.dumps(v["secoes"], ensure_ascii=False) for v in verbetes), "a biblioteca em memória não muda"
        r = s["linha"]
        assert r["aplicavel"] is True and r["verbete"] == nao_citado and r["cita_plantado"] is True and r["mudou_rotulo"] is False and r["pos_racionalizacao"] is True
        assert r["fonte_antes"] == [citado] and r["fonte_depois"] == [nao_citado] and r["rotulo_depois"] == "campo_renomeado" and r["trecho"] == plantado
        assert s["registro"]["caso"] == "lex-1@sonda" and tuple(s["registro"]) == dv.CHAVES_OFICIAIS
        # verbete trocado: a busca entrega o verbete errado no lugar do citado; o primeiro nó divergente é a recuperação
        v = at.rodar_mutacao(t, f"{raiz}@verbete_trocado", "verbete_trocado", caso, verbetes, indice, b, k=3, modelo="qwen2.5:7b", comum=comum, limiares=lim,
                             top=20, teto=600, ts=TS)
        assert len(chamadas) == 3
        prompt_v = chamadas[-1]["prompt"]
        assert f"[{errado['id']}]" in prompt_v and f"[{citado}]" not in prompt_v and prompt_v.count(f"[{errado['id']}]") == 1
        lv = v["linha"]
        assert lv["aplicavel"] is True and lv["detalhe"] == {"de": citado, "para": errado["id"], "alvo": "citado"}, lv
        assert lv["primeiro_no_divergente"]["decisao"] == "recuperacao" and lv["aponta_o_previsto"] is True and lv["no_previsto"] == "recuperacao"
        assert lv["rotulo_depois"] == "campo_ausente" and lv["mudou_rotulo"] is True
        nos_v = at.nos_da_trilha(t.eventos, f"{raiz}@verbete_trocado")
        assert nos_v[0] == at.nos_da_trilha(t.eventos, f"{raiz}@base")[0] and nos_v[1]["escolha"].startswith(errado["id"] + ",")
        assert v["registro"]["caso"] == "lex-1@verbete_trocado" and v["registro"]["verbetes_ids"][0] == errado["id"]
        # contrato alterado: o tipo do primeiro campo que concorda muda; a poda diverge primeiro
        c = at.rodar_mutacao(t, f"{raiz}@contrato_alterado", "contrato_alterado", caso, verbetes, indice, b, k=3, modelo="qwen2.5:7b", comum=comum, limiares=lim,
                             top=20, teto=600, ts=TS)
        assert len(chamadas) == 4 and f"CONTRATO ESPERADO PELA INTERFACE: {m['contrato']}" in chamadas[-1]["prompt"]
        lc = c["linha"]
        assert lc["aplicavel"] is True and lc["detalhe"]["campo"] == "id" and lc["primeiro_no_divergente"]["decisao"] == "poda" and lc["aponta_o_previsto"] is True
        assert at.nos_da_trilha(t.eventos, f"{raiz}@contrato_alterado")[0]["escolha"] == "json/lista; id:tipo_diferente, preco:renomeado"
        assert lc["rotulo_depois"] == "tipo_divergente" and lc["mudou_rotulo"] is True
        assert caso["entrada"]["contrato"] == "id: inteiro | nome: texto | preco: numero", "o caso original não muda"
        # um caso sem contrato (classe 6): a mutação do contrato não tem alvo, nada vai ao Ollama e a linha diz por quê
        sem = dict(caso, id="efe-1", entrada={**caso["entrada"], "contrato": "n/a", "corpo": "(nenhuma requisicao falhou)"})
        b6 = at.rodar_base(t, f"{raiz.replace('lex-1', 'efe-1')}@base", sem, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=comum, limiares=lim, top=20, teto=600, amostra=(), ts=TS)
        n = len(chamadas)
        c6 = at.rodar_mutacao(t, f"{raiz.replace('lex-1', 'efe-1')}@contrato_alterado", "contrato_alterado", sem, verbetes, indice, b6, k=3, modelo="qwen2.5:7b",
                              comum=comum, limiares=lim, top=20, teto=600, ts=TS)
        assert len(chamadas) == n and c6["linha"]["aplicavel"] is False and "contrato" in c6["linha"]["motivo"] and c6["registro"] is None
        assert at.nos_da_trilha(t.eventos, f"{raiz.replace('lex-1', 'efe-1')}@base")[0]["escolha"] == "sem_contrato"
        # sem verbete entregue não citado (a FONTE cita os três), a sonda não roda e diz por quê
        b2 = dict(b, fontes=list(ctx["verbetes_ids"]))
        s2 = at.rodar_sonda(t, f"{raiz}@sonda2", caso, verbetes, indice, b2, k=3, modelo="qwen2.5:7b", comum=comum, limiares=lim, top=20, teto=600, ts=TS)
        assert len(chamadas) == n and s2["linha"]["aplicavel"] is False and "citou" in s2["linha"]["motivo"] and s2["registro"] is None
    # a linha do caso junta tudo (o executor grava uma por caso em avaliacao.jsonl)
    linha = at.linha_do_caso(b, s, {"verbete_trocado": v, "contrato_alterado": c}, segundos_total=321.0)
    assert linha["caso"] == "lex-1" and linha["sonda"]["pos_racionalizacao"] is True and set(linha["mutacoes"]) == {"verbete_trocado", "contrato_alterado"}
    assert linha["mutacoes"]["verbete_trocado"]["aponta_o_previsto"] is True and linha["nos_base"][2] == ["diagnostico", "campo_renomeado"] and linha["segundos_total"] == 321.0
    json.dumps(linha, ensure_ascii=False)


def teste_executar_fase4_modo_avaliacao_trilha_partes_puras():
    import avaliacao_trilha as at
    import executar_fase4 as ex
    assert "avaliacao_trilha" in ex.MODOS and callable(ex.rodar_avaliacao_trilha)
    args = ex.montar_parser().parse_args(["--modo", "avaliacao_trilha", "--saida", "fase4_trilha"])
    assert args.modo == "avaliacao_trilha" and args.sem_seletor is False and args.casos == 0
    assert ex.montar_parser().parse_args(["--modo", "avaliacao_trilha", "--saida", "x", "--sem-seletor", "--casos", "2"]).sem_seletor is True
    # as contas da noite: 36 x (1 base + 4 intervenções + 1 sonda + 2 mutações) + 2 por roteiro de localizador (dourada e mutada)
    assert at.INFERENCIAS_POR_CASO == 8 and at.inferencias_previstas(36, roteiros=4) == 296 and at.inferencias_previstas(1, roteiros=0) == 8
    assert at.SEMENTE_DA_AMOSTRA == 20261104 and at.AMOSTRA_POR_LADO == 6
    # a amostra de revisão: até 6 certos e 6 errados sorteados com a semente fixa e embaralhados; o acerto não vai na amostra
    linhas = [{"caso": f"c{i}", "acerto": i % 3 != 0} for i in range(30)]
    am = at.amostra_de_revisao(linhas)
    assert len(am) == 12 and sum(1 for c in am if c["acerto"]) == 6 and len({c["caso"] for c in am}) == 12
    assert am == at.amostra_de_revisao(linhas), "a mesma semente dá a mesma amostra"
    assert [c["acerto"] for c in am] not in ([True] * 6 + [False] * 6, [False] * 6 + [True] * 6), "embaralhada: os certos não vêm todos juntos"
    poucos = at.amostra_de_revisao([{"caso": "a", "acerto": False}] + linhas[:3])
    assert len(poucos) == 4 and sum(1 for c in poucos if not c["acerto"]) == 2
    # o modo da mutação do seletor dos quatro roteiros do ensaio e o nome das etapas
    assert at.ETAPAS == ("base", "sonda", "verbete_trocado", "contrato_alterado") and at.ROTEIROS_DO_SELETOR == ("front-busca", "front-admin-login", "front-admin-produtos", "front-cliente-reserva")


# ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) teste novo: a linha do rodar_fase4.ps1 que monta a chamada de
# avaliar_fase4.py é tirada do arquivo pela árvore sintática do PowerShell e executada para cada modo do ValidateSet; o avaliador
# tem de aceitar a opção que sai dela.
# ! Motivo: na corrida 22 (05/11/2026, 02:40) o executor terminou inteiro, mas o .ps1 chamou `avaliar_fase4.py --avaliacao_trilha`,
# que não existe (a leitura é `--trilha`), e saiu com código 2 depois de 3h40 de máquina; o lançador, ao ver o código, não rodou a
# leitura dele. O teste antigo só procurava trechos no texto do .ps1 e a fumaça chamava o avaliador direto, sem passar pela linha.
def teste_rodar_fase4_ps1_cada_modo_chama_uma_leitura_que_o_avaliador_aceita():
    import base64
    import re
    import subprocess

    import avaliar_fase4 as av
    if not shutil.which("powershell"):
        print("  (pulado com aviso: powershell não está no PATH; a linha da leitura não foi exercitada)")
        return
    arq = EXP / "rodar_fase4.ps1"
    modos = re.findall(r'"([a-z_]+)"', re.search(r'ValidateSet\(([^)]*)\)\]\[string\]\$Modo', arq.read_text(encoding="utf-8-sig")).group(1))
    assert "avaliacao_trilha" in modos and "experimento_prompt" in modos and "ineditos" in modos and len(modos) == 9, modos
    caminho = "'" + str(arq).replace("'", "''") + "'"
    lista = ",".join(f"'{m}'" for m in modos)
    roteiro = "\n".join([
        "$ErrorActionPreference = 'Stop'",
        "$tokens = $null; $erros = $null",
        f"$ast = [System.Management.Automation.Language.Parser]::ParseFile({caminho}, [ref]$tokens, [ref]$erros)",
        "foreach ($f in $ast.FindAll({ param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] }, $true)) { if ($f.Name -eq 'FlagDaLeitura') { Invoke-Expression $f.Extent.Text } }",
        "$atrib = $ast.Find({ param($n) ($n -is [System.Management.Automation.Language.AssignmentStatementAst]) -and ($n.Left.Extent.Text -eq '$Avaliacao') -and ($n.Operator -eq 'Equals') }, $true)",
        "if (-not $atrib) { throw 'a linha $Avaliacao = ... nao esta no rodar_fase4.ps1' }",
        "$Saida = 'x'",
        f"foreach ($Modo in @({lista})) {{ Invoke-Expression $atrib.Extent.Text; Write-Output ($Modo + '=' + $Avaliacao[1]) }}",
    ])
    r = subprocess.run(["powershell", "-NoProfile", "-EncodedCommand", base64.b64encode(roteiro.encode("utf-16-le")).decode("ascii")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
    assert r.returncode == 0, (r.stdout, r.stderr)
    flags = dict(l.strip().split("=", 1) for l in r.stdout.splitlines() if "=" in l)
    assert set(flags) == set(modos), (flags, r.stderr)
    for modo, flag in flags.items():
        try:
            args = av.montar_parser().parse_args([flag, "--saida", "x"])
        except SystemExit as e:
            raise AssertionError(f"no modo {modo} o .ps1 chama avaliar_fase4.py {flag}, e o avaliador recusa essa opção (código {e.code})") from None
        assert getattr(args, flag[2:]) is True, (modo, flag)
    assert flags["avaliacao_trilha"] == "--trilha", flags


def teste_avaliar_fase4_trilha_tpr_tnr_mutacoes_sonda_e_amostra_com_check():
    import avaliacao_trilha as at
    import avaliar
    import avaliar_fase4 as av
    import biblioteca_fase4 as bf
    import pre_fase4 as pf

    def interv(tipo: str, mudou: bool, limite: bool = False) -> dict:
        return {"tipo": tipo, "verbete": "v", "rotulo_antes": "x", "rotulo_depois": "y" if mudou else "x", "mudou_rotulo": mudou, "p_antes": .8,
                "p_depois": .3 if mudou else .8, "limite_inferior": limite, "segundos": 50.0}

    def mut(aplicavel: bool, decisao, previsto: str, mudou: bool = False) -> dict:
        return {"aplicavel": aplicavel, "detalhe": {}, "no_previsto": previsto, "motivo": None if aplicavel else "sem alvo",
                "primeiro_no_divergente": {"posicao": 1, "decisao": decisao, "esperado": {}, "obtido": {}} if decisao else None,
                "aponta_o_previsto": (decisao == previsto) if (aplicavel and decisao) else None, "rotulo_depois": "y" if mudou else "x", "mudou_rotulo": mudou, "segundos": 60.0}

    def linha(caso: str, classe: int, rotulo: str, selo: str, div: bool, falha, interv_: list, sonda_ok, vt: dict, ca: dict) -> dict:
        return {"caso": caso, "classe": classe, "nivel": 1, "rotulo": rotulo, "p_rotulo": .9 if selo == "alto" else .4, "selo": selo, "falha": falha,
                "divergencia": div, "gatilhos": {"probabilidade": selo == "baixo", "fonte_divergente": False, "amostra": True, "algum": True},
                "intervencoes": interv_, "repeticao_manteve": not any(i["tipo"] == "repeticao_da_base" and i["mudou_rotulo"] for i in interv_),
                "sonda": {"aplicavel": sonda_ok is not None, "verbete": "v2" if sonda_ok is not None else None, "trecho": "x", "cita_plantado": sonda_ok,
                          "mudou_rotulo": False if sonda_ok is not None else None, "rotulo_depois": rotulo, "fonte_antes": ["v"], "fonte_depois": ["v2"] if sonda_ok else ["v"],
                          "pos_racionalizacao": sonda_ok, "p_depois": .8, "motivo": None if sonda_ok is not None else "a FONTE citou todos os verbetes entregues", "segundos": 55.0},
                "mutacoes": {"verbete_trocado": vt, "contrato_alterado": ca},
                "nos_base": [["poda", "json/lista; sem diferença"], ["recuperacao", "a,b,c"], ["diagnostico", rotulo]],
                "segundos_base": 60.0, "segundos_total": 400.0, "tokens_entrada": 1100}

    quatro = [interv("remocao", True, True), interv("troca", False), interv("sem_documentacao", True, True), interv("repeticao_da_base", False)]
    quietas = [interv("remocao", False), interv("troca", False), interv("sem_documentacao", True), interv("repeticao_da_base", False)]
    casos = [{"id": c, "classe": cl, "nivel": 1, "gabarito": {"causa_raiz": "x", "campo_afetado": None}} for c, cl in
             [("a", 1), ("b", 1), ("c", 2), ("d", 2), ("e", 3), ("f", 3)]]
    # a, b e c acertam (rótulo x); d, e e f erram (rótulo y). A divergência do nó está em b (acerto) e em d e e (erros): TPR 2/3, TNR 2/3
    linhas = [linha("a", 1, "x", "alto", False, None, quietas, True, mut(True, "recuperacao", "recuperacao"), mut(True, "poda", "poda")),
              linha("b", 1, "x", "medio", True, None, quatro, False, mut(True, "recuperacao", "recuperacao", True), mut(False, None, "poda")),
              linha("c", 2, "x", "alto", False, None, quietas, None, mut(True, None, "recuperacao"), mut(True, "poda", "poda")),
              linha("d", 2, "y", "baixo", True, "campo_errado", quatro, True, mut(True, "diagnostico", "recuperacao", True), mut(True, "recuperacao", "poda")),
              linha("e", 3, "y", "baixo", True, None, quatro, True, mut(True, "recuperacao", "recuperacao"), mut(True, "poda", "poda", True)),
              linha("f", 3, "y", "medio", False, None, quietas, False, mut(True, "recuperacao", "recuperacao"), mut(True, "poda", "poda"))]
    seletor = [{"roteiro": r, "cenario_id": f"localizador-{r}", "modo_dourado": md, "modo_mutado": f"{md}+{at.SUFIXO_DA_MUTACAO}",
                "dourada": {"quebrou": True, "curado": True, "estrategia": "papel_e_nome", "seletor_curado": "role=x", "rotulo": "localizador_quebrado", "p_rotulo": .9, "mttr_s": 60.0},
                "mutada": {"quebrou": True, "curado": cur, "estrategia": est, "seletor_curado": "role=y" if cur else None, "rotulo": "localizador_quebrado", "p_rotulo": .9,
                           "mttr_s": 70.0 if cur else None},
                "primeiro_no_divergente": {"posicao": 2, "decisao": dec, "esperado": {}, "obtido": {}} if dec else None, "no_previsto": "cura",
                "aponta_o_previsto": (dec == "cura") if dec else None, "segundos": 150.0}
               for r, md, cur, est, dec in [("front-busca", "id_renomeado", True, "caminho_do_ancestral_com_id", "cura"),
                                            ("front-admin-login", "classe_trocada", True, "caminho_do_ancestral_com_id", "cura"),
                                            ("front-admin-produtos", "texto_alterado", True, "data_id", "cura"),
                                            ("front-cliente-reserva", "estrutura_alterada", False, None, "diagnostico")]]
    bruto = {"condicoes": {"modelo": "qwen2.5:7b", "versao_ollama": "0.40.14", "k": 3, "casos": 6, "parcial": False, "inferencias_previstas": 56,
                           "biblioteca": {"hash": "95af35290860"}}, "avaliacao": linhas, "seletor": seletor, "casos": casos}
    # ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) o que só a trilha guarda: o controle da sonda (a FONTE da repetição
    # da base) e a mutação do verbete contra a intervenção de troca, além das inferências feitas e da pasta dos relatórios da sessão.
    # ! Motivo: a sonda sem controle superestima a pós-racionalização (2 de 36 citaram o mesmo verbete sem plantar nada), e a mutação do
    # verbete monta o mesmo prompt da troca: os dois fatos entram na leitura por script, não digitados.
    def visto(fonte, rep_resp=True, rep_fonte=True, tr_prompt=True, tr_resp=False, tr_fonte=True) -> dict:
        return {"fonte_na_repeticao": fonte, "repeticao_mesma_resposta": rep_resp, "repeticao_mesma_fonte": rep_fonte, "troca_mesmo_prompt": tr_prompt,
                "troca_mesma_resposta": tr_resp, "troca_mesma_fonte": tr_fonte}

    bruto["da_trilha"] = {"a": visto(["v2"]), "b": visto(["v"], rep_resp=False), "c": visto(["v"], rep_resp=False, rep_fonte=False), "d": visto(["v"], tr_resp=True),
                          "e": visto(["v"], tr_prompt=False), "f": visto(None, None, None, None, None, None)}
    dado = av.resumir_trilha(bruto, gerado_em="2026-11-05T06:00:00", corrida="fase4_trilha")
    r = dado["resumo"]
    # base e 4 intervenções em 6 casos, a sonda em 5, verbete trocado em 6, contrato alterado em 5, e 2 por roteiro em 4 roteiros
    assert r["inferencias"] == 6 * 5 + 5 + 6 + 5 + 8, r["inferencias"]
    por_gatilho = next(s for s in dado["sinais"] if s["sinal"] == "por_gatilho")
    assert (por_gatilho["vp"], por_gatilho["fn"], por_gatilho["fp"], por_gatilho["vn"]) == (2, 1, 0, 3), por_gatilho
    assert math.isclose(por_gatilho["produto"], 2 / 3) and por_gatilho["ic_tpr"] == avaliar.wilson(2, 3) and por_gatilho["ic_tnr"] == avaliar.wilson(3, 3)
    assert (dado["sonda"]["controle_n"], dado["sonda"]["controle_cita"]) == (4, 1), dado["sonda"]
    assert dado["sonda"]["controle_pct"] == 25.0
    pares = {x["par"]: x for x in dado["mesmo_prompt"]}
    assert (pares["repeticao_da_base"]["n"], pares["repeticao_da_base"]["mesma_resposta"], pares["repeticao_da_base"]["mesma_fonte"], pares["repeticao_da_base"]["mesmo_rotulo"]) == (5, 3, 4, 5), pares
    assert (pares["verbete_trocado_e_troca"]["n"], pares["verbete_trocado_e_troca"]["mesmo_prompt"], pares["verbete_trocado_e_troca"]["mesma_resposta"]) == (5, 4, 1), pares
    assert all(x["relatorio"].startswith(av.PASTA_RELATORIOS_REVISAO + "/") and x["relatorio"].endswith("@base.md") for x in dado["amostra_revisao"])
    assert (r["casos"], r["acertos"], r["erros"]) == (6, 3, 3) and r["acerto_pct"] == 50.0
    principal = next(s for s in dado["sinais"] if s["sinal"] == "divergencia")
    assert math.isclose(principal["tpr"], 2 / 3) and math.isclose(principal["tnr"], 2 / 3) and math.isclose(principal["produto"], 4 / 9) and principal["acaso"] == 0.25
    assert (r["tpr"], r["tnr"], r["produto"]) == (principal["tpr"], principal["tnr"], principal["produto"]), "o resumo leva o sinal principal, a divergência do nó"
    selo = next(s for s in dado["sinais"] if s["sinal"] == "selo_baixo")
    assert math.isclose(selo["tpr"], 2 / 3) and selo["tnr"] == 1.0, "o selo baixo marca d e e, e nenhum acerto"
    falha = next(s for s in dado["sinais"] if s["sinal"] == "falha")
    assert math.isclose(falha["tpr"], 1 / 3) and falha["tnr"] == 1.0
    assert [s["sinal"] for s in dado["sinais"]] == [n for n, _ in at.SINAIS] and all(s["descricao"] for s in dado["sinais"])
    inter = {x["tipo"]: x for x in dado["intervencoes"]}
    assert (inter["remocao"]["n"], inter["remocao"]["mudou_rotulo"], inter["remocao"]["limite_inferior"]) == (6, 3, 3), inter["remocao"]
    assert (inter["sem_documentacao"]["n"], inter["sem_documentacao"]["mudou_rotulo"], inter["sem_documentacao"]["limite_inferior"]) == (6, 6, 3)
    assert inter["troca"]["mudou_rotulo"] == 0 and dado["repeticao"] == {"n": 6, "manteve": 6, "mudou": 0}
    assert dado["fonte"] == {"casos": 6, "verificada_pela_remocao": 3, "sem_efeito_medido": 3}
    so = dado["sonda"]
    assert (so["casos"], so["com_alvo"], so["sem_alvo"], so["pos_racionalizacao"], so["mudou_rotulo"]) == (6, 5, 1, 3, 0) and so["taxa_pct"] == 60.0, so
    mu = {x["tipo"]: x for x in dado["mutacoes"]}
    assert (mu["verbete_trocado"]["aplicaveis"], mu["verbete_trocado"]["previsto"], mu["verbete_trocado"]["outro_no"], mu["verbete_trocado"]["sem_divergencia"],
            mu["verbete_trocado"]["rotulo_mudou"]) == (6, 4, 1, 1, 2), mu["verbete_trocado"]
    assert (mu["contrato_alterado"]["aplicaveis"], mu["contrato_alterado"]["sem_alvo"], mu["contrato_alterado"]["previsto"], mu["contrato_alterado"]["outro_no"],
            mu["contrato_alterado"]["rotulo_mudou"]) == (5, 1, 4, 1, 1)
    assert (mu["seletor_quebrado"]["aplicaveis"], mu["seletor_quebrado"]["previsto"], mu["seletor_quebrado"]["outro_no"], mu["seletor_quebrado"]["sem_divergencia"]) == (4, 3, 1, 0)
    assert mu["verbete_trocado"]["previsto_pct"] == round(100 * 4 / 6, 1) and mu["verbete_trocado"]["no_previsto"] == "recuperacao" and mu["seletor_quebrado"]["no_previsto"] == "cura"
    assert [m_["tipo"] for m_ in dado["mutacoes"]] == list(at.MUTACOES)
    assert dado["seletor"]["curadas_mutada"] == 3 and len(dado["seletor"]["roteiros"]) == 4 and dado["seletor"]["roteiros"][3]["primeiro_no"] == "diagnostico"
    assert [x["caso"] for x in dado["mutacoes_casos"] if x["tipo"] == "verbete_trocado" and x["primeiro_no"] == "diagnostico"] == ["d"]
    am = dado["amostra_revisao"]
    assert len(am) == 6 and {x["caso"] for x in am} == {"a", "b", "c", "d", "e", "f"} and all(set(x) == {"posicao", "caso", "classe", "relatorio"} for x in am)
    assert am == av.resumir_trilha(bruto, gerado_em="2026-11-05T07:00:00", corrida="fase4_trilha")["amostra_revisao"], "a semente fixa dá a mesma amostra"
    assert dado["casos"][3]["acerto"] is False and dado["casos"][3]["gabarito"] == "x" and dado["casos"][3]["sinais"]["divergencia"] is True
    md = av.render_trilha(dado)
    for bloco in ("tb_f4_trilha_resumo", "tb_f4_trilha_sinais", "tb_f4_trilha_intervencoes", "tb_f4_trilha_sonda", "tb_f4_trilha_mesmo_prompt", "tb_f4_trilha_mutacoes",
                  "tb_f4_trilha_seletor", "tb_f4_trilha_amostra", "tb_f4_trilha_casos"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    assert "—" not in md and "→" not in md and "0,25" in md
    # ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) TPR, TNR, o produto e o acaso em três casas nas tabelas, com o intervalo.
    # ! Motivo: o padrão de uma casa pôs o acaso como 0,2 e o produto da corrida 22 como 0,3; o teste antigo passava porque o 0,25 aparece
    # no texto do cabeçalho.
    linha_div = next(l for l in md.splitlines() if l.startswith("| `divergencia` |"))
    assert "| 0,667 | 0,667 | 0,444 | 0,250 |" in linha_div and f"{avaliar.wilson(2, 3)[0]:.1f}".replace(".", ",") + " a " in linha_div, linha_div
    assert "| 0,667 | 0,667 | 0,444 | 0,250 |" in next(l for l in md.split("tb_f4_trilha_resumo")[1].splitlines() if l.startswith("| 6 |")), "o resumo também em três casas"
    pasta = _temp()
    assert pf.fechar(av.NOME_TRILHA, dado, md, av.PREFIXO_TRILHA, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert pf.fechar(av.NOME_TRILHA, dado, md, av.PREFIXO_TRILHA, check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert av.nome_dos_arquivos(None, "trilha") == "trilha" and av.montar_parser().parse_args(["--trilha", "--saida", "fase4_trilha"]).trilha is True
    # a planilha da sessão de revisão: uma linha por relatório da amostra, as células do revisor em branco, nunca regravada depois de preenchida
    planilha = av.planilha_de_revisao_da_trilha(dado)
    linhas_p = [l for l in planilha.splitlines() if l.startswith("| ") and not l.startswith("| # |")]
    assert len(linhas_p) == 6 and all(l.rstrip().endswith(f"| {bf.CELULA_EM_BRANCO} |  |") for l in linhas_p), linhas_p
    assert "Tempo até a decisão" in planilha and "Erro localizado" in planilha and "Utilidade" in planilha and "gabarito" not in planilha.lower()
    arq = pasta / "revisao_trilha.md"
    assert bf.gravar_planilha_de_revisao(arq, planilha) == "gravada"
    arq.write_text(planilha.replace(f"| {bf.CELULA_EM_BRANCO} |  |", "| aceitou |  |", 1), encoding="utf-8")
    assert bf.gravar_planilha_de_revisao(arq, planilha) == "mantida" and (pasta / "revisao_trilha.nova.md").exists()
    vazio = av.resumir_trilha({"condicoes": {}, "avaliacao": [], "seletor": [], "casos": casos}, gerado_em="2026-11-05T06:00:00", corrida="x")
    assert vazio["resumo"]["casos"] == 0 and vazio["resumo"]["produto"] is None and av.render_trilha(vazio) and vazio["amostra_revisao"] == []


# ----------------------------------------------------------------------------- P0: a amostra real (fica por último)

def teste_fixture_da_arvore_tem_papel_e_nome():
    """A amostra real de produtos_api.php, com as cobaias no ar (P0, item 3 do plano aprovado). Fica por último porque
    o runner para na primeira falha: enquanto PHP e MariaDB não existirem na máquina, este é o único teste vermelho."""
    dados = _conferir_fixture_arvore(FIX / "arvore_produtos_api.json")
    assert dados["origem"].startswith("http://localhost:8080/"), dados["origem"]
    assert not dados.get("provisoria"), "a amostra real não pode ser marcada como provisória"


# ! Alteração de IA - Revisar: (05/11/2026, sessão de revisão) o relatório v2 dá nome à linha sem campo da tabela do contrato e não deixa crase do modelo quebrar o trecho de código.
# ! Motivo: o revisor lia uma linha de primeira coluna vazia nos casos em texto corrido, e a frase de impacto de um caso com crases saía com o código partido no meio.
def teste_relatorio_v2_nomeia_a_linha_sem_campo_e_nao_quebra_o_codigo_com_crase_do_modelo():
    t, tid, _, _ = _base_de_teste_do_p7()
    poda_ = next(e for e in t.eventos if e["trilha"] == tid and e["tipo"] == "poda")
    poda_["dados"]["diff"] = [{"campo": None, "esperado": "JSON completo e válido", "recebido": "corpo nao_json", "tipo": "nao_json"}] + list(poda_["dados"].get("diff") or [])
    impacto = next(e for e in t.eventos if e["trilha"] == tid and e["tipo"] == "declaracao" and e["dados"].get("campo") == "impacto")
    impacto["dados"]["valor"] = "o campo `preco` some da tela"
    md = grr.relatorio_do_caso_v2(t.eventos, tid)
    assert "| (corpo inteiro) | JSON completo e válido | corpo nao_json |" in md, md
    linha = next(l for l in md.splitlines() if l.startswith("**IMPACTO (declarado):**"))
    assert linha == "**IMPACTO (declarado):** `o campo 'preco' some da tela`", linha
    arvore = next(l for l in md.splitlines() if "impacto: `" in l)
    assert "impacto: `o campo 'preco' some da tela`" in arvore, arvore


# ! Alteração de IA - Revisar: (05/11/2026, sessão de revisão) testes da leitura `--revisao` de avaliar_fase4.py, escritos antes da sessão: adesão apropriada, localização do
# erro, tempo até a decisão e utilidade contra o acerto de cada caso em trilha.json; com a planilha incompleta a leitura não sai nem mostra resultado.
# ! Motivo: a conta fica fixada antes de existir resposta do revisor, para não ser ajustada depois de ver os dados (especificação da trilha, seção 12 c).
def _trilha_e_planilha_da_revisao(linhas=None) -> tuple[dict, str]:
    casos = [{"caso": "a-1", "classe": 1, "gabarito": "causa_x", "rotulo": "causa_x", "acerto": True, "selo": "alto", "p_rotulo": .9},
             {"caso": "a-2", "classe": 1, "gabarito": "causa_x", "rotulo": "causa_x", "acerto": True, "selo": "médio", "p_rotulo": .7},
             {"caso": "a-3", "classe": 2, "gabarito": "causa_y", "rotulo": "causa_y", "acerto": True, "selo": "baixo", "p_rotulo": .4},
             {"caso": "b-1", "classe": 2, "gabarito": "causa_y", "rotulo": "causa_z", "acerto": False, "selo": "baixo", "p_rotulo": .3},
             {"caso": "b-2", "classe": 3, "gabarito": "causa_w", "rotulo": "causa_z", "acerto": False, "selo": "alto", "p_rotulo": .95},
             {"caso": "fora-da-amostra", "classe": 3, "gabarito": "causa_w", "rotulo": "causa_w", "acerto": True, "selo": "alto", "p_rotulo": .99}]
    linhas = linhas or [("a-1", "100", "n.a.", "aceitar", "5", "certo", ""), ("a-2", "200", "não", "aceitar", "4", "errado", "fiquei em dúvida"), ("a-3", "300", "sim", "recusar", "2", "errado", ""),
                        ("b-1", "400", "sim", "recusar", "5", "errado", "na seção 3"), ("b-2", "500", "n.a.", "aceitar", "3", "certo", "")]
    planilha = ["<!-- comentário -->", "# Sessão", "", "| # | Caso | Classe | Relatório | Tempo até a decisão (s) | Erro localizado (sim, não, n.a.) | Decisão (aceitar, recusar) | Utilidade (1 a 5) | Avaliação (certo, errado) | Comentário |",
                "|---|---|---|---|---|---|---|---|---|---|"]
    planilha += [f"| {i + 1} | `{c}` | 1 | `relatorios_revisao_trilha/{c}@base.md` | {t} | {e} | {d} | {u} | {a} | {m} |" for i, (c, t, e, d, u, a, m) in enumerate(linhas)]
    return {"metadados": {"corrida": "fase4_trilha"}, "casos": casos}, "\n".join(planilha) + "\n"


def teste_avaliar_fase4_revisao_mede_adesao_localizacao_tempo_e_utilidade_contra_o_acerto_da_trilha():
    import avaliar
    import avaliar_fase4 as av
    trilha_, planilha = _trilha_e_planilha_da_revisao()
    lida = av.ler_planilha_de_revisao(planilha)
    assert lida["em_branco"] == [] and [x["caso"] for x in lida["linhas"]] == ["a-1", "a-2", "a-3", "b-1", "b-2"], lida
    assert (lida["linhas"][1]["segundos"], lida["linhas"][1]["utilidade"], lida["linhas"][1]["comentario"]) == (200, 4, "fiquei em dúvida"), lida["linhas"][1]
    dado = av.resumir_revisao(trilha_, lida["linhas"], gerado_em="2026-11-05T10:00:00", corrida="fase4_trilha")
    ade = {x["grupo"]: x for x in dado["adesao"]}
    assert (ade["diagnóstico certo"]["n"], ade["diagnóstico certo"]["aceitou"], ade["diagnóstico certo"]["recusou"], ade["diagnóstico certo"]["apropriadas"]) == (3, 2, 1, 2), ade
    assert (ade["diagnóstico errado"]["n"], ade["diagnóstico errado"]["aceitou"], ade["diagnóstico errado"]["recusou"], ade["diagnóstico errado"]["apropriadas"]) == (2, 1, 1, 1), ade
    assert (ade["todos"]["n"], ade["todos"]["apropriadas"], ade["todos"]["pct"]) == (5, 3, 60.0), ade
    assert tuple(ade["todos"]["ic"]) == avaliar.wilson(3, 5), ade
    loc = {x["grupo"]: x for x in dado["localizacao"]}
    assert (loc["diagnóstico errado"]["sim"], loc["diagnóstico errado"]["nao"], loc["diagnóstico errado"]["na"], loc["diagnóstico errado"]["pct_sim"]) == (1, 0, 1, 50.0), loc
    assert (loc["diagnóstico certo"]["sim"], loc["diagnóstico certo"]["nao"], loc["diagnóstico certo"]["na"]) == (1, 1, 1), "num diagnóstico certo, dizer sim é apontar erro onde não há"
    tempo = {x["grupo"]: x for x in dado["tempo"]}
    assert (tempo["todos"]["n"], tempo["todos"]["mediana"], tempo["todos"]["minimo"], tempo["todos"]["maximo"]) == (5, 300, 100, 500), tempo
    assert (tempo["diagnóstico certo"]["mediana"], tempo["diagnóstico errado"]["mediana"], tempo["aceitos"]["mediana"], tempo["recusados"]["mediana"]) == (200, 450, 200, 350), tempo
    uti = {x["grupo"]: x for x in dado["utilidade"]}
    assert uti["todos"]["mediana"] == 4 and uti["todos"]["contagem"] == {"1": 0, "2": 1, "3": 1, "4": 1, "5": 2}, uti
    assert uti["diagnóstico certo"]["mediana"] == 4 and uti["diagnóstico errado"]["mediana"] == 4, uti
    av_ = dado["avaliacao"]
    assert (av_["acertos"], av_["n"], av_["certo_disse_certo"], av_["certo_disse_errado"], av_["errado_disse_certo"], av_["errado_disse_errado"]) == (2, 5, 1, 2, 1, 1), av_
    assert av_["decisao_e_avaliacao_discordam"] == ["a-2"], av_
    assert [x["caso"] for x in dado["casos"]] == ["a-1", "a-2", "a-3", "b-1", "b-2"] and "fora-da-amostra" not in json.dumps(dado), "só os casos da planilha entram"
    assert [x["apropriada"] for x in dado["casos"]] == [True, True, False, True, False], dado["casos"]
    assert dado["resumo"]["adesao_apropriada"] == 3 and dado["resumo"]["relatorios"] == 5 and dado["resumo"]["erros_na_amostra"] == 2, dado["resumo"]
    md = av.render_revisao(dado)
    for bloco in ("resumo", "adesao", "localizacao", "tempo", "utilidade", "avaliacao", "casos"):
        assert f"<!-- tabela:tb_f4_revisao_{bloco} -->" in md, bloco
    assert "| todos | 5 | 3 | 2 | 3 | 60,0 |" in md, md
    assert "| 4 | `b-1` | `causa_y` | `causa_z` | errado |" in md, md
    assert "Um revisor só" in md, "a limitação fica escrita junto dos números"
    assert "—" not in md and "→" not in md


def teste_avaliar_fase4_revisao_nao_sai_com_a_planilha_incompleta_e_confere_com_check():
    import contextlib
    import io
    import avaliar_fase4 as av
    pasta = _temp()
    doc = pasta / "nao_existe.md"
    trilha_, planilha = _trilha_e_planilha_da_revisao()
    (pasta / "trilha.json").write_text(json.dumps(trilha_, ensure_ascii=False), encoding="utf-8")
    incompleta = planilha.replace("| 500 | n.a. | aceitar | 3 | certo |  |", "| (em branco) | (em branco) | (em branco) | (em branco) | (em branco) |  |")
    assert incompleta != planilha
    (pasta / "revisao_trilha.md").write_text(incompleta, encoding="utf-8", newline="\n")
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        codigo = av.fechar_revisao(pasta, doc=doc)
    assert codigo == 2, codigo
    assert not (pasta / f"{av.NOME_REVISAO}.json").exists() and not (pasta / f"{av.NOME_REVISAO}.md").exists()
    assert "1 de 5" in saida.getvalue() and "causa_" not in saida.getvalue() and "errado" not in saida.getvalue(), saida.getvalue()
    (pasta / "revisao_trilha.md").write_text(planilha, encoding="utf-8", newline="\n")
    assert av.fechar_revisao(pasta, doc=doc) == 0
    assert (pasta / f"{av.NOME_REVISAO}.json").exists() and (pasta / f"{av.NOME_REVISAO}.md").exists()
    assert av.fechar_revisao(pasta, check=True, doc=doc) == 0
    (pasta / "revisao_trilha.md").write_text(planilha.replace("| 400 | sim |", "| 401 | sim |"), encoding="utf-8", newline="\n")
    assert av.fechar_revisao(pasta, check=True, doc=doc) == 1, "o --check percebe uma planilha mudada depois da leitura"
    ruins = [("| 400 | sim | recusar |", "| 400 | talvez | recusar |"), ("| 400 | sim | recusar |", "| 400 | sim | adiar |"), ("| recusar | 5 | errado |", "| recusar | 6 | errado |"),
             ("| recusar | 5 | errado |", "| recusar | 5 | dúvida |"), ("| 400 | sim |", "| quatro | sim |"), ("`b-1`", "`caso-sem-trilha`")]
    for velho, novo in ruins:
        assert velho in planilha, velho
        (pasta / "revisao_trilha.md").write_text(planilha.replace(velho, novo), encoding="utf-8", newline="\n")
        try:
            av.fechar_revisao(pasta, doc=doc)
        except ValueError:
            continue
        raise AssertionError(f"aceitou {novo}")
    assert "--revisao" in av.montar_parser().format_help() and av.nome_dos_arquivos(None, "revisao") == av.NOME_REVISAO


# ! Alteração de IA - Revisar: (05/11/2026, decisão 86) a leitura `--revisao` separa a resposta do revisor do parecer do Claude aprovado, não mede tempo onde ele não existe, compara o parecer contra o gabarito e registra a dúvida de leitura do relatório 1.
# ! Motivo: o Eric respondeu um relatório antes de ler a pré-análise e aprovou o parecer nos outros; somar tudo como revisor humano apresentaria o julgamento do Claude como a medida da especificação (seção 12 c). A conta foi escrita antes de abrir o gabarito.
_PARECER_DE_TESTE = """| # | Relatório | Causa do agente | Selo | Erro localizado | Decisão | Utilidade | Avaliação | Causa que eu daria | Confiança |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `relatorio-1` | `causa_x` | alto | n.a. | aceitar | 3 | certo | a mesma | alta |
| 2 | `relatorio-2` | `causa_x` | alto | n.a. | aceitar | 3 | certo | a mesma | alta |
| 3 | `relatorio-3` | `causa_y` | alto | n.a. | recusar | 3 | errado | `causa_k` | média |
| 4 | `relatorio-4` | `causa_z` | baixo | sim | recusar | 4 | errado | `causa_y` | alta |
| 5 | `relatorio-5` | `causa_z` | alto | não | aceitar | 2 | certo | a mesma | média |
"""


def teste_avaliar_fase4_revisao_com_parecer_aprovado_separa_quem_decidiu_e_nao_chama_de_medida_humana():
    import avaliar
    import avaliar_fase4 as av
    ap = "Parecer do Claude aprovado"
    trilha_, planilha = _trilha_e_planilha_da_revisao([("a-1", "100", "sim", "aceitar", "4", "certo", ""), ("a-2", av.TEMPO_NAO_MEDIDO, "n.a.", "aceitar", "3", "certo", ap), ("a-3", av.TEMPO_NAO_MEDIDO, "n.a.", "recusar", "3", "errado", ap),
                                                       ("b-1", av.TEMPO_NAO_MEDIDO, "sim", "recusar", "4", "errado", ap), ("b-2", av.TEMPO_NAO_MEDIDO, "não", "aceitar", "2", "certo", ap)])
    lida = av.ler_planilha_de_revisao(planilha)
    assert [x["origem"] for x in lida["linhas"]] == ["revisor"] + ["parecer_aprovado"] * 4, lida
    assert [x["segundos"] for x in lida["linhas"]] == [100, None, None, None, None], lida
    parecer = av.ler_pre_analise(_PARECER_DE_TESTE)
    assert parecer[3]["causa"] == "causa_k" and parecer[1]["causa"] is None and parecer[3]["confianca"] == "média", parecer
    dado = av.resumir_revisao(trilha_, lida["linhas"], gerado_em="2026-11-05T10:00:00", corrida="fase4_trilha", parecer=parecer)
    org = {x["origem"]: x for x in dado["por_origem"]}
    assert (org["revisor"]["n"], org["revisor"]["apropriadas"]) == (1, 1), org
    assert (org["parecer_aprovado"]["n"], org["parecer_aprovado"]["apropriadas"], org["parecer_aprovado"]["pct"]) == (4, 2, 50.0), org
    assert tuple(org["parecer_aprovado"]["ic"]) == avaliar.wilson(2, 4), org
    tempo = {x["grupo"]: x for x in dado["tempo"]}
    assert (tempo["todos"]["n"], tempo["todos"]["mediana"]) == (1, 100) and (tempo["diagnóstico errado"]["n"], tempo["diagnóstico errado"]["mediana"]) == (0, None), tempo
    pa = dado["parecer"]
    assert (pa["n"], pa["apropriadas"], pa["causa_certa"], pa["avaliacao_bate"], pa["pct"]) == (5, 3, 3, 3, 60.0), pa
    assert pa["errou_a_decisao"] == ["a-3", "b-2"] and pa["errou_a_causa"] == ["a-3", "b-2"], pa
    assert dado["casos"][3]["parecer"]["causa"] == "causa_y" and dado["casos"][3]["parecer"]["causa_certa"] is True and dado["casos"][4]["parecer"]["causa_certa"] is False, dado["casos"]
    assert dado["duvidas_de_leitura"] == ["a-1"], dado["duvidas_de_leitura"]
    assert (dado["resumo"]["respostas_do_revisor"], dado["resumo"]["pareceres_aprovados"]) == (1, 4), dado["resumo"]
    md = av.render_revisao(dado)
    for bloco in ("origem", "parecer"):
        assert f"<!-- tabela:tb_f4_revisao_{bloco} -->" in md, bloco
    assert "Só 1 dos 5 relatórios tem resposta própria do revisor" in md and "não cumpre" in md and "pode ter lido" in md and "`a-1`" in md, md
    assert "Somando a resposta do revisor e o parecer aprovado" in md and "O revisor avaliou" not in md, "a frase final não atribui ao revisor o que é do parecer"
    assert "em aberto e será feita depois da Pós-Fase 4 (decisão 95)" in md, md
    assert "—" not in md and "→" not in md
    # sem parecer aprovado nem dúvida, a leitura não diz que a medida falhou
    trilha2, planilha2 = _trilha_e_planilha_da_revisao()
    md2 = av.render_revisao(av.resumir_revisao(trilha2, av.ler_planilha_de_revisao(planilha2)["linhas"], gerado_em="2026-11-05T10:00:00"))
    assert "não cumpre" not in md2 and "tb_f4_revisao_parecer" not in md2 and "O revisor avaliou" in md2, md2
    # a valor fora do que a planilha aceita continua sendo erro
    trilha3, planilha3 = _trilha_e_planilha_da_revisao([("a-1", "nao medido", "n.a.", "aceitar", "3", "certo", "")])
    try:
        av.ler_planilha_de_revisao(planilha3)
    except ValueError:
        pass
    else:
        raise AssertionError("aceitou um tempo fora do combinado")
    # fechar_revisao lê a pré-análise que está ao lado da planilha e o --check bate
    pasta = _temp()
    doc = pasta / "nao_existe.md"
    (pasta / "trilha.json").write_text(json.dumps(trilha_, ensure_ascii=False), encoding="utf-8")
    (pasta / "revisao_trilha.md").write_text(planilha, encoding="utf-8", newline="\n")
    (pasta / "pre_analise_revisao_trilha.md").write_text(_PARECER_DE_TESTE, encoding="utf-8", newline="\n")
    assert av.fechar_revisao(pasta, doc=doc) == 0 and av.fechar_revisao(pasta, check=True, doc=doc) == 0
    gravado = json.loads((pasta / f"{av.NOME_REVISAO}.json").read_text(encoding="utf-8"))
    assert gravado["parecer"]["apropriadas"] == 3, gravado["parecer"]


# ! Alteração de IA - Revisar: (05/11/2026, ficha 41) testes da poda que olha todos os itens da lista e segue a regra da biblioteca para booleano, da frase do sintoma que diz o item e da linha da tabela do contrato que diz o item.
# ! Motivo: `poda.diff_contrato` só olhava o primeiro item, então um defeito em outro item saía como "sem diferença"; e chamava `destaque: 2` de tipo diferente, enquanto a biblioteca separa `destaque 1` (tipo_divergente) de `destaque 2` (valor_fora_do_dominio).
def teste_poda_olha_todos_os_itens_da_lista_e_diz_em_qual_esta_a_diferenca():
    import avaliacao_trilha as at
    import caso_ao_vivo as cv
    import poda
    contrato = "id: inteiro | nome: texto | resumo: texto|nulo"

    def diff(corpo) -> dict:
        return poda.diff_contrato(contrato, json.dumps(corpo, ensure_ascii=False))

    bom = {"id": 1, "nome": "a", "resumo": "x"}
    # defeito só no segundo item: antes saía "sem diferença"
    d = diff([bom, {"id": 2, "nome": "b"}])
    assert [(x["campo"], x["tipo"], x.get("item")) for x in d["diferencas"]] == [("resumo", "ausente", 2)], d
    assert d["trecho"] == '{"(item 2)": {"resumo": "(ausente)"}}', d["trecho"]
    assert at.resumo_do_diff(d) == "json/lista; resumo:ausente", at.resumo_do_diff(d)
    assert cv._frases_do_corpo(d) == ["O campo resumo não veio no item 2 da resposta."], cv._frases_do_corpo(d)
    linhas = at.linhas_diff_do_contrato(d)
    assert linhas[0]["item"] == 2 and linhas[0]["campo"] == "resumo", linhas
    # sem nenhuma diferença, tudo igual a antes: o trecho é o primeiro item e não há marca de item
    d0 = diff([bom, {"id": 2, "nome": "b", "resumo": None}])
    assert d0["diferencas"] == [] and d0["trecho"] == json.dumps(bom, ensure_ascii=False), d0
    # diferença no primeiro item: sem a marca, com o trecho de antes; a mesma diferença em outro item não repete
    d1 = diff([{"id": "1", "nome": "a", "resumo": "x"}, {"id": "2", "nome": "b", "resumo": "y"}])
    assert [(x["campo"], x["tipo"], x.get("item")) for x in d1["diferencas"]] == [("id", "tipo_diferente", None)], d1
    assert "item" not in d1["diferencas"][0] and d1["trecho"] == '{"id": "1"}', d1
    # diferenças em itens diferentes: cada uma com o seu item, na ordem em que aparecem
    d2 = diff([{"id": "1", "nome": "a", "resumo": "x"}, bom, {"id": 3, "nome": None, "resumo": "z"}])
    assert [(x["campo"], x["tipo"], x.get("item")) for x in d2["diferencas"]] == [("id", "tipo_diferente", None), ("nome", "nulo_inesperado", 3)], d2
    assert d2["trecho"] == '{"id": "1", "(item 3)": {"nome": null}}', d2["trecho"]
    assert cv._frases_do_corpo(d2)[1] == "O campo nome veio nulo no item 3.", cv._frases_do_corpo(d2)
    # renomeado e inesperado também valem nos outros itens; item que não é objeto é ignorado
    d3 = diff([bom, {"id": 2, "nome_novo": "b", "resumo": "y"}, "texto solto", {"id": 4, "nome": "d", "resumo": "w", "extra": 1}])
    assert [(x["campo"], x["tipo"], x.get("item")) for x in d3["diferencas"]] == [("nome", "renomeado", 2), ("extra", "inesperado", 4)], d3
    assert '"(item 2)": {"nome_novo": "b"}' in d3["trecho"] and '"(item 4)": {"extra": 1}' in d3["trecho"], d3["trecho"]
    assert cv._frases_do_corpo(d3) == ["O campo nome veio como nome_novo no item 2.", "A resposta trouxe o campo extra no item 4, que o contrato não prevê."], cv._frases_do_corpo(d3)
    # um objeto só continua como antes
    d4 = poda.diff_contrato(contrato, json.dumps({"id": 1, "nome": "a"}))
    assert [(x["campo"], x["tipo"], x.get("item")) for x in d4["diferencas"]] == [("resumo", "ausente", None)], d4
    # a linha da tabela do contrato no relatório diz o item
    t, tid, _, _ = _base_de_teste_do_p7()
    poda_ = next(e for e in t.eventos if e["trilha"] == tid and e["tipo"] == "poda")
    poda_["dados"]["diff"] = [{"campo": "resumo", "esperado": "texto|nulo", "recebido": None, "tipo": "ausente", "item": 2}]
    assert "| resumo (item 2) | texto\\|nulo |  |" in grr.relatorio_do_caso_v2(t.eventos, tid), "a tabela diz em qual item está a diferença"


def teste_poda_booleano_com_numero_segue_a_regra_da_biblioteca():
    import poda
    contrato = "id: inteiro | destaque: booleano"

    def tipo(valor):
        d = poda.diff_contrato(contrato, json.dumps([{"id": 1, "destaque": valor}]))
        return [x["tipo"] for x in d["diferencas"]]

    assert tipo(True) == [] and tipo(False) == [], "booleano de verdade cabe no contrato"
    assert tipo(1) == ["tipo_diferente"] and tipo(0) == ["tipo_diferente"], "a biblioteca lista destaque 1 em tipo_divergente"
    assert tipo(2) == ["fora_do_dominio"] and tipo(-1) == ["fora_do_dominio"] and tipo(2.5) == ["fora_do_dominio"], "a biblioteca lista destaque 2 em valor_fora_do_dominio"
    assert tipo("Sim") == ["tipo_diferente"], "texto continua sendo tipo diferente"
    d = poda.diff_contrato(contrato, json.dumps([{"id": 1, "destaque": 2}]))
    assert d["diferencas"][0]["recebido"] == "2" and d["diferencas"][0]["esperado"] == "booleano", d["diferencas"]


def teste_poda_no_banco_de_casos_so_estes_casos_mudam():
    # o tamanho da mudança da ficha 41, preso aqui: se outro caso passar a mudar, é efeito que ninguém decidiu
    import executar_fase4 as ex
    import poda
    pelo_item, pelo_booleano = set(), set()
    for c in ex.casos_de_avaliacao("avaliacao"):
        contrato = str(c["entrada"].get("contrato") or "").strip()
        if not contrato or contrato.lower() == "n/a":
            continue
        d = poda.diff_contrato(contrato, c["entrada"].get("corpo") or "")
        if any(x.get("item") for x in d["diferencas"]):
            pelo_item.add(c["id"])
        booleanos = {x["campo"] for x in poda.campos_do_contrato(contrato) if "booleano" in x["tipos"]}
        if any(x["tipo"] == "fora_do_dominio" and x["campo"] in booleanos for x in d["diferencas"]):
            pelo_booleano.add(c["id"])
    assert pelo_item == {"sin-5", "semt-14", "sin-20", "semt-17"}, pelo_item
    assert pelo_booleano == {"semt-9"}, pelo_booleano


# ! Alteração de IA - Revisar: (05/11/2026, pacote P8) quatro testes do fechamento da fase: de qual leitura são os blocos do relatório quando o mesmo prefixo tem duas, as casas de p e de MTTR nas tabelas, e os blocos do relatório contra as leituras gravadas.
# ! Motivo: a corrida 17 tem duas leituras (os 72 casos e os 36 inéditos) e as corridas 18 e 21 têm as repetições 18b e 21b, todas com os mesmos nomes de bloco, e nas duas últimas a leitura vigente não é a de nome padrão (decisão 82 e roadmap §2.14). As tabelas de uma casa mostrariam p = 0,0003 como 0,0 e o limiar 0,990 como 1,0 no relatório da fase.
def _bloco_de_teste(prefixo: str, valor: str) -> str:
    nome = f"{prefixo}resumo"
    return f"<!-- x -->\n<!-- y -->\n# titulo\n\n<!-- tabela:{nome} -->\n| a |\n|---|\n| {valor} |\n<!-- /tabela:{nome} -->\n"


def teste_avaliar_fase4_o_relatorio_guarda_so_a_leitura_vigente_de_cada_prefixo():
    import contextlib
    import io
    import avaliar_fase4 as av
    assert av.LEITURA_NO_RELATORIO[av.PREFIXO] == "reproducibilidade"
    assert av.LEITURA_NO_RELATORIO[av.PREFIXO_TELA] == "tela_v4" and av.LEITURA_NO_RELATORIO[av.PREFIXO_CENARIOS] == "cenarios_v4"   # (06/11/2026) a 18d e a 21d passaram a valer (decisões 97 e 98)
    pasta = _temp()
    doc = pasta / "relatorio.md"
    prefixo = av.PREFIXO_TELA
    nome_bloco = f"{prefixo}resumo"
    original = f"# relatório\n\n<!-- tabela:{nome_bloco} -->\n<!-- /tabela:{nome_bloco} -->\n"
    doc.write_text(original, encoding="utf-8", newline="\n")
    md_18, md_18c = _bloco_de_teste(prefixo, "corrida 18"), _bloco_de_teste(prefixo, "corrida 18c")
    dado_18, dado_18c = {"metadados": {}, "corrida": "18"}, {"metadados": {}, "corrida": "18c"}
    silencio = io.StringIO()
    with contextlib.redirect_stdout(silencio):
        assert av.fechar_no_relatorio("tela", dado_18, md_18, prefixo, pasta=pasta, doc=doc) == 0
        assert av.fechar_no_relatorio("tela_v4", dado_18c, md_18c, prefixo, pasta=pasta, doc=doc) == 0
    assert doc.read_text(encoding="utf-8") == original, "gravar a leitura não mexe no relatório"
    # colar: só a leitura vigente, e só com a corrida dela
    for nome, md, trecho in (("tela", md_18, "tela_v4"), ("tela_v4", md_18, "tela_v4.md")):
        try:
            with contextlib.redirect_stdout(silencio):
                av.fechar_no_relatorio(nome, dado_18, md, prefixo, colar=True, pasta=pasta, doc=doc)
        except SystemExit as erro:
            assert trecho in str(erro), erro
        else:
            raise AssertionError(f"--colar de {nome} com a corrida 18 devia recusar")
        assert doc.read_text(encoding="utf-8") == original, "a recusa não mexe no relatório"
    with contextlib.redirect_stdout(silencio):
        assert av.fechar_no_relatorio("tela_v4", dado_18c, md_18c, prefixo, colar=True, pasta=pasta, doc=doc) == 0
    assert "corrida 18c" in doc.read_text(encoding="utf-8")
    # check: a vigente confere os blocos, e a outra confere só os arquivos dela
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        assert av.fechar_no_relatorio("tela_v4", dado_18c, md_18c, prefixo, check=True, pasta=pasta, doc=doc) == 0
        assert av.fechar_no_relatorio("tela", dado_18, md_18, prefixo, check=True, pasta=pasta, doc=doc) == 0
    assert "são da leitura tela_v4" in saida.getvalue(), saida.getvalue()
    with contextlib.redirect_stdout(silencio):
        assert av.fechar_no_relatorio("tela", {"metadados": {}, "corrida": "outra"}, md_18, prefixo, check=True, pasta=pasta, doc=doc) == 1, "a leitura antiga ainda confere o próprio JSON"
        (pasta / "tela_v4.md").write_text(md_18, encoding="utf-8", newline="\n")
        assert av.fechar_no_relatorio("tela_v4", dado_18c, md_18c, prefixo, check=True, pasta=pasta, doc=doc) == 1
    (pasta / "tela_v4.md").write_text(md_18c, encoding="utf-8", newline="\n")
    doc.write_text(doc.read_text(encoding="utf-8").replace("corrida 18c", "corrida 18"), encoding="utf-8", newline="\n")
    with contextlib.redirect_stdout(silencio):
        assert av.fechar_no_relatorio("tela_v4", dado_18c, md_18c, prefixo, check=True, pasta=pasta, doc=doc) == 1, "bloco colado da corrida errada aparece no --check"


def teste_avaliar_fase4_main_leva_o_nome_pedido_ao_colar_das_tres_leituras_com_duas_corridas():
    import avaliar_fase4 as av
    pedidos = []
    originais = {n: getattr(av, n) for n in ("fechar_no_relatorio", "ler_cenarios", "resumir_cenarios", "render_cenarios", "ler", "resumir", "render", "ler_tela", "resumir_tela", "render_tela")}
    argv = sys.argv
    try:
        av.fechar_no_relatorio = lambda nome, dado, md, prefixo, **kw: pedidos.append((nome, prefixo, kw.get("colar"))) or 0
        av.ler_cenarios = lambda saida: {"registros": [{}], "condicoes": {}}
        av.resumir_cenarios = lambda bruto, corrida=None: {}
        av.render_cenarios = lambda dado, titulo: ""
        av.ler = lambda saida: ([{}], [])
        av.resumir = lambda registros, fora, corrida=None: {}
        av.render = lambda dado, titulo: ""
        av.ler_tela = lambda saida: {"tela": [{}], "fixture": [], "casos": [], "por_caso": {}, "trilha_info": {}, "calibracao": {}, "condicoes": {}}
        av.resumir_tela = lambda *a, **k: {}
        av.render_tela = lambda dado, titulo: ""
        for args, esperado in ((["--cenarios", "--saida", "fase4_ensaio_v2", "--nome", "cenarios_v2", "--colar"], ("cenarios_v2", av.PREFIXO_CENARIOS, True)),
                               (["--tela", "--saida", "fase4_tela_v2", "--nome", "tela_v2", "--colar"], ("tela_v2", av.PREFIXO_TELA, True)),
                               (["--reproducao", "--saida", "fase4_reproducao", "--colar"], ("reproducibilidade", av.PREFIXO, True)),
                               (["--tela", "--saida", "fase4_tela", "--check"], ("tela", av.PREFIXO_TELA, False))):
            sys.argv = ["avaliar_fase4.py"] + args
            assert av.main() == 0, args
            assert pedidos[-1] == esperado, (args, pedidos[-1])
    finally:
        sys.argv = argv
        for nome, funcao in originais.items():
            setattr(av, nome, funcao)


def teste_avaliar_fase4_tabelas_com_tres_casas_em_p_e_em_mttr():
    import avaliar_fase4 as av
    assert av._tres(0.0003) == "0,000" and av._tres(0.1797) == "0,180" and av._tres(0.9898) == "0,990" and av._tres(None) == "não medido"
    assert av._tres(1) == "1,000"
    # as leituras gravadas: p e limiar saem nas três casas que o texto cita
    pasta = Path(__file__).resolve().parent / "resultados_alvo" / "fase4"
    if not (pasta / "tela_v2.md").exists():
        print("  (sem resultados_alvo/fase4 nesta máquina: conferência das leituras gravadas pulada)")
        return
    import analisar_fase3b as a3b

    def linha(nome_md: str, bloco: str) -> str:
        return a3b.blocos_de((pasta / nome_md).read_text(encoding="utf-8"))[bloco]
    assert "| 0,180 |" in linha("tela_v2.md", "tb_f4_tela_resumo")
    assert "| 0,000 |" in linha("tela.md", "tb_f4_tela_resumo")
    assert "| 0,832 | 0,990 |" in linha("calibracao.md", "tb_f4_calibracao_resumo")
    assert "| 0,581 |" in linha("calibracao.md", "tb_f4_calibracao_r8")
    assert "| 0,639 | 0,355 | 0,887 |" in linha("cura.md", "tb_f4_cura_resumo")
    assert "| 0,275 | 31,027 |" in linha("reproducibilidade.md", "tb_f4_reproducao_custo")
    assert "| 0,297 |" in linha("trilha.md", "tb_f4_trilha_intervencoes")


def teste_relatorio_da_fase_tem_os_blocos_da_leitura_vigente():
    import analisar_fase3b as a3b
    import avaliar_fase4 as av
    pasta = Path(__file__).resolve().parent / "resultados_alvo" / "fase4"
    if not av.RELATORIO.exists() or not (pasta / "tela_v2.md").exists():
        print("  (sem o relatório da fase ou sem resultados_alvo/fase4 nesta máquina: teste pulado)")
        return
    no_relatorio = a3b.blocos_de(av.RELATORIO.read_text(encoding="utf-8"))
    # (05/11/2026) a tela e os cenários seguem a leitura vigente de `LEITURA_NO_RELATORIO` (decisão 90), e o experimento da corrida 23 entra na conta (decisão 91)
    leituras = {av.PREFIXO: "reproducibilidade", av.PREFIXO_CALIBRACAO: "calibracao", av.PREFIXO_TELA: av.LEITURA_NO_RELATORIO[av.PREFIXO_TELA], av.PREFIXO_CURA: "cura", av.PREFIXO_BIBLIOTECA: "biblioteca",
                av.PREFIXO_CENARIOS: av.LEITURA_NO_RELATORIO[av.PREFIXO_CENARIOS], av.PREFIXO_TRILHA: "trilha", av.PREFIXO_REVISAO: "leitura_revisao_trilha", "tb_f4_exp_": "experimento_prompt"}
    for prefixo, nome in leituras.items():
        gerados = a3b.blocos_de((pasta / f"{nome}.md").read_text(encoding="utf-8"))
        assert gerados, nome
        for bloco, conteudo in gerados.items():
            assert no_relatorio.get(bloco) == conteudo, f"{bloco} do relatório não é o de {nome}.md"
    assert no_relatorio[f"{av.PREFIXO_TELA}resumo"] != a3b.blocos_de((pasta / "tela.md").read_text(encoding="utf-8"))[f"{av.PREFIXO_TELA}resumo"]


# ! Alteração de IA - Revisar: (05/11/2026, ficha 42) testes de `medir_prompt_tela.py`, escritos antes do módulo.
# ! Motivo: a decisão 90 cita de onde vêm os tokens do prompt na tela e quanto cada corte tira; esses números precisam
# sair de código testado, e a separação por bloco é a parte que erraria em silêncio se um cabeçalho do prompt mudasse.
def _prompt_de_teste(arvore: str, sintoma: str, observacao: str = "poda: árvore com 54 nós") -> str:
    return (f"DOC [v] texto\n\n=====\n\nVocê analisa falhas.\n\nREQUISIÇÃO: GET /api/produtos\n\nSTATUS HTTP: 200\n\nCONTRATO ESPERADO PELA INTERFACE: id: inteiro\n\n"
            f"CORPO DA RESPOSTA:\n[]\n\nÁRVORE DE ACESSIBILIDADE DA PÁGINA:\n{arvore}\n\nSINTOMA OBSERVADO: {sintoma}\n\nOBSERVAÇÃO ADICIONAL: {observacao}\n\n"
            "Depois do raciocínio, termine com estas quatro linhas")


def teste_medir_prompt_tela_separa_os_blocos_sem_perder_nem_repetir_texto():
    import medir_prompt_tela as mp
    prompt = _prompt_de_teste('document "P"\n  main', "Nada mudou.")
    blocos = mp.blocos_do_prompt(prompt)
    assert blocos["verbetes"].startswith("DOC [v]") and blocos["instrucao"].startswith("Você analisa")
    assert blocos["corpo"].startswith("CORPO DA RESPOSTA:") and "document" in blocos["arvore"] and blocos["sintoma"].startswith("SINTOMA OBSERVADO:")
    assert blocos["observacao"].startswith("OBSERVAÇÃO ADICIONAL:") and blocos["formato"].startswith("Depois do raciocínio")
    assert "seletor" not in blocos
    assert sum(len(v) for v in blocos.values()) + len(mp.SEPARADOR) == len(prompt), "os blocos somam o prompt inteiro"


def teste_medir_prompt_tela_arvore_fica_so_com_o_que_difere_da_referencia():
    import medir_prompt_tela as mp
    ref = 'document "P"\n  navigation\n    link "A"\n  main\n    heading "H" level=2\n    group\n      heading "C1" level=3\n      text "x"\n'
    atual = 'document "P"\n  navigation\n    link "A"\n  main\n    heading "H" level=2\n    text "Erro ao carregar"\n'
    assert mp.arvore_contra_referencia(atual, {"p@normal": ref}) == 'document "P"\n    text "Erro ao carregar"'
    # página sem referência guardada: tira o que é comum com a outra página (navegação e rodapé) e os cartões, e fica o que difere
    outra = 'document "Q"\n  navigation\n    link "A"\n    searchbox "s" id="novo"\n  main\n    group\n      heading "C9" level=3\n      text "y"\n    heading "Z" level=2\n'
    assert mp.arvore_contra_referencia(outra, {"p@normal": ref}) == 'document "Q"\n    searchbox "s" id="novo"\n    heading "Z" level=2'


def teste_medir_prompt_tela_sintoma_guarda_as_contagens_e_perde_as_listas():
    import medir_prompt_tela as mp
    s = ('SINTOMA OBSERVADO: A conferência falhou. A tela mostra 140 linha(s) a menos que a referência; faltam: - img; - img; - img. '
         'A tela mostra 1 linha(s) a mais que a referência; sobram: - text: "Erro em 1.5".\n\n')
    assert mp.sintoma_sem_listas(s) == "SINTOMA OBSERVADO: A conferência falhou. A tela mostra 140 linha(s) a menos que a referência. A tela mostra 1 linha(s) a mais que a referência.\n\n"
    assert mp.sintoma_sem_listas("SINTOMA OBSERVADO: Nada mudou.\n\n") == "SINTOMA OBSERVADO: Nada mudou.\n\n"


def teste_medir_prompt_tela_tokens_e_limite_vem_dos_dados():
    import medir_prompt_tela as mp
    assert mp.tokens_apos_corte(1000, 3000, 300) == 900, "o corte vale a razão de tokens por caractere do próprio prompt"
    assert mp.limite_do_plano(1281) == 1409, "o maior prompt da calibração mais 10%, arredondado para baixo"
    assert mp.resumo([1, 2, 3, 10]) == {"min": 1, "mediana": 2.5, "max": 10}


def teste_medir_prompt_tela_cortes_em_cascata_nunca_aumentam_o_prompt():
    import medir_prompt_tela as mp
    ref = 'document "P"\n  main\n    heading "H" level=2\n'
    prompt = _prompt_de_teste('document "P"\n  main\n    heading "H" level=2\n    text "novo"', 'A tela mostra 3 linha(s) a menos que a referência; faltam: - img; - img.')
    tokens = {n: mp.tokens_apos_corte(1000, len(prompt), len(prompt) - len(c)) for n, c in mp.cortes(prompt, {"p@normal": ref}).items()}
    assert list(tokens) == list(mp.DESCRICAO_DOS_CENARIOS)
    assert tokens["hoje"] == 1000
    assert tokens["hoje"] > tokens["arvore"] > tokens["arvore_observacao"] > tokens["arvore_observacao_sintoma"]
    assert tokens["sem_arvore"] < tokens["hoje"]


def teste_medir_prompt_tela_nos_dados_gravados_bate_com_a_ficha_42():
    import medir_prompt_tela as mp
    raiz = Path(__file__).resolve().parent / "resultados_alvo"
    if not (raiz / "fase4_tela_v2" / "trilha_tela.jsonl").exists():
        print("  (sem resultados_alvo nesta máquina: teste pulado)")
        return
    d = mp.medir(raiz)
    assert d["limite"]["tokens"] == 1409 and d["limite"]["maior_da_calibracao"] == 1281
    c18, c21 = d["corridas"]["18b"], d["corridas"]["21b"]
    assert c18["prompts"] == 37 and c21["prompts"] == 10
    assert c18["cenarios"]["hoje"]["acima_do_limite"] == 37 and c18["cenarios"]["hoje"]["max"] == 2034
    assert c21["cenarios"]["hoje"]["acima_do_limite"] == 9
    assert all(sum(b["mediana"] for b in c["blocos_chars"].values()) > 0 for c in (c18, c21))


# ! Alteração de IA - Revisar: (05/11/2026, ficha 42, decisão 90) testes do corte do caso ao vivo: a árvore do prompt fica com
# o título e o que a referência em modo normal não tem; sem referência, sem cartões e sem linhas repetidas; o SINTOMA guarda as
# contagens de linhas e perde as listas; os campos ausentes viram uma frase só; a OBSERVAÇÃO sai da entrada e fica no caso, fora
# do prompt e da busca; e o prompt fixo não muda.
# ! Motivo: o plano aprovado (seção 3.3) limita o prompt na tela ao maior da calibração mais 10%, e na corrida 18b os 37 prompts
# passaram disso. Sem estes testes, uma mudança no molde voltaria a encher o prompt e ninguém veria antes de uma noite de máquina.
def teste_corte_arvore_fica_com_o_titulo_e_o_que_a_referencia_nao_tem():
    import caso_ao_vivo as cv
    ref = ('document "Produtos"\n  navigation\n    link "CONTATO" href="index.php#contato"\n  main\n    heading "Produtos via API" level=2\n'
           '    group\n      heading "Picanha" level=3\n      button "R$ 89,90" class="btn"\n    text "(mais 11 cartões omitidos pela poda)"\n    heading "Links" level=4\n')
    assert cv.arvore_do_prompt(ref, ref, set()) == 'document "Produtos"', "tela igual à referência: só o título"
    atual = ref.replace("(mais 11", "(mais 10").replace('    heading "Links" level=4\n', '    text "Erro ao carregar"\n    heading "Links" level=4\n')
    assert cv.arvore_do_prompt(atual, ref, set()) == 'document "Produtos"\n    text "Erro ao carregar"', "o aviso da poda não é da página"
    assert cv.arvore_do_prompt("", ref, set()) == "", "sem árvore, nada"


def teste_corte_arvore_tira_o_rodape_que_so_a_referencia_completa_tem():
    """A tela de erro sobe o rodapé para o nível que a poda guarda; ele não é novidade: está na árvore completa da referência."""
    import caso_ao_vivo as cv
    ref = 'document "P"\n  main\n    heading "H" level=2\n'
    atual = ('document "P"\n  main\n    heading "H" level=2\n    text "Erro ao carregar: HTTP 500"\n    text "O melhor churrasco da Zona Leste"\n'
             '    link "contato@x.com" href="mailto:contato@x.com"\n')
    nomes = {"H", "O melhor churrasco da Zona Leste", "contato@x.com"}
    assert cv.arvore_do_prompt(atual, ref, nomes) == 'document "P"\n    text "Erro ao carregar: HTTP 500"'


def teste_corte_arvore_guarda_a_linha_que_mudou_so_no_atributo():
    """Um id renomeado muda a linha e não muda o nome: é a diferença que a quebra de localizador precisa mostrar."""
    import caso_ao_vivo as cv
    ref = 'document "P"\n  navigation\n    searchbox "search" id="buscar" name="buscar"\n'
    atual = 'document "P"\n  navigation\n    searchbox "search" id="buscar_novo" name="buscar"\n'
    assert cv.arvore_do_prompt(atual, ref, {"search"}) == 'document "P"\n    searchbox "search" id="buscar_novo" name="buscar"'


def teste_corte_arvore_tira_as_linhas_repetidas():
    import caso_ao_vivo as cv
    ref = 'document "Lista"\n  main\n    button " ALTERAR"\n    button " EXCLUIR"\n'
    atual = 'document "Lista"\n  main\n' + '    button " ALTERAR"\n    button " EXCLUIR ITEM"\n' * 3
    assert cv.arvore_do_prompt(atual, ref, {"ALTERAR", "EXCLUIR"}) == 'document "Lista"\n    button " EXCLUIR ITEM"'


def teste_corte_arvore_sem_referencia_tira_os_cartoes_e_as_repetidas():
    import caso_ao_vivo as cv
    atual = ('document "Lista"\n  navigation\n    link "ADMIN" href="index.php"\n  main\n    heading "Lista de Produtos" level=2\n'
             '    group\n      heading "Picanha" level=3\n      text "Carnes"\n'
             '    button " ALTERAR"\n    button " EXCLUIR"\n    button " ALTERAR"\n    button " EXCLUIR"\n    text "(mais 2 cartões omitidos pela poda)"\n')
    assert cv.arvore_do_prompt(atual) == ('document "Lista"\n  navigation\n    link "ADMIN" href="index.php"\n  main\n    heading "Lista de Produtos" level=2\n'
                                          '    button " ALTERAR"\n    button " EXCLUIR"')


def teste_corte_poda_nomes_dos_nos_limpos_como_a_poda():
    import poda
    nos = [{"papel": "text", "nome": "  Av.  Itaquera ", "profundidade": 1}, {"papel": "main", "profundidade": 0}, {"papel": "img", "nome": "", "profundidade": 2}]
    assert poda.nomes_dos_nos(nos) == {"Av. Itaquera"}
    assert poda.nomes_dos_nos(None) == set()


def teste_corte_sintoma_guarda_as_contagens_e_perde_as_listas():
    import caso_ao_vivo as cv
    arvore = cv.diff_arvore('document "x"\n  text "R$ 89,90"\n  text "b"\n', 'document "x"\n  text "undefined"\n')
    assert arvore["a_menos"] == 2 and arvore["a_mais"] == 1
    sintoma = cv.sintoma_por_molde(None, None, arvore, status=200)
    # ! Alteração de IA - Revisar: (05/11/2026, decisão 90) as duas contagens viram uma frase só quando existem as duas.
    # ! Motivo: a conferência sem modelo mostrou prompts com "A tela mostra 6 linha(s) a menos que a referência. A tela mostra 6 linha(s) a
    # mais que a referência." e o maior deles em 1408 tokens estimados, contra o limite de 1409.
    assert sintoma == "A tela mostra 2 linha(s) a menos e 1 a mais que a referência.", sintoma
    so_menos = cv.sintoma_por_molde(None, None, {"a_menos": 3, "a_mais": 0}, status=200)
    so_mais = cv.sintoma_por_molde(None, None, {"a_menos": 0, "a_mais": 4}, status=200)
    assert so_menos == "A tela mostra 3 linha(s) a menos que a referência." and so_mais == "A tela mostra 4 linha(s) a mais que a referência.", (so_menos, so_mais)
    assert arvore["faltam"] and arvore["sobram"], "as listas continuam no diff, para a trilha"


def teste_corte_campos_ausentes_viram_uma_frase_so():
    import caso_ao_vivo as cv
    sete = {"corpo": "json", "diferencas": [{"campo": c, "tipo": "ausente"} for c in ("id", "nome", "preco")] + [{"campo": "detail", "tipo": "inesperado"}]}
    assert cv._frases_do_corpo(sete) == ["Os campos id, nome e preco não vieram na resposta.", "A resposta trouxe o campo detail, que o contrato não prevê."]
    assert cv._frases_do_corpo({"corpo": "json", "diferencas": [{"campo": "id", "tipo": "ausente"}]}) == ["O campo id não veio na resposta."], "um campo: a frase de sempre"
    por_item = {"corpo": "json", "diferencas": [{"campo": "resumo", "tipo": "ausente", "item": 3}, {"campo": "tipo", "tipo": "ausente", "item": 3}, {"campo": "nome", "tipo": "ausente"}]}
    assert cv._frases_do_corpo(por_item) == ["Os campos resumo e tipo não vieram no item 3 da resposta.", "O campo nome não veio na resposta."], "o item é parte do que o sintoma afirma"


def teste_corte_caso_da_tela_leva_a_arvore_cortada_e_guarda_a_observacao_fora_do_prompt():
    import caso_ao_vivo as cv
    import estrategias
    import executar_fase4 as ex
    import recuperacao as rec
    ref = {"arvore": 'document "P"\n  main\n    heading "H" level=2\n', "nomes": {"H"}}
    podada = {"texto": 'document "P"\n  main\n    heading "H" level=2\n    text "Erro ao carregar"\n'}
    item = {"id": "run-1", "requisicao": "GET /api/produtos", "classe": 5, "nivel": 1}
    caso = ex.caso_vivo_da_tela(item, 500, "id: inteiro", "{}", "A requisição respondeu HTTP 500.", podada, ref, "poda: árvore com 54 nós e 21 linhas depois; corpo json, forma objeto, 1 diferença(s) contra o contrato")
    assert caso["entrada"]["arvore"] == 'document "P"\n    text "Erro ao carregar"'
    assert "observacao" not in caso["entrada"], "a OBSERVAÇÃO ADICIONAL não vai ao prompt nem à busca"
    assert caso["observacao_da_poda"].startswith("poda: árvore com 54 nós"), "fica no caso gravado na trilha"
    assert caso["classe"] == 5 and caso["nivel"] == 1 and caso["id"] == "run-1@tela"
    dados = estrategias._dados_do_caso(caso)
    assert "OBSERVAÇÃO ADICIONAL" not in dados and "54 nós" not in dados
    assert "54 nós" not in " ".join(rec.sinais_do_caso(caso)["consulta"])
    assert ex.caso_vivo_da_tela(item, 500, "id: inteiro", "{}", "s", None, ref, "sem captura da árvore")["entrada"].get("arvore") is None


def teste_corte_caso_do_localizador_usa_a_referencia_e_sem_observacao():
    import cenarios_fase4 as cen
    import executar_fase4 as ex
    loc = next(x for x in cen.CENARIOS_DO_ENSAIO if x["tipo"] == "localizador")
    q = cen.quebra(loc["cenario"], loc["modo"])
    r = {"conferencia_falha": {"nome": "passo 3", "passou": False, "esperado": "clicar", "observado": None}, "erro": "TimeoutError: locator.click", "chamadas": []}
    podada = {"texto": 'document "P"\n  main\n' + '    button " ALTERAR"\n    button " EXCLUIR ITEM"\n' * 4, "antes": 40, "depois": 10}
    ref = {"arvore": 'document "P"\n  main\n    button " ALTERAR"\n    button " EXCLUIR"\n', "nomes": {"ALTERAR", "EXCLUIR"}}
    caso = ex.caso_do_localizador(loc, {"quebra": q, "r": r, "podada": podada, "ref": ref})
    assert caso["entrada"]["arvore"] == 'document "P"\n    button " EXCLUIR ITEM"'
    assert "observacao" not in caso["entrada"] and "TimeoutError" in caso["observacao_da_poda"]
    assert caso["entrada"]["seletor_quebrado"] == q["localizador"]
    sem_ref = ex.caso_do_localizador(loc, {"quebra": q, "r": r, "podada": podada, "ref": {}})
    assert sem_ref["entrada"]["arvore"].count("ALTERAR") == 1, "sem a árvore da referência, ao menos sem repetidas"


def teste_corte_referencia_da_cura_guarda_a_arvore_e_os_nomes():
    import executar_fase4 as ex
    captura = {"titulo": "P", "nos": [{"papel": "main", "nome": "", "profundidade": 0}, {"papel": "button", "nome": "EXCLUIR", "profundidade": 1, "atributos": {}}],
               "interativos": [], "aria": "- main"}
    d = ex.arvore_da_referencia(captura, None)
    assert d["arvore"].startswith('document "P"') and "EXCLUIR" in d["arvore"] and d["nomes"] == {"EXCLUIR"}
    assert ex.arvore_da_referencia(None, None) == {}, "sem captura, a célula fica sem árvore de referência"
    assert ex.arvore_da_referencia({"erro": "página fechada", "nos": []}, None) == {}


def teste_corte_leitura_acha_a_observacao_fora_da_entrada():
    import avaliar_fase4 as af
    reg = {"id": "a@tela", "entrada": {"corpo": "{}", "sintoma": "s"}, "observacao_da_poda": "poda: corpo json, forma lista, 2 diferença(s) contra o contrato"}
    lida = af._leitura_do_caso_ao_vivo(af.entrada_do_caso_gravado(reg))
    assert lida["diferencas_contra_contrato"] == 2 and lida["forma_do_corpo"] == "lista"
    antigo = {"id": "b@tela", "entrada": {"corpo": "{}", "observacao": "corpo json, forma objeto, 1 diferença(s) contra o contrato"}}
    assert af._leitura_do_caso_ao_vivo(af.entrada_do_caso_gravado(antigo))["diferencas_contra_contrato"] == 1, "as corridas 18 e 18b continuam legíveis"


# ! Alteração de IA - Revisar: (05/11/2026, decisão 96) testes da busca do caso ao vivo: ela lê o corpo inteiro da resposta, o prompt
# continua com o trecho; a trilha lista os candidatos da mesma busca; e o tamanho do caso não conta o que não vai ao modelo.
# ! Motivo: a conferência sem modelo mostrou que os sinais em código da busca liam o recorte ou o resumo do CORPO: num corpo `{"preco":
# null}` os outros seis campos pareciam ausentes, e o verbete certo saía do contexto. Sem estes testes, a tela volta a procurar com menos
# informação que o caso escrito sem ninguém notar.
_CORPO_NULO = json.dumps([{"id": i, "nome": f"Produto {i}", "resumo": "r", "tipo": "Carnes", "preco": None, "imagem": "a.png", "destaque": False} for i in range(1, 15)])


def _caso_nulo(corpo_completo=None):
    import caso_ao_vivo as cv
    from banco_casos import CONTRATO_PRODUTO
    caso = cv.montar_caso("semt-8@tela", "GET /api/produtos", 200, CONTRATO_PRODUTO, '{"preco": null}', "O campo preco veio nulo.")
    if corpo_completo is not None:
        caso["corpo_completo"] = corpo_completo
    return caso


def teste_corte_busca_le_o_corpo_inteiro_e_o_prompt_leva_o_trecho():
    import diagnostico_ao_vivo as dv
    verbetes, indice = _curada()
    sem, _ = dv.montar_prompt(verbetes, indice, _caso_nulo(), 3)
    assert "nulo_inesperado" not in sem["verbetes_ids"], ("o recorte faz os outros campos parecerem ausentes", sem["verbetes_ids"])
    ctx, prompt = dv.montar_prompt(verbetes, indice, _caso_nulo(_CORPO_NULO), 3)
    assert "nulo_inesperado" in ctx["verbetes_ids"], ctx["verbetes_ids"]
    assert '{"preco": null}' in prompt and "Produto 14" not in prompt, "o corpo inteiro não vai ao prompt"
    assert dv.caso_da_busca(_caso_nulo())["entrada"]["corpo"] == '{"preco": null}', "sem corpo inteiro, a busca lê o que há"
    vazio = dv.caso_da_busca(_caso_nulo(""))
    assert vazio["entrada"]["corpo"] == "", "corpo vazio é informação, não ausência"
    assert _caso_nulo(_CORPO_NULO)["entrada"]["corpo"] == '{"preco": null}', "a entrada do caso não muda"


def teste_corte_trilha_lista_os_candidatos_da_mesma_busca():
    import diagnostico_ao_vivo as dv
    import trilha as tr
    verbetes, indice = _curada()
    caso = _caso_nulo(_CORPO_NULO)
    ctx, _ = dv.montar_prompt(verbetes, indice, caso, 3)
    _, itens = tr.candidatos(indice, dv.caso_da_busca(caso), 3)
    escolhidos = [x["id"] for x in sorted(itens, key=lambda x: x["posicao"]) if x.get("escolhido")]
    assert escolhidos == ctx["verbetes_ids"], (escolhidos, ctx["verbetes_ids"])


def teste_corte_tamanho_do_caso_nao_conta_o_que_nao_vai_ao_modelo():
    import caso_ao_vivo as cv
    com = _caso_nulo(_CORPO_NULO)
    com["observacao_da_poda"] = "poda: árvore com 193 nós"
    sem = _caso_nulo()
    assert cv.tamanho_do_caso(com) == cv.tamanho_do_caso(sem) == len(json.dumps(sem, ensure_ascii=False))


def teste_corte_corpo_do_caso_leva_um_exemplo_so():
    import caso_ao_vivo as cv
    import poda
    from banco_casos import CONTRATO_PRODUTO
    ref = [{"id": i, "nome": f"Produto {i}", "resumo": "r", "tipo": "Carnes", "preco": 10.0, "imagem": "a.png", "destaque": False} for i in range(1, 15)]
    atual = [{**x, "nome": x["nome"] + "?"} if x["id"] in (8, 11, 12) else x for x in ref]
    d = cv.diff_referencia(json.dumps(ref), json.dumps(atual), 20.0, 25.0)
    corpo = cv.corpo_do_caso(poda.diff_contrato(CONTRATO_PRODUTO, json.dumps(atual), forma_esperada="lista"), d)
    assert corpo.count('"id":') == 1 and '"id": 8' in corpo and "nome diferente em 3 itens" in corpo, corpo


def teste_corte_conferencia_estima_tokens_e_separa_o_que_mudou_os_verbetes():
    """A conferência sem modelo: os tokens saem da razão do prompt guardado, e os verbetes diferentes são separados entre o que
    o corte mudou (mesma biblioteca da corrida antiga) e o que a biblioteca de produção mudou."""
    import conferir_corte_tela as cc
    a = cc.linha_do_caso("a@tela", "x" * 3000, ["v1", "v2"], ["v1", "v3"], "x" * 6000, 2000, ["v1", "v2"])
    assert a["tokens_antes"] == 2000 and a["tokens_estimados"] == 1000 and a["chars_antes"] == 6000 and a["chars_depois"] == 3000
    assert a["mudou_pelo_corte"] is False and a["mudou_pela_biblioteca"] is True and a["verbetes_producao"] == ["v1", "v3"]
    b = cc.linha_do_caso("b@tela", "x" * 5000, ["v9", "v2"], ["v9", "v2"], "x" * 6000, 2000, ["v1", "v2"])
    assert b["tokens_estimados"] == 1667 and b["mudou_pelo_corte"] is True and b["mudou_pela_biblioteca"] is False
    r = cc.resumir([a, b], 1409)
    assert r["casos"] == 2 and r["acima_do_limite"] == ["b@tela"] and r["tokens"] == {"min": 1000, "mediana": 1333.5, "max": 1667}
    assert r["mudou_pelo_corte"] == ["b@tela"] and r["mudou_pela_biblioteca"] == ["a@tela"]
    vazio = cc.resumir([], 1409)
    assert vazio["casos"] == 0 and vazio["acima_do_limite"] == [] and vazio["tokens"] is None


def teste_corte_conferencia_diz_se_o_verbete_da_causa_certa_ficou_no_contexto():
    """A busca lê o SINTOMA, e o corte mudou o SINTOMA: a conferência compara, com o gabarito, se o verbete da causa certa continua
    entre os recuperados. O gabarito entra só nesta conta, depois de o prompt estar montado."""
    import conferir_corte_tela as cc
    perdeu = cc.linha_do_caso("a@tela", "x", ["v1"], ["v1"], "xx", 2, ["campo_ausente"], causa="campo_ausente")
    ganhou = cc.linha_do_caso("b@tela", "x", ["corpo_vazio"], ["corpo_vazio"], "xx", 2, ["v1"], causa="corpo_vazio")
    manteve = cc.linha_do_caso("c@tela", "x", ["tipo_divergente"], ["v1"], "xx", 2, ["tipo_divergente"], causa="tipo_divergente")
    assert perdeu["ouro_antes"] is True and perdeu["ouro_mesma_biblioteca"] is False and perdeu["ouro_producao"] is False
    r = cc.resumir([perdeu, ganhou, manteve], 1409)
    assert r["ouro"] == {"antes": 2, "mesma_biblioteca": 2, "producao": 1, "fixture": 0}
    assert r["perdeu_o_ouro_pelo_corte"] == ["a@tela"] and r["ganhou_o_ouro_pelo_corte"] == ["b@tela"]
    assert r["perdeu_o_ouro_pela_biblioteca"] == ["c@tela"] and r["ganhou_o_ouro_pela_biblioteca"] == []
    assert cc.linha_do_caso("d", "x", [], [], "xx", 2, [])["ouro_antes"] is None, "sem gabarito, sem conta"


# ! Alteração de IA - Revisar: (06/11/2026) a conferência sem modelo diz, caso a caso, se o prompt ficou igual ao guardado na corrida.
# ! Motivo: o teto nas listas do caso ao vivo só vale sem corrida nova se os prompts das corridas 18d e 21d não mudarem, e isso precisa sair de uma comparação byte a byte.
def teste_corte_conferencia_diz_se_o_prompt_ficou_igual():
    import conferir_corte_tela as cc
    igual = cc.linha_do_caso("a@tela", "abc", [], [], "abc", 2, [])
    diferente = cc.linha_do_caso("b@tela", "abd", [], [], "abc", 2, [])
    assert igual["prompt_igual"] is True and diferente["prompt_igual"] is False
    r = cc.resumir([igual, diferente], 1409)
    assert r["prompt_igual"] == 1 and r["prompt_diferente"] == ["b@tela"]
    assert set(cc.CORRIDAS_DE_ANTES) == {"18d", "18e", "21d"} and cc.ARQUIVO == "teto_prompt_tela.json"


# ! Alteração de IA - Revisar: (06/11/2026) a conferência mede com o próprio Ollama os prompts que mudaram de tamanho, sem cache e sem gerar resposta.
# ! Motivo: a estimativa pela razão de tokens por caractere exagerou em `semt-27`: disse 1447, e o medido foi 1367, porque o texto que saiu tinha mais tokens por caractere que o resto do prompt. O número que vai para o documento precisa ser o medido.
def teste_corte_conferencia_mede_os_tokens_sem_cache_e_so_nos_prompts_que_mudaram():
    import conferir_corte_tela as cc
    pedidos = []

    def post_de_teste(rota, corpo):
        pedidos.append((rota, corpo))
        return {"prompt_eval_count": 7}

    original = cc.co._post
    cc.co._post = post_de_teste
    try:
        assert cc.medir_tokens("abc") == 7
        rota, corpo = pedidos[0]
        assert rota == "/api/generate" and corpo["keep_alive"] == 0 and corpo["options"]["num_predict"] == 1 and corpo["options"]["num_ctx"] == cc.co.NUM_CTX and corpo["options"]["num_gpu"] == 0, corpo
        linhas = [cc.linha_do_caso("a", "xx", [], [], "xxx", 3, []), cc.linha_do_caso("b", "yyy", [], [], "yyy", 3, []), cc.linha_do_caso("c", "zzz", [], [], "zzy", 3, [])]
        cc.medir_os_que_mudaram_de_tamanho(linhas, {"a": "xx", "b": "yyy", "c": "zzz"})
        assert [l.get("tokens_medidos") for l in linhas] == [7, None, None], linhas
        assert len(pedidos) == 2, "só mede o prompt que mudou de tamanho; o resto só muda o tempo medido na hora"
    finally:
        cc.co._post = original


def teste_corte_conferencia_compara_com_o_fixture_e_acha_o_prompt_de_cada_corrida():
    import conferir_corte_tela as cc
    a = cc.linha_do_caso("a@tela", "x", ["campo_ausente"], ["campo_ausente"], "xx", 2, ["v1"], causa="campo_ausente", ids_fixture=["campo_ausente", "v2"])
    b = cc.linha_do_caso("b@tela", "x", ["v1"], ["v1"], "xx", 2, ["v1"], causa="corpo_vazio", ids_fixture=["corpo_vazio"])
    assert a["ouro_fixture"] is True and b["ouro_fixture"] is True and a["verbetes_fixture"] == ["campo_ausente", "v2"]
    assert cc.resumir([a, b], 1409)["ouro"]["fixture"] == 2
    guardados = {"contrato-x#1": ["v1"], "lex-1@tela": ["v2"], "localizador-y@cenario": ["v3"]}
    assert cc.verbetes_do_caso(guardados, "contrato-x#1@tela") == ["v1"] and cc.verbetes_do_caso(guardados, "lex-1@tela") == ["v2"]
    assert cc.verbetes_do_caso(guardados, "localizador-y@cenario") == ["v3"] and cc.verbetes_do_caso(guardados, "outro@tela") == []
    # ! Alteração de IA - Revisar: (06/11/2026) o cenário de localizador tem o id `localizador-z@cenario` no caso e `localizador-z#1` na trilha.
    # ! Motivo: a conferência não achava o prompt guardado desses quatro cenários e dizia que o verbete certo não estava lá: "de 1 para 9 dos 10 cenários", quando o medido nos registros é de 5 para 9.
    assert cc.verbetes_do_caso({"localizador-z#1": ["v4"], "localizador-zz#1": ["v5"]}, "localizador-z@cenario") == ["v4"], "o id da trilha leva o número da repetição"


# ! Alteração de IA - Revisar: (05/11/2026, decisões 91 e 92) testes das corridas em texto: o experimento dos itens da decisão 55 (corrida
# 23) muda só o que cada condição deve mudar e nunca o prompt do agente, e os 36 inéditos da ficha 27 (corrida 24) são lidos com a
# biblioteca de produção.
# ! Motivo: a corrida 23 custa cerca de 3 h, e a resposta dela só vale se a única diferença contra a corrida 16 for o item medido; a
# leitura pelo gabarito fica fora do agente, e um rótulo por extenso precisa voltar ao nome oficial para a conta ser a mesma.
def _caso_em_texto():
    from banco_casos import CONTRATO_PRODUTO
    return {"id": "x-1", "classe": 2, "nivel": 1, "origem": "fixture", "entrada": {"requisicao": "GET /api/produtos", "status": 200, "contrato": CONTRATO_PRODUTO, "corpo": "[]", "sintoma": "o cartão veio vazio"}}


def teste_corrida23_cada_condicao_muda_so_o_que_deve():
    import corridas_em_texto as ct
    import estrategias
    import taxonomia
    caso = _caso_em_texto()
    base = estrategias.linear_com_biblioteca(caso, "DOC")
    assert ct.prompt_da_condicao("base", caso, "DOC") == base, "a base é o prompt congelado, byte a byte"
    com = ct.prompt_da_condicao("exemplar", caso, "DOC")
    assert com.replace(ct.EXEMPLAR, "") == base and com.index("Você analisa") < com.index(ct.EXEMPLAR) < com.index("REQUISIÇÃO: GET /api/produtos")
    rot = ct.prompt_da_condicao("rotulos_por_extenso", caso, "DOC")
    assert rot.split("Valores permitidos")[0] == base.split("Valores permitidos")[0], "antes da lista, nada muda"
    assert "  - campo ausente\n" in rot + "\n" and "campo_ausente" not in rot
    assert set(ct.ROTULOS_POR_EXTENSO) == set(taxonomia.CAUSAS_RAIZ) and len(set(ct.ROTULOS_POR_EXTENSO.values())) == 23
    try:
        ct.prompt_da_condicao("outra", caso, "DOC")
    except ValueError:
        pass
    else:
        raise AssertionError("condição desconhecida deveria ser recusada")


def teste_corrida23_o_exemplar_nao_e_de_nenhum_caso_e_tem_a_forma_da_resposta():
    import avaliar
    import banco_casos
    import corridas_em_texto as ct
    lido = avaliar.extrair(ct.EXEMPLAR)
    assert lido["causa_raiz"] == ct.CAUSA_DO_EXEMPLAR and ct.CAUSA_DO_EXEMPLAR in banco_casos.CAUSAS_RAIZ if hasattr(banco_casos, "CAUSAS_RAIZ") else lido["causa_raiz"] == ct.CAUSA_DO_EXEMPLAR
    assert all(linha in ct.EXEMPLAR for linha in ("CAUSA_RAIZ:", "CAMPO:", "IMPACTO:", "FONTE:"))
    assert "/api/clientes" in ct.EXEMPLAR, "a rota não existe na CobaiaAPI: o exemplar não é de nenhum caso"
    assert not any("/api/clientes" in str(c["entrada"].get("requisicao")) for c in banco_casos.CASOS)
    assert "—" not in ct.EXEMPLAR and "→" not in ct.EXEMPLAR


def teste_corrida23_rotulo_por_extenso_volta_ao_nome_oficial():
    import corridas_em_texto as ct
    assert ct.rotulo_lido("Raciocínio.\nCAUSA_RAIZ: campo ausente\nCAMPO: preco") == "campo_ausente"
    assert ct.rotulo_lido("CAUSA_RAIZ: coleção no lugar de objeto.") == "colecao_no_lugar_de_objeto"
    assert ct.rotulo_lido("CAUSA_RAIZ: corpo não é JSON") == "corpo_nao_e_json"
    assert ct.rotulo_lido("**CAUSA_RAIZ:** tipo_divergente") == "tipo_divergente"
    assert ct.rotulo_lido("CAUSA_RAIZ: `chave de junção errada`") == "chave_de_juncao_errada"
    assert ct.rotulo_lido("CAUSA_RAIZ: outra coisa") == "outra coisa", "fora do conjunto fica como veio"
    assert ct.rotulo_lido("sem a linha") is None
    assert ct.rotulo_lido("CAUSA_RAIZ: tipo_divergente (o campo preco veio como texto)") == "tipo_divergente"
    assert ct.rotulo_lido("CAUSA_RAIZ: campo ausente, no campo preco") == "campo_ausente"
    assert ct.rotulo_lido("CAUSA_RAIZ: campo_ausente_preco") == "campo_ausente_preco", "um rótulo inventado não vira o oficial por começar igual"


# ! Alteração de IA - Revisar: (05/11/2026, decisão 91) a leitura das condições lê os 90 registros da corrida 16 como o leitor oficial.
# ! Motivo: `avaliar.extrair` guarda só a primeira palavra da linha CAUSA_RAIZ, então "campo ausente" viraria "campo"; a leitura nova lê a
# linha inteira. O acerto da base entra na mesma tabela das condições e precisa ser o número publicado da corrida 16.
def teste_corrida23_a_leitura_nova_nao_muda_a_corrida_16():
    import avaliar
    import corridas_em_texto as ct
    import executar_bateria
    arq = ct._pasta_da_base() / "qwen2.5_7b" / "diagnosticos__L100.jsonl"
    if not arq.exists():
        return
    registros = executar_bateria.ler_jsonl(arq)
    assert len(registros) == 90
    for r in registros:
        oficial = avaliar.avaliar_registro(r, set())
        rotulo = ct.rotulo_lido(r["resposta"])
        assert oficial["causa_correta"] == (rotulo == r["gabarito"]["causa_raiz"]), (r["caso"], r["resposta"][-200:])
        assert (rotulo or "") == avaliar._normalizar(oficial["causa_respondida"] or ""), (r["caso"], oficial["causa_respondida"])


def _registro_em_texto(caso, resposta, causa=None, particao="avaliacao", tokens=1000, segundos=60.0):
    return {"caso": caso, "resposta": resposta, "gabarito": {"causa_raiz": causa} if causa else None, "particao": particao, "tokens_entrada": tokens, "segundos": segundos, "versao_ollama": "0.40.14"}


def teste_corrida23_resumo_compara_com_a_corrida_16_caso_a_caso():
    import corridas_em_texto as ct
    base = [_registro_em_texto("a", "CAUSA_RAIZ: campo_ausente", "campo_ausente"), _registro_em_texto("b", "CAUSA_RAIZ: corpo_vazio", "tipo_divergente", particao="aprendizado"),
            _registro_em_texto("c", "CAUSA_RAIZ: erro_interno_do_servidor", "erro_interno_do_servidor"), _registro_em_texto("d", "CAUSA_RAIZ: tipo_divergente", "tipo_divergente")]
    por = {"exemplar": [_registro_em_texto("a", "CAUSA_RAIZ: campo_ausente", tokens=1100, segundos=70.0), _registro_em_texto("b", "CAUSA_RAIZ: tipo_divergente", tokens=1100),
                        _registro_em_texto("c", "CAUSA_RAIZ: erro_interno_do_servidor"), _registro_em_texto("d", "CAUSA_RAIZ: erro_interno_do_servidor")],
           "rotulos_por_extenso": [_registro_em_texto("a", "CAUSA_RAIZ: campo ausente"), _registro_em_texto("b", "CAUSA_RAIZ: outra coisa")]}
    d = ct.resumir_experimento(base, por, {"versao_ollama": "0.40.14"}, corrida="fase4_experimento")
    assert d["base"]["n"] == 4 and d["base"]["acertos"] == 3
    e = next(x for x in d["por_condicao"] if x["condicao"] == "exemplar")
    assert e["n"] == 4 and e["acertos"] == 3 and e["b"] == 1 and e["c"] == 1 and e["ganhos"] == ["b"] and e["perdas"] == ["d"], e
    assert e["trocas_de_rotulo"] == 2 and e["causa_do_exemplar_respondida"] == 2 and e["causa_do_exemplar_na_base"] == 1
    assert e["tokens_entrada_mediana"] == 1050.0 and e["avaliacao"]["n"] == 3 and e["avaliacao"]["acertos"] == 2, e
    r = next(x for x in d["por_condicao"] if x["condicao"] == "rotulos_por_extenso")
    assert r["n"] == 2 and r["completo"] is False and r["fora_do_conjunto"] == 1 and r["forma"] == {"oficial": 0, "por_extenso": 1, "outra": 1}, r
    assert ct._mediana([1.111, 1.114]) == 1.11, "a mediana sai em duas casas: na corrida 23 a leitura imprimiu 55,364999999999995"
    md = ct.render_experimento(d)
    for bloco in ("tb_f4_exp_resumo", "tb_f4_exp_mudaram"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    assert "—" not in md and "→" not in md


def teste_corrida23_diagnostico_de_uma_condicao_grava_o_registro_oficial():
    import corridas_em_texto as ct
    import diagnostico_ao_vivo as dv
    verbetes, indice = _curada()
    caso = _caso_em_texto()
    chamadas: list = []
    comum = {"digest": "d", "versao_ollama": "0.40.14", "maquina": "m", "biblioteca_versao": "h", "particao": None, "k": 3, "teto_tokens": 600}
    with _ollama_de_mentira_v2(lambda prompt, corpo: ("Curto.\nCAUSA_RAIZ: campo ausente\nCAMPO: preco\nIMPACTO: x.\nFONTE: nenhum", .9, []), chamadas):
        reg = ct.diagnosticar_na_condicao("qwen2.5:7b", caso, "rotulos_por_extenso", verbetes, indice, comum, teto=600, top=5, k=3)
    assert tuple(reg) == dv.CHAVES_OFICIAIS, "o registro mantém as 37 chaves"
    assert reg["estrategia"] == "experimento_rotulos_por_extenso" and reg["caso"] == "x-1"
    assert "  - campo ausente" in chamadas[0]["prompt"], "o Ollama recebeu o prompt da condição"
    assert chamadas[0].get("logprobs") is True, "como na corrida 16"


# ! Alteração de IA - Revisar: (06/11/2026) a leitura da corrida 24 separa o acerto com e sem o verbete certo no contexto e compara com o lado escrito e com a tela da corrida 18e.
# ! Motivo: a corrida mostrou 18 de 20 com o verbete certo e 7 de 16 sem ele, e os mesmos 25 casos já tinham sido lidos em texto na 18e; os dois números precisam sair da leitura, com `--check`, e não de uma conta à parte.
def teste_corrida24_separa_o_verbete_certo_e_compara_com_a_corrida_18e():
    import corridas_em_texto as ct
    casos = [{"id": "lex-22", "classe": 1, "nivel": 1, "gabarito": {"causa_raiz": "corpo_vazio"}}, {"id": "sin-22", "classe": 2, "nivel": 1, "gabarito": {"causa_raiz": "campo_ausente"}},
             {"id": "efe-22", "classe": 6, "nivel": 3, "gabarito": {"causa_raiz": "localizador_quebrado"}}]
    regs = [_registro_em_texto("lex-22", "CAUSA_RAIZ: corpo_vazio"), _registro_em_texto("sin-22", "CAUSA_RAIZ: tipo_divergente"), _registro_em_texto("efe-22", "CAUSA_RAIZ: localizador_quebrado")]
    linhas = [{"caso": "lex-22", "p_rotulo": .99, "selo": "alto", "verbetes_ids": ["corpo_vazio"]}, {"caso": "sin-22", "p_rotulo": .5, "selo": "baixo", "verbetes_ids": ["tipo_divergente"]},
              {"caso": "efe-22", "p_rotulo": .9, "selo": "medio", "verbetes_ids": ["campo_ausente"]}]
    tela = [{"caso": "lex-22", "rotulo_fixture": "corpo_vazio", "acerto_fixture": True, "acerto_tela": True}, {"caso": "sin-22", "rotulo_fixture": "campo_ausente", "acerto_fixture": True, "acerto_tela": False}]
    d = ct.resumir_ineditos(regs, linhas, casos, {}, corrida="x", lado_escrito=tela)
    assert d["verbete_certo"] == {"presente": {"casos": 1, "acertos": 1}, "ausente": {"casos": 2, "acertos": 1}}, d["verbete_certo"]
    assert d["lado_escrito_18e"] == {"casos": 2, "mesmo_rotulo": 1, "acertos_aqui": 1, "acertos_escrito": 2, "acertos_tela": 1, "rotulo_diferente": ["sin-22"]}, d["lado_escrito_18e"]
    md = ct.render_ineditos(d)
    for bloco in ("tb_f4_ineditos_verbete", "tb_f4_ineditos_18e"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    sem = ct.resumir_ineditos(regs, linhas, casos, {}, corrida="x")
    assert sem["lado_escrito_18e"] is None and "<!-- tabela:tb_f4_ineditos_18e -->" in ct.render_ineditos(sem), "sem a 18e, o bloco diz que não há leitura"


def teste_corrida24_resumo_le_o_gabarito_so_na_leitura():
    import corridas_em_texto as ct
    casos = [{"id": "lex-22", "classe": 1, "nivel": 1, "gabarito": {"causa_raiz": "corpo_vazio"}}, {"id": "sin-22", "classe": 2, "nivel": 1, "gabarito": {"causa_raiz": "campo_ausente"}},
             {"id": "efe-22", "classe": 6, "nivel": 3, "gabarito": {"causa_raiz": "localizador_quebrado"}}]
    regs = [_registro_em_texto("lex-22", "CAUSA_RAIZ: corpo_vazio"), _registro_em_texto("sin-22", "CAUSA_RAIZ: tipo_divergente"), _registro_em_texto("efe-22", "CAUSA_RAIZ: localizador_quebrado")]
    linhas = [{"caso": "lex-22", "p_rotulo": .99, "selo": "alto", "verbetes_ids": ["corpo_vazio"]}, {"caso": "sin-22", "p_rotulo": .5, "selo": "baixo", "verbetes_ids": ["tipo_divergente"]},
              {"caso": "efe-22", "p_rotulo": .9, "selo": "medio", "verbetes_ids": ["campo_ausente"]}]
    d = ct.resumir_ineditos(regs, linhas, casos, {"versao_ollama": "0.40.14", "biblioteca": {"hash": "h"}}, referencia={"casos": 36, "acertos": 31, "acerto_pct": 86.1}, corrida="fase4_ineditos")
    r = d["resumo"]
    assert r["casos"] == 3 and r["acertos"] == 2 and r["acerto_pct"] == 66.7 and r["erros"] == ["sin-22"] and r["verbete_certo_no_contexto"] == 1, r
    assert [x["classe"] for x in d["por_classe"]] == [1, 2, 6] and d["por_classe"][1]["acertos"] == 0
    assert {x["selo"]: (x["casos"], x["erros"]) for x in d["por_selo"]} == {"alto": (1, 0), "medio": (1, 0), "baixo": (1, 1)}
    assert d["referencia"]["acertos"] == 31
    md = ct.render_ineditos(d)
    for bloco in ("tb_f4_ineditos_resumo", "tb_f4_ineditos_classe", "tb_f4_ineditos_selo", "tb_f4_ineditos_casos"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    assert "—" not in md and "→" not in md


# ! Alteração de IA - Revisar: (06/11/2026, decisão 98) a regra R2 conta os casos que a tela perde para o caso escrito (c até 3), com b e a soma ao lado.
# ! Motivo: a regra se chama "a tela não piora", e a conta b + c penalizava a tela que passa à frente do caso escrito. A leitura foi fixada pelo Eric antes da corrida 18d, sem conhecer o resultado dela; nas corridas 18, 18b e 18c nada muda, porque c foi 16, 7 e 5.
def _resumo_r2_de_teste(pares):
    import avaliar_fase4 as av
    casos = [{"id": f"x{i}", "classe": 1, "nivel": 1, "gabarito": {"causa_raiz": "campo_ausente"}} for i in range(len(pares))]

    def reg(i, certo):
        return {"caso": f"x{i}@tela", "resposta": f"CAUSA_RAIZ: {'campo_ausente' if certo else 'tipo_divergente'}", "verbetes_ids": [], "tokens_entrada": 1000, "segundos": 50.0}

    tela = [reg(i, a) for i, (a, _) in enumerate(pares)]
    fixture = [reg(i, b) for i, (_, b) in enumerate(pares)]
    return av.resumir_tela(tela, fixture, casos, [], gerado_em="2026-11-06T10:00:00", corrida="x")


def teste_avaliar_fase4_regra_r2_conta_o_que_a_tela_perde():
    import avaliar_fase4 as av
    melhor = _resumo_r2_de_teste([(True, False)] * 5 + [(False, True)] * 1 + [(True, True)] * 4)
    r = melhor["resumo"]
    assert (r["b"], r["c"], r["discordantes"]) == (5, 1, 6)
    assert r["dentro_do_limite_r2"] is True, "a tela à frente do caso escrito não reprova a regra"
    assert r["dentro_pela_soma"] is False, "a conta antiga continua à vista"
    no_limite = _resumo_r2_de_teste([(False, True)] * 3 + [(True, True)] * 4)["resumo"]
    assert no_limite["c"] == 3 and no_limite["dentro_do_limite_r2"] is True and no_limite["dentro_pela_soma"] is True
    acima = _resumo_r2_de_teste([(False, True)] * 4 + [(True, True)] * 4)["resumo"]
    assert acima["c"] == 4 and acima["dentro_do_limite_r2"] is False
    md = av.render_tela(melhor)
    assert "decisão 98" in md and "b + c" in md and "—" not in md


# ! Alteração de IA - Revisar: (06/11/2026, decisão 97) a chave que volta a busca do caso ao vivo à da corrida 18c.
# ! Motivo: se a regra não fechar, o agente volta mudando uma linha, sem perder as decisões registradas nem a leitura da regra; restaurar os arquivos do ponto seguro apagaria as duas dos documentos.
def teste_busca_a_chave_do_ponto_seguro_desliga_os_sinais():
    import caso_ao_vivo as cv
    a = {"id": 1, "nome": "Água Mineral", "tipo": "Bebidas", "preco": 6.0, "destaque": False}
    b = {"id": 2, "nome": "Picanha", "tipo": "Carnes", "preco": 89.9, "destaque": True}
    assert cv.SINAIS_DA_REFERENCIA_NA_BUSCA is True, "a busca nova é a que está valendo"
    assert _fenomenos_de_teste([a, b, b]) == ["duplicado", "duplicado"]
    cv.SINAIS_DA_REFERENCIA_NA_BUSCA = False
    try:
        assert _fenomenos_de_teste([a, b, b]) == [] and _fenomenos_de_teste([{**a, "preco": 600.0}, b], tempo_ms=2000) == [], "desligada, a busca é a da corrida 18c"
    finally:
        cv.SINAIS_DA_REFERENCIA_NA_BUSCA = True


# ! Alteração de IA - Revisar: (06/11/2026) teto nas listas do caso ao vivo: ids que faltam e sobram, ids repetidos e campos diferentes; o diff guardado continua completo.
# ! Motivo: na corrida 18e, `semt-27` (todos os ids trocados por negativos) listou 28 ids no CORPO e de novo no SINTOMA, com 1829 tokens, e `tra-26` (seis campos diferentes) escreveu uma frase por campo, com 1620; o limite do plano é 1409, e ele manda a poda apertar. Nos prompts guardados das corridas 18d e 21d nenhuma lista passa destes tetos, então nenhum deles muda.
def _diff_de_teste(ref, atual):
    import caso_ao_vivo as cv
    return cv.diff_referencia(json.dumps(ref), json.dumps(atual), 10, 10)


def teste_caso_ao_vivo_lista_que_muda_inteira_tem_teto():
    import caso_ao_vivo as cv
    ref = [{"id": i, "nome": f"Produto {i}", "preco": 10.0} for i in range(1, 15)]
    d = _diff_de_teste(ref, [{**x, "id": -(x["id"] + 1)} for x in ref])
    assert len(d["faltam"]) == 14 and len(d["sobram"]) == 14, "o diff guarda tudo: o teto é só do texto"
    corpo = cv.corpo_do_caso({"corpo": "json", "diferencas": [], "trecho": "x"}, d)
    sintoma = " ".join(cv.frases_da_referencia(d))
    for texto in (corpo, sintoma):
        assert "faltam 14 ids, entre eles 1, 2, 3" in texto and "sobram 14 ids, entre eles -2, -3, -4" in texto, texto
        assert "Produto 7" not in texto, texto
    assert len(corpo) < 150 and len(sintoma) < 150, (len(corpo), len(sintoma))


def teste_caso_ao_vivo_lista_ate_o_teto_continua_com_os_nomes():
    import caso_ao_vivo as cv
    ref = [{"id": i, "nome": f"Produto {i}", "preco": 10.0} for i in range(1, 15)]
    assert cv._clausulas_de_lista(_diff_de_teste(ref, ref[:-3])) == ['faltam os ids 12 ("Produto 12"), 13 ("Produto 13"), 14 ("Produto 14")']
    assert cv._clausulas_de_lista(_diff_de_teste(ref, ref[:-1])) == ['falta o id 14 ("Produto 14")']
    assert cv._clausulas_de_lista(_diff_de_teste(ref, ref + ref[:1])) == ['o id 1 ("Produto 1") aparece 2 vezes']


def teste_caso_ao_vivo_lista_dobrada_tem_teto_nos_repetidos():
    import caso_ao_vivo as cv
    ref = [{"id": i, "nome": f"Produto {i}", "preco": 10.0} for i in range(1, 15)]
    assert cv._clausulas_de_lista(_diff_de_teste(ref, ref + ref)) == ['o id 1 ("Produto 1") aparece 2 vezes', 'o id 2 ("Produto 2") aparece 2 vezes', 'o id 3 ("Produto 3") aparece 2 vezes', "mais 11 ids aparecem repetidos"]


def teste_caso_ao_vivo_muitos_campos_diferentes_tem_teto():
    import caso_ao_vivo as cv
    ref = [{"id": i, "nome": f"P{i}", "resumo": f"R{i}", "preco": 10.0, "imagem": f"i{i}", "destaque": False, "tipo": "T"} for i in range(1, 6)]
    atual = [{**x, "nome": x["nome"] + "x", "resumo": x["resumo"] + "x", "preco": 11.0, "imagem": x["imagem"] + "x", "destaque": True, "tipo": "U"} for x in ref]
    d = _diff_de_teste(ref, atual)
    assert cv.frases_da_referencia(d) == ['O campo nome veio diferente da referência em modo normal em 5 itens, por exemplo no id 1: "P1x" em vez de "P1".',
                                          'O campo resumo veio diferente da referência em modo normal em 5 itens, por exemplo no id 1: "R1x" em vez de "R1".',
                                          "Mais 4 campos vieram diferentes: preco, imagem, destaque, tipo."]
    corpo = cv.corpo_do_caso({"corpo": "json", "diferencas": [], "trecho": "x"}, d)
    assert corpo == "lista com 5 itens (referência em modo normal: 5); nome diferente em 5 itens; resumo diferente em 5 itens; mais 4 campos diferentes", corpo
    # no objeto (detalhe) o teto é o mesmo
    d2 = _diff_de_teste(ref[0], atual[0])
    assert cv.frases_da_referencia(d2)[-1] == "Mais 4 campos vieram diferentes: preco, imagem, destaque, tipo."
    assert cv.corpo_do_caso({"corpo": "json", "diferencas": [], "trecho": "t"}, d2) == 't (contra a referência em modo normal: nome "P1x" em vez de "P1", resumo "R1x" em vez de "R1"; mais 4 campos diferentes)'
    d3 = _diff_de_teste(ref[0], {**ref[0], "nome": "a", "resumo": "b", "preco": 1.0})
    assert cv.frases_da_referencia(d3)[-1] == "Mais 1 campo veio diferente: preco."


def teste_caso_ao_vivo_um_campo_diferente_continua_igual():
    import caso_ao_vivo as cv
    ref = [{"id": i, "nome": f"P{i}", "preco": 10.0} for i in range(1, 4)]
    d = _diff_de_teste(ref, [{**x, "preco": 1000.0} for x in ref])
    assert cv.frases_da_referencia(d) == ["O campo preco veio diferente da referência em modo normal em 3 itens, por exemplo no id 1: 1000.0 em vez de 10.0."]
    corpo = cv.corpo_do_caso({"corpo": "json", "diferencas": [], "trecho": "x"}, d)
    assert corpo.startswith("lista com 3 itens (referência em modo normal: 3); preco diferente em 3 itens; por exemplo: "), corpo


# ! Alteração de IA - Revisar: (06/11/2026) o interceptador espera a resposta em andamento antes de a corrida ler as chamadas.
# ! Motivo: reproduzido sem modelo: 1 em 25 execuções do modo error_500 saía sem a chamada capturada, com a tela já mostrando "HTTP 500". O roteiro quebra tão rápido que `registros()` lia a lista enquanto a resposta ainda estava sendo guardada; o caso ia ao modelo sem status e sem corpo, e o erro seria do teste, não do agente.
class _RespostaDeTeste:
    def __init__(self, requisicao):
        self.request, self.url, self.status, self.headers = requisicao, requisicao.url, 500, {}

    def text(self):
        return '{"detail": "x"}'


class _RequisicaoDeTeste:
    def __init__(self, url):
        self.url, self.method, self.resource_type, self.failure = url, "GET", "fetch", "falhou"
        self.frame = type("F", (), {"url": "http://localhost/p.php"})()


class _PaginaDeTeste:
    def __init__(self, ao_esperar=None):
        self.url, self.esperas, self.ao_esperar = "http://localhost/p.php", 0, ao_esperar
        self.context = type("C", (), {"route": lambda *a, **k: None, "route_from_har": lambda *a, **k: None})()

    def on(self, *_):
        return None

    def wait_for_timeout(self, _ms):
        self.esperas += 1
        if self.ao_esperar:
            self.ao_esperar()


def teste_interceptador_espera_a_resposta_em_andamento():
    import interceptador as ic
    url = f"http://{ic.HOST_DA_API}/api/produtos"
    req = _RequisicaoDeTeste(url)
    pagina = _PaginaDeTeste()
    inter = ic.Interceptador(pagina, har=None)
    inter.esperar_respostas(50)
    assert pagina.esperas == 0, "sem nada em andamento, não espera"
    inter._ao_pedir(req)
    assert inter.registros() == [], "a resposta ainda não chegou"
    pagina.ao_esperar = lambda: inter._ao_responder(_RespostaDeTeste(req))
    inter.esperar_respostas(2000)
    assert pagina.esperas == 1 and [r["status"] for r in inter.registros()] == [500], "a resposta entra no registro antes de a corrida ler"
    # a chamada que falhou também encerra a espera
    req2 = _RequisicaoDeTeste(url)
    pagina2 = _PaginaDeTeste()
    inter2 = ic.Interceptador(pagina2, har=None)
    inter2._ao_pedir(req2)
    pagina2.ao_esperar = lambda: inter2._ao_falhar(req2)
    inter2.esperar_respostas(2000)
    assert pagina2.esperas == 1
    # o que não é da CobaiaAPI não segura a corrida, e a espera tem limite
    pagina3 = _PaginaDeTeste()
    inter3 = ic.Interceptador(pagina3, har=None)
    inter3._ao_pedir(_RequisicaoDeTeste("http://localhost/imagem.png"))
    inter3.esperar_respostas(2000)
    assert pagina3.esperas == 0, "só as chamadas à CobaiaAPI contam"
    pagina4 = _PaginaDeTeste()
    inter4 = ic.Interceptador(pagina4, har=None)
    inter4._ao_pedir(_RequisicaoDeTeste(url))
    inter4.esperar_respostas(30)
    assert pagina4.esperas >= 1, "esperou"


def teste_rodar_cenario_espera_as_respostas_antes_de_ler_as_chamadas():
    import cenarios_fase4 as cen
    ordem = []
    inter = type("I", (), {"esperar_respostas": lambda self: ordem.append("espera"), "registros": lambda self: ordem.append("le") or [], "capturar": lambda self: {"nos": [], "aria": "", "contagem": 0}})()
    cen.rodar_cenario({"id": "c", "passos": []}, None, inter)
    assert ordem == ["espera", "le"], ordem


# ! Alteração de IA - Revisar: (06/11/2026, ficha 47, decisão 97) o que a comparação com a referência mede vira fenômenos, só para a busca.
# ! Motivo: na corrida 18c o verbete certo chegou ao modelo em 21 dos 37 casos na tela, porque o caso da tela mede a diferença em números e nenhum passo a traduzia para as palavras da biblioteca.
# Os testes usam dados sintéticos: as regras saem da definição de cada fenômeno, não dos casos.
def _fenomenos_de_teste(atual, tempo_ms=60, ref=None):
    import caso_ao_vivo as cv
    ref = ref if ref is not None else [{"id": 1, "nome": "Água Mineral", "tipo": "Bebidas", "preco": 6.0, "destaque": False}, {"id": 2, "nome": "Picanha", "tipo": "Carnes", "preco": 89.9, "destaque": True}]
    c_ref, c_at = json.dumps(ref, ensure_ascii=False), json.dumps(atual, ensure_ascii=False)
    return cv.fenomenos_contra_a_referencia(c_ref, c_at, cv.diff_referencia(c_ref, c_at, 50, tempo_ms))


def teste_busca_fenomenos_de_valor_contra_a_referencia():
    a = {"id": 1, "nome": "Água Mineral", "tipo": "Bebidas", "preco": 6.0, "destaque": False}
    b = {"id": 2, "nome": "Picanha", "tipo": "Carnes", "preco": 89.9, "destaque": True}
    assert _fenomenos_de_teste([a, b]) == [], "igual à referência não dá sinal nenhum"
    quebrado = "Água Mineral".encode().decode("latin-1")
    assert _fenomenos_de_teste([{**a, "nome": quebrado}, b]) == ["codificacao"], "acento quebrado que, consertado, é o valor da referência"
    assert _fenomenos_de_teste([{**a, "preco": 600.0}, {**b, "preco": 8990.0}]) == ["escala", "escala"], "um por item afetado, como nos sinais do contrato"
    assert _fenomenos_de_teste([{**a, "preco": 0.6}, b]) == ["escala"], "dez vezes menor também é escala"
    assert _fenomenos_de_teste([a, {**b, "preco": 84.9}]) == [], "uma diferença pequena de preço não é escala nem domínio"
    assert _fenomenos_de_teste([{**a, "preco": -6.1}, b]) == ["dominio"], "negativo onde a referência é positiva"
    assert _fenomenos_de_teste([{**a, "preco": 0}, b]) == ["dominio"], "zero onde a referência é positiva"
    assert _fenomenos_de_teste([{**a, "tipo": "Carnes"}, b]) == ["troca"], "o valor existe na referência, em outro item"
    assert _fenomenos_de_teste([{**a, "nome": "Água (inválido)"}, b]) == ["dominio"], "texto que a referência não tem nesse campo"
    for trocado in ({"preco": "6.0"}, {"destaque": "talvez"}, {"nome": None}, {"tipo": ["Bebidas"]}):
        assert _fenomenos_de_teste([{**a, **trocado}, b]) == [], f"tipo diferente é dos sinais do contrato: {trocado}"


def teste_busca_fenomenos_de_lista_e_de_tempo():
    import caso_ao_vivo as cv
    a = {"id": 1, "nome": "Água Mineral", "tipo": "Bebidas", "preco": 6.0, "destaque": False}
    b = {"id": 2, "nome": "Picanha", "tipo": "Carnes", "preco": 89.9, "destaque": True}
    assert _fenomenos_de_teste([a, b, b]) == ["duplicado", "duplicado"], "as duas ocorrências do item repetido, e não contagem"
    assert _fenomenos_de_teste([a]) == ["contagem"], "item a menos"
    assert _fenomenos_de_teste([a, b, {**b, "id": 3}]) == ["contagem"], "item a mais, sem repetir id"
    assert _fenomenos_de_teste([a, b], tempo_ms=2000) == ["lento"], "acima do orçamento de tempo"
    assert _fenomenos_de_teste(a, ref=dict(a)) == [] and _fenomenos_de_teste({**a, "preco": 600.0}, ref=dict(a)) == ["escala"], "objeto contra objeto"
    assert cv.fenomenos_contra_a_referencia('[{"id": 1}]', "isto não é json", None) == [], "sem comparação não há sinal"
    assert cv.fenomenos_contra_a_referencia(None, None, None) == []


def teste_busca_os_termos_vao_so_para_a_busca_e_o_caso_escrito_nao_muda():
    import caso_ao_vivo as cv
    import diagnostico_ao_vivo as dv
    import estrategias
    for fenomeno, termos in cv.TERMOS_DO_FENOMENO.items():
        assert termos and "_" not in termos and not any(c.isdigit() for c in termos), fenomeno
    assert cv.termos_da_busca(["escala", "escala"]) == f"{cv.TERMOS_DO_FENOMENO['escala']} {cv.TERMOS_DO_FENOMENO['escala']}"
    assert cv.termos_da_busca([]) == ""
    caso = cv.montar_caso("x-1@tela", "GET /api/produtos", 200, "id: inteiro", "trecho", "Sintoma X")
    caso["corpo_completo"] = '[{"id": 1}]'
    caso["sinais_da_busca"] = ["codificacao"]
    busca = dv.caso_da_busca(caso)
    assert cv.TERMOS_DO_FENOMENO["codificacao"] in busca["entrada"]["observacao"] and busca["entrada"]["corpo"] == '[{"id": 1}]'
    assert "observacao" not in caso["entrada"] and caso["entrada"]["corpo"] == "trecho", "o caso que vai ao prompt não muda"
    assert "mojibake" not in estrategias._dados_do_caso(caso), "o prompt não leva os termos"
    assert cv.tamanho_do_caso(caso) == cv.tamanho_do_caso({k: v for k, v in caso.items() if k != "sinais_da_busca"}), "o tamanho do caso conta só o que vai ao modelo"
    com_obs = cv.montar_caso("x-2@tela", "GET /api/produtos", 200, "id: inteiro", "trecho", "Sintoma", observacao="Vista antes")
    com_obs["sinais_da_busca"] = ["lento"]
    assert dv.caso_da_busca(com_obs)["entrada"]["observacao"].startswith("Vista antes "), "a observação do caso continua na busca"
    so_corpo = cv.montar_caso("x-3@tela", "GET /api/produtos", 200, "id: inteiro", "trecho", "Sintoma")
    so_corpo["corpo_completo"] = "[]"
    assert "observacao" not in dv.caso_da_busca(so_corpo)["entrada"], "sem fenômeno, a busca é a de antes"
    escrito = {"id": "lex-1", "entrada": {"requisicao": "GET /api/produtos", "corpo": "x", "sintoma": "y"}}
    assert dv.caso_da_busca(escrito) is escrito, "o caso escrito não passa por nada disto"


def teste_busca_caso_da_tela_guarda_os_fenomenos_fora_do_prompt():
    import executar_fase4 as ex
    item = {"id": "tra-1", "requisicao": "GET /api/produtos", "classe": 4, "nivel": 1}
    ref = {"arvore": 'document "P"', "nomes": set()}
    caso = ex.caso_vivo_da_tela(item, 200, "id: inteiro", "trecho", "Sintoma", None, ref, "obs", corpo_completo="[]", sinais_da_busca=["escala"])
    assert caso["sinais_da_busca"] == ["escala"] and "sinais_da_busca" not in caso["entrada"]
    sem = ex.caso_vivo_da_tela(item, 200, "id: inteiro", "trecho", "Sintoma", None, ref, "obs", corpo_completo="[]")
    assert "sinais_da_busca" not in sem, "sem fenômeno o caso fica como era"


def teste_busca_corrida_na_tela_escolhe_os_casos_pelo_banco():
    import executar_fase4 as ex
    casos, arq = ex.casos_e_reproducao_da_tela("avaliacao")
    assert arq == "reproducibilidade.json" and {c["id"] for c in casos} == {c["id"] for c in ex.casos_de_avaliacao("avaliacao")}
    casos_i, arq_i = ex.casos_e_reproducao_da_tela("ineditos_fase4")
    assert arq_i == "reproducibilidade_ineditos.json" and len(casos_i) == 36 and casos_i[0]["id"] == "lex-22"


def teste_busca_leitura_da_tela_acha_o_gabarito_dos_ineditos():
    import avaliar_fase4 as av
    import banco_casos_ineditos_fase4 as bi4
    assert av.casos_com_gabarito_da_tela()[-1]["id"] == bi4.CASOS_INEDITOS_FASE4[-1]["id"], "a leitura da tela acha também os inéditos da ficha 27"


# ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 18c) a leitura da tela conta o acerto com e sem o verbete da causa certa entre os entregues, nos dois lados, e o acerto por selo na tela; `render_tela` aceita o título.
# ! Motivo: na 18c quase todos os erros na tela são de casos sem o verbete certo no contexto, e o texto do relatório e o painel precisam dessa conta saída de script; o título fixo diria "corrida 18" na leitura da 18c.
def teste_avaliar_fase4_tela_le_o_verbete_certo_e_o_selo():
    import avaliar_fase4 as av

    def reg(caso: str, rotulo: str, verbetes: list[str]) -> dict:
        return {"caso": f"{caso}@tela", "resposta": f"CAUSA_RAIZ: {rotulo}", "verbetes_ids": verbetes, "tokens_entrada": 1000, "segundos": 50.0}

    casos = [{"id": i, "classe": 1, "nivel": 1, "gabarito": {"causa_raiz": "campo_ausente"}} for i in ("a", "b", "c", "d")]
    tela = [reg("a", "campo_ausente", ["campo_ausente", "x"]), reg("b", "tipo_divergente", ["campo_ausente"]), reg("c", "campo_ausente", ["x"]), reg("d", "tipo_divergente", ["x", "y"])]
    fixture = [reg("a", "campo_ausente", ["campo_ausente"]), reg("b", "campo_ausente", ["campo_ausente"]), reg("c", "campo_ausente", ["campo_ausente"]), reg("d", "tipo_divergente", ["x"])]
    por_caso = [{"caso": "a", "selo_tela": "alto"}, {"caso": "b", "selo_tela": "baixo"}, {"caso": "c", "selo_tela": "alto"}, {"caso": "d", "selo_tela": "baixo"}]
    d = av.resumir_tela(tela, fixture, casos, por_caso, gerado_em="2026-11-05T20:00:00", corrida="x")
    assert d["verbete_certo"]["tela"] == {"presente": {"casos": 2, "acertos": 1}, "ausente": {"casos": 2, "acertos": 1}}, d["verbete_certo"]
    assert d["verbete_certo"]["fixture"] == {"presente": {"casos": 3, "acertos": 3}, "ausente": {"casos": 1, "acertos": 0}}, d["verbete_certo"]
    assert d["acerto_por_selo"] == {"alto": {"casos": 2, "acertos": 2}, "medio": {"casos": 0, "acertos": 0}, "baixo": {"casos": 2, "acertos": 0}}, d["acerto_por_selo"]
    md = av.render_tela(d, "Título da corrida")
    assert "Título da corrida" in md and av.TITULO_TELA not in md
    assert av.TITULO_TELA in av.render_tela(d)
    for bloco in ("tb_f4_tela_verbete", "tb_f4_tela_selo"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    assert "—" not in md and "→" not in md


# ! Alteração de IA - Revisar: (05/11/2026, decisões 90 e 91) a fila das corridas 18c, 21c e 23: BOM, sem travessão, os três comandos do roadmap e a parada na primeira falha.
# ! Motivo: a fila roda sem ninguém olhando, numa janela do PowerShell 5.1, que quebra o arquivo inteiro sem BOM; a corrida 24 não entra porque espera a conferência da ficha 46.
def teste_fila_das_corridas_pendentes():
    arq = EXP / "rodar_pendencias_fase4.ps1"
    dados = arq.read_bytes()
    assert dados[:3] == b"\xef\xbb\xbf", "sem BOM"
    texto = dados[3:].decode("utf-8")
    assert "—" not in texto and "–" not in texto and "→" not in texto
    assert "de IA - Revisar" in texto and "! Motivo:" in texto
    # ! Alteração de IA - Revisar: (06/11/2026, decisão 97) a fila passa às corridas com os sinais da busca: 18d, 21d e os inéditos na tela (18e).
    # ! Motivo: as corridas 18c, 21c e 23 já rodaram, e os inéditos que reproduzem na tela são a conferência limpa dos sinais, escritos olhando só os 37 casos.
    for trecho in ('"tela", "-Saida", "fase4_tela_v4", "-Nome", "tela_v4"', '"cenarios", "-Saida", "fase4_ensaio_v4", "-Repeticoes", "1", "-Nome", "cenarios_v4"',
                   '"tela", "-Saida", "fase4_tela_ineditos", "-Nome", "tela_ineditos", "-Banco", "ineditos_fase4"', "rodar_fase4.ps1", "$LASTEXITCODE", "exit $LASTEXITCODE"):
        assert trecho in texto, trecho
    assert '"ineditos"' not in texto, "a corrida 24 espera a conferência (decisão 92)"
    roadmap = (EXP.parent.parent.parent / "Documentacao" / "memorial" / "roadmap.md").read_text(encoding="utf-8")
    for comando in ("-Modo tela -Saida fase4_tela_v4 -Nome tela_v4", "-Modo cenarios -Saida fase4_ensaio_v4 -Repeticoes 1 -Nome cenarios_v4", "-Modo tela -Saida fase4_tela_ineditos -Nome tela_ineditos -Banco ineditos_fase4"):
        assert comando in roadmap, comando


# ! Alteração de IA - Revisar: (05/11/2026, decisão 92) o documento da conferência dos 36 inéditos sai de script, com o caso, a corrida 17 e a pré-análise.
# ! Motivo: o Eric confere os casos antes da corrida 24, e nenhum número ou trecho de caso pode ser digitado à mão; a pré-análise é do Claude e precisa aparecer como tal.
def teste_conferencia_ineditos_junta_caso_corrida17_e_preanalise():
    import gerar_conferencia_ineditos as gci
    casos = [{"id": "x-1", "classe": 1, "nivel": 1, "entrada": {"requisicao": "GET /api/produtos", "status": 200, "contrato": "id: inteiro", "corpo": "{}", "sintoma": "S1", "observacao": "O1", "arvore": "document"},
              "gabarito": {"causa_raiz": "corpo_vazio", "campo_afetado": None, "termos_esperados": ["vazio"], "termos_proibidos": ["json"]}},
             {"id": "x-2", "classe": 1, "nivel": 2, "entrada": {"requisicao": "POST /api/pedidos", "status": 201, "contrato": "id: inteiro", "corpo": "{}", "sintoma": "S2"},
              "gabarito": {"causa_raiz": "tipo_divergente", "campo_afetado": "id", "termos_esperados": [], "termos_proibidos": []}}]
    reproducao = {"casos": [{"id": "x-1", "modo": "m", "reproduz": True, "motivo": "corpo diferente"}], "fora": [{"id": "x-2", "motivo": "sem tela"}]}
    pre = {"origem": "pré-análise", "casos": [{"caso": "x-1", "veredito": "ok", "o_que_olhar": "", "causa_vizinha": None, "evidencia": "a.py:1"},
                                              {"caso": "x-2", "veredito": "ver", "o_que_olhar": "Olhar o id.", "causa_vizinha": "campo_ausente", "evidencia": "b.py:2"}]}
    d = gci.resumir(casos, reproducao, pre, gerado_em="2026-11-05T20:00:00")
    assert d["resumo"] == {"casos": 2, "ok": 1, "ver": 1, "reproduzem": 1, "fora_da_tela": 1, "sem_preanalise": 0}, d["resumo"]
    assert [x["caso"] for x in d["casos"]] == ["x-2", "x-1"], "os casos para olhar vêm primeiro"
    x2 = d["casos"][0]
    assert x2["tela"] == "fora: sem tela" and x2["causa_vizinha"] == "campo_ausente" and x2["gabarito"]["causa_raiz"] == "tipo_divergente"
    assert d["casos"][1]["tela"] == "reproduz: corpo diferente"
    assert d["por_classe"] == [{"classe": 1, "casos": 2, "ok": 1, "ver": 1, "reproduzem": 1}], d["por_classe"]
    com_ponto = {"origem": "p", "casos": [{"caso": "x-1", "veredito": "ver", "o_que_olhar": "Ponto 2: a API nunca produz isso.", "causa_vizinha": None, "evidencia": "a.py:1"}]}
    nota = gci.resumir(casos[:1], reproducao, com_ponto, gerado_em="x")["casos"][0]["o_que_olhar"]
    assert nota == "A API nunca produz isso.", "'Ponto 2' é da lista do agente e não diz nada a quem lê"
    md = gci.render(d)
    for bloco in ("tb_f4_conferencia_classes", "tb_f4_conferencia_ver"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    assert "x-2" in md and "Olhar o id." in md and "S1" in md and "corpo_vazio" in md and "pré-análise" in md
    assert "—" not in md and "→" not in md
    try:
        gci.resumir(casos, reproducao, {"origem": "p", "casos": pre["casos"] + [{"caso": "z-9", "veredito": "ok"}]}, gerado_em="x")
    except ValueError as e:
        assert "z-9" in str(e)
    else:
        raise AssertionError("pré-análise de um caso que não existe no banco passou calada")


def teste_conferencia_ineditos_os_36_do_banco_batem_com_a_corrida_17_e_a_preanalise():
    import banco_casos_ineditos_fase4 as bi4
    import gerar_conferencia_ineditos as gci
    bruto = gci.ler()
    if not bruto["preanalise"]:
        return
    d = gci.resumir(bi4.CASOS_INEDITOS_FASE4, bruto["reproducao"], bruto["preanalise"], gerado_em="2026-11-05T20:00:00")
    r = d["resumo"]
    assert r["casos"] == 36 and r["ok"] + r["ver"] == 36 and r["sem_preanalise"] == 0 and r["reproduzem"] + r["fora_da_tela"] == 36, r
    assert all(x["tela"] for x in d["casos"]), "todo caso diz o que a corrida 17 viu"


# ! Alteração de IA - Revisar: (05/11/2026, decisões 91 e 92) roda as corridas 23 e 24 pelo parser do executor, com o Ollama de mentira e a
# saída em pasta temporária; a pausa de descarga do modelo fica em zero só durante o teste.
# ! Motivo: as funções `rodar_*` juntam a biblioteca, os registros e a trilha, e um nome errado nelas só apareceria com a máquina reservada,
# no meio de uma corrida de horas. O teste não lê nem grava em pasta oficial: só as saídas `_fumaca*` vão para a pasta temporária.
@contextlib.contextmanager
def _saida_temporaria_das_corridas():
    import caminhos
    import executar_fase3
    original, pausa = caminhos.fase3, executar_fase3.PAUSA_DESCARGA
    with tempfile.TemporaryDirectory() as tmp:
        caminhos.fase3 = lambda nome="fase3": {"raiz": Path(tmp) / nome} if nome.startswith("_fumaca") else original(nome)
        executar_fase3.PAUSA_DESCARGA = 0
        try:
            yield Path(tmp)
        finally:
            caminhos.fase3, executar_fase3.PAUSA_DESCARGA = original, pausa


_RESPOSTA_DA_FUMACA = "Curto.\nCAUSA_RAIZ: campo ausente\nCAMPO: preco\nIMPACTO: O usuário não vê o preço.\nFONTE: nenhum"


def teste_corrida23_roda_de_ponta_a_ponta_e_retoma():
    import corridas_em_texto as ct
    import diagnostico_ao_vivo as dv
    import executar_bateria
    import executar_fase4 as ex
    chamadas: list = []
    args = ex.montar_parser().parse_args(["--modo", "experimento_prompt", "--saida", "_fumaca_exp", "--casos", "2"])
    with _saida_temporaria_das_corridas() as tmp, _ollama_de_mentira_v2(lambda prompt, corpo: (_RESPOSTA_DA_FUMACA, .9, []), chamadas, versao="0.40.14"):
        assert ct.rodar_experimento(args) == 0
        assert len(chamadas) == 4, "2 condições x 2 casos"
        assert "EXEMPLO RESOLVIDO" in chamadas[0]["prompt"] and "  - campo ausente" in chamadas[2]["prompt"]
        assert ct.rodar_experimento(args) == 0
        assert len(chamadas) == 4, "relançar retoma de onde parou"
        condicoes = json.loads((tmp / "_fumaca_exp" / "condicoes_fase4.json").read_text(encoding="utf-8"))
        assert condicoes["parcial"] is True and condicoes["k"] == 3 and condicoes["biblioteca"]["hash"] == HASH_DA_CURADA_DOS_TESTES, condicoes["biblioteca"]
        registros = executar_bateria.ler_jsonl(tmp / "_fumaca_exp" / "qwen2.5_7b" / "diagnosticos__exemplar.jsonl")
        assert len(registros) == 2 and tuple(registros[0]) == dv.CHAVES_OFICIAIS, "o registro mantém as 37 chaves"
        assert registros[0]["gabarito"] is None and registros[0]["estrategia"] == "experimento_exemplar" and registros[0]["versao_ollama"] == "0.40.14"
        bruto = ct.ler_experimento("_fumaca_exp")
        dado = ct.resumir_experimento(bruto["base"], bruto["por_condicao"], bruto["condicoes"], corrida="_fumaca_exp")
        assert [x["n"] for x in dado["por_condicao"]] == [2, 2] and all(not x["completo"] for x in dado["por_condicao"]), dado["por_condicao"]
        assert "tb_f4_exp_resumo" in ct.render_experimento(dado)


def teste_corrida24_roda_de_ponta_a_ponta_e_retoma():
    import corridas_em_texto as ct
    import diagnostico_ao_vivo as dv
    import executar_bateria
    import executar_fase4 as ex
    import trilha as tr
    chamadas: list = []
    args = ex.montar_parser().parse_args(["--modo", "ineditos", "--saida", "_fumaca_ined", "--casos", "2"])
    resposta = _RESPOSTA_DA_FUMACA.replace("campo ausente", "campo_ausente")
    with _saida_temporaria_das_corridas() as tmp, _ollama_de_mentira_v2(lambda prompt, corpo: (resposta, .9, []), chamadas, versao="0.40.14"):
        assert ct.rodar_ineditos(args) == 0
        assert len(chamadas) == 2
        assert ct.rodar_ineditos(args) == 0
        assert len(chamadas) == 2, "relançar retoma de onde parou"
        raiz = tmp / "_fumaca_ined"
        registros = executar_bateria.ler_jsonl(raiz / "qwen2.5_7b" / "diagnosticos__ineditos.jsonl")
        assert len(registros) == 2 and tuple(registros[0]) == dv.CHAVES_OFICIAIS and registros[0]["gabarito"] is None
        assert len(executar_bateria.ler_jsonl(raiz / "ineditos.jsonl")) == 2 and len(executar_bateria.ler_jsonl(raiz / "qwen2.5_7b" / "logprobs__ineditos.jsonl")) == 2
        lida = tr.Trilha.carregar(raiz / "trilha_ineditos.jsonl")
        assert sum(1 for x in lida.linhas() if '"tipo": "entrada"' in x or '"tipo":"entrada"' in x) == 2, "uma entrada por caso, sem repetir na retomada"
        bruto = ct.ler_ineditos("_fumaca_ined")
        dado = ct.resumir_ineditos(bruto["registros"], bruto["linhas"], bruto["casos"], bruto["condicoes"], referencia=bruto["referencia"], corrida="_fumaca_ined")
        assert dado["resumo"]["casos"] == 2 and dado["por_selo"], dado["resumo"]
        assert "tb_f4_ineditos_resumo" in ct.render_ineditos(dado)


def teste_corridas_em_texto_viram_modos_do_executor_e_do_avaliador():
    import avaliar_fase4 as av
    import executar_fase4 as ex
    assert "experimento_prompt" in ex.MODOS and "ineditos" in ex.MODOS
    args = ex.montar_parser().parse_args(["--modo", "experimento_prompt", "--saida", "fase4_experimento", "--condicoes", "exemplar"])
    assert args.condicoes == "exemplar"
    lido = av.montar_parser().parse_args(["--experimento_prompt", "--saida", "fase4_experimento"])
    assert lido.experimento_prompt is True
    assert av.montar_parser().parse_args(["--ineditos", "--saida", "fase4_ineditos"]).ineditos is True


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
