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
    """Sem banco_casos_ineditos.py no repositório (situação atual — o módulo é preparado numa
    tarefa futura), modo_ineditos para ANTES de tocar em disco ou no Ollama, com SystemExit de
    código 2 e uma mensagem clara no stderr."""
    assert "banco_casos_ineditos" not in sys.modules, (
        "banco_casos_ineditos já foi importado nesta sessão — este teste presume que o "
        "módulo não existe no repositório")
    args = argparse.Namespace(
        saida="fase3b_ineditos_teste", modelos=[_MODELO_TESTE], versoes=None, casos=0, k=3,
        max_tokens_diagnostico=600, max_tokens_proposta=700)
    erro = io.StringIO()
    try:
        with contextlib.redirect_stderr(erro):
            executar_fase3b.modo_ineditos(args)
        assert False, "modo_ineditos deveria ter parado sem banco_casos_ineditos.py"
    except SystemExit as e:
        assert e.code == 2, e.code
    assert "banco_casos_ineditos" in erro.getvalue(), erro.getvalue()


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
