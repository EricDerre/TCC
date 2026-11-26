#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (25/11/2026, ficha 109, decisão 170): os testes do hub como central aberta pelo `Cobaia.exe`, no mesmo
# formato sem pytest de `testar_hub.py`, de quem este arquivo reaproveita os ajudantes. Cobrem: o `run.py` subindo o hub com o Python da venv
# do AgenteCore e encerrando os três processos; o `Cobaia.py` abrindo uma aba só, no hub, e voltando ao site e à API quando o hub não sobe; a
# opção `--cobaias-no-ar` do executor, desligada por padrão; a corrida lançada pelo hub aberto pelo `.exe` (o executor chamado direto, com as
# cobaias já no ar e o Ollama conferido antes); a conferência do Ollama, com a sonda, a procura do programa e o início dele de mentira; a
# descoberta da corrida lançada pelo hub na lista de casos; o estado dos serviços e os atalhos (`/api/central`); as métricas por corrida
# lidas dos registros (`/api/metricas`), com o tempo de reparo da 28b e da 21d conferido contra as leituras gravadas da Fase 5 e da Fase 4;
# e, na página, a tela "Início" e a vista "Métricas".
# Escritos ANTES do código: a primeira rodada falhou por AttributeError em `run.comando_do_hub` e, feito o `run.py`, em `hub.comando_direto`.
# ! Motivo: o Eric pediu que o hub seja a central de tudo, aberta pelo `.exe`, de onde se rodam os testes e se veem as métricas. Os testes
# ficam num arquivo próprio para a contagem de `testar_hub.py`, que `resultados_alvo/fase4/hub.json` e os textos do pacote Q6 citam, não mudar.
# Nenhum deles sobe o site, a API, o banco, o Ollama ou o modelo: os processos, a sonda das portas e o Ollama são de mentira.
"""Testes do hub como central aberta pelo Cobaia.exe (ficha 109), sem pytest. Uso (em Programacao/AgenteCore/experimentos):
  PYTHONIOENCODING=utf-8 ../.venv/Scripts/python.exe testar_central.py     # todos, com o Chromium do Playwright sem janela
  PYTHONIOENCODING=utf-8 python testar_central.py                          # os da página são pulados com aviso
"""
import argparse
import inspect
import json
import shutil
import statistics
import sys
import traceback
from pathlib import Path

EXP = Path(__file__).resolve().parent
RAIZ = EXP.parent.parent.parent
RA = EXP / "resultados_alvo"
for pasta in (str(EXP), str(RAIZ)):
    if pasta not in sys.path:
        sys.path.insert(0, pasta)

import hub
import hub_dados as hd
import testar_hub as th
import testar_pos_fase4 as tp4

_TEMPORARIOS = tp4._TEMPORARIOS
_erro, _json, _http, _hub_no_ar, _navegador, _acervo_de_teste, _esperar_texto, _ate = (th._erro, th._json, th._http, th._hub_no_ar, th._navegador, th._acervo_de_teste,
                                                                                  th._esperar_texto, th._ate)


class ProcessoDeMentira:
    """Um processo que já terminou (ou não), para os testes do `run.py` e do `Cobaia.py` não subirem nada."""

    def __init__(self, vivo: bool = True) -> None:
        self.vivo, self.encerrado = vivo, False

    def poll(self):
        return None if self.vivo else 0

    def terminate(self) -> None:
        self.encerrado, self.vivo = True, False


def _acervo_que_descobre() -> tuple[hd.Acervo, Path]:
    """As duas corridas de mentira de `testar_hub`, num acervo que também procura as corridas lançadas pelo hub (o padrão de `python hub.py`)."""
    fixo, raiz = _acervo_de_teste()
    return hd.Acervo(raiz, corridas=("c1", "c2"), leituras=fixo.leituras), raiz


def _corrida_do_hub(raiz: Path, nome: str = "hub_20261125_230000") -> Path:
    """Uma corrida como a que o botão do hub lança: a trilha de `c2` com o nome da pasta nova nos identificadores (como o executor grava) e
    um `cenarios.jsonl` de duas execuções, uma de cada cenário."""
    pasta = raiz / nome
    pasta.mkdir()
    trilha_de_c2 = (raiz / "c2" / "trilha_tela.jsonl").read_text(encoding="utf-8")
    assert '"c2/qwen2.5_7b/' in trilha_de_c2
    (pasta / "trilha_tela.jsonl").write_text(trilha_de_c2.replace('"c2/qwen2.5_7b/', f'"{nome}/qwen2.5_7b/'), encoding="utf-8")
    shutil.copy(raiz / "c2" / "condicoes_fase4.json", pasta / "condicoes_fase4.json")
    linhas = [{"cenario": "contrato-field_missing", "repeticao": 1, "task_success": True, "detectou": True, "mttr_s": 60.0, "tipo": "contrato"},
              {"cenario": "localizador-front-busca", "repeticao": 1, "task_success": False, "detectou": True, "mttr_s": 80.0, "tipo": "localizador"}]
    (pasta / "cenarios.jsonl").write_text("".join(json.dumps(l) + "\n" for l in linhas), encoding="utf-8")
    return pasta


# ------------------------------------------------------------------ o run.py e o Cobaia.py

def teste_run_sobe_o_hub_com_o_python_da_venv_do_agente_e_encerra_os_tres():
    import run
    agente = tp4._temp() / "AgenteCore"
    assert run.comando_do_hub(agente=agente) is None, "sem a venv do AgenteCore não há como subir o hub"
    python = agente / ".venv" / ("Scripts/python.exe" if run.OS_NAME == "Windows" else "bin/python")
    python.parent.mkdir(parents=True)
    python.write_text("", encoding="utf-8")
    assert run.comando_do_hub(agente=agente) is None, "sem o hub.py também não"
    (agente / "experimentos").mkdir()
    (agente / "experimentos" / "hub.py").write_text("", encoding="utf-8")
    comando = run.comando_do_hub(agente=agente)
    assert comando == [str(python), str(agente / "experimentos" / "hub.py"), "--sem-abrir", "--porta", str(run.HUB_PORT), "--pelo-exe"], comando
    assert run.HUB_PORT == hub.PORTA_PADRAO == 8765 and run.HUB_PORT not in (run.FRONT_PORT, run.API_PORT)
    chamadas = []
    antigos = run.subprocess.Popen, run.stop_managed_mariadbd
    try:
        run.subprocess.Popen = lambda cmd, **k: chamadas.append((cmd, k)) or ProcessoDeMentira()
        run.stop_managed_mariadbd = lambda: chamadas.append("banco parado")
        assert run.start_hub(agente=tp4._temp()) is None and chamadas == [], "sem o que subir, nada é lançado"
        proc = run.start_hub(agente=agente)
        assert isinstance(proc, ProcessoDeMentira) and chamadas[0][0] == comando and chamadas[0][1]["cwd"] == str(agente / "experimentos")
        front, api, do_hub = ProcessoDeMentira(vivo=False), ProcessoDeMentira(), ProcessoDeMentira()
        run.wait_and_cleanup(front, api, do_hub)
        assert api.encerrado and do_hub.encerrado and chamadas[-1] == "banco parado", "o site caiu: a API, o hub e o banco são encerrados"
        front2, api2 = ProcessoDeMentira(vivo=False), ProcessoDeMentira()
        run.wait_and_cleanup(front2, api2, None)
        assert api2.encerrado, "sem hub (None), o encerramento é o de antes"
    finally:
        run.subprocess.Popen, run.stop_managed_mariadbd = antigos


def teste_cobaia_abre_so_o_hub_e_volta_ao_site_e_a_api_quando_o_hub_nao_sobe():
    import Cobaia
    import install
    import run
    abertos, limpeza = [], []
    guardados = {(m, n): getattr(m, n) for m, n in ((install, "main"), (run, "start_services"), (run, "start_hub"), (run, "wait_until_ready"), (run, "wait_for_port"),
                                                    (run, "wait_and_cleanup"), (Cobaia.webbrowser, "open"))}
    front, api, do_hub = ProcessoDeMentira(), ProcessoDeMentira(), ProcessoDeMentira()
    try:
        install.main = lambda: 0
        run.start_services = lambda: (front, api)
        run.wait_until_ready = lambda *a, **k: True
        run.wait_and_cleanup = lambda *procs: limpeza.append(procs)
        Cobaia.webbrowser.open = lambda url: abertos.append(url)
        run.start_hub = lambda: do_hub
        run.wait_for_port = lambda porta, timeout_s=30: porta == run.HUB_PORT
        Cobaia.main()
        assert abertos == [f"http://127.0.0.1:{run.HUB_PORT}/"], abertos
        assert limpeza == [(front, api, do_hub)], "fechar a janela encerra os três"
        for caso in ("o hub não foi lançado", "o hub foi lançado e a porta não respondeu"):
            abertos.clear()
            limpeza.clear()
            run.start_hub = (lambda: None) if caso.startswith("o hub não foi") else (lambda: do_hub)
            run.wait_for_port = lambda porta, timeout_s=30: False
            Cobaia.main()
            assert abertos == [f"http://localhost:{run.FRONT_PORT}", f"http://localhost:{run.API_PORT}/docs"], (caso, abertos)
            assert len(limpeza) == 1 and limpeza[0][:2] == (front, api), caso
    finally:
        for (modulo, nome), valor in guardados.items():
            setattr(modulo, nome, valor)


# ------------------------------------------------------------------ o executor com as cobaias já no ar

def teste_executor_cobaias_no_ar_vem_desligado_e_nao_sobe_nem_derruba_nada():
    import executar_fase4 as ex
    padrao = ex.montar_parser().parse_args(["--modo", "cenarios", "--saida", "qualquer"])
    assert padrao.cobaias_no_ar is False, "desligado por padrão: a corrida de sempre sobe e derruba o site, a API e o banco"
    ligado = ex.montar_parser().parse_args(["--modo", "cenarios", "--saida", "qualquer", "--cobaias-no-ar"])
    chamadas = []
    assert ex.subir_cobaias(padrao, iniciar=lambda: chamadas.append("subiu") or ("front", "api")) == ("front", "api") and chamadas == ["subiu"]
    assert ex.subir_cobaias(ligado, iniciar=lambda: chamadas.append("subiu de novo")) == (None, None) and chamadas == ["subiu"], "com as cobaias já no ar, nada é lançado"
    import _env_common as env
    antigos = ex.ligar_modo, env.stop_managed_mariadbd
    try:
        ex.ligar_modo = lambda modo, campo, token: chamadas.append(("modo", modo))
        env.stop_managed_mariadbd = lambda: chamadas.append("banco parado")
        ex.derrubar_cobaias(None, None, "token", parar_banco=False)
        assert chamadas[-1] == ("modo", "normal") and "banco parado" not in chamadas, "a API volta ao modo normal, e o banco do site que está no ar continua de pé"
        ex.derrubar_cobaias(None, None, "token")
        assert chamadas[-1] == "banco parado", "sem a opção, o fim da corrida é o de sempre"
    finally:
        ex.ligar_modo, env.stop_managed_mariadbd = antigos
    fonte = inspect.getsource(ex.rodar_cenarios)
    assert "front, api = subir_cobaias(args)" in fonte and "derrubar_cobaias(front, api, args.token, parar_banco=not args.cobaias_no_ar)" in fonte


# ------------------------------------------------------------------ a corrida lançada pelo hub aberto pelo .exe

def teste_hub_pelo_exe_chama_o_executor_direto_com_as_cobaias_no_ar_e_confere_o_ollama_antes():
    direto = hub.comando_direto("hub_x", {"repeticoes": 2, "selecao": "todos", "desde": None}, python="py")
    assert direto == ["py", "executar_fase4.py", "--modo", "cenarios", "--saida", "hub_x", "--casos", "10", "--repeticoes", "2", "--cobaias-no-ar"], direto
    assert hub.comando_direto("hub_x", {"repeticoes": 1, "selecao": "git", "desde": "abc1234"}, python="py")[-4:] == ["--selecao", "git", "--desde", "abc1234"]
    acervo, raiz = _acervo_de_teste()
    passos = []

    def lancador(saida, opcoes):
        passos.append("lançou")
        return [sys.executable, "-c", "import os; print('RESULTADOS_DIR=' + os.environ.get('RESULTADOS_DIR', '(vazio)') + ' fim')"]

    assert hub.pasta_dos_resultados(hub.RESULTADOS) == "resultados_alvo", "a pasta padrão vai pelo nome, como o `rodar_fase4.ps1` manda"
    assert hub.pasta_dos_resultados(raiz) == str(raiz), "outra pasta de resultados vai pelo caminho inteiro, para a corrida cair onde o hub lê"
    with _hub_no_ar(acervo, pelo_exe=True, comando_da_corrida=lancador, garantir_ollama=lambda: passos.append("ollama") and None) as (base, _, _srv):
        e = _json(base, "GET", "/api/execucao")[1]
        assert e["permitida"] is True and e["pelo_exe"] is True, "aberto pelo .exe, o botão vem liberado"
        assert "executar_fase4.py" in e["comando_sugerido"] and "--cobaias-no-ar" in e["comando_sugerido"] and "rodar_fase4.ps1" not in e["comando_sugerido"], e["comando_sugerido"]
        assert _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1})[0] == 200 and passos == ["ollama", "lançou"], passos
        fim = _ate(lambda: _json(base, "GET", "/api/execucao")[1], lambda d: d["terminou"])
        assert fim["codigo"] == 0 and f"RESULTADOS_DIR={raiz} fim" in fim["log"], fim["log"]
    with _hub_no_ar(acervo, pelo_exe=True, comando_da_corrida=lancador, garantir_ollama=lambda: "o Ollama não respondeu em 30 s") as (base, _, _srv):
        passos.clear()
        status, r = _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1})
        assert status == 409 and "Ollama" in r["erro"] and passos == [], "sem o Ollama no ar, a corrida nem é lançada, e a página diz por quê"
    with _hub_no_ar(acervo) as (base, _, _srv):
        e = _json(base, "GET", "/api/execucao")[1]
        assert e["permitida"] is False and e["pelo_exe"] is False and "rodar_fase4.ps1" in e["comando_sugerido"], "`python hub.py` sozinho continua só mostrando o comando"
    args = hub.argumentos(["--pelo-exe", "--sem-abrir"])
    assert args.pelo_exe is True and hub.argumentos([]).pelo_exe is False


def teste_garantir_ollama_so_inicia_o_que_nao_responde_e_diz_por_que_nao_deu():
    lancados = []
    lancar = lambda programa: lancados.append(programa)
    assert hub.garantir_ollama_no_ar(espera_s=1, sonda=lambda porta: True, achar=lambda: "ollama.exe", lancar=lancar) is None and lancados == [], "já no ar: nada é iniciado"
    falta = hub.garantir_ollama_no_ar(espera_s=1, sonda=lambda porta: False, achar=lambda: None, lancar=lancar)
    assert "Ollama" in falta and "instalador" in falta and lancados == [], falta
    respostas = iter([False, False, True])
    assert hub.garantir_ollama_no_ar(espera_s=5, sonda=lambda porta: next(respostas), achar=lambda: "ollama.exe", lancar=lancar, pausa_s=0.01) is None
    assert lancados == ["ollama.exe"], "fora do ar e instalado: o hub inicia o servidor do Ollama e espera a porta responder"
    portas = []
    mudo = hub.garantir_ollama_no_ar(espera_s=0.05, sonda=lambda porta: portas.append(porta) and False, achar=lambda: "ollama.exe", lancar=lancar, pausa_s=0.01)
    assert "Ollama" in mudo and "não respondeu" in mudo and set(portas) == {hub.PORTA_DO_OLLAMA} and hub.PORTA_DO_OLLAMA == 11434, mudo

    def quebra(programa):
        raise OSError("acesso negado")

    assert "acesso negado" in hub.garantir_ollama_no_ar(espera_s=1, sonda=lambda porta: False, achar=lambda: "ollama.exe", lancar=quebra)


def teste_acervo_descobre_a_corrida_lancada_pelo_hub():
    acervo, raiz = _acervo_que_descobre()
    assert [c["pasta"] for c in acervo.corridas()] == ["c1", "c2"] and len(acervo.indice()) == 3
    _corrida_do_hub(raiz)
    (raiz / "hub_sem_trilha").mkdir()
    (raiz / "outra_pasta").mkdir()
    shutil.copy(raiz / "c2" / "trilha_tela.jsonl", raiz / "outra_pasta" / "trilha_tela.jsonl")
    corridas = acervo.corridas()
    assert [c["pasta"] for c in corridas] == ["c1", "c2", "hub_20261125_230000"], "só entra a pasta `hub_...` que tem trilha"
    assert "pelo hub" in corridas[-1]["rotulo"] and corridas[-1]["casos"] == 2 and len(acervo.indice()) == 5
    nova = next(l for l in acervo.indice() if l["corrida"] == "hub_20261125_230000")
    assert acervo.caso(nova["tid"])["corrida"]["pasta"] == "hub_20261125_230000", "o caso da corrida nova abre como os outros"
    fixo = hd.Acervo(raiz, corridas=("c1",), descobrir=False)
    assert [c["pasta"] for c in fixo.corridas()] == ["c1"], "quem pede corridas fixas pode desligar a descoberta"


# ------------------------------------------------------------------ o início e as métricas

def teste_central_diz_o_estado_dos_servicos_e_da_os_atalhos():
    acervo, _ = _acervo_de_teste()
    with _hub_no_ar(acervo, sonda=lambda porta: porta == 8080, ollama_no_ar=lambda: False) as (base, _, _srv):
        status, c = _json(base, "GET", "/api/central")
        por = {s["id"]: s for s in c["servicos"]}
        assert status == 200 and list(por) == ["site", "api", "ollama", "hub"], list(por)
        assert por["site"] == {"id": "site", "nome": por["site"]["nome"], "url": "http://localhost:8080", "no_ar": True} and por["api"]["no_ar"] is False
        assert por["api"]["url"] == "http://localhost:8000/docs" and por["ollama"]["no_ar"] is False and por["ollama"]["url"] is None and por["hub"]["no_ar"] is True
        assert c["painel"].startswith("https://claude.ai/artifact/") and c["pelo_exe"] is False and c["execucao_permitida"] is False
        assert c["casos"] == 3 and c["corridas"] == 2
    with _hub_no_ar(acervo, pelo_exe=True, sonda=lambda porta: True, ollama_no_ar=lambda: True, garantir_ollama=lambda: None) as (base, _, _srv):
        c = _json(base, "GET", "/api/central")[1]
        assert c["pelo_exe"] is True and c["execucao_permitida"] is True and all(s["no_ar"] for s in c["servicos"])


def teste_metricas_por_corrida_saem_dos_registros_e_o_alto_do_resultado_da_fase_5():
    m = hd.metricas(hd.Acervo(RA))
    por = {c["pasta"]: c for c in m["corridas"]}
    assert list(por) == [c["pasta"] for c in hd.CORRIDAS_PADRAO] + [p for p in por if p.startswith("hub_")]
    registros = [json.loads(l) for l in (RA / "fase5_agente_b" / "cenarios.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    b = por["fase5_agente_b"]
    por_cenario: dict[str, list[float]] = {}
    for r in registros:
        if r.get("mttr_s") is not None:
            por_cenario.setdefault(r["cenario"], []).append(r["mttr_s"])
    media_dos_cenarios = statistics.fmean(statistics.fmean(t) for t in por_cenario.values())
    assert b["execucoes"] == len(registros) and b["task_success"] == sum(1 for r in registros if r["task_success"]) and b["detectou"] == sum(1 for r in registros if r["detectou"])
    assert b["mttr_media_s"] == round(media_dos_cenarios, 1) and b["cenarios_com_tempo"] == len(por_cenario), b["mttr_media_s"]
    oficial = json.loads((RA / "fase5" / "medicao.json").read_text(encoding="utf-8"))["lados"]["agente"]["geral"]["tempo_media_s"]
    assert b["mttr_media_s"] == round(oficial, 1), "o tempo de reparo da 28b no hub é o da leitura da Fase 5: a média dos cenários, não a das execuções"
    assert len(b["por_cenario"]) == len({r["cenario"] for r in registros}) and sum(x["execucoes"] for x in b["por_cenario"]) == len(registros)
    assert b["casos"] == b["execucoes"] and b["vale_como_medida"] is True and por["fase4_ensaio_v4"]["execucoes"] == 10
    ensaio = json.loads((RA / "fase4" / "cenarios_v4.json").read_text(encoding="utf-8"))["geral"]
    assert por["fase4_ensaio_v4"]["mttr_media_s"] == round(ensaio["mttr_media_s"], 1) and por["fase4_ensaio_v4"]["task_success"] == ensaio["sucessos"], "a 21d bate com a leitura da Fase 4"
    t = por["fase4_ineditos"]
    assert t["execucoes"] is None and t["task_success"] is None and t["casos"] == 36 and sum(t["confianca"].values()) == 36, "corrida em texto: só os casos e a confiança"
    assert list(t["confianca"]) == [n for n in ("alta", "média", "baixa") if n in t["confianca"]], "a confiança sai sempre na mesma ordem: alta, média, baixa"
    medicao = json.loads((RA / "fase5" / "medicao.json").read_text(encoding="utf-8"))
    f5 = m["fase5"]
    assert f5["tempo"] == medicao["tempo"]["geral"]["frase"] and f5["task_success"] == medicao["task_success"]["frase"]
    assert f5["agente"] == {"sucessos": medicao["task_success"]["agente"]["sucessos"], "n": medicao["task_success"]["agente"]["n"]}
    assert f5["pessoas"] == {"sucessos": medicao["task_success"]["pessoas"]["sucessos"], "n": medicao["task_success"]["pessoas"]["n"]}
    assert f5["ressalva"] and "integrante" in f5["ressalva"], "o veredito do Task Success vai sempre com a ressalva (decisão 151)"
    acervo, raiz = _acervo_que_descobre()
    _corrida_do_hub(raiz)
    sintetica = {c["pasta"]: c for c in hd.metricas(acervo)["corridas"]}
    h = sintetica["hub_20261125_230000"]
    assert h["execucoes"] == 2 and h["task_success"] == 1 and h["mttr_media_s"] == 70.0 and h["vale_como_medida"] is False, h
    assert sintetica["c1"]["execucoes"] is None and sintetica["c1"]["vale_como_medida"] is None, "de uma pasta que o hub não conhece, ele não diz se é medida"
    assert hd.metricas(acervo)["fase5"] is None, "sem medicao.json não há resultado da Fase 5 a mostrar"
    with _hub_no_ar(acervo) as (base, _, _srv):
        status, dado = _json(base, "GET", "/api/metricas")
        assert status == 200 and [c["pasta"] for c in dado["corridas"]] == ["c1", "c2", "hub_20261125_230000"]


def teste_pagina_inicio_mostra_os_servicos_leva_as_metricas_e_a_rodar():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, raiz = _acervo_que_descobre()
        _corrida_do_hub(raiz)
        with _hub_no_ar(acervo, pelo_exe=True, sonda=lambda porta: porta == 8080, ollama_no_ar=lambda: False, garantir_ollama=lambda: "sem Ollama no teste",
                        comando_da_corrida=lambda saida, opcoes: [sys.executable, "-c", "print('nunca roda')"]) as (base, _, _srv):
            pagina.goto(base + "/")
            pagina.wait_for_selector("#inicio .servico")
            assert pagina.is_visible("#inicio") and pagina.is_hidden("#caso") and pagina.is_hidden("#metricas") and pagina.is_hidden("#ao-vivo")
            assert pagina.locator("#inicio .servico").count() == 4
            assert "no ar" in pagina.inner_text('#inicio .servico[data-servico="site"]') and "fora do ar" in pagina.inner_text('#inicio .servico[data-servico="api"]')
            assert pagina.get_attribute('#inicio .servico[data-servico="site"] a', "href") == "http://localhost:8080"
            assert pagina.get_attribute("#inicio a.painel", "href").startswith("https://claude.ai/artifact/")
            assert "5 casos" in pagina.inner_text("#inicio")
            pagina.click("#ir-para-metricas")
            pagina.wait_for_selector("#metricas tr.corrida")
            assert pagina.is_visible("#metricas") and pagina.is_hidden("#inicio") and pagina.locator("#metricas tr.corrida").count() == 3
            linha = pagina.inner_text('#metricas tr.corrida[data-corrida="hub_20261125_230000"]')
            assert "1 de 2" in linha and "70,0" in linha and "não" in linha, linha
            pagina.click("#abrir-inicio")
            pagina.wait_for_selector("#inicio:visible")
            pagina.click("#ir-para-rodar")
            pagina.wait_for_selector("#rodar-cenarios:visible")
            assert pagina.is_visible("#ao-vivo") and pagina.is_hidden("#inicio")
            pagina.click("#rodar-cenarios")
            _esperar_texto(pagina, "#erro", "Ollama")
            pagina.click("#lista-de-casos .item-caso >> nth=0")
            pagina.wait_for_selector("#caso section.bloco")
            assert pagina.is_hidden("#inicio") and pagina.is_hidden("#ao-vivo")
            pagina.click("#abrir-metricas")
            pagina.wait_for_selector("#metricas:visible")
            pagina.reload()
            pagina.wait_for_selector("#metricas tr.corrida")
            assert pagina.is_visible("#metricas"), "o endereço guarda a vista"
        assert [e for e in erros if "status of 409" not in e] == [], erros


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    modulo = sys.modules[__name__]
    testes = [(nome, obj) for nome, obj in vars(modulo).items()
              if nome.startswith("teste_") and inspect.isfunction(obj) and obj.__module__ == modulo.__name__]
    try:
        for nome, funcao in testes:
            try:
                funcao()
            except Exception:  # noqa: BLE001 - o runner pega qualquer falha do teste para imprimir o rastro e parar com código 1
                print(nome)
                traceback.print_exc()
                sys.exit(1)
            print(f"{nome} ok")
        if th._PULADOS:
            print(f"aviso: {len(th._PULADOS)} teste(s) da página pulado(s), sem o Playwright neste Python")
        print(f"{len(testes)} testes ok")
    finally:
        for caminho in _TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)


if __name__ == "__main__":
    main()
