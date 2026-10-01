#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria testar_fase3b.py — o runner de testes da Fase 3-B
# (executar_fase3b.py e avaliar_fase3b.py), no mesmo formato sem pytest de testar_fase3.py:
# funções teste_<nome>(), main() roda todas em ordem de definição e reporta "<nome> ok" ou a
# falha. A tag deste cabeçalho cobre as funções de teste e os helpers de teste abaixo (mesma
# convenção de testar_fase3.py — não repetir tag em cada teste_*).
# ! Motivo: a Fase 3-B (P3.1) é código novo que reaproveita executar_fase3.rodar_epoca e
# avaliar_fase3.avaliar_saida sem alterá-los; sem um runner próprio não haveria onde exercitar
# os cinco modos (ponte/cruzada/texto_max/a5/ineditos) sem depender do Ollama. Os testes deste
# arquivo são escritos ANTES de executar_fase3b.py e avaliar_fase3b.py existirem — a primeira
# rodada falha por ModuleNotFoundError nos dois imports abaixo, que é o RED aceito para
# módulo novo (esclarecimento registrado em constraints.md).
"""Testes de regressão do harness da Fase 3-B, sem pytest (asserts em Python puro)."""
import argparse
import contextlib
import hashlib
import inspect
import io
import json
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, copiado de
# testar_fase3.py/biblioteca.py:25-32.
# ! Motivo: mesmo defeito de lá — no Windows o console roda em cp1252, que não imprime os
# símbolos usados nas mensagens de falha (aspas tipográficas, acentos); sem isso o runner
# aborta com UnicodeEncodeError antes de reportar qualquer resultado.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import avaliar_fase3b
import biblioteca as bib
import caminhos
import evolucao_biblioteca as evo
import executar_fase3
import executar_fase3b
import testar_fase3
import validar_banco
from banco_casos import CASOS
from banco_casos_extra import CASOS_EXTRA

# ! Alteração de IA - Revisar: acrescenta avaliar_fase3 e decidir_modelo para os testes da
# Tarefa P2.1 (decidir_modelo.py -- decide modelo e estado da biblioteca de produção a partir
# dos resultados oficiais da Fase 3).
# ! Motivo: os testes novos chamam avaliar_fase3.acuracia_balanceada (para calcular os números
# esperados da fixture) e as funções de decidir_modelo.py (montar_candidatos, regra_36,
# bootstrap, pareto, escore_ponderado, sensibilidade, resumo_revisao_humana, montar_decisao,
# gravar, conferir) -- sem os imports não haveria como exercitar o módulo novo fora dele
# mesmo. decidir_modelo é importado no TOPO (não dentro de cada teste) porque nenhuma das
# funções dele depende de matplotlib -- só gerar_graficos_decisao (importado localmente no
# teste 7, mesma regra de teste_graficos_fase3) depende.
import avaliar_fase3
import decidir_modelo

TODOS_OS_CASOS = CASOS + CASOS_EXTRA
_MODELO_TESTE = "modelo:teste"

# Caminho fixo da corrida oficial, sem passar por caminhos.py/RESULTADOS_DIR — o teste 7 (hash
# antes/depois) precisa apontar sempre para o resultados_alvo/fase3/ real do disco, mesmo
# quando outros testes trocam caminhos.RESULTADOS por uma pasta temporária no meio da suíte.
_RAIZ_OFICIAL_FASE3 = Path(__file__).resolve().parent / "resultados_alvo" / "fase3"


# --------------------------------------------------------------------------- infra de teste

# Pastas temporárias criadas pelos testes DESTE arquivo; main() apaga todas ao fim. Separada
# de testar_fase3._TEMPORARIOS porque os testes 2-4 chamam caminhos.RESULTADOS diretamente
# (não passam por testar_fase3._c3_temporario) e o teste 6 reaproveita
# testar_fase3._arvore_fase3_sintetica(), que grava na lista DELE — main() limpa as duas.
_TEMPORARIOS: list[Path] = []


def _pasta_temporaria() -> Path:
    caminho = Path(tempfile.mkdtemp(prefix="fase3b_teste_"))
    _TEMPORARIOS.append(caminho)
    return caminho


def _com_resultados_temporarios(funcao):
    """Aponta caminhos.RESULTADOS para uma pasta temporária durante funcao(tmp) e restaura no
    finally. Ao contrário de testar_fase3._c3_temporario (que só troca RESULTADOS durante o
    cálculo de UM dict de caminhos), aqui a troca precisa durar a chamada inteira: o código
    sob teste calcula sozinho tanto caminhos.fase3('fase3') (a origem oficial) quanto
    caminhos.fase3(args.saida) (o destino da 3-B), e os dois precisam resolver sob a MESMA
    raiz temporária para o teste não tocar em resultados_alvo/fase3/ de verdade."""
    tmp = _pasta_temporaria()
    anterior = caminhos.RESULTADOS
    caminhos.RESULTADOS = tmp
    try:
        return funcao(tmp)
    finally:
        caminhos.RESULTADOS = anterior


def _hash_arvore(raiz: Path) -> str | None:
    """sha256 de (caminho relativo, tamanho, mtime_ns) de cada arquivo sob raiz, em ordem —
    não lê o CONTEÚDO (resultados_alvo/fase3/ tem dezenas de milhares de linhas de JSONL;
    reler tudo a cada teste custaria minutos), mas qualquer arquivo criado, apagado, movido ou
    regravado (o que muda o mtime mesmo com o mesmo conteúdo) muda o hash. None se a pasta não
    existir, para o teste 7 aceitar rodar numa máquina sem a corrida oficial no disco."""
    if not raiz.exists():
        return None
    h = hashlib.sha256()
    for p in sorted(raiz.rglob("*")):
        if p.is_file():
            st = p.stat()
            h.update(f"{p.relative_to(raiz).as_posix()}\0{st.st_size}\0{st.st_mtime_ns}\0"
                     .encode())
    return h.hexdigest()[:12]


def _stubs_ollama(modelo: str) -> dict:
    """Os métodos de cliente_ollama que o código da Fase 3-B chama FORA de
    executar_fase3.rodar_epoca (que os testes 2-4 substituem inteira): instalados/_get (para
    digest e versão) e um_modelo_por_vez/descarregar (guarda de 'um modelo por vez'). Mesmo
    formato de testar_fase3._ollama_de_mentira, reduzido ao que este arquivo usa —
    executar_fase3.oll É cliente_ollama (o módulo, não uma cópia), então trocar os atributos
    dele vale também para executar_fase3b.oll, que importou o mesmo módulo."""
    return {"instalados": lambda: {modelo: "deadbeef0000"},
            "um_modelo_por_vez": lambda: (True, []),
            "descarregar": lambda m: None,
            "_get": lambda caminho, timeout=30: {"version": "0.34.1-teste"}}


def _fechar_biblioteca_de_mentira(pasta_bib: Path, epoca: int, modelo: str) -> Path:
    """Cópia de verdade de bib.BASE, fechada com fechar_snapshot — o que os testes precisam
    para uma pasta 'bibliotecas/<slug>/epoca-N' oficial de mentira passar em
    evo.snapshot_fechado. O conteúdo real (e não um verbete fabricado) é o que deixa
    evo.hash_biblioteca/copiar_biblioteca exercitados de verdade, igual a
    testar_fase3._arvore_fase3_sintetica."""
    raiz = pasta_bib / f"epoca-{epoca}"
    evo.copiar_biblioteca(bib.BASE, raiz)
    validar_banco.escrever_indice(bib.carregar(raiz), raiz)
    evo.fechar_snapshot(raiz, epoca, modelo, 0, versao_ollama="0.34.1-teste")
    return raiz


# ------------------------------------------------------------------ 7a. hash oficial (antes)

# ! Alteração de IA - Revisar: teste_area_oficial_hash_antes precisa ser o PRIMEIRO teste
# definido no arquivo (main() roda em ordem de definição, igual a testar_fase3.py) — grava o
# hash em _HASH_ANTES, conferido de novo por teste_area_oficial_hash_depois, o ÚLTIMO teste
# definido, ao fim da suíte inteira.
# ! Motivo: nenhum teste deste arquivo pode escrever em base_conhecimento/ (a biblioteca
# original) nem em resultados_alvo/fase3/ (a corrida oficial fechada da Fase 3, que os cinco
# modos da 3-B só podem LER); comparar o hash antes e depois de TODA a suíte prova isso sem
# reler cada teste individualmente à procura de um write acidental.
_HASH_ANTES: dict[str, str | None] = {}


def teste_area_oficial_hash_antes() -> None:
    _HASH_ANTES["base_conhecimento"] = _hash_arvore(bib.BASE)
    _HASH_ANTES["fase3_oficial"] = _hash_arvore(_RAIZ_OFICIAL_FASE3)


# --------------------------------------------------------------------------- 1. cópia/hash

def teste_copia_snapshot_preserva_hash() -> None:
    """_preparar_copia copia um snapshot fechado preservando o hash e, numa segunda chamada
    (relance depois de queda, com o destino já lá), confere em vez de tentar copiar de novo —
    evo.copiar_biblioteca recusaria (FileExistsError) um destino que já existe."""
    tmp = _pasta_temporaria()
    origem = _fechar_biblioteca_de_mentira(tmp, 0, _MODELO_TESTE)

    destino = tmp / "destino" / "epoca-0"
    h1 = executar_fase3b._preparar_copia(origem, destino)
    assert h1 == evo.hash_biblioteca(origem), (h1, evo.hash_biblioteca(origem))
    assert evo.snapshot_fechado(destino), "cópia não ficou com fechamento.json"

    h2 = executar_fase3b._preparar_copia(origem, destino)
    assert h2 == h1, (h2, h1)


# ----------------------------------------------------------------------------- 2. ponte

def teste_ponte_prepara_saida_e_chama_rodar_epoca() -> None:
    """modo_ponte prepara a saída (particao.json, condicoes_3b.json, maquina.json) e chama
    executar_fase3.rodar_epoca com n=1, epocas=0 (só a passada final, lendo a L0) para os 36
    casos de avaliação — rodar_epoca é trocada por uma função que registra os argumentos e
    grava um JSONL sintético, então nenhuma inferência real acontece."""
    def corpo(tmp: Path) -> None:
        c3_of = caminhos.fase3("fase3")
        particao = evo.particionar(TODOS_OS_CASOS)
        c3_of["raiz"].mkdir(parents=True, exist_ok=True)
        evo.gravar_ou_conferir_particao(c3_of["particao"], particao)
        slug = executar_fase3._slug(_MODELO_TESTE)
        _fechar_biblioteca_de_mentira(c3_of["bibliotecas"] / slug, 0, _MODELO_TESTE)

        chamadas: list[dict] = []

        def rodar_epoca_de_mentira(modelo, n, casos, particao, epocas, k, mt_diag, mt_prop,
                                   pasta, pasta_bib, digest, versao_ollama=None):
            chamadas.append({"modelo": modelo, "n": n, "epocas": epocas,
                             "n_casos": len(casos)})
            pasta.mkdir(parents=True, exist_ok=True)
            linha = {"modelo": modelo, "caso": casos[0]["id"], "versao_ollama": versao_ollama}
            (pasta / f"diagnosticos__L{n - 1}.jsonl").write_text(
                json.dumps(linha, ensure_ascii=False) + "\n", encoding="utf-8")

        original = executar_fase3.rodar_epoca
        executar_fase3.rodar_epoca = rodar_epoca_de_mentira
        try:
            args = argparse.Namespace(
                saida="fase3b_ponte_teste", modelos=[_MODELO_TESTE], casos=0, k=3,
                max_tokens_diagnostico=600, max_tokens_proposta=700)
            falhas = testar_fase3._com_stubs(
                _stubs_ollama(_MODELO_TESTE), lambda: executar_fase3b.modo_ponte(args))
        finally:
            executar_fase3.rodar_epoca = original

        assert falhas == [], falhas
        assert chamadas == [{"modelo": _MODELO_TESTE, "n": 1, "epocas": 0, "n_casos": 36}], \
            chamadas

        c3b = caminhos.fase3("fase3b_ponte_teste")
        assert c3b["particao"].exists()
        assert c3b["maquina"].exists()
        condicoes = json.loads((c3b["raiz"] / "condicoes_3b.json")
                               .read_text(encoding="utf-8"))
        assert condicoes["modo"] == "ponte", condicoes
        assert condicoes["origem"] == "resultados_alvo/fase3", condicoes
        assert condicoes["modelos"] == [_MODELO_TESTE], condicoes
        # a cópia do snapshot tem de existir de fato na saída (revisão da P3.1, 21/09/2026): sem
        # esta conferência, remover a chamada a _preparar_copia do modo deixaria o teste verde
        copia = c3b["bibliotecas"] / slug / "epoca-0"
        assert evo.snapshot_fechado(copia), "modo_ponte não materializou a cópia da epoca-0"
        assert evo.hash_biblioteca(copia) == evo.hash_biblioteca(c3_of["bibliotecas"] / slug / "epoca-0")

    _com_resultados_temporarios(corpo)


# ------------------------------------------------------------------------- 3. texto_max

def teste_texto_max_aplica_e_restaura() -> None:
    """modo_texto_max troca evo.TEXTO_MAX pelo --texto-max ANTES de chamar rodar_epoca (a
    época 1 completa e a passada final) e restaura o valor original no finally, mesmo com
    rodar_epoca trocada por uma função de mentira."""
    def corpo(tmp: Path) -> None:
        c3_of = caminhos.fase3("fase3")
        particao = evo.particionar(TODOS_OS_CASOS)
        c3_of["raiz"].mkdir(parents=True, exist_ok=True)
        evo.gravar_ou_conferir_particao(c3_of["particao"], particao)
        slug = executar_fase3._slug(executar_fase3b.GRANITE)
        _fechar_biblioteca_de_mentira(c3_of["bibliotecas"] / slug, 0, executar_fase3b.GRANITE)
        pasta_diag = c3_of["raiz"] / slug
        pasta_diag.mkdir(parents=True, exist_ok=True)
        linhas = "".join(json.dumps({"caso": c["id"]}, ensure_ascii=False) + "\n"
                         for c in TODOS_OS_CASOS)
        (pasta_diag / "diagnosticos__L0.jsonl").write_text(linhas, encoding="utf-8")

        valores_durante: list[int] = []

        def rodar_epoca_de_mentira(modelo, n, casos, particao, epocas, k, mt_diag, mt_prop,
                                   pasta, pasta_bib, digest, versao_ollama=None):
            valores_durante.append(evo.TEXTO_MAX)
            pasta.mkdir(parents=True, exist_ok=True)
            linha = {"caso": casos[0]["id"], "versao_ollama": versao_ollama}
            (pasta / f"diagnosticos__L{n - 1}.jsonl").write_text(
                json.dumps(linha, ensure_ascii=False) + "\n", encoding="utf-8")

        original_rodar_epoca = executar_fase3.rodar_epoca
        original_texto_max = evo.TEXTO_MAX
        executar_fase3.rodar_epoca = rodar_epoca_de_mentira
        try:
            args = argparse.Namespace(
                saida="fase3b_texto_max_teste", modelos=None, casos=2, k=3, texto_max=600,
                max_tokens_diagnostico=600, max_tokens_proposta=700)
            falhas = testar_fase3._com_stubs(
                _stubs_ollama(executar_fase3b.GRANITE),
                lambda: executar_fase3b.modo_texto_max(args))
        finally:
            executar_fase3.rodar_epoca = original_rodar_epoca

        assert falhas == [], falhas
        assert valores_durante == [600, 600], valores_durante
        assert evo.TEXTO_MAX == original_texto_max, evo.TEXTO_MAX
        # a cópia da epoca-0 do granite tem de existir na saída (revisão da P3.1, 21/09/2026)
        copia = caminhos.fase3("fase3b_texto_max_teste")["bibliotecas"] / slug / "epoca-0"
        assert evo.snapshot_fechado(copia), "modo_texto_max não materializou a cópia da epoca-0"
        assert evo.hash_biblioteca(copia) == evo.hash_biblioteca(c3_of["bibliotecas"] / slug / "epoca-0")

    _com_resultados_temporarios(corpo)


# -------------------------------------------------------------------------------- 4. a5

def teste_a5_aplica_e_restaura() -> None:
    """modo_a5 troca executar_fase3.CONDICAO por 'A5' antes de chamar rodar_epoca (L3, passada
    final) e restaura no finally."""
    def corpo(tmp: Path) -> None:
        c3_of = caminhos.fase3("fase3")
        particao = evo.particionar(TODOS_OS_CASOS)
        c3_of["raiz"].mkdir(parents=True, exist_ok=True)
        evo.gravar_ou_conferir_particao(c3_of["particao"], particao)
        slug = executar_fase3._slug(_MODELO_TESTE)
        _fechar_biblioteca_de_mentira(c3_of["bibliotecas"] / slug, 3, _MODELO_TESTE)

        valores_durante: list[str] = []

        def rodar_epoca_de_mentira(modelo, n, casos, particao, epocas, k, mt_diag, mt_prop,
                                   pasta, pasta_bib, digest, versao_ollama=None):
            valores_durante.append(executar_fase3.CONDICAO)
            pasta.mkdir(parents=True, exist_ok=True)
            linha = {"caso": casos[0]["id"], "versao_ollama": versao_ollama}
            (pasta / f"diagnosticos__L{n - 1}.jsonl").write_text(
                json.dumps(linha, ensure_ascii=False) + "\n", encoding="utf-8")

        original_rodar_epoca = executar_fase3.rodar_epoca
        original_condicao = executar_fase3.CONDICAO
        executar_fase3.rodar_epoca = rodar_epoca_de_mentira
        try:
            args = argparse.Namespace(
                saida="fase3b_a5_teste", modelos=[_MODELO_TESTE], casos=2, k=3,
                max_tokens_diagnostico=600, max_tokens_proposta=700)
            falhas = testar_fase3._com_stubs(
                _stubs_ollama(_MODELO_TESTE), lambda: executar_fase3b.modo_a5(args))
        finally:
            executar_fase3.rodar_epoca = original_rodar_epoca

        assert falhas == [], falhas
        assert valores_durante == ["A5"], valores_durante
        assert executar_fase3.CONDICAO == original_condicao, executar_fase3.CONDICAO
        # a cópia da epoca-3 tem de existir na saída (revisão da P3.1, 21/09/2026)
        copia = caminhos.fase3("fase3b_a5_teste")["bibliotecas"] / slug / "epoca-3"
        assert evo.snapshot_fechado(copia), "modo_a5 não materializou a cópia da epoca-3"
        assert evo.hash_biblioteca(copia) == evo.hash_biblioteca(c3_of["bibliotecas"] / slug / "epoca-3")

    _com_resultados_temporarios(corpo)


# --------------------------------------------------------------------------- 5. ineditos

def teste_ineditos_sem_modulo_para_com_systemexit_2() -> None:
    """Sem banco_casos_ineditos.py, modo_ineditos para ANTES de tocar em disco ou no Ollama,
    com SystemExit de código 2 e uma mensagem clara no stderr.

    ! Alteração de IA - Revisar: a ausência do módulo passou a ser SIMULADA (sys.modules com
    None faz o import falhar com ImportError) e restaurada ao fim, em vez de exigir que o
    arquivo não exista no repositório.
    ! Motivo: banco_casos_ineditos.py foi criado em 23/09/2026 (P3.6 do plano complementar) e
    o teste, que verificava a ausência real do arquivo, passou a falhar por construção; a
    guarda do executor continua valendo para quem clonar o repositório sem o módulo, e é isso
    que o teste precisa continuar cobrindo."""
    anterior = sys.modules.get("banco_casos_ineditos")
    sys.modules["banco_casos_ineditos"] = None  # import levanta ImportError
    args = argparse.Namespace(
        saida="fase3b_ineditos_teste", modelos=[_MODELO_TESTE], versoes=None, casos=0, k=3,
        max_tokens_diagnostico=600, max_tokens_proposta=700)
    erro = io.StringIO()
    try:
        try:
            with contextlib.redirect_stderr(erro):
                executar_fase3b.modo_ineditos(args)
            assert False, "modo_ineditos deveria ter parado sem banco_casos_ineditos.py"
        except SystemExit as e:
            assert e.code == 2, e.code
        assert "banco_casos_ineditos" in erro.getvalue(), erro.getvalue()
    finally:
        if anterior is None:
            sys.modules.pop("banco_casos_ineditos", None)
        else:
            sys.modules["banco_casos_ineditos"] = anterior


def teste_ineditos_banco_real_tem_36_casos_validos() -> None:
    """! Alteração de IA - Revisar: teste novo (23/09/2026) — o banco real de casos inéditos tem 36
    casos, 2 por célula classe × nível, ids 16–21 por classe, nenhum id dos 90 antigos e todos
    válidos para taxonomia.validar_caso; a partição do modo 'ineditos' põe os 36 em avaliação.
    ! Motivo: a corrida (a) da Fase 3-B lê esse módulo pelo executor; um caso fora do padrão
    (célula vazia, id repetido, causa fora do conjunto) só apareceria no meio da corrida."""
    import banco_casos
    import banco_casos_extra
    import taxonomia
    from collections import Counter

    casos = executar_fase3b._casos_ineditos()
    assert len(casos) == 36, len(casos)
    celulas = Counter((c["classe"], c["nivel"]) for c in casos)
    assert len(celulas) == 18 and set(celulas.values()) == {2}, celulas
    ids = [c["id"] for c in casos]
    assert len(set(ids)) == 36, ids
    antigos = {c["id"] for c in banco_casos.CASOS + banco_casos_extra.CASOS_EXTRA}
    assert not set(ids) & antigos, set(ids) & antigos
    assert all(16 <= int(i.split("-")[1]) <= 21 for i in ids), ids
    problemas = {c["id"]: taxonomia.validar_caso(c) for c in casos if taxonomia.validar_caso(c)}
    assert not problemas, problemas
    particao = executar_fase3b._particao_tudo_avaliacao(casos)
    assert particao["n_avaliacao"] == 36 and particao["n_aprendizado"] == 0, particao


# ------------------------------------------------------------------- 6. avaliar_fase3b

def teste_avaliar_fase3b_modo_simples_pasta_sintetica() -> None:
    """avaliar_modo_simples (ponte/cruzada/texto_max/a5) delega inteiramente a
    avaliar_fase3.avaliar_saida sobre a árvore sintética de testar_fase3 (reaproveitada, como
    o brief pede) e grava avaliacao_fase3.json/resumo_fase3.json na mesma pasta."""
    c3 = testar_fase3._arvore_fase3_sintetica()
    avaliados, resumo = avaliar_fase3b.avaliar_modo_simples(c3)

    assert len(avaliados) == 12, len(avaliados)
    assert resumo["metadados"]["n_diagnosticos"] == 12, resumo["metadados"]
    assert c3["avaliacao"].exists() and c3["resumo"].exists(), c3
    gravado = json.loads(c3["resumo"].read_text(encoding="utf-8"))
    assert gravado["metadados"]["n_diagnosticos"] == 12, gravado["metadados"]


# ------------------------------------------------------------------- 8. rodar_fase3b.ps1

def teste_rodar_fase3b_ps1_bom_e_sem_travessao() -> None:
    caminho = Path(__file__).resolve().parent / "rodar_fase3b.ps1"
    assert caminho.exists(), caminho
    dados = caminho.read_bytes()
    assert dados[:3] == b"\xef\xbb\xbf", "rodar_fase3b.ps1 sem BOM UTF-8 (esperado EF BB BF)"
    texto = dados.decode("utf-8-sig")
    assert "—" not in texto, "rodar_fase3b.ps1 usa o travessão — (proibido em .ps1)"


# ------------------------------------------------------------------- 9. decidir_modelo (P2.1)

def _col_teste(acuracia_balanceada: float, acerto: float, *, n: int = 8,
              segundos: float = 40.0, fora: float = 0.0, formato_errado: float = 0.0) -> dict:
    """Uma COL de comparar_fases._coluna reduzida aos campos que decidir_modelo.py lê."""
    return {"n": n, "acerto_pct": acerto, "acuracia_balanceada_pct": acuracia_balanceada,
           "segundos_mediana": segundos, "fora_do_conjunto_pct": fora,
           "formato_ok_conteudo_errado_pct": formato_errado}


def _avaliados_decisao_teste() -> list[dict]:
    """8 casos (4 de 'campo_ausente', 4 de 'tipo_divergente'), 3 modelos, 2 versões de
    biblioteca (L0 e L3), todos na partição 'avaliacao' -- fixture mínima para exercitar o
    bootstrap de decidir_modelo.py sem depender de avaliacao_fase3.json real (1.440 linhas).
    m1 melhora de L0 para L3, m2 piora (autoenvenenamento), m3 fica estável -- os acertos são
    fixos à mão para os testes não dependerem de nenhuma conta externa."""
    casos = [(f"c{i}", "campo_ausente" if i <= 4 else "tipo_divergente") for i in range(1, 9)]
    acertos = {
        ("m1", 0): [True, True, False, False, True, False, False, True],
        ("m1", 3): [True, True, True, True, True, True, False, True],
        ("m2", 0): [True, True, True, True, True, False, True, True],
        ("m2", 3): [False, True, False, True, False, False, True, False],
        ("m3", 0): [True, False, True, False, True, False, True, False],
        ("m3", 3): [True, False, True, False, True, False, True, False],
    }
    avaliados = []
    for (modelo, epoca), acertos_caso in acertos.items():
        for (caso, esperada), certo in zip(casos, acertos_caso):
            avaliados.append({
                "modelo": modelo, "biblioteca_epoca": epoca, "particao": "avaliacao",
                "caso": caso, "classe": 1, "nivel": 1, "causa_esperada": esperada,
                "causa_respondida": esperada if certo else "corpo_vazio",
                "causa_correta": certo, "segundos": 30.0,
            })
    return avaliados


def _fixture_completa_decisao() -> tuple[dict, dict, list[dict]]:
    """comparacao_fases.json + resumo_fase3.json + avaliacao_fase3.json sintéticos e
    coerentes entre si (3 modelos, L0 e L3, 8 casos) -- usada pelo teste de --check, que
    precisa da árvore inteira que decidir_modelo.montar_decisao lê. m2 tem autoenvenenamento
    de 25% na transição L1→L2 (> limiar de 10%): fica vetado na regra 36."""
    avaliados = _avaliados_decisao_teste()

    def acuracia(modelo: str, epoca: int) -> float:
        pares = [(a["causa_esperada"], a["causa_respondida"]) for a in avaliados
                if a["modelo"] == modelo and a["biblioteca_epoca"] == epoca]
        return avaliar_fase3.acuracia_balanceada(pares)

    def acerto(modelo: str, epoca: int) -> float:
        itens = [a for a in avaliados if a["modelo"] == modelo and a["biblioteca_epoca"] == epoca]
        return round(100 * sum(1 for a in itens if a["causa_correta"]) / len(itens), 1)

    autoenv = {"m1": {"L0→L1": 1.0, "L1→L2": 2.0, "L2→L3": 0.0},
              "m2": {"L0→L1": 3.0, "L1→L2": 25.0, "L2→L3": 1.0},
              "m3": {"L0→L1": 2.0, "L1→L2": 1.0, "L2→L3": 3.0}}
    segundos = {"m1": 40.0, "m2": 35.0, "m3": 50.0}

    por_modelo = {}
    for modelo in ("m1", "m2", "m3"):
        colunas = {f"F3_L{ep}": _col_teste(acuracia(modelo, ep), acerto(modelo, ep), n=8,
                                          segundos=segundos[modelo] + ep, fora=1.0,
                                          formato_errado=1.0)
                  for ep in (0, 3)}
        por_modelo[modelo] = {
            "nos_36_avaliacao": colunas, "nos_90": colunas,
            "autoenvenenamento_F3": autoenv[modelo], "adesao_cega_2B_A5_pct": 12.0,
        }
    comparacao = {"por_modelo": por_modelo}

    # particao='todos' (não 'avaliacao'): avaliar_fase3.avaliar_saida monta
    # por_modelo_biblioteca_classe só a partir de _com_particao_todos(avaliados) -- ver
    # decidir_modelo.estabilidade_ranking. Usar 'avaliacao' aqui testaria uma partição que a
    # árvore real nunca grava, e o teste passaria sem exercitar o filtro de verdade.
    classe_linhas = [
        {"modelo": modelo, "biblioteca_epoca": ep, "particao": "todos", "classe": 1,
        "acuracia_balanceada_pct": acuracia(modelo, ep)}
        for modelo in ("m1", "m2", "m3") for ep in (0, 3)
    ]
    resumo_f3 = {"por_modelo_biblioteca_classe": classe_linhas, "revisao_humana": []}

    return comparacao, resumo_f3, avaliados


def teste_decidir_regra_36_veto_e_vencedor() -> None:
    """regra_36: entre os (modelo, L) elegíveis, o de maior acurácia balanceada nos 36 vence;
    quando o autoenvenenamento máximo do modelo líder passa do limiar (10%),
    montar_candidatos já marca 'vetado' (em TODOS os L daquele modelo -- ver docstring de
    montar_candidatos) e regra_36 pula para o próximo da fila. O ranking continua listando o
    vetado na posição que a acurácia dele ocupa -- só o vencedor muda."""
    comparacao = {"por_modelo": {
        "campeao-envenenado": {
            "autoenvenenamento_F3": {"L0→L1": 5.0, "L1→L2": 22.0, "L2→L3": 3.0},
            "adesao_cega_2B_A5_pct": 10.0,
            "nos_36_avaliacao": {
                "F3_L0": _col_teste(70.0, 60.0, segundos=40.0, fora=5.0, formato_errado=5.0),
                "F3_L1": None, "F3_L2": None,
                "F3_L3": _col_teste(90.0, 85.0, segundos=42.0, fora=5.0, formato_errado=5.0),
            },
        },
        "vice-limpo": {
            "autoenvenenamento_F3": {"L0→L1": 2.0, "L1→L2": 4.0, "L2→L3": 1.0},
            "adesao_cega_2B_A5_pct": 8.0,
            "nos_36_avaliacao": {
                "F3_L0": _col_teste(60.0, 55.0, segundos=30.0, fora=2.0, formato_errado=2.0),
                "F3_L1": None, "F3_L2": None,
                "F3_L3": _col_teste(80.0, 78.0, segundos=32.0, fora=2.0, formato_errado=2.0),
            },
        },
    }}
    candidatos = decidir_modelo.montar_candidatos(comparacao, limiar=10.0)
    resultado = decidir_modelo.regra_36(candidatos)

    assert resultado["ranking"][0]["modelo"] == "campeao-envenenado", resultado["ranking"][0]
    assert resultado["ranking"][0]["biblioteca_epoca"] == 3, resultado["ranking"][0]
    assert resultado["ranking"][0]["vetado"] is True, resultado["ranking"][0]

    assert resultado["vencedor"]["modelo"] == "vice-limpo", resultado["vencedor"]
    assert resultado["vencedor"]["biblioteca_epoca"] == 3, resultado["vencedor"]
    assert resultado["vencedor"]["vetado"] is False, resultado["vencedor"]


def teste_decidir_bootstrap_reprodutivel_e_top1_soma_1() -> None:
    """bootstrap: com a mesma semente, duas chamadas devolvem exatamente o mesmo dicionário
    (reamostragem determinística por random.Random); a soma de p_top1 entre os (modelo, L)
    fecha em 1,0 (±0,001) -- cada réplica escolhe UM vencedor (desempate por L menor e depois
    por nome, nunca zero nem mais de um); e uma semente diferente muda a reamostragem."""
    avaliados = _avaliados_decisao_teste()
    r1 = decidir_modelo.bootstrap(avaliados, n_bootstrap=200, semente=20260921)
    r2 = decidir_modelo.bootstrap(avaliados, n_bootstrap=200, semente=20260921)
    assert r1 == r2, "duas rodadas com a mesma semente devolveram resultados diferentes"

    soma_36 = sum(c["p_top1"] for c in r1["nos_36"]["combos"])
    assert abs(soma_36 - 1.0) < 0.001, soma_36
    soma_90 = sum(c["p_top1"] for c in r1["nos_90"]["combos"])
    assert abs(soma_90 - 1.0) < 0.001, soma_90

    r3 = decidir_modelo.bootstrap(avaliados, n_bootstrap=200, semente=1)
    assert r3 != r1, "semente diferente deveria mudar a reamostragem"


def teste_decidir_pareto_um_dominado() -> None:
    """pareto: 'a' domina 'b' nos três critérios ao mesmo tempo (mais acurácia, menos
    segundos, menos risco); 'c' troca acurácia por custo/risco e não é dominado por ninguém.
    Só 'b' fica de fora de não_dominados."""
    candidatos = [
        {"modelo": "a", "biblioteca_epoca": 0, "acuracia_balanceada_36": 80.0,
        "segundos_mediana_36": 10.0, "risco": 5.0, "vetado": False},
        {"modelo": "b", "biblioteca_epoca": 0, "acuracia_balanceada_36": 70.0,
        "segundos_mediana_36": 20.0, "risco": 10.0, "vetado": False},
        {"modelo": "c", "biblioteca_epoca": 3, "acuracia_balanceada_36": 90.0,
        "segundos_mediana_36": 30.0, "risco": 2.0, "vetado": False},
    ]
    resultado = decidir_modelo.pareto(candidatos)
    nomes = {(l["modelo"], l["biblioteca_epoca"]) for l in resultado["nao_dominados"]}
    assert nomes == {("a", 0), ("c", 3)}, resultado["nao_dominados"]
    assert resultado["candidatos_considerados"] == 3, resultado


def teste_decidir_sensibilidade_pesos_extremos() -> None:
    """sensibilidade: 'preciso' tem a maior acurácia balanceada mas é o mais caro e mais
    arriscado; 'barato' é o oposto. Com os pesos padrão (mais peso em acurácia) 'preciso'
    vence; varrendo o peso de custo_segundos até 1,0 (e zerando os outros 3, renormalizados)
    o vencedor muda para 'barato' em algum ponto da varredura."""
    candidatos = [
        {"modelo": "preciso", "biblioteca_epoca": 3, "acuracia_balanceada_36": 90.0,
        "acerto_36": 88.0, "segundos_mediana_36": 60.0, "risco": 20.0, "vetado": False},
        {"modelo": "barato", "biblioteca_epoca": 0, "acuracia_balanceada_36": 55.0,
        "acerto_36": 50.0, "segundos_mediana_36": 5.0, "risco": 2.0, "vetado": False},
    ]
    pesos = {"acuracia_balanceada_36": 0.5, "acerto_36": 0.1, "custo_segundos": 0.2,
            "risco": 0.2}
    base = decidir_modelo.escore_ponderado(candidatos, pesos)
    assert base["vencedor"]["modelo"] == "preciso", base["vencedor"]

    resultado = decidir_modelo.sensibilidade(candidatos, pesos)
    pontos = resultado["custo_segundos"]["pontos"]
    assert pontos[0]["peso"] == 0.0 and pontos[-1]["peso"] == 1.0, (pontos[0], pontos[-1])
    assert pontos[-1]["vencedor"] == "barato/L0", pontos[-1]
    assert resultado["custo_segundos"]["mudancas_de_vencedor"], \
        "varrer custo_segundos até 1,0 deveria trocar o vencedor em algum ponto"


def teste_decidir_check_detecta_alteracao_no_md() -> None:
    """--check: decidir_modelo.gravar grava decisao_modelo.json/.md; conferir() sobre os
    mesmos dados dá 0; alterando (em disco, sem recalcular nada) o texto formatado do valor
    vencedor no .md, conferir() detecta a diferença e devolve 1."""
    tmp = _pasta_temporaria()
    comparacao, resumo_f3, avaliados = _fixture_completa_decisao()
    pesos_cfg = {"limiar_autoenvenenamento_pct": 10.0,
                "pesos": {"acuracia_balanceada_36": 0.5, "acerto_36": 0.1,
                         "custo_segundos": 0.2, "risco": 0.2},
                "n_bootstrap": 50, "semente": 20260921}

    decisao = decidir_modelo.montar_decisao(comparacao, resumo_f3, avaliados, pesos_cfg)
    caminho_json = tmp / "decisao_modelo.json"
    caminho_md = tmp / "decisao_modelo.md"
    decidir_modelo.gravar(caminho_json, caminho_md, decisao)

    decisao_de_novo = decidir_modelo.montar_decisao(comparacao, resumo_f3, avaliados, pesos_cfg)
    assert decidir_modelo.conferir(caminho_json, caminho_md, decisao_de_novo) == 0
    # gerado_em diferente em disco não pode contar como divergência (revisão da P2.1, 21/09/2026:
    # as duas chamadas caíam no mesmo segundo e o teste não provava a exclusão)
    dados = json.loads(caminho_json.read_text(encoding="utf-8"))
    for chave in ("metadados", ):
        if chave in dados and isinstance(dados[chave], dict) and "gerado_em" in dados[chave]:
            dados[chave]["gerado_em"] = "2000-01-01T00:00:00"
    if "gerado_em" in dados:
        dados["gerado_em"] = "2000-01-01T00:00:00"
    caminho_json.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    assert decidir_modelo.conferir(caminho_json, caminho_md, decisao_de_novo) == 0, "gerado_em diferente foi tratado como divergência"

    valor_vencedor = decisao_de_novo["regra_36"]["vencedor"]["acuracia_balanceada_36"]
    texto_valor = f"{valor_vencedor:.1f}".replace(".", ",")
    texto = caminho_md.read_text(encoding="utf-8")
    assert texto.count(texto_valor) >= 1, (texto_valor, texto)
    caminho_md.write_text(texto.replace(texto_valor, "999,9", 1), encoding="utf-8")
    assert decidir_modelo.conferir(caminho_json, caminho_md, decisao_de_novo) == 1


def teste_decidir_revisao_humana_vazia() -> None:
    """resumo_revisao_humana: sem nenhuma linha em resumo_fase3.json['revisao_humana'],
    devolve status 'sem_avaliacao' com a frase padrão em vez de uma tabela vazia -- tanto
    para lista vazia quanto para a chave ausente."""
    resultado = decidir_modelo.resumo_revisao_humana({"revisao_humana": []})
    assert resultado["status"] == "sem_avaliacao", resultado
    assert resultado["frase"], resultado

    resultado_ausente = decidir_modelo.resumo_revisao_humana({})
    assert resultado_ausente["status"] == "sem_avaliacao", resultado_ausente


def teste_decidir_revisao_humana_le_planilha_da_pasta() -> None:
    """! Alteração de IA - Revisar: com o resumo oficial sem revisão e `c3` apontando para uma
    pasta com a planilha revisao_edicoes__<slug>.md preenchida, resumo_revisao_humana lê a
    planilha direto e devolve as proporções por modelo (22/09/2026).
    ! Motivo: resumo_fase3.json da Fase 3 não é regravado depois da bateria; as planilhas
    foram preenchidas em 22/09/2026 e a decisão precisa enxergá-las sem tocar no resumo."""
    tmp = _pasta_temporaria()
    pasta = tmp / "modelo_x"
    pasta.mkdir(parents=True)
    (pasta / "diagnosticos__L0.jsonl").write_text('{"modelo": "modelo:x"}\n', encoding="utf-8")
    cabecalho = "| # | Época | Caso | Verbete | Operação | Texto | Motivo | Avaliação | Comentário |"
    linhas = [cabecalho, "|---|---|---|---|---|---|---|---|---|",
              "| 1 | 1 | lex-1 | v | nota | t | m | Correta | ok |",
              "| 2 | 1 | lex-2 | v | nota | t | m | Errada | não |",
              "| 3 | 2 | lex-3 | v | retificacao | t | m |  |  |"]
    (tmp / "revisao_edicoes__modelo_x.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    c3 = {"raiz": tmp}
    resultado = decidir_modelo.resumo_revisao_humana(
        {"revisao_humana": []}, c3, [{"modelo": "modelo:x"}])
    assert resultado["status"] == "avaliada", resultado
    assert "planilhas" in resultado["fonte"], resultado
    p = resultado["por_modelo"]["modelo:x"]
    assert p["n"] == 3 and p["Correta"] == 33.3 and p["Errada"] == 33.3 \
        and p["sem_avaliacao"] == 33.3 and p["Parcial"] == 0.0, p
    # o resumo oficial, quando traz a revisão, continua tendo prioridade
    com_resumo = decidir_modelo.resumo_revisao_humana(
        {"revisao_humana": [{"modelo": "outro", "operacao": "nota", "Correta": 2,
                             "Parcial": 0, "Errada": 0, "sem_avaliacao": 0}]}, c3, [])
    assert com_resumo["fonte"] == "resumo_fase3.json" and "outro" in com_resumo["por_modelo"]


def teste_decidir_grafico_18() -> None:
    """fig_18 (dispersão acurácia balanceada x segundos, IC do bootstrap e não dominados
    destacados) roda sobre um decisao_modelo.json sintético e grava PNG+SVG > 0 bytes; pulado
    sem matplotlib (mesma regra de teste_graficos_fase3 -- import local, não no topo do
    arquivo, para não quebrar quem roda testar_fase3b.py sem a venv)."""
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        print("teste_decidir_grafico_18: pulado (sem matplotlib nesta venv)")
        return
    import gerar_graficos as gg
    import gerar_graficos_decisao as ggd

    comparacao, resumo_f3, avaliados = _fixture_completa_decisao()
    pesos_cfg = {"limiar_autoenvenenamento_pct": 10.0,
                "pesos": {"acuracia_balanceada_36": 0.5, "acerto_36": 0.1,
                         "custo_segundos": 0.2, "risco": 0.2},
                "n_bootstrap": 50, "semente": 20260921}
    decisao = decidir_modelo.montar_decisao(comparacao, resumo_f3, avaliados, pesos_cfg)

    destino = _pasta_temporaria() / "graficos"
    gg.GRAFICOS = destino
    ggd.fig_18(decisao)

    arquivos = sorted(destino.iterdir()) if destino.exists() else []
    assert len(arquivos) == 2, arquivos
    for arquivo in arquivos:
        assert arquivo.stat().st_size > 0, arquivo


# ------------------------------------------------------------------ 7b. hash oficial (depois)


def teste_decidir_desempate_por_licenca() -> None:
    """Decisão 36: em empate de acurácia balanceada, a licença mais permissiva vence antes da época
    mais baixa e do nome — o candidato MIT em L0 e com nome alfabeticamente menor perde para o
    Apache-2.0 em L1."""
    original = dict(decidir_modelo.LICENCAS)
    decidir_modelo.LICENCAS.update({"a-mit:1b": "MIT", "b-apache:1b": "Apache-2.0"})
    try:
        candidatos = [
            {"modelo": "a-mit:1b", "biblioteca_epoca": 0, "acuracia_balanceada_36": 80.0, "vetado": False},
            {"modelo": "b-apache:1b", "biblioteca_epoca": 1, "acuracia_balanceada_36": 80.0, "vetado": False},
            {"modelo": "c-apache-vetado:1b", "biblioteca_epoca": 0, "acuracia_balanceada_36": 90.0, "vetado": True},
        ]
        decidir_modelo.LICENCAS["c-apache-vetado:1b"] = "Apache-2.0"
        r = decidir_modelo.regra_36(candidatos)
        assert r["vencedor"]["modelo"] == "b-apache:1b", r["vencedor"]
        assert [c["modelo"] for c in r["ranking"]] == ["c-apache-vetado:1b", "b-apache:1b", "a-mit:1b"], r["ranking"]
    finally:
        decidir_modelo.LICENCAS.clear(); decidir_modelo.LICENCAS.update(original)


# ----------------------------------------------------------------------------- 7. condições (ficha 15)

def teste_gravar_condicoes_junta_modelos_de_chamadas_sucessivas() -> None:
    """! Alteração de IA - Revisar: duas chamadas de _gravar_condicoes na mesma saída (o .ps1 roda um
    modelo por vez) deixam os DOIS modelos na lista, mantêm o criado_em da primeira e recusam um modo
    diferente na mesma pasta.
    ! Motivo: ficha 15 (29/09/2026) — fase3b_ineditos ficou com um modelo só na lista porque cada
    chamada regravava o arquivo inteiro."""
    tmp = Path(tempfile.mkdtemp(prefix="cond3b_"))
    _TEMPORARIOS.append(tmp)
    c3b = {"raiz": tmp}
    executar_fase3b._gravar_condicoes(c3b, modo="ineditos", doador=None, versoes=[0, 1, 3], texto_max=None,
                                      condicao="A2", modelos=["a:1b"], versao_ollama="0.34.1")
    primeiro = json.loads((tmp / "condicoes_3b.json").read_text(encoding="utf-8"))
    executar_fase3b._gravar_condicoes(c3b, modo="ineditos", doador=None, versoes=[0, 1, 3], texto_max=None,
                                      condicao="A2", modelos=["b:7b"], versao_ollama="0.34.1")
    segundo = json.loads((tmp / "condicoes_3b.json").read_text(encoding="utf-8"))
    assert segundo["modelos"] == ["a:1b", "b:7b"], segundo
    assert segundo["criado_em"] == primeiro["criado_em"] and "atualizado_em" in segundo, segundo
    try:
        executar_fase3b._gravar_condicoes(c3b, modo="ponte", doador=None, versoes=[0], texto_max=None,
                                          condicao="A2", modelos=["c:3b"], versao_ollama="0.34.1")
    except SystemExit as e:
        assert "outra --saida" in str(e), e
    else:
        raise AssertionError("modo diferente na mesma saída não foi recusado")


def teste_completar_condicoes_le_modelos_dos_jsonl() -> None:
    """completar_condicoes junta à lista gravada os modelos que aparecem nos JSONL de diagnóstico."""
    tmp = Path(tempfile.mkdtemp(prefix="cond3b_"))
    _TEMPORARIOS.append(tmp)
    (tmp / "condicoes_3b.json").write_text(json.dumps({"modo": "ineditos", "modelos": ["b:7b"]}),
                                           encoding="utf-8")
    for slug, modelo in (("a_1b", "a:1b"), ("b_7b", "b:7b")):
        (tmp / slug).mkdir()
        (tmp / slug / "diagnosticos__L0.jsonl").write_text(
            json.dumps({"modelo": modelo, "caso": "x"}) + "\n", encoding="utf-8")
    assert executar_fase3b.completar_condicoes(tmp) == ["b:7b", "a:1b"]
    dado = json.loads((tmp / "condicoes_3b.json").read_text(encoding="utf-8"))
    assert dado["modelos"] == ["b:7b", "a:1b"] and "atualizado_em" in dado, dado


# ----------------------------------------------------------------------------- 8. curadoria (ficha 2)

def teste_curar_reaplicar_todas_reproduz_hash_oficial() -> None:
    """! Alteração de IA - Revisar: reconstrói a epoca-1 oficial do qwen2.5:7b a partir da epoca-0
    reaplicando as 40 edições aceitas, na ordem, e exige o hash gravado em fechamento.json; depois
    reconstrói sem a primeira edição e exige hash diferente. Só roda com a corrida oficial presente.
    ! Motivo: curar_biblioteca.py só retira uma edição NÃO a reaplicando; a curadoria só é confiável
    se a reconstrução completa for byte a byte a mesma biblioteca da bateria (ficha 2, 29/09/2026)."""
    import curar_biblioteca
    c3 = caminhos.fase3("fase3")
    raiz_l1 = c3["bibliotecas"] / "qwen2.5_7b" / "epoca-1"
    if not (raiz_l1 / "fechamento.json").exists():
        print("teste_curar_reaplicar_todas_reproduz_hash_oficial: pulado (sem a corrida oficial)")
        return
    oficial = json.loads((raiz_l1 / "fechamento.json").read_text(encoding="utf-8"))["hash"]
    edicoes = curar_biblioteca.edicoes_aceitas(c3, "qwen2.5:7b", 1)
    assert len(edicoes) == 40, len(edicoes)
    tmp = Path(tempfile.mkdtemp(prefix="cura_"))
    _TEMPORARIOS.append(tmp)
    h_todas = curar_biblioteca.reconstruir(c3["bibliotecas"] / "qwen2.5_7b" / "epoca-0", tmp / "todas", edicoes)
    assert h_todas == oficial, (h_todas, oficial)
    h_menos = curar_biblioteca.reconstruir(c3["bibliotecas"] / "qwen2.5_7b" / "epoca-0", tmp / "menos", edicoes[1:])
    assert h_menos != oficial


# ----------------------------------------------------------------- 9. análise de fechamento da 3-B

# ! Alteração de IA - Revisar: testes de analisar_fase3b.py (01/10/2026), escritos antes do módulo
# existir: o pareamento caso a caso (ganhos, perdas, McNemar), a soma de dois conjuntos de casos
# disjuntos (36 oficiais + 36 inéditos), a contagem de casos que mudam entre corridas de L0, a leitura
# da linha FONTE com dois ids no mesmo colchete, a montagem completa sobre registros de mentira com
# --check, e a conferência dos números reais contra decisao_modelo.json quando a corrida oficial existe.
# ! Motivo: a análise da troca cruzada e das pontes decide como a Fase 3-B é lida no Memorial; a regra
# do projeto é nenhum número digitado à mão, então o script que gera as tabelas precisa de teste próprio
# (um pareamento com b e c trocados inverteria a conclusão sobre quem ganha com a biblioteca alheia).
def _reg_analise(modelo: str, epoca: int, caso: str, certo: bool, **extra) -> dict:
    base = {"modelo": modelo, "biblioteca_epoca": epoca, "caso": caso, "particao": "avaliacao",
            "causa_correta": certo, "causa_esperada": "campo_ausente",
            "causa_respondida": "campo_ausente" if certo else "corpo_vazio", "classe": 1, "nivel": 1,
            "segundos": 10.0, "tokens_entrada": 1000, "ouro_no_contexto": True,
            "contexto_com_nota": epoca > 0, "citou_verbete_anotado": False}
    return {**base, **extra}


def teste_analise3b_parear_conta_ganhos_e_perdas() -> None:
    import analisar_fase3b as an
    base = {c: _reg_analise("m", 0, c, v) for c, v in (("a", True), ("b", True), ("c", False), ("d", False))}
    nova = {c: _reg_analise("m", 1, c, v) for c, v in (("a", True), ("b", False), ("c", True), ("d", True))}
    par = an.parear(nova, base)
    assert (par["n_comuns"], par["b"], par["c"]) == (4, 2, 1), par
    assert par["ganhos"] == ["c", "d"] and par["perdas"] == ["b"], par
    assert par["delta_pp"] == 25.0 and par["p_mcnemar"] == 1.0, par
    # troca de rótulo é mais larga que troca de acerto: aqui os três casos que mudaram de acerto mudaram de rótulo,
    # e um quarto muda só o rótulo (errado nos dois lados)
    assert par["rotulos_diferentes"] == 3, par
    base["x"] = _reg_analise("m", 0, "x", False, causa_respondida="corpo_vazio")
    nova["x"] = _reg_analise("m", 1, "x", False, causa_respondida="corpo_nao_e_json")
    par_x = an.parear(nova, base)
    assert (par_x["b"], par_x["c"], par_x["rotulos_diferentes"]) == (2, 1, 4), par_x
    del base["x"], nova["x"]
    assert set(an.sem_casos(nova, {"b", "zz"})) == {"a", "c", "d"}
    # um caso que só existe de um lado não entra na conta
    nova["e"] = _reg_analise("m", 1, "e", True)
    assert an.parear(nova, base)["n_comuns"] == 4


def teste_analise3b_juntar_soma_conjuntos_disjuntos() -> None:
    import analisar_fase3b as an
    of_base = {"a": _reg_analise("m", 0, "a", False), "b": _reg_analise("m", 0, "b", True)}
    of_nova = {"a": _reg_analise("m", 1, "a", True), "b": _reg_analise("m", 1, "b", True)}
    in_base = {"a": _reg_analise("m", 0, "a", True)}   # mesmo id de caso em outro conjunto: não pode colidir
    in_nova = {"a": _reg_analise("m", 1, "a", False)}
    par = an.parear(an.juntar(oficiais=of_nova, ineditos=in_nova), an.juntar(oficiais=of_base, ineditos=in_base))
    assert (par["n_comuns"], par["b"], par["c"]) == (3, 1, 1), par
    assert par["ganhos"] == ["oficiais:a"] and par["perdas"] == ["ineditos:a"], par


def teste_analise3b_ruido_conta_casos_que_mudam_entre_corridas() -> None:
    import analisar_fase3b as an
    corridas = {
        "Fase 3": {c: _reg_analise("m", 0, c, v) for c, v in (("a", True), ("b", True), ("c", False))},
        "ponte 1": {c: _reg_analise("m", 0, c, v) for c, v in (("a", True), ("b", False), ("c", False))},
        "ponte 2": {c: _reg_analise("m", 0, c, v) for c, v in (("a", False), ("b", True), ("c", True))},
    }
    linhas = an.ruido_entre_corridas("m", corridas)
    por_par = {(l["corrida_a"], l["corrida_b"]): l for l in linhas}
    assert len(linhas) == 3, linhas
    assert por_par[("Fase 3", "ponte 1")]["discordantes"] == 1 and por_par[("Fase 3", "ponte 1")]["casos"] == ["b"]
    assert por_par[("Fase 3", "ponte 2")]["discordantes"] == 2
    assert por_par[("ponte 1", "ponte 2")]["discordantes"] == 3
    # sem informar caso de texto alterado, "com a mesma entrada" é igual ao total
    assert all(l["discordantes_mesma_entrada"] == l["discordantes"] for l in linhas), linhas
    # o caso "a" teve o texto corrigido antes da "ponte 2": sai das comparações que cruzam a correção e só delas
    linhas = an.ruido_entre_corridas("m", corridas, alterados={"a"}, depois={"ponte 2"})
    por_par = {(l["corrida_a"], l["corrida_b"]): l for l in linhas}
    assert por_par[("Fase 3", "ponte 1")]["discordantes_mesma_entrada"] == 1
    assert por_par[("Fase 3", "ponte 2")]["discordantes_mesma_entrada"] == 1 and por_par[("Fase 3", "ponte 2")]["discordantes"] == 2
    assert por_par[("ponte 1", "ponte 2")]["discordantes_mesma_entrada"] == 2
    assert por_par[("Fase 3", "ponte 2")]["casos_de_texto_alterado"] == ["a"] and por_par[("Fase 3", "ponte 1")]["casos_de_texto_alterado"] == []


def teste_analise3b_fontes_do_contexto() -> None:
    import analisar_fase3b as an
    r = {"resposta": "CAUSA_RAIZ: corpo_nao_e_json\nCAMPO: preco\nFONTE: [contrato-produto, corpo_nao_e_json]",
         "verbetes_ids": ["entidade-produto", "contrato-produto", "nulo_inesperado"]}
    assert an.fontes_do_contexto(r) == ["contrato-produto"], an.fontes_do_contexto(r)
    r2 = {"resposta": "FONTE: [entidade-produto], [nulo_inesperado]", "verbetes_ids": r["verbetes_ids"]}
    assert an.fontes_do_contexto(r2) == ["entidade-produto", "nulo_inesperado"]
    assert an.fontes_do_contexto({"resposta": "CAUSA_RAIZ: x", "verbetes_ids": ["a"]}) == []


def _dados_de_mentira_analise() -> dict:
    """Registros mínimos para montar a análise inteira: 1 doador, 2 leitores, 4 casos oficiais e 2 inéditos."""
    casos = ["a", "b", "c", "d"]
    f3, p1, p4, cru, ined = [], [], [], [], []
    for m, acertos_l0 in (("doador", "TTFF"), ("leitor-x", "TFTF"), ("leitor-y", "TTTF")):
        for c, v in zip(casos, acertos_l0):
            f3.append(_reg_analise(m, 0, c, v == "T"))
            p1.append(_reg_analise(m, 0, c, v == "T"))
            p4.append(_reg_analise(m, 0, c, v == "T"))
        for epoca in (1, 3):
            for c in casos:
                f3.append(_reg_analise(m, epoca, c, True if m == "doador" else c != "d"))
    for c in casos:   # leitor-x ganha "b" com a biblioteca do doador; leitor-y perde "a" e "b"
        for epoca in (1, 3):
            cru.append(_reg_analise("leitor-x", epoca, c, c != "d"))
            cru.append(_reg_analise("leitor-y", epoca, c, c == "c"))
    for m in ("doador", "leitor-y"):
        for epoca, padrao in ((0, "TF"), (1, "TT"), (3, "FF")):
            for c, v in zip(("n1", "n2"), padrao):
                ined.append(_reg_analise(m, epoca, c, v == "T"))
    brutos = {}
    for (m, epoca) in (("leitor-x", 1), ("leitor-x", 3), ("leitor-y", 1), ("leitor-y", 3)):
        brutos[("cruzada", m, epoca)] = {c: {"caso": c, "resposta": "CAUSA_RAIZ: z\nFONTE: [contrato-produto]",
                                             "verbetes_ids": ["contrato-produto", "campo_ausente"]} for c in casos}
    for m in ("leitor-x", "leitor-y"):
        brutos[("ponte", m, 0)] = {c: {"caso": c, "resposta": "CAUSA_RAIZ: z\nFONTE: [campo_ausente]",
                                       "verbetes_ids": ["contrato-produto", "campo_ausente"]} for c in casos}
    return {"f3": f3, "pontes": [("fase3b_ponte", "0.0.1", p1), ("fase3b_ponte_x", "0.0.4", p4)], "cruzada": cru, "ineditos": ined,
            "brutos": brutos, "corridas": [], "doador": "doador", "leitores": ["leitor-x", "leitor-y"],
            "casos_de_texto_alterado": frozenset({"a"}), "corridas_depois": frozenset({"fase3b_ponte_x", "cruzada"})}


def teste_analise3b_montar_render_e_check() -> None:
    import analisar_fase3b as an
    dado = an.montar(**_dados_de_mentira_analise())
    # pontes: nenhuma discordância contra a Fase 3 de mentira, todas pareáveis
    assert [p["saida"] for p in dado["pontes"]] == ["fase3b_ponte", "fase3b_ponte_x"]
    assert all(l["pareavel"] and l["b"] + l["c"] == 0 for p in dado["pontes"] for l in p["linhas"])
    # cruzada: leitor-x ganha 1 (b) e não perde contra o próprio L0 da ponte mais recente; leitor-y perde 2
    par = {(p["leitor"], p["biblioteca_epoca"], p["contra"]): p for p in dado["cruzada"]["pareados"]}
    assert (par[("leitor-x", 1, "l0_ponte")]["b"], par[("leitor-x", 1, "l0_ponte")]["c"]) == (1, 0), par[("leitor-x", 1, "l0_ponte")]
    assert (par[("leitor-y", 1, "l0_ponte")]["b"], par[("leitor-y", 1, "l0_ponte")]["c"]) == (0, 2)
    assert par[("leitor-y", 1, "doador")]["c"] == 3   # o doador acerta os 4 com a própria biblioteca; o leitor-y, 1
    assert {c["contra"] for c in dado["cruzada"]["pareados"]} == {"l0_ponte", "propria", "doador"}
    # o caso "a" teve o texto corrigido antes da ponte mais recente e da cruzada: contra a ponte (mesma época) nada
    # sai; contra a Fase 3 (antes da correção) o caso "a" sai da conta "com a mesma entrada"
    assert par[("leitor-y", 1, "l0_ponte")]["c_mesma_entrada"] == 2 and par[("leitor-y", 1, "l0_ponte")]["casos_de_texto_alterado"] == []
    assert (par[("leitor-y", 1, "propria")]["c"], par[("leitor-y", 1, "propria")]["c_mesma_entrada"]) == (2, 1), par[("leitor-y", 1, "propria")]
    assert par[("leitor-y", 1, "propria")]["casos_de_texto_alterado"] == ["a"]
    ponte_x = next(p for p in dado["pontes"] if p["saida"] == "fase3b_ponte_x")
    assert all("b_mesma_entrada" in l and "pareavel_mesma_entrada" in l for l in ponte_x["linhas"]), ponte_x
    assert all("discordantes_mesma_entrada" in l and "rotulos_diferentes" in l for l in dado["ruido_l0"]), dado["ruido_l0"][:1]
    # células: 2 leitores × (L0 Fase 3, L0 ponte, L1/L3 próprias, L1/L3 do doador) + doador × 4
    assert len(dado["cruzada"]["celulas"]) == 2 * 6 + 4, len(dado["cruzada"]["celulas"])
    # inéditos agrupados com os oficiais: 4 + 2 casos por linha
    assert all(l["n_comuns"] == 6 for l in dado["ineditos"]["agrupado"]), dado["ineditos"]["agrupado"]
    md = an.render(dado)
    for nome in ("tb_corridas", "tb_pontes", "tb_ruido", "tb_ineditos", "tb_agrupado", "tb_cruzada", "tb_cruzada_pareados",
                 "tb_cruzada_classe", "tb_cruzada_rotulos", "tb_cruzada_casos"):
        assert f"<!-- tabela:{nome} -->" in md and f"<!-- /tabela:{nome} -->" in md, nome
    assert "—" not in md and "→" not in md, "texto gerado com travessão ou seta"
    json.dumps(dado, ensure_ascii=False)   # serializável
    # --check: o documento que cola os blocos acusa um número alterado à mão
    tmp = Path(tempfile.mkdtemp(prefix="analise3b_"))
    _TEMPORARIOS.append(tmp)
    doc = tmp / "doc.md"
    doc.write_text("# x\n\n<!-- tabela:tb_pontes -->\n<!-- /tabela:tb_pontes -->\n", encoding="utf-8", newline="\n")
    n, mudou = an.colar(doc, md)
    assert (n, mudou) == (1, True) and an.conferir_doc(doc, md) == []
    doc.write_text(doc.read_text(encoding="utf-8").replace("| 0 | 0 |", "| 9 | 0 |", 1), encoding="utf-8", newline="\n")
    assert an.conferir_doc(doc, md) == ["tb_pontes"], an.conferir_doc(doc, md)


def teste_analise3b_numeros_reais_batem_com_a_decisao() -> None:
    """Com as corridas oficiais presentes: b e c das pontes iguais aos de decisao_modelo.json e o acerto de cada
    célula da cruzada igual ao resumo da própria corrida. Pulado quando a troca cruzada não está na máquina."""
    import analisar_fase3b as an
    cruzada = _RAIZ_OFICIAL_FASE3.parent / "fase3b_cruzada_qwen" / "resumo_fase3.json"
    decisao = _RAIZ_OFICIAL_FASE3 / "decisao_modelo.json"
    if not cruzada.exists() or not decisao.exists() or caminhos.fase3("fase3")["raiz"] != _RAIZ_OFICIAL_FASE3:
        print("teste_analise3b_numeros_reais_batem_com_a_decisao: pulado (sem a corrida oficial ou sem RESULTADOS_DIR=resultados_alvo)")
        return
    dado = an.montar(**an.carregar())
    tres_b = json.loads(decisao.read_text(encoding="utf-8"))["tres_b"]
    for ponte in dado["pontes"]:
        if ponte["saida"] not in tres_b:
            continue
        esperado = {l["modelo"]: (l["pareado_vs_f3"]["b"], l["pareado_vs_f3"]["c"]) for l in tres_b[ponte["saida"]]["linhas"]}
        assert {l["modelo"]: (l["b"], l["c"]) for l in ponte["linhas"]} == esperado, ponte["saida"]
    resumo = json.loads(cruzada.read_text(encoding="utf-8"))
    oficial = {(x["modelo"], x["biblioteca_epoca"]): x["causa_correta_pct"] for x in resumo["por_modelo_biblioteca_particao"]
               if x["particao"] == "avaliacao"}
    medido = {(c["leitor"], c["biblioteca_epoca"]): c["acerto_pct"] for c in dado["cruzada"]["celulas"] if c["origem"] == "cruzada"}
    assert medido == oficial, (medido, oficial)
    assert all(c["versoes_ollama"] == ["0.34.4"] for c in dado["corridas"] if c["saida"] in ("fase3b_cruzada_qwen", "fase3b_ponte_0344")), dado["corridas"]


def teste_area_oficial_hash_depois() -> None:
    """Repete o hash de teste_area_oficial_hash_antes ao fim da suíte — precisa ser o ÚLTIMO
    teste definido no arquivo, para rodar depois de todos os outros."""
    assert _HASH_ANTES, "teste_area_oficial_hash_antes não rodou antes deste"
    agora_base = _hash_arvore(bib.BASE)
    assert agora_base == _HASH_ANTES["base_conhecimento"], (
        f"base_conhecimento/ mudou durante os testes da Fase 3-B: "
        f"{_HASH_ANTES['base_conhecimento']} -> {agora_base}")
    agora_fase3 = _hash_arvore(_RAIZ_OFICIAL_FASE3)
    assert agora_fase3 == _HASH_ANTES["fase3_oficial"], (
        f"resultados_alvo/fase3/ mudou durante os testes da Fase 3-B: "
        f"{_HASH_ANTES['fase3_oficial']} -> {agora_fase3}")


# --------------------------------------------------------------------------------- runner

def main() -> None:
    modulo = sys.modules[__name__]
    testes = [(nome, obj) for nome, obj in vars(modulo).items()
              if nome.startswith("teste_") and inspect.isfunction(obj)
              and obj.__module__ == modulo.__name__]
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
        # ! Alteração de IA - Revisar: limpa tanto _TEMPORARIOS deste arquivo quanto o de
        # testar_fase3 (importado para reaproveitar _com_stubs/_arvore_fase3_sintetica, que
        # gravam pastas de mentira na lista DELE, não nesta).
        # ! Motivo: sem limpar as duas listas, cada rodada de testar_fase3b.py deixaria para
        # trás as pastas temporárias criadas pelas funções reaproveitadas de testar_fase3, do
        # mesmo jeito que %TEMP% cresceria se testar_fase3.py não limpasse a própria lista.
        for caminho in _TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)
        for caminho in testar_fase3._TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)


if __name__ == "__main__":
    main()
